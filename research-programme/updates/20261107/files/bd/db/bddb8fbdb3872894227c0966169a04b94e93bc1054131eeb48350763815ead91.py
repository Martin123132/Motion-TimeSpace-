from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH/'near-circular-quadrupole-20261005'
sys.path.insert(0, str(PARENT))
from sidebands import AnalyticWave, digest, read_json, write_json, modest_process, polar_settings
from analyze_limit import damping


def imported_hashes():
    paths = {Path(module.__file__).resolve() for module in list(sys.modules.values())
             if getattr(module, '__file__', None) and Path(module.__file__).suffix == '.py'
             and BRANCH in Path(module.__file__).resolve().parents}
    paths.add(PARENT/'results/stage-integrity.json')
    return {str(path): digest(path) for path in sorted(paths)}
