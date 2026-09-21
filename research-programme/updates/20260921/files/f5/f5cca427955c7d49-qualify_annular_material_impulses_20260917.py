from derive_annular_source_gravity_20260914 import EvidenceRun
from datetime import datetime, timezone
import argparse
import hashlib
import json
import numpy as np
import sympy as sp


def material_momentum(speed):
    return .03*speed/np.sqrt(1-speed**2)


def window_values(times, values, width):
    stride = int(round(width/(times[1]-times[0])))
    duration = times[stride:]-times[:-stride]
    if np.max(abs(duration-width)) > 3e-15:
        raise ValueError('Window must align with the original saved times.')
    return (values[stride:]-values[:-stride])/duration


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    options = parser.parse_args()
    evidence = EvidenceRun(options.label, __file__)
    try:
        widths = [.025, .05, .1, .2, .4]
        protocol = dict(frozen_at=datetime.now(timezone.utc).isoformat(), widths=widths,
            all_aligned_starts_included=True, both_branches_same_protocol=True,
            diagnostic_force_scale=2e-7, scale_is_not_a_new_acceptance_gate=True,
            material_mass=.03, no_sparse_force_quadrature_as_definition=True)
        path = evidence.output/'frozen-window-protocol.json'
        path.write_text(json.dumps(protocol, indent=2, allow_nan=False)+'\n', encoding='utf-8')
        evidence.own(path, 'outputs')
        evidence.report.update(original_action_unchanged=True, original_trajectories_reused_not_rerun=True,
            finite_future_trajectories_read=False, all_branches_treated_identically=True,
            old_peak_force_gates_unchanged=True, averaged_force_not_peak_force=True,
            no_new_smoothed_force_acceptance_claim=True, sampled_endpoint_controls_not_interval_certificate=True,
            protocol=protocol, force_fit=False, force_correction=False)
        speed, mass = sp.symbols('speed mass', real=True)
        evidence.check('material_force_is_momentum_derivative', sp.simplify(sp.diff(mass*speed/sp.sqrt(1-speed**2), speed)
            -mass/(1-speed**2)**sp.Rational(3, 2)) == 0)
        intake = evidence.root/'source-intake/navier-stokes/20260914'

        def read_pack(label, filename):
            folder = intake/label
            status_path = folder/'status.json'
            evidence.own(status_path)
            status = json.loads(status_path.read_text())
            evidence.check(label+filename+'_complete', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
            path = folder/filename
            evidence.own(path)
            evidence.check(label+filename+'_hash', hashlib.sha256(path.read_bytes()).hexdigest() == status['outputs'][str(path.relative_to(evidence.root))])
            with np.load(path, allow_pickle=False) as saved:
                return {name: saved[name].copy() for name in saved.files}

        reference = read_pack('annular-full-characteristic-field-attempt01', 'full-characteristic-reference.npz')
        times = reference['times']
        reference_momentum = material_momentum(reference['source_states'][:, 1])
        standard_reference_momentum = material_momentum(reference['standard_source_states'][:, 1])
        evidence.check('reference_same_original_81_times', len(times) == 81 and np.max(abs(np.diff(times)-.005)) < 3e-16)
        evidence.report['finite_read_started_at'] = datetime.now(timezone.utc).isoformat()
        evidence.report['finite_future_trajectories_read'] = True
        evidence.save()
        for count, standard_label, tight_label in [(513, 'annular-joint-rectangle-attempt01', 'annular-joint-tight513-attempt01'),
                (1025, 'annular-joint-finer1025-attempt01', 'annular-joint-tight1025-resumed-attempt01')]:
            for branch in ['reference', 'MTS']:
                name = branch+str(count)+'-8-trajectory.npz'
                standard, tight = [read_pack(label, name) for label in [standard_label, tight_label]]
                prefix = branch+str(count)
                evidence.check(prefix+'_matching_times', np.array_equal(standard['times'], times) and np.array_equal(tight['times'], times))
                evidence.check(prefix+'_timelike_saved_states', max(np.max(abs(pack['states'][:, -2])) for pack in [standard, tight]) < 1.)
                momentum = material_momentum(standard['states'][:, -2])
                tight_momentum = material_momentum(tight['states'][:, -2])
                error = momentum-reference_momentum
                tight_error = tight_momentum-reference_momentum
                epsilon_sample = float(max(abs(error)))
                momentum_control = float(max(abs(momentum-tight_momentum)))
                reference_control = float(max(abs(reference_momentum-standard_reference_momentum)))
                force_error = standard['forces']-reference['forces']
                sampled_force_integral = np.concatenate([[0.], np.cumsum(np.diff(times)*(standard['forces'][1:]+standard['forces'][:-1])/2)])
                sampled_reference_integral = np.concatenate([[0.], np.cumsum(np.diff(times)*(reference['forces'][1:]+reference['forces'][:-1])/2)])
                quadrature_error = sampled_force_integral-(momentum-momentum[0])
                reference_quadrature_error = sampled_reference_integral-(reference_momentum-reference_momentum[0])
                windows, arrays = [], dict(times=times, material_momentum=momentum, reference_momentum=reference_momentum,
                    tight_material_momentum=tight_momentum, momentum_error=error, tight_momentum_error=tight_error,
                    sampled_force_error=force_error, sparse_force_quadrature_error=quadrature_error,
                    sparse_reference_quadrature_error=reference_quadrature_error)
                for width in widths:
                    measured = window_values(times, error, width)
                    tight_measured = window_values(times, tight_error, width)
                    control = float(max(abs(measured-tight_measured)))
                    reference_average_control = float(max(abs(window_values(times, reference_momentum-standard_reference_momentum, width))))
                    endpoint_bound = 2*epsilon_sample/width
                    evidence.check(prefix+str(width)+'_endpoint_error_bound', max(abs(measured)) <= endpoint_bound+3e-16)
                    evidence.check(prefix+str(width)+'_endpoint_time_control_bound', control <= 2*momentum_control/width+3e-16)
                    worst = int(np.argmax(abs(measured)))
                    row = dict(width=width, aligned_windows=len(measured), maximum_absolute_average_force_error=float(max(abs(measured))),
                        tight_maximum_absolute_average_force_error=float(max(abs(tight_measured))),
                        sampled_endpoint_bound=endpoint_bound, numerical_time_control=control,
                        reference_time_control=reference_average_control, worst_start=float(times[worst]),
                        diagnostic_below_old_peak_force_scale=bool(max(abs(measured)) < 2e-7),
                        peak_force_acceptance_not_changed=True)
                    windows.append(row)
                    arrays['window_'+str(width)] = measured
                    arrays['tight_window_'+str(width)] = tight_measured
                row = dict(branch=branch, base_count=count, maximum_sampled_momentum_error=epsilon_sample,
                    maximum_sampled_cumulative_impulse_error=float(max(abs(error-error[0]))), momentum_time_control=momentum_control,
                    reference_momentum_time_control=reference_control, original_sampled_peak_force_error=float(max(abs(force_error))),
                    original_peak_force_gate_pass=bool(max(abs(force_error)) < 2e-7),
                    maximum_sparse_force_integral_mismatch=float(max(abs(quadrature_error))),
                    maximum_sparse_reference_integral_mismatch=float(max(abs(reference_quadrature_error))), windows=windows)
                destination = evidence.output/(prefix+'-impulses.npz')
                np.savez_compressed(destination, **arrays)
                evidence.own(destination, 'outputs')
                evidence.report['cases'].append(row)
                evidence.save()
                print({name: value for name, value in row.items() if name != 'windows'}, flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
