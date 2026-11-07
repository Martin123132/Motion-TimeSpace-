from nonlocal_dc import *


def finite_soft_target(basis, profile, soft_frequency, order=256):
    extra, weights = special.roots_laguerre(order)
    seed = 2 * soft_frequency + extra
    hard = seed - soft_frequency
    inside = seed <= basis.maximum
    seed, hard, weights = seed[inside], hard[inside], weights[inside]
    density = weights * seed**4 * gould(soft_frequency / seed)
    density /= (-np.expm1(-seed)) * (-np.expm1(-hard))
    difference = (basis.evaluate(seed) - basis.evaluate(hard)) @ profile / soft_frequency
    return float(density @ difference / density.sum())


def br_coefficient(emission, theta, frequency):
    saved = emission.frequency
    emission.frequency = np.array(frequency)
    try:
        result = emission.br_rates(theta) * np.array(frequency)**2
    finally:
        emission.frequency = saved
    return result


def main():
    modest()
    folder = ROOT / 'results/infrared-domain'
    folder.mkdir(parents=True, exist_ok=False)
    basis, specification = current_basis()
    slope192, slope256 = soft_slope_row(basis, 192), soft_slope_row(basis, 256)
    rows, checks, paths = [], [], []
    for model in ['heavy', 'cold']:
        background = thermal_wave.thermal.ThermalBackground(model)
        emission = NonlocalEmission(basis, background, 'nonlocal-leading', ROOT / 'banks/s700-i160')
        for mode, history in [
            ('inherited-local', KINETIC / 'backgrounds' / (model + '-derived-gaunt') / 'history.npz'),
            ('nonlocal-leading', ROOT / 'backgrounds' / (model + '-nonlocal-leading-6400') / 'history.npz')]:
            saved = dict(np.load(history))
            paths.extend([history, history.parent / 'status.json'])
            for fraction in [.25, .5, 1.]:
                index = round(fraction * (len(saved['expansion']) - 1))
                profile = saved['profiles'][index]
                gas = float(saved['temperature_scaled'][index])
                local = background.at(saved['expansion'][index])
                theta = local['thermal_parameter']
                beta = float(slope256 @ profile)
                beta_error = abs(float((slope192 - slope256) @ profile))
                frequencies = np.array([1e-7, 1e-6, 1e-5, 1e-4, 5e-4, .001])
                values = basis.evaluate(frequencies) @ profile
                offset_zero = float(basis.evaluate(np.array([0.]))[0] @ profile)
                dc_coefficient = integrated_dc.DC_CONSTANT * theta**2
                free_free = br_coefficient(emission, theta, frequencies)
                target = (dc_coefficient * beta + free_free * gas) / (dc_coefficient + free_free)
                constants = background.constants
                reduced_wavelength = 6.62607015e-34 / (2 * np.pi * constants['m_e'] * constants['c'])
                electron_density = background.electron0 / local['scale']**3
                plasma_frequency = math.sqrt(4 * integrated_dc.ALPHA * electron_density * reduced_wavelength**3) / theta
                checks.append(check('Hard-slope quadrature control ' + model + mode + str(fraction), beta_error, 2e-5))
                rows.append(dict(model=model, source=mode, history_fraction=fraction, temperature=theta,
                                 gas_slope=gas, dc_hard_slope=beta, slope_quadrature_absolute_error=beta_error,
                                 formal_basis_value_at_zero=offset_zero, frequencies=frequencies.tolist(),
                                 saved_phi_over_x=(values / frequencies).tolist(),
                                 leading_combined_source_target=target.tolist(),
                                 plasma_frequency_over_temperature=plasma_frequency,
                                 extrapolated_values_are_diagnostic_not_physical=True))
                if fraction == .5 and mode == 'nonlocal-leading':
                    targets = [finite_soft_target(basis, profile, soft) for soft in [.01, .001, .0001]]
                    checks.append(check('Finite-frequency hard target approaches derived slope ' + model,
                                        abs(targets[-1] - beta), 2e-4))
                    rows[-1]['finite_soft_frequencies'] = [.01, .001, .0001]
                    rows[-1]['finite_soft_targets'] = targets
        paths.extend(emission.inputs)
    checks.append(dict(name='A constant rational continuation is detected and explicitly not accepted as physical IR',
                       passed=all(abs(row['formal_basis_value_at_zero']) > 1e-10 for row in rows)))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
           rows=rows, infrared_slope_is_hard_spectrum_and_free_free_weighted=True,
           full_collective_plasma_completion=False, arbitrary_below_grid_extrapolation_used_in_evolution=False),
           __file__, paths)
    print(json.dumps(dict(failed=[row for row in checks if not row['passed']],
                         midpoint_rows=[row for row in rows if row['history_fraction'] == .5])), flush=True)


if __name__ == '__main__':
    main()
