import argparse
import hashlib
import json
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from scipy.linalg import solve
    from annular_adm_mixed_action_20260909 import MixedActionBasis
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian
    from annular_canonical_boundary_20260911 import CanonicalBoundarySystem, wronskian_tent

    parser = argparse.ArgumentParser()
    parser.add_argument('--attempt', required=True)
    parser.add_argument('--sizes', nargs='+', type=int, default=[16, 32, 64])
    arguments = parser.parse_args()
    if not arguments.attempt.isalnum() or any(size not in [16, 32, 64] for size in arguments.sizes):
        raise ValueError('Fresh alphanumeric attempt and supported mesh sizes required.')
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260911'
    destination = intake / ('annular-canonical-boundary-' + arguments.attempt)
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': {}, 'outputs': {}, 'checks': [], 'samples': [], 'valid_for_physics_claim': False, 'new_evolution': False, 'interval_certificate': False, 'inner_boundary_flux_parent_selected': False, 'scope': 'Parent-derived canonical bulk reformulation plus nonlocal Gram slice adjoint; boundary-conditioned initial multiplier solve. Inner flux is a named inherited diagnostic port, not a new physical boundary law. No earlier residence certificate transfers.'}

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def own(path):
        report['inputs'][str(path.relative_to(root))] = digest(path)

    def artifact(path):
        report['outputs'][str(path.relative_to(root))] = digest(path)

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    save()
    try:
        prior_path = intake / 'annular-initial-jet-adjoint-final-integrity.json'
        own(prior_path)
        prior = json.loads(prior_path.read_text())
        check('prior_complete', prior['state'] == 'complete')
        for table in ['inputs', 'outputs']:
            for name, expected in prior[table].items():
                if digest(root / name) != expected:
                    raise RuntimeError('Changed inherited evidence: ' + name)
                report['inputs'][name] = expected
        for name in ['annular_canonical_boundary_20260911.py', Path(__file__).name]:
            path = root / 'scripts' / name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
            output = destination / ('executed-' + name)
            output.write_bytes(path.read_bytes())
            artifact(output)
        radius, lapse, spatial_f, kappa = symbolic.symbols('R N F kappa', positive=True)
        lapse_r, scale_r, mass_r, mass_t, q, w, momentum, pi = symbolic.symbols('Nr ar mur mut q w P pi', real=True)
        shift = kappa * lapse * spatial_f**symbolic.Rational(3, 2) * momentum
        scale = 1 / symbolic.sqrt(spatial_f)
        weak = lapse * mass_r * scale / kappa + shift * mass_t / (kappa * lapse * spatial_f**symbolic.Rational(3, 2))
        weak -= radius * (scale_r * lapse + scale * lapse_r) * shift**2 / (2 * kappa * lapse**2)
        weak += radius**2 * scale * (q - shift * w)**2 / (2 * lapse) - radius**2 * lapse * w**2 / (2 * scale)
        canonical = momentum * mass_t + pi * q + lapse * mass_r * scale / kappa
        canonical -= lapse * symbolic.sqrt(spatial_f) * (pi**2 / (2 * radius**2) + radius**2 * w**2 / 2)
        canonical -= kappa * lapse * spatial_f**symbolic.Rational(3, 2) * momentum * pi * w
        canonical -= kappa * radius * spatial_f**3 * (scale_r * lapse + scale * lapse_r) * momentum**2 / 2
        pi_stationary = radius**2 * scale * (q - shift * w) / lapse
        check('exact_bulk_auxiliary_elimination_recovers_parent', symbolic.simplify(canonical.subs(pi, pi_stationary) - weak) == 0)
        check('exact_canonical_bulk_linear_in_N_and_Nr', all(symbolic.diff(canonical, first, second) == 0 for first in [lapse, lapse_r] for second in [lapse, lapse_r]))
        check('exact_physical_boundary_flux_pullback', symbolic.simplify(radius * scale * shift**2 / (2 * kappa * lapse) - kappa * radius * lapse * spatial_f**symbolic.Rational(5, 2) * momentum**2 / 2) == 0)
        connection = symbolic.simplify(shift / (lapse**2 * spatial_f - shift**2))
        check('canonical_connection_lapse_derivative', symbolic.simplify(symbolic.diff(connection, lapse) + connection / lapse) == 0)
        case_path = root / 'source-intake/navier-stokes/20260909/annular-constraint-correction-initial/canonical.json'
        own(case_path)
        constants = {name: float(symbolic.sympify(value)) for name, value in json.loads(case_path.read_text())['parameters'].items()}
        roots = root / 'source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02'
        for size in arguments.sizes:
            for branch in ['GR', 'metric_Gram']:
                label = 'canonical_N' + str(size) + '_' + branch + '_sample0'
                print('Starting ' + label, flush=True)
                report['active_sample'] = label
                save()
                source = roots / (label + '.npz')
                reference = intake / ('annular-time-link-adjoint-attempt01' if size == 16 else 'annular-initial-mesh-control-attempt01') / (label + '.npz')
                own(source)
                own(reference)
                with numerical.load(source) as archive:
                    saved = {name: archive[name].copy() for name in archive.files}
                with numerical.load(reference) as archive:
                    old = {name: archive[name].copy() for name in archive.files}
                basis = MixedActionBasis(saved['basis_radii'])
                count = basis.radii.size
                configuration, momenta = saved['original_configuration'], saved['original_momenta']
                packed = (saved['initial_root_box_lower'] + saved['initial_root_box_upper']) / 2
                system = ReleasedHermiteRouthian(basis, configuration[:count], configuration[count:], constants, .1, momenta[:count], momenta[count:], saved['affine_clock'][0], MetricLinkQuadrature(basis))
                velocity = packed[system.slices[2].start:]
                flux_port = float(old['mass_rate'][0])
                model = CanonicalBoundarySystem(system, packed, configuration, False, [flux_port, velocity[0], velocity[count - 1]])
                eigenvalues, eigenvectors = numerical.linalg.eigh(old['schur'])
                peak = 1 + int(abs(velocity[1:count - 1]).argmin())
                tent, primitive = wronskian_tent(basis.radii, model.lapse_seed, peak)
                normalized_tent = tent / numerical.linalg.norm(tent)
                alignment = float(abs(normalized_tent @ eigenvectors[:, 0]))
                wronskian = (model.lapse_seed[:-1] * tent[1:] - tent[:-1] * model.lapse_seed[1:]) / numerical.diff(basis.radii)
                wronskian_jump = numerical.diff(wronskian)
                nonpeak = numerical.delete(wronskian_jump, peak - 1)
                predicted_jump = -velocity[peak] / model.lapse_seed[peak]**3 * (1 / primitive[peak] + 1 / (primitive[-1] - primitive[peak]))
                actual_jump = velocity[peak] / model.lapse_seed[peak]**2 * wronskian_jump[peak - 1]
                check(label + '_Wronskian_tent_derived_not_fit', abs(nonpeak).max() < 1e-9 and abs(predicted_jump - actual_jump) < 1e-10 and tent[0] == 0 and tent[-1] == 0, {'alignment_with_smallest_mode': alignment, 'peak': peak, 'q_peak': float(velocity[peak]), 'predicted_product_derivative_jump': float(predicted_jump)})
                matrix, load = model.gr_linear_system()
                skew_error = float(abs(matrix + matrix.T).max())
                check(label + '_GR_Dirac_matrix_skew_control', skew_error < 1e-10, skew_error)
                answer = solve(matrix, load)
                reference_gr = answer.copy()
                check(label + '_GR_multiplier_solve_residual', abs(model.evaluate(answer)['residual']).max() < 1e-9)
                history = []
                if branch != 'GR':
                    model.include_gram = True
                    scales = numerical.maximum(numerical.max(abs(matrix), axis=1), 1e-12)
                    for iteration in range(15):
                        evaluated = model.evaluate(answer)
                        residual = evaluated['residual']
                        merit = float(abs(residual / scales).max())
                        history.append({'iteration': iteration, 'scaled_residual': merit, 'absolute_residual': float(abs(residual).max()), 'minimum_lapse': float(answer[:count].min())})
                        report['working_Newton_history'] = history.copy()
                        save()
                        print(json.dumps(history[-1]), flush=True)
                        if merit < 1e-10:
                            break
                        derivative = model.jacobian(answer)
                        correction = solve(derivative / scales[:, None], -residual / scales)
                        accepted = False
                        for power in range(18):
                            candidate = answer + correction * 2.**(-power)
                            if candidate[:count].min() <= .02:
                                continue
                            try:
                                candidate_merit = float(abs(model.evaluate(candidate)['residual'] / scales).max())
                            except ValueError:
                                continue
                            if candidate_merit < merit:
                                answer, accepted = candidate, True
                                break
                        if not accepted:
                            report['failed_Newton_diagnostics'] = {'correction_max': float(abs(correction).max()), 'jacobian_condition': float(numerical.linalg.cond(derivative)), 'smallest_trial_merit': candidate_merit if 'candidate_merit' in locals() else None}
                            raise RuntimeError('Positive-chart Newton step failed: ' + label)
                    else:
                        raise RuntimeError('Newton iteration limit: ' + label)
                result = model.evaluate(answer)
                check(label + '_coupled_constraints_and_boundary_velocities', abs(result['residual']).max() < 1e-9, float(abs(result['residual']).max()))
                check(label + '_positive_lapse_chart', answer[:count].min() > 0, [float(answer[:count].min()), float(answer[:count].max())])
                density = model.mass_r / (.1 * numerical.sqrt(model.spatial_f)) - numerical.sqrt(model.spatial_f) * (model.pi**2 / (2 * model.radius**2) + model.radius**2 * model.scalar_gradient**2 / 2)
                constraint = basis.node_value.T @ (model.weights * density)
                if branch != 'GR':
                    constraint -= basis.radii**2 * numerical.sqrt(model.node_f) * model.gram_density
                    check(label + '_weighted_time_current_conservation', abs(result['sources']['anchor_current']).max() < 1e-12)
                check(label + '_initial_canonical_constraints_preserved', abs(constraint).max() < 1e-9, float(abs(constraint).max()))
                arrays = {'unknown': answer, 'GR_seed_unknown': reference_gr, 'GR_Dirac_matrix': matrix, 'GR_Dirac_load': load, 'initial_constraint': constraint, 'tent': tent, 'old_smallest_mode': eigenvectors[:, 0], 'boundary_velocity': model.boundary_velocity}
                arrays.update({name: value for name, value in result.items() if isinstance(value, numerical.ndarray)})
                for name in ['pi_map', 'momentum_map', 'mass_pair', 'scalar_pair', 'mass_inverse', 'scalar_inverse']:
                    arrays[name] = getattr(model, name)
                arrays.update({'map_' + name: value for name, value in model.maps.items()})
                output = destination / (label + '.npz')
                numerical.savez_compressed(output, **arrays)
                with numerical.load(output) as archive:
                    check(label + '_archive_roundtrip', set(archive.files) == set(arrays) and all(numerical.array_equal(value, archive[name]) for name, value in arrays.items()))
                artifact(output)
                row = {'label': label, 'lapse_range': [float(answer[:count].min()), float(answer[:count].max())], 'maximum_lapse_change_from_seed': float(abs(answer[:count] - model.lapse_seed).max()), 'constraint_rate_max': float(abs(result['constraint_rate']).max()), 'boundary_velocity_residual_max': float(abs(result['boundary_residual']).max()), 'initial_constraint_max': float(abs(constraint).max()), 'GR_Dirac_condition': float(numerical.linalg.cond(matrix)), 'final_jacobian_condition': float(numerical.linalg.cond(model.jacobian(answer))) if branch != 'GR' else float(numerical.linalg.cond(matrix)), 'reaction_multipliers': answer[count:].tolist(), 'inner_flux_reference': flux_port, 'inner_flux_physical_law_selected': False, 'old_weak_mode_tent_alignment': alignment, 'scalar_zero_near_peak': float(velocity[peak]), 'time_link_max_logJ': float(abs(result['sources']['endpoint_log']).max()) if branch != 'GR' else None, 'Newton_history': history, 'midpoint_initial_repair': True, 'evolution_certificate': False, 'interval_certificate': False}
                report['samples'].append(row)
                save()
                print(json.dumps(row), flush=True)
        for module in tuple(sys.modules.values()):
            filename = getattr(module, '__file__', None)
            if filename:
                path = Path(filename).resolve()
                if path.parent == root / 'scripts' and path.suffix == '.py':
                    own(path)
        check('no_python_cache', not (root / 'scripts/__pycache__').exists())
        report['state'] = 'complete'
        report['completed_utc'] = datetime.now(timezone.utc).isoformat()
        report.pop('active_sample', None)
        save()
        print('Complete: ' + str(len(report['checks'])) + ' checks', flush=True)
    except Exception as error:
        report['state'] = 'failed'
        report['error'] = repr(error)
        report['traceback'] = traceback.format_exc()
        save()
        raise


if __name__ == '__main__':
    run()
