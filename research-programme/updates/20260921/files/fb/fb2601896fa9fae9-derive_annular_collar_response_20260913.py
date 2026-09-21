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
    from annular_finite_width_boundary_cut_20260913 import CutPreparation
    from annular_collar_response_20260913 import frozen_response_matrices, free_response_control, driven_response_control, physical_outer_acceleration

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260913'
    destination = intake / 'annular-collar-response-attempt01'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'checks': [], 'inputs': {}, 'outputs': {}, 'responses': [], 'physical_boundaries': [],
              'valid_for_physics_claim': False, 'full_first_jet_closed': False, 'full_GR_limit_proven': False,
              'full_physical_radial_port_action_signed': False, 'boundary_histories_complete': False,
              'full_C2_evaluated': False, 'new_spacetime_evolution': False,
              'unique_parent_regularizer_derived': False, 'retarded_kernel_is_standalone_single_history_action': False,
              'point_force_adopted': False, 'frozen_scalar_reservoir_response_derived': True,
              'frozen_scalar_ODE_control_not_full_geometric_evolution': True,
              'initial_reservoir_data_retained': True, 'manufactured_forced_reservoir_control': True}

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
        previous_path = intake / 'annular-finite-width-boundary-cut-final-integrity.json'
        previous = json.loads(previous_path.read_text())
        check('previous_initial_boundary_seal_complete_without_history_promotion', previous['state'] == 'complete' and not previous['boundary_histories_complete'])
        for table in ['inputs', 'outputs']:
            for filename, expected in previous[table].items():
                if filename in report['inputs']:
                    if report['inputs'][filename] != expected:
                        raise RuntimeError('Conflicting inherited evidence: ' + filename)
                    continue
                if hashlib.sha256((root / filename).read_bytes()).hexdigest() != expected:
                    raise RuntimeError('Changed evidence: ' + filename)
                report['inputs'][filename] = expected
        own(previous_path)
        for path in [Path(__file__), root / 'scripts/annular_collar_response_20260913.py']:
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
            executed = destination / ('executed-' + path.name)
            executed.write_bytes(path.read_bytes())
            own(executed, 'outputs')
        log_n, geometric, source, log_u, connection = sp.symbols('log_N_R A B log_U_R g_R', real=True)
        check('geometric_weight_lapse_and_density_cancellation', sp.expand((log_n + log_u + connection).subs({log_u: geometric - source, connection: -log_n + geometric + source}) - 2 * geometric) == 0)
        radius, lapse, mass, root_f, clock, clock_rate, mass_rate, scalar_velocity, momentum, momentum_rate = sp.symbols('R N mu U C C1 mu1 q p p1', positive=True)
        log_lapse_rate = clock_rate / clock - mass_rate / (radius * root_f**2)
        kinetic_rate = (log_lapse_rate - mass_rate / (radius * root_f**2)) * scalar_velocity + lapse * root_f * momentum_rate / radius**2
        expected_rate = (clock_rate / clock - 2 * mass_rate / (radius * root_f**2)) * scalar_velocity + lapse * root_f * momentum_rate / radius**2
        check('outer_clock_and_kinetic_law_second_order_compatibility', sp.simplify(kinetic_rate - expected_rate) == 0)
        prior_directory = intake / 'annular-finite-width-boundary-cut-attempt01'
        prior = json.loads((prior_directory / 'status.json').read_text())
        for case in prior['cases']:
            branch, index = case['branch'], case['case']
            name = branch + '_' + str(index)
            source_path = root / 'source-intake/navier-stokes/20260912/annular-interface-layer-clock-attempt03' / (branch + '_source_snapshot.npz')
            history_path = root / 'source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02' / ('canonical_N16_' + branch + '_sample0.npz')
            with np.load(source_path, allow_pickle=False) as archive:
                source_data = {key: archive[key].copy() for key in archive.files}
            with np.load(prior_directory / (name + '_prepared_collar.npz'), allow_pickle=False) as archive:
                prepared = {key: archive[key].copy() for key in archive.files}
            with np.load(history_path, allow_pickle=False) as archive:
                clock_history, accelerations = archive['affine_clock'].copy(), archive['endpoint_acceleration'].copy()
            own(source_path)
            own(history_path)
            check(name + '_same_sourced_initial_clock', abs(clock_history[0] - prepared['outer_clock']) < 1e-13)
            preparation = CutPreparation(source_data, branch != 'GR', prepared['kinetic_seed'], float(prepared['outer_clock']), prepared['drive'], case['width'], case['shape'])
            model = preparation.build(prepared['coefficients'])
            physical = physical_outer_acceleration(model, float(clock_history[1]), float(accelerations[-1]))
            physical.update({'branch': branch, 'case': index, 'width': case['width'], 'shape': case['shape'], 'old_inner_acceleration_not_reused_after_inverse_inner_velocity_change': True})
            report['physical_boundaries'].append(physical)
            check(name + '_physical_acceleration_finite_and_unpromoted', all(np.isfinite(value) for value in physical.values() if isinstance(value, (int, float))) and not physical['point_force_adopted'])
            for offset in [-.4, -.1, .1, .4]:
                label = name + '_' + str(offset)
                data = frozen_response_matrices(model, offset)
                action_force_error = float(abs(np.exp(data['g']) * data['parent_Gchi'] + data['K'] @ data['chi0']).max())
                velocity_error = float(abs(np.exp(data['g']) * data['parent_q'] - data['H'] * model.stencil([offset])['p'][0] / data['radii']**2).max())
                check(label + '_frozen_matrix_is_action_force_not_new_coupling', max(action_force_error, velocity_error) < 1e-10)
                check(label + '_positive_mass_and_Gram_factorization', data['M'].min() > 0 and data['factor_density'].min() > 0 and abs(data['K'] - data['K'].T).max() < 1e-11)
                free, arrays = free_response_control(data)
                driven, driven_arrays = driven_response_control(data)
                check(label + '_free_retarded_response_matches_full_oscillators', max(free[key] for key in ['spectral_ODE_error', 'retarded_exterior_error', 'retarded_traction_error', 'energy_drift', 'cross_energy_power_balance_error']) < 1e-10, free)
                check(label + '_memory_requires_initial_data_and_cross_energy', free['drop_initial_reservoir_data_error'] > 1e-8 and free['drop_cross_energy_power_error'] > 1e-8)
                check(label + '_driven_response_replay_and_external_work', max(driven[key] for key in ['full_forced_replay_error', 'external_work_energy_error', 'reaction_equation_error']) < 1e-10, driven)
                row = {'branch': branch, 'case': index, 'offset': offset, 'width': case['width'], 'shape': case['shape'], 'exterior_node': data['exterior'], 'matrix_force_error': action_force_error, 'free': free, 'driven': driven}
                report['responses'].append(row)
                path = destination / (label + '_response.npz')
                np.savez_compressed(path, **{key: value for key, value in data.items() if key not in ['exterior', 'interior']}, interior=data['interior'], exterior=data['exterior'], **arrays, **{'driven_' + key: value for key, value in driven_arrays.items()})
                own(path, 'outputs')
            save()
            print(json.dumps({'case': name, 'free_outer_acceleration': physical['free_outer_acceleration'], 'prescribed_outer_acceleration': physical['prescribed_outer_acceleration'], 'acceleration_defect': physical['acceleration_defect'], 'required_force_trace_not_installed': physical['required_generalized_force_trace_not_installed'], 'frozen_responses_complete': 4}), flush=True)
        check('twenty_four_frozen_response_cases_six_physical_boundary_tests', len(report['responses']) == 24 and len(report['physical_boundaries']) == 6)
        report['free_outer_second_order_all_pass'] = all(row['free_boundary_second_order_pass'] for row in report['physical_boundaries'])
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
