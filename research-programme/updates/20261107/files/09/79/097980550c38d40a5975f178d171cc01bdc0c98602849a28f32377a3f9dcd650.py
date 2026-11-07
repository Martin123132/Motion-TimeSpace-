import argparse
from tail_common import *


def main():
    modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--model', choices=['heavy', 'cold'], default='heavy')
    parser.add_argument('--size', type=int, default=241)
    parser.add_argument('--steps', type=int, default=1600)
    parser.add_argument('--order', type=int, default=4)
    parser.add_argument('--knots', type=int, default=65)
    parser.add_argument('--minimum', type=float, default=1e-6)
    parser.add_argument('--maximum', type=float, default=5e-4)
    arguments = parser.parse_args()
    folder = ROOT / 'runs' / arguments.name
    folder.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    basis, specification = current_basis()
    background = thermal_wave.thermal.ThermalBackground(arguments.model)
    history = PARENT / 'backgrounds' / (arguments.model + '-nonlocal-refined-6400') / 'history.npz'
    saved = dict(np.load(history))
    slope = soft_slope_row(basis, 256)
    grid = np.geomspace(arguments.minimum, arguments.maximum, arguments.size)
    spacing = math.log(grid[1] / grid[0])
    ratios, unused = jump_events(background.at(0)['thermal_parameter'], arguments.order)
    margin = int(np.ceil(np.max(abs(np.log(ratios))) / spacing)) + 2
    offsets = np.arange(-margin, margin + 1)
    low_grid = grid[0] * np.exp(spacing * np.arange(-margin, 0))
    high_grid = grid[-1] * np.exp(spacing * np.arange(1, margin + 1))
    assert high_grid.min() >= basis.minimum and high_grid.max() < basis.maximum
    all_grid = np.r_[low_grid, grid, high_grid]
    free_free = FreeFree(background, all_grid)
    knots = np.linspace(0, background.end, arguments.knots)
    rows, local_rows = [], []
    for coordinate in knots:
        local = background.at(coordinate)
        theta = local['thermal_parameter']
        coefficients, eigenvalue = stencil(theta, arguments.order, spacing, offsets)
        rows.append(np.r_[coefficients, eigenvalue, integrated_dc.DC_CONSTANT * theta**2,
                          local['coefficient'] / theta, free_free.br_rates(theta)])
        local_rows.append([theta, plasma_ratio(background, theta)])
    bank = np.asarray(rows)
    high_values = basis.evaluate(high_grid) / high_grid[:, None]
    driving = np.column_stack([saved['temperature_scaled'], saved['profiles'] @ slope,
                               saved['profiles'] @ high_values.T])
    drive = interpolate.interp1d(saved['expansion'], driving, axis=0, bounds_error=True)
    coefficients_at = interpolate.interp1d(knots, bank, axis=0, bounds_error=True)
    step = background.end / arguments.steps
    coordinates = np.linspace(0, background.end, arguments.steps + 1)
    state = np.zeros((arguments.size, 4))
    state[:, 3] = 1.
    solutions = [state.copy()]
    targets = [np.zeros(arguments.size)]
    approximate = [np.zeros(arguments.size)]
    residuals, gamma_rows, contractions = [], [], []
    solve_errors, certificates, row_margins = [], [], []
    boundary_powers = [2, 4, 8, 12]
    barrier_margins = {power: [] for power in boundary_powers}
    previous_target = np.zeros(arguments.size)
    identity = sparse.eye(arguments.size, format='csc')
    for index, coordinate in enumerate(coordinates[1:], 1):
        values = coefficients_at(coordinate)
        coefficients = values[:len(offsets)]
        eigenvalue, dc_coefficient, rate = values[len(offsets):len(offsets) + 3]
        br_rate = values[len(offsets) + 3:]
        gas, hard = drive(coordinate)[:2]
        high = drive(coordinate)[2:]
        dc_rate = dc_coefficient / all_grid**2
        total = dc_rate + br_rate
        target_all = (dc_rate * hard + br_rate * gas) / total
        target = target_all[margin:margin + arguments.size]
        gamma = total[margin:margin + arguments.size]
        internal, lower, upper = split_matrix(coefficients, offsets, arguments.size)
        generator = rate * (internal + sparse.diags(eigenvalue - gamma, format='csc'))
        rhs = rate * (gamma * target - eigenvalue * gas + lower @ target_all[:margin] + upper @ high)
        operator = identity - step * generator
        inverse = sparse_linalg.splu(operator)
        residual = (target - previous_target) / step - generator @ target - rhs
        right = state.copy()
        right[:, 0] += step * rhs
        right[:, 1] += step * abs(residual)
        right[:, 2] += step * rate * (lower @ np.ones(margin))
        updated = inverse.solve(right)
        solve_errors.append(float(np.max(abs(operator @ updated - right)) / max(1., np.max(abs(right)))))
        error = abs(updated[:, 0] - target)
        certificates.append(float(np.max(error - updated[:, 1])))
        offdiagonal = internal - sparse.diags(internal.diagonal())
        assert offdiagonal.data.min(initial=0.) >= -1e-15
        row_margin = float(np.min(gamma - eigenvalue))
        assert row_margin > 0
        row_margins.append(row_margin)
        for power in boundary_powers:
            eigen_barrier = float(coefficients @ np.exp(-power * offsets * spacing) + eigenvalue)
            barrier_margins[power].append(float(np.min(gamma - eigen_barrier)))
        source_derivative = (target - previous_target) / step
        target_transport = internal @ target + lower @ target_all[:margin] + upper @ target_all[margin + arguments.size:]
        correction = (target_transport + eigenvalue * (target - gas) - source_derivative / rate) / gamma
        state, previous_target = updated, target
        solutions.append(state.copy())
        targets.append(target.copy())
        approximate.append(target + correction)
        gamma_rows.append(gamma)
        contractions.append(rate * row_margin)
        residuals.append(residual)
        if index % max(1, arguments.steps // 4) == 0:
            print(json.dumps(dict(step=index, steps=arguments.steps, elapsed=time.perf_counter() - started)), flush=True)
    solutions, targets, approximate = map(np.asarray, [solutions, targets, approximate])
    accepted_powers = [power for power in boundary_powers if min(barrier_margins[power]) > 0]
    power = max(accepted_powers)
    boundary_envelope = (grid[0] / grid)**power
    checks = [
        dict(name='Sparse dynamic equations solved', value=max(solve_errors), passed=max(solve_errors) < 1e-9),
        dict(name='Absorbing positive-kernel contraction', value=min(row_margins), passed=min(row_margins) > 0),
        dict(name='Executed componentwise equilibrium-residual certificate', value=max(certificates), passed=max(certificates) < 1e-9),
        dict(name='Comparison solutions remain nonnegative', value=float(solutions[:, :, 1:].min()), passed=solutions[:, :, 1:].min() > -1e-12),
        dict(name='Lower-boundary influence below derived power barrier', value=float(np.max(solutions[:, :, 2] - boundary_envelope)), passed=np.max(solutions[:, :, 2] - boundary_envelope) < 1e-10),
        dict(name='No old basis extrapolated beneath its floor', passed=high_grid.min() >= basis.minimum),
        dict(name='All numerical arrays finite', passed=all(np.isfinite(item).all() for item in [solutions, targets, approximate, bank])),
    ]
    np.savez_compressed(folder / 'tail.npz', expansion=coordinates, frequency=grid, slope=solutions[:, :, 0],
        equilibrium=targets, first_correction=approximate, residual_bound=solutions[:, :, 1],
        lower_unit_response=solutions[:, :, 2], initial_unit_response=solutions[:, :, 3],
        boundary_envelope=boundary_envelope, gamma=np.array(gamma_rows), contraction=np.array(contractions),
        coefficient_knots=knots, coefficient_bank=bank, offsets=offsets, plasma=np.asarray(local_rows)[:, 1],
        heat=background.chi)
    core = (grid >= 1e-5) & (grid <= 1e-4)
    late = coordinates >= .02
    report = dict(checks=checks, model=arguments.model, settings=vars(arguments),
        scope='Driven leading soft-tail solve on saved finite-capacity background; no feedback or full finite-recoil claim.',
        beta_driver='Stage89 refined leading nonlocal source history, piecewise linear in expansion',
        selected_boundary_barrier_power=power,
        barrier_margins={str(key): min(value) for key, value in barrier_margins.items()},
        smallest_minimum_over_plasma=float(grid[0] / max(np.asarray(local_rows)[:, 1])),
        max_core_departure_from_source_target=float(np.max(abs(solutions[late, :, 0][:, core] - targets[late][:, core]))),
        max_core_equilibrium_error_certificate=float(np.max(solutions[late, :, 1][:, core])),
        max_core_lower_unit_influence=float(np.max(solutions[late, :, 2][:, core])),
        max_core_initial_unit_influence_after_002=float(np.max(solutions[late, :, 3][:, core])),
        minimum_contraction_per_expansion=min(contractions), elapsed=time.perf_counter() - started)
    finish(folder, report, __file__, [history, history.parent / 'status.json', background.parent.source,
                                    background.native_constants, *free_free.inputs])
    print(json.dumps(dict(name=arguments.name, passed=report['all_checks_passed'], elapsed=report['elapsed'], core_error=report['max_core_departure_from_source_target'], boundary_power=power), default=lambda value: value.item()), flush=True)


if __name__ == '__main__':
    main()
