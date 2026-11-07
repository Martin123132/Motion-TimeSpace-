from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from annular_position_reaction_20260929 import ResponseSum
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_joint_first_tangent_20260922 import RadialResponse, MomentumMetricResponse, MetricResponse
from annular_joint_flow_derivative_v2_20260922 import solve_joint_rhs
from annular_candidate_full_inverse_20260920 import BandedSourceInverse
from derive_annular_position_time_radial_v5_20260929 import solve_jumps
from annular_background_time_tangent_20260928 import FIELD_NAMES
from annular_candidate_radial_constraint_20260920 import radial_rhs
from annular_radial_time_forcing_20260928 import explicit_time_forcing
from annular_horizontal_clock_evolution_20260913 import ChebyshevRule
from scipy.sparse import load_npz
from decimal import localcontext
from time import perf_counter
from copy import copy
import argparse
import csv
import gc
import hashlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--parent', default='annular-position-reaction-attempt01')
    parser.add_argument('--label', default='annular-position-reaction-validation-attempt01')
    parser.add_argument('--max-seconds', type=float, default=5400)
    args = parser.parse_args()
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter() + args.max_seconds
    try:
        evidence.report.update(scope='Reconstruct lower-degree B0 and propagate cancellation-free sensitivity through k0',
            github_action=False, subagents_used=False, original_workbench_write=False, new_trajectories=0,
            uncertainty_is_rigorous_bound=False, C0_force_current_column_computed=False,
            inherited_position_density_precision_warnings=4, inherited_mixed_time_precision_warnings=4, inherited_raw_C2_warnings=2)
        evidence.own(evidence.root / 'DERIVATION-20260929-position-reaction-sensitivity.md')
        parent_path = evidence.output.parent / args.parent / 'status.json'
        parent = json.loads(parent_path.read_text())
        evidence.own(parent_path)
        evidence.check('parent_complete', parent['state'] == 'complete' and len(parent['cases']) == 4)
        digests, bad = {}, []
        for category in ['inputs', 'outputs']:
            for relative, expected in parent[category].items():
                if relative == 'CURRENT_LOCAL_RESUME.md':
                    continue
                path = evidence.root / relative
                if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                    bad.append(relative)
                else:
                    digests[relative] = expected
                    evidence.own(path)
        evidence.check('all_inputs_unchanged', not bad, bad)
        read = lambda relative: load_owned(evidence, digests, evidence.root / relative)
        status = lambda name: read(str((evidence.output.parent / name / 'status.json').relative_to(evidence.root)))
        mixed_parent, direct, positions, jets = [status(name) for name in [
            'annular-position-time-radial-attempt05', 'annular-direct-background-coupled-current-attempt01',
            'annular-compensated-position-attempt04', 'annular-position-metric-jet-validation-attempt01']]

        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter() - started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
            if perf_counter() > deadline:
                raise RuntimeError('Safe position reaction sensitivity boundary')

        def save(name, **arrays):
            path = evidence.output / (name + '.npz')
            np.savez_compressed(path, **arrays)
            evidence.own(path, 'outputs')
            return str(path.relative_to(evidence.root))

        restore = lambda archive: MetricResponse(*reconstructed_solver(archive), archive.get('forcing'), 0., [])
        summaries = []
        with localcontext() as context:
            context.prec = 70
            for case in parent['cases']:
                branch, level = case['branch'], case['level']
                name = branch + '-' + level
                progress(name + ':restore')
                loads, action, sources = restore_case(evidence, digests, branch, level, deadline)
                match = lambda report: next(row for row in report['cases'] if row['branch'] == branch and row['level'] == level)
                mixed_case, flow, position_case, jet = map(match, [mixed_parent, direct, positions, jets])
                archive = read(mixed_case['paths']['response'])
                fields = read(mixed_case['paths']['density'])
                position = ResponseSum(restore(read(position_case['paths']['response'])), restore(read(jet['paths']['transported_old_metric'])))
                metric_time = ResponseSum(restore(read(flow['paths']['background_response'])), restore(read(flow['paths']['velocity_response'])))
                solver = copy(action.solver)
                solver.nodes = archive['nodes']
                degree = solver.nodes.shape[1] - 1
                solver.rule = ChebyshevRule(degree)
                radius, gauss = fields['radius'], fields['gauss']
                inverse_rule = np.linalg.inv(np.polynomial.chebyshev.chebvander(gauss, degree))
                project = lambda array: np.asarray(array).reshape(-1, len(solver.lengths), degree + 1) @ inverse_rule.T
                vandermonde = np.polynomial.chebyshev.chebvander(solver.rule.points, degree)
                values = action.solver.values(action.solution, radius)[0]
                position_values, time_values = position.values(radius), metric_time.values(radius)
                unused, local = radial_rhs(radius, *values, *[fields[key][0] for key in FIELD_NAMES],
                    action.owner.coupling, action.owner.source_mass, True)
                amount = 1e-25j
                changed = {key: fields[key][0] + amount * fields[key][1] for key in FIELD_NAMES}
                unused, changed_local = radial_rhs(radius, *(values + amount * position_values), *[changed[key] for key in FIELD_NAMES],
                    action.owner.coupling, action.owner.source_mass, True)
                forcing = explicit_time_forcing(radius, *(values + amount * position_values), changed['source_density'], changed['velocity'],
                    *[fields[key][2] + amount * fields[key][3] for key in FIELD_NAMES], action.owner.coupling, action.owner.source_mass).imag / 1e-25
                forcing += np.einsum('abn,bn->an', changed_local.imag / 1e-25, time_values)
                local_coefficients, forcing_coefficients = project(local), project(forcing)
                local_full = (local_coefficients @ vandermonde.T).reshape(2, 2, -1)
                forcing_full = (forcing_coefficients @ vandermonde.T).reshape(2, -1)
                local_lower_coefficients, forcing_lower_coefficients = local_coefficients.copy(), forcing_coefficients.copy()
                local_lower_coefficients[:, :, -2:] = 0.
                forcing_lower_coefficients[:, :, -2:] = 0.
                local_lower = (local_lower_coefficients @ vandermonde.T).reshape(2, 2, -1)
                forcing_lower = (forcing_lower_coefficients @ vandermonde.T).reshape(2, -1)
                factor = solver.edges[-1] - 2 * action.solution['state'][0, -1, -1]
                outer = np.array([solver.edges[-1]])
                boundary = -2 * position.values(outer)[0, 0] * metric_time.values(outer)[0, 0] / factor**2
                full = solve_jumps(solver, local_full, forcing_full, factor, boundary, archive['jumps'])
                lower = solve_jumps(solver, local_lower, forcing_lower, factor, boundary, archive['jumps'])
                full_error = float(np.max(abs(full.solution['state'] - archive['state'])))
                lower_error = float(np.max(abs(lower.solution['state'] - archive['lower_polynomial_state'])))
                evidence.check(name + ':full_response_replay', full_error <= 2e-18, full_error)
                evidence.check(name + ':lower_response_replay', lower_error <= 2e-18, lower_error)
                delta_local = ((local_lower_coefficients - local_coefficients) @ vandermonde.T).reshape(2, 2, -1)
                delta_forcing = ((forcing_lower_coefficients - forcing_coefficients) @ vandermonde.T).reshape(2, -1)
                delta_forcing += np.einsum('abn,bn->an', delta_local, full.solution['state'].reshape(2, -1))
                delta = solve_jumps(solver, local_lower, delta_forcing, factor, 0., np.zeros_like(archive['jumps']))
                superposition = float(np.max(abs(lower.solution['state'] - full.solution['state'] - delta.solution['state'])))
                evidence.check(name + ':cancellation_free_difference_identity', superposition <= 2e-18, superposition)
                owner = read(sources['parent'])
                centre = next(row for row in owner['centres'] if row.get('route') == 'resampled') if level == 'fine' else owner['centres'][0]
                matrix_path = evidence.root / centre['matrix_path']
                evidence.check(name + ':matrix_owned', str(matrix_path.relative_to(evidence.root)) in digests)
                matrix = load_npz(matrix_path)
                inverse = BandedSourceInverse(matrix, loads.rates.shape)
                radial = RadialResponse(loads, action, branch.split('-')[1], deadline, lambda stage: progress(name + ':' + stage))
                momentum = MomentumMetricResponse(action, deadline, lambda stage: progress(name + ':' + stage))
                rhs = -momentum.accumulate(delta.values)
                iterations = []
                record = lambda row, direction, coupling, residual, metric: iterations.append(dict(row))
                reaction, reaction_metric, unused, unused2, history = solve_joint_rhs(dict(matrix=matrix, inverse=inverse), radial, momentum, rhs, record)
                maximum = float(np.max(abs(reaction)))
                evidence.check(name + ':B0_to_k0_sensitivity', maximum <= 2e-11, maximum)
                keys = ['state', 'rhs_coefficients', 'primitives', 'left']
                corrected = {key: delta.solution[key] + reaction_metric.solution[key] for key in keys}
                paths = dict(response=save(name + '-B0-to-k0-sensitivity', acceleration_change=reaction, rhs=rhs,
                    edges=solver.edges, **{'B0_' + key: delta.solution[key] for key in keys},
                    **{'corrected_' + key: corrected[key] for key in keys}))
                summary = dict(branch=branch, level=level, full_replay_error=full_error, lower_replay_error=lower_error,
                    subtraction_identity_error=superposition, cancellation_free_B0_change=float(np.max(abs(delta.solution['state']))),
                    k0_change_max=maximum, corrected_metric_time_change=float(np.max(abs(corrected['state']))),
                    live_relative_residual=history[-1]['relative_residual'], valid_for_claim=False)
                summaries.append(summary)
                evidence.report['cases'].append(dict(branch=branch, level=level, summary=summary, paths=paths, iterations=iterations))
                progress(name + ':complete')
                del radial, momentum, loads, action, fields, matrix, inverse
                gc.collect()
        table = evidence.output / 'position-reaction-B0-sensitivity.csv'
        with table.open('x', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(summaries[0]))
            writer.writeheader()
            writer.writerows(summaries)
        evidence.own(table, 'outputs')
        evidence.report['seconds'] = perf_counter() - started
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
