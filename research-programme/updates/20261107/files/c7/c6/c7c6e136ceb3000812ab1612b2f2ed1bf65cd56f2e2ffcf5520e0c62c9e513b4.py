from __future__ import annotations

import sympy as sp

from conservative import save, dependencies, modest_process


def main():
    modest_process()
    checks = []

    def exact(name, expression):
        reduced = sp.simplify(sp.expand(expression))
        assert reduced == 0, (name, reduced)
        checks.append(dict(name=name, residual=str(reduced), passed=True))

    semilatus, mass, particle, deformability, radius = sp.symbols('p M mu Lambda r0', positive=True)
    eccentricity, anomaly = sp.symbols('e chi', real=True)
    energy0 = (semilatus-2)/sp.sqrt(semilatus*(semilatus-3))
    angular0 = mass*semilatus/sp.sqrt(semilatus-3)
    angular2 = angular0/(2*(semilatus-3))
    energy2 = energy0*(1/(2*(semilatus-3))-2/(semilatus-2)**2)
    omega_phi = 1/(mass*semilatus**sp.Rational(3, 2))
    omega_r = sp.sqrt(semilatus-6)/(mass*semilatus**2)
    radial_coefficient = mass*semilatus**sp.Rational(3, 2)*sp.sqrt(semilatus-6)/(2*(semilatus-2)*sp.sqrt(semilatus-3))
    exact('background circular first law', sp.diff(energy0, semilatus)-omega_phi*sp.diff(angular0, semilatus))
    exact('eccentric energy action identity', energy2-omega_phi*angular2-omega_r*radial_coefficient)

    action0_prime, action2, angular_prime, angular_second, radial_second = sp.symbols('f0prime f2 h0prime h2 C', nonzero=True)
    jacobian = particle*sp.Matrix([[0, radial_second], [angular_prime, angular_second]])
    gradients = -particle**2*sp.Matrix([[action0_prime, action2]])*jacobian.inv()
    exact('radial frequency from inverse action map', gradients[0]+particle*(action2-angular_second*action0_prime/angular_prime)/radial_second)
    exact('azimuth frequency from inverse action map', gradients[1]+particle*action0_prime/angular_prime)

    epsilon, coupling, canonical, background, frequency = sp.symbols('eps k J A omega', real=True)
    toy = coupling*background**2*frequency**2/2
    corrected_background = canonical-epsilon*sp.diff(toy, frequency).subs({background:canonical, frequency:canonical})
    corrected_frequency = corrected_background-epsilon*sp.diff(toy, background).subs({background:canonical, frequency:canonical})
    pullback = toy.subs({background:canonical, frequency:canonical})
    exact('dispersive canonical frequency requires total derivative', corrected_frequency-canonical+epsilon*sp.diff(pullback, canonical))
    toy_energy = canonical**2/2-epsilon*pullback
    exact('dispersive Hamiltonian Legendre check', sp.diff(toy_energy, canonical)-corrected_frequency)

    def average(expression):
        return sp.simplify(sp.integrate(sp.expand_trig(sp.expand(expression)), (anomaly, 0, 2*sp.pi))/(2*sp.pi))

    local_weighted = (1-sp.Rational(3, 2)*eccentricity**2)*(1+eccentricity*sp.cos(anomaly))**4
    local_average = sp.series(average(local_weighted), eccentricity, 0, 3).removeO()
    exact('Kepler averaged inverse sixth power', local_average-1-sp.Rational(3, 2)*eccentricity**2)
    static_amplitude = average((1-sp.Rational(3, 2)*eccentricity**2)*(1+eccentricity*sp.cos(anomaly)))
    exact('static overlap correction', static_amplitude-1+sp.Rational(3, 2)*eccentricity**2)
    weight_tide = (1-sp.Rational(3, 2)*eccentricity**2)*(1+eccentricity*sp.cos(anomaly))
    phase_series = 1-4*sp.I*eccentricity*sp.sin(anomaly)-8*eccentricity**2*sp.sin(anomaly)**2
    carrier_average = sp.series(average(weight_tide*phase_series), eccentricity, 0, 3).removeO()
    exact('m2 tidal carrier correction', carrier_average-1+sp.Rational(11, 2)*eccentricity**2)
    sideband_values = {}
    for azimuth, harmonic in [(0, 1), (2, -1), (2, 1)]:
        oscillation = sp.cos(harmonic*anomaly)+sp.I*sp.sin(harmonic*anomaly)
        value = average(oscillation*(sp.cos(anomaly)-2*sp.I*(azimuth+harmonic)*sp.sin(anomaly)))
        expected = {(0, 1):sp.Rational(3, 2), (2, -1):-sp.Rational(1, 2), (2, 1):sp.Rational(7, 2)}[(azimuth, harmonic)]
        exact(f'tidal sideband m{azimuth} n{harmonic}', value-expected)
        sideband_values[f'm{azimuth}n{harmonic}'] = str(value)
    spectral_second = -sp.Rational(3, 4)+sp.Rational(1, 4)*2*sp.Rational(3, 2)**2-sp.Rational(3, 4)*11+sp.Rational(3, 4)*(sp.Rational(1, 2)**2+sp.Rational(7, 2)**2)
    exact('spectral and local O(e squared) action agree', spectral_second-sp.Rational(3, 2))
    harmonic0 = -sp.sqrt(5/(16*sp.pi))
    overlap0 = -4*sp.pi*harmonic0/(3*radius**3)
    static_action = -9*deformability/(16*sp.pi*(-sp.Rational(5, 6)))*overlap0**2
    leading = 3*deformability/(2*radius**6)
    exact('static mode quarter normalization', static_action-leading/4)

    leading_p = leading.subs(radius, mass*semilatus)
    newton_angular_prime = mass/(2*sp.sqrt(semilatus))
    newton_radial_second = mass*sp.sqrt(semilatus)/2
    newton_phi_shift = -particle*sp.diff(leading_p, semilatus)/newton_angular_prime
    newton_r_shift = -particle*sp.Rational(3, 2)*leading_p/newton_radial_second
    scale = particle*deformability/(mass*(mass*semilatus)**5)
    exact('Newtonian azimuth shift coefficient18', newton_phi_shift/omega_phi-18*scale)
    exact('Newtonian radial shift coefficient minus9over2', newton_r_shift/omega_phi+sp.Rational(9, 2)*scale)
    exact('Newtonian periapsis coefficient45over2', (newton_phi_shift-newton_r_shift)/omega_phi-sp.Rational(45, 2)*scale)

    frequency_symbol = sp.symbols('Omega', positive=True)
    frequency_action = 3*deformability*particle**2*frequency_symbol**4/(2*mass**2)
    energy_shift = frequency_symbol*sp.diff(frequency_action, frequency_symbol)-frequency_action
    angular_shift = sp.diff(frequency_action, frequency_symbol)
    exact('stage20 fixed frequency circular energy', energy_shift-3*frequency_action)
    exact('stage20 fixed frequency circular first law', sp.diff(energy_shift, frequency_symbol)-frequency_symbol*sp.diff(angular_shift, frequency_symbol))

    scaled_radius = sp.symbols('rho', positive=True)
    force_balance = scaled_radius+6*epsilon/scaled_radius**4-1
    exact('direct central force shifted radius', sp.diff(force_balance.subs(scaled_radius, 1-6*epsilon), epsilon).subs(epsilon, 0))
    angular_exact = scaled_radius**-2
    radial_squared_exact = scaled_radius**-3-24*epsilon*scaled_radius**-8
    exact('direct central force azimuth shift', sp.diff(angular_exact.subs(scaled_radius, 1-6*epsilon), epsilon).subs(epsilon, 0)-12)
    exact('direct central force radial shift', sp.diff(sp.sqrt(radial_squared_exact.subs(scaled_radius, 1-6*epsilon)), epsilon).subs(epsilon, 0)+3)
    save('derivation', __file__, dict(input_hashes=dependencies(), checks=checks, exact_checks=len(checks),
        weak_sideband_amplitudes=sideband_values, radial_action_coefficient=str(radial_coefficient),
        weak_action_second_over_zero=str(spectral_second), weak_precession_coefficient='45/2',
        interpretation='Analytic source action and circular-limit conservative frequency laws; finite e squared radial frequency needs action through e fourth.'))
    print(len(checks), 'exact identities pass', flush=True)


if __name__ == '__main__':
    main()
