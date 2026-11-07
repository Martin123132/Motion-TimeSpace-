from split_stage180 import *


def verify():
    status = read(ROOT/'results/status.json')
    assert status['all_checks_passed'] and (ROOT/'results/COMPLETE').exists()
    for filename,checksum in status['input_hashes'].items():
        assert saved.digest(filename)==checksum,filename
    return status


def report():
    status = verify()
    records = read(ROOT/'results/projection-shares.json')
    controls = read(ROOT/'results/saved-baseline-controls.json')
    gas_law = read(ROOT/'results/native-gas-law.json')
    def chosen(width,reference,history,term):
        return next(row for row in records if (row['width'],row['reference'],row['history'],row['term'])==(width,reference,history,term))
    lines = ['# Stage180 — incident photon and gas histories at one fixed operator','',
        'Post-test diagnostic at incoming x=18.449187113596366, with every operator',
        'quantity fixed at the original anchor. The saved histories, temperature curve,',
        'quadrature, baseline controls and acceptance tolerances are unchanged.','',
        '## The channel split','',
        'The Born driving jump is phi(x_out)-phi(x_in)+r0*g. Photon-only and gas-only',
        'refer to incident departures, not output rows. Both channels retain photon',
        'energy response and its opposite gas-energy transfer. The combined response',
        'is reproduced independently; its numerical closure residual is measured',
        'rather than assigned to either channel to force agreement.','',
        '|Width|History column|Photon share of anchor-history %|Gas share %|Photon norm / anchor norm|Gas norm / anchor norm|Cancellation factor|',
        '|---|---:|---:|---:|---:|---:|---:|']
    for order,width in enumerate(['coarse','fine','discrepancy']):
        for history in range(4):
            photon = chosen(width,'anchor_history',history,'photon')
            gas = chosen(width,'anchor_history',history,'gas')
            lines.append(f"|{width}|{history}|{100*photon['signed_share']:.10g}|{100*gas['signed_share']:.10g}|{photon['norm_ratio']:.10g}|{gas['norm_ratio']:.10g}|{status['cancellation_factor'][order][history]:.10g}|")
    lines += ['','These are signed projections in the inherited mass-dual photon metric, not',
        'probabilities or causal error fractions. Opposite signs indicate cancellation.',
        'Columns0/1 are the heavy background and columns2/3 the cold background, with',
        'both saved low-frequency join choices. Full curvature and its width difference',
        'are different quantities; small discrepancy share does not justify deleting a term.','',
        '## Contributions to the full matched discrepancy','',
        '|History column|Photon signed %|Gas signed %|Photon norm / matched norm|Gas norm / matched norm|Closure residual norm / matched norm|',
        '|---|---:|---:|---:|---:|---:|']
    for history in range(4):
        photon = chosen('discrepancy','matched',history,'photon')
        gas = chosen('discrepancy','matched',history,'gas')
        residual = chosen('discrepancy','matched',history,'closure_residual')
        lines.append(f"|{history}|{100*photon['signed_share']:.10g}|{100*gas['signed_share']:.10g}|{photon['norm_ratio']:.10g}|{gas['norm_ratio']:.10g}|{residual['norm_ratio']:.10g}|")
    lines += ['','Add the unchanged Stage179 fixed/mixed virtual, average-operator and nonvirtual',
        'contributions to recover the full matched discrepancy. Their values and the',
        'saved combined-history vector were not refitted or replaced.','',
        '## Derived unit-gas amplitude law','',
        'An independent action on unit gas departure gives K_g=A0[0,1]. With this',
        'operator fixed, U_gas_s=K_g*C_s[g] and DeltaU_gas=K_g*DeltaC[g]. No fitted',
        'coefficient or division by a measured gas amplitude is used. The four unit',
        'kernel columns agree exactly; only the native gas histories differ.','',
        '|History column|Native gas curvature change %|Evaluated gas-source change %|Unit-kernel discrepancy prediction relative error|',
        '|---|---:|---:|---:|']
    for row in gas_law:
        lines.append(f"|{row['history']}|{100*row['native_relative_curvature_change']:.10g}|{100*row['evaluated_gas_relative_curvature_change']:.10g}|{row['frozen_unit_prediction_relative_error']:.10g}|")
    lines += ['','This factorization locates the saved contribution. It does not prove the native',
        'gas history inaccurate, or establish the physical cause of its curvature.','',
        '## Baseline and original acceptance outcomes','',
        '|Component|Moving curvature change %|Fixed curvature change %|Moving passes /4|Fixed passes /4|',
        '|---|---:|---:|---:|---:|']
    for component in ['control','remainder','total']:
        moving = [row for row in controls if row['branch']=='moving_history' and row['component']==component]
        fixed = [row for row in controls if row['branch']=='fixed_incident' and row['component']==component]
        lines.append(f"|{component}|{100*max(row['relative'] for row in moving):.10g}|{100*max(row['relative'] for row in fixed):.10g}|{sum(row['passed'] for row in moving)}|{sum(row['passed'] for row in fixed)}|")
    lines += ['','The leading real baseline has no separate MTS virtual correction. Its saved',
        'controls are retained, not relabelled as newly evaluated real integrals.',
        'Original1% source gates, frozen predictions and failed labels remain unchanged.','',
        '## Validation and integrity','',
        f"-{status['count']} diagnostic checks pass at the unchanged tolerances.",
        f"-{status['bitwise_combined_reproductions']}/180 combined high/low actions reproduce Stage179 bit for bit.",
        '-360 separated photon/gas actions and36 unit-gas controls reuse36 saved loop scalars.',
        '-Both curvatures and their discrepancy close against saved results at1e-10.',
        '-Independent80/100-digit accumulation checks the diagnostic arithmetic.',
        '-No real-emission or new loop integrals, propagation, fit, cutoff or smoothing.',
        f"-{len(status['authenticated_parent_inputs'])} immediate-parent/consumed paths authenticated before/after.",
        '-Older archive inherited through seals; no new full historical archive rehash claimed.',
        f"-Protected workbench recent-mtime count:{status['protected_modified_file_count']}.",
        '-One below-normal worker, single-thread libraries, no subagents or GitHub.','',
        'See INTERPRETATION.md for the result-driven next calculation.','']
    (ROOT/'RESULTS.md').write_text('\n'.join(lines),encoding='utf-8')


def seal():
    status = verify()
    assert (ROOT/'RESULTS.md').exists() and (ROOT/'INTERPRETATION.md').exists()
    assert read(ROOT/'progress.json')['state']=='analysis_complete'
    destination = ROOT/'results/stage-integrity.json'
    assert not destination.exists()
    authenticated = authenticate()
    assert authenticated==status['authenticated_parent_inputs']
    import psutil
    for process in psutil.process_iter(['pid','name','cmdline']):
        if process.info['pid']==os.getpid():
            continue
        command = ' '.join(process.info['cmdline'] or [])
        assert not ('split_stage180.py' in command and 'python' in (process.info['name'] or '').lower()),command
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
    packet = dict(state='complete',stage=180,sealed_at_utc=datetime.now(timezone.utc).isoformat(),
        parent_seal_sha256=PARENT_SHA,inherited_sealed_payload_count=inherited,file_hashes=hashes,**carried,
        consumed_and_immediate_rehashed=authenticated,
        previous_primary_source_urls=parent.get('previous_primary_source_urls',[])+parent.get('new_primary_source_urls',[]),
        new_primary_source_urls=[],prior_archive_full_rehash_performed=False,
        prior_archive_verification_seal_sha256=parent['prior_archive_verification_seal_sha256'],
        prior_payload_verification_scope='Immediate Stage179 and consumed inputs rehashed; older archive inherited through seals.',
        accepted_current_scope_verified=True,accepted_scope='Fixed-anchor photon/gas history split and independently tested unit-gas law.',
        latest_anchor_photon_gas_history_split=str(ROOT/'RESULTS.md'),final_validation=str(ROOT/'results/status.json'),
        validation_checks=status['count'],separated_history_actions=360,combined_history_reproductions=180,
        bitwise_combined_reproductions=status['bitwise_combined_reproductions'],unit_gas_actions=36,reused_anchor_loops=36,
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


if __name__=='__main__':
    source.modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('phase',choices=['report','seal'])
    args = parser.parse_args()
    report() if args.phase=='report' else seal()
