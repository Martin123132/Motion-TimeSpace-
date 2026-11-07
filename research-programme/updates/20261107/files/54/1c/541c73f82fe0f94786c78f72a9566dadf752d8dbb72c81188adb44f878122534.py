from __future__ import annotations

import csv
from datetime import datetime, timezone
import json
import math

import mpmath as mp
import psutil

from acquire_source import ROOT, digest


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    paths = [ROOT/'results/refined/status.json', ROOT/'results/extended-control/status.json',
             ROOT.parent/'axial-companion-20261005/results/fine/status.json',
             ROOT/'results/derivation/status.json']
    refined, extended, previous, derivation = [read_json(path) for path in paths]
    comparison = {row['separation_over_radius']: row for report in [previous, extended] for row in report['rows']}
    mass, radius, sigma = refined['body_mass'], refined['body_radius'], refined['sigma_bar']
    beta = sigma/mass**5
    controls = []
    balances = []
    for row in refined['rows']:
        parameter = row['x']
        separation = row['separation_over_radius']
        reference = comparison[separation]
        for label, actual, first_order in [
            ('point_current', row['reference_power_to_STF_leading'], 1-17/14*parameter),
            ('magnetic_infinity_increment', row['infinity_increment_to_leading_magnetic'], 1+173/84*parameter)
        ]:
            tail = 2*math.pi*parameter**1.5
            prediction = first_order+tail
            expected_wrong_frequency = first_order+2*tail
            previous_actual = reference['reference_power_to_STF_leading'] if label == 'point_current' else reference['infinity_increment_to_leading_magnetic']
            controls.append({'sector': label, 'separation_over_radius': separation, 'x': parameter,
                             'numerical_ratio': actual, 'first_PN_ratio': first_order, 'first_PN_plus_tail': prediction,
                             'first_PN_error': abs(actual-first_order), 'tail_corrected_error': abs(actual-prediction),
                             'wrong_m2_frequency_error': abs(actual-expected_wrong_frequency),
                             'error_reduction_factor': abs(actual-first_order)/abs(actual-prediction),
                             'remaining_residual_over_x_squared': (actual-prediction)/parameter**2,
                             'resolution_difference': abs(actual-previous_actual),
                             'derived_tail_coefficient': 2*math.pi})
        slope = (1-6*parameter)/(1-3*parameter)**1.5
        infinity = row['infinity_increment_over_Newtonian']
        horizon = row['reference_horizon_power_over_Newtonian']
        leading_magnetic = -beta/3*parameter**6
        leading_absorption = parameter**5
        magnetic_approx = leading_magnetic*(1+299/84*parameter+2*math.pi*parameter**1.5)
        absorption_approx = -leading_absorption*(1+41/6*parameter)
        magnetic_chirp = infinity/slope
        absent_absorption_chirp = -horizon/slope
        previous_total = reference['total_infinity_plus_absorption_increment_over_Newtonian']/slope
        balances.append({'separation_over_radius': separation, 'x': parameter, 'geodesic_energy_slope': slope,
                         'delta_chirp_infinity_over_Newtonian': magnetic_chirp,
                         'delta_chirp_absent_BH_absorption_over_Newtonian': absent_absorption_chirp,
                         'delta_chirp_total_axial_over_Newtonian': magnetic_chirp+absent_absorption_chirp,
                         'derived_magnetic_chirp_through_1p5PN': magnetic_approx,
                         'derived_absent_absorption_chirp_through_1PN': absorption_approx,
                         'magnetic_chirp_prediction_relative_error': abs(magnetic_approx/magnetic_chirp-1),
                         'absorption_chirp_prediction_relative_error': abs(absorption_approx/absent_absorption_chirp-1),
                         'horizon_power_to_derived_leading': horizon/leading_absorption,
                         'horizon_power_first_PN_prediction': 1+16/3*parameter,
                         'horizon_power_first_PN_remainder_over_x_squared': (horizon/leading_absorption-1-16/3*parameter)/parameter**2,
                         'total_axial_resolution_difference': abs(magnetic_chirp+absent_absorption_chirp-previous_total),
                         'total_axial_resolution_fraction_of_component_sum': abs(magnetic_chirp+absent_absorption_chirp-previous_total)/(abs(magnetic_chirp)+abs(absent_absorption_chirp))})
    mp.mp.dps = 60
    beta_mp = mp.mpf(str(sigma))/mp.mpf(str(mass))**5
    radius_mp, mass_mp = mp.mpf(str(radius)), mp.mpf(str(mass))
    bands = []
    for start, end in [(40, 20), (20, 10), (10, 5)]:
        lower, upper = mass_mp/(start*radius_mp), mass_mp/(end*radius_mp)
        magnetic_integrand = lambda value: mp.mpf(5)/96*beta_mp*value**mp.mpf('2.5')*(1+mp.mpf(447)/56*value-6*mp.pi*value**mp.mpf('1.5'))
        absorption_integrand = lambda value: mp.mpf(5)/32*value**mp.mpf('1.5')*(1+mp.mpf(1891)/168*value-8*mp.pi*value**mp.mpf('1.5'))
        magnetic_primitive = lambda value: mp.mpf(5)/96*beta_mp*(mp.mpf(2)/7*value**mp.mpf('3.5')+mp.mpf(149)/84*value**mp.mpf('4.5')-mp.mpf(6)/5*mp.pi*value**5)
        absorption_primitive = lambda value: mp.mpf(5)/32*(mp.mpf(2)/5*value**mp.mpf('2.5')+mp.mpf(1891)/588*value**mp.mpf('3.5')-2*mp.pi*value**4)
        magnetic = magnetic_primitive(upper)-magnetic_primitive(lower)
        absorption = absorption_primitive(upper)-absorption_primitive(lower)
        magnetic_quad = mp.quad(magnetic_integrand, [lower, upper])
        absorption_quad = mp.quad(absorption_integrand, [lower, upper])
        errors = [abs(magnetic_quad/magnetic-1), abs(absorption_quad/absorption-1)]
        assert max(errors) < mp.mpf('1e-45'), errors
        bands.append({'start_D_over_R': start, 'end_D_over_R': end,
                      'q_times_delta_Phi_magnetic_radians': str(magnetic),
                      'q_times_delta_Phi_absent_axial_absorption_radians': str(absorption),
                      'q_times_delta_Phi_total_axial_radians': str(magnetic+absorption),
                      'maximum_primitive_quadrature_relative_error': str(max(errors)),
                      'scope': 'Strict linear axial-sector PN contribution; Phi=2 orbital phase; no finite-q correction or full-waveform claim.'})
    output = ROOT/'results/balance'
    output.mkdir(parents=True, exist_ok=False)
    for name, rows in [('tail-controls', controls), ('chirp-contributions', balances), ('phase-bands', bands)]:
        with (output/f'{name}.csv').open('x', encoding='utf-8', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    report = {'state': 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(),
              'script_sha256': digest(__file__), 'input_hashes': {str(path): digest(path) for path in paths},
              'body_mass': mass, 'body_radius': radius, 'sigma_bar': sigma, 'beta': beta,
              'tail_controls': controls, 'chirp_contributions': balances, 'phase_bands': bands,
              'leading_axial_loss_crossover_x': -3/beta,
              'leading_axial_loss_crossover_D_over_R': mass/(-3/beta)/radius,
              'new_coefficients_fitted': 0, 'new_background_solves': 0,
              'scope': 'Test-mass limit and linear axial-channel contribution; other radiative sectors not zeroed or claimed completed.'}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'beta': beta, 'crossover_D_over_R_leading': report['leading_axial_loss_crossover_D_over_R'],
                      'selected_tail_controls': [row for row in controls if row['separation_over_radius'] in [10., 160., 1280.]],
                      'selected_chirps': [row for row in balances if row['separation_over_radius'] in [10., 320., 640.]],
                      'phase_band_20_to_10': bands[1]}))


if __name__ == '__main__':
    main()
