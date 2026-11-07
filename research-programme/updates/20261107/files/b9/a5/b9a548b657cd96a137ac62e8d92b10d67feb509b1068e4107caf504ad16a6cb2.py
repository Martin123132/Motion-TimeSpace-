from derive_annular_source_gravity_20260914 import EvidenceRun
from validate_annular_MTS_matched_current_20260923 import independent_derivative
from datetime import datetime, timezone
from time import perf_counter
import contextlib
import csv
import hashlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-MTS-primary-matched-current-validation-attempt02',__file__)
    started = perf_counter()
    try:
        intake = evidence.output.parent
        paths = [intake/'annular-MTS-primary-matched-current-attempt01/status.json',
                 intake/'annular-MTS-primary-matched-current-validation-attempt01/status.json']
        main_run, prior = [json.loads(path.read_text()) for path in paths]
        for path in paths:
            evidence.own(path)
        evidence.check('main_complete',main_run['state']=='complete' and main_run['branch']=='MTS-primary')
        evidence.check('known_export_failure_only',prior['state']=='failed' and prior['error']=="FileNotFoundError(2, 'No such file or directory')"
            and 'paired-MTS-primary-radial.csv' in prior['traceback'] and 'line 322' in prior['traceback'])
        evidence.check('all_upstream_checks_passed',len(prior['checks'])==2123 and all(row['passed'] for row in prior['checks']))
        evidence.check('numeric_validation_reached_final_gate',prior['checks'][-1]['name']=='no_scientific_flags_skipped'
            and len(prior['scientific_replays'])==154 and len(prior['cases'])==12)
        reference_path = intake/'annular-reference-matched-current-validation-attempt01/status.json'
        reference = json.loads(reference_path.read_text())
        evidence.own(reference_path)
        evidence.check('reference_source_seal_complete',reference['state']=='complete')
        for relative,digest in reference['inputs'].items():
            path = evidence.root/relative
            if path.parent==evidence.root/'scripts':
                evidence.check('unchanged_shared_reference_source:'+relative,hashlib.sha256(path.read_bytes()).hexdigest()==digest)
                evidence.own(path)
        digests = {}
        for authority in [main_run,prior]:
            for table in ['inputs','outputs']:
                for relative,digest in authority[table].items():
                    if relative in digests:
                        evidence.check('matching_authority_hash:'+relative,digests[relative]==digest)
                    digests[relative] = digest
        for relative,digest in digests.items():
            path = evidence.root/relative
            evidence.check('sealed:'+relative,path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==digest)
            evidence.own(path)

        def read(relative):
            evidence.check('registered:'+relative,relative in digests)
            with np.load(evidence.root/relative,allow_pickle=False) as archive:
                return {key:archive[key].copy() for key in archive.files}

        def checked_csv(relative,count):
            evidence.check('registered_csv:'+relative,relative in digests)
            with (evidence.root/relative).open(newline='',encoding='utf-8') as stream:
                rows = list(csv.DictReader(stream))
            evidence.check('well_formed:'+relative,len(rows)==count and all(None not in row and None not in row.values() for row in rows))
            return rows

        def export(filename,rows):
            path = evidence.output/filename
            with path.open('w',newline='',encoding='utf-8') as stream:
                writer = csv.DictWriter(stream,fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            evidence.own(path,'outputs')

        expected = {(route,index,sign) for route in ['inherited','resampled'] for index in range(3) for sign in [-1,1]}
        evidence.check('complete_main_cases',len(main_run['cases'])==12 and
            {(row['route'],row['index'],row['sign']) for row in main_run['cases']}==expected)
        evidence.check('every_case_independently_validated',{row['case'] for row in prior['cases']}=={row['case'] for row in main_run['cases']})
        for check in main_run['scientific_checks']:
            matches = [row for row in prior['scientific_replays'] if row['case']==check['case'] and row['quantity']==check['quantity']]
            evidence.check('science_replay:'+check['case']+':'+check['quantity'],len(matches)==1)
            row = matches[0]
            evidence.check('science_unchanged:'+check['case']+':'+check['quantity'],
                row['tolerance']==check['tolerance'] and row['passed']==check['passed']
                and row['passed']==bool(np.isfinite(row['replayed_error']) and row['replayed_error']<=row['tolerance'])
                and abs(row['replayed_error']-check['error'])<=2e-14)
        negative = [row for row in main_run['scientific_checks'] if not row['passed']]
        evidence.check('inherited_negative_answers_preserved',len(negative)==2 and
            {(row['case'],row['quantity']) for row in negative}=={('inherited-resolution0','radial_zero_question'),('inherited-resolution1','radial_zero_question')})
        steps = np.array(main_run['outer_steps'])
        independently_saved,component_names,face_table = {},{},[]
        for route in ['inherited','resampled']:
            summary = next(row for row in main_run['summaries'] if row['route']==route)
            owned_path = str((paths[1].parent/(route+'-independent-rates.npz')).relative_to(evidence.root))
            validated = read(owned_path)
            independently_saved[route] = validated
            main_rates = read(summary['component_path'])
            component_names[route] = list(main_rates['component_names'])
            for key in ['channel_rate','transport_rate','components']:
                evidence.check(route+':independent_'+key,np.max(abs(validated[key]-main_rates[key]))<=2e-14)
            raw = {}
            for index in range(3):
                for sign in [-1,1]:
                    case = next(row for row in main_run['cases'] if (row['route'],row['index'],row['sign'])==(route,index,sign))
                    checked = next(row for row in prior['cases'] if row['case']==case['case'])
                    trace = read(checked['allface_path'])
                    evidence.check(case['case']+':all1093faces',checked['face_count']==1093 and trace['weighted_faces'].shape==(3,1093)
                        and np.array_equal(trace['faces'],validated['faces']))
                    evidence.check(case['case']+':endpoint_sum',np.max(abs(trace['weighted_faces'].sum(axis=1)+trace['pin']-trace['trace']))<=2e-16)
                    raw[index,sign] = trace
            face_values = np.array([[raw[index,sign]['weighted_faces'] for sign in [-1,1]] for index in range(3)])
            pin_values = np.array([[raw[index,sign]['pin'] for sign in [-1,1]] for index in range(3)])
            face_rate,pin_rate = independent_derivative(face_values,steps),independent_derivative(pin_values,steps)
            evidence.check(route+':face_rate_replay',np.max(abs(face_rate-validated['face_rate']))<=2e-16)
            evidence.check(route+':pin_rate_replay',np.max(abs(pin_rate-validated['pin_rate']))<=2e-16)
            evidence.check(route+':trace_rate_replay',np.max(abs(face_rate.sum(axis=2)+pin_rate-validated['transport_rate'][:,1]))<=2e-11)
            for face,position in enumerate(validated['faces']):
                for test in range(3):
                    face_table.append(dict(route=route,reference_face=position,test=test,trace_lift_rate=face_rate[-1,test,face],
                        paired_change=abs(face_rate[1,test,face]-face_rate[0,test,face])))
        comparisons = []
        for test in range(3):
            inherited,resampled = [independently_saved[route]['radial'] for route in ['inherited','resampled']]
            before,after = inherited[1,-1,test],resampled[1,-1,test]
            comparisons.append(dict(test=test,inherited=before,resampled=after,change=after-before,absolute_ratio=abs(after/before),
                inherited_outer_change=abs(inherited[1,1,test]-inherited[1,0,test]),resampled_outer_change=abs(resampled[1,1,test]-resampled[1,0,test]),
                inherited_quadrature_change=abs(inherited[1,-1,test]-inherited[0,-1,test]),resampled_quadrature_change=abs(resampled[1,-1,test]-resampled[0,-1,test])))
        legacy_path = str((paths[0].parent/'paired-transport_weak_assembly_defect-radial.csv').relative_to(evidence.root))
        nominal_path = paths[0].parent/'paired-MTS-primary-radial.csv'
        evidence.check('original_filename_bug_preserved',not nominal_path.exists() and legacy_path in main_run['outputs'])
        rows = checked_csv(legacy_path,3)
        for row,target in zip(rows,comparisons):
            for key,value in target.items():
                tolerance = 2e-5 if key=='absolute_ratio' else 2e-14
                evidence.check('paired_csv:'+row['test']+':'+key,abs(float(row[key])-value)<=tolerance)
        rows = checked_csv(str((paths[0].parent/'complete-component-rates.csv').relative_to(evidence.root)),120)
        for row in rows:
            component = component_names[row['route']].index(row['component'])
            test = int(row['test'])
            components = independently_saved[row['route']]['components']
            evidence.check('component_csv:'+row['route']+':'+row['component']+':'+row['test'],
                abs(float(row['value'])-components[-1,component,test])<=2e-14
                and abs(float(row['paired_change'])-abs(components[1,component,test]-components[0,component,test]))<=2e-14)
        export('paired-MTS-primary-radial.csv',comparisons)
        export('allface-trace-rates.csv',face_table)
        for filename,count in [('paired-MTS-primary-radial.csv',3),('allface-trace-rates.csv',6558)]:
            with (evidence.output/filename).open(newline='',encoding='utf-8') as stream:
                rows = list(csv.DictReader(stream))
            evidence.check('new_export:'+filename,len(rows)==count and all(None not in row and None not in row.values() for row in rows))
        source = evidence.root/'scripts/run_annular_MTS_matched_current_20260923.py'
        corrected = evidence.root/'scripts/run_annular_MTS_matched_current_v2_20260923.py'
        expected_source = source.read_text().replace('for component, name in enumerate(component_names):',
            'for component, component_name in enumerate(component_names):').replace(
            'component_table.append(dict(route=route,component=name,test=test,value=components[-1,component,test],',
            'component_table.append(dict(route=route,component=component_name,test=test,value=components[-1,component,test],')
        evidence.check('future_runner_fix_only_renames_shadowing_loop_variable',corrected.read_text()==expected_source)
        for path in [corrected,evidence.root/'scripts/validate_annular_MTS_matched_current_20260923.py',evidence.root/'scripts/finalize_annular_MTS_primary_matched_current_20260923.py']:
            compile(path.read_text(),str(path),'exec')
            evidence.own(path)
        threshold = datetime(2026,9,23,1,10,55,tzinfo=timezone.utc).timestamp()
        changed = [str(path) for path in (evidence.root.parent/'formalization-workbench').rglob('*') if path.is_file() and path.stat().st_mtime>=threshold]
        evidence.check('protected_workbench_unchanged',not changed,changed)
        evidence.check('no_scripts_bytecode_cache',not (evidence.root/'scripts/__pycache__').exists())
        for relative,digest in evidence.report['inputs'].copy().items():
            evidence.check('final_hash:'+relative,hashlib.sha256((evidence.root/relative).read_bytes()).hexdigest()==digest)
        evidence.report.update(seconds=perf_counter()-started,branch='MTS-primary',comparison=comparisons,cases=prior['cases'],
            upstream_validation_checks=len(prior['checks']),upstream_numeric_validation_status=str(paths[1].relative_to(evidence.root)),
            scientific_replays=prior['scientific_replays'],science_passed=main_run['science_passed'],science_total=main_run['science_total'],
            scientific_false_flags=negative,protected_workbench_changed_count=len(changed),github_action=False,subagents_used=False,
            fresh_nonlinear_solves=0,recovery='CSV filename only; component loop shadowed branch name. Original attempt preserved, complete numeric validations hash-reused.',
            validation_scope='Finalizes all completed 2123 upstream numerical checks with scientific-flag, allface derivative, CSV and hash replays; no tolerance changes')
        with (evidence.output/'completion.txt').open('w',encoding='utf-8') as stream,contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt','outputs')
        evidence.save()
        print(json.dumps(dict(state='complete',seconds=evidence.report['seconds'],checks=len(evidence.report['checks']),
            upstream_checks=len(prior['checks']),comparison=comparisons)),flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
