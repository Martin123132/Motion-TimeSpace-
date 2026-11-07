from __future__ import annotations

import csv
import math
from pathlib import Path

from secular import ROOT, BRANCH, PARENT, digest, geometry, read_json, save_report, modest_process


def main():
    modest_process()
    checks = []

    def check(name, passed, value=None, tolerance=None):
        checks.append({'name': name, 'passed': bool(passed), 'value': value, 'tolerance': tolerance})

    analysis_path = ROOT/'results/analysis/status.json'
    exact_path = ROOT/'results/exact/status.json'
    analysis, exact = read_json(analysis_path), read_json(exact_path)
    check('exact identities', exact['exact_checks'] == 17 and all(row['passed'] for row in exact['checks']))
    input_reports = [analysis_path, exact_path, ROOT/'results/small-e-coarse/status.json',
                     ROOT/'results/small-e-fine/status.json']
    for path in input_reports:
        report = read_json(path)
        check(f'completed {path.parent.name}', report['state'] == 'complete' and path.with_name('COMPLETE').is_file())
        for source, expected in report['input_hashes'].items():
            check(f'input hash {path.parent.name}:{Path(source).name}', Path(source).is_file() and digest(source) == expected)
    script_names = ['analyze_actions.py', 'derive_actions.py', 'run_small_e.py', 'run_small_e.py']
    for path, script_name in zip(input_reports, script_names):
        check(f'script hash {path.parent.name}', read_json(path)['script_sha256'] == digest(ROOT/script_name))
    geometry_error = max(item['relative_error'] for row in analysis['geometry_tests'] for item in row['derivatives'])
    for index, test in enumerate(analysis['geometry_tests']):
        check(f'direct radial integral {index}', test['action_relative_error'] < 1e-40, test['action_relative_error'], 1e-40)
        for derivative in test['derivatives']:
            check(f'action derivative {index}:{derivative["coordinate"]}', derivative['relative_error'] < 1e-14,
                  derivative['relative_error'], 1e-14)
            check(f'action derivative refinement {index}:{derivative["coordinate"]}',
                  derivative['relative_error'] < derivative['fine_relative_error'])
    for row in analysis['main_rates']+analysis['small_rates']:
        label = f'{row["eccentricity"]}:{row["channel"]}'
        state = geometry(row['mass'], row['semilatus'], row['eccentricity']**2)
        ep, ez, hp, hz = [state[key] for key in ['energy_p', 'energy_z', 'angular_p', 'angular_z']]
        pdot, zdot = row['semilatus_rate_per_mu'], row['squared_eccentricity_rate_per_mu']
        Edot, hdot, jdot = row['energy_rate_per_mu'], row['angular_rate_per_mu'], row['radial_action_rate_per_mu']
        check(f'regular determinant {label}', state['determinant'] < 0)
        for name, expected, actual in [('energy', Edot, ep*pdot+ez*zdot), ('angular', hdot, hp*pdot+hz*zdot)]:
            error = abs(expected-actual)/abs(expected)
            check(f'coordinate reconstruction {label}:{name}', error < 2e-12, error, 2e-12)
        modal_energy = row['Omega_r']*jdot+row['Omega_phi']*hdot
        error = abs(modal_energy-Edot)/abs(Edot)
        check(f'two action energy balance {label}', error < 2e-12, error, 2e-12)
        error = abs(row['direct_energy_angular_semilatus_rate']-pdot)/abs(pdot)
        check(f'independent inverse p {label}', error < 2e-12, error, 2e-12)
        z_scale = max(abs(zdot), abs(pdot)/row['semilatus'])
        error = abs(row['direct_energy_angular_squared_rate']-zdot)/z_scale
        check(f'independent inverse z {label}', error < 2e-12, error, 2e-12)
        if row['eccentricity'] == 0:
            check(f'circular radial action preserved {label}', jdot == 0 and zdot == 0)
        else:
            error = abs(row['action_p']*pdot+row['action_z']*zdot-jdot)/abs(jdot)
            check(f'coordinate radial action {label}', error < 2e-12, error, 2e-12)
        if row['channel'] == 'difference' and row['eccentricity'] > 0:
            error = abs(row['optical_radial_difference_rate']-jdot)/row['radial_loss_absolute_sum']
            check(f'optical radial work {label}', error < 2e-10, error, 2e-10)
    maxima = {}
    rate_keys = ['energy_rate_per_mu', 'angular_rate_per_mu', 'radial_action_rate_per_mu',
                 'semilatus_rate_per_mu', 'squared_eccentricity_rate_per_mu']
    comparisons = [('main_refinement', 'main_coarse_rates', 'main_fine_base_rates', 2e-7),
                   ('source_quadrature', 'main_fine_base_rates', 'main_quadrature_rates', 2e-7),
                   ('small_e_refinement', 'small_coarse_rates', 'small_rates', 2e-7),
                   ('tail64_to96', 'main_fine_base_rates', 'main_rates', 2e-8),
                   ('small_tail4_to8', 'small_tail4_rates', 'small_rates', 2e-6)]
    for name, first_name, second_name, tolerance in comparisons:
        differences = []
        for first, second in zip(analysis[first_name], analysis[second_name]):
            check(f'matched comparison {name}:{first["eccentricity"]}:{first["channel"]}',
                  (first['eccentricity'], first['semilatus'], first['channel']) ==
                  (second['eccentricity'], second['semilatus'], second['channel']))
            for key in rate_keys:
                error = abs(first[key]-second[key])/max(abs(first[key]), abs(second[key]), 1e-300)
                differences.append(error)
                check(f'{name}:{first["eccentricity"]}:{first["channel"]}:{key}', error < tolerance, error, tolerance)
        maxima[name] = max(differences)
    for limit in analysis['circular_limits']:
        check(f'finite damping limit pair consistency {limit["channel"]}',
              limit['extrapolation_pair_relative_spread'] < 5e-5, limit['extrapolation_pair_relative_spread'], 5e-5)
        check(f'limit action identity {limit["channel"]}', limit['identity_relative_difference'] < 5e-6,
              limit['identity_relative_difference'], 5e-6)
    source_errors, optical_errors, wronskian_errors = [], [], []
    for label in ['coarse', 'fine']:
        small = read_json(ROOT/f'results/small-e-{label}/status.json')
        check(f'small e mode count {label}', len(small['rows']) == 51)
        for orbit in small['orbits']:
            check(f'fixed p and exterior source {label}:{orbit["eccentricity"]}',
                  abs(orbit['semilatus']*orbit['mass']/(5*orbit['radius'])-1) < 1e-14
                  and orbit['mass']*orbit['semilatus']/(1+orbit['eccentricity']) > orbit['radius'])
        source_errors += [row['full_source_integral_error_over_absolute_scale'] for row in small['rows']]
        optical_errors += [row['optical_error_over_component_sum'] for row in small['rows']]
        wronskian_errors += [row['Wronskian_error'] for row in small['rows']]
    check('new mode source identity', max(source_errors) < 2e-10, max(source_errors), 2e-10)
    check('new mode optical identity', max(optical_errors) < 2e-10, max(optical_errors), 2e-10)
    check('new mode Wronskians', max(wronskian_errors) < 2e-9, max(wronskian_errors), 2e-9)
    csv_path = ROOT/'results/analysis/secular-rates.csv'
    with csv_path.open(encoding='utf-8', newline='') as handle:
        rows = list(csv.DictReader(handle))
    check('CSV complete and rectangular', len(rows) == 18 and all(None not in row for row in rows))
    check('no bytecode directories', not list(ROOT.rglob('__pycache__')))
    for path in ROOT.glob('*.py'):
        compile(path.read_bytes(), str(path), 'exec')
    urls = ['https://arxiv.org/abs/1506.05648v2', 'https://arxiv.org/html/1506.05648',
            'https://doi.org/10.1103/PhysRevD.92.084021', 'https://arxiv.org/abs/1311.3836v2',
            'https://arxiv.org/html/1311.3836', 'https://doi.org/10.1088/0264-9381/31/9/097001']
    sources = (ROOT/'SOURCES.md').read_text(encoding='utf-8')
    check('primary source URLs recorded', all(url in sources for url in urls))
    inputs = input_reports+[ROOT/'secular.py', ROOT/'SOURCES.md', csv_path]
    report = save_report(ROOT/'results/validation', __file__, {'checks': checks, 'exact_checks': 17,
            'input_hashes': {str(path): digest(path) for path in inputs}, 'source_urls': urls,
            'maximum_high_precision_action_derivative_error': geometry_error, 'comparison_maxima': maxima,
            'maximum_new_source_scaled_error': max(source_errors), 'maximum_new_optical_scaled_error': max(optical_errors),
            'maximum_new_Wronskian_error': max(wronskian_errors), 'checks_are_correlated_implementation_tests': True})
    failed = [row for row in checks if not row['passed']]
    print({'checks': len(checks), 'failed': failed, 'comparison_maxima': maxima,
           'max_geometry_error': geometry_error, 'max_source_error': max(source_errors)})
    assert not failed, failed


if __name__ == '__main__':
    main()
