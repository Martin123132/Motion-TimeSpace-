from collision_stage185 import *


def validate():
    assert read(ROOT / 'progress.json')['state'] == 'response_complete'
    paths = authenticate()
    assert paths == read(ROOT / 'authenticated-inputs.json')
    config = read(ROOT / 'configuration.json')
    assert config['source_prediction_tolerance'] == .01 and config['identity_tolerance'] == 1e-10
    for filename, checksum in config['prior_bookmark_normalized_sha256'].items():
        assert hashlib.sha256(Path(filename).read_text(encoding='utf-8').encode()).hexdigest() == checksum
    for filename, checksum in read(ROOT / 'response-inputs.json').items():
        assert paths[filename] == checksum == saved.digest(filename)
    checks = sum([read(ROOT / 'results' / filename)['checks'] for filename in
        ['matrix-analysis.json', 'gas-projection.json', 'source-comparisons.json']], [])
    frozen = read(ROOT / 'results/frozen-tangent.json')
    assert frozen['tangent_sha256'] == saved.digest(ROOT / 'results/frozen-tangent.npz')
    frozen_time = datetime.fromisoformat(frozen['frozen_at_utc']).timestamp()
    wider = read(ROOT / 'results/wider-predictions.json')
    assert wider['original_tangent_sha256'] == frozen['tangent_sha256']
    assert wider['prediction_sha256'] == saved.digest(ROOT / 'results/wider-predictions.npz')
    for index, offset in enumerate(all_offsets()):
        folder = ROOT / 'targets' / f'target-{index}'
        status = read(folder / 'status.json')
        assert status['frozen_tangent_sha256'] == frozen['tangent_sha256']
        assert saved.digest(folder / 'matrices.npz') == status['matrix_sha256']
        required_freeze = frozen_time if index < 4 else datetime.fromisoformat(wider['frozen_at_utc']).timestamp()
        assert (folder / 'matrices.npz').stat().st_mtime >= required_freeze
        assert status['offset'] == offset
        with np.load(folder / 'matrices.npz') as packet:
            assert packet['block'].shape == packet['fixed_mask'].shape == packet['boundary'].shape == (96, 96)
            assert all(np.isfinite(packet[key]).all() for key in packet.files)
        check(checks, f'target-{index}: original quadrature evaluated after frozen prediction', 0)
    with np.load(ROOT / 'results/gas-responses.npz') as packet:
        with np.load(PARENT / 'results/gas-response.npz') as ancestor:
            assert np.array_equal(packet['kernels'], ancestor['kernels'])
        assert packet['response'].shape == (3, 6, 98, 4)
        assert np.isfinite(packet['response']).all()
    check(checks, 'Baseline/MTS kernels preserved bitwise', 0)
    negatives = read(ROOT / 'results/matrix-analysis.json')['negative_controls']
    assert len(negatives) == 16 and all(row['rejected'] for row in negatives)
    check(checks, 'Sixteen deliberately zero-derivative predictions correctly rejected', 0)
    initial = read(ROOT / 'results/initial-near-tests.json')
    final_matrix = read(ROOT / 'results/matrix-analysis.json')
    final_gas = read(ROOT / 'results/gas-projection.json')
    assert initial['matrix']['predictions'] == final_matrix['predictions'][:8]
    for model in range(2):
        assert initial['gas']['results'][model]['predictions'] == final_gas['results'][model]['predictions'][:4]
    check(checks, 'Original near-test predictions and decisions unchanged in wider test', 0)
    controls = read(PARENT / 'results/saved-baseline-controls.json')
    write(ROOT / 'results/saved-baseline-controls.json', controls)
    assert controls == read(ROOT / 'results/saved-baseline-controls.json')
    check(checks, 'Original full-source decisions retained', 0)
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
    assert not list(ROOT.rglob('__pycache__'))
    check(checks, 'New scripts compile and leave no bytecode', 0)
    import scipy
    write(ROOT / 'results/runtime.json', dict(python=sys.version, numpy=np.__version__, scipy=scipy.__version__, mpmath=mp.__version__,
        thread_environment={name: os.environ[name] for name in ['OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS']}))
    protected = BRANCH.parent.parent / 'formalization-workbench'
    began = datetime.fromisoformat(STARTED).timestamp()
    recent = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= began]
    check(checks, 'Protected workbench recent-mtime count', len(recent), 0, 'integrity')
    assert authenticate() == paths
    failed = [row for row in checks if not row['passed']]
    parent = read(PARENT / 'results/status.json')
    payload = dict(stage=185, state='diagnostic_complete', completed_at_utc=datetime.now(timezone.utc).isoformat(),
        checks=checks, count=len(checks), passed_checks=len(checks) - len(failed), failed_checks=failed,
        all_checks_passed=not failed, identity_failures=[row for row in failed if row['category'] == 'identity'],
        authenticated_inputs=paths, frozen_tangent_sha256=frozen['tangent_sha256'],
        new_collision_matrix_evaluations=9, combined_anchor_tangent_evaluations=1, independent_target_evaluations=8,
        reused_gas_events=36, new_microscopic_source_events=0, new_virtual_integrals=0,
        no_fitted_coefficients=True, numerical_domain_mask_explicit=True,
        original_bank_changed=False, emission_bank_changed=False, source_curve_changed=False,
        temperature_history_changed=False, tolerances_changed=False, full_source_gate_retested=False,
        inherited_stage184_failures=parent['failed_checks'], inherited_stage182_failures=parent['inherited_stage182_failed_checks'],
        inherited_stage181_failed_count=parent['inherited_stage181_failed_check_count'],
        protected_workbench_recent_modified_file_count=len(recent), protected_recent_files=recent,
        protected_check_scope='Recent mtime since turn start; not a full-tree hash baseline',
        result_hashes={str(path): saved.digest(path) for directory in ['results', 'targets'] for path in sorted((ROOT / directory).rglob('*'))
            if path.is_file() and path.name not in ['status.json', 'stage-integrity.json']})
    write(ROOT / 'results/status.json', payload)
    write(ROOT / 'progress.json', dict(state='validation_complete'))
    print(json.dumps(dict(checks=len(checks), passed=payload['passed_checks'], failed=failed,
        input_paths=len(paths), protected_recent_count=len(recent))), flush=True)


def report():
    status = read(ROOT / 'results/status.json')
    matrices = read(ROOT / 'results/matrix-analysis.json')
    gas = read(ROOT / 'results/gas-projection.json')['results']
    responses = read(ROOT / 'results/source-comparisons.json')['rows']
    live = [row for row in matrices['predictions'] if row['kind'] == 'block']
    wide = [row for row in live if abs(row['offset']) >= .005]
    derivative = [row for row in matrices['derivatives'] if row['kind'] == 'block']
    near_derivative = [row for row in derivative if row['step'] <= .001]
    full_response_error = max(row['relative_error'] for row in responses if row['kind'] == 'block')
    lines = ['# Stage185: a temperature derivative from the actual collision integral', '',
        '## Outcome', '',
        'The operator tangent is derived analytically from thermal weights, Doppler',
        'shifts, recoil, stimulated scattering and the spectral basis. It is not',
        'a derivative of the bank interpolation. The physical bank remains unchanged.', '',
        f"The nearby centered derivative tests agree to within {100*max(row['derivative_error'] for row in near_derivative):.8g}% in full matrix norm.",
        f"Across the actual original curvature offsets +/-0.005 and +/-0.01, the frozen first-order prediction's worst small-change error is {100*max(row['prediction_relative_error'] for row in wide):.8g}%.",
        f"The corresponding frozen gas-channel predictions have worst error {100*full_response_error:.8g}% for baseline, MTS increment and total.",
        'These numbers concern the retained discrete collision calculation, not a',
        'new fit to astronomical observations or an error certificate for the continuum.', '',
        '## What is derived', '',
        'Let t=ln(theta/theta0), with dimensionless incoming x and the original',
        '96-mode basis fixed. For each event let a be its positive pair conductance,',
        'v=psi(x)-psi(x_out) and m its retained-domain membership. Then', '',
        '    B_t=-1/2 sum m [a_t v v^T+a(v_t v^T+v v_t^T)].', '',
        'The Maxwell-Juttner radial weights are differentiated including their',
        'normalization. Both Lorentz Doppler factors, recoil, Bose stimulation and',
        'outgoing basis values are differentiated. The original boost implementation',
        'independently checks the analytic event geometry. The analytic anchor',
        'construction reproduces the saved bank matrix within1e-10; the same gate',
        'checks symmetry and photon-number nullity. The derivative itself is not',
        'required to be negative: each finite-temperature collision matrix is.', '',
        '`DERIVATION.md` contains the formulas, energy projection and domain boundary',
        'qualification. d/dtheta=B_t/theta; along the saved expansion B_u=-B_t.',
        'No coefficient is fitted to these derivative or curvature results.', '',
        '## Predictions frozen before their target evaluations', '',
        '|Log-temperature offset|Relative temperature change %|Matrix small-change error %|Heavy gas error %|Cold gas error %|Matrix and gas pass1%|',
        '|---:|---:|---:|---:|---:|---|']
    for row in live:
        offset = row['offset']
        matches = [next(value for value in model['predictions'] if value['offset'] == offset)['values']['block'] for model in gas]
        passed = row['passed'] and all(value['passed'] for value in matches)
        lines.append(f"|{offset:+g}|{100*np.expm1(offset):.8g}|{100*row['prediction_relative_error']:.8g}|{100*matches[0]['relative_error']:.8g}|{100*matches[1]['relative_error']:.8g}|{passed}|")
    lines += ['', 'Errors are divided by the SMALL change from the anchor, not by the',
        'large full matrix. The deliberately zero-temperature-derivative prediction',
        'fails every negative control. The narrow test was specified first. After',
        'its success, the wider extension was frozen with the SAME tangent before',
        'evaluating the actual original curvature probes. The whole exercise is not',
        'described as pre-registered or as an observational holdout.', '',
        '|Log half-width|Live centered derivative error %|Fixed-mask derivative error %|Nearby one-sided derivative difference %|',
        '|---:|---:|---:|---:|']
    for row in derivative:
        fixed = next(value for value in matrices['derivatives'] if value['step'] == row['step'] and value['kind'] == 'fixed_mask')
        lines.append(f"|{row['step']:g}|{100*row['derivative_error']:.8g}|{100*fixed['derivative_error']:.8g}|{100*row['one_sided_gap']:.8g}|")
    lines += ['', '## What the old secants get wrong', '',
        '|Old bank side|Full-matrix derivative error %|Heavy gas-projected error %|Cold gas-projected error %|',
        '|---|---:|---:|---:|']
    for row in matrices['old_secants']:
        label = row['side']
        lines.append(f"|{label}|{100*row['relative_error']:.8g}|{100*gas[0]['old_relative_errors'][label]:.8g}|{100*gas[1]['old_relative_errors'][label]:.8g}|")
    lines += ['', 'Both full-matrix secant errors exceed the unchanged1% gate and remain',
        'recorded failures. Their energy projections are much closer. This explains',
        'how an otherwise accurate background bank can acquire a small artificial',
        'slope corner that is amplified by a narrow finite-width curvature stencil.',
        'Do not interpret the full-matrix errors as equally large gas or observation errors.', '',
        '## Hard-domain boundary check', '',
        'The analytic tangent holds inside a fixed membership cell of the retained',
        'quadrature. Some events cross x_out=1e-5 or60 at the test temperatures.',
        'Their exact signed matrix contribution is evaluated and saved separately.', '',
        '|Offset|Crossing events|Discarded conductance fraction|Boundary matrix / small-change norm|',
        '|---:|---:|---:|---:|']
    for row in matrices['target_metadata']:
        lines.append(f"|{row['offset']:+g}|{row['crossings']}|{row['discarded_weight_fraction']:.8g}|{row['boundary_over_small_change_norm']:.8g}|")
    lines += ['', 'The live-domain and frozen-domain tests are both retained. Discrete mask',
        'crossings can dominate the extremely small residual of a centered derivative',
        'as its step shrinks; a smaller finite-difference step is not automatically',
        'more accurate. None of this proves the continuum boundary integral vanishes.',
        'No cutoff, domain, quadrature order or bank entry is changed here.', '',
        '## Identical baseline/MTS treatment', '',
        'At the saved anchor, C=chi-e M^-1 S T and q=p-TG. The collision-only',
        'contribution to the slaved gas u-slope is L(B_t)=r e M^-1 B_t q/C.',
        'Rate evolution, emission and photon-history derivatives are separate terms.', '',
        '|History|Derived collision-only gas slope|Cool old secant|Warm old secant|',
        '|---|---:|---:|---:|']
    for row in gas:
        lines.append(f"|{row['model']}|{float(row['physical_collision_gas_slope']):.12g}|{float(row['cool_secant']):.12g}|{float(row['warm_secant']):.12g}|")
    lines += ['', 'The difference between the two old projections reproduces Stage184\'s',
        'slope jump at the unchanged1e-10 identity gate. Each of the36 saved gas-event',
        'kernels is reused; their sum is bitwise identical. Baseline/control, matched',
        'MTS increment/remainder and total use the same gas scalars and unchanged',
        'mass-dual source norm, but retain distinct absolute response amplitudes.', '',
        '|Component|History|Derived collision-tangent source norm|',
        '|---|---|---:|']
    for component in ['control', 'remainder', 'total']:
        for column in [0, 2]:
            row = next(value for value in responses if value['component'] == component and value['column'] == column)
            lines.append(f"|{component}|{row['model']}|{row['physical_tangent_response_norm']:.12g}|")
    lines += ['', 'Columns0/1 are heavy and2/3 cold histories, not baseline/MTS identifiers.',
        'Equal fractional gas-channel errors are a linearity consequence, not repeated',
        'independent empirical evidence. No source spectrum or gas history is replaced.',
        'The complete varying-temperature source curvature gate remains its saved',
        'decision; this local collision tangent does not retest it.', '',
        '## Validation and preservation', '',
        f"{status['passed_checks']}/{status['count']} checks pass; {len(status['failed_checks'])} failures remain recorded.",
        'All earlier scientific failures remain inherited. Numerical identity gates',
        'stay1e-10 and comparison gates stay1%. No acceptance threshold was loosened.',
        f"{len(status['authenticated_inputs'])} immediate-parent and consumed paths were rehashed before and after.",
        'Older archive contents are inherited through seals, not rehashed in full.',
        'The protected-workbench recent-mtime count is0, not a full-tree hash claim.',
        'Nine collision matrices were evaluated: one combined anchor/tangent pass',
        'and eight independent targets. The original700-node/order6 rule is reused.',
        'No new radiative source events, virtual-loop integrals, subagents or GitHub.',
        'A premature analysis startup safely failed before writing results while a',
        'target was unfinished; analysis was rerun only after all targets completed.',
        'Numerical work uses below-normal single-thread workers; physical target',
        'integrations are sequential. At most two owned processes briefly overlapped',
        'during that failed analysis startup. No unrelated processes were stopped.', '',
        '## Files and next derivation', '',
        '- `results/frozen-tangent.npz` and `results/anchor-events.npz`: analytic derivative and thermal geometry.',
        '- `results/wider-predictions.json`: frozen follow-on protocol and original tangent hash.',
        '- `results/initial-near-tests.json`: original narrow results preserved verbatim.',
        '- `targets/target-0/status.json` through `targets/target-7/status.json`: independent quadrature outputs, hashes and boundary counts.',
        '- `results/matrix-analysis.json`: operator tests and the two failed old secants.',
        '- `results/gas-projection.json` and `results/source-comparisons.json`: heavy/cold and baseline/MTS tests.',
        '- `results/saved-baseline-controls.json`: original full-source decisions, unchanged.',
        '- `authenticated-inputs.json`: exact inherited source paths and hashes.',
        '- `results/status.json` and `results/stage-integrity.json`: validation and seal.', '',
        'Next: derive the SECOND temperature derivative from the same collision',
        'integrand, and test its curvature against these saved temperature evaluations.',
        'That retains genuine physical curvature when constructing a separate smooth',
        'candidate operator; a first-order Taylor approximation alone is not enough',
        'to settle a curvature discrepancy. Keep the live bank and original histories',
        'unchanged until the candidate passes the same baseline/MTS tests.', '']
    (ROOT / 'RESULTS.md').write_text('\n'.join(lines), encoding='utf-8')


def seal():
    status = read(ROOT / 'results/status.json')
    assert not status['identity_failures'] and status['protected_workbench_recent_modified_file_count'] == 0
    assert authenticate() == status['authenticated_inputs']
    assert (ROOT / 'RESULTS.md').exists() and (ROOT / 'RUN-NOTES.md').exists()
    for filename, checksum in status['result_hashes'].items():
        assert saved.digest(filename) == checksum
    import psutil
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        if process.info['pid'] == os.getpid():
            continue
        command = ' '.join(process.info['cmdline'] or [])
        assert not ('python' in (process.info['name'] or '').lower() and any(name in command for name in
            ['collision_stage185', 'analyse_stage185', 'finish_stage185']))
    parent = read(PARENT / 'results/stage-integrity.json')
    inherited = parent['inherited_sealed_payload_count'] + len(parent['file_hashes'])
    assert inherited == 336293
    destination = ROOT / 'results/stage-integrity.json'
    assert not destination.exists()
    carry_names = ['checkpoint_manifest_sha256', 'local_source_documents', 'primary_pdfs', 'source_urls',
        'observational_source_urls', 'original_library_sha256', 'native_library_sha256', 'physical_source_scope',
        'retained_local_approximation_histories', 'raw_subtraction_response_retained', 'raw_failed_history_response_retained']
    carried = {key: value for key, value in parent.items() if key in carry_names or key.startswith('latest_')}
    hashes = {path.relative_to(ROOT).as_posix(): saved.digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path != destination}
    largest = max(sum(path.is_file() for path in folder.iterdir()) for folder in [ROOT, *[path for path in ROOT.rglob('*') if path.is_dir()]])
    assert largest <= 500 and not list(ROOT.rglob('__pycache__'))
    write(destination, dict(state='complete', stage=185, sealed_at_utc=datetime.now(timezone.utc).isoformat(),
        parent_seal_sha256=PARENT_SHA, inherited_sealed_payload_count=inherited, file_hashes=hashes, **carried,
        consumed_and_immediate_rehashed=status['authenticated_inputs'],
        previous_primary_source_urls=parent.get('previous_primary_source_urls', []) + parent.get('new_primary_source_urls', []), new_primary_source_urls=[],
        prior_archive_full_rehash_performed=False, prior_archive_verification_seal_sha256=parent['prior_archive_verification_seal_sha256'],
        prior_payload_verification_scope='Immediate Stage184 and consumed paths rehashed; older archive inherited through seals',
        latest_collision_temperature_derivative=str(ROOT / 'RESULTS.md'), final_validation=str(ROOT / 'results/status.json'),
        completion_qualification='Analytic physical quadrature tangent and nearby-temperature tests with unchanged bank and explicit mask boundaries',
        validation_checks=status['count'], passed_validation_checks=status['passed_checks'], current_stage_retained_failures=len(status['failed_checks']),
        all_raw_and_legacy_checks_passed=False, retained_failed_checks=parent.get('retained_failed_checks', []) + status['failed_checks'],
        physical_derivative_scope='Finite scalar order6 thermal quadrature, fixed incoming x, 96-mode basis and original domain',
        original_bank_changed=False, emission_bank_changed=False, source_curve_changed=False, temperature_history_changed=False,
        tolerances_changed=False, no_fitted_coefficients=True, full_source_gate_retested=False,
        new_collision_matrix_evaluations=9, combined_anchor_tangent_evaluations=1, independent_target_evaluations=8,
        reused_gas_events=36, new_microscopic_source_events=0, new_virtual_integrals=0,
        boundary_contribution_explicit=True, global_continuum_derivative_bound=None,
        protected_workbench_recent_modified_file_count=0, protected_check_scope=status['protected_check_scope'],
        maximum_active_workers=2, physical_integrations_concurrent=1, active_workers_at_seal=0, library_threads_per_worker=1, largest_direct_file_count=largest,
        github_action=False, subagents=0, global_installation_changed=False, galaxy_work_modified=False,
        next_target=read(ROOT / 'results/next-target.json')['next_target']))
    assert all(saved.digest(ROOT / name) == checksum for name, checksum in hashes.items())
    print(json.dumps(dict(sealed_files=len(hashes), cumulative_payloads=inherited + len(hashes), seal_sha256=saved.digest(destination))), flush=True)


if __name__ == '__main__':
    source.modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['validate', 'report', 'seal'])
    arguments = parser.parse_args()
    dict(validate=validate, report=report, seal=seal)[arguments.phase]()
