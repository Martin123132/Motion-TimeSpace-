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
    destination = intake/'annular-quadratic-crossing-final-integrity.json'
    snapshot = intake/'annular-quadratic-crossing-resume-snapshot.md'
    executed = intake/'annular-quadratic-crossing-executed-sealer.py'
    if any(path.exists() for path in [destination, snapshot, executed]):
        raise FileExistsError('Existing seals and executed snapshots are immutable.')
    report = dict(state='running', checks=[], inputs={}, outputs={},
        full_GR_limit_proven=False, valid_for_physics_claim=False, parent_source_action_uniquely_derived=False,
        live_quadratic_geometry_qualified=False, uniform_all_time_force_bound_proven=False,
        github_action=False, subagents_used=False,
        protected_scan_scope='mtime since2026-09-15T21:04:59Z, not a pre-turn hash baseline.')
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
                path.relative_to(root)
                normalized = str(path.relative_to(root))
                if not path.is_file() or digest(path) != expected:
                    raise RuntimeError('Missing or altered immutable evidence: '+name)
                if normalized in report['inputs'] and report['inputs'][normalized] != expected:
                    raise RuntimeError('Conflicting digest: '+name)
                report['inputs'][normalized] = expected

    save()
    try:
        prior_path = intake/'annular-source-fitted-crossing-final-integrity.json'
        previous = json.loads(prior_path.read_text())
        check('previous_checkpoint_complete', previous['state'] == 'complete' and all(row['passed'] for row in previous['checks']))
        inherit(previous)
        own(prior_path)
        statuses, counts = {}, {}
        for label, folder, count in [
            ('linear2049', 'annular-source-fitted-force2049-attempt01', 7),
            ('quadratic_action', 'annular-quadratic-source-fitted-action-attempt01', 47),
            ('quadratic_coarse', 'annular-quadratic-crossing-attempt01', 26),
            ('quadratic_fine', 'annular-quadratic-fine-crossing-attempt01', 14),
            ('initial_error', 'annular-quadratic-initial-error-law-attempt01', 3),
            ('oracle768', 'annular-crossing-oracle768-attempt01', 12),
            ('quadratic_precision', 'annular-quadratic-crossing-precision-attempt02', 49),
            ('force_error_budget', 'annular-crossing-force-error-budget-attempt01', 32)]:
            path = intake/folder/'status.json'
            status = json.loads(path.read_text())
            json.dumps(status, allow_nan=False)
            check(label+'_complete', status['state'] == 'complete' and len(status['checks']) == count and all(row['passed'] for row in status['checks']))
            check(label+'_broad_claims_false', not status['full_GR_limit_proven'] and not status['valid_for_physics_claim'] and not status['complete_parent_source_action_derived'])
            inherit(status)
            own(path)
            statuses[label], counts[label] = status, count
        failed_path = intake/'annular-quadratic-crossing-precision-attempt01/status.json'
        failed = json.loads(failed_path.read_text())
        check('underresolved_coarse_quadrature_attempt_preserved', failed['state'] == 'failed'
            and any(not row['passed'] and row['name'] == 'reference33_comparison_quadrature_agrees' for row in failed['checks']))
        inherit(failed)
        own(failed_path)
        quadratic = statuses['quadratic_coarse']['cases']+statuses['quadratic_fine']['cases']
        check('all_quadratic_counts_and_paired_branches_preserved', {(row['base_count'], row['branch']) for row in quadratic}
            == {(count, branch) for count in [33,65,129,257,513,1025] for branch in ['reference','MTS']})
        check('quadratic_dof_count_not_misrepresented', all(row['scalar_dofs'] == 2*row['base_count'] for row in quadratic))
        gates = dict(field=.005, source=5e-7, velocity=2e-5, clock=2e-7, force_absolute=2e-7, force_relative=.02)
        check('quadratic_data_and_gates_unchanged', all(statuses[label]['prespecified_accuracy_gates'] == gates
            and statuses[label]['original_crossing_data_and_gates_unchanged'] for label in ['quadratic_coarse','quadratic_fine']))
        check('nesting_Gram_and_full_source_momentum_retained', all(statuses[label]['all_original_vertex_Gram_rows_retained']
            and statuses[label]['source_field_momentum_derivative_retained'] and statuses[label]['original_linear_subspace_exactly_preserved']
            and statuses[label]['no_fitted_coefficient_added'] and not statuses[label]['energy_projection'] for label in ['quadratic_coarse','quadratic_fine']))
        check('genuine_base_vertex_crossings_and_positive_maps', all(row['original_base_vertices_crossed'] and row['minimum_jacobian'] > .9 for row in quadratic))
        linear = statuses['linear2049']['cases']
        check('linear_refinement_paired_and_preserved', {(row['count'], row['branch']) for row in linear} == {(2049, branch) for branch in ['reference','MTS']})
        check('force_and_field_flags_independently_recomputed', all(row['strict_force_gate'] == (row['final_force_absolute_error'] < 2e-7 and row['final_force_relative_error'] < .02)
            and row['strict_waveform_gate'] == (row['maximum_field_error'] < .005) for row in quadratic+linear))
        check('source_clock_flags_independently_recomputed', all(row['strict_source_clock_gate'] == (row['maximum_source_error'] < 5e-7
            and row['maximum_velocity_error'] < 2e-5 and row['maximum_clock_error'] < 2e-7) for row in quadratic+linear))
        check('coarse_and_old_failures_remain_visible', any(not row['strict_force_gate'] for row in quadratic)
            and previous['inherited_failed_attempts_preserved'] == 5)
        precision = statuses['quadratic_precision']['cases']
        lookup = {(row['base_count'], row['branch']): row for row in quadratic}
        check('independent_precision_covers_every_case', len(precision) == len(quadratic)
            and {(row['base_count'], row['branch']) for row in precision} == set(lookup))
        force768 = statuses['oracle768']['final_force']
        oracle_path = intake/'annular-source-fitted-fine-crossing-attempt01/status.json'
        own(oracle_path)
        check('precision_original_flags_preserved', all(row['original_final_force_gate'] == lookup[(row['base_count'],row['branch'])]['strict_force_gate']
            and row['original_field_gate'] == lookup[(row['base_count'],row['branch'])]['strict_waveform_gate'] for row in precision))
        check('refined_field_quadrature_and_flags_checked', all(row['quadrature16_24_maximum_difference'] < 2e-8
            and row['recomputed_waveform_gate'] == (row['recomputed_maximum_field_error'] < .005)
            and row['recomputed_waveform_gate'] == row['original_field_gate'] for row in precision))
        check('sampled_force_and_impulse_scope_explicit', all(row['stricter_nine_time_absolute_force_gate'] == (max(row['sampled_force_errors512']) < 2e-7)
            and row['impulse_computed_from_mechanical_momentum_not_nine_point_force_quadrature'] for row in precision)
            and not statuses['quadratic_precision']['uniform_all_time_force_bound_proven'])
        check('three_reference_resolutions_checked', all(row['checked_oracle_degrees'] == [512,384,768]
            and len(row['final_force_errors_checked_oracles']) == 3 for row in precision))
        check('extra_oracle_errors_recomputed', all(abs(row['final_force_errors_checked_oracles'][2]
            - abs(lookup[(row['base_count'],row['branch'])]['final_force']-force768)) < 2e-12 for row in precision))
        check('all_reference_force_flags_recomputed', all(row['final_force_gate_passes_all_checked_oracles'] == all(error < 2e-7
            and error/abs(force) < .02 for error, force in zip(row['final_force_errors_checked_oracles'],row['final_reference_forces'])) for row in precision))
        linear_precision = statuses['quadratic_precision']['linear_cases']
        linear_lookup = {(row['count'],row['branch']): row for row in linear}
        check('linear_both_branches_independently_checked_against_three_oracles', len(linear_precision) == 2 and all(row['checked_oracle_degrees'] == [512,384,768]
            and row['original_final_force_gate'] == linear_lookup[(row['count'],row['branch'])]['strict_force_gate'] for row in linear_precision))
        check('linear_extra_oracle_flags_recomputed', all(row['final_force_gate_passes_all_checked_oracles'] == all(error < 2e-7
            and error/abs(force) < .02 for error, force in zip(row['final_force_errors_checked_oracles'],row['final_reference_forces']))
            and abs(row['final_force_errors_checked_oracles'][2]-abs(linear_lookup[(row['count'],row['branch'])]['final_force']-force768)) < 2e-12 for row in linear_precision))
        check('fixed_background_not_live_gravity', all(not statuses[label]['live_quadratic_geometry_qualified']
            for label in ['quadratic_coarse','quadratic_fine','quadratic_precision','oracle768']))
        budget = statuses['force_error_budget']
        check('force_error_budget_covers_every_new_case', {(row['degree'],row['count'],row['branch']) for row in budget['cases']}
            == {(2,row['base_count'],row['branch']) for row in quadratic} | {(1,row['count'],row['branch']) for row in linear})
        check('force_error_budget_retains_terms_and_correct_scope', budget['all_force_terms_retained'] and budget['no_fitted_coefficient_added']
            and budget['kinematic_counterexample_not_claimed_as_on_shell_evolution'] and not budget['uniform_all_time_force_bound_proven']
            and not budget['live_quadratic_geometry_qualified'])
        check('triangle_envelope_flags_recomputed', all(item['triangle_envelope_below_absolute_gate'] == (item['observed_triangle_envelope'] < 2e-7)
            for row in budget['cases'] for item in row['budgets']))
        note = root/'DERIVATION-20260915-nested-quadratic-action-and-crossing-force-refinement.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json))`', content)
        check('all_cited_local_paths_exist', all((root/name).is_file() for name in cited), cited)
        check('main_note_complete_and_limitations_explicit', 'RESULTS_PENDING' not in content and 'not a full GR limit' in content
            and 'https://defelement.org/elements/examples/interval-lagrange-gll-2.html' in content)
        own(note)
        modules = ['refine_annular_source_fitted_force_20260915.py','annular_quadratic_source_fitted_action_20260915.py',
            'verify_annular_quadratic_source_fitted_action_20260915.py','run_annular_quadratic_crossing_20260915.py',
            'derive_annular_quadratic_initial_error_20260915.py','verify_annular_crossing_oracle768_20260915.py',
            'verify_annular_quadratic_crossing_precision_20260915.py','verify_annular_quadratic_crossing_precision_20260915_v2.py',
            'derive_annular_crossing_force_error_budget_20260915.py',
            'seal_annular_quadratic_crossing_20260915.py']
        for name in modules:
            path = root/'scripts'/name
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('new_modules_compile_without_bytecode', True, modules)
        check('script_bytecode_cache_absent', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        started = datetime(2026,9,15,21,4,59,tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= started]
        check('protected_workbench_mtime_changed_count_zero', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot,'outputs')
        own(executed,'outputs')
        check('resume_snapshot_and_executed_sealer_saved', True)
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(),
            current_suite_checks=counts, total_successful_current_checks=sum(counts.values()),
            distinct_files_rehashed=len(cache), inherited_failed_attempts_preserved=6,
            linear_refinement=linear, quadratic_results=quadratic, precision_results=precision, linear_precision_results=linear_precision,
            force_error_budgets=budget['cases'], paired_finest_quadratic_all_time_force_pass=False,
            implementation_checks_not_all_physical_accuracy_passes=True)
        save()
        print(json.dumps(dict(state='complete', checks=len(report['checks']), current_checks=sum(counts.values()),
            rehashed_files=len(cache), protected_changed=len(changed))),flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
