from __future__ import annotations

import hashlib
import json
from pathlib import Path

import psutil

from response_system_v3 import ResponseProblem, ROOT, encode


def decode(value):
    return complex(value['real'], value['imaginary'])


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/refined-residue'
    output.mkdir(exist_ok=False)
    source_path = ROOT/'results/residue/status.json'
    source = json.loads(source_path.read_text())
    old_pole = decode(source['pole'])
    center, minus, plus = [source['evaluations'][index] for index in [0, 5, 6]]
    shifts = [decode(middle['denominator'])/((decode(right['denominator'])-decode(left['denominator']))/1e-6)
              for middle, left, right in zip(center['rows'], minus['rows'], plus['rows'])]
    pole = old_pole-shifts[0]
    problem = ResponseProblem()
    new_center, _ = problem.evaluate(pole)
    controls, evaluations = [], [encode(new_center)]
    for step in [5e-7, 2.5e-7]:
        negative, _ = problem.evaluate(pole-step)
        positive, _ = problem.evaluate(pole+step)
        evaluations.extend([encode(negative), encode(positive)])
        residues = [row['numerator']/((right['denominator']-left['denominator'])/(2*step))
                    for row, left, right in zip(new_center['rows'], negative['rows'], positive['rows'])]
        green = 2*step/(1/positive['rows'][0]['total_green_surface_surface']-1/negative['rows'][0]['total_green_surface_surface'])
        controls.append(encode({'step': step, 'residues': residues, 'surface_green_residue': green}))
    extrapolated = [(4*decode(fine)-decode(coarse))/3 for coarse, fine in zip(controls[0]['residues'], controls[1]['residues'])]
    errors = [abs(value/decode(target)-1) for value, target in zip(extrapolated, source['contour_controls'][-1]['residues'])]
    report = {'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'source_path': str(source_path), 'source_sha256': hashlib.sha256(source_path.read_bytes()).hexdigest(),
              'old_pole': encode(old_pole), 'Newton_shifts_by_buffer': encode(shifts), 'corrected_pole': encode(pole),
              'derivative_controls': controls, 'extrapolated_residues': encode(extrapolated),
              'contour_relative_errors': errors, 'evaluations': evaluations,
              'scope': 'One Newton recentering with this stage outgoing boundary before the denominator-derivative residue check; contour values remain the primary residue measurement.'}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps(encode({'state': 'complete', 'shifts': shifts, 'pole': pole, 'errors': errors})))


if __name__ == '__main__':
    main()
