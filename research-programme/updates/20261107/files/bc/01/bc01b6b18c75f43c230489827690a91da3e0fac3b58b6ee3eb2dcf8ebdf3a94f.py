import argparse
from emission_angular_common import *


def load_history(folder, old=False):
    packet = json.loads((folder / 'status.json').read_text())
    assert packet['all_checks_passed']
    with np.load(folder / 'history.npz') as saved:
        if old:
            data = dict(expansion=saved['history'][:, 0].copy(), profiles=saved['profiles'].copy(),
                        temperature_scaled=saved['history'][:, 2].copy(), heat=float(saved['heat']))
        else:
            data = {key: saved[key].copy() for key in saved.files}
    return ConsistentBasis(**packet['basis_spec']), data, [folder / 'status.json', folder / 'history.npz']


def main(arguments):
    modest()
    folder = ROOT / 'results' / arguments.name
    folder.mkdir(parents=True, exist_ok=False)
    frequency, measure = thermal_wave.frequency_quadrature(1000)
    nodes, weights = np.polynomial.legendre.leggauss(40)
    checks, rows, inputs = [], [], []
    for model in ['heavy', 'cold']:
        basis, fine, sources = load_history(ROOT / 'backgrounds' / (model + '-reaction104-6400'))
        inputs.extend(sources)
        old = arguments.compare == 'old-soft'
        target = PARENT / 'density' / (model + '-tangent104-6400') if old else ROOT / 'backgrounds' / (model + '-' + arguments.compare)
        other_basis, other, sources = load_history(target, old)
        inputs.extend(sources)
        times = other['expansion']
        fine_profile = interpolate.CubicSpline(fine['expansion'], fine['profiles'])(times)
        fine_temperature = interpolate.CubicSpline(fine['expansion'], fine['temperature_scaled'])(times)
        fine_values = fine_profile @ basis.evaluate(frequency).T
        other_values = other['profiles'] @ other_basis.evaluate(frequency).T
        def relative(values, reference):
            return float(np.max(np.sqrt(np.sum(measure * abs(values - reference) ** 2, axis=-1))) /
                         np.max(np.sqrt(np.sum(measure * abs(reference) ** 2, axis=-1))))
        measures = dict(spectrum=relative(other_values, fine_values))
        fine_shape = fine_values - (fine_values @ measure / (measure @ frequency))[:, None] * frequency
        other_shape = other_values - (other_values @ measure / (measure @ frequency))[:, None] * frequency
        measures['shape'] = relative(other_shape, fine_shape)
        measures['gas'] = float(np.max(abs(other['temperature_scaled'] - fine_temperature)) / np.max(abs(fine_temperature)))
        for name, row, other_row in [('energy', basis.energy, other_basis.energy), ('number', basis.number, other_basis.number)]:
            reference, compared = fine_profile @ row, other['profiles'] @ other_row
            measures[name] = float(np.max(abs(compared - reference)) / np.max(abs(reference)))
        for centre in [.001, .003, .01, .03, .1, .3, 1., 3., 8.]:
            coordinate = centre * np.exp(.08 * nodes)
            planck = 1 / np.expm1(coordinate)
            band_weight = weights / 2 * coordinate ** 3 * planck * (1 + planck)
            reference = fine_profile @ (band_weight @ basis.evaluate(coordinate))
            compared = other['profiles'] @ (band_weight @ other_basis.evaluate(coordinate))
            measures['band_' + str(centre)] = float(np.max(abs(compared - reference)) / np.max(abs(reference)))
        if arguments.refinement:
            checks.extend(check(model + ' refinement ' + name, value, .002) for name, value in measures.items())
        else:
            checks.append(dict(name=model + ' diagnostic differences finite', passed=all(np.isfinite(list(measures.values())))))
        number_factor = math.pi ** 4 / (30 * special.zeta(3))
        rows.append(dict(model=model, measures=measures,
            new_energy_fraction=float(fine['heat'] * basis.energy @ fine_profile[-1]),
            compared_energy_fraction=float(other['heat'] * other_basis.energy @ other['profiles'][-1]),
            new_number_fraction=float(fine['heat'] * number_factor * basis.number @ fine_profile[-1]),
            compared_number_fraction=float(other['heat'] * number_factor * other_basis.number @ other['profiles'][-1]),
            new_gas_fraction=float(fine['heat'] * fine_temperature[-1]),
            compared_gas_fraction=float(other['heat'] * other['temperature_scaled'][-1])))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
        rows=rows, refinement_gate=arguments.refinement, compared=arguments.compare,
        first_nonzero_tested_expansion=float(times[1]), initial_stiff_layer_resolved_pointwise=False,
        maximum=max(max(row['measures'].values()) for row in rows)), __file__, inputs)
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], rows=rows)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--compare', required=True)
    parser.add_argument('--name', required=True)
    parser.add_argument('--refinement', action='store_true')
    main(parser.parse_args())
