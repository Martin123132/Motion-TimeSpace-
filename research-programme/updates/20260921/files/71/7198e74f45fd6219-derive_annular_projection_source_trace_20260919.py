from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_Gram_projection_commutator_20260919 import field_extension, mass_pairing, band_action
from derive_annular_spatial_Gram_defect_split_20260919 import state_pair
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from scipy.linalg import solve_banded
import contextlib
import json
import numpy as np


def constant_trace_response(layer, extension, position):
    source_index = int(np.searchsorted(layer.edges, layer.anchor))
    order = len(layer.fractions)
    missing = np.zeros((len(layer.reference_radius), 2))
    fractions = layer.fractions
    missing[(source_index-1)*order:source_index*order, 0] = fractions*(2*fractions-1)
    missing[source_index*order:(source_index+1)*order, 1] = (1-fractions)*(1-2*fractions)
    radius, jacobian, unused = layer.mapping(layer.reference_radius, position)
    weight = layer.reference_weight*jacobian*radius**4/layer.coefficient(0., radius)
    side_quadrature = np.column_stack([layer.reference_radius < layer.anchor, layer.reference_radius > layer.anchor])
    side_nodes = np.column_stack([layer.radii < layer.anchor, layer.radii > layer.anchor]).astype(float)
    columns = np.column_stack([layer.assemble_quadratic(layer.reference_indices,
        layer.reference_shape*(weight*missing[:, side])[:, None]) for side in range(2)])
    loads = np.column_stack([layer.assemble_quadratic(layer.reference_indices,
        layer.reference_shape*(weight*side_quadrature[:, side])[:, None]) for side in range(2)])
    defects = solve_banded((2, 2), extension['bands'], columns, check_finite=False)
    response = side_nodes+defects
    direct = solve_banded((2, 2), extension['bands'], loads, check_finite=False)
    return dict(nodes=side_nodes, columns=columns, loads=loads, defects=defects, response=response,
        direct=direct, response_error=float(np.max(abs(response-direct))),
        load_identity_error=float(max(np.max(abs(loads[:, side]-band_action(extension['bands'], side_nodes[:, side])
            -columns[:, side])) for side in range(2))))


def source_traces(model, values):
    source = int(np.searchsorted(model.edges, model.anchor))
    gradients = []
    for element, derivative in [(source-1, np.array([1., -4., 3.])), (source, np.array([-3., 4., -1.]))]:
        indices = model.element_indices[element]
        present = indices >= 0
        gradients.append(float(derivative[present] @ values[:-1][indices[present]]/(model.edges[element+1]-model.edges[element])))
    reference = np.array([np.nextafter(model.anchor, -np.inf), model.anchor])
    unused, jacobian, unused = model.mapping(reference, values[-1])
    return -np.array(gradients)/jacobian, np.array(gradients)


def main():
    evidence = EvidenceRun('annular-projection-source-trace-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, full_live_P2_force_convergence_proven=False,
            no_new_evolution=True, source_Dirichlet_condition_unchanged=True, all_Gram_rows_retained=True,
            two_trace_response_exact_for_piecewise_constants=True, remainder_retained=True,
            full_nonlinear_source_error_bound_derived=False, complete_physical_force_not_bounded=True)
        path = evidence.output.parent/'annular-spatial-projection-commutator-attempt01/status.json'
        previous = json.loads(path.read_text())
        evidence.own(path)
        evidence.check('previous_commutator_complete', previous['state'] == 'complete' and all(row['passed'] for row in previous['checks']))
        for branch in ['reference', 'MTS']:
            coarse_system = IndexedGradedP2System(257, branch == 'MTS', 2e-5)
            fine_system = IndexedGradedP2System(513, branch == 'MTS', 1e-5)
            center = int(np.argmin(abs(coarse_system.labels)))
            label = coarse_system.labels[center]
            for final in [False, True]:
                state, unused = state_pair(evidence, branch, final)
                unused, geometry = coarse_system.solve(*state)
                values = state[0, center]
                coarse_layer, fine_layer = coarse_system.layer(label, geometry), fine_system.layer(label, geometry)
                coarse = field_extension(coarse_layer, coarse_system.model, values, values[-1])
                fine = field_extension(fine_layer, coarse_system.model, values, values[-1])
                trace, gradients = source_traces(coarse_system.model, values)
                coarse_trace = constant_trace_response(coarse_layer, coarse, values[-1])
                fine_trace = constant_trace_response(fine_layer, fine, values[-1])
                indices, shape, unused = coarse_system.model.features_quadratic(fine_layer.radii)

                def transfer(vector):
                    return np.sum(shape*vector[indices], axis=1)

                trace_correction = fine_trace['response']-np.column_stack([transfer(coarse_trace['response'][:, side]) for side in range(2)])
                nodal_correction = fine_trace['nodes']-np.column_stack([transfer(coarse_trace['nodes'][:, side]) for side in range(2)])
                defect_correction = fine_trace['defects']-np.column_stack([transfer(coarse_trace['defects'][:, side]) for side in range(2)])
                coarse_remainder_load = coarse['load']-coarse_trace['loads'] @ trace
                fine_remainder_load = fine['load']-fine_trace['loads'] @ trace
                coarse_remainder = solve_banded((2, 2), coarse['bands'], coarse_remainder_load, check_finite=False)
                fine_remainder = solve_banded((2, 2), fine['bands'], fine_remainder_load, check_finite=False)
                remainder_correction = fine_remainder-transfer(coarse_remainder)
                full_correction = fine['projection']-transfer(coarse['projection'])
                remainder_residual = fine_remainder_load-band_action(fine['bands'], transfer(coarse_remainder))
                time = 4e-5 if final else 0.
                tag = branch+('_final' if final else '_initial')
                evidence.check(tag+'_source_gradient_trace_jump', abs(gradients[1]-gradients[0]
                    -coarse_system.model.jump @ values[:-1]) < 2e-14)
                for name, item in [('fine', fine_trace), ('coarse', coarse_trace)]:
                    evidence.check(tag+'_'+name+'_constant_trace_mass_law', item['response_error'] < 3e-13
                        and item['load_identity_error'] < 3e-11, dict(response=item['response_error'], load=item['load_identity_error']))
                error = float(np.max(abs(full_correction-trace_correction @ trace-remainder_correction)))
                evidence.check(tag+'_complete_trace_plus_remainder', error < 3e-13, error)
                old = next(case for case in previous['cases'] if case['branch'] == branch and case['time'] == time)
                partitions = []
                saved = dict(trace=trace, coarse_gradient_traces=gradients, trace_correction=trace_correction,
                    remainder_correction=remainder_correction, full_correction=full_correction,
                    fine_trace_response=fine_trace['response'], coarse_trace_response=coarse_trace['response'],
                    fine_remainder_residual=remainder_residual)
                for name in ['all_rows', 'source_straddling', 'remaining']:
                    selected = np.ones(len(fine['factor']), dtype=bool) if name == 'all_rows' else fine['source_rows']
                    if name == 'remaining':
                        selected = ~selected
                    covector = np.asarray(fine_layer.lifted.T @ (fine['weights']*fine['factor']*selected)).ravel()
                    coefficients = covector @ trace_correction
                    trace_force = float(coefficients @ trace)
                    full_force = float(covector @ full_correction)
                    remainder_force = float(covector @ remainder_correction)
                    remainder_bound, unused = mass_pairing(fine['bands'], remainder_residual, covector)
                    old_part = next(part for part in old['partitions'] if part['partition'] == name)
                    evidence.check(tag+'_'+name+'_force_split_and_saved_match', abs(full_force-trace_force-remainder_force) < 3e-15
                        and abs(full_force-old_part['projection_force']) < 3e-15)
                    evidence.check(tag+'_'+name+'_remainder_has_independent_load_bound',
                        abs(remainder_force-remainder_bound['projection_force']) < 3e-15
                        and abs(remainder_force) <= remainder_bound['dual_residual_absolute_bound']+3e-15
                        and abs(remainder_force) <= remainder_bound['dual_mass_bound']+3e-15)
                    partitions.append(dict(partition=name, full_projection_force=full_force, trace_force=trace_force,
                        remainder_force=remainder_force, left_trace_coefficient=float(coefficients[0]),
                        right_trace_coefficient=float(coefficients[1]), left_trace_force=float(coefficients[0]*trace[0]),
                        right_trace_force=float(coefficients[1]*trace[1]),
                        nodal_trace_transfer_force=float(covector @ (nodal_correction @ trace)),
                        constrained_mass_trace_force=float(covector @ (defect_correction @ trace)),
                        trace_absolute_bound=float(np.sum(abs(coefficients*trace))),
                        remainder_dual_mass_bound=remainder_bound['dual_mass_bound'],
                        remainder_localized_bound=remainder_bound['dual_residual_absolute_bound'],
                        trace_fraction=trace_force/full_force if full_force != 0 else None, valid_for_claim=False))
                    saved[name+'_covector'] = covector
                evidence.report['cases'].append(dict(branch=branch, time=time, source_motion_traces=trace.tolist(),
                    original_gradient_traces=gradients.tolist(), partitions=partitions, valid_for_claim=False))
                path = evidence.output/(tag+'-trace-response.npz')
                np.savez_compressed(path, **saved)
                evidence.own(path, 'outputs')
                evidence.save()
                print(json.dumps(dict(case=tag, traces=trace.tolist(), all_rows=partitions[0])), flush=True)
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
