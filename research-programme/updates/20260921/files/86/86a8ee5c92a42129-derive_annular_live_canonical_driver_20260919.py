from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_canonical_driver_residual_20260919 import canonical_residual_split, driver_pairing
from derive_annular_Gram_two_trace_force_law_20260919 import trace_force_data
from derive_annular_spatial_Gram_defect_split_20260919 import state_pair
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-live-canonical-driver-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, full_live_P2_force_convergence_proven=False,
            no_new_evolution=True, full_geometry_reconstructed=True, all_Gram_rows_retained=True,
            both_inverse_momentum_residuals_retained=True, nonnested_transfer_jump_retained=True,
            momentum_covectors_not_nodally_interpolated=True, instantaneous_driver_not_total_force_rate=True,
            hierarchy_not_continuum_error=True, full_nonlinear_stability_proven=False)
        previous = {}
        for name in ['annular-canonical-driver-algebra-attempt01', 'annular-live-coefficient-bounds-attempt02']:
            path = evidence.output.parent/name/'status.json'
            status = json.loads(path.read_text())
            evidence.own(path)
            evidence.check(name+'_complete', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
            previous[name] = status
        for branch in ['reference', 'MTS']:
            coarse_system = IndexedGradedP2System(257, branch == 'MTS', 2e-5)
            fine_system = IndexedGradedP2System(513, branch == 'MTS', 1e-5)
            center = int(np.argmin(abs(fine_system.labels)))
            label = fine_system.labels[center]
            for final in [False, True]:
                coarse_state, fine_state = state_pair(evidence, branch, final)
                coarse_rates, coarse_geometry = coarse_system.solve(*coarse_state)
                fine_rates, fine_geometry = fine_system.solve(*fine_state)
                coarse_values, fine_values = coarse_state[0, center], fine_state[0, center]
                coarse_layer, fine_layer = coarse_system.layer(label, coarse_geometry), fine_system.layer(label, fine_geometry)
                coarse = coarse_layer.evaluate(0., coarse_values, coarse_rates[center])
                fine = fine_layer.evaluate(0., fine_values, fine_rates[center])
                indices, shape, unused = coarse_system.model.features_quadratic(fine_layer.radii)

                def transfer(values):
                    return np.sum(shape*values[indices], axis=1)

                split = canonical_residual_split(coarse, fine, coarse_state[1, center, :-1], fine_state[1, center, :-1],
                    coarse_rates[center], fine_rates[center], transfer)
                actual = trace_force_data(fine_layer, fine_system.model, fine_values, fine_values[-1])
                off_coarse = trace_force_data(fine_layer, coarse_system.model, coarse_values, fine_values[-1])
                mean_trace = (actual[2]+off_coarse[2])/2
                responses = actual[1]['response']
                targets = dict(left=responses[:, 0], right=responses[:, 1], trace_weighted=responses @ mean_trace)
                velocity_transferred = transfer(coarse_rates[center, :-1])
                jump_defect = float(coarse_system.model.jump @ coarse_rates[center, :-1]-fine_layer.jump @ velocity_transferred)
                direct_factor_rate = (fine_layer.lifted @ fine_rates[center, :-1]-fine_layer.original @ velocity_transferred
                    +fine_layer.lifted_hinge*(coarse_system.model.jump @ coarse_rates[center, :-1]))
                instant = 4e-5 if final else 0.
                old = next(case for case in previous['annular-live-coefficient-bounds-attempt02']['cases']
                    if case['branch'] == branch and case['time'] == instant)
                tag = branch+('_final' if final else '_initial')
                evidence.check(tag+'_mass_residual_velocity_reconstruction', split['velocity_reconstruction_error'] < 3e-12
                    and split['load_split_error'] < 3e-12, dict(velocity=split['velocity_reconstruction_error'], load=split['load_split_error']))
                rows, arrays = [], {name:value for name, value in split.items() if isinstance(value, np.ndarray)}
                arrays.update(fine_mass_bands=fine['mass_bands'], coarse_mass_bands=coarse['mass_bands'],
                    fine_scalar_velocity=fine_rates[center, :-1], coarse_scalar_velocity=coarse_rates[center, :-1],
                    direct_factor_rate=direct_factor_rate, jump_defect=jump_defect)
                for partition in ['all_rows', 'source_straddling', 'remaining']:
                    mask = np.ones(len(actual[0]['factor']), dtype=bool) if partition == 'all_rows' else actual[0]['source_rows']
                    if partition == 'remaining':
                        mask = ~mask
                    for name, target in targets.items():
                        row_covector = mask*actual[0]['weights']*(fine_layer.lifted @ target)
                        covector = np.asarray(fine_layer.lifted.T @ row_covector).ravel()
                        result, dual = driver_pairing(fine['mass_bands'], split, covector)
                        jump_channel = float((row_covector @ fine_layer.lifted_hinge)*jump_defect)
                        direct = float(row_covector @ direct_factor_rate)
                        component_names = ['momentum_channel', 'source_cross_channel', 'coarse_inverse_channel', 'fine_inverse_channel']
                        channel_sum = sum(result[key] for key in component_names)+jump_channel
                        cancellation_scale = sum(abs(result[key]) for key in component_names)+abs(jump_channel)
                        tolerance = 3e-10*max(abs(direct), cancellation_scale, 1e-9)+3e-11
                        expected = next(row for row in old['field_rows'] if row['functional'] == name and row['partition'] == partition)
                        check_tag = tag+'_'+partition+'_'+name
                        error = abs(direct-channel_sum)
                        evidence.check(check_tag+'_five_channel_identity_and_saved_driver', error <= tolerance
                            and abs(direct-result['residual_pairing']-jump_channel) <= tolerance
                            and abs(direct-expected['instantaneous_fixed_geometry_field_driver']) <= tolerance,
                            dict(error=error, numerical_tolerance=tolerance))
                        local_bound = result['corrected_residual_localized_bound']+abs(jump_channel)
                        mass_bound = result['corrected_residual_mass_bound']+abs(jump_channel)
                        evidence.check(check_tag+'_both_total_driver_bounds', abs(direct) <= local_bound+tolerance
                            and abs(direct) <= mass_bound+tolerance)
                        near = abs(fine_layer.radii-fine_layer.anchor) <= 2*coarse_layer.source_cap
                        terms = dual*split['corrected_load']
                        rows.append(dict(partition=partition, functional=name, **result,
                            interpolation_jump_channel=jump_channel, direct_driver=direct,
                            total_localized_bound=local_bound, total_mass_bound=mass_bound,
                            near_source_residual_pairing=float(np.sum(terms[near])),
                            far_source_residual_pairing=float(np.sum(terms[~near])),
                            near_source_residual_absolute_bound=float(np.sum(abs(terms[near]))),
                            far_source_residual_absolute_bound=float(np.sum(abs(terms[~near]))),
                            component_cancellation_scale=cancellation_scale, five_channel_reconstruction_error=error,
                            numerical_control_tolerance=tolerance,
                            bound_over_absolute_driver=local_bound/abs(direct) if direct != 0 else None))
                        arrays[partition+'_'+name+'_dual'] = dual
                        arrays[partition+'_'+name+'_corrected_residual_terms'] = terms
                evidence.report['cases'].append(dict(branch=branch, time=instant, rows=rows,
                    fine_source_velocity=float(fine_rates[center, -1]), coarse_source_velocity=float(coarse_rates[center, -1]),
                    transfer_jump_defect=jump_defect, inverse_momentum_residual_maximum=split['maximum_inverse_residual'],
                    velocity_reconstruction_error=split['velocity_reconstruction_error'], valid_for_claim=False))
                path = evidence.output/(tag+'-canonical-driver.npz')
                np.savez_compressed(path, **arrays)
                evidence.own(path, 'outputs')
                evidence.save()
                print(json.dumps(dict(case=tag, total=[row for row in rows if row['partition'] == 'all_rows'
                    and row['functional'] == 'trace_weighted'])), flush=True)
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
