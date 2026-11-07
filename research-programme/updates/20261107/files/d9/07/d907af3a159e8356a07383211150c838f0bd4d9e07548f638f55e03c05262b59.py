from stage150_colder_common import *
from compare_steps import state_difference


def main():
    modest()
    folder=ROOT/'results/comparison'
    folder.mkdir(parents=True,exist_ok=False)
    allowed=verify_packet(ROOT/'results/readiness')['allowed_routes']
    old_report=verify_packet(PARENT/'results/comparison')
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    reader=ShapeReadout(ladder.basis,canonical=True)
    checks,inputs,readouts,comparisons=[],[ROOT/'results/readiness/status.json',
        PARENT/'results/comparison/status.json',*ladder.inputs],{},{}
    groups={'original':slice(0,2),'revised':slice(2,4),'increment':slice(4,6)}
    for model in ['heavy','cold']:
        heat=old_report['metadata'][model]['heat']
        for route in ['local','cubic']:
            if not allowed[route]:
                continue
            states={}
            for count in COUNTS:
                location=ROOT/'results/response'/f'{model}-{route}-{count}'
                assert verify_packet(location)['all_checks_passed']
                final=read_npz(location/'response.npz')
                states[count]=final
                original,revised,increment=[reader.values@final['photon'][-1,:,selection] for selection in groups.values()]
                original_energy,revised_energy,increment_energy=[final['energy'][-1,selection] for selection in groups.values()]
                for match in [20,40]:
                    baseline_key=f'{model}-m{match}'
                    prior_path=PARENT/'results/comparison'/f'{baseline_key}-{route}-4096.npz'
                    prior=read_npz(prior_path)
                    assert np.array_equal(prior['frequency'],reader.frequency)
                    assert np.array_equal(prior['measure'],reader.measure)
                    baseline,old=prior['potential'][:,:1],prior['potential'][:,1:3]
                    baseline_energy,old_energy=prior['energy'][:1],prior['energy'][1:3]
                    potential=np.column_stack([baseline,old,original,revised,old+original,old+revised,
                        baseline+old+original,baseline+old+revised,increment])
                    energy=np.r_[baseline_energy,old_energy,original_energy,revised_energy,
                        old_energy+original_energy,old_energy+revised_energy,
                        baseline_energy+old_energy+original_energy,baseline_energy+old_energy+revised_energy,increment_energy]
                    split=reader.split_values(potential,energy)
                    label=f'{baseline_key}-{route}-{count}'
                    inherited.invariants(checks,reader,split,label)
                    assert np.array_equal(potential[:,:3],prior['potential'][:,:3])
                    assert np.array_equal(split['amplitudes'][:,:1],prior['amplitudes'][:,:1])
                    checks.append(dict(name='Exact saved baseline/old MTS reuse:'+label,passed=True))
                    test(checks,'Identical baseline/MTS projection:'+label,
                        np.max(abs(split['amplitudes'][:,13:15]-split['amplitudes'][:,:1]-split['amplitudes'][:,9:11]))/
                        max(float(np.max(abs(split['amplitudes'][:,9:11]))),1e-300),1e-8)
                    metrics=inherited.metrics(reader,split,heat)
                    readouts[label]=dict(metrics=metrics,increment_over_new={name:
                        (np.asarray(metrics[name])[15:17]/np.asarray(metrics[name])[3:5]).tolist() for name in ['mu','y']},
                        increment_over_combined={name:(np.asarray(metrics[name])[15:17]/np.asarray(metrics[name])[7:9]).tolist()
                                                 for name in ['mu','y']})
                    np.savez_compressed(folder/(label+'.npz'),**split,frequency=reader.frequency,measure=reader.measure,heat=heat)
                    inputs.append(prior_path)
                inputs.extend([location/'status.json',location/'response.npz'])
            key=f'{model}-{route}'
            comparisons[key]=dict(state={},spectral={})
            for group,selection in groups.items():
                record=state_difference(states[2048],states[4096],selection,ladder.basis.mass)
                comparisons[key]['state'][group]=record
                for name,values in record['relative'].items():
                    test(checks,'CONVERGENCE:'+key+':'+group+':'+name,float(max(values)),.01)
            for match in [20,40]:
                baseline_key=f'{model}-m{match}'
                records={}
                for name in ['mu','y']:
                    coarse=np.asarray(readouts[f'{baseline_key}-{route}-2048']['metrics'][name])
                    fine=np.asarray(readouts[f'{baseline_key}-{route}-4096']['metrics'][name])
                    assert np.array_equal(coarse[:3],fine[:3])
                    records[name]={}
                    for group,selection in [('original',slice(3,5)),('revised',slice(5,7)),
                                             ('combined',slice(9,11)),('increment',slice(15,17))]:
                        relative=abs(fine[selection]-coarse[selection])/np.maximum(abs(fine[selection]),1e-300)
                        records[name][group]=dict(fine=fine[selection].tolist(),
                            signed_change=(fine[selection]-coarse[selection]).tolist(),relative_change=relative.tolist())
                        test(checks,'CONVERGENCE:'+baseline_key+':'+route+':'+name+':'+group,float(max(relative)),.01)
                comparisons[key]['spectral'][baseline_key]=records
    route_spread={}
    if all(allowed.values()):
        for model in ['heavy','cold']:
            for match in [20,40]:
                key=f'{model}-m{match}'
                route_spread[key]={}
                for name in ['mu','y']:
                    local=np.asarray(readouts[key+'-local-4096']['metrics'][name])
                    cubic=np.asarray(readouts[key+'-cubic-4096']['metrics'][name])
                    route_spread[key][name]=dict(new_relative=(abs(cubic[5:7]-local[5:7])/abs(cubic[5:7])).tolist(),
                        combined_relative=(abs(cubic[9:11]-local[9:11])/abs(cubic[9:11])).tolist())
    column_order=['baseline']+[prefix+'_source_join'+str(join) for prefix in
        ['old_mts','original','revised','old_plus_original','old_plus_revised',
         'baseline_plus_old_plus_original','baseline_plus_old_plus_revised','increment'] for join in [1,2]]
    finish(folder,dict(checks=checks,allowed_routes=allowed,comparisons=comparisons,readouts=readouts,
        route_spread=route_spread,column_order=column_order,metadata=old_report['metadata'],
        counts=COUNTS,modes=96,source_interval=[.75,1.],final_epoch=1e-5,
        convergence_passed=all(row['passed'] for row in checks if row['name'].startswith('CONVERGENCE:')),
        baseline_preserved=True,baseline_inner_history_refined=False,interpolation_spread_is_error_bound=False,
        new_window_inner_feedback_recomputed=False,source_holdout_retest_after_fitting=False),
        __file__,inputs)
    print(json.dumps(dict(checks=len(checks),allowed_routes=allowed,
        failed=[row for row in checks if not row['passed']],route_spread=route_spread)),flush=True)


if __name__=='__main__':
    main()
