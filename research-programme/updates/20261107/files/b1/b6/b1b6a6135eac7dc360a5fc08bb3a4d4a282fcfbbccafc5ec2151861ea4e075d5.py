from __future__ import annotations

from seed_common import *


def main():
    modest()
    folder=ROOT/'results/geometric-seed'
    folder.mkdir(parents=True,exist_ok=False)
    native=np.load(ROOT/'results/native-seed-valid/heavy.npz')
    background=np.load(BACKGROUND)
    scale=float(native['scales'][0])
    beta=float(native['beta'][0])
    fraction=float(native['neutrino_fraction'][0])
    response=1+4*fraction/15
    tau=scale/beta
    hubble=beta/scale**2
    count=16
    axis=np.linspace(0,2*math.pi,count,endpoint=False)
    first,second,third=np.meshgrid(axis,axis,axis,indexing='ij')
    angle=second+third+.3
    amplitude=1e-5
    zeta=amplitude*(np.cos(first)+.2*np.cos(angle))
    identity=np.eye(3)
    rows=[]
    checks=[]
    for wave in [.03,.1,1.]:
        gradient=np.stack([-amplitude*wave*np.sin(first),-.2*amplitude*wave*np.sin(angle),-.2*amplitude*wave*np.sin(angle)],axis=-1)
        hessian=np.zeros(zeta.shape+(3,3))
        hessian[...,0,0]=-amplitude*wave**2*np.cos(first)
        hessian[...,1,1]=hessian[...,2,2]=hessian[...,1,2]=hessian[...,2,1]=-.2*amplitude*wave**2*np.cos(angle)
        laplacian=np.trace(hessian,axis1=-2,axis2=-1)
        norm=np.sum(gradient**2,axis=-1)
        curvature=np.exp(-2*zeta)*(-4*laplacian-2*norm)
        tracefree=np.exp(-2*zeta)[...,None,None]*(-hessian+gradient[..., :,None]*gradient[...,None,:]+
            identity*(laplacian-norm)[...,None,None]/3)
        volume=-tau**2*curvature/16
        metric_correction=2*volume[...,None,None]*identity/3-tau**2*tracefree/(3*response)
        metric=scale**2*np.exp(2*zeta)[...,None,None]*(identity+metric_correction)
        expansion_shear=-tracefree/(3*beta*response)
        volume_rate=-curvature/(8*beta)
        extrinsic=-hubble*identity-volume_rate[...,None,None]*identity/3-expansion_shear
        frequency=np.fft.fftfreq(count,d=1/count)
        frequency[count//2]=0
        derivatives=[]
        transformed=np.fft.fftn(curvature)
        for component in range(3):
            shape=[1,1,1]
            shape[component]=count
            derivatives.append(np.fft.ifftn(transformed*(1j*wave*frequency.reshape(shape))).real)
        curvature_gradient=np.stack(derivatives,axis=-1)
        photon_velocity=-tau**3*curvature_gradient/144
        neutrino_velocity=photon_velocity*(1+8/(15*response))
        neutrino_stress=4*tau**2*tracefree/(45*response)
        cold=-volume
        radiation=-4*volume/3
        fields={}
        for suffix,title in [('s','slow'),('h','heavy')]:
            mass=float(background[title+'_mass_mpc'])
            initial=float(background['phi_'+suffix][0])
            factor=(mass*beta*tau**2)**2
            fields[title+'_field_background']=initial*(1-factor/20)
            fields[title+'_field_background_prime']=-initial*factor/(5*tau)
            fields[title+'_delta_field']=-initial*factor*cold/105
            fields[title+'_delta_field_prime']=6*fields[title+'_delta_field']/tau
        path=folder/('two-mode-seed-'+str(wave)+'.npz')
        np.savez_compressed(path,axis_phase=axis,curvature_zeta=zeta,curvature_scalar=curvature,curvature_tracefree_mixed=tracefree,
            spatial_metric_covariant=metric,extrinsic_curvature_mixed=extrinsic,log_volume_perturbation=volume,
            cold_contrast=cold,baryon_contrast=cold,radiation_contrast=radiation,
            neutrino_stress_mixed_over_background_density=neutrino_stress,
            photon_covariant_conformal_velocity=photon_velocity,neutrino_covariant_conformal_velocity=neutrino_velocity,
            scale=scale,radiation_limit_conformal_time=tau,native_conformal_time=float(native['times'][0]),
            H_rad_Mpc_inverse=hubble,beta_Mpc_inverse=beta,neutrino_fraction=fraction,
            k_base_Mpc_inverse=wave,curvature_amplitude=amplitude,primordial_zeta_second=0.,**fields)
        minimum=float(np.linalg.eigvalsh(identity+metric_correction).min())
        trace_error=float(np.max(abs(np.trace(tracefree,axis1=-2,axis2=-1))))/max(float(np.max(abs(tracefree))),1e-30)
        row=dict(path=str(path),k_base_Mpc_inverse=wave,maximum_input_k_tau=math.sqrt(2)*wave*tau,
            maximum_quadratic_output_k_tau=2*math.sqrt(2)*wave*tau,
            minimum_spatial_metric_factor=minimum,relative_tracefree_error=trace_error,
            max_cold_contrast=float(np.max(abs(cold))),
            intrinsic_curvature_coordinate_mean=float(np.mean(curvature)),
            radiation_limit_time_offset_fraction=tau/float(native['times'][0])-1)
        rows.append(row)
        for name,passed in [('positive spatial metric',minimum>0),('tracefree curvature',trace_error<1e-12),
            ('superhorizon input modes',row['maximum_input_k_tau']<.1),
            ('adiabatic radiation ratio',np.allclose(radiation,4*cold/3,rtol=1e-14,atol=0))]:
            checks.append(dict(name=name+' k='+str(wave),passed=bool(passed)))
    assert all(row['passed'] for row in checks)
    finish(folder,dict(rows=rows,checks=checks,all_checks_passed=True,count=len(checks),
        frame='Conformal seed chart, cold-comoving synchronous time; not a complete second-order native solver state',
        fields_in_reduced_Planck_units=True,gravity_units='H, curvature and K in Mpc units; radiation normalization implicit 8piG rho_r=3H_rad^2',
        order='Second spatial-gradient order, velocity third-gradient order; leading frozen-field expansion',
        primordial_zeta_second_chosen_zero=True,background_clock_difference_recorded=True),
        __file__,[BACKGROUND,ROOT/'results/native-seed-valid/heavy.npz',*folder.glob('*.npz')])
    print(json.dumps(dict(state='complete',seed_packets=len(rows),self_checks=len(checks),
        max_input_k_tau=max(row['maximum_input_k_tau'] for row in rows))))


if __name__=='__main__':
    main()
