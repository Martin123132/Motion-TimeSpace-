import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

for variable in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS"):
    os.environ[variable] = "1"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
STAGE = Path(__file__).resolve().parent
LABEL = sys.argv[1] if len(sys.argv) == 2 else ""
if LABEL not in ("half", "double", "summary"):
    raise ValueError("explicit owned family required")
ROOT = STAGE / LABEL
POST = STAGE.parent
SEALED = POST / "mts-native-rest-action-feedback-20261107"
PARENT = POST / "mts-joint-gravity-hamiltonian-20261107"
PREVIOUS = POST / "mts-correlated-action-mean-20261107"
TIMECHAIN = POST / "mts-canonical-full-time-chain-20261107"
BACKGROUND = POST / "mts-background-repair-20261107"
SECOND = POST / "mts-second-micromotion-20261107"
BRIDGE = Path("C:/MTS-Data/condensate-origin-20261003/stiff-gas-dense-output-20261027/data/memory-tail-history-20261027/source-readout-bridge-20261102")
BRANCH = POST / "condensate-origin-20261003"
PRIOR = POST / "mts-metric-feedback-20261107"
SOURCE = POST / "mts-direct-tangent-20261107"
HIERARCHY = POST / "mts-retarded-hierarchy-20261107"
NATIVE = BRANCH / "native-heavy-matching-20261007/native"
EARLY = BRANCH / "native-two-field-transfer-20261007"
WAVELENGTH = POST / "mts-derived-wavelength-test-20261107"
ORIGINAL_POISSON = POST / "mts-independent-poisson-evolution-20261107"
ORIGINAL_ADJOINT = POST / "mts-newton-feedback-adjoint-20261107"
ORIGINAL_PRIMITIVE = POST / "mts-metric-time-primitive-20261107"
POISSON = ROOT
ADJOINT = ROOT
LATEST = ORIGINAL_PRIMITIVE
REFERENCE_ROOT = POST / "mts-coupled-wavelength-controls-20261107" / LABEL
WAVE = dict(json.loads((WAVELENGTH / "inventory-config.json").read_text(encoding="utf-8-sig"))["waves"]).get(LABEL)
PARENT_SEAL = "287e3bc01d13d195e70137e417bc8aa5906506145ccc85e982a008bb07cf99a5"
ALGEBRA = 1e-10
GATE = 2e-5
sys.path.extend([str(ORIGINAL_PRIMITIVE), str(ORIGINAL_ADJOINT), str(ORIGINAL_POISSON), str(SEALED), str(TIMECHAIN), str(PREVIOUS)])


def require(condition, message):
    if not condition:
        raise ValueError(message)


def guard():
    require(datetime.now(timezone.utc) < datetime(2026, 11, 7, 17, 36, tzinfo=timezone.utc), "check-in cutoff")
    for path in (STAGE / "STOP-REQUESTED", ROOT / "STOP-REQUESTED", BRIDGE / "STOP-REQUESTED", BRIDGE.parent / "STOP-REQUESTED",
                 BRIDGE.parent / "execution-v3/STOP-REQUEST.json", BRIDGE / "final-epoch-kinematic-bank/STOP-REQUESTED"):
        require(not path.exists(), "owner hold: " + str(path))


def modest():
    import psutil
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([4])
    guard()


def digest(path):
    result = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write(path, value):
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, allow_nan=False)


def check_parent():
    require(digest(LATEST / "closeout.json") == PARENT_SEAL, "parent seal")
    seal = read(LATEST / "closeout.json")
    require(seal["state"] == "verified_closed" and seal["all_numerical_checks_passed"], "parent scope")
    for record in seal["artifacts"]:
        guard()
        require(digest(record["path"]) == record["sha256"], "changed parent: " + record["path"])
    for source in read(STAGE / "source-provenance.json"):
        require(digest(source["path"]) == source["sha256"], "retained algorithm source changed")
        require(digest(source["owner"]) == source["owner_sha256"], "retained source owner changed")
    return seal


def load(path):
    import numpy as np
    with np.load(path) as archive:
        return {name: archive[name].copy() for name in archive.files}
