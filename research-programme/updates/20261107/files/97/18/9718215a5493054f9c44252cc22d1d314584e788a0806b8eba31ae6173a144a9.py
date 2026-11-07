from __future__ import annotations

import hashlib
import json
from pathlib import Path

import psutil
import sympy as sp


ROOT = Path(__file__).resolve().parent


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    checks = []

    def check(name, expression):
        residual = sp.factor(sp.expand(expression))
        assert residual == 0, (name, residual)
        checks.append({'name': name, 'passed': True, 'residual': str(residual)})

    radius, alpha, body_frequency = sp.symbols('radius alpha body_frequency', positive=True)
    field, lapse, metric = [sp.Function(name)(radius) for name in ['field', 'nu', 'F']]
    potential = sp.Function('W')(field)
    rotation = body_frequency**2*field**2*sp.exp(-2*lapse)
    gradient = metric*sp.diff(field, radius)**2
    density, pressure = (rotation+gradient)/2+potential, (rotation+gradient)/2-potential
    transverse = (rotation-gradient)/2-potential
    scalar_second = (sp.diff(potential, field)-body_frequency**2*sp.exp(-2*lapse)*field)/metric
    scalar_second -= (2/radius+sp.diff(lapse, radius)+sp.diff(metric, radius)/(2*metric))*sp.diff(field, radius)
    conservation = sp.diff(pressure, radius)+(density+pressure)*sp.diff(lapse, radius)+2*(pressure-transverse)/radius
    check('scalar_radial_stress_conservation', conservation.subs(sp.diff(field, radius, 2), scalar_second))
    density_symbol, pressure_symbol, mass, gradient_squared = sp.symbols('rho pressure mass gradient_squared')
    lapse_derivative = (mass+alpha*radius**3*pressure_symbol)/(radius**2*metric)
    coefficient = mass/(radius**2*metric)+alpha*radius*(density_symbol+pressure_symbol)/metric
    source = mass*density_symbol/(radius**2*metric)+2*metric*gradient_squared/radius
    check('positive_pressure_integrating_factor', -(density_symbol+pressure_symbol)*lapse_derivative-2*metric*gradient_squared/radius
          +coefficient*pressure_symbol+source)
    tortoise, squared_frequency = sp.symbols('rstar squared_frequency', real=True)
    wave_potential = sp.Function('V')(tortoise)
    zero_solution, finite_solution = [sp.Function(name)(tortoise) for name in ['u0', 'us']]
    wronskian = zero_solution*sp.diff(finite_solution, tortoise)-sp.diff(zero_solution, tortoise)*finite_solution
    equation_rules = {sp.diff(zero_solution, tortoise, 2): wave_potential*zero_solution,
                      sp.diff(finite_solution, tortoise, 2): (wave_potential-squared_frequency)*finite_solution}
    check('boundary_resolvent_Wronskian', sp.diff(wronskian, tortoise).subs(equation_rules)+squared_frequency*zero_solution*finite_solution)
    eigenvalue = sp.symbols('eigenvalue', positive=True)
    check('spectral_remainder_identity', squared_frequency*eigenvalue/(eigenvalue-squared_frequency)
          -squared_frequency-squared_frequency**2/(eigenvalue-squared_frequency))
    exact_impedance, approximate_impedance, outgoing = sp.symbols('Y_exact Y_approx Y_out')
    check('retarded_kernel_resolvent_identity', 1/(exact_impedance-outgoing)-1/(approximate_impedance-outgoing)
          -(approximate_impedance-exact_impedance)/((exact_impedance-outgoing)*(approximate_impedance-outgoing)))
    coordinate_time = sp.symbols('time', real=True)
    wave = sp.Function('wave')(coordinate_time, tortoise)
    energy = (sp.diff(wave, coordinate_time)**2+sp.diff(wave, tortoise)**2+wave_potential*wave**2)/2
    flux = -sp.diff(wave, coordinate_time)*sp.diff(wave, tortoise)
    check('local_positive_wave_energy_identity', (sp.diff(energy, coordinate_time)+sp.diff(flux, tortoise)).subs(
        sp.diff(wave, coordinate_time, 2), sp.diff(wave, tortoise, 2)-wave_potential*wave))
    dimensionless_frequency = sp.symbols('k', real=True)
    flat_inner = 3-dimensionless_frequency**2/7-dimensionless_frequency**4/441
    flat_spherical = (3/dimensionless_frequency**3-1/dimensionless_frequency)*sp.sin(dimensionless_frequency)-3*sp.cos(dimensionless_frequency)/dimensionless_frequency**2
    flat_exact = 1+dimensionless_frequency*sp.diff(flat_spherical, dimensionless_frequency)/flat_spherical
    check('flat_impedance_expansion', sp.series(flat_exact-flat_inner, dimensionless_frequency, 0, 6).removeO())
    report = {'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'checks': checks,
              'pressure_positivity': 'p_prime+A(r)p=-B(r), p(R)=0; B=M*rho/(r^2 F)+2F*h_prime^2/r>=0, hence p>=0 and N>=N0.',
              'Dirichlet_gap': 'A_D=-d_rstar^2+V on regular center to R with zero endpoints: lambda1>=3*N0^2/R^2 for ell2.',
              'boundary_identity': 'm(s)=m(0)-s*I0-s^2*<u0,(A_D-s)^(-1)u0>, I0=int u0^2 drstar, u0(R)=1.',
              'bound': '0<=m0-s*I0-m(s)<=s^2*I0/(lambda_lower-s), 0<=s<lambda_lower.',
              'kernel_bound': '|K_exact-K_quad|<=B/[|D_quad|*(|D_quad|-B)] if |D_quad|>B, D_quad=m0-s*I0-mout.',
              'energy_statement': 'Regular finite-energy solutions obey positive wave energy conservation with outward flux; no exponentially growing axial mode under stated background and boundary assumptions.',
              'scope': 'Linear nonrotating odd-parity sector. Not a claim of stability of every condensate sector or absence of damped quasinormal modes.'}
    output = ROOT/'results/bounds/status.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf-8') as handle:
        json.dump(report, handle, indent=2)
    print(json.dumps({'state': 'complete', 'exact_checks': len(checks)}))


if __name__ == '__main__':
    main()
