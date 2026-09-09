import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from annular_adm_mixed_action_20260909 import MixedActionBasis, OrthogonalReference, real_linear
    from annular_adm_clock_quadratic_20260909 import LocalQuadraticPath
    from annular_constraint_routhian_20260909 import ConstraintRouthian

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260909'
    destination = intake / 'annular-constraint-routhian-derived'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': {}, 'outputs': {}, 'checks': [], 'samples': [], 'valid_for_physics_claim': False, 'scope': 'Nonlinear initial-slice radial and scalar Legendre constraints in a declared local patch variational boundary problem. Matched GR/P(X) and Gram runs with the same interior canonical momentum, scalar position, lifting, inner mass, outer clock and fixed scalar endpoint velocities. Square direct Newton solves, no least-squares or row projection. Differentiated-constraint/shift compatibility is measured separately, not assumed from an initial root. No global boundary, local-GR or causal-evolution certificate.'}
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
        prior_path = intake / 'annular-adm-quadratic-final-integrity.json'
        own(prior_path)
        prior = json.loads(prior_path.read_text())
        verify('prior_integrity_complete', prior['state'] == 'complete')
        verify('prior_sources_and_outputs_unchanged', all(own(root / name) == digest for name, digest in {**prior['inputs'], **prior['outputs']}.items()))
        for name in ['annular_constraint_routhian_20260909.py', 'derive_annular_constraint_routhian_20260909.py']:
            own(root / 'scripts' / name)
            compile((root / 'scripts' / name).read_bytes(), name, 'exec')

        radius, mass, mass_r, clock, clock_r, velocity, gradient, scalar, kappa, quartic, sextic, potential_mass, cosmological = symbolic.symbols('r mu mur E Er q w chi kappa b2 b3 mc Lambda', real=True)
        spatial_f = 1 - 2 * mass / radius - cosmological * radius**2 / 3
        kinetic = -velocity**2 / (clock**2 * spatial_f) + spatial_f * gradient**2
        matter = -kinetic / 2 - potential_mass**2 * scalar**2 / 2 + quartic * kinetic**2 + sextic * kinetic**3
        principal = 1 - 4 * quartic * kinetic - 6 * sextic * kinetic**2
        density = clock * mass_r / kappa + radius**2 * clock * matter
        hamiltonian = mass_r / kappa + radius**2 * (matter - principal * velocity**2 / (clock**2 * spatial_f))
        radial = -clock_r / kappa + radius * clock * principal * (gradient**2 + velocity**2 / (clock**2 * spatial_f**2))
        verify('symbolic_GR_Hamiltonian_constraint_in_E_NL_chart', symbolic.simplify(symbolic.diff(density, clock) - hamiltonian) == 0)
        verify('symbolic_GR_radial_clock_constraint_in_E_NL_chart', symbolic.simplify(symbolic.diff(density, mass) - clock_r / kappa - radial) == 0)
        verify('symbolic_outer_clock_Legendre_boundary_term', symbolic.diff(density, mass_r) == clock / kappa)

        for case_name in ['canonical', 'nonlinear_modulated']:
            case_path = intake / 'annular-constraint-correction-initial' / (case_name + '.json')
            own(case_path)
            case = json.loads(case_path.read_text())
            reference = OrthogonalReference(case)
            kappa_value = float(symbolic.sympify(case['normalization_kappa']))
            for intervals in [16, 32, 64]:
                tag = case_name + '_N' + str(intervals)
                report['active_job'] = tag
                save()
                basis = MixedActionBasis(numerical.linspace(5.875, 6.125, intervals + 1))
                nodal, facial = reference.adapted(0.15, basis.radii), reference.adapted(0.15, basis.faces)
                path = LocalQuadraticPath(basis, nodal, facial, reference.constants)
                position, velocity_fields, defect, defect_time = path.path(0.0)
                seed = numerical.concatenate([position[1], position[2], velocity_fields[0]])
                outer_f = 1 - 2 * position[1][-1] / basis.faces[-1] - reference.constants['Lambda'] * basis.faces[-1]**2 / 3
                outer_clock = position[2][-1] / numerical.sqrt(outer_f)
                outer_clock_time = velocity_fields[2][-1] / numerical.sqrt(outer_f) + position[2][-1] * velocity_fields[1][-1] / (basis.faces[-1] * outer_f**1.5)
                system = ConstraintRouthian(basis, position[0], defect, defect_time, reference.constants, kappa_value, numerical.zeros_like(position[0]), outer_clock)
                system.momentum = system.evaluate(seed, False)[1][system.slices[2]].copy()
                system.momentum[[0, -1]] = 0
                scaling = system.scaling(seed)
                verify(tag + '_correct_free_equation_count_and_lapse_not_fixed', len(system.free) == 3 * basis.radii.size - 2 and not any(index in system.fixed for index in range(system.face_count, system.face_count + system.node_count)))
                verify(tag + '_nonzero_lifting_and_owned_patch_preserved', maximum(defect) > 1e-6 and maximum(defect_time) > 1e-6 and reference.minimum_advanced >= 0 and reference.maximum_advanced <= 0.5)
                direct_bulk = basis.action(position, velocity_fields, defect, defect_time, reference.constants, kappa_value)
                expected = direct_bulk - outer_clock * seed[system.face_count - 1] / kappa_value - numerical.dot(system.momentum, seed[system.slices[2]])
                verify(tag + '_Routhian_matches_full_shift_unfixed_ADM_at_zero_shift', abs(system.evaluate(seed, False)[0] - expected) < 1e-12)
                radius_q, scale_q, unused_scale_t, unused_scale_r, lapse_q, unused_lapse_r, unused_shift, unused_shift_r, unused_scalar, scalar_q, gradient_q = basis.unpack(position, velocity_fields, defect, defect_time, reference.constants)
                kinetic_q = -(scalar_q / lapse_q)**2 + (gradient_q / scale_q)**2
                principal_q = 1 - 4 * reference.constants['b2'] * kinetic_q - 6 * reference.constants['b3'] * kinetic_q**2
                independent_momentum = real_linear(basis.scalar_value.T, basis.quadrature_weights * radius_q**2 * scale_q * principal_q * scalar_q / lapse_q)
                verify(tag + '_common_canonical_phase_data_independently_verified', maximum(independent_momentum[1:-1] - system.momentum[1:-1]) < 1e-14)

                roots = {}
                for include_gram, branch_name in [(False, 'GR'), (True, 'Gram')]:
                    label = tag + '_' + branch_name
                    direction = numerical.concatenate([0.02 * numerical.sin(1.7 * basis.faces), 0.01 * numerical.cos(2.3 * basis.radii), 0.001 * numerical.sin(3.1 * basis.radii)])
                    direction[system.fixed] = 0
                    value, analytic_gradient, analytic_hessian = system.evaluate(seed, include_gram)
                    complex_gradient = numerical.empty_like(seed)
                    for index in range(seed.size):
                        changed = seed.astype(complex)
                        changed[index] += 1j * 1e-25
                        complex_gradient[index] = system.evaluate(changed, include_gram, hessian=False)[0].imag / 1e-25
                    verify(label + '_independent_full_action_gradient_complex_step', maximum(complex_gradient - analytic_gradient) < 2e-12)
                    verify(label + '_analytic_Hessian_symmetry', maximum(analytic_hessian - analytic_hessian.T) < 2e-12)
                    exact_direction = real_linear(analytic_hessian, direction)
                    for step in [0.001, 0.0005]:
                        measured = (system.evaluate(seed + step * direction, include_gram, hessian=False)[1] - system.evaluate(seed - step * direction, include_gram, hessian=False)[1]) / (2 * step)
                        verify(label + '_independent_Hessian_direction_' + str(step), maximum(measured - exact_direction) < 1e-8 * max(maximum(exact_direction), 1e-20) + 5e-11)

                    corrected, history, solved, reason = system.solve(seed, include_gram, scaling)
                    final_value, final_gradient, final_hessian = system.evaluate(corrected, include_gram)
                    roots[branch_name] = corrected
                    verify(label + '_all_free_constraints_solved', solved, {'reason': reason, 'iterations': len(history) - 1, 'history': history})
                    verify(label + '_fixed_mass_and_scalar_velocity_endpoints_exact', numerical.array_equal(corrected[system.fixed], seed[system.fixed]))
                    verify(label + '_residual_reduction_without_projection', maximum(final_gradient[system.free] / scaling[1]) < 1e-12 and maximum(final_gradient[system.free]) < 1e-10 and history[-1]['scaled_residual_max'] < 1e-5 * history[0]['scaled_residual_max'])
                    verify(label + '_nonzero_boundary_reactions_not_counted_as_failed_bulk_rows', maximum(final_gradient[system.fixed]) > 1)
                    root_f = 1 - 2 * corrected[system.face_count - 1] / basis.faces[-1] - reference.constants['Lambda'] * basis.faces[-1]**2 / 3
                    trace_clock = corrected[system.face_count + system.node_count - 1] / numerical.sqrt(root_f)
                    boundary_disabled_gradient = final_gradient.copy()
                    boundary_disabled_gradient[system.face_count - 1] += outer_clock / kappa_value
                    verify(label + '_omitted_boundary_term_negative_control_detected', maximum(boundary_disabled_gradient[system.free]) > 1)

                    force = system.scalar_force(corrected, include_gram)
                    scalar_direction = 0.01 * numerical.sin(7 * basis.radii)
                    altered_system = ConstraintRouthian(basis, position[0] + 1j * 1e-25 * scalar_direction, defect, defect_time, reference.constants, kappa_value, system.momentum, outer_clock)
                    measured_force = altered_system.evaluate(corrected, include_gram, hessian=False)[0].imag / 1e-25
                    verify(label + '_independent_scalar_Hamilton_force', abs(measured_force - numerical.dot(force, scalar_direction)) < 1e-12)
                    tangent = system.constraint_tangent(corrected, include_gram, -real_linear(basis.derivative, path.acceleration), path.acceleration, outer_clock_time)
                    verify(label + '_differentiated_constraints_solved', maximum(tangent['constraint_derivative_residual']) < 1e-11)
                    verify(label + '_mass_shift_pairing_positive_and_flux_solve_exact', numerical.linalg.eigvalsh(tangent['pairing'])[0] > 0 and maximum(real_linear(tangent['pairing'], tangent['shift_mass_speed']) + tangent['matter_shift'] - tangent['Gram_shift']) < 1e-14)
                    verify(label + '_inner_mass_rate_is_flux_derived_not_reference_imposed', abs(tangent['packed_speed'][0] - tangent['shift_mass_speed'][0]) < 1e-15)

                    if intervals == 16:
                        displaced_seed = seed + 0.001 * direction
                        repeated, repeat_history, repeat_solved, repeat_reason = system.solve(displaced_seed, include_gram, scaling)
                        verify(label + '_independent_perturbed_start_recovers_same_root', repeat_solved and maximum(repeated - corrected) < 2e-10, {'reason': repeat_reason, 'iterations': len(repeat_history) - 1, 'maximum_root_difference': maximum(repeated - corrected)})
                        affine = numerical.load(intake / 'annular-adm-affine-and-boundary-derived' / (case_name + '_affine_covectors.npz'))
                        prefix = 'candidate_' if include_gram else 'baseline_'
                        expected_mass = affine[prefix + 'spatial_mass'].copy()
                        expected_mass[-1] -= outer_clock / kappa_value
                        verify(label + '_saved_affine_geometry_forcing_reused_with_declared_boundary', maximum(analytic_gradient[system.slices[0]] - expected_mass) < 1e-12 and maximum(analytic_gradient[system.slices[1]] - affine[prefix + 'lapse']) < 1e-12)

                    artifact = destination / (label + '.npz')
                    numerical.savez_compressed(artifact, radius=basis.radii, faces=basis.faces, seed=seed, corrected=corrected, free=system.free, fixed=system.fixed, gradient_seed=analytic_gradient, gradient_final=final_gradient, Hessian_final=final_hessian, row_scale=scaling[1], unknown_scale=scaling[0], momentum=system.momentum, scalar=position[0], defect=defect, defect_time=defect_time, defect_acceleration=-real_linear(basis.derivative, path.acceleration), endpoint_acceleration=path.acceleration[[0, -1]], outer_clock=numerical.array([outer_clock, outer_clock_time]), **tangent)
                    report['outputs'][str(artifact.relative_to(root))] = hashlib.sha256(artifact.read_bytes()).hexdigest()
                    mass_speed_mismatch = tangent['packed_speed'][system.slices[0]] - tangent['shift_mass_speed']
                    report['samples'].append({'case': case_name, 'intervals': intervals, 'branch': branch_name, 'root_solved': solved, 'iterations': len(history) - 1, 'scaled_residual_max': history[-1]['scaled_residual_max'], 'raw_free_residual_max': maximum(final_gradient[system.free]), 'maximum_correction_by_field_mass_lapse_scalar_speed': [maximum((corrected - seed)[field]) for field in system.slices], 'outer_clock_trace_minus_natural_datum': float(trace_clock - outer_clock), 'fixed_reactions_mass_inner_scalar_endpoints': final_gradient[system.fixed].tolist(), 'condition_number': history[-1]['condition_number'], 'scalar_Legendre_minimum': history[-1]['branch']['minimum_scalar_Legendre_eigenvalue'], 'tangent_mass_rate_mismatch_max': maximum(mass_speed_mismatch), 'tangent_shift_residual_max': maximum(tangent['shift_residual']), 'tangent_flux_mass_rate_max': maximum(tangent['shift_mass_speed']), 'inner_flux_rate_minus_reference': float(tangent['shift_mass_speed'][0] - velocity_fields[1][0]), 'all_shift_rows_satisfied_by_constraint_tangent': maximum(tangent['shift_residual']) < 1e-10, 'scope': 'Local initial constraints solved; all remaining shift rows are diagnostics, not erased or silently fitted.', 'history': history})
                    save()
                difference = roots['Gram'] - roots['GR']
                print(json.dumps({'tag': tag, 'candidate_minus_GR_max_by_field': [maximum(difference[field]) for field in system.slices]}), flush=True)

        verify('all_owned_inputs_unchanged', all(hashlib.sha256((root / name).read_bytes()).hexdigest() == digest for name, digest in report['inputs'].items()))
        verify('all_output_arrays_unchanged', all(hashlib.sha256((root / name).read_bytes()).hexdigest() == digest for name, digest in report['outputs'].items()))
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
