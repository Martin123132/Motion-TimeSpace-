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
    from annular_action_boundary_current_20260909 import boundary_balance, gram_current

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260909'
    destination = intake / 'annular-boundary-N64-evolution-smoke'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': {}, 'outputs': {}, 'checks': [], 'samples': [], 'valid_for_physics_claim': False, 'full_coupled_DAE_solved': False, 'scope': 'Unmodified released-Hermite evolution at N64 with matched GR/candidate external data. Boundary currents are diagnostics only: no endpoint offset subtraction, no new boundary equation, no root reprojection or damping.'}
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

    class CurrentWard(LocalWardIdentity):
        def connection_transport(self):
            packed, system = self.arrays['corrected'], self.system
            return system.links.matrix(packed[system.slices[0]], packed[system.slices[1]], system.constants)

    save()
    try:
        own(Path(__file__))
        gate_path = intake / 'annular-action-boundary-current-derived/status.json'
        own(gate_path)
        gate = json.loads(gate_path.read_text())
        check('boundary_derivation_gate_complete', gate['state'] == 'complete' and gate['passed'] == gate['total'])
        check('all_boundary_sources_and_results_unchanged', all(own(root / path) == digest for path, digest in {**gate['inputs'], **gate['outputs']}.items()))
        if not all(row['passed'] for row in report['checks']):
            raise RuntimeError('Source/derivation gate failed.')
        endpoints = {}
        for case_name in ['canonical', 'nonlinear_modulated']:
            case_path = intake / 'annular-constraint-correction-initial' / (case_name + '.json')
            own(case_path)
            case = json.loads(case_path.read_text())
            constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
            kappa = float(symbolic.sympify(case['normalization_kappa']))
            shared = {}
            for branch in ['GR', 'metric_Gram']:
                tag = case_name + '_N64_' + branch
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
                        raise RuntimeError('Kinetic/metric chart gate: ' + repr(health))
                    tangent = system.constraint_tangent(packed, include_gram, source['endpoint_acceleration'], source['outer_clock'][1])
                    derivative = numerical.concatenate([packed[system.slices[2]], packed[system.slope_slice], tangent['momentum_speed'], tangent['slope_momentum_speed'], tangent['packed_speed']])
                    if not numerical.all(numerical.isfinite(derivative)):
                        raise RuntimeError('Nonfinite derivative.')
                    if not diagnostic:
                        return derivative
                    balance = boundary_balance(system, packed, tangent, include_gram, source['outer_clock'][1])
                    unused_value, gradient, hessian = system.evaluate(packed, include_gram)
                    mismatch = tangent['packed_speed'][system.slices[0]] - tangent['shift_mass_speed']
                    detail = {'time': float(time), 'constraint_max': maximum(balance['free_constraint']), 'constraint_derivative_max': maximum(balance['free_constraint_rate']), 'mass_rate_mismatch_max': maximum(mismatch), 'shift_residual_max': maximum(tangent['shift_residual']), 'slope_Euler_max': maximum(balance['slope_Euler']), 'boundary_offset_max': maximum(balance['local_boundary_balance']), 'boundary_identity_error': maximum(balance['global_boundary_identity_error']), 'energy_identity_error': maximum(balance['full_energy_work_identity_error']), **health}
                    arrays = dict(source, scalar=scalar, slope=slope, momentum=momentum, slope_momentum=slope_momentum, corrected=packed, defect=slope / basis.spacing, defect_time=packed[system.slope_slice] / basis.spacing, defect_acceleration=tangent['packed_speed'][system.slope_slice] / basis.spacing, gradient_final=gradient, Hessian_final=hessian, **tangent)
                    return derivative, detail, balance, mismatch, system, arrays

                initial_data = rhs(0, initial, True)
                check(tag + '_same_initial_derivative_as_owned_root', maximum(initial_data[0][4 * node_count:] - source['packed_speed']) < 2e-12)
                for steps in [16, 32, 64]:
                    report['active_job'] = tag + '_steps' + str(steps)
                    save()
                    state = initial.copy()
                    step = 0.01 / steps
                    records = {key: [] for key in ['time', 'state', 'constraints', 'shifts', 'mass_rate_mismatch', 'slope_Euler', 'boundary_offset', 'boundary_flux', 'boundary_clocks', 'global_boundary_remainder']}
                    details, failure = [], None
                    try:
                        for index in range(steps + 1):
                            time = index * step
                            first, detail, balance, mismatch, system, arrays = rhs(time, state, True)
                            for key, value in [('time', time), ('state', state.copy()), ('constraints', balance['free_constraint']), ('shifts', arrays['shift_residual']), ('mass_rate_mismatch', mismatch), ('slope_Euler', balance['slope_Euler']), ('boundary_offset', balance['local_boundary_balance']), ('boundary_flux', balance['reaction_flux_positive_R']), ('boundary_clocks', balance['variational_boundary_clocks']), ('global_boundary_remainder', balance['global_boundary_remainder'])]:
                                records[key].append(value)
                            details.append(detail)
                            if steps == 64 and index in [0, 32, 64]:
                                ward = CurrentWard(system, arrays).evaluate(include_gram)
                                check(tag + '_full_evolved_Ward_sample' + str(index), maximum(ward['identity_error']) < 2e-11 and maximum(ward['lifting_euler'] - basis.spacing * balance['slope_Euler']) < 2e-11)
                                current = gram_current(system, arrays['corrected'], arrays) if include_gram else {}
                                if include_gram:
                                    check(tag + '_full_evolved_cut_current_sample' + str(index), maximum(current['cut_shift_covector'] - current['endpoint_shift_covector']) < 1e-13 and maximum(current['Gram_boundary_reaction_flux'] - current['Gram_boundary_link_flux'] - current['Gram_boundary_coefficient_flux']) < 1e-14)
                                target = destination / (tag + '_sample' + str(index) + '.npz')
                                numerical.savez_compressed(target, **{'Ward_' + name: value for name, value in ward.items()}, **{'boundary_' + name: value for name, value in balance.items()}, **{'current_' + name: value for name, value in current.items()})
                                artifact(target)
                            if index < steps:
                                second = rhs(time + step / 2, state + step * first / 2)
                                third = rhs(time + step / 2, state + step * second / 2)
                                fourth = rhs(time + step, state + step * third)
                                state = state + step * (first + 2 * second + 2 * third + fourth) / 6
                    except Exception as error:
                        failure = {'error': repr(error), 'traceback': traceback.format_exc(), 'completed_steps': len(details) - 1}
                    target = destination / (tag + '_steps' + str(steps) + '.npz')
                    numerical.savez_compressed(target, **{name: numerical.asarray(value) for name, value in records.items()}, radius=basis.radii, faces=basis.faces)
                    artifact(target)
                    detail_path = destination / (tag + '_steps' + str(steps) + '.json')
                    detail_path.write_text(json.dumps({'samples': details, 'failure': failure}, indent=2) + '\n')
                    artifact(detail_path)
                    check(tag + '_steps' + str(steps) + '_complete_finite_trajectory', failure is None and len(details) == steps + 1, failure)
                    if failure is not None:
                        report['samples'].append({'case': case_name, 'branch': branch, 'steps': steps, 'state': 'failed', 'failure': failure})
                        save()
                        continue
                    check(tag + '_steps' + str(steps) + '_all_faces_and_endpoint_offsets_saved', numerical.asarray(records['shifts']).shape == (steps + 1, basis.faces.size) and numerical.asarray(records['boundary_offset']).shape == (steps + 1, 2))
                    check(tag + '_steps' + str(steps) + '_full_boundary_work_identity', max(row['boundary_identity_error'] for row in details) < 2e-11 and max(row['energy_identity_error'] for row in details) < 2e-11)
                    check(tag + '_steps' + str(steps) + '_released_slope_equation', max(row['slope_Euler_max'] for row in details) < 2e-11)
                    expected = source['scalar'][[0, -1]] + 0.01 * source['corrected'][system.slices[2]][[0, -1]] + 0.01**2 * source['endpoint_acceleration'] / 2
                    check(tag + '_steps' + str(steps) + '_unchanged_scalar_boundary_history', maximum(state[:node_count][[0, -1]] - expected) < 1e-13)
                    drift = maximum(numerical.asarray(records['constraints']) - initial_data[2]['free_constraint'])
                    report['samples'].append({'case': case_name, 'intervals': 64, 'branch': branch, 'steps': steps, 'state': 'complete', 'maximum_constraint_drift': drift, 'maximum_constraint_residual': max(row['constraint_max'] for row in details), 'maximum_mass_rate_mismatch': max(row['mass_rate_mismatch_max'] for row in details), 'maximum_shift_residual': max(row['shift_residual_max'] for row in details), 'maximum_boundary_offset': max(row['boundary_offset_max'] for row in details), 'maximum_boundary_identity_error': max(row['boundary_identity_error'] for row in details), 'maximum_energy_identity_error': max(row['energy_identity_error'] for row in details), 'minimum_full_kinetic_eigenvalue': min(row['minimum_full_scalar_Legendre_eigenvalue'] for row in details), 'final_boundary_offset': records['boundary_offset'][-1].tolist(), 'end_mass_rate_mismatch': details[-1]['mass_rate_mismatch_max'], 'full_shift_equations_solved': False})
                    endpoints[case_name, branch, steps] = state.copy()
                    save()
                    print(tag + ' steps=' + str(steps) + ' mass=' + str(report['samples'][-1]['maximum_mass_rate_mismatch']) + ' shift=' + str(report['samples'][-1]['maximum_shift_residual']), flush=True)
                if all((case_name, branch, steps) in endpoints for steps in [16, 32, 64]):
                    coarse = maximum(endpoints[case_name, branch, 16] - endpoints[case_name, branch, 32])
                    fine = maximum(endpoints[case_name, branch, 32] - endpoints[case_name, branch, 64])
                    check(tag + '_time_refinement_or_roundoff', fine < 0.5 * coarse or max(coarse, fine) < 5e-12, {'coarse_difference': coarse, 'fine_difference': fine, 'ratio': coarse / fine if fine else None})
            fields = ['scalar', 'slope', 'momentum', 'slope_momentum', 'outer_clock', 'endpoint_acceleration']
            check(case_name + '_same_GR_and_candidate_phase_data', all(numerical.array_equal(shared['GR'][field], shared['metric_Gram'][field]) for field in fields))
        report['spatial_comparisons'] = []
        for case_name in ['canonical', 'nonlinear_modulated']:
            for branch in ['GR', 'metric_Gram']:
                if (case_name, branch, 64) not in endpoints:
                    continue
                samples = {}
                for intervals in [16, 32, 64]:
                    folder = destination if intervals == 64 else intake / 'annular-released-Hermite-evolution-smoke'
                    steps = 64 if intervals == 64 else 32
                    path = folder / (case_name + '_N' + str(intervals) + '_' + branch + '_steps' + str(steps) + '.npz')
                    if intervals != 64:
                        own(path)
                    with numerical.load(path) as loaded:
                        stride = 2 if intervals == 64 else 1
                        samples[intervals] = {'mass': maximum(loaded['mass_rate_mismatch'][::stride]), 'shift': maximum(loaded['shifts'][::stride])}
                record = {'case': case_name, 'branch': branch, 'same_33_coordinate_times': True, 'data': samples, 'mass_refinement_32_to_64': samples[32]['mass'] / samples[64]['mass'], 'shift_refinement_32_to_64': samples[32]['shift'] / samples[64]['shift']}
                report['spatial_comparisons'].append(record)
        for module in tuple(sys.modules.values()):
            filename = getattr(module, '__file__', None)
            if filename:
                path = Path(filename).resolve()
                if path.parent == root / 'scripts' and path.suffix == '.py':
                    own(path)
        check('all_owned_sources_unchanged', all(hashlib.sha256((root / name).read_bytes()).hexdigest() == digest for name, digest in report['inputs'].items()))
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
