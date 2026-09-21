from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_moving_duhamel_20260919 import live_item,live_acceleration,moving_forcing,forced_linear_step
from derive_annular_frozen_forcing_time_envelope_20260919 import modal_setup,modal_state
from derive_annular_frozen_oscillatory_response_20260919 import response_kernel
from derive_annular_spatial_Gram_defect_split_20260919 import state_pair
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from annular_wave_error_energy_20260919 import stiffness_terms
from annular_P2_weighted_projection_bounds_20260919 import band_action
from run_annular_P2_continuum_bridge_20260918 import checked_load
from scipy.linalg import cholesky
from time import perf_counter
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-moving-duhamel-trajectory-attempt01',__file__)
    start = perf_counter()
    try:
        evidence.report.update(github_action=False,subagents_used=False,no_new_evolution=True,no_new_live_evolution=True,
            full_live_P2_force_convergence_proven=False,full_nonlinear_stability_proven=False,
            saved_trajectory_sampling_not_uniform_certificate=True,forcing_interpolation_not_actual_forcing=True,
            backward_time_from_previous_final_freeze=True,all_modes_retained=True,
            inverse_residual_and_action_reconstruction_defect_retained=True,
            temporal_integration_defect_not_assumed_zero=True,maximum_wall_seconds=10800)
        evidence.report['points'],evidence.report['channels'],evidence.report['reconstructions'],evidence.report['quadrature_comparisons'] = [],[],[],[]
        prerequisite = evidence.output.parent/'annular-moving-duhamel-algebra-endpoint-attempt01/status.json'
        status = json.loads(prerequisite.read_text())
        evidence.own(prerequisite)
        evidence.check('algebra_and_endpoint_complete',status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
        for branch in ['reference','MTS']:
            systems = [IndexedGradedP2System(257,branch == 'MTS',2e-5),IndexedGradedP2System(513,branch == 'MTS',1e-5)]
            center = int(np.argmin(abs(systems[0].labels)))
            initial_states = state_pair(evidence,branch,False)
            fine_folder = 'annular-P2-bulk513-MTS-time128-attempt01' if branch == 'MTS' else 'annular-P2-bulk513-evolution-reference-attempt01'
            fine_steps = 128 if branch == 'MTS' else 64
            saved_fine = checked_load(evidence,fine_folder,'trajectory-steps'+str(fine_steps)+'.npz')
            coarse_folder = 'annular-P2-evolved-source-halving-'+branch+'-attempt'+('02' if branch == 'MTS' else '01')
            matrices = checked_load(evidence,'annular-action-adjoint-stability-attempt01',branch+'_final-action-matrices.npz')
            frozen_source = checked_load(evidence,'annular-live-compensated-rate-attempt01',branch+'-1e-07-compensated-rate.npz')
            direct = checked_load(evidence,'annular-direct-stiffness-forcing-attempt02',branch+'-1e-07-direct-forcing.npz')
            masses = [matrices['coarse_mass'],matrices['fine_mass']]
            stiffnesses = [matrices['coarse_stiffness'],matrices['fine_stiffness']]
            lowers = [cholesky(mass,lower=True,check_finite=False) for mass in masses]
            modal = [modal_setup(masses[level],stiffnesses[level],frozen_source[str(level)+'_state'][0,center,:-1],
                -frozen_source[str(level)+'_full_direction'][0,center,:-1]) for level in range(2)]
            projections = [data['modes'].T @ mass for data,mass in zip(modal,masses)]
            interpolation = matrices['interpolation']
            overlap = projections[1] @ interpolation @ modal[0]['modes']
            coupling = modal[1]['modes'].T @ direct['total_mismatch'] @ modal[0]['modes']
            times = np.linspace(0.,4e-5,33)
            field_values,field_velocities,field_accelerations,modal_forces = [[],[]],[[],[]],[[],[]],[[],[]]
            for reverse_index,reverse_time in enumerate(times):
                if perf_counter()-start > 10800:
                    raise RuntimeError('Three-hour safe-save boundary; partial source evaluations preserved.')
                index = 32-reverse_index
                if index:
                    data = checked_load(evidence,coarse_folder,'steps32-accepted'+str(index).zfill(3)+'.npz')
                    coarse_state = data['state']
                    evidence.check(branch+'_'+str(index)+'_matching_saved_times',abs(float(data['time'])-(4e-5-reverse_time)) < 1e-17
                        and abs(saved_fine['times'][index*(fine_steps//32)]-float(data['time'])) < 1e-17)
                else:
                    coarse_state = initial_states[0]
                fine_state = saved_fine['states'][index*(fine_steps//32)]
                if not index:
                    evidence.check(branch+'_fine_initial_state_unchanged',np.array_equal(fine_state,initial_states[1]))
                arrays = dict(reverse_time=reverse_time,physical_time=4e-5-reverse_time)
                live_bases = []
                live_accelerations = []
                for level,(system,state) in enumerate(zip(systems,[coarse_state,fine_state])):
                    base = live_item(system,state,center)
                    base['center'] = center
                    base['flow'] = np.stack([base['all_rates'],system.forces(state[0],base['all_rates'],base['geometry'])])
                    acceleration = live_acceleration(system,state,center,base,5e-8)
                    error = float(np.max(abs(acceleration['acceleration']-acceleration['direct_acceleration'])))
                    tolerance = 2e-4*max(float(np.max(abs(acceleration['direct_acceleration']))),1e-8)+1e-8
                    tag = branch+'_'+str(reverse_index)+'_'+str(level)
                    evidence.check(tag+'_canonical_acceleration_control',error <= tolerance,dict(error=error,tolerance=tolerance))
                    half_error = 0.
                    if reverse_index in [0,16,32]:
                        halved = live_acceleration(system,state,center,base,2.5e-8)
                        half_error = float(np.max(abs(acceleration['acceleration']-halved['acceleration'])))
                        evidence.check(tag+'_acceleration_probe_halving',half_error <= tolerance,
                            dict(error=half_error,tolerance=tolerance))
                    force = moving_forcing(base,acceleration,lowers[level],stiffnesses[level])
                    error_force = float(np.linalg.norm(projections[level] @ (force['forcing']-force['direct'])))
                    scale_force = max(float(np.linalg.norm(projections[level] @ force['direct'])),1e-8)
                    evidence.check(tag+'_all_moving_action_loads_reconstruct',error_force <= 1e-7*scale_force+1e-10,
                        dict(error=error_force,scale=scale_force))
                    position,velocity,accel = base['values'][:-1],-base['rates'][:-1],acceleration['acceleration']
                    field_values[level].append(position.copy())
                    field_velocities[level].append(velocity.copy())
                    field_accelerations[level].append(accel.copy())
                    forcing = projections[level] @ force['forcing']
                    modal_forces[level].append(forcing)
                    for name,channel in force['channels'].items():
                        projected = projections[level] @ channel
                        evidence.report['channels'].append(dict(branch=branch,reverse_time=float(reverse_time),level=level,
                            channel=name,modal_force_norm=float(np.linalg.norm(projected)),valid_for_claim=False))
                        arrays[str(level)+'_'+name] = projected
                    evidence.report['points'].append(dict(branch=branch,reverse_time=float(reverse_time),physical_time=float(4e-5-reverse_time),
                        level=level,modal_force_norm=float(np.linalg.norm(forcing)),source_acceleration=float(acceleration['source_acceleration']),
                        acceleration_control_error=error,acceleration_control_tolerance=tolerance,
                        probe_halving_performed=reverse_index in [0,16,32],probe_halving_error=half_error,
                        forcing_reconstruction_error=error_force,valid_for_claim=False))
                    arrays.update({str(level)+'_'+name:value for name,value in dict(position=position,reverse_velocity=velocity,
                        acceleration=accel,modal_force=forcing,mass_rate=acceleration['mass_rate'],
                        cross_rate=acceleration['cross_rate'],inverse_residual_rate=acceleration['inverse_residual_rate'],
                        mass_bands=base['data']['mass_bands'],gradient_weights=base['weights']['gradient'],
                        gram_weights=base['weights']['gram']).items()})
                    live_bases.append(base)
                    live_accelerations.append(acceleration)
                difference = field_velocities[1][-1]-interpolation @ field_velocities[0][-1]
                difference_accel = field_accelerations[1][-1]-interpolation @ field_accelerations[0][-1]
                current_energy = .5*float(difference_accel @ band_action(live_bases[1]['data']['mass_bands'],difference_accel))
                current_energy += sum(stiffness_terms(live_bases[1]['layer'],live_bases[1]['weights'],difference)[name]
                    for name in ['gradient_energy','gram_energy'])
                arrays['current_metric_energy'] = current_energy
                path = evidence.output/(branch+'-point'+str(reverse_index).zfill(3)+'.npz')
                np.savez_compressed(path,**arrays)
                evidence.own(path,'outputs')
                evidence.report['progress'] = dict(branch=branch,completed_points=reverse_index+1,total_points=33)
                evidence.save()
                if reverse_index % 4 == 0:
                    print(json.dumps(dict(branch=branch,point=reverse_index,wall_seconds=perf_counter()-start)),flush=True)
            field_values = [np.asarray(values) for values in field_values]
            field_velocities = [np.asarray(values) for values in field_velocities]
            field_accelerations = [np.asarray(values) for values in field_accelerations]
            modal_forces = [np.asarray(values) for values in modal_forces]
            frozen_initial = [modal_state(data,0.) for data in modal]
            initial_z = projections[1] @ (frozen_initial[1][2]-interpolation @ frozen_initial[0][2])
            initial_z = initial_z+1j*modal[1]['frequency']*(projections[1] @ (frozen_initial[1][1]-interpolation @ frozen_initial[0][1]))
            results_by_stride = {}
            for stride in [4,2,1]:
                positions = [np.zeros(len(data['frequency'])) for data in modal]
                velocities = [np.zeros(len(data['frequency'])) for data in modal]
                selected = list(range(0,33,stride))
                results_by_stride[stride] = {}
                for local,index in enumerate(selected):
                    time = times[index]
                    if local:
                        before = selected[local-1]
                        for level in range(2):
                            positions[level],velocities[level] = forced_linear_step(modal[level]['frequency'],positions[level],velocities[level],
                                modal_forces[level][before],modal_forces[level][index],time-times[before])
                    correction_accel = [modal_forces[level][index]-modal[level]['frequency']**2*positions[level] for level in range(2)]
                    correction = correction_accel[1]-overlap @ correction_accel[0]
                    correction = correction+1j*modal[1]['frequency']*(velocities[1]-overlap @ velocities[0])
                    frozen = [modal_state(data,time) for data in modal]
                    frozen_z = projections[1] @ (frozen[1][2]-interpolation @ frozen[0][2])
                    frozen_z = frozen_z+1j*modal[1]['frequency']*(projections[1] @ (frozen[1][1]-interpolation @ frozen[0][1]))
                    actual_z = projections[1] @ (field_accelerations[1][index]-interpolation @ field_accelerations[0][index])
                    actual_z = actual_z+1j*modal[1]['frequency']*(projections[1] @ (field_velocities[1][index]-interpolation @ field_velocities[0][index]))
                    predicted = frozen_z+correction
                    response,envelope = response_kernel(coupling,modal[0],modal[1]['frequency'],time)
                    evidence.check(branch+'_'+str(stride)+'_'+str(index)+'_reverse_frozen_identity',
                        np.linalg.norm(frozen_z-np.exp(1j*modal[1]['frequency']*time)*initial_z-response)
                        < 2e-6*max(np.linalg.norm(frozen_z),np.linalg.norm(initial_z),1e-12)+1e-11)
                    component_bound = abs(initial_z)+envelope+abs(correction)
                    conditional_bound = .5*float(np.sum(component_bound**2))
                    actual_energy = .5*float(np.vdot(actual_z,actual_z).real)
                    discrepancy = float(np.linalg.norm(actual_z-predicted))
                    interpolation_correction = float(np.linalg.norm(correction))
                    frozen_energy = .5*float(np.vdot(frozen_z,frozen_z).real)
                    row = dict(branch=branch,grid_points=len(selected),reverse_time=float(time),physical_time=float(4e-5-time),
                        actual_fixed_metric_energy=actual_energy,frozen_energy=frozen_energy,
                        reconstructed_energy=.5*float(np.vdot(predicted,predicted).real),
                        frozen_analytic_energy_envelope=.5*float(np.sum((abs(initial_z)+envelope)**2)),
                        conditional_energy_bound_without_unresolved_error=conditional_bound,
                        predicted_correction_norm=interpolation_correction,
                        observed_correction_norm=float(np.linalg.norm(actual_z-frozen_z)),
                        unresolved_response_norm=discrepancy,
                        sample_inside_conditional_bound=bool(actual_energy <= conditional_bound),
                        valid_for_claim=False)
                    evidence.report['reconstructions'].append(row)
                    results_by_stride[stride][index] = dict(correction=correction,predicted=predicted,actual=actual_z,row=row)
                path = evidence.output/(branch+'-reconstruction-grid'+str(len(selected))+'.npz')
                np.savez_compressed(path,times=times[selected],corrections=[results_by_stride[stride][index]['correction'] for index in selected],
                    predicted=[results_by_stride[stride][index]['predicted'] for index in selected],
                    actual=[results_by_stride[stride][index]['actual'] for index in selected])
                evidence.own(path,'outputs')
            for index in range(0,33,4):
                coarse = np.linalg.norm(results_by_stride[4][index]['correction']-results_by_stride[2][index]['correction'])
                fine = np.linalg.norm(results_by_stride[2][index]['correction']-results_by_stride[1][index]['correction'])
                evidence.report['quadrature_comparisons'].append(dict(branch=branch,reverse_time=float(times[index]),
                    grid9_to17=float(coarse),grid17_to33=float(fine),valid_for_claim=False))
            rows = [value['row'] for value in results_by_stride[1].values()]
            final = rows[-1]
            evidence.report['cases'].append(dict(branch=branch,physical_interval_start=0.,physical_interval_end=4e-5,
                reconstruction_grid_points=33,initial_acceleration_gap_norm=rows[0]['observed_correction_norm'],
                final_actual_energy=final['actual_fixed_metric_energy'],final_frozen_energy=final['frozen_energy'],
                final_reconstructed_energy=final['reconstructed_energy'],
                final_frozen_envelope=final['frozen_analytic_energy_envelope'],
                final_conditional_bound=final['conditional_energy_bound_without_unresolved_error'],
                final_predicted_correction_norm=final['predicted_correction_norm'],
                final_observed_correction_norm=final['observed_correction_norm'],final_unresolved_response_norm=final['unresolved_response_norm'],
                maximum_unresolved_response_norm=max(row['unresolved_response_norm'] for row in rows),
                samples_inside_conditional_bound=sum(row['sample_inside_conditional_bound'] for row in rows),
                certified_continuous_time_envelope=False,valid_for_claim=False))
            evidence.save()
            print(json.dumps(evidence.report['cases'][-1]),flush=True)
        with (evidence.output/'completion.txt').open('w',encoding='utf-8') as stream,contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt','outputs')
        evidence.save()
        print(json.dumps(dict(state='complete',checks=len(evidence.report['checks']),wall_seconds=perf_counter()-start)),flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
