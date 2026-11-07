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
BRANCH = POST / "condensate-origin-20261003"
PRIOR = POST / "mts-metric-feedback-20261107"
PAIRED = POST / "mts-state-feedback-20261107"
SOURCE = POST / "mts-direct-tangent-20261107"
HIERARCHY = POST / "mts-retarded-hierarchy-20261107"
CLOSURE = POST / "mts-pressure-balance-20261107"
ADAPTER = POST / "mts-background-operator-bridge-20261107"
EVOLUTION = POST / "mts-repaired-coupled-evolution-20261107"
BACKGROUND = POST / "mts-background-repair-20261107"
COUPLED = POST / "mts-neutrino-metric-feedback-20261107"
WAVELENGTH = POST / "mts-derived-wavelength-test-20261107"
AVERAGE = POST / "mts-scalar-cycle-average-20261107"
ENVELOPE = POST / "mts-rotating-envelope-20261107"
NORMAL = POST / "mts-slow-normal-form-20261107"
NATIVE = BRANCH / "native-heavy-matching-20261007/native"
EARLY = BRANCH / "native-two-field-transfer-20261007"
BRIDGE = Path("C:/MTS-Data/condensate-origin-20261003/stiff-gas-dense-output-20261027/data/memory-tail-history-20261027/source-readout-bridge-20261102")
GATE, ALGEBRA = 2e-5, 1e-10


def require(condition, message):
    if not condition:
        raise ValueError(message)


def guard():
    require(datetime.now(timezone.utc) < datetime(2026, 11, 7, 12, 2, tzinfo=timezone.utc), "deadline")
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
    with np.load(path) as archive:
        return {name: archive[name].copy() for name in archive.files}


def check_prior():
    require(digest(AVERAGE / "closeout.json") == "b65029f97a5c43c58f85c2cd9c8e3348461f9d79ac83a83170e65b7669caec36", "previous averaging seal")
    for folder, checksum in ((NORMAL, "4cfb6deacf12e07ea66b278eacff95760aa5d6bace63e4e1ff37e8ffeb27bfde"),
                             (ENVELOPE, "fc9ea51bd6e0074e0e4935978c66940a50eb1fd52c79b69a33af512e03ac44d5"),
                             (AVERAGE, "b65029f97a5c43c58f85c2cd9c8e3348461f9d79ac83a83170e65b7669caec36"),
                             (WAVELENGTH, "2fa0b8f2790e2e3cb11badc01b6b6f2489df548eb9533352176047bef3eb50fc")):
        require(digest(folder / "closeout.json") == checksum, "parent closeout")
        seal = read(folder / "closeout.json")
        require(seal["state"] == "verified_closed", "closed parent")
        for record in seal["artifacts"]:
            guard()
            require(digest(record["path"]) == record["sha256"], "parent changed: " + record["path"])
    return read(AVERAGE / "closeout.json")


def native_background(model):
    import ast
    import sys
    import numpy as np
    sys.path.insert(0, str(CLOSURE / "build/native"))
    import camb
    from camb.mts import MTSTwoField
    sys.path.append(str(BRANCH / "radiation-and-slow-field-transfer-20261007"))
    import radiation_common
    owner = NATIVE.parent / "matching_common.py"
    function = next(node for node in ast.parse(owner.read_text()).body if isinstance(node, ast.FunctionDef) and node.name == "params_for")
    namespace = dict(np=np, previous=radiation_common, MTSTwoField=MTSTwoField)
    exec(compile(ast.Module(body=[function], type_ignores=[]), str(owner), "exec"), namespace)
    params = namespace["params_for"](EARLY / ("runs/backgrounds/" + model + ".npz"))
    return camb.get_background(params)


def other_density(native, scale):
    import numpy as np
    values = np.atleast_1d(scale).astype(float)
    output = native.get_background_densities(values, vars=["cdm", "baryon", "photon", "neutrino", "nu"], format="array")
    return np.sum(output, axis=1) / values ** 2


def dense_values(packet, points):
    import numpy as np
    points = np.asarray(points)
    starts, ends = packet["segment_start"], packet["segment_end"]
    require(np.min(points) >= starts[0] and np.max(points) <= ends[-1], "dense evaluation domain")
    positions = np.searchsorted(ends, points, side="left").clip(0, len(ends) - 1)
    values, derivatives = np.zeros((len(points), 5)), np.zeros((len(points), 5))
    for index in np.unique(positions):
        selected = positions == index
        width = ends[index] - starts[index]
        local = ((points[selected] - starts[index]) / width)[:, None]
        coefficients = packet["coefficients"][index]
        value, derivative = np.zeros((sum(selected), 5)), np.zeros((sum(selected), 5))
        if str(packet["method"]) == "DOP853":
            for degree, coefficient in enumerate(coefficients[::-1]):
                value += coefficient
                if degree % 2 == 0:
                    derivative = derivative * local + value
                    value *= local
                else:
                    derivative = derivative * (1 - local) - value
                    value *= 1 - local
            derivative /= width
        else:
            for degree, coefficient in enumerate(coefficients):
                value += width * local ** (degree + 1) * coefficient
                derivative += (degree + 1) * local ** degree * coefficient
        values[selected] = packet["segment_initial"][index] + value
        derivatives[selected] = derivative
    return values, derivatives
