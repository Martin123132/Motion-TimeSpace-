from derive_annular_source_gravity_20260914 import EvidenceRun
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import re
import traceback


def main():
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    destination = intake/'annular-live-Gram-stress-final-integrity.json'
    snapshot = intake/'annular-live-Gram-stress-resume-snapshot.md'
    executed = intake/'annular-live-Gram-stress-executed-sealer.py'
    if any(path.exists() for path in [destination, snapshot, executed]):
        raise FileExistsError('Immutable evidence destination already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, no_forward_evolution=True,
        actual_retained_P2_Gram_diagonal_stress_derived=True,
        arbitrary_MTS_parent_stress_derived=False, full_live_P2_canonical_inverse_qualified=False,
        full_GR_limit_proven=False, valid_for_physics_claim=False, independently_reviewed_proof=False,
        original_action_unchanged=True, original_initial_data_unchanged=True,
        no_GitHub_action=True, subagents_used=False, implementation_checks_not_physics_passes=True,
        protected_scan_scope='mtime since2026-09-18T12:02:47Z; not a pre-turn full hash baseline')
    cache = {}

    def digest(path):
        path = path.resolve()
        if path not in cache:
            hasher = hashlib.sha256()
            with path.open('rb') as stream:
                while chunk := stream.read(1024*1024):
                    hasher.update(chunk)
            cache[path] = hasher.hexdigest()
        return cache[path]

    def own(path, table='inputs'):
        report[table][str(path.resolve().relative_to(root))] = digest(path)

    def save():
        destination.write_text(json.dumps(report, indent=2, allow_nan=False)+'\n', encoding='utf-8')

    def check(name, passed, detail=None):
        report['checks'].append(dict(name=name, passed=bool(passed), detail=detail))
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def inherit(path):
        status = json.loads(path.read_text())
        for table in ['inputs', 'outputs']:
            for name, expected in status[table].items():
                source = (root/name).resolve()
                key = str(source.relative_to(root))
                if not source.is_file() or digest(source) != expected:
                    raise RuntimeError('Missing or modified sealed source: '+name)
                if key in report['inputs'] and report['inputs'][key] != expected:
                    raise RuntimeError('Conflicting sealed hash: '+name)
                report['inputs'][key] = expected
        own(path)
        return status

    save()
    try:
        previous = inherit(intake/'annular-live-radial-response-final-integrity.json')
        check('preceding_seal_complete_and_hash_chain_preserved', previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks']))
        check('all_previous_failures_retained', previous['inherited_failed_attempts_preserved'] == 31
            and previous['inherited_peak_force_failures_preserved'] == 4)
        statuses = {}
        for name, count in [('annular-live-P2-Gram-stress-attempt01', 114),
                ('annular-live-P2-Gram-radial-attempt01', 42), ('annular-Gram-shape-L1-bound-attempt01', 30)]:
            status = inherit(intake/name/'status.json')
            statuses[name] = status
            check(name+'_completed', status['state'] == 'complete' and len(status['checks']) == count
                and all(row['passed'] for row in status['checks']))
            check(name+'_claim_scope_unchanged', not status['valid_for_physics_claim'] and not status['full_GR_limit_proven']
                and not status['full_live_P2_force_convergence_proven'] and status['no_forward_evolution']
                and status['original_action_unchanged'] and not status['github_action'] and not status['subagents_used'])
        stress = statuses['annular-live-P2-Gram-stress-attempt01']
        radial = statuses['annular-live-P2-Gram-radial-attempt01']
        shape = statuses['annular-Gram-shape-L1-bound-attempt01']
        expected = {(count, profile) for count in [33, 129, 257] for profile in ['original_profile', 'oscillatory_control']}
        check('both_profiles_all_three_original_P2_grids', all({(row['base_count'], row['profile']) for row in status['cases']}
            == expected for status in [stress, radial]))
        check('actual_Gram_metric_action_not_substituted_equation_of_state', stress['reference_and_MTS_action_difference_used']
            and stress['actual_retained_P2_Gram_stress_derived'] and stress['Gram_rho_equals_radial_pressure']
            and not stress['arbitrary_parent_MTS_stress_derived'] and stress['all_Gram_rows_retained'])
        check('independent_density_pushforward_and_negative_Jacobian_control',
            max(row['weak_relative_error'] for row in stress['cases']) < 3e-9
            and min(row['incorrect_width_relative_error'] for row in stress['cases']) > .001)
        check('radial_bounds_are_offshell_not_a_full_canonical_evolution', radial['offshell_canonical_density_constraint_resolves_only']
            and radial['finite_P2_canonical_momentum_inverse_not_qualified']
            and radial['actual_action_Gram_not_potential_substitution'] and radial['uniform_bounds_derived_not_fitted_to_samples'])
        check('source_shape_estimate_keeps_label_hypotheses', shape['unweighted_label_Gram_and_derivative_control_required']
            and shape['weighted_energy_alone_not_asserted_sufficient'] and not shape['uniform_in_label_resolution_proven']
            and not shape['zero_width_limit_proven'])
        old = json.loads((intake/'annular-initial-corner-response-final-integrity.json').read_text())
        check('all_four_original_force_gates_still_fail', len(old['comparison_results']) == 4
            and all(not row['original_peak_force_gate_pass'] for row in old['comparison_results']))
        note = root/'DERIVATION-20260918-action-derived-live-Gram-stress-and-shape.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json))`', content)
        check('all_cited_local_paths_exist', bool(cited) and all((root/name).is_file() for name in cited), cited)
        check('completed_derivation_records_results_and_limitations', '186 successful implementation checks' in content
            and 'PENDING' not in content and 'No new failed attempt' in content
            and 'not the complete dispersion relation' in content and 'OFF-SHELL constraint comparisons' in content)
        own(note)
        names = ['annular_live_gram_stress_20260918.py', 'qualify_annular_live_gram_stress_20260918.py',
            'qualify_annular_live_gram_radial_20260918.py', 'qualify_annular_Gram_shape_L1_bound_20260918.py',
            'seal_annular_live_Gram_stress_20260918.py']
        for name in names:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('all_new_scripts_compile_and_no_bytecode', not (root/'scripts/__pycache__').exists(), names)
        protected = root.parent/'formalization-workbench'
        timestamp = datetime(2026, 9, 18, 12, 2, 47, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*')
            if path.is_file() and path.stat().st_mtime >= timestamp]
        check('protected_workbench_mtime_changed_count_zero', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        check('resume_and_executed_sealer_snapshots_saved', True)
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(),
            total_successful_current_checks=186, distinct_files_rehashed=len(cache),
            inherited_failed_attempts_preserved=31, inherited_peak_force_failures_preserved=4,
            new_failed_attempts_preserved=[], results={name: status['cases'] for name, status in statuses.items()})
        save()
        print(json.dumps(dict(state='complete', integrity_checks=len(report['checks']), current_checks=186,
            rehashed_files=len(cache), protected_changed=len(changed), failed_attempts_preserved=31)), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
