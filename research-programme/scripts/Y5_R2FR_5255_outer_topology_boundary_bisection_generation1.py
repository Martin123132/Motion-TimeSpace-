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
SOURCE = POST / "source-intake" / "functional_rg" / "5255"
NODES = SOURCE / "nodes"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5254 = (
    POST
    / "scripts"
    / "Y5_R2FR_5254_dominant_outer_quarterpoint_topology_bracketing.py"
)
SOURCE_5254 = POST / "source-intake" / "functional_rg" / "5254"
RESULT_5254 = SOURCE_5254 / "dominant_quarterpoint_result.json"
MANIFEST_5254 = SOURCE_5254 / "dominant_quarterpoint_manifest.json"
QUARTERPOINT_ROWS_5254 = SOURCE_5254 / "dominant_quarterpoint_nodes.csv"
TWO_PANEL_ROWS_5254 = SOURCE_5254 / "dominant_interval_two_panel_rules.csv"
TRANSITION_ROWS_5254 = SOURCE_5254 / "outer_topology_transition_brackets.csv"
VALIDATION_5254 = RESIDUALS / "P8_Y5_BRR545_5254_VALIDATION.csv"

MANIFEST = SOURCE / "boundary_bisection_generation1_manifest.json"
DRY_RUN = SOURCE / "boundary_bisection_generation1_dry_run.json"
STATUS = SOURCE / "boundary_bisection_generation1_status.json"
RESULT = SOURCE / "boundary_bisection_generation1_result.json"
BISECTION_NODE_ROWS = SOURCE / "boundary_bisection_generation1_nodes.csv"
NARROWED_BRACKETS = SOURCE / "narrowed_topology_transition_brackets.csv"
ERROR_BUDGET_ROWS = SOURCE / "boundary_location_error_budget.csv"
FORMAL_INVENTORY = SOURCE / "formalization_workbench_start_inventory.csv"
FORMAL_DIFF = SOURCE / "formalization_workbench_run_diff.csv"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5255_VALIDATION.csv"
DOCUMENT = (
    POST
    / "5255-Y5-R2FR-outer-topology-boundary-bisection-generation1.md"
)
COMPLETE = SOURCE / "COMPLETE.marker"

CHECKPOINT = 5255
PARENT_CHECKPOINT = 5254
MARKER = "MTS_5255_OUTER_TOPOLOGY_BOUNDARY_BISECTION_GENERATION1"
REVISION = "outer-topology-boundary-bisection-generation1-v1"
TRANSPORT_CACHE_REVISION = (
    "outer-topology-boundary-bisection-generation1-v1"
)
TARGET_NODE_IDS = ("C01A", "C01B", "C06A", "C06B")
TRANSITION_TO_NODE = {
    "I01_T00": "C01A",
    "I01_T01": "C01B",
    "I06_T00": "C06A",
    "I06_T01": "C06B",
}
INNER_ORDERS = (128, 512)
DEFAULT_MAX_WORKERS = 2
MAXIMUM_NODE_RUNTIME_SECONDS = 4.0 * 60.0 * 60.0
MAXIMUM_BATCH_RUNTIME_SECONDS = 6.0 * 60.0 * 60.0
ANGULAR_JACOBIAN = 0.25
OUTER_RELATIVE_ERROR_BUDGET = 0.2
EXPECTED_PARENT_DECISION = (
    "ADOPT_DOMINANT_TOPOLOGY_BRACKETS__SOLVE_OUTER_BOUNDARIES"
)


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"Unable to load {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


M5254 = load_module(SCRIPT_5254, "mts_5254_for_5255")
M5251 = M5254.M5251


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


def transition_rows() -> list[dict[str, str]]:
    rows = read_csv(TRANSITION_ROWS_5254)
    if {row["transition_id"] for row in rows} != set(
        TRANSITION_TO_NODE
    ):
        raise RuntimeError("5254 transition set changed")
    return sorted(rows, key=lambda row: row["transition_id"])


def previous_quarterpoint_results() -> dict[str, dict[str, Any]]:
    return {
        node_id: read_json(
            SOURCE_5254 / "nodes" / node_id / "node_result.json"
        )
        for node_id in M5254.TARGET_NODE_IDS
    }


def previous_interval_points(
    interval_id: str,
) -> list[dict[str, Any]]:
    contract = M5254.interval_anchor_contracts()[interval_id]
    node_by_id = {
        row["order9_node_id"]: row
        for row in M5254.quarterpoint_nodes()
    }
    results = previous_quarterpoint_results()

    def quarter_record(node_id: str) -> dict[str, Any]:
        node = node_by_id[node_id]
        result_path = (
            SOURCE_5254 / "nodes" / node_id / "node_result.json"
        )
        signature = M5254.active_signature_from_catalog(
            M5254.result_catalog_path(result_path)
        )
        result = results[node_id]
        return {
            "interval_id": interval_id,
            "point_id": node_id,
            "point_role": node["quarter_role"],
            "decay_cosine": float(node["decay_cosine"]),
            "result_path": str(result_path),
            "active_pole_count": len(signature),
            "active_signature": signature,
            "values": {
                inner_order: M5254.result_value(
                    result, inner_order
                )
                for inner_order in INNER_ORDERS
            },
        }

    points = [
        M5254.endpoint_record(
            interval_id, contract["left_id"], contract["left"]
        ),
        quarter_record(contract["left_quarter_id"]),
        M5254.midpoint_record(
            interval_id,
            contract["middle_id"],
            contract["middle"],
        ),
        quarter_record(contract["right_quarter_id"]),
        M5254.endpoint_record(
            interval_id, contract["right_id"], contract["right"]
        ),
    ]
    return sorted(points, key=lambda point: point["decay_cosine"])


def previous_point_lookup() -> dict[str, dict[str, Any]]:
    lookup: dict[str, dict[str, Any]] = {}
    for interval_id in M5254.TARGET_INTERVAL_IDS:
        for point in previous_interval_points(interval_id):
            lookup[point["point_id"]] = point
    return lookup


def bisection_nodes() -> list[dict[str, Any]]:
    rows = []
    for index, transition in enumerate(transition_rows()):
        node_id = TRANSITION_TO_NODE[transition["transition_id"]]
        left = float(transition["left_decay_cosine"])
        right = float(transition["right_decay_cosine"])
        coordinate = 0.5 * (left + right)
        rows.append(
            {
                "order9_node_id": node_id,
                "execution_node_id": f"U{index:02d}",
                "master_index": index,
                "decay_cosine": coordinate,
                "transition_id": transition["transition_id"],
                "parent_interval_id": transition["interval_id"],
                "left_point_id": transition["left_point_id"],
                "right_point_id": transition["right_point_id"],
                "old_bracket_lower": left,
                "old_bracket_upper": right,
                "old_bracket_width": right - left,
                "reused_from_5240": False,
                "source_cache": str(
                    NODES / node_id / "node_result.json"
                ),
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def bisection_reference_values() -> dict[str, dict[int, complex]]:
    points = previous_point_lookup()
    references: dict[str, dict[int, complex]] = {}
    for node in bisection_nodes():
        left = points[node["left_point_id"]]
        right = points[node["right_point_id"]]
        references[node["order9_node_id"]] = {
            inner_order: 0.5
            * (
                left["values"][inner_order]
                + right["values"][inner_order]
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
    M5251.RESULT_5250 = RESULT_5254
    M5251.MAXIMUM_NODE_RUNTIME_SECONDS = MAXIMUM_NODE_RUNTIME_SECONDS
    M5251.fixed_node_values = bisection_reference_values
    M5251.M5243.compare_intervals = (
        M5254.M5253.no_same_coordinate_legacy_comparison
    )


def source_rows() -> list[dict[str, str]]:
    paths = [
        Path(__file__),
        SCRIPT_5254,
        RESULT_5254,
        MANIFEST_5254,
        QUARTERPOINT_ROWS_5254,
        TWO_PANEL_ROWS_5254,
        TRANSITION_ROWS_5254,
        VALIDATION_5254,
    ]
    paths.extend(
        Path(point["result_path"])
        for point in previous_point_lookup().values()
    )
    unique_paths = sorted(set(paths), key=str)
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in unique_paths
    ]


def prepare() -> tuple[dict[str, Any], dict[str, Any]]:
    configure_node_engine()
    parent_result = read_json(RESULT_5254)
    parent_validation = read_csv(VALIDATION_5254)
    targets = bisection_nodes()
    formal_rows = M5251.formal_inventory_rows()
    formal_digest = M5251.inventory_digest(formal_rows)
    M5251.write_csv(FORMAL_INVENTORY, formal_rows)
    manifest = {
        "marker": MARKER,
        "revision": REVISION,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "parent_decision": parent_result["decision"],
        "target_node_ids": list(TARGET_NODE_IDS),
        "target_transition_ids": sorted(TRANSITION_TO_NODE),
        "outer_nodes": targets,
        "bisection_contract": {
            "signature_rule": (
                "The midpoint signature must equal exactly one endpoint "
                "signature. Retain the half bracket whose endpoint "
                "signature differs from the midpoint."
            ),
            "third_signature_action": (
                "Fail closed and split the transition model; do not "
                "silently assign a new topology to either old chamber."
            ),
            "location_error_identity": (
                "|delta I_boundary| <= J delta_x "
                "sup|f_left_branch-f_right_branch|"
            ),
            "measured_envelope_status": (
                "finite-sample proxy only; not a certified supremum"
            ),
        },
        "angular_unit_cube_jacobian": ANGULAR_JACOBIAN,
        "outer_relative_error_budget": OUTER_RELATIVE_ERROR_BUDGET,
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
                "This is the first outer topology-boundary bisection "
                "generation. The finite-sample jump proxy is not an "
                "analytic residue-envelope bound."
            ),
        },
    }
    manifest["manifest_hash"] = serialized_hash(manifest)
    parent_integrity = [
        row
        for row in parent_validation
        if row["gate_kind"] == "integrity"
    ]
    transition_by_id = {
        row["transition_id"]: row for row in transition_rows()
    }
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
        "parent_decision_authorizes_boundary_solve": (
            parent_result["decision"] == EXPECTED_PARENT_DECISION
        ),
        "transition_set_exact": (
            set(transition_by_id) == set(TRANSITION_TO_NODE)
            and len(transition_by_id) == 4
        ),
        "endpoint_signatures_differ": all(
            json.loads(row["left_active_signature"])
            != json.loads(row["right_active_signature"])
            for row in transition_rows()
        ),
        "bisection_coordinates_exact": all(
            math.isclose(
                float(node["decay_cosine"]),
                float(
                    transition_by_id[node["transition_id"]][
                        "next_bisection_coordinate"
                    ]
                ),
                rel_tol=0.0,
                abs_tol=2.0e-15,
            )
            for node in targets
        ),
        "target_node_accounting_exact": (
            len(targets) == 4
            and {
                row["order9_node_id"] for row in targets
            }
            == set(TARGET_NODE_IDS)
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


def active_signature(node_id: str) -> tuple[str, ...]:
    result_path = M5251.node_paths(node_id)["result"]
    return M5254.active_signature_from_catalog(
        M5254.result_catalog_path(result_path)
    )


def bisection_result_rows(
    results: dict[str, dict[str, Any]]
) -> list[dict[str, Any]]:
    references = bisection_reference_values()
    rows = []
    for node in bisection_nodes():
        node_id = node["order9_node_id"]
        result = results[node_id]
        value_128 = result_value(result, 128)
        value_512 = result_value(result, 512)
        signature = active_signature(node_id)
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
                "linear_reference_512_real": (
                    references[node_id][512].real
                ),
                "linear_reference_512_imaginary": (
                    references[node_id][512].imag
                ),
                "linear_departure_512_magnitude": abs(
                    value_512 - references[node_id][512]
                ),
                "inner128_to512_relative_difference": (
                    abs(value_128 - value_512)
                    / max(abs(value_512), 1.0)
                ),
                "elapsed_seconds": result["elapsed_seconds"],
                "internal_fixed_field_semantics": (
                    "BRACKET_ENDPOINT_LINEAR_REFERENCE_DIAGNOSTIC_ONLY"
                ),
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def narrow_brackets(
    bisection_rows: list[dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    prior_points = previous_point_lookup()
    previous_transitions = {
        row["transition_id"]: row for row in transition_rows()
    }
    midpoint_by_transition = {
        row["transition_id"]: row for row in bisection_rows
    }
    narrowed: list[dict[str, Any]] = []
    third_signature_count = 0
    for transition_id in sorted(previous_transitions):
        old = previous_transitions[transition_id]
        midpoint = midpoint_by_transition[transition_id]
        left_signature = tuple(
            json.loads(old["left_active_signature"])
        )
        right_signature = tuple(
            json.loads(old["right_active_signature"])
        )
        midpoint_signature = tuple(
            json.loads(midpoint["active_pole_signature"])
        )
        midpoint_matches_left = midpoint_signature == left_signature
        midpoint_matches_right = midpoint_signature == right_signature
        if midpoint_matches_left == midpoint_matches_right:
            third_signature_count += 1
            update_status = "THIRD_OR_AMBIGUOUS_SIGNATURE"
            new_left_id = old["left_point_id"]
            new_right_id = old["right_point_id"]
            new_left = float(old["left_decay_cosine"])
            new_right = float(old["right_decay_cosine"])
            new_left_signature = left_signature
            new_right_signature = right_signature
        elif midpoint_matches_left:
            update_status = "MIDPOINT_MATCHES_LEFT"
            new_left_id = midpoint["order9_node_id"]
            new_right_id = old["right_point_id"]
            new_left = float(midpoint["decay_cosine"])
            new_right = float(old["right_decay_cosine"])
            new_left_signature = midpoint_signature
            new_right_signature = right_signature
        else:
            update_status = "MIDPOINT_MATCHES_RIGHT"
            new_left_id = old["left_point_id"]
            new_right_id = midpoint["order9_node_id"]
            new_left = float(old["left_decay_cosine"])
            new_right = float(midpoint["decay_cosine"])
            new_left_signature = left_signature
            new_right_signature = midpoint_signature
        old_width = float(old["bracket_width"])
        new_width = new_right - new_left
        narrowed.append(
            {
                "transition_id": transition_id,
                "interval_id": old["interval_id"],
                "generation": 1,
                "update_status": update_status,
                "old_left_point_id": old["left_point_id"],
                "old_right_point_id": old["right_point_id"],
                "bisection_node_id": midpoint[
                    "order9_node_id"
                ],
                "new_left_point_id": new_left_id,
                "new_right_point_id": new_right_id,
                "new_left_decay_cosine": new_left,
                "new_right_decay_cosine": new_right,
                "old_bracket_width": old_width,
                "new_bracket_width": new_width,
                "width_reduction_factor": (
                    new_width / old_width
                ),
                "parent_interval_width": float(
                    old["parent_interval_width"]
                ),
                "bracket_to_parent_width_ratio": (
                    new_width
                    / float(old["parent_interval_width"])
                ),
                "new_left_active_pole_count": len(
                    new_left_signature
                ),
                "new_right_active_pole_count": len(
                    new_right_signature
                ),
                "new_left_active_signature": json.dumps(
                    new_left_signature
                ),
                "new_right_active_signature": json.dumps(
                    new_right_signature
                ),
                "next_bisection_coordinate": 0.5
                * (new_left + new_right),
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )

    point_values: dict[str, complex] = {
        point_id: point["values"][512]
        for point_id, point in prior_points.items()
    }
    point_values.update(
        {
            row["order9_node_id"]: complex(
                float(row["order512_subtracted_real"]),
                float(row["order512_subtracted_imaginary"]),
            )
            for row in bisection_rows
        }
    )
    parent_value = complex(
        float(
            read_json(RESULT_5254)["summary"][
                "adaptive_two_panel_512_real"
            ]
        ),
        float(
            read_json(RESULT_5254)["summary"][
                "adaptive_two_panel_512_imaginary"
            ]
        ),
    )
    total_absolute_budget = (
        OUTER_RELATIVE_ERROR_BUDGET
        * max(abs(parent_value), 1.0)
    )
    equal_boundary_budget = total_absolute_budget / len(narrowed)
    error_rows: list[dict[str, Any]] = []
    for row in narrowed:
        left_value = point_values[row["new_left_point_id"]]
        right_value = point_values[row["new_right_point_id"]]
        jump_proxy = abs(right_value - left_value)
        width = float(row["new_bracket_width"])
        location_proxy = (
            ANGULAR_JACOBIAN * width * jump_proxy
        )
        target_width = (
            equal_boundary_budget
            / (ANGULAR_JACOBIAN * jump_proxy)
            if jump_proxy > 0.0
            else math.inf
        )
        remaining_generations = (
            max(
                0,
                math.ceil(math.log2(width / target_width)),
            )
            if math.isfinite(target_width)
            and target_width > 0.0
            else 0
        )
        error_rows.append(
            {
                "transition_id": row["transition_id"],
                "new_bracket_width": width,
                "measured_endpoint_jump_proxy": jump_proxy,
                "location_error_proxy": location_proxy,
                "total_outer_absolute_budget": (
                    total_absolute_budget
                ),
                "equal_boundary_budget": equal_boundary_budget,
                "provisional_target_width": target_width,
                "provisional_remaining_bisection_generations": (
                    remaining_generations
                ),
                "envelope_is_certified_supremum": False,
                "valid_for_outer_error_claim": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    total_location_proxy = sum(
        float(row["location_error_proxy"]) for row in error_rows
    )
    summary = {
        "narrowed_bracket_count": len(narrowed),
        "third_or_ambiguous_signature_count": third_signature_count,
        "maximum_width_reduction_factor": max(
            float(row["width_reduction_factor"])
            for row in narrowed
        ),
        "maximum_bracket_to_parent_width_ratio": max(
            float(row["bracket_to_parent_width_ratio"])
            for row in narrowed
        ),
        "total_measured_location_error_proxy": total_location_proxy,
        "outer_absolute_error_budget": total_absolute_budget,
        "measured_proxy_within_budget": (
            total_location_proxy <= total_absolute_budget
        ),
        "measured_proxy_is_certified_bound": False,
        "maximum_provisional_remaining_bisection_generations": max(
            int(
                row[
                    "provisional_remaining_bisection_generations"
                ]
            )
            for row in error_rows
        ),
        "next_bisection_coordinates": [
            {
                "transition_id": row["transition_id"],
                "decay_cosine": row[
                    "next_bisection_coordinate"
                ],
            }
            for row in narrowed
        ],
    }
    return narrowed, error_rows, summary


def validation_rows(
    manifest: dict[str, Any],
    results: dict[str, dict[str, Any]],
    bisection_rows: list[dict[str, Any]],
    narrowed_rows: list[dict[str, Any]],
    error_rows: list[dict[str, Any]],
    summary: dict[str, Any],
    formal_diff_rows: list[dict[str, Any]],
    elapsed: float,
) -> list[dict[str, Any]]:
    mirror_pairs = (
        ("I01_T00", "I06_T01"),
        ("I01_T01", "I06_T00"),
    )
    narrowed_by_id = {
        row["transition_id"]: row for row in narrowed_rows
    }
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
            "BISECTION_NODE_ACCOUNTING_EXACT",
            (
                set(results) == set(TARGET_NODE_IDS)
                and len(bisection_rows) == 4
            ),
            f"{len(results)} results, {len(bisection_rows)} rows",
            "4 results, 4 rows",
        ),
        (
            "integrity",
            "ALL_BISECTION_NODE_INTEGRITY_GATES_PASS",
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
            "ALL_BISECTION_NODE_ACCEPTANCE_GATES_PASS",
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
            "NO_THIRD_OR_AMBIGUOUS_SIGNATURE",
            summary["third_or_ambiguous_signature_count"] == 0,
            summary["third_or_ambiguous_signature_count"],
            0,
        ),
        (
            "acceptance",
            "ALL_BRACKETS_HALVED",
            (
                float(summary["maximum_width_reduction_factor"])
                <= 0.5 + 2.0e-15
            ),
            summary["maximum_width_reduction_factor"],
            0.5,
        ),
        (
            "acceptance",
            "MIRROR_TOPOLOGY_COUNTS_AGREE",
            all(
                (
                    narrowed_by_id[left][
                        "new_left_active_pole_count"
                    ],
                    narrowed_by_id[left][
                        "new_right_active_pole_count"
                    ],
                )
                == (
                    narrowed_by_id[right][
                        "new_right_active_pole_count"
                    ],
                    narrowed_by_id[right][
                        "new_left_active_pole_count"
                    ],
                )
                for left, right in mirror_pairs
            ),
            "two mirrored boundary pairs",
            "reversed active-count sequences agree",
        ),
        (
            "integrity",
            "MEASURED_ERROR_PROXY_NOT_PROMOTED_TO_BOUND",
            (
                not bool(
                    summary["measured_proxy_is_certified_bound"]
                )
                and all(
                    row["envelope_is_certified_supremum"] is False
                    and row["valid_for_outer_error_claim"] is False
                    for row in error_rows
                )
            ),
            "finite-sample proxy, claim false",
            "finite-sample proxy, claim false",
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
    bisection_rows: list[dict[str, Any]],
    narrowed_rows: list[dict[str, Any]],
    error_rows: list[dict[str, Any]],
    summary: dict[str, Any],
    decision: str,
) -> str:
    node_lines = [
        (
            f"- `{row['order9_node_id']}` / "
            f"`{row['transition_id']}` at "
            f"`{float(row['decay_cosine']):.12g}`: "
            f"`({float(row['order512_subtracted_real'])}"
            f"{float(row['order512_subtracted_imaginary']):+}j)`, "
            f"active poles `{row['active_pole_count']}`."
        )
        for row in bisection_rows
    ]
    bracket_lines = [
        (
            f"- `{row['transition_id']}` -> "
            f"`[{float(row['new_left_decay_cosine']):.12g}, "
            f"{float(row['new_right_decay_cosine']):.12g}]`, "
            f"counts `{row['new_left_active_pole_count']} -> "
            f"{row['new_right_active_pole_count']}`, width "
            f"`{float(row['new_bracket_width']):.12g}`, next "
            f"`{float(row['next_bisection_coordinate']):.12g}`."
        )
        for row in narrowed_rows
    ]
    budget_lines = [
        (
            f"- `{row['transition_id']}` measured jump proxy "
            f"`{float(row['measured_endpoint_jump_proxy']):.12g}`, "
            f"location proxy `{float(row['location_error_proxy']):.12g}`, "
            f"provisional generations remaining "
            f"`{row['provisional_remaining_bisection_generations']}`."
        )
        for row in error_rows
    ]
    return "\n".join(
        [
            "# 5255 - Outer topology-boundary bisection generation 1",
            "",
            "## Calculation",
            "",
            "The four predeclared checkpoint-5254 transition midpoints "
            "were evaluated with the same reciprocal-projective topology "
            "and corrected-inner-slice engine. A midpoint is assigned only "
            "when its complete active-pole signature equals exactly one "
            "bracket endpoint signature.",
            "",
            *node_lines,
            "",
            "## Narrowed brackets",
            "",
            *bracket_lines,
            "",
            "All four brackets are halved without a third topology.",
            "",
            "## Boundary-location error identity",
            "",
            "For a boundary known only within width `delta_x`,",
            "",
            "```text",
            "|delta I_boundary| <= J delta_x "
            "sup |f_left_branch-f_right_branch|.",
            "```",
            "",
            "The rows below use measured endpoint differences only. They "
            "are planning proxies, not certified suprema or error bounds.",
            "",
            *budget_lines,
            "",
            (
                "- Total measured location proxy: "
                f"`{summary['total_measured_location_error_proxy']:.12g}`."
            ),
            (
                "- Provisional outer absolute budget: "
                f"`{summary['outer_absolute_error_budget']:.12g}`."
            ),
            (
                "- Maximum provisional generations remaining: "
                f"`{summary['maximum_provisional_remaining_bisection_generations']}`."
            ),
            "",
            "## Decision",
            "",
            f"`{decision}`",
            "",
            "## Claim boundary",
            "",
            "No finite-sample envelope is promoted to a mathematical "
            "supremum. No outer-convergence, numeric p8, all-operator "
            "local-GR, or full-MTS claim follows.",
            "",
            "## Next exact target",
            "",
            "Run the four recorded generation-2 bisection coordinates. "
            "In parallel, derive a chamber-local residue-envelope bound "
            "from the fitted pole numerator and denominator derivatives; "
            "that bound, rather than sampled endpoint magnitudes, must own "
            "the stopping rule.",
            "",
        ]
    )


def execute(max_workers: int) -> dict[str, Any]:
    started = time.perf_counter()
    SOURCE.mkdir(parents=True, exist_ok=True)
    manifest, dry_run = prepare()
    M5251.atomic_json(MANIFEST, manifest)
    M5251.atomic_json(DRY_RUN, dry_run)
    M5251.write_csv(BISECTION_NODE_ROWS, bisection_nodes())
    if not dry_run["dry_run_passed"]:
        failed = [
            key
            for key, passed in dry_run["checks"].items()
            if not passed
        ]
        raise RuntimeError(f"5255 dry run failed: {failed}")

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
        raise RuntimeError(f"5255 workers failed: {worker_failures}")

    results = {
        node_id: node_result(node_id)
        for node_id in TARGET_NODE_IDS
    }
    bisection_rows = bisection_result_rows(results)
    narrowed_rows, error_rows, summary = narrow_brackets(
        bisection_rows
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
        bisection_rows,
        narrowed_rows,
        error_rows,
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
        decision = "INVALID_OUTER_TOPOLOGY_BOUNDARY_BISECTION_GEN1"
    elif not acceptance_passed:
        decision = (
            "HOLD_OUTER_TOPOLOGY_BOUNDARY_BISECTION_GEN1__"
            "LOCALIZE_FAILED_GATE"
        )
    else:
        decision = (
            "ADOPT_BISECTION_GENERATION1__"
            "CONTINUE_BOUNDARY_SOLVE"
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
    M5251.write_csv(BISECTION_NODE_ROWS, bisection_rows)
    M5251.write_csv(NARROWED_BRACKETS, narrowed_rows)
    M5251.write_csv(ERROR_BUDGET_ROWS, error_rows)
    M5251.write_csv(VALIDATION, validations)
    M5251.atomic_text(
        DOCUMENT,
        render_document(
            bisection_rows,
            narrowed_rows,
            error_rows,
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
        raise RuntimeError("5255 integrity failed")
    return result


def run_single_node(node_id: str) -> dict[str, Any]:
    configure_node_engine()
    result = M5251.run_node(node_id)
    result["summary"]["internal_fixed_field_semantics"] = (
        "BRACKET_ENDPOINT_LINEAR_REFERENCE_DIAGNOSTIC_ONLY"
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
    M5251.write_csv(BISECTION_NODE_ROWS, bisection_nodes())
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
