import os

for variable in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "BLIS_NUM_THREADS"):
    os.environ[variable] = "1"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import hashlib
import json
import math
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

import psutil

process = psutil.Process()
process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
process.cpu_affinity([4])
sys.dont_write_bytecode = True
sys.setrecursionlimit(3000)
ROOT = Path(__file__).resolve().parent
BASE = Path("D:/Users/ollet/Desktop/Turn an intuitive research programme into a formal field-theoretic framework/Motion-TimeSpace--main/post-checkpoint-work/condensate-origin-20261003")
started = time.monotonic()
checks, sources = [], {}


def protect(event, arguments):
    if event == "open":
        path, mode, flags = arguments
        writing = isinstance(mode, str) and any(character in mode for character in "wax+") or flags & (os.O_CREAT | os.O_TRUNC | os.O_APPEND | os.O_WRONLY | os.O_RDWR)
        if writing and not isinstance(path, int) and not Path(path).resolve().is_relative_to(ROOT):
            raise PermissionError("Readout check may not write outside its isolated directory")


sys.addaudithook(protect)
import mpmath as mp
import numpy as np

sys.path.insert(0, str(BASE / "mixed-angular-vertex-20261026"))
sys.path.insert(0, str(BASE / "finite-real-mixed-source-20261026"))
import run233 as retained
from factors236 import spline_difference
from correlated_readout import CorrelatedNodalFeatures
from nodal_readout import NodalFeatures


def register(path):
    path = Path(path).resolve()
    sources[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    return path


def compare(name, actual, expected):
    if time.monotonic() - started > 120:
        raise TimeoutError("Bounded representation check exceeded its allowance")
    actual, expected = np.asarray(actual), np.asarray(expected)
    error = float(np.linalg.norm(actual - expected))
    reference = max(float(np.linalg.norm(expected)), 1e-300)
    checks.append(dict(name=name, relative=error / reference, limit=1e-10, passed=error <= 1e-10 * reference))


def reject(name, action):
    try:
        action()
    except ValueError:
        checks.append(dict(name=name, passed=True))
    else:
        checks.append(dict(name=name, passed=False))


def high_precision_reference(spline, frequency, shifts):
    output = []
    with mp.workdps(80):
        origin = mp.mpf(math.log(frequency))
        for shift in shifts:
            destination = origin + mp.mpf(float(np.log1p(shift / frequency)))
            values = []
            for coordinate in (origin, destination):
                position = min(max(int(np.searchsorted(spline.x, float(coordinate), side="right") - 1), 0), len(spline.x) - 2)
                while position > 0 and mp.mpf(float(spline.x[position])) > coordinate:
                    position -= 1
                while position < len(spline.x) - 2 and mp.mpf(float(spline.x[position + 1])) <= coordinate:
                    position += 1
                local = coordinate - mp.mpf(float(spline.x[position]))
                coefficient = spline.c[:, position]
                values.append([((mp.mpf(float(column[0])) * local + mp.mpf(float(column[1]))) * local
                    + mp.mpf(float(column[2]))) * local + mp.mpf(float(column[3])) for column in coefficient.T])
            output.append([float(second - first) for first, second in zip(*values)])
    return np.asarray(output)


config = json.loads(register(BASE / "mixed-angular-vertex-20261026/configuration.json").read_text())
original, theta = retained.source.context(config["target_fraction"])
assert theta == config["target_theta"] and original.epochs[0].heat == config["heat"]
for path in original.inputs:
    register(path)
for path in (ROOT.parent / "execution-v3/science-config.json", ROOT.parent / "execution-v3/history_run.py"):
    register(path)
tail = original.epochs[0].tails["heavy"][0]
assert np.array_equal(tail, original.epochs[0].tails["cold"][0])
compact = CorrelatedNodalFeatures(original, tail)
legacy = retained.precise.Features(original)
embedding = np.zeros((compact.spectral_count, 98))
embedding[:96, :96] = np.eye(96)
embedding[96:, 96] = original.epochs[0].tails["heavy"][1]
embedding[96:, 97] = original.epochs[0].tails["cold"][1]
physical = np.asarray([[float(mp.mpf(value) * mp.mpf(float(config["heat"]))) for value in state["coefficients"][:98]] for state in config["states"]]).T

probes = [7.952885162185943e-5, 1.5e-4, 14.]
for probe in probes:
    shifts = probe * np.array([0., 1e-20, -1e-20, 1e-12, -1e-12, 1e-5, -1e-5, .002, -.002])
    for join in (0, 1):
        output = compact.difference(probe, shifts, join)
        reference = spline_difference(legacy.splines[join], probe, shifts)
        for index, shift in enumerate(shifts):
            label = f"production:x{probe}:join{join}:relative-shift{shift/probe}"
            compare(label + ":old subspace", output[index] @ embedding, reference[index])
            for state_index in range(6):
                compare(label + f":physical-state{state_index}", output[index] @ embedding @ physical[:, state_index], reference[index] @ physical[:, state_index])
        tiny = output[1]
        compare(f"x{probe}:join{join}:sub-ulp derivative", tiny / shifts[1], compact.evaluate(probe, join, derivative=True))
        checks.append(dict(name=f"x{probe}:join{join}:rounded-subtraction negative control",
            passed=bool(np.array_equal(compact.evaluate(probe + shifts[1], join), compact.evaluate(probe, join)) and np.linalg.norm(tiny) > 0)))

small_frequency = np.geomspace(1e-6, 60., 71)
small_frequency[1:-1] *= np.exp(.02 * np.sin(np.arange(69)))
small_original = SimpleNamespace(epochs=[SimpleNamespace(frequency=small_frequency, basis=original.basis)], basis=original.basis)
small = CorrelatedNodalFeatures(small_original, tail)
dense = NodalFeatures(small_original, tail)
for probe in (7.952885162185943e-5, .023, 14.):
    shifts = probe * np.array([1e-20, -1e-20, .001, -.001, .02, -.02])
    for join in (0, 1):
        output = small.difference(probe, shifts, join)
        reference = high_precision_reference(dense.splines[join], probe, shifts)
        for index, shift in enumerate(shifts):
            compare(f"irregular:all577:x{probe}:join{join}:shift{shift/probe}", output[index], reference[index])

for features, label in ((small, "irregular"), (compact, "production")):
    knot_index = int(np.searchsorted(features.frequency, 8e-5))
    knot = features.frequency[knot_index]
    for sign in (-1, 1):
        probe = knot * (1 - sign * 1e-8)
        shifts = np.array([sign * 2e-8 * knot])
        for join in (0, 1):
            output = features.difference(probe, shifts, join)
            if features is compact:
                output = output @ embedding
                spline = legacy.splines[join]
            else:
                spline = dense.splines[join]
            compare(f"{label}:cross-knot:sign{sign}:join{join}", output, high_precision_reference(spline, probe, shifts))
    probe = float(features.frequency[knot_index])
    for sign in (-1, 1):
        shifts = np.array([sign * probe * 1e-20])
        for join in (0, 1):
            compare(f"{label}:at-knot:sign{sign}:join{join}", features.difference(probe, shifts, join)[0] / shifts[0], features.evaluate(probe, join, derivative=True))

reject("invalid join", lambda: compact.difference(.1, [.001], 2))
reject("nonfinite shift", lambda: compact.difference(.1, [float("nan")], 0))
reject("nonpositive destination", lambda: compact.difference(.1, [-.1], 0))
reject("out-of-domain destination", lambda: compact.difference(59., [2.], 0))
reject("out-of-domain reference", lambda: compact.difference(61., [-2.], 0))
reject("unbounded weight allocation", lambda: compact.difference_weights(.1, np.zeros(9)))
checks.append(dict(name="no persistent spline bank", passed=not hasattr(compact, "splines") and compact.storage_bytes() == 21604748))
for module in list(sys.modules.values()):
    filename = getattr(module, "__file__", None)
    if filename and Path(filename).suffix == ".py" and Path(filename).resolve().is_relative_to(BASE):
        register(filename)
for filename in ("correlated_readout.py", "check_correlated_readout.py", "adjoint_readout.py", "nodal_readout.py"):
    register(ROOT / filename)
checks.append(dict(name="frozen source hashes unchanged", passed=all(hashlib.sha256(Path(path).read_bytes()).hexdigest() == checksum for path, checksum in sources.items())))
report = dict(passed=all(row["passed"] for row in checks), checks=checks, sources=sources,
    scope="Correlated readout representation on retained basis and six frozen physical backgrounds; no source integral or propagation",
    master_nodes=len(compact.frequency), tail_nodes=len(tail), persistent_array_bytes=compact.storage_bytes(),
    limit=1e-10, maximum_relative=max(row.get("relative", 0) for row in checks), seconds=time.monotonic()-started,
    process=dict(pid=process.pid, created_time=process.create_time(), command=process.cmdline(), priority=process.nice(), affinity=process.cpu_affinity()),
    finished_at=datetime.now(timezone.utc).isoformat(), propagation_changed=False, source_budget_assessed=False)
with (ROOT / "correlated-readout-validation.json").open("x", encoding="utf-8") as stream:
    json.dump(report, stream, indent=2)
print(json.dumps(dict(passed=report["passed"], checks=len(checks), maximum=report["maximum_relative"],
    failed=[row for row in checks if not row["passed"]][:12], seconds=report["seconds"], pid=process.pid)))
raise SystemExit(0 if report["passed"] else 1)
