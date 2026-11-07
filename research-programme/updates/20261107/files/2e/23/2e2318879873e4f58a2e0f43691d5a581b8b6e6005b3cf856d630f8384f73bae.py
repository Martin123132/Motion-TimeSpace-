from __future__ import annotations

from datetime import datetime, timezone
import math
import sys

import numpy as np

from sidebands import ROOT, BRANCH, digest, read_json, write_json, modest_process

sys.path.insert(0, str(BRANCH/'eccentric-polar-radiation-20261005'))
from analyze_waves import rates, power_for, write_csv
from secular import geometry


def damping(rows, component, channel):
    selected = [row for row in rows if component == 'combined_ell2' or row['sector'] == component]
    mass, semilatus = selected[0]['mass'], selected[0]['semilatus']
    circular = [row for row in selected if row['harmonic'] == 0]
    sidebands = [row for row in selected if row['harmonic'] != 0]
    state = geometry(mass, semilatus, 0.)
    circular_angular_rate = -math.fsum(row['azimuth']*power_for(row, channel)/row['frequency'] for row in circular)
    circular_p_rate = circular_angular_rate/state['angular_p']
    radial_rate_coefficient = -math.fsum(row['harmonic']*power_for(row, channel)/row['frequency'] for row in sidebands)
    coefficient = mass*semilatus**1.5*np.sqrt(semilatus-6)/(2*(semilatus-2)*np.sqrt(semilatus-3))
    coefficient_prime = coefficient*(1.5/semilatus+.5/(semilatus-6)-1/(semilatus-2)-.5/(semilatus-3))
    gamma = (radial_rate_coefficient-coefficient_prime*circular_p_rate)/coefficient
    optical_radial = -math.fsum(2*row['harmonic']*row['retarded_action_imag'] for row in sidebands) if channel == 'difference' else None
    return {'separation_over_radius': selected[0]['separation_over_radius'], 'mass': mass, 'semilatus': semilatus,
            'component': component, 'channel': channel, 'circular_p_rate_per_mu': circular_p_rate,
            'radial_rate_over_mu_e_squared_limit': radial_rate_coefficient, 'action_coefficient': coefficient,
            'action_coefficient_p_derivative': coefficient_prime, 'Gamma_z_per_mu': gamma,
            'optical_radial_limit': optical_radial, 'carrier_mode_count': len(circular), 'sideband_mode_count': len(sidebands)}


def complex_amplitude(row, prefix):
    return complex(row[prefix+'_real'], row[prefix+'_imag'])


def extrapolate(first_e, first, second_e, second):
    return (second_e**2*first-first_e**2*second)/(second_e**2-first_e**2)


def main():
    modest_process()
    directory = ROOT/'results/analysis'
    directory.mkdir(parents=True, exist_ok=False)
    inputs = {}

    def report(path):
        inputs[str(path)] = digest(path)
        result = read_json(path)
        assert result['state'] == 'complete', path
        return result

    groups = {label: report(ROOT/'results'/label/'status.json') for label in ['analytic-fine', 'analytic-coarse', 'finite-fine', 'finite-coarse']}
    previous_odd = {label: report(BRANCH/'secular-actions-20261005/results'/('small-e-'+label)/'status.json') for label in ['fine', 'coarse']}
    prior_odd_analysis = report(BRANCH/'secular-actions-20261005/results/analysis/status.json')
    old_polar_circular = report(BRANCH/'companion-source-20261004/results/fine/status.json')
    old_odd_circular = report(BRANCH/'eccentric-radiation-20261005/results/fine/status.json')
    limit_rows, finite_rows, comparisons, amplitude_checks, refinement, baseline, circular_controls, mode_contributions = [], [], [], [], [], [], [], []
    for label in ['fine', 'coarse']:
        analytic = groups['analytic-'+label]['rows']
        for separation in [5., 10., 20., 40.]:
            selected = [row for row in analytic if abs(row['separation_over_radius']-separation) < 1e-10]
            for component in ['polar', 'odd', 'combined_ell2']:
                for channel in ['BH', 'body', 'difference']:
                    result = damping(selected, component, channel)
                    limit_rows.append({'settings': label, **result})
            for row in selected:
                for channel in ['BH', 'body', 'difference']:
                    mode_contributions.append({'settings': label, 'separation_over_radius': separation,
                         'sector': row['sector'], 'azimuth': row['azimuth'], 'harmonic': row['harmonic'], 'channel': channel,
                         'frequency': row['frequency'], 'power_coefficient': power_for(row, channel),
                         'radial_rate_coefficient': -row['harmonic']*power_for(row, channel)/row['frequency']})
        finite = groups['finite-'+label]
        finite_modes = finite['rows']+[{**row, 'sector': 'odd', 'azimuth': 1} for row in previous_odd[label]['rows']]
        analytic_circle = {(row['sector'], row['azimuth'], row['harmonic']): row for row in analytic if abs(row['separation_over_radius']-5) < 1e-10}
        for orbit in finite['orbits']:
            eccentricity = orbit['eccentricity']
            selected = [row for row in finite_modes if row['eccentricity'] == eccentricity]
            assert len({(row['sector'], row['azimuth'], row['harmonic']) for row in selected}) == len(selected)
            for row in selected:
                expected_frequency = row['azimuth']*orbit['omega_phi']+row['harmonic']*orbit['omega_r']
                assert abs(row['frequency']-expected_frequency) < 1e-12*max(abs(expected_frequency), orbit['omega_r'])
                key = (row['sector'], row['azimuth'], row['harmonic'])
                if key in analytic_circle:
                    predicted = analytic_circle[key]
                    amplitude_scale = eccentricity if row['harmonic'] else 1.
                    for prefix in ['reference_amplitude', 'delta_amplitude', 'horizon_amplitude']:
                        exact = complex_amplitude(predicted, prefix)
                        finite_value = complex_amplitude(row, prefix)/amplitude_scale
                        amplitude_checks.append({'settings': label, 'eccentricity': eccentricity,
                             'sector': row['sector'], 'azimuth': row['azimuth'], 'harmonic': row['harmonic'], 'amplitude': prefix,
                             'relative_error': abs(finite_value-exact)/max(abs(exact), 1e-300),
                             'predicted_real': exact.real, 'predicted_imag': exact.imag,
                             'finite_scaled_real': finite_value.real, 'finite_scaled_imag': finite_value.imag})
            for component in ['polar', 'odd', 'combined_ell2']:
                chosen = [row for row in selected if component == 'combined_ell2' or row['sector'] == component]
                for channel in ['BH', 'body', 'difference']:
                    value = rates(orbit, chosen, channel)
                    value['Gamma_z_per_mu'] = value['squared_eccentricity_rate_per_mu']/eccentricity**2
                    truncated = rates(orbit, [row for row in chosen if abs(row['harmonic']) <= 4], channel)
                    finite_rows.append({'settings': label, 'eccentricity': eccentricity, 'component': component,
                                       **value, 'tail4_Gamma_difference_relative': abs(value['squared_eccentricity_rate_per_mu']-truncated['squared_eccentricity_rate_per_mu'])/max(abs(value['squared_eccentricity_rate_per_mu']), 1e-300)})
        for component in ['polar', 'odd', 'combined_ell2']:
            for channel in ['BH', 'body', 'difference']:
                analytic_value = next(row for row in limit_rows if row['settings'] == label and abs(row['separation_over_radius']-5) < 1e-10 and row['component'] == component and row['channel'] == channel)
                selected = [row for row in finite_rows if row['settings'] == label and row['component'] == component and row['channel'] == channel]
                selected.sort(key=lambda row: row['eccentricity'])
                predicted = analytic_value['Gamma_z_per_mu']
                first, second, third, fourth = selected
                small = extrapolate(first['eccentricity'], first['Gamma_z_per_mu'], second['eccentricity'], second['Gamma_z_per_mu'])
                middle = extrapolate(second['eccentricity'], second['Gamma_z_per_mu'], third['eccentricity'], third['Gamma_z_per_mu'])
                comparisons.append({'settings': label, 'component': component, 'channel': channel,
                     'analytic_Gamma': predicted, 'small_pair_extrapolation': small, 'middle_pair_extrapolation': middle,
                     'small_pair_relative_error': abs(small/predicted-1), 'middle_pair_relative_error': abs(middle/predicted-1),
                     'raw_e0005_relative_error': abs(first['Gamma_z_per_mu']/predicted-1),
                     'raw_e001_relative_error': abs(second['Gamma_z_per_mu']/predicted-1),
                     'raw_e002_relative_error': abs(third['Gamma_z_per_mu']/predicted-1),
                     'raw_e004_relative_error': abs(fourth['Gamma_z_per_mu']/predicted-1)})
    for row in [row for row in limit_rows if row['settings'] == 'fine']:
        coarse = next(item for item in limit_rows if item['settings'] == 'coarse' and item['component'] == row['component'] and item['channel'] == row['channel'] and abs(item['separation_over_radius']-row['separation_over_radius']) < 1e-10)
        refinement.append({'component': row['component'], 'channel': row['channel'], 'separation_over_radius': row['separation_over_radius'],
                           'Gamma_relative_refinement': abs(coarse['Gamma_z_per_mu']/row['Gamma_z_per_mu']-1)})
        if row['component'] == 'combined_ell2' and row['channel'] == 'BH':
            difference = next(item for item in limit_rows if item['settings'] == 'fine' and item['component'] == 'combined_ell2' and item['channel'] == 'difference' and abs(item['separation_over_radius']-row['separation_over_radius']) < 1e-10)
            newtonian = -608/(15*row['mass']**2*row['semilatus']**4)
            baseline.append({'separation_over_radius': row['separation_over_radius'], 'semilatus': row['semilatus'],
                             'Newtonian_Gamma': newtonian, 'BH_Gamma': row['Gamma_z_per_mu'], 'difference_Gamma': difference['Gamma_z_per_mu'],
                             'BH_over_Newtonian': row['Gamma_z_per_mu']/newtonian,
                             'fractional_body_extra_damping': difference['Gamma_z_per_mu']/row['Gamma_z_per_mu']})
    for row in groups['analytic-fine']['rows']:
        if row['harmonic']:
            continue
        if row['sector'] == 'polar':
            prior = next(item for item in old_polar_circular['rows'] if abs(item['separation_over_radius']-row['separation_over_radius']) < 1e-10)
            reference_power = prior['reference_pair_power_infinity']
            difference = reference_power*prior['pair_flux_ratio_minus_one']
        elif abs(row['separation_over_radius']-5) < 1e-10:
            prior = next(item for item in old_odd_circular['rows'] if item['eccentricity'] == 0)
            reference_power, difference = prior['BH_infinity_energy'], prior['difference_infinity_energy']
        else:
            continue
        circular_controls.append({'sector': row['sector'], 'separation_over_radius': row['separation_over_radius'],
                     'BH_power_relative_error': abs(row['BH_infinity_energy']/reference_power-1),
                     'difference_power_relative_error': abs(row['difference_infinity_energy']/difference-1)})
    previous_controls = []
    for prior in prior_odd_analysis['circular_limits']:
        new = next(row for row in limit_rows if row['settings'] == 'fine' and row['component'] == 'odd' and row['channel'] == prior['channel'] and abs(row['separation_over_radius']-5) < 1e-10)
        previous_controls.append({'channel': prior['channel'], 'old_numerical_extrapolation': prior['small_pair_damping_limit'],
                                  'new_derived_value': new['Gamma_z_per_mu'],
                                  'old_extrapolation_relative_error': abs(prior['small_pair_damping_limit']/new['Gamma_z_per_mu']-1)})
    result = {'state': 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(), 'script_sha256': digest(__file__),
              'input_hashes': inputs, 'analytic_limits': limit_rows, 'finite_rates': finite_rows,
              'limit_comparisons': comparisons, 'amplitude_checks': amplitude_checks, 'refinement': refinement,
              'weak_field_baseline': baseline, 'circular_regression': circular_controls, 'previous_odd_comparison': previous_controls,
              'mode_contributions': mode_contributions, 'normalization': 'Gamma=(e^2)_dot/(mu e^2), all results in inherited geometric model units; no fit.'}
    write_json(directory/'status.json', result, exclusive=True)
    for name, rows in [('analytic_limits', limit_rows), ('finite_rates', finite_rows), ('limit_comparisons', comparisons),
                       ('amplitude_checks', amplitude_checks), ('refinement', refinement), ('weak_field_baseline', baseline),
                       ('circular_regression', circular_controls), ('mode_contributions', mode_contributions)]:
        write_csv(directory/(name+'.csv'), rows)
    print({'weak_field_baseline': baseline, 'max_small_extrapolation_error': max(row['small_pair_relative_error'] for row in comparisons),
           'max_radial_refinement': max(row['Gamma_relative_refinement'] for row in refinement), 'old_odd_comparison': previous_controls}, flush=True)


if __name__ == '__main__':
    main()
