from derive_annular_source_gravity_20260914 import EvidenceRun
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import re
import traceback
import numpy as np


def main():
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    destination = intake/'annular-GR-causal-final-integrity.json'
    snapshot = intake/'annular-GR-causal-resume-snapshot.md'
    executed = intake/'annular-GR-causal-executed-sealer.py'
    if any(path.exists() for path in [destination,snapshot,executed]):
        raise FileExistsError('Immutable evidence already exists.')
    report = dict(state='running',checks=[],inputs={},outputs={},full_GR_limit_proven=False,
        valid_for_physics_claim=False,continuum_limit_proven=False,uniform_time_bound=False,
        github_action=False,subagents_used=False,implementation_checks_not_physics_passes=True,
        protected_scan_scope='mtime since turn start2026-09-17T00:54:04Z; not a pre-turn full hash baseline')
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
        previous_path = intake/'annular-GR-projection-final-integrity.json'
        previous = json.loads(previous_path.read_text())
        check('previous_seal_complete',previous['state']=='complete' and all(row['passed'] for row in previous['checks']))
        inherit(previous)
        own(previous_path)
        specifications = [('inputs','annular-GR-causal-inputs-attempt01',19,3)]
        for name in ['standard','tight','reconstruction','oracle512','oracle384']:
            specifications.append((name,'annular-GR-causal-'+name+'-attempt01',9,2))
        specifications.append(('validation','annular-GR-causal-validation-attempt01',39,10))
        statuses,counts = {},{}
        for name,label,count,cases in specifications:
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
        check('GR_only_preparation',not statuses['inputs']['finite_future_trajectories_read'])
        predictions = {}
        expected = {(768,1,1.),(768,1,.5),(768,2,1.),(512,1,1.),(384,1,1.)}
        observed = set()
        for name in ['standard','tight','reconstruction','oracle512','oracle384']:
            status = statuses[name]
            configuration = status['configuration']
            observed.add((configuration['degree'],configuration['stride'],configuration['spectral_step_multiplier']))
            inputs = {str(Path(path)) for path in status['inputs'] if Path(path).suffix.lower() in ['.npz','.npy']}
            check(name+'_independent_original_response',not status['finite_future_trajectories_read']
                and not status['force_fit'] and not status['retrospective_force_subtraction']
                and status['original_action_unchanged'] and status['all_modes_and_Gram_rows_retained']
                and status['reconstruction_derivative_is_own_exact_derivative']
                and status['original_initial_projection_error_retained']
                and status['known_benchmark_not_blind_new_experiment']
                and inputs=={str(Path(path)) for path in status['npz_read_allowlist']}
                and len(inputs)==1 and {row['branch'] for row in status['cases']}=={'reference','MTS'}
                and status['count']==513 and status['source_splits']==8 and status['final_time']==.4)
            label = 'annular-GR-causal-'+name+'-attempt01'
            for branch in ['reference','MTS']:
                with np.load(intake/label/(branch+'-prediction.npz'),allow_pickle=False) as saved:
                    predictions[(label,branch)] = {key:saved[key].copy() for key in ['force_reconstructed','force_linear','oracle_forces']}
        check('all_prespecified_independent_controls',observed==expected and statuses['validation']['all_prespecified_controls_present'])
        validation = statuses['validation']
        validation_folder = intake/'annular-GR-causal-validation-attempt01'
        manifest = json.loads((validation_folder/'frozen-predictions-before-finite-comparison.json').read_text())
        frozen = datetime.fromisoformat(manifest['frozen_at'])
        check('all_predictions_frozen_before_future_comparison',validation['predictions_frozen_before_future_state_reads']
            and manifest['future_finite_states_not_yet_opened'] and len(manifest['predictions'])==10
            and validation['freeze_time']==manifest['frozen_at']
            and frozen<datetime.fromisoformat(validation['future_state_read_phase_began_at'])
            and all(datetime.fromisoformat(row['predictor_completed_at'])<=frozen
                and digest(root/row['path'])==row['sha256'] for row in manifest['predictions']))
        accurate_flags,linear_flags,physical_flags = [],[],[]
        for row in validation['cases']:
            label,branch = row['label'],row['branch']
            with np.load(validation_folder/(label+'-'+branch+'-comparison.npz'),allow_pickle=False) as saved:
                reconstructed = float(np.max(abs(saved['reconstructed_error'])))
                linear = float(np.max(abs(saved['linear_error'])))
                actual_GR = float(np.max(abs(saved['actual_GR_error'])))
                predicted_GR = float(np.max(abs(saved['reconstructed_GR_error'])))
            accurate_flags.append(reconstructed<2e-7)
            linear_flags.append(linear<2e-7)
            physical_flags.append(actual_GR<2e-7)
            if not (reconstructed==row['maximum_reconstructed_force_prediction_error']
                and linear==row['maximum_linear_force_prediction_error']
                and actual_GR==row['maximum_original_GR_force_error']
                and predicted_GR==row['maximum_predicted_GR_force_error']
                and row['reconstructed_prediction_2e7_pass']==(reconstructed<2e-7)
                and row['linear_prediction_2e7_pass']==(linear<2e-7)
                and row['original_GR_force_gate_pass']==(actual_GR<2e-7)
                and row['predicted_GR_force_gate_pass']==(predicted_GR<2e-7)):
                raise RuntimeError('Incorrect acceptance flag: '+label+branch)
        check('prediction_and_physics_gates_recomputed_separately',len(accurate_flags)==10
            and validation['all_reconstructed_predictions_pass']==all(accurate_flags)
            and validation['all_linear_predictions_pass']==all(linear_flags))
        reconstructed_controls,linear_controls = [],[]
        for row in validation['numerical_controls']:
            selected = predictions[(row['label'],row['branch'])]
            baseline = predictions[('annular-GR-causal-standard-attempt01',row['branch'])]
            reconstructed = float(np.max(abs(selected['force_reconstructed']-baseline['force_reconstructed'])))
            linear = float(np.max(abs(selected['force_linear']-baseline['force_linear'])))
            reconstructed_controls.append(reconstructed<2e-8)
            linear_controls.append(linear<2e-8)
            if not (reconstructed==row['reconstructed_force_change'] and linear==row['linear_force_change']
                and row['reconstructed_control_resolved']==(reconstructed<2e-8)
                and row['linear_control_resolved']==(linear<2e-8)):
                raise RuntimeError('Incorrect numerical control: '+row['label']+row['branch'])
        check('control_gates_recomputed_without_changing_reference',len(reconstructed_controls)==8
            and validation['all_reconstructed_controls_resolved']==all(reconstructed_controls)
            and validation['all_linear_controls_resolved']==all(linear_controls))
        check('original_GR_force_failures_not_reclassified',not any(physical_flags)
            and not validation['full_GR_limit_proven'] and not validation['uniform_trajectory_bound'])
        note = root/'DERIVATION-20260917-causal-GR-driven-field-source-response.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json))`',content)
        check('cited_note_paths_exist',all((root/name).is_file() for name in cited),cited)
        check('finished_note_scoped','PENDING' not in content and 'not the full GR limit' in content
            and 'not a claim of statistical' in content and 'does not remove' in content)
        own(note)
        names = ['annular_GR_causal_predictor_20260917.py','prepare_annular_GR_causal_predictor_20260917.py',
            'run_annular_GR_causal_predictor_20260917.py','validate_annular_GR_causal_predictor_20260917.py',
            'seal_annular_GR_causal_predictor_20260917.py']
        for name in names:
            path = root/'scripts'/name
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('new_sources_compile',True,names)
        check('script_bytecode_cache_absent',not(root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        started = datetime(2026,9,17,0,54,4,tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=started]
        check('protected_workbench_mtime_changed_count_zero',not changed,changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot,'outputs')
        own(executed,'outputs')
        check('resume_and_executed_source_preserved',True)
        report.update(state='complete',completed_at=datetime.now(timezone.utc).isoformat(),current_suite_checks=counts,
            total_successful_current_checks=sum(counts.values()),distinct_files_rehashed=len(cache),
            inherited_failed_attempts_preserved=previous['inherited_failed_attempts_preserved'],new_failed_attempts_preserved=[],
            results=validation['cases'],numerical_controls=validation['numerical_controls'],
            all_predictions_within_gate=all(accurate_flags) and all(linear_flags),
            all_numerical_controls_resolved=all(reconstructed_controls) and all(linear_controls),
            original_failed_cases_preserved=True)
        save()
        print(json.dumps(dict(state='complete',checks=len(report['checks']),current_checks=sum(counts.values()),
            rehashed_files=len(cache),protected_changed=len(changed),failed_attempts_preserved=report['inherited_failed_attempts_preserved'],
            all_predictions_within_gate=report['all_predictions_within_gate'],
            all_numerical_controls_resolved=report['all_numerical_controls_resolved'])),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__=='__main__':
    main()
