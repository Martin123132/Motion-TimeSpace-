from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys

os.environ['OMP_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent / 'native-two-field-transfer-20261007'
POST = ROOT.parent.parent


def digest(path):
    hasher = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            hasher.update(block)
    return hasher.hexdigest()


def modest():
    import psutil
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False), encoding='utf-8')


def finish(folder, report, script, extra=()):
    paths = [Path(script), ROOT / 'stage_common.py', PARENT / 'results/stage-integrity.json', *extra]
    report.update(state='complete', finished_utc=datetime.now(timezone.utc).isoformat(),
        script_sha256=digest(script), input_hashes={str(path): digest(path) for path in paths})
    write_json(folder / 'status.json', report)
    (folder / 'COMPLETE').write_text('complete\n', encoding='utf-8')


def native_imports():
    sys.path.insert(0, str(ROOT / 'native'))
    sys.path.append(str(ROOT.parent / 'radiation-and-slow-field-transfer-20261007'))
    import camb
    import radiation_common
    assert Path(camb.__file__).resolve().is_relative_to(ROOT / 'native')
    return camb, radiation_common
