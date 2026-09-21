import os
for name in ['OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS']:
    os.environ[name] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
from navier_stokes_source_audit_20260908 import limit_process
limit_process()

import json
import numpy as np
from scipy.integrate import solve_ivp
from annular_reference_continuum_shell_20260914 import EvidenceRun
from annular_dynamical_source_20260914 import shell_geometry, shell_acceleration, reflecting_trace, quiet_pressure, DustSurface, CausalSurface, vacuum_rhs


def quiet_slope(radius, mass, reservoir, pressure, sound, coupling=.1):
    data = shell_geometry(radius, 0., mass, reservoir, coupling)
    root, outer = data['beta_minus'], data['beta_plus']
    density = reservoir/radius**2
    ratio = pressure/density
    root_rate = mass/(radius**2*root)
    reservoir_rate = -2*radius*pressure
    outer_rate = root_rate-coupling*reservoir_rate/radius+coupling*reservoir/radius**2
    ratio_rate = -2*(1+ratio)*(sound-ratio)/radius
    return (2*ratio_rate*root*outer/radius+2*ratio*(root_rate*outer+root*outer_rate)/radius-
            2*ratio*root*outer/radius**2+2*mass/radius**3-
            coupling*(reservoir_rate*root+reservoir*root_rate)/(2*radius**2)+coupling*reservoir*root/radius**3)


def run():
    evidence = EvidenceRun('annular-dynamical-source-numerics-attempt01', __file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        algebra_path = intake/'annular-dynamical-source-algebra-attempt02/status.json'
        algebra = json.loads(algebra_path.read_text())
        evidence.own(algebra_path)
        evidence.check('symbolic_identities_passed', algebra['state'] == 'complete' and all(row['passed'] for row in algebra['checks']))
        evidence.report.update(scope='Local covariant shell identities, vacuum self-gravitating source and material stability controls; no prescribed old pulse used as a moving-boundary drive.',
            material_and_reflection_parent_derived=False, coupled_moving_GR_scalar_PDE_tested=False)
        initial_path = intake/'annular-collision-refined-target-attempt01/continuum_count4097.npz'
        evidence.own(initial_path)
        initial = np.load(initial_path, allow_pickle=False)
        interior_mass = float(initial['masses'][0, -1])
        radius, reservoir = 6., .003
        equilibrium_pressure = quiet_pressure(radius, interior_mass, reservoir)
        density = reservoir/radius**2
        data = shell_geometry(radius, 0., interior_mass, reservoir)
        slope_zero = quiet_slope(radius, interior_mass, reservoir, equilibrium_pressure, 0.)
        slope_coefficient = 4*(1+equilibrium_pressure/density)*data['beta_minus']*data['beta_plus']/radius**2
        critical_sound = slope_zero/slope_coefficient
        evidence.report['quiet_material'] = dict(radius=radius, reservoir=reservoir, interior_mass=interior_mass,
            equilibrium_pressure=equilibrium_pressure, pressure_density_ratio=equilibrium_pressure/density,
            radial_stability_critical_sound_squared=critical_sound, chosen_sound_squared=.5,
            calibration_scope='Static reference state only; a material-law example, not a parent-selected coefficient.')
        evidence.check('causal_stable_material_interval_nonempty', 0 < critical_sound < .5 < 1 and equilibrium_pressure/density < .5)
        evidence.check('slope_threshold_zero', abs(quiet_slope(radius, interior_mass, reservoir, equilibrium_pressure, critical_sound)) < 1e-14)
        material = CausalSurface(radius, reservoir, equilibrium_pressure, .5)
        slope = quiet_slope(radius, interior_mass, reservoir, equilibrium_pressure, .5)
        def acceleration_at(value):
            energy, pressure = material.stress(value)
            return shell_acceleration(value, 0., interior_mass, energy, pressure, 0.)
        complex_slope = float(np.imag(acceleration_at(radius+1e-25j))/1e-25)
        evidence.check('independent_complex_step_stability_slope', abs(complex_slope-slope) < 2e-13, dict(analytic=slope, complex_step=complex_slope))
        evidence.report['quiet_material']['proper_frequency'] = float(np.sqrt(-slope))
        weak_sound = max(equilibrium_pressure/density+.001, critical_sound-.02)
        evidence.check('causal_but_unstable_material_negative_control', weak_sound < critical_sound and quiet_slope(radius, interior_mass, reservoir, equilibrium_pressure, weak_sound) > 0)
        maximum_first_law = 0.
        for sample_radius in np.geomspace(3., 12., 101):
            energy, pressure = material.stress(sample_radius)
            density = energy/sample_radius**2
            derivative = np.imag(material.stress(sample_radius+1e-25j)[0])/1e-25
            maximum_first_law = max(maximum_first_law, abs(derivative+2*sample_radius*pressure))
            if not (density > 0 and density-abs(pressure) >= 0):
                raise RuntimeError('Material energy condition failed.')
        evidence.check('material_pressure_is_action_first_law', maximum_first_law < 1e-14, maximum_first_law)
        evidence.check('sampled_material_dominant_energy_condition', True)
        random = np.random.default_rng(91426)
        maximum_time_jump = maximum_force_balance = maximum_clock_error = maximum_comoving_error = 0.
        for sample in range(60):
            sample_radius = random.uniform(5.5, 8.)
            proper_rate = random.uniform(-.7, .7)
            mass = random.uniform(.4, 1.)
            energy = random.uniform(.003, .02)
            pressure = random.uniform(-.5, .5)*energy/sample_radius**2
            gradient = random.uniform(-.15, .15)
            lapse = random.uniform(.7, .95)
            trace = reflecting_trace(sample_radius, proper_rate, mass, gradient, lapse)
            geometry = shell_geometry(sample_radius, proper_rate, mass, energy)
            beta, outer = geometry['beta_minus'], geometry['beta_plus']
            acceleration = shell_acceleration(sample_radius, proper_rate, mass, energy, pressure, trace['normal_pressure'])
            curvature_inner = (acceleration+mass/sample_radius**2+.1*sample_radius*trace['normal_pressure'])/beta
            curvature_outer = (acceleration+geometry['mass_plus']/sample_radius**2)/outer
            maximum_time_jump = max(maximum_time_jump, abs(curvature_outer-curvature_inner-.1*(energy/sample_radius**2+2*pressure)))
            balance = -energy/sample_radius**2*(curvature_outer+curvature_inner)/2+pressure*(beta+outer)/sample_radius+trace['normal_pressure']
            maximum_force_balance = max(maximum_force_balance, abs(balance))
            chi_time = lapse*np.sqrt(geometry['F_minus'])*trace['momentum']/sample_radius**2
            maximum_comoving_error = max(maximum_comoving_error, abs(chi_time+trace['coordinate_rate']*gradient))
            for label, root_beta, metric in [('inner', beta, geometry['F_minus']), ('outer', outer, geometry['F_plus'])]:
                clock = root_beta/(lapse*np.sqrt(metric))
                maximum_clock_error = max(maximum_clock_error, abs(-lapse**2*clock**2+proper_rate**2/metric+1))
        evidence.check('numeric_temporal_junction', maximum_time_jump < 5e-12, maximum_time_jump)
        evidence.check('numeric_normal_shape_force_balance', maximum_force_balance < 1e-14, maximum_force_balance)
        evidence.check('moving_reflection_not_fixed_p_zero', maximum_comoving_error < 1e-15, maximum_comoving_error)
        evidence.check('two_clock_induced_metric_matches', maximum_clock_error < 2e-14, maximum_clock_error)
        probe = shell_geometry(6., .4, interior_mass, reservoir)
        coordinate_rate = .85*np.sqrt(probe['F_minus'])*.4/probe['beta_minus']
        wrong_jump = coordinate_rate**2*(1/probe['F_plus']-1/probe['F_minus'])
        evidence.check('naive_shared_moving_lapse_rejected', abs(wrong_jump) > 1e-7, float(wrong_jump))
        reference_held = equilibrium_pressure-np.sqrt(1-2*interior_mass/6)*36*.12**2/4/6
        pressure_normal = .5*(1-2*interior_mass/6)*.12**2
        evidence.check('held_pressure_limit_gives_zero_acceleration', abs(shell_acceleration(6., 0., interior_mass, reservoir, reference_held, pressure_normal)) < 5e-13)
        evidence.check('zero_tension_dust_recoils_instead', shell_acceleration(6., 0., interior_mass, reservoir, 0., pressure_normal) > 1.)
        weak_gravity_errors = []
        for coupling in [1e-3, 1e-4, 1e-5]:
            central_reduced = 8.
            exact = shell_acceleration(6., 0., coupling*central_reduced, reservoir, 0., 0., coupling)
            newton = -coupling*(central_reduced+reservoir/2)/36
            weak_gravity_errors.append(float(abs(exact/newton-1)))
        evidence.check('Newton_central_plus_half_self_mass_refines', all(later < earlier for earlier,later in zip(weak_gravity_errors,weak_gravity_errors[1:])), weak_gravity_errors)
        for label, chosen, perturbation, duration in [('dust', DustSurface(reservoir), 0., 2.), ('causal_rest', material, 0., 80.), ('causal_displaced', material, .001, 80.)]:
            state = np.array([radius+perturbation, 0., interior_mass])
            times = np.linspace(0., duration, 401)
            rhs = vacuum_rhs(chosen)
            result = solve_ivp(rhs, (0., duration), state, method='DOP853', rtol=2e-11, atol=2e-13, max_step=.05, t_eval=times)
            evidence.check(label+'_solver_finished', result.success)
            exterior_masses, densities, pressures = [], [], []
            for current_radius, proper_rate, mass in result.y.T:
                energy, pressure = chosen.stress(current_radius)
                exterior_masses.append(float(shell_geometry(current_radius, proper_rate, mass, energy)['mass_plus']))
                densities.append(float(energy/current_radius**2))
                pressures.append(float(pressure))
            drift = float(np.max(abs(np.array(exterior_masses)-exterior_masses[0])))
            evidence.check(label+'_exterior_mass_conserved', drift < 1e-10, drift)
            evidence.check(label+'_material_energy_conditions', min(np.array(densities)-abs(np.array(pressures))) >= 0)
            if label == 'dust':
                evidence.check('dust_falls_without_artificial_support', result.y[0,-1] < 6. and result.y[1,-1] < 0.)
            elif label == 'causal_rest':
                evidence.check('action_supported_quiet_equilibrium', float(abs(result.y[0]-6.).max()) < 1e-10)
            else:
                evidence.check('displaced_shell_returns_and_stays_bounded', result.y[0].min() < 6. and result.y[0].max() < 6.002)
            output = evidence.output/(label+'.npz')
            np.savez_compressed(output, proper_times=times, states=result.y.T, exterior_mass=exterior_masses, surface_density=densities, surface_pressure=pressures)
            evidence.own(output, 'outputs')
            evidence.report['cases'].append(dict(branch=label, duration=duration, final_state=result.y[:,-1].tolist(),
                radius_min=float(result.y[0].min()), radius_max=float(result.y[0].max()), mass_drift=drift))
            if label == 'causal_displaced':
                tighter = solve_ivp(rhs, (0., duration), state, method='DOP853', rtol=2e-12, atol=2e-14, max_step=.025, t_eval=times)
                evidence.check('vacuum_evolution_time_refinement', tighter.success and float(abs(tighter.y-result.y).max()) < 1e-10, float(abs(tighter.y-result.y).max()))
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    run()
