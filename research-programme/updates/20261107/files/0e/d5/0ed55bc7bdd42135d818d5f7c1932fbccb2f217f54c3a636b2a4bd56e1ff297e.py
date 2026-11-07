from common235 import *
import state235
import argparse


def combine():
    modest()
    config, unused = state235.state_protocol()
    target = ROOT / 'results/combined.json'
    assert not target.exists()
    virtual = packet(PARENT / 'results/virtual-mixed-blocks.npz')
    checks, records, output = [], [], {}
    for row in config['events']:
        state = packet(ROOT / 'runs' / row['label'] / 'state.npz')
        assert read(ROOT / 'runs' / row['label'] / 'state.json')['qualified']
        for join in config['joins']:
            for state_index, history in enumerate(config['states']):
                for degree in config['multipoles']:
                    prefix = f'{row["label"]}:join{join}:{history["model"]}:{history["history"]}:l{degree}'
                    coarse_state = state[f'join{join}:state{state_index}:l{degree}:step0.001:total']
                    fine_state = state[f'join{join}:state{state_index}:l{degree}:step0.0005:total']
                    coarse = virtual[prefix + ':order4:total'] + coarse_state
                    fine = virtual[prefix + ':order6:total'] + fine_state
                    output[prefix + ':coarse'] = coarse
                    output[prefix + ':fine'] = fine
                    error = relative(coarse, fine)
                    check(checks, prefix + ':combined refinement', error, .002)
                    if degree < 2:
                        check(checks, prefix + ':combined independent gas force', np.linalg.norm(fine[0] + fine[-1]) / max(np.linalg.norm(fine[0]) + np.linalg.norm(fine[-1]), 1e-300))
                    records.append(dict(anchor=row['label'], join=join, model=history['model'], history=history['history'], degree=degree,
                        refinement=error, state_over_virtual=float(np.linalg.norm(fine_state) / max(np.linalg.norm(virtual[prefix + ':order6:total']), 1e-300))))
    save(ROOT / 'results/virtual-state-combined.npz', **output)
    failed = [entry for entry in checks if not entry['passed']]
    write(target, dict(state='complete', qualified=not failed, checks=checks, failed=failed, records=records,
        sha256=digest(ROOT / 'results/virtual-state-combined.npz'), finished_at=now(),
        scope='Virtual plus displaced-state mixed contribution; finite real remainder/exterior terms not silently assigned zero'))
    print(json.dumps(dict(checks=len(checks), failed=failed, maximum_refinement=max(row['refinement'] for row in records))), flush=True)
    assert not failed, failed


def validate():
    modest()
    config, unused = state235.state_protocol()
    report_names = ['mass.json', 'mass-angular.json', 'state-tangent-controls.json', 'state-replay.json',
        'state-product-control.json', 'soft-product-and-profile.json', 'real-vertex.json', 'combined.json']
    reports = {name: read(ROOT / 'results' / name) for name in report_names}
    paths = [ROOT / 'results' / name for name in report_names]
    for row in config['events']:
        path = ROOT / 'runs' / row['label'] / 'state.json'
        reports[row['label']] = read(path)
        assert digest(path.with_suffix('.npz')) == reports[row['label']]['sha256']
        paths.append(path)
    checks = []
    for name, report in reports.items():
        assert report['state'] == 'complete' and report['qualified'] and not report['failed'], name
        checks.extend(report['checks'])
    for report, filename, field in [('mass.json', 'mass-coefficients.npz', 'coefficient_sha256'),
            ('soft-product-and-profile.json', 'soft-profile-maps.npz', 'sha256'),
            ('combined.json', 'virtual-state-combined.npz', 'sha256')]:
        assert digest(ROOT / 'results' / filename) == reports[report][field]
    for name, filename in [('tangent-controls', 'state_controls235.py'), ('replay', 'state_replay235.py'),
            ('product', 'product235.py'), ('soft', 'soft235.py'), ('real', 'real235.py'), ('mass-angular', 'mass_angular235.py')]:
        assert digest(ROOT / filename) == read(ROOT / (name + '-configuration.json'))['script_sha256']
    assert digest(ROOT / 'state235.py') == read(ROOT / 'tangent-controls-configuration.json')['implementation_sha256']
    inputs = read(ROOT / 'inputs.json')
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
    check(checks, 'consumed source hashes unchanged', 0, 0)
    check(checks, 'protected workbench recent-mtime count', len(changed), 0)
    state_records = [entry for label in ('warm', 'middle', 'cold') for entry in reports[label]['records']]
    coarse_angles = [entry for entry in reports['mass-angular.json']['records'] if entry['order'] == 2]
    summary = dict(stage=235, state='complete', qualified=True, finished_at=now(), total_checks=len(checks), checks=checks, failed=[],
        maximum_original_state_replay=max(entry['relative_error'] for entry in reports['state-replay.json']['records']),
        maximum_state_product_error=max(entry['relative_error'] for entry in reports['state-product-control.json']['records']),
        maximum_statistical_mass_tangent_error=max(entry['derivative_error'] for entry in reports['state-tangent-controls.json']['records']),
        minimum_omitted_mean_derivative_error=min(entry['omitted_mean_error'] for entry in reports['state-tangent-controls.json']['records']),
        maximum_canonical_step_refinement=max(entry['canonical_step_refinement'] for entry in state_records),
        mass_background_over_planck_range=[min(entry['fraction_of_planck'] for entry in reports['mass.json']['records']), max(entry['fraction_of_planck'] for entry in reports['mass.json']['records'])],
        background_mass_term_over_statistical_range=[min(entry['background_mass_over_statistical'] for entry in state_records), max(entry['background_mass_over_statistical'] for entry in state_records)],
        maximum_wave_mass_over_total=max(entry['wave_mass_over_total'] for entry in state_records),
        maximum_soft_product_error=reports['soft-product-and-profile.json']['maximum_derivative_error'],
        maximum_profile_cancellation=max(entry['independent_quadrature_residual'] for entry in reports['soft-product-and-profile.json']['records']),
        maximum_stable_real_vertex_error=max(entry['relative_error'] for entry in reports['real-vertex.json']['records']),
        maximum_combined_refinement=max(entry['refinement'] for entry in reports['combined.json']['records']),
        original_eight_ray_mass_angular_errors={str(degree): max(entry['angular_errors'][str(degree)] for entry in coarse_angles) for degree in (0, 1, 2)},
        original_bank_changed=False, original_tolerances_changed=False, directly_consumed_files_rehashed=len(inputs), protected_recent_mtime_count=0,
        mass_angular_response='Exact scalar identity; recorded eight-ray artifacts not silently projected into the original virtual bank',
        full_real_remainder_integrated=False, actual_history_exterior_supplied=False, inclusive_mixed_source_qualified=False,
        new_empirical_fit=False, report_hashes={str(path.relative_to(ROOT)): digest(path) for path in paths},
        scope='Derived scalar pole-mass functional from the directional Dirac kernel, implemented three full-basis displaced-state mixed terms, common soft-profile matching, and stable exact real vertex; virtual/state sum saved')
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
    assert all(path.read_text(encoding='utf-8').startswith('# Stage235 SAVED') for path in bookmarks)
    target = ROOT / 'results/stage-integrity.json'
    assert not target.exists()
    paths = {str(path.relative_to(ROOT)): digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file()}
    write(target, dict(stage=235, state='complete', qualified=True, sealed_at=now(), file_hashes=paths,
        directly_consumed_inputs=read(ROOT / 'results/inputs-final.json'), bookmarks={str(path): digest(path) for path in bookmarks},
        scope=completion['scope'], inclusive_mixed_source_qualified=False))
    print(json.dumps(dict(seal_sha256=digest(target), files=len(paths), checks=completion['total_checks'])), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['combine', 'validate', 'seal'])
    args = parser.parse_args()
    {'combine': combine, 'validate': validate, 'seal': seal}[args.mode]()
