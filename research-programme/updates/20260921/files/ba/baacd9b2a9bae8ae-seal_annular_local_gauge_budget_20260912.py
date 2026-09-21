import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as np
    from scipy.linalg import lstsq, solve
    from annular_canonical_common_profile_aligned_20260912 import CommonProfile
    from annular_canonical_trace_context_20260911 import load_archive
    from annular_canonical_trace_projection_stable_20260911 import GlobalPrimitive
    from annular_covariant_canonical_ports_20260912 import CanonicalPortPreparation
    from annular_covariant_flux_moments_20260912 import install
    from annular_local_gauge_commutator_20260912 import gauge_budget

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260912'
    target = intake / 'annular-local-gauge-budget-final-integrity.json'
    snapshot = intake / 'annular-local-gauge-budget-resume-snapshot.md'
    if target.exists() or snapshot.exists():
        raise FileExistsError('Completed evidence cannot be overwritten.')
    report = {'state': 'running', 'checks': [], 'inputs': {}, 'outputs': {}, 'valid_for_physics_claim': False, 'new_evolution': False, 'full_first_jet_closed': False, 'full_second_jet_closed': False, 'interval_certificate': False, 'full_GR_limit_proven': False, 'old_working_branch': 'annular-acceleration-trace-completion-attempt02', 'preferred_small_new_action_diagnostic': 'annular-covariant-canonical-ports-attempt02 original79', 'improved_but_not_passing_new_action_comparison': 'annular-local-gauge-trace-stable-attempt01 modes4', 'protected_scan_scope': 'mtime since 2026-09-12T21:24:43Z, not pre-turn content hashes'}
    hashes = {}

    def digest(path):
        if path not in hashes:
            hashes[path] = hashlib.sha256(path.read_bytes()).hexdigest()
        return hashes[path]

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = digest(path)

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    batches = {}
    names = ['annular-local-gauge-budget-attempt01', 'annular-local-gauge-trace-stable-attempt01']
    failed_names = ['annular-local-gauge-trace-preserving-attempt01', 'annular-local-gauge-trace-factored-attempt01']
    for name in names + failed_names:
        directory = intake / name
        batch = json.loads((directory / 'status.json').read_text())
        batches[name] = batch
        if name in names:
            check(name + '_completed_validations', batch['state'] == 'complete' and all(row['passed'] for row in batch['checks']))
        else:
            check(name + '_failed_attempt_retained_as_failed', batch['state'] == 'failed' and bool(batch['error']))
        check(name + '_no_physics_or_full_jet_claim', not batch['valid_for_physics_claim'] and not batch['full_first_jet_closed'] and not batch['new_evolution'])
        for table in ['inputs', 'outputs']:
            for filename, expected in batch[table].items():
                if digest(root / filename) != expected:
                    raise RuntimeError('Changed evidence: ' + filename)
                if filename in report['inputs'] and report['inputs'][filename] != expected:
                    raise RuntimeError('Conflicting hash: ' + filename)
                report['inputs'][filename] = expected
        for path in directory.iterdir():
            if not path.is_file():
                continue
            own(path, 'outputs')
            if path.name.startswith('executed-'):
                check(name + '_executed_source_matches', digest(path) == digest(root / 'scripts' / path.name.removeprefix('executed-')))
            if path.suffix == '.npz':
                with np.load(path, allow_pickle=False) as arrays:
                    check(name + '_' + path.name + '_finite_numeric_arrays', all(np.isfinite(arrays[key]).all() for key in arrays.files))
    check('failed_trace_reconstruction_not_relabelled_physics_failure', 'protected traces' in batches[failed_names[0]]['error'])
    check('failed_moment_roundoff_not_fixed_by_relaxing_threshold', any(not row['passed'] and row['detail']['canonical_block_error'] > 1e-8 for row in batches[failed_names[1]]['checks']))
    completed = [case for name in names for case in batches[name]['cases']]
    check('both_matched_arenas_all_ten_prepared_candidates_kept', len(completed) == 10 and sum(case['branch'] == 'GR' for case in completed) == 5)
    check('no_candidate_laundered_to_full_first_jet', all(not row['full_first_jet_gate'] for case in completed for row in case['surfaces']))
    check('all_claim_tolerances_still_one_e_minus_ten', min(row['C1'] for case in completed for row in case['surfaces']) > 1e-10)
    common = CommonProfile(root)
    controls = []
    for name in names:
        for case in batches[name]['cases']:
            branch, modes = case['branch'], case['bubble_modes']
            model = CanonicalPortPreparation(common, branch)
            old_frames = model.frame
            old_pairings = model.pairings
            saved = load_archive(intake / name / (branch + '_modes' + str(modes) + '_candidate.npz'))
            raw_frames = load_archive(intake / name / (branch + '_modes' + str(modes) + '_frames.npz'))
            frames = {surface: {kind: raw_frames[surface + '__' + kind] for kind in ['q', 'qr', 'p']} for surface in model.frame}
            check(name + '_' + branch + '_' + str(modes) + '_old_columns_exact', all(np.array_equal(frames[surface][kind][:, :79], old_frames[surface][kind]) for surface in frames for kind in ['q', 'qr', 'p']))
            install(model, frames)
            free = common.physical_free(model.radii)
            amplitudes, unused_residual, rank, unused_singular = lstsq(model.momentum_lifts, saved['momentum'] - free['pi'])
            source_error = float(abs(saved['momentum'] - free['pi'] - model.momentum_lifts @ amplitudes).max())
            check(name + '_' + branch + '_' + str(modes) + '_unchanged_free_source_two_owned_lifts_only', rank == 2 and source_error < 1e-11 and abs(model.scalar - free['chi']).max() < 1e-13)
            for surface, weights, order in [('quad', model.context.weights, 12), ('check', model.context.check_weights, 16)]:
                result = model.evaluate(saved['coefficients'], surface)
                budget = gauge_budget(model, result, surface)
                values, nodes = result['fields'][surface], result['fields']['nodes']
                prefix = name + '_' + branch + '_' + str(modes) + '_' + surface
                check(prefix + '_saved_C1_reproduced', abs(result['C1'] - saved[surface + '__C1']).max() < 1e-12)
                check(prefix + '_full_gauge_identity_and_projected_equations', max(abs(budget[key]).max() for key in ['identity_error', 'q_weak_equation_error', 'p_weak_equation_error']) < 1e-10)
                check(prefix + '_gradient_omission_detected', abs(budget['missing_gradient_negative_control']).max() > 1e-10)
                check(prefix + '_nonzero_boundary_scalar_velocity', min(abs(result['current']['q'][[0, -1]])) > 1e-8)
                scalar_velocity = result['current']['q']
                power_target = np.array([-1., 1.]) * nodes['N'][[0, -1]] * result['mu_nodes'][[0, -1]] / (.1 * np.sqrt(nodes['F'][[0, -1]]))
                check(prefix + '_derived_canonical_boundary_power', abs(result['rho'][[0, -1]] * scalar_velocity[[0, -1]] - power_target).max() < 1e-12)
                check(prefix + '_bound_includes_roundoff_remainders', np.all(abs(result['C1']) <= budget['bound'] + abs(budget['identity_error']) + abs(budget['q_weak_equation_error']) + abs(budget['p_weak_equation_error']) + 1e-12))
                step = 1e-24j
                force_errors = []
                reaction = nodes['N'][0] / (.1 * np.sqrt(nodes['F'][0]))
                for column in range(model.frame[surface]['q'].shape[1]):
                    mass = values['mu'] + step * model.frame[surface]['q'][:, column]
                    node_mass = nodes['mu'] + step * model.frame['nodes']['q'][:, column]
                    root_f = np.sqrt(1 - 2 * mass / values['R'])
                    node_root = np.sqrt(1 - 2 * node_mass / model.radii)
                    hamiltonian = weights @ (-values['N'] * (root_f + 1 / root_f - 2 * model.reference) / .2 - values['R'] * values['N_r'] * (root_f - model.reference) / .1)
                    boundary = model.radii * nodes['N'] * (node_root - model.reference) / .1
                    hamiltonian += boundary[-1] - boundary[0] + model.clock * node_mass[-1] / .1 + (nodes['N'] * node_root) @ result['energy']
                    derivative = -hamiltonian.imag / step.imag + reaction * model.frame['nodes']['q'][0, column]
                    force_errors.append(abs(derivative - result['P_force'][column]))
                check(prefix + '_all_metric_action_variations', max(force_errors) < 1e-10, max(force_errors))
                current = result['current']
                c_p = .1 * np.sqrt(values['F']) / values['N']
                weak_columns = model.frame[surface]['p'] * (c_p * np.exp(-2 * current['primitive'].evaluate(values['R'])))[:, None]
                link_load = []
                for column in range(weak_columns.shape[1]):
                    primitive = GlobalPrimitive(model.context.knots, weak_columns[:, column], order)
                    link_load.append((primitive.evaluate(model.targets) - primitive.evaluate(model.anchors)) @ current['global_current'])
                load = model.frame[surface]['p'].T @ (weights * c_p * current['K'][surface])
                link_error = float(abs(np.array(link_load) - load).max())
                check(prefix + '_all_oriented_history_loads', link_error < 1e-9, link_error)
                old_velocity_map = old_frames['nodes']['q'][[0, -1]] @ solve(old_pairings[surface], old_frames[surface]['p'].T * weights)
                velocity_map = frames['nodes']['q'][[0, -1]] @ solve(model.pairings[surface], frames[surface]['p'].T * weights)
                old_load_map = np.concatenate([old_frames[surface]['q'].T * weights, old_frames['nodes']['q'].T], axis=1)
                load_map = np.concatenate([frames[surface]['q'].T * weights, frames['nodes']['q'].T], axis=1)
                old_trace_map = old_frames['nodes']['p'][[0, -1]] @ solve(old_pairings[surface].T, old_load_map)
                trace_map = frames['nodes']['p'][[0, -1]] @ solve(model.pairings[surface].T, load_map)
                velocity_map_error = float(abs(velocity_map - old_velocity_map).max())
                trace_map_error = float(abs(trace_map - old_trace_map).max())
                if name == names[1] and surface == 'quad':
                    check(prefix + '_both_added_traces_exactly_zero', not np.any(frames['nodes']['q'][[0, -1], 79:]) and not np.any(frames['nodes']['p'][[0, -1], 79:]))
                    check(prefix + '_endpoint_velocity_and_force_operators_preserved_for_all_loads', max(velocity_map_error, trace_map_error) < 1e-9, {'velocity': velocity_map_error, 'momentum': trace_map_error})
                controls.append({'run': name, 'branch': branch, 'modes': modes, 'quadrature': surface, 'phase_dimension': frames[surface]['q'].shape[1], 'metric_force_variations': len(force_errors), 'maximum_metric_force_error': float(max(force_errors)), 'history_load_error': link_error, 'source_profile_error': source_error, 'endpoint_velocity_operator_error': velocity_map_error, 'endpoint_momentum_operator_error': trace_map_error, 'gauge_identity_error': float(abs(budget['identity_error']).max())})
                print(json.dumps(controls[-1]), flush=True)
    files = ['annular_local_gauge_commutator', 'derive_annular_local_gauge_budget', 'annular_local_gauge_trace_preserving', 'derive_annular_local_gauge_trace_preserving', 'annular_local_gauge_trace_factored', 'derive_annular_local_gauge_trace_factored', 'annular_local_gauge_trace_stable', 'derive_annular_local_gauge_trace_stable', 'seal_annular_local_gauge_budget']
    interface_controls = []
    points, gauss = np.polynomial.legendre.leggauss(48)
    lower, interface, upper, coupling = 5.875, 6., 6.125, .1
    for mass_jump in [.001, .003, -.002]:
        masses = [1., 1. + mass_jump]
        root_left, root_right = np.sqrt(1 - 2 * np.array(masses) / interface)
        source_strength = -interface * (root_right - root_left) / coupling
        weak = np.zeros(5)
        for left, right, mass in [(lower, interface, masses[0]), (interface, upper, masses[1])]:
            radii = (left + right) / 2 + (right - left) * points / 2
            weights = (right - left) * gauss / 2
            fraction = (radii - lower) / (upper - lower)
            root_f = np.sqrt(1 - 2 * mass / radii)
            for degree in range(5):
                test = fraction**(degree + 1) * (1 - fraction)
                test_r = ((degree + 1) * fraction**degree * (1 - fraction) - fraction**(degree + 1)) / (upper - lower)
                weak[degree] += weights @ (test * (root_f + 1 / root_f - 2 * model.reference) / (2 * coupling) + test_r * radii * (root_f - model.reference) / coupling)
        test_interface = np.array([.5**(degree + 2) for degree in range(5)])
        residual = weak - source_strength * test_interface
        check('conditional_interface_jump_weak_action_' + str(mass_jump), abs(residual).max() < 1e-12, float(abs(residual).max()))
        check('interface_wrong_orientation_detected_' + str(mass_jump), abs(weak + source_strength * test_interface).max() > 1e-5)
        check('interface_exact_mass_jump_relation_' + str(mass_jump), abs(mass_jump - coupling * (root_left + root_right) * source_strength / 2) < 1e-12)
        interface_controls.append({'mass_jump': mass_jump, 'source_strength': float(source_strength), 'maximum_weak_error': float(abs(residual).max()), 'tests': 5, 'manufactured_weak_identity_only_not_parent_trace_choice': True})
    report['conditional_interface_identity_controls'] = interface_controls
    for stem in files:
        path = root / 'scripts' / (stem + '_20260912.py')
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    check('nine_new_scripts_compile_no_bytecode', True)
    note = root / 'DERIVATION-20260912-local-gauge-error-law-and-trace-preserving-trial.md'
    for citation in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')):
        if citation.endswith(('.py', '.md', '.npz', '.json')):
            check('cited_path_exists_' + citation, (root / citation).is_file())
    own(note, 'outputs')
    start = datetime.fromisoformat('2026-09-12T21:24:43+00:00').timestamp()
    protected = root.parent / 'formalization-workbench'
    check('protected_workbench_exists', protected.is_dir())
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start]
    check('protected_modified_count_zero_mtime', not changed, changed)
    check('no_python_cache', not (root / 'scripts/__pycache__').exists())
    snapshot.write_bytes((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    own(snapshot, 'outputs')
    report['run_check_counts'] = {name: len(batches[name]['checks']) for name in names}
    report['failed_attempts_preserved'] = {name: batches[name]['error'].split(': {')[0] for name in failed_names}
    report['independent_controls'] = controls
    report['completed_cases'] = completed
    report['protected_modified_count'] = len(changed)
    report['completed_utc'] = datetime.now(timezone.utc).isoformat()
    report['state'] = 'complete'
    target.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'state': 'complete', 'seal_checks': len(report['checks']), 'run_checks': report['run_check_counts'], 'independent_metric_variations': sum(row['metric_force_variations'] for row in controls), 'max_force_error': max(row['maximum_metric_force_error'] for row in controls), 'max_history_error': max(row['history_load_error'] for row in controls), 'max_gauge_identity_error': max(row['gauge_identity_error'] for row in controls), 'protected_modified_count': len(changed), 'full_first_jet_closed': False}), flush=True)


if __name__ == '__main__':
    run()
