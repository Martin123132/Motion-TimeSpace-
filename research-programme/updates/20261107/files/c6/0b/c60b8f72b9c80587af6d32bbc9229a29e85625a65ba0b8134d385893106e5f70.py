from anchor_stage179 import *


def verify():
    status = read(ROOT/'results/status.json')
    assert status['all_checks_passed'] and (ROOT/'results/COMPLETE').exists()
    for filename,checksum in status['input_hashes'].items():
        assert saved.digest(filename) == checksum,filename
    return status


def report():
    status = verify()
    records = read(ROOT/'results/projection-shares.json')
    controls = read(ROOT/'results/saved-baseline-controls.json')
    def chosen(width,reference,history,term):
        return next(row for row in records if (row['width'],row['reference'],row['history'],row['term'])==(width,reference,history,term))
    lines = ['# Stage179 — history curvature with the operator frozen at its anchor','',
        'Post-test virtual/Born diagnostic at incoming x=18.449187113596366.',
        'The same anchor kinematics, event weight, vacuum coefficient and cached loop',
        'scalar were used for all five histories: anchor and the four saved side histories.',
        'No real-emission or new loop integration was performed.','',
        '## What this now separates','',
        'The Stage178 transmitted term H_s=A_average_s C_s[h] splits exactly into',
        'U_s=A0 C_s[h] and W_s=(A_average_s-A0) C_s[h]. Here A0 is one fixed',
        'anchor operator, and the histories and finite widths are unchanged.',
        'We compare both widths (.01 and .005) and their difference before rounding.',
        'This separates curvature of the saved incident history from the remaining',
        'average-operator correction. It does not assume that the history is erroneous.','',
        '## Within the previously transmitted discrepancy','',
        '|History column|Anchor-history signed %|Average-operator signed %|Anchor-history norm / transmitted norm|Average-operator norm / transmitted norm|',
        '|---|---:|---:|---:|---:|']
    for history in range(4):
        anchor = chosen('discrepancy','transmitted_history_curvature',history,'anchor_history_curvature')
        average = chosen('discrepancy','transmitted_history_curvature',history,'average_operator_change')
        lines.append(f"|{history}|{100*anchor['signed_share']:.10g}|{100*average['signed_share']:.10g}|{anchor['norm_ratio']:.10g}|{average['norm_ratio']:.10g}|")
    lines += ['','Only these two components sum to100% of the transmitted discrepancy.',
        'Shares are signed projections in the inherited mass-dual photon metric;',
        'they are not causal probabilities or error percentages. Norms need not add.','',
        '## Full matched discrepancy','',
        '|History column|Fixed virtual %|Mixed virtual %|Anchor-history %|Average-operator %|Nonvirtual %|Cancellation factor|',
        '|---|---:|---:|---:|---:|---:|---:|']
    for history in range(4):
        shares = '|'.join(f"{100*chosen('discrepancy','moving_matched',history,term)['signed_share']:.10g}" for term in TERMS[:5])
        lines.append(f"|{history}|{shares}|{status['cancellation_factor'][2][history]:.10g}|")
    lines += ['','All five contributions close against the original matched discrepancy.',
        'Nonvirtual is the saved real-minus-control difference plus state response.',
        'Columns0/1 are heavy-background join controls; columns2/3 are cold-background',
        'join controls, with both saved low-frequency joins preserved.','',
        '## Full curvature is distinct from its width discrepancy','',
        '|Width|History column|Fixed virtual %|Mixed virtual %|Anchor-history %|Average-operator %|',
        '|---|---:|---:|---:|---:|---:|']
    for width in ['coarse','fine']:
        for history in range(4):
            shares = '|'.join(f"{100*chosen(width,'moving_virtual',history,term)['signed_share']:.10g}" for term in TERMS[:4])
            lines.append(f"|{width}|{history}|{shares}|")
    lines += ['','These full-curvature pieces can be large and cancel. A small contribution',
        'to the width discrepancy does not justify dropping that term from the source.',
        'Projection-shares.json also records individual norms for every reference.','',
        '## Baseline and original MTS controls retained','',
        '|Component|Moving curvature change %|Fixed curvature change %|Moving passes /4|Fixed passes /4|',
        '|---|---:|---:|---:|---:|']
    for component in ['control','remainder','total']:
        moving = [row for row in controls if row['branch']=='moving_history' and row['component']==component]
        fixed = [row for row in controls if row['branch']=='fixed_incident' and row['component']==component]
        lines.append(f"|{component}|{100*max(row['relative'] for row in moving):.10g}|{100*max(row['relative'] for row in fixed):.10g}|{sum(row['passed'] for row in moving)}|{sum(row['passed'] for row in fixed)}|")
    lines += ['','The leading real baseline has no separate MTS virtual correction. Its saved',
        'moving/fixed controls were reused, not called a newly crossed real integral.',
        'The original1.03659637% matched moving-history curvature flag and original',
        'frozen prediction outcomes remain unchanged. No acceptance threshold changed.','',
        '## Validation and provenance','',
        f"- {status['count']} diagnostic checks pass, including unchanged1e-10 identities and precision checks.",
        '-144 new side-history actions use36 cached anchor loop scalars.',
        f"-{status['bitwise_anchor_reproductions']}/36 anchor actions reproduce saved high/low arrays bit for bit.",
        '-All180 source stencil packets and144 Stage178 crossed packets are reused.',
        '-Born linearity is checked on sum, difference and zero histories at both widths.',
        '-Finite-width decompositions are reconstructed at80digits and independently at100digits.',
        '-Precision of this arithmetic does not certify the integration error of old packets.',
        f"-{len(status['authenticated_parent_inputs'])} immediate-parent and consumed paths authenticated before/after.",
        '-Older seals and failed checks remain intact; no full historical archive rehash claimed.',
        f"-Protected workbench recent-mtime count:{status['protected_modified_file_count']}.",
        '-One below-normal worker, one thread per numerical library; no subagents or GitHub.','',
        'Result-driven next calculation: INTERPRETATION.md.','']
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
        assert not ('anchor_stage179.py' in command and 'python' in (process.info['name'] or '').lower()),command
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    assert not list(ROOT.rglob('__pycache__'))
    parent = read(PARENT/'results/stage-integrity.json')
    inherited = parent['inherited_sealed_payload_count']+len(parent['file_hashes'])
    assert inherited == 335957
    carry_names = ['checkpoint_manifest_sha256','local_source_documents','primary_pdfs','source_urls',
        'observational_source_urls','original_library_sha256','native_library_sha256','physical_source_scope',
        'retained_local_approximation_histories','raw_subtraction_response_retained','raw_failed_history_response_retained']
    carried = {key:value for key,value in parent.items() if key in carry_names or key.startswith('latest_')}
    hashes = {path.relative_to(ROOT).as_posix():saved.digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path != destination}
    largest = max(sum(path.is_file() for path in folder.iterdir()) for folder in [ROOT,*[path for path in ROOT.rglob('*') if path.is_dir()]])
    assert largest <= 500
    packet = dict(state='complete',stage=179,sealed_at_utc=datetime.now(timezone.utc).isoformat(),
        parent_seal_sha256=PARENT_SHA,inherited_sealed_payload_count=inherited,file_hashes=hashes,**carried,
        consumed_and_immediate_rehashed=authenticated,
        previous_primary_source_urls=parent.get('previous_primary_source_urls',[])+parent.get('new_primary_source_urls',[]),
        new_primary_source_urls=[],prior_archive_full_rehash_performed=False,
        prior_archive_verification_seal_sha256=parent['prior_archive_verification_seal_sha256'],
        prior_payload_verification_scope='Immediate Stage178 and consumed inputs rehashed; older archive inherited through seals.',
        accepted_current_scope_verified=True,accepted_scope='Anchor-frozen virtual/Born history curvature separated from average-operator correction.',
        latest_anchor_operator_history_curvature=str(ROOT/'RESULTS.md'),final_validation=str(ROOT/'results/status.json'),
        validation_checks=status['count'],new_history_actions=144,anchor_reproductions=36,bitwise_anchor_reproductions=36,
        reused_stencil_events=180,reused_crossed_packets=144,reused_anchor_loops=36,
        real_emission_integrations=0,new_loop_integrations=0,incoming_frequency=18.449187113596366,
        incoming_panel_complete=False,full_population_integral=False,full_population_source_temperature_law_certified=False,
        native_incident_histories_are_inputs=True,native_history_classical_second_derivative_claimed=False,
        derivative_numbers_are_finite_difference_evaluations=True,operator_frozen_at_anchor=True,
        post_test_diagnostic=True,history_artifact_proved=False,
        new_node_matched_moving_curvature_gate_passed=status['new_node_matched_moving_curvature_gate_passed'],
        source_curve_changed=False,temperature_curve_changed=False,current_history_replaced=False,tolerances_changed=False,
        baseline_preserved=True,crossed_real_baseline_evaluated=False,independent_raw_physical_source_qualified=False,
        retained_failed_checks=parent.get('retained_failed_checks',[]),current_stage_retained_failures=0,
        scientific_failure_inherited=True,global_numerical_error_bound=None,
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
