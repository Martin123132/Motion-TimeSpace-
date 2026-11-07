from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'observer-frequency-projection-20261007'))
from observer_common import *
from consistent_system import ConsistentSystem
from spectral_readout import SpectralReadout, spectral_norm
from scipy.sparse import linalg as sparse_linalg

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent / 'observer-frequency-projection-20261007'
BATH_PARENT = ROOT.parent / 'mixed-bath-transport-20261007'


def finish(folder, report, script, extra=()):
    paths = [Path(script), ROOT / 'scaled_common.py', ROOT / 'ACCEPTANCE.md',
             PARENT / 'results/stage-integrity.json', *extra]
    report.update(state='complete', finished_utc=datetime.now(timezone.utc).isoformat(),
                  script_sha256=digest(script), input_hashes={str(path): digest(path) for path in paths})
    write_json(folder / 'status.json', report)
    (folder / 'COMPLETE').write_text('complete\n', encoding='utf-8')
