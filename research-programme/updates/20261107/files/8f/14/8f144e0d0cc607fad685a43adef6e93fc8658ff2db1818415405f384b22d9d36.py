from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_position_reaction_20260929 import second_radial, metric_jets, jet_exp, material_position_reaction
from annular_position_time_loads_20260929 import MixedJet
from annular_old_field_reaction_20260929 import wave_packet
from annular_source_centered_quadrature_20260929 import CenteredLabelDensity, reference_offsets, metric_at_offset, response_at_offset
from annular_candidate_coordinate_covectors_20260921 import local_polynomials
from annular_physical_native_kernel_20260928 import decimals
from time import perf_counter
import numpy as np


def eulerian_field_reaction(loads, action, directions, correction, mode_rate, acceleration,
                            position, metric_time, mixed_time, radial_order, label_order,
                            deadline, progress, acceleration_change=None):
    names = ['momentum_rate', 'oracle_momentum_rate', 'force_wave', 'base_momentum', 'base_force_wave']
    output = {name: np.zeros_like(loads.rates) for name in names}
    material = loads.material
    material.owner.label_order = label_order
    model = material.owner.model
    anchor = float(model.anchor)
    edges = reference_offsets(action)
    widths = np.asarray([float(right - left) for left, right in zip(action.edges[:-1], action.edges[1:])])
    field_direction = directions['field_vertices'] - correction[:, :-1]
    field_poly, field_grad = local_polynomials(action.mesh, decimals(field_direction.T))
    mode_poly, mode_grad = local_polynomials(action.mesh, decimals(mode_rate[:, :-1].T))
    accel_poly = local_polynomials(action.mesh, decimals(acceleration[:, :-1].T))[0]
    acceleration_change = np.zeros_like(acceleration) if acceleration_change is None else acceleration_change
    reaction_poly = local_polynomials(action.mesh, decimals(acceleration_change[:, :-1].T))[0]
    points, weights = np.polynomial.legendre.leggauss(radial_order)
    radial_edges = action.solver.edges - anchor
    radial_centers = (radial_edges[:-1] + radial_edges[1:]) / 2
    radii = (radial_centers[:, None] + action.solver.lengths[:, None] * points / 2).ravel()
    radial_weights = (action.solver.lengths[:, None] * weights / 2).ravel()
    for start in range(0, len(radii), 16):
        if perf_counter() > deadline:
            raise RuntimeError('Safe Eulerian position reaction boundary')
        section = slice(start, start + 16)
        density = CenteredLabelDensity(action, radii[section], label_order)
        labels, cardinal = density.offsets, density.interpolation
        radius_offset = radii[section][density.indices]
        radius = anchor + radius_offset
        source_offset = density.source_offset(labels)
        velocity = cardinal @ action.velocity
        inner, outer = edges[0] + action.owner.width * labels, edges[-1] + action.owner.width * labels
        left = radius_offset < source_offset
        jacobian = np.where(left, 1 + (source_offset - action.owner.width * labels) / (-edges[0]),
            1 - (source_offset - action.owner.width * labels) / edges[-1])
        reference = (radius_offset - source_offset) / jacobian
        active = (radius_offset >= inner) & (radius_offset <= outer)
        cells = np.clip(np.searchsorted(edges, reference, side='right') - 1, 0, len(edges) - 2)
        local = (reference - edges[cells]) / widths[cells]
        indices = np.asarray(action.mesh['elements'])[cells]
        selected = (indices >= 0) & active[:, None]
        shape = np.column_stack([(1 - local) * (1 - 2 * local), 4 * local * (1 - local), local * (2 * local - 1)]) * selected
        test_gradient = np.column_stack([4 * local - 3, 4 - 8 * local, 4 * local - 1]) / (widths[cells] * jacobian)[:, None] * selected

        def evaluate(poly):
            coefficients = np.einsum('qpl,ql->qp', poly[cells], cardinal, optimize=False)
            if coefficients.shape[1] == 2:
                return coefficients[:, 0] + local * coefficients[:, 1]
            return coefficients[:, 0] + local * (coefficients[:, 1] + local * coefficients[:, 2])

        gradient_reference = evaluate(action.gradient)
        rate = evaluate(action.rate_polynomial)
        rate_gradient_poly = np.stack([action.rate_polynomial[:, 1] / widths[:, None],
            2 * action.rate_polynomial[:, 2] / widths[:, None]], axis=1)
        rate_reference_gradient = evaluate(rate_gradient_poly)
        field_reference_gradient = evaluate(field_grad)
        transported, transported_reference_gradient = evaluate(mode_poly), evaluate(mode_grad)
        old_accel, changed_accel = evaluate(accel_poly), evaluate(reaction_poly)
        source_mode = -(cardinal @ correction[:, -1])
        source_rate = cardinal @ mode_rate[:, -1]
        source_accel = cardinal @ acceleration[:, -1]
        source_accel_change = cardinal @ acceleration_change[:, -1]
        displacement = np.where(reference < 0., 1 + reference / (-edges[0]), 1 - reference / edges[-1])
        displacement_xi = np.where(reference < 0., 1 / (-edges[0]), -1 / edges[-1])
        eta_left = np.einsum('ql,lq->q', cardinal, directions['edge_vertices'][:, cells], optimize=False)
        eta_right = np.einsum('ql,lq->q', cardinal, directions['edge_vertices'][:, cells + 1], optimize=False)
        movement = (1 - local) * eta_left + local * eta_right + displacement * source_mode
        movement_r = ((eta_right - eta_left) / widths[cells] + displacement_xi * source_mode) / jacobian
        speed = displacement * velocity
        speed_r = displacement_xi * velocity / jacobian
        movement_rate = displacement * source_rate
        movement_rate_r = displacement_xi * source_rate / jacobian
        values, radial = metric_at_offset(action.solver, action.solution, radius_offset, anchor)
        second = metric_at_offset(action.solver, action.solution, radius_offset, anchor, second=True)
        pos, pos_r = response_at_offset(position, radius_offset, anchor)
        time, time_r = response_at_offset(metric_time, radius_offset, anchor)
        mixed = response_at_offset(mixed_time, radius_offset, anchor)[0]
        geometry = dict(radius=radius, jacobian=jacobian, displacement=displacement, jacobian_source=displacement_xi)
        row = dict(geometry=geometry, gradient=gradient_reference)
        amount, step = 1e-25j, 1e-25
        changed_jacobian = jacobian * (1 + amount * movement_r)
        changed_row = dict(geometry=dict(geometry, radius=radius + amount * movement, jacobian=changed_jacobian),
            gradient=gradient_reference + amount * field_reference_gradient)
        base = wave_packet(row, values, radial, time, rate, rate_reference_gradient / jacobian,
            old_accel, speed, speed_r, displacement * source_accel)
        changed = wave_packet(changed_row, values + amount * (pos + radial * movement),
            radial + amount * (pos_r + second * movement), time + amount * (mixed + time_r * movement),
            rate + amount * transported, (rate_reference_gradient + amount * transported_reference_gradient) / changed_jacobian,
            old_accel + amount * changed_accel, speed + amount * movement_rate,
            (speed_r + amount * movement_rate_r) / (1 + amount * movement_r),
            displacement * (source_accel + amount * source_accel_change))
        radius_jet = MixedJet(radius, movement, speed, movement_rate)
        jacobian_jet = MixedJet(jacobian, movement_r * jacobian, speed_r * jacobian, movement_rate_r * jacobian)
        gradient_jet = MixedJet(gradient_reference, field_reference_gradient, rate_reference_gradient, transported_reference_gradient) / jacobian_jet
        speed_jet = MixedJet(speed, movement_rate, displacement * source_accel, displacement * source_accel_change)
        rate_jet = MixedJet(rate, transported, old_accel, changed_accel)
        mass_jet, nu_jet = metric_jets(values, radial, second, pos, pos_r, time, time_r, mixed, movement, speed, movement_rate)
        metric_jet = 1. - 2 * mass_jet / radius_jet
        momentum_jet = jacobian_jet * radius_jet**2 / (jet_exp(nu_jet) * metric_jet**.5) * (rate_jet - speed_jet * gradient_jet)
        measure = radial_weights[section][density.indices] * density.label_weights * active
        packets = [
            ('momentum_rate', ((1 + amount * movement_r) * changed['momentum_rate']).imag / step, shape),
            ('oracle_momentum_rate', momentum_jet.parts[3] / jacobian, shape),
            ('force_wave', changed['force_field'].imag / step, test_gradient),
            ('base_momentum', base['momentum'], shape),
            ('base_force_wave', base['force_field'], test_gradient)]
        for name, value, basis in packets:
            for column in range(3):
                mask = selected[:, column]
                factors = measure[mask] * value[mask] * basis[mask, column]
                np.add.at(output[name].T, indices[mask, column], factors[:, None] * cardinal[mask])
        if start % 2048 == 0:
            progress('Eulerian-' + str(radial_order) + '-' + str(label_order) + ':' + str(start) + '/' + str(len(radii)))
    return output


def hybrid_position_reaction(loads, action, native, directions, correction, mode_rate, acceleration,
                             position, metric_time, mixed_time, order, deadline, progress,
                             acceleration_change=None, reference_order=12, include_native=True):
    result = material_position_reaction(loads, action, native, directions, correction, mode_rate, acceleration,
        position, metric_time, mixed_time, order, deadline, progress, acceleration_change, reference_order, include_native)
    radial_order, label_order = {48: (24, 28), 64: (32, 36)}[order]
    field = eulerian_field_reaction(loads, action, directions, correction, mode_rate, acceleration,
        position, metric_time, mixed_time, radial_order, label_order, deadline, progress, acceleration_change)
    for key, value in field.items():
        result['unsplit_material_' + key] = result[key].copy()
        result[key][:, :-1] = value[:, :-1]
    result['force'] = result['force_wave'] + result['force_native']
    result['residual'] = result['momentum_rate'] - result['force']
    result['oracle_difference'] = result['oracle_momentum_rate'] - result['momentum_rate']
    result['quadrature_orders_radial_label_source'] = np.array([radial_order, label_order, order])
    return result
