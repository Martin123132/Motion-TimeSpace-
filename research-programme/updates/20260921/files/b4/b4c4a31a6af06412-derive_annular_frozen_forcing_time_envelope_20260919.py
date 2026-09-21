from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_direct_stiffness_forcing_20260919 import dual_norm
from run_annular_P2_continuum_bridge_20260918 import checked_load
from scipy.linalg import eigh,cholesky,cho_solve,solve_triangular
import contextlib
import json
import numpy as np


def modal_setup(mass,stiffness,values,velocity):
    eigenvalues,modes = eigh(stiffness,mass,check_finite=False)
    if np.any(eigenvalues <= 0.):
        raise ValueError('Frozen homogeneous scalar control needs a positive complete pencil.')
    frequency = np.sqrt(eigenvalues)
    position = modes.T @ mass @ values
    speed = modes.T @ mass @ velocity
    residual = stiffness @ modes-(mass @ modes)*eigenvalues[None,:]
    backward = float(np.max(np.linalg.norm(residual,axis=0)/
        ((np.linalg.norm(stiffness)+eigenvalues*np.linalg.norm(mass))*np.linalg.norm(modes,axis=0))))
    orthogonality = float(np.max(abs(modes.T @ mass @ modes-np.eye(len(eigenvalues)))))
    return dict(frequency=frequency,modes=modes,position=position,speed=speed,
        amplitude=np.hypot(speed,frequency*position),backward_residual=backward,orthogonality_error=orthogonality)


def modal_state(data,time):
    frequency,position,speed = data['frequency'],data['position'],data['speed']
    cosine,sine = np.cos(frequency*time),np.sin(frequency*time)
    moved_position = position*cosine+speed*sine/frequency
    moved_speed = speed*cosine-frequency*position*sine
    return (data['modes'] @ moved_position,data['modes'] @ moved_speed,
        data['modes'] @ (-frequency**2*moved_position))


def main():
    evidence = EvidenceRun('annular-frozen-forcing-time-envelope-attempt01',__file__)
    try:
        evidence.report.update(github_action=False,subagents_used=False,no_new_evolution=False,no_new_live_evolution=True,
            frozen_quadratic_control_only=True,not_the_actual_moving_source_trajectory=True,
            frozen_source_position_and_zero_source_velocity_in_control=True,
            full_live_P2_force_convergence_proven=False,uniform_evolving_refinement_rate_proven=False,
            all_modes_retained=True,no_fitted_frequency_filter=True,block_size_chosen_before_results=16,
            ideal_arithmetic_time_inequality_not_interval_numeric_certificate=True)
        evidence.report['samples'],evidence.report['energy_cases'],evidence.report['blocks'] = [],[],[]
        status_path = evidence.output.parent/'annular-direct-stiffness-forcing-attempt02/status.json'
        previous = json.loads(status_path.read_text())
        evidence.own(status_path)
        evidence.check('direct_stiffness_forcing_complete',previous['state'] == 'complete' and all(row['passed'] for row in previous['checks']))
        for branch in ['reference','MTS']:
            matrices = checked_load(evidence,'annular-action-adjoint-stability-attempt01',branch+'_final-action-matrices.npz')
            saved = checked_load(evidence,'annular-direct-stiffness-forcing-attempt02',branch+'-1e-07-direct-forcing.npz')
            canonical = checked_load(evidence,'annular-live-compensated-rate-attempt01',branch+'-1e-07-compensated-rate.npz')
            center = (canonical['1_state'].shape[1]-1)//2
            values = [saved['coarse_values'],canonical['1_state'][0,center,:-1]]
            velocities = [saved['coarse_velocity'],canonical['1_full_direction'][0,center,:-1]]
            masses = [matrices['coarse_mass'],matrices['fine_mass']]
            stiffnesses = [matrices['coarse_stiffness'],matrices['fine_stiffness']]
            modes = [modal_setup(mass,stiffness,position,speed) for mass,stiffness,position,speed in zip(masses,stiffnesses,values,velocities)]
            mass_lower = cholesky(masses[1],lower=True,check_finite=False)
            interpolation = matrices['interpolation']
            for level,data in enumerate(modes):
                evidence.check(branch+'_'+str(level)+'_complete_eigensystem',data['modes'].shape == masses[level].shape
                    and data['backward_residual'] < 2e-12 and data['orthogonality_error'] < 2e-10,
                    dict(backward=data['backward_residual'],orthogonality=data['orthogonality_error']))
                reconstructed = modal_state(data,0.)
                evidence.check(branch+'_'+str(level)+'_initial_fields_recovered',np.max(abs(reconstructed[0]-values[level])) < 1e-11
                    and np.max(abs(reconstructed[1]-velocities[level])) < 1e-11)
            envelopes = {}
            coarse_amplitude = modes[0]['amplitude']
            coarse_higher_energy = .5*float(np.sum((modes[0]['frequency']*coarse_amplitude)**2))
            for sector in ['gradient','gram','total']:
                mismatch = saved[sector+'_mismatch']
                images = solve_triangular(mass_lower,mismatch @ modes[0]['modes'],lower=True,check_finite=False)
                columns = images*coarse_amplitude[None,:]
                triangle = float(np.sum(np.linalg.norm(columns,axis=0)))
                block_bound = 0.
                covered = 0
                for start in range(0,len(coarse_amplitude),16):
                    stop = min(start+16,len(coarse_amplitude))
                    block = columns[:,start:stop]
                    gram = block.T @ block
                    largest = float(np.linalg.eigvalsh((gram+gram.T)/2)[-1])
                    local_triangle = float(np.sum(np.linalg.norm(block,axis=0)))
                    local_spectral = float(np.sqrt(max(largest,0.)*(stop-start)))
                    contribution = min(local_triangle,local_spectral)
                    block_bound += contribution
                    covered += stop-start
                    evidence.report['blocks'].append(dict(branch=branch,sector=sector,first_mode=start,last_mode=stop-1,
                        mode_count=stop-start,triangle_bound=local_triangle,spectral_box_bound=local_spectral,
                        retained_bound=contribution,valid_for_claim=False))
                evidence.check(branch+'_'+sector+'_all_modes_and_block_bound',covered == len(coarse_amplitude)
                    and block_bound <= triangle+1e-10*max(triangle,1e-20))
                old = next(row for row in previous['cases'] if row['branch'] == branch and row['sector'] == sector and row['probe_step'] == 1e-7)
                energy_bound = float(old['velocity_constant_upper']*np.sqrt(2*coarse_higher_energy))
                initial_norm = dual_norm(mass_lower,mismatch @ velocities[0])
                evidence.check(branch+'_'+sector+'_initial_forcing_matches_saved',abs(initial_norm-old['paired_velocity_dual_norm']) <= 1e-9*max(initial_norm,1e-10)+1e-10)
                evidence.report['cases'].append(dict(branch=branch,sector=sector,mode_count=covered,
                    initial_forcing_norm=initial_norm,all_mode_triangle_bound=triangle,all_mode_block_bound=float(block_bound),
                    uniform_coarse_energy_bound=energy_bound,coarse_higher_energy=coarse_higher_energy,
                    applies_to_frozen_control_only=True,valid_for_claim=False))
                envelopes[sector] = min(block_bound,energy_bound)
            initial = [modal_state(data,0.) for data in modes]
            initial_difference = initial[1][1]-interpolation @ initial[0][1]
            initial_acceleration = initial[1][2]-interpolation @ initial[0][2]
            initial_energy = .5*float(initial_acceleration @ masses[1] @ initial_acceleration
                +initial_difference @ stiffnesses[1] @ initial_difference)
            first_times = np.linspace(0.,4e-5,41)
            positions,velocities_out,accelerations = [],[],[]
            for time in first_times:
                state = [modal_state(data,time) for data in modes]
                difference = state[1][1]-interpolation @ state[0][1]
                acceleration = state[1][2]-interpolation @ state[0][2]
                energy = .5*float(acceleration @ masses[1] @ acceleration+difference @ stiffnesses[1] @ difference)
                energy_bound = .5*(np.sqrt(2*initial_energy)+time*envelopes['total'])**2
                evidence.check(branch+'_'+str(time)+'_frozen_differentiated_error_energy_bound',energy <= energy_bound+1e-8*max(energy_bound,initial_energy,1e-20))
                evidence.report['energy_cases'].append(dict(branch=branch,frozen_time=float(time),energy=energy,
                    initial_energy=initial_energy,analytic_time_bound=float(energy_bound),valid_for_claim=False))
                for sector in ['gradient','gram','total']:
                    forcing = saved[sector+'_mismatch'] @ state[0][1]
                    norm = dual_norm(mass_lower,forcing)
                    evidence.check(branch+'_'+str(time)+'_'+sector+'_uniform_envelope',norm <= envelopes[sector]+1e-8*max(envelopes[sector],1e-20))
                    evidence.report['samples'].append(dict(branch=branch,sector=sector,frozen_time=float(time),forcing_norm=norm,
                        analytic_envelope=envelopes[sector],valid_for_claim=False))
                positions.append(state[0][0])
                velocities_out.append(state[0][1])
                accelerations.append(state[0][2])
            path = evidence.output/(branch+'-frozen-control.npz')
            np.savez_compressed(path,times=first_times,coarse_positions=positions,coarse_velocities=velocities_out,
                coarse_accelerations=accelerations,coarse_frequencies=modes[0]['frequency'],fine_frequencies=modes[1]['frequency'],
                coarse_modal_amplitudes=coarse_amplitude)
            evidence.own(path,'outputs')
            evidence.save()
            print(json.dumps(dict(branch=branch,initial_error_energy=initial_energy,final=evidence.report['energy_cases'][-1],
                bounds=[row for row in evidence.report['cases'] if row['branch'] == branch])),flush=True)
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
