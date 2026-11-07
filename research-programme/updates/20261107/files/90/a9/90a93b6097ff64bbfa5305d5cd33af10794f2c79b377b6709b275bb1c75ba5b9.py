from gaunt_gradient import *


def main():
    modest()
    folder = ROOT / 'results/br-jacobian'
    folder.mkdir(parents=True, exist_ok=False)
    tables = [GauntTable(ROOT / 'sources' / ('gauntff_merged_Z0' + str(charge) + '.dat'), charge) for charge in [1, 2]]
    checks, rows = [], []
    step = 1e-6
    for frequency in [.00113, .0113, .113, 1.13, 3.13, 8.13]:
        theta = .000213
        ratio = 1.0003
        densities = np.array([1., .081])
        interpolation_errors = []
        for charge, table in zip([1, 2], tables):
            gamma_squared = charge ** 2 * ALPHA ** 2 / (2 * theta * ratio)
            value, gamma_derivative, frequency_derivative = gaunt_with_log_derivatives(table, gamma_squared, frequency / ratio)
            interpolation_errors.append(abs(value / float(table(gamma_squared, frequency / ratio)) - 1))
            gamma_finite = float((table(gamma_squared * math.exp(step), frequency / ratio) - table(gamma_squared * math.exp(-step), frequency / ratio)) / (2 * step))
            frequency_finite = float((table(gamma_squared, frequency / ratio * math.exp(step)) - table(gamma_squared, frequency / ratio * math.exp(-step))) / (2 * step))
            interpolation_errors.extend([abs(gamma_finite - gamma_derivative) / max(abs(gamma_derivative), 1e-30),
                                         abs(frequency_finite - frequency_derivative) / max(abs(frequency_derivative), 1e-30)])
        checks.append(dict(name='Jacobian differentiates the actual retained Gaunt interpolator at ' + str(frequency), passed=max(interpolation_errors) < 1e-5, value=max(interpolation_errors)))
        coefficient, temperature_derivative = br_coefficient(theta, ratio, frequency, densities, tables)
        temperature_finite = (br_coefficient(theta, ratio + step, frequency, densities, tables)[0] - br_coefficient(theta, ratio - step, frequency, densities, tables)[0]) / (2 * step)
        temperature_error = abs(temperature_finite - temperature_derivative) / max(abs(temperature_derivative), 1e-30)
        checks.append(dict(name='Sourced BR temperature-coefficient derivative at ' + str(frequency), passed=temperature_error < 1e-6, value=temperature_error))
        planck = 1 / np.expm1(frequency)
        distortion = 1e-4 * frequency * np.exp(-frequency)
        occupation_direction = .3 * frequency * np.exp(-frequency)
        temperature_direction = -.17
        density_direction = np.array([.11, -.007])
        occupation = planck + distortion
        coefficient_direction = br_coefficient(theta, ratio, frequency, density_direction, tables)[0] + temperature_derivative * temperature_direction
        soft_factor = planck * np.expm1(frequency - frequency / ratio) + distortion * np.expm1(-frequency / ratio)
        factor_direction = np.expm1(-frequency / ratio) * occupation_direction + np.exp(-frequency / ratio) * (1 + occupation) * frequency / ratio ** 2 * temperature_direction
        predicted = (coefficient_direction * soft_factor + coefficient * factor_direction) / frequency ** 3
        def source(offset):
            local_ratio = ratio + offset * temperature_direction
            local_distortion = distortion + offset * occupation_direction
            local_coefficient = br_coefficient(theta, local_ratio, frequency, densities + offset * density_direction, tables)[0]
            factor = planck * np.expm1(frequency - frequency / local_ratio) + local_distortion * np.expm1(-frequency / local_ratio)
            return local_coefficient * factor / frequency ** 3
        finite = (source(step) - source(-step)) / (2 * step)
        error = abs(finite - predicted) / max(abs(predicted), 1e-30)
        checks.append(dict(name='BR occupation-temperature-ion-density Jacobian at ' + str(frequency), passed=error < 1e-6, value=error))
        rows.append([frequency, coefficient, temperature_derivative, temperature_finite, predicted, finite])
    np.savez_compressed(folder / 'jacobian.npz', samples=rows)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
        derived_coefficient='At fixed theta_star,x: kappa_BR proportional to xi^(-1/2) sum Z_i^2 N_i g(Z_i^2 alpha^2/(2 theta_star xi), x/xi).',
        opacity_density_variation_separate=True, one_sided_table_derivatives_at_stencil_changes=True,
        no_new_fit=True, no_emitting_wave_evolution=True), __file__,
        [ROOT / 'gaunt_gradient.py', ROOT / 'sourced_emission.py', ROOT / 'sources/1109.6552.html', *[table.path for table in tables]])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    main()
