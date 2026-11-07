from common238 import *


def lift(matrix, degree, basis, opacity, heat, capacity, inertia):
    mass = np.triu(basis.mass) + np.triu(basis.mass, 1).T
    factor = linalg.cho_factor(mass, lower=False)
    photon = (2 * degree + 1) * opacity * linalg.cho_solve(factor, matrix[1:-1])
    measured_moment = basis.energy @ photon / (2 * degree + 1)
    direct_moment = opacity * matrix[0]
    gas_moment = opacity * matrix[-1]
    denominator = heat * capacity if degree == 0 else inertia if degree == 1 else 1.
    gas_rate = gas_moment / denominator
    return dict(photon=photon, photon_moment=measured_moment, direct_moment=direct_moment,
        gas_moment=gas_moment, gas_rate=gas_rate, angular_mass_factor=2 * degree + 1)


def metric_response(port, degree, reference_density, scale, capacity):
    photon, gas = port['photon_moment'], port['gas_moment']
    energy = reference_density * (photon + gas) if degree == 0 else np.zeros_like(photon)
    current = reference_density * (photon + gas) if degree == 1 else np.zeros_like(photon)
    pressure = reference_density * (photon / 3 + 2 * gas / (3 * capacity)) if degree == 0 else np.zeros_like(photon)
    shear = reference_density * photon / 3 if degree == 2 else np.zeros_like(photon)
    transverse, longitudinal = pressure - shear, pressure + 2 * shear
    metric_transverse = scale**2 * (energy - longitudinal) / 2
    metric_longitudinal = scale**2 * (energy + longitudinal - 2 * transverse) / 2
    constraint = gravity.constraint_forcing(scale, 0., 0., energy, current)
    return dict(energy=energy, current=current, pressure=pressure, shear=shear,
        stress_transverse=transverse, stress_longitudinal=longitudinal,
        sigma_transverse_second=metric_transverse, sigma_longitudinal_second=metric_longitudinal,
        constraint_forcing=constraint)


def background_transfer_tangent(local, delta_transfer, delta_energy, delta_current, density, temperature, velocity):
    heat, capacity, capacity_R, inertia = local['chi'], local['C'], local['C_R'], local['B']
    temperature_rate = (-delta_energy + delta_transfer * density) / (heat * capacity)
    temperature_rate += capacity_R * delta_transfer * temperature / (heat * capacity**2)
    velocity_rate = (-delta_current + (1 + 2 / (3 * capacity)) * delta_transfer * velocity) / inertia
    ratio_defect = delta_transfer / (heat * capacity)
    energy_defect, current_defect = gravity.defect_sources(local, ratio_defect, density, temperature, velocity)
    return dict(temperature_rate=temperature_rate, velocity_rate=velocity_rate,
        ratio_defect=ratio_defect, energy_defect=energy_defect, current_defect=current_defect)


def normalization_error(value, reference, scale=None):
    denominator = np.linalg.norm(reference) if scale is None else scale
    return float(np.linalg.norm(np.asarray(value) - np.asarray(reference)) / max(float(denominator), 1e-300))
