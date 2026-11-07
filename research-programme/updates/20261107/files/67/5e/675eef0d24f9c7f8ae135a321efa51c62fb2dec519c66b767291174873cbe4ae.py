from spatial_defect_common import *
from propagate_matched_feedback import solve_response
from propagate_repaired_feedback import readout
from evaluate_source_probes import response_metrics
import argparse
import time


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=['heavy','cold'],required=True)
    parser.add_argument('--upper',type=float,choices=[.02,.04],required=True)
    args=parser.parse_args()
    modest()
    started=time.monotonic()
    folder=ROOT/'results'/f'feedback-{args.model}-m{int(args.upper*1000)}'
    folder.mkdir(parents=True,exist_ok=False)
    operator_path=ROOT/'results'/f'operator-m{int(args.upper*1000)}/bank.npz'
    operators=read_npz(operator_path)
    replay_path=PARENT/'results'/f'replay-{args.model}-balanced/prediction.npz'
    replay=read_npz(replay_path)
    parent_folder=PARENT/'results'/f'feedback-{args.model}-m{int(args.upper*1000)}'
    template_path=parent_folder/'discrete-source.npz'
    template=read_npz(template_path)
    original_response=read_npz(parent_folder/'physical-response.npz')
    error_path=PARENT/'results'/f'shape-error-{args.model}-m{int(args.upper*1000)}/difference-response.npz'
    original_error=read_npz(error_path)
    inner_path=refined_owner(args.model)/'results'/f'inner-{args.model}-n40960/prediction.npz'
    inner=read_npz(inner_path)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    background=thermal_wave.thermal.ThermalBackground(args.model)
    emission=NonlocalEmission(basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
    field=np.array([compact_defect(operators['frequency'],replay['frequency'],value,args.upper) for value in replay['defect']])
    indices=np.searchsorted(template['coordinate'],replay['coordinate'])
    assert np.array_equal(template['coordinate'][indices],replay['coordinate'])
    assert np.array_equal(operators['coordinate'],replay['coordinate'])
    untouched=np.ones(139,dtype=bool)
    untouched[indices]=False
    checks,rows=[],{}
    response_sets={}
    for label,key in [('matched','physical'),('second','corrected2'),('third','corrected3')]:
        operator=operators[key]
        delta=np.einsum('nij,njk->nik',operator-operators['grid'],field)
        source={name:value.copy() for name,value in template.items()}
        source['source'][indices,0]+=delta
        source['raw_source'][indices,0]+=delta
        source['energy_source']=np.einsum('i,ntik->ntk',basis.temperature,source['source'])
        source['number_source']=np.einsum('i,ntik->ntk',basis.chemical,source['source'])
        for name in ['source','raw_source']:
            assert np.array_equal(source[name][untouched],template[name][untouched])
            assert np.array_equal(source[name][:,1:],template[name][:,1:])
        np.savez_compressed(folder/(label+'-source.npz'),**source)
        solution,errors=solve_response(args.model,source,2048,ladder,emission,background)
        metrics,view=readout(basis,inner,source,solution,args.upper)
        response={**solution,**view}
        np.savez_compressed(folder/(label+'-response.npz'),**{name:value for name,value in response.items() if name!='photon'},
            photon_final=solution['photon'][-1],integration_steps=2048)
        checks.extend(check('Response:'+label+':'+name,value,1. if name=='energy_spectrum' else 1e-7) for name,value in errors.items())
        checks.append(check('Unresolved moments:'+label,metrics['unresolved_energy_number_defect'],1e-10))
        comparison=response_metrics(response,original_response if label=='matched' else response_sets['matched'],basis)
        row=dict(comparison=comparison,response_errors=errors)
        if label=='matched' and args.upper==.02:
            checks.append(check('Control:matched-order gas',max(comparison['gas_peak_relative']),1e-7))
            checks.append(check('Control:matched-order radiation',max(comparison['radiation_relative']),1e-7))
        if label!='matched':
            residual_source=np.zeros_like(source['source'])
            residual_source[indices,0]=np.einsum('nij,njk->nik',operator-operators['physical'],field)
            packet=dict(coordinate=source['coordinate'],source=residual_source)
            residual,residual_errors=solve_response(args.model,packet,2048,ladder,emission,background)
            np.savez_compressed(folder/(label+'-residual-source.npz'),**packet)
            np.savez_compressed(folder/(label+'-residual-response.npz'),**{name:value for name,value in residual.items() if name!='photon'},
                photon_final=residual['photon'][-1],integration_steps=2048)
            checks.extend(check('Response:'+label+'-residual:'+name,value,1. if name=='energy_spectrum' else 1e-7) for name,value in residual_errors.items())
            physical_gas=response_sets['matched']['gas'][:,:3]
            residual_gas=residual['gas'][:,:3]
            source_error=original_error['gas'][:,:3]
            peak=np.max(abs(residual_gas),axis=0)
            old_peak=np.maximum(np.max(abs(source_error),axis=0),1e-300)
            relative_peak=peak/np.maximum(np.max(abs(physical_gas),axis=0),1e-300)
            relative_late=np.max(abs(residual_gas[1536:]),axis=0)/np.maximum(np.max(abs(physical_gas[1536:]),axis=0),1e-300)
            relative_endpoint=abs(residual_gas[-1])/np.maximum(abs(physical_gas[-1]),1e-300)
            remaining=peak/old_peak
            subtraction=response['gas'][:,:3]-physical_gas
            discrepancy=np.max(abs(subtraction-residual_gas),axis=0)
            superposition_new=discrepancy/np.maximum(peak,1e-300)
            superposition_old=discrepancy/old_peak
            for metric,values in [('peak',relative_peak),('late',relative_late),('endpoint',relative_endpoint)]:
                checks.extend(check('Sensitivity1percent:'+label+':'+metric+':'+column,value,.01)
                    for column,value in zip(['baseline','join1','join2'],values))
            checks.extend(check('Explained90percent:response:'+label+':'+column,value,.1)
                for column,value in zip(['baseline','join1','join2'],remaining))
            for metric,values in [('new-error',superposition_new),('old-error',superposition_old)]:
                checks.extend(check('Superposition:'+label+':'+metric+':'+column,value,1e-4)
                    for column,value in zip(['baseline','join1','join2'],values))
            row.update(residual_errors=residual_errors,direct_relative_peak=relative_peak.tolist(),
                direct_relative_late=relative_late.tolist(),direct_relative_endpoint=relative_endpoint.tolist(),
                remaining_grid_error_peak=remaining.tolist(),superposition_new_error=superposition_new.tolist(),
                superposition_old_error=superposition_old.tolist(),residual_gas_endpoint=residual_gas[-1].tolist())
        rows[label]=row
        response_sets[label]=response
    inputs=[operator_path,operator_path.parent/'status.json',replay_path,replay_path.parent/'status.json',template_path,
        parent_folder/'physical-response.npz',parent_folder/'status.json',error_path,inner_path,*ladder.inputs,*emission.inputs,
        background.parent.source,background.native_constants,ROOT/'RESPONSE-METRICS.md']
    chain=ancestors()
    for path in inputs:
        if not Path(path).is_relative_to(ROOT):
            verify_source(path,chain)
    finish(folder,dict(checks=checks,model=args.model,upper=args.upper,variants=rows,
        response_steps=2048,frequency_nodes=5265,inner_states_reused=True,local_splice_only=True,
        later_state_carried=False,seconds=time.monotonic()-started),__file__,inputs)
    print(json.dumps(dict(model=args.model,upper=args.upper,
        endpoint={key:row.get('direct_relative_endpoint') for key,row in rows.items()},
        failures=[row['name'] for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
