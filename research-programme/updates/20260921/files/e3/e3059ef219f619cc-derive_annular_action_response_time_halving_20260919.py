from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_action_exponential_20260919 import FactoredAction,propagate
from annular_moving_duhamel_20260919 import live_item,live_acceleration
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from derive_annular_spatial_Gram_defect_split_20260919 import state_pair
from run_annular_P2_continuum_bridge_20260918 import checked_load
from scipy.sparse import csr_matrix
from time import perf_counter
import contextlib
import json
import numpy as np


def restore_action(data):
    factors = [csr_matrix((data[name+'_data'],data[name+'_indices'],data[name+'_indptr']),shape=tuple(data[name+'_shape']))
        for name in ['gradient','gram']]
    return FactoredAction(data['mass_bands'],factors[0],data['gradient_weights'],factors[1],data['gram_weights'])


def main():
    evidence = EvidenceRun('annular-action-response-time-halving-attempt01',__file__)
    start = perf_counter()
    try:
        evidence.report.update(github_action=False,subagents_used=False,no_new_evolution=True,no_new_live_evolution=True,
            full_live_P2_force_convergence_proven=False,certified_continuous_time_bound=False,
            identical_frozen_action_for_both_temporal_resolutions=True,all_modes_retained=True,
            existing_trajectories_only=True,richardson_is_diagnostic_not_certificate=True,maximum_wall_seconds=10800)
        evidence.report['points'],evidence.report['responses'],evidence.report['comparisons'] = [],[],[]
        source_folder = 'annular-action-exponential-response-attempt01'
        path = evidence.output.parent/source_folder/'status.json'
        previous = json.loads(path.read_text())
        evidence.own(path)
        evidence.check('action_response_complete',previous['state'] == 'complete' and all(row['passed'] for row in previous['checks']))
        for branch in ['reference','MTS']:
            actions = [restore_action(checked_load(evidence,source_folder,branch+'-'+name+'-action.npz')) for name in ['coarse','fine']]
            matrices = checked_load(evidence,'annular-action-adjoint-stability-attempt01',branch+'_final-action-matrices.npz')
            interpolation = matrices['interpolation']
            systems = [IndexedGradedP2System(257,branch == 'MTS',2e-5),IndexedGradedP2System(513,branch == 'MTS',1e-5)]
            center = int(np.argmin(abs(systems[0].labels)))
            initial = state_pair(evidence,branch,False)
            coarse_folder = 'annular-P2-evolved-source-halving-'+branch+'-attempt'+('02' if branch == 'MTS' else '01')
            fine_folder = 'annular-P2-bulk513-evolution-'+branch+'-attempt01'
            fine_steps = 64 if branch == 'MTS' else 32
            fine_saved = checked_load(evidence,fine_folder,'trajectory-steps'+str(fine_steps)+'.npz')
            high_response = {count:checked_load(evidence,source_folder,branch+'-grid'+str(count)+'-response.npz') for count in [9,17,33]}
            times = np.linspace(0.,4e-5,17)
            forcing,velocities,accelerations = [[],[]],[[],[]],[[],[]]
            high_actual,low_actual = {},{}
            for index,time in enumerate(times):
                if perf_counter()-start > 10800:
                    raise RuntimeError('Three-hour safe-save boundary; partial evidence retained.')
                forward = 16-index
                if forward:
                    coarse = checked_load(evidence,coarse_folder,'steps16-accepted'+str(forward).zfill(3)+'.npz')
                    states = [coarse['state'],fine_saved['states'][forward*(fine_steps//16)]]
                    evidence.check(branch+'_'+str(index)+'_matching_lower_resolution_times',
                        abs(float(coarse['time'])-(4e-5-time)) < 1e-17
                        and abs(fine_saved['times'][forward*(fine_steps//16)]-float(coarse['time'])) < 1e-17)
                else:
                    states = initial
                    evidence.check(branch+'_lower_fine_initial_matches',np.array_equal(initial[1],fine_saved['states'][0]))
                high = checked_load(evidence,'annular-moving-duhamel-trajectory-attempt01',branch+'-point'+str(2*index).zfill(3)+'.npz')
                arrays = dict(reverse_time=time)
                for level,(system,state,action) in enumerate(zip(systems,states,actions)):
                    base = live_item(system,state,center)
                    base['flow'] = np.stack([base['all_rates'],system.forces(state[0],base['all_rates'],base['geometry'])])
                    measured = live_acceleration(system,state,center,base,5e-8)
                    error = float(np.max(abs(measured['acceleration']-measured['direct_acceleration'])))
                    tolerance = 2e-4*max(float(np.max(abs(measured['direct_acceleration']))),1e-8)+1e-8
                    evidence.check(branch+'_'+str(index)+'_'+str(level)+'_canonical_acceleration',error <= tolerance,
                        dict(error=error,tolerance=tolerance))
                    velocity,acceleration = -base['rates'][:-1],measured['acceleration']
                    force = acceleration+action.acceleration_operator(base['values'][:-1])
                    forcing[level].append(force)
                    velocities[level].append(velocity)
                    accelerations[level].append(acceleration)
                    prefix = str(level)+'_'
                    for name,value in dict(position=base['values'][:-1],reverse_velocity=velocity,acceleration=acceleration,
                            forcing=force,mass_rate=measured['mass_rate'],cross_rate=measured['cross_rate'],
                            inverse_residual_rate=measured['inverse_residual_rate'],source_acceleration=measured['source_acceleration']).items():
                        arrays[prefix+name] = value
                    evidence.report['points'].append(dict(branch=branch,reverse_time=float(time),level=level,
                        lower_trajectory_steps=16 if level == 0 else fine_steps,
                        higher_trajectory_steps=32 if level == 0 else 2*fine_steps,
                        acceleration_error=error,numerical_tolerance=tolerance,valid_for_claim=False))
                high_actual[index] = (high['1_reverse_velocity']-interpolation @ high['0_reverse_velocity'],
                    high['1_acceleration']-interpolation @ high['0_acceleration'])
                low_actual[index] = (velocities[1][-1]-interpolation @ velocities[0][-1],
                    accelerations[1][-1]-interpolation @ accelerations[0][-1])
                path = evidence.output/(branch+'-lower-point'+str(index).zfill(3)+'.npz')
                np.savez_compressed(path,**arrays)
                evidence.own(path,'outputs')
                evidence.report['progress'] = dict(branch=branch,completed_points=index+1,total_points=17)
                evidence.save()
                if index % 4 == 0:
                    print(json.dumps(dict(branch=branch,point=index,wall_seconds=perf_counter()-start)),flush=True)
            forcing = [np.asarray(values) for values in forcing]
            predictions = {}
            for stride in [2,1]:
                selected = list(range(0,17,stride))
                velocity = [values[0][:,None].copy() for values in velocities]
                acceleration = [values[0][:,None].copy() for values in accelerations]
                predictions[stride] = {}
                for local,index in enumerate(selected):
                    if local:
                        before = selected[local-1]
                        step = times[index]-times[before]
                        for level,action in enumerate(actions):
                            slope = (forcing[level][index]-forcing[level][before])/step
                            result = propagate(action,velocity[level],acceleration[level],slope,step,np.ones(1))
                            velocity[level],acceleration[level] = result['velocity'],result['acceleration']
                    difference = (velocity[1][:,0]-interpolation @ velocity[0][:,0],acceleration[1][:,0]-interpolation @ acceleration[0][:,0])
                    predictions[stride][index] = difference
                    actual = low_actual[index]
                    high_index = index//stride
                    high_data = high_response[len(selected)]
                    high_error = actions[1].energy_norm(high_data['velocity'][high_index]-high_actual[index][0],
                        high_data['acceleration'][high_index]-high_actual[index][1])
                    evidence.report['responses'].append(dict(branch=branch,forcing_nodes=len(selected),reverse_time=float(times[index]),
                        lower_time_resolution_error=actions[1].energy_norm(difference[0]-actual[0],difference[1]-actual[1]),
                        higher_time_resolution_error=high_error,
                        actual_temporal_difference_norm=actions[1].energy_norm(actual[0]-high_actual[index][0],actual[1]-high_actual[index][1]),
                        valid_for_claim=False))
                path = evidence.output/(branch+'-lower-response-grid'+str(len(selected))+'.npz')
                np.savez_compressed(path,times=times[selected],velocity=[predictions[stride][index][0] for index in selected],
                    acceleration=[predictions[stride][index][1] for index in selected])
                evidence.own(path,'outputs')
            for index in range(0,17,2):
                lower_rich = tuple((4*predictions[1][index][component]-predictions[2][index][component])/3-low_actual[index][component]
                    for component in [0,1])
                higher_rich = tuple((4*high_response[17][name][index]-high_response[9][name][index//2])/3-high_actual[index][component]
                    for component,name in enumerate(['velocity','acceleration']))
                lower_norm,higher_norm = actions[1].energy_norm(*lower_rich),actions[1].energy_norm(*higher_rich)
                factor4_gap = actions[1].energy_norm(lower_rich[0]-4*higher_rich[0],lower_rich[1]-4*higher_rich[1])
                row = dict(branch=branch,reverse_time=float(times[index]),lower_richardson_error=lower_norm,
                    higher_richardson_error=higher_norm,factor4_vector_gap=factor4_gap,
                    richardson_is_estimate_not_certificate=True,valid_for_claim=False)
                evidence.report['comparisons'].append(row)
            rows = [row for row in evidence.report['responses'] if row['branch'] == branch and row['forcing_nodes'] == 17]
            last = rows[-1]
            rich = evidence.report['comparisons'][-1]
            evidence.report['cases'].append(dict(branch=branch,final_lower_error=last['lower_time_resolution_error'],
                final_higher_error=last['higher_time_resolution_error'],
                max_lower_error=max(row['lower_time_resolution_error'] for row in rows),
                max_higher_error=max(row['higher_time_resolution_error'] for row in rows),
                final_lower_richardson_error=rich['lower_richardson_error'],
                final_higher_richardson_error=rich['higher_richardson_error'],
                final_factor4_vector_gap=rich['factor4_vector_gap'],valid_for_claim=False))
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
