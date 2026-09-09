import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from annular_covariant_time_transport_20260909 import ReferenceGeometry, coordinate_map, factor_action, layout
    from annular_gram_joint_action_20260909 import gram_matrices
    from annular_mixed_grid_basis_20260909 import mixed_basis, weak_gravity, weak_gravity_covectors

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260909'
    destination = intake / 'annular-covariant-transport-and-mixed-basis-derived'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'checks': [], 'inputs': {}, 'outputs': {}, 'samples': [], 'valid_for_physics_claim': False, 'scope': 'Exact continuum-time metric-connection transport of the positive Gram action density; finite coordinate covariance, action-integrated connection current with nonzero endpoint work, and first mixed-basis gravity covectors. Not the complete ungauged discrete Einstein action, horizon transport, evolution, calibrated coupling, local GR or a closed constraint algebra.'}
    (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')

    def own(path):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        report['inputs'][str(path.relative_to(root))] = digest
        return digest

    def verify(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        save()
        print(name + ': ' + str(bool(passed)), flush=True)

    def maximum(value):
        return float(numerical.max(numerical.abs(value)))

    def artifact(name, **arrays):
        path = destination / name
        numerical.savez_compressed(path, **arrays)
        report['outputs'][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    save()
    try:
        prior_path = intake / 'annular-clock-coframe-final-integrity.json'
        own(prior_path)
        previous = json.loads(prior_path.read_text())
        verify('previous_turn_verified_progress', previous['state'] == 'complete' and previous['output_hashes'] == 54)
        verify('previous_immutable_inputs_and_outputs_unchanged', all(own(root / name) == digest for name, digest in {**previous['inputs'], **previous['outputs']}.items()))
        for name in ['derive_annular_covariant_transport_and_mixed_basis_20260909.py', 'annular_covariant_time_transport_20260909.py', 'annular_mixed_grid_basis_20260909.py']:
            own(root / 'scripts' / name)
            compile((root / 'scripts' / name).read_bytes(), name, 'exec')

        density, density_time, jacobian, jacobian_time, epsilon, epsilon_time, epsilon_endpoint_time, varied_time = symbolic.symbols('a at J Jt eps epst endepst y')
        varied_jacobian = -epsilon_endpoint_time * jacobian + jacobian_time * epsilon + jacobian * epsilon_time
        endpoint_epsilon = symbolic.symbols('endeps')
        varied_time = -endpoint_epsilon + jacobian * epsilon
        pull_variation = density * varied_jacobian + jacobian * (endpoint_epsilon * density_time + epsilon_endpoint_time * density) + jacobian * density_time * varied_time
        expected = epsilon * (jacobian_time * density + jacobian**2 * density_time) + epsilon_time * jacobian * density
        verify('symbolic_pulled_density_full_time_reparametrization', symbolic.expand(pull_variation - expected) == 0)
        connection, connection_time, epsilon_radius = symbolic.symbols('A At epsr')
        link_variation_rhs = -(epsilon * connection_time + epsilon_radius - connection * epsilon_time) - connection_time * (-epsilon + jacobian * endpoint_epsilon)
        link_variation_derivative = -epsilon_radius + connection * epsilon_time - connection_time * jacobian * endpoint_epsilon
        verify('symbolic_link_sensitivity_solves_full_connection_law', symbolic.expand(link_variation_rhs - link_variation_derivative) == 0)
        fraction, first_left, first_right, second_left, second_right = symbolic.symbols('w fl fr gl gr')
        interpolate_product = (1 - fraction) * first_left * second_left + fraction * first_right * second_right
        product_interpolates = ((1 - fraction) * first_left + fraction * first_right) * ((1 - fraction) * second_left + fraction * second_right)
        verify('symbolic_fixed_linear_basis_product_commutator', symbolic.expand(interpolate_product - product_interpolates - fraction * (1 - fraction) * (first_right - first_left) * (second_right - second_left)) == 0)

        prior_owner = intake / 'annular-clock-coframe-current-derived'
        covariance_errors = []
        boundary_controls = []
        for case_name in ['canonical', 'nonlinear_modulated']:
            case_path = intake / 'annular-constraint-correction-initial' / (case_name + '.json')
            own(case_path)
            case = json.loads(case_path.read_text())
            reference = ReferenceGeometry(case)
            for intervals in [32, 64, 128]:
                radii = numerical.linspace(4, 8, intervals + 1)
                spacing = float(radii[1] - radii[0])
                factors, sampling = gram_matrices(radii.size)
                for time_value in [0.1, 0.15, 0.2]:
                    tag = case_name + '_N' + str(intervals) + '_T' + str(time_value)
                    source_path = prior_owner / (tag + '_clock_coframe.npz')
                    own(source_path)
                    arrays = numerical.load(source_path)
                    scalar, velocity, coefficient = reference.matter(numerical.full_like(radii, time_value), radii)
                    verify(tag + '_direct_profile_matches_owned_snapshot', maximum(scalar - arrays['scalar']) < 1e-13 and maximum(velocity - arrays['velocity']) < 1e-12 and maximum(coefficient - arrays['coefficient']) < 1e-11)
                    coefficient_time = arrays['coefficient_time']
                    clock = numerical.sin(1.3 * radii) + 0.2 * numerical.cos(2.1 * radii)
                    clock_time = 0.3 * numerical.cos(0.7 * radii)
                    anchor_clock, anchor_clock_time = sampling @ clock, sampling @ clock_time
                    offset = clock[None, :] - anchor_clock[:, None]
                    offset_time = clock_time[None, :] - anchor_clock_time[:, None]
                    factor_scalar, factor_velocity, factor_coefficient = factors @ scalar, factors @ velocity, sampling @ coefficient
                    variation_coefficient = -numerical.sum(sampling * (coefficient_time * offset + coefficient * offset_time), axis=1)
                    variation_scalar = -numerical.sum(factors * velocity * offset, axis=1)
                    raw = numerical.sum((variation_coefficient * factor_scalar**2 / 2 + factor_coefficient * factor_scalar * variation_scalar) / spacing)
                    local_energy = sampling.T @ (factor_scalar**2 / (2 * spacing))
                    local_energy_time = sampling.T @ (factor_scalar * factor_velocity / spacing)
                    factor_energy = factor_coefficient * factor_scalar**2 / (2 * spacing)
                    factor_energy_time = (sampling @ coefficient_time) * factor_scalar**2 / (2 * spacing) + factor_coefficient * factor_scalar * factor_velocity / spacing
                    boundary_time = numerical.dot(anchor_clock, factor_energy_time) + numerical.dot(anchor_clock_time, factor_energy) - numerical.sum((coefficient_time * local_energy + coefficient * local_energy_time) * clock + coefficient * local_energy * clock_time)
                    old_current = float(numerical.dot(arrays['clock_covector'], clock))
                    scale = max(abs(raw), abs(boundary_time), abs(old_current), 1e-25)
                    verify(tag + '_full_transport_recovers_old_current_plus_time_boundary', abs(raw - old_current - boundary_time) < 2e-9 * scale + 1e-22)

                basis = mixed_basis(radii)
                faces, weights, mass_to_node, shift_to_face, incidence = basis
                tag = case_name + '_basis_N' + str(intervals)
                verify(tag + '_positive_fixed_partition_and_affine_exactness', numerical.min(mass_to_node) > -1e-13 and numerical.min(shift_to_face) > -1e-13 and maximum(mass_to_node.sum(axis=1) - 1) < 1e-13 and maximum(shift_to_face.sum(axis=1) - 1) < 1e-13 and maximum(mass_to_node @ faces - radii) < 1e-13 and maximum(shift_to_face @ radii - faces) < 1e-13)
                nodal_data = reference.fields(numerical.full_like(radii, 0.18), radii)
                face_data = reference.fields(numerical.full_like(faces, 0.18), faces)
                mass, mass_time = face_data['mass_ref'][:2]
                shift, shift_time = nodal_data['shift_ref'][:2]
                kappa = float(symbolic.sympify(case['normalization_kappa']))
                radial, mass_euler, momentum, boundary = weak_gravity_covectors(mass, mass_time, shift, shift_time, basis, reference.sigma, kappa)
                direction_mass, direction_shift = numerical.sin(faces), numerical.cos(radii)
                step = 1e-25
                measured_mass = weak_gravity(mass + 1j * step * direction_mass, mass_time, shift, basis, reference.sigma, kappa).imag / step
                measured_shift = weak_gravity(mass, mass_time, shift + 1j * step * direction_shift, basis, reference.sigma, kappa).imag / step
                expected_mass = numerical.dot(incidence.T @ numerical.exp(shift) / kappa, direction_mass)
                verify(tag + '_action_derived_face_and_nodal_adjoints', abs(measured_mass - expected_mass) < 1e-11 and abs(measured_shift - numerical.dot(radial, direction_shift)) < 1e-11)
                measured_momentum = weak_gravity(mass, mass_time + 1j * step * direction_mass, shift, basis, reference.sigma, kappa).imag / step
                verify(tag + '_time_momentum_retained', abs(measured_momentum - numerical.dot(momentum, direction_mass)) < 1e-11)
                time_step = 1e-5
                momentum_plus = weak_gravity_covectors(mass, mass_time, shift + time_step * shift_time, shift_time, basis, reference.sigma, kappa)[2]
                momentum_minus = weak_gravity_covectors(mass, mass_time, shift - time_step * shift_time, shift_time, basis, reference.sigma, kappa)[2]
                expected_euler = incidence.T @ numerical.exp(shift) / kappa - (momentum_plus - momentum_minus) / (2 * time_step)
                verify(tag + '_Euler_covector_not_just_instantaneous_gradient', maximum(mass_euler - expected_euler) < 1e-9)
                flat = weak_gravity_covectors(mass, mass_time, numerical.zeros_like(radii), numerical.zeros_like(radii), basis, reference.sigma, kappa)
                verify(tag + '_physical_endpoint_covectors_not_deleted', maximum(flat[1] - flat[3]) < 1e-13 and maximum(flat[3]) == 1 / kappa)
                mixed_work = numerical.dot(numerical.cos(radii), mass_to_node @ direction_mass)
                verify(tag + '_adjoint_work_pairing', abs(mixed_work - numerical.dot(mass_to_node.T @ numerical.cos(radii), direction_mass)) < 1e-12)
                commutator = mass_to_node @ (numerical.sin(faces) * numerical.cos(1.2 * faces)) - (mass_to_node @ numerical.sin(faces)) * (mass_to_node @ numerical.cos(1.2 * faces))
                verify(tag + '_finite_basis_is_not_falsely_declared_gauge_closed', maximum(commutator) > 1e-7, {'product_commutator_max': maximum(commutator), 'constraint_algebra_signed': False})
                artifact(tag + '.npz', radius=radii, faces=faces, mass_to_node=mass_to_node, shift_to_face=shift_to_face, incidence=incidence, mass_euler=mass_euler, physical_boundary=boundary, product_commutator=commutator)

            radii = numerical.linspace(4, 8, 129)
            tag = case_name + '_actual_N128'
            report['active_job'] = tag + '_finite_covariance'
            save()
            base = factor_action(reference, 0.18, radii)
            transformed = factor_action(reference, 0.18, radii, coordinate_size=0.08)
            shifted_time, anchor_jacobian, unused_radius, unused_second, unused_mixed = coordinate_map(numerical.full(base['anchors'].shape, 0.18), base['anchors'], 0.08)
            shifted = factor_action(reference, shifted_time, radii)
            target_radius = radii[base['node_index']]
            endpoint_time, endpoint_jacobian, unused_radius, unused_second, unused_mixed = coordinate_map(transformed['transport'][0], target_radius, 0.08)
            endpoint_error = maximum(endpoint_time - shifted['transport'][0])
            jacobian_error = maximum(endpoint_jacobian * transformed['transport'][1] - shifted['transport'][1] * anchor_jacobian[base['factor_index']])
            expected = anchor_jacobian * shifted['value']
            covariance_error = maximum(transformed['value'] - expected)
            covariance_scale = max(maximum(expected), 1e-25)
            verify(tag + '_finite_coordinate_conjugacy_of_all_links', endpoint_error < 2e-10 and jacobian_error < 2e-10, {'endpoint_error': endpoint_error, 'jacobian_error': jacobian_error})
            verify(tag + '_full_factor_action_density_covariance', covariance_error < 2e-7 * covariance_scale + 1e-20, {'absolute_error': covariance_error, 'relative_max_norm': covariance_error / covariance_scale})
            wrong_jacobian_value = transformed['value'] / anchor_jacobian
            negative_error = maximum(wrong_jacobian_value - expected)
            verify(tag + '_omitting_density_weight_detectably_breaks_covariance', negative_error > 100 * max(covariance_error, 1e-20), {'wrong_weight_error': negative_error})
            current_sum = numerical.bincount(base['factor_index'], weights=base['current'], minlength=base['value'].size)
            current_scale = numerical.bincount(base['factor_index'], weights=numerical.abs(base['current']), minlength=base['value'].size)
            verify(tag + '_all_factor_connection_currents_balance', maximum(current_sum) < 1e-10 * maximum(current_scale) + 1e-24)
            refined = factor_action(reference, 0.18, radii, tolerance=2e-13)
            verify(tag + '_transport_solver_tolerance_control', maximum(refined['value'] - base['value']) < 2e-7 * max(maximum(base['value']), 1e-25) + 1e-20)
            artifact(tag + '_covariance.npz', radius=radii, factor_value=base['value'], transformed_value=transformed['value'], expected_value=expected, transported_time=base['transport'][0], transported_jacobian=base['transport'][1], current=base['current'], factor_index=base['factor_index'], node_index=base['node_index'])
            covariance_errors.append(covariance_error / covariance_scale)

            report['active_job'] = tag + '_integrated_connection_variation'
            save()
            lower, upper = 0.17, 0.19
            derivative_results = []
            for quadrature_order in [16, 24]:
                nodes, quadrature_weights = numerical.polynomial.legendre.leggauss(quadrature_order)
                time_nodes = (upper + lower) / 2 + (upper - lower) * nodes / 2
                quadrature_weights = (upper - lower) * quadrature_weights / 2
                values = numerical.zeros(4)
                bulk = 0.0
                for time_value, weight in zip(time_nodes, quadrature_weights):
                    tangent = factor_action(reference, time_value, radii, sensitivity=True)
                    bulk += weight * float(tangent['bulk_variation'].sum())
                    for index, forcing in enumerate([0.001, -0.001, 0.0005, -0.0005]):
                        values[index] += weight * float(factor_action(reference, time_value, radii, forcing_size=forcing)['value'].sum())
                endpoints = [factor_action(reference, time_value, radii, sensitivity=True) for time_value in [lower, upper]]
                boundary_term = float(endpoints[1]['boundary_variation'].sum() - endpoints[0]['boundary_variation'].sum())
                predicted = bulk + boundary_term
                measured = [(values[0] - values[1]) / 0.002, (values[2] - values[3]) / 0.001]
                scale = max(abs(predicted), abs(bulk), abs(boundary_term), 1e-25)
                errors = [abs(value - predicted) for value in measured]
                for index, error in enumerate(errors):
                    verify(tag + '_action_FD_with_endpoint_work_Q' + str(quadrature_order) + '_step' + str(index), error < 2e-5 * scale + 1e-17, {'error': error, 'scale': scale})
                verify(tag + '_nonzero_time_boundary_matters_Q' + str(quadrature_order), abs(boundary_term) > 100 * max(max(errors), 1e-17), {'bulk': bulk, 'time_boundary': boundary_term, 'complete_variation': predicted, 'FD': measured})
                derivative_results.append({'quadrature_order': quadrature_order, 'bulk': bulk, 'time_boundary': boundary_term, 'predicted': predicted, 'finite_difference': measured, 'absolute_errors': errors})
            verify(tag + '_independent_time_quadrature_refinement', abs(derivative_results[0]['predicted'] - derivative_results[1]['predicted']) < 1e-7 * max(abs(derivative_results[1]['predicted']), 1e-25) + 1e-18)
            boundary_controls.append(derivative_results)
            report['samples'].append({'case': case_name, 'intervals': 128, 'coordinate_covariance_relative_error': covariance_error / covariance_scale, 'time_domain_evaluated': [reference.minimum_advanced, reference.maximum_advanced], 'integrated_variation': derivative_results, 'physics_claim': False})
            save()

        verify('both_cases_and_eighteen_prior_snapshot_identities_checked', len(report['samples']) == 2)
        verify('no_bytecode_cache', not (root / 'scripts/__pycache__').exists())
        verify('all_owned_input_hashes_still_match', all(hashlib.sha256((root / name).read_bytes()).hexdigest() == digest for name, digest in report['inputs'].items()))
        report.update(passed=sum(check['passed'] for check in report['checks']), total=len(report['checks']), completed_utc=datetime.now(timezone.utc).isoformat(), active_job=None)
        report['state'] = 'complete' if report['passed'] == report['total'] else 'failed'
        save()
    except Exception as error:
        report.update(state='failed', failure=repr(error), completed_utc=datetime.now(timezone.utc).isoformat(), active_job=None)
        save()
        raise
    print(json.dumps({key: report[key] for key in ['state', 'passed', 'total', 'completed_utc']}), flush=True)
    if report['state'] != 'complete':
        raise SystemExit(1)
    (destination / 'COMPLETE').write_text(report['completed_utc'] + '\n')


if __name__ == '__main__':
    run()
