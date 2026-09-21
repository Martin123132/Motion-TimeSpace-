from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_dynamic_reduction_bound_20260916 import build_reduction, initial_projection, evolution, energy_norm, maximum, source_load, retarded_error
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_quadratic_source_fitted_action_20260915 import QuadraticSourceFittedAction
from run_annular_source_fitted_crossing_20260915 import initial
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-retained-boundary-modes-attempt02', __file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        previous_path = intake/'annular-dynamic-reduction-bound-attempt01/status.json'
        previous = json.loads(previous_path.read_text())
        evidence.own(previous_path)
        evidence.check('static_reduction_comparison_complete', previous['state']=='complete' and all(row['passed'] for row in previous['checks']))
        times = np.linspace(0., .4, 1601)
        choices = [('static', []), ('lowest_one', [0]), ('highest_one', [27]),
            ('lowest_four', list(range(4))), ('lowest_eight', list(range(8))),
            ('lowest_seven_plus_highest', list(range(7))+[27]),
            ('lowest_fourteen', list(range(14))), ('all_twenty_eight', list(range(28)))]
        evidence.report.update(prespecified_mode_choices=[dict(name=name, indices=indices) for name, indices in choices],
            sampled_reduction_budget=2e-7, selection_is_diagnostic_not_parent_physics=True)
        evidence.save()
        for gram in [False, True]:
            branch = 'MTS' if gram else 'reference'
            coarse = QuadraticSourceFittedAction(129, gram, background_mass=0.)
            fine = LocallyRefinedSourceAction(129, gram, background_mass=0., source_splits=8)
            raw = initial(fine)
            coordinates, rates = np.split(raw[:-1], 2)
            original_position, original_velocity = coordinates[:-1], rates[:-1]
            for name, chosen in choices:
                label = branch+'-'+name
                data = build_reduction(coarse, fine, retain_local=chosen)
                mass, stiffness, trial = [data[key] for key in ['mass', 'stiffness', 'trial']]
                reduced_position, reduced_velocity = initial_projection(data, original_position, original_velocity)
                full_q, full_v, full_a = evolution(mass, data['full_frequencies'], data['full_vectors'], original_position, original_velocity, times)
                reduced_q, reduced_v, reduced_a = evolution(data['reduced_mass'], data['reduced_frequencies'], data['reduced_vectors'],
                    reduced_position, reduced_velocity, times)
                approximate_q, approximate_v, approximate_a = [values @ trial.T for values in [reduced_q, reduced_v, reduced_a]]
                full_load = source_load(data, full_q, full_v, full_a)
                approximate_load = source_load(data, approximate_q, approximate_v, approximate_a)
                error_q, error_v = full_q-approximate_q, full_v-approximate_v
                initial_error_q = original_position-trial @ reduced_position
                initial_error_v = original_velocity-trial @ reduced_velocity
                initial_error = float(energy_norm(initial_error_q, initial_error_v, stiffness, mass))
                reduced_energy = float(energy_norm(reduced_position, reduced_velocity, data['reduced_stiffness'], data['reduced_mass']))
                energy_bound = initial_error+times*data['residual_norm']*reduced_energy
                actual_energy = energy_norm(error_q, error_v, stiffness, mass)
                force_bound = data['load_norm']*(reduced_energy*energy_bound+energy_bound**2/2)
                force_bound += data['residual_norm']*data['current_norm']*reduced_energy**2
                force_error = abs(full_load-approximate_load)
                galerkin_absolute = maximum(trial.T @ data['residual_map'])
                galerkin_scale = max(1., maximum(data['reduced_stiffness']))
                evidence.check(label+'_positive_variational_reduction', data['reduced_frequencies'][0]>0
                    and galerkin_absolute/galerkin_scale<2e-8,
                    dict(absolute_residual=galerkin_absolute, stiffness_scale=galerkin_scale,
                         backward_relative_residual=galerkin_absolute/galerkin_scale,
                         failed_attempt01_used_cancelling_residual_as_scale=True))
                evidence.check(label+'_full_feedback_energy_bound', np.all(actual_energy<=energy_bound*(1+2e-8)+2e-10))
                evidence.check(label+'_full_source_current_bound', np.all(force_error<=force_bound*(1+2e-8)+2e-10))
                selected = np.arange(0, 1601, 200)
                memory_q, memory_v, unused_q, unused_v = retarded_error(data, reduced_position, reduced_velocity,
                    initial_error_q, initial_error_v, times[selected])
                memory_error = max(maximum(memory_q-error_q[selected]), maximum(memory_v-error_v[selected]))
                evidence.check(label+'_retarded_defect_identity', memory_error<2e-9, memory_error)
                drift = maximum(energy_norm(approximate_q, approximate_v, stiffness, mass)-reduced_energy)
                evidence.check(label+'_conservative_induced_action', drift<2e-10, drift)
                if len(chosen)==28:
                    evidence.check(label+'_full_mode_coordinate_control', maximum(error_q)<2e-9 and maximum(error_v)<2e-9 and maximum(force_error)<2e-9,
                        dict(field=maximum(error_q), velocity=maximum(error_v), source_load=maximum(force_error)))
                path = evidence.output/(label+'.npz')
                np.savez_compressed(path, times=times, energy_error=actual_energy, energy_bound=energy_bound,
                    full_source_load=full_load, reduced_source_load=approximate_load, force_error=force_error, force_bound=force_bound)
                evidence.own(path, 'outputs')
                evidence.report['cases'].append(dict(branch=branch, mode_policy=name, retained_indices=chosen, fine_dof=fine.count,
                    reduced_dof=trial.shape[1], initial_error_energy_norm=initial_error, maximum_energy_error=float(np.max(actual_energy)),
                    maximum_source_load_error=float(np.max(force_error)), endpoint_source_load_error=float(force_error[-1]),
                    sampled_reduction_error_below_budget=bool(np.max(force_error)<=2e-7),
                    analytic_bound_numerically_below_budget=bool(force_bound[-1]<=2e-7), uniform_source_load_bound=float(force_bound[-1]),
                    retarded_error=memory_error, original_fine_initial_data_unchanged=True, freely_moving_source=False,
                    is_full_dimension_coordinate_control=bool(len(chosen)==28), mode_indices_from_low_to_high_frequency=True))
                evidence.save()
        evidence.report.update(scope='Conservative fixed-source trial spaces retain specified local normal modes and induced kinetic cross terms; not a new parent action or moving-boundary solver.',
            physical_GR_force_gate_retested=False, original_Gram_rows_retained=True, damping_added=False,
            external_data_fitted=False, freely_moving_source_certified=False, full_mode_test_is_identity_control_not_a_reduction=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
