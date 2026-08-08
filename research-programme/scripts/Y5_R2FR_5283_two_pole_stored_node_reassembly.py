from __future__ import annotations

import argparse
import cmath
import csv
import ctypes
import hashlib
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
FORMAL = ROOT / "formalization-workbench"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
RESIDUALS = POST / "source-intake" / "mts_residuals"
SOURCE = FUNCTIONAL_RG / "5283"

NODES_5281 = (
    FUNCTIONAL_RG / "5281" / "high_order_energy_component_nodes.csv"
)
TOTALS_5281 = FUNCTIONAL_RG / "5281" / "high_order_energy_totals.csv"
RESULT_5281 = (
    FUNCTIONAL_RG / "5281" / "high_order_energy_convergence_result.json"
)
VALIDATION_5281 = (
    FUNCTIONAL_RG
    / "5281"
    / "high_order_energy_convergence_validation.csv"
)
PANELS_5280 = FUNCTIONAL_RG / "5280" / "composite_energy_panels.csv"
POLE_FITS_5280 = (
    FUNCTIONAL_RG / "5280" / "true_limit_energy_pole_fits.csv"
)
RESULT_5282 = (
    FUNCTIONAL_RG / "5282" / "exact_mask_energy_pole_result.json"
)
VALIDATION_5282 = (
    FUNCTIONAL_RG / "5282" / "exact_mask_energy_pole_validation.csv"
)
POLE_FITS_5282 = (
    FUNCTIONAL_RG / "5282" / "true_limit_exact_active_pole_fits.csv"
)
RECLASSIFICATION_5282 = (
    FUNCTIONAL_RG / "5282" / "exact_mask_energy_pole_reclassification.csv"
)

DRY_RUN = SOURCE / "two_pole_stored_node_reassembly_dry_run.json"
NODE_ROWS = SOURCE / "two_pole_reassembled_component_nodes.csv"
COMPONENT_TOTALS = SOURCE / "two_pole_component_totals.csv"
ENERGY_TOTALS = SOURCE / "two_pole_energy_totals.csv"
CONVERGENCE_ROWS = SOURCE / "two_pole_convergence.csv"
PANEL_ROWS = SOURCE / "two_pole_panel_diagnostics.csv"
RESULT = SOURCE / "two_pole_stored_node_reassembly_result.json"
VALIDATION = SOURCE / "two_pole_stored_node_reassembly_validation.csv"
RESIDUAL_VALIDATION = (
    RESIDUALS / "P8_Y5_BRR545_5283_VALIDATION.csv"
)
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5283-Y5-R2FR-two-pole-stored-node-reassembly.md"

CHECKPOINT = 5283
PARENT_CHECKPOINT = 5282
MARKER = "MTS_5283_TWO_POLE_STORED_NODE_REASSEMBLY"
REVISION = "two-pole-stored-node-reassembly-v1"
REGULATOR_IDS = ("E040", "E020")
QUADRATURE_ORDERS = (4, 8, 16)
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
LEGACY_SIX_IDS = ("MC03", "MC04", "MC07", "MC12", "MC14", "MC15")
HIDDEN_IDS = ("MC02", "MC08")
MATERIAL_COMPONENT_IDS = ("MC04", "MC12")
MID_ORDER_RELATIVE_CHANGE_LIMIT = 5.0e-3
HIGH_ORDER_RELATIVE_CHANGE_LIMIT = 1.0e-3
REPLAY_RELATIVE_ERROR_LIMIT = 2.0e-10
COMPONENT_SUM_RELATIVE_ERROR_LIMIT = 1.0e-12
CLAIM_FIELDS = (
    "valid_for_full_phase_space_coefficient",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)


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
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def serialized_hash(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def formal_inventory_digest() -> str:
    rows = [
        {
            "relative_path": str(path.relative_to(FORMAL)),
            "size": str(path.stat().st_size),
            "sha256": digest(path),
        }
        for path in sorted(
            (item for item in FORMAL.rglob("*") if item.is_file()),
            key=lambda item: str(item).lower(),
        )
    ]
    return serialized_hash(rows)


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        NODES_5281,
        TOTALS_5281,
        RESULT_5281,
        VALIDATION_5281,
        PANELS_5280,
        POLE_FITS_5280,
        RESULT_5282,
        VALIDATION_5282,
        POLE_FITS_5282,
        RECLASSIFICATION_5282,
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


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


def complex_from_row(row: dict[str, Any], prefix: str) -> complex:
    return complex(
        float(row[f"{prefix}_real"]),
        float(row[f"{prefix}_imaginary"]),
    )


def relative_complex_difference(first: complex, second: complex) -> float:
    return abs(first - second) / max(abs(first), abs(second), 1.0e-300)


def pole_dictionary(
    rows: list[dict[str, str]],
    material_only: bool,
) -> dict[tuple[str, str], dict[str, complex]]:
    poles: dict[tuple[str, str], dict[str, complex]] = {}
    for row in rows:
        if material_only and not parse_bool(row["material_pole"]):
            continue
        key = (row["epsilon_id"], row["component_id"])
        poles[key] = {
            "pole": complex(
                float(row["pole_real"]),
                float(row["pole_imaginary"]),
            ),
            "residue": complex(
                float(row["true_limit_residue_real"]),
                float(row["true_limit_residue_imaginary"]),
            ),
        }
    return poles


def integration_constants(
    panels: list[dict[str, str]],
    parent_totals: list[dict[str, str]],
) -> dict[str, float]:
    physical = next(
        row
        for row in parent_totals
        if row["row_type"] == "PHYSICAL_ENERGY_EXTRAPOLATION"
    )
    return {
        "energy_minimum": min(float(row["lower"]) for row in panels),
        "energy_maximum": max(float(row["upper"]) for row in panels),
        "kernel_multiplier": float(physical["kernel_multiplier"]),
        "physical_A00_weight": float(physical["physical_A00_weight"]),
    }


def analytic_terms(
    poles: dict[tuple[str, str], dict[str, complex]],
    constants: dict[str, float],
) -> dict[tuple[str, str], complex]:
    minimum = constants["energy_minimum"]
    maximum = constants["energy_maximum"]
    return {
        key: value["residue"]
        * (
            cmath.log(maximum - value["pole"])
            - cmath.log(minimum - value["pole"])
        )
        for key, value in poles.items()
    }


def assemble(
    source_nodes: list[dict[str, str]],
    poles: dict[tuple[str, str], dict[str, complex]],
    constants: dict[str, float],
    retain_nodes: bool,
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    regular_components: defaultdict[tuple[str, int, str], complex] = (
        defaultdict(complex)
    )
    raw_components: defaultdict[tuple[str, int, str], complex] = defaultdict(
        complex
    )
    panel_components: defaultdict[
        tuple[str, int, str, str], complex
    ] = defaultdict(complex)
    node_rows: list[dict[str, Any]] = []
    for row in source_nodes:
        epsilon_id = row["epsilon_id"]
        order = int(row["quadrature_order"])
        component_id = row["component_id"]
        energy = float(row["soft_energy"])
        weight = float(row["mapped_weight"])
        raw = complex(
            float(row["residue_real"]),
            float(row["residue_imaginary"]),
        )
        pole = poles.get((epsilon_id, component_id))
        singular = (
            pole["residue"] / (energy - pole["pole"])
            if pole is not None
            else 0.0j
        )
        regular = raw - singular
        component_key = (epsilon_id, order, component_id)
        raw_components[component_key] += weight * raw
        regular_components[component_key] += weight * regular
        panel_components[
            (epsilon_id, order, row["panel_id"], component_id)
        ] += weight * regular
        if retain_nodes:
            node_rows.append(
                {
                    "epsilon_id": epsilon_id,
                    "quadrature_order": order,
                    "panel_id": row["panel_id"],
                    "local_node_index": row["local_node_index"],
                    "soft_energy": energy,
                    "mapped_weight": weight,
                    "component_id": component_id,
                    "mask_active": row["mask_active"],
                    **complex_fields("raw_residue", raw),
                    **complex_fields("subtracted_singular", singular),
                    **complex_fields("regularized_residue", regular),
                    **complex_fields("weighted_regularized_residue", weight * regular),
                    "valid_for_two_pole_stored_node_reassembly": True,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    analytic = analytic_terms(poles, constants)
    corrected = dict(regular_components)
    for order in QUADRATURE_ORDERS:
        for key, value in analytic.items():
            epsilon_id, component_id = key
            corrected[(epsilon_id, order, component_id)] = (
                corrected.get((epsilon_id, order, component_id), 0.0j)
                + value
            )
    multiplier = (
        constants["kernel_multiplier"] * constants["physical_A00_weight"]
    )
    component_rows: list[dict[str, Any]] = []
    for order in QUADRATURE_ORDERS:
        for component_id in COMPONENT_IDS:
            E040 = corrected[("E040", order, component_id)]
            E020 = corrected[("E020", order, component_id)]
            physical = multiplier * (2.0 * E020 - E040)
            component_rows.append(
                {
                    "quadrature_order": order,
                    "component_id": component_id,
                    **complex_fields("E040_integral", E040),
                    **complex_fields("E020_integral", E020),
                    **complex_fields("physical_integral", physical),
                    "valid_for_two_pole_stored_node_reassembly": True,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    total_rows: list[dict[str, Any]] = []
    regulator_lookup: dict[tuple[int, str], dict[str, complex]] = {}
    for order in QUADRATURE_ORDERS:
        for epsilon_id in REGULATOR_IDS:
            raw_eight = sum(
                raw_components[(epsilon_id, order, component_id)]
                for component_id in COMPONENT_IDS
            )
            regular = sum(
                regular_components[(epsilon_id, order, component_id)]
                for component_id in COMPONENT_IDS
            )
            analytic_total = sum(
                (
                    analytic.get((epsilon_id, component_id), 0.0j)
                    for component_id in COMPONENT_IDS
                ),
                0.0j,
            )
            subtracted_eight = sum(
                corrected[(epsilon_id, order, component_id)]
                for component_id in COMPONENT_IDS
            )
            subtracted_six = sum(
                corrected[(epsilon_id, order, component_id)]
                for component_id in LEGACY_SIX_IDS
            )
            hidden = sum(
                corrected[(epsilon_id, order, component_id)]
                for component_id in HIDDEN_IDS
            )
            direct_total = regular + analytic_total
            regulator_lookup[(order, epsilon_id)] = {
                "raw_eight_integral": raw_eight,
                "subtracted_eight_integral": subtracted_eight,
                "subtracted_six_integral": subtracted_six,
                "hidden_MC02_MC08_integral": hidden,
            }
            total_rows.append(
                {
                    "row_type": "REGULATOR_ENERGY_INTEGRAL",
                    "epsilon_id": epsilon_id,
                    "quadrature_order": order,
                    **complex_fields("raw_eight_integral", raw_eight),
                    **complex_fields("regular_remainder", regular),
                    **complex_fields("analytic_singular", analytic_total),
                    **complex_fields(
                        "subtracted_eight_integral",
                        subtracted_eight,
                    ),
                    **complex_fields("subtracted_six_integral", subtracted_six),
                    **complex_fields(
                        "hidden_MC02_MC08_integral",
                        hidden,
                    ),
                    "component_sum_relative_residual": (
                        abs(subtracted_eight - direct_total)
                        / max(abs(subtracted_eight), abs(direct_total), 1.0)
                    ),
                    "valid_for_two_pole_stored_node_reassembly": True,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    for order in QUADRATURE_ORDERS:
        values: dict[str, complex] = {}
        for channel in (
            "raw_eight_integral",
            "subtracted_eight_integral",
            "subtracted_six_integral",
            "hidden_MC02_MC08_integral",
        ):
            values[channel] = multiplier * (
                2.0 * regulator_lookup[(order, "E020")][channel]
                - regulator_lookup[(order, "E040")][channel]
            )
        total_rows.append(
            {
                "row_type": "PHYSICAL_ENERGY_EXTRAPOLATION",
                "epsilon_id": "2E020_MINUS_E040",
                "quadrature_order": order,
                **complex_fields(
                    "raw_eight_integral",
                    values["raw_eight_integral"],
                ),
                **complex_fields(
                    "subtracted_eight_integral",
                    values["subtracted_eight_integral"],
                ),
                **complex_fields(
                    "subtracted_six_integral",
                    values["subtracted_six_integral"],
                ),
                **complex_fields(
                    "hidden_MC02_MC08_integral",
                    values["hidden_MC02_MC08_integral"],
                ),
                "kernel_multiplier": constants["kernel_multiplier"],
                "physical_A00_weight": constants["physical_A00_weight"],
                "valid_for_two_pole_stored_node_reassembly": True,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    panel_rows: list[dict[str, Any]] = []
    panel_ids = sorted({row["panel_id"] for row in source_nodes})
    for order in QUADRATURE_ORDERS:
        for panel_id in panel_ids:
            E040 = sum(
                panel_components[("E040", order, panel_id, component_id)]
                for component_id in COMPONENT_IDS
            )
            E020 = sum(
                panel_components[("E020", order, panel_id, component_id)]
                for component_id in COMPONENT_IDS
            )
            physical = multiplier * (2.0 * E020 - E040)
            panel_rows.append(
                {
                    "quadrature_order": order,
                    "panel_id": panel_id,
                    **complex_fields(
                        "physical_two_pole_regular_remainder",
                        physical,
                    ),
                    "valid_for_two_pole_panel_diagnosis": True,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    return node_rows, component_rows, total_rows, panel_rows


def convergence_rows(
    totals: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    physical = {
        int(row["quadrature_order"]): row
        for row in totals
        if row["row_type"] == "PHYSICAL_ENERGY_EXTRAPOLATION"
    }
    rows: list[dict[str, Any]] = []
    for channel in (
        "raw_eight_integral",
        "subtracted_eight_integral",
        "subtracted_six_integral",
        "hidden_MC02_MC08_integral",
    ):
        for lower, upper in zip(
            QUADRATURE_ORDERS[:-1],
            QUADRATURE_ORDERS[1:],
        ):
            lower_value = complex_from_row(physical[lower], channel)
            upper_value = complex_from_row(physical[upper], channel)
            rows.append(
                {
                    "channel": channel,
                    "lower_order": lower,
                    "upper_order": upper,
                    **complex_fields("lower_value", lower_value),
                    **complex_fields("upper_value", upper_value),
                    "relative_change": relative_complex_difference(
                        lower_value,
                        upper_value,
                    ),
                    "valid_for_two_pole_convergence_diagnosis": True,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    return rows


def replay_error(
    replay: list[dict[str, Any]],
    parent: list[dict[str, str]],
    channel: str,
) -> float:
    replay_physical = {
        int(row["quadrature_order"]): row
        for row in replay
        if row["row_type"] == "PHYSICAL_ENERGY_EXTRAPOLATION"
    }
    parent_physical = {
        int(row["quadrature_order"]): row
        for row in parent
        if row["row_type"] == "PHYSICAL_ENERGY_EXTRAPOLATION"
    }
    return max(
        relative_complex_difference(
            complex_from_row(replay_physical[order], channel),
            complex_from_row(parent_physical[order], channel),
        )
        for order in QUADRATURE_ORDERS
    )


def dry_run() -> dict[str, Any]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    required = (
        NODES_5281,
        TOTALS_5281,
        RESULT_5281,
        VALIDATION_5281,
        PANELS_5280,
        POLE_FITS_5280,
        RESULT_5282,
        VALIDATION_5282,
        POLE_FITS_5282,
        RECLASSIFICATION_5282,
    )
    parent = read_json(RESULT_5282)
    diagnosis = read_json(RESULT_5281)
    checks = {
        "required_sources_exist": all(path.exists() for path in required),
        "parent_5282_accepted": bool(parent["acceptance_passed"]),
        "parent_5282_validated": all(
            parse_bool(row["passed"]) for row in read_csv(VALIDATION_5282)
        ),
        "diagnosis_5281_accepted": bool(diagnosis["acceptance_passed"]),
        "diagnosis_5281_validated": all(
            parse_bool(row["passed"]) for row in read_csv(VALIDATION_5281)
        ),
        "two_material_poles_per_regulator": (
            len(
                pole_dictionary(
                    read_csv(POLE_FITS_5282),
                    material_only=True,
                )
            )
            == len(REGULATOR_IDS) * len(MATERIAL_COMPONENT_IDS)
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
            "DRY_RUN_ACCEPTED__REASSEMBLE_STORED_NODES_WITH_MC04_MC12"
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
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5283 dry run did not pass")
    parent = read_json(RESULT_5282)
    source_nodes = read_csv(NODES_5281)
    parent_totals = read_csv(TOTALS_5281)
    panels = read_csv(PANELS_5280)
    constants = integration_constants(panels, parent_totals)
    old_poles = pole_dictionary(
        read_csv(POLE_FITS_5280),
        material_only=False,
    )
    new_poles = pole_dictionary(
        read_csv(POLE_FITS_5282),
        material_only=True,
    )
    _, _, old_replay, _ = assemble(
        source_nodes,
        old_poles,
        constants,
        retain_nodes=False,
    )
    node_rows, component_rows, totals, panel_rows = assemble(
        source_nodes,
        new_poles,
        constants,
        retain_nodes=True,
    )
    convergence = convergence_rows(totals)
    old_subtracted_replay_error = replay_error(
        old_replay,
        parent_totals,
        "subtracted_eight_integral",
    )
    raw_replay_error = replay_error(
        totals,
        parent_totals,
        "raw_eight_integral",
    )
    subtracted_changes = {
        (int(row["lower_order"]), int(row["upper_order"])): float(
            row["relative_change"]
        )
        for row in convergence
        if row["channel"] == "subtracted_eight_integral"
    }
    middle_change = subtracted_changes[(4, 8)]
    high_change = subtracted_changes[(8, 16)]
    fixed_angle_converged = (
        middle_change <= MID_ORDER_RELATIVE_CHANGE_LIMIT
        and high_change <= HIGH_ORDER_RELATIVE_CHANGE_LIMIT
    )
    component_sum_residual = max(
        float(row.get("component_sum_relative_residual", 0.0))
        for row in totals
        if row["row_type"] == "REGULATOR_ENERGY_INTEGRAL"
    )
    largest_panel = max(
        (
            row
            for row in panel_rows
            if int(row["quadrature_order"]) == QUADRATURE_ORDERS[-1]
        ),
        key=lambda row: float(
            row["physical_two_pole_regular_remainder_magnitude"]
        ),
    )
    finite = all(
        math.isfinite(float(value))
        for row in totals
        for field, value in row.items()
        if field.endswith(("_real", "_imaginary", "_magnitude"))
    )
    checks = {
        "stored_node_count_preserved": len(node_rows) == len(source_nodes),
        "old_MC04_replay_reproduces_5281": (
            old_subtracted_replay_error <= REPLAY_RELATIVE_ERROR_LIMIT
        ),
        "raw_integral_reproduces_5281": (
            raw_replay_error <= REPLAY_RELATIVE_ERROR_LIMIT
        ),
        "material_pole_set_is_MC04_MC12": (
            {component_id for _, component_id in new_poles}
            == set(MATERIAL_COMPONENT_IDS)
            and len(new_poles)
            == len(REGULATOR_IDS) * len(MATERIAL_COMPONENT_IDS)
        ),
        "component_sum_crosscheck_passes": (
            component_sum_residual <= COMPONENT_SUM_RELATIVE_ERROR_LIMIT
        ),
        "all_reassembled_totals_finite": finite,
        "formalization_workbench_unchanged": (
            formal_inventory_digest()
            == str(parent["formalization_workbench_end_digest"])
        ),
        "claims_locked_false": True,
    }
    accepted = all(checks.values())
    physical_totals = {
        str(row["quadrature_order"]): {
            "subtracted_eight_real": row[
                "subtracted_eight_integral_real"
            ],
            "subtracted_eight_imaginary": row[
                "subtracted_eight_integral_imaginary"
            ],
            "subtracted_six_real": row[
                "subtracted_six_integral_real"
            ],
            "subtracted_six_imaginary": row[
                "subtracted_six_integral_imaginary"
            ],
            "hidden_real": row["hidden_MC02_MC08_integral_real"],
            "hidden_imaginary": row[
                "hidden_MC02_MC08_integral_imaginary"
            ],
        }
        for row in totals
        if row["row_type"] == "PHYSICAL_ENERGY_EXTRAPOLATION"
    }
    formal_end = formal_inventory_digest()
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "two-pole-stored-node-reassembly",
        "checks": checks,
        "acceptance_passed": accepted,
        "component_node_row_count": len(node_rows),
        "material_pole_components": list(MATERIAL_COMPONENT_IDS),
        "old_MC04_replay_maximum_relative_error": (
            old_subtracted_replay_error
        ),
        "raw_integral_replay_maximum_relative_error": raw_replay_error,
        "maximum_component_sum_relative_residual": component_sum_residual,
        "order4_to_order8_relative_change": middle_change,
        "order8_to_order16_relative_change": high_change,
        "fixed_angle_energy_converged": fixed_angle_converged,
        "largest_order16_regular_panel": largest_panel,
        "physical_order_totals": physical_totals,
        "integration_constants": constants,
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
            "node_reevaluation_count": 0,
            "sustained_redline_forbidden": True,
        },
        "runtime_seconds": time.perf_counter() - started,
        "decision": (
            (
                "ACCEPT_CONVERGED_TWO_POLE_FIXED_ANGLE_ENERGY_RULE__"
                "RESTORE_CHAMBER_ADAPTED_ANGULAR_INTEGRATION"
            )
            if accepted and fixed_angle_converged
            else (
                "TWO_POLE_REASSEMBLY_VALID_BUT_NOT_CONVERGED__"
                "LOCALIZE_REMAINING_INTERIOR_FEATURE"
                if accepted
                else "TWO_POLE_STORED_NODE_REASSEMBLY_REQUIRES_REPAIR"
            )
        ),
        "claim_boundary": {
            "valid_for_two_pole_stored_node_reassembly": accepted,
            "valid_for_converged_fixed_angle_energy_integral": (
                accepted and fixed_angle_converged
            ),
            "valid_for_angular_outer_integration": (
                accepted and fixed_angle_converged
            ),
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "The stored 5281 nodes are reassembled with both derived "
                "material poles. Convergence, rather than checkpoint "
                "completion, controls whether angular integration opens."
            ),
        },
    }
    write_csv(NODE_ROWS, node_rows)
    write_csv(COMPONENT_TOTALS, component_rows)
    write_csv(ENERGY_TOTALS, totals)
    write_csv(CONVERGENCE_ROWS, convergence)
    write_csv(PANEL_ROWS, panel_rows)
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "COMPLETED",
            "mode": result["mode"],
            "acceptance_passed": accepted,
            "fixed_angle_energy_converged": fixed_angle_converged,
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
    return {"gate_id": gate_id, "passed": passed, "detail": detail}


def render_document(
    result: dict[str, Any],
    validation_passed: bool,
) -> None:
    totals = "\n".join(
        (
            f"- order {order}: "
            f"`{values['subtracted_eight_real']:.12g}"
            f"{values['subtracted_eight_imaginary']:+.12g}i`"
        )
        for order, values in result["physical_order_totals"].items()
    )
    checks = "\n".join(
        f"- `{name}`: **{'PASS' if passed else 'FAIL'}**"
        for name, passed in result["checks"].items()
    )
    largest = result["largest_order16_regular_panel"]
    text = f"""# 5283 — Two-pole stored-node reassembly

## Purpose

Checkpoint 5282 proved that MC04 and MC12, not MC04 alone, are the
material fixed-angle energy poles. This checkpoint reuses all 20,608
already evaluated 5281 nodes, subtracts both sourced poles, restores
their analytic logarithmic integrals, and retests orders 4, 8, and 16.
No local-limit coefficient or root is reevaluated.

## Physical order sequence

{totals}

- order 4 to 8 relative change:
  `{result['order4_to_order8_relative_change']:.12g}`;
- order 8 to 16 relative change:
  `{result['order8_to_order16_relative_change']:.12g}`;
- fixed-angle convergence:
  `{result['fixed_angle_energy_converged']}`.

The largest order-16 regular panel is `{largest['panel_id']}` with
magnitude
`{float(largest['physical_two_pole_regular_remainder_magnitude']):.12g}`.

## Audit

- old MC04-only replay error:
  `{result['old_MC04_replay_maximum_relative_error']:.12g}`;
- raw-integral replay error:
  `{result['raw_integral_replay_maximum_relative_error']:.12g}`;
- node reevaluations: `0`.

{checks}

Validation: **{'PASS' if validation_passed else 'FAIL'}**.

## Claim boundary

This is a fixed-angle energy convergence gate only. It does not yet
authorize a full angular coefficient, UV claim, local-GR claim, or full
MTS claim.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    result = read_json(RESULT)
    required_csvs = (
        NODE_ROWS,
        COMPONENT_TOTALS,
        ENERGY_TOTALS,
        CONVERGENCE_ROWS,
        PANEL_ROWS,
    )
    csv_rows = {
        str(path): read_csv(path)
        for path in required_csvs
        if path.exists()
    }
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
    source_files = result["source_files"]
    current_formal_digest = formal_inventory_digest()
    reference_formal_digest = str(
        result["formalization_workbench_reference_digest"]
    )
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
            "PARENT_5282_ACCEPTED",
            bool(read_json(RESULT_5282)["acceptance_passed"]),
            str(read_json(RESULT_5282)["decision"]),
        ),
        validation_gate(
            "REASSEMBLY_ACCEPTED",
            bool(result["acceptance_passed"]),
            str(result["decision"]),
        ),
        validation_gate(
            "REQUIRED_CSVS_PARSE",
            len(csv_rows) == len(required_csvs) and all(csv_rows.values()),
            f"{len(csv_rows)}/{len(required_csvs)} non-empty CSVs",
        ),
        validation_gate(
            "NO_NODE_REEVALUATION",
            (
                result["resource_contract"]["node_reevaluation_count"] == 0
                and result["component_node_row_count"] == 20608
            ),
            f"{result['component_node_row_count']} stored rows",
        ),
        validation_gate(
            "REPLAY_CROSSCHECKS_PASS",
            (
                result["old_MC04_replay_maximum_relative_error"]
                <= REPLAY_RELATIVE_ERROR_LIMIT
                and result["raw_integral_replay_maximum_relative_error"]
                <= REPLAY_RELATIVE_ERROR_LIMIT
            ),
            (
                "old="
                f"{result['old_MC04_replay_maximum_relative_error']}; "
                "raw="
                f"{result['raw_integral_replay_maximum_relative_error']}"
            ),
        ),
        validation_gate(
            "MATERIAL_POLE_SET_EXACT",
            result["material_pole_components"]
            == list(MATERIAL_COMPONENT_IDS),
            str(result["material_pole_components"]),
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
                and result["resource_contract"]["worker_math_threads"] == 1
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
            "VALIDATED_TWO_POLE_STORED_NODE_REASSEMBLY"
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
