from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_weighted_projection_bounds_20260919 import band_action
from annular_compatible_current_restoring_20260909 import unit_gram_template
from scipy.linalg import solve_banded
from fractions import Fraction
import numpy as np


TEMPLATE_BOUND = float(Fraction(59097, 573104)+Fraction(1, 56))


def source_mask(model):
    stencil = abs(model.original)
    return (np.asarray(stencil @ (model.radii < model.anchor)).ravel() > 0) & (np.asarray(stencil @ (model.radii > model.anchor)).ravel() > 0)


def adjoint_test(coarse_bands, fine_bands, test, indices, shape, coarse_count):
    fine_load = band_action(fine_bands, test)
    coarse_load = np.zeros(coarse_count)
    np.add.at(coarse_load, indices.ravel(), (shape*fine_load[:, None]).ravel())
    result = solve_banded((2, 2), coarse_bands, coarse_load, check_finite=False)
    return result, coarse_load


def norm_bounds(model, weights, values):
    jump = float(model.jump @ values)
    hinge = np.maximum(model.radii-model.anchor, 0.)
    detrended = values-jump*hinge
    actual = np.asarray(model.lifted @ values).ravel()
    centered = np.asarray(model.original @ detrended).ravel()
    arithmetic_norm = float(np.sqrt(np.sum(weights*(actual-centered)**2)))
    base_indices = np.searchsorted(model.radii, model.base_radii)
    third = np.diff(detrended[base_indices], n=3)
    spacing = model.gram_spacing
    coefficient_max = float(np.max(weights*spacing, initial=0.))
    derivative = np.sum(model.reference_radial*values[model.reference_indices], axis=1)
    derivative -= jump*(model.reference_radius > model.anchor)
    gradient_square = float(np.sum(model.reference_weight*derivative**2))
    raw_gradient = np.sum(model.reference_radial*values[model.reference_indices], axis=1)
    raw_gradient_square = float(np.sum(model.reference_weight*raw_gradient**2))
    third_seminorm = float(np.sum(third**2)/spacing**5)
    margins, adjacent, extras = unit_gram_template(model.base_count)
    pieces = [np.sqrt(margins)*third, np.sqrt(abs(adjacent))*(third[:-1]+np.sign(adjacent)*third[1:])]
    pieces.append(np.array([np.sqrt(abs(weight))*(third[first]+np.sign(weight)*third[second]) for first, second, weight in extras]))
    reconstructed = np.concatenate(pieces) if len(weights) else np.zeros(0)
    template_arithmetic_norm = float(np.sqrt(np.sum(weights*(centered-reconstructed)**2)))
    arithmetic_norm += template_arithmetic_norm
    row_sums = margins.copy()
    row_sums[:-1] += 2*abs(adjacent)
    row_sums[1:] += 2*abs(adjacent)
    for first, second, weight in extras:
        row_sums[[first, second]] += 2*abs(weight)
    spectral_bound = float(max(row_sums))
    return dict(Gram_norm=float(np.sqrt(np.sum(weights*actual**2))),
        discrete_third_difference_bound=float(spacing**2*np.sqrt(TEMPLATE_BOUND*coefficient_max*third_seminorm)+arithmetic_norm),
        lifted_H1_bound=float(4*np.sqrt(TEMPLATE_BOUND*coefficient_max*gradient_square)+arithmetic_norm),
        lifted_H1_norm=float(np.sqrt(gradient_square)), raw_H1_norm=float(np.sqrt(raw_gradient_square)),
        source_jump=jump, discrete_third_seminorm_squared=third_seminorm,
        template_row_bound=spectral_bound, uniform_template_bound=TEMPLATE_BOUND,
        coefficient_max=coefficient_max, floating_lift_norm_correction=arithmetic_norm,
        floating_template_norm_correction=template_arithmetic_norm,
        spacing=spacing, valid_for_claim=False)
