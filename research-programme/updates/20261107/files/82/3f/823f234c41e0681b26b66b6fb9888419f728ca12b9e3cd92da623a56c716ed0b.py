from __future__ import annotations

import sympy as sp

from inspiral import ROOT, BRANCH, PARENT, read_json, digest, save, dependencies, modest_process


def main():
    modest_process()
    mass_ratio, tide, squared, ratio, initial_z, initial_tide = sp.symbols('q ell z y zi li', positive=True)
    epsilon, eccentric_parameter = sp.symbols('eps eta', real=True)
    locals_map = dict(q=mass_ratio, ell=tide, z=squared)
    source_path = PARENT/'results/chirp/status.json'
    balance_path = PARENT/'results/derivation/status.json'
    source = read_json(source_path)
    parent_balance = read_json(balance_path)
    chirp = sp.sympify(source['physical_frequency_chirp'], locals=locals_map)
    gamma_action = sp.sympify(parent_balance['physical_laws']['damping_ratio'], locals=locals_map)
    eccentric = sp.expand(chirp).coeff(squared, 1).subs(tide, 0)
    circular_tide = sp.expand(chirp).coeff(tide, 1).subs(squared, 0)
    eccentric_tide = sp.expand(chirp).coeff(tide, 1).coeff(squared, 1)
    gamma_frequency = sp.expand(gamma_action).coeff(tide, 1)-48*mass_ratio
    power = sp.Rational(19, 6)
    transport = sp.factor(power*(gamma_frequency-circular_tide)/5)
    mixed = sp.factor(2*eccentric*circular_tide-eccentric_tide+eccentric*transport)
    checks = []

    def exact(name, expression):
        residual = sp.factor(sp.cancel(expression))
        assert residual == 0, (name, residual)
        checks.append(dict(name=name, residual=str(residual), passed=True))

    def truncate(expression):
        value = expression.subs({tide:epsilon*tide, squared:eccentric_parameter*squared})
        return sp.expand(sp.series(sp.series(value, epsilon, 0, 2).removeO(), eccentric_parameter, 0, 2).removeO().subs({epsilon:1, eccentric_parameter:1}))

    exact('frequency-radius damping coefficient', gamma_frequency-sp.Rational(459, 19)-sp.Rational(8547, 76)*mass_ratio)
    exact('derived eccentricity transport coefficient', transport-sp.Rational(23, 2)-sp.Rational(205, 8)*mass_ratio)
    transport0 = ratio**power
    transport1 = -transport*(ratio**-5-1)*transport0
    exact('point eccentricity transport', sp.diff(transport0, ratio)-power*transport0/ratio)
    exact('tidal eccentricity transport', sp.diff(transport1, ratio)-power*transport1/ratio-power*(gamma_frequency-circular_tide)*transport0/ratio**6)
    exact('common initial eccentricity', transport1.subs(ratio, 1))
    inverse = truncate(1/chirp)
    expected_inverse = 1-eccentric*squared-circular_tide*tide+(2*eccentric*circular_tide-eccentric_tide)*tide*squared
    exact('mixed-order reciprocal chirp', inverse-expected_inverse)
    inverse_with_transport = sp.expand(inverse.subs({squared:initial_z*(transport0+initial_tide*transport1), tide:initial_tide/ratio**5}))
    inverse_with_transport = sp.series(inverse_with_transport, initial_tide, 0, 2).removeO()
    bracket = 1-eccentric*initial_z*transport0-circular_tide*initial_tide/ratio**5+initial_z*initial_tide*transport0*(mixed/ratio**5-eccentric*transport)
    exact('clock includes changed eccentricity history', inverse_with_transport-bracket)
    coefficient_primitives = {}
    for name, exponent in [('time', sp.Integer(3)), ('orbital_phase', sp.Rational(3, 2))]:
        kernels = [-ratio**exponent, eccentric*ratio**(exponent+power), circular_tide*ratio**(exponent-5),
                   -mixed*ratio**(exponent+power-5)+eccentric*transport*ratio**(exponent+power)]
        primitives = []
        for index, kernel in enumerate(kernels):
            primitive = sp.integrate(kernel, ratio)
            primitive -= primitive.subs(ratio, 1)
            exact(name+' primitive '+str(index), sp.diff(primitive, ratio)-kernel)
            exact(name+' initial condition '+str(index), primitive.subs(ratio, 1))
            primitives.append(str(primitive))
        coefficient_primitives[name] = primitives

    radius_ratio = 1-squared+12*mass_ratio*tide+sp.Rational(171, 2)*mass_ratio*tide*squared
    squared_prime_times_radius = power*squared*(1+(gamma_frequency-circular_tide)*tide)
    radius_derivative = truncate(radius_ratio-5*tide*sp.diff(radius_ratio, tide)+sp.diff(radius_ratio, squared)*squared_prime_times_radius)
    action_shrink = sp.sympify(parent_balance['physical_laws']['torque0'], locals=locals_map)+squared*sp.sympify(parent_balance['physical_laws']['torque2'], locals=locals_map)
    transformed = truncate(radius_ratio**3*radius_derivative/action_shrink.subs(tide, tide/radius_ratio**5))
    exact('independent action-radius clock pullback all mass ratios', transformed-inverse)
    exact('stage37 outgoing testmass clock pullback', (transformed-inverse).subs(mass_ratio, 0))

    total_mass, reduced, frequency_initial, frequency_final, deformability = sp.symbols('MT mr Oi Of Lambda', positive=True)
    initial_distance = (total_mass/frequency_initial**2)**sp.Rational(1, 3)
    final_distance = (total_mass/frequency_final**2)**sp.Rational(1, 3)
    phase_circular = -circular_tide*deformability/(32*reduced*total_mass**sp.Rational(3, 2))*(final_distance**(-sp.Rational(5, 2))-initial_distance**(-sp.Rational(5, 2)))
    inherited_gw_phase = -3*deformability*(1+12*mass_ratio)/(8*reduced*total_mass**sp.Rational(7, 3))*(frequency_final**sp.Rational(5, 3)-frequency_initial**sp.Rational(5, 3))
    exact('stage20 circular m2 phase primitive', 2*phase_circular-inherited_gw_phase)
    result = dict(input_hashes={**dependencies(), str(source_path):digest(source_path), str(balance_path):digest(balance_path)},
        checks=checks, exact_checks=len(checks), coefficients=dict(eccentric=str(eccentric), circular_tide=str(circular_tide),
             eccentric_tide=str(eccentric_tide), gamma_frequency=str(gamma_frequency), transport=str(transport), mixed=str(mixed), power=str(power)),
        transport0=str(transport0), transport1=str(transport1), primitives=coefficient_primitives,
        normalization='T=(mu_red/MT²)t; Phi=(mu_red/MT)orbital_phase; y=D/Di; li=lambda/Di^5',
        approximation='Strict first order in lambda and initial zi, retaining lambda*zi; independent same-frequency endpoints.')
    save('derivation', __file__, result)
    print(len(checks), 'exact checks', result['coefficients'], flush=True)


if __name__ == '__main__':
    main()
