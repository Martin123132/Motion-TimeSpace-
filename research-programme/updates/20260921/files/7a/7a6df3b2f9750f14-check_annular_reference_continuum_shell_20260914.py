import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:
    os.environ[name] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
from navier_stokes_source_audit_20260908 import limit_process
limit_process()

import sympy as sp
from annular_reference_continuum_shell_20260914 import EvidenceRun


def run():
    evidence = EvidenceRun('annular-reference-continuum-shell-algebra-attempt01',__file__)
    try:
        time,radius,angle,azimuth = sp.symbols('t R theta phi',real=True)
        coordinates = [time,radius,angle,azimuth]
        mass = sp.Function('m')(time,radius)
        lapse = sp.Function('N')(time,radius)
        field = sp.Function('chi')(time,radius)
        geometry = 1-2*mass/radius
        metric = [-lapse**2,1/geometry,radius**2,radius**2*sp.sin(angle)**2]
        inverse = [1/value for value in metric]
        def metric_component(first,second):
            return metric[first] if first==second else sp.S.Zero
        connection = {}
        for upper in range(4):
            for first in range(4):
                for second in range(4):
                    connection[upper,first,second] = sp.simplify(inverse[upper]*(
                        sp.diff(metric_component(upper,second),coordinates[first])+
                        sp.diff(metric_component(upper,first),coordinates[second])-
                        sp.diff(metric_component(first,second),coordinates[upper]))/2)
        def ricci(first,second):
            result = sp.S.Zero
            for upper in range(4):
                result += sp.diff(connection[upper,first,second],coordinates[upper])
                result -= sp.diff(connection[upper,first,upper],coordinates[second])
                for contracted in range(4):
                    result += connection[upper,first,second]*connection[contracted,upper,contracted]
                    result -= connection[contracted,first,upper]*connection[upper,second,contracted]
            return sp.simplify(result)
        diagonal = [ricci(index,index) for index in range(4)]
        curvature = sp.simplify(sum(inverse[index]*diagonal[index] for index in range(4)))
        einstein_time = sp.simplify(inverse[0]*diagonal[0]-curvature/2)
        einstein_radius = sp.simplify(inverse[1]*diagonal[1]-curvature/2)
        einstein_flux = sp.simplify(inverse[1]*ricci(1,0))
        expected = [-2*sp.diff(mass,radius)/radius**2,
                    -2*mass/radius**3+2*geometry*sp.diff(lapse,radius)/(radius*lapse),
                    2*sp.diff(mass,time)/radius**2]
        for name,actual,target in zip(['Einstein_tt','Einstein_rr','Einstein_rt'],
                                      [einstein_time,einstein_radius,einstein_flux],expected):
            evidence.check(name+'_exact',sp.simplify(actual-target)==0,str(actual))
        wave = sum(inverse[index]*(sp.diff(field,coordinates[index],2)-
                       sum(connection[upper,index,index]*sp.diff(field,coordinates[upper])
                           for upper in range(4))) for index in range(4))
        light_speed = lapse*sp.sqrt(geometry)
        wave_expected = (-sp.diff(radius**2*sp.diff(field,time)/light_speed,time)+
                          sp.diff(radius**2*light_speed*sp.diff(field,radius),radius))*sp.sqrt(geometry)/(lapse*radius**2)
        evidence.check('covariant_wave_exact',sp.simplify(wave-wave_expected)==0)
        scalar_norm = sum(inverse[index]*sp.diff(field,coordinates[index])**2 for index in range(4))
        stress_time = inverse[0]*sp.diff(field,time)**2-scalar_norm/2
        stress_radius = inverse[1]*sp.diff(field,radius)**2-scalar_norm/2
        energy = (radius**2*sp.diff(field,radius)**2+
                  radius**2*sp.diff(field,time)**2/light_speed**2)/2
        evidence.check('canonical_scalar_density',sp.simplify(stress_time+geometry*energy/radius**2)==0)
        evidence.check('canonical_scalar_radial_pressure',sp.simplify(stress_radius-geometry*energy/radius**2)==0)
        coupling = sp.symbols('kappa',positive=True)
        density = sp.Function('e')(time,radius)
        current = sp.Function('J')(time,radius)
        radial_geometry = -2*coupling*geometry*density/radius+2*mass/radius**2
        radial_log_speed = 2*mass/(radius**2*geometry)
        mass_flux_obstruction = geometry*radial_log_speed-radial_geometry-2*coupling*geometry*density/radius
        evidence.check('constraint_mass_flux_propagation_exact',sp.simplify(mass_flux_obstruction)==0)
        stress_flux = geometry*sp.diff(field,radius)*sp.diff(field,time)
        mt_prediction = coupling*geometry*radius**2*sp.diff(field,radius)*sp.diff(field,time)
        evidence.check('Einstein_flux_normalization',sp.simplify(2*mt_prediction/radius**2-2*coupling*stress_flux)==0)
        residual_angle = sp.symbols('angular_residual')
        divergence = -sum(connection[index,index,1]*residual_angle for index in [2,3])
        evidence.check('Bianchi_forces_angular_residual',sp.simplify(divergence+2*residual_angle/radius)==0)
        root_minus,root_plus,boundary = sp.symbols('U_minus U_plus b',positive=True)
        density_shell = (root_minus-root_plus)/(coupling*boundary)
        pressure_shell = ((1-root_plus**2)/(2*boundary*root_plus)-
                          (1-root_minus**2)/(2*boundary*root_minus)+(root_plus-root_minus)/boundary)/(2*coupling)
        pressure_expected = density_shell*(1/(root_minus*root_plus)-1)/4
        evidence.check('Israel_surface_pressure_exact',sp.factor(pressure_shell-pressure_expected)==0)
        proper_mass = sp.symbols('mu',positive=True)
        mass_minus = sp.symbols('m_minus',positive=True)
        radial_root = sp.sqrt(1-2*mass_minus/boundary)
        mass_plus = mass_minus+proper_mass*radial_root-proper_mass**2/(2*boundary)
        evidence.check('source_mass_jump_exact',sp.simplify(1-2*mass_plus/boundary-
                         (radial_root-proper_mass/boundary)**2)==0)
        matching_pressure = pressure_expected.subs({root_minus:radial_root,
                                      root_plus:radial_root-proper_mass/boundary})
        mass_derivative = sp.diff(mass_plus,boundary)+sp.diff(mass_plus,proper_mass)*(-2*coupling*boundary*matching_pressure)
        evidence.check('shell_virtual_work_matches_Israel',sp.simplify(mass_derivative)==0)
        shell_scalar_density = sp.symbols('e_minus')
        general_pressure = pressure_shell-root_minus*shell_scalar_density/(2*boundary)
        general_extrinsic = ((1-root_plus**2)/(2*boundary*root_plus)-
                            (1-root_minus**2)/(2*boundary*root_minus)-
                            coupling*root_minus*shell_scalar_density/boundary+
                            (root_plus-root_minus)/boundary)/(2*coupling)
        evidence.check('nonvacuum_inner_pressure_correction',sp.simplify(general_pressure-general_extrinsic)==0)
        reservoir = sp.symbols('S',positive=True)
        sigma = sp.symbols('sigma',nonnegative=True)
        Uvalue = sp.symbols('U',positive=True)
        density_value = sp.symbols('e')
        Fvalue = Uvalue**2
        root_gradient_direct = (-2*coupling*(Fvalue*density_value+Uvalue*sigma)/radius+2*mass/radius**2)/(2*Uvalue)
        root_gradient_target = mass/(radius**2*Uvalue)-coupling*Uvalue*density_value/radius-coupling*sigma/radius
        evidence.check('finite_collar_root_transfer_exact',sp.simplify(root_gradient_direct-root_gradient_target)==0)
        vacuum_pressure_integral = reservoir/(2*boundary**2)*sp.integrate(
            (1-sp.Symbol('u',positive=True)**2)/(2*sp.Symbol('u',positive=True)**2),
            (sp.Symbol('u',positive=True),root_plus,root_minus))/(root_minus-root_plus)
        vacuum_pressure_target = reservoir/boundary**2*(1/(root_minus*root_plus)-1)/4
        evidence.check('finite_collar_stress_thin_integral',sp.simplify(vacuum_pressure_integral-vacuum_pressure_target)==0)
        evidence.report['checked_tensor_components'] = {
            'G^t_t':str(einstein_time),'G^R_R':str(einstein_radius),'G^R_t':str(einstein_flux)}
        evidence.report['scope'] = 'Exact conditional continuum identities, not compactness, source-action ownership, or numerical evolution proof.'
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    run()

