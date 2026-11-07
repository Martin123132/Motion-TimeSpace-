from __future__ import annotations

from window_common import *


def convolved_basis(poles,operator):
    base=np.array([operator@row[:3].reshape(-1) for row in poles])
    noise=np.zeros(1200);noise[:400]=1.
    return np.vstack([base,operator@noise])


def main():
    modest()
    folder=ROOT/'results/response'
    folder.mkdir(parents=True,exist_ok=False)
    reports=[]
    for label in ['heavy','cold','lcdm']:
        geom=geometry(label)
        poles=multipole_basis(label)
        pchip=multipole_basis(label,method='pchip')
        angular=multipole_basis(label,nmu=32)
        identity=multipole_basis(label,identity=True)
        density_fn,velocity_fn=transfer(label)
        wave=HUNIT*KIN
        density=np.exp(density_fn(np.log(wave)));velocity=np.exp(velocity_fn(np.log(wave)))
        power=2*math.pi**2/wave**3*previous.previous.AS*(wave/.05)**(previous.previous.NS-1)*HUNIT**3
        zero=np.zeros_like(power)
        analytic=np.array([[power*density**2,zero,zero],
            [2/3*power*density*velocity,4/3*power*density*velocity,zero],
            [power*velocity**2/5,4/7*power*velocity**2,8/35*power*velocity**2]])
        scale=max(abs(analytic.flatten()))
        kaiser_error=float(np.max(abs(identity[:,:3]-analytic))/scale)
        assert kaiser_error<1e-12
        reports.append(dict(branch=label,geometry=geom,identity_kaiser_error=kaiser_error))
        for cap in ['NGC','SGC']:
            survey=np.load(ROOT/'results/prepared'/(cap+'.npz'))
            operator=survey['operator']
            response=convolved_basis(poles,operator)
            tail=poles.copy();tail[:,:,KIN<=.2]=0.
            tail_response=convolved_basis(tail,operator);tail_response[3]=0.
            plain=np.zeros((4,200))
            for term in range(3):
                for place,ell in enumerate([0,2,4]):
                    plain[term,ell*40:(ell+1)*40]=interpolate.CubicSpline(KIN,poles[term,place])(survey['k_effective'])
            plain[3,:40]=1.
            np.savez_compressed(folder/(label+'-'+cap+'.npz'),basis=response,poles=poles,
                pchip_basis=convolved_basis(pchip,operator),angular32_basis=convolved_basis(angular,operator),
                identity_basis=convolved_basis(identity,operator),tail_basis=tail_response,no_window_basis=plain)
    finish(folder,dict(branches=reports,model='Linear cb density and velocity, AP remapping, ell0/2/4, released leading wide-angle and window.',
        shot_noise_policy='Free constant pre-window monopole residual; no extra subtraction of header noise.',
        units=dict(k='h/Mpc',power='(Mpc/h)^3'),galaxy_velocity_assumption='cb tracer velocity without extra velocity bias'),
        __file__,[ROOT/'results/prepared/status.json',*sorted((ROOT/'results/prepared').glob('*.npz')),
            *[PARENT/'results/spectrum'/(label+'.npz') for label in ['heavy','cold','lcdm']],
            *[PARENT/'runs'/label/'background.npz' for label in ['heavy','cold','lcdm']],*folder.glob('*.npz')])
    print(json.dumps(reports,indent=2))


if __name__=='__main__':
    main()
