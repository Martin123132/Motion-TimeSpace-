from __future__ import annotations

import sympy as sp

from balance import ROOT, digest, read_json, save, input_hashes, modest_process


def main():
    modest_process()
    source = ROOT/'results/derivation/status.json'
    report = read_json(source)
    conservative, induced, squared, mass_ratio, tidal = sp.symbols('k b z q ell', real=True)
    epsilon = sp.symbols('eps', real=True)
    locals_map = dict(k=conservative, b=induced, z=squared)
    laws = {key:sp.sympify(value, locals=locals_map) for key, value in report['dimensionless_laws'].items()}
    checks = []

    def truncate(expression):
        replaced = expression.subs({conservative:epsilon*conservative, induced:epsilon*induced})
        return sp.expand(sp.series(sp.series(replaced, epsilon, 0, 2).removeO(), squared, 0, 2).removeO().subs(epsilon, 1))

    def exact(name, expression):
        residual = sp.factor(expression)
        assert residual == 0, (name, residual)
        checks.append(dict(name=name, residual=str(residual), passed=True))

    omega_ratio = laws['omega0']+squared*laws['omega2']
    distance_slope = -sp.Rational(3, 2)*omega_ratio-5*conservative*sp.diff(omega_ratio, conservative)
    torque = laws['torque0']+squared*laws['torque2']
    chirp_at_actions = truncate(-sp.Rational(2, 3)*distance_slope*torque
                    -sp.Rational(19, 9)*squared*laws['omega2']*laws['damping_ratio'])
    mapping_coefficient = sp.symbols('c', real=True)
    radius_ratio = 1-squared+8*conservative+mapping_coefficient*conservative*squared
    fixed_frequency = truncate(radius_ratio**(-sp.Rational(3, 2))*omega_ratio.subs(conservative, conservative*radius_ratio**-5))
    solved = sp.solve((fixed_frequency-1).coeff(conservative, 1).coeff(squared, 1), mapping_coefficient)[0]
    exact('fixed-frequency action-radius cross coefficient', solved-57)
    radius_ratio = radius_ratio.subs(mapping_coefficient, solved)
    exact('fixed-frequency orbit mapping', truncate(radius_ratio**(-sp.Rational(3, 2))*omega_ratio.subs(conservative, conservative*radius_ratio**-5))-1)
    chirp_at_frequency = truncate(radius_ratio**(-sp.Rational(11, 2))*chirp_at_actions.subs(
        {conservative:conservative*radius_ratio**-5, induced:induced*radius_ratio**-5}, simultaneous=True))
    physical = {conservative:sp.Rational(3, 2)*mass_ratio*tidal, induced:3*(1+mass_ratio)*tidal}
    exact('Peters circular frequency chirp eccentricity', chirp_at_frequency.subs({conservative:0, induced:0})-1-sp.Rational(157, 24)*squared)
    exact('stage20 circular chirp recovered again', chirp_at_frequency.subs(squared, 0).subs(physical)-1-6*(1+12*mass_ratio)*tidal)
    exact('testmass conversion from action radius', chirp_at_frequency.subs(conservative, 0)-truncate((1-squared)**(-sp.Rational(11, 2))*chirp_at_actions.subs(conservative, 0).subs(induced, induced*(1-squared)**-5)))
    exact('circular zero tide chirp', chirp_at_actions.subs({squared:0, conservative:0, induced:0})-1)
    values = dict(action_radius_chirp=str(chirp_at_actions), frequency_radius_chirp=str(chirp_at_frequency),
                  physical_frequency_chirp=str(sp.expand(chirp_at_frequency.subs(physical))),
                  action_to_frequency_radius=str(radius_ratio), exact_checks=len(checks), checks=checks)
    save('chirp', __file__, dict(input_hashes={**input_hashes(), str(source):digest(source)}, **values,
         eccentricity_definition='z=2Jr/Jphi; agrees with Kepler e squared only to first order at zero tide',
         frequency_radius='D=(MT/Omega_phi squared)^(1/3)',
         scope='Same linear static electric tide and first-order z as derivation; not a finite-frequency postadiabatic waveform.'))
    print(values, flush=True)


if __name__ == '__main__':
    main()
