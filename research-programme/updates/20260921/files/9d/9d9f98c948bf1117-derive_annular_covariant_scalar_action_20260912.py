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
    from annular_covariant_scalar_action_20260912 import CovariantScalarAction, TimePullbackHistory, full_spatial_factors
    from annular_nonlinear_history_20260912 import ManufacturedHistory

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260912'
    destination = intake / 'annular-covariant-full-scalar-action-attempt01'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'checks': [], 'cases': [], 'inputs': {}, 'outputs': {}, 'valid_for_physics_claim': False, 'new_evolution': False, 'full_second_jet_closed': False, 'interval_certificate': False, 'new_finite_scalar_action_not_old_certificate': True, 'manufactured_history_only': True, 'full_coupled_initial_state_not_yet_prepared': True, 'same_continuum_minimal_scalar_action': True, 'temporal_and_radial_ports_not_dropped': True}

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        save()
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))
        print(name + ': passed', flush=True)

    save()
    try:
        prior_path = intake / 'annular-scalar-kinetic-pair-attempt01/status.json'
        prior = json.loads(prior_path.read_text())
        check('kinetic_pair_attempt_complete_not_a_full_pass', prior['state'] == 'complete' and not prior['full_second_jet_closed'])
        inherited = dict(prior['inputs'])
        inherited.update(prior['outputs'])
        for name, expected in inherited.items():
            if hashlib.sha256((root / name).read_bytes()).hexdigest() != expected:
                raise RuntimeError('Changed evidence: ' + name)
            report['inputs'][name] = expected
        own(prior_path)
        for path in [Path(__file__), root / 'scripts/annular_covariant_scalar_action_20260912.py']:
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
            snapshot = destination / ('executed-' + path.name)
            snapshot.write_bytes(path.read_bytes())
            own(snapshot, 'outputs')
        radius, geometry, lapse, beta, velocity, gradient, old_pi, new_pi = sp.symbols('R F N beta q w pi p', real=True, nonzero=True)
        chart = 1 - beta**2 / (lapse**2 * geometry)
        coefficient = radius**2 * lapse * sp.sqrt(geometry) * chart
        connection = beta / (lapse**2 * geometry - beta**2)
        kinetic = radius**4 / coefficient
        old_kinetic = radius**2 / (lapse * sp.sqrt(geometry))
        old_second_order = old_kinetic * (velocity - beta * gradient)**2 / 2 - radius**2 * lapse * sp.sqrt(geometry) * gradient**2 / 2
        new_second_order = kinetic * velocity**2 / 2 - coefficient * (gradient + connection * velocity)**2 / 2
        check('exact_threading_decomposition_of_continuum_scalar', sp.simplify(old_second_order - new_second_order) == 0)
        check('reciprocal_kinetic_coefficient_not_new_parameter', sp.simplify(kinetic * coefficient - radius**4) == 0)
        new_first_order = new_pi * velocity - coefficient * new_pi**2 / (2 * radius**4) - coefficient * (gradient + connection * velocity)**2 / 2
        check('new_auxiliary_eliminates_to_same_continuum_action', sp.simplify(new_first_order.subs(new_pi, kinetic * velocity) - old_second_order) == 0)
        check('new_auxiliary_is_not_old_pi_away_from_zero_shift', sp.simplify(kinetic * velocity - old_kinetic * (velocity - beta * gradient)) != 0)
        density, density_t, momentum, momentum_t, scalar_q, scalar_q_t, clock, clock_t, epsilon, epsilon_t, radius4, weight, nodal_d, nodal_d_t, nodal_force = sp.symbols('C Ct p pt q qt epsilon_clock epsilon_clock_t epsilon epsilon_t radius4 weight d dt G')
        canonical_density = momentum * scalar_q - density * momentum**2 / (2 * radius4)
        derivative = sp.diff(canonical_density, momentum) * momentum_t + sp.diff(canonical_density, scalar_q) * scalar_q_t + sp.diff(canonical_density, density) * density_t
        variation = sp.diff(canonical_density, momentum) * epsilon * momentum_t + sp.diff(canonical_density, scalar_q) * (epsilon * scalar_q_t + epsilon_t * scalar_q) + sp.diff(canonical_density, density) * (epsilon * density_t + epsilon_t * density)
        check('nodal_first_order_kinetic_time_density_off_shell', sp.expand(variation - epsilon * derivative - epsilon_t * canonical_density) == 0)
        coefficient_force_t = -weight * momentum * momentum_t / radius4 - nodal_d_t
        scalar_E = -weight * momentum_t + nodal_force
        momentum_E = weight * (scalar_q - density * momentum / radius4)
        check('whole_scalar_nodal_Ward_has_no_projection_remainder', sp.expand(-density * coefficient_force_t + scalar_E * scalar_q + momentum_E * momentum_t - density * nodal_d_t - nodal_force * scalar_q) == 0)
        manufactured = ManufacturedHistory(soluble=False)
        for gram in [False, True]:
            branch = 'GR_base' if not gram else 'base_plus_same_Gram'
            action = CovariantScalarAction(manufactured, gram)
            check(branch + '_positive_sampling_and_constant_nullspace', action.sampling.min() >= 0 and abs(action.sampling.sum(axis=1) - 1).max() < 1e-14 and abs(action.factors @ np.ones(17)).max() < 1e-13)
            for index, direction in enumerate([np.eye(4)[index] for index in range(4)] + [np.ones(4)]):
                actual = action.full_integrated(direction)
                differences = []
                for step in [2e-4, 1e-4]:
                    plus = action.full_integrated(direction, step)['action']
                    minus = action.full_integrated(direction, -step)['action']
                    differences.append((plus - minus) / (2 * step))
                extrapolated = (4 * differences[-1] - differences[0]) / 3
                control = {'branch': branch, 'direction': np.asarray(direction).tolist(), 'raw_variation': actual['raw'], 'action_difference_error': abs(extrapolated - actual['raw']), 'full_adjoint_with_both_temporal_boundaries_error': abs(actual['adjoint'] - actual['raw']), **{key: value for key, value in actual.items() if key not in ['raw', 'adjoint']}}
                check(branch + '_actual_action_derivative_' + str(index), control['action_difference_error'] < 1e-8 and control['full_adjoint_with_both_temporal_boundaries_error'] < 1e-8, control)
                report['cases'].append(control)
                save()
        soluble = ManufacturedHistory(soluble=True)
        pulled_history = TimePullbackHistory(soluble)
        points, weights = np.polynomial.legendre.leggauss(20)
        times, weights = .05 + .35 * points, .35 * weights
        for gram in [False, True]:
            branch = 'GR_base' if not gram else 'base_plus_same_Gram'
            base = CovariantScalarAction(soluble, gram)
            pulled = CovariantScalarAction(pulled_history, gram)
            transformed_T, transformed_J, unused_Y, unused_Z = pulled.transport(times, [0, 0, 0, 0])
            anchor_H, anchor_Ht, unused_Hr, unused_Hrt = pulled_history.map(times[:, None], base.anchors)
            endpoint_H, endpoint_Ht, unused_Hr, unused_Hrt = pulled_history.map(transformed_T, base.targets)
            expected_T, expected_J = soluble.exact_transport(anchor_H, base.anchors, base.targets)
            check(branch + '_independent_finite_time_map_conjugacy', max(float(abs(endpoint_H - expected_T).max()), float(abs(endpoint_Ht * transformed_J - expected_J * anchor_Ht).max())) < 1e-9)
            fields = soluble.evaluate(expected_T, base.targets, [0, 0, 0, 0])[0]
            coefficient = base.geometry.evaluate(base.targets, fields)['C']
            amplitude = base.collect(base.factor_weight * fields[3])
            density_sum = base.collect(base.sample_weight * expected_J * coefficient)
            factor_Ht = pulled_history.map(times[:, None], base.sampling @ base.radii)[1]
            spatial_reference = -np.sum(factor_Ht * density_sum * amplitude**2, axis=1) / (2 * base.spacing)
            spatial_actual = pulled.integrands(times, [0, 0, 0, 0])['action']
            check(branch + '_full_spatial_action_density_covariance', abs(spatial_actual - spatial_reference).max() < 1e-9, float(abs(spatial_actual - spatial_reference).max()))
            node_H, node_Ht, node_Hr, unused_Hrt = pulled_history.map(times[:, None], base.radii)
            fields, rates, unused_second, unused_delta, unused_delta_rate, unused_delta_second = soluble.evaluate(node_H, base.radii, [0, 0, 0, 0])
            base_C = base.geometry.evaluate(base.radii, fields)['C']
            base_B = base.radii**4 / base_C
            kinetic_reference = (.5 * node_Ht * base_B * rates[3]**2) @ base.node_weights
            kinetic_actual = pulled.kinetic(times, [0, 0, 0, 0])['action']
            check(branch + '_full_kinetic_action_density_covariance', abs(kinetic_actual - kinetic_reference).max() < 1e-10)
            finite_map_error = float(abs(weights @ (kinetic_actual + spatial_actual - kinetic_reference - spatial_reference)))
            record = {'branch': branch, 'same_physical_window_full_action_covariance_error': finite_map_error, 'node_dependent_time_windows_not_identical_coordinate_bounds': True, 'maximum_endpoint_time_displacement': float(abs(transformed_T - times[:, None]).max())}
            transformed_fields = pulled_history.evaluate(transformed_T, pulled.targets, [0, 0, 0, 0])[0]
            transformed_C = pulled.geometry.evaluate(pulled.targets, transformed_fields)['C']
            wrong_density = pulled.collect(pulled.sample_weight * transformed_C)
            transformed_amplitude = pulled.collect(pulled.factor_weight * transformed_fields[3])
            wrong_spatial = -np.sum(wrong_density * transformed_amplitude**2, axis=1) / (2 * pulled.spacing)
            wrong_kinetic = (.5 * node_Ht**2 * base_B * rates[3]**2) @ base.node_weights
            record['drop_J_negative_control_max'] = float(abs(wrong_spatial - spatial_reference).max())
            record['wrong_B_time_weight_negative_control_max'] = float(abs(wrong_kinetic - kinetic_reference).max())
            check(branch + '_finite_covariance_negative_controls', min(record['drop_J_negative_control_max'], record['wrong_B_time_weight_negative_control_max']) > 1e-9, record)
            report.setdefault('covariance_cases', []).append(record)
        smooth = []
        def profile(time, radii):
            fraction = 8 * (radii - 6)
            scalar = .2 + .012 * fraction + .005 * fraction**3 + .003 * fraction**4 + time * (.018 + .011 * fraction + .006 * fraction**2) + .004 * time**2
            velocity = .018 + .011 * fraction + .006 * fraction**2 + .008 * time
            gradient = 8 * (.012 + .015 * fraction**2 + .012 * fraction**3 + time * (.011 + .012 * fraction))
            return scalar, velocity, gradient
        gauss, gauss_weights = np.polynomial.legendre.leggauss(64)
        radius_quad, radius_weights = 6 + .125 * gauss, .125 * gauss_weights
        unused_scalar, velocity, gradient = profile(.08, radius_quad)
        coefficient = 2 + .2 * (radius_quad - 6)
        connection = .07 + .015 * (radius_quad - 6)
        exact_spatial = float(radius_weights @ (.5 * coefficient * (gradient + connection * velocity)**2))
        exact_kinetic = float(radius_weights @ (.5 * radius_quad**4 * velocity**2 / coefficient))
        for intervals in [16, 32, 64]:
            radii = np.linspace(5.875, 6.125, intervals + 1)
            spacing = radii[1] - radii[0]
            kinetic_weights = np.full(radii.size, spacing)
            kinetic_weights[[0, -1]] /= 2
            spatial_values = {}
            for gram in [False, True]:
                factors, sampling = full_spatial_factors(radii.size, gram)
                factor, node = np.nonzero((factors != 0) | (sampling != 0))
                anchors = (sampling @ radii)[factor]
                targets = radii[node]
                transported = .08 + .07 * (targets - anchors) + .0075 * ((targets - 6)**2 - (anchors - 6)**2)
                scalar = profile(transported, targets)[0]
                amplitudes = np.bincount(factor, weights=factors[factor, node] * scalar, minlength=factors.shape[0])
                coefficients = sampling @ (2 + .2 * (radii - 6))
                spatial_values['MTS' if gram else 'GR'] = float(coefficients @ amplitudes**2 / (2 * spacing))
            scalar, velocity, unused_gradient = profile(.08, radii)
            kinetic_value = float(kinetic_weights @ (.5 * radii**4 * velocity**2 / (2 + .2 * (radii - 6))))
            wrong_spatial = float(((2 + .2 * (radii - 6))[:-1] + (2 + .2 * (radii - 6))[1:]) @ np.diff(scalar)**2 / (4 * spacing))
            smooth.append({'intervals': intervals, 'kinetic_error': abs(kinetic_value - exact_kinetic), 'base_spatial_error': abs(spatial_values['GR'] - exact_spatial), 'MTS_spatial_error': abs(spatial_values['MTS'] - exact_spatial), 'Gram_extra': spatial_values['MTS'] - spatial_values['GR'], 'untransported_base_error': abs(wrong_spatial - exact_spatial)})
        for key in ['kinetic_error', 'base_spatial_error', 'MTS_spatial_error']:
            check('smooth_mesh_refinement_' + key, smooth[0][key] > smooth[1][key] > smooth[2][key], [row[key] for row in smooth])
        check('wrong_equal_time_spatial_limit_remains_detectable', smooth[-1]['untransported_base_error'] > 10 * smooth[-1]['base_spatial_error'], smooth)
        report['smooth_refinement_not_interval_certificate'] = smooth
        count = 17
        factors, sampling = full_spatial_factors(count, False)
        radii = np.linspace(5.875, 6.125, count)
        spacing = radii[1] - radii[0]
        amplitude = factors @ (.3 + .2 * radii)
        sample_C, velocity_constant = 2., .04
        factor, node = np.nonzero((factors != 0) | (sampling != 0))
        current = -amplitude[factor] * factors[factor, node] * velocity_constant * sample_C / spacing
        expected_current = np.where(factors[factor, node] < 0, 1., -1.) * sample_C * .2 * velocity_constant
        check('affine_wave_base_transport_restores_original_scalar_mass_flux', abs(current - expected_current).max() < 1e-13)
        report['affine_flux_identity'] = 'At c=c_t=0, constant C, chi=w*R+q*t: K=-C*q*w on both halves of every base edge; -c_P*K=kappa*R^2*F*q*w, the original scalar mass flux. Do not also retain the old beta*pi*w block.'
        for module in tuple(sys.modules.values()):
            filename = getattr(module, '__file__', None)
            if filename:
                path = Path(filename).resolve()
                if path.parent == root / 'scripts' and path.suffix == '.py':
                    own(path)
        check('no_python_cache', not (root / 'scripts/__pycache__').exists())
        report['state'] = 'complete'
        save()
        print(json.dumps({'state': report['state'], 'checks': len(report['checks']), 'covariance_cases': report['covariance_cases'], 'smooth_refinement': smooth}), flush=True)
    except Exception as error:
        report.update({'state': 'failed', 'error': repr(error), 'traceback': traceback.format_exc()})
        save()
        raise


if __name__ == '__main__':
    run()
