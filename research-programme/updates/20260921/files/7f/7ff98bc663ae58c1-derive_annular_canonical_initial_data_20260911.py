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
    from scipy.linalg import solve
    from annular_adm_mixed_action_20260909 import MixedActionBasis
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian
    from annular_canonical_initial_data_20260911 import CanonicalInitialData
    from annular_canonical_nodal_data_20260911 import CanonicalInitialNodalData

    parser = argparse.ArgumentParser()
    parser.add_argument('--attempt', required=True)
    parser.add_argument('--sizes', nargs='+', type=int, default=[16, 32, 64])
    parser.add_argument('--free-data', choices=['nodal', 'bubble'], default='nodal')
    arguments = parser.parse_args()
    if not arguments.attempt.isalnum() or any(size not in [16, 32, 64] for size in arguments.sizes):
        raise ValueError('Invalid attempt or mesh.')
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260911'
    destination = intake / ('annular-canonical-initial-data-' + arguments.attempt)
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': {}, 'outputs': {}, 'checks': [], 'samples': [], 'free_data_protocol': arguments.free_data, 'inner_flux_policy': 'same inherited GR diagnostic mass-rate port for both branches at each mesh', 'inner_flux_parent_selected': False, 'initial_scalar_momenta_changed': True, 'old_residence_transferred': False, 'interval_certificate': False, 'valid_for_physics_claim': False, 'new_evolution': False}

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
    prior_path = intake / 'annular-initial-jet-adjoint-final-integrity.json'
    own(prior_path)
    prior = json.loads(prior_path.read_text())
    for table in ['inputs', 'outputs']:
        for name, expected in prior[table].items():
            if digest(root / name) != expected:
                raise RuntimeError('Inherited evidence changed: ' + name)
            report['inputs'][name] = expected
    check('prior_complete_and_hashes_match', prior['state'] == 'complete')
    for name in ['annular_canonical_boundary_20260911.py', 'annular_canonical_initial_data_20260911.py', 'annular_canonical_nodal_data_20260911.py', Path(__file__).name]:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
        output = destination / ('executed-' + name)
        output.write_bytes(path.read_bytes())
        artifact(output)
    case_path = root / 'source-intake/navier-stokes/20260909/annular-constraint-correction-initial/canonical.json'
    own(case_path)
    constants = {name: float(symbolic.sympify(value)) for name, value in json.loads(case_path.read_text())['parameters'].items()}
    roots = root / 'source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02'
    for size in arguments.sizes:
        port_path = intake / ('annular-time-link-adjoint-attempt01' if size == 16 else 'annular-initial-mesh-control-attempt01') / ('canonical_N' + str(size) + '_GR_sample0.npz')
        own(port_path)
        with numerical.load(port_path) as archive:
            flux_port = float(archive['mass_rate'][0])
        for branch in ['GR', 'metric_Gram']:
            label = 'canonical_N' + str(size) + '_' + branch + '_sample0'
            print('Starting ' + label, flush=True)
            source = roots / (label + '.npz')
            own(source)
            with numerical.load(source) as archive:
                saved = {name: archive[name].copy() for name in archive.files}
            basis = MixedActionBasis(saved['basis_radii'])
            count = basis.radii.size
            configuration, momenta = saved['original_configuration'], saved['original_momenta']
            packed = (saved['initial_root_box_lower'] + saved['initial_root_box_upper']) / 2
            system = ReleasedHermiteRouthian(basis, configuration[:count], configuration[count:], constants, .1, momenta[:count], momenta[count:], saved['affine_clock'][0], MetricLinkQuadrature(basis))
            velocity = packed[system.slices[2].start:]
            constructor = CanonicalInitialNodalData if arguments.free_data == 'nodal' else CanonicalInitialData
            model = constructor(system, packed, configuration, branch != 'GR', [flux_port, velocity[0], velocity[count - 1]])
            state = model.seed(numerical.array([10., .34, .58]))
            seed_state = state.copy()
            seed_mass_q = model.mass_q.copy()
            seed_pi = model.pi.copy()
            seed_mass_gradient = model.mass_r.copy()
            history, failure = [], None
            try:
                derivative = model.data_jacobian(state)
                scales = numerical.maximum(numerical.max(abs(derivative), axis=1), 1e-12)
                for iteration in range(25):
                    residual = model.data_residual(state)
                    merit = float(abs(residual / scales).max())
                    history.append({'iteration': iteration, 'scaled_residual': merit, 'absolute_residual': float(abs(residual).max())})
                    report['active_sample'] = {'label': label, 'history': history}
                    save()
                    if merit < 1e-10 and abs(residual).max() < 1e-9:
                        break
                    derivative = model.data_jacobian(state)
                    correction = solve(derivative / scales[:, None], -residual / scales)
                    accepted = False
                    for power in range(20):
                        trial = state + correction * 2.**(-power)
                        try:
                            trial_merit = float(abs(model.data_residual(trial) / scales).max())
                        except ValueError:
                            continue
                        if trial_merit < merit:
                            state, accepted = trial, True
                            break
                    if not accepted:
                        raise RuntimeError('Newton positive-metric line search failed.')
                else:
                    raise RuntimeError('Newton iteration limit.')
            except Exception as error:
                failure = repr(error)
            mass_coeff, pi_coeff, reactions = model.set_state(state)
            result = model.evaluate(numerical.concatenate([model.fixed_lapse, reactions]))
            constraint = model.constraint()
            density = model.mass_r / (.1 * numerical.sqrt(model.spatial_f)) - numerical.sqrt(model.spatial_f) * (model.pi**2 / (2 * model.radius**2) + model.radius**2 * model.scalar_gradient**2 / 2)
            seed_f = 1 - 2 * seed_mass_q / model.radius
            seed_density = seed_mass_gradient / (.1 * numerical.sqrt(seed_f)) - numerical.sqrt(seed_f) * (seed_pi**2 / (2 * model.radius**2) + model.radius**2 * model.scalar_gradient**2 / 2)
            raw = {'status': 'converged' if failure is None else 'not_converged', 'failure': failure, 'label': label, 'iterations': history, 'constraint_max': float(abs(constraint).max()), 'constraint_rate_max': float(abs(result['constraint_rate']).max()), 'boundary_velocity_residual': float(abs(result['boundary_residual']).max()), 'mass_field_change_max': float(abs(model.mass_q - seed_mass_q).max()), 'pi_coefficient_change_max': float(abs(pi_coeff - model.pi_coeff_seed).max()), 'scalar_velocity_field_change_max': float(abs(model.value @ (result['scalar_velocity'] - velocity)).max()), 'scalar_seed_velocity_field_max': float(abs(model.value @ velocity).max()), 'lapse_range': [float(model.fixed_lapse.min()), float(model.fixed_lapse.max())], 'minimum_F': float(model.spatial_f.min()), 'mass_gradient_range': [float(model.mass_r.min()), float(model.mass_r.max())], 'bulk_strong_constraint_sample_max_before': float(abs(seed_density).max()), 'bulk_strong_constraint_sample_max_after': float(abs(density).max()), 'strong_diagnostic_scope': 'Bulk density at stored quadrature only; excludes Gram point/nonlocal covectors and is NOT a full strong residual bound.', 'inner_flux': flux_port, 'inner_flux_parent_selected': False, 'initial_data_changed': True, 'parent_evolution_proved': False}
            if failure is None:
                check(label + '_all_initial_equations', max(raw['constraint_max'], raw['constraint_rate_max'], raw['boundary_velocity_residual']) < 1e-9)
                check(label + '_positive_metric', raw['minimum_F'] > .1 and raw['lapse_range'][0] > 0)
                check(label + '_fixed_lapse_and_inner_mass_preserved', numerical.array_equal(model.fixed_lapse, model.lapse_seed) and mass_coeff[0] == model.mass_coeff_seed[0])
                if arguments.free_data == 'nodal':
                    check(label + '_no_mass_bubble_initial_excitation', numerical.all(mass_coeff[model.face_count:] == 0))
                direction = numerical.sin(numerical.arange(state.size) + 1.) * numerical.maximum(abs(state), .001)
                derivative = model.data_jacobian(state)
                step = 1e-5
                finite = (model.data_residual(state + step * direction) - model.data_residual(state - step * direction)) / (2 * step)
                expected = derivative @ direction
                difference = float(abs(finite - expected).max() / max(1., float(abs(expected).max())))
                check(label + '_Jacobian_directional_control', difference < 1e-7, difference)
                model.set_state(state)
                raw['scaled_Jacobian_condition'] = float(numerical.linalg.cond(derivative / scales[:, None]))
            arrays = {'state': state, 'seed_state': seed_state, 'mass_coefficients': mass_coeff, 'pi_coefficients': pi_coeff, 'fixed_lapse': model.fixed_lapse, 'configuration': configuration, 'boundary_velocity': model.boundary_velocity, 'constraint': constraint, 'row_scales': scales, 'mass_field': model.mass_q, 'seed_mass_field': seed_mass_q, 'pi_field': model.pi, 'seed_pi_field': seed_pi, 'bulk_strong_density': density}
            arrays.update({name: value for name, value in result.items() if isinstance(value, numerical.ndarray)})
            output = destination / (label + '.npz')
            numerical.savez_compressed(output, **arrays)
            with numerical.load(output) as archive:
                check(label + '_archive_roundtrip', set(archive.files) == set(arrays) and all(numerical.array_equal(archive[name], value) for name, value in arrays.items()))
            artifact(output)
            report['samples'].append(raw)
            save()
            print(json.dumps(raw), flush=True)
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
    print('Complete: ' + str(sum(item['status'] == 'converged' for item in report['samples'])) + '/' + str(len(report['samples'])) + ' converged cases', flush=True)


if __name__ == '__main__':
    run()
