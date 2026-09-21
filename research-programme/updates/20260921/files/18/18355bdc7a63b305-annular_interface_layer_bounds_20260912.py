import numpy as np


def limit_bounds(radius, mass_left, lapse_left, energy, width):
    coupling = .1
    lower_radius = radius - width / 2
    upper_mass = mass_left + coupling * energy
    lower_F = 1 - 2 * upper_mass / lower_radius
    initial_lower_F = 1 - 2 * mass_left / lower_radius
    if min(lower_radius, lower_F, initial_lower_F) <= 0:
        raise ValueError('The analytic positivity bound does not cover this layer.')
    maximum_background = upper_mass / (lower_radius**2 * lower_F)
    initial_log_error = width * mass_left / (2 * lower_radius**2 * initial_lower_F)
    source_exponent_error = coupling * energy * width / (2 * radius * lower_radius)
    G_error = width * maximum_background + source_exponent_error
    log_error = initial_log_error + G_error
    zeta = coupling * energy / radius
    root_left = np.sqrt(1 - 2 * mass_left / radius)
    root_limit = root_left * np.exp(-zeta)
    mean_limit = root_left * (-np.expm1(-zeta)) / zeta
    momentum_limit = lapse_left * np.expm1(zeta) / (coupling * root_left)
    radial_log_error = np.log(radius / lower_radius)
    momentum_error = width * lapse_left * maximum_background / (coupling * np.sqrt(lower_F))
    momentum_error += momentum_limit * np.expm1(log_error + radial_log_error)
    return {'root_limit_error': float(root_limit * np.expm1(log_error)),
            'mass_limit_error': float(radius * root_limit**2 * np.expm1(2 * log_error) / 2 + width / 4),
            'mean_limit_error': float(mean_limit * np.expm1(log_error)),
            'G_limit_error': float(G_error),
            'P1_integral_limit_error': float(momentum_error),
            'analytic_lower_F': float(lower_F), 'maximum_background': float(maximum_background),
            'pointwise_log_U_limit_error': float(log_error)}
