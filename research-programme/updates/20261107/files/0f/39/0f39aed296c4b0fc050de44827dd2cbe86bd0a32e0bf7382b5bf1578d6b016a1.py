from __future__ import annotations

import csv
from datetime import datetime, timezone
import math
from pathlib import Path

import numpy as np

from sidebands import ROOT, BRANCH, digest, read_json, write_json, modest_process, numeric_coefficients, polar_settings
from analyze_limit import extrapolate
from polar_source import coefficients, harmonic_value
from eccentric_source import orbit_constants


def main():
    modest_process()
    checks, inputs, groups = [], {}, {}

    def check(name, passed, value=None, tolerance=None):
        checks.append(dict(name=name, passed=bool(passed), value=value, tolerance=tolerance))

    def below(name, value, tolerance):
        check(name, math.isfinite(value) and value <= tolerance, float(value), tolerance)

    def relative(first, second):
        return abs(first-second)/max(abs(first), abs(second), 1e-300)

    def report(path, script):
        inputs[str(path)] = digest(path)
        value = read_json(path)
        check(str(path)+' complete', value['state'] == 'complete')
        check(str(path)+' producer current', value['script_sha256'] == digest(ROOT/script))
        for source, expected in value.get('input_hashes', {}).items():
            check(str(path)+' input '+source, Path(source).is_file() and digest(source) == expected)
        return value

    analysis = report(ROOT/'results/analysis/status.json', 'analyze_limit.py')
    exact_count = 0
    for label, script, count in [('derivation', 'derive_sidebands.py', 16),
                                 ('tidal-limit', 'derive_tidal_limit.py', 7),
                                 ('horizon-limit', 'derive_horizon_limit.py', 7)]:
        value = report(ROOT/'results'/label/'status.json', script)
        groups[label] = value
        exact_count += len(value['checks'])
        check(label+' exact identities', len(value['checks']) == count and all(row['passed'] and row['residual'] == '0' for row in value['checks']))
    check('electric tidal coefficient', groups['tidal-limit']['linear_tidal_coefficient'] == '459/19')
    check('electric absorption coefficient', groups['horizon-limit']['leading_horizon_coefficient'] == '54/19')
    mode_count = 0
    for label, count in [('analytic-fine', 28), ('analytic-coarse', 28), ('finite-fine', 93), ('finite-coarse', 93)]:
        directory = ROOT/'results'/label
        value = report(directory/'status.json', 'run_sidebands.py')
        groups[label] = value
        check(label+' completion marker', (directory/'COMPLETE').is_file())
        check(label+' requested evaluations', len(value['rows']) == count)
        identity = lambda row: (row.get('eccentricity'), row.get('separation_over_radius'), row['sector'], row['azimuth'], row['harmonic'])
        check(label+' no duplicate modes', len({identity(row) for row in value['rows']}) == count)
        mode_count += len(value['rows'])
        for row in value['rows']:
            prefix = label+':'+str(identity(row))+':'
            with np.load(directory/row['archive'], allow_pickle=False) as archive:
                check(prefix+'finite saved arrays', bool(archive.files) and all(np.isfinite(archive[key]).all() for key in archive.files))
                if 'frequency' in archive.files:
                    below(prefix+'saved frequency', relative(abs(float(archive['frequency'])), abs(row['frequency'])), 1e-14)
                else:
                    check(prefix+'inherited odd archive schema', row['sector'] == 'odd' and label.startswith('finite') and 'half_time' in archive.files)
                if row['sector'] == 'polar':
                    check(prefix+'coupled interior archived', 'spline_coefficients' in archive.files)
                elif label.startswith('analytic'):
                    check(prefix+'odd interior archived', 'interior_values' in archive.files)
            check(prefix+'positive emitted powers', all(row[key] >= 0 for key in ['BH_infinity_energy', 'BH_horizon_energy', 'body_infinity_energy']))
            below(prefix+'Wronskian', row['Wronskian_error'], 1e-7)
            below(prefix+'optical identity', row['optical_error_over_component_sum'], 1e-11)
            below(prefix+'infinity unit current', row['outgoing_diagnostic']['infinity_flux_normalization_error'], 1e-11)
            below(prefix+'horizon unit current', row['horizon_diagnostic']['horizon_flux_normalization_error'], 1e-11)
            for key in ['direct_body_amplitude_relative_error', 'direct_body_amplitude_error_over_source_scale', 'BH_reconstruction_relative_error']:
                if key in row:
                    below(prefix+key, row[key], 1e-7)
            for key in ['metric_reciprocity_error_over_absolute_scale', 'full_vs_half_error_over_absolute_scale', 'full_source_integral_error_over_absolute_scale']:
                if key in row:
                    below(prefix+key, row[key], 1e-8)
            if row['sector'] == 'polar':
                below(prefix+'interior residual', row['interior_maximum_residual'], 1.001*polar_settings(value['arguments']['settings'])['interior_tolerance'])
                below(prefix+'boundary residual', row['interior_boundary_residual'], 1e-8)
            if 'BH_boundary_control' in row:
                check(prefix+'identical boundary null', row['BH_boundary_control'] == 0)
            if row['azimuth'] == 0 and label.startswith('finite'):
                check(prefix+'zero azimuthal angular flux', all(row[key+'_angular'] == 0 for key in ['BH_infinity', 'BH_horizon', 'body_infinity', 'difference_total']))
            if label.startswith('analytic'):
                check(prefix+'correct eccentricity normalization', row['eccentricity_order_amplitude'] == int(row['harmonic'] != 0))
        if label.startswith('finite'):
            orbits = value['orbits']
            check(label+'four eccentricities', {row['eccentricity'] for row in orbits} == {.005, .01, .02, .04})
            below(label+'fixed p rather than fixed periapsis', max(row['semilatus'] for row in orbits)-min(row['semilatus'] for row in orbits), 1e-12)

    independent = []
    mass = groups['analytic-fine']['rows'][0]['mass']
    for semilatus in [8., 40., 332.6905215498321]:
        energy, angular = orbit_constants(mass, semilatus, 0.)
        for ratio in [.9, 1., 1.1]:
            radius = mass*semilatus*ratio
            for azimuth in [0, 2]:
                frequency = (azimuth+1)/(mass*semilatus**1.5)
                model = numeric_coefficients('polar')(radius, mass, energy, angular, azimuth, frequency, harmonic_value(azimuth))

                def original(position, velocity=0.):
                    samples = dict(radius=position, coordinate_velocity=velocity, phase=0.,
                                   proper_velocity=energy*velocity/(1-2*mass/position))
                    return coefficients(samples, mass, energy, angular, azimuth)

                base = original(radius)
                perturbation = radius*1e-4
                for position, key in [(0, 'delta'), (1, 'delta_prime')]:
                    error = relative(model[position], base[key])
                    independent.append(float(error))
                    below('independent canonical coefficient '+str((semilatus, ratio, azimuth, key)), error, 1e-11)
                    derivative = (original(radius-2*perturbation)[key]-8*original(radius-perturbation)[key]
                                  +8*original(radius+perturbation)[key]-original(radius+2*perturbation)[key])/(12*perturbation)
                    below('independent fixed E,h radial derivative '+str((semilatus, ratio, azimuth, key)), relative(model[position+3], derivative), 1e-8)
                velocity_coefficient = (original(radius, 1e-5)['delta']-original(radius, -1e-5)['delta'])/(2j*1e-5)
                below('independent velocity coefficient '+str((semilatus, ratio, azimuth)), relative(model[2], velocity_coefficient), 1e-11)

    amplitude_extrapolation = []
    smallest = [row for row in analysis['amplitude_checks'] if row['eccentricity'] == .005]
    for first in smallest:
        second = next(row for row in analysis['amplitude_checks'] if row['eccentricity'] == .01 and
                      all(row[key] == first[key] for key in ['settings', 'sector', 'azimuth', 'harmonic', 'amplitude']))
        predicted = complex(first['predicted_real'], first['predicted_imag'])
        first_value = complex(first['finite_scaled_real'], first['finite_scaled_imag'])
        second_value = complex(second['finite_scaled_real'], second['finite_scaled_imag'])
        error = relative(extrapolate(.005, first_value, .01, second_value), predicted)
        amplitude_extrapolation.append(float(error))
        prefix = str(tuple(first[key] for key in ['settings', 'sector', 'azimuth', 'harmonic', 'amplitude']))
        below(prefix+'amplitude e2 extrapolation', error, 1e-6)
        if first['relative_error'] > 1e-7:
            below(prefix+'leading e2 scaling', abs(second['relative_error']/first['relative_error']/4-1), .03)
    for row in analysis['limit_comparisons']:
        prefix = str((row['settings'], row['component'], row['channel']))
        below(prefix+'small-e damping limit', row['small_pair_relative_error'], 1e-6)
        check(prefix+'raw damping approaches analytic limit', row['raw_e0005_relative_error'] < row['raw_e001_relative_error'] < row['raw_e002_relative_error'] < row['raw_e004_relative_error'])
    for row in analysis['refinement']:
        below('two-resolution damping '+str((row['component'], row['channel'], row['separation_over_radius'])), row['Gamma_relative_refinement'], 1e-6)
    for row in analysis['circular_regression']:
        below('circular source regression '+str(row['sector'])+str(row['separation_over_radius']), max(row['BH_power_relative_error'], row['difference_power_relative_error']), 1e-9)
    for row in analysis['finite_rates']:
        prefix = str((row['settings'], row['eccentricity'], row['component'], row['channel']))
        below(prefix+'finite first law', row['first_law_relative_error'], 1e-10)
        below(prefix+'independent p inverse', relative(row['semilatus_rate_per_mu'], row['direct_energy_angular_semilatus_rate']), 1e-9)
        below(prefix+'independent z inverse', relative(row['squared_eccentricity_rate_per_mu'], row['direct_energy_angular_squared_rate']), 1e-8)
        below(prefix+'cutoff4 control', row['tail4_Gamma_difference_relative'], 1e-6)
    limits = analysis['analytic_limits']
    for row in limits:
        prefix = str((row['settings'], row['component'], row['channel'], row['separation_over_radius']))
        if row['channel'] == 'difference':
            below(prefix+'analytic optical radial law', relative(row['optical_radial_limit'], row['radial_rate_over_mu_e_squared_limit']), 1e-10)
        if row['component'] == 'combined_ell2':
            components = [item for item in limits if item['component'] in ['polar', 'odd'] and
                          all(item[key] == row[key] for key in ['settings', 'channel', 'separation_over_radius'])]
            below(prefix+'parity sum', relative(row['Gamma_z_per_mu'], sum(item['Gamma_z_per_mu'] for item in components)), 1e-12)
        if row['channel'] == 'body':
            others = [item for item in limits if item['channel'] in ['BH', 'difference'] and
                      all(item[key] == row[key] for key in ['settings', 'component', 'separation_over_radius'])]
            below(prefix+'linear boundary decomposition', relative(row['Gamma_z_per_mu'], sum(item['Gamma_z_per_mu'] for item in others)), 1e-12)
    baseline = sorted(analysis['weak_field_baseline'], key=lambda row: row['separation_over_radius'])
    errors = [abs(row['BH_over_Newtonian']-1) for row in baseline]
    check('four-radius approach to Newtonian damping', all(first > second for first, second in zip(errors, errors[1:])))
    below('outermost Newtonian damping residual', errors[-1], .002)
    for row in groups['horizon-limit']['rows']:
        prefix = 'asymptotic '+str(row['separation_over_radius'])
        below(prefix+'exact infinity minus horizon split', row['exact_split_relative_error'], 1e-12)
        below(prefix+'leading electric tide residual', abs(row['outgoing_leading_relative_correction']), .004)
        below(prefix+'leading electric absorption residual', abs(row['horizon_leading_relative_correction']), .021)

    for path in sorted((ROOT/'results/analysis').glob('*.csv')):
        with path.open(newline='', encoding='utf-8') as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            check(path.name+'well formed nonempty table', bool(rows) and len(reader.fieldnames) == len(set(reader.fieldnames)) and
                  all(None not in row and all(value is not None for value in row.values()) for row in rows))
        inputs[str(path)] = digest(path)
    prior_path = BRANCH/'eccentric-polar-radiation-20261005/results/validation/status.json'
    prior = read_json(prior_path)
    inputs[str(prior_path)] = digest(prior_path)
    for primary in prior['primary_pdfs']:
        check('primary PDF '+primary['path'], Path(primary['path']).is_file() and digest(primary['path']) == primary['sha256'])
    urls = prior['source_urls']+['https://arxiv.org/abs/gr-qc/0407050', 'https://arxiv.org/pdf/gr-qc/0407050',
                                 'https://doi.org/10.1103/PhysRevD.70.084044']
    check('horizon source recorded', groups['horizon-limit']['source_url'] in urls and groups['horizon-limit']['source_doi'] == '10.1103/PhysRevD.70.084044')
    failed = [row for row in checks if not row['passed']]
    result = dict(state='failed' if failed else 'complete', time_utc=datetime.now(timezone.utc).isoformat(),
                  script_sha256=digest(__file__), input_hashes=inputs, checks=checks, exact_checks=exact_count,
                  wave_mode_evaluations=mode_count, inherited_odd_rows=102, primary_pdfs=prior['primary_pdfs'], source_urls=urls,
                  maximum_amplitude_extrapolation_error=max(amplitude_extrapolation),
                  maximum_small_pair_damping_error=max(row['small_pair_relative_error'] for row in analysis['limit_comparisons']),
                  maximum_damping_refinement=max(row['Gamma_relative_refinement'] for row in analysis['refinement']),
                  maximum_finite_cutoff4_error=max(row['tail4_Gamma_difference_relative'] for row in analysis['finite_rates']),
                  scope='Correlated numerical/provenance checks, not independent experiments or new observational tests.')
    directory = ROOT/'results/validation'
    directory.mkdir(parents=True, exist_ok=False)
    write_json(directory/'status.json', result, exclusive=True)
    print(dict(checks=len(checks), failed=failed[:15], wave_mode_evaluations=mode_count,
               exact_checks=exact_count, maximum_amplitude_extrapolation_error=max(amplitude_extrapolation)), flush=True)
    assert not failed, str(len(failed))+' checks failed'


if __name__ == '__main__':
    main()

