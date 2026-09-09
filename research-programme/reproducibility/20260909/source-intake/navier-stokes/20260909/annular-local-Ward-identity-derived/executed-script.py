import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from annular_adm_mixed_action_20260909 import MixedActionBasis, real_linear
    from annular_constraint_routhian_20260909 import ConstraintRouthian
    from annular_local_ward_identity_20260909 import LocalWardIdentity

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260909'
    source = intake / 'annular-constraint-routhian-derived'
    destination = intake / 'annular-local-Ward-identity-derived'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': {}, 'outputs': {}, 'checks': [], 'samples': [], 'valid_for_physics_claim': False, 'scope': 'Derive full local time-generator Ward identity of the saved ADM+Gram first variation, with independent nodal values and slopes, explicit bulk reconstruction/product defects, Gram metric coefficient and link defects, lifting Euler work, and boundary reactions. Test ALL shift directions through a full-row-rank generator, retain the nonzero shift residual, and verify off-shell controls. This identifies the finite-action remainder; it does not repair it or establish stable time evolution.'}
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
        previous_path = intake / 'annular-constraint-routhian-final-integrity.json'
        own(previous_path)
        previous = json.loads(previous_path.read_text())
        verify('previous_constraint_and_tangent_result_complete', previous['state'] == 'complete' and previous['final_check_count'] == 370)
        verify('all_previous_sources_and_results_unchanged', all(own(root / name) == digest for name, digest in {**previous['inputs'], **previous['outputs']}.items()))
        for name in ['annular_local_ward_identity_20260909.py', 'derive_annular_local_ward_identity_20260909.py']:
            path = root / 'scripts' / name
            own(path)
            compile(path.read_bytes(), str(path), 'exec')

        mass, mass_r, lapse, scalar, velocity, gradient, radius, mass_time, mass_rt, lapse_time, scalar_second, gradient_time, quartic, sextic, potential_mass, cosmological, kappa, generator, generator_r, generator_t, shift = symbolic.symbols('mu mur N chi q w r mut murt Nt qt wt b2 b3 mc Lambda kappa f fr ft V', real=True)
        spatial_f = 1 - 2 * mass / radius - cosmological * radius**2 / 3
        scale = spatial_f**(-symbolic.Rational(1, 2))
        kinetic = -velocity**2 / lapse**2 + spatial_f * gradient**2
        matter = -kinetic / 2 - potential_mass**2 * scalar**2 / 2 + quartic * kinetic**2 + sextic * kinetic**3
        principal = 1 - 4 * quartic * kinetic - 6 * sextic * kinetic**2
        density = lapse * scale * mass_r / kappa + radius**2 * lapse * scale * matter
        variables = [mass, mass_r, lapse, scalar, velocity, gradient]
        rates = [mass_time, mass_rt, lapse_time, velocity, scalar_second, gradient_time]
        variations = [generator * mass_time, generator * mass_rt + generator_r * mass_time, generator * lapse_time + generator_t * lapse, generator * velocity, generator * scalar_second + generator_t * velocity, generator * gradient_time + generator_r * velocity]
        shift_derivative = mass_time / (kappa * lapse * spatial_f**symbolic.Rational(3, 2)) - radius**2 * scale * principal * velocity * gradient / lapse
        variation = sum(symbolic.diff(density, variable) * change for variable, change in zip(variables, variations)) - shift_derivative * lapse**2 * spatial_f * generator_r
        time_derivative = sum(symbolic.diff(density, variable) * rate for variable, rate in zip(variables, rates))
        verify('symbolic_pointwise_ADM_matter_time_covariance_before_projection', symbolic.simplify(variation - generator * time_derivative - generator_t * density) == 0)
        full_kinetic = -(velocity - shift * gradient)**2 / lapse**2 + spatial_f * gradient**2
        full_principal = 1 - 4 * quartic * full_kinetic - 6 * sextic * full_kinetic**2
        full_slope = -4 * quartic - 12 * sextic * full_kinetic
        coefficient = radius**2 * lapse * scale * (full_principal * (spatial_f - shift**2 / lapse**2) + 2 * full_slope * (spatial_f * gradient + shift * (velocity - shift * gradient) / lapse**2)**2)
        verify('symbolic_Gram_spatial_generator_cancellation_a_w_q_equals_gamma_a_V', symbolic.simplify((symbolic.diff(coefficient, gradient) * velocity - lapse**2 * spatial_f * symbolic.diff(coefficient, shift)).subs(shift, 0)) == 0)
        verify('symbolic_Gram_temporal_density_weight_a_q_q_plus_a_N_N_equals_a', symbolic.simplify((symbolic.diff(coefficient, velocity) * velocity + symbolic.diff(coefficient, lapse) * lapse - coefficient).subs(shift, 0)) == 0)

        initial = json.loads((source / 'status.json').read_text())
        for sample in initial['samples']:
            case_name, intervals, branch = sample['case'], sample['intervals'], sample['branch']
            tag = case_name + '_N' + str(intervals) + '_' + branch
            report['active_job'] = tag
            save()
            case = json.loads((intake / 'annular-constraint-correction-initial' / (case_name + '.json')).read_text())
            constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
            with numerical.load(source / (tag + '.npz')) as loaded:
                arrays = {name: loaded[name].copy() for name in loaded.files}
            basis = MixedActionBasis(arrays['radius'])
            system = ConstraintRouthian(basis, arrays['scalar'], arrays['defect'], arrays['defect_time'], constants, float(symbolic.sympify(case['normalization_kappa'])), arrays['momentum'], arrays['outer_clock'][0])
            identity = LocalWardIdentity(system, arrays)
            result = identity.evaluate(branch == 'Gram')
            singular = numerical.linalg.svd(result['shift_generator'], compute_uv=False)
            verify(tag + '_all_shift_directions_covered_by_enriched_generator', singular.size == system.face_count and singular[-1] > 1e-10 * singular[0], {'largest_singular_value': float(singular[0]), 'smallest_singular_value': float(singular[-1]), 'generator_count': identity.generator_count, 'shift_face_count': system.face_count})
            verify(tag + '_full_Ward_identity_including_boundary_and_lifting', maximum(result['identity_error']) < 2e-11 + 1e-9 * maximum(result['shift_work']), {'maximum_error': maximum(result['identity_error'])})
            verify(tag + '_nonzero_shift_residual_is_not_reclassified_as_zero', maximum(arrays['shift_residual']) > 1e-10)
            constant = numerical.concatenate([numerical.ones(system.node_count), numerical.zeros(system.node_count)])
            verify(tag + '_constant_generator_has_no_shift_and_closes_with_boundary_work', maximum(result['shift_generator'] @ constant) < 1e-10 and abs(numerical.dot(result['predicted_shift_work'], constant)) < 1e-11)
            verify(tag + '_omitting_lifting_work_breaks_identity', maximum(result['identity_error'] - result['lifting_work']) > 100 * max(maximum(result['identity_error']), 1e-14))
            verify(tag + '_omitting_endpoint_reactions_breaks_identity', maximum(result['identity_error'] - result['scalar_endpoint_and_bulk_work'] - result['mass_boundary_and_bulk_work']) > 100 * max(maximum(result['identity_error']), 1e-14))
            if branch == 'Gram':
                verify(tag + '_omitting_connection_reconstruction_remainder_breaks_identity', maximum(result['identity_error'] - result['Gram_link_remainder']) > 100 * max(maximum(result['identity_error']), 1e-14))
            norm_residual = float(numerical.linalg.norm(arrays['shift_residual']))
            sharp_bound = float(numerical.linalg.norm(result['predicted_shift_work']) / singular[-1])
            triangle_bound = float(sum(numerical.linalg.norm(result[name]) for name in ['bulk_remainder', 'Gram_remainder', 'lifting_work', 'scalar_endpoint_and_bulk_work', 'mass_boundary_and_bulk_work', 'lapse_constraint_derivative_work']) / singular[-1])
            verify(tag + '_full_vector_norm_bound_without_filtering', norm_residual <= sharp_bound + 1e-12 and sharp_bound <= triangle_bound + 1e-12)

            if intervals == 16:
                state = identity.state()
                normalized = (basis.radii - basis.radii[0]) / (basis.radii[-1] - basis.radii[0])
                probe = numerical.concatenate([numerical.sin(2 * numerical.pi * normalized), basis.spacing * 2 * numerical.pi * numerical.cos(2 * numerical.pi * normalized) / (basis.radii[-1] - basis.radii[0])])
                mass_slice, lapse_slice, velocity_slice = system.slices
                fields = [arrays['scalar'], arrays['corrected'][mass_slice], arrays['corrected'][lapse_slice], numerical.zeros(system.face_count)]
                velocities = [arrays['corrected'][velocity_slice], arrays['packed_speed'][mass_slice], arrays['packed_speed'][lapse_slice], numerical.zeros(system.face_count)]
                field_direction = [state['scalar_time'] * (identity.node_value @ probe), state['mass_time'] * (identity.face_value @ probe), state['lapse_time'] * (identity.node_value @ probe), state['shift_generator'] @ probe]
                velocity_direction = [state['scalar_second'] * (identity.node_value @ probe), numerical.zeros(system.face_count), numerical.zeros(system.node_count), numerical.zeros(system.face_count)]
                changed_fields = [value + 1j * 1e-25 * change for value, change in zip(fields, field_direction)]
                changed_velocities = [value + 1j * 1e-25 * change for value, change in zip(velocities, velocity_direction)]
                raw_variation = basis.action(changed_fields, changed_velocities, arrays['defect'] + 1j * 1e-25 * (state['lifting_generator'] @ probe), arrays['defect_time'] + 1j * 1e-25 * (state['lifting_generator_time'] @ probe), constants, system.kappa).imag / 1e-25
                weighted_time = numerical.dot(basis.quadrature_weights * (identity.quad_value @ probe), identity.state(1j * 1e-25)['bulk_density'].imag / 1e-25)
                predicted = numerical.dot(sum(state['amplitude_parts'].values()), probe)
                verify(tag + '_independent_unfixed_bulk_variation_has_derived_reconstruction_defect', abs(raw_variation - weighted_time - predicted) < 1e-12)
                changed_fields = [value.astype(complex) for value in fields]
                changed_velocities = [value.astype(complex) for value in velocities]
                changed_fields[2] += 1j * 1e-25 * fields[2] * (identity.node_value @ probe)
                changed_velocities[0] += 1j * 1e-25 * state['scalar_time'] * (identity.node_value @ probe)
                temporal_variation = basis.action(changed_fields, changed_velocities, arrays['defect'], arrays['defect_time'] + 1j * 1e-25 * (state['lifting_generator'] @ probe), constants, system.kappa).imag / 1e-25
                weighted = numerical.dot(basis.quadrature_weights * (identity.quad_value @ probe), state['bulk_density'])
                verify(tag + '_independent_temporal_generator_coefficient', abs(temporal_variation - weighted - numerical.dot(sum(state['time_parts'].values()), probe)) < 1e-12)
                for step in [0.001, 0.0005]:
                    finite_time = (sum(identity.state(step)['time_parts'].values()) - sum(identity.state(-step)['time_parts'].values())) / (2 * step)
                    exact_time = sum(identity.state(1j * 1e-25)['time_parts'].values()).imag / 1e-25
                    verify(tag + '_independent_reconstruction_time_derivative_' + str(step), maximum(finite_time - exact_time) < 1e-8)
                altered = {name: value.copy() for name, value in arrays.items()}
                altered['packed_speed'][mass_slice] += 0.001 * numerical.sin(19 * basis.faces)
                altered['packed_speed'][lapse_slice] += 0.01 * numerical.cos(17 * basis.radii)
                altered['packed_speed'][velocity_slice] += 0.01 * numerical.sin(13 * basis.radii)
                altered['shift_residual'] = arrays['pairing'] @ altered['packed_speed'][mass_slice] + arrays['matter_shift'] - arrays['Gram_shift']
                off_shell = LocalWardIdentity(system, altered).evaluate(branch == 'Gram')
                verify(tag + '_off_shell_Ward_identity_with_unsatisfied_Euler_rows', maximum(off_shell['identity_error']) < 2e-11 and maximum(off_shell['lapse_constraint_derivative_work']) > 1e-6 and maximum(off_shell['shift_work']) > 1e-5)

            artifact = destination / (tag + '.npz')
            numerical.savez_compressed(artifact, faces=basis.faces, radius=basis.radii, shift_residual=arrays['shift_residual'], generator_singular_values=singular, **result)
            report['outputs'][str(artifact.relative_to(root))] = hashlib.sha256(artifact.read_bytes()).hexdigest()
            report['samples'].append({'case': case_name, 'intervals': intervals, 'branch': branch, 'maximum_identity_error': maximum(result['identity_error']), 'full_shift_residual_norm': norm_residual, 'sharp_finite_vector_bound': sharp_bound, 'triangle_finite_vector_bound': triangle_bound, 'full_shift_generator_condition': float(singular[0] / singular[-1]), 'maximum_remainder_by_term': {name: maximum(result[name]) for name in ['bulk_remainder', 'Gram_coefficient_remainder', 'Gram_link_remainder', 'lifting_work', 'scalar_endpoint_and_bulk_work', 'mass_boundary_and_bulk_work']}, 'full_constraint_preservation': False, 'bound_scope': 'Measured finite matrix and state, not a uniform continuum or interval-certified bound.'})
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
