from common241 import *
from repair241 import setup_repair, CANDIDATE
import argparse


def report_at(path, checks, inputs, owner):
    report = read(register(inputs, path))
    assert isinstance(report['qualified'], bool)
    assert report['checks']
    failures = [entry for entry in report['checks'] if not entry['passed']]
    assert failures == report['failed']
    assert report['qualified'] == (not failures)
    checks.extend(dict(owner=owner, **entry) for entry in report['checks'])
    return report


def validate():
    modest()
    config = setup_repair()
    assert not (ROOT / 'results/completion.json').exists()
    inputs = read(ROOT / 'inputs.json')
    checks, summaries, preserved_failures = [], [], []
    for name in ('algebra', 'control', 'metric-jet-derivation', 'precision-pilot'):
        report = report_at(ROOT / 'results' / f'{name}.json', checks, inputs, name)
        assert report['qualified']
        if 'script_sha256' in report:
            script = {'algebra': 'algebra241.py', 'control': 'ports241.py', 'metric-jet-derivation': 'jet241.py', 'precision-pilot': 'repair241.py'}[name]
            assert digest(ROOT / script) == report['script_sha256']
    pilot = read(ROOT / 'results/precision-pilot.json')
    for anchor in ('warm', 'middle', 'cold'):
        original = read(register(inputs, ROOT / 'results' / f'{anchor}.json'))
        assert not original['qualified']
        preserved_failures.extend(dict(anchor=anchor, **entry) for entry in original['failed'])
        register(inputs, ROOT / 'results' / f'{anchor}-ports-and-jets.npz', original['output_sha256'])
        candidate = report_at(CANDIDATE / 'results' / f'{anchor}.json', checks, inputs, anchor + ':precision-carried source')
        assert candidate['script_sha256'] == digest(ROOT / 'repair241.py')
        assert [(row['name'], row['limit']) for row in original['checks']] == [(row['name'], row['limit']) for row in candidate['checks']]
        path = CANDIDATE / 'results' / f'{anchor}-ports-and-jets.npz'
        arrays = packet(register(inputs, path, candidate['output_sha256']))
        check(checks, anchor + ':all candidate arrays finite', int(not all(np.all(np.isfinite(value)) for value in arrays.values())), 0)
        count = 0
        for key, high in arrays.items():
            if key.endswith(':photon'):
                low_key = key + '_low'
                assert low_key in arrays
                assert arrays[low_key].shape == high.shape == (96, 99)
                count += 1
        assert count == 432
        check(checks, anchor + ':retained high/low photon pairs', abs(count - 432), 0)
        for path, expected in read(CANDIDATE / 'results' / f'{anchor}-inputs.json').items():
            register(inputs, path, expected)
        summaries.append(dict(anchor=anchor, checks=len(candidate['checks']), failures=len(candidate['failed']),
            maximum_port_refinement=candidate['maximum_port_refinement'], maximum_readout_error=candidate['maximum_readout_error'],
            maximum_exchange_error=candidate['maximum_exchange_error'], maximum_native_frame_error=candidate['maximum_native_frame_error']))
    assert len(preserved_failures) == 146
    for path, expected in read(ROOT / 'results/control-inputs.json').items():
        register(inputs, path, expected)
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
    check(checks, 'protected workbench recent-mtime count', len(changed), 0)
    failures = [entry for entry in checks if not entry['passed']]
    result = dict(stage=241, state='complete', qualified=not failures, checks=checks, failed=failures,
        accepted_check_count=sum(row['passed'] for row in checks), total_check_count=len(checks), anchors=summaries,
        preserved_original_failed_checks=preserved_failures, precision_pilot_maximum_mass_error=pilot['maximum_mass_error'],
        precision_pilot_maximum_energy_error=pilot['maximum_moment_error'], exact_neumann_remainder_bound=pilot['solver_bound']['exact_neumann_remainder'],
        maximum_port_refinement=max(row['maximum_port_refinement'] for row in summaries),
        maximum_readout_error=max(row['maximum_readout_error'] for row in summaries),
        maximum_exchange_error=max(row['maximum_exchange_error'] for row in summaries),
        maximum_native_frame_error=max(row['maximum_native_frame_error'] for row in summaries),
        directly_consumed_files_rehashed=len(inputs), protected_recent_mtime_count=len(changed),
        original_bank_changed=False, original_histories_changed=False, original_tolerances_changed=False,
        independent_gas_replaced=False, finite_interval_propagated=False, tail_closure_added=False,
        scope=config['source_scope'], physical_advance='Expanded source to native stress/metric ports; derived local cubic metric response and source-owned density/background-transfer columns',
        remaining_for_finite_evolution='Actual time-dependent background/source ownership, explicit tails and matched full transport; no interpolation of frozen-history anchors asserted as physical evolution',
        source_sha256=digest(__file__), finished_at=now())
    write(ROOT / 'results/inputs-final.json', inputs)
    write(ROOT / 'results/completion.json', result)
    print(json.dumps({name: value for name, value in result.items() if name not in ('checks', 'failed', 'preserved_original_failed_checks')}, indent=2), flush=True)


def seal():
    target = ROOT / 'results/stage-integrity.json'
    assert not target.exists()
    setup_repair()
    result = read(ROOT / 'results/completion.json')
    assert result['qualified'] and not result['failed']
    assert result['source_sha256'] == digest(__file__)
    for path, expected in read(ROOT / 'results/inputs-final.json').items():
        assert digest(path) == expected, path
    for name in ('RESULTS.md', 'NEXT.md', 'RUN-NOTES.md'):
        assert (ROOT / name).is_file()
    bookmarks = [BRANCH / 'RESUME-CURRENT.md', BRANCH.parent / 'CURRENT_LOCAL_RESUME.md']
    assert all(path.read_text(encoding='utf-8').startswith('# Stage241 SAVED') for path in bookmarks)
    payloads = {str(path.relative_to(ROOT)): digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file()}
    write(target, dict(stage=241, qualified=True, state='complete', sealed_at=now(), file_hashes=payloads,
        directly_consumed_inputs=read(ROOT / 'results/inputs-final.json'), bookmarks={str(path): digest(path) for path in bookmarks},
        scope=result['scope'], physical_advance=result['physical_advance'], original_bank_changed=False,
        original_tolerances_changed=False, finite_interval_propagated=False, raw_failed_trials_preserved=True))
    print(json.dumps(dict(seal_sha256=digest(target), payloads=len(payloads), qualified=True)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['validate', 'seal'])
    {'validate': validate, 'seal': seal}[parser.parse_args().mode]()
