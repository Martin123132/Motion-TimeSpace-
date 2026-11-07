from restart_stage182 import *


def validate():
    assert read(ROOT/'progress.json')['state']=='history_assessment_complete'
    assert read(ROOT/'response-progress.json')['state']=='response_assessment_complete'
    paths=authenticate()
    assert paths==read(ROOT/'authenticated-inputs.json')
    for ledger in ['bank-inputs.json','response-inputs.json']:
        for filename,checksum in read(ROOT/ledger).items():
            assert saved.digest(filename)==checksum,filename
    history=read(ROOT/'results/history-checks.json')
    response=read(ROOT/'results/gas-response-checks.json')
    checks=history['checks']+response['checks']
    with np.load(ROOT/'results/history-curvature.npz') as packet:
        assert list(packet['models'])==MODELS
        assert list(packet['branches'])==['native','half','half_thinned','half_early']
        assert list(packet['profile_branches'])==['native','half','half_early']
        assert packet['samples'].shape==(2,4,5) and packet['curves'].shape==(2,4,3) and packet['profiles'].shape==(2,3,5,96)
    config=read(ROOT/'configuration.json')
    updates=0
    for model in MODELS:
        for branch in config['branches']:
            folder=ROOT/'histories'/model/branch
            status=read(folder/'status.json')
            updates+=status['updates']
            with np.load(folder/'history.npz') as packet:
                assert np.all(np.diff(packet['expansion'])>0)
                assert np.isfinite(packet['profiles']).all()
                step=float(packet['step'])
                check(checks,model+'/'+branch+' uniform grid check',np.max(abs(np.diff(packet['expansion'])/step-1)))
                if branch=='half':
                    with np.load(ROOT/'histories'/model/'native/history.npz') as parent:
                        assert np.array_equal(packet['expansion'][::2],parent['expansion'])
                        assert np.array_equal(packet['initial_profile'],parent['initial_profile'])
                        assert np.array_equal(packet['initial_previous_profile'],parent['initial_previous_profile'])
                        assert float(packet['initial_gas'])==float(parent['initial_gas'])
                        assert float(packet['initial_previous_gas'])==float(parent['initial_previous_gas'])
                    check(checks,model+' common start and native-aligned half grid',0)
    assert updates==674
    old_controls=read(PARENT/'results/saved-baseline-controls.json')
    write(ROOT/'results/saved-baseline-controls.json',old_controls)
    assert read(ROOT/'results/saved-baseline-controls.json')==old_controls
    check(checks,'Original full-source baseline/MTS control table preserved',0)
    import scipy
    write(ROOT/'results/runtime.json',dict(python=sys.version,numpy=np.__version__,scipy=scipy.__version__,mpmath=mp.__version__,
        thread_environment={name:os.environ.get(name) for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']}))
    protected=BRANCH.parent.parent/'formalization-workbench'
    start=datetime.fromisoformat(STARTED).timestamp()
    changed=[str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=start]
    check(checks,'Protected workbench recent-mtime count',len(changed),0,'integrity')
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    assert not list(ROOT.rglob('__pycache__'))
    assert authenticate()==paths
    failed=[row for row in checks if not row['passed']]
    identity_failures=[row for row in failed if row['category']=='identity']
    report=dict(stage=182,state='diagnostic_complete',checks=checks,count=len(checks),passed_checks=len(checks)-len(failed),
        all_checks_passed=not failed,failed_checks=failed,identity_failures=identity_failures,
        original_source_packets_replaced=False,original_full_source_decisions_preserved=True,
        original_matched_moving_curvature_gate_passed=False,new_full_varying_temperature_source_evaluated=False,
        gas_only_fixed_anchor_scope=True,scattering_bank_changed=False,emission_bank_changed=False,
        temperature_curve_changed=False,tolerances_changed=False,global_history_replaced=False,
        new_local_history_updates=updates,bitwise_native_restart_updates=122,
        new_real_response_events=36,new_real_integrator_calls=144,new_virtual_loop_integrations=0,
        inherited_stage181_failed_checks=len(read(PARENT/'results/status.json')['failed_checks']),
        protected_workbench_recent_modified_file_count=len(changed),protected_recent_files=changed,
        protected_check_scope='Recent mtime since turn start, not a full before/after directory hash audit',
        authenticated_parent_inputs=paths,
        input_hashes={str(path):saved.digest(path) for directory in ['histories','gas-events','results']
            for path in sorted((ROOT/directory).rglob('*')) if path.is_file() and path.name!='stage-integrity.json' and path!=ROOT/'results/status.json'})
    write(ROOT/'results/status.json',report)
    write(ROOT/'progress.json',dict(state='validation_complete'))
    print(json.dumps(dict(checks=len(checks),passed=report['passed_checks'],identity_failures=identity_failures,
        failed_comparisons=[row for row in failed if row['category']!='identity'],updates=updates)),flush=True)


def report():
    status=read(ROOT/'results/status.json')
    outcomes=read(ROOT/'results/history-comparison.json')
    response=read(ROOT/'results/gas-response-comparison.json')
    controls=read(ROOT/'results/saved-baseline-controls.json')
    lines=['# Stage182: halve the local time step, keep the scattering bank fixed','',
        'The native restart exactly reproduces the saved run. Halving the step changes',
        'the fine-width gas curvature by about0.026%, chiefly through finer interpolation',
        'between saved epochs. Its smaller coarse/fine difference still changes by more',
        'than1%; that failure is retained. No original history or temperature curve is replaced.','',
        '## Restart and controls','',
        '- Primary seeds: native indices5568/5569; evolve through5630.',
        '- Native:61 updates per heavy/cold history, reproducing profiles, gas and work bitwise.',
        '- Half step:122 updates per history, first step using second-order variable-step BDF2.',
        '- Startup control:154 half updates per history, starting16 native steps earlier.',
        '- All674 updates use the original scattering and emission banks and physical coupling.',
        '- Same five temperature probes, widths0.01/0.005, basis, source/derivative1%',
        '  tolerance and identity1e-10 tolerance. No fit or new virtual loop.','',
        '## Local gas-curvature comparison','',
        '|History|Native fine-width curvature|Half-step fine-width curvature|Relative change %|Native coarse/fine change %|Half coarse/fine change %|',
        '|---|---:|---:|---:|---:|---:|']
    for row in outcomes:
        fine=row['comparison'][1]
        lines.append(f"|{row['model']}|{fine['native']:.12g}|{fine['half']:.12g}|{100*fine['relative_change']:.10g}|{100*row['native_width_relative']:.10g}|{100*row['half_width_relative']:.10g}|")
    lines+=['','The full fine-width curvature passes the1% step comparison. Its smaller',
        'width difference is more sensitive:','',
        '|History|Native width difference|Half-step width difference|Relative change %|Earlier-start sensitivity %|',
        '|---|---:|---:|---:|---:|']
    for row in outcomes:
        value=row['comparison'][2]
        lines.append(f"|{row['model']}|{value['native']:.12g}|{value['half']:.12g}|{100*value['relative_change']:.10g}|{100*value['startup_relative']:.10g}|")
    lines+=['','These two width-difference changes fail1%. The earlier-start check is much',
        'smaller and passes, but two resolutions are not a global convergence proof.','',
        '## Separate integration from sampling','',
        'Thin the half-step result back to native-aligned nodes before applying the',
        'same linear interpolation. This changes no evolved values. The exact split is',
        'half_full-native = (half_thinned-native) + (half_full-half_thinned).','',
        '|History|Quantity|Change on common nodes|Change from finer interpolation|Total change|',
        '|---|---|---:|---:|---:|']
    for row in outcomes:
        for value in row['comparison']:
            lines.append(f"|{row['model']}|{value['quantity']}|{value['evolution_change']:.10g}|{value['interpolation_change']:.10g}|{value['half']-value['native']:.10g}|")
    lines+=['','The observed interpolation contribution is thousands of times larger than',
        'the observed common-node evolution change. Tiny evolution changes are near',
        'the prior roundoff/startup sensitivity and should not be assigned a precise',
        'physical sign or treated as rigorous integration-error bounds.','',
        '## Baseline and MTS tested on equal terms','',
        'At the original fixed microscopic anchor, independently evaluate the response',
        'to zero photon departure and unit gas for all36 saved electron/hard-angle',
        'events at x=18.449187113596366. The leading baseline and MTS increment use',
        'the same history, quadrature and precision conventions. Each evaluation also',
        'replays the original incident source as a control. Cached virtual coefficients',
        'are reused;36 real-response event evaluations (144 real integrator calls',
        'including both representations/components) are new, not labelled cache-only.','',
        'With K_component derived from unit-gas response, U_component=K_component*C[g].',
        'The fractional gas-only change is therefore common to baseline and MTS by',
        'linearity, not a new independent empirical success. Their amplitudes differ.','',
        '|Component|History column|Fine-curvature source change %|Width-difference source change %|',
        '|---|---:|---:|---:|']
    for component in ['control','remainder','total']:
        for column in range(4):
            fine=next(row for row in response if row['component']==component and row['column']==column and row['quantity']=='fine_curvature')
            discrepancy=next(row for row in response if row['component']==component and row['column']==column and row['quantity']=='width_discrepancy')
            lines.append(f"|{component}|{column}|{100*fine['relative_change']:.10g}|{100*discrepancy['relative_change']:.10g}|")
    lines+=['','Control=leading baseline; remainder=matched MTS increment; total=sum.',
        'Columns0/1 share heavy gas;2/3 share cold gas. This isolates the gas channel.',
        'The changing photon profile/tail and full temperature-dependent microscopic',
        'source have NOT been propagated here. The original full-source table stays:','',
        '|Component|Moving curvature change %|Fixed curvature change %|Moving passes /4|Fixed passes /4|',
        '|---|---:|---:|---:|---:|']
    for component in ['control','remainder','total']:
        moving=[row for row in controls if row['branch']=='moving_history' and row['component']==component]
        fixed=[row for row in controls if row['branch']=='fixed_incident' and row['component']==component]
        lines.append(f"|{component}|{100*max(row['relative'] for row in moving):.10g}|{100*max(row['relative'] for row in fixed):.10g}|{sum(row['passed'] for row in moving)}|{sum(row['passed'] for row in fixed)}|")
    lines+=['','## Validation and retained failures','',
        f"{status['passed_checks']}/{status['count']} current checks pass;{len(status['failed_checks'])} fail at unchanged thresholds.",
        f"Identity failures:{len(status['identity_failures'])}. All25 Stage181 failed checks remain inherited, along with older flags.",
        'Repeated branch/column source tests are correlated, not independent experiments.','',
        '|Failed comparison|Value|Tolerance|','|---|---:|---:|']
    for row in status['failed_checks']:
        lines.append(f"|{row['name']}|{row['value']:.10g}|{row['tolerance']:.10g}|")
    lines+=['','## What this resolves and the next test','',
        'The tested step refinement does not remove the gas-curvature discrepancy.',
        'It shows that most of this refinement effect comes from temporal sampling,',
        'rather than appreciably changed evolved values on common epochs. Keep the',
        'original source curve and all failed criteria; do not claim complete convergence.',
        'Next, isolate the remaining interpolation contribution with a short quarter-step',
        'restart and the same native-grid thinning control. This is a bounded check',
        'on the1% width-difference failure, not a request to rerun full source integrals.',
        'Then examine the already identified scattering-bank slope break separately',
        'using its saved one-sided derivatives; do not conflate it with time stepping.','',
        '## Integrity','',
        f"{len(status['authenticated_parent_inputs'])} immediate-parent/consumed paths authenticated before and after.",
        'Older archive inherited via seals, not rehashed in full.',
        f"Protected-workbench recent-mtime count:{status['protected_workbench_recent_modified_file_count']}.",
        'One below-normal worker, numerical-library threads1, no subagents or GitHub.',
        'Previous stages unchanged; new child plus additive bookmark heads only.','']
    (ROOT/'RESULTS.md').write_text('\n'.join(lines),encoding='utf-8')


def seal():
    status=read(ROOT/'results/status.json')
    assert status['protected_workbench_recent_modified_file_count']==0
    assert not status['identity_failures']
    assert authenticate()==status['authenticated_parent_inputs']
    for filename,checksum in status['input_hashes'].items():
        assert saved.digest(filename)==checksum,filename
    for filename,checksum in read(ROOT/'response-inputs.json').items():
        assert saved.digest(filename)==checksum,filename
    import psutil
    for process in psutil.process_iter(['pid','name','cmdline']):
        if process.info['pid']==os.getpid():
            continue
        command=' '.join(process.info['cmdline'] or [])
        assert not ('python' in (process.info['name'] or '').lower() and any(script in command for script in ['restart_stage182.py','gas_response_stage182.py']))
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    assert not list(ROOT.rglob('__pycache__'))
    parent=read(PARENT/'results/stage-integrity.json')
    inherited=parent['inherited_sealed_payload_count']+len(parent['file_hashes'])
    assert inherited==336154
    destination=ROOT/'results/stage-integrity.json'
    assert not destination.exists()
    carry_names=['checkpoint_manifest_sha256','local_source_documents','primary_pdfs','source_urls',
        'observational_source_urls','original_library_sha256','native_library_sha256','physical_source_scope',
        'retained_local_approximation_histories','raw_subtraction_response_retained','raw_failed_history_response_retained']
    carried={key:value for key,value in parent.items() if key in carry_names or key.startswith('latest_')}
    hashes={path.relative_to(ROOT).as_posix():saved.digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path!=destination}
    largest=max(sum(path.is_file() for path in folder.iterdir()) for folder in [ROOT,*[path for path in ROOT.rglob('*') if path.is_dir()]])
    assert largest<=500
    write(destination,dict(state='complete',stage=182,completion_qualification='local refinement complete with retained1% width-difference failures',
        sealed_at_utc=datetime.now(timezone.utc).isoformat(),parent_seal_sha256=PARENT_SHA,
        inherited_sealed_payload_count=inherited,file_hashes=hashes,**carried,
        consumed_and_immediate_rehashed=status['authenticated_parent_inputs'],
        previous_primary_source_urls=parent.get('previous_primary_source_urls',[])+parent.get('new_primary_source_urls',[]),new_primary_source_urls=[],
        prior_archive_full_rehash_performed=False,prior_archive_verification_seal_sha256=parent['prior_archive_verification_seal_sha256'],
        prior_payload_verification_scope='Immediate Stage181 and consumed inputs rehashed; older archive inherited through seals.',
        latest_local_half_step_gas_curvature=str(ROOT/'RESULTS.md'),final_validation=str(ROOT/'results/status.json'),
        accepted_current_scope_verified=True,accepted_scope='Local native/half-step coupled evolution, sampling split, and equal fixed-anchor isolated gas response for baseline/MTS.',
        validation_checks=status['count'],passed_validation_checks=status['passed_checks'],
        current_stage_retained_failures=len(status['failed_checks']),all_raw_and_legacy_checks_passed=False,
        retained_failed_checks=parent.get('retained_failed_checks',[])+status['failed_checks'],
        new_local_history_updates=674,native_reproduced_updates=122,
        new_real_response_events=36,new_real_integrator_calls=144,new_virtual_loop_integrations=0,
        incoming_frequency=18.449187113596366,full_population_source_temperature_law_certified=False,
        isolated_gas_channel=True,full_revised_source_history_evaluated=False,
        scattering_bank_changed=False,emission_bank_changed=False,source_curve_changed=False,temperature_curve_changed=False,
        original_source_packets_replaced=False,global_history_replaced=False,tolerances_changed=False,
        baseline_preserved=True,original_matched_moving_curvature_gate_passed=False,scientific_failure_inherited=True,
        bank_knot_causality_proved=False,global_numerical_error_bound=None,
        protected_workbench_recent_modified_file_count=0,protected_check_scope=status['protected_check_scope'],
        maximum_active_workers=1,active_workers_at_seal=0,library_threads_per_worker=1,largest_direct_file_count=largest,
        github_action=False,subagents=0,global_installation_changed=False,galaxy_work_modified=False,
        next_target='Quarter-step short local restart plus native-grid thinning, reusing all fixed gas-response kernels; then isolate the scattering-bank knot.'))
    assert all(saved.digest(ROOT/name)==checksum for name,checksum in hashes.items())
    print(json.dumps(dict(sealed_files=len(hashes),cumulative_payloads=inherited+len(hashes),seal_sha256=saved.digest(destination))),flush=True)


def bookmarks():
    seal_path=ROOT/'results/stage-integrity.json'
    packet=read(seal_path)
    assert all(saved.digest(ROOT/name)==checksum for name,checksum in packet['file_hashes'].items())
    config=read(ROOT/'configuration.json')
    prefix='\n'.join(['# Stage182 COMPLETE — local half step and equal gas-channel controls','',
        f'Latest child: {ROOT}',f'Results: {ROOT / "RESULTS.md"}',f'Status: {ROOT / "results/status.json"}',
        f'Seal SHA256: {saved.digest(seal_path)}',
        f'Sealed payloads: {packet["inherited_sealed_payload_count"]+len(packet["file_hashes"])} (older archive inherited through seals).','',
        'Native restart bitwise; both backgrounds evolved at half step with unchanged banks.',
        'Fine-width gas curvature changes~0.026%; width discrepancy changes~1.50/1.55% (fails unchanged1%).',
        'Most refinement change is sampling/interpolation, not changed states at common epochs.',
        'Baseline/MTS/total isolated gas responses evaluated on equal terms at fixed anchor.',
        'Original full-source decisions, photon/tail histories and temperature curve preserved.',
        'NEXT: bounded quarter-step local restart with thinning; reuse the36 gas kernels, no new loop/source integration.',
        'Then investigate bank-knot one-sided derivatives separately. Local only; no active worker.','',
        '--- Previous bookmark body preserved verbatim after normalized newline handling ---',''])+'\n'
    for filename,checksum in config['prior_bookmark_normalized_sha256'].items():
        path=Path(filename)
        body=path.read_text(encoding='utf-8')
        assert hashlib.sha256(body.encode()).hexdigest()==checksum
        path.write_text(prefix+body,encoding='utf-8')
        updated=path.read_text(encoding='utf-8')
        assert updated.startswith(prefix) and hashlib.sha256(updated[len(prefix):].encode()).hexdigest()==checksum
    print('Additive bookmarks verified; earlier bodies preserved.',flush=True)


if __name__=='__main__':
    source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['validate','report','seal','bookmarks'])
    arguments=parser.parse_args()
    {'validate':validate,'report':report,'seal':seal,'bookmarks':bookmarks}[arguments.phase]()
