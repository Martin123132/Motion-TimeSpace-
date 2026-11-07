from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import psutil
from scipy.integrate import quad
from scipy.optimize import brentq
import sympy as sp


ROOT = Path(__file__).resolve().parent


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/balance'
    output.mkdir(parents=True, exist_ok=False)
    checks = []

    def exact(name, expression):
        assert sp.simplify(expression) == 0, name
        checks.append({'name': name, 'passed': True})

    time, omega, strength = sp.symbols('t Omega Iamp', real=True)
    normal = sp.Matrix([sp.cos(omega*time), sp.sin(omega*time), 0])
    quadrupole = strength*(normal*normal.T-sp.eye(3)/3)
    third = quadrupole.diff(time, 3)
    exact('explicit_STF_wave_power', sp.trace(third.T*third)/5-sp.Rational(32, 5)*strength**2*omega**6)
    second = quadrupole.diff(time, 2)
    torque = sp.Rational(2, 5)*sum(second[0, index]*third[1, index]-second[1, index]*third[0, index] for index in range(3))
    exact('explicit_wave_energy_angular_momentum_balance', torque-sp.Rational(32, 5)*strength**2*omega**5)
    particle, ut, unit_helical = sp.symbols('mu ut hkk_per_mu', real=True)
    action = particle**2*ut*unit_helical/4
    delta_redshift = -particle*ut*unit_helical/2
    exact('redshift_mass_first_law', sp.diff(action, particle)+delta_redshift)
    function = sp.Function('F')(omega)
    energy = omega*sp.diff(function, omega)-function
    momentum = sp.diff(function, omega)
    exact('nonlocal_frequency_dependent_circular_first_law', sp.diff(energy, omega)-omega*sp.diff(momentum, omega))
    input_path = ROOT/'results/fine/status.json'
    source = json.loads(input_path.read_text())
    mass, radius, tidal_lambda = (source[key] for key in ['mass', 'radius', 'tidal_lambda'])
    algebra_controls = []
    for mass_ratio in [.001, .01]:
        companion = mass_ratio*mass
        total = mass+companion
        reduced = mass*companion/total
        orbit_zero = 2*radius
        frequency = np.sqrt(total/orbit_zero**3)
        baseline_chirp = 96/5*reduced*total**(2/3)*frequency**(11/3)
        baseline_energy = -reduced*total/(2*orbit_zero)
        for coefficient in [1., .5, .25]:
            deformability = coefficient*tidal_lambda
            interaction = 1.5*deformability*companion**2
            circular_radius = orbit_zero*brentq(lambda ratio: ratio-ratio**-2-9*deformability*companion/(mass*orbit_zero**5)*ratio**-7,
                                              1., 2., xtol=5e-15, rtol=1e-14)
            omega_squared_prime = -3*total/circular_radius**4-48*interaction/(reduced*circular_radius**9)
            omega_prime = omega_squared_prime/(2*frequency)
            energy_value = .5*reduced*circular_radius**2*frequency**2-mass*companion/circular_radius-interaction/circular_radius**6
            energy_prime = .5*reduced*(2*circular_radius*frequency**2+circular_radius**2*omega_squared_prime)+mass*companion/circular_radius**2+6*interaction/circular_radius**7
            momentum_prime = reduced*(2*circular_radius*frequency+circular_radius**2*omega_prime)
            amplitude = reduced*circular_radius**2+3*deformability*companion/circular_radius**3
            power = 32/5*frequency**6*amplitude**2
            chirp = -power*omega_prime/energy_prime
            predicted_fraction = 6*deformability*(1+12*mass_ratio)/orbit_zero**5
            predicted_energy = 4.5*deformability*companion**2/orbit_zero**6
            algebra_controls.append({'mass_ratio': mass_ratio, 'lambda_multiplier': coefficient,
                                     'radius_over_reference': circular_radius/orbit_zero,
                                     'nonlinear_chirp_excess': chirp/baseline_chirp-1,
                                     'linear_chirp_excess': predicted_fraction,
                                     'chirp_linear_remainder': chirp/baseline_chirp-1-predicted_fraction,
                                     'energy_linear_remainder': energy_value-baseline_energy-predicted_energy,
                                     'first_law_relative_residual': abs(energy_prime/(frequency*momentum_prime)-1),
                                     'interpretation': 'Algebraic test of the truncated Newtonian action, not an added nonlinear-physics prediction.'})
    phase_rows = []
    for mass_ratio in [.001, .01]:
        companion = mass_ratio*mass
        total = mass+companion
        reduced = mass*companion/total
        for outer, inner in [(20., 10.), (10., 5.)]:
            omega_initial, omega_final = np.sqrt(total/(outer*radius)**3), np.sqrt(total/(inner*radius)**3)

            def chirp_point(frequency):
                return 96/5*reduced*total**(2/3)*frequency**(11/3)

            def delta_integrand(frequency):
                orbit = (total/frequency**2)**(1/3)
                return -2*frequency/chirp_point(frequency)*6*tidal_lambda*(1+12*mass_ratio)/orbit**5

            numeric, quadrature_error = quad(delta_integrand, omega_initial, omega_final, epsabs=1e-9, epsrel=2e-12)
            analytic = -3/8*tidal_lambda*(1+12*mass_ratio)/(reduced*total**(7/3))*(omega_final**(5/3)-omega_initial**(5/3))
            baseline_phase = 1/(16*reduced*total**(2/3))*(omega_initial**(-5/3)-omega_final**(-5/3))
            endpoint_fraction = 6*tidal_lambda*(1+12*mass_ratio)/(inner*radius)**5
            phase_rows.append({'illustrative_mass_ratio_not_fitted': mass_ratio, 'outer_separation_over_radius': outer,
                               'inner_separation_over_radius': inner, 'delta_GW_phase_radians': analytic,
                               'point_GW_cycles': baseline_phase/(2*np.pi), 'delta_GW_cycles': analytic/(2*np.pi),
                               'quadrature_relative_error': abs(numeric/analytic-1), 'quadrature_reported_absolute_error': quadrature_error,
                               'endpoint_leading_chirp_fraction': endpoint_fraction,
                               'scope': 'Leading adiabatic Newtonian electric-quadrupole phase between fixed frequency endpoints; dimensionless illustration, no astrophysical mass calibration or detector prediction.'})
    report = {'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'input_hashes': {str(input_path): hashlib.sha256(input_path.read_bytes()).hexdigest()},
              'checks': checks, 'nonlinear_algebra_controls': algebra_controls, 'phase_illustrations': phase_rows}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
