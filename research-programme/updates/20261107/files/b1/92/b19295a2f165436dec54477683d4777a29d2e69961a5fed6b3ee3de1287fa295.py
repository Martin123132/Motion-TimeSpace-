from __future__ import annotations
import os
for variable in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[variable] = "1"
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import argparse
import hashlib
import json
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH / "equation-sampled-gas-probes-20261021"
PARENT_SHA = "b8742a115397667f41e34cdbe0f44ab6061824d9669a1f7d3104265f8e4dde98"
sys.path.insert(0, str(PARENT))
import probe_stage188 as previous
np, mp, linear = previous.np, previous.mp, previous.linear
saved, read, check, packet = previous.saved, previous.read, previous.check, previous.packet
MODELS, KINDS, GRIDS = ["heavy", "cold"], ["bank", "candidate"], ["half", "quarter"]
DIGITS, BLOCK = 80, 8


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".partial")
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def authenticate():
    seal_path = PARENT / "results/stage-integrity.json"
    assert saved.digest(seal_path) == PARENT_SHA
    seal = read(seal_path)
    paths = dict(seal["consumed_and_immediate_rehashed"])
    paths.update({str(PARENT / name): checksum for name, checksum in seal["file_hashes"].items()})
    paths[str(seal_path)] = PARENT_SHA
    for name in ("MTS-COSMOLOGY-LAB-HANDOFF.md", "MTS-HOLDOUT-DATA-EXPOSURE-HANDOFF.md"):
        path = BRANCH.parent / name
        assert path.is_file()
        paths.setdefault(str(path), saved.digest(path))
    for name, checksum in paths.items():
        assert saved.digest(name) == checksum, name
    return paths


def protocol():
    config = read(ROOT / "configuration.json")
    for name, checksum in config["protocol_hashes"].items():
        assert saved.digest(ROOT / name) == checksum
    assert saved.digest(previous.PARENT / "results/frozen-candidate.npz") == config["candidate_sha256"]
    return config


def directory(model, kind, grid):
    return ROOT / "histories" / model / kind / grid


def parse_state(state):
    return dict(profile=mp.matrix([mp.mpf(value) for value in state["profile"]]),
                gas=mp.mpf(state["gas"]), work=mp.mpf(state["work"]))


def seeds(model, grid):
    original = previous.corner.history(model, grid)
    native = packet(previous.corner.ENERGY / "results" / model / "state.npz")
    start = int(original["start_index"])
    current = dict(profile=previous.corner.mp_vector(original["initial_profile"]),
                   gas=mp.mpf(float(original["initial_gas"])),
                   work=mp.mpf(float(native["expansion_work"][start])))
    older = dict(profile=previous.corner.mp_vector(original["initial_previous_profile"]),
                 gas=mp.mpf(float(original["initial_previous_gas"])),
                 work=mp.mpf(float(native["expansion_work"][start - 1])))
    return current, older


def spacing(history, grid, ordinal):
    step = mp.mpf(float(history["step"]))
    previous_step = step * (dict(half=2, quarter=4)[grid] if ordinal == 1 else 1)
    return step, previous_step


def identity_rows(diagnostics, prefix=""):
    rows = []
    for diagnostic in diagnostics:
        for name in ("kinetic_relative", "gas_energy_residual", "work_residual", "integrated_energy"):
            check(rows, prefix + str(diagnostic["ordinal"]) + ": " + name, diagnostic[name])
    return rows


class Equation(previous.ProbeEquation):
    def __init__(self, model, kind):
        super().__init__(model, kind)
        self.last_stiffness_hash = None

    def stiffness(self, coordinate):
        result = super().stiffness(coordinate)
        binary = np.array(result.tolist(), dtype="<f8")
        self.last_stiffness_hash = hashlib.sha256(binary.tobytes()).hexdigest()
        return result


def reference(model, kind, grid):
    target = directory(model, kind, grid)
    assert not (target / "reference.json").exists()
    original = previous.history(model, kind, grid)
    with mp.workdps(DIGITS):
        equation = Equation(model, kind)
        current_mp, older_mp = seeds(model, grid)
        current = dict(profile=np.array(list(current_mp["profile"]), dtype=float),
                       gas=float(current_mp["gas"]), work=float(current_mp["work"]))
        older = dict(profile=np.array(list(older_mp["profile"]), dtype=float),
                     gas=float(older_mp["gas"]), work=float(older_mp["work"]))
        mass = np.array(equation.mass.tolist(), dtype=float)
        energy = np.array(list(equation.energy), dtype=float)
        template = np.array(list(equation.template), dtype=float)
        heat = float(equation.heat)
        states, checks, hashes = [current.copy()], [], []
        step = float(original["step"])
        for ordinal, coordinate in enumerate(original["expansion"][1:], 1):
            ratio = 1 / dict(half=2, quarter=4)[grid] if ordinal == 1 else 1.
            coefficient, weight = (1 + 2 * ratio) / (1 + ratio), ratio ** 2 / (1 + ratio)
            stiffness = np.array(equation.stiffness(float(coordinate)).tolist(), dtype=float)
            hashes.append(equation.last_stiffness_hash)
            profile_change = current["profile"] - older["profile"]
            gas_change = current["gas"] - older["gas"]
            departure = current["profile"] - template * current["gas"]
            system = coefficient * mass - step * stiffness
            solution = linear.solve(system, np.column_stack((
                weight * mass @ profile_change + step * stiffness @ departure,
                -step * stiffness @ template)), assume_a="gen")
            free, response = solution[:, 0], solution[:, 1]
            denominator = heat * (coefficient + step) + coefficient * (energy @ response)
            assert np.isfinite(denominator) and denominator > 0
            gas_increment = (weight * (energy @ profile_change + heat * gas_change)
                             - coefficient * (energy @ free) - step * (1 + heat * current["gas"])) / denominator
            profile_increment = free + response * gas_increment
            next_gas = current["gas"] + gas_increment
            work_increment = (weight * (current["work"] - older["work"]) + step * (1 + heat * next_gas)) / coefficient
            new = dict(profile=current["profile"] + profile_increment, gas=next_gas, work=current["work"] + work_increment)
            energy_error = float(energy @ new["profile"] + heat * new["gas"] + new["work"])
            check(checks, f"{ordinal}: binary64 energy", energy_error, category="binary64_control")
            older, current = current, new
            states.append(new)
        target.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(target / "reference.npz", profiles=np.array([state["profile"] for state in states]),
                            gas=np.array([state["gas"] for state in states]), work=np.array([state["work"] for state in states]),
                            expansion=original["expansion"], coordinates=original["coordinates"], step=step)
        write(target / "reference.json", dict(sha256=saved.digest(target / "reference.npz"),
              stiffness_hashes=hashes, checks=checks, updates=len(hashes),
              initial=previous.serial_state(current_mp), previous=previous.serial_state(older_mp),
              physical_inputs="inherited binary64; full matrix; stable increment; general solve"))
    return len(hashes)


def prepare():
    assert not (ROOT / "configuration.json").exists()
    paths = authenticate()
    old_config = read(PARENT / "configuration.json")
    assert old_config["source_prediction_tolerance"] == .01 and old_config["identity_tolerance"] == 1e-10
    write(ROOT / "configuration.json", dict(stage=189, started_utc=datetime.now(timezone.utc).isoformat(),
          protocol_hashes={name: saved.digest(ROOT / name) for name in ["ACCEPTANCE.md", "DERIVATION.md"]},
          candidate_sha256=old_config["candidate_sha256"], source_prediction_tolerance=.01,
          identity_tolerance=1e-10, primary_digits=DIGITS, pilot_audit_digits=100, block_size=BLOCK,
          bookmark_hashes={str(path): saved.digest(path) for path in [BRANCH / "RESUME-CURRENT.md", BRANCH.parent / "CURRENT_LOCAL_RESUME.md"]}))
    write(ROOT / "authenticated-inputs.json", paths)
    updates = 0
    for model in MODELS:
        for kind in KINDS:
            for grid in GRIDS:
                updates += reference(model, kind, grid)
    assert updates == 1464
    write(ROOT / "progress.json", dict(state="prepared", binary64_reference_updates=updates))
    print(json.dumps(dict(state="prepared", inputs=len(paths), reference_updates=updates)), flush=True)


def evolve_block(model, kind, grid, first, last, current, older, digits):
    original = previous.history(model, kind, grid)
    reference_data = read(directory(model, kind, grid) / "reference.json")
    states, diagnostics = [], []
    began = time.monotonic()
    with mp.workdps(digits):
        equation = Equation(model, kind)
        for ordinal in range(first, last + 1):
            step, previous_step = spacing(original, grid, ordinal)
            new, diagnostic = equation.advance(current, older, mp.mpf(float(original["expansion"][ordinal])), step, previous_step)
            assert equation.last_stiffness_hash == reference_data["stiffness_hashes"][ordinal - 1]
            diagnostic.update(ordinal=ordinal, stiffness_sha256=equation.last_stiffness_hash)
            diagnostics.append(diagnostic)
            states.append(dict(index=ordinal, state=previous.serial_state(new)))
            older, current = current, new
    checks = identity_rows(diagnostics)
    return dict(model=model, kind=kind, grid=grid, digits=digits, first=first, last=last,
                states=states, diagnostics=diagnostics, checks=checks, failed_checks=[row for row in checks if not row["passed"]],
                solves=last-first+1, elapsed_seconds=time.monotonic()-began)


def pilot():
    protocol()
    assert read(ROOT / "progress.json")["state"] == "prepared"
    outputs = []
    for digits in (80, 100):
        with mp.workdps(digits):
            current, older = seeds("cold", "quarter")
            result = evolve_block("cold", "candidate", "quarter", 1, BLOCK, current, older, digits)
        write(ROOT / "pilot" / f"digits-{digits}.json", result)
        assert not result["failed_checks"]
        outputs.append(result)
    checks = []
    with mp.workdps(100):
        for primary, audit in zip(outputs[0]["states"], outputs[1]["states"]):
            first, second = parse_state(primary["state"]), parse_state(audit["state"])
            norm = lambda vector: mp.sqrt(mp.fsum(value * value for value in vector))
            check(checks, str(primary["index"]) + ": pilot profile relative", norm(first["profile"]-second["profile"]) / norm(second["profile"]))
            for name in ("gas", "work"):
                check(checks, str(primary["index"]) + ": pilot " + name + " absolute", first[name]-second[name])
    write(ROOT / "pilot/status.json", dict(checks=checks, failed_checks=[row for row in checks if not row["passed"]],
          primary_seconds=outputs[0]["elapsed_seconds"], audit_seconds=outputs[1]["elapsed_seconds"]))
    assert all(row["passed"] for row in checks)
    first_block = dict(outputs[0], previous_block_sha256=None, protocol_hashes=protocol()["protocol_hashes"])
    write(directory("cold", "candidate", "quarter") / "blocks/0001.json", first_block)
    write(ROOT / "progress.json", dict(state="pilot_passed", primary_updates=BLOCK))
    print(json.dumps(dict(state="pilot_passed", checks=len(checks), primary_seconds=outputs[0]["elapsed_seconds"],
                          audit_seconds=outputs[1]["elapsed_seconds"])), flush=True)


def read_history(model, kind, grid):
    target = directory(model, kind, grid)
    metadata = read(target / "reference.json")
    assert saved.digest(target / "reference.npz") == metadata["sha256"]
    states = [metadata["initial"]]
    checks, previous_hash = [], None
    for block in sorted((target / "blocks").glob("*.json")):
        data = read(block)
        assert data["previous_block_sha256"] == previous_hash
        assert data["protocol_hashes"] == protocol()["protocol_hashes"]
        assert data["first"] == len(states) and not data["failed_checks"]
        for row in data["states"]:
            assert row["index"] == len(states)
            states.append(row["state"])
        checks.extend(data["checks"])
        previous_hash = saved.digest(block)
    return states, checks, previous_hash


def sample(model, kind, grid, representation, states):
    target = directory(model, kind, grid) / f"probes-{representation}.json"
    if target.exists():
        result = read(target)
        assert not result["failed_checks"]
        return
    original = previous.history(model, kind, grid)
    records, checks, solves = [], [], 0
    with mp.workdps(DIGITS):
        equation = Equation(model, kind)
        for index in range(5):
            point = previous.geometry(original, index)
            current = parse_state(states[point["left_index"]])
            older = parse_state(states[point["left_index"] - 1])
            if point["exact_node"]:
                partial = split = current
            else:
                step = mp.mpf(point["target"]) - mp.mpf(point["left"])
                previous_step = mp.mpf(point["nominal_previous_step"])
                partial, diagnostic = equation.advance(current, older, mp.mpf(point["target"]), step, previous_step)
                checks.extend(identity_rows([dict(diagnostic, ordinal=f"{index}:partial")]))
                midpoint = mp.mpf(point["left"]) + step / 2
                intermediate, diagnostic = equation.advance(current, older, midpoint, step / 2, previous_step)
                checks.extend(identity_rows([dict(diagnostic, ordinal=f"{index}:split-first")]))
                split, diagnostic = equation.advance(intermediate, current, mp.mpf(point["target"]), step / 2, step / 2)
                checks.extend(identity_rows([dict(diagnostic, ordinal=f"{index}:split-second")]))
            record = dict(index=index, geometry=point, partial=previous.serial_state(partial), split=previous.serial_state(split))
            if grid == "quarter":
                with mp.workdps(100):
                    if point["exact_node"]:
                        audit = parse_state(states[point["left_index"]])
                    else:
                        audit_equation = Equation(model, kind)
                        audit, diagnostic = audit_equation.advance(parse_state(states[point["left_index"]]),
                            parse_state(states[point["left_index"]-1]), mp.mpf(point["target"]),
                            mp.mpf(point["target"])-mp.mpf(point["left"]), mp.mpf(point["nominal_previous_step"]))
                        solves += audit_equation.solves
                        checks.extend(identity_rows([dict(diagnostic, ordinal=f"{index}:audit100")]))
                    record["audit"] = previous.serial_state(audit)
                    check(checks, f"{index}: 80/100 probe gas", audit["gas"]-mp.mpf(record["partial"]["gas"]))
            records.append(record)
        solves += equation.solves
    result = dict(records=records, checks=checks, failed_checks=[row for row in checks if not row["passed"]], solves=solves,
                  model=model, kind=kind, grid=grid, representation=representation)
    write(target, result)
    assert not result["failed_checks"]


def batch():
    config = protocol()
    assert not (ROOT / "results/stage-integrity.json").exists()
    assert not read(ROOT / "pilot/status.json")["failed_checks"]
    began = time.monotonic()
    for model in MODELS:
        for kind in KINDS:
            for grid in GRIDS:
                original = previous.history(model, kind, grid)
                target = directory(model, kind, grid)
                states, checks, previous_hash = read_history(model, kind, grid)
                while len(states) < len(original["expansion"]):
                    if time.monotonic()-began > 3*3600:
                        write(ROOT / "progress.json", dict(state="safe_restart", model=model, kind=kind, grid=grid, next_index=len(states)))
                        print("Safe restart saved.", flush=True)
                        return
                    first, last = len(states), min(len(states)+BLOCK-1, len(original["expansion"])-1)
                    with mp.workdps(DIGITS):
                        current = parse_state(states[-1])
                        older = parse_state(states[-2]) if len(states)>1 else parse_state(read(target / "reference.json")["previous"])
                        result = evolve_block(model, kind, grid, first, last, current, older, DIGITS)
                    result.update(previous_block_sha256=previous_hash, protocol_hashes=config["protocol_hashes"])
                    path = target / "blocks" / f"{first:04d}.json"
                    assert not path.exists()
                    write(path, result)
                    assert not result["failed_checks"]
                    previous_hash = saved.digest(path)
                    states.extend([row["state"] for row in result["states"]])
                    write(ROOT / "progress.json", dict(state="evolving", model=model, kind=kind, grid=grid,
                          completed_index=last, total_indices=len(original["expansion"])-1))
                    print(json.dumps(dict(model=model, kind=kind, grid=grid, through=last,
                          total=len(original["expansion"])-1, seconds=result["elapsed_seconds"], failures=0)), flush=True)
                sample(model, kind, grid, "precision80", states)
                reference_data = packet(target / "reference.npz")
                with mp.workdps(DIGITS):
                    binary_states = [previous.serial_state(dict(profile=previous.corner.mp_vector(reference_data["profiles"][index]),
                                     gas=mp.mpf(float(reference_data["gas"][index])), work=mp.mpf(float(reference_data["work"][index]))))
                                     for index in range(len(states))]
                sample(model, kind, grid, "increment64", binary_states)
    write(ROOT / "progress.json", dict(state="evolution_complete", primary_history_updates=1464))
    print("Evolution and all original probes complete.", flush=True)


if __name__ == "__main__":
    import psutil
    psutil.Process().nice(psutil.NORMAL_PRIORITY_CLASS)
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=["prepare", "pilot", "batch"])
    arguments = parser.parse_args()
    globals()[arguments.phase]()
