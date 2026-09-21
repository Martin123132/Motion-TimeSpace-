import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    from annular_nonlinear_history_20260912 import CanonicalGeometry, ManufacturedHistory, HistoryAction

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260912'
    destination = intake / 'annular-bounded-nonlinear-final-integrity.json'
    if destination.exists():
        raise FileExistsError('Completed seal is immutable.')
    report = {'state': 'running', 'checks': [], 'inputs': {}, 'outputs': {}, 'valid_for_physics_claim': False, 'new_evolution': False, 'interval_certificate': False, 'N128_run': True, 'N256_run': False, 'full_GR_limit_proven': False, 'full_nonlinear_history_equations_derived_conditionally': True, 'physical_initial_lapse_changed': False, 'protected_scan_scope': 'mtime since 2026-09-12T10:13:59Z, not a pre-turn content snapshot', 'resource_policy': 'one BelowNormal single-core Python at a time; no subagents, GitHub actions or owned persistent jobs'}

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = digest(path)

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    def inherit(batch):
        for table in ['inputs', 'outputs']:
            for name, expected in batch[table].items():
                if digest(root / name) != expected:
                    raise RuntimeError('Changed evidence: ' + name)
                report['inputs'][name] = expected

    prior = intake / 'annular-common-profile-refinement-final-integrity.json'
    own(prior)
    prior_status = json.loads(prior.read_text())
    check('preceding_spatial_seal_complete', prior_status['state'] == 'complete')
    inherit(prior_status)
    batches = {}
    names = ['annular-bounded-N128-attempt01', 'annular-bounded-N128-attempt02', 'annular-bounded-N128-control-attempt01', 'annular-nonlinear-history-attempt01', 'annular-nonlinear-history-attempt02']
    for name in names:
        directory = intake / name
        batch = json.loads((directory / 'status.json').read_text())
        batches[name] = batch
        if name == 'annular-bounded-N128-attempt01':
            check(name + '_failed_archive_write_preserved', batch['state'] == 'complete_with_failures' and all('NpzFile' in row['error'] for row in batch['cases']))
        elif name == 'annular-nonlinear-history-attempt01':
            check(name + '_failed_diagnostic_preserved', batch['state'] == 'failed' and len(batch['cases']) == 7 and sum(not row['passed'] for row in batch['checks']) == 1 and batch['checks'][-1]['name'] == 'omitted_time_boundary_rejected')
        else:
            check(name + '_complete_all_checks_pass', batch['state'] == 'complete' and all(row['passed'] for row in batch['checks']))
        check(name + '_limited_claim_flags', not batch['valid_for_physics_claim'] and not batch['new_evolution'] and not batch['interval_certificate'])
        inherit(batch)
        for path in directory.iterdir():
            if path.is_file():
                own(path, 'outputs')
        for path in directory.glob('executed-*.py'):
            check(path.name + '_snapshot_matches_source', digest(path) == digest(root / 'scripts' / path.name[len('executed-'):]))
        for path in directory.glob('*.npz'):
            with numerical.load(path, allow_pickle=False) as archive:
                check(path.name + '_all_arrays_finite', all(numerical.isfinite(archive[key]).all() for key in archive.files))
    initial_runner = (root / 'scripts/derive_annular_bounded_128_20260912.py').read_text()
    fixed_runner = (root / 'scripts/derive_annular_bounded_128_fixed_20260912.py').read_text()
    expected_runner = initial_runner.replace('with numerical.load(path, allow_pickle=False) as archive:\n                surveys[(64, branch)] = {key: archive[key].copy() for key in archive.files}', 'with numerical.load(path, allow_pickle=False) as saved_lower:\n                surveys[(64, branch)] = {key: saved_lower[key].copy() for key in saved_lower.files}')
    check('N128_fix_only_archive_variable_shadow', expected_runner == fixed_runner)
    initial_history = (root / 'scripts/derive_annular_nonlinear_history_20260912.py').read_text()
    fixed_history = (root / 'scripts/derive_annular_nonlinear_history_control_20260912.py').read_text()
    check('history_fix_only_negative_control_scale', initial_history.replace("all(abs(row['primary']['boundary']) > 1e-10 for row in boundary_cases)", "all(abs(row['primary']['boundary']) > 100 * max(row['raw_adjoint_error'], 1e-15) for row in boundary_cases)") == fixed_history)
    spatial = batches['annular-bounded-N128-attempt02']
    control = batches['annular-bounded-N128-control-attempt01']
    history = batches['annular-nonlinear-history-attempt02']
    check('both_N128_branches_all_gates_pass', {(row['intervals'], row['branch']) for row in spatial['cases']} == {(128, 'GR'), (128, 'metric_Gram')} and all(row['finite_initial_identity_gate'] for row in spatial['cases']))
    check('N128_failure_did_not_change_computed_primary_results', all(old['outcomes']['primary'] == new['outcomes']['primary'] for old, new in zip(batches['annular-bounded-N128-attempt01']['cases'], spatial['cases'])))
    check('history_rescaling_did_not_change_results', batches['annular-nonlinear-history-attempt01']['cases'] == history['cases'])
    report['spatial_cases'] = [{key: case[key] for key in ['label', 'outcomes', 'survey_norms', 'Gram_base_quadratic_form']} for case in spatial['cases']]
    report['spatial_comparisons'] = control['comparisons']
    report['matched_branch_comparisons'] = spatial['matched_branch_comparisons']
    report['endpoint_bounds'] = control['endpoint_bounds']
    report['boundary_trace_diagnostics'] = control['boundary_trace_diagnostics']
    report['nonlinear_cases'] = history['cases']
    check('all_original_phase_modes_retained', all(all(item['original_modes_removed'] == 0 for item in case['completion'].values()) for case in spatial['cases']))
    check('all_parent_kernel_modes_retained', all(case['trace_extension']['parent_family_dimension'] == 128 and case['trace_extension']['no_parent_family_modes_discarded'] for case in spatial['cases']))
    check('endpoint_finite_bounds_pass_not_uniform_claims', len(control['endpoint_bounds']) == 4 and all(row['force_over_bound'] <= 1 and row['not_uniform_history_or_interval_bound'] for row in control['endpoint_bounds']))
    check('unapplied_boundary_candidates_no_new_initial_state', all(row['candidate_not_applied'] and row['candidate_requires_exact_P1_plus_global_cubic_representation'] for row in control['boundary_trace_diagnostics']))
    geometry = CanonicalGeometry()
    for name, fields in [('negative_F', [4., .9, .1, 0.]), ('negative_N', [1., -.9, .1, 0.]), ('shift_chart_failure', [1., .9, 20., 0.])]:
        rejected = False
        with numerical.errstate(invalid='ignore', divide='ignore'):
            try:
                geometry.evaluate(numerical.array([6.]), numerical.array(fields)[:, None])
            except ValueError:
                rejected = True
        check('nonlinear_chart_rejects_' + name, rejected)

    class ConstantScalarHistory(ManufacturedHistory):
        def evaluate(self, time, radius, direction, amplitude=0):
            fields = super().evaluate(time, radius, direction, amplitude)
            for index, group in enumerate(fields):
                group[3] = .7 if index == 0 else 0.
            return fields

    zero_action = HistoryAction(ConstantScalarHistory()).integrated([1, 1, 1, 1])
    report['constant_scalar_nonlinear_control'] = zero_action
    check('constant_scalar_has_no_Gram_action_or_force_at_nonzero_P', max(abs(zero_action[key]) for key in ['action', 'raw', 'adjoint', 'transport', 'direct', 'boundary']) < 1e-25)
    scripts = ['annular_canonical_bounded_128_20260912.py', 'derive_annular_bounded_128_20260912.py', 'derive_annular_bounded_128_fixed_20260912.py', 'verify_annular_bounded_128_20260912.py', 'annular_nonlinear_history_20260912.py', 'derive_annular_nonlinear_history_20260912.py', 'derive_annular_nonlinear_history_control_20260912.py', Path(__file__).name]
    for name in scripts:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    check('all_new_scripts_compile_without_bytecode', True)
    for name in ['DERIVATION-20260912-nonlinear-history-Euler-equations.md', 'DERIVATION-20260912-bounded-N128-and-nonlinear-continuation.md']:
        path = root / name
        for citation in re.findall(r'`([^`]+)`', path.read_text(encoding='utf-8')):
            if citation.endswith(('.py', '.md', '.json', '.npz')):
                check('citation_exists_' + citation, (root / citation).is_file())
        own(path, 'outputs')
    protected = root.parent / 'formalization-workbench'
    check('protected_workbench_exists', protected.is_dir())
    started = datetime.fromisoformat('2026-09-12T10:13:59+00:00').timestamp()
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > started]
    report['protected_modified_count'] = len(changed)
    check('protected_modified_count_zero_mtime', not changed, changed)
    check('no_python_cache', not (root / 'scripts/__pycache__').exists())
    snapshot = intake / 'annular-bounded-nonlinear-resume-snapshot.md'
    if snapshot.exists():
        raise FileExistsError(snapshot)
    snapshot.write_bytes((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    own(snapshot, 'outputs')
    report['state'] = 'complete'
    report['completed_utc'] = datetime.now(timezone.utc).isoformat()
    destination.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'state': report['state'], 'seal_checks': len(report['checks']), 'spatial_run_checks': len(spatial['checks']), 'independent_spatial_checks': len(control['checks']), 'nonlinear_checks': len(history['checks']), 'inputs': len(report['inputs']), 'outputs': len(report['outputs']), 'protected_modified_count': len(changed)}), flush=True)


if __name__ == '__main__':
    run()
