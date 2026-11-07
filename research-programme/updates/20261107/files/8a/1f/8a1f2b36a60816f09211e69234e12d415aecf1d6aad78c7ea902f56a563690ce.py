from __future__ import annotations

import hashlib
import json
from pathlib import Path

import mpmath as mp
import numpy as np

from nodal_readout import coefficient_difference, make_bundle
from adjoint_readout import AdjointNodalFeatures as NodalFeatures


SCIENCE_HASH = "508063733ce6897fc455c4e2f0419614b557abb46f84d1b88a8b45540a2537e1"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_verified_cell(root, cell, verification_path):
    root = Path(root).resolve()
    run = root / "execution-v3"
    inputs = {}

    def register(path, expected=None):
        path = Path(path).resolve()
        checksum = digest(path)
        require(expected is None or checksum == expected, f"Source hash mismatch: {path}")
        inputs[str(path)] = checksum
        return path

    science = read(register(run / "science-config.json", SCIENCE_HASH))
    verification = read(register(verification_path))
    require(verification["passed"] is True, "Independent verification did not pass")
    require(verification["through_coarse_node"] == cell + 1, "Verification endpoint differs")
    require(verification["full_chain_verified_from_cell"] == 1, "Full preceding chain not verified")
    require(verification["source_config_sha256"] == SCIENCE_HASH, "Verification science differs")
    register(root / "supervisor_history_check.py", verification["script_sha256"])
    pair = read(register(run / "paired" / f"cell-{cell:04d}.json", verification["final_paired_sha256"]))
    require(pair["state"] == "paired_passed" and pair["cell"] == cell, "Uncommitted paired endpoint")
    require(all(row["passed"] is True for row in pair["checks"]) and len(pair["checks"]) == 48, "Paired gates not satisfied")
    register(run / "paired" / f"cell-{cell:04d}.npz", pair["packet_sha256"])
    with np.load(register(science["execution_grids"], science["execution_grids_sha256"]), allow_pickle=False) as packet:
        frequency, coarse = packet["frequency"].copy(), packet["coarse"].copy()
    coordinate = float(coarse[cell + 1])
    require(coordinate == verification["coordinate"], "Verification coordinate differs")
    states = {}
    require(set(pair["case_heads"]) == {case["id"] for case in science["cases"]}, "Case coverage differs")
    for case in science["cases"]:
        identifier = case["id"]
        metadata_path = run / "checkpoints" / identifier / f"cell-{cell:04d}.json"
        metadata = read(register(metadata_path, pair["case_heads"][identifier]))
        row_index = (cell + 1) * case["subdivision"]
        require(metadata["state"] == "committed" and metadata["case"] == identifier, "Case not committed")
        require(metadata["coordinate"] == coordinate and metadata["history_row_index"] == row_index, "Case time differs")
        with np.load(register(metadata_path.with_suffix(".npz"), metadata["packet_sha256"]), allow_pickle=False) as packet:
            profile, tail = packet["profile"].copy(), packet["endpoint_tail"].copy()
            gas, work = float(packet["gas"]), float(packet["work"])
            require(np.array_equal(tail, packet["tail"][-1]), "Total endpoint tail not retained")
            require(float(packet["times"][-1]) == coordinate, "Tail time differs")
        require(profile.shape == (case["photon_dimension"],) and tail.shape == (case["tail_dimension"],), "State dimensions differ")
        require(tail.size == frequency.size, "Tail grid differs")
        values = np.r_[profile, tail, gas]
        require(np.isfinite(values).all() and np.isfinite(work), "Nonfinite saved history")
        with np.load(register(case["driver_history"], case["driver_history_sha256"]), allow_pickle=False) as driver:
            require(float(driver["coordinates"][row_index]) == coordinate, "Driver time differs")
            require(np.array_equal(profile, driver["profiles"][row_index]), "Driver profile differs")
            require(gas == float(driver["gas"][row_index]) and work == float(driver["work"][row_index]), "Gas/work differs")
        with mp.workdps(80):
            coefficients = [mp.mpf(float(value)) for value in values]
        states[identifier] = dict(coefficients=coefficients, profile=profile, tail=tail, gas=gas,
            work=work, model=case["model"], kind=case["kind"], subdivision=case["subdivision"])
    require(all(digest(path) == checksum for path, checksum in inputs.items()), "Input changed during read")
    return dict(coordinate=coordinate, frequency=frequency, states=states, inputs=inputs, cell=cell)


def at_epoch(retained_bundle_class, original, restart, identifiers, differences=None, *, convention):
    require(len(original.epochs) == 1, "Supply one source-owned epoch")
    require(float(original.epochs[0].coordinate) == restart["coordinate"], "Do not substitute a different source temperature/time")
    require(convention in ("normalized-history", "physical-background"), "Name the history normalization explicitly")
    require(differences is None or len(differences) == len(identifiers), "Comparison case coverage differs")
    with mp.workdps(80):
        scale = mp.mpf(1)
        if convention == "physical-background":
            require(hasattr(original.epochs[0], "heat"), "Missing source-owned epoch heat normalization")
            source_heat = original.epochs[0].heat
            scale = mp.mpf(float(source_heat)) if isinstance(source_heat, (float, np.floating)) else mp.mpf(source_heat)
            require(mp.isfinite(scale) and scale > 0, "Invalid source-owned epoch heat normalization")
    features = NodalFeatures(original, restart["frequency"])
    columns = []
    for position, identifier in enumerate(identifiers):
        state = restart["states"][identifier]
        values = state["coefficients"]
        if differences is not None:
            reference = restart["states"][differences[position]]
            require(reference["model"] == state["model"], "Do not subtract different heavy/cold models")
            values = coefficient_difference(reference["coefficients"], values)
        with mp.workdps(80):
            values = [scale * value for value in values]
        columns.extend([values, values])
    inputs = list(dict.fromkeys([*map(str, original.inputs), *restart["inputs"]]))
    bundle = make_bundle(retained_bundle_class, features, columns, inputs)
    bundle.coordinate_convention = convention
    bundle.history_scale = scale
    return bundle
