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
    from annular_adm_mixed_action_20260909 import MixedActionBasis
    from annular_local_ward_identity_20260909 import LocalWardIdentity
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260909'
    destination = intake / 'annular-released-Hermite-evolution-smoke'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': {}, 'outputs': {}, 'checks': [], 'samples': [], 'valid_for_physics_claim': False, 'full_coupled_DAE_solved': False, 'scope': 'Bounded RK4 evolution of chi,s=hI,pi_chi,p_s,mu,N,q,s_dot with the released scalar Euler equation. No prescribed I history, no damping or root reprojection. Scalar value endpoint accelerations and outer clock history remain prescribed identically for GR and candidate; all shift residuals remain diagnostics.'}
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

    def artifact(path):
        report['outputs'][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    class ReleasedWard(LocalWardIdentity):
        def connection_transport(self):
            packed, system = self.arrays['corrected'], self.system
            return system.links.matrix(packed[system.slices[0]], packed[system.slices[1]], system.constants)

    save()
    try:
        own(Path(__file__))
        gate_path = intake / 'annular-released-Hermite-initial-derived/status.json'
        own(gate_path)
        gate = json.loads(gate_path.read_text())
        check('released_kinetic_and_initial_root_gates_complete', gate['state'] == 'complete' and gate['passed'] == gate['total'])
        check('all_initial_gate_sources_and_results_unchanged', all(own(root / path) == digest for path, digest in {**gate['inputs'], **gate['outputs']}.items()))
        if not all(row['passed'] for row in report['checks']):
            raise RuntimeError('No evolution before kinetic and root gates.')
        endpoints = {}
        for case_name in ['canonical', 'nonlinear_modulated']:
            case_path = intake / 'annular-constraint-correction-initial' / (case_name + '.json')
            own(case_path)
            case = json.loads(case_path.read_text())
            constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
            kappa = float(symbolic.sympify(case['normalization_kappa']))
            for intervals in [16, 32]:
                shared = {}
                for branch in ['GR', 'metric_Gram']:
                    tag = case_name + '_N' + str(intervals) + '_' + branch
                    report['active_job'] = tag
                    save()
                    source_path = intake / 'annular-released-Hermite-initial-derived' / (tag + '.npz')
                    own(source_path)
                    with numerical.load(source_path) as loaded:
                        source = {name: loaded[name].copy() for name in loaded.files}
                    shared[branch] = source
                    basis = MixedActionBasis(source['radius'])
                    links = MetricLinkQuadrature(basis)
                    node_count = basis.radii.size
                    include_gram = branch != 'GR'
                    initial = numerical.concatenate([source['scalar'], source['slope'], source['momentum'], source['slope_momentum'], source['corrected']])

                    def rhs(time, state, diagnostic=False):
                        scalar, slope, momentum, slope_momentum = [state[index * node_count:(index + 1) * node_count] for index in range(4)]
                        packed = state[4 * node_count:]
                        system = ReleasedHermiteRouthian(basis, scalar, slope, constants, kappa, momentum, slope_momentum, source['outer_clock'][0] + time * source['outer_clock'][1], links)
                        valid, health = system.admissible(packed, include_gram)
                        if not valid:
                            raise RuntimeError('Scalar/metric branch gate: ' + repr(health))
                        tangent = system.constraint_tangent(packed, include_gram, source['endpoint_acceleration'], source['outer_clock'][1])
                        scalar_speed, slope_speed = packed[system.slices[2]], packed[system.slope_slice]
                        derivative = numerical.concatenate([scalar_speed, slope_speed, tangent['momentum_speed'], tangent['slope_momentum_speed'], tangent['packed_speed']])
                        if not numerical.all(numerical.isfinite(derivative)):
                            raise RuntimeError('Nonfinite derivative.')
                        if not diagnostic:
                            return derivative
                        unused_value, gradient, hessian = system.evaluate(packed, include_gram)
                        step = 1e-25
                        changed = ReleasedHermiteRouthian(basis, scalar + 1j * step * scalar_speed, slope + 1j * step * slope_speed, constants, kappa, momentum, slope_momentum, system.outer_clock, links)
                        momentum_time = changed.slope_canonical_momentum(packed + 1j * step * tangent['packed_speed']).imag / step
                        slope_euler = tangent['slope_momentum_speed'] - momentum_time
                        mismatch = tangent['packed_speed'][system.slices[0]] - tangent['shift_mass_speed']
                        detail = {'time': float(time), 'constraint_max': maximum(gradient[system.free]), 'constraint_scaled_max': maximum(gradient[system.free] / source['row_scale']), 'constraint_derivative_max': maximum(tangent['constraint_derivative_residual']), 'slope_Euler_max': maximum(slope_euler), 'raw_I_Euler_max': basis.spacing * maximum(slope_euler), 'shift_residual_max': maximum(tangent['shift_residual']), 'mass_rate_mismatch_max': maximum(mismatch), **health}
                        arrays = dict(source, scalar=scalar, slope=slope, momentum=momentum, slope_momentum=slope_momentum, corrected=packed, defect=slope / basis.spacing, defect_time=slope_speed / basis.spacing, defect_acceleration=tangent['packed_speed'][system.slope_slice] / basis.spacing, gradient_final=gradient, Hessian_final=hessian, **tangent)
                        return derivative, detail, gradient[system.free], tangent['shift_residual'], mismatch, slope_euler, gradient[system.fixed], system, arrays

                    initial_rhs = rhs(0, initial, True)
                    check(tag + '_initial_derivative_matches_owned_released_tangent', maximum(initial_rhs[0][4 * node_count:] - source['packed_speed']) < 2e-12)
                    end_time = 0.01
                    for steps in [8, 16, 32]:
                        step = end_time / steps
                        state = initial.copy()
                        records = {'time': [], 'state': [], 'constraints': [], 'shifts': [], 'mass_rate_mismatch': [], 'slope_Euler': [], 'fixed_boundary_reactions': []}
                        details = []
                        failure = None
                        try:
                            for index in range(steps + 1):
                                time = index * step
                                first, detail, constraints, shifts, mismatch, slope_euler, reactions, system, arrays = rhs(time, state, True)
                                for key, value in [('time', time), ('state', state.copy()), ('constraints', constraints), ('shifts', shifts), ('mass_rate_mismatch', mismatch), ('slope_Euler', slope_euler), ('fixed_boundary_reactions', reactions)]:
                                    records[key].append(value)
                                details.append(detail)
                                if steps == 32 and index in [0, 16, 32]:
                                    ward = ReleasedWard(system, arrays).evaluate(include_gram)
                                    check(tag + '_evolved_full_Ward_sample' + str(index), maximum(ward['identity_error']) < 2e-11 and maximum(ward['lifting_euler'] - basis.spacing * slope_euler) < 2e-11, {'Ward_error': maximum(ward['identity_error']), 'lifting_Euler': maximum(ward['lifting_euler'])})
                                    target = destination / (tag + '_Ward' + str(index) + '.npz')
                                    numerical.savez_compressed(target, **ward)
                                    artifact(target)
                                if index < steps:
                                    second = rhs(time + step / 2, state + step * first / 2)
                                    third = rhs(time + step / 2, state + step * second / 2)
                                    fourth = rhs(time + step, state + step * third)
                                    state = state + step * (first + 2 * second + 2 * third + fourth) / 6
                        except Exception as error:
                            failure = {'error': repr(error), 'traceback': traceback.format_exc(), 'completed_steps': len(details) - 1}
                        target = destination / (tag + '_steps' + str(steps) + '.npz')
                        numerical.savez_compressed(target, **{key: numerical.asarray(value) for key, value in records.items()}, radius=basis.radii, faces=basis.faces)
                        artifact(target)
                        detail_path = destination / (tag + '_steps' + str(steps) + '.json')
                        detail_path.write_text(json.dumps({'samples': details, 'failure': failure}, indent=2) + '\n')
                        artifact(detail_path)
                        check(tag + '_steps' + str(steps) + '_finite_full_trajectory', failure is None and len(details) == steps + 1, failure)
                        if failure is not None:
                            report['samples'].append({'case': case_name, 'intervals': intervals, 'branch': branch, 'steps': steps, 'state': 'failed', 'failure': failure})
                            save()
                            continue
                        check(tag + '_steps' + str(steps) + '_all_shift_and_slope_rows_retained', numerical.asarray(records['shifts']).shape == (steps + 1, basis.faces.size) and numerical.asarray(records['slope_Euler']).shape == (steps + 1, node_count))
                        check(tag + '_steps' + str(steps) + '_slope_Euler_equations_satisfied', max(row['slope_Euler_max'] for row in details) < 2e-11)
                        expected_endpoints = source['scalar'][[0, -1]] + end_time * source['corrected'][system.slices[2]][[0, -1]] + end_time**2 * source['endpoint_acceleration'] / 2
                        check(tag + '_steps' + str(steps) + '_same_prescribed_value_boundaries', maximum(state[:node_count][[0, -1]] - expected_endpoints) < 1e-13)
                        drift = maximum(numerical.asarray(records['constraints']) - initial_rhs[2])
                        report['samples'].append({'case': case_name, 'intervals': intervals, 'branch': branch, 'steps': steps, 'state': 'complete', 'end_time': end_time, 'maximum_constraint_drift': drift, 'maximum_constraint_residual': max(row['constraint_max'] for row in details), 'maximum_shift_residual': max(row['shift_residual_max'] for row in details), 'maximum_mass_rate_mismatch': max(row['mass_rate_mismatch_max'] for row in details), 'end_mass_rate_mismatch': details[-1]['mass_rate_mismatch_max'], 'maximum_slope_Euler': max(row['slope_Euler_max'] for row in details), 'maximum_raw_I_Euler': max(row['raw_I_Euler_max'] for row in details), 'minimum_full_scalar_Legendre_eigenvalue': min(row['minimum_full_scalar_Legendre_eigenvalue'] for row in details), 'maximum_scalar_Legendre_condition': max(row['scalar_Legendre_condition'] for row in details), 'slope_position_change_max': maximum(state[node_count:2 * node_count] - initial[node_count:2 * node_count]), 'state_change_max': maximum(state - initial), 'full_shift_equations_solved': False})
                        endpoints[case_name, intervals, branch, steps] = state.copy()
                        save()
                        print(tag + ' steps=' + str(steps) + ' drift=' + str(drift) + ' mismatch=' + str(details[-1]['mass_rate_mismatch_max']), flush=True)
                    if all((case_name, intervals, branch, steps) in endpoints for steps in [8, 16, 32]):
                        coarse = maximum(endpoints[case_name, intervals, branch, 8] - endpoints[case_name, intervals, branch, 16])
                        fine = maximum(endpoints[case_name, intervals, branch, 16] - endpoints[case_name, intervals, branch, 32])
                        check(tag + '_time_refinement_or_roundoff', fine < 0.5 * coarse or max(coarse, fine) < 5e-12, {'coarse_difference': coarse, 'fine_difference': fine, 'ratio': coarse / fine if fine else None})
                fields = ['scalar', 'slope', 'momentum', 'slope_momentum', 'outer_clock', 'endpoint_acceleration']
                check(case_name + '_N' + str(intervals) + '_same_shared_released_phase_data', all(numerical.array_equal(shared['GR'][field], shared['metric_Gram'][field]) for field in fields))
        report['comparisons'] = []
        previous_path = intake / 'annular-metric-evolution-smoke/status.json'
        own(previous_path)
        previous = json.loads(previous_path.read_text())
        for row in report['samples']:
            if row['state'] != 'complete' or row['steps'] != 32:
                continue
            old = next(item for item in previous['samples'] if item['case'] == row['case'] and item['intervals'] == row['intervals'] and item['branch'] == row['branch'] and item['steps'] == 16)
            new_at16 = next(item for item in report['samples'] if item['case'] == row['case'] and item['intervals'] == row['intervals'] and item['branch'] == row['branch'] and item['steps'] == 16 and item['state'] == 'complete')
            report['comparisons'].append({'case': row['case'], 'intervals': row['intervals'], 'branch': row['branch'], 'old_prescribed_mass_mismatch_steps16': old['maximum_mass_rate_mismatch'], 'new_released_mass_mismatch_steps16': new_at16['maximum_mass_rate_mismatch'], 'new_released_mass_mismatch_steps32': row['maximum_mass_rate_mismatch'], 'released_to_prescribed_ratio_same_steps16': new_at16['maximum_mass_rate_mismatch'] / old['maximum_mass_rate_mismatch'], 'same_boundary_value_and_clock_history': True, 'new_phase_space_and_canonical_slope_data_disclosed': True})
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
