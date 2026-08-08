from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import os
import time
from pathlib import Path
from typing import Any

import numpy as np
from scipy.interpolate import Akima1DInterpolator, PchipInterpolator


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
SOURCE_5241 = FUNCTIONAL_RG / "5241"
SOURCE_5252 = FUNCTIONAL_RG / "5252"
SOURCE_5253 = FUNCTIONAL_RG / "5253"
SOURCE_5254 = FUNCTIONAL_RG / "5254"
SOURCE_5255 = FUNCTIONAL_RG / "5255"
SOURCE_5256 = FUNCTIONAL_RG / "5256"
SOURCE_5264 = FUNCTIONAL_RG / "5264"
SOURCE = FUNCTIONAL_RG / "5265"
NODES = SOURCE / "nodes"
SCRIPT_5265 = Path(__file__).resolve()

SCRIPT_5264 = (
    SCRIPTS
    / "Y5_R2FR_5264_occupation_separated_laurent_residue_and_boundary_completion.py"
)
RESULT_5264 = (
    SOURCE_5264 / "occupation_separated_completion_result.json"
)
BRACKETS_5264 = (
    SOURCE_5264 / "final_topology_transition_brackets.csv"
)
NODES_5264 = SOURCE_5264 / "targeted_boundary_nodes.csv"
FORMAL_INVENTORY = (
    SOURCE_5252 / "formalization_workbench_start_inventory.csv"
)

MANIFEST = SOURCE / "piecewise_outer_manifest.json"
TARGETS = SOURCE / "piecewise_outer_target_nodes.csv"
FIXED_VALUES = SOURCE / "piecewise_outer_fixed_values.json"
DRY_RUN = SOURCE / "piecewise_outer_dry_run.json"
STATUS = SOURCE / "status.json"
NODE_ROWS = SOURCE / "piecewise_outer_node_results.csv"
SMOOTH_RULES = SOURCE / "smooth_interval_two_panel_rules.csv"
TRANSITION_RULES = SOURCE / "transition_chamber_interpolation_rules.csv"
COEFFICIENT_ROWS = SOURCE / "piecewise_outer_coefficient.csv"
VALIDATION = SOURCE / "piecewise_outer_validation.csv"
FORMAL_DIFF = SOURCE / "formalization_workbench_run_diff.csv"
RESULT = SOURCE / "piecewise_outer_result.json"
DOC = POST / "5265-Y5-R2FR-piecewise-outer-coefficient-reassembly.md"

CHECKPOINT = 5265
PARENT_CHECKPOINT = 5264
MARKER = "MTS_5265_PIECEWISE_OUTER_COEFFICIENT_REASSEMBLY"
REVISION = "piecewise-outer-coefficient-reassembly-v2"
ENGINE_GENERATION = 11
INNER_ORDERS = (128, 512)
QUADRATURE_ORDERS = (96, 128, 512)
OUTER_RELATIVE_ERROR_LIMIT = 0.2
INNER_RELATIVE_ERROR_LIMIT = 1.0e-3
ANGULAR_JACOBIAN = 0.25
GENERATION_COMPARISON_LEVEL = 8

SMOOTH_INTERVALS = {
    "I00": ("Q00", "M00", "Q01"),
    "I02": ("Q02", "M02", "Q03"),
    "I03": ("Q03", "M03", "Q04"),
    "I04": ("Q04", "M04", "Q05"),
    "I05": ("Q05", "M05", "Q06"),
    "I07": ("Q07", "M07", "Q08"),
}
TRANSITION_INTERVALS = {
    "I01": ("Q01", "Q02", ("I01_T00", "I01_T01")),
    "I06": ("Q06", "Q07", ("I06_T00", "I06_T01")),
}


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5264 = load_module("mts_5264_for_5265", SCRIPT_5264)
M5261 = M5264.M5261
M5251 = M5264.M5251
M5239 = M5264.M5239
M5238 = M5239.M5238
M5237 = M5239.M5237
M5231 = M5239.M5231


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def serialized_hash(value: Any) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    os.replace(temporary, path)


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes"}


def source_files() -> tuple[Path, ...]:
    return (
        SCRIPT_5265,
        SCRIPT_5264,
        RESULT_5264,
        BRACKETS_5264,
        NODES_5264,
        FORMAL_INVENTORY,
        SOURCE_5252 / "full_order9_node_summary.csv",
        SOURCE_5253 / "outer_interval_midpoint_nodes.csv",
        SOURCE_5254 / "dominant_quarterpoint_nodes.csv",
        SOURCE_5255 / "boundary_bisection_generation1_nodes.csv",
        SOURCE_5256 / "boundary_bisection_generation2_nodes.csv",
    )


def analytic_root_rationals(
    event: dict[str, Any], target: complex
) -> dict[str, Any]:
    rows = M5231.M5029.root_rationals(
        event["soft_energy"],
        event["soft_cosine"],
        event["decay_cosine"],
        target,
    )
    for suffix in ("plus_u", "plus_v", "minus_u", "minus_v"):
        rows[f"subtraction:soft:{suffix}"] = rows[
            f"direct:g3:{suffix}"
        ]
    return rows


def analytic_endpoint_geometry(
    problem: dict[str, Any], coordinate: complex
) -> dict[str, Any]:
    event = dict(problem["event"])
    event[problem["case"]["outer_coordinate"]] = complex(coordinate)
    relative_root, _ = M5237.selected_component_roots(
        problem, complex(coordinate)
    )
    rationals = analytic_root_rationals(event, problem["target"])
    global_values = [
        M5231.rational_value_and_derivative(
            rationals[label], relative_root
        )[0]
        for label in problem["case"]["representative_pair"]
    ]
    global_root = complex(sum(global_values) / len(global_values))
    soft_direction, decay_direction, _ = (
        M5238.M5232.M5028.event_geometry(
            event["soft_energy"],
            event["soft_cosine"],
            event["decay_cosine"],
            relative_root,
        )
    )
    soft_rotated = M5238.M5022.rotate_vector(
        soft_direction, global_root
    )
    decay_rotated = M5238.M5022.rotate_vector(
        decay_direction, global_root
    )
    endpoint_internal = np.zeros((3, 4), dtype=np.complex128)
    endpoint_internal[0] = np.concatenate(([1.0], decay_rotated))
    endpoint_internal[1] = np.concatenate(([1.0], -decay_rotated))
    left, right = M5238.M5017.cut_momenta(
        endpoint_internal, problem["target"], 1.0
    )
    soft_left = np.concatenate(([1.0], soft_rotated)).astype(
        np.complex128
    )
    return {
        "left": left,
        "right": right,
        "soft_left": soft_left,
        "soft_right": -soft_left,
    }


def base_point_rows() -> list[dict[str, Any]]:
    specifications = (
        (
            SOURCE_5252 / "full_order9_node_summary.csv",
            0,
            "5252",
        ),
        (
            SOURCE_5253 / "outer_interval_midpoint_nodes.csv",
            0,
            "5253",
        ),
        (
            SOURCE_5254 / "dominant_quarterpoint_nodes.csv",
            0,
            "5254",
        ),
        (
            SOURCE_5255 / "boundary_bisection_generation1_nodes.csv",
            1,
            "5255",
        ),
        (
            SOURCE_5256 / "boundary_bisection_generation2_nodes.csv",
            2,
            "5256",
        ),
        (NODES_5264, -1, "5264"),
    )
    rows: list[dict[str, Any]] = []
    for path, default_generation, checkpoint in specifications:
        for row in read_csv(path):
            generation = int(
                row.get("generation") or default_generation
            )
            rows.append(
                {
                    "order9_node_id": row["order9_node_id"],
                    "decay_cosine": float(row["decay_cosine"]),
                    "generation": generation,
                    "source_checkpoint": checkpoint,
                    "order128": complex(
                        float(row["order128_subtracted_real"]),
                        float(row["order128_subtracted_imaginary"]),
                    ),
                    "order512": complex(
                        float(row["order512_subtracted_real"]),
                        float(row["order512_subtracted_imaginary"]),
                    ),
                }
            )
    return rows


def target_rows() -> list[dict[str, Any]]:
    points = {
        row["order9_node_id"]: row for row in base_point_rows()
    }
    rows: list[dict[str, Any]] = []
    master_index = 0
    for interval_id, (left_id, middle_id, right_id) in (
        SMOOTH_INTERVALS.items()
    ):
        left = float(points[left_id]["decay_cosine"])
        middle = float(points[middle_id]["decay_cosine"])
        right = float(points[right_id]["decay_cosine"])
        for suffix, coordinate, anchor_left, anchor_right in (
            ("L", 0.5 * (left + middle), left_id, middle_id),
            ("R", 0.5 * (middle + right), middle_id, right_id),
        ):
            node_id = f"P{interval_id.removeprefix('I')}{suffix}"
            rows.append(
                {
                    "order9_node_id": node_id,
                    "execution_node_id": f"S65_{master_index:02d}",
                    "master_index": master_index,
                    "decay_cosine": coordinate,
                    "parent_interval_id": interval_id,
                    "node_role": "SMOOTH_INTERVAL_QUARTERPOINT",
                    "left_anchor_id": anchor_left,
                    "right_anchor_id": anchor_right,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
            master_index += 1
    extra_nodes = (
        (
            "L06A",
            0.5
            * (
                float(points["Q06"]["decay_cosine"])
                + float(points["B06L"]["decay_cosine"])
            ),
            "Q06",
            "B06L",
        ),
        (
            "L06B",
            0.5
            * (
                float(points["B06L"]["decay_cosine"])
                + float(points["D06A"]["decay_cosine"])
            ),
            "B06L",
            "D06A",
        ),
    )
    for node_id, coordinate, left_id, right_id in extra_nodes:
        rows.append(
            {
                "order9_node_id": node_id,
                "execution_node_id": f"S65_{master_index:02d}",
                "master_index": master_index,
                "decay_cosine": coordinate,
                "parent_interval_id": "I06",
                "node_role": "I06_LEFT_CHAMBER_REFINEMENT",
                "left_anchor_id": left_id,
                "right_anchor_id": right_id,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
        master_index += 1
    return rows


def fixed_values(targets: list[dict[str, Any]]) -> dict[str, Any]:
    points = sorted(
        base_point_rows(),
        key=lambda row: float(row["decay_cosine"]),
    )
    coordinates = np.asarray(
        [float(row["decay_cosine"]) for row in points],
        dtype=float,
    )
    result: dict[str, Any] = {}
    for order in INNER_ORDERS:
        values = np.asarray(
            [complex(row[f"order{order}"]) for row in points],
            dtype=np.complex128,
        )
        real_fit = PchipInterpolator(coordinates, values.real)
        imaginary_fit = PchipInterpolator(coordinates, values.imag)
        for target in targets:
            coordinate = float(target["decay_cosine"])
            value = complex(
                float(real_fit(coordinate)),
                float(imaginary_fit(coordinate)),
            )
            result.setdefault(target["order9_node_id"], {})[
                str(order)
            ] = [value.real, value.imag]
    return result


def decoded_fixed_values() -> dict[str, dict[int, complex]]:
    payload = json.loads(FIXED_VALUES.read_text(encoding="utf-8"))
    return {
        node_id: {
            int(order): complex(float(value[0]), float(value[1]))
            for order, value in orders.items()
        }
        for node_id, orders in payload.items()
    }


def formal_start_digest() -> str:
    return M5251.inventory_digest(read_csv(FORMAL_INVENTORY))


def build_manifest(
    targets: list[dict[str, Any]],
    fixed: dict[str, Any],
) -> dict[str, Any]:
    manifest = {
        "marker": f"{MARKER}_MANIFEST",
        "revision": REVISION,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "parent_decision": json.loads(
            RESULT_5264.read_text(encoding="utf-8")
        )["decision"],
        "generation": ENGINE_GENERATION,
        "target_node_ids": [
            row["order9_node_id"] for row in targets
        ],
        "outer_nodes": targets,
        "quadrature_orders": list(QUADRATURE_ORDERS),
        "formalization_workbench_start_digest": (
            formal_start_digest()
        ),
        "residue_fit_contract": (
            "constant contour occupation times the bare analytic "
            "component with a genuinely complex owner-channel root; "
            "endpoint geometry retains the full complex outer coordinate"
        ),
        "outer_reassembly_contract": (
            "two-panel Simpson on topology-uniform intervals; "
            "split PCHIP/Akima chamber interpolation on I01/I06"
        ),
        "fixed_reference_hash": serialized_hash(fixed),
        "source_files": [
            {"path": str(path), "sha256": digest(path)}
            for path in source_files()
        ],
        "claim_boundary": {
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "This remains one fixed-soft-energy angular slice."
            ),
        },
    }
    manifest["manifest_hash"] = serialized_hash(manifest)
    return manifest


def prepare() -> dict[str, Any]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    targets = target_rows()
    fixed = fixed_values(targets)
    manifest = build_manifest(targets, fixed)
    checks = {
        "all_sources_exist": all(
            path.exists() for path in source_files()
        ),
        "parent_validation_passed": bool(
            json.loads(RESULT_5264.read_text(encoding="utf-8"))[
                "validation_passed"
            ]
        ),
        "target_count_is_fourteen": len(targets) == 14,
        "target_ids_unique": len(
            {row["order9_node_id"] for row in targets}
        )
        == len(targets),
        "target_coordinates_strictly_internal": all(
            -0.995 < float(row["decay_cosine"]) < 0.995
            for row in targets
        ),
        "formalization_digest_matches_parent": (
            formal_start_digest()
            == json.loads(
                (
                    SOURCE_5264 / "generation_10" / "manifest.json"
                ).read_text(encoding="utf-8")
            )["formalization_workbench_start_digest"]
        ),
        "claim_flags_locked_false": all(
            not bool(manifest["claim_boundary"][field])
            for field in (
                "valid_for_numeric_UV_claim",
                "valid_for_local_GR_claim",
                "valid_for_full_MTS_claim",
            )
        ),
    }
    dry = {
        "marker": f"{MARKER}_DRY_RUN",
        "revision": REVISION,
        "dry_run_passed": all(checks.values()),
        "checks": checks,
        "manifest_hash": manifest["manifest_hash"],
        "writes_performed": True,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    if not dry["dry_run_passed"]:
        failed = [key for key, value in checks.items() if not value]
        raise RuntimeError(f"5265 prepare failed: {failed}")
    write_csv(TARGETS, targets)
    atomic_json(FIXED_VALUES, fixed)
    atomic_json(MANIFEST, manifest)
    atomic_json(DRY_RUN, dry)
    atomic_json(
        STATUS,
        {
            "marker": MARKER,
            "state": "prepared",
            "completed_nodes": 0,
            "total_nodes": len(targets),
            "manifest_hash": manifest["manifest_hash"],
        },
    )
    return dry


def configure_engine(worker_node_id: str | None = None) -> None:
    targets = read_csv(TARGETS)
    fixed = decoded_fixed_values()
    M5264.configure_controller()
    M5238.endpoint_geometry = analytic_endpoint_geometry
    M5261.SOURCE = SOURCE
    M5261.NODES = NODES
    M5261.MARKER = MARKER
    M5261.REVISION = REVISION
    M5261.CHECKPOINT = CHECKPOINT
    M5261.PARENT_CHECKPOINT = PARENT_CHECKPOINT
    M5239.QUADRATURE_ORDERS = QUADRATURE_ORDERS
    M5239.fit_full_component_residues = (
        M5264.fit_occupation_separated_residues
    )
    M5261.configure_node_engine(
        ENGINE_GENERATION,
        targets,
        MANIFEST,
        fixed,
    )
    if worker_node_id is not None:
        M5264.FIT_CANDIDATES = (
            NODES
            / worker_node_id
            / "occupation_separated_fit_candidates.csv"
        )


def worker(node_id: str) -> dict[str, Any]:
    if not MANIFEST.exists():
        raise RuntimeError("run --prepare before workers")
    targets = {
        row["order9_node_id"]: row for row in read_csv(TARGETS)
    }
    if node_id not in targets:
        raise ValueError(f"unsupported node {node_id}")
    configure_engine(node_id)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    existing = M5261.validate_reusable_node(
        node_id,
        manifest["manifest_hash"],
        float(targets[node_id]["decay_cosine"]),
    )
    result = existing if existing is not None else M5251.run_node(node_id)
    if not bool(result["integrity_passed"]):
        raise RuntimeError(f"node integrity failed: {node_id}")
    if not bool(result["acceptance_passed"]):
        raise RuntimeError(f"node acceptance failed: {node_id}")
    print(
        json.dumps(
            {
                "node_id": node_id,
                "reused": existing is not None,
                "integrity_passed": result["integrity_passed"],
                "acceptance_passed": result["acceptance_passed"],
                "elapsed_seconds": result["elapsed_seconds"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return result


def node_result_rows() -> list[dict[str, Any]]:
    targets = read_csv(TARGETS)
    rows: list[dict[str, Any]] = []
    for target in targets:
        node_id = target["order9_node_id"]
        result_path = NODES / node_id / "node_result.json"
        if not result_path.exists():
            continue
        result = json.loads(result_path.read_text(encoding="utf-8"))
        signature = M5261.active_signature(result_path)
        rows.append(
            {
                **target,
                "active_pole_count": len(signature),
                "active_pole_signature": json.dumps(signature),
                "order128_subtracted_real": M5261.result_value(
                    result, 128
                ).real,
                "order128_subtracted_imaginary": M5261.result_value(
                    result, 128
                ).imag,
                "order512_subtracted_real": M5261.result_value(
                    result, 512
                ).real,
                "order512_subtracted_imaginary": M5261.result_value(
                    result, 512
                ).imag,
                "integrity_passed": result["integrity_passed"],
                "acceptance_passed": result["acceptance_passed"],
                "elapsed_seconds": result["elapsed_seconds"],
                "result_path": str(result_path),
                "valid_for_fixed_soft_outer_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def all_point_rows(new_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = base_point_rows()
    for row in new_rows:
        rows.append(
            {
                "order9_node_id": row["order9_node_id"],
                "decay_cosine": float(row["decay_cosine"]),
                "generation": 0,
                "source_checkpoint": "5265",
                "order128": complex(
                    float(row["order128_subtracted_real"]),
                    float(row["order128_subtracted_imaginary"]),
                ),
                "order512": complex(
                    float(row["order512_subtracted_real"]),
                    float(row["order512_subtracted_imaginary"]),
                ),
            }
        )
    return rows


def simpson(
    lower: float,
    middle: float,
    upper: float,
    left_value: complex,
    middle_value: complex,
    right_value: complex,
) -> complex:
    if not math.isclose(
        middle,
        0.5 * (lower + upper),
        rel_tol=0.0,
        abs_tol=2.0e-14,
    ):
        raise RuntimeError("Simpson midpoint is not arithmetic")
    return (
        ANGULAR_JACOBIAN
        * (upper - lower)
        * (left_value + 4.0 * middle_value + right_value)
        / 6.0
    )


def smooth_rule_rows(
    points: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    lookup = {row["order9_node_id"]: row for row in points}
    rows: list[dict[str, Any]] = []
    for interval_id, (
        left_id,
        middle_id,
        right_id,
    ) in SMOOTH_INTERVALS.items():
        left_quarter = f"P{interval_id.removeprefix('I')}L"
        right_quarter = f"P{interval_id.removeprefix('I')}R"
        ids = (
            left_id,
            left_quarter,
            middle_id,
            right_quarter,
            right_id,
        )
        coordinates = [
            float(lookup[node_id]["decay_cosine"]) for node_id in ids
        ]
        row: dict[str, Any] = {
            "interval_id": interval_id,
            "point_ids": "|".join(ids),
            "interval_lower": coordinates[0],
            "interval_upper": coordinates[-1],
            "topology_transition_absent": interval_id
            not in TRANSITION_INTERVALS,
        }
        for order in INNER_ORDERS:
            values = [
                complex(lookup[node_id][f"order{order}"])
                for node_id in ids
            ]
            one_panel = simpson(
                coordinates[0],
                coordinates[2],
                coordinates[4],
                values[0],
                values[2],
                values[4],
            )
            left_panel = simpson(
                coordinates[0],
                coordinates[1],
                coordinates[2],
                values[0],
                values[1],
                values[2],
            )
            right_panel = simpson(
                coordinates[2],
                coordinates[3],
                coordinates[4],
                values[2],
                values[3],
                values[4],
            )
            two_panel = left_panel + right_panel
            richardson = abs(two_panel - one_panel) / 15.0
            row.update(
                {
                    f"order{order}_one_panel_real": one_panel.real,
                    f"order{order}_one_panel_imaginary": (
                        one_panel.imag
                    ),
                    f"order{order}_two_panel_real": two_panel.real,
                    f"order{order}_two_panel_imaginary": (
                        two_panel.imag
                    ),
                    f"order{order}_richardson_error_estimate": (
                        richardson
                    ),
                }
            )
        row.update(
            {
                "valid_for_fixed_soft_outer_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
        rows.append(row)
    return rows


def boundary_lookup() -> dict[str, dict[str, str]]:
    return {
        row["transition_id"]: row
        for row in read_csv(BRACKETS_5264)
    }


def transition_integral(
    points: list[dict[str, Any]],
    interval_id: str,
    order: int,
    method: str,
    maximum_generation: int,
) -> complex:
    lookup = {row["order9_node_id"]: row for row in points}
    left_id, right_id, transition_ids = TRANSITION_INTERVALS[
        interval_id
    ]
    brackets = boundary_lookup()
    bounds = [
        float(lookup[left_id]["decay_cosine"]),
        *[
            0.5
            * (
                float(brackets[transition_id]["left_decay_cosine"])
                + float(
                    brackets[transition_id]["right_decay_cosine"]
                )
            )
            for transition_id in transition_ids
        ],
        float(lookup[right_id]["decay_cosine"]),
    ]
    retained = [
        row
        for row in points
        if row["source_checkpoint"] != "5264"
        or int(row["generation"]) <= maximum_generation
    ]
    total = 0.0j
    for lower, upper in zip(bounds[:-1], bounds[1:]):
        chamber = sorted(
            [
                row
                for row in retained
                if lower - 1.0e-14
                <= float(row["decay_cosine"])
                <= upper + 1.0e-14
            ],
            key=lambda row: float(row["decay_cosine"]),
        )
        if len(chamber) < 2:
            raise RuntimeError(
                f"insufficient chamber points: {interval_id}"
            )
        coordinates = np.asarray(
            [float(row["decay_cosine"]) for row in chamber]
        )
        values = np.asarray(
            [complex(row[f"order{order}"]) for row in chamber]
        )
        interpolator = (
            PchipInterpolator
            if method == "PCHIP"
            else Akima1DInterpolator
        )
        real_fit = interpolator(
            coordinates, values.real, extrapolate=True
        )
        imaginary_fit = interpolator(
            coordinates, values.imag, extrapolate=True
        )
        total += ANGULAR_JACOBIAN * complex(
            float(real_fit.integrate(lower, upper)),
            float(imaginary_fit.integrate(lower, upper)),
        )
    return total


def transition_rule_rows(
    points: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    brackets = boundary_lookup()
    rows: list[dict[str, Any]] = []
    for interval_id, (
        _,
        _,
        transition_ids,
    ) in TRANSITION_INTERVALS.items():
        boundary_error = sum(
            float(
                brackets[transition_id][
                    "boundary_location_error_upper"
                ]
            )
            for transition_id in transition_ids
        )
        row: dict[str, Any] = {
            "interval_id": interval_id,
            "transition_ids": "|".join(transition_ids),
            "certified_boundary_error_upper": boundary_error,
        }
        for order in INNER_ORDERS:
            pchip = transition_integral(
                points,
                interval_id,
                order,
                "PCHIP",
                maximum_generation=10,
            )
            akima = transition_integral(
                points,
                interval_id,
                order,
                "AKIMA",
                maximum_generation=10,
            )
            pchip_generation8 = transition_integral(
                points,
                interval_id,
                order,
                "PCHIP",
                maximum_generation=GENERATION_COMPARISON_LEVEL,
            )
            akima_generation8 = transition_integral(
                points,
                interval_id,
                order,
                "AKIMA",
                maximum_generation=GENERATION_COMPARISON_LEVEL,
            )
            central = 0.5 * (pchip + akima)
            generation8_central = 0.5 * (
                pchip_generation8 + akima_generation8
            )
            half_spread = 0.5 * abs(pchip - akima)
            generation_shift = abs(central - generation8_central)
            empirical_error = (
                half_spread + generation_shift + boundary_error
            )
            row.update(
                {
                    f"order{order}_pchip_real": pchip.real,
                    f"order{order}_pchip_imaginary": pchip.imag,
                    f"order{order}_akima_real": akima.real,
                    f"order{order}_akima_imaginary": akima.imag,
                    f"order{order}_central_real": central.real,
                    f"order{order}_central_imaginary": central.imag,
                    f"order{order}_method_half_spread": half_spread,
                    f"order{order}_generation8_to_final_shift": (
                        generation_shift
                    ),
                    f"order{order}_combined_error_estimate": (
                        empirical_error
                    ),
                }
            )
        row.update(
            {
                "valid_for_fixed_soft_outer_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
        rows.append(row)
    return rows


def coefficient_row(
    smooth_rows: list[dict[str, Any]],
    transition_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    row: dict[str, Any] = {
        "outer_relative_error_limit": OUTER_RELATIVE_ERROR_LIMIT,
        "inner_relative_error_limit": INNER_RELATIVE_ERROR_LIMIT,
    }
    totals: dict[int, complex] = {}
    errors: dict[int, float] = {}
    for order in INNER_ORDERS:
        smooth_total = sum(
            complex(
                float(local[f"order{order}_two_panel_real"]),
                float(
                    local[
                        f"order{order}_two_panel_imaginary"
                    ]
                ),
            )
            for local in smooth_rows
        )
        transition_total = sum(
            complex(
                float(local[f"order{order}_central_real"]),
                float(local[f"order{order}_central_imaginary"]),
            )
            for local in transition_rows
        )
        smooth_error = sum(
            float(
                local[
                    f"order{order}_richardson_error_estimate"
                ]
            )
            for local in smooth_rows
        )
        transition_error = sum(
            float(
                local[f"order{order}_combined_error_estimate"]
            )
            for local in transition_rows
        )
        total = smooth_total + transition_total
        error = smooth_error + transition_error
        totals[order] = total
        errors[order] = error
        row.update(
            {
                f"order{order}_smooth_real": smooth_total.real,
                f"order{order}_smooth_imaginary": smooth_total.imag,
                f"order{order}_transition_real": (
                    transition_total.real
                ),
                f"order{order}_transition_imaginary": (
                    transition_total.imag
                ),
                f"order{order}_coefficient_real": total.real,
                f"order{order}_coefficient_imaginary": total.imag,
                f"order{order}_coefficient_magnitude": abs(total),
                f"order{order}_smooth_error_estimate": smooth_error,
                f"order{order}_transition_error_estimate": (
                    transition_error
                ),
                f"order{order}_total_error_estimate": error,
                f"order{order}_relative_error_estimate": (
                    error / max(abs(total), 1.0e-30)
                ),
            }
        )
    inner_relative = abs(totals[128] - totals[512]) / max(
        abs(totals[512]), 1.0e-30
    )
    accepted = (
        errors[512] / max(abs(totals[512]), 1.0e-30)
        <= OUTER_RELATIVE_ERROR_LIMIT
        and inner_relative <= INNER_RELATIVE_ERROR_LIMIT
    )
    row.update(
        {
            "inner128_to512_relative_difference": inner_relative,
            "fixed_soft_outer_coefficient_accepted": accepted,
            "valid_for_fixed_soft_outer_coefficient": accepted,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
    )
    return row


def write_document(result: dict[str, Any]) -> None:
    lines = [
        "# 5265 — Piecewise outer-coefficient reassembly",
        "",
        "## Construction",
        "",
        (
            "The decay-cosine integral is no longer forced through a "
            "single global polynomial. Six topology-uniform intervals "
            "use nested one-panel/two-panel Simpson rules. I01 and I06 "
            "are split at the four checkpoint-5264 certified boundary "
            "brackets and integrated chamber by chamber."
        ),
        (
            "The transition estimate is the mean of shape-preserving "
            "PCHIP and Akima integrals. Its internal error ledger adds "
            "half their spread, the generation-8 to final-boundary "
            "shift, and the independently certified boundary-location "
            "error. This numerical ledger is conservative but is not "
            "promoted to a theorem-level interpolation bound."
        ),
        "",
        "## Result",
        "",
        f"- Validation passed: `{result['validation_passed']}`.",
        (
            f"- Order-512 coefficient: "
            f"`{result['order512_coefficient_real']} "
            f"{result['order512_coefficient_imaginary']:+}i`."
        ),
        (
            f"- Order-512 magnitude: "
            f"`{result['order512_coefficient_magnitude']}`."
        ),
        (
            f"- Total error estimate: "
            f"`{result['order512_total_error_estimate']}`."
        ),
        (
            f"- Relative error estimate: "
            f"`{result['order512_relative_error_estimate']}`."
        ),
        (
            f"- Inner 128/512 relative difference: "
            f"`{result['inner128_to512_relative_difference']}`."
        ),
        (
            f"- Fixed-soft outer coefficient accepted: "
            f"`{result['valid_for_fixed_soft_outer_coefficient']}`."
        ),
        f"- Decision: `{result['decision']}`.",
        "",
        "## Claim boundary",
        "",
        (
            "This locks one fixed-soft-energy two-angular coefficient. "
            "The final soft-energy integration, endpoint subtraction "
            "across that variable, and source-pool replication remain "
            "required before a numeric UV coefficient can be claimed. "
            "No local-GR or full-MTS claim follows from this checkpoint."
        ),
        "",
    ]
    atomic_text(DOC, "\n".join(lines))


def aggregate() -> dict[str, Any]:
    configure_engine()
    rows = node_result_rows()
    if len(rows) != len(read_csv(TARGETS)):
        missing = sorted(
            {
                row["order9_node_id"] for row in read_csv(TARGETS)
            }
            - {row["order9_node_id"] for row in rows}
        )
        raise RuntimeError(f"missing 5265 node results: {missing}")
    points = all_point_rows(rows)
    smooth_rows = smooth_rule_rows(points)
    transition_rows = transition_rule_rows(points)
    coefficient = coefficient_row(smooth_rows, transition_rows)
    formal_after = M5251.formal_inventory_rows()
    formal_before = read_csv(FORMAL_INVENTORY)
    formal_diff = M5251.inventory_diff_rows(
        formal_before, formal_after
    )
    write_csv(FORMAL_DIFF, formal_diff)
    fit_rows = []
    for path in NODES.glob(
        "*/corrected_residue_fits.csv"
    ):
        fit_rows.extend(read_csv(path))
    checks = [
        {
            "check_id": "ALL_FOURTEEN_TARGET_NODES_COMPLETE",
            "passed": len(rows) == 14,
            "detail": f"nodes={len(rows)}",
        },
        {
            "check_id": "ALL_NODE_GATES_PASS",
            "passed": all(
                parse_bool(row["integrity_passed"])
                and parse_bool(row["acceptance_passed"])
                for row in rows
            ),
            "detail": (
                f"passed={sum(parse_bool(row['integrity_passed']) and parse_bool(row['acceptance_passed']) for row in rows)}/"
                f"{len(rows)}"
            ),
        },
        {
            "check_id": "ALL_ACTIVE_RESIDUE_CERTIFICATES_PASS",
            "passed": all(
                parse_bool(row["fit_passed"])
                and parse_bool(
                    row[
                        "direct_simple_pole_certificate_passed"
                    ]
                )
                for row in fit_rows
            ),
            "detail": f"active_fit_rows={len(fit_rows)}",
        },
        {
            "check_id": "ALL_SMOOTH_INTERVAL_RULES_COMPLETE",
            "passed": len(smooth_rows) == len(SMOOTH_INTERVALS)
            and all(
                parse_bool(row["topology_transition_absent"])
                for row in smooth_rows
            ),
            "detail": f"intervals={len(smooth_rows)}",
        },
        {
            "check_id": "TRANSITION_RULES_SPLIT_AT_CERTIFIED_BRACKETS",
            "passed": len(transition_rows)
            == len(TRANSITION_INTERVALS),
            "detail": f"intervals={len(transition_rows)}",
        },
        {
            "check_id": "OUTER_RELATIVE_ERROR_GATE_PASSES",
            "passed": float(
                coefficient["order512_relative_error_estimate"]
            )
            <= OUTER_RELATIVE_ERROR_LIMIT,
            "detail": (
                f"observed={coefficient['order512_relative_error_estimate']}; "
                f"limit={OUTER_RELATIVE_ERROR_LIMIT}"
            ),
        },
        {
            "check_id": "INNER_128_TO_512_GATE_PASSES",
            "passed": float(
                coefficient[
                    "inner128_to512_relative_difference"
                ]
            )
            <= INNER_RELATIVE_ERROR_LIMIT,
            "detail": (
                f"observed={coefficient['inner128_to512_relative_difference']}; "
                f"limit={INNER_RELATIVE_ERROR_LIMIT}"
            ),
        },
        {
            "check_id": "FORMALIZATION_WORKBENCH_UNCHANGED",
            "passed": len(formal_diff) == 0,
            "detail": f"modified_files={len(formal_diff)}",
        },
        {
            "check_id": "HIGHER_CLAIMS_REMAIN_FALSE",
            "passed": all(
                not parse_bool(coefficient[field])
                for field in (
                    "valid_for_numeric_UV_claim",
                    "valid_for_local_GR_claim",
                    "valid_for_full_MTS_claim",
                )
            ),
            "detail": "false,false,false",
        },
    ]
    passed = all(bool(row["passed"]) for row in checks)
    accepted = bool(
        coefficient["valid_for_fixed_soft_outer_coefficient"]
    )
    result = {
        "marker": MARKER,
        "revision": REVISION,
        "validation_passed": passed,
        **{
            key: value
            for key, value in coefficient.items()
            if key.startswith("order512_")
            or key
            in {
                "inner128_to512_relative_difference",
                "valid_for_fixed_soft_outer_coefficient",
                "valid_for_numeric_UV_claim",
                "valid_for_local_GR_claim",
                "valid_for_full_MTS_claim",
            }
        },
        "node_count": len(rows),
        "smooth_interval_count": len(smooth_rows),
        "transition_interval_count": len(transition_rows),
        "formalization_workbench_modified_file_count": len(
            formal_diff
        ),
        "decision": (
            "ADOPT_FIXED_SOFT_PIECEWISE_OUTER_COEFFICIENT__"
            "HANDOFF_TO_SOFT_ENERGY_RULE"
            if passed and accepted
            else "HOLD_PIECEWISE_OUTER_COEFFICIENT"
        ),
    }
    write_csv(NODE_ROWS, rows)
    write_csv(SMOOTH_RULES, smooth_rows)
    write_csv(TRANSITION_RULES, transition_rows)
    write_csv(COEFFICIENT_ROWS, [coefficient])
    write_csv(VALIDATION, checks)
    atomic_json(RESULT, result)
    write_document(result)
    atomic_json(
        STATUS,
        {
            "marker": MARKER,
            "state": "complete" if passed else "validation_failed",
            "completed_nodes": len(rows),
            "total_nodes": len(read_csv(TARGETS)),
            "validation_passed": passed,
            "decision": result["decision"],
        },
    )
    if not passed:
        failed = [
            row["check_id"] for row in checks if not row["passed"]
        ]
        raise RuntimeError(f"5265 validation failed: {failed}")
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def status() -> dict[str, Any]:
    targets = read_csv(TARGETS) if TARGETS.exists() else []
    completed = [
        row["order9_node_id"]
        for row in targets
        if (NODES / row["order9_node_id"] / "node_result.json").exists()
    ]
    running = []
    for row in targets:
        status_path = (
            NODES / row["order9_node_id"] / "node_status.json"
        )
        if status_path.exists():
            node_status = json.loads(
                status_path.read_text(encoding="utf-8")
            )
            if node_status.get("status") == "RUNNING":
                running.append(
                    {
                        "node_id": row["order9_node_id"],
                        "completed_jobs": node_status.get(
                            "completed_jobs", 0
                        ),
                        "total_jobs": node_status.get(
                            "total_jobs", 12
                        ),
                    }
                )
    result = {
        "prepared": MANIFEST.exists(),
        "completed_count": len(completed),
        "total_count": len(targets),
        "completed_node_ids": completed,
        "running": running,
        "pending_node_ids": [
            row["order9_node_id"]
            for row in targets
            if row["order9_node_id"] not in completed
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--worker-node")
    parser.add_argument("--aggregate", action="store_true")
    parser.add_argument("--status", action="store_true")
    arguments = parser.parse_args()
    selected = sum(
        bool(value)
        for value in (
            arguments.prepare,
            arguments.worker_node,
            arguments.aggregate,
            arguments.status,
        )
    )
    if selected != 1:
        raise SystemExit(
            "select exactly one of --prepare, --worker-node, "
            "--aggregate, or --status"
        )
    started = time.perf_counter()
    if arguments.prepare:
        print(json.dumps(prepare(), indent=2, sort_keys=True))
    elif arguments.worker_node:
        worker(arguments.worker_node)
    elif arguments.aggregate:
        aggregate()
    else:
        status()
    print(
        json.dumps(
            {"elapsed_seconds": time.perf_counter() - started},
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
