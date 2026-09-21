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
    destination = intake/'annular-joint-refinement-final-integrity.json'
    snapshot = intake/'annular-joint-refinement-resume-snapshot.md'
    executed = intake/'annular-joint-refinement-executed-sealer.py'
    if any(path.exists() for path in [destination,snapshot,executed]):
        raise FileExistsError('Immutable evidence already exists.')
    report = dict(state='running',checks=[],inputs={},outputs={},full_GR_limit_proven=False,
        valid_for_physics_claim=False,continuum_limit_proven=False,uniform_time_bound=False,
        github_action=False,subagents_used=False,
        protected_scan_scope='mtime since2026-09-16T16:49:55Z; not a pre-turn full hash baseline')
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
        previous_path = intake/'annular-causal-correction-final-integrity.json'
        previous = json.loads(previous_path.read_text())
        check('previous_seal_complete',previous['state']=='complete' and all(row['passed'] for row in previous['checks']))
        inherit(previous)
        own(previous_path)
        statuses,counts = {},{}
        for name,label,count,cases in [('preassembly','annular-flat-preassembly-attempt01',96,24),
            ('references','annular-dense-GR-references-attempt01',12,3),
            ('rectangle','annular-joint-rectangle-attempt01',33,8),
            ('finer','annular-joint-finer1025-attempt01',9,2),
            ('tight','annular-joint-tight513-attempt01',9,2),
            ('tight257','annular-joint-tight257-attempt01',9,2),
            ('validation','annular-joint-validation-attempt02',54,10)]:
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
        check('full_original_action_cases',all(statuses[name]['original_action_unchanged']
            and statuses[name]['all_modes_and_Gram_rows_retained'] and not statuses[name]['force_correction']
            and not statuses[name]['reduced_solver'] and statuses[name]['final_time']==.4
            for name in ['rectangle','finer','tight','tight257']))
        expected = {(branch,count,splits) for branch in ['reference','MTS']
            for count,splits in [(257,4),(257,8),(513,4),(513,8),(1025,8)]}
        rows = statuses['validation']['cases']
        check('paired_rectangle_and_finer_case_present',{(row['branch'],row['count'],row['splits']) for row in rows}==expected)
        for row in rows:
            prefix = row['branch']+str(row['count'])+'-'+str(row['splits'])
            check(prefix+'_sampled_flags_recomputed',all(row['sampled81_flags'][degree]==(error<2e-7)
                for degree,error in row['maximum_force_errors'].items())
                and row['sampled_pass_all_references']==all(row['sampled81_flags'].values()))
            check(prefix+'_time_scope_explicit',row['full_duration_tighter_time_control_available']==(row['count'] in [257,513] and row['splits']==8)
                and row['time_controlled_all_sampled_gates_pass']==(row['full_duration_tighter_time_control_available']
                    and row['sampled_pass_all_references'] and row['field_gate768'] and all(row['source_clock_flags'].values())))
        check('all_three_reference_resolutions',{row['degree'] for row in statuses['references']['cases']}=={384,512,768})
        check('full_duration_tighter_control_only_on_qualified_grid',len(statuses['validation']['time_controls'])==4
            and all(row['count'] in [257,513] and row['splits']==8 and row['full_duration']==.4
                and row['force_change']<2e-8 and row['state_change']<2e-8 for row in statuses['validation']['time_controls']))
        check('exact_Gram_response_all_paired_grids',len(statuses['validation']['Gram_response'])==5
            and all(row['derived_force_identity_error']<2e-11 and row['not_a_force_correction']
                for row in statuses['validation']['Gram_response']))
        failed_path = intake/'annular-joint-validation-attempt01/status.json'
        failed = json.loads(failed_path.read_text())
        check('failed_legacy_state_check_preserved',failed['state']=='failed' and 'old_full_action_replay' in failed['error'])
        inherit(failed)
        own(failed_path)
        check('legacy_state_flags_not_relabelled',all(row['legacy_state_replay_pass']==(row['old_state_replay_error']<2e-8)
            for row in rows if 'old_state_replay_error' in row)
            and any(not row.get('legacy_state_replay_pass',True) for row in rows))
        note = root/'DERIVATION-20260916-original-action-joint-refinement.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json))`',content)
        check('cited_note_paths_exist',all((root/name).is_file() for name in cited),cited)
        check('finished_note_scoped','PENDING' not in content and 'not the full GR limit' in content
            and 'NOT exactly nested Gram matrices' in content)
        own(note)
        names = ['annular_flat_preassembled_flow_20260916.py','verify_annular_flat_preassembly_20260916.py',
            'run_annular_joint_refinement_20260916.py','run_annular_dense_GR_references_20260916.py',
            'validate_annular_joint_refinement_20260916.py','validate_annular_joint_refinement_20260916_v2.py',
            'seal_annular_joint_refinement_20260916.py']
        for name in names:
            path = root/'scripts'/name
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('new_sources_compile',True,names)
        check('script_bytecode_cache_absent',not(root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        started = datetime(2026,9,16,16,49,55,tzinfo=timezone.utc).timestamp()
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
            results=rows,Gram_response=statuses['validation']['Gram_response'],
            original_failed_cases_preserved=True,implementation_checks_not_physics_passes=True)
        save()
        print(json.dumps(dict(state='complete',checks=len(report['checks']),current_checks=sum(counts.values()),
            rehashed_files=len(cache),protected_changed=len(changed),failed_attempts_preserved=report['inherited_failed_attempts_preserved'])),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__=='__main__':
    main()
