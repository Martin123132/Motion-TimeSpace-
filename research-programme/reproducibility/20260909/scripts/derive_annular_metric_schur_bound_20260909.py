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
    from annular_metric_schur_bound_20260909 import analytic_schur_bound, exact_overlap_geometry, independent_schur_components, lapse_projection_residual, measured_schur_norms, schur_blocks
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian

    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['derive', 'seal'])
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260909'
    destination = intake / 'annular-metric-Schur-bound-derived'
    final_path = intake / 'annular-metric-Schur-bound-final-integrity.json'
    prior_path = intake / 'annular-coupled-metric-bootstrap-final-integrity.json'
    prior = json.loads(prior_path.read_text())
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

    if prior['state'] != 'complete':
        raise RuntimeError('Prior gate incomplete.')
    inherit(inputs, prior['inputs'])
    inherit(outputs, prior['outputs'])
    own(prior_path)
    scripts = ['annular_metric_schur_bound_20260909.py', 'derive_annular_metric_schur_bound_20260909.py']
    for name in scripts:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    if arguments.phase == 'derive':
        destination.mkdir(exist_ok=False)
        (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())
        report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': inputs, 'outputs': outputs, 'checks': [], 'samples': [], 'manufactured': [], 'conditional_mesh_uniform_metric_inverse_derived': True, 'norm_scope': 'mass H1 seminorm with fixed inner trace lifted; lapse nodal h-weighted L2; dual covector norm. NOT a pointwise bound on lapse derivatives.', 'uniform_source_and_trace_estimates_closed': False, 'full_coupled_DAE_solved': False, 'valid_for_physics_claim': False, 'reference': {'url': 'https://jschoeberl.github.io/SciCADE-course/unit5-mixed/1_mixedmethods.html', 'title': 'J. Schoberl, Mixed Methods, sections21.1-21.2', 'accessed_date': '2026-09-09', 'role': 'General inf-sup/inverse background. Explicit grid constants, projection remainder and perturbation bound derived from local owned action, not copied as a theorem for MTS.'}}

        def save():
            (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

        def maximum(values):
            return float(numerical.max(numerical.abs(values)))

        def check(name, passed, detail=None):
            report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
            if not passed:
                raise RuntimeError('Failed check: ' + name + ' ' + repr(detail))

        geometry = exact_overlap_geometry()

        def evaluate_case(label, system, packed, include_gram):
            bounds = analytic_schur_bound(system, packed, include_gram, geometry)
            blocks = schur_blocks(system, packed, include_gram)
            basis = system.basis
            reference = bounds['sigma_center'] / system.kappa * basis.face_gradient[:, 1:].T @ (basis.quadrature_weights[:, None] * basis.node_value)
            measured = measured_schur_norms(blocks, reference)
            check(label + '_sufficient_inverse_gate', bounds['sufficient_uniform_inverse_gate'], {'beta': bounds['beta_B_bound'], 'feedback': bounds['Neumann_feedback']})
            check(label + '_B_perturbation_bound', measured['B_perturbation_norm'] <= bounds['B_perturbation_bound'] + 1e-10)
            check(label + '_B_inf_sup_bound', measured['beta_B'] >= bounds['beta_B_bound'] - 1e-10)
            check(label + '_A_bound', measured['A_norm'] <= bounds['A_bound'] + 1e-10)
            check(label + '_D_bound_and_positivity', measured['D_norm'] <= bounds['D_bound'] + 1e-10 and measured['D_minimum'] >= -1e-10)
            check(label + '_full_inverse_bound', measured['inverse_norm'] <= bounds['inverse_bound'] + 1e-10)
            check(label + '_actual_lapse_projection_error_identity', maximum(lapse_projection_residual(system, packed, blocks) - blocks['D']) < 2e-11)
            components = independent_schur_components(system, packed, blocks, include_gram)
            for name in ['A', 'B', 'D']:
                check(label + '_independent_' + name + '_components', maximum(components[name + '_reconstructed'] - blocks[name]) < 2e-11)
            check(label + '_Gram_density_uniform_envelope', maximum(system.density) <= bounds['Gram_density_bound'] + 1e-14)
            check(label + '_natural_outer_and_all_lapse_rows_kept', blocks['metric_indices'].size == 2 * system.node_count and system.face_count - 1 in blocks['metric_indices'] and set(range(system.slices[1].start, system.slices[1].stop)) <= set(blocks['metric_indices']))
            record_bounds = {name: value for name, value in bounds.items() if not isinstance(value, numerical.ndarray)}
            return blocks, bounds, measured, components, record_bounds

        save()
        try:
            check('exact_all_grid_overlap_template', geometry['template_proved'])
            report['geometry_certificate'] = {name: value for name, value in geometry.items() if name != 'overlap'}
            for name in ['row_gap', 'column_gap', 'width_max', 'beta_squared']:
                report['geometry_certificate'][name] = str(geometry[name])
            rational = symbolic.Rational
            margins = [rational(59097, 573104), rational(1825, 25284), rational(491, 7056), rational(5, 72)]
            adjacent = [rational(253, 50568), rational(3, 392), rational(1, 144)]
            check('exact_Gram_coefficient_majorants', max(margins) < rational(1, 8) and max(adjacent) < rational(1, 128) and rational(1, 392) < rational(1, 256))
            check('exact_Gram_density_constant_less_than_two', 8 * rational(1, 8) + 32 * rational(1, 128) + 16 * rational(1, 256) < 2)
            case_path = intake / 'annular-constraint-correction-initial/canonical.json'
            own(case_path)
            case = json.loads(case_path.read_text())
            constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
            kappa = float(symbolic.sympify(case['normalization_kappa']))
            for intervals in [16, 32, 64, 128]:
                basis = MixedActionBasis(numerical.linspace(5.875, 6.125, intervals + 1))
                links = MetricLinkQuadrature(basis)
                count, face_count = basis.radii.size, basis.faces.size
                for mode in ['vacuum', 'weak_field']:
                    offset = basis.radii - basis.radii[0]
                    scalar = numerical.zeros(count) if mode == 'vacuum' else .001 * numerical.sin(4 * offset)
                    scalar_r = numerical.zeros(count) if mode == 'vacuum' else .004 * numerical.cos(4 * offset)
                    slope = basis.spacing * (scalar_r - basis.derivative @ scalar)
                    system = ReleasedHermiteRouthian(basis, scalar, slope, constants, kappa, numerical.zeros(count), numerical.zeros(count), 1.0, links)
                    packed = numerical.zeros(system.count)
                    packed[system.slices[0]] = 1.0
                    packed[system.slices[1]] = numerical.sqrt(1 - 2 / basis.radii)
                    packed[system.slices[2]] = 0.0 if mode == 'vacuum' else .002 * numerical.cos(3 * offset)
                    q_r = numerical.zeros(count) if mode == 'vacuum' else -.006 * numerical.sin(3 * offset)
                    packed[system.slope_slice] = basis.spacing * (q_r - basis.derivative @ packed[system.slices[2]])
                    for include_gram in [False, True]:
                        label = 'manufactured_' + mode + '_N' + str(intervals) + ('_Gram' if include_gram else '_GR')
                        unused_blocks, bounds, measured, unused_components, record_bounds = evaluate_case(label, system, packed, include_gram)
                        if mode == 'vacuum':
                            check(label + '_vacuum_lapse_block_zero', measured['D_norm'] == 0 and bounds['D_bound'] == 0)
                        report['manufactured'].append({'label': label, 'bounds': record_bounds, 'measured': measured})
                    if intervals == 16 and mode == 'weak_field':
                        high = packed.copy()
                        high[system.slices[2]] *= 1e5
                        high[system.slope_slice] *= 1e5
                        failed_gate = analytic_schur_bound(system, high, True, geometry)
                        check('high_field_sufficient_gate_refuses_claim', failed_gate['sufficient_uniform_inverse_gate'] is False and failed_gate['inverse_bound'] is None)
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
                        include_gram = branch != 'GR'
                        old = loaded(intake / 'annular-uniform-energy-bounds-derived' / (label + '.npz'))
                        jets = loaded(intake / 'annular-metric-flux-jets-derived' / (label + '.npz'))
                        tangent = system.constraint_tangent(packed, include_gram, source['endpoint_acceleration'], source['outer_clock'][1])
                        check(label + '_same_state_speed_and_shift', maximum(packed - old['packed']) == 0 and maximum(tangent['packed_speed'] - old['packed_speed']) < 1e-12 and maximum(tangent['shift_residual'] - jets['full_shift_residual']) < 1e-12)
                        blocks, bounds, measured, components, record_bounds = evaluate_case(label, system, packed, include_gram)
                        forcing_records, saved_forces = [], {}
                        for order, derivative, known in [(1, tangent['packed_speed'], tangent['data_derivative']), (2, jets['jet_acceleration'], jets['jet_known_second_forcing'])]:
                            lift = numerical.zeros_like(packed)
                            lift[system.slices[0]] = derivative[0]
                            velocity_lift = affine_lift_matrix(basis) @ (source['endpoint_acceleration'] if order == 1 else numerical.zeros(2))
                            lift[system.slices[2]] = velocity_lift[:count]
                            lift[system.slope_slice] = velocity_lift[count:]
                            check(label + '_order' + str(order) + '_lift_preserves_all_fixed_entries', maximum((lift - derivative)[system.fixed]) < 1e-14)
                            raw_forcing = -known - blocks['jacobian'] @ lift
                            metric_forcing = raw_forcing[blocks['metric_indices']] - blocks['coupling'] @ numerical.linalg.solve(blocks['scalar_mass'], raw_forcing[blocks['velocity_indices']])
                            solution = numerical.linalg.solve(blocks['schur'], metric_forcing)
                            expected = (derivative - lift)[blocks['metric_indices']]
                            error = maximum(solution - expected)
                            check(label + '_order' + str(order) + '_unchanged_Schur_solution', error < 2e-10 * max(1.0, maximum(expected)), error)
                            norm = float(numerical.sqrt(max(0.0, expected @ blocks['metric_norm'] @ expected)))
                            dual_norm = float(numerical.sqrt(max(0.0, metric_forcing @ numerical.linalg.solve(blocks['metric_norm'], metric_forcing))))
                            estimate = bounds['inverse_bound'] * dual_norm
                            check(label + '_order' + str(order) + '_derived_inverse_estimate', norm <= estimate + 1e-10, {'norm': norm, 'bound': estimate})
                            mass_sup_bound = abs(float(derivative[0])) + numerical.sqrt(bounds['envelope']['length']) * estimate
                            check(label + '_order' + str(order) + '_mass_rate_sup_bound', maximum(derivative[system.slices[0]]) <= mass_sup_bound + 1e-10)
                            forcing_records.append({'order': order, 'metric_physical_norm': norm, 'source_dual_norm': dual_norm, 'metric_norm_bound': estimate, 'mass_rate_sup_bound': mass_sup_bound, 'Schur_reconstruction_error': error})
                            saved_forces.update({'source_order' + str(order): metric_forcing, 'lift_order' + str(order): lift})
                        result_path = destination / (label + '.npz')
                        numerical.savez_compressed(result_path, **blocks, **components, **saved_forces, q_Bernstein_controls=bounds['q_Bernstein_controls'], w_Bernstein_controls=bounds['w_Bernstein_controls'], old_physical_mismatch=jets['physical_mismatch'], old_physical_mismatch_time=jets['jet_physical_mismatch_time'], full_shift_residual=jets['full_shift_residual'])
                        artifact(result_path)
                        record = {'label': label, 'intervals': intervals, 'branch': branch, 'time': float(time), 'bounds': record_bounds, 'measured': measured, 'forcing': forcing_records, 'uniform_source_bound_proved': False, 'outward_rounded_interval_certificate': False}
                        report['samples'].append(record)
                        save()
                        if index == steps:
                            print(json.dumps({'label': label, 'beta_bound': bounds['beta_B_bound'], 'feedback_bound': bounds['Neumann_feedback'], 'inverse_measured': measured['inverse_norm'], 'inverse_bound': bounds['inverse_bound'], 'D_measured': measured['D_norm'], 'forcing': forcing_records}), flush=True)
            for module in tuple(sys.modules.values()):
                filename = getattr(module, '__file__', None)
                if filename:
                    path = Path(filename).resolve()
                    if path.parent == root / 'scripts' and path.suffix == '.py':
                        own(path)
            check('all_sources_preserved', all(digest(root / name) == expected for name, expected in inputs.items()))
            check('all_outputs_preserved', all(digest(root / name) == expected for name, expected in outputs.items()))
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
        raise RuntimeError('Metric inverse gate incomplete.')
    inherit(inputs, report['inputs'])
    inherit(outputs, report['outputs'])
    for path in [report_path, destination / 'COMPLETE', destination / 'executed-script.py']:
        own(path)
    note = root / 'DERIVATION-20260909-metric-Schur-inverse-and-projection-remainder.md'
    cited = [value for value in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')) if value.endswith(('.py', '.json', '.md', '.npz'))]
    missing = [value for value in cited if root / value != final_path and not (root / value).is_file()]
    if missing:
        raise FileNotFoundError(str(missing))
    own(note)
    snapshot = intake / 'annular-metric-Schur-bound-resume-snapshot.md'
    with snapshot.open('xb') as handle:
        handle.write((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    artifact(snapshot)
    frozen = root.parent / 'formalization-workbench'
    since = datetime(2026, 9, 9, 17, 35, 0, tzinfo=timezone.utc).timestamp()
    touched = [str(path.relative_to(frozen)) for path in frozen.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if touched or (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Protected workbench or cache check failed: ' + repr(touched))
    final = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'checks': report['total'], 'saved_canonical_states': len(report['samples']), 'manufactured_cases': len(report['manufactured']), 'compiled_scripts': scripts, 'inputs': inputs, 'outputs': outputs, 'cited_local_paths_checked': cited, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-09T17:35:00Z; not full pre-turn hash comparison', 'mutable_resume_pinned_as_snapshot': True, 'no_bytecode_cache': True, 'conditional_mesh_uniform_metric_inverse_proved_in_H1_L2_norm': True, 'uniform_forcing_and_lapse_trace_estimate_proved': False, 'full_coupled_DAE_solved': False, 'valid_for_physics_claim': False}
    with final_path.open('x') as handle:
        json.dump(final, handle, indent=2)
        handle.write('\n')
    print(json.dumps({name: final[name] for name in ['state', 'checks', 'saved_canonical_states', 'manufactured_cases', 'protected_workbench_files_written_since_turn_start']}), flush=True)


if __name__ == '__main__':
    run()
