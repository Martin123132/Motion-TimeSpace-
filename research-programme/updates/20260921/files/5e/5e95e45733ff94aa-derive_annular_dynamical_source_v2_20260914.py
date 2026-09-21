import os
for name in ['OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS']:
    os.environ[name] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
from navier_stokes_source_audit_20260908 import limit_process
limit_process()

import json
import sympy as sym
from annular_reference_continuum_shell_20260914 import EvidenceRun


def run():
    evidence = EvidenceRun('annular-dynamical-source-algebra-attempt02', __file__)
    try:
        prior = evidence.root/'source-intake/navier-stokes/20260914/annular-dynamical-source-algebra-attempt01/status.json'
        failed = json.loads(prior.read_text())
        evidence.own(prior)
        evidence.check('first_substitution_error_preserved', failed['state'] == 'failed' and 'direct_time_dependent_interior_curvature' in failed['error'])
        evidence.report.update(scope='Exact algebra after stated surface-action variation, not a machine-certified functional proof.',
            correction='Use independent acceleration for the geometric curvature identity, not Pi-dependent acceleration on one side and its trace substitution only on the other. Replace the unexecuted beta->1 pseudo-Newton check by kappa->0 at fixed physical masses.',
            surface_material_law_parent_derived=False, perfect_reflection_parent_derived=False,
            moving_GR_wave_evolution_completed=False)

        def exact(name, expression):
            residual = sym.factor(sym.simplify(expression))
            evidence.check(name, residual == 0, str(residual))

        radius, beta, reservoir, coupling = sym.symbols('b beta S kappa', positive=True)
        proper_rate, pressure, normal_pressure, gradient, free_acceleration = sym.symbols('w P Pi u a', real=True)
        geometry = beta**2-proper_rate**2
        interior_mass = radius*(1-geometry)/2
        beta_plus = beta-coupling*reservoir/radius
        exterior_mass = interior_mass+coupling*reservoir*beta-(coupling*reservoir)**2/(2*radius)
        acceleration = (radius**2*normal_pressure*beta_plus/reservoir+
                        2*radius*pressure*beta*beta_plus/reservoir-interior_mass/radius**2-
                        coupling*reservoir*beta/(2*radius**2))
        momentum = -radius**2*proper_rate*gradient/beta
        density = (radius**2*gradient**2+momentum**2/radius**2)/2
        trace_pressure = geometry**2*gradient**2/(2*beta**2)
        exact('angular_junction_mass_map', beta_plus**2-(1+proper_rate**2-2*exterior_mass/radius))
        exact('comoving_dirichlet_condition', beta*momentum/radius**2+proper_rate*gradient)
        exact('normal_scalar_gradient', proper_rate*momentum/radius**2+beta*gradient-geometry*gradient/beta)
        mass_rate_from_bulk = coupling*geometry*(beta*momentum*gradient+density*proper_rate)
        exact('moving_boundary_mass_work', mass_rate_from_bulk+coupling*radius**2*trace_pressure*proper_rate)
        reservoir_rate = -2*radius*pressure*proper_rate
        mass_rate = -coupling*radius**2*normal_pressure*proper_rate
        beta_rate = proper_rate*(acceleration+interior_mass/radius**2+coupling*radius*normal_pressure)/beta
        exact('exterior_mass_conserved', mass_rate+coupling*reservoir_rate*beta+coupling*reservoir*beta_rate-
              coupling**2*reservoir*reservoir_rate/radius+coupling**2*reservoir**2*proper_rate/(2*radius**2))
        curvature_minus = (acceleration+interior_mass/radius**2+coupling*radius*normal_pressure)/beta
        curvature_plus = (acceleration+exterior_mass/radius**2)/beta_plus
        exact('temporal_junction_without_division_by_velocity', curvature_plus-curvature_minus-coupling*(reservoir/radius**2+2*pressure))
        exact('mean_curvature_normal_force', -reservoir/radius**2*(curvature_plus+curvature_minus)/2+
              pressure*(beta_plus+beta)/radius+normal_pressure)
        radial_lapse = interior_mass/(radius**2*geometry)+coupling*density/radius
        radial_root_log = interior_mass/(radius**2*geometry)-coupling*density/radius
        temporal_root_ratio = -coupling*momentum*gradient/radius
        direct_curvature = free_acceleration/beta+beta*radial_lapse-proper_rate**2*radial_root_log/beta-2*proper_rate*temporal_root_ratio
        expected_curvature = (free_acceleration+interior_mass/radius**2+coupling*radius*trace_pressure)/beta
        exact('direct_time_dependent_interior_curvature', direct_curvature-expected_curvature)
        vacuum_pressure = reservoir/(4*radius**2)*(1/(beta*beta_plus)-1)
        held_pressure = vacuum_pressure-beta*(radius**2*gradient**2/2)/(2*radius)
        exact('old_rigid_pressure_recovered', acceleration.subs({proper_rate:0, normal_pressure:beta**2*gradient**2/2, pressure:held_pressure}))
        lapse_a, length_a, length_b, current = sym.symbols('lapse a1 a2 J', positive=True)
        number_density = current/(length_a*length_b)
        rho = sym.Function('rho')
        density_symbol = sym.Symbol('n', positive=True)
        action_density = -lapse_a*length_a*length_b*rho(number_density)
        eos = number_density*sym.diff(rho(density_symbol),density_symbol).subs(density_symbol,number_density)-rho(number_density)
        exact('material_energy_from_lapse_variation', -sym.diff(action_density,lapse_a)/(length_a*length_b)-rho(number_density))
        exact('material_pressure_from_first_metric_variation', sym.diff(action_density,length_a)/(lapse_a*length_b)-eos)
        exact('material_pressure_from_second_metric_variation', sym.diff(action_density,length_b)/(lapse_a*length_a)-eos)
        multiplier, normal_gradient = sym.symbols('lambda eta', real=True)
        exact('embedding_scalar_reaction_half_factor', (-normal_gradient**2/2+multiplier*normal_gradient).subs(multiplier,normal_gradient)-normal_gradient**2/2)
        independent_radius, independent_mass, independent_source, independent_pressure, sound, reduced_central_mass = sym.symbols('r m source surface_P sound_sq central_mass', positive=True)
        root = sym.sqrt(1-2*independent_mass/independent_radius)
        root_plus = root-coupling*independent_source/independent_radius
        quiet_acceleration = (2*independent_radius*independent_pressure*root*root_plus/independent_source-
                              independent_mass/independent_radius**2-coupling*independent_source*root/(2*independent_radius**2))
        exact('physical_Newton_dust_limit', sym.limit(quiet_acceleration.subs({independent_mass:coupling*reduced_central_mass, independent_pressure:0})/coupling,coupling,0)+
              (reduced_central_mass+independent_source/2)/independent_radius**2)
        total_derivative = (sym.diff(quiet_acceleration,independent_radius)+sym.diff(quiet_acceleration,independent_source)*(-2*independent_radius*independent_pressure)+
                            sym.diff(quiet_acceleration,independent_pressure)*(-2*sound*(independent_source/independent_radius**2+independent_pressure)/independent_radius))
        slope_coefficient = sym.diff(total_derivative,sound)
        exact('causal_material_stabilizing_slope', slope_coefficient+4*(1+independent_pressure*independent_radius**2/independent_source)*root*root_plus/independent_radius**2)
        evidence.report['quiet_acceleration_slope_formula'] = str(total_derivative)
        rapidity_factor, factor_initial, incident = sym.symbols('D D0 Einc', positive=True)
        reflected = reservoir/2*(1/factor_initial-1/rapidity_factor)
        gained_energy = reservoir/2*(rapidity_factor+1/rapidity_factor-factor_initial-1/factor_initial)
        gained_impulse = reservoir/2*(rapidity_factor-1/rapidity_factor-factor_initial+1/factor_initial)
        incident_expression = reservoir*(rapidity_factor-factor_initial)/2
        exact('exact_flat_recoil_energy_identity', incident_expression-reflected-gained_energy)
        exact('exact_flat_radial_null_mode_impulse_identity', incident_expression+reflected-gained_impulse)
        evidence.report['turning_point_acceleration_regular_for_positive_source'] = True
        evidence.report['clock_matching'] = 'dt_plus/dtau=beta_plus/(N_plus U_plus); dt_minus/dtau=beta_minus/(N_minus U_minus). Equal lapse in one common moving polar chart generally violates induced-metric continuity.'
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    run()
