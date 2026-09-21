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
    from annular_adm_mixed_action_20260909 import MixedActionBasis, linear_value_gradient
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian
    from annular_canonical_nodal_data_20260911 import CanonicalInitialNodalData
    from annular_canonical_mesh_transfer_20260911 import fields, project_momentum, split_quadrature, compare_fields, newton_initial_data

    class FixedDerivativeData(CanonicalInitialNodalData):
        def set_state(self, data):
            mass, pi_coeff, reactions = super().set_state(data)
            pi_coeff[self.count:] = self.basis.spacing * (self.fixed_auxiliary_derivative - self.basis.derivative @ pi_coeff[:self.count])
            self.pi = self.pi_map @ pi_coeff
            return mass, pi_coeff, reactions

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260911'
    destination = intake / 'annular-canonical-fixed-derivative-attempt01'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'inputs': {}, 'outputs': {}, 'checks': [], 'samples': [], 'skipped': [], 'started_utc': datetime.now(timezone.utc).isoformat(), 'valid_for_physics_claim': False, 'new_evolution': False, 'interval_certificate': False, 'free_data_policy': 'Fix the auxiliary Hermite derivative D*a+b/h, NOT its released correction b, to its pre-solve transferred value. Physical pi=m_seed*u; no claim that pi derivative or solved pi profile remains fixed. New initial-data slice, same canonical equations and original fine chi/lapse.', 'boundary_policy': 'Common converged N16 flux and scalar endpoint velocities held exactly across refinements.', 'inner_flux_parent_selected': False}

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
        check('prior_continuation_complete', prior['state'] == 'complete')
        for table in ['inputs', 'outputs']:
            for name, expected in prior[table].items():
                if digest(root / name) != expected:
                    raise RuntimeError('Changed prior evidence: ' + name)
                report['inputs'][name] = expected
        own(Path(__file__))
        snapshot = destination / ('executed-' + Path(__file__).name)
        snapshot.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        parameter_path = root / 'source-intake/navier-stokes/20260909/annular-constraint-correction-initial/canonical.json'
        own(parameter_path)
        constants = {name: float(symbolic.sympify(value)) for name, value in json.loads(parameter_path.read_text())['parameters'].items()}
        roots = root / 'source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02'

        def build(mesh, branch, boundary, constructor):
            source = archive(roots / ('canonical_N' + str(mesh) + '_' + branch + '_sample0.npz'))
            basis = MixedActionBasis(source['basis_radii'])
            count = basis.radii.size
            configuration, momenta = source['original_configuration'], source['original_momenta']
            packed = (source['initial_root_box_lower'] + source['initial_root_box_upper']) / 2
            system = ReleasedHermiteRouthian(basis, configuration[:count], configuration[count:], constants, .1, momenta[:count], momenta[count:], source['affine_clock'][0], MetricLinkQuadrature(basis))
            return constructor(system, packed, configuration, branch != 'GR', boundary)

        for branch in ['GR', 'metric_Gram']:
            coarse_path = intake / 'annular-canonical-initial-data-nodal01' / ('canonical_N16_' + branch + '_sample0.npz')
            saved = archive(coarse_path)
            boundary = saved['boundary_velocity']
            check(branch + '_shared_boundary', numerical.array_equal(boundary, prior['common_boundary_velocity']))
            coarse = build(16, branch, boundary, CanonicalInitialNodalData)
            coarse.pi_coeff_seed = saved['pi_coefficients'].copy()
            coarse_mass, coarse_pi, coarse_reactions = coarse.set_state(saved['state'])
            for mesh in [32, 64]:
                fine = build(mesh, branch, boundary, FixedDerivativeData)
                fine.mass_coeff_seed[0] = coarse_mass[0]
                projected_pi, projection = project_momentum(coarse, fine, coarse_mass, coarse_pi)
                fine.pi_coeff_seed = projected_pi.copy()
                fine.fixed_auxiliary_derivative = fine.basis.derivative @ projected_pi[:fine.count] + projected_pi[fine.count:] / fine.basis.spacing
                projected_mass = linear_value_gradient(coarse.basis.faces, fine.basis.faces)[0] @ coarse_mass[:coarse.face_count]
                seed = numerical.concatenate([projected_mass[1:], projected_pi[:fine.count], coarse_reactions])
                seed_mass, seed_pi, unused_reactions = fine.set_state(seed)
                check(branch + str(mesh) + '_seed_physical_projection_unchanged', abs(seed_pi - projected_pi).max() < 1e-12)
                points, weights = split_quadrature([coarse, fine], 12)
                coarse_evaluation = coarse.evaluate(numerical.concatenate([coarse.fixed_lapse, coarse_reactions]))
                coarse_fields = fields(coarse, coarse_mass, coarse_pi, points, coarse_evaluation['scalar_velocity'])
                label = 'N' + str(mesh) + '_' + branch + '_fixed_auxiliary_derivative'
                print('Starting ' + label, flush=True)

                def progress(history, state, scales):
                    report['active_case'] = {'label': label, 'history': history}
                    numerical.savez_compressed(destination / 'recovery-active.npz', state=state, row_scales=scales, fixed_auxiliary_derivative=fine.fixed_auxiliary_derivative)
                    save()

                state, scales, history, converged, failure = newton_initial_data(fine, seed, progress)
                mass_coeff, pi_coeff, reactions = fine.set_state(state)
                result = fine.evaluate(numerical.concatenate([fine.fixed_lapse, reactions]))
                constraint = fine.constraint()
                all_residual = fine.data_residual(state)
                fine_fields = fields(fine, mass_coeff, pi_coeff, points, result['scalar_velocity'])
                reintegrated = linear_value_gradient(fine.basis.radii, points)[0].T @ (weights * fine_fields['bulk_density'])
                if fine.include_gram:
                    reintegrated -= fine.basis.radii**2 * numerical.sqrt(fine.node_f) * fine.gram_density
                fixed_derivative_error = float(abs(fine.basis.derivative @ pi_coeff[:fine.count] + pi_coeff[fine.count:] / fine.basis.spacing - fine.fixed_auxiliary_derivative).max())
                check(label + '_fixed_derivative_not_fixed_correction', fixed_derivative_error < 1e-10, fixed_derivative_error)
                record = {'label': label, 'mesh': mesh, 'branch': branch, 'source_coarse_path': str(coarse_path.relative_to(root)), 'status': 'converged' if converged else 'not_converged', 'failure': failure, 'iterations': history, 'all_residual_max': float(abs(all_residual).max()), 'all_scaled_residual_max': float(abs(all_residual / scales).max()), 'constraint_max': float(abs(constraint).max()), 'constraint_rate_max': float(abs(result['constraint_rate']).max()), 'boundary_residual_max': float(abs(result['boundary_residual']).max()), 'minimum_F': float(min(fine.spatial_f.min(), fine.node_f.min(), fine.link_f.min())), 'lapse_range': [float(fine.fixed_lapse.min()), float(fine.fixed_lapse.max())], 'bulk_density_L2': float(numerical.sqrt(weights @ fine_fields['bulk_density']**2)), 'coarse_bulk_density_L2': float(numerical.sqrt(weights @ coarse_fields['bulk_density']**2)), 'reintegrated_constraint_max': float(abs(reintegrated).max()), 'pi_total_variation_sampled': float(weights @ abs(fine_fields['pi_gradient'])), 'coarse_pi_total_variation_sampled': float(weights @ abs(coarse_fields['pi_gradient'])), 'solved_vs_coarse_fields': compare_fields(coarse_fields, fine_fields, weights), 'projection': projection, 'valid_for_physics_claim': False, 'new_evolution': False}
                if converged:
                    check(label + '_all_root_equations', record['all_residual_max'] < 1e-9 and record['all_scaled_residual_max'] < 1e-10)
                    check(label + '_positive_metric', record['minimum_F'] > .1 and record['lapse_range'][0] > 0)
                    derivative = fine.data_jacobian(state)
                    direction = numerical.sin(numerical.arange(state.size) + 1.) * numerical.maximum(abs(state), .001)
                    step = 1e-5
                    finite = (fine.data_residual(state + step * direction) - fine.data_residual(state - step * direction)) / (2 * step)
                    expected = derivative @ direction
                    error = float(abs(finite - expected).max() / max(1., float(abs(expected).max())))
                    check(label + '_Jacobian_control', error < 1e-7, error)
                    record['scaled_Jacobian_condition'] = float(numerical.linalg.cond(derivative / scales[:, None]))
                    fine.set_state(state)
                arrays = {'state': state, 'seed_state': seed, 'row_scales': scales, 'mass_coefficients': mass_coeff, 'pi_coefficients': pi_coeff, 'fixed_auxiliary_derivative': fine.fixed_auxiliary_derivative, 'projected_pi_coefficients': projected_pi, 'fixed_lapse': fine.fixed_lapse, 'configuration': fine.configuration, 'boundary_velocity': boundary, 'constraint': constraint, 'reintegrated_constraint': reintegrated, 'common_sample_points': points, 'common_sample_weights': weights}
                arrays.update({name: value for name, value in result.items() if isinstance(value, numerical.ndarray)})
                arrays.update({'fine_sample_' + name: value for name, value in fine_fields.items()})
                arrays.update({'coarse_sample_' + name: value for name, value in coarse_fields.items()})
                output = destination / (label + '.npz')
                numerical.savez_compressed(output, **arrays)
                with numerical.load(output, allow_pickle=False) as archive_file:
                    check(label + '_finite_archive_roundtrip', set(archive_file.files) == set(arrays) and all(numerical.array_equal(value, archive_file[name]) and numerical.all(numerical.isfinite(value)) for name, value in arrays.items()))
                own(output, 'outputs')
                report['samples'].append(record)
                save()
                print(json.dumps({name: record[name] for name in ['label', 'status', 'failure', 'all_residual_max', 'bulk_density_L2', 'reintegrated_constraint_max']}), flush=True)
                if not converged:
                    report['skipped'].append({'branch': branch, 'next_mesh': mesh * 2, 'reason': 'No converged immediate-coarser state; do not promote failed iterates.'})
                    break
                coarse, coarse_mass, coarse_pi, coarse_reactions, coarse_path = fine, mass_coeff.copy(), pi_coeff.copy(), reactions.copy(), output
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
        print('Fixed-derivative batch complete.', flush=True)
    except Exception as error:
        report['state'] = 'failed'
        report['error'] = repr(error)
        save()
        raise


if __name__ == '__main__':
    run()
