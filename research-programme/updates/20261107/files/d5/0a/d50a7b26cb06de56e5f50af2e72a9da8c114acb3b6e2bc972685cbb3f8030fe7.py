from factors236 import *


def exact_projection(factors, event, join, degree, state_index):
    owner = factors.owner
    soft_x = abs(event['soft']) * owner.doppler / owner.temperature
    hard_x = event['hard'] * owner.hard_doppler / owner.temperature
    frequencies = [factors.event['frequencies'][0], hard_x, soft_x]
    basis = factors.features.evaluate(np.array(list(map(float, frequencies))), join)
    tests = factors.tests.evaluate(np.array(list(map(float, frequencies))))
    transfer = owner.transform * mp.matrix([event['kinetic'], *event['recoil']])
    current = dict(factors.event, frequencies=frequencies, signs=[-1, 1, 1 if event['soft'] > 0 else -1],
        electron_transfer=list(transfer), directions=factors.directions.tolist())
    if state_index == 0:
        coefficients = equilibrium(current)
    else:
        potential = [state235.contraction(line, factors.physical[state_index - 1][:98]) for line in basis]
        coefficients = statistics(current, potential, factors.gas[state_index - 1])['mixed']
    return projected(current, tests, basis, coefficients, degree)


def main():
    modest()
    config = protocol()
    original, features, models = setup(config)
    checks = []
    nodes = list(angular.inherited.source.angular_nodes(4))
    started = time.monotonic()
    with mp.workdps(80):
        for row in config['events']:
            parameters, weight = source.physics.parameters_and_weight(row['theta'], row['node'])
            refined = precise_context(parameters)
            check(checks, row['label'] + ':same physical energy', abs(float(refined['energy']) / parameters['energy'] - 1))
            check(checks, row['label'] + ':same physical transform', relative(np.array(refined['transform'], dtype=float), parameters['transform']))
            for ray_index in (0, 11):
                owner = Direction(refined, nodes[ray_index][0])
                factors = Factors(owner, features, models[0]['difference'].tests, config['states'], config['heat'])
                frequencies = [1.2e-6, 1e-4, .01, 1., 3.]
                soft_values = [scalar(value) * owner.temperature / owner.doppler for value in frequencies]
                values = {}
                for sign in (-1, 1):
                    events = [owner.event(sign * value) for value in soft_values]
                    data = factors.evaluate(soft_values, events, sign)
                    values[sign] = data
                    for index, event in enumerate(events):
                        for degree in (0, 1, 2):
                            left = factors.left[degree] + data[degree, 'left_delta'][index]
                            if degree < 2:
                                residual = np.linalg.norm(left[0] + left[-1]) / max(np.linalg.norm(left[0]) + np.linalg.norm(left[-1]), 1e-300)
                                check(checks, f'{row["label"]}:ray{ray_index}:x{frequencies[index]}:sign{sign}:l{degree}:independent four-force', residual)
                            for join in (0, 1):
                                for state_index in (0, 1, 4):
                                    right = data[join, degree, 'reference'][index, state_index] + data[join, degree, 'right_delta'][index, state_index]
                                    actual = left @ right.T / (2 * degree + 1)
                                    expected, unused, reference_left, reference_right = exact_projection(factors, event, join, degree, state_index)
                                    prefix = f'{row["label"]}:ray{ray_index}:x{frequencies[index]}:sign{sign}:join{join}:state{state_index}:l{degree}'
                                    check(checks, prefix + ':independent complete vertex', relative(actual, np.asarray(expected, dtype=float)))
                                    check(checks, prefix + ':right factor', relative(right, reference_right))
                for join in (0, 1):
                    for degree in (0, 1, 2):
                        check(checks, f'{row["label"]}:ray{ray_index}:join{join}:l{degree}:shared reference',
                            relative(values[1][join, degree, 'reference'], values[-1][join, degree, 'reference']))
            print(json.dumps(dict(anchor=row['label'], checks=len(checks), failed=sum(not row['passed'] for row in checks))), flush=True)
    failures = [row for row in checks if not row['passed']]
    write(ROOT / 'results/factor-pilot.json', dict(qualified=not failures, checks=checks, failed=failures,
        script_hashes={name: digest(ROOT / name) for name in ('factors236.py', 'test_factors236.py')},
        elapsed_seconds=time.monotonic() - started, finished_at=now()))
    print(json.dumps(dict(checks=len(checks), failed=len(failures), examples=failures[:8])), flush=True)
    assert not failures


if __name__ == '__main__':
    main()
