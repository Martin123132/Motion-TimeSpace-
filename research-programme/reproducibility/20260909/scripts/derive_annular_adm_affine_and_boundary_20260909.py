import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from annular_adm_mixed_action_20260909 import MixedActionBasis, OrthogonalReference, coefficient_jets, real_linear
    from annular_adm_clock_quadratic_20260909 import LocalQuadraticPath
    from annular_gram_joint_action_20260909 import gram_matrices

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260909'
    destination = intake / 'annular-adm-affine-and-boundary-derived'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': {}, 'outputs': {}, 'checks': [], 'samples': [], 'valid_for_physics_claim': False, 'scope': 'Independent spatial-curvature derivation, bulk position/momentum derivatives, candidate and baseline affine Euler defects of the declared parent-seeded time-jet path, exact patch endpoint covectors, and resolved quadratic time-boundary identity. Affine defects are not parent-signed physical forcing or evolved solutions; patch endpoints are not the original global physical boundaries.'}
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

    save()
    try:
        prior_path = intake / 'annular-adm-clock-quadratic-derived/status.json'
        own(prior_path)
        prior = json.loads(prior_path.read_text())
        verify('completed_action_derivation_and_kinetic_tests_verified', prior['state'] == 'complete' and prior['passed'] == prior['total'])
        verify('all_prior_sources_and_arrays_unchanged', all(own(root / name) == digest for name, digest in {**prior['inputs'], **prior['outputs']}.items()))
        own(Path(__file__))
        compile(Path(__file__).read_bytes(), str(Path(__file__)), 'exec')
        radius, theta, phi = symbolic.symbols('r theta phi', positive=True)
        radial_scale = symbolic.Function('L')(radius)
        coordinates = [radius, theta, phi]
        diagonal = [radial_scale**2, radius**2, radius**2 * symbolic.sin(theta)**2]
        metric = symbolic.diag(*diagonal)
        inverse = symbolic.diag(*[1 / value for value in diagonal])
        connection = [[[symbolic.simplify(sum(inverse[upper, contracted] * (symbolic.diff(metric[contracted, second], coordinates[first]) + symbolic.diff(metric[contracted, first], coordinates[second]) - symbolic.diff(metric[first, second], coordinates[contracted])) for contracted in range(3)) / 2) for second in range(3)] for first in range(3)] for upper in range(3)]
        curvature = symbolic.S.Zero
        for component in range(3):
            ricci = sum(symbolic.diff(connection[contracted][component][component], coordinates[contracted]) - symbolic.diff(connection[contracted][component][contracted], coordinates[component]) + sum(connection[contracted][component][component] * connection[other][contracted][other] - connection[other][component][contracted] * connection[contracted][component][other] for other in range(3)) for contracted in range(3))
            curvature += inverse[component, component] * ricci
        expected_curvature = 2 * (1 - 1 / radial_scale**2) / radius**2 + 4 * symbolic.diff(radial_scale, radius) / (radius * radial_scale**3)
        verify('independent_Christoffel_Ricci_spatial_curvature_derivation', symbolic.simplify(curvature - expected_curvature) == 0)

        for case_name in ['canonical', 'nonlinear_modulated']:
            case_path = intake / 'annular-constraint-correction-initial' / (case_name + '.json')
            own(case_path)
            case = json.loads(case_path.read_text())
            reference = OrthogonalReference(case)
            kappa = float(symbolic.sympify(case['normalization_kappa']))
            radii = numerical.linspace(5.875, 6.125, 17)
            basis = MixedActionBasis(radii)
            path = LocalQuadraticPath(basis, reference.adapted(0.15, radii), reference.adapted(0.15, basis.faces), reference.constants)
            position, velocity, defect, defect_time = path.path(0.0)
            gradients = []
            for component, values in enumerate(position):
                gradient = numerical.zeros_like(values)
                for index in range(values.size):
                    changed = [value.astype(complex) for value in position]
                    changed[component][index] += 1j * 1e-25
                    gradient[index] = basis.action(changed, velocity, defect, defect_time, reference.constants, kappa).imag / 1e-25
                gradients.append(gradient)
            direction = [0.02 * numerical.sin(radii), 0.02 * numerical.cos(basis.faces), 0.02 * numerical.cos(1.3 * radii), 0.03 * numerical.sin(0.7 * basis.faces)]
            expected_direction = sum(numerical.dot(gradient, delta) for gradient, delta in zip(gradients, direction))
            for step in [0.001, 0.0005]:
                plus = [value + step * delta for value, delta in zip(position, direction)]
                minus = [value - step * delta for value, delta in zip(position, direction)]
                measured = (basis.action(plus, velocity, defect, defect_time, reference.constants, kappa) - basis.action(minus, velocity, defect, defect_time, reference.constants, kappa)) / (2 * step)
                verify(case_name + '_independent_complete_bulk_position_gradient_' + str(step), abs(measured - expected_direction) < 1e-7 * max(abs(expected_direction), 1e-20) + 1e-12)

            def momenta(time):
                fields, speeds, lift, lift_time = path.path(time)
                radius_q, scale, unused_scale_t, unused_scale_r, lapse, unused_lapse_r, shift, unused_shift_r, scalar, scalar_t, scalar_r = basis.unpack(fields, speeds, lift, lift_time, reference.constants)
                normal_velocity = (scalar_t - shift * scalar_r) / lapse
                kinetic = -normal_velocity**2 + scalar_r**2 / scale**2
                principal = 1 - 4 * reference.constants['b2'] * kinetic - 6 * reference.constants['b3'] * kinetic**2
                scalar_momentum = basis.scalar_value.T @ (basis.quadrature_weights * radius_q**2 * scale * principal * normal_velocity)
                mass_momentum = basis.face_value.T @ (basis.quadrature_weights * shift * scale**3 / (kappa * lapse))
                return [scalar_momentum, mass_momentum, numerical.zeros_like(fields[2]), numerical.zeros_like(fields[3])]

            baseline_momenta = momenta(0.0)
            for component, values in enumerate(velocity):
                changed = [value.astype(complex) for value in velocity]
                changed[component] += 1j * 1e-25 * direction[component]
                measured = basis.action(position, changed, defect, defect_time, reference.constants, kappa).imag / 1e-25
                verify(case_name + '_independent_bulk_momentum_' + str(component), abs(measured - numerical.dot(baseline_momenta[component], direction[component])) < 1e-12)

            def gram_linear(time):
                fields, speeds, lift, unused_lift_time = path.path(time)
                scalar, mass_face, lapse, unused_shift = fields
                mass = real_linear(basis.face_to_node, mass_face)
                gradient = real_linear(basis.derivative, scalar) + lift
                coefficient, coefficient_gradient, unused_hessian = coefficient_jets(speeds[0], gradient, mass, lapse, radii, reference.constants)
                factors, sampling = gram_matrices(radii.size)
                factor_scalar, factor_velocity, factor_coefficient = [real_linear(matrix, value) for matrix, value in [(factors, scalar), (factors, speeds[0]), (sampling, coefficient)]]
                density = real_linear(sampling.T, factor_scalar**2) / (2 * basis.spacing)
                scalar_gradient = real_linear(factors.T, factor_coefficient * factor_scalar) / basis.spacing + real_linear(basis.derivative.T, density * coefficient_gradient[1])
                scalar_momentum = density * coefficient_gradient[0]
                links = path.links
                factor_energy_time = factor_scalar * factor_velocity / basis.spacing
                current = coefficient[links.node] * links.sweight * factor_energy_time[links.factor] - speeds[0][links.node] * links.tweight * factor_coefficient[links.factor] * factor_scalar[links.factor] / basis.spacing
                spatial_f = 1 - 2 * mass / radii - reference.constants['Lambda'] * radii**2 / 3
                inverse_clock = 1 / (spatial_f * lapse**2)
                connection_shift = inverse_clock * real_linear(links.first.T, current)
                gradients = [scalar_gradient, real_linear(basis.face_to_node.T, density * coefficient_gradient[2]), density * coefficient_gradient[3], real_linear(basis.face_to_node.T, density * coefficient_gradient[4] + connection_shift)]
                return gradients, scalar_momentum

            residual_controls = []
            for time_step in [1e-4, 5e-5]:
                plus_momentum, minus_momentum = momenta(time_step), momenta(-time_step)
                baseline_residual = [gradient - (plus - minus) / (2 * time_step) for gradient, plus, minus in zip(gradients, plus_momentum, minus_momentum)]
                gram_gradient, unused_momentum = gram_linear(0.0)
                gram_residual = [value.copy() for value in gram_gradient]
                gram_residual[0] -= (gram_linear(time_step)[1] - gram_linear(-time_step)[1]) / (2 * time_step)
                candidate_residual = [baseline - change for baseline, change in zip(baseline_residual, gram_residual)]
                residual_controls.append((baseline_residual, gram_residual, candidate_residual))
            residual_error = max(maximum(first - second) for first, second in zip(residual_controls[0][2], residual_controls[1][2]))
            verify(case_name + '_affine_Euler_defect_time_step_control', residual_error < 1e-8, {'maximum_difference': residual_error})
            baseline_residual, gram_residual, candidate_residual = residual_controls[-1]
            verify(case_name + '_nonzero_baseline_and_candidate_forcing_retained', max(maximum(value) for value in baseline_residual) > 1e-8 and max(maximum(value) for value in candidate_residual) > 1e-8)
            zero = [numerical.zeros_like(value) for value in position]
            for selected in [2, 3]:
                probe = [value.copy() for value in zero]
                probe[selected] = direction[selected]
                predicted = numerical.dot(gram_linear(0.0)[0][selected], probe[selected])
                for step in [0.001, 0.0005]:
                    measured = (path.exact_potential(0.0, probe, zero, step) - path.exact_potential(0.0, probe, zero, -step)) / (2 * step)
                    if selected == 3:
                        links = path.links
                        fields, speeds, unused_lift, unused_lift_time = path.path(0.0)
                        scalar, mass_face, lapse, unused_shift = fields
                        mass = real_linear(basis.face_to_node, mass_face)
                        coefficient = coefficient_jets(speeds[0], path.gradient, mass, lapse, radii, reference.constants)[0]
                        spatial_f = 1 - 2 * mass / radii - reference.constants['Lambda'] * radii**2 / 3
                        connection = -real_linear(basis.face_to_node, probe[3]) / (spatial_f * lapse**2)
                        first_link = real_linear(links.first, connection)

                        def linear_boundary(time):
                            parts = path.components(time, probe, zero)
                            scalar_now, unused_velocity, coefficient_now, unused_coefficient_time, unused_first, unused_second, unused_perturbation, unused_rate, link_now, unused_link_time, unused_second_link = parts
                            leading = links.collect(links.tweight * scalar_now[links.node])
                            return numerical.dot(leading**2 / (2 * basis.spacing), links.collect(links.sweight * coefficient_now[links.node] * link_now))

                        boundary_derivative = linear_boundary(1j * 1e-25).imag / 1e-25
                    else:
                        boundary_derivative = 0.0
                    scale = max(abs(measured), abs(predicted), abs(boundary_derivative), 1e-25)
                    verify(case_name + '_independent_lapse_or_shift_covector_' + str(selected) + '_' + str(step), abs(measured - predicted - boundary_derivative) < 2e-4 * scale + 1e-15, {'predicted_reduced': float(predicted), 'time_boundary_derivative': float(boundary_derivative), 'measured_raw': float(measured)})

            rough_position = [0.03 * numerical.sin(13 * radii), 0.1 * numerical.cos(17 * basis.faces), 0.1 * numerical.cos(31 * radii), 0.2 * numerical.sin(47 * basis.faces)]
            rough_speed = [0.1 * numerical.cos(19 * radii), 0.2 * numerical.sin(23 * basis.faces), 0.2 * numerical.sin(29 * radii), 0.3 * numerical.cos(53 * basis.faces)]
            reduced, unused_boundary, raw = path.quadratic(0.0, rough_position, rough_speed, raw=True)
            boundary_derivative = path.quadratic(1j * 1e-25, rough_position, rough_speed)[1].imag / 1e-25
            identity_error = abs(raw - reduced - boundary_derivative)
            verify(case_name + '_resolved_time_boundary_negative_control', identity_error < 1e-8 * abs(boundary_derivative) and abs(raw - reduced) > 100 * max(identity_error, 1e-24), {'boundary_derivative': float(boundary_derivative), 'identity_error': float(identity_error), 'test': 'Direct unreduced/reduced quadratic germs and derivative; not a claim that the smaller integrated finite-difference control resolved this term.'})
            endpoint_radius = radii[[0, -1]]
            endpoint_mass = position[1][[0, -1]]
            endpoint_lapse = position[2][[0, -1]]
            endpoint_f = 1 - 2 * endpoint_mass / endpoint_radius - reference.constants['Lambda'] * endpoint_radius**2 / 3
            mass_boundary = endpoint_lapse / (kappa * numerical.sqrt(endpoint_f))
            verify(case_name + '_nonzero_patch_mass_boundary_covectors_retained', numerical.all(mass_boundary > 0), {'signed_mass_coefficients': [-float(mass_boundary[0]), float(mass_boundary[1])], 'outer_global_BC_supplied': False})
            artifact = destination / (case_name + '_affine_covectors.npz')
            arrays = {'radius': radii, 'faces': basis.faces, 'signed_patch_mass_boundary': numerical.array([-mass_boundary[0], mass_boundary[1]])}
            for name, baseline, correction, candidate in zip(['scalar', 'spatial_mass', 'lapse', 'radial_shift'], baseline_residual, gram_residual, candidate_residual):
                arrays['baseline_' + name] = baseline
                arrays['Gram_' + name] = correction
                arrays['candidate_' + name] = candidate
            numerical.savez_compressed(artifact, **arrays)
            report['outputs'][str(artifact.relative_to(root))] = hashlib.sha256(artifact.read_bytes()).hexdigest()
            report['samples'].append({'case': case_name, 'baseline_Euler_max_by_field': [maximum(value) for value in baseline_residual], 'Gram_Euler_max_by_field': [maximum(value) for value in gram_residual], 'candidate_Euler_max_by_field': [maximum(value) for value in candidate_residual], 'field_order': ['scalar', 'spatial_mass', 'lapse', 'radial_shift'], 'parent_signed_external_source': False, 'background_assumed_on_shell': False})
            save()
        verify('all_owned_inputs_unchanged', all(hashlib.sha256((root / name).read_bytes()).hexdigest() == digest for name, digest in report['inputs'].items()))
        verify('no_bytecode_cache', not (root / 'scripts/__pycache__').exists())
        report.update(passed=sum(check['passed'] for check in report['checks']), total=len(report['checks']), completed_utc=datetime.now(timezone.utc).isoformat())
        report['state'] = 'complete' if report['passed'] == report['total'] else 'failed'
        save()
    except Exception as error:
        report.update(state='failed', failure=repr(error), completed_utc=datetime.now(timezone.utc).isoformat())
        save()
        raise
    print(json.dumps({key: report[key] for key in ['state', 'passed', 'total', 'completed_utc']}), flush=True)
    if report['state'] != 'complete':
        raise SystemExit(1)
    (destination / 'COMPLETE').write_text(report['completed_utc'] + '\n')


if __name__ == '__main__':
    run()
