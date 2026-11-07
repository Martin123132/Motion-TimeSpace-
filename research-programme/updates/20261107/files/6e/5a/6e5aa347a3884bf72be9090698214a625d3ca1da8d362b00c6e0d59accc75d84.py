import numpy as np


def explicit_time_forcing(radius, mass, log_lapse, source_density, velocity,
        temporal_square_rate, gradient_square_rate, gram_rate, source_density_rate, velocity_rate,
        coupling, source_mass):
    metric = 1 - 2 * mass / radius
    lapse = np.exp(log_lapse)
    clock_square = lapse**2 - velocity**2 / metric
    root, clock = np.sqrt(metric), np.sqrt(clock_square)
    density_rate = temporal_square_rate / (2 * lapse**2 * metric) + gradient_square_rate / 2 + gram_rate
    mass_density_partial = coupling * source_mass * root * lapse / clock
    lapse_density_partial = coupling * source_mass * velocity**2 / (radius * lapse * root**3 * clock)
    mass_velocity_partial = coupling * source_mass * source_density * lapse * velocity / (root * clock**3)
    lapse_velocity_partial = coupling * source_mass * source_density / (radius * lapse * root**3)
    lapse_velocity_partial *= 2 * velocity / clock + velocity**3 / (metric * clock**3)
    mass_forcing = coupling * radius**2 * metric * density_rate
    mass_forcing += mass_density_partial * source_density_rate + mass_velocity_partial * velocity_rate
    lapse_forcing = coupling * radius * density_rate
    lapse_forcing += lapse_density_partial * source_density_rate + lapse_velocity_partial * velocity_rate
    return np.stack([mass_forcing, lapse_forcing])
