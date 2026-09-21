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
    from annular_homogeneous_trace_feedback_20260910 import trace_feedback, normal_form, normal_form_bounds
    from annular_regular_transport_bound_20260910 import weak_commutator_parts, regular_transport_bounds
    from annular_endpoint_commutator_bound_20260910 import clock_curvature
    from annular_paired_variational_energy_20260910 import scalar_maps, symmetric
    from annular_spatial_clock_energy_20260909 import profile
    from annular_uniform_energy_bounds_20260909 import exact_certificates, metric_envelope
    from annular_gram_joint_action_20260909 import gram_matrices

    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['derive', 'seal'])
    parser.add_argument('--attempt', default='derived')
    arguments = parser.parse_args()
    if not re.fullmatch('[a-z0-9-]+', arguments.attempt):
        raise ValueError('Invalid attempt identifier.')
    root = Path(__file__).resolve().parents[1]
    old = root / 'source-intake/navier-stokes/20260909'
    intake = root / 'source-intake/navier-stokes/20260910'
    destination = intake / ('annular-regular-transport-bound-' + arguments.attempt)
    prior_path = intake / 'annular-homogeneous-trace-feedback-final-integrity.json'
    final_path = intake / 'annular-regular-transport-bound-final-integrity.json'
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
        raise RuntimeError('Previous gate incomplete.')
    inherit(inputs, prior['inputs'])
    inherit(outputs, prior['outputs'])
    own(prior_path)
    failed_attempt = intake / 'annular-regular-transport-bound-derived'
    if arguments.attempt != 'derived' and (failed_attempt / 'FAILED-NOTE.md').exists():
        for path in failed_attempt.iterdir():
            if path.is_file():
                own(path)
    for name in ['annular_regular_transport_bound_20260910.py', 'derive_annular_regular_transport_bound_20260910.py']:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    if arguments.phase == 'derive':
        destination.mkdir(exist_ok=False)
        (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())
        report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': inputs, 'outputs': outputs, 'checks': [], 'samples': [], 'controls': [], 'projection_controls': [], 'conditional_regular_transport_bound_derived': True, 'weak_commutator_M_bound_proportional_to_mesh_derived': True, 'value_jumps_and_Gram_retained': True, 'conditional_normal_form_homogeneous_bound_derived': True, 'parent_bounds_propagated_in_time': False, 'external_source_closed': False, 'new_physical_evolution': False, 'valid_for_physics_claim': False}

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

        def norm(mapping, domain, target):
            return float(numerical.sqrt(max(float(eigvalsh(symmetric(mapping.T @ target @ mapping), domain)[-1]), 0.)))

        def evaluate(label, system, packed, speed, second, include_gram):
            result = trace_feedback(system, packed, speed, include_gram)
            parts = weak_commutator_parts(system, packed, speed, result)
            bounds = regular_transport_bounds(system, packed, speed, include_gram, result)
            normal = normal_form(system, packed, speed, second, result)
            feedback = normal_form_bounds(system, packed, speed, include_gram, normal)
            basis, mass, stiffness = system.basis, result['mass'], result['stiffness']
            free, operators, potential = result['free'], result['operators'], result['potential']
            center = bounds['theta_center']
            identity = numerical.eye(free.size)
            close(label + '_exact_weak_commutator_reconstruction', parts['direct'], parts['reconstructed'])
            close(label + '_full_D0_decomposition', -2 * operators['A'] + parts['zero_trace_volume'] + parts['direct'], result['gradient_regular'])
            quadrature_metric = numerical.diag(basis.quadrature_weights)
            value = result['volume']['maps'][0]
            scalar_l2 = value.T @ quadrature_metric @ value
            check(label + '_product_error_three_h_Lipschitz', norm(parts['value_error'], scalar_l2, quadrature_metric) <= 3 * basis.spacing * bounds['theta_lipschitz'] + 1e-10)
            check(label + '_product_derivative_error_thirty_Lipschitz', norm(parts['derivative_error'], scalar_l2, quadrature_metric) <= 30 * bounds['theta_lipschitz'] + 1e-9)
            measured_mass = norm(parts['direct'], mass, mass)
            measured_energy = norm(parts['direct'], mass, stiffness)
            check(label + '_commutator_mass_norm_has_explicit_h', measured_mass <= basis.spacing * bounds['commutator_M_norm_over_h_upper'] + 1e-10)
            check(label + '_commutator_energy_norm_no_inverse_h', measured_energy <= bounds['commutator_M_to_K_upper'] + 1e-9)
            gram_operator = solve(mass, parts['gram'], assume_a='sym')
            envelope = metric_envelope(basis, packed[system.slices[0]], packed[system.slices[1]], speed[system.slices[0]], speed[system.slices[1]])
            check(label + '_retained_Gram_commutator_bound', norm(gram_operator, mass, mass) <= basis.spacing * bounds['commutator_Gram_bilinear_over_h_upper'] / numerical.sqrt(envelope['m_min']) + 1e-10)
            data = profile(system, packed, speed, basis.quadrature)
            maps = result['volume']['maps']
            characteristic, first_c = data['c'][:2]
            theta_first, theta_second = data['theta'][1:3]
            gradient_derivative = -((2 * characteristic * first_c * theta_first + characteristic**2 * theta_second)[:, None] * maps[1] + (characteristic**2 * theta_first)[:, None] * maps[2]) @ potential
            lift_derivative = numerical.broadcast_to((result['endpoint']['gradient'][1] - result['endpoint']['gradient'][0]) / envelope['length'], gradient_derivative.shape)
            derivative = gradient_derivative - lift_derivative
            curvature = clock_curvature(system, packed, speed)
            knots = curvature['knots'][1:-1]
            interior = profile(system, packed, speed, knots)
            jump = -(interior['c'][0]**2 * curvature['theta_jump'])[:, None] * (scalar_maps(basis, knots)[1][:, free] @ potential)
            jump_norm = norm(jump / numerical.sqrt(basis.spacing), mass, numerical.eye(knots.size))
            check(label + '_actual_gradient_value_jump_bound', jump_norm <= bounds['gradient_value_jump_M_upper'] + 1e-10)
            check(label + '_actual_zero_trace_derivative_bound', norm(derivative, mass, quadrature_metric) <= bounds['gradient_broken_derivative_M_upper'] + bounds['gradient_lift_derivative_M_upper'] + 1e-9)
            projected_norm = norm(parts['zero_trace_volume'], mass, stiffness)
            check(label + '_projection_bound_retains_value_jumps', projected_norm <= bounds['zero_trace_M_to_K_upper'] + 1e-9)
            configuration_norm = norm(result['gradient_regular'] - 2 * center * identity, stiffness, stiffness)
            velocity_norm = norm(operators['velocity_transport'] - 3 * center * identity, mass, mass)
            check(label + '_derived_centered_configuration_transport_bound', configuration_norm <= bounds['configuration_centered_K_norm_upper'] + 1e-8)
            check(label + '_derived_centered_velocity_transport_bound', velocity_norm <= bounds['velocity_centered_M_norm_upper'] + 1e-8)
            check(label + '_derived_full_regular_growth_bound', result['gradient_regular_growth'] <= bounds['regular_growth_upper'] + 1e-9)
            normal_upper = bounds['regular_growth_upper'] + feedback['added_growth_over_regular_upper']
            check(label + '_derived_full_normal_growth_bound', normal['growth'] <= normal_upper + 1e-9)
            output = destination / (label + '.npz')
            numerical.savez_compressed(output, commutator_direct=parts['direct'], commutator_reconstructed=parts['reconstructed'], weak_bulk=parts['bulk'], weak_load=parts['load'], weak_Gram=parts['gram'], product_error=parts['value_error'], product_derivative_error=parts['derivative_error'], zero_trace_volume=parts['zero_trace_volume'], zero_trace_derivative=derivative, gradient_value_jumps=jump, regular_transport=result['gradient_regular'])
            artifact(output)
            row = {'label': label, 'bounds': bounds, 'measured_commutator_M_norm': measured_mass, 'measured_commutator_M_norm_over_h': measured_mass / basis.spacing, 'measured_commutator_M_to_K_norm': measured_energy, 'measured_zero_trace_M_to_K_norm': projected_norm, 'measured_gradient_value_jump_M_norm': jump_norm, 'measured_centered_D0_K_norm': configuration_norm, 'measured_centered_Dh_M_norm': velocity_norm, 'measured_regular_growth': result['gradient_regular_growth'], 'measured_normal_growth': normal['growth'], 'derived_normal_growth_upper': normal_upper, 'valid_for_physics_claim': False}
            return row, result

        def projection_controls(basis, result, envelope):
            length, spacing = envelope['length'], basis.spacing
            count, intervals = basis.radii.size, basis.radii.size - 1
            offset = basis.radii - basis.radii[0]
            points = basis.quadrature - basis.radii[0]
            value = result['volume']['maps'][0]
            for kind in ['smooth', 'node_step', 'face_step', 'scaled_saw']:
                cut = offset[intervals // 2] if kind != 'face_step' else basis.faces[count // 2] - basis.radii[0]
                if kind == 'smooth':
                    target, derivative = points * (length - points), length - 2 * points
                    nodal = offset * (length - offset)
                    jump_radius = 0.
                elif kind == 'scaled_saw':
                    target = spacing * numerical.minimum(numerical.floor(points / spacing), intervals - 1) - spacing * (intervals - 1) * points / length
                    derivative = numerical.full_like(points, -spacing * (intervals - 1) / length)
                    indices = numerical.arange(count)
                    nodal = .5 * spacing * (numerical.clip(indices - 1, 0, intervals - 1) + numerical.clip(indices, 0, intervals - 1)) - spacing * (intervals - 1) * offset / length
                    jump_radius = numerical.sqrt((intervals - 1) * spacing)
                else:
                    target = (points > cut).astype(float) - points / length
                    derivative = numerical.full_like(points, -1 / length)
                    nodal = .5 * ((offset > cut).astype(float) + (offset >= cut).astype(float)) - offset / length
                    jump_radius = 1 / numerical.sqrt(spacing)
                interpolant = numerical.concatenate([nodal, -spacing * (basis.derivative @ nodal)])
                interpolant_free = interpolant[result['free']]
                weighted_norm = lambda vector: float(numerical.sqrt(numerical.dot(basis.quadrature_weights, vector**2)))
                radius = weighted_norm(derivative) + numerical.sqrt(6) * jump_radius
                projection = result['projection'] @ target
                derivative_map = result['volume']['maps'][1]
                label = 'projection_N' + str(intervals) + '_' + ('Gram' if numerical.any(result['matrices']['K_Gram']) else 'GR') + '_' + kind
                close(label + '_zero_endpoints', nodal[[0, -1]], 0.)
                check(label + '_interpolation_error_with_actual_value_jumps', weighted_norm(target - value @ interpolant_free) <= 2 * spacing * radius + 1e-12)
                check(label + '_auxiliary_interpolant_derivative_bound', weighted_norm(derivative_map @ interpolant_free) <= 2 * radius + 1e-10)
                upper = (2 + 32 * numerical.sqrt(envelope['m_max'] / envelope['m_min'])) * radius
                measured = weighted_norm(derivative_map @ projection)
                check(label + '_projection_derivative_bound_with_value_jumps', measured <= upper + 1e-10)
                report['projection_controls'].append({'label': label, 'radius': float(radius), 'jump_radius': float(jump_radius), 'projected_derivative': measured, 'upper': float(upper), 'scope': 'Manufactured discontinuous function, no alteration of physical fields.'})

        save()
        try:
            certificates = exact_certificates()
            report['inherited_polynomial_and_Gram_certificates'] = {name: dict(values, positive=bool(values['positive'])) for name, values in certificates.items()}
            for name in ['inverse_16', 'right_2', 'right_gradient_13', 'all_Gram_row_types']:
                check('exact_' + name, certificates[name]['positive'])
            coordinate = symbolic.Symbol('coordinate', real=True)
            for degree in range(4):
                polynomial = symbolic.legendre(degree, coordinate)
                critical = symbolic.solve(symbolic.diff(polynomial, coordinate), coordinate) if degree else []
                tested = [-1, 1] + [value for value in critical if value.is_real and -1 <= value <= 1]
                check('Legendre_sup_for_cubic_evaluation_' + str(degree), all(abs(polynomial.subs(coordinate, value)) <= 1 for value in tested))
            check('Gram_commutator_constant_rounding', 80 * symbolic.sqrt(symbolic.Rational(2, 3)) <= 128)
            case_path = old / 'annular-constraint-correction-initial/canonical.json'
            parent_path = intake / 'annular-homogeneous-trace-feedback-derived/status.json'
            own(case_path)
            own(parent_path)
            case = json.loads(case_path.read_text())
            constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
            kappa = float(symbolic.sympify(case['normalization_kappa']))
            for sample in json.loads(parent_path.read_text())['samples']:
                label, intervals, branch = sample['label'], sample['intervals'], sample['branch']
                tag, index = label.split('_sample')[0], int(label.rsplit('sample', 1)[1])
                steps = 64 if intervals == 64 else 32
                source = loaded(old / 'annular-released-Hermite-initial-derived' / (tag + '.npz'))
                spatial = loaded(old / 'annular-spatial-clock-energy-derived' / (label + '.npz'))
                jets = loaded(old / 'annular-metric-flux-jets-derived' / (label + '.npz'))
                folder = 'annular-boundary-N64-evolution-smoke' if intervals == 64 else 'annular-released-Hermite-evolution-smoke'
                trajectory = loaded(old / folder / (tag + '_steps' + str(steps) + '.npz'))
                basis = MixedActionBasis(source['radius'])
                count = basis.radii.size
                time, state = trajectory['time'][index], trajectory['state'][index]
                scalar, slope, momentum, slope_momentum = [state[part * count:(part + 1) * count] for part in range(4)]
                packed, speed, second = state[4 * count:], spatial['packed_speed'], jets['jet_acceleration']
                system = ReleasedHermiteRouthian(basis, scalar, slope, constants, kappa, momentum, slope_momentum, source['outer_clock'][0] + time * source['outer_clock'][1], MetricLinkQuadrature(basis))
                row, result = evaluate(label, system, packed, speed, second, branch != 'GR')
                close(label + '_prior_normal_growth_unchanged', row['measured_normal_growth'], sample['normal_growth'])
                row.update(intervals=intervals, branch=branch, time=float(time), scope='Original saved state; bounds not time propagation.')
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
                factors, sampling = gram_matrices(count)
                support_diameter = max(numerical.ptp(numerical.flatnonzero(row)) for row in factors)
                check('N' + str(intervals) + '_Gram_support_diameter_at_most_five_cells', support_diameter <= 5)
                check('N' + str(intervals) + '_absolute_Gram_factor_norm', numerical.linalg.norm(abs(factors), 2) <= numerical.sqrt(8) + 1e-12)
                check('N' + str(intervals) + '_one_internal_mass_face_per_scalar_cell', all(numerical.count_nonzero((basis.faces > lower) & (basis.faces < upper)) <= 1 for lower, upper in zip(basis.radii[:-1], basis.radii[1:])))
                for branch in ['GR', 'metric_Gram']:
                    for kind in ['constant_positive', 'constant_negative', 'linear', 'quadratic']:
                        centered = basis.radii - 6.
                        theta = .001 * (numerical.ones(count) if kind == 'constant_positive' else -numerical.ones(count) if kind == 'constant_negative' else centered if kind == 'linear' else centered**2)
                        speed = numerical.zeros_like(packed)
                        speed[system.slices[1]] = .82 * theta
                        label = 'control_N' + str(intervals) + '_' + branch + '_' + kind
                        row, result = evaluate(label, system, packed, speed, numerical.zeros_like(packed), branch != 'GR')
                        if kind.startswith('constant'):
                            expected = .005 if kind == 'constant_positive' else 0.
                            close(label + '_exact_constant_clock_growth_upper', row['derived_normal_growth_upper'], expected)
                        if kind == 'constant_positive':
                            projection_controls(basis, result, metric_envelope(basis, packed[system.slices[0]], packed[system.slices[1]], speed[system.slices[0]], speed[system.slices[1]]))
                        row.update(intervals=intervals, branch=branch, kind=kind, scope='Manufactured off-shell coefficient jet, not physical evolution.')
                        report['controls'].append(row)
                        if kind == 'linear':
                            print(json.dumps({'control': label, 'E_mass_over_h': row['measured_commutator_M_norm_over_h'], 'E_energy': row['measured_commutator_M_to_K_norm'], 'D0_centered_norm': row['measured_centered_D0_K_norm'], 'derived_growth': row['derived_normal_growth_upper']}), flush=True)
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
        raise RuntimeError('Regular transport derivation validation incomplete.')
    inherit(inputs, report['inputs'])
    inherit(outputs, report['outputs'])
    for path in [report_path, destination / 'COMPLETE', destination / 'executed-script.py']:
        own(path)
    note = root / 'DERIVATION-20260910-mesh-independent-regular-transport-with-clock-jumps.md'
    cited = [value for value in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')) if value.endswith(('.py', '.md', '.json', '.npz'))]
    missing = [value for value in cited if root / value != final_path and not (root / value).is_file()]
    if missing:
        raise FileNotFoundError(str(missing))
    own(note)
    snapshot = intake / 'annular-regular-transport-bound-resume-snapshot.md'
    with snapshot.open('xb') as handle:
        handle.write((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    artifact(snapshot)
    frozen = root.parent / 'formalization-workbench'
    since = datetime(2026, 9, 10, 1, 42, 0, tzinfo=timezone.utc).timestamp()
    touched = [str(path.relative_to(frozen)) for path in frozen.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if touched or (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Protected workbench/cache check failed: ' + repr(touched))
    final = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'checks': report['total'], 'saved_states': len(report['samples']), 'controls': len(report['controls']), 'projection_controls': len(report['projection_controls']), 'inputs': inputs, 'outputs': outputs, 'cited_local_paths_checked': cited, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-10T01:42:00Z, not a full pre-turn hash baseline', 'no_bytecode_cache': True, 'conditional_regular_and_normal_form_growth_bounds_derived': True, 'parent_time_propagation_and_external_source_open': True, 'valid_for_physics_claim': False}
    with final_path.open('x') as handle:
        json.dump(final, handle, indent=2)
        handle.write('\n')
    print(json.dumps({name: final[name] for name in ['state', 'checks', 'saved_states', 'controls', 'projection_controls', 'protected_workbench_files_written_since_turn_start']}), flush=True)


if __name__ == '__main__':
    run()
