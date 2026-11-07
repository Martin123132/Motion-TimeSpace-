from __future__ import annotations

import argparse
import json
import sys
import time

import numpy as np

from secular import ROOT, BRANCH, PARENT, digest, modest_process, save_report
sys.path.insert(0, str(PARENT))
from eccentric_radiation import EccentricRadiation, settings
from eccentric_source import anomaly_solution


class FixedSemilatusRadiation(EccentricRadiation):
    def __init__(self, chosen_settings, eccentricity):
        super().__init__(chosen_settings, eccentricity)
        self.semilatus = 5*self.radius/self.mass
        self.trajectory = anomaly_solution(self.mass, self.semilatus, eccentricity, chosen_settings['orbit_tolerance'])
        self.period, self.phase_advance = 2*self.trajectory.sol(np.pi)[:2]
        self.half, self.half_weights = self.source_nodes(chosen_settings['source_order'], 0., np.pi)
        self.full, self.full_weights = self.source_nodes(chosen_settings['source_order'], 0., 2*np.pi)
        radii = np.concatenate([[self.radius], self.half['radius'], self.full['radius']])
        self.positions = np.array(sorted(set(radii)))
        self.half_indices = np.searchsorted(self.positions, self.half['radius'])
        self.full_indices = np.searchsorted(self.positions, self.full['radius'])


def main():
    modest_process()
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', choices=['coarse', 'fine'], required=True)
    arguments = parser.parse_args()
    output = ROOT/'results'/('small-e-'+arguments.label)
    output.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    chosen_settings = settings(arguments.label)
    rows, orbits = [], []
    with (output/'log.txt').open('x', encoding='utf-8', buffering=1) as log:
        for eccentricity in [.01, .02, .04]:
            problem = FixedSemilatusRadiation(chosen_settings, eccentricity)
            orbits.append({'eccentricity': eccentricity, 'semilatus': problem.semilatus,
                           'period': float(problem.period), 'phase_advance': float(problem.phase_advance),
                           'mass': problem.mass, 'radius': problem.radius})
            for harmonic in range(-8, 9):
                row, _ = problem.evaluate(harmonic)
                rows.append(row)
                log.write(json.dumps({'eccentricity': eccentricity, 'harmonic': harmonic,
                                      'power': row['BH_infinity_energy'], 'difference': row['difference_total_energy']})+'\n')
            print(json.dumps({'eccentricity': eccentricity, 'completed_modes': len(rows)}), flush=True)
    inputs = [ROOT/'secular.py', PARENT/'eccentric_radiation.py', PARENT/'results/stage-integrity.json',
              BRANCH/'eccentric-source-20261005/eccentric_source.py', BRANCH/'axial-companion-20261005/axial_binary.py',
              BRANCH/'dynamical-axial-20261004/axial_wave.py', BRANCH/'axial-reciprocity-20261005/axial_action.py',
              problem.body.profile.path]
    report = save_report(output, __file__, {'orbits': orbits, 'rows': rows, 'settings': chosen_settings,
            'input_hashes': {str(path): digest(path) for path in inputs},
            'elapsed_seconds': time.monotonic()-started, 'normalization': 'wave power per mu squared',
            'sector': 'odd ell2 m+/-1', 'new_background_solves': 0, 'fixed_semilatus': True})
    print(json.dumps({'state': 'complete', 'modes': len(rows), 'elapsed_seconds': report['elapsed_seconds']}))


if __name__ == '__main__':
    main()
