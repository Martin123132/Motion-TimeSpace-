from __future__ import annotations

from seed_common import *


def constraint_probe(amplitude,fraction,tau,count):
    phase,zeta,curvature,tracefree_x=planar_geometry(amplitude,count)
    response=1+4*fraction/15
    scale=tau
    hubble=1/tau**2
    volume=-tau**2*curvature/16
    metric_x=2*volume/3-tau**2*tracefree_x/(3*response)
    metric_y=2*volume/3+tau**2*tracefree_x/(6*response)
    longitudinal=scale**2*np.exp(2*zeta)*(1+metric_x)
    transverse=scale**2*np.exp(2*zeta)*(1+metric_y)
    curvature_exact=(-2*derivative(transverse,2)/(longitudinal*transverse)+
        derivative(longitudinal)*derivative(transverse)/(longitudinal**2*transverse)+
        derivative(transverse)**2/(2*longitudinal*transverse**2))
    delta_kx=-metric_x/(tau**2*(1+metric_x))
    delta_ky=-metric_y/(tau**2*(1+metric_y))
    volume_exact=.5*(np.log1p(metric_x)+2*np.log1p(metric_y))
    energy_perturbation=6*hubble**2*np.expm1(-4*volume_exact/3)
    expansion_perturbation=-4*hubble*(delta_kx+2*delta_ky)+4*delta_kx*delta_ky+2*delta_ky**2
    hamiltonian=curvature_exact+expansion_perturbation-energy_perturbation
    scale_h=float(np.max(abs(curvature_exact)+abs(expansion_perturbation)+abs(energy_perturbation)))
    connection=derivative(transverse)/(2*transverse)
    momentum_geometry=-2*derivative(delta_ky)+2*connection*(delta_kx-delta_ky)
    curvature_gradient=derivative(curvature)
    photon_velocity=-tau**3*curvature_gradient/144
    neutrino_velocity=photon_velocity*(1+8/(15*response))
    momentum_matter=4*hubble**2*scale*np.exp(-4*volume_exact/3)*((1-fraction)*photon_velocity+fraction*neutrino_velocity)
    scale_m=float(np.max(abs(momentum_geometry)+abs(momentum_matter)))
    momentum_residual=momentum_geometry-momentum_matter
    wrong_geometry=-2*derivative(delta_ky)
    mass=(np.exp(-volume_exact)*np.exp(volume_exact))
    return dict(amplitude=amplitude,neutrino_fraction=fraction,tau=tau,count=count,
        hamiltonian_relative=float(np.max(abs(hamiltonian))/scale_h),
        momentum_relative=float(np.max(abs(momentum_residual))/scale_m),
        wrong_flat_divergence_relative=float(np.max(abs(wrong_geometry-momentum_matter))/scale_m),
        min_spatial_metric_factor=float(min(np.min(1+metric_x),np.min(1+metric_y))),
        mass_jacobian_error=float(max(abs(mass-1))))


def main():
    modest()
    folder=ROOT/'results/geometry'
    folder.mkdir(parents=True,exist_ok=False)
    rows=[]
    for fraction in [0.,.4,.6]:
        for amplitude in [.01,.03]:
            for tau in [.08,.04,.02]:
                rows.append(constraint_probe(amplitude,fraction,tau,256))
            rows.append(constraint_probe(amplitude,fraction,.04,512))
    gauge=[]
    phase=np.linspace(0,2*math.pi,1024,endpoint=False)
    expected=(1-9*np.cos(2*phase))/16
    for amplitude in [.02,.01,.005]:
        values=[]
        for signed in [amplitude,-amplitude]:
            original=phase-3*signed*np.sin(phase)
            zeta=signed*np.cos(original)
            curvature=np.exp(-2*zeta)*(4*signed*np.cos(original)-2*signed**2*np.sin(original)**2)
            values.append(curvature/16)
        coefficient=(values[0]+values[1])/(2*amplitude**2)
        wrong=-(5+3*np.cos(2*phase))/16
        gauge.append(dict(amplitude=amplitude,
            correct_pullback_error=float(np.max(abs(coefficient-expected))),
            omitted_pullback_error=float(np.max(abs(coefficient-wrong)))))
    finish(folder,dict(rows=rows,gauge_pullback=gauge,
        constraint_scope='Exact geometry of a truncated gradient seed; residual tests omitted fourth/fifth spatial-gradient order, not full cosmological evolution.'),
        __file__)
    print(json.dumps(dict(state='complete',rows=len(rows),smallest_time=[row for row in rows if row['tau']==.02],gauge=gauge),indent=2))


if __name__=='__main__':
    main()
