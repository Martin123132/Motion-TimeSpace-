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
    destination = intake / 'annular-adm-clock-quadratic-derived'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': {}, 'outputs': {}, 'checks': [], 'samples': [], 'valid_for_physics_claim': False, 'sources': [{'url': 'https://arxiv.org/abs/gr-qc/0405109', 'title': 'The Dynamics of General Relativity', 'use': 'ADM action normalization/convention background'}, {'url': 'https://arxiv.org/pdf/gr-qc/9403003', 'title': 'Geometrodynamics of Schwarzschild Black Holes', 'use': 'Equations17-22 spherical ADM action, independent convention check; boundary and horizon cautions'}], 'scope': 'Construct full shift-unfixed areal spherical ADM plus P(X) mixed finite-element action and a local-in-time quadratic covariant Gram completion. Actual orthogonal local reference patches and explicitly declared time-jet validation paths. No global orthogonal data extrapolation, live evolution, full Dirac closure, physical boundary/horizon/calibration or local-GR certificate.'}
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

    def pack_zero(position):
        return [numerical.zeros_like(value) for value in position]

    def direction_unit(position, index):
        result = pack_zero(position)
        for component, value in enumerate(result):
            if index < value.size:
                result[component][index] = 1
                return result
            index -= value.size
        raise IndexError(index)

    save()
    try:
        prior_path = intake / 'annular-covariant-time-links-final-integrity.json'
        own(prior_path)
        prior = json.loads(prior_path.read_text())
        verify('previous_turn_verified_progress', prior['state'] == 'complete' and prior['compiled_scripts'] == 6)
        verify('inherited_sources_and_outputs_unchanged', all(own(root / name) == digest for name, digest in {**prior['inputs'], **prior['outputs']}.items()))
        for name in ['annular_adm_mixed_action_20260909.py', 'annular_adm_clock_quadratic_20260909.py', 'derive_annular_adm_clock_quadratic_20260909.py']:
            own(root / 'scripts' / name)
            compile((root / 'scripts' / name).read_bytes(), name, 'exec')

        radius, radial_scale, lapse, shift, scale_t, scale_r, lapse_r, shift_r, cosmological, kappa = symbolic.symbols('r L N V Lt Lr Nr Vr Lambda kappa', positive=True)
        radial_curvature = (-scale_t / radial_scale + shift * scale_r / radial_scale + shift_r) / lapse
        angular_curvature = shift / (lapse * radius)
        spatial_curvature = 2 * (1 - 1 / radial_scale**2) / radius**2 + 4 * scale_r / (radius * radial_scale**3)
        adm_definition = lapse * radial_scale * radius**2 * (-4 * radial_curvature * angular_curvature - 2 * angular_curvature**2 + spatial_curvature - 2 * cosmological) / (4 * kappa)
        explicit = (radius * shift * scale_t / lapse - radius * shift**2 * scale_r / lapse - radius * radial_scale * shift * shift_r / lapse - radial_scale * shift**2 / (2 * lapse) + lapse * (radial_scale - 1 / radial_scale) / 2 + lapse * radius * scale_r / radial_scale**2 - cosmological * lapse * radial_scale * radius**2 / 2) / kappa
        verify('symbolic_full_shift_unfixed_ADM_density', symbolic.simplify(adm_definition - explicit) == 0)
        mass_r = (1 - 1 / radial_scale**2 - cosmological * radius**2) / 2 + radius * scale_r / radial_scale**3
        verify('symbolic_zero_shift_static_block_matches_previous_E_mu_r', symbolic.simplify(explicit.subs({shift: 0, shift_r: 0}) - lapse * radial_scale * mass_r / kappa) == 0)
        boundary = -radius * radial_scale * shift**2 / (2 * kappa * lapse)
        boundary_r = symbolic.diff(boundary, radius) + symbolic.diff(boundary, radial_scale) * scale_r + symbolic.diff(boundary, lapse) * lapse_r + symbolic.diff(boundary, shift) * shift_r
        integrated = (radius * shift * scale_t / lapse - radius * shift**2 * (scale_r + radial_scale * lapse_r / lapse) / (2 * lapse) + lapse * (radial_scale - 1 / radial_scale) / 2 + lapse * radius * scale_r / radial_scale**2 - cosmological * lapse * radial_scale * radius**2 / 2) / kappa
        verify('symbolic_radial_integration_boundary_retained', symbolic.simplify(explicit - integrated - boundary_r) == 0)
        verify('symbolic_shift_equation_contains_mass_time', symbolic.simplify(symbolic.diff(explicit, shift).subs({shift: 0, shift_r: 0}) - radius * scale_t / (kappa * lapse)) == 0)
        connection = radial_scale**2 * shift / (-lapse**2 + radial_scale**2 * shift**2)
        verify('symbolic_metric_to_connection_linear_normalization', symbolic.simplify(symbolic.diff(connection, shift).subs(shift, 0) + radial_scale**2 / lapse**2) == 0)
        mass_speed = symbolic.symbols('mut')
        current = symbolic.symbols('Jcut')
        equation = radius * scale_t / (kappa * lapse) + current * radial_scale**2 / lapse**2
        verify('symbolic_connection_mass_source_normalization_is_derived', symbolic.simplify(equation.subs(scale_t, radial_scale**3 * mass_speed / radius).subs(mass_speed, -kappa * current / (lapse * radial_scale))) == 0)
        metric_inverse_rr = 1 / radial_scale**2 - shift**2 / lapse**2
        physical_mass = radius * (1 - metric_inverse_rr - cosmological * radius**2 / 3) / 2
        spatial_mass = radius * (1 - 1 / radial_scale**2 - cosmological * radius**2 / 3) / 2
        verify('symbolic_physical_mass_has_required_shift_squared_correction', symbolic.simplify(physical_mass - spatial_mass - radius * shift**2 / (2 * lapse**2)) == 0)

        for case_name in ['canonical', 'nonlinear_modulated']:
            case_path = intake / 'annular-constraint-correction-initial' / (case_name + '.json')
            own(case_path)
            case = json.loads(case_path.read_text())
            reference = OrthogonalReference(case)
            kappa_value = float(symbolic.sympify(case['normalization_kappa']))
            for intervals in [16, 32]:
                tag = case_name + '_local_N' + str(intervals)
                report['active_job'] = tag
                save()
                radii = numerical.linspace(5.875, 6.125, intervals + 1)
                basis = MixedActionBasis(radii)
                nodal = reference.adapted(0.15, radii)
                facial = reference.adapted(0.15, basis.faces)
                path = LocalQuadraticPath(basis, nodal, facial, reference.constants)
                position, velocity, defect, defect_time = path.path(0.0)
                verify(tag + '_orthogonal_parent_patch_within_owned_domain', reference.minimum_advanced >= 0 and reference.maximum_advanced <= 0.5 and numerical.min(nodal['jacobian']) > 0, {'advanced_time_range': [reference.minimum_advanced, reference.maximum_advanced], 'global_annulus_orthogonal_extension': False})
                old_data = reference.fields(nodal['old_time'], radii)
                old_exponential = numerical.exp(old_data['shift_ref'][0])
                old_radial = old_data['scalar_ref'][3] - reference.sigma * old_data['scalar_ref'][1]
                old_kinetic = 2 * old_data['scalar_ref'][1] * old_radial / old_exponential + nodal['spatial_f'] * old_radial**2
                new_kinetic = -(nodal['scalar_time'] / nodal['lapse'])**2 + nodal['spatial_f'] * nodal['gradient']**2
                verify(tag + '_physical_kinetic_scalar_preserved_by_slice_change', maximum(new_kinetic - old_kinetic) < 1e-13)
                derivative_controls = []
                for time_step in [1e-4, 5e-5]:
                    plus, minus = reference.adapted(0.15 + time_step, radii), reference.adapted(0.15 - time_step, radii)
                    errors = [maximum((plus[name] - minus[name]) / (2 * time_step) - nodal[target]) for name, target in [('lapse', 'lapse_time'), ('gradient', 'gradient_time'), ('scalar_time', 'scalar_second')]]
                    derivative_controls.append(errors)
                    verify(tag + '_adapted_time_jets_FD_' + str(time_step), max(errors) < 1e-6)

                displacement = [0.01 * numerical.sin(1.3 * radii), 0.01 * numerical.cos(basis.faces), 0.01 * numerical.cos(0.7 * radii), 0.02 * numerical.sin(basis.faces)]
                speed = [0.015 * numerical.cos(radii), 0.008 * numerical.sin(0.6 * basis.faces), 0.01 * numerical.sin(radii), 0.012 * numerical.cos(0.8 * basis.faces)]
                reduced, time_boundary, raw = path.quadratic(0.0, displacement, speed, raw=True)
                boundary_derivative = path.quadratic(1j * 1e-25, displacement, speed)[1].imag / 1e-25
                reduction_scale = max(abs(raw), abs(reduced), abs(boundary_derivative), 1e-25)
                verify(tag + '_history_accelerations_removed_with_exact_time_boundary', abs(raw - reduced - boundary_derivative) < 2e-8 * reduction_scale + 1e-22, {'raw': float(raw), 'reduced': float(reduced), 'boundary_derivative': float(boundary_derivative)})
                base_potential = path.exact_potential(0.0, displacement, speed, 0.0)
                flow_controls = []
                for amplitude in [0.01, 0.005]:
                    plus = path.exact_potential(0.0, displacement, speed, amplitude)
                    minus = path.exact_potential(0.0, displacement, speed, -amplitude)
                    measured = (plus + minus - 2 * base_potential) / (2 * amplitude**2)
                    allowance = 512 * numerical.finfo(float).eps * max(abs(plus), abs(minus), abs(base_potential)) / amplitude**2
                    verify(tag + '_independent_finite_time_link_second_variation_' + str(amplitude), abs(measured - raw) < 2e-3 * max(abs(raw), 1e-25) + allowance, {'measured': float(measured), 'predicted_raw': float(raw), 'allowance': float(allowance)})
                    flow_controls.append(float(abs(measured - raw)))

                bare_kinetic = basis.kinetic_matrix(position, velocity, defect, defect_time, reference.constants)
                factors, sampling = gram_matrices(radii.size)
                coefficient, gradient, hessian = coefficient_jets(velocity[0], nodal['gradient'], real_linear(basis.face_to_node, position[1]), position[2], radii, reference.constants)
                density_dual = real_linear(sampling.T, real_linear(factors, position[0])**2) / (2 * basis.spacing)
                kinetic_correction = numerical.diag(density_dual * hessian[0, 0])
                kinetic = bare_kinetic - kinetic_correction
                eigenvalues, eigenvectors = numerical.linalg.eigh(bare_kinetic)
                inverse_half = (eigenvectors / numerical.sqrt(eigenvalues)) @ eigenvectors.T
                relative_correction = maximum(numerical.linalg.eigvalsh(inverse_half @ kinetic_correction @ inverse_half))
                verify(tag + '_positive_scalar_Legendre_block_with_full_coefficient', numerical.min(numerical.linalg.eigvalsh(kinetic)) > 0, {'bare_minimum': float(eigenvalues[0]), 'modified_minimum': float(numerical.linalg.eigvalsh(kinetic)[0]), 'relative_Gram_mass_operator_norm': relative_correction})
                zero = pack_zero(position)
                pure_clock_kinetic = path.quadratic(0.0, zero, speed)[0]
                expected_clock_kinetic = numerical.dot(speed[0], kinetic_correction @ speed[0]) / 2
                verify(tag + '_only_scalar_velocity_squared_after_reduction', abs(pure_clock_kinetic - expected_clock_kinetic) < 1e-20 + 1e-9 * max(abs(expected_clock_kinetic), 1e-25))
                pure_metric_speed = pack_zero(position)
                pure_metric_speed[1:] = speed[1:]
                verify(tag + '_metric_velocity_squared_vanishes_without_projection', abs(path.quadratic(0.0, zero, pure_metric_speed)[0]) < 1e-25)
                bare_controls = []
                for step in [0.001, 0.0005]:
                    plus_velocity = [value + step * rate for value, rate in zip(velocity, speed)]
                    minus_velocity = [value - step * rate for value, rate in zip(velocity, speed)]
                    plus = basis.action(position, plus_velocity, defect, defect_time, reference.constants, kappa_value)
                    minus = basis.action(position, minus_velocity, defect, defect_time, reference.constants, kappa_value)
                    base_value = basis.action(position, velocity, defect, defect_time, reference.constants, kappa_value)
                    measured = (plus + minus - 2 * base_value) / (2 * step**2)
                    expected = numerical.dot(speed[0], bare_kinetic @ speed[0]) / 2
                    allowance = 256 * numerical.finfo(float).eps * max(abs(plus), abs(minus), abs(base_value)) / step**2
                    verify(tag + '_independent_bulk_velocity_Hessian_' + str(step), abs(measured - expected) < 1e-5 * max(abs(expected), 1e-25) + allowance)
                    bare_controls.append(float(abs(measured - expected)))

                if intervals == 16:
                    lower, upper = -0.001, 0.001
                    gauss, gauss_weights = numerical.polynomial.legendre.leggauss(8)
                    times, time_weights = gauss * (upper - lower) / 2, gauss_weights * (upper - lower) / 2
                    integrated_controls = []
                    for amplitude in [0.01, 0.005]:
                        direct_integral, reduced_integral = 0.0, 0.0
                        for time, weight in zip(times, time_weights):
                            base_position, base_velocity, base_defect, base_defect_time = path.path(time)
                            direction = [value + time * rate for value, rate in zip(displacement, speed)]
                            values = []
                            for sign in [1, -1, 0]:
                                varied_position = [value + sign * amplitude * delta for value, delta in zip(base_position, direction)]
                                varied_velocity = [value + sign * amplitude * delta for value, delta in zip(base_velocity, speed)]
                                bulk = basis.action(varied_position, varied_velocity, base_defect, base_defect_time, reference.constants, kappa_value)
                                potential = path.exact_potential(time, displacement, speed, sign * amplitude)
                                values.append((bulk, potential))
                            bulk_quadratic = (values[0][0] + values[1][0] - 2 * values[2][0]) / (2 * amplitude**2)
                            direct_integral += weight * (bulk_quadratic - (values[0][1] + values[1][1] - 2 * values[2][1]) / (2 * amplitude**2))
                            reduced_integral += weight * (bulk_quadratic - path.quadratic(time, displacement, speed)[0])
                        endpoint = path.quadratic(upper, displacement, speed)[1] - path.quadratic(lower, displacement, speed)[1]
                        discrepancy = abs(direct_integral - reduced_integral + endpoint)
                        control_scale = abs(endpoint) + (upper - lower) * abs(raw)
                        verify(tag + '_combined_GR_matter_clock_action_integrated_' + str(amplitude), discrepancy < 2e-3 * max(control_scale, 1e-25) + 1e-18, {'error': float(discrepancy), 'endpoint_term': float(endpoint), 'scope': 'Same bulk second difference on both sides; independently tests clock completion and boundary within combined action, not an independent Hessian proof for every bulk position block.'})
                        integrated_controls.append({'amplitude': amplitude, 'discrepancy': float(discrepancy), 'endpoint': float(endpoint)})

                    count = sum(value.size for value in position)
                    metric_count = count - radii.size
                    clock_cross = numerical.zeros((count, count))
                    units = [direction_unit(position, index) for index in range(count)]
                    position_only = [path.quadratic(0.0, unit, zero)[0] for unit in units]
                    speed_only = [path.quadratic(0.0, zero, unit)[0] for unit in units]
                    report['active_job'] = tag + '_complete_clock_position_velocity_block'
                    save()
                    for velocity_index, speed_unit in enumerate(units):
                        for position_index, position_unit in enumerate(units):
                            clock_cross[velocity_index, position_index] = -(path.quadratic(0.0, position_unit, speed_unit)[0] - position_only[position_index] - speed_only[velocity_index])
                    scalar_count, face_count = radii.size, basis.faces.size
                    mass_slice = slice(scalar_count, scalar_count + face_count)
                    lapse_slice = slice(scalar_count + face_count, 2 * scalar_count + face_count)
                    shift_slice = slice(2 * scalar_count + face_count, count)
                    radius_q, radial_scale, unused_scale_t, unused_scale_r, lapse_q, unused_lapse_r, unused_shift, unused_shift_r, unused_scalar, unused_time, unused_gradient = basis.unpack(position, velocity, defect, defect_time, reference.constants)
                    gravity_pairing = basis.face_value.T @ ((basis.quadrature_weights * radial_scale**3 / (kappa_value * lapse_q))[:, None] * basis.face_value)
                    metric_cross = clock_cross[scalar_count:, scalar_count:].copy()
                    metric_cross[:face_count, face_count + scalar_count:] += gravity_pairing
                    symplectic = metric_cross - metric_cross.T
                    singular_values = numerical.linalg.svd(symplectic, compute_uv=False)
                    rank_threshold = 1e-10 * singular_values[0]
                    rank = int(numerical.sum(singular_values > rank_threshold))
                    verify(tag + '_metric_first_order_rank_not_increased', rank == 2 * face_count, {'rank': rank, 'baseline_rank': 2 * face_count, 'metric_variables': metric_count, 'lapse_null_count': metric_count - rank, 'rank_threshold': float(rank_threshold), 'full_Dirac_constraint_analysis': False})
                    forbidden = max(maximum(clock_cross[mass_slice]), maximum(clock_cross[lapse_slice]), maximum(clock_cross[shift_slice, lapse_slice]), maximum(clock_cross[shift_slice, mass_slice]))
                    verify(tag + '_clock_cross_block_matches_local_time_structure', forbidden < 1e-10 * max(maximum(clock_cross), 1e-25) + 1e-20, {'forbidden_block_max': forbidden, 'clock_cross_max': maximum(clock_cross)})
                    artifact = destination / (tag + '_quadratic_blocks.npz')
                    numerical.savez_compressed(artifact, radius=radii, faces=basis.faces, scalar_kinetic=kinetic, baseline_scalar_kinetic=bare_kinetic, clock_position_velocity=clock_cross, metric_first_order_antisymmetric=symplectic, gravity_pairing=gravity_pairing, integrability_defect=defect, integrability_defect_time=defect_time)
                    report['outputs'][str(artifact.relative_to(root))] = hashlib.sha256(artifact.read_bytes()).hexdigest()
                report['samples'].append({'case': case_name, 'intervals': intervals, 'patch': [5.875, 6.125], 'declared_validation_time_jet_window': [-0.001, 0.001], 'reference_tau_anchor': 0.15, 'relative_Gram_kinetic_correction': relative_correction, 'minimum_scalar_kinetic_eigenvalue': float(numerical.linalg.eigvalsh(kinetic)[0]), 'integrability_defect_max': maximum(defect), 'integrability_defect_time_max': maximum(defect_time), 'clock_time_boundary': float(time_boundary), 'finite_link_quadratic_errors': flow_controls, 'physical_claim': False})
                save()
        verify('four_actual_patch_discretizations_completed', len(report['samples']) == 4)
        verify('all_owned_inputs_unchanged', all(hashlib.sha256((root / name).read_bytes()).hexdigest() == digest for name, digest in report['inputs'].items()))
        verify('no_bytecode_cache', not (root / 'scripts/__pycache__').exists())
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
