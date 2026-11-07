from cross_stage178 import *


def verify():
    status = read(ROOT/'results/status.json')
    assert status['all_checks_passed'] and (ROOT/'results/COMPLETE').exists()
    for filename, checksum in status['input_hashes'].items():
        assert saved.digest(filename) == checksum, filename
    return status


def report():
    status = verify()
    records = read(ROOT/'results/projection-shares.json')
    controls = read(ROOT/'results/saved-baseline-controls.json')
    widths = read(ROOT/'results/width-decomposition.json')
    lines = ['# Stage178 — crossed-history virtual/Born response','',
        'Post-test diagnostic at incoming x=18.449187113596366. The temperature curve,',
        'saved histories, frequency bands, integration settings and tolerances are unchanged.',
        'The operator at each temperature was applied to its opposite-temperature history,',
        'using the cached loop scalar and existing Born map. No real-emission integral',
        'or new loop integral was performed.','',
        '## Exact separation','',
        'At BOTH existing widths .01 and .005, the moving virtual curvature splits into:',
        '- fixed-history operator curvature;',
        '- mixed first-difference operator/history response;',
        '- the average operator acting on incident-history curvature.','',
        'The difference between the two widths inherits this exact decomposition.',
        'The third term still uses a width-dependent average operator: it is not an',
        'operator-free measure of history curvature. The algebra does not establish',
        'that the history is erroneous, nor that an interpolation knot is the cause.','',
        '## Signed contributions to the matched discrepancy','',
        'Each share is a projection in the inherited mass-dual photon norm, not a',
        'probability, variance fraction or causal percentage. Negative and >100% shares',
        'are allowed. The unaltered difference+state vector is included for closure.','',
        '|History column|Fixed virtual %|Mixed virtual %|Transmitted history curvature %|Other matched terms %|Cancellation factor|',
        '|---|---:|---:|---:|---:|---:|']
    term_names = ['fixed_operator','mixed_operator_history','transmitted_history_curvature','nonvirtual_matched']
    for history in range(4):
        selected = {row['term']:row for row in records if row['reference']=='moving_matched' and row['history']==history}
        shares = '|'.join(f"{100*selected[name]['signed_share']:.10g}" for name in term_names)
        lines.append(f"|{history}|{shares}|{status['cancellation_factor'][history]:.10g}|")
    lines += ['','History columns 0/1 are heavy-background join controls; 2/3 are cold-background',
        'join controls. The two columns in each background use the saved low-frequency joins.','',
        '## Size as well as alignment','',
        '|History column|Term|Norm / matched discrepancy norm|Signed share of virtual discrepancy %|',
        '|---|---|---:|---:|']
    for history in range(4):
        for term in term_names:
            matched = next(row for row in records if (row['reference'],row['history'],row['term'])==('moving_matched',history,term))
            virtual = next(row for row in records if (row['reference'],row['history'],row['term'])==('moving_virtual',history,term))
            lines.append(f"|{history}|{term}|{matched['norm_ratio']:.10g}|{100*virtual['signed_share']:.10g}|")
    lines += ['','Only the three virtual terms sum to100% of the virtual discrepancy.',
        'All four terms sum to100% of the matched discrepancy. Norms do not add.','',
        '## Coarse and fine virtual curvature separately','',
        '|Width|History column|Fixed signed %|Mixed signed %|History-curvature signed %|',
        '|---|---:|---:|---:|---:|']
    for width in ['coarse','fine']:
        for history in range(4):
            selected = {row['term']:row for row in widths if row['width']==width and row['history']==history}
            shares = '|'.join(f"{100*selected[name]['signed_share']:.10g}" for name in ['fixed','mixed','history_curvature'])
            lines.append(f"|{width}|{history}|{shares}|")
    lines += ['','## Identical baseline controls and retained outcomes','',
        '|Component|Moving curvature change %|Fixed curvature change %|Moving passes /4|Fixed passes /4|',
        '|---|---:|---:|---:|---:|']
    for component in ['control','remainder','total']:
        moving = [row for row in controls if row['branch']=='moving_history' and row['component']==component]
        fixed = [row for row in controls if row['branch']=='fixed_incident' and row['component']==component]
        lines.append(f"|{component}|{100*max(row['relative'] for row in moving):.10g}|{100*max(row['relative'] for row in fixed):.10g}|{sum(row['passed'] for row in moving)}|{sum(row['passed'] for row in fixed)}|")
    lines += ['','Control is the leading real microscopic baseline. Remainder is the matched',
        'MTS difference+virtual+state increment. Total includes both. The baseline',
        'has no separate MTS virtual correction; its saved moving/fixed controls were',
        'reused, not relabelled as newly evaluated crossed real-emission sources.',
        'The new-node 1.03659637% matched moving curvature flag remains failed at the',
        'unchanged1% gate. The saved target prediction and five-node partial results',
        'are unchanged. This test explains structure; it does not replace them.','',
        '## Validation and integrity','',
        f"- {status['count']} protocol, reproduction, linearity, moment and arithmetic checks pass at their unchanged thresholds.",
        '-144 opposite-history actions evaluated;288 same/fixed-history actions reproduced.',
        '-180 original stencil packets reused;144 original loop scalars reused.',
        '-At every operator temperature, summed/differenced/zero histories test Born linearity independently.',
        '-The finite-width split and source sums are reconstructed at80digits and independently at100digits.',
        '-Precision of that arithmetic does not certify integration errors inside saved source packets.',
        f"-{len(status['authenticated_parent_inputs'])} immediate-parent and consumed paths authenticated before/after.",
        '-Older failed checks remain in their original stages and inherited seal; none reclassified.',
        f"-Protected workbench recent-mtime count: {status['protected_modified_file_count']} (not a historical full hash snapshot).",
        '-One worker, one thread per numerical library; no subagents, remote actions or installs.','',
        'See INTERPRETATION.md for the result-driven next calculation.','']
    (ROOT/'RESULTS.md').write_text('\n'.join(lines),encoding='utf-8')


def seal():
    status = verify()
    assert (ROOT/'RESULTS.md').exists() and (ROOT/'INTERPRETATION.md').exists()
    assert read(ROOT/'progress.json')['state'] == 'analysis_complete'
    destination = ROOT/'results/stage-integrity.json'
    assert not destination.exists()
    authenticated = authenticate()
    assert authenticated == status['authenticated_parent_inputs']
    import psutil
    for process in psutil.process_iter(['pid','name','cmdline']):
        if process.info['pid'] == os.getpid():
            continue
        command = ' '.join(process.info['cmdline'] or [])
        assert not ('cross_stage178.py' in command and 'python' in (process.info['name'] or '').lower()),command
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    assert not list(ROOT.rglob('__pycache__'))
    parent = read(PARENT/'results/stage-integrity.json')
    inherited = parent['inherited_sealed_payload_count']+len(parent['file_hashes'])
    assert inherited == 335796
    carry_names = ['checkpoint_manifest_sha256','local_source_documents','primary_pdfs','source_urls',
        'observational_source_urls','original_library_sha256','native_library_sha256','physical_source_scope',
        'retained_local_approximation_histories','raw_subtraction_response_retained','raw_failed_history_response_retained']
    carried = {key:value for key,value in parent.items() if key in carry_names or key.startswith('latest_')}
    hashes = {path.relative_to(ROOT).as_posix():saved.digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path != destination}
    largest = max(sum(path.is_file() for path in folder.iterdir()) for folder in [ROOT,*[path for path in ROOT.rglob('*') if path.is_dir()]])
    assert largest <= 500
    packet = dict(state='complete',stage=178,sealed_at_utc=datetime.now(timezone.utc).isoformat(),
        parent_seal_sha256=PARENT_SHA,inherited_sealed_payload_count=inherited,file_hashes=hashes,**carried,
        consumed_and_immediate_rehashed=authenticated,
        previous_primary_source_urls=parent.get('previous_primary_source_urls',[])+parent.get('new_primary_source_urls',[]),
        new_primary_source_urls=[],prior_archive_full_rehash_performed=False,
        prior_archive_verification_seal_sha256=parent['prior_archive_verification_seal_sha256'],
        prior_payload_verification_scope='Immediate Stage177 and consumed inputs rehashed; older archive inherited through seals.',
        accepted_current_scope_verified=True,accepted_scope='Crossed virtual/Born finite-width attribution with unchanged source gates.',
        latest_crossed_history_virtual_response=str(ROOT/'RESULTS.md'),final_validation=str(ROOT/'results/status.json'),
        validation_checks=status['count'],crossed_actions=144,reproduced_diagonal_actions=288,reused_stencil_events=180,
        real_emission_integrations=0,new_loop_integrations=0,incoming_frequency=18.449187113596366,
        incoming_panel_complete=False,full_population_integral=False,full_population_source_temperature_law_certified=False,
        native_incident_histories_are_inputs=True,native_history_classical_second_derivative_claimed=False,
        derivative_numbers_are_finite_difference_evaluations=True,post_test_diagnostic=True,history_artifact_proved=False,
        new_node_matched_moving_curvature_gate_passed=False,source_curve_changed=False,temperature_curve_changed=False,
        current_history_replaced=False,tolerances_changed=False,baseline_preserved=True,crossed_real_baseline_evaluated=False,
        independent_raw_physical_source_qualified=False,retained_failed_checks=parent.get('retained_failed_checks',[]),
        current_stage_retained_failures=0,scientific_failure_inherited=True,global_numerical_error_bound=None,
        protected_workbench_recent_modified_file_count=status['protected_modified_file_count'],
        protected_check_scope=status['protected_check_scope'],maximum_active_workers=1,active_workers_at_seal=0,
        library_threads_per_worker=1,largest_direct_file_count=largest,github_action=False,subagents=0,
        global_installation_changed=False,galaxy_work_modified=False,next_target_file=str(ROOT/'INTERPRETATION.md'))
    saved.write_json(destination,packet)
    assert all(saved.digest(ROOT/name)==checksum for name,checksum in hashes.items())
    print(json.dumps(dict(sealed_files=len(hashes),cumulative_payloads=inherited+len(hashes),seal_sha256=saved.digest(destination))),flush=True)


if __name__ == '__main__':
    source.modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('phase',choices=['report','seal'])
    args = parser.parse_args()
    report() if args.phase == 'report' else seal()
