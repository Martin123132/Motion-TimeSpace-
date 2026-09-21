import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as np
    from scipy.linalg import lstsq
    from annular_canonical_common_profile_aligned_20260912 import CommonProfile
    from annular_canonical_trace_context_20260911 import load_archive
    from annular_canonical_trace_projection_stable_20260911 import GlobalPrimitive
    from annular_covariant_canonical_ports_20260912 import CanonicalPortPreparation
    from annular_covariant_flux_moments_20260912 import install

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260912'
    target = intake / 'annular-covariant-flux-ports-final-integrity.json'
    snapshot = intake / 'annular-covariant-flux-ports-resume-snapshot.md'
    if target.exists() or snapshot.exists():
        raise FileExistsError('Completed evidence cannot be overwritten.')
    report = {'state': 'running', 'checks': [], 'inputs': {}, 'outputs': {}, 'valid_for_physics_claim': False, 'new_evolution': False, 'full_first_jet_closed': False, 'full_second_jet_closed': False, 'interval_certificate': False, 'full_GR_limit_proven': False, 'moment_completion_constructed': True, 'feedback_completion_adopted': False, 'canonical_boundary_power_derived_under_endpoint_balance_contract': True, 'parent_signed_full_source_histories': False, 'old_working_branch': 'annular-acceleration-trace-completion-attempt02', 'preferred_new_action_diagnostic': 'annular-covariant-canonical-ports-attempt02 original79', 'protected_scan_scope': 'mtime since 2026-09-12T20:51:40Z, not pre-turn content hashes'}
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
    names = ['annular-covariant-flux-moments-attempt01', 'annular-covariant-flux-feedback-attempt01', 'annular-covariant-canonical-ports-attempt02']
    for name in names:
        directory = intake / name
        batch = json.loads((directory / 'status.json').read_text())
        batches[name] = batch
        check(name + '_all_validation_checks_completed', batch['state'] == 'complete' and all(item['passed'] for item in batch['checks']))
        check(name + '_no_physics_evolution_or_full_first_jet_claim', not batch['valid_for_physics_claim'] and not batch['new_evolution'] and not batch['full_first_jet_closed'])
        for table in ['inputs', 'outputs']:
            for name_input, expected in batch[table].items():
                if digest(root / name_input) != expected:
                    raise RuntimeError('Changed evidence: ' + name_input)
                if name_input in report['inputs'] and report['inputs'][name_input] != expected:
                    raise RuntimeError('Conflicting hash: ' + name_input)
                report['inputs'][name_input] = expected
        for path in directory.iterdir():
            if not path.is_file():
                continue
            own(path, 'outputs')
            if path.name.startswith('executed-'):
                check(name + '_executed_source_matches', digest(path) == digest(root / 'scripts' / path.name.removeprefix('executed-')))
            if path.suffix == '.npz':
                with np.load(path, allow_pickle=False) as arrays:
                    check(name + '_' + path.name + '_finite_numeric_arrays', all(np.isfinite(arrays[key]).all() for key in arrays.files))
    failed_directory = intake / 'annular-covariant-canonical-ports-attempt01'
    failed = json.loads((failed_directory / 'status.json').read_text())
    check('failed_normalized_residual_validator_preserved_not_laundered', failed['state'] == 'failed' and 'metric_Gram_original79_check_joint_physical_drive_and_C0' in failed['error'] and any(not row['passed'] for row in failed['checks']))
    for path in failed_directory.iterdir():
        if path.is_file():
            own(path, 'outputs')
    check('inherited_unique_evidence_hashes_match', True, len(report['inputs']))
    moment = batches[names[0]]
    feedback = batches[names[1]]
    ports = batches[names[2]]
    for case in moment['cases']:
        construction = case['construction']
        check(case['branch'] + '_continuous_all16_lift_constructed', construction['family_dimension'] == 16 and construction['coordinate_system']['rank'] == 100 and construction['momentum_system']['rank'] == 113 and construction['source_moment_error'] < 1e-9 and construction['endpoint_trace_error'] < 1e-10 and construction['new_phase_dimension'] == 95)
        check(case['branch'] + '_regenerated_family_not_promoted_from_frozen_certificate', all(row['regenerated_all16_moment_error'] > 1e-6 and not row['full_first_jet_gate'] for row in case['results']))
    for case in feedback['cases']:
        iterations = case['iterations']
        check(case['branch'] + '_feedback_budget_four_and_no_growth', len(iterations) == 4 and all(row['current_frozen_mass_dimension'] == 95 for row in iterations))
        check(case['branch'] + '_feedback_not_claimed_contracting', iterations[-1]['generator_change_max'] > iterations[-2]['generator_change_max'] and all(not item['full_first_jet_gate'] for row in iterations for item in row['surfaces']))
    check('all12_port_comparisons_done_not_selected_only_best', len(ports['cases']) == 12 and all(not row['full_first_jet_gate'] for row in ports['cases']))
    check('same_physical_tolerance_corrected_not_relaxed', 'No physical tolerance changed' in ports['attempt01_test_normalization_bug_corrected'])
    check('global_canonical_power_without_local_constraint_claim', max(abs(row['N_weighted_C1']) for row in ports['cases']) < 1e-12 and min(row['C1'] for row in ports['cases']) > 1e-10)
    check('port_difference_identity_not_row_fitted', max(row['port_rule_difference'] for row in ports['cases']) < 1e-12)
    controls = []
    common = CommonProfile(root)
    for branch in ['GR', 'metric_Gram']:
        for selection in ['original79', 'one_pass95', 'feedback_last95']:
            model = CanonicalPortPreparation(common, branch)
            if selection != 'original79':
                path = intake / names[0] / (branch + '_frozen_extended_frames.npz') if selection == 'one_pass95' else intake / names[1] / (branch + '_iteration4_frames.npz')
                raw = load_archive(path)
                install(model, {surface: {kind: raw[surface + '__' + kind] for kind in ['q', 'qr', 'p']} for surface in model.frame})
            saved = load_archive(intake / names[2] / (branch + '_' + selection + '_canonical_port_candidate.npz'))
            free = common.physical_free(model.radii)
            amplitudes, unused_residual, rank, unused_singular = lstsq(model.momentum_lifts, saved['momentum'] - free['pi'])
            source_error = float(abs(saved['momentum'] - free['pi'] - model.momentum_lifts @ amplitudes).max())
            check(branch + '_' + selection + '_common_source_profile_modulo_only_two_owned_lifts', rank == 2 and source_error < 1e-11 and abs(model.scalar - free['chi']).max() < 1e-13)
            for surface, weights, order in [('quad', model.context.weights, 12), ('check', model.context.check_weights, 16)]:
                result = model.evaluate(saved['coefficients'], surface)
                values, nodes = result['fields'][surface], result['fields']['nodes']
                step = 1e-24j
                force_errors = []
                inner_reaction = nodes['N'][0] / (.1 * np.sqrt(nodes['F'][0]))
                for column in range(model.frame[surface]['q'].shape[1]):
                    mass = values['mu'] + step * model.frame[surface]['q'][:, column]
                    node_mass = nodes['mu'] + step * model.frame['nodes']['q'][:, column]
                    root_f = np.sqrt(1 - 2 * mass / values['R'])
                    node_root = np.sqrt(1 - 2 * node_mass / model.radii)
                    hamiltonian = weights @ (-values['N'] * (root_f + 1 / root_f - 2 * model.reference) / .2 - values['R'] * values['N_r'] * (root_f - model.reference) / .1)
                    boundary = model.radii * nodes['N'] * (node_root - model.reference) / .1
                    hamiltonian += boundary[-1] - boundary[0] + model.clock * node_mass[-1] / .1 + (nodes['N'] * node_root) @ result['energy']
                    derivative = -hamiltonian.imag / step.imag + inner_reaction * model.frame['nodes']['q'][0, column]
                    force_errors.append(abs(derivative - result['P_force'][column]))
                current = result['current']
                c_p = .1 * np.sqrt(values['F']) / values['N']
                weak_columns = model.frame[surface]['p'] * (c_p * np.exp(-2 * current['primitive'].evaluate(values['R'])))[:, None]
                link_load = []
                for column in range(weak_columns.shape[1]):
                    primitive = GlobalPrimitive(model.context.knots, weak_columns[:, column], order)
                    link_load.append((primitive.evaluate(model.targets) - primitive.evaluate(model.anchors)) @ current['global_current'])
                load = model.frame[surface]['p'].T @ (weights * c_p * current['K'][surface])
                link_error = float(abs(np.array(link_load) - load).max())
                prefix = branch + '_' + selection + '_' + surface
                check(prefix + '_every_metric_force_action_derivative', max(force_errors) < 1e-10, max(force_errors))
                check(prefix + '_every_oriented_history_load', link_error < 1e-9, link_error)
                check(prefix + '_scalar_and_metric_canonical_equations', max(abs(model.node_weights * result['p_first'] - current['Gchi'] - result['rho']).max(), abs(model.pairings[surface].T @ result['P_coeff'] - result['P_force']).max()) < 1e-10)
                controls.append({'branch': branch, 'frame': selection, 'quadrature': surface, 'metric_force_variations': len(force_errors), 'maximum_metric_force_error': float(max(force_errors)), 'history_load_error': link_error, 'source_profile_error': source_error, 'minimum_interior_nodal_energy': float(result['energy'][1:-1].min())})
    check('positive_interior_energy_hypothesis_for_fixed_node_lemma', min(row['minimum_interior_nodal_energy'] for row in controls) > 0)
    stems = ['annular_covariant_flux_moments', 'derive_annular_covariant_flux_moments', 'derive_annular_covariant_flux_feedback', 'annular_covariant_canonical_ports', 'verify_annular_covariant_canonical_ports', 'verify_annular_covariant_canonical_ports_physical_units', 'seal_annular_covariant_flux_ports']
    for stem in stems:
        path = root / 'scripts' / (stem + '_20260912.py')
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    check('seven_new_scripts_compile_without_bytecode', True)
    note = root / 'DERIVATION-20260912-flux-moment-lifts-and-canonical-boundary-power.md'
    for citation in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')):
        if citation.endswith(('.py', '.md', '.npz', '.json')):
            check('cited_path_exists_' + citation, (root / citation).is_file())
    own(note, 'outputs')
    start = datetime.fromisoformat('2026-09-12T20:51:40+00:00').timestamp()
    protected = root.parent / 'formalization-workbench'
    check('protected_workbench_exists', protected.is_dir())
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start]
    check('protected_modified_count_zero_mtime', not changed, changed)
    check('no_python_cache', not (root / 'scripts/__pycache__').exists())
    snapshot.write_bytes((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    own(snapshot, 'outputs')
    report['run_check_counts'] = {name: len(batch['checks']) for name, batch in batches.items()}
    report['completed_canonical_port_cases'] = ports['cases']
    report['independent_action_and_history_controls'] = controls
    report['preferred_original79_cases'] = [row for row in ports['cases'] if row['frame'] == 'original79']
    report['protected_modified_count'] = len(changed)
    report['completed_utc'] = datetime.now(timezone.utc).isoformat()
    report['state'] = 'complete'
    target.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'state': 'complete', 'seal_checks': len(report['checks']), 'run_checks': report['run_check_counts'], 'independent_metric_variations': sum(row['metric_force_variations'] for row in controls), 'max_force_error': max(row['maximum_metric_force_error'] for row in controls), 'max_history_load_error': max(row['history_load_error'] for row in controls), 'protected_modified_count': len(changed), 'full_first_jet_closed': False}), flush=True)


if __name__ == '__main__':
    run()
