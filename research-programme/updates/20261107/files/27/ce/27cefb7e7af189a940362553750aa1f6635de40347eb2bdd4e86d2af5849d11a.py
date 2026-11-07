import argparse
from scaled_common import *
from scaled_system import ScaledSystem
from compare_scaled_waves import load_wave, band_rows
from verify_total_response import embed


def map_coordinates(fine, coarse, states):
    assert fine.heat == coarse.heat
    temperature = np.pad(coarse.temperature, (0, fine.count - coarse.count))
    assert np.array_equal(temperature, fine.temperature)
    padded_complement = np.pad(coarse.complement, ((0, fine.count - coarse.count), (0, 0)))
    thermal_shift = fine.number_row @ padded_complement
    shape_map = fine.shape_row @ padded_complement
    mapped = np.zeros((len(states), fine.size), complex)
    mapped[:, :11] = states[:, :11]
    mapped[:, fine.neutrino] = states[:, coarse.neutrino]
    for degree, names in enumerate(coarse.names):
        for name in names:
            source, target = coarse.mode_slice(degree, name), fine.mode_slice(degree, name)
            shapes = states[:, source.start + 1:source.stop]
            shift = shapes @ thermal_shift
            mapped[:, target.start] = states[:, source.start] + fine.heat * shift
            mapped[:, target.start + 1:target.stop] = shapes @ shape_map.T
            if degree == 0 and name == 'I':
                mapped[:, 10] -= shift
    return mapped


def main(arguments):
    modest()
    folder = ROOT / 'results' / ('basis' + str(arguments.fine) + '-over' + str(arguments.coarse) + '-' + str(arguments.steps))
    folder.mkdir(parents=True, exist_ok=False)
    checks, inputs, rows = [], [], []
    centres = np.array([.03, .1, .3, 1., 3., 8.])
    for model in ['heavy', 'cold']:
        fine_system, coarse_system = ScaledSystem(model, arguments.fine), ScaledSystem(model, arguments.coarse)
        fine, paths = load_wave(model, arguments.fine, arguments.steps)
        inputs.extend(paths)
        coarse, paths = load_wave(model, arguments.coarse, arguments.steps)
        inputs.extend(paths)
        assert np.max(abs(fine['expansion'] - coarse['expansion'])) < 1e-12
        coarse_states = coarse['baseline_coordinates'] + coarse['coordinate_differences']
        mapped = map_coordinates(fine_system, coarse_system, coarse_states)
        physical = np.array([coarse_system.physical_state(state) for state in coarse_states])
        target_physical = embed(fine_system.physical, physical, arguments.coarse)
        reconstructed = np.array([fine_system.physical_state(state) for state in mapped])
        error = float(np.max(abs(reconstructed - target_physical)))
        checks.append(dict(name=model + ': coordinate embedding preserves physical state', passed=error < 1e-14, value=error))
        coarse_shapes = np.array([fine_system.readout(expansion, state)['shapes'] for expansion, state in zip(fine['expansion'], mapped)])
        shapes = fine['full_shapes']
        for mode, label in [(0, '0I'), (2, '1I'), (4, '2I'), (5, '2E')]:
            scale = float(np.max(spectral_norm(shapes[:, mode], fine_system.basis.mass)))
            error = float(np.max(spectral_norm(shapes[:, mode] - coarse_shapes[:, mode], fine_system.basis.mass))) / scale
            checks.append(dict(name=model + ': directly evolved total shape basis refinement ' + label, passed=error < .002, value=error))
        fine_bands = shapes[:, 0] @ band_rows(fine_system.basis, 40, centres).T
        coarse_bands = coarse_shapes[:, 0] @ band_rows(fine_system.basis, 40, centres).T
        quadrature_bands = shapes[:, 0] @ band_rows(fine_system.basis, 20, centres).T
        for index, centre in enumerate(centres):
            scale = np.max(abs(fine_bands[:, index]))
            response_error = float(np.max(abs(fine_bands[:, index] - coarse_bands[:, index])) / scale)
            quadrature_error = float(np.max(abs(fine_bands[:, index] - quadrature_bands[:, index])) / scale)
            checks.extend([
                dict(name=model + ': directly evolved ideal band basis refinement x=' + str(centre), passed=response_error < .002, value=response_error),
                dict(name=model + ': direct ideal band quadrature20-to40 x=' + str(centre), passed=quadrature_error < .002, value=quadrature_error)])
            rows.append(dict(model=model, centre=float(centre), response_error=response_error, quadrature_error=quadrature_error))
        np.savez_compressed(folder / (model + '-readout.npz'), expansion=fine['expansion'], total_shapes=shapes,
                            embedded_coarse_shapes=coarse_shapes, ideal_band_x=centres, ideal_band_shape=fine_bands,
                            ideal_coarse_band_shape=coarse_bands)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
        unchanged_gate=.002, fine_basis=arguments.fine, coarse_basis=arguments.coarse, steps=arguments.steps,
        background_still24_function_no_emission=True, ideal_bands_not_instrument_responses=True,
        separate_refinement_checks_not_rigorous_aggregate_error_bound=True), __file__,
        [ROOT / 'scaled_system.py', ROOT / 'compare_scaled_waves.py', PARENT / 'verify_total_response.py', PARENT / 'compare_consistent_readout.py', *sorted(set(inputs))])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], rows=rows)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fine', type=int, default=36)
    parser.add_argument('--coarse', type=int, default=32)
    parser.add_argument('--steps', type=int, default=6400)
    main(parser.parse_args())
