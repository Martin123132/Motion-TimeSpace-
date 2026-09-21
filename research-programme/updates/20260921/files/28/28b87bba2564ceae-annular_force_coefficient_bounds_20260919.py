from derive_annular_source_gravity_20260914 import EvidenceRun
from scipy.linalg import solve_banded
import numpy as np


def kinetic_weights(layer, position):
    radius, jacobian, unused = layer.mapping(layer.reference_radius, position)
    return layer.reference_weight*jacobian*radius**4/layer.coefficient(0., radius)


def quadrature_values(layer, nodal):
    return np.sum(layer.reference_shape*nodal[layer.reference_indices], axis=1)


def assemble_load(layer, quadrature):
    return layer.assemble_quadratic(layer.reference_indices, layer.reference_shape*quadrature[:, None])


def geometry_pairing(layer, first, last, response_first, response_last, weight_first, weight_last, factor, mask):
    row_covector = last['weights']*factor*mask
    covector = np.asarray(layer.lifted.T @ row_covector).ravel()
    dual = solve_banded((2, 2), last['bands'], covector, check_finite=False)
    dual_values = quadrature_values(layer, dual)
    responses_first = response_first['response']
    responses_last = response_last['response']
    side_values = np.column_stack([layer.reference_radius < layer.anchor, layer.reference_radius > layer.anchor])
    first_values = np.column_stack([quadrature_values(layer, responses_first[:, side]) for side in range(2)])
    defects = side_values-first_values
    relative_change = (weight_last-weight_first)/weight_last
    results, arrays = [], {}
    for side in range(2):
        residual = assemble_load(layer, (weight_last-weight_first)*defects[:, side])
        correction = solve_banded((2, 2), last['bands'], residual, check_finite=False)
        direct = responses_last[:, side]-responses_first[:, side]
        mass_terms = (weight_last-weight_first)*dual_values*defects[:, side]
        gram_terms = mask*(last['weights']-first['weights'])*factor*(layer.lifted @ responses_first[:, side])
        mass_bound = float(np.sqrt(covector @ dual)*np.sqrt(np.sum(weight_last*(relative_change*defects[:, side])**2)))
        coefficient_first = float(np.sum(mask*first['weights']*factor*(layer.lifted @ responses_first[:, side])))
        coefficient_last = float(np.sum(mask*last['weights']*factor*(layer.lifted @ responses_last[:, side])))
        results.append(dict(side=side, coefficient_change=coefficient_last-coefficient_first,
            mass_response_pairing=float(np.sum(mass_terms)), gram_weight_pairing=float(np.sum(gram_terms)),
            localized_mass_bound=float(np.sum(abs(mass_terms))), localized_gram_bound=float(np.sum(abs(gram_terms))),
            weighted_projection_defect_bound=mass_bound, maximum_relative_weight_change=float(max(abs(relative_change))),
            response_identity_maximum_error=float(max(abs(direct-correction))), valid_for_claim=False))
        arrays['side'+str(side)+'_mass_terms'] = mass_terms
        arrays['side'+str(side)+'_gram_terms'] = gram_terms
    return results, arrays


def off_space_peano(layer, source_model, values):
    element_indices = source_model.element_indices
    nodal = values[np.maximum(element_indices, 0)]*(element_indices >= 0)
    lengths = np.diff(source_model.edges)
    left_gradient = nodal @ np.array([-3., 4., -1.])/lengths
    right_gradient = nodal @ np.array([1., -4., 3.])/lengths
    curvature = nodal @ np.array([4., -8., 4.])/lengths**2
    atoms = np.zeros(len(source_model.edges))
    atoms[1:-1] = left_gradient[1:]-right_gradient[:-1]
    source = int(np.searchsorted(source_model.edges, source_model.anchor))
    source_jump = float(source_model.jump @ values)
    jump_error = abs(atoms[source]-source_jump)
    atoms[source] = 0.
    curvature_scale = abs(nodal) @ np.array([4., 8., 4.])/lengths**2
    atom_scale = np.zeros(len(source_model.edges))
    atom_scale[1:-1] = (abs(nodal[1:]) @ np.array([3., 4., 1.])/lengths[1:]
        +abs(nodal[:-1]) @ np.array([1., 4., 3.])/lengths[:-1])
    atom_scale[source] = 0.
    indices, shape, unused = source_model.features_quadratic(layer.radii)
    samples = np.sum(shape*values[indices], axis=1)
    original = layer.original.tocsr()
    count = original.shape[0]
    regular, singular, moments, tolerances = [np.zeros(count) for unused in range(4)]
    for row in range(count):
        start, end = original.indptr[row:row+2]
        columns = original.indices[start:end]
        if not len(columns):
            continue
        coefficients = original.data[start:end]
        radii = layer.radii[columns]
        lower, upper = min(radii), max(radii)
        interior = source_model.edges[(source_model.edges > lower) & (source_model.edges < upper)]
        cuts = np.unique(np.concatenate([radii, interior]))
        kernel = np.maximum(radii[:, None]-cuts[None, :], 0.).T @ coefficients
        middles = (cuts[:-1]+cuts[1:])/2
        elements = np.clip(np.searchsorted(source_model.edges, middles, side='right')-1, 0, len(lengths)-1)
        integrals = np.diff(cuts)*(kernel[:-1]+kernel[1:])/2
        regular[row] = curvature[elements] @ integrals
        selected = (source_model.edges > lower) & (source_model.edges <= upper)
        atom_kernel = np.maximum(radii[:, None]-source_model.edges[selected][None, :], 0.).T @ coefficients
        singular[row] = atoms[selected] @ atom_kernel
        indices, basis, radial = source_model.features_quadratic(np.array([lower]))
        initial_value = float(np.sum(basis*values[indices]))-source_jump*max(lower-source_model.anchor, 0.)
        initial_gradient = float(np.sum(radial*values[indices]))-source_jump*(lower >= source_model.anchor)
        moments[row] = initial_value*np.sum(coefficients)+initial_gradient*(coefficients @ (radii-lower))
        arithmetic = np.sum(abs(coefficients)*abs(samples[columns]))+abs(layer.lifted_hinge[row]*source_jump)
        arithmetic += curvature_scale[elements] @ abs(integrals)+atom_scale[selected] @ abs(atom_kernel)
        arithmetic += abs(initial_value)*np.sum(abs(coefficients))+abs(initial_gradient)*(abs(coefficients) @ abs(radii-lower))
        tolerances[row] = 600*np.finfo(float).eps*arithmetic+jump_error*abs(layer.lifted_hinge[row])+1e-23
    actual = layer.original @ samples-layer.lifted_hinge*source_jump
    return dict(regular=regular, ordinary_jumps=singular, polynomial_moments=moments, tolerance=tolerances,
        actual=actual, source_jump_identity_error=jump_error)
