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
SOURCE = FUNCTIONAL_RG / "5300"
NODE_RUNS = SOURCE / "nodes"

SCRIPT_5295 = (
    SCRIPTS / "Y5_R2FR_5295_order6_exact_component_singularity_atlas.py"
)
SCRIPT_5296 = (
    SCRIPTS / "Y5_R2FR_5296_order6_inner_energy_and_order4_comparison.py"
)
SCRIPT_5299 = (
    SCRIPTS / "Y5_R2FR_5299_stored_angular_orbit_ridge_diagnostic.py"
)
RESULT_5299 = (
    FUNCTIONAL_RG / "5299" / "stored_angular_orbit_diagnostic_result.json"
)
VALIDATION_5299 = (
    FUNCTIONAL_RG
    / "5299"
    / "stored_angular_orbit_diagnostic_validation.csv"
)
TARGETS_5299 = FUNCTIONAL_RG / "5299" / "adaptive_ridge_target_orbits.csv"
ORBITS_5299 = FUNCTIONAL_RG / "5299" / "angular_sign_orbit_samples.csv"

ATLAS_DRY_RUN = SOURCE / "adaptive_ridge_atlas_dry_run.json"
ADAPTIVE_NODES = SOURCE / "adaptive_ridge_signed_nodes.csv"
EXACT_JOBS = SOURCE / "adaptive_ridge_exact_component_jobs.csv"
SCAN_JOBS = SOURCE / "adaptive_ridge_exact_scan_jobs.csv"
GEOMETRIC_POLES = SOURCE / "adaptive_ridge_geometric_poles.csv"
EXPANDED_POLES = SOURCE / "adaptive_ridge_expanded_geometric_poles.csv"
CLASSIFIED_POLES = SOURCE / "adaptive_ridge_exact_mask_poles.csv"
CHANNEL_ROOTS = SOURCE / "adaptive_ridge_channel_roots.csv"
POLE_SAMPLES = SOURCE / "adaptive_ridge_pole_samples.csv"
POLE_FITS = SOURCE / "adaptive_ridge_pole_fits.csv"
POLE_RESIDUES = SOURCE / "adaptive_ridge_selected_pole_residues.csv"
AMBIGUOUS_BOUNDS = SOURCE / "adaptive_ridge_ambiguous_pole_bounds.csv"
ENDPOINT_SAMPLES = SOURCE / "adaptive_ridge_endpoint_samples.csv"
ENDPOINT_FITS = SOURCE / "adaptive_ridge_endpoint_fits.csv"
ENDPOINT_COEFFICIENTS = SOURCE / "adaptive_ridge_endpoint_coefficients.csv"
ENDPOINT_CANCELLATIONS = SOURCE / "adaptive_ridge_endpoint_cancellations.csv"
ATLAS_RESULT = SOURCE / "adaptive_ridge_atlas_result.json"

NODE_MANIFEST = SOURCE / "adaptive_ridge_node_run_manifest.csv"
COMPONENT_TOTALS = SOURCE / "adaptive_ridge_component_totals.csv"
INNER_TOTALS = SOURCE / "adaptive_ridge_inner_energy_totals.csv"
INNER_CONVERGENCE = SOURCE / "adaptive_ridge_inner_energy_convergence.csv"
ORBIT_VALUES = SOURCE / "adaptive_ridge_orbit_values.csv"
RESULT = SOURCE / "adaptive_ridge_width_probe_result.json"
VALIDATION = SOURCE / "adaptive_ridge_width_probe_validation.csv"
RESIDUAL_VALIDATION = (
    RESIDUALS / "P8_Y5_BRR545_5300_VALIDATION.csv"
)
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5300-Y5-R2FR-adaptive-interior-ridge-width-probe.md"

CHECKPOINT = 5300
PARENT_CHECKPOINT = 5299
MARKER = "MTS_5300_ADAPTIVE_INTERIOR_RIDGE_WIDTH_PROBE"
REVISION = "adaptive-interior-ridge-width-probe-v1"
ENERGY_ORDERS = (4, 8)
INNER_RELATIVE_CHANGE_LIMIT = 5.0e-3
EXPECTED_ADAPTIVE_NODE_COUNT = 8
EXPECTED_ADAPTIVE_ORBIT_COUNT = 2
REGULATOR_IDS = ("E040", "E020")
COMPONENT_IDS = (
    "MC02",
    "MC03",
    "MC04",
    "MC07",
    "MC08",
    "MC12",
    "MC14",
    "MC15",
)
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


M5295 = load_module("mts_5295_for_5300", SCRIPT_5295)
M5296 = load_module("mts_5296_for_5300", SCRIPT_5296)
M5292 = M5296.M5292
M5288 = M5295.M5288
M5287 = M5295.M5287
M5283 = M5295.M5283
M5280 = M5295.M5280
M5267 = M5295.M5267
mp = M5295.mp


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


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
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


def adaptive_nodes() -> list[dict[str, Any]]:
    targets = [
        row
        for row in read_csv(TARGETS_5299)
        if parse_bool(row["requires_new_exact_node_runs"])
    ]
    rows: list[dict[str, Any]] = []
    for target_index, target in enumerate(targets, start=1):
        absolute_soft = float(target["absolute_soft_cosine"])
        absolute_decay = float(target["absolute_decay_cosine"])
        for soft_sign_index, soft_sign in enumerate((-1.0, 1.0), start=1):
            for decay_sign_index, decay_sign in enumerate(
                (-1.0, 1.0),
                start=1,
            ):
                rows.append(
                    {
                        "angular_node_id": (
                            f"AR{target_index:02d}_"
                            f"S{soft_sign_index:02d}_"
                            f"D{decay_sign_index:02d}"
                        ),
                        "target_id": target["target_id"],
                        "absolute_soft_cosine": absolute_soft,
                        "absolute_decay_cosine": absolute_decay,
                        "soft_sign": int(soft_sign),
                        "decay_sign": int(decay_sign),
                        "soft_cosine": soft_sign * absolute_soft,
                        "decay_cosine": decay_sign * absolute_decay,
                        "angular_weight": 1.0,
                        "angular_jacobian": M5280.M5278.ANGULAR_JACOBIAN,
                        "diagnostic_measure_weight_only": True,
                        "valid_for_adaptive_ridge_node": True,
                        **{field: False for field in CLAIM_FIELDS},
                    }
                )
    return rows


def patch_atlas_library() -> None:
    assignments = {
        "SOURCE": SOURCE,
        "DRY_RUN": ATLAS_DRY_RUN,
        "ANGULAR_NODES": ADAPTIVE_NODES,
        "EXACT_JOBS": EXACT_JOBS,
        "SCAN_JOBS": SCAN_JOBS,
        "GEOMETRIC_POLES": GEOMETRIC_POLES,
        "EXPANDED_POLES": EXPANDED_POLES,
        "CLASSIFIED_POLES": CLASSIFIED_POLES,
        "CHANNEL_ROOTS": CHANNEL_ROOTS,
        "POLE_SAMPLES": POLE_SAMPLES,
        "POLE_FITS": POLE_FITS,
        "POLE_RESIDUES": POLE_RESIDUES,
        "AMBIGUOUS_POLE_BOUNDS": AMBIGUOUS_BOUNDS,
        "ENDPOINT_SAMPLES": ENDPOINT_SAMPLES,
        "ENDPOINT_FITS": ENDPOINT_FITS,
        "ENDPOINT_COEFFICIENTS": ENDPOINT_COEFFICIENTS,
        "ENDPOINT_CANCELLATIONS": ENDPOINT_CANCELLATIONS,
        "RESULT": ATLAS_RESULT,
        "STATUS": STATUS,
        "RESULT_5294": RESULT_5299,
        "VALIDATION_5294": VALIDATION_5299,
        "CHECKPOINT": CHECKPOINT,
        "PARENT_CHECKPOINT": PARENT_CHECKPOINT,
        "MARKER": MARKER,
        "REVISION": REVISION,
        "ANGULAR_ORDER": 8,
        "angular_nodes": adaptive_nodes,
    }
    for name, value in assignments.items():
        setattr(M5295, name, value)


def atlas_dry_run() -> dict[str, Any]:
    patch_atlas_library()
    M5295.configure_reused_atlas_library()
    SOURCE.mkdir(parents=True, exist_ok=True)
    parent = read_json(RESULT_5299)
    nodes = adaptive_nodes()
    checks = {
        "parent_5299_accepted": bool(parent["acceptance_passed"]),
        "parent_5299_validated": all(
            parse_bool(row["passed"])
            for row in read_csv(VALIDATION_5299)
        ),
        "expected_signed_adaptive_nodes_constructed": (
            len(nodes) == EXPECTED_ADAPTIVE_NODE_COUNT
        ),
        "expected_complete_sign_orbits_constructed": (
            len({row["target_id"] for row in nodes})
            == EXPECTED_ADAPTIVE_ORBIT_COUNT
            and all(
                sum(
                    row["target_id"] == target_id for row in nodes
                )
                == 4
                for target_id in {
                    row["target_id"] for row in nodes
                }
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
        "mode": "adaptive-atlas-dry-run",
        "checks": checks,
        "acceptance_passed": accepted,
        "angular_node_count": len(nodes),
        "planned_exact_scan_count": len(nodes) * 2 * 8,
        "decision": (
            "DRY_RUN_ACCEPTED__BUILD_ADAPTIVE_RIDGE_ATLAS"
            if accepted
            else "DRY_RUN_REQUIRES_REPAIR"
        ),
        "runtime_seconds": 0.0,
        **{field: False for field in CLAIM_FIELDS},
    }
    atomic_json(ATLAS_DRY_RUN, result)
    return result


def convert_atlas_flags() -> None:
    conversions = (
        (
            ADAPTIVE_NODES,
            "valid_for_order6_singularity_atlas",
            "valid_for_adaptive_ridge_atlas",
        ),
        (
            EXACT_JOBS,
            "valid_for_order6_exact_component_scan",
            "valid_for_adaptive_ridge_exact_component_scan",
        ),
        (
            POLE_RESIDUES,
            "valid_for_order6_pole_subtraction",
            "valid_for_adaptive_ridge_pole_subtraction",
        ),
        (
            AMBIGUOUS_BOUNDS,
            "valid_for_order6_pole_subtraction",
            "valid_for_adaptive_ridge_pole_subtraction",
        ),
        (
            ENDPOINT_COEFFICIENTS,
            "valid_for_order6_endpoint_subtraction",
            "valid_for_adaptive_ridge_endpoint_subtraction",
        ),
    )
    for path, source, target in conversions:
        rows = read_csv(path)
        for row in rows:
            row[target] = (
                parse_bool(row.get(target, False))
                or parse_bool(row.get(source, False))
            )
            row[source] = False
        write_csv(path, rows)


def build_or_reuse_atlas() -> dict[str, Any]:
    patch_atlas_library()
    M5295.dry_run = atlas_dry_run
    reusable = (
        ADAPTIVE_NODES,
        EXACT_JOBS,
        SCAN_JOBS,
        GEOMETRIC_POLES,
        EXPANDED_POLES,
        CLASSIFIED_POLES,
        CHANNEL_ROOTS,
        POLE_SAMPLES,
        POLE_FITS,
        POLE_RESIDUES,
        AMBIGUOUS_BOUNDS,
        ENDPOINT_SAMPLES,
        ENDPOINT_FITS,
        ENDPOINT_COEFFICIENTS,
        ENDPOINT_CANCELLATIONS,
        ATLAS_RESULT,
    )
    if (
        all(path.exists() for path in reusable)
        and len(read_csv(SCAN_JOBS))
        == EXPECTED_ADAPTIVE_NODE_COUNT
        * len(REGULATOR_IDS)
        * len(COMPONENT_IDS)
        and read_json(ATLAS_RESULT).get("mode")
        == "adaptive-ridge-atlas"
        and bool(read_json(ATLAS_RESULT).get("acceptance_passed"))
    ):
        return read_json(ATLAS_RESULT)
    M5295.execute()
    convert_atlas_flags()
    parent = read_json(RESULT_5299)
    nodes = read_csv(ADAPTIVE_NODES)
    scans = read_csv(SCAN_JOBS)
    geometric = read_csv(GEOMETRIC_POLES)
    expanded = read_csv(EXPANDED_POLES)
    classified = read_csv(CLASSIFIED_POLES)
    roots = read_csv(CHANNEL_ROOTS)
    residues = read_csv(POLE_RESIDUES)
    bounds = read_csv(AMBIGUOUS_BOUNDS)
    endpoints = read_csv(ENDPOINT_COEFFICIENTS)
    cancellations = read_csv(ENDPOINT_CANCELLATIONS)
    unresolved = [
        row
        for row in residues
        if not parse_bool(row["pole_residue_controls_pass"])
        and not (
            parse_bool(row["bounded_ambiguous_residue"])
            and parse_bool(
                row["valid_for_adaptive_ridge_pole_subtraction"]
            )
        )
    ]
    checks = {
        "expected_adaptive_nodes_written": (
            len(nodes) == EXPECTED_ADAPTIVE_NODE_COUNT
        ),
        "all_expected_exact_scans_complete": (
            len(scans)
            == EXPECTED_ADAPTIVE_NODE_COUNT
            * len(REGULATOR_IDS)
            * len(COMPONENT_IDS)
            and len({row["scan_key"] for row in scans})
            == EXPECTED_ADAPTIVE_NODE_COUNT
            * len(REGULATOR_IDS)
            * len(COMPONENT_IDS)
        ),
        "no_family_transport_used": (
            len(expanded) == len(geometric)
            and all(
                not parse_bool(row["family_scan_transport"])
                for row in expanded
            )
        ),
        "all_geometric_poles_classified": (
            len(classified) == len(expanded)
        ),
        "root_residue_bijection": len(roots) == len(residues),
        "all_roots_resolved": not unresolved,
        "all_ambiguous_bounds_valid": all(
            parse_bool(row["bound_valid"]) for row in bounds
        ),
        "endpoint_coefficients_complete": (
            len(endpoints)
            == EXPECTED_ADAPTIVE_NODE_COUNT
            * len(REGULATOR_IDS)
            * len(COMPONENT_IDS)
        ),
        "all_endpoint_cancellations_pass": (
            len(cancellations) == EXPECTED_ADAPTIVE_NODE_COUNT
            and all(
                parse_bool(row["endpoint_cancellation_passed"])
                for row in cancellations
            )
        ),
        "formalization_workbench_unchanged": (
            M5283.formal_inventory_digest()
            == str(parent["formalization_workbench_end_digest"])
        ),
        "claims_locked_false": True,
    }
    accepted = all(checks.values())
    formal_end = M5283.formal_inventory_digest()
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "mode": "adaptive-ridge-atlas",
        "checks": checks,
        "acceptance_passed": accepted,
        "angular_node_count": len(nodes),
        "exact_scan_count": len(scans),
        "geometric_pole_count": len(geometric),
        "exact_active_root_count": len(roots),
        "material_pole_count": sum(
            parse_bool(row["material_pole"]) for row in residues
        ),
        "bounded_ambiguous_pole_count": sum(
            parse_bool(row["bounded_ambiguous_residue"])
            for row in residues
        ),
        "endpoint_subtraction_count": sum(
            parse_bool(
                row["valid_for_adaptive_ridge_endpoint_subtraction"]
            )
            for row in endpoints
        ),
        "formalization_workbench_reference_digest": str(
            parent["formalization_workbench_end_digest"]
        ),
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0
            if formal_end == str(parent["formalization_workbench_end_digest"])
            else -1
        ),
        "decision": (
            "CERTIFY_ADAPTIVE_RIDGE_ATLAS__RUN_EXPECTED_NODES"
            if accepted
            else "ADAPTIVE_RIDGE_ATLAS_REQUIRES_REPAIR"
        ),
        "runtime_seconds": 0.0,
        "claim_boundary": {
            "valid_for_adaptive_ridge_atlas": accepted,
            "valid_for_adaptive_ridge_node_run": accepted,
            **{field: False for field in CLAIM_FIELDS},
        },
    }
    atomic_json(ATLAS_RESULT, result)
    if not accepted:
        raise RuntimeError(result["decision"])
    return result


def normalize_integration_flags(row: dict[str, Any]) -> dict[str, Any]:
    value = dict(row)
    for source in (
        "valid_for_order4_inner_energy_run",
        "valid_for_order6_inner_energy_run",
    ):
        if source in value:
            value["valid_for_adaptive_ridge_inner_energy_run"] = (
                parse_bool(
                    value.get(
                        "valid_for_adaptive_ridge_inner_energy_run",
                        False,
                    )
                )
                or parse_bool(value[source])
            )
            value[source] = False
    return value


def integration_write_csv(
    path: Path,
    rows: list[dict[str, Any]],
) -> None:
    write_csv(path, [normalize_integration_flags(row) for row in rows])


def patch_integrator() -> None:
    M5292.NODE_RUNS = NODE_RUNS
    M5292.RESULT_5291 = ATLAS_RESULT
    M5292.ANGULAR_NODES_5291 = ADAPTIVE_NODES
    M5292.POLE_RESIDUES_5291 = POLE_RESIDUES
    M5292.ENDPOINT_COEFFICIENTS_5291 = ENDPOINT_COEFFICIENTS
    M5292.ENDPOINT_CANCELLATIONS_5291 = ENDPOINT_CANCELLATIONS
    M5292.BOUNDS_5291 = AMBIGUOUS_BOUNDS
    M5292.STATUS = STATUS
    M5292.CHECKPOINT = CHECKPOINT
    M5292.REVISION = REVISION
    M5292.ANGULAR_ORDER = 0
    M5292.ENERGY_ORDERS = ENERGY_ORDERS
    M5292.INNER_RELATIVE_CHANGE_LIMIT = INNER_RELATIVE_CHANGE_LIMIT
    M5292.write_csv = integration_write_csv
    M5292.atomic_json = atomic_json


def pole_lookup() -> dict[
    tuple[str, str, str],
    list[dict[str, complex]],
]:
    grouped: dict[
        tuple[str, str, str],
        list[dict[str, complex]],
    ] = {}
    for row in read_csv(POLE_RESIDUES):
        if not parse_bool(
            row["valid_for_adaptive_ridge_pole_subtraction"]
        ):
            continue
        key = (
            row["angular_node_id"],
            row["epsilon_id"],
            row["component_id"],
        )
        grouped.setdefault(key, []).append(
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
        for row in read_csv(ENDPOINT_COEFFICIENTS)
        if parse_bool(
            row["valid_for_adaptive_ridge_endpoint_subtraction"]
        )
    }


def run_or_reuse_nodes() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    patch_integrator()
    nodes = read_csv(ADAPTIVE_NODES)
    poles = pole_lookup()
    endpoints = endpoint_lookup()
    base_context = M5280.source_context()
    for node_index, node in enumerate(nodes, start=1):
        if not M5292.node_cache_valid(node):
            M5292.integrate_node(node, base_context, poles, endpoints)
        atomic_json(
            STATUS,
            {
                "checkpoint": CHECKPOINT,
                "state": "RUNNING",
                "stage": "ADAPTIVE_RIDGE_NODE_SEQUENCE",
                "last_completed_angular_node_id": node[
                    "angular_node_id"
                ],
                "completed_angular_node_count": node_index,
                "total_angular_node_count": len(nodes),
            },
        )
    return M5292.aggregate_nodes(nodes)


def ridge_orbit_rows(
    totals: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    nodes = read_csv(ADAPTIVE_NODES)
    target_lookup = {
        row["angular_node_id"]: row["target_id"] for row in nodes
    }
    physical = [
        row
        for row in totals
        if row["row_type"] == "PHYSICAL_INNER_ENERGY"
        and int(row["energy_order"]) == max(ENERGY_ORDERS)
    ]
    rows: list[dict[str, Any]] = []
    for target_id in sorted(set(target_lookup.values())):
        local = [
            row
            for row in physical
            if target_lookup[row["angular_node_id"]] == target_id
        ]
        value = sum(
            complex(
                float(row["eight_component_integral_real"]),
                float(row["eight_component_integral_imaginary"]),
            )
            for row in local
        )
        node = next(
            row for row in nodes if row["target_id"] == target_id
        )
        rows.append(
            {
                "target_id": target_id,
                "source": "NEW_ADAPTIVE_EXACT_NODES",
                "absolute_soft_cosine": node["absolute_soft_cosine"],
                "absolute_decay_cosine": node["absolute_decay_cosine"],
                "signed_node_count": len(local),
                **complex_fields("sign_orbit_integrand", value),
                "valid_for_adaptive_ridge_width_probe": True,
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    anchor = next(
        row
        for row in read_csv(ORBITS_5299)
        if int(row["angular_order"]) == 4
        and abs(float(row["absolute_soft_cosine"]) - 0.338281138367)
        <= 1.0e-9
        and abs(float(row["absolute_decay_cosine"]) - 0.338281138367)
        <= 1.0e-9
    )
    rows.append(
        {
            "target_id": "RIDGE_ANCHOR_EXISTING_ORDER4",
            "source": "STORED_ACCEPTED_ORDER4_ORBIT",
            "absolute_soft_cosine": anchor["absolute_soft_cosine"],
            "absolute_decay_cosine": anchor["absolute_decay_cosine"],
            "signed_node_count": anchor["orbit_member_count"],
            "sign_orbit_integrand_real": anchor[
                "sign_orbit_integrand_real"
            ],
            "sign_orbit_integrand_imaginary": anchor[
                "sign_orbit_integrand_imaginary"
            ],
            "sign_orbit_integrand_magnitude": anchor[
                "sign_orbit_integrand_magnitude"
            ],
            "valid_for_adaptive_ridge_width_probe": True,
            **{field: False for field in CLAIM_FIELDS},
        }
    )
    return sorted(
        rows,
        key=lambda row: float(row["absolute_soft_cosine"]),
    )


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5295,
        SCRIPT_5296,
        SCRIPT_5299,
        RESULT_5299,
        VALIDATION_5299,
        TARGETS_5299,
        ORBITS_5299,
        ATLAS_RESULT,
        ADAPTIVE_NODES,
        POLE_RESIDUES,
        ENDPOINT_COEFFICIENTS,
        M5283.TOTALS_5281,
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def dry_run() -> dict[str, Any]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    NODE_RUNS.mkdir(parents=True, exist_ok=True)
    parent = read_json(RESULT_5299)
    checks = {
        "required_parent_sources_exist": all(
            path.exists()
            for path in (
                SCRIPT_5295,
                SCRIPT_5296,
                SCRIPT_5299,
                RESULT_5299,
                VALIDATION_5299,
                TARGETS_5299,
                ORBITS_5299,
            )
        ),
        "parent_5299_accepted": bool(parent["acceptance_passed"]),
        "parent_5299_validated": all(
            parse_bool(row["passed"])
            for row in read_csv(VALIDATION_5299)
        ),
        "adaptive_scope_is_eight_new_nodes": len(adaptive_nodes()) == 8,
        "formalization_workbench_unchanged": (
            M5283.formal_inventory_digest()
            == str(parent["formalization_workbench_end_digest"])
        ),
    }
    accepted = all(checks.values())
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "mode": "dry-run",
        "checks": checks,
        "acceptance_passed": accepted,
        "planned_exact_scan_count": 128,
        "planned_signed_node_count": 8,
        "decision": (
            "DRY_RUN_ACCEPTED__PROBE_ADAPTIVE_RIDGE_WIDTH"
            if accepted
            else "DRY_RUN_REQUIRES_REPAIR"
        ),
        "runtime_seconds": 0.0,
        **{field: False for field in CLAIM_FIELDS},
    }
    atomic_json(SOURCE / "adaptive_ridge_width_probe_dry_run.json", result)
    return result


def execute() -> dict[str, Any]:
    set_below_normal_priority()
    mp.mp.dps = M5280.MP_DECIMAL_DIGITS
    M5295.M5291.install_bounded_root_refinement_fallback()
    started = time.perf_counter()
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5300 dry run did not pass")
    parent = read_json(RESULT_5299)
    atlas = build_or_reuse_atlas()
    manifest, components, totals, convergence = run_or_reuse_nodes()
    orbit_values = ridge_orbit_rows(totals)
    write_csv(NODE_MANIFEST, manifest)
    write_csv(COMPONENT_TOTALS, components)
    write_csv(INNER_TOTALS, totals)
    write_csv(INNER_CONVERGENCE, convergence)
    write_csv(ORBIT_VALUES, orbit_values)
    maximum_node_change = max(
        float(row["relative_change"])
        for row in convergence
        if row["channel"] == "eight_component_integral"
    )
    orbit_lookup = {row["target_id"]: row for row in orbit_values}
    anchor_magnitude = float(
        orbit_lookup["RIDGE_ANCHOR_EXISTING_ORDER4"][
            "sign_orbit_integrand_magnitude"
        ]
    )
    lower_magnitude = float(
        orbit_lookup["RIDGE_LOWER_DIAGONAL_MIDPOINT"][
            "sign_orbit_integrand_magnitude"
        ]
    )
    upper_magnitude = float(
        orbit_lookup["RIDGE_UPPER_DIAGONAL_MIDPOINT"][
            "sign_orbit_integrand_magnitude"
        ]
    )
    lower_ratio = lower_magnitude / max(anchor_magnitude, 1.0e-300)
    upper_ratio = upper_magnitude / max(anchor_magnitude, 1.0e-300)
    narrow_ridge = max(lower_ratio, upper_ratio) < 0.75
    checks = {
        "adaptive_atlas_accepted": bool(atlas["acceptance_passed"]),
        "all_eight_node_runs_completed": (
            len(manifest) == 8
            and all(
                parse_bool(row["node_run_completed"]) for row in manifest
            )
        ),
        "all_node_shards_hash": all(
            digest(Path(row["energy_component_rows_path"]))
            == row["energy_component_rows_sha256"]
            for row in manifest
        ),
        "component_totals_complete": len(components) == 8 * 32,
        "inner_totals_complete": len(totals) == 8 * 6,
        "inner_convergence_complete": len(convergence) == 8 * 3,
        "all_nodes_pass_energy_gate": (
            maximum_node_change <= INNER_RELATIVE_CHANGE_LIMIT
        ),
        "three_ridge_orbits_available": len(orbit_values) == 3,
        "new_orbit_values_finite": all(
            math.isfinite(
                float(row["sign_orbit_integrand_magnitude"])
            )
            for row in orbit_values
        ),
        "formalization_workbench_unchanged": (
            M5283.formal_inventory_digest()
            == str(parent["formalization_workbench_end_digest"])
        ),
        "claims_locked_false": True,
    }
    accepted = all(checks.values())
    formal_end = M5283.formal_inventory_digest()
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "adaptive-interior-ridge-width-probe",
        "checks": checks,
        "acceptance_passed": accepted,
        "adaptive_signed_node_count": len(manifest),
        "component_evaluation_count": sum(
            int(row["component_evaluation_count"]) for row in manifest
        ),
        "maximum_node_inner_energy_relative_change": maximum_node_change,
        "ridge_anchor_magnitude": anchor_magnitude,
        "ridge_lower_midpoint_magnitude": lower_magnitude,
        "ridge_upper_midpoint_magnitude": upper_magnitude,
        "lower_to_anchor_magnitude_ratio": lower_ratio,
        "upper_to_anchor_magnitude_ratio": upper_ratio,
        "narrow_ridge_classification": narrow_ridge,
        "atlas_exact_scan_count": atlas["exact_scan_count"],
        "atlas_exact_active_root_count": atlas[
            "exact_active_root_count"
        ],
        "atlas_material_pole_count": atlas["material_pole_count"],
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
            "resumable_scan_ledger": str(SCAN_JOBS),
            "resumable_node_shards": str(NODE_RUNS),
        },
        "runtime_seconds": time.perf_counter() - started,
        "decision": (
            "INTERIOR_RIDGE_IS_NARROW__BUILD_LOCAL_ADAPTIVE_CELL"
            if accepted and narrow_ridge
            else "INTERIOR_RIDGE_IS_BROAD__BUILD_COMPOSITE_ANGULAR_MAP"
            if accepted
            else "ADAPTIVE_RIDGE_WIDTH_PROBE_REQUIRES_REPAIR"
        ),
        "claim_boundary": {
            "valid_for_adaptive_ridge_width_probe": accepted,
            "valid_for_local_adaptive_cell_design": (
                accepted and narrow_ridge
            ),
            "valid_for_full_angular_convergence": False,
            **{field: False for field in CLAIM_FIELDS},
            "reason": (
                "Three diagonal sign orbits classify the stored hotspot "
                "as narrow or broad. They do not yet integrate its "
                "two-dimensional angular area."
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
            "lower_to_anchor_ratio": lower_ratio,
            "upper_to_anchor_ratio": upper_ratio,
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
    text = f"""# 5300 — Adaptive interior-ridge width probe

## Result

Eight new signed angular nodes were derived and energy-integrated as
two complete sign orbits bracketing the stored order-four hotspot.

- exact scans: `{result['atlas_exact_scan_count']}`;
- active roots: `{result['atlas_exact_active_root_count']}`;
- material poles: `{result['atlas_material_pole_count']}`;
- component evaluations: `{result['component_evaluation_count']}`;
- largest nodewise energy-order change:
  `{result['maximum_node_inner_energy_relative_change']:.12g}`;
- anchor orbit magnitude: `{result['ridge_anchor_magnitude']:.12g}`;
- lower midpoint/anchor ratio:
  `{result['lower_to_anchor_magnitude_ratio']:.12g}`;
- upper midpoint/anchor ratio:
  `{result['upper_to_anchor_magnitude_ratio']:.12g}`.

Ridge classification:
**{'NARROW' if result['narrow_ridge_classification'] else 'BROAD'}**.

## Acceptance gates

{checks}

Validation: **{'PASS' if validation_passed else 'FAIL'}**.

## Claim boundary

This probe measures the diagonal width of the unresolved interior
feature. It does not yet integrate the feature over its
two-dimensional angular area and therefore does not establish full
angular, phase-space, UV, local-GR, or full-MTS convergence.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    required = (
        ATLAS_DRY_RUN,
        ADAPTIVE_NODES,
        SCAN_JOBS,
        CHANNEL_ROOTS,
        POLE_RESIDUES,
        ENDPOINT_COEFFICIENTS,
        ATLAS_RESULT,
        NODE_MANIFEST,
        COMPONENT_TOTALS,
        INNER_TOTALS,
        INNER_CONVERGENCE,
        ORBIT_VALUES,
        RESULT,
        STATUS,
    )
    result = read_json(RESULT)
    manifest = read_csv(NODE_MANIFEST)
    orbits = read_csv(ORBIT_VALUES)
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
            "V04_EIGHT_NODE_SHARDS_COMPLETE",
            len(manifest) == 8
            and all(
                parse_bool(row["node_run_completed"]) for row in manifest
            )
            and shard_hashes_match,
            f"nodes={len(manifest)} hashes={shard_hashes_match}",
        ),
        validation_gate(
            "V05_ENERGY_GATE",
            float(result["maximum_node_inner_energy_relative_change"])
            <= INNER_RELATIVE_CHANGE_LIMIT,
            str(result["maximum_node_inner_energy_relative_change"]),
        ),
        validation_gate(
            "V06_THREE_ORBITS_AVAILABLE",
            len(orbits) == 3,
            f"orbits={len(orbits)}",
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
            "VALIDATED_ADAPTIVE_INTERIOR_RIDGE_WIDTH_PROBE"
            if passed
            else "ADAPTIVE_RIDGE_WIDTH_PROBE_VALIDATION_FAILED"
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
