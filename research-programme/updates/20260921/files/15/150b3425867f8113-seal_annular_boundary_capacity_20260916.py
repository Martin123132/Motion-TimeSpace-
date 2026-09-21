import hashlib
import json
import re
import traceback
from datetime import datetime,timezone
from pathlib import Path
from navier_stokes_source_audit_20260908 import limit_process


def main():
    limit_process()
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    destination = intake/'annular-boundary-capacity-final-integrity.json'
    snapshot = intake/'annular-boundary-capacity-resume-snapshot.md'
    executed = intake/'annular-boundary-capacity-executed-sealer.py'
    if any(path.exists() for path in [destination,snapshot,executed]):
        raise FileExistsError('Executed sources, evidence and seals are immutable.')
    report = dict(state='running',checks=[],inputs={},outputs={},full_GR_limit_proven=False,
        valid_for_physics_claim=False,complete_parent_source_action_derived=False,
        live_quadratic_geometry_qualified=False,uniform_all_time_force_bound_proven=False,
        github_action=False,subagents_used=False,protected_scan_scope='mtime since2026-09-15T23:14:28Z, not a pre-turn hash baseline.')
    cache = {}

    def digest(path):
        path = path.resolve()
        if path not in cache:
            value = hashlib.sha256()
            with path.open('rb') as stream:
                while chunk := stream.read(1024*1024):
                    value.update(chunk)
            cache[path] = value.hexdigest()
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
                path.relative_to(root)
                normalized = str(path.relative_to(root))
                if not path.is_file() or digest(path)!=expected:
                    raise RuntimeError('Missing or altered immutable evidence: '+name)
                if normalized in report['inputs'] and report['inputs'][normalized]!=expected:
                    raise RuntimeError('Conflicting digest: '+name)
                report['inputs'][normalized] = expected

    save()
    try:
        prior_path = intake/'annular-quadratic-crossing-final-integrity.json'
        prior = json.loads(prior_path.read_text())
        check('previous_checkpoint_complete',prior['state']=='complete' and all(row['passed'] for row in prior['checks']))
        inherit(prior)
        own(prior_path)
        statuses,counts = {},{}
        for label,folder,count in [
            ('projection','annular-variational-initial-projection-attempt02',49),
            ('inertia','annular-boundary-inertia-attempt01',56),
            ('capacity','annular-boundary-capacity-attempt01',4),
            ('local_action','annular-local-refinement-qualification-attempt04',72),
            ('stiffness','annular-local-stiffness-attempt01',4),
            ('crossing','annular-local-refinement-crossing-attempt02',16),
            ('tight_controls','annular-local-tight-controls-attempt01',7),
            ('trace_relaxation','annular-Gram-trace-relaxation-attempt01',11),
            ('precision','annular-local-crossing-precision-attempt01',25)]:
            path = intake/folder/'status.json'
            status = json.loads(path.read_text())
            json.dumps(status,allow_nan=False)
            check(label+'_complete',status['state']=='complete' and len(status['checks'])==count and all(row['passed'] for row in status['checks']))
            check(label+'_broad_claims_false',not status['full_GR_limit_proven'] and not status['valid_for_physics_claim'] and not status['complete_parent_source_action_derived'])
            inherit(status)
            own(path)
            statuses[label],counts[label] = status,count
        failed_folders = ['annular-variational-initial-projection-attempt01','annular-local-refinement-qualification-attempt01',
            'annular-local-refinement-qualification-attempt02','annular-local-refinement-qualification-attempt03','annular-local-refinement-crossing-attempt01']
        for folder in failed_folders:
            path = intake/folder/'status.json'
            failed = json.loads(path.read_text())
            check(folder+'_failure_preserved',failed['state']=='failed')
            inherit(failed)
            own(path)
        check('ineffective_projection_not_claimed_as_cure',all(not row['variants'][-1]['initial_force_gate'] for row in statuses['projection']['cases'] if row['degree']==2 and row['count']==1025)
            and statuses['crossing']['initial_Ritz_projection_not_adopted'])
        check('inertia_is_retained_not_subtracted',statuses['inertia']['all_source_inertia_retained'] and statuses['inertia']['local_initial_law_not_asserted_exact'])
        trace = statuses['trace_relaxation']
        check('trace_identity_not_promoted_to_replacement_dynamics',not trace['dynamic_relaxation_to_static_minimizer_proven']
            and not trace['permission_to_replace_action_by_static_relaxation'] and trace['full_energy_or_augmented_trace_domain_not_ruled_out'])
        decisions = {(row['count'],row['source_splits']) for row in statuses['capacity']['local_refinement_decisions']}
        check('capacity_prescribes_same_refinement_to_both_branches',decisions=={(257,8),(513,4)} and statuses['capacity']['frozen_weight_leading_law_not_exact'])
        crossing = statuses['crossing']['cases']
        check('complete_paired_refinement_matrix',{(row['base_count'],row['source_splits'],row['branch']) for row in crossing}
            == {(count,splits,branch) for count,splits in decisions for branch in ['reference','MTS']})
        check('expected_unknown_count_and_original_Gram_rows',all(row['scalar_dofs']==2*row['base_count']+4*(row['source_splits']-1) for row in crossing)
            and statuses['crossing']['all_original_vertex_Gram_rows_retained'] and statuses['local_action']['all_original_vertex_Gram_rows_retained'])
        check('unchanged_physical_data_and_accuracy_gates',statuses['crossing']['original_crossing_data_and_gates_unchanged']
            and statuses['crossing']['prespecified_accuracy_gates']==dict(field=.005,source=5e-7,velocity=2e-5,clock=2e-7,force_absolute=2e-7,force_relative=.02))
        check('original_full_source_momentum_and_no_force_projection',statuses['crossing']['source_field_momentum_derivative_retained']
            and not statuses['crossing']['energy_projection'] and statuses['local_action']['no_force_correction'])
        check('force_and_field_flags_recomputed',all(row['strict_force_gate']==(row['final_force_absolute_error']<2e-7 and row['final_force_relative_error']<.02)
            and row['strict_waveform_gate']==(row['maximum_field_error']<.005)
            and row['stricter_nine_time_absolute_force_gate']==(max(row['sampled_force_errors512'])<2e-7) for row in crossing))
        check('source_clock_flags_recomputed',all(row['strict_source_clock_gate']==(row['maximum_source_error']<5e-7 and row['maximum_velocity_error']<2e-5 and row['maximum_clock_error']<2e-7) for row in crossing))
        check('completed_reference_reused_without_relabelling_as_new_run',sum(bool(row.get('reused_completed_reference')) for row in crossing)==1)
        precision = statuses['precision']['cases']
        lookup = {(row['base_count'],row['branch']):row for row in crossing}
        check('precision_covers_every_branch_and_resolution',{(row['count'],row['branch']) for row in precision}==set(lookup))
        check('all_reference_flags_recomputed',all(row['final_force_passes_all_three_references']==all(row['final_force_flags_by_reference'].values())
            and row['sampled_force_passes_all_three_references']==all(row['sampled_force_flags_by_reference'].values())
            and set(row['force_errors'])=={'384','512','768'}
            and all(row['final_force_flags_by_reference'][degree]==(errors[-1]<2e-7 and errors[-1]/abs(row['reference_final_forces'][degree])<.02)
                and row['sampled_force_flags_by_reference'][degree]==(max(errors)<2e-7) for degree,errors in row['force_errors'].items()) for row in precision))
        check('precision_original_flags_preserved',all(row['original_final_force_gate']==lookup[(row['count'],row['branch'])]['strict_force_gate']
            and row['original_sampled_force_gate']==lookup[(row['count'],row['branch'])]['stricter_nine_time_absolute_force_gate'] for row in precision))
        check('both_fine_temporal_controls_preserved_without_full_time_overclaim',all(row.get('temporal_control_not_full_duration')
            and row['temporal_control_duration']==.05 and row['temporal_control_rtol']==2e-12 for row in precision if row['count']==513))
        note = root/'DERIVATION-20260916-boundary-capacity-and-local-source-refinement.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json))`',content)
        check('all_cited_local_paths_exist',all((root/name).is_file() for name in cited),cited)
        check('main_note_complete_and_scope_explicit','EVOLUTION_RESULTS_PENDING' not in content and 'not a full GR limit' in content)
        own(note)
        modules = ['annular_variational_initial_projection_20260916.py','annular_variational_initial_projection_20260916_v2.py',
            'verify_annular_variational_initial_projection_20260916.py','verify_annular_variational_initial_projection_20260916_v2.py',
            'derive_annular_boundary_inertia_20260916.py','derive_annular_boundary_capacity_20260916.py','annular_locally_refined_source_action_20260916.py',
            'verify_annular_local_refinement_20260916.py','verify_annular_local_refinement_20260916_v2.py','verify_annular_local_refinement_20260916_v3.py',
            'verify_annular_local_refinement_20260916_v4.py','annular_local_spectral_step_20260916.py','measure_annular_local_stiffness_20260916.py',
            'run_annular_local_refinement_crossing_20260916.py','run_annular_local_refinement_crossing_20260916_v2.py',
            'run_annular_local_tight_controls_20260916.py',
            'derive_annular_Gram_trace_relaxation_20260916.py',
            'verify_annular_local_crossing_precision_20260916.py','seal_annular_boundary_capacity_20260916.py']
        for name in modules:
            path = root/'scripts'/name
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('new_modules_compile_without_bytecode',True,modules)
        check('script_bytecode_cache_absent',not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        started = datetime(2026,9,15,23,14,28,tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= started]
        check('protected_workbench_mtime_changed_count_zero',not changed,changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot,'outputs')
        own(executed,'outputs')
        check('resume_snapshot_and_executed_sealer_saved',True)
        report.update(state='complete',completed_at=datetime.now(timezone.utc).isoformat(),current_suite_checks=counts,
            total_successful_current_checks=sum(counts.values()),distinct_files_rehashed=len(cache),
            inherited_failed_attempts_preserved=prior['inherited_failed_attempts_preserved']+len(failed_folders),
            refinement_results=crossing,qualified_precision_results=precision,
            implementation_checks_not_all_physical_accuracy_passes=True)
        save()
        print(json.dumps(dict(state='complete',checks=len(report['checks']),current_checks=sum(counts.values()),
            rehashed_files=len(cache),protected_changed=len(changed))),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
