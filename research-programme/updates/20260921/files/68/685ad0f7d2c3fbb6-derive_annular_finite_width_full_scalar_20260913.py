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
    from annular_nonlinear_history_20260912 import ManufacturedHistory
    from annular_covariant_scalar_action_20260912 import TimePullbackHistory
    from annular_finite_width_full_scalar_20260913 import FiniteWidthScalar, TranslatedScalarAction, LayerModeHistory, ZeroShiftHistory, proper_clock_integral, covariance_control

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260913'
    intake.mkdir(exist_ok=True)
    destination = intake / 'annular-finite-width-full-scalar-attempt01'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'checks': [], 'inputs': {}, 'outputs': {}, 'variation_cases': [],
              'proper_clock_cases': [], 'covariance_cases': [], 'point_limit_cases': [],
              'energy_density_cases': [], 'layer_mode_cases': [], 'valid_for_physics_claim': False,
              'new_spacetime_evolution': False, 'full_first_jet_closed': False, 'full_GR_limit_proven': False,
              'unique_parent_regularizer_derived': False, 'full_physical_radial_port_action_signed': False,
              'off_shell_complete_quadratic_scalar_regularization_constructed': True,
              'gravity_bulk_action_unchanged_not_replaced': True,
              'expanded_scalar_layer_phase_not_identical_to_old_17_pairs': True,
              'nominal_h_and_all_Gram_weights_unchanged': True,
              'manufactured_history_tests_not_coupled_initial_data': True,
              'common_translation_not_single_node_jitter': True}
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
        previous_path = root / 'source-intake/navier-stokes/20260912/annular-interface-layer-clock-final-integrity.json'
        previous = json.loads(previous_path.read_text())
        check('previous_layer_seal_complete_without_action_promotion', previous['state'] == 'complete' and not previous['full_scalar_action_descent_proven'])
        for table in ['inputs', 'outputs']:
            for name, expected in previous[table].items():
                if name in report['inputs']:
                    continue
                if hashlib.sha256((root / name).read_bytes()).hexdigest() != expected:
                    raise RuntimeError('Changed inherited evidence: ' + name)
                report['inputs'][name] = expected
        own(previous_path)
        for path in [Path(__file__), root / 'scripts/annular_finite_width_full_scalar_20260913.py']:
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
            snapshot = destination / ('executed-' + path.name)
            snapshot.write_bytes(path.read_bytes())
            own(snapshot, 'outputs')
        radius, root_f, lapse, momentum, coupling = sp.symbols('R U N P kappa', positive=True)
        chart = 1 - coupling**2 * root_f**4 * momentum**2
        clock_lapse = lapse * sp.sqrt(chart)
        radial_scale = 1 / (root_f * sp.sqrt(chart))
        connection = coupling * root_f * momentum / (lapse * chart)
        coefficient = radius**2 * lapse * root_f * chart
        shift = coupling * lapse * root_f**3 * momentum
        check('exact_metric_coframe', sp.simplify(-clock_lapse**2 + lapse**2 - shift**2 / root_f**2) == 0 and sp.simplify(clock_lapse**2 * connection - shift / root_f**2) == 0 and sp.simplify(radial_scale**2 - clock_lapse**2 * connection**2 - 1 / root_f**2) == 0)
        check('radial_measure_owns_scalar_clock_density', sp.simplify(coefficient - radius**2 * clock_lapse / radial_scale) == 0 and sp.simplify(radius**4 / coefficient - radius**2 * radial_scale / clock_lapse) == 0)
        proper_velocity, auxiliary, weight, chi_prime, time_prime, p_prime = sp.symbols('v p omega chi_prime t_prime p_prime')
        proper_hamiltonian = weight * auxiliary**2 / (2 * radius**2 * radial_scale)
        check('auxiliary_proper_clock_Legendre_pair', sp.simplify((weight * auxiliary * proper_velocity - proper_hamiltonian).subs(auxiliary, radius**2 * radial_scale * proper_velocity) - weight * radius**2 * radial_scale * proper_velocity**2 / 2) == 0)
        density_symbol = sp.symbols('C')
        derivative_H = weight * density_symbol * auxiliary / radius**4
        E_clock = derivative_H * p_prime
        E_chi = -weight * p_prime
        E_p = weight * chi_prime - time_prime * derivative_H
        check('parametrized_kinetic_clock_identity_off_shell', sp.expand(time_prime * E_clock + chi_prime * E_chi + p_prime * E_p) == 0)
        scale, velocity, delta_scale_first, delta_scale_second, delta_velocity_first, delta_velocity_second, delta_chi_first, delta_chi_second = sp.symbols('a v da1 da2 dv1 dv2 dx1 dx2')
        dp_first = radius**2 * (scale * delta_velocity_first + velocity * delta_scale_first)
        dp_second = radius**2 * (scale * delta_velocity_second + velocity * delta_scale_second)
        symplectic = dp_first * delta_chi_second - dp_second * delta_chi_first
        expected = radius**2 * scale * (delta_velocity_first * delta_chi_second - delta_velocity_second * delta_chi_first) + radius**2 * velocity * (delta_scale_first * delta_chi_second - delta_scale_second * delta_chi_first)
        check('radial_measure_mixed_symplectic_term_retained', sp.expand(symplectic - expected) == 0)
        check('dropping_mixed_symplectic_term_is_not_identity', sp.expand(symplectic - radius**2 * scale * (delta_velocity_first * delta_chi_second - delta_velocity_second * delta_chi_first)) != 0)
        history = ManufacturedHistory(soluble=False)
        width = 1 / 128
        directions = list(np.eye(4)) + [np.ones(4)]
        for gram in [False, True]:
            branch = 'GR' if not gram else 'metric_Gram'
            averaged = FiniteWidthScalar(history, gram, width)
            reference = TranslatedScalarAction(history, gram)
            check(branch + '_positive_normalized_average', abs(averaged.weights.sum() - 1) < 1e-14 and averaged.weights.min() > 0)
            check(branch + '_same_stencil_and_kinetic_weights_all_layers', all(np.array_equal(action.factors, reference.factors) and np.array_equal(action.sampling, reference.sampling) and np.array_equal(action.node_weights, reference.node_weights) and action.spacing == reference.spacing and np.max(abs(np.diff(action.radii) - reference.spacing)) < 1e-14 for action in averaged.actions))
            if gram:
                errors = [float(abs(action.factors[16:] @ action.radii**power).max()) for action in averaged.actions for power in [0, 1, 2]]
                jittered = reference.radii.copy()
                jittered[8] += width / 2
                negative = float(abs(reference.factors[16:] @ jittered**2).max())
                check('translation_preserves_Gram_polynomial_kernel_jitter_does_not', max(errors) < 1e-10 and negative > 1e-5, {'translation_error': max(errors), 'single_node_jitter_error': negative})
            for index, direction in enumerate(directions):
                actual = averaged.integrated(direction)
                differences = []
                for step in [2e-4, 1e-4]:
                    plus = averaged.integrated(direction, step)['action']
                    minus = averaged.integrated(direction, -step)['action']
                    differences.append((plus - minus) / (2 * step))
                extrapolated = (4 * differences[-1] - differences[0]) / 3
                row = {'branch': branch, 'direction': direction.tolist(), 'action_derivative_error': float(abs(extrapolated - actual['raw'])), 'adjoint_with_temporal_boundaries_error': float(abs(actual['raw'] - actual['adjoint'])), **actual}
                check(branch + '_full_action_variation_' + str(index), max(row['action_derivative_error'], row['adjoint_with_temporal_boundaries_error']) < 1e-8, row)
                check(branch + '_positive_chart_' + str(index), min(row['minimum_F'], row['minimum_chart_d'], row['minimum_J']) > 0 and row['maximum_nonzero_P'] > .1)
                report['variation_cases'].append(row)
                print(json.dumps({'branch': branch, 'direction': index, 'action_error': row['action_derivative_error'], 'adjoint_error': row['adjoint_with_temporal_boundaries_error']}), flush=True)
            higher = FiniteWidthScalar(history, gram, width, smear_order=8).integrated(np.ones(4), time_order=18)
            check(branch + '_higher_smear_and_time_quadrature', max(abs(higher[key] - report['variation_cases'][-1][key]) for key in ['action', 'raw', 'adjoint']) < 1e-9)
            mode_history = LayerModeHistory(history)
            point_mode = TranslatedScalarAction(mode_history, gram).full_integrated([0, 0, 0, 1])
            width_mode = FiniteWidthScalar(mode_history, gram, width).integrated([0, 0, 0, 1])
            check(branch + '_off_shell_layer_mode_not_erased', abs(point_mode['raw']) < 1e-12 and abs(width_mode['raw']) > 1e-8)
            report['layer_mode_cases'].append({'branch': branch, 'point_variation': point_mode['raw'], 'finite_width_variation': width_mode['raw']})
            for shape in ['beta22', 'beta23']:
                zero_history = ZeroShiftHistory(history)
                zero_action = FiniteWidthScalar(zero_history, gram, width, shape)
                for index in [0, 1]:
                    direction = np.eye(4)[index]
                    prediction, energy = zero_action.zero_shift_energy_variation(direction)
                    measured = zero_action.integrated(direction, time_order=20)['raw']
                    check(branch + '_' + shape + '_live_matter_density_' + str(index), abs(measured - prediction) < 1e-10 and energy.min() > 0)
                    report['energy_density_cases'].append({'branch': branch, 'shape': shape, 'direction': index, 'density_variation_error': abs(measured - prediction), 'minimum_live_energy': float(energy.min())})
                    if index == 0:
                        path = destination / (branch + '_' + shape + '_live_layer_energy.npz')
                        np.savez_compressed(path, energy=energy, offsets=zero_action.offsets, weights=zero_action.weights, radii=np.array([action.radii for action in zero_action.actions]))
                        own(path, 'outputs')
                point = reference.full_integrated(np.ones(4), order=18)
                widths = [width, width / 2, width / 4, width / 32768]
                rows = []
                for trial_width in widths:
                    result = FiniteWidthScalar(history, gram, trial_width, shape).integrated(np.ones(4), time_order=18)
                    rows.append({'branch': branch, 'shape': shape, 'width': trial_width, 'action_point_error': abs(result['action'] - point['action']), 'variation_point_error': abs(result['raw'] - point['raw'])})
                check(branch + '_' + shape + '_smooth_point_limit_not_constraint_pass', max(rows[-1]['action_point_error'], rows[-1]['variation_point_error']) < 1e-8)
                report['point_limit_cases'].extend(rows)
                save()
        soluble = ManufacturedHistory(soluble=True)
        pulled_history = TimePullbackHistory(soluble)
        for gram in [False, True]:
            branch = 'GR' if not gram else 'metric_Gram'
            averaged = FiniteWidthScalar(soluble, gram, width)
            proper_total = 0.
            proper_rows = []
            covariance_rows = []
            for weight_value, offset, action in zip(averaged.weights, averaged.offsets, averaged.actions):
                proper = proper_clock_integral(action)
                proper_total += weight_value * proper['action']
                proper_rows.append(proper)
                pulled = TranslatedScalarAction(pulled_history, gram, width * offset)
                covariance = covariance_control(action, pulled)
                covariance_rows.append(covariance)
            coordinate = averaged.integrated([0, 0, 0, 0], time_order=20)['action']
            check(branch + '_independent_proper_clock_integration', abs(proper_total - coordinate) < 1e-9 and max(row['endpoint_coordinate_time_error'] for row in proper_rows) < 1e-9)
            report['proper_clock_cases'].append({'branch': branch, 'coordinate_action': coordinate, 'proper_clock_action': proper_total, 'difference': abs(proper_total - coordinate), 'layers': proper_rows})
            check(branch + '_finite_time_covariance_every_layer', max(max(row[key] for key in ['time_map_conjugacy_error', 'spatial_covariance_error', 'kinetic_covariance_error', 'integrated_covariance_error']) for row in covariance_rows) < 1e-8)
            check(branch + '_drop_horizontal_J_detected', min(row['drop_transport_J_negative_control'] for row in covariance_rows) > 1e-9)
            report['covariance_cases'].append({'branch': branch, 'layers': covariance_rows})
            print(json.dumps({'branch': branch, 'proper_clock_action_error': abs(proper_total - coordinate), 'maximum_covariance_error': max(row['spatial_covariance_error'] for row in covariance_rows)}), flush=True)
        check('temporal_boundary_terms_have_not_become_silent', max(abs(row['spatial_time_boundary']) for row in report['variation_cases']) > 1e-9 and max(abs(row['kinetic_time_boundary']) for row in report['variation_cases']) > 1e-9)
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
