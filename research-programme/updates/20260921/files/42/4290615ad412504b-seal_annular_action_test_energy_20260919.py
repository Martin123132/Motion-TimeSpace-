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
    destination = intake/'annular-action-test-energy-final-integrity.json'
    snapshot = intake/'annular-action-test-energy-resume-snapshot.md'
    executed = intake/'annular-action-test-energy-executed-sealer.py'
    suffixes = ['algebra','stability','amplification','hotspots','energy','acceleration-controls','residual-channels','common-mesh']
    tables = [intake/('annular-action-test-'+suffix+'.csv') for suffix in suffixes]
    if any(path.exists() for path in [destination,snapshot,executed]+tables):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running',checks=[],inputs={},outputs={},github_action=False,subagents_used=False,
        valid_for_physics_claim=False,full_GR_limit_proven=False,full_live_P2_force_convergence_proven=False,
        uniform_evolving_refinement_rate_proven=False,full_nonlinear_stability_proven=False,
        no_new_trajectory_evolution=True,original_source_Dirichlet_condition_unchanged=True,
        continuum_mismatch_resolved=False,actual_continuous_time_bound=False,
        protected_scan_scope='mtime since2026-09-19T16:30:14Z; not a pre-turn whole-tree hash baseline')
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
        previous = inherit(intake/'annular-moving-Gram-regularity-final-integrity.json')
        check('previous7570file_seal_and43failures_preserved',previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks']) and previous['total_failed_attempts_preserved'] == 43
            and previous['distinct_files_rehashed'] == 7570)
        names = ['annular-action-test-energy-algebra-attempt01','annular-action-adjoint-stability-attempt01',
            'annular-action-adjoint-amplification-attempt01','annular-differentiated-action-energy-attempt01',
            'annular-common-mesh-adjoint-control-attempt01']
        statuses = []
        for name in names:
            status = inherit(intake/name/'status.json')
            statuses.append(status)
            check(name+'_complete_private_nonclaim',status['state'] == 'complete' and all(row['passed'] for row in status['checks'])
                and not status['valid_for_physics_claim'] and not status['full_GR_limit_proven']
                and not status['full_live_P2_force_convergence_proven'] and not status['github_action']
                and not status['subagents_used'] and status['no_new_evolution'])
        failures = []
        for prefix in ['annular-action-test-energy-algebra-','annular-action-adjoint-stability-',
                'annular-action-adjoint-amplification-','annular-differentiated-action-energy-',
                'annular-common-mesh-adjoint-control-']:
            for path in sorted(intake.glob(prefix+'*/status.json')):
                if path.parent.name not in names:
                    failed = inherit(path)
                    check(path.parent.name+'_failed_attempt_preserved',failed['state'] == 'failed')
                    failures.append(dict(folder=path.parent.name,error=failed['error']))
        check('no_new_failed_execution',not failures)
        sources = [str((intake/name/'status.json').relative_to(root)) for name in names]

        def sourced(rows,index,units):
            return [dict(**row,source_path=sources[index],units=units) for row in rows]

        rows_by_table = [sourced(statuses[0]['cases'],0,'synthetic_fixture'),
            sourced(statuses[1]['cases'],1,'normalized_annular_energy_and_operator_norm'),
            sourced(statuses[2]['cases'],2,'normalized_annular_stiffness'),
            sourced(statuses[2]['elements'],2,'normalized_annular_element_stiffness'),
            sourced(statuses[3]['cases'],3,'normalized_annular_energy_and_rate'),
            sourced(statuses[3]['acceleration_controls'],3,'normalized_annular_acceleration'),
            sourced(statuses[3]['residual_channels'],3,'normalized_annular_residual_rate'),
            sourced(statuses[4]['cases'],4,'normalized_annular_energy_and_work')]
        check('expected_table_rows',[len(rows) for rows in rows_by_table] == [4,4,4,20,4,24,28,2])
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
        check('stiffness_tests_both_branches_initial_final',{(row['branch'],row['time']) for row in statuses[1]['cases']}
            == {('reference',0.),('reference',4e-5),('MTS',0.),('MTS',4e-5)})
        for row in statuses[1]['cases']:
            check(row['branch']+'_'+str(row['time'])+'_operator_and_actual_work_bounds',
                row['stiffness_sharp_squared'] <= row['stiffness_squared_upper']+1e-8
                and row['Gram_sharp_squared'] <= row['Gram_squared_upper']+1e-8
                and abs(row['weak_work']) <= row['action_stiffness_work_bound']+1e-22)
        check('both_nested_probe_sizes_on_both_branches',{(row['branch'],row['outer_step']) for row in statuses[3]['cases']}
            == {('reference',1e-7),('reference',5e-8),('MTS',1e-7),('MTS',5e-8)})
        for row in statuses[3]['cases']:
            check(row['branch']+'_'+str(row['outer_step'])+'_differentiated_energy_and_conditional_bound',
                row['rate_error'] <= row['numerical_tolerance'] and row['exact_secant_error'] <= row['exact_secant_tolerance']
                and abs(row['predicted_rate']) <= row['energy_rate_upper_bound']+1e-16
                and abs(row['weak_work']) <= row['E1_weak_work_bound']+1e-22)
        check('nested_flow_and_energy_limit_explicit',statuses[3]['nested_actual_canonical_directions']
            and statuses[3]['inverse_residual_rates_retained'] and statuses[3]['energy_does_not_control_Gram_acceleration']
            and statuses[3]['rates_are_finite_difference_estimates'] and not statuses[3]['full_nonlinear_stability_proven'])
        for row in statuses[4]['cases']:
            check(row['branch']+'_common_mesh_defects_not_dropped',abs(row['worst_original_energy']-row['worst_common_projection_energy']
                -row['worst_defect_energy']-row['worst_signed_cross_energy']) < 1e-8*row['worst_original_energy']
                and abs(row['actual_original_coarse_work']-row['actual_common_coarse_work']-row['actual_retained_defect_coarse_work']) < 1e-19)
        check('counterfactual_not_substituted_dynamics',statuses[4]['counterfactual_diagnostic_not_replacement_action']
            and statuses[4]['original_transfer_and_force_results_unchanged']
            and statuses[4]['time_dependent_projection_not_inserted_in_original_energy_equations'])
        note = root/'DERIVATION-20260919-action-test-energy-and-transfer-stability.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv))`',content)
        check('all_cited_local_paths_exist',bool(cited) and all((root/name).is_file() for name in cited),cited)
        check('claim_limits_explicit',all(phrase in content for phrase in ['does not establish the full GR limit',
            '12.5718%','13.58%','not a pre-turn whole-tree hash baseline','not independent physical validations',
            'not interval-arithmetic error certificates','does not explain away']))
        check('report_complete','will be filled' not in content)
        own(note)
        for name in ['annular_action_test_energy_20260919.py','validate_annular_action_test_energy_20260919.py',
                'derive_annular_action_adjoint_stability_20260919.py','diagnose_annular_action_adjoint_amplification_20260919.py',
                'derive_annular_differentiated_action_energy_20260919.py','derive_annular_common_mesh_adjoint_control_20260919.py',
                'seal_annular_action_test_energy_20260919.py']:
            path = root/'scripts'/name
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('sources_compile_without_bytecode',not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026,9,19,16,30,14,tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= start]
        check('protected_mtime_changed_count_zero',not changed,changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot,'outputs')
        own(executed,'outputs')
        count = sum(len(status['checks']) for status in statuses)
        report.update(state='complete',completed_at=datetime.now(timezone.utc).isoformat(),implementation_checks=count,
            total_failed_attempts_preserved=43+len(failures),new_failures=failures,distinct_files_rehashed=len(cache),
            table_rows=[len(rows) for rows in rows_by_table],full_interval_retested=False,
            next_target='close or bound the differentiated residual forcing using the retained action channels; separate the small actual nodal alias work from remaining Gram mismatch')
        save()
        print(json.dumps(dict(state='complete',implementation_checks=count,integrity_checks=len(report['checks']),
            files_rehashed=len(cache),failed_attempts_preserved=43+len(failures),table_rows=report['table_rows'])),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
