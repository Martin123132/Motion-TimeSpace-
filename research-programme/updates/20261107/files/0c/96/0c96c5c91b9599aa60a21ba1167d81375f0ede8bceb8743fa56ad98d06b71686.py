from __future__ import annotations

import csv
from datetime import datetime, timezone
import math
import sys

import numpy as np

from polar_radiation import ROOT, BRANCH, read_json, write_json, digest, modest_process

sys.path.insert(0, str(BRANCH/'secular-actions-20261005'))
from secular import geometry, radial_action
sys.path.insert(0, str(BRANCH/'orbital-backreaction-20261004'))
from orbit_system import static_action


def power_for(row, channel):
    if channel == 'BH':
        return row['BH_infinity_energy']+row['BH_horizon_energy']
    return row['body_infinity_energy'] if channel == 'body' else row['difference_total_energy']


def losses(rows, channel):
    return {'energy': math.fsum(power_for(row, channel) for row in rows),
            'angular': math.fsum(row['azimuth']*power_for(row, channel)/row['frequency'] for row in rows),
            'radial': math.fsum(row['harmonic']*power_for(row, channel)/row['frequency'] for row in rows)}


def rates(orbit, rows, channel):
    state = geometry(orbit['mass'], orbit['semilatus'], orbit['eccentricity']**2)
    radial_frequency, angular_frequency = orbit['omega_r'], orbit['omega_phi']
    action_p = (state['energy_p']-angular_frequency*state['angular_p'])/radial_frequency
    action_z = (state['energy_z']-angular_frequency*state['angular_z'])/radial_frequency
    if orbit['eccentricity'] == 0:
        action_p = 0.
        semilatus, mass = orbit['semilatus'], orbit['mass']
        action_z = mass*semilatus**1.5*np.sqrt(semilatus-6)/(2*(semilatus-2)*np.sqrt(semilatus-3))
    action_det = -state['determinant']/radial_frequency
    flux = losses(rows, channel)
    energy_rate, angular_rate, radial_rate = -flux['energy'], -flux['angular'], -flux['radial']
    semilatus_rate = (angular_rate*action_z-state['angular_z']*radial_rate)/action_det
    squared_rate = (state['angular_p']*radial_rate-angular_rate*action_p)/action_det
    direct_p = (energy_rate*state['angular_z']-state['energy_z']*angular_rate)/state['determinant']
    direct_z = (state['energy_p']*angular_rate-energy_rate*state['angular_p'])/state['determinant']
    return {'channel': channel, 'energy_rate_per_mu': energy_rate, 'angular_rate_per_mu': angular_rate,
            'radial_action_rate_per_mu': radial_rate, 'semilatus_rate_per_mu': semilatus_rate,
            'squared_eccentricity_rate_per_mu': squared_rate,
            'direct_energy_angular_semilatus_rate': direct_p, 'direct_energy_angular_squared_rate': direct_z,
            'first_law_relative_error': abs(energy_rate-angular_frequency*angular_rate-radial_frequency*radial_rate)/max(abs(energy_rate), 1e-300),
            'optical_radial_difference': -math.fsum(2*row['harmonic']*row['retarded_action_imag'] for row in rows) if channel == 'difference' else None,
            'optical_angular_difference': -math.fsum(2*row['azimuth']*row['retarded_action_imag'] for row in rows) if channel == 'difference' else None,
            'mode_count': len(rows)}


def newtonian_quadrupole(orbit):
    mass, semilatus, eccentricity = orbit['mass'], orbit['semilatus'], orbit['eccentricity']
    nodes, weights = np.polynomial.legendre.leggauss(160)
    anomaly, weights = np.pi*(nodes+1), np.pi*weights
    radius = mass*semilatus/(1+eccentricity*np.cos(anomaly))
    position = radius[:, None]*np.array([np.cos(anomaly), np.sin(anomaly), np.zeros_like(anomaly)]).T
    velocity = np.array([-np.sin(anomaly), eccentricity+np.cos(anomaly), np.zeros_like(anomaly)]).T/np.sqrt(semilatus)
    acceleration = -mass*position/radius[:, None]**3
    scalar = np.sum(position*velocity, axis=1)
    jerk = -mass*(velocity/radius[:, None]**3-3*position*scalar[:, None]/radius[:, None]**5)
    outer = lambda first, second: np.einsum('ni,nj->nij', first, second)
    second = 2*outer(velocity, velocity)+outer(position, acceleration)+outer(acceleration, position)
    second -= (2/3)*(np.sum(velocity**2, axis=1)+np.sum(position*acceleration, axis=1))[:, None, None]*np.eye(3)
    third = 3*(outer(acceleration, velocity)+outer(velocity, acceleration))+outer(position, jerk)+outer(jerk, position)
    third -= (2/3)*(3*np.sum(velocity*acceleration, axis=1)+np.sum(position*jerk, axis=1))[:, None, None]*np.eye(3)
    major = mass*semilatus/(1-eccentricity**2)
    period = 2*np.pi*np.sqrt(major**3/mass)
    averaging = weights*radius**2/(mass*np.sqrt(semilatus)*period)
    power = float(np.dot(averaging, np.sum(third**2, axis=(1, 2))/5))
    angular = float(np.dot(averaging, 2/5*np.sum(second[:, 0, :]*third[:, 1, :]-second[:, 1, :]*third[:, 0, :], axis=1)))
    closed_power = 32/5*mass**3/major**5*(1+73*eccentricity**2/24+37*eccentricity**4/96)/(1-eccentricity**2)**3.5
    closed_angular = 32/5*mass**2.5/major**3.5*(1+7*eccentricity**2/8)/(1-eccentricity**2)**2
    return {'energy_flux_per_mu_squared': power, 'angular_flux_per_mu_squared': angular,
            'power_closed_form_relative_error': abs(power/closed_power-1),
            'angular_closed_form_relative_error': abs(angular/closed_angular-1),
            'average_constant_error': abs(float(np.sum(averaging))-1)}


def write_csv(path, rows):
    assert rows
    with path.open('x', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


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

    groups = {label: report(ROOT/'results'/label/'status.json') for label in
              ['pilot', 'fine-e03', 'fine-e06', 'resolved-coarse-e03', 'resolved-coarse-e06',
               'fine-tail03', 'fine-tail06', 'resolved-coarse-tail03', 'resolved-coarse-tail06']}
    axial = report(BRANCH/'eccentric-radiation-20261005/results/fine/status.json')
    axial_extension = report(BRANCH/'eccentric-radiation-20261005/results/extension/status.json')
    old_circular = report(BRANCH/'companion-source-20261004/results/fine/status.json')
    pole_report = report(BRANCH/'dynamical-tides-20261004/results/mode-edge004/status.json')
    pole = pole_report['iterations'][-1]['sigma']
    totals, secular, refinement, tails, poles, baseline, static_controls = [], [], [], [], [], [], []
    maxima = {}
    for eccentricity in [0., .3, .6]:
        if eccentricity == 0:
            parent = groups['pilot']
            fine = [row for row in parent['rows'] if row['eccentricity'] == 0 and row['azimuth'] == 2 and row['harmonic'] == 0]
            coarse = []
        else:
            suffix = '03' if eccentricity == .3 else '06'
            parent = groups['fine-e'+suffix]
            fine = parent['rows']+groups['fine-tail'+suffix]['rows']
            coarse = groups['resolved-coarse-e'+suffix]['rows']+groups['resolved-coarse-tail'+suffix]['rows']
        orbit = next(item for item in parent['orbits'] if item['eccentricity'] == eccentricity)
        assert len({(row['azimuth'], row['harmonic']) for row in fine}) == len(fine)
        odd = [{**row, 'azimuth': 1} for row in axial['rows']+axial_extension['rows'] if row['eccentricity'] == eccentricity]
        assert len({row['harmonic'] for row in odd}) == len(odd)
        for row in odd:
            expected = orbit['omega_phi']+row['harmonic']*orbit['omega_r']
            assert abs(row['frequency']-expected) < 3e-13*max(abs(expected), orbit['omega_r'])
        for component, rows in [('polar', fine), ('odd', odd), ('combined_ell2', fine+odd)]:
            powers = {}
            for channel in ['BH', 'body', 'difference']:
                flux = losses(rows, channel)
                powers[channel] = flux
                totals.append({'eccentricity': eccentricity, 'component': component, 'channel': channel,
                               'mode_count': len(rows), **flux})
                secular.append({'eccentricity': eccentricity, 'component': component, **rates(orbit, rows, channel)})
            if component == 'combined_ell2':
                newtonian = newtonian_quadrupole(orbit)
                baseline.append({'eccentricity': eccentricity, **newtonian,
                     'BH_energy_over_Newtonian': powers['BH']['energy']/newtonian['energy_flux_per_mu_squared'],
                     'BH_angular_over_Newtonian': powers['BH']['angular']/newtonian['angular_flux_per_mu_squared'],
                     'body_minus_BH_energy_fraction': powers['difference']['energy']/powers['BH']['energy'],
                     'body_minus_BH_angular_fraction': powers['difference']['angular']/powers['BH']['angular']})
        for azimuth in [0, 2]:
            selected = [row for row in fine if row['azimuth'] == azimuth]
            if not selected:
                continue
            closest = min(selected, key=lambda row: abs(abs(row['frequency'])-pole['real']))
            totalscale = math.fsum(row['body_infinity_energy'] for row in fine)
            difference_scale = math.fsum(abs(row['difference_total_energy']) for row in fine)
            poles.append({'eccentricity': eccentricity, 'azimuth': azimuth, 'harmonic': closest['harmonic'],
                          'signed_frequency': closest['frequency'], 'pole_real': pole['real'], 'pole_decay_rate': -pole['imaginary'],
                          'absolute_detuning_over_decay_rate': abs(abs(closest['frequency'])-pole['real'])/abs(pole['imaginary']),
                          'body_W_magnitude': closest['body_W_magnitude'],
                          'power_over_total_polar_body': closest['body_infinity_energy']/totalscale,
                          'absolute_difference_over_polar_absolute_difference': abs(closest['difference_total_energy'])/difference_scale})
        if coarse:
            for channel in ['BH', 'body', 'difference']:
                fine_totals, coarse_totals = losses(fine, channel), losses(coarse, channel)
                for quantity, weight in [('energy', lambda row: 1.), ('angular', lambda row: row['azimuth']/row['frequency']),
                                          ('radial', lambda row: row['harmonic']/row['frequency'])]:
                    scale = math.fsum(abs(weight(row)*power_for(row, channel)) for row in fine)
                    difference = abs(fine_totals[quantity]-coarse_totals[quantity])/max(scale, 1e-300)
                    refinement.append({'eccentricity': eccentricity, 'channel': channel, 'quantity': quantity,
                                       'fine_sum': fine_totals[quantity], 'coarse_sum': coarse_totals[quantity],
                                       'absolute_fine_modal_sum': scale, 'difference_over_absolute_sum': difference})
                    for cutoff in ([8, 12, 16, 24, 48, 64] if eccentricity == .3 else [16, 24, 32, 48, 64, 96, 128, 152]):
                        omitted = [row for row in fine if abs(row['harmonic']) > cutoff]
                        remainder = math.fsum(weight(row)*power_for(row, channel) for row in omitted)
                        absolute = math.fsum(abs(weight(row)*power_for(row, channel)) for row in omitted)
                        tails.append({'eccentricity': eccentricity, 'channel': channel, 'quantity': quantity, 'cutoff': cutoff,
                                      'computed_remainder_over_absolute_total': remainder/max(scale, 1e-300),
                                      'computed_absolute_remainder_over_absolute_total': absolute/max(scale, 1e-300),
                                      'is_certified_infinite_tail_bound': False})
        zero = next(row for row in parent['static_rows'] if row['eccentricity'] == eccentricity)
        static_controls.append({'eccentricity': eccentricity, 'static_action': zero['static_action_real'],
                                'tidal_lambda': zero['tidal_lambda'], 'energy_flux': zero['energy_flux'],
                                'circular_static_regression': abs(zero['static_action_real']/static_action(5*orbit['radius'], orbit['mass'], zero['tidal_lambda'])[0]-1)
                                 if eccentricity == 0 else None})
    circular = groups['pilot']['rows'][0]
    reference = next(row for row in old_circular['rows'] if row['separation_over_radius'] == 5.)
    circular_checks = {'infinity_power_relative_error': abs(circular['BH_infinity_energy']/reference['reference_pair_power_infinity']-1),
                       'horizon_power_relative_error': abs(circular['BH_horizon_energy']/reference['reference_pair_power_horizon']-1),
                       'difference_fraction_relative_error': abs((circular['difference_infinity_energy']/circular['BH_infinity_energy'])/reference['pair_flux_ratio_minus_one']-1)}
    for rows in [group['rows'] for group in groups.values()]:
        for row in rows:
            for key in ['Wronskian_error', 'BH_reconstruction_relative_error', 'optical_error_over_component_sum',
                        'full_vs_half_error_over_absolute_scale', 'metric_reciprocity_error_over_absolute_scale',
                        'direct_body_amplitude_error_over_source_scale', 'interior_boundary_residual']:
                maxima[key] = max(maxima.get(key, 0.), row[key])
    output = {'state': 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(), 'script_sha256': digest(__file__),
              'input_hashes': inputs, 'totals': totals, 'secular': secular, 'refinement': refinement, 'tails': tails,
              'pole_checks': poles, 'Newtonian_baselines': baseline, 'static_controls': static_controls,
              'circular_regression': circular_checks, 'diagnostic_maxima': maxima,
              'scope': 'Linear metric ell2 channels of inherited Einstein-scalar compact body, leading test mass; finite sampled harmonic sums.'}
    write_json(directory/'status.json', output, exclusive=True)
    for name, rows in [('totals', totals), ('secular', secular), ('refinement', refinement), ('tails', tails), ('pole_checks', poles),
                       ('Newtonian_baselines', baseline), ('static_controls', static_controls)]:
        write_csv(directory/(name+'.csv'), rows)
    print({'circular_regression': circular_checks, 'Newtonian_baselines': baseline,
           'maximum_refinement': max(row['difference_over_absolute_sum'] for row in refinement), 'diagnostics': maxima})


if __name__ == '__main__':
    main()
