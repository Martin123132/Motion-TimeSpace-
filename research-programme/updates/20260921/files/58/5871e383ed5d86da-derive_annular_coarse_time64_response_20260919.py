from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_action_response_time_halving_20260919 import restore_action
from annular_action_exponential_20260919 import propagate
from annular_moving_duhamel_20260919 import live_item, live_acceleration
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from run_annular_P2_continuum_bridge_20260918 import checked_load
from time import perf_counter
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-coarse-time64-response-attempt01', __file__)
    started = perf_counter()
    try:
        evidence.report.update(github_action=False, subagents_used=False,
            no_new_evolution_in_this_script=True, uses_new_coarse_evolution=True,
            original_action_and_source_unchanged=True, identical_frozen_action=True,
            fine_trajectory_fixed=True, all_action_rows_retained=True,
            no_modal_diagnostic=True, full_live_P2_force_convergence_proven=False,
            certified_continuous_time_bound=False, richardson_is_diagnostic=True,
            maximum_wall_seconds=7200., valid_for_claim=False)
        for name in ['points', 'responses', 'controls', 'sampling', 'richardson']:
            evidence.report[name] = []
        source_folder = 'annular-action-exponential-response-attempt01'
        times = np.linspace(0., 4e-5, 33)
        for branch in ['reference', 'MTS']:
            action_data = [checked_load(evidence, source_folder, branch+'-'+name+'-action.npz')
                for name in ['coarse', 'fine']]
            coarse_action, fine_action = [restore_action(data) for data in action_data]
            matrices = checked_load(evidence, 'annular-action-adjoint-stability-attempt01', branch+'_final-action-matrices.npz')
            interpolation = matrices['interpolation']
            trajectory = checked_load(evidence, 'annular-coarse-time64-'+branch+'-attempt01', 'trajectory-steps64.npz')
            old_response = {count: checked_load(evidence, source_folder, branch+'-grid'+str(count)+'-response.npz')
                for count in [9, 17, 33]}
            initial = checked_load(evidence, 'annular-P2-joint-refinement-257-cap2e-05-attempt01', branch+'-initial.npz')
            evidence.check(branch+'_same_original_initial_state', np.array_equal(trajectory['states'][0],
                np.stack([initial['coordinates'], initial['momenta']])))
            system = IndexedGradedP2System(257, branch == 'MTS', 2e-5)
            center = int(np.argmin(abs(system.labels)))
            positions, velocities, accelerations = [[], [], []], [[], [], []], [[], [], []]
            forcing = [[], [], []]
            for index, reverse_time in enumerate(times):
                if perf_counter()-started > evidence.report['maximum_wall_seconds']:
                    raise RuntimeError('Safe-save boundary; evaluated points preserved.')
                forward = 64-2*index
                state = trajectory['states'][forward]
                old = checked_load(evidence, 'annular-moving-duhamel-trajectory-attempt01',
                    branch+'-point'+str(index).zfill(3)+'.npz')
                evidence.check(branch+'_'+str(index)+'_matched_times',
                    abs(float(trajectory['times'][forward])-(4e-5-reverse_time)) < 1e-17
                    and abs(float(old['reverse_time'])-reverse_time) < 1e-17)
                base = live_item(system, state, center)
                base['flow'] = np.stack([base['all_rates'], system.forces(state[0], base['all_rates'], base['geometry'])])
                measured = live_acceleration(system, state, center, base, 5e-8)
                error = float(np.max(abs(measured['acceleration']-measured['direct_acceleration'])))
                tolerance = 2e-4*max(float(np.max(abs(measured['direct_acceleration']))), 1e-8)+1e-8
                evidence.check(branch+'_'+str(index)+'_canonical_acceleration', error <= tolerance,
                    dict(error=error, tolerance=tolerance))
                probe_error = 0.
                if index in [0, 16, 32]:
                    half = live_acceleration(system, state, center, base, 2.5e-8)
                    probe_error = float(np.max(abs(measured['acceleration']-half['acceleration'])))
                    evidence.check(branch+'_'+str(index)+'_probe_halving', probe_error <= tolerance,
                        dict(error=probe_error, tolerance=tolerance))
                positions[0].append(base['values'][:-1].copy())
                velocities[0].append(-base['rates'][:-1].copy())
                accelerations[0].append(measured['acceleration'])
                for column, prefix in [(1, '0_'), (2, '1_')]:
                    positions[column].append(old[prefix+'position'])
                    velocities[column].append(old[prefix+'reverse_velocity'])
                    accelerations[column].append(old[prefix+'acceleration'])
                for column, action in enumerate([coarse_action, coarse_action, fine_action]):
                    forcing[column].append(accelerations[column][-1]+action.acceleration_operator(positions[column][-1]))
                evidence.check(branch+'_'+str(index)+'_old_forcing_exactly_retained',
                    np.array_equal(forcing[1][-1], action_data[0]['physical_forcing'][index])
                    and np.array_equal(forcing[2][-1], action_data[1]['physical_forcing'][index]))
                temporal_velocity = interpolation @ (velocities[0][-1]-velocities[1][-1])
                temporal_acceleration = interpolation @ (accelerations[0][-1]-accelerations[1][-1])
                if index == 32:
                    evidence.check(branch+'_shared_initial_velocity_acceleration',
                        np.array_equal(velocities[0][-1], velocities[1][-1])
                        and np.array_equal(accelerations[0][-1], accelerations[1][-1]))
                arrays = dict(physical_time=4e-5-reverse_time, reverse_time=reverse_time,
                    position=positions[0][-1], reverse_velocity=velocities[0][-1], acceleration=accelerations[0][-1],
                    forcing=forcing[0][-1], mass_rate=measured['mass_rate'], cross_rate=measured['cross_rate'],
                    inverse_residual_rate=measured['inverse_residual_rate'], source_acceleration=measured['source_acceleration'])
                path = evidence.output/(branch+'-point'+str(index).zfill(3)+'.npz')
                np.savez_compressed(path, **arrays)
                evidence.own(path, 'outputs')
                evidence.report['points'].append(dict(branch=branch, reverse_time=float(reverse_time),
                    physical_time=float(4e-5-reverse_time), acceleration_control_error=error,
                    numerical_tolerance=tolerance, probe_halving_performed=index in [0, 16, 32],
                    probe_halving_error=probe_error, interpolated_coarse_temporal_norm=fine_action.energy_norm(
                        temporal_velocity, temporal_acceleration), valid_for_claim=False))
                evidence.report['progress'] = dict(branch=branch, completed_points=index+1, total_points=33,
                    seconds=perf_counter()-started)
                evidence.save()
                if index % 8 == 0:
                    print(json.dumps(evidence.report['progress']), flush=True)
            forcing = [np.asarray(values) for values in forcing]
            predictions = {}
            for stride in [4, 2, 1]:
                selected = list(range(0, 33, stride))
                predicted_velocity = [values[0][:, None].copy() for values in velocities]
                predicted_acceleration = [values[0][:, None].copy() for values in accelerations]
                predictions[stride] = {}
                for local, index in enumerate(selected):
                    if local:
                        before = selected[local-1]
                        step = times[index]-times[before]
                        for column, action in enumerate([coarse_action, coarse_action, fine_action]):
                            slope = (forcing[column][index]-forcing[column][before])/step
                            previous_velocity, previous_acceleration = predicted_velocity[column], predicted_acceleration[column]
                            moved = propagate(action, previous_velocity, previous_acceleration, slope, step, np.ones(1))
                            predicted_velocity[column], predicted_acceleration[column] = moved['velocity'], moved['acceleration']
                            evidence.check(branch+'_'+str(stride)+'_'+str(index)+'_'+str(column)+'_constant_coordinate',
                                abs(float(moved['constants'][0])-1.) < 1e-13)
                            if local == 1:
                                half = propagate(action, previous_velocity, previous_acceleration, slope, step/2, np.ones(1))
                                halves = propagate(action, half['velocity'], half['acceleration'], slope, step/2, np.ones(1))
                                rescaled = propagate(action, previous_velocity, previous_acceleration, slope, step, np.ones(1), scale=5e5)
                                half_error = action.energy_norm(moved['velocity'][:,0]-halves['velocity'][:,0],
                                    moved['acceleration'][:,0]-halves['acceleration'][:,0])
                                scale_error = action.energy_norm(moved['velocity'][:,0]-rescaled['velocity'][:,0],
                                    moved['acceleration'][:,0]-rescaled['acceleration'][:,0])
                                control_tolerance = 2e-10*max(action.energy_norm(previous_velocity[:,0], previous_acceleration[:,0]), 1e-8)+1e-12
                                evidence.check(branch+'_'+str(stride)+'_'+str(column)+'_propagation_controls',
                                    half_error <= control_tolerance and scale_error <= control_tolerance)
                                evidence.report['controls'].append(dict(branch=branch, grid_points=len(selected), column=column,
                                    halfstep_error=half_error, rescaling_error=scale_error,
                                    numerical_tolerance=control_tolerance, valid_for_claim=False))
                    predicted = [(predicted_velocity[2][:,0]-interpolation @ predicted_velocity[column][:,0],
                        predicted_acceleration[2][:,0]-interpolation @ predicted_acceleration[column][:,0]) for column in [0, 1]]
                    actual = [(velocities[2][index]-interpolation @ velocities[column][index],
                        accelerations[2][index]-interpolation @ accelerations[column][index]) for column in [0, 1]]
                    errors = [tuple(predicted[column][component]-actual[column][component] for component in [0,1]) for column in [0,1]]
                    old_saved = old_response[len(selected)]
                    match = fine_action.energy_norm(predicted[1][0]-old_saved['velocity'][local],
                        predicted[1][1]-old_saved['acceleration'][local])
                    evidence.check(branch+'_'+str(stride)+'_'+str(index)+'_old_response_reproduced', match < 1e-11, match)
                    fine_residual = (predicted_velocity[2][:,0]-velocities[2][index],
                        predicted_acceleration[2][:,0]-accelerations[2][index])
                    coarse_residuals = [(interpolation @ (predicted_velocity[column][:,0]-velocities[column][index]),
                        interpolation @ (predicted_acceleration[column][:,0]-accelerations[column][index])) for column in [0,1]]
                    cancellation = fine_action.energy_norm(errors[0][0]-errors[1][0]+coarse_residuals[0][0]-coarse_residuals[1][0],
                        errors[0][1]-errors[1][1]+coarse_residuals[0][1]-coarse_residuals[1][1])
                    evidence.check(branch+'_'+str(stride)+'_'+str(index)+'_fixed_fine_cancels', cancellation < 1e-11, cancellation)
                    fine_norm = fine_action.energy_norm(*fine_residual)
                    coarse_norm = fine_action.energy_norm(*coarse_residuals[0])
                    new_norm, old_norm = [fine_action.energy_norm(*value) for value in errors]
                    signed_cross = -2*float(fine_residual[0] @ fine_action.stiffness(coarse_residuals[0][0])
                        +fine_residual[1] @ fine_action.mass(coarse_residuals[0][1]))
                    telescope_error = abs(new_norm**2-fine_norm**2-coarse_norm**2-signed_cross)
                    tolerance = 1e-9*max(new_norm**2, fine_norm**2, coarse_norm**2, 1e-30)+1e-23
                    evidence.check(branch+'_'+str(stride)+'_'+str(index)+'_signed_energy_telescope', telescope_error <= tolerance)
                    row = dict(branch=branch, grid_points=len(selected), reverse_time=float(times[index]),
                        old_coarse32_error=old_norm, new_coarse64_error=new_norm,
                        fine_residual_norm=fine_norm, old_interpolated_coarse_residual_norm=fine_action.energy_norm(*coarse_residuals[1]),
                        new_interpolated_coarse_residual_norm=coarse_norm, signed_cross_energy_twice=signed_cross,
                        old_response_reproduction_error=match, fixed_fine_cancellation_error=cancellation,
                        signed_error_change_norm=fine_action.energy_norm(errors[0][0]-errors[1][0], errors[0][1]-errors[1][1]),
                        factor4_vector_gap=fine_action.energy_norm(errors[1][0]-4*errors[0][0], errors[1][1]-4*errors[0][1]),
                        valid_for_claim=False)
                    evidence.report['responses'].append(row)
                    predictions[stride][index] = dict(predicted=predicted, actual=actual, errors=errors, row=row)
                path = evidence.output/(branch+'-response-grid'+str(len(selected))+'.npz')
                np.savez_compressed(path, times=times[selected],
                    velocity=[predictions[stride][index]['predicted'][0][0] for index in selected],
                    acceleration=[predictions[stride][index]['predicted'][0][1] for index in selected],
                    new_error_velocity=[predictions[stride][index]['errors'][0][0] for index in selected],
                    new_error_acceleration=[predictions[stride][index]['errors'][0][1] for index in selected],
                    old_error_velocity=[predictions[stride][index]['errors'][1][0] for index in selected],
                    old_error_acceleration=[predictions[stride][index]['errors'][1][1] for index in selected])
                evidence.own(path, 'outputs')
                evidence.save()
            for index in range(0,33,4):
                old_differences, new_differences = [], []
                for first, last in [(4,2), (2,1)]:
                    for column, output in [(0, new_differences), (1, old_differences)]:
                        first_value = predictions[first][index]['predicted'][column]
                        last_value = predictions[last][index]['predicted'][column]
                        output.append(fine_action.energy_norm(first_value[0]-last_value[0], first_value[1]-last_value[1]))
                evidence.report['sampling'].append(dict(branch=branch, reverse_time=float(times[index]),
                    old_grid9_to17=old_differences[0], old_grid17_to33=old_differences[1],
                    new_grid9_to17=new_differences[0], new_grid17_to33=new_differences[1], valid_for_claim=False))
            for index in range(0,33,2):
                rich = [tuple((4*predictions[1][index]['errors'][column][component]
                    -predictions[2][index]['errors'][column][component])/3 for component in [0,1]) for column in [0,1]]
                evidence.report['richardson'].append(dict(branch=branch, reverse_time=float(times[index]),
                    old_error=fine_action.energy_norm(*rich[1]), new_error=fine_action.energy_norm(*rich[0]),
                    factor4_vector_gap=fine_action.energy_norm(rich[1][0]-4*rich[0][0], rich[1][1]-4*rich[0][1]),
                    valid_for_claim=False))
            for stride in [4,2,1]:
                rows = [item['row'] for item in predictions[stride].values()]
                last = rows[-1]
                evidence.report['cases'].append(dict(branch=branch, grid_points=len(rows),
                    final_old_error=last['old_coarse32_error'], final_new_error=last['new_coarse64_error'],
                    max_old_error=max(row['old_coarse32_error'] for row in rows),
                    max_new_error=max(row['new_coarse64_error'] for row in rows),
                    final_fine_residual=last['fine_residual_norm'],
                    final_new_coarse_residual=last['new_interpolated_coarse_residual_norm'],
                    max_new_coarse_residual=max(row['new_interpolated_coarse_residual_norm'] for row in rows),
                    max_fine_residual=max(row['fine_residual_norm'] for row in rows),
                    final_factor4_gap=last['factor4_vector_gap'], initial_error=rows[0]['new_coarse64_error'],
                    valid_for_claim=False))
            evidence.save()
            print(json.dumps(dict(seconds=perf_counter()-started, **evidence.report['cases'][-1])), flush=True)
        evidence.report['seconds'] = perf_counter()-started
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), seconds=perf_counter()-started)), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
