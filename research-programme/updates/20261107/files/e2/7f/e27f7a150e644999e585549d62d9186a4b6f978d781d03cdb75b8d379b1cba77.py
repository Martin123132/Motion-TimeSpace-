from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

import psutil

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
POST = BRANCH.parent
PARENT = BRANCH / 'early-adiabatic-matching-20261006'
MOTION = BRANCH / 'motion-bath-matching-20261006'
COMMIT = 'adc7f1241b42e322a6451854ab7e4b4c146bf78a'
SOURCE_PREFIXES = ['4873-', '4916-', '4937-', '4957-', '4958-', '5192-']
SOURCE_PATHS = []
for prefix in SOURCE_PREFIXES:
    matches = list(POST.glob(prefix + '*.md'))
    assert len(matches) == 1, (prefix, matches)
    SOURCE_PATHS.extend(matches)
SOURCE_PATHS += [MOTION / '49-real-motion-envelope-and-existing-bath-matching.md',
    PARENT / '51-early-adiabatic-onset-and-existing-growth-handoff.md',
    PARENT / 'results/stage-integrity.json', PARENT / 'results/matching/status.json']


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


def save(label, producer, report, extra=()):
    folder = ROOT / 'results' / label
    folder.mkdir(parents=True, exist_ok=False)
    paths = SOURCE_PATHS + [Path(__file__)] + list(extra)
    output = dict(state='complete', time_utc=datetime.now(timezone.utc).isoformat(),
        script_sha256=digest(producer), input_hashes={str(path): digest(path) for path in paths}, **report)
    write_json(folder / 'status.json', output)
    (folder / 'COMPLETE').write_text(output['time_utc'] + '\n', encoding='utf-8')
    return output
