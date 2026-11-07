from stage152_order6_common import *


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=True)
    assert not (folder/'status.json').exists()
    chain=ancestors()
    assert sum(len(packet['file_hashes']) for packet in chain.values())==INHERITED_PAYLOADS
    hashes={}
    def hashed(path):
        path=Path(path).resolve()
        if str(path) not in hashes:
            hashes[str(path)]=digest(path)
        return hashes[str(path)]
    for filename,sha in chain[PARENT/'results/stage-integrity.json']['file_hashes'].items():
        assert hashed(PARENT/filename)==sha
    checks=[dict(name='Stage151 immediate payloads unchanged',passed=True)]
    readiness=verify_packet(ROOT/'results/readiness')
    allowed=readiness['allowed_cases']
    packets=['results/preflight','runs/part0','runs/part1','results/integration-source','results/readiness',
        *[f'results/response/{model}-{case}-{count}' for model in ['heavy','cold']
          for case in CASES if allowed[case] for count in COUNTS],'results/comparison']
    inputs,failures=[],{}
    science=passed=0
    for name in packets:
        location=ROOT/name
        packet=json.loads((location/'status.json').read_text())
        assert packet['state']=='complete' and (location/'COMPLETE').exists()
        assert packet['count']==len(packet['checks'])
        bad=[row['name'] for row in packet['checks'] if not row['passed']]
        prefixes=['ACCURACY:','CONTRACTION:','FORECAST_DIAGNOSTIC:','RAW_MOMENT_DIAGNOSTIC:'] if name=='results/integration-source' else ['READINESS:'] if name=='results/readiness' else ['CONVERGENCE:','INTEGRATION_ACCURACY:','INTEGRATION_CONTRACTION:'] if name=='results/comparison' else []
        assert all(any(label.startswith(prefix) for prefix in prefixes) for label in bad),(name,bad)
        if bad:
            failures[name]=bad
        for filename,sha in packet['input_hashes'].items():
            path=Path(filename)
            assert hashed(path)==sha,path
            if not path.is_relative_to(ROOT):
                inherited.inherited.verify_source(path,chain)
        science+=packet['count']
        passed+=sum(bool(row['passed']) for row in packet['checks'])
        inputs.append(location/'status.json')
        checks.append(dict(name='Sourced complete packet with failures retained:'+name,passed=True))
    source=read_npz(ROOT/'results/integration-source/source.npz')
    source_report=verify_packet(ROOT/'results/integration-source')
    assert source_report['numerical_integrity_all_passed']
    parent_source=read_npz(PARENT/'results/integration-source/source.npz')
    assert all(np.array_equal(source[key],value) for key,value in parent_source.items())
    checks.append(dict(name='Orders3/4/5 and all old anchors/forecasts/components exactly preserved',passed=True))
    def independent_dual(value):
        solved=np.linalg.solve(source['mass'],value)
        return np.sqrt(np.maximum(np.sum(value*solved,axis=0),0.))
    scale=independent_dual(source['actual'][1:-1])
    for order in [5,6]:
        norms=np.asarray([independent_dual(source[f'delta{order}_{key}'][1:-1]) for key in COMPONENTS])
        reported=np.asarray(source_report['metrics'][str(order)]['source_component_sum'])
        independently=norms.sum(axis=0)/scale
        test(checks,'Independent component-sum norm:order'+str(order),
            max(abs(independently-reported)/reported),1e-10)
        for route in ['local','cubic'] if order==6 else []:
            difference=source['source'+str(order)]-source['prediction_'+route]
            error=independent_dual(difference[1:-1])/independent_dual(source['source'+str(order)][1:-1])
            reported=np.asarray(source_report['forecasts'][str(order)][route])
            test(checks,'Frozen forecast reassessment:order'+str(order)+':'+route,max(abs(error-reported)/reported),1e-10)
    proof=verify_packet(ROOT/'results/preflight')
    for part in [0,1]:
        assert len(list((ROOT/'runs'/f'part{part}'/'nodes').rglob('*.npz')))==756
    assert len(list((ROOT/'virtual-cache').rglob('*.json')))==1512
    assert proof['new_unique_events']==1512 and proof['nodes_per_part']==756
    checks.append(dict(name='1512unique order6 events and coefficients;two disjoint shards',passed=True))
    comparison=verify_packet(ROOT/'results/comparison')
    assert comparison['allowed_cases']==allowed and comparison['modes']==96
    assert len(comparison['column_order'])==23
    assert all('_source_join' in label for label in comparison['column_order'][1:])
    assert comparison['baseline_preserved'] and not comparison['baseline_inner_history_refined']
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    reader=ShapeReadout(ladder.basis,canonical=True)
    maximum_budget=maximum_svd=maximum_rewrite=0.
    for model in ['heavy','cold']:
        heat=comparison['metadata'][model]['heat']
        for case,(route,order) in CASES.items():
            if not allowed[case]:
                assert not any((ROOT/'results/response'/f'{model}-{case}-{count}').exists() for count in COUNTS)
                continue
            for count in COUNTS:
                location=ROOT/'results/response'/f'{model}-{case}-{count}'
                data=read_npz(location/'response.npz')
                old=read_npz(PARENT/'results/response'/f'{model}-{route}-order5-{count}/response.npz')
                assert data['photon'].shape==(count+1,96,18)
                assert all(np.isfinite(value).all() for value in data.values())
                for name in ['photon','energy','gas','work','integrated_number_source']:
                    assert np.array_equal(data[name][0,...,:12],old[name][0,...,:12])
                    assert not np.any(data[name][0,...,12:])
                    assert not np.any(data[name][...,6:8])
                checks.append(dict(name='Exact old restart and new zero controls:'+model+':'+case+':'+str(count),passed=True))
                balance=data['energy']+heat*data['gas']+data['work']
                denominator=np.maximum(np.max(abs(data['energy'])+abs(heat*data['gas'])+abs(data['work']),axis=0),1e-300)
                error=float(np.max(abs(balance-balance[0])/denominator))
                maximum_budget=max(maximum_budget,error)
                test(checks,'Independent18column energy/work budget:'+model+':'+case+':'+str(count),error,1e-7)
                maximum_rewrite=max(maximum_rewrite,json.loads((location/'status.json').read_text())['metrics']['source_rewrite'])
                for match in [20,40]:
                    label=f'{model}-m{match}-{case}-{count}'
                    result_path=ROOT/'results/comparison'/(label+'.npz')
                    result=read_npz(result_path)
                    prior_path=PARENT/'results/comparison'/f'{model}-m{match}-{route}-order5-4096.npz'
                    prior=read_npz(prior_path)
                    assert np.array_equal(result['frequency'],prior['frequency'])
                    assert np.array_equal(result['measure'],prior['measure'])
                    assert np.array_equal(result['potential'][:,:3],prior['potential'][:,:3])
                    assert np.array_equal(result['amplitudes'][:,:1],prior['amplitudes'][:,:1])
                    for result_selection,state_selection in [(slice(15,17),slice(4,6)),(slice(17,19),slice(12,14)),(slice(19,21),slice(14,16)),(slice(21,23),slice(16,18))]:
                        assert np.array_equal(result['potential'][:,result_selection],reader.values@data['photon'][-1,:,state_selection])
                    distortion=result['potential']-reader.frequency[:,None]*(result['energy']/reader.capacity)
                    alternate=np.linalg.lstsq(np.sqrt(reader.measure)[:,None]*reader.templates,
                        np.sqrt(reader.measure)[:,None]*distortion,rcond=None)[0]
                    difference=reader.templates@(alternate-result['amplitudes'])
                    numerator=np.sqrt((reader.measure[:,None]*difference**2).sum(axis=0))
                    denominator=np.sqrt((reader.measure[:,None]*distortion**2).sum(axis=0))
                    maximum_svd=max(maximum_svd,float(max(numerator/np.maximum(denominator,1e-300))))
                    for row,name in enumerate(['mu','y']):
                        reported=np.asarray(comparison['readouts'][label]['metrics'][name])
                        assert np.array_equal(reported,heat*result['amplitudes'][row])
                        budget=sum(abs(reported[selection]) for selection in [slice(17,19),slice(19,21),slice(21,23)])/abs(heat*prior['amplitudes'][row,7:9])
                        stored=np.asarray(comparison['readouts'][label]['component_budget'][name])
                        assert np.array_equal(budget,stored)
                        assert np.array_equal(abs(heat*prior['amplitudes'][row,7:9]),np.asarray(comparison['readouts'][label]['fixed_order4_denominator'][name]))
                    checks.append(dict(name='Same baseline/MTS/component projection and budget:'+label,passed=True))
                    inputs.extend([result_path,prior_path])
                inputs.append(location/'response.npz')
    old_comparison=verify_packet(PARENT/'results/comparison')
    for model in ['heavy','cold']:
        for route in ['local','cubic']:
            case=route+'-order6'
            if not allowed[case]:
                continue
            state=read_npz(ROOT/'results/response'/f'{model}-{case}-4096/response.npz')
            reference_path=BRANCH/'terminal-colder-half-frozen-predictions-20261017/results/response'/f'{model}-{route}-4096/response.npz'
            reference=read_npz(reference_path)
            def state_norm(value):
                return np.sqrt(np.maximum(np.einsum('...ik,ij,...jk->...k',value,ladder.basis.mass,value),0.))
            photon_reference=state_norm(reference['photon'][...,10:12])
            gas_reference=abs(reference['gas'][...,10:12])
            photon_sum=sum(state_norm(state['photon'][...,selection]) for selection in [slice(12,14),slice(14,16),slice(16,18)])
            gas_sum=sum(abs(state['gas'][...,selection]) for selection in [slice(12,14),slice(14,16),slice(16,18)])
            independent=dict(photon_endpoint=photon_sum[-1]/photon_reference[-1],
                photon_history_over_peak=photon_sum.max(axis=0)/photon_reference.max(axis=0),
                gas_endpoint_over_peak=gas_sum[-1]/gas_reference.max(axis=0),
                gas_history_over_peak=gas_sum.max(axis=0)/gas_reference.max(axis=0))
            for name,value in independent.items():
                reported=np.asarray(comparison['comparisons'][model+'-'+case]['integration_sensitivity'][name])
                assert np.array_equal(value,reported)
                contraction=comparison['integration_contraction'][f'{model}-{route}-state'][name]
                prior=np.asarray(old_comparison['comparisons'][f'{model}-{route}-order5']['integration_sensitivity'][name])
                assert np.array_equal(prior,np.asarray(contraction['old_component_sum']))
                assert np.array_equal(value/prior,np.asarray(contraction['ratio']))
            for match in [20,40]:
                key=f'{model}-m{match}-{route}'
                for name in ['mu','y']:
                    previous=np.asarray(old_comparison['readouts'][key+'-order5-4096']['component_budget'][name])
                    current=np.asarray(comparison['readouts'][key+'-order6-4096']['component_budget'][name])
                    contraction=comparison['integration_contraction'][key][name]
                    assert np.array_equal(previous,np.asarray(contraction['old_component_sum']))
                    assert np.array_equal(current/previous,np.asarray(contraction['ratio']))
            checks.append(dict(name='Independent fixed-S4 state and spectral contraction:'+model+':'+route,passed=True))
            inputs.append(reference_path)
    test(checks,'Source rewrite on own norm throughout response',maximum_rewrite,1e-10)
    test(checks,'Independent baseline/MTS weighted SVD',maximum_svd,1e-10)
    scripts=sorted(ROOT.glob('*.py'))
    for script in scripts:
        compile(script.read_text(),str(script),'exec')
    assert not list(ROOT.rglob('__pycache__'))
    largest=max(len(files) for directory,directories,files in os.walk(ROOT))
    assert largest<1000
    workbench=POST.parent/'formalization-workbench'
    assert not [path for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    checks.append(dict(name='Scripts compile,no bytecode,folder limit,protected workbench count0',passed=True))
    source_stable=all(row['passed'] for row in source_report['checks'] if row['name'].startswith(('ACCURACY:','CONTRACTION:')))
    propagated_stable=all(row['passed'] for row in comparison['checks'] if row['name'].startswith(('INTEGRATION_ACCURACY:','INTEGRATION_CONTRACTION:')))
    next_target='Use the order6 source and saved response to quantify whether the frozen colder-half interpolation failure exceeds the observed incoming-rule uncertainty; retain the other fixed integration axes as separate outstanding numerical uncertainties.'
    if not source_stable:
        next_target='Diagnose the order6-versus5 component changes using the saved frequency-resolved event contributions before spending on another order; retain the fixed order4 denominators and original frozen predictions.'
    elif not propagated_stable:
        next_target='Inspect the noncontracting propagated component using saved histories and fixed denominators before extending the temperature curve.'
    if not all(allowed.values()):
        next_target='Resolve blocked small-component numerical readiness without changing source-accuracy tolerances; retain every raw source result.'
    elif not comparison['convergence_passed']:
        next_target='Refine only the failed response-step diagnostic before interpreting its physical integration sensitivity.'
    summary=dict(stage=152,scientific_checks=science,passing_scientific_checks=passed,
        retained_failed_checks=science-passed,failed_by_packet=failures,packets=packets,
        source_metrics=source_report['metrics'],source_contraction=source_report['contraction'],
        frozen_prediction_diagnostics=source_report['forecasts'],
        source_arithmetic_change=source_report['source_arithmetic_change'],
        allowed_cases=allowed,convergence_passed=comparison['convergence_passed'],
        comparisons=comparison['comparisons'],readouts=comparison['readouts'],
        integration_response_contraction=comparison['integration_contraction'],
        maximum_energy_work_residual=maximum_budget,maximum_source_rewrite=maximum_rewrite,
        maximum_independent_svd_relative=maximum_svd,source_readiness=readiness['rows'],
        new_unique_physical_events=1512,shared_nodes=0,reused_order4_nodes=1008,reused_control_nodes=4608,
        frequency_modes=96,incoming_orders=[3,4,5,6],response_steps=COUNTS,source_anchor=.9375,final_epoch=1e-5,
        baseline_preserved=True,baseline_inner_history_refined=False,
        other_quadrature_axes_refined=False,continuum_error_bounded=False,
        accepted_scope='Four incoming-frequency rules at the saved colder temperature; fixed-reference5-to6 versus4-to5 component-resolved conditional baseline/MTS response sensitivity',
        next_target=next_target)
    write_json(ROOT/'NUMERICAL-SUMMARY.json',summary)
    consumed={path:sha for path,sha in hashes.items() if not Path(path).is_relative_to(ROOT)}
    finish(folder,dict(checks=checks,accepted_scope_verified=all(row['passed'] for row in checks),
        consumed_and_immediate_rehashed=consumed,rehashed_prior_files=len(consumed),
        scientific_checks=science,passing_scientific_checks=passed,compiled_scripts=len(scripts),
        largest_direct_file_count=largest,protected_workbench_recent_modified_file_count=0),
        __file__,[*inputs,ROOT/'NUMERICAL-SUMMARY.json'])
    print(json.dumps(dict(validation_checks=len(checks),passed=all(row['passed'] for row in checks),
        science=science,science_passed=passed,rehashed_prior_files=len(consumed),
        allowed_cases=allowed,convergence_passed=comparison['convergence_passed'])),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
