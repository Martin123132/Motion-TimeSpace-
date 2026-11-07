from __future__ import annotations

import csv
import json
import math

import mpmath as mp
import numpy as np
from scipy.integrate import quad
import sympy as sp

from common import BRANCH, ROOT, configure_worker, digest, read_json, write_new_json


def main():
    configure_worker()
    mp.mp.dps = 60
    checks = []

    def check(name, passed, **details):
        checks.append({'name': name, 'passed': bool(passed), **details})
        assert passed, (name, details)

    inputs = [ROOT/'results/combined/status.json', ROOT/'results/derivation/status.json',
              BRANCH/'axial-tides-20261004/results/fine-v2/status.json',
              BRANCH/'orbital-backreaction-20261004/results/fine/status.json',
              BRANCH/'pn-balance-20261004/results/predictions.csv']
    combined = read_json(inputs[0])
    coefficients = read_json(inputs[1])
    axial = read_json(inputs[2])['rows'][-1]
    electric_parent = read_json(inputs[3])
    body_mass, body_radius = axial['mass'], axial['radius']
    sigma_bar = axial['geometric_sigma_bar']
    tidal_lambda = electric_parent['tidal_lambda']
    check('same_reference_body_mass', body_mass == electric_parent['mass'])
    check('same_reference_body_radius', body_radius == electric_parent['radius'])
    check('inherited_sigma_normalization', sigma_bar == -axial['response']/6)
    chi_symbol = sp.Symbol('chi')
    evaluators = {name: sp.lambdify(chi_symbol, [sp.sympify(value) for value in entries], 'math')
                  for name, entries in combined['model'].items()}
    raw = {name: sp.lambdify(chi_symbol, sp.sympify(value), 'mpmath') for name, value in coefficients['coefficients'].items()}
    numerical_controls = []
    for fraction_text in ['0.25', '0.5', '0.9', '0.99']:
        fraction = mp.mpf(fraction_text)
        companion = 1-fraction
        for pn_text in ['0.001', '0.01', '0.03']:
            pn = mp.mpf(pn_text)
            increment = mp.mpf('1e-12')

            def orbit(magnetic):
                return mp.findroot(lambda radius: radius-radius**-2-24*companion/fraction*pn*magnetic/radius**5,
                                   (mp.mpf('.99'), mp.mpf('1.01')))

            def energy(magnetic):
                radius = orbit(magnetic)
                return radius**2/2-1/radius+6*companion/fraction*pn*magnetic/radius**4

            def flux(magnetic, phase):
                radius = orbit(magnetic)
                sine, cosine = mp.sin(phase), mp.cos(phase)
                normal = mp.matrix([cosine, sine, 0])
                tangent = mp.matrix([-sine, cosine, 0])
                vertical = mp.matrix([0, 0, 1])
                mixed = normal*tangent.T+tangent*normal.T
                mass_third = -4*mixed*(radius**2+8*companion/(3*fraction)*pn*magnetic/radius)
                axial_third = -(tangent*vertical.T+vertical*tangent.T)/2
                current_third = axial_third*((1-2*fraction)*radius**3+6*magnetic/(fraction*radius**2))
                mass_norm = sum(value**2 for value in mass_third)
                current_norm = sum(value**2 for value in current_third)
                return mass_norm/32+pn*current_norm/18

            radius_numeric = (orbit(increment)-orbit(-increment))/(2*increment*pn)
            energy_numeric = (energy(increment)-energy(-increment))/(2*increment*pn)
            radius_error = abs(radius_numeric-raw['radius'](fraction))
            energy_error = abs(energy_numeric-raw['energy'](fraction))
            flux_errors = []
            discarded_order = mp.mpf(4)/3*companion/fraction*(1-2*fraction)**2*pn
            for phase_text in ['0', '0.37', '1.23']:
                phase = mp.mpf(phase_text)
                flux_numeric = (flux(increment, phase)-flux(-increment, phase))/(2*increment*pn)
                flux_errors.append(abs(flux_numeric-raw['flux'](fraction)-discarded_order))
            check(f'independent_roots_and_tensor_flux_chi{fraction_text}_x{pn_text}',
                  max(radius_error, energy_error, *flux_errors) < mp.mpf('1e-18'),
                  radius_error=float(radius_error), energy_error=float(energy_error), flux_error=float(max(flux_errors)))
            numerical_controls.append({'chi': float(fraction), 'x': float(pn), 'radius_coefficient': float(radius_numeric),
                                       'energy_coefficient': float(energy_numeric), 'flux_coefficient_after_order_projection': float(flux_numeric-discarded_order),
                                       'raw_flux_higher_order_removed': float(discarded_order), 'max_absolute_error': float(max(radius_error, energy_error, *flux_errors))})
    predictions = []
    phases = []
    for ratio in [0.0001, 0.001, 0.01, 0.1, 1.0]:
        fraction = 1/(1+ratio)
        eta = fraction*(1-fraction)
        total_mass = body_mass*(1+ratio)
        values = {name: evaluator(fraction) for name, evaluator in evaluators.items()}
        for separation in [5.0, 10.0, 20.0, 40.0]:
            reference_radius = separation*body_radius
            pn = total_mass/reference_radius
            electric = tidal_lambda/reference_radius**5
            magnetic = sigma_bar/reference_radius**5
            basis = np.array([1, pn, electric, pn*electric, pn*magnetic])
            evaluated = {name: float(np.dot(array, basis)) for name, array in values.items()}
            electric_chirp = values['chirp'][2]*electric+values['chirp'][3]*pn*electric
            magnetic_chirp = values['chirp'][4]*pn*magnetic
            magnetic_flux = values['flux'][4]*pn*magnetic
            point_chirp = 1+values['chirp'][1]*pn
            row = {'companion_to_body_mass': ratio, 'd0_over_body_radius': separation,
                   'x': pn, 'lambda_over_d0_5': electric, 'sigma_bar_over_d0_5': magnetic,
                   'point_chirp_factor': point_chirp, 'electric_chirp_increment_over_Newtonian': electric_chirp,
                   'magnetic_chirp_increment_over_Newtonian': magnetic_chirp,
                   'total_chirp_factor': evaluated['chirp'], 'magnetic_to_electric_chirp': magnetic_chirp/electric_chirp,
                   'magnetic_flux_increment_over_Newtonian': magnetic_flux,
                   'total_flux_factor': evaluated['flux'], 'energy_over_reduced_mass_x': evaluated['energy'],
                   'positive_energy_slope_factor': evaluated['energy_slope'],
                   'Omega_times_body_radius': pn**1.5*body_radius/total_mass,
                   'magnetic_delta_Fourier_phase_rad': 3/(128*eta)*values['fourier_phase'][4]*magnetic*pn**(-1.5),
                   'magnetic_relative_to_unit_2PN_electric': abs(magnetic_chirp/(electric*pn**2))}
            predictions.append(row)
            check(f'weak_sample_physical_signs_mu{ratio}_d{separation}',
                  evaluated['flux'] > 0 and evaluated['chirp'] > 0 and evaluated['energy_slope'] > 0
                  and evaluated['energy'] < 0 and pn < 0.007 and abs(electric) < 1e-5 and abs(magnetic) < 1e-7)
        for outer, inner in [(20.0, 10.0), (10.0, 5.0)]:
            low = total_mass/(outer*body_radius)
            high = total_mass/(inner*body_radius)
            electric_leading = values['inverse_chirp'][2]*tidal_lambda/total_mass**5
            electric_pn = values['inverse_chirp'][3]*tidal_lambda/total_mass**5
            magnetic_coefficient = values['inverse_chirp'][4]*sigma_bar/total_mass**5
            factor = 5/(32*eta)
            electric_phase = factor*(electric_leading*(high**2.5-low**2.5)/2.5
                                     +electric_pn*(high**3.5-low**3.5)/3.5)
            magnetic_phase = factor*magnetic_coefficient*(high**3.5-low**3.5)/3.5
            quadrature, quadrature_error = quad(lambda frequency: factor*magnetic_coefficient*frequency**2.5,
                                                low, high, epsabs=1e-20, epsrel=1e-12)
            relative_error = abs(quadrature-magnetic_phase)/max(abs(magnetic_phase), 1e-30)
            check(f'phase_quadrature_mu{ratio}_d{outer}to{inner}', relative_error < 2e-12,
                  relative_error=relative_error, quadrature_error=quadrature_error)
            phases.append({'companion_to_body_mass': ratio, 'outer_d0_over_radius': outer, 'inner_d0_over_radius': inner,
                           'electric_delta_accumulated_GW_phase_rad': electric_phase,
                           'magnetic_delta_accumulated_GW_phase_rad': magnetic_phase,
                           'combined_delta_accumulated_GW_phase_rad': electric_phase+magnetic_phase,
                           'quadrature_relative_error': relative_error})
    for name, rows in [('predictions', predictions), ('phase-bands', phases), ('independent-controls', numerical_controls)]:
        path = ROOT/f'results/{name}.csv'
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('x', encoding='utf-8', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    reference = next(row for row in predictions if row['companion_to_body_mass'] == .01 and row['d0_over_body_radius'] == 10)
    check('electric_reference_regression', math.isclose(reference['electric_chirp_increment_over_Newtonian'], 1.4179789999e-6, rel_tol=2e-10))
    small = next(row for row in predictions if row['companion_to_body_mass'] == .0001 and row['d0_over_body_radius'] == 10)
    check('negative_sigma_does_not_fix_chirp_sign', small['magnetic_chirp_increment_over_Newtonian'] > 0 > reference['magnetic_chirp_increment_over_Newtonian'])
    intermediate = next(row for row in predictions if row['companion_to_body_mass'] == .001 and row['d0_over_body_radius'] == 10)
    check('flux_and_chirp_can_have_opposite_magnetic_signs', intermediate['magnetic_flux_increment_over_Newtonian'] > 0 > intermediate['magnetic_chirp_increment_over_Newtonian'])
    check('all_prediction_values_finite', all(math.isfinite(value) for row in predictions for value in row.values()))
    report = {'state': 'complete', 'script_sha256': digest(__file__), 'common_sha256': digest(ROOT/'common.py'),
              'input_hashes': {str(path): digest(path) for path in inputs}, 'checks': checks,
              'body': {'mass': body_mass, 'radius': body_radius, 'geometric_lambda': tidal_lambda, 'geometric_sigma_bar': sigma_bar},
              'reference': reference, 'phase_bands': phases, 'independent_controls': numerical_controls,
              'csv_hashes': {f'results/{name}.csv': digest(ROOT/f'results/{name}.csv') for name in ['predictions', 'phase-bands', 'independent-controls']},
              'conditional_adiabatic_evaluation': True, 'new_body_coefficients_fitted': False,
              'interpretation': 'Single deformable body plus point companion, weak-field nonspinning circular adiabatic reduction. Isolated magnetic term is not a total waveform error estimate.',
              'independent_control_scope': 'Unexpanded circular roots and explicit rotating STF tensors; discard a known x^2*sigma orbital-current term before matching the declared order.'}
    write_new_json(ROOT/'results/evaluation/status.json', report)
    print(json.dumps({'state': 'complete', 'checks': len(checks), 'prediction_rows': len(predictions), 'phase_rows': len(phases), 'reference': reference}))


if __name__ == '__main__':
    main()
