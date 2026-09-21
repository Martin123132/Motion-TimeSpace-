from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_dynamic_reduction_bound_20260916 import build_reduction, initial_projection, evolution, energy_norm, maximum, source_load, on_shell_load, retarded_error
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_quadratic_source_fitted_action_20260915 import QuadraticSourceFittedAction
from run_annular_source_fitted_crossing_20260915 import initial
from scipy.linalg import solve, solve_triangular
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-dynamic-reduction-bound-attempt01', __file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        previous_path = intake/'annular-relaxed-branch-final-integrity.json'
        previous = json.loads(previous_path.read_text())
        evidence.own(previous_path)
        evidence.check('previous_checkpoint_complete', previous['state']=='complete' and all(row['passed'] for row in previous['checks']))
        times = np.linspace(0., .4, 401)
        memory_indices = np.arange(0, 401, 50)
        for count, splits in [(33, 2), (65, 2), (65, 4), (65, 8), (129, 4), (129, 8)]:
            for gram in [False, True]:
                branch = 'MTS' if gram else 'reference'
                prefix = branch+'-'+str(count)+'-s'+str(splits)
                coarse = QuadraticSourceFittedAction(count, gram, background_mass=0.)
                fine = LocallyRefinedSourceAction(count, gram, background_mass=0., source_splits=splits)
                data = build_reduction(coarse, fine)
                mass, stiffness, trial = [data[key] for key in ['mass', 'stiffness', 'trial']]
                evidence.check(prefix+'_positive_mass_and_stiffness', data['full_frequencies'][0]>0 and data['reduced_frequencies'][0]>0)
                stationarity = maximum(data['bubbles'].T @ stiffness @ trial)/max(1., maximum(stiffness @ trial))
                galerkin = maximum(trial.T @ data['residual_map'])/max(1., maximum(data['residual_map']))
                evidence.check(prefix+'_static_and_dynamic_Galerkin_identities', stationarity<2e-10 and galerkin<2e-10,
                    dict(static=stationarity, dynamic=galerkin))
                coupling = trial.T @ mass @ data['bubbles']
                local_schur = data['bubbles'].T @ mass @ data['bubbles']-coupling.T @ solve(data['reduced_mass'], coupling, assume_a='pos')
                probe = np.sin(np.arange(coarse.count)*.37)
                coarse_accel = -solve(data['reduced_mass'], data['reduced_stiffness'] @ probe, assume_a='pos')
                residual = data['residual_map'] @ probe
                direct_square = residual @ solve(mass, residual, assume_a='pos')
                local_force = coupling.T @ coarse_accel
                schur_square = local_force @ solve(local_schur, local_force, assume_a='pos')
                evidence.check(prefix+'_exact_inertial_defect_Schur_norm', abs(direct_square-schur_square)<2e-8*max(1., direct_square),
                    dict(direct=float(direct_square), schur=float(schur_square)))
                raw = initial(fine)
                coordinates, rates = np.split(raw[:-1], 2)
                original_position, original_velocity = coordinates[:-1], rates[:-1]
                reduced_position, reduced_velocity = initial_projection(data, original_position, original_velocity)
                orthogonality = max(maximum(trial.T @ stiffness @ (original_position-trial @ reduced_position)),
                    maximum(trial.T @ mass @ (original_velocity-trial @ reduced_velocity)))
                evidence.check(prefix+'_best_preparation_energy_orthogonality', orthogonality<2e-10, orthogonality)
                reduced_q, reduced_v, reduced_a = evolution(data['reduced_mass'], data['reduced_frequencies'], data['reduced_vectors'],
                    reduced_position, reduced_velocity, times)
                approximate_q, approximate_v, approximate_a = [values @ trial.T for values in [reduced_q, reduced_v, reduced_a]]
                reduced_energy = float(energy_norm(reduced_position, reduced_velocity, data['reduced_stiffness'], data['reduced_mass']))
                residuals = reduced_q @ data['residual_map'].T
                residual_norms = np.linalg.norm(solve_triangular(data['root_mass'], residuals.T, lower=True), axis=0)
                residual_supremum = data['residual_norm']*reduced_energy
                evidence.check(prefix+'_uniform_residual_operator_bound', np.max(residual_norms)<=residual_supremum*(1+2e-9)+2e-12)
                direct_load = source_load(data, approximate_q, approximate_v, approximate_a)
                on_shell = on_shell_load(data, approximate_q, approximate_v)
                reaction_correction = np.einsum('ti,ti->t', solve(mass, residuals.T, assume_a='pos').T,
                    approximate_q @ data['transport'].T)
                evidence.check(prefix+'_source_current_residual_correction', maximum(direct_load-on_shell+reaction_correction)<2e-10,
                    maximum(direct_load-on_shell+reaction_correction))
                for prepared in [False, True]:
                    label = prefix+('-prepared' if prepared else '-original')
                    position = trial @ reduced_position if prepared else original_position
                    velocity = trial @ reduced_velocity if prepared else original_velocity
                    full_q, full_v, full_a = evolution(mass, data['full_frequencies'], data['full_vectors'], position, velocity, times)
                    error_q, error_v = full_q-approximate_q, full_v-approximate_v
                    initial_error_q = position-trial @ reduced_position
                    initial_error_v = velocity-trial @ reduced_velocity
                    initial_error = float(energy_norm(initial_error_q, initial_error_v, stiffness, mass))
                    actual_error = energy_norm(error_q, error_v, stiffness, mass)
                    bound = initial_error+times*residual_supremum
                    evidence.check(label+'_full_trajectory_energy_bound', np.all(actual_error<=bound*(1+2e-8)+2e-10),
                        dict(maximum_actual=float(np.max(actual_error)), final_bound=float(bound[-1])))
                    full_load = source_load(data, full_q, full_v, full_a)
                    observed_force = abs(full_load-direct_load)
                    force_bound = data['load_norm']*(reduced_energy*bound+bound**2/2)
                    force_bound += residual_supremum*data['current_norm']*reduced_energy
                    evidence.check(label+'_complete_source_load_bound', np.all(observed_force<=force_bound*(1+2e-8)+2e-10),
                        dict(maximum_observed=float(np.max(observed_force)), uniform_bound=float(force_bound[-1])))
                    evidence.check(label+'_on_shell_full_source_current_identity', maximum(full_load-on_shell_load(data, full_q, full_v))<2e-10,
                        maximum(full_load-on_shell_load(data, full_q, full_v)))
                    reconstructed_q, reconstructed_v, homogeneous_q, homogeneous_v = retarded_error(data, reduced_position, reduced_velocity,
                        initial_error_q, initial_error_v, times[memory_indices])
                    memory_error = max(maximum(reconstructed_q-error_q[memory_indices]), maximum(reconstructed_v-error_v[memory_indices]))
                    evidence.check(label+'_retarded_feedback_including_initial_state', memory_error<2e-9, memory_error)
                    energy_drift = maximum(energy_norm(full_q, full_v, stiffness, mass)-energy_norm(position, velocity, stiffness, mass))
                    evidence.check(label+'_exact_modal_energy_conservation', energy_drift<2e-10, energy_drift)
                    canonical_error = 0.
                    for index in [0, 100, 200, 300, 400]:
                        field_coordinates = np.append(full_q[index], fine.anchor)
                        field_rates = np.append(full_v[index], 0.)
                        field_accel = np.append(full_a[index], 0.)
                        covector = fine.source_covector(times[index], field_coordinates, field_rates)
                        moved = fine.evaluate(times[index], field_coordinates+1e-24j*field_rates, field_rates+1e-24j*field_accel)
                        current_rate = moved['field_momenta'][-1].imag/1e-24
                        canonical_error = max(canonical_error, abs(float(covector-current_rate)-full_load[index]))
                    evidence.check(label+'_independent_action_source_load', canonical_error<2e-10, canonical_error)
                    path = evidence.output/(label+'.npz')
                    np.savez_compressed(path, times=times, energy_error=actual_error, energy_bound=bound,
                        full_source_load=full_load, reconstructed_source_load=direct_load, force_error=observed_force,
                        force_bound=force_bound, homogeneous_position=homogeneous_q, homogeneous_velocity=homogeneous_v)
                    evidence.own(path, 'outputs')
                    evidence.report['cases'].append(dict(branch=branch, count=count, source_splits=splits, prepared_control=prepared,
                        fine_dof=fine.count, reduced_dof=coarse.count, omitted_local_modes=data['local_count'],
                        initial_error_energy_norm=initial_error, reduced_energy_norm=reduced_energy,
                        residual_operator_norm=data['residual_norm'], source_load_operator_norm=data['load_norm'],
                        source_current_operator_norm=data['current_norm'], residual_supremum=residual_supremum,
                        maximum_energy_error=float(np.max(actual_error)), final_energy_bound=float(bound[-1]),
                        maximum_source_load_error=float(np.max(observed_force)), uniform_source_load_bound=float(force_bound[-1]),
                        reduction_budget=2e-7, frozen_reduction_certified_below_budget=bool(force_bound[-1]<=2e-7),
                        sampled_frozen_reduction_error_below_budget=bool(np.max(observed_force)<=2e-7),
                        retarded_error=memory_error, omitted_initial_state_position_error=maximum(homogeneous_q),
                        initial_local_frequency_min=float(data['local_frequencies'][0]), initial_local_frequency_max=float(data['local_frequencies'][-1]),
                        continuous_bound_analytical_not_interval_certified=True, freely_moving_source=False))
                    evidence.save()
        evidence.report.update(scope='Exact finite frozen-source full-feedback and current-inclusive source-load error theorem; numerical modal controls, not a freely moving force or GR pass.',
            unchanged_original_physical_runs=True, original_Gram_rows_retained=True, damping_added=False,
            prepared_data_adopted_for_physics=False, moving_source_stability_tube_certified=False,
            all_time_frozen_bound_in_exact_arithmetic=True, interval_roundoff_enclosure=False,
            old_GR_force_gates_unchanged=True, static_boundary_replacement_adopted=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
