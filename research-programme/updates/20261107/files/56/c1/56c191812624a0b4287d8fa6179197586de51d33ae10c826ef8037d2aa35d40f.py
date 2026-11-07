from __future__ import annotations

from boundary_common import *


def main():
    modest()
    folder=ROOT/'results/native-boundary'
    folder.mkdir(parents=True,exist_ok=False)
    inputs=[NATIVE/'fortran/equations.f90',NATIVE/'camb/cambdll.dll',NATIVE/'fortran/MTSTwoField.f90']
    reports=[]
    checks=[]
    columns=['delta_cdm','delta_baryon','delta_photon','delta_neutrino','v_photon','v_neutrino','etak','mts_dphi_s','mts_dphidot_s','mts_dphi_h','mts_dphidot_h']
    for label,source_name in [('heavy','unmatched-base.npz'),('cold','cold-base.npz')]:
        source=HISTORY/'runs/sources'/source_name
        old_path=GEOMETRY/'runs/native'/(label+'.npz')
        inputs.extend([source,old_path])
        old=np.load(old_path)
        names=list(old['names'])
        source_data=np.load(source)
        params=inherited.inherited.inherited.inherited.inherited.inherited.params_for(source)
        background=inherited.camb.get_background(params)
        beta=float(background.adotrad)
        radiation=float(background.grhog+background.grhornomass+sum(background.grhormass))
        neutrino_fraction=1-float(background.grhog)/radiation
        denominator=15+4*neutrino_fraction
        field_constants=[]
        for sector in ['s','h']:
            mass=float(source_data['slow_mass_mpc' if sector=='s' else 'heavy_mass_mpc'])
            active=sector=='s' or float(source_data['fraction'])>0
            frozen=float(source_data['phi_'+sector][0]) if active else 0.
            field_constants.append(dict(sector=sector,mass=mass,frozen=frozen,active=active))
        rows=[]
        for mode_index,mode in enumerate(old['modes']):
            values=old['values'][mode_index]
            scales=values[:,names.index('a')]
            valid=np.flatnonzero(scales>0)
            assert len(valid)>0
            zero_rows=int(np.sum(scales==0))
            per_mode=[]
            for requested_scale in [1e-8,3e-8,1e-7,3e-7,1e-6]:
                index=int(valid[np.argmin(abs(scales[valid]-requested_scale))])
                tau=float(old['conformal_time'][index])
                scale=float(scales[index])
                curvature=4*mode**2
                density=curvature*tau**2/16
                flux=mode**3*tau**3/27
                eta=-1+(denominator-10)*mode**2*tau**2/(12*denominator)
                prediction=[density,density,4*density/3,4*density/3,flux,flux*(denominator+8)/denominator,mode*eta]
                for field in field_constants:
                    response=-curvature*beta**2*field['mass']**2*field['frozen']*tau**6/1680
                    prediction.extend([response,6*response/tau])
                reference=values[index,[names.index(column) for column in columns]]
                prediction=np.array(prediction)
                errors=abs(prediction-reference)/np.maximum(np.maximum(abs(prediction),abs(reference)),1e-100)
                row=dict(model=label,mode=float(mode),requested_scale=requested_scale,scale=scale,tau=tau,
                    zero_padded_rows_excluded=zero_rows,predicted=prediction.tolist(),native=reference.tolist(),relative_errors=errors.tolist(),
                    finite_gradient_parameter=(float(mode)*tau)**2,
                    ordinary_matter_over_radiation=float((background.grhob+background.grhoc)*scale/radiation),
                    photon_temperature_over_electron_mass=4.59620157197772e-10/scale)
                rows.append(row)
                per_mode.append(row)
            early=max(per_mode[0]['relative_errors'][:6])
            late=max(per_mode[-1]['relative_errors'][:6])
            checks.append(dict(name=label+' k'+str(float(mode))+': leading ordinary seed improves toward early radiation era',passed=bool(early<late),earliest_error=early,latest_error=late))
        output=dict(model=label,columns=columns,beta=beta,neutrino_fraction=neutrino_fraction,
            fixed_primordial_curvature_normalization=1,normalization_from_native_chi_minus_one_not_fitted=True,
            field_constants=field_constants,rows=rows,raw_zero_padding_not_physical_data=True)
        write_json(folder/(label+'-comparison.json'),output)
        reports.append(dict(model=label,beta=beta,neutrino_fraction=neutrino_fraction,
            mode1e_minus1_early=rows[5]['relative_errors'],mode1e_minus1_late=rows[9]['relative_errors'],field_constants=field_constants))
        mode_p=np.array([.1,0.,0.])
        mode_q=np.array([0.,.1,0.])
        geometry=seed_geometry(mode_p,mode_q,neutrino_fraction)
        values=old['values'][1]
        valid=np.flatnonzero(values[:,names.index('a')]>0)
        selected=int(valid[np.argmin(abs(values[valid,names.index('a')]-1e-6))])
        tau=float(old['conformal_time'][selected])
        scalar=float(geometry['scalar2'])
        curvature_tensor=geometry['ricci2']-np.eye(3)*scalar/3
        independent=seed_linear(mode_p+mode_q)
        independent_ricci=linear_ricci(independent,mode_p+mode_q)
        independent_scalar=float(np.trace(independent_ricci))
        independent_rate=-5/denominator*(independent_ricci-np.eye(3)*independent_scalar/3)-np.eye(3)*independent_scalar/24
        field2=np.array([-scalar*beta**2*field['mass']**2*field['frozen']*tau**6/1680 for field in field_constants])
        field2_primordial=np.array([-independent_scalar*beta**2*field['mass']**2*field['frozen']*tau**6/1680 for field in field_constants])
        np.savez_compressed(folder/(label+'-orthogonal-seed.npz'),tau=tau,scale=values[selected,names.index('a')],
            momentum_p=mode_p,momentum_q=mode_q,neutrino_fraction=neutrino_fraction,**geometry,
            metric2=geometry['seed2']+tau**2*geometry['metric2_time_coefficient'],mixed_rate2=tau*geometry['rate2'],
            dust_density2=scalar*tau**2/16,radiation_density2=scalar*tau**2/12,
            neutrino_mixed_stress2_over_background=4*tau**2*curvature_tensor/(3*denominator),
            covariant_photon_velocity2=-1j*(mode_p+mode_q)*scalar*tau**3/144,
            covariant_neutrino_velocity2=-1j*(mode_p+mode_q)*scalar*tau**3*(denominator+8)/(144*denominator),
            field2=field2,field_prime2=6*field2/tau,
            primordial_metric2_per_zeta2=independent+tau**2*independent_rate,
            primordial_mixed_rate2_per_zeta2=tau*independent_rate,
            primordial_dust_density2_per_zeta2=independent_scalar*tau**2/16,
            primordial_radiation_density2_per_zeta2=independent_scalar*tau**2/12,
            primordial_field2_per_zeta2=field2_primordial,
            primordial_field_prime2_per_zeta2=6*field2_primordial/tau,
            full_coupled_second_order_solution=False,primordial_zeta2_value_assigned=False,
            finite_matter_and_gradient_corrections_required=True)
        checks.append(dict(name=label+': seed geometry and canonical responses finite',passed=bool(np.isfinite(field2).all() and np.isfinite(geometry['metric2_time_coefficient']).all())))
        print(json.dumps(reports[-1]),flush=True)
    passed=all(row['passed'] for row in checks)
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=passed,models=reports,
        full_second_order_initial_accuracy_certified=False,primordial_zeta2_not_predicted=True,
        usable_asymptotic_boundary_family_exported=True,native_normalization_not_fitted=True,
        no_electron_recoil_extrapolation_in_new_evolution=True),__file__,inputs)
    assert passed,checks


if __name__=='__main__':
    main()
