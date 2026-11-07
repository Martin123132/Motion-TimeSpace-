from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_acceleration_archive_checks_v2_20261001 import verify_report
from analyze_annular_source_flat_state_20261002 import read_archive
from annular_high_order_native_v2_20261003 import adapt_owner, HighLoads, HighAction, maximum
from annular_candidate_hamiltonian_20260921 import decimals
from annular_candidate_energy_current_20260921 import reconstructed_solver
from derive_annular_native_shape_stress_20260928 import physical_data
from scipy.sparse import load_npz
from decimal import Decimal, localcontext
from time import perf_counter
import csv
import ctypes
import json
import numpy as np
import sympy as sp
from fractions import Fraction
from annular_high_order_native_v2_20261003 import PolynomialBasis


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 1 << 4):
        raise OSError('Affinity failed')
    evidence = EvidenceRun('annular-septic-live-analysis-attempt01', __file__)
    deadline = perf_counter() + 6000
    try:
        evidence.own(evidence.root / 'DERIVATION-20261003-explicit-third-jet-preservation-update.md')
        speed, coefficient, drift_radial, mean_rate, jump_rate, curvature_minus, curvature_plus, slope_minus, slope_plus = sp.symbols(
            'speed coefficient drift_radial mean_rate jump_rate curvature_minus curvature_plus slope_minus slope_plus')
        third_minus = (mean_rate - jump_rate / 2 - coefficient * curvature_minus - drift_radial * slope_minus) / speed
        third_plus = (mean_rate + jump_rate / 2 - coefficient * curvature_plus - drift_radial * slope_plus) / speed
        minus_rate = speed * third_minus + coefficient * curvature_minus + drift_radial * slope_minus
        plus_rate = speed * third_plus + coefficient * curvature_plus + drift_radial * slope_plus
        evidence.check('third_jet_update_mean', sp.simplify((plus_rate + minus_rate) / 2 - mean_rate) == 0)
        evidence.check('third_jet_update_jump', sp.simplify(plus_rate - minus_rate - jump_rate) == 0)
        coordinate = sp.Symbol('coordinate')
        bubble = coordinate**4 * (1 - coordinate)**4
        evidence.check('degree8_source_bubble_native_jets_through3', all(sp.diff(bubble, coordinate, order).subs(coordinate, endpoint) == 0
            for endpoint in [0, 1] for order in range(4)))
        basis = PolynomialBasis(7)
        exact_nodes = [Fraction(index, 7) for index in range(8)]
        for column in range(8):
            values = [sum(basis.rational[power, column] * node**power for power in range(8)) for node in exact_nodes]
            evidence.check('P7_exact_cardinality_' + str(column), values == [int(index == column) for index in range(8)])
        for degree in range(8):
            polynomial = basis.rational @ np.array([node**degree for node in exact_nodes], dtype=object)
            evidence.check('P7_exact_monomial_' + str(degree), list(polynomial) == [int(power == degree) for power in range(8)])
        base = 'source-intake/navier-stokes/20260914/'
        prepared = verify_report(evidence, base + 'annular-septic-response-construction-attempt01/status.json')
        adapter = verify_report(evidence, base + 'annular-high-order-adapter-validation-attempt02/status.json')
        parents = {branch: verify_report(evidence, base + 'annular-septic-live-' + branch + '-attempt01/status.json')
            for branch in ['primary', 'reference']}
        initial = read_archive(evidence.root / prepared['initial_path'])
        mesh = json.loads((evidence.root / prepared['mesh_path']).read_text())
        states, arrays, summary = {}, {}, []
        for branch, parent in parents.items():
            evidence.check(branch + ':complete', parent['state'] == 'complete')
            state = read_archive(evidence.root / parent['states'][0]['path'])
            states[branch] = state
            evidence.check(branch + ':actual_profile_unchanged', np.array_equal(state['coordinates'], initial['coordinates']))
            evidence.check(branch + ':zero_initial_rates', not np.any(state['rates']))
            for row in parent['results']:
                data = read_archive(evidence.root / row['path'])
                arrays[(branch, row['material'])] = data
                matrix = load_npz(evidence.root / row['matrix_path']).tocsr()
                prefix = row['name']
                evidence.check(prefix + ':finite_arrays', all(np.all(np.isfinite(value)) for value in data.values() if value.dtype.kind in 'fc'))
                evidence.check(prefix + ':complete_dimensions', matrix.shape == (data['force'].size,) * 2 and data['shape_layers'].shape == (row['material'], 33))
                error = matrix @ data['acceleration'].ravel() - data['force'].ravel()
                scale = np.max(abs(data['force']))
                evidence.check(prefix + ':Euler_replay', np.max(abs(error)) / scale < 2e-10, float(np.max(abs(error)) / scale))
                difference = matrix - matrix.T
                evidence.check(prefix + ':symmetric_mass', max(abs(difference.data), default=0.) < 2e-13)
                momentum = (matrix @ data['momentum_direction'].ravel()).reshape(data['force'].shape)
                oracle = float(np.max(abs(momentum - data['momentum_direct'])) / np.max(abs(momentum)))
                evidence.check(prefix + ':momentum_oracle_replay', oracle < 2e-11, oracle)
                selected = np.unique(np.r_[np.linspace(0, data['force'].size - 1, 33, dtype=int),
                    np.arange(data['force'].shape[0]) * data['force'].shape[1] + data['force'].shape[1] - 1])
                decimal_error = Decimal(0)
                with localcontext() as context:
                    context.prec = 75
                    for index in selected:
                        start, end = matrix.indptr[index:index + 2]
                        total = sum((Decimal.from_float(float(value)) * Decimal.from_float(float(data['acceleration'].ravel()[column]))
                            for value, column in zip(matrix.data[start:end], matrix.indices[start:end])), Decimal(0))
                        decimal_error = max(decimal_error, abs(total - Decimal.from_float(float(data['force'].ravel()[index]))))
                evidence.check(prefix + ':independent_75digit_rows', float(decimal_error) / scale < 2e-10, float(decimal_error) / scale)
                corner = data['native_speed_square'] * data['native_curvature_jumps']
                corner += (data['native_drift'] + data['native_displacement'] * data['source_acceleration'][:, None]) * data['native_slope_jumps']
                evidence.check(prefix + ':curvature_equation_replay', np.array_equal(corner, data['native_corner']))
                trace = data['speed_square'][:, None] * data['curvatures'] + (data['drift'] + data['source_acceleration'])[:, None] * data['slopes']
                evidence.check(prefix + ':source_equation_replay', np.array_equal(trace, data['trace']))
                evidence.check(prefix + ':shape_integral_replay',
                    abs(float(np.max(abs(data['weights'] @ data['shape_layers']))) - row['integrated_shape_force_max']) < 1e-32)
                evidence.check(prefix + ':energy_integral_replay',
                    abs(float(data['weights'] @ data['native_energy_layers']) - row['native_energy']) < 1e-25)
                evidence.check(prefix + ':outer_flux', not np.any(data['boundary_force']))
                evidence.check(prefix + ':force_split', np.max(abs(data['force'] - data['wave_source_force'] - data['native_force'])) < 1e-17)
                if branch == 'reference':
                    evidence.check(prefix + ':native_structurally_absent', not np.any(data['native_force']) and not np.any(data['native_energy_layers']))
                summary.append(dict(branch=branch, spatial=row['spatial'], material=row['material'],
                    Euler_relative=row['Euler_relative'], source_corner=row['maximum_trace_residual'],
                    native_curvature_corner=row['maximum_native_curvature_corner'], point_relative=row['relative_point_residual'],
                    jump_relative=row['relative_jump_residual'], shape_max=row['maximum_shape_force'],
                    native_energy=row['native_energy'], max_acceleration=row['maximum_acceleration'],
                    initial_candidate=row['initial_candidate'], valid_for_claim=False))
        evidence.check('matched_reference_same_initial_data', np.array_equal(states['primary']['coordinates'], states['reference']['coordinates']))
        seal = evidence.output.parent / 'annular-high-order-source-separation-integrity-20261003.json'
        evidence.own(seal)
        digests = json.loads(seal.read_text())['hashes']
        with localcontext() as context:
            context.prec = 75
            unused, original, sources = restore_case(evidence, digests, 'MTS-primary', 'third', deadline)
            owner = adapt_owner(original.owner, mesh)
            loads = HighLoads(owner, decimals(initial['coordinates']), initial['rates'], mesh, 'primary', deadline)
            solver, solution = reconstructed_solver(states['primary'])
            action = HighAction(loads, mesh, solver, solution)
            engine = loads.native_engine
            for label in [-.5, 0., .5]:
                data = physical_data(engine, loads, action, label)
                for variant in ['actual', 'source_jump_control']:
                    field = data['field'].copy()
                    if variant == 'source_jump_control':
                        field[engine.indices[engine.anchor, 1]] += Decimal('1e-13')
                    native = data['edges'][engine.native_edges]
                    result = engine.evaluate(data['edges'], field, 1 + native**2, 2 * native)
                    edge_direction = (data['edges'] - data['edges'][0]) * (data['edges'][-1] - data['edges']) / 100
                    field_direction = field / 7
                    expected = sum(result['field_gradient'] * field_direction, Decimal(0)) + sum(result['edge_gradient'] * edge_direction, Decimal(0))
                    differences = []
                    for step in [Decimal('1e-5'), Decimal('5e-6')]:
                        energy = []
                        for sign in [-1, 1]:
                            edges = data['edges'] + sign * step * edge_direction
                            energy.append(engine.evaluate(edges, field + sign * step * field_direction,
                                1 + edges[engine.native_edges]**2)['energy'])
                        differences.append((energy[1] - energy[0]) / (2 * step))
                    corrected = (4 * differences[1] - differences[0]) / 3
                    relative = float(abs(corrected - expected) / max(abs(expected), Decimal('1e-40')))
                    evidence.check(str(label) + ':' + variant + ':P7_native_action_derivative', relative < 1e-14, relative)
        points, weights = np.polynomial.legendre.leggauss(64)
        points, weights = points / 2, weights / 2
        weights *= 6 * (points + .5) * (.5 - points)
        wave_energy = 0.
        source_action_differences = np.zeros(2)
        for label, weight in zip(points, weights):
            row = action.samples(label, 16)
            wave_energy += weight * (row['quadrature']['measure'] @ (row['geometry']['gradient'] * row['gradient']**2 / 2))
            for index, step in enumerate([1e-4, 5e-5]):
                values = []
                for sign in [-1, 1]:
                    shifted_source = row['source'] + sign * step * np.sum(row['cardinal'])
                    geometry = action.geometry(row['quadrature']['reference'], shifted_source, label)
                    lagrangian = -(row['quadrature']['measure'] @ (geometry['gradient'] * row['gradient']**2 / 2))
                    lagrangian += action.dust(shifted_source, 0.)[0]
                    values.append(lagrangian)
                source_action_differences[index] += weight * (values[1] - values[0]) / (2 * step)
        live = arrays[('primary', 64)]
        contraction = np.sum(live['wave_source_force'][:, :-1] * np.asarray(decimals(initial['coordinates'])[:, :-1], float))
        energy_gradient_error = float(abs(contraction + 2 * wave_energy) / (2 * wave_energy))
        evidence.check('independent_wave_energy_field_derivative', energy_gradient_error < 2e-10, energy_gradient_error)
        predicted_source = (4 * source_action_differences[1] - source_action_differences[0]) / 3
        expected_source = np.sum(live['wave_source_force'][:, -1])
        source_action_error = float(abs(predicted_source - expected_source) / abs(expected_source))
        evidence.check('independent_wave_and_clock_source_action_derivative', source_action_error < 1e-7, source_action_error)
        path = evidence.output / 'live-higher-order-summary.csv'
        with path.open('x', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(summary[0]))
            writer.writeheader()
            writer.writerows(summary)
        evidence.own(path, 'outputs')
        evidence.report.update(summary=summary, live_wave_energy=wave_energy, P7_action_derivative_checked=True,
            wave_energy_field_derivative_error=energy_gradient_error, wave_clock_source_derivative_error=source_action_error,
            inherited_force_replay=adapter['wave_source_force_error'],
            source_difference_primary_reference=float(np.max(abs(arrays[('primary', 64)]['acceleration'][:, -1] - arrays[('reference', 64)]['acceleration'][:, -1]))),
            live_initial_candidate=parents['primary']['initial_candidate'], time_evolution_computed=False,
            github_action=False, subagents_used=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
