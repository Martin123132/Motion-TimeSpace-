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
    destination = intake/'annular-wave-energy-final-integrity.json'
    snapshot = intake/'annular-wave-energy-resume-snapshot.md'
    executed = intake/'annular-wave-energy-executed-sealer.py'
    tables = [intake/('annular-wave-energy-'+name+'.csv') for name in ['algebra', 'snapshots', 'rates', 'initial-jet', 'jet-controls']]
    if any(path.exists() for path in [destination, snapshot, executed]+tables):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, github_action=False, subagents_used=False,
        valid_for_physics_claim=False, full_GR_limit_proven=False, full_live_P2_force_convergence_proven=False,
        no_new_trajectory_evolution=True, full_nonlinear_stability_proven=False,
        derivative_convergence_certified=False, uniform_time_error_control_proven=False,
        original_source_Dirichlet_condition_unchanged=True, continuum_mismatch_resolved=False,
        protected_scan_scope='mtime since2026-09-19T14:03:20Z; not a pre-turn whole-tree hash baseline')
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
        previous = inherit(intake/'annular-compensated-canonical-driver-final-integrity.json')
        check('previous_seal_and43failures_preserved', previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks']) and previous['total_failed_attempts_preserved'] == 43)
        names = ['annular-wave-error-energy-algebra-attempt01', 'annular-live-wave-error-energy-attempt01',
            'annular-wave-initial-jet-split-attempt01']
        statuses = []
        for name in names:
            status = inherit(intake/name/'status.json')
            statuses.append(status)
            check(name+'_complete_nonclaim_private', status['state'] == 'complete'
                and all(row['passed'] for row in status['checks']) and not status['valid_for_physics_claim']
                and not status['full_GR_limit_proven'] and not status['full_live_P2_force_convergence_proven']
                and not status['github_action'] and not status['subagents_used'])
        failures = []
        for prefix in ['annular-wave-error-energy-algebra-', 'annular-live-wave-error-energy-', 'annular-wave-initial-jet-split-']:
            for path in sorted(intake.glob(prefix+'*/status.json')):
                if path.parent.name not in names:
                    failed = inherit(path)
                    check(path.parent.name+'_failed_attempt_preserved', failed['state'] == 'failed')
                    failures.append(dict(folder=path.parent.name, error=failed['error']))
        check('no_new_failed_execution', not failures)
        count = sum(len(status['checks']) for status in statuses)
        check('146_successful_implementation_checks', count == 146, count)
        sources = [str((intake/name/'status.json').relative_to(root)) for name in names]
        rows_by_table = [
            [dict(**row, source_path=sources[0], units='synthetic_fixture') for row in statuses[0]['cases']],
            [dict(**row, source_path=sources[1], units='normalized_annular_energy') for row in statuses[1]['energy_snapshots']],
            [dict(**row, source_path=sources[1], units='normalized_annular_energy_rate') for row in statuses[1]['cases']],
            [dict(**row, source_path=sources[2], units='normalized_annular_energy_rate') for row in statuses[2]['cases']],
            [dict(**row, source_path=sources[2], units='synthetic_fixture') for row in statuses[2]['controls']]]
        check('expected_table_rows', [len(rows) for rows in rows_by_table] == [4, 4, 8, 8, 4])
        for path, rows in zip(tables, rows_by_table):
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
        check('both_branches_initial_final_snapshots', {(row['branch'], row['time']) for row in statuses[1]['energy_snapshots']}
            == {('reference', 0.), ('reference', 4e-5), ('MTS', 0.), ('MTS', 4e-5)})
        check('full_action_geometry_source_and_nonclaim_scope', statuses[1]['full_geometry_reconstructed']
            and statuses[1]['all_scalar_modes_retained'] and statuses[1]['all_Gram_rows_retained']
            and statuses[1]['original_source_condition_retained'] and statuses[1]['no_new_evolution']
            and statuses[1]['rates_are_finite_difference_estimates']
            and statuses[1]['total_scalar_energy_not_total_gravity_Hamiltonian']
            and statuses[1]['nonnested_interpolation_not_exact_function_inclusion'])
        expected_pairs = {(branch, step) for branch in ['MTS', 'reference'] for step in [2e-7, 1e-7, 5e-8, 2.5e-8]}
        check('both_branches_all_four_probes', {(row['branch'], row['tangent_step']) for row in statuses[1]['cases']} == expected_pairs
            and {(row['branch'], row['tangent_step']) for row in statuses[2]['cases']} == expected_pairs)
        channels = ['gradient_stiffness_transfer', 'Gram_stiffness_transfer', 'source_kinetic', 'cross_transport',
            'source_acceleration', 'mass_transport', 'inverse_residual']
        for row in statuses[1]['cases']:
            tag = row['branch']+'_'+str(row['tangent_step'])
            check(tag+'_full_energy_decomposition', abs(row['total']-row['kinetic']-row['gradient']-row['Gram']) < 1e-24
                and min(row[name] for name in ['kinetic', 'gradient', 'Gram']) >= 0.)
            check(tag+'_exchange_cancels_but_residual_retained',
                abs(row['conservative_kinetic_work']+row['potential_exchange_rate']) < 1e-24
                and abs(sum(row[name] for name in channels)-row['residual_work']) < 1e-20
                and abs(row['full_wave_energy_rate']-row['residual_work']-row['mass_geometry_rate']-row['stiffness_geometry_rate']) < 1e-23
                and row['rate_comparison_error'] <= row['numerical_control_tolerance']
                and abs(row['full_wave_energy_rate']) <= row['localized_rate_bound']+1e-24)
            jet = next(item for item in statuses[2]['cases'] if item['branch'] == row['branch'] and item['tangent_step'] == row['tangent_step'])
            check(tag+'_initial_jet_cross_terms_retained', jet['baseline_energy'] >= 0. and jet['increment_energy'] >= 0.
                and abs(row['total']-jet['baseline_energy']-jet['increment_energy']-jet['cross_energy']) < 1e-23
                and abs(row['full_wave_energy_rate']-jet['baseline_rate']-jet['increment_rate']-jet['cross_rate']) < 1e-21)
        check('initial_jet_not_a_replacement_physical_solution', statuses[2]['diagnostic_baseline_not_a_physical_solution']
            and statuses[2]['both_initial_displacement_and_velocity_retained'] and statuses[2]['cross_energy_not_dropped']
            and statuses[2]['original_hierarchy_error_not_replaced'])
        note = root/'DERIVATION-20260919-wave-energy-and-Gram-transfer-defect.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv))`', content)
        check('all_cited_local_paths_exist', bool(cited) and all((root/name).is_file() for name in cited), cited)
        check('claim_limits_and_initial_floor_disclosed', all(phrase in content for phrase in [
            'does not establish the full GR limit', '12.5718%', '13.58%', 'NOT monotone',
            'finite-difference estimates, not certified derivatives', 'not a pre-turn whole-tree hash baseline',
            'not146 independent confirmations', '97.47%', 'initial velocity would be incorrect']))
        own(note)
        for name in ['annular_wave_error_energy_20260919.py', 'validate_annular_wave_error_energy_20260919.py',
                'derive_annular_live_wave_error_energy_20260919.py', 'derive_annular_wave_initial_jet_split_20260919.py',
                'seal_annular_wave_energy_20260919.py']:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('sources_compile_without_bytecode', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026, 9, 19, 14, 3, 20, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= start]
        check('protected_mtime_changed_count_zero', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(), implementation_checks=count,
            total_failed_attempts_preserved=43+len(failures), new_failures=failures, distinct_files_rehashed=len(cache),
            table_rows=[len(rows) for rows in rows_by_table], full_interval_retested=False,
            next_target='weak Gram-force transfer consistency with actual mass-adjoint tests and source/remaining row split')
        save()
        print(json.dumps(dict(state='complete', implementation_checks=count, integrity_checks=len(report['checks']),
            files_rehashed=len(cache), failed_attempts_preserved=43+len(failures), table_rows=report['table_rows'])), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
