from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import psutil

from response_system_v2 import determinant, outgoing_state, propagate, static_master_basis
from response_system_v3 import ResponseProblem, ROOT, encode, outward_amplitude_ratios


def decode(value):
    return complex(value['real'], value['imaginary'])


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/controls'
    output.mkdir(exist_ok=False)
    flat_controls, extraction_controls, source_controls, precision_controls = [], [], [], []
    radius = 19.73166220910539
    for sigma in [5e-5, 1e-4, .001, .02, .06]:
        state, diagnostics = outgoing_state(radius, 0., sigma)
        argument = sigma*radius
        polynomial = 1+3j/argument-3/argument**2
        derivative = -3j/argument**2+6/argument**3
        exact = 1j*sigma+sigma*derivative/polynomial
        exact_imaginary = sigma/abs(polynomial)**2
        flat_controls.append({'sigma': sigma, 'real_logarithm_relative_error': abs(state[1].real/exact.real-1),
                              'imaginary_logarithm_relative_error': abs(state[1].imag/exact_imaginary-1),
                              'raw_flux_cancellation_diagnostic': diagnostics['flux_error']})
    baseline = ResponseProblem()
    for sigma in [.005, .0204566]:
        inside, solution, problem = baseline.interior(sigma)
        outgoing, _ = outgoing_state(baseline.radius, baseline.mass, complex(sigma))
        basis = propagate(2*baseline.radius, baseline.radius, baseline.mass, sigma,
                          static_master_basis(2*baseline.radius, baseline.mass, baseline.radius))
        coefficients = np.linalg.solve(basis, np.column_stack([inside, outgoing]))
        original_determinant = determinant(inside, outgoing)
        for fraction in [1.3, 1.8, 2.5]:
            transported = propagate(baseline.radius, fraction*baseline.radius, baseline.mass, sigma,
                                    np.column_stack([basis, inside, outgoing]))
            recovered = np.linalg.solve(transported[:, :2], transported[:, 2:])
            error = np.max(abs(recovered-coefficients)/(1+abs(coefficients)))
            wronskian_error = abs(determinant(transported[:, 2], transported[:, 3])/original_determinant-1)
            extraction_controls.append({'sigma': sigma, 'extraction_radius_over_radius': fraction,
                                        'coefficient_scaled_error': error, 'Wronskian_relative_error': wronskian_error})
        for fraction in [3., 10.]:
            source_radius = fraction*baseline.radius
            inner_at_source = propagate(baseline.radius, source_radius, baseline.mass, sigma, inside)
            outer_at_source, _ = outgoing_state(source_radius, baseline.mass, complex(sigma))
            local_wronskian = determinant(inner_at_source, outer_at_source)
            interior_multiplier = outer_at_source[0]/local_wronskian
            exterior_multiplier = inner_at_source[0]/local_wronskian
            jump = exterior_multiplier*outer_at_source[1]-interior_multiplier*inner_at_source[1]
            continuity = exterior_multiplier*outer_at_source[0]-interior_multiplier*inner_at_source[0]
            independently_matched = interior_multiplier*inside[0]
            ratios = outward_amplitude_ratios(baseline.radius, baseline.mass, complex(sigma), [fraction])
            ratio = ratios[min(ratios, key=lambda key: abs(key-fraction))]
            surface_formula = inside[0]*outgoing[0]/original_determinant*ratio
            source_controls.append({'sigma': sigma, 'source_radius_over_radius': fraction,
                                    'continuity_absolute_error': abs(continuity), 'jump_absolute_error': abs(jump-1),
                                    'independent_source_match_relative_error': abs(independently_matched/surface_formula-1)})
    controlled = ResponseProblem(distance=.04, tolerance=5e-9, far_phase=60., order=12)
    main_reports, alternate_reports = [], []
    for sigma in [0., 1e-4, .01, .0204566]:
        main_report, _ = baseline.evaluate(sigma)
        alternate_report, _ = controlled.evaluate(sigma)
        main_reports.append(encode(main_report))
        alternate_reports.append(encode(alternate_report))
        precision_controls.append({'sigma': sigma,
                                   'susceptibility_relative_differences': [abs(second['susceptibility']/first['susceptibility']-1) for first, second in zip(main_report['rows'], alternate_report['rows'])],
                                   'shell_relative_differences': [abs(second['master_surface_per_unit_source_jump']/first['master_surface_per_unit_source_jump']-1) for first, second in zip(main_report['shell_rows'], alternate_report['shell_rows'])],
                                   'imaginary_susceptibility_relative_differences': [abs(second['susceptibility'].imag/first['susceptibility'].imag-1) if sigma else 0. for first, second in zip(main_report['rows'], alternate_report['rows'])]})
        print(json.dumps(precision_controls[-1]), flush=True)
    residue_report = json.loads((ROOT/'results/residue/status.json').read_text())
    pole = decode(residue_report['pole'])
    center, _ = controlled.evaluate(pole)
    derivative_controls = []
    for step in [1e-6, 5e-7]:
        negative, _ = controlled.evaluate(pole-step)
        positive, _ = controlled.evaluate(pole+step)
        residues = [row['numerator']/((plus['denominator']-minus['denominator'])/(2*step))
                    for row, plus, minus in zip(center['rows'], positive['rows'], negative['rows'])]
        green_residue = 2*step/(1/positive['rows'][0]['total_green_surface_surface']-1/negative['rows'][0]['total_green_surface_surface'])
        derivative_controls.append(encode({'step': step, 'residues': residues, 'surface_green_residue': green_residue}))
    report = {'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'flat_outgoing_controls': flat_controls, 'fixed_basis_extraction_controls': extraction_controls,
              'independent_source_jump_controls': source_controls, 'precision_controls': precision_controls,
              'alternate_pole_derivative_controls': derivative_controls,
              'main_evaluations': main_reports, 'alternate_evaluations': alternate_reports,
              'control_settings': {'main': {'distance': .02, 'tolerance': 2e-8, 'far_phase': 40., 'order': 10},
                                   'alternate': {'distance': .04, 'tolerance': 5e-9, 'far_phase': 60., 'order': 12}},
              'interior_evaluations_this_script': 15,
              'scope': 'Independent flat solution, propagation at fixed basis, direct source matching and join/outer-boundary controls; not a total discretization error certificate.'}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'flat': flat_controls, 'extraction': extraction_controls, 'source': source_controls, 'residue': derivative_controls}))


if __name__ == '__main__':
    main()
