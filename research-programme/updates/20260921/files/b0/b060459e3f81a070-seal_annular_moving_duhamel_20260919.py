from derive_annular_source_gravity_20260914 import EvidenceRun
from datetime import datetime,timezone
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
    destination = intake/'annular-moving-duhamel-final-integrity.json'
    snapshot = intake/'annular-moving-duhamel-resume-snapshot.md'
    executed = intake/'annular-moving-duhamel-executed-sealer.py'
    suffixes = ['algebra','endpoint','trajectory-summary','trajectory-points','action-channels','reconstruction','sampling-comparison',
        'arithmetic-summary','arithmetic-points','arithmetic-reconstruction','arithmetic-sampling']
    tables = [intake/('annular-moving-duhamel-'+suffix+'.csv') for suffix in suffixes]
    if any(path.exists() for path in [destination,snapshot,executed]+tables):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running',checks=[],inputs={},outputs={},github_action=False,subagents_used=False,
        valid_for_physics_claim=False,full_GR_limit_proven=False,full_live_P2_force_convergence_proven=False,
        uniform_evolving_refinement_rate_proven=False,full_nonlinear_stability_proven=False,
        no_new_live_trajectory=True,exact_moving_remainder_identity_derived=True,
        original_source_Dirichlet_condition_unchanged=True,continuum_mismatch_resolved=False,
        certified_live_continuous_time_bound=False,forcing_interpolation_error_not_assumed_zero=True,
        numerical_trajectory_error_not_assumed_zero=True,
        protected_scan_scope='mtime since2026-09-19T17:30:22Z; not a pre-turn whole-tree hash baseline')
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

    def own(path,category='inputs'):
        report[category][str(path.resolve().relative_to(root))] = digest(path)

    def save():
        destination.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf-8')

    def check(name,passed,detail=None):
        report['checks'].append(dict(name=name,passed=bool(passed),detail=detail))
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def inherit(path):
        data = json.loads(path.read_text())
        for category in ['inputs','outputs']:
            for name,expected in data[category].items():
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
        previous = inherit(intake/'annular-direct-forcing-time-bound-final-integrity.json')
        check('previous7661file_seal_and44failures_preserved',previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks']) and previous['total_failed_attempts_preserved'] == 44
            and previous['distinct_files_rehashed'] == 7661)
        names = ['annular-moving-duhamel-algebra-endpoint-attempt01','annular-moving-duhamel-trajectory-attempt01',
            'annular-moving-duhamel-modal-arithmetic-attempt01']
        statuses = []
        for name in names:
            status = inherit(intake/name/'status.json')
            statuses.append(status)
            check(name+'_complete_private_nonclaim',status['state'] == 'complete'
                and all(row['passed'] for row in status['checks']) and not status['valid_for_physics_claim']
                and not status['full_GR_limit_proven'] and not status['full_live_P2_force_convergence_proven']
                and not status['github_action'] and not status['subagents_used'] and status['no_new_evolution'])
        failures = []
        for path in sorted(intake.glob('annular-moving-duhamel-*/status.json')):
            if path.parent.name not in names:
                failed = inherit(path)
                check(path.parent.name+'_failed_attempt_preserved',failed['state'] == 'failed')
                failures.append(dict(folder=path.parent.name,error=failed['error']))
        check('no_new_failed_execution',not failures)
        sources = [str((intake/name/'status.json').relative_to(root)) for name in names]

        def sourced(rows,index,units):
            return [dict(**row,source_path=sources[index],units=units) for row in rows]

        endpoint,trajectory,arithmetic = statuses
        rows_by_table = [sourced(endpoint['fixtures'],0,'synthetic_fixture'),
            sourced(endpoint['cases'],0,'normalized_annular_fixed_basis_energy_and_forcing'),
            sourced(trajectory['cases'],1,'normalized_saved_trajectory_energy_and_response'),
            sourced(trajectory['points'],1,'normalized_saved_time_and_modal_action_acceleration'),
            sourced(trajectory['channels'],1,'normalized_saved_time_and_modal_action_acceleration'),
            sourced(trajectory['reconstructions'],1,'normalized_saved_time_energy_and_response'),
            sourced(trajectory['quadrature_comparisons'],1,'normalized_saved_time_and_energy_coordinate_difference'),
            sourced(arithmetic['cases'],2,'normalized_modal_arithmetic_and_response'),
            sourced(arithmetic['points'],2,'normalized_modal_acceleration_defect'),
            sourced(arithmetic['reconstructions'],2,'normalized_modal_response_and_energy'),
            sourced(arithmetic['comparisons'],2,'normalized_modal_response_difference')]
        check('expected_table_rows',[len(rows) for rows in rows_by_table] == [4,4,2,132,924,118,18,2,132,118,18])
        for path,rows in zip(tables,rows_by_table):
            with path.open('w',encoding='utf-8',newline='') as stream:
                writer = csv.DictWriter(stream,fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            with path.open(encoding='utf-8',newline='') as stream:
                parsed = list(csv.DictReader(stream))
            check(path.name+'_sourced_nonclaim_rows_parse',len(parsed) == len(rows) and all(None not in row
                and row['valid_for_claim'] == 'False' and (root/row['source_path']).is_file() for row in parsed))
            check(path.name+'_numbers_finite',all(math.isfinite(value) for row in rows for value in row.values()
                if isinstance(value,(float,int))))
            own(path,'outputs')
        check('endpoint_both_branches_and_probe_sizes',{(row['branch'],row['probe_step']) for row in endpoint['cases']}
            == {(branch,step) for branch in ['reference','MTS'] for step in [1e-7,5e-8]})
        check('endpoint_all_derivative_controls_pass',all(row['derivative_error'] <= row['numerical_tolerance']
            and row['initial_acceleration_gap_norm'] > 0. for row in endpoint['cases']))
        check('nonuniform_and_nonnumerical_claim_limits',endpoint['finite_probe_endpoint_checks_not_time_uniform_proof']
            and endpoint['all_source_residual_channels_retained'] and trajectory['saved_trajectory_sampling_not_uniform_certificate']
            and trajectory['forcing_interpolation_not_actual_forcing'] and trajectory['temporal_integration_defect_not_assumed_zero']
            and trajectory['backward_time_from_previous_final_freeze'] and trajectory['all_modes_retained'])
        expected_channels = {'geometry_stiffness_drift','source_kinetic','canonical_action_reconstruction_defect',
            'cross_transport','source_acceleration','mass_transport','inverse_residual'}
        for branch in ['reference','MTS']:
            points = [row for row in trajectory['points'] if row['branch'] == branch]
            times = sorted({row['reverse_time'] for row in points})
            check(branch+'_33_matched_times_two_levels',len(points) == 66 and len(times) == 33
                and times[0] == 0. and times[-1] == 4e-5 and {row['level'] for row in points} == {0,1}
                and all(abs(row['physical_time']+row['reverse_time']-4e-5) < 1e-17 for row in points))
            check(branch+'_canonical_and_halving_controls',all(row['acceleration_control_error'] <= row['acceleration_control_tolerance']
                and (not row['probe_halving_performed'] or row['probe_halving_error'] <= row['acceleration_control_tolerance']) for row in points)
                and sum(row['probe_halving_performed'] for row in points) == 6)
            check(branch+'_seven_channels_every_point',all({row['channel'] for row in trajectory['channels']
                if row['branch'] == branch and row['reverse_time'] == time and row['level'] == level} == expected_channels
                for time in times for level in [0,1]))
            check(branch+'_all_three_reconstruction_grids',all(len([row for row in trajectory['reconstructions']
                if row['branch'] == branch and row['grid_points'] == count]) == count for count in [9,17,33]))
            summary = next(row for row in trajectory['cases'] if row['branch'] == branch)
            selected = [row for row in trajectory['reconstructions'] if row['branch'] == branch and row['grid_points'] == 33]
            check(branch+'_unresolved_error_preserved',not summary['certified_continuous_time_envelope']
                and summary['final_unresolved_response_norm'] == selected[-1]['unresolved_response_norm']
                and summary['maximum_unresolved_response_norm'] == max(row['unresolved_response_norm'] for row in selected))
            check(branch+'_conditional_coverage_not_promoted_to_claim',summary['samples_inside_conditional_bound']
                == sum(row['sample_inside_conditional_bound'] for row in selected) and not summary['valid_for_claim'])
            check(branch+'_finite_positive_energy_rows',all(row['actual_fixed_metric_energy'] >= 0.
                and row['reconstructed_energy'] >= 0. and row['unresolved_response_norm'] >= 0. for row in selected))
            arithmetic_summary = next(row for row in arithmetic['cases'] if row['branch'] == branch)
            check(branch+'_initial_arithmetic_identity_and_remaining_floor',arithmetic_summary['initial_corrected_unresolved_norm'] < 1e-9
                and arithmetic_summary['final_corrected_unresolved_norm'] > 0.
                and arithmetic_summary['max_corrected_unresolved_norm'] >= arithmetic_summary['final_corrected_unresolved_norm'])
            check(branch+'_arithmetic_all_three_grids',all(len([row for row in arithmetic['reconstructions']
                if row['branch'] == branch and row['grid_points'] == count]) == count for count in [9,17,33]))
        check('arithmetic_correction_not_fitted_physics',arithmetic['arithmetic_defect_not_new_physical_force']
            and arithmetic['all_modes_retained'] and arithmetic['no_fitted_coefficients']
            and arithmetic['original_action_forcing_unchanged'] and arithmetic['no_continuous_time_certificate'])
        note = root/'DERIVATION-20260919-moving-system-Duhamel-remainder.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv))`',content)
        check('all_cited_local_paths_exist',bool(cited) and all((root/name).is_file() for name in cited),cited)
        check('claim_limits_and_error_budget_explicit',all(phrase.lower() in content.lower() for phrase in [
            'does not establish the full GR limit','12.5718%','13.58%','not a pre-turn whole-tree hash baseline',
            'not independent physical validations','numerical trajectory error','conditional live bound',
            'interpolation remainder']))
        check('report_complete','RESULTS_PENDING' not in content)
        own(note)
        for name in ['annular_moving_duhamel_20260919.py','validate_annular_moving_duhamel_20260919.py',
                'derive_annular_moving_duhamel_trajectory_20260919.py','diagnose_annular_modal_arithmetic_remainder_20260919.py',
                'seal_annular_moving_duhamel_20260919.py']:
            path = root/'scripts'/name
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('sources_compile_without_bytecode',not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026,9,19,17,30,22,tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*')
            if path.is_file() and path.stat().st_mtime >= start]
        check('protected_mtime_changed_count_zero',not changed,changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot,'outputs')
        own(executed,'outputs')
        count = sum(len(status['checks']) for status in statuses)
        check('successful_implementation_count',count == 642)
        report.update(state='complete',completed_at=datetime.now(timezone.utc).isoformat(),implementation_checks=count,
            total_failed_attempts_preserved=44+len(failures),new_failures=failures,distinct_files_rehashed=len(cache),
            table_rows=[len(rows) for rows in rows_by_table],full_interval_retested=False,
            next_target='action-consistent frozen response using banded mass and factored stiffness without acceleration from squared approximate eigenfrequencies; compare both branches and existing temporal-halving trajectories')
        save()
        print(json.dumps(dict(state='complete',implementation_checks=count,integrity_checks=len(report['checks']),
            files_rehashed=len(cache),failed_attempts_preserved=44+len(failures),table_rows=report['table_rows'])),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
