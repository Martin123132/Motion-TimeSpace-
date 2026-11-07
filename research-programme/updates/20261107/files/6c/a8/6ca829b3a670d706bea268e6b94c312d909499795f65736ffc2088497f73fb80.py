import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS"):
    os.environ[name] = "1"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import psutil
import numpy as np

ROOT = Path(__file__).resolve().parent
POST = ROOT.parent
PRIOR = POST / "mts-derived-wavelength-test-20261107"
BRIDGE = Path("C:/MTS-Data/condensate-origin-20261003/stiff-gas-dense-output-20261027/data/memory-tail-history-20261027/source-readout-bridge-20261102")
GATE, ALGEBRA = 2e-5, 1e-10


def require(condition, message):
    if not condition:
        raise ValueError(message)


def guard():
    require(datetime.now(timezone.utc) < datetime(2026, 11, 7, 10, 40, tzinfo=timezone.utc), "four-hour deadline")
    for path in (ROOT / "STOP-REQUESTED", BRIDGE / "STOP-REQUESTED", BRIDGE.parent / "STOP-REQUESTED", BRIDGE.parent / "execution-v3/STOP-REQUEST.json", BRIDGE / "final-epoch-kinematic-bank/STOP-REQUESTED"):
        require(not path.exists(), "owner hold: " + str(path))


def modest():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([4])
    guard()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write(path, value):
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, allow_nan=False)


def digest(path):
    hasher = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def load(path):
    with np.load(path) as archive:
        return {name: archive[name].copy() for name in archive.files}


def norm(value):
    return max(float(np.max(abs(value))), 1e-80)


def verify_parent():
    require(digest(PRIOR / "closeout.json") == "2fa0b8f2790e2e3cb11badc01b6b6f2489df548eb9533352176047bef3eb50fc", "parent seal")
    seal = read(PRIOR / "closeout.json")
    require(seal["state"] == "verified_closed" and seal["coupled_cases"] == 48, "completed parent")
    for record in seal["artifacts"]:
        guard()
        require(digest(record["path"]) == record["sha256"], "changed parent artifact: " + record["path"])
    return seal

