from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_source_centered_quadrature_20260929 import CenteredLabelDensity, reference_offsets
from annular_registered_metric_coordinates_20260929 import metric_at_offset, response_at_offset
from annular_candidate_coordinate_covectors_20260921 import local_polynomials
from annular_physical_native_kernel_20260928 import decimals
from time import perf_counter
import numpy as np


def force_integrals(loads, action, directions, correction, mode_rate, position,
                    radial_order, label_order, deadline, progress):
    names = ['base_force', 'position_force', 'oracle_difference']
    ordinary = {name: np.zeros_like(loads.rates) for name in names}
    accumulated = {name: np.zeros_like(loads.rates) for name in names}
    compensation = {name: np.zeros_like(loads.rates) for name in names}
    anchor = float(action.owner.model.anchor)
    edges = reference_offsets(action)
    widths = np.asarray([float(right-left) for left, right in zip(action.edges[:-1], action.edges[1:])])
    field_direction = directions['field_vertices'] - correction[:, :-1]
    field_gradient = local_polynomials(action.mesh, decimals(field_direction.T))[1]
    mode_polynomial = local_polynomials(action.mesh, decimals(mode_rate[:, :-1].T))[0]
    points, weights = np.polynomial.legendre.leggauss(radial_order)
    radial_edges = action.solver.edges-anchor
    centers = (radial_edges[:-1]+radial_edges[1:])/2
    radii = (centers[:, None]+action.solver.lengths[:, None]*points/2).ravel()
    radial_weights = (action.solver.lengths[:, None]*weights/2).ravel()
    element_indices = np.asarray(action.mesh['elements'])
    for start in range(0, len(radii), 16):
        if perf_counter() > deadline:
            raise RuntimeError('Safe compensated field-force boundary')
        section = slice(start, start+16)
        density = CenteredLabelDensity(action, radii[section], label_order)
        labels, cardinal = density.offsets, density.interpolation
        radius_offset = radii[section][density.indices]
        radius = anchor+radius_offset
        source_offset = density.source_offset(labels)
        inner, outer = edges[0]+action.owner.width*labels, edges[-1]+action.owner.width*labels
        jacobian = np.where(radius_offset < source_offset,
            1+(source_offset-action.owner.width*labels)/(-edges[0]),
            1-(source_offset-action.owner.width*labels)/edges[-1])
        reference = (radius_offset-source_offset)/jacobian
        active = (radius_offset >= inner) & (radius_offset <= outer)
        cells = np.clip(np.searchsorted(edges, reference, side='right')-1, 0, len(edges)-2)
        local = (reference-edges[cells])/widths[cells]
        indices = element_indices[cells]
        selected = (indices >= 0) & active[:, None]
        test_gradient = np.column_stack([4*local-3, 4-8*local, 4*local-1])/(widths[cells]*jacobian)[:, None]*selected

        def evaluate(polynomial):
            coefficients = np.einsum('qpl,ql->qp', polynomial[cells], cardinal, optimize=False)
            if coefficients.shape[1] == 2:
                return coefficients[:, 0]+local*coefficients[:, 1]
            return coefficients[:, 0]+local*(coefficients[:, 1]+local*coefficients[:, 2])

        gradient_reference = evaluate(action.gradient)
        gradient_direction = evaluate(field_gradient)
        rate = evaluate(action.rate_polynomial)
        rate_direction = evaluate(mode_polynomial)
        source_mode = -(cardinal @ correction[:, -1])
        source_rate = cardinal @ mode_rate[:, -1]
        velocity = cardinal @ action.velocity
        displacement = np.where(reference < 0., 1+reference/(-edges[0]), 1-reference/edges[-1])
        displacement_xi = np.where(reference < 0., 1/(-edges[0]), -1/edges[-1])
        eta_left = np.einsum('ql,lq->q', cardinal, directions['edge_vertices'][:, cells], optimize=False)
        eta_right = np.einsum('ql,lq->q', cardinal, directions['edge_vertices'][:, cells+1], optimize=False)
        movement = (1-local)*eta_left+local*eta_right+displacement*source_mode
        movement_r = ((eta_right-eta_left)/widths[cells]+displacement_xi*source_mode)/jacobian
        speed, speed_direction = displacement*velocity, displacement*source_rate
        values, radial = metric_at_offset(action.solver, action.solution, radius_offset, anchor)
        position_values = response_at_offset(position, radius_offset, anchor)[0]
        mass, nu = values
        mass_direction, nu_direction = position_values+radial*movement
        metric = 1-2*mass/radius
        metric_direction = -2*mass_direction/radius+2*mass*movement/radius**2
        alpha = radius**2/(np.exp(nu)*np.sqrt(metric))
        beta = radius**2*np.exp(nu)*np.sqrt(metric)
        alpha_direction = alpha*(2*movement/radius-nu_direction-metric_direction/(2*metric))
        beta_direction = beta*(2*movement/radius+nu_direction+metric_direction/(2*metric))
        gradient = gradient_reference/jacobian
        gradient_change = gradient_direction/jacobian-gradient*movement_r
        temporal = rate-speed*gradient
        temporal_change = rate_direction-speed_direction*gradient-speed*gradient_change
        flux = alpha*temporal*speed+beta*gradient
        flux_change = alpha_direction*temporal*speed+alpha*temporal_change*speed
        flux_change += alpha*temporal*speed_direction+beta_direction*gradient+beta*gradient_change
        amount, step = 1e-25j, 1e-25
        changed_radius = radius+amount*movement
        changed_metric = 1-2*(mass+amount*mass_direction)/changed_radius
        changed_alpha = changed_radius**2/(np.exp(nu+amount*nu_direction)*np.sqrt(changed_metric))
        changed_beta = changed_radius**2*np.exp(nu+amount*nu_direction)*np.sqrt(changed_metric)
        changed_gradient = (gradient_reference+amount*gradient_direction)/(jacobian*(1+amount*movement_r))
        changed_speed = speed+amount*speed_direction
        changed_temporal = rate+amount*rate_direction-changed_speed*changed_gradient
        oracle = (changed_alpha*changed_temporal*changed_speed+changed_beta*changed_gradient).imag/step
        measure = radial_weights[section][density.indices]*density.label_weights*active
        for name, value in [('base_force', -flux), ('position_force', -flux_change), ('oracle_difference', oracle-flux_change)]:
            block = np.zeros_like(loads.rates)
            for column in range(3):
                mask = selected[:, column]
                factors = measure[mask]*value[mask]*test_gradient[mask, column]
                deposits = factors[:, None]*cardinal[mask]
                np.add.at(ordinary[name].T, indices[mask, column], deposits)
                np.add.at(block.T, indices[mask, column], deposits)
            total = accumulated[name]+block
            compensation[name] += np.where(np.abs(accumulated[name]) >= np.abs(block),
                (accumulated[name]-total)+block, (block-total)+accumulated[name])
            accumulated[name] = total
        if start % 2048 == 0:
            progress('force-'+str(radial_order)+'-'+str(label_order)+':'+str(start)+'/'+str(len(radii)))
    return dict(**{'ordinary_'+name: ordinary[name] for name in names},
        **{'compensated_'+name: accumulated[name]+compensation[name] for name in names})
