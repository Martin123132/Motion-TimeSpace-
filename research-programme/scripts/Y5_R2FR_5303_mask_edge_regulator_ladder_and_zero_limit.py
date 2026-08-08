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
SOURCE = FUNCTIONAL_RG / "5303"

SCRIPT_5302 = SCRIPTS / (
    "Y5_R2FR_5302_mask_edge_integrability_and_limit_order_audit.py"
)
RESULT_5302 = FUNCTIONAL_RG / "5302" / (
    "mask_edge_integrability_result.json"
)
VALIDATION_5302 = FUNCTIONAL_RG / "5302" / (
    "mask_edge_integrability_validation.csv"
)
DRY_RUN = SOURCE / "mask_edge_regulator_ladder_dry_run.json"
MAP_AUDIT = SOURCE / "synthetic_regulator_component_map_audit.csv"
PANELS = SOURCE / "regulator_ladder_edge_panel_integrals.csv"
INTEGRALS = SOURCE / "regulator_ladder_edge_integrals.csv"
LIMITS = SOURCE / "regulator_zero_limit_estimates.csv"
RESULT = SOURCE / "mask_edge_regulator_zero_limit_result.json"
VALIDATION = SOURCE / "mask_edge_regulator_zero_limit_validation.csv"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5303_VALIDATION.csv"
STATUS = SOURCE / "status.json"
DOCUMENT = POST / (
    "5303-Y5-R2FR-mask-edge-regulator-ladder-and-zero-limit.md"
)

CHECKPOINT = 5303
PARENT_CHECKPOINT = 5302
MARKER = "MTS_5303_MASK_EDGE_REGULATOR_LADDER_AND_ZERO_LIMIT"
REVISION = "mask-edge-regulator-ladder-zero-limit-v1"
REGULATORS = (
    ("E040", 0.04),
    ("E020", 0.02),
    ("E010", 0.01),
    ("E005", 0.005),
    ("E0025", 0.0025),
)
NATIVE_REGULATORS = ("E040", "E020")
QUADRATURE_ORDERS = (4, 8)
QUADRATURE_CHANGE_LIMIT = 1.0e-3
MAP_REPRODUCTION_LIMIT = 1.0e-12
RICHARDSON_LIMIT_CHANGE_LIMIT = 1.0e-2
MODEL_INTERCEPT_CHANGE_LIMIT = 1.0e-2
MAP_AUDIT_OFFSETS = (
    1.0e-7,
    1.0e-4,
    1.5e-3,
    2.0e-3,
    2.0e-2,
)
CLAIM_FIELDS = (
    "valid_for_full_angular_convergence",
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


M5302 = load_module("mts_5302_for_5303", SCRIPT_5302)
M5301 = M5302.M5301
M5280 = M5302.M5280
M5283 = M5302.M5283
np = M5302.np
mp = M5302.mp


def set_below_normal_priority() -> None:
    if os.name != "nt":
        return
    process_handle = ctypes.windll.kernel32.GetCurrentProcess()
    ctypes.windll.kernel32.SetPriorityClass(process_handle, 0x00004000)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
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
    with temporary.open("w", newline="", encoding="utf-8") as handle:
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


def relative_complex_change(first: complex, second: complex) -> float:
    return abs(second - first) / max(abs(second), abs(first), 1.0e-300)


def panel_offsets() -> tuple[float, ...]:
    values = set(float(value) for value in M5302.EDGE_PANEL_OFFSETS)
    for index in range(101):
        values.add(1.2e-3 + index * 1.0e-5)
    for index in range(71):
        values.add(1.58e-3 + index * 2.0e-6)
    values.add(0.0)
    values.add(M5302.EDGE_WINDOW)
    return tuple(
        value
        for value in sorted(values)
        if 0.0 <= value <= M5302.EDGE_WINDOW
    )


def synthetic_context() -> dict[str, Any]:
    context = M5280.source_context()
    inventories = dict(context["inventories"])
    component_map = inventories["E020"]["components"]
    for epsilon_id, epsilon in REGULATORS:
        target = complex(-9.0, epsilon)
        inventories[epsilon_id] = {
            "target": target,
            "high_precision_target": M5280.M5275.target_as_mp(target),
            "components": component_map,
        }
    context["inventories"] = inventories
    return context


def component_value(
    base_context: dict[str, Any],
    epsilon_id: str,
    absolute_soft_cosine: float,
) -> tuple[complex, bool]:
    context = M5302.local_context(
        base_context,
        absolute_soft_cosine,
        M5302.EDGE_SOFT_SIGN,
        M5302.EDGE_DECAY_SIGN,
    )
    event = dict(context["source_event"])
    event["soft_energy"] = M5302.EDGE_ENERGY
    target = context["inventories"][epsilon_id]["target"]
    rationals = M5280.M5274.M5231.root_rationals(event, target)
    evaluation = M5280.evaluate_component(
        event,
        epsilon_id,
        M5302.EDGE_COMPONENT,
        context,
        rationals=rationals,
        convergence_audit=False,
    )
    return complex(evaluation["residue"]), bool(evaluation["mask_active"])


def edge_evaluator(
    base_context: dict[str, Any],
    multiplier: float,
) -> Any:
    cache: dict[tuple[str, float], tuple[complex, bool]] = {}

    def evaluate(
        epsilon_id: str,
        absolute_soft_cosine: float,
    ) -> tuple[complex, bool]:
        key = (epsilon_id, float(absolute_soft_cosine))
        if key not in cache:
            value, active = component_value(
                base_context,
                epsilon_id,
                absolute_soft_cosine,
            )
            cache[key] = (multiplier * value, active)
        return cache[key]

    return evaluate


def native_component_value(
    base_context: dict[str, Any],
    epsilon_id: str,
    absolute_soft_cosine: float,
) -> complex:
    native = M5280.source_context()
    context = M5302.local_context(
        native,
        absolute_soft_cosine,
        M5302.EDGE_SOFT_SIGN,
        M5302.EDGE_DECAY_SIGN,
    )
    event = dict(context["source_event"])
    event["soft_energy"] = M5302.EDGE_ENERGY
    target = context["inventories"][epsilon_id]["target"]
    rationals = M5280.M5274.M5231.root_rationals(event, target)
    return complex(
        M5280.evaluate_component(
            event,
            epsilon_id,
            M5302.EDGE_COMPONENT,
            context,
            rationals=rationals,
            convergence_audit=True,
        )["residue"]
    )


def map_audit_rows(
    context: dict[str, Any],
    boundary: float,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for offset in MAP_AUDIT_OFFSETS:
        coordinate = boundary + offset
        for epsilon_id in NATIVE_REGULATORS:
            native = native_component_value(
                context,
                epsilon_id,
                coordinate,
            )
            synthetic = component_value(
                context,
                epsilon_id,
                coordinate,
            )[0]
            change = relative_complex_change(native, synthetic)
            rows.append(
                {
                    "epsilon_id": epsilon_id,
                    "offset_from_boundary": offset,
                    "absolute_soft_cosine": coordinate,
                    **complex_fields("native_component", native),
                    **complex_fields("synthetic_component", synthetic),
                    "relative_change": change,
                    "valid_for_synthetic_regulator_map": (
                        change <= MAP_REPRODUCTION_LIMIT
                    ),
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
    return rows


def quadrature_rows(
    boundary: float,
    edge: Any,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    offsets = panel_offsets()
    panel_rows: list[dict[str, Any]] = []
    integral_rows: list[dict[str, Any]] = []
    totals: dict[tuple[int, str], complex] = {}
    for order in QUADRATURE_ORDERS:
        nodes, weights = np.polynomial.legendre.leggauss(order)
        for epsilon_id, epsilon in REGULATORS:
            total = 0.0j
            for panel_index, (left_offset, right_offset) in enumerate(
                zip(offsets[:-1], offsets[1:]),
                start=1,
            ):
                left = boundary + left_offset
                right = boundary + right_offset
                half_width = 0.5 * (right - left)
                midpoint = 0.5 * (right + left)
                panel_value = sum(
                    (
                        half_width
                        * float(weight)
                        * edge(
                            epsilon_id,
                            midpoint + half_width * float(node),
                        )[0]
                        for node, weight in zip(nodes, weights)
                    ),
                    0.0j,
                )
                total += panel_value
                panel_rows.append(
                    {
                        "epsilon_id": epsilon_id,
                        "epsilon": epsilon,
                        "quadrature_order": order,
                        "panel_index": panel_index,
                        "left_offset_from_boundary": left_offset,
                        "right_offset_from_boundary": right_offset,
                        "panel_width": right - left,
                        **complex_fields("panel_integral", panel_value),
                        **{field: False for field in CLAIM_FIELDS},
                    }
                )
            totals[(order, epsilon_id)] = total
    for epsilon_id, epsilon in REGULATORS:
        change = relative_complex_change(
            totals[(min(QUADRATURE_ORDERS), epsilon_id)],
            totals[(max(QUADRATURE_ORDERS), epsilon_id)],
        )
        for order in QUADRATURE_ORDERS:
            integral_rows.append(
                {
                    "epsilon_id": epsilon_id,
                    "epsilon": epsilon,
                    "quadrature_order": order,
                    **complex_fields(
                        "edge_integral",
                        totals[(order, epsilon_id)],
                    ),
                    "order4_order8_relative_change": change,
                    "passes_edge_quadrature_gate": (
                        change <= QUADRATURE_CHANGE_LIMIT
                    ),
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
    return panel_rows, integral_rows


def polynomial_intercept(
    points: list[tuple[float, complex]],
    degree: int,
) -> tuple[complex, float]:
    x_values = np.asarray([point[0] for point in points], dtype=float)
    y_values = np.asarray([point[1] for point in points], dtype=complex)
    matrix = np.column_stack(
        [x_values**power for power in range(degree + 1)]
    )
    coefficients, *_ = np.linalg.lstsq(matrix, y_values, rcond=None)
    fitted = matrix @ coefficients
    residual = float(
        np.linalg.norm(fitted - y_values)
        / max(np.linalg.norm(y_values), 1.0e-300)
    )
    return complex(coefficients[0]), residual


def limit_rows(
    integral_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, complex]]:
    values = {
        row["epsilon_id"]: complex(
            float(row["edge_integral_real"]),
            float(row["edge_integral_imaginary"]),
        )
        for row in integral_rows
        if int(row["quadrature_order"]) == max(QUADRATURE_ORDERS)
    }
    epsilon = dict(REGULATORS)
    rows: list[dict[str, Any]] = []
    estimates: dict[str, complex] = {}
    for first_id, second_id in zip(
        [row[0] for row in REGULATORS[:-1]],
        [row[0] for row in REGULATORS[1:]],
    ):
        estimate = 2.0 * values[second_id] - values[first_id]
        estimate_id = f"RICHARDSON_{first_id}_{second_id}"
        estimates[estimate_id] = estimate
        rows.append(
            {
                "estimate_id": estimate_id,
                "estimate_family": "FIRST_ORDER_RICHARDSON",
                "regulator_ids": f"{first_id}|{second_id}",
                "point_count": 2,
                "polynomial_degree": 1,
                **complex_fields("zero_limit_estimate", estimate),
                "fit_relative_residual": 0.0,
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    fit_definitions = (
        ("LINEAR_ALL5", [row[0] for row in REGULATORS], 1),
        ("QUADRATIC_ALL5", [row[0] for row in REGULATORS], 2),
        ("LINEAR_SMALL4", [row[0] for row in REGULATORS[-4:]], 1),
        ("QUADRATIC_SMALL4", [row[0] for row in REGULATORS[-4:]], 2),
        ("LINEAR_SMALL3", [row[0] for row in REGULATORS[-3:]], 1),
    )
    for estimate_id, ids, degree in fit_definitions:
        estimate, residual = polynomial_intercept(
            [(epsilon[item], values[item]) for item in ids],
            degree,
        )
        estimates[estimate_id] = estimate
        rows.append(
            {
                "estimate_id": estimate_id,
                "estimate_family": "COMPLEX_POLYNOMIAL_INTERCEPT",
                "regulator_ids": "|".join(ids),
                "point_count": len(ids),
                "polynomial_degree": degree,
                **complex_fields("zero_limit_estimate", estimate),
                "fit_relative_residual": residual,
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    previous = estimates["RICHARDSON_E010_E005"]
    latest = estimates["RICHARDSON_E005_E0025"]
    model_first = estimates["LINEAR_SMALL3"]
    model_second = estimates["QUADRATIC_SMALL4"]
    for row in rows:
        row["last_two_richardson_relative_change"] = (
            relative_complex_change(previous, latest)
        )
        row["small_regulator_model_intercept_relative_change"] = (
            relative_complex_change(model_first, model_second)
        )
        row["valid_for_regulator_zero_edge_slice"] = (
            row["last_two_richardson_relative_change"]
            <= RICHARDSON_LIMIT_CHANGE_LIMIT
            and row["small_regulator_model_intercept_relative_change"]
            <= MODEL_INTERCEPT_CHANGE_LIMIT
        )
    return rows, estimates


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5302,
        RESULT_5302,
        VALIDATION_5302,
    )
    return [
        {"path": str(path), "sha256": digest(path)} for path in paths
    ]


def dry_run() -> dict[str, Any]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    parent = read_json(RESULT_5302)
    offsets = panel_offsets()
    checks = {
        "parent_5302_accepted": bool(parent["acceptance_passed"]),
        "parent_5302_validated": all(
            parse_bool(row["passed"]) for row in read_csv(VALIDATION_5302)
        ),
        "parent_requests_regulator_ladder": (
            parent["decision"]
            == (
                "MASK_EDGE_DERIVED_AND_FINITE_REGULATORS_CONVERGED__"
                "BUILD_REGULATOR_LADDER_BEFORE_FULL_CUBATURE"
            )
        ),
        "five_regulator_values_descend_by_two": all(
            math.isclose(
                REGULATORS[index][1],
                2.0 * REGULATORS[index + 1][1],
            )
            for index in range(len(REGULATORS) - 1)
        ),
        "edge_panels_cover_parent_window": (
            offsets[0] == 0.0
            and math.isclose(offsets[-1], M5302.EDGE_WINDOW)
        ),
        "edge_peak_has_ultrafine_panels": (
            min(
                right - left
                for left, right in zip(offsets[:-1], offsets[1:])
                if 1.58e-3 <= left and right <= 1.72e-3
            )
            <= 2.01e-6
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
        "mode": "dry-run",
        "checks": checks,
        "acceptance_passed": accepted,
        "regulator_count": len(REGULATORS),
        "edge_panel_count": len(offsets) - 1,
        "decision": (
            "DRY_RUN_ACCEPTED__RUN_MASK_EDGE_REGULATOR_LADDER"
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
    mp.mp.dps = M5280.MP_DECIMAL_DIGITS
    M5301.configure_reused_pipeline()
    started = time.perf_counter()
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5303 dry run did not pass")
    parent = read_json(RESULT_5302)
    boundary = float(parent["absolute_soft_cosine_boundary"])
    context = synthetic_context()
    multiplier = M5301.M5300.M5292.physical_multiplier()
    edge = edge_evaluator(context, multiplier)
    map_rows = map_audit_rows(context, boundary)
    panel_rows, integral_rows = quadrature_rows(boundary, edge)
    limits, estimates = limit_rows(integral_rows)
    write_csv(MAP_AUDIT, map_rows)
    write_csv(PANELS, panel_rows)
    write_csv(INTEGRALS, integral_rows)
    write_csv(LIMITS, limits)
    maximum_map_change = max(
        float(row["relative_change"]) for row in map_rows
    )
    maximum_quadrature_change = max(
        float(row["order4_order8_relative_change"])
        for row in integral_rows
    )
    richardson_change = float(
        limits[0]["last_two_richardson_relative_change"]
    )
    model_change = float(
        limits[0][
            "small_regulator_model_intercept_relative_change"
        ]
    )
    limit_stable = (
        richardson_change <= RICHARDSON_LIMIT_CHANGE_LIMIT
        and model_change <= MODEL_INTERCEPT_CHANGE_LIMIT
    )
    final_estimate = estimates["RICHARDSON_E005_E0025"]
    formal_end = M5283.formal_inventory_digest()
    checks = {
        "native_component_map_reproduced": (
            maximum_map_change <= MAP_REPRODUCTION_LIMIT
        ),
        "all_five_regulators_integrated": (
            len(integral_rows)
            == len(REGULATORS) * len(QUADRATURE_ORDERS)
        ),
        "all_regulator_integrals_energy_finite": all(
            math.isfinite(float(row[field]))
            for row in integral_rows
            for field in (
                "edge_integral_real",
                "edge_integral_imaginary",
                "edge_integral_magnitude",
            )
        ),
        "all_regulator_integrals_quadrature_converged": (
            maximum_quadrature_change <= QUADRATURE_CHANGE_LIMIT
        ),
        "regulator_zero_edge_slice_stable": limit_stable,
        "integration_precision_initialized": (
            mp.mp.dps >= M5280.MP_DECIMAL_DIGITS
        ),
        "formalization_workbench_unchanged": (
            formal_end == str(parent["formalization_workbench_end_digest"])
        ),
        "claims_locked_false": True,
    }
    pipeline_accepted = all(
        value
        for key, value in checks.items()
        if key != "regulator_zero_edge_slice_stable"
    )
    if not pipeline_accepted:
        decision = "REGULATOR_LADDER_PIPELINE_REQUIRES_REPAIR"
    elif not limit_stable:
        decision = (
            "REGULATOR_LADDER_CONVERGED_BUT_ZERO_LIMIT_UNSTABLE__"
            "EXTEND_OR_DERIVE_DISTRIBUTIONAL_LIMIT"
        )
    else:
        decision = (
            "REGULATOR_ZERO_EDGE_SLICE_RESOLVED__"
            "BUILD_BOUNDARY_ALIGNED_ENERGY_ANGLE_CUBATURE"
        )
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "mask-edge-regulator-ladder-and-zero-limit",
        "checks": checks,
        "acceptance_passed": pipeline_accepted,
        "decision": decision,
        "regulator_count": len(REGULATORS),
        "edge_panel_count": int(dry["edge_panel_count"]),
        "maximum_native_map_reproduction_relative_change": (
            maximum_map_change
        ),
        "maximum_regulator_quadrature_relative_change": (
            maximum_quadrature_change
        ),
        "last_two_richardson_relative_change": richardson_change,
        "small_regulator_model_intercept_relative_change": model_change,
        **complex_fields(
            "regulator_zero_edge_slice_estimate",
            final_estimate,
        ),
        "integration_mp_decimal_digits": mp.mp.dps,
        "formalization_workbench_reference_digest": str(
            parent["formalization_workbench_end_digest"]
        ),
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0
            if formal_end == str(parent["formalization_workbench_end_digest"])
            else -1
        ),
        "claim_boundary": {
            "valid_for_synthetic_regulator_component_map": (
                pipeline_accepted
            ),
            "valid_for_five_regulator_edge_integrals": (
                pipeline_accepted
            ),
            "valid_for_regulator_zero_edge_slice": (
                pipeline_accepted and limit_stable
            ),
            **{field: False for field in CLAIM_FIELDS},
            "reason": (
                "The limit concerns one exact hard-mask edge at one "
                "soft-energy/decay-angle slice. It does not by itself "
                "establish the joint phase-space coefficient."
            ),
        },
        "resource_contract": {
            "maximum_task_python_processes": 1,
            "worker_math_threads": 1,
            "windows_priority": "BelowNormal",
            "sustained_redline_forbidden": True,
        },
        "source_files": source_rows(),
        "runtime_seconds": time.perf_counter() - started,
    }
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "COMPLETE" if pipeline_accepted else "FAILED",
            "decision": decision,
            "regulator_zero_edge_slice_stable": limit_stable,
        },
    )
    return result


def validation_gate(
    gate_id: str,
    passed: bool,
    detail: str,
) -> dict[str, Any]:
    return {"gate_id": gate_id, "passed": passed, "detail": detail}


def render_document(result: dict[str, Any], passed: bool) -> None:
    checks = "\n".join(
        f"- `{key}`: **{'PASS' if value else 'FAIL'}**"
        for key, value in sorted(result["checks"].items())
    )
    text = f"""# 5303 — Mask-edge regulator ladder and zero limit

## Result

The E020 component map reproduces the native E040 and E020 edge
integrands with maximum relative change
`{result['maximum_native_map_reproduction_relative_change']:.12g}`.
That algebraic map therefore supports the additional targets
`-9+0.01i`, `-9+0.005i`, and `-9+0.0025i` without inventing new component
labels.

All five finite regulators were integrated across the exact 5302 edge
using `{result['edge_panel_count']}` boundary-aligned panels. The maximum
order-4/order-8 change is
`{result['maximum_regulator_quadrature_relative_change']:.12g}`.

The last two first-order Richardson estimates change by
`{result['last_two_richardson_relative_change']:.12g}`. The small-regulator
linear/quadratic intercepts change by
`{result['small_regulator_model_intercept_relative_change']:.12g}`.

The final edge-slice estimate is

`{result['regulator_zero_edge_slice_estimate_real']:.12g} +
{result['regulator_zero_edge_slice_estimate_imaginary']:.12g} i`.

Decision: **{result['decision']}**.

## Acceptance gates

{checks}

Validation: **{'PASS' if passed else 'FAIL'}**.

## Claim boundary

This is a regulator-zero result only for one exact mask edge at one
soft-energy and decay-angle slice. It does not establish full angular
convergence, the joint phase-space coefficient, a UV coefficient, local
GR, or the full MTS theory.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    result = read_json(RESULT)
    map_rows = read_csv(MAP_AUDIT)
    panels = read_csv(PANELS)
    integrals = read_csv(INTEGRALS)
    limits = read_csv(LIMITS)
    gates = [
        validation_gate(
            "result_pipeline_accepted",
            bool(result["acceptance_passed"]),
            str(result["decision"]),
        ),
        validation_gate(
            "native_component_map_reproduced",
            len(map_rows)
            == len(MAP_AUDIT_OFFSETS) * len(NATIVE_REGULATORS)
            and all(
                parse_bool(row["valid_for_synthetic_regulator_map"])
                for row in map_rows
            ),
            f"rows={len(map_rows)}",
        ),
        validation_gate(
            "all_panel_rows_complete",
            len(panels)
            == (
                int(result["edge_panel_count"])
                * len(REGULATORS)
                * len(QUADRATURE_ORDERS)
            ),
            f"rows={len(panels)}",
        ),
        validation_gate(
            "all_five_regulator_integrals_converged",
            len(integrals)
            == len(REGULATORS) * len(QUADRATURE_ORDERS)
            and all(
                parse_bool(row["passes_edge_quadrature_gate"])
                for row in integrals
            ),
            f"rows={len(integrals)}",
        ),
        validation_gate(
            "limit_estimates_complete",
            len(limits) == 9,
            f"rows={len(limits)}",
        ),
        validation_gate(
            "limit_status_recorded_without_overclaim",
            bool(
                result["claim_boundary"][
                    "valid_for_regulator_zero_edge_slice"
                ]
            )
            == bool(result["checks"]["regulator_zero_edge_slice_stable"]),
            str(
                result["claim_boundary"][
                    "valid_for_regulator_zero_edge_slice"
                ]
            ),
        ),
        validation_gate(
            "integration_precision_initialized",
            int(result["integration_mp_decimal_digits"])
            >= int(M5280.MP_DECIMAL_DIGITS),
            (
                f"digits={result['integration_mp_decimal_digits']}; "
                f"required={M5280.MP_DECIMAL_DIGITS}"
            ),
        ),
        validation_gate(
            "formal_workbench_unchanged",
            M5283.formal_inventory_digest()
            == str(result["formalization_workbench_end_digest"]),
            str(result["formalization_workbench_end_digest"]),
        ),
        validation_gate(
            "full_claims_locked_false",
            all(
                not bool(result["claim_boundary"][field])
                for field in CLAIM_FIELDS
            ),
            "no full angular, phase-space, UV, local-GR, or MTS claim",
        ),
    ]
    passed = all(bool(row["passed"]) for row in gates)
    write_csv(VALIDATION, gates)
    write_csv(RESIDUAL_VALIDATION, gates)
    render_document(result, passed)
    return {
        "checkpoint": CHECKPOINT,
        "mode": "validation",
        "acceptance_passed": passed,
        "decision": (
            "VALIDATED_MASK_EDGE_REGULATOR_LADDER"
            if passed
            else "MASK_EDGE_REGULATOR_LADDER_VALIDATION_FAILED"
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
    arguments = parse_args()
    if arguments.mode == "dry-run":
        result = dry_run()
    elif arguments.mode == "run":
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
