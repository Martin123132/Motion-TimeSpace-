from __future__ import annotations

import csv
import cmath
import hashlib
import importlib.util
import json
import math
import os
import time
from pathlib import Path
from typing import Any

import numpy as np


POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
SCRIPT_5077 = POST / "scripts" / "Y5_R2FR_5077_central_anchor_pilot_runner.py"
RUN = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5079"
    / "runs"
    / "bounded_central_anchor_pilot_v8"
)
SOURCE = POST / "source-intake" / "functional_rg" / "5094"
RESULT_JSON = SOURCE / "E040_S507615_A14_adaptive_leaf_localization.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5094_VALIDATION.csv"
)
MARKER = "MTS_5094_E040_S507615_A14_ADAPTIVE_LEAF_LOCALIZATION"
REVISION = "depth14-leaf-localization-and-extra-depth-probe-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
EVENT_ID = "S507615_N0000"
ARGUMENT_ID = "E040_A14"
JOB_KEY = "E040__S507615_N0000__A14__coarse12"
DIAGNOSTIC_INTERVAL_CAP = 256
PRODUCTION_DEPTH_CAP = 14
EXTRA_DEPTH_CAP = 22


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(item.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(item).encode("ascii"))
    return value.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def complex_row(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def serialized_catalog_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "root": str(row["root"]),
        "pairs": [list(pair) for pair in row["pairs"]],
        "log_point": str(row["log_point"]),
        "log_distance": float(row["log_distance"]),
        "segment_projection": float(row["segment_projection"]),
        "near_path": bool(row["near_path"]),
        "numerically_zero": bool(row["numerically_zero"]),
        "stable": bool(row["stable"]),
        "included_as_pole_model": bool(row["included_as_pole_model"]),
        "residue": str(row["residue"]),
    }


def diagnose_chamber(
    module_5077: Any,
    module: Any,
    ownership: dict[str, bool],
    start: complex,
    end: complex,
    catalog: list[dict[str, Any]],
    profile: dict[str, Any],
) -> dict[str, Any]:
    high_order = int(profile["relative_orders"][-1])
    global_nodes = int(profile["global_nodes"])
    global_residue_nodes = int(profile["global_residue_nodes"])
    relative_tolerance = float(profile["relative_adaptive_tolerance"])
    models = [row for row in catalog if row["included_as_pole_model"]]
    breakpoints = module.collision_scaled_breakpoints(start, end, catalog)
    difference = end - start
    low_order = max(6, high_order // 2)
    low_nodes, low_weights = module.M5028.gauss_rule(low_order)
    high_nodes, high_weights = module.M5028.gauss_rule(high_order)
    evaluation_count = 0

    def regularized_value(parameter: float) -> complex:
        nonlocal evaluation_count
        log_point = start + parameter * difference
        value = module.global_chamber_value(
            cmath.exp(log_point),
            ownership,
            global_nodes,
            global_residue_nodes,
        )
        for model in models:
            value -= model["residue"] / (log_point - model["log_point"])
        evaluation_count += 1
        return value

    def rule(
        lower: float,
        upper: float,
        nodes: np.ndarray,
        weights: np.ndarray,
    ) -> complex:
        local = 0.0j
        for node, weight in zip(nodes, weights):
            parameter = lower + (upper - lower) * float(node)
            local += float(weight) * regularized_value(parameter)
        return difference * (upper - lower) * local / (2.0j * math.pi)

    def segment(lower: float, upper: float, depth: int) -> dict[str, Any]:
        low = rule(lower, upper, low_nodes, low_weights)
        high = rule(lower, upper, high_nodes, high_weights)
        return {
            "lower": lower,
            "upper": upper,
            "depth": depth,
            "low_value": low,
            "value": high,
            "error": abs(high - low),
        }

    segments = [
        segment(lower, upper, 0)
        for lower, upper in zip(breakpoints[:-1], breakpoints[1:])
    ]
    model_contribution = sum(
        (
            model["residue"]
            * module.continuous_straight_log_difference(
                start, end, model["log_point"]
            )
            / (2.0j * math.pi)
        )
        for model in models
    )

    def totals() -> tuple[complex, float, float]:
        value = sum((row["value"] for row in segments), 0.0j)
        error = sum(float(row["error"]) for row in segments)
        target = 1.0e-9 + relative_tolerance * max(
            abs(value + model_contribution), 1.0
        )
        return value, error, target

    value, error, target = totals()
    split_count = 0
    while error > target and len(segments) < DIAGNOSTIC_INTERVAL_CAP:
        candidates = [row for row in segments if row["depth"] < PRODUCTION_DEPTH_CAP]
        if not candidates:
            break
        parent = max(candidates, key=lambda row: row["error"])
        midpoint = 0.5 * (parent["lower"] + parent["upper"])
        segments.remove(parent)
        segments.extend(
            (
                segment(parent["lower"], midpoint, parent["depth"] + 1),
                segment(midpoint, parent["upper"], parent["depth"] + 1),
            )
        )
        split_count += 1
        value, error, target = totals()

    def leaf_row(row: dict[str, Any]) -> dict[str, Any]:
        midpoint = 0.5 * (row["lower"] + row["upper"])
        log_point = start + midpoint * difference
        root = cmath.exp(log_point)
        nearest = min(catalog, key=lambda candidate: abs(log_point - candidate["log_point"]))
        return {
            "lower": float(row["lower"]),
            "upper": float(row["upper"]),
            "width": float(row["upper"] - row["lower"]),
            "depth": int(row["depth"]),
            "value": complex_row(row["value"]),
            "low_value": complex_row(row["low_value"]),
            "absolute_error": float(row["error"]),
            "error_fraction": float(row["error"] / max(error, 1.0e-300)),
            "midpoint_parameter": float(midpoint),
            "midpoint_log_point": str(log_point),
            "midpoint_root": str(root),
            "nearest_catalog_log_distance": float(
                abs(log_point - nearest["log_point"])
            ),
            "nearest_catalog_row": serialized_catalog_row(nearest),
        }

    ranked = sorted(segments, key=lambda row: row["error"], reverse=True)
    locked = [row for row in ranked if row["depth"] >= PRODUCTION_DEPTH_CAP]
    probe_rows: list[dict[str, Any]] = []
    if locked:
        probe_segments = [locked[0]]
        for requested_depth in range(PRODUCTION_DEPTH_CAP, EXTRA_DEPTH_CAP + 1):
            probe_value = sum((row["value"] for row in probe_segments), 0.0j)
            probe_error = sum(float(row["error"]) for row in probe_segments)
            probe_rows.append(
                {
                    "depth": requested_depth,
                    "leaf_count": len(probe_segments),
                    "value": complex_row(probe_value),
                    "absolute_error": probe_error,
                }
            )
            if requested_depth == EXTRA_DEPTH_CAP:
                break
            parent = max(probe_segments, key=lambda row: row["error"])
            midpoint = 0.5 * (parent["lower"] + parent["upper"])
            probe_segments.remove(parent)
            probe_segments.extend(
                (
                    segment(parent["lower"], midpoint, parent["depth"] + 1),
                    segment(midpoint, parent["upper"], parent["depth"] + 1),
                )
            )

    result = value + model_contribution
    locked_error = sum(float(row["error"]) for row in locked)
    return {
        "start_log": str(start),
        "end_log": str(end),
        "difference": str(difference),
        "initial_breakpoints": breakpoints,
        "initial_interval_count": len(breakpoints) - 1,
        "final_interval_count": len(segments),
        "split_count": split_count,
        "evaluation_count": evaluation_count,
        "model_count": len(models),
        "integral_value": complex_row(result),
        "absolute_error_sum": float(error),
        "target_absolute_error": float(target),
        "relative_error": float(error / max(abs(result), 1.0)),
        "converged": bool(error <= target),
        "maximum_depth": max(int(row["depth"]) for row in segments),
        "locked_leaf_count": len(locked),
        "locked_absolute_error_sum": locked_error,
        "locked_error_fraction": float(locked_error / max(error, 1.0e-300)),
        "top_error_leaves": [leaf_row(row) for row in ranked[:12]],
        "locked_leaf_extra_depth_probe": probe_rows,
        "catalog": [serialized_catalog_row(row) for row in catalog],
    }


def main() -> None:
    topology_path = RUN / "topologies" / f"{EVENT_ID}__{ARGUMENT_ID}.json"
    required = [SCRIPT_5077, RUN / "config.json", topology_path, FORMAL]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing 5094 inputs: {missing}")
    module_5077 = load_module("mts_5077_for_5094", SCRIPT_5077)
    module_5077.removable_extension_gate()
    config = json.loads((RUN / "config.json").read_text(encoding="utf-8"))
    event = module_5077.M5036.event_lookup(config)[EVENT_ID]
    argument = module_5077.M5036.argument_lookup(config)[ARGUMENT_ID]
    target = module_5077.M5036.complex_from_row(argument["target_cosine"])
    module_5077.M5043.M5034.configure(event, target)
    module = module_5077.M5043.N5030
    topology = json.loads(topology_path.read_text(encoding="utf-8"))
    profile = module_5077.M5043.PROFILES["coarse12"]
    _, ownerships = module.physical_chambers()
    previous_catalog = module.chamber_residue_catalog
    previous_global = module.global_chamber_value
    removable = module_5077.M5085.CertifiedRemovableGlobalExtension(previous_global)
    module.chamber_residue_catalog = module_5077.restricted_coarse_catalog
    module.global_chamber_value = removable
    module_5077.M5043.CURRENT_JOB = f"5094::{JOB_KEY}"
    module_5077.M5043.THEOREM_AUDIT.clear()
    module_5077.M5043.CHART_AUDIT.clear()
    module_5077.M5043.NUMERIC_AUDIT.clear()
    module_5077.LOCAL_ZERO_AUDIT.clear()
    module_5077.OUTWARD_CONTOUR_AUDIT.clear()
    chamber_rows: list[dict[str, Any]] = []
    started = time.monotonic()
    try:
        for chamber_index, ownership in enumerate(ownerships):
            topology_chamber = topology["chambers"][chamber_index]
            start = complex(topology_chamber["target_start_log"])
            end = complex(topology_chamber["target_end_log"])
            required_roots = [
                complex(row["target_root"])
                for row in topology_chamber["surface_crossings"]
            ]
            catalog, stable = module_5077.restricted_coarse_catalog(
                ownership,
                start,
                end,
                required_roots,
                int(profile["global_nodes"]),
                int(profile["global_residue_nodes"]),
                int(profile["relative_residue_nodes"]),
                float(profile["model_distance"]),
            )
            row = diagnose_chamber(
                module_5077,
                module,
                ownership,
                start,
                end,
                catalog,
                profile,
            )
            row["chamber_index"] = chamber_index
            row["residues_stable"] = bool(stable)
            chamber_rows.append(row)
    finally:
        module.chamber_residue_catalog = previous_catalog
        module.global_chamber_value = previous_global
    elapsed = time.monotonic() - started
    formal_digest = tree_digest(FORMAL)
    locked_rows = [row for row in chamber_rows if row["locked_leaf_count"] > 0]
    extra_depth_decay_rows = []
    for row in locked_rows:
        probe = row["locked_leaf_extra_depth_probe"]
        if len(probe) >= 2:
            extra_depth_decay_rows.append(
                {
                    "chamber_index": row["chamber_index"],
                    "initial_error": probe[0]["absolute_error"],
                    "final_error": probe[-1]["absolute_error"],
                    "decay_ratio": probe[-1]["absolute_error"]
                    / max(probe[0]["absolute_error"], 1.0e-300),
                }
            )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "job_key": JOB_KEY,
        "diagnostic_interval_cap": DIAGNOSTIC_INTERVAL_CAP,
        "production_depth_cap": PRODUCTION_DEPTH_CAP,
        "extra_depth_cap": EXTRA_DEPTH_CAP,
        "adaptive_tolerance": float(profile["relative_adaptive_tolerance"]),
        "runtime_seconds": elapsed,
        "chambers": chamber_rows,
        "depth_locked_chamber_count": len(locked_rows),
        "extra_depth_decay_rows": extra_depth_decay_rows,
        "numerical_removable_extension_call_count": len(removable.calls),
        "formalization_workbench_tree_sha256": formal_digest,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    checks = [
        ("source_paths_exist", not missing, "all 5094 inputs exist"),
        ("two_chambers_diagnosed", len(chamber_rows) == 2, str(len(chamber_rows))),
        (
            "residues_stable",
            all(row["residues_stable"] for row in chamber_rows),
            str([row["residues_stable"] for row in chamber_rows]),
        ),
        (
            "diagnostic_reaches_depth_cap",
            bool(locked_rows),
            str([(row["chamber_index"], row["locked_leaf_count"]) for row in locked_rows]),
        ),
        (
            "extra_depth_probe_recorded",
            all(len(row["locked_leaf_extra_depth_probe"]) == 9 for row in locked_rows),
            str([len(row["locked_leaf_extra_depth_probe"]) for row in locked_rows]),
        ),
        (
            "no_collision_fallback",
            len(removable.calls) == 0,
            str(len(removable.calls)),
        ),
        ("formalization_unchanged", formal_digest == FORMAL_BASELINE, formal_digest),
        (
            "claim_discipline",
            not result["valid_for_full_MTS_claim"],
            "localization diagnostic is not physical evidence",
        ),
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("check_id", "passed", "detail", "checkpoint_marker"),
        )
        writer.writeheader()
        for index, (name, passed, detail) in enumerate(checks, start=1):
            writer.writerow(
                {
                    "check_id": f"V5094_{index:02d}_{name}",
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        raise RuntimeError(f"checkpoint 5094 validation failed: {failed}")


if __name__ == "__main__":
    main()
