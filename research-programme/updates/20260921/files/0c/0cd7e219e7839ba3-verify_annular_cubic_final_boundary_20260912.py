import hashlib
import json
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from scipy.linalg import solve
    from annular_canonical_common_profile_aligned_20260912 import CommonProfile
    from annular_canonical_trace_context_20260911 import load_archive
    from annular_cubic_lapse_final_boundary_20260912 import CubicContext, CubicPreparation, GRAVITY_REFERENCE_ROOT
    from annular_cubic_lapse_reference_gravity_20260912 import evaluate_cubic_initial

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260912'
    source = intake / 'annular-cubic-lapse-boundary-attempt07'
    destination = intake / 'annular-cubic-boundary-control-attempt01'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'inputs': {}, 'outputs': {}, 'checks': [], 'cases': [], 'valid_for_physics_claim': False, 'new_evolution': False, 'interval_certificate': False, 'next_lapse_rates_are_candidates_only': True}

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

    save()
    try:
        status = json.loads((source / 'status.json').read_text())
        own(source / 'status.json')
        check('paired_final_run_complete', status['state'] == 'complete' and len(status['cases']) == 2 and all(row['finite_initial_gate'] and row['classical_P_trace_tangent_gate'] for row in status['cases']))
        for table in ['inputs', 'outputs']:
            for name, expected in status[table].items():
                if digest(root / name) != expected:
                    raise RuntimeError('Changed evidence: ' + name)
                report['inputs'][name] = expected
        own(Path(__file__))
        snapshot = destination / ('executed-' + Path(__file__).name)
        snapshot.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        radius, mass, mass_r, lapse, lapse_r, kappa, reference = symbolic.symbols('R mu mu_R N N_R kappa reference', positive=True)
        geometry = 1 - 2 * mass / radius
        root_f = symbolic.sqrt(geometry)
        original = -lapse * mass_r / (kappa * root_f)
        changed = -lapse * (root_f + 1 / root_f - 2 * reference) / (2 * kappa) - radius * lapse_r * (root_f - reference) / kappa
        primitive = radius * lapse * (root_f - reference) / kappa
        derivative = symbolic.diff(primitive, radius) + symbolic.diff(primitive, mass) * mass_r + symbolic.diff(primitive, lapse) * lapse_r
        check('exact_action_change_is_radial_boundary', symbolic.simplify(changed - original + derivative) == 0)
        check('reference_changes_only_analytically_null_boundary_integral', symbolic.simplify(symbolic.diff(changed, reference) - (lapse + radius * lapse_r) / kappa) == 0 and symbolic.diff(primitive, reference) == -radius * lapse / kappa)
        mass_rate, energy, energy_rate = symbolic.symbols('mu_t energy energy_t', real=True)
        gradient_law = kappa * energy / radius + mass / (radius**2 * geometry)
        law_rate = symbolic.diff(gradient_law, mass) * mass_rate + symbolic.diff(gradient_law, energy) * energy_rate
        check('exact_next_endpoint_clock_gradient_law', symbolic.simplify(law_rate - kappa * energy_rate / radius - mass_rate / (radius**2 * geometry**2)) == 0)
        common = CommonProfile(root)
        for branch in ['GR', 'metric_Gram']:
            context = CubicContext(common, branch)
            label = branch + '_corrected'
            selected = load_archive(source / (label + '_initial_data.npz'))
            raw_data = load_archive(source / (label + '_data.npz'))
            raw_frames = load_archive(source / (label + '_frames.npz'))
            data = {surface: {key.split('__', 1)[1]: value for key, value in raw_data.items() if key.startswith(surface + '__')} for surface in context.surfaces}
            frames = {phase: {surface: {kind: raw_frames[phase + '__' + surface + '__' + kind] for kind in ['q', 'qr', 'p']} for surface in context.surfaces} for phase in ['mass', 'scalar']}
            saved = load_archive(source / (label + '_primary.npz'))
            replay = evaluate_cubic_initial(frames['mass'], frames['scalar'], data, context.basis, context.weights, context.links, context.include_gram, context.system.outer_clock)
            check(branch + '_fixed_frame_replay', max(float(abs(replay[key] - saved[key]).max()) for key in ['constraint', 'constraint_rate', 'P_t_nodes', 'mu_t_nodes', 'q_nodes']) < 1e-13)
            interior = numerical.arange(1, context.basis.radii.size - 1)
            nodal_load = frames['mass']['nodes']['q'][interior].T
            nodal_solution = solve(saved['mass_pair'].T, nodal_load)
            all_source_trace = frames['mass']['nodes']['p'][[0, -1]] @ nodal_solution
            trace_error = float(abs(all_source_trace).max())
            check(branch + '_all_fifteen_nodal_sources_have_zero_P_trace', trace_error < 1e-10, trace_error)
            preparation = CubicPreparation(context)
            direction = numerical.sin(numerical.arange(19) + .42)
            direction /= numerical.linalg.norm(direction)
            trial = {key: value.copy() for key, value in selected.items()}
            trial['mass_coefficients'] = trial['mass_coefficients'].astype(complex)
            trial['mass_lift_coefficients'] = trial['mass_lift_coefficients'].astype(complex)
            trial['mass_coefficients'][1:18] += 1e-25j * direction[:17]
            trial['mass_lift_coefficients'] += 1e-25j * direction[-2:]
            derivative_error = float(abs(preparation.mass_equations(trial)[0].imag / 1e-25 - preparation.mass_equations(selected)[1] @ direction).max())
            check(branch + '_analytic_nineteen_row_mass_Jacobian', derivative_error < 1e-9, derivative_error)
            values, nodes = data['quad'], data['nodes']
            weights, points = context.weights, values['R']
            offset = GRAVITY_REFERENCE_ROOT

            def gravity_action(local_mass, node_mass, local_lapse, node_lapse, local_lapse_r):
                geometry_root = numerical.sqrt(1 - 2 * local_mass / points)
                node_root = numerical.sqrt(1 - 2 * node_mass / nodes['R'])
                density = -local_lapse * (geometry_root + 1 / geometry_root - 2 * offset) / .2 - points * local_lapse_r * (geometry_root - offset) / .1
                return weights @ density + (nodes['R'] * node_lapse * (node_root - offset))[-1] / .1 - (nodes['R'] * node_lapse * (node_root - offset))[0] / .1

            mass_direction = frames['mass']['quad']['q'][:, 3]
            node_mass_direction = frames['mass']['nodes']['q'][:, 3]
            step = 1e-25
            actual_derivative = gravity_action(values['mu'] + 1j * step * mass_direction, nodes['mu'] + 1j * step * node_mass_direction, values['N'], nodes['N'], values['N_r']).imag / step
            expected = weights @ (mass_direction * (values['N_r'] / (.1 * numerical.sqrt(values['F'])) - values['N'] * values['mu'] / (.1 * points**2 * values['F']**1.5)))
            expected -= nodes['N'][-1] * node_mass_direction[-1] / (.1 * numerical.sqrt(nodes['F'][-1]))
            expected += nodes['N'][0] * node_mass_direction[0] / (.1 * numerical.sqrt(nodes['F'][0]))
            check(branch + '_actual_integrated_gravity_mass_variation', abs(actual_derivative - expected) < 1e-10, float(abs(actual_derivative - expected)))
            lapse_direction = values['eta'][:, -1]
            lapse_direction_r = values['eta_r'][:, -1]
            node_lapse_direction = nodes['eta'][:, -1]
            lapse_derivative = gravity_action(values['mu'], nodes['mu'], values['N'] + 1j * step * lapse_direction, nodes['N'] + 1j * step * node_lapse_direction, values['N_r'] + 1j * step * lapse_direction_r).imag / step
            gravitational_constraint = weights @ (lapse_direction * (numerical.sqrt(values['F']) + 1 / numerical.sqrt(values['F']) - 2 * offset) / .2 + lapse_direction_r * points * (numerical.sqrt(values['F']) - offset) / .1)
            gravitational_constraint -= (node_lapse_direction * nodes['R'] * (numerical.sqrt(nodes['F']) - offset))[-1] / .1
            gravitational_constraint += (node_lapse_direction * nodes['R'] * (numerical.sqrt(nodes['F']) - offset))[0] / .1
            check(branch + '_actual_new_cubic_lapse_action_variation', abs(lapse_derivative + gravitational_constraint) < 1e-10, float(abs(lapse_derivative + gravitational_constraint)))
            old_H = weights @ (-values['N'] * values['mu_r'] / (.1 * numerical.sqrt(values['F'])))
            new_H = gravity_action(values['mu'], nodes['mu'], values['N'], nodes['N'], values['N_r'])
            boundary = (nodes['R'] * nodes['N'] * (numerical.sqrt(nodes['F']) - offset))[-1] / .1 - (nodes['R'] * nodes['N'] * (numerical.sqrt(nodes['F']) - offset))[0] / .1
            derivative_primitive = ((values['N'] + points * values['N_r']) * (numerical.sqrt(values['F']) - offset) + points * values['N'] * values['F_r'] / (2 * numerical.sqrt(values['F']))) / .1
            action_defect = boundary - weights @ derivative_primitive
            check(branch + '_finite_action_difference_reported_not_hidden', abs(new_H - old_H - action_defect) < 1e-12)
            root_f_nodes = numerical.sqrt(nodes['F'])
            energy_rate_nodes = nodes['pi'] * (frames['scalar']['nodes']['p'] @ saved['pi_rate_coeff']) / nodes['R']**2 + nodes['R']**2 * nodes['w'] * (frames['scalar']['nodes']['qr'] @ saved['q_coeff'])
            desired_log_gradient_rate = .1 * energy_rate_nodes / nodes['R'] + saved['mu_t_nodes'] / (nodes['R']**2 * nodes['F']**2)
            scale_rate = -saved['mu_t_nodes'][-1] / (nodes['R'][-1] * nodes['F'][-1])
            amplitudes = (nodes['N'] * desired_log_gradient_rate)[[0, -1]]
            raw, raw_gradient = context.family.raw(nodes['R'])
            lapse_rate = scale_rate * nodes['N'] + raw @ amplitudes
            lapse_rate_r = scale_rate * nodes['N_r'] + raw_gradient @ amplitudes
            log_gradient_rate = lapse_rate_r / nodes['N'] - nodes['N_r'] * lapse_rate / nodes['N']**2
            clock_error = lapse_rate[-1] / root_f_nodes[-1] + nodes['N'][-1] * saved['mu_t_nodes'][-1] / (nodes['R'][-1] * nodes['F'][-1]**1.5)
            check(branch + '_candidate_next_clock_gradient', abs(log_gradient_rate[[0, -1]] - desired_log_gradient_rate[[0, -1]]).max() < 1e-10)
            check(branch + '_candidate_next_outer_clock_rate', abs(clock_error) < 1e-12)
            candidate_path = destination / (branch + '_unapplied_next_lapse_rate.npz')
            numerical.savez_compressed(candidate_path, radii=nodes['R'], lapse_rate=lapse_rate, lapse_rate_r=lapse_rate_r, endpoint_gradient_amplitudes=amplitudes, full_second_jet_solved=numerical.array(False))
            own(candidate_path, 'outputs')
            report['cases'].append({'branch': branch, 'nodal_family_trace_error': trace_error, 'mass_Jacobian_error': derivative_error, 'actual_gravity_action_change': float(new_H - old_H), 'derived_finite_action_defect': float(action_defect), 'next_clock_scale_rate': float(scale_rate), 'next_lapse_gradient_amplitudes': amplitudes.tolist(), 'next_lapse_candidate_only': True})
        check('no_python_cache', not (root / 'scripts/__pycache__').exists())
        report['state'] = 'complete'
        save()
        print(json.dumps({'state': report['state'], 'checks': len(report['checks']), 'cases': report['cases']}), flush=True)
    except Exception as error:
        report['state'], report['error'] = 'failed', repr(error)
        save()
        raise


if __name__ == '__main__':
    run()
