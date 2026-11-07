from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from annular_joint_first_tangent_20260922 import RadialResponse, MomentumMetricResponse, solve_tangent
from annular_joint_flow_derivative_v2_20260922 import solve_joint_rhs
from annular_live_compensation_derivative_20260928 import response_from_rhs
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--parent', default='annular-old-field-reaction-attempt01')
    parser.add_argument('--label', default='annular-old-reaction-validation-attempt01')
    parser.add_argument('--max-seconds', type=float, default=5400)
    args = parser.parse_args()
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter() + args.max_seconds
    try:
        evidence.report.update(scope='Old-action replay and position-oracle propagation through live reaction',
            github_action=False, subagents_used=False, new_trajectories=0, original_workbench_write=False,
            uncertainty_is_rigorous_bound=False, inherited_precision_flags_repaired=False)
        evidence.own(evidence.root / 'DERIVATION-20260929-old-field-reaction.md')
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
                    digests[str(path.relative_to(evidence.root))] = expected
                    evidence.own(path)
        evidence.check('parent_hashes_unchanged', not bad, bad)
        read = lambda relative: load_owned(evidence, digests, evidence.root / relative)
        positions = read(str((evidence.output.parent / 'annular-compensated-position-attempt04/status.json').relative_to(evidence.root)))

        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter() - started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
            if perf_counter() > deadline:
                raise RuntimeError('Safe reaction validation boundary')

        def save(name, **arrays):
            path = evidence.output / (name + '.npz')
            np.savez_compressed(path, **arrays)
            evidence.own(path, 'outputs')
            return str(path.relative_to(evidence.root))

        summaries = []
        with localcontext() as context:
            context.prec = 70
            for case in parent['cases']:
                branch, level = case['branch'], case['level']
                name = branch + '-' + level
                progress(name + ':restore')
                loads, action, sources = restore_case(evidence, digests, branch, level, deadline)
                material = read(case['paths']['material48'])
                original = action.momentum_and_force(12, 48, deadline)
                momentum_error = float(np.max(abs(original['momentum'] - material['base_momentum'])))
                force_error = float(np.max(abs(original['bulk'] + original['dust'] - material['base_force_wave'])))
                evidence.check(name + ':independent_original_momentum', momentum_error <= 2e-16, momentum_error)
                evidence.check(name + ':independent_original_wave_clock_force', force_error <= 2e-15, force_error)
                owner = read(sources['parent'])
                centre = next(row for row in owner['centres'] if row.get('route') == 'resampled') if level == 'fine' else owner['centres'][0]
                matrix_path = evidence.root / centre['matrix_path']
                evidence.check(name + ':matrix_owned', str(matrix_path.relative_to(evidence.root)) in digests)
                matrix = load_npz(matrix_path)
                inverse = BandedSourceInverse(matrix, loads.rates.shape)
                radial = RadialResponse(loads, action, branch.split('-')[1], deadline, lambda stage: progress(name + ':' + stage))
                momentum = MomentumMetricResponse(action, deadline, lambda stage: progress(name + ':' + stage))
                positioned = next(row for row in positions['cases'] if row['branch'] == branch and row['level'] == level)
                alternate = read(positioned['paths']['sensitivity'])
                tangent, residual, history = solve_tangent(radial.solver, radial.state, radial.extension, alternate['delta_forcing'])
                unused, local = radial.solver.rhs(radial.state, radial.extension, True)
                rhs = (np.einsum('abn,bn->an', local, tangent.reshape(2, -1)) + alternate['delta_forcing']).reshape(tangent.shape)
                outer_factor = radial.solver.edges[-1] - 2 * action.solution['state'][0, -1, -1]
                delta_position = response_from_rhs(radial.solver, tangent, rhs, alternate['delta_forcing'], outer_factor, 0., residual, history)
                replay = float(np.max(abs(tangent - alternate['delta_state'])))
                evidence.check(name + ':independent_position_sensitivity_replay', replay <= 1e-30 + 2e-8 * float(np.max(abs(tangent))), replay)
                forcing = momentum.accumulate(delta_position.values)
                iteration_rows = []
                record = lambda row, direction, coupling, residual, metric: iteration_rows.append(dict(row))
                direction, metric, unused, unused2, history = solve_joint_rhs(dict(matrix=matrix, inverse=inverse), radial, momentum, forcing, record)
                maximum = float(np.max(abs(direction)))
                evidence.check(name + ':position_to_reaction_sensitivity', maximum <= 2e-11, maximum)
                keys = ['state', 'rhs_coefficients', 'primitives', 'left']
                corrected = {key: delta_position.solution[key] - metric.solution[key] for key in keys}
                paths = dict(response=save(name + '-position-reaction-sensitivity', reaction_change=direction,
                    acceleration_change=-direction, forcing=forcing, edges=radial.solver.edges,
                    **{'corrected_' + key: value for key, value in corrected.items()},
                    **{'position_' + key: value for key, value in delta_position.solution.items()}))
                summary = dict(branch=branch, level=level, momentum_replay=momentum_error, wave_clock_force_replay=force_error,
                    delta_position_max=float(np.max(abs(tangent))), reaction_change_max=maximum,
                    corrected_metric_time_change_max=float(np.max(abs(corrected['state']))),
                    live_sensitivity_relative_residual=history[-1]['relative_residual'])
                summaries.append(summary)
                evidence.report['cases'].append(dict(branch=branch, level=level, paths=paths, summary=summary, iterations=iteration_rows))
                progress(name + ':complete')
                del radial, momentum, inverse, matrix, action, loads
                gc.collect()
        path = evidence.output / 'old-reaction-validation.csv'
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
