from stage168_common import *


def main():
    modest()
    folder=ROOT/'results/comparison'
    folder.mkdir(parents=True,exist_ok=False)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    reader=ShapeReadout(ladder.basis,canonical=True)
    preflight=verify_packet(ROOT/'results/preflight-audited')
    assert preflight['numerical_production_allowed']
    parent=verify_packet(PARENT/'results/budget-ready')
    assert parent['all_checks_passed']
    checks,inputs,records=[],[*ladder.inputs,ROOT/'results/preflight-audited/status.json',PARENT/'results/budget-ready/status.json'],{}
    convergence={}
    for model in ['heavy','cold']:
        for route in ['local','cubic']:
            states,proofs={},{}
            for count in COUNTS:
                path=ROOT/'results/response'/f'{model}-{route}-{count}'
                proofs[count]=verify_packet(path)
                assert proofs[count]['all_checks_passed']
                states[count]=read_npz(path/'response.npz')
                inputs.extend([path/'status.json',path/'response.npz'])
            fine,coarse=states[4096],states[2048]
            for label,selection in [('current_defect',slice(2,4)),('raw_difference',slice(8,10)),('raw_defect',slice(10,12)),
                ('endpoint65',slice(12,14)),('incoming13',slice(14,16)),('incoming38',slice(16,18)),('incoming820',slice(18,20))]:
                for quantity in ['photon','gas']:
                    measure=lambda value:state_norm(value,ladder.basis.mass) if quantity=='photon' else abs(value)
                    current=fine[quantity][...,selection]
                    previous=coarse[quantity][...,selection]
                    ratio=measure(current[::2]-previous).max(axis=0)/np.maximum(measure(current).max(axis=0),1e-300)
                    name=f'{model}-{route}-{label}-{quantity}'
                    test(checks,'CONVERGENCE:'+name,float(max(ratio)),.01)
                    convergence[name]=ratio.tolist()
            heat=proofs[4096]['heat']
            assert heat==proofs[2048]['heat']
            for count in COUNTS:
                response=states[count]
                defect=reader.apply(response['photon'][-1,:,2:4],response['energy'][-1,2:4])
                audit=reader.apply(response['photon'][-1,:,8:10],response['energy'][-1,8:10])
                old=reader.apply(response['photon'][-1,:,:2],response['energy'][-1,:2])
                endpoint=reader.apply(response['photon'][-1,:,4:6],response['energy'][-1,4:6])
                close(checks,'Final defect update telescope:'+model+':'+route+':'+str(count),old['residual']+endpoint['residual'],defect['residual'],1e-8)
                current_metrics=metrics(defect,heat,reader.measure)
                audit_metrics=metrics(audit,heat,reader.measure)
                for match in [20,40]:
                    label=f'{model}-{route}-{count}-m{match}'
                    source_path=BRANCH/'endpoint-twofold-response-20261019/results/comparison'/(label+'.npz')
                    saved=read_npz(source_path)
                    budget_path=PARENT/'results/budget-ready'/f'{model}-{route}-m{match}.npz'
                    budget=read_npz(budget_path)
                    inputs.extend([source_path,budget_path])
                    assert np.array_equal(saved['frequency'],reader.frequency) and np.array_equal(saved['measure'],reader.measure)
                    baseline=saved['potential'][:,:1]
                    current=saved['potential'][:,3:5]
                    current_energy=saved['energy'][3:5]
                    frozen=current-defect['potential']
                    frozen_energy=current_energy-defect['energy']
                    potential=np.column_stack([baseline,frozen,current,baseline+frozen,saved['potential'][:,7:9],
                        defect['potential'],audit['potential'],old['potential'],endpoint['potential']])
                    energy=np.r_[saved['energy'][:1],frozen_energy,current_energy,saved['energy'][:1]+frozen_energy,saved['energy'][7:9],
                        defect['energy'],audit['energy'],old['energy'],endpoint['energy']]
                    split=reader.split_values(potential,energy)
                    assert np.any(baseline)
                    assert np.array_equal(split['potential'][:,:1],saved['potential'][:,:1])
                    assert np.array_equal(split['potential'][:,3:5],saved['potential'][:,3:5])
                    assert np.array_equal(split['potential'][:,7:9],saved['potential'][:,7:9])
                    close(checks,'Common baseline readout:'+label,split['amplitudes'][:,:1],saved['amplitudes'][:,:1],1e-10)
                    precise=precise_readout(dict(potential=potential,energy=energy),reader)
                    test(checks,'60digit same-baseline defect:'+label,precise['same_baseline_cancellation'],1e-8)
                    close(checks,'60digit direct defect amplitudes:'+label,precise['amplitudes'][:,3:5],defect['amplitudes'],1e-8)
                    close(checks,'60digit direct defect residual:'+label,precise['residual'][:,3:5],defect['residual'],1e-10)
                    alternate=np.linalg.lstsq(np.sqrt(reader.measure)[:,None]*reader.templates,
                        np.sqrt(reader.measure)[:,None]*defect['distortion'],rcond=None)[0]
                    close(checks,'Independent SVD direct amplitudes:'+label,alternate,defect['amplitudes'],1e-10)
                    reference=metrics(reader.split_values(current,current_energy),heat,reader.measure)
                    component_splits=[reader.apply(response['photon'][-1,:,start:start+2],response['energy'][-1,start:start+2]) for start in [12,14,16,18]]
                    time=reader.apply(fine['photon'][-1,:,2:4]-coarse['photon'][-1,:,2:4],fine['energy'][-1,2:4]-coarse['energy'][-1,2:4])
                    components=np.stack([metrics(value,heat,reader.measure) for value in [*component_splits,time]])
                    own_allowance=np.sum(abs(components),axis=0)
                    own_envelope=sum(abs(heat*value['residual']) for value in [*component_splits,time])
                    if count==4096:
                        assert np.array_equal(current,budget['central_potential'][:,5:7])
                        assert np.array_equal(baseline,budget['central_potential'][:,:1])
                    regions=budget['region_edges']
                    masks=[(reader.frequency>=lower)&(reader.frequency<upper) for lower,upper in zip(regions[:-1],regions[1:])]
                    powers=np.stack([np.sum(reader.measure[mask,None]*(heat*defect['residual'][mask])**2,axis=0) for mask in masks])
                    close(checks,'Heldout frequency partition:'+label,powers.sum(axis=0),current_metrics[3]**2,1e-10)
                    test(checks,'Defect envelope triangle:'+label,float(max(norm(own_envelope,reader.measure)/np.maximum(own_allowance[3],1e-300))),1+1e-10)
                    record=dict(defect_metrics=current_metrics.tolist(),audit_metrics=audit_metrics.tolist(),
                        defect_over_current_mts=(abs(current_metrics)/np.maximum(abs(reference),1e-300)).tolist(),
                        defect_over_stage167_allowance=(abs(current_metrics)/np.maximum(budget['allowance'],1e-300)).tolist(),
                        audit_over_stage167_allowance=(abs(audit_metrics)/np.maximum(budget['allowance'],1e-300)).tolist(),
                        audit_over_defect=(abs(audit_metrics)/np.maximum(abs(current_metrics),1e-300)).tolist(),
                        own_allowance=own_allowance.tolist(),own_component_metrics=components.tolist(),
                        defect_over_own_allowance=(abs(current_metrics)/np.maximum(own_allowance,1e-300)).tolist(),
                        residual_power_by_region=powers.tolist(),source_qualified=False,
                        fixed_profile_sensitivity=True,baseline_reused=True,not_adopted=True,
                        paired_precision_cancellation=precise['same_baseline_cancellation'])
                    records[label]=record
                    np.savez_compressed(folder/(label+'.npz'),**split,frequency=reader.frequency,measure=reader.measure,heat=heat,
                        reference_metrics=reference,defect_metrics=current_metrics,audit_metrics=audit_metrics,
                        stage167_allowance=budget['allowance'],own_allowance=own_allowance,own_components=components,
                        own_envelope=own_envelope,regions=regions,residual_power=powers)
    summary=dict(stage=168,source_records=preflight['source_records'],raw_source_metrics=preflight['raw_source_metrics'],
        raw_source_failures=preflight['raw_source_failures'],retained_smoke_failures=preflight['retained_smoke_failures'],
        records=records,convergence=convergence,metrics_order=METRICS,
        numerical_integrity_passed=all(row['passed'] for row in checks if not row['name'].startswith('CONVERGENCE:')),
        convergence_passed=all(row['passed'] for row in checks if row['name'].startswith('CONVERGENCE:')),
        independent_raw_physical_source_qualified=False,curve_adopted=False,
        band_orders=[6,6,6,8,7,7,6],frequency_modes=96,response_counts=COUNTS,
        source_profile='The pre-existing cold_bubble(phase,route);not the uniquely inferred true defect history.',
        temperature_curve_changed=False,tolerances_changed=False,baseline_inner_rerun=False,
        new_event_evaluations=0,new_expensive_virtual_integrations=0,new_response_evolutions=8,
        raw_difference_gate='Full original-equation backward error1e-7;legacy diagnostic retained and may fail for near-pure-gas source.',
        next_target='Derive or test the temperature dependence of the held-out correction using saved neighboring source information;retain the measured moment-sensitivity audit and do not fit a new curve to the held-out datum.')
    write_json(ROOT/'NUMERICAL-SUMMARY.json',summary)
    finish(folder,dict(checks=checks,numerical_integrity_passed=summary['numerical_integrity_passed'],
        convergence_passed=summary['convergence_passed'],source_qualified=False,records=records),
        [*inputs,ROOT/'NUMERICAL-SUMMARY.json'])
    failed=[row for row in checks if not row['passed']]
    print(json.dumps(dict(checks=len(checks),failed=failed)),flush=True)
    assert not failed


if __name__=='__main__':
    main()
