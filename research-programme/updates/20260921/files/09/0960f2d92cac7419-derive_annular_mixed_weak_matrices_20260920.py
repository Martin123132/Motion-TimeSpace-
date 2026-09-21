from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_mixed_weak_maps_20260920 import assemble_mixed, stiffness_apply
from annular_common_weighted_moments_20260920 import apply_rational_rows, polynomial_products, contract
from derive_annular_common_weak_action_20260920 import dec_saved, factor_mapping
from derive_annular_commutator_riesz_bound_20260919 import mass_apply
from annular_decimal_transport_v2_20260919 import DecimalAction, DecimalMap, decimal_array, dot
from derive_annular_transfer_kernel_and_common_overlay_20260919 import owned_json
from run_annular_P2_continuum_bridge_20260918 import checked_load
from decimal import Decimal, localcontext
from scipy.sparse import csr_matrix
from time import perf_counter
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-mixed-weak-matrices-attempt01', __file__)
    started = perf_counter()
    try:
        evidence.report.update(github_action=False, subagents_used=False, no_new_evolution=True,
            original_action_unchanged=True, no_singular_inverse=True, original_physical_force_mismatch_unchanged=True,
            full_live_P2_force_convergence_proven=False, certified_continuous_time_bound=False,
            actual_time_integrated_force_decomposition_done=False, parent_coefficient_precision='binary64')
        with localcontext() as ctx:
            ctx.prec = 64
            for branch in ['reference', 'MTS']:
                packet = owned_json(evidence, 'annular-transfer-kernel-overlay-attempt01', branch+'-exact-common-overlay.json')
                data = [checked_load(evidence, 'annular-action-exponential-response-attempt01', branch+'-'+level+'-action.npz')
                    for level in ['coarse', 'fine']]
                actions = [DecimalAction(item) for item in data]
                matrices = checked_load(evidence, 'annular-action-adjoint-stability-attempt01', branch+'_final-action-matrices.npz')
                transfer = DecimalMap(csr_matrix(matrices['interpolation']))
                fields = owned_json(evidence, 'annular-common-weak-action-attempt01', branch+'-probe-fields.json')
                coarse, fine = dec_saved(fields['coarse']), dec_saved(fields['fine_canonical'])
                common_coarse = apply_rational_rows(packet['embeddings'][0], coarse)
                common_fine = apply_rational_rows(packet['embeddings'][1], fine)
                products = polynomial_products(packet['overlay'], np.column_stack([
                    common_fine[:, 0], common_coarse[:, 1], common_fine[:, 2], common_coarse[:, 3]]))
                for order in [32, 64]:
                    moments = {key: dec_saved(value) for key, value in owned_json(evidence,
                        'annular-common-weak-action-attempt01', branch+'-order'+str(order)+'-moments.json').items()}
                    maps = assemble_mixed(packet, moments, data[1])
                    for kind, first, last in [('mass', 2, 3), ('gradient', 0, 1)]:
                        actual = dot(fine[:, first:first+1], maps[kind].apply(coarse[:, last:last+1]))
                        expected = sum(contract(moments['fine_'+kind], products[kind]), Decimal(0))
                        error = abs(actual-expected)
                        evidence.check(branch+'_'+str(order)+'_'+kind+'_independent_field_moment_pairing',
                            error < Decimal('1e-40')*max(Decimal(1), abs(expected)), str(error))
                    fine_factor = factor_mapping(data[1], 'gram')
                    expected = dot(decimal_array(data[1]['gram_weights'])[:, None]*fine_factor.apply(fine[:, :1]),
                        fine_factor.apply(fine[:, 1:2]))
                    actual = dot(fine[:, :1], maps['gram'].apply(coarse[:, 1:2]))
                    evidence.check(branch+'_'+str(order)+'_original_Gram_extension', abs(actual-expected) < Decimal('1e-40'))
                    fixture_coarse = decimal_array(np.array([[(index*7 % 17-8)/16] for index in range(actions[0].count)]))
                    fixture_fine = decimal_array(np.array([[(index*11 % 23-11)/32] for index in range(actions[1].count)]))
                    for kind, mapping in maps.items():
                        error = abs(dot(fixture_fine, mapping.apply(fixture_coarse))
                            -dot(mapping.apply(fixture_fine, True), fixture_coarse))
                        evidence.check(branch+'_'+str(order)+'_'+kind+'_transpose_pairing', error < Decimal('1e-40'), str(error))
                    for label, values in [('initial_position', coarse[:, 1:2]), ('all_modes_fixture', fixture_coarse)]:
                        acceleration = actions[0].acceleration(values)
                        old = mass_apply(actions[1], transfer.apply(acceleration))-actions[1].stiffness(transfer.apply(values))
                        mass_term = mass_apply(actions[1], transfer.apply(acceleration))-maps['mass'].apply(acceleration)
                        stiffness_term = stiffness_apply(maps, values)-actions[1].stiffness(transfer.apply(values))
                        weak_term = maps['mass'].apply(acceleration)-stiffness_apply(maps, values)
                        error = max(map(abs, (mass_term+stiffness_term+weak_term-old).flat))
                        evidence.check(branch+'_'+str(order)+'_'+label+'_rank_safe_operator_identity',
                            error < Decimal('1e-38')*max(Decimal(1), max(map(abs, old.flat))), str(error))
                    output = evidence.output/(branch+'-order'+str(order)+'-mixed-matrices.json')
                    output.write_text(json.dumps({name: mapping.serialize() for name, mapping in maps.items()})+'\n', encoding='utf-8')
                    evidence.own(output, 'outputs')
                    evidence.report['cases'].append(dict(branch=branch, order=order, fine_dofs=actions[1].count,
                        coarse_dofs=actions[0].count, nonzeros={name:len(mapping.values) for name, mapping in maps.items()},
                        valid_for_claim=False))
                evidence.report['progress'] = dict(branch=branch, seconds=perf_counter()-started)
                evidence.save()
                print(json.dumps(evidence.report['progress']), flush=True)
        evidence.report['seconds'] = perf_counter()-started
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
