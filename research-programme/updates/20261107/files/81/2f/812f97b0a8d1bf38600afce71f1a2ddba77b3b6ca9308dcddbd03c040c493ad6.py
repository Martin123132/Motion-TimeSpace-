from __future__ import annotations

import sympy as symbolic
from collision_common import *


def main():
    modest()
    folder=ROOT/'results/relaxation'
    folder.mkdir(parents=True,exist_ok=False)
    projectors=CollisionProjectors(24,32)
    directions,weights,screen=projectors.directions,projectors.weights,projectors.screen
    checks=[]
    def check(name,passed,**details):
        checks.append(dict(name=name,passed=bool(passed),**details))
        assert passed,(name,details)
    matrix=np.array([[1.,.12+.1j,.04],[.12-.1j,.9,.02],[.04,.02,.8]],complex)
    intensity=(1+.2*directions[:,2])[:,None,None]*(screen@matrix@screen)
    mean=mean_matrix(weights,intensity)
    gain=1.5*(screen@mean@screen)
    mean_gain=mean_matrix(weights,gain)
    expected=(7*(mean+mean.T)/2+5*(mean-mean.T)/2+np.eye(3)*np.trace(mean))/10
    check('Polarized mean collision eigenvalues from sphere integration',np.max(abs(mean_gain-expected))<2e-13)
    for depth in [.001,.1,1.,1000.]:
        mean_iso=np.eye(3)*np.trace(mean)/3
        mean_tf=(mean+mean.T)/2-mean_iso
        mean_anti=(mean-mean.T)/2
        propagator=np.exp(-depth)*intensity+1.5*(screen@((1-np.exp(-depth))*mean_iso+
            (np.exp(-.3*depth)-np.exp(-depth))/.7*mean_tf+2*(np.exp(-.5*depth)-np.exp(-depth))*mean_anti)@screen)
        check('Rest-frame physical polarization stays positive '+str(depth),np.min(np.linalg.eigvalsh(propagator))>-2e-13)
        check('Rest scattering conserves photon energy '+str(depth),abs(np.trace(mean_matrix(weights,propagator))-np.trace(mean))<2e-13)
    radiation=.5*screen+(.07*directions[:,2])[:,None,None]*screen+.03*(screen@np.diag([1.,-1.,0.])@screen)
    baryon=np.array([.02,-.01,.04],complex)
    ratio=.4
    before=radiation_stress(directions,weights,radiation)[0,1:]+4*ratio*baryon/3
    for depth in [0.,.001,1.,1000.]:
        evolved,velocity=projectors.apply(radiation,baryon,ratio,depth)
        after=radiation_stress(directions,weights,evolved)[0,1:]+4*ratio*velocity/3
        check('Coupled photon/baryon momentum conserved '+str(depth),np.max(abs(after-before))<2e-13)
        stepped,stepped_velocity=projectors.apply(*projectors.apply(radiation,baryon,ratio,depth/2),ratio,depth/2)
        check('Frozen collision semigroup composition '+str(depth),np.max(abs(evolved-stepped))<2e-13 and np.max(abs(velocity-stepped_velocity))<2e-13)
    mu=directions[:,2]
    source=-2*(mu**2-1/3)[:,None,None]*screen
    parts,_,_=projectors.parts(source,np.zeros(3),ratio)
    steady=parts[1]+parts[2]/.3+parts[3]/.5
    quadrupole=-(weights*(3*mu**2-1)/2)@np.trace(steady,axis1=1,axis2=2)
    check('Tight-coupling quadrupole32/45 derived from polarized inverse operator',abs(quadrupole-32/45)<2e-13,coefficient=float(quadrupole.real))
    collision_rate,photon_enthalpy,baryon_density,velocity_b,velocity_gamma=symbolic.symbols('kappa w rho_b vb vg',positive=True)
    acceleration=collision_rate*photon_enthalpy*(velocity_gamma-velocity_b)/baryon_density
    power=collision_rate*velocity_b*photon_enthalpy*(velocity_gamma-velocity_b)
    check('Baryon kinetic work equals second-order radiation energy transfer',symbolic.simplify(baryon_density*velocity_b*acceleration-power)==0)
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=True,
        eigenvalues_per_opacity=[0,-1,-.3,-.5],coupled_relative_velocity_eigenvalue='-(1+1/R)',
        photon_quadrupole_coefficient=float(quadrupole.real),frozen_coefficients_exact=True),__file__)
    print(json.dumps(dict(checks=len(checks),quadrupole_coefficient=float(quadrupole.real))),flush=True)


if __name__=='__main__':
    main()
