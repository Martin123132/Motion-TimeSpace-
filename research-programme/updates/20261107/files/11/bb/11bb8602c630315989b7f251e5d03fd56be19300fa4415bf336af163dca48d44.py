from common237 import *
import argparse


def validate():
    modest()
    config = protocol()
    inputs = read(ROOT / 'inputs.json')
    checks, reports = {}, {}
    for path in sorted((ROOT / 'virtual').rglob('*-join*.json')):
        report = read(path)
        assert report['qualified'] and report['script_sha256'] == digest(ROOT / 'virtual237.py')
        assert digest(path.with_suffix('.npz')) == report['sha256']
        reports[str(path.relative_to(ROOT))] = digest(path)
        for entry in report['checks']:
            checks[entry['name']] = entry
    assert len(reports) == 24
    anchors = []
    for row in config['events']:
        path = ROOT / 'results' / (row['label'] + '-assessment.json')
        report = read(path)
        assert report['state'] == 'complete' and report['script_sha256'] == digest(ROOT / 'assess237.py')
        assert digest(path.with_suffix('.npz')) == report['output_sha256']
        reports[str(path.relative_to(ROOT))] = digest(path)
        for entry in report['checks']:
            checks[entry['name']] = entry
        for source_path, expected in report['directly_consumed_inputs'].items():
            register(inputs, source_path, expected)
        anchors.append(report)
    for module in list(sys.modules.values()):
        name = getattr(module, '__file__', None)
        if name:
            path = Path(name).resolve()
            if path.suffix == '.py' and path.is_relative_to(BRANCH) and not path.is_relative_to(ROOT):
                register(inputs, path)
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
    check(extra, 'consumed inputs unchanged', 0, 0)
    for entry in extra:
        checks[entry['name']] = entry
    real_reports = [read(path) for path in (ROOT / 'real').rglob('ray-*.json')]
    assert len(real_reports) == 600
    records = [entry for report in anchors for entry in report['records']]
    final_records = [entry for entry in records if entry['comparison'] in ('6-to8', 'virtual6-to8')]
    original_records = [entry for entry in records if entry['comparison'] in ('original-to8', 'virtual2-to8')]
    changes = []
    for comparison_name in sorted(set(entry['comparison'] for entry in records)):
        subset = [entry for entry in records if entry['comparison'] == comparison_name]
        for component in sorted(set(entry['component'] for entry in subset)):
            group = [entry for entry in subset if entry['component'] == component]
            worst = max(group, key=lambda entry: max(entry['matrix'], entry.get('gas', 0)))
            changes.append(dict(comparison=comparison_name, component=component, count=len(group),
                failures=sum(not entry['passed'] for entry in group), maximum_matrix_change=max(entry['matrix'] for entry in group),
                maximum_gas_change=max(entry.get('gas', 0) for entry in group),
                maximum_photon_shape_change=max(entry['photon_shape'] for entry in group), worst_case=worst))
    failures = [entry for entry in checks.values() if not entry['passed']]
    final_pass = all(entry['passed'] for entry in final_records)
    original_pass = all(entry['passed'] for entry in original_records)
    result = dict(stage=237, state='complete', qualified=not failures and final_pass,
        identities_pass=not failures, final_angular_accuracy_pass=final_pass,
        original_angular_accuracy_pass=original_pass, angular_tolerance=config['angular_tolerance'],
        checks=list(checks.values()), failed_identities=failures, unique_identity_checks=len(checks),
        final_accuracy_checks=len(final_records), final_accuracy_failures=sum(not entry['passed'] for entry in final_records),
        original_accuracy_checks=len(original_records), original_accuracy_failures=sum(not entry['passed'] for entry in original_records),
        maximum_final_change=max(max(entry['matrix'], entry.get('gas', 0)) for entry in final_records),
        maximum_original_change=max(max(entry['matrix'], entry.get('gas', 0)) for entry in original_records),
        component_summary=changes, real_ray_packets=len(real_reports), virtual_packets=24,
        total_signed_real_evaluations=sum(entry['evaluated_events'] for entry in real_reports),
        summed_real_seconds=sum(entry['seconds'] for entry in real_reports),
        report_hashes=reports, directly_consumed_files_rehashed=len(inputs), protected_recent_mtime_count=len(changed),
        original_bank_changed=False, original_histories_changed=False, original_tolerances_changed=False,
        physical_exterior_supplied=False, polarized_soft_response_qualified=False, new_empirical_fit=False,
        scope='Three saved x14 event0 temperatures, both joins, six heavy/cold original/half/quarter histories, scalar-intensity l0/1/2. Real equilibrium controls also tested.',
        finished_at=now())
    write(ROOT / 'results/inputs-final.json', inputs)
    write(ROOT / 'results/completion.json', result)
    print(json.dumps({key: value for key, value in result.items() if key not in ('checks', 'failed_identities', 'report_hashes', 'component_summary')}, indent=2), flush=True)
    print(json.dumps([dict(comparison=row['comparison'], component=row['component'], maximum_matrix_change=row['maximum_matrix_change'],
        maximum_gas_change=row['maximum_gas_change'], failures=row['failures']) for row in changes], indent=2), flush=True)


def seal():
    target = ROOT / 'results/stage-integrity.json'
    assert not target.exists()
    completion = read(ROOT / 'results/completion.json')
    assert completion['state'] == 'complete'
    for path, expected in read(ROOT / 'results/inputs-final.json').items():
        assert digest(path) == expected, path
    for name, expected in completion['report_hashes'].items():
        assert digest(ROOT / name) == expected, name
    for name in ('RESULTS.md', 'NEXT.md', 'RUN-NOTES.md'):
        assert (ROOT / name).exists()
    bookmarks = [BRANCH / 'RESUME-CURRENT.md', BRANCH.parent / 'CURRENT_LOCAL_RESUME.md']
    assert all(path.read_text(encoding='utf-8').startswith('# Stage237 SAVED') for path in bookmarks)
    payloads = {str(path.relative_to(ROOT)): digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file()}
    write(target, dict(stage=237, state='complete', qualified=completion['qualified'], sealed_at=now(), file_hashes=payloads,
        directly_consumed_inputs=read(ROOT / 'results/inputs-final.json'), bookmarks={str(path): digest(path) for path in bookmarks},
        scope=completion['scope'], final_angular_accuracy_pass=completion['final_angular_accuracy_pass'],
        original_angular_accuracy_pass=completion['original_angular_accuracy_pass']))
    print(json.dumps(dict(seal_sha256=digest(target), payloads=len(payloads), qualified=completion['qualified'])), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['validate', 'seal'])
    {'validate': validate, 'seal': seal}[parser.parse_args().mode]()
