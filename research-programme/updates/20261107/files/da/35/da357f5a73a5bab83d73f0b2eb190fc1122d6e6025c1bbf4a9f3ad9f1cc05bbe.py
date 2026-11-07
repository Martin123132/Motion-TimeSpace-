from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_acceleration_archive_checks_v2_20261001 import verify_report
from annular_high_order_native_v2_20261003 import adapt_owner, HighKernel
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_candidate_hamiltonian_20260921 import decimals
from annular_decimal_transport_v2_20260919 import decimal_array
from annular_quadratic_core_20261002 import physical_edges
from annular_physical_native_kernel_20260928 import maximum
from analyze_annular_source_flat_state_20261002 import read_archive
from construct_annular_septic_response_20261003 import pin, metric_jets, third, second_jet
from decimal import Decimal, localcontext
from fractions import Fraction
from time import perf_counter
import json
import numpy as np


def main():
    pin(2)
    evidence = EvidenceRun('annular-all-native-jump-construction-attempt02', __file__)
    started, deadline = perf_counter(), perf_counter() + 3600
    try:
        base = 'source-intake/navier-stokes/20260914/'
        live = verify_report(evidence, base + 'annular-septic-source-corrected-live-primary-attempt01/status.json')
        jet = verify_report(evidence, base + 'annular-septic-source-corrected-time-response-attempt01/status.json')
        original = verify_report(evidence, base + 'annular-septic-response-construction-attempt01/status.json')
        active = read_archive(evidence.root / original['initial_path'])['active']
        seal = evidence.output.parent / 'annular-septic-coupled-response-integrity-20261003.json'
        evidence.own(seal)
        digests = json.loads(seal.read_text())['hashes']
        mesh = json.loads((evidence.root / live['mesh_path']).read_text())
        saved = read_archive(evidence.root / live['states'][0]['path'])
        high = next(row for row in live['results'] if row['material'] == 64)
        acceleration = read_archive(evidence.root / high['path'])['acceleration']
        map_path = evidence.output.parent / 'annular-source-split-septic-algebra-attempt01/exact-septic-endpoint-map.json'
        evidence.own(map_path)
        endpoint_map = json.loads(map_path.read_text())
        reference = list(map(Fraction, mesh['gram_support']))
        moment_error = Fraction(0)
        for first in range(len(reference) - 3):
            points = reference[first:first + 4]
            weights = []
            for index, point in enumerate(points):
                denominator = Fraction(1)
                for other, target in enumerate(points):
                    if other != index:
                        denominator *= point - target
                weights.append(1 / denominator)
            for power in range(3):
                moment_error = max(moment_error, abs(sum(weight * point**power for weight, point in zip(weights, points))))
        evidence.check('exact_quadratic_kernel_identity_all_reference_windows', moment_error == 0)
        evidence.report.update(mesh_path=live['mesh_path'], progress={}, all_ordinary_native_jumps_targeted=True,
            no_division_by_A=True, source_third_jets_preserved=True, metric_response_frozen=True,
            exact_zero_load_not_assumed_from_mask=True, github_action=False, subagents_used=False)
        with localcontext() as context:
            context.prec = 75
            unused, original_action, sources = restore_case(evidence, digests, 'MTS-primary', 'third', deadline)
            owner = adapt_owner(original_action.owner, mesh)
            labels = owner.layer_rule.points / 2
            coordinates = decimals(saved['coordinates'])
            engine = HighKernel(mesh, mesh['gram_support'], True)
            transform = np.array([[Decimal(Fraction(value).numerator) / Decimal(Fraction(value).denominator) for value in row]
                for row in endpoint_map['coefficients_by_power']], dtype=object)
            rows, baseline = [], []
            for number, probe in enumerate(jet['probes']):
                state = read_archive(evidence.root / probe['path'])
                current_coordinates = decimals(state['coordinates'])
                solver, solution = reconstructed_solver(state)
                current = {key: [] for key in ['A', 'C', 'beta']}
                for vertex, label in enumerate(labels):
                    edges = physical_edges(engine, current_coordinates[vertex, -1], label, owner.width)
                    geometry = metric_jets(solver, solution, np.asarray(edges[engine.native_edges], float))
                    result = engine.evaluate(edges, current_coordinates[vertex, :-1], geometry['beta'], geometry['beta_first'])
                    current['A'].append(result['native_field'])
                    current['C'].append(result['native_shape'])
                    current['beta'].append(geometry['beta'])
                    if number == 0:
                        baseline.append(dict(edges=edges, geometry=geometry, atom=result['atoms']))
                rows.append({key: np.array(value, dtype=object) for key, value in current.items()})
                evidence.report['progress'] = dict(stage='material-vertex response ' + str(number), seconds=perf_counter() - started)
                evidence.save()
            derivatives, spreads = {}, {}
            for key in rows[0]:
                derivatives[key], spreads[key] = second_jet(rows, jet['amounts'], key)
            changed = coordinates.copy()
            target_rows, polynomial_rows, statistics = [], [], []
            selected = engine.native_edges[1:-1]
            for vertex, row in enumerate(baseline):
                edges, geometry, atom = row['edges'], row['geometry'], row['atom']
                native = edges[engine.native_edges]
                source = coordinates[vertex, -1]
                displacement = np.array([(point - edges[0]) / (source - edges[0]) if point <= source
                    else (edges[-1] - point) / (edges[-1] - source) for point in native], dtype=object)
                native_acceleration = displacement * Decimal.from_float(float(acceleration[vertex, -1]))
                before, after = atom['slope_right'][selected - 1], atom['slope_left'][selected]
                curvature_before, curvature_after = atom['curvature_right'][selected - 1], atom['curvature_left'][selected]
                slope_jump = after - before
                coefficient_second = derivatives['beta'][vertex] - 2 * geometry['beta'] * native_acceleration**2 / geometry['speed']
                required_jump_second = (derivatives['A'][vertex, 1:-1] - coefficient_second[1:-1] * slope_jump) / geometry['beta'][1:-1]
                factor = geometry['speed_first'] + geometry['drift'] + native_acceleration
                target_jump = (required_jump_second - factor[1:-1] * (curvature_after - curvature_before)
                    - geometry['drift_first'][1:-1] * slope_jump) / geometry['speed'][1:-1]
                endpoint_third = third(atom)
                mean = (endpoint_third[selected - 1, 1] + endpoint_third[selected, 0]) / 2
                endpoint_third[selected - 1, 1] = mean - target_jump / 2
                endpoint_third[selected, 0] = mean + target_jump / 2
                evidence.check('vertex' + str(vertex) + ':exact_original_zero_outer_cells', not np.any(atom['polynomial'][[0, -1]]))
                evidence.report.setdefault('outer_neighbour_forces', []).append(dict(vertex=vertex, A=list(map(str, rows[0]['A'][vertex, [1, -2]])), C=list(map(str, rows[0]['C'][vertex, [1, -2]]))))
                endpoint_third[0] = Decimal(0)
                endpoint_third[1, 0] = target_jump[0]
                endpoint_third[-1] = Decimal(0)
                endpoint_third[-2, 1] = -target_jump[-1]
                changed_mean = (endpoint_third[selected - 1, 1] + endpoint_third[selected, 0]) / 2
                point_increment = rows[0]['A'][vertex, 1:-1] * geometry['speed'][1:-1] * (changed_mean - mean)
                evidence.check('vertex' + str(vertex) + ':boundary_mean_point_increment', maximum(point_increment) < Decimal('1e-35'), str(maximum(point_increment)))
                edge_indices = np.r_[engine.indices[:, 0], engine.indices[-1, -1]]
                values = np.full(len(edges), Decimal(0), dtype=object)
                values[edge_indices >= 0] = coordinates[vertex, edge_indices[edge_indices >= 0]]
                widths = atom['widths']
                endpoint_data = np.column_stack([values[:-1], widths * atom['slope_left'], widths**2 * atom['curvature_left'], widths**3 * endpoint_third[:, 0],
                    values[1:], widths * atom['slope_right'], widths**2 * atom['curvature_right'], widths**3 * endpoint_third[:, 1]])
                polynomial = endpoint_data @ transform.T
                generated = np.full(engine.count, Decimal(0), dtype=object)
                for local_index in range(8):
                    local = Decimal(local_index) / 7
                    evaluated = np.full(len(widths), Decimal(0), dtype=object)
                    for power in reversed(range(8)):
                        evaluated = evaluated * local + polynomial[:, power]
                    indices = engine.indices[:, local_index]
                    generated[indices[indices >= 0]] = evaluated[indices >= 0]
                generated[engine.native_indices] = coordinates[vertex, engine.native_indices]
                new_atom = engine.atoms(edges, generated)
                errors = [maximum(new_atom[key] - atom[key]) for key in ['slope_left', 'slope_right', 'curvature_left', 'curvature_right']]
                errors.append(maximum(third(new_atom) - endpoint_third))
                evidence.check('vertex' + str(vertex) + ':all_endpoint_jets', max(errors) < Decimal('1e-35'), str(max(errors)))
                evidence.check('vertex' + str(vertex) + ':exact_outer_buffer_retained', not np.any(new_atom['polynomial'][[0, -1]]))
                evidence.check('vertex' + str(vertex) + ':source_third_jets_retained',
                    abs(endpoint_third[engine.anchor - 1, 1] - third(atom)[engine.anchor - 1, 1]) < Decimal('1e-55') and
                    abs(endpoint_third[engine.anchor, 0] - third(atom)[engine.anchor, 0]) < Decimal('1e-55'))
                jump_second = geometry['speed'][1:-1] * (endpoint_third[selected, 0] - endpoint_third[selected - 1, 1])
                jump_second += factor[1:-1] * (curvature_after - curvature_before) + geometry['drift_first'][1:-1] * slope_jump
                residual = geometry['beta'][1:-1] * jump_second + coefficient_second[1:-1] * slope_jump - derivatives['A'][vertex, 1:-1]
                evidence.check('vertex' + str(vertex) + ':all_frozen_jump_targets', maximum(residual) < Decimal('1e-45'), str(maximum(residual)))
                inactive = ~active[vertex, 1:-1]
                quiet_compatibility = derivatives['C'][vertex, 1:-1] + (after + before) * derivatives['A'][vertex, 1:-1] / 2
                statistics.append(dict(label=float(labels[vertex]), inactive_initial_A=str(maximum(rows[0]['A'][vertex, 1:-1][inactive])),
                    inactive_initial_C=str(maximum(rows[0]['C'][vertex, 1:-1][inactive])), inactive_initial_slope_jump=str(maximum(slope_jump[inactive])),
                    inactive_initial_curvature_jump=str(maximum((curvature_after - curvature_before)[inactive])),
                    inactive_point_compatibility_second=str(maximum(quiet_compatibility[inactive])),
                    maximum_third_jump_change=str(maximum(target_jump - (third(atom)[selected, 0] - third(atom)[selected - 1, 1])))))
                changed[vertex, :-1] = generated
                target_rows.append(np.asarray(endpoint_third, str))
                polynomial_rows.append(np.asarray(polynomial, str))
            path = evidence.output / 'P7-all-native-jump-initial.npz'
            np.savez_compressed(path, coordinates=np.asarray(changed, str), rates=np.zeros(changed.shape), endpoint_third=target_rows,
                polynomial=polynomial_rows, labels=labels, active=active, **{'second_' + key: np.asarray(value, str) for key, value in derivatives.items()})
            evidence.own(path, 'outputs')
            evidence.report.update(initial_path=str(path.relative_to(evidence.root)), field_count=engine.count, material_vertices=len(labels),
                seconds=perf_counter() - started, statistics=statistics, Richardson_spreads={key: str(value) for key, value in spreads.items()},
                exact_quadratic_identity_does_not_imply_stored_profile_exact_zero=True, mean_third_preserved_except_two_zero_outer_buffer_neighbours=True,
                outer_buffer_neighbour_jump_equations_retained=True, exact_outer_neighbour_zero_force_claimed=False, boundary_mean_point_increment_gate='1e-35', all_native_values_and_lower_jets_preserved=True,
                own_metric_solved=False, full_acceleration_solved=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
