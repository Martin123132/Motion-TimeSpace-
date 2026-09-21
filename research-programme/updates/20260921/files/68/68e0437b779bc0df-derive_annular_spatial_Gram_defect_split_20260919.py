from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from annular_P2_Gram_row_bounds_20260919 import row_bounds
from run_annular_P2_continuum_bridge_20260918 import checked_load
import contextlib
import json
import numpy as np


def state_pair(evidence, branch, final):
    if not final:
        coarse = checked_load(evidence, 'annular-P2-joint-refinement-257-cap2e-05-attempt01', branch+'-initial.npz')
        fine = checked_load(evidence, 'annular-P2-bulk513-preflight-'+branch+'-attempt01', 'initial.npz')
        return [np.stack([data['coordinates'], data['momenta']]) for data in [coarse, fine]]
    coarse_folder = 'annular-P2-evolved-source-halving-'+branch+'-attempt'+('02' if branch == 'MTS' else '01')
    fine_folder = 'annular-P2-bulk513-MTS-time128-attempt01' if branch == 'MTS' else 'annular-P2-bulk513-evolution-reference-attempt01'
    steps = 128 if branch == 'MTS' else 64
    coarse = checked_load(evidence, coarse_folder, 'steps32-accepted032.npz')['state']
    fine = checked_load(evidence, fine_folder, 'steps'+str(steps)+'-accepted'+str(steps).zfill(3)+'.npz')['state']
    return coarse, fine


def drive(layer, coordinates):
    report, unused = row_bounds(layer, coordinates, np.zeros_like(coordinates))
    parts = {group['name']:group['shape_sum']+group['projected_sum'] for group in report['groups']}
    parts['all_rows'] = report['explicit_drive']
    return parts


def main():
    evidence = EvidenceRun('annular-spatial-Gram-defect-split-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, full_live_P2_force_convergence_proven=False,
            no_new_evolution=True, all_Gram_rows_retained=True, spatial_hierarchy_not_continuum_error=True,
            counterfactuals_not_evolved_states=True, full_geometry_reconstructed_on_both_paths=True,
            split_order_explicit_not_unique_causal_attribution=True)
        for branch in ['reference', 'MTS']:
            coarse_system = IndexedGradedP2System(257, branch == 'MTS', 2e-5)
            fine_system = IndexedGradedP2System(513, branch == 'MTS', 1e-5)
            center = int(np.argmin(abs(fine_system.labels)))
            label = fine_system.labels[center]
            nesting_error = float(max(min(abs(fine_system.model.edges-edge)) for edge in coarse_system.model.edges))
            evidence.check(branch+'_actual_nested_spatial_elements', nesting_error < 2e-14, nesting_error)
            for final in [False, True]:
                coarse, fine = state_pair(evidence, branch, final)
                coarse_rates, coarse_geometry = coarse_system.solve(*coarse)
                fine_rates, fine_geometry = fine_system.solve(*fine)
                coarse_values, fine_values = coarse[0, center], fine[0, center]
                indices, shape, unused = coarse_system.model.features_quadratic(fine_system.model.radii)
                embedded = np.sum(shape*coarse_values[:-1][indices], axis=1)
                fine_layer = fine_system.layer(label, fine_geometry)
                fine_on_coarse_geometry = fine_system.layer(label, coarse_geometry)
                coarse_layer = coarse_system.layer(label, coarse_geometry)
                direct_fine = drive(fine_layer, fine_values)
                field_replaced = drive(fine_layer, np.append(embedded, fine_values[-1]))
                geometry_replaced = drive(fine_on_coarse_geometry, np.append(embedded, coarse_values[-1]))
                direct_coarse = drive(coarse_layer, coarse_values)
                tag = branch+('_final' if final else '_initial')
                actual_report, unused = row_bounds(fine_layer, fine_values, fine_rates[center])
                evidence.check(tag+'_explicit_Gram_drive_independent_of_probe_velocity',
                    abs(actual_report['explicit_drive']-direct_fine['all_rows']) < 2e-20)
                back_indices, back_shape, unused = fine_system.model.features_quadratic(coarse_system.model.radii)
                back = np.sum(back_shape*embedded[back_indices], axis=1)
                evidence.check(tag+'_exact_P2_embedding_at_coarse_nodes', max(abs(back-coarse_values[:-1])) < 2e-13)
                partitions = []
                for name in ['all_rows', 'source_straddling', 'remaining']:
                    field = direct_fine[name]-field_replaced[name]
                    geometry = field_replaced[name]-geometry_replaced[name]
                    operator = geometry_replaced[name]-direct_coarse[name]
                    difference = direct_fine[name]-direct_coarse[name]
                    evidence.check(tag+'_'+name+'_exact_three_way_spatial_telescope',
                        abs(difference-field-geometry-operator) < 3e-20)
                    partitions.append(dict(partition=name, fine_drive=direct_fine[name], coarse_drive=direct_coarse[name],
                        embedded_coarse_at_fine_geometry=field_replaced[name],
                        fine_operator_at_coarse_field_and_geometry=geometry_replaced[name],
                        field_state_difference=field, geometry_source_difference=geometry,
                        operator_mesh_difference=operator, direct_difference=difference,
                        absolute_three_term_bound=abs(field)+abs(geometry)+abs(operator), valid_for_claim=False))
                row = dict(branch=branch, time=4e-5 if final else 0., coarse_count=257, fine_count=513,
                    maximum_embedded_field_difference=float(max(abs(fine_values[:-1]-embedded))),
                    source_position_difference=float(fine_values[-1]-coarse_values[-1]),
                    partitions=partitions, valid_for_claim=False)
                evidence.report['cases'].append(row)
                evidence.save()
                print(json.dumps(row), flush=True)
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
