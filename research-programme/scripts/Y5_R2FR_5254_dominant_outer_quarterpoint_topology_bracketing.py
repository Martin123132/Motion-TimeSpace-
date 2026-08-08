from __future__ import annotations

import argparse
import concurrent.futures
import csv
import hashlib
import importlib.util
import json
import math
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5254"
NODES = SOURCE / "nodes"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5253 = (
    POST
    / "scripts"
    / "Y5_R2FR_5253_corrected_outer_interval_midpoint_localization.py"
)
SOURCE_5253 = POST / "source-intake" / "functional_rg" / "5253"
RESULT_5253 = SOURCE_5253 / "outer_interval_midpoint_result.json"
MANIFEST_5253 = SOURCE_5253 / "outer_interval_midpoint_manifest.json"
MIDPOINT_ROWS_5253 = SOURCE_5253 / "outer_interval_midpoint_nodes.csv"
INTERVAL_ROWS_5253 = SOURCE_5253 / "outer_interval_localization.csv"
VALIDATION_5253 = RESIDUALS / "P8_Y5_BRR545_5253_VALIDATION.csv"

MANIFEST = SOURCE / "dominant_quarterpoint_manifest.json"
DRY_RUN = SOURCE / "dominant_quarterpoint_dry_run.json"
STATUS = SOURCE / "dominant_quarterpoint_status.json"
RESULT = SOURCE / "dominant_quarterpoint_result.json"
QUARTERPOINT_ROWS = SOURCE / "dominant_quarterpoint_nodes.csv"
TWO_PANEL_ROWS = SOURCE / "dominant_interval_two_panel_rules.csv"
TOPOLOGY_ROWS = SOURCE / "outer_topology_transition_brackets.csv"
FORMAL_INVENTORY = SOURCE / "formalization_workbench_start_inventory.csv"
FORMAL_DIFF = SOURCE / "formalization_workbench_run_diff.csv"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5254_VALIDATION.csv"
DOCUMENT = (
    POST
    / "5254-Y5-R2FR-dominant-outer-quarterpoint-topology-bracketing.md"
)
COMPLETE = SOURCE / "COMPLETE.marker"

CHECKPOINT = 5254
PARENT_CHECKPOINT = 5253
MARKER = "MTS_5254_DOMINANT_OUTER_QUARTERPOINT_TOPOLOGY_BRACKETING"
REVISION = "dominant-outer-quarterpoint-topology-bracketing-v1"
TRANSPORT_CACHE_REVISION = (
    "dominant-outer-quarterpoint-topology-bracketing-v1"
)
TARGET_NODE_IDS = ("B01L", "B01R", "B06L", "B06R")
TARGET_INTERVAL_IDS = ("I01", "I06")
INNER_ORDERS = (128, 512)
DEFAULT_MAX_WORKERS = 2
MAXIMUM_NODE_RUNTIME_SECONDS = 4.0 * 60.0 * 60.0
MAXIMUM_BATCH_RUNTIME_SECONDS = 6.0 * 60.0 * 60.0
ANGULAR_JACOBIAN = 0.25
EXPECTED_PARENT_DECISION = (
    "ADOPT_INTERVAL_ERROR_MAP__BISECT_DOMINANT_INTERVALS"
)


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"Unable to load {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


M5253 = load_module(SCRIPT_5253, "mts_5253_for_5254")
M5251 = M5253.M5251


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


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def parent_rows_by_id() -> dict[str, dict[str, str]]:
    return {
        row["order9_node_id"]: row
        for row in M5253.parent_node_rows()
    }


def midpoint_rows_by_id() -> dict[str, dict[str, str]]:
    return {
        row["order9_node_id"]: row
        for row in read_csv(MIDPOINT_ROWS_5253)
    }


def interval_rows_by_id() -> dict[str, dict[str, str]]:
    return {
        row["interval_id"]: row
        for row in read_csv(INTERVAL_ROWS_5253)
    }


def complex_row_value(
    row: dict[str, str], inner_order: int
) -> complex:
    return complex(
        float(row[f"order{inner_order}_subtracted_real"]),
        float(row[f"order{inner_order}_subtracted_imaginary"]),
    )


def interval_anchor_contracts() -> dict[str, dict[str, Any]]:
    parents = parent_rows_by_id()
    midpoints = midpoint_rows_by_id()
    return {
        "I01": {
            "left_id": "Q01",
            "middle_id": "M01",
            "right_id": "Q02",
            "left": parents["Q01"],
            "middle": midpoints["M01"],
            "right": parents["Q02"],
            "left_quarter_id": "B01L",
            "right_quarter_id": "B01R",
        },
        "I06": {
            "left_id": "Q06",
            "middle_id": "M06",
            "right_id": "Q07",
            "left": parents["Q06"],
            "middle": midpoints["M06"],
            "right": parents["Q07"],
            "left_quarter_id": "B06L",
            "right_quarter_id": "B06R",
        },
    }


def point_coordinate(row: dict[str, str]) -> float:
    return float(row["decay_cosine"])


def quarterpoint_nodes() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    execution_index = 0
    for interval_id in TARGET_INTERVAL_IDS:
        contract = interval_anchor_contracts()[interval_id]
        left_x = point_coordinate(contract["left"])
        middle_x = point_coordinate(contract["middle"])
        right_x = point_coordinate(contract["right"])
        definitions = (
            (
                contract["left_quarter_id"],
                "LEFT_QUARTER",
                contract["left_id"],
                contract["middle_id"],
                0.5 * (left_x + middle_x),
            ),
            (
                contract["right_quarter_id"],
                "RIGHT_QUARTER",
                contract["middle_id"],
                contract["right_id"],
                0.5 * (middle_x + right_x),
            ),
        )
        for (
            node_id,
            role,
            left_anchor_id,
            right_anchor_id,
            coordinate,
        ) in definitions:
            rows.append(
                {
                    "order9_node_id": node_id,
                    "execution_node_id": f"T{execution_index:02d}",
                    "master_index": execution_index,
                    "decay_cosine": coordinate,
                    "parent_interval_id": interval_id,
                    "quarter_role": role,
                    "left_anchor_id": left_anchor_id,
                    "right_anchor_id": right_anchor_id,
                    "reused_from_5240": False,
                    "source_cache": str(
                        NODES / node_id / "node_result.json"
                    ),
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
            execution_index += 1
    return rows


def point_value(
    interval_id: str, point_id: str, inner_order: int
) -> complex:
    contract = interval_anchor_contracts()[interval_id]
    if point_id == contract["left_id"]:
        return complex_row_value(contract["left"], inner_order)
    if point_id == contract["middle_id"]:
        return complex_row_value(contract["middle"], inner_order)
    if point_id == contract["right_id"]:
        return complex_row_value(contract["right"], inner_order)
    raise KeyError(point_id)


def quarterpoint_reference_values() -> dict[
    str, dict[int, complex]
]:
    references: dict[str, dict[int, complex]] = {}
    for node in quarterpoint_nodes():
        interval_id = node["parent_interval_id"]
        references[node["order9_node_id"]] = {
            inner_order: 0.5
            * (
                point_value(
                    interval_id,
                    node["left_anchor_id"],
                    inner_order,
                )
                + point_value(
                    interval_id,
                    node["right_anchor_id"],
                    inner_order,
                )
            )
            for inner_order in INNER_ORDERS
        }
    return references


def configure_node_engine() -> None:
    M5251.SOURCE = SOURCE
    M5251.NODES = NODES
    M5251.MANIFEST = MANIFEST
    M5251.MANIFEST_5241 = MANIFEST
    M5251.MARKER = MARKER
    M5251.REVISION = REVISION
    M5251.TRANSPORT_CACHE_REVISION = TRANSPORT_CACHE_REVISION
    M5251.CHECKPOINT = CHECKPOINT
    M5251.PARENT_CHECKPOINT = PARENT_CHECKPOINT
    M5251.TARGET_NODE_IDS = TARGET_NODE_IDS
    M5251.RESULT_5250 = RESULT_5253
    M5251.MAXIMUM_NODE_RUNTIME_SECONDS = MAXIMUM_NODE_RUNTIME_SECONDS
    M5251.fixed_node_values = quarterpoint_reference_values
    M5251.M5243.compare_intervals = (
        M5253.no_same_coordinate_legacy_comparison
    )


def source_rows() -> list[dict[str, str]]:
    paths = [
        Path(__file__),
        SCRIPT_5253,
        RESULT_5253,
        MANIFEST_5253,
        MIDPOINT_ROWS_5253,
        INTERVAL_ROWS_5253,
        VALIDATION_5253,
    ]
    contracts = interval_anchor_contracts()
    for interval_id in TARGET_INTERVAL_IDS:
        contract = contracts[interval_id]
        paths.extend(
            [
                Path(contract["left"]["source_path"]),
                Path(contract["middle"]["source_cache"]),
                Path(contract["right"]["source_path"]),
            ]
        )
    unique_paths = sorted(set(paths), key=str)
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in unique_paths
    ]


def prepare() -> tuple[dict[str, Any], dict[str, Any]]:
    configure_node_engine()
    parent_result = read_json(RESULT_5253)
    parent_validation = read_csv(VALIDATION_5253)
    target_nodes = quarterpoint_nodes()
    formal_rows = M5251.formal_inventory_rows()
    formal_digest = M5251.inventory_digest(formal_rows)
    M5251.write_csv(FORMAL_INVENTORY, formal_rows)
    manifest = {
        "marker": MARKER,
        "revision": REVISION,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "parent_decision": parent_result["decision"],
        "parent_integrity_passed": parent_result["integrity_passed"],
        "target_interval_ids": list(TARGET_INTERVAL_IDS),
        "target_node_ids": list(TARGET_NODE_IDS),
        "outer_nodes": target_nodes,
        "topology_contract": {
            "point_order": (
                "left endpoint, left quarter, midpoint, right quarter, "
                "right endpoint"
            ),
            "richardson_authorization": (
                "All five points must have the same canonical active-pole "
                "signature before |S_two-S_one|/15 may be reported as a "
                "smooth-panel error estimate."
            ),
            "nonuniform_action": (
                "Retain raw one-panel/two-panel differences only as "
                "diagnostics and bisect every adjacent signature-change "
                "bracket."
            ),
        },
        "angular_unit_cube_jacobian": ANGULAR_JACOBIAN,
        "maximum_node_runtime_seconds": (
            MAXIMUM_NODE_RUNTIME_SECONDS
        ),
        "maximum_batch_runtime_seconds": (
            MAXIMUM_BATCH_RUNTIME_SECONDS
        ),
        "formalization_workbench_start_digest": formal_digest,
        "formalization_workbench_start_file_count": len(formal_rows),
        "source_files": source_rows(),
        "claim_boundary": {
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "Quarter points localize outer topology changes. They do "
                "not yet close the decay-angle integral or produce the "
                "canonical p8 coefficient."
            ),
        },
    }
    manifest["manifest_hash"] = serialized_hash(manifest)
    selected_parent_rows = [
        row
        for row in read_csv(INTERVAL_ROWS_5253)
        if row["selected_for_quarterpoint_refinement"] == "True"
    ]
    parent_integrity = [
        row
        for row in parent_validation
        if row["gate_kind"] == "integrity"
    ]
    checks = {
        "source_paths_exist_and_match": all(
            Path(row["path"]).exists()
            and digest(Path(row["path"])) == row["sha256"]
            for row in manifest["source_files"]
        ),
        "parent_integrity_passed": (
            bool(parent_result["integrity_passed"])
            and all(
                row["passed"] == "True" for row in parent_integrity
            )
        ),
        "parent_decision_authorizes_bisection": (
            parent_result["decision"] == EXPECTED_PARENT_DECISION
        ),
        "dominant_intervals_exact": (
            {
                row["interval_id"] for row in selected_parent_rows
            }
            == set(TARGET_INTERVAL_IDS)
        ),
        "quarterpoint_accounting_exact": (
            len(target_nodes) == 4
            and {
                row["order9_node_id"] for row in target_nodes
            }
            == set(TARGET_NODE_IDS)
        ),
        "quarterpoint_coordinates_exact": all(
            math.isclose(
                float(node["decay_cosine"]),
                0.5
                * (
                    point_coordinate(
                        next(
                            contract[key]
                            for key in ("left", "middle", "right")
                            if contract[f"{key}_id"]
                            == node["left_anchor_id"]
                        )
                    )
                    + point_coordinate(
                        next(
                            contract[key]
                            for key in ("left", "middle", "right")
                            if contract[f"{key}_id"]
                            == node["right_anchor_id"]
                        )
                    )
                ),
                rel_tol=0.0,
                abs_tol=2.0e-15,
            )
            for node in target_nodes
            for contract in [
                interval_anchor_contracts()[
                    node["parent_interval_id"]
                ]
            ]
        ),
        "formal_tree_stable_during_prepare": (
            M5251.tree_digest(FORMAL) == formal_digest
        ),
        "claims_locked_false": all(
            not bool(manifest["claim_boundary"][field])
            for field in (
                "valid_for_numeric_UV_claim",
                "valid_for_local_GR_claim",
                "valid_for_full_MTS_claim",
            )
        ),
    }
    dry_run = {
        "marker": MARKER,
        "revision": REVISION,
        "dry_run_passed": all(checks.values()),
        "checks": checks,
        "manifest_hash": manifest["manifest_hash"],
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    return manifest, dry_run


def run_worker(node_id: str) -> int:
    paths = M5251.node_paths(node_id)
    paths["root"].mkdir(parents=True, exist_ok=True)
    command = [
        sys.executable,
        str(Path(__file__)),
        "--worker-node",
        node_id,
    ]
    with (paths["root"] / "worker.log").open(
        "w", encoding="utf-8"
    ) as log_handle:
        completed = subprocess.run(
            command,
            stdout=log_handle,
            stderr=subprocess.STDOUT,
            check=False,
            timeout=MAXIMUM_NODE_RUNTIME_SECONDS + 300.0,
        )
    return int(completed.returncode)


def launch_workers(max_workers: int) -> dict[str, int]:
    return_codes: dict[str, int] = {}
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=max_workers
    ) as executor:
        futures = {
            executor.submit(run_worker, node_id): node_id
            for node_id in TARGET_NODE_IDS
        }
        for future in concurrent.futures.as_completed(futures):
            node_id = futures[future]
            return_codes[node_id] = future.result()
            M5251.atomic_json(
                STATUS,
                {
                    "marker": MARKER,
                    "status": "RUNNING",
                    "completed_nodes": len(return_codes),
                    "successful_nodes": sum(
                        code == 0 for code in return_codes.values()
                    ),
                    "total_nodes": len(TARGET_NODE_IDS),
                    "return_codes": return_codes,
                },
            )
    return return_codes


def node_result(node_id: str) -> dict[str, Any]:
    return read_json(M5251.node_paths(node_id)["result"])


def result_value(
    result: dict[str, Any], inner_order: int
) -> complex:
    values = result["physical_values"][str(inner_order)]
    return complex(
        float(values["subtracted_real"]),
        float(values["subtracted_imaginary"]),
    )


def active_signature_from_catalog(path: Path) -> tuple[str, ...]:
    if not path.exists():
        raise FileNotFoundError(path)
    signature = []
    for row in read_csv(path):
        if row["causal_family_active"] != "True":
            continue
        signature.append(
            "|".join(
                [
                    row["epsilon_id"],
                    row["component_id"],
                    row["pole_id"],
                    format(
                        float(row["dynamic_winding_multiplier"]),
                        ".12g",
                    ),
                ]
            )
        )
    return tuple(sorted(signature))


def result_catalog_path(result_path: Path) -> Path:
    return result_path.parent / "corrected_pole_catalog.csv"


def endpoint_record(
    interval_id: str,
    point_id: str,
    row: dict[str, str],
) -> dict[str, Any]:
    result_path = Path(row["source_path"])
    result = read_json(result_path)
    signature = active_signature_from_catalog(
        result_catalog_path(result_path)
    )
    return {
        "interval_id": interval_id,
        "point_id": point_id,
        "point_role": (
            "LEFT_ENDPOINT"
            if point_id
            == interval_anchor_contracts()[interval_id]["left_id"]
            else "RIGHT_ENDPOINT"
        ),
        "decay_cosine": point_coordinate(row),
        "result_path": str(result_path),
        "active_pole_count": len(signature),
        "active_signature": signature,
        "values": {
            inner_order: complex_row_value(row, inner_order)
            for inner_order in INNER_ORDERS
        },
        "integrity_passed": bool(result["integrity_passed"]),
        "acceptance_passed": bool(result["acceptance_passed"]),
    }


def midpoint_record(
    interval_id: str,
    point_id: str,
    row: dict[str, str],
) -> dict[str, Any]:
    result_path = Path(row["source_cache"])
    result = read_json(result_path)
    signature = active_signature_from_catalog(
        result_catalog_path(result_path)
    )
    return {
        "interval_id": interval_id,
        "point_id": point_id,
        "point_role": "MIDPOINT",
        "decay_cosine": point_coordinate(row),
        "result_path": str(result_path),
        "active_pole_count": len(signature),
        "active_signature": signature,
        "values": {
            inner_order: complex_row_value(row, inner_order)
            for inner_order in INNER_ORDERS
        },
        "integrity_passed": bool(result["integrity_passed"]),
        "acceptance_passed": bool(result["acceptance_passed"]),
    }


def quarterpoint_record(
    node: dict[str, Any], result: dict[str, Any]
) -> dict[str, Any]:
    result_path = M5251.node_paths(
        node["order9_node_id"]
    )["result"]
    signature = active_signature_from_catalog(
        result_catalog_path(result_path)
    )
    return {
        "interval_id": node["parent_interval_id"],
        "point_id": node["order9_node_id"],
        "point_role": node["quarter_role"],
        "decay_cosine": float(node["decay_cosine"]),
        "result_path": str(result_path),
        "active_pole_count": len(signature),
        "active_signature": signature,
        "values": {
            inner_order: result_value(result, inner_order)
            for inner_order in INNER_ORDERS
        },
        "integrity_passed": bool(result["integrity_passed"]),
        "acceptance_passed": bool(result["acceptance_passed"]),
    }


def ordered_interval_points(
    interval_id: str,
    results: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    contract = interval_anchor_contracts()[interval_id]
    node_map = {
        row["order9_node_id"]: row for row in quarterpoint_nodes()
    }
    points = [
        endpoint_record(
            interval_id, contract["left_id"], contract["left"]
        ),
        quarterpoint_record(
            node_map[contract["left_quarter_id"]],
            results[contract["left_quarter_id"]],
        ),
        midpoint_record(
            interval_id,
            contract["middle_id"],
            contract["middle"],
        ),
        quarterpoint_record(
            node_map[contract["right_quarter_id"]],
            results[contract["right_quarter_id"]],
        ),
        endpoint_record(
            interval_id, contract["right_id"], contract["right"]
        ),
    ]
    return sorted(points, key=lambda point: point["decay_cosine"])


def build_quarterpoint_rows(
    results: dict[str, dict[str, Any]]
) -> list[dict[str, Any]]:
    references = quarterpoint_reference_values()
    rows = []
    for node in quarterpoint_nodes():
        node_id = node["order9_node_id"]
        result = results[node_id]
        value_128 = result_value(result, 128)
        value_512 = result_value(result, 512)
        signature = active_signature_from_catalog(
            result_catalog_path(M5251.node_paths(node_id)["result"])
        )
        rows.append(
            {
                **node,
                "integrity_passed": result["integrity_passed"],
                "acceptance_passed": result["acceptance_passed"],
                "active_pole_count": len(signature),
                "active_pole_signature": json.dumps(signature),
                "order128_subtracted_real": value_128.real,
                "order128_subtracted_imaginary": value_128.imag,
                "order512_subtracted_real": value_512.real,
                "order512_subtracted_imaginary": value_512.imag,
                "endpoint_linear_reference_512_real": (
                    references[node_id][512].real
                ),
                "endpoint_linear_reference_512_imaginary": (
                    references[node_id][512].imag
                ),
                "inner128_to512_relative_difference": (
                    abs(value_128 - value_512)
                    / max(abs(value_512), 1.0)
                ),
                "elapsed_seconds": result["elapsed_seconds"],
                "internal_fixed_field_semantics": (
                    "ADJACENT_ANCHOR_LINEAR_REFERENCE_DIAGNOSTIC_ONLY"
                ),
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def analyze_intervals(
    results: dict[str, dict[str, Any]]
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    two_panel_rows: list[dict[str, Any]] = []
    transition_rows: list[dict[str, Any]] = []
    replacements: dict[int, complex] = {
        inner_order: 0.0j for inner_order in INNER_ORDERS
    }
    for interval_id in TARGET_INTERVAL_IDS:
        points = ordered_interval_points(interval_id, results)
        signatures = [
            point["active_signature"] for point in points
        ]
        topology_uniform = len(set(signatures)) == 1
        width = (
            points[-1]["decay_cosine"]
            - points[0]["decay_cosine"]
        )
        row: dict[str, Any] = {
            "interval_id": interval_id,
            "interval_lower": points[0]["decay_cosine"],
            "interval_upper": points[-1]["decay_cosine"],
            "interval_width": width,
            "point_ids": "|".join(
                point["point_id"] for point in points
            ),
            "active_pole_counts": "|".join(
                str(point["active_pole_count"])
                for point in points
            ),
            "topology_uniform_across_five_points": (
                topology_uniform
            ),
            "richardson_authorized": topology_uniform,
        }
        for inner_order in INNER_ORDERS:
            values = [
                point["values"][inner_order] for point in points
            ]
            one_panel = (
                ANGULAR_JACOBIAN
                * width
                / 6.0
                * (values[0] + 4.0 * values[2] + values[4])
            )
            two_panel = (
                ANGULAR_JACOBIAN
                * width
                / 12.0
                * (
                    values[0]
                    + 4.0 * values[1]
                    + 2.0 * values[2]
                    + 4.0 * values[3]
                    + values[4]
                )
            )
            difference = two_panel - one_panel
            replacements[inner_order] += difference
            prefix = f"order{inner_order}"
            row.update(
                {
                    f"{prefix}_one_panel_real": one_panel.real,
                    f"{prefix}_one_panel_imaginary": one_panel.imag,
                    f"{prefix}_two_panel_real": two_panel.real,
                    f"{prefix}_two_panel_imaginary": two_panel.imag,
                    f"{prefix}_raw_difference_real": difference.real,
                    f"{prefix}_raw_difference_imaginary": (
                        difference.imag
                    ),
                    f"{prefix}_raw_difference_magnitude": abs(
                        difference
                    ),
                    f"{prefix}_richardson_error_estimate": (
                        abs(difference) / 15.0
                        if topology_uniform
                        else ""
                    ),
                }
            )
        row.update(
            {
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
        two_panel_rows.append(row)

        transition_index = 0
        for left, right in zip(points[:-1], points[1:]):
            if left["active_signature"] == right["active_signature"]:
                continue
            transition_rows.append(
                {
                    "transition_id": (
                        f"{interval_id}_T{transition_index:02d}"
                    ),
                    "interval_id": interval_id,
                    "left_point_id": left["point_id"],
                    "right_point_id": right["point_id"],
                    "left_decay_cosine": left["decay_cosine"],
                    "right_decay_cosine": right["decay_cosine"],
                    "bracket_width": (
                        right["decay_cosine"]
                        - left["decay_cosine"]
                    ),
                    "parent_interval_width": width,
                    "bracket_to_parent_width_ratio": (
                        (
                            right["decay_cosine"]
                            - left["decay_cosine"]
                        )
                        / width
                    ),
                    "left_active_pole_count": (
                        left["active_pole_count"]
                    ),
                    "right_active_pole_count": (
                        right["active_pole_count"]
                    ),
                    "left_active_signature": json.dumps(
                        left["active_signature"]
                    ),
                    "right_active_signature": json.dumps(
                        right["active_signature"]
                    ),
                    "next_bisection_coordinate": 0.5
                    * (
                        left["decay_cosine"]
                        + right["decay_cosine"]
                    ),
                    "richardson_forbidden_across_bracket": True,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
            transition_index += 1

    parent_summary = read_json(RESULT_5253)["summary"]
    parent_simpson = {
        512: complex(
            float(parent_summary["composite_simpson_512_real"]),
            float(
                parent_summary[
                    "composite_simpson_512_imaginary"
                ]
            ),
        )
    }
    parent_composite_rows = read_csv(
        SOURCE_5253 / "outer_composite_rules.csv"
    )
    parent_128_row = next(
        row
        for row in parent_composite_rows
        if row["inner_order"] == "128"
        and row["outer_rule"] == "SIMPSON"
    )
    parent_simpson[128] = complex(
        float(parent_128_row["value_real"]),
        float(parent_128_row["value_imaginary"]),
    )
    adaptive = {
        inner_order: parent_simpson[inner_order]
        + replacements[inner_order]
        for inner_order in INNER_ORDERS
    }
    summary = {
        "transition_bracket_count": len(transition_rows),
        "transition_brackets_per_interval": {
            interval_id: sum(
                row["interval_id"] == interval_id
                for row in transition_rows
            )
            for interval_id in TARGET_INTERVAL_IDS
        },
        "maximum_transition_bracket_to_parent_width_ratio": max(
            float(row["bracket_to_parent_width_ratio"])
            for row in transition_rows
        ),
        "all_target_intervals_topology_uniform": all(
            bool(row["topology_uniform_across_five_points"])
            for row in two_panel_rows
        ),
        "richardson_authorized_interval_count": sum(
            bool(row["richardson_authorized"])
            for row in two_panel_rows
        ),
        "adaptive_two_panel_512_real": adaptive[512].real,
        "adaptive_two_panel_512_imaginary": adaptive[512].imag,
        "adaptive_two_panel_inner128_to512_relative_difference": (
            abs(adaptive[128] - adaptive[512])
            / max(abs(adaptive[512]), 1.0)
        ),
        "adaptive_two_panel_to_parent_simpson_relative_difference": (
            abs(adaptive[512] - parent_simpson[512])
            / max(abs(adaptive[512]), 1.0)
        ),
        "adaptive_value_valid_for_outer_claim": False,
        "next_bisection_coordinates": [
            {
                "transition_id": row["transition_id"],
                "decay_cosine": row[
                    "next_bisection_coordinate"
                ],
            }
            for row in transition_rows
        ],
    }
    return two_panel_rows, transition_rows, summary


def validation_rows(
    manifest: dict[str, Any],
    results: dict[str, dict[str, Any]],
    quarterpoint_rows: list[dict[str, Any]],
    two_panel_rows: list[dict[str, Any]],
    transition_rows: list[dict[str, Any]],
    summary: dict[str, Any],
    formal_diff_rows: list[dict[str, Any]],
    elapsed: float,
) -> list[dict[str, Any]]:
    brackets_by_interval = summary[
        "transition_brackets_per_interval"
    ]
    definitions = [
        (
            "integrity",
            "SOURCE_PATHS_EXIST_AND_MATCH",
            all(
                Path(row["path"]).exists()
                and digest(Path(row["path"])) == row["sha256"]
                for row in manifest["source_files"]
            ),
            len(manifest["source_files"]),
            "all source paths and hashes",
        ),
        (
            "integrity",
            "QUARTERPOINT_NODE_ACCOUNTING_EXACT",
            (
                set(results) == set(TARGET_NODE_IDS)
                and len(quarterpoint_rows) == 4
            ),
            f"{len(results)} results, {len(quarterpoint_rows)} rows",
            "4 results, 4 rows",
        ),
        (
            "integrity",
            "ALL_QUARTERPOINT_INTEGRITY_GATES_PASS",
            all(
                bool(result["integrity_passed"])
                for result in results.values()
            ),
            sum(
                bool(result["integrity_passed"])
                for result in results.values()
            ),
            4,
        ),
        (
            "acceptance",
            "ALL_QUARTERPOINT_ACCEPTANCE_GATES_PASS",
            all(
                bool(result["acceptance_passed"])
                for result in results.values()
            ),
            sum(
                bool(result["acceptance_passed"])
                for result in results.values()
            ),
            4,
        ),
        (
            "acceptance",
            "BOTH_DOMINANT_TOPOLOGY_BUBBLES_BRACKETED",
            all(
                int(brackets_by_interval[interval_id]) >= 2
                for interval_id in TARGET_INTERVAL_IDS
            ),
            brackets_by_interval,
            "at least 2 signature-change brackets per interval",
        ),
        (
            "acceptance",
            "TRANSITION_BRACKETS_REDUCED_TO_QUARTER_PANEL",
            (
                float(
                    summary[
                        "maximum_transition_bracket_to_parent_width_ratio"
                    ]
                )
                <= 0.25 + 2.0e-15
            ),
            summary[
                "maximum_transition_bracket_to_parent_width_ratio"
            ],
            0.25,
        ),
        (
            "integrity",
            "RICHARDSON_NOT_SMUGGLED_ACROSS_TOPOLOGY_CHANGES",
            all(
                (
                    bool(row["richardson_authorized"])
                    and row[
                        "order512_richardson_error_estimate"
                    ]
                    != ""
                )
                or (
                    not bool(row["richardson_authorized"])
                    and row[
                        "order512_richardson_error_estimate"
                    ]
                    == ""
                )
                for row in two_panel_rows
            ),
            summary["richardson_authorized_interval_count"],
            "estimate present only on topology-uniform intervals",
        ),
        (
            "integrity",
            "ADAPTIVE_VALUE_REMAINS_NONCLAIM",
            not bool(summary["adaptive_value_valid_for_outer_claim"]),
            summary["adaptive_value_valid_for_outer_claim"],
            False,
        ),
        (
            "integrity",
            "FORMALIZATION_WORKBENCH_UNCHANGED",
            len(formal_diff_rows) == 0,
            len(formal_diff_rows),
            0,
        ),
        (
            "integrity",
            "RUNTIME_BOUNDED",
            elapsed <= MAXIMUM_BATCH_RUNTIME_SECONDS,
            elapsed,
            MAXIMUM_BATCH_RUNTIME_SECONDS,
        ),
        (
            "integrity",
            "CLAIMS_REMAIN_FALSE",
            all(
                not bool(manifest["claim_boundary"][field])
                for field in (
                    "valid_for_numeric_UV_claim",
                    "valid_for_local_GR_claim",
                    "valid_for_full_MTS_claim",
                )
            ),
            "false,false,false",
            "false,false,false",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_kind": gate_kind,
            "gate": gate,
            "passed": passed,
            "observed": observed,
            "required": required,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        for gate_kind, gate, passed, observed, required in definitions
    ]


def render_document(
    quarterpoint_rows: list[dict[str, Any]],
    two_panel_rows: list[dict[str, Any]],
    transition_rows: list[dict[str, Any]],
    summary: dict[str, Any],
    decision: str,
) -> str:
    point_lines = [
        (
            f"- `{row['order9_node_id']}` at "
            f"`{float(row['decay_cosine']):.12g}`: "
            f"`({float(row['order512_subtracted_real'])}"
            f"{float(row['order512_subtracted_imaginary']):+}j)`, "
            f"active poles `{row['active_pole_count']}`."
        )
        for row in quarterpoint_rows
    ]
    panel_lines = [
        (
            f"- `{row['interval_id']}` active-count sequence "
            f"`{row['active_pole_counts']}`; topology uniform "
            f"`{row['topology_uniform_across_five_points']}`; "
            f"raw |S2-S1| "
            f"`{float(row['order512_raw_difference_magnitude']):.12g}`; "
            f"Richardson authorized `{row['richardson_authorized']}`."
        )
        for row in two_panel_rows
    ]
    bracket_lines = [
        (
            f"- `{row['transition_id']}`: "
            f"`[{float(row['left_decay_cosine']):.12g}, "
            f"{float(row['right_decay_cosine']):.12g}]`, "
            f"counts `{row['left_active_pole_count']} -> "
            f"{row['right_active_pole_count']}`, next midpoint "
            f"`{float(row['next_bisection_coordinate']):.12g}`."
        )
        for row in transition_rows
    ]
    return "\n".join(
        [
            "# 5254 - Dominant outer quarterpoint topology bracketing",
            "",
            "## Calculation",
            "",
            "Checkpoint 5253 localized more than eighty percent of its "
            "cancellation-safe first-level discrepancy to I01 and I06. "
            "Each interval is now sampled at both quarter points. The "
            "five-point sequence is audited for the canonical active-pole "
            "signature before any smooth Simpson Richardson formula is "
            "allowed.",
            "",
            *point_lines,
            "",
            "## Topology test",
            "",
            *panel_lines,
            "",
            "The topology is not uniform, so `|S2-S1|/15` is deliberately "
            "not reported as an error estimate. The raw difference remains "
            "a diagnostic only.",
            "",
            "## Transition brackets",
            "",
            *bracket_lines,
            "",
            (
                "- Maximum bracket/parent-width ratio: "
                f"`{summary['maximum_transition_bracket_to_parent_width_ratio']:.12g}`."
            ),
            (
                "- Nonclaim two-panel adaptive value (inner 512): "
                f"`({summary['adaptive_two_panel_512_real']}"
                f"{summary['adaptive_two_panel_512_imaginary']:+}j)`."
            ),
            (
                "- Adaptive inner 128/512 relative difference: "
                f"`{summary['adaptive_two_panel_inner128_to512_relative_difference']:.12g}`."
            ),
            "",
            "## Decision",
            "",
            f"`{decision}`",
            "",
            "## Physics boundary",
            "",
            "The large I01/I06 curvature is now identified as a change in "
            "the active causal-residue sector, not merely a high-degree "
            "smooth polynomial. This invalidates blind global-order "
            "escalation and smooth-panel error claims across those regions.",
            "",
            "No numeric p8 coefficient, all-operator local-GR result, or "
            "full-MTS claim is promoted.",
            "",
            "## Next exact target",
            "",
            "Evaluate the four predeclared bisection coordinates in the "
            "transition-bracket table. Continue bracketed bisection until "
            "the outer-boundary location uncertainty times a measured "
            "residue-envelope bound fits inside the allocated outer error "
            "budget. Integrate separately on each constant-topology "
            "chamber.",
            "",
        ]
    )


def execute(max_workers: int) -> dict[str, Any]:
    started = time.perf_counter()
    SOURCE.mkdir(parents=True, exist_ok=True)
    manifest, dry_run = prepare()
    M5251.atomic_json(MANIFEST, manifest)
    M5251.atomic_json(DRY_RUN, dry_run)
    M5251.write_csv(QUARTERPOINT_ROWS, quarterpoint_nodes())
    if not dry_run["dry_run_passed"]:
        failed = [
            key
            for key, passed in dry_run["checks"].items()
            if not passed
        ]
        raise RuntimeError(f"5254 dry run failed: {failed}")

    return_codes = launch_workers(max_workers)
    worker_failures = [
        node_id
        for node_id in TARGET_NODE_IDS
        if return_codes.get(node_id) != 0
        or not M5251.node_paths(node_id)["result"].exists()
    ]
    if worker_failures:
        M5251.atomic_json(
            STATUS,
            {
                "marker": MARKER,
                "status": "FAILED",
                "worker_failures": worker_failures,
                "return_codes": return_codes,
                "elapsed_seconds": time.perf_counter() - started,
            },
        )
        raise RuntimeError(f"5254 workers failed: {worker_failures}")

    results = {
        node_id: node_result(node_id)
        for node_id in TARGET_NODE_IDS
    }
    quarterpoint_rows = build_quarterpoint_rows(results)
    two_panel_rows, transition_rows, summary = analyze_intervals(
        results
    )
    formal_after_rows = M5251.formal_inventory_rows()
    formal_diff_rows = M5251.inventory_diff_rows(
        read_csv(FORMAL_INVENTORY), formal_after_rows
    )
    M5251.write_csv(FORMAL_DIFF, formal_diff_rows)
    elapsed = time.perf_counter() - started
    validations = validation_rows(
        manifest,
        results,
        quarterpoint_rows,
        two_panel_rows,
        transition_rows,
        summary,
        formal_diff_rows,
        elapsed,
    )
    integrity_passed = all(
        bool(row["passed"])
        for row in validations
        if row["gate_kind"] == "integrity"
    )
    acceptance_passed = all(
        bool(row["passed"])
        for row in validations
        if row["gate_kind"] == "acceptance"
    )
    if not integrity_passed:
        decision = "INVALID_DOMINANT_QUARTERPOINT_TOPOLOGY_BRACKETING"
    elif not acceptance_passed:
        decision = (
            "HOLD_DOMINANT_TOPOLOGY_BRACKETS__"
            "LOCALIZE_FAILED_GATE"
        )
    elif summary["all_target_intervals_topology_uniform"]:
        decision = (
            "ADOPT_SMOOTH_DOMINANT_TWO_PANEL_RULE__"
            "RUN_ERROR_BUDGET"
        )
    else:
        decision = (
            "ADOPT_DOMINANT_TOPOLOGY_BRACKETS__"
            "SOLVE_OUTER_BOUNDARIES"
        )
    summary.update(
        {
            "formalization_workbench_start_digest": manifest[
                "formalization_workbench_start_digest"
            ],
            "formalization_workbench_end_digest": (
                M5251.inventory_digest(formal_after_rows)
            ),
            "formalization_workbench_modified_file_count": len(
                formal_diff_rows
            ),
            "elapsed_seconds": elapsed,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
    )
    M5251.write_csv(QUARTERPOINT_ROWS, quarterpoint_rows)
    M5251.write_csv(TWO_PANEL_ROWS, two_panel_rows)
    M5251.write_csv(TOPOLOGY_ROWS, transition_rows)
    M5251.write_csv(VALIDATION, validations)
    M5251.atomic_text(
        DOCUMENT,
        render_document(
            quarterpoint_rows,
            two_panel_rows,
            transition_rows,
            summary,
            decision,
        ),
    )
    result = {
        "marker": MARKER,
        "revision": REVISION,
        "manifest_hash": manifest["manifest_hash"],
        "decision": decision,
        "integrity_passed": integrity_passed,
        "acceptance_passed": acceptance_passed,
        "summary": summary,
        "worker_return_codes": return_codes,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    M5251.atomic_json(RESULT, result)
    M5251.atomic_json(
        STATUS,
        {
            "marker": MARKER,
            "status": "COMPLETE" if integrity_passed else "FAILED",
            "decision": decision,
            "completed_nodes": len(results),
            "total_nodes": len(TARGET_NODE_IDS),
            "return_codes": return_codes,
            "elapsed_seconds": elapsed,
        },
    )
    M5251.atomic_text(
        COMPLETE,
        json.dumps(
            {
                "marker": MARKER,
                "decision": decision,
                "integrity_passed": integrity_passed,
                "acceptance_passed": acceptance_passed,
            },
            sort_keys=True,
        )
        + "\n",
    )
    if not integrity_passed:
        raise RuntimeError("5254 integrity failed")
    return result


def run_single_node(node_id: str) -> dict[str, Any]:
    configure_node_engine()
    result = M5251.run_node(node_id)
    result["summary"]["internal_fixed_field_semantics"] = (
        "ADJACENT_ANCHOR_LINEAR_REFERENCE_DIAGNOSTIC_ONLY"
    )
    result["summary"]["same_coordinate_legacy_baseline_available"] = (
        False
    )
    result["summary"]["legacy_comparison_used_for_acceptance"] = False
    M5251.atomic_json(M5251.node_paths(node_id)["result"], result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-node", choices=TARGET_NODE_IDS)
    parser.add_argument(
        "--max-workers",
        type=int,
        default=DEFAULT_MAX_WORKERS,
    )
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    configure_node_engine()
    if arguments.worker_node:
        result = run_single_node(arguments.worker_node)
        print(json.dumps(result, indent=2, sort_keys=True))
        return
    manifest, dry_run = prepare()
    SOURCE.mkdir(parents=True, exist_ok=True)
    M5251.atomic_json(MANIFEST, manifest)
    M5251.atomic_json(DRY_RUN, dry_run)
    M5251.write_csv(QUARTERPOINT_ROWS, quarterpoint_nodes())
    if arguments.dry_run:
        print(json.dumps(dry_run, indent=2, sort_keys=True))
        if not dry_run["dry_run_passed"]:
            raise SystemExit(1)
        return
    if arguments.max_workers < 1:
        raise ValueError("--max-workers must be positive")
    result = execute(
        min(arguments.max_workers, len(TARGET_NODE_IDS))
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
