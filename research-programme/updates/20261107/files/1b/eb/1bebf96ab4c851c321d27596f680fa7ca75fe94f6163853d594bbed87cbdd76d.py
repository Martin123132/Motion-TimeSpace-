from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_native_precision_context_20260929 import inherited_sources, restore_native
from annular_native_tangent_precision_repair_20260929 import repair_engine
from annular_joint_first_tangent_20260922 import RadialResponse, MomentumMetricResponse
from annular_joint_flow_derivative_v2_20260922 import solve_joint_rhs, DecimalSparseResidual
from annular_physical_native_kernel_20260928 import decimals
from scipy.sparse import load_npz
from decimal import Decimal, localcontext
from time import perf_counter
import argparse
import csv
import hashlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', default='annular-native-precision-live-response-attempt01')
    parser.add_argument('--max-seconds', type=float, default=3600)
    args = parser.parse_args()
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter() + args.max_seconds
    try:
        evidence.report.update(diagnostic_only=True, accepted_for_C0=False, valid_for_physics_claim=False,
            github_action=False, subagents_used=False, original_workbench_write=False,
            scope='Native-only precision correction propagated through the unchanged live operator',
            full_corrected_material_reintegrated=False, residual_update_uses_linearity=True,
            unchanged_wave_force_gate_still_outstanding=True, physics_coefficients_changed=False)
        evidence.own(evidence.root / 'DERIVATION-20260929-native-precision-live-response.md')
        candidate_path = evidence.output.parent / 'annular-native-tangent-precision-repair-attempt01/status.json'
        candidate = json.loads(candidate_path.read_text())
        evidence.own(candidate_path)
        evidence.check('both_grids_two_native_pairs_pass', candidate['state'] == 'complete'
            and candidate['all_native_pairs_passed'] and len(candidate['native_quadrature_checks']) == 4
            and all(row['passed'] for row in candidate['native_quadrature_checks']))
        for category in ['inputs', 'outputs']:
            for relative, digest in candidate[category].items():
                if relative == 'CURRENT_LOCAL_RESUME.md':
                    continue
                path = (evidence.root / relative).resolve()
                if not path.is_relative_to(evidence.root) or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                    raise RuntimeError('Changed repaired-force authority: ' + relative)
                evidence.own(path)
        digests = inherited_sources(evidence)

        def candidate_array(relative):
            path = evidence.root / relative
            if hashlib.sha256(path.read_bytes()).hexdigest() != candidate['outputs'][relative]:
                raise RuntimeError('Changed native repair output')
            with np.load(path, allow_pickle=False) as archive:
                return {name: archive[name].copy() for name in archive.files}

        def progress(stage):
            if perf_counter() > deadline:
                raise RuntimeError('Safe native response boundary')
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter() - started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)

        def save(name, **arrays):
            path = evidence.output / (name + '.npz')
            np.savez_compressed(path, **arrays)
            evidence.own(path, 'outputs')
            return str(path.relative_to(evidence.root))

        rows = []
        with localcontext() as context:
            context.prec = 70
            for level in ['fine', 'third']:
                progress(level + ':restore')
                setup = restore_native(evidence, digests, 'MTS-primary', level, deadline)
                read, inverse = setup['read'], setup['inverse']
                norm = lambda value: float(np.max(np.abs(inverse.solve(np.asarray(value, float).ravel()))))
                engine = repair_engine(setup['precision'])
                for label in [.017, .277]:
                    packet = engine.packet(label, 'decimal_tangents')
                    data, field_change, edge_change, beta_change, beta_r_change = packet
                    exact = engine.evaluate(label, 'decimal_tangents')[0]

                    def force(amount):
                        result = setup['native'].evaluate(data['edges'] + amount * edge_change,
                            data['field'] + amount * field_change, data['beta'] + amount * beta_change)
                        source = -sum(result['edge_gradient'] * data['displacement'], Decimal(0))
                        source -= sum(result['load'] * (data['beta_radial'] + amount * beta_r_change)
                            * data['displacement'][setup['native'].native_edges], Decimal(0))
                        return np.r_[-result['field_gradient'], source]

                    for step in [Decimal('1e-12'), Decimal('5e-13')]:
                        difference = (force(step) - force(-step)) / (2 * step) - exact
                        error = norm(np.outer(data['cardinal'], difference))
                        evidence.check(level + ':' + str(label) + ':new_force_finite_difference:' + str(step), error <= 2e-11, error)
                selected = {row['summary']['order']: row for row in candidate['cases'] if row['summary']['level'] == level}
                evidence.check(level + ':three_native_orders', sorted(selected) == [48, 64, 96])
                repaired = {order: candidate_array(selected[order]['path']) for order in [64, 96]}
                decimal_array = lambda values: np.array([Decimal(value) for value in values.ravel()], dtype=object).reshape(values.shape)
                upper = decimal_array(repaired[96]['force_decimal'])
                lower = decimal_array(repaired[64]['force_decimal'])
                force_change = np.asarray(upper - decimals(setup['original'][64]['force_native']), float)
                force_difference = np.asarray(upper - lower, float)
                evidence.check(level + ':native_pair_recheck', norm(force_difference) <= 2e-11, norm(force_difference))
                owner_name = 'annular-MTS-primary-matched-current-attempt01' if level == 'fine' else 'annular-MTS-primary-third-current-attempt02'
                owner = read(str((evidence.output.parent / owner_name / 'status.json').relative_to(evidence.root)))
                centre = next(row for row in owner['centres'] if row.get('route') == 'resampled') if level == 'fine' else owner['centres'][0]
                matrix = load_npz(evidence.root / centre['matrix_path'])
                system = dict(matrix=matrix, inverse=inverse)
                radial = RadialResponse(setup['loads'], setup['action'], 'primary', deadline, lambda stage: progress(level + ':' + stage))
                momentum = MomentumMetricResponse(setup['action'], deadline, lambda stage: progress(level + ':' + stage))
                evidence.check(level + ':unchanged_radial_background', radial.base_constraint_residual <= 2e-12, radial.base_constraint_residual)
                histories = {}
                answers = {}
                for name, rhs in [('correction', force_change), ('sensitivity', force_difference)]:
                    records = []
                    record = lambda row, direction, coupling, residual, metric: records.append(dict(row))
                    answer = solve_joint_rhs(system, radial, momentum, rhs, record)
                    histories[name] = records
                    answers[name] = answer
                    evidence.check(level + ':' + name + ':live_solve', records[-1]['relative_residual'] <= 2e-11
                        and records[-1]['maximum_correction'] <= 2e-12, records[-1])
                    progress(level + ':' + name + ':solved')
                direction, metric, coupling, unused, history = answers['correction']
                sensitive, sensitive_metric, unused, unused2, unused3 = answers['sensitivity']
                evidence.check(level + ':native_live_sensitivity', float(np.max(np.abs(sensitive))) <= 2e-11, float(np.max(np.abs(sensitive))))
                independent_coupling = momentum.accumulate(metric.values, complex_step=1e-25)
                coupling_error = norm(independent_coupling - coupling)
                evidence.check(level + ':metric_momentum_complex_oracle', coupling_error <= 2e-11, coupling_error)
                correction_residual = DecimalSparseResidual(matrix).evaluate(direction, independent_coupling, force_change)
                evidence.check(level + ':correction_equation', norm(correction_residual) <= 2e-11, norm(correction_residual))
                parent = read(str((evidence.output.parent / 'annular-position-reaction-diagnostic-attempt04/status.json').relative_to(evidence.root)))
                old = next(row for row in parent['cases'] if row['branch'] == 'MTS-primary' and row['level'] == level)
                old_reaction = read(old['paths']['reaction'])['acceleration_change']
                old_metric = read(old['paths']['corrected_metric_time'])
                old_checked = read(old['paths']['corrected_material'])['complete_residual']
                evidence.check(level + ':metric_grid_unchanged', np.array_equal(old_metric['edges'], metric.solver.edges))
                changed_metric = {key: old_metric[key] + metric.solution[key] for key in ['state', 'rhs_coefficients', 'primitives', 'left']}
                paths = dict(correction=save(level + '-native-live-correction', acceleration_change=direction,
                    force_change=force_change, correction_residual=correction_residual,
                    independent_coupling=independent_coupling, edges=metric.solver.edges,
                    **{'metric_' + key: value for key, value in metric.solution.items()}),
                    sensitivity=save(level + '-native-live-sensitivity', acceleration_change=sensitive,
                    force_difference=force_difference, edges=sensitive_metric.solver.edges,
                    **{'metric_' + key: value for key, value in sensitive_metric.solution.items()}),
                    candidate=save(level + '-native-repaired-reaction', acceleration_change=old_reaction + direction,
                    residual_by_linear_update=old_checked + correction_residual, edges=metric.solver.edges, **changed_metric))
                row = dict(level=level, native_force_change_inverse=norm(force_change),
                    k0_correction_max=float(np.max(np.abs(direction))),
                    corrected_k0_max=float(np.max(np.abs(old_reaction + direction))),
                    metric_time_correction_max=float(np.max(np.abs(metric.solution['state']))),
                    native_pair_inverse=norm(force_difference), native_live_pair_max=float(np.max(np.abs(sensitive))),
                    metric_coupling_oracle_inverse=coupling_error, correction_equation_inverse=norm(correction_residual),
                    corrected_equation_via_linear_update=norm(old_checked + correction_residual),
                    full_material_reintegration=False, seconds=perf_counter() - started, valid_for_claim=False)
                evidence.report['cases'].append(dict(summary=row, paths=paths, iterations=histories))
                rows.append(row)
                evidence.save()
                print(json.dumps(row), flush=True)
        path = evidence.output / 'native-precision-response.csv'
        with path.open('x', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        evidence.own(path, 'outputs')
        evidence.report.update(seconds=perf_counter() - started, native_only_response_complete=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
