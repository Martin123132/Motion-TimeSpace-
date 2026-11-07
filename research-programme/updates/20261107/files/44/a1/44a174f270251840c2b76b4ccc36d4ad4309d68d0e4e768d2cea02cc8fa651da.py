from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import mpmath as mp
import psutil
import sympy as sp


ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/shared-tail'
    output.mkdir(parents=True, exist_ok=False)
    checks = []

    def check(name, condition):
        assert condition, name
        checks.append({'name': name, 'passed': True})

    mass, frequency, length, pn = sp.symbols('M omega b x', positive=True)
    constant = sp.symbols('kappa', real=True)
    exponent, laplace = sp.symbols('a s', positive=True)
    transform = sp.diff(sp.gamma(exponent+1)*laplace**(-exponent-1), exponent).subs(exponent, 0)
    check('log_Laplace_transform', sp.simplify(transform-(-sp.EulerGamma-sp.log(laplace))/laplace) == 0)
    logarithm_limit = sp.log(frequency)-sp.I*sp.pi/2
    kernel_limit = (-sp.EulerGamma-logarithm_limit-sp.log(2*length)+constant)/(-sp.I*frequency)
    amplitude_correction = sp.expand_complex(-2*mass*frequency**2*kernel_limit)
    check('real_tail_amplitude', sp.simplify(sp.re(amplitude_correction)-sp.pi*mass*frequency) == 0)
    check('arbitrary_log_scale_only_changes_phase', sp.simplify(sp.diff(sp.re(amplitude_correction), length)) == 0)
    check('coordinate_constant_only_changes_phase', sp.simplify(sp.diff(sp.re(amplitude_correction), constant)) == 0)
    flux_correction = 2*sp.re(amplitude_correction)
    check('circular_quadrupole_4pi', sp.simplify(flux_correction.subs(frequency, 2*pn**sp.Rational(3, 2)/mass)-4*sp.pi*pn**sp.Rational(3, 2)) == 0)
    mp.mp.dps = 60
    damping_controls = []
    for omega_text, length_text in [('0.03', '2.0'), ('0.2', '0.7')]:
        omega, scale = mp.mpf(omega_text), mp.mpf(length_text)
        real_limit = mp.pi*omega
        errors = []
        for ratio_text in ['0.0001', '0.00001', '0.000001']:
            ratio = mp.mpf(ratio_text)
            argument = omega*(ratio-1j)
            integral = (-mp.euler-mp.log(argument)-mp.log(2*scale)+mp.mpf(11)/12)/argument
            amplitude = -2*omega**2*integral
            error = abs(mp.re(amplitude)/real_limit-1)
            errors.append(float(error))
        check('Abel_damped_limit_'+omega_text, errors[-1] < 1e-5 and errors[2] < errors[1] < errors[0])
        damping_controls.append({'frequency': omega_text, 'scale': length_text, 'relative_errors': errors})
    path = ROOT/'results/numerical-fine/status.json'
    saved = json.loads(path.read_text())
    controls = []
    coefficient = float(4*mp.pi)
    for row in saved['wave_controls']:
        pn_value = row['x']
        tail = coefficient*pn_value**1.5
        for sector, actual, first_pn in [
            ('point_GR_quadrupole', row['point_quadrupole_ratio'], row['point_quadrupole_first_PN_ratio']),
            ('linear_electric_body_minus_BH', row['relative_signal_vs_leading'], 1-22/21*pn_value)
        ]:
            prediction = first_pn+tail
            remainder = actual-prediction
            first_error = abs(first_pn/actual-1)
            tail_error = abs(prediction/actual-1)
            controls.append({'sector': sector, 'separation_over_radius': row['separation_over_radius'],
                             'x': pn_value, 'actual_normalized_flux': actual,
                             'first_PN_prediction': first_pn, 'first_PN_plus_leading_tail': prediction,
                             'first_PN_relative_error': first_error, 'tail_corrected_relative_error': tail_error,
                             'measured_tail_scaled_remainder': (actual-first_pn)/pn_value**1.5,
                             'tail_coefficient_derived_not_fitted': coefficient,
                             'residual_over_x_squared': remainder/pn_value**2})
            check('tail_improves_'+sector+'_'+str(row['separation_over_radius']), tail_error < first_error)
    for sector in ['point_GR_quadrupole', 'linear_electric_body_minus_BH']:
        selected = [row for row in controls if row['sector'] == sector]
        check('remainder_decreases_'+sector, all(first['tail_corrected_relative_error'] > second['tail_corrected_relative_error'] for first, second in zip(selected, selected[1:])))
        check('widest_tail_control_'+sector, selected[-1]['tail_corrected_relative_error'] < 2e-7)
        check('wide_limit_coefficient_near_4pi_'+sector, abs(selected[-1]['measured_tail_scaled_remainder']/coefficient-1) < .03)
    with (ROOT/'results/shared-tail-controls.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(controls[0]))
        writer.writeheader()
        writer.writerows(controls)
    report = {'state': 'complete', 'script_sha256': digest(__file__), 'checks': checks,
              'input_hashes': {str(path): digest(path)}, 'amplitude_correction': str(amplitude_correction),
              'leading_tail_flux_fraction': str(flux_correction),
              'circular_tail_coefficient': '4*pi, derived from the retained GR convolution; not fitted',
              'damped_limit_controls': damping_controls, 'controls': controls,
              'role': 'Shared propagation diagnostic on both point GR and electric tidal difference; no complete all-sector 1.5PN inspiral claim.',
              'GR_convolution_source': 'Blanchet2006 Eq97, first hereditary term; source and canonical mass quadrupoles coincide at the leading-tail order used here.'}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'checks': len(checks), 'widest_controls': controls[-2:]}))


if __name__ == '__main__':
    main()
