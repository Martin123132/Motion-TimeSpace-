from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

from eccentric_radiation import ROOT, BRANCH, digest, modest_process, save_json, report_header


FIELDS = ['BH_infinity_energy', 'body_infinity_energy', 'difference_infinity_energy', 'BH_horizon_energy',
          'difference_total_energy', 'BH_infinity_angular', 'body_infinity_angular',
          'difference_infinity_angular', 'BH_horizon_angular', 'difference_total_angular']


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    modest_process()
    labels = ['coarse', 'fine', 'quadrature', 'extension']
    reports = {label: read_json(ROOT/f'results/{label}/status.json') for label in labels}
    assert all(report['state'] == 'complete' for report in reports.values())
    rows = reports['fine']['rows']+reports['extension']['rows']
    assert len({(row['eccentricity'], row['harmonic']) for row in rows}) == len(rows)
    output = ROOT/'results/analysis'
    output.mkdir(parents=True, exist_ok=False)
    totals, tails, refinements = [], [], []
    for eccentricity in [0., .3, .6]:
        selected = [row for row in rows if row['eccentricity'] == eccentricity]
        orbit = next(row for row in reports['fine']['orbits'] if row['eccentricity'] == eccentricity)
        sums = {field: float(sum(row[field] for row in selected)) for field in FIELDS}
        absolute = {field: float(sum(abs(row[field]) for row in selected)) for field in FIELDS}
        axis = 5*orbit['radius']/(1-eccentricity)
        eccentric_polynomial = 1+19/2*eccentricity**2+69/8*eccentricity**4+9/16*eccentricity**6
        newtonian_current = 8/45*orbit['mass']**4/axis**6/(1-eccentricity**2)**4.5*eccentric_polynomial
        negative_energy = sum(row['BH_infinity_energy'] for row in selected if row['frequency'] < 0)
        totals.append({'eccentricity': eccentricity, 'maximum_abs_harmonic': max(abs(row['harmonic']) for row in selected),
                       **sums, 'absolute_modal_sums': absolute,
                       'fractional_infinity_energy_difference': sums['difference_infinity_energy']/sums['BH_infinity_energy'],
                       'fractional_total_energy_difference': sums['difference_total_energy']/(sums['BH_infinity_energy']+sums['BH_horizon_energy']),
                       'fractional_infinity_angular_difference': sums['difference_infinity_angular']/sums['BH_infinity_angular'],
                       'BH_horizon_to_infinity_energy': sums['BH_horizon_energy']/sums['BH_infinity_energy'],
                       'negative_frequency_BH_infinity_fraction': negative_energy/sums['BH_infinity_energy'],
                       'BH_infinity_to_leading_Newtonian_current': sums['BH_infinity_energy']/newtonian_current,
                       'leading_Newtonian_current_energy': newtonian_current,
                       'minimum_abs_frequency_R': min(abs(row['frequency_R']) for row in selected),
                       'max_optical_error': max(row['optical_error_over_component_sum'] for row in selected)})
        cuts = [0] if eccentricity == 0 else ([0, 4, 8, 12, 16, 24] if eccentricity == .3 else [0, 8, 16, 24, 32, 48, 64, 80, 96])
        for cutoff in cuts:
            tail = [row for row in selected if abs(row['harmonic']) > cutoff]
            record = {'eccentricity': eccentricity, 'cutoff': cutoff, 'computed_extension_to': max(abs(row['harmonic']) for row in selected)}
            for field in FIELDS:
                record[field+'_tested_absolute_tail_fraction'] = sum(abs(row[field]) for row in tail)/absolute[field]
            tails.append(record)
        for label in ['coarse', 'quadrature']:
            first = {(row['eccentricity'], row['harmonic']): row for row in reports[label]['rows'] if row['eccentricity'] == eccentricity}
            second = {(row['eccentricity'], row['harmonic']): row for row in reports['fine']['rows'] if row['eccentricity'] == eccentricity}
            assert first.keys() == second.keys()
            for field in FIELDS:
                denominator = sum(abs(row[field]) for row in second.values())
                change = sum(abs(first[key][field]-second[key][field]) for key in first)/denominator
                refinements.append({'eccentricity': eccentricity, 'comparison': label+'-to-fine',
                                    'quantity': field, 'absolute_modal_change_over_component_sum': float(change)})
    reference = read_json(BRANCH/'axial-reciprocity-20261005/results/current/fine/status.json')
    circular_old = next(row for row in reference['grid_rows'] if row['separation_over_radius'] == 5.)
    circular_new = next(row for row in rows if row['eccentricity'] == 0)
    circular_errors = {}
    for old, new in [('infinity_power_difference_per_mu_squared', 'difference_infinity_energy'),
                     ('reference_horizon_power_per_mu_squared', 'BH_horizon_energy'),
                     ('net_loss_difference_per_mu_squared', 'difference_total_energy'),
                     ('action_real_per_mu_squared', 'retarded_action_real'),
                     ('action_imag_per_mu_squared', 'retarded_action_imag')]:
        circular_errors[new] = abs(circular_new[new]/circular_old[old]-1)
    source_paths = [ROOT/f'results/{label}/status.json' for label in labels]
    source_paths += [BRANCH/'axial-reciprocity-20261005/results/current/fine/status.json', ROOT/'eccentric_radiation.py',
                     ROOT/'results/derivation/status.json', ROOT/'results/newtonian-control/status.json']
    report = {**report_header(__file__), 'totals': totals, 'tails': tails, 'refinements': refinements,
              'circular_regression_relative_errors': circular_errors,
              'maximum_refinement_change': max(row['absolute_modal_change_over_component_sum'] for row in refinements),
              'maximum_source_identity_scaled_error': max(row['full_source_integral_error_over_absolute_scale'] for row in rows),
              'maximum_Wronskian_error': max(row['Wronskian_error'] for row in rows),
              'input_hashes': {str(path): digest(path) for path in source_paths},
              'infinite_harmonic_tail_certified': False, 'spectrum_is_total_gravitational_radiation': False,
              'sector': 'odd ell2 m+/-1 only, source and response held identical across baseline comparison'}
    save_json(output/'status.json', report)
    for name, records in [('totals', totals), ('tails', tails), ('refinements', refinements)]:
        fields = [key for key, value in records[0].items() if not isinstance(value, dict)]
        with (output/f'{name}.csv').open('x', encoding='utf-8', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(records)
    print(json.dumps({'totals': totals, 'circular_errors': circular_errors,
                      'maximum_refinement': report['maximum_refinement_change']}))


if __name__ == '__main__':
    main()
