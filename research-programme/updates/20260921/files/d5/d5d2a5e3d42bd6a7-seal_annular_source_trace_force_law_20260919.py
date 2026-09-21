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
    destination = intake/'annular-source-trace-force-law-final-integrity.json'
    snapshot = intake/'annular-source-trace-force-law-resume-snapshot.md'
    executed = intake/'annular-source-trace-force-law-executed-sealer.py'
    tables = [intake/('annular-source-trace-'+name+'.csv') for name in ['algebra', 'commutator', 'response', 'force-law']]
    if any(path.exists() for path in [destination, snapshot, executed]+tables):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, github_action=False, subagents_used=False,
        valid_for_physics_claim=False, full_GR_limit_proven=False, full_live_P2_force_convergence_proven=False,
        no_new_trajectory_evolution=True, full_nonlinear_stability_proven=False,
        new_physical_couplings_introduced=False, original_source_Dirichlet_condition_unchanged=True,
        protected_scan_scope='mtime since2026-09-19T12:18:07Z; not a pre-turn full hash baseline')
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
        previous = inherit(intake/'annular-exponential-transport-final-integrity.json')
        check('previous_seal_and41failures_preserved', previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks']) and previous['total_failed_attempts_preserved'] == 41)
        names = ['annular-projection-commutator-algebra-attempt01', 'annular-spatial-projection-commutator-attempt01',
            'annular-projection-source-trace-attempt02', 'annular-Gram-two-trace-force-law-attempt01']
        statuses = []
        for name in names:
            status = inherit(intake/name/'status.json')
            statuses.append(status)
            check(name+'_complete_nonclaim_private', status['state'] == 'complete'
                and all(row['passed'] for row in status['checks']) and not status['valid_for_physics_claim']
                and not status['full_GR_limit_proven'] and not status['full_live_P2_force_convergence_proven']
                and not status['github_action'] and not status['subagents_used'])
        failures = []
        for prefix in ['annular-projection-commutator-algebra-', 'annular-spatial-projection-commutator-',
                'annular-projection-source-trace-', 'annular-Gram-two-trace-force-law-']:
            for path in sorted(intake.glob(prefix+'*/status.json')):
                if path.parent.name not in names:
                    failed = inherit(path)
                    check(path.parent.name+'_failed_attempt_preserved', failed['state'] == 'failed')
                    failures.append(dict(folder=path.parent.name, error=failed['error']))
        check('one_new_nominal_fraction_failure_preserved', len(failures) == 1
            and failures[0]['folder'] == 'annular-projection-source-trace-attempt01')
        count = sum(len(status['checks']) for status in statuses)
        check('238_successful_implementation_checks', count == 238, count)
        check('independent_nonzero_dense_controls', statuses[0]['independent_dense_mass_control']
            and statuses[0]['includes_nonzero_and_zero_controls'] and len(statuses[0]['cases']) == 10)
        all_tables = []
        for index, (name, status, path) in enumerate(zip(names, statuses, tables)):
            source_path = str((intake/name/'status.json').relative_to(root))
            if index == 0:
                rows = [dict(**item, source_path=source_path, units='synthetic_matrix_fixture') for item in status['cases']]
            else:
                check(name+'_both_branches_initial_and_final', {(case['branch'], case['time']) for case in status['cases']}
                    == {('reference', 0.), ('reference', 4e-5), ('MTS', 0.), ('MTS', 4e-5)}
                    and status['no_new_evolution'] and status['all_Gram_rows_retained'])
                rows = [dict(branch=case['branch'], time=case['time'], **part, source_path=source_path,
                    units='normalized_annular') for case in status['cases'] for part in case['partitions']]
            all_tables.append(rows)
            write_table(path, rows)
        check('expected_tabular_row_counts', [len(rows) for rows in all_tables] == [10, 12, 12, 24])
        for row in all_tables[1]:
            tag = row['branch']+'_'+str(row['time'])+'_'+row['partition']
            check(tag+'_commutator_and_complete_operator', abs(row['projection_force']-row['dual_residual_pairing']) < 3e-15
                and abs(row['projection_force']) <= row['dual_mass_bound']+3e-15
                and abs(row['projection_force']) <= row['dual_residual_absolute_bound']+3e-15
                and abs(row['operator_mesh_difference']-row['projection_force']-row['shape_weight_difference']
                    -row['transferred_stencil_difference']) < 3e-15)
        for row in all_tables[2]:
            tag = row['branch']+'_'+str(row['time'])+'_'+row['partition']
            check(tag+'_trace_remainder_retained', abs(row['full_projection_force']-row['trace_force']-row['remainder_force']) < 3e-15
                and abs(row['remainder_force']) <= row['remainder_localized_bound']+3e-15
                and abs(row['remainder_force']) <= row['remainder_dual_mass_bound']+3e-15)
        for row in all_tables[3]:
            tag = row['branch']+'_'+str(row['time'])+'_'+row['partition']+'_'+row['comparison']
            check(tag+'_four_force_channels', abs(row['difference']-row['trace_response_coefficient_channel']
                -row['source_trace_value_channel']-row['shape_weight_channel']-row['regular_projection_channel']) < 3e-15)
        for case in statuses[3]['cases']:
            for comparison in ['operator', 'field_without_nodal_transfer']:
                parts = {part['partition']:part for part in case['partitions'] if part['comparison'] == comparison}
                check(case['branch']+'_'+str(case['time'])+'_'+comparison+'_partitions_add', all(abs(parts['all_rows'][key]
                    -parts['source_straddling'][key]-parts['remaining'][key]) < 3e-15
                    for key in ['difference', 'trace_response_coefficient_channel', 'source_trace_value_channel',
                        'shape_weight_channel', 'regular_projection_channel']))
        check('corrected_coordinate_basis_and_unchanged_source_condition',
            statuses[2]['missing_source_basis_evaluated_at_actual_quadrature_coordinates']
            and statuses[2]['source_Dirichlet_condition_unchanged'] and statuses[2]['remainder_retained']
            and not statuses[2]['full_nonlinear_source_error_bound_derived'])
        note = root/'DERIVATION-20260919-source-trace-projection-and-force-law.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv))`', content)
        check('all_cited_local_paths_exist', bool(cited) and all((root/name).is_file() for name in cited), cited)
        check('nonclaim_and_failure_scope_disclosed', all(phrase in content for phrase in [
            'does not establish the full GR limit', '12.5718%', '13.58%', 'not an isolated spatial truncation error',
            'failed its constant-projection identity check', 'NOT newly introduced parent coupling constants',
            'numerical sharpness has NOT yet been tested', 'not an interval-arithmetic certificate']))
        own(note)
        for name in ['annular_Gram_projection_commutator_20260919.py', 'validate_annular_projection_commutator_20260919.py',
                'derive_annular_spatial_projection_commutator_20260919.py', 'derive_annular_projection_source_trace_20260919.py',
                'derive_annular_projection_source_trace_v2_20260919.py', 'derive_annular_Gram_two_trace_force_law_20260919.py',
                'seal_annular_source_trace_force_law_20260919.py']:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('all_sources_compile_without_bytecode', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026, 9, 19, 12, 18, 7, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= start]
        check('protected_mtime_changed_count_zero', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(), implementation_checks=count,
            total_failed_attempts_preserved=41+len(failures), new_failures=failures, distinct_files_rehashed=len(cache),
            algebra_rows=10, projection_rows=12, source_trace_rows=12, two_trace_force_rows=24,
            full_interval_retested=False, continuum_mismatch_resolved=False)
        save()
        print(json.dumps(dict(state='complete', implementation_checks=count, integrity_checks=len(report['checks']),
            files_rehashed=len(cache), failed_attempts_preserved=41+len(failures), table_rows=[len(rows) for rows in all_tables])), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
