from __future__ import annotations

import argparse
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

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5252"
NODES = SOURCE / "nodes"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5251 = (
    POST
    / "scripts"
    / "Y5_R2FR_5251_order5_backbone_paired_transport_rebuild.py"
)
SOURCE_5251 = POST / "source-intake" / "functional_rg" / "5251"
MANIFEST_5251 = SOURCE_5251 / "order5_backbone_manifest.json"
RESULT_5251 = SOURCE_5251 / "order5_backbone_result.json"
VALIDATION_5251 = RESIDUALS / "P8_Y5_BRR545_5251_VALIDATION.csv"
MANIFEST_5241 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5241"
    / "decay_angle_order9_manifest.json"
)
RESULT_5241 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5241"
    / "decay_angle_order9_result.json"
)
NODE_ROWS_5241 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5241"
    / "decay_angle_order9_node_summary.csv"
)
RESULT_5247 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5247"
    / "Q03_corrected_inner_slice_result.json"
)
EXTRAPOLATION_5247 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5247"
    / "Q03_corrected_regulator_extrapolation.csv"
)
RESULT_5249 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5249"
    / "Q05_corrected_inner_slice_result.json"
)
EXTRAPOLATION_5249 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5249"
    / "Q05_corrected_regulator_extrapolation.csv"
)

MANIFEST = SOURCE / "full_order9_manifest.json"
DRY_RUN = SOURCE / "full_order9_dry_run.json"
STATUS = SOURCE / "full_order9_status.json"
RESULT = SOURCE / "full_order9_result.json"
NODE_SUMMARY = SOURCE / "full_order9_node_summary.csv"
CUBATURE_ROWS = SOURCE / "full_order9_cubature.csv"
PROFILE_ROWS = SOURCE / "full_order9_profile.csv"
CHEBYSHEV_ROWS = SOURCE / "full_order9_chebyshev_coefficients.csv"
FORMAL_INVENTORY = (
    SOURCE / "formalization_workbench_start_inventory.csv"
)
FORMAL_DIFF = SOURCE / "formalization_workbench_run_diff.csv"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5252_VALIDATION.csv"
DOCUMENT = (
    POST
    / "5252-Y5-R2FR-Q01-Q07-full-order9-paired-transport-and-outer-gate.md"
)
COMPLETE = SOURCE / "COMPLETE.marker"

CHECKPOINT = 5252
PARENT_CHECKPOINT = 5251
MARKER = "MTS_5252_Q01_Q07_FULL_ORDER9_PAIRED_TRANSPORT_OUTER_GATE"
REVISION = "Q01-Q07-full-order9-paired-transport-outer-gate-v1"
TRANSPORT_CACHE_REVISION = (
    "Q01-Q07-full-order9-paired-transport-outer-gate-v1"
)
TARGET_NODE_IDS = ("Q01", "Q07")
BACKBONE_NODE_IDS = ("Q00", "Q02", "Q04", "Q06", "Q08")
PRECORRECTED_NODE_IDS = ("Q03", "Q05")
ALL_NODE_IDS = tuple(f"Q{index:02d}" for index in range(9))
OUTER_ORDERS = (3, 5, 9)
INNER_ORDERS = (128, 512)
DEFAULT_MAX_WORKERS = 2
MAXIMUM_OUTER_RELATIVE_DIFFERENCE = 0.2
MAXIMUM_CHEBYSHEV_TAIL_FRACTION = 0.2
MAXIMUM_RECONSTRUCTION_RESIDUAL = 2.0e-12
MAXIMUM_RUNTIME_SECONDS = 8.0 * 60.0 * 60.0
HISTORIC_FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"Unable to load {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


M5251 = load_module(SCRIPT_5251, "mts_5251_for_5252")


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> list[dict[str, str]]:
    paths = [
        Path(__file__),
        SCRIPT_5251,
        MANIFEST_5251,
        RESULT_5251,
        VALIDATION_5251,
        MANIFEST_5241,
        RESULT_5241,
        NODE_ROWS_5241,
        RESULT_5247,
        EXTRAPOLATION_5247,
        RESULT_5249,
        EXTRAPOLATION_5249,
    ]
    paths.extend(
        SOURCE_5251 / "nodes" / node_id / "node_result.json"
        for node_id in BACKBONE_NODE_IDS
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def configure_node_engine() -> None:
    M5251.SOURCE = SOURCE
    M5251.NODES = NODES
    M5251.MANIFEST = MANIFEST
    M5251.MARKER = MARKER
    M5251.REVISION = REVISION
    M5251.TRANSPORT_CACHE_REVISION = TRANSPORT_CACHE_REVISION
    M5251.CHECKPOINT = CHECKPOINT
    M5251.PARENT_CHECKPOINT = PARENT_CHECKPOINT
    M5251.TARGET_NODE_IDS = TARGET_NODE_IDS
    M5251.RESULT_5250 = RESULT_5251
    M5251.BACKBONE_BASE_RESOLUTION_LADDER = (
        M5251.BACKBONE_BASE_RESOLUTION_LADDER
    )


def prepare() -> tuple[dict[str, Any], dict[str, Any]]:
    configure_node_engine()
    parent = read_json(RESULT_5251)
    result_5247 = read_json(RESULT_5247)
    result_5249 = read_json(RESULT_5249)
    outer_manifest = read_json(MANIFEST_5241)
    target_nodes = [
        row
        for row in outer_manifest["outer_nodes"]
        if row["order9_node_id"] in TARGET_NODE_IDS
    ]
    formal_rows = M5251.formal_inventory_rows()
    formal_start_digest = M5251.inventory_digest(formal_rows)
    M5251.write_csv(FORMAL_INVENTORY, formal_rows)
    manifest = {
        "marker": MARKER,
        "revision": REVISION,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "parent_decision": parent["decision"],
        "target_node_ids": list(TARGET_NODE_IDS),
        "target_nodes": target_nodes,
        "all_node_ids": list(ALL_NODE_IDS),
        "outer_rule_rows": outer_manifest["outer_rule_rows"],
        "base_resolution_ladder": list(
            M5251.BACKBONE_BASE_RESOLUTION_LADDER
        ),
        "maximum_projective_step": M5251.M5246.MAXIMUM_PROJECTIVE_STEP,
        "maximum_reciprocal_residual": (
            M5251.M5246.MAXIMUM_RECIPROCAL_RESIDUAL
        ),
        "maximum_outer_relative_difference": (
            MAXIMUM_OUTER_RELATIVE_DIFFERENCE
        ),
        "maximum_chebyshev_tail_fraction": (
            MAXIMUM_CHEBYSHEV_TAIL_FRACTION
        ),
        "maximum_runtime_seconds": MAXIMUM_RUNTIME_SECONDS,
        "formalization_workbench_start_digest": formal_start_digest,
        "formalization_workbench_start_file_count": len(formal_rows),
        "historic_formalization_workbench_digest": (
            HISTORIC_FORMAL_BASELINE
        ),
        "historic_formalization_digest_matches_start": (
            formal_start_digest == HISTORIC_FORMAL_BASELINE
        ),
        "source_files": source_rows(),
        "claim_boundary": {
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "This closes one decay-angle order-9 slice only. A "
                "numeric UV coefficient still requires soft-energy and "
                "endpoint-cutoff convergence."
            ),
        },
    }
    manifest["manifest_hash"] = M5251.serialized_hash(manifest)
    parent_validation = read_csv(VALIDATION_5251)
    backbone_results = [
        read_json(
            SOURCE_5251 / "nodes" / node_id / "node_result.json"
        )
        for node_id in BACKBONE_NODE_IDS
    ]
    rules9 = [
        row
        for row in outer_manifest["outer_rule_rows"]
        if int(row["outer_rule_order"]) == 9
    ]
    checks = {
        "source_paths_exist_and_match": all(
            Path(row["path"]).exists()
            and digest(Path(row["path"])) == row["sha256"]
            for row in manifest["source_files"]
        ),
        "parent_5251_accepted": (
            parent["integrity_passed"]
            and parent["acceptance_passed"]
            and parent["decision"]
            == (
                "ADOPT_CORRECTED_ORDER5_BACKBONE__"
                "REBUILD_Q01_Q07_FOR_FULL_ORDER9"
            )
            and all(
                row["passed"] == "True"
                for row in parent_validation
                if row["gate_kind"] in ("integrity", "acceptance")
            )
        ),
        "backbone_results_accepted": (
            {row["node_id"] for row in backbone_results}
            == set(BACKBONE_NODE_IDS)
            and all(
                row["integrity_passed"] and row["acceptance_passed"]
                for row in backbone_results
            )
        ),
        "Q03_Q05_results_accepted": (
            result_5247["integrity_passed"]
            and result_5247["acceptance_passed"]
            and result_5249["integrity_passed"]
            and result_5249["acceptance_passed"]
        ),
        "target_nodes_exact": (
            {row["order9_node_id"] for row in target_nodes}
            == set(TARGET_NODE_IDS)
            and len(target_nodes) == len(TARGET_NODE_IDS)
        ),
        "order9_rule_exact": (
            {row["order9_node_id"] for row in rules9}
            == set(ALL_NODE_IDS)
            and len(rules9) == len(ALL_NODE_IDS)
        ),
        "formal_tree_stable_during_prepare": (
            M5251.tree_digest(FORMAL) == formal_start_digest
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
        "manifest_hash": manifest["manifest_hash"],
        "dry_run_passed": all(checks.values()),
        "checks": checks,
        "warnings": {
            "historic_formalization_digest_matches_start": (
                manifest[
                    "historic_formalization_digest_matches_start"
                ]
            ),
            "handling": (
                "The current 8,760-file workbench is frozen as the 5252 "
                "start snapshot; historical drift remains a provenance "
                "warning rather than being silently relabelled."
            ),
        },
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    return manifest, dry_run


def launch_workers(max_workers: int) -> dict[str, int]:
    pending = list(TARGET_NODE_IDS)
    running: dict[str, tuple[subprocess.Popen[Any], Any]] = {}
    return_codes: dict[str, int] = {}
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    while pending or running:
        while pending and len(running) < max_workers:
            node_id = pending.pop(0)
            paths = M5251.node_paths(node_id)
            paths["root"].mkdir(parents=True, exist_ok=True)
            log_handle = (
                paths["root"] / "worker.log"
            ).open("a", encoding="utf-8")
            process = subprocess.Popen(
                [
                    sys.executable,
                    str(Path(__file__)),
                    "--worker-node",
                    node_id,
                ],
                cwd=ROOT,
                stdout=log_handle,
                stderr=subprocess.STDOUT,
                env=environment,
                text=True,
            )
            running[node_id] = (process, log_handle)
        completed = []
        for node_id, (process, log_handle) in running.items():
            return_code = process.poll()
            if return_code is None:
                continue
            log_handle.close()
            return_codes[node_id] = return_code
            completed.append(node_id)
        for node_id in completed:
            del running[node_id]
        node_status = {}
        for node_id in TARGET_NODE_IDS:
            path = M5251.node_paths(node_id)["status"]
            node_status[node_id] = (
                read_json(path)
                if path.exists()
                else {
                    "node_id": node_id,
                    "status": (
                        "PENDING"
                        if node_id in pending
                        else (
                            "STARTING"
                            if node_id in running
                            else "UNKNOWN"
                        )
                    ),
                }
            )
        M5251.atomic_json(
            STATUS,
            {
                "marker": MARKER,
                "status": (
                    "RUNNING" if pending or running else "WORKERS_DONE"
                ),
                "pending": pending,
                "running": sorted(running),
                "return_codes": return_codes,
                "nodes": node_status,
            },
        )
        if pending or running:
            time.sleep(5.0)
    return return_codes


def node_result_values(path: Path) -> dict[int, complex]:
    return M5251.node_result_values(read_json(path))


def corrected_values() -> tuple[
    dict[str, dict[int, complex]],
    dict[str, dict[str, Any]],
]:
    values: dict[str, dict[int, complex]] = {}
    provenance: dict[str, dict[str, Any]] = {}
    for node_id in BACKBONE_NODE_IDS:
        path = SOURCE_5251 / "nodes" / node_id / "node_result.json"
        result = read_json(path)
        values[node_id] = M5251.node_result_values(result)
        provenance[node_id] = {
            "source_checkpoint": 5251,
            "integrity_passed": result["integrity_passed"],
            "acceptance_passed": result["acceptance_passed"],
            "source_path": str(path),
        }
    for node_id, checkpoint, result_path, extrapolation_path in (
        ("Q03", 5247, RESULT_5247, EXTRAPOLATION_5247),
        ("Q05", 5249, RESULT_5249, EXTRAPOLATION_5249),
    ):
        result = read_json(result_path)
        values[node_id] = M5251.physical_values(extrapolation_path)
        provenance[node_id] = {
            "source_checkpoint": checkpoint,
            "integrity_passed": result["integrity_passed"],
            "acceptance_passed": result["acceptance_passed"],
            "source_path": str(extrapolation_path),
        }
    for node_id in TARGET_NODE_IDS:
        path = M5251.node_paths(node_id)["result"]
        result = read_json(path)
        values[node_id] = M5251.node_result_values(result)
        provenance[node_id] = {
            "source_checkpoint": 5252,
            "integrity_passed": result["integrity_passed"],
            "acceptance_passed": result["acceptance_passed"],
            "source_path": str(path),
        }
    return values, provenance


def build_node_rows(
    values: dict[str, dict[int, complex]],
    provenance: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    outer_manifest = read_json(MANIFEST_5241)
    fixed = M5251.fixed_node_values()
    nodes = {
        row["order9_node_id"]: row
        for row in outer_manifest["outer_nodes"]
    }
    rows = []
    for node_id in ALL_NODE_IDS:
        node = nodes[node_id]
        corrected_512 = values[node_id][512]
        rows.append(
            {
                "order9_node_id": node_id,
                "decay_cosine": float(node["decay_cosine"]),
                "source_checkpoint": provenance[node_id][
                    "source_checkpoint"
                ],
                "source_path": provenance[node_id]["source_path"],
                "integrity_passed": provenance[node_id][
                    "integrity_passed"
                ],
                "acceptance_passed": provenance[node_id][
                    "acceptance_passed"
                ],
                "order128_subtracted_real": values[node_id][128].real,
                "order128_subtracted_imaginary": (
                    values[node_id][128].imag
                ),
                "order512_subtracted_real": corrected_512.real,
                "order512_subtracted_imaginary": corrected_512.imag,
                "fixed_order512_real": fixed[node_id][512].real,
                "fixed_order512_imaginary": fixed[node_id][512].imag,
                "relative_change_512": (
                    abs(corrected_512 - fixed[node_id][512])
                    / max(abs(fixed[node_id][512]), 1.0)
                ),
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def build_cubature(
    values: dict[str, dict[int, complex]],
) -> tuple[list[dict[str, Any]], dict[int, dict[int, complex]]]:
    outer_manifest = read_json(MANIFEST_5241)
    rules_by_order = {
        order: [
            row
            for row in outer_manifest["outer_rule_rows"]
            if int(row["outer_rule_order"]) == order
        ]
        for order in OUTER_ORDERS
    }
    cubature = {
        order: {
            inner_order: M5251.cubature_value(
                rules_by_order[order], values, inner_order
            )
            for inner_order in INNER_ORDERS
        }
        for order in OUTER_ORDERS
    }
    rows = [
        {
            "outer_rule_order": order,
            "inner_quadrature_order": inner_order,
            "value_real": cubature[order][inner_order].real,
            "value_imaginary": cubature[order][inner_order].imag,
            "fully_corrected": True,
            "remaining_node_ids": "",
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        for order in OUTER_ORDERS
        for inner_order in INNER_ORDERS
    ]
    return rows, cubature


def profile_and_chebyshev(
    node_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, float]]:
    ordered = sorted(node_rows, key=lambda row: row["decay_cosine"])
    coordinates = np.asarray(
        [
            row["decay_cosine"] / M5251.M5240.ANGULAR_LIMIT
            for row in ordered
        ],
        dtype=np.float64,
    )
    values = np.asarray(
        [
            complex(
                row["order512_subtracted_real"],
                row["order512_subtracted_imaginary"],
            )
            for row in ordered
        ],
        dtype=np.complex128,
    )
    real_coefficients = np.polynomial.chebyshev.chebfit(
        coordinates, values.real, 8
    )
    imaginary_coefficients = np.polynomial.chebyshev.chebfit(
        coordinates, values.imag, 8
    )
    coefficients = real_coefficients + 1.0j * imaginary_coefficients
    total_norm = float(np.linalg.norm(coefficients))
    tail_norm = float(np.linalg.norm(coefficients[5:]))
    tail_fraction = tail_norm / max(total_norm, 1.0e-300)
    magnitudes = np.abs(values)
    profile_rows = []
    for index, (node, value) in enumerate(zip(ordered, values)):
        profile_rows.append(
            {
                "order9_node_id": node["order9_node_id"],
                "decay_cosine": node["decay_cosine"],
                "subtracted_real": value.real,
                "subtracted_imaginary": value.imag,
                "magnitude": abs(value),
                "left_neighbor_jump": (
                    abs(value - values[index - 1])
                    if index > 0
                    else ""
                ),
                "right_neighbor_jump": (
                    abs(values[index + 1] - value)
                    if index + 1 < len(values)
                    else ""
                ),
                "source_checkpoint": node["source_checkpoint"],
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    coefficient_rows = [
        {
            "degree": degree,
            "coefficient_real": coefficient.real,
            "coefficient_imaginary": coefficient.imag,
            "coefficient_magnitude": abs(coefficient),
            "in_high_order_tail": degree >= 5,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        for degree, coefficient in enumerate(coefficients)
    ]
    median_magnitude = float(np.median(magnitudes))
    maximum_magnitude = float(np.max(magnitudes))
    summary = {
        "chebyshev_total_norm": total_norm,
        "chebyshev_degree5_to8_tail_norm": tail_norm,
        "chebyshev_degree5_to8_tail_fraction": tail_fraction,
        "maximum_node_magnitude": maximum_magnitude,
        "median_node_magnitude": median_magnitude,
        "maximum_to_median_node_ratio": (
            maximum_magnitude / max(median_magnitude, 1.0e-300)
        ),
    }
    return profile_rows, coefficient_rows, summary


def validation_rows(
    manifest: dict[str, Any],
    node_results: list[dict[str, Any]],
    node_rows: list[dict[str, Any]],
    cubature: dict[int, dict[int, complex]],
    profile: dict[str, float],
    summary: dict[str, Any],
    elapsed: float,
) -> list[dict[str, Any]]:
    fixed_values = M5251.fixed_node_values()
    outer_manifest = read_json(MANIFEST_5241)
    fixed_cubature = {
        order: M5251.cubature_value(
            [
                row
                for row in outer_manifest["outer_rule_rows"]
                if int(row["outer_rule_order"]) == order
            ],
            fixed_values,
            512,
        )
        for order in OUTER_ORDERS
    }
    reported = read_json(RESULT_5241)["cubature_values"]
    reconstruction_residual = max(
        abs(
            fixed_cubature[order]
            - complex(
                float(reported[str(order)]["real"]),
                float(reported[str(order)]["imaginary"]),
            )
        )
        for order in OUTER_ORDERS
    )
    order35 = summary["order3_to_order5_relative_difference"]
    order59 = summary["order5_to_order9_relative_difference"]
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
            "Q01_Q07_RESULTS_PRESENT",
            {row["node_id"] for row in node_results}
            == set(TARGET_NODE_IDS),
            sorted(row["node_id"] for row in node_results),
            list(TARGET_NODE_IDS),
        ),
        (
            "acceptance",
            "Q01_Q07_NODE_GATES_PASS",
            all(
                row["integrity_passed"] and row["acceptance_passed"]
                for row in node_results
            ),
            (
                f"{sum(row['integrity_passed'] and row['acceptance_passed'] for row in node_results)}"
                f"/{len(TARGET_NODE_IDS)}"
            ),
            f"{len(TARGET_NODE_IDS)}/{len(TARGET_NODE_IDS)}",
        ),
        (
            "integrity",
            "ALL_NINE_CORRECTED_NODES_ACCEPTED",
            (
                {row["order9_node_id"] for row in node_rows}
                == set(ALL_NODE_IDS)
                and all(
                    row["integrity_passed"]
                    and row["acceptance_passed"]
                    for row in node_rows
                )
            ),
            len(node_rows),
            len(ALL_NODE_IDS),
        ),
        (
            "integrity",
            "FIXED_CUBATURE_RECONSTRUCTS_5241",
            reconstruction_residual <= MAXIMUM_RECONSTRUCTION_RESIDUAL,
            reconstruction_residual,
            MAXIMUM_RECONSTRUCTION_RESIDUAL,
        ),
        (
            "integrity",
            "FULL_CORRECTED_CUBATURE_FINITE",
            all(
                math.isfinite(cubature[order][inner_order].real)
                and math.isfinite(cubature[order][inner_order].imag)
                for order in OUTER_ORDERS
                for inner_order in INNER_ORDERS
            ),
            "finite",
            "finite",
        ),
        (
            "acceptance",
            "OUTER_ORDER_3_TO_5_CONVERGENCE",
            order35 <= MAXIMUM_OUTER_RELATIVE_DIFFERENCE,
            order35,
            MAXIMUM_OUTER_RELATIVE_DIFFERENCE,
        ),
        (
            "acceptance",
            "OUTER_ORDER_5_TO_9_CONVERGENCE",
            order59 <= MAXIMUM_OUTER_RELATIVE_DIFFERENCE,
            order59,
            MAXIMUM_OUTER_RELATIVE_DIFFERENCE,
        ),
        (
            "acceptance",
            "ORDER9_CHEBYSHEV_TAIL_DECAY",
            profile["chebyshev_degree5_to8_tail_fraction"]
            <= MAXIMUM_CHEBYSHEV_TAIL_FRACTION,
            profile["chebyshev_degree5_to8_tail_fraction"],
            MAXIMUM_CHEBYSHEV_TAIL_FRACTION,
        ),
        (
            "diagnostic",
            "ORDER9_INNER_128_TO_512_STABILITY",
            math.isfinite(
                summary["order9_inner128_to512_relative_difference"]
            ),
            summary["order9_inner128_to512_relative_difference"],
            "finite; node-level regulator gates own acceptance",
        ),
        (
            "integrity",
            "FORMALIZATION_WORKBENCH_UNCHANGED_DURING_5252",
            summary["formalization_workbench_modified_file_count"] == 0,
            summary["formalization_workbench_modified_file_count"],
            0,
        ),
        (
            "provenance",
            "HISTORIC_FORMAL_BASELINE_MATCHES_5252_START",
            manifest["historic_formalization_digest_matches_start"],
            manifest["formalization_workbench_start_digest"],
            manifest["historic_formalization_workbench_digest"],
        ),
        (
            "integrity",
            "RUNTIME_BOUNDED",
            elapsed <= MAXIMUM_RUNTIME_SECONDS,
            elapsed,
            MAXIMUM_RUNTIME_SECONDS,
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
    node_rows: list[dict[str, Any]],
    summary: dict[str, Any],
    profile: dict[str, float],
    validations: list[dict[str, Any]],
    decision: str,
) -> str:
    node_lines = [
        (
            f"- {row['order9_node_id']}: "
            f"`({row['order512_subtracted_real']}"
            f"{row['order512_subtracted_imaginary']:+}j)`, "
            f"source checkpoint `{row['source_checkpoint']}`, "
            f"relative correction `{row['relative_change_512']:.12g}`."
        )
        for row in node_rows
    ]
    failed_acceptance = [
        row["gate"]
        for row in validations
        if row["gate_kind"] == "acceptance" and not bool(row["passed"])
    ]
    next_target = (
        "Proceed to the soft-energy and endpoint-cutoff grid."
        if not failed_acceptance
        else (
            "Localize the corrected decay-angle profile by interval and "
            "build a piecewise/adaptive outer rule before increasing the "
            "global order; do not promote this slice."
        )
    )
    return "\n".join(
        [
            "# 5252 - Q01/Q07 paired transport and full order-9 gate",
            "",
            "## Calculation",
            "",
            "Q01 and Q07 receive the same reciprocal-projective collision "
            "and chamber-boundary transport used for the accepted Q00-Q08 "
            "backbone. All nine corrected node values are then assembled "
            "under the original order-3/5/9 weights and the original "
            "0.2 convergence and Chebyshev-tail thresholds.",
            "",
            "## Corrected node profile",
            "",
            *node_lines,
            "",
            "## Full corrected cubature",
            "",
            f"- Order 3: `({summary['order3_real']}"
            f"{summary['order3_imaginary']:+}j)`.",
            f"- Order 5: `({summary['order5_real']}"
            f"{summary['order5_imaginary']:+}j)`.",
            f"- Order 9: `({summary['order9_real']}"
            f"{summary['order9_imaginary']:+}j)`.",
            f"- Order 3 to 5 relative difference: "
            f"`{summary['order3_to_order5_relative_difference']:.12g}`.",
            f"- Order 5 to 9 relative difference: "
            f"`{summary['order5_to_order9_relative_difference']:.12g}`.",
            f"- Degree 5 to 8 Chebyshev-tail fraction: "
            f"`{profile['chebyshev_degree5_to8_tail_fraction']:.12g}`.",
            f"- Order-9 inner 128/512 relative difference: "
            f"`{summary['order9_inner128_to512_relative_difference']:.12g}`.",
            "",
            "## Decision",
            "",
            f"`{decision}`",
            "",
            f"Failed acceptance gates: "
            f"`{'|'.join(failed_acceptance) if failed_acceptance else 'none'}`.",
            "",
            "## Protection and claim boundary",
            "",
            f"- Formal-workbench files changed during 5252: "
            f"`{summary['formalization_workbench_modified_file_count']}`.",
            "- No numeric UV coefficient, local-GR extension, or full-MTS "
            "claim follows from this one angular slice.",
            "",
            "## Next exact target",
            "",
            next_target,
            "",
        ]
    )


def execute(max_workers: int) -> dict[str, Any]:
    started = time.perf_counter()
    SOURCE.mkdir(parents=True, exist_ok=True)
    manifest, dry_run = prepare()
    M5251.atomic_json(MANIFEST, manifest)
    M5251.atomic_json(DRY_RUN, dry_run)
    if not dry_run["dry_run_passed"]:
        failed = [
            key
            for key, passed in dry_run["checks"].items()
            if not passed
        ]
        raise RuntimeError(f"5252 dry run failed: {failed}")
    return_codes = launch_workers(max_workers)
    node_results = [
        read_json(M5251.node_paths(node_id)["result"])
        for node_id in TARGET_NODE_IDS
        if M5251.node_paths(node_id)["result"].exists()
    ]
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
            },
        )
        raise RuntimeError(f"5252 workers failed: {worker_failures}")

    values, provenance = corrected_values()
    node_rows = build_node_rows(values, provenance)
    cubature_rows, cubature = build_cubature(values)
    profile_rows, coefficient_rows, profile = profile_and_chebyshev(
        node_rows
    )
    order35 = abs(cubature[3][512] - cubature[5][512]) / max(
        abs(cubature[5][512]), 1.0
    )
    order59 = abs(cubature[5][512] - cubature[9][512]) / max(
        abs(cubature[9][512]), 1.0
    )
    formal_after_rows = M5251.formal_inventory_rows()
    formal_diff_rows = M5251.inventory_diff_rows(
        read_csv(FORMAL_INVENTORY), formal_after_rows
    )
    M5251.write_csv(FORMAL_DIFF, formal_diff_rows)
    summary = {
        "order3_real": cubature[3][512].real,
        "order3_imaginary": cubature[3][512].imag,
        "order5_real": cubature[5][512].real,
        "order5_imaginary": cubature[5][512].imag,
        "order9_real": cubature[9][512].real,
        "order9_imaginary": cubature[9][512].imag,
        "order3_to_order5_relative_difference": order35,
        "order5_to_order9_relative_difference": order59,
        "order9_inner128_to512_relative_difference": (
            abs(cubature[9][128] - cubature[9][512])
            / max(abs(cubature[9][512]), 1.0)
        ),
        "formalization_workbench_start_digest": manifest[
            "formalization_workbench_start_digest"
        ],
        "formalization_workbench_end_digest": (
            M5251.inventory_digest(formal_after_rows)
        ),
        "formalization_workbench_modified_file_count": len(
            formal_diff_rows
        ),
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    elapsed = time.perf_counter() - started
    validations = validation_rows(
        manifest,
        node_results,
        node_rows,
        cubature,
        profile,
        summary,
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
    decision = (
        "INVALID_FULL_ORDER9_PAIRED_TRANSPORT_CHECKPOINT"
        if not integrity_passed
        else (
            "ADOPT_FULLY_CORRECTED_ORDER9_DECAY_ANGLE_CUBATURE__"
            "PROCEED_TO_SOFT_ENERGY_ENDPOINT_GRID"
            if acceptance_passed
            else (
                "HOLD_FULL_ORDER9_CUBATURE__"
                "LOCALIZE_CORRECTED_OUTER_PROFILE"
            )
        )
    )
    M5251.write_csv(NODE_SUMMARY, node_rows)
    M5251.write_csv(CUBATURE_ROWS, cubature_rows)
    M5251.write_csv(PROFILE_ROWS, profile_rows)
    M5251.write_csv(CHEBYSHEV_ROWS, coefficient_rows)
    M5251.write_csv(VALIDATION, validations)
    M5251.atomic_text(
        DOCUMENT,
        render_document(
            node_rows, summary, profile, validations, decision
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
        "profile": profile,
        "worker_return_codes": return_codes,
        "formalization_workbench_digest": summary[
            "formalization_workbench_end_digest"
        ],
        "historic_formalization_digest_matches_start": manifest[
            "historic_formalization_digest_matches_start"
        ],
        "elapsed_seconds": elapsed,
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
            "worker_return_codes": return_codes,
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
        raise RuntimeError("5252 integrity failed")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--worker-node",
        choices=TARGET_NODE_IDS,
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=DEFAULT_MAX_WORKERS,
    )
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    configure_node_engine()
    if arguments.worker_node:
        result = M5251.run_node(arguments.worker_node)
        print(json.dumps(result, indent=2, sort_keys=True))
        return
    manifest, dry_run = prepare()
    SOURCE.mkdir(parents=True, exist_ok=True)
    M5251.atomic_json(MANIFEST, manifest)
    M5251.atomic_json(DRY_RUN, dry_run)
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
