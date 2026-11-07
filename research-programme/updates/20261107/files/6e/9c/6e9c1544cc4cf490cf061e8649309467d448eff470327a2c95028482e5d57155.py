from resume_replay239 import *


def validate():
    modest()
    config, frozen, resumed = resume_protocol()
    points = read(ROOT / 'results/points.json')
    assert points['script_sha256'] == digest(ROOT / 'test239.py')
    checks = [dict(owner='point-and-algebra', **entry) for entry in points['checks']]
    inputs = read(ROOT / 'replay-inputs.json')
    for order in (6, 8):
        for path, expected in read(ROOT / 'confirmed-replay' / f'inputs-angular{order}.json').items():
            register(inputs, path, expected)
    reports, records, report_hashes = [], [], {}
    for case in frozen['cases']:
        stem = ROOT / 'confirmed-replay' / case_label(case)
        report = read(stem.with_suffix('.json'))
        assert report['configuration_sha256'] == digest(ROOT / 'replay-configuration.json')
        assert report['resume_sha256'] == digest(ROOT / 'replay-resume-configuration.json')
        assert report['sha256'] == digest(stem.with_suffix('.npz'))
        checks.extend(dict(owner='complete-radial-replay', **entry) for entry in report['checks'])
        arrays = packet(stem.with_suffix('.npz'))
        reference = packet(Path(case['reference_stem']).with_suffix('.npz'))
        bitwise = []
        for name in arrays:
            check(bitwise, case_label(case) + ':' + name + ':bitwise reference equality', int(not np.array_equal(arrays[name], reference[name])), 0)
        checks.extend(dict(owner='bitwise-reference-check', **entry) for entry in bitwise)
        reports.append(report)
        records.extend(dict(case=case_label(case), **row) for row in report['records'])
        report_hashes[str(stem.with_suffix('.json').relative_to(ROOT))] = digest(stem.with_suffix('.json'))
        report_hashes[str(stem.with_suffix('.npz').relative_to(ROOT))] = digest(stem.with_suffix('.npz'))
    modules(inputs)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    for path, expected in config['bookmarks'].items():
        assert digest(path) == expected, path
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
    assert not list(ROOT.rglob('__pycache__')) and not list(ROOT.rglob('*.partial'))
    protected = BRANCH.parent.parent / 'formalization-workbench'
    changed = [str(path) for path in protected.rglob('*') if path.is_file()
        and path.stat().st_mtime >= datetime.fromisoformat(START).timestamp()]
    extra = []
    check(extra, 'protected workbench recent-mtime count', len(changed), 0)
    check(extra, 'all consumed input hashes unchanged', 0, 0)
    check(extra, 'exactly18 frozen replay packets', abs(len(reports) - 18), 0)
    check(extra, 'old incomplete metadata packet preserved', int(digest(resumed['recovered_array']) != resumed['recovered_sha256']), 0)
    checks.extend(dict(owner='integrity', **entry) for entry in extra)
    failures = [entry for entry in checks if not entry['passed']]
    timing = []
    for digits in (config['digits'], config['control_digits']):
        group = [row for row in points['records'] if row['digits'] == digits]
        timing.append(dict(digits=digits, cases=len(group),
            reference_seconds=sum(row['reference_seconds'] for row in group),
            candidate_seconds=sum(row['accelerated_seconds'] for row in group),
            speedup=sum(row['reference_seconds'] for row in group) / sum(row['accelerated_seconds'] for row in group)))
    result = dict(stage=239, state='complete', qualified=not failures, checks=checks, failed=failures,
        accepted_check_count=len(checks), point_checks=len(points['checks']), point_cases=len(points['records']),
        exact_kinematic_and_amplitude_identities=sum(row['name'].startswith('symbolic:') for row in points['checks']),
        complete_radial_packets=len(reports), signed_real_evaluations=sum(row['evaluated_events'] for row in reports),
        source_matrices=18 * 36 * 7, maximum_matrix_replay_error=max(row['matrix'] for row in records),
        maximum_independent_gas_replay_error=max(row['gas'] for row in records),
        source_arrays_bitwise_equal=all(row['passed'] for row in checks if row['owner'] == 'bitwise-reference-check'),
        maximum_point_error=points['maximum_accuracy_error'], point_event_timings=timing,
        mean_construction_seconds=points['mean_construction_seconds'],
        summed_candidate_ray_seconds=sum(row['seconds'] for row in reports),
        summed_historical_reference_seconds=sum(row['old_seconds'] for row in reports),
        historical_ray_time_ratio=sum(row['old_seconds'] for row in reports) / sum(row['seconds'] for row in reports),
        full_ray_timing_is_controlled_comparison=False,
        directly_consumed_files_rehashed=len(inputs), protected_recent_mtime_count=len(changed),
        coefficient_fitting_used=False, original_bank_changed=False, original_histories_changed=False,
        original_tolerances_changed=False, complete_physical_event_bank_extended=False,
        retained_theory_unchanged=True,
        scope='Exact rational spin-summed intensity on18 replayed full radial packets across3 saved x14,event0 anchors; all7 histories, both joins, l0/1/2, leading and correction',
        physical_use='Same retained source evaluated more cheaply, enabling broader source support for the Stage238 gravity interface',
        report_hashes=report_hashes, finished_at=now())
    write(ROOT / 'results/inputs-final.json', inputs)
    write(ROOT / 'results/completion.json', result)
    print(json.dumps({name: value for name, value in result.items() if name not in ('checks', 'failed', 'report_hashes')}, indent=2), flush=True)


def seal():
    target = ROOT / 'results/stage-integrity.json'
    assert not target.exists()
    result = read(ROOT / 'results/completion.json')
    assert result['qualified']
    resume_protocol()
    for path, expected in read(ROOT / 'results/inputs-final.json').items():
        assert digest(path) == expected, path
    for name, expected in result['report_hashes'].items():
        assert digest(ROOT / name) == expected, name
    for name in ('RESULTS.md', 'NEXT.md', 'RUN-NOTES.md'):
        assert (ROOT / name).exists()
    bookmarks = [BRANCH / 'RESUME-CURRENT.md', BRANCH.parent / 'CURRENT_LOCAL_RESUME.md']
    assert all(path.read_text(encoding='utf-8').startswith('# Stage239 SAVED') for path in bookmarks)
    payloads = {str(path.relative_to(ROOT)): digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file()}
    write(target, dict(stage=239, state='complete', qualified=True, sealed_at=now(), file_hashes=payloads,
        directly_consumed_inputs=read(ROOT / 'results/inputs-final.json'), bookmarks={str(path): digest(path) for path in bookmarks},
        scope=result['scope'], original_bank_changed=False, source_arrays_bitwise_equal=result['source_arrays_bitwise_equal']))
    print(json.dumps(dict(seal_sha256=digest(target), payloads=len(payloads), qualified=True)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['validate', 'seal'])
    {'validate': validate, 'seal': seal}[parser.parse_args().mode]()
