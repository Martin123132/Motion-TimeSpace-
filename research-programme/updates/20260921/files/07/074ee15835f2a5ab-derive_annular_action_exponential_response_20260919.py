from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_action_exponential_20260919 import FactoredAction,propagate
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from derive_annular_moving_Gram_profile_20260919 import evaluate_pair
from run_annular_P2_continuum_bridge_20260918 import checked_load
from scipy.sparse import csr_matrix
from time import perf_counter
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-action-exponential-response-attempt01',__file__)
    start = perf_counter()
    try:
        evidence.report.update(github_action=False,subagents_used=False,no_new_evolution=True,no_new_live_evolution=True,
            frozen_forcing_reconstruction_only=True,all_action_rows_retained=True,
            no_modal_eigenvectors_or_frequencies_used=True,original_action_and_source_unchanged=True,
            full_live_P2_force_convergence_proven=False,certified_continuous_time_bound=False,
            exponential_scaling_is_coordinate_only=1e6,maximum_wall_seconds=10800)
        evidence.report['points'],evidence.report['sampling'],evidence.report['controls'] = [],[],[]
        for name in ['annular-action-exponential-algebra-attempt01','annular-moving-duhamel-trajectory-attempt01',
                'annular-moving-duhamel-modal-arithmetic-attempt01']:
            path = evidence.output.parent/name/'status.json'
            status = json.loads(path.read_text())
            evidence.own(path)
            evidence.check(name+'_complete',status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
            if name == 'annular-moving-duhamel-modal-arithmetic-attempt01':
                previous = status
        for branch in ['reference','MTS']:
            canonical = checked_load(evidence,'annular-live-compensated-rate-attempt01',branch+'-1e-07-compensated-rate.npz')
            matrices = checked_load(evidence,'annular-action-adjoint-stability-attempt01',branch+'_final-action-matrices.npz')
            systems = [IndexedGradedP2System(257,branch == 'MTS',2e-5),IndexedGradedP2System(513,branch == 'MTS',1e-5)]
            pair = evaluate_pair(systems,[canonical[str(level)+'_state'] for level in range(2)])
            points = [checked_load(evidence,'annular-moving-duhamel-trajectory-attempt01',branch+'-point'+str(index).zfill(3)+'.npz')
                for index in range(33)]
            actions,forces = [],[]
            for level,(item,name) in enumerate(zip(pair,['coarse','fine'])):
                layer = item['layer']
                gradient = csr_matrix((layer.reference_radial.ravel(),(np.repeat(np.arange(len(layer.reference_indices)),3),
                    layer.reference_indices.ravel())),shape=(len(layer.reference_indices),layer.count))
                gram = layer.lifted.tocsr()
                initial = points[0]
                action = FactoredAction(initial[str(level)+'_mass_bands'],gradient,initial[str(level)+'_gradient_weights'],
                    gram,initial[str(level)+'_gram_weights'])
                actions.append(action)
                test = np.column_stack([initial[str(level)+'_position'],initial[str(level)+'_reverse_velocity'],
                    np.sin(np.arange(layer.count)*.37)])
                factored = action.stiffness(test)
                assembled = matrices[name+'_stiffness'] @ test
                error = float(np.max(abs(factored-assembled)))
                tolerance = 2e-11*max(float(np.max(abs(factored))),1.)+1e-13
                evidence.check(branch+'_'+name+'_factored_action_matches_original',error <= tolerance,dict(error=error,tolerance=tolerance))
                evidence.check(branch+'_'+name+'_banded_mass_inverse',np.max(abs(action.mass(action.solve_mass(test))-test)) < 2e-12)
                forcing = np.array([point[str(level)+'_acceleration']+action.acceleration_operator(point[str(level)+'_position']) for point in points])
                forces.append(forcing)
                arrays = dict(mass_bands=action.mass_bands,gradient_data=gradient.data,gradient_indices=gradient.indices,
                    gradient_indptr=gradient.indptr,gradient_shape=gradient.shape,gradient_weights=action.gradient_weights,
                    gram_data=gram.data,gram_indices=gram.indices,gram_indptr=gram.indptr,gram_shape=gram.shape,
                    gram_weights=action.gram_weights,physical_forcing=forcing)
                path = evidence.output/(branch+'-'+name+'-action.npz')
                np.savez_compressed(path,**arrays)
                evidence.own(path,'outputs')
            interpolation = matrices['interpolation']
            times = np.array([point['reverse_time'] for point in points])
            results = {}
            for stride in [4,2,1]:
                selected = list(range(0,33,stride))
                velocities,accelerations,initial_energies = [],[],[]
                for level,action in enumerate(actions):
                    initial = points[0]
                    velocity = initial[str(level)+'_reverse_velocity']
                    free_acceleration = -action.acceleration_operator(initial[str(level)+'_position'])
                    velocities.append(np.column_stack([velocity,velocity]))
                    accelerations.append(np.column_stack([initial[str(level)+'_acceleration'],free_acceleration]))
                    initial_energies.append(action.energy(velocity,free_acceleration))
                results[stride] = {}
                cumulative_products = 0
                for local,index in enumerate(selected):
                    if perf_counter()-start > 10800:
                        raise RuntimeError('Three-hour safe-save boundary reached.')
                    if local:
                        before = selected[local-1]
                        step = times[index]-times[before]
                        for level,action in enumerate(actions):
                            slope = (forces[level][index]-forces[level][before])/step
                            old_velocity,old_acceleration = velocities[level],accelerations[level]
                            moved = propagate(action,old_velocity,old_acceleration,slope,step,np.array([1.,0.]))
                            velocities[level],accelerations[level] = moved['velocity'],moved['acceleration']
                            cumulative_products += moved['operator_vector_products']
                            evidence.check(branch+'_'+str(stride)+'_'+str(index)+'_'+str(level)+'_constant_coordinate_preserved',
                                np.max(abs(moved['constants']-np.array([1.,0.]))) < 1e-13)
                            if local == 1:
                                half = propagate(action,old_velocity,old_acceleration,slope,step/2,np.array([1.,0.]))
                                halves = propagate(action,half['velocity'],half['acceleration'],slope,step/2,np.array([1.,0.]))
                                rescaled = propagate(action,old_velocity,old_acceleration,slope,step,np.array([1.,0.]),scale=5e5)
                                half_error = action.energy_norm(moved['velocity'][:,0]-halves['velocity'][:,0],moved['acceleration'][:,0]-halves['acceleration'][:,0])
                                scale_error = action.energy_norm(moved['velocity'][:,0]-rescaled['velocity'][:,0],moved['acceleration'][:,0]-rescaled['acceleration'][:,0])
                                control_tolerance = 2e-10*max(action.energy_norm(old_velocity[:,0],old_acceleration[:,0]),1e-8)+1e-12
                                evidence.check(branch+'_'+str(stride)+'_'+str(level)+'_halfstep_and_rescaling',
                                    half_error <= control_tolerance and scale_error <= control_tolerance,
                                    dict(half_error=half_error,scale_error=scale_error,tolerance=control_tolerance))
                                evidence.report['controls'].append(dict(branch=branch,grid_points=len(selected),level=level,
                                    halfstep_error=half_error,coordinate_scaling_error=scale_error,numerical_tolerance=control_tolerance,valid_for_claim=False))
                    actual_velocity = points[index]['1_reverse_velocity']-interpolation @ points[index]['0_reverse_velocity']
                    actual_acceleration = points[index]['1_acceleration']-interpolation @ points[index]['0_acceleration']
                    predicted_velocity = velocities[1][:,0]-interpolation @ velocities[0][:,0]
                    predicted_acceleration = accelerations[1][:,0]-interpolation @ accelerations[0][:,0]
                    free_velocity = velocities[1][:,1]-interpolation @ velocities[0][:,1]
                    free_acceleration = accelerations[1][:,1]-interpolation @ accelerations[0][:,1]
                    error = actions[1].energy_norm(predicted_velocity-actual_velocity,predicted_acceleration-actual_acceleration)
                    drift = [abs(action.energy(velocities[level][:,1],accelerations[level][:,1])-initial_energies[level])
                        /max(initial_energies[level],1e-30) for level,action in enumerate(actions)]
                    evidence.check(branch+'_'+str(stride)+'_'+str(index)+'_homogeneous_energy_conservation',max(drift) < 2e-9,
                        dict(coarse=drift[0],fine=drift[1]))
                    old = next(row for row in previous['reconstructions'] if row['branch'] == branch
                        and row['grid_points'] == len(selected) and row['reverse_time'] == times[index])
                    row = dict(branch=branch,grid_points=len(selected),reverse_time=float(times[index]),
                        action_response_error_norm=error,previous_modal_error_norm=old['arithmetic_corrected_unresolved_norm'],
                        actual_action_energy=actions[1].energy(actual_velocity,actual_acceleration),
                        reconstructed_action_energy=actions[1].energy(predicted_velocity,predicted_acceleration),
                        frozen_action_energy=actions[1].energy(free_velocity,free_acceleration),
                        source_response_norm=actions[1].energy_norm(predicted_velocity-free_velocity,predicted_acceleration-free_acceleration),
                        max_homogeneous_energy_relative_drift=max(drift),operator_vector_products=cumulative_products,valid_for_claim=False)
                    evidence.report['points'].append(row)
                    results[stride][index] = dict(velocity=predicted_velocity,acceleration=predicted_acceleration,
                        free_velocity=free_velocity,free_acceleration=free_acceleration,row=row)
                path = evidence.output/(branch+'-grid'+str(len(selected))+'-response.npz')
                np.savez_compressed(path,times=times[selected],velocity=[results[stride][index]['velocity'] for index in selected],
                    acceleration=[results[stride][index]['acceleration'] for index in selected],
                    frozen_velocity=[results[stride][index]['free_velocity'] for index in selected],
                    frozen_acceleration=[results[stride][index]['free_acceleration'] for index in selected])
                evidence.own(path,'outputs')
                evidence.report['progress'] = dict(branch=branch,completed_grid=len(selected),wall_seconds=perf_counter()-start)
                evidence.save()
                print(json.dumps(dict(branch=branch,grid=len(selected),final_error=results[stride][32]['row']['action_response_error_norm'],
                    wall_seconds=perf_counter()-start,operator_products=cumulative_products)),flush=True)
            for index in range(0,33,4):
                differences = []
                for first,last in [(4,2),(2,1)]:
                    differences.append(actions[1].energy_norm(results[first][index]['velocity']-results[last][index]['velocity'],
                        results[first][index]['acceleration']-results[last][index]['acceleration']))
                evidence.report['sampling'].append(dict(branch=branch,reverse_time=float(times[index]),
                    grid9_to17=differences[0],grid17_to33=differences[1],valid_for_claim=False))
            final = results[1][32]['row']
            evidence.report['cases'].append(dict(branch=branch,final_action_response_error=final['action_response_error_norm'],
                final_previous_modal_error=final['previous_modal_error_norm'],
                max_action_response_error=max(value['row']['action_response_error_norm'] for value in results[1].values()),
                initial_action_response_error=results[1][0]['row']['action_response_error_norm'],
                final_actual_energy=final['actual_action_energy'],final_reconstructed_energy=final['reconstructed_action_energy'],
                final_source_response_norm=final['source_response_norm'],
                max_frozen_energy_relative_drift=max(value['row']['max_homogeneous_energy_relative_drift'] for value in results[1].values()),
                valid_for_claim=False))
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
