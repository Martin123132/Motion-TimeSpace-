import argparse
import hashlib
import json
import re
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from annular_adm_mixed_action_20260909 import MixedActionBasis
    from annular_first_derivative_energy_20260909 import affine_lift_matrix
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_metric_schur_bound_20260909 import schur_blocks
    from annular_metric_source_bound_20260909 import exact_lapse_margin, independent_first_source, normalized_mass_rows, scalar_source_data, source_bound
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian

    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['derive', 'seal'])
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260909'
    destination = intake / 'annular-metric-first-source-and-lapse-trace-derived'
    final_path = intake / 'annular-metric-first-source-and-lapse-trace-final-integrity.json'
    inputs, outputs = {}, {}

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def own(path):
        inputs[str(path.relative_to(root))] = digest(path)

    def artifact(path):
        outputs[str(path.relative_to(root))] = digest(path)

    def inherit(table, inherited):
        for name, expected in inherited.items():
            actual = digest(root / name)
            if actual != expected or name in table and table[name] != actual:
                raise RuntimeError('Changed evidence: ' + name)
            table[name] = actual

    def loaded(path):
        own(path)
        with numerical.load(path) as handle:
            return {name: handle[name].copy() for name in handle.files}

    prior_path = intake / 'annular-metric-Schur-box-final-integrity.json'
    prior = json.loads(prior_path.read_text())
    if prior['state'] != 'complete':
        raise RuntimeError('Previous inverse seal incomplete.')
    inherit(inputs, prior['inputs'])
    inherit(outputs, prior['outputs'])
    own(prior_path)
    scripts = ['annular_metric_source_bound_20260909.py', 'derive_annular_metric_source_bound_20260909.py']
    for name in scripts:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    if arguments.phase == 'derive':
        destination.mkdir(exist_ok=False)
        (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())
        report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': inputs, 'outputs': outputs, 'checks': [], 'samples': [], 'manufactured': [], 'first_effective_source_bound_from_scalar_graph_energy_derived': True, 'pointwise_lapse_rate_and_outer_trace_bound_derived': True, 'no_metric_time_derivatives_used_in_bound_inputs_except_actual_inner_mass_rate': True, 'remaining_inputs': ['uniform scalar graph energy over time', 'spatial coefficient Lipschitz control', 'actual physical inner mass-rate trace', 'prescribed scalar endpoint accelerations and outer clock rate'], 'second_effective_source_bound_derived': False, 'solution_stays_in_box_proved': False, 'full_coupled_DAE_solved': False, 'valid_for_physics_claim': False}

        def save():
            (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

        def check(name, passed, detail=None):
            report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
            if not passed:
                raise RuntimeError('Failed check: ' + name + ' ' + repr(detail))

        def maximum(values):
            return float(numerical.max(abs(values)))

        def metric_norm(vector, matrix):
            return float(numerical.sqrt(max(0.0, vector @ matrix @ vector)))

        def dual_norm(vector, matrix):
            return metric_norm(vector, numerical.linalg.inv(matrix))

        def evaluate(label, system, packed, include_gram, endpoint_acceleration, clock_rate, old=None, jets=None):
            basis = system.basis
            tangent = system.constraint_tangent(packed, include_gram, endpoint_acceleration, clock_rate)
            derivative = tangent['packed_speed']
            blocks = schur_blocks(system, packed, include_gram)
            scalar = scalar_source_data(system, packed, include_gram, endpoint_acceleration)
            bounds = source_bound(system, packed, include_gram, scalar, derivative[0], clock_rate, endpoint_acceleration, True)
            count = system.node_count
            lift = numerical.zeros_like(packed)
            lift[system.slices[0]] = derivative[0]
            lift[system.slices[2]] = scalar['velocity_boundary'][:count]
            lift[system.slope_slice] = scalar['velocity_boundary'][count:]
            independent = independent_first_source(system, packed, include_gram, blocks, scalar, lift, clock_rate)
            raw = -tangent['data_derivative'] - blocks['jacobian'] @ lift
            effective = raw[blocks['metric_indices']] - blocks['coupling'] @ numerical.linalg.solve(blocks['scalar_mass'], raw[blocks['velocity_indices']])
            check(label + '_independent_metric_data_derivative', maximum(independent['metric_data'] - tangent['data_derivative'][blocks['metric_indices']]) < 2e-10)
            check(label + '_canonical_velocity_data_is_stiffness_force', maximum(tangent['data_derivative'][blocks['velocity_indices']] - scalar['mass_free'] @ scalar['graph_force']) < 2e-10)
            check(label + '_independent_effective_source', maximum(effective - independent['source']) < 2e-10)
            check(label + '_all_fixed_boundary_entries_lifted', maximum((derivative - lift)[system.fixed]) < 1e-14)
            check(label + '_rho_time_pointwise_Cauchy', bool(numerical.all(scalar['rho_time']**2 <= 4 * system.density * scalar['rho_q'] + 1e-25)))
            check(label + '_rho_q_total_control', float(numerical.sum(scalar['rho_q'])) <= scalar['q_gradient_norm']**2 + 1e-14)
            check(label + '_rho_time_no_q_gradient_sup_assumption', scalar['rho_time_norm'] <= numerical.sqrt(8) * .03 * scalar['q_gradient_norm'] + 1e-12)
            check(label + '_energy_controls_q_radial', scalar['q_gradient_norm'] <= bounds['q_gradient_bound'] + 1e-12)
            check(label + '_affine_force_uniform_bound', scalar['lift_force_norm'] <= bounds['affine_force_bound'] + 1e-10)
            check(label + '_energy_controls_full_stiffness_force', scalar['graph_force_norm'] <= bounds['graph_force_bound'] + 1e-10)
            check(label + '_Gram_does_not_force_affine_lift', maximum(scalar['matrices']['K_Gram'] @ (affine_lift_matrix(basis) @ system.scalar[[0, -1]])) < 1e-10)
            measured_source = dual_norm(effective, blocks['metric_norm'])
            mass_dual = dual_norm(effective[:count], blocks['mass_norm'])
            lapse_dual = dual_norm(effective[count:], blocks['lapse_norm'])
            response = metric_norm((derivative - lift)[blocks['metric_indices']], blocks['metric_norm'])
            check(label + '_mass_source_dual_bound', mass_dual <= bounds['source_mass_dual_bound'] + 1e-10)
            check(label + '_lapse_source_dual_bound', lapse_dual <= bounds['source_lapse_dual_bound'] + 1e-10)
            check(label + '_combined_source_and_metric_response', measured_source <= bounds['source_dual_bound'] + 1e-10 and response <= bounds['metric_response_bound'] + 1e-10)
            mass_lift = numerical.zeros_like(lift)
            mass_lift[system.slices[0]] = derivative[0]
            extended_mass = blocks['jacobian'][blocks['metric_indices'], :] @ mass_lift - blocks['coupling'] @ numerical.linalg.solve(blocks['scalar_mass'], blocks['jacobian'][blocks['velocity_indices'], :] @ mass_lift)
            physical_source = effective + extended_mass
            mass_response = derivative[system.slices[0]][1:] - derivative[0]
            lapse_response = derivative[system.slices[1]]
            a_response = blocks['A'] @ mass_response + extended_mass[:count]
            spatial_f = 1 - 2 * basis.face_value @ packed[system.slices[0]] / basis.quadrature
            principal = basis.face_gradient[:, 1:].T @ ((basis.quadrature_weights / (system.kappa * numerical.sqrt(spatial_f)))[:, None] * basis.node_value)
            lower_response = (blocks['B'] - principal) @ lapse_response
            row_direct = maximum(normalized_mass_rows(basis, physical_source[:count]))
            row_mass = maximum(normalized_mass_rows(basis, a_response))
            row_lower = maximum(normalized_mass_rows(basis, lower_response))
            check(label + '_normalized_direct_mass_row_bound', row_direct <= bounds['normalized_row_direct_bound'] + 1e-9, {'measured': row_direct, 'bound': bounds['normalized_row_direct_bound']})
            check(label + '_normalized_mass_response_bound', row_mass <= bounds['normalized_row_mass_bound'] + 1e-9)
            check(label + '_normalized_lower_lapse_row_bound', row_lower <= bounds['normalized_row_lapse_lower_bound'] + 1e-9)
            check(label + '_actual_mass_row_retains_natural_boundary', maximum(principal @ lapse_response - (physical_source[:count] - a_response - lower_response)) < 2e-10)
            mass_sup, lapse_sup = maximum(derivative[system.slices[0]]), maximum(lapse_response)
            check(label + '_mass_pointwise_rate', mass_sup <= bounds['mass_rate_sup_bound'] + 1e-10)
            check(label + '_lapse_pointwise_rate_and_outer_trace', lapse_sup <= bounds['lapse_rate_sup_bound'] + 1e-10 and abs(lapse_response[-1]) <= bounds['lapse_rate_sup_bound'] + 1e-10)
            check(label + '_same_outer_row_and_slope_dofs', system.face_count - 1 in blocks['metric_indices'] and all(index in system.free_velocity_indices for index in range(system.slope_slice.start, system.slope_slice.stop)))
            if old is not None:
                check(label + '_old_first_source_unchanged', maximum(old['source_order1'] - effective) < 2e-11)
                check(label + '_old_metric_schur_unchanged', maximum(old['schur'] - blocks['schur']) == 0)
                check(label + '_physical_shift_mismatch_preserved', maximum(old['full_shift_residual'] - tangent['shift_residual']) < 1e-12 and numerical.array_equal(old['old_physical_mismatch'], jets['physical_mismatch']) and numerical.array_equal(old['old_physical_mismatch_time'], jets['jet_physical_mismatch_time']))
            measured = {'source_dual': measured_source, 'source_mass_dual': mass_dual, 'source_lapse_dual': lapse_dual, 'metric_response': response, 'mass_rate_sup': mass_sup, 'lapse_rate_sup': lapse_sup, 'outer_lapse_rate': float(lapse_response[-1]), 'q_gradient': scalar['q_gradient_norm'], 'graph_force': scalar['graph_force_norm'], 'affine_force': scalar['lift_force_norm'], 'rho_time_norm': scalar['rho_time_norm'], 'normalized_direct_row': row_direct, 'normalized_mass_row': row_mass, 'normalized_lower_lapse_row': row_lower}
            output = destination / (label + '.npz')
            saved = {'effective_source': effective, 'independent_source': independent['source'], 'packed_speed': derivative, 'rho_q': scalar['rho_q'], 'rho_time': scalar['rho_time'], 'full_shift_residual': tangent['shift_residual']}
            if old is not None:
                saved.update(old_physical_mismatch=old['old_physical_mismatch'], old_physical_mismatch_time=old['old_physical_mismatch_time'])
            numerical.savez_compressed(output, **saved)
            artifact(output)
            return {'label': label, 'bounds': bounds, 'measured': measured}

        save()
        try:
            report['exact_lapse_margin'] = exact_lapse_margin()
            check('exact_common_box_lapse_principal_margin_gt_5_over_2', report['exact_lapse_margin']['greater_than_5_over_2'])
            case_path = intake / 'annular-constraint-correction-initial/canonical.json'
            own(case_path)
            case = json.loads(case_path.read_text())
            constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
            kappa = float(symbolic.sympify(case['normalization_kappa']))
            for intervals in [16, 32, 64]:
                steps = 64 if intervals == 64 else 32
                for branch in ['GR', 'metric_Gram']:
                    tag = 'canonical_N' + str(intervals) + '_' + branch
                    source = loaded(intake / 'annular-released-Hermite-initial-derived' / (tag + '.npz'))
                    folder = 'annular-boundary-N64-evolution-smoke' if intervals == 64 else 'annular-released-Hermite-evolution-smoke'
                    trajectory = loaded(intake / folder / (tag + '_steps' + str(steps) + '.npz'))
                    basis = MixedActionBasis(source['radius'])
                    links = MetricLinkQuadrature(basis)
                    count = basis.radii.size
                    for index in [0, steps // 2, steps]:
                        label = tag + '_sample' + str(index)
                        report['active_job'] = label
                        save()
                        time, state = trajectory['time'][index], trajectory['state'][index]
                        scalar, slope, momentum, slope_momentum = [state[part * count:(part + 1) * count] for part in range(4)]
                        packed = state[4 * count:]
                        system = ReleasedHermiteRouthian(basis, scalar, slope, constants, kappa, momentum, slope_momentum, source['outer_clock'][0] + time * source['outer_clock'][1], links)
                        old = loaded(intake / 'annular-metric-Schur-bound-derived' / (label + '.npz'))
                        jets = loaded(intake / 'annular-metric-flux-jets-derived' / (label + '.npz'))
                        row = evaluate(label, system, packed, branch != 'GR', source['endpoint_acceleration'], source['outer_clock'][1], old, jets)
                        row.update(intervals=intervals, branch=branch, time=float(time))
                        report['samples'].append(row)
                        save()
                        if index == steps:
                            print(json.dumps({'label': label, 'energy': row['bounds']['energy'], 'measured': row['measured'], 'source_bound': row['bounds']['source_dual_bound'], 'lapse_sup_bound': row['bounds']['lapse_rate_sup_bound']}), flush=True)
            for intervals in [16, 64]:
                basis = MixedActionBasis(numerical.linspace(47 / 8, 49 / 8, intervals + 1))
                links = MetricLinkQuadrature(basis)
                count = basis.radii.size
                for mode in ['vacuum', 'oscillatory_velocity']:
                    scalar = numerical.zeros(count) if mode == 'vacuum' else .002 * (basis.radii - basis.radii[0])
                    slope = numerical.zeros(count) if mode == 'vacuum' else basis.spacing * (.002 - basis.derivative @ scalar)
                    system = ReleasedHermiteRouthian(basis, scalar, slope, constants, kappa, numerical.zeros(count), numerical.zeros(count), 1.0, links)
                    packed = numerical.zeros(system.count)
                    packed[system.slices[0]] = 1.0
                    packed[system.slices[1]] = numerical.sqrt(1 - 2 / basis.radii)
                    if mode != 'vacuum':
                        packed[system.slices[2]] = .004 * (-1.)**numerical.arange(count)
                        packed[system.slope_slice] = -basis.spacing * (basis.derivative @ packed[system.slices[2]])
                    for include_gram in [False, True]:
                        label = 'manufactured_' + mode + '_N' + str(intervals) + ('_Gram' if include_gram else '_GR')
                        row = evaluate(label, system, packed, include_gram, numerical.zeros(2), 0.0)
                        if mode == 'vacuum':
                            check(label + '_zero_source_zero_response', row['bounds']['source_dual_bound'] == 0 and row['measured']['lapse_rate_sup'] == 0)
                        report['manufactured'].append(row)
                        save()
            for include_gram in [False, True]:
                suffix = '_Gram' if include_gram else '_GR'
                chosen = [row for row in report['manufactured'] if 'oscillatory_velocity' in row['label'] and row['label'].endswith(suffix)]
                check('oscillatory_data_not_mistaken_for_uniform_energy' + suffix, chosen[-1]['bounds']['energy'] > 10 * chosen[0]['bounds']['energy'])
            for module in tuple(sys.modules.values()):
                filename = getattr(module, '__file__', None)
                if filename:
                    path = Path(filename).resolve()
                    if path.parent == root / 'scripts' and path.suffix == '.py':
                        own(path)
            check('all_inherited_inputs_unchanged', all(digest(root / name) == expected for name, expected in inputs.items()))
            check('all_inherited_and_new_outputs_unchanged', all(digest(root / name) == expected for name, expected in outputs.items()))
            check('no_bytecode_cache', not (root / 'scripts/__pycache__').exists())
            report.update(state='complete', passed=sum(row['passed'] for row in report['checks']), total=len(report['checks']), completed_utc=datetime.now(timezone.utc).isoformat())
            save()
            (destination / 'COMPLETE').write_text(report['completed_utc'] + '\n')
            print(json.dumps({name: report[name] for name in ['state', 'passed', 'total', 'completed_utc']}), flush=True)
            return
        except Exception as error:
            report.update(state='failed', failure=repr(error), traceback=traceback.format_exc(), completed_utc=datetime.now(timezone.utc).isoformat())
            save()
            raise
    report_path = destination / 'status.json'
    report = json.loads(report_path.read_text())
    if report['state'] != 'complete' or report['passed'] != report['total'] or not (destination / 'COMPLETE').exists():
        raise RuntimeError('Source/trace gate incomplete.')
    inherit(inputs, report['inputs'])
    inherit(outputs, report['outputs'])
    for path in [report_path, destination / 'COMPLETE', destination / 'executed-script.py']:
        own(path)
    note = root / 'DERIVATION-20260909-first-metric-source-and-pointwise-lapse-bound.md'
    cited = [value for value in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')) if value.endswith(('.py', '.json', '.md', '.npz'))]
    missing = [value for value in cited if root / value != final_path and not (root / value).is_file()]
    if missing:
        raise FileNotFoundError(str(missing))
    own(note)
    snapshot = intake / 'annular-metric-first-source-and-lapse-trace-resume-snapshot.md'
    with snapshot.open('xb') as handle:
        handle.write((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    artifact(snapshot)
    frozen = root.parent / 'formalization-workbench'
    since = datetime(2026, 9, 9, 20, 56, 0, tzinfo=timezone.utc).timestamp()
    touched = [str(path.relative_to(frozen)) for path in frozen.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if touched or (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Protected workbench/cache check failed: ' + repr(touched))
    final = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'checks': report['total'], 'saved_states': len(report['samples']), 'manufactured_cases': len(report['manufactured']), 'inputs': inputs, 'outputs': outputs, 'cited_local_paths_checked': cited, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-09T20:56:00Z, not full pre-turn hash baseline', 'mutable_resume_pinned_as_snapshot': True, 'no_bytecode_cache': True, 'first_source_and_pointwise_lapse_response_bound_derived': True, 'uniform_source_inputs_over_time_proved': False, 'second_effective_source_bound_derived': False, 'full_coupled_DAE_solved': False, 'valid_for_physics_claim': False}
    with final_path.open('x') as handle:
        json.dump(final, handle, indent=2)
        handle.write('\n')
    print(json.dumps({name: final[name] for name in ['state', 'checks', 'saved_states', 'manufactured_cases', 'protected_workbench_files_written_since_turn_start']}), flush=True)


if __name__ == '__main__':
    run()
