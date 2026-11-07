from thermal_common import *


def moments(frequency,quadrature,occupation):
    return float(np.sum(quadrature*frequency**3*occupation)),float(np.sum(quadrature*frequency**4*occupation*(1+occupation)))


def heat_jet(frequency,quadrature,zeroth,left,right,second,ratios,densities):
    ratio0,ratio_p,ratio_q,ratio2=ratios
    density_p,density_q,density2=densities
    energy0,recoil0=moments(frequency,quadrature,zeroth)
    energy_p=np.sum(quadrature*frequency**3*left)
    energy_q=np.sum(quadrature*frequency**3*right)
    energy2=np.sum(quadrature*frequency**3*second)
    recoil_p=np.sum(quadrature*frequency**4*(1+2*zeroth)*left)
    recoil_q=np.sum(quadrature*frequency**4*(1+2*zeroth)*right)
    recoil2=np.sum(quadrature*frequency**4*((1+2*zeroth)*second+left*right))
    heat0=4*ratio0*energy0-recoil0
    bare_p=4*ratio0*energy_p+4*ratio_p*energy0-recoil_p
    bare_q=4*ratio0*energy_q+4*ratio_q*energy0-recoil_q
    heat_p=bare_p+density_p*heat0
    heat_q=bare_q+density_q*heat0
    heat2=(4*ratio0*energy2+4*ratio2*energy0+2*(ratio_p*energy_q+ratio_q*energy_p)-recoil2+
        (density_p*bare_q+density_q*bare_p)/2+density2*heat0)
    return np.array([heat0,heat_p,heat_q,heat2])


def conformal_force_jet(heats,velocity_p,velocity_q,velocity2):
    heat0,heat_p,heat_q,heat2=heats
    zeroth=np.r_[heat0,np.zeros(3)]
    left=np.r_[heat_p,heat0*velocity_p]
    right=np.r_[heat_q,heat0*velocity_q]
    second=np.r_[heat2+heat0*(velocity_p@velocity_q)/2,heat0*velocity2+(heat_p*velocity_q+heat_q*velocity_p)/2]
    return np.array([zeroth,left,right,second])


def main():
    modest()
    folder=ROOT/'results/source-jet'
    folder.mkdir(parents=True,exist_ok=False)
    nodes,weights=np.polynomial.legendre.leggauss(400)
    frequency=30*(nodes+1)
    quadrature=30*weights
    zeroth=planck(frequency)
    left=weight(frequency)*(.03*frequency+.002*frequency**2)
    right=weight(frequency)*(-.02*frequency+.003*frequency**2)
    second=weight(frequency)*(.004*frequency+.001*frequency**2)
    ratios=[1.01,.03,-.02,.004]
    densities=[.02,-.03,.007]
    velocity_p=np.array([.02,.01,-.005])
    velocity_q=np.array([-.01,.015,.007])
    velocity2=np.array([.001,-.002,.003])
    predicted=heat_jet(frequency,quadrature,zeroth,left,right,second,ratios,densities)
    force=conformal_force_jet(predicted,velocity_p,velocity_q,velocity2)
    def exact(first_amplitude,second_amplitude):
        occupation=zeroth+first_amplitude*left+second_amplitude*right+2*first_amplitude*second_amplitude*second
        ratio=ratios[0]+first_amplitude*ratios[1]+second_amplitude*ratios[2]+2*first_amplitude*second_amplitude*ratios[3]
        density=1+first_amplitude*densities[0]+second_amplitude*densities[1]+2*first_amplitude*second_amplitude*densities[2]
        velocity=first_amplitude*velocity_p+second_amplitude*velocity_q+2*first_amplitude*second_amplitude*velocity2
        energy,recoil=moments(frequency,quadrature,occupation)
        heat=density*(4*ratio*energy-recoil)
        return heat,heat*np.r_[1.,velocity]/math.sqrt(1-velocity@velocity)
    checks=[]
    rows=[]
    for amplitude in [.01,.005,.0025]:
        values=[exact(amplitude,amplitude),exact(amplitude,-amplitude),exact(-amplitude,amplitude),exact(-amplitude,-amplitude)]
        heat=(values[0][0]-values[1][0]-values[2][0]+values[3][0])/(8*amplitude**2)
        vector=(values[0][1]-values[1][1]-values[2][1]+values[3][1])/(8*amplitude**2)
        heat_error=float(abs(heat-predicted[3])/max(abs(predicted[3]),1e-100))
        force_error=float(np.linalg.norm(vector-force[3])/max(np.linalg.norm(force[3]),1e-100))
        checks.append(dict(name='Independent mixed thermal/opacity/four-force derivative '+str(amplitude),passed=max(heat_error,force_error)<1e-4,value=max(heat_error,force_error),gate=1e-4))
        rows.append(dict(amplitude=amplitude,heat_error=heat_error,force_error=force_error))
    checks.append(dict(name='Plasma uses the exact opposite four-force at every retained order',passed=bool(np.array_equal(force+(-force),np.zeros_like(force)))))
    equilibrium=heat_jet(frequency,quadrature,zeroth,np.zeros_like(zeroth),np.zeros_like(zeroth),np.zeros_like(zeroth),[1.,0.,0.,0.],densities)
    checks.append(dict(name='Density modulation cannot heat exact equilibrium',passed=bool(np.max(abs(equilibrium))<1e-10),value=float(np.max(abs(equilibrium)))))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),finite_difference_rows=rows,
        heat_coefficients=predicted,conformal_four_force_coefficients=force,
        heat_unit='Multiply by kappa0*theta_ref*rho_ref/I3_Planck to obtain conformal energy-transfer density',
        proper_four_force_requires_division_by_scale_factor=True,
        kernel_is_electron_rest_isotropic_spectral_projection=True,
        arbitrary_anisotropic_induced_scattering_not_included=True,
        existing_second_order_parent_kernel_not_silently_replaced=True),__file__)
    print(json.dumps(dict(checks=checks,rows=rows)),flush=True)


if __name__=='__main__':
    main()
