from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_primitive_geometry_20260918 import PrimitiveP2System
from annular_live_P2_current_20260918 import LiveP2Tangent, physical_sample
from derive_annular_P2_broken_traction_identity_20260918 import broken_traction
from verify_annular_P2_broken_traction_offshell_20260918 import ManufacturedTangent
from run_annular_P2_continuum_bridge_20260918 import checked_load
import argparse
import json
import numpy as np
import sympy as symbolic


def conforming_force_lift(tangent, order=32):
    current = tangent.layer_data(0.)
    layer, values, rates = current.layer, current.coordinates, current.rates
    original = broken_traction(tangent, order=order)
    reference_lengths = np.diff(layer.edges)
    centers = (layer.edges[:-1]+layer.edges[1:])/2
    boundaries, unused, edge_motion = layer.mapping(layer.edges, values[-1])
    unused, jacobian, midpoint_motion = layer.mapping(centers, values[-1])
    indices = layer.element_indices
    valid = indices >= 0
    local_values = values[:-1][np.maximum(indices, 0)]*valid
    gradient_left = (local_values @ np.array([-3., 4., -1.]))/(reference_lengths*jacobian)
    gradient_right = (local_values @ np.array([1., -4., 3.]))/(reference_lengths*jacobian)
    gradient_midpoint = (local_values @ np.array([-1., 0., 1.]))/(reference_lengths*jacobian)
    source_edge = int(np.searchsorted(layer.edges, layer.anchor))
    edge_lift = np.zeros(len(layer.edges))
    edge_lift[1:-1] = edge_motion[1:-1]*(gradient_right[:-1]+gradient_left[1:])/2
    edge_lift[source_edge] = 0.
    lifted = np.zeros(layer.count)
    for column, data in [(0, edge_lift[:-1]), (1, midpoint_motion*gradient_midpoint), (2, edge_lift[1:])]:
        selected = valid[:, column]
        lifted[indices[selected, column]] = data[selected]
    left_remainder = edge_motion[:-1]*gradient_left-edge_lift[:-1]
    right_remainder = edge_motion[1:]*gradient_right-edge_lift[1:]
    interior = tangent.geometry.edges[(tangent.geometry.edges > boundaries[0]) & (tangent.geometry.edges < boundaries[-1])]
    endpoints = np.unique(np.concatenate([boundaries, interior]))
    lengths = np.diff(endpoints)
    points, weights = np.polynomial.legendre.leggauss(order)
    radius = ((endpoints[:-1, None]+endpoints[1:, None])/2+lengths[:, None]*points/2).ravel()
    quadrature = (lengths[:, None]*weights/2).ravel()
    element = np.clip(np.searchsorted(boundaries, radius)-1, 0, len(boundaries)-2)
    fraction = (radius-boundaries[element])/(boundaries[element+1]-boundaries[element])
    shapes = np.column_stack([(1-fraction)*(1-2*fraction), 4*fraction*(1-fraction), fraction*(2*fraction-1)])
    lift_values = np.sum(shapes*lifted[np.maximum(indices[element], 0)]*valid[element], axis=1)
    temporal, gradient = physical_sample(layer, values, rates, radius)
    changed_temporal, unused = physical_sample(current.tangent_layer, current.changed_coordinates, current.changed_rates, radius)
    temporal_derivative = (radius**4/current.tangent_layer.coefficient(0., radius)*changed_temporal).imag/current.step
    unused, changed_gradient = physical_sample(layer, values, rates, radius.astype(complex)+1j*current.step)
    spatial_derivative = (layer.coefficient(0., radius.astype(complex)+1j*current.step)*changed_gradient).imag/current.step
    residual = temporal_derivative-spatial_derivative
    motion = (1-fraction)*edge_motion[element]+fraction*edge_motion[element+1]
    remainder = motion*gradient-lift_values
    polynomial_remainder = shapes[:, 0]*left_remainder[element]+shapes[:, 2]*right_remainder[element]
    polynomial_error = float(max(abs(remainder-polynomial_remainder)))
    element_work = np.bincount(element, weights=quadrature*remainder*residual, minlength=len(reference_lengths))
    residual_norm_squared = np.bincount(element, weights=quadrature*residual**2, minlength=len(reference_lengths))
    remainder_norm_squared = np.diff(boundaries)*(2*left_remainder**2+2*right_remainder**2-left_remainder*right_remainder)/15
    quadrature_norm = np.bincount(element, weights=quadrature*remainder**2, minlength=len(reference_lengths))
    bounds = np.sqrt(np.maximum(0., remainder_norm_squared*residual_norm_squared))
    nodes, node_jacobian, unused = layer.mapping(layer.radii, values[-1])
    coefficient = layer.sampling @ (layer.coefficient(0., nodes)/node_jacobian)
    factor, varied_factor = layer.lifted @ values[:-1], layer.lifted @ lifted
    gram_variation = float(np.dot(coefficient*factor, varied_factor)/layer.gram_spacing)
    changed_factor = layer.lifted @ (values[:-1].astype(complex)+1j*current.step*lifted)
    gram_variation_check = float((np.dot(coefficient, changed_factor**2)/(2*layer.gram_spacing)).imag/current.step)
    gram_combined = original['explicit_Gram_shape_force']-gram_variation
    weak_pairing = float(lifted @ current.euler)
    internal = np.arange(1, len(layer.edges)-1)
    edge_coefficient = layer.coefficient(0., boundaries[internal])
    edge_kinetic = boundaries[internal]**4/edge_coefficient
    speed = edge_motion[internal]*rates[-1]
    traction_jump = (edge_coefficient-edge_kinetic*speed**2)*(gradient_right[:-1]-gradient_left[1:])
    projected_weak = float(quadrature @ (lift_values*residual)+traction_jump @ edge_lift[internal]+gram_variation)
    derived = weak_pairing+float(sum(element_work))+gram_combined
    elements = [dict(index=int(index), lower=float(boundaries[index]), upper=float(boundaries[index+1]),
        near_source=bool(abs((boundaries[index]+boundaries[index+1])/2-values[-1]) < .05),
        touches_source=bool(index in [source_edge-1, source_edge]),
        signed_lifting_work=float(element_work[index]), cauchy_bound=float(bounds[index]),
        remainder_norm_squared=float(remainder_norm_squared[index]),
        regular_Euler_norm_squared=float(residual_norm_squared[index])) for index in range(len(reference_lengths))]
    return dict(force=original['force'], trace_pressure=original['trace_pressure'],
        original_defect=original['actual_defect'], original_absolute_term_bound=original['absolute_term_bound'],
        scalar_weak_pairing=weak_pairing, projected_weak_identity_error=abs(projected_weak-weak_pairing),
        lift_bulk_work=float(sum(element_work)), Gram_variation=gram_variation,
        explicit_Gram_shape_force=original['explicit_Gram_shape_force'], combined_Gram_work=gram_combined,
        derived_defect=derived, identity_error=abs(original['actual_defect']-derived),
        local_cauchy_bound=float(sum(bounds)), signed_element_absolute_sum=float(sum(abs(element_work))),
        total_defect_bound=float(abs(weak_pairing)+sum(bounds)+abs(gram_combined)),
        polynomial_remainder_error=polynomial_error,
        analytic_remainder_norm_error=float(max(abs(remainder_norm_squared-quadrature_norm))),
        Gram_variation_derivative_error=abs(gram_variation-gram_variation_check),
        source_touching_work=float(sum(element_work[source_edge-1:source_edge+1])),
        source_near_work=float(sum(row['signed_lifting_work'] for row in elements if row['near_source'])),
        elements=elements)


def record(evidence, tangent, branch, count, time, fixture):
    row = conforming_force_lift(tangent)
    control = conforming_force_lift(tangent, order=48)
    row.update(branch=branch, base_count=count, time=time, fixture=fixture,
        quadrature_control=abs(control['derived_defect']-row['derived_defect']))
    evidence.report['cases'].append(row)
    evidence.save()
    key = fixture+'_'+branch+str(count)+'_'+str(time)
    evidence.check(key+'_force_lifting_identity', row['identity_error'] < 2e-9, row['identity_error'])
    evidence.check(key+'_projected_weak_identity', row['projected_weak_identity_error'] < 2e-9)
    evidence.check(key+'_quadratic_remainder_formula', row['polynomial_remainder_error'] < 2e-12
        and row['analytic_remainder_norm_error'] < 2e-16)
    evidence.check(key+'_Gram_derivative', row['Gram_variation_derivative_error'] < 2e-12)
    evidence.check(key+'_local_cauchy_bound', all(abs(part['signed_lifting_work']) <= part['cauchy_bound']+2e-14
        for part in row['elements']))
    evidence.check(key+'_quadrature_control', row['quadrature_control'] < 2e-9)
    if fixture == 'manufactured':
        evidence.check(key+'_omitted_weak_residual_negative_control', abs(row['scalar_weak_pairing']) > 1e-8)
        if branch == 'MTS':
            evidence.check(key+'_omitted_Gram_variation_negative_control', abs(row['Gram_variation']) > 1e-9)
    print(json.dumps({name:value for name,value in row.items() if name != 'elements'}), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fixture', choices=['manufactured', 'saved'], required=True)
    args = parser.parse_args()
    evidence = EvidenceRun('annular-P2-conforming-force-lift-'+args.fixture+'-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, no_forward_evolution=True,
            finite_Gram_retained=True, no_force_correction_applied=True,
            residual_representation_not_continuum_convergence=True,
            full_live_P2_force_convergence_proven=False,
            numerical_norm_integrals_not_interval_certified=True)
        coordinate, left, right = symbolic.symbols('coordinate left right', real=True)
        remainder = left*(1-coordinate)*(1-2*coordinate)+right*coordinate*(2*coordinate-1)
        norm = symbolic.integrate(remainder**2, (coordinate, 0, 1))
        evidence.check('exact_quadratic_remainder_L2_norm', symbolic.simplify(norm-(2*left**2+2*right**2-left*right)/15) == 0)
        if args.fixture == 'manufactured':
            for count in [17, 33]:
                for branch in ['reference', 'MTS']:
                    record(evidence, ManufacturedTangent(count, branch == 'MTS'), branch, count, 0., 'manufactured')
        else:
            for branch in ['reference', 'MTS']:
                saved = checked_load(evidence, 'annular-P2-continuum-bridge-'+branch+'-65-attempt01', 'trajectory.npz')
                system = PrimitiveP2System(65, branch == 'MTS', layer_degree=14, radial_degree=18, action_order=32, label_order=20)
                states = saved['states'].reshape(5, 2, len(system.labels), system.count+1)
                for index in ([0, 4] if branch == 'reference' else [1, 4]):
                    position, momentum = states[index]
                    record(evidence, LiveP2Tangent(system, position, momentum), branch, 65, float(saved['times'][index]), 'saved')
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
