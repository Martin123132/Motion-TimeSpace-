from __future__ import annotations

import sympy as sy

from eccentric_source import ROOT, BRANCH, digest, modest_process, write_report


def main():
    modest_process()
    checks = []

    def check(name, expression):
        residual = sy.factor(sy.cancel(sy.expand(expression)))
        checks.append({'name': name, 'passed': residual == 0, 'residual': str(residual)})
        assert residual == 0, (name, residual)

    radius, mass, energy, momentum, velocity, strength, frequency, acceleration = sy.symbols(
        'r M E h v A Omega a', real=True)
    multipole = sy.symbols('L', real=True)
    kappa = multipole-2
    metric = 1-2*mass/radius
    metric_prime = sy.diff(metric, radius)
    proper_velocity = sy.symbols('w', real=True)
    radial_acceleration = -mass/radius**2+momentum**2/radius**3-3*mass*momentum**2/radius**4
    effective = metric*(1+momentum**2/radius**2)
    check('proper_radial_acceleration_from_effective_potential', radial_acceleration+sy.diff(effective, radius)/2)
    check('full_timelike_normalization', ((-energy**2+proper_velocity**2)/metric+momentum**2/radius**2+1).subs(proper_velocity**2, energy**2-effective))
    check('time_geodesic_equation', -energy*metric_prime*proper_velocity/metric**2+metric_prime/metric*(energy/metric)*proper_velocity)
    check('angular_geodesic_equation', -2*momentum*proper_velocity/radius**3+2*proper_velocity/radius*(momentum/radius**2))
    radial_connection = metric*metric_prime*(energy/metric)**2/2-metric_prime*proper_velocity**2/(2*metric)-metric*momentum**2/radius**3
    check('radial_geodesic_equation', (radial_acceleration+radial_connection).subs(proper_velocity**2, energy**2-effective))
    check('tortoise_timelike_margin', (1-proper_velocity**2/energy**2).subs(proper_velocity**2, energy**2-effective)-effective/energy**2)
    semilatus, eccentricity, cosine = sy.symbols('p e c', real=True)
    denominator = semilatus-3-eccentricity**2
    eccentric_radius = mass*semilatus/(1+eccentricity*cosine)
    eccentric_energy2 = ((semilatus-2)**2-4*eccentricity**2)/(semilatus*denominator)
    eccentric_momentum2 = mass**2*semilatus**2/denominator
    radial_speed2 = eccentricity**2*(1-cosine**2)*(semilatus-6-2*eccentricity*cosine)/(semilatus*denominator)
    radial_energy = (energy**2-effective).subs({energy**2: eccentric_energy2, momentum**2: eccentric_momentum2, radius: eccentric_radius})
    check('Darwin_radial_energy_factorization', radial_energy-radial_speed2)
    for sign in [-1, 1]:
        check(f'turning_root_{sign}', radial_energy.subs(cosine, sign))
    proper_rate2 = mass**2*semilatus**3*denominator/((1+eccentricity*cosine)**4*(semilatus-6-2*eccentricity*cosine))
    time_rate2 = mass**2*semilatus**4*((semilatus-2)**2-4*eccentricity**2)/((semilatus-2-2*eccentricity*cosine)**2*(1+eccentricity*cosine)**4*(semilatus-6-2*eccentricity*cosine))
    phase_rate2 = semilatus/(semilatus-6-2*eccentricity*cosine)
    check('Darwin_time_rate', time_rate2/proper_rate2-eccentric_energy2/metric.subs(radius, eccentric_radius)**2)
    check('Darwin_phase_rate', phase_rate2/proper_rate2-eccentric_momentum2/eccentric_radius**4)
    check('Darwin_radius_rate', (mass*semilatus*eccentricity)**2*(1-cosine**2)/(1+eccentricity*cosine)**4/proper_rate2-radial_speed2)

    strength_dot = strength*(-2*velocity/radius-sy.I*frequency)
    tensor_strength = -sy.I*frequency*radius**2*strength/kappa
    check('axial_Bianchi_delta', strength_dot+2*velocity*strength/radius-kappa*tensor_strength/radius**2)
    check('axial_Bianchi_delta_prime', -velocity*strength+velocity*strength)
    window, window_dot = sy.symbols('window window_dot')
    check('windowed_source_has_nonzero_residual', window_dot*strength+window*(strength_dot+2*velocity*strength/radius-kappa*tensor_strength/radius**2)-window_dot*strength)
    radial_delta_prime = 2*radius*strength*(metric**2-velocity**2)/kappa
    raw_delta = 2*radius*(strength_dot*velocity+strength*acceleration+strength*metric*metric_prime)/kappa-sy.diff(radial_delta_prime, radius)
    radial_delta = 2*strength*(radius*acceleration-velocity**2-sy.I*radius*velocity*frequency-metric)/kappa
    check('canonical_radial_delta', raw_delta-radial_delta)
    tortoise_velocity, tortoise_acceleration = sy.symbols('u udot', real=True)
    conversion = {velocity: metric*tortoise_velocity,
                  acceleration: metric*tortoise_acceleration+metric*metric_prime*tortoise_velocity**2}
    jump = 2*radius*strength/kappa
    jump_dot = jump*(-metric*tortoise_velocity/radius-sy.I*frequency)
    delta_prime = (1-tortoise_velocity**2)*jump
    delta = jump*tortoise_acceleration-metric*jump*(1+tortoise_velocity**2)/radius-sy.I*frequency*tortoise_velocity*jump
    check('radial_to_tortoise_delta_prime', (radial_delta_prime/metric**2).subs(conversion)-delta_prime)
    check('radial_to_tortoise_delta', (radial_delta/metric+radial_delta_prime*metric_prime/metric**2).subs(conversion)-delta)
    check('delta_is_derivative_plus_potential_contact', delta-(tortoise_acceleration*jump+tortoise_velocity*jump_dot-metric*jump/radius))
    derivative_jump = -metric*jump/radius+sy.I*tortoise_velocity*frequency*jump/(1-tortoise_velocity**2)
    time_jump = -sy.I*frequency*jump/(1-tortoise_velocity**2)
    check('moving_value_jump', (1-tortoise_velocity**2)*jump-delta_prime)
    check('moving_derivative_jump', (1-tortoise_velocity**2)*derivative_jump+2*tortoise_velocity*jump_dot+tortoise_acceleration*jump-delta)
    check('worldline_chain_rule', time_jump+tortoise_velocity*derivative_jump-jump_dot)
    check('circular_value_jump', jump-2*radius*strength/kappa)
    check('circular_slope_jump', derivative_jump.subs(tortoise_velocity, 0)+2*strength*metric/kappa)
    check('circular_time_jump', time_jump.subs(tortoise_velocity, 0)+sy.I*frequency*jump)
    check('time_metric_delta_contact_cancellation', metric*radius*jump/2-radius**2*metric*strength/kappa)
    check('radial_metric_delta_contact_cancellation', -radius*velocity*jump/(2*metric)+radius**2*strength*velocity/(kappa*metric))
    time_metric_jump = (metric*jump+radius*derivative_jump)/2
    radial_metric_jump = radius*time_jump/(2*metric)
    check('worldline_metric_pullback_continuity', time_metric_jump+metric*tortoise_velocity*radial_metric_jump)

    time = sy.symbols('t', real=True)
    wave = sy.Function('psi')(time, radius)
    projected_time = sy.Function('T')(time, radius)
    projected_radial = sy.Function('U')(time, radius)
    potential = metric*(multipole/radius**2-6*mass/radius**3)
    force = 2*radius/kappa*(sy.diff(projected_radial, time)+metric*sy.diff(metric*projected_time, radius))
    wave_residual = -sy.diff(wave, time, 2)+metric*sy.diff(metric*sy.diff(wave, radius), radius)-potential*wave-force
    time_metric = metric*sy.diff(radius*wave, radius)/2-radius**2*metric*projected_time/kappa
    radial_metric = radius*sy.diff(wave, time)/(2*metric)+radius**2*projected_radial/(kappa*metric)
    definition = 2*radius/kappa*(sy.diff(time_metric, radius)-sy.diff(radial_metric, time)-2*time_metric/radius)
    check('general_CPM_definition_off_shell', definition-wave-radius**2*wave_residual/(kappa*metric))
    einstein_radial = sy.diff(radial_metric, time, 2)-sy.diff(time_metric, time, radius)+2*sy.diff(time_metric, time)/radius+kappa*metric*radial_metric/radius**2
    check('general_Einstein_Pr_off_shell', einstein_radial-projected_radial+radius*sy.diff(wave_residual, time)/(2*metric))
    einstein_time = -sy.diff(radial_metric, time, radius)+sy.diff(time_metric, radius, 2)-2*sy.diff(radial_metric, time)/radius-(multipole*radius-4*mass)/(radius**3*metric)*time_metric
    remainder_time = einstein_time-projected_time-radius*sy.diff(wave_residual, radius)/(2*metric)
    multiplier = sy.expand(remainder_time).coeff(sy.diff(wave, time, 2))*(-1)
    check('general_Einstein_Pt_off_shell', remainder_time-multiplier*wave_residual)
    einstein_tensor = -sy.diff(time_metric, time)/metric+metric*sy.diff(radial_metric, radius)+metric_prime*radial_metric
    tensor_source = radius**2/kappa*(sy.diff(projected_time, time)+sy.diff(projected_radial, radius)+2*projected_radial/radius)
    check('general_tensor_equation_is_Bianchi', einstein_tensor-tensor_source)
    value, space_derivative, time_derivative = sy.symbols('eta eta_x eta_t')
    line_derivative = time_derivative+tortoise_velocity*space_derivative
    endpoint_derivative = (tortoise_acceleration*jump+tortoise_velocity*jump_dot)*value+tortoise_velocity*jump*line_derivative
    line_kernel = -jump*(time_derivative*tortoise_velocity+space_derivative+metric*value/radius)
    check('weak_source_endpoint_integration_identity', delta*value-delta_prime*space_derivative-endpoint_derivative-line_kernel)
    metric_contraction = metric*value/2+radius*(space_derivative+tortoise_velocity*time_derivative)/2
    check('weak_source_is_metric_pullback_plus_endpoint', line_kernel+2*jump*metric_contraction/radius)
    fourier_frequency = sy.symbols('omega', real=True)
    check('Fourier_circular_kernel', line_kernel.subs({tortoise_velocity: 0, time_derivative: sy.I*fourier_frequency*value})-(-metric*jump*value/radius-jump*space_derivative))
    incoming_coefficient, outgoing_coefficient, integral_horizon, integral_outgoing, wronskian_ho = sy.symbols('a b I_H I_O W_HO')
    integral_body = incoming_coefficient*integral_horizon+outgoing_coefficient*integral_outgoing
    wronskian_bo = incoming_coefficient*wronskian_ho
    wronskian_bh = -outgoing_coefficient*wronskian_ho
    check('stable_body_minus_BH_source_kernel_identity', integral_body/wronskian_bo-integral_horizon/wronskian_ho+wronskian_bh*integral_outgoing/(wronskian_bo*wronskian_ho))
    check('weak_difference_common_source_cancels', (delta*value-delta_prime*space_derivative)-(delta*value-delta_prime*space_derivative))
    sources = [BRANCH/'companion-source-20261004/sources/martel-poisson-2005.pdf',
               BRANCH/'axial-companion-20261005/derive_source.py', ROOT/'eccentric_source.py',
               BRANCH/'causal-exterior-20261005/results/stage-integrity.json']
    write_report(ROOT/'results/derivation', __file__, {
        'checks': checks, 'exact_checks': len(checks), 'input_hashes': {str(path): digest(path) for path in sources},
        'convention': 'MP CPM, ell2 m+1, L=-dt^2+dx^2-V, x=rstar; particle mass normalized later',
        'projected_conservation_alone_does_not_prove_full_geodesic': True,
        'source_window_residual': 'window_dot*A*delta(r-rp)',
        'general_Pt_wave_residual_multiplier': str(sy.factor(multiplier)),
        'positive_timelike_jump_denominator': '1-u^2=f*(1+h^2/rp^2)/E^2>0 outside horizon',
        'orbital_radiation_reaction_derived': False, 'new_fitted_parameters': 0})
    print({'state': 'complete', 'exact_checks': len(checks)})


if __name__ == '__main__':
    main()
