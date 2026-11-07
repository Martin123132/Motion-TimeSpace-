import argparse
from wave_common import *


def load_named(name):
    folder = ROOT / 'density' / name
    packet = json.loads((folder / 'status.json').read_text())
    assert packet['all_checks_passed']
    specification = packet.get('basis_spec', dict(count=96, quadrature=700, minimum=1e-5, maximum=60., pivot=.1))
    with np.load(folder / 'history.npz') as saved:
        data = {key: saved[key].copy() for key in saved.files}
    return ConsistentBasis(**specification), data, [folder / 'history.npz', folder / 'status.json']


def main(arguments):
    modest()
    folder = ROOT / 'results' / arguments.name
    folder.mkdir(parents=True, exist_ok=False)
    checks, inputs, rows = [], [], []
    frequency, measure = thermal_wave.frequency_quadrature(1000)
    for model in ['heavy', 'cold']:
        fine_basis, fine, dependencies = load_named(model + '-' + arguments.fine)
        inputs.extend(dependencies)
        coarse_basis, coarse, dependencies = load_named(model + '-' + arguments.coarse)
        inputs.extend(dependencies)
        times = fine['history'][:, 0]
        coarse_response = interpolate.CubicSpline(coarse['history'][:, 0], coarse['responses'])(times)
        fine_values = fine['responses'] @ fine_basis.evaluate(frequency).T
        coarse_values = coarse_response @ coarse_basis.evaluate(frequency).T
        def relative(values, reference):
            return np.max(np.sqrt(np.sum(measure * abs(values - reference) ** 2, axis=-1))) / np.max(np.sqrt(np.sum(measure * abs(reference) ** 2, axis=-1)))
        checks.append(check(model + ' density response total spectrum', relative(coarse_values, fine_values), .002))
        fine_shape = fine_values - (fine_values @ measure / (measure @ frequency))[:, None] * frequency
        coarse_shape = coarse_values - (coarse_values @ measure / (measure @ frequency))[:, None] * frequency
        checks.append(check(model + ' density response temperature-removed shape', relative(coarse_shape, fine_shape), .002))
        for column, name in [(7, 'gas'), (9, 'number')]:
            interpolated = interpolate.CubicSpline(coarse['history'][:, 0], coarse['history'][:, column])(times)
            error = np.max(abs(interpolated - fine['history'][:, column])) / np.max(abs(fine['history'][:, column]))
            checks.append(check(model + ' density response ' + name, error, .002))
        nodes, weights = np.polynomial.legendre.leggauss(40)
        for centre in [.001, .003, .01, .03, .1, .3, 1., 3., 8.]:
            coordinate = centre * np.exp(.08 * nodes)
            planck = 1 / np.expm1(coordinate)
            band_weight = weights / 2 * coordinate ** 3 * planck * (1 + planck)
            fine_band = fine['responses'] @ (band_weight @ fine_basis.evaluate(coordinate))
            coarse_band = coarse_response @ (band_weight @ coarse_basis.evaluate(coordinate))
            error = np.max(abs(coarse_band - fine_band)) / np.max(abs(fine_band))
            checks.append(check(model + ' density response band x=' + str(centre), error, .002))
        number_factor = math.pi ** 4 / (30 * special.zeta(3))
        rows.append(dict(model=model, fine=arguments.fine, coarse=arguments.coarse,
            final_energy_fraction_response=float(fine['heat'] * (fine_basis.energy @ fine['responses'][-1])),
            final_number_fraction_response=float(fine['heat'] * (fine_basis.number @ fine['responses'][-1]) * number_factor),
            final_gas_temperature_fraction_response=float(fine['heat'] * fine['history'][-1, 7])))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
        maximum=max(row['value'] for row in checks), initial_electron_fast_layer_resolved=False,
        first_nonzero_tested_expansion=float(times[1])), __file__, inputs)
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']],
                         maximum=max(row['value'] for row in checks), rows=rows)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fine', required=True)
    parser.add_argument('--coarse', required=True)
    parser.add_argument('--name', required=True)
    main(parser.parse_args())
