from __future__ import annotations

import os
for variable in ["OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"]:
    os.environ[variable] = "1"
import sys
sys.dont_write_bytecode = True
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import time

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH / "smooth-local-collision-evolution-20261021"
PARENT_SHA = "f71ef7a74dde0b244346e1e456e8a05b5e9b05d990aed14554ee435ecbf718b2"
sys.path.insert(0, str(PARENT))
import smooth_stage187 as previous

np, mp, linear = previous.np, previous.mp, previous.linear
saved, source = previous.saved, previous.source
read, write, check = previous.read, previous.write, previous.check
corner, old = previous.corner, previous.old
packet = previous.packet
MODELS, KINDS, GRIDS = previous.MODELS, previous.KINDS, previous.GRIDS
METHODS = ["linear", "partial", "split"]
QUANTITIES = previous.QUANTITIES


def authenticate():
    path = PARENT / "results/stage-integrity.json"
    assert saved.digest(path) == PARENT_SHA
    seal = read(path)
    paths = dict(seal["consumed_and_immediate_rehashed"])
    paths.update({str(PARENT / name): checksum for name, checksum in seal["file_hashes"].items()})
    paths[str(path)] = PARENT_SHA
    for filename, checksum in paths.items():
        assert saved.digest(filename) == checksum, filename
    return paths


def destination(model, kind, grid, index):
    return ROOT / "probes" / model / kind / grid / f"probe-{index}.json"


def history(model, kind, grid):
    if kind == "bank":
        original = corner.history(model, grid)
        return dict(coordinates=original["coordinates"], expansion=original["expansion"], step=float(original["step"]),
                    profiles=original["profiles"], gas=original["temperature_scaled"], work=original["expansion_work"],
                    heat=float(original["heat"]))
    directory = PARENT / "histories" / model / grid
    status = read(directory / "status.json")
    assert saved.digest(directory / "history.npz") == status["history_sha256"]
    original = packet(directory / "history.npz")
    return dict(coordinates=original["coordinates"], expansion=original["expansion"], step=float(original["step"]),
                profiles=original["candidate_profiles"], gas=original["candidate_gas"], work=original["candidate_work"],
                heat=float(original["heat"]))


def geometry(original, index):
    target = float(original["coordinates"][index])
    coordinates = original["expansion"]
    position = int(np.searchsorted(coordinates, target))
    exact = bool(position < len(coordinates) and float(coordinates[position]) == target)
    left = position if exact else position - 1
    assert 0 < left < len(coordinates)
    if not exact:
        assert left + 1 < len(coordinates) and coordinates[left] < target < coordinates[left + 1]
    return dict(target=target, exact_node=exact, left_index=left,
                left=float(coordinates[left]), previous=float(coordinates[left - 1]),
                right=None if exact else float(coordinates[left + 1]),
                nominal_previous_step=float(original["step"]),
                represented_previous_spacing=float(coordinates[left] - coordinates[left - 1]),
                partial_step=float(target - coordinates[left]),
                ulps_from_left=float((target - coordinates[left]) / np.spacing(target)))


def prepare():
    assert not (ROOT / "configuration.json").exists()
    paths = authenticate()
    prior_config = read(PARENT / "configuration.json")
    assert prior_config["source_prediction_tolerance"] == .01 and prior_config["identity_tolerance"] == 1e-10
    locations = {}
    rows = []
    for grid in GRIDS:
        original = history("heavy", "bank", grid)
        locations[grid] = [geometry(original, index) for index in range(5)]
        for model in MODELS:
            for kind in KINDS:
                other = history(model, kind, grid)
                assert np.array_equal(other["expansion"], original["expansion"])
                assert np.array_equal(other["coordinates"], original["coordinates"])
                assert other["step"] == original["step"]
        with mp.workdps(80):
            for point in locations[grid]:
                if point["exact_node"]:
                    continue
                ratio = (mp.mpf(point["target"]) - mp.mpf(point["left"])) / mp.mpf(point["nominal_previous_step"])
                for effective_ratio in [ratio, ratio / 2, mp.mpf(1)]:
                    coefficient = (1 + 2 * effective_ratio) / (1 + effective_ratio)
                    previous_weight = effective_ratio ** 2 / (1 + effective_ratio)
                    for degree in range(3):
                        derivative = coefficient * mp.mpf(0) ** degree - (1 + effective_ratio) * (-mp.mpf(1)) ** degree
                        derivative += previous_weight * (-1 - 1 / effective_ratio) ** degree
                        expected = 1 if degree == 1 else 0
                        check(rows, f"{grid}:{point['target']}:{effective_ratio}: polynomial{degree}", derivative - expected)
    assert all(row["passed"] for row in rows)
    write(ROOT / "results/rule-checks.json", dict(checks=rows))
    protocol = {name: saved.digest(ROOT / name) for name in ["ACCEPTANCE.md", "DERIVATION.md"]}
    config = dict(stage=188, started_utc=datetime.now(timezone.utc).isoformat(), parent_seal_sha256=PARENT_SHA,
                  source_prediction_tolerance=.01, identity_tolerance=1e-10, working_digits=80, audit_digits=100,
                  locations=locations, protocol_hashes=protocol, grids=GRIDS, models=MODELS, kinds=KINDS, methods=METHODS,
                  candidate_sha256=prior_config["candidate_sha256"], previous_step="saved nominal BDF step, represented coordinate gap also recorded",
                  source_scope="Fixed-anchor gas-only projection through unchanged 36 event kernels",
                  bookmark_hashes={str(path): saved.digest(path) for path in [BRANCH / "RESUME-CURRENT.md", BRANCH.parent / "CURRENT_LOCAL_RESUME.md"]})
    write(ROOT / "configuration.json", config)
    write(ROOT / "authenticated-inputs.json", paths)
    write(ROOT / "progress.json", dict(state="protocol_frozen", completed_probes=0))
    print(json.dumps(dict(state="protocol_frozen", inputs=len(paths), rule_checks=len(rows),
                          off_node_cases=48, exact_node_cases=12, working_digits=80)), flush=True)


def protocol():
    config = read(ROOT / "configuration.json")
    for name, checksum in config["protocol_hashes"].items():
        assert saved.digest(ROOT / name) == checksum
    assert saved.digest(PARENT / "results/frozen-candidate.npz") == config["candidate_sha256"]
    return config


def state_at(original, index):
    return dict(profile=corner.mp_vector(original["profiles"][index]),
                gas=mp.mpf(float(original["gas"][index])), work=mp.mpf(float(original["work"][index])))


def serial_state(state):
    return dict(profile=[str(value) for value in state["profile"]], gas=str(state["gas"]), work=str(state["work"]))


class ProbeEquation:
    def __init__(self, model, kind):
        self.ladder, self.basis, self.theta0 = old.setup()
        self.operator = corner.Operators(model, self.ladder)
        self.kind = kind
        self.frozen = previous.frozen_candidate()
        self.mass = corner.mp_matrix(self.basis.mass)
        self.energy = corner.mp_vector(self.basis.energy).T
        self.template = corner.mp_vector(self.basis.temperature)
        self.heat = mp.mpf(float(self.operator.background.chi))
        self.solves = 0

    def stiffness(self, coordinate):
        local = self.operator.background.at(float(coordinate))
        if self.kind == "bank":
            scattering = self.ladder.at(local["thermal_parameter"], 0)
        else:
            offset = float(np.log(local["thermal_parameter"] / self.theta0))
            lower, upper = read(PARENT / "configuration.json")["domain"]
            assert lower - 1e-14 <= offset <= upper + 1e-14
            scattering = previous.candidate(offset, self.frozen)
        emission = self.operator.emission.at(local["thermal_parameter"], "dcbr")
        rate = local["coefficient"] / local["thermal_parameter"]
        return corner.mp_matrix(rate * (scattering - emission))

    def advance(self, current, older, coordinate, step, previous_step):
        assert step > 0 and previous_step > 0
        ratio = step / previous_step
        coefficient = (1 + 2 * ratio) / (1 + ratio)
        older_weight = ratio ** 2 / (1 + ratio)
        stiffness = self.stiffness(coordinate)
        profile_change = current["profile"] - older["profile"]
        gas_change = current["gas"] - older["gas"]
        departure = current["profile"] - self.template * current["gas"]
        system = coefficient * self.mass - step * stiffness
        decomposition, permutation = mp.mp.LU_decomp(system)

        def solve(vector):
            return mp.mp.U_solve(decomposition, mp.mp.L_solve(decomposition, vector, permutation))

        free = solve(older_weight * self.mass * profile_change + step * stiffness * departure)
        response = solve(-step * stiffness * self.template)
        denominator = self.heat * (coefficient + step) + coefficient * (self.energy * response)[0]
        assert denominator > 0
        gas_increment = (older_weight * ((self.energy * profile_change)[0] + self.heat * gas_change)
                         - coefficient * (self.energy * free)[0] - step * (1 + self.heat * current["gas"])) / denominator
        profile_increment = free + response * gas_increment
        new_gas = current["gas"] + gas_increment
        work_increment = (older_weight * (current["work"] - older["work"]) + step * (1 + self.heat * new_gas)) / coefficient
        result = dict(profile=current["profile"] + profile_increment, gas=new_gas, work=current["work"] + work_increment)
        rhs = step * stiffness * (result["profile"] - self.template * new_gas)
        residual = coefficient * self.mass * profile_increment - older_weight * self.mass * profile_change - rhs
        norm = lambda vector: mp.sqrt(mp.fsum(value * value for value in vector))
        scale = max(norm(coefficient * self.mass * profile_increment), norm(older_weight * self.mass * profile_change), norm(rhs))
        gas_residual = ((self.energy * (coefficient * profile_increment - older_weight * profile_change))[0]
                        + self.heat * (coefficient * gas_increment - older_weight * gas_change)
                        + step * (1 + self.heat * new_gas)) / step
        work_residual = (coefficient * work_increment - older_weight * (current["work"] - older["work"])) / step - 1 - self.heat * new_gas
        energy = (self.energy * result["profile"])[0] + self.heat * new_gas + result["work"]
        diagnostics = dict(kinetic_relative=float(norm(residual) / scale), gas_energy_residual=float(gas_residual),
                           work_residual=float(work_residual), integrated_energy=float(energy),
                           denominator=str(denominator), ratio=str(ratio), partial_step=str(step),
                           exact_coordinate=str(coordinate), coefficient_coordinate=float(coordinate))
        self.solves += 1
        return result, diagnostics


def sample(model, kind, grid, index):
    config = protocol()
    path = destination(model, kind, grid, index)
    if path.exists():
        result = read(path)
        assert result["candidate_sha256"] == config["candidate_sha256"]
        assert result["protocol_hashes"] == config["protocol_hashes"]
        assert not result["failed_checks"]
        print(json.dumps(dict(reused=str(path))), flush=True)
        return
    original = history(model, kind, grid)
    point = geometry(original, index)
    assert point == config["locations"][grid][index]
    began = time.monotonic()
    checks, diagnostics, audit = [], [], None
    with mp.workdps(80):
        current = state_at(original, point["left_index"])
        older = state_at(original, point["left_index"] - 1)
        if point["exact_node"]:
            partial = split = current
            solves = 0
            check(checks, "exact existing node reused without snapping", 0)
            replay = None
        else:
            equation = ProbeEquation(model, kind)
            assert equation.heat == mp.mpf(original["heat"])
            step = mp.mpf(point["target"]) - mp.mpf(point["left"])
            previous_step = mp.mpf(point["nominal_previous_step"])
            partial, diagnostic = equation.advance(current, older, mp.mpf(point["target"]), step, previous_step)
            diagnostics.append(dict(diagnostic, method="partial"))
            midpoint = mp.mpf(point["left"]) + step / 2
            assert point["left"] < float(midpoint) < point["target"]
            intermediate, diagnostic = equation.advance(current, older, midpoint, step / 2, previous_step)
            diagnostics.append(dict(diagnostic, method="split_first"))
            split, diagnostic = equation.advance(intermediate, current, mp.mpf(point["target"]), step / 2, step / 2)
            diagnostics.append(dict(diagnostic, method="split_second"))
            replay_state, diagnostic = equation.advance(current, older, mp.mpf(point["right"]), previous_step, previous_step)
            diagnostics.append(dict(diagnostic, method="nominal_full_step_replay"))
            right = state_at(original, point["left_index"] + 1)
            norm = lambda vector: mp.sqrt(mp.fsum(value * value for value in vector))
            replay = dict(profile_relative=float(norm(replay_state["profile"] - right["profile"]) / norm(right["profile"])),
                          gas_absolute=float(abs(replay_state["gas"] - right["gas"])),
                          work_absolute=float(abs(replay_state["work"] - right["work"])))
            for name, value in replay.items():
                check(checks, "saved full-step replay: " + name, value)
            for diagnostic in diagnostics:
                for name in ["kinetic_relative", "gas_energy_residual", "work_residual", "integrated_energy"]:
                    check(checks, diagnostic["method"] + ": " + name, diagnostic[name])
            solves = equation.solves
        partial_serial, split_serial = serial_state(partial), serial_state(split)
    if grid == "quarter":
        with mp.workdps(100):
            if point["exact_node"]:
                audited = state_at(original, point["left_index"])
            else:
                equation = ProbeEquation(model, kind)
                audited, audit_diagnostic = equation.advance(state_at(original, point["left_index"]),
                    state_at(original, point["left_index"] - 1), mp.mpf(point["target"]),
                    mp.mpf(point["target"]) - mp.mpf(point["left"]), mp.mpf(point["nominal_previous_step"]))
                solves += equation.solves
                for name in ["kinetic_relative", "gas_energy_residual", "work_residual", "integrated_energy"]:
                    check(checks, "100-digit partial: " + name, audit_diagnostic[name])
            audit = serial_state(audited)
            difference = abs(audited["gas"] - mp.mpf(partial_serial["gas"]))
            check(checks, "80/100-digit gas absolute agreement", difference)
    linear_value = float(np.interp(point["target"], original["expansion"], original["gas"]))
    failed = [row for row in checks if not row["passed"]]
    write(path, dict(state="complete", model=model, kind=kind, grid=grid, index=index, geometry=point,
          linear_gas=linear_value, partial=partial_serial, split=split_serial, audit=audit,
          checks=checks, failed_checks=failed, diagnostics=diagnostics, replay=replay,
          solves=solves, right_hand_sides_per_solve=2, elapsed_seconds=time.monotonic() - began,
          working_digits=80, protocol_hashes=config["protocol_hashes"], candidate_sha256=config["candidate_sha256"]))
    completed = len(list((ROOT / "probes").rglob("probe-*.json")))
    write(ROOT / "progress.json", dict(state="sampling", completed_probes=completed, last_probe=str(path)))
    print(json.dumps(dict(model=model, kind=kind, grid=grid, probe=index, exact=point["exact_node"], solves=solves,
                          failed=failed, elapsed_seconds=time.monotonic() - began)), flush=True)
    assert not failed


def batch():
    began = time.monotonic()
    for model in MODELS:
        for kind in KINDS:
            for grid in GRIDS:
                for index in range(5):
                    if time.monotonic() - began > 3 * 3600:
                        write(ROOT / "progress.json", dict(state="safe_restart", next_probe=[model, kind, grid, index]))
                        print("Safe restart saved before four-hour check-in.", flush=True)
                        return
                    sample(model, kind, grid, index)
    write(ROOT / "progress.json", dict(state="samples_complete", completed_probes=60))


if __name__ == "__main__":
    source.modest()
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=["prepare", "sample", "batch"])
    parser.add_argument("--model", choices=MODELS)
    parser.add_argument("--kind", choices=KINDS)
    parser.add_argument("--grid", choices=GRIDS)
    parser.add_argument("--index", type=int, choices=range(5))
    arguments = parser.parse_args()
    if arguments.phase == "sample":
        sample(arguments.model, arguments.kind, arguments.grid, arguments.index)
    else:
        dict(prepare=prepare, batch=batch)[arguments.phase]()

