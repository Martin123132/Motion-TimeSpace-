from run233 import *


def spline_value(features, frequency, join, coefficients):
    spline = features.splines[join]
    coordinate = mp.log(frequency)
    index = min(max(int(np.searchsorted(spline.x, float(coordinate))) - 1, 0), len(spline.x) - 2)
    delta = coordinate - scalar(spline.x[index])
    values = []
    for column in range(98):
        value = scalar(spline.c[0, index, column])
        for order in (1, 2, 3):
            value = value * delta + scalar(spline.c[order, index, column])
        values.append(value)
    return mp.fsum(value * coefficient for value, coefficient in zip(values, coefficients))


def main():
    modest()
    config, frozen = run_protocol()
    path = ROOT / 'results/tail-boost.json'
    assert not path.exists()
    write(ROOT / 'tail-boost-configuration.json', dict(frozen_at=now(), script_sha256=digest(Path(__file__)),
        soft_frequencies=[1.01e-6, 7.5e-5, 1.5e-4], angular_direction_index=11, directions_tested=[1, -1], tolerance=1e-10,
        reason='Exercise both actual tail columns and joins, and independently test the nonzero common boost instead of only high-frequency vertices'))
    original, features, models = setup(config)
    checks, records = [], []
    axis = np.array([.3, -.4, np.sqrt(.75)])
    with mp.workdps(80):
        for row in config['events']:
            parameters, unused = source.physics.parameters_and_weight(row['theta'], row['node'])
            direction, unused = list(angular.inherited.source.angular_nodes(4))[11]
            doppler = angular.inherited.source.dot(parameters['bath'], np.r_[1., direction])
            cases = [('born', geometry(parameters))]
            for sign in (1, -1):
                for frequency in (1.01e-6, 7.5e-5, 1.5e-4):
                    cases.append((f'soft{sign}:{frequency}', geometry(parameters, sign * frequency * row['theta'] / doppler, direction)))
            for tag, event in cases:
                frequencies = np.array(event['frequencies'])
                tests = models[0]['difference'].tests.evaluate(frequencies)
                for join in config['joins']:
                    feature_values = features.evaluate(frequencies, join)
                    feature_slopes = features.evaluate(frequencies, join, True)
                    for state in [item for item in config['states'] if item['history'] == 'quarter']:
                        coefficients = list(map(mp.mpf, state['coefficients']))
                        heat = scalar(config['heat'])
                        potential = [heat * mp.fsum(scalar(value) * coefficient for value, coefficient in zip(line, coefficients[:98])) for line in feature_values]
                        slopes = [heat * mp.fsum(scalar(value) * coefficient for value, coefficient in zip(line, coefficients[:98])) for line in feature_slopes]
                        gas = heat * coefficients[-1]
                        stats = statistics(event, potential, gas)
                        prefix = f'{row["label"]}:{tag}:{state["model"]}:join{join}'
                        derivative_checks(event, potential, gas, stats, checks, prefix, frozen)
                        for degree in (0, 1, 2):
                            matrix, unused, unused, unused = projected(event, tests, feature_values, stats['mixed'], degree)
                            check(checks, prefix + f':l{degree}:all columns finite', int(not np.isfinite(matrix).all()), 0)
                            if degree < 2:
                                check(checks, prefix + f':l{degree}:independent four-force', np.linalg.norm(matrix[0] + matrix[-1]) / max(np.linalg.norm(matrix[0]) + np.linalg.norm(matrix[-1]), 1e-300))
                        cosine = np.array(event['directions']) @ axis
                        photon_boost = [scalar(frequency) * (1 + (1 + 2 * occupation) * value - slope) * scalar(angle)
                            for frequency, occupation, value, slope, angle in zip(frequencies, stats['occupations'], potential, slopes, cosine)]
                        expected = scalar_product(stats['exact'], photon_boost, mp.mpf(0), list(map(scalar, axis)), mp.mpf(0))
                        def transformed(speed):
                            gamma = 1 / mp.sqrt(1 - speed**2)
                            shifted = []
                            for frequency, angle in zip(frequencies, cosine):
                                reference = 1 / mp.expm1(scalar(frequency))
                                shifted_x = gamma * scalar(frequency) * (1 - speed * scalar(angle))
                                occupation = 1 / mp.expm1(shifted_x)
                                occupation += occupation * (1 + occupation) * heat * spline_value(features, shifted_x, join, coefficients[:98])
                                shifted.append((occupation - reference) / (reference * (1 + reference)))
                            return raw_flux(event, shifted, gas, [speed * scalar(value) for value in axis])
                        step = mp.mpf('1e-20')
                        measured = (transformed(step) - transformed(-step)) / (2 * step)
                        check(checks, prefix + ':actual boosted spectrum derivative', abs(measured - expected) / max(abs(expected), mp.mpf('1e-300')))
                        if tag != 'born' and frequencies[-1] < 1e-4:
                            column = 96 + int(state['model'] == 'cold')
                            check(checks, prefix + ':physical tail coordinate exercised', int(not np.any(abs(feature_values[:, column]) > 0)), 0)
                        records.append(dict(anchor=row['label'], event=tag, model=state['model'], join=join,
                            minimum_frequency=float(min(frequencies)), common_boost_response=float(expected),
                            boost_derivative_error=float(abs(measured - expected) / max(abs(expected), mp.mpf('1e-300'))),
                            tail_columns=list(map(float, np.linalg.norm(feature_values[:, 96:98], axis=0)))))
    failed = [row for row in checks if not row['passed']]
    write(path, dict(state='complete', checks=checks, failed=failed, records=records, qualified=not failed, finished_at=now(),
        zero_floor_extension=False, below_saved_domain_value_assumed=False))
    print(json.dumps(dict(tail_boost_checks=len(checks), failed=failed, largest_boost_error=max(row['boost_derivative_error'] for row in records))), flush=True)
    assert not failed, failed


if __name__ == '__main__':
    main()
