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
    from annular_boundary_adapted_energy_20260909 import adapted_diagnostic, local_ode_acceleration, quadratic_path_energy
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian

    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['derive', 'seal'])
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260909'
    destination = intake / 'annular-boundary-adapted-energy-derived'
    final_path = intake / 'annular-first-derivative-energy-final-integrity.json'
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

    def maximum(value):
        return float(numerical.max(numerical.abs(value)))

    gate_path = intake / 'annular-first-derivative-energy-derived/status.json'
    gate = json.loads(gate_path.read_text())
    if gate['state'] != 'complete' or gate['passed'] != gate['total'] or not (gate_path.parent / 'COMPLETE').is_file():
        raise RuntimeError('First energy identity gate incomplete.')
    inherit(inputs, gate['inputs'])
    inherit(outputs, gate['outputs'])
    for path in [gate_path, gate_path.parent / 'COMPLETE', gate_path.parent / 'executed-script.py']:
        own(path)
    scripts = ['annular_first_derivative_energy_20260909.py', 'derive_annular_first_derivative_energy_20260909.py', 'annular_boundary_adapted_energy_20260909.py', 'derive_annular_boundary_adapted_energy_20260909.py']
    for name in scripts:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    if arguments.phase == 'derive':
        destination.mkdir(exist_ok=False)
        (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())
        report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': inputs, 'outputs': outputs, 'checks': [], 'samples': [], 'uniform_energy_estimate_closed': False, 'valid_for_physics_claim': False, 'scope': 'Replace the graph acceleration by M^-1(Ku-f_boundary), where f_boundary is fixed by the unchanged Dirichlet lift. No action, evolution or boundary-offset modification. Derive exact work identity, estimate the boundary source in M-dual L2, and retain nonlinear/residual forcing. Local coefficient accelerations are numerical directional derivatives of the existing ODE, not a mesh-uniform theorem.'}

        def save():
            (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

        def check(name, passed, detail=None):
            report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
            if not passed:
                raise RuntimeError('Failed check: ' + name + ' ' + repr(detail))

        save()
        try:
            for sample in gate['samples']:
                case_name, intervals, branch = sample['case'], sample['intervals'], sample['branch']
                tag = case_name + '_N' + str(intervals) + '_' + branch
                steps = 64 if intervals == 64 else 32
                index = int(round(sample['time'] / .01 * steps))
                label = tag + '_sample' + str(index)
                report['active_job'] = label
                save()
                case_path = intake / 'annular-constraint-correction-initial' / (case_name + '.json')
                own(case_path)
                case = json.loads(case_path.read_text())
                constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
                kappa = float(symbolic.sympify(case['normalization_kappa']))
                source = loaded(intake / 'annular-released-Hermite-initial-derived' / (tag + '.npz'))
                folder = intake / ('annular-boundary-N64-evolution-smoke' if intervals == 64 else 'annular-released-Hermite-evolution-smoke')
                trajectory = loaded(folder / (tag + '_steps' + str(steps) + '.npz'))
                base = loaded(gate_path.parent / (label + '.npz'))
                basis = MixedActionBasis(source['radius'])
                links = MetricLinkQuadrature(basis)
                count = basis.radii.size
                time, state = trajectory['time'][index], trajectory['state'][index]
                scalar, slope, momentum, slope_momentum = [state[part * count:(part + 1) * count] for part in range(4)]
                packed = state[4 * count:]
                system = ReleasedHermiteRouthian(basis, scalar, slope, constants, kappa, momentum, slope_momentum, source['outer_clock'][0] + time * source['outer_clock'][1], links)
                include_gram = branch != 'GR'
                tangent = system.constraint_tangent(packed, include_gram, source['endpoint_acceleration'], source['outer_clock'][1])
                check(label + '_unchanged_full_shift_residual', maximum(tangent['shift_residual'] - trajectory['shifts'][index]) < 1e-13)
                acceleration_steps = [2e-5, 1e-5, 5e-6]
                accelerations = [local_ode_acceleration(system, packed, tangent, source['endpoint_acceleration'], source['outer_clock'][1], include_gram, step) for step in acceleration_steps]
                coarse_error = maximum(accelerations[0] - accelerations[1])
                fine_error = maximum(accelerations[1] - accelerations[2])
                relative_scale = max(1., maximum(accelerations[2]))
                check(label + '_directional_ODE_acceleration_refinement', fine_error < .8 * coarse_error or max(fine_error, coarse_error) < 1e-6 * relative_scale, {'coarse_difference': coarse_error, 'fine_difference': fine_error, 'scale': relative_scale})
                data = adapted_diagnostic(system, packed, tangent, accelerations[2], base, include_gram)
                coarse_data = adapted_diagnostic(system, packed, tangent, accelerations[1], base, include_gram)
                source_difference = maximum(data['boundary_force_time'] - coarse_data['boundary_force_time'])
                check(label + '_boundary_source_rate_resolved_at_two_steps', source_difference < 2e-7 * max(1., maximum(data['boundary_force_time'])))
                check(label + '_independent_second_metric_rate', maximum(data['M_second_rate_check_error']) < 2e-10 * max(1., maximum(data['M_second_rate'])))
                check(label + '_positive_adapted_energy', float(data['energy']) > 0)
                check(label + '_adapted_exact_energy_work_identity', abs(float(data['energy_time_complex'] - data['energy_time_predicted'])) < 2e-9 * max(1., abs(float(data['energy_time_predicted']))))
                check(label + '_boundary_source_kept_in_inequality', float(data['energy_time_predicted']) <= float(data['energy_rate_upper_bound']) + 2e-9)
                check(label + '_velocity_gradient_control_unchanged', float(base['velocity_radial_norm_free'] + base['velocity_radial_norm_lift']) <= float(data['velocity_radial_norm_upper_bound']) + 1e-12)
                check(label + '_same_prescribed_boundary_force', maximum(base['force_boundary_lift'] - data['boundary_force']) == 0)
                path_errors = []
                if intervals == 16:
                    for step in [2e-5, 1e-5]:
                        forward = quadratic_path_energy(system, packed, tangent, accelerations[2], base, include_gram, step)
                        backward = quadratic_path_energy(system, packed, tangent, accelerations[2], base, include_gram, -step)
                        derivative = (forward - backward) / (2 * step)
                        path_errors.append(abs(float(derivative - data['energy_time_predicted'])))
                    check(label + '_independent_quadratic_jet_energy_path', path_errors[1] < .8 * path_errors[0] or max(path_errors) < 2e-6 * max(1., abs(float(data['energy_time_predicted']))), path_errors)
                path = destination / (label + '.npz')
                numerical.savez_compressed(path, **data, local_ODE_acceleration=accelerations[2], coarser_ODE_acceleration=accelerations[1], full_shift_residual=tangent['shift_residual'], mass_rate_mismatch=tangent['packed_speed'][system.slices[0]] - tangent['shift_mass_speed'])
                artifact(path)
                record = {'case': case_name, 'intervals': intervals, 'branch': branch, 'time': float(time), **{name: float(data[name]) for name in ['energy', 'energy_time_predicted', 'energy_growth_rate', 'energy_rate_upper_bound', 'boundary_source_M_dual_norm', 'residual_force_K_graph_norm', 'velocity_radial_norm_upper_bound']}, 'old_forcing_graph_norm': float(base['work_forcing_graph_norm']), 'old_energy': float(base['energy']), 'old_energy_rate_upper_bound': float(base['energy_rate_upper_bound']), 'source_rate_two_step_difference': source_difference, 'maximum_local_metric_acceleration': maximum(accelerations[2][:system.slices[1].stop]), 'directional_acceleration_coarse_difference': coarse_error, 'directional_acceleration_fine_difference': fine_error, 'energy_identity_error': abs(float(data['energy_time_complex'] - data['energy_time_predicted'])), 'quadratic_path_errors': path_errors, 'nonlinear_closure_still_acceleration_dependent': case_name != 'canonical'}
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
            check('all_previous_sources_preserved', all(digest(root / name) == expected for name, expected in inputs.items()))
            check('all_outputs_preserved', all(digest(root / name) == expected for name, expected in outputs.items()))
            check('no_bytecode_cache', not (root / 'scripts/__pycache__').exists())
            report.update(state='complete', passed=sum(row['passed'] for row in report['checks']), total=len(report['checks']), completed_utc=datetime.now(timezone.utc).isoformat())
            save()
            (destination / 'COMPLETE').write_text(report['completed_utc'] + '\n')
            print(json.dumps({key: report[key] for key in ['state', 'passed', 'total', 'completed_utc']}), flush=True)
            return
        except Exception as error:
            report.update(state='failed', failure=repr(error), traceback=traceback.format_exc(), completed_utc=datetime.now(timezone.utc).isoformat())
            save()
            raise
    if final_path.exists():
        raise FileExistsError('Final evidence already exists.')
    report_path = destination / 'status.json'
    report = json.loads(report_path.read_text())
    if report['state'] != 'complete' or report['passed'] != report['total'] or not (destination / 'COMPLETE').exists():
        raise RuntimeError('Adapted energy gate incomplete.')
    inherit(inputs, report['inputs'])
    inherit(outputs, report['outputs'])
    for path in [report_path, destination / 'COMPLETE', destination / 'executed-script.py']:
        own(path)
    note = root / 'DERIVATION-20260909-first-derivative-graph-energy-and-boundary-forcing.md'
    cited = [value for value in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')) if value.endswith(('.py', '.json', '.md', '.npz'))]
    missing = [value for value in cited if root / value != final_path and not (root / value).is_file()]
    if missing:
        raise FileNotFoundError(str(missing))
    own(note)
    snapshot = intake / 'annular-first-derivative-energy-resume-snapshot.md'
    with snapshot.open('xb') as handle:
        handle.write((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    artifact(snapshot)
    frozen = root.parent / 'formalization-workbench'
    since = datetime(2026, 9, 9, 16, 20, 0, tzinfo=timezone.utc).timestamp()
    touched = [str(path.relative_to(frozen)) for path in frozen.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if touched or (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Protected workbench or cache check failed: ' + repr(touched))
    final = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'first_energy_checks': gate['total'], 'adapted_energy_checks': report['total'], 'state_samples': len(report['samples']), 'compiled_scripts': scripts, 'inputs': inputs, 'outputs': outputs, 'cited_local_paths_checked': cited, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-09T16:20:00Z, not full pre-turn hash comparison; all writes scoped to post-checkpoint-work', 'mutable_resume_pinned_as_snapshot': True, 'no_bytecode_cache': True, 'conditional_graph_energy_identity_derived': True, 'boundary_adapted_energy_identity_derived': True, 'uniform_energy_estimate_closed': False, 'full_coupled_DAE_solved': False, 'valid_for_physics_claim': False}
    with final_path.open('x') as handle:
        json.dump(final, handle, indent=2)
        handle.write('\n')
    print(json.dumps({'state': final['state'], 'first_energy_checks': gate['total'], 'adapted_energy_checks': report['total'], 'samples': len(report['samples']), 'input_hashes': len(inputs), 'output_hashes': len(outputs), 'protected_workbench_files_written_since_turn_start': len(touched)}), flush=True)


if __name__ == '__main__':
    run()
