from __future__ import annotations

import sympy as sp

from balance import ROOT, BRANCH, digest, save, input_hashes, modest_process


def main():
    modest_process()
    radius, velocity = sp.symbols('r v', real=True, positive=True)
    perturbation, conservative, induced, squared, mass_ratio, tidal = sp.symbols('eps k b z q ell', real=True)
    checks = []

    def exact(name, expression):
        residual = sp.factor(sp.cancel(expression))
        assert residual == 0, (name, residual)
        checks.append(dict(name=name, passed=True, residual=str(residual)))

    def linear(expression):
        expression = sp.expand(expression)
        return expression.coeff(perturbation, 0)+perturbation*expression.coeff(perturbation, 1)

    rotation = sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 0]])
    quadrupole = (radius**2+perturbation*induced/radius**3)*sp.diag(sp.Rational(2, 3), -sp.Rational(1, 3), -sp.Rational(1, 3))
    force = radius**-3-radius**-2-6*perturbation*conservative/radius**7

    def time_derivative(matrix):
        return (velocity*matrix.diff(radius)+force*matrix.diff(velocity)+(rotation*matrix-matrix*rotation)/radius**2).applyfunc(linear)

    first = time_derivative(quadrupole)
    second = time_derivative(first)
    third = time_derivative(second)
    power = linear(sp.trace(third.T*third)/32)
    torque = linear(sum(second[0, index]*third[1, index]-second[1, index]*third[0, index] for index in range(3))/16)
    for index, matrix in enumerate([quadrupole, first, second, third]):
        exact('STF derivative '+str(index), sp.trace(matrix))
        for row_index in range(3):
            for column_index in range(row_index):
                exact(f'symmetric derivative {index} {row_index}{column_index}', matrix[row_index, column_index]-matrix[column_index, row_index])

    def shifted(expression):
        value = linear(expression.subs(velocity, 0))
        return linear(value.subs(radius, 1)-6*perturbation*conservative*sp.diff(value, radius).subs(radius, 1))

    def average_law(observable):
        base = shifted(observable)
        coefficient = linear(shifted(sp.diff(observable, radius))*(sp.Rational(3, 2)-sp.Rational(33, 2)*perturbation*conservative)
                        +shifted(sp.diff(observable, radius, 2))*(1+3*perturbation*conservative)/4
                        +shifted(sp.diff(observable, velocity, 2))*(1-3*perturbation*conservative)/4)
        return sp.factor(base), sp.factor(coefficient)

    power0, power2 = average_law(power)
    torque0, torque2 = average_law(torque)
    omega0, omega2 = average_law(radius**-2)
    radial0 = 1-3*perturbation*conservative
    exact('circular frequency', omega0-1-12*perturbation*conservative)
    exact('eccentric azimuthal frequency', omega2+sp.Rational(3, 2)-sp.Rational(39, 2)*perturbation*conservative)
    exact('circular power angular balance', linear(power0-omega0*torque0))
    exact('point energy eccentric coefficient', power2.subs(perturbation, 0)-sp.Rational(37, 24))
    exact('point angular eccentric coefficient', torque2.subs(perturbation, 0)+sp.Rational(5, 8))
    exact('induced quadrupole energy coefficient', sp.diff(power2, induced)-perturbation*sp.Rational(199, 4))
    exact('induced quadrupole angular coefficient', sp.diff(torque2, induced)-perturbation*sp.Rational(105, 4))
    radial_loss2 = linear((power2-linear(omega0*torque2+omega2*torque0))*(1+3*perturbation*conservative))
    damping_ratio = linear((2*radial_loss2-torque0)/(sp.Rational(19, 3)))
    physical = {conservative:sp.Rational(3, 2)*mass_ratio*tidal, induced:3*(1+mass_ratio)*tidal, perturbation:1}
    exact('testmass stage35 damping', (damping_ratio.subs(physical)).subs(mass_ratio, 0)-1-sp.Rational(459, 19)*tidal)
    exact('testmass stage37 P2', (torque2.subs(physical)).subs(mass_ratio, 0)+sp.Rational(5, 8)-sp.Rational(315, 4)*tidal)

    circular_power_fixed_frequency = linear(power0*(1-40*perturbation*conservative))
    exact('stage20 circular fixed-frequency flux', circular_power_fixed_frequency.subs(physical)-1-6*(1+3*mass_ratio)*tidal)
    frequency_slope_ratio = 1+52*perturbation*conservative
    circle_chirp_at_action = linear(torque0*frequency_slope_ratio)
    circle_chirp_at_frequency = linear(circle_chirp_at_action*(1-44*perturbation*conservative))
    exact('stage20 circular chirp', circle_chirp_at_frequency.subs(physical)-1-6*(1+12*mass_ratio)*tidal)

    angular_action, radial_action, alpha, total_mass = sp.symbols('h j alpha MT', positive=True)
    distance = angular_action**2/total_mass
    hamiltonian = -total_mass**2/(2*(radial_action+angular_action)**2)-alpha/distance**6*(1+3*radial_action/angular_action)
    scaled_phi = sp.diff(hamiltonian, angular_action).subs({angular_action:1, radial_action:squared/2, total_mass:1, alpha:conservative})
    scaled_phi = sp.series(scaled_phi, squared, 0, 2).removeO()
    exact('independent action Hamiltonian frequency', scaled_phi-(omega0+squared*omega2).subs(perturbation, 1))
    exact('radial frequency from action Hamiltonian', sp.diff(hamiltonian, radial_action).subs({angular_action:1, radial_action:0, total_mass:1, alpha:conservative})-radial0.subs(perturbation, 1))
    exact('first-law energy loss', linear(omega0*torque2+omega2*torque0+radial0*radial_loss2-power2))

    local_coefficients = {name:{'point':str(expression.coeff(perturbation, 0)),
        'conservative':str(sp.expand(expression).coeff(perturbation, 1).coeff(conservative, 1)),
        'induced':str(sp.expand(expression).coeff(perturbation, 1).coeff(induced, 1))}
        for name, expression in [('power', power), ('torque', torque)]}
    laws = {name:str(sp.expand(expression.subs(perturbation, 1))) for name, expression in
            [('power0', power0), ('power2', power2), ('torque0', torque0), ('torque2', torque2),
             ('omega0', omega0), ('omega2', omega2), ('radial0', radial0), ('radial_loss2', radial_loss2), ('damping_ratio', damping_ratio)]}
    physical_laws = {name:str(sp.factor(expression.subs(physical))) for name, expression in
                     [('power0', power0), ('power2', power2), ('torque0', torque0), ('torque2', torque2), ('damping_ratio', damping_ratio)]}
    sources = [BRANCH/'orbital-backreaction-20261004/20-reciprocal-tidal-orbit-and-consistent-leading-inspiral.md',
               BRANCH/'near-circular-quadrupole-20261005/results/stage-integrity.json',
               BRANCH/'postcircular-clock-20261005/results/weak-field/status.json']
    report = save('derivation', __file__, dict(input_hashes={**input_hashes(), **{str(path):digest(path) for path in sources}},
        checks=checks, exact_checks=len(checks), dimensionless_laws=laws, physical_laws=physical_laws,
        local_flux_coefficients=local_coefficients, small_parameters='k=3q lambda/(2d^5), b=3(1+q)lambda/d^5, z=2Jr/Jphi',
        scope='Leading Newtonian static electric tide; linear lambda and z, including lambda*z; no absorption, dynamic or PN completion.'))
    print('exact checks', len(checks), 'dimensionless laws', laws, 'physical laws', physical_laws, flush=True)


if __name__ == '__main__':
    main()
