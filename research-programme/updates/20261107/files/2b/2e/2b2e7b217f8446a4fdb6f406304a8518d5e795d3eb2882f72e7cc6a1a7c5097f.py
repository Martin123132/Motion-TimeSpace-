from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scaled-spectral-evolution-20261007'))
from scaled_common import *
import thermal_wave_common as thermal_wave
from consistent_spectral_basis import ConsistentBasis
from extended_system import ExtendedLadder

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent / 'scaled-spectral-evolution-20261007'
OBSERVER = ROOT.parent / 'observer-frequency-projection-20261007'
THERMAL_STAGE = ROOT.parent / 'expanding-thermal-gravity-20261007'


def finish(folder, report, script, extra=()):
    paths = [Path(script), ROOT / 'emission_common.py', ROOT / 'ACCEPTANCE.md',
             PARENT / 'results/stage-integrity.json', *extra]
    report.update(state='complete', finished_utc=datetime.now(timezone.utc).isoformat(),
                  script_sha256=digest(script), input_hashes={str(path): digest(path) for path in paths})
    write_json(folder / 'status.json', report)
    (folder / 'COMPLETE').write_text('complete\n', encoding='utf-8')
