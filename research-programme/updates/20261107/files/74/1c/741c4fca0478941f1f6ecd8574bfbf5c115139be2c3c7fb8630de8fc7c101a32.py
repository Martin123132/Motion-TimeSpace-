from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from annular_position_reaction_20260929 import ResponseSum
from annular_position_reaction_eulerian_v2_20260929 import hybrid_position_reaction as material_position_reaction
from annular_old_field_reaction_20260929 import symbolic_checks
from annular_physical_native_kernel_20260928 import NativeKernel
from annular_joint_first_tangent_20260922 import RadialResponse, MomentumMetricResponse, MetricResponse
from annular_joint_flow_derivative_v2_20260922 import solve_joint_rhs
from annular_candidate_full_inverse_20260920 import BandedSourceInverse
from annular_candidate_energy_current_20260921 import reconstructed_solver
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
    parser.add_argument('--label', default='annular-position-reaction-diagnostic-attempt01')
    parser.add_argument('--max-seconds', type=float, default=10000)
    parser.add_argument('--case-limit', type=int, default=1)
    args = parser.parse_args()
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter() + args.max_seconds
    try:
        evidence.report.update(scope='EXPLORATORY reference-only k0 solve; failed quadrature and baseline gates retained',
            accepted_for_C0=False, numerical_acceptance_passed=False, diagnostic_only=True,
            accuracy_gate_failures=[], inherited_failed_attempt='annular-position-reaction-attempt03',
            github_action=False, subagents_used=False, new_trajectories=0, original_workbench_write=False,
            inherited_position_density_precision_warnings=4, inherited_mixed_time_precision_warnings=4,
            inherited_raw_C2_warnings=2, C0_force_current_column_computed=False,
            uncertainty_is_rigorous_bound=False, B0_polynomial_sensitivity_propagated=False, units='code-normalized')
        evidence.own(evidence.root / 'DERIVATION-20260929-position-reaction-diagnostic-solve.md')
        evidence.own(evidence.root / 'scripts/annular_position_reaction_20260929.py')
        seal_path = evidence.output.parent / 'annular-position-time-final-integrity-20260929.json'
        seal = json.loads(seal_path.read_text())
        evidence.own(seal_path)
        digests, bad = {}, []
        for relative, expected in seal['hashes'].items():
            if relative == 'CURRENT_LOCAL_RESUME.md':
                continue
            path = evidence.root / relative
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                bad.append(relative)
            else:
                digests[str(path.relative_to(evidence.root))] = expected
                evidence.own(path)
        evidence.check('position_time_inputs_unchanged', seal['state'] == 'complete' and not bad, bad)
        previous_path = evidence.output.parent / 'annular-position-reaction-attempt03/status.json'
        previous = json.loads(previous_path.read_text())
        evidence.own(previous_path)
        for category in ['inputs', 'outputs']:
            for relative, expected in previous[category].items():
                if relative == 'CURRENT_LOCAL_RESUME.md':
                    continue
                path = evidence.root / relative
                if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                    raise RuntimeError('Changed exploratory input: ' + relative)
                digests[relative] = expected
                evidence.own(path)
        read = lambda relative: load_owned(evidence, digests, evidence.root / relative)
        status = lambda name: read(str((evidence.output.parent / name / 'status.json').relative_to(evidence.root)))
        parent, direct, live, positions, jets = [status(name) for name in [
            'annular-position-time-radial-attempt05', 'annular-direct-background-coupled-current-attempt01',
            'annular-live-support-acceleration-attempt01', 'annular-compensated-position-attempt04',
            'annular-position-metric-jet-validation-attempt01']]
        evidence.check('B0_complete', parent['state'] == 'complete' and len(parent['cases']) == 4)
        symbolic_checks(evidence)

        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter() - started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
            if perf_counter() > deadline:
                raise RuntimeError('Safe old-field position reaction boundary')

        def save(name, **arrays):
            path = evidence.output / (name + '.npz')
            np.savez_compressed(path, **arrays)
            evidence.own(path, 'outputs')
            return str(path.relative_to(evidence.root))

        def restore(archive):
            solver, solution = reconstructed_solver(archive)
            return MetricResponse(solver, solution, archive.get('forcing'), 0., [])

        summaries = []
        with localcontext() as context:
            context.prec = 70
            for case in parent['cases'][:args.case_limit]:
                branch, level = case['branch'], case['level']
                name = branch + '-' + level
                progress(name + ':restore')
                loads, action, sources = restore_case(evidence, digests, branch, level, deadline)
                match = lambda report: next(row for row in report['cases'] if row['branch'] == branch and row['level'] == level)
                flow_case, live_case, pos_case, jet_case = map(match, [direct, live, positions, jets])
                directions = read(live_case['direction_path'])
                correction = read(live_case['paths']['projection'])['correction']
                mode_rate = read(jet_case['paths']['completed_metric_time'])['mode_rate']
                acceleration = read(flow_case['paths']['flow'])['acceleration']
                position_archive = read(pos_case['paths']['response'])
                transported_archive = read(jet_case['paths']['transported_old_metric'])
                position = ResponseSum(restore(position_archive), restore(transported_archive))
                metric_time = ResponseSum(restore(read(flow_case['paths']['background_response'])),
                    restore(read(flow_case['paths']['velocity_response'])))
                mixed_archive = read(case['paths']['response'])
                mixed = restore(mixed_archive)
                packet = read(sources['packet'])
                native = NativeKernel(action.mesh, packet['gram_support'], branch.startswith('MTS'))
                owner = read(sources['parent'])
                centre = next(row for row in owner['centres'] if row.get('route') == 'resampled') if level == 'fine' else owner['centres'][0]
                matrix_path = evidence.root / centre['matrix_path']
                evidence.check(name + ':matrix_owned', str(matrix_path.relative_to(evidence.root)) in digests)
                matrix = load_npz(matrix_path)
                inverse = BandedSourceInverse(matrix, loads.rates.shape)
                invmax = lambda array: float(np.max(abs(inverse.solve(array.ravel()))))
                results, paths = {}, {}
                for order in [48, 64]:
                    progress(name + ':reuse-material' + str(order))
                    relative = str((evidence.output.parent / 'annular-position-reaction-attempt03' / (name + '-material' + str(order) + '.npz')).relative_to(evidence.root))
                    result = read(relative)
                    results[order] = result
                    paths['material' + str(order)] = save(name + '-material' + str(order), **result)
                    evidence.check(name + ':original_momentum_mixed_jet_' + str(order), invmax(result['oracle_difference']) <= 2e-11,
                        dict(inverse_error=invmax(result['oracle_difference']), raw_error=float(np.max(abs(result['oracle_difference'])))))
                    evidence.check(name + ':native_step_halving_' + str(order), invmax(result['native_halving_difference']) <= 2e-11,
                        invmax(result['native_halving_difference']))
                result = results[64]
                progress(name + ':original-action-replay')
                original = action.momentum_and_force(12, 64, deadline)
                momentum_error = float(np.max(abs(original['momentum'] - result['base_momentum'])))
                force_error = float(np.max(abs(original['bulk'] + original['dust'] - result['base_force_wave'])))
                evidence.report['accuracy_gate_failures'].append(dict(case=name, gate='original_momentum', error=momentum_error, tolerance=2e-16, passed=momentum_error <= 2e-16))
                evidence.report['accuracy_gate_failures'].append(dict(case=name, gate='original_wave_clock_force', error=force_error, tolerance=2e-15, passed=force_error <= 2e-15))
                difference = results[48]['residual'] - result['residual']
                quad_error = invmax(difference)
                evidence.report['accuracy_gate_failures'].append(dict(case=name, gate='paired_quadrature_inverse', error=quad_error, tolerance=2e-11, passed=quad_error <= 2e-11))
                progress(name + ':live-operator')
                radial = RadialResponse(loads, action, branch.split('-')[1], deadline, lambda stage: progress(name + ':' + stage))
                evidence.check(name + ':radial_background', radial.base_constraint_residual <= 2e-12, radial.base_constraint_residual)
                momentum = MomentumMetricResponse(action, deadline, lambda stage: progress(name + ':' + stage))
                system, iterations = dict(matrix=matrix, inverse=inverse), []

                def record(row, direction, coupling, residual, metric):
                    path = save(name + '-reaction-iteration' + str(row['iteration']), direction=direction,
                        coupling=coupling, residual=residual, forcing=metric.forcing,
                        **{'metric_' + key: value for key, value in metric.solution.items()})
                    iterations.append(dict(row, path=path))
                    evidence.report['latest_iteration'] = dict(case=name, **iterations[-1])
                    progress(name + ':reaction-' + str(row['iteration']))

                reaction, reaction_metric, coupling, unused, history = solve_joint_rhs(system, radial, momentum, -result['residual'], record)
                evidence.check(name + ':live_solve', history[-1]['relative_residual'] <= 2e-11 and history[-1]['maximum_correction'] <= 2e-12,
                    history[-1])
                corrected_time = ResponseSum(mixed, reaction_metric)
                keys = ['state', 'rhs_coefficients', 'primitives', 'left']
                evidence.check(name + ':same_metric_grid', np.array_equal(mixed.solver.edges, reaction_metric.solver.edges))
                corrected = {key: mixed.solution[key] + reaction_metric.solution[key] for key in keys}
                paths['reaction'] = save(name + '-reaction', acceleration_change=reaction, forcing=result['residual'],
                    mode_rate=mode_rate, quadrature_difference=difference)
                paths['corrected_metric_time'] = save(name + '-corrected-metric-time', **corrected,
                    edges=mixed.solver.edges, **{'reaction_' + key: reaction_metric.solution[key] for key in keys})
                progress(name + ':corrected-material')
                checked = material_position_reaction(loads, action, native, directions, correction, mode_rate,
                    acceleration, position, metric_time, corrected_time, 64, deadline, lambda stage: progress(name + ':corrected-' + stage),
                    acceleration_change=reaction, include_native=False)
                corrected_residual = checked['residual'] - result['force_native']
                corrected_error = invmax(corrected_residual)
                evidence.report['accuracy_gate_failures'].append(dict(case=name, gate='re_evaluated_corrected_Euler',
                    error=corrected_error, tolerance=2e-11, passed=corrected_error <= 2e-11,
                    raw_error=float(np.max(abs(corrected_residual))), original_inverse_scale=invmax(result['residual'])))
                evidence.check(name + ':corrected_original_momentum_jet', invmax(checked['oracle_difference']) <= 2e-11,
                    invmax(checked['oracle_difference']))
                paths['corrected_material'] = save(name + '-corrected-material', **checked,
                    complete_residual=corrected_residual, inverse_residual=inverse.solve(corrected_residual.ravel()).reshape(loads.rates.shape))
                sensitivity_rows = []
                record_sensitivity = lambda row, direction, coupled, residual, metric: sensitivity_rows.append(dict(row))
                sensitive, sensitive_metric, unused, unused2, sensitive_history = solve_joint_rhs(system, radial, momentum, -difference, record_sensitivity)
                sensitivity_error = float(np.max(abs(sensitive)))
                evidence.report['accuracy_gate_failures'].append(dict(case=name, gate='live_material_sensitivity', error=sensitivity_error, tolerance=2e-11, passed=sensitivity_error <= 2e-11))
                paths['sensitivity'] = save(name + '-material-sensitivity', acceleration_change=sensitive,
                    edges=radial.solver.edges, **{'metric_' + key: sensitive_metric.solution[key] for key in keys})
                summary = dict(branch=branch, level=level, k0_max=float(np.max(abs(reaction))),
                    uncorrected_inverse_max=invmax(result['residual']), corrected_inverse_max=corrected_error,
                    original_momentum_jet_inverse_error=invmax(result['oracle_difference']),
                    material_inverse_error=quad_error, live_material_sensitivity=sensitivity_error,
                    native_halving_inverse_error=invmax(result['native_halving_difference']),
                    corrected_metric_time_max=float(np.max(abs(corrected['state']))),
                    original_momentum_replay_error=momentum_error, original_force_replay_error=force_error,
                    live_relative_residual=history[-1]['relative_residual'], valid_for_claim=False)
                summaries.append(summary)
                evidence.report['cases'].append(dict(branch=branch, level=level, summary=summary, paths=paths,
                    iterations=iterations, sensitivity_iterations=sensitivity_rows))
                progress(name + ':complete')
                del radial, momentum, loads, action, native, results, result, checked, matrix, inverse, original
                gc.collect()
        table = evidence.output / 'old-field-position-reaction.csv'
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
