from __future__ import annotations

import argparse
import csv
import json
import time

import numpy as np

from eccentric_radiation import ROOT, BRANCH, EccentricRadiation, settings, modest_process, digest, save_json, report_header


def main():
    modest_process()
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', choices=['pilot', 'coarse', 'fine', 'quadrature', 'extension'], required=True)
    arguments = parser.parse_args()
    output = ROOT/'results'/arguments.label
    output.mkdir(parents=True, exist_ok=False)
    chosen_settings = settings('coarse' if arguments.label in ['pilot', 'coarse'] else arguments.label)
    if arguments.label == 'pilot':
        schedule = [(0., [0]), (.3, [-2, -1, 0, 1, 5, 12]), (.6, [-2, -1, 0, 1, 5, 16])]
    elif arguments.label == 'extension':
        schedule = [(.6, list(range(-96, -64))+list(range(65, 97)))]
    elif arguments.label == 'quadrature':
        schedule = [(0., [0]), (.3, list(range(-24, 25))), (.6, list(range(-64, 65)))]
    else:
        schedule = [(0., [0]), (.3, list(range(-24, 25))), (.6, list(range(-64, 65)))]
    started = time.monotonic()
    rows, orbits, archives = [], [], []
    with (output/'log.txt').open('x', encoding='utf-8', buffering=1) as log:
        for eccentricity, harmonics in schedule:
            problem = EccentricRadiation(chosen_settings, eccentricity)
            orbits.append({'eccentricity': eccentricity, 'semilatus': problem.semilatus,
                           'period': float(problem.period), 'phase_advance': float(problem.phase_advance),
                           'mass': problem.mass, 'radius': problem.radius})
            for harmonic in harmonics:
                row, saved = problem.evaluate(harmonic)
                rows.append(row)
                if harmonic in [-1, 0, 5, 16] or arguments.label == 'pilot':
                    archive = output/f'e{eccentricity:.1f}-n{harmonic}.npz'
                    np.savez_compressed(archive, **saved)
                    archives.append({'path': str(archive), 'sha256': digest(archive)})
                message = {'eccentricity': eccentricity, 'harmonic': harmonic, 'completed_modes': len(rows),
                           'power': row['BH_infinity_energy'], 'difference': row['difference_infinity_energy'],
                           'optical_error': row['optical_error_over_component_sum'],
                           'source_error': row['full_source_integral_error_over_absolute_scale']}
                log.write(json.dumps(message)+'\n')
                if arguments.label == 'pilot' or len(rows) % 16 == 0:
                    print(json.dumps(message), flush=True)
        inputs = [ROOT/'eccentric_radiation.py', BRANCH/'eccentric-source-20261005/eccentric_source.py',
                  BRANCH/'eccentric-source-20261005/results/stage-integrity.json', problem.body.profile.path,
                  BRANCH/'axial-companion-20261005/axial_binary.py', BRANCH/'dynamical-axial-20261004/axial_wave.py',
                  BRANCH/'axial-reciprocity-20261005/axial_action.py']
        report = {**report_header(__file__), 'settings': chosen_settings, 'orbits': orbits, 'rows': rows,
                  'input_hashes': {str(path): digest(path) for path in inputs}, 'saved_archives': archives,
                  'elapsed_seconds': time.monotonic()-started, 'new_background_solves': 0, 'new_fitted_parameters': 0,
                  'sector': 'odd ell2 m+/-1 only', 'mass_normalization': 'per mu squared',
                  'self_force_or_inspiral_integrated': False}
        save_json(output/'status.json', report)
        fields = [key for key, value in rows[0].items() if not isinstance(value, dict)]
        with (output/'spectrum.csv').open('x', encoding='utf-8', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(rows)
        (output/'COMPLETE').write_text(report['time_utc']+'\n', encoding='utf-8')
        print(json.dumps({'state': 'complete', 'modes': len(rows), 'elapsed_seconds': report['elapsed_seconds']}))


if __name__ == '__main__':
    main()
