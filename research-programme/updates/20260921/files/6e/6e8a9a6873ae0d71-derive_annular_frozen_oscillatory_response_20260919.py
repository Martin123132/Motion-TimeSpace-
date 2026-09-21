from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_frozen_forcing_time_envelope_20260919 import modal_setup,modal_state
from run_annular_P2_continuum_bridge_20260918 import checked_load
import contextlib
import json
import numpy as np


def phase_integral(frequency,time):
    return time*np.exp(.5j*frequency*time)*np.sinc(frequency*time/(2*np.pi))


def phase_bound(frequency,time):
    result = np.full_like(frequency,time,dtype=float)
    np.divide(2.,np.abs(frequency),out=result,where=frequency != 0.)
    return np.minimum(time,result)


def response_kernel(coupling,coarse,fine_frequency,time):
    difference = coarse['frequency'][None,:]-fine_frequency[:,None]
    negative_sum = -coarse['frequency'][None,:]-fine_frequency[:,None]
    coefficient = .5*(coarse['speed']+1j*coarse['frequency']*coarse['position'])
    response = np.exp(1j*fine_frequency*time)*np.sum(coupling*(
        coefficient[None,:]*phase_integral(difference,time)
        +coefficient.conj()[None,:]*phase_integral(negative_sum,time)),axis=1)
    envelope = np.sum(abs(coupling)*(.5*coarse['amplitude'])[None,:]*(
        phase_bound(difference,time)+phase_bound(negative_sum,time)),axis=1)
    return response,envelope


def main():
    evidence = EvidenceRun('annular-frozen-oscillatory-response-attempt01',__file__)
    try:
        evidence.report.update(github_action=False,subagents_used=False,no_new_live_evolution=True,
            frozen_quadratic_control_only=True,not_the_actual_moving_source_trajectory=True,
            all_modes_retained=True,no_fitted_frequency_filter=True,exact_resonance_not_divided_by_zero=True,
            floating_point_not_interval_certificate=True,full_live_P2_force_convergence_proven=False)
        evidence.report['samples'],evidence.report['fixtures'] = [],[]
        for frequency in [0.,1e-12,.7,30.]:
            time = .31
            integral = phase_integral(np.array([frequency]),time)[0]
            midpoint = (np.arange(4096)+.5)*time/4096
            quadrature = time*np.mean(np.exp(1j*frequency*midpoint))
            bound = phase_bound(np.array([frequency]),time)[0]
            evidence.check('phase_integral_'+str(frequency),abs(integral-quadrature) < 2e-7
                and abs(integral) <= bound+1e-14,
                dict(quadrature_error=float(abs(integral-quadrature)),bound=float(bound)))
            evidence.report['fixtures'].append(dict(frequency=frequency,time=time,
                integral_magnitude=float(abs(integral)),bound=float(bound),valid_for_claim=False))
        resonant = dict(frequency=np.array([2.]),speed=np.array([1.]),position=np.array([0.]),amplitude=np.array([1.]))
        response,envelope = response_kernel(np.ones((1,1)),resonant,np.array([2.]),.31)
        evidence.check('nonzero_resonant_forcing_has_finite_response',np.all(np.isfinite(response))
            and abs(response[0]) <= envelope[0]+1e-14)
        status_path = evidence.output.parent/'annular-frozen-forcing-time-envelope-attempt01/status.json'
        previous = json.loads(status_path.read_text())
        evidence.own(status_path)
        evidence.check('all_mode_time_envelope_complete',previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks']))
        for branch in ['reference','MTS']:
            matrices = checked_load(evidence,'annular-action-adjoint-stability-attempt01',branch+'_final-action-matrices.npz')
            direct = checked_load(evidence,'annular-direct-stiffness-forcing-attempt02',branch+'-1e-07-direct-forcing.npz')
            canonical = checked_load(evidence,'annular-live-compensated-rate-attempt01',branch+'-1e-07-compensated-rate.npz')
            control = checked_load(evidence,'annular-frozen-forcing-time-envelope-attempt01',branch+'-frozen-control.npz')
            center = (canonical['1_state'].shape[1]-1)//2
            coarse = modal_setup(matrices['coarse_mass'],matrices['coarse_stiffness'],direct['coarse_values'],direct['coarse_velocity'])
            fine = modal_setup(matrices['fine_mass'],matrices['fine_stiffness'],canonical['1_state'][0,center,:-1],
                canonical['1_full_direction'][0,center,:-1])
            interpolation = matrices['interpolation']
            projection = fine['modes'].T @ matrices['fine_mass']
            coupling = fine['modes'].T @ direct['total_mismatch'] @ coarse['modes']
            overlap = projection @ interpolation @ coarse['modes']
            spectral_coupling = (coarse['frequency'][None,:]**2-fine['frequency'][:,None]**2)*overlap
            relative_error = float(np.linalg.norm(coupling-spectral_coupling)/max(np.linalg.norm(coupling),1e-30))
            evidence.check(branch+'_spectral_mismatch_identity',relative_error < 2e-8,relative_error)
            coarse_initial,fine_initial = modal_state(coarse,0.),modal_state(fine,0.)
            initial_velocity = projection @ (fine_initial[1]-interpolation @ coarse_initial[1])
            initial_acceleration = projection @ (fine_initial[2]-interpolation @ coarse_initial[2])
            initial_complex = initial_acceleration+1j*fine['frequency']*initial_velocity
            initial_energy = .5*float(np.vdot(initial_complex,initial_complex).real)
            norm_errors = []
            sector = next(row for row in previous['cases'] if row['branch'] == branch and row['sector'] == 'total')
            forcing_envelope = min(sector['all_mode_block_bound'],sector['uniform_coarse_energy_bound'])
            response_vectors,envelope_vectors = [],[]
            for time in control['times']:
                response,envelope = response_kernel(coupling,coarse,fine['frequency'],time)
                predicted = np.exp(1j*fine['frequency']*time)*initial_complex+response
                coarse_state,fine_state = modal_state(coarse,time),modal_state(fine,time)
                velocity = projection @ (fine_state[1]-interpolation @ coarse_state[1])
                acceleration = projection @ (fine_state[2]-interpolation @ coarse_state[2])
                actual = acceleration+1j*fine['frequency']*velocity
                error = float(np.linalg.norm(predicted-actual))
                tolerance = 2e-6*max(float(np.linalg.norm(actual)),float(np.linalg.norm(initial_complex)),1e-12)+1e-11
                evidence.check(branch+'_'+str(time)+'_duhamel_matches_two_grid_propagation',error <= tolerance,
                    dict(error=error,tolerance=tolerance))
                evidence.check(branch+'_'+str(time)+'_component_response_envelope',
                    np.all(abs(response) <= envelope+1e-12*np.maximum(envelope,1e-15)))
                energy = .5*float(np.vdot(actual,actual).real)
                bound = .5*float(np.sum((abs(initial_complex)+envelope)**2))
                old_bound = .5*(np.sqrt(2*initial_energy)+time*forcing_envelope)**2
                evidence.check(branch+'_'+str(time)+'_oscillatory_energy_envelope',energy <= bound+1e-8*max(bound,initial_energy))
                old_sample = next(row for row in previous['energy_cases'] if row['branch'] == branch and row['frozen_time'] == time)
                evidence.check(branch+'_'+str(time)+'_same_control_energy',abs(energy-old_sample['energy']) < 1e-9*max(energy,initial_energy))
                evidence.report['samples'].append(dict(branch=branch,frozen_time=float(time),energy=energy,
                    oscillatory_energy_bound=bound,previous_force_envelope_bound=float(old_bound),
                    retained_energy_bound=float(min(bound,old_bound)),response_norm=float(np.linalg.norm(response)),
                    component_envelope_norm=float(np.linalg.norm(envelope)),duhamel_error=error,
                    numerical_tolerance=tolerance,valid_for_claim=False))
                norm_errors.append(error)
                response_vectors.append(response)
                envelope_vectors.append(envelope)
            final = evidence.report['samples'][-1]
            evidence.report['cases'].append(dict(branch=branch,coarse_modes=len(coarse['frequency']),fine_modes=len(fine['frequency']),
                spectral_identity_relative_error=relative_error,max_response_reconstruction_error=max(norm_errors),
                initial_energy=initial_energy,final_energy=final['energy'],
                final_oscillatory_energy_bound=final['oscillatory_energy_bound'],
                final_previous_energy_bound=final['previous_force_envelope_bound'],
                final_response_norm=final['response_norm'],final_response_envelope=final['component_envelope_norm'],
                applies_to_frozen_control_only=True,valid_for_claim=False))
            path = evidence.output/(branch+'-oscillatory-response.npz')
            np.savez_compressed(path,times=control['times'],coupling=coupling,overlap=overlap,
                coarse_frequencies=coarse['frequency'],fine_frequencies=fine['frequency'],
                initial_complex_error=initial_complex,responses=response_vectors,envelopes=envelope_vectors)
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
