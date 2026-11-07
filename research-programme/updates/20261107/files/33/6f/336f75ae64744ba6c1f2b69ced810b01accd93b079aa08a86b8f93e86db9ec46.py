from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from annular_old_field_reaction_20260929 import material_reaction, symbolic_checks
from annular_physical_native_kernel_20260928 import NativeKernel
from annular_joint_first_tangent_20260922 import RadialResponse, MomentumMetricResponse, MetricResponse
from annular_joint_flow_derivative_v2_20260922 import solve_joint_rhs
from annular_candidate_full_inverse_20260920 import BandedSourceInverse
from derive_annular_direct_background_coupled_current_20260928 import TotalResponse
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
    parser.add_argument('--label', default='annular-old-field-reaction-attempt01')
    parser.add_argument('--max-seconds', type=float, default=10000)
    parser.add_argument('--case-limit', type=int, default=4)
    args = parser.parse_args()
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter() + args.max_seconds
    try:
        evidence.report.update(scope='Derived live old-field velocity-jet reaction', github_action=False,
            subagents_used=False, new_trajectories=0, original_workbench_write=False,
            inherited_position_density_precision_warnings=4, inherited_mixed_time_precision_warnings=4,
            combined_support_current_test_completed=False, source_units='code-normalized')
        evidence.own(evidence.root / 'DERIVATION-20260929-old-field-reaction.md')
        seal_path = evidence.output.parent / 'annular-position-metric-jet-final-integrity-20260928.json'
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
        evidence.check('prior_scientific_inputs_unchanged', seal['state'] == 'complete' and not bad, bad)
        read = lambda relative: load_owned(evidence, digests, evidence.root / relative)
        status = lambda name: read(str((evidence.output.parent / name / 'status.json').relative_to(evidence.root)))
        parent = status('annular-direct-background-coupled-current-attempt01')
        live = status('annular-live-support-acceleration-attempt01')
        positions = status('annular-compensated-position-attempt04')
        jets = status('annular-position-metric-jet-validation-attempt01')
        times = status('annular-live-compensation-time-attempt04')
        symbolic_checks(evidence)

        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter() - started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
            if perf_counter() > deadline:
                raise RuntimeError('Safe old-field reaction boundary')

        def save(name, **arrays):
            path = evidence.output / (name + '.npz')
            np.savez_compressed(path, **arrays)
            evidence.own(path, 'outputs')
            return str(path.relative_to(evidence.root))

        keys = ['state', 'rhs_coefficients', 'primitives', 'left']
        summaries = []
        with localcontext() as context:
            context.prec = 70
            for case in parent['cases'][:args.case_limit]:
                branch, level = case['branch'], case['level']
                name = branch + '-' + level
                progress(name + ':restore')
                loads, action, sources = restore_case(evidence, digests, branch, level, deadline)
                match = lambda report: next(row for row in report['cases'] if row['branch'] == branch and row['level'] == level)
                previous, position_case, jet_case, timed = map(match, [live, positions, jets, times])
                directions = read(previous['direction_path'])
                correction = read(previous['paths']['projection'])['correction']
                flow = read(case['paths']['flow'])
                position_archive = read(position_case['paths']['response'])
                velocity_archive = read(previous['paths']['live_response'])
                jet_archive = read(jet_case['paths']['completed_metric_time'])
                old_rate_archive = read(jet_case['paths']['transported_old_metric'])
                mode_rate = jet_archive['mode_rate']
                owner = read(sources['parent'])
                centre = next(row for row in owner['centres'] if row.get('route') == 'resampled') if level == 'fine' else owner['centres'][0]
                matrix_path = evidence.root / centre['matrix_path']
                evidence.check(name + ':matrix_owned', str(matrix_path.relative_to(evidence.root)) in digests)
                matrix = load_npz(matrix_path)
                inverse = BandedSourceInverse(matrix, loads.rates.shape)
                radial = RadialResponse(loads, action, branch.split('-')[1], deadline, lambda stage: progress(name + ':' + stage))
                evidence.check(name + ':radial_background', radial.base_constraint_residual <= 2e-12, radial.base_constraint_residual)
                restore = lambda archive: MetricResponse(radial.solver, {key: archive[key] for key in keys}, archive.get('forcing'), 0., [])
                position, velocity, trial = map(restore, [position_archive, velocity_archive, jet_archive])
                time_response = TotalResponse(restore(read(case['paths']['background_response'])), restore(read(case['paths']['velocity_response'])))
                packet = read(sources['packet'])
                native = NativeKernel(action.mesh, packet['gram_support'], branch.startswith('MTS'))
                momentum = MomentumMetricResponse(action, deadline, lambda stage: progress(name + ':' + stage))
                old_rate = restore(old_rate_archive)
                live_transport = (matrix @ mode_rate.ravel()).reshape(loads.rates.shape) + momentum.accumulate(old_rate.values)
                results, paths = {}, {}
                for order in [48, 64]:
                    progress(name + ':material' + str(order))
                    results[order] = material_reaction(loads, action, native, directions, correction, mode_rate,
                        flow['acceleration'], position, velocity, time_response, trial, order, deadline,
                        lambda stage: progress(name + ':' + stage))
                    paths['material' + str(order)] = save(name + '-material' + str(order), **results[order])
                result = results[48]
                momentum_error = float(np.max(abs(result['base_momentum'] - momentum.base_momentum())))
                evidence.check(name + ':original_momentum_replay', momentum_error <= 2e-16, momentum_error)
                identity_residual = result['momentum_rate'] - result['position'] - live_transport
                identity_inverse = inverse.solve(identity_residual.ravel()).reshape(loads.rates.shape)
                identity_error = float(np.max(abs(identity_inverse)))
                identity_tolerance = 2e-11 + 2e-8 * float(np.max(abs(mode_rate)))
                evidence.check(name + ':independent_material_Euler_chain', identity_error <= identity_tolerance,
                    dict(inverse_error=identity_error, tolerance=identity_tolerance, raw_error=float(np.max(abs(identity_residual)))))
                difference = results[64]['rhs'] - result['rhs']
                quad_inverse = inverse.solve(difference.ravel()).reshape(loads.rates.shape)
                quad_error = float(np.max(abs(quad_inverse)))
                evidence.check(name + ':material48_64_inverse', quad_error <= 2e-11, quad_error)
                system = dict(matrix=matrix, inverse=inverse)
                iterations = []

                def record(row, direction, coupling, residual, metric):
                    path = save(name + '-reaction-iteration' + str(row['iteration']), direction=direction,
                        coupling=coupling, residual=residual, forcing=metric.forcing,
                        **{'metric_' + key: value for key, value in metric.solution.items()})
                    iterations.append(dict(row, path=path))
                    evidence.report['latest_iteration'] = dict(case=name, **iterations[-1])
                    progress(name + ':reaction-' + str(row['iteration']))

                reaction, reaction_metric, coupling, unused, history = solve_joint_rhs(system, radial, momentum, result['rhs'], record)
                evidence.check(name + ':live_reaction_solved', history[-1]['relative_residual'] <= 2e-11 and history[-1]['maximum_correction'] <= 2e-12, history[-1])
                mixed = read(timed['paths']['mixed_response'])
                final = read(timed['iterations'][-1]['path'])
                velocity_time = {key: mixed[key] - final['metric_' + key] for key in keys}
                corrected = {key: position.solution[key] + velocity_time[key] - reaction_metric.solution[key] for key in keys}
                corrected_time = MetricResponse(radial.solver, corrected, None, 0., [])
                acceleration_change = mode_rate - reaction
                paths['reaction'] = save(name + '-reaction', reaction=reaction, additional_reaction=-mode_rate-reaction,
                    mode_rate=mode_rate, acceleration_change=acceleration_change, rhs=result['rhs'],
                    position=result['position'], force=result['force'], identity_residual=identity_residual,
                    identity_inverse=identity_inverse, quadrature_rhs_difference=difference, quadrature_inverse=quad_inverse)
                paths['corrected_metric_time'] = save(name + '-corrected-metric-time', **corrected,
                    edges=radial.solver.edges, reaction_metric_state=reaction_metric.solution['state'])
                progress(name + ':independent-corrected-material')
                checked = material_reaction(loads, action, native, directions, correction, acceleration_change / 2,
                    flow['acceleration'], position, velocity, time_response, corrected_time, 48, deadline,
                    lambda stage: progress(name + ':corrected-' + stage))
                corrected_residual = checked['momentum_rate'] - checked['force']
                corrected_inverse = inverse.solve(corrected_residual.ravel()).reshape(loads.rates.shape)
                corrected_error = float(np.max(abs(corrected_inverse)))
                evidence.check(name + ':independent_corrected_old_Euler', corrected_error <= identity_tolerance,
                    dict(inverse_error=corrected_error, raw_error=float(np.max(abs(corrected_residual))), tolerance=identity_tolerance))
                paths['corrected_material'] = save(name + '-corrected-material', **checked,
                    residual=corrected_residual, inverse_residual=corrected_inverse)
                sensitivity_iterations = []

                def record_sensitivity(row, direction, coupled, residual, metric):
                    sensitivity_iterations.append(dict(row))

                sensitive, sensitive_metric, unused, unused2, sensitive_history = solve_joint_rhs(system, radial, momentum, difference, record_sensitivity)
                sensitivity_error = float(np.max(abs(sensitive)))
                evidence.check(name + ':live_quadrature_sensitivity', sensitivity_error <= 2e-11, sensitivity_error)
                paths['sensitivity'] = save(name + '-material-sensitivity', direction=sensitive,
                    **{'metric_' + key: value for key, value in sensitive_metric.solution.items()})
                summary = dict(branch=branch, level=level, reaction_max=float(np.max(abs(reaction))),
                    mode_rate_max=float(np.max(abs(mode_rate))), additional_reaction_max=float(np.max(abs(-mode_rate-reaction))),
                    corrected_acceleration_max=float(np.max(abs(acceleration_change))),
                    corrected_metric_time_max=float(np.max(abs(corrected['state']))),
                    uncorrected_Euler_inverse_max=float(np.max(abs(inverse.solve(result['direct_trial_Euler'].ravel())))),
                    corrected_Euler_inverse_max=corrected_error, independent_identity_inverse_max=identity_error,
                    material_inverse_error=quad_error, material_live_sensitivity=sensitivity_error,
                    live_relative_residual=history[-1]['relative_residual'], position_rhs_max=float(np.max(abs(result['position']))),
                    force_rhs_max=float(np.max(abs(result['force']))), rhs_max=float(np.max(abs(result['rhs']))))
                summaries.append(summary)
                evidence.report['cases'].append(dict(branch=branch, level=level, summary=summary, paths=paths,
                    iterations=iterations, sensitivity_iterations=sensitivity_iterations))
                progress(name + ':complete')
                del radial, momentum, loads, action, native, results, result, checked, matrix, inverse
                gc.collect()
        table = evidence.output / 'old-field-reaction.csv'
        with table.open('w', newline='', encoding='utf-8') as handle:
            writer = csv.DictWriter(handle, fieldnames=list(summaries[0]))
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
