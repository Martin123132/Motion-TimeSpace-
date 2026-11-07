from common231 import *


def eos_at(mixture, theta_star, ratio, kind='EOS'):
    if kind == 'NR':
        return dict(A=float(ratio), C=1., C_R=0., A_s_fixed_R=0.)
    state = mixture.state(theta_star, ratio)
    nodes, weights = prior.prior.radial_rule(32)
    theta = theta_star * ratio
    measure = weights * (1 + theta * nodes) * np.sqrt(2 + theta * nodes)
    measure /= measure.sum()
    mean = np.dot(measure, nodes)
    variance = np.dot(measure, (nodes - mean)**2)
    third = np.dot(measure, (nodes - mean)**3)
    capacity_R = (2 / 3) * mixture.fractions[0] * (third - 2 * variance) / ratio
    return dict(A=float(state['A']), C=float(state['C']), C_R=float(capacity_R),
                A_s_fixed_R=float(state['A'] - ratio * state['C']))


def gas_coefficients(hubble, rest_over_reference, heat, ratio, eos, photon_transfer):
    energy, capacity, capacity_R = eos['A'], eos['C'], eos['C_R']
    if min(hubble, rest_over_reference, heat, ratio, capacity) <= 0:
        raise ValueError('Positive physical background required')
    ratio_prime = hubble * ratio - (2 * hubble * ratio + photon_transfer / heat) / capacity
    energy_prime = hubble * (energy - ratio * capacity) + capacity * ratio_prime
    capacity_prime = capacity_R * (ratio_prime - hubble * ratio)
    inertia = rest_over_reference + heat * (energy + 2 * ratio / 3)
    inertia_prime = hubble * rest_over_reference + heat * (energy_prime + 2 * ratio_prime / 3)
    sound_squared = (2 * heat * ratio / 3) * (1 + 2 / (3 * capacity)) / inertia
    return dict(R=ratio, A=energy, C=capacity, C_R=capacity_R, chi=heat, H=hubble,
                Q=photon_transfer, rest=rest_over_reference, B=inertia, B_prime=inertia_prime,
                R_prime=ratio_prime, A_prime=energy_prime, C_prime=capacity_prime,
                temperature_self=hubble - 2 * hubble / capacity - capacity_prime / capacity,
                sound_squared=sound_squared)


def source_rows(local, density_row, compression_row, temperature_row, velocity_row,
                photon_energy_row, photon_momentum_row, wave_number):
    heat, ratio, capacity = local['chi'], local['R'], local['C']
    density = (local['rest'] + heat * local['A']) * density_row + heat * capacity * temperature_row
    pressure = (2 * heat / 3) * (ratio * density_row + temperature_row)
    current = local['B'] * velocity_row
    temperature = (local['temperature_self'] * temperature_row - 2 * ratio * compression_row / (3 * capacity)
                   - (photon_energy_row - local['Q'] * density_row) / (heat * capacity))
    velocity = (-photon_momentum_row - local['B_prime'] * velocity_row - 1j * wave_number * pressure) / local['B']
    return dict(density=density, pressure=pressure, current=current, temperature=temperature, velocity=velocity)


def stress_chain_derivatives(local, state, derivative, observed_ratio_prime):
    density, temperature, velocity = state
    density_prime, temperature_prime, velocity_prime = derivative
    heat, hubble, ratio = local['chi'], local['H'], local['R']
    energy_prime = hubble * (local['A'] - ratio * local['C']) + local['C'] * observed_ratio_prime
    capacity_prime = local['C_R'] * (observed_ratio_prime - hubble * ratio)
    inertia_prime = hubble * local['rest'] + heat * (energy_prime + 2 * observed_ratio_prime / 3)
    gas_density = (local['rest'] + heat * local['A']) * density + heat * local['C'] * temperature
    gas_density_prime = (local['rest'] * (density_prime - 3 * hubble * density)
        + heat * ((energy_prime - 4 * hubble * local['A']) * density + local['A'] * density_prime
        + (capacity_prime - 4 * hubble * local['C']) * temperature + local['C'] * temperature_prime))
    current_prime = local['B'] * velocity_prime + (inertia_prime - 4 * hubble * local['B']) * velocity
    return gas_density, gas_density_prime, current_prime


def defect_sources(local, ratio_defect, density, temperature, velocity):
    energy = local['chi'] * ratio_defect * (local['C'] * density + local['C_R'] * temperature)
    momentum = local['chi'] * (local['C'] + 2 / 3) * ratio_defect * velocity
    return energy, momentum


def field_defect_sources(scale, mass, position_defect, momentum_defect, delta_position, delta_momentum, wave_number):
    energy = np.sum(momentum_defect * delta_momentum / scale**2 + mass**2 * position_defect * delta_position)
    current = -1j * wave_number * np.sum(momentum_defect * delta_position) / scale**2
    return energy, current


def constraint_forcing(scale, spatial_trace, raychaudhuri_defect, energy_defect, momentum_defect):
    return np.array([4 * spatial_trace * raychaudhuri_defect - 2 * scale**2 * energy_defect,
                     -scale**2 * momentum_defect])
