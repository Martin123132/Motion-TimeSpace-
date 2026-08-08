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
SOURCE = FUNCTIONAL_RG / "5282"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5280 = (
    SCRIPTS
    / "Y5_R2FR_5280_algebraic_selector_energy_pole_subtracted_smoke.py"
)
RESULT_5280 = (
    FUNCTIONAL_RG
    / "5280"
    / "energy_pole_subtracted_smoke_result.json"
)
VALIDATION_5280 = (
    FUNCTIONAL_RG / "5280" / "energy_pole_subtracted_smoke_validation.csv"
)
RESULT_5281 = (
    FUNCTIONAL_RG
    / "5281"
    / "high_order_energy_convergence_result.json"
)
VALIDATION_5281 = (
    FUNCTIONAL_RG
    / "5281"
    / "high_order_energy_convergence_validation.csv"
)
POLE_ROWS_5267 = {
    epsilon_id: (
        FUNCTIONAL_RG
        / "5267"
        / "workers"
        / epsilon_id
        / "energy_poles.csv"
    )
    for epsilon_id in ("E040", "E020")
}

DRY_RUN = SOURCE / "exact_mask_pole_reclassification_dry_run.json"
RECLASSIFICATION_ROWS = (
    SOURCE / "exact_mask_energy_pole_reclassification.csv"
)
FIT_ROWS = SOURCE / "true_limit_exact_active_pole_fits.csv"
RESULT = SOURCE / "exact_mask_energy_pole_result.json"
VALIDATION = SOURCE / "exact_mask_energy_pole_validation.csv"
RESIDUAL_VALIDATION = (
    RESIDUALS / "P8_Y5_BRR545_5282_VALIDATION.csv"
)
STATUS = SOURCE / "status.json"
DOCUMENT = (
    POST
    / "5282-Y5-R2FR-exact-mask-energy-pole-reclassification.md"
)

CHECKPOINT = 5282
PARENT_CHECKPOINT = 5281
MARKER = "MTS_5282_EXACT_MASK_ENERGY_POLE_RECLASSIFICATION"
REVISION = "exact-mask-energy-pole-reclassification-v1"
REGULATOR_IDS = ("E040", "E020")
EXACT_ACTIVE_COMPONENT_IDS = ("MC03", "MC04", "MC07", "MC12")
EXPECTED_MATERIAL_POLE_IDS = ("MC04", "MC12")
EXPECTED_REMOVABLE_POLE_IDS = ("MC03", "MC07")
POLE_BACKGROUND_DEGREE = 3
MAXIMUM_FIT_RADIUS = 3.2e-3
FIT_RADIUS_NEIGHBOR_FRACTION = 0.18
FIT_FRACTIONS = (
    -1.0,
    -0.5,
    -0.25,
    -0.125,
    0.125,
    0.25,
    0.5,
    1.0,
)
FIT_RELATIVE_RESIDUAL_LIMIT = 5.0e-5
MATERIAL_RESIDUE_FLOOR = 1.0e-8
COEFFICIENT_CONVERGENCE_LIMIT = 1.0e-6
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


M5280 = load_module("mts_5280_for_5282", SCRIPT_5280)
M5279 = M5280.M5279
M5277 = M5280.M5277
M5274 = M5280.M5274
np = M5280.np
mp = M5280.mp


def set_below_normal_priority() -> None:
    if os.name != "nt":
        return
    handle = ctypes.windll.kernel32.GetCurrentProcess()
    ctypes.windll.kernel32.SetPriorityClass(handle, 0x00004000)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


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


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5280,
        RESULT_5280,
        VALIDATION_5280,
        RESULT_5281,
        VALIDATION_5281,
        POLE_ROWS_5267["E040"],
        POLE_ROWS_5267["E020"],
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def formal_inventory_digest() -> str:
    return str(M5280.formal_inventory_digest())


def exact_mask_reclassification_rows(
    context: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for epsilon_id in REGULATOR_IDS:
        target = context["inventories"][epsilon_id]["target"]
        components = context["inventories"][epsilon_id][
            "components"
        ]
        for source in read_csv(POLE_ROWS_5267[epsilon_id]):
            component_id = source["component_id"]
            center = float(source["real_axis_center"])
            event = dict(context["source_event"])
            event["soft_energy"] = center
            component = components[component_id]
            selection = M5279.algebraic_component_selector(
                event,
                target,
                component,
            )
            (
                exact_active,
                orientation,
                owned_labels,
                surface_values,
            ) = M5277.exact_mask_orientation(
                selection["selected_labels"],
                event,
                context["surfaces"],
            )
            old_active = (
                source["causal_family_active"].lower() == "true"
            )
            rows.append(
                {
                    "epsilon_id": epsilon_id,
                    "component_id": component_id,
                    "pole_id": source["pole_id"],
                    "real_axis_center": center,
                    "pole_real": source["pole_real"],
                    "pole_imaginary": source["pole_imaginary"],
                    "old_causal_family_active": old_active,
                    "exact_mask_active": exact_active,
                    "promoted_by_exact_mask": (
                        exact_active and not old_active
                    ),
                    "selected_role": selection["selected_role"],
                    "representing_pair": "|".join(
                        selection["selected_labels"]
                    ),
                    "orientation": orientation,
                    "first_label_owned": owned_labels[0],
                    "second_label_owned": owned_labels[1],
                    "first_surface_value": surface_values[0],
                    "second_surface_value": surface_values[1],
                    "reciprocal_residual": selection[
                        "reciprocal_residual"
                    ],
                    "source_path": str(POLE_ROWS_5267[epsilon_id]),
                    "valid_for_exact_mask_pole_classification": True,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    return rows


def fit_radius(
    center: float,
    active_centers: list[float],
) -> float:
    energy_minimum = float(M5274.M5267.ENERGY_MINIMUM)
    energy_maximum = float(M5274.M5267.ENERGY_MAXIMUM)
    separation = min(
        [
            abs(center - candidate)
            for candidate in active_centers
            if candidate != center
        ]
        + [
            center - energy_minimum,
            energy_maximum - center,
        ]
    )
    return min(
        MAXIMUM_FIT_RADIUS,
        FIT_RADIUS_NEIGHBOR_FRACTION * separation,
    )


def fit_active_poles(
    context: dict[str, Any],
    reclassification: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    cache: dict[tuple[str, float, str], dict[str, Any]] = {}
    for epsilon_id in REGULATOR_IDS:
        active = [
            row
            for row in reclassification
            if row["epsilon_id"] == epsilon_id
            and bool(row["exact_mask_active"])
        ]
        active_centers = [
            float(row["real_axis_center"]) for row in active
        ]
        for candidate in active:
            component_id = candidate["component_id"]
            center = float(candidate["real_axis_center"])
            pole = complex(
                float(candidate["pole_real"]),
                float(candidate["pole_imaginary"]),
            )
            radius = fit_radius(center, active_centers)
            values: list[complex] = []
            design: list[list[complex]] = []
            coefficient_changes: list[float] = []
            all_samples_active = True
            for fraction in FIT_FRACTIONS:
                energy = center + radius * fraction
                event = dict(context["source_event"])
                event["soft_energy"] = energy
                key = (epsilon_id, energy, component_id)
                if key not in cache:
                    cache[key] = M5280.evaluate_component(
                        event,
                        epsilon_id,
                        component_id,
                        context,
                        convergence_audit=True,
                    )
                evaluation = cache[key]
                all_samples_active = (
                    all_samples_active
                    and bool(evaluation["mask_active"])
                )
                values.append(complex(evaluation["residue"]))
                coefficient_changes.append(
                    float(
                        evaluation["coefficient_relative_change"]
                    )
                )
                delta = energy - center
                design.append(
                    [
                        1.0 / (energy - pole),
                        *[
                            complex(delta**power)
                            for power in range(
                                POLE_BACKGROUND_DEGREE + 1
                            )
                        ],
                    ]
                )
            matrix = np.asarray(design, dtype=np.complex128)
            vector = np.asarray(values, dtype=np.complex128)
            coefficients, _, _, _ = np.linalg.lstsq(
                matrix,
                vector,
                rcond=None,
            )
            predicted = matrix @ coefficients
            residual = float(
                np.linalg.norm(predicted - vector)
                / max(np.linalg.norm(vector), 1.0)
            )
            residue = complex(coefficients[0])
            material = abs(residue) > MATERIAL_RESIDUE_FLOOR
            fit_passed = (
                residual <= FIT_RELATIVE_RESIDUAL_LIMIT
                and all_samples_active
                and max(coefficient_changes)
                <= COEFFICIENT_CONVERGENCE_LIMIT
            )
            rows.append(
                {
                    "epsilon_id": epsilon_id,
                    "component_id": component_id,
                    "pole_id": candidate["pole_id"],
                    "center": center,
                    "pole_real": pole.real,
                    "pole_imaginary": pole.imag,
                    "fit_radius": radius,
                    "fit_sample_count": len(FIT_FRACTIONS),
                    "true_limit_residue_real": residue.real,
                    "true_limit_residue_imaginary": residue.imag,
                    "true_limit_residue_magnitude": abs(residue),
                    "fit_relative_residual": residual,
                    "maximum_coefficient_relative_change": max(
                        coefficient_changes
                    ),
                    "all_fit_samples_exact_mask_active": (
                        all_samples_active
                    ),
                    "material_pole": material,
                    "pole_classification": (
                        "EXACT_ACTIVE_MATERIAL_SIMPLE_POLE"
                        if material
                        else "EXACT_ACTIVE_REMOVABLE_ZERO_RESIDUE"
                    ),
                    "fit_passed": fit_passed,
                    "valid_for_true_limit_pole_subtraction": (
                        fit_passed and material
                    ),
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    return rows


def dry_run() -> dict[str, Any]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    required = (
        SCRIPT_5280,
        RESULT_5280,
        VALIDATION_5280,
        RESULT_5281,
        VALIDATION_5281,
        POLE_ROWS_5267["E040"],
        POLE_ROWS_5267["E020"],
    )
    parent = read_json(RESULT_5280)
    diagnosis = read_json(RESULT_5281)
    parent_validation = read_csv(VALIDATION_5280)
    diagnosis_validation = read_csv(VALIDATION_5281)
    checks = {
        "required_sources_exist": all(
            path.exists() for path in required
        ),
        "parent_5280_accepted": bool(parent["acceptance_passed"]),
        "parent_5280_validated": all(
            row["passed"].lower() == "true"
            for row in parent_validation
        ),
        "parent_5281_accepted": bool(diagnosis["acceptance_passed"]),
        "parent_5281_validated": all(
            row["passed"].lower() == "true"
            for row in diagnosis_validation
        ),
        "pointwise_evaluator_authorized": bool(
            parent["claim_boundary"][
                "valid_for_algebraic_pointwise_evaluator"
            ]
        ),
        "both_geometric_pole_ledgers_parse": all(
            bool(read_csv(POLE_ROWS_5267[epsilon_id]))
            for epsilon_id in REGULATOR_IDS
        ),
        "formalization_workbench_unchanged": (
            formal_inventory_digest()
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
        "decision": (
            "DRY_RUN_ACCEPTED__RECLASSIFY_ALL_GEOMETRIC_POLES"
            if accepted
            else "DRY_RUN_REQUIRES_REPAIR"
        ),
        "runtime_seconds": 0.0,
        "valid_for_full_phase_space_coefficient": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(DRY_RUN, result)
    return result


def execute() -> dict[str, Any]:
    started = time.perf_counter()
    set_below_normal_priority()
    mp.mp.dps = M5280.MP_DECIMAL_DIGITS
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5282 dry run did not pass")
    parent = read_json(RESULT_5280)
    context = M5280.source_context()
    reclassification = exact_mask_reclassification_rows(context)
    fits = fit_active_poles(context, reclassification)
    active = [
        row
        for row in reclassification
        if bool(row["exact_mask_active"])
    ]
    promoted = [
        row
        for row in reclassification
        if bool(row["promoted_by_exact_mask"])
    ]
    material = [
        row for row in fits if bool(row["material_pole"])
    ]
    removable = [
        row for row in fits if not bool(row["material_pole"])
    ]
    material_ids = {
        row["component_id"] for row in material
    }
    removable_ids = {
        row["component_id"] for row in removable
    }
    maximum_fit_residual = max(
        float(row["fit_relative_residual"]) for row in fits
    )
    maximum_coefficient_change = max(
        float(row["maximum_coefficient_relative_change"])
        for row in fits
    )
    checks = {
        "parent_5280_accepted": bool(parent["acceptance_passed"]),
        "four_exact_active_candidates_per_regulator": (
            len(active)
            == len(REGULATOR_IDS)
            * len(EXACT_ACTIVE_COMPONENT_IDS)
        ),
        "exact_active_component_set_reproduces": (
            {
                row["component_id"] for row in active
            }
            == set(EXACT_ACTIVE_COMPONENT_IDS)
        ),
        "all_active_candidates_fit": (
            len(fits) == len(active)
            and all(bool(row["fit_passed"]) for row in fits)
        ),
        "material_poles_are_MC04_and_MC12": (
            material_ids == set(EXPECTED_MATERIAL_POLE_IDS)
            and len(material)
            == len(REGULATOR_IDS)
            * len(EXPECTED_MATERIAL_POLE_IDS)
        ),
        "MC03_MC07_are_removable_zero_residues": (
            removable_ids == set(EXPECTED_REMOVABLE_POLE_IDS)
            and len(removable)
            == len(REGULATOR_IDS)
            * len(EXPECTED_REMOVABLE_POLE_IDS)
        ),
        "MC12_promoted_from_old_inactive_status": (
            any(
                row["component_id"] == "MC12"
                for row in promoted
            )
        ),
        "fit_and_coefficient_controls_pass": (
            maximum_fit_residual <= FIT_RELATIVE_RESIDUAL_LIMIT
            and maximum_coefficient_change
            <= COEFFICIENT_CONVERGENCE_LIMIT
        ),
        "formalization_workbench_unchanged": (
            formal_inventory_digest()
            == str(parent["formalization_workbench_end_digest"])
        ),
        "claims_locked_false": True,
    }
    accepted = all(checks.values())
    formal_end = formal_inventory_digest()
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "exact-mask-energy-pole-reclassification",
        "checks": checks,
        "acceptance_passed": accepted,
        "geometric_candidate_count": len(reclassification),
        "exact_active_candidate_count": len(active),
        "promoted_candidate_count": len(promoted),
        "true_limit_fit_count": len(fits),
        "material_pole_count": len(material),
        "removable_zero_residue_count": len(removable),
        "material_component_ids": sorted(material_ids),
        "removable_component_ids": sorted(removable_ids),
        "maximum_fit_relative_residual": maximum_fit_residual,
        "maximum_coefficient_relative_change": (
            maximum_coefficient_change
        ),
        "source_files": source_rows(),
        "formalization_workbench_reference_digest": str(
            parent["formalization_workbench_end_digest"]
        ),
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0
            if formal_end
            == str(parent["formalization_workbench_end_digest"])
            else -1
        ),
        "resource_contract": {
            "maximum_task_python_processes": 1,
            "worker_math_threads": 1,
            "windows_priority": "BelowNormal",
            "sustained_redline_forbidden": True,
        },
        "runtime_seconds": time.perf_counter() - started,
        "decision": (
            "ADOPT_EXACT_ACTIVE_MATERIAL_POLE_SET_MC04_MC12__"
            "RECOMPUTE_EXISTING_HIGH_ORDER_NODES_WITH_TWO_POLE_SUBTRACTION"
            if accepted
            else "EXACT_MASK_POLE_RECLASSIFICATION_REQUIRES_REPAIR"
        ),
        "claim_boundary": {
            "valid_for_exact_mask_active_pole_classification": (
                accepted
            ),
            "valid_for_true_limit_MC04_MC12_subtraction": accepted,
            "valid_for_converged_fixed_angle_energy_integral": False,
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "The exact mask promotes four old-inactive geometric "
                "candidates. MC03 and MC07 have vanishing true residues "
                "and are removable; MC12 has a material residue and "
                "must be subtracted alongside MC04. Existing high-order "
                "nodes can be reassembled without reevaluation."
            ),
        },
    }
    write_csv(RECLASSIFICATION_ROWS, reclassification)
    write_csv(FIT_ROWS, fits)
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "COMPLETED",
            "mode": result["mode"],
            "acceptance_passed": accepted,
            "decision": result["decision"],
            "runtime_seconds": result["runtime_seconds"],
        },
    )
    return result


def validation_gate(
    gate_id: str,
    passed: bool,
    detail: str,
) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "passed": passed,
        "detail": detail,
    }


def render_document(
    result: dict[str, Any],
    validation_passed: bool,
) -> None:
    checks = "\n".join(
        f"- `{name}`: **{'PASS' if passed else 'FAIL'}**"
        for name, passed in result["checks"].items()
    )
    text = f"""# 5282 — Exact-mask energy-pole reclassification

## Purpose

The 5281 order sequence did not converge and localized the dominant
regular-remainder mass near the old MC12 geometric pole. This checkpoint
reclassifies every sourced 5267 pole with the exact Boolean masks and
fits its true local-limit residue.

## Result

- geometric candidates: `{result['geometric_candidate_count']}`;
- exact-active candidates: `{result['exact_active_candidate_count']}`;
- promoted from old inactive status:
  `{result['promoted_candidate_count']}`;
- material pole owners: `{result['material_component_ids']}`;
- removable zero-residue owners:
  `{result['removable_component_ids']}`;
- maximum fit residual:
  `{result['maximum_fit_relative_residual']:.12g}`.

The exact mask activates MC03, MC04, MC07, and MC12 at their relevant
centres. True-limit fitting then separates geometry from materiality:
MC03 and MC07 have residues below the material floor, while MC04 and
MC12 carry nonzero simple-pole residues. MC12 was therefore omitted by
the old causal classification and must be restored.

## Acceptance gates

{checks}

Validation: **{'PASS' if validation_passed else 'FAIL'}**.

## Claim boundary

This closes the fixed-angle active-pole inventory, not the energy
integral. The already computed 4/8/16 nodes must now be reassembled with
both MC04 and MC12 subtracted before convergence can be judged.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    result = read_json(RESULT)
    parent = read_json(RESULT_5280)
    required_csvs = (RECLASSIFICATION_ROWS, FIT_ROWS)
    csv_rows = {
        str(path): read_csv(path)
        for path in required_csvs
        if path.exists()
    }
    source_files = result["source_files"]
    current_formal_digest = formal_inventory_digest()
    reference_formal_digest = str(
        result["formalization_workbench_reference_digest"]
    )
    serialized = json.dumps(
        {"result": result, "csvs": csv_rows},
        sort_keys=True,
    )
    claim_rows = [
        row
        for rows in csv_rows.values()
        for row in rows
        if any(field in row for field in CLAIM_FIELDS)
    ]
    rows = [
        validation_gate(
            "SOURCE_PATHS_EXIST",
            all(Path(row["path"]).exists() for row in source_files),
            f"{len(source_files)} source paths",
        ),
        validation_gate(
            "SOURCE_HASHES_MATCH",
            all(
                digest(Path(row["path"])) == row["sha256"]
                for row in source_files
            ),
            "all recorded source hashes reproduce",
        ),
        validation_gate(
            "PARENT_5280_ACCEPTED",
            bool(parent["acceptance_passed"]),
            str(parent["decision"]),
        ),
        validation_gate(
            "POLE_RECLASSIFICATION_ACCEPTED",
            bool(result["acceptance_passed"]),
            str(result["decision"]),
        ),
        validation_gate(
            "REQUIRED_CSVS_PARSE",
            (
                len(csv_rows) == len(required_csvs)
                and all(csv_rows.values())
            ),
            f"{len(csv_rows)}/{len(required_csvs)} non-empty CSVs",
        ),
        validation_gate(
            "MATERIAL_SET_EXACT",
            result["material_component_ids"]
            == list(EXPECTED_MATERIAL_POLE_IDS),
            str(result["material_component_ids"]),
        ),
        validation_gate(
            "REMOVABLE_SET_EXACT",
            result["removable_component_ids"]
            == list(EXPECTED_REMOVABLE_POLE_IDS),
            str(result["removable_component_ids"]),
        ),
        validation_gate(
            "MC12_SUBTRACTION_AUTHORIZED",
            bool(
                result["claim_boundary"][
                    "valid_for_true_limit_MC04_MC12_subtraction"
                ]
            ),
            "MC04 and MC12 true residues fitted",
        ),
        validation_gate(
            "NO_MISSING_MARKERS",
            "MISSING_" not in serialized,
            "no MISSING_ token in checkpoint artifacts",
        ),
        validation_gate(
            "CLAIMS_LOCKED_FALSE",
            (
                all(
                    not result["claim_boundary"][field]
                    for field in CLAIM_FIELDS
                )
                and all(
                    row.get(field, "false").lower() == "false"
                    for row in claim_rows
                    for field in CLAIM_FIELDS
                    if field in row
                )
            ),
            "phase-space, UV, local-GR, and full-MTS claims false",
        ),
        validation_gate(
            "FORMALIZATION_WORKBENCH_UNCHANGED",
            current_formal_digest == reference_formal_digest,
            (
                f"reference={reference_formal_digest}; "
                f"current={current_formal_digest}"
            ),
        ),
        validation_gate(
            "RESOURCE_CONTRACT_RECORDED",
            (
                result["resource_contract"][
                    "maximum_task_python_processes"
                ]
                == 1
                and result["resource_contract"][
                    "worker_math_threads"
                ]
                == 1
            ),
            "one below-normal single-thread process",
        ),
    ]
    passed = all(row["passed"] for row in rows)
    write_csv(VALIDATION, rows)
    write_csv(RESIDUAL_VALIDATION, rows)
    render_document(result, passed)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "COMPLETED",
            "mode": "validation",
            "validation_passed": passed,
            "validation_gate_count": len(rows),
            "decision": result["decision"],
        },
    )
    return {
        "checkpoint": CHECKPOINT,
        "mode": "validation",
        "acceptance_passed": passed,
        "decision": (
            "VALIDATED_EXACT_MASK_ENERGY_POLE_RECLASSIFICATION"
            if passed
            else "VALIDATION_REQUIRES_REPAIR"
        ),
        "runtime_seconds": 0.0,
        "validation_gate_count": len(rows),
        "failed_gates": [
            row["gate_id"] for row in rows if not row["passed"]
        ],
        "valid_for_full_phase_space_coefficient": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("dry-run", "run", "validate"),
        default="dry-run",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.mode == "dry-run":
        result = dry_run()
    elif args.mode == "run":
        result = execute()
    elif args.mode == "validate":
        result = validate_outputs()
    else:
        raise RuntimeError(f"unsupported mode: {args.mode}")
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
