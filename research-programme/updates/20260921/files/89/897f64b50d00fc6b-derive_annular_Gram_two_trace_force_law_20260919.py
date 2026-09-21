from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_Gram_projection_commutator_20260919 import field_extension
from derive_annular_projection_source_trace_v2_20260919 import constant_trace_response, source_traces
from derive_annular_spatial_Gram_defect_split_20260919 import state_pair
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from scipy.linalg import solve_banded
import contextlib
import json
import numpy as np


def trace_force_data(layer, source_model, values, position):
    extension = field_extension(layer, source_model, values, position)
    response = constant_trace_response(layer, extension, position)
    moved = np.append(values[:-1], position)
    trace, unused = source_traces(source_model, moved)
    remainder_load = extension['load']-response['loads'] @ trace
    remainder = solve_banded((2, 2), extension['bands'], remainder_load, check_finite=False)
    return extension, response, trace, remainder


def functional_parts(layer, data, name):
    extension, response, trace, remainder = data
    selected = np.ones(len(extension['factor']), dtype=bool) if name == 'all_rows' else extension['source_rows']
    if name == 'remaining':
        selected = ~selected
    covector = np.asarray(layer.lifted.T @ (extension['weights']*extension['factor']*selected)).ravel()
    coefficient = covector @ response['response']
    shape = float(np.sum(extension['shape_rows'][selected]))
    regular = float(covector @ remainder)
    full = float(np.sum((extension['shape_rows']+extension['projected_rows'])[selected]))
    return dict(shape=shape, regular=regular, coefficient=coefficient, trace=trace,
        trace_force=float(coefficient @ trace), full=full)


def main():
    evidence = EvidenceRun('annular-Gram-two-trace-force-law-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, full_live_P2_force_convergence_proven=False,
            no_new_evolution=True, all_Gram_rows_retained=True, full_geometry_reconstructed=True,
            two_trace_force_identity_not_a_new_action=True, regular_remainder_retained=True,
            spatial_hierarchy_not_continuum_error=True, full_nonlinear_stability_proven=False)
        previous = {}
        for name in ['annular-projection-source-trace-attempt02', 'annular-spatial-Gram-defect-split-attempt02']:
            path = evidence.output.parent/name/'status.json'
            previous[name] = json.loads(path.read_text())
            evidence.own(path)
            evidence.check(name+'_complete', previous[name]['state'] == 'complete'
                and all(row['passed'] for row in previous[name]['checks']))
        for branch in ['reference', 'MTS']:
            coarse_system = IndexedGradedP2System(257, branch == 'MTS', 2e-5)
            fine_system = IndexedGradedP2System(513, branch == 'MTS', 1e-5)
            center = int(np.argmin(abs(coarse_system.labels)))
            label = coarse_system.labels[center]
            for final in [False, True]:
                coarse_state, fine_state = state_pair(evidence, branch, final)
                unused, coarse_geometry = coarse_system.solve(*coarse_state)
                unused, fine_geometry = fine_system.solve(*fine_state)
                coarse_values, fine_values = coarse_state[0, center], fine_state[0, center]
                coarse_layer = coarse_system.layer(label, coarse_geometry)
                fine_operator_layer = fine_system.layer(label, coarse_geometry)
                fine_layer = fine_system.layer(label, fine_geometry)
                configurations = dict(
                    coarse=(coarse_layer, coarse_system.model, coarse_values, coarse_values[-1]),
                    fine_operator=(fine_operator_layer, coarse_system.model, coarse_values, coarse_values[-1]),
                    fine_actual=(fine_layer, fine_system.model, fine_values, fine_values[-1]),
                    coarse_field_fine_geometry=(fine_layer, coarse_system.model, coarse_values, fine_values[-1]))
                data = {name:trace_force_data(*args) for name, args in configurations.items()}
                instant = 4e-5 if final else 0.
                old = next(case for case in previous['annular-spatial-Gram-defect-split-attempt02']['cases']
                    if case['branch'] == branch and case['time'] == instant)
                tag = branch+('_final' if final else '_initial')
                partitions, saved = [], {}
                for partition in ['all_rows', 'source_straddling', 'remaining']:
                    parts = {name:functional_parts(configurations[name][0], item, partition) for name, item in data.items()}
                    for name, item in parts.items():
                        evidence.check(tag+'_'+partition+'_'+name+'_force_identity',
                            abs(item['full']-item['shape']-item['trace_force']-item['regular']) < 3e-15)
                    for kind, first_name, last_name in [('operator', 'coarse', 'fine_operator'),
                            ('field_without_nodal_transfer', 'coarse_field_fine_geometry', 'fine_actual')]:
                        first, last = parts[first_name], parts[last_name]
                        coefficient_change = last['coefficient']-first['coefficient']
                        trace_change = last['trace']-first['trace']
                        mean_coefficient = (last['coefficient']+first['coefficient'])/2
                        mean_trace = (last['trace']+first['trace'])/2
                        coefficient_channel = float(coefficient_change @ mean_trace)
                        trace_channel = float(mean_coefficient @ trace_change)
                        shape = last['shape']-first['shape']
                        regular = last['regular']-first['regular']
                        difference = last['full']-first['full']
                        old_part = next(item for item in old['partitions'] if item['partition'] == partition)
                        expected = old_part['operator_mesh_difference'] if kind == 'operator' else (
                            old_part['field_state_difference']+old_part['transfer_commutator'])
                        error = abs(difference-coefficient_channel-trace_channel-shape-regular)
                        evidence.check(tag+'_'+partition+'_'+kind+'_polarization_and_saved_difference',
                            error < 3e-15 and abs(difference-expected) < 3e-15, error)
                        if kind == 'operator':
                            evidence.check(tag+'_'+partition+'_same_source_trace_in_operator_comparison', np.array_equal(first['trace'], last['trace']))
                        partitions.append(dict(partition=partition, comparison=kind, difference=difference,
                            trace_response_coefficient_channel=coefficient_channel, source_trace_value_channel=trace_channel,
                            shape_weight_channel=shape, regular_projection_channel=regular,
                            coefficient_change_left=float(coefficient_change[0]), coefficient_change_right=float(coefficient_change[1]),
                            source_trace_change_left=float(trace_change[0]), source_trace_change_right=float(trace_change[1]),
                            reconstruction_error=error, source_trace_variation_only_not_sufficient=True, valid_for_claim=False))
                    for name, item in parts.items():
                        saved[partition+'_'+name+'_coefficient'] = item['coefficient']
                        saved[partition+'_'+name+'_trace'] = item['trace']
                evidence.report['cases'].append(dict(branch=branch, time=instant, partitions=partitions, valid_for_claim=False))
                path = evidence.output/(tag+'-two-trace-covectors.npz')
                np.savez_compressed(path, **saved)
                evidence.own(path, 'outputs')
                evidence.save()
                print(json.dumps(dict(case=tag, all_rows=[row for row in partitions if row['partition'] == 'all_rows'])), flush=True)
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
