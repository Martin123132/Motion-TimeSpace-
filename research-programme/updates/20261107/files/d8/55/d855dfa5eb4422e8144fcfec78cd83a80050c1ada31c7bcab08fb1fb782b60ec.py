import argparse
from emission_common import *


def load(name):
    path = ROOT / 'backgrounds' / name / 'history.npz'
    packet = json.loads((path.parent / 'status.json').read_text())
    assert packet['all_checks_passed'], path
    specification = packet.get('basis_spec', dict(count=packet['basis_count']))
    basis = ConsistentBasis(**specification)
    with np.load(path) as saved:
        data = {key: saved[key].copy() for key in saved.files}
    return basis, data, packet, [path, path.parent / 'status.json']


def main(arguments):
    modest()
    folder = ROOT / 'results' / arguments.name
    folder.mkdir(parents=True, exist_ok=False)
    fine_basis, fine, fine_packet, inputs = load(arguments.fine)
    coarse_basis, coarse, coarse_packet, extra = load(arguments.coarse)
    assert fine_packet['model'] == coarse_packet['model'] and fine_packet['emission'] == coarse_packet['emission']
    inputs.extend(extra)
    times = np.r_[0., np.linspace(.02, float(fine['expansion'][-1]), 151)]
    frequency, measure = thermal_wave.frequency_quadrature(900)
    fine_coefficients = interpolate.CubicSpline(fine['expansion'], fine['profiles'])(times)
    coarse_coefficients = interpolate.CubicSpline(coarse['expansion'], coarse['profiles'])(times)
    fine_spectrum = fine_coefficients @ fine_basis.evaluate(frequency).T
    coarse_spectrum = coarse_coefficients @ coarse_basis.evaluate(frequency).T
    denominator = measure @ frequency
    fine_shape = fine_spectrum - np.outer(fine_spectrum @ measure / denominator, frequency)
    coarse_shape = coarse_spectrum - np.outer(coarse_spectrum @ measure / denominator, frequency)
    checks = []
    def check(name, error):
        checks.append(dict(name=name, passed=error < .002, value=float(error)))
    def relative(numerator, reference):
        return np.max(np.sqrt(np.sum(measure * abs(numerator) ** 2, axis=-1))) / np.max(np.sqrt(np.sum(measure * abs(reference) ** 2, axis=-1)))
    check('Physical total background spectral refinement', relative(coarse_spectrum - fine_spectrum, fine_spectrum))
    check('Temperature-removed background shape refinement', relative(coarse_shape - fine_shape, fine_shape))
    for key in ['temperature_scaled', 'number_scaled']:
        fine_values = interpolate.CubicSpline(fine['expansion'], fine[key])(times)
        coarse_values = interpolate.CubicSpline(coarse['expansion'], coarse[key])(times)
        check(key + ' refinement', np.max(abs(coarse_values - fine_values)) / max(np.max(abs(fine_values)), 1e-6))
    centres = np.array([.001, .003, .01, .03, .1, .3, 1., 3., 8.])
    band_points, band_weights = np.polynomial.legendre.leggauss(40)
    band_fine, band_coarse = [], []
    for centre in centres:
        frequencies = centre * np.exp(.08 * band_points)
        occupation = 1 / np.expm1(frequencies)
        weights = band_weights / 2 * frequencies ** 3 * occupation * (1 + occupation)
        values_fine = fine_coefficients @ (weights @ fine_basis.evaluate(frequencies))
        values_coarse = coarse_coefficients @ (weights @ coarse_basis.evaluate(frequencies))
        check('Physical background ideal band x=' + str(centre), np.max(abs(values_fine - values_coarse)) / np.max(abs(values_fine)))
        band_fine.append(values_fine)
        band_coarse.append(values_coarse)
    np.savez_compressed(folder / 'comparison.npz', expansion=times, frequency=frequency,
        fine_shape=fine_shape, coarse_shape=coarse_shape, centres=centres,
        fine_bands=band_fine, coarse_bands=band_coarse)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
        fine=arguments.fine, coarse=arguments.coarse, gate=.002,
        initial_very_fast_electron_layer_not_time_resolved=True, first_nonzero_tested_expansion=.02),
        __file__, [OBSERVER / 'consistent_spectral_basis.py', *inputs])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], maximum=max(row['value'] for row in checks))), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fine', required=True)
    parser.add_argument('--coarse', required=True)
    parser.add_argument('--name', required=True)
    main(parser.parse_args())
