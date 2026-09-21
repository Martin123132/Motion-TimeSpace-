import hashlib
import json
import re
import traceback
from datetime import datetime, timezone
from pathlib import Path
from navier_stokes_source_audit_20260908 import limit_process


def main():
    limit_process()
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    destination = intake/'annular-relaxed-branch-final-integrity.json'
    snapshot = intake/'annular-relaxed-branch-resume-snapshot.md'
    executed = intake/'annular-relaxed-branch-executed-sealer.py'
    if any(path.exists() for path in [destination, snapshot, executed]):
        raise FileExistsError('Executed evidence and seals are immutable.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, full_GR_limit_proven=False,
                  valid_for_physics_claim=False, complete_parent_source_action_derived=False,
                  relaxed_action_adopted_as_parent=False, relaxed_action_improves_tested_final_force=False,
                  github_action=False, subagents_used=False,
                  protected_scan_scope='mtime since 2026-09-16T10:26:04Z, not a pre-turn full hash baseline')
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

    def own(path, table='inputs'):
        report[table][str(path.resolve().relative_to(root))] = digest(path)

    def save():
        destination.write_text(json.dumps(report, indent=2, allow_nan=False)+'\n', encoding='utf-8')

    def check(name, passed, detail=None):
        report['checks'].append(dict(name=name, passed=bool(passed), detail=detail))
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def inherit(status):
        for table in ['inputs', 'outputs']:
            for name, expected in status[table].items():
                path = (root/name).resolve()
                normalized = str(path.relative_to(root))
                if not path.is_file() or digest(path)!=expected:
                    raise RuntimeError('Missing or altered immutable evidence: '+name)
                if normalized in report['inputs'] and report['inputs'][normalized]!=expected:
                    raise RuntimeError('Conflicting immutable digest: '+name)
                report['inputs'][normalized] = expected

    save()
    try:
        previous_path = intake/'annular-boundary-response-final-integrity.json'
        previous = json.loads(previous_path.read_text())
        check('previous_checkpoint_complete', previous['state']=='complete' and all(row['passed'] for row in previous['checks']))
        inherit(previous)
        own(previous_path)
        statuses, counts = {}, {}
        for label, folder, count in [
            ('qualification', 'annular-relaxed-branch-qualification-attempt01', 120),
            ('smoke', 'annular-relaxed-branch-smoke-attempt01', 27),
            ('refinement', 'annular-relaxed-branch-refinement257-attempt01', 16),
            ('precision', 'annular-relaxed-precision-attempt01', 19),
            ('response', 'annular-relaxed-force-change-attempt01', 21)]:
            path = intake/folder/'status.json'
            status = json.loads(path.read_text())
            json.dumps(status, allow_nan=False)
            check(label+'_complete', status['state']=='complete' and len(status['checks'])==count and all(row['passed'] for row in status['checks']))
            check(label+'_broad_claims_false', not status['full_GR_limit_proven'] and not status['valid_for_physics_claim'] and not status['complete_parent_source_action_derived'])
            inherit(status)
            own(path)
            statuses[label], counts[label] = status, count
        qualification = statuses['qualification']
        check('actual_and_auxiliary_traces_distinct_and_unconstrained', all(row['no_physical_trace_constraint_imposed'] for row in qualification['cases'])
              and any(abs(row['auxiliary_trace']-row['actual_derivative_jump'])>1e-6 for row in qualification['cases'] if row['branch']=='relaxed_MTS')
              and not qualification['derivative_trace_overwritten'])
        check('original_kinetic_source_momentum_and_rows_retained', qualification['source_field_momentum_retained']
              and qualification['original_sampling_rows_retained'] and qualification['no_new_fitted_parameter'])
        check('legacy_helpers_fail_closed', qualification['legacy_gradient_Gram_helpers_rejected'])
        expected_gates = dict(field=.005, source=5e-7, velocity=2e-5, clock=2e-7, force_absolute=2e-7, force_relative=.02)
        for label in ['smoke', 'refinement']:
            status = statuses[label]
            check(label+'_original_data_gates_and_scope', status['prespecified_gates']==expected_gates and status['original_profile_and_final_time_unchanged']
                  and status['candidate_not_original_action'] and status['kinetic_source_current_retained'] and not status['energy_projection']
                  and not status['dynamic_convergence_from_unrelaxed_action_proven'] and status['source_splits']==1)
        results = statuses['smoke']['cases']+statuses['refinement']['cases']
        check('complete_paired_resolution_matrix', {(row['base_count'], row['branch']) for row in results}
              =={(count, branch) for count in [65, 129, 257] for branch in ['reference', 'relaxed_MTS']})
        check('force_flags_recomputed_across_all_oracles', all(set(row['force_errors'])=={'384','512','768'}
              and row['final_force_passes_all_references']==all(row['final_force_flags_by_reference'].values())
              and row['sampled_force_passes_all_references']==all(row['sampled_force_flags_by_reference'].values())
              and all(row['final_force_flags_by_reference'][degree]==(errors[-1]<2e-7 and errors[-1]/abs(row['reference_final_forces'][degree])<.02)
                      and row['sampled_force_flags_by_reference'][degree]==(max(errors)<2e-7) for degree, errors in row['force_errors'].items()) for row in results))
        check('field_source_clock_flags_recomputed', all(row['strict_waveform_gate']==(row['maximum_field_error']<.005)
              and row['strict_source_clock_gate']==(row['maximum_source_error']<5e-7 and row['maximum_velocity_error']<2e-5 and row['maximum_clock_error']<2e-7) for row in results))
        check('all_failed_force_flags_preserved', all(not row['final_force_passes_all_references'] and not row['sampled_force_passes_all_references'] for row in results))
        check('candidate_worse_than_old_MTS_at_each_endpoint', all(row['final_force_absolute_error']>row['old_unrelaxed_final_force_error'] for row in results if row['branch']=='relaxed_MTS'))
        check('reference_reproduction_preserved', all(row['state_difference_from_old_same_mesh']<2e-8 for row in results if row['branch']=='reference'))
        coarse = next(row for row in results if row['base_count']==65 and row['branch']=='relaxed_MTS')
        check('coarse_source_and_velocity_failures_explicit', not coarse['strict_source_clock_gate'] and coarse['maximum_source_error']>5e-7 and coarse['maximum_velocity_error']>2e-5)
        precision = statuses['precision']
        check('tight_controls_not_overclaimed', len(precision['cases'])==2 and all(row['count']==129 and row['duration']==.05
              and row['rtol']==2e-12 and not row['full_duration_temporal_control'] for row in precision['cases'])
              and not precision['whole_duration_temporal_convergence_proven'])
        check('complex_coefficient_warning_explained_and_controlled', len(precision['coefficient_type_controls'])==4
              and all(row['mass_derivative_error']<2e-10 for row in precision['coefficient_type_controls']) and bool(precision['qualification_warning_explained']))
        response = statuses['response']
        check('response_law_not_applied_as_force_correction', not response['force_decomposition_used_as_correction'] and not response['relaxed_model_adopted_as_parent'])
        check('derived_response_and_feedback_add_to_total', all(abs(item['derived_same_state_force_change']+item['trajectory_feedback_force_change']-item['total_force_change'])<2e-11
              for row in response['cases'] for item in row['trajectory']))
        note = root/'DERIVATION-20260916-relaxed-trace-candidate-and-paired-smoke.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json))`', content)
        check('all_cited_local_paths_exist', all((root/name).is_file() for name in cited), cited)
        check('main_note_complete_and_nonclaim_scope', 'REFINEMENT_AND_FORCE_RESPONSE_PENDING' not in content and 'not a full GR limit' in content
              and 'not adopted as a force cure' in content and 'fails the source-position and velocity gates' in content)
        own(note)
        modules = ['annular_relaxed_trace_action_20260916.py', 'verify_annular_relaxed_branch_20260916.py',
                   'run_annular_relaxed_branch_smoke_20260916.py', 'run_annular_relaxed_branch_refinement257_20260916.py',
                   'verify_annular_relaxed_precision_20260916.py', 'derive_annular_relaxed_force_change_20260916.py',
                   'seal_annular_relaxed_branch_20260916.py']
        for name in modules:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('modules_compile_without_bytecode', True, modules)
        check('script_bytecode_cache_absent', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        started = datetime(2026, 9, 16, 10, 26, 4, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=started]
        check('protected_workbench_mtime_changed_count_zero', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        check('resume_and_executed_sealer_preserved', True)
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(), current_suite_checks=counts,
                      total_successful_current_checks=sum(counts.values()), distinct_files_rehashed=len(cache),
                      inherited_failed_attempts_preserved=previous['inherited_failed_attempts_preserved'],
                      new_failed_attempts=0, candidate_test_results=results, implementation_checks_not_physics_passes=True)
        save()
        print(json.dumps(dict(state='complete', checks=len(report['checks']), current_checks=sum(counts.values()),
                              rehashed_files=len(cache), protected_changed=len(changed))), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__=='__main__':
    main()
