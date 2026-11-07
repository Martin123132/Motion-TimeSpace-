from __future__ import annotations

from datetime import datetime, timezone
import json
import sys

import psutil

from acquire_source import ROOT, digest

sys.path.insert(0, str(ROOT.parent/'axial-companion-20261005'))
from axial_binary import AxialCompanion


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/extended-control'
    output.mkdir(parents=True, exist_ok=False)
    interior = {'tolerance': 3e-12, 'max_step': 1/240, 'start': 1e-5}
    exterior = {'tolerance': 3e-12, 'far_phase': 80., 'order': 14, 'horizon_epsilon': 3e-6}
    problem = AxialCompanion(interior, exterior)
    rows = [problem.evaluate(separation) for separation in [320., 640., 1280.]]
    report = {'state': 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(),
              'script_sha256': digest(__file__), 'rows': rows,
              'interior_settings': interior, 'exterior_settings': exterior,
              'input_hashes': {str(path): digest(path) for path in [ROOT.parent/'axial-companion-20261005/axial_binary.py',
                                                                  ROOT.parent/'dynamical-axial-20261004/axial_wave.py', problem.body.profile.path]}}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'rows': len(rows)}))


if __name__ == '__main__':
    main()
