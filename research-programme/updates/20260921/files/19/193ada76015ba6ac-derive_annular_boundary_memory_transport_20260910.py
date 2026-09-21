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
    from scipy.integrate import solve_ivp
    from scipy.linalg import eigvalsh, solve
    from annular_adm_mixed_action_20260909 import MixedActionBasis
    from annular_first_derivative_energy_20260909 import affine_lift_matrix
    from annular_paired_variational_energy_20260910 import graph_operators

    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['derive', 'seal'])
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    old_intake = root / 'source-intake/navier-stokes/20260909'
    intake = root / 'source-intake/navier-stokes/20260910'
    parent_folder = intake / 'annular-boundary-memory-energy-derived'
    destination = intake / 'annular-boundary-memory-transport-derived'
    parent_path = parent_folder / 'status.json'
    final_path = intake / 'annular-boundary-memory-energy-final-integrity.json'
    parent = json.loads(parent_path.read_text())
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

    if parent['state'] != 'complete' or parent['passed'] != parent['total']:
        raise RuntimeError('Memory-energy gate incomplete.')
    inherit(inputs, parent['inputs'])
    inherit(outputs, parent['outputs'])
    for path in [parent_path, parent_folder / 'COMPLETE', parent_folder / 'executed-script.py', Path(__file__).resolve()]:
        own(path)
    compile(Path(__file__).read_bytes(), str(Path(__file__)), 'exec')
    if arguments.phase == 'derive':
        destination.mkdir(exist_ok=False)
        (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())
        report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': inputs, 'outputs': outputs, 'checks': [], 'samples': [], 'manufactured': [], 'conditional_moving_BV_memory_bound_derived': True, 'actual_lift_transport_defect_sourced': True, 'actual_uniform_defect_and_beta_variation_bounds_proved': False, 'actual_memory_history_integrated': False, 'valid_for_physics_claim': False}

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
            for sample in parent['samples']:
                label = sample['label']
                tag = label.split('_sample')[0]
                base = loaded(old_intake / 'annular-first-derivative-energy-derived' / (label + '.npz'))
                spatial = loaded(old_intake / 'annular-spatial-clock-energy-derived' / (label + '.npz'))
                initial = loaded(old_intake / 'annular-released-Hermite-initial-derived' / (tag + '.npz'))
                memory = loaded(parent_folder / (label + '.npz'))
                basis = MixedActionBasis(initial['radius'])
                lift = affine_lift_matrix(basis)
                value = numerical.concatenate([basis.scalar_value, basis.lift_value / basis.spacing], axis=1)
                mass_density = basis.quadrature**2 / spatial['c'][0]
                full_mass_time = -value.T @ ((basis.quadrature_weights * mass_density * spatial['theta'])[:, None] * value)
                free = base['free']
                close(label + '_old_mass_rate_reconstructed', full_mass_time[numerical.ix_(free, free)], base['M_dot'])
                lift_value = memory['endpoint_lift']
                lift_time = solve(base['M'], (full_mass_time @ lift)[free] - base['M_dot'] @ lift_value, assume_a='sym')
                operators = graph_operators(base['M'], base['K'], base['M_dot'], base['K_dot'])
                defect = lift_time - operators['velocity_transport'] @ lift_value
                epsilon = 1e-25
                moved_lift = solve(base['M'] + 1j * epsilon * base['M_dot'], ((base['full_M'] + 1j * epsilon * full_mass_time) @ lift)[free], assume_a='sym')
                close(label + '_complex_endpoint_lift_derivative', moved_lift.imag / epsilon, lift_time)
                theta = float(numerical.max(abs(spatial['theta'])))
                lift_bound = numerical.sqrt((60025 / 1024) * .25 / 2)
                rate_norm = float(numerical.sqrt(max(eigvalsh(lift_time.T @ base['M'] @ lift_time)[-1], 0.)))
                defect_norm = float(numerical.sqrt(max(eigvalsh(defect.T @ base['M'] @ defect)[-1], 0.)))
                check(label + '_proved_lift_rate_bound', rate_norm <= 2 * theta * lift_bound + 1e-10)
                report['samples'].append({'label': label, 'intervals': sample['intervals'], 'branch': sample['branch'], 'time': sample['time'], 'endpoint_lift_rate_M_operator_norm': rate_norm, 'derived_lift_rate_upper_using_measured_theta': 2 * theta * lift_bound, 'moving_endpoint_transport_defect_M_operator_norm': defect_norm, 'uniform_defect_bound_proved': False})
                if sample['time'] == .01:
                    print(json.dumps(report['samples'][-1]), flush=True)
                save()
            initial_lift = numerical.array([[1., .2], [.1, .8]])
            endpoints_start, endpoints_rate = numerical.array([.02, -.01]), numerical.array([-.005, .003])
            operator = numerical.diag([2., 8.])

            def manufactured_rhs(time, state):
                direct_graph, direct_velocity, integrated_graph, integrated_velocity = state.reshape(4, 2)
                alpha = .1 / (1 + .1 * time)
                lift = (1 + .03 * time) * initial_lift
                lift_time = .03 * initial_lift
                endpoints = endpoints_start + time * endpoints_rate
                defect = lift_time + alpha * lift
                direct = numerical.concatenate([direct_velocity + lift @ endpoints, -operator @ direct_graph - alpha * direct_velocity])
                integrated = numerical.concatenate([integrated_velocity, -operator @ integrated_graph - alpha * integrated_velocity + defect @ endpoints + lift @ endpoints_rate])
                return numerical.concatenate([direct, integrated])

            state = numerical.concatenate([numerical.zeros(6), initial_lift @ endpoints_start])
            solution = solve_ivp(manufactured_rhs, [0., 1.], state, method='DOP853', rtol=2e-12, atol=2e-14, dense_output=True)
            check('manufactured_moving_system_integrates', solution.success)
            initial_lift_norm = float(numerical.linalg.norm(initial_lift, 2))
            lift_sup = numerical.sqrt(1.1) * 1.03 * initial_lift_norm
            defect_sup = numerical.sqrt(1.1) * (.03 + .1 * 1.03) * initial_lift_norm
            for time in [.1, .5, 1.]:
                direct_graph, direct_velocity, integrated_graph, integrated_velocity = solution.sol(time).reshape(4, 2)
                lift = (1 + .03 * time) * initial_lift
                endpoints = endpoints_start + time * endpoints_rate
                close('manufactured_BV_identity_graph_' + str(time), direct_graph, integrated_graph)
                close('manufactured_BV_identity_velocity_' + str(time), direct_velocity, integrated_velocity - lift @ endpoints)
                mass = (1 + .1 * time) * numerical.eye(2)
                stiffness = (1 + .1 * time) * operator
                norm = numerical.sqrt(direct_graph @ stiffness @ direct_graph + direct_velocity @ mass @ direct_velocity)
                propagator = numerical.exp(.05 * time)
                bound = lift_sup * (numerical.linalg.norm(endpoints) + propagator * (numerical.linalg.norm(endpoints_start) + time * numerical.linalg.norm(endpoints_rate)))
                bound += propagator * defect_sup * time * max(numerical.linalg.norm(endpoints_start), numerical.linalg.norm(endpoints))
                check('manufactured_uniform_moving_bound_' + str(time), norm <= bound)
                report['manufactured'].append({'time': time, 'energy_norm': float(norm), 'derived_uniform_upper': float(bound), 'scope': 'Analytic two-mode moving oscillator with known coefficient bounds, not an MTS trajectory.'})
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
        raise RuntimeError('Moving transport validation incomplete.')
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
    final = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'memory_checks': parent['total'], 'transport_checks': report['total'], 'checks': parent['total'] + report['total'], 'saved_states': len(parent['samples']), 'frozen_controls': len(parent['frozen_controls']), 'manufactured_moving_control_samples': len(report['manufactured']), 'inputs': inputs, 'outputs': outputs, 'cited_local_paths_checked': cited, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-10T00:19:00Z, not a full pre-turn hash baseline', 'no_bytecode_cache': True, 'boundary_memory_energy_correction_derived': True, 'frozen_uniform_BV_bound_derived': True, 'conditional_moving_BV_bound_derived': True, 'actual_moving_memory_bound_open': True, 'actual_corrector_history_integrated': False, 'full_evolution_closed': False, 'valid_for_physics_claim': False}
    with final_path.open('x') as handle:
        json.dump(final, handle, indent=2)
        handle.write('\n')
    print(json.dumps({name: final[name] for name in ['state', 'checks', 'saved_states', 'frozen_controls', 'protected_workbench_files_written_since_turn_start']}), flush=True)


if __name__ == '__main__':
    run()
