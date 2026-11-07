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
    checks = []

    def exact(name, expression):
        reduced = sp.factor(expression)
        assert reduced == 0, (name, reduced)
        checks.append({'name': name, 'passed': True})

    radius, orbit, mass, particle, harmonic = sp.symbols('r D M mu Ybar', positive=True)
    azimuth, master, slope = sp.symbols('m Z Ystar', real=True)
    metric = 1-2*mass/radius
    angular_speed_squared = mass/orbit**3
    velocity = 1/sp.sqrt(1-3*mass/orbit)
    common = 8*sp.pi*particle*velocity*harmonic
    source_trace = -metric*common/radius**2
    source_flat = common*angular_speed_squared
    source_sharp = common*angular_speed_squared*radius**2*(3-azimuth**2)/6
    large_lambda = 4+6*mass/radius
    polynomial = 8+12*mass/radius+84*mass**2/radius**2
    raw_derivative = metric*(-2*radius**2*metric*source_trace)/(3*large_lambda)
    raw_delta = metric*(-source_sharp/radius+(-2*radius**2*metric*sp.diff(source_trace, radius)
                   +2*radius*metric*source_flat+radius*polynomial*source_trace/large_lambda)/(3*large_lambda))
    metric_orbit = metric.subs(radius, orbit)
    derivative = raw_derivative.subs(radius, orbit)
    delta = (raw_delta-sp.diff(raw_derivative, radius)).subs(radius, orbit)
    jump_value = sp.factor(derivative/metric_orbit**2)
    jump_slope = sp.factor(delta/metric_orbit+derivative*sp.diff(metric, radius).subs(radius, orbit)/metric_orbit**2)
    old_slope = -common*(12*orbit**3-16*orbit**2*mass-24*orbit*mass**2-33*mass**3)/(6*orbit**2*(2*orbit+3*mass)**2)
    exact('general_source_value_jump', jump_value-common*(orbit-2*mass)/(3*(2*orbit+3*mass)))
    exact('general_source_slope_jump', jump_slope-old_slope-common*mass*(azimuth**2-4)/(6*orbit**2))
    exact('angular_source_conservation_all_m', -azimuth**2*source_flat/3-2*source_sharp/radius**2+source_flat)
    potential = metric*(24*radius**3+24*mass*radius**2+36*mass**2*radius+18*mass**3)/(radius**3*(2*radius+3*mass)**2)
    angular_coefficient = (6*radius**2+6*mass*radius+6*mass**2)/(radius**2*(2*radius+3*mass))
    angular = angular_coefficient*master+slope
    angular_prime = sp.diff(angular_coefficient, radius)*master+angular_coefficient*slope/metric+(potential-azimuth**2*angular_speed_squared)*master/metric
    lapse = (2+3*mass/radius)/metric*(3*master/radius-angular)+radius*angular_prime
    helical = sp.factor((metric*lapse+radius**2*angular_speed_squared*angular).subs(radius, orbit)*harmonic)
    overlap = jump_slope*master-jump_value*slope
    exact('metric_source_reciprocity', helical+3*overlap/(4*sp.pi*particle*velocity))
    tidal_lambda = sp.symbols('lambda', positive=True)
    leading_common = 8*sp.pi*particle*harmonic
    growing = sp.Matrix([orbit**3/6, orbit**2/2])
    decaying = sp.Matrix([orbit**-2, -2*orbit**-3])
    leading_a, leading_b = leading_common/6, -leading_common/(2*orbit)
    determinant = sp.det(sp.Matrix.hstack(growing, decaying))
    incident = (leading_b*decaying[0]-leading_a*decaying[1])/determinant
    induced_master = 3*tidal_lambda*incident*decaying
    induced_helical = harmonic*induced_master[0]/orbit
    static_y_squared = sp.Rational(5, 16)/sp.pi
    rotating_y_squared = sp.Rational(15, 32)/sp.pi
    zero_helical = sp.factor(induced_helical.subs(harmonic**2, static_y_squared))
    pair_helical = sp.factor(2*induced_helical.subs(harmonic**2, rotating_y_squared))
    exact('static_m0_supplies_one_quarter', zero_helical-sp.Rational(3, 2)*tidal_lambda*particle/orbit**6)
    exact('rotating_pair_supplies_three_quarters', pair_helical-sp.Rational(9, 2)*tidal_lambda*particle/orbit**6)
    exact('metric_action_matches_static_tidal_action', particle*(zero_helical+pair_helical)/4-sp.Rational(3, 2)*tidal_lambda*particle**2/orbit**6)
    field, source, stiffness = sp.symbols('field source stiffness', nonzero=True)
    quadratic_action = -stiffness*field**2/2+source*field
    exact('integrating_out_gives_half_interaction', quadratic_action.subs(field, source/stiffness)-source**2/(2*stiffness))
    omega = sp.symbols('Omega', positive=True)
    total, reduced = mass+particle, mass*particle/(mass+particle)
    reference_radius = (total/omega**2)**sp.Rational(1, 3)
    radial_shift = 3*tidal_lambda*particle/(mass*reference_radius**4)
    lagrangian = reduced*radius**2*omega**2/2+mass*particle/radius+sp.Rational(3, 2)*tidal_lambda*particle**2/radius**6
    radial_point = sp.diff(lagrangian.subs(tidal_lambda, 0), radius)
    radial_tide = sp.diff(lagrangian-lagrangian.subs(tidal_lambda, 0), radius)
    exact('fixed_frequency_radius_shift', sp.diff(radial_point, radius).subs(radius, reference_radius)*radial_shift+radial_tide.subs(radius, reference_radius))
    circular_action = sp.Rational(3, 2)*tidal_lambda*particle**2/reference_radius**6
    angular_momentum = sp.diff(circular_action, omega)
    energy = omega*angular_momentum-circular_action
    exact('fixed_frequency_energy', energy-sp.Rational(9, 2)*tidal_lambda*particle**2/reference_radius**6)
    exact('fixed_frequency_angular_momentum', angular_momentum-6*tidal_lambda*particle**2/(omega*reference_radius**6))
    exact('circular_first_law', sp.diff(energy, omega)-omega*sp.diff(angular_momentum, omega))
    quadrupole_fraction = 2*radial_shift/reference_radius+3*tidal_lambda*particle/(reduced*reference_radius**5)
    flux_fraction = 2*quadrupole_fraction
    exact('corrected_total_quadrupole_flux', flux_fraction-6*tidal_lambda*(1+3*particle/mass)/reference_radius**5)
    point_energy = -reduced*(total*omega)**sp.Rational(2, 3)/2
    energy_slope_fraction = sp.factor(sp.diff(energy, omega)/sp.diff(point_energy, omega))
    exact('binding_energy_slope_fraction', energy_slope_fraction+54*tidal_lambda*particle/(mass*reference_radius**5))
    chirp_fraction = sp.factor(flux_fraction-energy_slope_fraction)
    exact('consistent_tidal_chirp', chirp_fraction-6*tidal_lambda*(1+12*particle/mass)/reference_radius**5)
    point_chirp = sp.Rational(96, 5)*reduced*total**sp.Rational(2, 3)*omega**sp.Rational(11, 3)
    phase_derivative = sp.factor(-2*omega*chirp_fraction/point_chirp)
    phase_primitive = -sp.Rational(3, 8)*tidal_lambda*(1+12*particle/mass)*omega**sp.Rational(5, 3)/(reduced*total**sp.Rational(7, 3))
    exact('time_domain_phase_difference', sp.diff(phase_primitive, omega)-phase_derivative)
    symmetric_ratio = reduced/total
    effective_lambda = sp.Rational(16, 13)*(mass+12*particle)*tidal_lambda/(mass*total**5)
    fourier_phase = -sp.Rational(117, 256)/symmetric_ratio*effective_lambda*(total*omega)**sp.Rational(5, 3)
    exact('Fourier_phase_second_derivative_balance', sp.diff(fourier_phase, omega, 2)+2*chirp_fraction/point_chirp)
    exact('independent_published_leading_tidal_energy', energy-reduced*(total*omega)**sp.Rational(2, 3)*sp.Rational(9, 2)*particle/mass*tidal_lambda/reference_radius**5)
    exact('independent_published_leading_tidal_flux', flux_fraction-6*(3-2*mass/total)/(mass/total)*tidal_lambda/reference_radius**5)
    report = {'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'checks': checks, 'general_value_jump': str(jump_value), 'general_slope_jump': str(jump_slope),
              'helical_metric': str(helical), 'radial_shift': str(radial_shift), 'tidal_action': str(circular_action),
              'energy': str(energy), 'angular_momentum': str(angular_momentum), 'flux_fraction': str(sp.factor(flux_fraction)),
              'chirp_fraction': str(chirp_fraction), 'phase_primitive': str(phase_primitive),
              'fourier_phase': str(sp.factor(fourier_phase)),
              'scope': 'Relativistic polar-quadrupole source/action identities plus a separate leading Newtonian adiabatic two-body tidal expansion. No mixing of PN orders.'}
    (output/'status.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'checks': len(checks), 'source_slope': str(jump_slope), 'chirp': str(chirp_fraction)}))


if __name__ == '__main__':
    main()
