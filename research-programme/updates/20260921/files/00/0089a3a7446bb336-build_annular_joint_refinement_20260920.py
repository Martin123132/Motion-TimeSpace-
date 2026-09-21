from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_common_P2_overlay_20260919 import evaluation_rows, compose_rows, apply_rows, forms, serialize_mesh, serialize_rows
from annular_common_frozen_candidate_20260920 import gram_rows, gram_matrix, sum_rows, forms_from_moments, FrozenCandidate
from annular_common_weighted_moments_20260920 import decimal_fraction, apply_rational_rows
from annular_mixed_weak_maps_20260920 import MixedMap
from annular_decimal_transport_v2_20260919 import decimal_array
from derive_annular_common_weak_action_20260920 import dec_saved
from build_annular_complete_frozen_candidate_20260920 import derivative_coefficients, dust_data
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from derive_annular_moving_Gram_profile_20260919 import evaluate_pair
from derive_annular_transfer_kernel_and_common_overlay_20260919 import owned_json
from run_annular_P2_continuum_bridge_20260918 import checked_load
from qualify_annular_nonuniform_Gram_precision_20260920 import sparse_apply
from decimal import Decimal, localcontext
from fractions import Fraction
from bisect import bisect_right
from time import perf_counter
import contextlib
import json
import numpy as np


ZERO = Decimal(0)


def rational_mesh(packet):
    return dict(edges=list(map(Fraction, packet['edges'])), nodes=list(map(Fraction, packet['nodes'])),
        anchor=Fraction(packet['anchor']), elements=packet['elements'], count=packet['count'])


def bisect_mesh(mesh):
    edges = sorted(mesh['edges']+[(lower+upper)/2 for lower, upper in zip(mesh['edges'], mesh['edges'][1:])])
    nodes = sorted([location for location in edges if location != mesh['anchor']]
        +[(lower+upper)/2 for lower, upper in zip(edges, edges[1:])])
    indices = {location:index for index, location in enumerate(nodes)}
    elements = [[indices.get(lower, -1), indices[(lower+upper)/2], indices.get(upper, -1)]
        for lower, upper in zip(edges, edges[1:])]
    return dict(edges=edges, nodes=nodes, elements=elements, count=len(nodes), anchor=mesh['anchor'])


def exact_cut_moments(mesh, cuts, fractions, weights, densities):
    parents, lengths, offsets, spans = [], [], [], []
    for lower, upper in zip(cuts, cuts[1:]):
        parent = bisect_right(mesh['edges'], (lower+upper)/2)-1
        left, right = mesh['edges'][parent:parent+2]
        if lower < left or upper > right:
            raise ValueError('Quadrature crosses exact rational child edge.')
        parents.append(parent)
        lengths.append(decimal_fraction(upper-lower))
        offsets.append(decimal_fraction((lower-left)/(right-left)))
        spans.append(decimal_fraction((upper-lower)/(right-left)))
    local = np.asarray(offsets, dtype=object)[:, None]+np.asarray(spans, dtype=object)[:, None]*decimal_array(fractions)
    measure = np.asarray(lengths, dtype=object)[:, None]*decimal_array(weights)
    result = {name:np.full((len(mesh['elements']), 5), ZERO, dtype=object) for name in densities}
    converted = {name:decimal_array(values) for name, values in densities.items()}
    power = np.full(local.shape, Decimal(1), dtype=object)
    for degree in range(5):
        weighted = measure*power
        for name, values in converted.items():
            np.add.at(result[name][:, degree], np.asarray(parents), np.sum(weighted*values, axis=1))
        power *= local
    return result


def pullback(rows, embedding, count):
    coefficients = [{column:decimal_fraction(value) for column, value in row.items()} for row in embedding]
    answer = [{} for unused in range(count)]
    for row, entries in enumerate(rows):
        for column, value in entries.items():
            for first, first_value in coefficients[row].items():
                for last, last_value in coefficients[column].items():
                    answer[first][last] = answer[first].get(last, ZERO)+first_value*value*last_value
    return answer


def relative_matrix_difference(first, last):
    maximum = ZERO
    scale = Decimal(1)
    for before, after in zip(first, last):
        for column in set(before) | set(after):
            maximum = max(maximum, abs(before.get(column, ZERO)-after.get(column, ZERO)))
            scale = max(scale, abs(after.get(column, ZERO)))
    return maximum/scale


def main():
    evidence = EvidenceRun('annular-joint-candidate-refinement-build-attempt01', __file__)
    started = perf_counter()
    try:
        evidence.report.update(github_action=False, subagents_used=False, candidate_only=True,
            original_live_action_unchanged=True, no_new_evolution=True, frozen_background_only=True,
            physical_force_mismatch_fixed=False, self_consistent_candidate_metric_solved=False,
            full_live_P2_force_convergence_proven=False, certified_continuous_time_bound=False,
            joint_refinement_assembly_qualified=False)
        evidence.report['meshes'], evidence.report['matrix_checks'] = [], []
        with localcontext() as ctx:
            ctx.prec = 64
            for branch in ['reference', 'MTS']:
                base_packet = owned_json(evidence, 'annular-transfer-kernel-overlay-attempt01', branch+'-exact-common-overlay.json')
                base = rational_mesh(base_packet['overlay'])
                base_action = owned_json(evidence, 'annular-complete-frozen-candidate-attempt01',
                    branch+('-reference' if branch == 'reference' else '-primary')+'-action.json')
                original_phase = dec_saved(base_action['phase'])
                geometry = checked_load(evidence, 'annular-common-action-weights-attempt01', branch+'-native-and-cuts.npz')
                saved = checked_load(evidence, 'annular-live-compensated-rate-attempt01', branch+'-1e-07-compensated-rate.npz')
                systems = [IndexedGradedP2System(257, branch == 'MTS', 2e-5), IndexedGradedP2System(513, branch == 'MTS', 1e-5)]
                pair = evaluate_pair(systems, [saved[str(level)+'_state'] for level in range(2)])
                layer, position = pair[0]['layer'], pair[0]['values'][-1]
                dust = dust_data(layer, position, pair[0]['rates'][-1])
                evidence.check(branch+'_unchanged_dust_background_exact', dust == base_action['dust'])
                mesh = base
                for level in [1, 2]:
                    mesh = bisect_mesh(mesh)
                    label = branch+'-L'+str(level)
                    embedding = evaluation_rows(base, mesh['nodes'])
                    restriction = evaluation_rows(mesh, base['nodes'])
                    evidence.check(label+'_exact_left_inverse', all(row == {index:Fraction(1)}
                        for index, row in enumerate(compose_rows(restriction, embedding))))
                    evidence.check(label+'_joint_every_cell_refinement', mesh['count'] == base['count']*2**level
                        and set(base['edges']).issubset(mesh['edges']) and mesh['anchor'] == base['anchor']
                        and max(np.diff(mesh['edges'])) == max(np.diff(base['edges']))/2**level)
                    for probe in range(2):
                        values = [Fraction((index*(17+probe)+3*probe)%31-15, 16) for index in range(base['count'])]
                        evidence.check(label+'_exact_unweighted_forms_'+str(probe),
                            forms(base, values) == forms(mesh, apply_rows(embedding, values)))
                    phase = np.stack([apply_rational_rows(embedding, values[:, None])[:, 0] for values in original_phase])
                    recovery = np.stack([apply_rational_rows(restriction, values[:, None])[:, 0] for values in phase])
                    evidence.check(label+'_initial_physical_field_preserved', max(abs(value) for value in
                        (recovery-original_phase).flat) < Decimal('1e-55'))
                    cuts = sorted(set(map(Fraction.from_float, map(float, geometry['integration_cuts']))) | set(mesh['edges']))
                    maps_by_order = {}
                    for order in [32, 64]:
                        old = checked_load(evidence, 'annular-common-action-weights-attempt01', branch+'-order'+str(order)+'-densities.npz')
                        fractions, weights = old['fractions'], old['gauss_weights']
                        coordinates = (np.array(list(map(float, cuts[:-1])))[:, None]
                            +np.array([float(upper-lower) for lower, upper in zip(cuts, cuts[1:])])[:, None]*fractions).ravel()
                        fields = derivative_coefficients(layer, position, coordinates)
                        shape = (len(cuts)-1, order)
                        densities = {name:fields[name].reshape(shape) for name in ['mass', 'mass_X', 'gradient', 'gradient_X']}
                        densities['transport'] = (fields['mass']*fields['transport']).reshape(shape)
                        densities['transport_X'] = (fields['mass_X']*fields['transport']+fields['mass']*fields['transport_X']).reshape(shape)
                        densities['inertia'] = (fields['mass']*fields['transport']**2).reshape(shape)
                        densities['inertia_X'] = (fields['mass_X']*fields['transport']**2+2*fields['mass']*fields['transport']*fields['transport_X']).reshape(shape)
                        moments = exact_cut_moments(mesh, cuts, fractions, weights, densities)
                        maps_by_order[order] = forms_from_moments(serialize_mesh(mesh), moments)
                    for name in maps_by_order[64]:
                        error = relative_matrix_difference(maps_by_order[32][name], maps_by_order[64][name])
                        evidence.check(label+'_'+name+'_quadrature', error < Decimal('3e-10'), str(error))
                        parent_rows = [{int(column):Decimal(value) for column, value in row.items()}
                            for row in base_action['maps'][name]['rows']]
                        preserved = relative_matrix_difference(pullback(maps_by_order[64][name], embedding, base['count']), parent_rows)
                        evidence.check(label+'_'+name+'_parent_pullback', preserved < Decimal('3e-10'), str(preserved))
                        evidence.report['matrix_checks'].append(dict(branch=branch, level=level, matrix=name,
                            quadrature_relative_change=str(error), parent_pullback_relative_change=str(preserved),
                            gate='3e-10', not_a_physical_force_gate=True, valid_for_claim=False))
                    mesh_path = evidence.output/(label+'-mesh.json')
                    mesh_path.write_text(json.dumps(dict(mesh=serialize_mesh(mesh), embedding_from_base=serialize_rows(embedding),
                        restriction_to_base=serialize_rows(restriction), level=level, valid_for_claim=False))+'\n', encoding='utf-8')
                    evidence.own(mesh_path, 'outputs')
                    knots = mesh['nodes']
                    node_fields = derivative_coefficients(layer, position, np.array(list(map(float, knots))))
                    for extension in (['reference'] if branch == 'reference' else ['primary', 'alternative']):
                        if extension == 'reference':
                            factors, row_weights, derivative_weights = [], [], []
                            gram, gram_X = [[{} for unused in range(mesh['count'])] for unused in range(2)]
                        else:
                            factors, sampling = gram_rows(serialize_mesh(mesh), knots, extension == 'alternative')
                            row_weights = sparse_apply(sampling, list(decimal_array(node_fields['gradient'])))
                            derivative_weights = sparse_apply(sampling, list(decimal_array(node_fields['gradient_X'])))
                            gram = gram_matrix(factors, row_weights, mesh['count'])
                            gram_X = gram_matrix(factors, derivative_weights, mesh['count'])
                        maps = dict(maps_by_order[64])
                        maps['stiffness'] = sum_rows(maps['gradient'], gram)
                        maps['stiffness_X'] = sum_rows(maps['gradient_X'], gram_X)
                        serial = dict(count=mesh['count'], branch=branch, extension=extension, level=level,
                            dust=dust, phase=phase.tolist(), maps={name:MixedMap(rows, mesh['count']).serialize() for name, rows in maps.items()},
                            gram_factor=MixedMap(factors, mesh['count']).serialize(), gram_weights=list(map(str, row_weights)),
                            gram_weights_X=list(map(str, derivative_weights)), valid_for_claim=False)
                        for name in ['mass', 'mass_X', 'gradient', 'gradient_X', 'inertia', 'inertia_X', 'stiffness', 'stiffness_X']:
                            evidence.check(label+'_'+extension+'_'+name+'_symmetric', all(value == maps[name][column].get(row, ZERO)
                                for row, entries in enumerate(maps[name]) for column, value in entries.items()))
                        action = FrozenCandidate(serial)
                        probe = np.array([[Decimal((index*7)%17-8)/16] for index in range(mesh['count'])], dtype=object)
                        error = max(abs(value) for value in (action.maps['mass'].apply(action.solve(probe))-probe).flat)
                        evidence.check(label+'_'+extension+'_mass_solve', error < Decimal('1e-45'), str(error))
                        if factors:
                            image = MixedMap(factors, mesh['count']).apply(phase[0, :, None])[:, 0]
                            direct = sum((weight*value**2 for weight, value in zip(row_weights, image)), ZERO)
                            assembled = sum(phase[0]*MixedMap(gram, mesh['count']).apply(phase[0, :, None])[:, 0], ZERO)
                            evidence.check(label+'_'+extension+'_positive_Gram_identity', direct >= 0
                                and abs(direct-assembled) < Decimal('1e-38'), str(abs(direct-assembled)))
                        output = evidence.output/(branch+'-'+extension+'-L'+str(level)+'-action.json')
                        output.write_text(json.dumps(serial, default=str)+'\n', encoding='utf-8')
                        evidence.own(output, 'outputs')
                        evidence.report['cases'].append(dict(branch=branch, extension=extension, level=level, count=mesh['count'],
                            frequency_bound=str(action.frequency_bound), mass_jacobi_ratio=str(action.mass_jacobi_ratio),
                            minimum_mass_pivot=str(min(action.diagonal)),
                            steps_at_4e_5=int((Decimal.from_float(4e-5)*action.frequency_bound/4).to_integral_value(rounding='ROUND_CEILING')),
                            valid_for_claim=False))
                    evidence.report['meshes'].append(dict(branch=branch, level=level, field_dofs=mesh['count'],
                        gram_knots=len(knots), cells=len(mesh['elements']), exact_largest_cell=str(max(np.diff(mesh['edges']))),
                        exact_smallest_cell=str(min(np.diff(mesh['edges']))), all_cells_bisected=True,
                        different_from_previous_fixed_field_knot_only_scan=True, valid_for_claim=False))
                    evidence.report['progress'] = dict(branch=branch, level=level, seconds=perf_counter()-started)
                    evidence.save()
                    print(json.dumps(evidence.report['progress']), flush=True)
        evidence.report.update(joint_refinement_assembly_qualified=True, seconds=perf_counter()-started)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), seconds=evidence.report['seconds'],
            cases=evidence.report['cases'])), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
