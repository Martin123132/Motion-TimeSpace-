from run233 import *


def validate():
    modest()
    config, frozen = run_protocol()
    checks, inputs = [], read(ROOT / 'inputs.json')
    report_paths = [ROOT / 'results' / name for name in ('scalar-replay.json', 'controls.json', 'polarization.json', 'tail-boost.json', 'medium-derivative.json', 'components.json')]
    report_paths += [ROOT / 'runs' / label / 'status.json' for label in ('warm', 'middle', 'cold')]
    reports = [read(path) for path in report_paths]
    for report in reports:
        assert report['state'] == 'complete' and not report['failed']
        checks.extend(report['checks'])
    for label in ('warm', 'middle', 'cold'):
        report = read(ROOT / 'runs' / label / 'status.json')
        assert report['events'] == 19 and report['new_virtual_integrals'] == 0
        assert digest(ROOT / 'runs' / label / 'vertices.npz') == report['vertices_sha256']
    for prefix, filename in [('controls', 'controls233.py'), ('polarization', 'polarization233.py'), ('tail-boost', 'tail_boost233.py'), ('medium', 'medium233.py'), ('components', 'component_checks233.py')]:
        local = read(ROOT / (prefix + '-configuration.json'))
        assert digest(ROOT / filename) == local['script_sha256']
    assert digest(ROOT / 'MEDIUM-DERIVATIVE.md') == read(ROOT / 'medium-configuration.json')['derivation_sha256']
    for name in ('thermal_radial.py', 'thermal_dressed.py', 'DERIVATION.md'):
        register(inputs, BRANCH / 'thermal-ward-kernel-20261008' / name)
    modules(inputs)
    for name, expected in inputs.items():
        assert digest(name) == expected, name
    for name, expected in config['bookmarks'].items():
        assert digest(name) == expected, name
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
    assert not list(ROOT.rglob('__pycache__')) and not list(ROOT.rglob('*.partial'))
    protected = BRANCH.parent.parent / 'formalization-workbench'
    since = datetime.fromisoformat(START).timestamp()
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    assert not changed, changed
    check(checks, 'consumed sources unchanged', 0, 0)
    check(checks, 'protected workbench recent-mtime count', len(changed), 0)
    records = [entry for label in ('warm', 'middle', 'cold') for entry in read(ROOT / 'runs' / label / 'status.json')['records']]
    summary = dict(stage=233, state='complete', qualified=True, finished_at=now(), checks=checks, failed=[],
        total_checks=len(checks), anchors=3, event_geometries=57, saved_history_states=6, infrared_joins=2,
        full_input_columns=99, output_rows=98, multipoles=[0, 1, 2],
        maximum_scalar_replay=reports[0]['maximum_relative_error'],
        maximum_mixed_test_direction_fraction=max(row['mixed_fraction_in_test_direction'] for row in records),
        maximum_nonlinear_remainder_over_mixed=max(row['nonlinear_remainder_over_mixed'] for row in records),
        maximum_common_boost_norm=max(row['non_equilibrium_common_boost_norm'] for row in records),
        maximum_physical_gas_shift=max(abs(row['physical_gas_shift']) for row in records),
        maximum_photon_potential=max(row['maximum_photon_potential'] for row in records),
        maximum_direct_coefficient_error=reports[5]['maxima'],
        minimum_incorrect_T2_error=min(row['blanket_T2_relative_error'] for row in reports[4]['records']),
        maximum_polarized_I_Q=max(abs(row['intensity_from_Q']) for row in reports[2]['records']),
        maximum_boost_derivative_error=max(row['boost_derivative_error'] for row in reports[3]['records']),
        vertex_worker_seconds=sum(read(ROOT / 'runs' / label / 'status.json')['elapsed_seconds'] for label in ('warm', 'middle', 'cold')),
        directly_consumed_files_rehashed=len(inputs), protected_recent_mtime_count=0,
        original_bank_changed=False, original_tolerances_changed=False, new_loop_amplitudes=0,
        scope='Implemented exact and mixed statistical angular vertex on saved histories, independent four-force and polarized Born connection; derived medium functional, not yet inclusive mixed integration',
        inclusive_mixed_source_qualified=False, new_empirical_fit=False,
        report_hashes={str(path.relative_to(ROOT)): digest(path) for path in report_paths})
    assert not (ROOT / 'results/completion.json').exists()
    write(ROOT / 'results/inputs-final.json', inputs)
    write(ROOT / 'results/completion.json', summary)
    print(json.dumps({name: value for name, value in summary.items() if name not in ('checks', 'report_hashes')}), flush=True)


def seal():
    completion = read(ROOT / 'results/completion.json')
    assert completion['qualified']
    for name, expected in read(ROOT / 'results/inputs-final.json').items():
        assert digest(name) == expected, name
    for name, expected in completion['report_hashes'].items():
        assert digest(ROOT / name) == expected, name
    for name in ('RESULTS.md', 'NEXT.md', 'RUN-NOTES.md'):
        assert (ROOT / name).exists()
    bookmarks = [BRANCH / 'RESUME-CURRENT.md', BRANCH.parent / 'CURRENT_LOCAL_RESUME.md']
    assert all(path.read_text(encoding='utf-8').startswith('# Stage233 SAVED') for path in bookmarks)
    target = ROOT / 'results/stage-integrity.json'
    assert not target.exists()
    paths = {str(path.relative_to(ROOT)): digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file()}
    write(target, dict(stage=233, state='complete', qualified=True, sealed_at=now(), file_hashes=paths,
        directly_consumed_inputs=read(ROOT / 'results/inputs-final.json'), bookmarks={str(path): digest(path) for path in bookmarks},
        scope=completion['scope'], inclusive_mixed_source_qualified=False))
    print(json.dumps(dict(seal_sha256=digest(target), files=len(paths), checks=completion['total_checks'])), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['validate', 'seal'])
    arguments = parser.parse_args()
    validate() if arguments.mode == 'validate' else seal()
