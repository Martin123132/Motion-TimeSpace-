from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_weighted_projection_bounds_20260919 import band_action
from scipy.linalg import solve_banded
import numpy as np


def compensated_acceleration(data, rates, scalar_force, mass_rate, cross_rate, source_acceleration, inverse_residual_rate):
    loads = dict(canonical_force=scalar_force, cross_transport=-cross_rate*rates[-1],
        source_acceleration=-data['cross']*source_acceleration,
        mass_transport=-band_action(mass_rate, rates[:-1]), inverse_residual=-inverse_residual_rate)
    names = list(loads)
    solved = solve_banded((2, 2), data['mass_bands'], np.column_stack([loads[name] for name in names]), check_finite=False)
    combined = sum(loads.values())
    acceleration = solve_banded((2, 2), data['mass_bands'], combined, check_finite=False)
    return dict(acceleration=acceleration, load=combined, channels=dict(zip(names, solved.T)))


def inverse_residual(data, rates, momenta):
    return momenta-band_action(data['mass_bands'], rates[:-1])-data['cross']*rates[-1]


def velocity_energy_rate(mass_bands, mass_rate, velocity_difference, acceleration_difference):
    energy = .5*float(velocity_difference @ band_action(mass_bands, velocity_difference))
    forcing = float(velocity_difference @ band_action(mass_bands, acceleration_difference))
    metric = .5*float(velocity_difference @ band_action(mass_rate, velocity_difference))
    return dict(energy=energy, forcing_rate=forcing, mass_rate=metric, total_rate=forcing+metric,
        absolute_bound=float(np.sum(abs(velocity_difference*band_action(mass_bands, acceleration_difference)))
            +.5*np.sum(abs(velocity_difference*band_action(mass_rate, velocity_difference)))))
