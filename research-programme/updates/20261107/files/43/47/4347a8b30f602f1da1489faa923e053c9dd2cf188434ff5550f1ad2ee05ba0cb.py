from interpolation_common import *
from propagate_matched_feedback import solve_response
from propagate_repaired_feedback import readout
from evaluate_source_probes import response_metrics
import argparse
import time


def saved_response(path,solution,view=None):
    packet={key:value for key,value in solution.items() if key!='photon'}
    packet['photon_final']=solution['photon'][-1]
    if view:
        packet.update(view)
    np.savez_compressed(path,**packet,integration_steps=2048)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=['heavy','cold'],required=True)
    parser.add_argument('--upper',type=float,choices=[.04,.02],required=True)
    args=parser.parse_args()
    modest()
    started=time.monotonic()
    folder=ROOT/'results'/f'case-{args.model}-m{int(args.upper*1000)}'
    folder.mkdir(parents=True,exist_ok=False)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    data=load_inputs(args.model,args.upper,basis)
    coordinate,operators,field,moments=[data[key] for key in ['coordinate','operators','field','moments']]
    fraction=(coordinate-coordinate[0])/(coordinate[-1]-coordinate[0])
    def chord(values):
        weight=fraction.reshape((-1,)+(1,)*(values.ndim-1))
        return (1-weight)*values[0]+weight*values[-1]
    def apply(matrix,values):
        return np.einsum('nif,nfk->nik',matrix,values)
    operator_chord,field_chord=chord(operators),chord(field)
    raw=apply(operators,field)
    raw_chord=chord(raw)
    shape=operators/moments[:,None,None]
    shape_chord=chord(shape)
    moment_chord=chord(moments)
    corrected_operator=moments[:,None,None]*shape_chord
    components=dict(total=raw-raw_chord,
        operator=apply(operators-operator_chord,field),
        state=apply(operator_chord,field-field_chord),
        cross=-fraction[:,None,None]*(1-fraction[:,None,None])*((operators[-1]-operators[0])@(field[-1]-field[0]))[None,:,:],
        moment=apply((moments-moment_chord)[:,None,None]*shape_chord,field),
        shape=apply(moments[:,None,None]*(shape-shape_chord),field),
        moment_cross=apply((-fraction*(1-fraction)*(moments[-1]-moments[0]))[:,None,None]*(shape[-1]-shape[0])[None,:,:],field))
    corrected_raw=apply(corrected_operator,field)
    prior=data['sources']
    original=prior['direct-sites32-source']
    original_response=prior['direct-sites32-response']
    checks=[]
    checks.append(check('Product source identity',max_relative(components['total']-sum(components[key] for key in ['operator','state','cross']),[raw,raw_chord]),1e-10))
    checks.append(check('Operator moment identity',max_relative(components['operator']-sum(components[key] for key in ['moment','shape','moment_cross']),[raw,apply(operator_chord,field)]),1e-10))
    checks.append(check('Direct candidate identity',max_relative(raw-corrected_raw-components['shape'],[raw,corrected_raw]),1e-10))
    checks.append(check('Saved direct raw source',max_relative(raw-prior['direct-evaluated']['raw_source'][:,0],[raw]),1e-10))
    checks.append(check('Saved assembled raw source',max_relative(apply(operator_chord,field)-prior['assembled-evaluated']['raw_source'][:,0],[raw]),1e-10))
    expected=moments[:,None]*data['weights']*data['frequency']/(2*I3)
    energy=np.einsum('i,nif->nf',basis.temperature,corrected_operator)
    checks.append(check('Exact candidate energy moment',float(np.max(abs(energy-expected)/np.maximum(abs(expected),1e-300))),1e-10))
    checks.append(check('Candidate number invariant',float(np.max(abs(np.einsum('i,nif->nf',basis.chemical,corrected_operator)))),1e-14))
    checks.append(dict(name='Positive analytic moment',passed=bool(np.all(moments>0))))
    checks.append(check('Candidate endpoints retained',max_relative(corrected_operator[[0,-1]]-operators[[0,-1]],[operators[[0,-1]]]),1e-14))
    for name,values in components.items():
        checks.append(dict(name='Zero diagnostic endpoint:'+name,passed=not np.count_nonzero(values[[0,-1]])))
    source_indices=np.searchsorted(original['coordinate'],coordinate)
    assert np.array_equal(original['coordinate'][source_indices],coordinate)
    background=thermal_wave.thermal.ThermalBackground(args.model)
    emission=NonlocalEmission(basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
    inputs=[*data['inputs'],*ladder.inputs,*emission.inputs,background.parent.source,background.native_constants]
    inner_path=refined_owner(args.model)/'results'/f'inner-{args.model}-n40960/prediction.npz'
    inner=read_npz(inner_path)
    inputs.extend([inner_path,inner_path.parent/'status.json'])
    np.savez_compressed(folder/'decomposition.npz',coordinate=coordinate,fraction=fraction,operators=operators,
        field=field,moments=moments,temperature=data['temperature'],frequency=data['frequency'],weights=data['weights'],
        operator_chord=operator_chord,field_chord=field_chord,raw=raw,raw_chord=raw_chord,
        corrected_operator=corrected_operator,source_indices=source_indices,source_coordinate=original['coordinate'],**components)
    propagated,errors_by_case={},{}
    for name in PARTS:
        values=np.zeros_like(original['source'])
        values[source_indices,0]=components[name]
        source=dict(coordinate=original['coordinate'],source=values)
        solution,errors=solve_response(args.model,source,2048,ladder,emission,background)
        checks.extend(check('Response:'+name+':'+key,value,1. if key=='energy_spectrum' else 1e-7) for key,value in errors.items())
        checks.append(dict(name='Zero diagnostic DC/BR:'+name,passed=not np.count_nonzero(solution['gas'][:,6:])))
        saved_response(folder/(name+'-response.npz'),solution)
        propagated[name]=solution
        errors_by_case[name]=errors
    closure={}
    for target,pieces in [('total',['operator','state','cross']),('operator',['moment','shape','moment_cross'])]:
        for quantity in ['gas','energy','work']:
            operands=[propagated[target][quantity],*[propagated[key][quantity] for key in pieces]]
            value=max_relative(operands[0]-sum(operands[1:]),operands)
            checks.append(check('Response closure:'+target+':'+quantity,value,1e-7))
            closure[target+':'+quantity]=value
    candidates={}
    for name,replacement in [('control',None),('chord',apply(operator_chord,field)),('factored',corrected_raw)]:
        source={key:value.copy() for key,value in original.items()}
        if replacement is not None:
            selected=source_indices[1:-1]
            source['raw_source'][selected,0]=replacement[1:-1]
            source['source'][selected,0]=replacement[1:-1]-source['overlap_source'][selected,0]
            source['energy_source'][selected,0]=np.einsum('i,nik->nk',basis.temperature,source['source'][selected,0])
            source['number_source'][selected,0]=np.einsum('i,nik->nk',basis.chemical,source['source'][selected,0])
            untouched=np.ones(len(source['coordinate']),dtype=bool)
            untouched[selected]=False
            for key in ['source','raw_source','energy_source','number_source']:
                assert np.array_equal(source[key][untouched],original[key][untouched])
                assert np.array_equal(source[key][:,1:],original[key][:,1:])
        np.savez_compressed(folder/(name+'-source.npz'),**source)
        solution,errors=solve_response(args.model,source,2048,ladder,emission,background)
        metrics,view=readout(basis,inner,source,solution,args.upper)
        response={**solution,**view}
        saved_response(folder/(name+'-response.npz'),solution,view)
        checks.extend(check('Response:'+name+':'+key,value,1. if key=='energy_spectrum' else 1e-7) for key,value in errors.items())
        checks.append(check('Unresolved moment:'+name,metrics['unresolved_energy_number_defect'],1e-10))
        checks.append(dict(name='Unchanged candidate DC/BR:'+name,passed=np.array_equal(solution['gas'][:,6:],original_response['gas'][:,6:])))
        candidates[name]=response
        errors_by_case[name]=errors
    control_metrics=response_metrics(candidates['control'],original_response,basis)
    checks.append(check('Saved response reproduction',max(control_metrics['gas_peak_relative']),1e-7))
    checks.append(check('Saved radiation reproduction',max(control_metrics['radiation_relative']),1e-7))
    comparisons={name:response_metrics(response,candidates['control'],basis) for name,response in candidates.items() if name!='control'}
    for name,part in [('chord','operator'),('factored','shape')]:
        for quantity in ['gas','energy','work']:
            operands=[candidates['control'][quantity],candidates[name][quantity],propagated[part][quantity]]
            value=max_relative(operands[0]-operands[1]-operands[2],operands)
            checks.append(check('Candidate attribution:'+name+':'+quantity,value,1e-7))
            closure[name+':'+quantity]=value
        if name=='factored':
            for metric in ['radiation_relative','gas_peak_relative','gas_late_relative','gas_endpoint_relative']:
                checks.extend(check('Factored1percent:'+metric+':'+column,value,.01) for column,value in
                    zip(['baseline','join1','join2'],comparisons[name][metric]))
    endpoint={name:solution['gas'][-1,:3].tolist() for name,solution in propagated.items()}
    denominator=np.maximum(abs(propagated['operator']['gas'][-1,:3]),1e-300)
    fractions={name:(propagated[name]['gas'][-1,:3]/np.where(propagated['operator']['gas'][-1,:3]==0,np.inf,
        propagated['operator']['gas'][-1,:3])).tolist() for name in ['moment','shape','moment_cross']}
    residual=(abs(propagated['shape']['gas'][-1,:3])/denominator).tolist()
    peak=np.maximum(abs(propagated['operator']['gas'][:,:3]).max(axis=0),1e-300)
    report=dict(checks=checks,model=args.model,upper=args.upper,columns=['baseline','join1','join2'],
        endpoint=endpoint,operator_signed_fractions=fractions,factored_operator_endpoint_residual_ratio=residual,
        operator_endpoint_resolved=(denominator>1e-6*peak).tolist(),
        factored_operator_peak_residual_ratio=(abs(propagated['shape']['gas'][:,:3]).max(axis=0)/peak).tolist(),
        candidate_comparisons=comparisons,control_comparison=control_metrics,closure=closure,response_errors=errors_by_case,
        moment_curvature_relative=((moments-moment_chord)/moment_chord).tolist(),
        source_sites=33,changed_candidate_sites=31,new_inner_steps=0,new_temperature_integrals=0,
        fixed_frequency_nodes=5265,inner_steps=40960,response_steps=2048,
        source_only_interpolation_test=True,inner_source_consistency_established=False,seconds=time.monotonic()-started)
    chain=ancestors()
    for path in inputs:
        verify_source(path,chain)
    finish(folder,report,__file__,inputs)
    print(json.dumps(dict(model=args.model,upper=args.upper,checks=len(checks),
        failed=[row for row in checks if not row['passed']],fractions=fractions,residual_ratio=residual,
        factored=comparisons['factored'],seconds=time.monotonic()-started)),flush=True)


if __name__=='__main__':
    main()
