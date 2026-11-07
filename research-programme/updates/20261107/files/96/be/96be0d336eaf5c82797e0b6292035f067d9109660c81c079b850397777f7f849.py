import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
import sys
sys.dont_write_bytecode = True
from pathlib import Path
ROOT = Path(__file__).resolve().parent
BRANCH, POST = ROOT.parent, ROOT.parent.parent
PARENT = BRANCH / 'panelled-recoil-control-20261008'
sys.path.insert(0, str(PARENT))
import control_common as inherited
from control_common import np, math, json, time, special, linalg, interpolate, weak, prior, thermal_wave, I3, Spectra, TestFunctions, SplitReal
from panel_rule import PanelRule
from datetime import datetime, timezone
modest, digest, write_json = inherited.modest, inherited.digest, inherited.write_json
STARTED = datetime(2026, 10, 8, 19, 35, 49, tzinfo=timezone.utc)


def finish(folder, report, script, extra=()):
    paths = {ROOT / 'outer_common.py', ROOT / 'ACCEPTANCE.md', Path(script).resolve(),
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
    report['count'] = len(report['checks'])
    report['all_checks_passed'] = all(row['passed'] for row in report['checks'])
    write_json(folder / 'status.json', report)
    (folder / 'COMPLETE').write_text('complete\n', encoding='utf-8')
