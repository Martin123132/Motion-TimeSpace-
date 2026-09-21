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
    destination = intake/'annular-common-weak-action-final-integrity.json'
    executed = intake/'annular-common-weak-action-executed-sealer.py'
    snapshot = intake/'annular-common-weak-action-resume-snapshot.md'
    tables = [intake/('annular-common-weak-'+name+'.csv') for name in
        ['acquisition', 'summary', 'channels', 'regions', 'moments-controls', 'refinement', 'independent-controls']]
    if any(path.exists() for path in [destination, executed, snapshot]+tables):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, github_action=False, subagents_used=False,
        no_new_evolution=True, valid_for_physics_claim=False, full_GR_limit_proven=False,
        full_live_P2_force_convergence_proven=False, certified_continuous_time_bound=False,
        weighted_probe_precision_qualified=False, actual_time_integrated_force_decomposition_done=False,
        physical_force_mismatch_fixed=False,
        protected_scan_scope='mtime since2026-09-19T23:00:47Z; not a pre-turn whole-tree hash baseline')
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
        previous = inherit(intake/'annular-rank-safe-commutator-final-integrity.json')
        check('previous_seal_and_rank_obstruction_preserved', previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks']) and previous['common_overlay_injective']
            and not previous['old_transfer_injective'])
        names = ['annular-common-action-weights-attempt01', 'annular-common-weak-action-attempt01', 'annular-common-weak-controls-attempt01']
        statuses = [inherit(intake/name/'status.json') for name in names]
        for name, status in zip(names, statuses):
            check(name+'_complete_nonclaim', status['state'] == 'complete'
                and all(row['passed'] for row in status['checks']) and not status['valid_for_physics_claim']
                and not status['full_GR_limit_proven'] and not status['full_live_P2_force_convergence_proven']
                and not status['github_action'] and not status['subagents_used'] and status['no_new_evolution'])
        acquisition, weak, independent = statuses
        strict = json.loads((intake/'annular-decimal-duality-attempt02/status.json').read_text())
        check('actual_geometry_mass_and_Gram_reproduced', len(acquisition['cases']) == 4
            and all(row['mass_relative_error'] == 0 and row['gram_relative_error'] == 0 for row in acquisition['cases']))
        check('weighted_probe_not_physical_force_claim', weak['weighted_forms_precision_qualified']
            and weak['frozen_source_force_derived_probe_not_dynamic_force_budget']
            and weak['original_physical_force_mismatch_unchanged'])
        for branch in ['reference', 'MTS']:
            prior = next(row for row in strict['cases'] if row['branch'] == branch and row['comparison'] == 'spatial64' and row['digits'] == 48)
            tolerance = Decimal(prior['unchanged_numerical_tolerance'])
            rows = [row for row in weak['refinement'] if row['branch'] == branch]
            check(branch+'_literal_predecessor_gate_for_all_refinements', len(rows) == 4
                and all(row['literal_gate_pass'] and Decimal(row['maximum_channel_change']) <= tolerance
                    and Decimal(row['literal_predecessor_gate']) == tolerance for row in rows))
            rows = [row for row in weak['channels'] if row['branch'] == branch]
            for row in rows:
                keys = ['fine_native_quadrature_and_basis', 'legacy_sampler_arithmetic', 'representation_alias',
                    'geometry_weight_difference', 'stencil_difference', 'coarse_native_quadrature_and_basis']
                total = sum((Decimal(row[key]) for key in keys), Decimal(0))
                check(branch+'_'+row['sector']+'_'+str(row['order'])+'_six_term_telescope',
                    abs(total-Decimal(row['native_difference'])) <= tolerance)
            witness = next(row for row in independent['cases'] if row['branch'] == branch and row['control'] == 'erased_basis_265_weighted_witness')
            check(branch+'_weighted_information_loss_witness', Decimal(witness['weighted_mass']) > 0
                and Decimal(witness['weighted_gradient']) > 0 and Decimal(witness['fine_sampled_mass']) == 0
                and Decimal(witness['fine_sampled_gradient']) == 0)
            direct = [row for row in independent['cases'] if row['branch'] == branch and row['control'].startswith('independent_direct_')]
            check(branch+'_two_independent_integrals', len(direct) == 2 and all(Decimal(row['error']) <= tolerance for row in direct))
        rows_by_table = [acquisition['cases'], weak['cases'], weak['channels'], weak['regions'], weak['controls'], weak['refinement'], independent['cases']]
        source_indices = [0, 1, 1, 1, 1, 1, 2]
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
        note = root/'DERIVATION-20260920-original-weighted-action-on-common-cells.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv))`', content)
        check('report_finished_and_cited_paths_exist', 'RESULTS_PENDING' not in content
            and bool(cited) and all((root/name).is_file() for name in cited), cited)
        own(note)
        for name in ['acquire_annular_common_action_weights_20260920.py', 'annular_common_weighted_moments_20260920.py',
                'derive_annular_common_weak_action_20260920.py', 'validate_annular_common_weak_action_20260920.py',
                'seal_annular_common_weak_action_20260920.py']:
            source = root/'scripts'/name
            compile(source.read_bytes(), str(source), 'exec')
            own(source)
        check('sources_compile_no_bytecode', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026, 9, 19, 23, 0, 47, tzinfo=timezone.utc).timestamp()
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
            weighted_probe_precision_qualified=True,
            next_target='assemble common mixed mass B_fc and stiffness S_fc; validate rank-safe commutator split and integrate against actual frozen primal/adjoint paths with native closures retained')
        save()
        print(json.dumps(dict(state='complete', checks=report['implementation_checks'], integrity_checks=len(report['checks']),
            files_rehashed=len(cache), table_rows=report['table_rows'], failures_preserved=report['total_failed_attempts_preserved'])), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
