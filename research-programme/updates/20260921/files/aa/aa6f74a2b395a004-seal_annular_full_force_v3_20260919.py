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
    destination = intake/'annular-full-force-final-integrity-v3.json'
    snapshot = intake/'annular-full-force-resume-snapshot-v3.md'
    executed = intake/'annular-full-force-executed-sealer-v3.py'
    suffixes = ['algebra','states','schur','secants','duality-diagnostic','transport-summary',
        'transport-budgets','transport-controls','transport-duals','transport-sampling']
    tables = [intake/('annular-full-force-v3-'+suffix+'.csv') for suffix in suffixes]
    if any(path.exists() for path in [destination,snapshot,executed]+tables):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running',checks=[],inputs={},outputs={},github_action=False,subagents_used=False,
        no_new_evolution=True,valid_for_physics_claim=False,full_GR_limit_proven=False,
        full_live_P2_force_convergence_proven=False,certified_continuous_time_bound=False,
        strict_spatial_transport_qualification_pass=False,
        protected_scan_scope='mtime since2026-09-19T21:32:36Z; not a pre-turn whole-tree hash baseline')
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
                    raise RuntimeError('Conflicting source: '+name)
                report['inputs'][key] = expected
        own(path)
        return data

    save()
    try:
        previous = inherit(intake/'annular-coarse-time64-final-integrity-v2.json')
        check('previous8093file_seal_and45failures_preserved',previous['state'] == 'complete'
            and previous['distinct_files_rehashed'] == 8093 and previous['total_failed_attempts_preserved'] == 45
            and all(row['passed'] for row in previous['checks']))
        names = ['annular-full-force-algebra-attempt01','annular-full-force-endpoints-attempt01',
            'annular-full-force-duality-diagnostic-attempt01','annular-full-force-transport-attempt02']
        statuses = []
        for name in names:
            status = inherit(intake/name/'status.json')
            statuses.append(status)
            check(name+'_complete_scoped_implementation_nonclaim',status['state'] == 'complete'
                and all(row['passed'] for row in status['checks']) and not status['valid_for_physics_claim']
                and not status['full_GR_limit_proven'] and not status['full_live_P2_force_convergence_proven']
                and status['no_new_evolution'] and not status['github_action'] and not status['subagents_used'])
        failures = []
        for path in [intake/'annular-full-force-transport-attempt01/status.json']:
            if path.parent.name not in names:
                failed = inherit(path)
                check(path.parent.name+'_failed_execution_preserved',failed['state'] == 'failed')
                failures.append(dict(folder=path.parent.name,error=failed['error']))
        check('strict_transport_failure_retained',len(failures) == 1
            and failures[0]['folder'] == 'annular-full-force-transport-attempt01')
        failed_seal_path = intake/'annular-full-force-final-integrity.json'
        failed_seal = inherit(failed_seal_path)
        own(root/'scripts/seal_annular_full_force_20260919.py')
        check('seal_scope_collision_preserved',failed_seal['state'] == 'failed'
            and failed_seal['checks'][-1]['name'] == 'annular-full-force-linearization-attempt01_failed_execution_preserved')
        failures.append(dict(folder=failed_seal_path.name,error=failed_seal['error'],kind='seal_scope_collision_with_September16_complete_run'))
        count_failure_path = intake/'annular-full-force-final-integrity-v2.json'
        count_failure = inherit(count_failure_path)
        check('manual_count_failure_preserved',count_failure['state'] == 'failed'
            and count_failure['checks'][-1]['name'] == 'scoped_successful_check_count')
        failures.append(dict(folder=count_failure_path.name,error=count_failure['error'],kind='manual_count_omitted_source_hash_checks'))
        algebra,endpoints,diagnostic,transport = statuses
        check('failed_qualification_not_promoted_to_pass',transport['strict_dual_gate_required_for_claim']
            and not transport['original_strict_dual_gate_pass'] and not transport['certified_continuous_time_bound']
            and transport['measured_path_defect_not_certified_error_bound'])
        spatial = [row for row in transport['duals'] if row['comparison'].startswith('spatial')]
        temporal = [row for row in transport['duals'] if row['comparison'] == 'temporal32to64']
        check('all_four_spatial_strict_failures_visible',len(spatial) == 4 and all(not row['original_strict_gate_pass']
            and row['error'] > row['numerical_tolerance'] for row in spatial))
        check('two_same_grid_temporal_cancellations_visible',len(temporal) == 2
            and all(row['original_strict_gate_pass'] and row['error'] == 0 for row in temporal))
        sources = [str((intake/name/'status.json').relative_to(root)) for name in names]

        def sourced(rows,index,units):
            return [dict(**row,source_path=sources[index],units=units) for row in rows]

        rows_by_table = [sourced(algebra['cases'],0,'synthetic_fixture'),
            sourced(endpoints['states'],1,'normalized_force_and_inertia'),
            sourced(endpoints['schur'],1,'normalized_signed_force'),
            sourced(endpoints['secants'],1,'normalized_signed_force'),
            sourced(diagnostic['cases'],2,'normalized_duality_arithmetic'),
            sourced(transport['cases'],3,'normalized_signed_force_budget'),
            sourced(transport['budgets'],3,'normalized_signed_force_budget'),
            sourced(transport['controls'],3,'normalized_action_arithmetic'),
            sourced(transport['duals'],3,'normalized_duality_arithmetic_with_failed_gate'),
            sourced(transport['sampling'],3,'normalized_forcing_sampling_change')]
        check('table_row_counts',[len(rows) for rows in rows_by_table] == [15,6,6,6,4,6,18,18,6,12])
        for path,rows in zip(tables,rows_by_table):
            fields = list(dict.fromkeys(key for row in rows for key in row))
            with path.open('w',encoding='utf-8',newline='') as stream:
                writer = csv.DictWriter(stream,fieldnames=fields)
                writer.writeheader()
                writer.writerows(rows)
            with path.open(encoding='utf-8',newline='') as stream:
                parsed = list(csv.DictReader(stream))
            check(path.name+'_sourced_nonclaim_rows_parse',len(parsed) == len(rows) and all(None not in row
                and row['valid_for_claim'] == 'False' and (root/row['source_path']).is_file() for row in parsed))
            check(path.name+'_finite_numbers',all(math.isfinite(value) for row in rows for value in row.values()
                if isinstance(value,(float,int))))
            own(path,'outputs')
        for branch in ['reference','MTS']:
            rows = [row for row in endpoints['secants'] if row['branch'] == branch]
            check(branch+'_three_full_force_secants',len(rows) == 3 and all(row['reconstruction_error'] <= row['numerical_tolerance']
                and row['covector_velocity_norm'] > 0 for row in rows))
            for comparison in ['spatial32','spatial64','temporal32to64']:
                rows = [row for row in transport['budgets'] if row['branch'] == branch and row['comparison'] == comparison]
                check(branch+'_'+comparison+'_three_grids_retain_path_defect',len(rows) == 3
                    and {row['grid_points'] for row in rows} == {9,17,33}
                    and all(row['measured_defect_is_not_certificate'] for row in rows))
            controls = [row for row in transport['controls'] if row['branch'] == branch]
            check(branch+'_exponential_arithmetic_controls',len(controls) == 9 and all(row['halfstep_error'] <= row['numerical_tolerance']
                and row['rescaling_error'] <= row['numerical_tolerance'] for row in controls))
        note = root/'DERIVATION-20260919-full-source-force-spatial-budget-v2.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv))`',content)
        check('cited_local_paths_exist',bool(cited) and all((root/name).is_file() for name in cited),cited)
        check('report_complete_and_failed_gate_explicit','RESULTS_PENDING' not in content
            and 'original_strict_dual_gate_pass=false' in content and 'does not establish the full GR limit' in content)
        own(note)
        for name in ['annular_full_schur_force_20260919.py','annular_position_action_response_20260919.py',
                'validate_annular_full_force_20260919.py','derive_annular_full_force_endpoints_20260919.py',
                'derive_annular_full_force_transport_20260919.py','diagnose_annular_full_force_duality_20260919.py',
                'derive_annular_full_force_transport_v2_20260919.py','seal_annular_full_force_20260919.py','seal_annular_full_force_v2_20260919.py','seal_annular_full_force_v3_20260919.py']:
            path = root/'scripts'/name
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('sources_compile_without_bytecode',not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026,9,19,21,32,36,tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*')
            if path.is_file() and path.stat().st_mtime >= start]
        check('protected_mtime_changed_count_zero',not changed,changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot,'outputs')
        own(executed,'outputs')
        count = sum(len(status['checks']) for status in statuses)
        report['implementation_check_breakdown'] = {name:len(status['checks']) for name,status in zip(names,statuses)}
        report.update(state='complete',completed_at=datetime.now(timezone.utc).isoformat(),implementation_checks=count,
            total_failed_attempts_preserved=45+len(failures),new_failures=failures,
            distinct_files_rehashed=len(cache),table_rows=[len(rows) for rows in rows_by_table],
            next_target='cancellation-preserving factored full-force/increment transport; retest unchanged strict dual gate before force-weighted spatial-commutator bounds')
        save()
        print(json.dumps(dict(state='complete',implementation_checks=count,integrity_checks=len(report['checks']),
            files_rehashed=len(cache),failed_attempts_preserved=report['total_failed_attempts_preserved'],
            strict_spatial_transport_qualification_pass=False,table_rows=report['table_rows'])),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
