from isolate_stage177 import *
import argparse


def read(name):
    return json.loads((ROOT/'results'/(name+'.json')).read_text())


def verify():
    status=read('status')
    assert status['all_checks_passed'] and (ROOT/'results/COMPLETE').exists()
    for filename,checksum in status['input_hashes'].items():
        assert saved.digest(filename)==checksum,filename
    return status


def report():
    status=verify()
    metrics=read('source-metrics')
    attribution=read('fixed-history-attribution')
    components=read('component-attribution')
    localization=read('angle-electron-attribution')
    histories=read('native-history-diagnostics')
    lines=['# Stage177 — saved curvature discrepancy isolated','',
           'Post-test diagnostic at x=18.449187113596366. No source event was reevaluated.',
           'Original1% derivative/prediction and1e-10 identity/precision tolerances retained.',
           'The following decomposition does not replace the frozen Stage176 predictions.','',
           '## Moving versus fixed incident histories',
           '|Component|Moving curvature change %|Fixed curvature change %|Moving gate passes /4|Fixed gate passes /4|',
           '|---|---:|---:|---:|---:|']
    for component in source.COMPONENTS:
        moving=[row for row in metrics if row['branch']=='moving_history' and row['component']==component]
        fixed=[row for row in metrics if row['branch']=='fixed_incident' and row['component']==component]
        lines.append(f"|{component}|{100*max(row['relative'] for row in moving):.10g}|{100*max(row['relative'] for row in fixed):.10g}|{sum(row['passed'] for row in moving)}|{sum(row['passed'] for row in fixed)}|")
    lines+=['','Control is the leading microscopic baseline. Remainder is the matched MTS',
            'difference+virtual+state increment. Both use the same incident-history inputs.',
            'The complete-node matched moving-history curvature gate remains failed.','',
            '## Exact fixed/history-dependent attribution',
            'Signed projections onto the moving discrepancy; positive and negative pieces',
            'sum to100%. History-dependent includes real evolution and mixed operator/history',
            'response. It is NOT an estimate of interpolation error or a causal percentage.','',
            '|Component|History column|Fixed signed share %|History-dependent signed share %|Fixed norm / moving norm|',
            '|---|---:|---:|---:|---:|']
    for row in attribution:
        if row['component'] in ['control','remainder','total']:
            lines.append(f"|{row['component']}|{row['history']}|{100*row['fixed_signed_share']:.10g}|{100*row['history_signed_share']:.10g}|{row['fixed_norm_over_moving']:.8g}|")
    lines+=['','## Which matched components carry the discrepancy?',
            'Signed shares refer to the matched increment, not to the total baseline+MTS source.',
            'Cancellation factor is sum of the three discrepancy norms / matched discrepancy norm.','',
            '|Incident history|History column|Difference share %|Virtual share %|State share %|Cancellation factor|',
            '|---|---:|---:|---:|---:|---:|']
    for branch in saved.BRANCHES:
        for history in range(4):
            selected=[row for row in components if row['branch']==branch and row['history']==history]
            values={row['component']:row for row in selected}
            lines.append(f"|{branch}|{history}|{100*values['difference']['signed_share']:.10g}|{100*values['virtual']['signed_share']:.10g}|{100*values['state']['signed_share']:.10g}|{selected[0]['cancellation_factor']:.8g}|")
    lines+=['','## Angular and electron localization',
            'All signed projections are saved in angle-electron-attribution.json.',
            'For the worst matched moving-history column, the leading signed event',
            'contributions and full hard-angle subtotals are:','',
            '|Group|Signed share of matched discrepancy %|','|---|---:|']
    worst=max((row for row in metrics if row['branch']=='moving_history' and row['component']=='remainder'),key=lambda row:row['relative'])['history']
    chosen=[row for row in localization if (row['branch'],row['component'],row['history'])==('moving_history','remainder',worst)]
    for row in [*[row for row in chosen if row['group'].startswith('angle_')],
                *sorted([row for row in chosen if ':electron' in row['group']],key=lambda row:abs(row['signed_share']),reverse=True)[:8]]:
        lines.append(f"|{row['group']}|{100*row['signed_share']:.10g}|")
    lines+=['','## Effect on the frozen prediction',
            'Each sensitivity below is normalized by the ORIGINAL target-source norm,',
            'not the fine curvature norm. Vector contributions are not scalar-added.','',
            '|Incident history|Component|D1 contribution %|D2 contribution %|Combined P2 change %|',
            '|---|---|---:|---:|---:|']
    for branch in saved.BRANCHES:
        for component in ['control','remainder','total']:
            rows=[row for row in metrics if row['branch']==branch and row['component']==component]
            lines.append(f"|{branch}|{component}|{100*max(row['tangent_prediction_change'] for row in rows):.10g}|{100*max(row['curvature_prediction_change'] for row in rows):.10g}|{100*max(row['combined_prediction_change'] for row in rows):.10g}|")
    lines+=['','## Independent arithmetic check',
            'The first diagnostic attempt exposed roundoff in differences of already-rounded',
            'curvatures. That attempt and its failures are preserved under',
            'attempt-01-rounded-differences. Rebuilt each primitive event component at80digits',
            'from180 saved packets including low parts, then assembled components and sums.',
            'Repeated independently at100digits; no event physics was rerun.',
            f"Maximum80-versus100digit relative difference: {status['max_independent_reconstruction_relative']:.10g}.",
            f"Maximum legacy-versus-rebuilt relative difference: {status['max_legacy_roundoff_relative']:.10g}.",
            f"Legacy-versus-rebuilt1e-10 failures retained: {status['legacy_roundoff_failed_checks']}.",
            'All ORIGINAL curvature-gate classifications are unchanged. Attributions use the',
            'rebuilt arithmetic; original predictions, stencils and thresholds are untouched.',
            'This does not test source-integration errors already in the saved packets.','',
            '## Native incident-history inspection',
            'The saved history grids have6401 points and the anchor is at a grid knot.',
            'Both stencils cross multiple intervals: plus/minus h=.01 reaches approximately',
            '28 intervals on each side, and h=.005 approximately14. A knot is not by itself',
            'proof that interpolation caused the source discrepancy.','',
            '|Model|Field|Native curvature change %|Anchor slope-jump / mean slope %|Diagnostic norm|',
            '|---|---|---:|---:|---|']
    for row in histories:
        lines.append(f"|{row['model']}|{row['field']}|{100*row['relative_curvature_change']:.10g}|{100*row['anchor_slope_jump_relative']:.10g}|{row['norm']}|")
    lines+=['','These native-field norms differ from the source norm; they are not new pass/fail',
            'gates and cannot identify their collision-weighted contribution by themselves.','',
            '## What is identified, and the next discriminating calculation',
            'The fixed/history-dependent and matched-component splits are determined by the',
            'saved source vectors. Interpolation error versus genuine history curvature versus',
            'mixed operator/history evolution is NOT separately determined by this bank.',
            'DERIVATION.md gives the exact mixed/curvature identity and its missing crossed',
            'actions A(+h)h(-h) and A(-h)h(+h), at BOTH existing step sizes.',
            'Next evaluate those crossed actions first in the virtual/Born channel carrying',
            'the discrepancy, reusing saved loop scalars and the existing Born formula.',
            'That first separation does not need the expensive real-emission integrals.',
            'Retain the baseline moving/fixed controls and extend to other components only',
            'if their remaining contribution requires it. This tests the two contributions',
            'without smoothing a history, fitting a temperature curve or changing a tolerance.',
            'Until then keep the new-node curvature flag and the successful frozen prediction',
            'as separate outcomes; the five-node partial-sum pass does not erase the flag.','',
            '## Integrity',
            f"{status['count']} rebuilt diagnostic protocol/identity/precision checks pass.",
            'Legacy rounding failures remain separately recorded; no tolerance was relaxed.',
            f"{len(status['authenticated_parent_inputs'])} parent/consumed paths authenticated before and after.",
            '180 stencil packets reused; frozen predictions and target vectors reused unchanged.',
            'Zero new source evaluations, no integration/transport rerun, no GitHub or subagents.',
            f"Protected workbench mtime count: {status['protected_modified_file_count']}.",
            'Earlier work preserved. The diagnosis is local to this finite quadrature and',
            'these saved histories; it is not a new full-spectrum or continuum bound.','']
    (ROOT/'RESULTS.md').write_text('\n'.join(lines),encoding='utf-8')


def seal():
    status=verify()
    destination=ROOT/'results/stage-integrity.json'
    assert not destination.exists() and (ROOT/'RESULTS.md').exists()
    assert json.loads((ROOT/'progress.json').read_text())['state']=='analysis_complete'
    parent_path=PARENT/'results/stage-integrity.json'
    assert saved.digest(parent_path)==PARENT_SHA
    parent=json.loads(parent_path.read_text())
    for filename,checksum in status['authenticated_parent_inputs'].items():
        assert saved.digest(filename)==checksum,filename
    import psutil
    for process in psutil.process_iter(['pid','name','cmdline']):
        if process.info['pid']==os.getpid():
            continue
        command=' '.join(process.info['cmdline'] or [])
        assert not ('isolate_stage177.py' in command and 'python' in (process.info['name'] or '').lower()),command
    assert not list(ROOT.rglob('__pycache__'))
    inherited=parent['inherited_sealed_payload_count']+len(parent['file_hashes'])
    assert inherited==335760
    carried_names=['checkpoint_manifest_sha256','local_source_documents','primary_pdfs','source_urls',
                   'observational_source_urls','original_library_sha256','native_library_sha256',
                   'physical_source_scope','retained_local_approximation_histories',
                   'raw_subtraction_response_retained','raw_failed_history_response_retained']
    carried={key:value for key,value in parent.items() if key in carried_names or key.startswith('latest_')}
    hashes={path.relative_to(ROOT).as_posix():saved.digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path!=destination}
    largest=max(sum(path.is_file() for path in folder.iterdir()) for folder in [ROOT,*[path for path in ROOT.rglob('*') if path.is_dir()]])
    assert largest<=500
    packet=dict(state='complete',stage=177,sealed_at_utc=datetime.now(timezone.utc).isoformat(),
                parent_seal_sha256=PARENT_SHA,inherited_sealed_payload_count=inherited,file_hashes=hashes,**carried,
                consumed_and_immediate_rehashed={**status['authenticated_parent_inputs'],str(parent_path):PARENT_SHA},
                previous_primary_source_urls=parent.get('previous_primary_source_urls',[])+parent.get('new_primary_source_urls',[]),
                new_primary_source_urls=[],prior_archive_full_rehash_performed=False,
                prior_archive_verification_seal_sha256=parent['prior_archive_verification_seal_sha256'],
                prior_payload_verification_scope='Immediate Stage176 and its consumed inputs rehashed; older archive inherited through seals.',
                accepted_current_scope_verified=True,
                accepted_scope='Saved-source curvature decomposition and arithmetic checks; new-node curvature failure retained.',
                latest_curvature_history_isolation=str(ROOT/'RESULTS.md'),final_validation=str(ROOT/'results/status.json'),
                validation_checks=status['count'],new_source_evaluations=0,reused_stencil_events=180,
                incoming_frequency=18.449187113596366,incoming_panel_complete=False,
                full_population_integral=False,full_population_source_temperature_law_certified=False,
                native_incident_histories_are_inputs=True,native_history_classical_second_derivative_claimed=False,
                derivative_numbers_are_finite_difference_evaluations=True,post_test_diagnostic=True,
                history_artifact_proved=False,new_node_matched_moving_curvature_gate_passed=False,
                source_curve_changed=False,temperature_curve_changed=False,current_history_replaced=False,
                tolerances_changed=False,baseline_preserved=True,independent_raw_physical_source_qualified=False,
                retained_failed_checks=parent.get('retained_failed_checks',[])+[
                    dict(row,packet='Stage177 legacy_roundoff') for row in read('legacy-roundoff-checks') if not row['passed']],
                current_stage_retained_failures=status['legacy_roundoff_failed_checks'],
                diagnostic_arithmetic_rebuilt_from_saved_primitive_components=True,
                first_attempt_failures_preserved='attempt-01-rounded-differences/results/status.json',
                scientific_failure_inherited=True,global_numerical_error_bound=None,
                protected_workbench_recent_modified_file_count=status['protected_modified_file_count'],
                protected_check_scope=status['protected_check_scope'],maximum_active_workers=1,active_workers_at_seal=0,
                library_threads_per_worker=1,largest_direct_file_count=largest,github_action=False,subagents=0,
                global_installation_changed=False,galaxy_work_modified=False,next_target_file=str(ROOT/'RESULTS.md'))
    saved.write_json(destination,packet)
    assert all(saved.digest(ROOT/name)==checksum for name,checksum in hashes.items())
    print(json.dumps(dict(sealed_files=len(hashes),cumulative_payloads=inherited+len(hashes),seal_sha256=saved.digest(destination))),flush=True)


if __name__=='__main__':
    source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['report','seal'])
    arguments=parser.parse_args()
    report() if arguments.phase=='report' else seal()
