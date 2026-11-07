from common234 import *
import argparse
import medium233


def basis_mp(spline, frequency):
    coordinate = mp.log(frequency)
    index = min(max(int(np.searchsorted(spline.x, float(coordinate))) - 1, 0), len(spline.x) - 2)
    delta = coordinate - scalar(spline.x[index])
    values, derivatives = [], []
    for column in range(98):
        coefficients = [scalar(spline.c[power, index, column]) for power in range(4)]
        values.append(((coefficients[0] * delta + coefficients[1]) * delta + coefficients[2]) * delta + coefficients[3])
        derivatives.append((3 * coefficients[0] * delta**2 + 2 * coefficients[1] * delta + coefficients[2]) / frequency)
    return values + [frequency], derivatives + [mp.mpf(1)]


def numerator_mp(spline, frequency, derivative=False):
    values, slopes = basis_mp(spline, frequency)
    occupation = 1 / mp.expm1(frequency)
    weight = occupation * (1 + occupation)
    if derivative:
        return [weight * ((1 - frequency * (1 + 2 * occupation)) * value + frequency * slope) for value, slope in zip(values, slopes)]
    return [frequency * weight * value for value in values]


def grid(features, join, order):
    spline = features.splines[join]
    points, gauss_weights = np.polynomial.legendre.leggauss(order)
    lower, upper = spline.x[:-1], spline.x[1:]
    log_frequency = ((lower + upper)[:, None] + (upper - lower)[:, None] * points) / 2
    frequency = np.exp(log_frequency).ravel()
    weights = (((upper - lower)[:, None] * gauss_weights / 2).ravel()) * frequency
    values = np.column_stack([features.evaluate(frequency, join), frequency])
    occupation_weight = np.exp(-frequency) / (-np.expm1(-frequency))**2
    numerator = (frequency * occupation_weight)[:, None] * values
    return frequency, weights, numerator


def pole_integral(spline, frequency, weights, numerator, location, sign):
    pole = float(location)
    with mp.workdps(80):
        exact_location = scalar(pole)
        exact_numerator = numerator_mp(spline, exact_location)
        at_pole = np.array(list(map(float, exact_numerator)))
        occupation = 1 / mp.expm1(exact_location)
        exact_basis, unused = basis_mp(spline, exact_location)
        imaginary = np.array([float(-mp.pi * sign * occupation * (1 + occupation) * value / 2) for value in exact_basis])
        close = np.flatnonzero(abs(frequency - pole) <= 1e-5 * max(1., abs(pole)))
        divided = (numerator - at_pole[None, :]) / (frequency - pole)[:, None]
        for index in close:
            sample = scalar(frequency[index])
            if sample == exact_location:
                values = numerator_mp(spline, exact_location, True)
            else:
                current = numerator_mp(spline, sample)
                values = [(value - before) / (sample - exact_location) for value, before in zip(current, exact_numerator)]
            divided[index] = list(map(float, values))
    divided -= numerator / (frequency + pole)[:, None]
    lower, upper = np.exp(spline.x[0]), np.exp(spline.x[-1])
    assert lower < pole < upper
    real = (weights @ divided + at_pole * np.log((upper - pole) / (pole - lower))) / (2 * pole)
    return real + 1j * imaginary, len(close)


def thermal_exterior(lower, upper, location=None):
    with mp.workdps(80):
        lower, upper = scalar(lower), scalar(upper)
        def numerator(value):
            return mp.mpf(1) if value == 0 else value**2 / (4 * mp.sinh(value / 2)**2)
        if location is None:
            integrand = numerator
        else:
            pole = scalar(location)
            integrand = lambda value: numerator(value) / (value**2 - pole**2)
        return mp.quad(integrand, [0, lower]) + mp.quad(integrand, [upper, upper + 20, mp.inf])


def freeze():
    config = protocol()
    assert not (ROOT / 'radial-configuration.json').exists()
    tensor_hashes = {}
    for row in config['events']:
        path = ROOT / 'tensors' / (row['label'] + '.json')
        report = read(path)
        assert report['qualified']
        tensor_hashes[row['label']] = digest(path)
    write(ROOT / 'radial-configuration.json', dict(frozen_at=now(), script_sha256=digest(Path(__file__)),
        tensor_hashes=tensor_hashes, refinement_orders=config['radial_orders'], interval=config['spectral_domain'],
        unknown_exterior_contribution='explicit additional constant/pole functionals; never evaluated as zero',
        thermal_control_exterior='only h=x has its known analytic tails added'))
    print('Full spectral radial protocol frozen.', flush=True)


def radial_protocol():
    config = protocol()
    frozen = read(ROOT / 'radial-configuration.json')
    assert digest(Path(__file__)) == frozen['script_sha256']
    for label, expected in frozen['tensor_hashes'].items():
        assert digest(ROOT / 'tensors' / (label + '.json')) == expected
    return config, frozen


def run():
    modest()
    config, frozen = radial_protocol()
    original, features, models = setup(config)
    tensor_reports = [read(ROOT / 'tensors' / (row['label'] + '.json')) for row in config['events']]
    for join in config['joins']:
        for order in config['radial_orders']:
            destination = ROOT / 'radial' / f'join{join}-order{order}.npz'
            if destination.exists():
                existing = read(destination.with_suffix('.json'))
                assert existing['qualified'] and digest(destination) == existing['sha256']
                continue
            began = time.monotonic()
            frequency, weights, numerator = grid(features, join, order)
            constant = weights @ numerator
            values = np.empty((3, 8, 2, 99), dtype=complex)
            locations = np.empty((3, 8, 2))
            signs = np.empty((3, 8, 2), dtype=int)
            checks, corrected_count = [], 0
            with mp.workdps(80):
                expected = mp.pi**2 / 3
                measured = scalar(constant[-1]) + thermal_exterior(*config['spectral_domain'])
                check(checks, 'thermal constant moment including known exterior', abs(measured / expected - 1))
            for anchor, report in enumerate(tensor_reports):
                temperature = config['events'][anchor]['theta']
                for ray_index, ray in enumerate(report['rays']):
                    poles = ray['polarizations'][0]['poles']
                    assert all([pole['location'] for pole in entry['poles']] == [pole['location'] for pole in poles] for entry in ray['polarizations'])
                    for pole_index, pole in enumerate(poles):
                        with mp.workdps(80):
                            location = float(mp.mpf(pole['location']) * mp.mpf(ray['doppler']) / scalar(temperature))
                        locations[anchor, ray_index, pole_index] = location
                        signs[anchor, ray_index, pole_index] = pole['sign']
                        integral, close = pole_integral(features.splines[join], frequency, weights, numerator, location, pole['sign'])
                        corrected_count += close
                        values[anchor, ray_index, pole_index] = integral
                        with mp.workdps(80):
                            scaled = scalar(location)
                            occupation = 1 / mp.expm1(scaled)
                            expected = medium233.temperature_derivative(scaled) - mp.j * mp.pi * pole['sign'] * scaled * occupation * (1 + occupation) / 2
                            measured = mp.mpc(integral[-1]) + thermal_exterior(*config['spectral_domain'], location)
                            check(checks, f'{report["label"]}:ray{ray_index}:pole{pole_index}:thermal response including known exterior', abs(measured - expected) / abs(expected))
            save(destination, constant=constant, poles=values, locations=locations, signs=signs,
                spectral_domain=np.array(config['spectral_domain']), order=order, join=join)
            failed = [row for row in checks if not row['passed']]
            report = dict(state='complete', qualified=not failed, checks=checks, failed=failed, sha256=digest(destination),
                seconds=time.monotonic() - began, close_differences_at80digits=corrected_count,
                original_cells=config['spline_grid_cells'], quadrature_nodes=len(frequency), finished_at=now())
            write(destination.with_suffix('.json'), report)
            print(json.dumps(dict(join=join, order=order, checks=len(checks), failed=failed, seconds=report['seconds'], near_pole_mp=corrected_count)), flush=True)
            assert not failed, failed


def assess():
    config, frozen = radial_protocol()
    checks, records = [], []
    for join in config['joins']:
        coarse = packet(ROOT / 'radial' / f'join{join}-order4.npz')
        fine = packet(ROOT / 'radial' / f'join{join}-order6.npz')
        for name in ('constant', 'poles'):
            first, second = coarse[name][..., :98], fine[name][..., :98]
            difference = np.linalg.norm(first - second, axis=-1) / np.maximum(np.linalg.norm(second, axis=-1), 1e-300)
            check(checks, f'join{join}:{name}:full98 coordinate norm refinement', np.max(difference), .002)
            column_error = abs(first - second) / np.maximum(abs(second), 1e-300)
            records.append(dict(join=join, component=name, maximum_vector_norm_change=float(np.max(difference)),
                maximum_column_relative_change=float(np.max(column_error)),
                absolute_difference=float(np.max(abs(first - second))), norm_convention='Euclidean in frozen98 coefficient coordinates; not a basis-independent physical bound'))
    report = dict(state='complete', qualified=all(row['passed'] for row in checks), checks=checks,
        failed=[row for row in checks if not row['passed']], records=records, finished_at=now())
    write(ROOT / 'results/radial-assessment.json', report)
    print(json.dumps(report), flush=True)
    assert not report['failed'], report['failed']


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['freeze', 'run', 'assess'])
    arguments = parser.parse_args()
    modest()
    {'freeze': freeze, 'run': run, 'assess': assess}[arguments.mode]()
