from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import sys
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
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FORMAL = ROOT / "formalization-workbench"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
MTS_RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5337 = SCRIPTS / "Y5_R2FR_5337_D4_regulator_fold_double_scaling_and_contrast_gate.py"
SCRIPT_5358 = SCRIPTS / "Y5_R2FR_5358_D4_zero_regulator_analytic_collision_and_event_continuation.py"
SCRIPT_5359 = SCRIPTS / "Y5_R2FR_5359_D4_zero_regulator_endpoint_coefficient_limit.py"
SCRIPT_5373 = SCRIPTS / "Y5_R2FR_5373_D4_seven_rung_extended_window_stability_gate.py"
SCRIPT_5375 = SCRIPTS / "Y5_R2FR_5375_D4_derived_A_primary_role_separation_gate.py"
SCRIPT_5376 = SCRIPTS / "Y5_R2FR_5376_D4_uniform_remainder_decomposition_and_bound_reduction.py"

SCAN_5337 = FUNCTIONAL_RG / "5337" / "D4_targeted_event_regulator_scan.csv"
RESULT_5337 = FUNCTIONAL_RG / "5337" / "D4_regulator_fold_double_scaling_contrast_result.json"
SOURCES_5337 = FUNCTIONAL_RG / "5337" / "source_register.csv"
ZERO_EVENTS_5358 = FUNCTIONAL_RG / "5358" / "D4_zero_regulator_event_certificate.csv"
RESULT_5358 = FUNCTIONAL_RG / "5358" / "D4_zero_regulator_continuation_result.json"
VALIDATION_5358 = FUNCTIONAL_RG / "5358" / "D4_zero_regulator_continuation_validation.csv"
SOURCES_5358 = FUNCTIONAL_RG / "5358" / "source_register.csv"
ZERO_COEFFICIENTS_5359 = FUNCTIONAL_RG / "5359" / "D4_zero_regulator_endpoint_coefficients.csv"
RESULT_5359 = FUNCTIONAL_RG / "5359" / "D4_zero_regulator_endpoint_result.json"
VALIDATION_5359 = FUNCTIONAL_RG / "5359" / "D4_zero_regulator_endpoint_validation.csv"
SOURCES_5359 = FUNCTIONAL_RG / "5359" / "source_register.csv"
INPUTS_5357 = FUNCTIONAL_RG / "5357" / "D4_six_regulator_coefficient_inputs.csv"
VALIDATION_5357 = FUNCTIONAL_RG / "5357" / "D4_six_regulator_coefficient_validation.csv"
SOURCES_5357 = FUNCTIONAL_RG / "5357" / "source_register.csv"
INPUTS_5373 = FUNCTIONAL_RG / "5373" / "D4_seven_rung_inputs.csv"
FIT_5373 = FUNCTIONAL_RG / "5373" / "D4_seven_rung_fixed_A_complete_fit.csv"
RESULT_5373 = FUNCTIONAL_RG / "5373" / "D4_seven_rung_extended_window_result.json"
VALIDATION_5373 = FUNCTIONAL_RG / "5373" / "D4_seven_rung_extended_window_validation.csv"
SOURCES_5373 = FUNCTIONAL_RG / "5373" / "source_register.csv"
RESULT_5375 = FUNCTIONAL_RG / "5375" / "D4_derived_A_primary_role_result.json"
VALIDATION_5375 = FUNCTIONAL_RG / "5375" / "D4_derived_A_primary_role_validation.csv"
SOURCES_5375 = FUNCTIONAL_RG / "5375" / "source_register.csv"
RESULT_5376 = FUNCTIONAL_RG / "5376" / "D4_uniform_remainder_reduction_result.json"
VALIDATION_5376 = FUNCTIONAL_RG / "5376" / "D4_uniform_remainder_reduction_validation.csv"
SOURCES_5376 = FUNCTIONAL_RG / "5376" / "source_register.csv"

OUTPUT = FUNCTIONAL_RG / "5377"
EVENT_RECONSTRUCTION = OUTPUT / "D4_full_endpoint_primitive_event_reconstruction.csv"
RUNG_TOTALS = OUTPUT / "D4_full_endpoint_primitive_rung_totals.csv"
C_STABILITY = OUTPUT / "D4_endpoint_C_candidate_stability.csv"
EVENT_SAMPLES = OUTPUT / "D4_sampled_event_branch_atlas.csv"
EVENT_TUBES = OUTPUT / "D4_sampled_fixed_event_tubes.csv"
FIXED_AC_FIT = OUTPUT / "D4_fixed_A_C_fit.csv"
FIXED_AC_RESIDUALS = OUTPUT / "D4_fixed_A_C_residuals.csv"
CONTRACT = OUTPUT / "D4_full_endpoint_C_reconstruction_contract.csv"
RESULT = OUTPUT / "D4_full_endpoint_C_reconstruction_result.json"
VALIDATION = OUTPUT / "D4_full_endpoint_C_reconstruction_validation.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
STATUS = OUTPUT / "status.json"
RESIDUAL_VALIDATION = MTS_RESIDUALS / "P8_Y5_BRR545_5377_VALIDATION.csv"
DOCUMENT = POST / "5377-Y5-R2FR-D4-full-endpoint-C-reconstruction-and-fixed-AC-gate.md"

CHECKPOINT = 5377
MARKER = "MTS_5377_D4_FULL_ENDPOINT_C_RECONSTRUCTION_AND_FIXED_AC_GATE"
REVISION = "D4-full-endpoint-C-reconstruction-fixed-AC-v1"
EPSILON_REFERENCE = 0.0025
EPSILON_ATLAS_MAXIMUM = 0.02
EVENT_ROOT_RADIUS = 1.0e-11
EVENT_IDS = tuple(f"E{index:02d}" for index in range(1, 9))
COORDINATE_ORDER = ("E01", "E02", "E03", "E05", "E04", "E06", "E07", "E08")
FORMAL_DIGEST = "0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f"
RELATIVE_INTERCEPT_LIMIT = 1.0e-2

CLAIM_RECONSTRUCTION = "valid_for_D4_full_endpoint_primitive_finite_rung_reconstruction"
CLAIM_SAMPLED_ATLAS = "valid_for_D4_sampled_eight_event_topology_atlas"
CLAIM_C_CANDIDATE = "valid_for_D4_parent_normal_form_C_candidate"
CLAIM_FIXED_AC = "valid_for_D4_conditional_fixed_A_C_seven_rung_numerical_stability"
FALSE_CLAIMS = (
    "valid_for_D4_endpoint_C_regulator_zero_limit",
    "valid_for_D4_common_closed_interval_event_atlas",
    "valid_for_D4_numeric_H3_bound",
    "valid_for_D4_numeric_uniform_remainder_bound",
    "valid_for_D4_outer_regulator_zero_limit",
    "valid_for_decay_angle_integral",
    "valid_for_full_angular_convergence",
    "valid_for_full_phase_space_coefficient",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)

RUNG_SPECS = (
    {
        "epsilon_id": "E000625",
        "epsilon": 0.000625,
        "support": FUNCTIONAL_RG / "5347" / "E000625" / "support" / "D4_E000625_support_endpoint_coefficients.csv",
        "branch": FUNCTIONAL_RG / "5347" / "E000625" / "all-eight" / "D4_E000625_one_sided_branch_endpoint_coefficients.csv",
        "ledger": FUNCTIONAL_RG / "5347" / "E000625" / "all-eight" / "D4_E000625_all_eight_endpoint_coefficient_ledger.csv",
        "support_validation": FUNCTIONAL_RG / "5347" / "E000625" / "support" / "D4_E000625_support_endpoint_validation.csv",
        "branch_validation": FUNCTIONAL_RG / "5347" / "E000625" / "all-eight" / "D4_E000625_all_eight_endpoint_validation.csv",
        "support_sources": FUNCTIONAL_RG / "5347" / "E000625" / "support" / "source_register.csv",
        "branch_sources": FUNCTIONAL_RG / "5347" / "E000625" / "all-eight" / "source_register.csv",
    },
    {
        "epsilon_id": "E00125",
        "epsilon": 0.00125,
        "support": FUNCTIONAL_RG / "5342" / "D4_E00125_support_endpoint_coefficients.csv",
        "branch": FUNCTIONAL_RG / "5346" / "E00125" / "D4_E00125_one_sided_branch_endpoint_coefficients.csv",
        "ledger": FUNCTIONAL_RG / "5346" / "E00125" / "D4_E00125_all_eight_endpoint_coefficient_ledger.csv",
        "support_validation": FUNCTIONAL_RG / "5342" / "D4_E00125_support_endpoint_normal_form_result.json",
        "branch_validation": FUNCTIONAL_RG / "5346" / "E00125" / "D4_E00125_all_eight_endpoint_validation.csv",
        "support_sources": FUNCTIONAL_RG / "5342" / "source_register.csv",
        "branch_sources": FUNCTIONAL_RG / "5346" / "E00125" / "source_register.csv",
    },
    {
        "epsilon_id": "E0025",
        "epsilon": 0.0025,
        "support": FUNCTIONAL_RG / "5351" / "E0025" / "support" / "D4_E0025_support_endpoint_coefficients.csv",
        "branch": FUNCTIONAL_RG / "5353" / "E0025" / "all-eight" / "D4_E0025_one_sided_branch_endpoint_coefficients.csv",
        "ledger": FUNCTIONAL_RG / "5353" / "E0025" / "all-eight" / "D4_E0025_all_eight_endpoint_coefficient_ledger.csv",
        "support_validation": FUNCTIONAL_RG / "5351" / "E0025" / "support" / "D4_E0025_support_endpoint_validation.csv",
        "branch_validation": FUNCTIONAL_RG / "5353" / "E0025" / "all-eight" / "D4_E0025_all_eight_endpoint_validation.csv",
        "support_sources": FUNCTIONAL_RG / "5351" / "E0025" / "support" / "source_register.csv",
        "branch_sources": FUNCTIONAL_RG / "5353" / "E0025" / "all-eight" / "source_register.csv",
    },
    {
        "epsilon_id": "E005",
        "epsilon": 0.005,
        "support": FUNCTIONAL_RG / "5347" / "E005" / "support" / "D4_E005_support_endpoint_coefficients.csv",
        "branch": FUNCTIONAL_RG / "5347" / "E005" / "all-eight" / "D4_E005_one_sided_branch_endpoint_coefficients.csv",
        "ledger": FUNCTIONAL_RG / "5347" / "E005" / "all-eight" / "D4_E005_all_eight_endpoint_coefficient_ledger.csv",
        "support_validation": FUNCTIONAL_RG / "5347" / "E005" / "support" / "D4_E005_support_endpoint_validation.csv",
        "branch_validation": FUNCTIONAL_RG / "5347" / "E005" / "all-eight" / "D4_E005_all_eight_endpoint_validation.csv",
        "support_sources": FUNCTIONAL_RG / "5347" / "E005" / "support" / "source_register.csv",
        "branch_sources": FUNCTIONAL_RG / "5347" / "E005" / "all-eight" / "source_register.csv",
    },
    {
        "epsilon_id": "E010",
        "epsilon": 0.01,
        "support": FUNCTIONAL_RG / "5356" / "E010" / "support" / "D4_E010_support_endpoint_coefficients.csv",
        "branch": FUNCTIONAL_RG / "5356" / "E010" / "all-eight" / "D4_E010_one_sided_branch_endpoint_coefficients.csv",
        "ledger": FUNCTIONAL_RG / "5356" / "E010" / "all-eight" / "D4_E010_all_eight_endpoint_coefficient_ledger.csv",
        "support_validation": FUNCTIONAL_RG / "5356" / "E010" / "support" / "D4_E010_support_endpoint_validation.csv",
        "branch_validation": FUNCTIONAL_RG / "5356" / "E010" / "all-eight" / "D4_E010_all_eight_endpoint_validation.csv",
        "support_sources": FUNCTIONAL_RG / "5356" / "E010" / "support" / "source_register.csv",
        "branch_sources": FUNCTIONAL_RG / "5356" / "E010" / "all-eight" / "source_register.csv",
    },
    {
        "epsilon_id": "E020",
        "epsilon": 0.02,
        "support": FUNCTIONAL_RG / "5356" / "E020" / "support" / "D4_E020_support_endpoint_coefficients.csv",
        "branch": FUNCTIONAL_RG / "5356" / "E020" / "all-eight" / "D4_E020_one_sided_branch_endpoint_coefficients.csv",
        "ledger": FUNCTIONAL_RG / "5356" / "E020" / "all-eight" / "D4_E020_all_eight_endpoint_coefficient_ledger.csv",
        "support_validation": FUNCTIONAL_RG / "5356" / "E020" / "support" / "D4_E020_support_endpoint_validation.csv",
        "branch_validation": FUNCTIONAL_RG / "5356" / "E020" / "all-eight" / "D4_E020_all_eight_endpoint_validation.csv",
        "support_sources": FUNCTIONAL_RG / "5356" / "E020" / "support" / "source_register.csv",
        "branch_sources": FUNCTIONAL_RG / "5356" / "E020" / "all-eight" / "source_register.csv",
    },
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


M5376 = load_module("mts_5376_for_5377", SCRIPT_5376)
M5373 = M5376.M5373
M5370 = M5376.M5370
np = M5370.np


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def set_below_normal_priority() -> None:
    M5376.set_below_normal_priority()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def normalize(value: Any) -> Any:
    return M5376.normalize(value)


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    M5376.atomic_csv(path, rows)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    M5376.atomic_json(path, payload)


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return M5376.complex_fields(prefix, value)


def validation_row(gate: str, passed: bool, detail: Any) -> dict[str, Any]:
    return {"gate": gate, "passed": bool(passed), "detail": str(detail)}


def csv_passes(path: Path) -> bool:
    rows = read_csv(path)
    return bool(rows) and all(parse_bool(row["passed"]) for row in rows)


def source_register_current(path: Path) -> tuple[bool, int, list[str]]:
    rows = read_csv(path)
    drifts: list[str] = []
    for row in rows:
        source_text = row.get("path") or row.get("source_path_or_url") or ""
        expected = row.get("sha256") or row.get("expected_sha256") or ""
        if not source_text or not expected:
            drifts.append(f"malformed:{path}")
            continue
        if source_text.startswith(("http://", "https://")):
            if row.get("expected_sha256") and row.get("sha256") != row.get(
                "expected_sha256"
            ):
                drifts.append(source_text)
            continue
        source = Path(source_text)
        if not source.is_file() or digest(source) != expected:
            drifts.append(str(source))
    return not drifts, len(rows), drifts


def false_claims() -> dict[str, bool]:
    return {field: False for field in FALSE_CLAIMS}


def complex_from_row(row: dict[str, str], prefix: str) -> complex:
    return complex(float(row[f"{prefix}_real"]), float(row[f"{prefix}_imaginary"]))


def direct_source_paths() -> tuple[Path, ...]:
    paths: list[Path] = [
        Path(__file__).resolve(),
        SCRIPT_5337,
        SCRIPT_5358,
        SCRIPT_5359,
        SCRIPT_5373,
        SCRIPT_5375,
        SCRIPT_5376,
        SCAN_5337,
        RESULT_5337,
        SOURCES_5337,
        ZERO_EVENTS_5358,
        RESULT_5358,
        VALIDATION_5358,
        SOURCES_5358,
        ZERO_COEFFICIENTS_5359,
        RESULT_5359,
        VALIDATION_5359,
        SOURCES_5359,
        INPUTS_5357,
        VALIDATION_5357,
        SOURCES_5357,
        INPUTS_5373,
        FIT_5373,
        RESULT_5373,
        VALIDATION_5373,
        SOURCES_5373,
        RESULT_5375,
        VALIDATION_5375,
        SOURCES_5375,
        RESULT_5376,
        VALIDATION_5376,
        SOURCES_5376,
    ]
    for spec in RUNG_SPECS:
        paths.extend(
            (
                spec["support"],
                spec["branch"],
                spec["ledger"],
                spec["support_validation"],
                spec["branch_validation"],
                spec["support_sources"],
                spec["branch_sources"],
            )
        )
    return tuple(dict.fromkeys(paths))


def relative_metric(row: dict[str, str], names: tuple[str, ...]) -> float:
    for name in names:
        value = row.get(name, "")
        if value not in (None, ""):
            return abs(float(value))
    return 0.0


def reconstruct_rungs() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    total_input_disks = {
        row["epsilon_id"]: float(row["A_diagnostic_disk_radius"])
        for row in read_csv(INPUTS_5357)
    }
    event_rows: list[dict[str, Any]] = []
    total_rows: list[dict[str, Any]] = []
    for spec in RUNG_SPECS:
        epsilon_id = str(spec["epsilon_id"])
        epsilon = float(spec["epsilon"])
        ledger = {row["event_id"]: row for row in read_csv(spec["ledger"])}
        normal_rows = read_csv(spec["support"]) + read_csv(spec["branch"])
        leading_total = 0.0j
        correction_total = 0.0j
        full_total = 0.0j
        correction_disk_total = 0.0
        maximum_leading_identity_error = 0.0
        for row in normal_rows:
            event_id = row["event_id"]
            ledger_row = ledger[event_id]
            z0 = complex_from_row(row, "boundary_gap_z0")
            z1 = complex_from_row(row, "boundary_gap_derivative_z1")
            c0 = complex_from_row(row, "physical_coefficient_C0")
            c1 = complex_from_row(row, "physical_coefficient_derivative_C1")
            ratio = z0 / z1
            sign = int(row["log_sign"])
            leading_h = -sign * c0 * ratio
            c1_h = 0.5 * sign * c1 * ratio**2
            full_h = leading_h + c1_h
            leading_coefficient = leading_h / epsilon
            correction_coefficient = c1_h / epsilon
            full_coefficient = full_h / epsilon
            stored_leading = complex(
                float(ledger_row["A_event_real"]),
                float(ledger_row["A_event_imaginary"]),
            )
            leading_identity_error = abs(leading_coefficient - stored_leading)
            maximum_leading_identity_error = max(
                maximum_leading_identity_error, leading_identity_error
            )
            z0_relative = relative_metric(
                row, ("boundary_gap_trace_relative_mismatch",)
            )
            z1_relative = relative_metric(
                row,
                (
                    "boundary_gap_derivative_relative_change_full_vs_half",
                    "boundary_gap_derivative_relative_change",
                ),
            )
            c1_relative = relative_metric(
                row,
                (
                    "physical_coefficient_derivative_relative_change_full_vs_half",
                    "physical_coefficient_derivative_relative_change",
                ),
            )
            primitive_relative = relative_metric(
                row, ("primitive_derivative_relative_error",)
            )
            coordinate_disk = float(
                ledger_row.get("A_event_coordinate_disk_radius") or 0.0
            )
            scaled_coordinate_disk = coordinate_disk * abs(correction_coefficient) / max(
                abs(leading_coefficient), 1.0e-300
            )
            correction_disk = abs(correction_coefficient) * (
                2.0 * z0_relative
                + 2.0 * z1_relative
                + c1_relative
                + primitive_relative
            ) + scaled_coordinate_disk
            leading_total += leading_coefficient
            correction_total += correction_coefficient
            full_total += full_coefficient
            correction_disk_total += correction_disk
            event_rows.append(
                {
                    "epsilon_id": epsilon_id,
                    "epsilon": epsilon,
                    "event_id": event_id,
                    "event_type": row["event_type"],
                    "term_id": row["term_id"],
                    "primary_surface_id": row["primary_surface_id"],
                    "log_sign": sign,
                    **complex_fields("z0", z0),
                    **complex_fields("z1", z1),
                    **complex_fields("C0", c0),
                    **complex_fields("C1", c1),
                    **complex_fields("leading_H_over_epsilon", leading_coefficient),
                    **complex_fields("C1_correction_H_over_epsilon", correction_coefficient),
                    **complex_fields("full_H_over_epsilon", full_coefficient),
                    "stored_leading_A_identity_error": leading_identity_error,
                    "C1_correction_diagnostic_disk": correction_disk,
                    "coefficient_contract_passes": parse_bool(
                        row["coefficient_contract_passes"]
                    )
                    and parse_bool(ledger_row["coefficient_contract_passes"]),
                    "normal_form_source_path": str(
                        (
                            spec["support"]
                            if row["event_type"] != "BRANCH_DEATH"
                            else spec["branch"]
                        ).resolve()
                    ),
                    "ledger_source_path": str(spec["ledger"].resolve()),
                }
            )
        total_disk = total_input_disks[epsilon_id] + correction_disk_total
        total_rows.append(
            {
                "epsilon_id": epsilon_id,
                "epsilon": epsilon,
                "event_count": len(normal_rows),
                **complex_fields("leading_A_finite", leading_total),
                **complex_fields("C1_correction_H_over_epsilon", correction_total),
                **complex_fields("full_H_over_epsilon", full_total),
                "leading_A_source_disk": total_input_disks[epsilon_id],
                "C1_correction_diagnostic_disk": correction_disk_total,
                "full_H_over_epsilon_diagnostic_disk": total_disk,
                "maximum_event_leading_identity_error": maximum_leading_identity_error,
                "all_event_contracts_pass": all(
                    parse_bool(row["coefficient_contract_passes"])
                    for row in normal_rows
                ),
            }
        )
    return event_rows, total_rows


def slope_model(
    rows: list[dict[str, Any]],
    source_a: complex,
    source_a_radius: float,
    count: int,
    weighted: bool,
) -> dict[str, Any]:
    selected = rows[:count]
    epsilon = np.asarray([row["epsilon"] for row in selected], dtype=float)
    values = np.asarray(
        [
            complex(
                row["full_H_over_epsilon_real"],
                row["full_H_over_epsilon_imaginary"],
            )
            for row in selected
        ],
        dtype=complex,
    )
    radii = np.asarray(
        [row["full_H_over_epsilon_diagnostic_disk"] for row in selected],
        dtype=float,
    )
    weights = 1.0 / radii**2 if weighted else np.ones(len(selected))
    denominator = float(np.sum(weights * epsilon**2))
    projection = weights * epsilon / denominator
    slope = complex(projection @ (values - source_a))
    predictions = source_a + slope * epsilon
    residuals = values - predictions
    data_disk = float(np.sum(np.abs(projection) * radii))
    source_a_disk = abs(float(np.sum(projection))) * source_a_radius
    return {
        "model_id": f"{'WEIGHTED' if weighted else 'UNWEIGHTED'}_SMALLEST_{count}",
        "count": count,
        "weighted": weighted,
        "slope": slope,
        "projection": projection,
        "residuals": residuals,
        "maximum_residual": float(np.max(np.abs(residuals))),
        "maximum_residual_over_epsilon": float(
            np.max(np.abs(residuals) / epsilon)
        ),
        "maximum_remainder_quotient": float(
            np.max((np.abs(residuals) + radii + source_a_radius) / epsilon**2)
        ),
        "data_disk": data_disk,
        "source_a_disk": source_a_disk,
        "base_disk": data_disk + source_a_disk,
    }


def build_C_models(
    rows: list[dict[str, Any]], source_a: complex, source_a_radius: float
) -> tuple[list[dict[str, Any]], dict[str, Any], float]:
    models = [
        slope_model(rows, source_a, source_a_radius, count, weighted)
        for count in range(3, 7)
        for weighted in (True, False)
    ]
    selected = next(
        model
        for model in models
        if model["count"] == 6 and model["weighted"] is True
    )
    center_shifts = [
        abs(model["slope"] - selected["slope"]) for model in models
    ]
    maximum_center_shift = max(center_shifts)
    candidate_disk = (
        selected["base_disk"]
        + maximum_center_shift
        + selected["maximum_residual_over_epsilon"]
    )
    output_rows = [
        {
            "model_id": model["model_id"],
            "rung_count": model["count"],
            "weighted_by_inverse_diagnostic_disk_squared": model["weighted"],
            **complex_fields("C_log_candidate", model["slope"]),
            "C_log_estimator_data_disk": model["data_disk"],
            "C_log_correlated_A_disk": model["source_a_disk"],
            "C_log_base_estimator_disk": model["base_disk"],
            "maximum_full_H_over_epsilon_residual": model["maximum_residual"],
            "maximum_residual_over_epsilon": model[
                "maximum_residual_over_epsilon"
            ],
            "maximum_disk_inclusive_full_H_remainder_quotient": model[
                "maximum_remainder_quotient"
            ],
            "shift_from_selected_C_candidate": shift,
            "selected_C_candidate": model is selected,
        }
        for model, shift in zip(models, center_shifts)
    ]
    return output_rows, selected, candidate_disk


def weighted_fit(
    design: Any, values: Any, radii: Any, weighted: bool
) -> tuple[Any, Any]:
    weights = 1.0 / radii**2 if weighted else np.ones(len(radii))
    normal = design.T @ (weights[:, None] * design)
    projection = np.linalg.solve(normal, design.T * weights)
    return projection @ values, projection


def fixed_AC_fit(
    inputs: list[dict[str, Any]],
    source_a: complex,
    source_a_radius: float,
    source_c: complex,
    source_c_radius: float,
) -> dict[str, Any]:
    epsilon = np.asarray([row["epsilon"] for row in inputs], dtype=float)
    values = np.asarray([row["value"] for row in inputs], dtype=complex)
    radii = np.asarray([row["radius"] for row in inputs], dtype=float)
    logarithm = np.log(epsilon / EPSILON_REFERENCE)
    x = epsilon / EPSILON_REFERENCE
    a_feature = epsilon * logarithm
    c_feature = epsilon**2 * logarithm
    corrected = values - source_a * a_feature - source_c * c_feature
    design = np.column_stack((np.ones(len(x)), x, x**2))
    weighted_coefficients, weighted_projection = weighted_fit(
        design, corrected, radii, True
    )
    unweighted_coefficients, _ = weighted_fit(design, corrected, radii, False)
    predictions = (
        design @ weighted_coefficients
        + source_a * a_feature
        + source_c * c_feature
    )
    residuals = values - predictions
    intercept_projection = weighted_projection[0]
    input_disk = float(np.sum(np.abs(intercept_projection) * radii))
    a_disk = abs(complex(intercept_projection @ a_feature)) * source_a_radius
    c_disk = abs(complex(intercept_projection @ c_feature)) * source_c_radius
    base_disk = input_disk + a_disk + c_disk
    loo_intercepts: list[complex] = []
    for omitted in range(len(inputs)):
        keep = np.asarray([index != omitted for index in range(len(inputs))])
        coefficients, _ = weighted_fit(
            design[keep], corrected[keep], radii[keep], True
        )
        loo_intercepts.append(complex(coefficients[0]))
    intercept = complex(weighted_coefficients[0])
    loo_spread = max(abs(value - intercept) for value in loo_intercepts)
    weight_shift = abs(intercept - complex(unweighted_coefficients[0]))
    maximum_residual = float(np.max(np.abs(residuals)))
    maximum_normalized_residual = float(np.max(np.abs(residuals) / radii))
    envelope = base_disk + loo_spread + weight_shift + maximum_residual
    return {
        "design": design,
        "weighted_coefficients": weighted_coefficients,
        "unweighted_coefficients": unweighted_coefficients,
        "predictions": predictions,
        "residuals": residuals,
        "intercept": intercept,
        "input_disk": input_disk,
        "a_disk": a_disk,
        "c_disk": c_disk,
        "base_disk": base_disk,
        "loo_spread": loo_spread,
        "weight_shift": weight_shift,
        "maximum_residual": maximum_residual,
        "maximum_normalized_residual": maximum_normalized_residual,
        "envelope": envelope,
        "relative_envelope": envelope / max(abs(intercept), 1.0e-300),
    }


def sampled_event_atlas() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    zero_rows = {row["event_id"]: row for row in read_csv(ZERO_EVENTS_5358)}
    scan_rows = [
        row
        for row in read_csv(SCAN_5337)
        if float(row["epsilon"]) <= EPSILON_ATLAS_MAXIMUM
    ]
    samples: list[dict[str, Any]] = []
    for event_id in EVENT_IDS:
        zero = zero_rows[event_id]
        samples.append(
            {
                "epsilon_id": "E000",
                "epsilon": 0.0,
                "event_id": event_id,
                "event_type": zero["event_type"],
                "event_coordinate": float(
                    zero["zero_regulator_absolute_soft_cosine"]
                ),
                "coordinate_disk_radius": float(
                    zero["coordinate_bracket_width"]
                )
                / 2.0,
                "near_transverse_slope_magnitude": float(
                    zero["minimum_local_scalar_derivative"]
                ),
                "local_half_nearest_event_gap": math.nan,
                "regulator_width_over_half_gap": 0.0,
                "event_contract_passes": parse_bool(
                    zero["valid_for_D4_zero_regulator_local_event_continuation"]
                ),
                "sample_class": "ZERO_ANALYTIC_EVENT",
            }
        )
    for row in scan_rows:
        samples.append(
            {
                "epsilon_id": row["epsilon_id"],
                "epsilon": float(row["epsilon"]),
                "event_id": row["event_id"],
                "event_type": row["event_type"],
                "event_coordinate": float(row["event_coordinate"]),
                "coordinate_disk_radius": EVENT_ROOT_RADIUS,
                "near_transverse_slope_magnitude": float(
                    row["near_transverse_slope_magnitude"]
                ),
                "local_half_nearest_event_gap": float(
                    row["local_half_nearest_event_gap"]
                ),
                "regulator_width_over_half_gap": float(
                    row["eta_regulator_width_over_half_gap"]
                ),
                "event_contract_passes": parse_bool(
                    row["targeted_event_contract_passes"]
                ),
                "sample_class": "POSITIVE_REGULATOR_TARGETED_SCAN",
            }
        )
    zero_coordinates = {
        event_id: next(
            row["event_coordinate"]
            for row in samples
            if row["event_id"] == event_id and row["epsilon"] == 0.0
        )
        for event_id in EVENT_IDS
    }
    tubes: list[dict[str, Any]] = []
    for order_index, event_id in enumerate(COORDINATE_ORDER):
        local = [row for row in samples if row["event_id"] == event_id]
        zero_coordinate = zero_coordinates[event_id]
        neighbor_gaps: list[float] = []
        if order_index > 0:
            neighbor_gaps.append(
                zero_coordinate - zero_coordinates[COORDINATE_ORDER[order_index - 1]]
            )
        if order_index + 1 < len(COORDINATE_ORDER):
            neighbor_gaps.append(
                zero_coordinates[COORDINATE_ORDER[order_index + 1]] - zero_coordinate
            )
        nearest_zero_gap = min(neighbor_gaps)
        half_width = 0.2 * nearest_zero_gap
        maximum_displacement = max(
            abs(row["event_coordinate"] - zero_coordinate)
            + row["coordinate_disk_radius"]
            for row in local
        )
        tubes.append(
            {
                "event_id": event_id,
                "event_type": local[0]["event_type"],
                "coordinate_order_index": order_index + 1,
                "zero_event_coordinate": zero_coordinate,
                "nearest_zero_event_gap": nearest_zero_gap,
                "fixed_tube_half_width": half_width,
                "fixed_tube_lower": zero_coordinate - half_width,
                "fixed_tube_upper": zero_coordinate + half_width,
                "maximum_sampled_coordinate_displacement_with_disk": maximum_displacement,
                "sampled_displacement_fraction_of_tube": maximum_displacement
                / half_width,
                "minimum_sampled_transverse_slope": min(
                    row["near_transverse_slope_magnitude"] for row in local
                ),
                "maximum_sampled_regulator_width_over_half_gap": max(
                    row["regulator_width_over_half_gap"] for row in local
                ),
                "sample_count": len(local),
                "all_samples_inside_fixed_tube": all(
                    zero_coordinate - half_width
                    < row["event_coordinate"] - row["coordinate_disk_radius"]
                    and row["event_coordinate"] + row["coordinate_disk_radius"]
                    < zero_coordinate + half_width
                    for row in local
                ),
                "valid_for_closed_interval_atlas": False,
            }
        )
    return samples, tubes


def contract_rows(claims: dict[str, bool]) -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "EC5377_00_exact_full_endpoint_coefficient",
            "premises": "r=z0/z1 and the exact primitive has lower logarithmic coefficient H=-s[C0 r-(C1/2)r^2]",
            "derived_statement": "K(e)=H(e)/e equals the stored leading coefficient -s C0 r/e plus the previously omitted finite-e correction +(s C1/2)r^2/e",
            "status": "EXACT_ALGEBRA_RECONSTRUCTED_AT_SIX_RUNGS",
            **claims,
        },
        {
            "contract_id": "EC5377_01_second_log_coefficient",
            "premises": "H(0)=0 and H(e)=A e+C_log e^2+O(e^3)",
            "derived_statement": "C_log=K'(0)=H''(0)/2",
            "status": "EXACT_DERIVATIVE_IDENTITY",
            **claims,
        },
        {
            "contract_id": "EC5377_02_parent_derivative_formula",
            "premises": "r(0)=0",
            "derived_statement": "C_log,e=-s[C0' r'+(C0/2)r''-(C1/2)(r')^2] at e=0",
            "status": "EXACT_ALGEBRA_PARENT_DERIVATIVE_TARGET",
            **claims,
        },
        {
            "contract_id": "EC5377_03_numeric_candidate_boundary",
            "premises": "six finite-e normal forms reconstruct K but no interval enclosure of their derivatives is available",
            "derived_statement": "the anchored slope is a source-backed C_log candidate and sensitivity input, not yet the regulator-zero coefficient theorem",
            "status": "CANDIDATE_NOT_LIMIT_CLAIM",
            **claims,
        },
        {
            "contract_id": "EC5377_04_sampled_atlas_boundary",
            "premises": "zero plus six positive-regulator scans preserve eight ordered transverse events inside disjoint fixed tubes",
            "derived_statement": "the tubes are a candidate fixed atlas; unsampled epsilon still requires interval Newton or an equivalent continuation certificate",
            "status": "SAMPLED_ATLAS_NOT_CLOSED_INTERVAL_PROOF",
            **claims,
        },
        {
            "contract_id": "EC5377_05_claim_boundary",
            "premises": "fixed-A,C numerical compatibility does not supply H3, G3 or W3",
            "derived_statement": "no endpoint-C limit, common interval, uniform remainder or D4 outer-limit claim follows",
            "status": "ENFORCED",
            **claims,
        },
    ]


def render_document(payload: dict[str, Any]) -> None:
    lines = [
        "# 5377 - D4 full endpoint C reconstruction and fixed-A,C gate",
        "",
        "## Decision",
        "",
        f"`{payload['decision']}`",
        "",
        "The exact endpoint primitive was reconstructed at all six coefficient rungs with the full lower-log coefficient",
        "",
        "`H=-s[C0(z0/z1)-(C1/2)(z0/z1)^2]`.",
        "",
        "The first term reproduces every stored 5357 event coefficient. The second term is not optional at order epsilon squared. Defining `K=H/epsilon` gives the exact identity `C_log=K'(0)=H''(0)/2`, and event by event",
        "",
        "`C_log,e=-s[C0' r'+(C0/2)r''-(C1/2)(r')^2]`, with `r=z0/z1`.",
        "",
        "## Numerical reconstruction",
        "",
        f"- full-primitive C candidate: `{payload['C_log_candidate_real']} {payload['C_log_candidate_imaginary']:+} i`;",
        f"- conservative candidate diagnostic disk: `{payload['C_log_candidate_diagnostic_disk']}`;",
        f"- fixed-A,C maximum normalized integral residual: `{payload['fixed_A_C_maximum_normalized_residual']}`;",
        f"- fixed-A,C relative intercept envelope: `{payload['fixed_A_C_relative_intercept_envelope']}`;",
        f"- unchanged one-percent comparison: `{payload['relative_intercept_limit']}`.",
        "",
        "Fixing this parent candidate removes the freely fitted `C epsilon^2 Log epsilon` direction. The seven integrated rungs remain comfortably inside their conservative disks. This is a useful compatibility result, but the finite-rung slope is not relabeled as the exact zero-regulator derivative.",
        "",
        "## Event atlas",
        "",
        f"All eight events retain their source ordering across `{payload['sampled_event_rung_count']}` sampled regulator values from zero through `{payload['sampled_atlas_epsilon_maximum']}`. Their fixed candidate tubes are disjoint, the largest sampled displacement occupies `{payload['maximum_sampled_event_tube_fraction']}` of its tube, and the minimum sampled transverse slope is `{payload['minimum_sampled_transverse_slope']}`.",
        "",
        "The next proof is now sharply defined: interval-certify those tubes, evaluate the parent derivative formula for C at zero, and enclose H3. Until that is done, the common-interval atlas, endpoint-C limit, uniform remainder, D4 outer limit and all broader claims remain false.",
    ]
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    temporary.replace(DOCUMENT)


def execute() -> dict[str, Any]:
    required = direct_source_paths()
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(missing)
    parent_5375 = read_json(RESULT_5375)
    parent_5376 = read_json(RESULT_5376)
    source_a = complex(
        float(parent_5375["derived_A_real"]),
        float(parent_5375["derived_A_imaginary"]),
    )
    source_a_radius = float(parent_5375["derived_A_disk_radius"])
    event_rows, rung_rows = reconstruct_rungs()
    C_rows, selected_C, C_disk = build_C_models(
        rung_rows, source_a, source_a_radius
    )
    source_c = complex(selected_C["slope"])
    inputs = M5373.load_inputs()
    AC = fixed_AC_fit(
        inputs, source_a, source_a_radius, source_c, C_disk
    )
    samples, tubes = sampled_event_atlas()
    coordinate_orders = {
        row["epsilon_id"]: tuple(
            item["event_id"]
            for item in sorted(
                [sample for sample in samples if sample["epsilon_id"] == row["epsilon_id"]],
                key=lambda item: item["event_coordinate"],
            )
        )
        for row in samples
    }
    sampled_atlas_passes = (
        len(samples) == 56
        and len(tubes) == 8
        and all(order == COORDINATE_ORDER for order in coordinate_orders.values())
        and all(row["event_contract_passes"] for row in samples)
        and all(row["all_samples_inside_fixed_tube"] for row in tubes)
        and all(
            tubes[index]["fixed_tube_upper"]
            < tubes[index + 1]["fixed_tube_lower"]
            for index in range(len(tubes) - 1)
        )
    )
    reconstruction_passes = (
        len(event_rows) == 48
        and len(rung_rows) == 6
        and all(row["coefficient_contract_passes"] for row in event_rows)
        and max(row["stored_leading_A_identity_error"] for row in event_rows)
        <= 1.0e-12
        and all(row["event_count"] == 8 for row in rung_rows)
    )
    C_candidate_passes = (
        reconstruction_passes
        and math.isfinite(source_c.real)
        and math.isfinite(source_c.imag)
        and math.isfinite(C_disk)
        and C_disk > 0.0
        and selected_C["maximum_remainder_quotient"] > 0.0
    )
    parent_fixed_A_intercept = complex(
        float(parent_5375["fixed_A_intercept_real"]),
        float(parent_5375["fixed_A_intercept_imaginary"]),
    )
    intercept_shift = abs(AC["intercept"] - parent_fixed_A_intercept)
    fixed_AC_passes = (
        C_candidate_passes
        and AC["maximum_normalized_residual"] <= 1.0
        and AC["relative_envelope"] <= RELATIVE_INTERCEPT_LIMIT
        and intercept_shift
        <= AC["envelope"] + float(parent_5375["fixed_A_conservative_envelope"])
    )
    validation_paths = [
        VALIDATION_5357,
        VALIDATION_5358,
        VALIDATION_5359,
        VALIDATION_5373,
        VALIDATION_5375,
        VALIDATION_5376,
    ] + [
        spec[key]
        for spec in RUNG_SPECS
        for key in ("support_validation", "branch_validation")
        if str(spec[key]).lower().endswith(".csv")
    ]
    parent_sources = {
        "5337": source_register_current(SOURCES_5337),
        "5357": source_register_current(SOURCES_5357),
        "5358": source_register_current(SOURCES_5358),
        "5359": source_register_current(SOURCES_5359),
        "5373": source_register_current(SOURCES_5373),
        "5375": source_register_current(SOURCES_5375),
        "5376": source_register_current(SOURCES_5376),
    }
    allowed_legacy_drift_suffixes = (
        "/scripts/y5_r2fr_5334_d4_outer_regulator_ladder_controller.py",
        "/source-intake/functional_rg/5334/e0025/d4_outer_event_aligned_e0025_result.json",
    )
    legacy_source_audit_passes = all(
        all(
            str(drift).replace("\\", "/").lower().endswith(
                allowed_legacy_drift_suffixes
            )
            for drift in parent_sources[key][2]
        )
        for key in ("5337", "5358")
    )
    current_primary_sources_pass = all(
        parent_sources[key][0] and parent_sources[key][1] > 0
        for key in ("5357", "5359", "5373", "5375", "5376")
    )
    validations = [
        validation_row(
            "parent_validations_and_primary_source_registers_are_current",
            all(csv_passes(path) for path in validation_paths)
            and current_primary_sources_pass
            and legacy_source_audit_passes,
            {
                "drifts": {key: value[2] for key, value in parent_sources.items()},
                "allowed_legacy_suffixes": allowed_legacy_drift_suffixes,
            },
        ),
        validation_row(
            "full_six_rung_eight_event_primitive_reconstruction_closes",
            reconstruction_passes,
            {
                "event_rows": len(event_rows),
                "maximum_leading_identity_error": max(
                    row["stored_leading_A_identity_error"] for row in event_rows
                ),
            },
        ),
        validation_row(
            "full_endpoint_C_candidate_is_numeric_and_source_backed",
            C_candidate_passes,
            {"C": source_c, "disk": C_disk},
        ),
        validation_row(
            "fixed_A_C_seven_rung_branch_is_numerically_compatible",
            fixed_AC_passes,
            {
                "maximum_normalized_residual": AC[
                    "maximum_normalized_residual"
                ],
                "relative_envelope": AC["relative_envelope"],
                "intercept_shift": intercept_shift,
            },
        ),
        validation_row(
            "zero_to_E020_sampled_event_atlas_preserves_order_and_tubes",
            sampled_atlas_passes,
            {
                "sample_count": len(samples),
                "maximum_tube_fraction": max(
                    row["sampled_displacement_fraction_of_tube"] for row in tubes
                ),
            },
        ),
        validation_row(
            "closed_interval_C_H3_and_outer_limit_claims_remain_false",
            parent_5376.get("numeric_H3_available") is False
            and parent_5376.get("numeric_uniform_M_D4_available") is False,
            false_claims(),
        ),
        validation_row(
            "formal_workbench_unchanged",
            M5370.formal_inventory_digest() == FORMAL_DIGEST,
            M5370.formal_inventory_digest(),
        ),
        validation_row(
            "scripts_cache_absent",
            not (SCRIPTS / "__pycache__").exists(),
            SCRIPTS / "__pycache__",
        ),
    ]
    artifact_passed = all(parse_bool(row["passed"]) for row in validations)
    claims = {
        CLAIM_RECONSTRUCTION: artifact_passed and reconstruction_passes,
        CLAIM_SAMPLED_ATLAS: artifact_passed and sampled_atlas_passes,
        CLAIM_C_CANDIDATE: artifact_passed and C_candidate_passes,
        CLAIM_FIXED_AC: artifact_passed and fixed_AC_passes,
        **false_claims(),
    }
    for rows in (event_rows, rung_rows, C_rows, samples, tubes):
        for row in rows:
            row.update(claims)
    fit_names = ("I0", "B_scaled", "D_scaled")
    fit_rows = [
        {
            "coefficient": name,
            **complex_fields(
                "weighted_value", complex(AC["weighted_coefficients"][index])
            ),
            **complex_fields(
                "unweighted_value", complex(AC["unweighted_coefficients"][index])
            ),
            **claims,
        }
        for index, name in enumerate(fit_names)
    ]
    residual_rows = [
        {
            "epsilon_id": input_row["epsilon_id"],
            "epsilon": input_row["epsilon"],
            "input_disk_radius": input_row["radius"],
            **complex_fields("prediction", complex(AC["predictions"][index])),
            **complex_fields("residual", complex(AC["residuals"][index])),
            "normalized_residual": abs(AC["residuals"][index])
            / input_row["radius"],
            **claims,
        }
        for index, input_row in enumerate(inputs)
    ]
    contract = contract_rows(claims)
    maximum_tube_fraction = max(
        row["sampled_displacement_fraction_of_tube"] for row in tubes
    )
    minimum_slope = min(row["minimum_sampled_transverse_slope"] for row in tubes)
    sampled_rungs = len({row["epsilon_id"] for row in samples})
    payload = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "D4-full-endpoint-C-reconstruction-and-fixed-A-C-gate",
        "validation_passed": artifact_passed,
        "decision": (
            "D4_FULL_ENDPOINT_C_CANDIDATE_RECONSTRUCTED__FIXED_A_C_BRANCH_COMPATIBLE__INTERVAL_PROOF_OPEN"
            if artifact_passed and fixed_AC_passes and sampled_atlas_passes
            else "D4_FULL_ENDPOINT_C_RECONSTRUCTION_OR_FIXED_A_C_GATE_BLOCKED"
        ),
        **complex_fields("derived_A", source_a),
        "derived_A_disk_radius": source_a_radius,
        **complex_fields("C_log_candidate", source_c),
        "C_log_candidate_diagnostic_disk": C_disk,
        "C_log_candidate_is_regulator_zero_limit": False,
        **complex_fields("fixed_A_C_intercept", AC["intercept"]),
        "fixed_A_C_input_disk": AC["input_disk"],
        "fixed_A_C_correlated_A_disk": AC["a_disk"],
        "fixed_A_C_correlated_C_candidate_disk": AC["c_disk"],
        "fixed_A_C_base_estimator_disk": AC["base_disk"],
        "fixed_A_C_leave_one_out_spread": AC["loo_spread"],
        "fixed_A_C_weighted_unweighted_shift": AC["weight_shift"],
        "fixed_A_C_maximum_absolute_residual": AC["maximum_residual"],
        "fixed_A_C_maximum_normalized_residual": AC[
            "maximum_normalized_residual"
        ],
        "fixed_A_C_intercept_envelope": AC["envelope"],
        "fixed_A_C_relative_intercept_envelope": AC["relative_envelope"],
        "relative_intercept_limit": RELATIVE_INTERCEPT_LIMIT,
        "fixed_A_C_intercept_shift_from_fixed_A_parent": intercept_shift,
        "sampled_event_rung_count": sampled_rungs,
        "sampled_event_sample_count": len(samples),
        "sampled_atlas_epsilon_maximum": EPSILON_ATLAS_MAXIMUM,
        "maximum_sampled_event_tube_fraction": maximum_tube_fraction,
        "minimum_sampled_transverse_slope": minimum_slope,
        "common_closed_interval_atlas_proved": False,
        "numeric_H3_available": False,
        "claim_boundary": claims,
        "remaining_obstruction": "replace the finite-rung C slope by the zero-event parent derivative evaluation, then interval-Newton certify the eight fixed tubes and enclose H3 before attacking mapped-away W3",
        "formalization_workbench_modified_file_count": 0,
        "updated_utc": utc_now(),
    }
    atomic_csv(EVENT_RECONSTRUCTION, event_rows)
    atomic_csv(RUNG_TOTALS, rung_rows)
    atomic_csv(C_STABILITY, C_rows)
    atomic_csv(EVENT_SAMPLES, samples)
    atomic_csv(EVENT_TUBES, tubes)
    atomic_csv(FIXED_AC_FIT, fit_rows)
    atomic_csv(FIXED_AC_RESIDUALS, residual_rows)
    atomic_csv(CONTRACT, contract)
    atomic_csv(VALIDATION, validations)
    atomic_csv(RESIDUAL_VALIDATION, validations)
    atomic_json(RESULT, payload)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "complete" if artifact_passed else "blocked",
            "decision": payload["decision"],
            "updated_utc": payload["updated_utc"],
        },
    )
    render_document(payload)
    generated = (
        EVENT_RECONSTRUCTION,
        RUNG_TOTALS,
        C_STABILITY,
        EVENT_SAMPLES,
        EVENT_TUBES,
        FIXED_AC_FIT,
        FIXED_AC_RESIDUALS,
        CONTRACT,
        VALIDATION,
        RESULT,
        DOCUMENT,
    )
    source_rows = [
        {
            "path": str(path.resolve()),
            "sha256": digest(path),
            "exists": True,
            **claims,
        }
        for path in tuple(dict.fromkeys((*required, *generated)))
    ]
    atomic_csv(SOURCE_REGISTER, source_rows)
    return payload


def validate_saved() -> dict[str, Any]:
    required = (
        EVENT_RECONSTRUCTION,
        RUNG_TOTALS,
        C_STABILITY,
        EVENT_SAMPLES,
        EVENT_TUBES,
        FIXED_AC_FIT,
        FIXED_AC_RESIDUALS,
        CONTRACT,
        RESULT,
        VALIDATION,
        SOURCE_REGISTER,
        DOCUMENT,
    )
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(missing)
    payload = read_json(RESULT)
    sources = source_register_current(SOURCE_REGISTER)
    checks = {
        "saved_result_passes": payload.get("validation_passed") is True,
        "saved_validation_rows_pass": csv_passes(VALIDATION),
        "saved_sources_are_current": sources[0] and sources[1] > 0,
        "full_primitive_reconstruction_claimed": payload.get(
            "claim_boundary", {}
        ).get(CLAIM_RECONSTRUCTION)
        is True,
        "fixed_A_C_conditional_stability_claimed": payload.get(
            "claim_boundary", {}
        ).get(CLAIM_FIXED_AC)
        is True,
        "closed_interval_and_broad_claims_remain_false": all(
            payload.get("claim_boundary", {}).get(field) is False
            for field in FALSE_CLAIMS
        ),
        "formal_workbench_unchanged": M5370.formal_inventory_digest()
        == FORMAL_DIGEST,
        "scripts_cache_absent": not (SCRIPTS / "__pycache__").exists(),
    }
    return {
        "validation_passed": all(checks.values()),
        "decision": (
            "D4_FULL_ENDPOINT_C_RECONSTRUCTION_AND_FIXED_A_C_GATE_VALIDATED"
            if all(checks.values())
            else "D4_FULL_ENDPOINT_C_RECONSTRUCTION_VALIDATION_FAILED"
        ),
        "checks": checks,
        "source_drifts": sources[2],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("run", "validate"), default="run")
    arguments = parser.parse_args()
    set_below_normal_priority()
    payload = execute() if arguments.mode == "run" else validate_saved()
    print(json.dumps(normalize(payload), indent=2, sort_keys=True, allow_nan=False))
    return 0 if payload.get("validation_passed") else 1


if __name__ == "__main__":
    raise SystemExit(main())
