from pathlib import Path
import sys
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH / 'matched-weak-redistribution-20261008'
KINETIC = BRANCH / 'kinetic-gain-loss-20261008'
BACKGROUND = BRANCH / 'emitting-thermal-background-20261008'
sys.path.insert(0, str(KINETIC))
import kinetic_common as inherited
import numpy as np
import math
import json
import time
import os
from datetime import datetime, timezone
from scipy import special, linalg, interpolate
from consistent_spectral_basis import ConsistentBasis
import thermal_wave_common as thermal_wave
import integrated_dc
import infrared_ladder
from evolve_derived_gaunt import DerivedEmission
import evolve_emitting_background as engine

STARTED = datetime(2026, 10, 8, 4, 59, 15, tzinfo=timezone.utc)
POST = BRANCH.parent
modest = inherited.modest
digest = inherited.digest
write_json = inherited.write_json
check = inherited.check
I3 = np.pi**4 / 15
I4 = 4 * I3


def finish(folder, report, script, extra=()):
    paths = {Path(__file__).resolve(), Path(script).resolve(), ROOT / 'ACCEPTANCE.md',
             PARENT / 'results/stage-integrity.json'}
    paths.update(Path(path).resolve() for path in extra)
    for module in list(sys.modules.values()):
        filename = getattr(module, '__file__', None)
        if filename:
            path = Path(filename).resolve()
            if path.suffix == '.py' and path.is_relative_to(BRANCH):
                paths.add(path)
    report.update(state='complete', finished_utc=datetime.now(timezone.utc).isoformat(),
                  script_sha256=digest(script), input_hashes={str(path): digest(path) for path in sorted(paths)})
    write_json(folder / 'status.json', report)
    (folder / 'COMPLETE').write_text('complete\n', encoding='utf-8')


def relative(actual, expected):
    return float(np.linalg.norm(actual - expected) / max(np.linalg.norm(expected), 1e-300))


def current_basis():
    packet = json.loads((KINETIC / 'backgrounds/heavy-derived-gaunt/status.json').read_text())
    return ConsistentBasis(**packet['basis_spec']), packet['basis_spec']
