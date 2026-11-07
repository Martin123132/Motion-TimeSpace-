from __future__ import annotations

from pathlib import Path
import csv

import numpy as np
from scipy.optimize import brentq

from conservative import ROOT, BRANCH, PARENT, digest, read_json, save, dependencies, modest_process


def main():
    modest_process()
    inputs, checks = {}, []

    def load(path):
        report = read_json(path)
        assert report['state'] == 'complete', path
        inputs[str(path)] = digest(path)
        return report

    def check(name, value, tolerance):
        passed = bool(np.isfinite(value) and abs(value) <= tolerance)
        checks.append(dict(name=name, value=float(value), tolerance=tolerance, passed=passed))

    action = load(ROOT/'results/action/status.json')
    exact = load(ROOT/'results/derivation/status.json')
    radial = load(ROOT/'results/radial-derivative/status.json')
    parent = load(PARENT/'results/stage-integrity.json')
    for report in [action, exact, radial]:
        for path, expected in report['input_hashes'].items():
            assert Path(path).is_file() and digest(path) == expected, path
    assert len(exact['checks']) == 22 and all(row['passed'] for row in exact['checks'])
    assert len(radial['rows']) == 48 and action['new_static_interior_solves'] == 2
    for row in action['finite_comparisons']:
        check('held-out '+row['settings']+' '+row['component'], row['relative_error'], 1e-7)
    for index, row in enumerate(action['static_source_controls']):
        for key in ['imaginary_overlap', 'normalized_weight_error', 'metric_reciprocity_error', 'wronskian_error', 'quadrature_error']:
            check(f'static source {index} {key}', row[key], 2e-10)
    for label, diagnostic in action['static_interiors'].items():
        check(label+' static interior residual', diagnostic['interior_maximum_residual'], 2.1e-8)
        check(label+' static boundary', diagnostic['interior_boundary_residual'], 1e-10)
        assert diagnostic['tidal_lambda'] > 0
    for label, rows in action['raw_nodes'].items():
        assert len(rows) == 17
        for index, row in enumerate(rows):
            for sector in ['polar', 'odd']:
                check(f'{label} node{index} {sector} frequency step', row[sector+'_frequency_step_error'], 1e-6)
                check(f'{label} node{index} {sector} carrier regression', row[sector+'_carrier_regression_error'], 1e-10)
            check(f'{label} node{index} static Wronskian', row['static_law']['wronskian']+5/6, 1e-11)
    for index, row in enumerate(radial['rows']):
        for key in ['optical_error_over_component_sum', 'direct_body_amplitude_relative_error', 'Wronskian_error']:
            check(f'wave{index} {key}', row[key], 1e-8)
        for diagnostic in ['outgoing_diagnostic', 'horizon_diagnostic']:
            for key, value in row[diagnostic].items():
                if key.endswith('normalization_error'):
                    check(f'wave{index} {key}', value, 1e-10)
        if row['sector'] == 'polar':
            check(f'wave{index} interior residual', row['interior_maximum_residual'], 2.1e-8)
            check(f'wave{index} boundary', row['interior_boundary_residual'], 1e-10)
        with np.load(ROOT/'results/radial-derivative'/row['archive']) as archive:
            for key in archive.files:
                assert np.isfinite(archive[key]).all(), (index, key)
    for row in radial['derivatives']:
        label = f"{row['settings']} {row['component']} r{row['separation']}"
        check(label+' independent derivative', row['independent_stencil_error'], 1e-6)
        check(label+' derivative step', row['step_error'], 1e-6)
    for regression in action['circular_regressions']:
        check('circular action r'+str(regression['separation']), regression['action_error'], 1e-10)
        old = regression['stage20_derivatives']['estimates'][0]
        new = regression['stage38']
        check('circular energy r'+str(regression['separation']), new['delta_energy_per_mu_squared_fixed_Omega_phi']/old['energy_per_particle_squared']-1, 1e-7)
        check('circular angular r'+str(regression['separation']), new['delta_angular_per_mu_squared_fixed_Omega_phi']/old['angular_momentum_per_particle_squared']-1, 1e-7)
    numerical_keys = ['action0', 'action2', 'action0_prime', 'delta_Omega_phi_per_mu_fixed_actions',
                      'delta_Omega_r_per_mu_fixed_actions', 'delta_K_over_K_per_eta_fixed_Omega_phi',
                      'delta_energy_per_mu_squared_fixed_Omega_phi']
    resolution, nested = [], []
    for row in action['frequency_laws']['fine']:
        for label in ['coarse', 'nested9', 'nested5']:
            other = next(value for value in action['frequency_laws'][label]
                         if value['component'] == row['component'] and value['separation'] == row['separation'])
            for key in numerical_keys:
                error = abs(other[key]/row[key]-1)
                item = dict(settings=label, component=row['component'], separation=row['separation'], quantity=key, relative_error=error)
                if label == 'coarse':
                    resolution.append(item)
                    check(f"resolution {row['component']} {row['separation']} {key}", error, 1e-6)
                else:
                    item['passes_1e6_gate'] = bool(error < 1e-6)
                    nested.append(item)
                    if label == 'nested9' and row['component'] != 'odd':
                        check(f"nine-node {row['component']} {row['separation']} {key}", error, 1e-6)
    mechanical = []
    for perturbation in [1e-5, 2e-5]:
        scaled_radius = brentq(lambda value:value+6*perturbation/value**4-1, .99, 1., xtol=5e-15)
        angular = scaled_radius**-2
        radial_frequency = np.sqrt(scaled_radius**-3-24*perturbation/scaled_radius**8)
        values = np.array([angular, radial_frequency, angular/radial_frequency])
        predicted = 1+np.array([12., -3., 15.])*perturbation
        mechanical.append(dict(perturbation=perturbation, radius=scaled_radius,
                               remainder=(values-predicted).tolist(), exact_values=values.tolist()))
    remainder_ratios = np.array(mechanical[1]['remainder'])/np.array(mechanical[0]['remainder'])
    for index, ratio in enumerate(remainder_ratios):
        check('independent central-force quadratic remainder '+str(index), ratio/4-1, .01)
    compiled = []
    for path in ROOT.glob('*.py'):
        compile(path.read_bytes(), str(path), 'exec')
        compiled.append(path.name)
    for path in ROOT.rglob('*.csv'):
        with path.open(newline='', encoding='utf-8') as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            assert rows and len(set(reader.fieldnames)) == len(reader.fieldnames)
            assert all(None not in row and None not in row.values() for row in rows)
    assert not list(ROOT.rglob('__pycache__'))
    failures = [row for row in checks if not row['passed']]
    if failures:
        print('FAILED', failures, flush=True)
        raise AssertionError('Acceptance failure; no validation seal written.')
    sources = parent['primary_pdfs']+[dict(path=str(BRANCH/'orbital-backreaction-20261004/sources/fujita-et-al-2017.pdf'),
                    url='https://arxiv.org/abs/1612.02504', role='Reciprocal conservative Hamiltonian and action first-law cross-check')]
    for source in sources:
        if 'sha256' in source:
            assert digest(source['path']) == source['sha256']
        else:
            source['sha256'] = digest(source['path'])
    report = save('validation', __file__, dict(input_hashes={**inputs, **dependencies()}, checks=checks,
        exact_checks=22, resolution=resolution, nested_grid_diagnostics=nested,
        independent_central_force=mechanical, quadratic_remainder_ratios=remainder_ratios.tolist(), compiled_scripts=compiled,
        maximum_finite_action_error=max(row['relative_error'] for row in action['finite_comparisons']),
        maximum_frequency_resolution=max(row['relative_error'] for row in resolution),
        maximum_independent_radial_derivative_error=max(row['independent_stencil_error'] for row in radial['derivatives']),
        maximum_derivative_step_error=max(row['step_error'] for row in radial['derivatives']),
        maximum_frequency_step_error=max(row[sector+'_frequency_step_error'] for rows in action['raw_nodes'].values() for row in rows for sector in ['polar','odd']),
        primary_pdfs=sources, source_urls=parent['source_urls']+['https://arxiv.org/abs/1612.02504',
                  'https://arxiv.org/html/1612.02504', 'https://doi.org/10.1088/1361-6382/aa7342'],
        new_static_interiors=2, new_circular_wave_evaluations=48,
        accepted_grid='17 nodes, both radial settings; independent six-point log-radius data at5R/10R',
        excluded_grid_diagnostics='Nine-node odd derivative and five-node grids are diagnostics, not accepted solutions.',
        all_mode_self_force=False, new_observational_data=False))
    print(len(checks), 'numerical checks pass; maxima', {key:value for key,value in report.items() if key.startswith('maximum_')}, flush=True)


if __name__ == '__main__':
    main()
