from __future__ import annotations

import sympy as sp

from secular import ROOT, digest, modest_process, save_report


def main():
    modest_process()
    checks = []

    def verify(name, expression):
        residual = sp.factor(expression)
        assert residual == 0, (name, residual)
        checks.append({'name': name, 'residual': str(residual), 'passed': True})

    radius, mass, energy, angular = sp.symbols('radius mass energy angular', positive=True)
    metric = 1-2*mass/radius
    potential = energy**2-metric*(1+angular**2/radius**2)
    momentum = sp.sqrt(potential)/metric
    verify('radial momentum energy derivative equals dt/dr', sp.diff(momentum, energy)-energy/(metric*sp.sqrt(potential)))
    verify('radial momentum angular derivative equals minus dphi/dr', sp.diff(momentum, angular)+angular/(radius**2*sp.sqrt(potential)))
    semilatus, squared, energy_symbol = sp.symbols('p z E', positive=True)
    denominator = semilatus-3-squared
    numerator = (semilatus-2)**2-4*squared
    energy_squared = numerator/(semilatus*denominator)
    angular_expr = mass*semilatus/sp.sqrt(denominator)
    energy_p = (2*(semilatus-2)*semilatus*denominator-numerator*(denominator+semilatus))/(2*energy_symbol*(semilatus*denominator)**2)
    energy_z = (semilatus-4)**2/(2*energy_symbol*semilatus*denominator**2)
    angular_p = mass*(semilatus-6-2*squared)/(2*denominator**sp.Rational(3, 2))
    angular_z = mass*semilatus/(2*denominator**sp.Rational(3, 2))
    verify('energy p derivative', 2*energy_symbol*energy_p-sp.diff(energy_squared, semilatus))
    verify('energy z derivative', 2*energy_symbol*energy_z-sp.diff(energy_squared, squared))
    verify('angular p derivative', angular_p-sp.diff(angular_expr, semilatus))
    verify('angular z derivative', angular_z-sp.diff(angular_expr, squared))
    determinant = -mass*((semilatus-6)**2-4*squared)/(4*energy_symbol*semilatus*denominator**sp.Rational(5, 2))
    verify('regular p z determinant', energy_p*angular_z-energy_z*angular_p-determinant)
    circular_energy = (semilatus-2)/sp.sqrt(semilatus*(semilatus-3))
    omega_phi = 1/(mass*semilatus**sp.Rational(3, 2))
    omega_radial = omega_phi*sp.sqrt((semilatus-6)/semilatus)
    circular_ep = energy_p.subs({squared: 0, energy_symbol: circular_energy})
    circular_ez = energy_z.subs({squared: 0, energy_symbol: circular_energy})
    verify('circular energy tangent', circular_ep-omega_phi*angular_p.subs(squared, 0))
    circular_jz = mass*semilatus**sp.Rational(3, 2)*sp.sqrt(semilatus-6)/(2*(semilatus-2)*sp.sqrt(semilatus-3))
    verify('circular radial action z derivative', (circular_ez-omega_phi*angular_z.subs(squared, 0))-omega_radial*circular_jz)
    power, radial_freq, angular_freq, harmonic = sp.symbols('power Omega_r Omega_phi n', nonzero=True)
    frequency = angular_freq+harmonic*radial_freq
    verify('modal radial action balance', (power-angular_freq*power/frequency)/radial_freq-harmonic*power/frequency)
    action_imag = sp.symbols('Im_F')
    verify('retarded modal radial work', (harmonic*power/frequency).subs(power, 2*frequency*action_imag)-2*harmonic*action_imag)
    ep, ez, hp, hz = sp.symbols('E_p E_z h_p h_z')
    pdot, zdot, Edot, hdot = sp.symbols('pdot zdot Edot hdot')
    det = ep*hz-ez*hp
    p_rate = (Edot*hz-ez*hdot)/det
    z_rate = (ep*hdot-Edot*hp)/det
    verify('inverse reconstructs energy', ep*p_rate+ez*z_rate-Edot)
    verify('inverse reconstructs angular momentum', hp*p_rate+hz*z_rate-hdot)
    jp, jz = (ep-angular_freq*hp)/radial_freq, (ez-angular_freq*hz)/radial_freq
    verify('action determinant', hp*jz-hz*jp+det/radial_freq)
    jdot = (Edot-angular_freq*hdot)/radial_freq
    verify('action inverse p', (hdot*jz-hz*jdot)/(hp*jz-hz*jp)-p_rate)
    verify('action inverse z', (hp*jdot-hdot*jp)/(hp*jz-hz*jp)-z_rate)
    verify('circular z rate vanishes for P equals Omega L',
           (ep*hdot-Edot*hp).subs(Edot, angular_freq*hdot).subs(ep, angular_freq*hp))
    save_report(ROOT/'results/exact', __file__, {'checks': checks, 'exact_checks': len(checks),
                'input_hashes': {str(ROOT/'secular.py'): digest(ROOT/'secular.py')},
                'turning_point_derivative_conditions': 'Simple turning points, stable eccentric orbit; circular identity uses limiting action.'})
    print(f'{len(checks)} exact identities passed')


if __name__ == '__main__':
    main()
