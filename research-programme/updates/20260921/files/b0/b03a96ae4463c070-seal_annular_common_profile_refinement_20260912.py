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
    destination = intake / 'annular-common-profile-refinement-final-integrity.json'
    if destination.exists():
        raise FileExistsError('Sealed work is immutable.')
    report = {'state': 'running', 'inputs': {}, 'outputs': {}, 'checks': [], 'valid_for_physics_claim': False, 'new_evolution': False, 'interval_certificate': False, 'continuum_convergence_proven': False, 'full_GR_limit_proven': False, 'N128_run': False, 'protected_scan_scope': 'mtime since 2026-09-11T23:14:47Z; not a pre-turn content snapshot', 'resource_policy': 'one BelowNormal single-core Python at a time; no subagents or GitHub actions'}

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
                    raise RuntimeError('Evidence changed: ' + name)
                report['inputs'][name] = expected

    predecessor = root / 'source-intake/navier-stokes/20260911/annular-canonical-trace-final-integrity.json'
    previous = json.loads(predecessor.read_text())
    own(predecessor)
    check('predecessor_complete', previous['state'] == 'complete')
    inherit(previous)
    batches = {}
    for name in ['annular-common-profile-refinement-attempt01', 'annular-common-profile-refinement-attempt02', 'annular-common-profile-refinement-control-attempt01']:
        directory = intake / name
        batch = json.loads((directory / 'status.json').read_text())
        batches[name] = batch
        if name.endswith('refinement-attempt01'):
            check('original_failed_two_MTS_gates_preserved', batch['state'] == 'complete_with_failures' and sum(not row['passed'] for row in batch['checks']) == 2)
        else:
            check(name + '_complete_checks_pass', batch['state'] == 'complete' and all(row['passed'] for row in batch['checks']))
        check(name + '_claims_remain_limited', batch['valid_for_physics_claim'] is False and batch['new_evolution'] is False and batch['interval_certificate'] is False)
        inherit(batch)
        for path in directory.iterdir():
            if path.is_file():
                own(path, 'outputs')
        for path in directory.glob('executed-*.py'):
            check(path.stem + '_executed_source_unchanged', digest(path) == digest(root / 'scripts' / path.name[len('executed-'):]))
        for path in directory.glob('*.npz'):
            with numerical.load(path, allow_pickle=False) as archive:
                check(path.stem + '_all_arrays_finite', all(numerical.isfinite(archive[key]).all() for key in archive.files))
    completed = batches['annular-common-profile-refinement-attempt02']
    controls = batches['annular-common-profile-refinement-control-attempt01']
    report['cases'] = [{key: case[key] for key in ['label', 'state', 'intervals', 'branch', 'amplitudes', 'outcomes', 'survey_norms', 'Gram_base_quadratic_form']} for case in completed['cases']]
    report['physical_refinement'] = completed['comparisons']
    report['matched_GR_comparison'] = completed['matched_branch_comparisons']
    report['convergence_ratios'] = controls['convergence_ratios']
    report['conditional_endpoint_bound'] = controls['conditional_endpoint_bound']
    check('complete_paired_three_grid_matrix', {(case['intervals'], case['branch']) for case in completed['cases']} == {(intervals, branch) for intervals in [16, 32, 64] for branch in ['GR', 'metric_Gram']})
    for case in completed['cases']:
        label = case['label']
        check(label + '_all_constraints_boundary_and_clock_pass', case['finite_initial_identity_gate'] and all(max(row['C_max'], row['Cdot_max'], abs(row['mass_drive_gap']), abs(row['outer_scalar_drive_gap']), abs(row['clock_gap'])) < 1e-10 for row in case['outcomes'].values()))
        check(label + '_same_free_physical_profile', max(case['transfer_errors_before_boundary_preparation'].values()) < 1e-10)
        diagnostic = case['trace_extension']
        check(label + '_full_kernel_family_no_deletion', diagnostic['parent_family_dimension'] == case['intervals'] and diagnostic['no_parent_family_modes_discarded'] and diagnostic['all_kernel_family_trace_error'] < 1e-10)
        check(label + '_original_phase_directions_retained', all(row['original_modes_removed'] == 0 for row in case['completion'].values()))
        check(label + '_well_conditioned_pairing', diagnostic['new_pairing_condition'] < 2 and diagnostic['block_pairing_error'] < 1e-10)
    check('all_physical_differences_decrease_both_branches', len(controls['convergence_ratios']) == 2 and all(max(row['fine_difference_over_coarse_difference'].values()) < 1 for row in controls['convergence_ratios']))
    for branch in ['GR', 'metric_Gram']:
        case = next(row for row in completed['cases'] if row['intervals'] == 64 and row['branch'] == branch)
        comparison = next(row for row in completed['comparisons'] if row['fine'] == 64 and row['branch'] == branch)
        report[branch + '_last_step_relative_gradient_change'] = comparison['physical_L2_differences']['mu_r'] / case['survey_norms']['mu_r_L2']
        check(branch + '_slow_gradient_resolution_not_hidden', report[branch + '_last_step_relative_gradient_change'] > .1)
        if branch == 'metric_Gram':
            report['MTS_last_step_relative_pi_rate_change'] = comparison['physical_L2_differences']['pi_t'] / case['survey_norms']['pi_t_L2']
    check('six_inherited_breaks_in_both_fine_controls', all(len(row['inherited_knots_absent_from_old_split']) == 6 for row in controls['knot_controls'] if row['intervals'] > 16))
    check('exact_hinge_controls_and_original_failure', all(row['new_hinge_integral_error'] < 1e-14 and row['new_partial_hinge_error'] < 1e-14 for row in controls['knot_controls']) and all(row['old_hinge_integral_error'] > 1e-10 for row in controls['knot_controls'] if row['intervals'] > 16))
    check('full_Gram_load_repaired', controls['fixed_N32_load_control']['weak_load_error'] < 1e-11)
    diagnosis = intake / 'annular-refined-kernel-load-diagnosis-attempt01.json'
    own(diagnosis, 'outputs')
    check('diagnosis_complete', json.loads(diagnosis.read_text())['state'] == 'complete')
    scripts = ['annular_canonical_common_profile_refinement_20260912.py', 'derive_annular_common_profile_refinement_20260912.py', 'diagnose_annular_refined_kernel_load_20260912.py', 'annular_inherited_knot_link_quadrature_20260912.py', 'annular_canonical_common_profile_aligned_20260912.py', 'derive_annular_common_profile_aligned_20260912.py', 'verify_annular_common_profile_refinement_20260912.py', Path(__file__).name]
    for name in scripts:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    check('eight_new_scripts_compile_without_bytecode', True)
    note = root / 'DERIVATION-20260912-common-profile-refinement-and-inherited-knot-repair.md'
    for citation in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')):
        if citation.endswith(('.py', '.md', '.json', '.npz')):
            check('citation_exists_' + citation, (root / citation).is_file())
    own(note, 'outputs')
    protected = root.parent / 'formalization-workbench'
    check('protected_workbench_exists', protected.is_dir())
    started = datetime.fromisoformat('2026-09-11T23:14:47+00:00').timestamp()
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > started]
    report['protected_modified_count'] = len(changed)
    check('protected_modified_count_zero_mtime', not changed, changed)
    check('no_python_cache', not (root / 'scripts/__pycache__').exists())
    snapshot = intake / 'annular-common-profile-refinement-resume-snapshot.md'
    if snapshot.exists():
        raise FileExistsError(snapshot)
    snapshot.write_bytes((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    own(snapshot, 'outputs')
    report['state'] = 'complete'
    report['completed_utc'] = datetime.now(timezone.utc).isoformat()
    destination.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'state': report['state'], 'seal_checks': len(report['checks']), 'run_checks': len(completed['checks']), 'independent_checks': len(controls['checks']), 'inputs': len(report['inputs']), 'outputs': len(report['outputs']), 'protected_modified_count': len(changed), 'matched_relative_gradient_changes': {branch: report[branch + '_last_step_relative_gradient_change'] for branch in ['GR', 'metric_Gram']}, 'MTS_relative_pi_rate_change': report['MTS_last_step_relative_pi_rate_change']}), flush=True)


if __name__ == '__main__':
    run()
