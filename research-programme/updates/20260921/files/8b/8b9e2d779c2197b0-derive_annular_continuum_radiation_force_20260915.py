from derive_annular_source_gravity_20260914 import EvidenceRun
import sympy as sp


def main():
    evidence = EvidenceRun('annular-continuum-radiation-force-algebra-attempt01', __file__)
    try:
        radius, lapse, root, source, coupling = sp.symbols('R N U S kappa', positive=True)
        velocity, gradient, temporal, mass, density, flux, momentum, weight = sp.symbols('V H W mu rho WH p d', real=True)
        clock_squared = lapse**2-velocity**2/root**2
        clock = sp.sqrt(clock_squared)
        coefficient = radius**2*lapse*root
        kinetic = radius**2/(lapse*root)
        lagrangian = (kinetic*temporal**2-coefficient*gradient**2)/2
        boundary_flux = -coefficient*gradient-velocity*kinetic*temporal
        shape_force = (lagrangian-boundary_flux*gradient).subs(temporal, -velocity*gradient)
        pressure_force = (coefficient-kinetic*velocity**2)*gradient**2/2
        evidence.check('moving_domain_plus_temporal_boundary_flux_gives_pressure', sp.simplify(shape_force-pressure_force) == 0)
        source_velocity = sp.Matrix([1, velocity])/clock
        normal = sp.Matrix([velocity/(lapse*root), lapse*root])/clock
        metric = sp.diag(-lapse**2, root**-2)
        evidence.check('source_unit_timelike', sp.simplify((source_velocity.T*metric*source_velocity)[0]+1) == 0)
        evidence.check('source_normal_unit_spacelike', sp.simplify((normal.T*metric*normal)[0]-1) == 0)
        evidence.check('source_normal_orthogonal', sp.simplify((normal.T*metric*source_velocity)[0]) == 0)
        normal_gradient = (normal.T*sp.Matrix([temporal, gradient]))[0].subs(temporal, -velocity*gradient)
        pressure = sp.simplify(normal_gradient**2/2)
        evidence.check('coordinate_force_is_rest_pressure_with_geometric_measure', sp.simplify(pressure_force-radius**2*lapse/root*pressure) == 0)
        lapse_radial, root_radial = sp.symbols('N_R U_R', real=True)
        particle_action = -source*clock
        material_covector = sp.diff(particle_action, lapse)*lapse_radial+sp.diff(particle_action, root)*root_radial
        expected_covector = -source*(lapse*lapse_radial+velocity**2*root_radial/root**3)/clock
        evidence.check('material_coordinate_force_retains_metric_gradients', sp.simplify(material_covector-expected_covector) == 0)
        energy = sp.sqrt(source**2+root**2*momentum**2)
        material_velocity = lapse*root**2*momentum/energy
        dust_terms = -lapse**2*root**3*momentum**2/energy+2*lapse*root*momentum*velocity-energy*velocity**2/root
        evidence.check('own_smooth_dust_density_cancels_in_proper_acceleration', sp.simplify(dust_terms.subs(velocity, material_velocity)) == 0)
        mass_radial = coupling*radius**2*density+coupling*root*energy*weight
        log_lapse_radial = mass/(radius**2*root**2)+coupling*radius*density/root**2+coupling*root*momentum**2/(radius*energy)*weight
        root_time = -coupling*radius*root*flux+coupling*lapse*root**2*momentum/radius*weight
        root_space = (mass/radius**2-mass_radial/radius)/root
        geometric_acceleration_numerator = -root**2*lapse**2*log_lapse_radial+2*root_time/root*velocity+root_space/root*velocity**2
        reduced = -clock_squared*mass/radius**2-coupling*radius*((lapse**2+velocity**2/root**2)*density+2*velocity*flux)
        evidence.check('proper_acceleration_mass_plus_wave_focusing_after_self_cancellation',
                       sp.simplify((geometric_acceleration_numerator-reduced).subs(velocity, material_velocity)) == 0)
        scalar_density = (temporal**2/lapse**2+root**2*gradient**2)/2
        observed_density = ((temporal+velocity*gradient)**2+(lapse*root*gradient+velocity*temporal/(lapse*root))**2)/(2*clock_squared)
        focusing = ((lapse**2+velocity**2/root**2)*scalar_density+2*velocity*temporal*gradient)/clock_squared
        evidence.check('wave_focusing_is_positive_source_frame_energy_density', sp.simplify(focusing-observed_density) == 0)
        evidence.check('normal_radial_component_matches_proper_radial_gamma', sp.simplify((lapse*root/clock)**2-root**2-(velocity/clock)**2) == 0)
        evidence.check('dust_limit_recovers_radial_GR_acceleration', sp.simplify((-mass/radius**2-coupling*radius*focusing).subs({temporal:0, gradient:0})+mass/radius**2) == 0)
        evidence.report.update(
            continuum_coordinate_force='F_wave = R^2 N/U (Pi_minus-Pi_plus) = (C-R^4 V^2/C)(H_minus^2-H_plus^2)/2',
            rest_pressure='Pi_side = U^2 (1-V^2/(N^2 U^2)) H_side^2/2',
            proper_acceleration='R_tautau = -mu/R^2 - kappa R <rho_wave_in_source_frame> + R^2 sqrt(U^2+R_tau^2)/S * (Pi_minus-Pi_plus)',
            assumptions='Positive finite ordered material width; regular polar metric; minimally coupled continuum scalar; zero source trace on both sides; fixed proper-time source mass; smooth averaged Einstein radial/current equations.',
            finite_action_force_is_L_b_minus_time_derivative_of_field_source_momentum=True,
            moving_boundary_force_derived=True, self_density_cancellation_derived=True,
            original_Gram_terms_discarded_at_finite_resolution=False,
            finite_action_continuum_convergence_proven=False, full_GR_limit_proven=False, valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
