from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH/'polar-hamiltonian-20261006'
sys.path.insert(0, str(PARENT))
from polar_energy import Background, digest, read_json, modest_process, whiten


def dependencies():
    paths = {Path(module.__file__).resolve() for module in list(sys.modules.values())
             if getattr(module, '__file__', None) and Path(module.__file__).suffix == '.py'
             and BRANCH in Path(module.__file__).resolve().parents}
    paths.add(PARENT/'results/stage-integrity.json')
    return {str(path):digest(path) for path in sorted(paths)}


def save(label, script, report, extra_inputs=()):
    directory = ROOT/'results'/label
    directory.mkdir(parents=True, exist_ok=False)
    inputs = dependencies()
    inputs.update({str(path):digest(path) for path in extra_inputs})
    report = dict(state='complete', time_utc=datetime.now(timezone.utc).isoformat(),
                  script_sha256=digest(script), input_hashes=inputs, **report)
    with (directory/'status.json').open('x', encoding='utf-8') as handle:
        json.dump(report, handle, indent=2, allow_nan=False)
    (directory/'COMPLETE').write_text(report['time_utc']+'\n', encoding='utf-8')
    return report
