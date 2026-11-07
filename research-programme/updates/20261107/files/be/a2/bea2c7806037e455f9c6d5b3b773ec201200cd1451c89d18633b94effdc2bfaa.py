from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_acceleration_archive_checks_v2_20261001 import verify_report
from annular_high_order_native_v2_20261003 import adapt_owner, HighLoads, HighAction, HighKernel, high_mesh
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_candidate_hamiltonian_20260921 import decimals
from annular_decimal_transport_v2_20260919 import decimal_array
from annular_quadratic_core_20261002 import physical_edges
from annular_physical_native_kernel_20260928 import maximum
from analyze_annular_source_flat_state_20261002 import read_archive
from decimal import Decimal, localcontext
from fractions import Fraction
from time import perf_counter
import ctypes
import json
import numpy as np


ZERO = Decimal(0)
BASE = 'source-intake/navier-stokes/20260914/'


def pin(cpu):
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 1 << cpu):
        raise OSError('Affinity failed')


def metric_jets(solver, solution, radius):
    radius = np.asarray(radius, float)
    values, first = solver.values(solution, radius)
    indices = np.clip(np.searchsorted(solver.edges, radius, side='right') - 1, 0, len(solver.lengths) - 1)
    local = 2 * (radius - solver.centers[indices]) / solver.lengths[indices]
    second = []
    for component in range(2):
        coefficients = np.polynomial.chebyshev.chebder(solution['rhs_coefficients'][component], axis=-1)
        second.append(np.polynomial.chebyshev.chebval(local, coefficients[indices].T, tensor=False) * 2 / solver.lengths[indices])
    second = np.array(second)
    metric = 1 - 2 * values[0] / radius
    metric_first = -2 * first[0] / radius + 2 * values[0] / radius**2
    metric_second = -2 * second[0] / radius + 4 * first[0] / radius**2 - 4 * values[0] / radius**3
    speed = np.exp(2 * values[1]) * metric
    speed_first = speed * (2 * first[1] + metric_first / metric)
    factor = 2 / radius + first[1] + metric_first / (2 * metric)
    drift = speed * factor
    drift_first = speed_first * factor + speed * (-2 / radius**2 + second[1] + metric_second / (2 * metric) - metric_first**2 / (2 * metric**2))
    beta = radius**2 * np.exp(values[1]) * np.sqrt(metric)
    return dict(speed=decimal_array(speed), speed_first=decimal_array(speed_first), drift=decimal_array(drift),
        drift_first=decimal_array(drift_first), beta=decimal_array(beta), beta_first=decimal_array(beta * factor),
        metric_second=second)


def third(atom):
    powers = np.arange(atom['polynomial'].shape[1])
    return np.column_stack([6 * atom['polynomial'][:, 3] / atom['widths']**3,
        np.sum(atom['polynomial'] * powers * (powers - 1) * (powers - 2), axis=1) / atom['widths']**3])


def second_jet(rows, amounts, key):
    derivatives = [(row[key] - rows[0][key]) / Decimal.from_float(amount) for row, amount in zip(rows[1:], amounts)]
    coarse = (4 * derivatives[1] - derivatives[0]) / 3
    fine = (4 * derivatives[2] - derivatives[1]) / 3
    return fine, maximum(fine - coarse)


def main():
    pin(2)
    evidence = EvidenceRun('annular-septic-response-construction-attempt01', __file__)
    started, deadline = perf_counter(), perf_counter() + 3600
    try:
        parent = verify_report(evidence, BASE + 'annular-high-order-live-primary-attempt02/status.json')
        jet = verify_report(evidence, BASE + 'annular-high-order-time-jet-attempt01/status.json')
        original_mask = verify_report(evidence, BASE + 'annular-native-interface-transmission-attempt01/status.json')
        original_active = read_archive(evidence.root / next(row for row in original_mask['cases'] if row['level'] == 'third')['path'])['active']
        seal = evidence.output.parent / 'annular-high-order-source-separation-integrity-20261003.json'
        evidence.own(seal)
        digests = json.loads(seal.read_text())['hashes']
        map_path = evidence.output.parent / 'annular-source-split-septic-algebra-attempt01/exact-septic-endpoint-map.json'
        evidence.own(map_path)
        endpoint_map = json.loads(map_path.read_text())
        old_mesh = json.loads((evidence.root / parent['mesh_path']).read_text())
        acceleration = read_archive(evidence.root / next(row for row in parent['results'] if row['material'] == 64)['path'])['acceleration']
        new_mesh = high_mesh(old_mesh['gram_support'], old_mesh['anchor'], degree=7)
        evidence.report.update(progress={}, frozen_response_only=True, source_coupling_reinserted_in_native_targets=True,
            source_mean_third_rule='Preserve inherited mean; solve independent source jump.', github_action=False, subagents_used=False)
        with localcontext() as context:
            context.prec = 64
            unused, original, sources = restore_case(evidence, digests, 'MTS-primary', 'third', deadline)
            owner = adapt_owner(original.owner, old_mesh)
            labels = owner.layer_rule.points / 2
            rows, baseline = [], []
            for number, probe in enumerate(jet['probes']):
                evidence.report['progress'] = dict(stage='vertex jets ' + str(number), seconds=perf_counter() - started)
                evidence.save()
                state = read_archive(evidence.root / probe['path'])
                loads = HighLoads(owner, decimals(state['coordinates']), state['rates'], old_mesh, 'primary', deadline)
                solver, solution = reconstructed_solver(state)
                engine = loads.native_engine
                current = {name: [] for name in ['A', 'C', 'beta', 'T', 'J']}
                for vertex, label in enumerate(labels):
                    edges = physical_edges(engine, loads.coordinates[vertex, -1], label, owner.width)
                    geometry = metric_jets(solver, solution, np.asarray(edges[engine.native_edges], float))
                    result = engine.evaluate(edges, loads.coordinates[vertex, :-1], geometry['beta'], geometry['beta_first'])
                    for name, value in [('A', result['native_field']), ('C', result['native_shape']), ('beta', geometry['beta']),
                            ('T', result['jump_covector']), ('J', result['source_jump'])]:
                        current[name].append(value)
                    if number == 0:
                        baseline.append(dict(edges=edges, field=loads.coordinates[vertex, :-1].copy(), source=loads.coordinates[vertex, -1],
                            atom=result['atoms'], geometry=geometry, source_geometry=metric_jets(solver, solution, np.array([float(edges[engine.anchor])]))))
                rows.append({name: np.array(values, dtype=object) for name, values in current.items()})
            derivatives, spreads = {}, {}
            for name in rows[0]:
                derivatives[name], spreads[name] = second_jet(rows, jet['amounts'], name)
            new_engine = HighKernel(new_mesh, new_mesh['gram_support'], True)
            transform = np.array([[Decimal(Fraction(value).numerator) / Decimal(Fraction(value).denominator)
                for value in row] for row in endpoint_map['coefficients_by_power']], dtype=object)
            coordinates = np.full((len(labels), new_mesh['count'] + 1), ZERO, dtype=object)
            polynomials, frozen_residuals, targets, mask_rows, hinge_rows = [], [], [], [], []
            for vertex, row in enumerate(baseline):
                edges, field, atom, geometry = row['edges'], row['field'], row['atom'], row['geometry']
                native = edges[engine.native_edges]
                fraction = np.array([abs((point - row['source']) / ((edges[0] if point < row['source'] else edges[-1]) - row['source'])) for point in native])
                support = (fraction > Decimal('.18')) & (fraction < Decimal('.82'))
                kernel_support = np.array([np.any(support[index:index + 4]) for index in range(len(native) - 3)])
                image_support = np.asarray(abs(engine.template) @ kernel_support.astype(float) > 0).ravel()
                kernel_halo = np.asarray(abs(engine.template).T @ image_support.astype(float) > 0).ravel()
                active = np.asarray(abs(engine.sampling).T @ image_support.astype(float) > 0).ravel() | original_active
                for index in np.flatnonzero(kernel_halo):
                    active[index:index + 4] = True
                active[[0, -1]] = False
                evidence.check('vertex' + str(vertex) + ':no_active_zero_denominator', not np.any(rows[0]['A'][vertex, active] == 0))
                perturbation = np.full(engine.count, ZERO, dtype=object)
                source_cell = engine.anchor
                perturbation[engine.indices[source_cell, 1]] = atom['widths'][source_cell] / engine.basis.left_first[1]
                plus = engine.evaluate(edges, field + perturbation, geometry['beta'], geometry['beta_first'])
                minus = engine.evaluate(edges, field - perturbation, geometry['beta'], geometry['beta_first'])
                hinge_stiffness = (plus['jump_covector'] - minus['jump_covector']) / 2
                evidence.check('vertex' + str(vertex) + ':positive_source_hinge_stiffness', hinge_stiffness > 0, str(hinge_stiffness))
                source_delta = -derivatives['T'][vertex] / hinge_stiffness
                target_source_second = derivatives['J'][vertex] + source_delta
                corrected_A = derivatives['A'][vertex] + (plus['native_field'] - minus['native_field']) * source_delta / 2
                corrected_C = derivatives['C'][vertex] + (plus['native_shape'] - minus['native_shape']) * source_delta / 2
                endpoint_third = third(atom)
                selected = engine.native_edges[1:-1]
                before, after = atom['slope_right'][selected - 1], atom['slope_left'][selected]
                curvature_before, curvature_after = atom['curvature_right'][selected - 1], atom['curvature_left'][selected]
                displacement = np.array([(point - edges[0]) / (row['source'] - edges[0]) if point < row['source']
                    else (edges[-1] - point) / (edges[-1] - row['source']) for point in native], dtype=object)
                native_acceleration = displacement * Decimal.from_float(float(acceleration[vertex, -1]))
                coefficient_second = derivatives['beta'][vertex] - 2 * geometry['beta'] * native_acceleration**2 / geometry['speed']
                mean = (after + before) / 2
                target_mean = np.full(len(selected), ZERO, dtype=object)
                target_jump = np.full(len(selected), ZERO, dtype=object)
                chosen = active[1:-1]
                target_mean[chosen] = -(corrected_A[1:-1][chosen] * mean[chosen] + corrected_C[1:-1][chosen]) / rows[0]['A'][vertex, 1:-1][chosen]
                target_jump[chosen] = (corrected_A[1:-1][chosen] - coefficient_second[1:-1][chosen] * (after - before)[chosen]) / geometry['beta'][1:-1][chosen]
                factor = geometry['speed_first'] + geometry['drift'] + native_acceleration
                incoming = (target_mean - target_jump / 2 - factor[1:-1] * curvature_before - geometry['drift_first'][1:-1] * before) / geometry['speed'][1:-1]
                outgoing = (target_mean + target_jump / 2 - factor[1:-1] * curvature_after - geometry['drift_first'][1:-1] * after) / geometry['speed'][1:-1]
                endpoint_third[selected[chosen] - 1, 1] = incoming[chosen]
                endpoint_third[selected[chosen], 0] = outgoing[chosen]
                source_geometry = row['source_geometry']
                source_speed = source_geometry['speed'][0]
                source_factor = source_geometry['speed_first'][0] + source_geometry['drift'][0] + Decimal.from_float(float(acceleration[vertex, -1]))
                slope_jump = atom['slope_left'][engine.anchor] - atom['slope_right'][engine.anchor - 1]
                curvature_jump = atom['curvature_left'][engine.anchor] - atom['curvature_right'][engine.anchor - 1]
                source_ell_jump = (target_source_second - source_factor * curvature_jump - source_geometry['drift_first'][0] * slope_jump) / source_speed
                source_ell_mean = (endpoint_third[engine.anchor - 1, 1] + endpoint_third[engine.anchor, 0]) / 2
                endpoint_third[engine.anchor - 1, 1] = source_ell_mean - source_ell_jump / 2
                endpoint_third[engine.anchor, 0] = source_ell_mean + source_ell_jump / 2
                values = np.full(len(edges), ZERO, dtype=object)
                edge_indices = np.r_[engine.indices[:, 0], engine.indices[-1, -1]]
                values[edge_indices >= 0] = field[edge_indices[edge_indices >= 0]]
                width = atom['widths']
                endpoint_data = np.column_stack([values[:-1], width * atom['slope_left'], width**2 * atom['curvature_left'], width**3 * endpoint_third[:, 0],
                    values[1:], width * atom['slope_right'], width**2 * atom['curvature_right'], width**3 * endpoint_third[:, 1]])
                polynomial = endpoint_data @ transform.T
                generated = np.full(new_mesh['count'], ZERO, dtype=object)
                for local_index in range(8):
                    local = Decimal(local_index) / 7
                    evaluated = np.full(len(width), ZERO, dtype=object)
                    for power in reversed(range(8)):
                        evaluated = evaluated * local + polynomial[:, power]
                    indices = new_engine.indices[:, local_index]
                    generated[indices[indices >= 0]] = evaluated[indices >= 0]
                generated[new_engine.native_indices] = field[engine.native_indices]
                new_atom = new_engine.atoms(edges, generated)
                errors = [maximum(new_atom[key] - atom[key]) for key in ['slope_left', 'slope_right', 'curvature_left', 'curvature_right']]
                errors.append(maximum(third(new_atom) - endpoint_third))
                evidence.check('vertex' + str(vertex) + ':all_endpoint_jets_represented', max(errors) < Decimal('1e-28'), str(max(errors)))
                evidence.check('vertex' + str(vertex) + ':same_native_values', np.array_equal(generated[new_engine.native_indices], field[engine.native_indices]))
                evidence.check('vertex' + str(vertex) + ':source_value_pinned', abs(sum(polynomial[engine.anchor - 1], ZERO)) < Decimal('1e-45') and polynomial[engine.anchor, 0] == 0)
                mean_second = (geometry['speed'][1:-1] * (incoming + outgoing) + factor[1:-1] * (curvature_before + curvature_after) + geometry['drift_first'][1:-1] * (before + after)) / 2
                jump_second = geometry['speed'][1:-1] * (outgoing - incoming) + factor[1:-1] * (curvature_after - curvature_before) + geometry['drift_first'][1:-1] * (after - before)
                point_residual = rows[0]['A'][vertex, 1:-1] * mean_second + corrected_A[1:-1] * mean + corrected_C[1:-1]
                jump_residual = geometry['beta'][1:-1] * jump_second + coefficient_second[1:-1] * (after - before) - corrected_A[1:-1]
                source_residual = derivatives['T'][vertex] + hinge_stiffness * source_delta
                evidence.check('vertex' + str(vertex) + ':frozen_target_equations', max(maximum(point_residual[chosen]), maximum(jump_residual[chosen]), abs(source_residual)) < Decimal('1e-35'))
                coordinates[vertex, :-1], coordinates[vertex, -1] = generated, row['source']
                polynomials.append(np.asarray(polynomial, str))
                targets.append(np.asarray(endpoint_third, str))
                mask_rows.append(active)
                frozen_residuals.append([float(maximum(point_residual[chosen])), float(maximum(jump_residual[chosen])), float(source_residual)])
                hinge_rows.append([str(hinge_stiffness), str(derivatives['T'][vertex]), str(source_delta), str(target_source_second), str(source_ell_jump)])
            evidence.check('parent_vertices_and_support', len(labels) == 15 and new_mesh['gram_support'] == old_mesh['gram_support'])
            path = evidence.output / 'P7-initial.npz'
            np.savez_compressed(path, coordinates=np.asarray(coordinates, str), rates=np.zeros(coordinates.shape), polynomial=polynomials,
                endpoint_third=targets, active=mask_rows, frozen_residuals=frozen_residuals, source_targets=hinge_rows, labels=labels,
                **{'second_' + key: np.asarray(value, str) for key, value in derivatives.items()})
            evidence.own(path, 'outputs')
            mesh_path = evidence.output / 'P7-mesh.json'
            mesh_path.write_text(json.dumps(new_mesh) + '\n')
            evidence.own(mesh_path, 'outputs')
            evidence.report.update(initial_path=str(path.relative_to(evidence.root)), mesh_path=str(mesh_path.relative_to(evidence.root)),
                field_count=new_mesh['count'], material_vertices=len(labels), seconds=perf_counter() - started,
                Richardson_spreads={key: str(value) for key, value in spreads.items()},
                maximum_third_jet=float(np.max(abs(np.asarray(targets, float)))), maximum_source_jump_correction=float(np.max(abs(np.asarray(hinge_rows, float)[:, 2]))),
                own_metric_solved=False, full_acceleration_solved=False, live_preservation_test_pending=True,
                inactive_nodes_not_divided=True, target_response='Inherited P6 weak acceleration, source Schur correction reinserted; requires new coupled feedback.')
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
