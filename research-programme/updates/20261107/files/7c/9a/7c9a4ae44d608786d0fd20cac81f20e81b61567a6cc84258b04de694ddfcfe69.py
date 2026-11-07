from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.interpolate import PPoly

import validate_finite_bodies as runner


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'results/verified-bodies'


def reconstruct_canonical_spline(coefficients, knots, axis):
    assert axis == 1 and coefficients.ndim == 3 and coefficients.shape[0] == 4
    assert coefficients.shape[1] == len(knots)-1 and coefficients.shape[2] == 2
    assert np.all(np.diff(knots) > 0) and np.all(np.isfinite(coefficients))
    return PPoly.construct_fast(coefficients, knots, axis=1)


def main():
    runner.OUTPUT = OUTPUT
    runner.PPoly = reconstruct_canonical_spline
    try:
        runner.main()
    finally:
        record = {'wrapper_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  'base_runner_sha256': hashlib.sha256((ROOT/'validate_finite_bodies.py').read_bytes()).hexdigest(),
                  'override': 'Canonical scipy PPoly.c already has shape (power, interval, component); use shape-checked construct_fast with axis=1, not the input-axis-permuting constructor.',
                  'previous_validated_attempt': 'aborted in spline loading before solving or spectral calculation',
                  'prior_data_and_science_files_modified': False,
                  'output_directory': OUTPUT.relative_to(ROOT).as_posix()}
        if OUTPUT.is_dir():
            (OUTPUT/'execution-provenance.json').write_text(json.dumps(record, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
