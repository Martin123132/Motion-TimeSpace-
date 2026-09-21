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
    destination = intake/'annular-full-characteristic-final-integrity.json'
    snapshot = intake/'annular-full-characteristic-resume-snapshot.md'
    executed = intake/'annular-full-characteristic-executed-sealer.py'
    if any(path.exists() for path in [destination, snapshot, executed]):
        raise FileExistsError('Immutable evidence already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, full_GR_limit_proven=False,
        valid_for_physics_claim=False, original_action_unchanged=True, github_action=False,
        subagents_used=False, original_trajectories_reused_not_rerun=True,
        implementation_checks_not_physical_passes=True,
        protected_scan_scope='mtime since turn start2026-09-17T17:01:29Z; not a pre-turn full hash baseline')
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
        path = intake/'annular-force-adjoint-final-integrity.json'
        previous = json.loads(path.read_text())
        check('previous_seal_complete', previous['state'] == 'complete' and all(row['passed'] for row in previous['checks']))
        inherit(previous)
        own(path)
        statuses, counts = {}, {}
        for name, label, count, cases in [('field', 'annular-full-characteristic-field-attempt01', 35, 1),
                ('regularity', 'annular-actual-reference-regularity-attempt01', 15, 1),
                ('comparison', 'annular-characteristic-saved-comparison-attempt01', 27, 4)]:
            path = intake/label/'status.json'
            status = json.loads(path.read_text())
            check(name+'_complete', status['state'] == 'complete' and len(status['checks']) == count
                and len(status['cases']) == cases and all(row['passed'] for row in status['checks']))
            check(name+'_scope', not status['full_GR_limit_proven'] and not status['valid_for_physics_claim']
                and not status['complete_parent_source_action_derived'] and status['original_action_unchanged'])
            inherit(status)
            own(path)
            statuses[name], counts[name] = status, count
        field, regularity, comparison = [statuses[name] for name in ['field', 'regularity', 'comparison']]
        check('reference_and_regularity_independent_of_finite_future', not field['finite_future_trajectories_read']
            and not regularity['finite_future_trajectories_read'] and field['cases'][0]['comparison_data_not_yet_opened'])
        check('comparison_reference_freeze_order', datetime.fromisoformat(field['reference_frozen_at'])
            < datetime.fromisoformat(comparison['qualified_reference_verified_at'])
            <= datetime.fromisoformat(comparison['finite_read_started_at']))
        check('analytic_regularities_not_entire_MTS_claim', regularity['actual_flat_reference_piecewise_curvature_bound_derived']
            and regularity['exact_rational_majorants'] and regularity['constants_deliberately_nonsharp']
            and not regularity['actual_finite_MTS_trajectory_regularity_proven']
            and not regularity['base_Galerkin_residual_bound_proven']
            and not regularity['nonlinear_neighborhood_bootstrap_proven'] and not regularity['force_trace_convergence_proven'])
        check('fair_original_trajectory_comparison', comparison['original_trajectories_reused_not_rerun']
            and comparison['all_branches_treated_identically'] and not comparison['force_fit']
            and not comparison['force_correction'] and comparison['original_physical_gates_unchanged']
            and {(row['branch'], row['base_count']) for row in comparison['cases']}
                == {('reference', 513), ('reference', 1025), ('MTS', 513), ('MTS', 1025)})
        check('all_four_peak_force_failures_retained', all(not row['peak_absolute_force_gate_pass'] for row in comparison['cases']))
        check('field_and_source_gates_pass_not_full_GR', all(row['field_gate_pass'] and row['source_clock_gate_pass']
            and not row['full_GR_limit_proven'] for row in comparison['cases']))
        check('terminal_and_peak_gates_not_confused', all(row['terminal_combined_force_gate_pass'] == (row['base_count'] == 1025)
            for row in comparison['cases']))
        check('two_grid_ratios_not_convergence_proof', all(row['two_grid_comparison_not_uniform_convergence_proof'] for row in comparison['refinement']))
        check('inherited_failures_preserved', previous['inherited_failed_attempts_preserved'] == 25 and previous['original_failed_cases_preserved'])
        note = root/'DERIVATION-20260917-full-characteristic-reference-and-actual-regularity.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json))`', content)
        check('cited_note_paths_exist', all((root/name).is_file() for name in cited), cited)
        check('completed_note_scoped', 'PENDING' not in content and 'not the full GR limit' in content
            and '77 current implementation checks' in content and 'four failed peak-force gates' in content)
        own(note)
        names = ['annular_full_characteristic_field_20260917.py', 'qualify_annular_full_characteristic_field_20260917.py',
            'derive_annular_actual_reference_regularity_20260917.py', 'compare_annular_characteristic_saved_trajectories_20260917.py',
            'seal_annular_full_characteristic_20260917.py']
        for name in names:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('new_sources_compile', True, names)
        check('script_bytecode_cache_absent', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        started = datetime(2026, 9, 17, 17, 1, 29, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*')
            if path.is_file() and path.stat().st_mtime >= started]
        check('protected_workbench_mtime_changed_count_zero', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        check('resume_and_executed_source_preserved', True)
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(),
            total_successful_current_checks=sum(counts.values()), current_suite_checks=counts,
            distinct_files_rehashed=len(cache), inherited_failed_attempts_preserved=25,
            new_failed_attempts_preserved=[], original_failed_cases_preserved=True,
            failed_current_peak_force_cases=4, field_qualification=field['cases'],
            actual_reference_regularity=regularity['cases'], saved_comparisons=comparison['cases'],
            two_grid_refinement=comparison['refinement'])
        save()
        print(json.dumps(dict(state='complete', checks=len(report['checks']), current_checks=sum(counts.values()),
            rehashed_files=len(cache), protected_changed=len(changed), failed_attempts_preserved=25,
            failed_current_peak_force_cases=4)), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
