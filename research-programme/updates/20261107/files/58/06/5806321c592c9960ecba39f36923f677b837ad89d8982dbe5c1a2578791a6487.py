from __future__ import annotations

from velocity_common import *


def moments(label,nodes=16385,method='cubic',upper=5.):
    density_fn,velocity_fn=previous.transfer(label,method)
    logarithm=np.linspace(math.log(1e-5),math.log(upper),nodes)
    wave=np.exp(logarithm)
    velocity=np.exp(velocity_fn(logarithm))
    primordial=2*math.pi**2/wave**3*previous.previous.previous.AS*(wave/.05)**(previous.previous.previous.NS-1)
    velocity_power=primordial*velocity**2
    variance=HUNIT**2/(6*math.pi**2)*integrate.simpson(wave*velocity_power,x=logarithm)
    rows=[]
    for separation in [0.,10.,30.,50.,100.,150.,200.]:
        phase=wave*separation/HUNIT
        monopole=special.spherical_jn(0,phase)
        quadrupole=special.spherical_jn(2,phase)
        for direction_cosine in [0.,1.]:
            kernel=1-monopole+2*special.eval_legendre(2,direction_cosine)*quadrupole
            pair=HUNIT**2/(3*math.pi**2)*integrate.simpson(wave*velocity_power*kernel,x=logarithm)
            rows.append(dict(separation_Mpc_over_h=separation,LOS_cosine=direction_cosine,
                pairwise_variance_Mpc_over_h_squared=float(pair)))
    return dict(one_point_variance_Mpc_over_h_squared=float(variance),
        one_point_rms_Mpc_over_h=math.sqrt(variance),pairwise=rows,upper_k_Mpc_inverse=upper)


def main():
    modest()
    folder=ROOT/'results/derived-moments'
    folder.mkdir(parents=True,exist_ok=False)
    rows=[]
    for label in ['heavy','cold','lcdm']:
        central=moments(label)
        resolution=moments(label,nodes=8193)
        pchip=moments(label,method='pchip')
        cuts={str(upper):moments(label,upper=upper)['one_point_variance_Mpc_over_h_squared'] for upper in [.2,.5,1.,3.]}
        scale=central['one_point_variance_Mpc_over_h_squared']
        changes={}
        for name,variant in [('resolution',resolution),('pchip',pchip)]:
            changes[name]=max(abs(variant['one_point_variance_Mpc_over_h_squared']/scale-1),
                max(abs(other['pairwise_variance_Mpc_over_h_squared']-base['pairwise_variance_Mpc_over_h_squared'])/scale
                    for base,other in zip(central['pairwise'],variant['pairwise'])))
        rows.append(dict(branch=label,central=central,cutoff_variances=cuts,mode_variance_normalized_changes=changes,
            parent_linear_prediction=True,equal_to_fitted_residual_variance=False))
    cosine,weights=np.polynomial.legendre.leggauss(96)
    checks=[]
    for argument in [.001,.1,1.,5.,20.]:
        for direction in [0.,1.]:
            angular_factor=cosine**2 if direction==1. else (1-cosine**2)/2
            angular=1.5*np.sum(weights*angular_factor*(1-np.cos(argument*cosine)))
            bessel=1-special.spherical_jn(0,argument)+2*special.eval_legendre(2,direction)*special.spherical_jn(2,argument)
            checks.append(dict(argument=argument,LOS_cosine=direction,error=float(abs(angular-bessel))))
    finish(folder,dict(branches=rows,angular_Bessel_identity=checks,
        definition='Unweighted coherent cb linear displacement covariance derived from the retained velocity transfer, finite1e-5..5 Mpc^-1.',
        not_density_weighted_pair_distribution=True,not_residual_galaxy_velocity_calibration=True),
        __file__,[*[SPECTRUM/'results/spectrum'/(label+'.npz') for label in ['heavy','cold','lcdm']]])
    print(json.dumps(rows,indent=2))


if __name__=='__main__':
    main()
