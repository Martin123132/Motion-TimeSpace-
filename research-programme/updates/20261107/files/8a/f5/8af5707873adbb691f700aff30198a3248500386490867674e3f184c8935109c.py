import argparse
from observer_common import *
from consistent_system import ConsistentSystem
from compare_extended_readout import load_projection
from spectral_readout import SpectralReadout, spectral_norm


def band_rows(basis, order, centres):
    nodes, weights = np.polynomial.legendre.leggauss(order)
    rows = []
    for centre in centres:
        frequencies = centre * np.exp(.08 * nodes)
        occupation = 1 / np.expm1(frequencies)
        rows.append((weights / 2 * frequencies ** 3 * occupation * (1 + occupation)) @ basis.evaluate(frequencies))
    return np.asarray(rows)


def main(arguments):
    modest()
    folder = ROOT / 'results' / ('coherent' + str(arguments.count) + '-over' + str(arguments.coarse))
    folder.mkdir(parents=True, exist_ok=False)
    checks, rows, inputs = [], [], []
    centres = np.array([.03, .1, .3, 1., 3., 8.])
    for model in ['heavy', 'cold']:
        system = ConsistentSystem(model, arguments.count)
        times, baseline, correction, source = load_projection(system, ROOT / 'waves' / (model + str(arguments.count) + '-3200') / 'evolution.npz')
        inputs.extend(source)
        total = baseline + correction
        coarse_times, coarse_base, coarse_correction, source = load_projection(system, ROOT / 'waves' / (model + str(arguments.coarse) + '-3200') / 'evolution.npz')
        inputs.extend(source)
        assert np.max(abs(times - coarse_times)) < 1e-12
        coarse = coarse_base + coarse_correction
        baseline_norm = float(np.max(spectral_norm(baseline[:, 0], system.basis.mass)))
        total_norm = float(np.max(spectral_norm(total[:, 0], system.basis.mass)))
        inner = np.einsum('ti,ij,tj->', baseline[:, 0].conj(), system.basis.mass, correction[:, 0]).real
        base_power = np.einsum('ti,ij,tj->', baseline[:, 0].conj(), system.basis.mass, baseline[:, 0]).real
        correction_power = np.einsum('ti,ij,tj->', correction[:, 0].conj(), system.basis.mass, correction[:, 0]).real
        rows.append(dict(model=model, baseline_shape_norm=baseline_norm, total_shape_norm=total_norm,
                         remaining_fraction=total_norm / baseline_norm, spectral_mass_weighted_overlap=float(inner / np.sqrt(base_power * correction_power))))
        bands20, bands40 = [band_rows(system.basis, order, centres) for order in [20, 40]]
        fine_bands = total[:, 0] @ bands40.T
        coarse_bands = coarse[:, 0] @ bands40.T
        integration_bands = total[:, 0] @ bands20.T
        np.savez_compressed(folder / (model + '-total.npz'), expansion=times, baseline=baseline,
                            correction=correction, total=total, ideal_band_x=centres,
                            ideal_total_band_shape=fine_bands, ideal_coarse_band_shape=coarse_bands)
        for mode, label in [(0, '0I'), (2, '1I'), (4, '2I'), (5, '2E')]:
            norm = float(np.max(spectral_norm(total[:, mode], system.basis.mass)))
            error = float(np.max(spectral_norm(coarse[:, mode] - total[:, mode], system.basis.mass)))
            relative = error / norm
            checks.append(dict(name=model + ': total physical shape resolution ' + label, passed=relative < .002, value=relative))
            number_error = float(np.max(abs(total[:, mode] @ system.basis.number))) / norm
            checks.append(dict(name=model + ': total shape retains number-free split ' + label, passed=number_error < 1e-8, value=number_error))
        for index, centre in enumerate(centres):
            scale = float(np.max(abs(fine_bands[:, index])))
            quadrature_error = float(np.max(abs(integration_bands[:, index] - fine_bands[:, index]))) / scale
            response_error = float(np.max(abs(coarse_bands[:, index] - fine_bands[:, index]))) / scale
            checks.append(dict(name=model + ': ideal band integration20-to40 at x=' + str(centre), passed=quadrature_error < .002, value=quadrature_error))
            checks.append(dict(name=model + ': total ideal band response refinement at x=' + str(centre), passed=response_error < .002, value=response_error))
            rows.append(dict(model=model, ideal_band_x=float(centre), response_error=response_error, integration_error=quadrature_error))
        readout = SpectralReadout(system)
        for point in [0., 1., 2.1]:
            background = readout.background(point)
            weak = system.redshift_weak @ background['profile'] - background['boundary']
            strong = system.basis.mass @ background['dilation_change']
            error = float(linalg.norm(weak - strong) / max(linalg.norm(strong), 1e-100))
            checks.append(dict(name=model + ': refined strong-weak dilation with boundary at ' + str(point), passed=error < 1e-7, value=error))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
                        gate=.002, common_readout_basis=arguments.count, coarse_basis=arguments.coarse, physical_background_basis=24,
                        ideal_bands_are_comoving_log_frequency_not_instrument_bandpasses=True,
                        unchanged_physical_parameters=True,
                        scope='Conditional early-time coherent readout on the saved24-function no-emission background; numerical convergence does not bound omitted physical effects.'), __file__,
           [ROOT / 'consistent_system.py', ROOT / 'extended_system.py', ROOT / 'consistent_spectral_basis.py',
            ROOT / 'compare_extended_readout.py', ROOT / 'verify_total_response.py', ROOT / 'spectral_readout.py', *sorted(set(inputs))])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']],
                          cancellation=[row for row in rows if 'remaining_fraction' in row])), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', type=int, default=32)
    parser.add_argument('--coarse', type=int, default=28)
    main(parser.parse_args())
