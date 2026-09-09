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
    from annular_adm_mixed_action_20260909 import MixedActionBasis
    from annular_boundary_adapted_energy_20260909 import adapted_diagnostic
    from annular_clock_spatial_bound_20260909 import spatial_bounds
    from annular_first_derivative_energy_20260909 import canonical_matrices
    from annular_H1_clock_energy_20260909 import adapted_energy_feedback, boundary_bounds, local_certificates, transport_bounds, zero_slope_lift
    from annular_metric_flux_jets_20260909 import second_spatial_matrix
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_metric_source_bound_20260909 import scalar_source_data
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian
    from annular_uniform_energy_bounds_20260909 import full_operator_norm, metric_envelope

    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['derive', 'seal'])
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260909'
    destination = intake / 'annular-H1-clock-energy-derived'
    final_path = intake / 'annular-H1-clock-energy-final-integrity.json'
    prior_path = intake / 'annular-clock-spatial-and-inner-shift-final-integrity.json'
    prior = json.loads(prior_path.read_text())
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

    if prior['state'] != 'complete':
        raise RuntimeError('Spatial/inner-flux gate incomplete.')
    inherit(inputs, prior['inputs'])
    inherit(outputs, prior['outputs'])
    own(prior_path)
    scripts = ['annular_H1_clock_energy_20260909.py', 'derive_annular_H1_clock_energy_20260909.py']
    for name in scripts:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    if arguments.phase == 'derive':
        destination.mkdir(exist_ok=False)
        (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())
        report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': inputs, 'outputs': outputs, 'checks': [], 'samples': [], 'manufactured': [], 'actual_weighted_projection_H1_bound_derived': True, 'bulk_and_Gram_stiffness_transport_H1_bound_derived': True, 'boundary_adapted_energy_inequality_derived': True, 'remaining_boundary_input': 'T2=||theta_t|| in the actual quadrature L2 norm; measured here from the exact owned second jets, NOT bounded uniformly over time by this step.', 'energy_evolution_or_box_persistence_closed': False, 'full_coupled_DAE_solved': False, 'valid_for_physics_claim': False}

        def save():
            (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

        def check(name, passed, detail=None):
            report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
            if not passed:
                raise RuntimeError('Failed check: ' + name + ' ' + repr(detail))

        def maximum(values):
            return float(numerical.max(abs(values)))

        def norm(values, weights):
            return float(numerical.sqrt(max(0.0, weights @ values**2)))

        def matrix_dual(vector, mass):
            return float(numerical.sqrt(max(0.0, vector @ numerical.linalg.solve(mass, vector))))

        def operators(label, system, packed, speed, include_gram, bounds):
            matrices = canonical_matrices(system, packed, speed, include_gram)
            free = system.free_velocity_indices - system.slices[2].start
            selection = numerical.ix_(free, free)
            mass, stiffness, mass_rate, stiffness_rate = [matrices[name][selection] for name in ['M', 'K', 'M_dot', 'K_dot']]
            mass_operator = numerical.linalg.solve(mass, mass_rate)
            stiffness_operator = numerical.linalg.solve(mass, stiffness_rate @ numerical.linalg.solve(stiffness, mass))
            measured_a = full_operator_norm(mass_operator, stiffness)
            measured_l = full_operator_norm(stiffness_operator, mass)
            check(label + '_actual_mass_projection_H1_transport', measured_a <= bounds['alpha_A_bound'] + 1e-10)
            check(label + '_actual_bulk_plus_Gram_transport', measured_l <= bounds['alpha_L_bound'] + 1e-10)
            second = second_spatial_matrix(system.basis, system.basis.quadrature)[:, free]
            elliptic = numerical.linalg.solve(stiffness, mass)
            root_mass = numerical.linalg.cholesky(mass)
            mapped = numerical.sqrt(system.basis.quadrature_weights)[:, None] * (second @ elliptic)
            measured_h2 = float(numerical.linalg.svd(numerical.linalg.solve(root_mass, mapped.T).T, compute_uv=False)[0])
            check(label + '_inherited_actual_H2_graph_bound', measured_h2 <= bounds['elliptic_H2_constant'] + 1e-10)
            return {'alpha_A_full_norm': measured_a, 'alpha_L_full_norm': measured_l, 'elliptic_H2_operator_norm': measured_h2}, matrices

        save()
        try:
            report['local_certificates'] = local_certificates()
            check('exact_zero_slope_interpolant_derivative_constant', report['local_certificates']['derivative_constant_two_valid'])
            case_path = intake / 'annular-constraint-correction-initial/canonical.json'
            own(case_path)
            case = json.loads(case_path.read_text())
            constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
            kappa = float(symbolic.sympify(case['normalization_kappa']))
            inner_path = intake / 'annular-inner-shift-trace-certified/status.json'
            own(inner_path)
            inner_report = json.loads(inner_path.read_text())
            common = {'length': .25, 'm_min': (47 / 8)**2 / (.84 * numerical.sqrt(.68)), 'm_max': 60025 / 1024, 'p_min': (47 / 8)**2 * .8 * numerical.sqrt(.65), 'p_max': 16807 / 640}
            for parent in inner_report['samples']:
                label, intervals, branch = parent['label'], parent['intervals'], parent['branch']
                steps = 64 if intervals == 64 else 32
                index = int(label.rsplit('sample', 1)[1])
                tag = label.split('_sample')[0]
                report['active_job'] = label
                save()
                source = loaded(intake / 'annular-released-Hermite-initial-derived' / (tag + '.npz'))
                folder = 'annular-boundary-N64-evolution-smoke' if intervals == 64 else 'annular-released-Hermite-evolution-smoke'
                trajectory = loaded(intake / folder / (tag + '_steps' + str(steps) + '.npz'))
                basis = MixedActionBasis(source['radius'])
                count = basis.radii.size
                time, state = trajectory['time'][index], trajectory['state'][index]
                scalar, slope, momentum, slope_momentum = [state[part * count:(part + 1) * count] for part in range(4)]
                packed = state[4 * count:]
                include_gram = branch != 'GR'
                system = ReleasedHermiteRouthian(basis, scalar, slope, constants, kappa, momentum, slope_momentum, source['outer_clock'][0] + time * source['outer_clock'][1], MetricLinkQuadrature(basis))
                tangent = system.constraint_tangent(packed, include_gram, source['endpoint_acceleration'], source['outer_clock'][1])
                speed = tangent['packed_speed']
                jets = loaded(intake / 'annular-metric-flux-jets-derived' / (label + '.npz'))
                spatial = loaded(intake / 'annular-clock-spatial-gradient-derived' / (label + '.npz'))
                base = loaded(intake / 'annular-first-derivative-energy-derived' / (label + '.npz'))
                adapted = adapted_diagnostic(system, packed, tangent, jets['jet_acceleration'], base, include_gram)
                scalar_data = scalar_source_data(system, packed, include_gram, source['endpoint_acceleration'])
                feedback = adapted_energy_feedback(system, scalar_data, spatial['mass_static_residual'], spatial['mass_time_residual'], parent['all_grid_shift_bound'], source['outer_clock'][1], source['endpoint_acceleration'], include_gram)
                check(label + '_actual_boundary_feedback_absorbable', feedback['absorption_gate'], feedback['raw_to_adapted_feedback'])
                raw_root = numerical.sqrt(max(0.0, 2 * scalar_data['energy']))
                adapted_root = numerical.sqrt(max(0.0, 2 * float(adapted['energy'])))
                raw_upper = (adapted_root + feedback['raw_to_adapted_boundary_offset']) / (1 - feedback['raw_to_adapted_feedback'])
                check(label + '_raw_energy_matches_old_energy', abs(scalar_data['energy'] - float(base['energy'])) < 1e-11)
                check(label + '_raw_to_adapted_energy_transfer', raw_root <= raw_upper + 1e-11)
                for trial_root in [0., .1, 1., 10.]:
                    changed_data = dict(scalar_data, energy=trial_root**2 / 2)
                    direct_bound = spatial_bounds(system, changed_data, spatial['mass_static_residual'], spatial['mass_time_residual'], parent['all_grid_shift_bound'], source['outer_clock'][1], source['endpoint_acceleration'], include_gram)
                    check(label + '_homogeneous_majorant_' + str(trial_root), direct_bound['theta_sup_bound'] <= feedback['theta_sup_offset'] + feedback['theta_sup_slope'] * trial_root + 1e-10 and direct_bound['theta_radial_L2_bound'] <= feedback['theta_gradient_L2_offset'] + feedback['theta_gradient_L2_slope'] * trial_root + 1e-10)
                theta_bound = feedback['theta_sup_offset'] + feedback['theta_sup_slope'] * raw_upper
                gradient_bound = feedback['theta_gradient_L2_offset'] + feedback['theta_gradient_L2_slope'] * raw_upper
                bound = transport_bounds(**common, p_lipschitz=feedback['p_lipschitz_derived'], theta_center=0.0, theta_radius=theta_bound, theta_gradient_l2=gradient_bound, include_gram=include_gram)
                measured, matrices = operators(label, system, packed, speed, include_gram, bound)
                mass_value = basis.face_value @ packed[system.slices[0]]
                mass_speed = basis.face_value @ speed[system.slices[0]]
                mass_second = basis.face_value @ jets['jet_acceleration'][system.slices[0]]
                lapse_value = basis.node_value @ packed[system.slices[1]]
                lapse_speed = basis.node_value @ speed[system.slices[1]]
                lapse_second = basis.node_value @ jets['jet_acceleration'][system.slices[1]]
                denominator = basis.quadrature - 2 * mass_value
                theta_time = lapse_second / lapse_value - (lapse_speed / lapse_value)**2 - mass_second / denominator - 2 * (mass_speed / denominator)**2
                theta_time_qnorm = norm(theta_time, basis.quadrature_weights)
                boundary = boundary_bounds(common['length'], common['m_min'], common['m_max'], common['p_max'], feedback['p_lipschitz_derived'], theta_bound, gradient_bound, theta_time_qnorm, system.scalar[[0, -1]], packed[system.slices[2]][[0, -1]], source['endpoint_acceleration'])
                force_norm = matrix_dual(adapted['boundary_force'], base['M'])
                rate_norm = matrix_dual(adapted['boundary_force_time'], base['M'])
                source_upper = bound['alpha_L_bound'] * boundary['force_M_dual_bound'] + boundary['force_time_M_dual_bound']
                check(label + '_boundary_force_bound_with_H1_clock', force_norm <= boundary['force_M_dual_bound'] + 1e-10)
                check(label + '_boundary_force_rate_bound_with_explicit_T2', rate_norm <= boundary['force_time_M_dual_bound'] + 1e-10)
                check(label + '_boundary_adapted_source_bound', float(adapted['boundary_source_M_dual_norm']) <= source_upper + 1e-10)
                energy_upper = bound['growth_bound'] * float(adapted['energy']) + adapted_root * (source_upper + float(adapted['residual_force_K_graph_norm']))
                check(label + '_same_exact_adapted_energy_identity', abs(float(adapted['energy_time_predicted'] - adapted['energy_time_complex'])) < 1e-9)
                check(label + '_H1_energy_differential_inequality', float(adapted['energy_time_predicted']) <= energy_upper + 1e-9)
                check(label + '_old_boundary_and_shift_preserved', numerical.array_equal(speed, spatial['packed_speed']) and numerical.array_equal(tangent['shift_residual'], spatial['full_shift_residual']) and numerical.array_equal(jets['physical_mismatch'], spatial['old_physical_mismatch']))
                output = destination / (label + '.npz')
                numerical.savez_compressed(output, **adapted, theta_time=theta_time, physical_mismatch=jets['physical_mismatch'], physical_mismatch_time=jets['jet_physical_mismatch_time'], full_shift_residual=spatial['full_shift_residual'])
                artifact(output)
                row = {'label': label, 'intervals': intervals, 'branch': branch, 'time': float(time), 'feedback': feedback, 'bounds': bound, 'boundary_bounds': boundary, 'measured': measured, 'raw_graph_energy': scalar_data['energy'], 'adapted_graph_energy': float(adapted['energy']), 'raw_energy_root_upper_from_adapted': float(raw_upper), 'boundary_source_bound': source_upper, 'boundary_source_measured': float(adapted['boundary_source_M_dual_norm']), 'energy_derivative': float(adapted['energy_time_predicted']), 'energy_derivative_bound_conditional_on_T2': float(energy_upper), 'theta_time_Q_L2_sampled_not_uniformly_bounded': theta_time_qnorm}
                report['samples'].append(row)
                save()
                if index == steps:
                    print(json.dumps({'label': label, 'feedback': feedback['raw_to_adapted_feedback'], 'alpha_A_bound': bound['alpha_A_bound'], 'alpha_L_bound': bound['alpha_L_bound'], 'T2_measured_only': theta_time_qnorm, 'energy_derivative': row['energy_derivative'], 'energy_upper': energy_upper}), flush=True)
            for intervals in [16, 32, 64, 128]:
                basis = MixedActionBasis(numerical.linspace(47 / 8, 49 / 8, intervals + 1))
                count = basis.radii.size
                system = ReleasedHermiteRouthian(basis, numerical.zeros(count), numerical.zeros(count), constants, kappa, numerical.zeros(count), numerical.zeros(count), 1.0, MetricLinkQuadrature(basis))
                packed = numerical.zeros(system.count)
                packed[system.slices[0]], packed[system.slices[1]] = 1.0, .82
                envelope = metric_envelope(basis, packed[system.slices[0]], packed[system.slices[1]], numerical.zeros(system.face_count), numerical.zeros(count))
                for mode in ['constant_clock', 'H1_bounded_spike']:
                    theta_nodes = numerical.full(count, .003) if mode == 'constant_clock' else numerical.zeros(count)
                    if mode != 'constant_clock':
                        theta_nodes[count // 2] = numerical.sqrt(basis.spacing)
                    theta_center = float((min(theta_nodes) + max(theta_nodes)) / 2)
                    theta_radius = float((max(theta_nodes) - min(theta_nodes)) / 2)
                    gradient_l2 = float(numerical.linalg.norm(numerical.diff(theta_nodes)) / numerical.sqrt(basis.spacing))
                    gradient_sup = float(max(abs(numerical.diff(theta_nodes))) / basis.spacing)
                    speed = numerical.zeros_like(packed)
                    speed[system.slices[1]] = .82 * theta_nodes
                    for include_gram in [False, True]:
                        label = mode + '_N' + str(intervals) + ('_Gram' if include_gram else '_GR')
                        bound = transport_bounds(envelope['length'], envelope['m_min'], envelope['m_max'], envelope['p_min'], envelope['p_max'], envelope['p_lipschitz'], theta_center, theta_radius, gradient_l2, include_gram)
                        measured, matrices = operators(label, system, packed, speed, include_gram, bound)
                        if mode == 'constant_clock':
                            check(label + '_constant_rescaling_exact', abs(measured['alpha_A_full_norm'] - .003) < 1e-9 and abs(measured['alpha_L_full_norm'] - .003) < 1e-9 and bound['alpha_A_bound'] == .003 and bound['alpha_L_bound'] == .003)
                        else:
                            check(label + '_spatial_L2_fixed_despite_pointwise_growth', abs(gradient_l2 - numerical.sqrt(2)) < 1e-12)
                        free = system.free_velocity_indices - system.slices[2].start
                        value = numerical.concatenate([basis.scalar_value, basis.lift_value / basis.spacing], axis=1)
                        radial = numerical.concatenate([basis.scalar_gradient, basis.lift_gradient / basis.spacing], axis=1)
                        offset = basis.radii - basis.radii[0]
                        scalar_nodes = offset * (.25 - offset)
                        configuration = numerical.concatenate([scalar_nodes, basis.spacing * (.25 - 2 * offset - basis.derivative @ scalar_nodes)])
                        theta_q, theta_r = basis.node_value @ theta_nodes, basis.node_gradient @ theta_nodes
                        product = theta_q * (value @ configuration)
                        product_radial = theta_r * (value @ configuration) + theta_q * (radial @ configuration)
                        lift = zero_slope_lift(basis, theta_nodes * scalar_nodes)
                        product_gradient = norm(product_radial, basis.quadrature_weights)
                        check(label + '_zero_slope_H1_interpolant_and_Q_error', norm(radial @ lift, basis.quadrature_weights) <= 2 * product_gradient + 1e-12 and norm(value @ lift - product, basis.quadrature_weights) <= 2 * basis.spacing * product_gradient + 1e-12)
                        mass_q = basis.quadrature**2 / (.82 * numerical.sqrt(1 - 2 / basis.quadrature))
                        projected = numerical.linalg.solve(matrices['M'][numerical.ix_(free, free)], value[:, free].T @ (basis.quadrature_weights * mass_q * product))
                        check(label + '_actual_weighted_projection_H1_stability', norm(radial[:, free] @ projected, basis.quadrature_weights) <= bound['projection_H1_constant'] * product_gradient + 1e-10)
                        report['manufactured'].append({'label': label, 'bounds': bound, 'measured': measured, 'theta_gradient_L2': gradient_l2, 'theta_gradient_sup': gradient_sup})
                        save()
            for module in tuple(sys.modules.values()):
                filename = getattr(module, '__file__', None)
                if filename:
                    path = Path(filename).resolve()
                    if path.parent == root / 'scripts' and path.suffix == '.py':
                        own(path)
            check('all_inherited_sources_preserved', all(digest(root / name) == expected for name, expected in inputs.items()))
            check('all_inherited_and_new_evidence_preserved', all(digest(root / name) == expected for name, expected in outputs.items()))
            check('no_bytecode_cache', not (root / 'scripts/__pycache__').exists())
            report.update(state='complete', passed=sum(row['passed'] for row in report['checks']), total=len(report['checks']), completed_utc=datetime.now(timezone.utc).isoformat())
            save()
            (destination / 'COMPLETE').write_text(report['completed_utc'] + '\n')
            print(json.dumps({name: report[name] for name in ['state', 'passed', 'total', 'completed_utc']}), flush=True)
            return
        except Exception as error:
            report.update(state='failed', failure=repr(error), traceback=traceback.format_exc(), completed_utc=datetime.now(timezone.utc).isoformat())
            save()
            raise
    report_path = destination / 'status.json'
    report = json.loads(report_path.read_text())
    if report['state'] != 'complete' or report['passed'] != report['total']:
        raise RuntimeError('H1 clock energy gate incomplete.')
    inherit(inputs, report['inputs'])
    inherit(outputs, report['outputs'])
    for path in [report_path, destination / 'COMPLETE', destination / 'executed-script.py']:
        own(path)
    note = root / 'DERIVATION-20260909-H1-clock-energy-transport-and-boundary-feedback.md'
    cited = [value for value in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')) if value.endswith(('.py', '.md', '.json', '.npz'))]
    missing = [value for value in cited if root / value != final_path and not (root / value).is_file()]
    if missing:
        raise FileNotFoundError(str(missing))
    own(note)
    snapshot = intake / 'annular-H1-clock-energy-resume-snapshot.md'
    with snapshot.open('xb') as handle:
        handle.write((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    artifact(snapshot)
    frozen = root.parent / 'formalization-workbench'
    since = datetime(2026, 9, 9, 21, 36, 0, tzinfo=timezone.utc).timestamp()
    touched = [str(path.relative_to(frozen)) for path in frozen.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if touched or (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Protected workbench/cache check failed: ' + repr(touched))
    final = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'checks': report['total'], 'saved_states': len(report['samples']), 'manufactured_cases': len(report['manufactured']), 'inputs': inputs, 'outputs': outputs, 'cited_local_paths_checked': cited, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-09T21:36:00Z, not full pre-turn hash baseline', 'mutable_resume_pinned_as_snapshot': True, 'no_bytecode_cache': True, 'H1_clock_operator_and_energy_bounds_derived': True, 'raw_adapted_energy_feedback_absorbed_on_saved_data': True, 'remaining_uniform_boundary_input': 'actual-quadrature L2 norm of theta_t', 'energy_evolution_and_box_persistence_closed': False, 'valid_for_physics_claim': False}
    with final_path.open('x') as handle:
        json.dump(final, handle, indent=2)
        handle.write('\n')
    print(json.dumps({name: final[name] for name in ['state', 'checks', 'saved_states', 'manufactured_cases', 'protected_workbench_files_written_since_turn_start']}), flush=True)


if __name__ == '__main__':
    run()
