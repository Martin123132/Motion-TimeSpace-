from __future__ import annotations

import argparse
import csv
import ctypes
import hashlib
import importlib.util
import json
import math
import os
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any


for thread_variable in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "BLIS_NUM_THREADS",
):
    os.environ[thread_variable] = "1"
os.environ["PYTHONNOUSERSITE"] = "1"
sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
RESIDUALS = POST / "source-intake" / "mts_residuals"
SOURCE = FUNCTIONAL_RG / "5298"
NODE_RUNS = SOURCE / "nodes"

SCRIPT_5296 = (
    SCRIPTS / "Y5_R2FR_5296_order6_inner_energy_and_order4_comparison.py"
)
SCRIPT_5297 = (
    SCRIPTS / "Y5_R2FR_5297_order8_exact_component_singularity_atlas.py"
)
RESULT_5297 = (
    FUNCTIONAL_RG / "5297" / "order8_exact_component_atlas_result.json"
)
VALIDATION_5297 = (
    FUNCTIONAL_RG / "5297" / "order8_exact_component_atlas_validation.csv"
)
ANGULAR_NODES_5297 = FUNCTIONAL_RG / "5297" / "angular_order8_nodes.csv"
POLE_RESIDUES_5297 = (
    FUNCTIONAL_RG / "5297" / "angular_order8_selected_pole_residues.csv"
)
ENDPOINT_COEFFICIENTS_5297 = (
    FUNCTIONAL_RG / "5297" / "angular_order8_endpoint_coefficients.csv"
)
ENDPOINT_CANCELLATIONS_5297 = (
    FUNCTIONAL_RG / "5297" / "angular_order8_endpoint_cancellations.csv"
)
AMBIGUOUS_BOUNDS_5297 = (
    FUNCTIONAL_RG
    / "5297"
    / "angular_order8_bounded_ambiguous_pole_residues.csv"
)
CLUSTER_BOUNDS_5297 = (
    FUNCTIONAL_RG
    / "5297"
    / "angular_order8_cluster_deflated_removable_bounds.csv"
)
ORDER6_OUTER_5296 = FUNCTIONAL_RG / "5296" / "order6_outer_totals.csv"

DRY_RUN = SOURCE / "order8_inner_energy_dry_run.json"
NODE_MANIFEST = SOURCE / "order8_node_run_manifest.csv"
COMPONENT_TOTALS = SOURCE / "order8_inner_component_totals.csv"
INNER_TOTALS = SOURCE / "order8_inner_energy_totals.csv"
INNER_CONVERGENCE = SOURCE / "order8_inner_energy_convergence.csv"
OUTER_TOTALS = SOURCE / "order8_outer_totals.csv"
ANGULAR_COMPARISON = SOURCE / "order6_order8_angular_comparison.csv"
RESULT = SOURCE / "order8_inner_energy_result.json"
VALIDATION = SOURCE / "order8_inner_energy_validation.csv"
RESIDUAL_VALIDATION = (
    RESIDUALS / "P8_Y5_BRR545_5298_VALIDATION.csv"
)
STATUS = SOURCE / "status.json"
DOCUMENT = (
    POST / "5298-Y5-R2FR-order8-inner-energy-and-order6-comparison.md"
)

CHECKPOINT = 5298
PARENT_CHECKPOINT = 5297
MARKER = "MTS_5298_ORDER8_INNER_ENERGY_AND_ORDER6_COMPARISON"
REVISION = "order8-inner-energy-order6-comparison-v1"
ANGULAR_ORDER = 8
ENERGY_ORDERS = (4, 8)
INNER_RELATIVE_CHANGE_LIMIT = 5.0e-3
OUTER_ENERGY_RELATIVE_CHANGE_LIMIT = 5.0e-3
ANGULAR_RELATIVE_CHANGE_LIMIT = 5.0e-3
CLAIM_FIELDS = (
    "valid_for_full_phase_space_coefficient",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5296 = load_module("mts_5296_for_5298", SCRIPT_5296)
M5292 = M5296.M5292
M5288 = M5296.M5288
M5287 = M5296.M5287
M5283 = M5296.M5283
M5280 = M5296.M5280
M5267 = M5296.M5267
mp = M5296.mp


def set_below_normal_priority() -> None:
    if os.name != "nt":
        return
    process_handle = ctypes.windll.kernel32.GetCurrentProcess()
    ctypes.windll.kernel32.SetPriorityClass(process_handle, 0x00004000)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def normalize_order8_flags(row: dict[str, Any]) -> dict[str, Any]:
    value = dict(row)
    replacements = {
        "valid_for_order4_inner_energy_run": (
            "valid_for_order8_inner_energy_run"
        ),
        "valid_for_order6_inner_energy_run": (
            "valid_for_order8_inner_energy_run"
        ),
        "valid_for_order4_angular_smoke": (
            "valid_for_order8_angular_smoke"
        ),
        "valid_for_order6_angular_smoke": (
            "valid_for_order8_angular_smoke"
        ),
    }
    for source, target in replacements.items():
        if source in value:
            value[target] = (
                parse_bool(value.get(target, False))
                or parse_bool(value[source])
            )
            value[source] = False
    return value


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    normalized = [normalize_order8_flags(row) for row in rows]
    fields: list[str] = []
    for row in normalized:
        for field in row:
            if field not in fields:
                fields.append(field)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(normalized)
    temporary.replace(path)


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1024 * 1024):
            value.update(block)
    return value.hexdigest()


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return {
        f"{prefix}_real": float(value.real),
        f"{prefix}_imaginary": float(value.imag),
        f"{prefix}_magnitude": float(abs(value)),
    }


def relative_complex_difference(first: complex, second: complex) -> float:
    return abs(first - second) / max(abs(first), abs(second), 1.0e-300)


def pole_lookup() -> dict[
    tuple[str, str, str],
    list[dict[str, complex]],
]:
    grouped: dict[
        tuple[str, str, str],
        list[dict[str, complex]],
    ] = defaultdict(list)
    for row in read_csv(POLE_RESIDUES_5297):
        if not parse_bool(row["valid_for_order8_pole_subtraction"]):
            continue
        grouped[
            (
                row["angular_node_id"],
                row["epsilon_id"],
                row["component_id"],
            )
        ].append(
            {
                "pole": complex(
                    float(row["pole_real"]),
                    float(row["pole_imaginary"]),
                ),
                "residue": complex(
                    float(row["true_limit_residue_real"]),
                    float(row["true_limit_residue_imaginary"]),
                ),
                "bounded_ambiguous": complex(
                    1.0
                    if parse_bool(row["bounded_ambiguous_residue"])
                    else 0.0,
                    0.0,
                ),
            }
        )
    return grouped


def endpoint_lookup() -> dict[tuple[str, str, str], complex]:
    return {
        (
            row["angular_node_id"],
            row["epsilon_id"],
            row["component_id"],
        ): complex(
            float(row["endpoint_log_coefficient_real"]),
            float(row["endpoint_log_coefficient_imaginary"]),
        )
        for row in read_csv(ENDPOINT_COEFFICIENTS_5297)
        if parse_bool(row["valid_for_order8_endpoint_subtraction"])
    }


def angular_comparison_rows(
    outer8: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    order6_source = next(
        row
        for row in read_csv(ORDER6_OUTER_5296)
        if int(row["energy_order"]) == max(ENERGY_ORDERS)
    )
    order8_source = next(
        row
        for row in outer8
        if int(row["energy_order"]) == max(ENERGY_ORDERS)
    )
    rows: list[dict[str, Any]] = []
    for channel in (
        "eight_component_integral",
        "six_component_integral",
        "hidden_component_integral",
    ):
        lower = complex(
            float(order6_source[f"{channel}_real"]),
            float(order6_source[f"{channel}_imaginary"]),
        )
        upper = complex(
            float(order8_source[f"{channel}_real"]),
            float(order8_source[f"{channel}_imaginary"]),
        )
        change = relative_complex_difference(lower, upper)
        rows.append(
            {
                "channel": channel,
                "lower_angular_order": 6,
                "upper_angular_order": 8,
                "energy_order": max(ENERGY_ORDERS),
                **complex_fields("order6_value", lower),
                **complex_fields("order8_value", upper),
                "relative_change": change,
                "passes_order6_order8_smoke_gate": (
                    change <= ANGULAR_RELATIVE_CHANGE_LIMIT
                    if channel == "eight_component_integral"
                    else ""
                ),
                "valid_for_order6_order8_angular_comparison": True,
                "valid_for_full_angular_convergence": False,
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return rows


def patch_library_globals() -> None:
    assignments = {
        "SOURCE": SOURCE,
        "NODE_RUNS": NODE_RUNS,
        "SCRIPT_5295": SCRIPT_5297,
        "RESULT_5295": RESULT_5297,
        "VALIDATION_5295": VALIDATION_5297,
        "ANGULAR_NODES_5295": ANGULAR_NODES_5297,
        "POLE_RESIDUES_5295": POLE_RESIDUES_5297,
        "ENDPOINT_COEFFICIENTS_5295": ENDPOINT_COEFFICIENTS_5297,
        "ENDPOINT_CANCELLATIONS_5295": ENDPOINT_CANCELLATIONS_5297,
        "AMBIGUOUS_BOUNDS_5295": AMBIGUOUS_BOUNDS_5297,
        "ORDER4_OUTER_5294": ORDER6_OUTER_5296,
        "DRY_RUN": DRY_RUN,
        "NODE_MANIFEST": NODE_MANIFEST,
        "COMPONENT_TOTALS": COMPONENT_TOTALS,
        "INNER_TOTALS": INNER_TOTALS,
        "INNER_CONVERGENCE": INNER_CONVERGENCE,
        "OUTER_TOTALS": OUTER_TOTALS,
        "ANGULAR_COMPARISON": ANGULAR_COMPARISON,
        "RESULT": RESULT,
        "VALIDATION": VALIDATION,
        "RESIDUAL_VALIDATION": RESIDUAL_VALIDATION,
        "STATUS": STATUS,
        "DOCUMENT": DOCUMENT,
        "CHECKPOINT": CHECKPOINT,
        "PARENT_CHECKPOINT": PARENT_CHECKPOINT,
        "MARKER": MARKER,
        "REVISION": REVISION,
        "ANGULAR_ORDER": ANGULAR_ORDER,
        "ENERGY_ORDERS": ENERGY_ORDERS,
        "INNER_RELATIVE_CHANGE_LIMIT": INNER_RELATIVE_CHANGE_LIMIT,
        "OUTER_ENERGY_RELATIVE_CHANGE_LIMIT": (
            OUTER_ENERGY_RELATIVE_CHANGE_LIMIT
        ),
        "ANGULAR_RELATIVE_CHANGE_LIMIT": ANGULAR_RELATIVE_CHANGE_LIMIT,
        "write_csv": write_csv,
        "atomic_json": atomic_json,
        "pole_lookup": pole_lookup,
        "endpoint_lookup": endpoint_lookup,
        "angular_comparison_rows": angular_comparison_rows,
    }
    for name, value in assignments.items():
        setattr(M5296, name, value)


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5296,
        SCRIPT_5297,
        RESULT_5297,
        VALIDATION_5297,
        ANGULAR_NODES_5297,
        POLE_RESIDUES_5297,
        ENDPOINT_COEFFICIENTS_5297,
        ENDPOINT_CANCELLATIONS_5297,
        AMBIGUOUS_BOUNDS_5297,
        CLUSTER_BOUNDS_5297,
        ORDER6_OUTER_5296,
        M5283.TOTALS_5281,
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def dry_run() -> dict[str, Any]:
    patch_library_globals()
    M5296.configure_reused_integrator()
    SOURCE.mkdir(parents=True, exist_ok=True)
    NODE_RUNS.mkdir(parents=True, exist_ok=True)
    parent = read_json(RESULT_5297)
    nodes = read_csv(ANGULAR_NODES_5297)
    valid_poles = [
        row
        for row in read_csv(POLE_RESIDUES_5297)
        if parse_bool(row["valid_for_order8_pole_subtraction"])
    ]
    endpoints = [
        row
        for row in read_csv(ENDPOINT_COEFFICIENTS_5297)
        if parse_bool(row["valid_for_order8_endpoint_subtraction"])
    ]
    cancellations = read_csv(ENDPOINT_CANCELLATIONS_5297)
    checks = {
        "required_sources_exist": all(
            path.exists()
            for path in (
                SCRIPT_5296,
                SCRIPT_5297,
                RESULT_5297,
                VALIDATION_5297,
                ANGULAR_NODES_5297,
                POLE_RESIDUES_5297,
                ENDPOINT_COEFFICIENTS_5297,
                ENDPOINT_CANCELLATIONS_5297,
                AMBIGUOUS_BOUNDS_5297,
                CLUSTER_BOUNDS_5297,
                ORDER6_OUTER_5296,
            )
        ),
        "parent_5297_accepted": bool(parent["acceptance_passed"]),
        "parent_5297_validated": all(
            parse_bool(row["passed"])
            for row in read_csv(VALIDATION_5297)
        ),
        "sixty_four_order8_nodes_parse": len(nodes) == 64,
        "certified_pole_subtractions_present": bool(valid_poles),
        "certified_endpoint_subtractions_present": bool(endpoints),
        "all_endpoint_cancellations_pass": (
            len(cancellations) == 64
            and all(
                parse_bool(row["endpoint_cancellation_passed"])
                for row in cancellations
            )
        ),
        "formalization_workbench_unchanged": (
            M5283.formal_inventory_digest()
            == str(parent["formalization_workbench_end_digest"])
        ),
    }
    accepted = all(checks.values())
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "dry-run",
        "checks": checks,
        "acceptance_passed": accepted,
        "angular_node_count": len(nodes),
        "pole_subtraction_count": len(valid_poles),
        "endpoint_subtraction_count": len(endpoints),
        "planned_energy_orders": list(ENERGY_ORDERS),
        "decision": (
            "DRY_RUN_ACCEPTED__RUN_ORDER8_INNER_ENERGY"
            if accepted
            else "DRY_RUN_REQUIRES_REPAIR"
        ),
        "runtime_seconds": 0.0,
        **{field: False for field in CLAIM_FIELDS},
    }
    atomic_json(DRY_RUN, result)
    return result


def execute() -> dict[str, Any]:
    set_below_normal_priority()
    patch_library_globals()
    M5296.dry_run = dry_run
    started = time.perf_counter()
    M5296.execute()
    parent = read_json(RESULT_5297)
    nodes = read_csv(ANGULAR_NODES_5297)
    manifest = read_csv(NODE_MANIFEST)
    components = read_csv(COMPONENT_TOTALS)
    totals = read_csv(INNER_TOTALS)
    convergence = read_csv(INNER_CONVERGENCE)
    outer = read_csv(OUTER_TOTALS)
    comparison = read_csv(ANGULAR_COMPARISON)
    eight_node_changes = [
        float(row["relative_change"])
        for row in convergence
        if row["channel"] == "eight_component_integral"
    ]
    maximum_node_change = max(eight_node_changes)
    outer_lookup = {int(row["energy_order"]): row for row in outer}
    lower_outer = complex(
        float(
            outer_lookup[min(ENERGY_ORDERS)][
                "eight_component_integral_real"
            ]
        ),
        float(
            outer_lookup[min(ENERGY_ORDERS)][
                "eight_component_integral_imaginary"
            ]
        ),
    )
    upper_outer = complex(
        float(
            outer_lookup[max(ENERGY_ORDERS)][
                "eight_component_integral_real"
            ]
        ),
        float(
            outer_lookup[max(ENERGY_ORDERS)][
                "eight_component_integral_imaginary"
            ]
        ),
    )
    outer_energy_change = relative_complex_difference(
        lower_outer,
        upper_outer,
    )
    angular_change = float(
        next(
            row
            for row in comparison
            if row["channel"] == "eight_component_integral"
        )["relative_change"]
    )
    all_finite = all(
        math.isfinite(float(row[field]))
        for rows in (components, totals, convergence, outer, comparison)
        for row in rows
        for field in row
        if field.endswith("_real")
        or field.endswith("_imaginary")
        or field.endswith("_magnitude")
        or field == "relative_change"
    )
    checks = {
        "all_sixty_four_node_runs_completed": (
            len(manifest) == 64
            and all(
                parse_bool(row["node_run_completed"]) for row in manifest
            )
        ),
        "all_node_shards_hash": all(
            digest(Path(row["energy_component_rows_path"]))
            == row["energy_component_rows_sha256"]
            for row in manifest
        ),
        "component_totals_complete": len(components) == 64 * 32,
        "inner_totals_complete": len(totals) == 64 * 6,
        "inner_convergence_complete": len(convergence) == 64 * 3,
        "all_values_finite": all_finite,
        "all_nodes_pass_inner_energy_gate": (
            maximum_node_change <= INNER_RELATIVE_CHANGE_LIMIT
        ),
        "order8_outer_passes_energy_gate": (
            outer_energy_change <= OUTER_ENERGY_RELATIVE_CHANGE_LIMIT
        ),
        "formalization_workbench_unchanged": (
            M5283.formal_inventory_digest()
            == str(parent["formalization_workbench_end_digest"])
        ),
        "claims_locked_false": True,
    }
    accepted = all(checks.values())
    angular_smoke_passed = angular_change <= ANGULAR_RELATIVE_CHANGE_LIMIT
    formal_end = M5283.formal_inventory_digest()
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "order8-inner-energy-and-order6-comparison",
        "checks": checks,
        "acceptance_passed": accepted,
        "angular_node_count": len(nodes),
        "completed_node_count": len(manifest),
        "component_evaluation_count": sum(
            int(row["component_evaluation_count"]) for row in manifest
        ),
        "component_total_count": len(components),
        "inner_total_count": len(totals),
        "inner_convergence_count": len(convergence),
        "maximum_node_inner_energy_relative_change": maximum_node_change,
        "order8_outer_energy_relative_change": outer_energy_change,
        "order6_order8_angular_relative_change": angular_change,
        "inner_energy_relative_change_limit": (
            INNER_RELATIVE_CHANGE_LIMIT
        ),
        "angular_relative_change_limit": ANGULAR_RELATIVE_CHANGE_LIMIT,
        "order6_order8_angular_smoke_passed": angular_smoke_passed,
        "order8_energy8_eight_component_integral": {
            "real": upper_outer.real,
            "imaginary": upper_outer.imag,
        },
        "bounded_ambiguous_global_absolute_error_bound": parent[
            "bounded_ambiguous_global_absolute_error_bound"
        ],
        "bounded_ambiguous_global_relative_error_bound": parent[
            "bounded_ambiguous_global_relative_error_bound"
        ],
        "source_files": source_rows(),
        "formalization_workbench_reference_digest": str(
            parent["formalization_workbench_end_digest"]
        ),
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0
            if formal_end == str(parent["formalization_workbench_end_digest"])
            else -1
        ),
        "resource_contract": {
            "maximum_task_python_processes": 1,
            "worker_math_threads": 1,
            "windows_priority": "BelowNormal",
            "sustained_redline_forbidden": True,
            "resumable_node_shards": str(NODE_RUNS),
        },
        "runtime_seconds": time.perf_counter() - started,
        "decision": (
            "ORDER6_ORDER8_ANGULAR_CHANGE_PASSES_SMOKE__"
            "REQUIRE_ADAPTIVE_CROSSCHECK"
            if accepted and angular_smoke_passed
            else "ORDER8_VALID_BUT_ANGULAR_NOT_CONVERGED__"
            "DERIVE_ANGULAR_ENDPOINT_OR_ADAPTIVE_MAP"
            if accepted
            else "ORDER8_INNER_ENERGY_REQUIRES_LOCAL_REPAIR"
        ),
        "claim_boundary": {
            "valid_for_order8_inner_energy_run": accepted,
            "valid_for_order6_order8_angular_smoke": accepted,
            "valid_for_full_angular_convergence": False,
            **{field: False for field in CLAIM_FIELDS},
            "reason": (
                "The order-six/order-eight comparison is a finite-order "
                "convergence gate. An independent adaptive or "
                "endpoint-subtracted angular cross-check is still "
                "required."
            ),
        },
    }
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "COMPLETE" if accepted else "FAILED",
            "decision": result["decision"],
            "maximum_node_inner_energy_relative_change": maximum_node_change,
            "order8_outer_energy_relative_change": outer_energy_change,
            "order6_order8_angular_relative_change": angular_change,
        },
    )
    return result


def validation_gate(
    gate_id: str,
    passed: bool,
    detail: str,
) -> dict[str, Any]:
    return {"gate_id": gate_id, "passed": passed, "detail": detail}


def render_document(
    result: dict[str, Any],
    validation_passed: bool,
) -> None:
    checks = "\n".join(
        f"- `{key}`: **{'PASS' if value else 'FAIL'}**"
        for key, value in sorted(result["checks"].items())
    )
    value = result["order8_energy8_eight_component_integral"]
    text = f"""# 5298 — Order-eight inner energy and order-six comparison

## Result

All `{result['angular_node_count']}` order-eight nodes were evaluated
with the exact-component singular atlas.

- component evaluations:
  `{result['component_evaluation_count']}`;
- largest nodewise energy-order change:
  `{result['maximum_node_inner_energy_relative_change']:.12g}`;
- outer energy-order change:
  `{result['order8_outer_energy_relative_change']:.12g}`;
- order-six/order-eight angular change:
  `{result['order6_order8_angular_relative_change']:.12g}`;
- order-eight energy-eight total:
  `{value['real']:.16g} + {value['imaginary']:.16g} i`;
- bounded singular-atlas relative uncertainty:
  `{result['bounded_ambiguous_global_relative_error_bound']:.12g}`.

## Acceptance gates

{checks}

Validation: **{'PASS' if validation_passed else 'FAIL'}**.

## Claim boundary

This is a numerical angular-convergence rung inside the current
functional-RG construction. It is not a UV, local-GR, or full-MTS
claim. A stable result still requires an adaptive or explicitly
angular-endpoint-subtracted cross-check.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    required = (
        DRY_RUN,
        NODE_MANIFEST,
        COMPONENT_TOTALS,
        INNER_TOTALS,
        INNER_CONVERGENCE,
        OUTER_TOTALS,
        ANGULAR_COMPARISON,
        RESULT,
        STATUS,
    )
    result = read_json(RESULT)
    manifest = read_csv(NODE_MANIFEST)
    components = read_csv(COMPONENT_TOTALS)
    totals = read_csv(INNER_TOTALS)
    convergence = read_csv(INNER_CONVERGENCE)
    outer = read_csv(OUTER_TOTALS)
    comparison = read_csv(ANGULAR_COMPARISON)
    source_hashes_match = all(
        Path(row["path"]).exists()
        and digest(Path(row["path"])) == row["sha256"]
        for row in result["source_files"]
    )
    shard_hashes_match = all(
        Path(row["energy_component_rows_path"]).exists()
        and digest(Path(row["energy_component_rows_path"]))
        == row["energy_component_rows_sha256"]
        for row in manifest
    )
    formal_end = M5283.formal_inventory_digest()
    gates = [
        validation_gate(
            "V01_REQUIRED_OUTPUTS_EXIST",
            all(path.exists() for path in required),
            f"{len(required)} required outputs",
        ),
        validation_gate(
            "V02_RESULT_ACCEPTED",
            bool(result["acceptance_passed"]),
            result["decision"],
        ),
        validation_gate(
            "V03_SOURCE_HASHES_MATCH",
            source_hashes_match,
            f"{len(result['source_files'])} source hashes",
        ),
        validation_gate(
            "V04_ALL_NODE_SHARDS_COMPLETE",
            len(manifest) == 64
            and all(
                parse_bool(row["node_run_completed"]) for row in manifest
            )
            and shard_hashes_match,
            f"nodes={len(manifest)} hashes={shard_hashes_match}",
        ),
        validation_gate(
            "V05_AGGREGATE_COUNTS",
            len(components) == 2048
            and len(totals) == 384
            and len(convergence) == 192
            and len(outer) == 2
            and len(comparison) == 3,
            (
                f"components={len(components)} totals={len(totals)} "
                f"convergence={len(convergence)}"
            ),
        ),
        validation_gate(
            "V06_ENERGY_GATES_PASS",
            float(result["maximum_node_inner_energy_relative_change"])
            <= INNER_RELATIVE_CHANGE_LIMIT
            and float(result["order8_outer_energy_relative_change"])
            <= OUTER_ENERGY_RELATIVE_CHANGE_LIMIT,
            (
                f"node={result['maximum_node_inner_energy_relative_change']} "
                f"outer={result['order8_outer_energy_relative_change']}"
            ),
        ),
        validation_gate(
            "V07_FORMAL_WORKBENCH_UNCHANGED",
            formal_end
            == str(result["formalization_workbench_reference_digest"]),
            formal_end,
        ),
        validation_gate(
            "V08_CLAIMS_LOCKED_FALSE",
            all(
                not bool(result["claim_boundary"][field])
                for field in CLAIM_FIELDS
            ),
            "phase-space, UV, local-GR, and full-MTS claims false",
        ),
    ]
    passed = all(row["passed"] for row in gates)
    write_csv(VALIDATION, gates)
    write_csv(RESIDUAL_VALIDATION, gates)
    render_document(result, passed)
    return {
        "checkpoint": CHECKPOINT,
        "mode": "validation",
        "acceptance_passed": passed,
        "decision": (
            "VALIDATED_ORDER8_INNER_ENERGY_AND_ORDER6_COMPARISON"
            if passed
            else "ORDER8_INNER_ENERGY_VALIDATION_FAILED"
        ),
        "runtime_seconds": time.perf_counter() - started,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("dry-run", "run", "validate"),
        required=True,
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.mode == "dry-run":
        result = dry_run()
    elif args.mode == "run":
        result = execute()
    else:
        result = validate_outputs()
    print(
        json.dumps(
            {
                "checkpoint": result["checkpoint"],
                "mode": result["mode"],
                "acceptance_passed": result["acceptance_passed"],
                "decision": result["decision"],
                "runtime_seconds": result["runtime_seconds"],
            },
            sort_keys=True,
        )
    )
    return 0 if result["acceptance_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
