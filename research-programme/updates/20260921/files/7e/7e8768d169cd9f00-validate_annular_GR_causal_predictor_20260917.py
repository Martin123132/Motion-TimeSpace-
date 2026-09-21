from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_flat_preassembled_flow_20260916 import FlatPreassembledFlow
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from datetime import datetime, timezone
import argparse
import hashlib
import json
import numpy as np


def component_maximum(values,count):
    return dict(field=float(np.max(abs(values[:,:count]))),source=float(np.max(abs(values[:,count]))),
        field_rate=float(np.max(abs(values[:,count+1:-2]))),velocity=float(np.max(abs(values[:,-2]))),
        clock=float(np.max(abs(values[:,-1]))))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label',required=True)
    parser.add_argument('--runs',nargs='+',required=True)
    options = parser.parse_args()
    evidence = EvidenceRun(options.label,__file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        statuses,predictions,manifest_rows = {},{},[]
        evidence.report.update(known_benchmark_not_blind_new_experiment=True,predictions_frozen_before_future_state_reads=False,
            physical_GR_force_gate=2e-7,prediction_accuracy_gate=2e-7,numerical_control_gate=2e-8,
            original_action_unchanged=True,force_fit=False,uniform_trajectory_bound=False)
        for label in options.runs:
            folder = intake/label
            path = folder/'status.json'
            evidence.own(path)
            status = json.loads(path.read_text())
            evidence.check(label+'_complete_isolated_prediction',status['state']=='complete' and len(status['checks'])==9
                and len(status['cases'])==2 and all(row['passed'] for row in status['checks'])
                and not status['finite_future_trajectories_read'] and not status['force_fit']
                and status['count']==513 and status['source_splits']==8 and status['final_time']==.4)
            statuses[label] = status
            for branch in ['reference','MTS']:
                path = folder/(branch+'-prediction.npz')
                evidence.own(path)
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                evidence.check(label+branch+'_sealed_prediction',digest==status['outputs'][str(path.relative_to(evidence.root))])
                with np.load(path,allow_pickle=False) as saved:
                    predictions[(label,branch)] = {name:saved[name].copy() for name in saved.files}
                manifest_rows.append(dict(label=label,branch=branch,path=str(path.relative_to(evidence.root)),sha256=digest,
                    predictor_completed_at=status['completed_at']))
        configurations = {(status['configuration']['degree'],status['configuration']['stride'],status['configuration']['spectral_step_multiplier'])
            for status in statuses.values()}
        required = {(768,1,1.),(768,1,.5),(768,2,1.),(512,1,1.),(384,1,1.)}
        evidence.report['all_prespecified_controls_present'] = configurations==required
        evidence.check('no_duplicate_predictor_configurations',len(configurations)==len(statuses))
        standard_label = next(label for label,status in statuses.items() if status['configuration']['degree']==768
            and status['configuration']['stride']==1 and status['configuration']['spectral_step_multiplier']==1.)
        manifest = dict(frozen_at=datetime.now(timezone.utc).isoformat(),predictions=manifest_rows,
            physical_GR_force_gate=2e-7,prediction_accuracy_gate=2e-7,numerical_control_gate=2e-8,
            future_finite_states_not_yet_opened=True)
        destination = evidence.output/'frozen-predictions-before-finite-comparison.json'
        destination.write_text(json.dumps(manifest,indent=2,allow_nan=False)+'\n',encoding='utf-8')
        evidence.own(destination,'outputs')
        evidence.report.update(predictions_frozen_before_future_state_reads=True,freeze_time=manifest['frozen_at'])
        evidence.save()
        full_folder = intake/'annular-joint-rectangle-attempt01'
        path = full_folder/'status.json'
        evidence.own(path)
        full_status = json.loads(path.read_text())
        evidence.check('full_original_trajectories_complete',full_status['state']=='complete' and all(row['passed'] for row in full_status['checks']))
        evidence.report['future_state_read_phase_began_at'] = datetime.now(timezone.utc).isoformat()
        full = {}
        for branch in ['reference','MTS']:
            path = full_folder/(branch+'513-8-trajectory.npz')
            evidence.own(path)
            evidence.check(branch+'_full_trajectory_hash',hashlib.sha256(path.read_bytes()).hexdigest()==full_status['outputs'][str(path.relative_to(evidence.root))])
            with np.load(path,allow_pickle=False) as saved:
                full[branch] = {name:saved[name].copy() for name in ['times','states','forces','energies']}
        evidence.report['numerical_controls'] = []
        for label,status in statuses.items():
            for branch in ['reference','MTS']:
                predicted = predictions[(label,branch)]
                target = full[branch]
                baseline = predictions[(standard_label,branch)]
                system = LocallyRefinedSourceAction(513,branch=='MTS',background_mass=0.,source_splits=8)
                model = FlatPreassembledFlow(system)
                prefix = label+branch
                evidence.check(prefix+'_matching_full_times',np.array_equal(predicted['times'],target['times']) and len(predicted['times'])==81)
                original_errors = []
                for index in [0,37,42,80]:
                    state = predicted['states'][index]
                    coordinates,rates = np.split(state[:-1],2)
                    acceleration = system.acceleration(predicted['times'][index],coordinates,rates)
                    force = system.source_mass*acceleration[-1]/(1-rates[-1]**2)**1.5
                    original_errors.append(abs(float(force-predicted['force_reconstructed'][index])))
                evidence.check(prefix+'_independent_original_force',max(original_errors)<2e-11,max(original_errors))
                reconstructed_error = predicted['force_reconstructed']-target['forces']
                linear_error = predicted['force_linear']-target['forces']
                state_error = predicted['states']-target['states']
                actual_GR_error = target['forces']-predicted['oracle_forces']
                reconstructed_GR_error = predicted['force_reconstructed']-predicted['oracle_forces']
                linear_GR_error = predicted['force_linear']-predicted['oracle_forces']
                components = component_maximum(state_error,system.count)
                row = dict(label=label,branch=branch,configuration=status['configuration'],
                    maximum_reconstructed_force_prediction_error=float(np.max(abs(reconstructed_error))),
                    maximum_linear_force_prediction_error=float(np.max(abs(linear_error))),
                    reconstructed_prediction_2e7_pass=bool(np.max(abs(reconstructed_error))<2e-7),
                    linear_prediction_2e7_pass=bool(np.max(abs(linear_error))<2e-7),
                    maximum_original_GR_force_error=float(np.max(abs(actual_GR_error))),
                    maximum_predicted_GR_force_error=float(np.max(abs(reconstructed_GR_error))),
                    original_GR_force_gate_pass=bool(np.max(abs(actual_GR_error))<2e-7),
                    predicted_GR_force_gate_pass=bool(np.max(abs(reconstructed_GR_error))<2e-7),
                    actual_GR_error_at_021=float(actual_GR_error[42]),predicted_GR_error_at_021=float(reconstructed_GR_error[42]),
                    linear_GR_error_at_021=float(linear_GR_error[42]),reconstructed_error_at_021=float(reconstructed_error[42]),
                    maximum_state_prediction_errors=components,
                    original_source_clock_prediction_gates=bool(components['source']<5e-7 and components['velocity']<2e-5 and components['clock']<2e-7),
                    maximum_sampled_nonlinear_dynamical_remainder=float(np.max(abs(predicted['nonlinear_flow_remainder']))),
                    original_force_replay_error=max(original_errors))
                evidence.report['cases'].append(row)
                destination = evidence.output/(label+'-'+branch+'-comparison.npz')
                np.savez_compressed(destination,times=target['times'],actual_forces=target['forces'],
                    reconstructed_error=reconstructed_error,linear_error=linear_error,state_error=state_error,
                    actual_GR_error=actual_GR_error,reconstructed_GR_error=reconstructed_GR_error,linear_GR_error=linear_GR_error)
                evidence.own(destination,'outputs')
                if label!=standard_label:
                    force_change=float(np.max(abs(predicted['force_reconstructed']-baseline['force_reconstructed'])))
                    linear_change=float(np.max(abs(predicted['force_linear']-baseline['force_linear'])))
                    control = dict(label=label,branch=branch,configuration=status['configuration'],
                        reconstructed_force_change=force_change,linear_force_change=linear_change,
                        reconstructed_control_resolved=bool(force_change<2e-8),linear_control_resolved=bool(linear_change<2e-8),
                        state_changes=component_maximum(predicted['states']-baseline['states'],system.count))
                    evidence.report['numerical_controls'].append(control)
                evidence.save()
                print(row,flush=True)
        evidence.report.update(all_reconstructed_predictions_pass=all(row['reconstructed_prediction_2e7_pass'] for row in evidence.report['cases']),
            all_linear_predictions_pass=all(row['linear_prediction_2e7_pass'] for row in evidence.report['cases']),
            all_reconstructed_controls_resolved=all(row['reconstructed_control_resolved'] for row in evidence.report['numerical_controls']),
            all_linear_controls_resolved=all(row['linear_control_resolved'] for row in evidence.report['numerical_controls']),
            implementation_checks_not_acceptance_flags=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
