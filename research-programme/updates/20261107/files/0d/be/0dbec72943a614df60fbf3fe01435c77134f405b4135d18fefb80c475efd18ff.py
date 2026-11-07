from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_joint_first_tangent_20260922 import MetricResponse
from annular_moving_Legendre_current_20260921 import samples
from annular_directional_coupled_Euler_20260928 import interpolate_nodal
from annular_support_radial_response_20260928 import gravitational_moments
from annular_reacted_support_columns_20260929 import compatibility
from annular_aligned_acceleration_channels_20260929 import acceleration_channels_aligned
from decimal import localcontext
from time import perf_counter
import argparse
import csv
import gc
import hashlib
import json
import numpy as np


def acceleration_channels(action, loads, directions, acceleration, metric_response, support_factor, order, deadline):
    points, weights = np.polynomial.legendre.leggauss(order)
    points, weights = points / 2, weights / 2
    weights *= 6 * (points + .5) * (.5 - points)
    result = np.zeros(4)
    reference_edges = np.array([float(value) for value in action.edges])
    for label, weight in zip(points, weights):
        if perf_counter() > deadline:
            raise RuntimeError('Safe acceleration sensitivity boundary')
        row = samples(action, label, 12)
        quad, geometry, cardinal = row['quadrature'], row['geometry'], row['cardinal']
        cells, local = quad['cells'], quad['local']
        indices = np.asarray(action.mesh['elements'])[cells]
        widths = np.diff(reference_edges)[cells] * geometry['jacobian']
        interpolate = lambda nodes: interpolate_nodal(nodes, indices, local, widths)[0]
        edge = cardinal @ directions['edge_vertices']
        eta = edge[cells] * (1 - local) + edge[cells + 1] * local
        field_test = interpolate(cardinal @ directions['field_vertices'])
        gradient = row['gradient'] / geometry['jacobian']
        radius, metric = geometry['radius'], geometry['metric']
        alpha = radius**2 / (geometry['lapse'] * np.sqrt(metric))
        temporal_acceleration = interpolate(cardinal @ acceleration[:, :-1])
        temporal_acceleration -= (geometry['displacement'] * (cardinal @ acceleration[:, -1]) + support_factor * eta) * gradient
        metric_change = metric_response.values(radius)
        density = alpha * (temporal_acceleration + row['temporal'] * (metric_change[0] / (radius * metric) - metric_change[1]))
        measure = quad['measure'] * geometry['jacobian']
        channels = [measure @ (density * (field_test - eta * gradient))]
        node_radius = action.geometry(action.knots, row['source'], label)['radius']
        node_rate = cardinal @ loads.rates[:, :-1]
        for power in range(3):
            integral = ((radius - 6)**(power + 1) - (row['source'] - 6)**(power + 1)) / (power + 1)
            node_integral = ((node_radius - 6)**(power + 1) - (row['source'] - 6)**(power + 1)) / (power + 1)
            weighted = interpolate(node_rate * node_integral)
            channels.append(measure @ (density * (row['temporal'] * integral - weighted)))
        result += weight * np.array(channels)
    result[1:] += gravitational_moments(action, metric_response, 32)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', default='annular-reacted-column-sensitivity-attempt01')
    parser.add_argument('--max-seconds', type=float, default=3600)
    parser.add_argument('--columns', default='annular-reacted-support-columns-attempt02')
    args = parser.parse_args()
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter() + args.max_seconds
    try:
        evidence.report.update(scope='Analytic acceleration replay and independent propagated position-oracle uncertainty',
            github_action=False, subagents_used=False, new_trajectories=0, original_workbench_write=False,
            inherited_precision_flags_repaired=False, uncertainty_is_rigorous_bound=False)
        evidence.own(evidence.root / 'DERIVATION-20260929-reacted-column-sensitivity.md')
        digests, parents, bad = {}, {}, []
        for folder in [args.columns, 'annular-old-reaction-validation-attempt01']:
            path = evidence.output.parent / folder / 'status.json'
            report = json.loads(path.read_text())
            evidence.own(path)
            evidence.check(folder + ':complete', report['state'] == 'complete' and len(report['cases']) == 4)
            parents[folder] = report
            for category in ['inputs', 'outputs']:
                for relative, expected in report[category].items():
                    if relative == 'CURRENT_LOCAL_RESUME.md':
                        continue
                    source = evidence.root / relative
                    normalized = str(source.relative_to(evidence.root))
                    if normalized in digests:
                        if digests[normalized] != expected:
                            bad.append('conflicting digest: ' + normalized)
                        continue
                    if not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest() != expected:
                        bad.append(relative)
                    else:
                        digests[normalized] = expected
                        evidence.own(source)
        evidence.check('all_inputs_unchanged', not bad, bad)
        read = lambda relative: load_owned(evidence, digests, evidence.root / relative)
        status = lambda name: read(str((evidence.output.parent / name / 'status.json').relative_to(evidence.root)))
        live = status('annular-live-support-acceleration-attempt01')
        reactions = status('annular-old-field-reaction-attempt01')

        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter() - started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
            if perf_counter() > deadline:
                raise RuntimeError('Safe final sensitivity boundary')

        def save(name, **arrays):
            path = evidence.output / (name + '.npz')
            np.savez_compressed(path, **arrays)
            evidence.own(path, 'outputs')
            return str(path.relative_to(evidence.root))

        summaries = []
        keys = ['state', 'rhs_coefficients', 'primitives', 'left']
        with localcontext() as context:
            context.prec = 70
            for case in parents[args.columns]['cases']:
                branch, level = case['branch'], case['level']
                name = branch + '-' + level
                match = lambda report: next(row for row in report['cases'] if row['branch'] == branch and row['level'] == level)
                progress(name + ':restore')
                loads, action, sources = restore_case(evidence, digests, branch, level, deadline)
                old = match(live)
                directions = read(old['direction_path'])
                correction = read(old['paths']['projection'])['correction']
                velocity_archive = read(old['paths']['live_response'])
                solver, solution = reconstructed_solver(velocity_archive)
                velocity = MetricResponse(solver, solution, velocity_archive['forcing'], 0., [])
                material_sensitivity = read(match(reactions)['paths']['sensitivity'])
                material_metric = MetricResponse(solver, {key: -material_sensitivity['metric_' + key] for key in keys}, None, 0., [])
                oracle_case = match(parents['annular-old-reaction-validation-attempt01'])
                oracle = read(oracle_case['paths']['response'])
                oracle_metric = MetricResponse(solver, {key: oracle['corrected_' + key] for key in keys}, None, 0., [])
                acceleration = np.column_stack([directions['field_vertices'] - correction[:, :-1], -correction[:, -1]])
                coefficient = acceleration_channels_aligned(action, loads, directions, acceleration, velocity, 1., 64, deadline)
                combined = read(case['paths']['combined'])
                evidence.check(name + ':analytic_acceleration_block_replay', np.max(abs(coefficient - combined['fine'][2])) <= 2e-24,
                    float(np.max(abs(coefficient - combined['fine'][2]))))
                material = acceleration_channels(action, loads, directions, -material_sensitivity['direction'], material_metric, 0., 64, deadline)
                archived_material = read(case['paths']['material64'])['reaction_delta']
                evidence.check(name + ':independent_reaction_uncertainty_block',
                    np.max(abs(material - archived_material)) <= 2e-26 + 2e-7 * np.max(abs(material)),
                    float(np.max(abs(material - archived_material))))
                oracle_columns = []
                for order in [48, 64]:
                    progress(name + ':oracle-material' + str(order))
                    oracle_columns.append(acceleration_channels(action, loads, directions, oracle['acceleration_change'], oracle_metric, 0., order, deadline))
                oracle_error = float(np.max(abs(oracle_columns[1] - oracle_columns[0])))
                evidence.check(name + ':oracle_material48_64', oracle_error <= 2e-25, oracle_error)
                uncertainty = combined['sampled_uncertainty'].copy()
                uncertainty[1] += np.maximum(abs(oracle_columns[0]), abs(oracle_columns[1]))
                diagnostic = compatibility(combined['coarse'], combined['fine'], uncertainty, uncertainty)
                paths = dict(response=save(name + '-propagated-uncertainty', independent_C2=coefficient,
                    independent_material_uncertainty=material, position_oracle48=oracle_columns[0], position_oracle64=oracle_columns[1],
                    original_uncertainty=combined['sampled_uncertainty'], augmented_uncertainty=uncertainty,
                    columns=combined['fine'], coarse_columns=combined['coarse']))
                summary = dict(branch=branch, level=level, C2_replay_error=float(np.max(abs(coefficient - combined['fine'][2]))),
                    material_derivative_error=float(np.max(abs(material - archived_material))), position_oracle_C1_max=float(np.max(abs(oracle_columns[1]))),
                    rank_resolved=diagnostic['rank_resolved'], residual_within_sampled_uncertainty=diagnostic['residual_within_sampled_uncertainty'],
                    any_force_current_pair_compatible=any(row.get('all_rows_within_sampled_uncertainty', False) for row in diagnostic['exact_force_current_pairs']))
                summaries.append(summary)
                evidence.report['cases'].append(dict(branch=branch, level=level, paths=paths, summary=summary,
                    diagnostic=diagnostic, previous_diagnostic=case['diagnostic']))
                progress(name + ':complete')
                del action, loads
                gc.collect()
        path = evidence.output / 'reacted-column-sensitivity.csv'
        with path.open('w', newline='', encoding='utf-8') as handle:
            writer = csv.DictWriter(handle, fieldnames=list(summaries[0]))
            writer.writeheader()
            writer.writerows(summaries)
        evidence.own(path, 'outputs')
        evidence.report['seconds'] = perf_counter() - started
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
