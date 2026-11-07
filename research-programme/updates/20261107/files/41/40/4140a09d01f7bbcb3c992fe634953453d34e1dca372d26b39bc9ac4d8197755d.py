from __future__ import annotations

import sympy as sy
from stage_common import *


def main():
    modest()
    folder = ROOT / 'results/identities'
    folder.mkdir(parents=True, exist_ok=False)
    hubble, mode, density, delta, momentum, pressure, metric = sy.symbols('H k R delta q Pi z', nonzero=True)
    delta_prime = -3*hubble*pressure-mode*momentum-mode*metric
    momentum_prime = -hubble*momentum+mode*pressure
    density_prime = -hubble*density
    checks = {}
    checks['averaged_energy_identity'] = sy.simplify(density_prime*delta+density*delta_prime
        +hubble*(density*delta+3*density*pressure)+mode*density*momentum+mode*metric*density)
    checks['averaged_momentum_identity'] = sy.simplify(density_prime*momentum+density*momentum_prime
        +2*hubble*density*momentum-mode*density*pressure)
    scale, mass, root = sy.symbols('a M root', positive=True)
    sound2 = (root-1)/(root+1)
    beat = scale*mass*(root-1)
    checks['beat_dispersion'] = sy.factor((beat**2-mode**2*sound2).subs(mode**2, (scale*mass)**2*(root**2-1)))
    kappa = sy.symbols('kappa')
    sound = kappa**2/(sy.sqrt(1+kappa**2)+1)**2
    checks['nonrelativistic_sound_limit'] = sy.limit(sound/kappa**2, kappa, 0)-sy.Rational(1,4)
    checks['zero_pressure_cold_limit_density'] = sy.simplify(delta_prime.subs(pressure,0)+mode*momentum+mode*metric)
    checks['zero_pressure_cold_limit_momentum'] = sy.simplify(momentum_prime.subs(pressure,0)+hubble*momentum)
    checks['background_comoving_density_constant'] = sy.simplify(scale*density_prime+scale*hubble*density)
    rows = [dict(name=name, residual=str(value), passed=value==0) for name,value in checks.items()]
    assert all(row['passed'] for row in rows)
    finish(folder, dict(checks=rows, count=len(rows), all_checks_passed=True,
        note='Exact algebra for the retained averaged equations, not an all-orders averaging proof.'), __file__)
    print(json.dumps(rows, indent=2))


if __name__ == '__main__':
    main()
