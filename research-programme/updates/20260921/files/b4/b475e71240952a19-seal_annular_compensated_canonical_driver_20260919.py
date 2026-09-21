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
    destination = intake/'annular-compensated-canonical-driver-final-integrity.json'
    snapshot = intake/'annular-compensated-canonical-driver-resume-snapshot.md'
    executed = intake/'annular-compensated-canonical-driver-executed-sealer.py'
    tables = [intake/('annular-compensated-canonical-'+name+'.csv') for name in
        ['driver-algebra', 'driver', 'rate-algebra', 'rate', 'energy', 'energy-bound', 'energy-controls']]
    if any(path.exists() for path in [destination, snapshot, executed]+tables):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, github_action=False, subagents_used=False,
        valid_for_physics_claim=False, full_GR_limit_proven=False, full_live_P2_force_convergence_proven=False,
        no_new_trajectory_evolution=True, full_nonlinear_stability_proven=False,
        derivative_convergence_certified=False, uniform_time_error_control_proven=False,
        new_physical_couplings_introduced=False, original_source_Dirichlet_condition_unchanged=True,
        protected_scan_scope='mtime since2026-09-19T13:37:35Z; not a pre-turn whole-tree hash baseline')
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
        keys = list(dict.fromkeys(key for row in rows for key in row))
        with path.open('w', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=keys)
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
        previous = inherit(intake/'annular-coefficient-bounds-rate-final-integrity.json')
        check('previous_seal_and43failures_preserved', previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks']) and previous['total_failed_attempts_preserved'] == 43)
        names = ['annular-canonical-driver-algebra-attempt01', 'annular-live-canonical-driver-attempt01',
            'annular-compensated-rate-algebra-attempt01', 'annular-live-compensated-rate-attempt01',
            'annular-compensated-energy-bound-attempt01']
        statuses = []
        for name in names:
            status = inherit(intake/name/'status.json')
            statuses.append(status)
            check(name+'_complete_nonclaim_private', status['state'] == 'complete'
                and all(row['passed'] for row in status['checks']) and not status['valid_for_physics_claim']
                and not status['full_GR_limit_proven'] and not status['full_live_P2_force_convergence_proven']
                and not status['github_action'] and not status['subagents_used'])
        failures = []
        for prefix in ['annular-canonical-driver-algebra-', 'annular-live-canonical-driver-',
                'annular-compensated-rate-algebra-', 'annular-live-compensated-rate-', 'annular-compensated-energy-bound-']:
            for path in sorted(intake.glob(prefix+'*/status.json')):
                if path.parent.name not in names:
                    failed = inherit(path)
                    check(path.parent.name+'_failed_attempt_preserved', failed['state'] == 'failed')
                    failures.append(dict(folder=path.parent.name, error=failed['error']))
        check('no_new_failed_execution', len(failures) == 0)
        count = sum(len(status['checks']) for status in statuses)
        check('300_successful_implementation_checks', count == 300, count)
        sources = [str((intake/name/'status.json').relative_to(root)) for name in names]
        driver_algebra = [dict(**row, source_path=sources[0], units='synthetic_fixture') for row in statuses[0]['cases']]
        driver = [dict(branch=case['branch'], time=case['time'], **row, source_path=sources[1], units='normalized_annular')
            for case in statuses[1]['cases'] for row in case['rows']]
        rate_algebra = [dict(**row, source_path=sources[2], units='synthetic_fixture') for row in statuses[2]['cases']]
        rates = [dict(**row, source_path=sources[3], units='normalized_annular_rate')
            for case in statuses[3]['cases'] for row in case['rows']]
        energy = [dict(**row, source_path=sources[3], units='normalized_annular_energy_rate') for row in statuses[3]['energy_rows']]
        bounds = [{**row, 'input_artifact':row['source_path'], 'source_path':sources[4], 'units':'normalized_annular_energy_rate'}
            for row in statuses[4]['cases']]
        controls = [dict(**row, source_path=sources[4], units='synthetic_fixture') for row in statuses[4]['controls']]
        rows_by_table = [driver_algebra, driver, rate_algebra, rates, energy, bounds, controls]
        check('seven_distinct_table_destinations', len(tables) == 7 and len(set(tables)) == 7)
        check('expected_table_rows', [len(rows) for rows in rows_by_table] == [4, 36, 4, 72, 8, 8, 4])
        for path, rows in zip(tables, rows_by_table):
            write_table(path, rows)
        check('actual_driver_both_branches_initial_final', {(case['branch'], case['time']) for case in statuses[1]['cases']}
            == {('reference', 0.), ('reference', 4e-5), ('MTS', 0.), ('MTS', 4e-5)}
            and statuses[1]['no_new_evolution'] and statuses[1]['all_Gram_rows_retained']
            and statuses[1]['both_inverse_momentum_residuals_retained'] and statuses[1]['nonnested_transfer_jump_retained']
            and statuses[1]['momentum_covectors_not_nodally_interpolated'])
        for row in driver:
            tag = row['branch']+'_'+str(row['time'])+'_'+row['partition']+'_'+row['functional']
            component = sum(row[name] for name in ['momentum_channel', 'source_cross_channel', 'coarse_inverse_channel',
                'fine_inverse_channel', 'interpolation_jump_channel'])
            tolerance = row['numerical_control_tolerance']
            check(tag+'_combined_driver_identity_and_bounds', abs(component-row['direct_driver']) <= tolerance
                and abs(row['direct_driver']) <= row['total_localized_bound']+tolerance
                and abs(row['direct_driver']) <= row['total_mass_bound']+tolerance)
        check('four_full_state_probes_on_both_branches', {(case['branch'], case['tangent_step']) for case in statuses[3]['cases']}
            == {(branch, step) for branch in ['MTS', 'reference'] for step in [2e-7, 1e-7, 5e-8, 2.5e-8]}
            and statuses[3]['full_global_canonical_direction'] and statuses[3]['no_new_evolution']
            and statuses[3]['rates_are_finite_difference_estimates'] and statuses[3]['both_inverse_residual_rates_retained']
            and statuses[3]['nonnested_jump_rate_retained'] and statuses[3]['centered_identity_not_independent_physics_validation'])
        for case in statuses[3]['cases']:
            for functional in ['left', 'right', 'trace_weighted']:
                selected = {row['partition']:row for row in case['rows'] if row['functional'] == functional}
                check(case['branch']+'_'+str(case['tangent_step'])+'_'+functional+'_all_rows_retained',
                    abs(selected['all_rows']['compensated_driver_rate']-selected['source_straddling']['compensated_driver_rate']
                        -selected['remaining']['compensated_driver_rate']) < 1e-8*max(1., abs(selected['all_rows']['compensated_driver_rate'])))
        for row in rates:
            tag = row['branch']+'_'+str(row['tangent_step'])+'_'+row['partition']+'_'+row['functional']
            check(tag+'_rate_channels_control_and_bound',
                abs(row['compensated_driver_rate']-row['combined_acceleration_channel']-row['changing_functional_channel']
                    -row['transfer_jump_rate_channel']) < 1e-8*max(1., abs(row['compensated_driver_rate']))
                and row['comparison_error'] <= row['numerical_control_tolerance']
                and abs(row['compensated_driver_rate']) <= row['localized_absolute_bound']+1e-9)
        for row in bounds:
            check(row['branch']+'_'+str(row['tangent_step'])+'_conditional_energy_bound',
                abs(row['energy_rate']) <= row['energy_rate_absolute_bound']+1e-25
                and row['sampled_mass_relative_rate_bound'] >= 0. and row['energy'] > 0.
                and (root/row['input_artifact']).is_file())
        check('kinetic_growth_not_mislabeled_instability', statuses[4]['oscillator_control']['kinetic_growth'] > .4
            and abs(statuses[4]['oscillator_control']['total_growth']) < 1e-15
            and statuses[4]['no_time_uniform_certificate'])
        note = root/'DERIVATION-20260919-compensated-canonical-driver-and-energy.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv))`', content)
        check('all_cited_local_paths_exist', bool(cited) and all((root/name).is_file() for name in cited), cited)
        check('claim_limits_cancellation_and_roundoff_disclosed', all(phrase in content for phrase in [
            'does not establish the full GR limit', '12.5718%', '13.58%', 'NOT monotone',
            'finite-difference estimates, not certified derivatives', 'not a proved stability theorem',
            'NOT independent validation', 'not a pre-turn whole-tree hash baseline', '300 independent physics confirmations']))
        own(note)
        for name in ['annular_canonical_driver_residual_20260919.py', 'validate_annular_canonical_driver_residual_20260919.py',
                'derive_annular_live_canonical_driver_20260919.py', 'annular_compensated_momentum_rate_20260919.py',
                'validate_annular_compensated_momentum_rate_20260919.py', 'derive_annular_live_compensated_rate_20260919.py',
                'derive_annular_compensated_energy_bound_20260919.py', 'seal_annular_compensated_canonical_driver_20260919.py']:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('all_sources_compile_without_bytecode', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026, 9, 19, 13, 37, 35, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= start]
        check('protected_mtime_changed_count_zero', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(), implementation_checks=count,
            total_failed_attempts_preserved=43+len(failures), new_failures=failures, distinct_files_rehashed=len(cache),
            table_rows=[len(rows) for rows in rows_by_table], full_interval_retested=False,
            continuum_mismatch_resolved=False, next_target='kinetic-plus-potential spatial hierarchy energy and compensated stiffness-transfer residual')
        save()
        print(json.dumps(dict(state='complete', implementation_checks=count, integrity_checks=len(report['checks']),
            files_rehashed=len(cache), failed_attempts_preserved=43+len(failures), table_rows=report['table_rows'])), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
