import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from scipy.interpolate import CubicHermiteSpline
    from annular_adm_mixed_action_20260909 import MixedActionBasis, linear_value_gradient
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian
    from annular_canonical_nodal_data_20260911 import CanonicalInitialNodalData
    from annular_canonical_mesh_transfer_20260911 import fields, project_momentum, split_quadrature, newton_initial_data

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260911'
    destination = intake / 'annular-canonical-continuation-control-attempt01'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'inputs': {}, 'outputs': {}, 'checks': [], 'samples': [], 'started_utc': datetime.now(timezone.utc).isoformat(), 'interval_certificate': False, 'valid_for_physics_claim': False, 'new_evolution': False, 'strict_control_policy': 'N32 retains every original fine source, free slope coefficient, inner mass, lapse, configuration, clock and the original mesh-dependent GR flux. Only initial guess changes; solver cap also increases to35, recorded iterations distinguish that effect.'}

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = digest(path)

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    def archive(path):
        own(path)
        with numerical.load(path, allow_pickle=False) as saved:
            return {name: saved[name].copy() for name in saved.files}

    save()
    try:
        prior_path = intake / 'annular-canonical-mesh-continuation-attempt02/status.json'
        own(prior_path)
        prior = json.loads(prior_path.read_text())
        check('continuation_finished_checks_pass', prior['state'] == 'complete' and all(item['passed'] for item in prior['checks']))
        for table in ['inputs', 'outputs']:
            for name, expected in prior[table].items():
                if digest(root / name) != expected:
                    raise RuntimeError('Prior evidence changed: ' + name)
                report['inputs'][name] = expected
        own(Path(__file__))
        snapshot = destination / ('executed-' + Path(__file__).name)
        snapshot.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        parameter_path = root / 'source-intake/navier-stokes/20260909/annular-constraint-correction-initial/canonical.json'
        own(parameter_path)
        constants = {name: float(symbolic.sympify(value)) for name, value in json.loads(parameter_path.read_text())['parameters'].items()}
        roots = root / 'source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02'

        def build(mesh, branch, boundary):
            source = archive(roots / ('canonical_N' + str(mesh) + '_' + branch + '_sample0.npz'))
            basis = MixedActionBasis(source['basis_radii'])
            count = basis.radii.size
            configuration, momenta = source['original_configuration'], source['original_momenta']
            packed = (source['initial_root_box_lower'] + source['initial_root_box_upper']) / 2
            system = ReleasedHermiteRouthian(basis, configuration[:count], configuration[count:], constants, .1, momenta[:count], momenta[count:], source['affine_clock'][0], MetricLinkQuadrature(basis))
            velocity = packed[system.slices[2].start:]
            if boundary is None:
                port = archive(intake / 'annular-initial-mesh-control-attempt01' / ('canonical_N' + str(mesh) + '_GR_sample0.npz'))['mass_rate'][0]
                boundary = numerical.array([port, velocity[0], velocity[count - 1]])
            return CanonicalInitialNodalData(system, packed, configuration, branch != 'GR', boundary)

        for branch in ['GR', 'metric_Gram']:
            coarse_saved = archive(intake / 'annular-canonical-initial-data-nodal01' / ('canonical_N16_' + branch + '_sample0.npz'))
            coarse = build(16, branch, coarse_saved['boundary_velocity'])
            coarse.pi_coeff_seed = coarse_saved['pi_coefficients'].copy()
            coarse_mass, coarse_pi, coarse_reactions = coarse.set_state(coarse_saved['state'])
            identity, diagnostics = project_momentum(coarse, coarse, coarse_mass, coarse_pi, order=12)
            check(branch + '_physical_transfer_same_space_identity', abs(identity - coarse_pi).max() < 1e-11, float(abs(identity - coarse_pi).max()))
            points, weights = split_quadrature([coarse], 9)
            direct_fields = fields(coarse, coarse_mass, coarse_pi, points)
            spline = CubicHermiteSpline(coarse.basis.radii, coarse_pi[:coarse.count], coarse.basis.derivative @ coarse_pi[:coarse.count] + coarse_pi[coarse.count:] / coarse.basis.spacing)
            source_mass = numerical.interp(points, coarse.basis.faces, coarse.packed[coarse.system.slices[0]])
            source_lapse = numerical.interp(points, coarse.basis.radii, coarse.lapse_seed)
            independent_pi = points**2 * spline(points) / (source_lapse * numerical.sqrt(1 - 2 * source_mass / points))
            check(branch + '_independent_physical_pi_reconstruction', abs(independent_pi - direct_fields['pi']).max() < 1e-12, float(abs(independent_pi - direct_fields['pi']).max()))
            distance = numerical.min(abs(points[:, None] - numerical.unique(numerical.concatenate([coarse.basis.faces, coarse.basis.radii]))[None, :]))
            step = min(1e-6, float(distance) / 10)
            derivative = (fields(coarse, coarse_mass, coarse_pi, points + step)['pi'] - fields(coarse, coarse_mass, coarse_pi, points - step)['pi']) / (2 * step)
            derivative_error = float(abs(derivative - direct_fields['pi_gradient']).max() / max(1., float(abs(direct_fields['pi_gradient']).max())))
            check(branch + '_piecewise_physical_derivative_control', derivative_error < 1e-6, derivative_error)
            fine = build(32, branch, None)
            projected_pi, unused_projection = project_momentum(coarse, fine, coarse_mass, coarse_pi)
            projected_mass = linear_value_gradient(coarse.basis.faces, fine.basis.faces)[0] @ coarse_mass[:coarse.face_count]
            check(branch + '_strict_control_inner_mass_unchanged', projected_mass[0] == fine.mass_coeff_seed[0])
            state = numerical.concatenate([projected_mass[1:], projected_pi[:fine.count], coarse_reactions])
            initial_state = state.copy()
            original_free_slopes = fine.pi_coeff_seed[fine.count:].copy()
            label = 'N32_' + branch + '_strict_legacy_port_control'
            print('Starting ' + label, flush=True)

            def progress(history, current, scales):
                report['active_case'] = {'label': label, 'history': history}
                numerical.savez_compressed(destination / 'recovery-active.npz', state=current, scales=scales)
                save()

            state, scales, history, converged, failure = newton_initial_data(fine, state, progress)
            mass_coeff, pi_coeff, reactions = fine.set_state(state)
            residual = fine.data_residual(state)
            check(label + '_free_slopes_unchanged', numerical.array_equal(pi_coeff[fine.count:], original_free_slopes))
            record = {'label': label, 'status': 'converged' if converged else 'not_converged', 'failure': failure, 'history': history, 'all_residual_max': float(abs(residual).max()), 'all_scaled_residual_max': float(abs(residual / scales).max()), 'boundary_velocity': fine.boundary_velocity.tolist(), 'coarse_fixed_flux_difference': float(fine.boundary_velocity[0] - coarse.boundary_velocity[0]), 'within_old_iteration_budget': len(history) <= 25, 'valid_for_physics_claim': False}
            if converged:
                check(label + '_root_residuals', record['all_residual_max'] < 1e-9 and record['all_scaled_residual_max'] < 1e-10)
            output = destination / (label + '.npz')
            arrays = {'state': state, 'seed_state': initial_state, 'row_scales': scales, 'mass_coefficients': mass_coeff, 'pi_coefficients': pi_coeff, 'fixed_lapse': fine.fixed_lapse, 'boundary_velocity': fine.boundary_velocity, 'configuration': fine.configuration, 'residual': residual}
            numerical.savez_compressed(output, **arrays)
            with numerical.load(output, allow_pickle=False) as saved:
                check(label + '_finite_archive_roundtrip', set(saved.files) == set(arrays) and all(numerical.array_equal(value, saved[name]) and numerical.all(numerical.isfinite(value)) for name, value in arrays.items()))
            own(output, 'outputs')
            report['samples'].append(record)
            save()
            print(json.dumps(record), flush=True)
        report['mass_constraint_reduction'] = []
        for sample in prior['samples']:
            if sample['status'] != 'converged':
                continue
            label = sample['label']
            saved = archive(prior_path.parent / (label + '.npz'))
            model = build(sample['size'], sample['branch'], saved['boundary_velocity'])
            model.pi_coeff_seed = saved['pi_coefficients'].copy()
            model.mass_coeff_seed[0] = saved['mass_coefficients'][0]
            residual = model.data_residual(saved['state'])
            check(label + '_fresh_model_root_roundtrip', abs(residual).max() < 1e-9 and abs(residual / saved['row_scales']).max() < 1e-10)
            mass_coeff, pi_coeff, reactions = model.set_state(saved['state'])
            evaluation = model.evaluate(numerical.concatenate([model.fixed_lapse, reactions]))
            reconstructed = fields(model, mass_coeff, pi_coeff, saved['common_sample_points'], evaluation['scalar_velocity'])
            check(label + '_physical_samples_roundtrip', all(numerical.array_equal(value, saved['fine_sample_' + name]) for name, value in reconstructed.items()))
            derivative = model.data_jacobian(saved['state'])
            mass_count = model.count
            mass_block = derivative[:mass_count, :mass_count]
            mass_singular = numerical.linalg.svd(mass_block, compute_uv=False)
            reduced_record = {'label': label, 'mass_block_condition': float(mass_singular[0] / mass_singular[-1]), 'mass_block_smallest_singular_value': float(mass_singular[-1]), 'interval_invertibility_certificate': False}
            response = numerical.linalg.solve(mass_block, derivative[:mass_count, mass_count:])
            reduced = derivative[mass_count:, mass_count:] - derivative[mass_count:, :mass_count] @ response
            direction = numerical.cos(numerical.arange(reduced.shape[1]) + .3)
            lifted = numerical.concatenate([-response @ direction, direction])
            full_action = derivative @ lifted
            identity_error = float(max(abs(full_action[:mass_count]).max(), abs(full_action[mass_count:] - reduced @ direction).max()))
            check(label + '_exact_tangent_Schur_identity_numerical_control', identity_error < 1e-10, identity_error)
            reduced_record['reduced_condition'] = float(numerical.linalg.cond(reduced / saved['row_scales'][mass_count:, None]))
            reduced_record['tangent_identity_error'] = identity_error
            report['mass_constraint_reduction'].append(reduced_record)
        for module in tuple(sys.modules.values()):
            filename = getattr(module, '__file__', None)
            if filename:
                path = Path(filename).resolve()
                if path.parent == root / 'scripts' and path.suffix == '.py':
                    own(path)
        own(destination / 'recovery-active.npz', 'outputs')
        check('no_python_cache', not (root / 'scripts/__pycache__').exists())
        report['state'] = 'complete'
        report.pop('active_case', None)
        report['completed_utc'] = datetime.now(timezone.utc).isoformat()
        save()
        print('Controls complete.', flush=True)
    except Exception as error:
        report['state'] = 'failed'
        report['error'] = repr(error)
        save()
        raise


if __name__ == '__main__':
    run()
