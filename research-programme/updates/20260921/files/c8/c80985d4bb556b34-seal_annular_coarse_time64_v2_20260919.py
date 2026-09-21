from derive_annular_source_gravity_20260914 import EvidenceRun
from datetime import datetime, timezone
from pathlib import Path
import csv
import hashlib
import json
import math
import re
import traceback


def main():
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    destination = intake/'annular-coarse-time64-final-integrity-v2.json'
    snapshot = intake/'annular-coarse-time64-resume-snapshot-v2.md'
    executed = intake/'annular-coarse-time64-executed-sealer-v2.py'
    suffixes = ['force', 'response-summary', 'points', 'responses', 'controls', 'sampling', 'richardson']
    tables = [intake/('annular-coarse-time64-v2-'+suffix+'.csv') for suffix in suffixes]
    if any(path.exists() for path in [destination, snapshot, executed]+tables):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, github_action=False, subagents_used=False,
        valid_for_physics_claim=False, full_GR_limit_proven=False, full_live_P2_force_convergence_proven=False,
        new_short_live_evolution=True, fine_trajectories_unchanged=True,
        certified_continuous_time_bound=False, continuum_mismatch_resolved=False,
        protected_scan_scope='mtime since2026-09-19T20:31:36Z; not a pre-turn whole-tree hash baseline')
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

    def own(path, category='inputs'):
        report[category][str(path.resolve().relative_to(root))] = digest(path)

    def save():
        destination.write_text(json.dumps(report, indent=2, allow_nan=False)+'\n', encoding='utf-8')

    def check(name, passed, detail=None):
        report['checks'].append(dict(name=name, passed=bool(passed), detail=detail))
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def inherit(path):
        data = json.loads(path.read_text())
        for category in ['inputs', 'outputs']:
            for name, expected in data[category].items():
                source = (root/name).resolve()
                key = str(source.relative_to(root))
                if not source.is_file() or digest(source) != expected:
                    raise RuntimeError('Changed sealed source: '+name)
                if key in report['inputs'] and report['inputs'][key] != expected:
                    raise RuntimeError('Conflicting source: '+name)
                report['inputs'][key] = expected
        own(path)
        return data

    save()
    try:
        previous = inherit(intake/'annular-action-response-refinement-final-integrity.json')
        check('prior7857files_and44failures_intact', previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks'])
            and previous['distinct_files_rehashed'] == 7857 and previous['total_failed_attempts_preserved'] == 44)
        names = ['annular-coarse-time64-reference-attempt01', 'annular-coarse-time64-MTS-attempt01',
            'annular-coarse-time64-response-attempt01']
        statuses = []
        for name in names:
            status = inherit(intake/name/'status.json')
            statuses.append(status)
            check(name+'_complete_private_nonclaim', status['state'] == 'complete'
                and all(row['passed'] for row in status['checks'])
                and not status['valid_for_physics_claim'] and not status['full_GR_limit_proven']
                and not status['full_live_P2_force_convergence_proven']
                and not status['github_action'] and not status['subagents_used'])
        failed_seal_path = intake/'annular-coarse-time64-final-integrity.json'
        failed_seal = inherit(failed_seal_path)
        own(root/'scripts/seal_annular_coarse_time64_20260919.py')
        failed_checks = [row for row in failed_seal['checks'] if not row['passed']]
        check('first_seal_literal_wording_failure_preserved', failed_seal['state'] == 'failed'
            and len(failed_checks) == 1 and failed_checks[0]['name'] == 'report_complete_with_limits'
            and len(failed_seal['outputs']) == 7)
        failures = [dict(folder=failed_seal_path.name, error=failed_seal['error'],
            kind='integrity_report_literal_wording_not_calculation_failure')]
        for path in sorted(intake.glob('annular-coarse-time64-*/status.json')):
            if path.parent.name not in names:
                failed = inherit(path)
                check(path.parent.name+'_failed_attempt_preserved', failed['state'] == 'failed')
                failures.append(dict(folder=path.parent.name, error=failed['error']))
        for status in statuses[:2]:
            branch = status['branch']
            check(branch+'_only_coarse_time_changed', status['steps'] == 64 and status['accepted'] == 64
                and status['base_count'] == 257 and status['source_cap'] == 2e-5
                and status['duration'] == 4e-5 and status['fine_trajectory_fixed']
                and status['initial_preparation_unchanged'] and status['original_action_and_source_unchanged']
                and status['same_exponential_midpoint_integrator'] and status['all_modes_retained'])
            check(branch+'_new_evolution_honestly_marked', status['new_short_live_evolution'] and not status['no_new_evolution'])
            case = status['cases'][0]
            check(branch+'_force_denominators_explicit', math.isclose(case['new_coarse_fine_relative_force_difference'],
                abs(case['fine_force']-case['new_coarse_force'])/abs(case['fine_force']), rel_tol=1e-14)
                and math.isclose(case['fixed_fine_continuum_relative_force_error'],
                    abs(case['fine_force']-case['continuum_force'])/abs(case['continuum_force']), rel_tol=1e-14))
            lower = abs(case['old_coarse_fine_force_difference'])-case['absolute_coarse_time_force_change']
            check(branch+'_finite_force_change_triangle_bound', abs(case['new_coarse_fine_force_difference'])+1e-22 >= lower)
            check(branch+'_impulse_and_long_window_not_retested', status['impulse_not_recomputed']
                and status['previous_long_window_not_retested'])
        response = statuses[2]
        check('response_is_postprocessing_with_fixed_actions', response['no_new_evolution_in_this_script']
            and response['uses_new_coarse_evolution'] and response['identical_frozen_action']
            and response['fine_trajectory_fixed'] and response['all_action_rows_retained']
            and response['no_modal_diagnostic'] and not response['certified_continuous_time_bound'])
        sources = [str((intake/name/'status.json').relative_to(root)) for name in names]

        def sourced(rows, index, units):
            return [dict(**row, source_path=sources[index], units=units) for row in rows]

        rows_by_table = [sourced(statuses[0]['cases'],0,'normalized_force_and_canonical_state')
            +sourced(statuses[1]['cases'],1,'normalized_force_and_canonical_state'),
            sourced(response['cases'],2,'normalized_action_response_norm'),
            sourced(response['points'],2,'normalized_saved_time_canonical_acceleration'),
            sourced(response['responses'],2,'normalized_saved_time_action_response'),
            sourced(response['controls'],2,'normalized_exponential_arithmetic'),
            sourced(response['sampling'],2,'normalized_forcing_sampling_difference'),
            sourced(response['richardson'],2,'normalized_forcing_extrapolation_diagnostic')]
        check('table_row_counts', [len(rows) for rows in rows_by_table] == [2,6,66,118,18,18,34])
        for path, rows in zip(tables, rows_by_table):
            with path.open('w', encoding='utf-8', newline='') as stream:
                writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            with path.open(encoding='utf-8', newline='') as stream:
                parsed = list(csv.DictReader(stream))
            check(path.name+'_sourced_nonclaim_rows_parse', len(parsed) == len(rows) and all(None not in row
                and row['valid_for_claim'] == 'False' and (root/row['source_path']).is_file() for row in parsed))
            check(path.name+'_finite_numbers', all(math.isfinite(value) for row in rows for value in row.values()
                if isinstance(value,(float,int))))
            own(path,'outputs')
        for branch in ['reference','MTS']:
            points = [row for row in response['points'] if row['branch'] == branch]
            check(branch+'_33matched_points_and_nested_probes', len(points) == 33
                and len({row['reverse_time'] for row in points}) == 33
                and sum(row['probe_halving_performed'] for row in points) == 3
                and all(row['acceleration_control_error'] <= row['numerical_tolerance']
                    and row['probe_halving_error'] <= row['numerical_tolerance'] for row in points))
            check(branch+'_initial_state_difference_zero', points[-1]['interpolated_coarse_temporal_norm'] == 0.)
            rows = [row for row in response['responses'] if row['branch'] == branch]
            check(branch+'_all_three_forcing_grids', all(sum(row['grid_points'] == count for row in rows) == count
                for count in [9,17,33]))
            check(branch+'_old_result_reproduced_and_fine_cancels', all(row['old_response_reproduction_error'] < 1e-11
                and row['fixed_fine_cancellation_error'] < 1e-11 for row in rows))
            controls = [row for row in response['controls'] if row['branch'] == branch]
            check(branch+'_all_exponential_controls', len(controls) == 9 and all(row['halfstep_error'] <= row['numerical_tolerance']
                and row['rescaling_error'] <= row['numerical_tolerance'] for row in controls))
            summaries = [row for row in response['cases'] if row['branch'] == branch]
            check(branch+'_residuals_recorded_without_demanding_improvement', len(summaries) == 3 and all(
                row['initial_error'] == 0 and row['final_new_error'] >= 0 and row['max_new_error'] >= row['final_new_error']
                for row in summaries))
        note = root/'DERIVATION-20260919-coarse-time64-isolation.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv))`', content)
        check('all_cited_local_paths_exist', bool(cited) and all((root/name).is_file() for name in cited), cited)
        check('report_complete_with_limits', 'RESULTS_PENDING' not in content and all(phrase.lower() in content.lower()
            for phrase in ['does not establish the full GR limit','12.5718%','13.58%','not independent physical validations',
                'not a pre-turn whole-tree hash baseline','original action','Next target']))
        own(note)
        for name in ['run_annular_coarse_time64_20260919.py', 'derive_annular_coarse_time64_response_20260919.py',
                'seal_annular_coarse_time64_20260919.py', 'seal_annular_coarse_time64_v2_20260919.py']:
            path = root/'scripts'/name
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('sources_compile_without_bytecode', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026,9,19,20,31,36,tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*')
            if path.is_file() and path.stat().st_mtime >= start]
        check('protected_mtime_changed_count_zero', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot,'outputs')
        own(executed,'outputs')
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(),
            implementation_checks=sum(len(status['checks']) for status in statuses),
            total_failed_attempts_preserved=44+len(failures), new_failures=failures,
            distinct_files_rehashed=len(cache), table_rows=[len(rows) for rows in rows_by_table],
            original_long_window_retested=False, impulse_recomputed=False,
            next_target='See the signed residual/force evidence and Next target in the owned report; no automatic new run.')
        save()
        print(json.dumps(dict(state='complete',implementation_checks=report['implementation_checks'],
            integrity_checks=len(report['checks']),files_rehashed=len(cache),
            failed_attempts_preserved=report['total_failed_attempts_preserved'],table_rows=report['table_rows'])),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
