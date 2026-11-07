from __future__ import annotations

import sympy as sp

from inspiral import ROOT, BRANCH, PARENT, read_json, digest, save, modest_process


def main():
    modest_process()
    paths = [BRANCH/'postcircular-clock-20261005/results/weak-field/status.json',
        BRANCH/'near-circular-quadrupole-20261005/results/stage-integrity.json',
        PARENT/'results/derivation/status.json', ROOT/'results/derivation/status.json']
    older_clock, older_damping, parent, current = [read_json(path) for path in paths]
    tide, squared, mass_ratio, auxiliary = sp.symbols('ell z q eps')
    namespace = dict(ell=tide, z=squared, q=mass_ratio)
    torque2 = sp.sympify(older_clock['tidal_P2_coefficient'])
    gamma = sp.sympify(older_damping['outgoing_tidal_coefficient'])
    checks = []

    def exact(name, value):
        residual = sp.factor(value)
        assert residual == 0, (name, residual)
        checks.append(dict(name=name, residual=str(residual), passed=True))

    def truncate(value):
        value = value.subs(tide, auxiliary*tide)
        value = sp.series(value, auxiliary, 0, 2).removeO().subs(auxiliary, 1)
        return sp.series(value, squared, 0, 2).removeO().expand()

    exact('q0 damping uses archived stage35 outgoing coefficient',
        sp.sympify(current['coefficients']['gamma_frequency'], locals=namespace).subs(mass_ratio, 0)-gamma)
    exact('q0 action shrinkage uses archived stage37 coefficient',
        sp.sympify(parent['physical_laws']['torque2'], locals=namespace).subs(mass_ratio, 0).coeff(tide)-torque2)
    radius_ratio = 1-squared
    radius_derivative = radius_ratio-sp.Rational(19, 6)*squared*(1+(gamma-6)*tide)
    source_shrinkage = 1+6*tide/radius_ratio**5+squared*(-sp.Rational(5, 8)+torque2*tide/radius_ratio**5)
    pulled_clock = truncate(radius_ratio**3*radius_derivative/source_shrinkage)
    new = current['coefficients']
    chirp = 1+sp.sympify(new['eccentric'])*squared+6*tide+sp.sympify(new['eccentric_tide'], locals=namespace).subs(mass_ratio, 0)*tide*squared
    exact('source-independent stage35/37 outgoing clock pullback', pulled_clock-truncate(1/chirp))
    save('testmass', __file__, dict(checks=checks, exact_checks=len(checks),
        input_hashes={str(path):digest(path) for path in paths},
        interpretation='Outgoing static electric part only. No horizon absorption carried over; frequency endpoints are transformed.'))
    print(len(checks), 'additional archived-source identities passed', flush=True)


if __name__ == '__main__':
    main()
