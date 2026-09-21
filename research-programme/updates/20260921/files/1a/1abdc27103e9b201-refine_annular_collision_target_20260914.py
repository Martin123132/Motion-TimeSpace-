import os
for name in ['OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS']:
    os.environ[name] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
from navier_stokes_source_audit_20260908 import limit_process
limit_process()

import json
from time import perf_counter
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
from annular_reference_continuum_shell_20260914 import EvidenceRun
from annular_reflecting_boundary_20260914 import ReflectingContinuum
from verify_annular_collision_and_support_20260914 import support, minimum_nec_reservoir


def run():
    evidence = EvidenceRun('annular-collision-refined-target-attempt01', __file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        failed_path = intake/'annular-collision-support-verification-attempt01/status.json'
        failed = json.loads(failed_path.read_text())
        evidence.own(failed_path)
        evidence.check('failed_absolute_radial_gate_preserved', failed['state'] == 'failed' and 'radial_37_active_constraints' in failed['error'])
        evidence.report.update(scope='4097-node refinement of unchanged continuum equation and boundary scheme; original2e-9 radial gate retained.',
                               no_dense_trajectory_retained=True, old_absolute_radial_gate_was_not_passed=True,
                               source_support_action_derived=False, source_parameter_changed=False)
        old_path = intake/'annular-source-collision-continuum-attempt01/continuum_count2049.npz'
        evidence.own(old_path)
        old = dict(np.load(old_path, allow_pickle=False))
        system = ReflectingContinuum(4097)
        started = perf_counter()
        solution = solve_ivp(system.rhs, (0., .45), system.initial_state, method='DOP853', rtol=2e-11, atol=2e-13,
                             max_step=system.spacing/4, t_eval=old['times'], dense_output=False)
        evidence.check('fine_evolution_finished', solution.success)
        states = solution.y.T
        masses, lapses, energies, rows = [], [], [], []
        for time, state in zip(old['times'], states):
            geometry = system.geometry(state)
            scalar, gradient, momentum = system.unpack(state)
            force = 36*geometry['L'][-1]*gradient[-1]
            minimum = minimum_nec_reservoir(6., .1, geometry['U_minus'], geometry['density'][-1])
            minimum_sigma, minimum_pressure, minimum_root = support(6., .1, minimum, geometry['U_minus'], geometry['density'][-1])
            pressure_direct = ((geometry['mass_plus']/(36*geometry['U_plus'])+geometry['U_plus']/6)-
                              (geometry['mass'][-1]/(36*geometry['U_minus'])+.1*geometry['U_minus']*geometry['density'][-1]/6+geometry['U_minus']/6))/.2
            row = dict(time=float(time), mass_plus=float(geometry['mass_plus']), minimum_F=float(geometry['F'].min()),
                       wall_force=float(force), wall_gradient=float(gradient[-1]), source_pressure=float(geometry['P']),
                       source_density=float(geometry['Sigma']), surface_null_contraction=float(geometry['Sigma']+geometry['P']),
                       minimum_reservoir_for_nec_at_frozen_interior=float(minimum),
                       source_power=float(force*geometry['L'][-1]*momentum[-1]/36),
                       boundary_error=float(max(abs(gradient[0]), abs(scalar[-1]), abs(momentum[-1]))),
                       junction_error=float(abs(pressure_direct-geometry['P'])),
                       nec_threshold_error=float(abs(minimum_sigma+minimum_pressure)))
            rows.append(row)
            masses.append(geometry['mass'])
            lapses.append(geometry['log_N'])
            energies.append(geometry['energy'])
        output = evidence.output/'continuum_count4097.npz'
        np.savez_compressed(output, times=old['times'], radii=system.radii, states=states,
                            masses=np.array(masses), log_lapses=np.array(lapses), energies=np.array(energies))
        evidence.own(output, 'outputs')
        evidence.report['diagnostics'] = rows
        evidence.report['seconds'] = perf_counter()-started
        evidence.report['calls'] = system.calls
        drift = max(abs(row['mass_plus']-rows[0]['mass_plus']) for row in rows)
        evidence.report['mass_drift'] = drift
        evidence.check('refined_mass_drift_below_previous', drift < 1.432054475003497e-9, drift)
        evidence.check('regular_fixed_source_active', min(row['minimum_F'] for row in rows) > .5 and max(abs(row['wall_force']) for row in rows) > .1)
        evidence.check('no_boundary_work', max(max(abs(row['source_power']), row['boundary_error']) for row in rows) < 1e-13)
        evidence.check('independent_junction_and_nec_root', max(max(row['junction_error'], row['nec_threshold_error']) for row in rows) < 1e-14)
        field_error = np.max(abs(states.reshape(46, 3, 4097)[:, :, ::2]-old['states'].reshape(46, 3, 2049)), axis=(0, 2))
        evidence.report['refinement'] = dict(field_max_errors=field_error.tolist(),
            mass_max_error=float(abs(np.array(masses)[:, ::2]-old['masses']).max()),
            log_lapse_max_error=float(abs(np.array(lapses)[:, ::2]-old['log_lapses']).max()))
        evidence.check('fine_all_fields_improve', all(value < bound for value, bound in zip(field_error, [1.790774931801496e-7, 3.774841249555371e-5, .0011396029315903777])))
        evidence.check('fine_metric_improves', evidence.report['refinement']['mass_max_error'] < 1.9218820979105544e-8 and evidence.report['refinement']['log_lapse_max_error'] < 5.838003747093978e-9)
        evidence.save()
        print('4097 evolution saved; independent radial checks next', flush=True)
        for index in [37, 45]:
            state = states[index]
            scalar, gradient, momentum = system.unpack(state)
            gradient_spline = CubicSpline(system.radii, gradient)
            momentum_spline = CubicSpline(system.radii, momentum)

            def radial_rhs(radius, values):
                density = .5*(radius**2*gradient_spline(radius)**2+momentum_spline(radius)**2/radius**2)
                geometry = 1-2*values[0]/radius
                return [.1*geometry*density, values[0]/(radius**2*geometry)+.1*density/radius]

            geometry = system.geometry(state)
            independent = []
            for divisor in [4096, 8192]:
                result = solve_ivp(radial_rhs, (5., 6.), [.8, 0.], method='DOP853', rtol=2e-12, atol=2e-14,
                                   max_step=1/divisor, t_eval=system.radii)
                evidence.check(str(index)+'_radial_solver_'+str(divisor), result.success)
                lapse = result.y[1]+np.log(geometry['N_shell'])-result.y[1, -1]
                errors = dict(mass=float(abs(result.y[0]-geometry['mass']).max()), log_lapse=float(abs(lapse-geometry['log_N']).max()))
                evidence.check(str(index)+'_original_absolute_gate_'+str(divisor), max(errors.values()) < 2e-9, errors)
                independent.append(np.array([result.y[0], lapse]))
            difference = float(abs(independent[1]-independent[0]).max())
            evidence.check(str(index)+'_radial_integrator_step_refinement', difference < 1e-11, difference)
        evidence.report.update(current_rigid_source_satisfies_surface_NEC=False,
                               nec_bound_is_not_a_parent_derived_parameter=True,
                               first_sampled_nec_violation=next(row['time'] for row in rows if row['surface_null_contraction'] < 0),
                               minimum_surface_null_contraction=min(row['surface_null_contraction'] for row in rows),
                               maximum_frozen_interior_minimum_reservoir=max(row['minimum_reservoir_for_nec_at_frozen_interior'] for row in rows))
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    run()
