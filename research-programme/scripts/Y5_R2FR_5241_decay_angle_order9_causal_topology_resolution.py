from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import shutil
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5241"
SOURCE_5240 = POST / "source-intake" / "functional_rg" / "5240"
RESIDUALS = POST / "source-intake" / "mts_residuals"
NODE_CACHE = SOURCE / "node-cache"

SCRIPT_5240 = (
    POST
    / "scripts"
    / "Y5_R2FR_5240_two_angular_nested_A00_causal_cubature_pilot.py"
)
RESULT_5240 = SOURCE_5240 / "two_angular_nested_A00_result.json"
VALIDATION_5240 = RESIDUALS / "P8_Y5_BRR545_5240_VALIDATION.csv"
OLD_NODE_CACHE = SOURCE_5240 / "node-cache"

MANIFEST = SOURCE / "decay_angle_order9_manifest.json"
MANIFEST_ROWS = SOURCE / "decay_angle_order9_nodes.csv"
DRY_RUN = SOURCE / "decay_angle_order9_dry_run.json"
RESULT = SOURCE / "decay_angle_order9_result.json"
OUTER_TRACK_ROWS = SOURCE / "decay_angle_outer_branch_track_audit.csv"
NODE_ROWS = SOURCE / "decay_angle_order9_node_summary.csv"
ZERO_ROWS = SOURCE / "decay_angle_order9_structural_zero_audit.csv"
WINDING_ROWS = SOURCE / "decay_angle_order9_winding_intervals.csv"
WINDING_CACHE = SOURCE / "decay_angle_order9_winding_cache.json"
CLOSURE_ROWS = SOURCE / "decay_angle_order9_dynamic_closure.csv"
POLE_ROWS = SOURCE / "decay_angle_order9_pole_catalog.csv"
RESIDUE_ROWS = SOURCE / "decay_angle_order9_residue_fits.csv"
RULE_ROWS = SOURCE / "decay_angle_order9_rule_audit.csv"
CUBATURE_ROWS = SOURCE / "decay_angle_order9_cubature.csv"
PROFILE_ROWS = SOURCE / "decay_angle_order9_profile.csv"
TRANSITION_ROWS = SOURCE / "decay_angle_topology_transition_intervals.csv"
CHEBYSHEV_ROWS = SOURCE / "decay_angle_order9_chebyshev_coefficients.csv"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5241_VALIDATION.csv"
DOCUMENT = (
    POST
    / "5241-Y5-R2FR-decay-angle-order9-causal-topology-resolution.md"
)

MARKER = "MTS_5241_DECAY_ANGLE_ORDER9_CAUSAL_TOPOLOGY_RESOLUTION"
REVISION = "decay-angle-order9-causal-topology-resolution-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)

OUTER_ORDERS = (3, 5, 9)
MASTER_ORDER = 9
EXPECTED_REUSED_NODES = 5
EXPECTED_NEW_NODES = 4
EXPECTED_TOTAL_NODES = 9
EXPECTED_BASE_JOBS = 12
EXPECTED_NEW_JOBS = EXPECTED_NEW_NODES * EXPECTED_BASE_JOBS
MAXIMUM_OUTER_RELATIVE_DIFFERENCE = 0.2
MAXIMUM_CHEBYSHEV_TAIL_FRACTION = 0.2
MAXIMUM_RUNTIME_SECONDS = 4.0 * 60.0 * 60.0


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5240 = load_module(SCRIPT_5240, "mts_5240_for_5241")


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(str(item.relative_to(path)).replace("\\", "/").encode())
        value.update(digest(item).encode())
    return value.hexdigest()


def serialized_hash(value: Any) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    temporary.replace(path)


def atomic_json(path: Path, value: Any) -> None:
    atomic_text(path, json.dumps(value, indent=2, sort_keys=True) + "\n")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        atomic_text(path, "")
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
    temporary.replace(path)


def complex_value(value: Any) -> complex:
    return M5240.complex_value(value)


def complex_row(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def source_rows() -> list[dict[str, str]]:
    paths = [SCRIPT_5240, RESULT_5240, VALIDATION_5240]
    paths.extend(sorted(OLD_NODE_CACHE.glob("Y*.json")))
    return [{"path": str(path), "sha256": digest(path)} for path in paths]


def old_failure_signature() -> list[str]:
    return [
        row["gate"]
        for row in read_csv(VALIDATION_5240)
        if row["passed"] != "True"
    ]


def master_nodes() -> list[dict[str, Any]]:
    coordinates, _, residual = M5240.interpolatory_rule(
        MASTER_ORDER,
        -M5240.ANGULAR_LIMIT,
        M5240.ANGULAR_LIMIT,
    )
    if residual > M5240.MAXIMUM_OUTER_RULE_MOMENT_RESIDUAL:
        raise RuntimeError("order-9 rule fails its moment audit")
    old_manifest = read_json(M5240.MANIFEST_JSON)
    old_nodes = list(old_manifest["outer_nodes"])
    rows: list[dict[str, Any]] = []
    new_index = 0
    for index, coordinate in enumerate(coordinates):
        candidate = min(
            old_nodes,
            key=lambda row: abs(
                float(row["decay_cosine"]) - float(coordinate)
            ),
        )
        mismatch = abs(
            float(candidate["decay_cosine"]) - float(coordinate)
        )
        reused = mismatch <= 2.0e-12
        if reused:
            execution_id = candidate["outer_node_id"]
            source_cache = OLD_NODE_CACHE / f"{execution_id}.json"
        else:
            execution_id = f"N{new_index:02d}"
            source_cache = NODE_CACHE / f"{execution_id}.json"
            new_index += 1
        rows.append(
            {
                "order9_node_id": f"Q{index:02d}",
                "master_index": index,
                "decay_cosine": float(coordinate),
                "execution_node_id": execution_id,
                "reused_from_5240": reused,
                "source_cache": str(source_cache),
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def rule_rows(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for order in OUTER_ORDERS:
        coordinates, weights, residual = M5240.interpolatory_rule(
            order,
            -M5240.ANGULAR_LIMIT,
            M5240.ANGULAR_LIMIT,
        )
        for coordinate, weight in zip(coordinates, weights):
            node = min(
                nodes,
                key=lambda row: abs(
                    float(row["decay_cosine"]) - float(coordinate)
                ),
            )
            mismatch = abs(
                float(node["decay_cosine"]) - float(coordinate)
            )
            if mismatch > 2.0e-12:
                raise RuntimeError(f"order {order} is not nested in order 9")
            rows.append(
                {
                    "outer_rule_order": order,
                    "order9_node_id": node["order9_node_id"],
                    "decay_cosine": float(coordinate),
                    "weight_d_decay_cosine": float(weight),
                    "master_node_mismatch": mismatch,
                    "maximum_monomial_moment_residual": residual,
                    "angular_unit_cube_jacobian": 0.25,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    return rows


def build_manifest() -> tuple[
    dict[str, Any],
    dict[str, Any],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    parent_manifest, matches, base_jobs, _ = M5240.build_manifest()
    nodes = master_nodes()
    rules = rule_rows(nodes)
    sources = source_rows()
    manifest = {
        "marker": MARKER,
        "revision": REVISION,
        "parent_checkpoint": 5240,
        "parent_manifest_hash": parent_manifest["manifest_hash"],
        "parent_decision": read_json(RESULT_5240)["decision"],
        "parent_failed_gates": old_failure_signature(),
        "fixed_soft_energy": parent_manifest["fixed_soft_energy"],
        "inner_coordinate": M5240.INNER_COORDINATE,
        "outer_coordinate": M5240.OUTER_COORDINATE,
        "angular_cutoff": M5240.ANGULAR_CUTOFF,
        "angular_domain": [
            -M5240.ANGULAR_LIMIT,
            M5240.ANGULAR_LIMIT,
        ],
        "outer_rule_orders": list(OUTER_ORDERS),
        "master_outer_order": MASTER_ORDER,
        "reused_node_count": sum(
            bool(row["reused_from_5240"]) for row in nodes
        ),
        "new_node_count": sum(
            not bool(row["reused_from_5240"]) for row in nodes
        ),
        "total_node_count": len(nodes),
        "new_nested_job_count": (
            sum(not bool(row["reused_from_5240"]) for row in nodes)
            * len(base_jobs)
        ),
        "base_job_count": len(base_jobs),
        "source_files": sources,
        "outer_nodes": nodes,
        "outer_rule_rows": rules,
        "acceptance_thresholds": {
            "maximum_outer_relative_difference": (
                MAXIMUM_OUTER_RELATIVE_DIFFERENCE
            ),
            "maximum_chebyshev_tail_fraction": (
                MAXIMUM_CHEBYSHEV_TAIL_FRACTION
            ),
            "maximum_winding_projective_step": (
                M5240.M5239.DYNAMIC_PROJECTIVE_STEP_LIMIT
            ),
        },
        "claim_boundary": {
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "Order 9 still covers only two angular coordinates at one "
                "fixed soft energy and one endpoint cutoff."
            ),
        },
    }
    manifest["manifest_hash"] = serialized_hash(manifest)
    return manifest, parent_manifest, matches, base_jobs, rules


def write_manifest_and_dry_run() -> dict[str, Any]:
    manifest, parent_manifest, matches, base_jobs, rules = build_manifest()
    checks = {
        "source_paths_exist_and_match": all(
            Path(row["path"]).exists()
            and digest(Path(row["path"])) == row["sha256"]
            for row in manifest["source_files"]
        ),
        "parent_hold_signature_exact": (
            manifest["parent_failed_gates"]
            == [
                "WINDING_INTERVAL_TRACK_RESOLUTION",
                "OUTER_ORDER_3_TO_5_CONVERGENCE",
            ]
        ),
        "node_accounting_exact": (
            manifest["reused_node_count"] == EXPECTED_REUSED_NODES
            and manifest["new_node_count"] == EXPECTED_NEW_NODES
            and manifest["total_node_count"] == EXPECTED_TOTAL_NODES
        ),
        "new_job_count_bounded": (
            len(base_jobs) == EXPECTED_BASE_JOBS
            and manifest["new_nested_job_count"] == EXPECTED_NEW_JOBS
        ),
        "safe_component_contract_preserved": (
            len(matches) == M5240.EXPECTED_SAFE_COMPONENT_COUNT
            and parent_manifest["material_component_count"]
            == M5240.EXPECTED_MATERIAL_COMPONENT_COUNT
        ),
        "rules_nested_and_exact": (
            len(rules) == sum(OUTER_ORDERS)
            and max(
                float(row["maximum_monomial_moment_residual"])
                for row in rules
            )
            <= M5240.MAXIMUM_OUTER_RULE_MOMENT_RESIDUAL
        ),
        "formal_digest_unchanged": (
            tree_digest(FORMAL) == FORMAL_BASELINE
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
    report = {
        "marker": MARKER,
        "revision": REVISION,
        "dry_run_passed": all(checks.values()),
        "checks": checks,
        "manifest_hash": manifest["manifest_hash"],
        "reused_node_count": manifest["reused_node_count"],
        "new_node_count": manifest["new_node_count"],
        "new_nested_job_count": manifest["new_nested_job_count"],
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(MANIFEST, manifest)
    write_csv(MANIFEST_ROWS, manifest["outer_nodes"])
    write_csv(RULE_ROWS, rules)
    atomic_json(DRY_RUN, report)
    if not report["dry_run_passed"]:
        failed = [key for key, passed in checks.items() if not passed]
        raise RuntimeError(f"5241 dry run failed: {failed}")
    return report


def load_reused_result(node: dict[str, Any]) -> dict[str, Any]:
    path = Path(node["source_cache"])
    payload = read_json(path)
    if payload.get("status") != "COMPLETED":
        raise RuntimeError(f"reused node cache is incomplete: {path}")
    result = payload["result"]
    if (
        abs(
            float(result["decay_cosine"])
            - float(node["decay_cosine"])
        )
        > 2.0e-12
    ):
        raise RuntimeError(f"reused node coordinate mismatch: {path}")
    return result


def canonical_node_row(
    node: dict[str, Any],
    result: dict[str, Any],
    cache_hit: bool,
) -> dict[str, Any]:
    row = M5240.node_summary_row(result, cache_hit)
    return {
        "order9_node_id": node["order9_node_id"],
        "execution_node_id": node["execution_node_id"],
        "decay_cosine": node["decay_cosine"],
        "reused_from_5240": node["reused_from_5240"],
        **{
            key: value
            for key, value in row.items()
            if key not in {"outer_node_id", "decay_cosine"}
        },
    }


def qualify_result_rows(
    node: dict[str, Any],
    result: dict[str, Any],
    field: str,
) -> list[dict[str, Any]]:
    return [
        {
            "order9_node_id": node["order9_node_id"],
            "execution_node_id": node["execution_node_id"],
            "reused_from_5240": node["reused_from_5240"],
            **row,
        }
        for row in result[field]
    ]


def value_from_node(row: dict[str, Any], inner_order: int) -> complex:
    return complex(
        float(row[f"order{inner_order}_subtracted_real"]),
        float(row[f"order{inner_order}_subtracted_imaginary"]),
    )


def cubature(
    nodes: list[dict[str, Any]],
    rules: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[int, complex]]:
    by_id = {row["order9_node_id"]: row for row in nodes}
    values: dict[int, complex] = {}
    rows: list[dict[str, Any]] = []
    for outer_order in OUTER_ORDERS:
        selected = [
            row
            for row in rules
            if int(row["outer_rule_order"]) == outer_order
        ]
        inner_values: dict[int, complex] = {}
        for inner_order in (128, 512):
            value = 0.25 * sum(
                (
                    float(rule["weight_d_decay_cosine"])
                    * value_from_node(
                        by_id[rule["order9_node_id"]],
                        inner_order,
                    )
                    for rule in selected
                ),
                0.0j,
            )
            inner_values[inner_order] = value
        values[outer_order] = inner_values[512]
        rows.append(
            {
                "outer_rule_order": outer_order,
                "outer_node_count": len(selected),
                "outer_node_ids": "|".join(
                    row["order9_node_id"] for row in selected
                ),
                "angular_unit_cube_jacobian": 0.25,
                "covered_normalized_angular_measure": (
                    M5240.ANGULAR_LIMIT**2
                ),
                "inner128_subtracted_real": inner_values[128].real,
                "inner128_subtracted_imaginary": (
                    inner_values[128].imag
                ),
                "inner512_subtracted_real": inner_values[512].real,
                "inner512_subtracted_imaginary": (
                    inner_values[512].imag
                ),
                "nested_inner128_to512_relative_difference": (
                    abs(inner_values[128] - inner_values[512])
                    / max(abs(inner_values[512]), 1.0)
                ),
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows, values


def profile_and_chebyshev(
    node_rows: list[dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, float],
]:
    ordered = sorted(node_rows, key=lambda row: float(row["decay_cosine"]))
    coordinates = np.asarray(
        [
            float(row["decay_cosine"]) / M5240.ANGULAR_LIMIT
            for row in ordered
        ],
        dtype=np.float64,
    )
    values = np.asarray(
        [value_from_node(row, 512) for row in ordered],
        dtype=np.complex128,
    )
    real_coefficients = np.polynomial.chebyshev.chebfit(
        coordinates, values.real, MASTER_ORDER - 1
    )
    imaginary_coefficients = np.polynomial.chebyshev.chebfit(
        coordinates, values.imag, MASTER_ORDER - 1
    )
    coefficients = real_coefficients + 1.0j * imaginary_coefficients
    total_norm = float(np.linalg.norm(coefficients))
    tail_norm = float(np.linalg.norm(coefficients[5:]))
    tail_fraction = tail_norm / max(total_norm, 1.0e-300)
    magnitudes = np.abs(values)
    median_magnitude = float(np.median(magnitudes))
    maximum_magnitude = float(np.max(magnitudes))
    profile_rows: list[dict[str, Any]] = []
    for index, (node, value) in enumerate(zip(ordered, values)):
        left_jump = (
            abs(value - values[index - 1])
            if index > 0
            else None
        )
        right_jump = (
            abs(values[index + 1] - value)
            if index + 1 < len(values)
            else None
        )
        profile_rows.append(
            {
                "order9_node_id": node["order9_node_id"],
                "decay_cosine": node["decay_cosine"],
                "subtracted_real": value.real,
                "subtracted_imaginary": value.imag,
                "magnitude": abs(value),
                "left_neighbor_jump": left_jump,
                "right_neighbor_jump": right_jump,
                "active_pole_count": node["active_pole_count"],
                "geometric_pole_count": node["geometric_pole_count"],
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


def topology_transitions(
    node_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    ordered = sorted(node_rows, key=lambda row: float(row["decay_cosine"]))
    rows: list[dict[str, Any]] = []
    for left, right in zip(ordered[:-1], ordered[1:]):
        active_changed = (
            int(left["active_pole_count"])
            != int(right["active_pole_count"])
        )
        geometric_changed = (
            int(left["geometric_pole_count"])
            != int(right["geometric_pole_count"])
        )
        if not (active_changed or geometric_changed):
            continue
        rows.append(
            {
                "left_node_id": left["order9_node_id"],
                "right_node_id": right["order9_node_id"],
                "left_decay_cosine": left["decay_cosine"],
                "right_decay_cosine": right["decay_cosine"],
                "left_active_poles": left["active_pole_count"],
                "right_active_poles": right["active_pole_count"],
                "left_geometric_poles": left["geometric_pole_count"],
                "right_geometric_poles": right["geometric_pole_count"],
                "active_topology_changed": active_changed,
                "geometric_topology_changed": geometric_changed,
                "interpretation": (
                    "BRACKET_OUTER_TOPOLOGY_TRANSITION__NOT_YET_LOCALIZED"
                ),
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def validation_rows(
    manifest: dict[str, Any],
    node_rows: list[dict[str, Any]],
    zero_rows: list[dict[str, Any]],
    winding_rows: list[dict[str, Any]],
    closure_rows: list[dict[str, Any]],
    pole_rows: list[dict[str, Any]],
    residue_rows: list[dict[str, Any]],
    rules: list[dict[str, Any]],
    cubature_values: dict[int, complex],
    profile_summary: dict[str, float],
    formal_digest: str,
    elapsed: float,
) -> list[dict[str, Any]]:
    active_poles = [
        row for row in pole_rows if bool(row["causal_family_active"])
    ]
    order35 = abs(cubature_values[3] - cubature_values[5]) / max(
        abs(cubature_values[5]), 1.0
    )
    order59 = abs(cubature_values[5] - cubature_values[9]) / max(
        abs(cubature_values[9]), 1.0
    )
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
            "PARENT_FAILURE_SIGNATURE_PRESERVED",
            manifest["parent_failed_gates"]
            == [
                "WINDING_INTERVAL_TRACK_RESOLUTION",
                "OUTER_ORDER_3_TO_5_CONVERGENCE",
            ],
            "|".join(manifest["parent_failed_gates"]),
            (
                "WINDING_INTERVAL_TRACK_RESOLUTION|"
                "OUTER_ORDER_3_TO_5_CONVERGENCE"
            ),
        ),
        (
            "integrity",
            "ORDER9_NODE_ACCOUNTING",
            (
                len(node_rows) == EXPECTED_TOTAL_NODES
                and sum(bool(row["reused_from_5240"]) for row in node_rows)
                == EXPECTED_REUSED_NODES
            ),
            (
                f"{sum(bool(row['reused_from_5240']) for row in node_rows)}"
                f"+{sum(not bool(row['reused_from_5240']) for row in node_rows)}"
            ),
            f"{EXPECTED_REUSED_NODES}+{EXPECTED_NEW_NODES}",
        ),
        (
            "integrity",
            "ALL_OUTER_NODES_PASS_INNER_GATES",
            all(bool(row["node_passed"]) for row in node_rows),
            (
                f"{sum(bool(row['node_passed']) for row in node_rows)}"
                f"/{len(node_rows)}"
            ),
            f"{EXPECTED_TOTAL_NODES}/{EXPECTED_TOTAL_NODES}",
        ),
        (
            "integrity",
            "STRUCTURAL_ZEROS_PERSIST",
            all(bool(row["structural_zero_passed"]) for row in zero_rows),
            (
                f"{sum(bool(row['structural_zero_passed']) for row in zero_rows)}"
                f"/{len(zero_rows)}"
            ),
            "all structural-zero rows",
        ),
        (
            "integrity",
            "DYNAMIC_CLOSURE",
            max(
                float(row["relative_closure_residual"])
                for row in closure_rows
            )
            <= M5240.MAXIMUM_DYNAMIC_CLOSURE_RESIDUAL,
            max(
                float(row["relative_closure_residual"])
                for row in closure_rows
            ),
            M5240.MAXIMUM_DYNAMIC_CLOSURE_RESIDUAL,
        ),
        (
            "integrity",
            "ACTIVE_POLES_FITTED",
            (
                len(residue_rows) == len(active_poles)
                and all(bool(row["fit_passed"]) for row in residue_rows)
            ),
            f"{len(residue_rows)}/{len(active_poles)}",
            "all dynamically active poles",
        ),
        (
            "integrity",
            "OUTER_RULE_MOMENTS",
            max(
                float(row["maximum_monomial_moment_residual"])
                for row in rules
            )
            <= M5240.MAXIMUM_OUTER_RULE_MOMENT_RESIDUAL,
            max(
                float(row["maximum_monomial_moment_residual"])
                for row in rules
            ),
            M5240.MAXIMUM_OUTER_RULE_MOMENT_RESIDUAL,
        ),
        (
            "acceptance",
            "WINDING_INTERVAL_TRACK_RESOLUTION",
            max(
                float(row["maximum_pair_projective_step"])
                for row in winding_rows
            )
            <= M5240.M5239.DYNAMIC_PROJECTIVE_STEP_LIMIT,
            max(
                float(row["maximum_pair_projective_step"])
                for row in winding_rows
            ),
            M5240.M5239.DYNAMIC_PROJECTIVE_STEP_LIMIT,
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
            profile_summary[
                "chebyshev_degree5_to8_tail_fraction"
            ]
            <= MAXIMUM_CHEBYSHEV_TAIL_FRACTION,
            profile_summary[
                "chebyshev_degree5_to8_tail_fraction"
            ],
            MAXIMUM_CHEBYSHEV_TAIL_FRACTION,
        ),
        (
            "integrity",
            "FORMALIZATION_WORKBENCH_UNCHANGED",
            formal_digest == FORMAL_BASELINE,
            formal_digest,
            FORMAL_BASELINE,
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
            "checkpoint": 5241,
            "gate_kind": kind,
            "gate": gate,
            "passed": passed,
            "observed": observed,
            "required": required,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        for kind, gate, passed, observed, required in definitions
    ]


def render_document(
    manifest: dict[str, Any],
    node_rows: list[dict[str, Any]],
    cubature_values: dict[int, complex],
    profile_summary: dict[str, float],
    transitions: list[dict[str, Any]],
    validations: list[dict[str, Any]],
    elapsed: float,
) -> str:
    order35 = abs(cubature_values[3] - cubature_values[5]) / max(
        abs(cubature_values[5]), 1.0
    )
    order59 = abs(cubature_values[5] - cubature_values[9]) / max(
        abs(cubature_values[9]), 1.0
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
        decision = "INVALID_ORDER9_CHECKPOINT"
    elif acceptance_passed:
        decision = "ADOPT_ORDER9_DECAY_ANGLE_CUBATURE"
    else:
        decision = (
            "HOLD_OUTER_CUBATURE__DERIVE_PIECEWISE_DECAY_TOPOLOGY"
        )
    failed = [
        row["gate"] for row in validations if not bool(row["passed"])
    ]
    return "\n".join(
        [
            "# 5241 — Decay-angle order-9 causal-topology resolution",
            "",
            "## Purpose",
            "",
            (
                "Extend 5240 from nested outer orders 3 and 5 to order 9 "
                "without discarding its five completed causal nodes. Four "
                "new nodes are evaluated through the complete 5239 inner "
                "continuation, dynamic winding, pole subtraction, and "
                "E040/E020 extrapolation machinery."
            ),
            "",
            "## Derived measure",
            "",
            (
                "The parent Sobol map gives "
                "`du_soft du_decay = (d cos_soft/2)(d cos_decay/2)`, "
                "so the two-angle Jacobian remains exactly `1/4`."
            ),
            "",
            "## Results",
            "",
            (
                f"- Nodes: `{len(node_rows)}` total; "
                f"`{sum(bool(row['reused_from_5240']) for row in node_rows)}` "
                "reused and "
                f"`{sum(not bool(row['reused_from_5240']) for row in node_rows)}` "
                "new."
            ),
            (
                f"- Order-3→5 relative difference: `{order35:.12g}`."
            ),
            (
                f"- Order-5→9 relative difference: `{order59:.12g}`."
            ),
            (
                "- Order-9 two-angle value: "
                f"`{cubature_values[9].real:.16g} "
                f"{cubature_values[9].imag:+.16g} i`."
            ),
            (
                "- Degree-5..8 Chebyshev tail fraction: "
                f"`{profile_summary['chebyshev_degree5_to8_tail_fraction']:.12g}`."
            ),
            (
                "- Maximum/median node magnitude ratio: "
                f"`{profile_summary['maximum_to_median_node_ratio']:.12g}`."
            ),
            (
                f"- Bracketed outer topology-transition intervals: "
                f"`{len(transitions)}`."
            ),
            f"- Runtime: `{elapsed:.3f} s`.",
            "",
            "## Decision",
            "",
            f"`{decision}`",
            "",
            "Failed gates: "
            + (
                ", ".join(f"`{gate}`" for gate in failed)
                if failed
                else "none"
            )
            + ".",
            "",
            "## Interpretation",
            "",
            (
                "A failed order-5→9 or high-order Chebyshev-tail gate is "
                "not repaired by loosening a tolerance. Together with a "
                "change in active/geometric pole count between adjacent "
                "decay-angle nodes, it means the next mathematical object "
                "is a piecewise decay-angle topology map: localize each "
                "transition, derive its causal winding jump, and integrate "
                "regular subdomains separately."
            ),
            "",
            "## Claim boundary",
            "",
            (
                "This remains one fixed-soft-energy, cutoff two-angle "
                "slice. It is not a numerical UV coefficient, local-GR "
                "derivation, or full-MTS result."
            ),
            "",
            "## Next exact target",
            "",
            (
                "Localize the intervals in "
                f"`{TRANSITION_ROWS.name}` by bisection in decay cosine, "
                "construct the outer dynamic-winding map, and test a "
                "piecewise pole-subtracted outer integral before adding "
                "soft-energy integration."
            ),
            "",
        ]
    )


def remove_project_pycache() -> None:
    target = POST / "scripts" / "__pycache__"
    if target.exists():
        shutil.rmtree(target)


def execute() -> dict[str, Any]:
    started = time.perf_counter()
    dry_run = write_manifest_and_dry_run()
    manifest = read_json(MANIFEST)
    parent_manifest, matches, base_jobs, _ = M5240.build_manifest()
    event = dict(parent_manifest["target_event"])
    tracks, outer_track_rows = M5240.build_outer_branch_tracks(
        matches, event
    )
    write_csv(OUTER_TRACK_ROWS, outer_track_rows)

    NODE_CACHE.mkdir(parents=True, exist_ok=True)
    M5240.NODE_CACHE = NODE_CACHE
    M5240.WINDING_CACHE = WINDING_CACHE
    winding_cache = M5240.load_winding_cache(parent_manifest)

    result_by_canonical_id: dict[str, dict[str, Any]] = {}
    cache_flags: dict[str, bool] = {}
    for node in manifest["outer_nodes"]:
        if bool(node["reused_from_5240"]):
            result = load_reused_result(node)
            cache_hit = True
        else:
            execution_node = {
                "outer_node_id": node["execution_node_id"],
                "master_index": int(node["master_index"]),
                "decay_cosine": float(node["decay_cosine"]),
            }
            result, cache_hit, _, _ = M5240.run_node(
                parent_manifest,
                execution_node,
                base_jobs,
                matches,
                tracks,
                event,
                winding_cache,
            )
        result_by_canonical_id[node["order9_node_id"]] = result
        cache_flags[node["order9_node_id"]] = cache_hit

    node_rows = [
        canonical_node_row(
            node,
            result_by_canonical_id[node["order9_node_id"]],
            cache_flags[node["order9_node_id"]],
        )
        for node in manifest["outer_nodes"]
    ]
    zero_rows = [
        row
        for node in manifest["outer_nodes"]
        for row in qualify_result_rows(
            node,
            result_by_canonical_id[node["order9_node_id"]],
            "zero_rows",
        )
    ]
    winding_rows = [
        row
        for node in manifest["outer_nodes"]
        for row in qualify_result_rows(
            node,
            result_by_canonical_id[node["order9_node_id"]],
            "winding_rows",
        )
    ]
    closure_rows = [
        row
        for node in manifest["outer_nodes"]
        for row in qualify_result_rows(
            node,
            result_by_canonical_id[node["order9_node_id"]],
            "closure_rows",
        )
    ]
    pole_rows = [
        row
        for node in manifest["outer_nodes"]
        for row in qualify_result_rows(
            node,
            result_by_canonical_id[node["order9_node_id"]],
            "pole_rows",
        )
    ]
    residue_rows = [
        row
        for node in manifest["outer_nodes"]
        for row in qualify_result_rows(
            node,
            result_by_canonical_id[node["order9_node_id"]],
            "residue_rows",
        )
    ]
    cubature_rows, cubature_values = cubature(
        node_rows, manifest["outer_rule_rows"]
    )
    profile_rows, coefficient_rows, profile_summary = (
        profile_and_chebyshev(node_rows)
    )
    transitions = topology_transitions(node_rows)

    formal_digest = tree_digest(FORMAL)
    elapsed = time.perf_counter() - started
    validations = validation_rows(
        manifest,
        node_rows,
        zero_rows,
        winding_rows,
        closure_rows,
        pole_rows,
        residue_rows,
        manifest["outer_rule_rows"],
        cubature_values,
        profile_summary,
        formal_digest,
        elapsed,
    )

    write_csv(NODE_ROWS, node_rows)
    write_csv(ZERO_ROWS, zero_rows)
    write_csv(WINDING_ROWS, winding_rows)
    write_csv(CLOSURE_ROWS, closure_rows)
    write_csv(POLE_ROWS, pole_rows)
    write_csv(RESIDUE_ROWS, residue_rows)
    write_csv(CUBATURE_ROWS, cubature_rows)
    write_csv(PROFILE_ROWS, profile_rows)
    write_csv(TRANSITION_ROWS, transitions)
    write_csv(CHEBYSHEV_ROWS, coefficient_rows)
    write_csv(VALIDATION, validations)

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
        decision = "INVALID_ORDER9_CHECKPOINT"
    elif acceptance_passed:
        decision = "ADOPT_ORDER9_DECAY_ANGLE_CUBATURE"
    else:
        decision = (
            "HOLD_OUTER_CUBATURE__DERIVE_PIECEWISE_DECAY_TOPOLOGY"
        )
    document = render_document(
        manifest,
        node_rows,
        cubature_values,
        profile_summary,
        transitions,
        validations,
        elapsed,
    )
    atomic_text(DOCUMENT, document)
    result = {
        "marker": MARKER,
        "revision": REVISION,
        "dry_run": dry_run,
        "manifest_hash": manifest["manifest_hash"],
        "decision": decision,
        "integrity_passed": integrity_passed,
        "acceptance_passed": acceptance_passed,
        "failed_gates": [
            row["gate"]
            for row in validations
            if not bool(row["passed"])
        ],
        "reused_node_count": manifest["reused_node_count"],
        "new_node_count": manifest["new_node_count"],
        "new_nested_job_count": manifest["new_nested_job_count"],
        "cubature_values": {
            str(order): complex_row(value)
            for order, value in cubature_values.items()
        },
        "order3_to_order5_relative_difference": (
            abs(cubature_values[3] - cubature_values[5])
            / max(abs(cubature_values[5]), 1.0)
        ),
        "order5_to_order9_relative_difference": (
            abs(cubature_values[5] - cubature_values[9])
            / max(abs(cubature_values[9]), 1.0)
        ),
        "profile": profile_summary,
        "topology_transition_interval_count": len(transitions),
        "formalization_workbench_digest": formal_digest,
        "elapsed_seconds": elapsed,
        "outputs": [
            str(path)
            for path in (
                MANIFEST,
                MANIFEST_ROWS,
                DRY_RUN,
                OUTER_TRACK_ROWS,
                NODE_ROWS,
                ZERO_ROWS,
                WINDING_ROWS,
                WINDING_CACHE,
                CLOSURE_ROWS,
                POLE_ROWS,
                RESIDUE_ROWS,
                RULE_ROWS,
                CUBATURE_ROWS,
                PROFILE_ROWS,
                TRANSITION_ROWS,
                CHEBYSHEV_ROWS,
                VALIDATION,
                DOCUMENT,
            )
        ],
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT, result)
    remove_project_pycache()
    if not integrity_passed:
        failed = [
            row["gate"]
            for row in validations
            if row["gate_kind"] == "integrity"
            and not bool(row["passed"])
        ]
        raise RuntimeError(f"5241 integrity validation failed: {failed}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate the cached order-9 extension manifest only",
    )
    arguments = parser.parse_args()
    if arguments.dry_run:
        print(
            json.dumps(
                write_manifest_and_dry_run(),
                indent=2,
                sort_keys=True,
            )
        )
        return
    print(json.dumps(execute(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
