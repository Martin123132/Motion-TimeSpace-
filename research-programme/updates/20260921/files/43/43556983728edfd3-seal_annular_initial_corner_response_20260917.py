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
    destination = intake/'annular-initial-corner-response-final-integrity.json'
    snapshot = intake/'annular-initial-corner-response-resume-snapshot.md'
    executed = intake/'annular-initial-corner-response-executed-sealer.py'
    if any(path.exists() for path in [destination, snapshot, executed]):
        raise FileExistsError('Immutable evidence already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, full_GR_limit_proven=False,
        valid_for_physics_claim=False, original_action_unchanged=True, github_action=False, subagents_used=False,
        no_nonlinear_finite_trajectory_rerun=True, instantaneous_force_convergence_proven=False,
        uniform_nonlinear_remainder_proven=False, benchmark_time_units_not_SI=True,
        implementation_checks_not_physics_passes=True, original_failed_cases_preserved=True,
        protected_scan_scope='mtime since turn start2026-09-17T18:46:37Z; not a pre-turn full hash baseline')
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
        previous_path = intake/'annular-material-force-bridge-final-integrity.json'
        previous = json.loads(previous_path.read_text())
        check('previous_seal_complete', previous['state'] == 'complete' and all(row['passed'] for row in previous['checks']))
        inherit(previous)
        own(previous_path)
        statuses, counts = {}, {}
        for name, label, count, cases in [('prediction', 'annular-frozen-initial-layer-attempt03', 24, 4),
                ('comparison', 'annular-frozen-layer-comparison-attempt01', 41, 4),
                ('inner', 'annular-corner-inner-solution-attempt01', 16, 4)]:
            path = intake/label/'status.json'
            status = json.loads(path.read_text())
            check(name+'_complete', status['state'] == 'complete' and len(status['checks']) == count
                and len(status['cases']) == cases and all(row['passed'] for row in status['checks']))
            check(name+'_claim_scope', not status['full_GR_limit_proven'] and not status['valid_for_physics_claim']
                and not status['complete_parent_source_action_derived'] and status['original_action_unchanged']
                and not status['uniform_nonlinear_remainder_proven'])
            inherit(status)
            own(path)
            statuses[name], counts[name] = status, count
        failed_paths = []
        for label, expected_failure in [('annular-frozen-initial-layer-attempt01', 'reference513_frozen_force_time_control'),
                ('annular-frozen-initial-layer-attempt02', 'MTS1025_frozen_force_time_control')]:
            path = intake/label/'status.json'
            failed = json.loads(path.read_text())
            check(label+'_control_failure_retained', failed['state'] == 'failed'
                and [row['name'] for row in failed['checks'] if not row['passed']] == [expected_failure])
            inherit(failed)
            own(path)
            failed_paths.append(str(path.relative_to(root)))
        prediction, comparison, inner = [statuses[name] for name in ['prediction', 'comparison', 'inner']]
        check('time_controls_tightened_not_gate_relaxed', prediction['unchanged_force_time_control_threshold'] == 2e-10
            and len(prediction['supersedes_failed_time_control']) == 2
            and all(max(row['force_time_control'], row['evaluated_force_time_control']) < 2e-10 for row in prediction['cases']))
        check('all_predictions_frozen_before_this_comparison', not prediction['finite_future_trajectories_read']
            and comparison['predictions_frozen_at'] == prediction['predictions_frozen_at']
            and comparison['predictions_frozen_at'] < comparison['comparison_started_at'])
        check('no_fit_or_deleted_coupling', not prediction['force_fit'] and not prediction['force_correction']
            and prediction['source_field_inertia_retained'] and prediction['all_source_Gram_terms_retained']
            and prediction['no_nonlinear_forward_trajectory_rerun'])
        expected_keys = {(branch, count) for branch in ['reference', 'MTS'] for count in [513, 1025]}
        check('same_four_cases_both_branches', all({(row['branch'], row['base_count']) for row in status['cases']} == expected_keys
            for status in [prediction, comparison]))
        negative = [(row['branch'], row['base_count']) for row in comparison['cases']
            if not row['linear_diagnostic_explains_to_frozen_fraction']]
        check('negative_linear_prediction_diagnostic_retained', negative == [('reference', 1025)])
        coarse_mts = next(row for row in comparison['cases'] if row['branch'] == 'MTS' and row['base_count'] == 513)
        check('evaluated_not_claimed_always_better', coarse_mts['maximum_frozen_evaluated_prediction_remainder']
            > coarse_mts['maximum_frozen_linear_prediction_remainder'])
        old_rows = {(row['branch'], row['base_count']): row for row in previous['bridge_results']}
        check('original_peak_values_and_all_failures_preserved', all(not row['original_peak_force_gate_pass']
            and abs(row['original_full_horizon_sampled_peak_force_error']
                -old_rows[(row['branch'], row['base_count'])]['original_sampled_peak_force_error']) < 1e-16
            for row in comparison['cases']))
        check('inherited_failure_count_preserved', previous['inherited_failed_attempts_preserved'] == 26
            and previous['inherited_peak_force_failures_preserved'] == 4)
        check('inner_solution_not_finite_matching_proof', inner['exact_forced_convected_halfline_solution']
            and not inner['matching_to_evolved_finite_action_proven'] and inner['initial_layer_only_not_later_envelope'])
        note = root/'DERIVATION-20260917-initial-corner-response-and-frozen-action-prediction.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json))`', content)
        check('all_cited_local_paths_exist', bool(cited) and all((root/name).is_file() for name in cited), cited)
        check('note_scope_and_failures_complete', 'PENDING' not in content and '81 successful current implementation checks' in content
            and 'retained failed-attempt total to28' in content and 'full GR limit remains open' in content
            and 'not a blind prospective experiment' in content and 'It does not remove any original force discrepancy.' in content)
        own(note)
        names = ['annular_frozen_initial_layer_20260917.py', 'run_annular_frozen_initial_layer_20260917.py',
            'run_annular_frozen_initial_layer_v2_20260917.py', 'run_annular_frozen_initial_layer_v3_20260917.py',
            'qualify_annular_frozen_layer_predictions_20260917.py', 'qualify_annular_corner_inner_solution_20260917.py',
            'seal_annular_initial_corner_response_20260917.py']
        for name in names:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('all_new_scripts_compile', True, names)
        check('script_bytecode_cache_absent', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        started = datetime(2026, 9, 17, 18, 46, 37, tzinfo=timezone.utc).timestamp()
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
            distinct_files_rehashed=len(cache), inherited_failed_attempts_preserved=28,
            prior_failed_attempts=26, new_failed_attempts_preserved=failed_paths,
            inherited_peak_force_failures_preserved=4, prediction_results=prediction['cases'],
            comparison_results=comparison['cases'], inner_results=inner['cases'])
        save()
        print(json.dumps(dict(state='complete', checks=len(report['checks']), current_checks=sum(counts.values()),
            rehashed_files=len(cache), protected_changed=len(changed), failed_attempts_preserved=28)), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
