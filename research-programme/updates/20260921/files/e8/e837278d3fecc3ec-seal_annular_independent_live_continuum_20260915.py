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
    destination = intake/'annular-independent-live-continuum-final-integrity.json'
    snapshot = intake/'annular-independent-live-continuum-resume-snapshot.md'
    executed = intake/'annular-independent-live-continuum-executed-sealer.py'
    if any(path.exists() for path in [destination, snapshot, executed]):
        raise FileExistsError('Do not replace any previous executed seal or snapshot.')
    report = dict(state='running', checks=[], inputs={}, outputs={},
                  independent_common_live_geometry_continuum_evolved=True,
                  conditional_scaled_characteristics_and_canonical_radial_solve_derived=True,
                  conditional_continuum_interior_angular_completion_derived=True,
                  continuum_benchmark_not_observational_evidence=True,
                  full_GR_limit_proven=False, valid_for_physics_claim=False,
                  parent_material_action_uniquely_selected=False,
                  uniform_all_mesh_continuum_theorem_proven=False,
                  github_action=False, subagents_used=False,
                  resource_policy='At most two own BelowNormal one-core numerical workers; all own numerical jobs finished before sealing.',
                  protected_scan_scope='mtime since2026-09-15T11:27:24Z, not a pre-turn hash baseline.')
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
                if not path.is_file() or digest(path) != expected:
                    raise RuntimeError('Missing or altered immutable evidence: '+name)
                if name in report['inputs'] and report['inputs'][name] != expected:
                    raise RuntimeError('Conflicting immutable digest: '+name)
                report['inputs'][name] = expected

    save()
    try:
        previous_path = intake/'annular-continuum-radiation-force-final-integrity.json'
        previous = json.loads(previous_path.read_text())
        check('previous_continuum_force_checkpoint_complete', previous['state'] == 'complete' and all(row['passed'] for row in previous['checks']))
        inherit(previous)
        own(previous_path)
        statuses, counts = {}, {}
        for label, folder, count in [
                ('algebra', 'annular-live-scaled-characteristics-algebra-attempt01', 10),
                ('snapshot', 'annular-live-continuum-snapshot-attempt01', 9),
                ('live_evolution', 'annular-live-continuum-evolution-attempt01', 43),
                ('independent_controls', 'annular-live-oracle-independent-controls-attempt02', 9),
                ('product_defect', 'annular-characteristic-product-defect-attempt01', 3),
                ('angular_closure', 'annular-continuum-angular-closure-attempt01', 8),
                ('factored_equivalence', 'annular-live-continuum-factorization-attempt01', 6),
                ('barycentric_equivalence', 'annular-live-barycentric-equivalence-attempt01', 6),
                ('refined_oracle', 'annular-live-continuum-degree512-attempt01', 10),
                ('paired_comparison', 'annular-repaired-live-continuum-comparison-attempt03', 19)]:
            path = intake/folder/'status.json'
            status = json.loads(path.read_text())
            json.dumps(status, allow_nan=False)
            check(label+'_complete_finite_checks', status['state'] == 'complete' and len(status['checks']) == count
                  and all(row['passed'] for row in status['checks']))
            check(label+'_broad_claims_false', not status['full_GR_limit_proven'] and not status['valid_for_physics_claim']
                  and not status['complete_parent_source_action_derived'])
            inherit(status)
            own(path)
            statuses[label], counts[label] = status, count
        for folder in ['annular-live-continuum-refinement-attempt01', 'annular-live-oracle-independent-controls-attempt01',
                       'annular-live-continuum-refinement-attempt02', 'annular-live-oracle-jump-aware-refinement-attempt01',
                       'annular-repaired-live-continuum-comparison-attempt02']:
            path = intake/folder/'status.json'
            status = json.loads(path.read_text())
            check(folder+'_failed_evidence_preserved', status['state'] == 'failed' and not status['valid_for_physics_claim'])
            inherit(status)
            own(path)
        check('continuum_reference_live_and_refinement_qualified', statuses['refined_oracle']['independent_common_live_geometry_continuum_evolved']
              and statuses['refined_oracle']['sampled_finite_time_continuum_accuracy_qualified'])
        check('jump_comparison_change_explicit_and_gap_not_masked', statuses['refined_oracle']['global_sup_across_displaced_jumps_not_claimed']
              and statuses['refined_oracle']['corrected_norm_does_not_mask_gap']
              and statuses['refined_oracle']['one_sided_absolute_tolerance_unchanged'])
        check('original_preparation_width_and_Gram_factors_retained', statuses['paired_comparison']['same_original_repaired_live_preparation']
              and statuses['paired_comparison']['same_finite_width_and_coupling'] and statuses['paired_comparison']['original_Gram_rows_retained'])
        check('physical_force_retains_moving_field_momentum_rate', statuses['paired_comparison']['moving_field_source_momentum_rate_retained_in_force'])
        check('same_test_both_branches_all_three_grids', {(row['branch'], row['count']) for row in statuses['paired_comparison']['cases']}
              == {(branch, count) for branch in ['reference', 'MTS'] for count in [17, 33, 65]})
        strict = all(row['strict_half_percent_waveform_gate'] for row in statuses['paired_comparison']['cases'] if row['count'] == 65)
        check('strict_waveform_gate_not_replaced_by_trend', statuses['paired_comparison']['strict_half_percent_gate_not_relaxed']
              and statuses['paired_comparison']['strict_live_waveform_accuracy_qualified'] == strict)
        check('coarsest_MTS_velocity_failure_not_hidden_by_finer_passes', statuses['paired_comparison']['coarsest_MTS_source_gate_failed_and_retained']
              and not statuses['paired_comparison']['all_resolutions_source_accuracy_qualified']
              and any(row['branch'] == 'MTS' and row['count'] == 17 and not row['source_and_clock_smoke_pass']
                      for row in statuses['paired_comparison']['cases']))
        check('failed_control_fixed_without_tolerance_change', statuses['independent_controls']['original_gates_unchanged']
              and statuses['product_defect']['finite_collocation_product_rule_not_exact'])
        check('conditional_angular_result_not_promoted_to_global_parent_GR', statuses['angular_closure']['conditional_spherical_interior_angular_completion_derived']
              and statuses['angular_closure']['moving_interface_total_stress_conservation_derived']
              and statuses['angular_closure']['outer_boundary_supports_or_global_completion_not_derived']
              and not statuses['angular_closure']['parent_action_uniquely_selected'])
        note = root/'DERIVATION-20260915-independent-live-continuum-GR-oracle.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json))`', content)
        check('all_cited_local_paths_exist', all((root/name).is_file() for name in cited), cited)
        check('main_note_has_no_pending_results', 'RESULTS_PENDING' not in content)
        check('external_source_and_fetch_limit_disclosed', '10.1088/1674-1137/ad361c' in content and 'timed out' in content)
        own(note)
        scripts = [root/name for name in cited if name.startswith('scripts/') and name.endswith('.py')]
        if Path(__file__) not in scripts:
            scripts.append(Path(__file__))
        for path in scripts:
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('new_modules_compile_without_bytecode', len(scripts) >= 13, len(scripts))
        check('script_bytecode_cache_absent', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        started = datetime(2026, 9, 15, 11, 27, 24, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= started]
        check('protected_workbench_mtime_changed_count_zero', len(changed) == 0, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        check('immutable_resume_and_executed_sealer_saved', snapshot.is_file() and executed.is_file())
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(),
                      successful_current_suite_checks=counts, total_successful_current_checks=sum(counts.values()),
                      distinct_files_rehashed=len(cache), preserved_failed_attempts=5,
                      strict_live_waveform_accuracy_qualified=strict,
                      next_target='Refine the repaired LIVE finite-action waveform and physical force against this independently qualified continuum oracle, retaining positive width and source momentum transport; derive cell-crossing transfer before arbitrary resolution/long time.')
        save()
        print(json.dumps(dict(state='complete', checks=len(report['checks']), current_checks=sum(counts.values()),
                              rehashed_files=len(cache), protected_changed=len(changed))), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
