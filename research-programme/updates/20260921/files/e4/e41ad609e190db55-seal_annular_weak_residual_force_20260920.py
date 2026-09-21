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
    destination = intake/'annular-weak-residual-force-final-integrity.json'
    executed = intake/'annular-weak-residual-force-executed-sealer.py'
    snapshot = intake/'annular-weak-residual-force-resume-snapshot.md'
    tables = [intake/('annular-weak-residual-'+label+'.csv') for label in
        ['matrices', 'field-pairings', 'integrals', 'refinement', 'integration-controls', 'dense-controls', 'exact-traces']]
    if any(path.exists() for path in [destination, executed, snapshot]+tables):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, github_action=False, subagents_used=False,
        no_new_evolution=True, valid_for_physics_claim=False, full_GR_limit_proven=False,
        full_live_P2_force_convergence_proven=False, certified_continuous_time_bound=False,
        physical_force_mismatch_fixed=False, full_moving_force_decomposition_done=False,
        weak_residual_channels_qualified=False,
        protected_scan_scope='mtime since2026-09-20T00:05:57Z; not a pre-turn whole-tree hash baseline')
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
        previous = inherit(intake/'annular-mixed-force-final-integrity.json')
        check('previous_frozen_force_seal_preserved', previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks']) and previous['frozen_operator_force_integrals_qualified']
            and not previous['physical_force_mismatch_fixed'])
        names = ['annular-weak-residual-matrices-attempt01', 'annular-weak-channel-controls-attempt01',
            'annular-weak-residual-force-attempt01', 'annular-exact-source-trace-comparison-attempt01']
        statuses = [inherit(intake/name/'status.json') for name in names]
        for name, status in zip(names, statuses):
            check(name+'_complete_nonclaim', status['state'] == 'complete' and all(row['passed'] for row in status['checks'])
                and not status['valid_for_physics_claim'] and not status['full_GR_limit_proven']
                and not status['full_live_P2_force_convergence_proven'] and not status['certified_continuous_time_bound']
                and not status['physical_force_mismatch_fixed'] and status['no_new_evolution']
                and not status['github_action'] and not status['subagents_used'])
        matrices, fixture, integrals, traces = statuses
        check('coarse_Gram_test_vanishes_without_deleting_fields', matrices['unresolved_test_Gram_zero_qualified'])
        check('independent_integrals_qualified_not_physical_pass', integrals['weak_residual_channels_qualified']
            and not integrals['full_moving_force_decomposition_done'])
        check('exact_trace_asymmetry_not_force_attribution', traces['trace_witness_not_integrated_force_attribution']
            and len(traces['cases']) == 2 and all(row['trial_jump_commutes_exactly']
                and not row['test_jump_commutes_exactly'] and row['witness_fine_index'] == 555 for row in traces['cases']))
        strict = json.loads((intake/'annular-mixed-force-integrals-attempt01/status.json').read_text())
        for branch in ['reference', 'MTS']:
            original = next(row for row in strict['cases'] if row['branch'] == branch and row['digits'] == 48 and row['channel'] == 'mixed_weak_remainder')
            tolerance = Decimal(original['literal_predecessor_gate'])
            for digits, order in [(32, 32), (48, 32), (48, 64)]:
                rows = [row for row in integrals['cases'] if row['branch'] == branch and row['digits'] == digits and row['moment_order'] == order]
                total = sum((Decimal(row['integral']) for row in rows), Decimal(0))
                check(branch+'_'+str(digits)+'_'+str(order)+'_previous_remainder', len(rows) == 5
                    and abs(total-Decimal(original['forward_integral'])) <= tolerance
                    and all(Decimal(row['literal_predecessor_gate']) == tolerance for row in rows))
                if branch == 'reference':
                    check('reference_'+str(digits)+'_'+str(order)+'_Gram_zero', all(Decimal(row['integral']) == 0
                        for row in rows if row['channel'].startswith('Gram_')))
                if digits == 48 and order == 64:
                    for row in rows:
                        check(branch+'_'+row['channel']+'_independent_adjoint',
                            abs(Decimal(row['integral'])-Decimal(row['adjoint_integral'])) <= tolerance)
            refinements = [row for row in integrals['refinement'] if row['branch'] == branch]
            check(branch+'_separated_refinement_gates', len(refinements) == 10
                and all(Decimal(row['absolute_change']) <= tolerance and row['passed']
                    and Decimal(row['literal_predecessor_gate']) == tolerance for row in refinements))
        rows_by_table = [matrices['cases'], matrices['pairings'], integrals['cases'], integrals['refinement'], integrals['controls'], fixture['cases'], traces['cases']]
        sources = [0, 0, 2, 2, 2, 1, 3]
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
        note = root/'DERIVATION-20260920-finer-test-geometry-and-Gram-force-split.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv))`', content)
        check('completed_report_and_cited_paths', 'RESULTS_PENDING' not in content and bool(cited)
            and all((root/name).is_file() for name in cited), cited)
        for name in cited:
            own(root/name)
        own(note)
        for name in ['annular_weak_residual_split_20260920.py', 'derive_annular_weak_residual_matrices_20260920.py',
                'annular_weak_channel_evolution_20260920.py', 'validate_annular_weak_channel_evolution_20260920.py',
                'derive_annular_weak_residual_force_20260920.py', 'derive_annular_exact_source_trace_comparison_20260920.py',
                'seal_annular_weak_residual_force_20260920.py']:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('sources_compile_without_bytecode', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026, 9, 20, 0, 5, 57, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= start]
        check('protected_workbench_mtime_unchanged', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(),
            implementation_checks=sum(len(status['checks']) for status in statuses),
            implementation_check_breakdown={name:len(status['checks']) for name, status in zip(names, statuses)},
            total_failed_attempts_preserved=previous['total_failed_attempts_preserved'], new_failures=[],
            distinct_files_rehashed=len(cache), table_rows=[len(rows) for rows in rows_by_table],
            weak_residual_channels_qualified=True,
            next_target='source original lifted-hinge vector and evaluate the derived rank-one lost-test-jump Gram force contribution against the trace-aware remainder; preserve native actions and all other channels')
        save()
        print(json.dumps(dict(state='complete', checks=report['implementation_checks'], integrity_checks=len(report['checks']),
            files_rehashed=len(cache), table_rows=report['table_rows'], failures_preserved=report['total_failed_attempts_preserved'])), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
