from observer_common import *
from consistent_system import ConsistentSystem
from spectral_readout import SpectralReadout
from compare_consistent_readout import band_rows
import mpmath as mp


def precise_shape(readout, expansion, state):
    background = readout.background(expansion)
    heat = mp.mpf(background['heat'])
    basis = readout.basis
    dilation = [mp.mpf(base) + heat * mp.mpf(change) for base, change in zip(basis.temperature, background['dilation_change'])]
    age = [heat * mp.mpf(value) - tangent for value, tangent in zip(background['profile_prime'], dilation)]
    density = mp.mpc(complex(state[8])) - mp.mpc(complex(state[0])) - mp.mpc(complex(state[1])) / 2
    coefficients = [mp.mpc(complex(value)) + tangent * density / 3 for value, tangent in zip(state[readout.system.mode_slice(0)], age)]
    number = [mp.mpf(value) for value in basis.number]
    temperature = mp.fsum(moment * value for moment, value in zip(number, coefficients)) / mp.fsum(moment * value for moment, value in zip(number, dilation))
    shape = [value - tangent * temperature for value, tangent in zip(coefficients, dilation)]
    residual = abs(mp.fsum(moment * value for moment, value in zip(number, shape)))
    return np.array([complex(value) for value in shape]), float(residual)


def main():
    modest()
    mp.mp.dps = 70
    folder = ROOT / 'results/band-precision-diagnostic'
    folder.mkdir(parents=True, exist_ok=False)
    checks, rows, inputs = [], [], []
    for model in ['heavy', 'cold']:
        system = ConsistentSystem(model, 36)
        readout = SpectralReadout(system)
        band = band_rows(system.basis, 40, [1.])[0]
        outputs, original, shapes = {}, {}, {}
        for steps in [3200, 6400]:
            source = ROOT / 'waves' / (model + '36-' + str(steps)) / 'evolution.npz'
            packet = json.loads((source.parent / 'status.json').read_text())
            assert packet['all_checks_passed']
            inputs.extend([source, source.parent / 'status.json'])
            with np.load(source) as saved:
                times = saved['expansion'].copy()
                heat = float(saved['heat'])
                computed, float_readout = [], []
                maximum_number = 0.
                for point, base, delta in zip(times, saved['baseline_states'], saved['scaled_differences']):
                    base_shape, base_residual = precise_shape(readout, point, base)
                    delta_shape, delta_residual = precise_shape(readout, point, delta)
                    computed.append(base_shape + heat * delta_shape)
                    float_readout.append(readout.apply(point, base)['shapes'][0] + heat * readout.apply(point, delta)['shapes'][0])
                    maximum_number = max(maximum_number, base_residual, heat * delta_residual)
            shapes[steps] = np.asarray(computed)
            outputs[steps] = shapes[steps] @ band
            original[steps] = np.asarray(float_readout) @ band
            checks.append(dict(name=model + ':' + str(steps) + ':70-digit number-free projection identity', passed=maximum_number < 1e-55, value=maximum_number))
        difference = shapes[6400] - shapes[3200]
        band_difference = outputs[6400] - outputs[3200]
        scale = float(np.max(abs(outputs[6400])))
        gap = float(np.max(abs(band_difference)))
        projection_error = max(float(np.max(abs(outputs[steps] - original[steps]))) for steps in [3200, 6400])
        index = int(np.argmax(abs(band_difference)))
        first_energy_component = difference[index, 1] * band[1]
        rows.append(dict(model=model, high_precision_time_relative=gap / scale,
                         maximum_band_amplitude=scale, maximum_time_discrepancy=gap,
                         double_to_high_precision_readout_difference=projection_error,
                         readout_arithmetic_fraction_of_time_discrepancy=projection_error / gap,
                         maximum_difference_expansion=float(times[index]),
                         fraction_from_first_nonthermal_energy_component=float(abs(first_energy_component) / abs(band_difference[index])),
                         detailed_time_accuracy_closed=gap / scale < .002))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
                        scope='Localizes numerical discrepancy using70-digit readout arithmetic on unchanged saved double-precision states. It does not repair or certify the evolution.',
                        no_physical_state_replacement=True, no_tolerance_relaxed=True), __file__,
           [ROOT / 'spectral_readout.py', ROOT / 'consistent_system.py', ROOT / 'consistent_spectral_basis.py',
            ROOT / 'compare_consistent_readout.py', *sorted(set(inputs))])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], rows=rows)), flush=True)


if __name__ == '__main__':
    main()
