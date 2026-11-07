from __future__ import annotations

import hashlib
import json
from pathlib import Path

import psutil

from companion_system import ROOT, ResponseProblem, encode


def decode(value):
    return complex(value['real'], value['imaginary'])


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/reduction'
    output.mkdir(exist_ok=False)
    labels = ['main', 'fine', 'wide', 'wide-control', 'reference', 'reference-fine', 'controls']
    reports = {label: json.loads((ROOT/f'results/{label}/status.json').read_text()) for label in labels}
    static = []
    for label, distance, tolerance in [('main', .02, 2e-8), ('fine', .04, 5e-9)]:
        problem = ResponseProblem(distance, tolerance)
        value, _ = problem.evaluate(0.)
        static.append({'label': label, 'lambda': value['rows'][0]['susceptibility'].real,
                       'interior_maximum_residual': value['interior_maximum_residual'],
                       'interior_boundary_residual': value['interior_boundary_residual']})
    differences = []
    for main_row, fine_row in zip(reports['main']['rows']+reports['wide-control']['rows'], reports['fine']['rows']+reports['wide']['rows']):
        main_excess, fine_excess = decode(main_row['amplitude_ratio_minus_one']), decode(fine_row['amplitude_ratio_minus_one'])
        differences.append({'separation_over_radius': main_row['separation_over_radius'],
                            'complex_excess_relative_difference': abs(main_excess/fine_excess-1),
                            'imaginary_excess_relative_difference': abs(main_excess.imag/fine_excess.imag-1),
                            'reference_power_relative_difference': abs(main_row['reference_pair_power_infinity']/fine_row['reference_pair_power_infinity']-1)})
    predictions = []
    for row in reports['fine']['rows']+reports['wide']['rows']:
        amplitude_excess = decode(row['amplitude_ratio_minus_one'])
        leading = 3*static[1]['lambda']/row['orbit']**5
        pn = leading*(1+85/21*row['mass']/row['orbit'])
        predictions.append({'separation_over_radius': row['separation_over_radius'],
                            'leading_amplitude_excess': leading, 'first_PN_amplitude_excess': pn,
                            'computed_real_amplitude_excess': amplitude_excess.real,
                            'computed_pair_power_excess': row['pair_flux_ratio_minus_one'],
                            'relative_error_leading': abs(leading/amplitude_excess.real-1),
                            'relative_error_first_PN': abs(pn/amplitude_excess.real-1),
                            'inferred_first_PN_coefficient': (amplitude_excess.real/leading-1)*row['orbit']/row['mass']})
    report = {'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'source_hashes': {label: hashlib.sha256((ROOT/f'results/{label}/status.json').read_bytes()).hexdigest() for label in labels},
              'static_calculations': static, 'precision_controls': differences, 'wide_orbit_predictions': predictions,
              'interior_evaluations': 2,
              'scope': 'Static normalization is computed from the same body and numerical settings, not fitted to orbital data. All waveform quantities are ell=2,m=+/-2 on a fixed circular test-companion orbit.'}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
