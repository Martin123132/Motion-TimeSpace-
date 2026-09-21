from derive_annular_source_gravity_20260914 import EvidenceRun
from datetime import datetime, timezone
from pathlib import Path
import csv
import hashlib
import json
import math
import re
import traceback


def main():
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    destination = intake/'annular-live-Gram-transport-final-integrity.json'
    table = intake/'annular-live-Gram-transport-budgets.csv'
    samples_table = intake/'annular-live-Gram-transport-samples.csv'
    snapshot = intake/'annular-live-Gram-transport-resume-snapshot.md'
    executed = intake/'annular-live-Gram-transport-executed-sealer.py'
    if any(path.exists() for path in [destination, table, samples_table, snapshot, executed]):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, github_action=False,
        subagents_used=False, full_GR_limit_proven=False, valid_for_physics_claim=False,
        full_live_P2_force_convergence_proven=False, no_new_trajectory_evolution=True,
        complete_nonlinear_adjoint_derived=False, live_transport_channel_quadrature_certified=False,
        protected_scan_scope='mtime since2026-09-19T07:39:31Z; not a pre-turn full hash baseline')
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

    def own(path, category='inputs'):
        report[category][str(path.resolve().relative_to(root))] = digest(path)

    def save():
        destination.write_text(json.dumps(report, indent=2, allow_nan=False)+'\n', encoding='utf-8')

    def check(name, passed, detail=None):
        report['checks'].append(dict(name=name, passed=bool(passed), detail=detail))
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def inherit(path):
        data = json.loads(path.read_text())
        for category in ['inputs', 'outputs']:
            for name, expected in data[category].items():
                source = (root/name).resolve()
                key = str(source.relative_to(root))
                if not source.is_file() or digest(source) != expected:
                    raise RuntimeError('Changed sealed source: '+name)
                if key in report['inputs'] and report['inputs'][key] != expected:
                    raise RuntimeError('Conflicting sealed source: '+name)
                report['inputs'][key] = expected
        own(path)
        return data

    def write_table(path, rows):
        with path.open('w', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        with path.open(encoding='utf-8', newline='') as stream:
            parsed = list(csv.DictReader(stream))
        check(path.name+'_sourced_nonclaim_rows_parse', len(parsed) == len(rows) and all(None not in row
            and row['valid_for_claim'] == 'False' and (root/row['source_path']).is_file() for row in parsed))
        check(path.name+'_numeric_values_finite', all(math.isfinite(value) for row in rows
            for value in row.values() if isinstance(value, (float, int))))
        own(path, 'outputs')

    save()
    try:
        previous = inherit(intake/'annular-source-impulse-final-integrity.json')
        check('previous_checkpoint_and40failures_preserved', previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks']) and previous['total_failed_attempts_preserved'] == 40)
        names = ['annular-live-Gram-defect-transport-MTS-attempt01',
            'annular-live-Gram-defect-transport-reference-attempt01', 'annular-Gram-transport-identity-attempt01']
        statuses = []
        for name in names:
            status = inherit(intake/name/'status.json')
            statuses.append(status)
            check(name+'_complete_nonclaim_private', status['state'] == 'complete'
                and all(row['passed'] for row in status['checks']) and not status['valid_for_physics_claim']
                and not status['full_GR_limit_proven'] and not status['full_live_P2_force_convergence_proven']
                and not status['github_action'] and not status['subagents_used'])
        failures = []
        for prefix in ['annular-live-Gram-defect-transport-', 'annular-Gram-transport-identity-']:
            for path in sorted(intake.glob(prefix+'*/status.json')):
                if path.parent.name not in names:
                    status = inherit(path)
                    check(path.parent.name+'_failed_attempt_preserved', status['state'] == 'failed')
                    failures.append(dict(folder=path.parent.name, error=status['error']))
        count = sum(len(status['checks']) for status in statuses)
        check('236_successful_implementation_checks', count == 236, count)
        budgets, samples = [], []
        for name, status in zip(names[:2], statuses[:2]):
            check(name+'_actual_paths_and_scope_retained', len(status['samples']) == 33 and len(status['cases']) == 9
                and status['no_new_trajectory_evolution'] and status['changing_geometry_reconstructed_on_both_actual_paths']
                and status['all_Gram_rows_retained'] and status['geometry_and_initial_data_terms_not_discarded']
                and status['temporal_hierarchy_not_continuum_error']
                and status['exact_moving_covector_identity_not_a_full_adjoint_solve'])
            source_path = str((intake/name/'status.json').relative_to(root))
            for item in status['cases']:
                budgets.append(dict(branch=status['branch'], partition=item['partition'],
                    intervals=item['sample_intervals'], endpoint_difference=item['endpoint_difference'],
                    initial_difference=item['initial_difference'], geometry_change=item['terminal_geometry_change'],
                    **item['signed_terms'], endpoint_absolute_bound=item['endpoint_bound'],
                    reconstruction_error=item['reconstruction_error'], valid_for_claim=False, source_path=source_path))
            for item in status['samples']:
                samples.append(dict(branch=status['branch'], **item, source_path=source_path))
            for stride in [1, 2, 4]:
                parts = {row['partition']:row for row in status['cases'] if row['stride'] == stride}
                check(name+'_'+str(stride)+'_partitions_add', abs(parts['all_rows']['endpoint_difference']
                    -parts['source_rows']['endpoint_difference']-parts['remaining_rows']['endpoint_difference']) < 3e-15)
        check('independent_exact_solution_and_negative_controls', statuses[2]['nonzero_path_quadrature_defect_despite_zero_ODE_error']
            and statuses[2]['independent_exact_solution_not_a_parent_evolution']
            and len(statuses[2]['cases']) == 3 and all(row['known_ODE_error'] == 0 for row in statuses[2]['cases']))
        write_table(table, budgets)
        write_table(samples_table, samples)
        note = root/'DERIVATION-20260919-live-Gram-force-error-transport.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv))`', content)
        check('all_cited_local_paths_exist', bool(cited) and all((root/name).is_file() for name in cited), cited)
        check('adverse_results_and_scope_disclosed', 'Results pending' not in content
            and 'does not establish the full GR limit' in content and 'NOT a resolved attribution' in content
            and '13.58%' in content and '12.5718%' in content and 'reconstruction floor' in content)
        own(note)
        for name in ['derive_annular_live_Gram_defect_transport_20260919.py',
                'validate_annular_Gram_transport_identity_20260919.py', 'seal_annular_live_Gram_transport_20260919.py']:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('sources_compile_without_bytecode', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026, 9, 19, 7, 39, 31, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= start]
        check('protected_mtime_changed_count_zero', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(),
            implementation_checks=count, total_failed_attempts_preserved=40+len(failures),
            new_failed_executions=len(failures), new_failures=failures, distinct_files_rehashed=len(cache),
            full_interval_retested=False, budget_rows=len(budgets), sample_rows=len(samples))
        save()
        print(json.dumps(dict(state='complete', implementation_checks=count, integrity_checks=len(report['checks']),
            files_rehashed=len(cache), failed_attempts_preserved=40+len(failures), budget_rows=len(budgets), sample_rows=len(samples))), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
