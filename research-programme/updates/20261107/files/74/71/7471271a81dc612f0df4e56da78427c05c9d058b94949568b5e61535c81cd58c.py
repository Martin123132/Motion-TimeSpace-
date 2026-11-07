from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from annular_compensation_cardinal_source_20260928 import CompensationLoads
from annular_live_compensation_derivative_20260928 import linear_solve, response_from_rhs
from annular_background_time_tangent_20260928 import FIELD_NAMES
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_joint_first_tangent_20260922 import MetricResponse, RadialResponse, MomentumMetricResponse
from annular_joint_flow_derivative_v2_20260922 import solve_joint_rhs
from derive_annular_direct_background_coupled_current_20260928 import TotalResponse
from annular_moving_Legendre_current_20260921 import samples
from annular_directional_coupled_Euler_20260928 import interpolate_nodal
from annular_candidate_radial_constraint_20260920 import radial_rhs
from annular_radial_time_forcing_20260928 import explicit_time_forcing
from annular_candidate_full_inverse_20260920 import BandedSourceInverse
from scipy.sparse import load_npz
from decimal import localcontext
from time import perf_counter
import argparse
import csv
import gc
import hashlib
import json
import numpy as np


def nonlinear_material(engine, action, time_response, support_response, response_rate, order, amount, correction_rate=None):
    labels, weights = np.polynomial.legendre.leggauss(order)
    labels, weights = labels / 2, weights / 2
    weights *= 6 * (labels + .5) * (.5 - labels)
    result = np.zeros_like(engine.loads.rates, dtype=complex)
    correction_rate = np.zeros_like(engine.loads.rates) if correction_rate is None else correction_rate
    for label, weight in zip(labels, weights):
        row = samples(action, label, 12)
        quad, geometry, cardinal = row['quadrature'], row['geometry'], row['cardinal']
        cells, local = quad['cells'], quad['local']
        indices = np.array(action.mesh['elements'])[cells]
        source = row['source'] + amount * row['velocity']
        velocity = row['velocity'] + amount * (cardinal @ engine.velocity_direction[:, -1])
        radius = geometry['radius'] + amount * geometry['displacement'] * row['velocity']
        jacobian = geometry['jacobian'] + amount * geometry['jacobian_source'] * row['velocity']
        gradient = (row['gradient'] + amount * row['rate_gradient']) / jacobian
        motion = -geometry['displacement'] * gradient
        widths = np.ones_like(radius.real)
        field_acceleration = interpolate_nodal(cardinal @ engine.velocity_direction[:, :-1], indices, local, widths)[0]
        temporal = row['rate'] + amount * field_acceleration + velocity * motion
        metric_values = action.solver.values(action.solution, radius)[0] + amount * time_response.values(radius)
        metric, lapse = 1 - 2 * metric_values[0] / radius, np.exp(metric_values[1])
        alpha = radius**2 / (lapse * np.sqrt(metric))
        field_nodes = cardinal @ (engine.field_direction + amount * (engine.field_direction_rate - correction_rate[:, :-1]))
        field = interpolate_nodal(field_nodes, indices, local, widths)[0]
        edges = cardinal @ engine.edges_direction
        source_direction = cardinal @ (engine.source_direction - amount * correction_rate[:, -1])
        movement = (1 - local) * edges[cells] + local * edges[cells + 1] + geometry['displacement'] * source_direction
        defect = field - movement * gradient
        variation = support_response.values(radius) + amount * response_rate.values(radius)
        density = quad['measure'] * jacobian * alpha * (defect + temporal * (variation[0] / (radius * metric) - variation[1]))
        source_radius = np.array([source])
        source_values = action.solver.values(action.solution, source_radius)[0][:, 0] + amount * time_response.values(source_radius)[:, 0]
        source_variation = support_response.values(source_radius)[:, 0] + amount * response_rate.values(source_radius)[:, 0]
        source_metric, source_lapse = 1 - 2 * source_values[0] / source, np.exp(source_values[1])
        clock_square = source_lapse**2 - velocity**2 / source_metric
        inertia = action.owner.source_mass * source_lapse**2 / (source_metric * clock_square**1.5)
        momentum = action.owner.source_mass * velocity / (source_metric * np.sqrt(clock_square))
        dust = inertia * source_direction
        dust += momentum * ((2 / (source * source_metric) + velocity**2 / (source * source_metric**2 * clock_square)) * source_variation[0]
            - source_lapse**2 / clock_square * source_variation[1])
        field_covector = np.zeros(result.shape[1] - 1, complex)
        selected = indices >= 0
        contributions = density[:, None] * row['shape']
        np.add.at(field_covector, indices[selected], contributions[selected])
        result += weight * np.outer(cardinal, np.r_[field_covector, density @ motion + dust])
    return result


def off_grid(engine, action, time_response, support, mixed_response, radius):
    fields, rates = engine.sample(radius)
    temporal, temporal_rate = engine.mixed_wave(radius)
    velocity, velocity_rate = engine.mixed_source(radius)
    state = action.solver.values(action.solution, radius)[0]
    time_state = time_response.values(radius)
    step = 1e-25
    unused, local = radial_rhs(radius, *state, *[fields[key] for key in FIELD_NAMES], engine.owner.coupling, engine.owner.source_mass, True)
    altered = {key: fields[key] + 1j * step * rates[key] for key in FIELD_NAMES}
    unused, changed_local = radial_rhs(radius, *(state + 1j * step * time_state), *[altered[key] for key in FIELD_NAMES], engine.owner.coupling, engine.owner.source_mass, True)
    zeros = np.zeros(len(radius))
    changed_forcing = explicit_time_forcing(radius, *(state + 1j * step * time_state), altered['source_density'], altered['velocity'],
        temporal + 1j * step * temporal_rate, zeros, zeros, zeros, velocity + 1j * step * velocity_rate,
        engine.owner.coupling, engine.owner.source_mass)
    values, derivative = mixed_response.solver.values(mixed_response.solution, radius)
    expected = np.einsum('abn,bn->an', local, values)
    expected += np.einsum('abn,bn->an', changed_local.imag / step, support.values(radius)) + changed_forcing.imag / step
    return derivative, expected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--parent', default='annular-live-compensation-time-attempt04')
    parser.add_argument('--label', default='annular-live-compensation-time-validation-attempt01')
    args = parser.parse_args()
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter() + 4800
    try:
        path = evidence.output.parent / args.parent / 'status.json'
        parent = json.loads(path.read_text())
        evidence.own(path)
        evidence.check('parent_complete', parent['state'] == 'complete' and parent['full_four_cases'] and all(row['passed'] for row in parent['checks']))
        digests, bad = {}, []
        for category in ['inputs', 'outputs']:
            for relative, expected in parent[category].items():
                path = evidence.root / relative
                if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                    bad.append(relative)
                else:
                    digests[str(path.relative_to(evidence.root))] = expected
                    evidence.own(path)
        evidence.check('parent_inputs_and_outputs_rehashed', not bad, bad)
        read = lambda relative: load_owned(evidence, digests, evidence.root / relative)
        status = lambda name: read(str((evidence.output.parent / name / 'status.json').relative_to(evidence.root)))
        flow_parent = status('annular-direct-background-coupled-current-attempt01')
        live = status('annular-live-support-acceleration-attempt01')
        geometric = status('annular-geometric-support-jet-attempt01')

        def save(name, **arrays):
            path = evidence.output / (name + '.npz')
            np.savez_compressed(path, **arrays)
            evidence.own(path, 'outputs')
            return str(path.relative_to(evidence.root))

        rows = []
        with localcontext() as context:
            context.prec = 70
            for case in parent['cases']:
                branch, level = case['branch'], case['level']
                name = branch + '-' + level
                print(json.dumps(dict(stage=name, seconds=perf_counter() - started)), flush=True)
                loads, action, sources = restore_case(evidence, digests, branch, level, deadline)
                select = lambda authority: next(item for item in authority['cases'] if item['branch'] == branch and item['level'] == level)
                previous, original, direct = select(live), select(geometric), select(flow_parent)
                directions = read(previous['direction_path'])
                projection = read(previous['paths']['projection'])
                transported = read(original['vertex_path'])['vertices'] / 2
                flow = read(direct['paths']['flow'])
                engine = CompensationLoads(loads, action, flow['acceleration'], directions, projection['correction'], transported)
                loads.owner.label_order = 28
                keys = ['state', 'rhs_coefficients', 'primitives', 'left']

                def response(relative):
                    archive = read(relative)
                    solver, solution = reconstructed_solver(archive)
                    return MetricResponse(solver, solution, archive['forcing'], 0., [])

                background, velocity = [response(direct['paths'][key]) for key in ['background_response', 'velocity_response']]
                support = response(previous['paths']['live_response'])
                mixed = response(case['paths']['mixed_response'])
                time_response = TotalResponse(background, velocity)
                if not rows:
                    from annular_horizontal_clock_evolution_20260913 import ChebyshevRule
                    from copy import copy
                    manufactured_solver = copy(mixed.solver)
                    manufactured_solver.rule = ChebyshevRule(22)
                    manufactured_solver.nodes = manufactured_solver.centers[:, None] + manufactured_solver.lengths[:, None] * manufactured_solver.rule.points / 2
                    local_zero = np.zeros((2, 2, manufactured_solver.nodes.size))
                    forcing = np.zeros((2, manufactured_solver.nodes.size))
                    forcing[0] = 1 / (manufactured_solver.edges[-1] - manufactured_solver.edges[0])
                    extra = -.0075
                    state, rhs, residual, history = linear_solve(manufactured_solver, local_zero, forcing, 4., extra)
                    manufactured = response_from_rhs(manufactured_solver, state, rhs, forcing, 4., extra, residual, history)
                    boundary = manufactured.values(np.array([manufactured_solver.edges[0], manufactured_solver.edges[-1]]))
                    evidence.check('manufactured_nonzero_mixed_boundary', np.max(abs(boundary - np.array([[0., 1.], [-.2575, -.2575]]))) <= 2e-13,
                        dict(evaluated=boundary.tolist(), omitted_boundary_error=abs(extra)))
                saved = read(case['paths']['derivative'])
                final = read(case['iterations'][-1]['path'])
                completed_solution = {key: mixed.solution[key] - final['metric_' + key] for key in keys}
                completed = MetricResponse(mixed.solver, completed_solution, np.zeros(1), 0., [])
                owner = read(sources['parent'])
                centre = next(item for item in owner['centres'] if item.get('route') == 'resampled') if level == 'fine' else owner['centres'][0]
                matrix = load_npz(evidence.root / centre['matrix_path'])
                inverse = BandedSourceInverse(matrix, loads.rates.shape)
                step = 1e-25
                numeric = nonlinear_material(engine, action, time_response, support, mixed, 48, 1j * step).imag / step
                completed_numeric = nonlinear_material(engine, action, time_response, support, completed, 48, 1j * step, saved['derivative']).imag / step
                analytic = read(case['paths']['material48'])['derivative']
                error = float(np.max(abs(numeric - analytic)))
                scale = float(np.max(abs(analytic)))
                evidence.check(name + ':nonlinear_material_directional_derivative', error <= 1e-24 + 2e-7 * scale, dict(error=error, scale=scale))
                inverse_error = float(np.max(abs(inverse.solve((numeric - analytic).ravel()))))
                max_wdot = float(np.max(abs(saved['derivative'])))
                evidence.check(name + ':inverse_weighted_nonlinear_material', inverse_error <= 2e-12 + 1e-7 * max_wdot, inverse_error)
                corrected_residual = float(np.max(abs(completed_numeric)))
                corrected_inverse = float(np.max(abs(inverse.solve(completed_numeric.ravel()))))
                evidence.check(name + ':completed_differentiated_projection', corrected_inverse <= 2e-12 + 1e-7 * max_wdot,
                    dict(raw=corrected_residual, inverse=corrected_inverse, max_wdot=max_wdot))
                paths = dict(material=save(name + '-independent-material', nonlinear=numeric, analytic=analytic,
                    completed_nonlinear=completed_numeric, inverse_discrepancy=inverse.solve((numeric - analytic).ravel())))
                indices = np.linspace(0, len(mixed.solver.lengths) - 1, 257, dtype=int)
                radius = (mixed.solver.centers[indices, None] + mixed.solver.lengths[indices, None] * np.array([-.287, .113, .329])).ravel()
                derivative, expected = off_grid(engine, action, time_response, support, mixed, radius)
                paths['offgrid'] = save(name + '-offgrid-mixed-equation', radius=radius, derivative=derivative, expected=expected)
                offgrid_error = np.max(abs(derivative - expected), axis=1)
                offgrid_scale = np.max(abs(expected), axis=1)
                for component in range(2):
                    evidence.check(name + ':offgrid_mixed_equation:' + str(component), offgrid_error[component] <= 1e-20 + 2e-6 * offgrid_scale[component],
                        dict(error=float(offgrid_error[component]), scale=float(offgrid_scale[component]), samples=len(radius)))
                mixed_archive = read(case['paths']['mixed_response'])
                difference_solution = {key: mixed_archive['alternate_' + key] - mixed_archive[key] for key in keys}
                difference_response = MetricResponse(mixed.solver, difference_solution, np.zeros(1), 0., [])
                momentum = MomentumMetricResponse(action, deadline, lambda stage: None)
                direct_difference_rhs = momentum.accumulate(difference_response.values)
                rounded_difference = read(case['paths']['sensitivity'])['delta_rhs']
                sparse_response = RadialResponse(loads, action, branch.split('-')[1], deadline,
                    lambda stage: print(json.dumps(dict(stage=name + ':sensitivity:' + stage, seconds=perf_counter() - started)), flush=True))
                sensitivity_iterations = []
                def record_sensitivity(row, direction, coupling, residual, metric):
                    sensitivity_iterations.append(row)
                direct_sensitivity, unused, unused2, unused3, sensitivity_history = solve_joint_rhs(
                    dict(inverse=inverse, matrix=matrix), sparse_response, momentum, direct_difference_rhs, record_sensitivity)
                sensitivity_max = float(np.max(abs(direct_sensitivity)))
                evidence.check(name + ':cancellation_free_oracle_live_sensitivity', sensitivity_max <= 2e-12,
                    dict(maximum_wdot_change=sensitivity_max, rhs_max=float(np.max(abs(direct_difference_rhs))),
                        rounded_rhs_discrepancy=float(np.max(abs(direct_difference_rhs - rounded_difference)))))
                paths['cancellation_free_sensitivity'] = save(name + '-cancellation-free-sensitivity',
                    delta_rhs=direct_difference_rhs, rounded_delta_rhs=rounded_difference, delta_wdot=direct_sensitivity)
                row = dict(branch=branch, level=level, material_oracle_error=error, inverse_material_oracle_error=inverse_error,
                    completed_raw_residual=corrected_residual, completed_inverse_residual=corrected_inverse,
                    frozen_raw_residual=scale, offgrid_mass_error=float(offgrid_error[0]), offgrid_lapse_error=float(offgrid_error[1]),
                    offgrid_points=len(radius), cancellation_free_oracle_wdot_change=sensitivity_max, valid_for_physics_claim=False)
                rows.append(row)
                evidence.report['cases'].append(dict(branch=branch, level=level, paths=paths, summary=row))
                evidence.save()
                del inverse, engine, action, loads, sparse_response, momentum, matrix
                gc.collect()
        path = evidence.output / 'independent-time-derivative-checks.csv'
        with path.open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        evidence.own(path, 'outputs')
        evidence.report.update(seconds=perf_counter() - started, summaries=rows, github_action=False,
            subagents_used=False, new_nonlinear_evolution_solves=0)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
