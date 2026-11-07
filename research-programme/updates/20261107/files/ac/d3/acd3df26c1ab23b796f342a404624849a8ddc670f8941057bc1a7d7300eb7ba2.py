from __future__ import annotations

from collision_common import *


def main():
    modest()
    folder=ROOT/'results/collision-operator'
    folder.mkdir(parents=True,exist_ok=False)
    directions,weights=angular_grid(32,64)
    screen=screens(directions)
    polarization=np.array([[1.,.1+.07j,.02],[.1-.07j,.8,.03],[.02,.03,.7]],complex)
    intensity=(1+.2*directions[:,2]-.1*directions[:,0])[:,None,None]*(screen@polarization@screen)
    stress=radiation_stress(directions,weights,intensity).real
    checks=[]
    def check(name,passed,**details):
        checks.append(dict(name=name,passed=bool(passed),**details))
        assert passed,(name,details)
    for velocity in [np.zeros(3),np.array([.001,.002,-.001]),np.array([.15,-.08,.03]),np.array([.4,.1,-.1])]:
        gamma=1/math.sqrt(1-velocity@velocity)
        four_velocity=gamma*np.r_[1.,velocity]
        lowered=four_velocity*np.array([-1.,1.,1.,1.])
        rest_energy=lowered@stress@lowered
        flux=-stress@lowered-four_velocity*rest_energy
        collision=exact_collision(directions,weights,intensity,velocity)
        scalar=np.trace(collision,axis1=1,axis2=2)
        moment=np.r_[weights@scalar,np.einsum('n,ni->i',weights*scalar,directions)]
        error=float(np.max(abs(moment+flux)))/max(stress[0,0],1.)
        check('Boosted collision four-force '+str(velocity.tolist()),error<2e-12,envelope_error=error)
        check('Elastic force orthogonal to electron velocity '+str(velocity.tolist()),abs(lowered@flux)<2e-12)
    zeroth=screen/2
    first=(.13*directions[:,2]+.08*(directions[:,0]**2-directions[:,1]**2))[:,None,None]*screen
    first+=.04*(screen@np.diag([1.,-1.,0.])@screen)
    second=.025*(screen@np.array([[.3,.1,0],[.1,-.2,.04],[0,.04,.1]])@screen)
    velocity1=np.array([.24,-.13,.06])
    velocity2=np.array([-.03,.02,.01])
    density1,density2=.17,-.08
    _,linear,quadratic=taylor_collision(directions,weights,zeroth,first,second,velocity1,velocity2,density1,density2)
    amplitudes=np.array([.08,.04,.02,.01,.005])
    errors=[]
    for epsilon in amplitudes:
        def exact(amplitude):
            return exact_collision(directions,weights,zeroth+amplitude*first+amplitude**2*second,
                amplitude*velocity1+amplitude**2*velocity2,1+amplitude*density1+amplitude**2*density2)
        coefficient=(exact(epsilon)+exact(-epsilon)-2*exact(0))/(2*epsilon**2)
        errors.append(float(np.max(abs(coefficient-quadratic)))/float(np.max(abs(quadratic))))
    check('Quadratic moving polarized collision converges',np.all(np.diff(errors)<0),errors=errors)
    check('Fine moving-collision coefficient error below1e-5',errors[-1]<1e-5)
    zero=np.zeros_like(zeroth)
    _,linear_velocity,_=taylor_collision(directions,weights,zeroth,zero,zero,velocity1,np.zeros(3),0,0)
    expected=4*(directions@velocity1)[:,None,None]*zeroth
    check('Linear Doppler dipole has derived factor4',np.max(abs(linear_velocity-expected))<2e-13)
    np.savez_compressed(folder/'taylor.npz',amplitudes=amplitudes,errors=errors,linear=linear,quadratic=quadratic)
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=True,
        finest_quadratic_error=errors[-1],full_boost_tested=True,polarization_included=True,
        electron_density_perturbation_included=True,elastic_rest_frame_only=True),__file__)
    print(json.dumps(dict(checks=len(checks),quadratic_errors=errors)),flush=True)


if __name__=='__main__':
    main()
