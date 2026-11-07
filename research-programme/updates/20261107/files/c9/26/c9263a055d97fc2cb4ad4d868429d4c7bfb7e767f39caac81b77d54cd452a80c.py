from pathlib import Path
import sys
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH / 'kinetic-gain-loss-20261008'
sys.path.insert(0, str(PARENT))
import kinetic_common as inherited
import numpy as np
import json
import math
import time
from datetime import datetime, timezone
from scipy import special, integrate
import polarized_source as source
from batched_real import intensity_batch
from mass_shell_population import normalized_mass_score, mass_reweight
import vacuum_virtual as vacuum

STARTED = datetime(2026, 10, 8, 4, 30, 49, tzinfo=timezone.utc)
POST = BRANCH.parent
modest = inherited.modest
digest = inherited.digest
write_json = inherited.write_json
check = inherited.check


def dependencies():
    paths = {Path(__file__).resolve(), ROOT / 'ACCEPTANCE.md',
             PARENT / 'results/stage-integrity.json'}
    for module in list(sys.modules.values()):
        filename = getattr(module, '__file__', None)
        if filename:
            path = Path(filename).resolve()
            if path.suffix == '.py' and path.is_relative_to(BRANCH):
                paths.add(path)
    return paths


def finish(folder, report, script, extra=()):
    paths = dependencies() | {Path(script).resolve()} | {Path(path).resolve() for path in extra}
    report.update(state='complete', finished_utc=datetime.now(timezone.utc).isoformat(),
                  script_sha256=digest(script),
                  input_hashes={str(path): digest(path) for path in sorted(paths)})
    write_json(folder / 'status.json', report)
    (folder / 'COMPLETE').write_text('complete\n', encoding='utf-8')


def relative(actual, expected):
    return float(np.linalg.norm(actual - expected) / max(np.linalg.norm(expected), 1e-300))
