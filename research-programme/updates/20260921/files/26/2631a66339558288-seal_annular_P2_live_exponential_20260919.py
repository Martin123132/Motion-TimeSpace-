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
    destination = intake/'annular-P2-live-exponential-final-integrity.json'
    snapshot = intake/'annular-P2-live-exponential-resume-snapshot.md'
    executed = intake/'annular-P2-live-exponential-executed-sealer.py'
    table = intake/'annular-P2-live-exponential-short-results.csv'
    spatial_table = intake/'annular-P2-evolved-source-halving-results.csv'
    if any(path.exists() for path in [destination, snapshot, executed, table, spatial_table]):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, github_action=False, subagents_used=False,
        full_GR_limit_proven=False, valid_for_physics_claim=False, full_live_P2_force_convergence_proven=False,
        protected_scan_scope='mtime since2026-09-18T23:34:00Z; not a pre-turn full hash baseline')
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

    def own(path, kind='inputs'):
        report[kind][str(path.resolve().relative_to(root))] = digest(path)

    def save():
        destination.write_text(json.dumps(report, indent=2, allow_nan=False)+'\n', encoding='utf-8')

    def check(name, passed, detail=None):
        report['checks'].append(dict(name=name, passed=bool(passed), detail=detail))
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def inherit(path):
        status = json.loads(path.read_text())
        for kind in ['inputs', 'outputs']:
            for name, expected in status[kind].items():
                source = (root/name).resolve()
                key = str(source.relative_to(root))
                if not source.is_file() or digest(source) != expected:
                    raise RuntimeError('Missing or changed sealed source: '+name)
                if key in report['inputs'] and report['inputs'][key] != expected:
                    raise RuntimeError('Conflicting sealed source: '+name)
                report['inputs'][key] = expected
        own(path)
        return status

    save()
    try:
        previous = inherit(intake/'annular-P2-joint-refinement-final-integrity.json')
        check('previous_seal_complete_and_preserved', previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks']))
        check('historical_failures_not_erased', previous['total_failed_attempts_preserved'] == 36
            and previous['inherited_peak_force_failures_preserved'] == 4
            and previous['inherited_short_horizon_scientific_failures_preserved'] == 6
            and previous['inherited_initial_force_failures_preserved'] == 4
            and previous['new_initial_gate_failures'] == 1)
        failure = inherit(intake/'annular-P2-live-exponential-algebra-attempt01/status.json')
        check('large_angle_validation_reference_failure_retained', failure['state'] == 'failed'
            and 'matrix_exponential_0.1' in failure['error'])
        names = ['annular-P2-live-exponential-algebra-attempt02',
            'annular-P2-live-exponential-reference-257-attempt01',
            'annular-P2-live-exponential-MTS-257-attempt01',
            'annular-P2-live-exponential-direct-reference-attempt01',
            'annular-P2-live-exponential-direct-reference-attempt02',
            'annular-P2-live-exponential-direct-MTS-attempt02',
            'annular-P2-indexed-live-geometry-attempt01',
            'annular-P2-indexed-full-pilot-control-reference-attempt01',
            'annular-P2-indexed-full-pilot-control-MTS-attempt01',
            'annular-P2-indexed-full-pilot-control-MTS-attempt02',
            'annular-P2-evolved-source-halving-reference-attempt01',
            'annular-P2-evolved-force-error-split-attempt01',
            'annular-P2-live-exponential-short-continuum-attempt01']
        mts_spatial_name = 'annular-P2-evolved-source-halving-MTS-attempt02'
        if (intake/mts_spatial_name/'status.json').exists():
            names.insert(-1, mts_spatial_name)
        statuses = {}
        for name in names:
            status = inherit(intake/name/'status.json')
            statuses[name] = status
            check(name+'_complete', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
            check(name+'_nonclaim_scope', not status['full_GR_limit_proven'] and not status['valid_for_physics_claim']
                and not status['full_live_P2_force_convergence_proven'] and not status['github_action'] and not status['subagents_used'])
        comparison = statuses[names[-1]]
        check('independent_short_comparison_not_full_window', comparison['duration'] == 4e-5
            and comparison['full_window_not_retested'] and comparison['finite_spatial_refinement_not_supplied'])
        rows = []
        for branch in ['reference', 'MTS']:
            status = statuses['annular-P2-live-exponential-'+branch+'-257-attempt01']
            control = statuses['annular-P2-live-exponential-direct-'+branch+'-attempt02']
            extended_initial = statuses['annular-P2-indexed-full-pilot-control-'+branch+'-attempt01']
            extended = statuses['annular-P2-indexed-full-pilot-control-'+branch+
                ('-attempt02' if branch == 'MTS' else '-attempt01')]
            final = next(row for row in comparison['results'] if row['branch'] == branch)
            check(branch+'_all_modes_live_equations_preserved', status['all_scalar_modes_retained']
                and status['live_geometry_recomputed_at_every_nonlinear_stage']
                and status['live_source_and_Gram_terms_retained'] and status['original_canonical_momenta_used']
                and status['initial_preparation_unchanged'])
            check(branch+'_three_time_refinements_recorded', [row['steps'] for row in status['cases']] == [4, 8, 16]
                and len(status['comparisons']) == 2)
            check(branch+'_direct_control_is_original_RHS', control['no_modal_split_in_DOP853']
                and control['independent_original_physical_RHS_used'] and control['duration'] == 2.5e-6
                and control['RK_control_changed_max_step']
                and not control['force_RK_tolerance_uncertainty_not_separately_extracted'])
            check(branch+'_unchanged_force_gate', final['force_threshold'] == 2.700598122731542e-8
                and final['full_interval_gate_pass'] is False and not final['spatial_force_convergence_claim'])
            check(branch+'_whole_short_pilot_control_scope', extended_initial['duration'] == 4e-5
                and extended_initial['no_modal_split_in_RK'] and extended_initial['previous_point004_window_not_retested']
                and extended_initial['original_indexed_RHS_agreement_prerequisite']
                and len(extended_initial['saved_time_differences']) == 17)
            for row in status['cases']:
                error = abs(row['reduced_wave_force']-final['continuum_force'])
                rows.append(dict(branch=branch, steps=row['steps'], time=status['duration'], step=row['step'],
                    force=row['reduced_wave_force'], continuum_force=final['continuum_force'],
                    force_error=error, inherited_peak_scaled_threshold=final['force_threshold'],
                    raw_endpoint_force_threshold_pass=error <= final['force_threshold'],
                    final_waveform_relative_error=final['field_error'] if row['steps'] == 16 else '',
                    final_empirical_time_budget_pass=status['empirical_final_time_budget_pass'] if row['steps'] == 16 else '',
                    direct_first_fine_step_agreement_pass=control['short_algorithm_agreement_pass'] if row['steps'] == 16 else '',
                    direct_full_short_pilot_agreement_pass=extended['independent_short_pilot_agreement_pass'] if row['steps'] == 16 else '',
                    evolution_seconds=row['evolution_seconds'], maximum_rotation_angle=row['maximum_rotation_angle'],
                    valid_for_claim=False, full_window_pass=False,
                    source_path=str((intake/('annular-P2-live-exponential-'+branch+'-257-attempt01')/'status.json').relative_to(root))))
        mts = statuses['annular-P2-live-exponential-MTS-257-attempt01']
        check('coarse_MTS_temporal_failure_preserved', not mts['comparisons'][0]['empirical_time_budget_pass']
            and mts['comparisons'][1]['empirical_time_budget_pass'])
        initial_rk = statuses['annular-P2-indexed-full-pilot-control-MTS-attempt01']
        refined_rk = statuses['annular-P2-indexed-full-pilot-control-MTS-attempt02']
        check('coarse_MTS_RK_control_failure_preserved', not initial_rk['independent_short_pilot_agreement_pass']
            and initial_rk['endpoint_force_RK_refinement_difference'] > 2e-10
            and refined_rk['previous_failed_coarse_control_preserved'])
        refined_budget_pass = (refined_rk['endpoint_force_RK_refinement_difference'] < 2e-10
            and refined_rk['endpoint_force_exponential_RK_difference'] < 2e-9
            and refined_rk['endpoint_relative_state_refinement'] < 1e-8
            and refined_rk['endpoint_relative_method_difference'] < 1e-6
            and max(row['exponential_RK_relative_difference']
                for row in refined_rk['inherited_seventeen_time_state_controls']) < 1e-6
            and max(row['source_gap'] for row in refined_rk['inherited_seventeen_time_state_controls']) < 1e-9)
        check('refined_MTS_control_flag_matches_unchanged_budgets',
            refined_rk['independent_short_pilot_agreement_pass'] == refined_budget_pass
            and refined_rk['maximum_step'] == 1.25e-6 and refined_rk['refined_force_test_only_at_endpoint'])
        indexed = statuses['annular-P2-indexed-live-geometry-attempt01']
        check('indexed_kernel_preserves_physics_and_saved_states', indexed['modes_and_quadrature_unchanged']
            and indexed['canonical_and_radial_tolerances_unchanged'] and indexed['new_evolution_performed'] is False
            and len(indexed['cases']) == 4 and len(indexed['force_controls']) == 2)
        force_split = statuses['annular-P2-evolved-force-error-split-attempt01']
        check('force_error_split_is_saved_state_algebra_not_new_limit',
            force_split['saved_state_algebra_only'] and not force_split['new_evolution_performed']
            and force_split['holding_drives_fixed_is_not_a_dynamical_Q_zero_limit']
            and force_split['continuum_oracle_error_not_certified']
            and len(force_split['cases']) == 4 and all(not row['valid_for_claim'] for row in force_split['cases']))
        with table.open('w', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        with table.open(encoding='utf-8', newline='') as stream:
            parsed = list(csv.DictReader(stream))
        check('six_row_CSV_parses_with_sources_and_nonclaim_flags', len(parsed) == 6 and all(None not in row
            and (root/row['source_path']).is_file() and row['valid_for_claim'] == 'False'
            and row['full_window_pass'] == 'False' for row in parsed))
        own(table, 'outputs')
        spatial_rows = []
        for name, status in statuses.items():
            if not name.startswith('annular-P2-evolved-source-halving-'):
                continue
            check(name+'_scope_and_two_time_controls', status['source_refinement_only_not_joint_spatial_convergence']
                and status['old_point004_window_not_retested'] and [row['steps'] for row in status['cases']] == [16, 32])
            check(name+'_reported_force_differences_recompute',
                abs(status['baseline_force']-status['continuum_force']) == status['baseline_force_error']
                and abs(status['cases'][-1]['force']-status['continuum_force']) == status['refined_force_error']
                and abs(status['cases'][0]['force']-status['cases'][1]['force']) == status['time_force_difference']
                and status['time_force_budget'] == 2e-9 and status['time_state_budget'] == 1e-6
                and status['empirical_time_budget_pass'] == (status['time_force_difference'] < 2e-9
                    and status['time_state_difference'] < 1e-6))
            for row in status['cases']:
                spatial_rows.append(dict(branch=status['branch'], base_count=status['base_count'],
                    source_cap=status['source_cap'], time=status['duration'], steps=row['steps'], force=row['force'],
                    continuum_force=status['continuum_force'], force_error=row['force_error'],
                    instantaneous_relative_error=row['instantaneous_force_relative_error'],
                    cap4_RK_force_error=status['baseline_force_error'],
                    pair_time_refinement_gate_pass=status['empirical_time_budget_pass'],
                    waveform_relative_error=row['field_error'],
                    source_projection_inertia=row['schur']['field_projection_inertia'],
                    source_touching_lift_work=row['lift']['source_touching_work'],
                    combined_Gram_work=row['lift']['combined_Gram_work'],
                    force_lift_identity_error=row['lift']['identity_error'],
                    valid_for_claim=False, full_window_pass=False,
                    source_path=str((intake/name/'status.json').relative_to(root))))
        with spatial_table.open('w', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(spatial_rows[0]))
            writer.writeheader()
            writer.writerows(spatial_rows)
        with spatial_table.open(encoding='utf-8', newline='') as stream:
            parsed = list(csv.DictReader(stream))
        check('source_halving_CSV_parses_and_scoped', len(parsed) == len(spatial_rows) and all(None not in row
            and (root/row['source_path']).is_file() and row['valid_for_claim'] == 'False' for row in parsed))
        own(spatial_table, 'outputs')
        note = root/'DERIVATION-20260919-live-canonical-exponential-step.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv))`', content)
        check('cited_local_paths_exist', bool(cited) and all((root/name).is_file() for name in cited), cited)
        check('final_note_scope_and_completion', 'Awaiting paired' not in content
            and 'to be completed' not in content and 'still running' not in content
            and 'not a full-interval force pass' in content)
        own(note)
        sources = ['annular_P2_live_exponential_20260919.py', 'verify_annular_P2_live_exponential_20260919.py',
            'verify_annular_P2_live_exponential_v2_20260919.py', 'run_annular_P2_live_exponential_20260919.py',
            'verify_annular_P2_live_exponential_direct_20260919.py', 'compare_annular_P2_live_exponential_short_20260919.py',
            'verify_annular_P2_live_exponential_direct_v2_20260919.py',
            'annular_P2_indexed_live_geometry_20260919.py', 'verify_annular_P2_indexed_live_geometry_20260919.py',
            'verify_annular_P2_indexed_full_pilot_20260919.py',
            'refine_annular_P2_indexed_MTS_RK_20260919.py', 'run_annular_P2_evolved_source_halving_20260919.py',
            'run_annular_P2_evolved_source_halving_v2_20260919.py',
            'derive_annular_P2_evolved_force_error_split_20260919.py',
            'seal_annular_P2_live_exponential_20260919.py']
        for name in sources:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('all_sources_compile_without_bytecode', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026, 9, 18, 23, 34, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= start]
        check('protected_mtime_changed_file_count_zero', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(),
            successful_current_implementation_checks=sum(len(status['checks']) for status in statuses.values()),
            inherited_failed_attempts_preserved=36, new_failed_attempts_preserved=1, total_failed_attempts_preserved=37,
            inherited_peak_force_failures_preserved=4, inherited_short_horizon_scientific_failures_preserved=6,
            inherited_initial_force_failures_preserved=5,
            new_coarse_temporal_scientific_failures_preserved=1,
            new_coarse_RK_precision_scientific_failures_preserved=1,
            endpoint_results=comparison['results'], numerical_rows=rows,
            indexed_kernel_comparisons=indexed['cases'],
            source_refinement_results=spatial_rows, MTS_source_refinement_executed=mts_spatial_name in statuses,
            saved_force_error_decomposition=force_split['cases'],
            distinct_files_rehashed=len(cache))
        save()
        print(json.dumps(dict(state='complete', integrity_checks=len(report['checks']),
            implementation_checks=report['successful_current_implementation_checks'], files_rehashed=len(cache),
            retained_failed_attempts=37, short_endpoint_passes=sum(row['short_endpoint_combined_gate_pass']
                for row in comparison['results']))), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
