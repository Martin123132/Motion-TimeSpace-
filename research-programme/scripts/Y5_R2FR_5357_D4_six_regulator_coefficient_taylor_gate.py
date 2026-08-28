from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import time
from typing import Any, Callable


os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")
sys.dont_write_bytecode = True

import numpy as np


POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / "5357"
EPSILON_REFERENCE = 0.0025
RELATIVE_ENVELOPE_LIMIT = 0.01

SCRIPT_5345 = SCRIPTS / "Y5_R2FR_5345_D4_regulator_zero_normal_form_preregistration.py"
DOC_5345 = POST / "5345-Y5-R2FR-D4-regulator-zero-endpoint-asymptotic-and-fit-preregistration.md"
RESULT_5345 = FUNCTIONAL_RG / "5345" / "D4_regulator_zero_preregistration_result.json"
CONTRACT_5345 = FUNCTIONAL_RG / "5345" / "D4_regulator_zero_endpoint_asymptotic_contract.csv"
RUNG_GATE_5345 = FUNCTIONAL_RG / "5345" / "D4_zero_rung_count_gate.csv"
SCRIPT_5354 = SCRIPTS / "Y5_R2FR_5354_D4_E0025_four_regulator_affine_holdout_gate.py"
DOC_5354 = POST / "5354-Y5-R2FR-D4-E0025-four-regulator-affine-holdout-gate.md"
RESULT_5354 = FUNCTIONAL_RG / "5354" / "E0025" / "affine-holdout" / "D4_E0025_four_regulator_affine_holdout_result.json"
SCRIPT_5355 = SCRIPTS / "Y5_R2FR_5355_D4_higher_rung_event_geometry_and_removable_singularity.py"
RESULT_5355 = FUNCTIONAL_RG / "5355" / "D4_higher_rung_event_geometry_result.json"
CONTRACT_5355 = FUNCTIONAL_RG / "5355" / "D4_endpoint_coefficient_removable_singularity_contract.csv"
SCRIPT_5356 = SCRIPTS / "Y5_R2FR_5356_D4_E010_E020_coefficient_extractor.py"

CLAIM_STABILITY = "valid_for_D4_six_regulator_quadratic_endpoint_coefficient_stability"
CLAIM_INTERCEPT = "valid_for_D4_six_regulator_nonzero_endpoint_intercept_diagnostic"
CLAIM_LIMIT = "valid_for_D4_endpoint_coefficient_regulator_zero_limit"
FALSE_CLAIMS = (
    CLAIM_LIMIT,
    "valid_for_D4_integral_six_rung_complete_second_order_fit",
    "valid_for_D4_outer_regulator_zero_limit",
    "valid_for_decay_angle_integral",
    "valid_for_full_angular_convergence",
    "valid_for_full_phase_space_coefficient",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)

RESULT_SPECS = (
    (
        "E000625",
        0.000625,
        FUNCTIONAL_RG / "5347" / "E000625" / "all-eight" / "D4_E000625_all_eight_endpoint_result.json",
        FUNCTIONAL_RG / "5347" / "E000625" / "all-eight" / "D4_E000625_all_eight_endpoint_validation.csv",
    ),
    (
        "E00125",
        0.00125,
        FUNCTIONAL_RG / "5346" / "E00125" / "D4_E00125_all_eight_endpoint_result.json",
        FUNCTIONAL_RG / "5346" / "E00125" / "D4_E00125_all_eight_endpoint_validation.csv",
    ),
    (
        "E0025",
        0.0025,
        FUNCTIONAL_RG / "5353" / "E0025" / "all-eight" / "D4_E0025_all_eight_endpoint_result.json",
        FUNCTIONAL_RG / "5353" / "E0025" / "all-eight" / "D4_E0025_all_eight_endpoint_validation.csv",
    ),
    (
        "E005",
        0.005,
        FUNCTIONAL_RG / "5347" / "E005" / "all-eight" / "D4_E005_all_eight_endpoint_result.json",
        FUNCTIONAL_RG / "5347" / "E005" / "all-eight" / "D4_E005_all_eight_endpoint_validation.csv",
    ),
    (
        "E010",
        0.01,
        FUNCTIONAL_RG / "5356" / "E010" / "all-eight" / "D4_E010_all_eight_endpoint_result.json",
        FUNCTIONAL_RG / "5356" / "E010" / "all-eight" / "D4_E010_all_eight_endpoint_validation.csv",
    ),
    (
        "E020",
        0.02,
        FUNCTIONAL_RG / "5356" / "E020" / "all-eight" / "D4_E020_all_eight_endpoint_result.json",
        FUNCTIONAL_RG / "5356" / "E020" / "all-eight" / "D4_E020_all_eight_endpoint_validation.csv",
    ),
)

KNOWN_HISTORICAL_RECURSIVE_FAILURE_SUFFIXES = (
    "scripts/y5_r2fr_5297_order8_exact_component_singularity_atlas.py",
    "source-intake/functional_rg/5297/order8_exact_component_atlas_result.json",
    "source-intake/functional_rg/5224/frozen_replacement_config.json",
)
HISTORICAL_REFINEMENT_IDS = {"E0025", "E010", "E020"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes"}


def finite_number(value: Any) -> bool:
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        fields.extend(key for key in row if key not in fields)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def validation_row(gate: str, passed: bool, detail: Any) -> dict[str, Any]:
    return {"gate": gate, "passed": bool(passed), "detail": str(detail)}


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return {
        f"{prefix}_real": float(value.real),
        f"{prefix}_imaginary": float(value.imag),
        f"{prefix}_magnitude": float(abs(value)),
    }


def source_chain_current(
    path: Path,
    visited: set[Path] | None = None,
) -> tuple[bool, int, list[str]]:
    resolved = path.resolve()
    visited = set() if visited is None else visited
    if resolved in visited:
        return True, 0, []
    visited.add(resolved)
    if not resolved.is_file():
        return False, 0, [f"missing:{resolved}"]
    if resolved.suffix.lower() != ".json":
        return True, 0, []
    try:
        payload = read_json(resolved)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return False, 0, [f"unreadable_json:{resolved}"]
    rows = payload.get("source_files", [])
    if not isinstance(rows, list):
        return False, 0, [f"malformed_source_files:{resolved}"]
    count = 0
    failures: list[str] = []
    for row in rows:
        source = Path(str(row.get("path", "")))
        expected = str(row.get("sha256", ""))
        if not source.is_file():
            failures.append(f"missing:{source}")
            continue
        if len(expected) != 64 or digest(source) != expected:
            failures.append(f"stale:{source}")
            continue
        count += 1
        nested_current, nested_count, nested_failures = source_chain_current(
            source,
            visited,
        )
        count += nested_count
        if not nested_current:
            failures.extend(nested_failures)
    return not failures, count, failures


def direct_source_chain_current(path: Path) -> tuple[bool, int, list[str]]:
    payload = read_json(path)
    rows = payload.get("source_files", [])
    if not isinstance(rows, list) or not rows:
        return False, 0, [f"missing_or_malformed_direct_source_files:{path}"]
    failures: list[str] = []
    count = 0
    for row in rows:
        source = Path(str(row.get("path", "")))
        expected = str(row.get("sha256", ""))
        if not source.is_file():
            failures.append(f"missing:{source}")
        elif len(expected) != 64 or digest(source) != expected:
            failures.append(f"stale:{source}")
        else:
            count += 1
    return not failures, count, failures


def historical_recursive_failures_are_exactly_known(
    epsilon_id: str,
    failures: list[str],
) -> bool:
    if epsilon_id not in HISTORICAL_REFINEMENT_IDS or not failures:
        return False
    for failure in failures:
        normalized = failure.replace("\\", "/").lower()
        if normalized.startswith("missing:") or not any(
            normalized.endswith(suffix)
            for suffix in KNOWN_HISTORICAL_RECURSIVE_FAILURE_SUFFIXES
        ):
            return False
    return True


def coefficient_claim(epsilon_id: str) -> str:
    return f"valid_for_D4_{epsilon_id}_all_eight_endpoint_coefficients"


def load_inputs() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for epsilon_id, expected_epsilon, result_path, validation_path in RESULT_SPECS:
        payload = read_json(result_path)
        validation = read_csv(validation_path)
        recursive_current, recursive_count, recursive_failures = source_chain_current(
            result_path
        )
        direct_current, direct_count, direct_failures = direct_source_chain_current(
            result_path
        )
        historical_failures_known = historical_recursive_failures_are_exactly_known(
            epsilon_id,
            recursive_failures,
        )
        recursive_audit_passes = recursive_current or (
            direct_current and historical_failures_known
        )
        value = complex(
            float(payload["A_total_finite_epsilon_estimator_real"]),
            float(payload["A_total_finite_epsilon_estimator_imaginary"]),
        )
        radius = float(payload["A_total_diagnostic_disk_radius"])
        claim = coefficient_claim(epsilon_id)
        contract_passes = (
            payload.get("validation_passed") is True
            and payload.get("claim_boundary", {}).get(claim) is True
            and payload.get("epsilon_id") == epsilon_id
            and abs(float(payload.get("epsilon")) - expected_epsilon) <= 1.0e-15
            and finite_number(value.real)
            and finite_number(value.imag)
            and finite_number(radius)
            and radius > 0.0
            and bool(validation)
            and all(parse_bool(item.get("passed")) for item in validation)
        )
        rows.append(
            {
                "epsilon_id": epsilon_id,
                "epsilon": expected_epsilon,
                "value": value,
                "radius": radius,
                "input_contract_passes": contract_passes,
                "recursive_source_chain_passes": recursive_current,
                "recursive_source_count": recursive_count,
                "recursive_source_failures": recursive_failures,
                "direct_source_chain_passes": direct_current,
                "direct_source_count": direct_count,
                "direct_source_failures": direct_failures,
                "historical_recursive_failures_exactly_known": historical_failures_known,
                "recursive_source_audit_passes": recursive_audit_passes,
                "formalization_workbench_modified_file_count": payload.get(
                    "formalization_workbench_modified_file_count"
                ),
                "result_path": result_path,
                "validation_path": validation_path,
                "result_sha256": digest(result_path),
            }
        )
    context = {
        "preregistration": read_json(RESULT_5345),
        "holdout": read_json(RESULT_5354),
        "removable": read_json(RESULT_5355),
        "removable_contract": read_csv(CONTRACT_5355),
    }
    return rows, context


def design_matrix(u: np.ndarray, family: str) -> np.ndarray:
    if family == "affine":
        return np.column_stack((np.ones(len(u)), u))
    if family == "quadratic":
        return np.column_stack((np.ones(len(u)), u, u**2))
    if family == "half_power_falsifier":
        return np.column_stack((np.ones(len(u)), np.sqrt(u), u))
    raise ValueError(family)


def basis_labels(family: str) -> list[str]:
    if family == "affine":
        return ["1", "u"]
    if family == "quadratic":
        return ["1", "u", "u^2"]
    if family == "half_power_falsifier":
        return ["1", "sqrt(u)", "u"]
    raise ValueError(family)


def fit_model(
    inputs: list[dict[str, Any]],
    indices: list[int],
    family: str,
    weighted: bool,
    model_id: str,
) -> dict[str, Any]:
    epsilon = np.array([inputs[index]["epsilon"] for index in indices], dtype=float)
    values = np.array([inputs[index]["value"] for index in indices], dtype=complex)
    radii = np.array([inputs[index]["radius"] for index in indices], dtype=float)
    u = epsilon / EPSILON_REFERENCE
    matrix = design_matrix(u, family)
    weights = 1.0 / radii**2 if weighted else np.ones(len(indices))
    square_root_weights = np.sqrt(weights)
    weighted_matrix = matrix * square_root_weights[:, None]
    weighted_values = values * square_root_weights
    coefficients, _, rank, singular_values = np.linalg.lstsq(
        weighted_matrix,
        weighted_values,
        rcond=None,
    )
    normal_inverse = np.linalg.inv(matrix.T @ (weights[:, None] * matrix))
    estimator = normal_inverse @ (matrix.T * weights)
    predictions = matrix @ coefficients
    residuals = values - predictions
    normalized_residuals = np.abs(residuals) / radii
    intercept_disk_radius = float(np.sum(np.abs(estimator[0]) * radii))
    coefficient_rows = [
        {
            "basis": label,
            **complex_fields("coefficient", complex(value)),
        }
        for label, value in zip(basis_labels(family), coefficients)
    ]
    return {
        "model_id": model_id,
        "family": family,
        "weighted": weighted,
        "indices": indices,
        "epsilon_ids": [inputs[index]["epsilon_id"] for index in indices],
        "parameter_count_complex": len(coefficients),
        "residual_degrees_of_freedom_complex": len(indices) - len(coefficients),
        "rank": int(rank),
        "full_rank": int(rank) == len(coefficients),
        "condition_number": float(np.linalg.cond(weighted_matrix)),
        "smallest_singular_value": float(singular_values[-1]),
        "coefficients": coefficients,
        "coefficient_rows": coefficient_rows,
        "intercept": complex(coefficients[0]),
        "intercept_disk_radius": intercept_disk_radius,
        "predictions": predictions,
        "residuals": residuals,
        "normalized_residuals": normalized_residuals,
        "maximum_absolute_residual": float(np.max(np.abs(residuals))),
        "maximum_normalized_residual": float(np.max(normalized_residuals)),
        "rms_normalized_residual": float(
            math.sqrt(float(np.mean(normalized_residuals**2)))
        ),
    }


def model_row(model: dict[str, Any], selected: bool) -> dict[str, Any]:
    return {
        "model_id": model["model_id"],
        "family": model["family"],
        "basis_variable": "u=epsilon/0.0025",
        "weighted_by_inverse_disk_radius_squared": model["weighted"],
        "epsilon_ids": "|".join(model["epsilon_ids"]),
        "rung_count": len(model["indices"]),
        "parameter_count_complex": model["parameter_count_complex"],
        "residual_degrees_of_freedom_complex": model[
            "residual_degrees_of_freedom_complex"
        ],
        "full_rank": model["full_rank"],
        "condition_number": model["condition_number"],
        "coefficients_json": json.dumps(model["coefficient_rows"], sort_keys=True),
        **complex_fields("intercept", model["intercept"]),
        "intercept_input_disk_radius": model["intercept_disk_radius"],
        "maximum_absolute_residual": model["maximum_absolute_residual"],
        "maximum_normalized_complex_residual": model[
            "maximum_normalized_residual"
        ],
        "rms_normalized_complex_residual": model["rms_normalized_residual"],
        "selected_for_intercept_envelope": selected,
        "valid_for_D4_endpoint_coefficient_regulator_zero_limit": False,
    }


def residual_rows(
    model: dict[str, Any], inputs: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for local_index, input_index in enumerate(model["indices"]):
        residual = complex(model["residuals"][local_index])
        prediction = complex(model["predictions"][local_index])
        source = inputs[input_index]
        rows.append(
            {
                "model_id": model["model_id"],
                "epsilon_id": source["epsilon_id"],
                "epsilon": source["epsilon"],
                **complex_fields("prediction", prediction),
                **complex_fields("residual", residual),
                "input_disk_radius": source["radius"],
                "normalized_complex_residual": float(
                    model["normalized_residuals"][local_index]
                ),
                "residual_inside_input_disk": float(
                    model["normalized_residuals"][local_index]
                )
                <= 1.0,
            }
        )
    return rows


def model_contract_rows() -> list[dict[str, Any]]:
    common = {
        "valid_for_D4_endpoint_coefficient_regulator_zero_limit": False,
        "valid_for_D4_outer_regulator_zero_limit": False,
    }
    return [
        {
            "contract_id": "MC5357_01_integral_family_boundary",
            "source_statement": "checkpoint 5345 derives I_D4=I0+A*e*Log(e/e_ref)+B*e+C*e^2*Log(e/e_ref)+D*e^2+O(e^3 Log e)",
            "derived_statement": "the five-complex-parameter family applies to integrated D4 values, not endpoint-log coefficients",
            "status": "CATEGORY_BOUNDARY_ENFORCED",
            **common,
        },
        {
            "contract_id": "MC5357_02_coefficient_family",
            "source_statement": "A_e(e)=-s_e*C0_e(e)*z0_e(e)/(e*z1_e(e))",
            "derived_statement": "if z0_e/e, C0_e and 1/z1_e are analytic at zero, A_total(e)=A0+A1*e+A2*e^2+O(e^3)",
            "status": "SOURCE_DERIVED_CONDITIONAL_TAYLOR_FAMILY",
            **common,
        },
        {
            "contract_id": "MC5357_03_rung_count",
            "source_statement": "the coefficient second-order family has three complex parameters",
            "derived_statement": "six accepted coefficient rungs leave three complex residual degrees of freedom",
            "status": "OVERDETERMINED_DESIGN",
            **common,
        },
        {
            "contract_id": "MC5357_04_frozen_diagnostics",
            "source_statement": "checkpoint 5345 freezes weighted/unweighted, leave-one-out, smallest-window, normalized-residual, model-shift and half-power diagnostics with a 1 percent envelope limit",
            "derived_statement": "the same diagnostics and threshold are applied without using coefficient rows as fake integral values",
            "status": "INHERITED_ACCEPTANCE_DISCIPLINE",
            **common,
        },
        {
            "contract_id": "MC5357_05_zero_proof_boundary",
            "source_statement": "checkpoint 5355 leaves the zero-regulator collision Jacobian unsigned",
            "derived_statement": "a passing six-rung coefficient fit is numerical stability evidence, not a proof of the removable zero limit",
            "status": "ZERO_LIMIT_BLOCKED_PENDING_JACOBIAN",
            **common,
        },
    ]


def source_rows(paths: list[Path]) -> list[dict[str, Any]]:
    return [
        {
            "path": str(path.resolve()),
            "sha256": digest(path),
            "exists": True,
            "valid_for_D4_endpoint_coefficient_regulator_zero_limit": False,
            "valid_for_D4_outer_regulator_zero_limit": False,
            "valid_for_full_MTS_claim": False,
        }
        for path in paths
    ]


def preflight() -> dict[str, Any]:
    required = [
        Path(__file__),
        SCRIPT_5345,
        DOC_5345,
        RESULT_5345,
        CONTRACT_5345,
        RUNG_GATE_5345,
        SCRIPT_5354,
        DOC_5354,
        RESULT_5354,
        SCRIPT_5355,
        RESULT_5355,
        CONTRACT_5355,
        SCRIPT_5356,
    ]
    for _, _, result_path, validation_path in RESULT_SPECS:
        required.extend((result_path, validation_path))
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        return {"all_pass": False, "missing": missing}
    inputs, context = load_inputs()
    acceptance = context["preregistration"].get("acceptance_contract", {})
    removable_rows = {
        row["contract_id"]: row for row in context["removable_contract"]
    }
    checks = {
        "all_input_paths_exist": not missing,
        "exactly_six_ordered_regulator_rungs": [
            row["epsilon_id"] for row in inputs
        ]
        == [spec[0] for spec in RESULT_SPECS],
        "all_six_coefficient_results_are_accepted": all(
            row["input_contract_passes"] for row in inputs
        ),
        "all_six_direct_source_chains_are_current": all(
            row["direct_source_chain_passes"] for row in inputs
        ),
        "strict_recursive_drifts_are_exactly_delimited": all(
            row["recursive_source_chain_passes"]
            or row["historical_recursive_failures_exactly_known"]
            for row in inputs
        ),
        "frozen_diagnostics_and_threshold_match_5345": acceptance.get(
            "minimum_complete_second_order_overdetermined_rungs"
        )
        == 6
        and acceptance.get("relative_zero_bound_limit")
        == RELATIVE_ENVELOPE_LIMIT
        and len(acceptance.get("required_diagnostics", [])) == 6,
        "5345_family_is_explicitly_integral_not_coefficient": str(
            context["preregistration"].get("derived_complete_second_order_family", "")
        ).startswith("I0+A*e*Log"),
        "5354_selected_two_additional_regulator_rungs": context["holdout"].get(
            "next_required_gate"
        )
        == "SOURCE_DERIVED_REMAINDER_BOUND_OR_TWO_ADDITIONAL_REGULATOR_RUNGS",
        "removable_coefficient_law_is_source_recorded": removable_rows.get(
            "AC5355_05_removable_coefficient", {}
        ).get("source_statement")
        == "A_e(epsilon)=-s_e*C0_e(epsilon)*z0_e(epsilon)/(epsilon*z1_e(epsilon))",
        "zero_collision_jacobian_remains_unsigned": context["removable"].get(
            "zero_regulator_collision_jacobian_signed"
        )
        is False,
        "formal_workbench_unchanged_in_inputs": all(
            row["formalization_workbench_modified_file_count"] in (0, None)
            for row in inputs
        ),
        "scripts_cache_absent": not (SCRIPTS / "__pycache__").exists(),
    }
    return {
        "all_pass": all(checks.values()),
        "checks": checks,
        "inputs": inputs,
        "context": context,
        "required": required,
    }


def run(output: Path) -> dict[str, Any]:
    started = time.perf_counter()
    state = preflight()
    if not state.get("all_pass"):
        raise RuntimeError(json.dumps(state, default=str, indent=2))
    inputs = state["inputs"]
    all_indices = list(range(len(inputs)))
    affine_weighted = fit_model(
        inputs, all_indices, "affine", True, "AFFINE_WEIGHTED_ALL_SIX"
    )
    affine_unweighted = fit_model(
        inputs, all_indices, "affine", False, "AFFINE_UNWEIGHTED_ALL_SIX"
    )
    quadratic_weighted = fit_model(
        inputs, all_indices, "quadratic", True, "QUADRATIC_WEIGHTED_ALL_SIX"
    )
    quadratic_unweighted = fit_model(
        inputs, all_indices, "quadratic", False, "QUADRATIC_UNWEIGHTED_ALL_SIX"
    )
    smallest_window = fit_model(
        inputs,
        list(range(4)),
        "quadratic",
        True,
        "QUADRATIC_WEIGHTED_SMALLEST_FOUR",
    )
    half_power = fit_model(
        inputs,
        all_indices,
        "half_power_falsifier",
        True,
        "HALF_POWER_WEIGHTED_FALSIFIER",
    )
    models = [
        affine_weighted,
        affine_unweighted,
        quadratic_weighted,
        quadratic_unweighted,
        smallest_window,
        half_power,
    ]
    leave_one_out: list[dict[str, Any]] = []
    leave_one_out_models: list[dict[str, Any]] = []
    for held_out in all_indices:
        retained = [index for index in all_indices if index != held_out]
        model = fit_model(
            inputs,
            retained,
            "quadratic",
            True,
            f"QUADRATIC_WEIGHTED_LOO_{inputs[held_out]['epsilon_id']}",
        )
        leave_one_out_models.append(model)
        shift = abs(model["intercept"] - quadratic_weighted["intercept"])
        leave_one_out.append(
            {
                "held_out_epsilon_id": inputs[held_out]["epsilon_id"],
                **complex_fields("intercept", model["intercept"]),
                "intercept_input_disk_radius": model["intercept_disk_radius"],
                "intercept_shift_from_all_six_weighted": float(shift),
                "maximum_normalized_complex_residual_on_training_rows": model[
                    "maximum_normalized_residual"
                ],
                "valid_for_D4_endpoint_coefficient_regulator_zero_limit": False,
            }
        )

    diagnostic_models = models + leave_one_out_models
    input_disk_component = max(
        model["intercept_disk_radius"]
        for model in diagnostic_models
        if model["family"] != "half_power_falsifier"
    )
    envelope_components = [
        {
            "component": "maximum_analytic_fit_input_disk_propagation",
            "radius": input_disk_component,
        },
        {
            "component": "weighted_unweighted_quadratic_intercept_shift",
            "radius": float(
                abs(
                    quadratic_weighted["intercept"]
                    - quadratic_unweighted["intercept"]
                )
            ),
        },
        {
            "component": "leave_one_out_quadratic_intercept_spread",
            "radius": max(
                row["intercept_shift_from_all_six_weighted"]
                for row in leave_one_out
            ),
        },
        {
            "component": "smallest_epsilon_window_intercept_shift",
            "radius": float(
                abs(
                    smallest_window["intercept"]
                    - quadratic_weighted["intercept"]
                )
            ),
        },
        {
            "component": "affine_quadratic_intercept_shift",
            "radius": float(
                abs(
                    affine_weighted["intercept"]
                    - quadratic_weighted["intercept"]
                )
            ),
        },
        {
            "component": "maximum_selected_absolute_complex_residual",
            "radius": quadratic_weighted["maximum_absolute_residual"],
        },
    ]
    envelope_radius = math.fsum(row["radius"] for row in envelope_components)
    intercept = quadratic_weighted["intercept"]
    relative_envelope = envelope_radius / abs(intercept)
    for row in envelope_components:
        row["fraction_of_intercept_magnitude"] = row["radius"] / abs(intercept)
        row["valid_for_D4_endpoint_coefficient_regulator_zero_limit"] = False

    input_rows = []
    for row in inputs:
        input_rows.append(
            {
                "epsilon_id": row["epsilon_id"],
                "epsilon": row["epsilon"],
                **complex_fields("A_finite_epsilon", row["value"]),
                "A_diagnostic_disk_radius": row["radius"],
                "input_contract_passes": row["input_contract_passes"],
                "recursive_source_chain_passes": row[
                    "recursive_source_chain_passes"
                ],
                "recursive_source_count": row["recursive_source_count"],
                "recursive_source_failures": "|".join(
                    row["recursive_source_failures"]
                ),
                "direct_source_chain_passes": row["direct_source_chain_passes"],
                "direct_source_count": row["direct_source_count"],
                "direct_source_failures": "|".join(row["direct_source_failures"]),
                "historical_recursive_failures_exactly_known": row[
                    "historical_recursive_failures_exactly_known"
                ],
                "recursive_source_audit_passes": row[
                    "recursive_source_audit_passes"
                ],
                "result_path": str(row["result_path"].resolve()),
                "result_sha256": row["result_sha256"],
                "valid_for_D4_endpoint_coefficient_regulator_zero_limit": False,
            }
        )

    model_rows = [
        model_row(model, model is quadratic_weighted) for model in models
    ]
    selected_residuals = []
    for model in (affine_weighted, quadratic_weighted, half_power):
        selected_residuals.extend(residual_rows(model, inputs))

    sources = source_rows(state["required"])
    required_diagnostics = {
        "weighted_and_unweighted_intercepts": True,
        "leave_one_out_intercept_spread": len(leave_one_out) == 6,
        "smallest_epsilon_window_stability": len(smallest_window["indices"]) == 4,
        "normalized_complex_residuals": len(selected_residuals) == 18,
        "leading_versus_second_order_intercept_envelope": True,
        "half_power_falsifier_reported_but_not_selected": half_power["family"]
        == "half_power_falsifier",
    }
    stability_passes = (
        quadratic_weighted["full_rank"]
        and quadratic_weighted["residual_degrees_of_freedom_complex"] == 3
        and quadratic_weighted["maximum_normalized_residual"] <= 1.0
        and relative_envelope < RELATIVE_ENVELOPE_LIMIT
    )
    intercept_nonzero = abs(intercept) > envelope_radius
    gates = [
        validation_row("preflight_passes", state["all_pass"], state["checks"]),
        validation_row(
            "all_sources_exist_and_are_hashed",
            all(row["exists"] and len(row["sha256"]) == 64 for row in sources),
            len(sources),
        ),
        validation_row(
            "six_independent_accepted_coefficient_disks",
            len(inputs) == 6
            and all(
                row["input_contract_passes"]
                and row["direct_source_chain_passes"]
                and row["recursive_source_audit_passes"]
                for row in inputs
            ),
            "|".join(row["epsilon_id"] for row in inputs),
        ),
        validation_row(
            "integral_and_coefficient_model_families_are_separated",
            True,
            "5345 integral log family is not fitted to endpoint coefficients",
        ),
        validation_row(
            "coefficient_quadratic_design_is_overdetermined_and_full_rank",
            quadratic_weighted["full_rank"]
            and quadratic_weighted["residual_degrees_of_freedom_complex"] == 3,
            quadratic_weighted["condition_number"],
        ),
        validation_row(
            "weighted_quadratic_residuals_fit_all_input_disks",
            quadratic_weighted["maximum_normalized_residual"] <= 1.0,
            quadratic_weighted["maximum_normalized_residual"],
        ),
        validation_row(
            "all_frozen_5345_diagnostics_are_materialized",
            all(required_diagnostics.values()),
            required_diagnostics,
        ),
        validation_row(
            "conservative_relative_intercept_envelope_is_below_one_percent",
            relative_envelope < RELATIVE_ENVELOPE_LIMIT,
            relative_envelope,
        ),
        validation_row(
            "intercept_diagnostic_disk_excludes_zero",
            intercept_nonzero,
            abs(intercept) - envelope_radius,
        ),
        validation_row(
            "half_power_falsifier_is_reported_but_not_selected",
            half_power["family"] == "half_power_falsifier",
            half_power["maximum_normalized_residual"],
        ),
        validation_row(
            "zero_collision_jacobian_remains_unsigned",
            state["checks"]["zero_collision_jacobian_remains_unsigned"],
            False,
        ),
        validation_row(
            "integral_complete_family_fit_remains_unclaimed",
            True,
            "no six-rung integrated I_D4 values exist in this checkpoint",
        ),
        validation_row(
            "formal_workbench_unchanged",
            state["checks"]["formal_workbench_unchanged_in_inputs"],
            0,
        ),
        validation_row(
            "scripts_cache_absent",
            not (SCRIPTS / "__pycache__").exists(),
            SCRIPTS / "__pycache__",
        ),
    ]
    validation_passed = all(bool(row["passed"]) for row in gates)
    claims = {claim: False for claim in FALSE_CLAIMS}
    claims[CLAIM_STABILITY] = validation_passed and stability_passes
    claims[CLAIM_INTERCEPT] = validation_passed and intercept_nonzero
    decision = (
        "D4_SIX_RUNG_COEFFICIENT_TAYLOR_STABILITY_PASSES__PROVE_ZERO_COLLISION_JACOBIAN"
        if claims[CLAIM_STABILITY]
        else "D4_SIX_RUNG_COEFFICIENT_TAYLOR_GATE_BLOCKED"
    )

    atomic_csv(output / "D4_six_regulator_coefficient_inputs.csv", input_rows)
    atomic_csv(output / "D4_coefficient_integral_model_boundary_contract.csv", model_contract_rows())
    atomic_csv(output / "D4_six_regulator_coefficient_models.csv", model_rows)
    atomic_csv(output / "D4_six_regulator_coefficient_residuals.csv", selected_residuals)
    atomic_csv(output / "D4_six_regulator_coefficient_leave_one_out.csv", leave_one_out)
    atomic_csv(output / "D4_six_regulator_intercept_envelope.csv", envelope_components)
    atomic_csv(output / "source_register.csv", sources)
    atomic_csv(output / "D4_six_regulator_coefficient_validation.csv", gates)
    result = {
        "mode": "D4-six-regulator-endpoint-coefficient-Taylor-stability-gate",
        "validation_passed": validation_passed,
        "decision": decision,
        "epsilon_reference": EPSILON_REFERENCE,
        "accepted_epsilon_ids": [row["epsilon_id"] for row in inputs],
        "accepted_epsilon_values": [row["epsilon"] for row in inputs],
        "coefficient_model": "A(epsilon)=A0+A1*(epsilon/epsilon_ref)+A2*(epsilon/epsilon_ref)^2+O(epsilon^3)",
        "coefficient_model_status": "SOURCE_DERIVED_CONDITIONAL_ON_ZERO_REGULATOR_SIMPLE_ROOTS",
        "integral_model_not_fitted": "I_D4=I0+A*e*Log(e/e_ref)+B*e+C*e^2*Log(e/e_ref)+D*e^2",
        "selected_model_id": quadratic_weighted["model_id"],
        **complex_fields("selected_intercept", intercept),
        "selected_intercept_input_disk_radius": quadratic_weighted[
            "intercept_disk_radius"
        ],
        "conservative_intercept_envelope_radius": envelope_radius,
        "conservative_relative_intercept_envelope": relative_envelope,
        "relative_intercept_envelope_limit": RELATIVE_ENVELOPE_LIMIT,
        "selected_model_maximum_normalized_complex_residual": quadratic_weighted[
            "maximum_normalized_residual"
        ],
        "half_power_falsifier_maximum_normalized_complex_residual": half_power[
            "maximum_normalized_residual"
        ],
        "half_power_falsifier_data_discriminates": half_power[
            "maximum_normalized_residual"
        ]
        > 1.0,
        "zero_regulator_collision_jacobian_signed": False,
        "coefficient_regulator_zero_limit_complete": False,
        "integrated_D4_six_rung_fit_complete": False,
        "strict_recursive_source_chains_current": all(
            row["recursive_source_chain_passes"] for row in inputs
        ),
        "historical_recursive_source_failures": {
            row["epsilon_id"]: row["recursive_source_failures"]
            for row in inputs
            if row["recursive_source_failures"]
        },
        "formalization_workbench_modified_file_count": 0,
        "claim_boundary": claims,
        "source_files": sources,
        "runtime_seconds": time.perf_counter() - started,
        "updated_utc": utc_now(),
    }
    atomic_json(output / "D4_six_regulator_coefficient_result.json", result)
    atomic_json(
        output / "status.json",
        {
            "state": "COMPLETE" if validation_passed else "BLOCKED",
            "decision": decision,
            "validation_passed": validation_passed,
            "updated_utc": utc_now(),
        },
    )
    return result


def self_test() -> dict[str, Any]:
    synthetic: list[dict[str, Any]] = []
    for index, epsilon in enumerate((0.001, 0.002, 0.004, 0.008, 0.016, 0.032)):
        u = epsilon / EPSILON_REFERENCE
        value = (2.0 + 3.0j) + (0.5 - 0.25j) * u + (0.1 + 0.2j) * u**2
        synthetic.append(
            {
                "epsilon_id": f"S{index}",
                "epsilon": epsilon,
                "value": value,
                "radius": 1.0e-6,
            }
        )
    model = fit_model(
        synthetic,
        list(range(6)),
        "quadratic",
        True,
        "SYNTHETIC_QUADRATIC",
    )
    checks = {
        "quadratic_intercept_recovered": abs(model["intercept"] - (2.0 + 3.0j))
        <= 1.0e-10,
        "quadratic_residual_is_zero_to_roundoff": model[
            "maximum_absolute_residual"
        ]
        <= 1.0e-10,
        "quadratic_design_is_overdetermined": model[
            "residual_degrees_of_freedom_complex"
        ]
        == 3,
    }
    return {"all_pass": all(checks.values()), "checks": checks}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=OUTPUT)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args()
    if arguments.self_test:
        result = self_test()
    elif arguments.dry_run:
        state = preflight()
        result = {
            "mode": "preflight",
            "all_pass": state.get("all_pass", False),
            "checks": state.get("checks", {}),
            "missing": state.get("missing", []),
            "valid_for_D4_endpoint_coefficient_regulator_zero_limit": False,
            "valid_for_D4_outer_regulator_zero_limit": False,
            "valid_for_full_MTS_claim": False,
        }
    else:
        result = run(arguments.output_dir.resolve())
    print(json.dumps(result, indent=2, sort_keys=True, default=str))
    return 0 if result.get("all_pass", result.get("validation_passed", False)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
