from stage167_common import *
from precision_pair import resolution_pair


def main():
    modest()
    folder=ROOT/'results/budget-checked'
    folder.mkdir(parents=True,exist_ok=False)
    assert digest(PARENT/'results/stage-integrity.json')==PARENT_SEAL
    parent_status=verify_packet(PARENT/'results/comparison')
    assert parent_status['all_checks_passed'] and parent_status['convergence_passed']
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    reader=ShapeReadout(ladder.basis,canonical=True)
    checks,inputs,records=[],list(ladder.inputs)+[PARENT/'results/comparison/status.json'],{}
    region_edges=np.array([reader.minimum,1.,3.,8.,20.,reader.maximum])
    assert np.all(np.diff(region_edges)>0)
    masks=np.array([(reader.frequency>=lower)&(reader.frequency<upper) for lower,upper in zip(region_edges[:-1],region_edges[1:])])
    assert np.all(masks.sum(axis=0)==1)
    channels=['endpoint54','endpoint65','endpoint64','arithmetic','twofold_low',*BAND_SOURCES,
        'time_response','baseline_time','combined_time','rounded_total_time']
    selected=['endpoint65',*BAND_SOURCES,'time_response']
    base_labels=['baseline','mts_order4_join0','mts_order4_join1','mts_order5_join0','mts_order5_join1',
        'mts_order6_join0','mts_order6_join1','total_order6_join0','total_order6_join1']
    cases={}
    for model in ['heavy','cold']:
        for route in ['local','cubic']:
            terminals={}
            for count in COUNTS:
                path=PARENT/'results/response'/f'{model}-{route}-{count}'
                proof=verify_packet(path)
                assert proof['all_checks_passed']
                terminals[count]=get_terminal(path/'terminal.npz')
                inputs.extend([path/'status.json',path/'terminal.npz'])
            for match in [20,40]:
                label=f'{model}-{route}-m{match}'
                saved={count:checked_readout(PARENT/'results/comparison'/f'{model}-{route}-{count}-m{match}.npz',reader,inputs,checks) for count in COUNTS}
                fine,coarse=saved[4096],saved[2048]
                heat=float(fine['heat'])
                assert heat==float(coarse['heat']) and heat>0
                final=terminals[4096]
                sources={name:(reader.values@final['photon'][:,start:start+2],final['energy'][start:start+2]) for name,start in
                    [('endpoint54',16),('endpoint65',18),('endpoint64',8),('arithmetic',2)]}
                sources['twofold_low']=(reader.values@final['photon_low'][:,8:10],final['energy_low'][8:10])
                site_arrays=[]
                for name,(child,suffix) in BAND_SOURCES.items():
                    old=checked_readout(BRANCH/child/'results/comparison'/f'{model}-{route}-4096-m{match}{suffix}.npz',reader,inputs,checks)
                    assert float(old['heat'])==heat
                    assert np.array_equal(old['potential'][:,:1],fine['potential'][:,:1])
                    sources[name]=(old['potential'][:,9:11],old['energy'][9:11])
                    site_arrays.append(np.stack([heat*old['residual'][:,start:start+2] for start in [11,13,15]]))
                    close(checks,'Interior sites sum:'+label+':'+name,sum(old['residual'][:,start:start+2] for start in [11,13,15]),old['residual'][:,9:11],1e-10)
                sources['time_response']=(fine['potential'][:,3:5]-coarse['potential'][:,3:5],fine['energy'][3:5]-coarse['energy'][3:5])
                sources['baseline_time']=(np.repeat(fine['potential'][:,:1]-coarse['potential'][:,:1],2,axis=1),np.repeat(fine['energy'][:1]-coarse['energy'][:1],2))
                sources['rounded_total_time']=(fine['potential'][:,7:9]-coarse['potential'][:,7:9],fine['energy'][7:9]-coarse['energy'][7:9])
                pair,identity,rounding=resolution_pair(fine,coarse)
                sources['combined_time']=(pair['potential'],pair['energy'])
                test(checks,'60digit total rounding identity:'+label,identity,1e-10)
                test(checks,'Recorded total addition rounding scale:'+label,rounding,1.)
                assert np.array_equal(fine['potential'][:,:1],coarse['potential'][:,:1])
                assert np.array_equal(fine['energy'][:1],coarse['energy'][:1])
                splits={name:reader.split_values(*sources[name]) for name in channels}
                close(checks,'Endpoint potential telescope:'+label,sources['endpoint54'][0]+sources['endpoint65'][0],sources['endpoint64'][0],1e-8)
                close(checks,'Endpoint residual telescope:'+label,splits['endpoint54']['residual']+splits['endpoint65']['residual'],splits['endpoint64']['residual'],1e-8)
                order4=fine['potential'][:,1:3]
                energy4=fine['energy'][1:3]
                order5=order4+sources['endpoint54'][0]
                energy5=energy4+sources['endpoint54'][1]
                order6=order5+sources['endpoint65'][0]
                energy6=energy5+sources['endpoint65'][1]
                close(checks,'Candidate not double counted:'+label,order6,fine['potential'][:,3:5],1e-10)
                close(checks,'Candidate energy telescope:'+label,energy6,fine['energy'][3:5],1e-10)
                baseline=fine['potential'][:,:1]
                assert np.any(baseline)
                all_potential=np.column_stack([baseline,order4,order5,fine['potential'][:,3:5],fine['potential'][:,7:9]])
                all_energy=np.r_[fine['energy'][:1],energy4,energy5,fine['energy'][3:5],fine['energy'][7:9]]
                central=reader.split_values(all_potential,all_energy)
                close(checks,'Actual baseline preserved:'+label,central['amplitudes'][:,:1],fine['amplitudes'][:,:1],1e-10)
                mock_potential=np.column_stack([baseline,order5,order6,baseline+order5,baseline+order6,sources['endpoint65'][0]])
                mock_energy=np.r_[fine['energy'][:1],energy5,energy6,fine['energy'][:1]+energy5,fine['energy'][:1]+energy6,sources['endpoint65'][1]]
                precise=precise_readout(dict(potential=mock_potential,energy=mock_energy),reader)
                test(checks,'60digit same-baseline cancellation:'+label,precise['same_baseline_cancellation'],1e-8)
                close(checks,'60digit last-step residual:'+label,precise['residual'][:,3:5],splits['endpoint65']['residual'],1e-10)
                close(checks,'60digit last-step amplitudes:'+label,precise['amplitudes'][:,3:5],splits['endpoint65']['amplitudes'],1e-8)
                channel_metrics=np.stack([metrics(splits[name],heat,reader.measure) for name in channels])
                residuals=np.stack([heat*splits[name]['residual'] for name in channels])
                index=[channels.index(name) for name in selected]
                allowance=np.sum(abs(channel_metrics[index]),axis=0)
                pointwise=np.sum(abs(residuals[index]),axis=0)
                coherent=np.sum(residuals[index],axis=0)
                independent_sites=np.sum(abs(np.stack(site_arrays)),axis=(0,1))+abs(residuals[channels.index('endpoint65')])+abs(residuals[channels.index('time_response')])
                envelope_norm=norm(pointwise,reader.measure)
                close(checks,'Time pairing:'+label,splits['time_response']['residual']+splits['baseline_time']['residual'],splits['combined_time']['residual'],1e-8)
                rounding_split=reader.split_values(pair['potential_rounding'],pair['energy_rounding'])
                close(checks,'Explained rounded-total residual:'+label,splits['combined_time']['residual']+rounding_split['residual'],splits['rounded_total_time']['residual'],1e-10)
                time_mock=dict(potential=np.column_stack([coarse['potential'][:,:1],coarse['potential'][:,3:5],fine['potential'][:,3:5],coarse['potential'][:,7:9],fine['potential'][:,7:9],sources['time_response'][0]]),
                    energy=np.r_[coarse['energy'][:1],coarse['energy'][3:5],fine['energy'][3:5],coarse['energy'][7:9],fine['energy'][7:9],sources['time_response'][1]])
                time_precise=precise_readout(time_mock,reader)
                test(checks,'60digit baseline time cancellation:'+label,time_precise['same_baseline_cancellation'],1e-8)
                close(checks,'60digit time residual:'+label,time_precise['residual'][:,3:5],splits['combined_time']['residual'],1e-10)
                test(checks,'Signed response bounded by envelope:'+label,float(np.max(norm(coherent,reader.measure)/np.maximum(envelope_norm,1e-300))),1+1e-10)
                test(checks,'Envelope bounded by norm sum:'+label,float(np.max(envelope_norm/np.maximum(allowance[3],1e-300))),1+1e-10)
                test(checks,'Matched sites bounded by separate sites:'+label,float(np.max(pointwise/np.maximum(independent_sites,1e-300))),1+1e-10)
                central_metrics=metrics(central,heat,reader.measure)
                residual_power=np.stack([np.sum(reader.measure[mask,None]*residuals[:,mask,:]**2,axis=1) for mask in masks],axis=1)
                envelope_power=np.stack([np.sum(reader.measure[mask,None]*pointwise[mask]**2,axis=0) for mask in masks])
                close(checks,'Output regions partition power:'+label,residual_power.sum(axis=1),channel_metrics[:,3,:]**2,1e-10)
                close(checks,'Envelope regions partition power:'+label,envelope_power.sum(axis=0),envelope_norm**2,1e-10)
                contraction=np.divide(abs(channel_metrics[1]),np.maximum(abs(channel_metrics[0]),1e-300))
                ratios={name:(allowance/np.maximum(abs(central_metrics[:,selection]),1e-300)).tolist() for name,selection in
                    [('baseline',slice(0,1)),('mts',slice(5,7)),('total',slice(7,9))]}
                records[label]=dict(heat=heat,contraction65_over54=contraction.tolist(),
                    central_metrics=central_metrics.tolist(),channel_metrics=channel_metrics.tolist(),
                    selected_allowance=allowance.tolist(),allowance_over=ratios,
                    pointwise_envelope_norm=envelope_norm.tolist(),separate_interior_sites_envelope_norm=norm(independent_sites,reader.measure).tolist(),
                    endpoint65_power_by_output_region=residual_power[1].tolist(),envelope_power_by_output_region=envelope_power.tolist(),
                    baseline_step_difference_is_zero=bool(np.all(sources['baseline_time'][0]==0) and np.all(sources['baseline_time'][1]==0)),
                    leading_residual_channel=[selected[position] for position in np.argmax(channel_metrics[index,3,:],axis=0)],
                    mu_y_cancellation_check=precise['same_baseline_cancellation'],time_pair_rounding_identity=identity,total_addition_rounding_ratio=rounding)
                np.savez_compressed(folder/(label+'.npz'),frequency=reader.frequency,measure=reader.measure,heat=heat,
                    channels=np.array(channels),selected=np.array(selected),metrics=np.array(METRICS),base_labels=np.array(base_labels),
                    source_potential=np.stack([sources[name][0] for name in channels]),source_energy=np.stack([sources[name][1] for name in channels]),
                    central_potential=all_potential,central_energy=all_energy,central_metrics=central_metrics,
                    central_residual=heat*central['residual'],channel_metrics=channel_metrics,channel_residual=residuals,
                    site_residuals=np.stack(site_arrays),allowance=allowance,pointwise=pointwise,
                    separate_sites_pointwise=independent_sites,region_edges=region_edges,residual_power=residual_power,
                    envelope_power=envelope_power,coherent=coherent,coarse_potential=coarse['potential'],coarse_energy=coarse['energy'])
                cases[label]=(central,heat,allowance)
                print('budget '+label,flush=True)
    spreads={}
    for model in ['heavy','cold']:
        for match in [20,40]:
            local,heat,local_budget=cases[f'{model}-local-m{match}']
            cubic,other_heat,cubic_budget=cases[f'{model}-cubic-m{match}']
            assert heat==other_heat
            difference=reader.split_values(cubic['potential'][:,5:7]-local['potential'][:,5:7],cubic['energy'][5:7]-local['energy'][5:7])
            spread=metrics(difference,heat,reader.measure)
            spreads[f'{model}-m{match}']=dict(signed_metrics=spread.tolist(),
                ratio_to_summed_partial_allowances=(abs(spread)/np.maximum(local_budget+cubic_budget,1e-300)).tolist(),
                is_fixed_alternative_route_sensitivity_not_error_bound=True)
    summary=dict(stage=167,metric_order=METRICS,channel_order=channels,central_order=base_labels,selected_budget_channels=selected,
        cases=records,saved_local_cubic_spread=spreads,
        budget_type='Finite propagated refinement sensitivity;partial,nonstatistical,not a certified remainder.',
        unresolved_axes=['four other incoming panels at current interior rule','independent endpoint65 site radii',
            'electron/hard-angle/real-emission/virtual-loop quadrature','96-mode frequency truncation',
            'inner thermal-history integration','baseline numerical and physical uncertainty','temperature-law interpolation remainder',
            'nonlinear background and omitted physical terms'],
        band_orders=[6,6,6,8,7,7,6],response_counts=COUNTS,frequency_modes=96,readout_nodes=len(reader.frequency),
        temperature_curve_changed=False,tolerances_changed=False,baseline_inner_rerun=False,
        new_event_evaluations=0,new_response_evolutions=0,reference_history_adopted=False,
        retained_failed_time_pair_checks=8,paired_time_representation_repaired=True,global_numerical_error_bound=None,geometric_tail_assumed=False,statistical_independence_assumed=False,
        output_region_edges=region_edges.tolist(),next_target='Use the final residual-shape budget to select the dominant propagated sensitivity;assess the frozen-temperature-law defect in the same observable space without refitting the curve.')
    write_json(ROOT/'NUMERICAL-SUMMARY-CHECKED.json',summary)
    finish(folder,dict(checks=checks,records=records,paired_baseline_mts=True,summary=str(ROOT/'NUMERICAL-SUMMARY-CHECKED.json')),
        [*inputs,ROOT/'NUMERICAL-SUMMARY-CHECKED.json'])
    failures=[row for row in checks if not row['passed']]
    print(json.dumps(dict(checks=len(checks),failures=failures)),flush=True)
    assert not failures,failures


if __name__=='__main__':
    main()
