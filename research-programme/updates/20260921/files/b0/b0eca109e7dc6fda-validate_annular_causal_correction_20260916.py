from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_full_force_linearization_20260916 import FullForceLinearization
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_anchored_projector_chart_20260916 import material_terms
from datetime import datetime, timezone
import hashlib
import json
import numpy as np


def component_maximum(difference, count):
    return dict(field=float(np.max(abs(difference[:,:count]))),
        source=float(np.max(abs(difference[:,count]))),
        field_rate=float(np.max(abs(difference[:,count+1:-2]))),
        source_rate=float(np.max(abs(difference[:,-2]))), clock=float(np.max(abs(difference[:,-1]))))


def align(prediction, times):
    indices = np.argmin(abs(prediction['times'][:,None]-times[None,:]),axis=0)
    if np.max(abs(prediction['times'][indices]-times))>2e-18:
        raise ValueError('Prediction and validation times differ.')
    return {key:value[indices] for key,value in prediction.items() if key!='knot_times'}


def main():
    evidence = EvidenceRun('annular-causal-validation-attempt01', __file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        pack_path = intake/'annular-causal-inputs-attempt01/status.json'
        evidence.own(pack_path)
        config = json.loads(pack_path.read_text())['configuration']
        predictions = {}
        for precision in ['standard','tight','tight-step']:
            folder = intake/('annular-causal-'+precision+'-attempt01')
            for name in ['status.json','predictions-sealed.json']:
                evidence.own(folder/name)
            status = json.loads((folder/'status.json').read_text())
            manifest = json.loads((folder/'predictions-sealed.json').read_text())
            evidence.check(precision+'_predictions_complete_before_truth_opened', status['state']=='complete'
                and all(row['passed'] for row in status['checks']) and not manifest['future_full_arrays_loaded'])
            for table in ['inputs','outputs']:
                for name, digest in status[table].items():
                    path = evidence.root/name
                    if hashlib.sha256(path.read_bytes()).hexdigest()!=digest:
                        raise RuntimeError('Changed prediction evidence: '+name)
                    evidence.own(path)
            evidence.check(precision+'_manifest_prediction_hashes', all(status['outputs'].get(name)==digest
                for name,digest in manifest['outputs'].items()))
            for branch in ['reference','MTS']:
                for stride in ([1,2] if precision=='standard' else [1]):
                    path = folder/(branch+'-stride'+str(stride)+'-prediction.npz')
                    with np.load(path,allow_pickle=False) as saved:
                        predictions[(precision,branch,stride)] = {key:saved[key].copy() for key in saved.files}
        evidence.report.update(truth_open_started_at=datetime.now(timezone.utc).isoformat(),
            predictions_saved_before_truth_open=True, input_isolation_not_blind_discovery=True,
            original_action_unchanged=True, original_GR_failures_unchanged=True,
            nonlinear_remainder_bound=False, all_time_error_certificate=False, configuration=config)
        evidence.save()
        for branch in ['reference','MTS']:
            path = intake/'annular-force-response-paths-attempt01'/(branch+'-physical-paths.npz')
            evidence.own(path)
            with np.load(path,allow_pickle=False) as saved:
                truth = {key:saved[key].copy() for key in ['times','raw_states','reduced_states','raw_forces','reduced_forces']}
            system = LocallyRefinedSourceAction(129,branch=='MTS',background_mass=0.,source_splits=8)
            model = FullForceLinearization(system)
            baseline = component_maximum(truth['reduced_states']-truth['raw_states'],system.count)
            baseline_force = float(np.max(abs(truth['reduced_forces']-truth['raw_forces'])))
            aligned = {}
            for precision,stride in [('standard',1),('standard',2),('tight',1),('tight-step',1)]:
                original = predictions[(precision,branch,stride)]
                prediction = align(original,truth['times'])
                aligned[(precision,stride)] = prediction
                state_errors = component_maximum(prediction['corrected_states']-truth['raw_states'],system.count)
                force_error = float(np.max(abs(prediction['corrected_forces']-truth['raw_forces'])))
                nominal_error = float(np.max(abs(prediction['nominal_forces']-truth['raw_forces'])))
                nonlinear_norm = float(np.linalg.norm(original['nonlinear_residuals']))
                half_norm = float(np.linalg.norm(original['half_nonlinear_residuals']))
                reconstruction = component_maximum(original['correction_reconstruction_residuals'],system.count)
                nonlinear = component_maximum(original['nonlinear_residuals'],system.count)
                remainder = component_maximum(original['total_residuals'],system.count)
                independent_errors, independent_forces = [],[]
                for index in range(0,len(truth['times']),40):
                    instant = truth['times'][index]
                    state = prediction['corrected_states'][index]
                    coordinates,rates = np.split(state[:-1],2)
                    acceleration = system.acceleration(instant,coordinates,rates)
                    values = model.evaluate(state)
                    independent_errors.append(float(np.linalg.norm(acceleration-values['acceleration'])/max(1.,np.linalg.norm(acceleration))))
                    material = material_terms(system,coordinates[-1],rates[-1])
                    force = material['inertia']*acceleration[-1]+material['momentum_b']*rates[-1]
                    independent_forces.append(abs(float(force-prediction['corrected_forces'][index])))
                prefix = branch+'-'+precision+'-'+str(stride)
                evidence.check(prefix+'_original_action_acceleration', max(independent_errors)<2e-9,max(independent_errors))
                evidence.check(prefix+'_original_action_force', max(independent_forces)<2e-10,max(independent_forces))
                evidence.check(prefix+'_initial_truth_agreement', np.max(abs(prediction['corrected_states'][0]-truth['raw_states'][0]))<2e-15)
                evidence.check(prefix+'_same_321_observations',len(prediction['times'])==321)
                row = dict(branch=branch,precision=precision,stride=stride,uncorrected_state_errors=baseline,
                    corrected_state_errors=state_errors,uncorrected_restricted_force_error=baseline_force,
                    uncorrected_original_force_at_reduced_state_error=nominal_error,
                    corrected_force_error=force_error,force_improvement_factor=baseline_force/max(force_error,1e-300),
                    corrected_force_budget_met=bool(force_error<=config['isolated_force_budget']),
                    force_control_met=bool(force_error<=config['force_control']),
                    state_controls_met={key:bool(value<=config['state_controls'][key]) for key,value in state_errors.items()},
                    component_improvements={key:bool(value<baseline[key]) for key,value in state_errors.items()},
                    clock_roundoff_scale=bool(max(state_errors['clock'],baseline['clock'])<1e-14),
                    measured_nonlinear_residual=nonlinear,measured_reconstruction_residual=reconstruction,
                    measured_total_residual=remainder,half_amplitude_remainder_norm_ratio=half_norm/max(nonlinear_norm,1e-300),
                    maximum_energy_drift=float(np.max(abs(original['energy']-original['energy'][0]))),
                    observable_linearization_remainder=float(np.max(abs(original['corrected_forces']-original['linear_forces']))),
                    endpoint_predicted_correction=float(prediction['corrected_forces'][-1]-truth['reduced_forces'][-1]),
                    endpoint_observed_correction=float(truth['raw_forces'][-1]-truth['reduced_forces'][-1]),
                    nonlinear_remainder_is_sampled_not_uniform_bound=True)
                evidence.report['cases'].append(row)
                evidence.save()
            for control,left,right in [('path',('standard',1),('standard',2)),('tolerance',('standard',1),('tight',1)),
                ('step',('standard',1),('tight-step',1))]:
                state_change = component_maximum(aligned[left]['corrected_states']-aligned[right]['corrected_states'],system.count)
                force_change = float(np.max(abs(aligned[left]['corrected_forces']-aligned[right]['corrected_forces'])))
                evidence.check(branch+'_'+control+'_state_controls', all(value<=config['state_controls'][key]
                    for key,value in state_change.items()),state_change)
                evidence.check(branch+'_'+control+'_force_control',force_change<=config['force_control'],force_change)
                evidence.report.setdefault('controls',[]).append(dict(branch=branch,control=control,
                    state_change=state_change,force_change=force_change))
        evidence.report['both_branches_force_control_met'] = all(row['force_control_met'] for row in evidence.report['cases'])
        evidence.report['both_branches_state_controls_met'] = all(all(row['state_controls_met'].values()) for row in evidence.report['cases'])
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
