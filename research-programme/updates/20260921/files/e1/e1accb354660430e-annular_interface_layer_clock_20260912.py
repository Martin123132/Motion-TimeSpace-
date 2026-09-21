import numpy as np
from scipy.integrate import solve_ivp


def profile(fraction, name):
    if name == 'beta22':
        return 6 * fraction * (1 - fraction)
    if name == 'beta33':
        return 30 * fraction**2 * (1 - fraction)**2
    if name == 'beta23':
        return 12 * fraction * (1 - fraction)**2
    raise ValueError(name)


def solve_layer(radius, mass_left, lapse_left, energy, width, name, order=96, tolerance=2e-13):
    if min(radius - width / 2, lapse_left, energy, width) <= 0 or mass_left < 0:
        raise ValueError('Invalid positive layer data.')
    coupling = .1

    def equation(fraction, state):
        location = radius + width * (fraction - .5)
        mass = state[0]
        geometry = 1 - 2 * mass / location
        if geometry <= .1:
            raise ValueError('Layer left the positive geometry chart.')
        weight = profile(fraction, name)
        background = width * mass / (location**2 * geometry)
        concentration = coupling * energy * weight / location
        return [coupling * geometry * energy * weight, background, concentration,
                np.sqrt(geometry) * energy * weight,
                lapse_left * (width * mass / (coupling * location**2 * geometry**1.5)
                              + energy * weight / (location * np.sqrt(geometry)))]

    solution = solve_ivp(equation, (0., 1.), [mass_left, 0., 0., 0., 0.], method='DOP853',
                         rtol=tolerance, atol=tolerance / 100, max_step=1 / 32, dense_output=True)
    if not solution.success:
        raise RuntimeError(solution.message)
    points, weights = np.polynomial.legendre.leggauss(order)
    fraction, weights = (points + 1) / 2, weights / 2
    mass, background, concentration, sigma, momentum_integral = solution.sol(fraction)
    location = radius + width * (fraction - .5)
    density = energy * profile(fraction, name) / width
    geometry = 1 - 2 * mass / location
    root = np.sqrt(geometry)
    base = mass / (location**2 * geometry)
    source = coupling * density / location
    root_initial = np.sqrt(1 - 2 * mass_left / (radius - width / 2))
    final = solution.y[:, -1]
    root_final = np.sqrt(1 - 2 * final[0] / (radius + width / 2))
    impulse = final[1] + final[2]
    constant_clock_rate = lapse_left * (base + source) / (coupling * root)
    static_lapse = lapse_left * np.exp(background + concentration)
    static_lapse_r = static_lapse * (base + source)
    static_rate = (-static_lapse_r / (coupling * root)
                   + static_lapse * mass / (coupling * location**2 * root**3)
                   + static_lapse * density / (location * root))
    logarithmic_change = np.log(root_final / root_initial)
    thin_parameter = coupling * energy / radius
    root_at_center_left = np.sqrt(1 - 2 * mass_left / radius)
    root_limit = root_at_center_left * np.exp(-thin_parameter)
    mean_limit = root_at_center_left * (-np.expm1(-thin_parameter)) / thin_parameter
    momentum_limit = lapse_left * np.expm1(thin_parameter) / (coupling * root_at_center_left)
    mass_limit = radius * (1 - root_limit**2) / 2
    coordinate_clock_ratio = np.exp(impulse)
    transport_ratio = np.exp(impulse) * root_final / root_initial
    peak_rate = float(constant_clock_rate.max())
    max_connection_coefficient = coupling / lapse_left
    pressure_integral_bound = impulse / (width * max_connection_coefficient)
    row = {'radius': radius, 'mass_left': mass_left, 'lapse_left': lapse_left, 'energy': energy,
           'width': width, 'profile': name, 'order': order, 'ode_steps': solution.t.size - 1,
           'zeta': thin_parameter, 'minimum_F': float(geometry.min()),
           'root_left_actual': float(root_initial), 'root_right': float(root_final),
           'mass_right': float(final[0]), 'I_background': float(final[1]),
           'I_source': float(final[2]), 'source_sigma': float(final[3]),
           'effective_U_trace': float(final[3] / energy),
           'constant_clock_G': float(impulse), 'constant_clock_J': float(np.exp(impulse)),
           'zero_P1_lapse_ratio': float(coordinate_clock_ratio),
           'zero_P1_max_residual': float(abs(static_rate).max()),
           'constant_clock_peak_P1': peak_rate, 'constant_clock_width_times_peak_P1': width * peak_rate,
           'required_peak_P1_lower_bound': float(pressure_integral_bound),
           'P1_integral': float(final[4]), 'P1_integral_thin_limit': float(momentum_limit),
           'P1_integral_limit_error': float(abs(final[4] - momentum_limit)),
           'log_U_identity_error': float(abs(logarithmic_change - final[1] + final[2])),
           'JC_over_R2_identity_error': float(abs(transport_ratio - np.exp(2 * final[1]))),
           'root_limit_error': float(abs(root_final - root_limit)),
           'mass_limit_error': float(abs(final[0] - mass_limit)),
           'log_mean_limit': float(mean_limit), 'mean_limit_error': float(abs(final[3] / energy - mean_limit)),
           'G_limit_error': float(abs(impulse - thin_parameter)),
           'singular_jump_remainder': float(abs((radius / coupling) * (root_final - root_initial) + final[3])),
           'shared_clock_with_bounded_P1_proven': False, 'full_scalar_action_descent_proven': False}
    arrays = {'fraction': fraction, 'weights': weights, 'R': location, 'mu': mass, 'U': root,
              'rho': density, 'I_background': background, 'I_source': concentration,
              'P1_constant_clock': constant_clock_rate, 'N_static': static_lapse,
              'N_static_R': static_lapse_r, 'J_constant_clock': np.exp(background + concentration)}
    return row, arrays


def action_controls(arrays, lapse, width):
    fraction, location, mass = arrays['fraction'], arrays['R'], arrays['mu']
    weights, density = arrays['weights'] * width, arrays['rho']
    coupling, reference = .1, np.sqrt(2 / 3)
    results = []
    for mode in ['constant_clock', 'zero_P1']:
        lapse_values = np.full_like(location, lapse) if mode == 'constant_clock' else arrays['N_static']
        lapse_r = np.zeros_like(location) if mode == 'constant_clock' else arrays['N_static_R']
        expected_rate = arrays['P1_constant_clock'] if mode == 'constant_clock' else np.zeros_like(location)

        def hamiltonian(trial_mass, trial_lapse, trial_lapse_r):
            root = np.sqrt(1 - 2 * trial_mass / location)
            return weights @ (-trial_lapse * (root + 1 / root - 2 * reference) / (2 * coupling)
                              - location * trial_lapse_r * (root - reference) / coupling
                              + trial_lapse * root * density)

        for degree in range(4):
            test = fraction**(degree + 1) * (1 - fraction)
            test_r = ((degree + 1) * fraction**degree * (1 - fraction) - fraction**(degree + 1)) / width
            step = 1e-24j
            lapse_force = hamiltonian(mass, lapse_values + step * test, lapse_r + step * test_r).imag / step.imag
            mass_force = -hamiltonian(mass + step * test, lapse_values, lapse_r).imag / step.imag
            predicted = weights @ (test * expected_rate)
            no_source_rate = -lapse_r / (coupling * arrays['U']) + lapse_values * mass / (coupling * location**2 * arrays['U']**3)
            results.append({'clock_branch': mode, 'test_degree': degree, 'lapse_action_constraint_error': float(abs(lapse_force)),
                            'mass_action_force_error': float(abs(mass_force - predicted)),
                            'missing_matter_force_negative_control': float(abs(mass_force - weights @ (test * no_source_rate)))})
    return results
