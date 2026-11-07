from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
import sympy as sp

from inspiral import (ROOT, BRANCH, PARENT, digest, read_json, modest_process, save,
                      dependencies, coefficients, analytic_coefficients, physical_row,
                      normalized_endpoint, resummed_control)


def main():
    modest_process()
    checks = []

    def check(name, passed, detail=None):
        checks.append(dict(name=name, passed=bool(passed), detail=detail))

    derivation = read_json(ROOT/'results/derivation/status.json')
    trajectories = read_json(ROOT/'results/trajectories/status.json')
    parent = read_json(PARENT/'results/validation/status.json')
    check('all 26 symbolic identities exact', len(derivation['checks']) == 26 and
          all(row['passed'] and row['residual'] == '0' for row in derivation['checks']))
    for name, script in [('derivation', 'derive_clock.py'), ('trajectories', 'run_inspiral.py')]:
        report = read_json(ROOT/'results'/name/'status.json')
        check(name+' script hash', report['script_sha256'] == digest(ROOT/script))
        for source, expected in report['input_hashes'].items():
            check(name+' source '+source, Path(source).is_file() and digest(source) == expected)
        for relative, expected in report.get('output_hashes', {}).items():
            check(name+' saved payload '+relative, digest(ROOT/'results'/name/relative) == expected)
    for mass_ratio in [0., .001, .01, 1.]:
        numeric = coefficients(mass_ratio)
        for name, expression in derivation['coefficients'].items():
            expression = sp.sympify(expression)
            evaluated = float(expression.subs({symbol:mass_ratio for symbol in expression.free_symbols}))
            name = 'gamma_tide' if name == 'gamma_frequency' else name
            check(f'coefficient {name} q={mass_ratio}', abs(numeric[name]-evaluated) < 2e-12)
    for row in trajectories['solutions']:
        check(f'variational primitive agreement q={row["mass_ratio"]}', row['maximum_scaled_error'] < 2e-11,
              row['maximum_scaled_error'])
        check(f'tolerance refinement q={row["mass_ratio"]}', row['maximum_scaled_resolution'] < 2e-8,
              row['maximum_scaled_resolution'])
    for row in trajectories['quadratures']:
        check(f'independent quadrature {row["mass_ratio"]} {row["exponent"]} {row["component"]}',
              row['relative_error'] < 2e-12, row['relative_error'])
    for family in ['tide_only', 'eccentricity_only', 'both']:
        controls = [row for row in trajectories['order_controls'] if row['family'] == family]
        for left, right in zip(controls, controls[1:]):
            for index in ([1, 2] if family == 'tide_only' else [0, 1, 2]):
                ratio = left['residual'][index]/right['residual'][index]
                check(f'quadratic order remainder {family} {left["strength"]} component {index}',
                      3.96 < ratio < 4.04, ratio)
    mass, radius, deformability = [trajectories['body'][key] for key in ['mass', 'radius', 'tidal_lambda']]
    with (ROOT/'results/trajectories/trajectories.csv').open(newline='', encoding='utf-8') as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        check('CSV rectangular and unique headers', len(rows) == 132 and len(set(reader.fieldnames)) == len(reader.fieldnames)
              and all(None not in row and None not in row.values() for row in rows))
    for mass_ratio in [.001, .01]:
        for initial_z in [0., .0001]:
            selected = [row for row in rows if float(row['mass_ratio']) == mass_ratio and float(row['initial_z']) == initial_z]
            frequencies = np.array([float(row['frequency']) for row in selected])
            initial = selected[0]
            check(f'common initial state {mass_ratio} {initial_z}',
                float(initial['z_body']) == initial_z == float(initial['z_point']) and
                all(float(initial[key]) == 0 for key in ['scaled_time_body', 'scaled_time_point',
                    'scaled_phase_body', 'scaled_phase_point', 'scaled_time_difference', 'scaled_phase_difference']))
            check(f'monotonic frequency {mass_ratio} {initial_z}', np.all(np.diff(frequencies) > 0))
            for key in ['scaled_time_body', 'scaled_time_point', 'scaled_phase_body', 'scaled_phase_point']:
                values = np.array([float(row[key]) for row in selected])
                check(f'positive growing {key} {mass_ratio} {initial_z}', values[0] == 0 and np.all(np.diff(values) > 0))
            check(f'nonnegative circularising action eccentricity {mass_ratio} {initial_z}',
                all(0 <= float(row['z_body']) <= float(row['z_point']) <= initial_z for row in selected))
            check(f'body-minus-point sign {mass_ratio} {initial_z}', all(float(row['scaled_time_difference']) <= 0 and
                float(row['scaled_phase_difference']) <= 0 for row in selected))
            for ratio in [1., .75, .5]:
                zero = physical_row(mass, radius, 0., mass_ratio, initial_z, 10., ratio)
                check(f'zero-tide equality {mass_ratio} {initial_z} {ratio}',
                    all(zero[key] == 0 for key in ['scaled_time_difference', 'scaled_phase_difference', 'z_difference']))
    prior_path = BRANCH/'orbital-backreaction-20261004/results/balance/status.json'
    circular_controls = []
    for prior in read_json(prior_path)['phase_illustrations']:
        mass_ratio = prior['illustrative_mass_ratio_not_fitted']
        outer, inner = prior['outer_separation_over_radius'], prior['inner_separation_over_radius']
        current = physical_row(mass, radius, deformability, mass_ratio, 0., outer, inner/outer)
        target = prior['delta_GW_phase_radians']
        error = abs(current['dominant_m2_carrier_phase_difference']/target-1)
        circular_controls.append(dict(mass_ratio=mass_ratio, outer=outer, inner=inner, relative_error=error))
        check(f'archived stage20 circular phase {mass_ratio} {outer}', error < 2e-10, error)
    mixed_controls = []
    for mass_ratio in [0., .01]:
        target = analytic_coefficients(mass_ratio, .5)[[1, 5, 9]]
        estimates = []
        for strength in [1., .5, .25]:
            eccentric_step, tide_step = .004*strength, 2e-5*strength
            derivative = np.zeros(3)
            samples = []
            for sign_z, sign_tide in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                solution = resummed_control(mass_ratio, .5, sign_z*eccentric_step, sign_tide*tide_step, tolerance=2.5e-14)
                value = solution.y[:, -1]
                derivative += sign_z*sign_tide*value/(4*eccentric_step*tide_step)
                samples.append(dict(sign_z=sign_z, sign_tide=sign_tide, endpoint=value.tolist()))
            estimates.append(derivative)
            mixed_controls.append(dict(mass_ratio=mass_ratio, strength=strength, estimate=derivative.tolist(),
                target=target.tolist(), samples=samples,
                role='Signed auxiliary sensitivity control, not physical negative eccentricity/deformability.'))
        extrapolated = (4*estimates[-1]-estimates[-2])/3
        error = float(np.max(abs(extrapolated/target-1)))
        check(f'independent mixed sensitivity q={mass_ratio}', error < 3e-7, error)
    maximum_tide = max(row['local_tide'] for row in trajectories['endpoints'])
    maximum_weakfield = max(row['central_weak_field_parameter'] for row in trajectories['endpoints'])
    check('declared illustrative expansion region', maximum_tide < 7e-6 and maximum_weakfield < .004,
          dict(maximum_local_tide=maximum_tide, maximum_weakfield_parameter=maximum_weakfield))
    for source in parent['primary_pdfs']:
        check('inherited primary source '+source['path'], digest(source['path']) == source['sha256'])
    check('no bytecode cache', not list(ROOT.rglob('__pycache__')))
    inputs = dependencies()
    for path in [ROOT/'results/derivation/status.json', ROOT/'results/trajectories/status.json', prior_path,
                 PARENT/'results/validation/status.json']:
        inputs[str(path)] = digest(path)
    failed = [row for row in checks if not row['passed']]
    report = dict(checks=checks, input_hashes=inputs, exact_checks=26,
        circular_controls=circular_controls, mixed_controls=mixed_controls, primary_pdfs=parent['primary_pdfs'],
        source_urls=parent['source_urls'],
        maximum_coefficient_error=max(row['maximum_scaled_error'] for row in trajectories['solutions']),
        maximum_resolution=max(row['maximum_scaled_resolution'] for row in trajectories['solutions']),
        maximum_quadrature_error=max(row['relative_error'] for row in trajectories['quadratures']),
        maximum_circular_phase_error=max(row['relative_error'] for row in circular_controls),
        independent_mixed_control_integrations=24, physical_trajectories=4,
        numeric_checks_are_correlated_not_independent_empirical_tests=True,
        uncertainty_scope='Integration precision only; does not bound omitted PN, dynamic tide, absorption or higher-eccentricity terms.')
    if failed:
        print(dict(state='failed', checks=len(checks), failures=failed), flush=True)
        raise SystemExit(1)
    save('validation', __file__, report)
    print(dict(state='complete', checks=len(checks), maximum_coefficient_error=report['maximum_coefficient_error'],
        maximum_resolution=report['maximum_resolution'], maximum_circular_phase_error=report['maximum_circular_phase_error'],
        mixed_errors=[row['detail'] for row in checks if row['name'].startswith('independent mixed')]), flush=True)


if __name__ == '__main__':
    main()
