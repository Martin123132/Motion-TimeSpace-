from tail_common import *
from compare_tails import moment_rows


def main():
    modest()
    folder = ROOT / 'results/regularity-certificate'
    folder.mkdir(parents=True, exist_ok=False)
    basis, unused = current_basis()
    paths, checks, rows = [], [], []
    for model in ['heavy', 'cold']:
        case_path = ROOT / 'runs' / (model + '-production') / 'tail.npz'
        case = dict(np.load(case_path))
        history = PARENT / 'backgrounds' / (model + '-nonlocal-refined-6400') / 'history.npz'
        parent = dict(np.load(history))
        grid, coordinates, offsets = case['frequency'], case['expansion'], case['offsets']
        size, margin = len(grid), -int(offsets[0])
        spacing = math.log(grid[1] / grid[0])
        all_grid = grid[0] * np.exp(spacing * np.arange(-margin, size + margin))
        high_grid = all_grid[margin + size:]
        bank = interpolate.interp1d(case['coefficient_knots'], case['coefficient_bank'], axis=0, bounds_error=True)(coordinates)
        driving_profiles = interpolate.interp1d(parent['expansion'], parent['profiles'], axis=0)(coordinates)
        gas = np.interp(coordinates, parent['expansion'], parent['temperature_scaled'])
        hard = driving_profiles @ soft_slope_row(basis, 256)
        high = driving_profiles @ (basis.evaluate(high_grid) / high_grid[:, None]).T
        constant, exterior, source_values, source_bounds = 0., 0., [], []
        powers = [2, 4, 6, 8, 10]
        margins = {power: [] for power in powers}
        previous_target = np.zeros(size)
        step = coordinates[1] - coordinates[0]
        for index in range(1, len(coordinates)):
            coefficients = bank[index, :len(offsets)]
            eigenvalue, dc_coefficient, rate = bank[index, len(offsets):len(offsets) + 3]
            dc = dc_coefficient / all_grid**2
            br = bank[index, len(offsets) + 3:]
            gamma_all = dc + br
            target_all = (dc * hard[index] + br * gas[index]) / gamma_all
            target = target_all[margin:margin + size]
            gamma = gamma_all[margin:margin + size]
            internal, lower, upper = split_matrix(coefficients, offsets, size)
            transport_target = internal @ target + lower @ target_all[:margin] + upper @ target_all[margin + size:]
            residual_source = (target - previous_target) / step - rate * (transport_target + eigenvalue * (target - gas[index]))
            eigen3 = float(coefficients @ np.exp(2 * offsets * spacing) + eigenvalue)
            denominator = rate * (gamma - eigen3) * grid**2
            assert denominator.min() > 0
            constant = max(constant, float(max(abs(residual_source) / denominator)))
            exterior = max(exterior, float(max(abs(high[index] - target_all[margin + size:]))))
            for power in powers:
                eigen = float(coefficients @ np.exp(power * offsets * spacing) + eigenvalue)
                margins[power].append(float(min(gamma - eigen)))
            if index in [1600, 3200, 6400]:
                number_row, energy_row = moment_rows(grid)
                dc_source = -dc[margin:margin + size] * (case['slope'][index] - hard[index])
                br_source = -br[margin:margin + size] * (case['slope'][index] - gas[index])
                total_source = -gamma * (case['slope'][index] - target)
                cancellation_error = float(max(abs(dc_source + br_source - total_source)) / max(1., max(abs(total_source))))
                checks.append(dict(name='DC/BR source combination derived, not set to zero ' + model + str(index), value=cancellation_error, passed=cancellation_error < 1e-7))
                source_values.append(dict(expansion=float(coordinates[index]),
                    dc_number_per_tau=float(case['heat'] * number_row @ dc_source),
                    br_number_per_tau=float(case['heat'] * number_row @ br_source),
                    combined_number_per_tau=float(case['heat'] * number_row @ total_source),
                    combined_energy_per_tau=float(case['heat'] * energy_row @ total_source)))
            previous_target = target
        allowed = [power for power in powers if min(margins[power]) > 0]
        power = max(allowed)
        envelope = constant * grid**2 + exterior * (grid / grid[-1])**power
        defect = float(max((abs(case['slope'] - case['equilibrium']) - envelope).ravel()))
        checks.append(dict(name='Derived regular x-squared plus exterior barrier controls full dynamic tail ' + model,
                           value=defect, passed=defect < 1e-9))
        checks.append(dict(name='Upper-boundary barrier exponent at least2 leaves integrable combined number source ' + model,
                           value=power, passed=power >= 2))
        rows.append(dict(model=model, source_residual_barrier_constant=constant,
            max_upper_exterior_slope_mismatch=exterior, upper_boundary_barrier_power=power,
            upper_barrier_gaps={str(key): min(value) for key, value in margins.items()},
            core_error_bound_at_1e5=constant * 1e-10 + exterior * (1e-5 / grid[-1])**power,
            core_error_bound_at_1e4=constant * 1e-8 + exterior * (1e-4 / grid[-1])**power,
            number_rate_examples=source_values,
            theorem_domain='Retained leading kinetic equation and positive discrete jump approximation; collective region and higher-order kernels excluded.'))
        paths.extend([case_path, case_path.parent / 'status.json', history, history.parent / 'status.json'])
    finish(folder, dict(checks=checks, rows=rows, zero_source_imposed=False,
        extrapolation_below_minimum_used=False, new_numerical_zero_frequency_solution_claimed=False), __file__, paths)
    print(json.dumps(dict(checks=len(checks), failed=[item for item in checks if not item['passed']], rows=rows)), flush=True)


if __name__ == '__main__':
    main()
