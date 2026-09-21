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
    destination = intake/'annular-direct-forcing-time-bound-final-integrity.json'
    snapshot = intake/'annular-direct-forcing-time-bound-resume-snapshot.md'
    executed = intake/'annular-direct-forcing-time-bound-executed-sealer.py'
    suffixes = ['algebra','operator','channels','frozen-envelope','frozen-blocks','frozen-samples',
        'frozen-energy','phase-fixtures','oscillatory-summary','oscillatory-samples','failed-attempts']
    tables = [intake/('annular-direct-forcing-'+suffix+'.csv') for suffix in suffixes]
    if any(path.exists() for path in [destination,snapshot,executed]+tables):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running',checks=[],inputs={},outputs={},github_action=False,subagents_used=False,
        valid_for_physics_claim=False,full_GR_limit_proven=False,full_live_P2_force_convergence_proven=False,
        uniform_evolving_refinement_rate_proven=False,full_nonlinear_stability_proven=False,
        no_new_live_trajectory=True,frozen_quadratic_control_evaluated=True,
        original_source_Dirichlet_condition_unchanged=True,continuum_mismatch_resolved=False,
        actual_live_continuous_time_bound=False,frozen_ideal_arithmetic_time_bound_derived=True,
        protected_scan_scope='mtime since2026-09-19T16:59:30Z; not a pre-turn whole-tree hash baseline')
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
        previous = inherit(intake/'annular-action-test-energy-final-integrity.json')
        check('previous7616file_seal_and43failures_preserved',previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks']) and previous['total_failed_attempts_preserved'] == 43
            and previous['distinct_files_rehashed'] == 7616)
        names = ['annular-direct-stiffness-forcing-algebra-attempt01','annular-direct-stiffness-forcing-attempt02',
            'annular-frozen-forcing-time-envelope-attempt01','annular-frozen-oscillatory-response-attempt01']
        statuses = []
        for name in names:
            status = inherit(intake/name/'status.json')
            statuses.append(status)
            check(name+'_complete_private_nonclaim',status['state'] == 'complete'
                and all(row['passed'] for row in status['checks']) and not status['valid_for_physics_claim']
                and not status['full_GR_limit_proven'] and not status['full_live_P2_force_convergence_proven']
                and not status['github_action'] and not status['subagents_used'])
        failures = []
        prefixes = ['annular-direct-stiffness-forcing-algebra-','annular-direct-stiffness-forcing-',
            'annular-frozen-forcing-time-envelope-','annular-frozen-oscillatory-response-']
        discovered = set()
        for prefix in prefixes:
            for path in sorted(intake.glob(prefix+'*/status.json')):
                if path.parent.name not in names and path not in discovered:
                    discovered.add(path)
                    failed = inherit(path)
                    check(path.parent.name+'_failed_attempt_preserved',failed['state'] == 'failed')
                    failures.append(dict(folder=path.parent.name,error=failed['error'],valid_for_claim=False,
                        source_path=str(path.relative_to(root)),units='execution_failure_not_physical_result'))
        check('one_failed_comparison_preserved',len(failures) == 1
            and failures[0]['folder'] == 'annular-direct-stiffness-forcing-attempt01')
        sources = [str((intake/name/'status.json').relative_to(root)) for name in names]

        def sourced(rows,index,units):
            return [dict(**row,source_path=sources[index],units=units) for row in rows]

        rows_by_table = [sourced(statuses[0]['cases'],0,'synthetic_fixture'),
            sourced(statuses[1]['cases'],1,'normalized_annular_mass_dual_forcing_and_operator_norm'),
            sourced(statuses[1]['channels'],1,'normalized_annular_mass_dual_forcing_and_energy_rate'),
            sourced(statuses[2]['cases'],2,'normalized_frozen_control_forcing_and_energy'),
            sourced(statuses[2]['blocks'],2,'normalized_frozen_control_forcing'),
            sourced(statuses[2]['samples'],2,'normalized_frozen_control_time_and_forcing'),
            sourced(statuses[2]['energy_cases'],2,'normalized_frozen_control_time_and_energy'),
            sourced(statuses[3]['fixtures'],3,'synthetic_phase_integral'),
            sourced(statuses[3]['cases'],3,'normalized_frozen_control_energy_and_response'),
            sourced(statuses[3]['samples'],3,'normalized_frozen_control_time_energy_and_response'),failures]
        check('expected_table_rows',[len(rows) for rows in rows_by_table] == [3,12,72,6,210,246,82,4,2,82,1])
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
        algebra,direct,frozen,oscillatory = statuses
        check('direct_complete_branches_steps_sectors',
            {(row['branch'],row['probe_step'],row['sector']) for row in direct['cases']}
            == {(branch,step,sector) for branch in ['reference','MTS'] for step in [1e-7,5e-8]
                for sector in ['gradient','gram','total']})
        for row in direct['cases']:
            label = row['branch']+'_'+str(row['probe_step'])+'_'+row['sector']
            check(label+'_direct_forcing_and_three_bounds',row['comparison_error'] <= row['numerical_tolerance']
                and row['forcing_dual_norm'] <= row['paired_norm_bound']+1e-12
                and row['forcing_dual_norm'] <= row['six_channel_norm_bound']+1e-12
                and row['forcing_dual_norm'] <= row['coarse_energy_forcing_bound']+1e-12)
            matching = [entry for entry in direct['channels'] if (entry['branch'],entry['probe_step'],entry['sector'])
                == (row['branch'],row['probe_step'],row['sector'])]
            check(label+'_all_six_channels',len(matching) == 6 and len({entry['channel'] for entry in matching}) == 6)
        check('live_no_new_jerk_or_changed_transfer',direct['new_jerk_not_computed'] and direct['no_new_evolution']
            and direct['original_nonnested_interpolation_retained'] and direct['original_source_condition_retained']
            and direct['mass_and_stiffness_rates_are_finite_probe_estimates']
            and direct['factored_endpoint_loads_preserve_original_action_arithmetic'])
        for status in [frozen,oscillatory]:
            check('frozen_only_scope_'+str(len(status['checks'])),status['no_new_live_evolution']
                and status['frozen_quadratic_control_only'] and status['not_the_actual_moving_source_trajectory']
                and status['all_modes_retained'] and status['no_fitted_frequency_filter'])
        for branch in ['reference','MTS']:
            for sector in ['gradient','gram','total']:
                blocks = [row for row in frozen['blocks'] if row['branch'] == branch and row['sector'] == sector]
                covered = [mode for row in blocks for mode in range(row['first_mode'],row['last_mode']+1)]
                check(branch+'_'+sector+'_complete_once_only_mode_coverage',covered == list(range(558)))
            samples = [row for row in oscillatory['samples'] if row['branch'] == branch]
            check(branch+'_all_oscillatory_samples_and_envelopes',len(samples) == 41
                and samples[0]['frozen_time'] == 0. and samples[-1]['frozen_time'] == 4e-5
                and all(row['duhamel_error'] <= row['numerical_tolerance']
                    and row['energy'] <= row['retained_energy_bound']+1e-8*max(row['energy'],row['retained_energy_bound'])
                    for row in samples))
            summary = next(row for row in oscillatory['cases'] if row['branch'] == branch)
            check(branch+'_spectral_identity_and_improved_response_bound',summary['spectral_identity_relative_error'] < 2e-8
                and summary['final_oscillatory_energy_bound'] < summary['final_previous_energy_bound']
                and summary['coarse_modes'] == 558 and summary['fine_modes'] == 1072
                and summary['applies_to_frozen_control_only'])
        check('resonance_limits_retained',oscillatory['exact_resonance_not_divided_by_zero']
            and oscillatory['floating_point_not_interval_certificate'])
        note = root/'DERIVATION-20260919-direct-forcing-and-frozen-time-bound.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv))`',content)
        check('all_cited_local_paths_exist',bool(cited) and all((root/name).is_file() for name in cited),cited)
        check('claim_limits_and_next_derivation_explicit',all(phrase in content for phrase in [
            'does not establish the full GR limit','12.5718%','13.58%','not a pre-turn whole-tree hash baseline',
            'not independent physical validations','not interval-arithmetic error certificates',
            'does not explain away','Duhamel remainder','801 implementation checks']))
        check('report_complete','will be inserted' not in content)
        own(note)
        script_names = ['annular_direct_stiffness_forcing_20260919.py','validate_annular_direct_stiffness_forcing_20260919.py',
            'derive_annular_direct_stiffness_forcing_20260919.py','derive_annular_direct_stiffness_forcing_v2_20260919.py',
            'derive_annular_frozen_forcing_time_envelope_20260919.py','derive_annular_frozen_oscillatory_response_20260919.py',
            'seal_annular_direct_forcing_time_bound_20260919.py']
        for name in script_names:
            path = root/'scripts'/name
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('sources_compile_without_bytecode',not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026,9,19,16,59,30,tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*')
            if path.is_file() and path.stat().st_mtime >= start]
        check('protected_mtime_changed_count_zero',not changed,changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot,'outputs')
        own(executed,'outputs')
        count = sum(len(status['checks']) for status in statuses)
        check('successful_implementation_count',count == 801)
        report.update(state='complete',completed_at=datetime.now(timezone.utc).isoformat(),implementation_checks=count,
            total_failed_attempts_preserved=43+len(failures),new_failures=failures,distinct_files_rehashed=len(cache),
            table_rows=[len(rows) for rows in rows_by_table],full_interval_retested=False,
            next_target='derive and bound the actual moving-system Duhamel remainder in a fixed frozen energy basis, retaining all source and coefficient-rate terms')
        save()
        print(json.dumps(dict(state='complete',implementation_checks=count,integrity_checks=len(report['checks']),
            files_rehashed=len(cache),failed_attempts_preserved=43+len(failures),table_rows=report['table_rows'])),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
