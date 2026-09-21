import hashlib
import json
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

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260911'
    destination = intake / 'annular-canonical-inverse-boundary-control-attempt01'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'inputs': {}, 'outputs': {}, 'checks': [], 'samples': [], 'valid_for_physics_claim': False, 'new_evolution': False}

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = digest(path)

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

    def archive(path):
        own(path)
        with numerical.load(path, allow_pickle=False) as saved:
            return {name: saved[name].copy() for name in saved.files}

    save()
    try:
        compile(Path(__file__).read_bytes(), __file__, 'exec')
        own(Path(__file__))
        snapshot = destination / ('executed-' + Path(__file__).name)
        snapshot.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        directory = intake / 'annular-canonical-inverse-boundary-attempt01'
        status_path = directory / 'status.json'
        own(status_path)
        status = json.loads(status_path.read_text())
        check('paired_attempt_complete', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
        parameter_path = root / 'source-intake/navier-stokes/20260909/annular-constraint-correction-initial/canonical.json'
        own(parameter_path)
        constants = {name: float(symbolic.sympify(value)) for name, value in json.loads(parameter_path.read_text())['parameters'].items()}
        for sample in status['samples']:
            label = sample['label']
            saved = archive(directory / (label + '.npz'))
            source = archive(root / 'source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02' / ('canonical_N16_' + sample['branch'] + '_sample0.npz'))
            basis = MixedActionBasis(source['basis_radii'])
            count = basis.radii.size
            configuration, momenta = source['original_configuration'], source['original_momenta']
            packed = (source['initial_root_box_lower'] + source['initial_root_box_upper']) / 2
            system = ReleasedHermiteRouthian(basis, configuration[:count], configuration[count:], constants, .1, momenta[:count], momenta[count:], source['affine_clock'][0], MetricLinkQuadrature(basis))
            model = InverseBoundaryInitialData(system, packed, configuration, sample['branch'] != 'GR', saved['boundary_velocity'].copy(), normalize_clock=sample['normalize_clock'])
            model.pi_coeff_seed = saved['pi_coefficients'].copy()
            state = saved['state'].copy()
            residual = model.data_residual(state)
            check(label + '_stored_residual_reproduced', abs(residual - saved['full_residual']).max() < 1e-14)
            old_boundary = model.boundary_velocity.copy()
            model.boundary_velocity[1] += .25
            check(label + '_old_inner_scalar_drive_really_released', numerical.array_equal(model.data_residual(state), residual))
            model.boundary_velocity = old_boundary.copy()
            model.boundary_velocity[0] += 1e-6
            expected_change = numerical.zeros_like(state)
            expected_change[-3] = -1e-6
            expected_change[-2] = -1e-6 / model.bulk_trace_coefficient
            check(label + '_mass_drive_owns_exactly_two_boundary_relations', abs(model.data_residual(state) - residual - expected_change).max() < 1e-13)
            model.boundary_velocity = old_boundary.copy()
            model.boundary_velocity[2] += 1e-6
            expected_change = numerical.zeros_like(state)
            expected_change[-1] = -1e-6
            check(label + '_outer_scalar_drive_not_released', abs(model.data_residual(state) - residual - expected_change).max() < 1e-13)
            model.boundary_velocity = old_boundary
            reduction = InverseBoundaryMassReduction(model)
            reduced, tangent, unused_mass = reduction.reduced_jacobian(state)
            direction = numerical.sin(numerical.arange(count + 3) + .7) * numerical.maximum(abs(state[count:]), .001)
            step = 1e-5
            plus, unused_plus = reduction.project(state + step * (tangent @ direction))
            minus, unused_minus = reduction.project(state - step * (tangent @ direction))
            finite = (model.data_residual(plus)[count:] - model.data_residual(minus)[count:]) / (2 * step)
            error = float(abs(finite - reduced @ direction).max() / max(1., float(abs(reduced @ direction).max())))
            check(label + '_final_state_projected_derivative', error < 1e-7, error)
            clock_omission_error = None
            if model.normalize_clock:
                model.set_state(state)
                original_profile = model.original_lapse.copy()
                model.original_lapse = model.fixed_lapse.copy()
                model.normalize_clock = False
                omitted, unused_tangent, unused_mass = reduction.reduced_jacobian(state)
                model.normalize_clock = True
                model.original_lapse = original_profile
                model.set_state(state)
                clock_omission_error = float(abs(reduced - omitted).max())
                check(label + '_omitted_clock_response_detected', clock_omission_error > 1e-12, clock_omission_error)
            evaluation, diagnostic = model.diagnostics(state)
            check(label + '_finite_trace_not_mislabelled_classical', sample['classical_boundary_certified'] is False and max(abs(value) for value in diagnostic['spatial_boundary_reaction_gaps']) > 1e-6)
            replay_distance = None
            if sample['status'] == 'converged':
                disturbed = state + 1e-7 * numerical.cos(numerical.arange(state.size) + .8) * numerical.maximum(abs(state), .001)
                solved = reduction.solve(disturbed, saved['row_scales'], maximum_iterations=12)
                replay_distance = float(abs(solved['state'] - state).max())
                check(label + '_perturbed_root_replay', solved['converged'] and replay_distance < 1e-5, {'failure': solved['failure'], 'distance': replay_distance})
                output = destination / (label + '_replay.npz')
                numerical.savez_compressed(output, state=solved['state'], original_state=state, full_residual=model.data_residual(solved['state']), row_scales=saved['row_scales'])
                own(output, 'outputs')
            report['samples'].append({'label': label, 'directional_error': error, 'clock_response_omission_error': clock_omission_error, 'replay_distance': replay_distance})
            save()
        check('no_python_cache', not (root / 'scripts/__pycache__').exists())
        report['state'] = 'complete'
        save()
        print(json.dumps({'checks': len(report['checks']), 'samples': report['samples']}), flush=True)
    except Exception as error:
        report['state'] = 'failed'
        report['error'] = repr(error)
        save()
        raise


if __name__ == '__main__':
    run()
