import numpy as np


def mean_coefficient(scale,omega,hubble,wave,mu,background,amplitude,metric):
    gamma=wave**2/(2*omega*hubble)
    coupling=wave/(2*hubble)
    return 1j/(2*mu)*((2.25+gamma**2+3*omega*abs(background)**2/(8*scale**2*hubble**2))*amplitude+
                     coupling*metric*(3-1j*gamma)*background+
                     3*omega*background**2*np.conjugate(amplitude)/(16*scale**2*hubble**2))


def harmonics(scale,omega,hubble,wave,mu,background,amplitude,metric,hzero,zzero):
    gamma=wave**2/(2*omega*hubble)
    coupling=wave/(2*hubble)
    coefficient=(1.5-1j*gamma)*np.conjugate(amplitude)+coupling*metric*np.conjugate(background)
    hplus=omega*np.conjugate(background)**2/(8*scale**2*hubble**2)
    zplus=3*omega*np.conjugate(background)*np.conjugate(amplitude)/(4*wave*hubble*scale**2)
    middle=(1j*gamma*np.conjugate(amplitude)+(1.5-1j*gamma)*(1j*gamma*np.conjugate(amplitude)-coupling*metric*np.conjugate(background))+
            coupling*zzero*np.conjugate(background)-coefficient+1.5*hzero*np.conjugate(amplitude))
    upper=coupling*zplus*np.conjugate(background)+1.5*hplus*np.conjugate(amplitude)
    return mean_coefficient(scale,omega,hubble,wave,mu,background,amplitude,metric),1j*middle/(2*mu),1j*upper/(2*mu)


def verify():
    import sympy as sp
    phase,amplitude,conjugate_amplitude,background,conjugate_background=sp.symbols("x B Bc A Ac")
    scale,omega,hubble,wave,mu,metric,hzero,zzero=sp.symbols("a omega H k mu z h0 z0",nonzero=True)
    gamma=wave**2/(2*omega*hubble)
    coupling=wave/(2*hubble)
    hminus=omega*background**2/(8*scale**2*hubble**2)
    hplus=omega*conjugate_background**2/(8*scale**2*hubble**2)
    zminus=3*omega*background*amplitude/(4*wave*hubble*scale**2)
    zplus=3*omega*conjugate_background*conjugate_amplitude/(4*wave*hubble*scale**2)
    hlog=hzero+hplus*phase+hminus/phase
    metric_rate=zzero+zplus*phase+zminus/phase
    coefficient=(sp.Rational(3,2)-sp.I*gamma)*conjugate_amplitude+coupling*metric*conjugate_background
    amplitude_rate=sp.I*gamma*conjugate_amplitude-coupling*metric*conjugate_background+((sp.Rational(3,2)+sp.I*gamma)*amplitude+coupling*metric*background)/phase
    coefficient_rate=(sp.I*gamma*(1+hlog)*conjugate_amplitude+(sp.Rational(3,2)-sp.I*gamma)*amplitude_rate-
                      coupling*hlog*metric*conjugate_background+coupling*metric_rate*conjugate_background+
                      sp.Rational(3,2)*coupling*metric*background/phase)
    exact=sp.expand(sp.I*phase*(coefficient_rate-(1-hlog)*coefficient)/(2*mu))
    constant=sp.I/(2*mu)*((sp.Rational(9,4)+gamma**2+3*omega*background*conjugate_background/(8*scale**2*hubble**2))*amplitude+
                        coupling*metric*(3-sp.I*gamma)*background+3*omega*background**2*conjugate_amplitude/(16*scale**2*hubble**2))
    middle=sp.I/(2*mu)*(sp.I*gamma*conjugate_amplitude+(sp.Rational(3,2)-sp.I*gamma)*(sp.I*gamma*conjugate_amplitude-coupling*metric*conjugate_background)+
                       coupling*zzero*conjugate_background-coefficient+sp.Rational(3,2)*hzero*conjugate_amplitude)
    upper=sp.I/(2*mu)*(coupling*zplus*conjugate_background+sp.Rational(3,2)*hplus*conjugate_amplitude)
    identities={f"harmonic_{index}":str(sp.simplify(exact.coeff(phase,index)-value)) for index,value in enumerate((constant,middle,upper))}
    clock=sp.symbols("N",real=True)
    harmonic=sp.symbols("j",integer=True,positive=True)
    angle=sp.Function("theta")(clock)
    frequency=sp.diff(angle,clock)
    source=sp.Function("C")(clock)
    rotate=sp.exp(2*sp.I*harmonic*angle)
    primitive=rotate*source/(2*sp.I*harmonic*frequency)
    residual=rotate*(sp.diff(source,clock)-sp.diff(frequency,clock)*source/frequency)/(2*sp.I*harmonic*frequency)
    identities["integration_by_parts"]=str(sp.simplify(sp.diff(primitive,clock)-rotate*source-residual))
    if set(identities.values())!={"0"}:
        raise ValueError("harmonic identities")
    return dict(passed=True,identities=identities,assumptions=["canonical trace and scalar equations","fixed a,H,A,B,z and spectator variables in carrier extraction"],
                coefficients=[str(value) for value in (constant,middle,upper)])

