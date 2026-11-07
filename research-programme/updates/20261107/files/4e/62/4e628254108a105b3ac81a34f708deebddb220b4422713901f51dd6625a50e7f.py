from __future__ import annotations

from datetime import datetime, timezone
import sympy as sp

from sidebands import ROOT, symbolic_coefficients, digest, write_json, modest_process


def main():
    modest_process()
    checks = []

    def exact(name, expression):
        value = sp.factor(sp.cancel(expression))
        assert value == 0, (name, value)
        checks.append({'name': name, 'residual': str(value), 'passed': True})

    semilatus, mass = sp.symbols('p M', positive=True)
    eccentricity, cosine = sp.symbols('e cosine', real=True)
    time_rate = mass*semilatus**2*sp.sqrt((semilatus-2)**2-4*eccentricity**2)/((semilatus-2-2*eccentricity*cosine)*(1+eccentricity*cosine)**2*sp.sqrt(semilatus-6-2*eccentricity*cosine))
    phase_rate = sp.sqrt(semilatus/(semilatus-6-2*eccentricity*cosine))
    time_modulation = 2/(semilatus-2)-2+1/(semilatus-6)
    exact('Darwin time Jacobian first variation', (sp.diff(time_rate, eccentricity)/time_rate).subs(eccentricity, 0)-time_modulation*cosine)
    exact('Darwin azimuth Jacobian first variation', (sp.diff(phase_rate, eccentricity)/phase_rate).subs(eccentricity, 0)-cosine/(semilatus-6))
    phase_wobble = 2*sp.sqrt(semilatus/(semilatus-6))*(semilatus-3)/(semilatus-2)
    exact('coordinate-time phase wobble after inversion', sp.sqrt(semilatus/(semilatus-6))*(1/(semilatus-6)-time_modulation)-phase_wobble)
    energy_squared = ((semilatus-2)**2-4*eccentricity**2)/(semilatus*(semilatus-3-eccentricity**2))
    angular_squared = mass**2*semilatus**2/(semilatus-3-eccentricity**2)
    exact('no linear energy drift at fixed p', sp.diff(energy_squared, eccentricity).subs(eccentricity, 0))
    exact('no linear angular drift at fixed p', sp.diff(angular_squared, eccentricity).subs(eccentricity, 0))
    arguments, expressions = symbolic_coefficients('polar')
    radius, mass_symbol, energy, angular, azimuth, frequency, harmonic_value = arguments
    velocity = sp.symbols('v', real=True)
    metric = 1-2*mass_symbol/radius
    metric_prime = sp.diff(metric, radius)
    small_lambda = 2+3*mass_symbol/radius
    lambda_prime = sp.diff(small_lambda, radius)
    speed = metric*angular/(energy*radius**2)
    strength = 8*sp.pi*energy*harmonic_value/metric
    trace = strength*(velocity**2/metric-metric)/radius**2
    trace_radial_fixed = strength*(-velocity**2*metric_prime/metric**2-metric_prime)/radius**2-2*trace/radius
    qrr = strength*velocity**2/radius**2
    qr = -sp.I*azimuth*strength*speed*velocity/3
    qflat = strength*speed**2
    qsharp = strength*radius**2*speed**2*(3-azimuth**2)/6
    polynomial = 8+12*mass_symbol/radius+84*mass_symbol**2/radius**2
    raw_F = strength*metric*(metric**2-velocity**2)/(3*small_lambda)
    auxiliary_F_prime = strength/(3*small_lambda)*(metric_prime*(3*metric**2-velocity**2)-metric*(metric**2-velocity**2)*lambda_prime/small_lambda)
    raw_G = metric*(2*qr/small_lambda-qsharp/radius+(-2*radius**2*metric*trace_radial_fixed+12*mass_symbol*qrr/small_lambda+2*radius*metric*qflat+radius*polynomial*trace/(2*small_lambda))/(6*small_lambda))
    source_delta = (raw_G-auxiliary_F_prime)/metric+raw_F*metric_prime/metric**2
    source_prime = raw_F/metric**2
    exact('polar reduced constant coefficient', source_delta.subs(velocity, 0)-expressions[0])
    exact('polar reduced delta-prime coefficient', source_prime.subs(velocity, 0)-expressions[1])
    exact('polar linear-velocity coefficient', sp.diff(source_delta, velocity).subs(velocity, 0)-sp.I*expressions[2])
    exact('delta-prime has no linear velocity term', sp.diff(source_prime, velocity).subs(velocity, 0))
    anomaly = sp.symbols('tau', real=True)
    source_base, radial_derivative, velocity_derivative, orbit_radius, radial_frequency, phase_coefficient = sp.symbols('T Tr Tv r0 Omega_r kappa', real=True)
    first_order = -orbit_radius*radial_derivative*sp.cos(anomaly)+(orbit_radius*radial_frequency*velocity_derivative-sp.I*azimuth*phase_coefficient*source_base)*sp.sin(anomaly)
    for harmonic in [-1, 1]:
        calculated = sp.integrate(sp.expand_complex(sp.exp(sp.I*harmonic*anomaly)*first_order), (anomaly, 0, 2*sp.pi))/(2*sp.pi)
        expected = (-orbit_radius*radial_derivative+sp.I*harmonic*orbit_radius*radial_frequency*velocity_derivative+harmonic*azimuth*phase_coefficient*source_base)/2
        exact('signed first-sideband Fourier integral '+str(harmonic), calculated-expected)
    exact('no linear carrier change', sp.integrate(first_order, (anomaly, 0, 2*sp.pi)))
    exact('higher sideband absent at linear order', sp.integrate(sp.expand_complex(sp.exp(2*sp.I*anomaly)*first_order), (anomaly, 0, 2*sp.pi)))
    coefficient = mass*semilatus**sp.Rational(3, 2)*sp.sqrt(semilatus-6)/(2*(semilatus-2)*sp.sqrt(semilatus-3))
    logarithmic_derivative = sp.Rational(3, 2)/semilatus+sp.Rational(1, 2)/(semilatus-6)-1/(semilatus-2)-sp.Rational(1, 2)/(semilatus-3)
    exact('radial-action susceptibility derivative', sp.diff(coefficient, semilatus)-coefficient*logarithmic_derivative)
    squared, radial_rate_coefficient, circular_p_rate = sp.symbols('z R0 P0', real=True)
    damping = (radial_rate_coefficient-sp.diff(coefficient, semilatus)*circular_p_rate)/coefficient
    exact('near-circular damping from action chain rule', coefficient*squared*damping+sp.diff(coefficient, semilatus)*squared*circular_p_rate-squared*radial_rate_coefficient)
    newtonian_coefficient = mass*sp.sqrt(semilatus)/2
    newtonian_p_rate = -64/(5*mass**2*semilatus**3)
    newtonian_radial_rate = -352/(15*mass*semilatus**sp.Rational(7, 2))
    newtonian_damping = -608/(15*mass**2*semilatus**4)
    exact('Kepler quadrupole damping coefficient', (newtonian_radial_rate-sp.diff(newtonian_coefficient, semilatus)*newtonian_p_rate)/newtonian_coefficient-newtonian_damping)
    directory = ROOT/'results/derivation'
    directory.mkdir(parents=True, exist_ok=False)
    symbolic = {sector: [str(expression) for expression in symbolic_coefficients(sector)[1]] for sector in ['polar', 'odd']}
    write_json(directory/'status.json', {'state': 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(),
             'script_sha256': digest(__file__), 'input_hashes': {str(ROOT/'sidebands.py'): digest(ROOT/'sidebands.py')},
             'checks': checks, 'coefficient_arguments': [str(item) for item in arguments],
             'coefficients_order': ['a', 'c', 'd', 'partial_r_a_at_fixed_E_h', 'partial_r_c_at_fixed_E_h'],
             'coefficients': symbolic, 'phase_wobble': str(phase_wobble), 'action_coefficient': str(coefficient),
             'newtonian_damping': str(newtonian_damping), 'domain': 'p>6, M>0, stable circular exterior orbit, fixed p expansion'}, exclusive=True)
    print(len(checks), 'exact identities passed', flush=True)


if __name__ == '__main__':
    main()
