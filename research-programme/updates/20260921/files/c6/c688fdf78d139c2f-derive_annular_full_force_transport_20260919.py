from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_position_action_response_20260919 import PositionGenerator, propagate_position
from derive_annular_action_response_time_halving_20260919 import restore_action
from run_annular_P2_continuum_bridge_20260918 import checked_load
from scipy.sparse.linalg import expm_multiply
from time import perf_counter
import contextlib
import json
import numpy as np


def homogeneous(action, phase):
    zeros = np.zeros(action.count)
    result = propagate_position(action, phase[0], phase[1], zeros, zeros, 4e-5, np.zeros(phase.shape[-1]))
    return np.stack([result['position'],result['velocity']])


def dual_initial(action, covector):
    scale = 1e6
    zeros = np.zeros(action.count)
    generator = PositionGenerator(action,zeros,zeros,scale)
    initial = np.concatenate([covector[0]/scale,covector[1],[0.,0.]])
    result = expm_multiply(4e-5*generator.T,initial,traceA=0.)
    return np.stack([scale*result[:action.count],result[action.count:2*action.count]])


def main():
    evidence = EvidenceRun('annular-full-force-transport-attempt01',__file__)
    started = perf_counter()
    try:
        evidence.report.update(github_action=False,subagents_used=False,no_new_evolution=True,
            full_live_P2_force_convergence_proven=False,certified_continuous_time_bound=False,
            full_force_secant_not_full_nonlinear_adjoint=True,all_action_modes_retained=True,
            original_action_unchanged=True,temporal_controls_and_spatial_comparisons=True,
            measured_path_defect_not_certified_error_bound=True,maximum_wall_seconds=7200)
        evidence.report['budgets'],evidence.report['controls'],evidence.report['sampling'],evidence.report['duals'] = [],[],[],[]
        endpoint_path = evidence.output.parent/'annular-full-force-endpoints-attempt01/status.json'
        endpoint = json.loads(endpoint_path.read_text())
        evidence.own(endpoint_path)
        evidence.check('endpoint_full_force_qualified',endpoint['state'] == 'complete' and all(row['passed'] for row in endpoint['checks']))
        times = np.linspace(0.,4e-5,33)
        for branch in ['reference','MTS']:
            coarse_action = restore_action(checked_load(evidence,'annular-action-exponential-response-attempt01',branch+'-coarse-action.npz'))
            fine_action = restore_action(checked_load(evidence,'annular-action-exponential-response-attempt01',branch+'-fine-action.npz'))
            actions = [coarse_action,coarse_action,fine_action]
            matrices = checked_load(evidence,'annular-action-adjoint-stability-attempt01',branch+'_final-action-matrices.npz')
            interpolation = matrices['interpolation']
            phases,forces = [[],[],[]],[[],[],[]]
            for index in range(33):
                backward = 32-index
                old = checked_load(evidence,'annular-moving-duhamel-trajectory-attempt01',branch+'-point'+str(backward).zfill(3)+'.npz')
                new = checked_load(evidence,'annular-coarse-time64-response-attempt01',branch+'-point'+str(backward).zfill(3)+'.npz')
                evidence.check(branch+'_'+str(index)+'_same_saved_physical_time',abs(float(new['physical_time'])-times[index]) < 1e-17
                    and abs(float(old['physical_time'])-times[index]) < 1e-17)
                for level,(data,prefix) in enumerate([(old,'0_'),(new,''),(old,'1_')]):
                    phase = np.stack([data[prefix+'position'],-data[prefix+'reverse_velocity']])
                    phases[level].append(phase)
                    forces[level].append(data[prefix+'acceleration']+actions[level].acceleration_operator(phase[0]))
            phases,forces = [np.asarray(values) for values in phases],[np.asarray(values) for values in forces]
            evidence.check(branch+'_temporal_preparation_identical',np.array_equal(phases[0][0],phases[1][0]))
            for index,name in enumerate(['coarse32','coarse64','fine']):
                saved = checked_load(evidence,'annular-full-force-endpoints-attempt01',branch+'-'+name+'-phase.npz')
                error = float(np.max(abs(saved['phase']-phases[index][-1])))
                evidence.check(branch+'_'+name+'_endpoint_phase_matches',error < 2e-14,error)
            coarse_free = homogeneous(coarse_action,phases[0][0][:,:,None])[:,:,0]
            embedded_initial = np.stack([interpolation @ component for component in phases[0][0]])
            fine_initial_columns = np.stack([phases[2][0],embedded_initial],axis=-1)
            fine_free = homogeneous(fine_action,fine_initial_columns)
            free = [coarse_free,coarse_free,fine_free[:,:,0]]
            covectors = {}
            for name,first,last in [('spatial32',0,2),('spatial64',1,2),('temporal32to64',0,1)]:
                covectors[name] = checked_load(evidence,'annular-full-force-endpoints-attempt01',branch+'-'+name+'-force-covector.npz')
                covector = covectors[name]['covector']
                transfer = interpolation if last == 2 else np.eye(coarse_action.count)
                coarse_covector = np.stack([transfer.T @ component for component in covector])
                dual_fine = dual_initial(actions[last],covector)
                dual_coarse = dual_initial(actions[first],coarse_covector)
                backward_pairing = float(np.sum(dual_fine*phases[last][0])-np.sum(dual_coarse*phases[first][0]))
                forward_pairing = float(np.sum(covector*(free[last]-np.stack([transfer @ component for component in free[first]]))))
                error = abs(backward_pairing-forward_pairing)
                tolerance = 2e-10*max(abs(backward_pairing),abs(forward_pairing),1e-9)+3e-16
                evidence.check(branch+'_'+name+'_independent_dual_initial_pairing',error <= tolerance,
                    dict(error=error,tolerance=tolerance))
                evidence.report['duals'].append(dict(branch=branch,comparison=name,forward_pairing=forward_pairing,
                    backward_pairing=backward_pairing,error=error,numerical_tolerance=tolerance,valid_for_claim=False))
            results = {}
            for stride in [4,2,1]:
                selected = list(range(0,33,stride))
                responses = [np.zeros((2,action.count,1)) for action in actions]
                saved_responses = [[value[:,:,0].copy()] for value in responses]
                for local in range(1,len(selected)):
                    if perf_counter()-started > evidence.report['maximum_wall_seconds']:
                        raise RuntimeError('Safe-save transport boundary reached.')
                    before,index = selected[local-1],selected[local]
                    step = times[index]-times[before]
                    for level,action in enumerate(actions):
                        first,last = forces[level][before],forces[level][index]
                        old_response = responses[level]
                        moved = propagate_position(action,old_response[0],old_response[1],first,last,step,[1.])
                        responses[level] = np.stack([moved['position'],moved['velocity']])
                        evidence.check(branch+'_'+str(stride)+'_'+str(index)+'_'+str(level)+'_affine_coordinates',
                            abs(float(moved['constants'][0])-1.) < 1e-13 and abs(float(moved['local_time'][0])-step) < 1e-17)
                        if local == 1:
                            half = propagate_position(action,old_response[0],old_response[1],first,(first+last)/2,step/2,[1.])
                            halves = propagate_position(action,half['position'],half['velocity'],(first+last)/2,last,step/2,[1.])
                            rescaled = propagate_position(action,old_response[0],old_response[1],first,last,step,[1.],scale=5e5)
                            half_error = action.energy_norm(moved['position'][:,0]-halves['position'][:,0],moved['velocity'][:,0]-halves['velocity'][:,0])
                            scale_error = action.energy_norm(moved['position'][:,0]-rescaled['position'][:,0],moved['velocity'][:,0]-rescaled['velocity'][:,0])
                            tolerance = 2e-10*max(action.energy_norm(moved['position'][:,0],moved['velocity'][:,0]),1e-10)+2e-15
                            evidence.check(branch+'_'+str(stride)+'_'+str(level)+'_exponential_controls',half_error <= tolerance and scale_error <= tolerance)
                            evidence.report['controls'].append(dict(branch=branch,grid_points=len(selected),level=level,
                                halfstep_error=half_error,rescaling_error=scale_error,numerical_tolerance=tolerance,valid_for_claim=False))
                        saved_responses[level].append(responses[level][:,:,0].copy())
                terminal_responses = [value[:,:,0] for value in responses]
                defects = [phases[level][-1]-free[level]-terminal_responses[level] for level in range(3)]
                for name,first,last in [('spatial32',0,2),('spatial64',1,2),('temporal32to64',0,1)]:
                    source = covectors[name]
                    covector = source['covector']
                    transfer = source['transfer']
                    if last == 2:
                        initial_representation = float(np.sum(covector*(fine_free[:,:,0]-fine_free[:,:,1])))
                        operator = float(np.sum(covector*(fine_free[:,:,1]-np.stack([transfer @ component for component in coarse_free]))))
                    else:
                        initial_representation,operator = 0.,0.
                    moving = float(np.sum(covector*(terminal_responses[last]-np.stack([transfer @ component for component in terminal_responses[first]]))))
                    path = float(np.sum(covector*(defects[last]-np.stack([transfer @ component for component in defects[first]]))))
                    terminal_pairing = float(np.sum(covector*(phases[last][-1]-np.stack([transfer @ component for component in phases[first][-1]]))))
                    reconstructed = initial_representation+operator+moving+path
                    tolerance = 2e-11*max(abs(initial_representation)+abs(operator)+abs(moving)+abs(path),1e-10)+3e-16
                    evidence.check(branch+'_'+str(stride)+'_'+name+'_signed_Duhamel_telescope',abs(reconstructed-terminal_pairing) <= tolerance,
                        dict(error=abs(reconstructed-terminal_pairing),tolerance=tolerance))
                    endpoint_row = next(row for row in endpoint['secants'] if row['branch'] == branch and row['comparison'] == name)
                    full = reconstructed+float(source['geometry'])+float(source['operator'])+float(source['closure'])
                    evidence.check(branch+'_'+str(stride)+'_'+name+'_full_force_reconstruction',
                        abs(full-endpoint_row['observed_difference']) <= tolerance+endpoint_row['numerical_tolerance'])
                    row = dict(branch=branch,comparison=name,grid_points=len(selected),
                        initial_representation=initial_representation,frozen_operator_commutator=operator,
                        moving_forcing=moving,measured_path_and_forcing_sampling_defect=path,
                        field_pairing=terminal_pairing,field_pairing_without_measured_defect=initial_representation+operator+moving,
                        endpoint_geometry_source=float(source['geometry']),endpoint_operator_transfer=float(source['operator']),
                        endpoint_recorded_closure=float(source['closure']),full_reconstructed_difference=full,
                        observed_force_difference=endpoint_row['observed_difference'],
                        reconstruction_error=abs(full-endpoint_row['observed_difference']),
                        signed_term_absolute_sum=abs(initial_representation)+abs(operator)+abs(moving)+abs(path)
                            +abs(float(source['geometry']))+abs(float(source['operator']))+abs(float(source['closure'])),
                        measured_defect_is_not_certificate=True,valid_for_claim=False)
                    evidence.report['budgets'].append(row)
                    results[(name,len(selected))] = row
                for level,values in enumerate(saved_responses):
                    path = evidence.output/(branch+'-level'+str(level)+'-grid'+str(len(selected))+'.npz')
                    np.savez_compressed(path,times=times[selected],response=np.asarray(values),free_terminal=free[level],defect_terminal=defects[level])
                    evidence.own(path,'outputs')
                evidence.report['progress'] = dict(branch=branch,grid_points=len(selected),seconds=perf_counter()-started)
                evidence.save()
                print(json.dumps(evidence.report['progress']),flush=True)
            for name in ['spatial32','spatial64','temporal32to64']:
                for before,after in [(9,17),(17,33)]:
                    first,last = results[(name,before)],results[(name,after)]
                    evidence.report['sampling'].append(dict(branch=branch,comparison=name,first_grid=before,last_grid=after,
                        signed_moving_forcing_change=last['moving_forcing']-first['moving_forcing'],
                        signed_measured_defect_change=last['measured_path_and_forcing_sampling_defect']-first['measured_path_and_forcing_sampling_defect'],
                        valid_for_claim=False))
                evidence.report['cases'].append(results[(name,33)])
            evidence.save()
        evidence.report['seconds'] = perf_counter()-started
        with (evidence.output/'completion.txt').open('w',encoding='utf-8') as stream,contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt','outputs')
        evidence.save()
        print(json.dumps(dict(state='complete',checks=len(evidence.report['checks']),seconds=perf_counter()-started)),flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
