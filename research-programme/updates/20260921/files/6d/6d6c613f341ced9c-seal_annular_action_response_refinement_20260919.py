from derive_annular_source_gravity_20260914 import EvidenceRun
from datetime import datetime,timezone
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
    destination = intake/'annular-action-response-refinement-final-integrity.json'
    snapshot = intake/'annular-action-response-refinement-resume-snapshot.md'
    executed = intake/'annular-action-response-refinement-executed-sealer.py'
    suffixes = ['algebra','response-summary','response-points','response-controls','response-sampling',
        'time-summary','time-points','time-responses','time-comparisons','level-summary','level-points']
    tables = [intake/('annular-action-response-'+suffix+'.csv') for suffix in suffixes]
    if any(path.exists() for path in [destination,snapshot,executed]+tables):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running',checks=[],inputs={},outputs={},github_action=False,subagents_used=False,
        valid_for_physics_claim=False,full_GR_limit_proven=False,full_live_P2_force_convergence_proven=False,
        uniform_evolving_refinement_rate_proven=False,full_nonlinear_stability_proven=False,
        no_new_live_trajectory=True,original_action_operator_used=True,
        continuum_mismatch_resolved=False,certified_live_continuous_time_bound=False,
        temporal_refinement_not_continuum_convergence=True,
        protected_scan_scope='mtime since2026-09-19T18:48:22Z; not a pre-turn whole-tree hash baseline')
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

    def own(path,category='inputs'):
        report[category][str(path.resolve().relative_to(root))] = digest(path)

    def save():
        destination.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf-8')

    def check(name,passed,detail=None):
        report['checks'].append(dict(name=name,passed=bool(passed),detail=detail))
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def inherit(path):
        data = json.loads(path.read_text())
        for category in ['inputs','outputs']:
            for name,expected in data[category].items():
                source = (root/name).resolve()
                key = str(source.relative_to(root))
                if not source.is_file() or digest(source) != expected:
                    raise RuntimeError('Changed sealed source: '+name)
                if key in report['inputs'] and report['inputs'][key] != expected:
                    raise RuntimeError('Conflicting sealed source: '+name)
                report['inputs'][key] = expected
        own(path)
        return data

    save()
    try:
        previous = inherit(intake/'annular-moving-duhamel-final-integrity.json')
        check('previous7774file_seal_and44failures_preserved',previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks']) and previous['total_failed_attempts_preserved'] == 44
            and previous['distinct_files_rehashed'] == 7774)
        names = ['annular-action-exponential-algebra-attempt01','annular-action-exponential-response-attempt01',
            'annular-action-response-time-halving-attempt01','annular-temporal-level-contributions-attempt01']
        statuses = []
        for name in names:
            status = inherit(intake/name/'status.json')
            statuses.append(status)
            check(name+'_complete_private_nonclaim',status['state'] == 'complete'
                and all(row['passed'] for row in status['checks']) and not status['valid_for_physics_claim']
                and not status['full_GR_limit_proven'] and not status['full_live_P2_force_convergence_proven']
                and not status['github_action'] and not status['subagents_used'] and status['no_new_evolution'])
        failures = []
        for prefix in ['annular-action-exponential-','annular-action-response-time-halving-','annular-temporal-level-contributions-']:
            for path in sorted(intake.glob(prefix+'*/status.json')):
                if path.parent.name not in names:
                    failed = inherit(path)
                    check(path.parent.name+'_failed_attempt_preserved',failed['state'] == 'failed')
                    failures.append(dict(folder=path.parent.name,error=failed['error']))
        check('no_new_failed_execution',not failures)
        algebra,response,temporal,levels = statuses
        sources = [str((intake/name/'status.json').relative_to(root)) for name in names]

        def sourced(rows,index,units):
            return [dict(**row,source_path=sources[index],units=units) for row in rows]

        rows_by_table = [sourced(algebra['cases'],0,'synthetic_fixture'),
            sourced(response['cases'],1,'normalized_action_energy_and_response'),
            sourced(response['points'],1,'normalized_saved_time_action_energy_and_response'),
            sourced(response['controls'],1,'normalized_action_response_error'),
            sourced(response['sampling'],1,'normalized_saved_time_action_response_difference'),
            sourced(temporal['cases'],2,'normalized_temporal_refinement_response'),
            sourced(temporal['points'],2,'normalized_saved_time_canonical_acceleration'),
            sourced(temporal['responses'],2,'normalized_saved_time_action_response_error'),
            sourced(temporal['comparisons'],2,'normalized_saved_time_Richardson_diagnostic'),
            sourced(levels['cases'],3,'normalized_action_temporal_difference'),
            sourced(levels['points'],3,'normalized_saved_time_signed_temporal_energy')]
        check('expected_table_rows',[len(rows) for rows in rows_by_table] == [3,2,118,12,18,2,68,52,18,2,34])
        for path,rows in zip(tables,rows_by_table):
            with path.open('w',encoding='utf-8',newline='') as stream:
                writer = csv.DictWriter(stream,fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            with path.open(encoding='utf-8',newline='') as stream:
                parsed = list(csv.DictReader(stream))
            check(path.name+'_sourced_nonclaim_rows_parse',len(parsed) == len(rows) and all(None not in row
                and row['valid_for_claim'] == 'False' and (root/row['source_path']).is_file() for row in parsed))
            check(path.name+'_numbers_finite',all(math.isfinite(value) for row in rows for value in row.values()
                if isinstance(value,(float,int))))
            own(path,'outputs')
        check('direct_operator_not_modal_or_new_dynamics',response['all_action_rows_retained']
            and response['no_modal_eigenvectors_or_frequencies_used'] and response['original_action_and_source_unchanged']
            and response['no_new_live_evolution'] and not response['certified_continuous_time_bound'])
        check('temporal_comparison_same_action_existing_runs',temporal['identical_frozen_action_for_both_temporal_resolutions']
            and temporal['existing_trajectories_only'] and temporal['richardson_is_diagnostic_not_certificate']
            and not temporal['certified_continuous_time_bound'])
        for branch in ['reference','MTS']:
            check(branch+'_response_all_three_forcing_grids',all(len([row for row in response['points']
                if row['branch'] == branch and row['grid_points'] == count]) == count for count in [9,17,33]))
            controls = [row for row in response['controls'] if row['branch'] == branch]
            check(branch+'_all_halfstep_rescaling_controls',len(controls) == 6 and all(
                row['halfstep_error'] <= row['numerical_tolerance'] and row['coordinate_scaling_error'] <= row['numerical_tolerance'] for row in controls))
            summary = next(row for row in response['cases'] if row['branch'] == branch)
            check(branch+'_zero_initial_and_conserved_homogeneous_column',summary['initial_action_response_error'] == 0.
                and summary['max_frozen_energy_relative_drift'] < 2e-9)
            check(branch+'_no_remaining_error_hidden',summary['final_action_response_error'] > 0.
                and summary['max_action_response_error'] >= summary['final_action_response_error'])
            points = [row for row in temporal['points'] if row['branch'] == branch]
            check(branch+'_lower_temporal_points_and_controls',len(points) == 34
                and len({row['reverse_time'] for row in points}) == 17
                and all(row['higher_trajectory_steps'] == 2*row['lower_trajectory_steps']
                    and row['acceleration_error'] <= row['numerical_tolerance'] for row in points))
            check(branch+'_matched_temporal_forcing_grids',all(len([row for row in temporal['responses']
                if row['branch'] == branch and row['forcing_nodes'] == count]) == count for count in [9,17]))
            comparisons = [row for row in temporal['comparisons'] if row['branch'] == branch]
            check(branch+'_vector_scaling_reported_not_assumed',len(comparisons) == 9
                and all(row['richardson_is_estimate_not_certificate'] and row['factor4_vector_gap'] >= 0. for row in comparisons))
            level_points = [row for row in levels['points'] if row['branch'] == branch]
            check(branch+'_signed_level_telescope_retained',len(level_points) == 17 and all(abs(row['combined_temporal_norm']**2
                -row['fine_temporal_norm']**2-row['coarse_temporal_norm']**2-row['signed_cross_energy_twice'])
                < 1e-10*max(row['combined_temporal_norm']**2,row['fine_temporal_norm']**2,row['coarse_temporal_norm']**2,1e-30)+1e-25
                for row in level_points))
            summary = next(row for row in levels['cases'] if row['branch'] == branch)
            check(branch+'_shared_initial_temporal_difference_zero',summary['shared_initial_temporal_norm'] == 0.)
        note = root/'DERIVATION-20260919-action-consistent-response-and-time-refinement.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv))`',content)
        check('all_cited_local_paths_exist',bool(cited) and all((root/name).is_file() for name in cited),cited)
        check('claim_limits_and_numerical_controls_explicit',all(phrase.lower() in content.lower() for phrase in [
            'does not establish the full GR limit','12.5718%','13.58%','not a pre-turn whole-tree hash baseline',
            'not independent physical validations','not a rigorous error certificate','piecewise-linear',
            'original action']))
        check('report_complete','RESULTS_PENDING' not in content)
        own(note)
        for name in ['annular_action_exponential_20260919.py','validate_annular_action_exponential_20260919.py',
                'derive_annular_action_exponential_response_20260919.py','derive_annular_action_response_time_halving_20260919.py',
                'diagnose_annular_temporal_level_contributions_20260919.py',
                'seal_annular_action_response_refinement_20260919.py']:
            path = root/'scripts'/name
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('sources_compile_without_bytecode',not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026,9,19,18,48,22,tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*')
            if path.is_file() and path.stat().st_mtime >= start]
        check('protected_mtime_changed_count_zero',not changed,changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot,'outputs')
        own(executed,'outputs')
        count = sum(len(status['checks']) for status in statuses)
        check('successful_implementation_count',count == 747)
        report.update(state='complete',completed_at=datetime.now(timezone.utc).isoformat(),implementation_checks=count,
            total_failed_attempts_preserved=44+len(failures),new_failures=failures,distinct_files_rehashed=len(cache),
            table_rows=[len(rows) for rows in rows_by_table],full_interval_retested=False,
            next_target='coarse257/cap2e-5 time64 on both branches, keeping fine128 MTS and fine64 reference fixed; compare signed response and force diagnostics before further refinement')
        save()
        print(json.dumps(dict(state='complete',implementation_checks=count,integrity_checks=len(report['checks']),
            files_rehashed=len(cache),failed_attempts_preserved=44+len(failures),table_rows=report['table_rows'])),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
