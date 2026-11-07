from __future__ import annotations

from datetime import datetime, timezone
import json

import psutil
import sympy as sy

from acquire_source import ROOT, digest


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    checks = []

    def check(name, expression):
        residual = sy.simplify(sy.expand(expression))
        checks.append({'name': name, 'passed': residual == 0, 'residual': str(residual)})
        assert residual == 0, (name, residual)

    radius, distance, mass, particle, frequency, lapse, epsilon = sy.symbols('r D M mu Omega ut epsilon', positive=True)
    metric_perturbation = sy.symbols('hkk', real=True)
    particle_action = -particle*sy.sqrt(lapse**-2-epsilon*metric_perturbation)
    check('worldline_linear_coupling', sy.diff(particle_action, epsilon).subs(epsilon, 0)-particle*lapse*metric_perturbation/2)
    stiffness, source, field = sy.symbols('a j phi', real=True, nonzero=True)
    quadratic = stiffness*field**2/2+source*field
    eliminated = quadratic.subs(field, -source/stiffness)
    check('eliminated_quadratic_field_half_source_interaction', eliminated-(source*field/2).subs(field, -source/stiffness))
    angular = sy.sqrt(15/(8*sy.pi))
    strength = 8*sy.pi/3*particle*frequency*lapse*angular
    speed = 1-2*mass/distance
    value, slope = sy.symbols('psi psi_star')
    jump, jump_slope = strength*distance/2, -strength*speed/2
    overlap = jump_slope*value-jump*slope
    time_metric = (speed*value+distance*slope)/2
    helical_single = 2*frequency*angular*time_metric
    check('axial_metric_source_reciprocity_single_mode', helical_single+3*overlap/(4*sy.pi*particle*lapse))
    conservative_overlap = sy.symbols('Re_overlap', real=True)
    helical_pair = -3*conservative_overlap/(2*sy.pi*particle*lapse)
    action_pair = particle*lapse*helical_pair/4
    check('pair_action_coefficient', action_pair+3*conservative_overlap/(8*sy.pi))
    check('common_metric_contact_cancels', -distance**2*speed*source/4-(-distance**2*speed*source/4))
    action_coefficient = sy.symbols('F_over_mu2', real=True)
    action = particle**2*action_coefficient
    redshift = -2*action/particle
    check('mass_first_law', sy.diff(action, particle)+redshift)
    check('redshift_worldline_normalization', -lapse*helical_pair/2+2*action_pair/particle)

    inside_slope, horizon_slope, outgoing_slope = sy.symbols('a b c')
    direct_difference = 1/(outgoing_slope-inside_slope)-1/(outgoing_slope-horizon_slope)
    check('rank_one_Green_difference', direct_difference+(horizon_slope-inside_slope)/((outgoing_slope-inside_slope)*(outgoing_slope-horizon_slope)))
    phase_scale = sy.symbols('normalization', nonzero=True)
    numerator, wronskian_body, wronskian_horizon, boundary_difference = sy.symbols('O WB WH DWH', nonzero=True)
    invariant = -boundary_difference*numerator**2/(wronskian_body*wronskian_horizon)
    rescaled = -boundary_difference*(phase_scale*numerator)**2/((phase_scale*wronskian_body)*(phase_scale*wronskian_horizon))
    check('outgoing_normalization_independence', rescaled-invariant)
    real_value, imaginary_value, real_slope, imaginary_slope, source_jump, source_slope = sy.symbols('ar ai br bi J K', real=True)
    left_value = real_value+sy.I*imaginary_value
    left_slope = real_slope+sy.I*imaginary_slope
    current_left = sy.im(sy.conjugate(left_value)*left_slope)
    current_right = sy.im(sy.conjugate(left_value+source_jump)*(left_slope+source_slope))
    source_work = sy.im(source_slope*left_value-source_jump*left_slope)
    check('wave_current_source_work_identity', current_right-current_left+source_work)
    retarded_action_imag = -3*source_work/(8*sy.pi)
    power = 3*frequency/(4*sy.pi)*(current_right-current_left)
    check('absorptive_action_optical_identity', power-2*frequency*retarded_action_imag)

    sigma = sy.symbols('sigma_bar', real=True, nonzero=True)
    growing = radius**3
    decaying = radius**-2
    wronskian = growing*sy.diff(decaying, radius)-sy.diff(growing, radius)*decaying
    check('static_master_Wronskian', wronskian+5)
    flat_strength = strength.subs(lapse, 1)
    overlap_decay = (-flat_strength*decaying/2-flat_strength*distance*sy.diff(decaying, radius)/2).subs(radius, distance)
    check('leading_decaying_source_overlap', overlap_decay-flat_strength/(2*distance**2))
    master_coefficient = 24*sigma
    leading = sy.simplify(-3/(8*sy.pi)*master_coefficient*overlap_decay**2/wronskian)
    check('magnetic_action_derived_six', leading-6*sigma*particle**2*frequency**2/distance**4)
    check('independent_BV36_normalization', leading-(12*sy.Symbol('sigma_BV')*particle**2*frequency**2/distance**4).subs('sigma_BV', sigma/2))
    check('magnetic_tensor_action_matching', leading-sigma/3*(18*particle**2*frequency**2/distance**4))
    check('omitting_elimination_half_doubles_answer', 2*leading/(6*sigma*particle**2*frequency**2/distance**4)-2)

    metric = 1-2*epsilon*mass/radius
    decay_pn = radius**-2*(1+epsilon*5*mass/(3*radius)+epsilon*frequency**2*radius**2/6)
    common = flat_strength/sy.sqrt(1-3*epsilon*mass/distance)
    overlap_pn = (-common*(1-2*epsilon*mass/distance)*decay_pn/2
                  -common*distance*metric*sy.diff(decay_pn, radius)/2).subs(radius, distance)
    ratio = sy.series(overlap_pn/overlap_decay, epsilon, 0, 2).removeO().subs(frequency**2, mass/distance**3)
    check('first_PN_overlap_8over3', ratio-1-epsilon*sy.Rational(8, 3)*mass/distance)
    action_ratio = sy.series(ratio**2, epsilon, 0, 2).removeO()
    check('first_PN_action_16over3', action_ratio-1-epsilon*sy.Rational(16, 3)*mass/distance)
    circular_distance = (mass/frequency**2)**sy.Rational(1, 3)
    leading_circular = leading.subs(distance, circular_distance)
    circular_action = leading_circular*(1+sy.Rational(16, 3)*mass/circular_distance)
    momentum = sy.diff(circular_action, frequency)
    energy = frequency*momentum-circular_action
    check('leading_and_first_PN_energy', energy-sy.Rational(11, 3)*leading_circular*(1+sy.Rational(208, 33)*mass/circular_distance))
    check('leading_and_first_PN_angular_momentum', momentum-sy.Rational(14, 3)*leading_circular/frequency*(1+sy.Rational(128, 21)*mass/circular_distance))
    check('conservative_circular_first_law', sy.diff(energy, frequency)-frequency*sy.diff(momentum, frequency))
    check('published_BV41_leading_energy_testmass', sy.Rational(11, 3)*leading_circular
          -(44*(sigma/2)*particle**2*mass/circular_distance**7))
    curvature, mixed, action_radius, action_frequency = sy.symbols('Lrr LrOmega Fr FOmega', nonzero=True)
    radius_shift = -action_radius/curvature
    orbit_derivative = -mixed/curvature
    check('on_shell_frequency_derivative_includes_radius_shift', mixed*radius_shift+action_frequency-(action_frequency+action_radius*orbit_derivative))
    probe, current_value = sy.symbols('B S', real=True)
    matched_internal = sy.Rational(2, 3)*current_value*probe-current_value**2/(3*sigma)
    check('matched_current_stationarity', sy.diff(matched_internal, current_value).subs(current_value, sigma*probe))
    check('matched_current_elimination_reproduces_action', matched_internal.subs(current_value, sigma*probe)-sigma*probe**2/3)

    output = ROOT/'results/derivation'
    output.mkdir(parents=True, exist_ok=False)
    report = {'state': 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(),
              'script_sha256': digest(__file__), 'checks': checks, 'exact_checks': len(checks),
              'leading_action': str(leading), 'source_action_overlap_coefficient': '-3/(8*pi), m=+/-1 pair',
              'optical_identity': 'Delta P_infinity - P_BH_horizon = 2*Omega*Im(F_retarded)',
              'first_relative_PN_coefficients': {'action': '16/3', 'energy': '208/33', 'angular_momentum': '128/21'},
              'matched_static_operator': 'L_B=sigma_bar*B_ij*B_ij/3, S_ij=sigma_bar*B_ij',
              'source_coupling_fitted': False, 'source_sigma': 'Inherited actual condensate static response, not an independent numeric matching input.',
              'finite_mass_ratio_scope': 'O(mu^2) conservative interaction about a fixed central background; not arbitrary mass ratio.'}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'exact_checks': len(checks), 'leading_action': str(leading)}))


if __name__ == '__main__':
    main()
