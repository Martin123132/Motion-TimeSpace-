import sympy as sp


def verify():
    phase, amplitude, amplitude_conjugate, background, background_conjugate = sp.symbols("x B Bc A Ac")
    scale, omega, hubble, wave, mu, metric, hzero, zzero = sp.symbols("a omega H k mu z h0 z0", nonzero=True)
    gamma=wave**2/(2*omega*hubble)
    coupling=wave/(2*hubble)
    hminus=omega*background**2/(8*scale**2*hubble**2)
    hplus=omega*background_conjugate**2/(8*scale**2*hubble**2)
    zminus=3*omega*background*amplitude/(4*wave*hubble*scale**2)
    zplus=3*omega*background_conjugate*amplitude_conjugate/(4*wave*hubble*scale**2)
    hlog=hzero+hplus*phase+hminus/phase
    metric_rate=zzero+zplus*phase+zminus/phase
    coefficient=(sp.Rational(3,2)-sp.I*gamma)*amplitude_conjugate+coupling*metric*background_conjugate
    conjugate_coefficient=(sp.Rational(3,2)+sp.I*gamma)*amplitude+coupling*metric*background
    amplitude_conjugate_rate=sp.I*gamma*amplitude_conjugate-coupling*metric*background_conjugate+conjugate_coefficient/phase
    background_conjugate_rate=sp.Rational(3,2)*background/phase
    coefficient_rate=(sp.I*gamma*(1+hlog)*amplitude_conjugate+
                      (sp.Rational(3,2)-sp.I*gamma)*amplitude_conjugate_rate-
                      coupling*hlog*metric*background_conjugate+coupling*metric_rate*background_conjugate+
                      coupling*metric*background_conjugate_rate)
    remainder=sp.expand(-phase/(2*sp.I*mu)*(coefficient_rate-(1-hlog)*coefficient))
    extracted=sp.expand(remainder).coeff(phase,0)
    prediction=sp.I/(2*mu)*(
        (sp.Rational(9,4)+gamma**2+3*omega*background*background_conjugate/(8*scale**2*hubble**2))*amplitude+
        coupling*metric*(3-sp.I*gamma)*background+
        3*omega*background**2*amplitude_conjugate/(16*scale**2*hubble**2))
    check=sp.simplify(extracted-prediction)
    polynomial=sp.Poly(remainder,phase)
    if check!=0 or polynomial.degree()>2:
        raise ValueError("mean remainder derivation")
    return dict(passed=True,mean_identity=str(check),harmonics=[int(item[0]) for item,_ in polynomial.terms()],
                expression=str(prediction),
                assumptions=["exact canonical background and trace constraint", "theta_N=omega/H",
                             "freeze a,H,A,B,z and other species while extracting carrier phase",
                             "dense/background/continuity defects separately retained in numerical control"],
                interpretation="R contains a nonzero phase-independent term; deleting all R is not the same as deleting only fast terms")

