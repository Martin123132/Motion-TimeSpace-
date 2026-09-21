from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_weighted_projection_bounds_20260919 import band_action
from scipy.linalg import solve_banded
import numpy as np


def canonical_residual_split(coarse, fine, coarse_momenta, fine_momenta, coarse_rates, fine_rates, transfer):
    coarse_bands, fine_bands = coarse['mass_bands'], fine['mass_bands']
    coarse_cross, fine_cross = coarse['cross'], fine['cross']
    coarse_inverse_residual = coarse_momenta-band_action(coarse_bands, coarse_rates[:-1])-coarse_cross*coarse_rates[-1]
    fine_inverse_residual = fine_momenta-band_action(fine_bands, fine_rates[:-1])-fine_cross*fine_rates[-1]
    solved = solve_banded((2, 2), coarse_bands,
        np.column_stack([coarse_momenta, coarse_cross, coarse_inverse_residual]), check_finite=False)
    momentum_load = fine_momenta-band_action(fine_bands, transfer(solved[:, 0]))
    source_load = -fine_cross*fine_rates[-1]+band_action(fine_bands, transfer(solved[:, 1]*coarse_rates[-1]))
    coarse_inverse_velocity = transfer(solved[:, 2])
    fine_inverse_velocity = solve_banded((2, 2), fine_bands, fine_inverse_residual, check_finite=False)
    direct_residual = fine_momenta-fine_cross*fine_rates[-1]-band_action(fine_bands, transfer(coarse_rates[:-1]))
    corrected_load = direct_residual-fine_inverse_residual
    correction = solve_banded((2, 2), fine_bands, corrected_load, check_finite=False)
    direct_velocity = fine_rates[:-1]-transfer(coarse_rates[:-1])
    split_load = momentum_load+source_load+band_action(fine_bands, coarse_inverse_velocity)-fine_inverse_residual
    return dict(momentum_load=momentum_load, source_load=source_load, corrected_load=corrected_load,
        coarse_inverse_velocity=coarse_inverse_velocity, fine_inverse_velocity=fine_inverse_velocity,
        fine_inverse_residual=fine_inverse_residual, coarse_inverse_residual=coarse_inverse_residual,
        correction=correction, direct_velocity=direct_velocity, split_load=split_load,
        raw_residual=direct_residual,
        maximum_inverse_residual=float(max(np.max(abs(fine_inverse_residual)), np.max(abs(coarse_inverse_residual)))),
        velocity_reconstruction_error=float(max(abs(correction-direct_velocity))),
        load_split_error=float(max(abs(split_load-corrected_load))))


def driver_pairing(fine_bands, split, covector):
    solved = solve_banded((2, 2), fine_bands, np.column_stack([split['corrected_load'], covector]), check_finite=False)
    correction, dual = solved[:, 0], solved[:, 1]
    pairing = float(dual @ split['corrected_load'])
    residual_square = float(split['corrected_load'] @ correction)
    dual_square = float(covector @ dual)
    if min(residual_square, dual_square) < 0:
        raise ValueError('Positive mass norm required.')
    result = dict(momentum_channel=float(dual @ split['momentum_load']),
        source_cross_channel=float(dual @ split['source_load']),
        coarse_inverse_channel=float(covector @ split['coarse_inverse_velocity']),
        fine_inverse_channel=float(-covector @ split['fine_inverse_velocity']),
        residual_pairing=pairing, direct_velocity_pairing=float(covector @ split['direct_velocity']),
        corrected_residual_localized_bound=float(np.sum(abs(dual*split['corrected_load']))),
        corrected_residual_mass_bound=float(np.sqrt(residual_square)*np.sqrt(dual_square)),
        momentum_localized_bound=float(np.sum(abs(dual*split['momentum_load']))),
        source_cross_localized_bound=float(np.sum(abs(dual*split['source_load']))),
        coarse_inverse_absolute_bound=float(np.sum(abs(covector*split['coarse_inverse_velocity']))),
        fine_inverse_absolute_bound=float(np.sum(abs(covector*split['fine_inverse_velocity']))),
        valid_for_claim=False)
    return result, dual
