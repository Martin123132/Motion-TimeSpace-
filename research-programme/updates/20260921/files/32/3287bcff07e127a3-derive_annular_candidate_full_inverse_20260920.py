from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_full_inverse_20260920 import QuadratureCache, FullMomentumMap, BandedSourceInverse, canonical_inverse
from annular_candidate_canonical_response_20260920 import common_material, restored_solver
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from run_annular_P2_continuum_bridge_20260918 import checked_load
from derive_annular_transfer_kernel_and_common_overlay_20260919 import owned_json
from scipy.sparse import save_npz
from time import perf_counter
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-candidate-full-canonical-inverse-attempt01', __file__)
    started = perf_counter()
    deadline = started+10800
    try:
        evidence.report.update(github_action=False, subagents_used=False, candidate_only=True,
            polar_zero_shift_only=True, original_live_action_unchanged=True, no_new_evolution=True,
            new_coupled_evolution=False, initial_physical_time=0., fixed_coordinates_only=True,
            target_momenta_action_owned=True, original_unweighted_momenta_reused=False,
            full_canonical_inverse_qualified=False, global_canonical_inverse_proven=False,
            all_mode_reduced_inertia_positive_proven=False, modes_deleted=False,
            general_nonzero_shift_or_temporal_current_derived=False,
            physical_force_mismatch_fixed=False, spatial_convergence_proven=False,
            full_live_P2_force_convergence_proven=False,
            canonical_inverse_scope='Numerical fixed-coordinate full-component solves near the coherent initial state; not a global existence or uniqueness theorem.',
            preconditioners=[], controls=[], iterations=[], rejected_trials=[], refinement=[],
            cache_budget_bytes=512*1024**2)
        prior_path = evidence.output.parent/'annular-candidate-canonical-response-final-integrity.json'
        prior = json.loads(prior_path.read_text())
        evidence.own(prior_path)
        evidence.check('preceding_momentum_response_complete', prior['state'] == 'complete'
            and prior['candidate_momenta_computed'] and not prior['full_GR_limit_proven'])
        np.random.seed(20260920)
        for branch in ['reference', 'MTS']:
            native = IndexedGradedP2System(257, branch == 'MTS', 2e-5)
            saved = checked_load(evidence, 'annular-candidate-initial-metric-attempt02', branch+'-velocity-owned-inputs.npz')
            mesh = owned_json(evidence, 'annular-transfer-kernel-overlay-attempt01', branch+'-exact-common-overlay.json')
            owner, coordinates, known_rates = common_material(native, saved, mesh)
            previous_inputs = checked_load(evidence, 'annular-candidate-live-momenta-attempt01', branch+'-common-inputs.npz')
            evidence.check(branch+'_same_coherent_coordinates_and_known_velocities',
                np.array_equal(coordinates, previous_inputs['coordinates'])
                and np.array_equal(known_rates, previous_inputs['rates']))
            rng = np.random.default_rng(20260920)
            perturbations = []
            for unused in range(2):
                perturbation = .0015*rng.standard_normal(known_rates.shape)
                perturbation[:, -1] = .006*rng.standard_normal(len(owner.labels))
                perturbations.append(perturbation)
            shift_velocity = .0001*rng.standard_normal(known_rates.shape)
            shift_velocity[:, -1] = .0003*rng.standard_normal(len(owner.labels))
            previous_solutions = {}
            extensions = ['reference'] if branch == 'reference' else ['primary', 'alternative']
            for degree, label_order in [(18, 20), (22, 28)]:
                density = checked_load(evidence, 'annular-candidate-initial-metric-attempt02',
                    branch+'-radial'+str(degree)+'-density.npz')
                solver = restored_solver(owner, density, degree)
                solver.label_order = label_order
                common_density = checked_load(evidence, 'annular-candidate-live-momenta-attempt01',
                    branch+'-'+str(degree)+'-density-response.npz')
                for name in ['temporal_square', 'gradient_square', 'source_density', 'velocity']:
                    solver.fields[name] = common_density[name].copy()
                evidence.report['progress'] = dict(branch=branch, radial_degree=degree,
                    operation='cache_fixed_coordinate_quadrature', seconds=perf_counter()-started)
                evidence.save()
                print(json.dumps(evidence.report['progress']), flush=True)
                cache = QuadratureCache(owner, coordinates, solver, deadline)
                evidence.check(branch+'_'+str(degree)+'_bounded_quadrature_cache', cache.bytes <= cache.budget,
                    dict(bytes=cache.bytes, cached_radial_nodes=cache.prefix, total_radial_nodes=len(cache.radius)))
                mapping = FullMomentumMap(owner, coordinates, solver, cache)
                for extension in extensions:
                    label = branch+'-'+extension+'-'+str(degree)
                    canonical = checked_load(evidence, 'annular-candidate-live-momenta-attempt01', label+'-canonical.npz')
                    target = canonical['momentum']
                    initial = known_rates+perturbations[0]
                    evidence.check(label+'_all_components_perturbed', np.count_nonzero(initial-known_rates) == known_rates.size)
                    evidence.report['progress'] = dict(case=label, operation='assemble_full_fixed_metric_preconditioner_from_perturbed_state',
                        seconds=perf_counter()-started)
                    evidence.save()
                    print(json.dumps(evidence.report['progress']), flush=True)
                    initial_evaluation = mapping.evaluate(initial, extension, assemble=True)
                    preconditioner = BandedSourceInverse(initial_evaluation['normal'], known_rates.shape)
                    matrix_path = evidence.output/(label+'-fixed-metric-mass.npz')
                    save_npz(matrix_path, preconditioner.matrix)
                    evidence.own(matrix_path, 'outputs')
                    factor_path = evidence.output/(label+'-preconditioner.npz')
                    np.savez_compressed(factor_path, bands=preconditioner.bands, factor=preconditioner.factor,
                        cross=preconditioner.cross, field_cross=preconditioner.field_cross,
                        source=preconditioner.source, schur=preconditioner.schur, scale=preconditioner.scale,
                        permutation=preconditioner.permutation, initial_rates=initial,
                        initial_metric=initial_evaluation['solution']['state'])
                    evidence.own(factor_path, 'outputs')
                    raw_condition, scaled_condition = preconditioner.condition_estimates()
                    field_extent = max(max(index for index in element if index >= 0)
                        -min(index for index in element if index >= 0) for element in owner.model.element_indices)
                    evidence.check(label+'_all_field_and_source_pivots_positive', preconditioner.minimum_field_cholesky_pivot > 0
                        and preconditioner.minimum_schur_eigenvalue > 0 and preconditioner.minimum_diagonal > 0)
                    evidence.check(label+'_derived_field_material_bandwidth', field_extent <= 2 and preconditioner.bandwidth == 44)
                    probes = rng.standard_normal((known_rates.size, 3))
                    rhs = preconditioner.matrix @ probes
                    recovered_probes = preconditioner.solve(rhs)
                    recovery_error = float(np.max(abs(recovered_probes-probes))/np.max(abs(probes)))
                    residual_error = float(np.linalg.norm(preconditioner.matrix @ recovered_probes-rhs)/np.linalg.norm(rhs))
                    evidence.check(label+'_full_preconditioner_solve_control', recovery_error < 2e-9 and residual_error < 2e-11,
                        dict(recovery_relative=recovery_error, residual_relative=residual_error))
                    direction = probes[:, 0].reshape(known_rates.shape)
                    independent, unused = mapping.fixed_momentum(initial.astype(complex)+1e-25j*direction,
                        initial_evaluation['solution']['state'])
                    expected = preconditioner.matrix @ direction.ravel()
                    derivative_error = float(np.max(abs(independent.ravel().imag/1e-25-expected))/np.max(abs(expected)))
                    evidence.check(label+'_independent_full_fixed_momentum_Jacobian', derivative_error < 2e-10, derivative_error)
                    evidence.report['controls'].append(dict(branch=branch, extension=extension, radial_degree=degree,
                        preconditioner_recovery_relative_error=recovery_error,
                        preconditioner_residual_relative_error=residual_error,
                        fixed_momentum_Jacobian_relative_error=derivative_error, valid_for_claim=False))
                    evidence.report['preconditioners'].append(dict(branch=branch, extension=extension, radial_degree=degree,
                        full_components=known_rates.size, field_components=preconditioner.field_count,
                        source_components=len(owner.labels), field_half_bandwidth=preconditioner.bandwidth,
                        symmetry_error=preconditioner.symmetry_error,
                        minimum_diagonal=preconditioner.minimum_diagonal, maximum_diagonal=preconditioner.maximum_diagonal,
                        minimum_scaled_field_cholesky_pivot=preconditioner.minimum_field_cholesky_pivot,
                        minimum_scaled_source_schur_eigenvalue=preconditioner.minimum_schur_eigenvalue,
                        raw_one_norm_condition_estimate=raw_condition, scaled_one_norm_condition_estimate=scaled_condition,
                        condition_estimates_not_upper_bounds=True, cache_bytes=cache.bytes,
                        constructed_from_perturbed_not_known_solution=True, valid_for_claim=False))
                    seeds = [('roundtrip_1', target, known_rates+perturbations[0]),
                        ('roundtrip_2', target, known_rates+perturbations[1])]
                    if degree == 22:
                        shifted = target+(preconditioner.matrix @ shift_velocity.ravel()).reshape(known_rates.shape)
                        seeds.append(('shifted_target', shifted, known_rates+perturbations[1]))
                    for seed_index, (seed_name, requested, seed) in enumerate(seeds):
                        case = label+'-'+seed_name
                        evidence.report['progress'] = dict(case=case, operation='full_component_canonical_inverse',
                            seconds=perf_counter()-started)
                        evidence.save()
                        print(json.dumps(evidence.report['progress']), flush=True)

                        def on_step(row):
                            evidence.report['iterations'].append(dict(case=case, **row, valid_for_claim=False))
                            evidence.report['progress'] = dict(case=case, operation='canonical_iteration',
                                iteration=row['iteration'], relative_residual=row['momentum_relative_residual'],
                                correction=row['maximum_preconditioned_correction'], seconds=perf_counter()-started)
                            evidence.save()
                            print(json.dumps(evidence.report['progress']), flush=True)

                        recovered, final, history, rejected = canonical_inverse(mapping, requested, seed, extension,
                            preconditioner, initial_evaluation if seed_index == 0 else None, on_step)
                        maximum_velocity_difference = float(np.max(abs(recovered-known_rates)))
                        momentum_scale = max(preconditioner.residual_norm(requested), 1e-30)
                        final_residual = preconditioner.residual_norm(final['momentum']-requested)/momentum_scale
                        final_correction = float(np.max(abs(preconditioner.solve((final['momentum']-requested).ravel()))))
                        evidence.check(case+'_all_momenta_and_radial_constraints',
                            final_residual < 2e-11 and final_correction < 2e-10
                            and final['solution']['maximum_residual'] < 2e-12,
                            dict(relative_residual=final_residual, correction=final_correction,
                                radial=final['solution']['maximum_residual']))
                        if seed_name.startswith('roundtrip'):
                            evidence.check(case+'_known_velocity_recovered_all_components', maximum_velocity_difference < 2e-9,
                                maximum_velocity_difference)
                            if degree == 18 and seed_name == 'roundtrip_1':
                                previous_solutions[extension] = recovered
                            if degree == 22 and seed_name == 'roundtrip_1':
                                change = float(np.max(abs(recovered-previous_solutions[extension])))
                                evidence.check(case+'_joint_quadrature_roundtrip_consistency', change < 2e-9, change)
                                evidence.report['refinement'].append(dict(branch=branch, extension=extension,
                                    maximum_roundtrip_velocity_difference=change,
                                    targets_use_their_own_quadrature=True,
                                    not_physical_spatial_or_evolution_convergence=True, valid_for_claim=False))
                        else:
                            target_change = preconditioner.residual_norm(requested-target)/max(
                                preconditioner.residual_norm(target), 1e-30)
                            evidence.check(case+'_independently_shifted_target_is_nontrivial',
                                maximum_velocity_difference > 1e-6 and target_change > 1e-4,
                                dict(velocity_change=maximum_velocity_difference, target_change=target_change))
                        evidence.check(case+'_timelike_untrapped_solution',
                            final['minimum_F'] > 0 and final['maximum_speed_ratio'] < 1)
                        output = evidence.output/(case+'-recovery.npz')
                        np.savez_compressed(output, target=requested, seed=seed, recovered=recovered, known=known_rates,
                            momentum=final['momentum'], metric=final['solution']['state'])
                        evidence.own(output, 'outputs')
                        for row in rejected:
                            evidence.report['rejected_trials'].append(dict(case=case, **row, valid_for_claim=False))
                        row = dict(branch=branch, extension=extension, radial_degree=degree, label_order=label_order,
                            seed=seed_name, full_components=known_rates.size, residual_evaluations=len(history),
                            rejected_trials=len(rejected), relative_momentum_residual=final_residual,
                            maximum_correction=final_correction, radial_residual=final['solution']['maximum_residual'],
                            maximum_velocity_difference_from_known=maximum_velocity_difference,
                            roundtrip=seed_name.startswith('roundtrip'), all_components_solved=True,
                            minimum_F=final['minimum_F'], maximum_speed_ratio=final['maximum_speed_ratio'],
                            fixed_coordinates_only=True, valid_for_claim=False)
                        evidence.report['cases'].append(row)
                        evidence.save()
                        print(json.dumps(dict(case=case, operation='case_complete', **{
                            key:row[key] for key in ['relative_momentum_residual', 'maximum_velocity_difference_from_known']},
                            seconds=perf_counter()-started)), flush=True)
                    del initial_evaluation, preconditioner
                del cache, mapping
        evidence.report.update(full_canonical_inverse_qualified=True, full_component_inverse_numerically_qualified=True,
            perturbed_momentum_targets_solved=True, seconds=perf_counter()-started)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), seconds=perf_counter()-started)), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()

