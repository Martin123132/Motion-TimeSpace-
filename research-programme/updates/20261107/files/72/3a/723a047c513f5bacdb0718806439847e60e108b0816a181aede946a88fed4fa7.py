from cold40960_common import *
from build_dc_cache import spline_map
from build_matched_sources import SourceQuadrature
from propagate_matched_feedback import solve_response
from propagate_repaired_feedback import readout
import argparse
import time


def compress_dc(basis,prediction,upper):
    grid=prediction['frequency']
    quadrature=SourceQuadrature(basis,grid,np.array([0]),upper,32)
    soft_matrix=np.stack([np.bincount(quadrature.soft_indices,weights=row,minlength=len(quadrature.soft)) for row in quadrature.dc_matrix])
    template=interpolate.make_interp_spline(np.log(grid),np.zeros(len(grid)),k=3)
    nodes=interpolate.BSpline.design_matrix(np.log(grid),template.t,3).tocsc()
    matrix=np.zeros((basis.count,len(grid)))
    for points,operator,sign in [(quadrature.soft,soft_matrix,1),(quadrature.hard,quadrature.dc_matrix,1),(quadrature.seed,quadrature.dc_matrix,-1)]:
        selected,design=spline_map(points,grid,upper,template.t)
        matrix+=sign*np.asarray(design.T@operator[:,selected].T).T
    compressed=sparse_linalg.splu(nodes.T.tocsc()).solve(matrix.T).T
    checks=[check('DC event energy identity',quadrature.event_energy_defect,1e-12)]
    for epoch in [16,32,64]:
        values=prediction['defect'][epoch]
        soft=compact_defect(quadrature.soft,grid,values,upper)
        hard=compact_defect(quadrature.hard,grid,values,upper)
        seed=compact_defect(quadrature.seed,grid,values,upper)
        jump=soft[quadrature.soft_indices]+hard-seed
        direct=quadrature.dc_matrix@jump
        operand=np.maximum(np.linalg.norm(abs(quadrature.dc_matrix)@abs(jump),axis=0),1e-300)
        checks.append(check('Compressed three-leg DC versus direct:'+str(epoch),float(np.max(np.linalg.norm(compressed@values-direct,axis=0)/operand)),1e-9))
    cache=dict(frequency=quadrature.frequency,projection=quadrature.projection,measure=quadrature.measure,
        dc_operator=compressed,inner_frequency=grid,upper=upper)
    return cache,checks


def sources(basis,ladder,prediction,cache,events,background,emission,free_free,upper):
    raw,represented,projections,moments,raw_norm,unresolved_norm,projection_changes=[],[],[],[],[],[],[]
    bank_at=interpolate.interp1d(prediction['coefficient_knots'],prediction['coefficient_bank'],axis=0,bounds_error=True)
    errors={key:0. for key in ['mass_projection','dc_energy','compton_number','dc_represented_energy','compton_represented_number','source_decomposition']}
    for epoch,coordinate in enumerate(prediction['coordinate']):
        theta=background.at(float(coordinate))['thermal_parameter']
        values=prediction['defect'][epoch]
        canonical=compact_defect(basis.nodes,prediction['frequency'],values,upper)
        quadrature=compact_defect(cache['frequency'],prediction['frequency'],values,upper)
        event_values=compact_defect(events['frequency'],prediction['frequency'],values,upper)
        moment=(basis.values.T*basis.measure)@canonical
        projected=linalg.solve(basis.mass,moment,assume_a='pos')
        refined=cache['projection']@quadrature
        projection_changes.append(linalg.solve(basis.mass,refined-moment,assume_a='pos'))
        scattering=events['adjoint'][epoch]@event_values
        kappa=bank_at(coordinate)[len(prediction['offsets'])+1]
        dc=kappa*(cache['dc_operator']@values)
        br=-cache['projection']@(free_free.br_rates(theta)[:,None]*quadrature)
        source=np.stack([scattering,dc,br])
        operators=np.stack([ladder.at(theta,0)[:96,:96],-emission.at(theta,'dc'),-emission.interpolator(math.log(theta))])
        old=np.einsum('tij,jk->tik',operators,projected)
        projection_scale=np.maximum(np.linalg.norm(moment,axis=0),1e-300)
        errors['mass_projection']=max(errors['mass_projection'],float(np.max(np.linalg.norm(basis.mass@projected-moment,axis=0)/projection_scale)))
        for name,vector,row in [('dc_energy',dc,basis.temperature),('compton_number',scattering,basis.chemical),
                ('dc_represented_energy',old[1],basis.temperature),('compton_represented_number',old[0],basis.chemical)]:
            scale=np.maximum(abs(row)@abs(vector),1e-300)
            errors[name]=max(errors[name],float(np.max(abs(row@vector)/scale)))
        combined=(ladder.at(theta,0)[:96,:96]-emission.at(theta,'dcbr'))@projected
        operand=np.maximum(np.linalg.norm(abs(operators).sum(axis=0)@abs(projected),axis=0),1e-300)
        errors['source_decomposition']=max(errors['source_decomposition'],float(np.max(np.linalg.norm(old.sum(axis=0)-combined,axis=0)/operand)))
        raw.append(source)
        represented.append(old)
        projections.append(projected)
        moments.append(moment)
        raw_norm.append(norm(canonical,basis.measure))
        unresolved_norm.append(norm(canonical-basis.values@projected,basis.measure))
    raw,represented=np.array(raw),np.array(represented)
    source=raw-represented
    result=dict(coordinate=prediction['coordinate'],source=source,raw_source=raw,overlap_source=represented,
        projected_replacement=np.array(projections),replacement_moments=np.array(moments),replacement_norm=np.array(raw_norm),
        unresolved_norm=np.array(unresolved_norm),projection_quadrature_difference=np.array(projection_changes),
        number_source=np.einsum('i,ntik->ntk',basis.chemical,source),energy_source=np.einsum('i,ntik->ntk',basis.temperature,source),
        profiles=prediction['profiles'],gas=prediction['gas'],match_upper=upper)
    checks=[check(name,value,1e-10) for name,value in errors.items()]
    checks.append(dict(name='Zero initial source',passed=not np.count_nonzero(source[0])))
    return result,checks,errors


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--upper',type=float,choices=[.04,.02],required=True)
    parser.add_argument('--inner-steps',type=int,choices=[40960],default=40960)
    args=parser.parse_args()
    modest()
    started=time.monotonic()
    folder=ROOT/'results'/f'feedback-m{int(args.upper*1000)}-n{args.inner_steps}'
    folder.mkdir(parents=True,exist_ok=False)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    event_order=8 if args.upper==.04 else 6
    event_path=BRANCH/'direct-doppler-compton-feedback-20261012/results'/f'bank-o{event_order}-q32-m{int(args.upper*1000)}'/'bank.npz'
    events=read_npz(event_path)
    inputs=[*ladder.inputs,event_path]
    checks,models=[],{}
    cache=None
    for model in ['cold']:
        inner_path=ROOT/'results'/f'inner-{model}-n{args.inner_steps}/prediction.npz'
        inner_status=local_packet(inner_path.parent)
        assert inner_status['all_checks_passed']
        prediction=read_npz(inner_path)
        inputs.extend([inner_path,inner_path.parent/'status.json'])
        if cache is None:
            cache_path=INNER_PARENT/'results'/f'feedback-m{int(args.upper*1000)}-n20480/source-cache.npz'
            local_packet(cache_path.parent)
            cache=read_npz(cache_path)
            inputs.extend([cache_path,cache_path.parent/'status.json'])
            assert float(cache['upper'])==args.upper
            checks.append(dict(name='Sealed fixed-grid DC source operator reused',passed=True))
            np.savez_compressed(folder/'source-cache.npz',**cache)
        assert np.array_equal(cache['inner_frequency'],prediction['frequency'])
        background=thermal_wave.thermal.ThermalBackground(model)
        emission=NonlocalEmission(basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
        free_free=FreeFree(background,cache['frequency'])
        inputs.extend([*emission.inputs,*free_free.inputs,background.parent.source,background.native_constants])
        source,source_checks,source_errors=sources(basis,ladder,prediction,cache,events,background,emission,free_free,args.upper)
        for row in source_checks:
            row['name']='Source:'+model+':'+row['name']
        checks.extend(source_checks)
        np.savez_compressed(folder/(model+'-source.npz'),**source)
        solution,response_errors=solve_response(model,source,2048,ladder,emission,background)
        metrics,view=readout(basis,prediction,source,solution,args.upper)
        checks.extend(check('Response:'+model+':'+name,value,1. if name=='energy_spectrum' else 1e-7) for name,value in response_errors.items())
        checks.append(check('Unresolved moments:'+model,metrics['unresolved_energy_number_defect'],1e-10))
        assert all(np.isfinite(value).all() for value in [*source.values(),*solution.values(),*view.values()])
        np.savez_compressed(folder/(model+'-response.npz'),**solution,**view,integration_steps=2048,
            saved_step_indices=np.arange(2049),all_steps_saved=True)
        models[model]=dict(source_errors=source_errors,response_errors=response_errors,metrics=metrics)
        print(json.dumps(dict(model=model,upper=args.upper,metrics=metrics,response_errors=response_errors,seconds=time.monotonic()-started)),flush=True)
    chain=ancestors()
    for path in inputs:
        if not Path(path).is_relative_to(ROOT):
            verify_source(path,chain)
    finish(folder,dict(checks=checks,models=models,upper=args.upper,inner_steps=args.inner_steps,response_steps=2048,
        frequency_nodes=5265,all_response_steps_saved=True,source_quadrature=32,event_order=event_order,
        parent_histories_reused=True,parent_history_rerun=False,physical_boundary_retained=True,
        raw_gas_gate_relaxed=False,seconds=time.monotonic()-started),__file__,inputs)


if __name__=='__main__':
    main()
