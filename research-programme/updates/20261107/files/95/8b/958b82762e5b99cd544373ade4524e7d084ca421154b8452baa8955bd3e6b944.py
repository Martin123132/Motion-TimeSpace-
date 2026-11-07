from corner_stage184 import *


def derivative_checks():
    ladder = native.infrared_ladder.InfraredLadder(native.BACKGROUND / 'banks/infrared96-q700')
    checks, records = [], []
    for model in MODELS:
        operator = Operators(model, ladder)
        for probe, coordinate in enumerate(history(model, 'quarter')['coordinates'][1:], 1):
            exact = operator.derivatives(float(coordinate))
            for step in [1e-4, 5e-5]:
                before = operator.at(float(coordinate - step))[0]
                after = operator.at(float(coordinate + step))[0]
                middle = operator.at(float(coordinate))[0]
                differences = [(after - before) / (2 * step), (after - 2 * middle + before) / step**2]
                for order, numerical in enumerate(differences, 1):
                    error = float(np.linalg.norm(numerical - exact[order]) / np.linalg.norm(exact[order]))
                    check(checks, f'{model}:{probe}:{step}: analytic operator derivative {order}', error, .01, 'derivative')
                    records.append(dict(model=model, probe=probe, step=step, order=order, relative_error=error))
        current, reference, delta = operator.at(operator.anchor)
        check(checks, model + ': bank/diagnostic continuity at anchor', np.linalg.norm(delta))
        check(checks, model + ': reference equals original at anchor', np.linalg.norm(reference - current))
    with mp.workdps(80):
        width = mp.mpf('.01')
        slope = mp.mpf('-.000066')
        def stencil(values):
            return (values[1] - 2 * values[0] + values[2]) / width**2 - (values[3] - 2 * values[0] + values[4]) / (width / 2)**2
        coordinates = [0, -width, width, -width / 2, width / 2]
        hinge = [slope * max(value, 0) for value in coordinates]
        quadratic = [max(value, 0)**2 for value in coordinates]
        check(checks, 'exact hinge width law', (stencil(hinge) + slope / width) / (slope / width))
        check(checks, 'one-sided quadratic cancels between widths', stencil(quadratic))
    write(ROOT / 'results/derivative-checks.json', dict(checks=checks, records=records,
        scope='Original operator evaluated within each smooth segment; centered finite differences, not fitted coefficients'))
    print(json.dumps(dict(checks=len(checks), maximum_derivative_error=max(row['relative_error'] for row in records),
        failed=[row for row in checks if not row['passed']])), flush=True)


def validate():
    assert read(ROOT / 'progress.json')['state'] == 'response_complete'
    paths = authenticate()
    assert paths == read(ROOT / 'authenticated-inputs.json')
    checks = sum([read(ROOT / 'results' / name)['checks'] for name in
        ['analysis-checks.json', 'response-checks.json', 'derivative-checks.json']], [])
    config = read(ROOT / 'configuration.json')
    assert config['source_prediction_tolerance'] == .01 and config['identity_tolerance'] == 1e-10
    for filename, checksum in config['prior_bookmark_normalized_sha256'].items():
        assert hashlib.sha256(Path(filename).read_text(encoding='utf-8').encode()).hexdigest() == checksum
    for ledger in ['bank-inputs.json', 'response-inputs.json']:
        for filename, checksum in read(ROOT / ledger).items():
            assert paths[filename] == checksum == saved.digest(filename)
    check(checks, 'All consumed scattering, emission and response hashes unchanged', 0)
    frozen_hash = saved.digest(ROOT / 'results/frozen-predictions.json')
    updates = 0
    for model in MODELS:
        for grid in GRIDS:
            folder = ROOT / 'counterfactuals' / model / grid
            status = read(folder / 'status.json')
            assert status['frozen_prediction_sha256'] == frozen_hash
            updates += status['updates']
            with np.load(folder / 'history.npz') as packet:
                original = history(model, grid)
                assert np.array_equal(packet['expansion'], original['expansion'])
                assert packet['reference_profiles'].shape == packet['forced_profiles'].shape == (status['updates'] + 1, 96)
                assert np.array_equal(packet['reference_profiles'][0], original['initial_profile'])
                assert float(packet['reference_gas'][0]) == float(original['initial_gas'])
                assert not np.any(packet['forced_profiles'][0]) and packet['forced_gas'][0] == 0
                assert all(np.isfinite(packet[key]).all() for key in packet.files)
                check(checks, f'{model}:{grid}: finite saved counterfactuals and matching restart', 0)
    assert updates == 854
    with np.load(ROOT / 'results/gas-response.npz') as packet:
        assert packet['responses'].shape == (3, 5, 6, 98, 4)
        assert np.isfinite(packet['responses']).all()
        with np.load(PARENT / 'results/gas-response.npz') as original:
            assert np.array_equal(packet['kernels'], original['kernels'])
    check(checks, 'Every baseline/MTS gas kernel remains bitwise unchanged', 0)
    controls = read(PARENT / 'results/saved-baseline-controls.json')
    write(ROOT / 'results/saved-baseline-controls.json', controls)
    assert read(ROOT / 'results/saved-baseline-controls.json') == controls
    check(checks, 'Full varying-temperature source decisions preserved separately', 0)
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
    assert not list(ROOT.rglob('__pycache__'))
    check(checks, 'All new scripts compile without bytecode residue', 0)
    import scipy
    write(ROOT / 'results/runtime.json', dict(python=sys.version, numpy=np.__version__, scipy=scipy.__version__, mpmath=mp.__version__,
        thread_environment={name: os.environ[name] for name in ['OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS']}))
    protected = BRANCH.parent.parent / 'formalization-workbench'
    started = datetime.fromisoformat(STARTED).timestamp()
    recent = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= started]
    check(checks, 'Protected workbench recent-mtime count', len(recent), 0, 'integrity')
    assert authenticate() == paths
    failed = [row for row in checks if not row['passed']]
    parent_status = read(PARENT / 'results/status.json')
    payload = dict(stage=184, state='diagnostic_complete', checks=checks, count=len(checks), passed_checks=len(checks) - len(failed),
        all_checks_passed=not failed, failed_checks=failed, identity_failures=[row for row in failed if row['category'] == 'identity'],
        completed_at_utc=datetime.now(timezone.utc).isoformat(),
        new_reference_updates=updates, new_forced_difference_updates=updates, shared_timepoints_and_three_rhs_solves=updates,
        reused_unit_gas_events=36, new_real_response_events=0, new_real_integrator_calls=0, new_virtual_loop_integrations=0,
        new_fitted_coefficients=0, exact_corner_energy_jump_verified=True, finite_heat_capacity_gas_is_C1=True,
        slaved_corner_prediction_scope='Fixed anchor, two histories, unchanged widths; retrospective diagnostic',
        original_source_packets_replaced=False, original_full_source_decisions_preserved=True,
        original_matched_moving_curvature_gate_passed=False, new_full_varying_temperature_source_evaluated=False,
        gas_only_fixed_anchor_scope=True, scattering_bank_changed=False, emission_bank_changed=False,
        temperature_curve_changed=False, tolerances_changed=False, global_history_replaced=False,
        inherited_stage183_failed_checks=parent_status['failed_checks'],
        inherited_stage182_failed_checks=parent_status['inherited_stage182_failed_checks'],
        inherited_stage181_failed_check_count=parent_status['inherited_stage181_failed_check_count'],
        protected_workbench_recent_modified_file_count=len(recent), protected_recent_files=recent,
        protected_check_scope='Recent mtime since turn start, not a full-tree hash baseline',
        authenticated_parent_inputs=paths, frozen_prediction_sha256=frozen_hash,
        input_hashes={str(path): saved.digest(path) for directory in ['counterfactuals', 'results']
            for path in sorted((ROOT / directory).rglob('*')) if path.is_file() and path.name not in ['status.json', 'stage-integrity.json']})
    write(ROOT / 'results/status.json', payload)
    write(ROOT / 'progress.json', dict(state='validation_complete', frozen_prediction_sha256=frozen_hash))
    print(json.dumps(dict(checks=len(checks), passed=payload['passed_checks'], failed=failed,
        authenticated_inputs=len(paths), updates=updates, protected_count=len(recent))), flush=True)


def seal():
    status = read(ROOT / 'results/status.json')
    assert not status['identity_failures']
    assert status['protected_workbench_recent_modified_file_count'] == 0
    assert authenticate() == status['authenticated_parent_inputs']
    assert (ROOT / 'RESULTS.md').is_file() and (ROOT / 'RUN-NOTES.md').is_file()
    for filename, checksum in status['input_hashes'].items():
        assert saved.digest(filename) == checksum
    import psutil
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        if process.info['pid'] == os.getpid():
            continue
        command = ' '.join(process.info['cmdline'] or [])
        assert not ('python' in (process.info['name'] or '').lower() and any(name in command for name in
            ['corner_stage184.py', 'analyse_stage184.py', 'finish_stage184.py', 'probe_stage184.py']))
    assert not list(ROOT.rglob('__pycache__'))
    parent = read(PARENT / 'results/stage-integrity.json')
    inherited = parent['inherited_sealed_payload_count'] + len(parent['file_hashes'])
    assert inherited == 336254
    destination = ROOT / 'results/stage-integrity.json'
    assert not destination.exists()
    carry_names = ['checkpoint_manifest_sha256', 'local_source_documents', 'primary_pdfs', 'source_urls',
        'observational_source_urls', 'original_library_sha256', 'native_library_sha256', 'physical_source_scope',
        'retained_local_approximation_histories', 'raw_subtraction_response_retained', 'raw_failed_history_response_retained']
    carried = {key: value for key, value in parent.items() if key in carry_names or key.startswith('latest_')}
    hashes = {path.relative_to(ROOT).as_posix(): saved.digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path != destination}
    largest = max(sum(path.is_file() for path in folder.iterdir()) for folder in [ROOT, *[path for path in ROOT.rglob('*') if path.is_dir()]])
    assert largest <= 500
    write(destination, dict(state='complete', stage=184,
        completion_qualification='Derived local bank-corner forcing and sampling attribution; coarse raw prediction failures retained',
        sealed_at_utc=datetime.now(timezone.utc).isoformat(), parent_seal_sha256=PARENT_SHA,
        inherited_sealed_payload_count=inherited, file_hashes=hashes, **carried,
        consumed_and_immediate_rehashed=status['authenticated_parent_inputs'],
        previous_primary_source_urls=parent.get('previous_primary_source_urls', []) + parent.get('new_primary_source_urls', []), new_primary_source_urls=[],
        prior_archive_full_rehash_performed=False, prior_archive_verification_seal_sha256=parent['prior_archive_verification_seal_sha256'],
        prior_payload_verification_scope='Immediate Stage183 plus consumed inputs rehashed; older archive inherited through seals',
        latest_bank_knot_gas_curvature=str(ROOT / 'RESULTS.md'), final_validation=str(ROOT / 'results/status.json'),
        accepted_current_scope_verified=True, accepted_scope='Equation-derived and counterfactually tested bank-corner contribution, fixed-anchor gas channel',
        validation_checks=status['count'], passed_validation_checks=status['passed_checks'], current_stage_retained_failures=len(status['failed_checks']),
        all_raw_and_legacy_checks_passed=False, retained_failed_checks=parent.get('retained_failed_checks', []) + status['failed_checks'],
        new_reference_updates=854, new_forced_difference_updates=854, shared_timepoints_and_three_rhs_solves=854, reused_unit_gas_events=36,
        new_real_response_events=0, new_real_integrator_calls=0, new_virtual_loop_integrations=0,
        incoming_frequency=18.449187113596366, full_population_source_temperature_law_certified=False,
        isolated_gas_channel=True, full_revised_source_history_evaluated=False,
        scattering_bank_changed=False, emission_bank_changed=False, source_curve_changed=False, temperature_curve_changed=False,
        original_source_packets_replaced=False, global_history_replaced=False, tolerances_changed=False,
        baseline_preserved=True, original_matched_moving_curvature_gate_passed=False, scientific_failure_inherited=True,
        bank_knot_local_forcing_identity_verified=True, bank_knot_full_source_discrepancy_explained=False,
        global_numerical_error_bound=None, protected_workbench_recent_modified_file_count=0,
        protected_check_scope=status['protected_check_scope'], maximum_active_workers=1, active_workers_at_seal=0,
        library_threads_per_worker=1, largest_direct_file_count=largest,
        github_action=False, subagents=0, global_installation_changed=False, galaxy_work_modified=False,
        next_target='Differentiate or independently evaluate the physical collision operator near the knot to test the bank secants before any smoothing; preserve baseline/MTS comparisons and thresholds'))
    assert all(saved.digest(ROOT / name) == checksum for name, checksum in hashes.items())
    print(json.dumps(dict(sealed_files=len(hashes), cumulative_payloads=inherited + len(hashes), seal_sha256=saved.digest(destination))), flush=True)


if __name__ == '__main__':
    source.modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['derivatives', 'validate', 'seal'])
    arguments = parser.parse_args()
    dict(derivatives=derivative_checks, validate=validate, seal=seal)[arguments.phase]()
