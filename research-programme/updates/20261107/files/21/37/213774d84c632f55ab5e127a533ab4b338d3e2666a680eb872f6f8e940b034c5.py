from shape_common import *


def main():
    modest()
    folder=ROOT/'results/decomposition'
    folder.mkdir(parents=True,exist_ok=False)
    chain=ancestors()
    for seal in [PARENT/'results/stage-integrity.json',inherited.PARENT/'results/stage-integrity.json']:
        packet=chain[seal]
        for name,expected in packet['file_hashes'].items():
            assert digest(seal.parent.parent/name)==expected,name
    raw_path=PARENT/'results/projection/status.json'
    raw=json.loads(raw_path.read_text())
    basis=infrared_ladder.ConsistentBasis(**raw['basis_specification'])
    readings={
        'canonical700':ShapeReadout(basis,canonical=True),
        'full1400':ShapeReadout(basis,1400),
        'full2100':ShapeReadout(basis,2100)}
    for lower,name in [(5e-5,'cut5e-5'),(1e-4,'cut1e-4'),(1e-3,'cut1e-3')]:
        for count in [1400,2100]:
            readings[name+'-'+str(count)]=ShapeReadout(basis,count,lower)
    canonical=readings['canonical700']
    checks,inputs=[],[raw_path,ROOT/'DERIVATION.md']
    summaries={}
    eps=np.finfo(float).eps
    def test(name,value,limit=1e-10):
        checks.append(dict(name=name,value=float(value),limit=limit,passed=bool(np.isfinite(value) and value<limit)))
    def invariant_checks(label,reader,result):
        scale=np.maximum(result['distortion_norm'],1e-300)
        original_scale=np.maximum(weighted_norm(result['potential'],reader.measure),scale)
        test('Reconstruction:'+label,
            np.max(weighted_norm(result['temperature']+result['joint']+result['residual']-result['potential'],reader.measure)/original_scale))
        cross=(reader.templates.T*reader.measure)@result['residual']
        test('Residual orthogonal to both templates:'+label,
            np.max(abs(cross)/(reader.template_norms[:,None]*scale)))
        test('Joint versus residual squared-norm partition:'+label,
            np.max(abs(result['distortion_norm']**2-result['joint_norm']**2-result['residual_norm']**2)/scale**2))
        residual_energy=(reader.measure*reader.frequency)@result['residual']
        allowance=256*eps*np.maximum((reader.measure*reader.frequency)@
            (abs(result['potential'])+abs(result['temperature'])+abs(result['joint'])+abs(result['residual'])),1e-300)
        test('Residual energy equals recorded input quadrature discrepancy:'+label,
            np.max(abs(residual_energy-result['energy_defect'])/allowance),1.)
        alternate=linalg.lstsq(reader.design,np.sqrt(reader.measure)[:,None]*result['distortion'],lapack_driver='gelsd')[0]/reader.template_norms[:,None]
        test('QR readout independently matches SVD:'+label,
            np.max(weighted_norm(reader.templates@(alternate-result['amplitudes']),reader.measure)/scale))
        standard=reader.frequency[:,None]*result['eta_standard']+reader.standard@result['amplitudes']+result['residual']
        test('Standard temperature convention reconstructs same spectrum:'+label,
            np.max(weighted_norm(standard-result['potential'],reader.measure)/original_scale))
    for label,reader in readings.items():
        assert np.linalg.matrix_rank(reader.design)==2
        test('Two-template conditioning:'+label,reader.condition,1e6)
        template_energy=(reader.measure*reader.frequency)@reader.templates
        allowance=256*eps*np.maximum((reader.measure*reader.frequency)@abs(reader.standard),1e-300)
        test('Templates energy-free within rounding:'+label,np.max(abs(template_energy)/allowance),1.)
        reference=np.array([[.21,-.15,0.,.13],[0.,0.,-.26,.17]])
        synthetic=reader.templates@reference
        temperature_test=np.array([.1,-.2,.04,.09])
        recovered=reader.split_values(synthetic+reader.frequency[:,None]*temperature_test,reader.capacity*temperature_test)
        test('Synthetic mu-only y-only mixed controls:'+label,np.max(abs(recovered['amplitudes']-reference)))
        test('Synthetic signals leave no unexplained residual:'+label,
            np.max(weighted_norm(recovered['residual'],reader.measure))/
            max(float(np.max(weighted_norm(synthetic,reader.measure))),1e-300))
        only_temp=reader.split_values(reader.frequency[:,None]*np.array([.3,-.7]),reader.capacity*np.array([.3,-.7]))
        test('Pure temperature is not labeled mu or y:'+label,np.max(abs(only_temp['amplitudes'])))
        probe=np.sin(np.log(reader.frequency+1))
        probe_result=reader.split_values(probe[:,None])
        orthogonal_probe=probe_result['residual']
        control=reader.split_values(orthogonal_probe)
        test('Non-template synthetic residual is retained:'+label,
            np.max(weighted_norm(control['residual']-orthogonal_probe,reader.measure)/
                weighted_norm(orthogonal_probe,reader.measure)))
        test('Synthetic residual gives no spurious mu/y:'+label,
            np.max(weighted_norm(control['joint'],reader.measure)/weighted_norm(orthogonal_probe,reader.measure)))
        np.savez(folder/(label+'-definition.npz'),frequency=reader.frequency,measure=reader.measure,
            standard=reader.standard,templates=reader.templates,shifts=reader.shifts,
            gram=reader.gram,singular_values=reader.singular,amplitude_matrix=reader.amplitude_matrix)
    test('Canonical inner product equals inherited mass',
        np.max(abs((canonical.values.T*canonical.measure)@canonical.values-basis.mass)))
    for label in ['canonical700','full1400','full2100']:
        reader=readings[label]
        moments=reader.measure@reader.standard
        energy=(reader.measure*reader.frequency)@reader.standard
        test('Standard mu and y number-preserving Planck moments:'+label,np.max(abs(moments)),1e-8)
        test('Standard y full-band energy equals4:'+label,abs(energy[1]/4-1),1e-8)
        test('Standard mu full-band energy normalization:'+label,
            abs(energy[0]-(4/BETA-6*special.zeta(3)/I3)),1e-8)
    case_names=['main-256','main-512','main-1024','from-parent128-1024','from-parent256-1024','split-second-512']
    for model in ['heavy','cold']:
        baseline_path=BRANCH/'infrared-source-domain-20261008/backgrounds'/f'{model}-nonlocal-refined-6400/history.npz'
        packet_path=inherited.PARENT/'results/window-transfer'/f'{model}-final-window-contribution.npz'
        inputs.extend([baseline_path,packet_path])
        with np.load(baseline_path) as archive,np.load(packet_path) as packet:
            baseline=archive['profiles'][-1].copy()
            baseline_energy=float(archive['energy_scaled'][-1])
            heat=float(archive['heat'])
            assert np.array_equal(baseline,packet['parent_photon'])
            assert np.array_equal(archive['temperature_template'],basis.temperature)
            assert np.array_equal(archive['energy_row'],basis.energy)
        assert heat==raw['models'][model]['metadata']['heat']
        cases={}
        for case in case_names:
            path=PARENT/'results/projection'/f'{model}-{case}-projected.npz'
            inputs.append(path)
            with np.load(path) as saved:
                photon=saved['photon'].copy()
                energy=saved['energy'].copy()
            combined=np.column_stack([baseline,photon])
            combined_energy=np.r_[baseline_energy,energy]
            result=canonical.apply(combined,combined_energy)
            invariant_checks(model+':'+case,canonical,result)
            if case=='main-1024':
                authoritative_photon,authoritative_energy=combined,combined_energy
            cases[case]=result
            np.savez(folder/f'{model}-{case}-canonical.npz',**result,photon=combined,
                heat=heat,physical_amplitudes=heat*result['amplitudes'],
                physical_temperature_standard=heat*result['eta_standard'])
        fine=cases['main-1024']
        assert np.all(fine['distortion_norm']>0)
        test('Primary energy discrepancy inside inherited cancellation allowance:'+model,
            np.max(abs(fine['energy_defect'])/(256*eps*np.maximum(abs(basis.energy)@abs(authoritative_photon),1e-300))),1.)
        budget={}
        for level,offsets in [('43',[5,7,9]),('54',[11,13,15])]:
            parts=[fine['amplitudes'][:,offset:offset+2] for offset in offsets]
            residuals=[fine['residual'][:,offset:offset+2] for offset in offsets]
            component_amplitudes=sum(abs(part) for part in parts)
            residual_sum=sum(weighted_norm(part,canonical.measure) for part in residuals)
            coherent=weighted_norm(sum(residuals),canonical.measure)
            test('Residual component-sum triangle:'+model+':'+level,
                np.max((coherent-residual_sum)/fine['distortion_norm'][1:3]))
            central_amplitude=abs(fine['amplitudes'][:,1:3])
            budget[level]=dict(
                absolute_scaled_amplitude_sum=component_amplitudes.tolist(),
                relative_mu_y_amplitude_sum=np.divide(component_amplitudes,central_amplitude,
                    out=np.full_like(component_amplitudes,np.nan),where=central_amplitude>0).tolist(),
                physical_mu_y_absolute_sum=(heat*component_amplitudes).tolist(),
                residual_component_sum_absolute=residual_sum.tolist(),
                residual_component_sum_relative_to_central_residual=(residual_sum/fine['residual_norm'][1:3]).tolist(),
                residual_component_sum_relative_to_full_distortion=(residual_sum/fine['distortion_norm'][1:3]).tolist(),
                residual_coherent_relative_to_central_residual=(coherent/fine['residual_norm'][1:3]).tolist())
        component_total=sum(fine['amplitudes'][:,offset:offset+2] for offset in [11,13,15])
        component_residual=sum(fine['residual'][:,offset:offset+2] for offset in [11,13,15])
        amp_denom=sum(abs(fine['amplitudes'][:,offset:offset+2]) for offset in [11,13,15])
        res_denom=sum(weighted_norm(fine['residual'][:,offset:offset+2],canonical.measure) for offset in [11,13,15])
        test('Independent54 total equals projected mu/y component sum:'+model,
            np.max(abs(fine['amplitudes'][:,3:5]-component_total)/amp_denom),1e-8)
        test('Independent54 total equals residual component sum:'+model,
            np.max(weighted_norm(fine['residual'][:,3:5]-component_residual,canonical.measure)/res_denom),1e-8)
        numerical={}
        for case in case_names:
            if case=='main-1024':
                continue
            result=cases[case]
            numerical[case]=dict(
                correction_mu_y_relative=(abs(result['amplitudes'][:,1:3]-fine['amplitudes'][:,1:3])/
                    abs(fine['amplitudes'][:,1:3])).tolist(),
                correction_residual_relative=(weighted_norm(result['residual'][:,1:3]-fine['residual'][:,1:3],canonical.measure)/
                    fine['residual_norm'][1:3]).tolist())
        bands={}
        for label,reader in readings.items():
            full_band=reader.minimum==basis.minimum
            result=reader.apply(authoritative_photon,authoritative_energy if full_band else None)
            invariant_checks(model+':'+label,reader,result)
            physical=heat*result['amplitudes']
            bands[label]=dict(
                scaled_amplitudes=result['amplitudes'][:,:3].tolist(),
                physical_mu_y_amplitudes=physical[:,:3].tolist(),
                residual_norm_fraction=result['residual_fraction'][:3].tolist(),
                jointly_captured_squared_norm_fraction=result['captured_squared_fraction'][:3].tolist(),
                energy_defect=result['energy_defect'][:3].tolist(),
                standard_temperature_fraction=(heat*result['eta_standard'][:3]).tolist(),
                energy_temperature_fraction=(heat*result['eta'][:3]).tolist(),
                mu_y_change_relative_to_primary=(abs(result['amplitudes'][:,:3]-fine['amplitudes'][:,:3])/
                    abs(fine['amplitudes'][:,:3])).tolist(),
                residual_norm=result['residual_norm'][:3].tolist(),
                distortion_norm=result['distortion_norm'][:3].tolist(),
                maximum_phase_space_number_defect=float(np.max(abs(reader.measure@reader.standard))))
            if label!='canonical700':
                np.savez(folder/f'{model}-{label}.npz',**result,physical_amplitudes=physical)
        summaries[model]=dict(heat=heat,bands=bands,frequency_budgets=budget,saved_numerical_comparisons=numerical,
            correction_over_baseline_signed_mu_y=(fine['amplitudes'][:,1:3]/fine['amplitudes'][:,0,None]).tolist(),
            canonical_amplitudes_all_columns=fine['amplitudes'].tolist(),
            canonical_residual_fraction_all_columns=fine['residual_fraction'].tolist())
        print(json.dumps(dict(model=model,primary=bands['canonical700'],budgets=budget,
            cutoffs={key:value['residual_norm_fraction'] for key,value in bands.items()})),flush=True)
    for path in inputs:
        if path.is_relative_to(ROOT):
            continue
        inherited.inherited.verify_reference(path,chain)
    checks.append(dict(name='All consumed scientific files match sealed owners',value=len(inputs),passed=True))
    reader_metadata={name:dict(minimum=reader.minimum,maximum=reader.maximum,count=reader.count,
        condition=reader.condition,correlation=reader.correlation,energy_shifts=reader.shifts.tolist(),
        template_norms=reader.template_norms.tolist(),capacity=reader.capacity) for name,reader in readings.items()}
    finish(folder,dict(checks=checks,models=summaries,readouts=reader_metadata,beta=float(BETA),
        column_order=['saved-parent-baseline',*raw['column_order']],
        same_readout_for_baseline_and_window=True,full_96_mode_input_retained=True,
        source_evaluations=0,evolution_rerun=False,physical_parameters_fitted=False,
        empirical_fit=False,instrument_metric=False,new_physical_model=False,github_action=False,
        final_saved_scale=1e-5,physical_amplitude_is_chi_times_scaled=True,
        infrared_continuation_derived=False,later_time_transfer_derived=False,
        continuum_error_bounded=False,primary_independent_energy_retained=True,
        restricted_band_uses_own_energy=True,orthogonal_residual_retained=True,
        mu_y_component_powers_not_added=True),__file__,inputs)
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']])),flush=True)
    if not all(row['passed'] for row in checks):
        raise SystemExit(1)


if __name__=='__main__':
    main()

