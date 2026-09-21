from derive_annular_source_gravity_20260914 import EvidenceRun
import sympy as sp


def main():
    evidence = EvidenceRun('annular-live-scaled-characteristics-algebra-attempt01', __file__)
    try:
        radius, mass, lapse, root, source, coupling = sp.symbols('R mu N U S kappa', positive=True)
        momentum, density, wave_square = sp.symbols('p d_b T', real=True)
        energy = sp.sqrt(source**2+root**2*momentum**2)
        mass_radial = coupling*radius**2*root**2*wave_square/2+coupling*root*energy*density
        log_lapse_radial = mass/(radius**2*root**2)+coupling*radius*wave_square/2+coupling*root*momentum**2*density/(radius*energy)
        log_root_radial = mass/(radius**2*root**2)-mass_radial/(radius*root**2)
        log_speed_radial = 2*mass/(radius**2*root**2)-coupling*source**2*density/(radius*root*energy)
        evidence.check('wave_cancels_from_log_NU_radial', sp.simplify(log_lapse_radial+log_root_radial-log_speed_radial) == 0)
        raw_force = -lapse*energy*log_lapse_radial-lapse*root**2*momentum**2/energy*log_root_radial
        force = -lapse*mass/radius**2*(energy/root**2+momentum**2/energy)-coupling*lapse*radius*source**2*wave_square/(2*energy)
        evidence.check('source_density_cancels_from_canonical_gravity_force', sp.simplify(raw_force-force) == 0)
        speed, speed_radial, scaled, gradient, scaled_radial, gradient_radial = sp.symbols('s s_R P H P_R H_R', real=True)
        scaled_time = speed*gradient_radial+(speed_radial+2*speed/radius)*gradient
        gradient_time = speed*scaled_radial+speed_radial*scaled
        plus, minus = scaled+gradient, scaled-gradient
        evidence.check('plus_equation_no_metric_time_derivative', sp.expand(scaled_time+gradient_time-speed*(scaled_radial+gradient_radial)-speed_radial*plus-speed/radius*(plus-minus)) == 0)
        evidence.check('minus_equation_no_metric_time_derivative', sp.expand(scaled_time-gradient_time+speed*(scaled_radial-gradient_radial)+speed_radial*minus-speed/radius*(plus-minus)) == 0)
        evidence.check('canonical_wave_equation', sp.expand(radius**2*scaled_time-speed*radius**2*gradient_radial-(speed_radial*radius**2+2*speed*radius)*gradient) == 0)
        velocity = lapse*root**2*momentum/energy
        evidence.check('Doppler_ratio_lapse_independent', sp.simplify(velocity/(lapse*root)-root*momentum/energy) == 0)
        outgoing = sp.symbols('outgoing', real=True)
        ratio = root*momentum/energy
        incoming = -(1-ratio)/(1+ratio)*outgoing
        evidence.check('left_boundary_zero_trace_rate', sp.simplify(lapse*root*(incoming+outgoing)/2+velocity*(incoming-outgoing)/2) == 0)
        incoming_right = -(1+ratio)/(1-ratio)*outgoing
        evidence.check('right_boundary_zero_trace_rate', sp.simplify(lapse*root*(outgoing+incoming_right)/2+velocity*(outgoing-incoming_right)/2) == 0)
        pressure_jump = sp.symbols('DeltaH2', real=True)
        force_wave = radius**2*lapse*root*(1-ratio**2)*pressure_jump/2
        force_action = radius**2*(lapse*root-velocity**2/(lapse*root))*pressure_jump/2
        evidence.check('radiation_force_matches_moving_action', sp.simplify(force_wave-force_action) == 0)
        evidence.check('mass_constraint_lapse_independent_at_fixed_canonical_data', sp.diff(mass_radial, lapse) == 0)
        evidence.report.update(dynamic_metric_scaled_characteristics_derived=True, wave_self_gravity_retained=True,
                               explicit_source_density_cancellation_does_not_remove_integrated_source_mass=True,
                               continuum_live_evolution_completed=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
