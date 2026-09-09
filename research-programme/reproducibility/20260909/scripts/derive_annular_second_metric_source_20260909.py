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
    from annular_action_boundary_current_20260909 import changed_system
    from annular_adm_mixed_action_20260909 import MixedActionBasis
    from annular_clock_spatial_bound_20260909 import spatial_bounds
    from annular_metric_flux_jets_20260909 import SecondJet, canonical_constraint_jet
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_metric_schur_bound_20260909 import schur_blocks
    from annular_metric_source_bound_20260909 import scalar_source_data
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian
    from annular_second_metric_source_20260909 import independent_second_forcing, second_source_bound

    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['derive', 'seal'])
    parser.add_argument('--name', default='annular-second-metric-source-derived')
    args = parser.parse_args()
    if Path(args.name).name != args.name:
        raise ValueError('Result name must be a single path component.')
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260909'
    destination = intake / args.name
    final_path = intake / 'annular-second-metric-source-final-integrity.json'
    prior_path = intake / 'annular-H1-clock-energy-final-integrity.json'
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
        raise RuntimeError('Previous H1 energy gate incomplete.')
    inherit(inputs, prior['inputs'])
    inherit(outputs, prior['outputs'])
    own(prior_path)
    for name in ['annular_second_metric_source_20260909.py', 'derive_annular_second_metric_source_20260909.py']:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    if args.phase == 'derive':
        destination.mkdir(exist_ok=False)
        (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())
        report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': inputs, 'outputs': outputs, 'checks': [], 'samples': [], 'manufactured': [], 'second_source_and_inner_flux_derivative_bound_derived': True, 'T2_bound_condition': 'Canonical configuration box, lower graph radius and higher spatial radius H=sqrt(||g_hat||K^2+||M^-1 K z||M^2), retained equation residuals and actual boundary histories. H is not proved uniformly bounded in time.', 'higher_spatial_energy_evolution_derived': False, 'lower_energy_alone_suffices': False, 'lower_energy_alone_impossible_proved': False, 'energy_evolution_or_box_persistence_closed': False, 'full_coupled_DAE_solved': False, 'valid_for_physics_claim': False}

        def save():
            (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

        def check(name, passed, detail=None):
            report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
            if not passed:
                raise RuntimeError('Failed check: ' + name + ' ' + repr(detail))

        def norm(values, weights):
            return float(numerical.sqrt(max(0.0, weights @ values**2)))

        def dual(vector, matrix):
            return float(numerical.sqrt(max(0.0, vector @ numerical.linalg.solve(matrix, vector))))

        def close(label, left, right, tolerance=2e-8):
            error = float(numerical.max(abs(left - right)))
            scale = 1 + float(numerical.max(abs(right)))
            check(label, error <= tolerance * scale, {'error': error, 'scale': scale})

        save()
        try:
            case_path = intake / 'annular-constraint-correction-initial/canonical.json'
            own(case_path)
            case = json.loads(case_path.read_text())
            constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
            kappa = float(symbolic.sympify(case['normalization_kappa']))
            parent_path = intake / 'annular-H1-clock-energy-derived/status.json'
            inner_path = intake / 'annular-inner-shift-trace-certified/status.json'
            own(parent_path)
            own(inner_path)
            parents = json.loads(parent_path.read_text())['samples']
            inner_rows = {row['label']: row for row in json.loads(inner_path.read_text())['samples']}
            for parent in parents:
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
                adapted = loaded(intake / 'annular-H1-clock-energy-derived' / (label + '.npz'))
                scalar_data = scalar_source_data(system, packed, include_gram, source['endpoint_acceleration'])
                blocks = schur_blocks(system, packed, include_gram)
                free = scalar_data['free']
                mass, stiffness = base['M'], base['K']
                graph_q = numerical.linalg.solve(mass, stiffness @ base['velocity'])
                higher_squared = float(adapted['graph'] @ stiffness @ adapted['graph'] + graph_q @ mass @ graph_q)
                higher = numerical.sqrt(max(0.0, higher_squared))
                raw_radius = parent['raw_energy_root_upper_from_adapted']
                upper_scalar = dict(scalar_data, energy=raw_radius**2 / 2)
                inner_bound = inner_rows[label]['all_grid_shift_bound']
                first = spatial_bounds(system, upper_scalar, spatial['mass_static_residual'], spatial['mass_time_residual'], inner_bound, source['outer_clock'][1], source['endpoint_acceleration'], include_gram)
                endpoints = {'position': scalar[[0, -1]], 'velocity': packed[system.slices[2]][[0, -1]], 'acceleration': source['endpoint_acceleration']}
                independent = independent_second_forcing(system, packed, speed, include_gram)
                known = numerical.concatenate([independent['metric_mass'], independent['metric_lapse'], independent['velocity']])
                close(label + '_independent_full_second_source', known[system.free], jets['jet_known_second_forcing'][system.free])
                close(label + '_physical_scalar_acceleration_identity', (numerical.concatenate([speed[system.slices[2]], speed[system.slope_slice]]) - base['lift_acceleration'])[free], -adapted['graph'] - numerical.linalg.solve(mass, base['M_dot'] @ base['velocity']) + numerical.linalg.solve(mass, base['force_scalar_equation_residual']))
                epsilon = 1e-25
                moved = changed_system(system, packed, tangent, 1j * epsilon, source['outer_clock'][1])
                moved_shift = moved.shift_mass_velocity(packed + 1j * epsilon * speed, include_gram)
                shift, pairing, matter, gram = system.shift_mass_velocity(packed, include_gram)
                shift_time, pairing_time, matter_time, gram_time = [item.imag / epsilon for item in moved_shift]
                close(label + '_independent_actual_shift_time', shift_time, jets['jet_shift_speed_time'])
                widths = numerical.diff(basis.faces)
                stars = numerical.concatenate([widths, [0.]]) + numerical.concatenate([[0.], widths])
                shift_time_error = pairing @ shift_time + pairing_time @ shift + matter_time - gram_time
                defect = float(max(abs(shift_time_error) / stars))
                lift = numerical.zeros_like(packed)
                lift[system.slices[0]] = shift_time[0]
                metric_indices, velocity_indices = blocks['metric_indices'], blocks['velocity_indices']
                coupling, scalar_mass = blocks['coupling'], blocks['scalar_mass']
                lifted = blocks['jacobian'] @ lift
                effective = -known[metric_indices] + coupling @ numerical.linalg.solve(scalar_mass, known[velocity_indices]) - lifted[metric_indices] + coupling @ numerical.linalg.solve(scalar_mass, lifted[velocity_indices])
                response_vector = jets['jet_acceleration'][metric_indices] - lift[metric_indices]
                second_residual = blocks['schur'] @ response_vector - effective
                error_dual = dual(second_residual, blocks['metric_norm'])
                close(label + '_actual_second_Schur_equation', blocks['schur'] @ response_vector, effective)
                bound = second_source_bound(first, parent['bounds'], raw_radius, higher, endpoints, inner_bound, include_gram, float(adapted['residual_force_K_graph_norm']), defect, error_dual)
                weights = basis.quadrature_weights
                for name in ['gravity_mass', 'kinetic_mass', 'gradient_mass', 'flux_mass', 'gravity_lapse', 'kinetic_lapse', 'gradient_lapse']:
                    measured = norm(independent[name], weights)
                    check(label + '_' + name + '_L2_majorant', measured <= bound[name] + 1e-9, {'measured': measured, 'bound': bound[name]})
                for name in ['atom_mass', 'atom_lapse']:
                    measured = float(numerical.linalg.norm(independent[name]) / numerical.sqrt(basis.spacing))
                    check(label + '_' + name + '_dual_majorant', measured <= bound[name] + 1e-9)
                rho_second = float(numerical.linalg.norm(independent['rho_second']) / numerical.sqrt(basis.spacing))
                check(label + '_actual_Gram_second_density_bound', rho_second <= bound['rho_second_dual'] + 1e-9)
                check(label + '_acceleration_H1_bound', norm(independent['a_radial'], weights) <= bound['acceleration_radial_L2'] + 1e-9)
                check(label + '_acceleration_L2_bound', norm(independent['a_value'], weights) <= bound['acceleration_L2'] + 1e-9)
                check(label + '_q_gradient_quadrature_control', max(abs(independent['q_radial'])) <= bound['q_radial_sup'] + 1e-9)
                check(label + '_bulk_shift_derivative_density', max(abs(matter_time) / stars) <= bound['matter_shift_time_density'] / 2 + 1e-9)
                check(label + '_Gram_shift_derivative_density', max(abs(gram_time) / stars) <= bound['Gram_shift_time_density'] / 2 + 1e-9)
                check(label + '_pairing_shift_derivative_density', max(abs(pairing_time @ shift) / stars) <= bound['pairing_shift_time_density'] / 2 + 1e-9)
                check(label + '_entire_shift_derivative_and_inner_trace', max(abs(shift_time)) <= bound['inner_shift_second_bound'] + 1e-9)
                mass_count = system.node_count
                metric_mass_norm = dual(independent['metric_mass'][1:], blocks['mass_norm'])
                metric_lapse_norm = float(numerical.linalg.norm(independent['metric_lapse']) / numerical.sqrt(basis.spacing))
                velocity_norm = dual(known[velocity_indices], scalar_mass)
                check(label + '_second_metric_mass_functional', metric_mass_norm <= bound['metric_mass_dual'] + 1e-9)
                check(label + '_second_metric_lapse_functional', metric_lapse_norm <= bound['metric_lapse_dual'] + 1e-9)
                check(label + '_second_velocity_functional', velocity_norm <= bound['velocity_force_dual'] + 1e-9)
                check(label + '_effective_second_source_mass_bound', dual(effective[:mass_count], blocks['mass_norm']) <= bound['source_mass_dual'] + 1e-9)
                check(label + '_effective_second_source_lapse_bound', numerical.linalg.norm(effective[mass_count:]) / numerical.sqrt(basis.spacing) <= bound['source_lapse_dual'] + 1e-9)
                response_norm = float(numerical.sqrt(response_vector @ blocks['metric_norm'] @ response_vector))
                check(label + '_derived_second_metric_response', response_norm <= bound['second_metric_response'] + 1e-9)
                theta_time_norm = norm(adapted['theta_time'], weights)
                check(label + '_T2_bound_without_second_metric_input', theta_time_norm <= bound['theta_time_Q_L2_bound'] + 1e-9)
                first_zero = second_source_bound(first, parent['bounds'], raw_radius, 0.0, endpoints, inner_bound, include_gram, float(adapted['residual_force_K_graph_norm']), defect, error_dual)
                first_unit = second_source_bound(first, parent['bounds'], raw_radius, 1.0, endpoints, inner_bound, include_gram, float(adapted['residual_force_K_graph_norm']), defect, error_dual)
                offset = first_zero['theta_time_Q_L2_bound']
                source_slope = numerical.hypot(first_unit['source_mass_dual'] - first_zero['source_mass_dual'], first_unit['source_lapse_dual'] - first_zero['source_lapse_dual'])
                slope_bound = (175 / 118) * source_slope * (1 / .8 + .25 / ((47 / 8) * .65))
                slope_bound += .5 / ((47 / 8) * .65) * (first_unit['inner_shift_second_bound'] - first_zero['inner_shift_second_bound'])
                for trial in [0.1, 10., 100.]:
                    trial_bound = second_source_bound(first, parent['bounds'], raw_radius, trial, endpoints, inner_bound, include_gram, float(adapted['residual_force_K_graph_norm']), defect, error_dual)
                    check(label + '_subadditive_affine_H_majorant_' + str(trial), trial_bound['theta_time_Q_L2_bound'] <= offset + slope_bound * trial + 1e-7)
                check(label + '_old_physical_mismatch_and_boundary_preserved', numerical.array_equal(jets['jet_physical_mismatch_time'], adapted['physical_mismatch_time']) and numerical.array_equal(speed, spatial['packed_speed']) and numerical.array_equal(tangent['shift_residual'], adapted['full_shift_residual']))
                if intervals == 16 and index == 0:
                    for multiplier in [0., -1., 2.]:
                        trial_speed = multiplier * speed
                        trial = independent_second_forcing(system, packed, trial_speed, include_gram, clock_second=.005)
                        configuration = SecondJet(numerical.concatenate([system.scalar, system.slope]), scalar_data['velocity'], numerical.concatenate([trial_speed[system.slices[2]], trial_speed[system.slope_slice]]))
                        from annular_first_derivative_energy_20260909 import canonical_matrices
                        trial_matrices = canonical_matrices(system, packed, trial_speed, include_gram)
                        force_second = -(trial_matrices['K_dot'] @ scalar_data['configuration'] + trial_matrices['K'] @ scalar_data['velocity'])
                        momenta_jet = SecondJet(numerical.concatenate([momentum, slope_momentum]), 0., force_second)
                        clock_jet = SecondJet(system.outer_clock, source['outer_clock'][1], .005)
                        jet = canonical_constraint_jet(system, SecondJet(packed, trial_speed), configuration, momenta_jet, clock_jet, include_gram)
                        full_trial = numerical.concatenate([trial['metric_mass'], trial['metric_lapse'], trial['velocity']])
                        control_label = label + '_off_shell_rate_multiplier_' + str(multiplier)
                        close(control_label + '_independent_second_jet', full_trial, jet.second)
                        check(control_label + '_outer_clock_second_retained', abs((trial['metric_mass'] - independent_second_forcing(system, packed, trial_speed, include_gram)['metric_mass'])[-1] + .005 / kappa) < 1e-12)
                        report['manufactured'].append({'label': control_label, 'clock_second': .005, 'rate_multiplier': multiplier, 'scope': 'Off-shell algebraic control, not a physical trajectory.'})
                output = destination / (label + '.npz')
                numerical.savez_compressed(output, **independent, effective_second_source=effective, actual_response=response_vector, second_Schur_residual=second_residual, shift_time=shift_time, shift_time_residual=shift_time_error, higher_graph_velocity=graph_q, theta_time=adapted['theta_time'], physical_mismatch_time=jets['jet_physical_mismatch_time'], full_shift_residual=adapted['full_shift_residual'])
                artifact(output)
                row = {'label': label, 'intervals': intervals, 'branch': branch, 'time': float(time), 'raw_radius_upper': raw_radius, 'higher_spatial_radius': float(higher), 'higher_spatial_energy': higher_squared / 2, 'first_bounds': first, 'bounds': bound, 'theta_time_bound_affine_offset': offset, 'theta_time_bound_affine_slope': slope_bound, 'measured': {'theta_time_Q_L2': theta_time_norm, 'inner_shift_second': float(shift_time[0]), 'shift_second_sup': float(max(abs(shift_time))), 'effective_source_dual': dual(effective, blocks['metric_norm']), 'second_metric_response': response_norm, 'scalar_acceleration_radial_L2': norm(independent['a_radial'], weights), 'second_response_residual_dual': error_dual}, 'higher_energy_time_uniform_bound_proved': False}
                report['samples'].append(row)
                save()
                if index == steps:
                    print(json.dumps({'label': label, 'H': float(higher), 'T2_measured': theta_time_norm, 'T2_bound': bound['theta_time_Q_L2_bound'], 'inner_second_bound': bound['inner_shift_second_bound']}), flush=True)
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
        raise RuntimeError('Second source validation incomplete.')
    inherit(inputs, report['inputs'])
    inherit(outputs, report['outputs'])
    for path in [report_path, destination / 'COMPLETE', destination / 'executed-script.py']:
        own(path)
    note = root / 'DERIVATION-20260909-second-metric-source-and-clock-acceleration-bound.md'
    cited = [value for value in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')) if value.endswith(('.py', '.md', '.json', '.npz'))]
    missing = [value for value in cited if root / value != final_path and not (root / value).is_file()]
    if missing:
        raise FileNotFoundError(str(missing))
    own(note)
    snapshot = intake / 'annular-second-metric-source-resume-snapshot.md'
    with snapshot.open('xb') as handle:
        handle.write((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    artifact(snapshot)
    frozen = root.parent / 'formalization-workbench'
    since = datetime(2026, 9, 9, 21, 55, 0, tzinfo=timezone.utc).timestamp()
    touched = [str(path.relative_to(frozen)) for path in frozen.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if touched or (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Protected workbench/cache check failed: ' + repr(touched))
    final = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'checks': report['total'], 'saved_states': len(report['samples']), 'manufactured_cases': len(report['manufactured']), 'inputs': inputs, 'outputs': outputs, 'cited_local_paths_checked': cited, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-09T21:55:00Z, not full pre-turn hash baseline', 'mutable_resume_pinned_as_snapshot': True, 'no_bytecode_cache': True, 'second_metric_source_and_inner_flux_derivative_bounds_derived': True, 'clock_time_derivative_bound_conditional_on_higher_spatial_radius': True, 'higher_spatial_energy_evolution_and_box_persistence_closed': False, 'valid_for_physics_claim': False}
    with final_path.open('x') as handle:
        json.dump(final, handle, indent=2)
        handle.write('\n')
    print(json.dumps({name: final[name] for name in ['state', 'checks', 'saved_states', 'manufactured_cases', 'protected_workbench_files_written_since_turn_start']}), flush=True)


if __name__ == '__main__':
    run()
