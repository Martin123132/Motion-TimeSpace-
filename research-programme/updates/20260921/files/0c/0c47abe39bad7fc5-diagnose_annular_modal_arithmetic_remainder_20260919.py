from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_moving_duhamel_20260919 import forced_linear_step
from derive_annular_frozen_forcing_time_envelope_20260919 import modal_setup,modal_state
from run_annular_P2_continuum_bridge_20260918 import checked_load
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-moving-duhamel-modal-arithmetic-attempt01',__file__)
    try:
        evidence.report.update(github_action=False,subagents_used=False,no_new_evolution=True,
            full_live_P2_force_convergence_proven=False,arithmetic_defect_not_new_physical_force=True,
            all_modes_retained=True,no_fitted_coefficients=True,original_action_forcing_unchanged=True,
            no_continuous_time_certificate=True)
        evidence.report['points'],evidence.report['reconstructions'],evidence.report['comparisons'] = [],[],[]
        previous_path = evidence.output.parent/'annular-moving-duhamel-trajectory-attempt01/status.json'
        previous = json.loads(previous_path.read_text())
        evidence.own(previous_path)
        evidence.check('trajectory_evaluations_complete',previous['state'] == 'complete' and all(row['passed'] for row in previous['checks']))
        for branch in ['reference','MTS']:
            matrices = checked_load(evidence,'annular-action-adjoint-stability-attempt01',branch+'_final-action-matrices.npz')
            canonical = checked_load(evidence,'annular-live-compensated-rate-attempt01',branch+'-1e-07-compensated-rate.npz')
            center = (canonical['1_state'].shape[1]-1)//2
            modal = [modal_setup(matrices[name+'_mass'],matrices[name+'_stiffness'],canonical[str(level)+'_state'][0,center,:-1],
                -canonical[str(level)+'_full_direction'][0,center,:-1]) for level,name in enumerate(['coarse','fine'])]
            projection = [data['modes'].T @ matrices[name+'_mass'] for data,name in zip(modal,['coarse','fine'])]
            interpolation = matrices['interpolation']
            overlap = projection[1] @ interpolation @ modal[0]['modes']
            fine_gram = projection[1] @ modal[1]['modes']
            forces,points,defects = [[],[]],[],[[],[]]
            for index in range(33):
                point = checked_load(evidence,'annular-moving-duhamel-trajectory-attempt01',branch+'-point'+str(index).zfill(3)+'.npz')
                points.append(point)
                for level in range(2):
                    prefix = str(level)+'_'
                    position = projection[level] @ point[prefix+'position']
                    acceleration = projection[level] @ point[prefix+'acceleration']
                    force = acceleration+modal[level]['frequency']**2*position
                    original = point[prefix+'modal_force']
                    defect = force-original
                    forces[level].append(force)
                    defects[level].append(defect)
                    evidence.report['points'].append(dict(branch=branch,reverse_time=float(point['reverse_time']),level=level,
                        original_action_forcing_norm=float(np.linalg.norm(original)),
                        diagonal_coordinate_forcing_norm=float(np.linalg.norm(force)),
                        retained_modal_arithmetic_defect_norm=float(np.linalg.norm(defect)),valid_for_claim=False))
            forces,defects = [np.asarray(values) for values in forces],[np.asarray(values) for values in defects]
            times = np.array([point['reverse_time'] for point in points])
            results = {}
            for stride in [4,2,1]:
                positions = [np.zeros(len(data['frequency'])) for data in modal]
                velocities = [np.zeros(len(data['frequency'])) for data in modal]
                selected = list(range(0,33,stride))
                results[stride] = {}
                for local,index in enumerate(selected):
                    if local:
                        before = selected[local-1]
                        for level in range(2):
                            positions[level],velocities[level] = forced_linear_step(modal[level]['frequency'],positions[level],velocities[level],
                                forces[level][before],forces[level][index],times[index]-times[before])
                    accelerations = [forces[level][index]-modal[level]['frequency']**2*positions[level] for level in range(2)]
                    correction = fine_gram @ accelerations[1]-overlap @ accelerations[0]
                    correction = correction+1j*modal[1]['frequency']*(fine_gram @ velocities[1]-overlap @ velocities[0])
                    frozen = [modal_state(data,times[index]) for data in modal]
                    frozen_z = projection[1] @ (frozen[1][2]-interpolation @ frozen[0][2])
                    frozen_z = frozen_z+1j*modal[1]['frequency']*(projection[1] @ (frozen[1][1]-interpolation @ frozen[0][1]))
                    point = points[index]
                    actual_z = projection[1] @ (point['1_acceleration']-interpolation @ point['0_acceleration'])
                    actual_z = actual_z+1j*modal[1]['frequency']*(projection[1] @ (point['1_reverse_velocity']-interpolation @ point['0_reverse_velocity']))
                    predicted = frozen_z+correction
                    previous_row = next(row for row in previous['reconstructions'] if row['branch'] == branch
                        and row['grid_points'] == len(selected) and row['reverse_time'] == times[index])
                    row = dict(branch=branch,grid_points=len(selected),reverse_time=float(times[index]),
                        original_unresolved_norm=previous_row['unresolved_response_norm'],
                        arithmetic_corrected_unresolved_norm=float(np.linalg.norm(actual_z-predicted)),
                        corrected_response_norm=float(np.linalg.norm(correction)),
                        reconstructed_energy=.5*float(np.vdot(predicted,predicted).real),
                        actual_energy=.5*float(np.vdot(actual_z,actual_z).real),valid_for_claim=False)
                    evidence.report['reconstructions'].append(row)
                    results[stride][index] = dict(correction=correction,predicted=predicted,row=row)
                path = evidence.output/(branch+'-grid'+str(len(selected))+'.npz')
                np.savez_compressed(path,times=times[selected],corrections=[results[stride][index]['correction'] for index in selected],
                    predicted=[results[stride][index]['predicted'] for index in selected])
                evidence.own(path,'outputs')
            for index in range(0,33,4):
                evidence.report['comparisons'].append(dict(branch=branch,reverse_time=float(times[index]),
                    corrected_grid9_to17=float(np.linalg.norm(results[4][index]['correction']-results[2][index]['correction'])),
                    corrected_grid17_to33=float(np.linalg.norm(results[2][index]['correction']-results[1][index]['correction'])),valid_for_claim=False))
            summary = results[1][32]['row']
            evidence.report['cases'].append(dict(branch=branch,final_original_unresolved_norm=summary['original_unresolved_norm'],
                final_corrected_unresolved_norm=summary['arithmetic_corrected_unresolved_norm'],
                max_corrected_unresolved_norm=max(value['row']['arithmetic_corrected_unresolved_norm'] for value in results[1].values()),
                initial_original_unresolved_norm=results[1][0]['row']['original_unresolved_norm'],
                initial_corrected_unresolved_norm=results[1][0]['row']['arithmetic_corrected_unresolved_norm'],
                final_corrected_reconstructed_energy=summary['reconstructed_energy'],
                fine_max_arithmetic_defect=max(float(np.linalg.norm(value)) for value in defects[1]),
                coarse_max_arithmetic_defect=max(float(np.linalg.norm(value)) for value in defects[0]),
                valid_for_claim=False))
            evidence.check(branch+'_finite_all_mode_arithmetic_diagnostics',all(np.all(np.isfinite(values)) for values in forces+defects))
            evidence.check(branch+'_initial_coordinate_identity',results[1][0]['row']['arithmetic_corrected_unresolved_norm'] < 1e-9)
            path = evidence.output/(branch+'-modal-arithmetic.npz')
            np.savez_compressed(path,times=times,coarse_defect=defects[0],fine_defect=defects[1],
                coarse_coordinate_forcing=forces[0],fine_coordinate_forcing=forces[1])
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
