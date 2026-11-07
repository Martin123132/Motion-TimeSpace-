from __future__ import annotations

from vertex_common import *


def main():
    modest()
    folder=ROOT/'results/fourier'
    folder.mkdir(parents=True,exist_ok=False)
    size=16
    coordinate=np.stack(np.meshgrid(*([np.arange(size)*2*np.pi/size]*3),indexing='ij'),axis=-1)
    momentum_p=np.array([1.,0.,1.])
    momentum_q=np.array([0.,1.,1.])
    hp=np.array([[.3,.04,.06],[.04,-.15,.02],[.06,.02,.1]])
    hq=np.array([[-.1,.03,-.02],[.03,.25,.05],[-.02,.05,.12]])
    hpt=hp*.2
    hqt=hq*-.1
    up,uq,vp,vq=.47,.26,.13,-.07
    scale,mass=.73,.8
    phase_p=coordinate@momentum_p
    phase_q=coordinate@momentum_q
    cos_p,cos_q=np.cos(phase_p),np.cos(phase_q)
    sin_p,sin_q=np.sin(phase_p),np.sin(phase_q)
    field=up*cos_p+uq*cos_q
    velocity=vp*cos_p+vq*cos_q
    gradient=-up*sin_p[...,None]*momentum_p-uq*sin_q[...,None]*momentum_q
    hessian=-up*cos_p[...,None,None]*np.outer(momentum_p,momentum_p)-uq*cos_q[...,None,None]*np.outer(momentum_q,momentum_q)
    metric1=cos_p[...,None,None]*hp+cos_q[...,None,None]*hq
    metric_rate=cos_p[...,None,None]*hpt+cos_q[...,None,None]*hqt
    metric_divergence=-sin_p[...,None]*(momentum_p@hp)-sin_q[...,None]*(momentum_q@hq)
    theta_gradient=-(np.trace(hp)*sin_p[...,None]*momentum_p+np.trace(hq)*sin_q[...,None]*momentum_q)/2
    theta_rate=np.trace(metric_rate,axis1=-2,axis2=-1)/2
    kg=-theta_rate*velocity-np.einsum('...ij,...ij->...',metric1,hessian)-np.einsum('...j,...j->...',metric_divergence-theta_gradient,gradient)
    gradient_norm=np.sum(gradient**2,axis=-1)
    energy=(velocity**2+gradient_norm)/(2*scale**2)+mass**2*field**2/2
    pressure=(velocity**2-gradient_norm/3)/(2*scale**2)-mass**2*field**2/2
    current=-velocity[...,None]*gradient/scale
    anisotropy=(gradient[...,None]*gradient[...,None,:]-np.eye(3)*gradient_norm[...,None,None]/3)/scale**2
    geometric=-np.einsum('...ij,...ji->...',metric_rate,metric_rate)/4
    canonical=-velocity**2+scale**2*mass**2*field**2/2
    maps=dict(KG_total=kg,E_quadratic=energy,P_quadratic=pressure,
        j_quadratic_imaginary=current,anisotropic_stress=anisotropy,
        Einstein_volume_geometric=geometric,Einstein_volume_canonical=canonical)
    def bundle(spatial,rate):
        return np.array([np.trace(spatial)/2]),np.array([np.trace(rate)/2]),spatial[None],(rate-np.eye(3)*np.trace(rate)/3)[None]
    first=bundle(hp,hpt)
    second=bundle(hq,hqt)
    cases=[('sum',momentum_p,momentum_q,first,second,up,uq,vp,vq,.5),
        ('difference',momentum_p,-momentum_q,first,second,up,uq,vp,vq,.5),
        ('self_p',momentum_p,momentum_p,first,first,up,up,vp,vp,.25),
        ('self_q',momentum_q,momentum_q,second,second,uq,uq,vq,vq,.25)]
    transforms={key:np.fft.fftn(value,axes=(0,1,2))/size**3 for key,value in maps.items()}
    checks=[]
    for label,first_k,second_k,first_metric,second_metric,first_field,second_field,first_prime,second_prime,factor in cases:
        expected=vertices(first_k,second_k,first_metric,second_metric,np.array([first_field]),np.array([second_field]),np.array([first_prime]),np.array([second_prime]),np.array([scale]),mass)
        index=tuple(((first_k+second_k).astype(int)%size).tolist())
        for key in maps:
            predicted=expected[key][0]*factor*(1j if key=='j_quadratic_imaginary' else 1)
            actual=transforms[key][index]
            error=float(np.max(abs(predicted-actual)))
            checks.append(dict(name=label+': '+key,passed=bool(error<1e-13),max_absolute_error=error))
    zero_expected={key:np.zeros_like(value[0,0,0]) for key,value in maps.items()}
    for mode,geometry,field_value,prime_value in [(momentum_p,first,up,vp),(momentum_q,second,uq,vq)]:
        result=vertices(mode,-mode,geometry,geometry,np.array([field_value]),np.array([field_value]),np.array([prime_value]),np.array([prime_value]),np.array([scale]),mass)
        for key in maps:
            zero_expected[key]=zero_expected[key]+result[key][0]/2*(1j if key=='j_quadratic_imaginary' else 1)
    for key in maps:
        error=float(np.max(abs(zero_expected[key]-transforms[key][0,0,0])))
        checks.append(dict(name='Homogeneous source retained: '+key,passed=bool(error<1e-13),max_absolute_error=error))
    assert all(check['passed'] for check in checks),checks
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=True,
        independent_position_space_product=True,normalization='complex FFT; two distinct real cosines: V/2 at +K; self: V/4 at +2p; folded mean: V/2',
        maximum_absolute_error=max(check['max_absolute_error'] for check in checks)),__file__)
    print(json.dumps(dict(checks=len(checks),max_error=max(check['max_absolute_error'] for check in checks))),flush=True)


if __name__=='__main__':
    main()
