from __future__ import annotations

import json
import sys

import sympy as sp

from common import BRANCH, ROOT, configure_worker, digest, read_json, write_new_json, zero_check


sys.path.insert(0, str(BRANCH/'pn-balance-20261004'))
from pn_algebra import derive_circular_model


BASIS = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 1))
ORDER = (0, 1, 5, 6, 6)


class Series:
    def __init__(self, values):
        assert len(values) == len(BASIS)
        self.values = tuple(sp.sympify(value) for value in values)

    def __add__(self, other):
        return Series([first+second for first, second in zip(self.values, other.values)])

    def __mul__(self, other):
        result = {key: 0 for key in BASIS}
        for first_key, first in zip(BASIS, self.values):
            for second_key, second in zip(BASIS, other.values):
                key = tuple(first_index+second_index for first_index, second_index in zip(first_key, second_key))
                if key in result:
                    result[key] += first*second
        return Series([sp.factor(result[key]) for key in BASIS])

    def inverse(self):
        constant = self.values[0]
        perturbation = Series([0, *[value/constant for value in self.values[1:]]])
        square = perturbation*perturbation
        return Series([sp.factor(((1 if index == 0 else 0)-first+second)/constant)
                       for index, (first, second) in enumerate(zip(perturbation.values, square.values))])

    def expression(self, pn, electric, magnetic):
        return sum(value*pn**powers[0]*electric**powers[1]*magnetic**powers[2]
                   for powers, value in zip(BASIS, self.values))


def construct_model(chi, magnetic_coefficients):
    parent = derive_circular_model(chi)
    energy = Series([*parent['energy'].values, magnetic_coefficients['energy']])
    flux = Series([*parent['flux'].values, magnetic_coefficients['flux']])
    energy_slope = Series([-2*(order+1)*coefficient for order, coefficient in zip(ORDER, energy.values)])
    chirp = flux*energy_slope.inverse()
    inverse_chirp = chirp.inverse()
    phase = Series([sp.factor(20*coefficient/((2*order-5)*(order-4)))
                    for order, coefficient in zip(ORDER, inverse_chirp.values)])
    return parent, {'energy': energy, 'flux': flux, 'energy_slope': energy_slope,
                    'chirp': chirp, 'inverse_chirp': inverse_chirp, 'fourier_phase': phase}


def main():
    configure_worker()
    chi = sp.Symbol('chi', real=True)
    input_path = ROOT/'results/derivation/status.json'
    derived = read_json(input_path)
    coefficients = {name: sp.sympify(value, locals={'chi': chi}) for name, value in derived['coefficients'].items()}
    parent, model = construct_model(chi, coefficients)
    checks = []
    for name in ['energy', 'flux', 'energy_slope', 'chirp', 'inverse_chirp']:
        for index, value in enumerate(parent[name].values):
            zero_check(checks, f'electric_parent_recovered_{name}_{index}', model[name].values[index]-value)
    zero_check(checks, 'electric_parent_recovered_phase_tide', model['fourier_phase'].values[2]-parent['fourier_phase_tide'])
    zero_check(checks, 'electric_parent_recovered_phase_mixed', model['fourier_phase'].values[3]-parent['fourier_phase_mixed'])
    for name in ['chirp', 'inverse_chirp', 'fourier_phase']:
        zero_check(checks, f'magnetic_alone_matches_derived_{name}', model[name].values[4]-coefficients[name])
    identity = model['chirp']*model['inverse_chirp']
    for index, value in enumerate(identity.values):
        zero_check(checks, f'inverse_series_{index}', value-(1 if index == 0 else 0))
    eta = chi*(1-chi)
    zero_check(checks, 'point_GR_energy', model['energy'].values[1]-(9+eta)/24)
    zero_check(checks, 'point_GR_flux', model['flux'].values[1]+sp.Rational(1247, 336)+35*eta/12)
    zero_check(checks, 'point_GR_chirp', model['chirp'].values[1]+sp.Rational(743, 336)+11*eta/4)
    zero_check(checks, 'point_GR_phase', model['fourier_phase'].values[1]-sp.Rational(3715, 756)-55*eta/9)
    pn, electric, magnetic, total_mass, tidal_lambda, sigma_bar = sp.symbols('x electric magnetic MT lambda_geom sigma_bar', positive=True)
    substitutions = {electric: tidal_lambda*pn**5/total_mass**5, magnetic: sigma_bar*pn**5/total_mass**5}
    physical_energy = eta*total_mass*pn*model['energy'].expression(pn, electric, magnetic).subs(substitutions)
    derivative_slope = -2*sp.diff(physical_energy, pn)/(eta*total_mass)
    zero_check(checks, 'differentiate_fixed_body_coefficients', derivative_slope-model['energy_slope'].expression(pn, electric, magnetic).subs(substitutions))
    fourier_phase = 3*pn**(-sp.Rational(5, 2))/(128*eta)*model['fourier_phase'].expression(pn, electric, magnetic).subs(substitutions)
    frequency_derivative = lambda expression: 2*total_mass/(3*sp.sqrt(pn))*sp.diff(expression, pn)
    phase_second = frequency_derivative(frequency_derivative(fourier_phase))
    expected_second = 5*total_mass**2*pn**(-sp.Rational(11, 2))/(48*eta)*model['inverse_chirp'].expression(pn, electric, magnetic).subs(substitutions)
    zero_check(checks, 'SPA_frequency_second_derivative', phase_second-expected_second)
    primitives = [sp.Rational(5, 32)*coefficient*pn**(order-sp.Rational(5, 2))/(eta*(order-sp.Rational(5, 2)))
                  for order, coefficient in zip(ORDER, model['inverse_chirp'].values)]
    primitive_factors = [1, 1, tidal_lambda/total_mass**5, tidal_lambda/total_mass**5, sigma_bar/total_mass**5]
    time_phase = sum(factor*term for factor, term in zip(primitive_factors, primitives))
    zero_check(checks, 'time_domain_phase_derivative', sp.diff(time_phase, pn)-sp.Rational(5, 32)/eta*pn**(-sp.Rational(7, 2))*model['inverse_chirp'].expression(pn, electric, magnetic).subs(substitutions))
    zero_check(checks, 'flux_sign_threshold', coefficients['flux'].subs(chi, sp.Rational(113, 114)))
    zero_check(checks, 'chirp_sign_threshold', coefficients['chirp'].subs(chi, sp.Rational(1037, 1038)))
    unit = Series([1, 0, 0, 0, 0])
    for first_index in range(5):
        basis_element = Series([int(index == first_index) for index in range(5)])
        for index, value in enumerate((unit*basis_element).values):
            zero_check(checks, f'series_unit_{first_index}_{index}', value-basis_element.values[index])
    examples = [Series([2, 3, 5, 7, 11]), Series([3, -2, 7, 5, -13])]
    for example_index, example in enumerate(examples):
        product = example*example.inverse()
        for index, value in enumerate(product.values):
            zero_check(checks, f'series_nonunit_inverse_{example_index}_{index}', value-unit.values[index])
    omitted = {'lambda_sigma_cross': (1, 1, 1), 'magnetic_next_PN': (2, 0, 1),
               'electric_squared': (0, 2, 0), 'point_2PN': (2, 0, 0)}
    for name, exponent in omitted.items():
        assert exponent not in BASIS
        checks.append({'name': f'order_excludes_{name}', 'passed': True, 'exponent': exponent})
    negative_controls = {
        'unchanged_radiation_energy_only': -coefficients['energy_slope']-coefficients['chirp'],
        'missing_orbital_shift_flux': coefficients['intrinsic_mass_flux']+coefficients['intrinsic_current_flux']-coefficients['flux'],
        'current_only_flux': coefficients['intrinsic_current_flux']-coefficients['flux'],
        'wrong_sigma_factor_two': coefficients['chirp'],
        'holding_dimensionless_tide_constant_in_energy_derivative': -2*coefficients['energy']-coefficients['energy_slope']}
    for name, error in negative_controls.items():
        assert sp.factor(error).subs(chi, sp.Rational(9, 10)) != 0
        checks.append({'name': f'reject_{name}', 'passed': True, 'nonzero_coefficient_error': str(sp.factor(error))})
    report = {'state': 'complete', 'script_sha256': digest(__file__), 'common_sha256': digest(ROOT/'common.py'),
              'input_hashes': {str(input_path): digest(input_path), str(BRANCH/'pn-balance-20261004/pn_algebra.py'): digest(BRANCH/'pn-balance-20261004/pn_algebra.py')},
              'basis': ['1', 'x', 'lambda_geom/d0^5', 'x*lambda_geom/d0^5', 'x*sigma_bar_geom/d0^5'],
              'model': {name: [str(sp.factor(value)) for value in series.values] for name, series in model.items()},
              'time_domain_phase_primitive': str(sp.factor(time_phase)), 'checks': checks,
              'power_counting': 'Instantaneous point1PN, electric leading+1PN, leading magnetic; linear responses; no tail or lambda*sigma.',
              'negative_control_count': len(negative_controls)}
    write_new_json(ROOT/'results/combined/status.json', report)
    print(json.dumps({'state': 'complete', 'exact_and_algebra_checks': len(checks), 'chirp': report['model']['chirp'], 'phase': report['model']['fourier_phase']}))


if __name__ == '__main__':
    main()
