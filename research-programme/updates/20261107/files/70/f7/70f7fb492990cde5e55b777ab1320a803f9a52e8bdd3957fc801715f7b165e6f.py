from residual_kinetic_common import *


def main():
    modest()
    folder=ROOT/'results/kinetic-drive'
    folder.mkdir(parents=True,exist_ok=False)
    chain=ancestors()
    for name,expected in chain[PARENT/'results/stage-integrity.json']['file_hashes'].items():
        assert digest(PARENT/name)==expected,name
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    readout=ResidualMap(basis)
    checks,inputs,summaries=[],[*ladder.inputs],{}
    def test(name,value,limit):
        checks.append(dict(name=name,value=float(value),limit=limit,passed=bool(np.isfinite(value) and value<=limit)))
    test('Mass-projected decomposition identity',
        np.linalg.norm(readout.dual+np.outer(basis.temperature,readout.eta)+readout.projected_templates@readout.amplitude-np.eye(96)),1e-10)
    test('Residual projection annihilates temperature',norm((readout.mapping@basis.temperature)[:,None],basis.measure)[0],1e-10)
    test('Residual orthogonal to mu and y',np.linalg.norm((readout.reader.templates.T*basis.measure)@readout.mapping),1e-10)
    analytic_defect=readout.reader.templates-basis.values@readout.projected_templates
    template_defect=norm(analytic_defect,basis.measure)/readout.reader.template_norms
    for model in ['heavy','cold']:
        background=thermal_wave.thermal.ThermalBackground(model)
        emission=NonlocalEmission(basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
        inputs.extend([*emission.inputs,background.parent.source,background.native_constants])
        baseline_path=BASELINE/f'{model}-nonlocal-refined-6400/history.npz'
        with np.load(baseline_path) as archive:
            baseline={key:archive[key].copy() for key in archive.files}
        inputs.extend([baseline_path,baseline_path.parent/'status.json'])
        np.savez(folder/f'{model}-reconstructed-br-table.npz',temperatures=emission.temperatures,blocks=emission.br_blocks)
        for path in inputs:
            verify_source(path,chain)
        cases={}
        for steps in [1024,512,256]:
            window_path=WINDOW/f'{model}-main-{steps}.npz'
            inputs.append(window_path)
            verify_source(window_path,chain)
            with np.load(window_path) as archive:
                window={key:archive[key].copy() for key in archive.files}
            baseline_indices=np.arange(3200,6401,50)
            window_indices=np.arange(0,steps+1,steps//64)
            coordinate=window['coordinate'][window_indices]
            assert np.max(abs(coordinate-baseline['expansion'][baseline_indices]))<1e-13
            photon=np.concatenate([baseline['profiles'][baseline_indices,:,None],window['photon'][window_indices]],axis=2)
            gas=np.column_stack([baseline['temperature_scaled'][baseline_indices],window['gas'][window_indices]])
            independent_energy=np.column_stack([baseline['energy_scaled'][baseline_indices],window['energy'][window_indices]])
            spectral_energy=np.einsum('i,nij->nj',readout.energy,photon)
            allowance=512*np.finfo(float).eps*np.maximum(np.einsum('i,nij->nj',abs(basis.energy),abs(photon)),1e-300)
            test(f'Saved independent energy preserved within roundoff:{model}:{steps}',np.max(abs(spectral_energy-independent_energy)/allowance),1.)
            power=np.empty((65,3,17))
            rates=np.empty((65,3,3,4,17))
            residuals=np.empty((65,700,3))
            derivatives=np.zeros((65,96,17))
            rhs_history=np.empty((65,96,17))
            gamma=np.empty((65,17))
            norms_rhs=np.empty((65,17))
            errors={name:0. for name in ['split','self_identity','operator_sum','symmetry','positivity','original_photon','projected_photon','gas','bdf_identity','bdf_rate_budget']}
            absolute={name:0. for name in ['photon','projected','gas']}
            for epoch,position in enumerate(coordinate):
                local=background.at(float(position))
                theta=local['thermal_parameter']
                rate=local['coefficient']/theta
                scattering=ladder.at(theta,0)[:96,:96]
                dc=emission.at(theta,'dc')
                br=emission.interpolator(np.log(theta))
                operators=np.stack([scattering,-dc,-br])*rate
                direct=(scattering-emission.at(theta,'dcbr'))*rate
                scale=max(float(np.linalg.norm(direct)),1e-300)
                errors['operator_sum']=max(errors['operator_sum'],float(np.linalg.norm(operators.sum(axis=0)-direct)/scale))
                pieces=readout.pieces(photon[epoch],gas[epoch])
                departure=photon[epoch]-basis.temperature[:,None]*gas[epoch]
                errors['split']=max(errors['split'],float(np.max(np.linalg.norm(pieces.sum(axis=0)-departure,axis=0)/np.maximum(np.linalg.norm(pieces,axis=1).sum(axis=0),1e-300))))
                applied=np.einsum('aij,bjk->abik',operators,pieces)
                coefficient_rates=linalg.solve(basis.mass,applied.transpose(2,0,1,3).reshape(96,-1),assume_a='pos').reshape(96,3,4,17).transpose(1,2,0,3)
                direct_rhs=linalg.solve(basis.mass,direct@departure,assume_a='pos')
                rhs_history[epoch]=direct_rhs
                norm_scale=np.linalg.norm(coefficient_rates.sum(axis=1),axis=1).sum(axis=0)
                norms_rhs[epoch]=norm_scale
                for band,(name,frequency,measure,mapping) in enumerate(readout.bands):
                    residual=mapping@photon[epoch]
                    mapped_rates=np.einsum('fi,abik->abfk',mapping,coefficient_rates)
                    power[epoch,band]=np.sum(measure[:,None]*residual**2,axis=0)
                    rates[epoch,band]=np.einsum('fk,abfk,f->abk',residual,mapped_rates,measure)
                    if band==0:
                        residuals[epoch]=residual[:,:3]
                        exact_self=np.einsum('ik,aij,jk->ak',pieces[0],operators,pieces[0])
                        errors['self_identity']=max(errors['self_identity'],float(np.max(abs(rates[epoch,0,:,0]-exact_self)/
                            np.maximum(np.sum(abs(rates[epoch,0]),axis=(0,1))[None,:],1e-300))))
                        gamma[epoch]=-exact_self.sum(axis=0)/np.maximum(power[epoch,0],1e-300)
                if steps==1024:
                    for operator in operators:
                        operator_norm=max(float(np.linalg.norm(operator,2)),1e-300)
                        errors['symmetry']=max(errors['symmetry'],float(np.linalg.norm(operator-operator.T)/operator_norm))
                        errors['positivity']=max(errors['positivity'],float(linalg.eigvalsh((operator+operator.T)/2)[-1]/operator_norm))
                if epoch:
                    base_index,window_index=baseline_indices[epoch],window_indices[epoch]
                    base_step=baseline['expansion'][1]-baseline['expansion'][0]
                    window_step=window['coordinate'][1]-window['coordinate'][0]
                    older=[]; older_gas=[]
                    for offset in [0,1,2]:
                        older.append(np.column_stack([baseline['profiles'][base_index-offset],window['photon'][window_index-offset]]))
                        older_gas.append(np.r_[baseline['temperature_scaled'][base_index-offset],window['gas'][window_index-offset]])
                    steps_vector=np.r_[base_step,np.full(16,window_step)]
                    bdf=(1.5*older[0]-2*older[1]+.5*older[2])/steps_vector
                    gas_bdf=(1.5*older_gas[0]-2*older_gas[1]+.5*older_gas[2])/steps_vector
                    derivatives[epoch]=bdf
                    defect=bdf-direct_rhs
                    absolute['photon']=max(absolute['photon'],float(np.max(np.linalg.norm(defect,axis=0))))
                    errors['original_photon']=max(errors['original_photon'],float(np.max(np.linalg.norm(defect,axis=0)/np.maximum(norm_scale,1e-300))))
                    projected_norms=np.stack([norm(readout.mapping@coefficient_rates[term].sum(axis=0),basis.measure) for term in range(3)]).sum(axis=0)
                    residual_defect=norm(readout.mapping@defect,basis.measure)
                    absolute['projected']=max(absolute['projected'],float(residual_defect.max()))
                    errors['projected_photon']=max(errors['projected_photon'],float(np.max(residual_defect/np.maximum(projected_norms,1e-300))))
                    gas_source=np.r_[1.,np.zeros(16)]
                    gas_residual=background.chi*(gas_bdf+gas[epoch])+gas_source+basis.energy@direct_rhs
                    gas_scale=abs(gas_source)+abs(background.chi*(gas_bdf+gas[epoch]))+abs(basis.energy@direct_rhs)
                    errors['gas']=max(errors['gas'],float(np.max(abs(gas_residual)/np.maximum(gas_scale,1e-300))))
                    absolute['gas']=max(absolute['gas'],float(np.max(abs(gas_residual))))
                    for band,(name,frequency,measure,mapping) in enumerate(readout.bands):
                        current,previous,previous2=[mapping@item for item in older]
                        norm2=lambda value:np.sum(measure[:,None]*value**2,axis=0)
                        discrete=np.sum(measure[:,None]*current*(mapping@bdf),axis=0)
                        g_current=(norm2(current)+norm2(2*current-previous))/4
                        g_previous=(norm2(previous)+norm2(2*previous-previous2))/4
                        curvature=norm2(current-2*previous+previous2)/(4*steps_vector)
                        identity=(g_current-g_previous)/steps_vector+curvature
                        comparison_scale=np.maximum(np.sum(abs(rates[epoch,band]),axis=(0,1)),1e-300)
                        errors['bdf_identity']=max(errors['bdf_identity'],float(np.max(abs(identity-discrete)/comparison_scale)))
                        errors['bdf_rate_budget']=max(errors['bdf_rate_budget'],float(np.max(abs(discrete-rates[epoch,band].sum(axis=(0,1)))/comparison_scale)))
            for key,limit in [('split',1e-10),('self_identity',1e-10),('operator_sum',1e-10),('symmetry',1e-10),
                              ('positivity',1e-12),('original_photon',1e-6),('projected_photon',1e-6),('gas',1e-6),
                              ('bdf_identity',1e-6),('bdf_rate_budget',1e-6)]:
                test(f'{key}:{model}:{steps}',errors[key],limit)
            test(f'All full-band self terms dissipative:{model}:{steps}',np.max(rates[:,:, :,0][:,0]/
                np.maximum(np.sum(abs(rates[:,0]),axis=(1,2))[:,None,:],1e-300)),1e-12)
            output=folder/f'{model}-{steps}.npz'
            np.savez(output,coordinate=coordinate,photon=photon,gas=gas,independent_energy=independent_energy,
                residual_power=power,residual_power_half_derivative_terms=rates,self_rate=gamma,
                primary_residual=residuals,bdf_coefficient_derivative=derivatives,operator_coefficient_derivative=rhs_history,
                term_norm_scale=norms_rhs)
            row=dict(errors=errors,absolute_errors=absolute,
                endpoint_residual_power=power[-1,:,:3].tolist(),
                residual_power_final_over_initial=(power[-1,:,:3]/power[0,:,:3]).tolist(),
                endpoint_half_power_rate_terms=rates[-1,:,:,:,:3].tolist(),
                endpoint_self_rate=gamma[-1,:3].tolist(),
                minimum_self_rate=np.min(gamma[:,:3],axis=0).tolist(),
                maximum_self_rate=np.max(gamma[:,:3],axis=0).tolist(),
                net_half_power_rate_sign_counts={name:dict(positive=(rates[:,band].sum(axis=(1,2))[:,:3]>0).sum(axis=0).tolist(),
                    negative=(rates[:,band].sum(axis=(1,2))[:,:3]<0).sum(axis=0).tolist()) for band,(name,*rest) in enumerate(readout.bands)})
            cases[str(steps)]=row
            print(json.dumps(dict(model=model,steps=steps,errors=errors,endpoint_self_rate=row['endpoint_self_rate'])),flush=True)
        with np.load(folder/f'{model}-1024.npz') as fine:
            primary_power=fine['residual_power'].copy()
            primary_residual=fine['primary_residual'].copy()
            endpoint_photon=fine['photon'][-1]
        with np.load(PARENT/'results/decomposition'/f'{model}-main-1024-canonical.npz') as old:
            old_residual=old['residual'][:,:3]
            test(f'Stage109 endpoint reproduced:{model}',np.max(norm(primary_residual[-1]-old_residual,basis.measure)/norm(old_residual,basis.measure)),1e-10)
        inputs.append(PARENT/'results/decomposition'/f'{model}-main-1024-canonical.npz')
        refinements={}
        for steps in [512,256]:
            with np.load(folder/f'{model}-{steps}.npz') as coarse:
                difference=np.sqrt(np.sum(basis.measure[None,:,None]*(primary_residual-coarse['primary_residual'])**2,axis=1))
                relative=difference/np.maximum(np.sqrt(primary_power[:,0,:3]),1e-300)
                refinements[str(steps)]=dict(maximum_relative=relative.max(axis=0).tolist(),endpoint_relative=relative[-1].tolist())
        parts=[readout.mapping@endpoint_photon[:,offset:offset+2] for offset in [11,13,15]]
        budget=sum(norm(part,basis.measure) for part in parts)/np.sqrt(primary_power[-1,0,1:3])
        summaries[model]=dict(cases=cases,refinements=refinements,source54_endpoint_residual_component_budget=budget.tolist())
    finish(folder,dict(checks=checks,models=summaries,analytic_template_representation_defect=template_defect.tolist(),
        full_modes=96,matched_epochs=65,post_seam_native_bdf_checks=64,operators=TERM_NAMES,drives=DRIVE_NAMES,
        band_order=['full','low','peak'],column_order=['saved_baseline']+['window_'+str(index) for index in range(16)],
        fixed_background=True,no_evolution_rerun=True,no_finite_source_event_integrals=True,
        bremsstrahlung_matrices_reconstructed_from_unchanged_tables=True,
        baseline_time_refinement_not_matched=True,physical_parameters_fitted=False,empirical_fit=False,
        residual_scalar_closure_assumed=False,infrared_continuation_derived=False,github_action=False),
        __file__,inputs)
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
