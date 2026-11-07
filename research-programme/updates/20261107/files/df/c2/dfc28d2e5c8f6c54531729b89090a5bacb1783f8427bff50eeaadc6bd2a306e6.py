from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_acceleration_archive_checks_v2_20261001 import verify_report
from annular_high_order_native_v2_20261003 import adapt_owner, HighLoads, HighAction, HighInverse
from annular_product_live_20261003 import install_product_basis
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_candidate_hamiltonian_20260921 import decimals
from annular_decimal_transport_v2_20260919 import decimal_array
from annular_quadratic_core_20261002 import physical_edges
from annular_physical_native_kernel_20260928 import maximum
from analyze_annular_source_flat_state_20261002 import read_archive
from construct_annular_septic_response_20261003 import pin, metric_jets, third
from scipy.sparse import load_npz
from decimal import Decimal, localcontext
from fractions import Fraction
from time import perf_counter
import json
import numpy as np


def main():
    pin(2)
    evidence = EvidenceRun('annular-product-source-feedback-attempt01', __file__)
    started, deadline = perf_counter(), perf_counter() + 5400
    try:
        base = 'source-intake/navier-stokes/20260914/'
        live = verify_report(evidence, base + 'annular-product-basis-live-primary-attempt02/status.json')
        jet = verify_report(evidence, base + 'annular-product-basis-balanced-time-response-attempt01/status.json')
        evidence.check('source_feedback_required', live['initial_candidate'] and jet['P7_over_P6']['source'] > 1)
        seal = evidence.output.parent / 'annular-high-order-source-separation-integrity-20261003.json'
        evidence.own(seal)
        digests = json.loads(seal.read_text())['hashes']
        mesh = json.loads((evidence.root / live['mesh_path']).read_text())
        saved = read_archive(evidence.root / live['states'][0]['path'])
        high = next(row for row in live['balanced_results'] if row['material'] == 64)
        arrays = read_archive(evidence.root / high['path'])
        acceleration = arrays['acceleration']
        matrix = load_npz(evidence.root / high['matrix_path'])
        endpoint_path = evidence.output.parent / 'annular-source-split-septic-algebra-attempt01/exact-septic-endpoint-map.json'
        evidence.own(endpoint_path)
        endpoint_map = json.loads(endpoint_path.read_text())
        with localcontext() as context:
            context.prec = 64
            unused, original, sources = restore_case(evidence, digests, 'MTS-primary', 'third', deadline)
            owner = adapt_owner(original.owner, mesh)
            coordinates = decimals(saved['coordinates'])
            loads = HighLoads(owner, coordinates, saved['rates'], mesh, 'primary', deadline)
            solver, solution = reconstructed_solver(saved)
            install_product_basis(loads)
            action = HighAction(loads, mesh, solver, solution)
            engine = loads.native_engine
            count, labels = engine.count, owner.layer_rule.points / 2
            transform = np.array([[Decimal(Fraction(value).numerator) / Decimal(Fraction(value).denominator) for value in row]
                for row in endpoint_map['coefficients_by_power']], dtype=object)
            directions = np.full((len(labels), count), Decimal(0), dtype=object)
            observations, source_geometry_rows = [], []
            for vertex, label in enumerate(labels):
                edges = physical_edges(engine, coordinates[vertex, -1], label, owner.width)
                atom = engine.atoms(edges, coordinates[vertex, :-1])
                for cell, endpoint, sign in [(engine.anchor - 1, 7, Decimal('-.5')), (engine.anchor, 3, Decimal('.5'))]:
                    values = np.full(8, Decimal(0), dtype=object)
                    values[endpoint] = sign * atom['widths'][cell]**3
                    polynomial = transform @ values
                    for local_index, node in enumerate(engine.indices[cell]):
                        if node >= 0:
                            local = Decimal(local_index) / 7
                            directions[vertex, node] = sum((coefficient * (local**power if power else 1) for power, coefficient in enumerate(polynomial)), Decimal(0))
                directions[vertex, engine.native_indices] = Decimal(0)
                lift_atom = engine.atoms(edges, directions[vertex])
                evidence.check('vertex' + str(vertex) + ':source_lift_lower_jets_zero', max(maximum(lift_atom[key]) for key in ['slope_left', 'slope_right', 'curvature_left', 'curvature_right']) < Decimal('1e-45'))
                evidence.check('vertex' + str(vertex) + ':unit_source_third_jump', abs(third(lift_atom)[engine.anchor, 0] - third(lift_atom)[engine.anchor - 1, 1] - 1) < Decimal('1e-45'))
                geometry = metric_jets(solver, solution, np.asarray(edges[engine.native_edges], float))
                perturbation = np.full(count, Decimal(0), dtype=object)
                perturbation[engine.indices[engine.anchor, 1]] = atom['widths'][engine.anchor] / engine.basis.left_first[1]
                response = engine.evaluate(edges, perturbation, geometry['beta'], geometry['beta_first'])
                covector = np.full(count, Decimal(0), dtype=object)
                covector[engine.native_indices] = response['native_field']
                for cell, weights, sign in [(engine.anchor - 1, engine.basis.right_first, -1), (engine.anchor, engine.basis.left_first, 1)]:
                    selected = engine.indices[cell] >= 0
                    covector[engine.indices[cell, selected]] += sign * response['jump_covector'] * weights[selected] / atom['widths'][cell]
                displacement = np.array([(point - edges[0]) / (coordinates[vertex, -1] - edges[0]) if point <= coordinates[vertex, -1]
                    else (edges[-1] - point) / (edges[-1] - coordinates[vertex, -1]) for point in edges], dtype=object)
                derivative_estimates = []
                for step in [Decimal('1e-5'), Decimal('5e-6')]:
                    values = []
                    for sign in [-1, 1]:
                        values.append(engine.evaluate(edges + sign * step * displacement, coordinates[vertex, :-1],
                            geometry['beta'] + sign * step * geometry['beta_first'] * displacement[engine.native_edges])['jump_covector'])
                    derivative_estimates.append((values[1] - values[0]) / (2 * step))
                source_derivative = (4 * derivative_estimates[1] - derivative_estimates[0]) / 3
                observations.append(np.asarray(covector, float))
                source_geometry_rows.append(float(source_derivative))
            source_jets = []
            for probe in jet['probes']:
                archive = read_archive(evidence.root / probe['path'])
                jet_coordinates = decimals(archive['coordinates'])
                jet_solver, jet_solution = reconstructed_solver(archive)
                values = []
                for vertex, label in enumerate(labels):
                    edges = physical_edges(engine, jet_coordinates[vertex, -1], label, owner.width)
                    geometry = metric_jets(jet_solver, jet_solution, np.asarray(edges[engine.native_edges], float))
                    values.append(engine.evaluate(edges, jet_coordinates[vertex, :-1], geometry['beta'])['jump_covector'])
                source_jets.append(np.array(values, dtype=object))
            derivatives = [(values - source_jets[0]) / Decimal.from_float(amount) for values, amount in zip(source_jets[1:], jet['amounts'])]
            target = np.asarray((4 * derivatives[2] - derivatives[1]) / 3, float)
            gradient = engine.basis.polynomial(engine.indices, directions.T)[:, 1:] * np.arange(1, 8)[None, :, None]
            widths = np.array([Decimal(Fraction(upper).numerator) / Decimal(Fraction(upper).denominator) - Decimal(Fraction(lower).numerator) / Decimal(Fraction(lower).denominator)
                for lower, upper in zip(mesh['edges'][:-1], mesh['edges'][1:])], dtype=object)
            gradient = np.asarray(gradient / widths[:, None, None], float)
        observations, source_geometry_rows = np.array(observations), np.array(source_geometry_rows)
        right_hand = np.zeros(acceleration.shape + (len(labels),))
        points, weights = np.polynomial.legendre.leggauss(64)
        points, weights = points / 2, weights / 2
        weights *= 6 * (points + .5) * (.5 - points)
        for number, (label, weight) in enumerate(zip(points, weights)):
            if perf_counter() > deadline:
                raise RuntimeError('Source-feedback assembly deadline')
            row = action.samples(label, 16)
            quad, geometry, cardinal = row['quadrature'], row['geometry'], row['cardinal']
            selected = (quad['cells'] == engine.anchor - 1) | (quad['cells'] == engine.anchor)
            cells, local = quad['cells'][selected], quad['local'][selected]
            delta_gradient = np.zeros((len(cells), len(labels)))
            for power in reversed(range(7)):
                delta_gradient = delta_gradient * local[:, None] + gradient[cells, power]
            delta_gradient *= cardinal
            measure, indices, shape, radial = quad['measure'][selected], quad['indices'][selected], quad['shape'][selected], quad['radial'][selected]
            delta_motion = -geometry['displacement'][selected, None] * delta_gradient / geometry['jacobian'][selected, None]
            source_acceleration = cardinal @ acceleration[:, -1]
            field_acceleration = np.sum(shape * (cardinal @ acceleration[:, :-1])[indices], axis=1)
            field_values = np.zeros((count, len(labels)))
            for local_index in range(8):
                values = -measure[:, None] * (geometry['gradient'][selected, None] * delta_gradient * radial[:, local_index, None]
                    + geometry['kinetic'][selected, None] * delta_motion * source_acceleration * shape[:, local_index, None])
                np.add.at(field_values, indices[:, local_index], values)
            source_values = np.sum(-measure[:, None] * (geometry['gradient_source'][selected, None] * row['gradient'][selected, None] * delta_gradient
                + geometry['kinetic'][selected, None] * delta_motion * (field_acceleration + 2 * row['motion'][selected] * source_acceleration)[:, None]), axis=0)
            right_hand[:, :-1] += weight * cardinal[:, None, None] * field_values[None]
            right_hand[:, -1] += weight * cardinal[:, None] * source_values[None]
        inverse = HighInverse(matrix, acceleration.shape, 7)
        linear_acceleration = inverse.solve(right_hand.reshape(acceleration.size, len(labels))).reshape(acceleration.shape + (len(labels),))
        error = matrix @ linear_acceleration.reshape(acceleration.size, len(labels)) - right_hand.reshape(acceleration.size, len(labels))
        relative = float(np.max(abs(error)) / np.max(abs(right_hand)))
        evidence.check('complete_fixed_metric_Hessian_tangent', relative < 2e-10, relative)
        response_matrix = np.einsum('ij,ijk->ik', observations, linear_acceleration[:, :-1], optimize=False)
        response_matrix += source_geometry_rows[:, None] * linear_acceleration[:, -1]
        condition = float(np.linalg.cond(response_matrix))
        evidence.check('full_rank_source_response_without_regularization', np.isfinite(condition) and condition < 1e8, condition)
        correction = np.linalg.solve(response_matrix, -target)
        residual = response_matrix @ correction + target
        evidence.check('source_response_equations', np.max(abs(residual)) < 1e-12 * np.max(abs(target)), float(np.max(abs(residual))))
        with localcontext() as context:
            context.prec = 64
            changed = coordinates.copy()
            changed[:, :-1] += decimal_array(correction)[:, None] * directions
            for vertex, label in enumerate(labels):
                edges = physical_edges(engine, coordinates[vertex, -1], label, owner.width)
                before, after = engine.atoms(edges, coordinates[vertex, :-1]), engine.atoms(edges, changed[vertex, :-1])
                evidence.check('vertex' + str(vertex) + ':lower_jet_preservation', max(maximum(before[key] - after[key]) for key in ['slope_left', 'slope_right', 'curvature_left', 'curvature_right']) < Decimal('1e-35'))
                evidence.check('vertex' + str(vertex) + ':native_values_preserved', np.array_equal(coordinates[vertex, engine.native_indices], changed[vertex, engine.native_indices]))
        path = evidence.output / 'P7-source-corrected-initial.npz'
        np.savez_compressed(path, coordinates=np.asarray(changed, str), rates=np.zeros(changed.shape), correction=correction,
            response_matrix=response_matrix, target=target, residual=residual, labels=labels,
            directions=np.asarray(directions, str), linear_acceleration=linear_acceleration, tangent_rhs=right_hand)
        evidence.own(path, 'outputs')
        evidence.report.update(initial_path=str(path.relative_to(evidence.root)), mesh_path=live['mesh_path'], seconds=perf_counter() - started,
            response_condition=condition, source_residual_before=float(np.max(abs(target))), source_residual_predicted=float(np.max(abs(residual))),
            maximum_third_jump_correction=float(np.max(abs(correction))), complete_Hessian_tangent=True, product_basis_used=True, baseline_force_form='balanced',
            tangent_includes_source_inertia_and_cross_block=True, metric_feedback_frozen=True, fresh_live_test_required=True,
            arbitrary_fitted_physics_coefficient=False, direct_product_tangent_of_equivalent_balanced_force=True, github_action=False, subagents_used=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
