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
    from annular_adm_mixed_action_20260909 import MixedActionBasis, hermite_matrices
    from annular_local_ward_identity_20260909 import LocalWardIdentity
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature, CachedMetricLinkRouthian
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260909'
    destination = intake / 'annular-released-Hermite-initial-derived'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': {}, 'outputs': {}, 'checks': [], 'samples': [], 'valid_for_physics_claim': False, 'scope': 'Release s=hI and its conjugate momentum in the existing lifted scalar action, check the enlarged Legendre map, solve initial constraints, and test all shift rows and lifting Euler equations. Shared p_s is computed from the old GR root and physical reference I_t, not fitted to shift residuals.'}
    (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

    def own(path):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        report['inputs'][str(path.relative_to(root))] = digest
        return digest

    def maximum(value):
        return float(numerical.max(numerical.abs(value)))

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        save()
        print(name + ': ' + str(bool(passed)), flush=True)

    class ReleasedWard(LocalWardIdentity):
        def connection_transport(self):
            packed, system = self.arrays['corrected'], self.system
            return system.links.matrix(packed[system.slices[0]], packed[system.slices[1]], system.constants)

    save()
    try:
        prior_path = intake / 'annular-metric-dynamics-final-integrity.json'
        own(prior_path)
        prior = json.loads(prior_path.read_text())
        check('previous_dynamics_complete', prior['state'] == 'complete' and prior['owner_check_count'] == 330)
        check('previous_sources_and_outputs_unchanged', all(own(root / path) == digest for path, digest in {**prior['inputs'], **prior['outputs']}.items()))
        for name in ['annular_released_hermite_action_20260909.py', 'derive_annular_released_hermite_20260909.py']:
            path = root / 'scripts' / name
            own(path)
            compile(path.read_bytes(), str(path), 'exec')
        for case_name in ['canonical', 'nonlinear_modulated']:
            case_path = intake / 'annular-constraint-correction-initial' / (case_name + '.json')
            own(case_path)
            case = json.loads(case_path.read_text())
            constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
            kappa = float(symbolic.sympify(case['normalization_kappa']))
            for intervals in [16, 32, 64]:
                tag = case_name + '_N' + str(intervals)
                report['active_job'] = tag
                save()
                sources = {}
                for branch, label in [('GR', 'GR'), ('metric_Gram', 'Gram')]:
                    path = intake / 'annular-constraint-routhian-derived' / (tag + '_' + label + '.npz')
                    own(path)
                    with numerical.load(path) as loaded:
                        sources[branch] = {name: loaded[name].copy() for name in loaded.files}
                reference = sources['GR']
                basis = MixedActionBasis(reference['radius'])
                links = MetricLinkQuadrature(basis)
                slope = basis.spacing * reference['defect']
                slope_speed = basis.spacing * reference['defect_time']
                zero_momentum = numerical.zeros(basis.radii.size)
                provisional = ReleasedHermiteRouthian(basis, reference['scalar'], slope, constants, kappa, reference['momentum'], zero_momentum, reference['outer_clock'][0], links)
                reference_packed = numerical.concatenate([reference['corrected'], slope_speed])
                slope_momentum = provisional.slope_canonical_momentum(reference_packed)
                shared = ['radius', 'faces', 'scalar', 'momentum', 'defect', 'defect_time', 'endpoint_acceleration', 'outer_clock']
                check(tag + '_shared_phase_boundary_and_reference_data', all(numerical.array_equal(reference[name], sources['metric_Gram'][name]) for name in shared))
                endpoint_value, unused_gradient, endpoint_lift, unused_lift_gradient = hermite_matrices(basis.radii, basis.radii[[0, -1]], basis.derivative)
                expected_value = numerical.eye(basis.radii.size)[[0, -1]]
                check(tag + '_released_slopes_preserve_Dirichlet_value_trace', maximum(endpoint_value - expected_value) == 0 and maximum(endpoint_lift) == 0)
                scaling = provisional.scaling(reference_packed)
                for branch in ['GR', 'metric_Gram']:
                    source = sources[branch]
                    include_gram = branch != 'GR'
                    name = tag + '_' + branch
                    system = ReleasedHermiteRouthian(basis, source['scalar'], slope, constants, kappa, source['momentum'], slope_momentum, source['outer_clock'][0], links)
                    seed = numerical.concatenate([source['corrected'], slope_speed])
                    value, gradient, hessian = system.evaluate(seed, include_gram)
                    legacy = CachedMetricLinkRouthian(basis, source['scalar'], source['defect'], source['defect_time'], constants, kappa, source['momentum'], source['outer_clock'][0], links=links)
                    old_value, old_gradient, old_hessian = legacy.evaluate(source['corrected'], include_gram)
                    old_count = legacy.count
                    check(name + '_same_action_when_slope_history_held', abs(value + numerical.dot(slope_momentum, slope_speed) - old_value) < 2e-12 and maximum(gradient[:old_count] - old_gradient) < 2e-11 and maximum(hessian[:old_count, :old_count] - old_hessian) < 2e-10)
                    check(name + '_independent_full_ADM_action_value', abs(value - system.independent_action(seed, include_gram)) < 2e-12)
                    rng = numerical.random.default_rng(20260909 + intervals)
                    direction = 0.003 * rng.normal(size=system.count)
                    step = 1e-25
                    directional = system.independent_action(seed + 1j * step * direction, include_gram).imag / step
                    check(name + '_independent_action_gradient', abs(directional - numerical.dot(gradient, direction)) < 5e-12)
                    differentiated = system.evaluate(seed + 1j * step * direction, include_gram, hessian=False)[1].imag / step
                    check(name + '_full_Hessian_directional_derivative', maximum(differentiated - hessian @ direction) < 2e-10)
                    slope_direction = 0.002 * rng.normal(size=basis.radii.size)
                    changed = ReleasedHermiteRouthian(basis, source['scalar'], slope + 1j * step * slope_direction, constants, kappa, source['momentum'], slope_momentum, source['outer_clock'][0], links)
                    slope_variation = changed.independent_action(seed, include_gram).imag / step
                    check(name + '_slope_force_from_independent_action', abs(slope_variation - numerical.dot(system.slope_force(seed, include_gram), slope_direction)) < 2e-12)
                    check(name + '_slope_momentum_from_independent_formula', maximum(gradient[system.slope_slice] + slope_momentum - system.slope_canonical_momentum(seed)) < 2e-14)
                    bare_matrix = system.kinetic_matrix(seed, False)
                    matrix = system.kinetic_matrix(seed, include_gram)
                    indices = system.velocity_indices
                    check(name + '_enlarged_Legendre_matches_action_Hessian', maximum(matrix - hessian[numerical.ix_(indices, indices)]) < 1e-12)
                    eigenvalues = numerical.linalg.eigvalsh(matrix)
                    bare_factor = numerical.linalg.cholesky(bare_matrix)
                    normalized = numerical.linalg.solve(bare_factor, bare_matrix - matrix)
                    normalized = numerical.linalg.solve(bare_factor, normalized.T).T
                    relative_correction = maximum(numerical.linalg.eigvalsh(normalized))
                    check(name + '_full_kinetic_positive_and_correction_bounded', eigenvalues[0] > 0 and relative_correction < 1, {'minimum_eigenvalue': float(eigenvalues[0]), 'condition': float(eigenvalues[-1] / eigenvalues[0]), 'relative_operator_correction': relative_correction})
                    if case_name == 'canonical':
                        check(name + '_canonical_kinetic_correction_exact_zero', numerical.array_equal(matrix, bare_matrix))
                    corrected, history, solved, reason = system.solve(seed, include_gram, scaling)
                    check(name + '_enlarged_initial_constraints_solved', solved, {'history': history, 'reason': reason})
                    if not solved:
                        raise RuntimeError('No further continuation of an unsolved initial state: ' + name)
                    if branch == 'GR':
                        check(name + '_GR_reference_root_preserved', maximum(corrected - reference_packed) < 2e-11)
                    value, gradient, hessian = system.evaluate(corrected, include_gram)
                    tangent = system.constraint_tangent(corrected, include_gram, source['endpoint_acceleration'], source['outer_clock'][1])
                    check(name + '_all_free_constraint_rates_solved', maximum(tangent['constraint_derivative_residual']) < 2e-11)
                    changed = ReleasedHermiteRouthian(basis, source['scalar'] + 1j * step * corrected[system.slices[2]], slope + 1j * step * corrected[system.slope_slice], constants, kappa, source['momentum'], slope_momentum, source['outer_clock'][0], links)
                    slope_momentum_time = changed.slope_canonical_momentum(corrected + 1j * step * tangent['packed_speed']).imag / step
                    slope_euler = system.slope_force(corrected, include_gram) - slope_momentum_time
                    check(name + '_independent_slope_Euler_equation_solved', maximum(slope_euler) < 2e-11, maximum(slope_euler))
                    arrays = dict(source, scalar=system.scalar, corrected=corrected, slope=slope, slope_momentum=slope_momentum, defect=system.defect, defect_time=corrected[system.slope_slice] / basis.spacing, defect_acceleration=tangent['packed_speed'][system.slope_slice] / basis.spacing, gradient_final=gradient, Hessian_final=hessian, **tangent)
                    ward = ReleasedWard(system, arrays).evaluate(include_gram)
                    check(name + '_released_full_Ward_identity', maximum(ward['identity_error']) < 2e-11, maximum(ward['identity_error']))
                    check(name + '_independent_Ward_lifting_Euler_matches_released_equation', maximum(ward['lifting_euler'] - basis.spacing * slope_euler) < 2e-11)
                    old_tangent = legacy.constraint_tangent(source['corrected'], include_gram, source['defect_acceleration'], source['endpoint_acceleration'], source['outer_clock'][1])
                    old_mismatch = maximum(old_tangent['packed_speed'][legacy.slices[0]] - old_tangent['shift_mass_speed'])
                    new_mismatch = maximum(tangent['packed_speed'][system.slices[0]] - tangent['shift_mass_speed'])
                    if intervals == 16:
                        for amplitude in [0.0001, 0.00005]:
                            neighbors = []
                            for sign in [-1, 1]:
                                delta = sign * amplitude
                                neighboring = ReleasedHermiteRouthian(basis, system.scalar + delta * corrected[system.slices[2]], slope + delta * corrected[system.slope_slice], constants, kappa, system.momentum + delta * tangent['momentum_speed'], slope_momentum + delta * tangent['slope_momentum_speed'], system.outer_clock + delta * source['outer_clock'][1], links)
                                neighboring_seed = corrected + delta * tangent['packed_speed']
                                neighboring_root, unused_history, success, unused_reason = neighboring.solve(neighboring_seed, include_gram, scaling)
                                if not success:
                                    raise RuntimeError('Neighboring nonlinear root failed.')
                                neighbors.append(neighboring_root)
                            numerical_rate = (neighbors[1] - neighbors[0]) / (2 * amplitude)
                            check(name + '_nonlinear_root_family_tangent_' + str(amplitude), maximum(numerical_rate - tangent['packed_speed']) < 2e-7, maximum(numerical_rate - tangent['packed_speed']))
                    artifact = destination / (name + '.npz')
                    numerical.savez_compressed(artifact, radius=basis.radii, faces=basis.faces, scalar=system.scalar, slope=slope, momentum=system.momentum, slope_momentum=slope_momentum, corrected=corrected, seed=seed, shared_reference_packed=reference_packed, free=system.free, fixed=system.fixed, slope_slice_bounds=numerical.array([system.slope_slice.start, system.slope_slice.stop]), row_scale=scaling[1], unknown_scale=scaling[0], outer_clock=source['outer_clock'], endpoint_acceleration=source['endpoint_acceleration'], gradient_final=gradient, Hessian_final=hessian, kinetic_matrix=system.kinetic_matrix(corrected, include_gram), slope_Euler=slope_euler, **tangent, **{'Ward_' + key: item for key, item in ward.items()})
                    report['outputs'][str(artifact.relative_to(root))] = hashlib.sha256(artifact.read_bytes()).hexdigest()
                    report['samples'].append({'case': case_name, 'intervals': intervals, 'branch': branch, 'scalar_degrees': int(2 * basis.radii.size), 'free_scalar_velocities': int(system.free_velocity_indices.size), 'minimum_enlarged_kinetic_eigenvalue_at_seed': float(eigenvalues[0]), 'relative_kinetic_correction_at_seed': relative_correction, 'initial_root_residual': maximum(gradient[system.free]), 'root_iterations': len(history) - 1, 'root_displacement_max': maximum(corrected - seed), 'slope_Euler_max': maximum(slope_euler), 'raw_I_Euler_max': maximum(ward['lifting_euler']), 'I_tt_released_max': maximum(arrays['defect_acceleration']), 'I_tt_departure_from_prescribed_max': maximum(arrays['defect_acceleration'] - source['defect_acceleration']), 'old_prescribed_mass_rate_mismatch': old_mismatch, 'released_mass_rate_mismatch': new_mismatch, 'released_shift_residual': maximum(tangent['shift_residual']), 'Ward_error': maximum(ward['identity_error']), 'all_shift_rows_closed': False, 'full_coupled_DAE_solved': False})
                    save()
        for module in tuple(sys.modules.values()):
            filename = getattr(module, '__file__', None)
            if filename:
                path = Path(filename).resolve()
                if path.parent == root / 'scripts' and path.suffix == '.py':
                    own(path)
        check('all_owned_sources_unchanged', all(hashlib.sha256((root / path).read_bytes()).hexdigest() == digest for path, digest in report['inputs'].items()))
        check('no_bytecode_cache', not (root / 'scripts/__pycache__').exists())
        report.update(passed=sum(row['passed'] for row in report['checks']), total=len(report['checks']), completed_utc=datetime.now(timezone.utc).isoformat())
        report['state'] = 'complete' if report['passed'] == report['total'] else 'failed'
        save()
        if report['state'] == 'complete':
            (destination / 'COMPLETE').write_text(report['completed_utc'] + '\n')
        print(json.dumps({key: report[key] for key in ['state', 'passed', 'total', 'completed_utc']}), flush=True)
        if report['state'] != 'complete':
            raise SystemExit(1)
    except Exception as error:
        report.update(state='failed', failure=repr(error), traceback=traceback.format_exc(), completed_utc=datetime.now(timezone.utc).isoformat())
        save()
        raise


if __name__ == '__main__':
    run()
