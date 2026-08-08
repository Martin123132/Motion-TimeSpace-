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
SOURCE = POST / "source-intake" / "functional_rg" / "5256"
NODES = SOURCE / "nodes"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5255 = (
    POST
    / "scripts"
    / "Y5_R2FR_5255_outer_topology_boundary_bisection_generation1.py"
)
SOURCE_5255 = POST / "source-intake" / "functional_rg" / "5255"
RESULT_5255 = SOURCE_5255 / "boundary_bisection_generation1_result.json"
MANIFEST_5255 = (
    SOURCE_5255 / "boundary_bisection_generation1_manifest.json"
)
NODE_ROWS_5255 = SOURCE_5255 / "boundary_bisection_generation1_nodes.csv"
BRACKETS_5255 = SOURCE_5255 / "narrowed_topology_transition_brackets.csv"
ERROR_ROWS_5255 = SOURCE_5255 / "boundary_location_error_budget.csv"
VALIDATION_5255 = RESIDUALS / "P8_Y5_BRR545_5255_VALIDATION.csv"

MANIFEST = SOURCE / "boundary_bisection_generation2_manifest.json"
DRY_RUN = SOURCE / "boundary_bisection_generation2_dry_run.json"
STATUS = SOURCE / "boundary_bisection_generation2_status.json"
RESULT = SOURCE / "boundary_bisection_generation2_result.json"
BISECTION_ROWS = SOURCE / "boundary_bisection_generation2_nodes.csv"
NARROWED_BRACKETS = SOURCE / "narrowed_topology_transition_brackets.csv"
RESIDUE_BOUND_ROWS = SOURCE / "half_residue_envelope_audit.csv"
ERROR_BUDGET_ROWS = SOURCE / "boundary_location_error_budget.csv"
FORMAL_INVENTORY = SOURCE / "formalization_workbench_start_inventory.csv"
FORMAL_DIFF = SOURCE / "formalization_workbench_run_diff.csv"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5256_VALIDATION.csv"
DOCUMENT = (
    POST
    / "5256-Y5-R2FR-outer-topology-bisection-generation2-and-half-residue-bound.md"
)
COMPLETE = SOURCE / "COMPLETE.marker"

CHECKPOINT = 5256
PARENT_CHECKPOINT = 5255
MARKER = (
    "MTS_5256_OUTER_TOPOLOGY_BISECTION_GENERATION2_"
    "AND_HALF_RESIDUE_BOUND"
)
REVISION = "outer-topology-bisection-generation2-half-residue-bound-v1"
TRANSPORT_CACHE_REVISION = (
    "outer-topology-bisection-generation2-half-residue-bound-v1"
)
TARGET_NODE_IDS = ("D01A", "D01B", "D06A", "D06B")
TRANSITION_TO_NODE = {
    "I01_T00": "D01A",
    "I01_T01": "D01B",
    "I06_T00": "D06A",
    "I06_T01": "D06B",
}
INNER_ORDERS = (128, 512)
DEFAULT_MAX_WORKERS = 2
MAXIMUM_NODE_RUNTIME_SECONDS = 4.0 * 60.0 * 60.0
MAXIMUM_BATCH_RUNTIME_SECONDS = 6.0 * 60.0 * 60.0
ANGULAR_JACOBIAN = 0.25
OUTER_RELATIVE_ERROR_BUDGET = 0.2
MAXIMUM_HALF_RESIDUE_IMAGINARY_RELATIVE_RESIDUAL = 2.0e-4
EXPECTED_PARENT_DECISION = (
    "ADOPT_BISECTION_GENERATION1__CONTINUE_BOUNDARY_SOLVE"
)


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"Unable to load {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


M5255 = load_module(SCRIPT_5255, "mts_5255_for_5256")
M5254 = M5255.M5254
M5251 = M5255.M5251
M5231 = M5251.M5239.M5231


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


def prior_bracket_rows() -> list[dict[str, str]]:
    rows = read_csv(BRACKETS_5255)
    if {row["transition_id"] for row in rows} != set(
        TRANSITION_TO_NODE
    ):
        raise RuntimeError("5255 transition set changed")
    return sorted(rows, key=lambda row: row["transition_id"])


def generation1_point_records() -> dict[str, dict[str, Any]]:
    records = dict(M5255.previous_point_lookup())
    for row in read_csv(NODE_ROWS_5255):
        node_id = row["order9_node_id"]
        result_path = (
            SOURCE_5255 / "nodes" / node_id / "node_result.json"
        )
        signature = M5254.active_signature_from_catalog(
            M5254.result_catalog_path(result_path)
        )
        result = read_json(result_path)
        records[node_id] = {
            "interval_id": row["parent_interval_id"],
            "point_id": node_id,
            "point_role": "BISECTION_GENERATION1",
            "decay_cosine": float(row["decay_cosine"]),
            "result_path": str(result_path),
            "active_pole_count": len(signature),
            "active_signature": signature,
            "values": {
                inner_order: M5255.result_value(
                    result, inner_order
                )
                for inner_order in INNER_ORDERS
            },
        }
    return records


def bisection_nodes() -> list[dict[str, Any]]:
    rows = []
    for index, bracket in enumerate(prior_bracket_rows()):
        node_id = TRANSITION_TO_NODE[bracket["transition_id"]]
        lower = float(bracket["new_left_decay_cosine"])
        upper = float(bracket["new_right_decay_cosine"])
        rows.append(
            {
                "order9_node_id": node_id,
                "execution_node_id": f"V{index:02d}",
                "master_index": index,
                "decay_cosine": 0.5 * (lower + upper),
                "transition_id": bracket["transition_id"],
                "parent_interval_id": bracket["interval_id"],
                "left_point_id": bracket["new_left_point_id"],
                "right_point_id": bracket["new_right_point_id"],
                "old_bracket_lower": lower,
                "old_bracket_upper": upper,
                "old_bracket_width": upper - lower,
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
    points = generation1_point_records()
    return {
        node["order9_node_id"]: {
            inner_order: 0.5
            * (
                points[node["left_point_id"]]["values"][
                    inner_order
                ]
                + points[node["right_point_id"]]["values"][
                    inner_order
                ]
            )
            for inner_order in INNER_ORDERS
        }
        for node in bisection_nodes()
    }


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
    M5251.RESULT_5250 = RESULT_5255
    M5251.MAXIMUM_NODE_RUNTIME_SECONDS = MAXIMUM_NODE_RUNTIME_SECONDS
    M5251.fixed_node_values = bisection_reference_values
    M5251.M5243.compare_intervals = (
        M5254.M5253.no_same_coordinate_legacy_comparison
    )


def source_rows() -> list[dict[str, str]]:
    paths = [
        Path(__file__),
        SCRIPT_5255,
        RESULT_5255,
        MANIFEST_5255,
        NODE_ROWS_5255,
        BRACKETS_5255,
        ERROR_ROWS_5255,
        VALIDATION_5255,
        Path(M5231.__file__),
        Path(M5251.M5239.__file__),
    ]
    paths.extend(
        Path(point["result_path"])
        for point in generation1_point_records().values()
    )
    unique_paths = sorted(set(paths), key=str)
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in unique_paths
    ]


def half_residue_coefficient() -> float:
    physical_multiplier = (
        M5231.PHYSICAL_A00_WEIGHT * M5231.KERNEL_MULTIPLIER
    )
    return math.pi * abs(float(physical_multiplier))


def prepare() -> tuple[dict[str, Any], dict[str, Any]]:
    configure_node_engine()
    parent_result = read_json(RESULT_5255)
    parent_validation = read_csv(VALIDATION_5255)
    targets = bisection_nodes()
    coefficient = half_residue_coefficient()
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
        "half_residue_bound": {
            "physical_multiplier": (
                M5231.PHYSICAL_A00_WEIGHT
                * M5231.KERNEL_MULTIPLIER
            ),
            "physical_A00_weight": M5231.PHYSICAL_A00_WEIGHT,
            "kernel_multiplier": M5231.KERNEL_MULTIPLIER,
            "sokhotski_plemelj_factor": "pi",
            "absolute_jump_coefficient": coefficient,
            "regulator_combination": "2 R_E020 - R_E040",
            "residue_identity": "R_epsilon=N_epsilon/D'_epsilon",
            "jump_identity": (
                "Delta f=-i*pi*(P_A00*K)*(2 R_E020-R_E040)"
            ),
            "chamber_envelope_inequality": (
                "sup|Delta f| <= pi|P_A00 K| "
                "(2 sup|N20|/inf|D20'| + "
                "sup|N40|/inf|D40'|)"
            ),
            "boundary_location_inequality": (
                "|delta I_b| <= J delta_x sup|Delta f|"
            ),
            "continuous_enclosure_required": True,
        },
        "angular_unit_cube_jacobian": ANGULAR_JACOBIAN,
        "outer_relative_error_budget": OUTER_RELATIVE_ERROR_BUDGET,
        "maximum_half_residue_imaginary_relative_residual": (
            MAXIMUM_HALF_RESIDUE_IMAGINARY_RELATIVE_RESIDUAL
        ),
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
                "The half-residue inequality is derived, but continuous "
                "interval enclosures of N and D' over each boundary "
                "chamber are not yet supplied."
            ),
        },
    }
    manifest["manifest_hash"] = serialized_hash(manifest)
    parent_integrity = [
        row
        for row in parent_validation
        if row["gate_kind"] == "integrity"
    ]
    brackets_by_id = {
        row["transition_id"]: row for row in prior_bracket_rows()
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
        "parent_decision_authorizes_generation2": (
            parent_result["decision"] == EXPECTED_PARENT_DECISION
        ),
        "transition_set_exact": (
            set(brackets_by_id) == set(TRANSITION_TO_NODE)
            and len(brackets_by_id) == 4
        ),
        "endpoint_signatures_differ": all(
            json.loads(row["new_left_active_signature"])
            != json.loads(row["new_right_active_signature"])
            for row in prior_bracket_rows()
        ),
        "bisection_coordinates_exact": all(
            math.isclose(
                float(node["decay_cosine"]),
                float(
                    brackets_by_id[node["transition_id"]][
                        "next_bisection_coordinate"
                    ]
                ),
                rel_tol=0.0,
                abs_tol=2.0e-15,
            )
            for node in targets
        ),
        "half_residue_coefficient_exact": math.isclose(
            coefficient, 0.016, rel_tol=0.0, abs_tol=2.0e-15
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
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    old_by_id = {
        row["transition_id"]: row for row in prior_bracket_rows()
    }
    midpoint_by_id = {
        row["transition_id"]: row for row in bisection_rows
    }
    rows: list[dict[str, Any]] = []
    third_signature_count = 0
    for transition_id in sorted(old_by_id):
        old = old_by_id[transition_id]
        midpoint = midpoint_by_id[transition_id]
        left_signature = tuple(
            json.loads(old["new_left_active_signature"])
        )
        right_signature = tuple(
            json.loads(old["new_right_active_signature"])
        )
        midpoint_signature = tuple(
            json.loads(midpoint["active_pole_signature"])
        )
        matches_left = midpoint_signature == left_signature
        matches_right = midpoint_signature == right_signature
        if matches_left == matches_right:
            third_signature_count += 1
            status = "THIRD_OR_AMBIGUOUS_SIGNATURE"
            left_id = old["new_left_point_id"]
            right_id = old["new_right_point_id"]
            lower = float(old["new_left_decay_cosine"])
            upper = float(old["new_right_decay_cosine"])
            retained_left_signature = left_signature
            retained_right_signature = right_signature
        elif matches_left:
            status = "MIDPOINT_MATCHES_LEFT"
            left_id = midpoint["order9_node_id"]
            right_id = old["new_right_point_id"]
            lower = float(midpoint["decay_cosine"])
            upper = float(old["new_right_decay_cosine"])
            retained_left_signature = midpoint_signature
            retained_right_signature = right_signature
        else:
            status = "MIDPOINT_MATCHES_RIGHT"
            left_id = old["new_left_point_id"]
            right_id = midpoint["order9_node_id"]
            lower = float(old["new_left_decay_cosine"])
            upper = float(midpoint["decay_cosine"])
            retained_left_signature = left_signature
            retained_right_signature = midpoint_signature
        old_width = float(old["new_bracket_width"])
        new_width = upper - lower
        rows.append(
            {
                "transition_id": transition_id,
                "interval_id": old["interval_id"],
                "generation": 2,
                "update_status": status,
                "bisection_node_id": midpoint[
                    "order9_node_id"
                ],
                "new_left_point_id": left_id,
                "new_right_point_id": right_id,
                "new_left_decay_cosine": lower,
                "new_right_decay_cosine": upper,
                "old_bracket_width": old_width,
                "new_bracket_width": new_width,
                "width_reduction_factor": new_width / old_width,
                "parent_interval_width": float(
                    old["parent_interval_width"]
                ),
                "bracket_to_parent_width_ratio": (
                    new_width
                    / float(old["parent_interval_width"])
                ),
                "new_left_active_pole_count": len(
                    retained_left_signature
                ),
                "new_right_active_pole_count": len(
                    retained_right_signature
                ),
                "new_left_active_signature": json.dumps(
                    retained_left_signature
                ),
                "new_right_active_signature": json.dumps(
                    retained_right_signature
                ),
                "next_bisection_coordinate": 0.5
                * (lower + upper),
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    summary = {
        "narrowed_bracket_count": len(rows),
        "third_or_ambiguous_signature_count": third_signature_count,
        "maximum_width_reduction_factor": max(
            float(row["width_reduction_factor"]) for row in rows
        ),
        "maximum_bracket_to_parent_width_ratio": max(
            float(row["bracket_to_parent_width_ratio"])
            for row in rows
        ),
        "next_bisection_coordinates": [
            {
                "transition_id": row["transition_id"],
                "decay_cosine": row[
                    "next_bisection_coordinate"
                ],
            }
            for row in rows
        ],
    }
    return rows, summary


def residue_fit_rows(node_id: str) -> list[dict[str, str]]:
    path = M5251.node_paths(node_id)["residues"]
    if not path.exists():
        return []
    return read_csv(path)


def residue_bound_audit(
    bisection_rows: list[dict[str, Any]],
    narrowed_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    node_by_id = {
        row["order9_node_id"]: row for row in bisection_rows
    }
    coefficient = half_residue_coefficient()
    physical_multiplier = float(
        M5231.PHYSICAL_A00_WEIGHT * M5231.KERNEL_MULTIPLIER
    )
    residue_rows: list[dict[str, Any]] = []
    audit_by_node: dict[str, dict[str, Any]] = {}
    for node_id in TARGET_NODE_IDS:
        node = node_by_id[node_id]
        fits = residue_fit_rows(node_id)
        active = int(node["active_pole_count"]) > 0
        fits_by_epsilon = {
            row["epsilon_id"]: row for row in fits
        }
        if active and set(fits_by_epsilon) == {"E020", "E040"}:
            values: dict[str, dict[str, complex]] = {}
            for epsilon_id, fit in fits_by_epsilon.items():
                numerator = complex(
                    float(fit["numerator_at_pole_real"]),
                    float(fit["numerator_at_pole_imaginary"]),
                )
                derivative = complex(
                    float(fit["channel_derivative_real"]),
                    float(fit["channel_derivative_imaginary"]),
                )
                residue = complex(
                    float(fit["outer_residue_real"]),
                    float(fit["outer_residue_imaginary"]),
                )
                values[epsilon_id] = {
                    "numerator": numerator,
                    "derivative": derivative,
                    "residue": residue,
                }
            combination = (
                2.0 * values["E020"]["residue"]
                - values["E040"]["residue"]
            )
            predicted_jump = (
                -1.0j
                * math.pi
                * physical_multiplier
                * combination
            )
            physical = complex(
                float(node["order512_subtracted_real"]),
                float(node["order512_subtracted_imaginary"]),
            )
            imaginary_residual = abs(
                physical.imag - predicted_jump.imag
            ) / max(abs(predicted_jump.imag), 1.0)
            sampled_triangle_envelope = coefficient * (
                2.0
                * abs(values["E020"]["numerator"])
                / abs(values["E020"]["derivative"])
                + abs(values["E040"]["numerator"])
                / abs(values["E040"]["derivative"])
            )
            row = {
                "node_id": node_id,
                "transition_id": node["transition_id"],
                "decay_cosine": node["decay_cosine"],
                "active_pole_count": node["active_pole_count"],
                "residue_fit_status": "TWO_REGULATORS_FITTED",
                "R20_real": values["E020"]["residue"].real,
                "R20_imaginary": (
                    values["E020"]["residue"].imag
                ),
                "R40_real": values["E040"]["residue"].real,
                "R40_imaginary": (
                    values["E040"]["residue"].imag
                ),
                "combination_real": combination.real,
                "combination_imaginary": combination.imag,
                "predicted_half_residue_jump_real": (
                    predicted_jump.real
                ),
                "predicted_half_residue_jump_imaginary": (
                    predicted_jump.imag
                ),
                "physical_value_real": physical.real,
                "physical_value_imaginary": physical.imag,
                "imaginary_relative_residual": imaginary_residual,
                "sampled_triangle_envelope": (
                    sampled_triangle_envelope
                ),
                "continuous_envelope_certified": False,
                "valid_for_boundary_error_claim": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        elif active:
            row = {
                "node_id": node_id,
                "transition_id": node["transition_id"],
                "decay_cosine": node["decay_cosine"],
                "active_pole_count": node["active_pole_count"],
                "residue_fit_status": "INCOMPLETE_ACTIVE_FITS",
                "continuous_envelope_certified": False,
                "valid_for_boundary_error_claim": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        else:
            row = {
                "node_id": node_id,
                "transition_id": node["transition_id"],
                "decay_cosine": node["decay_cosine"],
                "active_pole_count": 0,
                "residue_fit_status": "INACTIVE_NO_RESIDUE_TERM",
                "continuous_envelope_certified": False,
                "valid_for_boundary_error_claim": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        residue_rows.append(row)
        audit_by_node[node_id] = row

    points = generation1_point_records()
    points.update(
        {
            row["order9_node_id"]: {
                "point_id": row["order9_node_id"],
                "active_pole_count": int(
                    row["active_pole_count"]
                ),
                "result_path": str(
                    M5251.node_paths(row["order9_node_id"])[
                        "result"
                    ]
                ),
            }
            for row in bisection_rows
        }
    )
    parent_value = complex(
        float(
            read_json(RESULT_5255)["summary"].get(
                "adaptive_two_panel_512_real",
                read_json(M5255.RESULT_5254)["summary"][
                    "adaptive_two_panel_512_real"
                ],
            )
        ),
        float(
            read_json(RESULT_5255)["summary"].get(
                "adaptive_two_panel_512_imaginary",
                read_json(M5255.RESULT_5254)["summary"][
                    "adaptive_two_panel_512_imaginary"
                ],
            )
        ),
    )
    total_budget = (
        OUTER_RELATIVE_ERROR_BUDGET * max(abs(parent_value), 1.0)
    )
    equal_budget = total_budget / len(narrowed_rows)
    error_rows: list[dict[str, Any]] = []
    for bracket in narrowed_rows:
        active_point_id = (
            bracket["new_left_point_id"]
            if int(bracket["new_left_active_pole_count"]) > 0
            else bracket["new_right_point_id"]
        )
        active_audit = audit_by_node.get(active_point_id)
        if active_audit is None:
            result_path = Path(points[active_point_id]["result_path"])
            fit_path = result_path.parent / "corrected_residue_fits.csv"
            fits = read_csv(fit_path) if fit_path.exists() else []
            fits_by_epsilon = {
                row["epsilon_id"]: row for row in fits
            }
            if set(fits_by_epsilon) == {"E020", "E040"}:
                sampled_envelope = coefficient * sum(
                    (
                        weight
                        * abs(
                            complex(
                                float(
                                    fits_by_epsilon[epsilon_id][
                                        "numerator_at_pole_real"
                                    ]
                                ),
                                float(
                                    fits_by_epsilon[epsilon_id][
                                        "numerator_at_pole_imaginary"
                                    ]
                                ),
                            )
                        )
                        / abs(
                            complex(
                                float(
                                    fits_by_epsilon[epsilon_id][
                                        "channel_derivative_real"
                                    ]
                                ),
                                float(
                                    fits_by_epsilon[epsilon_id][
                                        "channel_derivative_imaginary"
                                    ]
                                ),
                            )
                        )
                    )
                    for epsilon_id, weight in (
                        ("E020", 2.0),
                        ("E040", 1.0),
                    )
                )
                source_status = "PRIOR_ACTIVE_ENDPOINT_SAMPLE"
            else:
                sampled_envelope = math.inf
                source_status = "MISSING_ACTIVE_ENDPOINT_FITS"
        else:
            sampled_envelope = float(
                active_audit["sampled_triangle_envelope"]
            )
            source_status = "CURRENT_ACTIVE_MIDPOINT_SAMPLE"
        width = float(bracket["new_bracket_width"])
        location_proxy = (
            ANGULAR_JACOBIAN * width * sampled_envelope
        )
        target_width = (
            equal_budget
            / (ANGULAR_JACOBIAN * sampled_envelope)
            if math.isfinite(sampled_envelope)
            and sampled_envelope > 0.0
            else 0.0
        )
        remaining = (
            max(0, math.ceil(math.log2(width / target_width)))
            if target_width > 0.0
            else -1
        )
        error_rows.append(
            {
                "transition_id": bracket["transition_id"],
                "active_endpoint_id": active_point_id,
                "sample_source_status": source_status,
                "new_bracket_width": width,
                "sampled_half_residue_triangle_envelope": (
                    sampled_envelope
                ),
                "sampled_location_error_proxy": location_proxy,
                "equal_boundary_budget": equal_budget,
                "provisional_target_width": target_width,
                "provisional_remaining_bisection_generations": (
                    remaining
                ),
                "continuous_N_supremum_supplied": False,
                "continuous_Dprime_infimum_supplied": False,
                "continuous_envelope_certified": False,
                "valid_for_boundary_error_claim": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    active_audits = [
        row
        for row in residue_rows
        if row["residue_fit_status"] == "TWO_REGULATORS_FITTED"
    ]
    summary = {
        "half_residue_coefficient": coefficient,
        "active_current_node_count": len(active_audits),
        "maximum_half_residue_imaginary_relative_residual": max(
            (
                float(row["imaginary_relative_residual"])
                for row in active_audits
            ),
            default=0.0,
        ),
        "half_residue_identity_empirically_supported": (
            bool(active_audits)
            and all(
                float(row["imaginary_relative_residual"])
                <= MAXIMUM_HALF_RESIDUE_IMAGINARY_RELATIVE_RESIDUAL
                for row in active_audits
            )
        ),
        "continuous_residue_envelope_certified": False,
        "total_sampled_location_error_proxy": sum(
            float(row["sampled_location_error_proxy"])
            for row in error_rows
        ),
        "outer_absolute_error_budget": total_budget,
        "maximum_provisional_remaining_bisection_generations": max(
            int(row["provisional_remaining_bisection_generations"])
            for row in error_rows
        ),
    }
    return residue_rows, error_rows, summary


def validation_rows(
    manifest: dict[str, Any],
    results: dict[str, dict[str, Any]],
    bisection_rows: list[dict[str, Any]],
    narrowed_rows: list[dict[str, Any]],
    residue_rows: list[dict[str, Any]],
    error_rows: list[dict[str, Any]],
    summary: dict[str, Any],
    formal_diff_rows: list[dict[str, Any]],
    elapsed: float,
) -> list[dict[str, Any]]:
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
            "GENERATION2_NODE_ACCOUNTING_EXACT",
            (
                set(results) == set(TARGET_NODE_IDS)
                and len(bisection_rows) == 4
            ),
            f"{len(results)} results, {len(bisection_rows)} rows",
            "4 results, 4 rows",
        ),
        (
            "integrity",
            "ALL_GENERATION2_NODE_INTEGRITY_GATES_PASS",
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
            "ALL_GENERATION2_NODE_ACCEPTANCE_GATES_PASS",
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
                <= 0.5
                or math.isclose(
                    float(summary["maximum_width_reduction_factor"]),
                    0.5,
                    rel_tol=0.0,
                    abs_tol=1.0e-12,
                )
            ),
            summary["maximum_width_reduction_factor"],
            0.5,
        ),
        (
            "integrity",
            "HALF_RESIDUE_COEFFICIENT_DERIVED",
            math.isclose(
                float(summary["half_residue_coefficient"]),
                0.016,
                rel_tol=0.0,
                abs_tol=2.0e-15,
            ),
            summary["half_residue_coefficient"],
            0.016,
        ),
        (
            "acceptance",
            "HALF_RESIDUE_IMAGINARY_WITNESS_PASSES",
            bool(
                summary[
                    "half_residue_identity_empirically_supported"
                ]
            ),
            summary[
                "maximum_half_residue_imaginary_relative_residual"
            ],
            MAXIMUM_HALF_RESIDUE_IMAGINARY_RELATIVE_RESIDUAL,
        ),
        (
            "integrity",
            "CONTINUOUS_ENVELOPE_NOT_SMUGGLED",
            (
                not bool(
                    summary[
                        "continuous_residue_envelope_certified"
                    ]
                )
                and all(
                    row["continuous_envelope_certified"] is False
                    and row["valid_for_boundary_error_claim"] is False
                    for row in (*residue_rows, *error_rows)
                )
            ),
            "continuous enclosure absent; claim false",
            "continuous enclosure absent; claim false",
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
    residue_rows: list[dict[str, Any]],
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
            f"{row['new_right_active_pole_count']}`, next "
            f"`{float(row['next_bisection_coordinate']):.12g}`."
        )
        for row in narrowed_rows
    ]
    residue_lines = [
        (
            f"- `{row['node_id']}`: `{row['residue_fit_status']}`"
            + (
                f", predicted jump imaginary "
                f"`{float(row['predicted_half_residue_jump_imaginary']):.12g}`, "
                f"physical imaginary "
                f"`{float(row['physical_value_imaginary']):.12g}`, "
                f"relative residual "
                f"`{float(row['imaginary_relative_residual']):.12g}`."
                if row["residue_fit_status"]
                == "TWO_REGULATORS_FITTED"
                else "."
            )
        )
        for row in residue_rows
    ]
    budget_lines = [
        (
            f"- `{row['transition_id']}` active endpoint "
            f"`{row['active_endpoint_id']}`, sampled half-residue "
            f"envelope `{float(row['sampled_half_residue_triangle_envelope']):.12g}`, "
            f"location proxy "
            f"`{float(row['sampled_location_error_proxy']):.12g}`, "
            f"provisional generations "
            f"`{row['provisional_remaining_bisection_generations']}`."
        )
        for row in error_rows
    ]
    return "\n".join(
        [
            "# 5256 - Outer topology bisection generation 2 and "
            "half-residue bound",
            "",
            "## Generation-2 evaluation",
            "",
            *node_lines,
            "",
            "## Narrowed brackets",
            "",
            *bracket_lines,
            "",
            "## Derived half-residue identity",
            "",
            "The regulator combination and the physical A00/kernel "
            "normalization give",
            "",
            "```text",
            "R_epsilon(x) = N_epsilon(x)/D'_epsilon(x);",
            "Delta f(x) = -i pi (P_A00 K) "
            "[2 R_E020(x)-R_E040(x)];",
            "pi |P_A00 K| = 0.016.",
            "```",
            "",
            "Therefore, on a constant-topology chamber `C`,",
            "",
            "```text",
            "sup_C |Delta f|",
            " <= 0.016 [",
            "    2 sup_C|N20|/inf_C|D20'|",
            "      + sup_C|N40|/inf_C|D40'| ];",
            "",
            "|delta I_boundary|",
            " <= J delta_x sup_C|Delta f|.",
            "```",
            "",
            *residue_lines,
            "",
            (
                "- Maximum current half-residue imaginary residual: "
                f"`{summary['maximum_half_residue_imaginary_relative_residual']:.12g}`."
            ),
            "",
            "## Stopping-gate status",
            "",
            "The algebraic inequality is derived. The rows below insert "
            "sampled `N` and `D'` values only; they are not continuous "
            "interval enclosures and remain nonclaim.",
            "",
            *budget_lines,
            "",
            "## Decision",
            "",
            f"`{decision}`",
            "",
            "## Claim boundary",
            "",
            "No sampled extremum is called a supremum, and no sampled "
            "minimum is called an infimum. Outer convergence, the numeric "
            "p8 coefficient, all-operator local GR, and full MTS remain "
            "unclaimed.",
            "",
            "## Next exact target",
            "",
            "Construct interval enclosures for `N_epsilon(x)` and "
            "`D'_epsilon(x)` over each narrowed active-side chamber. "
            "Generation-3 bisection may run concurrently, but its stopping "
            "decision must use those continuous enclosures rather than "
            "another endpoint proxy.",
            "",
        ]
    )


def execute(
    max_workers: int,
    *,
    aggregate_only: bool = False,
) -> dict[str, Any]:
    started = time.perf_counter()
    SOURCE.mkdir(parents=True, exist_ok=True)
    manifest, dry_run = prepare()
    M5251.atomic_json(MANIFEST, manifest)
    M5251.atomic_json(DRY_RUN, dry_run)
    M5251.write_csv(BISECTION_ROWS, bisection_nodes())
    if not dry_run["dry_run_passed"]:
        failed = [
            key
            for key, passed in dry_run["checks"].items()
            if not passed
        ]
        raise RuntimeError(f"5256 dry run failed: {failed}")

    if aggregate_only:
        return_codes = {
            node_id: (
                0 if M5251.node_paths(node_id)["result"].exists() else 1
            )
            for node_id in TARGET_NODE_IDS
        }
    else:
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
        raise RuntimeError(f"5256 workers failed: {worker_failures}")

    results = {
        node_id: node_result(node_id)
        for node_id in TARGET_NODE_IDS
    }
    bisection_rows = bisection_result_rows(results)
    narrowed_rows, bracket_summary = narrow_brackets(
        bisection_rows
    )
    residue_rows, error_rows, residue_summary = (
        residue_bound_audit(bisection_rows, narrowed_rows)
    )
    summary = {**bracket_summary, **residue_summary}
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
        residue_rows,
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
        decision = "INVALID_TOPOLOGY_BISECTION_GEN2_HALF_RESIDUE_BOUND"
    elif not acceptance_passed:
        decision = (
            "HOLD_TOPOLOGY_BISECTION_GEN2_HALF_RESIDUE_BOUND__"
            "LOCALIZE_FAILED_GATE"
        )
    else:
        decision = (
            "ADOPT_BISECTION_GEN2_AND_HALF_RESIDUE_IDENTITY__"
            "BUILD_CONTINUOUS_ENCLOSURE"
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
    M5251.write_csv(BISECTION_ROWS, bisection_rows)
    M5251.write_csv(NARROWED_BRACKETS, narrowed_rows)
    M5251.write_csv(RESIDUE_BOUND_ROWS, residue_rows)
    M5251.write_csv(ERROR_BUDGET_ROWS, error_rows)
    M5251.write_csv(VALIDATION, validations)
    M5251.atomic_text(
        DOCUMENT,
        render_document(
            bisection_rows,
            narrowed_rows,
            residue_rows,
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
        raise RuntimeError("5256 integrity failed")
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
    parser.add_argument(
        "--aggregate-only",
        action="store_true",
        help="Reuse completed node results without launching workers.",
    )
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
    M5251.write_csv(BISECTION_ROWS, bisection_nodes())
    if arguments.dry_run:
        print(json.dumps(dry_run, indent=2, sort_keys=True))
        if not dry_run["dry_run_passed"]:
            raise SystemExit(1)
        return
    if arguments.max_workers < 1:
        raise ValueError("--max-workers must be positive")
    result = execute(
        min(arguments.max_workers, len(TARGET_NODE_IDS)),
        aggregate_only=arguments.aggregate_only,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
