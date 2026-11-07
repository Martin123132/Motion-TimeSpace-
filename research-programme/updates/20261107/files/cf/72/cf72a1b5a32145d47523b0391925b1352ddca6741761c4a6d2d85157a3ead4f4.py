from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import psutil
from scipy import linalg

from sequence_tools import SequenceProfile, build, digest


ROOT = Path(__file__).resolve().parent


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    source = ROOT/'results/clean-mesh-critical/status.json'
    row = json.loads(source.read_text(encoding='utf-8'))['rows'][0]
    profile = SequenceProfile(source.parent/row['archive'], row)
    system = build(profile, 256, 8)
    size = len(system['even'])
    zero = np.zeros((size, size))
    generator = np.block([[zero, system['dynamic']], [-system['even'], zero]])
    spectrum = linalg.eigvals(generator, check_finite=False)
    physical_real = sorted(float(value.real) for value in spectrum if abs(value.imag) < 1e-7 and abs(value.real) > 1e-6)
    squared = linalg.eigh(system['pulsation'], subset_by_index=[0, 3], eigvals_only=True)
    expected = float(np.sqrt(-squared[0]))
    assert len(physical_real) == 2 and physical_real[0] < 0 < physical_real[1]
    growth_error = max(abs(np.array(physical_real)-np.array([-expected, expected])))/expected
    assert growth_error < 1e-5
    output = ROOT/'results/first-order-growth'
    output.mkdir(exist_ok=False)
    np.savez_compressed(output/'generator-spectrum.npz', eigenvalues=spectrum, frequency_squared=squared)
    result = {'state': 'complete', 'source_sha256': digest(source), 'script_sha256': digest(Path(__file__)),
              'profile_sha256': digest(profile.path), 'cells': 256, 'central_amplitude': row['control_value'],
              'first_order_real_eigenvalues': physical_real, 'predicted_growth_rate': expected,
              'relative_growth_rate_difference': float(growth_error),
              'scope': 'Direct first-order finite-dimensional canonical generator check, not a nonlinear evolution.'}
    (output/'status.json').write_text(json.dumps(result, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
