from derive_annular_source_gravity_20260914 import EvidenceRun
from datetime import datetime, timezone
from decimal import Decimal, getcontext
from pathlib import Path
import csv
import hashlib
import json
import re
import traceback


def main():
    getcontext().prec = 80
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    destination = intake/'annular-mixed-force-final-integrity.json'
    executed = intake/'annular-mixed-force-executed-sealer.py'
    snapshot = intake/'annular-mixed-force-resume-snapshot.md'
    tables = [intake/('annular-mixed-force-'+label+'.csv') for label in
        ['matrices', 'integrals', 'combined-refinement', 'isolated-refinement', 'integration-controls', 'dense-controls']]
    if any(path.exists() for path in [destination, executed, snapshot]+tables):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, github_action=False, subagents_used=False,
        no_new_evolution=True, valid_for_physics_claim=False, full_GR_limit_proven=False,
        full_live_P2_force_convergence_proven=False, certified_continuous_time_bound=False,
        physical_force_mismatch_fixed=False, full_moving_force_decomposition_done=False,
        frozen_operator_force_integrals_qualified=False,
        protected_scan_scope='mtime since2026-09-19T23:27:37Z; not a pre-turn whole-tree hash baseline')
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
                    raise RuntimeError('Conflicting source: '+name)
                report['inputs'][key] = expected
        own(path)
        return data

    save()
    try:
        previous = inherit(intake/'annular-common-weak-action-final-integrity.json')
        check('previous_weighted_probe_seal_preserved', previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks']) and previous['weighted_probe_precision_qualified']
            and not previous['physical_force_mismatch_fixed'])
        names = ['annular-mixed-weak-matrices-attempt01', 'annular-mixed-force-controls-attempt02',
            'annular-mixed-force-integrals-attempt01', 'annular-mixed-force-refinement-attempt01']
        statuses = [inherit(intake/name/'status.json') for name in names]
        for name, status in zip(names, statuses):
            check(name+'_complete_nonclaim', status['state'] == 'complete' and all(row['passed'] for row in status['checks'])
                and not status['valid_for_physics_claim'] and not status['full_GR_limit_proven']
                and not status['full_live_P2_force_convergence_proven'] and not status['certified_continuous_time_bound']
                and status['no_new_evolution'] and not status['github_action'] and not status['subagents_used'])
        failed_name = 'annular-mixed-force-controls-attempt01'
        failed = inherit(intake/failed_name/'status.json')
        check('first_fixture_setup_failure_preserved', failed['state'] == 'failed'
            and 'zero-size array' in failed['error'])
        assembly, fixture, integrals, refinement = statuses
        check('time_integrals_not_just_initial_probes', integrals['frozen_operator_force_integrals_qualified']
            and refinement['isolated_quadrature_and_time_precision_checked']
            and not integrals['full_moving_force_decomposition_done'] and not integrals['physical_force_mismatch_fixed'])
        strict = json.loads((intake/'annular-decimal-duality-attempt02/status.json').read_text())
        for branch in ['reference', 'MTS']:
            original = next(row for row in strict['cases'] if row['branch'] == branch and row['comparison'] == 'spatial64' and row['digits'] == 48)
            tolerance = Decimal(original['unchanged_numerical_tolerance'])
            check(branch+'_both_moment_matrix_orders', {row['order'] for row in assembly['cases'] if row['branch'] == branch} == {32, 64})
            for digits in [32, 48]:
                rows = [row for row in integrals['cases'] if row['branch'] == branch and row['digits'] == digits]
                total = sum((Decimal(row['forward_integral']) for row in rows), Decimal(0))
                check(branch+'_'+str(digits)+'_original_frozen_force_sum', len(rows) == 3
                    and abs(total-Decimal(original['frozen_operator_commutator'])) <= tolerance
                    and all(Decimal(row['literal_predecessor_gate']) == tolerance for row in rows))
                if digits == 48:
                    for row in rows:
                        check(branch+'_'+row['channel']+'_independent_dual',
                            abs(Decimal(row['forward_integral'])-Decimal(row['adjoint_integral'])) <= tolerance)
            rows = [row for row in refinement['cases'] if row['branch'] == branch]
            check(branch+'_separated_refinements_replayed', len(rows) == 3
                and all(Decimal(row['time_order_and_precision_change']) <= tolerance
                    and Decimal(row['spatial_moment_order_change']) <= tolerance
                    and Decimal(row['literal_predecessor_gate']) == tolerance for row in rows))
        rows_by_table = [assembly['cases'], integrals['cases'], integrals['refinement'], refinement['cases'], integrals['controls'], fixture['cases']]
        sources = [0, 2, 2, 3, 2, 1]
        for path, rows, source_index in zip(tables, rows_by_table, sources):
            source = intake/names[source_index]/'status.json'
            sourced = [dict(**row, source_path=str(source.relative_to(root))) for row in rows]
            fields = list(dict.fromkeys(key for row in sourced for key in row))
            with path.open('w', encoding='utf-8', newline='') as stream:
                writer = csv.DictWriter(stream, fieldnames=fields)
                writer.writeheader()
                writer.writerows(sourced)
            with path.open(encoding='utf-8', newline='') as stream:
                parsed = list(csv.DictReader(stream))
            check(path.name+'_sourced_nonclaim_rows_parse', len(parsed) == len(rows) and all(None not in row
                and row['valid_for_claim'] == 'False' and (root/row['source_path']).is_file() for row in parsed))
            own(path, 'outputs')
        note = root/'DERIVATION-20260920-mixed-weak-frozen-force-integrals.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv))`', content)
        check('completed_report_and_cited_paths', 'RESULTS_PENDING' not in content
            and bool(cited) and all((root/name).is_file() for name in cited), cited)
        own(note)
        sources = ['annular_mixed_weak_maps_20260920.py', 'derive_annular_mixed_weak_matrices_20260920.py',
            'annular_mixed_force_cascade_20260920.py', 'validate_annular_mixed_force_cascade_20260920.py',
            'validate_annular_mixed_force_cascade_v2_20260920.py', 'derive_annular_mixed_force_integrals_20260920.py',
            'validate_annular_mixed_force_refinement_20260920.py', 'seal_annular_mixed_force_integrals_20260920.py']
        for name in sources:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('sources_compile_without_bytecode', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026, 9, 19, 23, 27, 37, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= start]
        check('protected_workbench_mtime_unchanged', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(),
            implementation_checks=sum(len(status['checks']) for status in statuses),
            implementation_check_breakdown={name:len(status['checks']) for name, status in zip(names, statuses)},
            total_failed_attempts_preserved=previous['total_failed_attempts_preserved']+1,
            new_failures=[failed_name], distinct_files_rehashed=len(cache), table_rows=[len(rows) for rows in rows_by_table],
            frozen_operator_force_integrals_qualified=True,
            next_target='derive the mixed weak remainder into coarse-test closure, fine-test approximation defect, geometry-weight and Gram-stencil differences before assigning a physical cause')
        save()
        print(json.dumps(dict(state='complete', checks=report['implementation_checks'], integrity_checks=len(report['checks']),
            files_rehashed=len(cache), table_rows=report['table_rows'], failures_preserved=report['total_failed_attempts_preserved'])), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
