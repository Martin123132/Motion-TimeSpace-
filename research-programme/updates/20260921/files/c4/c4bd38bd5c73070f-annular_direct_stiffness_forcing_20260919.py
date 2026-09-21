from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_action_test_energy_20260919 import whiten, operator_bound
from scipy.linalg import solve_banded, solve_triangular
import numpy as np


def transfer_rate(coarse_bands, fine_mass, coarse_mass_rate, fine_mass_rate,
                  coarse_stiffness, fine_stiffness, coarse_stiffness_rate, fine_stiffness_rate,
                  interpolation, values, velocity):
    transport = solve_banded((2, 2), coarse_bands, interpolation.T @ fine_mass, check_finite=False).T
    transport_rate = solve_banded((2, 2), coarse_bands,
        (fine_mass_rate @ interpolation-transport @ coarse_mass_rate).T, check_finite=False).T
    mismatch = transport @ coarse_stiffness-fine_stiffness @ interpolation
    mismatch_rate = transport_rate @ coarse_stiffness+transport @ coarse_stiffness_rate-fine_stiffness_rate @ interpolation
    inverse_load = solve_banded((2, 2), coarse_bands, coarse_stiffness @ values, check_finite=False)
    channels = dict(fine_mass_transport=fine_mass_rate @ interpolation @ inverse_load,
        coarse_mass_transport=-transport @ coarse_mass_rate @ inverse_load,
        coarse_stiffness_transport=transport @ coarse_stiffness_rate @ values,
        fine_stiffness_transport=-fine_stiffness_rate @ interpolation @ values,
        coarse_trial_velocity=transport @ coarse_stiffness @ velocity,
        fine_trial_velocity=-fine_stiffness @ interpolation @ velocity)
    return dict(transport=transport, transport_rate=transport_rate, mismatch=mismatch, mismatch_rate=mismatch_rate,
        derivative=mismatch @ velocity+mismatch_rate @ values, channels=channels,
        paired_velocity=mismatch @ velocity, paired_geometry=mismatch_rate @ values)


def dual_norm(lower, load):
    return float(np.linalg.norm(solve_triangular(lower, load, lower=True, check_finite=False)))


def forcing_constant(matrix, fine_mass_lower, coarse_stiffness_lower):
    if not np.any(matrix):
        return dict(sharp=0., upper=0., eigen_residual=0.)
    scaled = whiten(matrix, fine_mass_lower, coarse_stiffness_lower)
    result, unused = operator_bound(scaled.T)
    return dict(sharp=float(np.sqrt(max(result['sharp_squared'],0.))),
        upper=float(np.sqrt(max(result['row_sum_squared_bound'],0.))), eigen_residual=result['eigen_residual'])
