from __future__ import annotations
import os
import sys
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
sys.dont_write_bytecode = True
from pathlib import Path
from datetime import datetime, timezone
import json
import math
import time
import numpy as np
from scipy import linalg, integrate, interpolate, sparse, special
from scipy.sparse import linalg as sparse_linalg

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
POST = BRANCH.parent
PARENT = BRANCH / 'polarized-heat-momentum-grid-20261007'
THERMAL = BRANCH / 'thermal-recoil-and-spectral-response-20261007'
WAVES = BRANCH / 'coupled-finite-wave-evolution-20261007'
sys.path.insert(0, str(PARENT))
import grid_common as prior
sys.path.insert(0, str(THERMAL))
import thermal_common as thermal
modest, digest, write_json = prior.modest, prior.digest, prior.write_json
NATIVE, HISTORY, I3 = prior.NATIVE, prior.HISTORY, prior.I3


def finish(folder, report, script, extra=()):
    paths = [Path(script), ROOT / 'thermal_wave_common.py', ROOT / 'ACCEPTANCE.md',
             PARENT / 'results/stage-integrity.json', *extra]
    report.update(state='complete', finished_utc=datetime.now(timezone.utc).isoformat(),
                  script_sha256=digest(script), input_hashes={str(path): digest(path) for path in paths})
    write_json(folder / 'status.json', report)
    (folder / 'COMPLETE').write_text('complete\n', encoding='utf-8')


def frequency_quadrature(count=240, minimum=1e-5, maximum=60.):
    points, weights = np.polynomial.legendre.leggauss(count)
    lo, hi = math.log(minimum), math.log(maximum)
    frequency = np.exp(.5 * (hi + lo) + .5 * (hi - lo) * points)
    quadrature = .5 * (hi - lo) * weights * frequency
    occupation = 1 / np.expm1(frequency)
    measure = quadrature * frequency ** 2 * occupation * (1 + occupation) / I3
    return frequency, measure


class SpectralBasis:
    def __init__(self, count=16, quadrature=240, minimum=1e-5, maximum=60., pivot=3.):
        self.count, self.pivot = count, pivot
        self.nodes, self.measure = frequency_quadrature(quadrature, minimum, maximum)
        self.minimum, self.maximum = minimum, maximum
        raw = self.raw(self.nodes)
        orthogonal, triangular = linalg.qr(np.sqrt(self.measure[:, None]) * raw, mode='economic')
        self.transform = linalg.solve_triangular(triangular, np.eye(count))
        self.values = raw @ self.transform
        self.mass = (self.values.T * self.measure) @ self.values
        self.chemical = triangular[:, 0]
        self.temperature = triangular[:, 1]
        self.energy = self.temperature @ self.mass
        self.number = self.chemical @ self.mass
        self.qr_orthogonality = float(np.linalg.norm(self.mass - np.eye(count)))
        self.raw_condition = float(np.linalg.cond(triangular))

    def raw(self, frequency):
        frequency = np.asarray(frequency)
        compact = (frequency - self.pivot) / (frequency + self.pivot)
        polynomials = np.polynomial.chebyshev.chebvander(compact, self.count - 1)
        polynomials[..., 1] = frequency
        return polynomials

    def evaluate(self, frequency):
        return self.raw(frequency) @ self.transform

    def project(self, values):
        right = self.values.T @ (self.measure * values)
        return linalg.solve(self.mass, right, assume_a='pos')

    def derivative(self, frequency):
        frequency = np.asarray(frequency)
        compact = (frequency - self.pivot) / (frequency + self.pivot)
        result = np.zeros(frequency.shape + (self.count,))
        result[..., 1] = 1.
        derivative = 2 * self.pivot / (frequency + self.pivot) ** 2
        for degree in range(2, self.count):
            coefficients = np.zeros(degree + 1)
            coefficients[-1] = 1.
            result[..., degree] = np.polynomial.chebyshev.chebval(compact, np.polynomial.chebyshev.chebder(coefficients)) * derivative
        return result @ self.transform
