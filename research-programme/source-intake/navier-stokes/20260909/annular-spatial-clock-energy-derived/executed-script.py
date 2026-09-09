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
    from annular_action_boundary_current_20260909 import changed_system
    from annular_adm_mixed_action_20260909 import MixedActionBasis
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian
    from annular_spatial_clock_energy_20260909 import bulk_bounds, energy, profile

    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['derive', 'seal'])
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260909'
    destination = intake / 'annular-spatial-clock-energy-derived'
    final_path = intake / 'annular-spatial-clock-energy-final-integrity.json'
    prior_path = intake / 'annular-second-metric-source-final-integrity.json'
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

    prior = json.loads(prior_path.read_text())
    if prior['state'] != 'complete':
        raise RuntimeError('Previous source gate incomplete.')
    inherit(inputs, prior['inputs'])
    inherit(outputs, prior['outputs'])
    own(prior_path)
    for name in ['annular_spatial_clock_energy_20260909.py', 'derive_annular_spatial_clock_energy_20260909.py']:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    if args.phase == 'derive':
        destination.mkdir(exist_ok=False)
        (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())
        report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': inputs, 'outputs': outputs, 'checks': [], 'samples': [], 'manufactured': [], 'clock_normalized_spatial_energy_identity_derived': True, 'interior_coefficient_bounds_mesh_uniform': True, 'interfaces_and_actual_scalar_residuals_retained': True, 'theta_time_or_higher_time_jet_used': False, 'paired_interface_residual_uniform_estimate_proved': False, 'equivalence_to_previous_H_proved': False, 'spatial_energy_evolution_closed': False, 'valid_for_physics_claim': False}

        def save():
            (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

        def check(name, passed, detail=None):
            report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
            if not passed:
                raise RuntimeError('Failed check: ' + name + ' ' + repr(detail))

        def close(name, left, right, tolerance=1e-7):
            error = float(numerical.max(abs(left - right)))
            scale = 1 + float(numerical.max(abs(right)))
            check(name, error <= tolerance * scale, {'error': error, 'scale': scale})

        def sumreal(values):
            return float(numerical.sum(values).real)

        def evaluate(label, system, packed, speed, tangent, clock_rate, bounds):
            basis = system.basis
            result = energy(system, packed, speed, basis.quadrature, basis.quadrature_weights)
            close(label + '_spatially_commuted_velocity_equation', result['commuted_v_error'], numerical.zeros_like(result['commuted_v_error']))
            close(label + '_spatially_commuted_gradient_equation', result['commuted_w_error'], numerical.zeros_like(result['commuted_w_error']))
            close(label + '_exact_reconstructed_kinematics', result['r_w'], numerical.zeros_like(result['r_w']))
            decomposed = sum(result[name] for name in ['reaction_levels', 'residual_work_levels', 'outer_flux_levels', 'interface_flux_levels', 'quadrature_ibp_levels'])
            close(label + '_complete_spatial_energy_identity', decomposed, result['direct_rate_levels'])
            epsilon = 1e-25
            moved = changed_system(system, packed, tangent, 1j * epsilon, clock_rate)
            complex_result = energy(moved, packed + 1j * epsilon * speed, speed, basis.quadrature, basis.quadrature_weights)
            close(label + '_independent_complex_energy_derivative', complex_result['energy_levels'].imag / epsilon, result['direct_rate_levels'])
            close(label + '_continuous_v_and_w_not_their_derivatives', numerical.concatenate([result['interface_v_jump'][0], result['interface_w_jump'][0]]), numerical.zeros(result['interface_v_jump'].shape[1] * 2))
            for order in [1, 2, 3]:
                key = ['c_R_sup_broken', 'c_RR_sup_broken', 'c_RRR_sup_broken'][order - 1]
                check(label + '_broken_coefficient_bound_order' + str(order), max(abs(result['c'][order])) <= bounds[key] + 1e-10)
            total = sumreal(result['energy_levels'])
            bulk_upper = bounds['growth_bound'] * total + numerical.sqrt(2 * total) * bounds['known_coefficient_source_bound']
            check(label + '_derived_interior_growth_bound', sumreal(result['reaction_levels']) <= bulk_upper + 1e-9)
            residual_upper = numerical.sqrt(2 * total) * float(result['residual_norm'])
            check(label + '_actual_residual_Cauchy_bound', abs(sumreal(result['residual_work_levels'])) <= residual_upper + 1e-8)
            surface = sumreal(result['outer_flux_levels'] + result['interface_flux_levels'] + result['quadrature_ibp_levels'])
            check(label + '_conditional_full_energy_inequality', sumreal(result['direct_rate_levels']) <= surface + bulk_upper + residual_upper + 1e-8)
            knots = numerical.unique(numerical.concatenate([basis.radii, basis.faces]))
            gauss, weights = numerical.polynomial.legendre.leggauss(12)
            halves, centers = numerical.diff(knots) / 2, (knots[:-1] + knots[1:]) / 2
            points12 = (centers[:, None] + halves[:, None] * gauss).ravel()
            weights12 = (halves[:, None] * weights).ravel()
            refined = energy(system, packed, speed, points12, weights12)
            close(label + '_quadrature_refinement_energy_control', refined['energy_levels'], result['energy_levels'], tolerance=1e-5)
            check(label + '_all_diagnostic_values_finite', all(numerical.all(numerical.isfinite(value)) for value in result.values()))
            return result, {'energy_levels': result['energy_levels'].tolist(), 'total_energy': total, 'direct_rate': sumreal(result['direct_rate_levels']), 'reaction_work': sumreal(result['reaction_levels']), 'actual_residual_work': sumreal(result['residual_work_levels']), 'outer_flux': sumreal(result['outer_flux_levels']), 'interface_flux': sumreal(result['interface_flux_levels']), 'quadrature_ibp': sumreal(result['quadrature_ibp_levels']), 'paired_interface_residual_work': sumreal(result['interface_flux_levels'] + result['residual_work_levels'] + result['quadrature_ibp_levels']), 'residual_norm': float(result['residual_norm']), 'interior_rate_upper': float(bulk_upper), 'conditional_rate_upper': float(surface + bulk_upper + residual_upper), 'Q12_ibp': sumreal(refined['quadrature_ibp_levels']), 'v_derivative_jump_max': [float(max(abs(row))) for row in result['interface_v_jump']], 'w_derivative_jump_max': [float(max(abs(row))) for row in result['interface_w_jump']]}

        save()
        try:
            case_path = intake / 'annular-constraint-correction-initial/canonical.json'
            parent_path = intake / 'annular-second-metric-source-derived/status.json'
            own(case_path)
            own(parent_path)
            case = json.loads(case_path.read_text())
            constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
            kappa = float(symbolic.sympify(case['normalization_kappa']))
            parents = json.loads(parent_path.read_text())['samples']
            for parent in parents:
                label, intervals, branch = parent['label'], parent['intervals'], parent['branch']
                steps = 64 if intervals == 64 else 32
                index = int(label.rsplit('sample', 1)[1])
                tag = label.split('_sample')[0]
                report['active_job'] = label
                save()
                source = loaded(intake / 'annular-released-Hermite-initial-derived' / (tag + '.npz'))
                folder = 'annular-boundary-N64-evolution-smoke' if intervals == 64 else 'annular-released-Hermite-evolution-smoke'
                trajectory = loaded(intake / folder / (tag + '_steps' + str(steps) + '.npz'))
                basis = MixedActionBasis(source['radius'])
                count = basis.radii.size
                time, state = trajectory['time'][index], trajectory['state'][index]
                scalar, slope, momentum, slope_momentum = [state[part * count:(part + 1) * count] for part in range(4)]
                packed = state[4 * count:]
                include_gram = branch != 'GR'
                system = ReleasedHermiteRouthian(basis, scalar, slope, constants, kappa, momentum, slope_momentum, source['outer_clock'][0] + time * source['outer_clock'][1], MetricLinkQuadrature(basis))
                tangent = system.constraint_tangent(packed, include_gram, source['endpoint_acceleration'], source['outer_clock'][1])
                speed = tangent['packed_speed']
                first = parent['first_bounds']
                bounds = bulk_bounds(first['lapse_radial_sup_bound'], first['theta_sup_bound'])
                result, measured = evaluate(label, system, packed, speed, tangent, source['outer_clock'][1], bounds)
                old = loaded(intake / 'annular-metric-flux-jets-derived' / (label + '.npz'))
                close(label + '_old_scalar_defect_retained', result['r_v'][0], old['scalar_defect'])
                close(label + '_old_clock_rate_retained', result['theta'], old['theta'])
                close(label + '_old_full_shift_residual_retained', tangent['shift_residual'], old['full_shift_residual'])
                output = destination / (label + '.npz')
                numerical.savez_compressed(output, **result, packed_speed=speed, old_physical_mismatch=old['physical_mismatch'], full_shift_residual=tangent['shift_residual'])
                artifact(output)
                report['samples'].append({'label': label, 'intervals': intervals, 'branch': branch, 'time': float(time), 'bounds': bounds, 'measured': measured, 'previous_H': parent['higher_spatial_radius'], 'previous_H_equivalence_proved': False})
                save()
                if index == steps:
                    print(json.dumps({'label': label, 'energy': measured['total_energy'], 'rate': measured['direct_rate'], 'interface': measured['interface_flux'], 'residual_work': measured['actual_residual_work'], 'paired': measured['paired_interface_residual_work']}), flush=True)
            for intervals in [16, 32, 64]:
                basis = MixedActionBasis(numerical.linspace(47 / 8, 49 / 8, intervals + 1))
                count = basis.radii.size
                system = ReleasedHermiteRouthian(basis, numerical.zeros(count), numerical.zeros(count), constants, kappa, numerical.zeros(count), numerical.zeros(count), 1., MetricLinkQuadrature(basis))
                packed = numerical.zeros(system.count)
                packed[system.slices[0]], packed[system.slices[1]] = 1., .82
                speed = numerical.zeros_like(packed)
                vacuum = energy(system, packed, speed, basis.quadrature, basis.quadrature_weights)
                check('vacuum_N' + str(intervals) + '_zero_energy_forcing_and_surface', all(numerical.max(abs(vacuum[name])) == 0 for name in ['energy_levels', 'direct_rate_levels', 'r_v', 'r_w', 'outer_flux_levels', 'interface_flux_levels']))
                report['manufactured'].append({'label': 'vacuum_N' + str(intervals), 'scope': 'Zero scalar off-shell geometry control; no evolution claim.'})
                nodes = basis.radii - basis.radii[0]
                scalar = .002 * nodes**3
                slope = basis.spacing * (.006 * nodes**2 - basis.derivative @ scalar)
                system = ReleasedHermiteRouthian(basis, scalar, slope, constants, kappa, numerical.zeros(count), numerical.zeros(count), 1., MetricLinkQuadrature(basis))
                packed[system.slices[2]] = .001 * nodes**2
                packed[system.slope_slice] = basis.spacing * (.002 * nodes - basis.derivative @ packed[system.slices[2]])
                speed[system.slices[2]] = .0001 * nodes
                speed[system.slope_slice] = basis.spacing * (.0001 - basis.derivative @ speed[system.slices[2]])
                tangent = {'packed_speed': speed, 'momentum_speed': numerical.zeros(count), 'slope_momentum_speed': numerical.zeros(count)}
                result, measured = evaluate('smooth_off_shell_N' + str(intervals), system, packed, speed, tangent, 0., bulk_bounds(0., 0.))
                check('smooth_off_shell_N' + str(intervals) + '_no_artificial_interface_flux', abs(measured['interface_flux']) < 1e-10)
                check('smooth_off_shell_N' + str(intervals) + '_nonzero_boundary_flux_retained', abs(measured['outer_flux']) > 1e-9)
                report['manufactured'].append({'label': 'smooth_off_shell_N' + str(intervals), 'measured': measured, 'scope': 'Manufactured smooth polynomial fields, not constrained solutions.'})
            for module in tuple(sys.modules.values()):
                filename = getattr(module, '__file__', None)
                if filename:
                    path = Path(filename).resolve()
                    if path.parent == root / 'scripts' and path.suffix == '.py':
                        own(path)
            check('all_inherited_sources_preserved', all(digest(root / name) == expected for name, expected in inputs.items()))
            check('all_inherited_and_new_evidence_preserved', all(digest(root / name) == expected for name, expected in outputs.items()))
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
        raise RuntimeError('Spatial energy validation incomplete.')
    inherit(inputs, report['inputs'])
    inherit(outputs, report['outputs'])
    for path in [report_path, destination / 'COMPLETE', destination / 'executed-script.py']:
        own(path)
    note = root / 'DERIVATION-20260909-spatial-clock-energy-with-retained-interfaces.md'
    cited = [value for value in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')) if value.endswith(('.py', '.md', '.json', '.npz'))]
    missing = [value for value in cited if root / value != final_path and not (root / value).is_file()]
    if missing:
        raise FileNotFoundError(str(missing))
    own(note)
    snapshot = intake / 'annular-spatial-clock-energy-resume-snapshot.md'
    with snapshot.open('xb') as handle:
        handle.write((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    artifact(snapshot)
    frozen = root.parent / 'formalization-workbench'
    since = datetime(2026, 9, 9, 22, 14, 0, tzinfo=timezone.utc).timestamp()
    touched = [str(path.relative_to(frozen)) for path in frozen.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if touched or (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Protected workbench/cache check failed: ' + repr(touched))
    final = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'checks': report['total'], 'saved_states': len(report['samples']), 'manufactured_cases': len(report['manufactured']), 'inputs': inputs, 'outputs': outputs, 'cited_local_paths_checked': cited, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-09T22:14:00Z, not full pre-turn hash baseline', 'no_bytecode_cache': True, 'spatial_energy_identity_and_interior_bound_derived': True, 'paired_interface_residual_estimate_and_H_equivalence_open': True, 'spatial_energy_evolution_closed': False, 'valid_for_physics_claim': False}
    with final_path.open('x') as handle:
        json.dump(final, handle, indent=2)
        handle.write('\n')
    print(json.dumps({name: final[name] for name in ['state', 'checks', 'saved_states', 'manufactured_cases', 'protected_workbench_files_written_since_turn_start']}), flush=True)


if __name__ == '__main__':
    run()
