from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_graded_source_20260919 import GradedSourceAction
from annular_P2_Gram_row_bounds_20260919 import row_bounds
from annular_P2_weighted_projection_bounds_20260919 import projection_data, operator_constants, consistency_bound, uniform_constants, band_action
from derive_annular_P2_unresolved_front_Gram_20260919 import front_profile
from scipy.linalg import solve_banded
import contextlib
import json
import numpy as np
import sympy as symbolic


class VariableMetricFixture(GradedSourceAction):
    def metric(self, time, radius):
        radius = np.asarray(radius)
        root = np.sqrt(1-1.4/radius)
        return root*(1+.02*np.sin(2*(radius-6))), root


def analytic_geometry_bounds(layer, position):
    inner, outer = layer.base_radii[[0, -1]]
    buffers = np.array([layer.anchor-inner, outer-layer.anchor])
    jacobians = np.array([position-inner, outer-position])/buffers
    minimum = min(jacobians)
    coefficient_log_derivative = (2*outer-1.4)/(inner**2-1.4*inner)+.04/.98
    coefficient_maximum = (outer**2-1.4*outer)*1.02/minimum
    log_kinetic_derivative = max(jacobians)*(4/inner+coefficient_log_derivative)
    transport_derivative = max(1/(buffers*jacobians))
    return dict(maximum_transport_map=1/minimum, maximum_transport_map_derivative=float(transport_derivative),
        maximum_Gram_coefficient=float(coefficient_maximum),
        maximum_log_weight_derivative=float(coefficient_log_derivative+transport_derivative),
        log_kinetic_Lipschitz=float(log_kinetic_derivative),
        relative_cell_variation_bound=float(np.expm1(log_kinetic_derivative*max(np.diff(layer.edges))/2)),
        minimum_map_jacobian=float(minimum), maximum_map_jacobian=float(max(jacobians)))


def profile(position):
    return .01*np.asarray(position)+front_profile(position, .04, .77, .03, .002)


def profile_derivative(position, side=None):
    position = np.asarray(position)
    left = position < 0 if side is None else np.full_like(position, side == 0, dtype=bool)
    return .01+np.where(left, -.002*np.maximum(.04+position/.8, 0)/.8,
        .002*np.maximum(.04-position/.74, 0)/.74)


def run_case(evidence, count, power, displacement, gram=True):
    spacing = 1.6/(count-1)
    layer = VariableMetricFixture(count, gram, source_cap=spacing**power/8)
    coordinates = np.append(profile(layer.radii-layer.anchor), layer.anchor+displacement)
    rates = np.zeros_like(coordinates)
    projection = projection_data(layer, coordinates, rates)
    operator = operator_constants(layer)
    geometry = analytic_geometry_bounds(layer, coordinates[-1])
    field = dict(gradient=.01+.002*.04/.74, curvature=.002/.74**2)
    bound = consistency_bound(layer, coordinates, projection, operator, geometry, field)
    exact, unused = row_bounds(layer, coordinates, rates)
    constants = bound['constants']
    source = projection['source']
    centres = (layer.edges[:-1]+layer.edges[1:])/2
    unused, element_jacobian, unused2 = layer.mapping(centres, coordinates[-1])
    unused, node_jacobian, node_motion = layer.mapping(layer.radii, coordinates[-1])
    exact_transport_nodes = -node_motion/node_jacobian*profile_derivative(layer.radii-layer.anchor)
    source_values = np.array([-float(profile_derivative(0., side))/element_jacobian[source-1+side] for side in [0, 1]])
    exact_transport_quadrature = np.sum(layer.reference_shape*exact_transport_nodes[layer.reference_indices], axis=1)
    exact_transport_quadrature += projection['missing_shapes'] @ source_values
    residual = projection['field_motion']-exact_transport_quadrature
    residual_load = layer.assemble_quadratic(layer.reference_indices,
        layer.reference_shape*(projection['quadrature_weight']*residual)[:, None])
    residual_projected = solve_banded((2, 2), projection['data']['mass_bands'], residual_load, check_finite=False)
    recovered = exact_transport_nodes-projection['source_defects'] @ source_values+residual_projected
    projection_split_error = float(max(abs(recovered-projection['projection'])))
    defect_residual = max(float(max(abs(band_action(projection['data']['mass_bands'], projection['source_defects'][:, side])
        +projection['source_columns'][:, side]))) for side in [0, 1])
    key = ('MTS' if gram else 'reference')+'_'+str(count)+'_'+str(power)+'_'+str(displacement)
    evidence.check(key+'_analytic_positive_weight_variation', geometry['minimum_map_jacobian'] > 0
        and geometry['relative_cell_variation_bound'] <= constants['epsilon']
        and projection['discrete_relative_variation'] <= geometry['relative_cell_variation_bound']+2e-12)
    evidence.check(key+'_uniform_mass_projection_bounds', np.min(projection['margins']) > 0
        and projection['contraction'] <= constants['contraction']+2e-12
        and projection['stability'] <= constants['nodal_projection_stability']+2e-12)
    evidence.check(key+'_source_defect_locality_without_width_cutoff', defect_residual < 2e-12
        and projection['defect_pair_l1'] <= constants['source_pair_l1_bound'])
    evidence.check(key+'_weighted_projection_exact_split', projection_split_error < 2e-12
        and max(abs(residual_projected)) <= bound['projection_interpolation_remainder_bound']+2e-12)
    evidence.check(key+'_field_and_transport_interpolation_bounds', bound['field_factor_maximum'] <= bound['field_factor_bound']+2e-13
        and max(abs(projection['projection'])) <= bound['projected_velocity_bound']+2e-12)
    evidence.check(key+'_source_and_remaining_projected_bounds',
        abs(exact['groups'][0]['projected_sum']) <= bound['source_bound']+2e-12
        and abs(exact['groups'][1]['projected_sum']) <= bound['remaining_bound']+bound['numerical_hinge_tail']+2e-12)
    evidence.check(key+'_full_shape_and_drive_bounds', abs(exact['shape_force']) <= bound['shape_bound']+2e-12
        and abs(exact['explicit_drive']) <= bound['total_bound']+2e-12)
    if not gram:
        evidence.check(key+'_paired_zero_Gram_control', exact['explicit_drive'] == 0 and bound['total_bound'] == 0)
    row = dict(branch='MTS' if gram else 'reference', base_count=count, source_power=power,
        source_displacement=displacement, spacing=spacing, source_cap=spacing**power/8,
        exact_drive=exact['explicit_drive'], exact_shape=exact['shape_force'], exact_projected=exact['projected_drive'],
        source_projected=exact['groups'][0]['projected_sum'], remaining_projected=exact['groups'][1]['projected_sum'],
        a_priori_bound=bound, sharper_saved_state_row_bound=exact['drive_absolute_row_bound'],
        geometry_bounds=geometry, field_regularity_bounds=field,
        measured_cell_weight_variation=projection['discrete_relative_variation'],
        measured_mass_contraction=projection['contraction'], measured_projection_stability=projection['stability'],
        measured_source_defect_pair_l1=projection['defect_pair_l1'], weighted_projection_split_error=projection_split_error,
        actual_interpolation_projection_error=float(max(abs(residual_projected))),
        operator_constants={name:value for name,value in operator.items() if name != 'source_rows'},
        prescribed_geometry_not_parent_trajectory=True, no_front_fitting=True, valid_for_claim=False)
    evidence.report['cases'].append(row)
    evidence.save()
    return row


def main():
    evidence = EvidenceRun('annular-P2-variable-geometry-consistency-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False,
            full_live_P2_force_convergence_proven=False, no_new_evolution=True,
            same_Gram_and_mass_action_rules=True, positive_variable_metric_fixture=True,
            actual_nonrigid_source_map_retained=True, no_source_or_front_force_fitted=True,
            no_wavefront_fitting_in_this_test=True,
            theorem_for_interpolants_not_a_stability_theorem=True)
        fraction = symbolic.symbols('fraction', real=True)
        shapes = symbolic.Matrix([(1-fraction)*(1-2*fraction), 4*fraction*(1-fraction), fraction*(2*fraction-1)])
        mass = shapes*shapes.T
        integrated = mass.applyfunc(lambda value:symbolic.integrate(value, (fraction, 0, 1)))
        evidence.check('exact_unit_P2_mass', integrated == symbolic.Matrix([[4, 2, -1], [2, 16, 2], [-1, 2, 4]])/30)
        lebesgue_left = symbolic.expand(shapes[0]+shapes[1]-shapes[2])
        evidence.check('P2_Lebesgue_constant', lebesgue_left.subs(fraction, symbolic.Rational(1, 4)) == symbolic.Rational(5, 4)
            and symbolic.diff(lebesgue_left, fraction, 2) == -8)
        contraction = symbolic.symbols('contraction', positive=True)
        evidence.check('pair_defect_geometric_series', symbolic.simplify(4*contraction/(1-contraction)
            +4*contraction**2/(1-contraction)**2-4*contraction/(1-contraction)**2) == 0)
        constants = uniform_constants()
        evidence.check('conservative_projection_constants_contract', 0 < constants['contraction'] < 1
            and constants['nodal_projection_stability'] > 0)
        evidence.report['derived_constants'] = constants
        for count in [33, 65, 129, 257, 513, 1025, 2049]:
            for power in [1, 2]:
                for displacement in [-.02, .015]:
                    row = run_case(evidence, count, power, displacement)
                    print(json.dumps(dict(count=count, power=power, displacement=displacement,
                        force=row['exact_drive'], bound=row['a_priori_bound']['total_bound'])), flush=True)
        for displacement in [-.02, .015]:
            run_case(evidence, 513, 1, displacement, False)
        evidence.report.update(sufficient_limit='h -> 0 and h^2/delta_min -> 0, with the stated geometry and piecewise W2-infinity bounds uniform',
            remaining_gap='Actual nonlinear trajectory error in a force-controlling norm, metric feedback stability and a uniform-time bound are not supplied by consistency alone.',
            front_coefficients=dict(speed=.77, velocity=.03, forcing=.002, time=.04, background_gradient=.01),
            prescribed_metric='U=sqrt(1-1.4/R), N=U*(1+.02*sin(2*(R-6)))',
            coefficients_not_fitted_to_live_error=True)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), cases=len(evidence.report['cases']))), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
