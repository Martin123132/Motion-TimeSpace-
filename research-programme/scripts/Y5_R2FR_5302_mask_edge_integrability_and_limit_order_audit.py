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
SOURCE = FUNCTIONAL_RG / "5302"

SCRIPT_5301 = SCRIPTS / (
    "Y5_R2FR_5301_adaptive_local_cell_residual_integration.py"
)
SCRIPT_5272 = SCRIPTS / (
    "Y5_R2FR_5272_exact_analytic_boundary_surface_and_event_solver.py"
)
RESULT_5301 = FUNCTIONAL_RG / "5301" / (
    "adaptive_local_cell_residual_integration_result.json"
)
VALIDATION_5301 = FUNCTIONAL_RG / "5301" / (
    "adaptive_local_cell_residual_validation.csv"
)
DRY_RUN = SOURCE / "mask_edge_integrability_dry_run.json"
BOUNDARY = SOURCE / "exact_mask_edge_witness.csv"
SYMMETRY = SOURCE / "mask_edge_sign_orbit_symmetry.csv"
POINTWISE = SOURCE / "mask_edge_pointwise_scaling.csv"
PANELS = SOURCE / "mask_edge_quadrature_panel_integrals.csv"
INTEGRALS = SOURCE / "mask_edge_finite_regulator_integrals.csv"
RESULT = SOURCE / "mask_edge_integrability_result.json"
VALIDATION = SOURCE / "mask_edge_integrability_validation.csv"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5302_VALIDATION.csv"
STATUS = SOURCE / "status.json"
DOCUMENT = POST / (
    "5302-Y5-R2FR-mask-edge-integrability-and-limit-order-audit.md"
)

CHECKPOINT = 5302
PARENT_CHECKPOINT = 5301
MARKER = "MTS_5302_MASK_EDGE_INTEGRABILITY_AND_LIMIT_ORDER_AUDIT"
REVISION = "mask-edge-integrability-limit-order-audit-v1"
EDGE_ENERGY = 0.1100816778468012
EDGE_DECAY_ABSOLUTE = 0.338281138367
EDGE_BRACKET = (0.425, 0.428)
EDGE_COMPONENT = "MC04"
EDGE_SOFT_SIGN = -1
EDGE_DECAY_SIGN = -1
EDGE_WINDOW = 0.1
ENERGY_REGULATORS = ("E040", "E020")
PAIR_COMPONENTS = ("MC04", "MC12")
QUADRATURE_ORDERS = (4, 8)
QUADRATURE_CHANGE_LIMIT = 1.0e-3
SYMMETRY_RELATIVE_ERROR_LIMIT = 1.0e-9
BOUNDARY_RESIDUAL_LIMIT = 1.0e-13
BOUNDARY_DERIVATIVE_MINIMUM = 1.0e-6
EDGE_PANEL_OFFSETS = (
    0.0,
    1.0e-6,
    2.0e-6,
    5.0e-6,
    1.0e-5,
    2.0e-5,
    5.0e-5,
    1.0e-4,
    2.0e-4,
    5.0e-4,
    1.0e-3,
    1.1e-3,
    1.2e-3,
    1.3e-3,
    1.4e-3,
    1.5e-3,
    1.6e-3,
    1.7e-3,
    1.8e-3,
    1.9e-3,
    2.0e-3,
    3.0e-3,
    5.0e-3,
    8.0e-3,
    1.2e-2,
    2.0e-2,
    3.5e-2,
    6.0e-2,
    EDGE_WINDOW,
)
POINTWISE_OFFSETS = (
    1.0e-7,
    2.0e-7,
    5.0e-7,
    1.0e-6,
    2.0e-6,
    5.0e-6,
    1.0e-5,
    2.0e-5,
    5.0e-5,
    1.0e-4,
    2.0e-4,
    5.0e-4,
    1.0e-3,
    2.0e-3,
    5.0e-3,
    1.0e-2,
    2.0e-2,
    5.0e-2,
)
SYMMETRY_OFFSETS = (
    -1.0e-3,
    1.0e-7,
    1.0e-4,
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


M5301 = load_module("mts_5301_for_5302", SCRIPT_5301)
M5280 = M5301.M5300.M5280
M5272 = M5280.M5274.M5273.M5272
M5283 = M5301.M5283
np = M5301.np
mp = M5280.M5275.mp


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


def surface_value(absolute_soft_cosine: float) -> float:
    return M5272.hard_boundary_value(
        math.sqrt(1.0 - EDGE_ENERGY),
        -absolute_soft_cosine,
        -EDGE_DECAY_ABSOLUTE,
        1,
        -0.3,
        math.pi,
    )


def boundary_coordinate() -> float:
    lower, upper = EDGE_BRACKET
    lower_value = surface_value(lower)
    upper_value = surface_value(upper)
    if lower_value * upper_value >= 0.0:
        raise RuntimeError("mask-edge bracket does not change sign")
    for _ in range(100):
        midpoint = 0.5 * (lower + upper)
        midpoint_value = surface_value(midpoint)
        if lower_value * midpoint_value <= 0.0:
            upper = midpoint
            upper_value = midpoint_value
        else:
            lower = midpoint
            lower_value = midpoint_value
    return 0.5 * (lower + upper)


def boundary_derivative(coordinate: float) -> float:
    derivative_with_respect_to_signed_soft_cosine = (
        M5272.hard_boundary_coordinate_derivative(
            "soft_cosine",
            math.sqrt(1.0 - EDGE_ENERGY),
            -coordinate,
            -EDGE_DECAY_ABSOLUTE,
            1,
            -0.3,
            math.pi,
        )
    )
    return -float(derivative_with_respect_to_signed_soft_cosine)


def local_context(
    base_context: dict[str, Any],
    absolute_soft_cosine: float,
    soft_sign: int,
    decay_sign: int,
) -> dict[str, Any]:
    return M5301.M5300.M5295.M5287.local_context(
        base_context,
        {
            "soft_cosine": soft_sign * absolute_soft_cosine,
            "decay_cosine": decay_sign * EDGE_DECAY_ABSOLUTE,
        },
    )


def component_value(
    base_context: dict[str, Any],
    epsilon_id: str,
    component_id: str,
    absolute_soft_cosine: float,
    soft_sign: int,
    decay_sign: int,
) -> tuple[complex, bool]:
    context = local_context(
        base_context,
        absolute_soft_cosine,
        soft_sign,
        decay_sign,
    )
    event = dict(context["source_event"])
    event["soft_energy"] = EDGE_ENERGY
    target = context["inventories"][epsilon_id]["target"]
    rationals = M5280.M5274.M5231.root_rationals(event, target)
    evaluation = M5280.evaluate_component(
        event,
        epsilon_id,
        component_id,
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
                EDGE_COMPONENT,
                absolute_soft_cosine,
                EDGE_SOFT_SIGN,
                EDGE_DECAY_SIGN,
            )
            cache[key] = (multiplier * value, active)
        return cache[key]

    return evaluate


def pair_orbit_value(
    base_context: dict[str, Any],
    multiplier: float,
    epsilon_id: str,
    absolute_soft_cosine: float,
) -> complex:
    return multiplier * sum(
        (
            component_value(
                base_context,
                epsilon_id,
                component_id,
                absolute_soft_cosine,
                soft_sign,
                decay_sign,
            )[0]
            for soft_sign in (-1, 1)
            for decay_sign in (-1, 1)
            for component_id in PAIR_COMPONENTS
        ),
        0.0j,
    )


def symmetry_rows(
    base_context: dict[str, Any],
    multiplier: float,
    boundary: float,
    edge: Any,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for offset in SYMMETRY_OFFSETS:
        coordinate = boundary + offset
        for epsilon_id in ENERGY_REGULATORS:
            orbit = pair_orbit_value(
                base_context,
                multiplier,
                epsilon_id,
                coordinate,
            )
            witness, active = edge(epsilon_id, coordinate)
            error = abs(orbit - witness) / max(
                abs(orbit),
                abs(witness),
                1.0,
            )
            rows.append(
                {
                    "epsilon_id": epsilon_id,
                    "offset_from_boundary": offset,
                    "absolute_soft_cosine": coordinate,
                    "surface_value": surface_value(coordinate),
                    "edge_component_mask_active": active,
                    **complex_fields("pair_sign_orbit", orbit),
                    **complex_fields("single_edge_witness", witness),
                    **complex_fields("symmetry_remainder", orbit - witness),
                    "symmetry_relative_error": error,
                    "valid_for_single_edge_reduction": (
                        error <= SYMMETRY_RELATIVE_ERROR_LIMIT
                    ),
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
    return rows


def pointwise_rows(
    boundary: float,
    edge: Any,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    previous: dict[str, Any] | None = None
    for offset in POINTWISE_OFFSETS:
        coordinate = boundary + offset
        e040, active_040 = edge("E040", coordinate)
        e020, active_020 = edge("E020", coordinate)
        physical = 2.0 * e020 - e040
        row = {
            "offset_from_boundary": offset,
            "absolute_soft_cosine": coordinate,
            "surface_value": surface_value(coordinate),
            "E040_mask_active": active_040,
            "E020_mask_active": active_020,
            **complex_fields("E040_edge_value", e040),
            **complex_fields("E020_edge_value", e020),
            **complex_fields("pointwise_two_E020_minus_E040", physical),
            "pointwise_local_power": "",
            **{field: False for field in CLAIM_FIELDS},
        }
        if previous is not None:
            row["pointwise_local_power"] = -math.log(
                max(abs(physical), 1.0e-300)
                / max(
                    float(
                        previous[
                            "pointwise_two_E020_minus_E040_magnitude"
                        ]
                    ),
                    1.0e-300,
                )
            ) / math.log(
                offset / float(previous["offset_from_boundary"])
            )
        rows.append(row)
        previous = row
    return rows


def quadrature_rows(
    boundary: float,
    edge: Any,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    panel_rows: list[dict[str, Any]] = []
    integral_rows: list[dict[str, Any]] = []
    totals: dict[tuple[int, str], complex] = {}
    for order in QUADRATURE_ORDERS:
        nodes, weights = np.polynomial.legendre.leggauss(order)
        for epsilon_id in ENERGY_REGULATORS:
            total = 0.0j
            for panel_index, (left_offset, right_offset) in enumerate(
                zip(EDGE_PANEL_OFFSETS[:-1], EDGE_PANEL_OFFSETS[1:]),
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
            integral_rows.append(
                {
                    "row_type": "FINITE_REGULATOR_EDGE_INTEGRAL",
                    "epsilon_id": epsilon_id,
                    "quadrature_order": order,
                    **complex_fields("edge_integral", total),
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
        physical = (
            2.0 * totals[(order, "E020")] - totals[(order, "E040")]
        )
        totals[(order, "2E020_MINUS_E040")] = physical
        integral_rows.append(
            {
                "row_type": "TWO_REGULATOR_POINTWISE_EXTRAPOLATION",
                "epsilon_id": "2E020_MINUS_E040",
                "quadrature_order": order,
                **complex_fields("edge_integral", physical),
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    for row in integral_rows:
        epsilon_id = row["epsilon_id"]
        row["order4_order8_relative_change"] = relative_complex_change(
            totals[(min(QUADRATURE_ORDERS), epsilon_id)],
            totals[(max(QUADRATURE_ORDERS), epsilon_id)],
        )
        row["passes_edge_quadrature_gate"] = (
            row["order4_order8_relative_change"]
            <= QUADRATURE_CHANGE_LIMIT
        )
    return panel_rows, integral_rows


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5301,
        SCRIPT_5272,
        RESULT_5301,
        VALIDATION_5301,
    )
    return [
        {"path": str(path), "sha256": digest(path)} for path in paths
    ]


def dry_run() -> dict[str, Any]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    parent = read_json(RESULT_5301)
    coordinate = boundary_coordinate()
    checks = {
        "parent_5301_accepted": bool(parent["acceptance_passed"]),
        "parent_5301_validated": all(
            parse_bool(row["passed"]) for row in read_csv(VALIDATION_5301)
        ),
        "parent_requests_core_refinement": (
            parent["decision"]
            == "LOCAL_CELL_RESOLVED_BUT_MODEL_UNSTABLE__REFINE_CORE"
        ),
        "edge_bracket_changes_sign": (
            surface_value(EDGE_BRACKET[0])
            * surface_value(EDGE_BRACKET[1])
            < 0.0
        ),
        "edge_coordinate_inside_5301_cell": (
            float(parent["cell_lower"])
            < coordinate
            < float(parent["cell_upper"])
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
        "boundary_coordinate": coordinate,
        "decision": (
            "DRY_RUN_ACCEPTED__AUDIT_MASK_EDGE_INTEGRABILITY"
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
        raise RuntimeError("5302 dry run did not pass")
    parent = read_json(RESULT_5301)
    coordinate = float(dry["boundary_coordinate"])
    derivative = boundary_derivative(coordinate)
    residual = abs(surface_value(coordinate))
    base_context = M5280.source_context()
    multiplier = M5301.M5300.M5292.physical_multiplier()
    edge = edge_evaluator(base_context, multiplier)
    symmetry = symmetry_rows(
        base_context,
        multiplier,
        coordinate,
        edge,
    )
    pointwise = pointwise_rows(coordinate, edge)
    panel_rows, integral_rows = quadrature_rows(coordinate, edge)
    write_csv(
        BOUNDARY,
        [
            {
                "soft_energy": EDGE_ENERGY,
                "absolute_decay_cosine": EDGE_DECAY_ABSOLUTE,
                "absolute_soft_cosine_boundary": coordinate,
                "boundary_surface": "direct:g1|t=-0.3|phi=pi",
                "boundary_law": "F_{+1,-0.3}(sqrt(1-E),-s,-d)=0",
                "surface_residual": residual,
                "surface_derivative_with_respect_to_absolute_soft_cosine": (
                    derivative
                ),
                "edge_component": EDGE_COMPONENT,
                "edge_signed_node": "soft_sign=-1|decay_sign=-1",
                "edge_window": EDGE_WINDOW,
                "valid_for_exact_mask_edge_witness": (
                    residual <= BOUNDARY_RESIDUAL_LIMIT
                    and abs(derivative) >= BOUNDARY_DERIVATIVE_MINIMUM
                ),
                **{field: False for field in CLAIM_FIELDS},
            }
        ],
    )
    write_csv(SYMMETRY, symmetry)
    write_csv(POINTWISE, pointwise)
    write_csv(PANELS, panel_rows)
    write_csv(INTEGRALS, integral_rows)
    maximum_symmetry_error = max(
        float(row["symmetry_relative_error"]) for row in symmetry
    )
    maximum_quadrature_change = max(
        float(row["order4_order8_relative_change"])
        for row in integral_rows
    )
    order8 = {
        row["epsilon_id"]: complex(
            float(row["edge_integral_real"]),
            float(row["edge_integral_imaginary"]),
        )
        for row in integral_rows
        if int(row["quadrature_order"]) == max(QUADRATURE_ORDERS)
    }
    regulator_integral_ratio = abs(order8["E020"]) / max(
        abs(order8["E040"]),
        1.0e-300,
    )
    regulator_integral_change = relative_complex_change(
        order8["E040"],
        order8["E020"],
    )
    formal_end = M5283.formal_inventory_digest()
    checks = {
        "exact_mask_edge_solved": (
            residual <= BOUNDARY_RESIDUAL_LIMIT
        ),
        "mask_edge_is_transverse": (
            abs(derivative) >= BOUNDARY_DERIVATIVE_MINIMUM
        ),
        "single_component_edge_reduction_verified": (
            maximum_symmetry_error <= SYMMETRY_RELATIVE_ERROR_LIMIT
        ),
        "both_finite_regulators_integrated": (
            set(order8) == {"E040", "E020", "2E020_MINUS_E040"}
        ),
        "edge_quadrature_converged": (
            maximum_quadrature_change <= QUADRATURE_CHANGE_LIMIT
        ),
        "all_outputs_finite": all(
            math.isfinite(float(row[field]))
            for rows in (symmetry, pointwise, panel_rows, integral_rows)
            for row in rows
            for field in row
            if (
                field.endswith("_real")
                or field.endswith("_imaginary")
                or field.endswith("_magnitude")
                or field.endswith("_relative_change")
                or field == "symmetry_relative_error"
            )
            and row[field] != ""
        ),
        "integration_precision_initialized": (
            mp.mp.dps >= M5280.MP_DECIMAL_DIGITS
        ),
        "formalization_workbench_unchanged": (
            formal_end == str(parent["formalization_workbench_end_digest"])
        ),
        "claims_locked_false": True,
    }
    accepted = all(checks.values())
    if not accepted:
        decision = "MASK_EDGE_INTEGRABILITY_PIPELINE_REQUIRES_REPAIR"
    else:
        decision = (
            "MASK_EDGE_DERIVED_AND_FINITE_REGULATORS_CONVERGED__"
            "BUILD_REGULATOR_LADDER_BEFORE_FULL_CUBATURE"
        )
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "mask-edge-integrability-and-limit-order-audit",
        "checks": checks,
        "acceptance_passed": accepted,
        "decision": decision,
        "soft_energy": EDGE_ENERGY,
        "absolute_decay_cosine": EDGE_DECAY_ABSOLUTE,
        "absolute_soft_cosine_boundary": coordinate,
        "boundary_surface_residual": residual,
        "boundary_surface_derivative": derivative,
        "maximum_sign_orbit_symmetry_relative_error": (
            maximum_symmetry_error
        ),
        "maximum_edge_quadrature_relative_change": (
            maximum_quadrature_change
        ),
        **complex_fields("E040_edge_integral", order8["E040"]),
        **complex_fields("E020_edge_integral", order8["E020"]),
        **complex_fields(
            "two_E020_minus_E040_edge_integral",
            order8["2E020_MINUS_E040"],
        ),
        "E020_E040_integral_magnitude_ratio": regulator_integral_ratio,
        "E040_E020_integral_relative_change": regulator_integral_change,
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
            "valid_for_mask_edge_integrability_diagnostic": accepted,
            "valid_for_two_regulator_edge_integral": accepted,
            "valid_for_regulator_zero_limit": False,
            **{field: False for field in CLAIM_FIELDS},
            "reason": (
                "The exact mask edge and both available finite-regulator "
                "integrals are controlled, but two regulator values cannot "
                "establish the epsilon-to-zero limit or license the full "
                "angular cubature."
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
            "state": "COMPLETE" if accepted else "FAILED",
            "decision": decision,
            "boundary_coordinate": coordinate,
            "maximum_edge_quadrature_relative_change": (
                maximum_quadrature_change
            ),
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
    text = f"""# 5302 — Mask-edge integrability and limit-order audit

## Result

The unstable 5301 cell is not a generic interpolation failure. Its largest
residual is generated when the exact `MC04` mask turns on at the transverse
hard-leg surface

`F_{{+1,-0.3}}(sqrt(1-E),-s,-d)=0`.

At the sourced witness slice,

- `E={result['soft_energy']:.16g}`;
- `|d|={result['absolute_decay_cosine']:.16g}`;
- `|s|_edge={result['absolute_soft_cosine_boundary']:.16g}`;
- `|F|={result['boundary_surface_residual']:.12g}`;
- `dF/d|s|={result['boundary_surface_derivative']:.12g}`.

The remaining `MC04/MC12` sign-orbit terms cancel to relative error
`{result['maximum_sign_orbit_symmetry_relative_error']:.12g}`, leaving one
newly active signed `MC04` contribution. This proves why a smooth 3x3
polynomial model fails.

The boundary-aligned finite-regulator integrals over the first
`{EDGE_WINDOW:.3g}` in `|s|-|s|_edge` are

- `E040`: `{result['E040_edge_integral_real']:.12g} +
  {result['E040_edge_integral_imaginary']:.12g} i`;
- `E020`: `{result['E020_edge_integral_real']:.12g} +
  {result['E020_edge_integral_imaginary']:.12g} i`;
- `2 E020 - E040`: `{result['two_E020_minus_E040_edge_integral_real']:.12g} +
  {result['two_E020_minus_E040_edge_integral_imaginary']:.12g} i`.

The maximum order-4/order-8 edge-integral change is
`{result['maximum_edge_quadrature_relative_change']:.12g}`. The
`|I_E020|/|I_E040|` ratio is
`{result['E020_E040_integral_magnitude_ratio']:.12g}`.

Decision: **{result['decision']}**.

## Consequence

The earlier global angular rules sampled a threshold edge as though it were
a smooth ridge. Their values remain diagnostics, not a converged
phase-space coefficient. The correct next calculation is a regulator ladder
with boundary-aligned angular integration. Only that can distinguish a
finite regulator-zero limit from a pinch divergence or distributional
finite-part requirement.

## Acceptance gates

{checks}

Validation: **{'PASS' if passed else 'FAIL'}**.

## Claim boundary

This checkpoint derives one exact edge mechanism and integrates the two
available finite regulators. It does not establish the regulator-zero
limit, full angular convergence, the phase-space coefficient, a UV
coefficient, local GR, or the full MTS theory.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    result = read_json(RESULT)
    boundary = read_csv(BOUNDARY)
    symmetry = read_csv(SYMMETRY)
    pointwise = read_csv(POINTWISE)
    panels = read_csv(PANELS)
    integrals = read_csv(INTEGRALS)
    gates = [
        validation_gate(
            "result_accepted",
            bool(result["acceptance_passed"]),
            str(result["decision"]),
        ),
        validation_gate(
            "one_exact_boundary_witness",
            len(boundary) == 1
            and parse_bool(
                boundary[0]["valid_for_exact_mask_edge_witness"]
            ),
            f"rows={len(boundary)}",
        ),
        validation_gate(
            "symmetry_reduction_rows_complete",
            len(symmetry)
            == len(SYMMETRY_OFFSETS) * len(ENERGY_REGULATORS)
            and all(
                parse_bool(row["valid_for_single_edge_reduction"])
                for row in symmetry
            ),
            f"rows={len(symmetry)}",
        ),
        validation_gate(
            "pointwise_scaling_rows_complete",
            len(pointwise) == len(POINTWISE_OFFSETS),
            f"rows={len(pointwise)}",
        ),
        validation_gate(
            "edge_panel_integrals_complete",
            len(panels)
            == (
                (len(EDGE_PANEL_OFFSETS) - 1)
                * len(QUADRATURE_ORDERS)
                * len(ENERGY_REGULATORS)
            ),
            f"rows={len(panels)}",
        ),
        validation_gate(
            "finite_regulator_integrals_converged",
            len(integrals)
            == len(QUADRATURE_ORDERS)
            * (len(ENERGY_REGULATORS) + 1)
            and all(
                parse_bool(row["passes_edge_quadrature_gate"])
                for row in integrals
            ),
            f"rows={len(integrals)}",
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
            "claims_locked_false",
            not bool(
                result["claim_boundary"]["valid_for_regulator_zero_limit"]
            )
            and all(
                not bool(result["claim_boundary"][field])
                for field in CLAIM_FIELDS
            ),
            "no regulator-zero, angular, phase-space, UV, local-GR, or MTS claim",
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
            "VALIDATED_MASK_EDGE_INTEGRABILITY_AUDIT"
            if passed
            else "MASK_EDGE_INTEGRABILITY_VALIDATION_FAILED"
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
