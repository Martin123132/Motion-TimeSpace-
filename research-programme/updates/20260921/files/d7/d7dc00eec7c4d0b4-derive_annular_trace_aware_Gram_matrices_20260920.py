from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_graded_source_20260919 import GradedSourceAction
from annular_common_P2_overlay_20260919 import compose_rows
from annular_common_weighted_moments_20260920 import decimal_fraction
from annular_weak_residual_split_20260920 import combine, rational_composition
from annular_mixed_weak_maps_20260920 import MixedMap
from derive_annular_exact_source_trace_comparison_20260920 import jump_row, rational_rows, difference
from derive_annular_common_weak_action_20260920 import factor_mapping
from annular_decimal_transport_v2_20260919 import decimal_array, dot
from derive_annular_transfer_kernel_and_common_overlay_20260919 import owned_json
from run_annular_P2_continuum_bridge_20260918 import checked_load
from decimal import Decimal, localcontext
from fractions import Fraction
from scipy.sparse import csr_matrix
from time import perf_counter
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-trace-aware-Gram-matrices-attempt01', __file__)
    started = perf_counter()
    try:
        evidence.report.update(github_action=False, subagents_used=False, no_new_evolution=True,
            original_action_unchanged=True, full_live_P2_force_convergence_proven=False,
            certified_continuous_time_bound=False, physical_force_mismatch_fixed=False,
            no_singular_inverse=True, parent_coefficient_precision='binary64',
            original_Gram_factors_reproduced=False, native_action_preserving_extension_proven=False)
        evidence.report['sources'], evidence.report['pairings'] = [], []
        with localcontext() as ctx:
            ctx.prec = 64
            for branch in ['reference', 'MTS']:
                packet = owned_json(evidence, 'annular-transfer-kernel-overlay-attempt01', branch+'-exact-common-overlay.json')
                trace = owned_json(evidence, 'annular-exact-source-trace-comparison-attempt01', branch+'-exact-trace-comparison.json')
                geometry = checked_load(evidence, 'annular-common-action-weights-attempt01', branch+'-native-and-cuts.npz')
                data = [checked_load(evidence, 'annular-action-exponential-response-attempt01', branch+'-'+level+'-action.npz')
                    for level in ['coarse', 'fine']]
                models = [GradedSourceAction(257, branch == 'MTS', source_cap=2e-5),
                    GradedSourceAction(513, branch == 'MTS', source_cap=1e-5)]
                source_arrays = {}
                for level, model, item in zip(['coarse', 'fine'], models, data):
                    original = csr_matrix((item['gram_data'], item['gram_indices'], item['gram_indptr']), shape=tuple(item['gram_shape']))
                    evidence.check(branch+'_'+level+'_original_Gram_factor_reproduced_bitwise', original.shape == model.lifted.shape
                        and (original-model.lifted).nnz == 0)
                    hinge = np.maximum(model.radii-model.anchor, 0.)
                    evidence.check(branch+'_'+level+'_lifted_hinge_from_original_factor', np.array_equal(model.original @ hinge, model.lifted_hinge))
                    reconstructed = model.original-csr_matrix(model.lifted_hinge[:, None]) @ csr_matrix(model.jump[None, :])
                    evidence.check(branch+'_'+level+'_native_lifted_factor_identity', (reconstructed-original).nnz == 0)
                    source_arrays[level+'_lifted_hinge'] = model.lifted_hinge
                    source_arrays[level+'_assembled_jump'] = model.jump
                    source_arrays[level+'_radii'] = model.radii
                    evidence.report['sources'].append(dict(branch=branch, level=level, count=model.count,
                        gram_rows=original.shape[0], lifted_hinge_nonzeros=int(np.count_nonzero(model.lifted_hinge)),
                        exact_original_Gram_factor=True, valid_for_claim=False))
                embeddings = [rational_rows(rows) for rows in packet['embeddings']]
                restrictions = [rational_rows(rows) for rows in packet['left_inverses']]
                common_jump = jump_row(packet['overlay'])
                native_jump = [jump_row(mesh) for mesh in packet['native']]
                correction = [difference(common_jump, compose_rows([row], restriction)[0])
                    for row, restriction in zip(native_jump, restrictions)]
                for level, row, embedding in zip(['coarse', 'fine'], correction, embeddings):
                    evidence.check(branch+'_'+level+'_extension_native_correction_exactly_zero', compose_rows([row], embedding)[0] == {})
                evidence.check(branch+'_fine_extension_on_coarse_trial_exactly_unchanged', compose_rows([correction[1]], embeddings[0])[0] == {})
                delta_rational = compose_rows([correction[0]], embeddings[1])[0]
                expected_delta = {int(index):-Fraction(value) for index, value in trace['test_defect'].items()}
                evidence.check(branch+'_delta_is_negative_saved_test_defect', delta_rational == expected_delta)
                delta = {index:decimal_fraction(value) for index, value in delta_rational.items()}
                coarse_count, fine_count = [mesh['count'] for mesh in packet['native']]
                coarse_test = rational_composition(packet['left_inverses'][0], packet['embeddings'][1], fine_count)
                canonical_trial = rational_composition(packet['left_inverses'][1], packet['embeddings'][0], coarse_count)
                coarse_factor, fine_factor = [factor_mapping(item, 'gram') for item in data]
                hinge = decimal_array(models[0].lifted_hinge)[:, None]
                coarse_weights = decimal_array(data[0]['gram_weights'])[:, None]
                parent_row = coarse_factor.apply(coarse_weights*hinge, True)[:, 0]
                rows = [{} for unused in range(fine_count)]
                for index, value in delta.items():
                    rows[index] = {column:value*coefficient for column, coefficient in enumerate(parent_row) if coefficient}
                rank_one = MixedMap(rows, coarse_count)
                zero = MixedMap([{} for unused in range(fine_count)], coarse_count)
                old_packet = owned_json(evidence, 'annular-weak-residual-matrices-attempt01', branch+'-order64-residual-matrices.json')
                previous_order = owned_json(evidence, 'annular-weak-residual-matrices-attempt01', branch+'-order32-residual-matrices.json')
                old = old_packet['Gram_same_geometry_stencil']
                evidence.check(branch+'_Gram_channel_independent_of_moment_quadrature', old == previous_order['Gram_same_geometry_stencil'])
                original_stiffness = MixedMap(old['stiffness']['rows'], old['stiffness']['columns'])
                evidence.check(branch+'_old_Gram_channel_has_no_mass_term', all(not row for row in old['mass']['rows']))
                channels = dict(lost_test_trace=(zero, combine((-1, rank_one))),
                    trace_aware_Gram_remainder=(zero, combine((1, original_stiffness), (1, rank_one))))
                residual = combine((1, channels['lost_test_trace'][1]), (1, channels['trace_aware_Gram_remainder'][1]), (-1, original_stiffness))
                evidence.check(branch+'_two_channel_matrix_identity', max(map(abs, residual.values), default=Decimal(0)) < Decimal('1e-42'))
                for probe in range(2):
                    trial = decimal_array(np.array([[(index*7 % 17-8)/16] for index in range(coarse_count)]))
                    test = decimal_array(np.array([[(index*11 % 23-11)/32] for index in range(fine_count)]))
                    if probe:
                        test[:] = Decimal(0)
                        test[555, 0] = Decimal(1)
                    delta_test = sum((value*test[index, 0] for index, value in delta.items()), Decimal(0))
                    coarse_trial = coarse_factor.apply(trial)
                    native_test = coarse_factor.apply(coarse_test.apply(test))
                    corrected_test = native_test-hinge*delta_test
                    fine_pairing = dot(decimal_array(geometry['fine_gram_weights_at_coarse_geometry'])[:, None]*fine_factor.apply(test),
                        fine_factor.apply(canonical_trial.apply(trial)))
                    direct_lost = delta_test*dot(coarse_weights*hinge, coarse_trial)
                    direct_remainder = dot(coarse_weights*corrected_test, coarse_trial)-fine_pairing
                    for label, expected in [('lost_test_trace', direct_lost), ('trace_aware_Gram_remainder', direct_remainder)]:
                        actual = -dot(test, channels[label][1].apply(trial))
                        error = abs(actual-expected)
                        evidence.check(branch+'_'+str(probe)+'_'+label+'_independent_weighted_factors',
                            error < Decimal('1e-38')*max(Decimal(1), abs(expected)), str(error))
                        evidence.report['pairings'].append(dict(branch=branch, probe=probe, channel=label,
                            matrix_pairing=str(actual), direct_factor_pairing=str(expected), error=str(error), valid_for_claim=False))
                if branch == 'reference':
                    evidence.check('reference_both_operators_identically_zero', all(len(stiffness.values) == 0 for mass, stiffness in channels.values()))
                evidence.report['cases'].append(dict(branch=branch, fine_count=fine_count, coarse_count=coarse_count,
                    delta_nonzeros=len(delta), parent_row_nonzeros=int(np.count_nonzero(parent_row)),
                    rank_one_nonzeros=len(rank_one.values), parent_row_maximum=str(max(map(abs, parent_row), default=Decimal(0))),
                    native_actions_unchanged=True, valid_for_claim=False))
                output = evidence.output/(branch+'-trace-Gram-matrices.json')
                output.write_text(json.dumps(dict(channels={label:dict(mass=mass.serialize(), stiffness=stiffness.serialize())
                    for label, (mass, stiffness) in channels.items()}, delta={str(index):str(value) for index, value in delta_rational.items()},
                    parent_row=list(map(str, parent_row))))+'\n', encoding='utf-8')
                evidence.own(output, 'outputs')
                output = evidence.output/(branch+'-original-trace-arrays.npz')
                np.savez_compressed(output, **source_arrays)
                evidence.own(output, 'outputs')
                evidence.report['progress'] = dict(branch=branch, seconds=perf_counter()-started)
                evidence.save()
                print(json.dumps(evidence.report['progress']), flush=True)
        evidence.report.update(original_Gram_factors_reproduced=True, native_action_preserving_extension_proven=True, seconds=perf_counter()-started)
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
