from derive_annular_source_gravity_20260914 import EvidenceRun
from datetime import datetime, timezone
import argparse
import hashlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    options = parser.parse_args()
    evidence = EvidenceRun(options.label, __file__)
    try:
        evidence.report.update(original_action_unchanged=True, finite_future_trajectories_read=False,
            no_nonlinear_forward_trajectory_rerun=True, fitted_parameters=False, old_peak_force_gates_unchanged=True,
            instantaneous_force_convergence_proven=False, initial_layer_only_not_whole_horizon=True,
            uniform_nonlinear_remainder_proven=False, same_protocol_both_branches=True)
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        prediction_path = intake/'annular-frozen-initial-layer-attempt03/status.json'
        prediction = json.loads(prediction_path.read_text())
        evidence.own(prediction_path)
        evidence.check('all_four_predictions_complete_before_comparison', prediction['state'] == 'complete'
            and len(prediction['cases']) == 4 and not prediction['finite_future_trajectories_read']
            and all(row['passed'] for row in prediction['checks']))
        evidence.report['predictions_frozen_at'] = prediction['predictions_frozen_at']
        evidence.report['comparison_started_at'] = datetime.now(timezone.utc).isoformat()
        evidence.check('freeze_precedes_comparison', evidence.report['predictions_frozen_at'] < evidence.report['comparison_started_at'])

        def read_pack(label, filename):
            folder = intake/label
            status_path = folder/'status.json'
            status = json.loads(status_path.read_text())
            evidence.own(status_path)
            evidence.check(label+filename+'_complete', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
            path = folder/filename
            evidence.own(path)
            evidence.check(label+filename+'_hash', hashlib.sha256(path.read_bytes()).hexdigest() == status['outputs'][str(path.relative_to(evidence.root))])
            with np.load(path, allow_pickle=False) as saved:
                return {name: saved[name].copy() for name in saved.files}

        reference = read_pack('annular-full-characteristic-field-attempt01', 'full-characteristic-reference.npz')
        selected = np.arange(5)
        times = reference['times'][selected]
        evidence.check('frozen_comparison_times', max(abs(times-np.array(prediction['protocol']['comparison_times']))) < 2e-16)
        evidence.report['finite_future_trajectories_read'] = True
        for count, standard_label, tight_label in [(513, 'annular-joint-rectangle-attempt01', 'annular-joint-tight513-attempt01'),
                (1025, 'annular-joint-finer1025-attempt01', 'annular-joint-tight1025-resumed-attempt01')]:
            for branch in ['reference', 'MTS']:
                prefix = branch+str(count)
                frozen = read_pack('annular-frozen-initial-layer-attempt03', prefix+'-tight-frozen-layer.npz')
                indices = np.array([np.argmin(abs(frozen['times']-instant)) for instant in times])
                evidence.check(prefix+'_frozen_endpoint_alignment', max(abs(frozen['times'][indices]-times)) < 3e-14)
                standard, tight = [read_pack(label, prefix+'-8-trajectory.npz') for label in [standard_label, tight_label]]
                evidence.check(prefix+'_original_saved_times', np.array_equal(standard['times'], reference['times'])
                    and np.array_equal(tight['times'], reference['times']))
                evidence.check(prefix+'_same_initial_state', np.array_equal(frozen['initial_state'], standard['states'][0])
                    and np.array_equal(frozen['initial_state'], tight['states'][0]))
                original_force = standard['forces'][selected]
                continuum_force = reference['forces'][selected]
                linear_force = frozen['linear_force'][indices]
                evaluated_force = frozen['evaluated_force'][indices]
                original_error = original_force-continuum_force
                predicted_error = linear_force-continuum_force
                force_difference = original_force-linear_force
                evaluated_difference = original_force-evaluated_force
                original_maximum = float(max(abs(original_error)))
                linear_maximum = float(max(abs(force_difference)))
                evaluated_maximum = float(max(abs(evaluated_difference)))
                fine_time_control = float(max(abs(original_force-tight['forces'][selected])))
                old_peak = float(max(abs(standard['forces']-reference['forces'])))
                rows = [dict(time=float(instant), original_force=float(actual), reference_force=float(exact),
                    frozen_linear_force=float(linear), frozen_evaluated_force=float(evaluated),
                    original_force_error=float(actual-exact), frozen_linear_predicted_error=float(linear-exact),
                    linear_prediction_remainder=float(actual-linear), evaluated_prediction_remainder=float(actual-evaluated))
                    for instant, actual, exact, linear, evaluated in zip(times, original_force, continuum_force, linear_force, evaluated_force)]
                row = dict(branch=branch, base_count=count, times=times.tolist(),
                    maximum_original_initial_window_force_error=original_maximum,
                    maximum_frozen_linear_prediction_remainder=linear_maximum,
                    maximum_frozen_evaluated_prediction_remainder=evaluated_maximum,
                    linear_prediction_remainder_fraction=linear_maximum/original_maximum,
                    evaluated_prediction_remainder_fraction=evaluated_maximum/original_maximum,
                    linear_diagnostic_explains_to_frozen_fraction=linear_maximum <= .25*original_maximum,
                    evaluated_diagnostic_explains_to_frozen_fraction=evaluated_maximum <= .25*original_maximum,
                    nonlinear_standard_tight_force_control=fine_time_control,
                    original_full_horizon_sampled_peak_force_error=old_peak, original_peak_force_gate_pass=old_peak < 2e-7,
                    endpoint_rows=rows)
                evidence.report['cases'].append(row)
                destination = evidence.output/(prefix+'-frozen-comparison.npz')
                np.savez_compressed(destination, times=times, original_force=original_force, reference_force=continuum_force,
                    frozen_linear_force=linear_force, frozen_evaluated_force=evaluated_force,
                    original_error=original_error, predicted_error=predicted_error, force_remainder=force_difference,
                    evaluated_remainder=evaluated_difference)
                evidence.own(destination, 'outputs')
                evidence.save()
                print({name: value for name, value in row.items() if name != 'endpoint_rows'}, flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
