import os
for name in ['OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS']:
    os.environ[name] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
from navier_stokes_source_audit_20260908 import limit_process
limit_process()

import json
import numpy as np
from scipy.integrate import quad, solve_ivp
from annular_reference_continuum_shell_20260914 import EvidenceRun
from annular_dynamical_source_20260914 import outgoing_profile, flat_mirror_rhs


def incident_energy(retarded_time, amplitude):
    upper = min(float(retarded_time), -5.2)
    if upper <= -5.8:
        return 0.
    return quad(lambda value: float(outgoing_profile(value, amplitude)[1])**2, -5.8, upper,
                epsabs=2e-14, epsrel=2e-12, limit=150)[0]


def run():
    evidence = EvidenceRun('annular-exact-flat-recoil-attempt01', __file__)
    try:
        evidence.report.update(scope='Nonlinear spherical scalar and freely recoiling dust shell in G=0 Minkowski space, before any reflected pulse returns to the centre.',
                               production_GR_pulse_reused=False, scalar_profile_is_new_declared_control=True,
                               coupled_moving_GR_scalar_PDE_tested=False, parent_reflectivity_derived=False,
                               energy_is_angular_reduced=True, reservoir=.003,
                               radial_impulse_is_not_total_Cartesian_momentum=True)
        reservoir = .003
        for amplitude in [.005, .01, .02]:
            total_incident = incident_energy(-5.2, amplitude)
            exact_factor = 1+2*total_incident/reservoir
            exact_reflected = reservoir/2*(1-1/exact_factor)
            exact_mirror_gain = reservoir/2*(exact_factor+1/exact_factor-2)
            final_advanced = 6+quad(lambda retarded: (1+2*incident_energy(retarded, amplitude)/reservoir)**2,
                                   -6., -5.2, epsabs=2e-11, epsrel=2e-11, points=[-5.8], limit=150)[0]
            exact_time = (final_advanced-5.2)/2
            exact_radius = (final_advanced+5.2)/2
            def pulse_complete(time, state):
                return time-state[0]+5.2
            pulse_complete.terminal = True
            pulse_complete.direction = 1
            evidence.check(str(amplitude)+'_no_centre_return_in_exact_time', exact_time < 6.2)
            result = solve_ivp(flat_mirror_rhs(reservoir, amplitude), (0., 6.1), [6., 0., 0., 0.],
                               method='DOP853', rtol=2e-11, atol=2e-13, max_step=.002,
                               t_eval=np.arange(0., 6.1001, .01), events=pulse_complete)
            evidence.check(str(amplitude)+'_pulse_finished', result.success and len(result.t_events[0]) == 1)
            final_time = float(result.t_events[0][0])
            final_state = result.y_events[0][0]
            times = np.concatenate([result.t, [final_time]])
            states = np.vstack([result.y.T, final_state])
            radius, rapidity, arrived, reflected = states.T
            factor = np.exp(rapidity)
            mirror_energy = reservoir*np.cosh(rapidity)
            mirror_impulse = reservoir*np.sinh(rapidity)
            energy_defect = mirror_energy-reservoir-arrived+reflected
            impulse_defect = mirror_impulse-arrived-reflected
            total_energy = total_incident-arrived+reflected+mirror_energy
            independent_arrival = np.array([incident_energy(time-position, amplitude) for time, position in zip(times, radius)])
            exact_factor_profile = 1+2*independent_arrival/reservoir
            evidence.check(str(amplitude)+'_timelike_outward_response', np.max(np.tanh(rapidity)) < 1 and rapidity[-1] > .01 and np.min(rapidity) >= -1e-13)
            evidence.check(str(amplitude)+'_entire_energy_ledger', max(abs(energy_defect)) < 2e-11 and max(abs(total_energy-total_incident-reservoir)) < 2e-11,
                           float(max(abs(energy_defect))))
            evidence.check(str(amplitude)+'_radial_null_mode_impulse_identity', max(abs(impulse_defect)) < 2e-11, float(max(abs(impulse_defect))))
            evidence.check(str(amplitude)+'_independent_characteristic_rapidity', max(abs(factor-exact_factor_profile)) < 2e-8, float(max(abs(factor-exact_factor_profile))))
            evidence.check(str(amplitude)+'_independent_incident_quadrature', max(abs(arrived-independent_arrival)) < 2e-11, float(max(abs(arrived-independent_arrival))))
            event_error = max(abs(final_time-exact_time), abs(final_state[0]-exact_radius))
            evidence.check(str(amplitude)+'_independent_null_coordinate_trajectory', event_error < 2e-8, event_error)
            evidence.check(str(amplitude)+'_final_reflection_and_recoil_energy', abs(final_state[3]-exact_reflected) < 2e-11 and
                           abs(reservoir*(np.cosh(final_state[1])-1)-exact_mirror_gain) < 2e-11)
            evidence.check(str(amplitude)+'_old_reflection_plus_recoil_is_inconsistent', exact_mirror_gain > 1e-8)
            retarded = times-radius
            advanced = times+radius
            profile, profile_rate = outgoing_profile(retarded, amplitude)
            reflected_profile_rate = -profile_rate/factor**2
            gradient = (-profile_rate+reflected_profile_rate)/radius
            time_derivative = (profile_rate+reflected_profile_rate)/radius
            comoving = np.cosh(rapidity)*time_derivative+np.sinh(rapidity)*gradient
            normal = np.sinh(rapidity)*time_derivative+np.cosh(rapidity)*gradient
            expected_normal = -2*profile_rate/(radius*factor)
            evidence.check(str(amplitude)+'_full_wave_boundary_and_normal_derivative', max(abs(comoving)) < 1e-13 and max(abs(normal-expected_normal)) < 1e-13)
            evidence.check(str(amplitude)+'_monotone_null_coordinate_map', np.all(np.diff(retarded) > 0) and np.all(np.diff(advanced) > 0))
            output = evidence.output/('amplitude_'+str(amplitude)+'.npz')
            np.savez_compressed(output, times=times, states=states, retarded=retarded, advanced=advanced,
                                incoming_profile=profile, reflected_profile=-profile,
                                reflected_profile_derivative=reflected_profile_rate, total_energy=total_energy,
                                independent_arrived_energy=independent_arrival, normal_pressure=.5*normal**2)
            evidence.own(output, 'outputs')
            row = dict(amplitude=amplitude, reservoir=reservoir, incident_energy=total_incident,
                       final_time=final_time, final_radius=float(final_state[0]),
                       final_speed=float(np.tanh(final_state[1])), reflected_energy=exact_reflected,
                       shell_kinetic_energy=exact_mirror_gain, fraction_to_recoil=exact_mirror_gain/total_incident,
                       maximum_energy_defect=float(max(abs(energy_defect))), characteristic_trajectory_error=event_error)
            evidence.report['cases'].append(row)
            evidence.save()
            print(row, flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    run()
