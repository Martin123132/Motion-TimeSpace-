from stage150_colder_common import *


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
    for name,sha in chain[PARENT/'results/stage-integrity.json']['file_hashes'].items():
        assert hashed(PARENT/name)==sha,name
    checks=[dict(name='Immediate Stage149 payloads unchanged',passed=True)]
    readiness=verify_packet(ROOT/'results/readiness')
    allowed=readiness['allowed_routes']
    packets=['results/preflight','runs/expensive-holdout','runs/control-holdout',
        'results/holdout-source','results/readiness',
        *[f'results/response/{model}-{route}-{count}' for model in ['heavy','cold']
          for route in ['local','cubic'] if allowed[route] for count in COUNTS],'results/comparison']
    inputs,failures=[],{}
    science=passed=0
    for name in packets:
        location=ROOT/name
        report=json.loads((location/'status.json').read_text())
        assert report['state']=='complete' and (location/'COMPLETE').exists()
        assert report['count']==len(report['checks'])
        bad=[row['name'] for row in report['checks'] if not row['passed']]
        if bad:
            prefixes=['PREDICTION_DIAGNOSTIC:','RAW_MOMENT_DIAGNOSTIC:'] if name=='results/holdout-source' else ['CONVERGENCE:'] if name=='results/comparison' else ['Unchanged own-source rewrite gate:','Corrected energy moment:','Independent gas absolute change:'] if name=='results/readiness' else []
            assert all(any(item.startswith(prefix) for prefix in prefixes) for item in bad),(name,bad)
            failures[name]=bad
        for filename,sha in report['input_hashes'].items():
            path=Path(filename)
            assert hashed(path)==sha,path
            if not path.is_relative_to(ROOT):
                inherited.inherited.verify_source(path,chain)
        science+=report['count']
        passed+=sum(bool(row['passed']) for row in report['checks'])
        inputs.append(location/'status.json')
        checks.append(dict(name='Complete sourced packet with failures retained:'+name,passed=True))
    proof=verify_packet(ROOT/'results/preflight')
    frozen=read_npz(ROOT/'results/preflight/frozen-inputs.npz')
    source=read_npz(ROOT/'results/holdout-source/source.npz')
    source_report=verify_packet(ROOT/'results/holdout-source')
    assert digest(ROOT/'results/preflight/frozen-inputs.npz')==proof['frozen_inputs_sha256']
    assert source_report['numerical_integrity_all_passed']
    for name in ['start','centre','end','curvature','warm_defect','prediction_local','prediction_cubic']:
        assert np.array_equal(source[name],frozen[name]),name
    actual=source['actual']
    for kind in ['local','cubic']:
        difference=actual-frozen['prediction_'+kind]
        solved=np.linalg.solve(source['mass'],difference[1:-1])
        absolute=np.sqrt(np.maximum(np.sum(difference[1:-1]*solved,axis=0),0.))
        actual_solved=np.linalg.solve(source['mass'],actual[1:-1])
        scale=np.sqrt(np.maximum(np.sum(actual[1:-1]*actual_solved,axis=0),0.))
        relative=absolute/scale
        reported=np.asarray(source_report['metrics'][kind]['source_relative'])
        test(checks,'Independent actual-source normalized prediction error:'+kind,
             float(np.max(abs(relative-reported)/np.maximum(reported,1e-300))),1e-10)
    frozen_time=datetime.fromisoformat(proof['finished_utc']).timestamp()
    for part in ['expensive','control']:
        node_paths=list((ROOT/'runs'/f'{part}-holdout/nodes').rglob('*.npz'))
        assert node_paths and min(path.stat().st_mtime for path in node_paths)>=frozen_time
        config=json.loads((ROOT/'runs'/f'{part}-holdout/configuration.json').read_text())
        assert config['fingerprints'][str(ROOT/'results/preflight/status.json')]==digest(ROOT/'results/preflight/status.json')
    checks.append(dict(name='Numeric forecasts frozen before both physical node productions',passed=True))
    for route in ['local','cubic']:
        test(checks,'Measured defect retains frozen prediction:'+route,
             float(np.max(abs(source['defect_'+route]-(actual-frozen['prediction_'+route]))))/
             max(float(np.max(abs(source['defect_'+route]))),1e-300),1e-12)
        assert cold_bubble(.75,route)==1.
        assert all(cold_bubble(phase,route)==0. for phase in [0.,.25,.5,1.])
        revised=original_source(source,.75,route)+cold_bubble(.75,route)*source['defect_'+route]
        test(checks,'Post-test interpolation identity,not independent prediction:'+route,
            float(np.max(dual_norm((revised-actual)[1:-1],source['mass'])/
                         dual_norm(actual[1:-1],source['mass']))),1e-12)
    comparison=verify_packet(ROOT/'results/comparison')
    assert comparison['allowed_routes']==allowed and comparison['modes']==96
    assert not comparison['baseline_inner_history_refined']
    assert len(comparison['column_order'])==17
    assert all('_source_join' in name for name in comparison['column_order'][1:])
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    reader=ShapeReadout(ladder.basis,canonical=True)
    maximum_budget=maximum_svd=maximum_rewrite=0.
    for model in ['heavy','cold']:
        heat=comparison['metadata'][model]['heat']
        for route in ['local','cubic']:
            if not allowed[route]:
                assert not any((ROOT/'results/response'/f'{model}-{route}-{count}').exists() for count in COUNTS)
                continue
            states={}
            for count in COUNTS:
                location=ROOT/'results/response'/f'{model}-{route}-{count}'
                data=read_npz(location/'response.npz')
                states[count]=data
                old=read_npz(PARENT/'results/response'/f'{model}-{route}-{count}/response.npz')
                assert data['photon'].shape==(count+1,96,12)
                assert all(np.isfinite(value).all() for value in data.values())
                for name in ['photon','energy','gas','work','integrated_number_source']:
                    assert np.array_equal(data[name][0],old[name][0])
                    assert np.array_equal(data[name][...,6:8],np.zeros_like(data[name][...,6:8]))
                checks.append(dict(name='Fixed restart and zero control:'+model+':'+route+':'+str(count),passed=True))
                budget=data['energy']+heat*data['gas']+data['work']
                scale=np.maximum(np.max(abs(data['energy'])+abs(heat*data['gas'])+abs(data['work']),axis=0),1e-300)
                error=float(np.max(abs(budget-budget[0])/scale))
                maximum_budget=max(maximum_budget,error)
                test(checks,'Independent energy/work budget:'+model+':'+route+':'+str(count),error,1e-7)
                maximum_rewrite=max(maximum_rewrite,json.loads((location/'status.json').read_text())['metrics']['source_rewrite'])
                for match in [20,40]:
                    key=f'{model}-m{match}'
                    label=f'{key}-{route}-{count}'
                    result_path=ROOT/'results/comparison'/(label+'.npz')
                    result=read_npz(result_path)
                    prior_path=PARENT/'results/comparison'/f'{key}-{route}-4096.npz'
                    prior=read_npz(prior_path)
                    assert np.array_equal(result['frequency'],prior['frequency'])
                    assert np.array_equal(result['measure'],prior['measure'])
                    assert np.array_equal(result['potential'][:,:3],prior['potential'][:,:3])
                    assert np.array_equal(result['amplitudes'][:,:1],prior['amplitudes'][:,:1])
                    if count==4096:
                        for new_selection,old_selection,replay_label in [
                                (slice(3,5),slice(5,7),'source-window response'),
                                (slice(11,13),slice(13,15),'baseline plus accumulated MTS')]:
                            difference=result['potential'][:,new_selection]-prior['potential'][:,old_selection]
                            scale=max(float(np.max(abs(prior['potential'][:,old_selection]))),1e-300)
                            test(checks,'Route-specific Stage149 readout replay:'+replay_label+':'+model+':'+route+':'+str(match),
                                 float(np.max(abs(difference)))/scale,1e-10)
                    assert np.array_equal(result['potential'][:,15:17],reader.values@data['photon'][-1,:,4:6])
                    distortion=result['potential']-reader.frequency[:,None]*(result['energy']/reader.capacity)
                    alternate=np.linalg.lstsq(np.sqrt(reader.measure)[:,None]*reader.templates,
                        np.sqrt(reader.measure)[:,None]*distortion,rcond=None)[0]
                    difference=reader.templates@(alternate-result['amplitudes'])
                    numerator=np.sqrt((reader.measure[:,None]*difference**2).sum(axis=0))
                    denominator=np.sqrt((reader.measure[:,None]*distortion**2).sum(axis=0))
                    maximum_svd=max(maximum_svd,float(np.max(numerator/np.maximum(denominator,1e-300))))
                    for row,name in enumerate(['mu','y']):
                        assert np.array_equal(np.asarray(comparison['readouts'][label]['metrics'][name]),heat*result['amplitudes'][row])
                    checks.append(dict(name='Identical per-column baseline/MTS decomposition:'+label,passed=True))
                    inputs.extend([result_path,prior_path])
                inputs.append(location/'response.npz')
            delta=states[4096]['photon'][-1,:,4:6]-states[2048]['photon'][-1,:,4:6]
            endpoint=np.sqrt(np.maximum(np.sum(delta*(ladder.basis.mass@delta),axis=0),0.))
            reported=np.asarray(comparison['comparisons'][model+'-'+route]['state']['increment']['absolute']['photon_endpoint'])
            test(checks,'Independent isolated defect convergence norm:'+model+':'+route,
                float(np.max(abs(endpoint-reported)/np.maximum(endpoint,1e-300))),1e-10)
    test(checks,'Source-rewrite gate retained throughout response',maximum_rewrite,1e-10)
    test(checks,'Independent spectral SVD',maximum_svd,1e-10)
    scripts=sorted(ROOT.glob('*.py'))
    for script in scripts:
        compile(script.read_text(encoding='utf-8'),str(script),'exec')
    assert not list(ROOT.rglob('__pycache__'))
    largest=max(len(files) for directory,directories,files in os.walk(ROOT))
    assert largest<1000
    workbench=POST.parent/'formalization-workbench'
    assert not [path for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    checks.append(dict(name='Compiled scripts,no bytecode,folder limit,protected workbench mtime count0',passed=True))
    next_target='Check the physical event-quadrature uncertainty at f=.9375 using saved component sums as the reference, before further temperature-curve refinement; keep both histories, joins, baseline and numerical gates fixed.'
    if not all(allowed.values()):
        next_target='Resolve the explicitly blocked source-rewrite routes before adopting their responses; keep the holdout prediction result unchanged.'
    elif not comparison['convergence_passed']:
        next_target='Refine the failed isolated response-step diagnostics before adopting the corresponding readout.'
    summary=dict(stage=150,scientific_checks=science,passing_scientific_checks=passed,
        retained_failed_checks=science-passed,failed_by_packet=failures,packets=packets,
        holdout_fraction=.9375,primary_prediction_passed=source_report['primary_prediction_passed'],
        prediction_passed=source_report['prediction_passed'],
        prediction_metrics=source_report['metrics'],source_arithmetic_change=source_report['arithmetic_relative_change'],
        new_physical_event_nodes=5616,new_virtual_coefficients=1008,
        allowed_routes=allowed,convergence_passed=comparison['convergence_passed'],
        comparisons=comparison['comparisons'],readouts=comparison['readouts'],route_spread=comparison['route_spread'],
        maximum_energy_work_residual=maximum_budget,maximum_response_source_rewrite=maximum_rewrite,
        maximum_independent_svd_relative=maximum_svd,source_readiness=readiness['rows'],
        baseline_preserved=True,baseline_inner_history_refined=False,new_window_inner_feedback_recomputed=False,
        final_epoch=1e-5,frequency_modes=96,response_steps=COUNTS,event_grid_uncertainty_bounded=False,
        accepted_scope='Frozen independent source-prediction test; separately qualified response to measured interpolation defect',
        next_target=next_target)
    write_json(ROOT/'NUMERICAL-SUMMARY.json',summary)
    consumed={path:sha for path,sha in hashes.items() if not Path(path).is_relative_to(ROOT)}
    finish(folder,dict(checks=checks,accepted_scope_verified=all(row['passed'] for row in checks),
        consumed_and_immediate_rehashed=consumed,rehashed_prior_files=len(consumed),
        compiled_scripts=len(scripts),largest_direct_file_count=largest,
        scientific_checks=science,passing_scientific_checks=passed,protected_workbench_recent_modified_file_count=0),
        __file__,[*inputs,ROOT/'NUMERICAL-SUMMARY.json'])
    print(json.dumps(dict(validation_checks=len(checks),passed=all(row['passed'] for row in checks),
        science=science,science_passed=passed,rehashed_prior_files=len(consumed),
        primary_prediction_passed=source_report['primary_prediction_passed'],
        allowed_routes=allowed,convergence_passed=comparison['convergence_passed'])),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
