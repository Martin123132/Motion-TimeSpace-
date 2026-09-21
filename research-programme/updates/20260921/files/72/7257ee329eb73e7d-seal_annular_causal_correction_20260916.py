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
    destination = intake/'annular-causal-correction-final-integrity.json'
    snapshot = intake/'annular-causal-correction-resume-snapshot.md'
    executed = intake/'annular-causal-correction-executed-sealer.py'
    if any(path.exists() for path in [destination,snapshot,executed]):
        raise FileExistsError('Evidence and executed sources are immutable.')
    report = dict(state='running',checks=[],inputs={},outputs={},full_GR_limit_proven=False,
        valid_for_physics_claim=False,uniform_nonlinear_remainder_bound=False,continuum_limit_proven=False,
        github_action=False,subagents_used=False,original_GR_failures_unchanged=True,
        protected_scan_scope='mtime since 2026-09-16T15:37:04Z, not a pre-turn full hash baseline')
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
        destination.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf-8')

    def check(name, passed, detail=None):
        report['checks'].append(dict(name=name,passed=bool(passed),detail=detail))
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def inherit(status):
        for table in ['inputs','outputs']:
            for name, expected in status[table].items():
                path = (root/name).resolve()
                key = str(path.relative_to(root))
                if not path.is_file() or digest(path)!=expected:
                    raise RuntimeError('Missing or changed immutable file: '+name)
                if key in report['inputs'] and report['inputs'][key]!=expected:
                    raise RuntimeError('Conflicting immutable digest: '+name)
                report['inputs'][key] = expected

    save()
    try:
        previous_path = intake/'annular-force-response-final-integrity.json'
        previous = json.loads(previous_path.read_text())
        check('previous_checkpoint_complete',previous['state']=='complete' and all(row['passed'] for row in previous['checks']))
        inherit(previous)
        own(previous_path)
        statuses,counts = {},{}
        for label,folder,count,cases in [('inputs','annular-causal-inputs-attempt01',5,2),
            ('standard','annular-causal-standard-attempt01',21,4),('tight','annular-causal-tight-attempt01',13,2),
            ('tight-step','annular-causal-tight-step-attempt01',13,2),
            ('validation','annular-causal-validation-attempt01',50,8)]:
            path = intake/folder/'status.json'
            status = json.loads(path.read_text())
            json.dumps(status,allow_nan=False)
            check(label+'_complete',status['state']=='complete' and len(status['checks'])==count
                and len(status['cases'])==cases and all(row['passed'] for row in status['checks']))
            check(label+'_broad_claims_false',not status['full_GR_limit_proven'] and not status['valid_for_physics_claim']
                and not status['complete_parent_source_action_derived'])
            inherit(status)
            own(path)
            statuses[label],counts[label] = status,count
        for label in ['standard','tight','tight-step']:
            status = statuses[label]
            check(label+'_predictor_npz_inputs_isolated',all(name.endswith('-predictor-inputs.npz')
                for name in status['inputs'] if name.endswith('.npz')) and not status['future_full_arrays_loaded'])
            manifest_path = intake/('annular-causal-'+label+'-attempt01')/'predictions-sealed.json'
            manifest = json.loads(manifest_path.read_text())
            check(label+'_predictions_precede_truth_open',datetime.fromisoformat(manifest['sealed_at'])
                <datetime.fromisoformat(statuses['validation']['truth_open_started_at']))
            check(label+'_reconstruction_retained',all(row['maximum_measured_reconstruction_residual']>=0.
                and row['nonlinear_remainder_is_measured_not_uniform_bound'] for row in status['cases']))
        config = statuses['inputs']['configuration']
        for row in statuses['validation']['cases']:
            prefix = row['branch']+'-'+row['precision']+'-'+str(row['stride'])
            check(prefix+'_force_flags_recomputed',row['force_control_met']==(row['corrected_force_error']<=config['force_control'])
                and row['corrected_force_budget_met']==(row['corrected_force_error']<=config['isolated_force_budget']))
            check(prefix+'_component_flags_recomputed',all(row['state_controls_met'][key]==(value<=config['state_controls'][key])
                for key,value in row['corrected_state_errors'].items()))
            check(prefix+'_nonlinear_scope',row['nonlinear_remainder_is_sampled_not_uniform_bound'])
        check('genuinely_finer_accepted_steps',all(row['evaluations']>next(old['evaluations']
            for old in statuses['tight']['cases'] if old['branch']==row['branch'])
            for row in statuses['tight-step']['cases']))
        check('both_branches_and_all_controls',len(statuses['validation']['controls'])==6
            and {(row['branch'],row['precision'],row['stride']) for row in statuses['validation']['cases']}
            =={(branch,precision,stride) for branch in ['reference','MTS']
                for precision,stride in [('standard',1),('standard',2),('tight',1),('tight-step',1)]})
        note = root/'DERIVATION-20260916-causal-coupled-defect-correction.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json))`',content)
        check('all_note_paths_exist',all((root/name).is_file() for name in cited),cited)
        check('finished_scoped_note','PENDING' not in content and 'not a full GR limit' in content
            and 'NOT blind discovery' in content and 'not a bound on rho' in content)
        own(note)
        names = ['prepare_annular_causal_inputs_20260916.py','run_annular_causal_correction_20260916.py',
            'run_annular_causal_correction_20260916_v2.py',
            'validate_annular_causal_correction_20260916.py','seal_annular_causal_correction_20260916.py']
        for name in names:
            path = root/'scripts'/name
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('sources_compile_without_bytecode',True,names)
        check('script_bytecode_cache_absent',not(root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        started = datetime(2026,9,16,15,37,4,tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=started]
        check('protected_workbench_mtime_changed_count_zero',not changed,changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot,'outputs')
        own(executed,'outputs')
        check('resume_and_executed_sealer_saved',True)
        report.update(state='complete',completed_at=datetime.now(timezone.utc).isoformat(),current_suite_checks=counts,
            total_successful_current_checks=sum(counts.values()),distinct_files_rehashed=len(cache),
            inherited_failed_attempts_preserved=previous['inherited_failed_attempts_preserved'],new_failed_attempts_preserved=[],
            corrected_results=statuses['validation']['cases'],numerical_controls=statuses['validation']['controls'],
            implementation_checks_not_physics_passes=True)
        save()
        print(json.dumps(dict(state='complete',checks=len(report['checks']),current_checks=sum(counts.values()),
            rehashed_files=len(cache),protected_changed=len(changed),failed_attempts_preserved=report['inherited_failed_attempts_preserved'])),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__=='__main__':
    main()
