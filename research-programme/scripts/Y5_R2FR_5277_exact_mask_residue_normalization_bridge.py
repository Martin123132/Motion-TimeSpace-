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
SOURCE = FUNCTIONAL_RG / "5277"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5276 = (
    SCRIPTS
    / "Y5_R2FR_5276_spinor_denominator_incidence_and_analytic_pole_basis.py"
)
RESULT_5276 = FUNCTIONAL_RG / "5276" / "analytic_pole_basis_result.json"
VALIDATION_5276 = (
    FUNCTIONAL_RG / "5276" / "analytic_pole_basis_validation.csv"
)
LIMIT_ROWS_5275 = (
    FUNCTIONAL_RG
    / "5275"
    / "owner_resolved_local_coefficient_limits.csv"
)
COMPONENT_MAP_5239 = (
    FUNCTIONAL_RG / "5239" / "matched_regulator_component_map.csv"
)
FULL_MASK_LAWS_5274 = (
    FUNCTIONAL_RG / "5274" / "all_safe_component_boolean_mask_laws.csv"
)

DRY_RUN = SOURCE / "residue_normalization_bridge_dry_run.json"
NORMALIZATION_ROWS = SOURCE / "source_residue_normalization_bridge.csv"
TOTAL_ROWS = SOURCE / "corrected_source_component_totals.csv"
RESULT = SOURCE / "exact_mask_residue_normalization_result.json"
VALIDATION = SOURCE / "exact_mask_residue_normalization_validation.csv"
RESIDUAL_VALIDATION = (
    RESIDUALS / "P8_Y5_BRR545_5277_VALIDATION.csv"
)
STATUS = SOURCE / "status.json"
DOCUMENT = (
    POST / "5277-Y5-R2FR-exact-mask-residue-normalization-bridge.md"
)

CHECKPOINT = 5277
PARENT_CHECKPOINT = 5276
MARKER = "MTS_5277_EXACT_MASK_RESIDUE_NORMALIZATION_BRIDGE"
REVISION = "exact-mask-residue-normalization-bridge-v1"
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
LEGACY_MATERIAL_IDS = (
    "MC03",
    "MC04",
    "MC07",
    "MC12",
    "MC14",
    "MC15",
)
DOMINANT_IDS = ("MC04", "MC12", "MC14", "MC15")
SMALL_LEGACY_IDS = ("MC03", "MC07")
HIDDEN_IDS = ("MC02", "MC08")
MP_DECIMAL_DIGITS = 80
LEGACY_FRACTIONS = ("1e-5", "5e-6")
MAXIMUM_LEGACY_REPRODUCTION_RELATIVE_ERROR = 2.0e-8
MAXIMUM_DOMINANT_LIMIT_SHIFT = 1.0e-5
MINIMUM_SMALL_COMPONENT_LIMIT_SHIFT = 0.3
MINIMUM_HIDDEN_RESIDUE_MAGNITUDE = 1.0e-6
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


M5276 = load_module("mts_5276_for_5277", SCRIPT_5276)
M5275 = M5276.M5275
M5274 = M5275.M5274
M5040_MP = M5275.M5040_MP
mp = M5275.mp


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
        SCRIPT_5276,
        RESULT_5276,
        VALIDATION_5276,
        LIMIT_ROWS_5275,
        COMPONENT_MAP_5239,
        FULL_MASK_LAWS_5274,
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def formal_inventory_digest() -> str:
    return str(M5276.formal_inventory_digest())


def exact_surface_lookup() -> dict[str, dict[str, Any]]:
    return M5274.M5273.M5272.surface_lookup(
        M5274.M5273.M5272.surface_rows()
    )


def exact_mask_orientation(
    labels: tuple[str, str],
    event: dict[str, Any],
    surfaces: dict[str, dict[str, Any]],
) -> tuple[bool, int, tuple[bool, bool], tuple[float, float]]:
    owned: list[bool] = []
    values: list[float] = []
    for label in labels:
        surface_key = M5274.label_surface_key(label)
        value = M5274.M5273.surface_value(
            surfaces[surface_key],
            float(event["soft_energy"]),
            float(event["soft_cosine"]),
            float(event["decay_cosine"]),
        )
        parity = M5274.suffix_parity(label)
        owned.append(parity * value < 0.0)
        values.append(float(value))
    active = sum(owned) == 1
    orientation = 1 if owned[0] else -1
    return (
        active,
        orientation,
        (owned[0], owned[1]),
        (values[0], values[1]),
    )


def source_winding_delta(
    component: dict[str, Any],
    selected_role: str,
) -> int:
    entry = component[selected_role]
    partner_role = (
        "reciprocal"
        if selected_role == "representative"
        else "representative"
    )
    partner = component[partner_role]
    windings = M5274.M5239.suffix_windings(
        component["representative"],
        component["reciprocal"],
    )
    entry_suffix = entry["representing_pairs"][0][0].rsplit(
        "_", 1
    )[-1]
    partner_suffix = partner["representing_pairs"][0][0].rsplit(
        "_", 1
    )[-1]
    return int(windings[entry_suffix] - windings[partner_suffix])


def mp_collision_jacobian(
    event: dict[str, Any],
    target: Any,
    labels: tuple[str, str],
    relative_root: Any,
) -> Any:
    def global_root(
        label_index: int,
        varied_relative_root: Any,
    ) -> Any:
        return M5275.local_root_data(
            event,
            target,
            labels,
            varied_relative_root,
        )[-1][label_index]

    return mp.diff(
        lambda value: global_root(0, value),
        relative_root,
    ) - mp.diff(
        lambda value: global_root(1, value),
        relative_root,
    )


def residue_from_coefficient(
    coefficient: Any,
    relative_root: Any,
    global_root: Any,
    collision_jacobian: Any,
    orientation: int,
    winding_delta: int,
) -> Any:
    return (
        winding_delta
        * orientation
        * coefficient
        / (relative_root * global_root * collision_jacobian)
    )


def legacy_coefficient_estimate(
    high_precision_event: dict[str, Any],
    high_precision_target: Any,
    relative_root: Any,
    global_root: Any,
    soft_direction: list[Any],
    decay_direction: list[Any],
    internal: list[list[Any]],
) -> Any:
    scale = max(mp.mpf(1), abs(global_root))
    phase = mp.exp(mp.mpc(0, mp.mpf("0.37")))
    coefficients: list[Any] = []
    for fraction_text in LEGACY_FRACTIONS:
        displacement = (
            mp.mpf(fraction_text) * scale * phase
        )
        integrand = M5040_MP.finite_plus_integrand(
            internal,
            high_precision_event["soft_energy"],
            soft_direction,
            decay_direction,
            high_precision_target,
            global_root + displacement,
        )
        coefficients.append(integrand * displacement**2)
    return 2 * coefficients[1] - coefficients[0]


def relative_error(first: complex, second: complex) -> float:
    return abs(first - second) / max(
        abs(first),
        abs(second),
        1.0e-30,
    )


def normalization_rows() -> list[dict[str, Any]]:
    contract = M5274.M5239.source_contract()
    source_event = M5274.M5239.source_event(contract)
    source_point = next(
        row
        for row in M5275.selected_target_points()
        if row["point_id"] == "P000"
    )
    high_precision_event = M5275.event_as_mp(source_point)
    limit_rows = {
        (row["epsilon_id"], row["component_id"]): row
        for row in read_csv(LIMIT_ROWS_5275)
        if row["point_id"] == "P000"
    }
    surfaces = exact_surface_lookup()
    rows: list[dict[str, Any]] = []
    for epsilon_id in REGULATOR_IDS:
        (
            scattering_target,
            components,
            _,
        ) = M5274.component_inventory(
            epsilon_id,
            source_event,
            contract,
        )
        high_precision_target = M5275.target_as_mp(
            scattering_target
        )
        component_by_id = {
            str(component["component_id"]): component
            for component in components
        }
        for component_id in COMPONENT_IDS:
            component = component_by_id[component_id]
            limit = limit_rows[(epsilon_id, component_id)]
            selected_role = str(limit["selected_role"])
            entry = component[selected_role]
            labels = M5274.pair_labels(entry)
            relative_root = mp.mpc(
                limit["relative_root_real"],
                limit["relative_root_imaginary"],
            )
            (
                soft_direction,
                decay_direction,
                internal,
                global_roots,
            ) = M5275.local_root_data(
                high_precision_event,
                high_precision_target,
                labels,
                relative_root,
            )
            global_root = (global_roots[0] + global_roots[1]) / 2
            collision_jacobian = mp_collision_jacobian(
                high_precision_event,
                high_precision_target,
                labels,
                relative_root,
            )
            (
                mask_active,
                orientation,
                owned_labels,
                surface_values,
            ) = exact_mask_orientation(
                labels,
                source_event,
                surfaces,
            )
            winding_delta = source_winding_delta(
                component,
                selected_role,
            )
            true_coefficient = mp.mpc(
                limit["total_limit_real"],
                limit["total_limit_imaginary"],
            )
            legacy_coefficient = legacy_coefficient_estimate(
                high_precision_event,
                high_precision_target,
                relative_root,
                global_root,
                soft_direction,
                decay_direction,
                internal,
            )
            true_residue = residue_from_coefficient(
                true_coefficient,
                relative_root,
                global_root,
                collision_jacobian,
                orientation,
                winding_delta,
            )
            legacy_residue = residue_from_coefficient(
                legacy_coefficient,
                relative_root,
                global_root,
                collision_jacobian,
                orientation,
                winding_delta,
            )
            old_raw = complex(component["raw_contribution"])
            true_complex = complex(true_residue)
            legacy_complex = complex(legacy_residue)
            rows.append(
                {
                    "epsilon_id": epsilon_id,
                    "component_id": component_id,
                    "family": component["family"],
                    "selected_role": selected_role,
                    "representing_pair": "|".join(labels),
                    "mask_active": mask_active,
                    "first_label_owned": owned_labels[0],
                    "second_label_owned": owned_labels[1],
                    "first_surface_value": surface_values[0],
                    "second_surface_value": surface_values[1],
                    "orientation": orientation,
                    "source_winding_delta": winding_delta,
                    "collision_jacobian_magnitude": float(
                        abs(collision_jacobian)
                    ),
                    "true_coefficient_magnitude": float(
                        abs(true_coefficient)
                    ),
                    "legacy_coefficient_magnitude": float(
                        abs(legacy_coefficient)
                    ),
                    "true_residue_real": true_complex.real,
                    "true_residue_imaginary": true_complex.imag,
                    "true_residue_magnitude": abs(true_complex),
                    "legacy_residue_real": legacy_complex.real,
                    "legacy_residue_imaginary": legacy_complex.imag,
                    "legacy_residue_magnitude": abs(legacy_complex),
                    "old_raw_real": old_raw.real,
                    "old_raw_imaginary": old_raw.imag,
                    "old_raw_magnitude": abs(old_raw),
                    "legacy_reproduction_relative_error": (
                        relative_error(legacy_complex, old_raw)
                    ),
                    "true_limit_shift_from_old": (
                        relative_error(true_complex, old_raw)
                    ),
                    "hidden_by_old_classifier": (
                        component_id in HIDDEN_IDS
                    ),
                    "valid_for_source_normalization_bridge": True,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    return rows


def corrected_total_rows(
    rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for epsilon_id in REGULATOR_IDS:
        local = [
            row for row in rows if row["epsilon_id"] == epsilon_id
        ]
        true_total = sum(
            (
                complex(
                    float(row["true_residue_real"]),
                    float(row["true_residue_imaginary"]),
                )
                for row in local
            ),
            0.0j,
        )
        old_total = sum(
            (
                complex(
                    float(row["old_raw_real"]),
                    float(row["old_raw_imaginary"]),
                )
                for row in local
            ),
            0.0j,
        )
        hidden_total = sum(
            (
                complex(
                    float(row["true_residue_real"]),
                    float(row["true_residue_imaginary"]),
                )
                for row in local
                if row["component_id"] in HIDDEN_IDS
            ),
            0.0j,
        )
        result.append(
            {
                "epsilon_id": epsilon_id,
                "true_eight_component_total_real": true_total.real,
                "true_eight_component_total_imaginary": true_total.imag,
                "true_eight_component_total_magnitude": abs(
                    true_total
                ),
                "old_six_component_total_real": old_total.real,
                "old_six_component_total_imaginary": old_total.imag,
                "old_six_component_total_magnitude": abs(old_total),
                "eight_minus_six_real": (
                    true_total - old_total
                ).real,
                "eight_minus_six_imaginary": (
                    true_total - old_total
                ).imag,
                "eight_minus_six_magnitude": abs(
                    true_total - old_total
                ),
                "relative_total_shift": relative_error(
                    true_total,
                    old_total,
                ),
                "hidden_MC02_MC08_total_real": hidden_total.real,
                "hidden_MC02_MC08_total_imaginary": (
                    hidden_total.imag
                ),
                "hidden_MC02_MC08_total_magnitude": abs(
                    hidden_total
                ),
                "kernel_multiplier": (
                    M5274.M5231.KERNEL_MULTIPLIER
                ),
                "physical_A00_weight": (
                    M5274.M5231.PHYSICAL_A00_WEIGHT
                ),
                "valid_for_source_normalization_bridge": True,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return result


def dry_run() -> dict[str, Any]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    required = (
        SCRIPT_5276,
        RESULT_5276,
        VALIDATION_5276,
        LIMIT_ROWS_5275,
        COMPONENT_MAP_5239,
        FULL_MASK_LAWS_5274,
    )
    parent = read_json(RESULT_5276)
    parent_validation = read_csv(VALIDATION_5276)
    checks = {
        "required_sources_exist": all(
            path.exists() for path in required
        ),
        "parent_5276_accepted": bool(parent["acceptance_passed"]),
        "parent_5276_validated": all(
            row["passed"].lower() == "true"
            for row in parent_validation
        ),
        "parent_analytic_eight_basis": (
            parent["analytic_double_component_ids"]
            == list(COMPONENT_IDS)
        ),
        "source_limit_rows_complete": (
            sum(
                row["point_id"] == "P000"
                and row["component_id"] in COMPONENT_IDS
                for row in read_csv(LIMIT_ROWS_5275)
            )
            == len(REGULATOR_IDS) * len(COMPONENT_IDS)
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
            "DRY_RUN_ACCEPTED__REBUILD_SOURCE_RESIDUE_NORMALIZATION"
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
    mp.mp.dps = MP_DECIMAL_DIGITS
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5277 dry run did not pass")
    parent = read_json(RESULT_5276)
    rows = normalization_rows()
    totals = corrected_total_rows(rows)
    material_rows = [
        row
        for row in rows
        if row["component_id"] in LEGACY_MATERIAL_IDS
    ]
    dominant_rows = [
        row for row in rows if row["component_id"] in DOMINANT_IDS
    ]
    small_rows = [
        row
        for row in rows
        if row["component_id"] in SMALL_LEGACY_IDS
    ]
    hidden_rows = [
        row for row in rows if row["component_id"] in HIDDEN_IDS
    ]
    maximum_legacy_reproduction = max(
        float(row["legacy_reproduction_relative_error"])
        for row in material_rows
    )
    maximum_dominant_shift = max(
        float(row["true_limit_shift_from_old"])
        for row in dominant_rows
    )
    minimum_small_shift = min(
        float(row["true_limit_shift_from_old"])
        for row in small_rows
    )
    minimum_hidden_magnitude = min(
        float(row["true_residue_magnitude"])
        for row in hidden_rows
    )
    checks = {
        "parent_5276_accepted": bool(parent["acceptance_passed"]),
        "complete_two_regulator_eight_component_bridge": (
            len(rows) == len(REGULATOR_IDS) * len(COMPONENT_IDS)
        ),
        "all_exact_masks_active_at_source": all(
            bool(row["mask_active"]) for row in rows
        ),
        "all_ownership_states_unique": all(
            bool(row["first_label_owned"])
            != bool(row["second_label_owned"])
            for row in rows
        ),
        "all_source_winding_deltas_are_two": all(
            abs(int(row["source_winding_delta"])) == 2
            for row in rows
        ),
        "legacy_formula_reproduces_old_material_rows": (
            maximum_legacy_reproduction
            <= MAXIMUM_LEGACY_REPRODUCTION_RELATIVE_ERROR
        ),
        "dominant_true_limits_stable": (
            maximum_dominant_shift <= MAXIMUM_DOMINANT_LIMIT_SHIFT
        ),
        "small_component_truncation_bias_detected": (
            minimum_small_shift
            >= MINIMUM_SMALL_COMPONENT_LIMIT_SHIFT
        ),
        "hidden_MC02_MC08_residues_nonzero": (
            minimum_hidden_magnitude
            >= MINIMUM_HIDDEN_RESIDUE_MAGNITUDE
        ),
        "corrected_totals_finite": all(
            math.isfinite(
                float(row["true_eight_component_total_magnitude"])
            )
            for row in totals
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
        "mode": "exact-mask-residue-normalization-bridge",
        "checks": checks,
        "acceptance_passed": accepted,
        "normalization_row_count": len(rows),
        "mp_decimal_digits": MP_DECIMAL_DIGITS,
        "legacy_fractions": list(LEGACY_FRACTIONS),
        "maximum_legacy_material_reproduction_relative_error": (
            maximum_legacy_reproduction
        ),
        "maximum_dominant_true_limit_shift": maximum_dominant_shift,
        "minimum_small_component_true_limit_shift": (
            minimum_small_shift
        ),
        "minimum_hidden_residue_magnitude": (
            minimum_hidden_magnitude
        ),
        "corrected_source_totals": {
            row["epsilon_id"]: {
                "true_eight_component_total_real": row[
                    "true_eight_component_total_real"
                ],
                "true_eight_component_total_imaginary": row[
                    "true_eight_component_total_imaginary"
                ],
                "old_six_component_total_real": row[
                    "old_six_component_total_real"
                ],
                "old_six_component_total_imaginary": row[
                    "old_six_component_total_imaginary"
                ],
                "relative_total_shift": row["relative_total_shift"],
                "hidden_MC02_MC08_total_magnitude": row[
                    "hidden_MC02_MC08_total_magnitude"
                ],
            }
            for row in totals
        },
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
            "ACCEPT_TRUE_LOCAL_LIMIT_RESIDUE_NORMALIZATION__"
            "REPLACE_LEGACY_SOURCE_VALUES__PROCEED_TO_CUBATURE"
            if accepted
            else "RESIDUE_NORMALIZATION_BRIDGE_REQUIRES_REPAIR"
        ),
        "claim_boundary": {
            "valid_for_legacy_fixed_displacement_as_true_limit": False,
            "valid_for_true_local_limit_residue_evaluator": accepted,
            "valid_for_eight_component_exact_mask_cubature_smoke": (
                accepted
            ),
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "The old finite-displacement estimator is reproduced, "
                "which validates the orientation and winding bridge, "
                "but it is not the δ→0 coefficient for small residues. "
                "The corrected evaluator must be used in cubature."
            ),
        },
    }
    write_csv(NORMALIZATION_ROWS, rows)
    write_csv(TOTAL_ROWS, totals)
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
    totals = "\n".join(
        (
            f"- `{epsilon_id}`: corrected "
            f"`{values['true_eight_component_total_real']:.12g}"
            f"{values['true_eight_component_total_imaginary']:+.12g}i`; "
            f"old `{values['old_six_component_total_real']:.12g}"
            f"{values['old_six_component_total_imaginary']:+.12g}i`; "
            f"relative shift `{values['relative_total_shift']:.12g}`."
        )
        for epsilon_id, values in result[
            "corrected_source_totals"
        ].items()
    )
    text = f"""# 5277 — Exact-mask residue-normalization bridge

## Purpose

The eight-component basis and exact Boolean masks are not enough by
themselves. The pointwise contribution also needs the correct sign and
normalization:

`Delta w * orientation * C_2 / (R G (g_1'-g_2'))`,

where `C_2=lim_(delta->0) delta^2 I(G+delta)`.

## Exact sign bridge

- Root ownership is obtained directly from the analytic surface:
  a `u` root is inside when `F<0`, while a `v` root is inside when
  `F>0`.
- The local residue orientation is `+1` when the first pair label is
  owned and `-1` otherwise.
- Every active source component has `|Delta w|=2`.

All sixteen regulator/component source rows have an active exact mask
and unique ownership.

## Finite-displacement diagnosis

The legacy estimate

`C_legacy = 2 C(5e-6) - C(1e-5)`

reproduces every old material source residue to maximum relative error
`{result['maximum_legacy_material_reproduction_relative_error']:.12g}`.
This confirms the sign, Jacobian, and winding bridge.

It also proves that the discrepancy is estimator truncation rather than
branch misidentification:

- dominant components shift by at most
  `{result['maximum_dominant_true_limit_shift']:.12g}`;
- MC03/MC07 shift by at least
  `{result['minimum_small_component_true_limit_shift']:.12g}`;
- MC02/MC08 have nonzero true residues, with minimum magnitude
  `{result['minimum_hidden_residue_magnitude']:.12g}`.

## Corrected source totals

{totals}

## Acceptance gates

{checks}

Validation: **{'PASS' if validation_passed else 'FAIL'}**.

## Claim boundary

The true local-limit residue evaluator is now normalized and may be
used in an eight-component exact-mask cubature smoke. This source-event
bridge is not itself a phase-space integral, UV coefficient, local-GR
result, or full-MTS claim.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    result = read_json(RESULT)
    parent = read_json(RESULT_5276)
    required_csvs = (NORMALIZATION_ROWS, TOTAL_ROWS)
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
            "PARENT_5276_ACCEPTED",
            bool(parent["acceptance_passed"]),
            str(parent["decision"]),
        ),
        validation_gate(
            "NORMALIZATION_BRIDGE_ACCEPTED",
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
            "COMPLETE_SOURCE_MATRIX",
            int(result["normalization_row_count"]) == 16,
            f"{result['normalization_row_count']} rows",
        ),
        validation_gate(
            "LEGACY_REPRODUCTION",
            float(
                result[
                    "maximum_legacy_material_reproduction_relative_error"
                ]
            )
            <= MAXIMUM_LEGACY_REPRODUCTION_RELATIVE_ERROR,
            "legacy estimator independently reproduced",
        ),
        validation_gate(
            "TRUE_LIMIT_CORRECTION_RESOLVED",
            (
                float(
                    result["maximum_dominant_true_limit_shift"]
                )
                <= MAXIMUM_DOMINANT_LIMIT_SHIFT
                and float(
                    result[
                        "minimum_small_component_true_limit_shift"
                    ]
                )
                >= MINIMUM_SMALL_COMPONENT_LIMIT_SHIFT
                and float(
                    result["minimum_hidden_residue_magnitude"]
                )
                >= MINIMUM_HIDDEN_RESIDUE_MAGNITUDE
            ),
            "dominant stable; small biased; hidden nonzero",
        ),
        validation_gate(
            "TRUE_EVALUATOR_AUTHORIZED",
            (
                not result["claim_boundary"][
                    "valid_for_legacy_fixed_displacement_as_true_limit"
                ]
                and result["claim_boundary"][
                    "valid_for_true_local_limit_residue_evaluator"
                ]
            ),
            "legacy false; true local limit accepted",
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
            "VALIDATED_TRUE_LOCAL_LIMIT_RESIDUE_NORMALIZATION"
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
