import os
for name in ['OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS']:
    os.environ[name] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
from navier_stokes_source_audit_20260908 import limit_process
limit_process()

import json
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
from annular_reference_continuum_shell_20260914 import EvidenceRun
from annular_reflecting_boundary_20260914 import ReflectingContinuum


def support(radius, coupling, reservoir, root_minus, density):
    root_plus = root_minus-coupling*reservoir/radius
    sigma = reservoir/radius**2
    pressure = sigma*(1/(root_minus*root_plus)-1)/4-root_minus*density/(2*radius)
    return sigma, pressure, root_plus


def minimum_nec_reservoir(radius, coupling, root_minus, density):
    geometry = root_minus**2
    constant = 2*coupling*density*geometry
    linear = 3*geometry+1+constant
    fraction = 2*constant/(linear+np.sqrt(linear**2-12*geometry*constant))
    return radius*root_minus*fraction/coupling


def run():
    evidence = EvidenceRun('annular-collision-support-verification-attempt01', __file__)
    try:
        folder = evidence.root/'source-intake/navier-stokes/20260914/annular-source-collision-continuum-attempt01'
        status_path = folder/'status.json'
        status = json.loads(status_path.read_text())
        evidence.own(status_path)
        evidence.check('continuum_completed', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
        evidence.report.update(scope='Independent active radial constraints/time-step checks and exact static-shell stress/NEC loading law.',
                               source_support_action_derived=False, alternative_source_model_evolved=False,
                               classical_energy_condition_applies_to_isotropic_timelike_surface_model_only=True)
        for count in [513, 1025, 2049]:
            path = folder/('continuum_count'+str(count)+'.npz')
            evidence.own(path)
            archive = dict(np.load(path, allow_pickle=False))
            system = ReflectingContinuum(count)
            rows = []
            maximum_junction_error = 0.
            maximum_force_error = 0.
            for time, state in zip(archive['times'], archive['states']):
                geometry = system.geometry(state)
                scalar, gradient, momentum = system.unpack(state)
                radius, coupling, reservoir = 6., .1, .003
                root_minus, root_plus = geometry['U_minus'], geometry['U_plus']
                sigma = (root_minus-root_plus)/(coupling*radius)
                outer_curvature = geometry['mass_plus']/(radius**2*root_plus)+root_plus/radius
                inner_curvature = geometry['mass'][-1]/(radius**2*root_minus)+coupling*root_minus*geometry['density'][-1]/radius+root_minus/radius
                pressure = (outer_curvature-inner_curvature)/(2*coupling)
                force = radius**2*geometry['L'][-1]*gradient[-1]
                vacuum_pressure = geometry['Sigma']*(1/(root_minus*root_plus)-1)/4
                from_force = vacuum_pressure-force**2/(4*radius**3*geometry['N_shell']**2*root_minus)
                maximum_junction_error = max(maximum_junction_error, abs(pressure-geometry['P']), abs(sigma-geometry['Sigma']))
                maximum_force_error = max(maximum_force_error, abs(from_force-pressure))
                minimum = minimum_nec_reservoir(radius, coupling, root_minus, geometry['density'][-1])
                bound_sigma, bound_pressure, bound_root = support(radius, coupling, minimum, root_minus, geometry['density'][-1])
                if minimum > 1e-10:
                    lower_sigma, lower_pressure, lower_root = support(radius, coupling, .99*minimum, root_minus, geometry['density'][-1])
                    upper_sigma, upper_pressure, upper_root = support(radius, coupling, 1.01*minimum, root_minus, geometry['density'][-1])
                    if not (abs(bound_sigma+bound_pressure) < 1e-13 and lower_sigma+lower_pressure < 0 and upper_sigma+upper_pressure > 0 and upper_root > 0):
                        raise RuntimeError('NEC threshold root fails independent bracketing at '+str(time))
                rows.append(dict(time=float(time), source_pressure=float(pressure), source_density=float(sigma),
                                 surface_null_contraction=float(sigma+pressure), source_force=float(force),
                                 minimum_reservoir_for_nec_at_frozen_interior=float(minimum),
                                 root_plus_at_threshold=float(bound_root), null_energy_condition_satisfied=bool(sigma+pressure >= 0)))
            evidence.check(str(count)+'_independent_junction_stress', maximum_junction_error < 1e-14, maximum_junction_error)
            evidence.check(str(count)+'_force_to_pressure_identity', maximum_force_error < 1e-14, maximum_force_error)
            evidence.check(str(count)+'_nec_threshold_bracketed', True)
            failed = [row for row in rows if not row['null_energy_condition_satisfied']]
            evidence.check(str(count)+'_quiet_shell_nec_and_collision_counterexample', rows[0]['null_energy_condition_satisfied'] and bool(failed))
            row = dict(count=count, first_sampled_nec_violation=failed[0]['time'],
                       minimum_surface_null_contraction=min(row['surface_null_contraction'] for row in rows),
                       maximum_frozen_interior_minimum_reservoir=max(row['minimum_reservoir_for_nec_at_frozen_interior'] for row in rows),
                       rows=rows)
            evidence.report['cases'].append(row)
            if count == 2049:
                for index in [37, 45]:
                    state = archive['states'][index]
                    scalar, gradient, momentum = system.unpack(state)
                    gradient_spline = CubicSpline(system.radii, gradient)
                    momentum_spline = CubicSpline(system.radii, momentum)

                    def radial_rhs(radius, values):
                        density = .5*(radius**2*gradient_spline(radius)**2+momentum_spline(radius)**2/radius**2)
                        geometry_value = 1-2*values[0]/radius
                        return [.1*geometry_value*density, values[0]/(radius**2*geometry_value)+.1*density/radius]

                    reference = solve_ivp(radial_rhs, (5., 6.), [.8, 0.], method='DOP853', rtol=2e-12, atol=2e-14,
                                          max_step=1/2048, t_eval=system.radii)
                    evidence.check('radial_'+str(index)+'_completed', reference.success)
                    geometry = system.geometry(state)
                    lapse = reference.y[1]+np.log(geometry['N_shell'])-reference.y[1, -1]
                    error = dict(mass=float(abs(reference.y[0]-geometry['mass']).max()),
                                 log_lapse=float(abs(lapse-geometry['log_N']).max()))
                    evidence.check('radial_'+str(index)+'_active_constraints', max(error.values()) < 2e-9, error)
            if count == 513:
                initial = archive['states'][35].copy()
                duration = .002
                steps = 128
                step = duration/steps
                evolved = initial.copy()
                for index in range(steps):
                    time = .35+index*step
                    first = system.rhs(time, evolved)
                    second = system.rhs(time+step/2, evolved+step*first/2)
                    third = system.rhs(time+step/2, evolved+step*second/2)
                    fourth = system.rhs(time+step, evolved+step*third)
                    evolved += step*(first+2*second+2*third+fourth)/6
                dop = solve_ivp(system.rhs, (.35, .352), initial, method='DOP853', rtol=2e-13, atol=2e-15, max_step=step)
                temporal_error = float(abs(evolved-dop.y[:, -1]).max())
                evidence.check('independent_active_RK4_time_check', dop.success and temporal_error < 2e-10, temporal_error)
            evidence.save()
        maxima = [row['maximum_frozen_interior_minimum_reservoir'] for row in evidence.report['cases']]
        evidence.check('nec_design_bound_refines', abs(maxima[2]-maxima[1]) < abs(maxima[1]-maxima[0]), maxima)
        evidence.report.update(current_rigid_shell_satisfies_surface_NEC_during_collision=False,
                               current_rigid_shell_is_self_sufficient_barotropic_matter=False,
                               nec_threshold_is_a_frozen_interior_diagnostic_not_a_derived_parameter=True,
                               same_source_condition_must_be_applied_to_MTS_and_GR_reference=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    run()
