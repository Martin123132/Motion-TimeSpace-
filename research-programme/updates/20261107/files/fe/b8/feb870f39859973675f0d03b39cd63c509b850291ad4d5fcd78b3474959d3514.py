from observer_common import *
from consistent_system import ConsistentSystem
from compare_extended_readout import load_projection
from compare_consistent_readout import band_rows
from spectral_readout import spectral_norm


def main():
    modest()
    folder = ROOT / 'results/refined-time36'
    folder.mkdir(parents=True, exist_ok=False)
    checks, inputs, rows = [], [], []
    centres = np.array([.03, .1, .3, 1., 3., 8.])
    for model in ['heavy', 'cold']:
        system = ConsistentSystem(model, 36)
        times, baseline, correction, source = load_projection(system, ROOT / 'waves' / (model + '36-6400') / 'evolution.npz')
        inputs.extend(source)
        coarse_times, coarse_baseline, coarse_correction, source = load_projection(system, ROOT / 'waves' / (model + '36-3200') / 'evolution.npz')
        inputs.extend(source)
        assert np.max(abs(times - coarse_times)) < 1e-12
        total, coarse = baseline + correction, coarse_baseline + coarse_correction
        baseline_norm = float(np.max(spectral_norm(baseline[:, 0], system.basis.mass)))
        total_norm = float(np.max(spectral_norm(total[:, 0], system.basis.mass)))
        rows.append(dict(model=model, baseline_shape_norm=baseline_norm, total_shape_norm=total_norm,
                         remaining_fraction=total_norm / baseline_norm))
        for mode, label in [(0, '0I'), (2, '1I'), (4, '2I'), (5, '2E')]:
            norm = float(np.max(spectral_norm(total[:, mode], system.basis.mass)))
            error = float(np.max(spectral_norm(coarse[:, mode] - total[:, mode], system.basis.mass))) / norm
            checks.append(dict(name=model + ':3200-to6400 steps total shape ' + label, passed=error < .002, value=error))
        bands = band_rows(system.basis, 40, centres)
        fine_bands, coarse_bands = total[:, 0] @ bands.T, coarse[:, 0] @ bands.T
        for index, centre in enumerate(centres):
            error = float(np.max(abs(fine_bands[:, index] - coarse_bands[:, index])) / np.max(abs(fine_bands[:, index])))
            checks.append(dict(name=model + ':3200-to6400 steps total ideal band x=' + str(centre), passed=error < .002, value=error))
        np.savez_compressed(folder / (model + '-total.npz'), expansion=times, baseline=baseline,
                            correction=correction, total=total, ideal_band_x=centres, ideal_total_band_shape=fine_bands)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
                        unchanged_gate=.002, basis_count=36, physical_background_basis=24,
                        failed_1600_to3200_ideal_band_comparison_retained=True), __file__,
           [ROOT / 'consistent_system.py', ROOT / 'consistent_spectral_basis.py', ROOT / 'extended_system.py',
            ROOT / 'compare_extended_readout.py', ROOT / 'compare_consistent_readout.py',
            ROOT / 'verify_total_response.py', ROOT / 'spectral_readout.py', *sorted(set(inputs))])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], maximum=max(row['value'] for row in checks), rows=rows)), flush=True)


if __name__ == '__main__':
    main()
