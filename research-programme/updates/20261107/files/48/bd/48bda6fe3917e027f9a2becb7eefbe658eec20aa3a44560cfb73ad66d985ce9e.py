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
BRANCH, POST = ROOT.parent, ROOT.parent.parent
PARENT = BRANCH / 'expanding-thermal-gravity-20261007'
sys.path.insert(0, str(PARENT))
import thermal_wave_common as prior
modest, digest, write_json = prior.modest, prior.digest, prior.write_json
GRID, SPIN = prior.PARENT, prior.PARENT.parent / 'polarized-finite-shift-kernel-20261007'
WAVES, THERMAL, NATIVE, HISTORY, I3 = prior.WAVES, prior.THERMAL, prior.NATIVE, prior.HISTORY, prior.I3
grid = prior.prior
from stable_spectral_basis import StableBasis, load_basis
from high_degree_waves import RefinedSystem


def finish(folder, report, script, extra=()):
    paths = [Path(script), ROOT / 'mixed_common.py', ROOT / 'ACCEPTANCE.md',
             PARENT / 'results/stage-integrity.json', *extra]
    report.update(state='complete', finished_utc=datetime.now(timezone.utc).isoformat(),
                  script_sha256=digest(script), input_hashes={str(path): digest(path) for path in paths})
    write_json(folder / 'status.json', report)
    (folder / 'COMPLETE').write_text('complete\n', encoding='utf-8')
