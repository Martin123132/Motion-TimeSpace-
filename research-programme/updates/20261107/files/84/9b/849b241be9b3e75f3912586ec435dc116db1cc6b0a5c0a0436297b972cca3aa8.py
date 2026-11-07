from stage174_frequency_common import *
import argparse


def write_report():
    validation = verify(ROOT / 'results/validation')
    assessment = verify(ROOT / 'results/assessment')
    frozen = verify(ROOT / 'results/frozen')
    config = json.loads((ROOT / 'configuration.json').read_text())
    impacts = json.loads((ROOT / 'results/assessment/stencil-impact.json').read_text())
    rows = json.loads((ROOT / 'results/assessment/prediction-checks.json').read_text())
    lines = ['# Stage174 — matching upper incoming-frequency temperature test', '',
             f"New incoming frequency x={config['incoming_frequency']:.15g}; saved references x=11.564929091735618 and14.",
             'The new node is the immediately upper inherited order7 node in the8-20 panel,',
             'selected before source evaluation. No quadrature or temperature-rule changes.', '',
             '## What was predicted',
             'Applied the same microscopic temperature construction at the new frequency using',
             'its own physically evaluated stencils. This is NOT a frequency interpolation from the two saved nodes.',
             'All36 new electron/hard-angle target sources were evaluated after prediction freeze.',
             'Anchor fraction .875; target .90625; log-temperature steps .01 and .005 unchanged.',
             'Predictions and target sum from both saved nodes are reused unchanged. The three-node partial-sum',
             'comparison is partly prospective because target results at both earlier nodes were already known.',
             'Frozen SHA256: `'+frozen['prediction_sha256']+'`.',
             'Frozen UTC: '+frozen['finished_utc']+'.', '',
             '## Frozen quadratic comparisons',
             'Maximum mass-dual photon-source error over the four inherited history columns.',
             'Percentages follow sums of already-weighted source vectors, not averages of errors.', '',
             '|Contribution|Incident history|Source|Linear error %|Quadratic error %|Quadratic stencil change %|',
             '|---|---|---|---:|---:|---:|']
    for group in ['complete_sum', 'three_frequency_partial']:
        for branch in BRANCHES:
            for component in ['control', 'remainder', 'total']:
                linear = assessment['summary'][group+'/linear_fine/'+branch+'/'+component]['maximum']
                quadratic = assessment['summary'][group+'/quadratic_fine/'+branch+'/'+component]['maximum']
                sensitivity = max(row['relative'] for row in impacts if (row['group'], row['branch'], row['component']) == (group, branch, component))
                lines.append(f'|{group}|{branch}|{component}|{100*linear:.9g}|{100*quadratic:.9g}|{100*sensitivity:.9g}|')
    lines += ['', 'complete_sum is the full inherited finite electron/hard-angle sum at the NEW node.',
              'three_frequency_partial adds that contribution to the saved two-node sum. It is NOT the',
              'full8-20 panel, an integral between nodes, or the complete incoming spectrum.',
              'Control is the inherited leading microscopic baseline. Remainder is the matched MTS',
              'difference+virtual+state increment; total includes both. Native incident histories are',
              'the same for baseline/MTS, not refitted. These are numerical tests, not observational fits.', '',
              '## Per-angle new-frequency prediction',
              '|Hard-angle group|Moving baseline %|Moving MTS increment %|Fixed baseline %|Fixed MTS increment %|',
              '|---|---:|---:|---:|---:|']
    for group in ['angle_negative', 'angle_central', 'angle_positive']:
        values = [100*assessment['summary'][group+'/quadratic_fine/'+branch+'/'+component]['maximum'] for branch in BRANCHES for component in ['control', 'remainder']]
        lines.append('|'+group+'|'+'|'.join(f'{value:.9g}' for value in values)+'|')
    lines += ['', '## Finite-difference stability',
              'The1% coarse/fine D1 and D2 gates are unchanged. Native histories are piecewise',
              'linear in time: this is finite-step variation, not classical curvature at a knot.', '',
              '|Contribution|Incident history|Source|D1 change %|D2 change %|',
              '|---|---|---|---:|---:|']
    for group in ['complete_sum', 'three_frequency_partial']:
        for branch in BRANCHES:
            for component in source.COMPONENTS:
                prefix = f'{group}:{branch}:{component}:'
                first = max(row['value'] for row in frozen['checks'] if row['name'].startswith(prefix) and row['name'].endswith(':tangent'))
                second = max(row['value'] for row in frozen['checks'] if row['name'].startswith(prefix) and row['name'].endswith(':curvature'))
                lines.append(f'|{group}|{branch}|{component}|{100*first:.9g}|{100*second:.9g}|')
    lines += ['', '## Reuse, batching and validation',
              '216 new event-temperature combinations saved atomically in36 six-event batches.',
              'The first six-event batch was run separately to test safe continuation. The production',
              'restart skips those saved events and verifies their completed batch packet.',
              'Saved two-node predictions/derivatives and target sum, all native histories, basis and',
              'available virtual-loop coefficients are reused. No previous payload is overwritten.',
              f"Protocol checks: {validation['count']}; all pass: {validation['all_checks_passed']}.",
              f"Source energy/gas and component-closure checks: {assessment['moment_checks']}; failures: {assessment['moment_failures']}.",
              f"Current failed numerical comparisons retained: {validation['retained_failed_check_count']}.",
              f"Immediate-parent/consumed files rehashed and authenticated: {validation['rehashed_prior_files']}."]
    for kind in ['linear_fine', 'quadratic_fine', 'quadratic_coarse']:
        selected = [row for row in rows if row['prediction'] == kind]
        lines.append(f"{kind}: {sum(row['relative'] < .01 for row in selected)}/{len(selected)} pass the unchanged1% prediction gate.")
    lines += ['Individual, angle, complete-node and partial-sum outcomes are correlated numerical',
              'checks, not independent experiments. All failures remain visible. No fit, cutoff,',
              'source-curve/history replacement, transport rerun, GitHub action or subagent.',
              'One production worker, below-normal priority, one library thread.', '',
              '## Next target']
    if all(validation['primary_summed_derivative_stability'].values()):
        lines += ['Extend to the next unused inherited8-20 node below11.564929091735618, in bounded',
                  'batches, reusing all three completed nodes. Retain per-node outcomes while accumulating',
                  'the incoming panel; complete-node success is not a continuum integration bound.']
    else:
        lines += ['Use the saved new-node bank to isolate any failed derivative/curvature channel from',
                  'the native-history interpolation before expanding the panel. Derive the history',
                  'tangent from collision/emission dynamics instead of retuning the temperature curve.']
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
    assert progress['state'] == 'production_complete' and progress['saved_new_events'] == 216
    import psutil
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        if process.info['pid'] == os.getpid():
            continue
        command = ' '.join(process.info['cmdline'] or [])
        assert not ('run_stage174.py' in command and 'python' in (process.info['name'] or '').lower()), command
    assert not list(ROOT.rglob('__pycache__'))
    inherited = parent['inherited_sealed_payload_count']+len(parent['file_hashes'])
    assert inherited == 334227
    carried_names = ['checkpoint_manifest_sha256', 'local_source_documents', 'primary_pdfs', 'source_urls',
                     'observational_source_urls', 'original_library_sha256', 'native_library_sha256',
                     'physical_source_scope', 'retained_local_approximation_histories',
                     'raw_subtraction_response_retained', 'raw_failed_history_response_retained']
    carried = {key:value for key,value in parent.items() if key in carried_names or key.startswith('latest_')}
    payloads = {path.relative_to(ROOT).as_posix(): digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path != destination}
    largest = max(sum(path.is_file() for path in folder.iterdir()) for folder in [ROOT, *[path for path in ROOT.rglob('*') if path.is_dir()]])
    assert largest <= 500
    retained = json.loads((ROOT / 'results/validation/retained-failures.json').read_text())
    config = json.loads((ROOT / 'configuration.json').read_text())
    packet = dict(state='complete', stage=174, sealed_at_utc=datetime.now(timezone.utc).isoformat(),
                  parent_seal_sha256=PARENT_SHA, file_hashes=payloads, inherited_sealed_payload_count=inherited, **carried,
                  previous_primary_source_urls=parent.get('previous_primary_source_urls', [])+parent.get('new_primary_source_urls', []),
                  new_primary_source_urls=[], prior_archive_full_rehash_performed=False,
                  prior_archive_verification_seal_sha256=parent['prior_archive_verification_seal_sha256'],
                  prior_payload_verification_scope='Immediate Stage173 and consumed inputs rehashed; older archive inherited through seals.',
                  consumed_and_immediate_rehashed=validation['consumed_and_immediate_rehashed'],
                  prior_files_rehashed=validation['rehashed_prior_files'], validation_checks=validation['count'],
                  accepted_current_scope_verified=True,
                  accepted_scope='Frozen microscopic temperature predictions at one adjacent incoming quadrature node and unrenormalized three-frequency partial sum; failures retained.',
                  latest_upper_adjacent_frequency_temperature_test=str(ROOT / 'RESULTS.md'), final_validation=str(ROOT / 'results/validation/status.json'),
                  production_event_temperature_combinations=216, verified_six_event_batches=36,
                  complete_inherited_finite_electron_rule=True, complete_inherited_finite_hard_angle_rule=True,
                  incoming_frequency=config['incoming_frequency'], reference_frequencies=config['reference_frequencies'],
                  new_frequency_target_frozen_before_all_evaluations=True, partial_sum_partly_prospective=True,
                  incoming_panel_complete=False, incoming_frequency_interpolation_test=False,
                  primary_summed_derivative_stability=validation['primary_summed_derivative_stability'],
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
