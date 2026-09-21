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
    destination = intake / 'annular-history-ward-final-integrity.json'
    snapshot = intake / 'annular-history-ward-resume-snapshot.md'
    if destination.exists() or snapshot.exists():
        raise FileExistsError('Seals and resume snapshots are immutable.')
    report = {'state': 'running', 'checks': [], 'inputs': {}, 'outputs': {}, 'valid_for_physics_claim': False, 'new_evolution': False, 'full_second_jet_closed': False, 'interval_certificate': False, 'full_GR_limit_proven': False, 'history_time_Ward_derived': True, 'GR_off_shell_canonical_Ward_symbolically_proven': True, 'conditional_continuum_constraint_propagation_derived_for_this_action_sector': True, 'finite_onshell_solution_proven': False, 'scalar_frozen_enlargement_accepted': False, 'working_numerical_branch': 'annular-acceleration-trace-completion-attempt02', 'numerical_Ward_scope': '17 independent zero-endpoint lapse tests; NOT the two independent nonzero-endpoint rows', 'protected_scan_scope': 'mtime since 2026-09-12T16:11:04Z, not a pre-turn content snapshot'}
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
                check('immutable_' + name, digest(root / name) == expected)
                report['inputs'][name] = expected

    prior_path = intake / 'annular-second-jet-final-integrity.json'
    prior = json.loads(prior_path.read_text())
    check('previous_working_evidence_complete', prior['state'] == 'complete' and not prior['full_second_jet_closed'])
    inherit(prior)
    own(prior_path)
    names = ['annular-history-ward-attempt01', 'annular-history-ward-attempt02', 'annular-history-ward-symbolic-attempt01', 'annular-scalar-ward-completion-attempt01', 'annular-canonical-ward-control-attempt01', 'annular-canonical-ward-enlarged-control-attempt01']
    batches = {}
    for name in names:
        directory = intake / name
        batch = json.loads((directory / 'status.json').read_text())
        batches[name] = batch
        check(name + '_complete_all_validation_checks_pass', batch['state'] == 'complete' and all(row['passed'] for row in batch['checks']))
        check(name + '_not_a_physical_or_second_jet_pass', not batch['valid_for_physics_claim'] and not batch['new_evolution'] and not batch['full_second_jet_closed'])
        inherit(batch)
        for path in directory.iterdir():
            if path.is_file():
                own(path, 'outputs')
            if path.name.startswith('executed-'):
                check(name + '_executed_snapshot_matches', digest(path) == digest(root / 'scripts' / path.name.removeprefix('executed-')))
            if path.suffix == '.npz':
                with np.load(path, allow_pickle=False) as archive:
                    check(name + '_' + path.name + '_finite_arrays', all(np.isfinite(archive[key]).all() for key in archive.files))
    symbolic = batches['annular-history-ward-symbolic-attempt01']
    check('six_exact_symbolic_controls', len(symbolic['checks']) == 6 and symbolic['GR_off_shell_identity_proven_symbolically'] and symbolic['history_interior_identity_derived_with_exact_node_jumps'])
    for name, source in [('annular-canonical-ward-control-attempt01', 'annular-acceleration-trace-completion-attempt02'), ('annular-canonical-ward-enlarged-control-attempt01', 'annular-scalar-ward-completion-attempt01')]:
        batch = batches[name]
        check(name + '_both_branches_both_quadratures', {(row['branch'], row['variant']) for row in batch['cases']} == {(branch, variant) for branch in ['GR', 'metric_Gram'] for variant in ['primary', 'higher']})
        check(name + '_all_compact_Ward_errors_below_1e11', max(row['full_Ward_prediction_error'] for row in batch['cases']) < 1e-11)
        for row in batch['cases']:
            branch, variant = row['branch'], row['variant']
            path = intake / name / (branch + '_' + variant + '_ward_source_work.npz')
            saved_path = intake / source / (branch + ('_higher_second_jet.npz' if variant == 'higher' else '_completed_second_jet.npz'))
            with np.load(path, allow_pickle=False) as computed, np.load(saved_path, allow_pickle=False) as saved:
                error = float(abs(computed['compact_transform'].T @ saved['constraint_second'] - computed['actual']).max())
                check(name + '_' + branch + '_' + variant + '_replays_actual_saved_C2_on_all17_tests', error < 1e-9, error)
        for row in batch['memory_identity_cases']:
            check(name + '_' + row['variant'] + '_time_Ward_and_negative_control', row['Ward0_max'] < 1e-12 and row['Ward1_max'] < 1e-10 and row['wrong_two_instead_of_three_max'] > 1e-7)
    trial = batches['annular-scalar-ward-completion-attempt01']
    for row in trial['cases']:
        check(row['branch'] + '_failed_repair_preserved_not_adopted', row['primary_after_three_boundary_rows_only']['C2_max'] > row['baseline']['C2_max'] and not row['primary_after_three_boundary_rows_only']['full_second_jet_gate'] and not row['higher']['full_second_jet_gate'])
        check(row['branch'] + '_trial_keeps_first_jet_and_old_spaces', row['primary_after_three_boundary_rows_only']['first_jet_gate'] and row['higher']['first_jet_gate'] and row['completion']['original_modes_removed'] == 0 and max(row['original_span_errors'].values()) < 1e-8)
        check(row['branch'] + '_trial_pairing_well_conditioned_not_unreported_singular_fit', row['completion']['pairing_condition'] < 3 and row['no_C2_fitting'])
    stems = ['derive_annular_history_ward', 'derive_annular_history_ward_compact', 'verify_annular_history_ward_symbolic', 'derive_annular_scalar_ward_completion', 'verify_annular_canonical_ward_source_work', 'seal_annular_history_ward']
    for stem in stems:
        path = root / 'scripts' / (stem + '_20260912.py')
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    check('six_new_scripts_compile_without_bytecode', len(stems) == 6)
    note = root / 'DERIVATION-20260912-history-Ward-identity-and-scalar-projection.md'
    for citation in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')):
        if citation.endswith(('.py', '.md', '.json', '.npz')):
            check('citation_exists_' + citation, (root / citation).is_file())
    own(note, 'outputs')
    protected = root.parent / 'formalization-workbench'
    start = datetime.fromisoformat('2026-09-12T16:11:04+00:00').timestamp()
    check('protected_workbench_exists', protected.is_dir())
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start]
    check('protected_workbench_modified_zero_mtime', not changed, changed)
    check('no_python_cache', not (root / 'scripts/__pycache__').exists())
    snapshot.write_bytes((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    own(snapshot, 'outputs')
    report['run_check_counts'] = {name: len(batch['checks']) for name, batch in batches.items()}
    report['working_Ward_cases'] = batches['annular-canonical-ward-control-attempt01']['cases']
    report['rejected_enlargement_cases'] = trial['cases']
    report['rejected_enlargement_Ward_cases'] = batches['annular-canonical-ward-enlarged-control-attempt01']['cases']
    report['protected_modified_count'] = len(changed)
    report['state'] = 'complete'
    report['completed_utc'] = datetime.now(timezone.utc).isoformat()
    destination.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'state': report['state'], 'seal_checks': len(report['checks']), 'run_check_counts': report['run_check_counts'], 'inputs': len(report['inputs']), 'outputs': len(report['outputs']), 'protected_modified_count': len(changed), 'conditional_continuum_Ward_derived': True, 'full_second_jet_closed': False, 'scalar_enlargement_accepted': False}), flush=True)


if __name__ == '__main__':
    run()
