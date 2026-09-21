from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_dynamic_reduction_bound_20260916 import build_reduction, evolution, source_load, maximum
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_quadratic_source_fitted_action_20260915 import QuadraticSourceFittedAction
from run_annular_source_fitted_crossing_20260915 import initial
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-invariant-modal-force-bound-attempt01', __file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        previous_path = intake/'annular-retained-boundary-modes-attempt02/status.json'
        previous = json.loads(previous_path.read_text())
        evidence.own(previous_path)
        evidence.check('local_mode_comparison_complete', previous['state']=='complete' and all(row['passed'] for row in previous['checks']))
        evidence.report.update(mode_order='Ascending full coupled-field frequency; not ascending local-mode frequency.',
            cutoff_candidates=[16, 32, 64, 128, 192, 256, 272, 280, 285, 286], force_budget=2e-7,
            cutoff_is_numerical_resolution_not_fitted_physical_parameter=True)
        times = np.linspace(0., .4, 1601)
        for gram in [False, True]:
            branch = 'MTS' if gram else 'reference'
            coarse = QuadraticSourceFittedAction(129, gram, background_mass=0.)
            fine = LocallyRefinedSourceAction(129, gram, background_mass=0., source_splits=8)
            data = build_reduction(coarse, fine)
            mass, stiffness = data['mass'], data['stiffness']
            frequencies, vectors = data['full_frequencies'], data['full_vectors']
            coordinates, rates = np.split(initial(fine)[:-1], 2)
            position, velocity = coordinates[:-1], rates[:-1]
            amplitudes_q, amplitudes_v = vectors.T @ mass @ position, vectors.T @ mass @ velocity
            amplitude = np.hypot(amplitudes_q, amplitudes_v/frequencies)
            velocity_amplitude = frequencies*amplitude
            modal_position_load = vectors.T @ data['position_load'] @ vectors
            modal_velocity_load = vectors.T @ data['velocity_load'] @ vectors
            contribution = np.abs(modal_position_load)*np.outer(amplitude, amplitude)
            contribution += np.abs(modal_velocity_load)*np.outer(velocity_amplitude, velocity_amplitude)
            total_bound = float(np.sum(contribution)/2)
            all_bounds = []
            for cutoff in range(1, fine.count+1):
                bound = float(np.sum(contribution[:cutoff, cutoff:])+np.sum(contribution[cutoff:, cutoff:])/2)
                all_bounds.append(bound)
            first_accepted = next(index+1 for index, value in enumerate(all_bounds) if value<=2e-7)
            full_q, full_v, full_a = evolution(mass, frequencies, vectors, position, velocity, times)
            full_load = source_load(data, full_q, full_v, full_a)
            orthogonality = maximum(vectors.T @ mass @ vectors-np.eye(fine.count))
            spectrum_error = maximum(stiffness @ vectors-(mass @ vectors)*frequencies**2)/max(1., maximum(stiffness @ vectors))
            evidence.check(branch+'_mass_normalized_complete_modes', orthogonality<2e-10 and spectrum_error<2e-8,
                dict(mass_orthogonality=orthogonality, relative_eigen_residual=spectrum_error))
            evidence.check(branch+'_nonnegative_tail_envelope_monotone', all(value>=0 for value in all_bounds)
                and all(later<=earlier+2e-14 for earlier, later in zip(all_bounds, all_bounds[1:])) and all_bounds[-1]==0.)
            controls = []
            for cutoff in sorted(set(evidence.report['cutoff_candidates']+[first_accepted])):
                selected = vectors[:, :cutoff]
                reduced_q, reduced_v, reduced_a = evolution(mass, frequencies[:cutoff], selected, position, velocity, times)
                reduced_load = source_load(data, reduced_q, reduced_v, reduced_a)
                error = abs(full_load-reduced_load)
                bound = all_bounds[cutoff-1]
                evidence.check(branch+'-'+str(cutoff)+'_output_specific_uniform_bound', np.max(error)<=bound*(1+2e-8)+2e-10,
                    dict(sampled_error=float(np.max(error)), analytic_amplitude_bound=bound))
                controls.append(dict(retained_modes=cutoff, omitted_modes=fine.count-cutoff, sampled_maximum_source_load_error=float(np.max(error)),
                    uniform_source_load_tail_bound=bound, bound_numerically_below_budget=bool(bound<=2e-7),
                    is_full_dimension_identity=bool(cutoff==fine.count)))
                path = evidence.output/(branch+'-'+str(cutoff)+'.npz')
                np.savez_compressed(path, times=times, full_load=full_load, reduced_load=reduced_load, absolute_error=error,
                    uniform_bound=bound, retained_modes=cutoff)
                evidence.own(path, 'outputs')
            path = evidence.output/(branch+'-modal-budget.npz')
            np.savez_compressed(path, frequencies=frequencies, displacement_amplitudes=amplitude,
                velocity_amplitudes=velocity_amplitude, force_contribution_envelope=contribution,
                all_cutoff_bounds=np.array(all_bounds))
            evidence.own(path, 'outputs')
            evidence.report['cases'].append(dict(branch=branch, count=129, source_splits=8, fine_dof=fine.count,
                first_cutoff_numerically_below_budget=first_accepted, removed_modes=fine.count-first_accepted,
                total_source_load_envelope=total_bound, no_mode_fit_or_amplitude_rescaling=True,
                full_initial_state_used_for_tail=True, tests=controls,
                exact_arithmetic_frozen_time_uniform_theorem=True, interval_eigenpair_roundoff_certified=False,
                reference_is_original_full_finite_action_not_GR_oracle=True))
            evidence.save()
        evidence.report.update(scope='Constructive invariant frozen-field reduction with a source-current-inclusive, initial-amplitude-aware analytic tail bound. No freely moving or continuum GR claim.',
            original_action_unchanged=True, damping_added=False, fitted_parent_coefficients=False,
            moving_basis_connection_implemented=False, all_time_moving_force_bound_proven=False,
            full_mode_identity_not_counted_as_compression=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
