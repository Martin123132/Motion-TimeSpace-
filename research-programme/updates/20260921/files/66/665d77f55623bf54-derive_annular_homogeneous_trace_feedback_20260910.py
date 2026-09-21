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
    from scipy.linalg import eigvalsh, solve
    from annular_adm_mixed_action_20260909 import MixedActionBasis
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian
    from annular_homogeneous_trace_feedback_20260910 import trace_feedback, released_slope_moments, gradient_trace_map, normal_form, normal_form_bounds
    from annular_paired_variational_energy_20260910 import scalar_maps, symmetric
    from annular_spatial_clock_energy_20260909 import profile

    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['derive', 'seal'])
    parser.add_argument('--attempt', default='derived')
    arguments = parser.parse_args()
    if not re.fullmatch('[a-z0-9-]+', arguments.attempt):
        raise ValueError('Attempt must be an alphanumeric identifier.')
    root = Path(__file__).resolve().parents[1]
    old = root / 'source-intake/navier-stokes/20260909'
    intake = root / 'source-intake/navier-stokes/20260910'
    destination = intake / ('annular-homogeneous-trace-feedback-' + arguments.attempt)
    prior_path = intake / 'annular-endpoint-commutator-bound-final-integrity.json'
    final_path = intake / 'annular-homogeneous-trace-feedback-final-integrity.json'
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
        raise RuntimeError('Previous checkpoint is incomplete.')
    inherit(inputs, prior['inputs'])
    inherit(outputs, prior['outputs'])
    own(prior_path)
    for name in ['annular_homogeneous_trace_feedback_20260910.py', 'derive_annular_homogeneous_trace_feedback_20260910.py', 'explore_annular_trace_feedback_20260910.py']:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    if arguments.phase == 'derive':
        destination.mkdir(exist_ok=False)
        (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())
        report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': inputs, 'outputs': outputs, 'checks': [], 'samples': [], 'controls': [], 'released_slope_moment_identity_derived': True, 'gradient_trace_normal_form_derived': True, 'conditional_gradient_feedback_bound_derived': True, 'regular_transport_uniform_propagation_proved': False, 'external_boundary_source_removed': False, 'new_physical_evolution': False, 'valid_for_physics_claim': False}

        def save():
            (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

        def check(name, passed, detail=None):
            report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
            if not passed:
                raise RuntimeError('Failed check: ' + name + ' ' + repr(detail))

        def close(name, first, second, tolerance=2e-9):
            error = float(numerical.max(abs(numerical.asarray(first) - second)))
            scale = 1 + float(numerical.max(abs(numerical.asarray(second))))
            check(name, error <= tolerance * scale, {'error': error, 'scale': scale})

        def trace_norm(mapping, metric):
            return float(numerical.sqrt(max(float(eigvalsh(symmetric(mapping @ solve(metric, mapping.T, assume_a='sym')))[-1]), 0.)))

        def matrix_norm(mapping, domain, target):
            return float(numerical.sqrt(max(float(eigvalsh(symmetric(mapping.T @ target @ mapping), domain)[-1]), 0.)))

        def evaluate(label, system, packed, speed, second, include_gram, graph=None, velocity=None, force=None, residual=None):
            result = trace_feedback(system, packed, speed, include_gram)
            normal = normal_form(system, packed, speed, second, result)
            bounds = normal_form_bounds(system, packed, speed, include_gram, normal)
            moments = released_slope_moments(system, packed, speed, result)
            mass, stiffness, operators = result['mass'], result['stiffness'], result['operators']
            count = mass.shape[0]
            free = result['free']
            selection = numerical.ix_(free, free)
            close(label + '_exact_bulk_Gram_quadrature_reconstruction', result['reconstructed'], operators['configuration_transport'])
            close(label + '_actual_free_slope_equations', result['slope_balance'], 0.)
            close(label + '_Gram_has_no_endpoint_slope_force', result['matrices']['K_Gram'][free[result['slope_rows']]], 0.)
            for side, moment in enumerate(moments):
                close(label + '_slope_moment_curvature_side' + str(side), moment['predicted_second'], moment['direct_second'])
                check(label + '_slope_moment_denominator_side' + str(side), moment['coefficient_second'] < 0., moment['coefficient_second'])
            close(label + '_raw_trace_retains_static_compatibility_part', result['trace'], result['endpoint']['theta'][:, None] * result['endpoint']['static'] + normal['trace'])
            step = 1e-25
            changed = gradient_trace_map(system, packed + 1j * step * speed, speed + 1j * step * second, include_gram)
            close(label + '_trace_derivative_by_independent_complex_step', changed.imag / step, normal['trace_time'], tolerance=1e-8)
            close(label + '_material_trace_cancellation', normal['trace_time'] + normal['trace'] @ operators['configuration_transport'], normal['source'])
            changed_clock = profile(system, packed + 1j * step * speed, speed + 1j * step * second, system.basis.radii[[0, -1]])
            close(label + '_parent_clock_mixed_derivative', changed_clock['theta'][1].imag / step, normal['theta_time_r'], tolerance=1e-8)
            measured_trace = trace_norm(normal['trace'], mass)
            measured_source = trace_norm(normal['source'], mass)
            check(label + '_derived_feedback_M_bound', measured_trace <= bounds['trace_M_to_R2_upper'] + 1e-12)
            check(label + '_derived_feedback_rate_M_bound', measured_source <= bounds['source_M_to_R2_upper'] + 1e-12)
            check(label + '_derived_feedback_K_bound', result['gradient_trace_K_to_R2'] <= bounds['poincare_M_over_K'] * bounds['trace_M_to_R2_upper'] + 1e-12)
            lift, trace = result['endpoint_lift'], normal['trace']
            lift_trace = lift @ trace
            shear_norm = matrix_norm(lift_trace, stiffness, mass)
            check(label + '_derived_shear_norm', shear_norm <= bounds['shear_K_to_M_upper'] + 1e-12)
            identity, zero = numerical.eye(count), numerical.zeros_like(mass)
            transform = numerical.block([[identity, zero], [lift_trace, identity]])
            inverse = numerical.block([[identity, zero], [-lift_trace, identity]])
            transform_time = numerical.block([[zero, zero], [normal['lift_time'] @ trace + lift @ normal['trace_time'], zero]])
            original = numerical.block([[operators['configuration_transport'], identity], [-operators['L'], operators['velocity_transport']]])
            expected = numerical.block([[result['gradient_regular'], identity], [-operators['L'] + normal['coupling'], normal['velocity_transport']]])
            close(label + '_invertible_shear_no_small_gain_assumption', transform @ inverse, numerical.eye(2 * count))
            close(label + '_full_time_dependent_normal_form', (transform_time + transform @ original) @ inverse, expected, tolerance=1e-8)
            metric_time = numerical.block([[result['matrices']['K_dot'][selection], zero], [zero, result['matrices']['M_dot'][selection]]])
            close(label + '_normal_energy_retains_every_cross_term', .5 * metric_time + symmetric(normal['metric'] @ expected), normal['work'], tolerance=1e-8)
            check(label + '_normal_growth_conditional_bound', normal['growth'] <= result['gradient_regular_growth'] + bounds['added_growth_over_regular_upper'] + 1e-9)
            if graph is None:
                coordinate = numerical.linspace(0., 1., count)
                graph, velocity = numerical.sin(3. * coordinate), numerical.cos(5. * coordinate)
                force, residual = numerical.cos(2. * coordinate), numerical.sin(7. * coordinate)
            original_vector = numerical.concatenate([graph, velocity])
            normal_vector = transform @ original_vector
            transformed_force = numerical.concatenate([force, residual + lift_trace @ force])
            close(label + '_original_force_not_discarded', transformed_force, transform @ numerical.concatenate([force, residual]))
            old_energy = .5 * original_vector @ normal['metric'] @ original_vector
            new_energy = .5 * normal_vector @ normal['metric'] @ normal_vector
            factor = 1 + shear_norm
            check(label + '_both_energy_norm_comparisons', numerical.sqrt(new_energy) <= factor * numerical.sqrt(old_energy) + 1e-9 and numerical.sqrt(old_energy) <= factor * numerical.sqrt(new_energy) + 1e-9)
            pullback = transform.T @ normal['metric'] @ transform
            pullback_time = transform_time.T @ normal['metric'] @ transform + transform.T @ metric_time @ transform + transform.T @ normal['metric'] @ transform_time
            direct_rate = original_vector @ pullback @ (original @ original_vector + numerical.concatenate([force, residual])) + .5 * original_vector @ pullback_time @ original_vector
            derived_rate = normal_vector @ normal['work'] @ normal_vector + normal_vector @ normal['metric'] @ transformed_force
            close(label + '_actual_source_and_energy_rate_identity', direct_rate, derived_rate, tolerance=1e-8)
            source_norm = numerical.sqrt(transformed_force @ normal['metric'] @ transformed_force)
            check(label + '_full_forced_energy_inequality', derived_rate <= normal['growth'] * new_energy + numerical.sqrt(2 * new_energy) * source_norm + 1e-8 * (1 + abs(direct_rate)))
            output = destination / (label + '.npz')
            numerical.savez_compressed(output, raw_trace=result['trace'], gradient_trace=trace, static_compatibility_trace=result['endpoint']['static'], trace_time=normal['trace_time'], material_trace_source=normal['source'], endpoint_slope_moment_coefficients=numerical.array([[row['coefficient_first'], row['coefficient_second'], row['coefficient_third']] for row in moments]), slope_moment_second=numerical.stack([row['predicted_second'] for row in moments]), direct_endpoint_second=numerical.stack([row['direct_second'] for row in moments]), regular_transport=result['gradient_regular'], consistency_remainder=operators['C'] + operators['A'] - result['projection'] @ result['volume']['gradient'], Gram=result['gram'], quadrature=result['quadrature'], endpoint_defect=normal['endpoint_defect'], coupling=normal['coupling'], original_vector=original_vector, transformed_vector=normal_vector, transformed_force=transformed_force, coefficient=normal['coefficient'], coefficient_time=normal['coefficient_time'])
            artifact(output)
            row = {'label': label, 'old_growth': operators['growth_rate'], 'raw_trace_removed_growth': result['regular_growth'], 'gradient_regular_growth': result['gradient_regular_growth'], 'normal_growth': normal['growth'], 'gradient_trace_M_norm': measured_trace, 'gradient_trace_K_norm': result['gradient_trace_K_to_R2'], 'material_trace_source_M_norm': measured_source, 'shear_K_to_M_norm': shear_norm, 'raw_trace_K_norm': result['feedback_K_to_R2'], 'bounds': bounds, 'old_energy': float(old_energy), 'normal_energy': float(new_energy), 'normal_energy_rate': float(derived_rate), 'normal_source_norm': float(source_norm), 'clock_mixed_trace': normal['theta_time_r'].tolist(), 'valid_for_physics_claim': False}
            return row, result, normal

        save()
        try:
            coordinate = symbolic.Symbol('coordinate', real=True)
            shape = coordinate * (1 - coordinate)**2
            moments = [symbolic.integrate(symbolic.diff(shape, coordinate) * coordinate**degree, (coordinate, 0, 1)) for degree in range(3)]
            check('constant_coefficient_slope_moments_exact', moments == [0, -symbolic.Rational(1, 12), -symbolic.Rational(1, 15)], list(map(str, moments)))
            check('endpoint_curvature_law_keeps_third_derivative', moments[2] / (2 * moments[1]) == symbolic.Rational(2, 5))
            report['slope_moment_certificate'] = {'moments': list(map(str, moments)), 'constant_p_law': 'u_RR(endpoint)+(2*direction*h/5)u_RRR=-12 Q(m*g*v)/(p*h^2)', 'scope': 'Exact polynomial reference identity. Variable-coefficient tests use actual quadrature moments, not this constant-p simplification.'}
            case_path = old / 'annular-constraint-correction-initial/canonical.json'
            source_report = intake / 'annular-endpoint-commutator-bound-derived/status.json'
            own(case_path)
            own(source_report)
            case = json.loads(case_path.read_text())
            constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
            kappa = float(symbolic.sympify(case['normalization_kappa']))
            for sample in json.loads(source_report.read_text())['samples']:
                label, intervals, branch = sample['label'], sample['intervals'], sample['branch']
                tag = label.split('_sample')[0]
                index = int(label.rsplit('sample', 1)[1])
                steps = 64 if intervals == 64 else 32
                source = loaded(old / 'annular-released-Hermite-initial-derived' / (tag + '.npz'))
                spatial = loaded(old / 'annular-spatial-clock-energy-derived' / (label + '.npz'))
                jets = loaded(old / 'annular-metric-flux-jets-derived' / (label + '.npz'))
                pair = loaded(intake / 'annular-paired-variational-energy-derived-attempt03' / (label + '.npz'))
                folder = 'annular-boundary-N64-evolution-smoke' if intervals == 64 else 'annular-released-Hermite-evolution-smoke'
                trajectory = loaded(old / folder / (tag + '_steps' + str(steps) + '.npz'))
                basis = MixedActionBasis(source['radius'])
                count = basis.radii.size
                time, state = trajectory['time'][index], trajectory['state'][index]
                scalar, slope, momentum, slope_momentum = [state[part * count:(part + 1) * count] for part in range(4)]
                packed, speed, second = state[4 * count:], spatial['packed_speed'], jets['jet_acceleration']
                system = ReleasedHermiteRouthian(basis, scalar, slope, constants, kappa, momentum, slope_momentum, source['outer_clock'][0] + time * source['outer_clock'][1], MetricLinkQuadrature(basis))
                row, result, normal = evaluate(label, system, packed, speed, second, branch != 'GR', pair['graph'], pair['graph_velocity'], pair['source_configuration'], pair['source_velocity'])
                close(label + '_prior_growth_unchanged', row['old_growth'], sample['paired_growth_measured'])
                close(label + '_prior_endpoint_defect_unchanged', trace_norm(normal['endpoint_defect'].T @ result['mass'], result['mass']), sample['measured_endpoint_defect'])
                row.update(intervals=intervals, branch=branch, time=float(time), scope='Original saved constrained state and second metric jet; no new evolution.')
                report['samples'].append(row)
                if index == steps:
                    print(json.dumps(row), flush=True)
                save()
            for intervals in [16, 32, 64, 128]:
                basis = MixedActionBasis(numerical.linspace(47 / 8, 49 / 8, intervals + 1))
                count = basis.radii.size
                system = ReleasedHermiteRouthian(basis, numerical.zeros(count), numerical.zeros(count), constants, kappa, numerical.zeros(count), numerical.zeros(count), 1., MetricLinkQuadrature(basis))
                packed = numerical.zeros(system.count)
                packed[system.slices[0]], packed[system.slices[1]] = 1., .82
                for branch in ['GR', 'metric_Gram']:
                    for kind in ['constant', 'linear', 'quadratic']:
                        centered = basis.radii - 6.
                        theta = .001 * (numerical.ones(count) if kind == 'constant' else centered if kind == 'linear' else centered**2)
                        speed = numerical.zeros_like(packed)
                        speed[system.slices[1]] = .82 * theta
                        label = 'control_N' + str(intervals) + '_' + branch + '_' + kind
                        row, result, normal = evaluate(label, system, packed, speed, numerical.zeros_like(packed), branch != 'GR')
                        if kind == 'constant':
                            close(label + '_constant_clock_needs_no_gradient_shear', normal['trace'], 0.)
                            close(label + '_constant_clock_exact_C', result['operators']['C'], .001 * numerical.eye(result['mass'].shape[0]))
                            close(label + '_constant_clock_exact_growth', normal['growth'], .005)
                            check(label + '_nonzero_raw_trace_is_not_a_physical_clock_gradient', result['feedback_K_to_R2'] > 1e-7)
                        row.update(intervals=intervals, branch=branch, kind=kind, scope='Off-shell manufactured coefficient jet in original FE spaces, second packed time jet zero; not a constrained physical trajectory.')
                        report['controls'].append(row)
                        if kind == 'linear':
                            print(json.dumps({'control': label, 'old_growth': row['old_growth'], 'normal_growth': row['normal_growth'], 'shear_norm': row['shear_K_to_M_norm']}), flush=True)
                        save()
            for module in tuple(sys.modules.values()):
                filename = getattr(module, '__file__', None)
                if filename:
                    path = Path(filename).resolve()
                    if path.parent == root / 'scripts' and path.suffix == '.py':
                        own(path)
            check('all_inherited_inputs_preserved', all(digest(root / name) == expected for name, expected in inputs.items()))
            check('all_inherited_and_new_outputs_preserved', all(digest(root / name) == expected for name, expected in outputs.items()))
            check('no_bytecode_cache', not (root / 'scripts/__pycache__').exists())
            report.update(state='complete', passed=sum(row['passed'] for row in report['checks']), total=len(report['checks']), completed_utc=datetime.now(timezone.utc).isoformat())
            save()
            (destination / 'COMPLETE').write_text(report['completed_utc'] + '\n')
            print(json.dumps({name: report[name] for name in ['state', 'passed', 'total', 'completed_utc']}), flush=True)
            return
        except Exception as error:
            report.update(state='failed', failure=repr(error), traceback=traceback.format_exc())
            save()
            raise
    report_path = destination / 'status.json'
    report = json.loads(report_path.read_text())
    if report['state'] != 'complete' or report['passed'] != report['total']:
        raise RuntimeError('Normal-form validation incomplete.')
    inherit(inputs, report['inputs'])
    inherit(outputs, report['outputs'])
    for path in [report_path, destination / 'COMPLETE', destination / 'executed-script.py']:
        own(path)
    note = root / 'DERIVATION-20260910-released-slope-feedback-and-boundary-normal-form.md'
    cited = [value for value in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')) if value.endswith(('.py', '.md', '.json', '.npz'))]
    missing = [value for value in cited if root / value != final_path and not (root / value).is_file()]
    if missing:
        raise FileNotFoundError(str(missing))
    own(note)
    snapshot = intake / 'annular-homogeneous-trace-feedback-resume-snapshot.md'
    with snapshot.open('xb') as handle:
        handle.write((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    artifact(snapshot)
    frozen = root.parent / 'formalization-workbench'
    since = datetime(2026, 9, 10, 0, 59, 0, tzinfo=timezone.utc).timestamp()
    touched = [str(path.relative_to(frozen)) for path in frozen.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if touched or (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Protected workbench/cache check failed: ' + repr(touched))
    final = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'checks': report['total'], 'saved_states': len(report['samples']), 'controls': len(report['controls']), 'inputs': inputs, 'outputs': outputs, 'cited_local_paths_checked': cited, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-10T00:59:00Z, not a full pre-turn hash baseline', 'no_bytecode_cache': True, 'released_slope_law_and_gradient_feedback_normal_form_derived': True, 'regular_transport_growth_and_parent_propagation_open': True, 'external_source_and_full_evolution_open': True, 'valid_for_physics_claim': False}
    with final_path.open('x') as handle:
        json.dump(final, handle, indent=2)
        handle.write('\n')
    print(json.dumps({name: final[name] for name in ['state', 'checks', 'saved_states', 'controls', 'protected_workbench_files_written_since_turn_start']}), flush=True)


if __name__ == '__main__':
    run()
