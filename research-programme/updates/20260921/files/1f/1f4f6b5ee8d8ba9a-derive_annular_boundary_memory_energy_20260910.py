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
    from scipy.linalg import eigh, eigvalsh, solve
    from annular_adm_mixed_action_20260909 import MixedActionBasis
    from annular_first_derivative_energy_20260909 import affine_lift_matrix
    from annular_paired_variational_energy_20260910 import graph_operators
    from annular_boundary_memory_energy_20260910 import affine_response, constant_response, corrected_work, gramian_quadrature, input_gramian, input_sampling_bound, modal_system

    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['derive', 'seal'])
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    old_intake = root / 'source-intake/navier-stokes/20260909'
    intake = root / 'source-intake/navier-stokes/20260910'
    paired_folder = intake / 'annular-paired-variational-energy-derived-attempt03'
    source_folder = intake / 'annular-boundary-source-trace-law-derived'
    destination = intake / 'annular-boundary-memory-energy-derived'
    prior_path = intake / 'annular-paired-variational-energy-final-integrity.json'
    final_path = intake / 'annular-boundary-memory-energy-final-integrity.json'
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
    for name in ['annular_boundary_memory_energy_20260910.py', 'derive_annular_boundary_memory_energy_20260910.py']:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    if arguments.phase == 'derive':
        destination.mkdir(exist_ok=False)
        (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())
        report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': inputs, 'outputs': outputs, 'checks': [], 'samples': [], 'frozen_controls': [], 'moving_boundary_memory_correction_identity_derived': True, 'frozen_BV_input_mesh_uniform_bound_derived': True, 'no_beta_time_derivative_in_corrector_equations': True, 'actual_beta_uniform_BV_bound_proved': False, 'moving_memory_energy_mesh_uniform_bound_proved': False, 'actual_corrector_history_integrated': False, 'full_evolution_closed': False, 'valid_for_physics_claim': False}

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
            source_path = source_folder / 'status.json'
            own(source_path)
            samples = json.loads(source_path.read_text())['samples']
            for sample in samples:
                label, intervals, branch = sample['label'], sample['intervals'], sample['branch']
                tag = label.split('_sample')[0]
                base = loaded(old_intake / 'annular-first-derivative-energy-derived' / (label + '.npz'))
                pair = loaded(paired_folder / (label + '.npz'))
                source = loaded(source_folder / (label + '.npz'))
                initial = loaded(old_intake / 'annular-released-Hermite-initial-derived' / (tag + '.npz'))
                basis = MixedActionBasis(initial['radius'])
                mass, stiffness, mass_time, stiffness_time = [base[name] for name in ['M', 'K', 'M_dot', 'K_dot']]
                lift_map = affine_lift_matrix(basis)
                endpoint_lift = solve(mass, (base['full_M'] @ lift_map)[base['free']], assume_a='sym')
                endpoints = source['derived_endpoint_coefficients']
                close(label + '_derived_endpoint_source_unchanged', endpoint_lift @ endpoints, source['source_endpoint'])
                operators = graph_operators(mass, stiffness, mass_time, stiffness_time)
                modal = modal_system(mass, stiffness, endpoint_lift)
                duration = .01
                control = constant_response(modal, endpoints, duration)
                work = corrected_work(mass, stiffness, mass_time, stiffness_time, operators, pair['graph'], pair['graph_velocity'], pair['source_configuration'], pair['source_velocity'], source['source_endpoint'], control['g'], control['h'])
                close(label + '_actual_moving_corrected_energy_identity', work['direct_rate'], work['work_rate'])
                close(label + '_correction_not_deleted_work', work['energy'], work['original_energy'] + work['correction'])
                check(label + '_positive_corrected_and_memory_energies', min(work['energy'], work['memory_energy']) >= 0)
                check(label + '_corrected_finite_mesh_energy_inequality', work['direct_rate'] <= work['rate_upper'] + 1e-7)
                check(label + '_original_energy_triangle_control', work['original_energy'] <= work['triangle_bound'] + 1e-7)
                remaining = source['source_zero_trace_volume'] + source['source_Gram'] + source['source_quadrature']
                close(label + '_all_remaining_source_parts_retained', pair['source_configuration'] - source['source_endpoint'], remaining)
                epsilon = 1e-25
                moved_graph = work['corrected_graph'] + 1j * epsilon * work['corrected_graph_time']
                moved_velocity = work['corrected_velocity'] + 1j * epsilon * work['corrected_velocity_time']
                moved_energy = .5 * (moved_graph @ (stiffness + 1j * epsilon * stiffness_time) @ moved_graph + moved_velocity @ (mass + 1j * epsilon * mass_time) @ moved_velocity)
                close(label + '_complex_corrected_energy_derivative', moved_energy.imag / epsilon, work['direct_rate'])
                m_max, length = 60025 / 1024, .25
                lift_bound = m_max * length / 2
                actual_lift_squared = float(eigvalsh(endpoint_lift.T @ mass @ endpoint_lift)[-1])
                check(label + '_uniform_mass_projection_endpoint_lift_bound', actual_lift_squared <= lift_bound)
                check(label + '_frozen_constant_input_uniform_energy_bound', control['energy'] <= 2 * lift_bound * float(endpoints @ endpoints) + 1e-12)
                output = destination / (label + '.npz')
                numerical.savez_compressed(output, endpoint_lift=endpoint_lift, frequencies=modal['frequencies'], modal_lift=modal['lift'], memory_graph=control['g'], memory_velocity=control['h'], local_memory_graph_rate=work['memory_graph_time'], local_memory_velocity_rate=work['memory_velocity_time'], actual_derived_endpoint_coefficients=endpoints, remaining_source=remaining, physical_mismatch=pair['physical_mismatch'], full_shift_residual=pair['full_shift_residual'])
                artifact(output)
                row = {'label': label, 'intervals': intervals, 'branch': branch, 'time': sample['time'], 'remaining_source_norm': work['remaining_source_norm'], 'full_source_configuration_norm': float(numerical.sqrt(pair['source_configuration'] @ stiffness @ pair['source_configuration'])), 'frozen_constant_input_response_energy': control['energy'], 'frozen_constant_input_uniform_bound': 2 * lift_bound * float(endpoints @ endpoints), 'projection_L2_squared_norm': actual_lift_squared, 'comparison_jet_scope': 'Frozen constant-input value used as an arbitrary comparison jet at this state; its derivative uses actual moving operators. Not the integrated actual corrector history.'}
                report['samples'].append(row)
                if sample['time'] == .01:
                    frozen = {'tag': tag, 'frequencies_max': float(max(modal['frequencies'])), 'pointwise_input_squared_norm': float(eigvalsh(endpoint_lift.T @ stiffness @ endpoint_lift)[-1]), 'horizons': []}
                    for horizon in [.01, .1, 1.]:
                        gramian = input_gramian(modal, horizon)
                        eigenvalues = eigvalsh(gramian)
                        gain = float(eigenvalues[-1])
                        check(tag + '_Gramian_positive_' + str(horizon), eigenvalues[0] >= -1e-9 * (1 + gain))
                        sampling = input_sampling_bound(modal, horizon, 1 / horizon)
                        check(tag + '_proved_sampling_upper_bound_' + str(horizon), gain <= sampling['sufficient_gramian_bound'] * (1 + 1e-9))
                        frozen['horizons'].append({'duration': horizon, 'squared_L2_input_gain': gain, 'minimum_eigenvalue': float(eigenvalues[0]), 'spectral_sampling': sampling})
                        if horizon == .01:
                            order = max(100, int(2 * max(modal['frequencies']) * horizon) + 30)
                            direct = gramian_quadrature(modal, horizon, order)
                            close(tag + '_independent_Gramian_time_quadrature', gramian, direct, tolerance=1e-8)
                            final_endpoints = numerical.array([.7 * endpoints[0], -.2 * endpoints[1]])
                            affine = affine_response(modal, endpoints, final_endpoints, horizon)
                            variation = numerical.linalg.norm(final_endpoints - endpoints)
                            bound = 2 * lift_bound * (numerical.linalg.norm(endpoints) + variation)**2
                            check(tag + '_affine_BV_input_uniform_bound', affine['energy'] <= bound + 1e-10)
                            input_norm_squared = horizon / 3 * float(endpoints @ endpoints + endpoints @ final_endpoints + final_endpoints @ final_endpoints)
                            check(tag + '_affine_exact_Gramian_input_bound', 2 * affine['energy'] <= gain * input_norm_squared + 1e-10)
                            frozen['affine_control'] = {'energy': affine['energy'], 'uniform_BV_energy_bound': float(bound), 'input_L2_squared': input_norm_squared}
                    report['frozen_controls'].append(frozen)
                    print(json.dumps({'sample': row, 'frozen': frozen}), flush=True)
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
            report.update(state='failed', failure=repr(error), traceback=traceback.format_exc())
            save()
            raise
    report_path = destination / 'status.json'
    report = json.loads(report_path.read_text())
    if report['state'] != 'complete' or report['passed'] != report['total']:
        raise RuntimeError('Memory energy gate incomplete.')
    inherit(inputs, report['inputs'])
    inherit(outputs, report['outputs'])
    for path in [report_path, destination / 'COMPLETE', destination / 'executed-script.py']:
        own(path)
    note = root / 'DERIVATION-20260910-boundary-memory-correction-without-clock-differentiation.md'
    cited = [value for value in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')) if value.endswith(('.py', '.md', '.json', '.npz'))]
    missing = [value for value in cited if root / value != final_path and not (root / value).is_file()]
    if missing:
        raise FileNotFoundError(str(missing))
    own(note)
    snapshot = intake / 'annular-boundary-memory-energy-resume-snapshot.md'
    with snapshot.open('xb') as handle:
        handle.write((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    artifact(snapshot)
    frozen = root.parent / 'formalization-workbench'
    since = datetime(2026, 9, 10, 0, 19, 0, tzinfo=timezone.utc).timestamp()
    touched = [str(path.relative_to(frozen)) for path in frozen.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if touched or (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Protected workbench/cache check failed: ' + repr(touched))
    final = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'checks': report['total'], 'saved_states': len(report['samples']), 'frozen_controls': len(report['frozen_controls']), 'inputs': inputs, 'outputs': outputs, 'cited_local_paths_checked': cited, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-10T00:19:00Z, not a full pre-turn hash baseline', 'no_bytecode_cache': True, 'boundary_memory_energy_correction_derived': True, 'frozen_uniform_BV_bound_derived': True, 'actual_moving_memory_bound_open': True, 'actual_corrector_history_integrated': False, 'full_evolution_closed': False, 'valid_for_physics_claim': False}
    with final_path.open('x') as handle:
        json.dump(final, handle, indent=2)
        handle.write('\n')
    print(json.dumps({name: final[name] for name in ['state', 'checks', 'saved_states', 'frozen_controls', 'protected_workbench_files_written_since_turn_start']}), flush=True)


if __name__ == '__main__':
    run()
