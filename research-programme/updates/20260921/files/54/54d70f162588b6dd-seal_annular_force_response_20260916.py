from derive_annular_source_gravity_20260914 import EvidenceRun
import hashlib
import json
import re
import traceback
import numpy as np
from datetime import datetime, timezone
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    destination = intake/'annular-force-response-final-integrity.json'
    snapshot = intake/'annular-force-response-resume-snapshot.md'
    executed = intake/'annular-force-response-executed-sealer.py'
    if any(path.exists() for path in [destination,snapshot,executed]):
        raise FileExistsError('Evidence and executed sources are immutable.')
    report = dict(state='running',checks=[],inputs={},outputs={},full_GR_limit_proven=False,
        valid_for_physics_claim=False,uniform_nonlinear_remainder_bound=False,continuum_limit_proven=False,
        github_action=False,subagents_used=False,
        protected_scan_scope='mtime since 2026-09-16T14:40:57Z, not a pre-turn full hash baseline')
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
                    raise RuntimeError('Conflicting immutable digest: '+name)
                report['inputs'][key] = expected

    save()
    try:
        previous_path = intake/'annular-anchored-moving-final-integrity.json'
        previous = json.loads(previous_path.read_text())
        check('previous_checkpoint_complete',previous['state']=='complete' and all(row['passed'] for row in previous['checks']))
        inherit(previous)
        own(previous_path)
        statuses,counts = {},{}
        for label,folder,count,cases in [('linearization','annular-full-force-linearization-attempt01',60,12),
            ('paths','annular-force-response-paths-attempt01',18,2),('adjoint','annular-force-adjoint-response-attempt01',18,4),
            ('tight','annular-force-adjoint-tight-attempt01',8,2),('controls','annular-force-response-controls-attempt01',13,2)]:
            path = intake/folder/'status.json'
            status = json.loads(path.read_text())
            json.dumps(status,allow_nan=False)
            check(label+'_complete',status['state']=='complete' and len(status['checks'])==count and len(status['cases'])==cases
                and all(row['passed'] for row in status['checks']))
            check(label+'_broad_claims_false',not status['full_GR_limit_proven'] and not status['valid_for_physics_claim']
                and not status['complete_parent_source_action_derived'])
            inherit(status)
            own(path)
            statuses[label],counts[label] = status,count
        check('linearization_both_backgrounds_and_branches',
            {(row['branch'],row['base_count'],row['background'],row['moved']) for row in statuses['linearization']['cases']}
            =={(branch,count,mass,moved) for branch in ['reference','MTS'] for count,mass in [(33,0.),(33,.7),(129,0.)] for moved in [False,True]})
        for branch in ['reference','MTS']:
            row = next(row for row in statuses['paths']['cases'] if row['branch']==branch)
            path = intake/'annular-force-response-paths-attempt01'/(branch+'-physical-paths.npz')
            with np.load(path) as saved:
                check(branch+'_full_path_shapes',saved['raw_states'].shape==(321,575)
                    and saved['prepared_states'].shape==(321,575) and saved['reduced_states'].shape==(321,575)
                    and saved['times'][0]==0. and saved['times'][-1]==.005)
                observed = float(np.max(abs(saved['total_force_effect'])))
                check(branch+'_nonlinear_attribution_recomputed',np.max(abs(saved['initial_force_effect']+saved['moving_force_effect']-saved['total_force_effect']))<2e-18
                    and abs(row['endpoint_total_difference']-saved['total_force_effect'][-1])<2e-18)
                check(branch+'_finer_force_flags_not_hidden',row['maximum_total_difference']==observed
                    and row['finer_sample_budget_met']==(observed<=2e-7))
            check(branch+'_same_original_preparation_and_replay',row['maximum_force_replay_error']<2e-10
                and row['counterfactual_split_is_exact_algebra_but_order_dependent'] and row['nonlinear_evolution_not_linearized'])
        for label in ['adjoint','tight']:
            for row in statuses[label]['cases']:
                prefix = label+'_'+row['branch']+'_'+str(row['stride'])
                physical = row['direct_same_state_omission']+row['initial_preparation_linear_response']+row['accumulated_motion_linear_response']
                numerical = row['reduced_interpolation_contribution']+row['full_replay_residual_contribution']
                nonlinear = row['dynamical_nonlinear_remainder']+row['observable_nonlinear_remainder']
                check(prefix+'_identity_recomputed',abs(physical+numerical+nonlinear-row['observed_total_force_difference'])<2e-10
                    and abs(physical-row['physical_linear_prediction'])<2e-18)
                qualified = abs(physical-row['observed_total_force_difference'])<2e-10 and abs(numerical)<2e-10 and abs(nonlinear)<2e-10
                check(prefix+'_attribution_flag_recomputed',row['physical_linear_attribution_qualified']==qualified)
                check(prefix+'_full_reconstruction_and_nonlinearity_explicit',row['absolute_reconstruction_contributions']>=abs(numerical)-2e-18
                    and row['nonlinear_remainder_is_measured_not_uniform_bound'] and row['initial_adjoint_clock_component']==0.)
        check('independent_forward_backward_controls',all(row['tangent_adjoint_maximum_difference']<2e-10
            for row in statuses['adjoint']['cases'] if row['stride']==1))
        check('both_resolution_and_time_controls_pass',all(max(row['path_refinement_changes'].values())<2e-10
            and max(row['time_refinement_changes'].values())<2e-10 and not row['uniform_nonlinear_bound']
            for row in statuses['controls']['cases']))
        note = root/'DERIVATION-20260916-moving-force-attribution-and-adjoint.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json))`',content)
        check('all_note_paths_exist',all((root/name).is_file() for name in cited),cited)
        check('finished_note_scoped_and_remainders_explicit','PENDING' not in content and 'not a full GR limit' in content
            and 'NOT a uniform state-tube bound' in content and 'I_full,recon' in content)
        own(note)
        names = ['annular_full_force_linearization_20260916.py','verify_annular_full_force_linearization_20260916.py',
            'run_annular_force_response_paths_20260916.py','annular_force_adjoint_response_20260916.py',
            'run_annular_force_adjoint_response_20260916.py','verify_annular_force_response_controls_20260916.py',
            'seal_annular_force_response_20260916.py']
        for name in names:
            path = root/'scripts'/name
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('new_sources_compile_without_bytecode',True,names)
        check('script_bytecode_cache_absent',not(root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        started = datetime(2026,9,16,14,40,57,tzinfo=timezone.utc).timestamp()
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
            tight_response_results=statuses['tight']['cases'],attribution_controls=statuses['controls']['cases'],
            original_GR_failures_unchanged=True,implementation_checks_not_physics_passes=True)
        save()
        print(json.dumps(dict(state='complete',checks=len(report['checks']),current_checks=sum(counts.values()),
            rehashed_files=len(cache),protected_changed=len(changed),failed_attempts_preserved=report['inherited_failed_attempts_preserved'])),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__=='__main__':
    main()
