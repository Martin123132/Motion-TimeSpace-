from common229 import *


def symbolic(checks):
    alpha, heat, capacity, energy_response, free_rate, history_U, initial_heat, history_gas = sp.symbols('alpha chi C response free history_U A history_gas')
    denominator = heat * capacity * (alpha - 1) + 2 * heat + alpha * energy_response
    numerator = history_U - (alpha - 1) * initial_heat - 2 - free_rate
    gas = numerator / denominator
    residual = free_rate + alpha * energy_response * gas + (alpha - 1) * (initial_heat + heat * capacity * gas) - history_U + 2 + 2 * heat * gas
    check(checks, 'Full discrete first law derives the Schur update', int(sp.simplify(residual) != 0), 0)
    legacy = (heat * history_gas - 1 - free_rate) / (heat * (alpha + 1) + alpha * energy_response)
    limit = gas.subs({capacity: 1, initial_heat: 1, history_U: alpha + heat * history_gas})
    check(checks, 'Exact NR limit recovers original update', int(sp.simplify(limit - legacy) != 0), 0)
    delta_U, delta_work, delta_gas = sp.symbols('delta_U delta_work delta_gas')
    energy_derivative = delta_U - 2 * heat * delta_gas
    work_derivative = 2 * heat * delta_gas - delta_U
    check(checks, 'Difference energy and expansion work cancel', int(sp.simplify(energy_derivative + work_derivative) != 0), 0)


def state_from_saved(system, saved, index):
    nr = float(saved['temperature_scaled'][index])
    delta = .001 * nr
    return dict(profiles=np.column_stack([saved['profiles'][index], .001 * saved['profiles'][index]]),
        gas=np.array([nr, delta]), work=np.array([saved['expansion_work'][index], 0.]),
        delta_heat=np.asarray(system.eos['delta_A'][index] + system.heat * system.eos['delta_C'][index] * nr + system.heat * system.eos['C'][index] * delta))


def mp_matrix(array):
    array = np.asarray(array)
    if array.ndim == 1:
        return mp.matrix([mp.mpf(float(value)) for value in array])
    return mp.matrix([[mp.mpf(float(value)) for value in row] for row in array])


def explicit_block(system, data, column):
    size = system.basis.count
    top = np.triu(data['matrix']) + np.triu(data['matrix'], 1).T
    matrix = mp.zeros(size + 1)
    matrix[:size, :size] = mp_matrix(top)
    matrix[:size, size] = -mp_matrix(data['thermal'])
    energy = mp_matrix(system.basis.energy)
    alpha = mp.mpf(data['alpha'])
    matrix[size, :size] = alpha * energy.T
    heat = mp.mpf(system.heat)
    matrix[size, size] = heat * (alpha + 1) if column == 0 else heat * mp.mpf(data['capacity']) * (alpha - 1) + 2 * heat
    vector = mp_matrix(data['vector'][:, column])
    rhs = mp.zeros(size + 1, 1)
    rhs[:size, 0] = mp_matrix(system.basis.mass) * vector
    if column == 0:
        rhs[size] = heat * mp.mpf(float(data['histories']['gas'][0])) - 1 + (energy.T * vector)[0]
    else:
        rhs[size] = mp.mpf(float(data['histories']['delta_heat'])) - (alpha - 1) * mp.mpf(data['forcing']) + (energy.T * vector)[0]
    result = mp.lu_solve(matrix, rhs)
    return np.array([float(value) for value in result])


def main():
    modest()
    protocol()
    inputs = read(ROOT / 'inputs.json')
    checks, rows = [], []
    symbolic(checks)
    mp.mp.dps = 80
    for model in ('heavy', 'cold'):
        system = System(model, 6400, inputs)
        path = BRANCH / f'infrared-source-domain-20261008/backgrounds/{model}-nonlocal-refined-6400/history.npz'
        with np.load(register(inputs, path)) as archive:
            saved = dict(archive)
        for index in (1, 3200, 6400):
            previous = state_from_saved(system, saved, max(index - 2, 0))
            state = state_from_saved(system, saved, index - 1)
            if index == 1:
                state = initial(system)
                previous = initial(system)
            updated, details = advance(system, index, state, previous)
            for column, name in enumerate(('NR', 'EOS_difference')):
                full = explicit_block(system, details, column)
                computed = np.r_[updated['profiles'][:, column], updated['gas'][column]]
                error = relative(computed, full)
                check(checks, f'{model}:{index}:{name}: independent80-digit97-state solve', error, 1e-7)
                check(checks, f'{model}:{index}:{name}: raw kinetic equation', details['raw_relative'][column], 1e-7)
                rows.append(dict(model=model, index=index, component=name, block_error=error,
                                 raw_residual=float(details['raw_relative'][column])))
        for theta in (system.theta[0], system.theta[3200], system.theta[-1]):
            nodes, weights = radial_rule(32)
            measure = weights * (1 + theta * nodes) * np.sqrt(2 + theta * nodes)
            measure /= measure.sum()
            mean = np.dot(measure, nodes)
            variance = np.dot(measure, (nodes - mean)**2)
            third = np.dot(measure, (nodes - mean)**3)
            capacity_R = (2 / 3) * system.mixture.fractions[0] * (third - 2 * variance)
            temperature = mp.mpf(float(theta))
            def heat_function(argument):
                return mp.besselk(1, 1 / argument) / mp.besselk(2, 1 / argument) + 3 * argument - 1
            expected = mp.mpf(2) / 3 * mp.mpf(float(system.mixture.fractions[0])) * temperature * mp.diff(heat_function, temperature, 2)
            check(checks, f'{model}:{theta}: heat-capacity derivative from population', float(mp.mpf(capacity_R) / expected - 1), 1e-10)
    add_modules(inputs)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    assert not (ROOT / 'results/preflight.json').exists()
    write(ROOT / 'results/preflight-inputs.json', inputs)
    report = dict(stage=229, state='complete', finished_at=now(), checks=checks, probes=rows,
        qualified=all(row['passed'] for row in checks), failed=[row for row in checks if not row['passed']],
        scope='Symbolic identities and representative coupled-step tests, not full evolution')
    write(ROOT / 'results/preflight.json', report)
    print(json.dumps(dict(checks=len(checks), failed=report['failed'], qualified=report['qualified'])), flush=True)


if __name__ == '__main__':
    main()
