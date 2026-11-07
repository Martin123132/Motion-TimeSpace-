from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

import psutil

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
POST = BRANCH.parent
PARENT = BRANCH / 'cosmology-reconnection-20261006'
sys.dont_write_bytecode = True
sys.path.insert(0, str(PARENT))
import cosmology_common as previous

SOURCE_NAMES = [
    '4873-Y5-R2FR-covariant-open-parent-action-and-connected-covariance-kernel-to-unit-flow-Kubo-coefficients-or-final-EFT-freeze.md',
    '4897-Y5-R2FR-cosmology-without-bath-source-metric-only-baseline-and-derived-extension-reentry-gate.md',
    '4916-Y5-R2FR-covariantization-map-from-microscopic-motion-action-to-integrated-H-parent-and-no-direct-flow-charge-or-primitive-freeze.md',
    '4938-Y5-R2FR-motion-scale-to-Newton-scale-parent-identity-or-explicit-two-scale-theory-gate.md',
    '5192-Y5-R2FR-parent-motion-FLRW-branch-memory-separation-and-mass-gap-cosmology-gate.md',
]
SOURCE_URLS = [
    'https://arxiv.org/abs/1712.00445',
    'https://doi.org/10.1103/PhysRevD.98.016011',
    'https://arxiv.org/abs/2005.11359',
    'https://doi.org/10.1103/PhysRevD.102.036024',
]


def modest_process():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write_json(path, value):
    with Path(path).open('x', encoding='utf-8') as handle:
        json.dump(value, handle, indent=2, allow_nan=False)


def inputs():
    paths = [POST / name for name in SOURCE_NAMES]
    paths += [Path(__file__), PARENT / 'results/stage-integrity.json',
              PARENT / 'results/comparison/status.json', PARENT / 'cosmology_common.py',
              Path(previous.inherited.__file__), Path(previous.inherited.closure_runner.__file__)]
    paths += [previous.inherited.SN_DATA, previous.inherited.SN_COV,
              previous.inherited.BAO_DATA, previous.inherited.BAO_COV]
    return {str(path): digest(path) for path in sorted(set(paths))}


def save(label, script, report, extra_paths=()):
    folder = ROOT / 'results' / label
    folder.mkdir(parents=True, exist_ok=False)
    hashes = inputs()
    hashes.update({str(path): digest(path) for path in extra_paths})
    output = dict(state='complete', time_utc=datetime.now(timezone.utc).isoformat(),
                  script_sha256=digest(script), input_hashes=hashes, source_urls=SOURCE_URLS,
                  **report)
    write_json(folder / 'status.json', output)
    (folder / 'COMPLETE').write_text(output['time_utc'] + '\n', encoding='utf-8')
    return output
