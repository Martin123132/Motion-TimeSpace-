from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_common_P2_overlay_20260919 import compose_rows
from datetime import datetime, timezone
from decimal import Decimal, getcontext
from fractions import Fraction
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
    destination = intake/'annular-rank-safe-commutator-final-integrity.json'
    executed = intake/'annular-rank-safe-commutator-executed-sealer.py'
    snapshot = intake/'annular-rank-safe-commutator-resume-snapshot.md'
    tables = [intake/('annular-rank-safe-'+name+'.csv') for name in
        ['topology', 'witnesses', 'commutators', 'localization', 'riesz-bounds', 'riesz-groups', 'riesz-solves']]
    if any(path.exists() for path in [destination, executed, snapshot]+tables):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, github_action=False, subagents_used=False,
        no_new_evolution=True, valid_for_physics_claim=False, full_GR_limit_proven=False,
        full_live_P2_force_convergence_proven=False, certified_continuous_time_bound=False,
        old_transfer_injective=False, common_overlay_injective=False, physical_force_mismatch_fixed=False,
        sharp_local_force_bound_established=False,
        protected_scan_scope='mtime since2026-09-19T22:35:05Z; not a pre-turn whole-tree hash baseline')
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
        previous = inherit(intake/'annular-decimal-transport-final-integrity.json')
        check('previous_precision_seal_preserved', previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks']) and previous['strict_frozen_saved_covector_duality_pass'])
        names = ['annular-transfer-kernel-overlay-attempt01', 'annular-commutator-riesz-bound-attempt01']
        statuses = [inherit(intake/name/'status.json') for name in names]
        for name, status in zip(names, statuses):
            check(name+'_complete_nonclaim', status['state'] == 'complete'
                and all(row['passed'] for row in status['checks']) and not status['valid_for_physics_claim']
                and not status['full_GR_limit_proven'] and not status['full_live_P2_force_convergence_proven']
                and not status['github_action'] and not status['subagents_used'] and status['no_new_evolution'])
        overlay, riesz = statuses
        strict = json.loads((intake/'annular-decimal-duality-attempt02/status.json').read_text())
        for rows in [overlay['cases'], riesz['cases']]:
            check('both_branches_and_spatial_pairs_'+str(len(report['checks'])),
                {(row['branch'], row['comparison']) for row in rows} ==
                {(branch, comparison) for branch in ['reference', 'MTS'] for comparison in ['spatial32', 'spatial64']})
            for row in rows:
                prior = next(item for item in strict['cases'] if item['branch'] == row['branch']
                    and item['comparison'] == row['comparison'] and item['digits'] == 48)
                check(row['branch']+'_'+row['comparison']+'_literal_predecessor_gate_'+str(len(report['checks'])),
                    Decimal(row['reconstruction_error']) <= Decimal(prior['unchanged_numerical_tolerance']))
        for branch in ['reference', 'MTS']:
            topology = next(row for row in overlay['topology'] if row['branch'] == branch)
            check(branch+'_singular_old_transfer_not_inverted', not topology['original_transfer_injective']
                and len(topology['erased_columns']) == 6 and not topology['nodes_merged']
                and overlay['no_pseudoinverse_or_regularization'])
            path = intake/names[0]/(branch+'-exact-common-overlay.json')
            packet = json.loads(path.read_text())
            for index, name in enumerate(['coarse', 'fine']):
                embedding = [{int(column):Fraction(value) for column, value in row.items()} for row in packet['embeddings'][index]]
                restriction = [{int(column):Fraction(value) for column, value in row.items()} for row in packet['left_inverses'][index]]
                reconstructed = compose_rows(restriction, embedding)
                check(branch+'_'+name+'_exported_exact_left_inverse',
                    len(reconstructed) == packet['native'][index]['count']
                    and all(row == {number:Fraction(1)} for number, row in enumerate(reconstructed)))
            check(branch+'_no_extra_source_trace', Fraction(packet['overlay']['anchor']) not in
                [Fraction(value) for value in packet['overlay']['nodes']])
        check('both_bounds_remain_too_loose_for_claim', all(Decimal(row['bound_to_signed_ratio']) > Decimal('1e6')
            and not row['certified_continuum_bound'] for row in riesz['cases']))
        check('MTS_bound_worsening_visible', all(Decimal(row['improvement_over_nodal_bound']) < 1
            for row in riesz['cases'] if row['branch'] == 'MTS'))
        rows_by_table = [overlay['topology'], overlay['witnesses'], overlay['cases'], overlay['localization'],
            riesz['cases'], riesz['groups'], riesz['solves']]
        source_indices = [0, 0, 0, 0, 1, 1, 1]
        for path, rows, index in zip(tables, rows_by_table, source_indices):
            source = intake/names[index]/'status.json'
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
        note = root/'DERIVATION-20260919-rank-safe-spatial-commutator-and-common-overlay.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv))`', content)
        check('report_finished_and_cited_paths_exist', 'RESULTS_PENDING' not in content
            and bool(cited) and all((root/name).is_file() for name in cited), cited)
        own(note)
        for name in ['annular_common_P2_overlay_20260919.py', 'derive_annular_transfer_kernel_and_common_overlay_20260919.py',
                'derive_annular_commutator_riesz_bound_20260919.py', 'seal_annular_rank_safe_commutator_20260919.py']:
            source = root/'scripts'/name
            compile(source.read_bytes(), str(source), 'exec')
            own(source)
        check('sources_compile_no_bytecode', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026, 9, 19, 22, 35, 5, tzinfo=timezone.utc).timestamp()
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
            total_failed_attempts_preserved=previous['total_failed_attempts_preserved'], new_failures=[],
            distinct_files_rehashed=len(cache), table_rows=[len(rows) for rows in rows_by_table],
            common_overlay_injective=True,
            next_target='original weighted weak mass/gradient/Gram comparison on exact common cells, preserving native functions and signed moment cancellations before absolute bounds')
        save()
        print(json.dumps(dict(state='complete', checks=report['implementation_checks'], integrity_checks=len(report['checks']),
            files_rehashed=len(cache), table_rows=report['table_rows'], failures_preserved=report['total_failed_attempts_preserved'])), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
