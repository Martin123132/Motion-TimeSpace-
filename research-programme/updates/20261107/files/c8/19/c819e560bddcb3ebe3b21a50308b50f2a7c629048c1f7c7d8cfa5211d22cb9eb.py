from integrate236 import *


def validate():
    modest()
    config, frozen = run_protocol()
    inputs = read(ROOT / 'inputs.json')
    checks = []
    reports = {}
    names = ['density-pilot.json', 'factor-pilot.json', 'integrand-pilot.json', 'matching.json']
    names += [row['label'] + '-assessment.json' for row in config['events']]
    for name in names:
        report = read(ROOT / 'results' / name)
        reports[name] = report
        checks.extend(report['checks'])
        for path, expected in report.get('directly_consumed_inputs', {}).items():
            register(inputs, path, expected)
        if 'output_sha256' in report:
            assert digest((ROOT / 'results' / name).with_suffix('.npz')) == report['output_sha256']
    for name, expected in read(ROOT / 'results/factor-pilot.json')['script_hashes'].items():
        assert digest(ROOT / name) == expected, name
    assert digest(ROOT / 'matching236.py') == reports['matching.json']['script_sha256']
    assert all(digest(ROOT / 'assess236.py') == reports[row['label'] + '-assessment.json']['script_sha256'] for row in config['events'])
    modules(inputs)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    for path, expected in config['bookmarks'].items():
        assert digest(path) == expected, path
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
    assert not list(ROOT.rglob('__pycache__')) and not list(ROOT.rglob('*.partial'))
    protected = BRANCH.parent.parent / 'formalization-workbench'
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= datetime.fromisoformat(START).timestamp()]
    check(checks, 'protected workbench recent-mtime count', len(changed), 0)
    check(checks, 'consumed hashes unchanged', 0, 0)
    failures = [entry for entry in checks if not entry['passed']]
    ray_reports = [read(path) for path in (ROOT / 'rays').rglob('ray-*.json')]
    assert len(ray_reports) == 192
    records = [record for row in config['events'] for record in reports[row['label'] + '-assessment.json']['records']]
    summary = dict(stage=236, state='complete', qualified=not failures, finished_at=now(), checks=checks, failed=failures,
        total_checks=len(checks), full_finite_real_integrated=True, anchor_count=3, complete_ray_packets=len(ray_reports),
        total_real_event_evaluations=sum(row['evaluated_events'] for row in ray_reports),
        summed_worker_seconds=sum(row['seconds'] for row in ray_reports),
        maximum_event_force_residual=max(row['maximum_independent_four_force_residual'] for row in ray_reports),
        maximum_radial_refinement=max(row['refinement'] for row in records if 'refinement' in row),
        maximum_gas_refinement=max(row['gas_refinement'] for row in records if 'gas_refinement' in row and row['degree'] < 2),
        maximum_matched_refinement=max(row['matched_refinement'] for row in records if 'matched_refinement' in row),
        maximum_original_linear_comparison=max(row['inherited_linear_replay'] for row in records if 'inherited_linear_replay' in row),
        maximum_profile_cancellation=max(row['cancellation'] for row in reports['matching.json']['records']),
        report_hashes={name: digest(ROOT / 'results' / name) for name in names},
        directly_consumed_files_rehashed=len(inputs), protected_recent_mtime_count=len(changed),
        original_bank_changed=False, original_tolerances_changed=False, original_histories_changed=False,
        actual_history_exterior_supplied=False, general_virtual_angular_qualified=False, polarized_soft_response_qualified=False,
        inclusive_physical_claim=False, new_empirical_fit=False,
        scope='Finite-domain full-basis real mixed source and its combination with saved virtual/state blocks at three original x14 event0 anchors; original angular4')
    write(ROOT / 'results/inputs-final.json', inputs)
    write(ROOT / 'results/completion.json', summary)
    print(json.dumps({key: value for key, value in summary.items() if key not in ('checks', 'failed', 'report_hashes')}, indent=2), flush=True)
    if failures:
        print(json.dumps(dict(failures=failures[:15], count=len(failures))), flush=True)


def seal():
    target = ROOT / 'results/stage-integrity.json'
    assert not target.exists()
    completion = read(ROOT / 'results/completion.json')
    assert completion['state'] == 'complete'
    for path, expected in read(ROOT / 'results/inputs-final.json').items():
        assert digest(path) == expected, path
    for name, expected in completion['report_hashes'].items():
        assert digest(ROOT / 'results' / name) == expected, name
    for name in ('RESULTS.md', 'NEXT.md', 'RUN-NOTES.md'):
        assert (ROOT / name).exists()
    bookmarks = [BRANCH / 'RESUME-CURRENT.md', BRANCH.parent / 'CURRENT_LOCAL_RESUME.md']
    assert all(path.read_text(encoding='utf-8').startswith('# Stage236 SAVED') for path in bookmarks)
    payloads = {str(path.relative_to(ROOT)): digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file()}
    write(target, dict(stage=236, state='complete', qualified=completion['qualified'], sealed_at=now(), file_hashes=payloads,
        directly_consumed_inputs=read(ROOT / 'results/inputs-final.json'), bookmarks={str(path): digest(path) for path in bookmarks},
        scope=completion['scope'], inclusive_physical_claim=False, numerical_failures=len(completion['failed'])))
    print(json.dumps(dict(seal_sha256=digest(target), payloads=len(payloads), qualified=completion['qualified'])), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['validate', 'seal'])
    {'validate': validate, 'seal': seal}[parser.parse_args().mode]()
