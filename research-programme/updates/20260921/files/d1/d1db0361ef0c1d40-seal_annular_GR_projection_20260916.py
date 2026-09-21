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
    destination = intake/'annular-GR-projection-final-integrity.json'
    snapshot = intake/'annular-GR-projection-resume-snapshot.md'
    executed = intake/'annular-GR-projection-executed-sealer.py'
    if any(path.exists() for path in [destination,snapshot,executed]):
        raise FileExistsError('Immutable evidence already exists.')
    report = dict(state='running',checks=[],inputs={},outputs={},full_GR_limit_proven=False,
        valid_for_physics_claim=False,continuum_limit_proven=False,uniform_time_bound=False,
        github_action=False,subagents_used=False,
        protected_scan_scope='mtime since previous seal2026-09-16T20:11:48Z; not a pre-turn full hash baseline')
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

    def own(path,table='inputs'):
        report[table][str(path.resolve().relative_to(root))] = digest(path)

    def save():
        destination.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf-8')

    def check(name,passed,detail=None):
        report['checks'].append(dict(name=name,passed=bool(passed),detail=detail))
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def inherit(status):
        for table in ['inputs','outputs']:
            for name,expected in status[table].items():
                path = (root/name).resolve()
                key = str(path.relative_to(root))
                if not path.is_file() or digest(path)!=expected:
                    raise RuntimeError('Missing or changed immutable file: '+name)
                if key in report['inputs'] and report['inputs'][key]!=expected:
                    raise RuntimeError('Conflicting immutable file: '+name)
                report['inputs'][key] = expected

    save()
    try:
        previous_path = intake/'annular-joint-refinement-final-integrity.json'
        previous = json.loads(previous_path.read_text())
        check('previous_seal_complete',previous['state']=='complete' and all(row['passed'] for row in previous['checks']))
        inherit(previous)
        own(previous_path)
        statuses,counts = {},{}
        for name,label,count,cases in [('qualification','annular-GR-projection-qualification-attempt01',64,9),
            ('projection','annular-GR-projection-residual-attempt02',77,18),
            ('analysis','annular-GR-projection-analysis-attempt01',72,18),
            ('remainder','annular-rational-force-remainder-attempt01',36,6)]:
            path = intake/label/'status.json'
            status = json.loads(path.read_text())
            json.dumps(status,allow_nan=False)
            check(name+'_complete',status['state']=='complete' and len(status['checks'])==count
                and len(status['cases'])==cases and all(row['passed'] for row in status['checks']))
            check(name+'_broad_claims_false',not status['full_GR_limit_proven'] and not status['valid_for_physics_claim']
                and not status['complete_parent_source_action_derived'])
            inherit(status)
            own(path)
            statuses[name],counts[name] = status,count
        check('GR_only_constructive_inputs',not statuses['projection']['finite_future_trajectories_read']
            and not statuses['projection']['force_fit'] and not statuses['projection']['force_correction']
            and statuses['projection']['projection_kinematic_defect_retained'])
        check('retrospective_not_predictive',statuses['analysis']['retrospective_attribution_not_prediction']
            and statuses['analysis']['trajectory_errors_not_independently_predicted']
            and not statuses['analysis']['force_correction'])
        check('analytic_remainder_scope_explicit',statuses['remainder']['exact_fixed_geometry_remainder_derived']
            and statuses['remainder']['source_position_and_speed_held_fixed_for_bound']
            and statuses['remainder']['source_geometry_response_separately_retained']
            and not statuses['remainder']['uniform_trajectory_bound'])
        expected = {(branch,count,degree) for branch in ['reference','MTS'] for count in [257,513,1025] for degree in [384,512,768]}
        check('all_branches_grids_reference_degrees',{(row['branch'],row['count'],row['degree']) for row in statuses['analysis']['cases']}==expected)
        check('force_gate_flags_not_upgraded',all(row['total_force_gate_pass']==(row['max_total_force_error']<2e-7)
            and not row['total_force_gate_pass'] for row in statuses['analysis']['cases']))
        failed_path = intake/'annular-GR-projection-residual-attempt01/status.json'
        failed = json.loads(failed_path.read_text())
        check('reporting_failure_preserved',failed['state']=='failed' and 'TypeError' in failed['error'] and 'list' in failed['error'])
        inherit(failed)
        own(failed_path)
        tight_path = intake/'annular-joint-tight1025-attempt01/status.json'
        tight = json.loads(tight_path.read_text())
        check('finest_worker_at_safe_end',tight['state'] in ['complete','paused_safe_checkpoint'])
        inherit(tight)
        own(tight_path)
        resumed_path = intake/'annular-joint-tight1025-resumed-attempt01/status.json'
        if resumed_path.is_file():
            resumed = json.loads(resumed_path.read_text())
            check('resumed_worker_at_safe_end',resumed['state'] in ['complete','paused_safe_checkpoint']
                and resumed['resumed_from']=='annular-joint-tight1025-attempt01'
                and tight['state']=='paused_safe_checkpoint')
            inherit(resumed)
            own(resumed_path)
            report['first_pause_preserved'] = True
            tight = resumed
        report['full_duration_finest_time_control_complete'] = tight['state']=='complete'
        if tight['state']=='complete':
            check('paired_tight_original_runs',len(tight['checks'])==(10 if 'resumed_from' in tight else 9) and len(tight['cases'])==2
                and all(row['passed'] for row in tight['checks']) and tight['original_action_unchanged']
                and not tight['force_correction'] and tight['final_time']==.4)
            counts['finest_tight'] = len(tight['checks'])
            path = intake/'annular-joint-validation-attempt03/status.json'
            validation = json.loads(path.read_text())
            check('all_full_duration_time_controls_validated',validation['state']=='complete'
                and len(validation['checks'])==57 and len(validation['time_controls'])==6
                and all(row['passed'] for row in validation['checks']))
            check('both_finest_controls_present',len([row for row in validation['time_controls'] if row['count']==1025])==2)
            check('no_full_trajectory_pass',not validation['all_tested_cases_pass']
                and all(not row['sampled_pass_all_references'] for row in validation['cases']))
            inherit(validation)
            own(path)
            report['time_controls'] = validation['time_controls']
            counts['time_validation'] = len(validation['checks'])
        else:
            report['unfinished_finest_control_progress'] = tight.get('progress')
            check('unfinished_control_not_claimed_complete',not report['full_duration_finest_time_control_complete'])
        note = root/'DERIVATION-20260916-GR-projection-and-coupled-consistency-force.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json))`',content)
        check('cited_note_paths_exist',all((root/name).is_file() for name in cited),cited)
        check('finished_note_scoped','PENDING' not in content and 'not the full GR limit' in content
            and 'retrospective' in content and 'kinematic' in content)
        own(note)
        names = ['run_annular_joint_refinement_20260916_v2.py','annular_GR_projection_20260916.py',
            'qualify_annular_GR_projection_20260916.py','derive_annular_GR_projection_residual_20260916.py',
            'derive_annular_GR_projection_residual_20260916_v2.py','analyze_annular_GR_projection_residual_20260916.py',
            'derive_annular_rational_force_remainder_20260916.py','resume_annular_joint_refinement_20260916.py',
            'seal_annular_GR_projection_20260916.py']
        for name in names:
            path = root/'scripts'/name
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('new_sources_compile',True,names)
        check('script_bytecode_cache_absent',not(root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        started = datetime(2026,9,16,20,11,48,tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=started]
        check('protected_workbench_mtime_changed_count_zero',not changed,changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot,'outputs')
        own(executed,'outputs')
        check('resume_and_executed_source_preserved',True)
        report.update(state='complete',completed_at=datetime.now(timezone.utc).isoformat(),current_suite_checks=counts,
            total_successful_current_checks=sum(counts.values()),distinct_files_rehashed=len(cache),
            inherited_failed_attempts_preserved=previous['inherited_failed_attempts_preserved']+1,
            new_failed_attempts_preserved=[str(failed_path.relative_to(root))],
            results=statuses['analysis']['cases'],projection_results=statuses['projection']['cases'],
            exact_remainder_results=statuses['remainder']['cases'],
            original_failed_cases_preserved=True,implementation_checks_not_physics_passes=True)
        save()
        print(json.dumps(dict(state='complete',checks=len(report['checks']),current_checks=sum(counts.values()),
            rehashed_files=len(cache),protected_changed=len(changed),failed_attempts_preserved=report['inherited_failed_attempts_preserved'],
            paired_finest_time_control_complete=report['full_duration_finest_time_control_complete'])),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__=='__main__':
    main()
