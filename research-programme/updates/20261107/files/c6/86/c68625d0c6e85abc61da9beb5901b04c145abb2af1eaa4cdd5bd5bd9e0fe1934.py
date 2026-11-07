from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import psutil

from response_system_v3 import ResponseProblem, ROOT, PARENT, encode


def decode(value):
    return complex(value['real'], value['imaginary'])


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/low-frequency'
    output.mkdir(exist_ok=False)
    problem = ResponseProblem()
    evaluations, cache = [], {}

    def evaluate(sigma):
        if sigma not in cache:
            row, solution = problem.evaluate(sigma)
            evaluations.append(encode(row))
            cache[sigma] = row
            print(json.dumps(encode({'sigma': sigma, 'responses': [item['susceptibility'] for item in row['rows']]})), flush=True)
        return cache[sigma]

    static = evaluate(0.)
    for sigma in [5e-5, 1e-4, 2e-4, 4e-4]:
        evaluate(sigma)
    residue_path = ROOT/'results/residue/status.json'
    residue_data = json.loads(residue_path.read_text())
    pole = decode(residue_data['pole'])
    residues = [decode(value) for value in residue_data['contour_controls'][-1]['residues']]
    rows = []
    for index, fraction in enumerate([2., 3., 4.]):
        lambda0 = static['rows'][index]['susceptibility'].real
        fits = []
        for step in [5e-5, 1e-4, 2e-4]:
            first = (evaluate(step)['rows'][index]['susceptibility'].real-lambda0)/step**2
            second = (evaluate(2*step)['rows'][index]['susceptibility'].real-lambda0)/(2*step)**2
            fits.append({'step': step, 'quadratic_coefficient': (4*first-second)/3})
        pole_static = -2*(residues[index]/pole).real
        pole_quadratic = -2*(residues[index]/pole**3).real
        low_sigma = 1e-4
        pole_low = residues[index]/(low_sigma-pole)-np.conj(residues[index])/(low_sigma+np.conj(pole))
        rows.append({'buffer_over_radius': fraction, 'lambda_static': lambda0, 'quadratic_controls': fits,
                     'pole_pair_static_contribution': pole_static, 'pole_pair_static_fraction': pole_static/lambda0,
                     'regular_remainder_static': lambda0-pole_static, 'pole_pair_quadratic_contribution': pole_quadratic,
                     'regular_remainder_quadratic': fits[0]['quadratic_coefficient']-pole_quadratic,
                     'pole_pair_imaginary_at_sigma0001': pole_low.imag,
                     'full_imaginary_at_sigma0001': evaluate(low_sigma)['rows'][index]['susceptibility'].imag})
    radiation_rows = []
    for sigma in [5e-5, 1e-4, 2e-4, 4e-4]:
        result = evaluate(sigma)
        radiation_rows.append({'sigma': sigma, 'inverse_radiation_coefficient_by_buffer': [3*row['outgoing_mixing'].imag/sigma**5 for row in result['rows']],
                               'loss_over_static_lambda_squared_sigma_fifth': [row['susceptibility'].imag/(static['rows'][index]['susceptibility'].real**2*sigma**5) for index, row in enumerate(result['rows'])]})
    benchmarks = []
    for index, separation in enumerate([10., 20., 40.]):
        sigma = 2*np.sqrt(2*problem.mass/(separation*problem.radius)**3)
        row = evaluate(sigma)
        static_green = static['shell_rows'][index]['master_surface_per_unit_source_jump']
        first = (evaluate(1e-4)['shell_rows'][index]['master_surface_per_unit_source_jump'].real-static_green.real)/1e-8
        second = (evaluate(2e-4)['shell_rows'][index]['master_surface_per_unit_source_jump'].real-static_green.real)/4e-8
        coefficient = (4*first-second)/3
        predicted = static_green.real+coefficient*sigma**2
        actual = row['shell_rows'][index]['master_surface_per_unit_source_jump']
        susceptibility_prediction = rows[0]['lambda_static']+rows[0]['quadratic_controls'][0]['quadratic_coefficient']*sigma**2
        benchmarks.append({'source_radius_over_body_radius': separation, 'frequency': sigma,
                           'surface_master_per_source': actual, 'static_surface_master_per_source': static_green,
                           'fractional_full_transfer_change': actual/static_green-1,
                           'quadratic_green_prediction_relative_error': abs(predicted-actual.real)/abs(actual.real),
                           'buffer2_susceptibility_relative_change': row['rows'][0]['susceptibility']/rows[0]['lambda_static']-1,
                           'quadratic_susceptibility_prediction_relative_error': abs(susceptibility_prediction-row['rows'][0]['susceptibility'].real)/abs(row['rows'][0]['susceptibility'].real)})
    report = {'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'system_sha256': hashlib.sha256((ROOT/'response_system_v3.py').read_bytes()).hexdigest(),
              'residue_path': str(residue_path), 'residue_sha256': hashlib.sha256(residue_path.read_bytes()).hexdigest(),
              'buffer_response_decomposition': rows, 'radiation_controls': radiation_rows,
              'source_owned_benchmarks': encode(benchmarks), 'evaluations': evaluations,
              'scope': 'Fixed delta-source in the Zerilli equation, derivative jump in r_star; orbital-frequency values are benchmarks only, not a companion stress tensor or binary force calculation. Quadratic coefficients are buffer-scheme dependent.'}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps(encode({'state': 'complete', 'decomposition': rows, 'radiation': radiation_rows, 'benchmarks': benchmarks}), indent=2))


if __name__ == '__main__':
    main()
