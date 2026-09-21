import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    from scipy.linalg import solve
    from annular_canonical_trace_context_20260911 import TraceContext
    from annular_canonical_trace_projection_stable_20260911 import kernel_family, trace_extension, gram_density_control
    from annular_canonical_rate_completion_20260911 import evaluate_initial
    from annular_canonical_trace_boundary_data_20260911 import BoundaryPreparation

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260911'
    destination = intake / 'annular-canonical-trace-boundary-control-attempt01'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'inputs': {}, 'outputs': {}, 'checks': [], 'samples': [], 'valid_for_physics_claim': False, 'new_evolution': False, 'interval_certificate': False, 'spatial_refinement': False, 'initial_data_refit': 'MTS only: two global cubic auxiliary-momentum lifts and dependent mass constraint solve; GR formula reference retained.'}

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = digest(path)

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        save()
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    def archive(name, arrays):
        path = destination / (name + '.npz')
        if path.exists():
            raise FileExistsError(path)
        numerical.savez_compressed(path, **arrays)
        with numerical.load(path, allow_pickle=False) as saved:
            check(name + '_finite_roundtrip', set(saved.files) == set(arrays) and all(numerical.isfinite(value).all() and numerical.array_equal(value, saved[key]) for key, value in arrays.items()))
        own(path, 'outputs')

    save()
    try:
        prior_path = intake / 'annular-canonical-trace-projection-attempt02/status.json'
        own(prior_path)
        prior = json.loads(prior_path.read_text())
        check('trace_projection_completed', prior['state'] == 'complete' and all(row['passed'] for row in prior['checks']))
        for table in ['inputs', 'outputs']:
            for name, expected in prior[table].items():
                if digest(root / name) != expected:
                    raise RuntimeError('Prior evidence changed: ' + name)
                report['inputs'][name] = expected
        for name in ['annular_canonical_trace_boundary_data_20260911.py', Path(__file__).name]:
            path = root / 'scripts' / name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
            snapshot = destination / ('executed-' + name)
            snapshot.write_bytes(path.read_bytes())
            own(snapshot, 'outputs')
        random = numerical.random.default_rng(911204)
        for branch in ['GR', 'metric_Gram']:
            print('Independent family and canonical controls: ' + branch, flush=True)
            context = TraceContext(root, branch)
            data, frames, unused_completion = context.build()
            old = evaluate_initial(frames['mass'], frames['scalar'], data, context.basis, context.weights, context.links, branch != 'GR', context.system.outer_clock)
            family, primitive, unused_carrier = kernel_family(context, data, frames['mass'], old['P_rate_coeff'])
            extended, diagnostics = trace_extension(context, frames['mass'], family)
            actual = evaluate_initial(extended, frames['scalar'], data, context.basis, context.weights, context.links, branch != 'GR', context.system.outer_clock)
            saved_path = intake / 'annular-canonical-trace-projection-attempt02' / (branch + '_trace_completed.npz')
            with numerical.load(saved_path, allow_pickle=False) as saved:
                check(branch + '_independent_reconstruction_replays', all(abs(actual[key] - saved[key]).max() < 1e-12 for key in ['constraint_rate', 'mass_rate_coeff', 'P_rate_coeff', 'pi_rate_coeff', 'q_coeff']))
            modes = frames['mass']['quad']['q'].shape[1]
            check(branch + '_all_old_maps_unchanged', all(numerical.array_equal(extended[surface][kind][:, :modes], frames['mass'][surface][kind]) for surface in extended for kind in ['q', 'qr', 'p']))
            errors, old_errors = [], []
            for unused_draw in range(12):
                force_coefficients = random.standard_normal(family['quad'].shape[1])
                force = family['quad'] @ force_coefficients
                solved = solve(actual['mass_pair'], extended['quad']['p'].T @ (context.weights * force))
                errors.append(float(abs(extended['nodes']['q'][[0, -1]] @ solved - family['nodes'][[0, -1]] @ force_coefficients).max()))
                old_solved = solve(old['mass_pair'], frames['mass']['quad']['p'].T @ (context.weights * force))
                old_errors.append(float(abs(frames['mass']['nodes']['q'][[0, -1]] @ old_solved - family['nodes'][[0, -1]] @ force_coefficients).max()))
            check(branch + '_unfitted_random_kernel_combinations', max(errors) < 1e-12, errors)
            check(branch + '_old_projection_negative_control', min(old_errors) > 1e-6, old_errors)
            mass_force = actual['mass_pair'].T @ actual['P_rate_coeff']
            old_mass_force = old['mass_pair'].T @ old['P_rate_coeff']
            check(branch + '_same_old_spatial_mass_action', abs(mass_force[:modes] - old_mass_force).max() < 1e-12)
            check(branch + '_scalar_Legendre_equation_unchanged', numerical.array_equal(actual['q_coeff'], old['q_coeff']))
            if branch != 'GR':
                omitted = .1 * data['nodes']['N'][[0, -1]] * data['nodes']['F'][[0, -1]]**1.5 * data['nodes']['pi'][[0, -1]] * data['nodes']['w'][[0, -1]]
                check('omitting_Gram_boundary_force_detected', abs(actual['mu_t_nodes'][[0, -1]] - omitted).max() > 1e-7)
                coefficients, unused_density, kernel_check = gram_density_control(context, data, actual, family, primitive)
                check('factor_anchor_cancellation', kernel_check['anchor_cancellation_max'] < 1e-15)
                check('no_endpoint_Gram_sampling', numerical.all(context.links.sweight[(context.links.node == 0) | (context.links.node == context.basis.radii.size - 1)] == 0))
            report['samples'].append({'branch': branch, 'random_kernel_trace_error': max(errors), 'old_projection_error_minimum': min(old_errors), 'old_mass_Euler_force_error': float(abs(mass_force[:modes] - old_mass_force).max()), 'new_mass_Euler_force': mass_force[-2:].tolist(), 'extension': diagnostics})
            save()
        print('Preparing compatible MTS boundary data with two global cubic lifts.', flush=True)
        context = TraceContext(root, 'metric_Gram')
        preparation = BoundaryPreparation(context)
        amplitudes, prepared, history = preparation.solve()
        selected, data, frames, actual = [prepared[key] for key in ['saved', 'data', 'frames', 'actual']]
        higher = evaluate_initial(frames['mass'], frames['scalar'], data, context.basis, context.check_weights, context.check_links, True, context.system.outer_clock, surface='check', link_surface='links_check')
        nodes = data['nodes']
        record = {'amplitudes': amplitudes.tolist(), 'history': history, 'function_calls': preparation.calls, 'constraint_max': float(abs(actual['constraint']).max()), 'constraint_rate_max': float(abs(actual['constraint_rate']).max()), 'higher_constraint_max': float(abs(higher['constraint']).max()), 'higher_constraint_rate_max': float(abs(higher['constraint_rate']).max()), 'parent_inner_mass_drive_gap': float(prepared['parent_inner_mass_rate'] - selected['boundary_velocity'][0]), 'weak_inner_mass_drive_gap': float(actual['mu_t_nodes'][0] - selected['boundary_velocity'][0]), 'outer_scalar_drive_gap': float(actual['q_nodes'][-1] - selected['boundary_velocity'][2]), 'outer_clock_gap': float(nodes['N'][-1] / numerical.sqrt(nodes['F'][-1]) - context.system.outer_clock), 'minimum_sampled_F': float(min(values['F'].min() for values in data.values())), 'minimum_sampled_N': float(min(values['N'].min() for values in data.values())), 'maximum_mass_coefficient_change': float(abs(selected['mass_coefficients'] - context.saved['mass_coefficients']).max()), 'maximum_auxiliary_pi_coefficient_change': float(abs(selected['pi_coefficients'] - context.saved['pi_coefficients']).max()), 'weak_P_rate_change_after_trace_extension': float(abs(actual['P_t'] - prepared['baseline']['P_t']).max()), 'frame_completion': prepared['completion'], 'trace_extension': prepared['extension'], 'interval_certificate': False, 'new_evolution': False}
        report['boundary_preparation'] = record
        archive('MTS_prepared_initial_data', selected)
        for variant, result in [('prepared', actual), ('higher', higher)]:
            arrays = {key: value for key, value in result.items() if isinstance(value, numerical.ndarray)}
            surface = 'check' if variant == 'higher' else 'quad'
            arrays.update({'field_' + key: value for key, value in data[surface].items()})
            arrays.update({'mass_' + key: value for key, value in frames['mass'][surface].items()})
            arrays.update({'scalar_' + key: value for key, value in frames['scalar'][surface].items()})
            arrays['weights'] = context.check_weights if surface == 'check' else context.weights
            archive('MTS_' + variant + '_first_jet', arrays)
        archive('MTS_preparation_lifts', {'amplitudes': amplitudes, 'global_cubic_lifts': preparation.pi_lifts, 'radii': context.basis.radii})
        check('two_amplitude_boundary_root', abs(prepared['residual']).max() < 2e-12, prepared['residual'].tolist())
        check('prepared_all_C_and_Cdot_rows', max(record[key] for key in ['constraint_max', 'constraint_rate_max', 'higher_constraint_max', 'higher_constraint_rate_max']) < 1e-10, record)
        check('retained_external_drives_and_clock', max(abs(record[key]) for key in ['parent_inner_mass_drive_gap', 'weak_inner_mass_drive_gap', 'outer_scalar_drive_gap', 'outer_clock_gap']) < 1e-11)
        check('no_hidden_change_to_fixed_inputs', numerical.array_equal(selected['boundary_velocity'], context.saved['boundary_velocity']) and numerical.array_equal(selected['configuration'], context.saved['configuration']) and selected['mass_coefficients'][0] == context.saved['mass_coefficients'][0] and numerical.array_equal(selected['mass_coefficients'][preparation.face_count:], context.saved['mass_coefficients'][preparation.face_count:]))
        check('global_cubic_lifts_only', numerical.allclose(selected['pi_coefficients'] - context.saved['pi_coefficients'], preparation.pi_lifts @ amplitudes, rtol=0., atol=1e-17))
        check('positive_sampled_chart_not_interval_claim', record['minimum_sampled_F'] > .1 and record['minimum_sampled_N'] > .1)
        direction = random.standard_normal(preparation.face_count - 1)
        direction /= numerical.linalg.norm(direction)
        changed = {key: value.copy() for key, value in selected.items()}
        changed['mass_coefficients'] = selected['mass_coefficients'].astype(complex)
        changed['mass_coefficients'][1:preparation.face_count] += 1e-25j * direction
        derivative_actual = preparation.mass_equations(changed)[0].imag / 1e-25
        derivative_expected = preparation.mass_equations(selected)[1] @ direction
        derivative_error = float(abs(derivative_actual - derivative_expected).max())
        check('analytic_mass_constraint_derivative', derivative_error < 1e-10, derivative_error)
        record['analytic_mass_derivative_error'] = derivative_error
        first_jacobian = numerical.asarray(history[0]['boundary_jacobian'])
        step = 2e-8
        checked_jacobian = numerical.column_stack([(preparation.evaluate(amplitudes + step * direction)['residual'] - preparation.evaluate(amplitudes - step * direction)['residual']) / (2 * step) for direction in numerical.eye(2)])
        record['final_independent_boundary_jacobian'] = checked_jacobian.tolist()
        record['final_boundary_jacobian_condition'] = float(numerical.linalg.cond(checked_jacobian))
        check('independent_boundary_sensitivity_nondegenerate', record['final_boundary_jacobian_condition'] < 100 and abs(checked_jacobian - first_jacobian).max() < 1e-3)
        replay = preparation.evaluate(amplitudes)
        check('fresh_prepared_state_replay', abs(replay['actual']['constraint_rate'] - actual['constraint_rate']).max() < 1e-11 and abs(replay['residual']).max() < 2e-12)
        record['function_calls_including_controls'] = preparation.calls
        for module in tuple(sys.modules.values()):
            filename = getattr(module, '__file__', None)
            if filename:
                path = Path(filename).resolve()
                if path.parent == root / 'scripts' and path.suffix == '.py':
                    own(path)
        check('no_python_cache', not (root / 'scripts/__pycache__').exists())
        report['state'] = 'complete'
        report['completed_utc'] = datetime.now(timezone.utc).isoformat()
        save()
        print(json.dumps({'state': report['state'], 'checks': len(report['checks']), 'boundary_preparation': record}), flush=True)
    except Exception as error:
        report['state'] = 'failed'
        report['error'] = repr(error)
        save()
        raise


if __name__ == '__main__':
    run()
