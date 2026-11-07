import sympy as sp


def identities():
    scale, omega, hubble, wave = sp.symbols("a omega H k", positive=True, real=True)
    field, velocity, delta, speed, metric, phase, phase_rate, defect_phi, defect_v = sp.symbols("phi v d u z theta theta_rate ephi ev", real=True)
    rotate=sp.exp(sp.I*phase)
    amplitude=scale*(sp.sqrt(omega)*delta+sp.I*speed/sp.sqrt(omega))*rotate
    conjugate=scale*(sp.sqrt(omega)*delta-sp.I*speed/sp.sqrt(omega))/rotate
    acceleration=-2*hubble*speed-(wave**2+omega**2)*delta-wave*metric*velocity
    chain=sp.diff(amplitude,scale)*scale*hubble+sp.diff(amplitude,omega)*omega*hubble+sp.diff(amplitude,delta)*speed+sp.diff(amplitude,speed)*acceleration+sp.diff(amplitude,phase)*phase_rate
    derived=sp.Rational(3,2)*hubble*rotate**2*conjugate-sp.I*wave**2/(2*omega)*(amplitude+rotate**2*conjugate)-sp.I*scale*wave*metric*velocity*rotate/sp.sqrt(omega)+sp.I*(phase_rate-omega)*amplitude
    background=scale*(sp.sqrt(omega)*field+sp.I*velocity/sp.sqrt(omega))*rotate
    background_conjugate=scale*(sp.sqrt(omega)*field-sp.I*velocity/sp.sqrt(omega))/rotate
    background_chain=sp.diff(background,scale)*scale*hubble+sp.diff(background,omega)*omega*hubble+sp.diff(background,field)*(velocity+defect_phi)+sp.diff(background,velocity)*(-2*hubble*velocity-omega**2*field+defect_v)+sp.diff(background,phase)*phase_rate
    background_derived=sp.Rational(3,2)*hubble*rotate**2*background_conjugate+scale*rotate*(sp.sqrt(omega)*defect_phi+sp.I*defect_v/sp.sqrt(omega))+sp.I*(phase_rate-omega)*background
    unrotated_background=background/rotate
    unrotated_perturbation=amplitude/rotate
    products=dict(density=sp.re(unrotated_background*sp.conjugate(unrotated_perturbation))*omega/scale**2-(velocity*speed+omega**2*field*delta),
                  pressure=-sp.re(unrotated_background*unrotated_perturbation)*omega/scale**2-(velocity*speed-omega**2*field*delta),
                  current=wave/(2*scale**2)*(sp.im(unrotated_background*unrotated_perturbation)+sp.im(unrotated_background*sp.conjugate(unrotated_perturbation)))-wave*velocity*delta,
                  endpoint=sp.im(unrotated_background*unrotated_perturbation)/scale**2-(velocity*delta+field*speed))
    products.update(perturbation_evolution=chain-derived,background_evolution=background_chain-background_derived,
                    inverse_field=sp.re(amplitude/rotate)/(scale*sp.sqrt(omega))-delta,
                    inverse_velocity=sp.im(amplitude/rotate)*sp.sqrt(omega)/scale-speed)
    result={name:str(sp.simplify(sp.expand(value))) for name,value in products.items()}
    if set(result.values())!={"0"}:
        raise ValueError(result)
    return result

