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
    destination = intake / 'annular-cubic-boundary-final-integrity.json'
    snapshot = intake / 'annular-cubic-boundary-resume-snapshot.md'
    if destination.exists() or snapshot.exists():
        raise FileExistsError('Completed seal and resume snapshot are immutable.')
    report = {
        'state': 'running', 'checks': [], 'inputs': {}, 'outputs': {},
        'valid_for_physics_claim': False, 'new_evolution': False,
        'interval_certificate': False, 'full_GR_limit_proven': False,
        'finite_initial_boundary_first_jet_pass': False,
        'full_second_jet_solved': False, 'new_mesh_intervals': [16],
        'inner_mass_tolerance': 2e-13, 'external_gate_tolerance': 1e-10,
        'finite_gravity_action_quadrature_changed_explicitly': True,
        'physical_coupling_fitted': False,
        'resource_policy': 'one BelowNormal single-core Python at a time; no subagents or GitHub actions',
        'protected_scan_scope': 'mtime since 2026-09-12T12:03:18Z, not a pre-turn content snapshot',
    }
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
                path = root / name
                if digest(path) != expected:
                    raise RuntimeError('Changed evidence: ' + name)
                report['inputs'][name] = expected

    previous_path = intake / 'annular-bounded-nonlinear-final-integrity.json'
    previous = json.loads(previous_path.read_text())
    own(previous_path)
    check('preceding_seal_complete_all_checks_pass', previous['state'] == 'complete' and all(row['passed'] for row in previous['checks']))
    inherit(previous)
    batches = {}
    for number in range(1, 8):
        name = 'annular-cubic-lapse-boundary-attempt' + str(number).zfill(2)
        directory = intake / name
        batch = json.loads((directory / 'status.json').read_text())
        batches[number] = batch
        failures = [row['name'] for row in batch['checks'] if not row['passed']]
        if number == 1:
            check(name + '_primitive_origin_failure_preserved', batch['state'] == 'failed' and not batch['cases'] and failures == ['GR_two_mass_lifts_preserve_endpoint_values'])
        elif number in [5, 6]:
            expected_states = {'GR': 'failed', 'metric_Gram': 'failed' if number == 5 else 'complete'}
            actual_states = {row['label'].removesuffix('_corrected'): row['state'] for row in batch['cases']}
            check(name + '_strict_inner_solve_failures_preserved', batch['state'] == 'complete_with_failures' and actual_states == expected_states and not failures)
            check(name + '_only_declared_stall_errors', all('Nineteen-row mass preparation stalled.' in row['error'] for row in batch['cases'] if row['state'] == 'failed'))
        else:
            check(name + '_complete_all_checks_pass', batch['state'] == 'complete' and not failures)
            if number in [2, 3, 4]:
                check(name + '_failed_classical_trace_not_promoted', all(row['finite_initial_gate'] and not row['classical_P_trace_tangent_gate'] for row in batch['cases']))
        check(name + '_limited_claim_flags', not batch['valid_for_physics_claim'] and not batch['new_evolution'] and not batch['interval_certificate'])
        inherit(batch)
        for path in directory.iterdir():
            if path.is_file():
                own(path, 'outputs')
        for path in directory.glob('executed-*.py'):
            check(name + '_' + path.name + '_matches_source', digest(path) == digest(root / 'scripts' / path.name.removeprefix('executed-')))
        for path in directory.glob('*.npz'):
            with numerical.load(path, allow_pickle=False) as archive:
                check(name + '_' + path.name + '_finite_arrays', all(numerical.isfinite(archive[key]).all() for key in archive.files))
    final = batches[7]
    check('both_matched_branches_final_gates_pass', len(final['cases']) == 2 and {row['branch'] for row in final['cases']} == {'GR', 'metric_Gram'} and all(row['state'] == 'complete' and row['finite_initial_gate'] and row['classical_P_trace_tangent_gate'] for row in final['cases']))
    for case in final['cases']:
        branch = case['branch']
        check(branch + '_all_original_modes_retained', all(row['original_modes_removed'] == 0 for row in case['completion'].values()))
        node = case['completion']['mass']['nodal_trace_completion']
        check(branch + '_all_fifteen_nodal_sources_without_amplitude_fit', node['all_interior_nodal_source_directions'] == 15 and node['not_source_amplitude_fitted'] and node['original_modes_removed'] == 0 and node['all_nodal_source_trace_error'] < 1e-10)
        trace = case['trace_extension']
        check(branch + '_all_sixteen_parent_kernel_directions_retained', trace['parent_family_dimension'] == 16 and trace['no_parent_family_modes_discarded'] and trace['all_kernel_family_trace_error'] < 1e-10)
        for variant, values in case['outcomes'].items():
            residuals = [values[key] for key in ['C_max', 'Cdot_max', 'mass_drive_gap', 'outer_q_gap', 'clock_gap']]
            residuals += values['mass_trace_gaps'] + values['Pdot_endpoints']
            check(branch + '_' + variant + '_unchanged_external_gates', max(abs(value) for value in residuals) < 1e-10)
            check(branch + '_' + variant + '_sampled_positive_chart_not_interval', values['minimum_sampled_N'] > 0 and values['minimum_sampled_F'] > 0)
            path = intake / 'annular-cubic-lapse-boundary-attempt07' / (case['label'] + '_' + variant + '.npz')
            with numerical.load(path, allow_pickle=False) as archive:
                check(branch + '_' + variant + '_all_nineteen_rows_saved', archive['constraint'].shape == (19,) and archive['constraint_rate'].shape == (19,))
                check(branch + '_' + variant + '_saved_residuals_match_report', float(abs(archive['constraint']).max()) == values['C_max'] and float(abs(archive['constraint_rate']).max()) == values['Cdot_max'] and numerical.array_equal(archive['P_t_nodes'][[0, -1]], values['Pdot_endpoints']))
    report['final_cases'] = [{key: case[key] for key in ['label', 'outcomes', 'finite_initial_gate', 'classical_P_trace_tangent_gate']} for case in final['cases']]
    report['attempt_outcomes'] = {str(number): {'state': batch['state'], 'checks': len(batch['checks']), 'case_states': {case['label']: case['state'] for case in batch['cases']}} for number, batch in batches.items()}
    diagnosis_path = intake / 'annular-cubic-Ptrace-diagnosis-attempt01.json'
    diagnosis = json.loads(diagnosis_path.read_text())
    inherit(diagnosis)
    own(diagnosis_path, 'outputs')
    check('independent_old_trace_decomposition_reconstructs_four_cases', diagnosis['state'] == 'complete' and not diagnosis['valid_for_physics_claim'] and len(diagnosis['cases']) == 4 and max(row['decomposition_error'] for row in diagnosis['cases']) < 1e-15)
    directory = intake / 'annular-cubic-boundary-control-attempt01'
    control = json.loads((directory / 'status.json').read_text())
    inherit(control)
    check('independent_controls_all_twenty_one_pass', control['state'] == 'complete' and len(control['checks']) == 21 and all(row['passed'] for row in control['checks']))
    check('independent_control_remains_nonclaim_no_evolution', not control['valid_for_physics_claim'] and not control['new_evolution'] and not control['interval_certificate'])
    check('next_clock_rates_unapplied_candidates_only', control['next_lapse_rates_are_candidates_only'] and all(row['next_lapse_candidate_only'] for row in control['cases']))
    for path in directory.iterdir():
        if path.is_file():
            own(path, 'outputs')
        if path.name.startswith('executed-') and path.suffix == '.py':
            check(path.name + '_matches_source', digest(path) == digest(root / 'scripts' / path.name.removeprefix('executed-')))
        if path.suffix == '.npz':
            with numerical.load(path, allow_pickle=False) as archive:
                check(path.name + '_candidate_arrays_finite', all(numerical.isfinite(archive[key]).all() for key in archive.files))
    report['independent_control_cases'] = control['cases']
    script_names = [
        'annular_cubic_lapse_boundary', 'derive_annular_cubic_lapse_boundary',
        'annular_cubic_lapse_boundary_fixed', 'derive_annular_cubic_lapse_boundary_fixed',
        'diagnose_annular_cubic_Ptrace', 'annular_cubic_lapse_boundary_polynomial',
        'derive_annular_cubic_lapse_boundary_polynomial', 'annular_cubic_lapse_nodal_trace',
        'derive_annular_cubic_lapse_nodal_trace', 'annular_cubic_lapse_integrated_gravity',
        'derive_annular_cubic_lapse_integrated_gravity', 'annular_cubic_lapse_reference_gravity',
        'derive_annular_cubic_lapse_reference_gravity', 'annular_cubic_lapse_final_boundary',
        'derive_annular_cubic_lapse_final_boundary', 'verify_annular_cubic_final_boundary',
        'seal_annular_cubic_boundary',
    ]
    for stem in script_names:
        path = root / 'scripts' / (stem + '_20260912.py')
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    check('seventeen_new_scripts_compile_without_bytecode', len(script_names) == 17)
    note = root / 'DERIVATION-20260912-applied-cubic-clock-and-two-sided-boundary-first-jet.md'
    for citation in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')):
        if citation.endswith(('.py', '.md', '.json', '.npz')):
            check('citation_exists_' + citation, (root / citation).is_file())
    own(note, 'outputs')
    protected = root.parent / 'formalization-workbench'
    check('protected_workbench_exists', protected.is_dir())
    started = datetime.fromisoformat('2026-09-12T12:03:18+00:00').timestamp()
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > started]
    report['protected_modified_count'] = len(changed)
    check('protected_modified_count_zero_mtime', not changed, changed)
    check('no_python_cache', not (root / 'scripts/__pycache__').exists())
    snapshot.write_bytes((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    own(snapshot, 'outputs')
    report['finite_initial_boundary_first_jet_pass'] = True
    report['state'] = 'complete'
    report['completed_utc'] = datetime.now(timezone.utc).isoformat()
    destination.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'state': report['state'], 'seal_checks': len(report['checks']), 'paired_run_checks': len(final['checks']), 'independent_controls': len(control['checks']), 'inputs': len(report['inputs']), 'outputs': len(report['outputs']), 'protected_modified_count': len(changed), 'finite_initial_boundary_first_jet_pass': True, 'new_evolution': False, 'valid_for_physics_claim': False}), flush=True)


if __name__ == '__main__':
    run()
