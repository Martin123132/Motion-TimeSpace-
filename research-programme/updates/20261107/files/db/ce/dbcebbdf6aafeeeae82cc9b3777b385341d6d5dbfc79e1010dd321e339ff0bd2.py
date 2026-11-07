from projection_common import *


def main():
    modest()
    folder=ROOT/'results/projection'
    folder.mkdir(parents=True,exist_ok=False)
    chain=ancestors()
    parent=chain[PARENT/'results/stage-integrity.json']
    for name,expected in parent['file_hashes'].items():
        assert digest(PARENT/name)==expected,name
    checks=[]
    def test(name,value,limit):
        checks.append(dict(name=name,value=float(value),limit=float(limit),passed=bool(np.isfinite(value) and value<limit)))
    checks.append(dict(name='All48 Stage107 payloads match sealed hashes',passed=len(parent['file_hashes'])==48))
    authority_path=PARENT/'results/window-transfer/status.json'
    authority=json.loads(authority_path.read_text())
    assert authority['all_checks_passed'] and authority['window_contribution_only']
    spec_path=BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700/status.json'
    spec=json.loads(spec_path.read_text())['basis_spec']
    basis=infrared_ladder.ConsistentBasis(**spec)
    mass,temperature,energy_row,number_row=basis.mass,basis.temperature,basis.energy,basis.number
    capacity=float(energy_row@temperature)
    number_capacity=float(number_row@temperature)
    projector=np.outer(temperature,energy_row)/capacity
    complement=np.eye(96)-projector
    identity=np.eye(96)
    test('Projector complementarity',np.max(abs(projector+complement-identity)),1e-11)
    test('Temperature projector idempotence',np.max(abs(projector@projector-projector)),1e-11)
    test('Distortion projector idempotence',np.max(abs(complement@complement-complement)),1e-11)
    test('Complementary projectors annihilate one another',np.max(abs(projector@complement)),1e-11)
    test('Temperature projector M self adjoint',np.max(abs(projector.T@mass-mass@projector)),1e-11)
    checks.append(dict(name='One temperature plus95 independent distortion degrees of freedom',
        passed=np.linalg.matrix_rank(projector)==1 and np.linalg.matrix_rank(complement)==95))
    test('Temperature basis is x at independent sample frequencies',
        np.max(abs(basis.evaluate(np.geomspace(basis.minimum,basis.maximum,241))@temperature/np.geomspace(basis.minimum,basis.maximum,241)-1)),1e-11)
    test('Finite band temperature energy capacity agrees with Planck4',abs(capacity/4-1),1e-9)
    number_conversion=math.pi**4/(30*special.zeta(3))
    test('Finite band temperature number capacity agrees with Planck3',
        abs(number_capacity*number_conversion/3-1),1e-9)
    pure=temperature[:,None]*np.array([.1,-.27,0.])
    pure_result=decompose(pure,energy_row@pure,basis)
    test('Synthetic pure-temperature perturbation leaves no distortion',np.max(abs(pure_result['distortion'])),1e-11)
    probe=identity[:,3:6]
    mixed=probe+temperature[:,None]*np.array([.31,-.2,.41])
    mixed_result=decompose(mixed,energy_row@mixed,basis)
    test('Synthetic mixed signal recovers nonthermal probe',
        np.max(abs(mixed_result['distortion']-complement@probe)),1e-11)
    wrong_temperature=temperature[:,None]*((number_row@probe)/number_capacity)
    checks.append(dict(name='Nonthermal negative control is not accepted as pure-temperature',
        passed=bool(np.all(norm(probe-wrong_temperature,mass)>.99))))
    frequency=np.geomspace(basis.minimum,basis.maximum,241)
    values=basis.evaluate(frequency)
    occupation=1/np.expm1(frequency)
    weight=occupation*(1+occupation)
    template=frequency*weight
    derivative_errors=[]
    for step in [1e-4,5e-5]:
        derivative=(1/np.expm1(frequency/(1+step))-1/np.expm1(frequency/(1-step)))/(2*step)
        derivative_errors.append(float(np.max(abs(derivative/template-1))))
    test('Planck tangent finite difference fine error',derivative_errors[1],1e-4)
    test('Planck tangent finite difference contracts',derivative_errors[1]/derivative_errors[0],1.)
    inputs=[authority_path,spec_path,ROOT/'DERIVATION.md',*SOURCE_DOCS]
    cases=['main-256','main-512','main-1024','from-parent128-1024','from-parent256-1024','split-second-512']
    summary={}
    metadata={}
    eps=np.finfo(float).eps
    for model in ['heavy','cold']:
        background=thermal_wave.thermal.ThermalBackground(model)
        heat=background.chi
        reference_temperature=background.temperature0/background.end_scale
        constants=background.constants
        native_text=background.native_constants.read_text()
        planck_constant=float(re.search(r'\bh_P\s*=\s*([0-9.eE+-]+)_dl',native_text,re.I).group(1))
        density0=8*np.pi**5*constants['k_B']**4/(15*constants['c']**3*planck_constant**3)*background.temperature0**4
        test('Native Planck energy-density normalization:'+model,abs(density0/background.photon_energy0-1),1e-9)
        inputs.extend([background.parent.source,background.native_constants])
        original_path=BRANCH/'infrared-source-domain-20261008/backgrounds'/f'{model}-nonlocal-refined-6400/history.npz'
        inputs.append(original_path)
        with np.load(original_path) as source:
            test('Physical chi matches original saved profile heat:'+model,abs(float(source['heat'])/heat-1),1e-12)
        metadata[model]=dict(heat=heat,reference_temperature_K=reference_temperature,
            scale=background.end_scale,thermal_parameter=background.theta0/background.end_scale,
            h_P=planck_constant,k_B=constants['k_B'],c=constants['c'])
        states={}
        projected={}
        case_metrics={}
        for case in cases:
            state,path=read_final(model,case)
            inputs.append(path)
            assert state['photon'].shape==(96,16) and state['energy'].shape==(16,)
            assert abs(state['coordinate']-background.end)<1e-14
            assert all(np.isfinite(value).all() for value in state.values())
            result=decompose(state['photon'],state['energy'],basis)
            states[case]=state
            projected[case]=result
            photon=result['photon']
            distortion=result['distortion']
            temp=result['temperature']
            eta=result['eta']
            scale=norm(photon,mass)
            assert np.all(scale>0)
            allowance=256*eps*np.maximum(abs(energy_row)@(abs(photon)+abs(temp)+abs(distortion)),1e-300)
            spectral_mismatch=energy_row@photon-state['energy']
            residual_energy=energy_row@distortion
            test('Independent saved energy matches spectrum within cancellation allowance:'+model+':'+case,
                np.max(abs(spectral_mismatch)/allowance),1.)
            test('Residual distortion energy within cancellation allowance:'+model+':'+case,
                np.max(abs(residual_energy)/allowance),1.)
            test('Temperature plus distortion reconstructs original:'+model+':'+case,
                np.max(norm(temp+distortion-photon,mass)/scale),1e-11)
            test('Orthogonal spectral-norm splitting:'+model+':'+case,
                np.max(abs(scale**2-capacity*eta**2-norm(distortion,mass)**2)/scale**2),1e-11)
            test('Temperature piece carries independent energy:'+model+':'+case,
                np.max(abs(energy_row@temp-state['energy'])/np.maximum(abs(state['energy']),1e-300)),1e-11)
            beta=scale/math.sqrt(capacity)*np.where(np.arange(16)%2,1.,-1.)
            shifted=decompose(photon+temperature[:,None]*beta,state['energy']+capacity*beta,basis)
            test('Reference-temperature shift leaves distortion invariant:'+model+':'+case,
                np.max(norm(shifted['distortion']-distortion,mass)/scale),1e-11)
            eta_number=(number_row@photon)/number_capacity
            distortion_number=photon-temperature[:,None]*eta_number
            remapped=complement@distortion_number
            test('Number-matched convention represents same nonthermal quotient:'+model+':'+case,
                np.max(norm(remapped-distortion,mass)/scale),1e-11)
            number_scale=np.maximum(abs(number_row)@abs(photon),1e-300)
            test('Photon number partitions without imposing conservation:'+model+':'+case,
                np.max(abs(number_row@distortion+number_capacity*eta-state['number'])/number_scale),1e-11)
            balance=state['energy']+heat*state['gas']+state['work']
            balance_scale=abs(state['energy'])+abs(heat*state['gas'])+abs(state['work'])
            test('Inherited energy gas and work budget retained:'+model+':'+case,
                np.max(abs(balance)/np.maximum(balance_scale,1e-300)),1e-7)
            test('Discarding distortion negative control is detected:'+model+':'+case,
                1-float(np.min(norm(photon-temp,mass)/scale)),.999999)
            np.savez(folder/f'{model}-{case}-projected.npz',**result,
                gas=state['gas'],work=state['work'],number=state['number'],
                residual_number=number_row@distortion,eta_number_matched=eta_number,
                spectral_energy_mismatch=spectral_mismatch,residual_energy_from_spectrum=residual_energy,
                cancellation_allowance=allowance)
            case_metrics[case]=dict(maximum_energy_allowance_ratio=float(np.max(abs(residual_energy)/allowance)),
                original_energy_mismatch=spectral_mismatch.tolist(),
                scaled_temperature_eta=eta.tolist(),fractional_temperature=(heat*eta).tolist(),
                temperature_K=(reference_temperature*heat*eta).tolist(),distortion_norm=norm(distortion,mass).tolist(),
                temperature_norm_to_original=(norm(temp,mass)/scale).tolist(),
                distortion_norm_to_original=(norm(distortion,mass)/scale).tolist(),
                residual_fractional_photon_number=(heat*number_conversion*(number_row@distortion)).tolist())
        final=projected['main-1024']
        central_distortion=norm(final['distortion'][:,:2],mass)
        central_eta=abs(final['eta'][:2])
        assert np.all(central_eta>0)
        budgets={}
        for level,offsets in [('43',[4,6,8]),('54',[10,12,14])]:
            pieces=[final['distortion'][:,offset:offset+2] for offset in offsets]
            eta_pieces=[final['eta'][offset:offset+2] for offset in offsets]
            dist_sum=sum(norm(piece,mass) for piece in pieces)
            eta_sum=sum(abs(piece) for piece in eta_pieces)
            coherent=norm(sum(pieces),mass)
            test('Projected component triangle inequality:'+model+':'+level,
                np.max((coherent-dist_sum)/central_distortion),1e-11)
            budgets[level]=dict(distortion_component_sum_relative=(dist_sum/central_distortion).tolist(),
                temperature_component_sum_relative=(eta_sum/central_eta).tolist(),
                distortion_component_absolute=[norm(piece,mass).tolist() for piece in pieces],
                temperature_component_absolute=[abs(piece).tolist() for piece in eta_pieces],
                distortion_coherent_relative=(coherent/central_distortion).tolist(),
                physical_fractional_temperature_sum=(heat*eta_sum).tolist())
        total_dist=sum(final['distortion'][:,offset:offset+2] for offset in [10,12,14])
        total_eta=sum(final['eta'][offset:offset+2] for offset in [10,12,14])
        dist_denominator=sum(norm(final['distortion'][:,offset:offset+2],mass) for offset in [10,12,14])
        eta_denominator=sum(abs(final['eta'][offset:offset+2]) for offset in [10,12,14])
        test('Saved independent54 total versus projected component sum:'+model,
            np.max(norm(final['distortion'][:,2:4]-total_dist,mass)/dist_denominator),1e-8)
        test('Saved independent54 temperature versus component sum:'+model,
            np.max(abs(final['eta'][2:4]-total_eta)/eta_denominator),1e-8)
        comparisons={}
        for label,other_case in [('downstream512','main-512'),('downstream256','main-256'),
                                 ('terminal256','from-parent256-1024'),('terminal128','from-parent128-1024'),
                                 ('split_restart','split-second-512')]:
            other=projected[other_case]
            comparisons[label]=dict(
                central_distortion_relative=(norm((final['distortion']-other['distortion'])[:,:2],mass)/central_distortion).tolist(),
                central_temperature_relative=(abs((final['eta']-other['eta'])[:2])/central_eta).tolist(),
                all_column_distortion_absolute=norm(final['distortion']-other['distortion'],mass).tolist(),
                all_column_temperature_absolute=abs(final['eta']-other['eta']).tolist())
        potential=values@final['photon']
        distortion_potential=values@final['distortion']
        temp_potential=frequency[:,None]*final['eta']
        occupation_full=heat*weight[:,None]*potential
        occupation_dist=heat*weight[:,None]*distortion_potential
        occupation_temp=heat*weight[:,None]*temp_potential
        relative_scale=np.maximum(np.max(abs(occupation_full),axis=0),1e-300)
        test('Pointwise occupation reconstructs on represented band:'+model,
            np.max(abs(occupation_full-occupation_dist-occupation_temp)/relative_scale),1e-11)
        frequency_hz=frequency*constants['k_B']*reference_temperature/planck_constant
        radiance_factor=2*planck_constant*frequency_hz**3/constants['c']**2
        intensity_full=radiance_factor[:,None]*occupation_full
        intensity_dist=radiance_factor[:,None]*occupation_dist
        intensity_temp=radiance_factor[:,None]*occupation_temp
        intensity_scale=np.maximum(np.max(abs(intensity_full),axis=0),1e-300)
        test('Specific intensity reconstructs on represented band:'+model,
            np.max(abs(intensity_full-intensity_dist-intensity_temp)/intensity_scale),1e-11)
        test('Fractional intensity equals fractional occupation at fixed frequency:'+model,
            np.max(abs(intensity_dist/(radiance_factor*occupation)[:,None]-occupation_dist/occupation[:,None]))/
            max(float(np.max(abs(occupation_dist/occupation[:,None]))),1e-300),1e-11)
        np.savez(folder/f'{model}-band-spectrum.npz',x=frequency,frequency_Hz=frequency_hz,
            reference_temperature_K=reference_temperature,delta_occupation=occupation_full,
            delta_occupation_temperature=occupation_temp,delta_occupation_distortion=occupation_dist,
            delta_intensity_SI=intensity_full,delta_intensity_temperature_SI=intensity_temp,
            delta_intensity_distortion_SI=intensity_dist,
            distortion_fractional_intensity=occupation_dist/occupation[:,None])
        packet_path=PARENT/'results/window-transfer'/f'{model}-final-window-contribution.npz'
        inputs.append(packet_path)
        with np.load(packet_path) as saved:
            assert np.array_equal(saved['mass'],mass) and np.array_equal(saved['temperature'],temperature)
            assert np.array_equal(saved['photon_central'],final['photon'][:,:2])
            parent_photon=saved['parent_photon']
        parent_distortion=complement@parent_photon
        parent_distortion_norm=float(norm(parent_distortion[:,None],mass)[0])
        summary[model]=dict(metadata=metadata[model],cases=case_metrics,budgets=budgets,comparisons=comparisons,
            distortion54_over43=(np.asarray(budgets['54']['distortion_component_sum_relative'])/
                np.asarray(budgets['43']['distortion_component_sum_relative'])).tolist(),
            temperature54_over43=(np.asarray(budgets['54']['temperature_component_sum_relative'])/
                np.asarray(budgets['43']['temperature_component_sum_relative'])).tolist(),
            central_distortion_to_parent_distortion=(central_distortion/parent_distortion_norm).tolist(),
            central_band_relative_intensity_max=np.max(abs(occupation_dist[:,:2]/occupation[:,None]),axis=0).tolist(),
            central_band_relative_intensity_min=np.min(occupation_dist[:,:2]/occupation[:,None],axis=0).tolist(),
            central_band_relative_intensity_max_signed=np.max(occupation_dist[:,:2]/occupation[:,None],axis=0).tolist(),
            energy_physical_fraction=(heat*final['energy'][:2]).tolist(),
            gas_fraction=(heat*states['main-1024']['gas'][:2]).tolist(),
            number_convention_eta=((number_row@final['photon'][:,:2])/number_capacity).tolist())
        print(json.dumps(dict(model=model,central=case_metrics['main-1024'],budgets=budgets,comparisons=comparisons)),flush=True)
    for path in inputs:
        if path.is_relative_to(ROOT):
            continue
        inherited.verify_reference(path,chain)
    checks.append(dict(name='Every consumed scientific input has an unchanged sealed owner',passed=True,value=len(inputs)))
    np.savez(folder/'projection-definition.npz',mass=mass,temperature=temperature,energy_row=energy_row,
        number_row=number_row,temperature_projector=projector,distortion_projector=complement,
        energy_capacity=capacity,number_capacity=number_capacity,number_conversion=number_conversion)
    report=dict(checks=checks,models=summary,column_order=authority['column_order'],basis_specification=spec,
        energy_capacity=capacity,number_capacity=number_capacity,number_conversion=number_conversion,
        derivative_errors=derivative_errors,projection_convention='energy matched Planck tangent, inherited M metric',
        independent_energy_used=True,roundoff_allowance_factor=256,window_contribution_only=True,
        final_saved_scale=1e-5,current_epoch_today=False,temperature_shift_fraction_is_chi_times_eta=True,
        physical_source_recomputed=False,source_evaluations=0,new_empirical_fit=False,new_evolution=False,
        source_continuum_error_bounded=False,infrared_increment_continuation_computed=False,
        outside_window_source_assumed_zero=False,kinetic_modes_discarded=0,
        instrument_temperature_fit=False,github_action=False)
    finish(folder,report,__file__,inputs)
    print(json.dumps(dict(count=len(checks),failed=[row for row in checks if not row['passed']])),flush=True)
    if not report['all_checks_passed']:
        raise SystemExit(1)


if __name__=='__main__':
    main()

