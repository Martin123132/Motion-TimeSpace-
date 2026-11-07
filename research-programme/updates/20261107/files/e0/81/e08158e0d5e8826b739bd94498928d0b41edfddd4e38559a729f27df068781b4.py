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
PARENT = BRANCH / "collision-temperature-curvature-20261021"
PARENT_SHA = "c0a98715459c37a1dba53f35555455c0add86236b764f3ce9c9ae2100218a55d"
sys.path.insert(0, str(PARENT))
import curvature_stage186 as previous

np, mp, saved, source, linear = previous.np, previous.mp, previous.saved, previous.source, previous.linear
read, write, check = previous.read, previous.write, previous.check
old, corner = previous.old, previous.prior
native = corner.native
MODELS = ["heavy", "cold"]
GRIDS = ["native", "half", "quarter"]
KINDS = ["bank", "candidate"]
QUANTITIES = ["coarse_curvature", "fine_curvature", "width_discrepancy"]


def packet(path):
    with np.load(path) as archive:
        return {key: archive[key].copy() for key in archive.files}


def authenticate():
    seal_path = PARENT / "results/stage-integrity.json"
    assert saved.digest(seal_path) == PARENT_SHA
    seal = read(seal_path)
    paths = dict(seal["consumed_and_immediate_rehashed"])
    paths.update({str(PARENT / name): checksum for name, checksum in seal["file_hashes"].items()})
    paths[str(seal_path)] = PARENT_SHA
    for filename, checksum in paths.items():
        assert saved.digest(filename) == checksum, filename
    return paths


def candidate(offset, frozen):
    return frozen["block"] + offset * frozen["tangent"] + .5 * offset ** 2 * frozen["curvature"]


def prepare():
    assert not (ROOT / "configuration.json").exists()
    paths = authenticate()
    parent_config = read(PARENT / "configuration.json")
    assert parent_config["source_prediction_tolerance"] == .01 and parent_config["identity_tolerance"] == 1e-10
    schedules = {}
    for model in MODELS:
        history = corner.history(model, "native")
        anchor = float(history["coordinates"][0])
        schedules[model] = dict(anchor=anchor, warm=anchor - float(history["expansion"][0]),
                                cold=anchor - float(history["expansion"][-1]), targets=history["coordinates"].tolist())
    assert schedules["heavy"] == schedules["cold"]
    endpoints = [schedules["heavy"]["cold"], schedules["heavy"]["warm"]]
    frozen = packet(PARENT / "results/frozen-curvature.npz")
    directory = ROOT / "results"
    directory.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(directory / "frozen-candidate.npz", **{key: frozen[key] for key in ["block", "tangent", "curvature"]},
                        endpoints=np.array(endpoints), edge_predictions=np.array([candidate(offset, frozen) for offset in endpoints]))
    checksum = saved.digest(directory / "frozen-candidate.npz")
    write(ROOT / "configuration.json", dict(stage=187, started_utc=datetime.now(timezone.utc).isoformat(),
          parent_seal_sha256=PARENT_SHA, source_prediction_tolerance=.01, identity_tolerance=1e-10,
          domain=endpoints, schedules=schedules, candidate_sha256=checksum, grids=GRIDS, models=MODELS,
          extension_reason="Exact saved restart/end grids extend slightly beyond |t|=.01; freeze and directly test both outer temperatures before evolving",
          comparison_scope="Local coupled photon/gas evolution; unchanged background and emission; cached fixed-anchor baseline/MTS gas-source projection",
          parent_coefficient_sha256=saved.digest(PARENT / "results/frozen-curvature.npz"),
          bookmark_hashes={str(path): saved.digest(path) for path in [BRANCH / "RESUME-CURRENT.md", BRANCH.parent / "CURRENT_LOCAL_RESUME.md"]}))
    write(ROOT / "authenticated-inputs.json", paths)
    write(ROOT / "progress.json", dict(state="predictions_frozen"))
    print(json.dumps(dict(state="predictions_frozen", domain=endpoints, inputs=len(paths), candidate_sha256=checksum)), flush=True)


def frozen_candidate():
    config = read(ROOT / "configuration.json")
    path = ROOT / "results/frozen-candidate.npz"
    assert saved.digest(path) == config["candidate_sha256"]
    return packet(path)


def whiten(matrix, factor):
    left = linear.solve_triangular(factor, matrix, lower=True)
    return linear.solve_triangular(factor, left.T, lower=True).T


def structure():
    assert read(ROOT / "progress.json")["state"] == "predictions_frozen"
    frozen = frozen_candidate()
    config = read(ROOT / "configuration.json")
    ladder, basis, theta = old.setup()
    lower, upper = config["domain"]
    controls = [candidate(lower, frozen),
                candidate(lower, frozen) + .5 * (upper - lower) * (frozen["tangent"] + lower * frozen["curvature"]),
                candidate(upper, frozen)]
    factor = linear.cholesky(basis.mass, lower=True)
    null = factor.T @ basis.chemical
    orthogonal = linear.null_space(null[None, :])
    rows, spectra = [], []
    for index, matrix in enumerate(controls):
        scale = float(np.linalg.norm(matrix))
        check(rows, f"Bernstein{index}: symmetry", np.linalg.norm(matrix - matrix.T) / scale)
        check(rows, f"Bernstein{index}: number null", np.linalg.norm(matrix @ basis.chemical) / (scale * np.linalg.norm(basis.chemical)))
        transformed = whiten(matrix, factor)
        reduced = orthogonal.T @ transformed @ orthogonal
        eigenvalues = linear.eigvalsh(reduced)
        relative_positive = max(0., float(eigenvalues[-1])) / max(abs(float(eigenvalues[0])), abs(float(eigenvalues[-1])))
        check(rows, f"Bernstein{index}: nonpositive non-null spectrum", relative_positive)
        spectra.append(dict(control=index, smallest=float(eigenvalues[0]), largest=float(eigenvalues[-1]), relative_positive=relative_positive))
    capacity_rows = []
    dual = linear.solve(basis.mass, basis.energy, assume_a="pos")
    for model in MODELS:
        operator = corner.Operators(model, ladder)
        for filename in operator.inputs:
            assert read(ROOT / "authenticated-inputs.json")[str(filename)] == saved.digest(filename)
        history = corner.history(model, "quarter")
        coordinates = np.unique(np.concatenate([history["expansion"], history["coordinates"],
                                               .5 * (history["expansion"][:-1] + history["expansion"][1:])]))
        capacities = []
        for coordinate in coordinates:
            local = operator.background.at(float(coordinate))
            offset = float(np.log(local["thermal_parameter"] / theta))
            check(rows, f"{model}:{coordinate}: log-temperature coordinate", offset + float(coordinate) - operator.anchor)
            assert lower - 1e-14 <= offset <= upper + 1e-14
            damping = operator.emission.at(local["thermal_parameter"], "dcbr")
            rate = local["coefficient"] / local["thermal_parameter"]
            for kind, block in [("bank", ladder.at(local["thermal_parameter"], 0)), ("candidate", candidate(offset, frozen))]:
                capacity = operator.background.chi - dual @ (rate * (block - damping)) @ basis.temperature
                capacities.append((kind, float(capacity)))
        for kind in KINDS:
            minimum = min(value for label, value in capacities if label == kind)
            check(rows, model + ":" + kind + ": positive sampled gas capacity", 0 if minimum > 0 else 1)
            capacity_rows.append(dict(model=model, kind=kind, sampled_points=len(coordinates), minimum=minimum))
    failed = [row for row in rows if not row["passed"]]
    write(ROOT / "results/structure.json", dict(checks=rows, failed_checks=failed, spectra=spectra, capacities=capacity_rows,
          bernstein_scope="Quadratic Bernstein convex-hull proof with numerical eigenvalue checks of three controls; no interval-rounded spectral certificate",
          capacity_scope="Saved quarter nodes, midpoints and probes only", no_eigenvalue_clipping=True))
    write(ROOT / "progress.json", dict(state="structure_passed" if not failed else "structure_failed"))
    print(json.dumps(dict(state=read(ROOT / "progress.json")["state"], failed=failed, spectra=spectra, capacities=capacity_rows)), flush=True)


def edge(index):
    assert read(ROOT / "progress.json")["state"] in ["structure_passed", "edges_running"]
    frozen = frozen_candidate()
    config = read(ROOT / "configuration.json")
    offset = config["domain"][index]
    directory = ROOT / "edges" / str(index)
    assert not directory.exists()
    ladder, basis, theta0 = old.setup()
    theta = theta0 * np.exp(offset)
    anchor_masks = packet(old.ROOT / "results/frozen-tangent.npz")["masks"]
    events = old.geometry_module.event_geometry(theta, 6)
    began = time.monotonic()
    block, discarded = old.ladder_module.scalar_physical_block(basis, theta, events)
    boundary = np.zeros_like(block)
    crossings = 0
    for node, initial in enumerate(basis.values):
        ratio, extra, final, conductance = old.physical_pairs(basis, theta, events, node)
        inside = (final >= basis.minimum) & (final <= basis.maximum)
        changed = inside != anchor_masks[node]
        if not np.any(changed):
            continue
        difference = initial[None, :] - basis.evaluate(final[changed])
        sign = inside[changed].astype(int) - anchor_masks[node, changed].astype(int)
        boundary -= .5 * (difference.T * (conductance[changed] * sign)) @ difference
        crossings += int(changed.sum())
    rows, comparisons = [], []
    with mp.workdps(80):
        anchor = corner.mp_matrix(frozen["block"])
        tangent = corner.mp_matrix(frozen["tangent"])
        quadratic = mp.mpf(offset) ** 2 * corner.mp_matrix(frozen["curvature"]) / 2
        live = corner.mp_matrix(block)
        fixed = live - corner.mp_matrix(boundary)
        def matrix_norm(matrix):
            return mp.sqrt(mp.fsum(value * value for value in matrix))
        for kind, actual in [("live", live), ("fixed", fixed)]:
            change = actual - anchor
            remainder = change - mp.mpf(offset) * tangent
            error = float(matrix_norm(quadratic - remainder) / matrix_norm(remainder))
            small_error = float(matrix_norm(mp.mpf(offset) * tangent + quadratic - change) / matrix_norm(change))
            check(rows, kind + ": edge second-order remainder", error, .01, "prediction")
            check(rows, kind + ": edge small change", small_error, .01, "prediction")
            comparisons.append(dict(kind=kind, remainder_relative=error, small_change_relative=small_error))
    directory.mkdir(parents=True)
    path = directory / "matrices.npz"
    np.savez_compressed(path, block=block, boundary=boundary, offset=offset, theta=theta)
    failed = [row for row in rows if not row["passed"]]
    write(directory / "status.json", dict(state="complete", checks=rows, failed_checks=failed,
          comparisons=comparisons, matrix_sha256=saved.digest(path), frozen_candidate_sha256=config["candidate_sha256"],
          offset=offset, theta=theta, crossings=crossings, discarded_weight_fraction=discarded,
          elapsed_seconds=time.monotonic() - began, no_new_source_integrals=True))
    write(ROOT / "progress.json", dict(state="edges_running", last_edge=index))
    print(json.dumps(dict(edge=index, offset=offset, comparisons=comparisons, failed=failed)), flush=True)


def evolve(model, grid):
    config = read(ROOT / "configuration.json")
    frozen = frozen_candidate()
    for index in range(2):
        status = read(ROOT / "edges" / str(index) / "status.json")
        assert not status["failed_checks"]
        assert status["frozen_candidate_sha256"] == config["candidate_sha256"]
        assert saved.digest(ROOT / "edges" / str(index) / "matrices.npz") == status["matrix_sha256"]
    assert not read(ROOT / "results/structure.json")["failed_checks"]
    directory = ROOT / "histories" / model / grid
    assert not directory.exists()
    ladder, basis, theta0 = old.setup()
    operator = corner.Operators(model, ladder)
    history = corner.history(model, grid)
    original = packet(corner.ENERGY / "results" / model / "state.npz")
    divisor = dict(native=1, half=2, quarter=4)[grid]
    step, heat = float(history["step"]), float(history["heat"])
    start = int(history["start_index"])
    assert np.array_equal(history["initial_profile"], original["profiles"][start])
    assert np.array_equal(history["initial_previous_profile"], original["profiles"][start - 1])
    profile, older_profile = history["initial_profile"].copy(), history["initial_previous_profile"].copy()
    gas, older_gas = float(history["initial_gas"]), float(history["initial_previous_gas"])
    work, older_work = float(original["expansion_work"][start]), float(original["expansion_work"][start - 1])
    difference, older_difference = np.zeros(96), np.zeros(96)
    gas_difference, older_gas_difference = 0., 0.
    work_difference, older_work_difference = 0., 0.
    profiles, gases, works = [profile.copy()], [gas], [work]
    differences, gas_differences, work_differences = [difference.copy()], [0.], [0.]
    diagnostics, denominators = [], []
    began = time.monotonic()
    for ordinal, coordinate in enumerate(history["expansion"][1:], 1):
        local = operator.background.at(float(coordinate))
        offset = float(np.log(local["thermal_parameter"] / theta0))
        assert config["domain"][0] - 1e-14 <= offset <= config["domain"][1] + 1e-14
        rate = local["coefficient"] / local["thermal_parameter"]
        damping = operator.emission.at(local["thermal_parameter"], "dcbr")
        stiffness = rate * (candidate(offset, frozen) - damping)
        original_stiffness = rate * (ladder.at(local["thermal_parameter"], 0) - damping)
        alpha, vector = corner.bdf_terms(profile, older_profile, step, ordinal, divisor)
        _, scalar = corner.bdf_terms(gas, older_gas, step, ordinal, divisor)
        _, past_work = corner.bdf_terms(work, older_work, step, ordinal, divisor)
        _, delta_vector = corner.bdf_terms(difference, older_difference, step, ordinal, divisor)
        _, delta_scalar = corner.bdf_terms(gas_difference, older_gas_difference, step, ordinal, divisor)
        _, delta_work = corner.bdf_terms(work_difference, older_work_difference, step, ordinal, divisor)
        bank_departure = history["profiles"][ordinal] - basis.temperature * history["temperature_scaled"][ordinal]
        forcing = (original_stiffness - stiffness) @ bank_departure
        solution = linear.solve(alpha * basis.mass - stiffness,
                                np.column_stack([basis.mass @ vector, -stiffness @ basis.temperature,
                                                 basis.mass @ delta_vector + forcing]), assume_a="pos")
        free, response, free_difference = solution[:, 0], solution[:, 1], solution[:, 2]
        denominator = heat * (alpha + 1) + alpha * (basis.energy @ response)
        assert np.isfinite(denominator) and denominator > 0
        new_gas = (heat * scalar - 1 - basis.energy @ (alpha * free - vector)) / denominator
        new_gas_difference = (heat * delta_scalar - basis.energy @ (alpha * free_difference - delta_vector)) / denominator
        new_profile = free + response * new_gas
        new_difference = free_difference + response * new_gas_difference
        new_work = (past_work + 1 + heat * new_gas) / alpha
        new_work_difference = (delta_work + heat * new_gas_difference) / alpha
        rhs = stiffness @ (new_profile - basis.temperature * new_gas)
        residual = alpha * basis.mass @ new_profile - basis.mass @ vector - rhs
        difference_rhs = stiffness @ (new_difference - basis.temperature * new_gas_difference) + forcing
        difference_residual = alpha * basis.mass @ new_difference - basis.mass @ delta_vector - difference_rhs
        difference_scale = max(np.linalg.norm(difference_rhs), np.linalg.norm(forcing), 1e-300)
        diagnostics.append(dict(u=float(coordinate), kinetic_relative=float(np.linalg.norm(residual) / np.linalg.norm(rhs)),
            gas_energy_balance=float(basis.energy @ (alpha * new_profile - vector) + heat * ((alpha + 1) * new_gas - scalar) + 1),
            work_balance=float(alpha * new_work - past_work - 1 - heat * new_gas),
            difference_equation_relative=float(np.linalg.norm(difference_residual) / difference_scale),
            difference_gas_balance=float(basis.energy @ (alpha * new_difference - delta_vector) + heat * ((alpha + 1) * new_gas_difference - delta_scalar)),
            difference_work_balance=float(alpha * new_work_difference - delta_work - heat * new_gas_difference),
            reconstruction_profile_relative=float(np.linalg.norm(new_profile + new_difference - history["profiles"][ordinal]) / np.linalg.norm(history["profiles"][ordinal])),
            reconstruction_gas_absolute=float(abs(new_gas + new_gas_difference - history["temperature_scaled"][ordinal])),
            reconstruction_work_absolute=float(abs(new_work + new_work_difference - history["expansion_work"][ordinal]))))
        denominators.append(float(denominator))
        older_profile, profile = profile, new_profile
        older_gas, gas = gas, float(new_gas)
        older_work, work = work, float(new_work)
        older_difference, difference = difference, new_difference
        older_gas_difference, gas_difference = gas_difference, float(new_gas_difference)
        older_work_difference, work_difference = work_difference, float(new_work_difference)
        profiles.append(profile.copy())
        gases.append(gas)
        works.append(work)
        differences.append(difference.copy())
        gas_differences.append(gas_difference)
        work_differences.append(work_difference)
    profiles, gases, works = np.array(profiles), np.array(gases), np.array(works)
    differences, gas_differences, work_differences = np.array(differences), np.array(gas_differences), np.array(work_differences)
    rows = []
    for key in diagnostics[0]:
        if key != "u":
            check(rows, model + "/" + grid + ": " + key, max(abs(row[key]) for row in diagnostics))
    check(rows, model + "/" + grid + ": integrated candidate energy", max(abs(profiles @ basis.energy + heat * gases + works)))
    check(rows, model + "/" + grid + ": integrated difference energy", max(abs(differences @ basis.energy + heat * gas_differences + work_differences)))
    directory.mkdir(parents=True)
    path = directory / "history.npz"
    np.savez_compressed(path, expansion=history["expansion"], coordinates=history["coordinates"],
                        candidate_profiles=profiles, candidate_gas=gases, candidate_work=works,
                        bank_minus_candidate_profiles=differences, bank_minus_candidate_gas=gas_differences,
                        bank_minus_candidate_work=work_differences, step=step, heat=heat,
                        initial_profile=history["initial_profile"], initial_previous_profile=history["initial_previous_profile"],
                        initial_gas=history["initial_gas"], initial_previous_gas=history["initial_previous_gas"])
    failed = [row for row in rows if not row["passed"]]
    write(directory / "status.json", dict(state="complete", checks=rows, failed_checks=failed, diagnostics=diagnostics,
          history_sha256=saved.digest(path), frozen_candidate_sha256=config["candidate_sha256"], updates=len(diagnostics),
          coupled_solves=len(diagnostics), right_hand_sides=3, denominator_minimum=min(denominators),
          elapsed_seconds=time.monotonic() - began))
    write(ROOT / "progress.json", dict(state="evolution_running", last_model=model, last_grid=grid))
    print(json.dumps(dict(model=model, grid=grid, updates=len(diagnostics), failed=failed,
                         reconstruction=max(row["reconstruction_gas_absolute"] for row in diagnostics),
                         elapsed_seconds=time.monotonic() - began)), flush=True)


if __name__ == "__main__":
    source.modest()
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=["prepare", "structure", "edge", "evolve"])
    parser.add_argument("--index", type=int, choices=[0, 1])
    parser.add_argument("--model", choices=MODELS)
    parser.add_argument("--grid", choices=GRIDS)
    arguments = parser.parse_args()
    if arguments.phase == "edge":
        edge(arguments.index)
    elif arguments.phase == "evolve":
        evolve(arguments.model, arguments.grid)
    else:
        dict(prepare=prepare, structure=structure)[arguments.phase]()

