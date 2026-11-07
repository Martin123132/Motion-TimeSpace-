from common240 import *
from virtual240 import secondary_protocol
import argparse


def gather_report(path, inputs, checks, owner, output=None):
    report = read(register(inputs, path))
    assert isinstance(report.get('qualified'), bool), str(path)
    assert isinstance(report.get('checks'), list) and report['checks'], str(path)
    for entry in report['checks']:
        assert isinstance(entry['passed'], bool), str(path)
        checks.append(dict(owner=owner, **entry))
    failed = [entry for entry in report['checks'] if not entry['passed']]
    assert report['qualified'] == (not failed), str(path)
    assert report.get('failed') == failed, str(path)
    if output is not None:
        register(inputs, output, report['sha256'])
        arrays = packet(output)
        check(checks, owner + ':all output arrays finite', int(not all(np.all(np.isfinite(value)) for value in arrays.values())), 0)
    return report


def validate():
    modest()
    config = secondary_protocol()
    assert not (ROOT / 'results/completion.json').exists()
    assert not (ROOT / 'STOP-REQUESTED').exists()
    inputs = read(ROOT / 'inputs.json')
    for path, expected in read(ROOT / 'secondary-configuration.json')['inputs'].items():
        register(inputs, path, expected)
    for name, script, key in [('assessment-configuration.json', 'assess240.py', 'configuration_sha256'),
            ('radial-configuration.json', 'radial240.py', 'parent_configuration')]:
        frozen = read(register(inputs, ROOT / name))
        assert frozen['script_sha256'] == digest(ROOT / script)
        assert frozen[key] == digest(ROOT / 'configuration.json')
    checks, reports, refinement = [], [], []
    preflight = gather_report(ROOT / 'results/preflight.json', inputs, checks, 'exact-amplitude preflight')
    assert preflight['script_sha256'] == digest(ROOT / 'preflight240.py')
    control = gather_report(ROOT / 'results/secondary-control.json', inputs, checks, 'event0 secondary control')
    assert control['packets'] == 13
    for path in sorted((ROOT / 'control').rglob('*.json')):
        report = read(register(inputs, path))
        register(inputs, path.with_suffix('.npz'), report['sha256'])
        assert report['qualified']
    ray_counts = {26: 0, 18: 0}
    signed_events, maximum_force = 0, 0.
    packet_counts = dict(virtual=0, state=0, tensor=0)
    for row in config['events']:
        for radial, orders in ((26, config['angular_orders']), (18, [6])):
            for order in orders:
                directions = list(angular.inherited.source.angular_nodes(order))
                for index, direction in enumerate(directions):
                    stem = (ROOT / 'real' / event_key(row) / f'angular{order}' / f'ray-{index:03d}' if radial == 26 else
                        ROOT / 'radial18' / event_key(row) / f'ray-{index:03d}')
                    report = read(register(inputs, stem.with_suffix('.json')))
                    expected_config = ROOT / ('configuration.json' if radial == 26 else 'radial-configuration.json')
                    assert report['configuration_sha256'] == digest(expected_config)
                    assert report['event_key'] == event_key(row)
                    assert (report['angular_order'], report['radial_order'], report['ray']) == (order, radial, index)
                    assert report['event_weight'] == row['weight']
                    assert report['angular_weight'] == direction[1]
                    assert report['evaluated_events'] > 0 and report['panels'] > 0
                    register(inputs, stem.with_suffix('.npz'), report['sha256'])
                    arrays = packet(stem.with_suffix('.npz'))
                    expected_names = {f'{kind}:join{join}:l{degree}:{part}' for kind in ('control', 'difference')
                        for join in config['joins'] for degree in config['multipoles'] for part in ('finite', 'logarithm', 'total')}
                    assert set(arrays) == expected_names
                    check(checks, f'{event_key(row)}:a{order}:r{radial}:ray{index}:finite arrays and dimensions',
                        int(not all(value.shape == (7, 98, 99) and np.all(np.isfinite(value)) for value in arrays.values())), 0)
                    check(checks, f'{event_key(row)}:a{order}:r{radial}:ray{index}:event four-force', report['maximum_independent_four_force_residual'])
                    maximum_force = max(maximum_force, report['maximum_independent_four_force_residual'])
                    signed_events += report['evaluated_events']
                    ray_counts[radial] += 1
        for order in config['angular_orders']:
            tensor_path = ROOT / 'virtual' / event_key(row) / f'angular{order}-tensors.json'
            tensor = read(register(inputs, tensor_path))
            assert tensor['script_sha256'] == digest(ROOT / 'virtual240.py')
            assert tensor['event'] == event_key(row) and tensor['angular_order'] == order
            assert len(tensor['rays']) == 2 * order**2
            assert tensor['tensor_checks'] and all(entry['passed'] for entry in tensor['tensor_checks'])
            packet_counts['tensor'] += 1
            for join in config['joins']:
                path = ROOT / 'virtual' / event_key(row) / f'angular{order}-join{join}.npz'
                report = gather_report(path.with_suffix('.json'), inputs, checks, f'{event_key(row)}:a{order}:join{join}:virtual', path)
                assert report['script_sha256'] == digest(ROOT / 'virtual240.py')
                assert report['configuration_sha256'] == digest(ROOT / 'secondary-configuration.json')
                assert report['event'] == event_key(row) and report['order'] == order and report['join'] == join
                packet_counts['virtual'] += 1
        path = ROOT / 'state' / event_key(row) / 'state.npz'
        report = gather_report(path.with_suffix('.json'), inputs, checks, event_key(row) + ':state', path)
        assert report['script_sha256'] == digest(ROOT / 'state240.py')
        assert report['configuration_sha256'] == digest(ROOT / 'secondary-configuration.json')
        assert report['event'] == event_key(row)
        packet_counts['state'] += 1
    assert ray_counts == {26: 624, 18: 432} and packet_counts == dict(virtual=24, state=6, tensor=12)
    for hard_event in (1, 2):
        for group in (f'event{hard_event}', f'radial18-event{hard_event}'):
            folder = ROOT / 'workers' / group
            assert read(folder / 'status.json')['state'] == 'complete'
            assert (folder / 'COMPLETE').read_text(encoding='utf-8').strip() == 'complete'
        for path, expected in read(ROOT / 'workers' / f'event{hard_event}' / 'inputs.json').items():
            register(inputs, path, expected)
    for anchor in ('warm', 'middle', 'cold'):
        report = gather_report(ROOT / 'results' / f'{anchor}-assessment.json', inputs, checks, anchor + ':component and sum assessment')
        assert report['script_sha256'] == digest(ROOT / 'assess240.py')
        assert report['anchor'] == anchor and report['state'] == 'complete'
        for path, expected in report['consumed_inputs'].items():
            register(inputs, path, expected)
        target = ROOT / 'results' / f'{anchor}-three-hard-angle-sum.npz'
        register(inputs, target, report['output_sha256'])
        check(checks, anchor + ':finite three-hard-angle outputs', int(not all(np.all(np.isfinite(value)) for value in packet(target).values())), 0)
        old_report_path = REFERENCE / 'results' / f'{anchor}-assessment.json'
        old_report = read(register(inputs, old_report_path))
        assert old_report['qualified']
        reports.append(report)
        refinement.extend(report['records'])
    for path, expected in read(ROOT / 'running-bookmarks.json').items():
        assert digest(path) == expected, path
    modules(inputs)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
    assert not list(ROOT.rglob('__pycache__')) and not list(ROOT.rglob('*.partial'))
    protected = BRANCH.parent.parent / 'formalization-workbench'
    changed = [str(path) for path in protected.rglob('*') if path.is_file()
        and path.stat().st_mtime >= datetime.fromisoformat(START).timestamp()]
    check(checks, 'protected workbench recent-mtime count', len(changed), 0)
    failures = [entry for entry in checks if not entry['passed']]
    worst = sorted(refinement, key=lambda row: max(row['matrix'], row['gas'], row['photon_shape']), reverse=True)[:15]
    result = dict(stage=240, state='complete', qualified=not failures, checks=checks, failed=failures,
        accepted_check_count=sum(entry['passed'] for entry in checks), total_check_count=len(checks),
        preflight_checks=len(preflight['checks']), control_checks=len(control['checks']),
        new_real_rays=ray_counts[26], new_radial_control_rays=ray_counts[18], signed_real_evaluations=signed_events,
        new_virtual_packets=packet_counts['virtual'], new_state_packets=packet_counts['state'],
        new_tensor_packets=packet_counts['tensor'], maximum_event_four_force_residual=maximum_force,
        maximum_refinement=max(max(row['matrix'], row['gas'], row['photon_shape']) for row in refinement),
        worst_refinement=worst, directly_consumed_files_rehashed=len(inputs), protected_recent_mtime_count=len(changed),
        original_bank_changed=False, original_histories_changed=False, original_tolerances_changed=False,
        complete_physical_event_bank_extended=False, retained_theory_unchanged=True,
        scope='Three hard-scattering quadrature angles at x14 and first electron node, three temperatures, equilibrium and six histories, both joins and l0/1/2; not a full electron/frequency integral',
        numerical_scope='Observed angular4-to6 at radial26 and radial18-to26 at angular6 for new angles; retained event0 radial comparison at angular4; not a rigorous quadrature-error bound',
        physical_use='Expanded source matrices and monopole quadratic sources for the retained stress/gravity map; no new closure',
        source_sha256=digest(__file__), finished_at=now())
    write(ROOT / 'results/inputs-final.json', inputs)
    write(ROOT / 'results/completion.json', result)
    print(json.dumps({name: value for name, value in result.items() if name not in ('checks', 'failed', 'worst_refinement')}, indent=2), flush=True)
    print(json.dumps(dict(first_failures=failures[:10], worst_refinement=worst[:3])), flush=True)


def seal():
    target = ROOT / 'results/stage-integrity.json'
    assert not target.exists()
    secondary_protocol()
    result = read(ROOT / 'results/completion.json')
    assert result['qualified'] and not result['failed'] and result['state'] == 'complete'
    assert result['source_sha256'] == digest(__file__)
    for path, expected in read(ROOT / 'results/inputs-final.json').items():
        assert digest(path) == expected, path
    for name in ('RESULTS.md', 'NEXT.md', 'RUN-NOTES.md'):
        assert (ROOT / name).is_file()
    bookmarks = [BRANCH / 'RESUME-CURRENT.md', BRANCH.parent / 'CURRENT_LOCAL_RESUME.md']
    assert all(path.read_text(encoding='utf-8').startswith('# Stage240 SAVED') for path in bookmarks)
    payloads = {str(path.relative_to(ROOT)): digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file()}
    write(target, dict(stage=240, state='complete', qualified=True, sealed_at=now(), file_hashes=payloads,
        directly_consumed_inputs=read(ROOT / 'results/inputs-final.json'), bookmarks={str(path): digest(path) for path in bookmarks},
        scope=result['scope'], numerical_scope=result['numerical_scope'], original_bank_changed=False,
        original_tolerances_changed=False, retained_theory_unchanged=True))
    print(json.dumps(dict(seal_sha256=digest(target), payloads=len(payloads), qualified=True)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['validate', 'seal'])
    {'validate': validate, 'seal': seal}[parser.parse_args().mode]()
