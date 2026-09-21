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
    destination = intake/'annular-coefficient-bounds-rate-final-integrity.json'
    snapshot = intake/'annular-coefficient-bounds-rate-resume-snapshot.md'
    executed = intake/'annular-coefficient-bounds-rate-executed-sealer.py'
    tables = [intake/('annular-coefficient-bounds-'+name+'.csv') for name in ['algebra', 'field', 'geometry', 'rate', 'centered', 'centered-controls']]
    if any(path.exists() for path in [destination, snapshot, executed]+tables):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, github_action=False, subagents_used=False,
        valid_for_physics_claim=False, full_GR_limit_proven=False, full_live_P2_force_convergence_proven=False,
        no_new_trajectory_evolution=True, full_nonlinear_stability_proven=False,
        new_physical_couplings_introduced=False, original_source_Dirichlet_condition_unchanged=True,
        protected_scan_scope='mtime since2026-09-19T13:08:09Z; not a pre-turn full hash baseline')
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
        previous = inherit(intake/'annular-source-trace-force-law-final-integrity.json')
        check('previous_seal_and42failures_preserved', previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks']) and previous['total_failed_attempts_preserved'] == 42)
        names = ['annular-coefficient-geometry-algebra-attempt01', 'annular-live-coefficient-bounds-attempt02',
            'annular-live-coefficient-rate-MTS-attempt01', 'annular-live-coefficient-rate-reference-attempt01',
            'annular-centered-geometry-bound-attempt01']
        statuses = []
        for name in names:
            status = inherit(intake/name/'status.json')
            statuses.append(status)
            check(name+'_complete_nonclaim_private', status['state'] == 'complete'
                and all(row['passed'] for row in status['checks']) and not status['valid_for_physics_claim']
                and not status['full_GR_limit_proven'] and not status['full_live_P2_force_convergence_proven']
                and not status['github_action'] and not status['subagents_used'])
        failures = []
        for prefix in ['annular-coefficient-geometry-algebra-', 'annular-live-coefficient-bounds-',
                'annular-live-coefficient-rate-', 'annular-centered-geometry-bound-']:
            for path in sorted(intake.glob(prefix+'*/status.json')):
                if path.parent.name not in names:
                    failed = inherit(path)
                    check(path.parent.name+'_failed_attempt_preserved', failed['state'] == 'failed')
                    failures.append(dict(folder=path.parent.name, error=failed['error']))
        check('one_new_empty_reference_reduction_failure_preserved', len(failures) == 1
            and failures[0]['folder'] == 'annular-live-coefficient-bounds-attempt01')
        count = sum(len(status['checks']) for status in statuses)
        check('359_successful_implementation_checks', count == 359, count)
        source_paths = [str((intake/name/'status.json').relative_to(root)) for name in names]
        algebra = [dict(**row, source_path=source_paths[0], units='synthetic_fixture') for row in statuses[0]['cases']]
        field_rows, geometry_rows = [], []
        check('actual_bounds_both_branches_initial_final', {(case['branch'], case['time']) for case in statuses[1]['cases']}
            == {('reference', 0.), ('reference', 4e-5), ('MTS', 0.), ('MTS', 4e-5)}
            and statuses[1]['no_new_evolution'] and statuses[1]['all_Gram_rows_retained']
            and statuses[1]['ordinary_gradient_jumps_retained'] and statuses[1]['geometry_response_defect_retained']
            and statuses[1]['instantaneous_field_driver_not_total_time_derivative'])
        for case in statuses[1]['cases']:
            for row in case['field_rows']:
                field_rows.append(dict(branch=case['branch'], time=case['time'], **row,
                    source_path=source_paths[1], units='normalized_annular'))
            for row in case['geometry_rows']:
                geometry_rows.append(dict(branch=case['branch'], time=case['time'], **row,
                    source_path=source_paths[1], units='normalized_annular'))
        rates = []
        for index in [2, 3]:
            status = statuses[index]
            check(names[index]+'_full_direction_and_nonclaim_rate_scope', len(status['cases']) == 24
                and status['no_new_evolution'] and status['all_scalar_modes_retained']
                and status['full_global_canonical_direction'] and status['symmetric_tangent_probes_not_evolved_states']
                and status['rate_not_a_uniform_time_certificate'] and status['geometry_rates_finite_difference_not_certified_derivatives'])
            rates += [dict(branch=status['branch'], **row, source_path=source_paths[index], units='normalized_annular_rate')
                for row in status['cases']]
        centered = [dict(**row, source_path=source_paths[4], units='normalized_annular_rate') for row in statuses[4]['cases']]
        controls = [dict(**row, source_path=source_paths[4], units='synthetic_fixture') for row in statuses[4]['controls']]
        rows_by_table = [algebra, field_rows, geometry_rows, rates, centered, controls]
        check('six_distinct_table_destinations', len(tables) == 6 and len(set(tables)) == 6)
        check('expected_table_rows', [len(rows) for rows in rows_by_table] == [3, 36, 24, 48, 48, 3])
        for path, rows in zip(tables, rows_by_table):
            write_table(path, rows)
        for row in field_rows:
            tag = row['branch']+'_'+str(row['time'])+'_'+row['partition']+'_'+row['functional']
            check(tag+'_field_bounds_and_Peano_error_budget', abs(row['coefficient_channel']) <= row['rowwise_absolute_bound']+3e-20
                and abs(row['coefficient_channel']) <= row['weighted_energy_bound']+3e-20
                and abs(row['coefficient_channel']-row['curvature_channel']-row['ordinary_jump_channel']
                    -row['polynomial_moment_channel']) <= row['Peano_arithmetic_tolerance']+3e-20)
        for row in geometry_rows:
            tag = row['branch']+'_'+str(row['time'])+'_'+row['partition']+'_'+str(row['side'])
            check(tag+'_finite_geometry_identity_and_bound', abs(row['coefficient_change']-row['mass_response_pairing']
                -row['gram_weight_pairing']) < 3e-15
                and abs(row['mass_response_pairing']) <= row['localized_mass_bound']+3e-20
                and abs(row['mass_response_pairing']) <= row['weighted_projection_defect_bound']+3e-20)
        for row in rates:
            tag = row['branch']+'_'+row['partition']+'_'+str(row['side'])+'_'+str(row['tangent_step'])
            check(tag+'_rate_channels_and_conditional_bound', abs(row['coefficient_rate']-row['field_rate']-row['mass_response_rate']
                -row['Gram_weight_rate']) < 3e-15 and abs(row['coefficient_rate']) <= row['conditional_rate_bound']+3e-15
                and abs(row['coefficient_rate']) <= row['localized_rate_bound']+3e-15)
        for row in centered:
            tag = row['branch']+'_'+row['partition']+'_'+str(row['side'])+'_'+str(row['tangent_step'])
            check(tag+'_centered_bound_and_roundoff_correction', abs(row['direct_pairing']-row['centered_pairing']
                -row['floating_orthogonality_correction']) < 3e-18
                and abs(row['direct_pairing']) <= row['centered_absolute_bound']+3e-18)
        check('median_is_not_a_physical_fit', statuses[4]['weighted_median_is_bound_optimization_not_a_physical_fit']
            and statuses[4]['floating_orthogonality_residual_retained'] and statuses[4]['all_quadrature_terms_retained'])
        note = root/'DERIVATION-20260919-force-coefficient-bounds-and-live-rate.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv))`', content)
        check('all_cited_local_paths_exist', bool(cited) and all((root/name).is_file() for name in cited), cited)
        check('remaining_gaps_and_failure_disclosed', all(phrase in content for phrase in [
            'does not establish the full GR limit', '12.5718%', '13.58%', 'NOT monotone',
            'finite-difference estimates, not certified derivatives', 'max(empty)',
            'not a uniform bound', 'useful numerical bound has not yet been tested',
            'not a pre-turn whole-tree hash baseline']))
        own(note)
        for name in ['annular_force_coefficient_bounds_20260919.py', 'validate_annular_coefficient_geometry_law_20260919.py',
                'derive_annular_live_coefficient_bounds_20260919.py', 'derive_annular_live_coefficient_bounds_v2_20260919.py',
                'derive_annular_live_coefficient_rate_20260919.py', 'derive_annular_centered_geometry_bound_20260919.py',
                'seal_annular_coefficient_bounds_rate_20260919.py']:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('all_sources_compile_without_bytecode', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026, 9, 19, 13, 8, 9, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= start]
        check('protected_mtime_changed_count_zero', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(), implementation_checks=count,
            total_failed_attempts_preserved=42+len(failures), new_failures=failures, distinct_files_rehashed=len(cache),
            table_rows=[len(rows) for rows in rows_by_table], geometry_rates_are_finite_difference_estimates=True,
            direct_rate_probe_convergence_certified=False, uniform_time_error_control_proven=False,
            full_interval_retested=False, continuum_mismatch_resolved=False)
        save()
        print(json.dumps(dict(state='complete', implementation_checks=count, integrity_checks=len(report['checks']),
            files_rehashed=len(cache), failed_attempts_preserved=42+len(failures), table_rows=report['table_rows'])), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
