import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as np

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260912'
    destination = intake / 'annular-covariant-scalar-final-integrity.json'
    snapshot = intake / 'annular-covariant-scalar-resume-snapshot.md'
    if destination.exists() or snapshot.exists():
        raise FileExistsError('Completed seals and resume snapshots are immutable.')
    report = {'state': 'running', 'checks': [], 'inputs': {}, 'outputs': {}, 'valid_for_physics_claim': False, 'new_evolution': False, 'full_second_jet_closed': False, 'interval_certificate': False, 'full_GR_limit_proven': False, 'same_continuum_scalar_rewriting_derived': True, 'new_finite_full_scalar_action': True, 'kinetic_pair_adopted_as_full_repair': False, 'new_C0_only_roots_not_full_initial_data': True, 'source_scalar_jets_on_prescribed_metric_not_coupled_solutions': True, 'working_numerical_branch': 'annular-acceleration-trace-completion-attempt02', 'protected_scan_scope': 'mtime since 2026-09-12T18:36:21Z, not a pre-turn content snapshot'}
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

    def inherit(batch):
        for table in ['inputs', 'outputs']:
            for name, expected in batch.get(table, {}).items():
                if digest(root / name) != expected:
                    raise RuntimeError('Changed immutable evidence: ' + name)
                if name in report['inputs'] and report['inputs'][name] != expected:
                    raise RuntimeError('Conflicting source hash: ' + name)
                report['inputs'][name] = expected

    previous_path = intake / 'annular-history-ward-final-integrity.json'
    previous = json.loads(previous_path.read_text())
    check('previous_Ward_seal_complete_without_solution_claim', previous['state'] == 'complete' and not previous['full_second_jet_closed'])
    inherit(previous)
    own(previous_path)
    names = ['annular-scalar-kinetic-pair-attempt01', 'annular-scalar-kinetic-ward-control-attempt01', 'annular-covariant-full-scalar-action-attempt01', 'annular-covariant-scalar-source-jet-attempt01', 'annular-covariant-scalar-preparation-control-attempt01']
    batches = {}
    for name in names:
        directory = intake / name
        batch = json.loads((directory / 'status.json').read_text())
        batches[name] = batch
        check(name + '_completed_all_validation_checks', batch['state'] == 'complete' and all(row['passed'] for row in batch['checks']))
        check(name + '_no_physics_or_full_second_jet_promotion', not batch['valid_for_physics_claim'] and not batch['new_evolution'] and not batch['full_second_jet_closed'] and not batch['interval_certificate'])
        inherit(batch)
        for path in directory.iterdir():
            if path.is_file():
                own(path, 'outputs')
            if path.name.startswith('executed-'):
                check(name + '_' + path.name + '_matches_executed_source', digest(path) == digest(root / 'scripts' / path.name.removeprefix('executed-')))
            if path.suffix == '.npz':
                with np.load(path, allow_pickle=False) as archive:
                    check(name + '_' + path.name + '_finite_arrays', all(np.isfinite(archive[key]).all() for key in archive.files))
    check('all_inherited_source_and_output_hashes_match', True, {'unique_immutable_files_checked': len(report['inputs'])})
    pair = batches['annular-scalar-kinetic-pair-attempt01']
    for row in pair['cases']:
        check(row['branch'] + '_kinetic_map_fixed_without_claiming_old_momentum_retention', row['construction']['new_scalar_dimension'] == 75 and row['old_scalar_momentum_space_deliberately_replaced_not_silently_preserved'] and max(row['construction']['pointwise_kinetic_image_errors_all_surfaces'].values()) < 1e-12)
        check(row['branch'] + '_kinetic_acceleration_both_quadratures', max(row['primary_kinetic_control']['kinetic_rate_defect_max'], row['higher_kinetic_control']['kinetic_rate_defect_max']) < 1e-12)
        check(row['branch'] + '_kinetic_candidate_not_a_full_repair', not row['primary']['full_second_jet_gate'] and not row['higher']['full_second_jet_gate'] and row['primary']['C2_full19_max'] > row['baseline']['C2_full19_max'])
    ward = batches['annular-scalar-kinetic-ward-control-attempt01']
    check('kinetic_candidate_Ward_explains_remaining_error', len(ward['cases']) == 4 and max(row['full_Ward_prediction_error'] for row in ward['cases']) < 1e-11)
    action = batches['annular-covariant-full-scalar-action-attempt01']
    check('thirty_three_action_checks_include_ten_true_variation_tests', len(action['checks']) == 33 and len(action['cases']) == 10 and max(row['action_difference_error'] for row in action['cases']) < 1e-10)
    check('kinetic_and_spatial_temporal_boundary_work_really_tested', any(abs(row['kinetic_time_boundary']) > 1e-5 and abs(row['spatial_time_boundary']) > 1e-8 for row in action['cases']) and max(row['full_adjoint_with_both_temporal_boundaries_error'] for row in action['cases']) < 1e-12)
    check('same_window_covariance_and_negative_controls_both_branches', len(action['covariance_cases']) == 2 and all(row['same_physical_window_full_action_covariance_error'] < 1e-12 and row['drop_J_negative_control_max'] > 1e-8 and row['wrong_B_time_weight_negative_control_max'] > 1e-6 and row['node_dependent_time_windows_not_identical_coordinate_bounds'] for row in action['covariance_cases']))
    refinement = action['smooth_refinement_not_interval_certificate']
    check('only_bounded16_32_64_manufactured_refinement', [row['intervals'] for row in refinement] == [16, 32, 64] and all(refinement[0][key] > refinement[1][key] > refinement[2][key] for key in ['kinetic_error', 'base_spatial_error', 'MTS_spatial_error', 'Gram_extra']))
    source = batches['annular-covariant-scalar-source-jet-attempt01']
    for row in source['cases']:
        check(row['branch'] + '_node_energy_work_includes_sources', row['node_energy_identity_max'] < 1e-12 and row['node_energy_identity_time_max'] < 1e-11 and row['port_work_without_source_subtraction_max'] > 1e-4)
        check(row['branch'] + '_C0_only_preparation_not_silently_mixed_with_old_jets', row['prepared_new_C0_max'] < 1e-10 and row['new_C0_on_old_geometry_max'] > .01 and row['first_and_second_jets_not_recomputed_on_prepared_mass'] and abs(row['new_outer_clock_gap_at_old_lapse']) > 1e-8)
    prepared = batches['annular-covariant-scalar-preparation-control-attempt01']
    for row in prepared['cases']:
        check(row['branch'] + '_higher_C0_pass_not_full_boundary_pass', row['higher_C0_max'] < 1e-10 and row['new_full_boundary_and_first_jet_problem_remains'] and abs(row['inner_mass_drive_gap_on_old_prescribed_metric_jet']) > 1e-4)
        check(row['branch'] + '_outer_targets_unapplied_source_changes_explicit', 1e-7 < abs(row['relative_required_outer_auxiliary_change']) < 1e-5)
    stems = ['annular_scalar_kinetic_pair', 'derive_annular_scalar_kinetic_pair', 'verify_annular_scalar_kinetic_ward', 'annular_covariant_scalar_action', 'derive_annular_covariant_scalar_action', 'verify_annular_covariant_scalar_source_jet', 'verify_annular_covariant_scalar_preparation', 'seal_annular_covariant_scalar']
    for stem in stems:
        path = root / 'scripts' / (stem + '_20260912.py')
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    check('eight_new_scripts_compile_without_bytecode', len(stems) == 8)
    note = root / 'DERIVATION-20260912-covariant-full-scalar-action-and-initial-constraint.md'
    for citation in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')):
        if citation.endswith(('.py', '.md', '.json', '.npz')):
            check('citation_exists_' + citation, (root / citation).is_file())
    own(note, 'outputs')
    protected = root.parent / 'formalization-workbench'
    check('protected_workbench_exists', protected.is_dir())
    start = datetime.fromisoformat('2026-09-12T18:36:21+00:00').timestamp()
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start]
    check('protected_workbench_modified_count_zero_mtime', not changed, changed)
    check('no_python_cache', not (root / 'scripts/__pycache__').exists())
    snapshot.write_bytes((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    own(snapshot, 'outputs')
    report['run_check_counts'] = {name: len(batch['checks']) for name, batch in batches.items()}
    report['action_covariance_cases'] = action['covariance_cases']
    report['source_jet_and_C0_only_cases'] = source['cases']
    report['new_C0_and_unapplied_boundary_controls'] = prepared['cases']
    report['protected_modified_count'] = len(changed)
    report['state'] = 'complete'
    report['completed_utc'] = datetime.now(timezone.utc).isoformat()
    destination.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'state': report['state'], 'seal_checks': len(report['checks']), 'run_check_counts': report['run_check_counts'], 'inputs': len(report['inputs']), 'outputs': len(report['outputs']), 'protected_modified_count': len(changed), 'new_action_derived': True, 'full_second_jet_closed': False, 'C0_only_roots_not_full_initial_data': True}), flush=True)


if __name__ == '__main__':
    run()
