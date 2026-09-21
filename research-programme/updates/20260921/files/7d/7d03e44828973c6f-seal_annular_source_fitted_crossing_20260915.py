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
    destination = intake/'annular-source-fitted-crossing-final-integrity.json'
    snapshot = intake/'annular-source-fitted-crossing-resume-snapshot.md'
    executed = intake/'annular-source-fitted-crossing-executed-sealer.py'
    if any(path.exists() for path in [destination, snapshot, executed]):
        raise FileExistsError('Existing seals and executed snapshots are immutable.')
    report = dict(state='running', checks=[], inputs={}, outputs={},
        full_GR_limit_proven=False, valid_for_physics_claim=False, parent_source_action_uniquely_derived=False,
        live_source_fitted_geometry_qualified=False, github_action=False, subagents_used=False,
        protected_scan_scope='mtime since2026-09-15T17:19:05Z, not a pre-turn hash baseline.')
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
        prior_path = intake/'annular-sparse-live-resolution-final-integrity.json'
        previous = json.loads(prior_path.read_text())
        check('previous_checkpoint_complete', previous['state'] == 'complete' and all(row['passed'] for row in previous['checks']))
        inherit(previous)
        own(prior_path)
        statuses, counts = {}, {}
        for label, folder, count in [
            ('nearby_live_phase', 'annular-sparse-live-nearby-fine-phase-attempt01', 26),
            ('source_fitted_action', 'annular-source-fitted-action-qualification-attempt01', 42),
            ('source_fitted_pullback', 'annular-source-fitted-live-pullback-attempt01', 11),
            ('crossing_coarse', 'annular-source-fitted-crossing-attempt01', 31),
            ('crossing_fine', 'annular-source-fitted-fine-crossing-attempt01', 31),
            ('crossing_precision', 'annular-source-fitted-crossing-precision-attempt01', 24)]:
            path = intake/folder/'status.json'
            status = json.loads(path.read_text())
            json.dumps(status, allow_nan=False)
            check(label+'_complete', status['state'] == 'complete' and len(status['checks']) == count and all(row['passed'] for row in status['checks']))
            check(label+'_broad_claims_false', not status['full_GR_limit_proven'] and not status['valid_for_physics_claim'] and not status['complete_parent_source_action_derived'])
            inherit(status)
            own(path)
            statuses[label], counts[label] = status, count
        phase = statuses['nearby_live_phase']
        baseline_path = intake/'annular-sparse-live-fine-refinement-attempt01/status.json'
        baseline = json.loads(baseline_path.read_text())
        own(baseline_path)
        check('both_prespecified_live_counts_and_branches_present', {(row['count'], row['branch']) for row in phase['cases']}
              == {(count, branch) for count in [1031, 1037] for branch in ['reference', 'MTS']})
        check('live_data_and_all_gates_unchanged', phase['prespecified_accuracy_gates'] == baseline['prespecified_accuracy_gates']
              and phase['same_original_preparation_width_domain_and_duration'] and phase['all_Gram_factors_retained'] and not phase['energy_projection'])
        check('live_force_gate_flags_recomputed', all(row['strict_force_gate'] == (row['force_absolute_error'] < 2e-7 and row['force_relative_error'] < .02) for row in phase['cases']))
        check('live_field_and_source_gate_flags_recomputed', all(row['strict_half_percent_waveform_gate'] == (row['maximum_field_error'] < .005)
            and row['source_clock_gate'] == (row['maximum_source_error'] < 5e-7 and row['maximum_velocity_error'] < 2e-5 and row['maximum_clock_error'] < 2e-7) for row in phase['cases']))
        check('old_live_failures_still_present', any(not row['strict_force_gate'] for row in baseline['cases'])
              and previous['inherited_failed_attempts_preserved'] == 5)
        check('coarse_crossing_oracle_underresolution_not_deleted', not statuses['crossing_coarse']['oracle_resolution']['force_resolution_pass']
              and statuses['crossing_precision']['old_underresolved_oracle_preserved'])
        crossing_cases = [row for status in [statuses['crossing_coarse'], statuses['crossing_fine']] for row in status['cases'] if row['kind'] == 'source_fitted']
        check('all_crossing_branches_and_counts_preserved', {(row['count'], row['branch']) for row in crossing_cases}
              == {(count, branch) for count in [33,65,129,257,513,1025] for branch in ['reference','MTS']})
        check('real_crossings_and_positive_maps', all(row['old_grid_nodes_crossed'] and row['minimum_jacobian'] > .9 for row in crossing_cases))
        check('crossing_accuracy_flags_not_energy_flags', all(row['strict_force_gate'] == (row['final_force_absolute_error'] < 2e-7 and row['final_force_relative_error'] < .02)
              and row['strict_waveform_gate'] == (row['maximum_field_error'] < .005) for row in crossing_cases)
              and any(not row['strict_force_gate'] for row in crossing_cases))
        check('full_transport_retained_without_projection', all(status['all_Gram_rows_retained'] and status['source_field_momentum_derivative_retained']
              and not status['energy_projection'] for status in [statuses['crossing_coarse'], statuses['crossing_fine']]))
        check('fixed_background_not_misrepresented_as_live_crossing', all(not statuses[label]['live_source_fitted_geometry_qualified']
              for label in ['source_fitted_action','source_fitted_pullback','crossing_coarse','crossing_fine','crossing_precision']))
        qualified = [row for row in statuses['crossing_precision']['cases'] if row['kind'] == 'qualified_comparison']
        check('qualified_force_flags_recomputed', len(qualified) == 12 and all(row['strict_force_gate'] == (row['final_force_absolute_error'] < 2e-7 and row['final_force_relative_error'] < .02) for row in qualified))
        note = root/'DERIVATION-20260915-source-fitted-crossing-and-fine-phase-robustness.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json))`', content)
        check('all_cited_local_paths_exist', all((root/name).is_file() for name in cited), cited)
        check('main_note_complete_and_limitations_explicit', 'RESULTS_PENDING' not in content
              and 'not an exact finite-state change of variables' in content and 'not a full GR limit' in content
              and 'https://arxiv.org/abs/2009.12768' in content)
        own(note)
        modules = ['annular_source_fitted_action_20260915.py','verify_annular_source_fitted_action_20260915.py',
            'run_annular_source_fitted_crossing_20260915.py','derive_annular_source_fitted_live_pullback_20260915.py',
            'verify_annular_source_fitted_crossing_precision_20260915.py','seal_annular_source_fitted_crossing_20260915.py']
        for name in modules:
            path = root/'scripts'/name
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('new_modules_compile_without_bytecode', True, modules)
        check('script_bytecode_cache_absent', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        started = datetime(2026,9,15,17,19,5,tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= started]
        check('protected_workbench_mtime_changed_count_zero', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot,'outputs')
        own(executed,'outputs')
        check('resume_snapshot_and_executed_sealer_saved', True)
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(),
            current_suite_checks=counts, total_successful_current_checks=sum(counts.values()),
            distinct_files_rehashed=len(cache), inherited_failed_attempts_preserved=5,
            live_phase_results=phase['cases'], qualified_fixed_background_crossing_results=qualified,
            implementation_checks_not_all_physical_accuracy_passes=True)
        save()
        print(json.dumps(dict(state='complete', checks=len(report['checks']), current_checks=sum(counts.values()), rehashed_files=len(cache), protected_changed=len(changed))),flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
