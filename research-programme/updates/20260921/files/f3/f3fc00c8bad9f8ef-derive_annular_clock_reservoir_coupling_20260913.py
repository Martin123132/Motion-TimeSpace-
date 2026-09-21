import hashlib
import json
import sys
import traceback
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as np
    import sympy as sp
    from annular_clock_reservoir_coupling_20260913 import ClockReservoirPreparation, ProperClockDrive, clock_factor

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260913'
    destination = intake / 'annular-clock-reservoir-coupling-attempt01'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'checks': [], 'inputs': {}, 'outputs': {}, 'cases': [], 'action_variations': [],
              'valid_for_physics_claim': False, 'full_GR_limit_proven': False, 'full_C2_evaluated': False,
              'full_first_jet_closed': False, 'boundary_histories_complete': False,
              'full_physical_radial_port_action_signed': False, 'unique_parent_regularizer_derived': False,
              'apparatus_microphysics_derived': False, 'full_geometric_evolution': False,
              'point_force_adopted': False, 'new_fundamental_MTS_field_claimed': False,
              'finite_width_proper_clock_apparatus_candidate': True,
              'forced_acceleration_recovery_is_not_independent_prediction': True,
              'proper_acceleration_extension': 'constant across rightmost collar in individual source proper clocks',
              'initial_reservoir_energy_budgets': [.001, .002],
              'initial_lapse_time_extension': 'constant N1/N, normalized to sourced physical outer clock derivative'}

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        save()
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    save()
    try:
        previous_path = intake / 'annular-collar-response-final-integrity.json'
        previous = json.loads(previous_path.read_text())
        check('previous_complete_with_free_boundary_failure_preserved', previous['state'] == 'complete' and previous['free_outer_second_order_all_pass'] is False)
        for table in ['inputs', 'outputs']:
            for filename, expected in previous[table].items():
                if filename in report['inputs'] and report['inputs'][filename] != expected:
                    raise RuntimeError('Inconsistent inherited hash: ' + filename)
                if filename not in report['inputs']:
                    if hashlib.sha256((root / filename).read_bytes()).hexdigest() != expected:
                        raise RuntimeError('Changed inherited evidence: ' + filename)
                    report['inputs'][filename] = expected
        own(previous_path)
        for path in [Path(__file__), root / 'scripts/annular_clock_reservoir_coupling_20260913.py']:
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
            executed = destination / ('executed-' + path.name)
            executed.write_bytes(path.read_bytes())
            own(executed, 'outputs')

        radius, lapse, mass, momentum, coupling, energy = sp.symbols('R N mu P kappa E', positive=True)
        root_squared = 1 - 2 * mass / radius
        proper_clock = lapse * sp.sqrt(1 - coupling**2 * root_squared**2 * momentum**2)
        check('source_has_zero_P0_direct_first_metric_forces', sp.diff(proper_clock, momentum).subs(momentum, 0) == 0 and sp.diff(proper_clock, mass).subs(momentum, 0) == 0)
        check('source_has_nonzero_P0_metric_Hessian', sp.simplify(sp.diff(proper_clock, momentum, 2).subs(momentum, 0) + lapse * coupling**2 * root_squared**2) == 0)
        density, sigma, root_f, log_lapse_r = sp.symbols('epsilon sigma U logN_R')
        mass_r = coupling * (root_f**2 * density + root_f * sigma)
        log_root_r = mass / (radius**2 * root_f**2) - mass_r / (radius * root_f**2)
        generator = -log_lapse_r + mass / (radius**2 * root_f**2) + coupling * density / radius
        check('source_changes_geometric_H_gradient', sp.simplify(log_lapse_r + log_root_r + generator - (2 * mass / (radius**2 * root_f**2) - coupling * sigma / (radius * root_f))) == 0)
        check('C1_geometric_coefficient_keeps_two_transport_terms', sp.simplify(-log_root_r + log_lapse_r - mass_r / (radius * root_f**2) - coupling * density / radius - generator + 2 * generator) == 0)

        times, time_weights = np.polynomial.legendre.leggauss(48)
        times, time_weights = (times + 1) / 2, time_weights / 2
        values = {'R': 6.1, 'N': .83 + .02 * times, 'mu': 1 + .01 * times, 'P': .12 + .02 * times,
                  'E': .02 + .003 * times, 'theta': .04 + .8 * times + .01 * times**2,
                  'theta_rate': .8 + .02 * times, 'chi': .02 + .03 * times, 'lambda': .07 + .01 * times}
        directions = {'N': .03 * (1 + times), 'mu': .02 * (1 - times), 'P': .04 * np.sin(times + .3),
                      'E': .01 * (1 + times**2), 'theta': times**2 * (1 - times)**2,
                      'theta_rate': 2 * times * (1 - times)**2 - 2 * times**2 * (1 - times),
                      'chi': .1 * np.cos(times), 'lambda': .03 * (1 - times**2)}

        def source_action(state):
            clock = clock_factor(state['R'], state['N'], state['mu'], state['P'])
            prescribed = .02 + .03 * state['theta'] + .015 * state['theta']**2
            return time_weights @ (state['E'] * state['theta_rate'] - clock * state['E'] + clock * state['lambda'] * (state['chi'] - prescribed))

        clock = clock_factor(values['R'], values['N'], values['mu'], values['P'])
        root_squared_value = 1 - 2 * values['mu'] / values['R']
        sqrt_chart = clock / values['N']
        potential = values['E'] - values['lambda'] * (values['chi'] - .02 - .03 * values['theta'] - .015 * values['theta']**2)
        gradients = {'N': -potential * sqrt_chart,
                     'mu': -potential * values['N'] * 2 * .1**2 * root_squared_value * values['P']**2 / (values['R'] * sqrt_chart),
                     'P': potential * values['N'] * .1**2 * root_squared_value**2 * values['P'] / sqrt_chart,
                     'E': values['theta_rate'] - clock,
                     'theta': -clock * values['lambda'] * (.03 + .03 * values['theta']),
                     'chi': clock * values['lambda'],
                     'lambda': clock * (values['chi'] - .02 - .03 * values['theta'] - .015 * values['theta']**2)}
        for variable in ['N', 'mu', 'P', 'E', 'theta', 'chi', 'lambda']:
            changed = dict(values)
            changed[variable] = values[variable] + 1e-24j * directions[variable]
            expected = time_weights @ (gradients[variable] * directions[variable])
            if variable == 'theta':
                changed['theta_rate'] = values['theta_rate'] + 1e-24j * directions['theta_rate']
                expected += time_weights @ (values['E'] * directions['theta_rate'])
                integrated = time_weights @ ((-.003 + gradients['theta']) * directions['theta'])
                check('clock_energy_equation_from_compact_variation', abs(expected - integrated) < 1e-12)
            error = float(abs(source_action(changed).imag / 1e-24 - expected))
            check('source_action_variation_' + variable, error < 1e-11, error)
            report['action_variations'].append({'variable': variable, 'absolute_error': error})
        changed = dict(values)
        changed['theta'] = values['theta'] + 1e-24j * times
        changed['theta_rate'] = values['theta_rate'] + 1e-24j
        direct = source_action(changed).imag / 1e-24
        bulk = time_weights @ ((-.003 + gradients['theta']) * times)
        check('clock_temporal_boundary_energy_term_retained', abs(direct - bulk - .023) < 1e-12 and abs(direct - bulk) > .02)

        prior_cases = json.loads((intake / 'annular-finite-width-boundary-cut-attempt01/status.json').read_text())['cases']
        for prior in prior_cases:
            branch, index = prior['branch'], prior['case']
            source_path = root / 'source-intake/navier-stokes/20260912/annular-interface-layer-clock-attempt03' / (branch + '_source_snapshot.npz')
            prepared_path = intake / 'annular-finite-width-boundary-cut-attempt01' / (branch + '_' + str(index) + '_prepared_collar.npz')
            history_path = root / 'source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02' / ('canonical_N16_' + branch + '_sample0.npz')
            with np.load(source_path, allow_pickle=False) as archive:
                source = {key: archive[key].copy() for key in archive.files}
            with np.load(prepared_path, allow_pickle=False) as archive:
                prepared = {key: archive[key].copy() for key in archive.files}
            with np.load(history_path, allow_pickle=False) as archive:
                clock_history = archive['affine_clock'].copy()
                acceleration = float(archive['endpoint_acceleration'][-1])
            for path in [source_path, prepared_path, history_path]:
                own(path)
            for budget in ([.001, .002] if index == 0 else [.001]):
                label = branch + '_' + str(index) + '_' + str(budget)
                preparation = ClockReservoirPreparation(source, branch != 'GR', prepared['kinetic_seed'], float(prepared['outer_clock']), prepared['drive'], prior['width'], prior['shape'], reservoir_energy=budget)
                coefficients, model, root_diagnostic = preparation.solve()
                driver = ProperClockDrive(model, float(clock_history[1]), acceleration)
                first, second = driver.checks(24), driver.checks(40)
                center = driver.layer([0.])
                offsets, weights = np.polynomial.legendre.leggauss(40)
                layer = driver.layer(offsets / 2)
                endpoint = model.metric(model.radii[[0, -1]])
                source_boundary_error = float(max(abs(endpoint['mu'][0] - source['mu'][0]), abs(endpoint['N'][-1] / endpoint['U'][-1] - clock_history[0]), abs(center['q'][0] - prepared['drive'][2]), abs(first['endpoint_mu1'][0] - prepared['drive'][0]), abs(endpoint['P1']).max()))
                constraint_error = float(max(abs(first['C0']).max(), abs(second['C0']).max(), abs(first['C1']).max(), abs(second['C1']).max()))
                source_balance = float(max(abs(first['source_exchange']).max(), abs(second['source_exchange']).max()))
                acceleration_error = float(max(abs(center['driven_q1'][0] - acceleration), abs(layer['driven_q1'] - layer['prescribed_q1']).max()))
                check(label + '_initial_boundaries_reprepared_including_source_mass', source_boundary_error < 1e-10, source_boundary_error)
                check(label + '_unrestricted_C0_C1_with_finite_width_source', constraint_error < 1e-10, constraint_error)
                check(label + '_derived_source_energy_exchange', source_balance < 1e-10, source_balance)
                check(label + '_prescribed_acceleration_recovered_not_predicted', acceleration_error < 1e-10, acceleration_error)
                check(label + '_omitted_source_mass_or_work_fails', abs(second['omit_initial_reservoir_C0']).max() > 1e-7 and abs(second['omit_reservoir_energy_rate_C1']).max() > 1e-6 and abs(second['omit_scalar_force_C1']).max() > 1e-6)
                check(label + '_free_acceleration_failure_not_erased', abs(center['free_q1'][0] - acceleration) > 1)
                step = 1e-24j
                changed_u = np.sqrt(1 - 2 * (endpoint['mu'][-1] + step * center['mu1'][0]) / model.radii[-1])
                changed_n = endpoint['N'][-1] * (1 + step * driver.log_lapse_rate)
                changed_p = center['p'][0] + step * center['driven_p1'][0]
                independent_acceleration = (changed_n * changed_u * changed_p / model.radii[-1]**2).imag / step.imag
                check(label + '_independent_moving_geometry_acceleration', abs(independent_acceleration - acceleration) < 1e-10, float(independent_acceleration))
                locations, quadrature_weights = model.quadrature(40)
                geometry = model.metric(locations)
                edges = model.metric(model.edges[[0, -1]])
                log_ratio = np.log((edges['N'] * edges['U'] * np.exp(edges['g']))[1] / (edges['N'] * edges['U'] * np.exp(edges['g']))[0])
                bare_integral = 2 * quadrature_weights @ (geometry['mu'] / (locations**2 * geometry['U']**2))
                source_integral = quadrature_weights @ (model.coupling * model.reservoir_density(locations) / (locations * geometry['U']))
                check(label + '_modified_geometric_weight_not_old_frozen_law', abs(log_ratio - bare_integral + source_integral) < 1e-10 and source_integral > 1e-6)
                row = {'label': label, 'branch': branch, 'case': index, 'width': prior['width'], 'shape': prior['shape'], 'reservoir_energy': budget,
                       'coefficients': coefficients.tolist(), 'root': root_diagnostic, 'initial_boundary_error': source_boundary_error,
                       'maximum_C0': float(max(abs(first['C0']).max(), abs(second['C0']).max())),
                       'maximum_C1': float(max(abs(first['C1']).max(), abs(second['C1']).max())),
                       'source_exchange_error': source_balance, 'acceleration_error': acceleration_error,
                       'free_acceleration': float(center['free_q1'][0]), 'driven_acceleration': float(center['driven_q1'][0]),
                       'required_force_center': float(center['rho'][0]), 'reservoir_energy_rate_center': float(center['reservoir_E1'][0]),
                       'proper_acceleration_extension': float(driver.proper_acceleration), 'log_lapse_rate': float(driver.log_lapse_rate),
                       'minimum_F': float((second['U']**2).min()), 'outer_mass': float(endpoint['mu'][-1]),
                       'outer_mass_rate': float(center['mu1'][0]), 'source_geometric_integral': float(source_integral),
                       'omit_source_energy_rate_error': float(abs(second['omit_reservoir_energy_rate_C1']).max()),
                       'omit_initial_source_energy_error': float(abs(second['omit_initial_reservoir_C0']).max()),
                       'source_direct_mu2_term_max': float(abs(second['source_direct_mu2_term']).max()),
                       'instantaneous_budget_over_loss_rate_not_lifetime': float(np.min(budget / np.maximum(-layer['reservoir_E1'], 1e-30))),
                       'positive_energy_only_initial_not_evolved': True, 'force_is_reaction_not_prediction': True}
                report['cases'].append(row)
                path = destination / (label + '_source_coupled_initial.npz')
                np.savez_compressed(path, **second, coefficients=coefficients, offsets=offsets / 2,
                                    **{'layer_' + key: value for key, value in layer.items()})
                own(path, 'outputs')
                save()
                print(json.dumps(row), flush=True)
        check('eight_matched_source_coupled_preparations', len(report['cases']) == 8)
        check('positive_source_energy_is_not_zero_energy_free_force', all(row['reservoir_energy'] > 0 and row['reservoir_energy_rate_center'] < 0 for row in report['cases']))
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
