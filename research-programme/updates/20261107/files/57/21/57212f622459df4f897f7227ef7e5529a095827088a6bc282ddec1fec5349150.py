from tail_common import *
from inspect_infrared_state import finite_soft_target


def load_case(name):
    folder = ROOT / 'runs' / name
    return dict(np.load(folder / 'tail.npz')), json.loads((folder / 'status.json').read_text())


def sampled(case, frequencies, times, field='slope'):
    in_space = interpolate.interp1d(np.log(case['frequency']), case[field], axis=1, bounds_error=True)(np.log(frequencies))
    return interpolate.interp1d(case['expansion'], in_space, axis=0, bounds_error=True)(times)


def moment_rows(frequencies):
    weights = np.empty(len(frequencies))
    weights[1:-1] = (frequencies[2:] - frequencies[:-2]) / 2
    weights[0], weights[-1] = (frequencies[1] - frequencies[0]) / 2, (frequencies[-1] - frequencies[-2]) / 2
    bose = np.exp(-frequencies) / (-np.expm1(-frequencies))**2
    return weights * frequencies**3 * bose / (2 * special.zeta(3)), weights * frequencies**4 * bose / I3


def main():
    modest()
    folder = ROOT / 'results/comparison'
    folder.mkdir(parents=True, exist_ok=False)
    checks, refinements, rows, paths = [], [], [], []
    core = np.geomspace(1e-5, 1e-4, 101)
    times = np.linspace(.02, math.log(10), 401)
    pairs = [('heavy-base', 'heavy-time', 'time coarse'), ('heavy-time', 'heavy-space', 'frequency grid'),
             ('heavy-space', 'heavy-angles', 'velocity and angles'), ('heavy-angles', 'heavy-coefficients', 'coefficient table'),
             ('heavy-coefficients', 'heavy-production', 'time fine'), ('cold-base', 'cold-production', 'cold combined refinement'),
             ('heavy-production', 'heavy-upper-domain', 'upper boundary location'),
             ('heavy-production', 'heavy-lower-domain', 'lower boundary location')]
    for first, second, label in pairs:
        before, before_status = load_case(first)
        after, after_status = load_case(second)
        delta = sampled(before, core, times) - sampled(after, core, times)
        error = float(np.max(abs(delta)))
        checks.append(dict(name='Core slope refinement: ' + label, value=error, passed=error < 1e-4))
        frequencies = np.geomspace(max(before['frequency'][0], after['frequency'][0]), 1e-4, 401)
        number_row, energy_row = moment_rows(frequencies)
        old_values, new_values = sampled(before, frequencies, times), sampled(after, frequencies, times)
        moment_errors = []
        for title, weight in [('number', number_row), ('energy', energy_row)]:
            magnitude = float(np.max(abs(new_values @ weight)))
            envelope = float(np.max(abs(new_values)) * np.sum(abs(weight)))
            difference = float(np.max(abs((old_values - new_values) @ weight)))
            limit = max(.01 * magnitude, 1e-5 * envelope)
            moment_errors.append(dict(moment=title, difference_scaled=difference, max_magnitude_scaled=magnitude, tolerance=limit))
            checks.append(dict(name='Tail moment refinement ' + label + ' ' + title, value=difference, limit=limit, passed=difference < limit))
        refinements.append(dict(comparison=label, coarse=first, fine=second, core_max_absolute_error=error, moment_errors=moment_errors))
        for name in [first, second]:
            paths.extend([ROOT / 'runs' / name / suffix for suffix in ['status.json', 'tail.npz']])
    basis, unused = current_basis()
    for model in ['heavy', 'cold']:
        case, status = load_case(model + '-production')
        history = PARENT / 'backgrounds' / (model + '-nonlocal-refined-6400') / 'history.npz'
        parent = dict(np.load(history))
        heat = float(case['heat'])
        grid = np.geomspace(1e-6, 1e-4, 501)
        values = sampled(case, grid, times)
        number_row, energy_row = moment_rows(grid)
        amplitude = float(np.max(abs(values)))
        number, energy = heat * (values @ number_row), heat * (values @ energy_row)
        number_bound = heat * amplitude * (grid[-1]**2 - grid[0]**2) / (4 * special.zeta(3))
        energy_bound = heat * amplitude * (grid[-1]**3 - grid[0]**3) / (3 * I3)
        checks.append(dict(name='Derived number envelope ' + model, value=float(max(abs(number))), limit=number_bound * 1.0001, passed=max(abs(number)) <= number_bound * 1.0001))
        checks.append(dict(name='Derived energy envelope ' + model, value=float(max(abs(energy))), limit=energy_bound * 1.0001, passed=max(abs(energy)) <= energy_bound * 1.0001))
        dynamic = sampled(case, core, times)
        target = sampled(case, core, times, 'equilibrium')
        first_correction = sampled(case, core, times, 'first_correction')
        certificate = sampled(case, core, times, 'residual_bound')
        target_error = float(np.max(abs(dynamic - target)))
        correction_error = float(np.max(abs(dynamic - first_correction)))
        checks.append(dict(name='Derived first correction improves source-only approximation ' + model,
                           value=correction_error / target_error, passed=correction_error < .2 * target_error))
        checks.append(dict(name='Residual comparison remains valid on reported interior ' + model,
                           value=float(np.max(abs(dynamic - target) - certificate)), passed=np.max(abs(dynamic - target) - certificate) < 1e-9))
        original = interpolate.interp1d(parent['expansion'], parent['profiles'], axis=0)(times) @ (basis.evaluate(core) / core[:, None]).T
        core_number, core_energy = moment_rows(core)
        replacement_number = heat * ((dynamic - original) @ core_number)
        replacement_energy = heat * ((dynamic - original) @ core_energy)
        subgrid = np.geomspace(1e-6, 1e-5, 301)
        sub_number, sub_energy = moment_rows(subgrid)
        sub_values = sampled(case, subgrid, times)
        midpoint = len(parent['expansion']) // 2
        profile = parent['profiles'][midpoint]
        beta = float(soft_slope_row(basis, 256) @ profile)
        finite_frequencies = np.array([1e-5, 1e-4, 5e-4, 1e-3])
        finite_targets = np.array([finite_soft_target(basis, profile, frequency, 256) for frequency in finite_frequencies])
        finite_target_error = float(max(abs(finite_targets - beta)))
        shape_error = float(max(abs(integrated_dc.integrated_dc_absorption_shape(finite_frequencies, 256) * finite_frequencies**2 - 1)))
        checks.append(dict(name='Finite-soft target spot-check against limiting hard functional ' + model,
                           value=finite_target_error, passed=finite_target_error < 2e-6))
        checks.append(dict(name='Finite-soft local rate spot-check against inverse-square leading rate ' + model,
                           value=shape_error, passed=shape_error < 2e-6))
        rows.append(dict(model=model, driven_tail_history=str(ROOT / 'runs' / (model + '-production') / 'tail.npz'),
            scaled_slope_amplitude=amplitude, max_equilibrium_slope_error=target_error,
            max_first_corrected_slope_error=correction_error, correction_error_ratio=correction_error / target_error,
            core_rational_slope_mismatch=float(max(abs(dynamic - original).ravel())),
            max_tail_number_fraction=float(max(abs(number))), tail_number_envelope=number_bound,
            max_tail_energy_fraction=float(max(abs(energy))), tail_energy_envelope=energy_bound,
            max_core_replacement_number_fraction=float(max(abs(replacement_number))),
            max_core_replacement_energy_fraction=float(max(abs(replacement_energy))),
            max_subgrid_number_fraction=float(max(abs(heat * (sub_values @ sub_number)))),
            max_subgrid_energy_fraction=float(max(abs(heat * (sub_values @ sub_energy)))),
            max_plasma_ratio=float(case['plasma'].max()), boundary_power=status['selected_boundary_barrier_power'],
            boundary_unit_bound_at_1e5=(float(case['frequency'][0]) / 1e-5)**status['selected_boundary_barrier_power'],
            finite_soft_frequencies=finite_frequencies.tolist(), finite_soft_target_minus_beta=(finite_targets - beta).tolist(),
            finite_soft_rate_max_relative_difference=shape_error,
            physical_departures_multiply_scaled_slope_by_heat=heat))
        paths.extend([history, history.parent / 'status.json'])
    finish(folder, dict(checks=checks, refinements=refinements, rows=rows,
        numerical_bounds_scope='Driven discretized leading soft model; physical collective and finite-recoil errors not included.',
        moment_domain=[1e-6, 1e-4], core_domain=[1e-5, 1e-4], analysed_expansion=[.02, math.log(10)],
        full_parent_history_feedback_applied=False, pointwise_old_basis_extrapolation_used=False), __file__, paths)
    print(json.dumps(dict(checks=len(checks), failed=[item for item in checks if not item['passed']], rows=rows)), flush=True)


if __name__ == '__main__':
    main()
