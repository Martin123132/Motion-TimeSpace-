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
    destination = intake/'annular-moving-Gram-regularity-final-integrity.json'
    snapshot = intake/'annular-moving-Gram-regularity-resume-snapshot.md'
    executed = intake/'annular-moving-Gram-regularity-executed-sealer.py'
    suffixes = ['algebra','profile','norms','bilinear','secants','path-budgets','rates','atom-rates',
        'adjoint-channel-atoms','weighted-norms','weighted-intervals','weighted-work']
    tables = [intake/('annular-moving-Gram-'+suffix+'.csv') for suffix in suffixes]
    if any(path.exists() for path in [destination,snapshot,executed]+tables):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running',checks=[],inputs={},outputs={},github_action=False,subagents_used=False,
        valid_for_physics_claim=False,full_GR_limit_proven=False,full_live_P2_force_convergence_proven=False,
        uniform_evolving_refinement_rate_proven=False,full_nonlinear_stability_proven=False,
        no_new_trajectory_evolution=True,original_source_Dirichlet_condition_unchanged=True,
        continuum_mismatch_resolved=False,actual_continuous_time_bound=False,
        protected_scan_scope='mtime since2026-09-19T15:35:14Z; not a pre-turn whole-tree hash baseline')
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
        previous = inherit(intake/'annular-weak-Gram-consistency-final-integrity.json')
        check('previous7510file_seal_and43failures_preserved',previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks']) and previous['total_failed_attempts_preserved'] == 43
            and previous['distinct_files_rehashed'] == 7510)
        names = ['annular-moving-Gram-algebra-attempt01','annular-moving-Gram-profile-attempt01',
            'annular-moving-Gram-rate-attempt01','annular-weighted-row-transport-attempt01']
        statuses = []
        for name in names:
            status = inherit(intake/name/'status.json')
            statuses.append(status)
            check(name+'_complete_private_nonclaim',status['state'] == 'complete'
                and all(row['passed'] for row in status['checks']) and not status['valid_for_physics_claim']
                and not status['full_GR_limit_proven'] and not status['full_live_P2_force_convergence_proven']
                and not status['github_action'] and not status['subagents_used'] and status['no_new_evolution'])
        failures = []
        for prefix in ['annular-moving-Gram-algebra-','annular-moving-Gram-profile-',
                'annular-moving-Gram-rate-','annular-weighted-row-transport-']:
            for path in sorted(intake.glob(prefix+'*/status.json')):
                if path.parent.name not in names:
                    failed = inherit(path)
                    check(path.parent.name+'_failed_attempt_preserved',failed['state'] == 'failed')
                    failures.append(dict(folder=path.parent.name,error=failed['error']))
        check('no_new_failed_execution',not failures)
        sources = [str((intake/name/'status.json').relative_to(root)) for name in names]

        def sourced(rows,index,units):
            return [dict(**row,source_path=sources[index],units=units) for row in rows]

        profile = [{key:value for key,value in row.items() if key != 'norms'} for row in statuses[1]['cases']]
        norms = [dict(branch=case['branch'],time=case['time'],**row) for case in statuses[1]['cases'] for row in case['norms']]
        rows_by_table = [sourced(statuses[0]['cases'],0,'synthetic_fixture'),
            sourced(profile,1,'normalized_annular_work'),sourced(norms,1,'normalized_annular_regularity'),
            sourced(statuses[1]['bilinear_rows'],1,'normalized_annular_work'),
            sourced(statuses[1]['secants'],1,'normalized_annular_time_rate'),
            sourced(statuses[1]['path_budgets'],1,'normalized_annular_derivative_jump'),
            sourced(statuses[2]['cases'],2,'normalized_annular_time_rate'),
            sourced(statuses[2]['atom_rates'],2,'normalized_annular_derivative_jump_rate'),
            sourced(statuses[2]['adjoint_channel_atoms'],2,'normalized_annular_derivative_jump_rate'),
            sourced(statuses[3]['cases'],3,'normalized_annular_Gram_norm'),
            sourced(statuses[3]['intervals'],3,'normalized_annular_Gram_norm_increment'),
            sourced(statuses[3]['work_bounds'],3,'normalized_annular_work')]
        expected = [1,18,72,288,16,16,8,64,48,8,64,2]
        check('expected_table_row_counts',[len(rows) for rows in rows_by_table] == expected)
        for path,rows in zip(tables,rows_by_table):
            with path.open('w',encoding='utf-8',newline='') as stream:
                writer = csv.DictWriter(stream,fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            with path.open(encoding='utf-8',newline='') as stream:
                parsed = list(csv.DictReader(stream))
            check(path.name+'_sourced_nonclaim_rows_parse',len(parsed) == len(rows) and all(None not in row
                and row['valid_for_claim'] == 'False' and (root/row['source_path']).is_file() for row in parsed))
            check(path.name+'_numbers_finite',all(math.isfinite(value) for row in rows for value in row.values() if isinstance(value,(float,int))))
            own(path,'outputs')
        check('nine_matched_times_per_branch',all(len([row for row in profile if row['branch'] == branch]) == 9
            and {row['coarse_step'] for row in profile if row['branch'] == branch} == set(range(0,33,4)) for branch in ['reference','MTS']))
        check('actual_profiles_not_uniform_certificate',statuses[1]['sampled_path_not_continuous_solution_certificate']
            and not statuses[1]['uniform_evolving_refinement_rate_proven'] and statuses[1]['signed_gradient_curvature_cross_terms_retained'])
        for row in profile:
            channels = [item['work'] for item in statuses[1]['bilinear_rows'] if item['branch'] == row['branch'] and item['time'] == row['time']]
            check(row['branch']+'_'+str(row['time'])+'_signed_work_and_all16channels',len(channels) == 16
                and abs(sum(channels)-row['weak_work']) < 1e-20+1e-10*sum(abs(value) for value in channels)
                and abs(row['weak_work']) <= row['row_absolute_bound']+1e-23
                and abs(row['weak_work']) <= row['atom_work_bound']+1e-23)
        for row in statuses[2]['cases']:
            check(row['branch']+'_'+str(row['tangent_step'])+'_transport_and_work_checks',
                row['adjoint_error'] <= row['adjoint_tolerance'] and row['adjoint_exact_secant_error'] <= row['adjoint_exact_secant_tolerance']
                and row['work_rate_error'] <= row['work_rate_tolerance']
                and abs(row['work_rate']-row['weight_transport']-row['trial_transport']-row['test_transport']) < 1e-16)
        check('derivative_estimates_not_certificates',statuses[2]['rates_are_finite_difference_estimates']
            and statuses[2]['both_mass_transport_terms_retained'] and statuses[2]['inverse_residual_acceleration_retained']
            and statuses[2]['finite_probes_not_time_uniform_certificate'])
        check('weighted_path_not_continuous_bound',not statuses[3]['actual_continuous_time_bound']
            and not statuses[3]['uniform_evolving_refinement_rate_proven']
            and all(row['sampled_absolute_work_max'] <= row['coupled_weighted_path_bound']+1e-23 for row in statuses[3]['work_bounds']))
        note = root/'DERIVATION-20260919-moving-Gram-regularity-and-adjoint-transport.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv))`',content)
        check('all_cited_local_paths_exist',bool(cited) and all((root/name).is_file() for name in cited),cited)
        check('claim_limits_explicit',all(phrase in content for phrase in [
            'does not establish the full GR limit','12.5718%','13.58%',
            'not a pre-turn whole-tree hash baseline','not independent physical validations',
            'not interval-arithmetic error certificates','not control the unobserved evolution']))
        check('report_no_pending_results', 'will be recorded after' not in content)
        own(note)
        for name in ['annular_moving_Gram_budget_20260919.py','validate_annular_moving_Gram_budget_20260919.py',
                'derive_annular_moving_Gram_profile_20260919.py','derive_annular_moving_Gram_rate_20260919.py',
                'derive_annular_weighted_row_transport_20260919.py','seal_annular_moving_Gram_regularity_20260919.py']:
            path = root/'scripts'/name
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('sources_compile_without_bytecode',not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026,9,19,15,35,14,tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= start]
        check('protected_mtime_changed_count_zero',not changed,changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot,'outputs')
        own(executed,'outputs')
        implementation = sum(len(status['checks']) for status in statuses)
        report.update(state='complete',completed_at=datetime.now(timezone.utc).isoformat(),implementation_checks=implementation,
            total_failed_attempts_preserved=43+len(failures),new_failures=failures,distinct_files_rehashed=len(cache),
            table_rows=[len(rows) for rows in rows_by_table],full_interval_retested=False,
            next_target='derive an action-based uniform weighted-row forcing bound for B_H eta_dot and B_h d_dot; retain geometry, source traces and signed cancellations')
        save()
        print(json.dumps(dict(state='complete',implementation_checks=implementation,integrity_checks=len(report['checks']),
            files_rehashed=len(cache),failed_attempts_preserved=43+len(failures),table_rows=report['table_rows'])),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
