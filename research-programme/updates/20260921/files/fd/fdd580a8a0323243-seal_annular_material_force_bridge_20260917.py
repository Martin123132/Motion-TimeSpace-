from derive_annular_source_gravity_20260914 import EvidenceRun
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import re
import traceback


def main():
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    destination = intake/'annular-material-force-bridge-final-integrity.json'
    snapshot = intake/'annular-material-force-bridge-resume-snapshot.md'
    executed = intake/'annular-material-force-bridge-executed-sealer.py'
    if any(path.exists() for path in [destination, snapshot, executed]):
        raise FileExistsError('Immutable evidence already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, full_GR_limit_proven=False,
        valid_for_physics_claim=False, original_action_unchanged=True, github_action=False, subagents_used=False,
        original_trajectories_reused_not_rerun=True, no_forward_trajectory_rerun=True,
        instantaneous_force_convergence_proven=False, time_integrator_error_certified=False,
        derivative_samples_not_uniform_Lipschitz_certificate=True, implementation_checks_not_physics_passes=True,
        protected_scan_scope='mtime since turn start2026-09-17T18:29:02Z; not a pre-turn full hash baseline',
        sampled_lower_bound_flag_interpretation='Sample-supremum ordering only; evaluations at approximate saved states do not certify a bound on the exact trajectory.',
        current_initial_slope_limit_not_proven=True, averaged_force_not_peak_force=True)
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
                key = str(path.relative_to(root))
                if not path.is_file() or digest(path) != expected:
                    raise RuntimeError('Missing or changed immutable evidence: '+name)
                if key in report['inputs'] and report['inputs'][key] != expected:
                    raise RuntimeError('Conflicting immutable evidence: '+name)
                report['inputs'][key] = expected

    save()
    try:
        previous_path = intake/'annular-galerkin-limit-final-integrity.json'
        previous = json.loads(previous_path.read_text())
        check('previous_seal_complete', previous['state'] == 'complete' and all(row['passed'] for row in previous['checks']))
        inherit(previous)
        own(previous_path)
        statuses, counts = {}, {}
        for name, label, count, cases in [('impulses', 'annular-material-impulses-attempt01', 68, 4),
                ('bridge', 'annular-force-bridge-attempt01', 75, 4),
                ('corner', 'annular-initial-force-corner-attempt01', 57, 18)]:
            path = intake/label/'status.json'
            status = json.loads(path.read_text())
            check(name+'_complete', status['state'] == 'complete' and len(status['checks']) == count
                and len(status['cases']) == cases and all(row['passed'] for row in status['checks']))
            check(name+'_scope', not status['full_GR_limit_proven'] and not status['valid_for_physics_claim']
                and not status['complete_parent_source_action_derived'] and status['original_action_unchanged']
                and status['old_peak_force_gates_unchanged'])
            inherit(status)
            own(path)
            statuses[name], counts[name] = status, count
        check('inherited_failures_preserved', previous['inherited_failed_attempts_preserved'] == 26
            and previous['original_failed_cases_preserved'] and previous['inherited_peak_force_failures_preserved'] == 4)
        impulses, bridge, corner = [statuses[name] for name in ['impulses', 'bridge', 'corner']]
        expected_keys = {(branch, nodes) for branch in ['reference', 'MTS'] for nodes in [513, 1025]}
        check('same_four_saved_cases', all({(row['branch'], row['base_count']) for row in status['cases']} == expected_keys
            for status in [impulses, bridge]))
        check('all_four_peak_failures_retained', all(not row['original_peak_force_gate_pass']
            for status in [impulses, bridge] for row in status['cases']))
        check('same_peak_values_preserved', all(abs(left['original_sampled_peak_force_error']-right['original_sampled_peak_force_error']) < 1e-16
            for left, right in zip(impulses['cases'], bridge['cases'])))
        check('window_protocol_not_replacement_gate', impulses['averaged_force_not_peak_force']
            and impulses['no_new_smoothed_force_acceptance_claim'] and impulses['protocol']['scale_is_not_a_new_acceptance_gate']
            and impulses['protocol']['widths'] == [.025, .05, .1, .2, .4]
            and all([window['aligned_windows'] for window in row['windows']] == [76, 71, 61, 41, 1] for row in impulses['cases']))
        check('all_rate_diagnostics_uncertified', bridge['derivative_samples_not_uniform_Lipschitz_certificate']
            and not bridge['pointwise_force_convergence_proven'] and bridge['source_field_momentum_retained']
            and all(row['diagnostic_is_not_a_continuous_bound'] for row in bridge['cases']))
        check('all_optimizing_windows_unresolved', all(row['diagnostic_window_below_saved_spacing']
            and row['uncertified_optimizing_window'] < .005 for row in bridge['cases']))
        check('initial_corner_not_repaired_by_data_change', corner['initial_data_only'] and corner['original_incompatible_corner_retained']
            and corner['initial_data_not_replaced'] and corner['finite_initial_rate_limit_not_proven']
            and abs(corner['reference_initial_force_rate']+.002412) < 3e-17)
        check('initial_sweep_both_branches', {(row['branch'], row['base_count']) for row in corner['cases']}
            == {(branch, count) for branch in ['reference', 'MTS'] for count in [33, 65, 129, 257, 513, 1025, 2049, 4097, 8193]})
        note = root/'DERIVATION-20260917-material-impulses-and-instantaneous-force-bridge.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json))`', content)
        check('cited_note_paths_exist', bool(cited) and all((root/name).is_file() for name in cited), cited)
        check('note_complete_and_scope_clear', 'PENDING' not in content and '200 implementation checks' in content
            and 'Instantaneous force convergence remains unproved.' in content
            and 'not validated lower or upper bounds' in content and 'all26 inherited' in content)
        own(note)
        names = ['qualify_annular_material_impulses_20260917.py', 'annular_instantaneous_force_bridge_20260917.py',
            'qualify_annular_force_bridge_20260917.py', 'qualify_annular_initial_force_corner_20260917.py',
            'seal_annular_material_force_bridge_20260917.py']
        for name in names:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('new_sources_compile', True, names)
        check('script_bytecode_cache_absent', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        started = datetime(2026, 9, 17, 18, 29, 2, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*')
            if path.is_file() and path.stat().st_mtime >= started]
        check('protected_workbench_mtime_changed_count_zero', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        check('resume_and_executed_source_preserved', True)
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(),
            current_suite_checks=counts, total_successful_current_checks=sum(counts.values()),
            distinct_files_rehashed=len(cache), inherited_failed_attempts_preserved=26, new_failed_attempts_preserved=[],
            original_failed_cases_preserved=True, inherited_peak_force_failures_preserved=4,
            impulse_results=impulses['cases'], bridge_results=bridge['cases'], initial_corner_results=corner['cases'])
        save()
        print(json.dumps(dict(state='complete', checks=len(report['checks']), current_checks=sum(counts.values()),
            rehashed_files=len(cache), protected_changed=len(changed), failed_attempts_preserved=26)), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
