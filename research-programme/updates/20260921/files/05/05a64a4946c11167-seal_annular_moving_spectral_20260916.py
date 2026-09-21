from derive_annular_source_gravity_20260914 import EvidenceRun
import hashlib
import json
import re
import traceback
from datetime import datetime,timezone
from pathlib import Path


def main():
    root=Path(__file__).resolve().parents[1]
    intake=root/'source-intake/navier-stokes/20260914'
    destination=intake/'annular-moving-spectral-final-integrity.json'
    snapshot=intake/'annular-moving-spectral-resume-snapshot.md'
    executed=intake/'annular-moving-spectral-executed-sealer.py'
    if any(path.exists() for path in [destination,snapshot,executed]):
        raise FileExistsError('Executed sources and evidence are immutable.')
    report=dict(state='running',checks=[],inputs={},outputs={},full_GR_limit_proven=False,
        valid_for_physics_claim=False,moving_reduced_trajectory_verified=False,live_metric_action_varied=False,
        github_action=False,subagents_used=False,
        protected_scan_scope='mtime since 2026-09-16T12:41:39Z; not a pre-turn full hash baseline')
    cache={}

    def digest(path):
        path=path.resolve()
        if path not in cache:
            value=hashlib.sha256()
            with path.open('rb') as stream:
                while chunk:=stream.read(1024*1024):
                    value.update(chunk)
            cache[path]=value.hexdigest()
        return cache[path]

    def own(path,table='inputs'):
        report[table][str(path.resolve().relative_to(root))]=digest(path)

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
                path=(root/name).resolve()
                normalized=str(path.relative_to(root))
                if not path.is_file() or digest(path)!=expected:
                    raise RuntimeError('Missing or altered immutable evidence: '+name)
                if normalized in report['inputs'] and report['inputs'][normalized]!=expected:
                    raise RuntimeError('Conflicting digest: '+name)
                report['inputs'][normalized]=expected

    save()
    try:
        previous_path=intake/'annular-dynamic-reduction-final-integrity.json'
        previous=json.loads(previous_path.read_text())
        check('previous_checkpoint_complete',previous['state']=='complete' and all(row['passed'] for row in previous['checks']))
        inherit(previous)
        own(previous_path)
        statuses,counts={},{}
        for label,folder,count,cases in [
            ('connection','annular-moving-spectral-connection-attempt02',193,16),
            ('curvature','annular-spectral-clusters-curvature-attempt03',62,8),
            ('preliminary_force','annular-motion-driven-mode-force-attempt01',78,12),
            ('canonical_force','annular-motion-driven-mode-force-attempt02',102,12)]:
            path=intake/folder/'status.json'
            status=json.loads(path.read_text())
            json.dumps(status,allow_nan=False)
            check(label+'_complete',status['state']=='complete' and len(status['cases'])==cases
                and len(status['checks'])==count and all(row['passed'] for row in status['checks']))
            check(label+'_broad_claims_false',not status['full_GR_limit_proven'] and not status['valid_for_physics_claim']
                and not status['complete_parent_source_action_derived'])
            inherit(status)
            own(path)
            statuses[label],counts[label]=status,count
        connection=statuses['connection']
        check('paired_action_qualification_matrix_complete',{(row['count'],row['source_splits'],row['branch'],row['background_mass'],row['position']) for row in connection['cases']}
            =={(count,splits,branch,mass,position) for count,splits in [(33,2),(65,4)] for branch in ['reference','MTS'] for mass in [0.,.7] for position in [6.03,6.035]})
        check('both_on_and_off_shell_controls_retained',all({item['on_shell'] for item in row['EL_controls']}=={False,True}
            and all(item['cotangent_residual_error']<2e-9 for item in row['EL_controls']) for row in connection['cases']))
        check('first_frame_derivatives_converged_without_threshold_change',all(len(row['finite_difference_controls'])>=2
            and all(item['relative_frame_derivative_error']<2e-4 for item in row['finite_difference_controls'][-2:]) for row in connection['cases']))
        curvature=statuses['curvature']
        check('exact_degenerate_projector_control_retained',curvature['synthetic_cluster']['internal_gap']==0
            and curvature['synthetic_cluster']['projector_derivative_error']<2e-8 and curvature['synthetic_cluster']['synthetic_not_physical_evidence'])
        check('analytic_curvature_not_replaced_by_finite_difference',all(row['curvature_analytically_derived'] and row['finite_difference_not_used_as_curvature']
            and row['numerical_cluster_relative_gap']==1e-3 for row in curvature['cases']))
        check('two_independent_curvature_step_controls_pass',all(len(row['second_frame_controls'])>=2
            and all(item.get('relative_second_frame_error',1.)<3e-3 for item in row['second_frame_controls'][-2:]) for row in curvature['cases']))
        force=statuses['canonical_force']
        rows=force['cases']
        check('paired_motion_fixture_matrix_complete',{(row['branch'],row['snapshot_time'],row['assigned_source_speed']) for row in rows}
            =={(branch,instant,speed) for branch in ['reference','MTS'] for instant in [0.,.2,.4] for speed in [0.,.06]})
        check('canonical_initial_projection_and_error_explicit',force['canonical_momentum_projection_derived'] and force['full_projection_error_recorded']
            and force['frozen_bound_not_reused_as_moving_preparation_bound']
            and all(row['preparation_energy_norm']>0 and row['initial_error_quantified_not_uniformly_propagated'] for row in rows))
        check('source_force_law_and_projection_decomposition_recomputed',all(abs(row['same_state_material_force_difference'])<=row['same_state_material_force_bound']+2e-14
            and abs(row['projection_source_force_difference']+row['same_state_material_force_difference']-row['total_fixture_source_force_difference'])<2e-12 for row in rows))
        check('fixture_flags_recomputed',all(row['same_state_sufficient_budget_met']==(row['same_state_material_force_bound']<=2e-7)
            and row['total_fixture_observed_budget_met']==(abs(row['total_fixture_source_force_difference'])<=2e-7) for row in rows))
        failures=[(row['branch'],row['snapshot_time'],row['assigned_source_speed']) for row in rows if not row['total_fixture_observed_budget_met']]
        check('reference_failure_not_hidden_or_called_GR_failure',failures==[('reference',.4,.06)],failures)
        check('full_moving_original_action_reproduced',all(row['full_acceleration_original_error']<2e-8 for row in rows))
        check('cluster_completion_counts_and_frozen_scope',all(row['retained_count']==(271 if row['branch']=='reference' else 273)
            and row['omitted_count']==286-row['retained_count'] and row['frozen_envelope_after_cluster_completion']<=2e-7 for row in rows))
        check('fixture_results_not_promoted_to_trajectories',all(not row['freely_evolved_reduced_trajectory'] and 'NOT a moving trajectory' in row['fixture'] for row in rows)
            and not force['all_time_reduced_error_bound'] and not force['moving_solver_implemented'] and force['physical_GR_gates_unchanged'])
        failed_attempts=[]
        for folder,cases in [('annular-moving-spectral-connection-attempt01',10),('annular-spectral-clusters-curvature-attempt01',0),('annular-spectral-clusters-curvature-attempt02',4)]:
            path=intake/folder/'status.json'
            failed=json.loads(path.read_text())
            check(folder+'_failure_preserved',failed['state']=='failed' and len(failed['cases'])==cases and bool(failed['error']))
            inherit(failed)
            own(path)
            failed_attempts.append(dict(folder=folder,error=failed['error']))
        note=root/'DERIVATION-20260916-moving-spectral-connection-and-omitted-force.md'
        content=note.read_text(encoding='utf-8')
        cited=re.findall(r'`([^`\r\n]+\.(?:py|md|json))`',content)
        check('all_cited_paths_exist',all((root/name).is_file() for name in cited),cited)
        check('note_complete_scope_and_failure_caveats','not a full GR limit' in content and 'NOT a freely evolved reduced solution' in content
            and 'reference final moving fixture fails' in content and 'NOT automatically a bound on this moving preparation' in content)
        own(note)
        modules=['annular_moving_spectral_frame_20260916.py','verify_annular_moving_spectral_connection_20260916.py',
            'verify_annular_moving_spectral_connection_20260916_v2.py','annular_moving_spectral_curvature_20260916.py',
            'verify_annular_spectral_clusters_20260916.py','verify_annular_spectral_clusters_20260916_v2.py','verify_annular_spectral_clusters_20260916_v3.py',
            'derive_annular_motion_driven_mode_force_20260916.py','derive_annular_motion_driven_mode_force_20260916_v2.py',
            'seal_annular_moving_spectral_20260916.py']
        for name in modules:
            path=root/'scripts'/name
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('new_scripts_compile_without_bytecode',True,modules)
        check('script_bytecode_cache_absent',not(root/'scripts/__pycache__').exists())
        protected=root.parent/'formalization-workbench'
        started=datetime(2026,9,16,12,41,39,tzinfo=timezone.utc).timestamp()
        changed=[str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=started]
        check('protected_workbench_mtime_changed_count_zero',not changed,changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot,'outputs')
        own(executed,'outputs')
        check('resume_and_executed_sealer_saved',True)
        report.update(state='complete',completed_at=datetime.now(timezone.utc).isoformat(),current_suite_checks=counts,
            total_successful_current_checks=sum(counts.values()),distinct_files_rehashed=len(cache),
            inherited_failed_attempts_preserved=previous['inherited_failed_attempts_preserved']+len(failed_attempts),
            new_failed_attempts_preserved=failed_attempts,fixture_force_results=rows,
            original_GR_failures_unchanged=True,implementation_checks_not_physics_passes=True)
        save()
        print(json.dumps(dict(state='complete',checks=len(report['checks']),current_checks=sum(counts.values()),
            rehashed_files=len(cache),protected_changed=len(changed),failed_attempts_preserved=report['inherited_failed_attempts_preserved'],
            fixture_failures=failures)),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__=='__main__':
    main()
