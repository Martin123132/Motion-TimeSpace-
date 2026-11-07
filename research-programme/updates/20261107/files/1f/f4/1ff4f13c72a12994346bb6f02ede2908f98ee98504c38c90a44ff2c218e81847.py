from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path

import psutil
import sympy as sy

from acquire_source import digest


ROOT = Path(__file__).resolve().parent


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    checks = []

    def check(name, expression):
        residual = sy.simplify(sy.expand(expression))
        checks.append({'name': name, 'passed': residual == 0, 'residual': str(residual)})
        assert residual == 0, (name, residual)

    radius, mass, orbit, particle, omega, angle, azimuth = sy.symbols('r M D mu omega theta phi', positive=True, real=True)
    angular = sy.sqrt(15/(8*sy.pi))
    harmonic = -angular*sy.sin(angle)*sy.cos(angle)*sy.exp(sy.I*azimuth)
    axial_phi = sy.sin(angle)*sy.diff(harmonic, angle)
    axial_theta = -sy.diff(harmonic, azimuth)/sy.sin(angle)
    axial_phiphi = sy.diff(axial_phi, azimuth)+sy.sin(angle)*sy.cos(angle)*axial_theta
    check('normalized_Y21_axial_vector_at_equator', axial_phi.subs(angle, sy.pi/2)-angular*sy.exp(sy.I*azimuth))
    check('normalized_Y21_axial_tensor_at_equator', axial_phiphi.subs(angle, sy.pi/2)-sy.I*angular*sy.exp(sy.I*azimuth))
    harmonics = [sy.sqrt(5/(16*sy.pi))*(3*sy.cos(angle)**2-1),
                 sy.sqrt(15/(32*sy.pi))*sy.sin(angle)**2*sy.exp(2*sy.I*azimuth)]
    for index, other in zip([0, 2], harmonics):
        check(f'axial_2{index}_circular_projection_vanishes', (sy.sin(angle)*sy.diff(other, angle)).subs(angle, sy.pi/2))
    check('Y21_unit_norm', sy.integrate(sy.conjugate(harmonic)*harmonic*sy.sin(angle), (angle, 0, sy.pi), (azimuth, 0, 2*sy.pi))-1)
    orbital_frequency = sy.sqrt(mass/orbit**3)
    metric_orbit = 1-2*mass/orbit
    ut = 1/sy.sqrt(1-3*mass/orbit)
    check('circular_geodesic_normalization', (-metric_orbit+orbit**2*orbital_frequency**2)*ut**2+1)
    check('circular_geodesic_radial_acceleration', metric_orbit*(mass/orbit**2-orbit*orbital_frequency**2)*ut**2)
    coupling = 16*sy.pi/6*particle*orbital_frequency*ut*angular
    projected_tensor = -sy.I*16*sy.pi/24*particle*orbital_frequency**2*ut*orbit**2*angular
    check('projected_Bianchi_conservation', -sy.I*orbital_frequency*coupling-4*projected_tensor/orbit**2)

    metric = 1-2*mass/radius
    multipole = sy.symbols('L', positive=True)
    kappa = multipole-2
    wave = sy.Function('psi')(radius)
    source = sy.Function('T')(radius)
    potential = metric*(multipole/radius**2-6*mass/radius**3)
    force = 2*radius*metric/kappa*sy.diff(metric*source, radius)
    second = ((potential-omega**2)*wave-metric*sy.diff(metric, radius)*sy.diff(wave, radius)+force)/metric**2
    third = sy.diff(second, radius).subs(sy.diff(wave, radius, 2), second)

    def on_shell(expression):
        return expression.subs(sy.diff(wave, radius, 3), third).subs(sy.diff(wave, radius, 2), second)

    time_metric = metric*sy.diff(radius*wave, radius)/2-radius**2*metric*source/kappa
    radial_metric = -sy.I*omega*radius*wave/(2*metric)
    definition = 2*radius/kappa*(sy.diff(time_metric, radius)+sy.I*omega*radial_metric-2*time_metric/radius)
    projected_time = sy.I*omega*sy.diff(radial_metric, radius)+sy.diff(time_metric, radius, 2)+2*sy.I*omega*radial_metric/radius-(multipole*radius-4*mass)/(radius**3*metric)*time_metric
    projected_radial = -omega**2*radial_metric+sy.I*omega*sy.diff(time_metric, radius)-2*sy.I*omega*time_metric/radius+kappa*metric*radial_metric/radius**2
    projected_trace = sy.I*omega*time_metric/metric+metric*sy.diff(radial_metric, radius)+sy.diff(metric, radius)*radial_metric
    check('CPM_definition_with_contact_term', on_shell(definition-wave))
    check('Einstein_projected_Pt_with_contact_term', on_shell(projected_time-source))
    check('Einstein_projected_Pr_zero', on_shell(projected_radial))
    check('Einstein_projected_P_tensor', projected_trace+sy.I*omega*radius**2*source/kappa)
    wrong_trace = sy.I*omega*(metric*sy.diff(radius*wave, radius)/2)/metric+metric*sy.diff(radial_metric, radius)+sy.diff(metric, radius)*radial_metric
    check('omitting_contact_erases_required_tensor_source', wrong_trace)
    check('CPM_is_twice_parent_U_in_vacuum', (time_metric.subs(source, 0).subs(wave, 2*sy.Function('U')(radius)).doit())-metric*sy.diff(radius*sy.Function('U')(radius), radius))

    strength = sy.symbols('A', real=True)
    delta_prime = 2*strength*orbit*metric_orbit**2/kappa
    delta = -2*strength*metric_orbit/kappa
    raw_delta = (2*radius*metric*sy.diff(metric, radius)-sy.diff(2*radius*metric**2, radius))*strength/kappa
    check('canonical_delta_coefficient', raw_delta.subs(radius, orbit)-delta)
    jump = delta_prime/metric_orbit**2
    slope = delta/metric_orbit+delta_prime*(2*mass/orbit**2)/metric_orbit**2
    check('master_value_jump', jump-2*strength*orbit/kappa)
    check('master_tortoise_derivative_jump', slope+2*strength*metric_orbit/kappa)
    check('metric_delta_contact_cancellation', metric_orbit*orbit*jump/2-orbit**2*metric_orbit*strength/kappa)
    check('time_metric_regular_part_is_continuous', (metric_orbit*jump+orbit*slope)/2)
    radial_jump = -sy.I*omega*orbit*jump/(2*metric_orbit)
    time_prime_jump = jump*(kappa/(2*orbit)-orbit*omega**2/(2*metric_orbit))
    check('distributional_Pt_reconstructed', time_prime_jump+sy.I*omega*radial_jump-strength)
    check('distributional_tensor_P_reconstructed', metric_orbit*radial_jump+sy.I*omega*orbit**2*strength/kappa)

    outgoing_near = -3/(omega**2*radius**2)
    growing = radius**3
    wronskian = growing*sy.diff(outgoing_near, radius)-sy.diff(growing, radius)*outgoing_near
    check('flat_nearzone_Wronskian', wronskian-15/omega**2)
    flat_jump = 2*strength*orbit/4
    flat_slope = -2*strength/4
    numerator = flat_slope*orbit**3-flat_jump*3*orbit**2
    flat_amplitude = (numerator/wronskian).subs({omega: orbital_frequency, strength: 8*sy.pi/3*particle*orbital_frequency*angular})
    pair_power = sy.simplify(3/(4*sy.pi)*orbital_frequency**2*flat_amplitude**2)
    point_newton = sy.Rational(32, 5)*particle**2*mass**3/orbit**5
    check('MP_pair_power_matches_STF_current_quadrupole', pair_power-sy.Rational(8, 45)*particle**2*orbit**6*orbital_frequency**8)
    check('axial21_to_Newtonian_power_ratio', pair_power/point_newton-mass/(36*orbit))
    sigma, response, chi = sy.symbols('sigma R_B chi', real=True)
    check('static_master_ratio', -4*response-(24*sigma).subs(sigma, -response/6))
    decaying_numerator = flat_slope/orbit**2+2*flat_jump/orbit**3
    amplitude_increment = sy.simplify(24*sigma*decaying_numerator/numerator)
    check('induced_amplitude_leading_coefficient', amplitude_increment+6*sigma/orbit**5)
    check('induced_pair_flux_leading_coefficient', 2*amplitude_increment+12*sigma/orbit**5)
    total_increment = sy.simplify(2*amplitude_increment*pair_power/point_newton)
    check('leading_magnetic_Newtonian_power_increment', total_increment+mass*sigma/(3*orbit**6))
    stage23_coefficient = (114*(1-chi)-1)/(3*chi)
    check('stage23_independent_test_mass_limit', sy.limit(stage23_coefficient, chi, 1)-total_increment/(mass*sigma/orbit**6))
    check('stage23_orbital_energy_correction_vanishes_test_mass', sy.limit(22*(1-chi)/chi, chi, 1))
    stage23_chirp = (1038*(1-chi)-1)/(3*chi)
    check('stage23_test_mass_chirp_agrees', sy.limit(stage23_chirp, chi, 1)-total_increment/(mass*sigma/orbit**6))

    output = ROOT/'results/derivation'
    output.mkdir(parents=True, exist_ok=True)
    report = {'state': 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(),
              'script_sha256': digest(__file__), 'checks': checks, 'exact_checks': len(checks),
              'source_pdf_sha256': digest(ROOT.parent/'companion-source-20261004/sources/martel-poisson-2005.pdf'),
              'convention': 'CPM odd master psi=2U, exp(-i omega t), ell2 m1 pair, mu geometric, G_R=c=1',
              'metric_reconstruction': 'h_t=F(r psi)prime/2-r^2 F P^t/kappa; h_r=r partial_t psi/(2F), P^r=0',
              'source_jumps': '[psi]=2AD/kappa; [psi_star]=-2AF_D/kappa',
              'flat_pair_power': str(pair_power), 'leading_amplitude_excess': str(amplitude_increment),
              'leading_flux_excess_over_Newtonian': str(total_increment),
              'finite_mass_ratio_claim': False, 'derived_sigma_value': False,
              'sigma_is_inherited_from_stage22': True}
    (output/'status.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'exact_checks': len(checks), 'magnetic_flux_over_Newtonian': str(total_increment)}))


if __name__ == '__main__':
    main()
