import sympy as sp


def verify():
    phase, background, background_conjugate, amplitude, amplitude_conjugate = sp.symbols("x A Ac B Bc")
    scale, omega, hubble, wave, metric = sp.symbols("a omega H k z", nonzero=True)
    other_energy, other_pressure, other_density, other_perturbed_pressure, other_flux = sp.symbols("Ro Po Do dPo Qo")
    scalar_energy=omega*background*background_conjugate/(2*scale**2)
    scalar_pressure=-omega*(background**2/phase+background_conjugate**2*phase)/(4*scale**2)
    scalar_density=omega*(background*amplitude_conjugate+background_conjugate*amplitude)/(2*scale**2)
    scalar_perturbed_pressure=-omega*(background*amplitude/phase+background_conjugate*amplitude_conjugate*phase)/(2*scale**2)
    scalar_flux=wave*(background*amplitude/phase-background_conjugate*amplitude_conjugate*phase+
                      background*amplitude_conjugate-background_conjugate*amplitude)/(4*sp.I*scale**2)
    energy=other_energy+scalar_energy
    pressure=other_pressure+scalar_pressure
    density=other_density+scalar_density
    perturbed_pressure=other_perturbed_pressure+scalar_perturbed_pressure
    flux=other_flux+scalar_flux
    hubble_log=-(energy+3*pressure)/(6*hubble**2)
    density_rate=-hubble*(density+3*perturbed_pressure)-wave*flux-wave*metric*(energy+pressure)
    eta_rate=flux/(2*wave)
    metric_rate=(density_rate/(2*wave)+wave*eta_rate)/hubble**2-hubble_log*metric
    cancellation=sp.simplify(metric_rate+(density+3*perturbed_pressure)/(2*wave*hubble)+metric*energy/(3*hubble**2))
    hubble_minus=sp.expand(hubble_log).coeff(phase,-1)
    metric_minus=sp.expand(metric_rate).coeff(phase,-1)
    identities=dict(
        pressure_current_cancellation=cancellation,
        background_negative_harmonic=sp.simplify(hubble_minus-omega*background**2/(8*scale**2*hubble**2)),
        metric_negative_harmonic=sp.simplify(metric_minus-3*omega*background*amplitude/(4*wave*hubble*scale**2)))
    if any(value!=0 for value in identities.values()):
        raise ValueError("trace harmonic derivation")
    return dict(passed=True,identities={name:str(value) for name,value in identities.items()},
                assumptions=["flat canonical Einstein/continuity equations", "other species fixed during carrier harmonic extraction"],
                metric_equation="z_N=-(D+3 deltaP)/(2kH)-z R/(3H^2); with flat Friedmann R=3H^2 the last term is -z")

