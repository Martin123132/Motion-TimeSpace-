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
    destination = intake/'annular-P2-Gram-force-mesh-final-integrity.json'
    table = intake/'annular-P2-Gram-force-mesh-results.csv'
    snapshot = intake/'annular-P2-Gram-force-mesh-resume-snapshot.md'
    executed = intake/'annular-P2-Gram-force-mesh-executed-sealer.py'
    if any(path.exists() for path in [destination, table, snapshot, executed]):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, github_action=False,
        subagents_used=False, full_GR_limit_proven=False, valid_for_physics_claim=False,
        full_live_P2_force_convergence_proven=False, no_new_live_evolution=True,
        protected_scan_scope='mtime since2026-09-19T05:36:32Z; not a pre-turn full hash baseline')
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

    save()
    try:
        previous = inherit(intake/'annular-P2-bulk-Gram-final-integrity.json')
        check('all_previous_sources_and_failures_preserved', previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks']) and previous['total_failed_attempts_preserved'] == 37)
        names = ['annular-P2-local-Gram-bound-attempt01', 'annular-P2-Gram-source-reaction-attempt01',
            'annular-P2-Gram-force-mesh-law-attempt01', 'annular-P2-front-projected-Gram-attempt01',
            'annular-P2-Gram-recovery-budget-attempt01']
        statuses = {}
        for name in names:
            data = inherit(intake/name/'status.json')
            statuses[name] = data
            check(name+'_complete', data['state'] == 'complete' and all(row['passed'] for row in data['checks']))
            check(name+'_nonclaim_and_private', not data['valid_for_physics_claim'] and not data['full_GR_limit_proven']
                and not data['full_live_P2_force_convergence_proven'] and not data['github_action'] and not data['subagents_used'])
        count = sum(len(data['checks']) for data in statuses.values())
        check('implementation_check_count', count == 166, count)
        local = statuses[names[0]]
        reaction = statuses[names[1]]
        law = statuses[names[2]]
        front = statuses[names[3]]
        budget = statuses[names[4]]
        check('two_reference_controls_are_retained', len(local['cases']) == 4
            and sum(row['branch'] == 'reference' and row['explicit_drive'] == 0 for row in local['cases']) == 2)
        check('no_rows_discarded_or_reaction_fitted', all(row['all_rows_retained'] and row['no_small_hinge_tail_discarded']
            for row in local['cases']) and reaction['no_new_fitted_coupling'] and reaction['no_Gram_terms_removed'])
        check('force_mesh_fixture_scope_explicit', law['constant_weight_local_projection_fixture']
            and law['not_a_parent_trajectory_or_force_replacement'] and law['no_terms_deleted_from_actual_parent_action']
            and len(law['cases']) == 21 and {row['source_power'] for row in law['cases']} == {1, 2, 3})
        check('front_test_scope_explicit', front['source_and_two_fronts_fitted_in_scalar_mesh']
            and front['wider_Gram_stencil_still_uses_uniform_base_vertices']
            and front['actual_parent_front_resolution_not_yet_tested'] and len(front['cases']) == 9)
        check('no_blind_large_uniform_job_or_force_subtraction', budget['no_large_uniform_run_launched']
            and budget['prospective_count_not_allocated_or_authorized']
            and budget['full_force_not_replaced_by_Gram_subtraction'])
        closures = []
        for row in budget['cases']:
            closure = abs(row['force_error_signed']-row['reconstructed_error'])
            adjusted = row['absolute_error_bound']+closure
            check(row['branch']+str(row['base_count'])+'_evaluated_bound_includes_closure',
                abs(row['force_error_signed']) <= adjusted+2e-23)
            closures.append(dict(branch=row['branch'], base_count=row['base_count'],
                finite_precision_closure=closure, evaluated_bound_plus_closure=adjusted,
                rigorous_interval_certificate=False))
        fields = ['kind', 'branch', 'base_count', 'spacing', 'source_power', 'source_cap',
            'force', 'source_force', 'Gram_energy', 'bound', 'source_stencil_front_resolved', 'valid_for_claim', 'source_path']
        rows = []
        for row in local['cases']:
            rows.append(dict(kind='saved_live_Gram_drive', branch=row['branch'], base_count=row['base_count'],
                spacing=row['bulk_spacing'], source_cap=row['source_cap'], force=row['explicit_drive'],
                source_force=row['groups'][0]['projected_sum'], bound=row['drive_partitioned_bound'],
                valid_for_claim=False, source_path=str((intake/names[0]/'status.json').relative_to(root))))
        for row in law['cases']:
            rows.append(dict(kind='local_quadratic_projection_fixture', spacing=row['spacing'], source_power=row['source_power'],
                force=row['direct_force'], Gram_energy=row['Gram_energy'], valid_for_claim=False,
                source_path=str((intake/names[2]/'status.json').relative_to(root))))
        for row in front['cases']:
            rows.append(dict(kind='local_front_projection_fixture', spacing=row['spacing'], force=row['total_projected_force'],
                source_force=row['source_force'], Gram_energy=row['Gram_energy'], bound=row['absolute_row_bound'],
                source_stencil_front_resolved=row['source_stencil_front_resolved'], valid_for_claim=False,
                source_path=str((intake/names[3]/'status.json').relative_to(root))))
        with table.open('w', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        with table.open(encoding='utf-8', newline='') as stream:
            parsed = list(csv.DictReader(stream))
        check('34_sourced_nonclaim_CSV_rows', len(parsed) == 34 and all(None not in row
            and (root/row['source_path']).is_file() and row['valid_for_claim'] == 'False'
            and all(not row[key] or math.isfinite(float(row[key])) for key in
                ['spacing', 'force', 'source_force', 'Gram_energy', 'bound']) for row in parsed))
        own(table, 'outputs')
        note = root/'DERIVATION-20260919-localized-Gram-reaction-and-force-mesh-law.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv))`', content)
        check('all_cited_local_paths_exist', bool(cited) and all((root/name).is_file() for name in cited), cited)
        check('report_avoids_scope_inflation', 'does not establish the full GR limit' in content
            and 'No new live trajectory was evolved' in content and '166 implementation checks' in content
            and 'not interval-arithmetic or continuous-time certificates' in content)
        own(note)
        scripts = ['annular_P2_Gram_row_bounds_20260919.py', 'derive_annular_P2_local_Gram_bound_20260919.py',
            'derive_annular_P2_Gram_source_reaction_20260919.py', 'derive_annular_P2_Gram_force_mesh_law_20260919.py',
            'test_annular_P2_front_projected_Gram_20260919.py', 'derive_annular_P2_Gram_recovery_budget_20260919.py',
            'seal_annular_P2_Gram_force_mesh_20260919.py']
        for name in scripts:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('sources_compile_without_bytecode', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026, 9, 19, 5, 36, 32, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= start]
        check('protected_mtime_changed_count_zero', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(), implementation_checks=count,
            total_failed_attempts_preserved=37, new_failed_executions=0, inherited_scientific_failures_unchanged=True,
            distinct_files_rehashed=len(cache), full_interval_retested=False,
            evaluated_traction_bounds_with_closure=closures, result_rows=len(rows),
            prospective_uniform_base_count=budget['prospective_uniform_base_count'])
        save()
        print(json.dumps(dict(state='complete', implementation_checks=count, integrity_checks=len(report['checks']),
            files_rehashed=len(cache), results=len(rows))), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
