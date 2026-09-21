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
    from scipy.linalg import solve
    from annular_adm_mixed_action_20260909 import MixedActionBasis, coefficient_jets
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian
    from annular_first_derivative_energy_20260909 import canonical_matrices
    from annular_metric_flux_jets_20260909 import SecondJet, canonical_constraint_jet
    from annular_boundary_source_variation_20260910 import parent_third_jet, shift_second_jet, boundary_source, endpoint_time_data, variation_bound
    from annular_uniform_energy_bounds_20260909 import projection_map
    from annular_spatial_clock_energy_20260909 import profile

    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['derive', 'seal'])
    parser.add_argument('--attempt', default='derived')
    arguments = parser.parse_args()
    if not re.fullmatch('[a-z0-9-]+', arguments.attempt):
        raise ValueError('Invalid attempt identifier.')
    root = Path(__file__).resolve().parents[1]
    old = root / 'source-intake/navier-stokes/20260909'
    intake = root / 'source-intake/navier-stokes/20260910'
    destination = intake / ('annular-boundary-source-variation-' + arguments.attempt)
    prior_path = intake / 'annular-regular-transport-bound-final-integrity.json'
    final_path = intake / 'annular-boundary-source-variation-final-integrity.json'
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
        raise RuntimeError('Previous gate incomplete.')
    inherit(inputs, prior['inputs'])
    inherit(outputs, prior['outputs'])
    own(prior_path)
    for name in ['annular_boundary_source_variation_20260910.py', 'derive_annular_boundary_source_variation_20260910.py']:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    if arguments.phase == 'derive':
        destination.mkdir(exist_ok=False)
        (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())
        report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': inputs, 'outputs': outputs, 'checks': [], 'samples': [], 'third_parent_jet_from_original_constraints': True, 'old_and_repacked_boundary_derivatives_derived': True, 'complete_forcing_unchanged': True, 'conditional_repacked_source_variation_bound_derived': True, 'old_beta_uniform_BV_proved': False, 'actual_time_interval_TV_upper_proved': False, 'parent_uniform_inverse_Jacobian_bound_proved': False, 'new_physical_evolution': False, 'valid_for_physics_claim': False}

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

        def polynomial_jet(orders, time):
            return SecondJet(orders[0] + time * orders[1] + time**2 * orders[2] / 2 + time**3 * orders[3] / 6, orders[1] + time * orders[2] + time**2 * orders[3] / 2, orders[2] + time * orders[3])

        save()
        try:
            case_path = old / 'annular-constraint-correction-initial/canonical.json'
            parent_path = intake / 'annular-regular-transport-bound-attempt02/status.json'
            own(case_path)
            own(parent_path)
            case = json.loads(case_path.read_text())
            constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
            kappa = float(symbolic.sympify(case['normalization_kappa']))
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
                boundary = loaded(old / 'annular-H1-clock-energy-derived' / (label + '.npz'))
                old_trace = loaded(intake / 'annular-boundary-source-trace-law-derived' / (label + '.npz'))
                pair = loaded(intake / 'annular-paired-variational-energy-derived-attempt03' / (label + '.npz'))
                folder = 'annular-boundary-N64-evolution-smoke' if intervals == 64 else 'annular-released-Hermite-evolution-smoke'
                trajectory = loaded(old / folder / (tag + '_steps' + str(steps) + '.npz'))
                basis = MixedActionBasis(initial['radius'])
                count = basis.radii.size
                time, state = trajectory['time'][index], trajectory['state'][index]
                scalar, slope, momentum, slope_momentum = [state[part * count:(part + 1) * count] for part in range(4)]
                packed, speed, second = state[4 * count:], spatial['packed_speed'], jets['jet_acceleration']
                clock_rate = initial['outer_clock'][1]
                system = ReleasedHermiteRouthian(basis, scalar, slope, constants, kappa, momentum, slope_momentum, initial['outer_clock'][0] + time * clock_rate, MetricLinkQuadrature(basis))
                include_gram = branch != 'GR'
                parent = parent_third_jet(system, packed, speed, second, clock_rate, include_gram)
                third = parent['third']
                direct_matrices = canonical_matrices(system, packed, speed, include_gram)
                step = 1e-25
                shifted = canonical_matrices(system, packed + 1j * step * speed, speed + 1j * step * second, include_gram)
                for name in ['M', 'K']:
                    close(label + '_' + name + '_original_matrix', parent['matrices'][name].value, direct_matrices[name])
                    close(label + '_' + name + '_original_first_rate', parent['matrices'][name].first, direct_matrices[name + '_dot'])
                    close(label + '_' + name + '_second_rate_by_complex_step', parent['matrices'][name].second, shifted[name + '_dot'].imag / step)
                close(label + '_old_momentum_second_jet_preserved', parent['momentum_second'], jets['jet_momentum_second_rate'])
                direct_shift = system.shift_mass_velocity(packed, include_gram)
                close(label + '_original_shift_projection', parent['shift']['speed'].value, direct_shift[0])
                close(label + '_original_shift_pairing', parent['shift']['pairing'].value, direct_shift[1])
                close(label + '_original_shift_Gram_current', parent['shift']['Gram'].value, direct_shift[3])
                close(label + '_original_shift_first_rate_preserved', parent['shift']['speed'].first, jets['jet_shift_speed_time'])
                moved = ReleasedHermiteRouthian(basis, scalar + 1j * step * packed[system.slices[2]], slope + 1j * step * packed[system.slope_slice], constants, kappa, momentum + 1j * step * parent['momentum_rate'][:count], slope_momentum + 1j * step * parent['momentum_rate'][count:], system.outer_clock + 1j * step * clock_rate, system.links)
                moved_shift = shift_second_jet(moved, packed + 1j * step * speed, speed + 1j * step * second, second, include_gram)
                close(label + '_shift_second_rate_chain_rule', parent['shift']['speed'].second, moved_shift['speed'].first.imag / step, tolerance=1e-8)
                close(label + '_old_first_constraint_jet_preserved', parent['first_constraint_residual'], jets['jet_first_constraint_rate'])
                close(label + '_old_second_constraint_jet_preserved', parent['second_constraint_residual'], jets['jet_second_constraint_rate'])
                residual = float(max(abs(parent['third_constraint_residual'][system.free])))
                forcing_scale = 1 + float(max(abs(parent['known_third'])))
                check(label + '_third_free_constraint_rate_solved', residual <= 2e-8 * forcing_scale, {'residual': residual, 'forcing_scale': forcing_scale})
                close(label + '_third_fixed_endpoint_jet_sourced', third[system.fixed], [parent['shift']['speed'].second[0], 0., 0.])
                check(label + '_explicit_finite_mesh_third_jet_bound', max(abs(third)) <= parent['third_sup_upper'] + 1e-8)
                errors = []
                for delta in [2e-5, 1e-5]:
                    values = []
                    for sign in [-1, 1]:
                        local_time = sign * delta
                        residual_jet = canonical_constraint_jet(system, polynomial_jet([packed, speed, second, third], local_time), polynomial_jet(parent['configuration_jet'], local_time), polynomial_jet(parent['momentum_jet'], local_time), SecondJet(system.outer_clock + local_time * clock_rate, clock_rate), include_gram)
                        values.append(residual_jet.second)
                    derivative = (values[1] - values[0]) / (2 * delta)
                    errors.append(float(max(abs(derivative[system.free] - parent['third_constraint_residual'][system.free]))))
                check(label + '_independent_cubic_path_third_constraint_control', errors[1] < .8 * errors[0] or errors[1] < 1e-5 * forcing_scale, errors)
                primitive = coefficient_jets(packed[system.slices[2]], system.gradient_node, basis.face_to_node @ packed[system.slices[0]], packed[system.slices[1]], basis.radii, constants)
                close(label + '_canonical_local_Gram_shift_derivative_zero', primitive[1][4], 0.)
                lift, lift_time, lift_second = base['lift'], base['lift_velocity'], base['lift_acceleration']
                source = boundary_source(system, packed, speed, second, include_gram, lift, lift_time, lift_second)
                rates = endpoint_time_data(system, packed, speed, second, third, source, lift, lift_time, lift_second)
                bounds = variation_bound(system, packed, speed, second, source, rates, lift, lift_time, lift_second, include_gram, parent)
                close(label + '_original_boundary_force', source['force'], boundary['boundary_force'])
                close(label + '_original_boundary_force_time', source['force_time'], boundary['boundary_force_time'])
                close(label + '_original_beta_trace_preserved', source['endpoint']['old_beta'], old_trace['derived_endpoint_coefficients'])
                close(label + '_original_complete_source_preserved', source['actual'], pair['source_configuration'])
                close(label + '_repacked_complete_source_identical', source['endpoint_lift'] @ source['endpoint']['beta'] + source['regular'], source['actual'])
                close(label + '_potential_time_from_actual_source', source['potential_time'][source['free']], -solve(base['K'], base['M'] @ source['actual'], assume_a='sym'))
                changed_source = boundary_source(system, packed + 1j * step * speed, speed + 1j * step * second, second + 1j * step * third, include_gram, lift + 1j * step * lift_time, lift_time + 1j * step * lift_second, lift_second)
                close(label + '_original_beta_derivative_by_complex_step', rates['old_beta_time'], changed_source['endpoint']['old_beta'].imag / step, tolerance=1e-8)
                close(label + '_repacked_beta_derivative_by_complex_step', rates['beta_time'], changed_source['endpoint']['beta'].imag / step, tolerance=1e-8)
                close(label + '_theta_second_rate_by_complex_step', rates['theta_tt'], changed_source['endpoint']['theta_time'].imag / step, tolerance=1e-8)
                free = source['free']
                maps = source['interior']['maps']
                theta_nodes = profile(system, packed, speed, basis.radii)['theta'][0]
                product = projection_map(basis, theta_nodes)[numerical.ix_(free, free)]
                value = maps[0][:, free]
                radial = maps[1][:, free]
                theta_q = source['interior']['theta']
                error_value = theta_q[:, None] * value - value @ product
                error_derivative = source['interior']['theta_r'][:, None] * value + theta_q[:, None] * radial - radial @ product
                weights = basis.quadrature_weights
                density = basis.quadrature**2 / source['interior']['c']
                radial_density = basis.quadrature**2 * source['interior']['c']
                full = source['potential'] + lift
                full_gram = parent['matrices']['Gram']
                weak = error_derivative.T @ (weights * radial_density * (maps[1] @ full)) - error_value.T @ (weights * density * source['xi'])
                weak += (full_gram.first @ full)[free] - product.T @ (full_gram.value @ full)[free]
                close(label + '_repacked_remainder_from_actual_weak_equation', solve(base['M'], weak, assume_a='sym'), source['weak_remainder'])
                weak_norm = float(numerical.sqrt(source['weak_remainder'] @ base['K'] @ source['weak_remainder']))
                check(label + '_repacked_remainder_has_derived_energy_bound', weak_norm <= bounds['repacked_weak_remainder_K_upper'] + 1e-8)
                check(label + '_repacked_beta_pointwise_value_bound', numerical.all(abs(source['endpoint']['beta']) <= numerical.asarray(bounds['beta_abs_endpoint_upper']) + 1e-10))
                check(label + '_repacked_beta_pointwise_rate_bound', numerical.all(abs(rates['beta_time']) <= numerical.asarray(bounds['beta_time_abs_endpoint_upper']) + 1e-9))
                check(label + '_theta_second_rate_parent_solve_bound', max(abs(rates['theta_tt'])) <= bounds['theta_tt_from_parent_solve_upper'] + 1e-8)
                check(label + '_repacked_beta_parent_solve_rate_bound', numerical.linalg.norm(rates['beta_time']) <= bounds['beta_rate_parent_solve_R2_upper'] + 1e-8)
                old_work = float(pair['graph'] @ base['K'] @ source['actual'])
                new_work = float(pair['graph'] @ base['K'] @ (source['endpoint_lift'] @ source['endpoint']['beta']) + pair['graph'] @ base['K'] @ source['regular'])
                close(label + '_all_signed_source_energy_work_retained', old_work, new_work)
                output = destination / (label + '.npz')
                numerical.savez_compressed(output, third_parent_jet=third, third_constraint_residual=parent['third_constraint_residual'], known_third=parent['known_third'], shift_second=parent['shift']['speed'].second, physical_shift_second_mismatch=third[system.slices[0]] - parent['shift']['speed'].second, momentum_third=parent['momentum_third'], old_beta=source['endpoint']['old_beta'], old_beta_time=rates['old_beta_time'], repacked_beta=source['endpoint']['beta'], repacked_beta_time=rates['beta_time'], theta_tt=rates['theta_tt'], potential=source['potential'], potential_time=source['potential_time'], weak_remainder=source['weak_remainder'], affine_quadrature=source['affine_quadrature'], repacked_regular=source['regular'], original_complete_source=source['actual'])
                artifact(output)
                row = {'label': label, 'intervals': intervals, 'branch': branch, 'time': float(time), 'third_parent_jet_max': float(max(abs(third))), 'third_parent_jet_sup_upper': parent['third_sup_upper'], 'free_inverse_infinity_norm': parent['free_inverse_infinity_norm'], 'third_constraint_residual_max': residual, 'cubic_path_errors': errors, 'old_beta': source['endpoint']['old_beta'].tolist(), 'repacked_beta': source['endpoint']['beta'].tolist(), 'old_beta_time': rates['old_beta_time'].tolist(), 'repacked_beta_time': rates['beta_time'].tolist(), 'theta_tt': rates['theta_tt'].tolist(), 'repacked_weak_remainder_K_norm': weak_norm, 'repacked_regular_K_norm': float(numerical.sqrt(source['regular'] @ base['K'] @ source['regular'])), 'bounds': bounds, 'scope': 'Original state, derived local third jet, no new evolution and no certified time-interval variation.'}
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
        raise RuntimeError('Boundary source variation validation incomplete.')
    inherit(inputs, report['inputs'])
    inherit(outputs, report['outputs'])
    for path in [report_path, destination / 'COMPLETE', destination / 'executed-script.py']:
        own(path)
    note = root / 'DERIVATION-20260910-parent-third-jet-and-boundary-source-variation.md'
    cited = [value for value in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')) if value.endswith(('.py', '.md', '.json', '.npz'))]
    missing = [value for value in cited if root / value != final_path and not (root / value).is_file()]
    if missing:
        raise FileNotFoundError(str(missing))
    own(note)
    snapshot = intake / 'annular-boundary-source-variation-resume-snapshot.md'
    with snapshot.open('xb') as handle:
        handle.write((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    artifact(snapshot)
    frozen = root.parent / 'formalization-workbench'
    since = datetime(2026, 9, 10, 2, 7, 0, tzinfo=timezone.utc).timestamp()
    touched = [str(path.relative_to(frozen)) for path in frozen.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if touched or (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Protected workbench/cache check failed: ' + repr(touched))
    final = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'checks': report['total'], 'saved_states': len(report['samples']), 'inputs': inputs, 'outputs': outputs, 'cited_local_paths_checked': cited, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-10T02:07:00Z, not a full pre-turn hash baseline', 'no_bytecode_cache': True, 'parent_third_jet_and_repacked_beta_rate_derived': True, 'actual_interval_TV_and_uniform_parent_inverse_open': True, 'valid_for_physics_claim': False}
    with final_path.open('x') as handle:
        json.dump(final, handle, indent=2)
        handle.write('\n')
    print(json.dumps({name: final[name] for name in ['state', 'checks', 'saved_states', 'protected_workbench_files_written_since_turn_start']}), flush=True)


if __name__ == '__main__':
    run()
