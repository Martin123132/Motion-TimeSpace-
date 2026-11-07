from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_common_P2_overlay_20260919 import native_mesh, common_mesh, evaluation_rows, apply_rows, compose_rows, forms, serialize_mesh, serialize_rows
from annular_decimal_transport_v2_20260919 import DecimalMap, decimal_array
from annular_P2_graded_source_20260919 import GradedSourceAction
from run_annular_P2_continuum_bridge_20260918 import checked_load
from decimal import Decimal, localcontext
from fractions import Fraction
from scipy.sparse import csr_matrix
from time import perf_counter
import contextlib
import hashlib
import json
import numpy as np


def owned_json(evidence, folder, name):
    status_path = evidence.output.parent/folder/'status.json'
    status = json.loads(status_path.read_text())
    evidence.own(status_path)
    evidence.check(folder+'_'+name+'_complete_source', status['state'] == 'complete'
        and all(row['passed'] for row in status['checks']))
    path = status_path.parent/name
    key = str(path.relative_to(evidence.root))
    expected = status['outputs'].get(key)
    evidence.check(folder+'_'+name+'_source_hash', expected is not None
        and hashlib.sha256(path.read_bytes()).hexdigest() == expected)
    evidence.own(path)
    return json.loads(path.read_text())


def main():
    evidence = EvidenceRun('annular-transfer-kernel-overlay-attempt01', __file__)
    started = perf_counter()
    try:
        evidence.report.update(github_action=False, subagents_used=False, no_new_evolution=True,
            original_action_unchanged=True, no_pseudoinverse_or_regularization=True,
            full_live_P2_force_convergence_proven=False, certified_continuous_time_bound=False,
            transfer_injectivity_proven=False, common_overlay_injectivity_proven=False,
            original_physical_force_mismatch_unchanged=True, decomposition_not_unique_causal_attribution=True,
            exact_overlay_geometry_is_saved_binary64_edges=True, maximum_wall_seconds=3600)
        evidence.report['topology'], evidence.report['localization'], evidence.report['witnesses'] = [], [], []
        status_path = evidence.output.parent/'annular-decimal-duality-attempt02/status.json'
        prior = json.loads(status_path.read_text())
        evidence.own(status_path)
        evidence.check('prior_unchanged_strict_duality_complete', prior['state'] == 'complete'
            and prior['original_strict_dual_gate_pass'] and all(row['passed'] for row in prior['checks']))
        for branch in ['reference', 'MTS']:
            models = [GradedSourceAction(257, branch == 'MTS', source_cap=2e-5),
                GradedSourceAction(513, branch == 'MTS', source_cap=1e-5)]
            native = [native_mesh(model) for model in models]
            overlay = common_mesh(*native)
            embeddings = [evaluation_rows(mesh, overlay['nodes']) for mesh in native]
            restrictions = [evaluation_rows(overlay, mesh['nodes']) for mesh in native]
            for name, mesh, embedding, restriction in zip(['coarse', 'fine'], native, embeddings, restrictions):
                composition = compose_rows(restriction, embedding)
                evidence.check(branch+'_'+name+'_exact_rational_left_inverse',
                    all(row == {index:Fraction(1)} for index, row in enumerate(composition)))
                for probe in range(3):
                    values = ([Fraction((index*17+probe*7) % 31-15, 16) for index in range(mesh['count'])]
                        if probe < 2 else [max(value-mesh['anchor'], Fraction(0)) for value in mesh['nodes']])
                    represented = apply_rows(embedding, values)
                    before, after = forms(mesh, values), forms(overlay, represented)
                    evidence.check(branch+'_'+name+'_'+str(probe)+'_exact_unweighted_mass_and_gradient_forms', before == after)
                    evidence.check(branch+'_'+name+'_'+str(probe)+'_exact_all_coefficients_recovered',
                        apply_rows(restriction, represented) == values)
            matrices = checked_load(evidence, 'annular-action-adjoint-stability-attempt01', branch+'_final-action-matrices.npz')
            interpolation = matrices['interpolation']
            native_indices, native_shapes, unused = models[0].features_quadratic(models[1].radii)
            reconstructed = csr_matrix((native_shapes.ravel(), (np.repeat(np.arange(models[1].count), 3), native_indices.ravel())),
                shape=interpolation.shape).toarray()
            evidence.check(branch+'_original_pointwise_transfer_reproduced', np.array_equal(reconstructed, interpolation))
            zero_columns = np.flatnonzero(np.all(interpolation == 0., axis=0))
            norms = np.linalg.norm(interpolation, axis=0)
            near_zero = (norms > 0) & (norms < 1e-8)
            evidence.check(branch+'_exact_six_erased_coarse_columns', len(zero_columns) == 6)
            gram = interpolation.T @ matrices['fine_mass'] @ interpolation
            evidence.check(branch+'_projected_mass_singular_witness', np.all(gram[:, zero_columns] == 0.)
                and np.all(gram[zero_columns, :] == 0.))
            missing_edges = sorted(set(native[0]['edges'])-set(native[1]['edges']))
            evidence.check(branch+'_coarse_elements_not_nested_in_fine', bool(missing_edges))
            for column in zero_columns:
                values = [Fraction(int(index == column)) for index in range(native[0]['count'])]
                mapped = apply_rows(embeddings[0], values)
                native_mass, native_stiffness = forms(native[0], values)
                evidence.check(branch+'_witness_'+str(column)+'_nonzero_field_not_lost_on_overlay',
                    native_mass > 0 and native_stiffness > 0 and any(mapped)
                    and forms(overlay, mapped) == (native_mass, native_stiffness))
                evidence.report['witnesses'].append(dict(branch=branch, coarse_column=int(column),
                    canonical_radius=str(native[0]['nodes'][column]), old_transfer_image_exactly_zero=True,
                    original_unweighted_mass=str(native_mass), original_unweighted_gradient_form=str(native_stiffness),
                    overlay_preserves_both_forms_exactly=True, valid_for_claim=False))
            widths = [upper-lower for lower, upper in zip(overlay['edges'][:-1], overlay['edges'][1:])]
            evidence.report['topology'].append(dict(branch=branch, coarse_count=native[0]['count'], fine_count=native[1]['count'],
                overlay_count=overlay['count'], erased_columns=list(map(int, zero_columns)),
                near_zero_columns=list(map(int, np.flatnonzero(near_zero))), absent_coarse_edges=len(missing_edges),
                minimum_exact_overlay_cell_width=str(min(widths)), sub_1e_minus12_cells=sum(width < Fraction(1, 10**12) for width in widths),
                nodes_merged=False, original_transfer_injective=False, exact_overlay_left_inverses=True, valid_for_claim=False))
            source = owned_json(evidence, 'annular-decimal-duality-attempt02', branch+'-48-transport.json')
            initial = checked_load(evidence, 'annular-moving-duhamel-trajectory-attempt01', branch+'-point032.npz')
            with localcontext() as ctx:
                ctx.prec = 64
                dual_fine = np.array(source['backward_fine'], dtype=object)
                dual_coarse = np.array(source['backward_coarse'], dtype=object)
                dual_fine = np.array([Decimal(value) for value in dual_fine.flat], dtype=object).reshape(dual_fine.shape)
                dual_coarse = np.array([Decimal(value) for value in dual_coarse.flat], dtype=object).reshape(dual_coarse.shape)
                transfer = DecimalMap(csr_matrix(interpolation))
                pulled = np.stack([transfer.apply(component, transpose=True) for component in dual_fine])
                difference = pulled-dual_coarse
                phase = decimal_array(np.stack([initial['0_position'], -initial['0_reverse_velocity']]))
                products = difference*phase[:, :, None]
                rows = products[0]+products[1]
                absolute_rows = abs(products[0])+abs(products[1])
                selected_zero = np.isin(np.arange(native[0]['count']), zero_columns)
                distance = np.array([float(abs(value-native[0]['anchor'])) for value in native[0]['nodes']])
                partitions = [('exact_erased_columns', selected_zero), ('near_zero_columns', near_zero),
                    ('remaining_columns', ~(selected_zero | near_zero))]
                windows = [('within_'+str(width), distance <= width) for width in [1e-4, 1e-3, 5e-3, 1e-2]]
                for column, comparison in enumerate(['spatial32', 'spatial64']):
                    total = sum(rows[:, column], Decimal(0))
                    total_bound = sum(absolute_rows[:, column], Decimal(0))
                    expected = Decimal(next(row['frozen_operator_commutator'] for row in prior['cases']
                        if row['branch'] == branch and row['comparison'] == comparison and row['digits'] == 48))
                    error = abs(total-expected)
                    tolerance = Decimal('2e-10')*max(abs(total), abs(expected), Decimal('1e-9'))+Decimal('3e-16')
                    evidence.check(branch+'_'+comparison+'_original_strict_commutator_gate', error <= tolerance,
                        dict(error=str(error), tolerance=str(tolerance)))
                    partition_total = Decimal(0)
                    for partition, selected in partitions+windows:
                        value = sum(rows[selected, column], Decimal(0))
                        bound = sum(absolute_rows[selected, column], Decimal(0))
                        if partition in [name for name, mask in partitions]:
                            partition_total += value
                        evidence.check(branch+'_'+comparison+'_'+partition+'_finite_input_triangle_bound', abs(value) <= bound)
                        evidence.report['localization'].append(dict(branch=branch, comparison=comparison,
                            partition=partition, count=int(sum(selected)), signed_value=str(value),
                            finite_input_triangle_bound=str(bound), fraction_of_signed_total=str(value/total),
                            cumulative_window=partition.startswith('within_'), valid_for_claim=False))
                    evidence.check(branch+'_'+comparison+'_complete_disjoint_partition', abs(partition_total-total) < Decimal('1e-48'))
                    erased = sum(rows[selected_zero, column], Decimal(0))
                    erased_direct = -sum((dual_coarse[:, selected_zero, column]*phase[:, selected_zero]).flat, Decimal(0))
                    evidence.check(branch+'_'+comparison+'_erased_initial_modes_identity', abs(erased-erased_direct) < Decimal('1e-48'))
                    evidence.report['cases'].append(dict(branch=branch, comparison=comparison,
                        frozen_operator_commutator=str(total), previously_qualified_commutator=str(expected),
                        unchanged_numerical_tolerance=str(tolerance), reconstruction_error=str(error),
                        erased_initial_modes_contribution=str(erased), erased_fraction_of_signed_total=str(erased/total),
                        finite_input_triangle_bound=str(total_bound), bound_to_signed_ratio=str(total_bound/abs(total)),
                        continuum_bound_certified=False, valid_for_claim=False))
                output = evidence.output/(branch+'-coarse-commutator-rows.json')
                output.write_text(json.dumps(dict(radii=list(map(str, native[0]['nodes'])),
                    dual_difference=difference.tolist(), phase_products=products.tolist(), row_sums=rows.tolist()), default=str)+'\n', encoding='utf-8')
                evidence.own(output, 'outputs')
            output = evidence.output/(branch+'-exact-common-overlay.json')
            output.write_text(json.dumps(dict(native=[serialize_mesh(mesh) for mesh in native], overlay=serialize_mesh(overlay),
                embeddings=[serialize_rows(value) for value in embeddings],
                left_inverses=[serialize_rows(value) for value in restrictions]))+'\n', encoding='utf-8')
            evidence.own(output, 'outputs')
            evidence.report['progress'] = dict(branch=branch, seconds=perf_counter()-started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
        evidence.report['common_overlay_injectivity_proven'] = True
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
