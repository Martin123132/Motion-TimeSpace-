import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import json
import hashlib
import time
import math
from datetime import datetime, timezone
ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH / "low-frequency-temperature-law-20261019"
PARENT_SHA = "084d275a9a460f7e3886f6f0a0a645df1c2e1db3dcac51736b19589397df73a8"
sys.path.insert(0, str(BRANCH / "endpoint-state-precision-20261019"))
import stage165_common as physics
from precise_soft_shifts import PreciseSoftShifts
import numpy as np
import scipy.linalg as la
import mpmath as mp
START = .875
TARGET = .90625
OFFSETS = {"anchor": 0., "plus": .01, "minus": -.01, "plus_half": .005, "minus_half": -.005}
COMPONENTS = ["control", "difference", "virtual", "state", "remainder", "total"]
LOW = [0, 1, 2, 97]


def digest(path):
    result = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1048576), b""):
            result.update(block)
    return result.hexdigest()


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, indent=2, allow_nan=False), encoding="utf-8")
    temporary.replace(path)


def modest():
    import psutil
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity(list(range(psutil.cpu_count())))


def code_inputs():
    paths = {*ROOT.glob("*.py"), ROOT / "ACCEPTANCE.md", ROOT / "DERIVATION.md", PARENT / "results/stage-integrity.json"}
    for module in list(sys.modules.values()):
        filename = getattr(module, "__file__", None)
        if filename and Path(filename).suffix == ".py" and Path(filename).resolve().is_relative_to(BRANCH):
            paths.add(Path(filename).resolve())
    return paths


def check(rows, name, value, tolerance):
    rows.append(dict(name=name, value=float(value), tolerance=tolerance,
                     passed=bool(np.isfinite(value) and value < tolerance)))


def finish(folder, checks, inputs=(), **fields):
    inputs = code_inputs() | set(map(Path, inputs))
    report = dict(state="complete", finished_utc=datetime.now(timezone.utc).isoformat(), checks=checks,
                  count=len(checks), all_checks_passed=all(row["passed"] for row in checks),
                  input_hashes={str(path): digest(path) for path in sorted(inputs)}, **fields)
    write_json(folder / "status.json", report)
    (folder / "COMPLETE").write_text("complete\n", encoding="utf-8")
    return report


def verify(folder):
    report = json.loads((folder / "status.json").read_text())
    assert report["state"] == "complete" and (folder / "COMPLETE").exists()
    for filename, checksum in report["input_hashes"].items():
        assert digest(filename) == checksum, filename
    return report


def context(fraction):
    bundle = physics.EpochBundle(fraction)
    theta = physics.epoch_context(bundle)[0][0]["theta"]
    return bundle, theta


def virtual(parameters):
    identity = physics.event_owner.inherited.virtual_identity(parameters)
    key = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()
    locations = [BRANCH / name / "virtual-cache" / key[:2] / (key + ".json") for name in
                 ["predictor-anchor-order6-20261018", "incoming-band13-order8-20261018",
                  "targeted-frequency-band-refinement-20261018", "incoming-band820-order7-20261018"]]
    path = next((path for path in locations if path.exists()), ROOT / "virtual-cache" / key[:2] / (key + ".json"))
    reused = path.exists()
    if reused:
        packet = json.loads(path.read_text())
        assert packet["identity"] == identity and packet["finite"]
    else:
        unused, response = physics.weak.source.virtual_map(parameters, 2)
        packet = dict(identity=identity, scalar=float(response[0, 0]), finite=bool(np.isfinite(response[0, 0])))
        assert packet["finite"]
        write_json(path, packet)
    return packet["scalar"], path, reused


def models(bundle):
    full = {name: physics.FastSplit(bundle, name) for name in ["control", "difference"]}
    primitive = {name: PreciseSoftShifts(bundle) for name in ["control", "difference"]}
    primitive["control"].mode = "control"
    return full, primitive, physics.StableMoments(bundle)


class PairedHistory:
    def __init__(self, moving, fixed):
        self.parts = [moving, fixed]
        self.basis = moving.basis
        self.gas = [value for part in self.parts for value in part.gas]
        self.inputs = list(dict.fromkeys(path for part in self.parts for path in part.inputs))

    def functions(self, frequency, chemical=False):
        values = [part.functions(frequency, chemical) for part in self.parts]
        return np.concatenate([values[0][..., :1], *[value[..., 1:] for value in values]], axis=-1)

    def derivatives(self, frequency, chemical=False):
        values = [part.derivatives(frequency, chemical) for part in self.parts]
        return np.concatenate([values[0][..., :1], *[value[..., 1:] for value in values]], axis=-1)


class FourColumnView:
    def __init__(self, model, start):
        self.model = model
        self.start = start
        self.gas = model.gas[start:start+4]
        self.spectra = self

    def born_jumps(self, parameters):
        left, right = self.model.born_jumps(parameters)
        return left, right[self.start:self.start+4]

    def derivatives(self, frequency):
        values = self.model.spectra.derivatives(frequency)
        return np.concatenate([values[..., :1], values[..., 1+self.start:5+self.start]], axis=-1)


def evaluate(parameters, bundle, evaluators, scalar):
    full, primitive, state_model = evaluators
    upper, lower, diagnostics = {}, {}, {}
    for component in ["control", "difference"]:
        raw = full[component].real(parameters, angular=4, radial=18, rule=physics.PanelRule(.5))
        repaired = primitive[component].real(parameters, angular=4, radial=18, rule=physics.PanelRule(.5))
        upper[component], lower[component] = raw["total"], repaired["total"]
        diagnostics[component + "_event_null"] = float(repaired["event_energy_null"])
        diagnostics[component + "_shift_null"] = float(repaired["shift_energy_null"])
    with mp.workdps(60):
        vacuum = float(physics.weak.vacuum.finite_virtual_ratio(parameters["energy"], parameters["cosine"])
                       + physics.weak.vacuum.soft_constant(parameters["energy"], parameters["cosine"]))
    coefficient = .5 * (vacuum + scalar)
    unused, product = full["difference"].born_data(parameters)
    upper["virtual"] = coefficient * product
    upper["state"] = full["difference"].state_correction(parameters)["total"]
    with mp.workdps(80):
        unused, right = state_model.born_jumps(parameters)
        lower["virtual"] = np.array((mp.mpf(coefficient) * physics.outer(physics.exact_born_left(parameters), right)).tolist(), dtype=float)
    states, identities = [], []
    column_count = len(state_model.gas)
    for start in range(0, column_count, 4):
        state, identity = physics.precise_state(parameters, FourColumnView(state_model, start), 80)
        states.append(state["total"])
        identities.extend(identity.values())
    lower["state"] = np.concatenate(states, axis=-1)
    diagnostics["state_pair"] = max(identities)
    high, low = [], []
    with mp.workdps(80):
        norm0, norm1 = [mp.mpf(float(value)) for value in bundle.basis.norms[:2]]
        mean = mp.mpf(float(bundle.basis.mean))
        for component in COMPONENTS[:4]:
            values = upper[component].copy()
            correction = np.zeros_like(values)
            for column in range(column_count):
                energy, number, gas = map(lambda value: mp.mpf(float(value)), lower[component][:, column])
                exact = [energy, number / norm0, (energy - mean * number) / norm1, gas]
                for index, value in zip(LOW, exact):
                    values[index, column] = float(value)
                    correction[index, column] = float(value - mp.mpf(float(value)))
            high.append(values)
            low.append(correction)
        for indices in [[1, 2, 3], [0, 1, 2, 3]]:
            values = sum(high[index] for index in indices)
            correction = np.zeros_like(values)
            for row in LOW:
                for column in range(column_count):
                    exact = sum(mp.mpf(float(high[index][row, column])) + mp.mpf(float(low[index][row, column])) for index in indices)
                    values[row, column] = float(exact)
                    correction[row, column] = float(exact - mp.mpf(float(exact)))
            high.append(values)
            low.append(correction)
    return np.array(high), np.array(low), diagnostics


def photon_norm(values, mass):
    factor = la.cholesky(mass, lower=True)
    shape = values.shape
    reshaped = np.moveaxis(values[..., 1:97, :], -2, 0).reshape(96, -1)
    norms = np.linalg.norm(la.solve_triangular(factor, reshaped, lower=True), axis=0)
    return norms.reshape(shape[:-2] + (shape[-1],))


def precise_combine(pairs, coefficients):
    high = sum(float(coefficient)*pair[0] for pair, coefficient in zip(pairs, coefficients))
    low = np.zeros_like(high)
    with mp.workdps(80):
        for prefix in np.ndindex(high.shape[:-2]):
            for row in LOW:
                for column in range(high.shape[-1]):
                    index = prefix + (row, column)
                    value = sum(mp.mpf(float(coefficient))*(mp.mpf(float(pair[0][index]))+
                                mp.mpf(float(pair[1][index]))) for pair, coefficient in zip(pairs, coefficients))
                    high[index] = float(value)
                    low[index] = float(value-mp.mpf(float(value)))
    return high, low
