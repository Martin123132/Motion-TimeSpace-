from wave_common import *


def load_packet(name):
    path = ROOT / 'density' / name
    packet = json.loads((path / 'status.json').read_text())
    assert packet['all_checks_passed'] and (path / 'COMPLETE').is_file()
    for source, expected in packet['input_hashes'].items():
        assert digest(source) == expected, source
    with np.load(path / 'history.npz') as saved:
        return {key: saved[key].copy() for key in saved.files}


def norm(values, mass):
    return np.sqrt(np.maximum(0., np.einsum('...i,ij,...j->...', values, mass, values)))


def relative(values, reference, mass=None):
    numerator = np.max(abs(values - reference)) if mass is None else np.max(norm(values - reference, mass))
    denominator = np.max(abs(reference)) if mass is None else np.max(norm(reference, mass))
    return float(numerator / max(denominator, 1e-30))


def main():
    modest()
    folder = ROOT / 'results/density-comparison'
    folder.mkdir(parents=True, exist_ok=False)
    checks, rows, inputs = [], [], [ROOT / 'density_tangent.py']
    for model in ['heavy', 'cold']:
        base = load_packet(model + '-tangent-6400')
        low = load_packet(model + '-tangent-3200')
        negative = load_packet(model + '-omit-ion-6400')
        mass = base['mass']
        source = PARENT / 'backgrounds' / (model + '-ir96-integrated-6400') / 'history.npz'
        with np.load(source) as parent:
            selected = np.rint(base['history'][:, 0] / parent['expansion'][-1] * 6400).astype(int)
            parent_profile = parent['profiles'][selected]
            parent_temperature = parent['temperature_scaled'][selected]
        checks += [check(model + ' exactly retained parent trajectory', relative(base['profiles'], parent_profile, mass), 1e-7),
                   check(model + ' exactly retained parent gas history', relative(base['history'][:, 2], parent_temperature), 1e-7),
                   check(model + ' tangent time refinement3200-to6400', relative(low['responses'], base['responses'], mass), .002)]
        finite_differences = {}
        for epsilon in [.002, .001]:
            plus = load_packet(model + '-plus-' + str(epsilon) + '-6400')
            minus = load_packet(model + '-minus-' + str(epsilon) + '-6400')
            response = ((1 + epsilon) * plus['profiles'] - (1 - epsilon) * minus['profiles']) / (2 * epsilon)
            gas = ((1 + epsilon) * plus['history'][:, 2] - (1 - epsilon) * minus['history'][:, 2]) / (2 * epsilon)
            error = relative(response, base['responses'], mass)
            gas_error = relative(gas, base['history'][:, 7])
            checks += [check(model + ' independent finite-density photon derivative ' + str(epsilon), error, .002),
                       check(model + ' independent finite-density gas derivative ' + str(epsilon), gas_error, .002)]
            finite_differences[epsilon] = response
            rows.append(dict(model=model, epsilon=epsilon, spectral_derivative_relative_error=error,
                             gas_derivative_relative_error=gas_error))
        refinement = relative(finite_differences[.002], finite_differences[.001], mass)
        checks.append(check(model + ' finite-density step refinement', refinement, .002))
        final = finite_differences[.001]
        good = relative(base['responses'], final, mass)
        bad = relative(negative['responses'], final, mass)
        checks.append(dict(name=model + ' missing-ion negative control rejected', passed=bad > max(10 * good, 1e-6),
                           missing_ion_error=bad, derived_error=good))
        number = base['responses'] @ base['number']
        energy = base['responses'] @ base['energy']
        shape = base['responses'] - (number / (base['number'] @ base['temperature_template']))[:, None] * base['temperature_template']
        checks.append(dict(name=model + ' physical density response changes photon number', passed=abs(float(number[-1])) > 1e-6,
                           final_number_moment_per_unit_density=float(number[-1])))
        number_factor = math.pi ** 4 / (30 * special.zeta(3))
        rows.append(dict(model=model, final_energy_fraction_response=float(base['heat'] * energy[-1]),
            final_photon_number_fraction_response=float(base['heat'] * number[-1] * number_factor),
            final_gas_temperature_fraction_response=float(base['heat'] * base['history'][-1, 7]),
            final_number_removed_shape_norm=float(base['heat'] * norm(shape[-1], mass)),
            density_definition='Derivative with respect to fractional fully-ionized baryon density at fixed reference expansion and fixed H/He composition.',
            missing_ion_error=bad, derived_error=good, step_refinement=refinement))
        np.savez_compressed(folder / (model + '-comparison.npz'), expansion=base['history'][:, 0],
                            analytic=base['responses'], finite_difference=final, missing_ion=negative['responses'],
                            number_moment=number, energy_moment=energy, number_removed_shape=shape)
        inputs.append(source)
    for path in sorted((ROOT / 'density').glob('*/history.npz')):
        inputs.extend([path, path.parent / 'status.json'])
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
        rows=rows, full_finite_wavenumber_evolution=False,
        interpretation='New solved emitting-background density tangent, checked against separately evolved positive/negative density histories in both parent models.'), __file__, inputs)
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], rows=rows)), flush=True)


if __name__ == '__main__':
    main()
