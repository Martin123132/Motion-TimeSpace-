from stage172_angle_common import *
import argparse


def write_report():
    validation = verify(ROOT / 'results/validation')
    assessment = verify(ROOT / 'results/assessment')
    frozen = verify(ROOT / 'results/frozen')
    impacts = json.loads((ROOT / 'results/assessment/stencil-impact.json').read_text())
    rows = json.loads((ROOT / 'results/assessment/prediction-checks.json').read_text())
    lines = ['# Stage172 — complete inherited scattering-angle sum at x=14', '',
             '## Scope and reuse',
             'Completed the two missing hard-scattering cosines, plus the saved central cosine.',
             'Each angle uses the same12 reflection representatives of the16-node electron rule.',
             'The three hard Gauss weights are already included in each event contribution.',
             'Reused72 central-angle event-temperature combinations; evaluated144 new combinations.',
             'Incoming x=14, incoming weight, emitted integration, native histories and tolerances',
             'remain unchanged. This is one finite quadrature contribution, not the frequency integral.', '',
             '## Prediction freeze',
             'Anchor fraction .875; target .90625; log-temperature steps .01 and .005.',
             'Both linear and quadratic predictions were frozen before the24 new target events.',
             'The12 central target combinations were already known. The combined comparison is',
             'partly prospective, not a wholly blinded new-temperature trial. No target fit or retuning.',
             'Frozen SHA256: `'+frozen['prediction_sha256']+'`.',
             'Frozen UTC: '+frozen['finished_utc']+'.', '',
             '## Complete electron/angle sum',
             'Maximum photon-source mass-dual relative error over the four inherited history columns.',
             'Source vectors are summed before norms. Percentages are numerical errors, not fit scores.', '',
             '|Incident history|Source|Linear error %|Quadratic error %|Quadratic stencil change %|',
             '|---|---|---:|---:|---:|']
    for branch in BRANCHES:
        for component in ['control', 'remainder', 'total']:
            prefix = 'complete_sum/'
            linear = assessment['summary'][prefix+'linear_fine/'+branch+'/'+component]['maximum']
            quadratic = assessment['summary'][prefix+'quadratic_fine/'+branch+'/'+component]['maximum']
            sensitivity = max(row['relative'] for row in impacts if (row['group'], row['branch'], row['component']) == ('complete_sum', branch, component))
            lines.append(f'|{branch}|{component}|{100*linear:.9g}|{100*quadratic:.9g}|{100*sensitivity:.9g}|')
    lines += ['', 'Control is the inherited leading microscopic baseline; remainder is matched',
              'difference+virtual+state (MTS increment); total is control+remainder. Both use',
              'the same native incident histories, not independently refitted histories or a new LCDM fit.', '',
              '## Per-angle matched prediction',
              'Quadratic error percentages retain angle-by-angle outcomes rather than only the total.', '',
              '|Hard-angle group|Moving baseline %|Moving MTS increment %|Fixed baseline %|Fixed MTS increment %|',
              '|---|---:|---:|---:|---:|']
    for group in ['angle_negative', 'angle_central', 'angle_positive', 'new_angles_sum']:
        values = [100*assessment['summary'][group+'/quadratic_fine/'+branch+'/'+component]['maximum'] for branch in BRANCHES for component in ['control', 'remainder']]
        lines.append('|'+group+'|'+'|'.join(f'{value:.9g}' for value in values)+'|')
    lines += ['', '## Summed finite-difference stability',
              'Same1% gate for coarse/fine D1 and D2. Native histories remain piecewise linear:',
              'finite-step results are not a classical second-derivative claim at interpolation knots.', '',
              '|Incident history|Source|D1 change %|D2 change %|',
              '|---|---|---:|---:|']
    for branch in BRANCHES:
        for component in source.COMPONENTS:
            prefix = f'complete_sum:{branch}:{component}:'
            first = max(row['value'] for row in frozen['checks'] if row['name'].startswith(prefix) and row['name'].endswith(':tangent'))
            second = max(row['value'] for row in frozen['checks'] if row['name'].startswith(prefix) and row['name'].endswith(':curvature'))
            lines.append(f'|{branch}|{component}|{100*first:.9g}|{100*second:.9g}|')
    lines += ['', '## Validation',
              f"Protocol checks: {validation['count']}; all pass: {validation['all_checks_passed']}.",
              f"Source energy/gas and component-closure checks: {assessment['moment_checks']}; failures: {assessment['moment_failures']}.",
              f"Current failed numerical comparisons retained: {validation['retained_failed_check_count']}.",
              f"Immediate-parent/consumed files rehashed and authenticated: {validation['rehashed_prior_files']}."]
    for kind in ['linear_fine', 'quadratic_fine', 'quadratic_coarse']:
        selected = [row for row in rows if row['prediction'] == kind]
        lines.append(f"{kind}: {sum(row['relative'] < .01 for row in selected)}/{len(selected)} pass the unchanged1% prediction gate.")
    lines += ['Individual, per-angle, partial-sum and total results are correlated numerical checks,',
              'not independent experiments. All earlier and current failures remain in their records.',
              'Source files, curves, tolerances and histories are unchanged. No transport rerun,',
              'GitHub action or subagent. One production worker, below-normal priority, one library thread.', '',
              '## Next target']
    if validation['primary_summed_derivative_stability_pass']:
        lines += ['Carry the same frozen source-temperature construction into the incoming-frequency',
                  'integral using saved quadrature contributions, starting with a bounded frequency panel.',
                  'Retain separate-component flags; do not infer a continuum angular error bound from',
                  'completion of this inherited finite rule.']
    else:
        lines += ['Use the completed angle sum to separate the incident-history interpolation contribution',
                  'from the smooth microscopic kernel derivative before extending the frequency integral.',
                  'Derive the native-history tangent from collision/emission evolution rather than refitting',
                  'the temperature curve or relaxing tolerances.']
    lines += ['']
    (ROOT / 'RESULTS.md').write_text('\n'.join(lines), encoding='utf-8')


def seal():
    destination = ROOT / 'results/stage-integrity.json'
    assert not destination.exists()
    validation = verify(ROOT / 'results/validation')
    assert validation['all_checks_passed']
    assert (ROOT / 'RESULTS.md').exists() and (ROOT / 'RUN-NOTES.md').exists()
    parent = json.loads((PARENT / 'results/stage-integrity.json').read_text())
    assert digest(PARENT / 'results/stage-integrity.json') == PARENT_SHA
    for filename, checksum in validation['consumed_and_immediate_rehashed'].items():
        assert digest(filename) == checksum, filename
    progress = json.loads((ROOT / 'progress.json').read_text())
    assert progress['state'] == 'production_complete' and progress['saved_new_events'] == 144
    import psutil
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        if process.info['pid'] == os.getpid():
            continue
        command = ' '.join(process.info['cmdline'] or [])
        assert not ('run_stage172.py' in command and 'python' in (process.info['name'] or '').lower()), command
    assert not list(ROOT.rglob('__pycache__'))
    inherited = parent['inherited_sealed_payload_count']+len(parent['file_hashes'])
    assert inherited == 333386
    carried_names = ['checkpoint_manifest_sha256', 'local_source_documents', 'primary_pdfs', 'source_urls',
                     'observational_source_urls', 'original_library_sha256', 'native_library_sha256',
                     'physical_source_scope', 'retained_local_approximation_histories',
                     'raw_subtraction_response_retained', 'raw_failed_history_response_retained']
    carried = {key:value for key,value in parent.items() if key in carried_names or key.startswith('latest_')}
    payloads = {path.relative_to(ROOT).as_posix(): digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path != destination}
    largest = max(sum(path.is_file() for path in folder.iterdir()) for folder in [ROOT, *[path for path in ROOT.rglob('*') if path.is_dir()]])
    assert largest <= 500
    retained = json.loads((ROOT / 'results/validation/retained-failures.json').read_text())
    packet = dict(state='complete', stage=172, sealed_at_utc=datetime.now(timezone.utc).isoformat(),
                  parent_seal_sha256=PARENT_SHA, file_hashes=payloads, inherited_sealed_payload_count=inherited, **carried,
                  previous_primary_source_urls=parent.get('previous_primary_source_urls', [])+parent.get('new_primary_source_urls', []),
                  new_primary_source_urls=[], prior_archive_full_rehash_performed=False,
                  prior_archive_verification_seal_sha256=parent['prior_archive_verification_seal_sha256'],
                  prior_payload_verification_scope='Immediate Stage171 and consumed inputs rehashed; older archive inherited through seals.',
                  consumed_and_immediate_rehashed=validation['consumed_and_immediate_rehashed'],
                  prior_files_rehashed=validation['rehashed_prior_files'], validation_checks=validation['count'],
                  accepted_current_scope_verified=True,
                  accepted_scope='Complete inherited finite electron/hard-angle rule at x=14; frozen missing-angle source-temperature predictions and retained stability failures.',
                  latest_scattering_angle_temperature_sum=str(ROOT / 'RESULTS.md'),
                  final_validation=str(ROOT / 'results/validation/status.json'),
                  production_event_temperature_combinations=144, reused_event_temperature_combinations=72,
                  complete_inherited_finite_electron_rule=True, complete_inherited_finite_hard_angle_rule=True,
                  incoming_frequency=14., hard_cosines=json.loads((ROOT / 'configuration.json').read_text())['hard_cosines'],
                  partially_prospective_target_test=True, target_previously_seen_combinations=12, target_new_frozen_combinations=24,
                  primary_summed_derivative_stability_pass=validation['primary_summed_derivative_stability_pass'],
                  native_history_classical_second_derivative_claimed=False, derivative_numbers_are_finite_difference_evaluations=True,
                  full_population_integral=False, full_population_source_temperature_law_certified=False,
                  native_incident_histories_are_inputs=True, source_curve_changed=False, temperature_curve_changed=False,
                  current_history_replaced=False, tolerances_changed=False, baseline_preserved=True,
                  independent_raw_physical_source_qualified=False,
                  retained_failed_checks=parent.get('retained_failed_checks', [])+retained,
                  current_stage_retained_failures=len(retained), global_numerical_error_bound=None,
                  protected_workbench_recent_modified_file_count=validation['protected_modified_file_count'],
                  protected_check_scope=validation['protected_check_scope'], maximum_active_production_workers=1,
                  active_workers_at_seal=0, library_threads_per_production_worker=1, largest_direct_file_count=largest,
                  github_action=False, subagents=0, global_installation_changed=False, galaxy_work_modified=False,
                  next_target_file=str(ROOT / 'RESULTS.md'))
    write_json(destination, packet)
    assert all(digest(ROOT / filename) == checksum for filename, checksum in payloads.items())
    print(json.dumps(dict(sealed_files=len(payloads), cumulative_payloads=inherited+len(payloads), seal_sha256=digest(destination))), flush=True)


if __name__ == '__main__':
    source.modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['report', 'seal'])
    args = parser.parse_args()
    if args.phase == 'report':
        write_report()
    else:
        seal()
