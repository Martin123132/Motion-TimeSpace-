from coefficient_common import *
from interpolation_common import load_inputs as load_operator_inputs
from evaluate_source_probes import sources,response_metrics,source_diagnostics
from propagate_matched_feedback import solve_response
from propagate_repaired_feedback import readout
import argparse
import time


def retabulate(original,coordinate):
    result={}
    for key,value in original.items():
        if value.ndim>0 and value.shape[0]==len(original['coordinate']):
            result[key]=interpolate.interp1d(original['coordinate'],value,axis=0,bounds_error=True)(coordinate)
            result[key][np.searchsorted(coordinate,original['coordinate'])]=value
        else:
            result[key]=value.copy()
    result['coordinate']=coordinate
    return result


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=['heavy','cold'],required=True)
    parser.add_argument('--upper',type=float,choices=[.04,.02],required=True)
    args=parser.parse_args()
    modest()
    started=time.monotonic()
    folder=ROOT/'results'/f'feedback-{args.model}-m{int(args.upper*1000)}'
    folder.mkdir(parents=True,exist_ok=False)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    background=thermal_wave.thermal.ThermalBackground(args.model)
    emission=NonlocalEmission(basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
    operator_data=load_operator_inputs(args.model,args.upper,basis)
    operators=operator_data['operators']
    moments=operator_data['moments']
    fraction=(operator_data['coordinate']-operator_data['coordinate'][0])/(operator_data['coordinate'][-1]-operator_data['coordinate'][0])
    factored=moments[:,None,None]*((1-fraction[:,None,None])*operators[0]/moments[0]+fraction[:,None,None]*operators[-1]/moments[-1])
    owner=refined_owner(args.model)
    inner_path=owner/'results'/f'inner-{args.model}-n40960/prediction.npz'
    inner=read_npz(inner_path)
    cache_path=owner/'results'/f'feedback-m{int(args.upper*1000)}-n40960/source-cache.npz'
    cache=read_npz(cache_path)
    free_free=FreeFree(background,cache['frequency'])
    original=operator_data['sources']['direct-sites32-source']
    original_response=operator_data['sources']['direct-sites32-response']
    start,end=original['coordinate'][[0,-1]]
    restore=float(start+(end-start)*33/2048)
    coordinate=np.unique(np.r_[original['coordinate'],restore])
    assert len(coordinate)==139
    template=retabulate(original,coordinate)
    np.savez_compressed(folder/'retabulated-source.npz',**template)
    reference_solution,reference_errors=solve_response(args.model,template,2048,ladder,emission,background)
    reference_metrics,reference_view=readout(basis,inner,template,reference_solution,args.upper)
    reference={**reference_solution,**reference_view}
    np.savez_compressed(folder/'retabulated-response.npz',
        **{key:value for key,value in reference.items() if key!='photon'},photon_final=reference_solution['photon'][-1],integration_steps=2048)
    checks=[]
    inputs=[*operator_data['inputs'],inner_path,inner_path.parent/'status.json',cache_path,*ladder.inputs,*emission.inputs,*free_free.inputs,
        background.parent.source,background.native_constants,ROOT/'LOCAL-REPLAY-SPLICE.md']
    control_metric=response_metrics(reference,original_response,basis)
    checks.append(check('Retabulation gas control',max(control_metric['gas_peak_relative']),1e-7))
    checks.append(check('Retabulation radiation control',max(control_metric['radiation_relative']),1e-7))
    checks.extend(check('Response:retabulated:'+name,value,1. if name=='energy_spectrum' else 1e-7) for name,value in reference_errors.items())
    response_points=np.array([float(start+(end-start)*index/2048) for index in range(2049)])
    old_forcing=interpolate.interp1d(original['coordinate'],original['source'],axis=0)(response_points)
    results,source_sets,response_sets={},{'saved':template},{'saved':reference}
    for variant in ['control','dense','balanced']:
        replay_path=ROOT/'results'/f'replay-{args.model}-{variant}/prediction.npz'
        assert local_packet(replay_path.parent)['all_checks_passed']
        replay=read_npz(replay_path)
        inputs.extend([replay_path,replay_path.parent/'status.json'])
        prediction=dict(inner)
        for key in ['coordinate','defect','profiles','gas']:
            prediction[key]=replay[key]
        indices=np.searchsorted(coordinate,prediction['coordinate'])
        assert np.array_equal(coordinate[indices],prediction['coordinate'])
        for branch,adjoint in [('direct',operators),('factored',factored)]:
            label=variant+'-'+branch
            events=dict(frequency=operator_data['frequency'],adjoint=adjoint)
            fresh,group,source_errors=sources(basis,ladder,prediction,cache,events,background,emission,free_free,args.upper)
            checks.extend(dict(row,name='Source:'+label+':'+row['name']) for row in group)
            candidate={key:value.copy() for key,value in template.items()}
            for key,value in fresh.items():
                if isinstance(value,np.ndarray) and value.ndim>0 and value.shape[0]==33 and key!='coordinate':
                    candidate[key][indices]=value
            untouched=np.ones(len(coordinate),dtype=bool)
            untouched[indices]=False
            for key in ['source','raw_source','energy_source','number_source','overlap_source']:
                assert np.array_equal(candidate[key][untouched],template[key][untouched])
            forcing=interpolate.interp1d(candidate['coordinate'],candidate['source'],axis=0)(response_points)
            forcing_error=max_relative(forcing[33:]-old_forcing[33:],[old_forcing[33:]])
            checks.append(check('Unchanged later response forcing:'+label,forcing_error,1e-12))
            np.savez_compressed(folder/(label+'-source.npz'),**candidate)
            solution,errors=solve_response(args.model,candidate,2048,ladder,emission,background)
            metrics,view=readout(basis,inner,candidate,solution,args.upper)
            response={**solution,**view}
            np.savez_compressed(folder/(label+'-response.npz'),
                **{key:value for key,value in response.items() if key!='photon'},photon_final=solution['photon'][-1],integration_steps=2048)
            checks.extend(check('Response:'+label+':'+name,value,1. if name=='energy_spectrum' else 1e-7) for name,value in errors.items())
            checks.append(check('Unresolved moments:'+label,metrics['unresolved_energy_number_defect'],1e-10))
            if branch=='factored':
                reference_label=variant+'-direct'
                assert np.array_equal(candidate['source'][:,1:],source_sets[reference_label]['source'][:,1:])
            else:
                reference_label={'control':'saved','dense':'control-direct','balanced':'dense-direct'}[variant]
            comparison=response_metrics(response,response_sets[reference_label],basis)
            if label=='control-direct':
                checks.append(check('Source/control gas reproduction',max(comparison['gas_peak_relative']),1e-7))
                checks.append(check('Source/control radiation reproduction',max(comparison['radiation_relative']),1e-7))
            else:
                for metric in ['gas_peak_relative','gas_late_relative','gas_endpoint_relative','radiation_relative']:
                    checks.extend(check('Sensitivity1percent:'+label+':'+metric+':'+column,value,.01)
                        for column,value in zip(['baseline','join1','join2'],comparison[metric]))
            diagnostics=source_diagnostics(label,candidate['source'][indices],source_sets[reference_label]['source'][indices],basis)
            results[label]=dict(reference=reference_label,comparison=comparison,versus_saved=response_metrics(response,reference,basis),
                response_errors=errors,source_errors=source_errors,source_diagnostic=diagnostics,later_forcing_error=forcing_error)
            source_sets[label],response_sets[label]=candidate,response
    chain=ancestors()
    for path in inputs:
        if not Path(path).is_relative_to(ROOT):
            verify_source(path,chain)
    finish(folder,dict(checks=checks,model=args.model,upper=args.upper,variants=results,retabulation_control=control_metric,
        response_steps=2048,evolution_frequency_nodes=5265,inner_history_steps=40960,source_knots=139,
        changed_source_sites=33,restore_coordinate=restore,local_splice_only=True,later_state_carried=False,
        endpoint_state_reset_not_physical=True,seconds=time.monotonic()-started),__file__,inputs)
    print(json.dumps(dict(model=args.model,upper=args.upper,checks=len(checks),
        failures=[row['name'] for row in checks if not row['passed']],
        comparisons={key:value['comparison'] for key,value in results.items()},seconds=time.monotonic()-started)),flush=True)


if __name__=='__main__':
    main()
