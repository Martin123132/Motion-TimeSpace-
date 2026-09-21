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
    from annular_canonical_mesh_transfer_20260911 import fields, compare_fields, split_quadrature
    from annular_canonical_mass_reduction_20260911 import MassConstraintReduction

    parser = argparse.ArgumentParser()
    parser.add_argument('--attempt', required=True)
    parser.add_argument('--controls-only', action='store_true')
    arguments = parser.parse_args()
    if not arguments.attempt.isalnum():
        raise ValueError('Use a fresh alphanumeric attempt.')
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260911'
    destination = intake / ('annular-canonical-mass-reduction-' + arguments.attempt)
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': {}, 'outputs': {}, 'checks': [], 'replays': [], 'samples': [], 'valid_for_physics_claim': False, 'interval_certificate': False, 'new_evolution': False, 'inner_flux_parent_selected': False, 'algorithm': 'Analytic mass-constraint Jacobian; positive-chart nonlinear mass solve at every outer trial; full chain-rule reduced Jacobian, no deleted equations or action regularization.', 'source_policy': 'Replay existing N32 roots, then retry strict legacy-port N32 and common-coarse-port N64 using each archived original seed, original free corrections, fixed lapse/config/clock/inner mass/flux and inherited full row scales. Never use failed final iterates as seeds.', 'mass_tolerance': 2e-14, 'absolute_root_tolerance': 1e-9, 'scaled_root_tolerance': 1e-10, 'outer_iteration_limit': 35}

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
        prior_path = intake / 'annular-canonical-mesh-continuation-final-integrity.json'
        own(prior_path)
        prior = json.loads(prior_path.read_text())
        check('prior_complete', prior['state'] == 'complete')
        for table in ['inputs', 'outputs']:
            for name, expected in prior[table].items():
                if digest(root / name) != expected:
                    raise RuntimeError('Previously sealed evidence changed: ' + name)
                report['inputs'][name] = expected
        for name in ['annular_canonical_mass_reduction_20260911.py', Path(__file__).name]:
            path = root / 'scripts' / name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
            snapshot = destination / ('executed-' + name)
            snapshot.write_bytes(path.read_bytes())
            own(snapshot, 'outputs')
        parameter_path = root / 'source-intake/navier-stokes/20260909/annular-constraint-correction-initial/canonical.json'
        own(parameter_path)
        constants = {name: float(symbolic.sympify(value)) for name, value in json.loads(parameter_path.read_text())['parameters'].items()}
        roots = root / 'source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02'
        main_directory = intake / 'annular-canonical-mesh-continuation-attempt02'
        legacy_directory = intake / 'annular-canonical-continuation-control-attempt01'
        main_status = json.loads((main_directory / 'status.json').read_text())
        legacy_status = json.loads((legacy_directory / 'status.json').read_text())

        def build(mesh, branch, saved, protocol):
            source = archive(roots / ('canonical_N' + str(mesh) + '_' + branch + '_sample0.npz'))
            basis = MixedActionBasis(source['basis_radii'])
            count = basis.radii.size
            configuration, momenta = source['original_configuration'], source['original_momenta']
            packed = (source['initial_root_box_lower'] + source['initial_root_box_upper']) / 2
            system = ReleasedHermiteRouthian(basis, configuration[:count], configuration[count:], constants, .1, momenta[:count], momenta[count:], source['affine_clock'][0], MetricLinkQuadrature(basis))
            model = CanonicalInitialNodalData(system, packed, configuration, branch != 'GR', saved['boundary_velocity'])
            check(branch + str(mesh) + protocol + '_original_fixed_configuration_and_lapse', numerical.array_equal(model.fixed_lapse, saved['fixed_lapse']) and numerical.array_equal(model.configuration, saved['configuration']))
            if protocol == 'transferred_slopes':
                model.pi_coeff_seed = saved['projected_pi_coefficients'].copy()
            elif protocol == 'restored_root':
                model.pi_coeff_seed = saved['pi_coefficients'].copy()
            elif protocol not in ['original_slopes_control', 'legacy']:
                raise ValueError('Unknown free-data protocol.')
            model.mass_coeff_seed[0] = saved['mass_coefficients'][0]
            check(branch + str(mesh) + protocol + '_archived_free_corrections_match', numerical.array_equal(model.pi_coeff_seed[count:], saved['pi_coefficients'][count:]))
            return model

        def record_arrays(label, arrays):
            check(label + '_arrays_finite', all(numerical.all(numerical.isfinite(value)) for value in arrays.values()))
            path = destination / (label + '.npz')
            numerical.savez_compressed(path, **arrays)
            with numerical.load(path, allow_pickle=False) as saved:
                check(label + '_archive_roundtrip', set(saved.files) == set(arrays) and all(numerical.array_equal(value, saved[name]) for name, value in arrays.items()))
            own(path, 'outputs')

        def progress_for(label, model):
            def progress(history, state):
                report['active_case'] = {'label': label, 'history': history}
                numerical.savez_compressed(destination / 'recovery-active.npz', state=state, free_pi_coefficients=model.pi_coeff_seed, fixed_lapse=model.fixed_lapse, configuration=model.configuration, boundary_velocity=model.boundary_velocity)
                save()
            return progress

        replay_cases = [(sample, main_directory, sample['protocol']) for sample in main_status['samples'] if sample['status'] == 'converged']
        replay_cases += [(dict(sample, size=32, branch='metric_Gram'), legacy_directory, 'legacy') for sample in legacy_status['samples'] if sample['status'] == 'converged']
        for sample, directory, protocol in replay_cases:
            label = sample['label'] + '_root_replay'
            print('Checking ' + label, flush=True)
            saved = archive(directory / (sample['label'] + '.npz'))
            model = build(sample['size'], sample['branch'], saved, protocol)
            reduction = MassConstraintReduction(model)
            state = saved['state'].copy()
            full = model.data_jacobian(state)
            mass_block, other_block = reduction.constraint_blocks(state)
            block_error = float(abs(numerical.concatenate([mass_block, other_block], axis=1) - full[:model.count]).max())
            check(label + '_analytic_mass_blocks_vs_full_complex_derivative', block_error < 1e-10, block_error)
            projected, unused_history = reduction.project(state)
            reduced, tangent, unused_mass = reduction.reduced_jacobian(projected)
            direct_full = model.data_jacobian(projected)
            chain_error = float(abs(reduced - direct_full[model.count:] @ tangent).max())
            check(label + '_complete_chain_rule_identity', chain_error < 1e-10, chain_error)
            direction = numerical.sin(numerical.arange(reduced.shape[1]) + .4) * numerical.maximum(abs(projected[model.count:]), .001)
            step = 1e-5
            plus, unused_plus = reduction.project(projected + step * (tangent @ direction))
            minus, unused_minus = reduction.project(projected - step * (tangent @ direction))
            finite = (model.data_residual(plus)[model.count:] - model.data_residual(minus)[model.count:]) / (2 * step)
            expected = reduced @ direction
            directional_error = float(abs(finite - expected).max() / max(1., float(abs(expected).max())))
            check(label + '_nonlinear_constraint_manifold_directional_control', directional_error < 1e-7, directional_error)
            disturbed = projected + 1e-7 * numerical.cos(numerical.arange(state.size) + .8) * numerical.maximum(abs(projected), .001)
            solved = reduction.solve(disturbed, saved['row_scales'], progress_for(label, model), maximum_iterations=12)
            residual = model.data_residual(solved['state'])
            distance = float(abs(solved['state'] - state).max())
            check(label + '_nearby_replay_converges_without_equation_changes', solved['converged'] and abs(residual / saved['row_scales']).max() < 1e-10 and abs(residual).max() < 1e-9, solved['failure'])
            check(label + '_recovered_same_root_neighborhood', distance < 1e-5, distance)
            report['replays'].append({'label': label, 'converged': solved['converged'], 'all_residual_max': float(abs(residual).max()), 'all_scaled_residual_max': float(abs(residual / saved['row_scales']).max()), 'distance_from_original': distance, 'analytic_block_error': block_error, 'chain_error': chain_error, 'projected_directional_error': directional_error, 'history': solved['history']})
            record_arrays(label, {'state': solved['state'], 'original_state': state, 'perturbed_state': disturbed, 'residual': residual, 'row_scales': saved['row_scales'], 'mass_block': mass_block, 'reduced_jacobian': reduced, 'tangent': tangent})
            save()
        if not arguments.controls_only:
            cases = [(dict(sample, size=32, branch='GR' if sample['label'].startswith('N32_GR_') else 'metric_Gram'), legacy_directory, 'legacy') for sample in legacy_status['samples']]
            cases += [(sample, main_directory, sample['protocol']) for sample in main_status['samples'] if sample['size'] == 64]
            for sample, directory, protocol in cases:
                label = sample['label'] + '_mass_reduced'
                print('Starting ' + label, flush=True)
                saved = archive(directory / (sample['label'] + '.npz'))
                model = build(sample['size'], sample['branch'], saved, protocol)
                reduction = MassConstraintReduction(model)
                seed_state = saved['seed_state'].copy()
                fixed_slopes = model.pi_coeff_seed[model.count:].copy()
                fixed_boundary = model.boundary_velocity.copy()
                if protocol == 'legacy':
                    coarse_saved = archive(intake / 'annular-canonical-initial-data-nodal01' / ('canonical_N16_' + sample['branch'] + '_sample0.npz'))
                    coarse = build(16, sample['branch'], coarse_saved, 'restored_root')
                    coarse_mass, coarse_pi, coarse_reactions = coarse.set_state(coarse_saved['state'])
                    points, weights = split_quadrature([coarse, model], 12)
                    coarse_evaluation = coarse.evaluate(numerical.concatenate([coarse.fixed_lapse, coarse_reactions]))
                    coarse_fields = fields(coarse, coarse_mass, coarse_pi, points, coarse_evaluation['scalar_velocity'])
                else:
                    points, weights = saved['common_sample_points'], saved['common_sample_weights']
                    coarse_fields = {name[len('coarse_sample_'):]: value for name, value in saved.items() if name.startswith('coarse_sample_')}
                solved = reduction.solve(seed_state, saved['row_scales'], progress_for(label, model))
                state = solved['state']
                mass_coeff, pi_coeff, reactions = model.set_state(state)
                evaluation = model.evaluate(numerical.concatenate([model.fixed_lapse, reactions]))
                residual = model.data_residual(state)
                sampled = fields(model, mass_coeff, pi_coeff, points, evaluation['scalar_velocity'])
                reintegrated = linear_value_gradient(model.basis.radii, points)[0].T @ (weights * sampled['bulk_density'])
                if model.include_gram:
                    reintegrated -= model.basis.radii**2 * numerical.sqrt(model.node_f) * model.gram_density
                record = {'label': label, 'mesh': sample['size'], 'branch': sample['branch'], 'protocol': protocol, 'prior_status': sample['status'], 'prior_all_residual_max': sample['all_residual_max'], 'source_seed_archive': str((directory / (sample['label'] + '.npz')).relative_to(root)), 'seed_key': 'seed_state, NOT failed final state', 'status': 'converged' if solved['converged'] else 'not_converged', 'failure': solved['failure'], 'history': solved['history'], 'all_residual_max': float(abs(residual).max()), 'all_scaled_residual_max': float(abs(residual / saved['row_scales']).max()), 'constraint_max': float(abs(residual[:model.count]).max()), 'constraint_rate_max': float(abs(evaluation['constraint_rate']).max()), 'boundary_residual_max': float(abs(evaluation['boundary_residual']).max()), 'minimum_F': float(min(model.spatial_f.min(), model.node_f.min(), model.link_f.min())), 'lapse_range': [float(model.fixed_lapse.min()), float(model.fixed_lapse.max())], 'solved_vs_coarse': compare_fields(coarse_fields, sampled, weights), 'bulk_density_L2': float(numerical.sqrt(weights @ sampled['bulk_density']**2)), 'coarse_bulk_density_L2': float(numerical.sqrt(weights @ coarse_fields['bulk_density']**2)), 'pi_total_variation_sampled': float(weights @ abs(sampled['pi_gradient'])), 'coarse_pi_total_variation_sampled': float(weights @ abs(coarse_fields['pi_gradient'])), 'reintegrated_constraint_max': float(abs(reintegrated).max()), 'diagnostic_scope': 'Code-normalized Gauss diagnostics, not interval bounds; bulk density omits Gram point/nonlocal sources; reintegrated weak constraint retains the Gram nodal term.', 'valid_for_physics_claim': False, 'new_evolution': False}
                check(label + '_same_free_corrections_boundary_and_mass_bubbles', numerical.array_equal(pi_coeff[model.count:], fixed_slopes) and numerical.array_equal(model.boundary_velocity, fixed_boundary) and numerical.all(mass_coeff[model.face_count:] == 0))
                check(label + '_every_accepted_outer_state_satisfies_mass_constraint', all(item['mass_residual'] <= reduction.mass_tolerance for item in solved['history']))
                if solved['converged']:
                    check(label + '_full_root_not_only_reduced_root', record['all_residual_max'] < 1e-9 and record['all_scaled_residual_max'] < 1e-10)
                final_reduced, final_tangent, final_mass = reduction.reduced_jacobian(state)
                scaled_final = final_reduced / saved['row_scales'][model.count:, None]
                left, singular, right_transpose = numerical.linalg.svd(scaled_final)
                record['final_mass_block_condition'] = float(numerical.linalg.cond(final_mass))
                record['final_reduced_condition'] = float(singular[0] / singular[-1])
                record['smallest_reduced_singular_value'] = float(singular[-1])
                record['residual_projection_on_smallest_left_mode'] = float(left[:, -1] @ (residual[model.count:] / saved['row_scales'][model.count:]))
                arrays = {'state': state, 'seed_state': seed_state, 'mass_coefficients': mass_coeff, 'pi_coefficients': pi_coeff, 'fixed_lapse': model.fixed_lapse, 'configuration': model.configuration, 'boundary_velocity': model.boundary_velocity, 'row_scales': saved['row_scales'], 'full_residual': residual, 'common_sample_points': points, 'common_sample_weights': weights, 'reintegrated_constraint': reintegrated, 'reduced_jacobian': final_reduced, 'tangent': final_tangent, 'mass_block': final_mass, 'reduced_singular_values': singular, 'smallest_left_mode': left[:, -1], 'smallest_right_mode': right_transpose[-1]}
                arrays.update({name: value for name, value in evaluation.items() if isinstance(value, numerical.ndarray)})
                arrays.update({'sample_' + name: value for name, value in sampled.items()})
                arrays.update({'coarse_sample_' + name: value for name, value in coarse_fields.items()})
                record_arrays(label, arrays)
                report['samples'].append(record)
                save()
                print(json.dumps({name: record[name] for name in ['label', 'status', 'failure', 'all_residual_max', 'constraint_max', 'bulk_density_L2', 'final_reduced_condition']}), flush=True)
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
        print('Mass-reduced batch complete.', flush=True)
    except Exception as error:
        report['state'] = 'failed'
        report['error'] = repr(error)
        report['failed_utc'] = datetime.now(timezone.utc).isoformat()
        save()
        raise


if __name__ == '__main__':
    run()
