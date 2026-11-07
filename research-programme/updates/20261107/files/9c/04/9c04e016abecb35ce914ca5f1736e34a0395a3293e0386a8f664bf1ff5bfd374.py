from rational239 import *
import argparse
import types


def freeze():
    config = protocol()
    assert read(ROOT / 'results/points.json')['qualified']
    assert not (ROOT / 'replay-configuration.json').exists()
    cases = []
    inputs = read(ROOT / 'inputs.json')
    seal = read(REFERENCE / 'results/stage-integrity.json')
    seal_hashes = {name.replace('\\', '/'): value for name, value in seal['file_hashes'].items()}
    for event in config['events']:
        for order, rays in ((6, [0, 35, 71]), (8, [0, 63, 127])):
            for ray in rays:
                relative_stem = f'real/{event["label"]}/angular{order}/ray-{ray:03d}'
                report = read(register(inputs, REFERENCE / (relative_stem + '.json'), seal_hashes[relative_stem + '.json']))
                register(inputs, REFERENCE / (relative_stem + '.npz'), report['sha256'])
                cases.append(dict(anchor=event['label'], angular_order=order, radial_order=26, ray=ray,
                    reference_stem=str(REFERENCE / relative_stem), old_seconds=report['seconds'],
                    evaluated_events=report['evaluated_events']))
    write(ROOT / 'replay-inputs.json', inputs)
    write(ROOT / 'replay-configuration.json', dict(frozen_at=now(), cases=cases, digits=config['digits'],
        point_report_sha256=digest(ROOT / 'results/points.json'), script_sha256=digest(__file__),
        candidate_code_sha256=digest(ROOT / 'rational239.py'),
        inherited_integrator_sha256=digest(integration.__file__),
        numerical_change='Only Direction constructor rebound in a private copy of the inherited integrator globals',
        unchanged='weak factors, grids, histories, radial quadrature, soft profiles, subtraction order and gas recoil',
        replay_tolerance=config['same_discretization_replay_tolerance'],
        cancelled_increment_tolerance=config['same_discretization_replay_tolerance']))
    print(json.dumps(dict(replay_frozen=True, cases=len(cases))), flush=True)


def replay_protocol():
    config = protocol()
    frozen = read(ROOT / 'replay-configuration.json')
    for path, expected in [(ROOT / 'replay239.py', frozen['script_sha256']),
        (ROOT / 'rational239.py', frozen['candidate_code_sha256']),
        (ROOT / 'results/points.json', frozen['point_report_sha256']),
        (Path(integration.__file__), frozen['inherited_integrator_sha256'])]:
        assert digest(path) == expected, path
    return config, frozen


def case_label(case):
    return f'{case["anchor"]}-a{case["angular_order"]}-r{case["ray"]:03d}'


def compare(case, arrays, reference, tolerance):
    checks, records = [], []
    assert set(arrays) == set(reference)
    for key in sorted(arrays):
        assert arrays[key].shape == reference[key].shape == (7, 98, 99)
        for state in range(7):
            expected, measured = reference[key][state], arrays[key][state]
            matrix_error = relative(measured, expected)
            gas_error = relative(measured[-1], expected[-1]) if ':l2:' not in key else 0.
            photon_error = relative(measured[:-1], expected[:-1])
            check(checks, f'{case_label(case)}:{key}:state{state}:full matrix', matrix_error, tolerance)
            check(checks, f'{case_label(case)}:{key}:state{state}:photon rows', photon_error, tolerance)
            check(checks, f'{case_label(case)}:{key}:state{state}:independent gas row', gas_error, tolerance)
            if ':l2:' not in key:
                scale = max(np.linalg.norm(measured[0]) + np.linalg.norm(measured[-1]), 1e-300)
                exchange = float(np.linalg.norm(measured[0] + measured[-1]) / scale)
                check(checks, f'{case_label(case)}:{key}:state{state}:independent four-force', exchange)
            records.append(dict(key=key, state=state, matrix=matrix_error, photon=photon_error, gas=gas_error))
        for first, second in ((1, 2), (2, 3), (4, 5), (5, 6)):
            expected = reference[key][second] - reference[key][first]
            measured = arrays[key][second] - arrays[key][first]
            error = relative(measured, expected)
            gas_error = relative(measured[-1], expected[-1]) if ':l2:' not in key else 0.
            check(checks, f'{case_label(case)}:{key}:history{first}-to{second}:cancelled increment', error, tolerance)
            check(checks, f'{case_label(case)}:{key}:history{first}-to{second}:cancelled gas', gas_error, tolerance)
            records.append(dict(key=key, state=f'{first}-to{second}', matrix=error, photon=0., gas=gas_error))
    return checks, records


def run(order):
    modest()
    config, frozen = replay_protocol()
    retained_config = read(REFERENCE / 'configuration.json')
    original, features, models = integration.setup(retained_config)
    candidate_globals = dict(integration.ray_integral.__globals__)
    candidate_globals['Direction'] = RationalDirection
    candidate = types.FunctionType(integration.ray_integral.__code__, candidate_globals, 'exact_rational_ray_integral',
        integration.ray_integral.__defaults__, integration.ray_integral.__closure__)
    assert integration.ray_integral.__globals__['Direction'] is Direction
    inputs = read(ROOT / 'replay-inputs.json')
    modules(inputs)
    for case in frozen['cases']:
        if case['angular_order'] != order:
            continue
        stem = ROOT / 'replay' / case_label(case)
        if stem.with_suffix('.json').exists():
            result = read(stem.with_suffix('.json'))
            assert result['configuration_sha256'] == digest(ROOT / 'replay-configuration.json')
            assert result['sha256'] == digest(stem.with_suffix('.npz'))
            continue
        assert not stem.with_suffix('.npz').exists()
        if time.time() > datetime.fromisoformat(START).timestamp() + 3.7 * 3600:
            print(json.dumps(dict(safe_stop=True, next_case=case_label(case))), flush=True)
            return
        event = next(row for row in config['events'] if row['label'] == case['anchor'])
        local = dict(retained_config, angular_order=order)
        with mp.workdps(frozen['digits']):
            arrays, metadata = candidate(local, event, case['radial_order'], case['ray'], original, features, models)
        assert integration.ray_integral.__globals__['Direction'] is Direction
        assert all(np.all(np.isfinite(value)) for value in arrays.values())
        reference = packet(Path(case['reference_stem']).with_suffix('.npz'))
        checks, records = compare(case, arrays, reference, frozen['replay_tolerance'])
        check(checks, case_label(case) + ':same event count', abs(metadata['evaluated_events'] - case['evaluated_events']), 0)
        failed = [entry for entry in checks if not entry['passed']]
        save(stem.with_suffix('.npz'), **arrays)
        write(stem.with_suffix('.json'), dict(**case, **metadata, checks=checks, failed=failed, qualified=not failed,
            records=records, sha256=digest(stem.with_suffix('.npz')), configuration_sha256=digest(ROOT / 'replay-configuration.json'),
            old_walltime_over_new=case['old_seconds'] / metadata['seconds'],
            timing_note='Historical reference wall time, not a simultaneous controlled full-ray benchmark', finished_at=now()))
        print(json.dumps(dict(case=case_label(case), seconds=metadata['seconds'], checks=len(checks), failures=len(failed),
            maximum_matrix=max(row['matrix'] for row in records), maximum_gas=max(row['gas'] for row in records))), flush=True)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    write(ROOT / 'replay' / f'inputs-angular{order}.json', inputs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['freeze', 'run'])
    parser.add_argument('--order', type=int, choices=[6, 8], default=6)
    arguments = parser.parse_args()
    freeze() if arguments.mode == 'freeze' else run(arguments.order)
