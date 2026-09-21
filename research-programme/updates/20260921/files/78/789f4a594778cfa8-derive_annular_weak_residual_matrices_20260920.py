from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_weak_residual_split_20260920 import build_split
from annular_mixed_weak_maps_20260920 import MixedMap, stiffness_apply
from annular_common_weighted_moments_20260920 import apply_rational_rows, polynomial_products, contract
from derive_annular_common_weak_action_20260920 import dec_saved, factor_mapping
from derive_annular_commutator_riesz_bound_20260919 import mass_apply
from annular_decimal_transport_v2_20260919 import DecimalAction, decimal_array, dot
from derive_annular_transfer_kernel_and_common_overlay_20260919 import owned_json
from run_annular_P2_continuum_bridge_20260918 import checked_load
from decimal import Decimal, localcontext
from time import perf_counter
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-weak-residual-matrices-attempt01', __file__)
    started = perf_counter()
    try:
        evidence.report.update(github_action=False, subagents_used=False, no_new_evolution=True,
            original_action_unchanged=True, full_live_P2_force_convergence_proven=False,
            certified_continuous_time_bound=False, physical_force_mismatch_fixed=False,
            no_singular_inverse=True, unresolved_test_Gram_zero_qualified=False,
            parent_coefficient_precision='binary64')
        evidence.report['pairings'] = []
        with localcontext() as ctx:
            ctx.prec = 64
            for branch in ['reference', 'MTS']:
                packet = owned_json(evidence, 'annular-transfer-kernel-overlay-attempt01', branch+'-exact-common-overlay.json')
                data = [checked_load(evidence, 'annular-action-exponential-response-attempt01', branch+'-'+level+'-action.npz')
                    for level in ['coarse', 'fine']]
                geometry = checked_load(evidence, 'annular-common-action-weights-attempt01', branch+'-native-and-cuts.npz')
                action = DecimalAction(data[0])
                count_fine = packet['native'][1]['count']
                trial = decimal_array(np.array([[(index*7 % 17-8)/16] for index in range(action.count)]))
                test = decimal_array(np.array([[(index*11 % 23-11)/32] for index in range(count_fine)]))
                acceleration = action.acceleration(trial)
                for order in [32, 64]:
                    moments = {key:dec_saved(value) for key, value in owned_json(evidence,
                        'annular-common-weak-action-attempt01', branch+'-order'+str(order)+'-moments.json').items()}
                    mixed_packet = owned_json(evidence, 'annular-mixed-weak-matrices-attempt01', branch+'-order'+str(order)+'-mixed-matrices.json')
                    fine_maps = {name:MixedMap(item['rows'], item['columns']) for name, item in mixed_packet.items()}
                    channels, auxiliary = build_split(packet, moments, action, data[0], data[1],
                        geometry['fine_gram_weights_at_coarse_geometry'], fine_maps)
                    coarse_test = auxiliary['coarse_test'].apply(test)
                    common_test = apply_rational_rows(packet['embeddings'][1], test)
                    residual_test = common_test-apply_rational_rows(packet['embeddings'][0], coarse_test)
                    common_trial = apply_rational_rows(packet['embeddings'][0], trial)
                    common_acceleration = apply_rational_rows(packet['embeddings'][0], acceleration)
                    restricted = apply_rational_rows(packet['left_inverses'][0], residual_test)
                    evidence.check(branch+'_'+str(order)+'_unresolved_test_zero_coarse_nodes',
                        max(map(abs, restricted.flat)) < Decimal('1e-54'))
                    evidence.check(branch+'_'+str(order)+'_unresolved_test_original_coarse_Gram_zero',
                        max(map(abs, factor_mapping(data[0], 'gram').apply(restricted).flat), default=Decimal(0)) < Decimal('1e-42'))
                    expected = {}
                    residual_products = polynomial_products(packet['overlay'], np.column_stack([
                        residual_test, common_trial, residual_test, common_acceleration]))
                    common_products = polynomial_products(packet['overlay'], np.column_stack([
                        common_test, common_trial, common_test, common_acceleration]))
                    expected['unresolved_finer_test'] = sum(contract(moments['coarse_mass'], residual_products['mass'])
                        -contract(moments['coarse_gradient'], residual_products['gradient']), Decimal(0))
                    expected['mass_gradient_geometry'] = sum(contract(moments['fine_mass']-moments['coarse_mass'], common_products['mass'])
                        -contract(moments['fine_gradient']-moments['coarse_gradient'], common_products['gradient']), Decimal(0))
                    coarse_projection = apply_rational_rows(packet['embeddings'][0], coarse_test)
                    projection_products = polynomial_products(packet['overlay'], np.column_stack([
                        coarse_projection, common_trial, coarse_projection, common_acceleration]))
                    native_gradient = factor_mapping(data[0], 'gradient')
                    native_weak = dot(coarse_test, mass_apply(action, acceleration))-dot(
                        decimal_array(data[0]['gradient_weights'])[:, None]*native_gradient.apply(coarse_test), native_gradient.apply(trial))
                    expected['coarse_native_closure'] = sum(contract(moments['coarse_mass'], projection_products['mass'])
                        -contract(moments['coarse_gradient'], projection_products['gradient']), Decimal(0))-native_weak
                    fine_factor, coarse_factor = factor_mapping(data[1], 'gram'), factor_mapping(data[0], 'gram')
                    fine_product = fine_factor.apply(test)*fine_factor.apply(auxiliary['canonical_trial'].apply(trial))
                    coarse_product = coarse_factor.apply(coarse_test)*coarse_factor.apply(trial)
                    fine_weights = decimal_array(data[1]['gram_weights'])[:, None]
                    counter_weights = decimal_array(geometry['fine_gram_weights_at_coarse_geometry'])[:, None]
                    expected['Gram_geometry_weight'] = -sum(((fine_weights-counter_weights)*fine_product).flat, Decimal(0))
                    expected['Gram_same_geometry_stencil'] = -sum((counter_weights*fine_product).flat, Decimal(0))
                    expected['Gram_same_geometry_stencil'] += sum((decimal_array(data[0]['gram_weights'])[:, None]*coarse_product).flat, Decimal(0))
                    terms = []
                    for label, (mass, stiffness) in channels.items():
                        value = mass.apply(acceleration)-stiffness.apply(trial)
                        terms.append(value)
                        actual = dot(test, value)
                        error = abs(actual-expected[label])
                        evidence.check(branch+'_'+str(order)+'_'+label+'_independent_field_pairing',
                            error < Decimal('1e-37')*max(Decimal(1), abs(expected[label])), str(error))
                        for name, mapping in [('mass', mass), ('stiffness', stiffness)]:
                            dual_error = abs(dot(test, mapping.apply(trial))-dot(mapping.apply(test, True), trial))
                            evidence.check(branch+'_'+str(order)+'_'+label+'_'+name+'_transpose', dual_error < Decimal('1e-37'))
                        evidence.report['pairings'].append(dict(branch=branch, order=order, channel=label,
                            matrix_pairing=str(actual), independent_pairing=str(expected[label]), error=str(error), valid_for_claim=False))
                    direct = fine_maps['mass'].apply(acceleration)-stiffness_apply(fine_maps, trial)
                    error = max(map(abs, (sum(terms)-direct).flat))
                    evidence.check(branch+'_'+str(order)+'_complete_weak_operator_reconstruction',
                        error < Decimal('1e-37')*max(Decimal(1), max(map(abs, direct.flat))), str(error))
                    evidence.check(branch+'_'+str(order)+'_original_native_mass_semantics',
                        max(map(abs, (auxiliary['original_mass'].apply(acceleration)-mass_apply(action, acceleration)).flat)) < Decimal('1e-40'))
                    if branch == 'reference':
                        evidence.check('reference_'+str(order)+'_Gram_channels_exactly_zero',
                            all(len(channels[label][1].values) == 0 for label in ['Gram_geometry_weight', 'Gram_same_geometry_stencil']))
                    output = evidence.output/(branch+'-order'+str(order)+'-residual-matrices.json')
                    output.write_text(json.dumps({label:dict(mass=mass.serialize(), stiffness=stiffness.serialize())
                        for label, (mass, stiffness) in channels.items()})+'\n', encoding='utf-8')
                    evidence.own(output, 'outputs')
                    evidence.report['cases'].append(dict(branch=branch, order=order,
                        nonzeros={label:[len(mass.values), len(stiffness.values)] for label, (mass, stiffness) in channels.items()},
                        reconstruction_error=str(error), valid_for_claim=False))
                evidence.report['progress'] = dict(branch=branch, seconds=perf_counter()-started)
                evidence.save()
                print(json.dumps(evidence.report['progress']), flush=True)
        evidence.report['unresolved_test_Gram_zero_qualified'] = True
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
