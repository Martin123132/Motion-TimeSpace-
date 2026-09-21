from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System, IndexedP2Material
from annular_P2_weighted_projection_bounds_20260919 import projection_data, uniform_constants
from annular_P2_Gram_row_bounds_20260919 import row_bounds
from run_annular_P2_continuum_bridge_20260918 import checked_load
import contextlib
import json
import numpy as np


def peano_split(layer, values):
    indices = layer.element_indices
    nodal = values[np.maximum(indices, 0)]*(indices >= 0)
    lengths = np.diff(layer.edges)
    left_derivative = nodal @ np.array([-3., 4., -1.])/lengths
    right_derivative = nodal @ np.array([1., -4., 3.])/lengths
    curvature = nodal @ np.array([4., -8., 4.])/lengths**2
    atoms = np.zeros(len(layer.edges))
    atoms[1:-1] = left_derivative[1:]-right_derivative[:-1]
    source = int(np.searchsorted(layer.edges, layer.anchor))
    measured_jump = float(layer.jump @ values)
    source_jump_error = abs(atoms[source]-measured_jump)
    atoms[source] = 0.
    original = layer.original.tocsr()
    count = original.shape[0]
    regular, singular, boundary, bound, tolerances = [np.zeros(count) for unused in range(5)]
    phase_coordinate = (layer.anchor-layer.base_radii[0])/layer.gram_spacing
    phase = phase_coordinate-np.floor(phase_coordinate)
    source_neighbourhood = (layer.edges >= layer.anchor-(3+phase)*layer.gram_spacing-1e-12)
    source_neighbourhood &= layer.edges <= layer.anchor+(4-phase)*layer.gram_spacing+1e-12
    curvature_scale = abs(nodal) @ np.array([4., 8., 4.])/lengths**2
    left_scale = abs(nodal) @ np.array([3., 4., 1.])/lengths
    right_scale = abs(nodal) @ np.array([1., 4., 3.])/lengths
    atom_scale = np.zeros(len(layer.edges))
    atom_scale[1:-1] = left_scale[1:]+right_scale[:-1]
    atom_scale[source] = 0.
    abs_original = abs(original)
    source_rows = (np.asarray(abs_original @ (layer.radii < layer.anchor)).ravel() > 0)
    source_rows &= np.asarray(abs_original @ (layer.radii > layer.anchor)).ravel() > 0
    for row in range(count):
        start, end = original.indptr[row:row+2]
        columns = original.indices[start:end]
        coefficients = original.data[start:end]
        radii = layer.radii[columns]
        first, last = int(np.searchsorted(layer.edges, min(radii))), int(np.searchsorted(layer.edges, max(radii)))
        edges = layer.edges[first:last+1]
        kernel = np.maximum(radii[:, None]-edges[None, :], 0.).T @ coefficients
        integrals = np.diff(edges)*(kernel[:-1]+kernel[1:])/2
        regular[row] = curvature[first:last] @ integrals
        singular[row] = atoms[first+1:last+1] @ kernel[1:]
        selected = int(columns[np.argmin(radii)])
        initial_value = values[selected]-measured_jump*max(edges[0]-layer.anchor, 0.)
        initial_slope = left_derivative[first]-measured_jump*(edges[0] >= layer.anchor)
        boundary[row] = initial_value*np.sum(coefficients)+initial_slope*(coefficients @ (radii-edges[0]))
        bound[row] = np.sum(abs(curvature[first:last])*np.diff(edges)*(abs(kernel[:-1])+abs(kernel[1:]))/2)
        bound[row] += np.sum(abs(atoms[first+1:last+1]*kernel[1:]))+abs(boundary[row])
        arithmetic_scale = np.sum(abs(coefficients)*abs(values[columns]))+abs(layer.lifted_hinge[row]*measured_jump)
        arithmetic_scale += curvature_scale[first:last] @ abs(integrals)+atom_scale[first+1:last+1] @ abs(kernel[1:])
        tolerances[row] = 400*np.finfo(float).eps*arithmetic_scale+source_jump_error*abs(layer.lifted_hinge[row])+1e-23
        if source_rows[row]:
            source_neighbourhood[first:last+1] = True
    actual = layer.lifted @ values
    return dict(regular=regular, atoms=singular, moment_residual=boundary, absolute_bound=bound,
        actual=actual, tolerance=tolerances, source_rows=source_rows,
        curvature=curvature, ordinary_jumps=atoms, source_neighbourhood=source_neighbourhood,
        source_jump_identity_error=source_jump_error)


def main():
    evidence = EvidenceRun('annular-P2-live-weighted-projection-attempt04', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False,
            full_live_P2_force_convergence_proven=False, no_new_evolution=True,
            same_saved_live_states=True, finite_quadrature_weight_certificate_not_continuous_supremum=True,
            weighted_projection_bound_not_dynamic_stability=True,
            ordinary_gradient_jumps_not_discarded=True,
            common_source_window_used_for_zero_Gram_reference=True,
            three_prior_failed_attempts_preserved=True,
            left_endpoint_atom_excluded_because_initial_slope_is_right_trace=True,
            Peano_tolerance_includes_midpoint_differentiation_and_source_jump_roundoff=True,
            no_parent_regularity_claim_from_samples=True)
        constants = uniform_constants()
        for branch in ['reference', 'MTS']:
            configurations = [(257, 2e-5, 'annular-P2-evolved-source-halving-'+branch+'-attempt'+('02' if branch == 'MTS' else '01'),
                    'steps32-accepted032.npz'),
                (513, 1e-5, 'annular-P2-bulk513-MTS-time128-attempt01' if branch == 'MTS'
                    else 'annular-P2-bulk513-evolution-reference-attempt01',
                    'steps128-accepted128.npz' if branch == 'MTS' else 'steps64-accepted064.npz')]
            for count, cap, folder, filename in configurations:
                saved = checked_load(evidence, folder, filename)
                coordinates, momenta = saved['state']
                system = IndexedGradedP2System(count, branch == 'MTS', cap)
                rates, geometry = system.solve(coordinates, momenta)
                interpolation = IndexedP2Material(system, coordinates).interpolation(np.array([0.]))[0]
                layer = system.layer(0., geometry)
                values, speeds = interpolation @ coordinates, interpolation @ rates
                projected = projection_data(layer, values, speeds)
                ledger, arrays = row_bounds(layer, values, speeds)
                split = peano_split(layer, values[:-1])
                key = branch+str(count)
                error = abs(split['actual']-split['regular']-split['atoms']-split['moment_residual'])
                evidence.check(key+'_actual_weight_variation_and_mass_bound',
                    projected['discrete_relative_variation'] < constants['epsilon']
                    and projected['contraction'] <= constants['contraction']
                    and projected['stability'] <= constants['nodal_projection_stability'])
                evidence.check(key+'_actual_source_defect_pair_l1', projected['defect_pair_l1'] <= constants['source_pair_l1_bound'])
                evidence.check(key+'_actual_Peano_decomposition', np.all(error <= split['tolerance'])
                    and split['source_jump_identity_error'] < 2e-11,
                    dict(maximum_error=float(np.max(error, initial=0.)), maximum_tolerance=float(np.max(split['tolerance'], initial=0.))))
                evidence.check(key+'_actual_field_factor_BV_bound', np.all(abs(split['actual']) <= split['absolute_bound']+split['tolerance']))
                weighted_direction = arrays['weights']*arrays['direction_factors']
                components = []
                for name, mask in [('source_straddling', split['source_rows']), ('remaining', ~split['source_rows'])]:
                    components.append(dict(name=name, rows=int(sum(mask)),
                        regular_curvature_work=float(weighted_direction[mask] @ split['regular'][mask]),
                        ordinary_jump_work=float(weighted_direction[mask] @ split['atoms'][mask]),
                        polynomial_moment_roundoff_work=float(weighted_direction[mask] @ split['moment_residual'][mask]),
                        measured_work=float(np.sum(arrays['projected_rows'][mask])),
                        BV_absolute_work_bound=float(abs(weighted_direction[mask]) @ split['absolute_bound'][mask]),
                        floating_reconstruction_tolerance=float(abs(weighted_direction[mask]) @ split['tolerance'][mask])))
                for item in components:
                    reconstructed = item['regular_curvature_work']+item['ordinary_jump_work']+item['polynomial_moment_roundoff_work']
                    evidence.check(key+'_'+item['name']+'_force_Peano_split',
                        abs(reconstructed-item['measured_work']) <= item['floating_reconstruction_tolerance']+2e-20)
                source_mask = split['source_neighbourhood']
                edge_curvature_mask = source_mask[:-1] | source_mask[1:]
                row = dict(branch=branch, base_count=count, source_cap=cap,
                    discrete_cell_weight_variation=projected['discrete_relative_variation'],
                    mass_contraction=projected['contraction'], projection_stability=projected['stability'],
                    source_defect_pair_l1=projected['defect_pair_l1'],
                    measured_projection_maximum=float(max(abs(projected['projection']))),
                    global_maximum_element_curvature=float(max(abs(split['curvature']))),
                    global_ordinary_derivative_jump_variation=float(np.sum(abs(split['ordinary_jumps']))),
                    source_neighbourhood_maximum_element_curvature=float(np.max(abs(split['curvature'][edge_curvature_mask]), initial=0.)),
                    source_neighbourhood_ordinary_jump_variation=float(np.sum(abs(split['ordinary_jumps'][source_mask]))),
                    source_neighbourhood_jump_variation_over_h=float(np.sum(abs(split['ordinary_jumps'][source_mask]))/layer.gram_spacing),
                    Peano_maximum_error=float(np.max(error, initial=0.)), components=components,
                    actual_explicit_Gram_drive=ledger['explicit_drive'],
                    actual_explicit_shape_force=ledger['shape_force'],
                    valid_for_claim=False, source_path=str((evidence.output.parent/folder/'status.json').relative_to(evidence.root)))
                path = evidence.output/(key+'-weighted-Peano.npz')
                np.savez_compressed(path, projection=projected['projection'], source_defects=projected['source_defects'],
                    margins=projected['margins'], discrete_cell_variation=projected['discrete_cell_variation'],
                    **{name:value for name,value in split.items() if isinstance(value, np.ndarray)})
                evidence.own(path, 'outputs')
                evidence.report['cases'].append(row)
                evidence.save()
                print(json.dumps(row), flush=True)
        evidence.report['uniform_projection_constants'] = constants
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
