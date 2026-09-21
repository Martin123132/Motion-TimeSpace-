from derive_annular_source_gravity_20260914 import EvidenceRun
from datetime import datetime, timezone
from pathlib import Path
import csv
import hashlib
import json
import re
import traceback


def main():
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    destination = intake/'annular-P2-bulk-Gram-final-integrity.json'
    table = intake/'annular-P2-bulk-Gram-results.csv'
    snapshot = intake/'annular-P2-bulk-Gram-resume-snapshot.md'
    executed = intake/'annular-P2-bulk-Gram-executed-sealer.py'
    if any(path.exists() for path in [destination, table, snapshot, executed]):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, github_action=False,
        subagents_used=False, full_GR_limit_proven=False, valid_for_physics_claim=False,
        full_live_P2_force_convergence_proven=False,
        protected_scan_scope='mtime since2026-09-19T03:16:28Z; not a pre-turn full hash baseline')
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
        previous = inherit(intake/'annular-P2-live-exponential-final-integrity.json')
        check('previous_checkpoint_and_all_sources_preserved', previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks']) and previous['total_failed_attempts_preserved'] == 37)
        names = ['annular-P2-Gram-jump-scale-attempt01', 'annular-P2-Gram-projected-drive-attempt01',
            'annular-P2-unresolved-front-Gram-attempt01',
            'annular-P2-bulk513-MTS-time128-attempt01']
        for branch in ['reference', 'MTS']:
            names.extend(['annular-P2-bulk513-'+stage+'-'+branch+'-attempt01'
                for stage in ['preflight', 'evolution', 'first-step']])
        statuses = {}
        for name in names:
            status = inherit(intake/name/'status.json')
            statuses[name] = status
            check(name+'_complete', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
            check(name+'_nonclaim_scope', not status['valid_for_physics_claim'] and not status['full_GR_limit_proven']
                and not status['full_live_P2_force_convergence_proven'] and not status['github_action']
                and not status['subagents_used'])
        rows = []
        scientific_misses = []
        further = statuses['annular-P2-bulk513-MTS-time128-attempt01']
        check('further_MTS_time_refinement_has_same_scope_and_budgets', further['steps'] == 128
            and further['duration'] == 4e-5 and further['base_count'] == 513 and further['source_cap'] == 1e-5
            and further['all_modes_and_Gram_retained'] and further['previous_point004_window_not_retested']
            and further['time_force_budget'] == 2e-9 and further['time_state_budget'] == 1e-6
            and further['endpoint_force_threshold'] == 2.700598122731542e-8)
        for flag in ['empirical_time_budget_pass', 'scoped_endpoint_gate_pass']:
            if not further[flag]:
                scientific_misses.append(dict(branch='MTS', stage='time128', flag=flag))
        drive = statuses['annular-P2-Gram-projected-drive-attempt01']
        check('projected_drive_split_not_a_modified_theory', drive['no_new_evolution']
            and drive['actual_live_geometry_tangent_held_for_algebraic_split']
            and drive['residual_drive_contains_implicit_Gram_geometry_feedback']
            and drive['removing_explicit_Gram_is_not_a_physical_counterfactual']
            and len(drive['cases']) == 4)
        front = statuses['annular-P2-unresolved-front-Gram-attempt01']
        check('front_fixture_not_promoted_to_parent_solution', front['no_live_evolution']
            and front['constant_coefficient_local_fixture_not_parent_solution']
            and front['energy_limit_not_force_limit'] and front['no_force_or_initial_data_replacement'])
        for branch in ['reference', 'MTS']:
            preflight = statuses['annular-P2-bulk513-preflight-'+branch+'-attempt01']
            evolved = statuses['annular-P2-bulk513-evolution-'+branch+'-attempt01']
            control = statuses['annular-P2-bulk513-first-step-'+branch+'-attempt01']
            check(branch+'_unaltered_preparation_and_gate', preflight['preparation_control']['coordinates'] == 0
                and preflight['preparation_control']['momenta'] < 2e-12
                and preflight['initial_force_threshold'] == 2.700598122731542e-8
                and evolved['endpoint_force_threshold'] == 2.700598122731542e-8)
            check(branch+'_scoped_actual_evolution', evolved['duration'] == 4e-5
                and evolved['previous_point004_window_not_retested'] and evolved['base_count'] == 513
                and evolved['source_cap'] == 1e-5 and evolved['all_scalar_modes_retained']
                and evolved['full_Gram_source_geometry_retained'] and [row['steps'] for row in evolved['cases']] == [32, 64])
            check(branch+'_control_scope_and_real_step_halving', control['duration'] == 4e-5/64
                and control['no_modal_split_in_RK'] and control['independent_first_step_only']
                and not control['independent_full_short_pilot_control']
                and control['cases'][0]['maximum_step'] == 2*control['cases'][1]['maximum_step'])
            check(branch+'_reported_time_difference', abs(evolved['cases'][0]['force']-evolved['cases'][1]['force'])
                == evolved['time_force_difference'] and evolved['time_force_budget'] == 2e-9
                and evolved['empirical_time_budget_pass'] == (evolved['time_force_difference'] < 2e-9
                    and evolved['time_state_difference'] < 1e-6))
            for key in ['empirical_time_budget_pass', 'scoped_endpoint_gate_pass']:
                if not evolved[key]:
                    scientific_misses.append(dict(branch=branch, stage='evolution', flag=key))
            if not control['independent_first_step_agreement_pass']:
                scientific_misses.append(dict(branch=branch, stage='first-step', flag='independent_first_step_agreement_pass'))
            for row in evolved['cases']+(further['cases'] if branch == 'MTS' else []):
                time_report = further if row['steps'] == 128 else evolved
                source_folder = 'annular-P2-bulk513-MTS-time128-attempt01' if row['steps'] == 128 else 'annular-P2-bulk513-evolution-'+branch+'-attempt01'
                rows.append(dict(branch=branch, base_count=513, source_cap=1e-5, duration=4e-5,
                    steps=row['steps'], force=row['force'], continuum_force=evolved['continuum_force'],
                    force_error=row['force_error'], instantaneous_relative_error=row['instantaneous_relative_force_error'],
                    waveform_error=row['field_error'], free_wave_drive=row['schur']['free_wave_drive'],
                    projection_inertia=row['schur']['field_projection_inertia'],
                    trace_pressure=row['lift']['trace_pressure'], bulk_lift=row['lift']['lift_bulk_work'],
                    combined_Gram_work=row['lift']['combined_Gram_work'],
                    source_touching_work=row['lift']['source_touching_work'],
                    paired_time_force_difference=time_report['time_force_difference'],
                    separate_64_scheme_first_step_agreement=control['independent_first_step_agreement_pass'],
                    valid_for_claim=False, full_interval_pass=False,
                    source_path=str((intake/source_folder/'status.json').relative_to(root))))
        with table.open('w', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        with table.open(encoding='utf-8', newline='') as stream:
            parsed = list(csv.DictReader(stream))
        check('five_sourced_nonclaim_CSV_rows', len(parsed) == 5 and all(None not in row
            and (root/row['source_path']).is_file() and row['valid_for_claim'] == 'False'
            and row['full_interval_pass'] == 'False' for row in parsed))
        own(table, 'outputs')
        note = root/'DERIVATION-20260919-bulk-Gram-source-jump-scaling-and-evolution.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv))`', content)
        check('all_cited_local_paths_exist', bool(cited) and all((root/name).is_file() for name in cited), cited)
        check('note_finished_without_inflating_scope', 'Results are pending' not in content
            and 'must be inserted here' not in content and 'not establish the full GR limit' in content)
        own(note)
        for name in ['annular_P2_bulk_refinement_20260919.py', 'probe_annular_P2_bulk_refinement_20260919.py',
                'run_annular_P2_bulk_refinement_20260919.py', 'derive_annular_P2_Gram_jump_scale_20260919.py',
                'check_annular_P2_bulk_first_step_20260919.py', 'refine_annular_P2_bulk_MTS_time_20260919.py',
                'derive_annular_P2_unresolved_front_Gram_20260919.py',
                'seal_annular_P2_bulk_Gram_20260919.py']:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        path = root/'scripts/derive_annular_P2_Gram_projected_drive_20260919.py'
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
        check('sources_compile_without_bytecode', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026, 9, 19, 3, 16, 28, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= start]
        check('protected_mtime_changed_count_zero', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(),
            implementation_checks=sum(len(status['checks']) for status in statuses.values()),
            total_failed_attempts_preserved=37, new_failed_executions=0,
            inherited_scientific_failures_unchanged=True, current_scientific_misses=scientific_misses,
            rows=rows, physical_Gram_scaling=statuses['annular-P2-Gram-jump-scale-attempt01']['physical_initial_controls'],
            projected_drive_results=drive['cases'],
            unresolved_front_fixture=front['cases'],
            distinct_files_rehashed=len(cache), full_interval_retested=False)
        save()
        print(json.dumps(dict(state='complete', implementation_checks=report['implementation_checks'],
            integrity_checks=len(report['checks']), files_rehashed=len(cache), scientific_misses=scientific_misses)), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
