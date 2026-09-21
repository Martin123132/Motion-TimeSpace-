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
    destination = intake/'annular-P2-weighted-consistency-final-integrity.json'
    table = intake/'annular-P2-weighted-consistency-results.csv'
    snapshot = intake/'annular-P2-weighted-consistency-resume-snapshot.md'
    executed = intake/'annular-P2-weighted-consistency-executed-sealer.py'
    if any(path.exists() for path in [destination, table, snapshot, executed]):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, github_action=False,
        subagents_used=False, full_GR_limit_proven=False, valid_for_physics_claim=False,
        full_live_P2_force_convergence_proven=False, no_new_live_evolution=True,
        protected_scan_scope='mtime since2026-09-19T06:10:38Z; not a pre-turn full hash baseline')
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
        previous = inherit(intake/'annular-P2-Gram-force-mesh-final-integrity.json')
        check('previous_checkpoint_preserved', previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks']) and previous['total_failed_attempts_preserved'] == 37)
        names = ['annular-P2-variable-geometry-consistency-attempt01',
            'annular-P2-live-weighted-projection-attempt04', 'annular-P2-Gram-trajectory-defect-attempt01']
        statuses = {}
        for name in names:
            status = inherit(intake/name/'status.json')
            statuses[name] = status
            check(name+'_complete', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
            check(name+'_nonclaim_and_private', not status['valid_for_physics_claim'] and not status['full_GR_limit_proven']
                and not status['full_live_P2_force_convergence_proven'] and not status['github_action'] and not status['subagents_used'])
        failures = []
        for attempt in [1, 2, 3]:
            name = 'annular-P2-live-weighted-projection-attempt'+str(attempt).zfill(2)
            failed = inherit(intake/name/'status.json')
            check(name+'_failed_execution_preserved', failed['state'] == 'failed')
            failures.append(dict(folder=name, error=failed['error']))
        fixture, live, defect = [statuses[name] for name in names]
        count = sum(len(status['checks']) for status in statuses.values())
        check('256_current_successful_implementation_checks', count == 256, count)
        check('fixture_is_variable_geometry_not_a_parent_trajectory', fixture['positive_variable_metric_fixture']
            and fixture['actual_nonrigid_source_map_retained'] and fixture['no_wavefront_fitting_in_this_test']
            and fixture['theorem_for_interpolants_not_a_stability_theorem'] and len(fixture['cases']) == 30)
        check('live_audit_covers_both_branches_and_same_windows', len(live['cases']) == 4
            and live['common_source_window_used_for_zero_Gram_reference']
            and live['finite_quadrature_weight_certificate_not_continuous_supremum']
            and live['left_endpoint_atom_excluded_because_initial_slope_is_right_trace'])
        check('trajectory_defect_is_not_a_continuum_error_estimate', len(defect['cases']) == 2
            and defect['hierarchical_field_difference_not_known_continuum_error']
            and defect['full_geometry_feedback_difference_not_in_this_split']
            and defect['actual_Gram_and_cross_terms_retained'])
        rows = []
        for item in fixture['cases']:
            rows.append(dict(kind='prescribed_variable_metric_fixture', branch=item['branch'], base_count=item['base_count'],
                source_power=item['source_power'], source_displacement=item['source_displacement'],
                drive=item['exact_drive'], bound=item['a_priori_bound']['total_bound'],
                coefficient_variation=item['measured_cell_weight_variation'],
                mass_contraction=item['measured_mass_contraction'], valid_for_claim=False,
                source_path=str((intake/names[0]/'status.json').relative_to(root))))
        for item in live['cases']:
            rows.append(dict(kind='actual_saved_live_projection', branch=item['branch'], base_count=item['base_count'],
                drive=item['actual_explicit_Gram_drive'], coefficient_variation=item['discrete_cell_weight_variation'],
                mass_contraction=item['mass_contraction'], source_curvature=item['source_neighbourhood_maximum_element_curvature'],
                source_gradient_jump_variation=item['source_neighbourhood_ordinary_jump_variation'], valid_for_claim=False,
                source_path=str((intake/names[1]/'status.json').relative_to(root))))
        for item in defect['cases']:
            rows.append(dict(kind='hierarchical_field_defect_at_fixed_geometry', branch=item['branch'], base_count=item['fine_count'],
                drive=item['measured_difference'], bound=sum(row['absolute_row_bound'] for row in item['components']),
                field_difference=item['field_nodal_maximum_difference'], valid_for_claim=False,
                source_path=str((intake/names[2]/'status.json').relative_to(root))))
        fields = ['kind', 'branch', 'base_count', 'source_power', 'source_displacement', 'drive', 'bound',
            'coefficient_variation', 'mass_contraction', 'source_curvature', 'source_gradient_jump_variation',
            'field_difference', 'valid_for_claim', 'source_path']
        with table.open('w', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        with table.open(encoding='utf-8', newline='') as stream:
            parsed = list(csv.DictReader(stream))
        check('36_sourced_nonclaim_rows_parse', len(parsed) == 36 and all(None not in row
            and row['valid_for_claim'] == 'False' and (root/row['source_path']).is_file()
            and all(not row[key] or math.isfinite(float(row[key])) for key in fields
                if key not in ['kind', 'branch', 'valid_for_claim', 'source_path']) for row in parsed))
        own(table, 'outputs')
        note = root/'DERIVATION-20260919-variable-geometry-Gram-consistency.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv))`', content)
        check('all_cited_local_paths_exist', bool(cited) and all((root/name).is_file() for name in cited), cited)
        check('scope_and_failures_are_disclosed', 'does not establish the full GR limit' in content
            and 'Three failed executions are preserved' in content and '256 implementation checks' in content
            and '13.58%' in content and 'not an estimate of the unknown exact continuum error' in content)
        own(note)
        for name in ['annular_P2_weighted_projection_bounds_20260919.py',
                'derive_annular_P2_weighted_consistency_20260919.py',
                'derive_annular_P2_live_weighted_projection_v2_20260919.py',
                'derive_annular_P2_live_weighted_projection_v3_20260919.py',
                'derive_annular_P2_live_weighted_projection_v4_20260919.py',
                'derive_annular_P2_Gram_trajectory_defect_20260919.py',
                'seal_annular_P2_weighted_consistency_20260919.py']:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        original = root/'scripts/derive_annular_P2_live_weighted_projection_20260919.py'
        failed_as_expected = False
        try:
            compile(original.read_bytes(), str(original), 'exec')
        except SyntaxError:
            failed_as_expected = True
        own(original)
        check('original_syntax_failure_not_silently_overwritten', failed_as_expected)
        check('working_sources_compile_without_bytecode', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026, 9, 19, 6, 10, 38, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= start]
        check('protected_mtime_changed_count_zero', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(),
            implementation_checks=count, total_failed_attempts_preserved=40, new_failed_executions=3,
            new_failures=failures, inherited_scientific_failures_unchanged=True,
            distinct_files_rehashed=len(cache), full_interval_retested=False, result_rows=len(rows))
        save()
        print(json.dumps(dict(state='complete', implementation_checks=count, integrity_checks=len(report['checks']),
            files_rehashed=len(cache), total_failed_attempts_preserved=40, results=len(rows))), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
