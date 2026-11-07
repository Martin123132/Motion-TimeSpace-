from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
import sympy as sp

from balance import ROOT, BRANCH, PARENT, read_json, digest, save, input_hashes, scalar_flux, modest_process
from check_orbits import zero_intercept


def main():
    modest_process()
    inputs, checks = {}, []

    def load(path):
        result = read_json(path)
        assert result['state'] == 'complete', path
        inputs[str(path)] = digest(path)
        return result

    def check(name, error, tolerance):
        checks.append(dict(name=name, error=float(error), tolerance=tolerance,
                           passed=bool(np.isfinite(error) and abs(error) <= tolerance)))

    derived = load(ROOT/'results/derivation/status.json')
    chirp = load(ROOT/'results/chirp/status.json')
    orbits = load(ROOT/'results/orbits/status.json')
    parent = load(PARENT/'results/stage-integrity.json')
    for report in [derived, chirp, orbits]:
        for path, expected in report['input_hashes'].items():
            assert Path(path).is_file() and digest(path) == expected, path
    assert all(row['passed'] for row in derived['checks']+chirp['checks'])
    exact_count = derived['exact_checks']+chirp['exact_checks']
    assert exact_count == 36 and len(orbits['rows']) == 54
    radius, velocity = sp.symbols('r v', real=True, positive=True)
    local_functions = {}
    for quantity, expressions in derived['local_flux_coefficients'].items():
        local_functions[quantity] = {key:sp.lambdify((radius, velocity), sp.sympify(expression, locals=dict(r=radius, v=velocity)), 'numpy')
                                     for key, expression in expressions.items()}
    local_controls = []
    for position in [.85, 1., 1.25]:
        for speed in [-.15, 0., .2]:
            point = scalar_flux(position, speed, 0., 0.)
            for index, quantity in enumerate(['power', 'torque']):
                expected = float(local_functions[quantity]['point'](position, speed))
                check(f'{quantity} point {position} {speed}', point[index]/expected-1, 1e-12)
                for parameter in ['conservative', 'induced']:
                    step = 2e-4
                    values = {}
                    for multiple in [-2, -1, 1, 2]:
                        chosen = multiple*step
                        values[multiple] = scalar_flux(position, speed, chosen if parameter == 'conservative' else 0.,
                                                       chosen if parameter == 'induced' else 0.)[index]
                    derivative = (values[-2]-8*values[-1]+8*values[1]-values[2])/(12*step)
                    expected = float(local_functions[quantity][parameter](position, speed))
                    error = abs(derivative-expected)/max(abs(expected), 1.)
                    check(f'{quantity} local derivative {parameter} {position} {speed}', error, 1e-9)
                    local_controls.append(dict(quantity=quantity, parameter=parameter, radius=position, velocity=speed, relative_scaled_error=error))
    expected_coefficients = dict(conservative=dict(energy2=3627/8, angular2=1605/8, omega2=39/2, radial0=-3.),
                                 induced=dict(energy2=199/4, angular2=105/4, omega2=0., radial0=0.))
    baseline = dict(energy2=37/24, angular2=-5/8, omega2=-1.5, radial0=1.)
    coefficient_controls = []
    for row in orbits['coefficients']:
        expected = expected_coefficients[row['parameter']][row['quantity']]
        error = abs(row['derivative']-expected)/max(abs(expected), 1.)
        coefficient_controls.append({**row, 'expected':expected, 'scaled_error':error})
        check(f"finite orbit {row['settings']} {row['parameter']} {row['quantity']}", error, 2e-6)
        check(f"point orbit {row['settings']} {row['quantity']}", row['zero_value']/baseline[row['quantity']]-1, 1e-7)
    for index, row in enumerate(orbits['rows']):
        check(f'orbit{index} energy conservation', row['energy_conservation_error'], 1e-10)
        check(f'orbit{index} turning point', row['apocenter_velocity_residual'], 1e-12)
        assert row['z'] > 0 and row['Omega_r'] > 0
        with np.load(ROOT/'results/orbits'/row['archive']) as archive:
            assert all(np.isfinite(archive[key]).all() for key in archive.files)
    damping_extrapolations, damping_controls = [], []
    for label in ['fine', 'coarse']:
        for conservative, induced in sorted({(row['conservative'], row['induced']) for row in orbits['rows']}):
            family = sorted([row for row in orbits['rows'] if row['settings'] == label and row['conservative'] == conservative
                             and row['induced'] == induced], key=lambda row:row['z'])
            coordinates = [row['z'] for row in family]
            values = [(2*(row['energy_flux_ratio']-row['Omega_phi']*row['angular_flux_ratio'])/(row['Omega_r']*row['z'])
                       -row['angular_flux_ratio'])*3/19 for row in family]
            damping_extrapolations.append(dict(settings=label, conservative=conservative, induced=induced,
                                               coefficient=zero_intercept(coordinates, values), raw=values))
        for parameter, expected in [('conservative', 3453/38), ('induced', 153/19)]:
            selected = [row for row in damping_extrapolations if row['settings'] == label
                        and row['induced' if parameter == 'conservative' else 'conservative'] == 0.]
            lookup = {round(row[parameter]/1e-4):row['coefficient'] for row in selected}
            derivative = (lookup[-2]-8*lookup[-1]+8*lookup[1]-lookup[2])/(12e-4)
            error = abs(derivative/expected-1)
            damping_controls.append(dict(settings=label, parameter=parameter, expected=expected, computed=derivative, relative_error=error))
            check('damping derivative '+label+' '+parameter, error, 2e-6)
            check('damping point '+label+' '+parameter, lookup[0]-1, 1e-7)
    resolution = []
    for row in orbits['coefficients']:
        if row['settings'] != 'fine':
            continue
        other = next(value for value in orbits['coefficients'] if value['settings'] == 'coarse' and
                     value['parameter'] == row['parameter'] and value['quantity'] == row['quantity'])
        error = abs(other['derivative']-row['derivative'])/max(1., abs(row['derivative']))
        resolution.append(error)
        check('orbit resolution '+row['parameter']+' '+row['quantity'], error, 2e-6)
    zero = next(row for row in orbits['extrapolations'] if row['settings'] == 'fine' and row['conservative'] == 0 and row['induced'] == 0)
    order_controls = []
    for parameter in ['conservative', 'induced']:
        chosen = [next(row for row in orbits['extrapolations'] if row['settings'] == 'fine' and row[parameter] == multiple*1e-4
                       and row['induced' if parameter == 'conservative' else 'conservative'] == 0) for multiple in [1, 2]]
        for quantity in ['energy2', 'angular2']:
            remainders = [row[quantity]-zero[quantity]-row[parameter]*expected_coefficients[parameter][quantity] for row in chosen]
            ratio = remainders[1]/remainders[0]
            order_controls.append(dict(parameter=parameter, quantity=quantity, remainders=remainders, ratio=ratio))
            check('truncated model quadratic remainder '+parameter+' '+quantity, ratio/4-1, .04)
    for path in ROOT.glob('*.py'):
        compile(path.read_bytes(), str(path), 'exec')
    assert not list(ROOT.rglob('__pycache__'))
    failures = [row for row in checks if not row['passed']]
    if failures:
        print('FAILED', failures, flush=True)
        raise AssertionError('Validation failed; no validation report sealed.')
    background = load(PARENT/'results/action/status.json')['raw_nodes']['fine'][0]
    mass, central_radius, deformability = [background[key] for key in ['mass', 'radius', 'tidal_lambda']]
    illustrations = []
    for mass_ratio in [.001, .01]:
        companion = mass_ratio*mass
        total_mass = mass+companion
        reduced = mass*companion/total_mass
        for separation in [5., 10.]:
            distance = separation*central_radius
            tide = deformability/distance**5
            for squared_eccentricity in [0., .0001]:
                shrink_ratio = 1+(6+60*mass_ratio)*tide+squared_eccentricity*(-5/8+(315/4+6075*mass_ratio/16)*tide)
                gamma_ratio = 1+(459/19+12195*mass_ratio/76)*tide
                illustrations.append(dict(mass_ratio=mass_ratio, action_radius_over_R=separation, z_action=squared_eccentricity,
                    tidal_parameter=tide, distance_rate=-64/5*reduced*total_mass**2/distance**3*shrink_ratio,
                    eccentricity_squared_rate=-608/15*reduced*total_mass**2/distance**4*squared_eccentricity*gamma_ratio,
                    circular_shrink_tidal_fraction=(6+60*mass_ratio)*tide, damping_tidal_fraction=gamma_ratio-1,
                    illustrative_not_fitted=True))
    source_pdf = BRANCH/'orbital-backreaction-20261004/sources/vines-flanagan-hinderer-2011.pdf'
    report = save('validation', __file__, dict(input_hashes={**input_hashes(), **inputs, str(ROOT/'check_orbits.py'):digest(ROOT/'check_orbits.py')},
        exact_checks=exact_count, checks=checks, coefficient_controls=coefficient_controls, damping_controls=damping_controls,
        damping_extrapolations=damping_extrapolations, local_tensor_controls=local_controls, nonlinear_order_controls=order_controls,
        independent_orbit_count=54, maximum_coefficient_scaled_error=max(row['scaled_error'] for row in coefficient_controls),
        maximum_damping_coefficient_error=max(row['relative_error'] for row in damping_controls),
        maximum_numerical_resolution=max(resolution), illustrations=illustrations,
        primary_pdfs=parent['primary_pdfs']+[dict(path=str(source_pdf), sha256=digest(source_pdf), url='https://arxiv.org/abs/1101.1673',
                                              role='Circular tidal action/quadrupole normalization, inherited stage20 comparison')],
        source_urls=parent['source_urls']+['https://arxiv.org/abs/1101.1673', 'https://doi.org/10.1103/PhysRevD.83.084051'],
        new_fitted_parameters=0, new_background_solves=0, new_interior_wave_solves=0,
        scope='Linear static electric tide and O(z) near-circular balance, with mixed lambda*z retained. No dynamical-tide, absorption, higher-PN or detector claim.'))
    with (ROOT/'results/validation/illustrative-rates.csv').open('x', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(illustrations[0]))
        writer.writeheader()
        writer.writerows(illustrations)
    print(len(checks), 'numerical checks pass', {key:value for key,value in report.items() if key.startswith('maximum_')}, flush=True)


if __name__ == '__main__':
    main()
