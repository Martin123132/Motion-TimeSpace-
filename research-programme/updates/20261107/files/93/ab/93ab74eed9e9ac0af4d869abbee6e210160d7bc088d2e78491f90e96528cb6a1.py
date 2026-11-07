from common230 import *


def symbolic(checks):
    alpha, omega, first, second = sp.symbols('alpha omega first second', positive=True)
    determinant = alpha * (alpha + 2) + omega**2
    horizontal = ((alpha + 2) * first + omega * second) / determinant
    vertical = (alpha * second - omega * first) / determinant
    check(checks, 'Field position implicit equation', int(sp.simplify(alpha * horizontal - omega * vertical - first) != 0), 0)
    check(checks, 'Field momentum implicit equation', int(sp.simplify(omega * horizontal + (alpha + 2) * vertical - second) != 0), 0)
    derivative = sp.Matrix([horizontal, vertical]).diff(omega) * (-omega)
    matrix = sp.Matrix([[alpha, -omega], [omega, alpha + 2]])
    residual = matrix * derivative - sp.Matrix([-omega * vertical, omega * horizontal])
    check(checks, 'Analytic field logarithmic-H derivative', int(any(sp.simplify(value) != 0 for value in residual)), 0)
    heat, capacity, gas_log = sp.symbols('chi C gas_log')
    energy_log = -heat * (capacity * (alpha - 1) + 2) * gas_log / alpha
    check(checks, 'Thermal density derivative loses leading exchange term',
        int(sp.simplify(heat * (energy_log + heat * capacity * gas_log) - heat**2 * (capacity - 2) * gas_log / alpha) != 0), 0)


def saved_state(system, thermal, response_spline, index):
    coordinate = float(system.coordinates[index])
    native = state_at_scale(system.background, system.background.start_scale * math.exp(coordinate))
    responses = response_spline(coordinate)
    fields = np.zeros((2, 2, 3))
    fields[0, :, 0], fields[1, :, 0] = native['fields'], native['prime']
    fields[0, :, 1] = system.heat * responses[:2, 0]
    fields[1, :, 1] = system.heat * responses[2:4, 0]
    fields[0, :, 2] = system.heat * system.initial_D * responses[:2, 1]
    fields[1, :, 2] = system.heat * system.initial_D * responses[2:4, 1]
    row = thermal['rows'][index]
    return dict(profiles=thermal['profiles'][index], gas=row[3:5], delta_heat=np.asarray(row[5]),
                work=row[6:8], fields=fields, clocks=np.zeros((2, 3)))


def mp_array(values):
    values = np.asarray(values)
    if values.ndim == 1:
        return mp.matrix([mp.mpf(float(value)) for value in values])
    return mp.matrix([[mp.mpf(float(value)) for value in row] for row in values])


def full_mp(step, hubble, component):
    system, size = step.system, step.system.basis.count
    alpha, heat, scale = mp.mpf(step.alpha), mp.mpf(system.heat), mp.mpf(step.scale)
    rate = mp.mpf(step.opacity) / hubble
    field_history = sum((mp_array(step.field_history[:, :, column]) for column in range(component + 1)), mp.zeros(2))
    omega = [scale * mp.mpf(float(mass)) / hubble for mass in system.mass]
    field_energy = mp.mpf(0)
    for index in range(2):
        history_first, history_second = field_history[0, index], field_history[1, index]
        determinant = alpha * (alpha + 2) + omega[index]**2
        field_first = ((alpha + 2) * history_first + omega[index] * history_second) / determinant
        field_second = (alpha * history_second - omega[index] * history_first) / determinant
        field_energy += (field_first**2 + field_second**2) / 2
    if component == 0:
        thermal_energy = mp.mpf(0)
    else:
        vector = mp_array(step.histories['profiles'][:, 0])
        if component == 2:
            vector += mp_array(step.histories['profiles'][:, 1])
        capacity = mp.mpf(1) if component == 1 else mp.mpf(step.capacity)
        operator = mp.zeros(size + 1)
        operator[:size, :size] = alpha * mp_array(system.effective_mass) - rate * mp_array(step.effective_stiffness)
        operator[:size, size] = rate * mp_array(step.column)
        energy_row = mp_array(system.basis.energy)
        operator[size, :size] = alpha * energy_row.T
        operator[size, size] = heat * (capacity * (alpha - 1) + 2)
        rhs = mp.zeros(size + 1, 1)
        rhs[:size, 0] = mp_array(system.basis.mass) * vector
        rhs[size] = heat * mp.mpf(float(step.histories['gas'][0])) - 1 + (energy_row.T * vector)[0]
        if component == 2:
            rhs[size] += mp.mpf(float(step.histories['delta_heat'])) - (alpha - 1) * mp.mpf(step.excess)
        solution = mp.lu_solve(operator, rhs)
        energy = (energy_row.T * solution[:size, 0])[0]
        gas_heat = 1 + heat * solution[size] if component == 1 else 1 + mp.mpf(step.excess) + heat * capacity * solution[size]
        thermal_energy = mp.mpf(step.photon) * heat * (energy + gas_heat)
    return hubble**2 - scale**2 * (mp.mpf(step.base_density) + field_energy + thermal_energy) / 3


def main():
    modest()
    protocol()
    inputs = read(ROOT / 'inputs.json')
    checks, probes = [], []
    symbolic(checks)
    mp.mp.dps = 80
    for model in ('heavy', 'cold'):
        system = System(model, 6400, inputs)
        with np.load(register(inputs, PREVIOUS / f'runs/{model}-6400/history.npz')) as saved:
            thermal = dict(saved)
        with np.load(register(inputs, THERMO / f'results/{model}-gravity.npz')) as saved:
            response_spline = interpolate.CubicSpline(saved['expansion'], saved['response'], axis=0)
        for index in (1, 3200, 6400):
            state = saved_state(system, thermal, response_spline, index - 1)
            previous = saved_state(system, thermal, response_spline, max(index - 2, 0))
            if index == 1:
                state, ignored = initial(system)
                previous, ignored = initial(system)
            step = Step(system, index, state, previous)
            result, diagnostic = step.advance()
            native = state_at_scale(system.background, step.scale)
            fixed_NR = step.thermal(native['hubble'], 'NR')
            fixed_EOS = step.thermal(native['hubble'], 'EOS', fixed_NR, 0.)
            old_result, old_details = prior.advance(system, index, state, previous)
            check(checks, f'{model}:{index}: original fixed-H NR solve', relative(fixed_NR['profile'], old_result['profiles'][:, 0]), 1e-7)
            check(checks, f'{model}:{index}: original fixed-H EOS difference', relative(fixed_EOS['profile'], old_result['profiles'][:, 1]), 1e-7)
            for kind in ('nr', 'eos'):
                root = diagnostic[kind]
                width = 5e-4
                slope = (root['evaluate'](root['normalized'] + width)['residual'] - root['evaluate'](root['normalized'] - width)['residual']) / (2 * width)
                check(checks, f'{model}:{index}:{kind}: independent root Jacobian', slope / root['jacobian'] - 1, 1e-7)
                check(checks, f'{model}:{index}:{kind}: scaled small-source residual', root['residual'], 1e-10)
                check(checks, f'{model}:{index}:{kind}: positive sampled branch Jacobian', int(root['minimum_sampled_jacobian'] <= 0), 0)
            hubble0 = mp.mpf(diagnostic['hubble0'])
            fraction_NR = mp.mpf(diagnostic['fraction_NR'])
            fraction_EOS = mp.mpf(diagnostic['fraction_EOS'])
            hubble_NR = hubble0 * (1 + fraction_NR)
            hubble_EOS = hubble_NR * (1 + fraction_EOS)
            full0 = full_mp(step, hubble0, 0)
            full_NR = full_mp(step, hubble_NR, 1)
            full_EOS = full_mp(step, hubble_EOS, 2)
            error_NR = float((full_NR - full0) / (hubble0**2 * mp.mpf(system.heat)))
            error_EOS = float((full_EOS - full_NR) / (hubble_NR**2 * mp.mpf(system.heat) * mp.mpf(system.initial_D)))
            check(checks, f'{model}:{index}: full80-digit NR difference Friedmann residual', error_NR, 1e-7)
            check(checks, f'{model}:{index}: full80-digit EOS difference Friedmann residual', error_EOS, 1e-7)
            probes.append(dict(model=model, index=index, fraction_NR=diagnostic['fraction_NR'],
                fraction_EOS=diagnostic['fraction_EOS'], minimum_J=diagnostic['minimum_jacobian'] / 2,
                independent_NR_residual=error_NR, independent_EOS_residual=error_EOS,
                no_heat_constraint_residual=diagnostic['root_residual0']))
            print(json.dumps(probes[-1]), flush=True)
    add_modules(inputs)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    write(ROOT / 'results/preflight-inputs.json', inputs)
    assert not (ROOT / 'results/preflight.json').exists()
    report = dict(stage=230, state='complete', finished_at=now(), checks=checks, probes=probes,
        qualified=all(row['passed'] for row in checks), failed=[row for row in checks if not row['passed']])
    write(ROOT / 'results/preflight.json', report)
    print(json.dumps(dict(checks=len(checks), failed=report['failed'], qualified=report['qualified'])), flush=True)


if __name__ == '__main__':
    main()
