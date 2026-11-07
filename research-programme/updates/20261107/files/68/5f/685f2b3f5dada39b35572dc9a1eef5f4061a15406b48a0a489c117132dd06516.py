from quarter_step_stage183 import *


def validate():
    assert read(ROOT / 'progress.json')['state'] == 'response_assessment_complete'
    config = read(ROOT / 'configuration.json')
    paths = authenticate()
    assert paths == read(ROOT / 'authenticated-inputs.json')
    checks = read(ROOT / 'results/history-checks.json')['checks'] + read(ROOT / 'results/gas-response-checks.json')['checks']
    assert read(ROOT / 'bank-inputs.json') == read(PARENT / 'bank-inputs.json')
    for ledger in ['bank-inputs.json', 'response-inputs.json']:
        for filename, checksum in read(ROOT / ledger).items():
            assert saved.digest(filename) == checksum
    check(checks, 'Scattering and emission bank hashes identical to Stage182', 0)
    updates = 0
    for model in MODELS:
        for branch in config['branches']:
            folder = ROOT / 'histories' / model / branch
            status = read(folder / 'status.json')
            assert saved.digest(folder / 'history.npz') == status['history_sha256']
            updates += status['updates']
            with np.load(folder / 'history.npz') as packet:
                assert packet['profiles'].shape == (status['updates'] + 1, 96)
                assert np.all(np.isfinite(packet['profiles']))
                assert np.all(np.isfinite(packet['temperature_scaled']))
                assert int(packet['end_index']) == config['end_index']
                assert status['updates'] == (config['end_index'] - int(packet['start_index'])) * 4
                with np.load(PARENT / 'histories' / model / ('half_early' if branch == 'quarter_early' else 'half') / 'history.npz') as parent:
                    assert np.array_equal(packet['expansion'][::2], parent['expansion'])
                    assert np.array_equal(packet['coordinates'], parent['coordinates'])
                    for field in ['initial_profile', 'initial_previous_profile', 'initial_gas', 'initial_previous_gas']:
                        assert np.array_equal(packet[field], parent[field])
                check(checks, model + '/' + branch + ': saved-grid/seed consistency', 0)
    assert updates == 1104
    with np.load(ROOT / 'results/history-curvature.npz') as packet:
        assert packet['curves'].shape == (2, 8, 3) and packet['samples'].shape == (2, 8, 5)
    with np.load(ROOT / 'results/gas-response.npz') as packet:
        assert packet['responses'].shape == (8, 3, 6, 98, 4)
        assert np.isfinite(packet['responses']).all()
        with np.load(PARENT / 'results/gas-response.npz') as parent:
            assert np.array_equal(packet['kernels'], parent['kernels'])
            assert np.array_equal(packet['responses'][:4], parent['responses'])
        check(checks, 'Old cached gas kernels and all old source responses unchanged', 0)
    controls = read(PARENT / 'results/saved-baseline-controls.json')
    write(ROOT / 'results/saved-baseline-controls.json', controls)
    assert read(ROOT / 'results/saved-baseline-controls.json') == controls
    check(checks, 'Original full-source control table preserved', 0)
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
    assert not list(ROOT.rglob('__pycache__'))
    import scipy
    write(ROOT / 'results/runtime.json', dict(python=sys.version, numpy=np.__version__, scipy=scipy.__version__, mpmath=mp.__version__,
        thread_environment={name: os.environ[name] for name in ['OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS']}))
    protected = BRANCH.parent.parent / 'formalization-workbench'
    started = datetime.fromisoformat(STARTED).timestamp()
    recent = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= started]
    check(checks, 'Protected workbench recent-mtime count', len(recent), 0, 'integrity')
    assert authenticate() == paths
    failed = [row for row in checks if not row['passed']]
    identity_failures = [row for row in failed if row['category'] == 'identity']
    history = read(ROOT / 'results/history-comparison.json')
    parent_status = read(PARENT / 'results/status.json')
    payload = dict(stage=183, state='diagnostic_complete', checks=checks, count=len(checks), passed_checks=len(checks) - len(failed),
        all_checks_passed=not failed, failed_checks=failed, identity_failures=identity_failures,
        completed_at_utc=datetime.now(timezone.utc).isoformat(),
        history_results=history, new_local_history_updates=updates, reused_unit_gas_events=36,
        new_real_response_events=0, new_real_integrator_calls=0, new_virtual_loop_integrations=0,
        original_source_packets_replaced=False, original_full_source_decisions_preserved=True,
        original_matched_moving_curvature_gate_passed=False, new_full_varying_temperature_source_evaluated=False,
        gas_only_fixed_anchor_scope=True, scattering_bank_changed=False, emission_bank_changed=False,
        temperature_curve_changed=False, tolerances_changed=False, global_history_replaced=False,
        inherited_stage182_failed_checks=parent_status['failed_checks'],
        inherited_stage181_failed_check_count=parent_status['inherited_stage181_failed_checks'],
        protected_workbench_recent_modified_file_count=len(recent), protected_recent_files=recent,
        protected_check_scope='Recent mtime since turn start, not a full-tree hash baseline',
        authenticated_parent_inputs=paths,
        input_hashes={str(path): saved.digest(path) for directory in ['histories', 'results']
            for path in sorted((ROOT / directory).rglob('*')) if path.is_file() and path.name not in ['status.json', 'stage-integrity.json']})
    write(ROOT / 'results/status.json', payload)
    write(ROOT / 'progress.json', dict(state='validation_complete'))
    print(json.dumps(dict(checks=len(checks), passed=payload['passed_checks'], failed=failed, updates=updates,
        inherited_stage182_failures=len(parent_status['failed_checks']))), flush=True)


def report():
    status = read(ROOT / 'results/status.json')
    histories = status['history_results']
    source_rows = read(ROOT / 'results/gas-response-comparison.json')
    controls = read(ROOT / 'results/saved-baseline-controls.json')
    lines = ['# Stage183: quarter-step local history with reused baseline/MTS gas kernels', '',
        'The next local time-step refinement passes the unchanged1% comparison.',
        'The sensitive width-difference changes shrink by about half, rather than',
        'disappearing. The difference is still dominated by temporal interpolation,',
        'not changed evolved values at common nodes. The old source curve is unchanged.', '',
        '## What ran and what was reused', '',
        '- Same primary native seeds5568/5569 and endpoint5630;244 quarter updates per history.',
        '- Same earlier seeds5552/5553;308 quarter updates per history for startup sensitivity.',
        '- Heavy and cold backgrounds both evolved:1104 new coupled updates total.',
        '- First-step BDF2 ratio1/4 checked on constant, linear and quadratic polynomials.',
        '- The saved native/half/earlier-half results were reused, not recomputed.',
        '- All36 cached gas-event kernels sum bitwise to the previous combined kernel.',
        '- Zero new real-response or virtual-loop integrations; fixed scattering/emission banks.',
        '- Same probes, widths0.01/0.005, linear interpolation,1% comparison and1e-10 identities.', '',
        '## Gas curvature and refinement', '',
        '|History|Half-step fine curvature|Quarter-step fine curvature|Change %|Half/quarter width-difference change %|Previous native/half width-difference change %|',
        '|---|---:|---:|---:|---:|---:|']
    for history in histories:
        fine, width = history['comparison'][1:]
        previous_relative = abs(width['previous_change'] / width['half'])
        lines.append(f"|{history['model']}|{fine['half']:.12g}|{fine['quarter']:.12g}|{100*fine['relative_change']:.10g}|{100*width['relative_change']:.10g}|{100*previous_relative:.10g}|")
    lines += ['', 'The current comparisons pass1%; the previous native/half failures remain',
        'recorded, not retroactively converted into passes. The widths themselves',
        'remain0.01 and0.005; only the evolution time step is refined.', '',
        '|History|Quarter width difference|Quarter width difference / fine curvature %|Ratio of successive refinement increments|Earlier-start sensitivity of width difference %|',
        '|---|---:|---:|---:|---:|']
    for history in histories:
        width = history['comparison'][2]
        lines.append(f"|{history['model']}|{width['quarter']:.12g}|{100*history['width_relative']['quarter']:.10g}|{width['absolute_increment_ratio']:.10g}|{100*width['startup_relative']:.10g}|")
    lines += ['', 'The increment ratios are about0.5, not the0.25 associated with clean',
        'second-order asymptotics. That is an observation about this sampled',
        'curvature diagnostic, not a demonstrated order reduction of the BDF solver.',
        'No Richardson extrapolation or certified remaining-error bound is claimed.', '',
        '## Evolution versus interpolation', '',
        'Quarter_full-half = (quarter_thinned_to_half-half)',
        '+ (quarter_full-quarter_thinned_to_half). Both pieces use the same evolved',
        'quarter history; only sampling changes. Native-grid thinning is also saved.', '',
        '|History|Quantity|Change on common half nodes|Change from finer interpolation|Total change|',
        '|---|---|---:|---:|---:|']
    for history in histories:
        for row in history['comparison']:
            lines.append(f"|{history['model']}|{row['quantity']}|{row['evolution_change_on_half_nodes']:.10g}|{row['interpolation_change']:.10g}|{row['change']:.10g}|")
    lines += ['', 'Interpolation dominates the observed difference. The much smaller common-node',
        'changes retain native floating-point and inherited startup errors; their',
        'smallness is not a universal integration-error certificate.', '',
        '## Baseline and MTS treated identically', '',
        'The exact cached-kernel reuse is U_component=K_component*C[g]. Baseline',
        '(control), matched MTS increment (remainder), and total all use the same',
        'two background histories and unchanged anchor at x=18.449187113596366.',
        'Their fractional gas-only changes agree by linearity; their source amplitudes',
        'are not identical. This is not three independent observational confirmations.', '',
        '|Component|Column|Fine-curvature response change %|Width-difference response change %|Pass1%|',
        '|---|---:|---:|---:|---|']
    for component in ['control', 'remainder', 'total']:
        for column in range(4):
            fine = next(row for row in source_rows if row['component'] == component and row['column'] == column and row['quantity'] == 'fine_curvature')
            width = next(row for row in source_rows if row['component'] == component and row['column'] == column and row['quantity'] == 'width_discrepancy')
            lines.append(f"|{component}|{column}|{100*fine['relative_change']:.10g}|{100*width['relative_change']:.10g}|{fine['passed'] and width['passed']}|")
    lines += ['', 'Columns0/1 use heavy gas,2/3 cold gas. Neither label means baseline versus',
        'MTS. Original photon profiles/tails and the complete varying-temperature',
        'microscopic source are not replaced by the isolated gas diagnostic.', '',
        '## Original source decision retained', '',
        '|Component|Moving-history curvature change %|Fixed-incident curvature change %|Moving passes /4|Fixed passes /4|',
        '|---|---:|---:|---:|---:|']
    for component in ['control', 'remainder', 'total']:
        moving = [row for row in controls if row['component'] == component and row['branch'] == 'moving_history']
        fixed = [row for row in controls if row['component'] == component and row['branch'] == 'fixed_incident']
        lines.append(f"|{component}|{100*max(row['relative'] for row in moving):.10g}|{100*max(row['relative'] for row in fixed):.10g}|{sum(row['passed'] for row in moving)}|{sum(row['passed'] for row in fixed)}|")
    lines += ['', 'The previous1.036596% matched moving-history curvature discrepancy is still',
        'its original full-source result. The current passing local step test is not',
        'a new evaluation of that gate.', '',
        '## Validation and next physical calculation', '',
        f"{status['passed_checks']}/{status['count']} current checks pass;{len(status['failed_checks'])} current failures.",
        f"{len(status['inherited_stage182_failed_checks'])} Stage182 failures and{status['inherited_stage181_failed_check_count']} Stage181 failures remain inherited, along with older flags.",
        'No numerical tolerance, coefficient, temperature curve or full-source decision',
        'was changed to obtain the current pass.', '',
        'Next: use the already saved one-sided scattering-bank slopes to calculate',
        'the gas-energy response on either side of the anchor knot. Predict the',
        'finite-width curvature/sampling contribution from those equations, then',
        'compare it with this three-grid ladder for both backgrounds and cached',
        'baseline/MTS kernels. Do not smooth the bank or fit away its corner first.',
        'This targets the observed near-halving of interpolation increments instead',
        'of blindly launching another time-step refinement.', '',
        '## Preservation', '',
        f"{len(status['authenticated_parent_inputs'])} immediate-parent and consumed paths rehashed before and after.",
        'Older archive inherited through seals, not rehashed in full.',
        f"Protected-workbench recent-mtime count:{status['protected_workbench_recent_modified_file_count']} (not a full-tree hash audit).",
        'One below-normal worker, library threads1, no subagents, downloads or GitHub.',
        'Earlier research and the Cosmology Lab handoff remain in place. Only this',
        'new child and additive resume heads are part of the continuation.', '']
    (ROOT / 'RESULTS.md').write_text('\n'.join(lines), encoding='utf-8')


def seal():
    status = read(ROOT / 'results/status.json')
    assert not status['identity_failures']
    assert status['protected_workbench_recent_modified_file_count'] == 0
    assert authenticate() == status['authenticated_parent_inputs']
    for filename, checksum in status['input_hashes'].items():
        assert saved.digest(filename) == checksum
    import psutil
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        if process.info['pid'] == os.getpid():
            continue
        command = ' '.join(process.info['cmdline'] or [])
        assert not ('python' in (process.info['name'] or '').lower() and 'quarter_step_stage183.py' in command)
    assert not list(ROOT.rglob('__pycache__'))
    parent = read(PARENT / 'results/stage-integrity.json')
    inherited = parent['inherited_sealed_payload_count'] + len(parent['file_hashes'])
    assert inherited == 336225
    destination = ROOT / 'results/stage-integrity.json'
    assert not destination.exists()
    carry_names = ['checkpoint_manifest_sha256', 'local_source_documents', 'primary_pdfs', 'source_urls',
        'observational_source_urls', 'original_library_sha256', 'native_library_sha256', 'physical_source_scope',
        'retained_local_approximation_histories', 'raw_subtraction_response_retained', 'raw_failed_history_response_retained']
    carried = {key: value for key, value in parent.items() if key in carry_names or key.startswith('latest_')}
    hashes = {path.relative_to(ROOT).as_posix(): saved.digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path != destination}
    largest = max(sum(path.is_file() for path in folder.iterdir()) for folder in [ROOT, *[path for path in ROOT.rglob('*') if path.is_dir()]])
    assert largest <= 500
    write(destination, dict(state='complete', stage=183,
        completion_qualification='Local half/quarter step and cached gas response comparisons; earlier source and precision flags retained',
        sealed_at_utc=datetime.now(timezone.utc).isoformat(), parent_seal_sha256=PARENT_SHA,
        inherited_sealed_payload_count=inherited, file_hashes=hashes, **carried,
        consumed_and_immediate_rehashed=status['authenticated_parent_inputs'],
        previous_primary_source_urls=parent.get('previous_primary_source_urls', []) + parent.get('new_primary_source_urls', []), new_primary_source_urls=[],
        prior_archive_full_rehash_performed=False, prior_archive_verification_seal_sha256=parent['prior_archive_verification_seal_sha256'],
        prior_payload_verification_scope='Immediate Stage182 plus consumed inputs rehashed; older archive inherited through seals',
        latest_local_quarter_step_gas_curvature=str(ROOT / 'RESULTS.md'), final_validation=str(ROOT / 'results/status.json'),
        accepted_current_scope_verified=True, accepted_scope='Quarter-step short history, sampling split and cached fixed-anchor gas response for baseline/MTS',
        validation_checks=status['count'], passed_validation_checks=status['passed_checks'], current_stage_retained_failures=len(status['failed_checks']),
        all_raw_and_legacy_checks_passed=False, retained_failed_checks=parent.get('retained_failed_checks', []) + status['failed_checks'],
        new_local_history_updates=1104, reused_unit_gas_events=36,
        new_real_response_events=0, new_real_integrator_calls=0, new_virtual_loop_integrations=0,
        incoming_frequency=18.449187113596366, full_population_source_temperature_law_certified=False,
        isolated_gas_channel=True, full_revised_source_history_evaluated=False,
        scattering_bank_changed=False, emission_bank_changed=False, source_curve_changed=False, temperature_curve_changed=False,
        original_source_packets_replaced=False, global_history_replaced=False, tolerances_changed=False,
        baseline_preserved=True, original_matched_moving_curvature_gate_passed=False, scientific_failure_inherited=True,
        bank_knot_causality_proved=False, global_numerical_error_bound=None,
        protected_workbench_recent_modified_file_count=0, protected_check_scope=status['protected_check_scope'],
        maximum_active_workers=1, active_workers_at_seal=0, library_threads_per_worker=1, largest_direct_file_count=largest,
        github_action=False, subagents=0, global_installation_changed=False, galaxy_work_modified=False,
        next_target='Use saved one-sided bank slopes and gas-energy equation to predict knot contribution to curvature and sampling; same baseline/MTS kernels and thresholds'))
    assert all(saved.digest(ROOT / name) == checksum for name, checksum in hashes.items())
    print(json.dumps(dict(sealed_files=len(hashes), cumulative_payloads=inherited + len(hashes), seal_sha256=saved.digest(destination))), flush=True)


if __name__ == '__main__':
    source.modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['validate', 'report', 'seal'])
    arguments = parser.parse_args()
    dict(validate=validate, report=report, seal=seal)[arguments.phase]()
