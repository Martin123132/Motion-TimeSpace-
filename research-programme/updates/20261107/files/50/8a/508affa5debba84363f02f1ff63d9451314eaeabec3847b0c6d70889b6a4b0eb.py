from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import mpmath as mp
import psutil
from scipy.integrate import quad
import sympy as sp

from pn_algebra import Jet, derive_circular_model


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def direct_model(pn, tide, central):
    companion = 1-central
    eta = central*companion
    coupling = 3*companion/(2*central)
    theta0, theta1, theta3 = (1-3*eta)/8, (3+eta)/2, -mp.mpf('.5')
    xi1, xi3 = companion*(5+central)/2, -7+5*central
    force = lambda radius: (radius-radius**-2-6*coupling*tide*radius**-7
                              +pn*(4*theta0*radius**3+theta1-2*theta3*radius**-3
                                     +coupling*tide*(-4*xi1*radius**-5-7*xi3*radius**-8)))
    radius = mp.findroot(force, 1+(eta-3)/3*pn+3*companion/central*tide, tol=mp.mpf('1e-55'))
    energy = (radius**2/2-radius**-1-coupling*tide*radius**-6
              +pn*(3*theta0*radius**4+theta1*radius-theta3*radius**-2
                     +coupling*tide*(xi1*radius**-4-xi3*radius**-7)))
    normal = (radius**2+3*tide/(central*radius**3)
              +pn*(mp.mpf(29)/42*(1-3*eta)*radius**4+(8*eta-5)/7*radius
                     +tide*(13*companion**2/(7*central*radius)-3*companion*(8+23*central+13*central**2)/(14*central*radius**4))
                     +3*tide/(central*radius**3)*(2*radius**2-(6-central)/(2*radius))))
    tangent = pn*(mp.mpf(11)/21*(1-3*eta)*radius**4+38*companion**2*tide/(7*central*radius)+3*tide/(central*radius))
    octupole = (1-2*central)*radius**3+9*companion/central*tide/radius**2
    current = (1-2*central)*radius**3+mp.mpf(9)/2*companion/central*tide/radius**2
    flux = (normal-tangent)**2+pn*(mp.mpf(1367)/1008*octupole**2+current**2/36)
    return radius, energy, flux


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/numerical'
    output.mkdir(parents=True, exist_ok=False)
    mp.mp.dps = 65
    central = sp.symbols('chi', positive=True)
    model = derive_circular_model(central)
    checks = []

    def check(name, condition):
        assert condition, name
        checks.append({'name': name, 'passed': True})

    numeric_controls = []
    for central_text in ['0.25', '0.5', '0.9', '0.99']:
        fraction = mp.mpf(central_text)
        expected = [model[key].values for key in ['radius', 'energy', 'flux']]
        for step_text in ['0.0001', '0.00005', '0.000025']:
            step = mp.mpf(step_text)
            values = {(first, second): direct_model(first*step, second*step, fraction)
                      for first, second in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]}
            differences = []
            for index, key in enumerate(['radius', 'energy', 'flux']):
                pn_derivative = (values[1, 0][index]-values[-1, 0][index])/(2*step)
                tidal_derivative = (values[0, 1][index]-values[0, -1][index])/(2*step)
                mixed = (values[1, 1][index]-values[1, -1][index]-values[-1, 1][index]+values[-1, -1][index])/(4*step**2)
                for order, estimate in [(1, pn_derivative), (2, tidal_derivative), (3, mixed)]:
                    reference = mp.mpf(str(sp.N(expected[index][order].subs(central, sp.Rational(central_text)), 62)))
                    differences.append({'quantity': key, 'order': order, 'relative_or_unit_scaled_error': float(abs(estimate-reference)/max(abs(reference), mp.mpf(1)))})
            numeric_controls.append({'central_fraction': central_text, 'step': float(step), 'coefficient_controls': differences})
        last = numeric_controls[-1]
        check('independent_root_and_multipole_coefficients_'+central_text,
              max(row['relative_or_unit_scaled_error'] for row in last['coefficient_controls']) < 1e-5)
        for first, second in zip(numeric_controls[-3:], numeric_controls[-2:]):
            first_max = max(row['relative_or_unit_scaled_error'] for row in first['coefficient_controls'])
            second_max = max(row['relative_or_unit_scaled_error'] for row in second['coefficient_controls'])
            check('centered_difference_second_order_'+central_text+'_'+str(second['step']), .24 < second_max/first_max < .26)
    pn_symbol, tide_symbol = sp.symbols('pn tide')
    jet_checks = 0
    for sample in range(1, 8):
        numerator = Jet(sample+1, 2-sample, sample+3, 2*sample-1)
        denominator = Jet(sample+2, sample-3, 2*sample, 4-sample)
        exact_function = numerator.expression(pn_symbol, tide_symbol)/denominator.expression(pn_symbol, tide_symbol)
        series = numerator/denominator
        for order, pn_order, tide_order in [(0, 0, 0), (1, 1, 0), (2, 0, 1), (3, 1, 1)]:
            reference = sp.diff(exact_function, pn_symbol, pn_order, tide_symbol, tide_order).subs({pn_symbol: 0, tide_symbol: 0})
            check('Jet_independent_Taylor_'+str(sample)+'_'+str(order), sp.simplify(reference-series.values[order]) == 0)
            jet_checks += 1
    inputs = {}
    input_body = BRANCH/'orbital-backreaction-20261004/results/fine/status.json'
    body = json.loads(input_body.read_text())
    inputs[str(input_body)] = digest(input_body)
    mass, radius, tidal_lambda = (body[key] for key in ['mass', 'radius', 'tidal_lambda'])
    wave_controls = []
    for label in ['fine', 'wide']:
        path = BRANCH/f'companion-source-20261004/results/{label}/status.json'
        source = json.loads(path.read_text())
        inputs[str(path)] = digest(path)
        for row in source['rows']:
            if row['separation_over_radius'] < 10:
                continue
            orbit = row['orbit']
            pn = mass/orbit
            point_power = 32/5*mass**3/orbit**5
            tide = tidal_lambda/orbit**5
            actual_linear_tide = 2*row['amplitude_ratio_minus_one']['real']*row['reference_pair_power_infinity']
            leading = point_power*6*tide
            first_pn = leading*(1-22/21*pn)
            record = {'separation_over_radius': row['separation_over_radius'], 'x': pn,
                      'relative_signal_vs_leading': actual_linear_tide/leading,
                      'leading_relative_error': abs(leading/actual_linear_tide-1),
                      'first_PN_relative_error': abs(first_pn/actual_linear_tide-1),
                      'residual_scaled_by_x_three_halves': (actual_linear_tide/leading-(1-22/21*pn))/pn**1.5,
                      'point_quadrupole_ratio': row['reference_pair_power_infinity']/point_power,
                      'point_quadrupole_first_PN_ratio': 1-107/21*pn,
                      'quadratic_wave_term_omitted': abs(complex(row['amplitude_ratio_minus_one']['real'], row['amplitude_ratio_minus_one']['imaginary']))**2*row['reference_pair_power_infinity']}
            wave_controls.append(record)
    for row in wave_controls:
        if row['separation_over_radius'] >= 40:
            check('unfitted_wave_PN_improvement_'+str(row['separation_over_radius']), row['first_PN_relative_error'] < row['leading_relative_error'])
    check('unfitted_wave_remainder_decreases', all(first['first_PN_relative_error'] > second['first_PN_relative_error'] for first, second in zip(wave_controls, wave_controls[1:])))
    check('widest_wave_agreement', wave_controls[-1]['first_PN_relative_error'] < 2e-5)
    examples = []
    for mass_ratio in [.001, .01, .1]:
        fraction = 1/(1+mass_ratio)
        total = mass*(1+mass_ratio)
        eta = mass_ratio/(1+mass_ratio)**2
        coefficients = {key: [float(value.subs(central, fraction)) for value in model[key].values]
                        for key in ['energy', 'flux', 'chirp', 'inverse_chirp', 'electric_flux', 'octupole_flux', 'current_flux']}
        for separation in [5., 10., 20.]:
            orbit = separation*radius
            pn, tide = total/orbit, tidal_lambda/orbit**5
            flux, chirp = coefficients['flux'], coefficients['chirp']
            leading_chirp_fraction = chirp[2]*tide
            consistent_fraction = (chirp[2]+(chirp[3]-chirp[1]*chirp[2])*pn)*tide
            examples.append({'illustrative_mass_ratio': mass_ratio, 'separation_over_radius': separation, 'x': pn, 'lambda_over_d0_fifth': tide,
                             'leading_chirp_fraction_over_point': leading_chirp_fraction,
                             'first_PN_electric_tide_chirp_fraction_over_point': consistent_fraction,
                             'first_PN_relative_change_of_tidal_chirp': consistent_fraction/leading_chirp_fraction-1,
                             'point_flux_ratio_through_1PN': 1+flux[1]*pn,
                             'tidal_flux_normalized_to_Newton_point': (flux[2]+flux[3]*pn)*tide,
                             'electric_quadrupole_mixed_flux': coefficients['electric_flux'][3]*pn*tide,
                             'transported_mass_octupole_mixed_flux': coefficients['octupole_flux'][3]*pn*tide,
                             'transported_current_quadrupole_mixed_flux': coefficients['current_flux'][3]*pn*tide})
    phases = []
    for mass_ratio in [.001, .01]:
        fraction = 1/(1+mass_ratio)
        total = mass*(1+mass_ratio)
        eta = mass_ratio/(1+mass_ratio)**2
        leading_coefficient = float(model['chirp'].values[2].subs(central, fraction))
        mixed_inverse = float(model['inverse_chirp'].values[3].subs(central, fraction))
        scale = tidal_lambda/total**5
        for outer, inner in [(20., 10.), (10., 5.)]:
            first, last = total/(outer*radius), total/(inner*radius)
            leading_phase = -scale*leading_coefficient/(16*eta)*(last**2.5-first**2.5)
            correction = 5*scale*mixed_inverse/(112*eta)*(last**3.5-first**3.5)
            integrand = lambda pn: 5*scale/(32*eta)*(-leading_coefficient*pn**1.5+mixed_inverse*pn**2.5)
            numeric, integration_error = quad(integrand, first, last, epsabs=1e-9, epsrel=2e-12)
            total_phase = leading_phase+correction
            check('phase_quadrature_'+str(mass_ratio)+'_'+str(inner), abs(numeric/total_phase-1) < 1e-12)
            phases.append({'illustrative_mass_ratio': mass_ratio, 'outer_separation_over_radius': outer, 'inner_separation_over_radius': inner,
                           'leading_delta_GW_phase': leading_phase, 'additional_1PN_electric_delta_GW_phase': correction,
                           'total_through_1PN_electric_delta_GW_phase': total_phase,
                           'quadrature_relative_difference': abs(numeric/total_phase-1), 'quadrature_reported_absolute_error': integration_error,
                           'scope': 'Adiabatic electric-tide-only dimensionless prediction over long fixed-frequency intervals, not a calibrated observational phase estimate.'})
    check('all_example_chirp_excesses_positive', all(row['first_PN_electric_tide_chirp_fraction_over_point'] > 0 for row in examples))
    check('all_example_point_fluxes_positive', all(row['point_flux_ratio_through_1PN'] > 0 for row in examples))
    check('no_unstable_signal_subtraction', all(row['quadratic_wave_term_omitted'] >= 0 for row in wave_controls))
    for name, rows in [('predictions', examples), ('wave-controls', wave_controls), ('phase-illustrations', phases)]:
        with (ROOT/f'results/{name}.csv').open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    report = {'state': 'complete', 'script_sha256': digest(__file__), 'algebra_sha256': digest(ROOT/'pn_algebra.py'),
              'checks': checks, 'input_hashes': inputs, 'direct_root_controls': numeric_controls, 'Jet_Taylor_checks': jet_checks,
              'wave_controls': wave_controls, 'illustrations': examples, 'phase_illustrations': phases,
              'new_interior_solves': 0, 'existing_body_response_reused': True,
              'scope': 'Electric tide only; universal 1PN GR matching retained, no independent axial Love response set to zero.'}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'checks': len(checks), 'wave_controls': wave_controls,
                      'mass_ratio_0p01_at_10R': examples[4], 'phases': phases}))


if __name__ == '__main__':
    main()
