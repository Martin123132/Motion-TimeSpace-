from stage161_common import *


def main():
    modest()
    folder=ROOT/'results/comparison'
    folder.mkdir(parents=True,exist_ok=False)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    reader=ShapeReadout(ladder.basis,canonical=True)
    source_packet=verify_packet(ROOT/'results/sources')
    checks,inputs,records=[],[*ladder.inputs,ROOT/'results/sources/status.json'],{}
    maximum_precision=maximum_svd=0.
    for model in ['heavy','cold']:
        for route in ['local','cubic']:
            assert source_packet['allowed_routes'][route]
            states={}
            for count in COUNTS:
                location=ROOT/'results/response'/f'{model}-{route}-{count}'
                proof=verify_packet(location)
                assert proof['all_checks_passed']
                current=read_npz(location/'response.npz')
                base_path=SOURCE155/'results/response'/f'{model}-{route}-{count}/response.npz'
                parent_path=SOURCE158/'results/response'/f'{model}-{route}-{count}/response.npz'
                refined_path=SOURCE159/'results/response'/f'{model}-{route}-{count}/response.npz'
                base,previous,refined=read_npz(base_path),read_npz(parent_path),read_npz(refined_path)
                assert np.array_equal(current['coordinate'],refined['coordinate'])
                assert np.array_equal(current['coordinate'],base['coordinate'])
                assert np.array_equal(current['coordinate'],previous['coordinate'])
                old={key:base[key][...,10:12]+previous[key][...,2:4]+refined[key][...,2:4] for key in
                    ['photon','gas','energy','work','number','integrated_number_source']}
                heat=proof['heat']
                states[count]=current
                inputs.extend([location/'status.json',location/'response.npz',base_path,parent_path,refined_path])
                state_metrics={}
                for name in ['photon','gas']:
                    measure=lambda value:state_norm(value,ladder.basis.mass) if name=='photon' else abs(value)
                    reference=measure(old[name])
                    increment=measure(current[name][...,2:4])
                    budget=sum(measure(current[name][...,start:start+2]) for start in [12,14,16])
                    denominator=reference[-1] if name=='photon' else reference.max(axis=0)
                    state_metrics[name]=dict(endpoint_over_stage159=(increment[-1]/denominator).tolist(),
                        history_over_stage159_peak=(increment.max(axis=0)/reference.max(axis=0)).tolist(),
                        endpoint_coherence=(increment[-1]/np.maximum(budget[-1],1e-300)).tolist())
                    test(checks,'Three-site response triangle:'+model+':'+route+':'+str(count)+':'+name,
                        float(np.max(increment[-1]/np.maximum(budget[-1],1e-300))),1+1e-10)
                energy=old['energy']+current['energy'][...,2:4]
                gas=old['gas']+current['gas'][...,2:4]
                work=old['work']+current['work'][...,2:4]
                balance=energy+heat*gas+work
                scale=np.maximum(np.max(abs(energy)+abs(heat*gas)+abs(work),axis=0),1e-300)
                test(checks,'Updated MTS energy/work:'+model+':'+route+':'+str(count),float(np.max(abs(balance-balance[0])/scale)),1e-7)
                label=f'{model}-{route}-{count}'
                readouts={}
                for match in [20,40]:
                    prior_path=SOURCE159/'results/comparison'/f'{model}-{route}-{count}-m{match}.npz'
                    prior=read_npz(prior_path)
                    inputs.append(prior_path)
                    baseline=prior['potential'][:,:1]
                    before=prior['potential'][:,3:5]
                    before_energy=prior['energy'][3:5]
                    increment=reader.values@current['photon'][-1,:,2:4]
                    increment_energy=current['energy'][-1,2:4]
                    after=before+increment
                    after_energy=before_energy+increment_energy
                    pieces=[reader.values@current['photon'][-1,:,start:start+2] for start in [12,14,16]]
                    potential=np.column_stack([baseline,before,after,baseline+before,baseline+after,increment,*pieces])
                    energy=np.r_[prior['energy'][:1],before_energy,after_energy,
                        prior['energy'][:1]+before_energy,prior['energy'][:1]+after_energy,
                        increment_energy,*[current['energy'][-1,start:start+2] for start in [12,14,16]]]
                    split=reader.split_values(potential,energy)
                    key=label+f'-m{match}'
                    inherited.invariants(checks,reader,split,key)
                    assert np.array_equal(split['amplitudes'][:,:1],prior['amplitudes'][:,:1])
                    assert np.array_equal(potential[:,:1],prior['potential'][:,:1])
                    assert np.array_equal(potential[:,1:3],prior['potential'][:,3:5])
                    precise=precise_readout(dict(potential=potential,energy=energy),reader)
                    maximum_precision=max(maximum_precision,precise['same_baseline_cancellation'])
                    test(checks,'60digit paired baseline/MTS:'+key,precise['same_baseline_cancellation'],1e-8)
                    close(checks,'Independent60digit increment amplitudes:'+key,precise['amplitudes'][:,3:5],split['amplitudes'][:,9:11],1e-8)
                    close(checks,'Independent60digit increment residual:'+key,precise['residual'][:,3:5],split['residual'][:,9:11],1e-10)
                    alternate=np.linalg.lstsq(np.sqrt(reader.measure)[:,None]*reader.templates,
                        np.sqrt(reader.measure)[:,None]*split['distortion'],rcond=None)[0]
                    numerator=np.linalg.norm(np.sqrt(reader.measure)[:,None]*(reader.templates@(alternate-split['amplitudes'])),axis=0)
                    denominator=np.linalg.norm(np.sqrt(reader.measure)[:,None]*split['distortion'],axis=0)
                    maximum_svd=max(maximum_svd,float(np.max(numerator/np.maximum(denominator,1e-300))))
                    metrics={}
                    for position,name in enumerate(['mu','y']):
                        values=split['amplitudes'][position]
                        budget=sum(abs(values[start:start+2]) for start in [11,13,15])
                        metrics[name]=dict(signed_amplitude=(heat*values[9:11]).tolist(),
                            increment_over_stage159_MTS=(abs(values[9:11])/abs(prior['amplitudes'][position,3:5])).tolist(),
                            site_coherence=(abs(values[9:11])/np.maximum(budget,1e-300)).tolist())
                    readouts[str(match)]=metrics
                    np.savez_compressed(folder/(key+'.npz'),**split,frequency=reader.frequency,measure=reader.measure,heat=heat)
                records[label]=dict(state=state_metrics,readouts=readouts,baseline_preserved=True)
            step_metrics={}
            for name,selection in [('all_temperatures',slice(2,4)),('cold',slice(12,14)),('warm',slice(14,16)),('centre',slice(16,18))]:
                step_metrics[name]={}
                for quantity in ['photon','gas']:
                    measure=lambda value:state_norm(value,ladder.basis.mass) if quantity=='photon' else abs(value)
                    coarse=states[2048][quantity][...,selection]
                    fine=states[4096][quantity][...,selection]
                    ratio=measure(fine[::2]-coarse).max(axis=0)/np.maximum(measure(fine).max(axis=0),1e-300)
                    step_metrics[name][quantity]=ratio.tolist()
                    test(checks,'CONVERGENCE:'+model+':'+route+':'+name+':'+quantity,float(np.max(ratio)),.01)
            records[model+'-'+route+'-steps']=step_metrics
    test(checks,'Independent weightedSVD',maximum_svd,1e-10)
    numerical=all(row['passed'] for row in checks if not row['name'].startswith('CONVERGENCE:'))
    summary=dict(stage=161,source={key:source_packet[key] for key in
        ['panel_metrics','frequency_metrics','diagnostics','per_site_change_over_saved_source','readiness','uncertainty_update']},
        response=dict(records=records,maximum_precision_cancellation=maximum_precision,maximum_independent_svd=maximum_svd,
            convergence_passed=all(row['passed'] for row in checks if row['name'].startswith('CONVERGENCE:'))),
        numerical_integrity_passed=numerical,temperature_curve_changed=False,lower_bands_changed=False,
        frozen_predictions_preserved=True,baseline_preserved=True,baseline_inner_rerun=False,
        new_event_evaluations=648,reused_new_rule_values=108,reused_reference_events=648,new_response_evolutions=8,
        refined_panel=[8.,20.],selected_panel_order=7,band13_order=8,band38_order=7,other_panel_order=6,
        mixed_incoming_orders=[6,6,6,8,7,7,6],
        incoming_continuum_error_certified=False,
        next_target='Use the new8–20 contraction and updated latest-step budgets to choose the next unresolved accuracy requirement,including endpoints;keep the temperature curve fixed until the remaining numerical allowance is understood.')
    write_json(ROOT/'NUMERICAL-SUMMARY.json',summary)
    finish(folder,dict(checks=checks,records=records,numerical_integrity_passed=numerical,
        convergence_passed=summary['response']['convergence_passed'],
        maximum_precision_cancellation=maximum_precision,maximum_independent_svd=maximum_svd,
        temperature_curve_changed=False,baseline_preserved=True,baseline_inner_rerun=False,
        lower_bands_rerun=False,incoming_continuum_error_certified=False),__file__,
        [*inputs,*folder.glob('*.npz'),ROOT/'NUMERICAL-SUMMARY.json'])
    print(json.dumps(dict(checks=len(checks),numerical=numerical,failed=[row for row in checks if not row['passed']])),flush=True)
    assert numerical


if __name__=='__main__':
    main()
