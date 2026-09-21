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
    from annular_canonical_common_profile_aligned_20260912 import CommonProfile
    from annular_canonical_trace_context_20260911 import load_archive
    from annular_cubic_lapse_reference_gravity_20260912 import evaluate_cubic_initial
    from annular_frozen_second_jet_complex_20260912 import FrozenSecondJet

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260912'
    source = intake / 'annular-acceleration-trace-completion-attempt02'
    destination = intake / 'annular-history-ward-attempt01'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'checks': [], 'cases': [], 'inputs': {}, 'outputs': {}, 'valid_for_physics_claim': False, 'new_evolution': False, 'full_second_jet_closed': False, 'interval_certificate': False, 'physical_fields_or_phase_maps_changed': False, 'temporal_boundary_work_retained': True}

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
        prior_path = intake / 'annular-second-jet-final-integrity.json'
        prior = json.loads(prior_path.read_text())
        check('prior_seal_complete_without_second_jet_claim', prior['state'] == 'complete' and not prior['full_second_jet_closed'])
        inherited = dict(prior['inputs'])
        inherited.update(prior['outputs'])
        for name, expected in inherited.items():
            if hashlib.sha256((root / name).read_bytes()).hexdigest() != expected:
                raise RuntimeError('Changed immutable evidence: ' + name)
            report['inputs'][name] = expected
        for path in [prior_path, Path(__file__), root / 'DERIVATION-20260909-covariant-time-links-and-mixed-gravity-basis.md', root / 'DERIVATION-20260912-nonlinear-history-Euler-equations.md']:
            own(path)
        snapshot = destination / ('executed-' + Path(__file__).name)
        snapshot.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        radius, mu, lapse, momentum, kappa = sp.symbols('R mu N P kappa', positive=True)
        geometry = 1 - 2 * mu / radius
        shift = kappa * lapse * geometry**sp.Rational(3, 2) * momentum
        nonlinear = kappa**2 * geometry**2 * momentum**2
        connection = kappa * sp.sqrt(geometry) * momentum / (lapse * (1 - nonlinear))
        density = radius**2 * lapse * sp.sqrt(geometry) * (1 - nonlinear)
        radial_generator = {mu: radius * geometry * shift, lapse: -lapse * shift, momentum: -lapse * (1 - 3 * nonlinear) / (kappa * sp.sqrt(geometry))}
        check('metric_pullback_connection_epsilon_R', sp.simplify(sum(sp.diff(connection, variable) * value for variable, value in radial_generator.items()) + 1) == 0)
        check('metric_pullback_density_epsilon_R', sp.simplify(sum(sp.diff(density, variable) * value for variable, value in radial_generator.items())) == 0)
        check('metric_pullback_connection_epsilon_t', sp.simplify(lapse * sp.diff(connection, lapse) + connection) == 0)
        check('metric_pullback_density_epsilon_t', sp.simplify(lapse * sp.diff(density, lapse) - density) == 0)
        report['derived_memory_Ward'] = 'K_R+c*K_t+2*c_t*K+sum delta_i*(C_i*d_i,t+G_chi,i*chi_i,t)=0 in the interior physical-time window; endpoint distributions and temporal action work are retained.'
        report['derived_memory_Ward_time_P0'] = 'K_t,R+3*c_t*K_t+2*c_tt*K+sum delta_i*(C_i,t*d_i,t+C_i*d_i,tt+G_chi,i,t*chi_i,t+G_chi,i*chi_i,tt)=0.'
        report['canonical_Ward_candidate'] = 'N*C_t=E_mu*mu_t+E_P*P_t+E_chi*chi_t+E_pi*pi_t-d_R(E_mu*R*F*beta-E_P*N*(1-3u)/(kappa*sqrtF)+E_pi*T-N*beta*C). Pullback and independent weak evaluation required, not an on-shell finite-grid assertion.'
        common = CommonProfile(root)
        for branch in ['GR', 'metric_Gram']:
            for higher in [False, True]:
                variant = 'higher' if higher else 'primary'
                print('Ward source work: ' + branch + ' ' + variant, flush=True)
                model = FrozenSecondJet(common, branch, higher=higher)
                for phase in model.frames:
                    archive = load_archive(source / (branch + '_extended_' + phase + '_frames.npz'))
                    model.frames[phase] = {surface: {kind: archive[surface + '__' + kind] for kind in ['q', 'qr', 'p']} for surface in model.data}
                model.first = evaluate_cubic_initial(model.frames['mass'], model.frames['scalar'], model.data, model.basis, model.weights, model.links, model.gram, model.context.system.outer_clock, surface=model.surface, link_surface=model.link_surface)
                for surface in model.rates:
                    mass, scalar = model.frames['mass'][surface], model.frames['scalar'][surface]
                    model.rates[surface] = {'mu': mass['q'] @ model.first['mass_rate_coeff'], 'mu_r': mass['qr'] @ model.first['mass_rate_coeff'], 'P': mass['p'] @ model.first['P_rate_coeff'], 'pi': scalar['p'] @ model.first['pi_rate_coeff'], 'chi': scalar['q'] @ model.first['q_coeff'], 'w': scalar['qr'] @ model.first['q_coeff']}
                model.prepare_links()
                saved = load_archive(source / (branch + '_completed_second_jet.npz'))
                result = model.evaluate(saved['lapse_rate_coefficients'])
                coefficients = saved['lapse_rate_coefficients']
                derivative = result['current_first'], result['endpoint_Tss'], result['partial_Tss']
                prepared = {}
                for surface, values in model.data.items():
                    rates = model.rates[surface]
                    mass, scalar = model.frames['mass'][surface], model.frames['scalar'][surface]
                    second = {'mu': mass['q'] @ result['second']['mu'], 'P': mass['p'] @ result['second']['P'], 'chi': scalar['q'] @ result['second']['chi'], 'pi': scalar['p'] @ result['second']['pi'], 'mu_r': mass['qr'] @ result['second']['mu'], 'w': scalar['qr'] @ result['second']['chi']}
                    radial = values['R']
                    root_f = np.sqrt(values['F'])
                    lapse_first, lapse_radial_first = values['eta'] @ coefficients, values['eta_r'] @ coefficients
                    rate_root = -rates['mu'] / (radial * root_f)
                    energy = values['pi']**2 / (2 * radial**2) + radial**2 * values['w']**2 / 2
                    energy_first = values['pi'] * rates['pi'] / radial**2 + radial**2 * values['w'] * rates['w']
                    velocity_mu = .1 * values['N'] * values['F']**1.5 * values['pi'] * values['w']
                    velocity_mu_first = .1 * ((lapse_first * values['F']**1.5 + 3 * values['N'] * values['F'] * rate_root) * values['pi'] * values['w'] + values['N'] * values['F']**1.5 * (rates['pi'] * values['w'] + values['pi'] * rates['w']))
                    velocity_mu_first += .1 * (radial * values['F']**2.5 * values['N_r'] + values['N'] * values['F']**1.5 * (values['mu_r'] - values['mu'] / radial)) * rates['P']
                    velocity_chi = values['N'] * root_f * values['pi'] / radial**2
                    velocity_chi_first = ((lapse_first * root_f + values['N'] * rate_root) * values['pi'] + values['N'] * root_f * rates['pi']) / radial**2 + .1 * values['N'] * values['F']**1.5 * rates['P'] * values['w']
                    force_P = values['N'] * energy / (radial * root_f) - values['N_r'] / (.1 * root_f) + values['N'] * values['mu'] / (.1 * radial**2 * values['F']**1.5)
                    force_P_first = (lapse_first * energy + values['N'] * energy_first) / (radial * root_f) - values['N'] * energy * rate_root / (radial * values['F'])
                    force_P_first += -lapse_radial_first / (.1 * root_f) + values['N_r'] * rate_root / (.1 * values['F'])
                    force_P_first += (lapse_first * values['mu'] + values['N'] * rates['mu']) / (.1 * radial**2 * values['F']**1.5) - 3 * values['N'] * values['mu'] * rate_root / (.1 * radial**2 * values['F']**2)
                    force_P_first += .3 * values['N'] * root_f * rates['P'] * values['pi'] * values['w'] / radial
                    flux = values['N'] * root_f * radial**2 * values['w']
                    flux_first = radial**2 * ((lapse_first * root_f + values['N'] * rate_root) * values['w'] + values['N'] * root_f * rates['w']) + .1 * values['N'] * values['F']**1.5 * rates['P'] * values['pi']
                    test = values['eta'][:, 1:16]
                    test_r = values['eta_r'][:, 1:16]
                    clock_test = test / values['N'][:, None]
                    clock_test_r = test_r / values['N'][:, None] - test * (values['N_r'] / values['N']**2)[:, None]
                    clock_test_first = -clock_test * (lapse_first / values['N'])[:, None]
                    clock_test_radial_first = -test_r * (lapse_first / values['N']**2)[:, None] - test * (lapse_radial_first / values['N']**2 - 2 * values['N_r'] * lapse_first / values['N']**3)[:, None]
                    inv_cP = values['N'] / (.1 * root_f)
                    inv_cP_first = lapse_first / (.1 * root_f) - values['N'] * rate_root / (.1 * values['F'])
                    gauge = {'mu': clock_test * rates['mu'][:, None], 'P': clock_test * rates['P'][:, None] - clock_test_r * inv_cP[:, None], 'chi': clock_test * rates['chi'][:, None], 'pi': clock_test * rates['pi'][:, None] + clock_test_r * flux[:, None]}
                    gauge_first = {'mu': clock_test_first * rates['mu'][:, None] + clock_test * second['mu'][:, None] + clock_test_r * (.1 * radial * values['N'] * values['F']**2.5 * rates['P'])[:, None], 'P': clock_test_first * rates['P'][:, None] + clock_test * second['P'][:, None] - clock_test_radial_first * inv_cP[:, None] - clock_test_r * inv_cP_first[:, None], 'chi': clock_test_first * rates['chi'][:, None] + clock_test * second['chi'][:, None], 'pi': clock_test_first * rates['pi'][:, None] + clock_test * second['pi'][:, None] + clock_test_radial_first * flux[:, None] + clock_test_r * flux_first[:, None]}
                    gauge['chi_r'] = clock_test_r * rates['chi'][:, None] + clock_test * rates['w'][:, None]
                    gauge_first['chi_r'] = clock_test_radial_first * rates['chi'][:, None] + clock_test_first * rates['w'][:, None] + clock_test_r * second['chi'][:, None] + clock_test * second['w'][:, None]
                    prepared[surface] = {'values': values, 'rates': rates, 'second': second, 'gauge': gauge, 'gauge_first': gauge_first, 'E_mu': force_P - rates['P'], 'E_mu_first': force_P_first - second['P'], 'E_P': rates['mu'] - velocity_mu, 'E_P_first': second['mu'] - velocity_mu_first, 'E_pi': rates['chi'] - velocity_chi, 'E_pi_first': second['chi'] - velocity_chi_first, 'flux': flux, 'flux_first': flux_first, 'lapse_first': lapse_first}
                local, nodal, linked = prepared[model.surface], prepared['nodes'], prepared[model.link_surface]
                values, nodes = local['values'], nodal['values']
                weights = model.weights
                contributions = {}
                for phase in ['mu', 'P', 'pi']:
                    contributions['local_' + phase] = local['gauge'][phase].T @ (weights * local['E_' + phase + '_first']) + local['gauge_first'][phase].T @ (weights * local['E_' + phase])
                contributions['local_chi'] = -local['gauge']['chi'].T @ (weights * local['second']['pi']) - local['gauge_first']['chi'].T @ (weights * local['rates']['pi']) - local['gauge']['chi_r'].T @ (weights * local['flux_first']) - local['gauge_first']['chi_r'].T @ (weights * local['flux'])
                signs = np.array([-1., 1.])
                boundary_mass_first = .1 * nodes['R'] * nodes['N'] * nodes['F']**2.5 * nodal['rates']['P']
                contributions['mass_P_boundary'] = -nodal['gauge']['P'][[0, -1]].T @ (signs * boundary_mass_first[[0, -1]])
                contributions['scalar_flux_boundary'] = nodal['gauge']['chi'][[0, -1]].T @ (signs * nodal['flux_first'][[0, -1]]) + nodal['gauge_first']['chi'][[0, -1]].T @ (signs * nodal['flux'][[0, -1]])
                if model.gram:
                    link_values, link_rates = linked['values'], linked['rates']
                    cP = .1 * np.sqrt(link_values['F']) / link_values['N']
                    alpha = -link_rates['mu'] / (link_values['R'] * link_values['F']) - linked['lapse_first'] / link_values['N']
                    cMu_first = -.1 * link_rates['P'] / (link_values['R'] * link_values['N'] * np.sqrt(link_values['F']))
                    dvalue, dfirst, dsecond = model.nodal_density, model.nodal_density_first, result['gram_density_second']
                    Cmu = -nodes['R'] * nodes['N'] / np.sqrt(nodes['F'])
                    Cmu_first = -nodes['R'] * (nodal['lapse_first'] / np.sqrt(nodes['F']) + nodes['N'] * nodal['rates']['mu'] / (nodes['R'] * nodes['F']**1.5))
                    CP_first = -2 * .1**2 * nodes['R']**2 * nodes['N'] * nodes['F']**2.5 * nodal['rates']['P']
                    contributions['memory_mu_regular'] = model.transport_load(linked['gauge']['mu'], cMu_first)
                    contributions['memory_mu_nodes'] = -nodal['gauge']['mu'].T @ (dfirst * Cmu + dvalue * Cmu_first) - nodal['gauge_first']['mu'].T @ (dvalue * Cmu)
                    contributions['memory_P_regular'] = model.transport_load(linked['gauge']['P'], cP, derivative) + model.transport_load(linked['gauge']['P'], cP * alpha) + model.transport_load(linked['gauge_first']['P'], cP)
                    contributions['memory_P_nodes'] = -nodal['gauge']['P'].T @ (dvalue * CP_first)
                    contributions['memory_chi_nodes'] = nodal['gauge']['chi'].T @ result['gram_scalar_first'] + nodal['gauge_first']['chi'].T @ model.first['gram_scalar']
                    contributions['memory_chi_boundary_reaction'] = -nodal['gauge']['chi'][[0, -1]].T @ result['gram_scalar_first'][[0, -1]] - nodal['gauge_first']['chi'][[0, -1]].T @ model.first['gram_scalar'][[0, -1]]
                    test, test_r = link_values['eta'], link_values['eta_r']
                    generator = cP * link_rates['P']
                    csecond = cP * (linked['second']['P'] + 2 * alpha * link_rates['P'])
                    Cvalue = model.coefficient
                    Cfirst = nodes['R']**2 * (nodal['lapse_first'] * np.sqrt(nodes['F']) - nodes['N'] * nodal['rates']['mu'] / (nodes['R'] * np.sqrt(nodes['F'])))
                    node_work = Cvalue * dfirst + model.first['gram_scalar'] * nodal['rates']['chi']
                    node_work_first = Cfirst * dfirst + Cvalue * dsecond + result['gram_scalar_first'] * nodal['rates']['chi'] + model.first['gram_scalar'] * nodal['second']['chi']
                    ward_zero = -model.transport_load(test_r, np.ones_like(generator)) + model.transport_load(test, 2 * generator) + nodes['eta'].T @ node_work
                    ward_one = -model.transport_load(test_r, np.ones_like(generator), derivative) + model.transport_load(test, 3 * generator, derivative) + model.transport_load(test, 2 * csecond) + nodes['eta'].T @ node_work_first
                    check(variant + '_memory_Ward_including_endpoint_distributions', abs(ward_zero).max() < 1e-8, float(abs(ward_zero).max()))
                    check(variant + '_differentiated_memory_Ward_including_inverse_time', abs(ward_one).max() < 1e-8, float(abs(ward_one).max()))
                    wrong_one = ward_one - model.transport_load(test, generator, derivative)
                    report.setdefault('memory_identity_cases', []).append({'variant': variant, 'Ward0_max': float(abs(ward_zero).max()), 'Ward1_max': float(abs(ward_one).max()), 'wrong_two_instead_of_three_max': float(abs(wrong_one).max())})
                energy = values['pi']**2 / (2 * values['R']**2) + values['R']**2 * values['w']**2 / 2
                Cbulk = values['mu_r'] / (.1 * np.sqrt(values['F'])) - np.sqrt(values['F']) * energy
                zeta = .1 * (values['F']**1.5 * local['rates']['P'])[:, None] * (values['eta'][:, 1:16] * values['N_r'][:, None] - values['eta_r'][:, 1:16] * values['N'][:, None])
                transported_constraint = zeta.T @ (weights * Cbulk)
                if model.gram:
                    node_zeta = .1 * (nodes['F']**1.5 * nodal['rates']['P'])[:, None] * (nodes['eta'][:, 1:16] * nodes['N_r'][:, None] - nodes['eta_r'][:, 1:16] * nodes['N'][:, None])
                    transported_constraint -= node_zeta.T @ (nodes['R']**2 * np.sqrt(nodes['F']) * model.nodal_density)
                work = sum(contributions.values())
                actual = result['constraint_second'][1:16]
                record = {'branch': branch, 'variant': variant, 'compact_test_count': 15, 'actual_Cddot_max': float(abs(actual).max()), 'transported_constraint_max': float(abs(transported_constraint).max()), 'Euler_source_work_max': float(abs(work).max()), 'full_Ward_prediction_error': float(abs(actual - transported_constraint - work).max()), 'contribution_maxima': {name: float(abs(value).max()) for name, value in contributions.items()}, 'compact_only_not_all_nineteen_boundary_rows': True}
                report['cases'].append(record)
                path = destination / (branch + '_' + variant + '_ward_source_work.npz')
                np.savez_compressed(path, actual=actual, transported_constraint=transported_constraint, Euler_source_work=work, unexplained=actual - transported_constraint - work, **contributions)
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
        print(json.dumps({'state': report['state'], 'checks': len(report['checks'])}), flush=True)
    except Exception as error:
        report.update({'state': 'failed', 'error': repr(error), 'traceback': traceback.format_exc()})
        save()
        raise


if __name__ == '__main__':
    run()
