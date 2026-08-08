from __future__ import annotations

import argparse
import concurrent.futures
import csv
import hashlib
import importlib.util
import json
import math
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5253"
NODES = SOURCE / "nodes"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5252 = (
    POST
    / "scripts"
    / "Y5_R2FR_5252_Q01_Q07_full_order9_paired_transport_and_outer_gate.py"
)
RESULT_5252 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5252"
    / "full_order9_result.json"
)
MANIFEST_5252 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5252"
    / "full_order9_manifest.json"
)
NODE_ROWS_5252 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5252"
    / "full_order9_node_summary.csv"
)
VALIDATION_5252 = RESIDUALS / "P8_Y5_BRR545_5252_VALIDATION.csv"

MANIFEST = SOURCE / "outer_interval_midpoint_manifest.json"
DRY_RUN = SOURCE / "outer_interval_midpoint_dry_run.json"
STATUS = SOURCE / "outer_interval_midpoint_status.json"
RESULT = SOURCE / "outer_interval_midpoint_result.json"
MIDPOINT_ROWS = SOURCE / "outer_interval_midpoint_nodes.csv"
INTERVAL_ROWS = SOURCE / "outer_interval_localization.csv"
COMPOSITE_ROWS = SOURCE / "outer_composite_rules.csv"
FORMAL_INVENTORY = SOURCE / "formalization_workbench_start_inventory.csv"
FORMAL_DIFF = SOURCE / "formalization_workbench_run_diff.csv"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5253_VALIDATION.csv"
DOCUMENT = (
    POST
    / "5253-Y5-R2FR-corrected-outer-interval-midpoint-localization.md"
)
COMPLETE = SOURCE / "COMPLETE.marker"

CHECKPOINT = 5253
PARENT_CHECKPOINT = 5252
MARKER = "MTS_5253_CORRECTED_OUTER_INTERVAL_MIDPOINT_LOCALIZATION"
REVISION = "corrected-outer-interval-midpoint-localization-v1"
TRANSPORT_CACHE_REVISION = (
    "corrected-outer-interval-midpoint-localization-v1"
)
TARGET_NODE_IDS = tuple(f"M{index:02d}" for index in range(8))
INNER_ORDERS = (128, 512)
DEFAULT_MAX_WORKERS = 2
MAXIMUM_NODE_RUNTIME_SECONDS = 4.0 * 60.0 * 60.0
MAXIMUM_BATCH_RUNTIME_SECONDS = 10.0 * 60.0 * 60.0
MAXIMUM_FIRST_LEVEL_RELATIVE_DIFFERENCE = 0.2
DOMINANT_ERROR_FRACTION = 0.8
ANGULAR_JACOBIAN = 0.25
EXPECTED_PARENT_DECISION = (
    "HOLD_FULL_ORDER9_CUBATURE__LOCALIZE_CORRECTED_OUTER_PROFILE"
)


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"Unable to load {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


M5252 = load_module(SCRIPT_5252, "mts_5252_for_5253")
M5251 = M5252.M5251


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


def complex_parent_value(
    row: dict[str, str], inner_order: int
) -> complex:
    return complex(
        float(row[f"order{inner_order}_subtracted_real"]),
        float(row[f"order{inner_order}_subtracted_imaginary"]),
    )


def parent_node_rows() -> list[dict[str, str]]:
    rows = sorted(
        read_csv(NODE_ROWS_5252),
        key=lambda row: float(row["decay_cosine"]),
    )
    if len(rows) != 9:
        raise RuntimeError(f"Expected 9 parent nodes, found {len(rows)}")
    return rows


def midpoint_nodes() -> list[dict[str, Any]]:
    parent_rows = parent_node_rows()
    rows: list[dict[str, Any]] = []
    for index, (left, right) in enumerate(
        zip(parent_rows[:-1], parent_rows[1:])
    ):
        lower = float(left["decay_cosine"])
        upper = float(right["decay_cosine"])
        midpoint = 0.5 * (lower + upper)
        rows.append(
            {
                "order9_node_id": TARGET_NODE_IDS[index],
                "execution_node_id": f"I{index:02d}",
                "master_index": 2 * index + 1,
                "decay_cosine": midpoint,
                "interval_index": index,
                "left_parent_node_id": left["order9_node_id"],
                "right_parent_node_id": right["order9_node_id"],
                "interval_lower": lower,
                "interval_upper": upper,
                "interval_width": upper - lower,
                "node_role": "ARITHMETIC_INTERVAL_MIDPOINT",
                "reused_from_5240": False,
                "source_cache": str(
                    NODES
                    / TARGET_NODE_IDS[index]
                    / "node_result.json"
                ),
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def endpoint_linear_reference_values() -> dict[
    str, dict[int, complex]
]:
    parent_rows = parent_node_rows()
    return {
        TARGET_NODE_IDS[index]: {
            inner_order: 0.5
            * (
                complex_parent_value(left, inner_order)
                + complex_parent_value(right, inner_order)
            )
            for inner_order in INNER_ORDERS
        }
        for index, (left, right) in enumerate(
            zip(parent_rows[:-1], parent_rows[1:])
        )
    }


def no_same_coordinate_legacy_comparison(
    node_id: str,
    adaptive_rows: list[dict[str, Any]],
    _fixed_rows_all: list[dict[str, str]],
) -> list[dict[str, Any]]:
    grouped = M5251.M5239.interval_rows_by_job(adaptive_rows)
    rows: list[dict[str, Any]] = []
    for job_id, local_rows in sorted(grouped.items()):
        sample = local_rows[0]
        rows.append(
            {
                "order9_node_id": node_id,
                "job_id": job_id,
                "epsilon_id": sample["epsilon_id"],
                "component_id": sample["component_id"],
                "family": sample["family"],
                "fixed_interval_count": 0,
                "adaptive_interval_count": len(local_rows),
                "interval_count_change": len(local_rows),
                "fixed_state_measure": "{}",
                "adaptive_state_measure": json.dumps(
                    M5251.M5243.state_measure(local_rows),
                    sort_keys=True,
                ),
                "multiplier_mismatch_measure": "",
                "maps_identical_up_to_measure": False,
                "comparison_status": (
                    "NO_SAME_COORDINATE_LEGACY_BASELINE"
                ),
                "comparison_used_for_acceptance": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


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
    M5251.RESULT_5250 = RESULT_5252
    M5251.MAXIMUM_NODE_RUNTIME_SECONDS = MAXIMUM_NODE_RUNTIME_SECONDS
    M5251.fixed_node_values = endpoint_linear_reference_values
    M5251.M5243.compare_intervals = (
        no_same_coordinate_legacy_comparison
    )


def source_rows() -> list[dict[str, str]]:
    paths = [
        Path(__file__),
        SCRIPT_5252,
        RESULT_5252,
        MANIFEST_5252,
        NODE_ROWS_5252,
        VALIDATION_5252,
    ]
    paths.extend(
        Path(row["source_path"])
        for row in parent_node_rows()
        if row.get("source_path")
    )
    unique_paths = sorted(set(paths), key=str)
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in unique_paths
    ]


def prepare() -> tuple[dict[str, Any], dict[str, Any]]:
    configure_node_engine()
    parent_result = read_json(RESULT_5252)
    parent_validation = read_csv(VALIDATION_5252)
    parent_rows = parent_node_rows()
    target_nodes = midpoint_nodes()
    formal_rows = M5251.formal_inventory_rows()
    formal_digest = M5251.inventory_digest(formal_rows)
    M5251.write_csv(FORMAL_INVENTORY, formal_rows)
    manifest = {
        "marker": MARKER,
        "revision": REVISION,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "parent_decision": parent_result["decision"],
        "parent_integrity_passed": parent_result["integrity_passed"],
        "parent_acceptance_passed": parent_result[
            "acceptance_passed"
        ],
        "outer_coordinate": "decay_cosine",
        "angular_domain": [
            float(parent_rows[0]["decay_cosine"]),
            float(parent_rows[-1]["decay_cosine"]),
        ],
        "parent_node_count": len(parent_rows),
        "target_node_ids": list(TARGET_NODE_IDS),
        "outer_nodes": target_nodes,
        "local_rule": {
            "coarse": "interval trapezoid",
            "fine": "interval Simpson using one arithmetic midpoint",
            "local_indicator": "abs(S_i-T_i)",
            "global_indicator": "abs(sum(S_i)-sum(T_i))",
            "cancellation_safe_indicator": "sum(abs(S_i-T_i))",
            "angular_unit_cube_jacobian": ANGULAR_JACOBIAN,
            "interpretation": (
                "The first-level embedded difference is a localization "
                "indicator, not a rigorous error bound. A smooth-interval "
                "error estimate requires quarter-point refinement."
            ),
        },
        "dominant_error_fraction": DOMINANT_ERROR_FRACTION,
        "maximum_first_level_relative_difference": (
            MAXIMUM_FIRST_LEVEL_RELATIVE_DIFFERENCE
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
                "This checkpoint localizes one decay-angle slice at one "
                "soft energy. First-level Simpson/trapezoid disagreement "
                "is not a certified outer error bound."
            ),
        },
    }
    manifest["manifest_hash"] = serialized_hash(manifest)
    coordinates = [
        float(row["decay_cosine"]) for row in target_nodes
    ]
    interval_pairs = list(zip(parent_rows[:-1], parent_rows[1:]))
    parent_integrity_rows = [
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
                row["passed"] == "True"
                for row in parent_integrity_rows
            )
        ),
        "parent_failure_signature_expected": (
            not bool(parent_result["acceptance_passed"])
            and parent_result["decision"] == EXPECTED_PARENT_DECISION
        ),
        "parent_node_partition_exact": (
            len(parent_rows) == 9
            and len(interval_pairs) == 8
            and all(
                float(left["decay_cosine"])
                < float(right["decay_cosine"])
                for left, right in interval_pairs
            )
        ),
        "midpoints_exact": (
            len(target_nodes) == 8
            and len(set(coordinates)) == 8
            and all(
                math.isclose(
                    float(node["decay_cosine"]),
                    0.5
                    * (
                        float(left["decay_cosine"])
                        + float(right["decay_cosine"])
                    ),
                    rel_tol=0.0,
                    abs_tol=2.0e-15,
                )
                for node, (left, right) in zip(
                    target_nodes, interval_pairs
                )
            )
        ),
        "target_ids_exact": (
            {row["order9_node_id"] for row in target_nodes}
            == set(TARGET_NODE_IDS)
        ),
        "formal_snapshot_captured": (
            len(formal_rows) > 0
            and len(formal_digest) == 64
            and FORMAL_INVENTORY.exists()
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
        "target_node_ids": list(TARGET_NODE_IDS),
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    return manifest, dry_run


def run_worker(node_id: str) -> int:
    paths = M5251.node_paths(node_id)
    paths["root"].mkdir(parents=True, exist_ok=True)
    log_path = paths["root"] / "worker.log"
    command = [
        sys.executable,
        str(Path(__file__)),
        "--worker-node",
        node_id,
    ]
    with log_path.open("w", encoding="utf-8") as log_handle:
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
            completed = sum(
                code == 0 for code in return_codes.values()
            )
            M5251.atomic_json(
                STATUS,
                {
                    "marker": MARKER,
                    "status": "RUNNING",
                    "completed_nodes": len(return_codes),
                    "successful_nodes": completed,
                    "total_nodes": len(TARGET_NODE_IDS),
                    "return_codes": return_codes,
                },
            )
    return return_codes


def node_result(node_id: str) -> dict[str, Any]:
    return read_json(M5251.node_paths(node_id)["result"])


def node_value(
    result: dict[str, Any], inner_order: int
) -> complex:
    values = result["physical_values"][str(inner_order)]
    return complex(
        float(values["subtracted_real"]),
        float(values["subtracted_imaginary"]),
    )


def build_midpoint_rows(
    results: dict[str, dict[str, Any]]
) -> list[dict[str, Any]]:
    references = endpoint_linear_reference_values()
    rows: list[dict[str, Any]] = []
    for node in midpoint_nodes():
        node_id = node["order9_node_id"]
        result = results[node_id]
        values = {
            inner_order: node_value(result, inner_order)
            for inner_order in INNER_ORDERS
        }
        departures = {
            inner_order: values[inner_order]
            - references[node_id][inner_order]
            for inner_order in INNER_ORDERS
        }
        rows.append(
            {
                **node,
                "integrity_passed": result["integrity_passed"],
                "acceptance_passed": result["acceptance_passed"],
                "order128_subtracted_real": values[128].real,
                "order128_subtracted_imaginary": values[128].imag,
                "order512_subtracted_real": values[512].real,
                "order512_subtracted_imaginary": values[512].imag,
                "endpoint_linear_reference_512_real": (
                    references[node_id][512].real
                ),
                "endpoint_linear_reference_512_imaginary": (
                    references[node_id][512].imag
                ),
                "midpoint_curvature_departure_512_real": (
                    departures[512].real
                ),
                "midpoint_curvature_departure_512_imaginary": (
                    departures[512].imag
                ),
                "midpoint_curvature_departure_512_magnitude": abs(
                    departures[512]
                ),
                "inner128_to512_relative_difference": (
                    abs(values[128] - values[512])
                    / max(abs(values[512]), 1.0)
                ),
                "elapsed_seconds": result["elapsed_seconds"],
                "internal_fixed_field_semantics": (
                    "ENDPOINT_LINEAR_REFERENCE_DIAGNOSTIC_ONLY"
                ),
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def interval_localization(
    midpoint_rows: list[dict[str, Any]]
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    parents = parent_node_rows()
    midpoint_by_id = {
        row["order9_node_id"]: row for row in midpoint_rows
    }
    interval_rows: list[dict[str, Any]] = []
    composite: dict[int, dict[str, complex]] = {
        inner_order: {"trapezoid": 0.0j, "simpson": 0.0j}
        for inner_order in INNER_ORDERS
    }
    for index, (left, right) in enumerate(
        zip(parents[:-1], parents[1:])
    ):
        node_id = TARGET_NODE_IDS[index]
        midpoint = midpoint_by_id[node_id]
        lower = float(left["decay_cosine"])
        upper = float(right["decay_cosine"])
        width = upper - lower
        row: dict[str, Any] = {
            "interval_id": f"I{index:02d}",
            "interval_index": index,
            "left_parent_node_id": left["order9_node_id"],
            "midpoint_node_id": node_id,
            "right_parent_node_id": right["order9_node_id"],
            "interval_lower": lower,
            "interval_midpoint": float(midpoint["decay_cosine"]),
            "interval_upper": upper,
            "interval_width": width,
        }
        for inner_order in INNER_ORDERS:
            left_value = complex_parent_value(left, inner_order)
            right_value = complex_parent_value(right, inner_order)
            midpoint_value = complex(
                float(
                    midpoint[
                        f"order{inner_order}_subtracted_real"
                    ]
                ),
                float(
                    midpoint[
                        f"order{inner_order}_subtracted_imaginary"
                    ]
                ),
            )
            trapezoid = (
                ANGULAR_JACOBIAN
                * width
                * 0.5
                * (left_value + right_value)
            )
            simpson = (
                ANGULAR_JACOBIAN
                * width
                / 6.0
                * (
                    left_value
                    + 4.0 * midpoint_value
                    + right_value
                )
            )
            difference = simpson - trapezoid
            composite[inner_order]["trapezoid"] += trapezoid
            composite[inner_order]["simpson"] += simpson
            prefix = f"order{inner_order}"
            row.update(
                {
                    f"{prefix}_trapezoid_real": trapezoid.real,
                    f"{prefix}_trapezoid_imaginary": (
                        trapezoid.imag
                    ),
                    f"{prefix}_simpson_real": simpson.real,
                    f"{prefix}_simpson_imaginary": simpson.imag,
                    f"{prefix}_embedded_difference_real": (
                        difference.real
                    ),
                    f"{prefix}_embedded_difference_imaginary": (
                        difference.imag
                    ),
                    f"{prefix}_embedded_indicator": abs(difference),
                }
            )
        row.update(
            {
                "priority_rank": 0,
                "selected_for_quarterpoint_refinement": False,
                "selection_reason": "",
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
        interval_rows.append(row)

    ranked = sorted(
        interval_rows,
        key=lambda row: float(row["order512_embedded_indicator"]),
        reverse=True,
    )
    total_local_indicator = sum(
        float(row["order512_embedded_indicator"])
        for row in ranked
    )
    cumulative = 0.0
    selected_ids: list[str] = []
    for rank, row in enumerate(ranked, start=1):
        row["priority_rank"] = rank
        if (
            total_local_indicator > 0.0
            and cumulative
            < DOMINANT_ERROR_FRACTION * total_local_indicator
        ):
            row["selected_for_quarterpoint_refinement"] = True
            row["selection_reason"] = (
                f"DOMINANT_{DOMINANT_ERROR_FRACTION:.0%}_"
                "CANCELLATION_SAFE_INDICATOR"
            )
            selected_ids.append(row["interval_id"])
        cumulative += float(row["order512_embedded_indicator"])
        row["cumulative_indicator_fraction"] = (
            cumulative / total_local_indicator
            if total_local_indicator > 0.0
            else 0.0
        )

    composite_rows: list[dict[str, Any]] = []
    for inner_order in INNER_ORDERS:
        for rule_name in ("trapezoid", "simpson"):
            value = composite[inner_order][rule_name]
            composite_rows.append(
                {
                    "inner_order": inner_order,
                    "outer_rule": rule_name.upper(),
                    "outer_interval_count": len(interval_rows),
                    "outer_new_node_count": len(midpoint_rows),
                    "value_real": value.real,
                    "value_imaginary": value.imag,
                    "magnitude": abs(value),
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )

    trapezoid_512 = composite[512]["trapezoid"]
    simpson_512 = composite[512]["simpson"]
    difference_512 = simpson_512 - trapezoid_512
    cancellation_safe = sum(
        float(row["order512_embedded_indicator"])
        for row in interval_rows
    )
    parent_result = read_json(RESULT_5252)
    parent_order9 = complex(
        float(parent_result["summary"]["order9_real"]),
        float(parent_result["summary"]["order9_imaginary"]),
    )
    summary = {
        "composite_trapezoid_512_real": trapezoid_512.real,
        "composite_trapezoid_512_imaginary": (
            trapezoid_512.imag
        ),
        "composite_simpson_512_real": simpson_512.real,
        "composite_simpson_512_imaginary": simpson_512.imag,
        "global_embedded_difference_512": abs(difference_512),
        "global_embedded_relative_difference_512": (
            abs(difference_512) / max(abs(simpson_512), 1.0)
        ),
        "cancellation_safe_embedded_indicator_512": (
            cancellation_safe
        ),
        "cancellation_safe_relative_indicator_512": (
            cancellation_safe / max(abs(simpson_512), 1.0)
        ),
        "composite_simpson_inner128_to512_relative_difference": (
            abs(
                composite[128]["simpson"]
                - composite[512]["simpson"]
            )
            / max(abs(composite[512]["simpson"]), 1.0)
        ),
        "parent_global_order9_real": parent_order9.real,
        "parent_global_order9_imaginary": parent_order9.imag,
        "simpson_to_parent_order9_relative_difference": (
            abs(simpson_512 - parent_order9)
            / max(abs(simpson_512), 1.0)
        ),
        "dominant_interval_ids": selected_ids,
        "dominant_interval_count": len(selected_ids),
        "dominant_error_fraction_target": DOMINANT_ERROR_FRACTION,
        "first_level_indicator_is_rigorous_bound": False,
        "quarterpoint_confirmation_required": True,
    }
    return interval_rows, composite_rows, summary


def validation_rows(
    manifest: dict[str, Any],
    results: dict[str, dict[str, Any]],
    midpoint_rows: list[dict[str, Any]],
    interval_rows: list[dict[str, Any]],
    summary: dict[str, Any],
    formal_diff_rows: list[dict[str, Any]],
    elapsed: float,
) -> list[dict[str, Any]]:
    finite_fields = [
        key
        for key in interval_rows[0]
        if key.startswith("order")
        and (
            key.endswith("_real")
            or key.endswith("_imaginary")
            or key.endswith("_indicator")
        )
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
            "MIDPOINT_NODE_ACCOUNTING_EXACT",
            (
                set(results) == set(TARGET_NODE_IDS)
                and len(midpoint_rows) == 8
                and len(interval_rows) == 8
            ),
            (
                f"{len(results)} results, {len(midpoint_rows)} nodes, "
                f"{len(interval_rows)} intervals"
            ),
            "8 results, 8 nodes, 8 intervals",
        ),
        (
            "integrity",
            "ALL_MIDPOINT_NODE_INTEGRITY_GATES_PASS",
            all(
                bool(result["integrity_passed"])
                for result in results.values()
            ),
            sum(
                bool(result["integrity_passed"])
                for result in results.values()
            ),
            len(TARGET_NODE_IDS),
        ),
        (
            "acceptance",
            "ALL_MIDPOINT_NODE_ACCEPTANCE_GATES_PASS",
            all(
                bool(result["acceptance_passed"])
                for result in results.values()
            ),
            sum(
                bool(result["acceptance_passed"])
                for result in results.values()
            ),
            len(TARGET_NODE_IDS),
        ),
        (
            "integrity",
            "MIDPOINT_REFERENCE_SEMANTICS_EXPLICIT",
            all(
                row["internal_fixed_field_semantics"]
                == "ENDPOINT_LINEAR_REFERENCE_DIAGNOSTIC_ONLY"
                for row in midpoint_rows
            ),
            len(midpoint_rows),
            8,
        ),
        (
            "integrity",
            "INTERVAL_PARTITION_CLOSES",
            (
                math.isclose(
                    float(interval_rows[0]["interval_lower"]),
                    float(manifest["angular_domain"][0]),
                    abs_tol=2.0e-15,
                )
                and math.isclose(
                    float(interval_rows[-1]["interval_upper"]),
                    float(manifest["angular_domain"][1]),
                    abs_tol=2.0e-15,
                )
                and all(
                    math.isclose(
                        float(left["interval_upper"]),
                        float(right["interval_lower"]),
                        abs_tol=2.0e-15,
                    )
                    for left, right in zip(
                        interval_rows[:-1], interval_rows[1:]
                    )
                )
            ),
            (
                f"[{interval_rows[0]['interval_lower']},"
                f"{interval_rows[-1]['interval_upper']}]"
            ),
            str(manifest["angular_domain"]),
        ),
        (
            "integrity",
            "ALL_LOCAL_RULE_VALUES_FINITE",
            all(
                math.isfinite(float(row[field]))
                for row in interval_rows
                for field in finite_fields
            ),
            len(interval_rows) * len(finite_fields),
            len(interval_rows) * len(finite_fields),
        ),
        (
            "acceptance",
            "GLOBAL_FIRST_LEVEL_EMBEDDED_DIFFERENCE",
            (
                float(
                    summary[
                        "global_embedded_relative_difference_512"
                    ]
                )
                <= MAXIMUM_FIRST_LEVEL_RELATIVE_DIFFERENCE
            ),
            summary["global_embedded_relative_difference_512"],
            MAXIMUM_FIRST_LEVEL_RELATIVE_DIFFERENCE,
        ),
        (
            "acceptance",
            "CANCELLATION_SAFE_FIRST_LEVEL_EMBEDDED_BUDGET",
            (
                float(
                    summary[
                        "cancellation_safe_relative_indicator_512"
                    ]
                )
                <= MAXIMUM_FIRST_LEVEL_RELATIVE_DIFFERENCE
            ),
            summary["cancellation_safe_relative_indicator_512"],
            MAXIMUM_FIRST_LEVEL_RELATIVE_DIFFERENCE,
        ),
        (
            "integrity",
            "QUARTERPOINT_CONFIRMATION_RETAINED",
            (
                not bool(
                    summary["first_level_indicator_is_rigorous_bound"]
                )
                and bool(
                    summary["quarterpoint_confirmation_required"]
                )
            ),
            "nonrigorous first-level; confirmation required",
            "nonrigorous first-level; confirmation required",
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
    interval_rows: list[dict[str, Any]],
    summary: dict[str, Any],
    validations: list[dict[str, Any]],
    decision: str,
) -> str:
    ranked = sorted(
        interval_rows,
        key=lambda row: int(row["priority_rank"]),
    )
    table_lines = [
        (
            f"- `{row['interval_id']}` "
            f"[{float(row['interval_lower']):.12g}, "
            f"{float(row['interval_upper']):.12g}]: "
            f"midpoint `{float(row['interval_midpoint']):.12g}`, "
            f"|S-T| `{float(row['order512_embedded_indicator']):.12g}`, "
            f"rank `{row['priority_rank']}`, "
            f"refine `{row['selected_for_quarterpoint_refinement']}`."
        )
        for row in ranked
    ]
    failed_acceptance = [
        row["gate"]
        for row in validations
        if row["gate_kind"] == "acceptance"
        and not bool(row["passed"])
    ]
    selected = ", ".join(summary["dominant_interval_ids"])
    return "\n".join(
        [
            "# 5253 - Corrected outer interval midpoint localization",
            "",
            "## Derivation",
            "",
            "Let `f_i=f(x_i)` be consecutive corrected order-9 endpoint "
            "values, `m_i=(x_i+x_(i+1))/2`, and `h_i=x_(i+1)-x_i`. "
            "The checkpoint evaluates the parent integrand at every "
            "arithmetic midpoint and forms",
            "",
            "```text",
            "T_i = J h_i [f(x_i)+f(x_(i+1))]/2;",
            "S_i = J h_i [f(x_i)+4 f(m_i)+f(x_(i+1))]/6;",
            "D_i = S_i-T_i",
            "    = (2 J h_i/3) [f(m_i)-(f(x_i)+f(x_(i+1)))/2];",
            f"J   = {ANGULAR_JACOBIAN}.",
            "```",
            "",
            "`|D_i|` is used only to localize curvature and cancellation. "
            "It is not called a rigorous quadrature bound. That requires "
            "quarter-point refinement and comparison of one-panel with "
            "two-panel Simpson rules.",
            "",
            "## Measured interval map",
            "",
            *table_lines,
            "",
            "## Composite result",
            "",
            (
                "- Composite trapezoid (inner 512): "
                f"`({summary['composite_trapezoid_512_real']}"
                f"{summary['composite_trapezoid_512_imaginary']:+}j)`."
            ),
            (
                "- Composite Simpson (inner 512): "
                f"`({summary['composite_simpson_512_real']}"
                f"{summary['composite_simpson_512_imaginary']:+}j)`."
            ),
            (
                "- Global embedded relative difference: "
                f"`{summary['global_embedded_relative_difference_512']:.12g}`."
            ),
            (
                "- Cancellation-safe relative indicator: "
                f"`{summary['cancellation_safe_relative_indicator_512']:.12g}`."
            ),
            (
                "- Simpson inner 128/512 relative difference: "
                f"`{summary['composite_simpson_inner128_to512_relative_difference']:.12g}`."
            ),
            (
                "- Simpson versus parent global order-9 relative "
                f"difference: `{summary['simpson_to_parent_order9_relative_difference']:.12g}`."
            ),
            "",
            "## Decision",
            "",
            f"`{decision}`",
            "",
            (
                "Failed acceptance gates: "
                f"`{'|'.join(failed_acceptance) if failed_acceptance else 'none'}`."
            ),
            "",
            "## Claim boundary",
            "",
            "- This is one fixed-soft-energy decay-angle slice.",
            "- The first-level embedded indicator is not a proof of "
            "outer convergence.",
            "- No numeric UV coefficient, all-operator local-GR result, "
            "or full-MTS claim is promoted.",
            "",
            "## Next exact target",
            "",
            (
                "Evaluate both quarter points in the dominant intervals "
                f"`{selected}`. For each selected interval compare the "
                "one-panel Simpson value with the sum of its two "
                "half-panel Simpson values. Use `|S_two-S_one|/15` only "
                "where the measured topology is unchanged and the "
                "smoothness audit passes; otherwise split at the observed "
                "topology boundary."
            ),
            "",
        ]
    )


def execute(max_workers: int) -> dict[str, Any]:
    started = time.perf_counter()
    SOURCE.mkdir(parents=True, exist_ok=True)
    manifest, dry_run = prepare()
    M5251.atomic_json(MANIFEST, manifest)
    M5251.atomic_json(DRY_RUN, dry_run)
    M5251.write_csv(MIDPOINT_ROWS, midpoint_nodes())
    if not dry_run["dry_run_passed"]:
        failed = [
            key
            for key, passed in dry_run["checks"].items()
            if not passed
        ]
        raise RuntimeError(f"5253 dry run failed: {failed}")

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
        raise RuntimeError(f"5253 workers failed: {worker_failures}")

    results = {
        node_id: node_result(node_id)
        for node_id in TARGET_NODE_IDS
    }
    midpoint_summary_rows = build_midpoint_rows(results)
    (
        local_interval_rows,
        composite_rows,
        summary,
    ) = interval_localization(midpoint_summary_rows)
    formal_after_rows = M5251.formal_inventory_rows()
    formal_diff_rows = M5251.inventory_diff_rows(
        read_csv(FORMAL_INVENTORY), formal_after_rows
    )
    M5251.write_csv(FORMAL_DIFF, formal_diff_rows)
    elapsed = time.perf_counter() - started
    validations = validation_rows(
        manifest,
        results,
        midpoint_summary_rows,
        local_interval_rows,
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
        decision = "INVALID_OUTER_INTERVAL_MIDPOINT_LOCALIZATION"
    elif not all(
        bool(result["acceptance_passed"])
        for result in results.values()
    ):
        decision = (
            "HOLD_OUTER_INTERVAL_LOCALIZATION__"
            "REPAIR_FAILED_MIDPOINT_NODE"
        )
    elif acceptance_passed:
        decision = (
            "HOLD_FIRST_LEVEL_LOCAL_RULE__"
            "RUN_QUARTERPOINT_CONFIRMATION"
        )
    else:
        decision = (
            "ADOPT_INTERVAL_ERROR_MAP__"
            "BISECT_DOMINANT_INTERVALS"
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
    M5251.write_csv(MIDPOINT_ROWS, midpoint_summary_rows)
    M5251.write_csv(INTERVAL_ROWS, local_interval_rows)
    M5251.write_csv(COMPOSITE_ROWS, composite_rows)
    M5251.write_csv(VALIDATION, validations)
    M5251.atomic_text(
        DOCUMENT,
        render_document(
            local_interval_rows, summary, validations, decision
        ),
    )
    result = {
        "marker": MARKER,
        "revision": REVISION,
        "manifest_hash": manifest["manifest_hash"],
        "decision": decision,
        "integrity_passed": integrity_passed,
        "acceptance_passed": acceptance_passed,
        "failed_acceptance_gates": [
            row["gate"]
            for row in validations
            if row["gate_kind"] == "acceptance"
            and not bool(row["passed"])
        ],
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
        raise RuntimeError("5253 integrity failed")
    return result


def run_single_node(node_id: str) -> dict[str, Any]:
    configure_node_engine()
    result = M5251.run_node(node_id)
    result["summary"]["internal_fixed_field_semantics"] = (
        "ENDPOINT_LINEAR_REFERENCE_DIAGNOSTIC_ONLY"
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
    M5251.write_csv(MIDPOINT_ROWS, midpoint_nodes())
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
