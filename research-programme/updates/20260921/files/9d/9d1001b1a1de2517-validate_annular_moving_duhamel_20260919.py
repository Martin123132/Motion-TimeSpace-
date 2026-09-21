from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_moving_duhamel_20260919 import forced_linear_step,fixed_basis_remainder
from derive_annular_frozen_forcing_time_envelope_20260919 import modal_setup
from run_annular_P2_continuum_bridge_20260918 import checked_load
from scipy.linalg import cho_solve,cholesky
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-moving-duhamel-algebra-endpoint-attempt01',__file__)
    try:
        evidence.report.update(github_action=False,subagents_used=False,no_new_evolution=True,
            full_live_P2_force_convergence_proven=False,full_nonlinear_stability_proven=False,
            finite_probe_endpoint_checks_not_time_uniform_proof=True,all_source_residual_channels_retained=True)
        evidence.report['fixtures'] = []
        frequency = np.array([0.,1e-8,.4,15.,120.])
        step = .013
        position = np.array([.2,-.1,.5,.7,.3])
        velocity = np.array([.3,.1,-.2,.5,-.4])
        first = np.array([.8,.2,-.4,.3,.1])
        last = first+np.array([.2,-.1,.1,.4,-.2])*step
        actual = forced_linear_step(frequency,position,velocity,first,last,step)
        quadrature_times = (np.arange(32768)+.5)*step/32768
        remaining = step-quadrature_times[:,None]
        force = first[None,:]+quadrature_times[:,None]*(last-first)[None,:]/step
        expected_position = np.cos(frequency*step)*position+step*np.sinc(frequency*step/np.pi)*velocity
        expected_position += step*np.mean(remaining*np.sinc(frequency[None,:]*remaining/np.pi)*force,axis=0)
        expected_velocity = -frequency*np.sin(frequency*step)*position+np.cos(frequency*step)*velocity
        expected_velocity += step*np.mean(np.cos(frequency[None,:]*remaining)*force,axis=0)
        evidence.check('linear_ramp_all_frequencies_matches_independent_quadrature',
            max(np.max(abs(actual[0]-expected_position)),np.max(abs(actual[1]-expected_velocity))) < 2e-10)
        evidence.check('zero_frequency_polynomial_limit',abs(actual[0][0]-(position[0]+step*velocity[0]
            +.5*step**2*first[0]+step**2*(last[0]-first[0])/6)) < 1e-14)
        middle = (first+last)/2
        half = forced_linear_step(frequency,position,velocity,first,middle,step/2)
        halves = forced_linear_step(frequency,*half,middle,last,step/2)
        evidence.check('linear_force_subdivision_invariant',max(np.max(abs(actual[0]-halves[0])),
            np.max(abs(actual[1]-halves[1]))) < 2e-13)
        evidence.report['fixtures'].append(dict(kind='forced_ramp',position_error=float(np.max(abs(actual[0]-expected_position))),
            velocity_error=float(np.max(abs(actual[1]-expected_velocity))),valid_for_claim=False))
        random = np.random.default_rng(191730)
        for index in range(3):
            matrices = []
            for unused in range(4):
                raw = random.normal(size=(7,7))
                matrices.append(raw.T @ raw+np.eye(7))
            mass,stiffness,reference_mass,reference_stiffness = matrices
            raw = random.normal(size=(2,7,7))
            mass_rate,stiffness_rate = (raw+raw.transpose(0,2,1))/2
            displacement,velocity,acceleration,jerk = random.normal(size=(4,7))
            residual_rate = mass @ jerk+mass_rate @ acceleration+stiffness_rate @ displacement+stiffness @ velocity
            load,solved = fixed_basis_remainder(mass,stiffness,mass_rate,stiffness_rate,reference_mass,
                reference_stiffness,displacement,velocity,acceleration,residual_rate)
            evidence.check('noncommuting_fixed_basis_identity_'+str(index),np.max(abs(solved-jerk)) < 2e-13
                and np.max(abs(load-reference_mass @ jerk-reference_stiffness @ velocity)) < 2e-12)
            for name,missing in [('mass_rate',mass_rate @ acceleration),('stiffness_rate',stiffness_rate @ displacement)]:
                wrong,unused = fixed_basis_remainder(mass,stiffness,mass_rate,stiffness_rate,reference_mass,
                    reference_stiffness,displacement,velocity,acceleration,residual_rate+missing)
                evidence.check(name+'_omission_detected_'+str(index),np.linalg.norm(wrong-load) > .01)
            evidence.report['fixtures'].append(dict(kind='noncommuting_'+str(index),position_error=float(np.max(abs(solved-jerk))),
                velocity_error=float(np.max(abs(load-reference_mass @ jerk-reference_stiffness @ velocity))),valid_for_claim=False))
        for branch in ['reference','MTS']:
            matrices = checked_load(evidence,'annular-action-adjoint-stability-attempt01',branch+'_final-action-matrices.npz')
            canonical = checked_load(evidence,'annular-live-compensated-rate-attempt01',branch+'-1e-07-compensated-rate.npz')
            direct = checked_load(evidence,'annular-direct-stiffness-forcing-attempt02',branch+'-1e-07-direct-forcing.npz')
            center = (canonical['1_state'].shape[1]-1)//2
            mass,stiffness,interpolation = matrices['fine_mass'],matrices['fine_stiffness'],matrices['interpolation']
            modes = modal_setup(mass,stiffness,canonical['1_state'][0,center,:-1],canonical['1_full_direction'][0,center,:-1])
            projection = modes['modes'].T @ mass
            coarse_acceleration = -cho_solve((cholesky(matrices['coarse_mass'],lower=True),True),
                matrices['coarse_stiffness'] @ direct['coarse_values'])
            fine_acceleration = -cho_solve((cholesky(mass,lower=True),True),stiffness @ canonical['1_state'][0,center,:-1])
            frozen_difference = fine_acceleration-interpolation @ coarse_acceleration
            for step in [1e-7,5e-8]:
                saved = checked_load(evidence,'annular-differentiated-action-energy-attempt01',branch+'-'+str(step)+'-differentiated-energy.npz')
                load,jerk = fixed_basis_remainder(mass,stiffness,saved['mass_rate'],saved['stiffness_rate'],mass,stiffness,
                    saved['displacement'],saved['velocity'],saved['acceleration'],saved['residual_rate'])
                secular = modes['modes'].T @ direct['total_paired_velocity']
                channels = dict(nonstiffness_and_geometry_rate=modes['modes'].T @
                    (saved['residual_rate']-direct['total_paired_velocity']),
                    stiffness_transport=-modes['modes'].T @ saved['stiffness_rate'] @ saved['displacement'],
                    mass_transport=-modes['modes'].T @ saved['mass_rate'] @ saved['acceleration'])
                remainder = sum(channels.values())
                predicted = 1j*modes['frequency']*(projection @ saved['acceleration']
                    +1j*modes['frequency']*(projection @ saved['velocity']))+secular+remainder
                numerical_jerk = (saved['last_acceleration']-saved['first_acceleration'])/(2*step)
                fine_rate = (saved['1_after_flow'][0,center,:-1]-saved['1_before_flow'][0,center,:-1])/(2*step)
                coarse_rate = (saved['0_after_flow'][0,center,:-1]-saved['0_before_flow'][0,center,:-1])/(2*step)
                numerical = projection @ numerical_jerk+1j*modes['frequency']*(projection @ (fine_rate-interpolation @ coarse_rate))
                error = float(np.linalg.norm(predicted-numerical))
                tolerance = 2e-4*max(float(np.linalg.norm(predicted)),float(np.linalg.norm(numerical)),1e-8)+1e-8
                evidence.check(branch+'_'+str(step)+'_full_fixed_basis_derivative',error <= tolerance,dict(error=error,tolerance=tolerance))
                evidence.check(branch+'_'+str(step)+'_remainder_reconstructs_covector',
                    np.linalg.norm(modes['modes'].T @ load-secular-remainder) < 1e-8*max(np.linalg.norm(secular),1.))
                initial_gap = projection @ (saved['acceleration']-frozen_difference)
                energy_coordinate = projection @ saved['acceleration']+1j*modes['frequency']*(projection @ saved['velocity'])
                evidence.report['cases'].append(dict(branch=branch,probe_step=step,
                    full_frozen_basis_rhs_norm=float(np.linalg.norm(modes['modes'].T @ load)),
                    frozen_stiffness_forcing_norm=float(np.linalg.norm(secular)),remainder_norm=float(np.linalg.norm(remainder)),
                    nonstiffness_and_geometry_rate_norm=float(np.linalg.norm(channels['nonstiffness_and_geometry_rate'])),
                    stiffness_transport_norm=float(np.linalg.norm(channels['stiffness_transport'])),
                    mass_transport_norm=float(np.linalg.norm(channels['mass_transport'])),
                    initial_acceleration_gap_norm=float(np.linalg.norm(initial_gap)),
                    initial_live_energy=.5*float(np.vdot(energy_coordinate,energy_coordinate).real),
                    derivative_error=error,numerical_tolerance=tolerance,valid_for_claim=False))
                path = evidence.output/(branch+'-'+str(step)+'-remainder.npz')
                np.savez_compressed(path,remainder=remainder,initial_gap=initial_gap,energy_coordinate=energy_coordinate,
                    secular=secular,**channels)
                evidence.own(path,'outputs')
                evidence.save()
                print(json.dumps(evidence.report['cases'][-1]),flush=True)
        with (evidence.output/'completion.txt').open('w',encoding='utf-8') as stream,contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt','outputs')
        evidence.save()
        print(json.dumps(dict(state='complete',checks=len(evidence.report['checks']))),flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
