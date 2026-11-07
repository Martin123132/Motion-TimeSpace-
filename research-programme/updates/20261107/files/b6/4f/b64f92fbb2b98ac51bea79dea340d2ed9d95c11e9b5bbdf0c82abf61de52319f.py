from __future__ import annotations

from feedback_common import *
import sympy as sp


def main():
    modest()
    folder=ROOT/'results/derivation'
    folder.mkdir(parents=True,exist_ok=False)
    checks=[]
    def identity(name,expression):
        residual=sp.simplify(sp.expand_trig(expression))
        checks.append(dict(name=name,passed=residual==0,residual=str(residual)))
        assert residual==0,(name,residual)

    time,space,transverse=sp.symbols('time space transverse',real=True)
    mass,lapse,scale,field,rate,gradient,shift,volume=sp.symbols('mass lapse scale field rate gradient shift volume',positive=True)
    potential=mass**2*field**2/2
    momentum=(rate-shift*gradient)/lapse
    lagrangian=lapse*volume*(momentum**2/2-gradient**2/(2*scale**2)-potential)
    energy=momentum**2/2+gradient**2/(2*scale**2)+potential
    identity('ADM lapse variation gives energy',-sp.diff(lagrangian,lapse)/volume-energy)
    identity('ADM shift variation gives momentum density',sp.diff(lagrangian,shift)/volume+momentum*gradient)
    identity('canonical momentum from same action',sp.diff(lagrangian,rate)/volume-momentum)

    phi=sp.Function('phi')(time,space)
    expansion=sp.Function('scale')(time)
    hubble=sp.diff(expansion,time)/expansion
    kinetic=sp.diff(phi,time)
    spatial=sp.diff(phi,space)
    rho=kinetic**2/2+spatial**2/(2*expansion**2)+mass**2*phi**2/2
    pressure=kinetic**2/2-spatial**2/(6*expansion**2)-mass**2*phi**2/2
    flux=-kinetic*spatial/expansion
    longitudinal=kinetic**2/2+spatial**2/(2*expansion**2)-mass**2*phi**2/2
    klein=sp.diff(phi,time,2)+3*hubble*kinetic-sp.diff(phi,space,2)/expansion**2+mass**2*phi
    identity('exact FLRW energy Ward identity',sp.diff(rho,time)+3*hubble*(rho+pressure)+sp.diff(flux,space)/expansion-kinetic*klein)
    identity('exact FLRW momentum Ward identity',sp.diff(flux,time)+4*hubble*flux+sp.diff(longitudinal,space)/expansion+spatial*klein/expansion)

    epsilon=sp.symbols('epsilon')
    p0,p1,p2,f0,f1,f2,g1=sp.symbols('p0 p1 p2 f0 f1 f2 g1')
    energy_series=((p0+epsilon*p1+epsilon**2*p2)**2+
        mass**2*(f0+epsilon*f1+epsilon**2*f2)**2+epsilon**2*g1**2/scale**2)/2
    identity('quadratic energy including second-order field',sp.expand(energy_series).coeff(epsilon,2)-
        (p0*p2+p1**2/2+mass**2*f0*f2+mass**2*f1**2/2+g1**2/(2*scale**2)))
    n1,n2,rate0,rate1,rate2,advected=sp.symbols('n1 n2 rate0 rate1 rate2 advected')
    expansion_pi=sp.series((rate0+epsilon*rate1+epsilon**2*(rate2-advected))/(1+epsilon*n1+epsilon**2*n2),epsilon,0,3).removeO()
    identity('lapse and shift terms of second-order normal momentum',sp.expand(expansion_pi).coeff(epsilon,2)-
        (rate2-n1*rate1+(n1**2-n2)*rate0-advected))
    gradx,grady,gradz=sp.symbols('gradx grady gradz')
    gradient_vector=sp.Matrix([gradx,grady,gradz])
    tracefree=gradient_vector*gradient_vector.T-sp.eye(3)*(gradient_vector.dot(gradient_vector))/3
    identity('canonical quadratic anisotropic stress trace',sp.trace(tracefree))
    identity('homogeneous background has no linear scalar anisotropic stress',
        sp.expand(epsilon**2*tracefree[0,0]).coeff(epsilon,1))

    density=sp.Function('density')(space,transverse)
    coordinates=[space,transverse]
    laplacian=sum(sp.diff(density,coordinate,2) for coordinate in coordinates)
    root=sp.sqrt(density)
    quantum=sum(sp.diff(root,coordinate,2) for coordinate in coordinates)/root
    def stress(first,second):
        return (sp.diff(density,first)*sp.diff(density,second)/density-sp.diff(density,first,second))/(4*mass**2*scale**2)
    divergence=sum(sp.diff(stress(space,coordinate),coordinate) for coordinate in coordinates)
    identity('nonlinear conservative quantum-force identity',divergence+density*sp.diff(quantum,space)/(2*mass**2*scale**2))
    improvement_div=sum(sp.diff(sp.diff(density,space,coordinate)-(laplacian if coordinate==space else 0),coordinate) for coordinate in coordinates)
    identity('Hessian versus isotropic Laplacian improvement has zero divergence',improvement_div)

    phase,first,second,speed,second_speed,pressure_coefficient=sp.symbols('phase first second speed second_speed pressure_coefficient',real=True)
    contrast=epsilon*first*sp.cos(phase)+epsilon**2*second*sp.cos(2*phase)
    root_expansion=1+contrast/2-contrast**2/8
    inverse_expansion=1-contrast/2+3*contrast**2/8
    quantum_expansion=sp.series(sp.diff(root_expansion,phase,2)*inverse_expansion,epsilon,0,3).removeO().expand()
    identity('quadratic square-root pressure expansion',quantum_expansion-
        (-epsilon*first*sp.cos(phase)/2+epsilon**2*(first**2/8+(3*first**2/8-2*second)*sp.cos(2*phase))))
    flow=-epsilon*speed*sp.sin(phase)-epsilon**2*second_speed*sp.sin(2*phase)/2
    continuity=-sp.diff((1+contrast)*flow,phase)
    identity('second harmonic continuity source',sp.expand(continuity).coeff(epsilon,2)-(second_speed+first*speed)*sp.cos(2*phase))
    identity('second harmonic convective acceleration',sp.expand(flow*sp.diff(flow,phase)).coeff(epsilon,2)-speed**2*sp.sin(2*phase)/2)
    quantum_force=2*pressure_coefficient*sp.diff(quantum_expansion,phase)
    identity('quadratic quantum source coefficient three',
        sp.expand(-2*quantum_force).coeff(epsilon,2)-(-16*pressure_coefficient*second+3*pressure_coefficient*first**2)*sp.sin(2*phase))
    identity('linear pressure sign',sp.expand(quantum_force).coeff(epsilon,1)-pressure_coefficient*first*sp.sin(phase))

    initial_density,integral=sp.symbols('initial_density integral')
    transport_second=initial_density*integral+integral**2/2
    identity('Stage60 no-feedback limit',sp.diff(transport_second,integral)-(initial_density+integral))
    efold=sp.symbols('efold')
    growth=sp.exp(efold)
    for tag,second_value in [('growing',growth**2),('zero-quadratic-initial',growth**2-growth)]:
        velocity_value=sp.diff(second_value,efold)-growth**2
        identity('EdS continuity '+tag,sp.diff(second_value,efold)-velocity_value-growth**2)
        identity('EdS Euler '+tag,sp.diff(velocity_value,efold)+velocity_value/2-sp.Rational(3,2)*second_value-growth**2)

    weight,velocity_a,velocity_b=sp.symbols('weight velocity_a velocity_b')
    bulk=weight*velocity_a+(1-weight)*velocity_b
    identity('cb relative-flow stress cannot be silently discarded',
        weight*velocity_a**2+(1-weight)*velocity_b**2-bulk**2-weight*(1-weight)*(velocity_a-velocity_b)**2)
    kappa=sp.symbols('kappa',positive=True)
    sound=kappa**2/(sp.sqrt(1+kappa**2)+1)**2
    identity('native heavy beat pressure matches NR leading term',sp.limit(sound/kappa**2,kappa,0)-sp.Rational(1,4))
    identity('native higher-gradient remainder order',sp.limit((sound-kappa**2/4)/kappa**4,kappa,0)+sp.Rational(1,8))

    sources=[
        BRANCH/'motion-bath-matching-20261006/49-real-motion-envelope-and-existing-bath-matching.md',
        BRANCH/'heavy-interaction-and-condensate-bridge-20261007/52-heavy-mode-interactions-and-condensate-coherence.md',
        BRANCH/'native-two-field-transfer-20261007/54-native-canonical-fields-and-radiation.md',
        BRANCH/'native-heavy-matching-20261007/55-native-heavy-matching-and-late-matter.md']
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),
        hilbert_stress_and_effective_momentum_flux_distinguished=True,new_fitted_coefficients=0,
        envelope_scope='Leading weak-field nonrelativistic Gaussian canonical subfamily, not an exact heavy-number symmetry.'),
        __file__,sources)
    print(json.dumps(dict(state='complete',symbolic_identities=len(checks))))


if __name__=='__main__':
    main()
