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
    destination = intake/'annular-trace-aware-Gram-final-integrity.json'
    executed = intake/'annular-trace-aware-Gram-executed-sealer.py'
    snapshot = intake/'annular-trace-aware-Gram-resume-snapshot.md'
    tables = [intake/('annular-trace-aware-Gram-'+label+'.csv') for label in
        ['sources', 'matrices', 'field-pairings', 'integrals', 'refinement', 'integration-controls', 'regrouped']]
    if any(path.exists() for path in [destination, executed, snapshot]+tables):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, github_action=False, subagents_used=False,
        no_new_evolution=True, original_action_unchanged=True, valid_for_physics_claim=False, full_GR_limit_proven=False,
        full_live_P2_force_convergence_proven=False, certified_continuous_time_bound=False,
        physical_force_mismatch_fixed=False, full_moving_force_decomposition_done=False,
        trace_aware_Gram_force_qualified=False,
        protected_scan_scope='mtime since2026-09-20T12:38:52Z; not a pre-turn whole-tree hash baseline')
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
        previous = inherit(intake/'annular-weak-residual-force-final-integrity.json')
        check('previous_weak_force_seal_preserved', previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks']) and previous['weak_residual_channels_qualified']
            and not previous['physical_force_mismatch_fixed'])
        names = ['annular-trace-aware-Gram-matrices-attempt01', 'annular-trace-aware-Gram-force-attempt01']
        statuses = [inherit(intake/name/'status.json') for name in names]
        for name, status in zip(names, statuses):
            check(name+'_complete_nonclaim', status['state'] == 'complete' and all(row['passed'] for row in status['checks'])
                and not status['valid_for_physics_claim'] and not status['full_GR_limit_proven']
                and not status['full_live_P2_force_convergence_proven'] and not status['certified_continuous_time_bound']
                and not status['physical_force_mismatch_fixed'] and status['no_new_evolution'] and status['original_action_unchanged']
                and not status['github_action'] and not status['subagents_used'])
        matrices, integrals = statuses
        check('original_factors_and_native_action_preserved', matrices['original_Gram_factors_reproduced']
            and matrices['native_action_preserving_extension_proven']
            and len(matrices['sources']) == 4 and all(row['exact_original_Gram_factor'] for row in matrices['sources']))
        check('integrals_qualified_not_physical_pass', integrals['trace_aware_Gram_force_qualified']
            and not integrals['full_moving_force_decomposition_done'])
        strict = json.loads((intake/'annular-weak-residual-force-attempt01/status.json').read_text())
        for branch in ['reference', 'MTS']:
            original = next(row for row in strict['cases'] if row['branch'] == branch and row['digits'] == 48
                and row['moment_order'] == 64 and row['channel'] == 'Gram_same_geometry_stencil')
            tolerance = Decimal(original['literal_predecessor_gate'])
            for digits in ([0] if branch == 'reference' else [32, 48]):
                rows = [row for row in integrals['cases'] if row['branch'] == branch and row['digits'] == digits]
                total = sum((Decimal(row['integral']) for row in rows), Decimal(0))
                check(branch+'_'+str(digits)+'_previous_Gram_recovered', len(rows) == 2
                    and abs(total-Decimal(original['integral'])) <= tolerance
                    and all(Decimal(row['literal_predecessor_gate']) == tolerance for row in rows))
                if digits in [0, 48]:
                    for row in rows:
                        check(branch+'_'+row['channel']+'_adjoint_or_exact_zero', abs(Decimal(row['integral'])-Decimal(row['adjoint_integral'])) <= tolerance)
                if branch == 'reference':
                    check('reference_analytic_zero_not_surrogate', all(Decimal(row['integral']) == 0
                        and row['evaluation_method'] == 'analytic_zero_operator' for row in rows))
            regrouped = next(row for row in integrals['regrouped'] if row['branch'] == branch)
            check(branch+'_regrouping_not_a_repair', abs(Decimal(regrouped['weak_total'])-Decimal(original['total'])) <= tolerance
                and Decimal(regrouped['literal_predecessor_gate']) == tolerance)
        check('MTS_fixed_matrix_precision_order_refinement', len(integrals['refinement']) == 2
            and all(row['passed'] and Decimal(row['absolute_change']) <= Decimal(row['literal_predecessor_gate'])
                and row['comparison'] == 'arithmetic_and_time_order_fixed_matrices' for row in integrals['refinement']))
        mts_rows = {row['channel']:row for row in integrals['cases'] if row['branch'] == 'MTS' and row['digits'] == 48}
        mts_old = Decimal(mts_rows['lost_test_trace']['prior_Gram_integral'])
        mts_trace = Decimal(mts_rows['lost_test_trace']['integral'])
        mts_remainder = Decimal(mts_rows['trace_aware_Gram_remainder']['integral'])
        mts_gate = Decimal(mts_rows['lost_test_trace']['literal_predecessor_gate'])
        report['scientific_decision'] = dict(scope='specified off-native comparison and original frozen paths only',
            old_Gram_integral=str(mts_old), lost_trace_integral=str(mts_trace), remainder=str(mts_remainder),
            remainder_to_old_magnitude=str(abs(mts_remainder/mts_old)),
            trace_has_opposite_sign_to_old=bool(mts_trace*mts_old < 0),
            trace_alone_exhausts_old_channel_at_literal_gate=bool(abs(mts_remainder) <= mts_gate),
            remainder_smaller_than_old_channel=bool(abs(mts_remainder) < abs(mts_old)),
            physical_force_mismatch_fixed=False, whole_MTS_rejected=False, valid_for_claim=False)
        rows_by_table = [matrices['sources'], matrices['cases'], matrices['pairings'], integrals['cases'],
            integrals['refinement'], integrals['controls'], integrals['regrouped']]
        source_indices = [0, 0, 0, 1, 1, 1, 1]
        for path, rows, source_index in zip(tables, rows_by_table, source_indices):
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
        note = root/'DERIVATION-20260920-trace-aware-Gram-force-contribution.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv))`', content)
        check('completed_report_and_cited_paths', 'RESULTS_PENDING' not in content and bool(cited)
            and all((root/name).is_file() for name in cited), cited)
        for name in cited:
            own(root/name)
        own(note)
        for name in ['derive_annular_trace_aware_Gram_matrices_20260920.py',
                'derive_annular_trace_aware_Gram_force_20260920.py', 'seal_annular_trace_aware_Gram_20260920.py']:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('sources_compile_without_bytecode', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026, 9, 20, 12, 38, 52, tzinfo=timezone.utc).timestamp()
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
            trace_aware_Gram_force_qualified=True,
            next_target='Derive and qualify an action-consistent source/front-resolved spatial construction before a short frozen force pilot in both branches: uniform-grid recovery, full source/metric variation, unchanged physical coefficients and all modes. No further trace-only repair or blind source-cell halving.')
        save()
        print(json.dumps(dict(state='complete', checks=report['implementation_checks'], integrity_checks=len(report['checks']),
            files_rehashed=len(cache), table_rows=report['table_rows'], failures_preserved=report['total_failed_attempts_preserved'])), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
