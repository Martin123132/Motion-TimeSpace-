from derive_annular_source_gravity_20260914 import EvidenceRun
import sympy as sp


def main():
    evidence = EvidenceRun('annular-characteristic-work-balance-attempt01', __file__)
    try:
        radius, metric, metric_radial, kinetic, coefficient, velocity = sp.symbols('R F F_R A C V', real=True)
        temporal, gradient, temporal_radial, gradient_radial = sp.symbols('W H W_R H_R', real=True)
        temporal_time = metric**2*gradient_radial+metric*(metric_radial+2*metric/radius)*gradient
        gradient_time = temporal_radial
        plus_radial = temporal_radial+metric_radial*gradient+metric*gradient_radial
        minus_radial = temporal_radial-metric_radial*gradient-metric*gradient_radial
        plus_time, minus_time = temporal_time+metric*gradient_time, temporal_time-metric*gradient_time
        curvature = 2*metric**2*gradient/radius
        evidence.check('plus_characteristic_equation_from_scalar_PDE', sp.simplify(plus_time-metric*plus_radial-curvature) == 0)
        evidence.check('minus_characteristic_equation_from_scalar_PDE', sp.simplify(minus_time+metric*minus_radial-curvature) == 0)
        plus, minus = sp.symbols('f_plus f_minus', real=True)
        trace_rate = (plus+minus)/2+velocity*(plus-minus)/(2*metric)
        evidence.check('left_incoming_Doppler_condition', sp.simplify(trace_rate.subs(plus, -(metric-velocity)/(metric+velocity)*minus)) == 0)
        evidence.check('right_incoming_Doppler_condition', sp.simplify(trace_rate.subs(minus, -(metric+velocity)/(metric-velocity)*plus)) == 0)
        energy = (kinetic*velocity**2+coefficient)*gradient**2/2
        outward_flux = coefficient*velocity*gradient**2
        pressure_force = (coefficient-kinetic*velocity**2)*gradient**2/2
        evidence.check('moving_boundary_energy_loss_equals_source_work', sp.simplify(-outward_flux+velocity*energy+velocity*pressure_force) == 0)
        curvature_at_source, acceleration = sp.symbols('H_R_at_b b_tt', real=True)
        second_trace_rate = (metric**2-velocity**2)*curvature_at_source+(metric*(metric_radial+2*metric/radius)+acceleration)*gradient
        compatible_curvature = -(metric*(metric_radial+2*metric/radius)+acceleration)*gradient/(metric**2-velocity**2)
        evidence.check('initial_second_trace_compatibility_is_not_a_force_fit', sp.simplify(second_trace_rate.subs(curvature_at_source, compatible_curvature)) == 0)
        source, force = sp.symbols('S F_wave', positive=True)
        clock = sp.sqrt(metric-velocity**2/metric)
        momentum = source*velocity/(metric*clock)
        material_gradient = -source*metric_radial*(1+velocity**2/metric**2)/(2*clock)
        coordinate_acceleration = -metric*metric_radial/2+3*metric_radial*velocity**2/(2*metric)+clock**3/source*force
        momentum_rate = sp.diff(momentum, velocity)*coordinate_acceleration+sp.diff(momentum, metric)*metric_radial*velocity
        evidence.check('benchmark_coordinate_acceleration_follows_canonical_source_law', sp.simplify(momentum_rate-material_gradient-force) == 0)
        evidence.report.update(continuum_characteristics_derived_from_scalar_PDE=True,
                               two_sided_Doppler_boundary_conditions_derived=True,
                               continuum_wave_source_energy_exchange_derived=True,
                               initial_curvature_enforces_compatibility_not_evolved_force=True,
                               full_GR_limit_proven=False, valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
