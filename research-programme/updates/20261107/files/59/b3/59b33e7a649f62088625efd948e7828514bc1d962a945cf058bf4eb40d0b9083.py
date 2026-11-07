from stage152_order6_common import *
from compare_steps import state_difference


def main():
    modest()
    folder=ROOT/'results/comparison'
    folder.mkdir(parents=True,exist_ok=False)
    allowed=verify_packet(ROOT/'results/readiness')['allowed_cases']
    old_report=verify_packet(PARENT/'results/comparison')
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    reader=ShapeReadout(ladder.basis,canonical=True)
    checks,inputs,readouts,comparisons=[],[ROOT/'results/readiness/status.json',
        PARENT/'results/comparison/status.json',*ladder.inputs],{},{}
    groups={'original':slice(0,2),'revised':slice(2,4),'increment':slice(4,6)}
    components={'difference':slice(12,14),'virtual':slice(14,16),'state':slice(16,18)}
    for model in ['heavy','cold']:
        heat=old_report['metadata'][model]['heat']
        for case,(route,order) in CASES.items():
            if not allowed[case]:
                continue
            states={}
            for count in COUNTS:
                location=ROOT/'results/response'/f'{model}-{case}-{count}'
                assert verify_packet(location)['all_checks_passed']
                final=read_npz(location/'response.npz')
                states[count]=final
                original,revised,increment=[reader.values@final['photon'][-1,:,selection] for selection in groups.values()]
                original_energy,revised_energy,increment_energy=[final['energy'][-1,selection] for selection in groups.values()]
                for match in [20,40]:
                    baseline_key=f'{model}-m{match}'
                    prior_path=PARENT/'results/comparison'/f'{baseline_key}-{route}-order5-4096.npz'
                    prior=read_npz(prior_path)
                    assert np.array_equal(prior['frequency'],reader.frequency)
                    assert np.array_equal(prior['measure'],reader.measure)
                    baseline,old=prior['potential'][:,:1],prior['potential'][:,1:3]
                    baseline_energy,old_energy=prior['energy'][:1],prior['energy'][1:3]
                    potential=np.column_stack([baseline,old,original,revised,old+original,old+revised,
                        baseline+old+original,baseline+old+revised,increment,
                        *[reader.values@final['photon'][-1,:,selection] for selection in components.values()]])
                    energy=np.r_[baseline_energy,old_energy,original_energy,revised_energy,
                        old_energy+original_energy,old_energy+revised_energy,
                        baseline_energy+old_energy+original_energy,baseline_energy+old_energy+revised_energy,increment_energy,
                        *[final['energy'][-1,selection] for selection in components.values()]]
                    split=reader.split_values(potential,energy)
                    label=f'{baseline_key}-{case}-{count}'
                    inherited.invariants(checks,reader,split,label)
                    assert np.array_equal(potential[:,:3],prior['potential'][:,:3])
                    assert np.array_equal(split['amplitudes'][:,:1],prior['amplitudes'][:,:1])
                    checks.append(dict(name='Exact saved baseline/old MTS reuse:'+label,passed=True))
                    test(checks,'Identical baseline/MTS projection:'+label,
                        np.max(abs(split['amplitudes'][:,13:15]-split['amplitudes'][:,:1]-split['amplitudes'][:,9:11]))/
                        max(float(np.max(abs(split['amplitudes'][:,9:11]))),1e-300),1e-8)
                    metrics=inherited.metrics(reader,split,heat)
                    reference_metrics=inherited.metrics(reader,prior,heat)
                    fixed_denominator={name:abs(np.asarray(reference_metrics[name])[7:9]) for name in ['mu','y']}
                    component_budget={name:(sum(abs(np.asarray(metrics[name])[selection]) for selection in [slice(17,19),slice(19,21),slice(21,23)])/fixed_denominator[name]).tolist() for name in ['mu','y']}
                    readouts[label]=dict(metrics=metrics,component_budget=component_budget,
                        fixed_order4_denominator={name:value.tolist() for name,value in fixed_denominator.items()},increment_over_new={name:
                        (np.asarray(metrics[name])[15:17]/np.asarray(metrics[name])[3:5]).tolist() for name in ['mu','y']},
                        increment_over_combined={name:(np.asarray(metrics[name])[15:17]/np.asarray(metrics[name])[7:9]).tolist()
                                                 for name in ['mu','y']})
                    np.savez_compressed(folder/(label+'.npz'),**split,frequency=reader.frequency,measure=reader.measure,heat=heat)
                    inputs.append(prior_path)
                inputs.extend([location/'status.json',location/'response.npz'])
            key=f'{model}-{case}'
            comparisons[key]=dict(state={},spectral={})
            fine_state=states[4096]
            parent_path=BRANCH/'terminal-colder-half-frozen-predictions-20261017/results/response'/f'{model}-{route}-4096/response.npz'
            parent_state=read_npz(parent_path)
            inputs.append(parent_path)
            def photon_norm(value):
                return np.sqrt(np.maximum(np.einsum('...ik,ij,...jk->...k',value,ladder.basis.mass,value),0.))
            reference_photon=photon_norm(parent_state['photon'][...,10:12])
            reference_gas=abs(parent_state['gas'][...,10:12])
            photon_sum=sum(photon_norm(fine_state['photon'][...,selection]) for selection in components.values())
            gas_sum=sum(abs(fine_state['gas'][...,selection]) for selection in components.values())
            assert np.all(reference_photon[-1]>0) and np.all(reference_photon.max(axis=0)>0)
            assert np.all(reference_gas.max(axis=0)>0)
            comparisons[key]['integration_sensitivity']=dict(
                photon_endpoint=(photon_sum[-1]/reference_photon[-1]).tolist(),
                photon_history_over_peak=(photon_sum.max(axis=0)/reference_photon.max(axis=0)).tolist(),
                gas_endpoint_over_peak=(gas_sum[-1]/reference_gas.max(axis=0)).tolist(),
                gas_history_over_peak=(gas_sum.max(axis=0)/reference_gas.max(axis=0)).tolist())
            for group,selection in {**groups,**components}.items():
                record=state_difference(states[2048],states[4096],selection,ladder.basis.mass)
                comparisons[key]['state'][group]=record
                for name,values in record['relative'].items():
                    test(checks,'CONVERGENCE:'+key+':'+group+':'+name,float(max(values)),.01)
            for match in [20,40]:
                baseline_key=f'{model}-m{match}'
                records={}
                for name in ['mu','y']:
                    coarse=np.asarray(readouts[f'{baseline_key}-{case}-2048']['metrics'][name])
                    fine=np.asarray(readouts[f'{baseline_key}-{case}-4096']['metrics'][name])
                    assert np.array_equal(coarse[:3],fine[:3])
                    records[name]={}
                    for group,selection in [('original',slice(3,5)),('revised',slice(5,7)),
                                             ('combined',slice(9,11)),('increment',slice(15,17)),('difference',slice(17,19)),('virtual',slice(19,21)),('state',slice(21,23))]:
                        relative=abs(fine[selection]-coarse[selection])/np.maximum(abs(fine[selection]),1e-300)
                        records[name][group]=dict(fine=fine[selection].tolist(),
                            signed_change=(fine[selection]-coarse[selection]).tolist(),relative_change=relative.tolist())
                        test(checks,'CONVERGENCE:'+baseline_key+':'+case+':'+name+':'+group,float(max(relative)),.01)
                comparisons[key]['spectral'][baseline_key]=records
    contraction={}
    for model in ['heavy','cold']:
        for route in ['local','cubic']:
            if not allowed[f'{route}-order6']:
                continue
            old_state=old_report['comparisons'][f'{model}-{route}-order5']['integration_sensitivity']
            new_state=comparisons[f'{model}-{route}-order6']['integration_sensitivity']
            contraction[f'{model}-{route}-state']={}
            for name in old_state:
                coarse=np.asarray(old_state[name])
                fine=np.asarray(new_state[name])
                ratio=fine/coarse
                contraction[f'{model}-{route}-state'][name]=dict(old_component_sum=coarse.tolist(),new_component_sum=fine.tolist(),ratio=ratio.tolist())
                test(checks,'INTEGRATION_ACCURACY:'+model+':'+route+':'+name,float(max(fine)),.01)
                test(checks,'INTEGRATION_CONTRACTION:'+model+':'+route+':'+name,float(max(ratio)),1.)
            for match in [20,40]:
                key=f'{model}-m{match}-{route}'
                old=old_report['readouts'][f'{key}-order5-4096']
                new=readouts[f'{key}-order6-4096']
                contraction[key]={}
                for name in ['mu','y']:
                    coarse=np.asarray(old['component_budget'][name])
                    fine=np.asarray(new['component_budget'][name])
                    ratio=fine/coarse
                    contraction[key][name]=dict(old_component_sum=coarse.tolist(),new_component_sum=fine.tolist(),ratio=ratio.tolist())
                    test(checks,'INTEGRATION_ACCURACY:'+key+':'+name,float(max(fine)),.01)
                    test(checks,'INTEGRATION_CONTRACTION:'+key+':'+name,float(max(ratio)),1.)
    route_spread={}
    column_order=['baseline']+[prefix+'_source_join'+str(join) for prefix in
        ['old_mts','original','revised','old_plus_original','old_plus_revised',
         'baseline_plus_old_plus_original','baseline_plus_old_plus_revised','increment','difference','virtual','state'] for join in [1,2]]
    finish(folder,dict(checks=checks,allowed_cases=allowed,comparisons=comparisons,readouts=readouts,
        route_spread=route_spread,integration_contraction=contraction,column_order=column_order,metadata=old_report['metadata'],
        counts=COUNTS,modes=96,source_interval=[.75,1.],perturbed_source_anchor=.9375,final_epoch=1e-5,
        convergence_passed=all(row['passed'] for row in checks if row['name'].startswith('CONVERGENCE:')),
        baseline_preserved=True,baseline_inner_history_refined=False,interpolation_spread_is_error_bound=False,
        new_window_inner_feedback_recomputed=False,source_holdout_retest_after_fitting=False,incoming_orders=[3,4,5,6],fixed_budget_reference_order=4,quadrature_other_axes_fixed=True),
        __file__,inputs)
    print(json.dumps(dict(checks=len(checks),allowed_cases=allowed,
        failed=[row for row in checks if not row['passed']],route_spread=route_spread)),flush=True)


if __name__=='__main__':
    main()
