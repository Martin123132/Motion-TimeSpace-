from stage148_terminal_common import *


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
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
    checks=[dict(name='All immediate parent payloads intact',passed=True)]
    packets=['results/preflight',*[f'runs/{part}-{epoch}' for epoch in FRACTIONS for part in ['expensive','control']],
        'results/terminal-sources','results/readiness',
        *[f'results/response/{model}-{count}' for model in ['heavy','cold'] for count in COUNTS],
        'results/comparison']
    inputs,failures=[],{}
    science=passed=0
    for name in packets:
        location=ROOT/name
        report=json.loads((location/'status.json').read_text())
        assert report['state']=='complete' and (location/'COMPLETE').exists()
        assert report['count']==len(report['checks'])
        bad=[row['name'] for row in report['checks'] if not row['passed']]
        if bad:
            allowed=['FORECAST_DIAGNOSTIC:','INTERPOLATION_DIAGNOSTIC:','RAW_MOMENT_DIAGNOSTIC:'] if name=='results/terminal-sources' else ['CONVERGENCE:'] if name=='results/comparison' else []
            assert all(any(item.startswith(prefix) for prefix in allowed) for item in bad),(name,bad)
            failures[name]=bad
        for filename,sha in report['input_hashes'].items():
            path=Path(filename)
            assert hashed(path)==sha,path
            if not path.is_relative_to(ROOT):
                inherited.inherited.verify_source(path,chain)
        science+=report['count']
        passed+=sum(bool(row['passed']) for row in report['checks'])
        inputs.append(location/'status.json')
        checks.append(dict(name='Complete sourced packet with failures explicitly classified:'+name,passed=True))
    preflight=verify_packet(ROOT/'results/preflight')
    frozen_path=ROOT/'results/preflight/frozen-inputs.npz'
    assert digest(frozen_path)==preflight['frozen_inputs_sha256']
    frozen=read_npz(frozen_path)
    source=read_npz(ROOT/'results/terminal-sources/source.npz')
    assert np.array_equal(source['start'],frozen['start_source'])
    assert np.array_equal(source['start'],read_npz(REPAIRED/'results/reaggregation/end/source.npz')['remainder'])
    checks.append(dict(name='Actual prior endpoint reused exactly',passed=True))
    readiness=verify_packet(ROOT/'results/readiness')
    assert readiness['all_checks_passed'] and readiness['energy_coordinate_evolution_allowed']
    comparison=verify_packet(ROOT/'results/comparison')
    assert comparison['counts']==COUNTS and comparison['modes']==96
    assert not comparison['baseline_inner_history_refined']
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    reader=ShapeReadout(ladder.basis,canonical=True)
    maximum_budget=maximum_svd=maximum_rewrite=0.
    for model in ['heavy','cold']:
        heat=comparison['metadata'][model]['heat']
        old=read_npz(PARENT/'results/response'/f'{model}-4096/active/response.npz')
        states={}
        for count in COUNTS:
            location=ROOT/'results/response'/f'{model}-{count}'
            data=read_npz(location/'response.npz')
            states[count]=data
            assert data['photon'].shape==(count+1,96,12)
            assert all(np.isfinite(value).all() for value in data.values())
            assert abs(data['coordinate'][0]/data['coordinate'][-1]-.75)<1e-14
            for key in ['photon','energy','gas','work','integrated_number_source']:
                assert np.array_equal(data[key][0,...,8:10],old[key][-1,...,10:12])
                assert np.array_equal(data[key][0,...,10:12],old[key][-1,...,10:12])
                assert np.array_equal(data[key][0,...,:8],np.zeros_like(data[key][0,...,:8]))
                assert np.array_equal(data[key][...,6:8],np.zeros_like(data[key][...,6:8]))
            checks.append(dict(name='Fixed restart and exact zero control:'+model+':'+str(count),passed=True))
            budget=data['energy']+heat*data['gas']+data['work']
            scale=np.maximum(np.max(abs(data['energy'])+abs(heat*data['gas'])+abs(data['work']),axis=0),1e-300)
            residual=float(np.max(abs(budget-budget[0])/scale))
            maximum_budget=max(maximum_budget,residual)
            test(checks,'Independent stored energy-work budget:'+model+':'+str(count),residual,1e-7)
            maximum_rewrite=max(maximum_rewrite,json.loads((location/'status.json').read_text())['metrics']['source_rewrite'])
            for match in [20,40]:
                key=f'{model}-m{match}'
                label=key+'-'+str(count)
                result_path=ROOT/'results/comparison'/(label+'.npz')
                result=read_npz(result_path)
                prior_path=PARENT/'results/comparison'/f'{key}-4096.npz'
                prior=read_npz(prior_path)
                assert np.array_equal(result['frequency'],prior['frequency'])
                assert np.array_equal(result['measure'],prior['measure'])
                assert np.array_equal(result['potential'][:,:1],prior['potential'][:,:1])
                assert np.array_equal(result['amplitudes'][:,:1],prior['amplitudes'][:,:1])
                assert np.array_equal(result['potential'][:,1:3],prior['potential'][:,9:11])
                assert np.array_equal(result['potential'][:,15:17],reader.values@data['photon'][-1,:,4:6])
                distortion=result['potential']-reader.frequency[:,None]*(result['energy']/reader.capacity)
                alternate=np.linalg.lstsq(np.sqrt(reader.measure)[:,None]*reader.templates,
                    np.sqrt(reader.measure)[:,None]*distortion,rcond=None)[0]
                error=reader.templates@(alternate-result['amplitudes'])
                numerator=np.sqrt((reader.measure[:,None]*error**2).sum(axis=0))
                denominator=np.sqrt((reader.measure[:,None]*distortion**2).sum(axis=0))
                maximum_svd=max(maximum_svd,float(np.max(numerator/np.maximum(denominator,1e-300))))
                for row,name in enumerate(['mu','y']):
                    assert np.array_equal(np.asarray(comparison['readouts'][label]['metrics'][name]),heat*result['amplitudes'][row])
                checks.append(dict(name='Identical independent baseline/MTS spectral decomposition:'+label,passed=True))
                inputs.extend([result_path,prior_path])
            inputs.append(location/'response.npz')
        for group,selection in [('quadratic',slice(2,4)),('curvature',slice(4,6))]:
            delta=states[4096]['photon'][-1,:,selection]-states[2048]['photon'][-1,:,selection]
            endpoint=np.sqrt(np.maximum(np.sum(delta*(ladder.basis.mass@delta),axis=0),0.))
            recorded=np.asarray(comparison['comparisons'][model]['state'][group]['absolute']['photon_endpoint'])
            test(checks,'Independent photon convergence norm:'+model+':'+group,
                float(np.max(abs(endpoint-recorded)/np.maximum(endpoint,1e-300))),1e-10)
            gas_delta=abs(states[4096]['gas'][-1,selection]-states[2048]['gas'][-1,selection])
            assert np.array_equal(gas_delta,np.asarray(comparison['comparisons'][model]['state'][group]['absolute']['gas_endpoint']))
        for match in [20,40]:
            key=f'{model}-m{match}'
            spectra=[read_npz(ROOT/'results/comparison'/f'{key}-{count}.npz') for count in COUNTS]
            for row,name in enumerate(['mu','y']):
                values=[heat*item['amplitudes'][row,15:17] for item in spectra]
                relative=abs(values[1]-values[0])/np.maximum(abs(values[1]),1e-300)
                assert np.array_equal(relative,np.asarray(comparison['comparisons'][model]['spectral'][key][name]['curvature']['relative_change']))
                checks.append(dict(name='Isolated curvature '+name+' convergence uses its own scale:'+key,passed=True))
    test(checks,'Unchanged source rewrite limit throughout response',maximum_rewrite,1e-10)
    test(checks,'Independent spectral SVD',maximum_svd,1e-10)
    scripts=sorted(ROOT.glob('*.py'))
    for script in scripts:
        compile(script.read_text(encoding='utf-8'),str(script),'exec')
    assert not list(ROOT.rglob('__pycache__'))
    largest=max(len(files) for directory,directories,files in os.walk(ROOT))
    assert largest<1000
    workbench=POST.parent/'formalization-workbench'
    assert not [path for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    checks.append(dict(name='Compiled scripts,no bytecode,folder safety,protected workbench mtime count0',passed=True))
    source_report=verify_packet(ROOT/'results/terminal-sources')
    summary=dict(stage=148,scientific_checks=science,passing_scientific_checks=passed,
        retained_failed_checks=science-passed,failed_by_packet=failures,packets=packets,
        new_physical_event_nodes=11232,new_virtual_coefficients=2016,
        source_interval=[.75,1.],represented_source_union=[.25,1.],final_epoch=1e-5,
        source_metrics=source_report['metrics'],maximum_source_rewrite=maximum_rewrite,
        maximum_energy_work_residual=maximum_budget,maximum_independent_svd_relative=maximum_svd,
        comparisons=comparison['comparisons'],readouts=comparison['readouts'],
        convergence_passed=comparison['convergence_passed'],frequency_modes=96,response_steps=COUNTS,
        baseline_preserved=True,baseline_inner_history_refined=False,new_window_inner_feedback_recomputed=False,
        rigorous_error_bound=False,event_grid_uncertainty_bounded=False,
        accepted_scope='New actual source anchors at .875 and1; repaired arithmetic, window response and matched baseline/MTS readout',
        next_target=('Test an independent non-midpoint temperature within .75-to1 with frozen predictions and identical baseline/MTS treatment.'
                     if comparison['convergence_passed'] else 'Resolve retained response time-step convergence failures before adopting the new final readout.'))
    write_json(ROOT/'NUMERICAL-SUMMARY.json',summary)
    consumed={path:sha for path,sha in hashes.items() if not Path(path).is_relative_to(ROOT)}
    finish(folder,dict(checks=checks,accepted_scope_verified=all(row['passed'] for row in checks),
        consumed_and_immediate_rehashed=consumed,rehashed_prior_files=len(consumed),
        compiled_scripts=len(scripts),largest_direct_file_count=largest,
        scientific_checks=science,passing_scientific_checks=passed,
        protected_workbench_recent_modified_file_count=0),__file__,[*inputs,ROOT/'NUMERICAL-SUMMARY.json'])
    print(json.dumps(dict(validation_checks=len(checks),passed=all(row['passed'] for row in checks),
        science=science,science_passed=passed,rehashed_prior_files=len(consumed),
        maximum_budget=maximum_budget,maximum_source_rewrite=maximum_rewrite)),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()

