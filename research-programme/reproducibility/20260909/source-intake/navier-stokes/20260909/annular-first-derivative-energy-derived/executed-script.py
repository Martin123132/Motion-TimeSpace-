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
    from annular_adm_mixed_action_20260909 import MixedActionBasis, real_linear
    from annular_action_boundary_current_20260909 import boundary_balance, canonical_momenta
    from annular_first_derivative_energy_20260909 import canonical_matrices, energy_diagnostic, graph_energy, growth_rates
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian

    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['derive', 'seal'])
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260909'
    destination = intake / 'annular-first-derivative-energy-derived'
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

    prior_path = intake / 'annular-mass-trace-final-integrity.json'
    prior = json.loads(prior_path.read_text())
    if prior['state'] != 'complete':
        raise RuntimeError('Mass-trace/commutator gate incomplete.')
    inherit(inputs, prior['inputs'])
    inherit(outputs, prior['outputs'])
    own(prior_path)
    scripts = ['annular_first_derivative_energy_20260909.py', 'derive_annular_first_derivative_energy_20260909.py']
    for name in scripts:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    if arguments.phase == 'derive':
        destination.mkdir(exist_ok=False)
        (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())
        report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': inputs, 'outputs': outputs, 'checks': [], 'samples': [], 'valid_for_physics_claim': False, 'uniform_energy_estimate_closed': False, 'scope': 'Conditional graph energy for the released scalar equation with unchanged Dirichlet traces. Canonical GR/Gram included in M,K; P(X) correction explicitly retained as acceleration-dependent forcing. Boundary-lift work, scalar-equation residuals and direct mass-rate mismatch work are recorded; no new evolution.'}

        def save():
            (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

        def check(name, passed, detail=None):
            report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
            if not passed:
                raise RuntimeError('Failed check: ' + name + ' ' + repr(detail))

        save()
        try:
            for case_name in ['canonical', 'nonlinear_modulated']:
                case_path = intake / 'annular-constraint-correction-initial' / (case_name + '.json')
                own(case_path)
                case = json.loads(case_path.read_text())
                constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
                kappa = float(symbolic.sympify(case['normalization_kappa']))
                for intervals in [16, 32, 64]:
                    for branch in ['GR', 'metric_Gram']:
                        tag = case_name + '_N' + str(intervals) + '_' + branch
                        report['active_job'] = tag
                        save()
                        source = loaded(intake / 'annular-released-Hermite-initial-derived' / (tag + '.npz'))
                        folder = intake / ('annular-boundary-N64-evolution-smoke' if intervals == 64 else 'annular-released-Hermite-evolution-smoke')
                        steps = 64 if intervals == 64 else 32
                        trajectory = loaded(folder / (tag + '_steps' + str(steps) + '.npz'))
                        basis = MixedActionBasis(source['radius'])
                        links = MetricLinkQuadrature(basis)
                        count = basis.radii.size
                        include_gram = branch != 'GR'
                        for index in [0, steps // 2, steps]:
                            time, state = trajectory['time'][index], trajectory['state'][index]
                            scalar, slope, momentum, slope_momentum = [state[part * count:(part + 1) * count] for part in range(4)]
                            packed = state[4 * count:]
                            system = ReleasedHermiteRouthian(basis, scalar, slope, constants, kappa, momentum, slope_momentum, source['outer_clock'][0] + time * source['outer_clock'][1], links)
                            tangent = system.constraint_tangent(packed, include_gram, source['endpoint_acceleration'], source['outer_clock'][1])
                            balance = boundary_balance(system, packed, tangent, include_gram, source['outer_clock'][1])
                            data = energy_diagnostic(system, packed, tangent, balance, include_gram, source['outer_clock'][1])
                            label = tag + '_sample' + str(index)
                            check(label + '_original_shift_vector_retained', maximum(tangent['shift_residual'] - trajectory['shifts'][index]) < 1e-13)
                            check(label + '_positive_free_mass_and_stiffness', numerical.linalg.eigvalsh(data['M'])[0] > 0 and numerical.linalg.eigvalsh(data['K'])[0] > 0)
                            check(label + '_same_two_scalar_boundary_traces', maximum(data['lift'][[0, count - 1]] - scalar[[0, -1]]) < 1e-14)
                            check(label + '_independent_analytic_mass_rate', maximum(data['matrix_M_rate_error']) < 2e-11 * max(1, maximum(data['M_dot'])))
                            check(label + '_independent_analytic_stiffness_rate', maximum(data['matrix_K_rate_error']) < 2e-11 * max(1, maximum(data['K_dot'])))
                            full_velocity = numerical.concatenate([packed[system.slices[2]], packed[system.slope_slice]])
                            momenta = numerical.concatenate(canonical_momenta(system, packed, include_gram))
                            check(label + '_independent_nonlinear_momentum_split', maximum(momenta - real_linear(data['full_M'], full_velocity) - data['nonlinear_momentum']) < 2e-12)
                            check(label + '_full_forced_scalar_equation', maximum(data['free_equation_residual']) < 2e-11)
                            check(label + '_energy_derivative_independent_complex_path', abs(float(data['energy_time_direct'] - data['energy_time_complex'])) < 2e-10 * max(1, abs(float(data['energy_time_direct']))))
                            check(label + '_derived_energy_work_identity', abs(float(data['energy_time_direct'] - data['energy_time_predicted'])) < 2e-10 * max(1, abs(float(data['energy_time_direct']))))
                            check(label + '_finite_energy_growth_inequality', float(data['energy_time_direct']) <= float(data['energy_rate_upper_bound']) + 2e-10)
                            check(label + '_velocity_gradient_controlled', float(data['velocity_radial_norm_free'] + data['velocity_radial_norm_lift']) <= float(data['velocity_radial_norm_upper_bound']) + 1e-12)
                            forcing_work = sum(float(data['forcing_work_' + name]) for name in ['boundary_lift', 'nonlinear', 'scalar_equation_residual'])
                            check(label + '_all_force_work_components_retained', abs(forcing_work - float(data['work_force_work'])) < 2e-10)
                            if case_name == 'canonical':
                                check(label + '_canonical_case_needs_no_nonlinear_closure_force', maximum(data['nonlinear_force']) == 0)
                                check(label + '_canonical_kinetic_is_existing_action', maximum(data['full_M'] - system.kinetic_matrix(packed, include_gram)) < 1e-12)
                            if index == 0:
                                mass, stiffness = data['M'], data['K']
                                frozen_acceleration = -data['graph']
                                step = 1e-25
                                frozen_energy = graph_energy(mass, stiffness, data['displacement'] + 1j * step * data['velocity'], data['velocity'] + 1j * step * frozen_acceleration)[0]
                                check(label + '_frozen_homogeneous_control_conserves_graph_energy', abs(frozen_energy.imag / step) < 2e-10)
                                rates = growth_rates(mass, stiffness, .07 * mass, -.03 * stiffness)
                                expected = {'alpha_M': .07, 'alpha_K': .03, 'alpha_A': .07, 'alpha_L': .03, 'energy_growth_rate': .17}
                                check(label + '_proportional_metric_control_has_grid_independent_rates', max(abs(rates[name] - value) for name, value in expected.items()) < 2e-7, rates)
                            if intervals == 16 and index == 0:
                                offshell = {name: value.copy() for name, value in tangent.items()}
                                offshell['packed_speed'][system.slices[2]] += .01 * numerical.sin(numerical.linspace(0, numerical.pi, count))
                                off_balance = boundary_balance(system, packed, offshell, include_gram, source['outer_clock'][1])
                                off_data = energy_diagnostic(system, packed, offshell, off_balance, include_gram, source['outer_clock'][1])
                                check(label + '_off_shell_scalar_force_cannot_be_deleted', maximum(off_data['force_scalar_equation_residual']) > 1e-7 and maximum(off_data['free_equation_residual']) < 2e-11)
                            path = destination / (label + '.npz')
                            numerical.savez_compressed(path, **data)
                            artifact(path)
                            fields = ['energy', 'energy_time_direct', 'energy_time_predicted', 'energy_rate_upper_bound', 'energy_growth_rate', 'alpha_M', 'alpha_K', 'alpha_A', 'alpha_L', 'work_forcing_graph_norm', 'forcing_work_boundary_lift', 'forcing_work_nonlinear', 'forcing_work_scalar_equation_residual', 'direct_mass_mismatch_energy_work', 'velocity_radial_norm_free', 'velocity_radial_norm_lift', 'velocity_radial_norm_upper_bound']
                            row = {'case': case_name, 'intervals': intervals, 'branch': branch, 'time': float(time), **{name: float(data[name]) for name in fields}, 'maximum_scalar_equation_residual_force': maximum(data['force_scalar_equation_residual']), 'maximum_full_shift_residual': maximum(tangent['shift_residual']), 'nonlinear_force_depends_on_acceleration': case_name != 'canonical'}
                            report['samples'].append(row)
                        save()
                        print(json.dumps(report['samples'][-1]), flush=True)
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
        raise RuntimeError('Energy derivation gate incomplete.')
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
    final = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'implementation_checks': report['total'], 'state_samples': len(report['samples']), 'compiled_scripts': scripts, 'inputs': inputs, 'outputs': outputs, 'cited_local_paths_checked': cited, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-09T16:20:00Z, not full pre-turn hash comparison; all writes scoped to post-checkpoint-work', 'mutable_resume_pinned_as_snapshot': True, 'no_bytecode_cache': True, 'conditional_graph_energy_identity_derived': True, 'uniform_energy_estimate_closed': False, 'full_coupled_DAE_solved': False, 'valid_for_physics_claim': False}
    with final_path.open('x') as handle:
        json.dump(final, handle, indent=2)
        handle.write('\n')
    print(json.dumps({'state': final['state'], 'checks': report['total'], 'samples': len(report['samples']), 'input_hashes': len(inputs), 'output_hashes': len(outputs), 'protected_workbench_files_written_since_turn_start': len(touched)}), flush=True)


if __name__ == '__main__':
    run()
