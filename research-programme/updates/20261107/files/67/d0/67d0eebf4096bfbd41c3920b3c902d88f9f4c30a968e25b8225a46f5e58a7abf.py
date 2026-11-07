from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from annular_support_radial_response_20260928 import SupportRadialResponse, projected_response, gravitational_moments, symbolic_checks
from annular_joint_first_tangent_20260922 import MomentumMetricResponse
from annular_candidate_full_inverse_20260920 import BandedSourceInverse
from scipy.sparse import load_npz
from decimal import localcontext
from time import perf_counter
import contextlib
import csv
import gc
import hashlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-live-support-acceleration-attempt01', __file__)
    started, deadline = perf_counter(), perf_counter() + 10800
    try:
        evidence.report.update(new_trajectories=0, new_nonlinear_evolution_solves=0, github_action=False,
            subagents_used=False, protected_since='2026-09-28T12:10:23+00:00',
            scope='Live radial metric time-response and complete old field/source acceleration elimination in the s=sdot=0 channel; C0 and C1 metric-history blocks are not computed')
        evidence.own(evidence.root / 'DERIVATION-20260928-live-metric-support-acceleration.md')
        seal_path = evidence.output.parent / 'annular-support-shift-jet-final-integrity-20260928.json'
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
        evidence.check('prior_scientific_evidence_unchanged', seal['state'] == 'complete' and not bad, bad)
        read = lambda relative: load_owned(evidence, digests, evidence.root / relative)
        parent = read(str((evidence.output.parent / 'annular-support-shift-jet-attempt01/status.json').relative_to(evidence.root)))
        balance = read(str((evidence.output.parent / 'annular-directional-coupled-Euler-attempt02/status.json').relative_to(evidence.root)))
        symbolic_checks(evidence)

        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter() - started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
            if perf_counter() > deadline:
                raise RuntimeError('Safe completed-block wall boundary')

        def save(name, **arrays):
            path = evidence.output / (name + '.npz')
            np.savez_compressed(path, **arrays)
            evidence.own(path, 'outputs')
            return str(path.relative_to(evidence.root))

        def response_save(name, response):
            return save(name, **response.solution, forcing=response.forcing,
                delta_temporal=response.temporal, delta_velocity=response.velocity,
                edges=response.solver.edges, nodes=response.solver.nodes)

        summaries, current_rows, iterations = [], [], []
        with localcontext() as context:
            context.prec = 70
            for case in parent['cases']:
                branch, level = case['branch'], case['level']
                name = branch + '-' + level
                progress(name + ':restore')
                loads, action, sources = restore_case(evidence, digests, branch, level, deadline)
                directions = read(case['direction_path'])
                fixed = read(case['correction_path'])
                archived_owner = read(sources['parent'])
                centre = next(row for row in archived_owner['centres'] if row.get('route') == 'resampled') if level == 'fine' else archived_owner['centres'][0]
                matrix_path = evidence.root / centre['matrix_path']
                evidence.check(name + ':matrix_owned', str(matrix_path.relative_to(evidence.root)) in digests)
                matrix = load_npz(matrix_path)
                inverse = BandedSourceInverse(matrix, loads.rates.shape)
                response = SupportRadialResponse(loads, action, branch.split('-')[1], directions, deadline,
                    lambda stage: progress(name + ':' + stage))
                evidence.check(name + ':radial_background_replay', response.base_residual <= 2e-12, response.base_residual)
                progress(name + ':radial-response-ready')
                momentum = MomentumMetricResponse(action, deadline, lambda stage: progress(name + ':' + stage))
                zero = np.zeros_like(loads.rates)
                original_response = response.apply(zero)
                original_metric_momentum = momentum.accumulate(original_response.values)
                correction = fixed['correction'].copy()
                scale = max(inverse.residual_norm(fixed['coupling']), 1e-300)
                history = []
                for iteration in range(16):
                    live_response = response.apply(-correction)
                    metric_momentum = momentum.accumulate(live_response.values)
                    residual = fixed['coupling'] - (matrix @ correction.ravel()).reshape(correction.shape) + metric_momentum
                    change = inverse.solve(residual.ravel()).reshape(correction.shape)
                    relative = inverse.residual_norm(residual) / scale
                    row = dict(branch=branch, level=level, iteration=iteration, relative_old_Euler_residual=float(relative),
                        max_correction=float(np.max(abs(change))), radial_residual=live_response.residual)
                    history.append(row)
                    iterations.append(row)
                    progress(name + ':live-elimination-' + str(iteration) + ':residual-' + format(relative, '.4e'))
                    if relative <= 2e-11 and row['max_correction'] <= 2e-12:
                        break
                    if iteration > 1 and relative > 1.25 * history[-2]['relative_old_Euler_residual']:
                        raise RuntimeError('Live support elimination lost contraction')
                    correction += change
                else:
                    raise RuntimeError('Live support elimination did not converge')
                evidence.check(name + ':live_old_Euler_eliminated', relative <= 2e-11)
                paths = dict(original_response=response_save(name + '-original-radial-response', original_response),
                    live_response=response_save(name + '-compensated-radial-response', live_response))
                paths['projection'] = save(name + '-live-projection', correction=correction, fixed_correction=fixed['correction'],
                    fixed_coupling=fixed['coupling'], metric_momentum=metric_momentum, original_metric_momentum=original_metric_momentum,
                    old_Euler_residual=residual, saved_Euler_residual=fixed['solved_Euler_residual'])
                for mode, item in [('original', original_response), ('compensated', live_response)]:
                    checked = response.complex_check(item)
                    error = float(np.max(abs(checked - item.solution['state'])))
                    response_scale = max(float(np.max(abs(item.solution['state']))), 1e-300)
                    evidence.check(name + ':complex_radial:' + mode, error <= 2e-8 * response_scale + 1e-30,
                        dict(error=error, scale=response_scale, relative=error / response_scale))
                    paths[mode + '_complex'] = save(name + '-' + mode + '-complex-check', checked=checked,
                        difference=checked - item.solution['state'])
                packets = {}
                for mode, adjustment, item in [('original', zero, original_response), ('compensated', correction, live_response)]:
                    for order in [48, 64]:
                        progress(name + ':' + mode + ':material' + str(order))
                        packet = projected_response(loads, action, directions, adjustment, item, order)
                        paths[mode + '_material' + str(order)] = save(name + '-' + mode + '-material' + str(order), **packet)
                        packets[mode, order] = packet
                        evidence.check(name + ':' + mode + ':finite:' + str(order), np.isfinite(packet['totals']).all() and np.isfinite(packet['moments']).all())
                        if mode == 'original':
                            previous = read(case['material_paths'][0 if order == 48 else 1])
                            error = float(np.max(abs(packet['current'][:, 0] - previous['average'][0, :, 4])))
                            evidence.check(name + ':original_C2_replay:' + str(order), error <= 2e-22, error)
                    difference = float(np.max(abs(packets[mode, 64]['average'] - packets[mode, 48]['average'])))
                    norm_scale = max(abs(float(packets[mode, 48]['average'][-1])), 1e-300)
                    evidence.check(name + ':' + mode + ':norm_material48_64', difference <= 2e-6 * norm_scale + 1e-25,
                        dict(error=difference, scale=norm_scale))
                gravity = gravitational_moments(action, live_response, 24)
                gravity32 = gravitational_moments(action, live_response, 32)
                evidence.check(name + ':gravitational_quadrature', np.max(abs(gravity - gravity32)) <= 1e-24 + 1e-9 * np.max(abs(gravity32)), float(np.max(abs(gravity - gravity32))))
                compensated = packets['compensated', 64]['average']
                fixed_positive = float(compensated[0] + compensated[1])
                metric_addition = float(compensated[2] + compensated[3])
                effective = float(compensated[-1])
                old_metric_response = response.apply(correction, 0.)
                cross = projected_response(loads, action, directions, zero, old_metric_response, 48)
                cross_support_old = float(sum(cross['average'][2:4]))
                cross_old_support = float(correction.ravel() @ original_metric_momentum.ravel())
                old_case = next(row for row in balance['cases'] if row['branch'] == branch and row['level'] == level)
                old_balance = read(old_case['material_paths'][0])
                force = float(old_balance['average'][list(old_balance['channels']).index('coupled_direct')])
                removed = float(correction.ravel() @ fixed['solved_Euler_residual'].ravel())
                boundary = live_response.values(np.array([response.solver.edges[0], response.solver.edges[-1]]))
                outer_factor = response.solver.edges[-1] - 2 * response.state[0, -1, -1]
                boundary_error = max(abs(boundary[0, 0]), abs(boundary[1, -1] + boundary[0, -1] / outer_factor))
                evidence.check(name + ':radial_boundary_response', boundary_error <= 1e-25, float(boundary_error))
                summary = dict(branch=branch, level=level, fixed_metric_mass=float(fixed['effective_mass']),
                    positive_compensated_norm=fixed_positive, metric_addition=metric_addition, live_projected_coefficient=effective,
                    coefficient_ratio=effective / float(fixed['effective_mass']),
                    source_force=force, removed_old_Euler_work=removed, remaining_force=force - removed,
                    conditional_linear_amplitude=-(force - removed) / effective if effective != 0 else None,
                    iteration_count=len(history), old_Euler_relative_residual=float(relative),
                    cross_support_old=cross_support_old, cross_old_support=cross_old_support,
                    reciprocity_difference=cross_support_old - cross_old_support,
                    sparse_response_bytes=response.stored_bytes, max_mass_rate=float(np.max(abs(live_response.solution['state'][0]))),
                    max_log_lapse_rate=float(np.max(abs(live_response.solution['state'][1]))),
                    outer_mass_rate=float(boundary[0, -1]), radial_background_residual=response.base_residual)
                summaries.append(summary)
                for power in range(3):
                    currents = packets['compensated', 64]['current'][power]
                    current_rows.append(dict(branch=branch, level=level, power=power, direct_matter=float(currents[0]),
                        metric_matter=float(currents[1]), gravity=float(gravity32[power]),
                        total=float(currents[2] + gravity32[power])))
                evidence.report['cases'].append(dict(branch=branch, level=level, sources=sources, paths=paths,
                    direction_path=case['direction_path'], prior_probe_paths=case['probe_paths'], summary=summary))
                evidence.save()
                progress(name + ':saved')
                del response, momentum, inverse, matrix
                gc.collect()
        for name, rows in [('live-support-coefficients.csv', summaries), ('live-acceleration-current-moments.csv', current_rows), ('live-elimination-iterations.csv', iterations)]:
            path = evidence.output / name
            with path.open('w', newline='', encoding='utf-8') as stream:
                writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            evidence.own(path, 'outputs')
        evidence.report.update(seconds=perf_counter() - started, summaries=summaries, position_block_computed=False,
            completed_velocity_metric_history_computed=False, support_amplitude_evolved=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    with contextlib.redirect_stderr(__import__('sys').stdout):
        main()
