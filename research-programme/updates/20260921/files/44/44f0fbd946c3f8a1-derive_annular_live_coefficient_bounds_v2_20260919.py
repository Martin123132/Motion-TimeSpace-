from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_force_coefficient_bounds_20260919 import off_space_peano, kinetic_weights, geometry_pairing
from derive_annular_Gram_two_trace_force_law_20260919 import trace_force_data
from derive_annular_spatial_Gram_defect_split_20260919 import state_pair
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-live-coefficient-bounds-attempt02', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, full_live_P2_force_convergence_proven=False,
            no_new_evolution=True, all_Gram_rows_retained=True, full_geometry_reconstructed=True,
            ordinary_gradient_jumps_retained=True, geometry_response_defect_retained=True,
            instantaneous_field_driver_not_total_time_derivative=True,
            full_nonlinear_stability_proven=False, hierarchy_not_continuum_error=True)
        failed_path = evidence.output.parent/'annular-live-coefficient-bounds-attempt01/status.json'
        failed = json.loads(failed_path.read_text())
        evidence.own(failed_path)
        evidence.check('empty_reference_reduction_failure_preserved', failed['state'] == 'failed')
        previous = {}
        for name in ['annular-coefficient-geometry-algebra-attempt01', 'annular-Gram-two-trace-force-law-attempt01']:
            path = evidence.output.parent/name/'status.json'
            status = json.loads(path.read_text())
            evidence.own(path)
            evidence.check(name+'_complete', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
            previous[name] = status
        for branch in ['reference', 'MTS']:
            coarse_system = IndexedGradedP2System(257, branch == 'MTS', 2e-5)
            fine_system = IndexedGradedP2System(513, branch == 'MTS', 1e-5)
            center = int(np.argmin(abs(coarse_system.labels)))
            label = coarse_system.labels[center]
            for final in [False, True]:
                coarse_state, fine_state = state_pair(evidence, branch, final)
                coarse_rates, coarse_geometry = coarse_system.solve(*coarse_state)
                fine_rates, fine_geometry = fine_system.solve(*fine_state)
                coarse_values, fine_values = coarse_state[0, center], fine_state[0, center]
                fine_layer = fine_system.layer(label, fine_geometry)
                coarse_geometry_layer = fine_system.layer(label, coarse_geometry)
                actual = trace_force_data(fine_layer, fine_system.model, fine_values, fine_values[-1])
                off_coarse = trace_force_data(fine_layer, coarse_system.model, coarse_values, fine_values[-1])
                old_geometry = trace_force_data(coarse_geometry_layer, coarse_system.model, coarse_values, coarse_values[-1])
                fine_split = off_space_peano(fine_layer, fine_system.model, fine_values[:-1])
                coarse_split = off_space_peano(fine_layer, coarse_system.model, coarse_values[:-1])
                instant = 4e-5 if final else 0.
                tag = branch+('_final' if final else '_initial')
                for name, split in [('fine', fine_split), ('coarse', coarse_split)]:
                    error = abs(split['actual']-split['regular']-split['ordinary_jumps']-split['polynomial_moments'])
                    evidence.check(tag+'_'+name+'_off_space_Peano_reconstructs', np.all(error <= split['tolerance']),
                        dict(maximum_error=float(np.max(error, initial=0.)), maximum_tolerance=float(np.max(split['tolerance'], initial=0.))))
                difference = actual[0]['factor']-off_coarse[0]['factor']
                regular = fine_split['regular']-coarse_split['regular']
                jumps = fine_split['ordinary_jumps']-coarse_split['ordinary_jumps']
                moments = fine_split['polynomial_moments']-coarse_split['polynomial_moments']
                tolerance = fine_split['tolerance']+coarse_split['tolerance']
                rates_indices, rates_shape, unused = coarse_system.model.features_quadratic(fine_layer.radii)
                coarse_rate_samples = np.sum(rates_shape*coarse_rates[center, :-1][rates_indices], axis=1)
                fine_rate_factor = fine_layer.lifted @ fine_rates[center, :-1]
                coarse_rate_factor = (fine_layer.original @ coarse_rate_samples
                    -fine_layer.lifted_hinge*(coarse_system.model.jump @ coarse_rates[center, :-1]))
                rate_difference = fine_rate_factor-coarse_rate_factor
                mean_trace = (actual[2]+off_coarse[2])/2
                responses = actual[1]['response']
                targets = dict(left=responses[:, 0], right=responses[:, 1], trace_weighted=responses @ mean_trace)
                prior = next(case for case in previous['annular-Gram-two-trace-force-law-attempt01']['cases']
                    if case['branch'] == branch and case['time'] == instant)
                rows, geometry_rows = [], []
                arrays = dict(field_factor_difference=difference, regular_difference=regular, ordinary_jump_difference=jumps,
                    polynomial_moment_difference=moments, Peano_tolerance=tolerance, field_rate_difference=rate_difference)
                for partition in ['all_rows', 'source_straddling', 'remaining']:
                    mask = np.ones(len(difference), dtype=bool) if partition == 'all_rows' else actual[0]['source_rows']
                    if partition == 'remaining':
                        mask = ~mask
                    previous_part = next(row for row in prior['partitions'] if row['comparison'] == 'field_without_nodal_transfer'
                        and row['partition'] == partition)
                    for name, target in targets.items():
                        response_factor = fine_layer.lifted @ target
                        weighted = mask*actual[0]['weights']*response_factor
                        measured = float(weighted @ difference)
                        row_bound = float(abs(weighted) @ abs(difference))
                        energy_bound = float(np.sqrt(np.sum(mask*actual[0]['weights']*difference**2))
                            *np.sqrt(np.sum(mask*actual[0]['weights']*response_factor**2)))
                        curvature_term, jump_term, moment_term = [float(weighted @ value) for value in [regular, jumps, moments]]
                        reconstruction_tolerance = float(abs(weighted) @ tolerance)
                        expected_key = 'trace_response_coefficient_channel' if name == 'trace_weighted' else 'coefficient_change_'+name
                        expected = previous_part[expected_key]
                        check_tag = tag+'_'+partition+'_'+name
                        evidence.check(check_tag+'_coefficient_and_two_bounds', abs(measured-expected) < 3e-15
                            and abs(measured) <= row_bound+3e-20 and abs(measured) <= energy_bound+3e-20)
                        reconstruction_error = abs(measured-curvature_term-jump_term-moment_term)
                        evidence.check(check_tag+'_Peano_channels_retained', reconstruction_error <= reconstruction_tolerance+3e-20,
                            dict(error=reconstruction_error, arithmetic_tolerance=reconstruction_tolerance))
                        rows.append(dict(partition=partition, functional=name, coefficient_channel=measured,
                            rowwise_absolute_bound=row_bound, weighted_energy_bound=energy_bound,
                            curvature_channel=curvature_term, ordinary_jump_channel=jump_term, polynomial_moment_channel=moment_term,
                            separated_Peano_absolute_bound=float(abs(weighted) @ (abs(regular)+abs(jumps)+abs(moments))),
                            Peano_reconstruction_error=reconstruction_error, Peano_arithmetic_tolerance=reconstruction_tolerance,
                            instantaneous_fixed_geometry_field_driver=float(weighted @ rate_difference),
                            fixed_geometry_field_driver_absolute_bound=float(abs(weighted) @ abs(rate_difference)),
                            bound_over_absolute_channel=row_bound/abs(measured) if measured != 0 else None,
                            valid_for_claim=False))
                        arrays[partition+'_'+name+'_row_terms'] = weighted*difference
                    first_weights = kinetic_weights(coarse_geometry_layer, coarse_values[-1])
                    last_weights = kinetic_weights(fine_layer, fine_values[-1])
                    geometry, geometry_arrays = geometry_pairing(fine_layer, old_geometry[0], off_coarse[0],
                        old_geometry[1], off_coarse[1], first_weights, last_weights, off_coarse[0]['factor'], mask)
                    evidence.check(tag+'_'+partition+'_geometry_comparison_holds_field_fixed',
                        np.array_equal(old_geometry[0]['factor'], off_coarse[0]['factor']))
                    for item in geometry:
                        error = abs(item['coefficient_change']-item['mass_response_pairing']-item['gram_weight_pairing'])
                        evidence.check(tag+'_'+partition+'_geometry_side'+str(item['side'])+'_identity_and_bounds',
                            item['response_identity_maximum_error'] < 3e-13 and error < 3e-15
                            and abs(item['mass_response_pairing']) <= item['weighted_projection_defect_bound']+3e-20)
                        geometry_rows.append(dict(partition=partition, **item, coefficient_identity_error=error,
                            change_exceeds_ten_reconstruction_errors=abs(item['coefficient_change']) > 10*error))
                    arrays.update({partition+'_'+name:value for name, value in geometry_arrays.items()})
                evidence.report['cases'].append(dict(branch=branch, time=instant, field_rows=rows, geometry_rows=geometry_rows,
                    maximum_nodal_field_difference=float(max(abs(actual[0]['samples']-off_coarse[0]['samples']))), valid_for_claim=False))
                path = evidence.output/(tag+'-coefficient-bounds.npz')
                np.savez_compressed(path, **arrays)
                evidence.own(path, 'outputs')
                evidence.save()
                print(json.dumps(dict(case=tag, total=[row for row in rows if row['partition'] == 'all_rows'
                    and row['functional'] == 'trace_weighted'], geometry_total=[row for row in geometry_rows if row['partition'] == 'all_rows'])), flush=True)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']))), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
