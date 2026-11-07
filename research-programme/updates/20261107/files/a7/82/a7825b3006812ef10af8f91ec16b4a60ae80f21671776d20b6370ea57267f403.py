from repair_common import *
import argparse


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--variant',choices=['fine','space'],default='fine')
    parser.add_argument('--points',type=int,choices=[4,6],default=4)
    parser.add_argument('--inner-steps',type=int,choices=[5120,10240],default=5120)
    parser.add_argument('--event-order',type=int,choices=[6,8],default=8)
    parser.add_argument('--upper',type=float,choices=[.02,.04],default=.04)
    parser.add_argument('--quadrature',type=int,choices=[32,48],default=32)
    args=parser.parse_args()
    modest()
    assert args.upper==.04 or args.event_order==6
    label=f'{args.variant}-p{args.points}-n{args.inner_steps}-o{args.event_order}-q{args.quadrature}-m{int(args.upper*1000)}'
    folder=ROOT/'results'/('sources-'+label)
    folder.mkdir(parents=True,exist_ok=False)
    cache_folder=ROOT/'results'/f'dc-cache-q{args.quadrature}-m{int(args.upper*1000)}'
    cache_status=local_packet(cache_folder)
    assert cache_status['all_checks_passed']
    cache_path=cache_folder/(args.variant+'.npz')
    cache=read_npz(cache_path)
    event_path=BRANCH/'direct-doppler-compton-feedback-20261012/results'/f'bank-o{args.event_order}-q32-m{int(args.upper*1000)}'/'bank.npz'
    events=read_npz(event_path)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    inputs=[cache_path,cache_folder/'status.json',event_path,*ladder.inputs]
    chain=ancestors()
    checks,summaries=[],{}
    for model in ['heavy','cold']:
        inner_folder=ROOT/'results'/f'inner-{model}-{args.variant}-p{args.points}-n{args.inner_steps}'
        status=local_packet(inner_folder)
        assert status['all_checks_passed']
        path=inner_folder/'prediction.npz'
        prediction=read_npz(path)
        assert np.array_equal(prediction['frequency'],cache['inner_frequency'])
        assert np.allclose(prediction['coordinate'],events['coordinate'],rtol=0,atol=1e-14)
        background=thermal_wave.thermal.ThermalBackground(model)
        emission=NonlocalEmission(basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
        free_free=FreeFree(background,cache['frequency'])
        inputs.extend([path,inner_folder/'status.json',*emission.inputs,*free_free.inputs,background.parent.source,background.native_constants])
        raw,represented,projections,moments,raw_norm,unresolved_norm,projection_changes=[],[],[],[],[],[],[]
        bank_at=interpolate.interp1d(prediction['coefficient_knots'],prediction['coefficient_bank'],axis=0,bounds_error=True)
        errors={key:0. for key in ['mass_projection','dc_energy','compton_number','dc_represented_energy','compton_represented_number','source_decomposition']}
        for epoch,coordinate in enumerate(prediction['coordinate']):
            local=background.at(float(coordinate))
            theta=local['thermal_parameter']
            values=prediction['defect'][epoch]
            canonical=compact_defect(basis.nodes,prediction['frequency'],values,args.upper)
            quadrature=compact_defect(cache['frequency'],prediction['frequency'],values,args.upper)
            event_values=compact_defect(events['frequency'],prediction['frequency'],values,args.upper)
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
            unresolved=canonical-basis.values@projected
            raw.append(source)
            represented.append(old)
            projections.append(projected)
            moments.append(moment)
            raw_norm.append(norm(canonical,basis.measure))
            unresolved_norm.append(norm(unresolved,basis.measure))
        raw,represented=np.array(raw),np.array(represented)
        source=raw-represented
        checks.extend(check(name+':'+model,value,1e-10) for name,value in errors.items())
        checks.append(dict(name='Zero initial defect gives zero initial source:'+model,passed=not np.count_nonzero(source[0])))
        checks.append(dict(name='Finite rebuilt sources:'+model,passed=bool(np.isfinite(source).all())))
        np.savez_compressed(folder/(model+'.npz'),coordinate=prediction['coordinate'],source=source,
            raw_source=raw,overlap_source=represented,projected_replacement=np.array(projections),
            replacement_moments=np.array(moments),replacement_norm=np.array(raw_norm),unresolved_norm=np.array(unresolved_norm),
            number_source=np.einsum('i,ntik->ntk',basis.chemical,source),energy_source=np.einsum('i,ntik->ntk',basis.temperature,source),
            projection_quadrature_difference=np.array(projection_changes),profiles=prediction['profiles'],gas=prediction['gas'],
            inner_packet=inner_folder.name,match_upper=args.upper,event_order=args.event_order,quadrature_order=args.quadrature)
        summaries[model]=dict(errors=errors,maximum_replacement_norm=np.max(raw_norm,axis=0).tolist(),
            final_replacement_norm=raw_norm[-1].tolist(),final_unresolved_norm=unresolved_norm[-1].tolist())
        print(json.dumps(dict(packet=folder.name,model=model,summary=summaries[model])),flush=True)
    for path in inputs:
        if not Path(path).is_relative_to(ROOT):
            verify_source(path,chain)
    finish(folder,dict(checks=checks,models=summaries,variant=args.variant,points=args.points,inner_steps=args.inner_steps,
        upper=args.upper,event_order=args.event_order,quadrature=args.quadrature,
        stored_small_defect_used=True,dc_br_recalculated=True,canonical_moments_recalculated=True,
        full_compact_compton_functional=True,joining_term_discarded=False,columns=['baseline','join1','join2']),__file__,inputs)


if __name__=='__main__':
    main()
