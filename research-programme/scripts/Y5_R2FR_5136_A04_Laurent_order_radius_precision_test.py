from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
GENERIC_RUNNER = (
    POST
    / "scripts"
    / "Y5_R2FR_5132_locked_next_argument_gate_and_single_job_runner.py"
)
SOURCE = POST / "source-intake" / "functional_rg" / "5136"
DEFAULT_GATE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5135"
    / "A04_argument_local_outer_collinear_chart_gate.json"
)
ROWS_CSV = SOURCE / "A04_laurent_order_radius_precision_rows.csv"
RESULT_JSON = SOURCE / "A04_laurent_order_radius_precision_result.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5136_VALIDATION.csv"
)
DOCUMENT = POST / "5136-Y5-R2FR-A04-Laurent-order-radius-precision-test.md"

CHECKPOINT_ID = "5136"
MARKER = "MTS_5136_A04_LAURENT_ORDER_RADIUS_PRECISION_TEST"
CHECKED_DATE = "2026-07-20"
JOB_KEY = "E040__S512503_N0000__A04__primary24"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
BOUNDARY_FRACTIONS = (0.12, 0.10, 0.08, 0.06)
CHART_FRACTION = 0.65
MAXIMUM_RESIDUE_DISAGREEMENT = 5.0e-5
MAXIMUM_DOUBLE_TO_SIMPLE_RATIO = 2.0e-4
MAXIMUM_REGULAR_INTEGRAL_UNCERTAINTY = 2.0e-4
PRECISION_PROFILES = {
    "default": {
        "low_boundary_nodes": 24,
        "low_global_nodes": 32,
        "low_global_residue_nodes": 48,
        "high_boundary_nodes": 32,
        "high_global_nodes": 48,
        "high_global_residue_nodes": 64,
    },
    "nested": {
        "low_boundary_nodes": 48,
        "low_global_nodes": 64,
        "low_global_residue_nodes": 96,
        "high_boundary_nodes": 64,
        "high_global_nodes": 96,
        "high_global_residue_nodes": 128,
    },
}


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True), encoding="utf-8"
    )
    os.replace(temporary, path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def complex_row(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def log_slope(x_values: list[float], y_values: list[float]) -> float:
    logarithmic_x = [math.log(value) for value in x_values]
    logarithmic_y = [math.log(value) for value in y_values]
    mean_x = sum(logarithmic_x) / len(logarithmic_x)
    mean_y = sum(logarithmic_y) / len(logarithmic_y)
    numerator = sum(
        (x_value - mean_x) * (y_value - mean_y)
        for x_value, y_value in zip(logarithmic_x, logarithmic_y)
    )
    denominator = sum((value - mean_x) ** 2 for value in logarithmic_x)
    return numerator / denominator


def regular_uncertainty(
    module: Any,
    high: dict[str, Any],
    low: dict[str, Any],
    chart_radius: float,
) -> float:
    probes = [0.0j]
    for fraction in (0.25, 0.50):
        for direction in (1.0 + 0.0j, 1.0j, -1.0 + 0.0j, -1.0j):
            probes.append(fraction * chart_radius * direction)
    maximum_difference = max(
        abs(
            module.cauchy_regular_value(high, displacement)
            - module.cauchy_regular_value(low, displacement)
        )
        for displacement in probes
    )
    return maximum_difference * 2.0 * chart_radius / (2.0 * math.pi)


def measure_row(
    module: Any,
    original: Any,
    ownership: dict[str, bool],
    center: complex,
    nearest_distance: float,
    path_distance: float,
    boundary_fraction: float,
    precision_name: str,
    precision: dict[str, int],
) -> dict[str, Any]:
    radius = boundary_fraction * nearest_distance
    chart_radius = CHART_FRACTION * radius
    high = module.cauchy_boundary(
        original,
        ownership,
        center,
        radius,
        precision["high_boundary_nodes"],
        precision["high_global_nodes"],
        precision["high_global_residue_nodes"],
    )
    low = module.cauchy_boundary(
        original,
        ownership,
        center,
        radius,
        precision["low_boundary_nodes"],
        precision["low_global_nodes"],
        precision["low_global_residue_nodes"],
    )
    high_residue = complex(high["residue"])
    low_residue = complex(low["residue"])
    high_second = complex(high["second_principal_coefficient"])
    low_second = complex(low["second_principal_coefficient"])
    residue_disagreement = abs(high_residue - low_residue) / max(
        1.0, abs(high_residue), abs(low_residue)
    )
    high_ratio = abs(high_second) / max(abs(high_residue) * radius, 1.0e-30)
    low_ratio = abs(low_second) / max(abs(low_residue) * radius, 1.0e-30)
    coefficient_disagreement = abs(high_second - low_second) / max(
        abs(high_second), abs(low_second), 1.0e-30
    )
    regular_error = regular_uncertainty(module, high, low, chart_radius)
    accepted = bool(
        residue_disagreement < MAXIMUM_RESIDUE_DISAGREEMENT
        and high_ratio < MAXIMUM_DOUBLE_TO_SIMPLE_RATIO
        and regular_error < MAXIMUM_REGULAR_INTEGRAL_UNCERTAINTY
        and path_distance < chart_radius
    )
    return {
        "precision": precision_name,
        "boundary_fraction": boundary_fraction,
        "boundary_radius": radius,
        "chart_radius": chart_radius,
        "path_distance": path_distance,
        "path_intersects_chart": path_distance < chart_radius,
        "high_residue_real": high_residue.real,
        "high_residue_imaginary": high_residue.imag,
        "high_residue_magnitude": abs(high_residue),
        "low_residue_real": low_residue.real,
        "low_residue_imaginary": low_residue.imag,
        "low_residue_magnitude": abs(low_residue),
        "residue_disagreement": residue_disagreement,
        "high_second_principal_real": high_second.real,
        "high_second_principal_imaginary": high_second.imag,
        "high_second_principal_magnitude": abs(high_second),
        "low_second_principal_real": low_second.real,
        "low_second_principal_imaginary": low_second.imag,
        "low_second_principal_magnitude": abs(low_second),
        "second_principal_high_low_disagreement": coefficient_disagreement,
        "high_double_to_simple_ratio": high_ratio,
        "low_double_to_simple_ratio": low_ratio,
        "regular_integral_uncertainty": regular_error,
        "accepted_under_locked_thresholds": accepted,
        "high_runtime_seconds": high["runtime_seconds"],
        "low_runtime_seconds": low["runtime_seconds"],
        "checkpoint_marker": MARKER,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "source_checked_date": CHECKED_DATE,
    }


def decision(rows: list[dict[str, Any]]) -> dict[str, Any]:
    nested = [row for row in rows if row["precision"] == "nested"]
    default = [row for row in rows if row["precision"] == "default"]
    nested.sort(key=lambda row: row["boundary_radius"], reverse=True)
    default.sort(key=lambda row: row["boundary_radius"], reverse=True)
    nested_coefficients = [
        complex(
            row["high_second_principal_real"],
            row["high_second_principal_imaginary"],
        )
        for row in nested
    ]
    coefficient_mean = sum(nested_coefficients, 0.0j) / len(nested_coefficients)
    coefficient_spread = max(
        abs(value - coefficient_mean) for value in nested_coefficients
    ) / max(abs(coefficient_mean), 1.0e-30)
    ratio_slope = log_slope(
        [row["boundary_radius"] for row in nested],
        [row["high_double_to_simple_ratio"] for row in nested],
    )
    coefficient_slope = log_slope(
        [row["boundary_radius"] for row in nested],
        [row["high_second_principal_magnitude"] for row in nested],
    )
    maximum_high_low_disagreement = max(
        row["second_principal_high_low_disagreement"] for row in nested
    )
    nested_default_radius = next(
        row for row in nested if row["boundary_fraction"] == 0.12
    )
    default_default_radius = next(
        row for row in default if row["boundary_fraction"] == 0.12
    )
    precision_reduction = (
        default_default_radius["high_second_principal_magnitude"]
        / max(
            nested_default_radius["high_second_principal_magnitude"], 1.0e-30
        )
    )
    true_double_supported = bool(
        coefficient_spread <= 0.15
        and maximum_high_low_disagreement <= 0.15
        and -1.25 <= ratio_slope <= -0.75
        and abs(coefficient_slope) <= 0.25
    )
    numerical_contamination_supported = bool(
        not true_double_supported
        and nested_default_radius["accepted_under_locked_thresholds"]
        and precision_reduction >= 5.0
        and coefficient_spread > 0.15
    )
    if true_double_supported:
        outcome = "GENUINE_DOUBLE_POLE_SUPPORTED_SIMPLE_CHART_REJECTED"
    elif numerical_contamination_supported:
        outcome = "NUMERICAL_CONTAMINATION_SUPPORTED_REFINED_SIMPLE_CHART_ADMISSIBLE"
    else:
        outcome = "INCONCLUSIVE_SIMPLE_CHART_REMAINS_BLOCKED"
    return {
        "outcome": outcome,
        "true_double_pole_supported": true_double_supported,
        "numerical_contamination_supported": numerical_contamination_supported,
        "refined_simple_chart_admissible": numerical_contamination_supported,
        "nested_second_coefficient_relative_spread": coefficient_spread,
        "nested_double_to_simple_log_slope_vs_radius": ratio_slope,
        "nested_second_coefficient_log_slope_vs_radius": coefficient_slope,
        "nested_maximum_high_low_coefficient_disagreement": (
            maximum_high_low_disagreement
        ),
        "default_to_nested_second_coefficient_reduction_at_fraction_0p12": (
            precision_reduction
        ),
        "nested_fraction_0p12_passes_locked_thresholds": (
            nested_default_radius["accepted_under_locked_thresholds"]
        ),
        "criteria_fixed_before_result": True,
    }


def main() -> None:
    source_gate_hash_before = sha256(DEFAULT_GATE)
    runner = load_module("mts_5132_for_5136", GENERIC_RUNNER)
    arguments = argparse.Namespace(
        checkpoint_id=CHECKPOINT_ID,
        checked_date=CHECKED_DATE,
        job_key=JOB_KEY,
        precision="default",
        mode="dry-run",
    )
    job, configuration = runner.configure(arguments)
    base = runner.M5128
    chart_module = base.M5127
    context = base.build_context()
    candidates: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for chamber in context["chambers"]:
        for pole in chamber["active_poles"]:
            if pole["family"] == "beam_spinor" and pole["member"] == "small":
                candidates.append((chamber, pole))
    if len(candidates) != 1:
        raise RuntimeError(
            f"expected one active small beam-spinor pole, found {len(candidates)}"
        )
    chamber, pole = candidates[0]
    original = chamber["problem"]["module"].global_chamber_value
    center = complex(pole["log_point"])
    nearest_distance = float(pole["nearest_other_log_singularity_distance"])
    path_distance = float(pole["log_distance"])
    rows: list[dict[str, Any]] = []
    for precision_name, precision in PRECISION_PROFILES.items():
        for boundary_fraction in BOUNDARY_FRACTIONS:
            rows.append(
                measure_row(
                    chart_module,
                    original,
                    chamber["ownership"],
                    center,
                    nearest_distance,
                    path_distance,
                    boundary_fraction,
                    precision_name,
                    precision,
                )
            )
    diagnostic = decision(rows)
    write_csv(ROWS_CSV, rows)
    counts_after = base.M5125.run_counts(
        base.RUN, context["config"]["config_digest"], context["schedule"]
    )
    default_gate = read_json(DEFAULT_GATE)
    result = {
        "checkpoint_marker": MARKER,
        "job_key": JOB_KEY,
        "job": job,
        "configuration": configuration,
        "default_rejected_gate": base.relative(DEFAULT_GATE),
        "default_gate_sha256": source_gate_hash_before,
        "pole": {
            "family": pole["family"],
            "member": pole["member"],
            "root": complex_row(complex(pole["root"])),
            "log_point": complex_row(center),
            "path_distance": path_distance,
            "nearest_other_log_singularity_distance": nearest_distance,
        },
        "boundary_fractions": list(BOUNDARY_FRACTIONS),
        "chart_fraction": CHART_FRACTION,
        "precision_profiles": PRECISION_PROFILES,
        "locked_thresholds": {
            "maximum_residue_disagreement": MAXIMUM_RESIDUE_DISAGREEMENT,
            "maximum_double_to_simple_ratio": MAXIMUM_DOUBLE_TO_SIMPLE_RATIO,
            "maximum_regular_integral_uncertainty": (
                MAXIMUM_REGULAR_INTEGRAL_UNCERTAINTY
            ),
        },
        "diagnostic": diagnostic,
        "rows": base.relative(ROWS_CSV),
        "counts_before": configuration["counts_before"],
        "counts_after": counts_after,
        "formalization_workbench_tree_sha256": chart_module.tree_digest(FORMAL),
        "execution_performed": False,
        "full_pilot_resume_authorized": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "source_checked_date": CHECKED_DATE,
    }
    atomic_json(RESULT_JSON, result)
    finite_values = all(
        math.isfinite(float(row[key]))
        for row in rows
        for key in (
            "boundary_radius",
            "chart_radius",
            "high_residue_magnitude",
            "residue_disagreement",
            "high_second_principal_magnitude",
            "high_double_to_simple_ratio",
            "regular_integral_uncertainty",
        )
    )
    checks = [
        ("VAL5136_01_sources_exist", GENERIC_RUNNER.exists() and DEFAULT_GATE.exists()),
        ("VAL5136_02_locked_A04_selected", job["job_key"] == JOB_KEY),
        ("VAL5136_03_default_gate_preserved_rejected", not default_gate["gate_accepted"]),
        ("VAL5136_04_eight_predeclared_rows", len(rows) == 8),
        ("VAL5136_05_all_radius_charts_isolated", all(row["boundary_radius"] < nearest_distance for row in rows)),
        ("VAL5136_06_all_target_paths_intersect", all(row["path_intersects_chart"] for row in rows)),
        ("VAL5136_07_all_diagnostics_finite", finite_values),
        ("VAL5136_08_locked_thresholds_unchanged", chart_module.MAXIMUM_RESIDUE_DISAGREEMENT == MAXIMUM_RESIDUE_DISAGREEMENT and chart_module.MAXIMUM_DOUBLE_TO_SIMPLE_RATIO == MAXIMUM_DOUBLE_TO_SIMPLE_RATIO and chart_module.MAXIMUM_REGULAR_INTEGRAL_UNCERTAINTY == MAXIMUM_REGULAR_INTEGRAL_UNCERTAINTY),
        ("VAL5136_09_default_gate_file_unchanged", sha256(DEFAULT_GATE) == source_gate_hash_before),
        ("VAL5136_10_run_counts_unchanged", counts_after == configuration["counts_before"]),
        ("VAL5136_11_formal_tree_unchanged", result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE),
        ("VAL5136_12_no_claim_or_execution", not result["execution_performed"] and not result["valid_for_numeric_UV_claim"] and not result["valid_for_local_GR_claim"] and not result["valid_for_full_MTS_claim"]),
    ]
    validation_rows = [
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
    ]
    write_csv(VALIDATION_CSV, validation_rows)
    document_text = f"""# 5136: A04 Laurent-order radius/precision test

## Question

The locked default chart rejected `A04` because the small beam-spinor pole gave a
double-to-simple ratio above the fixed limit. Nested precision was not invoked as
a rescue because the existing policy allows it only after Laurent order already
passes. This checkpoint instead asks whether the apparent second-principal
coefficient behaves like a genuine double pole.

## Predeclared discriminator

The same pole is measured at boundary fractions `{BOUNDARY_FRACTIONS}` with the
existing default and nested node profiles. A genuine coefficient `a_(-2)` must
be stable between quadratures and radii, while
`|a_(-2)|/(|a_(-1)| r)` must scale approximately as `r^-1`. Numerical
contamination is admitted only if refinement reduces the coefficient by at
least a factor of five, the original radius passes every locked threshold at
nested precision, and the coefficient is not radius-stable.

## Result

- Outcome: `{diagnostic['outcome']}`.
- Nested coefficient relative spread: `{diagnostic['nested_second_coefficient_relative_spread']:.12g}`.
- Nested ratio log-slope: `{diagnostic['nested_double_to_simple_log_slope_vs_radius']:.12g}`.
- Nested coefficient log-slope: `{diagnostic['nested_second_coefficient_log_slope_vs_radius']:.12g}`.
- Default-to-nested coefficient reduction at boundary fraction `0.12`: `{diagnostic['default_to_nested_second_coefficient_reduction_at_fraction_0p12']:.12g}`.
- Nested original-radius locked-threshold pass: `{diagnostic['nested_fraction_0p12_passes_locked_thresholds']}`.
- Pilot counts remain `{counts_after}`; no coefficient job was executed.

## Discipline

This is a pole-order diagnostic, not a changed acceptance threshold. It cannot
establish a UV coefficient, local GR, galaxy phenomenology, or the full MTS
theory. The protected formalization tree remains `{FORMAL_BASELINE}` and no
GitHub action occurred.
"""
    DOCUMENT.write_text(document_text, encoding="utf-8")
    failures = [check_id for check_id, passed in checks if not passed]
    print(json.dumps({"result": result, "validation_failures": failures}, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
