from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_Gram_projection_commutator_20260919 import field_extension, mass_pairing, band_action
from derive_annular_spatial_Gram_defect_split_20260919 import state_pair, drive
from derive_annular_spatial_Gram_transfer_split_v2_20260919 import extended_drive
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from run_annular_P2_saved_impulse_20260919 import own_core
from time import perf_counter
import contextlib
import json
import numpy as np


def main():
    own_core(0)
    evidence = EvidenceRun('annular-spatial-projection-commutator-attempt01', __file__)
    try:
        started = perf_counter()
        evidence.report.update(github_action=False, subagents_used=False, full_live_P2_force_convergence_proven=False,
            no_new_evolution=True, all_Gram_rows_retained=True, unchanged_fine_quadrature=True,
            reference_Gram_identically_zero=True, counterfactuals_not_evolved_states=True,
            spatial_hierarchy_not_isolated_truncation_error=True, complete_physical_force_not_bounded=True)
        statuses = {}
        for name in ['annular-projection-commutator-algebra-attempt01', 'annular-spatial-Gram-defect-split-attempt02']:
            path = evidence.output.parent/name/'status.json'
            status = json.loads(path.read_text())
            evidence.own(path)
            evidence.check(name+'_complete', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
            statuses[name] = status
        previous = statuses['annular-spatial-Gram-defect-split-attempt02']
        for branch in ['reference', 'MTS']:
            coarse_system = IndexedGradedP2System(257, branch == 'MTS', 2e-5)
            fine_system = IndexedGradedP2System(513, branch == 'MTS', 1e-5)
            center = int(np.argmin(abs(coarse_system.labels)))
            label = coarse_system.labels[center]
            for final in [False, True]:
                coarse_state, unused = state_pair(evidence, branch, final)
                unused, geometry = coarse_system.solve(*coarse_state)
                values = coarse_state[0, center]
                coarse_layer = coarse_system.layer(label, geometry)
                fine_layer = fine_system.layer(label, geometry)
                fine = field_extension(fine_layer, coarse_system.model, values, values[-1])
                coarse = field_extension(coarse_layer, coarse_system.model, values, values[-1])
                fine_check, unused = extended_drive(fine_layer, coarse_system.model, values, values[-1])
                coarse_check = drive(coarse_layer, values)
                indices, shape, unused = coarse_system.model.features_quadratic(fine_layer.radii)
                transferred_projection = np.sum(shape*coarse['projection'][indices], axis=1)
                residual = fine['load']-band_action(fine['bands'], transferred_projection)
                direct_correction = fine['projection']-transferred_projection
                actual_time = 4e-5 if final else 0.
                tag = branch+('_final' if final else '_initial')
                old = next(row for row in previous['cases'] if row['branch'] == branch and row['time'] == actual_time)
                evidence.check(tag+'_positive_mass_Cholesky', min(fine['minimum_cholesky_diagonal'],
                    coarse['minimum_cholesky_diagonal']) > 0)
                arrays = dict(residual=residual, mass_bands=fine['bands'], fine_load=fine['load'],
                    fine_projection=fine['projection'], transferred_coarse_projection=transferred_projection,
                    direct_correction=direct_correction, fine_radii=fine_layer.radii,
                    fine_shape_rows=fine['shape_rows'], fine_projected_rows=fine['projected_rows'],
                    coarse_shape_rows=coarse['shape_rows'], coarse_projected_rows=coarse['projected_rows'])
                partitions = []
                for name in ['all_rows', 'source_straddling', 'remaining']:
                    fine_mask = np.ones(len(fine['factor']), dtype=bool) if name == 'all_rows' else fine['source_rows']
                    coarse_mask = np.ones(len(coarse['factor']), dtype=bool) if name == 'all_rows' else coarse['source_rows']
                    if name == 'remaining':
                        fine_mask, coarse_mask = ~fine_mask, ~coarse_mask
                    covector = np.asarray(fine_layer.lifted.T @ (fine['weights']*fine['factor']*fine_mask)).ravel()
                    result, solved = mass_pairing(fine['bands'], residual, covector)
                    direct_pair = float(covector @ direct_correction)
                    mismatch = float(np.linalg.norm(solved['correction']-direct_correction))
                    relative = mismatch/max(np.linalg.norm(direct_correction), 1e-30)
                    fine_shape = float(np.sum(fine['shape_rows'][fine_mask]))
                    coarse_shape = float(np.sum(coarse['shape_rows'][coarse_mask]))
                    transferred_product = float(np.sum((fine['weights']*fine['factor']
                        *(fine_layer.lifted @ transferred_projection))[fine_mask]))
                    coarse_product = float(np.sum(coarse['projected_rows'][coarse_mask]))
                    fine_total = float(np.sum((fine['shape_rows']+fine['projected_rows'])[fine_mask]))
                    coarse_total = coarse_shape+coarse_product
                    shape_difference = fine_shape-coarse_shape
                    stencil_difference = transferred_product-coarse_product
                    operator = fine_total-coarse_total
                    previous_part = next(part for part in old['partitions'] if part['partition'] == name)
                    check_tag = tag+'_'+name
                    evidence.check(check_tag+'_original_and_extended_drives_retained', abs(fine_total-fine_check[name]) < 3e-15
                        and abs(coarse_total-coarse_check[name]) < 3e-15
                        and abs(operator-previous_part['operator_mesh_difference']) < 3e-15)
                    evidence.check(check_tag+'_actual_mass_commutator_recovered', relative < 3e-6
                        and abs(direct_pair-result['projection_force']) < 3e-15,
                        dict(relative_correction_error=relative, force_pair_error=abs(direct_pair-result['projection_force'])))
                    evidence.check(check_tag+'_dual_identity_and_both_bounds', abs(result['dual_residual_pairing']-direct_pair) < 3e-15
                        and abs(direct_pair) <= result['dual_mass_bound']+3e-15
                        and abs(direct_pair) <= result['dual_residual_absolute_bound']+3e-15)
                    telescope_error = abs(operator-result['projection_force']-shape_difference-stencil_difference)
                    evidence.check(check_tag+'_operator_split', telescope_error < 3e-15, telescope_error)
                    selected = abs(fine_layer.radii-fine_layer.anchor) <= 2*coarse_layer.source_cap
                    node_parts = dict(source_near_dual_residual=float(np.sum(solved['dual_terms'][selected])),
                        source_far_dual_residual=float(np.sum(solved['dual_terms'][~selected])),
                        source_near_absolute_bound=float(np.sum(abs(solved['dual_terms'][selected]))),
                        source_far_absolute_bound=float(np.sum(abs(solved['dual_terms'][~selected]))))
                    partitions.append(dict(partition=name, **result, **node_parts,
                        direct_projection_pairing=direct_pair, mass_correction_relative_error=relative,
                        shape_weight_difference=shape_difference, transferred_stencil_difference=stencil_difference,
                        operator_mesh_difference=operator, split_reconstruction_error=telescope_error,
                        fine_extended_force=fine_total, coarse_force=coarse_total,
                        source_node_window_half_width=2*coarse_layer.source_cap))
                    arrays[name+'_dual'] = solved['dual']
                    arrays[name+'_dual_terms'] = solved['dual_terms']
                    arrays[name+'_correction'] = solved['correction']
                evidence.report['cases'].append(dict(branch=branch, time=actual_time, partitions=partitions,
                    coarse_count=257, fine_count=513, residual_euclidean_norm=float(np.linalg.norm(residual)),
                    projection_correction_maximum=float(max(abs(direct_correction))), valid_for_claim=False))
                path = evidence.output/(tag+'-projection.npz')
                np.savez_compressed(path, **arrays)
                evidence.own(path, 'outputs')
                evidence.report.update(seconds=perf_counter()-started)
                evidence.save()
                print(json.dumps(dict(case=tag, seconds=perf_counter()-started, all_rows=partitions[0])), flush=True)
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
