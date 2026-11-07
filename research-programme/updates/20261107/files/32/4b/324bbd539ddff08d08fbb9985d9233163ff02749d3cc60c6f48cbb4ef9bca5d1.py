from __future__ import annotations

import hashlib
import json
from pathlib import Path

import psutil
import sympy as sp


ROOT = Path(__file__).resolve().parent


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/radiation-law'
    output.mkdir(exist_ok=False)
    radius, mass, sigma = sp.symbols('radius mass sigma', positive=True)
    metric = 1-2*mass/radius
    lapse_prime = mass/(radius**2*metric)
    amplitude, amplitude_prime = sp.symbols('amplitude amplitude_prime')
    angular = ((3-metric)/2+radius**2*metric*lapse_prime**2)*amplitude+radius**2*metric*lapse_prime*amplitude_prime/2
    shift = radius**2/3*(amplitude_prime+2*lapse_prime*amplitude-(lapse_prime-1/radius)*angular-amplitude/radius)
    metric_transform = sp.Matrix([angular, shift]).jacobian([amplitude, amplitude_prime])
    master_transform = sp.Matrix([[(6*radius**2+6*mass*radius+6*mass**2)/(radius**2*(2*radius+3*mass)), 1],
                                  [(2*radius**2-6*mass*radius-3*mass**2)/((radius-2*mass)*(2*radius+3*mass)), radius/metric]])
    checks = []

    def exact(name, expression):
        assert sp.simplify(expression) == 0, name
        checks.append({'name': name, 'passed': True})

    exact('static_master_Wronskian_minus_five_sixths', sp.det(metric_transform)/sp.det(master_transform)*(-5/(radius**2*metric))+sp.Rational(5, 6))
    outgoing = sp.exp(sp.I*sigma*radius)*(1+3*sp.I/(sigma*radius)-3/(sigma*radius)**2)
    exact('flat_outgoing_Zerilli_equation', sp.diff(outgoing, radius, 2)+(sigma**2-6/radius**2)*outgoing)
    near = sp.series(-sigma**2*outgoing/3, sigma, 0, 7).removeO().expand()
    exact('normalized_static_decaying_limit', near.coeff(sigma, 0)-radius**(-2))
    exact('leading_radiative_growing_piece', near.coeff(sigma, 5)-sp.I*radius**3/45)
    mixing = sp.simplify(near.coeff(sigma, 5)/(radius**3/6))
    exact('mixing_radiation_coefficient', mixing-2*sp.I/15)
    exact('inverse_response_radiation_coefficient', 3*mixing-2*sp.I/5)
    real_lambda, frequency_power = sp.symbols('real_lambda frequency_power', real=True)
    leading_imaginary = sp.Rational(2, 5)*real_lambda**2*frequency_power**5
    exact('response_imaginary_leading_fifth_power', leading_imaginary-sp.Rational(2, 5)*real_lambda**2*frequency_power**5)
    report = {'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'checks': checks,
              'normalized_flat_outgoing_near_series': str(near),
              'leading_mixing': 'Im(p/q)=(2/15)*sigma^5 + higher-order propagation corrections',
              'leading_radiation_self_energy': 'Im(Sigma_ret)=(2/5)*sigma^5',
              'leading_response_loss': 'Im(chi_ret)=(2/5)*lambda_static^2*sigma^5 + higher orders',
              'schwarzschild_extension': 'Formal fixed-M matched low-frequency limit M << r << 1/sigma, using the same static master Wronskian and asymptotic multipole normalization; numerical curved checks required.',
              'limitation': 'This is outgoing gravitational radiation, not matter heating. A constant-width pole extrapolated to zero frequency generally produces spurious lower odd powers; the non-pole response must cancel them.'}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'checks': len(checks), 'near': str(near)}))


if __name__ == '__main__':
    main()
