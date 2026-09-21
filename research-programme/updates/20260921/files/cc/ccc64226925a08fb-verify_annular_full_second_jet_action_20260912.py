import hashlib
import json
import sys
import traceback
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from scipy.linalg import solve
    from annular_canonical_common_profile_aligned_20260912 import CommonProfile
    from annular_frozen_second_jet_complex_20260912 import FrozenSecondJet

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260912'
    destination = intake / 'annular-frozen-second-jet-control-attempt03'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'checks': [], 'cases': [], 'inputs': {}, 'outputs': {}, 'valid_for_physics_claim': False, 'new_evolution': False, 'interval_certificate': False, 'formal_interior_time_germ_only': True}

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
        source = intake / 'annular-frozen-second-jet-attempt02/status.json'
        batch = json.loads(source.read_text())
        own(source)
        check('paired_formal_second_jet_run_complete_not_pass_claim', batch['state'] == 'complete' and not batch['valid_for_physics_claim'] and len(batch['cases']) == 2)
        known = {}
        for table in ['inputs', 'outputs']:
            for name, expected in batch[table].items():
                if name not in known:
                    known[name] = digest(root / name)
                if known[name] != expected:
                    raise RuntimeError('Changed source: ' + name)
                report['inputs'][name] = expected
        own(Path(__file__))
        snapshot = destination / ('executed-' + Path(__file__).name)
        snapshot.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        radius, mu, mu_r, mu_rr, lapse, lapse_r, shift, shift_r, pi, pi_r, gradient, gradient_r, kappa = symbolic.symbols('R mu mu_r mu_rr N N_r P P_r pi pi_r w w_r kappa', real=True)
        geometry = 1 - 2 * mu / radius
        energy = pi**2 / (2 * radius**2) + radius**2 * gradient**2 / 2

        def radial(expression):
            return symbolic.diff(expression, radius) + symbolic.diff(expression, mu) * mu_r + symbolic.diff(expression, mu_r) * mu_rr + symbolic.diff(expression, shift) * shift_r + symbolic.diff(expression, pi) * pi_r + symbolic.diff(expression, gradient) * gradient_r

        coefficient = -mu_r / (kappa * symbolic.sqrt(geometry)) + symbolic.sqrt(geometry) * energy + kappa * geometry**symbolic.Rational(3, 2) * shift * pi * gradient + kappa * geometry**symbolic.Rational(3, 2) * (mu_r - mu / radius) * shift**2 / 2
        radial_coefficient = kappa * radius * geometry**symbolic.Rational(5, 2) * shift**2 / 2
        mass_local = symbolic.diff(coefficient, mu) - radial(symbolic.diff(coefficient, mu_r))
        mass_lapse_gradient = symbolic.diff(radial_coefficient, mu) - symbolic.diff(coefficient, mu_r)
        bracket_coefficient = mass_local * symbolic.diff(radial_coefficient, shift) - mass_lapse_gradient * symbolic.diff(coefficient, shift) + symbolic.diff(coefficient, pi) * symbolic.diff(coefficient, gradient)
        strong_constraint = -coefficient + radial(radial_coefficient)
        check('exact_GR_constraint_bracket_structure', symbolic.simplify(bracket_coefficient + kappa * geometry**symbolic.Rational(3, 2) * shift * strong_constraint) == 0)
        report['derived_GR_bracket'] = '{H[eta],H[N]} = integral (eta*N_R-N*eta_R)*(-kappa*F^(3/2)*P*C_bulk), with radial boundary/interface terms retained separately.'
        report['derived_GR_second_constraint_interior'] = 'At P=0, Cddot[eta] = integral (eta*N_R-N*eta_R)*kappa*F^(3/2)*P_t*C0 for smooth compactly supported tests; independent of N_t. Do not discard interface/boundary terms for broken finite maps.'
        reference = symbolic.sqrt(symbolic.Rational(2, 3))
        hamiltonian = -lapse * (symbolic.sqrt(geometry) + 1 / symbolic.sqrt(geometry) - 2 * reference) / (2 * kappa) - radius * lapse_r * (symbolic.sqrt(geometry) - reference) / kappa
        hamiltonian += lapse * symbolic.sqrt(geometry) * energy + kappa * lapse * geometry**symbolic.Rational(3, 2) * shift * pi * gradient
        hamiltonian += lapse_r * radial_coefficient + kappa * lapse * geometry**symbolic.Rational(3, 2) * (mu_r - mu / radius) * shift**2 / 2
        boundary = radius * lapse * (symbolic.sqrt(geometry) - reference) / kappa + kappa * radius * lapse * geometry**symbolic.Rational(5, 2) * shift**2 / 2
        arguments = [radius, mu, mu_r, lapse, lapse_r, shift, pi, gradient]
        derivatives = [symbolic.diff(hamiltonian, variable).subs(kappa, symbolic.Rational(1, 10)) for variable in arguments[1:]]
        boundary_derivatives = [symbolic.diff(boundary, variable).subs(kappa, symbolic.Rational(1, 10)) for variable in [mu, lapse, shift]]
        bulk_function = symbolic.lambdify(arguments, derivatives, 'numpy', cse=True, docstring_limit=0)
        boundary_function = symbolic.lambdify(arguments, boundary_derivatives, 'numpy', cse=True, docstring_limit=0)

        def local_action_rows(model, result, time):
            def moved(surface):
                values, rates = model.data[surface], model.rates[surface]
                frames = {phase: model.frames[phase][surface] for phase in model.frames}
                mu_value = values['mu'] + time * rates['mu'] + time**2 * (frames['mass']['q'] @ result['second']['mu']) / 2
                mu_gradient = values['mu_r'] + time * rates['mu_r'] + time**2 * (frames['mass']['qr'] @ result['second']['mu']) / 2
                lapse_value = values['N'] + time * (values['eta'] @ result['lapse_rate_coefficients'])
                lapse_gradient = values['N_r'] + time * (values['eta_r'] @ result['lapse_rate_coefficients'])
                shift_value = time * rates['P'] + time**2 * (frames['mass']['p'] @ result['second']['P']) / 2
                pi_value = values['pi'] + time * rates['pi'] + time**2 * (frames['scalar']['p'] @ result['second']['pi']) / 2
                scalar_gradient = values['w'] + time * rates['w'] + time**2 * (frames['scalar']['qr'] @ result['second']['chi']) / 2
                return [values['R'], mu_value, mu_gradient, lapse_value, lapse_gradient, shift_value, pi_value, scalar_gradient]

            bulk_args, node_args = moved(model.surface), moved('nodes')
            bulk = numerical.array([numerical.broadcast_to(value, bulk_args[0].shape) for value in bulk_function(*bulk_args)])
            nodal = numerical.array([numerical.broadcast_to(value, node_args[0].shape) for value in boundary_function(*node_args)])
            node_bulk = numerical.array([numerical.broadcast_to(value, node_args[0].shape) for value in bulk_function(*node_args)])
            mass, scalar = model.frames['mass'][model.surface], model.frames['scalar'][model.surface]
            mass_nodes, scalar_nodes = model.frames['mass']['nodes'], model.frames['scalar']['nodes']
            weights = model.weights
            P_force = -mass['q'].T @ (weights * bulk[0]) - mass['qr'].T @ (weights * bulk[1])
            P_force -= mass_nodes['q'][-1] * (nodal[0, -1] + model.context.system.outer_clock / .1)
            P_force += mass_nodes['q'][0] * (nodal[0, 0] + node_args[3][0] / (.1 * numerical.sqrt(1 - 2 * node_args[1][0] / node_args[0][0])))
            mu_force = mass['p'].T @ (weights * bulk[4]) + mass_nodes['p'][-1] * nodal[2, -1] - mass_nodes['p'][0] * nodal[2, 0]
            pi_force = -scalar['qr'].T @ (weights * bulk[6]) - scalar_nodes['q'][0] * node_bulk[6, 0] + scalar_nodes['q'][-1] * node_bulk[6, -1]
            chi_force = scalar['p'].T @ (weights * bulk[5])
            values, nodes = model.data[model.surface], model.data['nodes']
            constraint = -values['eta'].T @ (weights * bulk[2]) - values['eta_r'].T @ (weights * bulk[3]) - nodes['eta'][-1] * nodal[1, -1] + nodes['eta'][0] * nodal[1, 0]
            return {'mu': solve(model.first['mass_pair'], mu_force), 'P': solve(model.first['mass_pair'].T, P_force), 'chi': solve(model.first['scalar_pair'], chi_force), 'pi': solve(model.first['scalar_pair'].T, pi_force), 'constraint': constraint}

        def transported_gram(model, result, time):
            links, nodes = model.links, model.data['nodes']
            rates, second = model.rates['nodes'], result['nodes']
            lapse_rate = nodes['eta'] @ result['lapse_rate_coefficients']
            endpoint_J, endpoint_L = model.jacobian, result['endpoint_Tss']

            def factor_values(anchor_time, indices):
                selected_nodes = links.node[indices]
                anchor_time = numerical.atleast_1d(anchor_time)[:, None]
                transported = anchor_time * endpoint_J[indices] + anchor_time**2 * endpoint_L[indices] / 2
                jacobian = endpoint_J[indices] + anchor_time * endpoint_L[indices]
                node_mu = nodes['mu'][selected_nodes] + transported * rates['mu'][selected_nodes] + transported**2 * second['mu'][selected_nodes] / 2
                node_N = nodes['N'][selected_nodes] + transported * lapse_rate[selected_nodes]
                node_P = transported * rates['P'][selected_nodes] + transported**2 * second['P'][selected_nodes] / 2
                node_chi = nodes['chi'][selected_nodes] + transported * rates['chi'][selected_nodes] + transported**2 * second['chi'][selected_nodes] / 2
                velocity = rates['chi'][selected_nodes] + transported * second['chi'][selected_nodes]
                geometry = 1 - 2 * node_mu / nodes['R'][selected_nodes]
                coefficient = nodes['R'][selected_nodes]**2 * node_N * numerical.sqrt(geometry) * (1 - .1**2 * geometry**2 * node_P**2)
                amplitude = node_chi @ links.tweight[indices]
                density = (jacobian * coefficient) @ links.sweight[indices]
                amplitude_rate = (jacobian * velocity) @ links.tweight[indices]
                current = amplitude[:, None] * (links.sweight[indices] * coefficient * amplitude_rate[:, None] - links.tweight[indices] * velocity * density[:, None]) / model.basis.spacing
                return amplitude, density, current, jacobian

            local = model.data[model.link_surface]
            local_rates = model.rates[model.link_surface]
            local_mass = local['mu'] + time * local_rates['mu'] + time**2 * (model.frames['mass'][model.link_surface]['q'] @ result['second']['mu']) / 2
            local_lapse = local['N'] + time * (local['eta'] @ result['lapse_rate_coefficients'])
            local_shift = time * local_rates['P'] + time**2 * (model.frames['mass'][model.link_surface]['p'] @ result['second']['P']) / 2
            geometry = 1 - 2 * local_mass / local['R']
            nonlinear = .1**2 * geometry**2 * local_shift**2
            cP = .1 * numerical.sqrt(geometry) * (1 + nonlinear) / (local_lapse * (1 - nonlinear)**2)
            cMu = -.1 * local_shift * (1 + 3 * nonlinear) / (local['R'] * local_lapse * numerical.sqrt(geometry) * (1 - nonlinear)**2)
            cN = -.1 * numerical.sqrt(geometry) * local_shift / (local_lapse**2 * (1 - nonlinear))
            covector = numerical.zeros(local['R'].shape, dtype=numerical.result_type(time))
            for pair, selection, unused_matrix in links.blocks:
                indices = numerical.flatnonzero(links.factor == links.factor[pair])
                selected_pair = int(numerical.flatnonzero(indices == pair)[0])
                anchor = time / model.partial_jacobian[selection] - result['partial_Tss'][selection] * time**2 / (2 * model.partial_jacobian[selection]**3)
                unused_A, unused_D, current, jacobian = factor_values(anchor, indices)
                partial = model.partial_jacobian[selection] + result['partial_Tss'][selection] * anchor
                covector[selection] = current[:, selected_pair] * jacobian[:, selected_pair] / partial**2
            gramP = model.frames['mass'][model.link_surface]['p'].T @ (links.weights * covector * cP)
            gramMu = model.frames['mass'][model.link_surface]['q'].T @ (links.weights * covector * cMu)
            gramN = local['eta'].T @ (links.weights * covector * cN)
            density = numerical.zeros(nodes['R'].shape, dtype=numerical.result_type(time))
            scalar = numerical.zeros_like(density)
            for pair in range(links.node.size):
                indices = numerical.flatnonzero(links.factor == links.factor[pair])
                selected_pair = int(numerical.flatnonzero(indices == pair)[0])
                anchor = time / endpoint_J[pair] - endpoint_L[pair] * time**2 / (2 * endpoint_J[pair]**3)
                amplitude, coefficient, unused_I, jacobian = factor_values(anchor, indices)
                density[links.node[pair]] += links.sweight[pair] * amplitude[0]**2 / (2 * model.basis.spacing)
                scalar[links.node[pair]] -= links.tweight[pair] * amplitude[0] * coefficient[0] / (model.basis.spacing * jacobian[0, selected_pair])
            node_mu = nodes['mu'] + time * rates['mu'] + time**2 * second['mu'] / 2
            node_P = time * rates['P'] + time**2 * second['P'] / 2
            node_N = nodes['N'] + time * lapse_rate
            node_F = 1 - 2 * node_mu / nodes['R']
            coefficient_P = -2 * .1**2 * nodes['R']**2 * node_N * node_F**2.5 * node_P
            coefficient_N = nodes['R']**2 * numerical.sqrt(node_F) * (1 - .1**2 * node_F**2 * node_P**2)
            coefficient_mu = -nodes['R'] * node_N * (1 - 5 * .1**2 * node_F**2 * node_P**2) / numerical.sqrt(node_F)
            gramMu -= model.frames['mass']['nodes']['q'].T @ (density * coefficient_mu)
            gramP -= model.frames['mass']['nodes']['p'].T @ (density * coefficient_P)
            gramN -= nodes['eta'].T @ (density * coefficient_N)
            return {'P': gramP, 'mu': gramMu, 'N': gramN, 'chi': scalar}

        common = CommonProfile(root)
        for branch in ['GR', 'metric_Gram']:
            print('Independent action and transport checks: ' + branch, flush=True)
            model = FrozenSecondJet(common, branch)
            result = model.evaluate(model.candidate())
            record = {'branch': branch}
            local_complex = local_action_rows(model, result, 1e-25j)
            if not model.gram:
                errors = {phase: float(abs(local_complex[phase].imag / 1e-25 - result['second'][phase]).max()) for phase in result['second']}
                record['GR_action_second_rate_errors'] = errors
                check('GR_all_four_accelerations_from_actual_action', max(errors.values()) < 1e-8, errors)
            else:
                gram_complex = transported_gram(model, result, 1e-25j)
                errors = {'G_P_time': float(abs(gram_complex['P'].imag / 1e-25 - result['gram_P_first']).max()), 'G_chi_time': float(abs(gram_complex['chi'].imag / 1e-25 - result['gram_scalar_first']).max())}
                record['independent_inverse_time_errors'] = errors
                check('MTS_inverse_time_second_link_transport_derivatives', max(errors.values()) < 1e-9, errors)
                scalar_map = model.frames['scalar']['nodes']['q']
                scalar_load = scalar_map.T @ (gram_complex['chi'].imag / 1e-25)
                scalar_load -= scalar_map[0] * (gram_complex['chi'][0].imag / 1e-25) + scalar_map[-1] * (gram_complex['chi'][-1].imag / 1e-25)
                independent_second = {
                    'mu': local_complex['mu'].imag / 1e-25 - solve(model.first['mass_pair'], gram_complex['P'].imag / 1e-25),
                    'P': local_complex['P'].imag / 1e-25 + solve(model.first['mass_pair'].T, gram_complex['mu'].imag / 1e-25),
                    'chi': local_complex['chi'].imag / 1e-25,
                    'pi': local_complex['pi'].imag / 1e-25 + solve(model.first['scalar_pair'].T, scalar_load),
                }
                full_errors = {phase: float(abs(independent_second[phase] - result['second'][phase]).max()) for phase in independent_second}
                record['MTS_all_four_action_acceleration_errors'] = full_errors
                check('MTS_all_four_accelerations_from_actual_action_and_inverse_time', max(full_errors.values()) < 1e-8, full_errors)
            differences = []
            computed_arrays = []
            for step in [.002, .001, .0005]:
                states = [local_action_rows(model, result, time)['constraint'] for time in [-step, 0., step]]
                if model.gram:
                    states = [value + transported_gram(model, result, time)['N'] for value, time in zip(states, [-step, 0., step])]
                computed = (states[2] - 2 * states[1] + states[0]) / step**2
                computed_arrays.append(computed)
                differences.append({'step': step, 'max_error': float(abs(computed - result['constraint_second']).max())})
            record['actual_action_constraint_second_differences'] = differences
            extrapolated = (4 * computed_arrays[-1] - computed_arrays[-2]) / 3
            extrapolated_error = float(abs(extrapolated - result['constraint_second']).max())
            record['Richardson_Cddot_error'] = extrapolated_error
            check(branch + '_actual_action_Cddot_independent_Richardson', extrapolated_error < 2e-5, {'raw': differences, 'extrapolated_error': extrapolated_error})
            values, rates = model.data[model.surface], model.rates[model.surface]
            strong_C0 = values['mu_r'] / (.1 * numerical.sqrt(values['F'])) - numerical.sqrt(values['F']) * (values['pi']**2 / (2 * values['R']**2) + values['R']**2 * values['w']**2 / 2)
            expected = (values['eta'] * values['N_r'][:, None] - values['eta_r'] * values['N'][:, None]).T @ (model.weights * .1 * values['F']**1.5 * rates['P'] * strong_C0)
            record['sampled_strong_C0_max_excluding_Gram_nodes'] = float(abs(strong_C0).max())
            record['GR_continuum_bulk_bracket_Cddot'] = expected.tolist()
            record['finite_minus_continuum_bulk_interior_max'] = float(abs(result['constraint_second'][1:16] - expected[1:16]).max())
            record['continuum_comparison_is_not_full_discrete_or_MTS_identity'] = True
            report['cases'].append(record)
            save()
        for module in tuple(sys.modules.values()):
            filename = getattr(module, '__file__', None)
            if filename:
                path = Path(filename).resolve()
                if path.parent == root / 'scripts' and path.suffix == '.py':
                    own(path)
        check('no_python_cache', not (root / 'scripts/__pycache__').exists())
        report['state'] = 'complete'
        save()
        print(json.dumps({'state': report['state'], 'checks': len(report['checks']), 'cases': report['cases']}), flush=True)
    except Exception as error:
        report.update({'state': 'failed', 'error': repr(error), 'traceback': traceback.format_exc()})
        save()
        raise


if __name__ == '__main__':
    run()
