from __future__ import annotations

import csv
from datetime import datetime, timezone
import json
import sys
import time

import psutil

from acquire_source import ROOT, digest

sys.path.insert(0, str(ROOT.parent/'axial-companion-20261005'))
from axial_binary import AxialCompanion


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/refined'
    output.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    interior = {'tolerance': 8e-14, 'max_step': 1/360, 'start': 5e-6}
    exterior = {'tolerance': 8e-14, 'far_phase': 65., 'order': 16, 'horizon_epsilon': 2e-6}
    problem = AxialCompanion(interior, exterior)
    rows = []
    with (output/'log.txt').open('x', encoding='utf-8', buffering=1) as log:
        for separation in [5., 10., 20., 40., 80., 160., 320., 640., 1280.]:
            row = problem.evaluate(separation)
            rows.append(row)
            message = {'state': 'running', 'separation_over_radius': separation,
                       'ratio': row['infinity_increment_to_leading_magnetic'], 'elapsed_seconds': time.monotonic()-started}
            log.write(json.dumps(message)+'\n')
            print(json.dumps(message), flush=True)
        sources = [problem.body.profile.path, ROOT.parent/'axial-companion-20261005/axial_binary.py',
                   ROOT.parent/'axial-companion-20261005/results/stage-integrity.json',
                   ROOT.parent/'dynamical-axial-20261004/axial_wave.py']
        report = {'state': 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(),
                  'script_sha256': digest(__file__), 'input_hashes': {str(path): digest(path) for path in sources},
                  'body_mass': problem.mass, 'body_radius': problem.radius, 'sigma_bar': problem.sigma,
                  'rows': rows, 'interior_settings': interior, 'exterior_settings': exterior,
                  'new_body_fits': 0, 'new_background_solves': 0, 'elapsed_seconds': time.monotonic()-started}
        (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
        with (output/'rows.csv').open('x', encoding='utf-8', newline='') as handle:
            fields = [key for key in rows[0] if not isinstance(rows[0][key], dict)]
            writer = csv.DictWriter(handle, fieldnames=fields, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(rows)
        (output/'COMPLETE').write_text(report['time_utc']+'\n', encoding='utf-8')
        log.write(json.dumps({'state': 'complete', 'elapsed_seconds': report['elapsed_seconds']})+'\n')
    print(json.dumps({'state': 'complete', 'rows': len(rows), 'elapsed_seconds': report['elapsed_seconds']}))


if __name__ == '__main__':
    main()
