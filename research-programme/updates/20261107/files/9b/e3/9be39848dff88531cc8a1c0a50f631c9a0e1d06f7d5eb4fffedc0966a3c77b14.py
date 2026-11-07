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
    output = ROOT/'results/derivation'
    output.mkdir(parents=True, exist_ok=False)
    radius, orbit, mass, particle, angular_value = sp.symbols('r D M mu Ybar', positive=True)
    sigma, master, master_star_prime = sp.symbols('sigma Z Ystar')
    metric = 1-2*mass/radius
    metric_orbit = metric.subs(radius, orbit)
    omega_squared = mass/orbit**3
    time_velocity = 1/sp.sqrt(1-3*mass/orbit)
    source_constant = 8*sp.pi*particle*time_velocity*angular_value
    source_tt = source_constant/radius**2
    source_flat = source_constant*omega_squared
    source_sharp = -source_constant*omega_squared*radius**2/6
    source_trace = -metric*source_tt
    large_lambda = 4+6*mass/radius
    polynomial = 8+12*mass/radius+84*mass**2/radius**2
    raw_derivative = sp.factor(metric*(-2*radius**2*metric*source_trace)/(3*large_lambda))
    raw_delta = sp.factor(metric*(-source_sharp/radius+(-2*radius**2*metric*sp.diff(source_trace, radius)
                            +2*radius*metric*source_flat+radius*polynomial*source_trace/large_lambda)/(3*large_lambda)))
    derivative = sp.factor(raw_derivative.subs(radius, orbit))
    delta = sp.factor((raw_delta-sp.diff(raw_derivative, radius)).subs(radius, orbit))
    jump_value = sp.factor(derivative/metric_orbit**2)
    jump_slope = sp.factor(delta/metric_orbit+derivative*sp.diff(metric, radius).subs(radius, orbit)/metric_orbit**2)
    checks = []

    def exact(name, expression):
        assert sp.simplify(expression) == 0, (name, sp.simplify(expression))
        checks.append({'name': name, 'passed': True})

    exact('circular_four_velocity_normalization', (-metric_orbit+orbit**2*omega_squared)*time_velocity**2+1)
    exact('radial_geodesic_equation', time_velocity**2*metric_orbit*(mass/orbit**2-orbit*omega_squared))
    exact('projected_time_conservation', -2*sp.I*sp.sqrt(omega_squared)*source_tt-3/radius**2*(-2*sp.I*source_constant*sp.sqrt(omega_squared)/3))
    exact('projected_radial_conservation', (mass*metric*source_tt/radius**2-metric*source_flat/radius).subs(radius, orbit))
    exact('projected_angular_conservation', -4*source_constant*omega_squared/3-2*source_sharp/radius**2+source_flat)
    energy = metric_orbit*time_velocity
    momentum_squared = mass*orbit/(1-3*mass/orbit)
    small_lambda = 2+3*mass/radius
    potential_squared = metric*(1+momentum_squared/radius**2)
    martel_derivative = 8*sp.pi*particle*angular_value/3*metric**2*potential_squared/(small_lambda*energy)
    martel_scalar = 8*sp.pi*particle*angular_value/3*metric**2/(radius*small_lambda**2)*(6*mass/radius*energy-small_lambda/energy*(3-3*mass/radius+momentum_squared/radius**2*(5-7*mass/radius)))
    martel_trace = 8*sp.pi*particle*angular_value/3*momentum_squared/energy*metric**3/(radius**3*small_lambda)
    martel_tensor = -4*sp.pi*particle*angular_value/3*momentum_squared/energy*metric**2/radius**3
    martel_delta = martel_scalar+martel_trace-martel_tensor
    exact('independent_Martel_derivative_source', derivative-martel_derivative.subs(radius, orbit))
    exact('independent_Martel_canonical_delta_source', delta-(martel_delta-sp.diff(martel_derivative, radius)).subs(radius, orbit))
    angular_metric = (6*radius**2+6*mass*radius+6*mass**2)/(radius**2*(2*radius+3*mass))*master+master_star_prime
    shift = (2*radius**2-6*mass*radius-3*mass**2)/((radius-2*mass)*(2*radius+3*mass))*master+radius/metric*master_star_prime
    lapse_prime = mass/(radius**2*metric)
    master_definition = radius/3*(angular_metric+metric/small_lambda*((1-radius*lapse_prime)*angular_metric-3*shift/radius))
    exact('parent_master_is_Zerilli_Moncrief_normalization', master_definition-master)
    function_value, function_prime, delta_coeff, derivative_coeff = sp.symbols('test_value test_prime G Fdelta')
    metric_prime = sp.diff(metric, radius).subs(radius, orbit)
    torture_a = derivative_coeff/metric_orbit**2
    torture_b = delta_coeff/metric_orbit+derivative_coeff*metric_prime/metric_orbit**2
    exact('distribution_change_of_radial_coordinate', torture_b*function_value-torture_a*metric_orbit*function_prime
          -(delta_coeff*function_value/metric_orbit-derivative_coeff*(function_prime/metric_orbit-function_value*metric_prime/metric_orbit**2)))
    inside, inside_slope, outside, outside_slope, jump_a, jump_b = sp.symbols('U Ustar V Vstar a b')
    wronskian = inside*outside_slope-inside_slope*outside
    outward_coefficient = (jump_b*inside-jump_a*inside_slope)/wronskian
    inward_coefficient = (jump_b*outside-jump_a*outside_slope)/wronskian
    exact('derived_value_jump', outward_coefficient*outside-inward_coefficient*inside-jump_a)
    exact('derived_slope_jump', outward_coefficient*outside_slope-inward_coefficient*inside_slope-jump_b)
    reference, reference_slope = sp.symbols('H Hstar')
    reference_wronskian = reference*outside_slope-reference_slope*outside
    reference_coefficient = (jump_b*reference-jump_a*reference_slope)/reference_wronskian
    excess = -(inside*reference_slope-inside_slope*reference)*(jump_b*outside-jump_a*outside_slope)/(wronskian*reference_wronskian)
    exact('stable_physical_reference_difference', outward_coefficient-reference_coefficient-excess)
    source_amplitude, tidal_lambda = sp.symbols('source_amplitude lambda_tide')
    growing, growing_prime = orbit**3/6, orbit**2/2
    decaying, decaying_prime = orbit**(-2), -2*orbit**(-3)
    leading_jump_value, leading_jump_slope = source_amplitude/6, -source_amplitude/(2*orbit)
    numerator_growing = leading_jump_slope*growing-leading_jump_value*growing_prime
    numerator_decaying = leading_jump_slope*decaying-leading_jump_value*decaying_prime
    exact('leading_tidal_wave_amplitude_fraction', 3*tidal_lambda*numerator_decaying/numerator_growing-3*tidal_lambda/orbit**5)
    leading_wave = -source_amplitude*orbit**2*(4*mass/orbit**3)/15
    leading_wave = leading_wave.subs(source_amplitude, 8*sp.pi*particle*sp.sqrt(15/(32*sp.pi)))
    pair_power = sp.Rational(3, 4)/sp.pi*(4*mass/orbit**3)*leading_wave**2
    exact('Newton_quadrupole_wave_flux_normalization', pair_power-sp.Rational(32, 5)*particle**2*mass**3/orbit**5)
    report = {'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'checks': checks, 'canonical_radial_delta': str(delta), 'canonical_radial_delta_derivative': str(derivative),
              'master_value_jump': str(jump_value), 'master_tortoise_derivative_jump': str(jump_slope),
              'source_constant': str(source_constant), 'scope': 'Circular equatorial test companion, ell=m=2, unit-normalized harmonics. Geometric companion mass mu=G_R*m_comp. First order in mass ratio; Einstein sector retained.'}
    (output/'status.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
