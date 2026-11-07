from __future__ import annotations

from seed_common import *


def main():
    modest()
    folder=ROOT/'results/native-seed-valid'
    folder.mkdir(parents=True,exist_ok=False)
    evolution=inherited.inherited.evolution
    camb=evolution.camb
    scales=np.array([1e-7,1.05e-7,1.1e-7])
    waves=np.array([.03,.1,1.,5.])
    names=camb.model.evolve_names
    rows=[]
    inputs=[]
    native_metadata=[]
    seed_paths=[]
    for label in ['heavy','cold','lcdm']:
        source=BACKGROUND if label=='heavy' else BRANCH/'native-two-field-transfer-20261007/runs/backgrounds/cold.npz'
        table=np.load(source)
        params=evolution.inherited.params_for(source)
        if label=='lcdm':
            params.DarkEnergy=camb.dark_energy.DarkEnergyFluid()
        native=camb.get_background(params)
        times=native.conformal_time(1/scales-1,tol=1e-10)
        native.Params.Accuracy.IntTolBoost=6
        values=native.get_time_evolution(waves,times,vars=names,lAccuracyBoost=4)
        assert np.all(values[:,:,names.index('a')]>0), 'Native exporter skipped a requested time before its per-mode initialization'
        assert np.max(abs(values[:,:,names.index('a')]/scales-1))<1e-7
        assert np.isfinite(values).all()
        densities=native.get_background_densities(scales,vars=['cdm','baryon','photon','neutrino','nu'])
        radiation=densities['photon']+densities['neutrino']+densities['nu']
        fractions=(densities['neutrino']+densities['nu'])/radiation
        beta=np.sqrt(radiation/3)
        metadata=dict(branch=label,scales=scales.tolist(),conformal_times=times.tolist(),
            beta=beta.tolist(),neutrino_fractions=fractions.tolist(),
            cold_to_radiation=((densities['cdm']+densities['baryon'])/radiation).tolist(),
            max_radiation_clock_relative_error=float(max(abs(scales/(beta*times)-1))))
        native_metadata.append(metadata)
        np.savez_compressed(folder/(label+'.npz'),waves=waves,scales=scales,times=times,names=names,values=values,
            beta=beta,neutrino_fraction=fractions,**densities)
        for mode,wave in enumerate(waves):
            eta=values[mode,:,names.index('etak')]/wave
            eta_coefficient=(5+4*fractions)/(12*(15+4*fractions))
            zeta0=float(-eta[0]/(1-eta_coefficient[0]*(wave*times[0])**2))
            cold_prediction=zeta0*(wave*times)**2/4
            tests={'cold':(cold_prediction,values[mode,:,names.index('delta_cdm')]),
                'baryon':(cold_prediction,values[mode,:,names.index('delta_baryon')]),
                'photon':(4*cold_prediction/3,values[mode,:,names.index('delta_photon')]),
                'neutrino':(4*cold_prediction/3,values[mode,:,names.index('delta_neutrino')])}
            if label!='lcdm':
                for suffix,table_key in [('s','slow'),('h','heavy')]:
                    if suffix=='h' and label!='heavy':
                        continue
                    mass=float(table[table_key+'_mass_mpc'])
                    field0=float(table['phi_'+suffix][0])
                    prediction=-field0*(beta*mass*times**2)**2*cold_prediction/105
                    tests[table_key+'_field']=(prediction,values[mode,:,names.index('mts_dphi_'+suffix)])
            for quantity,(prediction,actual) in tests.items():
                error=abs(actual/prediction-1)
                rows.append(dict(branch=label,k_Mpc_inverse=float(wave),quantity=quantity,
                    relative_errors=error.tolist(),max_relative_error=float(max(error)),
                    primary=bool(wave<=1),qualified=bool(max(error)<.01),
                    zeta_normalization_from_native_eta=zeta0,max_k_tau=float(wave*times[-1])))
            if label=='heavy' and wave<=1:
                count=256
                phase=np.linspace(0,2*math.pi,count,endpoint=False)
                shape=np.cos(phase)+.2*np.cos(2*phase+.3)
                first=-np.sin(phase)-.4*np.sin(2*phase+.3)
                second=-np.cos(phase)-.8*np.cos(2*phase+.3)
                curvature1=-4*wave**2*second
                curvature2=wave**2*(8*shape*second-2*first**2)
                tau=float(times[0])
                response=1+4*float(fractions[0])/15
                cold1=tau**2*curvature1/16
                cold2=tau**2*curvature2/16
                displacement=-3*(np.sin(phase)+.1*np.sin(2*phase+.3))/wave
                pullback=displacement*wave*derivative(cold1)
                sources=dict(phase=phase,shape=shape,curvature_first=curvature1,curvature_second=curvature2,
                    cold_first=cold1,cold_second_conformal=cold2,cold_second_native_extension=cold2+pullback,
                    radiation_first=4*cold1/3,radiation_second_conformal=4*cold2/3,
                    radiation_second_native_extension=4*(cold2+pullback)/3,
                    neutrino_response_denominator=response,tau=tau,scale=float(scales[0]),
                    k_Mpc_inverse=wave,primordial_zeta_second=0.,amplitude_convention='coefficients per epsilon and epsilon squared',
                    conditional_zeta_amplitude=1e-5)
                for suffix,table_key in [('s','slow'),('h','heavy')]:
                    mass=float(table[table_key+'_mass_mpc'])
                    field0=float(table['phi_'+suffix][0])
                    factor=-field0*(float(beta[0])*mass*tau**2)**2/105
                    sources.update({table_key+'_mass_Mpc_inverse':mass,table_key+'_field_first':factor*cold1,
                        table_key+'_field_second_conformal':factor*cold2,
                        table_key+'_field_second_native_extension':factor*(cold2+pullback),
                        table_key+'_field_prime_first':6*factor*cold1/tau,
                        table_key+'_field_prime_second_native_extension':6*factor*(cold2+pullback)/tau})
                path=folder/('quadratic-seed-'+str(wave)+'.npz')
                np.savez_compressed(path,**sources)
                seed_paths.append(path)
        inputs.append(source)
        print(json.dumps(dict(branch=label,max_primary_error=max(row['max_relative_error'] for row in rows if row['branch']==label and row['primary']))),flush=True)
    cold_controls=[]
    for initial_redshift in [1.,2.,10.]:
        ratio=(1+.38)/(1+initial_redshift)
        cold_controls.append(dict(initial_redshift=initial_redshift,final_redshift=.38,
            EdS_zero_quadratic_seed_fractional_deficit=ratio,
            interpretation='Exact planar growing cold limit; not a fitted MTS initial condition.'))
    dust_residuals=[]
    for label in ['heavy','cold','lcdm']:
        for wave in [.03,.1,1.]:
            model=inherited.NativeSeed(label,wave)
            reference=inherited.NativeSeed('lcdm',wave)
            initial=model.seed(float(reference.density[0,reference.final])).reshape(4,-1)
            density,velocity=initial[:2]
            friction,gravity,pressure=model.coefficients(inherited.INITIAL)
            residual=density*np.dot(gravity,density)-np.dot(gravity,density**2)+12*pressure*density**2
            scale=np.maximum(abs(density*np.dot(gravity,density))+abs(np.dot(gravity,density**2))+velocity**2,1e-10)
            dust_residuals.append(dict(branch=label,k_Mpc_inverse=wave,species=model.species,
                residual=residual.tolist(),normalized_residual=(abs(residual)/scale).tolist(),
                copied_dust_seed_proved=False))
            inputs+=model.paths+reference.paths
    finish(folder,dict(rows=rows,native_metadata=native_metadata,cold_controls=cold_controls,
        dust_ansatz_residuals=dust_residuals,source_backed_seed_paths=[str(path) for path in seed_paths],
        primordial_zeta_second_chosen_zero=True,nonlinear_native_solver_installed=False,
        late_nonlinear_prediction=False,new_parameters_fitted=0),
        __file__,sorted(set(inputs))+[NATIVE/'fortran/MTSTwoField.f90',NATIVE/'camb/cambdll.dll',*folder.glob('*.npz')])
    print(json.dumps(dict(state='complete',comparison_rows=len(rows),seed_files=len(seed_paths),
        max_primary_error=max(row['max_relative_error'] for row in rows if row['primary']))))


if __name__=='__main__':
    main()
