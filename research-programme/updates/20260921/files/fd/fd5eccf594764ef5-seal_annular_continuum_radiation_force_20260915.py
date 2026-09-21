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
    destination = intake/'annular-continuum-radiation-force-final-integrity.json'
    snapshot = intake/'annular-continuum-radiation-force-resume-snapshot.md'
    executed = intake/'annular-continuum-radiation-force-executed-sealer.py'
    if any(path.exists() for path in [destination, snapshot, executed]):
        raise FileExistsError('Preserve every previous executed seal and snapshot.')
    report = dict(state='running', checks=[], inputs={}, outputs={},
                  continuum_timelike_pressure_force_derived=True,
                  conditional_live_proper_acceleration_law_derived=True,
                  mesh_small_momentum_finite_derivative_cancellation_derived=True,
                  original_dense_sparse_equivalence_tested=True,
                  independent_prescribed_GR_characteristic_benchmark_completed=True,
                  live_backreaction_continuum_comparison_completed=False,
                  both_underresolved_failures_retained=True,
                  full_GR_limit_proven=False, valid_for_physics_claim=False,
                  unique_parent_material_law_proven=False,
                  uniform_evolving_continuum_limit_proven=False,
                  source_cell_crossing_transfer_derived=False,
                  github_action=False, subagents_used=False,
                  resource_policy='At most two own BelowNormal single-core numerical workers; all numerical jobs finished before sealing.',
                  protected_scan_scope='mtime since2026-09-15T10:23:04Z, not a pre-turn content-hash baseline.')
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
                    raise RuntimeError('Missing or changed executed evidence: '+name)
                if name in report['inputs'] and report['inputs'][name] != expected:
                    raise RuntimeError('Conflicting evidence hash: '+name)
                report['inputs'][name] = expected

    save()
    try:
        previous_path = intake/'annular-repaired-live-final-integrity.json'
        previous = json.loads(previous_path.read_text())
        check('previous_live_action_seal_complete', previous['state'] == 'complete' and all(row['passed'] for row in previous['checks']))
        inherit(previous)
        own(previous_path)
        statuses, counts = {}, {}
        for label, folder, count in [
                ('force_algebra', 'annular-continuum-radiation-force-algebra-attempt01', 11),
                ('sparse_equivalence', 'annular-sparse-repaired-cut-equivalence-attempt01', 18),
                ('manufactured_force', 'annular-continuum-moving-force-limit-attempt01', 6),
                ('momentum_cancellation', 'annular-moving-momentum-cancellation-attempt01', 5),
                ('characteristic_work', 'annular-characteristic-work-balance-attempt01', 7),
                ('refined_oracle', 'annular-two-sided-GR-oracle-attempt02', 4),
                ('refined_benchmark', 'annular-repaired-GR-force-benchmark-attempt02', 13)]:
            path = intake/folder/'status.json'
            status = json.loads(path.read_text())
            json.dumps(status, allow_nan=False)
            check(label+'_complete_finite_results', status['state'] == 'complete' and len(status['checks']) == count and all(row['passed'] for row in status['checks']))
            check(label+'_broad_claims_false', not status['full_GR_limit_proven'] and not status['valid_for_physics_claim']
                  and not status['complete_parent_source_action_derived'])
            inherit(status)
            own(path)
            statuses[label], counts[label] = status, count
        for folder, expected_gate in [
                ('annular-two-sided-GR-oracle-attempt01', 'independent_continuum_fields_refine'),
                ('annular-repaired-GR-force-benchmark-attempt01', 'reference_physical_waveform_accuracy')]:
            path = intake/folder/'status.json'
            status = json.loads(path.read_text())
            json.dumps(status, allow_nan=False)
            check(folder+'_failure_preserved', status['state'] == 'failed' and status['checks'][-1]['name'] == expected_gate and not status['checks'][-1]['passed'])
            inherit(status)
            own(path)
        check('finite_source_momentum_derivative_not_dropped', statuses['momentum_cancellation']['field_source_momentum_O_h_but_time_derivative_not_O_h_generically']
              and statuses['refined_benchmark']['boundary_field_momentum_rate_retained'])
        check('no_force_fit_factor_deletion_or_projection', statuses['refined_benchmark']['continuum_force_not_fitted']
              and statuses['refined_benchmark']['all_Gram_rows_retained'] and statuses['refined_benchmark']['no_energy_or_position_projection'])
        check('resolution_refinements_preserve_initial_data_equations_gates', statuses['refined_oracle']['original_gates_unchanged']
              and statuses['refined_benchmark']['equations_initial_data_and_gates_unchanged'])
        check('prescribed_background_not_mislabeled_live_oracle', not statuses['refined_oracle']['live_backreaction_oracle_completed']
              and not statuses['refined_benchmark']['live_backreaction_continuum_comparison_completed'])
        check('both_final_branches_present', {row['branch'] for row in statuses['refined_benchmark']['cases']} == {'reference', 'MTS'})
        note = root/'DERIVATION-20260915-continuum-radiation-force-and-independent-GR-benchmark.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json))`', content)
        check('all_cited_local_paths_exist', all((root/name).is_file() for name in cited), cited)
        check('note_has_no_pending_result_placeholder', 'RESULTS_PENDING' not in content)
        own(note)
        scripts = [root/name for name in cited if name.startswith('scripts/') and name.endswith('.py')]
        scripts.append(Path(__file__))
        for path in scripts:
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('thirteen_new_modules_compile_without_bytecode', len(scripts) == 13)
        check('script_bytecode_cache_absent', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        started = datetime(2026, 9, 15, 10, 23, 4, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= started]
        check('protected_workbench_mtime_changed_count_zero', len(changed) == 0, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        check('immutable_resume_and_sealer_snapshot_saved', snapshot.is_file() and executed.is_file())
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(),
                      successful_current_suite_checks=counts, total_successful_current_checks=sum(counts.values()),
                      failed_underresolved_suite_count=2, distinct_files_rehashed=len(cache),
                      next_target='Independent finite-width common-live-geometry continuum characteristic/source solver using the derived radiation force; compare to repaired live canonical evolution at identical width/preparation.')
        save()
        print(json.dumps(dict(state='complete', checks=len(report['checks']), current_checks=sum(counts.values()),
                              distinct_files_rehashed=len(cache), protected_changed=len(changed))), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
