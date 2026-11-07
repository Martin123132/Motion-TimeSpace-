import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS"):
    os.environ[name] = "1"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import psutil

ROOT = Path(__file__).resolve().parent
POST = ROOT.parent
PRIOR = POST / "mts-tail-energy-20261107"
HIERARCHY = POST / "mts-retarded-hierarchy-20261107"
BRIDGE = Path("C:/MTS-Data/condensate-origin-20261003/stiff-gas-dense-output-20261027/data/memory-tail-history-20261027/source-readout-bridge-20261102")
GATE, ALGEBRA, WAVE = 2e-5, 1e-10, 5.0


def require(condition, message):
    if not condition:
        raise ValueError(message)


def guard():
    require(datetime.now(timezone.utc) < datetime(2026, 11, 7, 8, 30, tzinfo=timezone.utc), "deadline")
    for path in (ROOT / "STOP-REQUESTED", BRIDGE / "STOP-REQUESTED", BRIDGE.parent / "STOP-REQUESTED", BRIDGE.parent / "execution-v3/STOP-REQUEST.json", BRIDGE / "final-epoch-kinematic-bank/STOP-REQUESTED"):
        require(not path.exists(), "owner hold: " + str(path))


def modest():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([4])
    guard()


def digest(path):
    hasher = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write(path, value):
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, allow_nan=False)


def load(path):
    import numpy as np
    with Path(path).open("rb") as stream, np.load(stream) as archive:
        return {name: archive[name].copy() for name in archive.files}


def check_prior():
    require(digest(PRIOR / "validation-result.json") == "1b89b6786ffb7f68e252343d54a50da47233520215a7d8ad0b9b08ba9aae3071", "prior validation")
    seal = read(PRIOR / "closeout.json")
    require(seal["state"] == "verified_closed", "prior closed")
    for record in seal["artifacts"]:
        require(digest(record["path"]) == record["sha256"], "prior artifact changed: " + record["path"])
    return seal


def source_curves(model):
    import numpy as np
    from scipy.interpolate import PchipInterpolator, CubicHermiteSpline
    reference = load(HIERARCHY / "runs-balanced" / model / "native-reference.npz")
    summary = read(PRIOR / "results" / model / "result.json")
    groups = [group for group in summary["groups"] if group["name"].startswith("neutrino-")]
    require(len(groups) == 5, "five retained momentum nodes")
    packets = [load(PRIOR / "results" / model / group["file"]) for group in groups]
    for group in groups:
        require(digest(PRIOR / "results" / model / group["file"]) == group["sha256"], "prior tail packet owner")
    low = [int(np.flatnonzero(reference["mapping"] == group["low_native"])[0]) for group in groups]
    speed = np.column_stack([packet["speed"] for packet in packets])
    require(np.min(speed) > 0 and np.max(speed) <= 1, "physical speed")
    velocity = PchipInterpolator(reference["times"], speed, axis=0)
    quadrupoles = reference["state"][:, low]
    forcing = CubicHermiteSpline(reference["times"], quadrupoles, reference["derivative"][:, low], axis=0)
    return reference, groups, packets, velocity, forcing
