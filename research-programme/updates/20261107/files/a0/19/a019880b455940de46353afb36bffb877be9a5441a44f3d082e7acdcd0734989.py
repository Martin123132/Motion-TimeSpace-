from factors236 import *
import argparse
from datetime import timedelta


def contract(left, right):
    return np.einsum('nai,nvbi->vab', left, right, optimize=True)


def paired(left_base, emission, absorption, reference, density_sum, density_difference, density_residual):
    left_even = (emission[0] + absorption[0]) * .5
    left_odd = (emission[0] - absorption[0]) * .5
    right_even = (emission[1] + absorption[1]) * .5
    right_odd = (emission[1] - absorption[1]) * .5
    scale = lambda value: value[:, None, None, None]
    average = reference + right_even
    result = contract(left_even, scale(density_sum) * average + scale(density_difference) * right_odd)
    result += contract(left_odd, scale(density_sum) * right_odd + scale(density_difference) * average)
    right_sum = np.sum(scale(density_residual) * reference + scale(density_sum) * right_even + scale(density_difference) * right_odd, axis=0)
    result += np.einsum('ai,vbi->vab', left_base, right_sum, optimize=True)
    return result


def upper_limits(owner):
    ratio = owner.doppler / owner.hard_doppler
    mixed = 1 - mp.fsum(owner.hard_direction[axis] * owner.direction[axis] for axis in range(3))
    middle = 1 + owner.energy * (1 - owner.direction[2]) + ratio * (1 + owner.energy * (1 - owner.cosine))
    emission = 2 * owner.energy / (middle + mp.sqrt(middle**2 - 4 * ratio * mixed * owner.energy))
    absorption = scalar(owner.parameters['lab_energy']) / owner.doppler
    local_temperature = owner.temperature / owner.doppler
    return emission, absorption, local_temperature


def freeze():
    config = protocol()
    assert read(ROOT / 'results/density-pilot.json')['qualified']
    assert read(ROOT / 'results/factor-pilot.json')['qualified']
    assert read(ROOT / 'results/integrand-pilot.json')['qualified']
    path = ROOT / 'integration-configuration.json'
    assert not path.exists()
    write(path, dict(frozen_at=now(), files={name: digest(ROOT / name) for name in
        ('density236.py', 'factors236.py', 'integrate236.py')},
        pilot_hashes={name: digest(ROOT / 'results' / name) for name in ('density-pilot.json', 'factor-pilot.json', 'integrand-pilot.json')},
        orders=config['radial_orders'], angular_order=config['angular_order'], digits=config['arbitrary_precision_digits'],
        profiles=[None, .2, .5], separator_fractions=[1., .5],
        finite_domain=config['spectral_domain'], maximum_log_width=config['maximum_log_width'],
        original_bank_changed=False, original_tolerances_changed=False,
        compound_rule='Original log-panel width and Gauss orders on the union of original spontaneous/thermal boundaries',
        response_scope='Full98 photon plus gas, equilibrium and six mixed histories; l0/1/2; three original x14,event0 anchors'))
    print('Integration algorithm and controls frozen.', flush=True)


def run_protocol():
    config = protocol()
    frozen = read(ROOT / 'integration-configuration.json')
    for name, expected in frozen['files'].items():
        assert digest(ROOT / name) == expected, name
    for name, expected in frozen['pilot_hashes'].items():
        assert digest(ROOT / 'results' / name) == expected, name
    return config, frozen


def panels(owner, order, config):
    emission, absorption, local_temperature = upper_limits(owner)
    emission_x, absorption_x = float(emission / local_temperature), float(absorption / local_temperature)
    floor, ceiling = config['spectral_domain']
    assert floor < emission_x < absorption_x < ceiling
    boundaries = sorted({floor, ceiling, emission_x, absorption_x, .1, .5, 1., 2., 5., 10., 20., 40.})
    gauss, weights = np.polynomial.legendre.leggauss(order)
    for left, right in zip(boundaries[:-1], boundaries[1:]):
        count = max(1, math.ceil(math.log(right / left) / config['maximum_log_width']))
        edges = np.linspace(math.log(left), math.log(right), count + 1)
        for lower, upper in zip(edges[:-1], edges[1:]):
            half, middle = (upper - lower) / 2, (upper + lower) / 2
            frequency = np.exp(middle + half * gauss)
            yield frequency, half * weights * frequency, right <= emission_x * (1 + 1e-14), right <= absorption_x * (1 + 1e-14)


def reference_only(factors, frequency, degree, join):
    basis = factors.features.evaluate(frequency, join)
    potential = precise.stable_dot(basis, factors.high, factors.low)
    occupation = 1 / np.expm1(frequency)
    coupling = 2 * occupation * (1 + occupation) / (1 + 2 * occupation)
    harmonic = factors.harmonics[degree][2]
    wave = np.concatenate([basis[:, :, None] * harmonic, np.zeros((len(frequency), 1, len(harmonic)))], axis=1)
    result = np.broadcast_to(np.array(factors.right[join, degree]), (len(frequency), 7, 99, len(harmonic))).copy()
    for state in range(1, 7):
        result[:, state] += (coupling * potential[:, state - 1])[:, None, None] * factors.right[join, degree][0]
        result[:, state] += (coupling * float(factors.coefficients[join][state]['density']))[:, None, None] * wave
    return result


def ray_integral(config, row, order, ray_index, original, features, models):
    started = time.monotonic()
    parameters, event_weight = source.physics.parameters_and_weight(row['theta'], row['node'])
    direction, angular_weight = list(angular.inherited.source.angular_nodes(config['angular_order']))[ray_index]
    owner = Direction(precise_context(parameters), direction)
    factors = Factors(owner, features, models[0]['difference'].tests, config['states'], config['heat'])
    emission_upper, absorption_upper, local_temperature = upper_limits(owner)
    output = {(mode, join, degree): np.zeros((7, 98, 99)) for mode in ('control', 'difference') for join in (0, 1) for degree in (0, 1, 2)}
    compensation = {key: np.zeros_like(value) for key, value in output.items()}
    event_count, panel_count, maximum_null = 0, 0, 0.
    for frequency, measure, emission_allowed, absorption_allowed in panels(owner, order, config):
        soft = [scalar(value) * local_temperature for value in frequency]
        occupation = [1 / mp.expm1(scalar(value)) for value in frequency]
        densities, events, factors_data = {}, {}, {}
        for sign, allowed in ((1, emission_allowed), (-1, absorption_allowed)):
            if allowed:
                values = [owner.densities(sign * value) for value in soft]
                densities[sign] = [value[0] for value in values]
                events[sign] = [value[1] for value in values]
                factors_data[sign] = factors.evaluate(soft, events[sign], sign)
                event_count += len(soft)
                for degree in (0, 1):
                    left = factors.left[degree][None] + factors_data[sign][degree, 'left_delta']
                    maximum_null = max(maximum_null, float(np.max(np.linalg.norm(left[:, 0] + left[:, -1], axis=1)
                        / np.maximum(np.linalg.norm(left[:, 0], axis=1) + np.linalg.norm(left[:, -1], axis=1), 1e-300))))
        for mode in ('control', 'difference'):
            pole = owner.pole[mode]
            if emission_allowed and absorption_allowed:
                sums = [(1 + population) * positive[mode] + population * negative[mode] for population, positive, negative in zip(occupation, densities[1], densities[-1])]
                differences = [(1 + population) * positive[mode] - population * negative[mode] for population, positive, negative in zip(occupation, densities[1], densities[-1])]
                residuals = [value - pole * (1 + 2 * population) / energy for value, population, energy in zip(sums, occupation, soft)]
                rho_sum, rho_diff, rho_residual = [measure * float(local_temperature) * np.array(list(map(float, value))) for value in (sums, differences, residuals)]
            for join in (0, 1):
                for degree in (0, 1, 2):
                    left_base = factors.left[degree]
                    if emission_allowed and absorption_allowed:
                        reference = factors_data[1][join, degree, 'reference']
                        result = paired(left_base,
                            (factors_data[1][degree, 'left_delta'], factors_data[1][join, degree, 'right_delta']),
                            (factors_data[-1][degree, 'left_delta'], factors_data[-1][join, degree, 'right_delta']),
                            reference, rho_sum, rho_diff, rho_residual)
                    else:
                        reference = factors_data[-1][join, degree, 'reference'] if absorption_allowed else reference_only(factors, frequency, degree, join)
                        subtracted = np.array([float(-pole * (1 + 2 * population) / energy) for population, energy in zip(occupation, soft)])
                        reference_sum = np.einsum('n,nvbi->vbi', measure * float(local_temperature) * subtracted, reference)
                        result = np.einsum('ai,vbi->vab', left_base, reference_sum, optimize=True)
                        restore = float(pole) * np.sum(measure / frequency)
                        result += restore * np.einsum('ai,vbi->vab', left_base, np.array(factors.right[join, degree]), optimize=True)
                        if absorption_allowed:
                            weighted_density = measure * float(local_temperature) * np.array([float(population * value[mode]) for population, value in zip(occupation, densities[-1])])
                            left = left_base[None] + factors_data[-1][degree, 'left_delta']
                            right = reference + factors_data[-1][join, degree, 'right_delta']
                            result += contract(left, weighted_density[:, None, None, None] * right)
                    result *= .5 * event_weight * angular_weight / (2 * degree + 1)
                    key = mode, join, degree
                    corrected = result - compensation[key]
                    new = output[key] + corrected
                    compensation[key] = (new - output[key]) - corrected
                    output[key] = new
        panel_count += 1
    arrays = {}
    for (mode, join, degree), values in output.items():
        logarithm = .5 * event_weight * angular_weight * float(owner.pole[mode] * mp.log(2 * emission_upper))
        logarithm *= 1 / (2 * degree + 1)
        logarithm = logarithm * np.einsum('ai,vbi->vab', factors.left[degree], np.array(factors.right[join, degree]), optimize=True)
        prefix = f'{mode}:join{join}:l{degree}'
        arrays[prefix + ':finite'] = values
        arrays[prefix + ':logarithm'] = logarithm
        arrays[prefix + ':total'] = values + logarithm
    return arrays, dict(seconds=time.monotonic() - started, panels=panel_count, evaluated_events=event_count,
        maximum_independent_four_force_residual=maximum_null, emission_upper=float(emission_upper), absorption_upper=float(absorption_upper),
        event_weight=event_weight, angular_weight=angular_weight)


def run(anchor, order, first, count, deadline):
    modest()
    config, frozen = run_protocol()
    assert order in frozen['orders']
    original, features, models = setup(config)
    row = next(value for value in config['events'] if value['label'] == anchor)
    end = len(list(angular.inherited.source.angular_nodes(config['angular_order'])))
    for ray in range(first, min(end, first + count)):
        stem = ROOT / 'rays' / anchor / f'order{order}' / f'ray-{ray:02d}'
        if stem.with_suffix('.json').exists():
            previous = read(stem.with_suffix('.json'))
            assert previous['configuration_sha256'] == digest(ROOT / 'integration-configuration.json')
            assert previous['sha256'] == digest(stem.with_suffix('.npz'))
            print(json.dumps(dict(reused=anchor, order=order, ray=ray)), flush=True)
            continue
        assert not stem.with_suffix('.npz').exists(), 'Unsealed output: inspect rather than overwrite'
        if datetime.now().timestamp() >= deadline:
            print(json.dumps(dict(safe_stop=True, next_ray=ray, anchor=anchor, order=order)), flush=True)
            return
        with mp.workdps(frozen['digits']):
            arrays, metadata = ray_integral(config, row, order, ray, original, features, models)
        assert all(np.all(np.isfinite(value)) for value in arrays.values())
        save(stem.with_suffix('.npz'), **arrays)
        write(stem.with_suffix('.json'), dict(anchor=anchor, order=order, ray=ray, **metadata,
            sha256=digest(stem.with_suffix('.npz')), configuration_sha256=digest(ROOT / 'integration-configuration.json'), finished_at=now()))
        print(json.dumps(dict(saved=anchor, order=order, ray=ray, **metadata)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['freeze', 'run'])
    parser.add_argument('--anchor', default='warm')
    parser.add_argument('--order', type=int, default=18)
    parser.add_argument('--first', type=int, default=0)
    parser.add_argument('--count', type=int, default=32)
    parser.add_argument('--minutes', type=float, default=180)
    arguments = parser.parse_args()
    if arguments.mode == 'freeze':
        freeze()
    else:
        run(arguments.anchor, arguments.order, arguments.first, arguments.count, time.time() + arguments.minutes * 60)
