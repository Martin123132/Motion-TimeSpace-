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
    from annular_clock_reservoir_coupling_20260913 import ClockReservoirPreparation, ProperClockDrive
    from annular_source_second_jet_20260913 import SourceSecondJet

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260913'
    destination = intake / 'annular-source-second-jet-attempt01'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'checks': [], 'inputs': {}, 'outputs': {}, 'cases': [], 'constant_lapse_controls': [],
              'full_C2_evaluated': True, 'valid_for_physics_claim': False, 'full_GR_limit_proven': False,
              'full_geometric_evolution': False, 'boundary_histories_complete': False, 'full_first_jet_closed': False,
              'apparatus_microphysics_derived': False, 'unique_parent_regularizer_derived': False,
              'source_support_stresses_derived': False, 'full_physical_radial_port_action_signed': False,
              'new_fundamental_MTS_field_claimed': False, 'point_force_adopted': False,
              'second_jet_is_formal_two_sided_time_germ': True, 'N2_is_not_needed_for_C2_or_reaction_rate': True}

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
        previous_path = intake / 'annular-clock-reservoir-coupling-final-integrity.json'
        previous = json.loads(previous_path.read_text())
        check('previous_source_coupling_complete', previous['state'] == 'complete' and previous['full_C2_evaluated'] is False)
        for table in ['inputs', 'outputs']:
            for filename, expected in previous[table].items():
                if filename in report['inputs'] and report['inputs'][filename] != expected:
                    raise RuntimeError('Conflicting inherited hash: ' + filename)
                if filename not in report['inputs']:
                    if hashlib.sha256((root / filename).read_bytes()).hexdigest() != expected:
                        raise RuntimeError('Changed evidence: ' + filename)
                    report['inputs'][filename] = expected
        own(previous_path)
        for path in [Path(__file__), root / 'scripts/annular_source_second_jet_20260913.py']:
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
            executed = destination / ('executed-' + path.name)
            executed.write_bytes(path.read_bytes())
            own(executed, 'outputs')
        radius, root_f, lapse, lapse_r, coupling, density, sigma, mass, momentum_rate = sp.symbols('R U N Nr kappa epsilon sigma mu P1', positive=True)
        mass_r = coupling * (root_f**2 * density + root_f * sigma)
        gravity = coupling * radius * root_f**3 * (root_f**2 * lapse_r + lapse * mass_r / radius - lapse * mass / radius**2)
        explicit = gravity - 2 * coupling**2 * lapse * root_f**5 * density - coupling**2 * lapse * root_f**4 * sigma
        p_first = -lapse_r / (coupling * root_f) + lapse * mass / (coupling * radius**2 * root_f**3) + lapse * density / (radius * root_f)
        check('full_source_scalar_gravity_mu2_coefficient_simplifies', sp.simplify(explicit + coupling**2 * radius * root_f**6 * p_first) == 0)
        mass_rate, epsilon_rate, log_lapse_rate, log_lapse_r = sp.symbols('mu1 eps1 L Lr')
        f_mu = -lapse_r / (coupling * radius * root_f**3) + lapse / (coupling * radius**2 * root_f**3) + 3 * lapse * mass / (coupling * radius**3 * root_f**5) + lapse * density / (radius**2 * root_f**3)
        p_second = log_lapse_rate * p_first - lapse * log_lapse_r / (coupling * root_f) + f_mu * mass_rate + lapse * epsilon_rate / (radius * root_f) + mass_rate * p_first / (radius * root_f**2)
        c_second = coupling * root_f / lapse * (p_second - 2 * (mass_rate / (radius * root_f**2) + log_lapse_rate) * p_first)
        expected = mass_rate / (radius**2 * root_f**4) + coupling * epsilon_rate / radius - log_lapse_r - log_lapse_rate * coupling * root_f * p_first / lapse
        check('c_tt_simplifies_with_full_transport_metric_term', sp.simplify((c_second - expected).subs(mass, radius * (1 - root_f**2) / 2)) == 0)

        prior = json.loads((intake / 'annular-clock-reservoir-coupling-attempt01/status.json').read_text())
        for source_row in prior['cases']:
            branch, index, label = source_row['branch'], source_row['case'], source_row['label']
            source_path = root / 'source-intake/navier-stokes/20260912/annular-interface-layer-clock-attempt03' / (branch + '_source_snapshot.npz')
            prepared_path = intake / 'annular-finite-width-boundary-cut-attempt01' / (branch + '_' + str(index) + '_prepared_collar.npz')
            history_path = root / 'source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02' / ('canonical_N16_' + branch + '_sample0.npz')
            with np.load(source_path, allow_pickle=False) as archive:
                source = {key: archive[key].copy() for key in archive.files}
            with np.load(prepared_path, allow_pickle=False) as archive:
                prepared = {key: archive[key].copy() for key in archive.files}
            with np.load(history_path, allow_pickle=False) as archive:
                clock = archive['affine_clock'].copy()
                target_acceleration = float(archive['endpoint_acceleration'][-1])
            preparation = ClockReservoirPreparation(source, branch != 'GR', prepared['kinetic_seed'], float(prepared['outer_clock']), prepared['drive'], source_row['width'], source_row['shape'], reservoir_energy=source_row['reservoir_energy'])
            model = preparation.build(np.asarray(source_row['coefficients']))
            driver = ProperClockDrive(model, float(clock[1]), target_acceleration)
            jet = SourceSecondJet(model, driver)
            outputs = [jet.check_second(order) for order in [24, 40]]
            maximum_c2 = float(max(abs(result['C2']).max() for result in outputs))
            maximum_ward = float(max(abs(result['ward1']).max() for result in outputs))
            endpoint_error = float(max(abs(result['endpoint_P2']).max() for result in outputs))
            higher = outputs[-1]
            metric = jet.first_fields(higher['R'])
            radius_value, root_value, lapse_value = higher['R'], metric['U'], metric['N']
            lapse_radial = lapse_value * (metric['mu'] / (radius_value**2 * root_value**2) + model.coupling * metric['epsilon'] / radius_value - metric['g_r'])
            mass_derivative = -lapse_radial / (model.coupling * radius_value * root_value**3) + lapse_value / (model.coupling * radius_value**2 * root_value**3) + 3 * lapse_value * metric['mu'] / (model.coupling * radius_value**3 * root_value**5) + lapse_value * metric['epsilon'] / (radius_value**2 * root_value**3)
            direct_p2 = metric['L'] * metric['P1'] - lapse_value * metric['L_r'] / (model.coupling * root_value) + mass_derivative * metric['mu1'] + lapse_value * metric['epsilon1'] / (radius_value * root_value) + metric['mu1'] * metric['P1'] / (radius_value * root_value**2)
            check(label + '_P2_matches_unsimplified_metric_equations', abs(direct_p2 - metric['P2']).max() < 1e-10)
            check(label + '_finite_full_second_jet', all(np.isfinite(value).all() for output in outputs for value in output.values()))
            check(label + '_c2_recorded_without_forcing_acceptance', np.isfinite(maximum_c2) and np.isfinite(maximum_ward))
            check(label + '_natural_P2_boundary_derived', endpoint_error < 1e-10)
            initial = jet.completed_layer([0.])
            row = {'label': label, 'branch': branch, 'case': index, 'width': source_row['width'], 'shape': source_row['shape'], 'reservoir_energy': source_row['reservoir_energy'],
                   'maximum_C2': maximum_c2, 'maximum_differentiated_Ward': maximum_ward, 'maximum_endpoint_P2': endpoint_error,
                   'C2_pass': maximum_c2 < 1e-10, 'P2_boundary_pass': endpoint_error < 1e-10,
                   'quadrature_C2_difference': float(abs(outputs[0]['C2'] - higher['C2']).max()),
                   'primitive_fit_error': jet.primitive_max_fit_error,
                   'lapse_rate_slopes': jet.lapse_slopes.tolist(), 'maximum_log_lapse_rate': float(abs(metric['L']).max()),
                   'required_inner_mass_acceleration': float(higher['endpoint_mu2'][0]), 'derived_outer_mass_acceleration': float(higher['endpoint_mu2'][1]),
                   'source_force_rate_at_cut': float(initial['rho1'][0]), 'source_energy_second_at_cut': float(initial['reservoir_E2'][0]),
                   'omit_source_C2': float(abs(higher['no_source_C2']).max()), 'omit_connection_C2': float(abs(higher['no_connection_C2']).max()),
                   'omit_P_squared_C2': float(abs(higher['no_P_squared_C2']).max()), 'omit_radial_C2': float(abs(higher['no_radial_C2']).max()),
                   'source_prescribed_acceleration_error': float(abs(initial['q1'][0, -1] - target_acceleration)),
                   'inner_mass_acceleration_is_output_not_unsourced_zero': True}
            report['cases'].append(row)
            path = destination / (label + '_second_jet.npz')
            np.savez_compressed(path, **higher, lower_C2=outputs[0]['C2'],
                                **{'center_' + key: value for key, value in initial.items() if isinstance(value, np.ndarray)})
            own(path, 'outputs')
            if index == 0 and source_row['reservoir_energy'] == .001:
                constant = SourceSecondJet(model, driver, correct_boundary_slopes=False)
                comparison = constant.check_second(24)
                report['constant_lapse_controls'].append({'branch': branch, 'maximum_C2': float(abs(comparison['C2']).max()), 'maximum_endpoint_P2': float(abs(comparison['endpoint_P2']).max()), 'adopted': False})
                check(branch + '_constant_lapse_rate_misses_second_boundary', abs(comparison['endpoint_P2']).max() > 1e-5)
                path = destination / (branch + '_constant_lapse_second_jet.npz')
                np.savez_compressed(path, **comparison)
                own(path, 'outputs')
            save()
            print(json.dumps(row), flush=True)
        for module in tuple(sys.modules.values()):
            filename = getattr(module, '__file__', None)
            if filename:
                path = Path(filename).resolve()
                if path.parent == root / 'scripts' and path.suffix == '.py':
                    own(path)
        check('eight_source_second_jets_complete', len(report['cases']) == 8)
        check('no_python_cache', not (root / 'scripts/__pycache__').exists())
        report['C2_all_pass'] = all(row['C2_pass'] for row in report['cases'])
        report['P2_boundary_all_pass'] = all(row['P2_boundary_pass'] for row in report['cases'])
        report['state'] = 'complete'
        save()
    except Exception as error:
        report.update({'state': 'failed', 'error': repr(error), 'traceback': traceback.format_exc()})
        save()
        raise


if __name__ == '__main__':
    run()
