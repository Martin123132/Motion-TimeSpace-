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
SOURCE = FUNCTIONAL_RG / "5281"
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
PANELS_5280 = (
    FUNCTIONAL_RG / "5280" / "composite_energy_panels.csv"
)
POLE_FITS_5280 = (
    FUNCTIONAL_RG / "5280" / "true_limit_energy_pole_fits.csv"
)
ORDER_TOTALS_5280 = (
    FUNCTIONAL_RG / "5280" / "energy_first_order_totals.csv"
)

DRY_RUN = SOURCE / "high_order_energy_convergence_dry_run.json"
NODE_ROWS = SOURCE / "high_order_energy_component_nodes.csv"
ORDER_TOTALS = SOURCE / "high_order_energy_totals.csv"
COMPONENT_TOTALS = SOURCE / "high_order_component_totals.csv"
PANEL_DIAGNOSTICS = SOURCE / "high_order_panel_diagnostics.csv"
CONVERGENCE_ROWS = SOURCE / "high_order_energy_convergence.csv"
RESULT = SOURCE / "high_order_energy_convergence_result.json"
VALIDATION = SOURCE / "high_order_energy_convergence_validation.csv"
RESIDUAL_VALIDATION = (
    RESIDUALS / "P8_Y5_BRR545_5281_VALIDATION.csv"
)
STATUS = SOURCE / "status.json"
DOCUMENT = (
    POST
    / "5281-Y5-R2FR-high-order-energy-convergence-and-endpoint-diagnosis.md"
)

CHECKPOINT = 5281
PARENT_CHECKPOINT = 5280
MARKER = "MTS_5281_HIGH_ORDER_ENERGY_CONVERGENCE_AND_ENDPOINT_DIAGNOSIS"
REVISION = "high-order-energy-convergence-endpoint-diagnosis-v1"
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
QUADRATURE_ORDERS = (4, 8, 16)
MID_ORDER_RELATIVE_CHANGE_LIMIT = 5.0e-3
HIGH_ORDER_RELATIVE_CHANGE_LIMIT = 1.0e-3
ORDER4_REPRODUCTION_LIMIT = 2.0e-10
COEFFICIENT_CONVERGENCE_LIMIT = 1.0e-6
ROOT_RESIDUAL_LIMIT = 1.0e-50
ROOT_REFINEMENT_DISTANCE_LIMIT = 1.0e-7
ENDPOINT_DIAGNOSTIC_WIDTH = 5.0e-2
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


M5280 = load_module("mts_5280_for_5281", SCRIPT_5280)
M5279 = M5280.M5279
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
        PANELS_5280,
        POLE_FITS_5280,
        ORDER_TOTALS_5280,
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def formal_inventory_digest() -> str:
    return str(M5280.formal_inventory_digest())


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return {
        f"{prefix}_real": float(value.real),
        f"{prefix}_imaginary": float(value.imag),
        f"{prefix}_magnitude": float(abs(value)),
    }


def complex_from_row(
    row: dict[str, Any],
    prefix: str,
) -> complex:
    return complex(
        float(row[f"{prefix}_real"]),
        float(row[f"{prefix}_imaginary"]),
    )


def relative_complex_difference(
    first: complex,
    second: complex,
) -> float:
    return abs(first - second) / max(
        abs(first),
        abs(second),
        1.0,
    )


def component_total_rows(
    node_rows: list[dict[str, Any]],
    pole_fits: list[dict[str, str]],
) -> list[dict[str, Any]]:
    grouped: defaultdict[
        tuple[str, int, str],
        complex,
    ] = defaultdict(complex)
    for row in node_rows:
        key = (
            str(row["epsilon_id"]),
            int(row["quadrature_order"]),
            str(row["component_id"]),
        )
        grouped[key] += float(row["mapped_weight"]) * complex(
            float(row["regularized_residue_real"]),
            float(row["regularized_residue_imaginary"]),
        )
    analytic = {}
    energy_minimum = float(M5274.M5267.ENERGY_MINIMUM)
    energy_maximum = float(M5274.M5267.ENERGY_MAXIMUM)
    for row in pole_fits:
        epsilon_id = row["epsilon_id"]
        pole = complex(
            float(row["pole_real"]),
            float(row["pole_imaginary"]),
        )
        residue = complex(
            float(row["true_limit_residue_real"]),
            float(row["true_limit_residue_imaginary"]),
        )
        analytic[epsilon_id] = residue * (
            __import__("cmath").log(energy_maximum - pole)
            - __import__("cmath").log(energy_minimum - pole)
        )
    corrected = dict(grouped)
    for epsilon_id in REGULATOR_IDS:
        for order in QUADRATURE_ORDERS:
            corrected[
                (epsilon_id, order, M5280.POLE_COMPONENT_ID)
            ] += analytic[epsilon_id]
    multiplier = (
        M5274.M5231.PHYSICAL_A00_WEIGHT
        * M5274.M5231.KERNEL_MULTIPLIER
    )
    rows: list[dict[str, Any]] = []
    for order in QUADRATURE_ORDERS:
        for component_id in COMPONENT_IDS:
            E040 = corrected[("E040", order, component_id)]
            E020 = corrected[("E020", order, component_id)]
            physical = multiplier * (2.0 * E020 - E040)
            rows.append(
                {
                    "quadrature_order": order,
                    "component_id": component_id,
                    **complex_fields("E040_integral", E040),
                    **complex_fields("E020_integral", E020),
                    **complex_fields("physical_integral", physical),
                    "valid_for_high_order_energy_diagnosis": True,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    return rows


def panel_diagnostic_rows(
    node_rows: list[dict[str, Any]],
    panels: list[dict[str, str]],
) -> list[dict[str, Any]]:
    panel_lookup = {
        row["panel_id"]: row for row in panels
    }
    grouped: defaultdict[
        tuple[int, str, str],
        complex,
    ] = defaultdict(complex)
    for row in node_rows:
        grouped[
            (
                int(row["quadrature_order"]),
                str(row["epsilon_id"]),
                str(row["panel_id"]),
            )
        ] += float(row["mapped_weight"]) * complex(
            float(row["regularized_residue_real"]),
            float(row["regularized_residue_imaginary"]),
        )
    multiplier = (
        M5274.M5231.PHYSICAL_A00_WEIGHT
        * M5274.M5231.KERNEL_MULTIPLIER
    )
    energy_minimum = float(M5274.M5267.ENERGY_MINIMUM)
    energy_maximum = float(M5274.M5267.ENERGY_MAXIMUM)
    rows: list[dict[str, Any]] = []
    for order in QUADRATURE_ORDERS:
        for panel_id in sorted(panel_lookup):
            panel = panel_lookup[panel_id]
            E040 = grouped[(order, "E040", panel_id)]
            E020 = grouped[(order, "E020", panel_id)]
            physical = multiplier * (2.0 * E020 - E040)
            midpoint = float(panel["midpoint"])
            endpoint_region = (
                midpoint
                <= energy_minimum + ENDPOINT_DIAGNOSTIC_WIDTH
                or midpoint
                >= energy_maximum - ENDPOINT_DIAGNOSTIC_WIDTH
            )
            rows.append(
                {
                    "quadrature_order": order,
                    "panel_id": panel_id,
                    "lower": panel["lower"],
                    "upper": panel["upper"],
                    "midpoint": midpoint,
                    "width": panel["width"],
                    "endpoint_region": endpoint_region,
                    **complex_fields(
                        "physical_regular_remainder",
                        physical,
                    ),
                    "valid_for_endpoint_diagnosis": True,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    return rows


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
        for lower_order, upper_order in zip(
            QUADRATURE_ORDERS[:-1],
            QUADRATURE_ORDERS[1:],
        ):
            lower = complex_from_row(
                physical[lower_order],
                channel,
            )
            upper = complex_from_row(
                physical[upper_order],
                channel,
            )
            rows.append(
                {
                    "channel": channel,
                    "lower_order": lower_order,
                    "upper_order": upper_order,
                    **complex_fields("lower_value", lower),
                    **complex_fields("upper_value", upper),
                    "relative_change": relative_complex_difference(
                        lower,
                        upper,
                    ),
                    "valid_for_high_order_energy_diagnosis": True,
                    "valid_for_converged_fixed_angle_energy_integral": (
                        False
                    ),
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    return rows


def order4_reproduction_error(
    totals: list[dict[str, Any]],
) -> float:
    current = next(
        row
        for row in totals
        if row["row_type"] == "PHYSICAL_ENERGY_EXTRAPOLATION"
        and int(row["quadrature_order"]) == 4
    )
    parent = next(
        row
        for row in read_csv(ORDER_TOTALS_5280)
        if row["row_type"] == "PHYSICAL_ENERGY_EXTRAPOLATION"
        and int(row["quadrature_order"]) == 4
    )
    return relative_complex_difference(
        complex_from_row(current, "subtracted_eight_integral"),
        complex_from_row(parent, "subtracted_eight_integral"),
    )


def dry_run() -> dict[str, Any]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    required = (
        SCRIPT_5280,
        RESULT_5280,
        VALIDATION_5280,
        PANELS_5280,
        POLE_FITS_5280,
        ORDER_TOTALS_5280,
    )
    parent = read_json(RESULT_5280)
    parent_validation = read_csv(VALIDATION_5280)
    checks = {
        "required_sources_exist": all(
            path.exists() for path in required
        ),
        "parent_5280_accepted": bool(parent["acceptance_passed"]),
        "parent_5280_validated": all(
            row["passed"].lower() == "true"
            for row in parent_validation
        ),
        "pointwise_evaluator_authorized": bool(
            parent["claim_boundary"][
                "valid_for_algebraic_pointwise_evaluator"
            ]
        ),
        "panel_and_pole_inputs_parse": (
            bool(read_csv(PANELS_5280))
            and len(read_csv(POLE_FITS_5280))
            == len(REGULATOR_IDS)
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
        "quadrature_orders": list(QUADRATURE_ORDERS),
        "decision": (
            "DRY_RUN_ACCEPTED__RUN_HIGH_ORDER_ENERGY_CONVERGENCE"
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
        raise RuntimeError("5281 dry run did not pass")
    parent = read_json(RESULT_5280)
    context = M5280.source_context()
    panels = read_csv(PANELS_5280)
    pole_fits = read_csv(POLE_FITS_5280)
    cache: dict[tuple[str, float, str], dict[str, Any]] = {}
    original_orders = M5280.QUADRATURE_ORDERS
    original_status = M5280.STATUS
    M5280.QUADRATURE_ORDERS = QUADRATURE_ORDERS
    M5280.STATUS = STATUS
    try:
        node_rows, regulator_totals = M5280.integrate_energy(
            context,
            panels,
            pole_fits,
            cache,
        )
        totals = M5280.physical_total_rows(regulator_totals)
    finally:
        M5280.QUADRATURE_ORDERS = original_orders
        M5280.STATUS = original_status
    components = component_total_rows(node_rows, pole_fits)
    panel_rows = panel_diagnostic_rows(node_rows, panels)
    convergence = convergence_rows(totals)
    audited = [
        evaluation
        for evaluation in cache.values()
        if bool(evaluation["convergence_audited"])
        and bool(evaluation["mask_active"])
    ]
    active = [
        evaluation
        for evaluation in cache.values()
        if bool(evaluation["mask_active"])
    ]
    maximum_coefficient_change = max(
        (
            float(row["coefficient_relative_change"])
            for row in audited
        ),
        default=0.0,
    )
    maximum_root_residual = max(
        (
            float(row["root_equation_residual"])
            for row in active
        ),
        default=0.0,
    )
    maximum_refinement_distance = max(
        (
            float(row["root_refinement_chordal_distance"])
            for row in active
        ),
        default=0.0,
    )
    order4_error = order4_reproduction_error(totals)
    subtracted_changes = {
        (
            int(row["lower_order"]),
            int(row["upper_order"]),
        ): float(row["relative_change"])
        for row in convergence
        if row["channel"] == "subtracted_eight_integral"
    }
    mid_change = subtracted_changes[(4, 8)]
    high_change = subtracted_changes[(8, 16)]
    fixed_angle_converged = (
        mid_change <= MID_ORDER_RELATIVE_CHANGE_LIMIT
        and high_change <= HIGH_ORDER_RELATIVE_CHANGE_LIMIT
    )
    endpoint_rows = [
        row
        for row in panel_rows
        if bool(row["endpoint_region"])
        and int(row["quadrature_order"])
        == QUADRATURE_ORDERS[-1]
    ]
    endpoint_magnitude = sum(
        float(row["physical_regular_remainder_magnitude"])
        for row in endpoint_rows
    )
    all_panel_magnitude = sum(
        float(row["physical_regular_remainder_magnitude"])
        for row in panel_rows
        if int(row["quadrature_order"])
        == QUADRATURE_ORDERS[-1]
    )
    endpoint_fraction = endpoint_magnitude / max(
        all_panel_magnitude,
        1.0e-300,
    )
    checks = {
        "parent_5280_accepted": bool(parent["acceptance_passed"]),
        "orders_4_8_16_completed": (
            {
                int(row["quadrature_order"])
                for row in totals
                if row["row_type"]
                == "PHYSICAL_ENERGY_EXTRAPOLATION"
            }
            == set(QUADRATURE_ORDERS)
        ),
        "order4_reproduces_5280": (
            order4_error <= ORDER4_REPRODUCTION_LIMIT
        ),
        "audited_coefficients_converged": (
            bool(audited)
            and maximum_coefficient_change
            <= COEFFICIENT_CONVERGENCE_LIMIT
        ),
        "all_active_roots_refined": (
            maximum_root_residual <= ROOT_RESIDUAL_LIMIT
            and maximum_refinement_distance
            <= ROOT_REFINEMENT_DISTANCE_LIMIT
        ),
        "component_totals_close_order_totals": all(
            float(row["component_sum_relative_residual"])
            <= 1.0e-10
            for row in regulator_totals
        ),
        "endpoint_diagnosis_complete": bool(endpoint_rows),
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
            "hidden_real": row[
                "hidden_MC02_MC08_integral_real"
            ],
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
        "mode": "high-order-energy-convergence-endpoint-diagnosis",
        "checks": checks,
        "acceptance_passed": accepted,
        "quadrature_orders": list(QUADRATURE_ORDERS),
        "component_node_row_count": len(node_rows),
        "unique_component_evaluation_count": len(cache),
        "active_component_evaluation_count": len(active),
        "coefficient_audit_count": len(audited),
        "maximum_audited_coefficient_relative_change": (
            maximum_coefficient_change
        ),
        "maximum_root_equation_residual": maximum_root_residual,
        "maximum_root_refinement_chordal_distance": (
            maximum_refinement_distance
        ),
        "order4_reproduction_relative_error": order4_error,
        "order4_to_order8_relative_change": mid_change,
        "order8_to_order16_relative_change": high_change,
        "fixed_angle_energy_converged": fixed_angle_converged,
        "endpoint_regular_remainder_fraction": endpoint_fraction,
        "physical_order_totals": physical_totals,
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
            (
                "ACCEPT_CONVERGED_TRUE_LIMIT_FIXED_ANGLE_ENERGY_RULE__"
                "RESTORE_ANGULAR_OUTER_INTEGRATION"
            )
            if accepted and fixed_angle_converged
            else (
                "HIGH_ORDER_ENERGY_NOT_CONVERGED__"
                "DERIVE_ENDPOINT_ASYMPTOTIC_SUBTRACTIONS"
                if accepted
                else "HIGH_ORDER_ENERGY_RUN_REQUIRES_REPAIR"
            )
        ),
        "claim_boundary": {
            "valid_for_high_order_energy_diagnosis": accepted,
            "valid_for_converged_fixed_angle_energy_integral": (
                accepted and fixed_angle_converged
            ),
            "valid_for_endpoint_asymptotic_control": False,
            "valid_for_angular_outer_integration": False,
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "Orders 4, 8, and 16 test the true-limit, "
                "pole-subtracted fixed-angle energy rule. Angular "
                "integration remains forbidden until this energy rule "
                "converges; if it does not, endpoint asymptotics rather "
                "than still higher blind tensor orders are required."
            ),
        },
    }
    write_csv(NODE_ROWS, node_rows)
    write_csv(ORDER_TOTALS, totals)
    write_csv(COMPONENT_TOTALS, components)
    write_csv(PANEL_DIAGNOSTICS, panel_rows)
    write_csv(CONVERGENCE_ROWS, convergence)
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
            f"- order `{order}`: eight "
            f"`{values['subtracted_eight_real']:.12g}"
            f"{values['subtracted_eight_imaginary']:+.12g}i`; "
            f"six `{values['subtracted_six_real']:.12g}"
            f"{values['subtracted_six_imaginary']:+.12g}i`; "
            f"hidden `{values['hidden_real']:.12g}"
            f"{values['hidden_imaginary']:+.12g}i`."
        )
        for order, values in result["physical_order_totals"].items()
    )
    text = f"""# 5281 — High-order energy convergence and endpoint diagnosis

## Purpose

Checkpoint 5280 proved the corrected pole-subtraction mechanism at
orders two and four. This checkpoint raises the fixed-angle energy
calculation to orders 4, 8, and 16 using the same exact panels, true
local-limit residues, and algebraic branch selector.

## Results

{totals}

- order 4 to 8 relative change:
  `{result['order4_to_order8_relative_change']:.12g}`;
- order 8 to 16 relative change:
  `{result['order8_to_order16_relative_change']:.12g}`;
- endpoint-panel fraction of absolute regular-remainder mass:
  `{result['endpoint_regular_remainder_fraction']:.12g}`;
- fixed-angle convergence accepted:
  `{result['fixed_angle_energy_converged']}`.

The order-4 value reproduces checkpoint 5280 to relative error
`{result['order4_reproduction_relative_error']:.12g}`.

## Acceptance gates

{checks}

Validation: **{'PASS' if validation_passed else 'FAIL'}**.

## Claim boundary

This checkpoint decides whether ordinary high-order panel quadrature is
enough. If order 8 to 16 is still unstable, the next move is not blind
order inflation: the endpoint scaling must be derived and subtracted.
No angular, full phase-space, UV, local-GR, or full-MTS claim is made.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    result = read_json(RESULT)
    parent = read_json(RESULT_5280)
    required_csvs = (
        NODE_ROWS,
        ORDER_TOTALS,
        COMPONENT_TOTALS,
        PANEL_DIAGNOSTICS,
        CONVERGENCE_ROWS,
    )
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
            "HIGH_ORDER_RUN_ACCEPTED",
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
            "ORDER4_REPRODUCED",
            float(result["order4_reproduction_relative_error"])
            <= ORDER4_REPRODUCTION_LIMIT,
            str(result["order4_reproduction_relative_error"]),
        ),
        validation_gate(
            "LOCAL_NUMERIC_CONTROLS_PASS",
            (
                float(
                    result[
                        "maximum_audited_coefficient_relative_change"
                    ]
                )
                <= COEFFICIENT_CONVERGENCE_LIMIT
                and float(result["maximum_root_equation_residual"])
                <= ROOT_RESIDUAL_LIMIT
                and float(
                    result[
                        "maximum_root_refinement_chordal_distance"
                    ]
                )
                <= ROOT_REFINEMENT_DISTANCE_LIMIT
            ),
            "coefficient and root controls pass",
        ),
        validation_gate(
            "CONVERGENCE_DECISION_EXPLICIT",
            (
                bool(result["fixed_angle_energy_converged"])
                == bool(
                    result["claim_boundary"][
                        "valid_for_converged_fixed_angle_energy_integral"
                    ]
                )
            ),
            (
                "fixed-angle convergence="
                f"{result['fixed_angle_energy_converged']}"
            ),
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
            "VALIDATED_HIGH_ORDER_ENERGY_CONVERGENCE_DIAGNOSIS"
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
