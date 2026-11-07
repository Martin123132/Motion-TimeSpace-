from __future__ import annotations

from spectrum_common import *


def main():
    modest()
    folder=ROOT/'results/growth-screen'
    folder.mkdir(parents=True,exist_ok=False)
    source=np.load(ROOT/'sources/sdss-growth/growth-only.npz')
    data=source['mean'];covariance=source['covariance'];redshifts=source['redshifts']
    spectrum=json.loads((ROOT/'results/spectrum/status.json').read_text())
    controls=json.loads((ROOT/'runs/native-control-integrals/status.json').read_text())
    by_label={row['label']:row for row in spectrum['branches']}
    rows=[]
    for label in ['heavy','cold','lcdm']:
        stats=by_label[label]['central']
        selected=[next(row for row in stats if abs(row['z']-redshift)<1e-10) for redshift in redshifts]
        definitions=['fsigma8_cdm_m','fsigma8_cb_m','fsigma8_cb_cb','velocity_sigma8_cb','d_sigma8m_d_lna']
        results=[]
        for definition in definitions:
            predicted=np.array([row[definition] for row in selected])
            residual=predicted-data
            chi2=float(residual@np.linalg.solve(covariance,residual))
            results.append(dict(definition=definition,prediction=predicted.tolist(),
                residual_over_marginal_error=(residual/np.sqrt(np.diag(covariance))).tolist(),
                conditional_chi2=chi2,claim_valid_as_general_MTS_likelihood=False))
        rows.append(dict(branch=label,mappings=results,parameter_fit=False,
            parameter_policy='Common inherited H0/Omega_m/As/ns/species; fixed slow and heavy benchmark parameters.'))
    control_errors=[]
    for control in controls['controls']:
        row=by_label[control['branch']]['central']
        sigma=np.array([item['sigma8_m'] for item in row])
        growth=np.array([item['fsigma8_cdm_m'] for item in row])
        control_errors.append(dict(branch=control['branch'],sigma8_max_relative_error=float(max(abs(sigma/np.array(control['sigma8'])-1))),
            fsigma8_max_relative_error=float(max(abs(growth/np.array(control['fsigma8_velocity_cdm_total'])-1)))))
    packets={label:np.load(ROOT/'results/spectrum'/(label+'.npz')) for label in ['heavy','cold','lcdm']}
    grid=packets['heavy']['modes'];scales=packets['heavy']['scales']
    band=(grid>=.007)&(grid<=.14)
    log_band=np.log(grid[band])
    log_width=log_band[-1]-log_band[0]
    shape=[]
    for redshift in redshifts:
        index=int(np.argmin(abs(scales-1/(1+redshift))))
        for label in ['heavy','cold']:
            ratios=packets[label]['velocity_cb'][band,index]/packets['lcdm']['velocity_cb'][band,index]
            amplitude=float(np.exp(integrate.trapezoid(np.log(ratios),x=log_band)/log_width))
            mismatch=ratios/amplitude-1
            shape.append(dict(branch=label,z=float(redshift),comparison='to LCDM velocity transfer over .007.. .14 Mpc^-1',
                unweighted_log_k_amplitude=amplitude,shape_residual_min=float(min(mismatch)),shape_residual_max=float(max(mismatch)),
                shape_residual_rms=float(np.sqrt(integrate.trapezoid(mismatch**2,x=log_band)/log_width)),survey_window_used=False))
    central=by_label['heavy']['central']
    variants=[]
    for row in spectrum['branches']:
        if row['label'].startswith('heavy-'):
            variants.append(dict(label=row['label'],sigma8_max_change=max(abs(other['sigma8_m']/base['sigma8_m']-1)
                for base,other in zip(central,row['central'])),growth_max_change=max(abs(other['fsigma8_cdm_m']/base['fsigma8_cdm_m']-1)
                for base,other in zip(central,row['central']))))
    ratio=packets['heavy']['linear_power_Mpc3'][:,-1]/packets['cold']['linear_power_Mpc3'][:,-1]
    crossings=np.flatnonzero((ratio[:-1]>.5)&(ratio[1:]<=.5))
    half=None
    if len(crossings):
        index=int(crossings[0])
        half=float(np.exp(np.interp(math.log(.5),np.log(ratio[index:index+2])[::-1],np.log(grid[index:index+2])[::-1])))
    finish(folder,dict(rows=rows,data_redshifts=redshifts.tolist(),data_mean=data.tolist(),
        native_control_checks=control_errors,matching_variations=variants,template_shape_diagnostics=shape,
        half_power_k_Mpc_inverse=half,number_of_observations=len(data),free_parameters_fitted=0,
        growth_only=True,geometry_not_added=True,ELG_not_Gaussianized=True,
        formal_model_preference=False,p_values_not_reported=True,
        interpretation='Conditional screening: real source-backed growth data, complete covariance, several explicit theory-to-compression mappings. Full-shape/window/bias validation is still needed before model-evidence claims.'),
        __file__,[ROOT/'sources/sdss-growth/status.json',ROOT/'sources/sdss-growth/growth-only.npz',
            ROOT/'results/spectrum/status.json',ROOT/'runs/native-control-integrals/status.json',
            *[ROOT/'results/spectrum'/(label+'.npz') for label in packets]])
    print(json.dumps(dict(rows=rows,controls=control_errors,matching=variants,half_power=half,shape=shape),indent=2))


if __name__=='__main__':
    main()
