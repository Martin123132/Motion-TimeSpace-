import argparse
from scaled_common import *
from scaled_system import ScaledSystem
from compare_consistent_readout import band_rows


def load_wave(model, count, steps):
    path = ROOT / 'waves' / (model + str(count) + '-' + str(steps)) / 'evolution.npz'
    packet = json.loads((path.parent / 'status.json').read_text())
    assert packet['all_checks_passed']
    with np.load(path) as saved:
        result = {key: saved[key].copy() for key in saved.files}
    return result, [path, path.parent / 'status.json']


def main(arguments):
    modest()
    folder = ROOT / 'results' / ('time' + str(arguments.fine) + '-over' + str(arguments.coarse))
    folder.mkdir(parents=True, exist_ok=False)
    checks, rows, inputs = [], [], []
    centres = np.array([.03, .1, .3, 1., 3., 8.])
    for model in ['heavy', 'cold']:
        system = ScaledSystem(model, arguments.count)
        fine, source = load_wave(model, arguments.count, arguments.fine)
        inputs.extend(source)
        coarse, source = load_wave(model, arguments.count, arguments.coarse)
        inputs.extend(source)
        assert np.max(abs(fine['expansion'] - coarse['expansion'])) < 1e-12
        shapes, coarse_shapes = fine['full_shapes'], coarse['full_shapes']
        bands = band_rows(system.basis, 40, centres)
        fine_bands, coarse_bands = shapes[:, 0] @ bands.T, coarse_shapes[:, 0] @ bands.T
        for mode, label in [(0, '0I'), (2, '1I'), (4, '2I'), (5, '2E')]:
            norm = float(np.max(spectral_norm(shapes[:, mode], system.basis.mass)))
            error = float(np.max(spectral_norm(shapes[:, mode] - coarse_shapes[:, mode], system.basis.mass))) / norm
            checks.append(dict(name=model + ': total shape time refinement ' + label, passed=error < .002, value=error))
        for index, centre in enumerate(centres):
            error = float(np.max(abs(fine_bands[:, index] - coarse_bands[:, index])) / np.max(abs(fine_bands[:, index])))
            checks.append(dict(name=model + ': total ideal band time refinement x=' + str(centre), passed=error < .002, value=error))
        total_norm = float(np.max(spectral_norm(shapes[:, 0], system.basis.mass)))
        base_norm = float(np.max(spectral_norm(fine['baseline_shapes'][:, 0], system.basis.mass)))
        rows.append(dict(model=model, total_shape_norm=total_norm, baseline_shape_norm=base_norm,
                         remaining_fraction=total_norm / base_norm))
        np.savez_compressed(folder / (model + '-readout.npz'), expansion=fine['expansion'], total_shapes=shapes,
                            ideal_band_x=centres, ideal_band_shape=fine_bands)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
                        unchanged_gate=.002, count_basis=arguments.count, fine_steps=arguments.fine, coarse_steps=arguments.coarse,
                        background_still24_function_no_emission=True), __file__,
           [ROOT / 'scaled_system.py', PARENT / 'compare_consistent_readout.py', *sorted(set(inputs))])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], maximum=max(row['value'] for row in checks), rows=rows)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', type=int, default=36)
    parser.add_argument('--fine', type=int, default=3200)
    parser.add_argument('--coarse', type=int, default=1600)
    main(parser.parse_args())
