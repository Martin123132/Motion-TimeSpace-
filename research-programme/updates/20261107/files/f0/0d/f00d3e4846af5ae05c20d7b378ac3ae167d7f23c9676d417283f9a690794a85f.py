from compare_density_response import load_packet
from wave_common import *
from infrared_ladder import InfraredLadder


def main():
    modest()
    folder = ROOT / 'results/density-basis-comparison'
    folder.mkdir(parents=True, exist_ok=False)
    fine_basis = InfraredLadder(PARENT / 'banks/infrared96-q700').basis
    coarse_basis = InfraredLadder(PARENT / 'banks/infrared88-q700').basis
    frequency, measure = thermal_wave.frequency_quadrature(900)
    checks, inputs = [], [ROOT / 'compare_density_response.py']
    for model in ['heavy', 'cold']:
        fine = load_packet(model + '-tangent-6400')
        coarse = load_packet(model + '-tangent88-6400')
        fine_values = fine['responses'] @ fine_basis.evaluate(frequency).T
        coarse_values = coarse['responses'] @ coarse_basis.evaluate(frequency).T
        def relative(values, reference):
            return np.max(np.sqrt(np.sum(measure * abs(values - reference) ** 2, axis=-1))) / np.max(np.sqrt(np.sum(measure * abs(reference) ** 2, axis=-1)))
        checks.append(check(model + ' density response spectral basis88-to96', relative(coarse_values, fine_values), .002))
        fine_shape = fine_values - (fine_values @ measure / (measure @ frequency))[:, None] * frequency
        coarse_shape = coarse_values - (coarse_values @ measure / (measure @ frequency))[:, None] * frequency
        checks.append(check(model + ' density response temperature-removed basis88-to96', relative(coarse_shape, fine_shape), .002))
        for column, name in [(7, 'gas'), (9, 'number')]:
            error = np.max(abs(coarse['history'][:, column] - fine['history'][:, column])) / np.max(abs(fine['history'][:, column]))
            checks.append(check(model + ' density response ' + name + ' basis88-to96', error, .002))
        nodes, weights = np.polynomial.legendre.leggauss(40)
        for centre in [.001, .003, .01, .03, .1, .3, 1., 3., 8.]:
            coordinate = centre * np.exp(.08 * nodes)
            planck = 1 / np.expm1(coordinate)
            band_weight = weights / 2 * coordinate ** 3 * planck * (1 + planck)
            fine_band = fine['responses'] @ (band_weight @ fine_basis.evaluate(coordinate))
            coarse_band = coarse['responses'] @ (band_weight @ coarse_basis.evaluate(coordinate))
            error = np.max(abs(coarse_band - fine_band)) / np.max(abs(fine_band))
            checks.append(check(model + ' density response band x=' + str(centre), error, .002))
        for name in [model + '-tangent-6400', model + '-tangent88-6400']:
            inputs.extend([ROOT / 'density' / name / 'history.npz', ROOT / 'density' / name / 'status.json'])
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
        maximum=max(row['value'] for row in checks), initial_electron_fast_layer_resolved=False,
        first_nonzero_tested_expansion=float(fine['history'][1, 0]),
        independent_emission_quadrature_not_retested_here=True), __file__, inputs)
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']],
                         maximum=max(row['value'] for row in checks))), flush=True)


if __name__ == '__main__':
    main()
