from integrate236 import *


def main():
    modest()
    config = protocol()
    original, features, models = setup(config)
    row = config['events'][0]
    parameters, weight = source.physics.parameters_and_weight(row['theta'], row['node'])
    checks = []
    records = []
    with mp.workdps(80):
        owner = Direction(precise_context(parameters), list(angular.inherited.source.angular_nodes(4))[11][0])
        factors = Factors(owner, features, models[0]['difference'].tests, config['states'], config['heat'])
        frequencies = [1.2e-6, 1e-4, .01, 1., 3.]
        soft = [scalar(value) * owner.temperature / owner.doppler for value in frequencies]
        occupation = [1 / mp.expm1(scalar(value)) for value in frequencies]
        densities, data = {}, {}
        for sign in (1, -1):
            samples = [owner.densities(sign * value) for value in soft]
            densities[sign] = [value[0] for value in samples]
            data[sign] = factors.evaluate(soft, [value[1] for value in samples], sign)
        for mode in ('control', 'difference'):
            pole = owner.pole[mode]
            sums = [(1 + population) * positive[mode] + population * negative[mode] for population, positive, negative in zip(occupation, densities[1], densities[-1])]
            differences = [(1 + population) * positive[mode] - population * negative[mode] for population, positive, negative in zip(occupation, densities[1], densities[-1])]
            residuals = [value - pole * (1 + 2 * population) / energy for value, population, energy in zip(sums, occupation, soft)]
            for join in (0, 1):
                for degree in (0, 1, 2):
                    left = factors.left[degree]
                    reference = data[1][join, degree, 'reference']
                    for index, frequency in enumerate(frequencies):
                        measured = paired(left, (data[1][degree, 'left_delta'][index:index+1], data[1][join, degree, 'right_delta'][index:index+1]),
                            (data[-1][degree, 'left_delta'][index:index+1], data[-1][join, degree, 'right_delta'][index:index+1]),
                            reference[index:index+1], np.array([float(sums[index])]), np.array([float(differences[index])]), np.array([float(residuals[index])]))
                        for state in (0, 1, 4):
                            expected, actual = [], []
                            for out_coordinate in (0, 1, 2, 15, 97):
                                for in_coordinate in (0, 1, 30, 96, 98):
                                    result = mp.mpf(0)
                                    for harmonic in range(left.shape[-1]):
                                        base = scalar(left[out_coordinate, harmonic])
                                        ref = scalar(reference[index, state, in_coordinate, harmonic])
                                        result -= pole * (1 + 2 * occupation[index]) / soft[index] * base * ref
                                        for sign in (1, -1):
                                            amplitude = densities[sign][index][mode] * (occupation[index] + int(sign == 1))
                                            real_left = base + scalar(data[sign][degree, 'left_delta'][index, out_coordinate, harmonic])
                                            real_right = ref + scalar(data[sign][join, degree, 'right_delta'][index, state, in_coordinate, harmonic])
                                            result += amplitude * real_left * real_right
                                    expected.append(result)
                                    actual.append(scalar(measured[state, out_coordinate, in_coordinate]))
                            error = prior.mp_relative(actual, expected)
                            check(checks, f'{mode}:join{join}:l{degree}:state{state}:x{frequency}:direct80-digit subtracted product', error)
                            records.append(dict(mode=mode, join=join, degree=degree, state=state, frequency=frequency, error=error))
    failures = [row for row in checks if not row['passed']]
    write(ROOT / 'results/integrand-pilot.json', dict(qualified=not failures, checks=checks, failed=failures, records=records,
        code_hashes={name: digest(ROOT / name) for name in ('factors236.py', 'integrate236.py', 'test_integrand236.py')}, finished_at=now()))
    print(json.dumps(dict(checks=len(checks), failed=len(failures), maximum=max(row['value'] for row in checks), examples=failures[:8])), flush=True)
    assert not failures


if __name__ == '__main__':
    main()
