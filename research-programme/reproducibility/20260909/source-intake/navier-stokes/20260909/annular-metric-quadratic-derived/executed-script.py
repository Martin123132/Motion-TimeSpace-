import argparse
import hashlib
import json
import os
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from annular_adm_mixed_action_20260909 import MixedActionBasis, coefficient_jets, real_linear
    from annular_constraint_routhian_20260909 import ConstraintRouthian
    from annular_metric_link_quadratic_20260909 import CachedMetricLinkRouthian, MetricLinkQuadrature, MetricQuadraticPath

    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['quadratic', 'evolution'])
    parser.add_argument('--name', required=True)
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260909'
    destination = intake / arguments.name
    if destination.parent != intake or not arguments.name.startswith('annular-metric-'):
        raise ValueError('Output must be a named direct child of the intake.')
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'phase': arguments.phase, 'started_utc': datetime.now(timezone.utc).isoformat(), 'pid': os.getpid(), 'inputs': {}, 'outputs': {}, 'checks': [], 'samples': [], 'valid_for_physics_claim': False, 'full_coupled_DAE_solved': False, 'scope': 'Metric-reconstructed link quadratic action and bounded unprojected constraint-tangent ODE, NOT an exact solution of all shift equations. Prescribed lifting and boundary jets are kept; all unsatisfied shift rows are recorded. GR and candidate use identical external data, integrator and stopping gates.'}
    (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')

    def own(path):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        report['inputs'][str(path.relative_to(root))] = digest
        return digest

    def artifact(path):
        report['outputs'][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def maximum(value):
        return float(numerical.max(numerical.abs(value)))

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        save()
        print(name + ': ' + str(bool(passed)), flush=True)

    def fixture(case_name, intervals, branch):
        case_path = intake / 'annular-constraint-correction-initial' / (case_name + '.json')
        own(case_path)
        case = json.loads(case_path.read_text())
        constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
        kappa = float(symbolic.sympify(case['normalization_kappa']))
        tag = case_name + '_N' + str(intervals)
        path = intake / 'annular-constraint-routhian-derived' / (tag + '_' + ('GR' if branch == 'GR' else 'Gram') + '.npz')
        own(path)
        with numerical.load(path) as loaded:
            arrays = {name: loaded[name].copy() for name in loaded.files}
        if branch != 'GR':
            path = intake / 'annular-metric-time-links-derived' / (tag + '.npz')
            own(path)
            with numerical.load(path) as loaded:
                arrays.update({name: loaded[name].copy() for name in loaded.files})
        basis = MixedActionBasis(arrays['radius'])
        links = MetricLinkQuadrature(basis)
        system = CachedMetricLinkRouthian(basis, arrays['scalar'], arrays['defect'], arrays['defect_time'], constants, kappa, arrays['momentum'], arrays['outer_clock'][0], links=links)
        return arrays, basis, links, system

    save()
    try:
        prior_path = intake / 'annular-metric-time-links-derived/status.json'
        own(prior_path)
        prior = json.loads(prior_path.read_text())
        check('previous_metric_link_first_variation_complete', prior['state'] == 'complete' and prior['passed'] == prior['total'])
        check('previous_source_and_result_hashes_match', all(own(root / name) == digest for name, digest in {**prior['inputs'], **prior['outputs']}.items()))
        for name in ['annular_metric_link_quadratic_20260909.py', 'derive_annular_metric_dynamics_20260909.py']:
            path = root / 'scripts' / name
            own(path)
            compile(path.read_bytes(), str(path), 'exec')
        if arguments.phase == 'evolution':
            gate_path = intake / 'annular-metric-quadratic-derived/status.json'
            own(gate_path)
            gate = json.loads(gate_path.read_text())
            check('new_action_quadratic_gate_complete', gate['state'] == 'complete' and gate['passed'] == gate['total'])
            check('quadratic_sources_and_results_unchanged', all(own(root / name) == digest for name, digest in {**gate['inputs'], **gate['outputs']}.items()))
            if not all(row['passed'] for row in report['checks']):
                raise RuntimeError('No evolution before source and quadratic gates.')
        endpoints = {}
        for case_name in ['canonical', 'nonlinear_modulated']:
            for intervals in [16, 32]:
                if arguments.phase == 'quadratic':
                    tag = case_name + '_N' + str(intervals)
                    report['active_job'] = tag
                    save()
                    arrays, basis, links, system = fixture(case_name, intervals, 'metric_Gram')
                    path = MetricQuadraticPath(system, arrays, links)
                    mass, lapse, velocity = [arrays['corrected'][selected] for selected in system.slices]
                    matrix = links.matrix(mass, lapse, system.constants)
                    check(tag + '_cached_metric_integral_matches_owned_matrix', maximum(matrix - arrays['metric_link_matrix']) < 1e-13, maximum(matrix - arrays['metric_link_matrix']))
                    low_order = MetricLinkQuadrature(basis, order=4)
                    check(tag + '_quadrature_order_control', maximum(matrix - low_order.matrix(mass, lapse, system.constants)) < 1e-13)
                    coordinate = (links.points - links.anchors[links.pairs]) / basis.spacing
                    endpoint = (links.targets - links.anchors) / basis.spacing
                    for power in range(5):
                        integrand = coordinate**power
                        partial_error = maximum(links.partial(integrand) - basis.spacing * coordinate**(power + 1) / (power + 1))
                        endpoint_error = maximum(links.integrate(integrand) - basis.spacing * endpoint**(power + 1) / (power + 1))
                        check(tag + '_signed_primitive_polynomial_' + str(power), max(partial_error, endpoint_error) < 5e-12, {'partial_error': partial_error, 'endpoint_error': endpoint_error})
                    tangent = system.constraint_tangent(arrays['corrected'], True, arrays['defect_acceleration'], arrays['endpoint_acceleration'], arrays['outer_clock'][1])
                    check(tag + '_cached_tangent_matches_saved_new_action', maximum(tangent['packed_speed'] - arrays['packed_speed']) < 2e-12)
                    position, background_speed, defect, defect_time = path.path(0)
                    tiny = 1e-25
                    check(tag + '_actual_lifting_acceleration_retained', maximum(path.path(1j * tiny)[3].imag / tiny - arrays['defect_acceleration']) < 1e-11)
                    mass_node = real_linear(basis.face_to_node, mass)
                    coefficient, unused_gradient, hessian = coefficient_jets(velocity, path.gradient, mass_node, lapse, basis.radii, system.constants)
                    bare_kinetic = basis.kinetic_matrix(position, background_speed, defect, defect_time, system.constants)
                    correction = numerical.diag(system.density * hessian[0, 0])
                    kinetic = bare_kinetic - correction
                    eigenvalues = numerical.linalg.eigvalsh(kinetic)
                    check(tag + '_positive_scalar_kinetic_matrix', float(eigenvalues[0]) > 0, {'minimum_eigenvalue': float(eigenvalues[0]), 'relative_correction': float(numerical.linalg.norm(correction) / numerical.linalg.norm(bare_kinetic))})
                    if case_name == 'canonical':
                        check(tag + '_canonical_scalar_kinetic_correction_exact_zero', not numerical.any(correction))
                    zeros = [numerical.zeros_like(value) for value in position]
                    rng = numerical.random.default_rng(20260909 + intervals)
                    displacement = [scale * rng.normal(size=value.size) for value, scale in zip(position, [0.0002, 0.003, 0.002, 0.005])]
                    speed = [scale * rng.normal(size=value.size) for value, scale in zip(position, [0.0003, 0.002, 0.001, 0.004])]
                    reduced, boundary, raw = path.quadratic(0, displacement, speed, raw=True)
                    boundary_rate = path.quadratic(1j * tiny, displacement, speed)[1].imag / tiny
                    identity_error = float(abs(raw - reduced - boundary_rate))
                    check(tag + '_raw_reduced_time_boundary_identity', identity_error < 1e-11 * max(abs(raw), abs(reduced), abs(boundary_rate), 1e-12), {'raw': float(raw), 'reduced': float(reduced), 'boundary_rate': float(boundary_rate), 'error': identity_error})
                    check(tag + '_time_boundary_not_silently_omitted', abs(boundary_rate) > 100 * max(identity_error, 1e-22))
                    scalar_speed = [speed[0], zeros[1], zeros[2], zeros[3]]
                    direct_kinetic = -path.quadratic(0, zeros, scalar_speed)[0]
                    check(tag + '_independent_scalar_velocity_quadratic', abs(direct_kinetic + numerical.dot(speed[0], correction @ speed[0]) / 2) < 1e-18)
                    metric_speed = [zeros[0], speed[1], speed[2], speed[3]]
                    check(tag + '_no_metric_velocity_squared', path.quadratic(0, zeros, metric_speed)[0] == 0)
                    metric_block = path.metric_velocity_position_block()
                    for probe_index in range(3):
                        varied = [numerical.zeros_like(value) for value in position]
                        varied[3] = rng.normal(size=basis.faces.size)
                        metric_rate = [numerical.zeros_like(value) for value in position]
                        metric_rate[3] = rng.normal(size=basis.faces.size)
                        mixed = -path.quadratic(0, varied, metric_rate)[0] + path.quadratic(0, varied, zeros)[0] + path.quadratic(0, zeros, metric_rate)[0]
                        analytic = numerical.dot(metric_rate[3], metric_block @ varied[3])
                        check(tag + '_analytic_full_shift_pairing_probe_' + str(probe_index), abs(mixed - analytic) < 1e-10 * max(abs(mixed), abs(analytic), 1e-12), {'direct': float(mixed), 'analytic': float(analytic), 'error': float(abs(mixed - analytic))})
                    forbidden_position = [zeros[0], displacement[1], displacement[2], zeros[3]]
                    forbidden_speed = [zeros[0], speed[1], speed[2], speed[3]]
                    forbidden = path.quadratic(0, forbidden_position, forbidden_speed)[0] - path.quadratic(0, forbidden_position, zeros)[0]
                    check(tag + '_forbidden_metric_pairings_absent', forbidden == 0)
                    face_count, node_count = basis.faces.size, basis.radii.size
                    pairing = tangent['pairing']
                    omega = numerical.zeros((2 * face_count + node_count, 2 * face_count + node_count))
                    omega[:face_count, face_count:2 * face_count] = pairing
                    omega[face_count:2 * face_count, :face_count] = -pairing.T
                    omega[face_count:2 * face_count, face_count:2 * face_count] = metric_block - metric_block.T
                    singular_values = numerical.linalg.svd(omega, compute_uv=False)
                    rank = int(numerical.sum(singular_values > singular_values[0] * 1e-11))
                    check(tag + '_full_metric_primary_rank', rank == 2 * face_count and numerical.linalg.eigvalsh(pairing)[0] > 0, {'rank': rank, 'metric_variables': omega.shape[0], 'lapse_nullity': int(omega.shape[0] - rank)})
                    finite_rows = []
                    base = path.exact_potential(0, displacement, speed, 0)
                    for amplitude in [0.01, 0.005]:
                        finite = (path.exact_potential(0, displacement, speed, amplitude) + path.exact_potential(0, displacement, speed, -amplitude) - 2 * base) / (2 * amplitude**2)
                        error = float(abs(finite - raw))
                        finite_rows.append({'amplitude': amplitude, 'finite': float(finite), 'raw_quadratic': float(raw), 'error': error})
                        check(tag + '_independent_nonlinear_flow_second_variation_' + str(amplitude), error < 1e-4 * max(abs(raw), abs(finite), 1e-15) + 2e-12, finite_rows[-1])
                    extrapolated = (4 * finite_rows[-1]['finite'] - finite_rows[0]['finite']) / 3
                    check(tag + '_second_variation_Richardson', abs(extrapolated - raw) < 2e-5 * max(abs(raw), 1e-15) + 2e-12, {'extrapolated': float(extrapolated), 'error': float(abs(extrapolated - raw))})
                    target = destination / (tag + '.npz')
                    numerical.savez_compressed(target, kinetic=kinetic, bare_kinetic=bare_kinetic, scalar_correction=correction, metric_shift_velocity_position=metric_block, full_metric_primary_omega=omega, metric_link_matrix=matrix, singular_values=singular_values, **{'displacement_' + str(index): value for index, value in enumerate(displacement)}, **{'speed_' + str(index): value for index, value in enumerate(speed)})
                    artifact(target)
                    report['samples'].append({'case': case_name, 'intervals': intervals, 'scalar_minimum_eigenvalue': float(eigenvalues[0]), 'kinetic_relative_correction': float(numerical.linalg.norm(correction) / numerical.linalg.norm(bare_kinetic)), 'primary_metric_rank': rank, 'primary_lapse_nullity': node_count, 'secondary_Dirac_closure_proven': False, 'finite_second_variations': finite_rows})
                    save()
                else:
                    for branch in ['GR', 'metric_Gram']:
                        arrays, basis, links, initial_system = fixture(case_name, intervals, branch)
                        node_count, packed_count = basis.radii.size, initial_system.count
                        include_gram = branch != 'GR'
                        initial = numerical.concatenate([arrays['scalar'], arrays['momentum'], arrays['corrected']])
                        tag = case_name + '_N' + str(intervals) + '_' + branch
                        report['active_job'] = tag
                        save()

                        def rhs(time, state, diagnostic=False):
                            scalar, momentum, packed = state[:node_count], state[node_count:2 * node_count], state[2 * node_count:]
                            defect = arrays['defect'] + time * arrays['defect_time'] + time**2 * arrays['defect_acceleration'] / 2
                            defect_time = arrays['defect_time'] + time * arrays['defect_acceleration']
                            system = CachedMetricLinkRouthian(basis, scalar, defect, defect_time, initial_system.constants, initial_system.kappa, momentum, arrays['outer_clock'][0] + time * arrays['outer_clock'][1], links=links)
                            tangent = system.constraint_tangent(packed, include_gram, arrays['defect_acceleration'], arrays['endpoint_acceleration'], arrays['outer_clock'][1])
                            derivative = numerical.concatenate([packed[system.slices[2]], tangent['momentum_speed'], tangent['packed_speed']])
                            if not numerical.all(numerical.isfinite(derivative)):
                                raise ValueError('Nonfinite tangent; no continuation past this state.')
                            if not diagnostic:
                                return derivative
                            unused_action, gradient, unused_hessian = system.evaluate(packed, include_gram)
                            valid, health = system.admissible(packed, include_gram)
                            if not valid:
                                raise ValueError('Admissibility gate: ' + repr(health))
                            free_gradient = gradient[system.free]
                            mass_mismatch = tangent['packed_speed'][system.slices[0]] - tangent['shift_mass_speed']
                            diagnostic_data = {'time': float(time), 'constraint_max': maximum(free_gradient), 'constraint_scaled_max': maximum(free_gradient / arrays['row_scale']), 'constraint_derivative_max': maximum(tangent['constraint_derivative_residual']), 'shift_residual_max': maximum(tangent['shift_residual']), 'mass_rate_mismatch_max': maximum(mass_mismatch), **health}
                            return derivative, diagnostic_data, free_gradient, tangent['shift_residual'], mass_mismatch, gradient[system.fixed]

                        derivative0, diagnostic0, constraint0, unused_shift, unused_mass, unused_reactions = rhs(0, initial, True)
                        check(tag + '_initial_tangent_matches_owned_result', maximum(derivative0[2 * node_count:] - arrays['packed_speed']) < 2e-12)
                        end_time = 0.01
                        for steps in [4, 8, 16]:
                            state = initial.copy()
                            step = end_time / steps
                            times, states, diagnostics, constraints, shifts, mismatches, reactions = [], [], [], [], [], [], []
                            for index in range(steps + 1):
                                time = index * step
                                first, diagnostic, residual, shift, mismatch, reaction = rhs(time, state, True)
                                times.append(time)
                                states.append(state.copy())
                                diagnostics.append(diagnostic)
                                constraints.append(residual)
                                shifts.append(shift)
                                mismatches.append(mismatch)
                                reactions.append(reaction)
                                if index < steps:
                                    second = rhs(time + step / 2, state + step * first / 2)
                                    third = rhs(time + step / 2, state + step * second / 2)
                                    fourth = rhs(time + step, state + step * third)
                                    state = state + step * (first + 2 * second + 2 * third + fourth) / 6
                            target = destination / (tag + '_steps' + str(steps) + '.npz')
                            numerical.savez_compressed(target, time=numerical.asarray(times), state=numerical.asarray(states), constraints=numerical.asarray(constraints), shifts=numerical.asarray(shifts), mass_rate_mismatch=numerical.asarray(mismatches), fixed_boundary_reactions=numerical.asarray(reactions), radius=basis.radii, faces=basis.faces)
                            artifact(target)
                            detail_path = destination / (tag + '_steps' + str(steps) + '.json')
                            detail_path.write_text(json.dumps(diagnostics, indent=2) + '\n')
                            artifact(detail_path)
                            check(tag + '_steps' + str(steps) + '_finite_unprojected_trajectory', numerical.all(numerical.isfinite(states)) and len(states) == steps + 1)
                            check(tag + '_steps' + str(steps) + '_all_shift_rows_saved', numerical.asarray(shifts).shape == (steps + 1, basis.faces.size))
                            expected_endpoints = arrays['scalar'][[0, -1]] + end_time * arrays['corrected'][initial_system.slices[2]][[0, -1]] + end_time**2 * arrays['endpoint_acceleration'] / 2
                            check(tag + '_steps' + str(steps) + '_prescribed_scalar_boundary_history', maximum(state[:node_count][[0, -1]] - expected_endpoints) < 1e-13)
                            drift = maximum(numerical.asarray(constraints) - constraint0)
                            report['samples'].append({'case': case_name, 'intervals': intervals, 'branch': branch, 'steps': steps, 'end_time': end_time, 'start_constraint_max': diagnostic0['constraint_max'], 'maximum_constraint_drift': drift, 'maximum_constraint_residual': max(value['constraint_max'] for value in diagnostics), 'maximum_shift_residual': max(value['shift_residual_max'] for value in diagnostics), 'maximum_mass_rate_mismatch': max(value['mass_rate_mismatch_max'] for value in diagnostics), 'end_mass_rate_mismatch': diagnostics[-1]['mass_rate_mismatch_max'], 'minimum_scalar_Legendre_eigenvalue': min(value['minimum_scalar_Legendre_eigenvalue'] for value in diagnostics), 'state_change_max': maximum(state - initial), 'equations_integrated': 'chi_dot=q; pi_dot=L_chi interior; differentiated free Routh equations; inner mass rate from full shift solve; prescribed endpoint acceleration; no algebraic projection', 'full_shift_equations_solved': False})
                            endpoints[case_name, intervals, branch, steps] = state.copy()
                            save()
                            print(tag + ' steps=' + str(steps) + ' drift=' + str(drift), flush=True)
                        coarse = maximum(endpoints[case_name, intervals, branch, 4] - endpoints[case_name, intervals, branch, 8])
                        fine = maximum(endpoints[case_name, intervals, branch, 8] - endpoints[case_name, intervals, branch, 16])
                        check(tag + '_time_refinement_or_roundoff_floor', fine < 0.3 * coarse or max(coarse, fine) < 5e-12, {'coarse_endpoint_difference': coarse, 'fine_endpoint_difference': fine, 'ratio': coarse / fine if fine else None})
        if arguments.phase == 'evolution':
            report['comparisons'] = []
            for case_name in ['canonical', 'nonlinear_modulated']:
                for intervals in [16, 32]:
                    rows = [row for row in report['samples'] if row['case'] == case_name and row['intervals'] == intervals and row['steps'] == 16]
                    gr = next(row for row in rows if row['branch'] == 'GR')
                    candidate = next(row for row in rows if row['branch'] == 'metric_Gram')
                    report['comparisons'].append({'case': case_name, 'intervals': intervals, 'candidate_to_GR_mass_rate_mismatch': candidate['maximum_mass_rate_mismatch'] / gr['maximum_mass_rate_mismatch'], 'candidate_to_GR_shift_residual': candidate['maximum_shift_residual'] / gr['maximum_shift_residual'], 'GR_constraint_drift': gr['maximum_constraint_drift'], 'candidate_constraint_drift': candidate['maximum_constraint_drift'], 'same_external_lifting_and_boundary_jets': True, 'no_projection_or_constraint_damping': True, 'empirical_comparison': False})
        imported = []
        for module in tuple(sys.modules.values()):
            filename = getattr(module, '__file__', None)
            if filename:
                path = Path(filename).resolve()
                if path.parent == root / 'scripts' and path.suffix == '.py':
                    own(path)
                    imported.append(str(path.relative_to(root)))
        report['imported_local_modules'] = sorted(imported)
        check('all_owned_inputs_unchanged', all(hashlib.sha256((root / name).read_bytes()).hexdigest() == digest for name, digest in report['inputs'].items()))
        check('no_bytecode_cache', not (root / 'scripts/__pycache__').exists())
        report.update(passed=sum(row['passed'] for row in report['checks']), total=len(report['checks']), completed_utc=datetime.now(timezone.utc).isoformat())
        report['state'] = 'complete' if report['passed'] == report['total'] else 'failed'
        artifact(destination / 'executed-script.py')
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
