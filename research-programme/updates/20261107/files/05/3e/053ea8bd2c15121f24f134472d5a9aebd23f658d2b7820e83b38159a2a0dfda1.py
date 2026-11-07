from __future__ import annotations

import csv
import math

import mpmath as mp

from secular import ROOT, BRANCH, PARENT, digest, read_json, save_report, modest_process, rates


def mp_action(mass, semilatus, squared):
    eccentricity = mp.sqrt(squared)
    denominator = semilatus-3-squared
    def integrand(anomaly):
        cosine = mp.cos(anomaly)
        return (mp.sin(anomaly)**2*mp.sqrt(semilatus-6-2*eccentricity*cosine)
                /((semilatus-2-2*eccentricity*cosine)*(1+eccentricity*cosine)**2))
    return mass*semilatus**mp.mpf('1.5')*squared/(mp.pi*mp.sqrt(denominator))*mp.quad(integrand, [0, mp.pi])


def mp_constants(mass, semilatus, squared):
    denominator = semilatus-3-squared
    return mp.sqrt(((semilatus-2)**2-4*squared)/(semilatus*denominator)), mass*semilatus/mp.sqrt(denominator)


def mp_geometry_test(mass, semilatus, eccentricity):
    mass, semilatus, eccentricity = map(mp.mpf, map(str, [mass, semilatus, eccentricity]))
    squared = eccentricity**2
    energy, angular = mp_constants(mass, semilatus, squared)
    def time_rate(anomaly):
        cosine = mp.cos(anomaly)
        return (mass*semilatus**2*mp.sqrt((semilatus-2)**2-4*squared)
                /((semilatus-2-2*eccentricity*cosine)*(1+eccentricity*cosine)**2
                  *mp.sqrt(semilatus-6-2*eccentricity*cosine)))
    period = 2*mp.quad(time_rate, [0, mp.pi])
    phase = 2*mp.quad(lambda anomaly: mp.sqrt(semilatus/(semilatus-6-2*eccentricity*mp.cos(anomaly))), [0, mp.pi])
    radial_frequency, angular_frequency = 2*mp.pi/period, phase/period
    ep = mp.diff(lambda chosen: mp_constants(mass, chosen, squared)[0], semilatus)
    ez = mp.diff(lambda chosen: mp_constants(mass, semilatus, chosen)[0], squared)
    hp = mp.diff(lambda chosen: mp_constants(mass, chosen, squared)[1], semilatus)
    hz = mp.diff(lambda chosen: mp_constants(mass, semilatus, chosen)[1], squared)
    target_p = (ep-angular_frequency*hp)/radial_frequency
    target_z = (ez-angular_frequency*hz)/radial_frequency
    derivatives = []
    for coordinate, value, step, target in [('p', semilatus, semilatus*mp.mpf('1e-5'), target_p),
                                             ('z', squared, min(squared/20, mp.mpf('1e-5')), target_z)]:
        def action_at(chosen):
            return mp_action(mass, chosen if coordinate == 'p' else semilatus,
                             chosen if coordinate == 'z' else squared)
        coarse = (action_at(value+step)-action_at(value-step))/(2*step)
        fine = (action_at(value+step/2)-action_at(value-step/2))/step
        extrapolated = (4*fine-coarse)/3
        derivatives.append({'coordinate': coordinate, 'coarse': str(coarse), 'fine': str(fine),
                            'extrapolated': str(extrapolated), 'first_law_target': str(target),
                            'relative_error': float(abs(extrapolated-target)/abs(target)),
                            'fine_relative_error': float(abs(fine-target)/abs(target))})
    periapsis = mass*semilatus/(1+eccentricity)
    apoapsis = mass*semilatus/(1-eccentricity)
    third_root = 2*mass*semilatus/(semilatus-4)
    half_span = (apoapsis-periapsis)/2
    def radial_integrand(angle):
        radius = (apoapsis+periapsis)/2-half_span*mp.cos(angle)
        potential = (1-energy**2)*(radius-periapsis)*(apoapsis-radius)*(radius-third_root)/radius**3
        return mp.sqrt(max(mp.mpf(0), potential))/(1-2*mass/radius)*half_span*mp.sin(angle)
    direct = mp.quad(radial_integrand, [0, mp.pi])/mp.pi
    transformed = mp_action(mass, semilatus, squared)
    return {'mass': float(mass), 'semilatus': float(semilatus), 'eccentricity': float(eccentricity),
            'action': str(transformed), 'direct_radius_action': str(direct),
            'action_relative_error': float(abs(direct-transformed)/abs(direct)),
            'derivatives': derivatives, 'Omega_r': str(radial_frequency), 'Omega_phi': str(angular_frequency),
            'mp_digits': mp.mp.dps, 'purpose': 'Schwarzschild geometry control, not an additional body wave run'}


def collect(report, extension=None, max_harmonic=None):
    result = []
    all_rows = report['rows']+(extension['rows'] if extension else [])
    for orbit in report['orbits']:
        rows = [row for row in all_rows if row['eccentricity'] == orbit['eccentricity']
                and (max_harmonic is None or abs(row['harmonic']) <= max_harmonic)]
        for channel in ['body', 'BH', 'difference']:
            result.append(rates(orbit, rows, channel))
    return result


def extrapolate(first_z, first_value, second_z, second_value):
    return (second_z*first_value-first_z*second_value)/(second_z-first_z)


def main():
    modest_process()
    mp.mp.dps = 55
    fine_path = PARENT/'results/fine/status.json'
    extension_path = PARENT/'results/extension/status.json'
    coarse_path = PARENT/'results/coarse/status.json'
    quadrature_path = PARENT/'results/quadrature/status.json'
    small_fine_path = ROOT/'results/small-e-fine/status.json'
    small_coarse_path = ROOT/'results/small-e-coarse/status.json'
    fine, extension, coarse, quadrature, small_fine, small_coarse = map(read_json,
         [fine_path, extension_path, coarse_path, quadrature_path, small_fine_path, small_coarse_path])
    main_rates = collect(fine, extension)
    small_rates = collect(small_fine)
    circular_limits = []
    for channel in ['body', 'BH', 'difference']:
        circular = next(row for row in main_rates if row['channel'] == channel and row['eccentricity'] == 0)
        chosen = sorted([row for row in small_rates if row['channel'] == channel], key=lambda row: row['eccentricity'])
        squared = [row['eccentricity']**2 for row in chosen]
        damping = [row['fractional_squared_eccentricity_rate_per_mu'] for row in chosen]
        action_slope = [row['radial_action_rate_per_mu']/row['eccentricity']**2 for row in chosen]
        damping_limit = extrapolate(squared[0], damping[0], squared[1], damping[1])
        damping_large_pair = extrapolate(squared[1], damping[1], squared[2], damping[2])
        radial_limit = extrapolate(squared[0], action_slope[0], squared[1], action_slope[1])
        semilatus = circular['semilatus']
        coefficient = circular['action_z']
        derivative = coefficient*(1.5/semilatus+.5/(semilatus-6)-1/(semilatus-2)-.5/(semilatus-3))
        from_action = (radial_limit-derivative*circular['semilatus_rate_per_mu'])/coefficient
        circular_limits.append({'channel': channel, 'small_pair_damping_limit': damping_limit,
                'large_pair_damping_limit': damping_large_pair,
                'extrapolation_pair_relative_spread': abs(damping_limit-damping_large_pair)/abs(damping_limit),
                'radial_rate_over_z_limit': radial_limit, 'action_coefficient': coefficient,
                'action_coefficient_p_derivative': derivative, 'damping_limit_from_action_identity': from_action,
                'identity_relative_difference': abs(from_action-damping_limit)/abs(damping_limit),
                'interpretation': 'Numerical small-z extrapolation, not a fitted theory parameter or certified error bar'})
    geometry_tests = [mp_geometry_test(orbit['mass'], orbit['semilatus'], orbit['eccentricity'])
                      for orbit in fine['orbits'] if orbit['eccentricity'] > 0]
    geometry_tests += [mp_geometry_test(small_fine['orbits'][0]['mass'], small_fine['orbits'][0]['semilatus'], .01),
                       mp_geometry_test(1., 10., .3), mp_geometry_test(1., 7.5, .6)]
    inputs = [fine_path, extension_path, coarse_path, quadrature_path, small_fine_path, small_coarse_path,
              ROOT/'secular.py', PARENT/'results/stage-integrity.json',
              BRANCH/'eccentric-source-20261005/eccentric_source.py']
    report = save_report(ROOT/'results/analysis', __file__, {'main_rates': main_rates, 'small_rates': small_rates,
            'main_coarse_rates': collect(coarse), 'main_fine_base_rates': collect(fine),
            'main_quadrature_rates': collect(quadrature), 'small_coarse_rates': collect(small_coarse),
            'small_tail4_rates': collect(small_fine, max_harmonic=4),
            'main_tail32_rates': collect(fine, extension, max_harmonic=32),
            'circular_limits': circular_limits, 'geometry_tests': geometry_tests,
            'input_hashes': {str(path): digest(path) for path in inputs},
            'rate_normalization': 'Specific E,h,j,p,z time rates divided by companion mass mu; G_R=c=1 inherited length units',
            'sector': 'odd ell2 m+/-1 only', 'evolved_trajectory': False})
    with (ROOT/'results/analysis/secular-rates.csv').open('x', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(main_rates[0]))
        writer.writeheader()
        writer.writerows(main_rates+small_rates)
    print(json_summary(report))


def json_summary(report):
    import json
    return json.dumps({'rates': [{key: row[key] for key in ['eccentricity', 'channel', 'radial_action_rate_per_mu',
                         'semilatus_rate_per_mu', 'squared_eccentricity_rate_per_mu']} for row in report['main_rates']],
                       'limits': report['circular_limits'],
                       'max_action_derivative_error': max(item['relative_error'] for row in report['geometry_tests'] for item in row['derivatives'])})


if __name__ == '__main__':
    main()
