from check_stage181 import *


def add_check(checks, name, value, tolerance, category):
    checks.append(dict(name=name, value=float(value), tolerance=float(tolerance),
        passed=bool(abs(value)<=tolerance), category=category))


def curvatures(samples):
    coarse = (samples[1]-2*samples[0]+samples[2])*10000
    fine = (samples[3]-2*samples[0]+samples[4])*40000
    return [coarse,fine,coarse-fine]


def interpolate_correction(state, node_values):
    expansion = state['expansion']
    output = []
    for coordinate in state['coordinates']:
        left = int(np.searchsorted(expansion,coordinate,side='right')-1)
        right = left+1
        weight = (mp.mpf(float(coordinate))-mp.mpf(float(expansion[left])))/(mp.mpf(float(expansion[right]))-mp.mpf(float(expansion[left])))
        output.append((1-weight)*node_values[left]+weight*node_values[right])
    return output


def analyse():
    assert read(ROOT/'progress.json')['state'] in ['precision_complete','analysis_complete']
    paths = authenticate()
    assert paths==read(ROOT/'authenticated-inputs.json')
    for filename,checksum in read(ROOT/'consumed-bank-inputs.json').items():
        assert saved.digest(filename)==checksum,filename
    independent = read(ROOT/'results/independent-equation-checks.json')
    assert independent['all_checks_passed']
    checks, outcomes = list(independent['checks']), []
    with np.load(PARENT/'results/decomposition-vectors.npz') as packet:
        inherited_samples = packet['gas_values'].copy()
        inherited_curves = packet['native_gas_curvature'].copy()
    with np.load(PARENT/'results/precision/decomposition-vectors.npz') as packet:
        unit_predictions = packet['independent_original_unit_predictions'].copy()
        gas_vectors = packet['curves'][:,2].copy()
    carried_controls = read(PARENT/'results/saved-baseline-controls.json')
    write(ROOT/'results/saved-baseline-controls.json', carried_controls)
    law_predictions = np.zeros_like(unit_predictions)
    for model_index,model in enumerate(MODELS):
        folder = ROOT/'results'/model
        native_records = read(folder/'native-diagnostic.json')
        precision80,precision100 = read(folder/'precision-80.json'),read(folder/'precision-100.json')
        with np.load(folder/'state.npz') as packet:
            state = {name:packet[name].copy() for name in packet.files}
        with np.load(folder/'replay.npz') as packet:
            samples, replay_samples = packet['original_samples'].copy(),packet['replay_samples'].copy()
        assert np.array_equal(samples,inherited_samples[:,2*model_index])
        assert np.array_equal(samples,inherited_samples[:,2*model_index+1])
        assert np.array_equal(samples,replay_samples)
        add_check(checks,model+' original five gas samples exactly retained',0,1e-10,'identity')
        add_check(checks,model+' bitwise original double gas replay',max(row['replay_gas_absolute_error'] for row in native_records),1e-10,'identity')
        add_check(checks,model+' bitwise original double profile replay',max(row['replay_profile_relative'] for row in native_records),1e-10,'identity')
        for field in ['balance_residual','work_bdf_residual','gas_energy_bdf_residual','profile_energy_bdf_residual','kinetic_residual_relative']:
            add_check(checks,model+' '+field,max(abs(row[field]) for row in native_records),1e-10,'identity')
        for field in ['energy_bdf_gas_rhs_error','profile_bdf_gas_rhs_error','source_rhs_gas_error']:
            relative = max(abs(row[field])/max(abs(row['gas_bdf_first']),1e-300) for row in native_records)
            add_check(checks,model+' '+field+' at gas-scale identity precision',relative,1e-10,'precision_flag')
            add_check(checks,model+' '+field+' at unchanged derivative tolerance',relative,.01,'source')
        with mp.workdps(110):
            coarse,fine,difference = original = curvatures([mp.mpf(float(value)) for value in samples])
            changes = {}
            precision_difference = mp.mpf('0')
            for lower,higher in zip(precision80,precision100):
                assert lower['index']==higher['index']
                for field in ['gas','gas_rhs','source_energy','denominator']:
                    precision_difference = max(precision_difference,abs(mp.mpf(lower[field])-mp.mpf(higher[field]))/max(abs(mp.mpf(higher[field])),mp.mpf('1e-300')))
            add_check(checks,model+' 80/100 digit agreement',precision_difference,1e-10,'identity')
            add_check(checks,model+' precise Schur energy identity',max(abs(mp.mpf(row['closure'])) for row in precision100),1e-10,'identity')
            add_check(checks,model+' precise versus saved gas pointwise relative',max(abs(mp.mpf(row['replay_error'])/mp.mpf(row['stored_gas'])) for row in precision100),1e-10,'identity')
            rhs_relative = max(abs(mp.mpf(row['gas_rhs_error'])/mp.mpf(row['gas_bdf'])) for row in precision100)
            add_check(checks,model+' precise source RHS gas-scale identity',rhs_relative,1e-10,'precision_flag')
            add_check(checks,model+' precise source RHS derivative check',rhs_relative,.01,'source')
            for digits,rows in [(80,precision80),(100,precision100)]:
                corrections = {row['index']:mp.mpf(row['replay_error']) for row in rows}
                changes[str(digits)] = curvatures(interpolate_correction(state,corrections))
            closure_agreement = max(abs(first-second)/max(abs(second),mp.mpf('1e-300')) for first,second in zip(changes['80'],changes['100']))
            add_check(checks,model+' curvature correction 80/100 agreement',closure_agreement,1e-10,'identity')
            curve_rows = []
            for order,label in enumerate(['coarse','fine','width_difference']):
                correction = changes['100'][order]
                predicted = original[order]+correction
                relative = abs(correction/original[order])
                add_check(checks,model+' '+label+' Schur replay versus saved curvature at identity precision',relative,1e-10,'precision_flag')
                add_check(checks,model+' '+label+' Schur replay versus saved curvature',relative,.01,'source')
                curve_rows.append(dict(width=label,original=float(original[order]),coupled_energy_prediction=float(predicted),
                    correction=float(correction),relative=float(relative),source_tolerance=.01,passed_source=bool(relative<=.01)))
                for column in [2*model_index,2*model_index+1]:
                    law_predictions[order,:,column] = unit_predictions[order,:,column]*float(predicted/original[order])
            direct_curves = {}
            alpha = mp.mpf(float(1.5/float(state['step'])))
            heat = mp.mpf(float(state['heat']))
            for field in ['gas_energy_bdf_residual','profile_energy_bdf_residual']:
                node_errors = {row['index']:-mp.mpf(float(row[field]))/(heat*(alpha+1)) for row in native_records}
                curve_errors = curvatures(interpolate_correction(state,node_errors))
                direct_curves[field] = [dict(width=label,correction=float(error),relative=float(abs(error/expected)))
                    for label,error,expected in zip(['coarse','fine','width_difference'],curve_errors,original)]
                for row in direct_curves[field]:
                    add_check(checks,model+' uncoupled '+field+' '+row['width'],row['relative'],.01,'conditioning_flag')
            for row in precision100:
                assert mp.mpf(row['denominator'])>0
            outcome = dict(model=model,heat=float(state['heat']),native_nodes=len(native_records),precision_nodes=len(precision100),
                original_width_relative=float(abs(difference/fine)),
                replay_width_relative=float(abs((difference+changes['100'][2])/(fine+changes['100'][1]))),
                curvature=curve_rows,uncoupled_energy_readback=direct_curves,
                maximum_raw_balance_residual=max(abs(row['balance_residual']) for row in native_records),
                maximum_precise_replay_gas_error=float(max(abs(mp.mpf(row['replay_error'])) for row in precision100)),
                maximum_precise_source_gas_relative=float(rhs_relative),
                minimum_schur_denominator=min(float(row['denominator']) for row in precision100),
                maximum_schur_denominator=max(float(row['denominator']) for row in precision100),
                schur_to_bare_heat_denominator_min=min(row['denominator_over_bare_heat'] for row in native_records))
            outcomes.append(outcome)
    with np.load(source.ROOT/'results/preparation/basis.npz') as packet:
        mass = packet['mass'].copy()
    factor = linear.cholesky(mass,lower=True)
    def norm(vector):
        return np.linalg.norm(linear.solve_triangular(factor,vector[1:97],lower=True),axis=0)
    gas_law_errors = np.stack([norm(law_predictions[order]-gas_vectors[order])/norm(gas_vectors[order]) for order in range(3)])
    for order,column in np.ndindex(3,4):
        add_check(checks,f'Fixed K_g source prediction order{order} history{column}',gas_law_errors[order,column],.01,'source')
    bank_path = native.BACKGROUND/'banks/infrared96-q700/status.json'
    bank = read(bank_path)
    theta = read(ROOT/'results/heavy/native-diagnostic.json')
    theta = next(row['theta'] for row in theta if row['index']==5600)
    temperatures = np.array(bank['temperatures'])
    closest = int(np.argmin(abs(temperatures-theta)))
    left_distance = abs((theta-temperatures[closest])/theta)
    assert 0<closest<len(temperatures)-1
    blocks = []
    for index in range(closest-1,closest+2):
        with np.load(bank_path.parent/f'planck-{index}.npz') as packet:
            blocks.append(packet['stiffness'].copy())
    derivative_low = (blocks[1]-blocks[0])/(temperatures[closest]-temperatures[closest-1])
    derivative_high = (blocks[2]-blocks[1])/(temperatures[closest+1]-temperatures[closest])
    bank_knot = dict(anchor_theta=theta,nearest_index=closest,nearest_theta=float(temperatures[closest]),
        relative_distance=float(left_distance),interpolation='piecewise linear in theta, per original InfraredLadder.at',
        relative_matrix_slope_jump=float(np.linalg.norm(derivative_high-derivative_low)/max(np.linalg.norm(derivative_low),np.linalg.norm(derivative_high))),
        diagnostic_only=True,knot_causality_proved=False,bank_source=str(bank_path))
    write(ROOT/'results/bank-knot.json',bank_knot)
    write(ROOT/'results/gas-curvature.json',outcomes)
    np.savez_compressed(ROOT/'results/gas-law-predictions.npz',coupled_energy_gas_predictions=law_predictions,
        saved_gas_vectors=gas_vectors,relative_errors=gas_law_errors)
    protected = BRANCH.parent.parent/'formalization-workbench'
    start = datetime.fromisoformat(STARTED).timestamp()
    recent = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=start]
    add_check(checks,'Protected workbench recent-mtime count',len(recent),0,'integrity')
    assert carried_controls==read(PARENT/'results/saved-baseline-controls.json')
    assert authenticate()==paths
    for filename,checksum in read(ROOT/'consumed-bank-inputs.json').items():
        assert saved.digest(filename)==checksum,filename
    assert not read(ROOT/'additional-inputs.json')
    failed = [row for row in checks if not row['passed']]
    status = dict(stage=181,state='diagnostic_complete',checks=checks,count=len(checks),
        all_checks_passed=not failed,passed_checks=len(checks)-len(failed),failed_checks=failed,
        key_coupled_replay_source_checks_pass=all(row['passed'] for row in checks if row['category']=='source'),
        retained_parent_precision_flags=read(PARENT/'results/precision/status.json')['retained_failed_checks'],
        baseline_source_controls_unchanged=True,original_matched_moving_curvature_gate_passed=False,
        original_source_packets_replaced=False,current_history_replaced=False,temperature_curve_changed=False,
        tolerances_changed=False,native_history_reintegrated=False,physical_accuracy_independently_proved=False,
        new_loop_integrations=0,real_emission_integrations=0,
        native_replayed_nodes=122,high_precision_prior_state_replays=40,
        protected_modified_file_count=len(recent),protected_recent_files=recent,
        protected_check_scope='Recent mtime since turn start, not a full before/after directory hash audit',
        authenticated_parent_inputs=paths,
        input_hashes={str(path):saved.digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file()
            and path.name not in ['progress.json','status.json'] and path.parent!=ROOT})
    write(ROOT/'results/status.json',status)
    write(ROOT/'progress.json',dict(state='analysis_complete'))
    print(json.dumps(dict(passed=status['passed_checks'],total=status['count'],failed=failed,
        outcomes=outcomes,bank_knot=bank_knot)),flush=True)


def independent_checks():
    checks = []
    step = .125
    coordinate = np.arange(8)*step
    for label,values,expected in [
        ('constant',np.ones(8),np.zeros(6)),
        ('linear',coordinate,np.ones(6)),
        ('quadratic',coordinate**2,2*coordinate[2:]),
        ('cubic truncation',coordinate**3,3*coordinate[2:]**2-2*step**2)]:
        add_check(checks,'BDF2 first derivative '+label,np.max(abs(bdf2_first_derivative(values,step)-expected)),1e-10,'identity')
    samples = [mp.mpf('0'),mp.mpf('0.0001'),mp.mpf('0.0001'),mp.mpf('0.000025'),mp.mpf('0.000025')]
    with mp.workdps(80):
        curves = curvatures(samples)
        add_check(checks,'Centered finite-width quadratic curvature',max(abs(curves[0]-2),abs(curves[1]-2),abs(curves[2])),1e-10,'identity')
    for model in MODELS:
        folder = ROOT/'results'/model
        with np.load(folder/'state.npz') as packet:
            state = {name:packet[name].copy() for name in packet.files}
        with np.load(folder/'operator-5600.npz') as packet:
            operator = {name:packet[name].copy() for name in packet.files}
        reference = next(row for row in read(folder/'precision-100.json') if row['index']==5600)
        with mp.workdps(80):
            count = 96
            system = mp.matrix(count+1)
            right = mp.matrix(count+1,1)
            upper = np.triu(operator['left'])+np.triu(operator['left'],1).T
            alpha,heat = mp.mpf(float(operator['alpha'])),mp.mpf(float(state['heat']))
            energy,vector = mp_vector(state['energy']),mp_vector(operator['vector'])
            for row in range(count):
                for column in range(count):
                    system[row,column] = mp.mpf(float(upper[row,column]))
                system[row,count] = -mp.mpf(float(operator['thermal_source'][row]))
                system[count,row] = alpha*energy[row]
                right[row] = mp.mpf(float(operator['right'][row]))
            system[count,count] = heat*(alpha+1)
            right[count] = heat*mp.mpf(float(operator['scalar']))-1+(energy.T*vector)[0]
            solution = mp.lu_solve(system,right)
            add_check(checks,model+' independent 97-variable block gas matches Schur',abs(solution[count]-mp.mpf(reference['gas']))/abs(mp.mpf(reference['gas'])),1e-10,'identity')
            add_check(checks,model+' independent full block residual',mp.norm(system*solution-right)/mp.norm(right),1e-10,'identity')
    write(ROOT/'results/independent-equation-checks.json',dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks)))
    print(json.dumps(dict(independent_checks=len(checks),all_checks_passed=all(row['passed'] for row in checks))),flush=True)


def report():
    status = read(ROOT/'results/status.json')
    outcomes = read(ROOT/'results/gas-curvature.json')
    knot = read(ROOT/'results/bank-knot.json')
    controls = read(ROOT/'results/saved-baseline-controls.json')
    lines = ['# Stage181: test the gas curvature against its energy equation','',
        'The saved gas curvature is reproduced by the coupled energy-balance update.',
        'Its width discrepancy survives this local arithmetic check. A direct scalar',
        'energy subtraction is poorly conditioned, and the anchor lies on a kernel-bank',
        'interpolation knot. Keep the temperature curve unchanged while testing the',
        'local time resolution and kernel interpolation separately.','',
        '## What was evaluated','',
        '- Replayed all 61 local native updates in each of the heavy/cold histories.',
        '  All gas and photon-profile outputs reproduce the original double solver bitwise.',
        '- At ten native nodes per history bracketing the existing five probes, solved',
        '  the prior-state coupled equation at 80 and 100 digits using unchanged saved',
        '  binary64 operator operands and the original upper-triangle solve convention.',
        '- Independently solved the full 97-variable photon/gas block at both anchors;',
        '  it agrees with the eliminated gas equation. Polynomial BDF2/curvature controls pass.',
        '- Reused all original source/baseline decisions, the fixed-anchor unit-gas',
        '  coefficient and saved incident histories. No new virtual or real-emission',
        '  integrals, no new history evolution, and no changed coefficients.','',
        '## Gas-curvature result','',
        '|History|Original coarse/fine change %|Coupled-energy replay change %|Relative change of the width discrepancy %|',
        '|---|---:|---:|---:|']
    for row in outcomes:
        lines.append(f"|{row['model']}|{100*row['original_width_relative']:.12g}|{100*row['replay_width_relative']:.12g}|{100*row['curvature'][2]['relative']:.8g}|")
    lines += ['','The replay predicts the gas-source contribution through the already tested',
        'law Delta U_gas=K_g Delta C[g], for all four history columns at the unchanged',
        '1% criterion. The six older representation flags and the original 1.0366%',
        'matched moving-history derivative discrepancy remain recorded.','',
        '## Why a tiny energy residual can mislead','',
        '|History|chi|Maximum integrated energy balance residual|Maximum pointwise precise replay change in g|Minimum coupled/bare-heat denominator ratio|',
        '|---|---:|---:|---:|---:|']
    for row in outcomes:
        lines.append(f"|{row['model']}|{row['heat']:.12g}|{row['maximum_raw_balance_residual']:.8g}|{row['maximum_precise_replay_gas_error']:.8g}|{row['schur_to_bare_heat_denominator_min']:.8g}|")
    lines += ['','The uncoupled readback divides radiation-scale residuals by chi. It loses',
        'the feedback term a e r in the coupled denominator. The mathematically',
        'equivalent expressions therefore have very different numerical conditioning.',
        'High precision on already rounded stored energies cannot restore digits',
        'that were not saved. See DERIVATION.md and results/gas-curvature.json.',
        'Passing total energy balance alone is not a gas-derivative accuracy claim.','',
        '## Precision and failed comparisons','',
        f"{status['passed_checks']}/{status['count']} current checks pass; {len(status['failed_checks'])} fail and are retained below.",
        'The source/derivative threshold stays1%; identity precision stays1e-10.',
        'No failure is erased by marking the diagnostic complete.','',
        '|Check|Value|Unchanged tolerance|','|---|---:|---:|']
    for row in status['failed_checks']:
        lines.append(f"|{row['name']}|{row['value']:.10g}|{row['tolerance']:.5g}|")
    lines += ['','80/100-digit agreement validates evaluation of these saved operands, not',
        'the physical accuracy of the underlying binary64 matrices or the original',
        'history integration. One-step replay keeps previous history values fixed;',
        'it does not test accumulated error.','',
        '## Bank-knot observation','',
        f"Anchor theta={knot['anchor_theta']:.17g}; nearest bank theta={knot['nearest_theta']:.17g}.",
        f"Their relative distance is {knot['relative_distance']:.10g}.",
        f"The adjacent matrix slopes differ by {100*knot['relative_matrix_slope_jump']:.10g}% in Frobenius norm.",
        'This is the existing piecewise-linear scattering-bank interpolator, not a',
        'new physical transition. A smooth Taylor-error argument across that knot',
        'cannot be assumed without testing. This observation alone does not prove',
        'that the knot causes the measured curvature discrepancy.','',
        '## Baseline and MTS comparison preserved','',
        '|Component|Moving curvature change %|Fixed curvature change %|Moving passes /4|Fixed passes /4|',
        '|---|---:|---:|---:|---:|']
    for component in ['control','remainder','total']:
        moving = [row for row in controls if row['branch']=='moving_history' and row['component']==component]
        fixed = [row for row in controls if row['branch']=='fixed_incident' and row['component']==component]
        lines.append(f"|{component}|{100*max(row['relative'] for row in moving):.10g}|{100*max(row['relative'] for row in fixed):.10g}|{sum(row['passed'] for row in moving)}|{sum(row['passed'] for row in fixed)}|")
    lines += ['','Heavy/cold are the two retained incident backgrounds, each shared by the',
        'baseline and matched MTS response with two photon-join controls. This is not',
        'a new MTS-only gas evolution or a relabelling of heavy/cold as competing theories.','',
        '## Next discriminating calculation','',
        'Use a short local restart across the same anchor window at the native step',
        'and half step, with identical starting history, source banks and coupling.',
        'Compare gas curvature and the common baseline/MTS source consequences at',
        'the unchanged probes and tolerances. Verify native-step replay first.',
        'Use a second-order variable-step startup for the half-step branch, not an',
        'uncontrolled first-order restart that could inject a new transient.',
        'Keep the bank fixed in that test, so time discretization is isolated. If',
        'the discrepancy survives, test the bank knot separately; do not fit it away',
        'by changing the temperature curve.','',
        '## Integrity','',
        f"{len(status['authenticated_parent_inputs'])} parent/consumed input paths rehashed before/after.",
        'Older archive inherited through seals, not claimed newly rehashed in full.',
        f"Protected workbench recent-mtime count: {status['protected_modified_file_count']}.",
        'One below-normal worker, single-thread libraries; no subagents/GitHub actions.',
        'Previous stages immutable; only the new child and additive bookmark heads change.','']
    (ROOT/'RESULTS.md').write_text('\n'.join(lines),encoding='utf-8')


def seal():
    status = read(ROOT/'results/status.json')
    assert status['key_coupled_replay_source_checks_pass']
    assert status['protected_modified_file_count']==0
    assert read(ROOT/'progress.json')['state']=='analysis_complete'
    assert authenticate()==status['authenticated_parent_inputs']
    for filename,checksum in status['input_hashes'].items():
        assert saved.digest(filename)==checksum,filename
    for filename,checksum in read(ROOT/'consumed-bank-inputs.json').items():
        assert saved.digest(filename)==checksum,filename
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    assert not list(ROOT.rglob('__pycache__'))
    import psutil
    for process in psutil.process_iter(['pid','name','cmdline']):
        if process.info['pid']==os.getpid():
            continue
        assert not ('python' in (process.info['name'] or '').lower() and
            'check_stage181.py' in ' '.join(process.info['cmdline'] or []))
    parent = read(PARENT/'results/stage-integrity.json')
    inherited = parent['inherited_sealed_payload_count']+len(parent['file_hashes'])
    assert inherited==336107
    destination = ROOT/'results/stage-integrity.json'
    assert not destination.exists()
    carry_names = ['checkpoint_manifest_sha256','local_source_documents','primary_pdfs','source_urls',
        'observational_source_urls','original_library_sha256','native_library_sha256','physical_source_scope',
        'retained_local_approximation_histories','raw_subtraction_response_retained','raw_failed_history_response_retained']
    carried = {key:value for key,value in parent.items() if key in carry_names or key.startswith('latest_')}
    hashes = {path.relative_to(ROOT).as_posix():saved.digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path!=destination}
    largest = max(sum(path.is_file() for path in folder.iterdir()) for folder in [ROOT,*[path for path in ROOT.rglob('*') if path.is_dir()]])
    assert largest<=500
    write(destination,dict(state='complete',completion_qualification='diagnostic_complete_with_retained_flags',stage=181,sealed_at_utc=datetime.now(timezone.utc).isoformat(),
        parent_seal_sha256=PARENT_SHA,inherited_sealed_payload_count=inherited,file_hashes=hashes,**carried,
        consumed_and_immediate_rehashed=status['authenticated_parent_inputs'],
        previous_primary_source_urls=parent.get('previous_primary_source_urls',[])+parent.get('new_primary_source_urls',[]),
        new_primary_source_urls=[],prior_archive_full_rehash_performed=False,
        prior_archive_verification_seal_sha256=parent['prior_archive_verification_seal_sha256'],
        prior_payload_verification_scope='Immediate Stage180, consumed inputs and native equation/bank owners rehashed; older archive inherited through seals.',
        accepted_current_scope_verified=True,accepted_scope='Prior-state coupled energy replay reproduces finite-width gas curvature at unchanged1%; conditioning and legacy failures retained.',
        latest_gas_energy_curvature_diagnostic=str(ROOT/'RESULTS.md'),final_validation=str(ROOT/'results/status.json'),
        validation_checks=status['count'],passed_validation_checks=status['passed_checks'],
        current_stage_retained_failures=len(status['failed_checks']),all_raw_and_legacy_checks_passed=False,
        retained_failed_checks=parent.get('retained_failed_checks',[])+status['failed_checks'],
        native_replayed_nodes=122,high_precision_prior_state_replays=40,new_loop_integrations=0,real_emission_integrations=0,
        operator_frozen_at_anchor=True,native_gas_operator_varies_along_saved_background=True,
        original_matched_moving_curvature_gate_passed=False,source_curve_changed=False,temperature_curve_changed=False,
        baseline_preserved=True,original_source_packets_replaced=False,current_history_replaced=False,tolerances_changed=False,
        native_history_reintegrated=False,post_test_diagnostic=True,bank_knot_causality_proved=False,
        independent_raw_physical_source_qualified=False,full_population_source_temperature_law_certified=False,
        scientific_failure_inherited=True,global_numerical_error_bound=None,
        protected_workbench_recent_modified_file_count=0,protected_check_scope=status['protected_check_scope'],
        maximum_active_workers=1,active_workers_at_seal=0,library_threads_per_worker=1,largest_direct_file_count=largest,
        github_action=False,subagents=0,global_installation_changed=False,galaxy_work_modified=False,
        next_target='Native versus half-step short local coupled-history restart across the anchor, banks/probes/tolerances fixed.'))
    assert all(saved.digest(ROOT/name)==checksum for name,checksum in hashes.items())
    print(json.dumps(dict(sealed_files=len(hashes),cumulative_payloads=inherited+len(hashes),seal_sha256=saved.digest(destination))),flush=True)


def bookmarks():
    seal_path = ROOT/'results/stage-integrity.json'
    seal_packet = read(seal_path)
    assert all(saved.digest(ROOT/name)==checksum for name,checksum in seal_packet['file_hashes'].items())
    config = read(ROOT/'configuration.json')
    prefix = '\n'.join(['# Stage181 COMPLETE — gas-energy replay; conditioning flags retained','',
        f'Latest child: {ROOT}',f'Results: {ROOT / "RESULTS.md"}',
        f'Status: {ROOT / "results/status.json"}',f'Seal SHA256: {saved.digest(seal_path)}',
        f'Sealed payloads: {seal_packet["inherited_sealed_payload_count"]+len(seal_packet["file_hashes"])} (older archive inherited through seals).','',
        'Gas curvature reproduced by the prior-state coupled energy equation, with unchanged1% checks.',
        'Native double replay bitwise at122 nodes;80/100-digit arithmetic at20 nodes.',
        'Gas-scale precision/readback failures retained; current status is not all-checks-pass.',
        'Anchor coincides with a piecewise-linear scattering-bank knot; causal attribution not made.',
        'Original source/curve and baseline decisions unchanged; no GitHub action or running worker.',
        'NEXT: short native/half-step local restart, banks/probes/tolerances fixed; test bank knot separately if needed.','',
        '--- Previous bookmark body preserved verbatim after normalized newline handling ---',''])+'\n'
    for filename,checksum in config['prior_bookmark_normalized_sha256'].items():
        path = Path(filename)
        body = path.read_text(encoding='utf-8')
        assert hashlib.sha256(body.encode()).hexdigest()==checksum
        path.write_text(prefix+body,encoding='utf-8')
        updated = path.read_text(encoding='utf-8')
        assert updated.startswith(prefix)
        assert hashlib.sha256(updated[len(prefix):].encode()).hexdigest()==checksum
    print('Both additive bookmark heads verified; previous bodies preserved.',flush=True)


if __name__=='__main__':
    source.modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('phase',choices=['independent','analyse','report','seal','bookmarks'])
    arguments = parser.parse_args()
    {'independent':independent_checks,'analyse':analyse,'report':report,'seal':seal,'bookmarks':bookmarks}[arguments.phase]()
