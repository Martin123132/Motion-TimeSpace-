from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_full_schur_force_20260919 import FullSchurForce, schur_difference
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from annular_live_P2_current_20260918 import LiveP2Tangent
from annular_P2_graded_source_20260919 import force_schur_identity
from run_annular_P2_continuum_bridge_20260918 import checked_load
from time import perf_counter
import contextlib
import json
import numpy as np


def scalar_row(result):
    return {name:float(value) for name,value in result.items() if np.ndim(value) == 0}


def main():
    evidence = EvidenceRun('annular-full-force-endpoints-attempt01',__file__)
    started = perf_counter()
    try:
        evidence.report.update(github_action=False,subagents_used=False,no_new_evolution=True,
            full_live_P2_force_convergence_proven=False,full_force_not_only_explicit_Gram=True,
            fixed_geometry_jet_counterfactual_not_new_dynamics=True,
            original_action_unchanged=True,maximum_wall_seconds=5400)
        evidence.report['states'],evidence.report['secants'],evidence.report['schur'] = [],[],[]
        prerequisite = evidence.output.parent/'annular-full-force-algebra-attempt01/status.json'
        previous = json.loads(prerequisite.read_text())
        evidence.own(prerequisite)
        evidence.check('independent_algebra_complete',previous['state'] == 'complete' and all(row['passed'] for row in previous['checks']))
        random = np.random.default_rng(919332)
        for branch in ['reference','MTS']:
            coarse_folder = 'annular-P2-evolved-source-halving-'+branch+'-attempt'+('02' if branch == 'MTS' else '01')
            fine_folder = ('annular-P2-bulk513-MTS-time128-attempt01' if branch == 'MTS'
                else 'annular-P2-bulk513-evolution-reference-attempt01')
            fine_steps = 128 if branch == 'MTS' else 64
            old = checked_load(evidence,coarse_folder,'steps32-accepted032.npz')
            new = checked_load(evidence,'annular-coarse-time64-'+branch+'-attempt01','trajectory-steps64.npz')
            fine = checked_load(evidence,fine_folder,'trajectory-steps'+str(fine_steps)+'.npz')
            folders = [coarse_folder,'annular-coarse-time64-'+branch+'-attempt01',fine_folder]
            statuses = [json.loads((evidence.output.parent/folder/'status.json').read_text()) for folder in folders]
            observed_forces = [next(row for row in statuses[0]['cases'] if row['steps'] == 32)['force'],
                statuses[1]['cases'][0]['new_coarse_force'],
                next(row for row in statuses[2]['cases'] if row['steps'] == fine_steps)['force']]
            states = [old['state'],new['states'][-1],fine['states'][-1]]
            systems = [IndexedGradedP2System(257,branch == 'MTS',2e-5),IndexedGradedP2System(513,branch == 'MTS',1e-5)]
            center = int(np.argmin(abs(systems[0].labels)))
            label = float(systems[0].labels[center])
            matrices = checked_load(evidence,'annular-action-adjoint-stability-attempt01',branch+'_final-action-matrices.npz')
            interpolation = matrices['interpolation']
            tangents,models,phase_states,values = [],[],[],[]
            for index,(name,state,observed) in enumerate(zip(['coarse32','coarse64','fine'],states,observed_forces)):
                if perf_counter()-started > evidence.report['maximum_wall_seconds']:
                    raise RuntimeError('Safe-save endpoint boundary reached.')
                system = systems[1] if index == 2 else systems[0]
                tangent = LiveP2Tangent(system,*state)
                current = tangent.layer_data(label)
                model = FullSchurForce(current.layer,current.tangent_layer,current.coordinates[-1],current.rates[-1])
                phase = np.stack([current.coordinates[:-1],current.rates[:-1]])
                result = model.evaluate(*phase,with_gradient=True)
                schur = force_schur_identity(current)
                tolerance = 256*np.finfo(float).eps*max(result['cancellation_scale'],1e-9)+2e-17
                drive_error = abs(result['free_wave_drive']-schur['free_wave_drive'])
                force_error = abs(result['force']-schur['predicted_reduced_force'])
                evidence.check(branch+'_'+name+'_original_action_schur',drive_error <= tolerance and force_error <= tolerance,
                    dict(drive_error=drive_error,force_error=force_error,tolerance=tolerance))
                ratio_error = abs(result['inertia_ratio']-schur['field_projection_inertia']/schur['dust_inertia'])
                evidence.check(branch+'_'+name+'_inertia_and_dust',ratio_error < 2e-13*max(result['inertia_ratio'],1e-12)
                    and abs(result['dust_drive']-schur['dust_drive']) <= tolerance,dict(ratio_error=ratio_error,tolerance=tolerance))
                observed_error = abs(result['force']-observed)
                evidence.check(branch+'_'+name+'_recorded_force_reproduced',observed_error < 3e-13,observed_error)
                direction = random.normal(size=phase.shape)*np.array([1e-8,1e-5])[:,None]
                plus,minus = model.evaluate(*(phase+direction)),model.evaluate(*(phase-direction))
                for key,gradient in [('free_wave_drive','gradient_drive'),('inertia_ratio','gradient_ratio')]:
                    difference = (plus[key]-minus[key])/2
                    analytic = float(np.sum(result[gradient]*direction))
                    numerical_tolerance = 2e-10*max(abs(analytic),1e-12)+3e-16
                    evidence.check(branch+'_'+name+'_'+key+'_actual_directional_gradient',
                        abs(difference-analytic) <= numerical_tolerance,
                        dict(difference=difference,analytic=analytic,tolerance=numerical_tolerance))
                row = dict(branch=branch,level=name,observed_force=observed,
                    signed_observed_minus_schur=observed-result['force'],original_schur_force_error=force_error,
                    original_schur_drive_error=drive_error,numerical_tolerance=tolerance,**scalar_row(result),valid_for_claim=False)
                evidence.report['states'].append(row)
                tangents.append(tangent)
                models.append(model)
                phase_states.append(phase)
                values.append(scalar_row(result))
                path = evidence.output/(branch+'-'+name+'-phase.npz')
                np.savez_compressed(path,phase=phase,gradient_force=result['gradient_force'],
                    gradient_drive=result['gradient_drive'],gradient_ratio=result['gradient_ratio'])
                evidence.own(path,'outputs')
                evidence.report['progress'] = dict(branch=branch,level=name,seconds=perf_counter()-started)
                evidence.save()
                print(json.dumps(evidence.report['progress']),flush=True)
            for name,first_index,last_index in [('spatial32',0,2),('spatial64',1,2),('temporal32to64',0,1)]:
                transfer = interpolation if last_index == 2 else np.eye(systems[0].count)
                first_phase = np.stack([transfer @ component for component in phase_states[first_index]])
                last_phase = phase_states[last_index]
                model = models[last_index]
                covector,before,after = model.secant(first_phase,last_phase)
                first_tangent,last_tangent = tangents[first_index],tangents[last_index]
                target_system = systems[1] if last_index == 2 else systems[0]
                counterfactual = FullSchurForce(target_system.layer(label,first_tangent.geometry),
                    target_system.layer(label,first_tangent.tangent_geometry),
                    states[first_index][0,center,-1],first_tangent.rates[center,-1])
                old_geometry = counterfactual.evaluate(*first_phase)
                position_pairing = float(covector[0] @ (last_phase[0]-first_phase[0]))
                velocity_pairing = float(covector[1] @ (last_phase[1]-first_phase[1]))
                field_pairing = position_pairing+velocity_pairing
                field_direct = after['force']-before['force']
                geometry = before['force']-old_geometry['force']
                operator = old_geometry['force']-values[first_index]['force']
                observed = observed_forces[last_index]-observed_forces[first_index]
                closure = ((observed_forces[last_index]-values[last_index]['force'])
                    -(observed_forces[first_index]-values[first_index]['force']))
                reconstruction = field_pairing+geometry+operator+closure
                tolerance = 512*np.finfo(float).eps*(before['cancellation_scale']+after['cancellation_scale']+1e-9)+5e-17
                evidence.check(branch+'_'+name+'_full_force_secant',abs(field_pairing-field_direct) <= tolerance,
                    dict(error=abs(field_pairing-field_direct),tolerance=tolerance))
                evidence.check(branch+'_'+name+'_signed_full_spatial_telescope',abs(reconstruction-observed) <= tolerance,
                    dict(error=abs(reconstruction-observed),tolerance=tolerance))
                if last_index == 1:
                    evidence.check(branch+'_temporal_operator_term_zero',abs(operator) <= tolerance,operator)
                schur = schur_difference(values[first_index],values[last_index])
                evidence.check(branch+'_'+name+'_J_G_q_difference',abs(schur['total']+closure-observed) <= tolerance)
                evidence.report['schur'].append(dict(branch=branch,comparison=name,**schur,
                    closure_residual=closure,observed_difference=observed,valid_for_claim=False))
                evidence.report['secants'].append(dict(branch=branch,comparison=name,
                    field_state=field_pairing,field_scalar_position=position_pairing,field_scalar_velocity=velocity_pairing,
                    geometry_source_jet=geometry,operator_and_nonnested_transfer=operator,
                    recorded_closure_residual=closure,observed_difference=observed,
                    reconstruction_error=abs(reconstruction-observed),numerical_tolerance=tolerance,
                    covector_position_norm=float(np.linalg.norm(covector[0])),
                    covector_velocity_norm=float(np.linalg.norm(covector[1])),valid_for_claim=False))
                path = evidence.output/(branch+'-'+name+'-force-covector.npz')
                np.savez_compressed(path,covector=covector,first_phase=first_phase,last_phase=last_phase,
                    transfer=transfer,field_pairing=field_pairing,geometry=geometry,operator=operator,closure=closure)
                evidence.own(path,'outputs')
            evidence.report['cases'].append(dict(branch=branch,
                spatial64_force_difference=observed_forces[2]-observed_forces[1],
                temporal_force_difference=observed_forces[1]-observed_forces[0],valid_for_claim=False))
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
