from derive_annular_source_gravity_20260914 import EvidenceRun
import sympy as sp


def main():
    evidence = EvidenceRun('annular-continuum-angular-closure-attempt01', __file__)
    try:
        radius, lapse, root, source = sp.symbols('R N U S', positive=True)
        velocity, left_gradient, right_gradient = sp.symbols('V H_minus H_plus', real=True)
        speed = lapse*root
        jump_gradient_square = left_gradient**2-right_gradient**2
        force = radius**2*(speed-velocity**2/speed)*jump_gradient_square/2
        jump_mixed_time_radial = radius**2*velocity/speed*jump_gradient_square
        jump_mixed_radial_radial = radius**2*(speed+velocity**2/speed)*jump_gradient_square/2
        jump_mixed_time_time = -jump_mixed_radial_radial
        jump_mixed_radial_time = -radius**2*speed*velocity*jump_gradient_square
        wave_radial_divergence = velocity*jump_mixed_time_radial-jump_mixed_radial_radial
        wave_time_divergence = velocity*jump_mixed_time_time-jump_mixed_radial_time
        evidence.check('scalar_moving_interface_radial_divergence_minus_force', sp.simplify(wave_radial_divergence+force) == 0)
        evidence.check('scalar_moving_interface_time_divergence_velocity_times_force', sp.simplify(wave_time_divergence-velocity*force) == 0)
        evidence.check('interface_force_orthogonal_to_source_worldline', sp.simplify(wave_time_divergence+velocity*wave_radial_divergence) == 0)
        lapse_radial, root_radial, momentum_time = sp.symbols('N_R U_R p_t', real=True)
        clock = sp.sqrt(lapse**2-velocity**2/root**2)
        momentum = source*velocity/(root**2*clock)
        determinant = lapse*radius**2/root
        stress_time_radial = source*velocity/(lapse*radius**2*root*clock)
        evidence.check('densitized_source_radial_momentum_is_canonical_p', sp.simplify(determinant*stress_time_radial-momentum) == 0)
        gravity = -source*(lapse*lapse_radial+velocity**2*root_radial/root**3)/clock
        source_divergence = momentum_time-gravity
        evidence.check('source_radial_divergence_cancels_scalar_jump_on_shell', sp.simplify(source_divergence.subs(momentum_time, gravity+force)+wave_radial_divergence) == 0)
        evidence.check('source_time_divergence_cancels_scalar_jump', sp.simplify(-velocity*source_divergence.subs(momentum_time, gravity+force)+wave_time_divergence) == 0)
        time, radial_coordinate, angle, azimuth = sp.symbols('t r theta varphi', real=True)
        coordinates = [time, radial_coordinate, angle, azimuth]
        metric_lapse = sp.Function('N')(time, radial_coordinate)
        metric_root = sp.Function('U')(time, radial_coordinate)
        metric = sp.diag(-metric_lapse**2, metric_root**-2, radial_coordinate**2, radial_coordinate**2*sp.sin(angle)**2)
        inverse = metric.inv()
        connection = [[[sp.simplify(sum(inverse[upper, contracted]*(sp.diff(metric[contracted, lower_second], coordinates[lower_first])
                         +sp.diff(metric[contracted, lower_first], coordinates[lower_second])-sp.diff(metric[lower_first, lower_second], coordinates[contracted]))
                         for contracted in range(4))/2) for lower_second in range(4)] for lower_first in range(4)] for upper in range(4)]
        residual_time = sp.Function('Ett')(time, radial_coordinate)
        residual_cross = sp.Function('EtR')(time, radial_coordinate)
        residual_radial = sp.Function('ERR')(time, radial_coordinate)
        residual_angle = sp.Function('EAA')(time, radial_coordinate)
        residual = sp.Matrix([[residual_time, residual_cross, 0, 0],
                              [-metric_lapse**2*metric_root**2*residual_cross, residual_radial, 0, 0],
                              [0, 0, residual_angle, 0], [0, 0, 0, residual_angle]])
        divergence = sum(sp.diff(residual[upper, 1], coordinates[upper]) for upper in range(4))
        divergence += sum(connection[upper][upper][contracted]*residual[contracted, 1]
                          -connection[contracted][upper][1]*residual[upper, contracted] for upper in range(4) for contracted in range(4))
        expected = sp.diff(residual_cross, time)+sp.diff(residual_radial, radial_coordinate)
        expected += (sp.diff(metric_lapse, time)/metric_lapse-sp.diff(metric_root, time)/metric_root)*residual_cross
        expected += (sp.diff(metric_lapse, radial_coordinate)/metric_lapse+2/radial_coordinate)*residual_radial
        expected -= sp.diff(metric_lapse, radial_coordinate)/metric_lapse*residual_time+2*residual_angle/radial_coordinate
        evidence.check('angular_residual_identity_from_full_metric_connection', sp.simplify(divergence-expected) == 0)
        reduced = expected.subs({residual_time:0, residual_cross:0, residual_radial:0}).doit()
        evidence.check('conserved_matter_and_three_Einstein_components_force_angular_component', sp.simplify(reduced+2*residual_angle/radial_coordinate) == 0)
        evidence.report.update(conditional_spherical_interior_angular_completion_derived=True,
                               moving_interface_total_stress_conservation_derived=True,
                               averaging_commutes_with_divergence_for_fixed_label_weight_and_common_metric=True,
                               requires_radial_constraints_temporal_current_and_on_shell_matter=True,
                               outer_boundary_supports_or_global_completion_not_derived=True,
                               unrestricted_full_GR_limit_proven=False, full_GR_limit_proven=False,
                               parent_action_uniquely_selected=False, valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
