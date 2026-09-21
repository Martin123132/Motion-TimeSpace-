import argparse
import hashlib
import json
import re
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from scipy.linalg import eigvalsh, solve
    from annular_adm_mixed_action_20260909 import MixedActionBasis
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian
    from annular_endpoint_metric_adjoint_20260910 import metric_schur_response, response_neighborhood_bound

    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['derive', 'seal'])
    parser.add_argument('--attempt', default='derived')
    arguments = parser.parse_args()
    if not re.fullmatch('[a-z0-9-]+', arguments.attempt):
        raise ValueError('Invalid attempt identifier.')
    root = Path(__file__).resolve().parents[1]
    old = root / 'source-intake/navier-stokes/20260909'
    intake = root / 'source-intake/navier-stokes/20260910'
    destination = intake / ('annular-endpoint-metric-adjoint-' + arguments.attempt)
    prior_path = intake / 'annular-boundary-source-variation-final-integrity.json'
    final_path = intake / 'annular-endpoint-metric-adjoint-final-integrity.json'
    inputs, outputs = {}, {}

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def own(path):
        inputs[str(path.relative_to(root))] = digest(path)

    def artifact(path):
        outputs[str(path.relative_to(root))] = digest(path)

    def inherit(table, inherited):
        for name, expected in inherited.items():
            actual = digest(root / name)
            if actual != expected or name in table and table[name] != actual:
                raise RuntimeError('Changed evidence: ' + name)
            table[name] = actual

    def loaded(path):
        own(path)
        with numerical.load(path) as handle:
            return {name: handle[name].copy() for name in handle.files}

    prior = json.loads(prior_path.read_text())
    if prior['state'] != 'complete':
        raise RuntimeError('Prior gate incomplete.')
    inherit(inputs, prior['inputs'])
    inherit(outputs, prior['outputs'])
    own(prior_path)
    for name in ['annular_endpoint_metric_adjoint_20260910.py', 'derive_annular_endpoint_metric_adjoint_20260910.py']:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    if arguments.phase == 'derive':
        destination.mkdir(exist_ok=False)
        (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())
        report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': inputs, 'outputs': outputs, 'checks': [], 'samples': [], 'physical_time_interval_certified': False, 'uniform_parent_inverse_proved': False, 'new_evolution': False, 'interval_arithmetic_certificate': False, 'valid_for_physics_claim': False}

        def save():
            (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

        def check(name, passed, detail=None):
            report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
            if not passed:
                raise RuntimeError('Failed check: ' + name + ' ' + repr(detail))

        def close(name, first, second, tolerance=2e-9):
            error = float(numerical.max(abs(numerical.asarray(first) - second)))
            scale = 1 + float(numerical.max(abs(numerical.asarray(second))))
            check(name, error <= tolerance * scale, {'error': error, 'scale': scale})

        save()
        try:
            case_path = old / 'annular-constraint-correction-initial/canonical.json'
            parent_path = intake / 'annular-boundary-source-variation-derived/status.json'
            own(case_path)
            own(parent_path)
            case = json.loads(case_path.read_text())
            constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
            kappa = float(symbolic.sympify(case['normalization_kappa']))
            random = numerical.random.default_rng(20260910)
            check('zero_perturbation_identity', response_neighborhood_bound(2., 3., 4., 0., 0., 0., 0.)['response_change_upper'] == 0.)
            check('threshold_equality_refused', not response_neighborhood_bound(2., 3., 4., .5, 0., 0., 0.)['gate'])
            check('threshold_excess_refused', not response_neighborhood_bound(2., 3., 4., .6, 0., 0., 0.)['gate'])
            for invalid in [-1., float('nan'), float('inf')]:
                try:
                    response_neighborhood_bound(2., 3., 4., invalid, 0., 0., 0.)
                except ValueError:
                    rejected = True
                else:
                    rejected = False
                check('invalid_perturbation_' + str(invalid) + '_refused', rejected)
            for sample in json.loads(parent_path.read_text())['samples']:
                label, intervals, branch = sample['label'], sample['intervals'], sample['branch']
                report['active_sample'] = label
                save()
                tag, index = label.split('_sample')[0], int(label.rsplit('sample', 1)[1])
                steps = 64 if intervals == 64 else 32
                initial = loaded(old / 'annular-released-Hermite-initial-derived' / (tag + '.npz'))
                spatial = loaded(old / 'annular-spatial-clock-energy-derived' / (label + '.npz'))
                jets = loaded(old / 'annular-metric-flux-jets-derived' / (label + '.npz'))
                base = loaded(old / 'annular-first-derivative-energy-derived' / (label + '.npz'))
                source = loaded(intake / 'annular-boundary-source-variation-derived' / (label + '.npz'))
                folder = 'annular-boundary-N64-evolution-smoke' if intervals == 64 else 'annular-released-Hermite-evolution-smoke'
                trajectory = loaded(old / folder / (tag + '_steps' + str(steps) + '.npz'))
                basis = MixedActionBasis(initial['radius'])
                count = basis.radii.size
                time, state = trajectory['time'][index], trajectory['state'][index]
                scalar, slope, momentum, slope_momentum = [state[part * count:(part + 1) * count] for part in range(4)]
                packed, speed, second = state[4 * count:], spatial['packed_speed'], jets['jet_acceleration']
                system = ReleasedHermiteRouthian(basis, scalar, slope, constants, kappa, momentum, slope_momentum, initial['outer_clock'][0] + time * initial['outer_clock'][1], MetricLinkQuadrature(basis))
                data = metric_schur_response(system, packed, speed, second, source['third_parent_jet'], source['known_third'], branch != 'GR')
                jacobian, metric, velocity, free = [data[name] for name in ['jacobian', 'metric_indices', 'velocity_indices', 'full_free']]
                close(label + '_free_parent_partition_preserved', free, system.free)
                close(label + '_original_J_symmetric', jacobian, jacobian.T)
                close(label + '_canonical_kinetic_is_actual_mass', data['kinetic'], base['M'])
                close(label + '_kinetic_matches_positive_quadrature', data['kinetic'], data['kinetic_quadrature_matrix'])
                check(label + '_kinetic_positive', eigvalsh(data['kinetic'])[0] > 0)
                close(label + '_metric_third_reconstruction', data['metric_third'], source['third_parent_jet'][metric])
                close(label + '_scalar_third_reconstruction', data['velocity_third'], source['third_parent_jet'][velocity])
                close(label + '_sourced_theta_tt_functional', data['functional'] @ source['third_parent_jet'] + data['lower'], source['theta_tt'])
                close(label + '_adjoint_theta_tt_identical', data['predicted_theta_tt'], source['theta_tt'])
                close(label + '_schur_equation_residual', data['schur'] @ data['metric_third'], data['reduced_forcing'])
                close(label + '_adjoint_equation_residual', data['schur'].T @ data['adjoint'], data['target'].T)
                full_jacobian = jacobian[numerical.ix_(free, free)]
                full_adjoint = solve(full_jacobian.T, data['functional'][:, free].T, assume_a='sym')
                close(label + '_independent_full_adjoint_reconstruction', data['full_adjoint'], full_adjoint)
                close(label + '_full_adjoint_response', data['offset'] + full_adjoint.T @ data['forcing'][free], source['theta_tt'])
                close(label + '_normalized_adjoint_response', data['offset'] + data['normalized_adjoint'].T @ data['normalized_forcing'], source['theta_tt'])
                close(label + '_normalized_adjoint_equation', data['normalized_schur'].T @ data['normalized_adjoint'], data['normalized_target'].T)
                lapse_positions = data['lapse_positions']
                lapse_block = data['schur'][numerical.ix_(lapse_positions, lapse_positions)]
                close(label + '_lapse_schur_exact_projection_residual', lapse_block, data['lapse_residual_gram'])
                check(label + '_lapse_residual_gram_PSD', eigvalsh(data['lapse_residual_gram'])[0] >= -1e-12)
                spectrum = data['normalized_spectrum']
                check(label + '_normalized_metric_invertible_at_saved_state', min(abs(spectrum)) > 1e-10)
                for upper_name in ['theta_schur_component_upper', 'theta_full_component_upper', 'theta_natural_upper']:
                    check(label + '_' + upper_name, numerical.all(abs(source['theta_tt']) <= data[upper_name] + 1e-9))
                endpoint_time = abs(base['lift_velocity'][:count][[0, -1]])
                rate_without_third = numerical.asarray(sample['bounds']['beta_time_abs_endpoint_upper']) - abs(source['theta_tt']) * endpoint_time
                check(label + '_rate_remainder_nonnegative', min(rate_without_third) >= -1e-12)
                rates = {}
                for kind in ['schur_component', 'full_component', 'natural']:
                    upper = rate_without_third + data['theta_' + kind + '_upper'] * endpoint_time
                    rates[kind] = float(numerical.linalg.norm(upper))
                    check(label + '_beta_rate_' + kind + '_bound', numerical.all(abs(source['repacked_beta_time']) <= upper + 1e-9))
                for endpoint in range(2):
                    alignment = 1. if data['offset'][endpoint] >= 0 else -1.
                    adversarial = alignment * numerical.sign(data['adjoint'][:, endpoint]) * abs(data['reduced_forcing'])
                    response = data['offset'][endpoint] + data['target'][endpoint] @ solve(data['schur'], adversarial, assume_a='sym')
                    close(label + '_sharp_independent_reduced_box_' + str(endpoint), abs(response), data['theta_schur_component_upper'][endpoint])
                normalized = data['normalized_schur']
                inverse_norm = data['normalized_inverse_norm']
                dimension = normalized.shape[0]
                perturbation = random.normal(size=(dimension, dimension))
                perturbation = (perturbation + perturbation.T) / 2
                perturbation *= .2 / (inverse_norm * max(abs(eigvalsh(perturbation))))
                delta_matrix = float(max(abs(eigvalsh(perturbation))))
                forced_change = random.normal(size=dimension)
                forced_change *= .01 * (1 + numerical.linalg.norm(data['normalized_forcing'])) / numerical.linalg.norm(forced_change)
                control_bounds = []
                for endpoint in range(2):
                    target_change = random.normal(size=dimension)
                    target_change *= .01 * numerical.linalg.norm(data['normalized_target'][endpoint]) / numerical.linalg.norm(target_change)
                    offset_change = .001
                    bound = response_neighborhood_bound(inverse_norm, data['adjoint_natural_norms'][endpoint], numerical.linalg.norm(data['normalized_forcing']), delta_matrix, numerical.linalg.norm(target_change), numerical.linalg.norm(forced_change), offset_change)
                    check(label + '_neighborhood_gate_' + str(endpoint), bound['gate'])
                    changed_adjoint = solve((normalized + perturbation).T, data['normalized_target'][endpoint] + target_change, assume_a='sym')
                    changed_response = data['offset'][endpoint] + offset_change + changed_adjoint @ (data['normalized_forcing'] + forced_change)
                    delta_response = abs(changed_response - data['predicted_theta_tt'][endpoint])
                    check(label + '_neighborhood_response_control_' + str(endpoint), delta_response <= bound['response_change_upper'] + 1e-8)
                    check(label + '_neighborhood_adjoint_control_' + str(endpoint), numerical.linalg.norm(changed_adjoint - data['normalized_adjoint'][:, endpoint]) <= bound['adjoint_change_upper'] + 1e-8)
                    control_bounds.append(dict(bound, observed_response_change=float(delta_response)))
                output = destination / (label + '.npz')
                saved_names = ['metric_indices', 'velocity_indices', 'schur', 'reduced_forcing', 'metric_third', 'velocity_third', 'functional', 'lower', 'adjoint', 'full_adjoint', 'offset', 'predicted_theta_tt', 'theta_schur_component_upper', 'theta_full_component_upper', 'theta_natural_upper', 'metric_weight', 'normalized_schur', 'normalized_forcing', 'normalized_target', 'normalized_adjoint', 'normalized_spectrum', 'lapse_residual_gram', 'lapse_projection_error']
                numerical.savez_compressed(output, **{name: data[name] for name in saved_names})
                artifact(output)
                row = {'label': label, 'intervals': intervals, 'branch': branch, 'time': float(time), 'theta_tt': source['theta_tt'].tolist(), 'theta_schur_component_upper': data['theta_schur_component_upper'].tolist(), 'theta_full_component_upper': data['theta_full_component_upper'].tolist(), 'theta_natural_upper': data['theta_natural_upper'].tolist(), 'beta_rate_upper': rates, 'old_endpoint_rate_upper': sample['bounds']['beta_rate_R2_upper'], 'old_whole_parent_rate_upper': sample['bounds']['beta_rate_parent_solve_R2_upper'], 'adjoint_natural_norms': data['adjoint_natural_norms'].tolist(), 'normalized_metric_inverse_norm': inverse_norm, 'normalized_metric_min_abs_eigenvalue': float(min(abs(spectrum))), 'normalized_metric_inertia': {'negative': int(sum(spectrum < 0)), 'positive': int(sum(spectrum > 0))}, 'lapse_schur_frobenius_norm': float(numerical.linalg.norm(lapse_block)), 'metric_third_max': float(max(abs(data['metric_third']))), 'scalar_velocity_third_max': float(max(abs(data['velocity_third']))), 'reduced_forcing_natural_norm': float(numerical.linalg.norm(data['normalized_forcing'])), 'neighborhood_controls': control_bounds, 'scope': 'Pointwise actual-parent functional bounds and manufactured algebraic neighborhoods; no actual physical time interval or continuum claim.'}
                report['samples'].append(row)
                if index == steps:
                    print(json.dumps(row), flush=True)
                save()
            for module in tuple(sys.modules.values()):
                filename = getattr(module, '__file__', None)
                if filename:
                    path = Path(filename).resolve()
                    if path.parent == root / 'scripts' and path.suffix == '.py':
                        own(path)
            check('all_inherited_inputs_preserved', all(digest(root / name) == expected for name, expected in inputs.items()))
            check('all_inherited_and_new_outputs_preserved', all(digest(root / name) == expected for name, expected in outputs.items()))
            check('no_bytecode_cache', not (root / 'scripts/__pycache__').exists())
            report.update(state='complete', passed=sum(row['passed'] for row in report['checks']), total=len(report['checks']), completed_utc=datetime.now(timezone.utc).isoformat())
            report.pop('active_sample', None)
            save()
            (destination / 'COMPLETE').write_text(report['completed_utc'] + '\n')
            print(json.dumps({name: report[name] for name in ['state', 'passed', 'total', 'completed_utc']}), flush=True)
            return
        except Exception as error:
            report.update(state='failed', failure=repr(error), traceback=traceback.format_exc())
            save()
            raise
    report_path = destination / 'status.json'
    report = json.loads(report_path.read_text())
    if report['state'] != 'complete' or report['passed'] != report['total']:
        raise RuntimeError('Endpoint metric validation incomplete.')
    inherit(inputs, report['inputs'])
    inherit(outputs, report['outputs'])
    for path in [report_path, destination / 'COMPLETE', destination / 'executed-script.py']:
        own(path)
    note = root / 'DERIVATION-20260910-endpoint-metric-adjoint-and-source-specific-bounds.md'
    cited = [value for value in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')) if value.endswith(('.py', '.md', '.json', '.npz'))]
    missing = [value for value in cited if root / value != final_path and not (root / value).is_file()]
    if missing:
        raise FileNotFoundError(str(missing))
    own(note)
    snapshot = intake / 'annular-endpoint-metric-adjoint-resume-snapshot.md'
    with snapshot.open('xb') as handle:
        handle.write((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    artifact(snapshot)
    frozen = root.parent / 'formalization-workbench'
    since = datetime(2026, 9, 10, 10, 42, 12, tzinfo=timezone.utc).timestamp()
    touched = [str(path.relative_to(frozen)) for path in frozen.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if touched or (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Protected workbench/cache check failed: ' + repr(touched))
    final = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'checks': report['total'], 'saved_states': len(report['samples']), 'inputs': inputs, 'outputs': outputs, 'cited_local_paths_checked': cited, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-10T10:42:12Z, not a full pre-turn hash baseline', 'no_bytecode_cache': True, 'metric_adjoint_and_lapse_projection_identity_derived': True, 'actual_interval_TV_and_uniform_parent_inverse_open': True, 'valid_for_physics_claim': False}
    with final_path.open('x') as handle:
        json.dump(final, handle, indent=2)
        handle.write('\n')
    print(json.dumps({name: final[name] for name in ['state', 'checks', 'saved_states', 'protected_workbench_files_written_since_turn_start']}), flush=True)


if __name__ == '__main__':
    run()
