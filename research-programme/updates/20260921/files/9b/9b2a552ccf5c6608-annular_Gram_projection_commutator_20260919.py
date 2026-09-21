from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_weighted_projection_bounds_20260919 import band_action
from scipy.linalg import solve_banded, cholesky_banded
import numpy as np


def field_extension(layer, source_model, source_values, position):
    indices, shape, unused = source_model.features_quadratic(layer.radii)
    samples = np.sum(shape*source_values[:-1][indices], axis=1)
    indices, unused, radial = source_model.features_quadratic(layer.reference_radius)
    reference_gradient = np.sum(radial*source_values[:-1][indices], axis=1)
    radius, jacobian, motion = layer.mapping(layer.reference_radius, position)
    kinetic = layer.reference_weight*jacobian*radius**4/layer.coefficient(0., radius)
    load = layer.assemble_quadratic(layer.reference_indices,
        layer.reference_shape*((-motion/jacobian)*kinetic*reference_gradient)[:, None])
    coordinates = np.append(samples, position)
    original = layer.evaluate(0., coordinates, np.zeros_like(coordinates))
    bands = original['mass_bands']
    factorization = cholesky_banded(bands[:3], lower=False, check_finite=False)
    projection = solve_banded((2, 2), bands, load, check_finite=False)
    radius, jacobian, unused = layer.mapping(layer.radii, position)
    weights = np.asarray(layer.sampling @ (layer.coefficient(0., radius)/jacobian))/layer.gram_spacing
    radius, jacobian, unused = layer.mapping(layer.radii, complex(position, 1e-24))
    derivative = np.asarray(layer.sampling @ (layer.coefficient(0., radius)/jacobian)).imag/(1e-24*layer.gram_spacing)
    factor = layer.original @ samples-layer.lifted_hinge*(source_model.jump @ source_values[:-1])
    shape_rows = -.5*derivative*factor**2
    projected_rows = weights*factor*(layer.lifted @ projection)
    stencil = abs(layer.original)
    source_rows = (np.asarray(stencil @ (layer.radii < layer.anchor)).ravel() > 0)
    source_rows &= np.asarray(stencil @ (layer.radii > layer.anchor)).ravel() > 0
    return dict(samples=samples, bands=bands, load=load, projection=projection, factor=factor,
        weights=weights, derivative=derivative, shape_rows=shape_rows, projected_rows=projected_rows,
        source_rows=source_rows, minimum_cholesky_diagonal=float(min(factorization[-1])))


def mass_pairing(bands, residual, covector):
    solved = solve_banded((2, 2), bands, np.column_stack([residual, covector]), check_finite=False)
    correction, dual = solved[:, 0], solved[:, 1]
    residual_energy = float(residual @ correction)
    dual_energy = float(covector @ dual)
    if min(residual_energy, dual_energy) < 0:
        raise ValueError('Negative mass-dual quadratic form.')
    pairing = float(covector @ correction)
    dual_terms = dual*residual
    bound = float(np.sqrt(residual_energy)*np.sqrt(dual_energy))
    result = dict(projection_force=pairing, dual_residual_pairing=float(np.sum(dual_terms)),
        dual_residual_absolute_bound=float(np.sum(abs(dual_terms))), dual_mass_bound=bound,
        residual_dual_mass_norm=float(np.sqrt(residual_energy)), covector_dual_mass_norm=float(np.sqrt(dual_energy)),
        signed_mass_alignment=pairing/bound if bound > 0 else None,
        mass_bound_over_absolute_force=bound/abs(pairing) if pairing != 0 else None,
        dual_residual_solve_error=float(np.linalg.norm(band_action(bands, dual)-covector)),
        correction_solve_error=float(np.linalg.norm(band_action(bands, correction)-residual)), valid_for_claim=False)
    return result, dict(correction=correction, dual=dual, dual_terms=dual_terms)
