from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_full_characteristic_field_20260917 import InitialPrimitives
from derive_annular_characteristic_source_20260917 import rhs, force
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_flat_preassembled_flow_20260916 import FlatPreassembledFlow
from annular_matrix_free_adjoint_20260917 import MatrixFreeAdjoint
from annular_instantaneous_force_bridge_20260917 import reference_force_rate, force_diagnostics
import argparse
import hashlib
import json
import numpy as np
import sympy as sp


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    options = parser.parse_args()
    evidence = EvidenceRun(options.label, __file__)
    try:
        evidence.report.update(original_action_unchanged=True, original_trajectories_reused_not_rerun=True,
            finite_future_trajectories_read=True, no_forward_trajectory_rerun=True, both_branches_same_protocol=True,
            derivative_samples_not_uniform_Lipschitz_certificate=True, pointwise_force_convergence_proven=False,
            energy_norm_uses_instantaneous_geometry=True, source_field_momentum_retained=True,
            old_peak_force_gates_unchanged=True, force_fit=False, force_correction=False)
        epsilon, regularity, delta = sp.symbols('epsilon regularity delta', positive=True)
        upper = 2*epsilon/delta+regularity*delta/2
        optimum = 2*sp.sqrt(epsilon/regularity)
        evidence.check('interpolation_stationary_window', sp.simplify(sp.diff(upper, delta).subs(delta, optimum)) == 0)
        evidence.check('interpolation_optimal_value', sp.simplify(upper.subs(delta, optimum)-2*sp.sqrt(epsilon*regularity)) == 0)
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
        initial = InitialPrimitives()
        times = reference['times']
        derivatives = np.array([reference_force_rate(instant, state, initial)['rate']
            for instant, state in zip(times, reference['source_states'])])
        reference_controls = np.array([reference_force_rate(instant, state, initial)['rate']
            for instant, state in zip(times, reference['standard_source_states'])])
        reconstructed = np.array([reference_force_rate(instant, state, initial)['force']
            for instant, state in zip(times, reference['source_states'])])
        evidence.check('reference_force_matches_original', max(abs(reconstructed-reference['forces'])) < 2e-14,
            float(max(abs(reconstructed-reference['forces']))))
        reference_difference_errors = []
        for index in [10, 20, 34, 42, 64, 70]:
            instant, state = times[index], reference['source_states'][index]
            direction = rhs(instant, state)
            step = 1e-5
            values = [force(instant+offset*step, state+offset*step*direction) for offset in [-2, -1, 1, 2]]
            difference = (values[0]-8*values[1]+8*values[2]-values[3])/(12*step)
            error = float(abs(difference-derivatives[index]))
            reference_difference_errors.append(error)
            evidence.check('reference_directional_derivative_'+str(index), error < 3e-10, error)
        evidence.report['reference_derivative_control'] = float(max(abs(derivatives-reference_controls)))
        evidence.report['reference_maximum_directional_difference_error'] = max(reference_difference_errors)
        for count, standard_label, tight_label in [(513, 'annular-joint-rectangle-attempt01', 'annular-joint-tight513-attempt01'),
                (1025, 'annular-joint-finer1025-attempt01', 'annular-joint-tight1025-resumed-attempt01')]:
            for branch in ['reference', 'MTS']:
                prefix = branch+str(count)
                system = LocallyRefinedSourceAction(count, branch == 'MTS', background_mass=0., source_splits=8)
                adjoint = MatrixFreeAdjoint(FlatPreassembledFlow(system))
                filename = prefix+'-8-trajectory.npz'
                arrays, controls = [], []
                for label, setting in [(standard_label, 'standard'), (tight_label, 'tight')]:
                    saved = read_pack(label, filename)
                    evidence.check(prefix+setting+'_original_times_shape', np.array_equal(saved['times'], times)
                        and saved['states'].shape == (81, 2*system.count+3))
                    rows = [force_diagnostics(adjoint, state) for state in saved['states']]
                    values = {name: np.array([row[name] for row in rows]) for name in rows[0]}
                    rate_scale = max(1., float(max(abs(values['rate']))))
                    complex_error = float(max(abs(values['rate']-values['complex_rate'])))
                    canonical_error = float(max(abs(values['rate']-values['canonical_rate'])))
                    pushforward_error = float(max(values['canonical_pushforward_error']))
                    evidence.check(prefix+setting+'_complex_step_force_derivative', complex_error < 2e-11*rate_scale, complex_error)
                    evidence.check(prefix+setting+'_canonical_force_derivative', canonical_error < 2e-11*rate_scale, canonical_error)
                    evidence.check(prefix+setting+'_canonical_momentum_evolution', pushforward_error < 2e-11, pushforward_error)
                    evidence.check(prefix+setting+'_Cauchy_duality', bool(np.all(abs(values['rate']) <= values['pointwise_cauchy_bound']+1e-12)))
                    force_error = float(max(abs(values['force']-saved['forces'])))
                    evidence.check(prefix+setting+'_original_saved_force', force_error < 3e-13, force_error)
                    controls.append(dict(setting=setting, complex_step_error=complex_error, canonical_pairing_error=canonical_error,
                        canonical_momentum_pushforward_error=pushforward_error, force_reconstruction_error=force_error))
                    arrays.append(values)
                standard, tight = arrays
                derivative_error = standard['rate']-derivatives
                momentum = .03*saved['states'][:, -2]/np.sqrt(1-saved['states'][:, -2]**2)
                reference_momentum = .03*reference['source_states'][:, 1]/np.sqrt(1-reference['source_states'][:, 1]**2)
                sampled_epsilon = float(max(abs(momentum-reference_momentum)))
                sampled_regularity = float(max(abs(derivative_error)))
                diagnostic_window = 2*np.sqrt(sampled_epsilon/sampled_regularity)
                sampled_peak_force = float(max(abs(standard['force']-reference['forces'])))
                row = dict(branch=branch, base_count=count, scalar_dofs=system.count,
                    maximum_sampled_absolute_force_rate=float(max(abs(standard['rate']))),
                    maximum_sampled_force_rate_error=sampled_regularity,
                    maximum_sampled_force_rate_time_control=float(max(abs(standard['rate']-tight['rate']))),
                    maximum_sampled_energy_dual_sensitivity=float(max(standard['energy_dual_sensitivity'])),
                    initial_energy_dual_sensitivity=float(standard['energy_dual_sensitivity'][0]),
                    maximum_sampled_canonical_flow_norm=float(max(standard['canonical_flow_energy_norm'])),
                    maximum_sampled_pointwise_Cauchy_bound=float(max(standard['pointwise_cauchy_bound'])),
                    tight_sample_momentum_error=sampled_epsilon,
                    uncertified_interpolation_diagnostic=2*np.sqrt(sampled_epsilon*sampled_regularity),
                    uncertified_optimizing_window=float(diagnostic_window),
                    diagnostic_window_below_saved_spacing=bool(diagnostic_window < .005),
                    diagnostic_is_not_a_continuous_bound=True, sampled_rate_is_lower_bound_on_required_Lipschitz_constant=True,
                    original_sampled_peak_force_error=sampled_peak_force, original_peak_force_gate_pass=sampled_peak_force < 2e-7,
                    implementation_controls=controls)
                destination = evidence.output/(prefix+'-force-bridge.npz')
                payload = dict(times=times, reference_rate=derivatives, standard_reference_rate=reference_controls,
                    rate_error=derivative_error)
                for setting, values in zip(['standard', 'tight'], arrays):
                    payload.update({setting+'_'+name: value for name, value in values.items()})
                np.savez_compressed(destination, **payload)
                evidence.own(destination, 'outputs')
                evidence.report['cases'].append(row)
                evidence.save()
                print({name: value for name, value in row.items() if name != 'implementation_controls'}, flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
