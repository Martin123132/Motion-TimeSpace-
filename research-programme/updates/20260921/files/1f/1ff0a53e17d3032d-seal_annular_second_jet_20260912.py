import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260912'
    destination = intake / 'annular-second-jet-final-integrity.json'
    snapshot = intake / 'annular-second-jet-resume-snapshot.md'
    if destination.exists() or snapshot.exists():
        raise FileExistsError('Completed seals and resume snapshots are immutable.')
    report = {'state': 'running', 'checks': [], 'inputs': {}, 'outputs': {}, 'valid_for_physics_claim': False, 'new_evolution': False, 'interval_certificate': False, 'full_GR_limit_proven': False, 'full_second_jet_closed': False, 'MTS_full_constraint_propagation_identity_proven': False, 'GR_interior_constraint_bracket_derived': True, 'formal_interior_time_germ_only': True, 'new_initial_physical_fields': False, 'phase_maps_extended_explicitly': True, 'drive_accelerations_parent_owned': False, 'protected_scan_scope': 'mtime since 2026-09-12T15:27:33Z, not a pre-turn content snapshot', 'resource_policy': 'one BelowNormal single-core Python at a time; no subagents, GitHub actions or new evolution'}
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
                    raise RuntimeError('Changed evidence: ' + name)
                report['inputs'][name] = expected

    previous_path = intake / 'annular-cubic-boundary-final-integrity.json'
    previous = json.loads(previous_path.read_text())
    own(previous_path)
    check('preceding_first_jet_seal_complete', previous['state'] == 'complete' and previous['finite_initial_boundary_first_jet_pass'] and all(row['passed'] for row in previous['checks']))
    inherit(previous)
    names = ['annular-frozen-second-jet-attempt01', 'annular-frozen-second-jet-attempt02', 'annular-frozen-second-jet-control-attempt01', 'annular-frozen-second-jet-control-attempt02', 'annular-frozen-second-jet-control-attempt03', 'annular-acceleration-trace-completion-attempt01', 'annular-acceleration-trace-completion-attempt02', 'annular-acceleration-memory-control-attempt01', 'annular-second-constraint-owner-attempt01']
    batches = {}
    for name in names:
        directory = intake / name
        batch = json.loads((directory / 'status.json').read_text())
        batches[name] = batch
        failed = [row['name'] for row in batch.get('checks', []) if not row['passed']]
        if name == 'annular-frozen-second-jet-attempt01':
            check(name + '_complex_cast_failure_preserved', batch['state'] == 'failed' and not failed and 'UFuncTypeError' in batch['error'])
        elif name == 'annular-frozen-second-jet-control-attempt01':
            check(name + '_finite_difference_failure_preserved', batch['state'] == 'failed' and failed == ['GR_actual_action_Cddot_independent_time_differences'])
        else:
            check(name + '_complete_no_failed_validation', batch['state'] == 'complete' and not failed)
        check(name + '_no_physics_or_evolution_claim', not batch['valid_for_physics_claim'] and not batch['new_evolution'] and not batch['interval_certificate'])
        inherit(batch)
        for path in directory.iterdir():
            if path.is_file():
                own(path, 'outputs')
            if path.name.startswith('executed-') and path.suffix == '.py':
                check(name + '_' + path.name + '_matches_executed_source', digest(path) == digest(root / 'scripts' / path.name.removeprefix('executed-')))
            if path.suffix == '.npz':
                with numerical.load(path, allow_pickle=False) as archive:
                    check(name + '_' + path.name + '_finite_arrays', all(numerical.isfinite(archive[key]).all() for key in archive.files))
    original = (root / 'scripts/annular_frozen_second_jet_20260912.py').read_text()
    corrected = (root / 'scripts/annular_frozen_second_jet_complex_20260912.py').read_text()
    check('complex_step_fix_changes_only_in_place_current_addition', original.replace('current_first += self.amplitude[links.factor]', 'current_first = current_first + self.amplitude[links.factor]') == corrected)
    frozen = batches['annular-frozen-second-jet-attempt02']
    check('frozen_second_jet_failures_not_promoted', not frozen['boundary_accelerations_parent_owned'] and frozen['formal_interior_time_germ_only'] and all(not row['primary']['finite_second_jet_gate'] for case in frozen['cases'] for row in case['solutions']))
    action = batches['annular-frozen-second-jet-control-attempt03']
    check('eight_independent_full_action_checks_pass', len(action['checks']) == 8 and all(row['passed'] for row in action['checks']))
    check('all_four_accelerations_have_independent_action_validation', max(action['cases'][0]['GR_action_second_rate_errors'].values()) < 1e-8 and max(action['cases'][1]['MTS_all_four_action_acceleration_errors'].values()) < 1e-8)
    joint = batches['annular-acceleration-trace-completion-attempt02']
    check('joint_full_second_jet_gate_still_false_both_branches', len(joint['cases']) == 2 and {row['branch'] for row in joint['cases']} == {'GR', 'metric_Gram'} and all(not row['finite_full_second_jet_gate'] for row in joint['cases']))
    check('joint_repair_keeps_all_mass_and_scalar_families', all(row['completion']['parent_family_dimension'] == 35 and row['completion']['resolved_residual_rank'] == 35 and row['scalar_completion']['parent_family_dimension'] == 19 and row['scalar_completion']['resolved_residual_rank'] == 19 and row['completion']['no_parent_family_modes_discarded'] and row['scalar_completion']['no_parent_family_modes_discarded'] for row in joint['cases']))
    control = batches['annular-acceleration-memory-control-attempt01']
    check('twenty_six_repaired_frame_and_carrier_checks_pass', len(control['checks']) == 26 and all(row['passed'] for row in control['checks']))
    check('higher_quadrature_second_trace_failure_not_hidden', max(abs(value) for row in control['cases'] if row['variant'] == 'higher' for value in row['Pddot_endpoints']) > 1e-10)
    check('GR_remaining_constraint_owned_by_derived_bracket', all(row['GR_bracket_prediction_error'] < 3e-8 for row in control['cases'] if row['branch'] == 'GR'))
    check('MTS_remaining_constraint_is_not_claimed_as_boundary_only', all(row['residual_after_boundary_covector_max'] > .006 and row['boundary_covector_max'] < 1e-7 for row in control['cases'] if row['branch'] == 'metric_Gram'))
    check('derived_memory_time_carriers_numerically_verified', all(row['memory_time_carrier_weak_error'] < 1e-8 and row['memory_time_anchor_jump_cancellation'] < 1e-9 for row in control['cases'] if row['branch'] == 'metric_Gram'))
    owner = batches['annular-second-constraint-owner-attempt01']
    check('naive_MTS_full_nodal_bracket_hypothesis_rejected', not owner['MTS_full_bracket_identity_proven'] and len(owner['cases']) == 4 and all(not row['full_nodal_candidate_matches_at_1e8_gate'] and row['full_nodal_candidate_error'] > .006 for row in owner['cases'] if row['branch'] == 'metric_Gram'))
    report['action_control_cases'] = action['cases']
    report['final_joint_trace_cases'] = joint['cases']
    report['final_constraint_and_carrier_cases'] = control['cases']
    report['rejected_nodal_bracket_cases'] = owner['cases']
    report['run_check_counts'] = {name: len(batch.get('checks', [])) for name, batch in batches.items()}
    stems = ['annular_frozen_second_jet', 'derive_annular_frozen_second_jet', 'annular_frozen_second_jet_complex', 'derive_annular_frozen_second_jet_complex', 'verify_annular_frozen_second_jet', 'verify_annular_frozen_second_jet_extrapolated', 'verify_annular_full_second_jet_action', 'annular_acceleration_trace_completion', 'derive_annular_acceleration_trace_completion', 'derive_annular_joint_acceleration_trace_completion', 'verify_annular_acceleration_trace_and_memory_carrier', 'derive_annular_second_constraint_owner', 'seal_annular_second_jet']
    for stem in stems:
        path = root / 'scripts' / (stem + '_20260912.py')
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    check('all_thirteen_new_scripts_compile_without_bytecode', len(stems) == 13)
    note = root / 'DERIVATION-20260912-full-second-jet-and-constraint-propagation.md'
    for citation in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')):
        if citation.endswith(('.py', '.md', '.json', '.npz')):
            check('citation_exists_' + citation, (root / citation).is_file())
    own(note, 'outputs')
    protected = root.parent / 'formalization-workbench'
    check('protected_workbench_exists', protected.is_dir())
    start = datetime.fromisoformat('2026-09-12T15:27:33+00:00').timestamp()
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start]
    report['protected_modified_count'] = len(changed)
    check('protected_modified_count_zero_mtime', not changed, changed)
    check('no_python_cache', not (root / 'scripts/__pycache__').exists())
    snapshot.write_bytes((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    own(snapshot, 'outputs')
    report['state'] = 'complete'
    report['completed_utc'] = datetime.now(timezone.utc).isoformat()
    destination.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'state': report['state'], 'seal_checks': len(report['checks']), 'joint_trace_checks': len(joint['checks']), 'full_action_checks': len(action['checks']), 'repaired_frame_and_carrier_checks': len(control['checks']), 'inputs': len(report['inputs']), 'outputs': len(report['outputs']), 'protected_modified_count': len(changed), 'full_second_jet_closed': False, 'new_evolution': False}), flush=True)


if __name__ == '__main__':
    run()
