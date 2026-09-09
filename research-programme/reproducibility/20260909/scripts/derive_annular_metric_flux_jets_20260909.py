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
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian
    from annular_metric_flux_jets_20260909 import SecondJet, exact_local_acceleration, flux_profile, metric_weak_reconstruction
    from annular_uniform_energy_bounds_20260909 import metric_envelope, coefficient_bounds, boundary_bounds

    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['derive', 'seal'])
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260909'
    destination = intake / 'annular-metric-flux-jets-derived'
    final_path = intake / 'annular-metric-flux-jets-final-integrity.json'
    prior_path = intake / 'annular-uniform-energy-bounds-final-integrity.json'
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
        raise RuntimeError('Prior gate incomplete.')
    inherit(inputs, prior['inputs'])
    inherit(outputs, prior['outputs'])
    own(prior_path)
    scripts = ['annular_metric_flux_jets_20260909.py', 'derive_annular_metric_flux_jets_20260909.py']
    for name in scripts:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    if arguments.phase == 'derive':
        destination.mkdir(exist_ok=False)
        (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())
        report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': inputs, 'outputs': outputs, 'checks': [], 'samples': [], 'canonical_metric_flux_cancellation_derived_with_all_defects': True, 'canonical_local_constraint_acceleration_differentiated': True, 'scalar_H2_bound_conditional_on_previous_envelopes': True, 'mesh_uniform_metric_bootstrap_closed': False, 'full_coupled_DAE_solved': False, 'valid_for_physics_claim': False, 'scope': 'Canonical Lambda=m_chi=b2=b3=0. Same finite action and same old states. Analytic second-order jet algebra and complex-step first derivatives, not differences of complete ODE solutions. No removal of old physical mismatch, Gram source, weak/strong constraint defect or natural boundary reaction.'}

        def save():
            (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

        def check(name, passed, detail=None):
            report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
            if not passed:
                raise RuntimeError('Failed check: ' + name + ' ' + repr(detail))

        def maximum(values):
            return float(numerical.max(numerical.abs(values)))

        def norm(values, weights):
            return float(numerical.sqrt(numerical.dot(weights, values**2)))

        save()
        try:
            parameter = symbolic.Symbol('parameter', real=True)
            expression = (2 + parameter + parameter**2 / 3)**symbolic.Rational(-1, 2) * (3 - 2 * parameter + parameter**2)**2 / (4 + parameter)
            evaluated = (SecondJet(2.0, 1.0, 2 / 3)**-.5) * SecondJet(3.0, -2.0, 2.0)**2 / SecondJet(4.0, 1.0)
            for order, value in enumerate([evaluated.value, evaluated.first, evaluated.second]):
                expected = float(symbolic.diff(expression, parameter, order).subs(parameter, 0))
                check('jet_order_' + str(order), abs(float(value) - expected) < 1e-14)
            case_path = intake / 'annular-constraint-correction-initial/canonical.json'
            own(case_path)
            case = json.loads(case_path.read_text())
            constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
            kappa = float(symbolic.sympify(case['normalization_kappa']))
            for intervals in [16, 32, 64]:
                steps = 64 if intervals == 64 else 32
                for branch in ['GR', 'metric_Gram']:
                    tag = 'canonical_N' + str(intervals) + '_' + branch
                    source = loaded(intake / 'annular-released-Hermite-initial-derived' / (tag + '.npz'))
                    folder = 'annular-boundary-N64-evolution-smoke' if intervals == 64 else 'annular-released-Hermite-evolution-smoke'
                    trajectory = loaded(intake / folder / (tag + '_steps' + str(steps) + '.npz'))
                    basis = MixedActionBasis(source['radius'])
                    links = MetricLinkQuadrature(basis)
                    count = basis.radii.size
                    for index in [0, steps // 2, steps]:
                        label = tag + '_sample' + str(index)
                        report['active_job'] = label
                        save()
                        time, state = trajectory['time'][index], trajectory['state'][index]
                        scalar, slope, momentum, slope_momentum = [state[part * count:(part + 1) * count] for part in range(4)]
                        packed = state[4 * count:]
                        system = ReleasedHermiteRouthian(basis, scalar, slope, constants, kappa, momentum, slope_momentum, source['outer_clock'][0] + time * source['outer_clock'][1], links)
                        include_gram = branch != 'GR'
                        tangent = system.constraint_tangent(packed, include_gram, source['endpoint_acceleration'], source['outer_clock'][1])
                        speed = tangent['packed_speed']
                        previous_state = loaded(intake / 'annular-uniform-energy-bounds-derived' / (label + '.npz'))
                        base = loaded(intake / 'annular-first-derivative-energy-derived' / (label + '.npz'))
                        adapted = loaded(intake / 'annular-boundary-adapted-energy-derived' / (label + '.npz'))
                        check(label + '_same_saved_state_and_speed', maximum(packed - previous_state['packed']) == 0 and maximum(speed - previous_state['packed_speed']) < 1e-12)
                        jets = exact_local_acceleration(system, packed, tangent, source['outer_clock'][1], include_gram)
                        gradient = system.evaluate(packed, include_gram, hessian=False)[1]
                        check(label + '_independent_canonical_gradient', maximum(jets['gradient'] - gradient) < 2e-12)
                        check(label + '_first_constraint_chain_rule', maximum(jets['first_constraint_rate'][system.free] - tangent['constraint_derivative_residual']) < 2e-11)
                        check(label + '_second_constraint_chain_rule', maximum(jets['second_constraint_rate'][system.free]) < 2e-10)
                        check(label + '_fixed_second_rates', maximum(jets['acceleration'][system.fixed] - numerical.array([jets['shift_speed_time'][0], 0.0, 0.0])) < 1e-14)
                        old_difference = maximum(jets['acceleration'] - adapted['local_ODE_acceleration'])
                        check(label + '_old_directional_ODE_sanity', old_difference < 1e-5 * max(1.0, maximum(jets['acceleration'])), old_difference)
                        if intervals == 16:
                            differences = []
                            for increment in [2e-4, 1e-4]:
                                sampled = []
                                for direction in [-1, 1]:
                                    offset = direction * increment
                                    moved = ReleasedHermiteRouthian(basis, scalar + offset * packed[system.slices[2]] + offset**2 / 2 * speed[system.slices[2]], slope + offset * packed[system.slope_slice] + offset**2 / 2 * speed[system.slope_slice], constants, kappa, momentum + offset * tangent['momentum_speed'] + offset**2 / 2 * jets['momentum_second_rate'][:count], slope_momentum + offset * tangent['slope_momentum_speed'] + offset**2 / 2 * jets['momentum_second_rate'][count:], system.outer_clock + offset * source['outer_clock'][1], links)
                                    moved_packed = packed + offset * speed + offset**2 / 2 * jets['acceleration']
                                    sampled.append(moved.evaluate(moved_packed, include_gram, hessian=False)[1])
                                second_difference = (sampled[0] + sampled[1] - 2 * gradient) / increment**2
                                differences.append(maximum(second_difference - jets['second_constraint_rate']))
                            check(label + '_independent_quadratic_path', differences[-1] < .8 * differences[0] or max(differences) < 2e-5, differences)
                        profile = flux_profile(system, packed, speed, basis.quadrature)
                        check(label + '_off_shell_flux_identity', maximum(profile['theta_r'] - profile['theta_r_predicted']) < 2e-11)
                        check(label + '_kinematic_identity', maximum(profile['kinematic_defect']) < 1e-12)
                        weak = metric_weak_reconstruction(system, packed, profile, include_gram)
                        check(label + '_actual_mass_variation_reconstructed', maximum(weak['mass_row'] - gradient[system.slices[0]]) < 2e-12)
                        check(label + '_actual_lapse_variation_reconstructed', maximum(weak['lapse_row'] - gradient[system.slices[1]]) < 2e-12)
                        endpoint = flux_profile(system, packed, speed, basis.radii[[0, -1]])
                        integration_errors = []
                        for order in [8, 12]:
                            refined = MixedActionBasis(basis.radii, order=order)
                            interior = flux_profile(system, packed, speed, refined.quadrature)
                            outer_corrected = endpoint['theta'][-1] + 2 * endpoint['strong_mismatch'][-1] / (endpoint['radius'][-1] * endpoint['F'][-1])
                            reconstructed = outer_corrected - numerical.dot(refined.quadrature_weights, interior['leading_flux_term'] + interior['remainder']) - 2 * endpoint['strong_mismatch'][0] / (endpoint['radius'][0] * endpoint['F'][0])
                            integration_errors.append(abs(float(reconstructed - endpoint['theta'][0])))
                        check(label + '_integrated_boundary_flux_identity', max(integration_errors) < 2e-11, integration_errors)
                        physical_mismatch = speed[system.slices[0]] - tangent['shift_mass_speed']
                        physical_mismatch_r = basis.face_gradient @ physical_mismatch
                        shift_projection_defect = basis.face_value @ tangent['shift_mass_speed'] - profile['bulk_flux']
                        check(label + '_physical_mismatch_preserved', maximum(physical_mismatch - adapted['mass_rate_mismatch']) < 1e-12 and maximum(tangent['shift_residual'] - adapted['full_shift_residual']) < 1e-12)
                        check(label + '_strong_vs_physical_mismatch_distinguished', maximum(profile['strong_mismatch'] - basis.face_value @ physical_mismatch - shift_projection_defect) < 1e-14)
                        envelope = metric_envelope(basis, packed[system.slices[0]], packed[system.slices[1]], speed[system.slices[0]], speed[system.slices[1]], jets['acceleration'][system.slices[0]], jets['acceleration'][system.slices[1]])
                        bounds = coefficient_bounds(envelope, include_gram)
                        boundary = boundary_bounds(envelope, bounds, scalar[[0, -1]], packed[system.slices[2]][[0, -1]], source['endpoint_acceleration'])
                        energy_root = numerical.sqrt(2 * float(adapted['energy']))
                        h2_bound = envelope['m_max'] / numerical.sqrt(envelope['m_min']) * (4 * bounds['elliptic_second'] + 16 * bounds['elliptic_error_constant']) * (energy_root + boundary['boundary_force_bound'])
                        h2_measured = norm(profile['scalar_rr'], basis.quadrature_weights)
                        check(label + '_derived_scalar_H2_bound', h2_measured <= h2_bound + 1e-10, {'measured': h2_measured, 'bound': h2_bound})
                        configuration = numerical.concatenate([scalar, slope])
                        velocity = numerical.concatenate([packed[system.slices[2]], packed[system.slope_slice]])
                        energy_zero = float((velocity @ base['full_M'] @ velocity + configuration @ base['full_K'] @ configuration) / 2)
                        q_l2_bound, w_l2_bound = numerical.sqrt(2 * energy_zero / envelope['m_min']), numerical.sqrt(2 * energy_zero / envelope['p_min'])
                        q_r_bound = float(adapted['velocity_radial_norm_upper_bound'])
                        q_sup_bound = q_l2_bound / numerical.sqrt(envelope['length']) + numerical.sqrt(envelope['length']) * q_r_bound
                        w_sup_bound = w_l2_bound / numerical.sqrt(envelope['length']) + numerical.sqrt(envelope['length']) * h2_bound
                        bulk_flux_bound = kappa * basis.radii[-1]**2 * envelope['F_max'] * q_sup_bound * w_sup_bound
                        check(label + '_bulk_flux_scalar_energy_bound', maximum(profile['bulk_flux']) <= bulk_flux_bound + 1e-10)
                        no_defect_theta_r_bound = 2 * bulk_flux_bound / (basis.radii[0]**2 * envelope['F_min']**2)
                        full_theta_r_bound = no_defect_theta_r_bound + maximum(profile['mismatch_derivative_term']) + maximum(profile['remainder'])
                        check(label + '_all_defects_kept_in_theta_R_bound', maximum(profile['theta_r']) <= full_theta_r_bound + 1e-10)
                        clock_mismatch_rate = float(endpoint['clock_log_t'][-1] - source['outer_clock'][1] / system.outer_clock)
                        record = {'label': label, 'intervals': intervals, 'branch': branch, 'time': float(time), 'new_acceleration_max': maximum(jets['acceleration']), 'old_acceleration_difference': old_difference, 'second_constraint_residual': maximum(jets['second_constraint_rate'][system.free]), 'physical_mismatch_max': maximum(physical_mismatch), 'physical_mismatch_R_max': maximum(physical_mismatch_r), 'physical_mismatch_time_max': maximum(jets['physical_mismatch_time']), 'shift_projection_defect_max': maximum(shift_projection_defect), 'clock_mismatch_rate': clock_mismatch_rate, 'profile_maxima': {name: maximum(profile[name]) for name in ['theta_r', 'leading_flux_term', 'mismatch_derivative_term', 'remainder', 'remainder_H', 'remainder_lapse', 'remainder_lapse_time', 'remainder_wave', 'hamiltonian_defect', 'lapse_defect', 'scalar_defect']}, 'scalar_H2_measured': h2_measured, 'scalar_H2_bound': float(h2_bound), 'bulk_flux_bound': float(bulk_flux_bound), 'no_defect_theta_R_bound': float(no_defect_theta_r_bound), 'full_theta_R_bound': float(full_theta_r_bound), 'analytic_second_jet_theta_time_envelope': envelope['theta_time_max'], 'new_boundary_source_bound': boundary['boundary_source_bound'], 'flux_integral_errors': integration_errors}
                        result_path = destination / (label + '.npz')
                        numerical.savez_compressed(result_path, **profile, **{'jet_' + name: value for name, value in jets.items()}, **{'weak_' + name: value for name, value in weak.items()}, physical_mismatch=physical_mismatch, physical_mismatch_r=physical_mismatch_r, full_shift_residual=tangent['shift_residual'], shift_projection_defect=shift_projection_defect)
                        artifact(result_path)
                        report['samples'].append(record)
                        save()
                        if index == steps:
                            print(json.dumps(record), flush=True)
            for module in tuple(sys.modules.values()):
                filename = getattr(module, '__file__', None)
                if filename:
                    path = Path(filename).resolve()
                    if path.parent == root / 'scripts' and path.suffix == '.py':
                        own(path)
            check('all_inherited_sources_preserved', all(digest(root / name) == expected for name, expected in inputs.items()))
            check('all_inherited_outputs_preserved', all(digest(root / name) == expected for name, expected in outputs.items()))
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
    if report['state'] != 'complete' or report['passed'] != report['total'] or not (destination / 'COMPLETE').is_file():
        raise RuntimeError('Metric jet gate incomplete.')
    inherit(inputs, report['inputs'])
    inherit(outputs, report['outputs'])
    for path in [report_path, destination / 'COMPLETE', destination / 'executed-script.py']:
        own(path)
    note = root / 'DERIVATION-20260909-metric-flux-cancellation-and-exact-constraint-jets.md'
    cited = [value for value in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')) if value.endswith(('.py', '.json', '.md', '.npz'))]
    missing = [value for value in cited if root / value != final_path and not (root / value).is_file()]
    if missing:
        raise FileNotFoundError(str(missing))
    own(note)
    snapshot = intake / 'annular-metric-flux-jets-resume-snapshot.md'
    with snapshot.open('xb') as handle:
        handle.write((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    artifact(snapshot)
    frozen = root.parent / 'formalization-workbench'
    since = datetime(2026, 9, 9, 17, 10, 0, tzinfo=timezone.utc).timestamp()
    touched = [str(path.relative_to(frozen)) for path in frozen.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if touched or (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Protected workbench or cache check failed: ' + repr(touched))
    final = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'checks': report['total'], 'canonical_saved_states': len(report['samples']), 'compiled_scripts': scripts, 'inputs': inputs, 'outputs': outputs, 'cited_local_paths_checked': cited, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-09T17:10:00Z; not full pre-turn hash comparison', 'mutable_resume_pinned_as_snapshot': True, 'no_bytecode_cache': True, 'metric_flux_identity_with_all_defects_derived': True, 'canonical_local_second_constraint_jets_derived': True, 'mesh_uniform_coupled_metric_bootstrap_closed': False, 'full_coupled_DAE_solved': False, 'valid_for_physics_claim': False}
    with final_path.open('x') as handle:
        json.dump(final, handle, indent=2)
        handle.write('\n')
    print(json.dumps({name: final[name] for name in ['state', 'checks', 'canonical_saved_states', 'protected_workbench_files_written_since_turn_start']}), flush=True)


if __name__ == '__main__':
    run()
