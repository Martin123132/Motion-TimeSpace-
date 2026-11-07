from __future__ import annotations

from datetime import datetime, timezone
import json

import numpy as np
import psutil

from causal_system import ROOT, digest
from run_pulses import pulse_solution


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    source = ROOT/'results/spectrum/body-256.npz'
    with np.load(source, allow_pickle=False) as archive:
        model = {key: archive[key] for key in archive.files}
    summary, samples = pulse_solution(model, 4., .25, 16385, 256)
    output = ROOT/'results/fast-pulse-refinement'
    output.mkdir(parents=True, exist_ok=False)
    np.savez_compressed(output/'pulse.npz', **samples)
    with np.load(ROOT/'results/pulses/cells256-T4-n16385-m128.npz', allow_pickle=False) as archive:
        control = {key: archive[key] for key in archive.files}
    difference = float(np.max(np.abs(samples['p']-control['p']))/np.max(np.abs(samples['p'])))
    assert difference < 2e-7, difference
    inputs = [source, ROOT/'run_pulses.py', ROOT/'results/pulses/cells256-T4-n16385-m128.npz']
    report = {'state': 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(),
              'script_sha256': digest(__file__), 'input_hashes': {str(path): digest(path) for path in inputs},
              'row': summary, 'archive_sha256': digest(output/'pulse.npz'),
              '128_to_256_mode_traction_error_over_peak': difference,
              'reason': 'The64-to128-mode fast pulse difference4.1223e-7 exceeded the2e-7 acceptance gate; refine modes, do not loosen it.'}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', '128_to_256_difference': difference,
                      'quartic_error': summary['quartic_traction_error_over_peak'],
                      'integrated_work_error': summary['work_integral_error_over_peak_energy']}))


if __name__ == '__main__':
    main()
