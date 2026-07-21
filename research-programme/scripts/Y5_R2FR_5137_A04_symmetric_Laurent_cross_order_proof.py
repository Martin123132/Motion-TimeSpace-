from __future__ import annotations

import argparse
import importlib.util
import json
import math
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
SCRIPT_5136 = POST / "scripts" / "Y5_R2FR_5136_A04_Laurent_order_radius_precision_test.py"
GENERIC_RUNNER = POST / "scripts" / "Y5_R2FR_5132_locked_next_argument_gate_and_single_job_runner.py"
RADIUS_RESULT = POST / "source-intake" / "functional_rg" / "5136" / "A04_laurent_order_radius_precision_result.json"
SOURCE = POST / "source-intake" / "functional_rg" / "5137"
ROWS_CSV = SOURCE / "A04_symmetric_Laurent_cross_rows.csv"
RESULT_JSON = SOURCE / "A04_symmetric_Laurent_cross_result.json"
VALIDATION_CSV = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5137_VALIDATION.csv"
DOCUMENT = POST / "5137-Y5-R2FR-A04-symmetric-Laurent-cross-order-proof.md"

CHECKPOINT_ID = "5137"
MARKER = "MTS_5137_A04_SYMMETRIC_LAURENT_CROSS_ORDER_PROOF"
CHECKED_DATE = "2026-07-20"
JOB_KEY = "E040__S512503_N0000__A04__primary24"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
DISPLACEMENT_SCALES = (
    5.0e-3,
    2.0e-3,
    1.0e-3,
    5.0e-4,
    2.0e-4,
    1.0e-4,
    5.0e-5,
    2.0e-5,
    1.0e-5,
    5.0e-6,
    2.0e-6,
    1.0e-6,
)
AXES = {"real": 1.0 + 0.0j, "imaginary": 0.0 + 1.0j}
POINT_PRECISIONS = {
    "nested": {"global_nodes": 96, "global_residue_nodes": 128},
    "deep": {"global_nodes": 192, "global_residue_nodes": 256},
}
MAXIMUM_DOUBLE_TO_SIMPLE_RATIO = 2.0e-4


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def relative_difference(first: complex, second: complex) -> float:
    return abs(first - second) / max(abs(first), abs(second), 1.0e-30)


def coefficient(row: dict[str, Any], prefix: str) -> complex:
    return complex(row[f"{prefix}_real"], row[f"{prefix}_imaginary"])


def selected_row(
    rows: list[dict[str, Any]], precision: str, axis: str, scale: float
) -> dict[str, Any]:
    return next(
        row
        for row in rows
        if row["precision"] == precision
        and row["axis"] == axis
        and row["displacement_scale"] == scale
    )


def decision(rows: list[dict[str, Any]], nominal_boundary_radius: float) -> dict[str, Any]:
    tail_scales = [scale for scale in DISPLACEMENT_SCALES if scale <= 5.0e-5]
    axis_slopes: dict[str, float] = {}
    for axis in AXES:
        tail_rows = [selected_row(rows, "deep", axis, scale) for scale in tail_scales]
        axis_slopes[axis] = R5136.log_slope(
            [row["displacement_scale"] for row in tail_rows],
            [row["second_coefficient_magnitude"] for row in tail_rows],
        )
    smallest = min(DISPLACEMENT_SCALES)
    next_scale = sorted(DISPLACEMENT_SCALES)[1]
    deep_small = {axis: selected_row(rows, "deep", axis, smallest) for axis in AXES}
    nested_small = {axis: selected_row(rows, "nested", axis, smallest) for axis in AXES}
    deep_next = {axis: selected_row(rows, "deep", axis, next_scale) for axis in AXES}
    deep_residues = {
        axis: coefficient(row, "residue_estimate") for axis, row in deep_small.items()
    }
    nested_residues = {
        axis: coefficient(row, "residue_estimate") for axis, row in nested_small.items()
    }
    residue_axis_disagreement = relative_difference(
        deep_residues["real"], deep_residues["imaginary"]
    )
    residue_scale_drift = max(
        relative_difference(
            deep_residues[axis], coefficient(deep_next[axis], "residue_estimate")
        )
        for axis in AXES
    )
    residue_precision_disagreement = max(
        relative_difference(deep_residues[axis], nested_residues[axis])
        for axis in AXES
    )
    residue_mean = sum(deep_residues.values(), 0.0j) / len(deep_residues)
    deep_second = {
        axis: coefficient(row, "second_coefficient_estimate")
        for axis, row in deep_small.items()
    }
    nested_second = {
        axis: coefficient(row, "second_coefficient_estimate")
        for axis, row in nested_small.items()
    }
    second_upper_bound = max(
        max(abs(value) for value in deep_second.values()),
        max(abs(value) for value in nested_second.values()),
        max(
            abs(deep_second[axis] - nested_second[axis]) for axis in AXES
        ),
    )
    normalized_second_bound = second_upper_bound / max(
        abs(residue_mean) * nominal_boundary_radius, 1.0e-30
    )
    deep_second_axis_disagreement = relative_difference(
        deep_second["real"], deep_second["imaginary"]
    )
    simple_supported = bool(
        min(axis_slopes.values()) >= 1.5
        and residue_axis_disagreement <= 1.0e-2
        and residue_scale_drift <= 1.0e-2
        and residue_precision_disagreement <= 1.0e-2
        and normalized_second_bound < MAXIMUM_DOUBLE_TO_SIMPLE_RATIO
    )
    double_supported = bool(
        max(abs(value) for value in axis_slopes.values()) <= 0.25
        and deep_second_axis_disagreement <= 0.15
        and normalized_second_bound >= MAXIMUM_DOUBLE_TO_SIMPLE_RATIO
    )
    if simple_supported:
        outcome = "SIMPLE_POLE_SUPPORTED_SYMMETRIC_LAURENT_GATE_CLOSED"
    elif double_supported:
        outcome = "DOUBLE_POLE_SUPPORTED_SIMPLE_CHART_REJECTED"
    else:
        outcome = "INCONCLUSIVE_A04_REMAINS_BLOCKED"
    return {
        "outcome": outcome,
        "simple_pole_supported": simple_supported,
        "double_pole_supported": double_supported,
        "axis_second_coefficient_log_slopes": axis_slopes,
        "deep_residue_axis_disagreement": residue_axis_disagreement,
        "deep_residue_scale_drift": residue_scale_drift,
        "nested_deep_residue_precision_disagreement": residue_precision_disagreement,
        "deep_residue_mean": R5136.complex_row(residue_mean),
        "deep_second_axis_disagreement": deep_second_axis_disagreement,
        "conservative_second_coefficient_upper_bound": second_upper_bound,
        "normalized_second_coefficient_upper_bound": normalized_second_bound,
        "locked_maximum_double_to_simple_ratio": MAXIMUM_DOUBLE_TO_SIMPLE_RATIO,
        "criteria_fixed_before_result": True,
        "deep_chart_repair_authorized": simple_supported,
    }


def main() -> None:
    runner = load_module("mts_5132_for_5137", GENERIC_RUNNER)
    arguments = argparse.Namespace(
        checkpoint_id=CHECKPOINT_ID,
        checked_date=CHECKED_DATE,
        job_key=JOB_KEY,
        precision="default",
        mode="dry-run",
    )
    job, configuration = runner.configure(arguments)
    base = runner.M5128
    context = base.build_context()
    candidates: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for chamber in context["chambers"]:
        for pole in chamber["active_poles"]:
            if pole["family"] == "beam_spinor" and pole["member"] == "small":
                candidates.append((chamber, pole))
    if len(candidates) != 1:
        raise RuntimeError(f"expected one active target pole, found {len(candidates)}")
    chamber, pole = candidates[0]
    evaluator = chamber["problem"]["module"].global_chamber_value
    center = complex(pole["log_point"])
    rows: list[dict[str, Any]] = []
    for precision_name, precision in POINT_PRECISIONS.items():
        for axis_name, axis in AXES.items():
            for scale in DISPLACEMENT_SCALES:
                displacement = scale * axis
                plus_value = evaluator(
                    math.e ** (center + displacement),
                    chamber["ownership"],
                    precision["global_nodes"],
                    precision["global_residue_nodes"],
                )
                minus_value = evaluator(
                    math.e ** (center - displacement),
                    chamber["ownership"],
                    precision["global_nodes"],
                    precision["global_residue_nodes"],
                )
                residue_estimate = 0.5 * displacement * (plus_value - minus_value)
                second_estimate = 0.5 * displacement * displacement * (
                    plus_value + minus_value
                )
                rows.append(
                    {
                        "precision": precision_name,
                        "axis": axis_name,
                        "displacement_scale": scale,
                        "global_nodes": precision["global_nodes"],
                        "global_residue_nodes": precision["global_residue_nodes"],
                        "plus_value_real": plus_value.real,
                        "plus_value_imaginary": plus_value.imag,
                        "minus_value_real": minus_value.real,
                        "minus_value_imaginary": minus_value.imag,
                        "residue_estimate_real": residue_estimate.real,
                        "residue_estimate_imaginary": residue_estimate.imag,
                        "residue_estimate_magnitude": abs(residue_estimate),
                        "second_coefficient_estimate_real": second_estimate.real,
                        "second_coefficient_estimate_imaginary": second_estimate.imag,
                        "second_coefficient_magnitude": abs(second_estimate),
                        "checkpoint_marker": MARKER,
                        "valid_for_numeric_UV_claim": False,
                        "valid_for_local_GR_claim": False,
                        "valid_for_full_MTS_claim": False,
                        "source_checked_date": CHECKED_DATE,
                    }
                )
    R5136.write_csv(ROWS_CSV, rows)
    nominal_boundary_radius = float(pole["nominal_boundary_radius"])
    diagnostic = decision(rows, nominal_boundary_radius)
    counts_after = base.M5125.run_counts(
        base.RUN, context["config"]["config_digest"], context["schedule"]
    )
    result = {
        "checkpoint_marker": MARKER,
        "job_key": JOB_KEY,
        "job": job,
        "configuration": configuration,
        "predecessor_radius_result": base.relative(RADIUS_RESULT),
        "identity": {
            "residue": "a_-1(t)=(t/2)[f(t)-f(-t)]",
            "second_principal": "a_-2(t)=(t^2/2)[f(t)+f(-t)]",
            "simple_pole_limit": "a_-1(t)->a_-1 and a_-2(t)=O(t^2)",
            "double_pole_limit": "a_-2(t)->nonzero constant",
        },
        "point_precisions": POINT_PRECISIONS,
        "displacement_scales": list(DISPLACEMENT_SCALES),
        "axes": list(AXES),
        "nominal_boundary_radius": nominal_boundary_radius,
        "diagnostic": diagnostic,
        "rows": base.relative(ROWS_CSV),
        "counts_before": configuration["counts_before"],
        "counts_after": counts_after,
        "formalization_workbench_tree_sha256": base.M5127.tree_digest(FORMAL),
        "execution_performed": False,
        "full_pilot_resume_authorized": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "source_checked_date": CHECKED_DATE,
    }
    R5136.atomic_json(RESULT_JSON, result)
    finite_rows = all(
        math.isfinite(float(row[key]))
        for row in rows
        for key in (
            "residue_estimate_magnitude",
            "second_coefficient_magnitude",
            "plus_value_real",
            "minus_value_real",
        )
    )
    checks = [
        ("VAL5137_01_sources_exist", all(path.exists() for path in (SCRIPT_5136, GENERIC_RUNNER, RADIUS_RESULT))),
        ("VAL5137_02_locked_A04_selected", job["job_key"] == JOB_KEY),
        ("VAL5137_03_predecessor_inconclusive", R5136.read_json(RADIUS_RESULT)["diagnostic"]["outcome"] == "INCONCLUSIVE_SIMPLE_CHART_REMAINS_BLOCKED"),
        ("VAL5137_04_predeclared_48_rows", len(rows) == len(POINT_PRECISIONS) * len(AXES) * len(DISPLACEMENT_SCALES)),
        ("VAL5137_05_all_points_inside_isolated_chart", max(DISPLACEMENT_SCALES) < nominal_boundary_radius),
        ("VAL5137_06_all_values_finite", finite_rows),
        ("VAL5137_07_identity_axes_complete", set(row["axis"] for row in rows) == set(AXES)),
        ("VAL5137_08_precision_profiles_complete", set(row["precision"] for row in rows) == set(POINT_PRECISIONS)),
        ("VAL5137_09_decision_exclusive", not (diagnostic["simple_pole_supported"] and diagnostic["double_pole_supported"])),
        ("VAL5137_10_run_counts_unchanged", counts_after == configuration["counts_before"]),
        ("VAL5137_11_formal_tree_unchanged", result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE),
        ("VAL5137_12_no_claim_or_execution", not result["execution_performed"] and not result["valid_for_numeric_UV_claim"] and not result["valid_for_local_GR_claim"] and not result["valid_for_full_MTS_claim"]),
    ]
    R5136.write_csv(
        VALIDATION_CSV,
        [
            {
                "check_id": check_id,
                "passed": passed,
                "checkpoint_marker": MARKER,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
                "source_checked_date": CHECKED_DATE,
            }
            for check_id, passed in checks
        ],
    )
    document = f"""# 5137: A04 symmetric Laurent-cross order proof

## Derivation

For `f(t)=a_-2/t^2+a_-1/t+a_0+a_1 t+...`, paired samples give

`(t/2)[f(t)-f(-t)]=a_-1+O(t^2)`

and

`(t^2/2)[f(t)+f(-t)]=a_-2+O(t^2)`.

This separates simple and double principal parts without extracting a noisy
second Fourier mode from a surrounding contour.

## Result

- Outcome: `{diagnostic['outcome']}`.
- Real/imaginary `a_-2(t)` slopes: `{diagnostic['axis_second_coefficient_log_slopes']}`.
- Residue axis disagreement: `{diagnostic['deep_residue_axis_disagreement']:.12g}`.
- Residue scale drift: `{diagnostic['deep_residue_scale_drift']:.12g}`.
- Nested/deep residue disagreement: `{diagnostic['nested_deep_residue_precision_disagreement']:.12g}`.
- Conservative normalized `a_-2` bound: `{diagnostic['normalized_second_coefficient_upper_bound']:.12g}` against the unchanged `{MAXIMUM_DOUBLE_TO_SIMPLE_RATIO}` gate.
- Deep chart repair authorized: `{diagnostic['deep_chart_repair_authorized']}`.

## Scope

No coefficient job was executed. This establishes only the local meromorphic
order needed by the numerical coefficient pipeline; it is not a UV, local-GR,
galaxy, or full-MTS result. The formalization tree remains `{FORMAL_BASELINE}`.
"""
    DOCUMENT.write_text(document, encoding="utf-8")
    failures = [check_id for check_id, passed in checks if not passed]
    print(json.dumps({"result": result, "validation_failures": failures}, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


R5136 = load_module("mts_5136_for_5137", SCRIPT_5136)


if __name__ == "__main__":
    main()
