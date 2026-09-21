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
    from annular_adm_mixed_action_20260909 import MixedActionBasis
    from annular_first_derivative_energy_20260909 import canonical_matrices
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian
    from annular_spatial_clock_energy_20260909 import energy as spatial_energy
    from annular_paired_variational_energy_20260910 import frozen_spatial_growth, graph_operators, higher_energy, higher_work, paired_work, spatial_forms

    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['derive', 'seal'])
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260909'
    new_intake = root / 'source-intake/navier-stokes/20260910'
    destination = new_intake / 'annular-paired-variational-energy-derived'
    final_path = new_intake / 'annular-paired-variational-energy-final-integrity.json'
    prior_path = intake / 'annular-spatial-clock-energy-final-integrity.json'
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

    prior = json.loads(prior_path.read_text())
    if prior['state'] != 'complete':
        raise RuntimeError('Previous source gate incomplete.')
    inherit(inputs, prior['inputs'])
    inherit(outputs, prior['outputs'])
    own(prior_path)
    for name in ['annular_paired_variational_energy_20260910.py', 'derive_annular_paired_variational_energy_20260910.py']:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    if args.phase == 'derive':
        destination.mkdir(parents=True, exist_ok=False)
        (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())
        report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': inputs, 'outputs': outputs, 'checks': [], 'samples': [], 'frozen_controls': [], 'paired_variational_identity_derived': True, 'positive_boundary_adapted_graph_energy_constructed': True, 'same_H_as_previous_second_source_gate': True, 'frozen_principal_cancellation_exact_algebra': True, 'mesh_uniform_moving_graph_growth_bound_proved': False, 'mesh_uniform_boundary_source_bound_proved': False, 'raw_broken_energy_uniform_equivalence_proved': False, 'full_evolution_closed': False, 'valid_for_physics_claim': False}

        def save():
            (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

        def check(name, passed, detail=None):
            report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
            if not passed:
                raise RuntimeError('Failed check: ' + name + ' ' + repr(detail))

        def close(name, first, second, tolerance=2e-7):
            error = float(numerical.max(abs(numerical.asarray(first) - second)))
            scale = 1 + float(numerical.max(abs(numerical.asarray(second))))
            check(name, error <= tolerance * scale, {'error': error, 'scale': scale})

        save()
        try:
            case_path = intake / 'annular-constraint-correction-initial/canonical.json'
            sample_path = intake / 'annular-spatial-clock-energy-derived/status.json'
            own(case_path)
            own(sample_path)
            case = json.loads(case_path.read_text())
            constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
            kappa = float(symbolic.sympify(case['normalization_kappa']))
            parents = json.loads(sample_path.read_text())['samples']
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
                base = loaded(intake / 'annular-first-derivative-energy-derived' / (label + '.npz'))
                boundary = loaded(intake / 'annular-H1-clock-energy-derived' / (label + '.npz'))
                old = loaded(intake / 'annular-spatial-clock-energy-derived' / (label + '.npz'))
                basis = MixedActionBasis(source['radius'])
                count = basis.radii.size
                time, state = trajectory['time'][index], trajectory['state'][index]
                scalar, slope, momentum, slope_momentum = [state[part * count:(part + 1) * count] for part in range(4)]
                packed, speed = state[4 * count:], old['packed_speed']
                include_gram = branch != 'GR'
                system = ReleasedHermiteRouthian(basis, scalar, slope, constants, kappa, momentum, slope_momentum, source['outer_clock'][0] + time * source['outer_clock'][1], MetricLinkQuadrature(basis))
                matrices = canonical_matrices(system, packed, speed, include_gram)
                configuration = numerical.concatenate([scalar, slope])
                velocity = numerical.concatenate([packed[system.slices[2]], packed[system.slope_slice]])
                acceleration = numerical.concatenate([speed[system.slices[2]], speed[system.slope_slice]])
                forms = spatial_forms(system, packed, speed)
                free = base['free']
                selection = numerical.ix_(free, free)
                mass, stiffness, mass_time, stiffness_time = [matrices[name][selection] for name in ['M', 'K', 'M_dot', 'K_dot']]
                for name in ['M', 'K', 'M_dot', 'K_dot']:
                    close(label + '_unchanged_' + name, matrices[name][selection], base[name])
                check(label + '_every_slope_stays_free', set(range(count, 2 * count)).issubset(set(free)))
                close(label + '_original_endpoint_accelerations', acceleration[[0, count - 1]], source['endpoint_acceleration'])
                mapped_energy = .5 * (configuration @ forms['S'] @ configuration + velocity @ forms['T'] @ velocity)
                close(label + '_quadratic_form_is_actual_broken_energy', mapped_energy, sum(old['energy_levels']))
                close(label + '_actual_w_derivatives_reconstructed', numerical.einsum('kij,j->ki', forms['scalar_maps'][1:4], configuration), old['w'])
                close(label + '_actual_v_derivatives_reconstructed', numerical.einsum('kij,j->ki', forms['normalized_maps'], velocity), old['v'])
                work = paired_work(forms, matrices, configuration, velocity, acceleration, free)
                close(label + '_same_free_Euler_residual', work['free_Euler'], base['force_scalar_equation_residual'])
                close(label + '_variational_rate_matches_broken_segment_rate', work['variational_rate'], sum(old['direct_rate_levels']))
                old_pair = sum(numerical.sum(old[name]) for name in ['outer_flux_levels', 'interface_flux_levels', 'residual_work_levels', 'quadrature_ibp_levels'])
                close(label + '_complete_signed_pair_through_actual_free_rows', work['variational_rate'] - sum(old['reaction_levels']), old_pair)
                residual_force = base['force_nonlinear'] + base['force_scalar_equation_residual']
                higher = higher_work(mass, stiffness, mass_time, stiffness_time, base['displacement'], base['velocity'], base['velocity_time'], boundary['boundary_force'], boundary['boundary_force_time'], residual_force)
                close(label + '_same_H_not_new_regularity_norm', numerical.sqrt(2 * higher['energy']), parent['previous_H'])
                close(label + '_same_boundary_adapted_graph', higher['graph'], boundary['graph'])
                close(label + '_derived_graph_equation', higher['graph_time_error'], 0.)
                close(label + '_derived_graph_velocity_equation', higher['graph_velocity_time_error'], 0.)
                close(label + '_higher_energy_exact_work', higher['direct_rate'], higher['transport_work'] + higher['source_work'])
                epsilon = 1e-25
                moved_energy = higher_energy(mass + 1j * epsilon * mass_time, stiffness + 1j * epsilon * stiffness_time, base['displacement'] + 1j * epsilon * base['velocity'], base['velocity'] + 1j * epsilon * base['velocity_time'], boundary['boundary_force'] + 1j * epsilon * boundary['boundary_force_time'])[0]
                close(label + '_complex_differentiation_higher_energy', moved_energy.imag / epsilon, higher['direct_rate'])
                check(label + '_finite_mesh_higher_energy_inequality', higher['direct_rate'] <= higher['rate_upper'] + 1e-6)
                check(label + '_source_Cauchy_inequality', abs(higher['source_work']) <= numerical.sqrt(2 * higher['energy']) * higher['source_norm'] + 1e-6)
                correction, correction_rate = higher['energy'] - float(mapped_energy), higher['direct_rate'] - work['variational_rate']
                close(label + '_signed_pair_corrected_energy_identity', higher['direct_rate'] - correction_rate - sum(old['reaction_levels']), old_pair)
                scalar_summary = {name: value for name, value in higher.items() if isinstance(value, float)}
                paired_summary = {name: value for name, value in work.items() if isinstance(value, float)}
                report['samples'].append({'label': label, 'intervals': intervals, 'branch': branch, 'time': float(time), 'spatial_energy': float(mapped_energy), 'old_full_pair': float(old_pair), 'paired': paired_summary, 'higher': scalar_summary, 'correction': correction, 'correction_rate': correction_rate, 'frozen_control_is_not_a_new_solution': True})
                output = destination / (label + '.npz')
                numerical.savez_compressed(output, test=work['test'], free_Euler=work['free_Euler'], graph=higher['graph'], graph_velocity=higher['graph_velocity'], source_configuration=higher['source_configuration'], source_velocity=higher['source_velocity'], correction=correction, correction_rate=correction_rate, physical_mismatch=old['old_physical_mismatch'], full_shift_residual=old['full_shift_residual'])
                artifact(output)
                if index == steps:
                    raw = frozen_spatial_growth(forms['S'][selection], forms['T'][selection], mass, stiffness)
                    control_configuration, control_velocity = raw['configuration'], raw['velocity']
                    control_energy = .5 * (control_configuration @ forms['S'][selection] @ control_configuration + control_velocity @ forms['T'][selection] @ control_velocity)
                    control_rate = control_velocity @ raw['defect'] @ control_configuration
                    close(label + '_frozen_witness_spatial_energy_normalized', control_energy, 1., tolerance=1e-5)
                    close(label + '_frozen_witness_achieves_positive_rate', control_rate, raw['max_logarithmic_energy_rate'], tolerance=1e-5)
                    check(label + '_raw_broken_energy_not_frozen_symmetrizer', control_rate > 1.)
                    frozen = graph_operators(mass, stiffness, numerical.zeros_like(mass), numerical.zeros_like(stiffness))
                    close(label + '_frozen_graph_transport_is_exact_zero', frozen['growth_rate'], 0.)
                    graph_control = frozen['L'] @ control_configuration
                    velocity_control = frozen['L'] @ control_velocity
                    first_cross = graph_control @ stiffness @ velocity_control
                    second_cross = -velocity_control @ stiffness @ graph_control
                    check(label + '_actual_Gram_graph_principal_cancels', abs(first_cross + second_cross) <= 1e-9 * (1 + abs(first_cross) + abs(second_cross)))
                    numerical.savez_compressed(destination / (tag + '_frozen-witness.npz'), configuration=control_configuration, velocity=control_velocity, free=free, mass=mass, stiffness=stiffness)
                    artifact(destination / (tag + '_frozen-witness.npz'))
                    report['frozen_controls'].append({'tag': tag, 'spatial_positive_log_rate': float(control_rate / control_energy), 'graph_log_rate': 0., 'principal_cancellation_roundoff': float(first_cross + second_cross), 'scope': 'Algebraic frozen-coefficient homogeneous-boundary operator control, not a coupled constrained trajectory or admissible perturbation certificate.'})
                    print(json.dumps({'label': label, 'H_energy': higher['energy'], 'H_rate': higher['direct_rate'], 'growth': higher['growth_rate'], 'source': higher['source_norm'], 'frozen_raw_growth': raw['max_logarithmic_energy_rate']}), flush=True)
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
        raise RuntimeError('Paired variational energy validation incomplete.')
    inherit(inputs, report['inputs'])
    inherit(outputs, report['outputs'])
    for path in [report_path, destination / 'COMPLETE', destination / 'executed-script.py']:
        own(path)
    note = root / 'DERIVATION-20260910-paired-variational-work-and-graph-energy-correction.md'
    cited = [value for value in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')) if value.endswith(('.py', '.md', '.json', '.npz'))]
    missing = [value for value in cited if root / value != final_path and not (root / value).is_file()]
    if missing:
        raise FileNotFoundError(str(missing))
    own(note)
    snapshot = new_intake / 'annular-paired-variational-energy-resume-snapshot.md'
    with snapshot.open('xb') as handle:
        handle.write((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    artifact(snapshot)
    frozen = root.parent / 'formalization-workbench'
    since = datetime(2026, 9, 9, 23, 45, 0, tzinfo=timezone.utc).timestamp()
    touched = [str(path.relative_to(frozen)) for path in frozen.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if touched or (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Protected workbench/cache check failed: ' + repr(touched))
    final = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'checks': report['total'], 'saved_states': len(report['samples']), 'frozen_controls': len(report['frozen_controls']), 'inputs': inputs, 'outputs': outputs, 'cited_local_paths_checked': cited, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-09T23:45:00Z, not a full pre-turn hash baseline', 'no_bytecode_cache': True, 'paired_identity_and_graph_correction_derived': True, 'moving_mesh_uniform_bound_open': True, 'full_evolution_closed': False, 'valid_for_physics_claim': False}
    with final_path.open('x') as handle:
        json.dump(final, handle, indent=2)
        handle.write('\n')
    print(json.dumps({name: final[name] for name in ['state', 'checks', 'saved_states', 'frozen_controls', 'protected_workbench_files_written_since_turn_start']}), flush=True)


if __name__ == '__main__':
    run()
