from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from annular_reacted_support_columns_20260929 import columns_layer, gravity_columns, compatibility
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_joint_first_tangent_20260922 import MetricResponse
from annular_joint_flow_derivative_20260922 import JointMetricTangent
from derive_annular_direct_background_coupled_current_20260928 import TotalResponse, CoordinateAdapter
from annular_physical_native_kernel_20260928 import NativeKernel
from annular_radial_Ward_moments_20260921 import prepare
from annular_support_radial_response_20260928 import gravitational_moments
from annular_aligned_acceleration_channels_20260929 import acceleration_channels_aligned as acceleration_channels
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
    parser.add_argument('--label', default='annular-reacted-support-columns-attempt02')
    parser.add_argument('--max-seconds', type=float, default=6600)
    args = parser.parse_args()
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter() + args.max_seconds
    try:
        evidence.report.update(scope='Corrected support force and three weak currents at zero-position jet',
            github_action=False, subagents_used=False, new_trajectories=0, original_workbench_write=False,
            inherited_position_density_precision_warnings=4, inherited_mixed_time_precision_warnings=4,
            finite_amplitude_solution_established=False, residual_baseline_subtracted=False)
        evidence.own(evidence.root / 'DERIVATION-20260929-reacted-force-current-columns.md')
        evidence.own(evidence.root / 'DERIVATION-20260929-C2-cancellation-correction.md')
        parent_path = evidence.output.parent / args.parent / 'status.json'
        parent = json.loads(parent_path.read_text())
        evidence.own(parent_path)
        evidence.check('old_reaction_complete_all_four_cases', parent['state'] == 'complete' and len(parent['cases']) == 4)
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
        evidence.check('owned_inputs_unchanged', not bad, bad)
        failed_path = evidence.output.parent / 'annular-reacted-support-columns-attempt01/status.json'
        failed = json.loads(failed_path.read_text())
        evidence.own(failed_path)
        failed_checks = [row for row in failed['checks'] if not row['passed']]
        evidence.check('reuse_failure_is_only_raw_C2_replay', failed['state'] == 'failed' and len(failed_checks) == 1
            and failed_checks[0]['name'] == 'reference-reference-third:inherited_C2_replay')
        for category in ['inputs', 'outputs']:
            for relative, expected in failed[category].items():
                if relative == 'CURRENT_LOCAL_RESUME.md':
                    continue
                path = evidence.root / relative
                if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                    raise RuntimeError('Changed reusable column input: ' + relative)
                digests[str(path.relative_to(evidence.root))] = expected
                evidence.own(path)
        failed_details = {row['name']: row for row in failed['checks']}
        evidence.report['reuse'] = dict(reference_material_cases=2, reason='Reuse unchanged baseline/C1 rows; replace cancellation-prone C2 evaluation algebraically',
            raw_failed_gate=failed_checks[0], tolerances_unchanged=True)

        manufactured_matrix = np.array([[1., 2.], [2., -1.], [.5, 3.], [-2., 1.5]])
        manufactured_amplitudes = np.array([.3, -.7])
        manufactured = np.vstack([-manufactured_matrix @ manufactured_amplitudes, manufactured_matrix.T])
        manufactured_error = np.full_like(manufactured, 1e-12)
        compatible = compatibility(manufactured, manufactured, manufactured_error, manufactured_error)
        evidence.check('manufactured_joint_compatibility', compatible['rank_resolved']
            and compatible['residual_within_sampled_uncertainty']
            and np.max(abs(np.array(compatible['amplitudes']) - manufactured_amplitudes)) <= 1e-12
            and all(row['all_rows_within_sampled_uncertainty'] for row in compatible['exact_force_current_pairs']))
        incompatible = manufactured.copy()
        incompatible[0, 3] += .1
        rejected = compatibility(incompatible, incompatible, manufactured_error, manufactured_error)
        evidence.check('manufactured_joint_incompatibility', not rejected['residual_within_sampled_uncertainty']
            and not any(row.get('all_rows_within_sampled_uncertainty', False) for row in rejected['exact_force_current_pairs']))
        read = lambda relative: load_owned(evidence, digests, evidence.root / relative)
        status = lambda name: read(str((evidence.output.parent / name / 'status.json').relative_to(evidence.root)))
        background = status('annular-direct-background-coupled-current-attempt01')
        live = status('annular-live-support-acceleration-attempt01')
        current_path = evidence.output.parent / 'annular-live-support-acceleration-attempt01/live-acceleration-current-moments.csv'
        evidence.check('old_C2_table_owned', str(current_path.relative_to(evidence.root)) in digests)
        with current_path.open(newline='', encoding='utf-8') as handle:
            old_currents = list(csv.DictReader(handle))
        baseline_path = evidence.output.parent / 'annular-direct-background-coupled-current-attempt01/direct-current-moments.csv'
        evidence.check('old_baseline_table_owned', str(baseline_path.relative_to(evidence.root)) in digests)
        with baseline_path.open(newline='', encoding='utf-8') as handle:
            old_baselines = list(csv.DictReader(handle))

        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter() - started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
            if perf_counter() > deadline:
                raise RuntimeError('Safe support column boundary')

        def save(name, **arrays):
            path = evidence.output / (name + '.npz')
            np.savez_compressed(path, **arrays)
            evidence.own(path, 'outputs')
            return str(path.relative_to(evidence.root))

        table_rows = []
        with localcontext() as context:
            context.prec = 70
            for case in parent['cases']:
                branch, level = case['branch'], case['level']
                name = branch + '-' + level
                progress(name + ':restore')
                loads, action, sources = restore_case(evidence, digests, branch, level, deadline)
                match = lambda report: next(row for row in report['cases'] if row['branch'] == branch and row['level'] == level)
                previous, flow_case = match(live), match(background)
                restore = lambda archive: MetricResponse(*reconstructed_solver(archive), archive.get('forcing'), 0., [])
                base_background = restore(read(flow_case['paths']['background_response']))
                base_velocity = restore(read(flow_case['paths']['velocity_response']))
                baseline_time = TotalResponse(base_background, base_velocity)
                tangent = JointMetricTangent(CoordinateAdapter(base_background), [base_velocity])
                velocity = restore(read(previous['paths']['live_response']))
                corrected_time = restore(read(case['paths']['corrected_metric_time']))
                reaction = read(case['paths']['reaction'])
                sensitivity = read(case['paths']['sensitivity'])
                metric_uncertainty = MetricResponse(velocity.solver,
                    {key: -sensitivity['metric_' + key] for key in ['state', 'rhs_coefficients', 'primitives', 'left']}, None, 0., [])
                acceleration_uncertainty = -sensitivity['direction']
                acceleration = read(flow_case['paths']['flow'])['acceleration']
                polynomial, unused = prepare(action, loads, acceleration)
                directions = read(previous['direction_path'])
                correction = read(previous['paths']['projection'])['correction']
                packet = read(sources['packet'])
                native = NativeKernel(packet['mesh'], packet['gram_support'], branch.startswith('MTS'))
                gravity24 = gravity_columns(action, velocity, corrected_time, baseline_time, 24)
                gravity32 = gravity_columns(action, velocity, corrected_time, baseline_time, 32)
                gravity_error = abs(gravity32 - gravity24)
                gravity_reaction_delta = gravitational_moments(action, metric_uncertainty, 32)
                evidence.check(name + ':gravity24_32', float(np.max(gravity_error)) <= 2e-17, float(np.max(gravity_error)))
                paths, averages, precision, raw_C2_changes = {}, [], [], []
                native_error, face_error, spatial_error, complex_error = 0., 0., 0., 0.
                for order in [48, 64]:
                    labels, weights = np.polynomial.legendre.leggauss(order)
                    labels, weights = labels / 2, weights / 2
                    weights *= 6 * (labels + .5) * (.5 - labels)
                    if branch == 'reference-reference':
                        saved_path = evidence.output.parent / 'annular-reacted-support-columns-attempt01' / (name + '-columns' + str(order) + '.npz')
                        prior = read(str(saved_path.relative_to(evidence.root)))
                        labels, weights = prior['labels'], prior['weights']
                        layers, reaction_deltas = prior['layers'], prior['reaction_deltas']
                        restored_checks = {}
                        for key in ['native_product_rule', 'wave_cell_face_identity', 'spatial8_12', 'complex_step_stability']:
                            item = failed_details[name + ':' + key]
                            evidence.check(name + ':reuse:' + key + ':' + str(order), item['passed'], item['detail'])
                            restored_checks[key] = item['detail']
                        native_error = restored_checks['native_product_rule']
                        face_error = restored_checks['wave_cell_face_identity']
                        spatial_error = restored_checks['spatial8_12']
                        complex_error = restored_checks['complex_step_stability']
                    else:
                        layers, reaction_deltas = [], []
                        for index, label in enumerate(labels):
                            result = columns_layer(native, loads, action, tangent, acceleration, polynomial, directions, correction,
                                reaction['acceleration_change'], velocity, corrected_time, baseline_time, label,
                                acceleration_uncertainty=acceleration_uncertainty, metric_uncertainty=metric_uncertainty)
                            layer_values = np.array([result[key] for key in ['baseline', 'column1', 'column2']])
                            layers.append(layer_values)
                            reaction_deltas.append(result['reaction_column_delta'])
                            native_error = max(native_error, result['native_linear_error'])
                            face_error = max(face_error, result['face_identity_error'])
                            if order == 64 and index == 31:
                                for spatial, step in [(8, 1e-25), (12, 1e-20)]:
                                    check = columns_layer(native, loads, action, tangent, acceleration, polynomial, directions, correction,
                                        reaction['acceleration_change'], velocity, corrected_time, baseline_time, label, spatial, step)
                                    discrepancy = float(np.max(abs(np.array([check[key] for key in ['baseline', 'column1', 'column2']]) - layer_values)))
                                    if spatial == 8:
                                        spatial_error = discrepancy
                                    else:
                                        complex_error = discrepancy
                            if index % 8 == 7:
                                progress(name + ':material' + str(order) + '-label' + str(index + 1))
                    average = np.einsum('l,lrc->rc', weights, np.array(layers))
                    total = average.copy()
                    total[:, 1:] += gravity32
                    raw_C2 = total[2].copy()
                    old_direction = np.column_stack([directions['field_vertices'] - correction[:, :-1], -correction[:, -1]])
                    total[2] = acceleration_channels(action, loads, directions, old_direction, velocity, 1., order, deadline)
                    raw_C2_changes.append(total[2] - raw_C2)
                    average[2] = total[2]
                    average[2, 1:] -= gravity32[2]
                    reaction_delta = weights @ np.array(reaction_deltas)
                    reaction_delta[1:] += gravity_reaction_delta
                    precision.append(reaction_delta)
                    averages.append(total)
                    paths['material' + str(order)] = save(name + '-columns' + str(order), labels=labels, weights=weights,
                        layers=np.array(layers), matter=average, gravity=gravity32, total=total,
                        reaction_deltas=np.array(reaction_deltas), reaction_delta=reaction_delta,
                        raw_complete_C2=raw_C2, cancellation_free_C2=total[2])
                error = abs(averages[1] - averages[0])
                error[:, 1:] += gravity_error
                error[1] += np.maximum(abs(precision[0]), abs(precision[1]))
                error[2] += np.maximum(abs(raw_C2_changes[0]), abs(raw_C2_changes[1]))
                evidence.check(name + ':material48_64', float(np.max(abs(averages[1] - averages[0]))) <= 2e-17,
                    float(np.max(abs(averages[1] - averages[0]))))
                evidence.check(name + ':native_product_rule', native_error <= 1e-35, native_error)
                evidence.check(name + ':wave_cell_face_identity', face_error <= 2e-17, face_error)
                evidence.check(name + ':spatial8_12', spatial_error <= 2e-17, spatial_error)
                evidence.check(name + ':complex_step_stability', complex_error <= 2e-17, complex_error)
                inherited_baseline = np.r_[flow_case['summary']['source_force'],
                    [float(next(row for row in old_baselines if row['branch'] == branch and row['level'] == level
                        and int(row['material_order']) == 64 and int(row['power']) == power)['total']) for power in range(3)]]
                baseline_error = float(np.max(abs(averages[1][0] - inherited_baseline)))
                evidence.check(name + ':existing_baseline_replay', baseline_error <= 2e-17, float(baseline_error))
                inherited_C2 = np.r_[previous['summary']['live_projected_coefficient'],
                    [float(next(row for row in old_currents if row['branch'] == branch and row['level'] == level and int(row['power']) == power)['total']) for power in range(3)]]
                acceleration_error = abs(averages[1][2] - inherited_C2)
                evidence.check(name + ':inherited_C2_replay', bool(np.all(acceleration_error <= 2e-24 + 2e-6 * abs(inherited_C2))),
                    dict(error=acceleration_error.tolist(), inherited=inherited_C2.tolist()))
                diagnostic = compatibility(averages[0], averages[1], error, error)
                paths['combined'] = save(name + '-combined', coarse=averages[0], fine=averages[1],
                    sampled_uncertainty=error, inherited_C2=inherited_C2, gravity24=gravity24, gravity32=gravity32)
                for index, label in enumerate(['force', 'current_h0', 'current_h1', 'current_h2']):
                    table_rows.append(dict(branch=branch, level=level, condition=label, baseline=float(averages[1][0, index]),
                        C1=float(averages[1][1, index]), C2=float(averages[1][2, index]),
                        baseline_error=float(error[0, index]), C1_error=float(error[1, index]), C2_error=float(error[2, index])))
                evidence.report['cases'].append(dict(branch=branch, level=level, paths=paths, diagnostic=diagnostic,
                    max_face_identity_error=face_error, max_native_product_error=native_error,
                    spatial_error=spatial_error, complex_error=complex_error, baseline_replay_error=float(baseline_error),
                    raw_C2_difference=np.asarray(raw_C2_changes).tolist(),
                    raw_C2_evaluator_replay_pass=bool(np.all(abs(raw_C2 - inherited_C2) <= 2e-24 + 2e-6 * abs(inherited_C2))),
                    C2_evaluation='analytic acceleration block; raw complete-current derivative retained'))
                progress(name + ':complete')
                del loads, action, native
                gc.collect()
        path = evidence.output / 'reacted-force-current-columns.csv'
        with path.open('w', newline='', encoding='utf-8') as handle:
            writer = csv.DictWriter(handle, fieldnames=list(table_rows[0]))
            writer.writeheader()
            writer.writerows(table_rows)
        evidence.own(path, 'outputs')
        evidence.report['seconds'] = perf_counter() - started
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
