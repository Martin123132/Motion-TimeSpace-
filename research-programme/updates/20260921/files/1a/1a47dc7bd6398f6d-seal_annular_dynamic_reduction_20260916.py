from derive_annular_source_gravity_20260914 import EvidenceRun
import hashlib
import json
import re
import traceback
from datetime import datetime, timezone
from pathlib import Path
import numpy as np


def main():
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    destination = intake/'annular-dynamic-reduction-final-integrity.json'
    snapshot = intake/'annular-dynamic-reduction-resume-snapshot.md'
    executed = intake/'annular-dynamic-reduction-executed-sealer.py'
    if any(path.exists() for path in [destination, snapshot, executed]):
        raise FileExistsError('Existing seals and evidence are immutable.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, full_GR_limit_proven=False,
        valid_for_physics_claim=False, freely_moving_source_bound_certified=False,
        frozen_analytic_bound_evaluated_not_interval_certified=True, github_action=False, subagents_used=False,
        protected_scan_scope='mtime since 2026-09-16T11:47:52Z; not a pre-turn full hash baseline')
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
                    raise RuntimeError('Conflicting source digest: '+name)
                report['inputs'][normalized] = expected

    save()
    try:
        previous_path = intake/'annular-relaxed-branch-final-integrity.json'
        previous = json.loads(previous_path.read_text())
        check('previous_checkpoint_complete', previous['state']=='complete' and all(row['passed'] for row in previous['checks']))
        inherit(previous)
        own(previous_path)
        statuses, counts = {}, {}
        for label, folder, count, cases in [
            ('dynamic', 'annular-dynamic-reduction-bound-attempt01', 217, 24),
            ('prepared', 'annular-prepared-data-criterion-attempt01', 36, 3),
            ('local_modes', 'annular-retained-boundary-modes-attempt02', 83, 16),
            ('invariant', 'annular-invariant-modal-force-bound-attempt01', 26, 2),
            ('force_aware', 'annular-force-aware-modes-attempt01', 7, 2)]:
            path = intake/folder/'status.json'
            status = json.loads(path.read_text())
            json.dumps(status, allow_nan=False)
            check(label+'_complete', status['state']=='complete' and len(status['checks'])==count
                and all(row['passed'] for row in status['checks']) and len(status['cases'])==cases)
            check(label+'_broad_claims_false', not status['full_GR_limit_proven'] and not status['valid_for_physics_claim']
                and not status['complete_parent_source_action_derived'])
            inherit(status)
            own(path)
            statuses[label], counts[label] = status, count
        dynamic = statuses['dynamic']
        check('paired_original_and_prepared_matrix_complete', {(row['branch'],row['count'],row['source_splits'],row['prepared_control']) for row in dynamic['cases']}
            =={(branch,count,splits,prepared) for branch in ['reference','MTS'] for count,splits in [(33,2),(65,2),(65,4),(65,8),(129,4),(129,8)] for prepared in [False,True]})
        check('static_reduction_failures_not_upgraded', all(not row['sampled_frozen_reduction_error_below_budget']
            and not row['frozen_reduction_certified_below_budget'] and not row['freely_moving_source'] for row in dynamic['cases']))
        check('original_data_and_action_not_changed', dynamic['unchanged_original_physical_runs'] and dynamic['original_Gram_rows_retained']
            and not dynamic['damping_added'] and not dynamic['prepared_data_adopted_for_physics']
            and not dynamic['static_boundary_replacement_adopted'] and dynamic['old_GR_force_gates_unchanged'])
        local = statuses['local_modes']
        check('only_full_dimension_local_mode_controls_pass_budget', all(row['sampled_reduction_error_below_budget']==row['is_full_dimension_coordinate_control'] for row in local['cases']))
        check('local_mode_control_is_not_physics_pass', not local['physical_GR_force_gate_retested'] and local['full_mode_test_is_identity_control_not_a_reduction'])
        invariant = statuses['invariant']
        check('ascending_frequency_result_recorded_without_overclaim', {row['branch']:row['first_cutoff_numerically_below_budget'] for row in invariant['cases']}=={'reference':275,'MTS':286}
            and all(not row['interval_eigenpair_roundoff_certified'] and row['reference_is_original_full_finite_action_not_GR_oracle'] for row in invariant['cases']))
        selected = statuses['force_aware']
        selection_rows = []
        for row in selected['cases']:
            path = intake/'annular-invariant-modal-force-bound-attempt01'/(row['branch']+'-modal-budget.npz')
            with np.load(path) as saved:
                matrix = saved['force_contribution_envelope']
                matrix = np.maximum(matrix,matrix.T)
                retained, removed = row['retained_indices'],row['removed_indices']
                bound = float(np.sum(matrix[np.ix_(retained,removed)])+np.sum(matrix[np.ix_(removed,removed)])/2)
            check(row['branch']+'_selection_partition_complete', len(set(retained+removed))==286 and sorted(retained+removed)==list(range(286))
                and len(retained)==row['retained_mode_count'] and len(removed)==row['removed_mode_count'])
            check(row['branch']+'_envelope_independently_recomputed', abs(bound-row['uniform_source_load_tail_bound'])<2e-15
                and row['maximum_sampled_source_load_error']<=bound and bound<=2e-7 and row['source_load_budget']==2e-7)
            check(row['branch']+'_nontrivial_selection_not_full_identity', row['nontrivial_reduction'] and len(removed)>0
                and not row['interval_roundoff_certified'] and not row['globally_minimal_mode_count_claimed'])
            selection_rows.append(dict(branch=row['branch'], retained=len(retained), omitted=len(removed),
                envelope=bound, sampled_error=row['maximum_sampled_source_load_error'], fastest_retained=row['highest_frequency_mode_retained']))
        check('fast_MTS_mode_is_retained', next(row for row in selection_rows if row['branch']=='MTS')['fastest_retained'])
        check('selection_scope_not_moving_or_GR', not selected['moving_source_certified'] and not selected['GR_oracle_comparison']
            and not selected['original_action_changed'] and not selected['damping_added'])
        prepared = statuses['prepared']
        check('moving_states_and_scalar_fixture_scopes_separate', sum(len(row['saved_states']) for row in prepared['cases'])==27
            and all(not item['full_trajectory_certified'] for row in prepared['cases'] for item in row['saved_states'])
            and all(not row['is_physical_source_force'] and row['scalar_trial_layer_not_full_coupled_solution'] for row in prepared['layer_controls']))
        failed_path = intake/'annular-retained-boundary-modes-attempt01/status.json'
        failed = json.loads(failed_path.read_text())
        check('failed_first_enrichment_attempt_preserved', failed['state']=='failed'
            and 'reference-all_twenty_eight_positive_variational_reduction' in failed['error'] and len(failed['cases'])==7)
        inherit(failed)
        own(failed_path)
        note = root/'DERIVATION-20260916-dynamic-boundary-reduction-and-force-aware-memory.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json))`', content)
        check('all_cited_paths_exist', all((root/name).is_file() for name in cited), cited)
        check('note_nonclaim_limits_and_next_connection_explicit', 'not a full GR limit' in content
            and 'not certified interval arithmetic' in content and 'not implemented or numerically qualified' in content
            and 'does not establish a large speedup' in content and 'not369 physics validations' in content)
        own(note)
        modules = ['annular_dynamic_reduction_bound_20260916.py','verify_annular_dynamic_reduction_20260916.py',
            'derive_annular_prepared_data_20260916.py','verify_annular_retained_boundary_modes_20260916.py',
            'verify_annular_retained_boundary_modes_20260916_v2.py','verify_annular_invariant_modal_force_bound_20260916.py',
            'verify_annular_force_aware_modes_20260916.py','seal_annular_dynamic_reduction_20260916.py']
        for name in modules:
            path = root/'scripts'/name
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('all_new_modules_compile_without_bytecode', True, modules)
        check('script_bytecode_cache_absent', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        started = datetime(2026,9,16,11,47,52,tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=started]
        check('protected_workbench_mtime_changed_count_zero', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot,'outputs')
        own(executed,'outputs')
        check('resume_and_executed_sealer_saved', True)
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(), current_suite_checks=counts,
            total_successful_current_checks=sum(counts.values()), distinct_files_rehashed=len(cache),
            inherited_failed_attempts_preserved=previous['inherited_failed_attempts_preserved']+1,
            new_failed_attempts_preserved=1, force_aware_results=selection_rows,
            original_moving_GR_failures_unchanged=True, implementation_checks_not_physics_passes=True)
        save()
        print(json.dumps(dict(state='complete', checks=len(report['checks']), current_checks=sum(counts.values()),
            rehashed_files=len(cache), protected_changed=len(changed), results=selection_rows)),flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__=='__main__':
    main()
