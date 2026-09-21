import argparse
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
    from annular_canonical_mesh_transfer_20260911 import project_momentum, fields, split_quadrature, compare_fields, newton_initial_data

    parser = argparse.ArgumentParser()
    parser.add_argument('--attempt', required=True)
    parser.add_argument('--sizes', nargs='+', type=int, default=[32, 64])
    arguments = parser.parse_args()
    if not arguments.attempt.isalnum() or arguments.sizes not in [[32], [32, 64]]:
        raise ValueError('Use a fresh alphanumeric attempt and consecutive meshes.')
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260911'
    destination = intake / ('annular-canonical-mesh-continuation-' + arguments.attempt)
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': {}, 'outputs': {}, 'checks': [], 'samples': [], 'skipped': [], 'valid_for_physics_claim': False, 'interval_certificate': False, 'new_evolution': False, 'inner_flux_parent_selected': False, 'boundary_policy': 'Hold each converged N16 boundary-velocity triple unchanged; verify both branches identical.', 'free_data_policy': 'Original fine chi and lapse retained. Transfer physical pi by endpoint-constrained L2 projection. Control keeps original fine released slope coefficients; transferred protocol fixes projected released slope coefficients. All initial mass bubbles zero.', 'residual_policy': 'All original canonical finite initial equations retained; no residual fitting, row deletion, regularization or unreported parameter homotopy.'}

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

    def load_archive(path):
        own(path)
        with numerical.load(path, allow_pickle=False) as archive:
            return {name: archive[name].copy() for name in archive.files}

    save()
    try:
        prior_path = intake / 'annular-canonical-initial-data-final-integrity.json'
        own(prior_path)
        prior = json.loads(prior_path.read_text())
        for table in ['inputs', 'outputs']:
            for name, expected in prior[table].items():
                if digest(root / name) != expected:
                    raise RuntimeError('Sealed input changed: ' + name)
                report['inputs'][name] = expected
        check('prior_complete_and_unchanged', prior['state'] == 'complete')
        for name in ['annular_canonical_mesh_transfer_20260911.py', Path(__file__).name]:
            source = root / 'scripts' / name
            compile(source.read_bytes(), str(source), 'exec')
            own(source)
            snapshot = destination / ('executed-' + name)
            snapshot.write_bytes(source.read_bytes())
            own(snapshot, 'outputs')
        parameter_path = root / 'source-intake/navier-stokes/20260909/annular-constraint-correction-initial/canonical.json'
        own(parameter_path)
        constants = {name: float(symbolic.sympify(value)) for name, value in json.loads(parameter_path.read_text())['parameters'].items()}
        roots = root / 'source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02'

        def build(size, branch, boundary_velocity):
            source = load_archive(roots / ('canonical_N' + str(size) + '_' + branch + '_sample0.npz'))
            basis = MixedActionBasis(source['basis_radii'])
            count = basis.radii.size
            configuration, momenta = source['original_configuration'], source['original_momenta']
            packed = (source['initial_root_box_lower'] + source['initial_root_box_upper']) / 2
            system = ReleasedHermiteRouthian(basis, configuration[:count], configuration[count:], constants, .1, momenta[:count], momenta[count:], source['affine_clock'][0], MetricLinkQuadrature(basis))
            return CanonicalInitialNodalData(system, packed, configuration, branch != 'GR', boundary_velocity)

        common_boundary = None
        prior_status = json.loads((intake / 'annular-canonical-initial-data-nodal01/status.json').read_text())
        for branch in ['GR', 'metric_Gram']:
            label = 'canonical_N16_' + branch + '_sample0'
            prior_case = next(item for item in prior_status['samples'] if item['label'] == label)
            check(branch + '_coarse_input_converged', prior_case['status'] == 'converged')
            coarse_path = intake / 'annular-canonical-initial-data-nodal01' / (label + '.npz')
            archive = load_archive(coarse_path)
            boundary = archive['boundary_velocity']
            if common_boundary is None:
                common_boundary = boundary.copy()
                report['common_boundary_velocity'] = common_boundary.tolist()
            check(branch + '_same_GR_boundary_ports', numerical.array_equal(boundary, common_boundary))
            coarse = build(16, branch, boundary)
            coarse.pi_coeff_seed = archive['pi_coefficients'].copy()
            coarse.fixed_lapse = archive['fixed_lapse'].copy()
            coarse_state = archive['state'].copy()
            coarse_mass, coarse_pi, coarse_reactions = coarse.set_state(coarse_state)
            check(branch + '_coarse_source_roundtrip', numerical.max(abs(coarse.data_residual(coarse_state))) < 1e-9 and numerical.array_equal(coarse.pi, archive['pi_field']) and numerical.array_equal(coarse.mass_q, archive['mass_field']))
            for size in arguments.sizes:
                if (coarse.count - 1) * 2 != size:
                    report['skipped'].append({'branch': branch, 'size': size, 'reason': 'No converged immediate-coarser transferred state. Failed iterates are never promoted.'})
                    continue
                fine = build(size, branch, boundary)
                fine.mass_coeff_seed[0] = coarse_mass[0]
                original_slopes = fine.pi_coeff_seed[fine.count:].copy()
                projected_pi, projection = project_momentum(coarse, fine, coarse_mass, coarse_pi)
                alternate_pi, alternate = project_momentum(coarse, fine, coarse_mass, coarse_pi, order=12)
                check(branch + str(size) + '_physical_projection_stationarity', projection['normal_residual_max'] < 1e-10, projection)
                check(branch + str(size) + '_physical_projection_endpoints', projection['endpoint_constraint_max'] < 1e-12)
                projection_difference = float(abs(projected_pi - alternate_pi).max())
                check(branch + str(size) + '_projection_quadrature_order_control', projection_difference < 1e-9, projection_difference)
                points, weights = split_quadrature([coarse, fine], 12)
                coarse_result = coarse.evaluate(numerical.concatenate([coarse.fixed_lapse, coarse_reactions]))
                coarse_fields = fields(coarse, coarse_mass, coarse_pi, points, coarse_result['scalar_velocity'])
                prolonged_mass = linear_value_gradient(coarse.basis.faces, fine.basis.faces)[0] @ coarse_mass[:coarse.face_count]
                seed_state = numerical.concatenate([prolonged_mass[1:], projected_pi[:fine.count], coarse_reactions])
                refined = None
                for protocol in ['original_slopes_control', 'transferred_slopes']:
                    fine.pi_coeff_seed = projected_pi.copy()
                    if protocol == 'original_slopes_control':
                        fine.pi_coeff_seed[fine.count:] = original_slopes
                    label = 'N' + str(size) + '_' + branch + '_' + protocol
                    print('Starting ' + label, flush=True)
                    seed_mass, seed_pi, unused_reactions = fine.set_state(seed_state)
                    seed_fields = fields(fine, seed_mass, seed_pi, points)

                    def progress(history, state, scales):
                        report['active_case'] = {'label': label, 'history': history}
                        numerical.savez_compressed(destination / 'recovery-active.npz', state=state, row_scales=scales, pi_free_coefficients=fine.pi_coeff_seed, fixed_lapse=fine.fixed_lapse, boundary_velocity=boundary, configuration=fine.configuration)
                        save()

                    state, scales, history, converged, failure = newton_initial_data(fine, seed_state, progress)
                    mass_coeff, pi_coeff, reactions = fine.set_state(state)
                    result = fine.evaluate(numerical.concatenate([fine.fixed_lapse, reactions]))
                    constraint = fine.constraint()
                    all_residual = fine.data_residual(state)
                    fine_fields = fields(fine, mass_coeff, pi_coeff, points, result['scalar_velocity'])
                    reintegrated = linear_value_gradient(fine.basis.radii, points)[0].T @ (weights * fine_fields['bulk_density'])
                    if fine.include_gram:
                        reintegrated -= fine.basis.radii**2 * numerical.sqrt(fine.node_f) * fine.gram_density
                    record = {'label': label, 'size': size, 'branch': branch, 'protocol': protocol, 'status': 'converged' if converged else 'not_converged', 'failure': failure, 'source_coarse_path': str(coarse_path.relative_to(root)), 'iterations': history, 'projection': projection, 'projection_order_difference_max': projection_difference, 'seed_field_transfer': compare_fields(coarse_fields, seed_fields, weights), 'solved_vs_coarse_fields': compare_fields(coarse_fields, fine_fields, weights), 'constraint_max': float(abs(constraint).max()), 'constraint_rate_max': float(abs(result['constraint_rate']).max()), 'boundary_residual_max': float(abs(result['boundary_residual']).max()), 'all_residual_max': float(abs(all_residual).max()), 'all_scaled_residual_max': float(abs(all_residual / scales).max()), 'minimum_F': float(min(fine.spatial_f.min(), fine.node_f.min(), fine.link_f.min())), 'lapse_range': [float(fine.fixed_lapse.min()), float(fine.fixed_lapse.max())], 'reintegrated_constraint_max': float(abs(reintegrated).max()), 'constraint_quadrature_difference_max': float(abs(reintegrated - constraint).max()), 'bulk_density_sample_max': float(abs(fine_fields['bulk_density']).max()), 'bulk_density_L2': float(numerical.sqrt(weights @ fine_fields['bulk_density']**2)), 'coarse_bulk_density_L2': float(numerical.sqrt(weights @ coarse_fields['bulk_density']**2)), 'pi_total_variation_sampled': float(weights @ abs(fine_fields['pi_gradient'])), 'coarse_pi_total_variation_sampled': float(weights @ abs(coarse_fields['pi_gradient'])), 'diagnostic_scope': 'Split Gauss samples, not interval bounds; bulk density excludes Gram point/nonlocal covectors. Finite root and reintegrated constraint are distinct.', 'valid_for_physics_claim': False, 'new_evolution': False}
                    if converged:
                        check(label + '_all_equations', record['all_residual_max'] < 1e-9 and record['all_scaled_residual_max'] < 1e-10)
                        check(label + '_positive_geometry', record['minimum_F'] > .1 and record['lapse_range'][0] > 0)
                        check(label + '_fixed_ports_and_no_mass_bubbles', numerical.array_equal(fine.boundary_velocity, common_boundary) and mass_coeff[0] == coarse_mass[0] and numerical.all(mass_coeff[fine.face_count:] == 0))
                        derivative = fine.data_jacobian(state)
                        direction = numerical.sin(numerical.arange(state.size) + 1.) * numerical.maximum(abs(state), .001)
                        step = 1e-5
                        finite = (fine.data_residual(state + step * direction) - fine.data_residual(state - step * direction)) / (2 * step)
                        expected = derivative @ direction
                        error = float(abs(finite - expected).max() / max(1., float(abs(expected).max())))
                        check(label + '_directional_jacobian_control', error < 1e-7, error)
                        record['scaled_Jacobian_condition'] = float(numerical.linalg.cond(derivative / scales[:, None]))
                        fine.set_state(state)
                    arrays = {'state': state, 'seed_state': seed_state, 'mass_coefficients': mass_coeff, 'pi_coefficients': pi_coeff, 'fixed_lapse': fine.fixed_lapse, 'configuration': fine.configuration, 'boundary_velocity': boundary, 'constraint': constraint, 'row_scales': scales, 'mass_field': fine.mass_q, 'pi_field': fine.pi, 'projected_pi_coefficients': projected_pi, 'original_fine_slopes': original_slopes, 'common_sample_points': points, 'common_sample_weights': weights, 'reintegrated_constraint': reintegrated}
                    arrays.update({name: value for name, value in result.items() if isinstance(value, numerical.ndarray)})
                    arrays.update({'fine_sample_' + name: value for name, value in fine_fields.items()})
                    arrays.update({'coarse_sample_' + name: value for name, value in coarse_fields.items()})
                    check(label + '_all_arrays_finite', all(numerical.all(numerical.isfinite(value)) for value in arrays.values()))
                    output = destination / (label + '.npz')
                    numerical.savez_compressed(output, **arrays)
                    with numerical.load(output, allow_pickle=False) as saved:
                        check(label + '_archive_roundtrip', set(saved.files) == set(arrays) and all(numerical.array_equal(saved[name], value) for name, value in arrays.items()))
                    own(output, 'outputs')
                    report['samples'].append(record)
                    save()
                    print(json.dumps({name: record[name] for name in ['label', 'status', 'failure', 'all_residual_max', 'bulk_density_L2', 'reintegrated_constraint_max']}), flush=True)
                    if converged and protocol == 'transferred_slopes':
                        refined = (fine, state.copy(), mass_coeff.copy(), pi_coeff.copy(), reactions.copy(), output)
                if refined:
                    coarse, coarse_state, coarse_mass, coarse_pi, coarse_reactions, coarse_path = refined
                else:
                    report['skipped'].append({'branch': branch, 'source_size': size, 'reason': 'Transferred-slopes fine problem did not converge; stop this refinement chain.'})
                    break
        for module in tuple(sys.modules.values()):
            filename = getattr(module, '__file__', None)
            if filename:
                source = Path(filename).resolve()
                if source.parent == root / 'scripts' and source.suffix == '.py':
                    own(source)
        check('no_python_cache', not (root / 'scripts/__pycache__').exists())
        own(destination / 'recovery-active.npz', 'outputs')
        report['state'] = 'complete'
        report.pop('active_case', None)
        report['completed_utc'] = datetime.now(timezone.utc).isoformat()
        save()
        print('Complete: ' + str(sum(sample['status'] == 'converged' for sample in report['samples'])) + '/' + str(len(report['samples'])) + ' finite roots.', flush=True)
    except Exception as error:
        report['state'] = 'failed'
        report['error'] = repr(error)
        report['failed_utc'] = datetime.now(timezone.utc).isoformat()
        save()
        raise


if __name__ == '__main__':
    run()
