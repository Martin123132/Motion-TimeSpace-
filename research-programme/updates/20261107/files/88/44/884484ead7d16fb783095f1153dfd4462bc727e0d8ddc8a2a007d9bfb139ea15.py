from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'inclusive-soft-matching-20261008'))
from soft_matching_common import *

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent / 'inclusive-soft-matching-20261008'
STARTED = datetime(2026, 10, 8, 1, 36, 9, tzinfo=timezone.utc)


def finish(folder, report, script, extra=()):
    paths = [Path(script), ROOT / 'finite_matching_common.py', ROOT / 'ACCEPTANCE.md',
             PARENT / 'results/stage-integrity.json', *extra]
    report.update(state='complete', finished_utc=datetime.now(timezone.utc).isoformat(),
                  script_sha256=digest(script), input_hashes={str(path): digest(path) for path in paths})
    write_json(folder / 'status.json', report)
    (folder / 'COMPLETE').write_text('complete\n', encoding='utf-8')
