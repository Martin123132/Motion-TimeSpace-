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
    destination = intake/'annular-nonlinear-initial-force-final-integrity.json'
    snapshot = intake/'annular-nonlinear-initial-force-resume-snapshot.md'
    executed = intake/'annular-nonlinear-initial-force-executed-sealer.py'
    if any(path.exists() for path in [destination, snapshot, executed]):
        raise FileExistsError('Immutable evidence already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, full_GR_limit_proven=False,
        valid_for_physics_claim=False, original_action_unchanged=True, github_action=False, subagents_used=False,
        no_nonlinear_finite_trajectory_rerun=True, full_fixed_time_force_convergence_proven=False,
        internal_nonlinear_initial_window_force_bound_derived=True, useful_h0_certified=False,
        independently_reviewed_proof=False, time_integration_error_certified=False,
        bound='C(h+t+t^2), implying O(h) for0<=t<=tau_star*h with fixed tau_star; not fixed-time force convergence.',
        implementation_checks_not_physics_passes=True, original_failed_cases_preserved=True,
        protected_scan_scope='mtime since turn start2026-09-17T20:03:38Z; not a pre-turn full hash baseline')
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

    def inherit(status):
        for table in ['inputs', 'outputs']:
            for name, expected in status[table].items():
                path = (root/name).resolve()
                key = str(path.relative_to(root))
                if not path.is_file() or digest(path) != expected:
                    raise RuntimeError('Missing or changed immutable evidence: '+name)
                if key in report['inputs'] and report['inputs'][key] != expected:
                    raise RuntimeError('Conflicting immutable evidence: '+name)
                report['inputs'][key] = expected

    save()
    try:
        previous_path = intake/'annular-initial-corner-response-final-integrity.json'
        previous = json.loads(previous_path.read_text())
        check('previous_seal_complete', previous['state'] == 'complete' and all(row['passed'] for row in previous['checks']))
        inherit(previous)
        own(previous_path)
        statuses, counts = {}, {}
        for name, label, count in [('projection', 'annular-shrinking-window-force-attempt02', 332),
                ('generator', 'annular-material-generator-bound-attempt01', 565)]:
            path = intake/label/'status.json'
            status = json.loads(path.read_text())
            check(name+'_complete', status['state'] == 'complete' and len(status['checks']) == count
                and len(status['cases']) == 14 and all(row['passed'] for row in status['checks']))
            check(name+'_claim_scope', not status['full_GR_limit_proven'] and not status['valid_for_physics_claim']
                and not status['complete_parent_source_action_derived'] and status['original_action_unchanged']
                and not status['full_fixed_time_force_convergence_proven'] and not status['useful_h0_certified'])
            check(name+'_no_forward_data_or_changed_force_gate', not status['finite_future_trajectories_read']
                and status['no_nonlinear_finite_trajectory_rerun'] and status['old_peak_force_gates_unchanged']
                and status['source_field_momentum_retained'])
            inherit(status)
            own(path)
            statuses[name], counts[name] = status, count
        failed_path = intake/'annular-shrinking-window-force-attempt01/status.json'
        failed = json.loads(failed_path.read_text())
        check('symbolic_domain_checker_failure_retained', failed['state'] == 'failed'
            and [row['name'] for row in failed['checks'] if not row['passed']] == ['exact_P2_inverse_eigenvalues'])
        inherit(failed)
        own(failed_path)
        projection, generator = statuses['projection'], statuses['generator']
        check('same_polynomial_and_phase_family_after_fix', projection['exact_local_generalized_eigenvalues'] == [0, 12, 60]
            and projection['supersedes_symbolic_domain_comparison_failure'] == failed_path.parent.name
            and set(projection['exact_source_phase_cycle']) == {'1/5', '2/5', '3/5', '4/5'})
        expected = {(branch, count) for branch in ['reference', 'MTS'] for count in [33, 65, 129, 257, 513, 1025, 2049]}
        check('both_full_phase_grid_sweeps_retained', all({(row['branch'], row['base_count']) for row in status['cases']} == expected
            for status in [projection, generator]))
        check('canonical_source_identity_qualified', max(point['projection_identity_error']
            for row in projection['cases'] for point in row['probes']) < 2e-12)
        check('exact_projection_majorants_unchanged', generator['exact_projection_majorants']['nodal_bound'] == 10
            and generator['exact_projection_majorants']['function_bound'] == 12.5
            and generator['exact_projection_majorants']['relative_density_variation_maximum'] == '1/50')
        check('Gram_not_discarded', not projection['Gram_removed'] and generator['all_Gram_rows_retained']
            and all(row['max_Gram_factor_l1_over_h_squared'] > 0 for row in generator['cases'] if row['branch'] == 'MTS'))
        check('samples_not_uniform_proof_substitute', projection['numeric_checks_not_uniform_bound']
            and generator['uniform_bound_is_analytic_not_inferred_from_samples'])
        check('all_old_peak_failures_and_failure_count_preserved', previous['inherited_failed_attempts_preserved'] == 28
            and previous['inherited_peak_force_failures_preserved'] == 4
            and all(not row['original_peak_force_gate_pass'] for row in previous['comparison_results']))
        note = root/'DERIVATION-20260917-nonlinear-initial-force-refinement-bound.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json))`', content)
        check('all_cited_local_paths_exist', bool(cited) and all((root/name).is_file() for name in cited), cited)
        check('note_completed_with_scope_and_negative_results', 'PENDING' not in content
            and 'C [h+t+t^2]' in content and 'Total897 successful current implementation checks' in content
            and '29 retained failed attempts' in content and 'It is not full GR' in content
            and 'cannot be tiled' in content and 'It does not identify' not in content)
        own(note)
        names = ['qualify_annular_shrinking_window_force_20260917.py', 'qualify_annular_shrinking_window_force_v2_20260917.py',
            'qualify_annular_material_generator_bound_20260917.py', 'seal_annular_nonlinear_initial_force_20260917.py']
        for name in names:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('all_new_scripts_compile', True, names)
        check('script_bytecode_cache_absent', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        started = datetime(2026, 9, 17, 20, 3, 38, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*')
            if path.is_file() and path.stat().st_mtime >= started]
        check('protected_workbench_mtime_changed_count_zero', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        check('resume_and_executed_source_preserved', True)
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(),
            current_suite_checks=counts, total_successful_current_checks=sum(counts.values()),
            distinct_files_rehashed=len(cache), inherited_failed_attempts_preserved=29,
            prior_failed_attempts=28, new_failed_attempts_preserved=[str(failed_path.relative_to(root))],
            inherited_peak_force_failures_preserved=4,
            proof_status='Internal analytic proof for shrinking initial windows of the exact prescribed-flat semidiscrete family, not independent proof review or full GR.',
            projection_results=projection['cases'], generator_results=generator['cases'])
        save()
        print(json.dumps(dict(state='complete', checks=len(report['checks']), current_checks=sum(counts.values()),
            rehashed_files=len(cache), protected_changed=len(changed), failed_attempts_preserved=29)), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
