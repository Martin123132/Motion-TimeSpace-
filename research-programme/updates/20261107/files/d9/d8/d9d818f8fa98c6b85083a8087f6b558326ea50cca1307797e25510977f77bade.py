from __future__ import annotations

import csv
from datetime import datetime, timezone
import json

import psutil
import sympy as sy

from acquire_source import ROOT, digest


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    checks = []

    def check(name, expression):
        residual = sy.simplify(expression)
        checks.append({'name': name, 'passed': residual == 0, 'residual': str(residual)})
        assert residual == 0, (name, residual)

    radius, mass, omega, epsilon, orbit, strength, x = sy.symbols('r M omega epsilon D A x', positive=True)
    metric = 1-2*epsilon*mass/radius
    growing = radius**3*(1-epsilon*omega**2*radius**2/14)
    decaying = radius**-2*(1+epsilon*5*mass/(3*radius)+epsilon*omega**2*radius**2/6)

    def equation(wave):
        return sy.expand(metric**2*sy.diff(wave, radius, 2)+metric*sy.diff(metric, radius)*sy.diff(wave, radius)
                         +(epsilon*omega**2-metric*(6/radius**2-6*epsilon*mass/radius**3))*wave)

    for name, wave in [('growing', growing), ('decaying', decaying)]:
        for order in [0, 1]:
            check(f'{name}_Regge_Wheeler_order_{order}', equation(wave).coeff(epsilon, order))
    wronskian = sy.expand(metric*(growing*sy.diff(decaying, radius)-sy.diff(growing, radius)*decaying))
    check('static_Wronskian_value', wronskian.coeff(epsilon, 0)+5)
    check('first_PN_Wronskian_unchanged', wronskian.coeff(epsilon, 1))
    orbit_metric = 1-2*epsilon*mass/orbit
    jump = strength*orbit/2
    slope = -strength*orbit_metric/2

    def numerator(wave):
        return sy.series(slope*wave.subs(radius, orbit)-jump*(metric*sy.diff(wave, radius)).subs(radius, orbit), epsilon, 0, 2).removeO()

    growing_source = numerator(growing)
    decaying_source = numerator(decaying)
    amplitude_ratio = sy.series(-4*orbit**5*decaying_source/growing_source, epsilon, 0, 2).removeO()
    amplitude_on_orbit = sy.expand(amplitude_ratio.subs(omega**2, mass/orbit**3).subs(mass, x*orbit))
    check('amplitude_1PN_275_over_84', amplitude_on_orbit-1-epsilon*sy.Rational(275, 84)*x)
    source_ratio = sy.series(growing_source/(-2*strength*orbit**3), epsilon, 0, 2).removeO()
    point_power = sy.series(source_ratio**2/(1-3*epsilon*mass/orbit), epsilon, 0, 2).removeO()
    point_on_orbit = sy.expand(point_power.subs(omega**2, mass/orbit**3).subs(mass, x*orbit))
    check('point_current_pair_power_1PN_minus17_over14', point_on_orbit-1+epsilon*sy.Rational(17, 14)*x)
    magnetic_ratio = sy.series(amplitude_on_orbit*point_on_orbit, epsilon, 0, 2).removeO()
    check('magnetic_infinity_increment_1PN_173_over84', magnetic_ratio-1-epsilon*sy.Rational(173, 84)*x)
    check('omitted_value_jump_flat_amplitude_factor', (-strength*orbit**3/2)/(-2*strength*orbit**3)-sy.Rational(1, 4))
    check('omitted_value_jump_flat_power_factor', ((-strength*orbit**3/2)/(-2*strength*orbit**3))**2-sy.Rational(1, 16))
    check('using_U_in_CPM_flux_wrong_power_factor', sy.Rational(1, 2)**2-sy.Rational(1, 4))

    fine_path = ROOT/'results/fine/status.json'
    coarse_path = ROOT/'results/coarse/status.json'
    fine = json.loads(fine_path.read_text(encoding='utf-8'))
    coarse = json.loads(coarse_path.read_text(encoding='utf-8'))
    rows = []
    for high, low in zip(fine['rows'], coarse['rows']):
        parameter = high['x']
        amplitude_pn = 1+275/84*parameter
        point_pn = 1-17/14*parameter
        magnetic_pn = 1+173/84*parameter
        observed = high['infinity_increment_to_leading_magnetic']
        residual = observed-magnetic_pn
        rows.append({'separation_over_radius': high['separation_over_radius'], 'x': parameter,
                     'observed_magnetic_ratio': observed, 'derived_1PN_magnetic_ratio': magnetic_pn,
                     'residual_beyond_1PN': residual, 'residual_over_x_to_three_halves': residual/parameter**1.5,
                     'observed_amplitude_ratio': high['amplitude_real_to_leading_magnetic'],
                     'derived_1PN_amplitude_ratio': amplitude_pn,
                     'amplitude_residual_over_x_squared': (high['amplitude_real_to_leading_magnetic']-amplitude_pn)/parameter**2,
                     'observed_point_power_ratio': high['reference_power_to_STF_leading'],
                     'derived_1PN_point_power_ratio': point_pn,
                     'coarse_fine_magnetic_ratio_difference': abs(observed-low['infinity_increment_to_leading_magnetic']),
                     'quadratic_boundary_error_resolved': high['quadratic_boundary_amplitude_error'] > 3e-12*abs(high['amplitude_excess_real']),
                     'quadratic_boundary_error_over_exact_bound': high['quadratic_boundary_amplitude_error']/high['quadratic_boundary_amplitude_error_bound']})
    output = ROOT/'results/matching'
    output.mkdir(parents=True, exist_ok=False)
    with (output/'rows.csv').open('x', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    report = {'state': 'complete', 'completed_at_utc': datetime.now(timezone.utc).isoformat(),
              'script_sha256': digest(__file__), 'input_hashes': {str(path): digest(path) for path in [fine_path, coarse_path]},
              'exact_checks': len(checks), 'checks': checks, 'rows': rows,
              'derived_first_PN_coefficient': '173/84', 'new_coefficients_fitted': 0,
              'tail_coefficient_derived_or_claimed': False,
              'scope': 'Real leading magnetic infinity-power increment in the test-mass, fixed-body, wide-orbit expansion. Horizon flux reported separately.',
              'roundoff_policy': 'If the interior analytic remainder is below boundary numerical resolution, do not claim a numerical bound verification or inflate it.'}
    (output/'status.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'exact_checks': len(checks), 'rows': rows}))


if __name__ == '__main__':
    main()
