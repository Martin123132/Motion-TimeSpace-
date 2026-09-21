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
    from annular_adm_mixed_action_20260909 import MixedActionBasis
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian
    from annular_canonical_inverse_boundary_20260911 import InverseBoundaryInitialData, InverseBoundaryMassReduction
    from annular_canonical_mesh_transfer_20260911 import fields

    parser = argparse.ArgumentParser()
    parser.add_argument('--attempt', required=True)
    arguments = parser.parse_args()
    if not arguments.attempt.isalnum():
        raise ValueError('Use a fresh alphanumeric attempt.')
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260911'
    destination = intake / ('annular-canonical-inverse-boundary-' + arguments.attempt)
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': {}, 'outputs': {}, 'checks': [], 'samples': [], 'valid_for_physics_claim': False, 'new_evolution': False, 'interval_certificate': False, 'protocol': 'Inverse boundary first jet: common imposed inner mass drive and outer scalar velocity; inner scalar velocity solved by full parent flux compatibility, not prescribed. Original scalar configuration and free momentum corrections retained. Primary lapse profile has outer-clock normalization; fixed-lapse branch is an explicitly incomplete boundary control. All finite C and Cdot rows retained. Classical endpoint Legendre/reaction gaps remain independent diagnostics.', 'outer_iteration_limit': 35}

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
        seal_path = intake / 'annular-canonical-mass-reduction-final-integrity.json'
        own(seal_path)
        prior = json.loads(seal_path.read_text())
        check('prior_complete', prior['state'] == 'complete')
        for table in ['inputs', 'outputs']:
            for name, expected in prior[table].items():
                if digest(root / name) != expected:
                    raise RuntimeError('Previously sealed evidence changed: ' + name)
                report['inputs'][name] = expected
        for name in ['annular_canonical_inverse_boundary_20260911.py', Path(__file__).name]:
            path = root / 'scripts' / name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
            snapshot = destination / ('executed-' + name)
            snapshot.write_bytes(path.read_bytes())
            own(snapshot, 'outputs')
        radius, geometry, lapse, kappa, gradient, velocity, force, drive = symbolic.symbols('R F N kappa w q Gchi v', nonzero=True)
        coefficient = kappa * radius**2 * geometry * gradient + kappa * symbolic.sqrt(geometry) * force / lapse
        gram_trace = -kappa * symbolic.sqrt(geometry) * velocity * force / lapse
        check('symbolic_inverse_trace_identity', symbolic.simplify(coefficient * velocity - (kappa * radius**2 * geometry * velocity * gradient - gram_trace)) == 0)
        check('symbolic_inverse_drive_solution', symbolic.simplify((coefficient * velocity - drive).subs(velocity, drive / coefficient)) == 0)
        coefficient_rate, drive_rate, velocity_rate = symbolic.symbols('Ddot vdot qdot')
        check('symbolic_next_jet_product_rule', symbolic.simplify(coefficient_rate * velocity + coefficient * ((drive_rate - coefficient_rate * velocity) / coefficient) - drive_rate) == 0)
        outer_mass, outer_clock, outer_lapse = symbolic.symbols('m C Nout', real=True)
        clock_variation = outer_lapse / (kappa * symbolic.sqrt(1 - 2 * outer_mass / radius)) - outer_clock / kappa
        check('symbolic_outer_natural_clock', symbolic.simplify(clock_variation.subs(outer_lapse, outer_clock * symbolic.sqrt(1 - 2 * outer_mass / radius))) == 0)
        parameter_path = root / 'source-intake/navier-stokes/20260909/annular-constraint-correction-initial/canonical.json'
        own(parameter_path)
        constants = {name: float(symbolic.sympify(value)) for name, value in json.loads(parameter_path.read_text())['parameters'].items()}
        roots = root / 'source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02'
        coarse_dir = intake / 'annular-canonical-initial-data-nodal01'
        common = archive(coarse_dir / 'canonical_N16_GR_sample0.npz')['boundary_velocity']
        completed_primary = []
        cases = [(16, branch, normalized) for normalized in [False, True] for branch in ['GR', 'metric_Gram']]
        for mesh, branch, normalized in cases:
            label = 'N' + str(mesh) + '_' + branch + ('_outer_clock' if normalized else '_fixed_lapse_control')
            print('Starting ' + label, flush=True)
            source = archive(roots / ('canonical_N' + str(mesh) + '_' + branch + '_sample0.npz'))
            old_path = coarse_dir / ('canonical_N16_' + branch + '_sample0.npz') if mesh == 16 else intake / 'annular-canonical-mesh-continuation-attempt02' / ('N32_' + branch + '_original_slopes_control.npz')
            saved = archive(old_path)
            check(label + '_source_root_not_failed', abs(saved['full_residual'] / saved['row_scales']).max() < 1e-10 if 'full_residual' in saved else abs(numerical.concatenate([saved['constraint'], saved['residual']]) / saved['row_scales']).max() < 1e-10)
            basis = MixedActionBasis(source['basis_radii'])
            count = basis.radii.size
            configuration, momenta = source['original_configuration'], source['original_momenta']
            packed = (source['initial_root_box_lower'] + source['initial_root_box_upper']) / 2
            system = ReleasedHermiteRouthian(basis, configuration[:count], configuration[count:], constants, .1, momenta[:count], momenta[count:], source['affine_clock'][0], MetricLinkQuadrature(basis))
            model = InverseBoundaryInitialData(system, packed, configuration, branch != 'GR', common.copy(), normalize_clock=normalized)
            model.pi_coeff_seed = saved['pi_coefficients'].copy()
            check(label + '_unchanged_scalar_and_momentum_corrections', numerical.array_equal(configuration, saved['configuration']) and numerical.array_equal(model.pi_coeff_seed[count:], saved['pi_coefficients'][count:]))
            seed = saved['state'].copy()
            scales = saved['row_scales'].copy()
            reduction = InverseBoundaryMassReduction(model)
            original_diagnostics = model.diagnostics(seed)[1]
            projected, unused_history = reduction.project(seed)
            full = model.data_jacobian(projected)
            mass_block, other_block = reduction.constraint_blocks(projected)
            block_error = float(abs(numerical.concatenate([mass_block, other_block], axis=1) - full[:count]).max())
            check(label + '_analytic_mass_blocks_unchanged', block_error < 1e-10, block_error)
            reduced, tangent, unused_mass = reduction.reduced_jacobian(projected)
            chain_error = float(abs(reduced - full[count:] @ tangent).max())
            check(label + '_complete_chain_includes_clock_and_Gram', chain_error < 1e-9, chain_error)
            direction = numerical.cos(numerical.arange(count + 3) + .6) * numerical.maximum(abs(projected[count:]), .001)
            step = 1e-5
            plus, unused_plus = reduction.project(projected + step * (tangent @ direction))
            minus, unused_minus = reduction.project(projected - step * (tangent @ direction))
            finite = (model.data_residual(plus)[count:] - model.data_residual(minus)[count:]) / (2 * step)
            error = float(abs(finite - reduced @ direction).max() / max(1., float(abs(reduced @ direction).max())))
            check(label + '_projected_finite_difference_control', error < 1e-7, error)

            def progress(history, state):
                report['active_case'] = {'label': label, 'history': history}
                numerical.savez_compressed(destination / 'recovery-active.npz', state=state, row_scales=scales, pi_coeff_seed=model.pi_coeff_seed, configuration=configuration, boundary_velocity=common, normalize_clock=numerical.array(normalized))
                save()

            solved = reduction.solve(seed, scales, progress)
            state = solved['state']
            residual = model.data_residual(state)
            evaluation, diagnostic = model.diagnostics(state)
            mass_coefficients, pi_coefficients, unused_reactions = model.set_state(state)
            sampled = fields(model, mass_coefficients, pi_coefficients, model.radius, evaluation['scalar_velocity'])
            arrays = {'state': state, 'seed_state': seed, 'row_scales': scales, 'full_residual': residual, 'mass_coefficients': mass_coefficients, 'pi_coefficients': pi_coefficients, 'fixed_lapse': model.fixed_lapse, 'configuration': configuration, 'boundary_velocity': common, 'normalize_clock': numerical.array(normalized), 'mass_block': mass_block, 'seed_reduced_jacobian': reduced, 'seed_tangent': tangent}
            arrays.update({name: value for name, value in evaluation.items() if isinstance(value, numerical.ndarray)})
            arrays.update({'sample_' + name: value for name, value in sampled.items()})
            if model.include_gram:
                arrays.update({'Gram_' + name: value for name, value in evaluation['sources'].items()})
                endpoint = numerical.exp(evaluation['sources']['endpoint_log'])
                links = model.links
                density = links.collect(links.sweight * endpoint * (basis.radii**2 * model.fixed_lapse * numerical.sqrt(model.node_f))[links.node])
                amplitude_time = links.collect(links.tweight * evaluation['scalar_velocity'][links.node] * endpoint)
                current = model.amplitude[links.factor] * (links.sweight * (basis.radii**2 * model.fixed_lapse * numerical.sqrt(model.node_f))[links.node] * amplitude_time[links.factor] - links.tweight * evaluation['scalar_velocity'][links.node] * density[links.factor]) / basis.spacing
                selected = links.node == 0
                direct_trace = -.1 * numerical.sqrt(model.node_f[0]) / model.fixed_lapse[0] * numerical.sum(current[selected] / endpoint[selected])
                check(label + '_independent_oriented_Gram_trace', abs(direct_trace - diagnostic['Gram_P_trace']) < 1e-11, float(abs(direct_trace - diagnostic['Gram_P_trace'])))
                check(label + '_Gram_omission_detectable', abs(diagnostic['Gram_P_trace']) > 1e-12)
            check(label + '_finite_arrays', all(numerical.all(numerical.isfinite(value)) for value in arrays.values()))
            output = destination / (label + '.npz')
            numerical.savez_compressed(output, **arrays)
            with numerical.load(output, allow_pickle=False) as reread:
                check(label + '_archive_roundtrip', set(reread.files) == set(arrays) and all(numerical.array_equal(value, reread[name]) for name, value in arrays.items()))
            own(output, 'outputs')
            if normalized:
                check(label + '_outer_clock_exact_to_roundoff', abs(diagnostic['outer_clock_gap']) < 1e-14)
            if solved['converged']:
                check(label + '_full_root_gates', abs(residual).max() < 1e-9 and abs(residual / scales).max() < 1e-10)
            record = {'label': label, 'mesh': mesh, 'branch': branch, 'normalize_clock': normalized, 'status': 'converged' if solved['converged'] else 'not_converged', 'failure': solved['failure'], 'history': solved['history'], 'source_archive': str(old_path.relative_to(root)), 'absolute_residual': float(abs(residual).max()), 'scaled_residual': float(abs(residual / scales).max()), 'mass_residual': float(abs(residual[:count]).max()), 'constraint_rate_residual': float(abs(evaluation['constraint_rate']).max()), 'diagnostics': diagnostic, 'source_diagnostics': original_diagnostics, 'bulk_density_L2': float(numerical.sqrt(model.weights @ sampled['bulk_density']**2)), 'pi_total_variation_sampled': float(model.weights @ abs(sampled['pi_gradient'])), 'block_error': block_error, 'chain_error': chain_error, 'directional_error': error, 'classical_boundary_certified': False, 'valid_for_physics_claim': False}
            report['samples'].append(record)
            save()
            print(json.dumps({name: record[name] for name in ['label', 'status', 'absolute_residual', 'failure', 'diagnostics']}), flush=True)
            if normalized and mesh == 16:
                completed_primary.append(solved['converged'])
                if len(completed_primary) == 2:
                    if all(completed_primary):
                        cases.extend([(32, later_branch, True) for later_branch in ['GR', 'metric_Gram']])
                    else:
                        report['N32_policy'] = 'Not run: both primary N16 branches must converge first; failed states never evolved or transferred.'
        for module in tuple(sys.modules.values()):
            filename = getattr(module, '__file__', None)
            if filename:
                path = Path(filename).resolve()
                if path.parent == root / 'scripts' and path.suffix == '.py':
                    own(path)
        check('no_python_cache', not (root / 'scripts/__pycache__').exists())
        report['state'] = 'complete'
        report['completed_utc'] = datetime.now(timezone.utc).isoformat()
        save()
        print('Inverse boundary preparation complete.', flush=True)
    except Exception as error:
        report['state'] = 'failed'
        report['error'] = repr(error)
        save()
        raise


if __name__ == '__main__':
    run()
