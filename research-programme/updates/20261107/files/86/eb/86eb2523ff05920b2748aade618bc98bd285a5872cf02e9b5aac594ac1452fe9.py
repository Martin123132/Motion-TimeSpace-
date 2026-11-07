from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'finite-vacuum-matching-20261008'))
from finite_matching_common import *

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent / 'finite-vacuum-matching-20261008'
AMPLITUDE_PARENT = ROOT.parent / 'inclusive-soft-matching-20261008'
STARTED = datetime(2026, 10, 8, 1, 59, 39, tzinfo=timezone.utc)


def finish(folder, report, script, extra=()):
    paths = [Path(script), ROOT / 'thermal_vertex_common.py', ROOT / 'ACCEPTANCE.md',
             PARENT / 'results/stage-integrity.json', *extra]
    report.update(state='complete', finished_utc=datetime.now(timezone.utc).isoformat(),
                  script_sha256=digest(script), input_hashes={str(path): digest(path) for path in paths})
    write_json(folder / 'status.json', report)
    (folder / 'COMPLETE').write_text('complete\n', encoding='utf-8')


def check(name, value, limit):
    value=float(value)
    return dict(name=name,value=value,limit=float(limit),passed=bool(np.isfinite(value) and value<limit))
