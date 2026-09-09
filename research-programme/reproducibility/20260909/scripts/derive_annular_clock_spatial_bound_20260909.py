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
    from annular_clock_spatial_bound_20260909 import exact_gradient_geometry, row_data, spatial_bounds
    from annular_metric_flux_jets_20260909 import flux_profile
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_metric_schur_bound_20260909 import schur_blocks
    from annular_metric_source_bound_20260909 import scalar_source_data, source_bound
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian

    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['derive', 'seal'])
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260909'
    destination = intake / 'annular-clock-spatial-gradient-derived'
    final_path = intake / 'annular-clock-spatial-gradient-final-integrity.json'
    prior_path = intake / 'annular-metric-first-source-and-lapse-trace-final-integrity.json'
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
        raise RuntimeError('Previous source/trace seal incomplete.')
    inherit(inputs, prior['inputs'])
    inherit(outputs, prior['outputs'])
    own(prior_path)
    scripts = ['annular_clock_spatial_bound_20260909.py', 'derive_annular_clock_spatial_bound_20260909.py']
    for name in scripts:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    if arguments.phase == 'derive':
        destination.mkdir(exist_ok=False)
        (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())
        report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': inputs, 'outputs': outputs, 'checks': [], 'samples': [], 'manufactured': [], 'static_lapse_gradient_and_spatial_coefficient_derived': True, 'lapse_rate_and_clock_rate_spatial_L2_bound_derived': True, 'pointwise_clock_rate_spatial_gradient_bound_derived': False, 'physical_inner_shift_trace_still_input': True, 'energy_transport_reclosed_with_L2_coefficient_gradients': False, 'second_effective_source_bound_derived': False, 'solution_stays_in_box_proved': False, 'valid_for_physics_claim': False}

        def save():
            (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

        def check(name, passed, detail=None):
            report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
            if not passed:
                raise RuntimeError('Failed check: ' + name + ' ' + repr(detail))

        def maximum(values):
            return float(numerical.max(abs(values)))

        def norm(values, weights):
            return float(numerical.sqrt(max(0.0, weights @ values**2)))

        def evaluate(label, system, packed, include_gram, endpoint_acceleration, clock_rate, old=None):
            basis = system.basis
            tangent = system.constraint_tangent(packed, include_gram, endpoint_acceleration, clock_rate)
            speed = tangent['packed_speed']
            scalar = scalar_source_data(system, packed, include_gram, endpoint_acceleration)
            source_bound(system, packed, include_gram, scalar, speed[0], clock_rate, endpoint_acceleration, True)
            blocks = schur_blocks(system, packed, include_gram)
            static_full = system.evaluate(packed, include_gram, hessian=False)[1]
            time_full = blocks['jacobian'] @ speed + tangent['data_derivative']
            static = static_full[system.slices[0]]
            time = time_full[system.slices[0]]
            scalar_error = time_full[blocks['velocity_indices']]
            scalar_error_norm = numerical.sqrt(max(0.0, scalar_error @ numerical.linalg.solve(blocks['scalar_mass'], scalar_error)))
            effective_error = time_full[blocks['metric_indices']] - blocks['coupling'] @ numerical.linalg.solve(blocks['scalar_mass'], scalar_error)
            error_norm = numerical.sqrt(max(0.0, effective_error @ numerical.linalg.solve(blocks['metric_norm'], effective_error)))
            bound = spatial_bounds(system, scalar, static, time, speed[0], clock_rate, endpoint_acceleration, include_gram, error_norm, scalar_error_norm)
            data = row_data(system, packed, speed, include_gram, scalar['rho_time'])
            weights, spacing = basis.quadrature_weights, basis.spacing
            tail_static, tail_time = numerical.cumsum(static[1:][::-1])[::-1], numerical.cumsum(time[1:][::-1])[::-1]
            static_equation = data['averages'] @ (data['sigma'] * data['lapse']) + system.kappa * (data['ramp'] @ (weights * data['density']) + data['nodal_ramp'] @ data['atoms']) - system.outer_clock - system.kappa * tail_static
            time_equation = data['averages'] @ (data['sigma'] * data['lapse_time'] + data['sigma_time'] * data['lapse']) + system.kappa * (data['ramp'] @ (weights * data['density_time']) + data['nodal_ramp'] @ data['atoms_time']) - clock_rate - system.kappa * tail_time
            check(label + '_exact_static_cumulative_mass_row', maximum(static_equation) < 5e-12)
            check(label + '_exact_time_cumulative_mass_row', maximum(time_equation) < 5e-12)
            grid_gradient = numerical.diff(packed[system.slices[1]]) / spacing
            time_gradient = numerical.diff(speed[system.slices[1]]) / spacing
            unweighted = data['averages'] @ basis.node_value
            check(label + '_exact_average_derivative_commutation', maximum(numerical.diff(unweighted @ packed[system.slices[1]]) / spacing - data['gradient_matrix'] @ grid_gradient) < 5e-11)
            geometry = data['gradient_matrix']
            diagonal = numerical.diag(geometry)
            check(label + '_all_grid_gradient_diagonal_gaps', min(2 * diagonal - numerical.sum(abs(geometry), axis=1)) >= float(symbolic.Rational(report['geometry']['row_gap'])) - 1e-11 and min(2 * diagonal - numerical.sum(abs(geometry), axis=0)) >= float(symbolic.Rational(report['geometry']['column_gap'])) - 1e-11)
            check(label + '_positive_quadrature_exact_cell_centroids', maximum(data['averages'] @ basis.quadrature - (basis.faces[1:] + basis.faces[:-1]) / 2) < 1e-12 and maximum(data['averages'].sum(axis=1) - 1) < 1e-12)
            check(label + '_positive_source_hat_partition', numerical.min(data['hat']) >= -1e-13 and numerical.max(spacing * numerical.sum(data['hat'], axis=0)) <= 1 + 1e-12 and numerical.max(data['hat'] @ weights) <= 59 / 48 + 1e-12)
            check(label + '_nodal_atom_sampling_overlap', numerical.min(data['node_hat']) >= -1e-13 and numerical.max(spacing * data['node_hat'].sum(axis=1)) <= 3 + 1e-12 and numerical.max(spacing * data['node_hat'].sum(axis=0)) <= 1 + 1e-12)
            density_time = norm(data['density_time'], weights)
            atom_time = float(numerical.linalg.norm(data['atoms_time']) / numerical.sqrt(spacing))
            check(label + '_static_bulk_density_bound', maximum(data['density']) <= bound['static_mass_density_sup_bound'] + 1e-12)
            check(label + '_static_atom_density_bound', maximum(data['atoms']) / spacing <= bound['static_atom_density_sup_bound'] + 1e-12)
            check(label + '_static_lapse_spatial_sup_bound', maximum(grid_gradient) <= bound['lapse_radial_sup_bound'] + 1e-10)
            p_actual = 2 * basis.quadrature * data['lapse'] / data['sigma'] + basis.quadrature**2 * (basis.node_gradient @ packed[system.slices[1]]) / data['sigma']
            f_actual = data['sigma']**-2
            f_radial = (1 - f_actual - 2 * (basis.face_gradient @ packed[system.slices[0]])) / basis.quadrature
            p_actual += basis.quadrature**2 * data['lapse'] * data['sigma'] * f_radial / 2
            check(label + '_derived_not_measured_p_Lipschitz_input', maximum(p_actual) <= bound['p_radial_sup_bound'] + 1e-10)
            check(label + '_scalar_acceleration_from_Legendre_source', norm(data['acceleration'], weights) <= bound['scalar_acceleration_L2_bound'] + 1e-10)
            check(label + '_differentiated_bulk_density_L2', density_time <= bound['mass_density_time_L2_bound'] + 1e-10)
            check(label + '_differentiated_Gram_atom_L2', atom_time <= bound['atom_time_dual_L2_bound'] + 1e-10)
            mass_value = basis.face_value @ speed[system.slices[0]]
            mass_radial = basis.face_gradient @ speed[system.slices[0]]
            lapse_radial = basis.node_gradient @ packed[system.slices[1]]
            lambda_radial = (lapse_radial * mass_value + data['lapse'] * mass_radial) / (basis.quadrature * f_actual**1.5) - data['lapse'] * mass_value / (basis.quadrature**2 * f_actual**1.5) - 1.5 * data['lapse'] * mass_value * f_radial / (basis.quadrature * f_actual**2.5)
            check(label + '_sigma_time_N_gradient_L2', norm(lambda_radial, weights) <= bound['sigma_time_N_radial_L2_bound'] + 1e-10)
            check(label + '_lapse_time_spatial_L2_bound', numerical.linalg.norm(time_gradient) * numerical.sqrt(spacing) <= bound['lapse_time_radial_L2_bound'] + 1e-10)
            profile = flux_profile(system, packed, speed, basis.quadrature)
            paired = profile['remainder'] + profile['mismatch_derivative_term']
            check(label + '_paired_flux_identity_without_zeroing_defects', maximum(paired - (profile['theta_r'] - profile['leading_flux_term'])) < 1e-11)
            check(label + '_clock_spatial_L2_bound', norm(profile['theta_r'], weights) <= bound['theta_radial_L2_bound'] + 1e-10)
            check(label + '_paired_remainder_L2_bound', norm(paired, weights) <= bound['paired_flux_remainder_L2_bound'] + 1e-10)
            if old is not None:
                check(label + '_unchanged_speed_and_physical_shift', maximum(old['packed_speed'] - speed) == 0 and maximum(old['full_shift_residual'] - tangent['shift_residual']) == 0)
            measured = {'lapse_radial_sup': maximum(grid_gradient), 'p_radial_sup_sampled': maximum(p_actual), 'lapse_time_radial_L2': float(numerical.linalg.norm(time_gradient) * numerical.sqrt(spacing)), 'theta_radial_L2': norm(profile['theta_r'], weights), 'theta_radial_sup_sampled': maximum(profile['theta_r']), 'paired_flux_L2': norm(paired, weights), 'scalar_acceleration_L2': norm(data['acceleration'], weights), 'mass_density_time_L2': density_time, 'Gram_atom_time_L2': atom_time, 'lapse_defect_time_L2': norm(profile['lapse_defect_time'], weights), 'bulk_mismatch_derivative_L2': norm(profile['mismatch_derivative_term'], weights), 'effective_constraint_rate_residual_dual': float(error_norm), 'scalar_constraint_rate_residual_m': float(scalar_error_norm)}
            output = destination / (label + '.npz')
            saved = {'packed_speed': speed, 'full_shift_residual': tangent['shift_residual'], 'mass_static_residual': static, 'mass_time_residual': time, 'density': data['density'], 'density_time': data['density_time'], 'atoms_time': data['atoms_time'], 'theta_r': profile['theta_r'], 'paired_remainder': paired, 'lapse_defect_time': profile['lapse_defect_time'], 'bulk_mismatch_derivative': profile['mismatch_derivative_term']}
            if old is not None:
                saved.update(old_physical_mismatch=old['old_physical_mismatch'], old_physical_mismatch_time=old['old_physical_mismatch_time'])
            numerical.savez_compressed(output, **saved)
            artifact(output)
            return {'label': label, 'bounds': bound, 'measured': measured}

        save()
        try:
            report['geometry'] = exact_gradient_geometry()
            check('exact_all_grid_differentiated_overlap_and_margins', report['geometry']['proved'])
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
                        old = loaded(intake / 'annular-metric-first-source-and-lapse-trace-derived' / (label + '.npz'))
                        row = evaluate(label, system, packed, branch != 'GR', source['endpoint_acceleration'], source['outer_clock'][1], old)
                        row.update(intervals=intervals, branch=branch, time=float(time))
                        report['samples'].append(row)
                        save()
                        if index == steps:
                            print(json.dumps({'label': label, 'measured': row['measured'], 'N_R_bound': row['bounds']['lapse_radial_sup_bound'], 'p_R_bound': row['bounds']['p_radial_sup_bound'], 'theta_R_L2_bound': row['bounds']['theta_radial_L2_bound']}), flush=True)
            for intervals in [16, 64]:
                basis = MixedActionBasis(numerical.linspace(47 / 8, 49 / 8, intervals + 1))
                links = MetricLinkQuadrature(basis)
                count = basis.radii.size
                for mode in ['vacuum', 'off_shell_oscillatory_lapse']:
                    system = ReleasedHermiteRouthian(basis, numerical.zeros(count), numerical.zeros(count), constants, kappa, numerical.zeros(count), numerical.zeros(count), 1.0, links)
                    packed = numerical.zeros(system.count)
                    packed[system.slices[0]] = 1.0
                    packed[system.slices[1]] = numerical.sqrt(1 - 2 / basis.radii) if mode == 'vacuum' else .82 + .01 * (-1.)**numerical.arange(count)
                    for include_gram in [False, True]:
                        label = 'manufactured_' + mode + '_N' + str(intervals) + ('_Gram' if include_gram else '_GR')
                        row = evaluate(label, system, packed, include_gram, numerical.zeros(2), 0.0)
                        if mode != 'vacuum':
                            without_residual = row['bounds']['lapse_radial_sup_bound'] - .2 * row['bounds']['static_residual_density_sup']
                            check(label + '_off_shell_residual_cannot_be_discarded', row['measured']['lapse_radial_sup'] > without_residual)
                        report['manufactured'].append(row)
                        save()
            for module in tuple(sys.modules.values()):
                filename = getattr(module, '__file__', None)
                if filename:
                    path = Path(filename).resolve()
                    if path.parent == root / 'scripts' and path.suffix == '.py':
                        own(path)
            check('inherited_inputs_preserved', all(digest(root / name) == expected for name, expected in inputs.items()))
            check('inherited_and_new_outputs_preserved', all(digest(root / name) == expected for name, expected in outputs.items()))
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
    if report['state'] != 'complete' or report['passed'] != report['total']:
        raise RuntimeError('Spatial gradient gate incomplete.')
    inherit(inputs, report['inputs'])
    inherit(outputs, report['outputs'])
    for path in [report_path, destination / 'COMPLETE', destination / 'executed-script.py']:
        own(path)
    note = root / 'DERIVATION-20260909-clock-spatial-gradient-and-derived-coefficient-input.md'
    cited = [value for value in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')) if value.endswith(('.py', '.md', '.json', '.npz'))]
    missing = [value for value in cited if root / value != final_path and not (root / value).is_file()]
    if missing:
        raise FileNotFoundError(str(missing))
    own(note)
    snapshot = intake / 'annular-clock-spatial-gradient-resume-snapshot.md'
    with snapshot.open('xb') as handle:
        handle.write((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    artifact(snapshot)
    frozen = root.parent / 'formalization-workbench'
    since = datetime(2026, 9, 9, 21, 11, 0, tzinfo=timezone.utc).timestamp()
    touched = [str(path.relative_to(frozen)) for path in frozen.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if touched or (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Protected workbench/cache check failed: ' + repr(touched))
    final = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'checks': report['total'], 'saved_states': len(report['samples']), 'manufactured_cases': len(report['manufactured']), 'inputs': inputs, 'outputs': outputs, 'cited_local_paths_checked': cited, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-09T21:11:00Z, not full pre-turn hash baseline', 'mutable_resume_pinned_as_snapshot': True, 'no_bytecode_cache': True, 'static_spatial_coefficient_bound_derived': True, 'clock_rate_gradient_and_paired_remainder_L2_bound_derived': True, 'clock_rate_gradient_Linfinity_bound_derived': False, 'energy_transport_closed': False, 'actual_inner_shift_trace_bound_derived': False, 'valid_for_physics_claim': False}
    with final_path.open('x') as handle:
        json.dump(final, handle, indent=2)
        handle.write('\n')
    print(json.dumps({name: final[name] for name in ['state', 'checks', 'saved_states', 'manufactured_cases', 'protected_workbench_files_written_since_turn_start']}), flush=True)


if __name__ == '__main__':
    run()
