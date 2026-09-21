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
    destination = intake/'annular-source-refinement-final-integrity.json'
    snapshot = intake/'annular-source-refinement-resume-snapshot.md'
    executed = intake/'annular-source-refinement-executed-sealer.py'
    if any(path.exists() for path in [destination,snapshot,executed]):
        raise FileExistsError('Immutable evidence already exists.')
    report = dict(state='running',checks=[],inputs={},outputs={},full_GR_limit_proven=False,
        valid_for_physics_claim=False,continuum_limit_proven=False,uniform_time_bound=False,
        github_action=False,subagents_used=False,implementation_checks_not_physics_passes=True,
        protected_scan_scope='mtime since turn start2026-09-17T10:05:37Z; not a pre-turn full hash baseline')
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
        previous_path = intake/'annular-GR-causal-final-integrity.json'
        previous = json.loads(previous_path.read_text())
        check('previous_seal_complete',previous['state']=='complete' and all(row['passed'] for row in previous['checks']))
        inherit(previous)
        own(previous_path)
        specifications = [('inputs','annular-GR-causal-refinement-inputs-attempt01',19,3),
            ('prediction768','annular-GR-causal-refinement-768-attempt01',9,2),
            ('prediction512','annular-GR-causal-refinement-512-attempt01',9,2),
            ('trace','annular-source-trace-refinement-attempt03',97,6),
            ('validation','annular-GR-causal-refinement-validation-attempt01',23,4)]
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
        for degree in [768,512]:
            status = statuses['prediction'+str(degree)]
            configuration = status['configuration']
            inputs = {str(Path(path)) for path in status['inputs'] if Path(path).suffix.lower() in ['.npz','.npy']}
            check(str(degree)+'_independent_fine_response',not status['finite_future_trajectories_read']
                and not status['force_fit'] and not status['retrospective_force_subtraction']
                and status['original_action_unchanged'] and status['all_modes_and_Gram_rows_retained']
                and status['reconstruction_derivative_is_own_exact_derivative']
                and status['original_initial_projection_error_retained']
                and status['known_benchmark_not_blind_new_experiment']
                and inputs=={str(Path(path)) for path in status['npz_read_allowlist']}
                and len(inputs)==1 and {row['branch'] for row in status['cases']}=={'reference','MTS'}
                and status['count']==1025 and status['source_splits']==8 and status['final_time']==.4
                and configuration['degree']==degree and configuration['stride']==1
                and configuration['spectral_step_multiplier']==1.)
            label = 'annular-GR-causal-refinement-'+str(degree)+'-attempt01'
            for branch in ['reference','MTS']:
                with np.load(intake/label/(branch+'-prediction.npz'),allow_pickle=False) as saved:
                    predictions[(label,branch)] = {key:saved[key].copy() for key in ['force_reconstructed','force_linear']}
        trace = statuses['trace']
        check('source_trace_scope_explicit',not trace['finite_future_trajectories_read']
            and not trace['force_fit'] and not trace['force_correction'] and not trace['interval_arithmetic']
            and trace['conditional_smoothness_not_assumed_for_continuum']
            and trace['local_trace_identity_not_global_force_convergence']
            and len(trace['mesh_cases'])==7 and all(not row['continuum_jet_bounds_established'] for row in trace['cases']))
        check('trace_all_meshes_and_reference_degrees',
            {(row['count'],row['degree']) for row in trace['cases']}=={(count,degree) for count in [257,513,1025] for degree in [512,768]})
        failed_paths = []
        for attempt,marker in [('01','1025_piecewise_quintic_jump'),('02','2049_unit_hinge_jump')]:
            path = intake/('annular-source-trace-refinement-attempt'+attempt)/'status.json'
            failed = json.loads(path.read_text())
            check('coordinate_roundoff_attempt'+attempt+'_preserved',failed['state']=='failed' and marker in failed['error'])
            inherit(failed)
            own(path)
            failed_paths.append(str(path.relative_to(root)))
        report['trace_approximation_diagnostics'] = [dict(count=row['count'],degree=row['degree'],
            cubic_trace_improves_zero_correction=row['maximum_cubic_trace_residual']<row['maximum_trace_error'],
            quartic_trace_improves_zero_correction=row['maximum_quartic_trace_residual']<row['maximum_trace_error'],
            curvature_factor_improves_zero_factor=row['maximum_quadratic_factor_residual']<row['maximum_source_factor_norm'],
            cubic_source_force_improves_zero_force=row['maximum_cubic_source_force_residual']<row['maximum_source_row_Gram_force'])
            for row in trace['cases']]
        check('failed_pointwise_jet_shortcut_explicit',all(not row['cubic_trace_improves_zero_correction']
            and not row['quartic_trace_improves_zero_correction'] and not row['curvature_factor_improves_zero_factor']
            and not row['cubic_source_force_improves_zero_force'] for row in report['trace_approximation_diagnostics']))
        validation = statuses['validation']
        folder = intake/'annular-GR-causal-refinement-validation-attempt01'
        manifest = json.loads((folder/'frozen-predictions-before-finite-comparison.json').read_text())
        frozen = datetime.fromisoformat(manifest['frozen_at'])
        check('four_fine_predictions_frozen_before_comparison',validation['predictions_frozen_before_future_state_reads']
            and manifest['future_finite_states_not_yet_opened'] and len(manifest['predictions'])==4
            and validation['freeze_time']==manifest['frozen_at']
            and frozen<datetime.fromisoformat(validation['future_state_read_phase_began_at'])
            and all(datetime.fromisoformat(row['predictor_completed_at'])<=frozen
                and digest(root/row['path'])==row['sha256'] for row in manifest['predictions']))
        accurate_flags,linear_flags,physical_flags = [],[],[]
        for row in validation['cases']:
            label,branch = row['label'],row['branch']
            with np.load(folder/(label+'-'+branch+'-comparison.npz'),allow_pickle=False) as saved:
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
        check('prediction_gates_recomputed',len(accurate_flags)==4
            and validation['all_reconstructed_predictions_pass']==all(accurate_flags)
            and validation['all_linear_predictions_pass']==all(linear_flags))
        reconstructed_controls,linear_controls = [],[]
        for row in validation['numerical_controls']:
            selected = predictions[(row['label'],row['branch'])]
            baseline = predictions[('annular-GR-causal-refinement-768-attempt01',row['branch'])]
            reconstructed = float(np.max(abs(selected['force_reconstructed']-baseline['force_reconstructed'])))
            linear = float(np.max(abs(selected['force_linear']-baseline['force_linear'])))
            reconstructed_controls.append(reconstructed<2e-8)
            linear_controls.append(linear<2e-8)
            if not (reconstructed==row['reconstructed_force_change'] and linear==row['linear_force_change']
                and row['reconstructed_control_resolved']==(reconstructed<2e-8)
                and row['linear_control_resolved']==(linear<2e-8)):
                raise RuntimeError('Incorrect reference control: '+row['label']+row['branch'])
        check('reference_degree_control_recomputed',len(reconstructed_controls)==2
            and validation['all_prespecified_controls_present']
            and validation['all_reconstructed_controls_resolved']==all(reconstructed_controls)
            and validation['all_linear_controls_resolved']==all(linear_controls))
        check('force_failures_and_unperformed_fine_time_control_honest',not any(physical_flags)
            and not validation['fine_predictor_tighter_time_control_performed']
            and not validation['spatial_convergence_proven'] and not validation['uniform_trajectory_bound'])
        for row in validation['refinement_comparisons']:
            if not (row['coarse_phase']=='3/5' and row['fine_phase']=='1/5'
                and row['actual_peak_ratio']==row['fine_actual_maximum']/row['coarse_actual_maximum']
                and row['predicted_peak_ratio']==row['fine_predicted_maximum']/row['coarse_predicted_maximum']
                and row['two_grid_ratios_are_not_a_uniform_convergence_proof']):
                raise RuntimeError('Incorrect refinement summary.')
        check('both_branches_paired_refinement',len(validation['refinement_comparisons'])==4)
        path = intake/'annular-joint-validation-attempt03/status.json'
        old_time = json.loads(path.read_text())
        own(path)
        controls = [row for row in old_time['time_controls'] if row['count']==1025]
        check('original_fine_time_controls_reused_not_rerun',old_time['state']=='complete' and len(controls)==2
            and validation['original_fine_trajectory_time_controls_reused'])
        note = root/'DERIVATION-20260917-source-trace-law-and-causal-refinement.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json))`',content)
        check('cited_note_paths_exist',all((root/name).is_file() for name in cited),cited)
        check('finished_note_scoped','PENDING' not in content and 'not the full GR limit' in content
            and 'not a time-evolution stability theorem' in content)
        own(note)
        names = ['prepare_annular_GR_causal_refinement_20260917.py','run_annular_GR_causal_refinement_20260917.py',
            'derive_annular_source_trace_refinement_20260917.py','derive_annular_source_trace_refinement_20260917_v2.py',
            'derive_annular_source_trace_refinement_20260917_v3.py','validate_annular_GR_causal_refinement_20260917.py',
            'seal_annular_source_refinement_20260917.py']
        for name in names:
            path = root/'scripts'/name
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('new_sources_compile',True,names)
        check('script_bytecode_cache_absent',not(root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        started = datetime(2026,9,17,10,5,37,tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=started]
        check('protected_workbench_mtime_changed_count_zero',not changed,changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot,'outputs')
        own(executed,'outputs')
        check('resume_and_executed_source_preserved',True)
        report.update(state='complete',completed_at=datetime.now(timezone.utc).isoformat(),current_suite_checks=counts,
            total_successful_current_checks=sum(counts.values()),distinct_files_rehashed=len(cache),
            inherited_failed_attempts_preserved=previous['inherited_failed_attempts_preserved']+len(failed_paths),
            new_failed_attempts_preserved=failed_paths,pointwise_jet_shortcut_claimed=False,
            results=validation['cases'],refinement_comparisons=validation['refinement_comparisons'],
            source_trace_results=trace['cases'],numerical_controls=validation['numerical_controls'],
            all_predictions_within_gate=all(accurate_flags) and all(linear_flags),
            reference_degree_control_resolved=all(reconstructed_controls) and all(linear_controls),
            fine_predictor_tighter_time_control_performed=False,original_failed_cases_preserved=True)
        save()
        print(json.dumps(dict(state='complete',checks=len(report['checks']),current_checks=sum(counts.values()),
            rehashed_files=len(cache),protected_changed=len(changed),failed_attempts_preserved=report['inherited_failed_attempts_preserved'],
            all_predictions_within_gate=report['all_predictions_within_gate'],
            reference_degree_control_resolved=report['reference_degree_control_resolved'])),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__=='__main__':
    main()
