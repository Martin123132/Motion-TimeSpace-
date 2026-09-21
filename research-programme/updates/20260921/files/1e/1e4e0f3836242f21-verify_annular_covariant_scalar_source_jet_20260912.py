import hashlib
import json
import sys
import traceback
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as np
    from scipy.linalg import solve
    from annular_canonical_common_profile_aligned_20260912 import CommonProfile
    from annular_canonical_trace_context_20260911 import load_archive
    from annular_canonical_trace_projection_stable_20260911 import GlobalPrimitive
    from annular_frozen_second_jet_complex_20260912 import FrozenSecondJet
    from annular_scalar_kinetic_pair_20260912 import refresh
    from annular_covariant_scalar_action_20260912 import full_spatial_factors

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260912'
    source = intake / 'annular-acceleration-trace-completion-attempt02'
    destination = intake / 'annular-covariant-scalar-source-jet-attempt01'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'checks': [], 'cases': [], 'inputs': {}, 'outputs': {}, 'valid_for_physics_claim': False, 'new_evolution': False, 'full_second_jet_closed': False, 'interval_certificate': False, 'new_finite_scalar_action': True, 'scalar_jet_metric_history_prescribed_not_coupled_solution': True, 'constraint_only_mass_preparation_not_full_boundary_first_jet': True, 'old_working_branch_unchanged': True}

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        save()
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    save()
    try:
        previous_path = intake / 'annular-covariant-full-scalar-action-attempt01/status.json'
        previous = json.loads(previous_path.read_text())
        check('new_action_validation_complete_not_a_coupled_solution', previous['state'] == 'complete' and previous['full_coupled_initial_state_not_yet_prepared'])
        inherited = dict(previous['inputs'])
        inherited.update(previous['outputs'])
        for name, expected in inherited.items():
            if hashlib.sha256((root / name).read_bytes()).hexdigest() != expected:
                raise RuntimeError('Changed evidence: ' + name)
            report['inputs'][name] = expected
        own(previous_path)
        own(Path(__file__))
        snapshot = destination / ('executed-' + Path(__file__).name)
        snapshot.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        common = CommonProfile(root)
        for branch in ['GR', 'metric_Gram']:
            print('Source-backed scalar jet and new C0 preparation: ' + branch, flush=True)
            model = FrozenSecondJet(common, branch)
            for phase in model.frames:
                raw = load_archive(source / (branch + '_extended_' + phase + '_frames.npz'))
                model.frames[phase] = {surface: {kind: raw[surface + '__' + kind] for kind in ['q', 'qr', 'p']} for surface in model.data}
            refresh(model)
            saved = load_archive(source / (branch + '_completed_second_jet.npz'))
            old_result = model.evaluate(saved['lapse_rate_coefficients'])
            values, nodes = model.data['quad'], model.data['nodes']
            rates, node_rates = model.rates['quad'], model.rates['nodes']
            lapse_first = values['eta'] @ saved['lapse_rate_coefficients']
            node_lapse_first = nodes['eta'] @ saved['lapse_rate_coefficients']
            cP = .1 * np.sqrt(values['F']) / values['N']
            alpha = -rates['mu'] / (values['R'] * values['F']) - lapse_first / values['N']
            generator = cP * rates['P']
            second_generator = cP * (model.frames['mass']['quad']['p'] @ old_result['second']['P'] + 2 * alpha * rates['P'])
            first_primitive = GlobalPrimitive(model.context.knots, generator, 12)
            second_primitive = GlobalPrimitive(model.context.knots, second_generator * np.exp(first_primitive.evaluate(values['R'])), 12)
            factors, sampling = full_spatial_factors(nodes['R'].size, model.gram)
            factor, node = np.nonzero((factors != 0) | (sampling != 0))
            anchors = (sampling @ nodes['R'])[factor]
            targets = nodes['R'][node]
            target_g, anchor_g = first_primitive.evaluate(targets), first_primitive.evaluate(anchors)
            endpoint_J = np.exp(target_g - anchor_g)
            endpoint_L = np.exp(target_g - 2 * anchor_g) * (second_primitive.evaluate(targets) - second_primitive.evaluate(anchors))
            factor_weight, sample_weight = factors[factor, node], sampling[factor, node]
            spacing = model.basis.spacing
            node_weights = np.full(nodes['R'].size, spacing)
            node_weights[[0, -1]] /= 2

            def collect(array):
                return np.bincount(factor, weights=array, minlength=factors.shape[0])

            def scatter(array):
                return np.bincount(node, weights=array, minlength=nodes['R'].size)

            coefficient = nodes['R']**2 * nodes['N'] * np.sqrt(nodes['F'])
            coefficient_first = nodes['R']**2 * (node_lapse_first * np.sqrt(nodes['F']) - nodes['N'] * node_rates['mu'] / (nodes['R'] * np.sqrt(nodes['F'])))
            scalar = nodes['chi']
            momentum = nodes['pi'].copy()
            velocity = coefficient * momentum / nodes['R']**4
            amplitude = factors @ scalar
            density = collect(sample_weight * endpoint_J * coefficient[node])
            amplitude_first = collect(factor_weight * endpoint_J * velocity[node])
            scalar_force = scatter(-factor_weight * amplitude[factor] * density[factor] / (spacing * endpoint_J))
            source_force = np.zeros_like(momentum)
            source_force[[0, -1]] = model.first['reactions'][1:]
            old_flux_first = nodes['R']**2 * ((node_lapse_first * np.sqrt(nodes['F']) - nodes['N'] * node_rates['mu'] / (nodes['R'] * np.sqrt(nodes['F']))) * nodes['w'] + nodes['N'] * np.sqrt(nodes['F']) * node_rates['w'])
            old_flux_first += .1 * nodes['N'] * nodes['F']**1.5 * node_rates['P'] * nodes['pi']
            source_force_first = np.zeros_like(momentum)
            source_force_first[[0, -1]] = np.array([-1., 1.]) * old_flux_first[[0, -1]] - old_result['gram_scalar_first'][[0, -1]]
            momentum_first = (scalar_force + source_force) / node_weights
            acceleration = (coefficient_first * momentum + coefficient * momentum_first) / nodes['R']**4
            density_first = collect(sample_weight * (endpoint_L * coefficient[node] + endpoint_J**2 * coefficient_first[node]))
            amplitude_second = collect(factor_weight * (endpoint_L * velocity[node] + endpoint_J**2 * acceleration[node]))
            current = amplitude[factor] * (sample_weight * coefficient[node] * amplitude_first[factor] - factor_weight * velocity[node] * density[factor]) / spacing
            current_first = amplitude_first[factor] * (sample_weight * coefficient[node] * amplitude_first[factor] - factor_weight * velocity[node] * density[factor]) / spacing
            current_first += amplitude[factor] * (sample_weight * (endpoint_J * coefficient_first[node] * amplitude_first[factor] + coefficient[node] * amplitude_second[factor]) - factor_weight * (endpoint_J * acceleration[node] * density[factor] + velocity[node] * density_first[factor])) / spacing
            scalar_force_first = scatter(-factor_weight / (spacing * endpoint_J**2) * (amplitude_first[factor] * density[factor] + amplitude[factor] * density_first[factor] - amplitude[factor] * density[factor] * endpoint_L / endpoint_J))
            momentum_second = (scalar_force_first + source_force_first) / node_weights
            nodal_d = sampling.T @ amplitude**2 / (2 * spacing)
            nodal_d_first = scatter(sample_weight * amplitude[factor] * amplitude_first[factor] / (spacing * endpoint_J))
            nodal_d_second = scatter(sample_weight / spacing * ((amplitude_first[factor]**2 + amplitude[factor] * amplitude_second[factor]) / endpoint_J**2 - amplitude[factor] * amplitude_first[factor] * endpoint_L / endpoint_J**3))
            EC_first = -node_weights * momentum * momentum_first / nodes['R']**4 - nodal_d_first
            EC_second = -node_weights * (momentum_first**2 + momentum * momentum_second) / nodes['R']**4 - nodal_d_second
            jump = -scatter(current / endpoint_J)
            jump_first = -scatter(current_first / endpoint_J**2 - current * endpoint_L / endpoint_J**3)
            exchange = jump - coefficient * EC_first - source_force * velocity
            exchange_first = jump_first - coefficient_first * EC_first - coefficient * EC_second - source_force_first * velocity - source_force * acceleration
            check(branch + '_all17_source_driven_scalar_equations', max(float(abs(-node_weights * momentum_first + scalar_force + source_force).max()), float(abs(-node_weights * momentum_second + scalar_force_first + source_force_first).max())) < 1e-12)
            check(branch + '_all17_nodal_energy_Ward_with_ports', max(float(abs(exchange).max()), float(abs(exchange_first).max())) < 1e-11, {'first': float(abs(exchange).max()), 'second': float(abs(exchange_first).max())})
            check(branch + '_anchor_work_not_discarded', max(float(abs(collect(endpoint_J * current)).max()), float(abs(collect(endpoint_L * current + endpoint_J * current_first)).max())) < 1e-10)
            check(branch + '_initial_scalar_velocity_unchanged', abs(velocity - node_rates['chi']).max() < 1e-12)
            local_primitive = [GlobalPrimitive(model.context.knots, values['eta'][:, column], 12) for column in range(19)]
            mass_maps = {surface: np.column_stack([primitive.evaluate(data['R']) for primitive in local_primitive]) for surface, data in model.data.items()}
            node_energy = node_weights * momentum**2 / (2 * nodes['R']**2) + nodes['R']**2 * nodal_d
            reference = np.sqrt(2 / 3)

            def constraint(coefficients, derivative=False):
                mass = values['mu'] + mass_maps['quad'] @ coefficients
                node_mass = nodes['mu'] + mass_maps['nodes'] @ coefficients
                geometry = 1 - 2 * mass / values['R']
                node_geometry = 1 - 2 * node_mass / nodes['R']
                if min(geometry.real.min(), node_geometry.real.min()) <= .1:
                    raise ValueError('Mass trial leaves the positive chart.')
                root_f, node_root = np.sqrt(geometry), np.sqrt(node_geometry)
                residual = values['eta'].T @ (model.weights * (root_f + 1 / root_f - 2 * reference) / .2)
                residual += values['eta_r'].T @ (model.weights * values['R'] * (root_f - reference) / .1)
                residual -= nodes['eta'][-1] * nodes['R'][-1] * (node_root[-1] - reference) / .1
                residual += nodes['eta'][0] * nodes['R'][0] * (node_root[0] - reference) / .1
                residual -= nodes['eta'].T @ (node_root * node_energy)
                if not derivative:
                    return residual
                jacobian = values['eta'].T @ ((model.weights * mass / (.1 * values['R']**2 * geometry**1.5))[:, None] * mass_maps['quad'])
                jacobian -= values['eta_r'].T @ ((model.weights / (.1 * root_f))[:, None] * mass_maps['quad'])
                jacobian += np.outer(nodes['eta'][-1], mass_maps['nodes'][-1]) / (.1 * node_root[-1])
                jacobian -= np.outer(nodes['eta'][0], mass_maps['nodes'][0]) / (.1 * node_root[0])
                jacobian += nodes['eta'].T @ ((node_energy / (nodes['R'] * node_root))[:, None] * mass_maps['nodes'])
                return residual, jacobian

            coefficients = np.zeros(19)
            initial_residual, jacobian = constraint(coefficients, True)
            complex_jacobian = np.column_stack([constraint(1e-25j * np.eye(19)[column]).imag / 1e-25 for column in range(19)])
            check(branch + '_new_C0_Jacobian_derived_not_finite_difference_fit', abs(jacobian - complex_jacobian).max() < 1e-9, float(abs(jacobian - complex_jacobian).max()))
            history = []
            for iteration in range(12):
                residual, jacobian = constraint(coefficients, True)
                error = float(abs(residual).max())
                history.append({'iteration': iteration, 'max_constraint': error})
                if error < 1e-11:
                    break
                direction = solve(jacobian, -residual)
                for backtrack in range(18):
                    candidate = coefficients + direction * 2.**(-backtrack)
                    try:
                        trial_error = float(abs(constraint(candidate)).max())
                    except ValueError:
                        continue
                    if trial_error < error:
                        coefficients = candidate
                        break
                else:
                    raise RuntimeError('C0 Newton line search stalled.')
            prepared_constraint = constraint(coefficients)
            check(branch + '_new_full19_C0_only_preparation', abs(prepared_constraint).max() < 1e-10, history)
            new_mass = {surface: data['mu'] + mass_maps[surface] @ coefficients for surface, data in model.data.items()}
            check(branch + '_dependent_mass_change_keeps_inner_source_exact', abs(new_mass['nodes'][0] - nodes['mu'][0]) < 1e-14)
            new_F = 1 - 2 * new_mass['nodes'] / nodes['R']
            clock_change = nodes['N'][-1] / np.sqrt(new_F[-1]) - model.context.system.outer_clock
            new_outer_velocity = nodes['N'][-1] * np.sqrt(new_F[-1]) * momentum[-1] / nodes['R'][-1]**2
            record = {'branch': branch, 'nodes': nodes['R'].size, 'scalar_equations_solved_on_prescribed_old_metric_jet_only': True, 'old_port_force_samples_transferred_not_full_boundary_history_derived': True, 'node_energy_identity_max': float(abs(exchange).max()), 'node_energy_identity_time_max': float(abs(exchange_first).max()), 'port_work_without_source_subtraction_max': float(abs(source_force * velocity).max()), 'minimum_J': float(endpoint_J.min()), 'new_C0_on_old_geometry_max': float(abs(initial_residual).max()), 'prepared_new_C0_max': float(abs(prepared_constraint).max()), 'new_C0_jacobian_condition': float(np.linalg.cond(jacobian)), 'mass_change_max_all_surfaces': max(float(abs(new_mass[surface] - model.data[surface]['mu']).max()) for surface in new_mass), 'new_geometry_min_all_surfaces': min(float((1 - 2 * new_mass[surface] / model.data[surface]['R']).min()) for surface in new_mass), 'new_outer_clock_gap_at_old_lapse': float(clock_change), 'new_outer_scalar_drive_gap_at_old_lapse': float(new_outer_velocity - model.saved['boundary_velocity'][2]), 'first_and_second_jets_not_recomputed_on_prepared_mass': True, 'Newton_history': history}
            report['cases'].append(record)
            path = destination / (branch + '_source_jet_and_C0_only_preparation.npz')
            np.savez_compressed(path, scalar=scalar, momentum=momentum, scalar_velocity=velocity, scalar_acceleration=acceleration, momentum_first=momentum_first, momentum_second=momentum_second, prescribed_port_force=source_force, prescribed_port_force_first=source_force_first, nodal_Ward=exchange, nodal_Ward_time=exchange_first, mass_change_coefficients=coefficients, initial_C0=initial_residual, prepared_C0=prepared_constraint, endpoint_J=endpoint_J, endpoint_L=endpoint_L, **{surface + '_prepared_mass': array for surface, array in new_mass.items()}, **{surface + '_mass_variation_map': array for surface, array in mass_maps.items()})
            own(path, 'outputs')
            save()
            print(json.dumps(record), flush=True)
        for module in tuple(sys.modules.values()):
            filename = getattr(module, '__file__', None)
            if filename:
                path = Path(filename).resolve()
                if path.parent == root / 'scripts' and path.suffix == '.py':
                    own(path)
        check('no_python_cache', not (root / 'scripts/__pycache__').exists())
        report['state'] = 'complete'
        save()
    except Exception as error:
        report.update({'state': 'failed', 'error': repr(error), 'traceback': traceback.format_exc()})
        save()
        raise


if __name__ == '__main__':
    run()
