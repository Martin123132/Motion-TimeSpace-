import argparse
from thermal_wave_common import *
from stable_spectral_basis import load_basis
sys.path.insert(0, str(PARENT))
from cold_control import exact_cold


def propagate(stiffness, mass, basis, degree, capacity, initial, times):
    modes = len(stiffness) // basis.count
    metric = linalg.block_diag(*([mass] * modes))
    null_columns = []
    if degree in [0, 1]:
        equilibrium = np.r_[basis.temperature, np.zeros((modes - 1) * basis.count)]
        coupling = np.column_stack([np.eye(len(stiffness)), -equilibrium])
        full = coupling.T @ stiffness @ coupling
        metric = linalg.block_diag(metric, capacity)
        null_columns.append(np.r_[equilibrium, 1.])
        if degree == 0:
            null_columns.append(np.r_[basis.chemical, np.zeros((modes - 1) * basis.count + 1)])
    else:
        full = stiffness
    factor = linalg.cholesky(metric, lower=True)
    symmetric = linalg.solve_triangular(factor, full, lower=True)
    symmetric = linalg.solve_triangular(factor, symmetric.T, lower=True).T
    if null_columns:
        nulls = factor.T @ np.column_stack(null_columns)
        rotation, _ = linalg.qr(nulls, mode='full')
        complement = rotation[:, len(null_columns):]
    else:
        complement = np.eye(len(metric))
    values, vectors = linalg.eigh(complement.T @ ((symmetric + symmetric.T) / 2) @ complement)
    assert max(values) < 1e-7
    eigenbasis = complement @ vectors
    amplitudes = eigenbasis.T @ factor.T @ initial
    return np.array([linalg.solve_triangular(factor.T, eigenbasis @ (np.exp(values * moment) * amplitudes), lower=False)
                     for moment in times])


def reference_block(label, degree):
    path = PARENT / 'runs' / label / ('evolution-' + str(degree) + '.npz')
    with np.load(path, allow_pickle=False) as source:
        data = {key: source[key].copy() for key in source.files}
    return data, path


def main(arguments):
    modest()
    bank = ROOT / 'banks' / arguments.bank
    metadata = json.loads((bank / 'status.json').read_text())
    assert metadata['all_checks_passed']
    basis = load_basis(bank)
    target, measure = frequency_quadrature(420, basis.minimum, basis.maximum)
    evaluate = basis.evaluate(target)
    folder = ROOT / 'results' / arguments.name
    assert not folder.exists()
    checks, rows, inputs = [], [], [bank / 'status.json', ROOT / 'stable_spectral_basis.py', PARENT / 'cold_control.py']
    for model in ['heavy', 'cold', 'synthetic']:
        sectors = {name: [np.zeros(33), np.zeros(33)] for name in []}
        for degree in range(9):
            reference, path = reference_block(model + '-split-448-band', degree)
            inputs.append(path)
            inputs.append(path.parent / 'status.json')
            names = metadata['rows'][degree]['names']
            with np.load(bank / ('block-' + str(degree) + '.npz')) as saved:
                stiffness, mass = saved['stiffness'], saved['mass']
            inputs.append(bank / ('block-' + str(degree) + '.npz'))
            count = len(reference['nodes'])
            potentials = []
            for mode, name in enumerate(names):
                if model != 'synthetic':
                    coefficient = reference['initial'][mode * count + count // 2] / reference['nodes'][count // 2]
                    potential = coefficient * basis.temperature
                else:
                    frequency = basis.nodes
                    if degree == 0 and name == 'I':
                        values = frequency * (.02 + .003 * np.exp(-frequency / 3) * np.sin(np.log(frequency + .2)))
                    else:
                        values = frequency * .001 * np.exp(-frequency / 4) / (degree + 1) / (mode + 1)
                    potential = basis.project(values)
                potentials.append(potential)
            initial = np.concatenate(potentials).astype(complex)
            capacity = float(reference['capacity'])
            if degree in [0, 1]:
                initial = np.r_[initial, reference['initial'][-1]]
            predicted = propagate(stiffness, mass, basis, degree, capacity, initial, reference['times'])
            reference_values = reference['defects'].copy()
            if model != 'synthetic':
                predicted -= propagate(np.kron(exact_cold(degree), mass), mass, basis, degree, capacity, initial, reference['times'])
                elastic, source = reference_block(model + '-split-448-band-elastic', degree)
                inputs += [source, source.parent / 'status.json']
                reference_values -= elastic['defects']
            for mode, name in enumerate(names):
                compact = predicted[:, mode * basis.count:(mode + 1) * basis.count] @ evaluate.T
                raw = reference_values[:, mode * count:(mode + 1) * count]
                resolved = np.array([np.interp(target, reference['nodes'], row.real) + 1j * np.interp(target, reference['nodes'], row.imag)
                                     for row in raw])
                if name not in sectors:
                    sectors[name] = [np.zeros(len(raw)), np.zeros(len(raw))]
                sectors[name][0] += np.sum(measure * abs(compact - resolved) ** 2, axis=1) / (2 * degree + 1)
                sectors[name][1] += np.sum(measure * abs(resolved) ** 2, axis=1) / (2 * degree + 1)
            if degree in [0, 1]:
                name = 'temperature' if degree == 0 else 'velocity'
                sectors[name] = [capacity * abs(predicted[:, -1] - reference_values[:, -1]) ** 2,
                                 capacity * abs(reference_values[:, -1]) ** 2]
        for name, (difference, scale) in sectors.items():
            numerator, denominator = float(np.sqrt(max(difference))), float(np.sqrt(max(scale)))
            active = denominator > 3.5e-14
            error = numerator / denominator if active else None
            passed = error < .002 if active else numerator < 3.5e-14
            checks.append(dict(name=model + ':' + name + ': compact versus refined physical grid', passed=passed, value=error))
            rows.append(dict(model=model, sector=name, error=error, difference=numerator, reference=denominator, resolved=active))
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        rows=rows, bank=arguments.bank, gate=.002, prior_exact_grid_control=True,
                        no_fit_to_reference_coefficients=True), __file__, sorted(set(inputs)))
    print(json.dumps(dict(checks=checks, rows=rows)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bank', required=True)
    parser.add_argument('--name', required=True)
    main(parser.parse_args())
