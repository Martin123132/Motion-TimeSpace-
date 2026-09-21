from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_spatial_Gram_defect_split_20260919 import state_pair, drive
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from annular_P2_Gram_row_bounds_20260919 import row_bounds
from scipy.linalg import solve_banded
import contextlib
import json
import numpy as np


def extended_drive(layer, source_model, source_values, position):
    indices, shape, unused = source_model.features_quadratic(layer.radii)
    samples = np.sum(shape*source_values[:-1][indices], axis=1)
    indices, unused, radial = source_model.features_quadratic(layer.reference_radius)
    reference_gradient = np.sum(radial*source_values[:-1][indices], axis=1)
    radius, jacobian, motion = layer.mapping(layer.reference_radius, position)
    kinetic_weight = layer.reference_weight*jacobian*radius**4/layer.coefficient(0., radius)
    load = layer.assemble_quadratic(layer.reference_indices,
        layer.reference_shape*((-motion/jacobian)*kinetic_weight*reference_gradient)[:, None])
    coordinates = np.append(samples, position)
    data = layer.evaluate(0., coordinates, np.zeros_like(coordinates))
    projection = solve_banded((2, 2), data['mass_bands'], load, check_finite=False)
    radius, jacobian, unused = layer.mapping(layer.radii, position)
    weights = np.asarray(layer.sampling @ (layer.coefficient(0., radius)/jacobian))/layer.gram_spacing
    radius, jacobian, unused = layer.mapping(layer.radii, complex(position, 1e-24))
    derivative = np.asarray(layer.sampling @ (layer.coefficient(0., radius)/jacobian)).imag/(1e-24*layer.gram_spacing)
    coarse_jump = source_model.jump @ source_values[:-1]
    factor = layer.original @ samples-layer.lifted_hinge*coarse_jump
    projected = layer.lifted @ projection
    rows = -.5*derivative*factor**2+weights*factor*projected
    stencil = abs(layer.original)
    left = np.asarray(stencil @ (layer.radii < layer.anchor)).ravel()
    right = np.asarray(stencil @ (layer.radii > layer.anchor)).ravel()
    source = (left > 0) & (right > 0)
    return dict(all_rows=float(np.sum(rows)), source_straddling=float(np.sum(rows[source])),
        remaining=float(np.sum(rows[~source]))), dict(original_source_jump=float(coarse_jump),
        interpolated_source_jump=float(layer.jump @ samples),
        cross_load_interpolation_difference=float(np.linalg.norm(load-data['cross'])),
        retains_original_fine_mass_and_quadrature=True)


def main():
    evidence = EvidenceRun('annular-spatial-Gram-defect-split-attempt02', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, full_live_P2_force_convergence_proven=False,
            no_new_evolution=True, all_Gram_rows_retained=True, spatial_hierarchy_not_continuum_error=True,
            counterfactuals_not_evolved_states=True, full_geometry_reconstructed_on_both_paths=True,
            split_order_explicit_not_unique_causal_attribution=True, nonnested_mesh_transfer_retained=True,
            off_space_extension_uses_unchanged_fine_quadrature=True,
            off_space_quadrature_not_a_continuous_integral_certificate=True)
        failure_path = evidence.output.parent/'annular-spatial-Gram-defect-split-attempt01/status.json'
        failure = json.loads(failure_path.read_text())
        evidence.own(failure_path)
        evidence.check('failed_nested_mesh_assumption_preserved', failure['state'] == 'failed')
        for branch in ['reference', 'MTS']:
            coarse_system = IndexedGradedP2System(257, branch == 'MTS', 2e-5)
            fine_system = IndexedGradedP2System(513, branch == 'MTS', 1e-5)
            center = int(np.argmin(abs(fine_system.labels)))
            label = fine_system.labels[center]
            distances = np.array([min(abs(fine_system.model.edges-edge)) for edge in coarse_system.model.edges])
            unmatched = coarse_system.model.edges[distances > 2e-14]
            evidence.check(branch+'_common_domain_and_source_anchor', np.array_equal(coarse_system.model.edges[[0, -1]],
                fine_system.model.edges[[0, -1]]) and coarse_system.model.anchor == fine_system.model.anchor)
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
                transferred_coarse = drive(fine_layer, np.append(embedded, fine_values[-1]))
                actual_coarse_on_fine, transfer_diagnostic = extended_drive(fine_layer,
                    coarse_system.model, coarse_values, fine_values[-1])
                actual_coarse_with_coarse_geometry, unused = extended_drive(fine_on_coarse_geometry,
                    coarse_system.model, coarse_values, coarse_values[-1])
                direct_coarse = drive(coarse_layer, coarse_values)
                self_extended, self_diagnostic = extended_drive(fine_layer, fine_system.model, fine_values, fine_values[-1])
                tag = branch+('_final' if final else '_initial')
                evidence.check(tag+'_extension_equals_original_on_fine_space',
                    abs(self_extended['all_rows']-direct_fine['all_rows']) < 3e-15
                    and self_diagnostic['cross_load_interpolation_difference'] < 2e-13)
                actual_report, unused = row_bounds(fine_layer, fine_values, fine_rates[center])
                evidence.check(tag+'_original_live_Gram_drive_retained',
                    abs(actual_report['explicit_drive']-direct_fine['all_rows']) < 2e-20)
                back_indices, back_shape, unused = fine_system.model.features_quadratic(coarse_system.model.radii)
                back = np.sum(back_shape*embedded[back_indices], axis=1)
                partitions = []
                for name in ['all_rows', 'source_straddling', 'remaining']:
                    state = direct_fine[name]-transferred_coarse[name]
                    transfer = transferred_coarse[name]-actual_coarse_on_fine[name]
                    geometry = actual_coarse_on_fine[name]-actual_coarse_with_coarse_geometry[name]
                    operator = actual_coarse_with_coarse_geometry[name]-direct_coarse[name]
                    difference = direct_fine[name]-direct_coarse[name]
                    evidence.check(tag+'_'+name+'_exact_four_way_spatial_telescope',
                        abs(difference-state-transfer-geometry-operator) < 3e-20)
                    partitions.append(dict(partition=name, fine_drive=direct_fine[name], coarse_drive=direct_coarse[name],
                        transferred_coarse_at_fine_geometry=transferred_coarse[name],
                        uninterpolated_coarse_at_fine_geometry=actual_coarse_on_fine[name],
                        fine_extended_operator_at_coarse_geometry=actual_coarse_with_coarse_geometry[name],
                        field_state_difference=state, transfer_commutator=transfer, geometry_source_difference=geometry,
                        operator_mesh_difference=operator, direct_difference=difference,
                        absolute_four_term_bound=abs(state)+abs(transfer)+abs(geometry)+abs(operator), valid_for_claim=False))
                row = dict(branch=branch, time=4e-5 if final else 0., coarse_count=257, fine_count=513,
                    maximum_embedded_field_difference=float(max(abs(fine_values[:-1]-embedded))),
                    source_position_difference=float(fine_values[-1]-coarse_values[-1]),
                    source_mesh_is_nested=bool(len(unmatched) == 0), unmatched_coarse_edges=unmatched.tolist(),
                    maximum_coarse_edge_distance=float(max(distances)),
                    nodal_roundtrip_transfer_error=float(max(abs(back-coarse_values[:-1]))),
                    transfer_diagnostic=transfer_diagnostic, partitions=partitions, valid_for_claim=False)
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
