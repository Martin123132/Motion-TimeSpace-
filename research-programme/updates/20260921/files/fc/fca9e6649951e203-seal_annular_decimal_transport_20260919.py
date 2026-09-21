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
    destination = intake/'annular-decimal-transport-final-integrity.json'
    executed = intake/'annular-decimal-transport-executed-sealer.py'
    snapshot = intake/'annular-decimal-transport-resume-snapshot.md'
    tables = [intake/('annular-decimal-transport-'+name+'.csv') for name in ['pairings', 'controls', 'operators']]
    if any(path.exists() for path in [destination, executed, snapshot]+tables):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, github_action=False, subagents_used=False,
        no_new_evolution=True, valid_for_physics_claim=False, full_GR_limit_proven=False,
        full_live_P2_force_convergence_proven=False, certified_continuous_time_bound=False,
        strict_frozen_saved_covector_duality_pass=False, full_nonlinear_transport_certified=False,
        protected_scan_scope='mtime since2026-09-19T22:04:29Z; not a pre-turn whole-tree hash baseline')
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
        previous = inherit(intake/'annular-full-force-final-integrity-v3.json')
        check('previous_seal_and_failed_gate_retained', previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks']) and not previous['strict_spatial_transport_qualification_pass'])
        failed = inherit(intake/'annular-decimal-duality-attempt01/status.json')
        check('rejected_mass_storage_assumption_retained', failed['state'] == 'failed')
        names = ['annular-decimal-duality-attempt02', 'annular-decimal-operators-attempt01']
        statuses = [inherit(intake/name/'status.json') for name in names]
        for name, status in zip(names, statuses):
            check(name+'_complete_scoped_nonclaim', status['state'] == 'complete'
                and all(row['passed'] for row in status['checks']) and not status['valid_for_physics_claim']
                and not status['full_GR_limit_proven'] and not status['full_live_P2_force_convergence_proven']
                and not status['github_action'] and not status['subagents_used'] and status['no_new_evolution'])
        transport, operators = statuses
        check('eight_refined_pairings_cover_both_branches', len(transport['cases']) == 8
            and {(row['branch'], row['comparison'], row['digits']) for row in transport['cases']} ==
                {(branch, comparison, digits) for branch in ['reference', 'MTS']
                    for comparison in ['spatial32', 'spatial64'] for digits in [32, 48]})
        for row in transport['cases']:
            forward, backward = Decimal(row['forward_pairing']), Decimal(row['backward_pairing'])
            tolerance = Decimal('2e-10')*max(abs(forward), abs(backward), Decimal('1e-9'))+Decimal('3e-16')
            error = abs(forward-backward)
            check(row['branch']+'_'+row['comparison']+'_'+str(row['digits'])+'_original_gate_recomputed',
                row['original_strict_gate_pass'] and error <= tolerance
                and abs(tolerance-Decimal(row['unchanged_numerical_tolerance'])) < Decimal('1e-40'))
        check('precision_refinement_qualified_not_interval_certificate', transport['original_strict_dual_gate_pass']
            and not transport['interval_roundoff_certificate'] and not transport['certified_continuous_time_bound'])
        check('four_actual_operator_controls', len(operators['cases']) == 4
            and all(Decimal(row['wrong_transpose_relative_error']) > Decimal('1e-8') for row in operators['cases']))
        rows_by_table = [transport['cases'], transport['controls'], operators['cases']]
        source_paths = [intake/names[0]/'status.json', intake/names[0]/'status.json', intake/names[1]/'status.json']
        for path, rows, source in zip(tables, rows_by_table, source_paths):
            sourced = [dict(**row, source_path=str(source.relative_to(root))) for row in rows]
            fields = list(dict.fromkeys(key for row in sourced for key in row))
            with path.open('w', encoding='utf-8', newline='') as stream:
                writer = csv.DictWriter(stream, fieldnames=fields)
                writer.writeheader()
                writer.writerows(sourced)
            with path.open(encoding='utf-8', newline='') as stream:
                parsed = list(csv.DictReader(stream))
            check(path.name+'_sourced_nonclaim_rows_parse', len(parsed) == len(sourced)
                and all(None not in row and row['valid_for_claim'] == 'False'
                    and (root/row['source_path']).is_file() for row in parsed))
            own(path, 'outputs')
        note = root/'DERIVATION-20260919-cancellation-preserving-source-force-transport.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv))`', content)
        check('report_finished_and_cited_paths_exist', 'RESULTS_PENDING' not in content
            and bool(cited) and all((root/name).is_file() for name in cited), cited)
        own(note)
        for name in ['annular_decimal_transport_20260919.py', 'annular_decimal_transport_v2_20260919.py',
                'derive_annular_decimal_duality_20260919.py', 'derive_annular_decimal_duality_v2_20260919.py',
                'validate_annular_decimal_operators_20260919.py', 'seal_annular_decimal_transport_20260919.py']:
            source = root/'scripts'/name
            compile(source.read_bytes(), str(source), 'exec')
            own(source)
        check('compiled_without_bytecode', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026, 9, 19, 22, 4, 29, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*')
            if path.is_file() and path.stat().st_mtime >= start]
        check('protected_mtime_changed_count_zero', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(),
            implementation_checks=sum(len(status['checks']) for status in statuses),
            implementation_check_breakdown={name:len(status['checks']) for name, status in zip(names, statuses)},
            total_failed_attempts_preserved=previous['total_failed_attempts_preserved']+1,
            new_failures=[dict(folder='annular-decimal-duality-attempt01', error=failed['error'])],
            distinct_files_rehashed=len(cache), table_rows=[len(rows) for rows in rows_by_table],
            strict_frozen_saved_covector_duality_pass=True,
            next_target='force-weighted mass/stiffness/nonnested-transfer commutator and source-local bound; physical force mismatch unchanged')
        save()
        print(json.dumps(dict(state='complete', checks=report['implementation_checks'],
            integrity_checks=len(report['checks']), files_rehashed=len(cache),
            strict_frozen_saved_covector_duality_pass=True)), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
