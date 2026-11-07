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

ROOT = Path(__file__).resolve().parent
BRANCH, POST = ROOT.parent, ROOT.parent.parent
PARENT = BRANCH / 'mixed-bath-transport-20261007'
sys.path.insert(0, str(PARENT))
import mixed_common as previous
from mixed_wave_system import MixedSystem
modest, digest, write_json = previous.modest, previous.digest, previous.write_json
THERMAL_PARENT = previous.PARENT
NATIVE, HISTORY, I3 = previous.NATIVE, previous.HISTORY, previous.I3
StableBasis = previous.StableBasis


def finish(folder, report, script, extra=()):
    paths = [Path(script), ROOT / 'observer_common.py', ROOT / 'ACCEPTANCE.md',
             PARENT / 'results/stage-integrity.json', *extra]
    report.update(state='complete', finished_utc=datetime.now(timezone.utc).isoformat(),
                  script_sha256=digest(script), input_hashes={str(path): digest(path) for path in paths})
    write_json(folder / 'status.json', report)
    (folder / 'COMPLETE').write_text('complete\n', encoding='utf-8')
