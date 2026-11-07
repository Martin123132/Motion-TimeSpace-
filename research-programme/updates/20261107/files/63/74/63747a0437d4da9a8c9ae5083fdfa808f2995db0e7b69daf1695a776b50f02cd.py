from scipy import interpolate
from step_common import *


FREQUENCY = np.geomspace(.01, 20., 240)
COSINE, ANGULAR_WEIGHTS = np.polynomial.legendre.leggauss(24)
ANGULAR_WEIGHTS /= 2


def sampled(packet):
    values = packet['spectrum_history']
    points = len(packet['frequency'])
    polar = len(packet['cosine'])
    values = values.reshape(len(values), points, 2, polar)
    vandermonde = np.polynomial.legendre.legvander(packet['cosine'], polar - 1)
    target = np.polynomial.legendre.legvander(COSINE, polar - 1)
    transform = target @ np.linalg.inv(vandermonde)
    angular = np.einsum('mn,txan->txam', transform, values)
    return interpolate.CubicSpline(np.log(packet['frequency']), angular, axis=1)(np.log(FREQUENCY))


def norms(values):
    occupation = 1 / np.expm1(FREQUENCY)
    physical = FREQUENCY ** 3 * occupation * (1 + occupation)
    angular = .5 * np.einsum('n,txan,txan->tx', ANGULAR_WEIGHTS, values.conj(), values).real
    return np.sqrt(np.maximum(np.trapezoid(angular * physical[None, :] ** 2, np.log(FREQUENCY), axis=1), 0))


def pair(label, suffix):
    warm_path = ROOT / 'runs' / (label + '-warm-' + suffix) / 'evolution.npz'
    cold_path = ROOT / 'runs' / (label + '-elastic-' + suffix) / 'evolution.npz'
    with np.load(warm_path, allow_pickle=False) as warm, np.load(cold_path, allow_pickle=False) as cold:
        assert np.max(abs(warm['optical_depth'] - cold['optical_depth'])) < 1e-12
        assert np.max(abs(warm['equilibrium'] - cold['equilibrium'])) == 0
        warm_values, cold_values = sampled(warm), sampled(cold)
        return warm_values - cold_values, cold_values, warm['optical_depth'].copy(), [warm_path, cold_path]


def main():
    modest()
    folder = ROOT / 'results/response-refinements'
    assert not folder.exists()
    checks, rows, inputs, packets = [], [], [], {}
    for label in ['heavy', 'cold']:
        for suffix in ['base', 'time', 'frequency', 'fine', 'angular']:
            response, control, times, paths = pair(label, suffix)
            inputs.extend(paths)
            packets[label + '-' + suffix] = (response, control, times)
        for name, previous, refined, gate in [('time', 'base', 'time', .002),
            ('frequency96/144', 'time', 'frequency', .002), ('frequency144/192', 'frequency', 'fine', .002),
            ('angular10/12', 'fine', 'angular', .001)]:
            first, _, old_times = packets[label + '-' + previous]
            second, _, new_times = packets[label + '-' + refined]
            assert np.max(abs(old_times - new_times)) < 1e-12
            residual = float(max(norms(first - second)) / max(norms(second)))
            checks.append(dict(name=label + ': ' + name + ' refinement of thermal-minus-elastic response itself',
                               passed=residual < gate, value=residual, gate=gate))
        response, control, times = packets[label + '-angular']
        signal = norms(response)
        initial = float(norms(control)[0])
        row = dict(model=label, peak_thermal_response_relative_initial_cold_defect=float(max(signal) / initial),
                   endpoint_thermal_response_relative_endpoint_cold_defect=float(signal[-1] / norms(control)[-1]),
                   peak_optical_depth=float(times[np.argmax(signal)]),
                   weighted_norm='L2 of x^3*w*potential over log(x) in[0.01,20] and angular Stokes trace norm',
                   source_step_not_accumulated_cosmological_error=True)
        rows.append(row)
    folder.mkdir(parents=True, exist_ok=False)
    for label in ['heavy', 'cold']:
        response, control, times = packets[label + '-angular']
        np.savez_compressed(folder / (label + '.npz'), frequency=FREQUENCY, cosine=COSINE, optical_depth=times,
                            response=response, cold_control_defect=control, response_norm=norms(response))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        rows=rows, refinement_is_on_small_correction_not_large_parent_state=True), __file__, inputs)
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], rows=rows)), flush=True)


if __name__ == '__main__':
    main()
