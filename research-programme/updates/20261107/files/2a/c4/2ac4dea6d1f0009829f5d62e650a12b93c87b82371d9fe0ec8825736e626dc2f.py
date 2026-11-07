from split_stage180 import *


def verify():
    status = read(ROOT/'results/precision/status.json')
    assert status['all_checks_passed'] and (ROOT/'results/precision/COMPLETE').exists()
    for filename,checksum in status['input_hashes'].items():
        assert saved.digest(filename)==checksum,filename
    initial = read(ROOT/'results/status.json')
    assert not initial['all_checks_passed']
    assert len([row for row in initial['checks'] if not row['passed']])==3
    for filename,checksum in initial['input_hashes'].items():
        assert saved.digest(filename)==checksum,filename
    return status,initial


def report():
    status,initial = verify()
    shares = read(ROOT/'results/precision/projection-shares.json')
    gas_law = read(ROOT/'results/precision/native-gas-law.json')
    controls = read(ROOT/'results/saved-baseline-controls.json')
    def chosen(width,reference,history,term):
        return next(row for row in shares if (row['width'],row['reference'],row['history'],row['term'])==(width,reference,history,term))
    lines = ['# Stage180 — photon/gas history split at the fixed anchor','',
        'The discrepancy is dominated by the incident gas history, with a smaller',
        'opposing photon-history contribution. No history or temperature curve was fitted.',
        'This is a post-test virtual/Born diagnostic at x=18.449187113596366.',
        'The operators, cached loop scalars, baseline controls and tolerances stay fixed.','',
        '## Fixed-anchor history discrepancy','',
        '|History column|Photon signed %|Gas signed %|Photon norm / anchor norm|Gas norm / anchor norm|Cancellation factor|',
        '|---|---:|---:|---:|---:|---:|']
    for history in range(4):
        photon = chosen('discrepancy','anchor_history',history,'photon')
        gas = chosen('discrepancy','anchor_history',history,'gas')
        lines.append(f"|{history}|{100*photon['signed_share']:.10g}|{100*gas['signed_share']:.10g}|{photon['norm_ratio']:.10g}|{gas['norm_ratio']:.10g}|{status['cancellation_factor'][2][history]:.10g}|")
    lines += ['','Signed projections use the inherited mass-dual photon metric. They are not',
        'probabilities or estimates of interpolation error. Opposite signs mean cancellation.',
        'Both incident channels retain photon output and opposite gas-energy transfer.',
        'Columns0/1 are heavy-background join controls and2/3 cold-background controls.','',
        '## Full matched discrepancy','',
        '|History column|Photon signed %|Gas signed %|Representation residual norm / matched norm|',
        '|---|---:|---:|---:|']
    for history in range(4):
        photon = chosen('discrepancy','matched',history,'photon')
        gas = chosen('discrepancy','matched',history,'gas')
        residual = chosen('discrepancy','matched',history,'representation_residual')
        lines.append(f"|{history}|{100*photon['signed_share']:.10g}|{100*gas['signed_share']:.10g}|{residual['norm_ratio']:.10g}|")
    lines += ['','Add the unchanged Stage179 fixed/mixed virtual, average-operator and nonvirtual',
        'terms, plus the explicit numerical-representation residual, for full saved closure.',
        'The residual is not assigned to either physical channel.','',
        '## Curvature before taking its width difference','',
        '|Width|History column|Photon signed % of anchor curvature|Gas signed %|Cancellation factor|',
        '|---|---:|---:|---:|---:|']
    for order,width in enumerate(['coarse','fine']):
        for history in range(4):
            photon = chosen(width,'anchor_history',history,'photon')
            gas = chosen(width,'anchor_history',history,'gas')
            lines.append(f"|{width}|{history}|{100*photon['signed_share']:.10g}|{100*gas['signed_share']:.10g}|{status['cancellation_factor'][order][history]:.10g}|")
    lines += ['','Full curvature has stronger cancellation than its width discrepancy. Do not',
        'delete the photon term merely because the gas dominates the discrepancy.','',
        '## A derived and independently checked gas law','',
        'With fixed A0, K_g=A0[0,1] gives U_gas_s=K_g*C_s[g]. K_g was independently',
        'evaluated as a unit-gas action, not fitted to the gas response. The ORIGINAL',
        'unit-gas packets predict the higher-precision gas curvature and discrepancy.','',
        '|History column|Native gas curvature change %|Precise gas-source change %|Independent unit-law relative error|',
        '|---|---:|---:|---:|']
    for row in gas_law:
        lines.append(f"|{row['history']}|{100*row['native_relative_curvature_change']:.10g}|{100*row['precise_gas_relative_curvature_change']:.10g}|{row['unit_prediction_relative_error']:.10g}|")
    lines += ['','This directly maps the saved gas curvature into the virtual response. It does',
        'not establish whether that curvature is physical, finite-width truncation,',
        'or a native-history integration/interpolation error.','',
        '## Precision checks: failures retained, not relaxed','',
        f"- Initial split: {initial['count']-3}/{initial['count']} checks passed;3 discrepancy-level1e-10 failures remain recorded.",
        '- Shared primitive Born arithmetic is now carried through the channel split and',
        '  curvature subtraction before rounding, with high/low storage on all source rows.',
        f"- {status['count']} repaired diagnostic checks pass at unchanged tolerances;80/100-digit arrays agree.",
        '-3 additional old/new discrepancy compatibility checks fail1e-10 and remain flagged.',
        f"- All{len(status['retained_failed_checks'])} flags are included in the final status/seal. See PRECISION-NOTES.md.",
        f"- Combined old/new discrepancy relative difference is at most{status['max_saved_combined_discrepancy_relative']:.10g}.",
        '- Original180 combined responses reproduced bit for bit before the precision rebuild.',
        '- No original packets, predictions or acceptance decisions are overwritten.','',
        '## Baseline and original source outcomes','',
        '|Component|Moving curvature change %|Fixed curvature change %|Moving passes /4|Fixed passes /4|',
        '|---|---:|---:|---:|---:|']
    for component in ['control','remainder','total']:
        moving = [row for row in controls if row['branch']=='moving_history' and row['component']==component]
        fixed = [row for row in controls if row['branch']=='fixed_incident' and row['component']==component]
        lines.append(f"|{component}|{100*max(row['relative'] for row in moving):.10g}|{100*max(row['relative'] for row in fixed):.10g}|{sum(row['passed'] for row in moving)}|{sum(row['passed'] for row in fixed)}|")
    lines += ['','The real baseline controls are reused, not relabelled as new virtual corrections.',
        'Source1% gates, baseline histories and earlier scientific failures stay unchanged.','',
        '## Integrity and next action','',
        f"{len(status['authenticated_parent_inputs'])} immediate-parent/consumed paths authenticated before/after.",
        'Older archive inherited through seals; no new full historical rehash claimed.',
        f"Protected workbench recent-mtime count:{status['protected_modified_file_count']}.",
        'One below-normal worker, single-thread libraries, no new loop/real-emission',
        'integrals, subagents or GitHub actions. All work stays local.',
        'Next: the gas-energy-balance derivation and saved-history test in INTERPRETATION.md.','']
    (ROOT/'RESULTS.md').write_text('\n'.join(lines),encoding='utf-8')


def seal():
    status,initial = verify()
    assert read(ROOT/'precision-progress.json')['state']=='analysis_complete'
    assert (ROOT/'RESULTS.md').exists() and (ROOT/'INTERPRETATION.md').exists() and (ROOT/'PRECISION-NOTES.md').exists()
    destination = ROOT/'results/stage-integrity.json'
    assert not destination.exists()
    authenticated = authenticate()
    assert authenticated==status['authenticated_parent_inputs']
    import psutil
    for process in psutil.process_iter(['pid','name','cmdline']):
        if process.info['pid']==os.getpid():
            continue
        command = ' '.join(process.info['cmdline'] or [])
        assert not (('split_stage180.py' in command or 'precise_stage180.py' in command) and 'python' in (process.info['name'] or '').lower()),command
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    assert not list(ROOT.rglob('__pycache__'))
    parent = read(PARENT/'results/stage-integrity.json')
    inherited = parent['inherited_sealed_payload_count']+len(parent['file_hashes'])
    assert inherited==336009
    carry_names = ['checkpoint_manifest_sha256','local_source_documents','primary_pdfs','source_urls',
        'observational_source_urls','original_library_sha256','native_library_sha256','physical_source_scope',
        'retained_local_approximation_histories','raw_subtraction_response_retained','raw_failed_history_response_retained']
    carried = {key:value for key,value in parent.items() if key in carry_names or key.startswith('latest_')}
    hashes = {path.relative_to(ROOT).as_posix():saved.digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path!=destination}
    largest = max(sum(path.is_file() for path in folder.iterdir()) for folder in [ROOT,*[path for path in ROOT.rglob('*') if path.is_dir()]])
    assert largest<=500
    next_sources = [BRANCH/'infrared-source-domain-20261008/evolve_nonlocal_background.py',
        BRANCH/'infrared-source-domain-20261008/nonlocal_common.py',
        BRANCH/'emitting-thermal-background-20261008/evolve_emitting_background.py']
    packet = dict(state='complete',stage=180,sealed_at_utc=datetime.now(timezone.utc).isoformat(),
        parent_seal_sha256=PARENT_SHA,inherited_sealed_payload_count=inherited,file_hashes=hashes,**carried,
        consumed_and_immediate_rehashed=authenticated,
        previous_primary_source_urls=parent.get('previous_primary_source_urls',[])+parent.get('new_primary_source_urls',[]),
        new_primary_source_urls=[],prior_archive_full_rehash_performed=False,
        prior_archive_verification_seal_sha256=parent['prior_archive_verification_seal_sha256'],
        prior_payload_verification_scope='Immediate Stage179 and consumed inputs rehashed; older archive inherited through seals.',
        accepted_current_scope_verified=True,accepted_scope='Shared-precision photon/gas split and unit-gas law; six legacy precision failures explicitly retained.',
        latest_anchor_photon_gas_history_split=str(ROOT/'RESULTS.md'),final_validation=str(ROOT/'results/precision/status.json'),
        initial_validation=str(ROOT/'results/status.json'),validation_checks=status['count'],initial_validation_checks=initial['count'],
        current_stage_retained_failures=len(status['retained_failed_checks']),all_raw_and_legacy_checks_passed=False,
        retained_failed_checks=parent.get('retained_failed_checks',[])+status['retained_failed_checks'],
        separated_history_actions=360,combined_history_reproductions=180,bitwise_combined_reproductions=180,
        unit_gas_actions=36,reused_anchor_loops=36,real_emission_integrations=0,new_loop_integrations=0,
        incoming_frequency=18.449187113596366,incoming_panel_complete=False,full_population_integral=False,
        full_population_source_temperature_law_certified=False,native_incident_histories_are_inputs=True,
        native_history_classical_second_derivative_claimed=False,derivative_numbers_are_finite_difference_evaluations=True,
        operator_frozen_at_anchor=True,post_test_diagnostic=True,history_artifact_proved=False,
        new_node_matched_moving_curvature_gate_passed=initial['new_node_matched_moving_curvature_gate_passed'],
        source_curve_changed=False,temperature_curve_changed=False,current_history_replaced=False,tolerances_changed=False,
        baseline_preserved=True,crossed_real_baseline_evaluated=False,original_source_packets_replaced=False,
        original_predictions_replaced=False,independent_raw_physical_source_qualified=False,
        scientific_failure_inherited=True,global_numerical_error_bound=None,
        protected_workbench_recent_modified_file_count=status['protected_modified_file_count'],
        protected_check_scope=status['protected_check_scope'],maximum_active_workers=1,active_workers_at_seal=0,
        library_threads_per_worker=1,largest_direct_file_count=largest,github_action=False,subagents=0,
        global_installation_changed=False,galaxy_work_modified=False,
        next_equation_source_hashes={str(path):saved.digest(path) for path in next_sources},next_target_file=str(ROOT/'INTERPRETATION.md'))
    saved.write_json(destination,packet)
    assert all(saved.digest(ROOT/name)==checksum for name,checksum in hashes.items())
    print(json.dumps(dict(sealed_files=len(hashes),cumulative_payloads=inherited+len(hashes),seal_sha256=saved.digest(destination))),flush=True)


if __name__=='__main__':
    source.modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('phase',choices=['report','seal'])
    args = parser.parse_args()
    report() if args.phase=='report' else seal()
