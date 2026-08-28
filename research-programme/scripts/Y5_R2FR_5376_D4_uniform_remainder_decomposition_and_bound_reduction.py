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

SCRIPT_5357 = SCRIPTS / "Y5_R2FR_5357_D4_six_regulator_coefficient_taylor_gate.py"
SCRIPT_5359 = SCRIPTS / "Y5_R2FR_5359_D4_zero_regulator_endpoint_coefficient_limit.py"
SCRIPT_5360 = SCRIPTS / "Y5_R2FR_5360_D4_derived_A_subtraction_and_E005_holdout_preregistration.py"
SCRIPT_5373 = SCRIPTS / "Y5_R2FR_5373_D4_seven_rung_extended_window_stability_gate.py"
SCRIPT_5375 = SCRIPTS / "Y5_R2FR_5375_D4_derived_A_primary_role_separation_gate.py"

INPUTS_5357 = FUNCTIONAL_RG / "5357" / "D4_six_regulator_coefficient_inputs.csv"
MODELS_5357 = FUNCTIONAL_RG / "5357" / "D4_six_regulator_coefficient_models.csv"
RESULT_5357 = FUNCTIONAL_RG / "5357" / "D4_six_regulator_coefficient_result.json"
VALIDATION_5357 = FUNCTIONAL_RG / "5357" / "D4_six_regulator_coefficient_validation.csv"
SOURCES_5357 = FUNCTIONAL_RG / "5357" / "source_register.csv"

ENDPOINTS_5359 = FUNCTIONAL_RG / "5359" / "D4_zero_regulator_endpoint_coefficients.csv"
RESULT_5359 = FUNCTIONAL_RG / "5359" / "D4_zero_regulator_endpoint_result.json"
VALIDATION_5359 = FUNCTIONAL_RG / "5359" / "D4_zero_regulator_endpoint_validation.csv"
SOURCES_5359 = FUNCTIONAL_RG / "5359" / "source_register.csv"

CONTRACT_5360 = FUNCTIONAL_RG / "5360" / "D4_fixed_A_integral_subtraction_contract.csv"
RESULT_5360 = FUNCTIONAL_RG / "5360" / "D4_fixed_A_subtraction_result.json"
VALIDATION_5360 = FUNCTIONAL_RG / "5360" / "D4_fixed_A_subtraction_validation.csv"
SOURCES_5360 = FUNCTIONAL_RG / "5360" / "source_register.csv"

INPUTS_5373 = FUNCTIONAL_RG / "5373" / "D4_seven_rung_inputs.csv"
RESIDUALS_5373 = FUNCTIONAL_RG / "5373" / "D4_seven_rung_model_residuals.csv"
RESULT_5373 = FUNCTIONAL_RG / "5373" / "D4_seven_rung_extended_window_result.json"
VALIDATION_5373 = FUNCTIONAL_RG / "5373" / "D4_seven_rung_extended_window_validation.csv"
SOURCES_5373 = FUNCTIONAL_RG / "5373" / "source_register.csv"

RESULT_5375 = FUNCTIONAL_RG / "5375" / "D4_derived_A_primary_role_result.json"
VALIDATION_5375 = FUNCTIONAL_RG / "5375" / "D4_derived_A_primary_role_validation.csv"
SOURCES_5375 = FUNCTIONAL_RG / "5375" / "source_register.csv"

OUTPUT = FUNCTIONAL_RG / "5376"
DECOMPOSITION = OUTPUT / "D4_selected_leaf_component_decomposition.csv"
CANCELLATION = OUTPUT / "D4_raw_partition_dyadic_cancellation.csv"
TOTAL_QUOTIENTS = OUTPUT / "D4_discrete_total_remainder_quotients.csv"
ENDPOINT_LOG_BOUND = OUTPUT / "D4_leading_endpoint_log_coefficient_discrete_diagnostic.csv"
THEOREM = OUTPUT / "D4_uniform_remainder_derivative_contract.csv"
RESULT = OUTPUT / "D4_uniform_remainder_reduction_result.json"
VALIDATION = OUTPUT / "D4_uniform_remainder_reduction_validation.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
STATUS = OUTPUT / "status.json"
RESIDUAL_VALIDATION = MTS_RESIDUALS / "P8_Y5_BRR545_5376_VALIDATION.csv"
DOCUMENT = POST / "5376-Y5-R2FR-D4-uniform-remainder-decomposition-and-bound-reduction.md"

CHECKPOINT = 5376
MARKER = "MTS_5376_D4_UNIFORM_REMAINDER_DECOMPOSITION_AND_BOUND_REDUCTION"
REVISION = "D4-uniform-remainder-invariant-decomposition-v1"
EPSILON_REFERENCE = 0.0025
FORMAL_DIGEST = "0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f"

CLAIM_DECOMPOSITION = "valid_for_D4_selected_leaf_component_decomposition"
CLAIM_NONINVARIANCE = "valid_for_D4_raw_pole_regular_split_noninvariance"
CLAIM_REDUCTION = "valid_for_D4_uniform_remainder_derivative_reduction"
CLAIM_TOTAL_DIAGNOSTIC = "valid_for_D4_discrete_total_remainder_diagnostic"
CLAIM_LOG_DIAGNOSTIC = (
    "valid_for_D4_discrete_leading_endpoint_log_coefficient_diagnostic"
)
FALSE_CLAIMS = (
    "valid_for_D4_numeric_uniform_remainder_bound",
    "valid_for_D4_outer_regulator_zero_limit",
    "valid_for_decay_angle_integral",
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
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


M5375 = load_module("mts_5375_for_5376", SCRIPT_5375)
M5373 = M5375.M5373
M5370 = M5375.M5370
np = M5370.np


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def set_below_normal_priority() -> None:
    M5375.set_below_normal_priority()


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
    if isinstance(value, dict):
        return {str(key): normalize(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [normalize(item) for item in value]
    if hasattr(value, "item"):
        return normalize(value.item())
    if isinstance(value, complex):
        return {"real": float(value.real), "imaginary": float(value.imag)}
    return value


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(normalize(payload), indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return {
        f"{prefix}_real": float(value.real),
        f"{prefix}_imaginary": float(value.imag),
        f"{prefix}_magnitude": float(abs(value)),
    }


def validation_row(gate: str, passed: bool, detail: Any) -> dict[str, Any]:
    return {"gate": gate, "passed": bool(passed), "detail": str(detail)}


def csv_passes(path: Path) -> bool:
    rows = read_csv(path)
    return bool(rows) and all(parse_bool(row["passed"]) for row in rows)


def source_register_current(path: Path) -> tuple[bool, int, list[str]]:
    rows = read_csv(path)
    drifts: list[str] = []
    for row in rows:
        source = Path(row["path"])
        if not source.is_file() or digest(source) != row["sha256"]:
            drifts.append(str(source))
    return not drifts, len(rows), drifts


def false_claims() -> dict[str, bool]:
    return {field: False for field in FALSE_CLAIMS}


def rung_paths(epsilon_id: str) -> dict[str, Path]:
    root = FUNCTIONAL_RG / "5334" / epsilon_id
    stem = f"D4_outer_event_aligned_{epsilon_id}"
    return {
        "cells": root / f"{stem}_cell_integrals.csv",
        "manifest": root / f"{stem}_node_manifest.csv",
        "panels": root / f"{stem}_adaptive_panels.csv",
        "result": root / f"{stem}_result.json",
        "validation": root / f"{stem}_validation.csv",
    }


def direct_source_paths(inputs: list[dict[str, Any]]) -> tuple[Path, ...]:
    paths: list[Path] = [
        Path(__file__).resolve(),
        SCRIPT_5357,
        SCRIPT_5359,
        SCRIPT_5360,
        SCRIPT_5373,
        SCRIPT_5375,
        INPUTS_5357,
        MODELS_5357,
        RESULT_5357,
        VALIDATION_5357,
        SOURCES_5357,
        ENDPOINTS_5359,
        RESULT_5359,
        VALIDATION_5359,
        SOURCES_5359,
        CONTRACT_5360,
        RESULT_5360,
        VALIDATION_5360,
        SOURCES_5360,
        INPUTS_5373,
        RESIDUALS_5373,
        RESULT_5373,
        VALIDATION_5373,
        SOURCES_5373,
        RESULT_5375,
        VALIDATION_5375,
        SOURCES_5375,
    ]
    for row in inputs:
        paths.extend(rung_paths(row["epsilon_id"]).values())
        paths.append(Path(row["source_path"]))
    return tuple(dict.fromkeys(paths))


def selected_leaf_decomposition(input_row: dict[str, Any]) -> tuple[dict[str, Any], float]:
    epsilon_id = input_row["epsilon_id"]
    paths = rung_paths(epsilon_id)
    leaves = {
        row["adaptive_panel_id"]
        for row in read_csv(paths["panels"])
        if parse_bool(row["adaptive_leaf"])
    }
    weights = {
        row["node_id"]: float(row["mapped_outer_weight"])
        for row in read_csv(paths["manifest"])
        if int(row["outer_order"]) == 8 and row["adaptive_panel_id"] in leaves
    }
    analytic = 0.0j
    regular = 0.0j
    corrected = 0.0j
    selected_cells = 0
    selected_nodes: set[str] = set()
    maximum_cell_identity_error = 0.0
    material_cells = 0
    for row in read_csv(paths["cells"]):
        if (
            int(row["outer_order"]) != 8
            or int(row["energy_order"]) != 8
            or row["node_id"] not in weights
        ):
            continue
        weight = weights[row["node_id"]]
        cell_analytic = complex(
            float(row["analytic_pole_integral_real"]),
            float(row["analytic_pole_integral_imaginary"]),
        )
        cell_regular = complex(
            float(row["regularized_numeric_integral_real"]),
            float(row["regularized_numeric_integral_imaginary"]),
        )
        cell_corrected = complex(
            float(row["pole_corrected_integral_real"]),
            float(row["pole_corrected_integral_imaginary"]),
        )
        analytic += weight * cell_analytic
        regular += weight * cell_regular
        corrected += weight * cell_corrected
        maximum_cell_identity_error = max(
            maximum_cell_identity_error,
            abs(cell_corrected - cell_analytic - cell_regular),
        )
        selected_cells += 1
        selected_nodes.add(row["node_id"])
        material_cells += int(row["material_pole_count"]) > 0
    canonical = complex(input_row["value"])
    canonical_correction = canonical - corrected
    closure = analytic + regular + canonical_correction
    row = {
        "epsilon_id": epsilon_id,
        "epsilon": float(input_row["epsilon"]),
        "selected_leaf_count": len(leaves),
        "selected_outer_Q8_node_count": len(weights),
        "selected_nodes_with_cell_rows": len(selected_nodes),
        "selected_cell_count": selected_cells,
        "selected_material_pole_cell_count": material_cells,
        **complex_fields("analytic_pole_partition_component", analytic),
        **complex_fields("regularized_numeric_partition_component", regular),
        **complex_fields("raw_partition_sum", corrected),
        **complex_fields("canonical_postintegration_correction", canonical_correction),
        **complex_fields("canonical_integral", canonical),
        "canonical_input_disk_radius": float(input_row["radius"]),
        "maximum_cell_sum_identity_error": maximum_cell_identity_error,
        "component_closure_error": abs(closure - canonical),
        "raw_partition_cancellation_ratio": (
            (abs(analytic) + abs(regular)) / max(abs(corrected), 1.0e-300)
        ),
        "canonical_source_path": str(Path(input_row["source_path"]).resolve()),
        "cell_source_path": str(paths["cells"].resolve()),
        "manifest_source_path": str(paths["manifest"].resolve()),
        "panel_source_path": str(paths["panels"].resolve()),
    }
    return row, maximum_cell_identity_error


def component_value(row: dict[str, Any], prefix: str) -> complex:
    return complex(float(row[f"{prefix}_real"]), float(row[f"{prefix}_imaginary"]))


def dyadic_cancellation_rows(decomposition: list[dict[str, Any]]) -> list[dict[str, Any]]:
    prefixes = (
        "analytic_pole_partition_component",
        "regularized_numeric_partition_component",
        "canonical_postintegration_correction",
        "canonical_integral",
    )
    rows: list[dict[str, Any]] = []
    for index in range(2, len(decomposition)):
        first = decomposition[index - 2]
        second = decomposition[index - 1]
        current = decomposition[index]
        epsilon_first = float(first["epsilon"])
        epsilon_second = float(second["epsilon"])
        epsilon_current = float(current["epsilon"])
        ratio = (epsilon_current - epsilon_second) / (
            epsilon_second - epsilon_first
        )
        innovations: dict[str, complex] = {}
        for prefix in prefixes:
            first_value = component_value(first, prefix)
            second_value = component_value(second, prefix)
            current_value = component_value(current, prefix)
            prediction = second_value + ratio * (second_value - first_value)
            innovations[prefix] = current_value - prediction
        analytic = innovations["analytic_pole_partition_component"]
        regular = innovations["regularized_numeric_partition_component"]
        correction = innovations["canonical_postintegration_correction"]
        total = innovations["canonical_integral"]
        component_sum = analytic + regular + correction
        variation_sum = abs(analytic) + abs(regular) + abs(correction)
        opposition = (
            float((analytic * regular.conjugate()).real / (abs(analytic) * abs(regular)))
            if abs(analytic) > 0.0 and abs(regular) > 0.0
            else math.nan
        )
        rows.append(
            {
                "epsilon_id": current["epsilon_id"],
                "epsilon": epsilon_current,
                "dyadic_affine_prediction_ratio": ratio,
                **complex_fields("analytic_partition_innovation", analytic),
                **complex_fields("regular_partition_innovation", regular),
                **complex_fields("canonical_correction_innovation", correction),
                **complex_fields("canonical_total_innovation", total),
                "innovation_closure_error": abs(component_sum - total),
                "component_variation_sum": variation_sum,
                "component_to_total_innovation_ratio": variation_sum
                / max(abs(total), 1.0e-300),
                "analytic_regular_opposition_cosine": opposition,
                "fraction_cancelled_before_total": 1.0
                - abs(total) / max(variation_sum, 1.0e-300),
            }
        )
    return rows


def total_remainder_rows(
    inputs: list[dict[str, Any]], evaluation: dict[str, Any]
) -> list[dict[str, Any]]:
    fixed = evaluation["fixed"]
    source_a_radius = float(evaluation["source_a_radius"])
    rows: list[dict[str, Any]] = []
    for index, input_row in enumerate(inputs):
        epsilon = float(input_row["epsilon"])
        logarithm = math.log(epsilon / EPSILON_REFERENCE)
        scale = epsilon**3 * (1.0 + abs(logarithm))
        residual = complex(fixed["residuals"][index])
        input_disk = float(input_row["radius"])
        coefficient_disk = abs(epsilon * logarithm) * source_a_radius
        conservative_numerator = abs(residual) + input_disk + coefficient_disk
        rows.append(
            {
                "epsilon_id": input_row["epsilon_id"],
                "epsilon": epsilon,
                "absolute_logarithm": abs(logarithm),
                "remainder_scale_e3_one_plus_abs_log": scale,
                **complex_fields("fixed_A_central_residual", residual),
                "input_disk_radius": input_disk,
                "correlated_derived_A_disk_contribution": coefficient_disk,
                "central_discrete_remainder_quotient": abs(residual) / scale,
                "disk_inclusive_discrete_remainder_quotient": conservative_numerator
                / scale,
                "valid_only_at_sampled_rung": True,
                "valid_for_uniform_interval_bound": False,
            }
        )
    return rows


def endpoint_log_bound_rows(
    source_a: complex, source_a_radius: float
) -> tuple[list[dict[str, Any]], complex, complex, float, float, float]:
    inputs = read_csv(INPUTS_5357)
    epsilon = np.array([float(row["epsilon"]) for row in inputs], dtype=float)
    values = np.array(
        [
            complex(
                float(row["A_finite_epsilon_real"]),
                float(row["A_finite_epsilon_imaginary"]),
            )
            for row in inputs
        ],
        dtype=complex,
    )
    radii = np.array(
        [float(row["A_diagnostic_disk_radius"]) for row in inputs], dtype=float
    )
    effective_radii = radii + source_a_radius
    weights = 1.0 / effective_radii**2
    centered = values - source_a
    weighted_slope = complex(
        np.sum(weights * epsilon * centered) / np.sum(weights * epsilon**2)
    )
    unweighted_slope = complex(np.sum(epsilon * centered) / np.sum(epsilon**2))
    rows: list[dict[str, Any]] = []
    for index, input_row in enumerate(inputs):
        prediction = source_a + weighted_slope * epsilon[index]
        residual = complex(values[index] - prediction)
        disk_numerator = abs(residual) + effective_radii[index]
        rows.append(
            {
                "epsilon_id": input_row["epsilon_id"],
                "epsilon": epsilon[index],
                **complex_fields("A_finite_epsilon", complex(values[index])),
                "A_diagnostic_disk_radius": radii[index],
                **complex_fields("anchored_A0_plus_C_epsilon_prediction", prediction),
                **complex_fields("anchored_affine_residual", residual),
                "epsilon_squared": epsilon[index] ** 2,
                "central_leading_coefficient_affine_residual_quotient": abs(residual)
                / epsilon[index] ** 2,
                "disk_inclusive_leading_coefficient_affine_residual_quotient": disk_numerator
                / epsilon[index] ** 2,
                "valid_only_at_sampled_endpoint_coefficient_rung": True,
                "valid_for_uniform_interval_bound": False,
            }
        )
    model = next(
        row
        for row in read_csv(MODELS_5357)
        if row["model_id"] == "QUADRATIC_WEIGHTED_ALL_SIX"
    )
    coefficients = json.loads(model["coefficients_json"])
    coefficient_u2 = complex(
        float(coefficients[2]["coefficient_real"]),
        float(coefficients[2]["coefficient_imaginary"]),
    )
    quadratic_center_candidate = abs(coefficient_u2) / EPSILON_REFERENCE**2
    maximum_center = max(
        float(row["central_leading_coefficient_affine_residual_quotient"])
        for row in rows
    )
    maximum_disk = max(
        float(
            row[
                "disk_inclusive_leading_coefficient_affine_residual_quotient"
            ]
        )
        for row in rows
    )
    return (
        rows,
        weighted_slope,
        unweighted_slope,
        quadratic_center_candidate,
        maximum_center,
        maximum_disk,
    )


def theorem_rows(claims: dict[str, bool]) -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "UR5376_00_invariant_parent_split",
            "premises": "eight parent event branches are mapped to fixed local coordinates and the complement is mapped to finitely many fixed compact boxes",
            "derived_statement": "I(e)=sum_k[H_k(e) Log(e/e_ref)+G_k(e)]+W(e), with H_k and G_k C3 and W the mapped away integral",
            "bound_owner": "PARENT_FROZEN_EVENT_AND_AWAY_ATLAS",
            "numeric_uniform_bound_available": False,
            **claims,
        },
        {
            "contract_id": "UR5376_01_event_log_taylor_bound",
            "premises": "H=sum H_k, H(0)=0, H'(0)=A and H''(0)=2C",
            "derived_statement": "|H(e)-A e-C e^2| <= e^3 H3/6, H3=sum_k sup_[0,e_max]|H_k'''|",
            "bound_owner": "EIGHT_EVENT_LOG_COEFFICIENT_DERIVATIVES",
            "numeric_uniform_bound_available": False,
            **claims,
        },
        {
            "contract_id": "UR5376_02_event_regular_taylor_bound",
            "premises": "G=sum G_k is the nonlogarithmic part of the exact endpoint primitives",
            "derived_statement": "|G(e)-G(0)-G'(0)e-G''(0)e^2/2| <= e^3 G3/6, G3=sum_k sup_[0,e_max]|G_k'''|",
            "bound_owner": "EIGHT_EVENT_NONLOG_PRIMITIVE_DERIVATIVES",
            "numeric_uniform_bound_available": False,
            **claims,
        },
        {
            "contract_id": "UR5376_03_mapped_away_taylor_bound",
            "premises": "each moving away cell is pulled back to a fixed compact box U_a with mapped integrand f_a J_a",
            "derived_statement": "W3 <= sum_a Vol(U_a) sup_[U_a x 0,e_max]|partial_e^3(f_a J_a)| and |R_W3| <= e^3 W3/6",
            "bound_owner": "COMMON_COMPACT_AWAY_CELL_DERIVATIVE_ENCLOSURES",
            "numeric_uniform_bound_available": False,
            **claims,
        },
        {
            "contract_id": "UR5376_04_combined_constant",
            "premises": "the three preceding finite suprema have numeric enclosures",
            "derived_statement": "M_D4=max(H3,G3+W3)/6 implies |R3|<=M_D4 e^3[1+|Log(e/e_ref)|]",
            "bound_owner": "MAXIMUM_OF_LOG_AND_NONLOG_THIRD_DERIVATIVE_BOUNDS",
            "numeric_uniform_bound_available": False,
            **claims,
        },
        {
            "contract_id": "UR5376_05_raw_partition_noninvariance",
            "premises": "saved pole subtraction writes I=P+N but permits P->P+chi and N->N-chi for any finite analytic chi",
            "derived_statement": "P and N are bookkeeping components unless the parent freezes chi; only P+N and a parent-frozen event/away atlas can own a uniform bound",
            "bound_owner": "ALGEBRAIC_NONINVARIANCE_PROOF_PLUS_LEAF_CLOSURE_AUDIT",
            "numeric_uniform_bound_available": False,
            **claims,
        },
        {
            "contract_id": "UR5376_06_claim_boundary",
            "premises": "finite-rung quotients do not control unsampled epsilon and the H3, G3 and W3 suprema are not interval-enclosed",
            "derived_statement": "5376 reduces the proof to finite derivative owners but does not claim numeric M_D4 or the D4 regulator-zero limit",
            "bound_owner": "ENFORCED_NONCLAIM",
            "numeric_uniform_bound_available": False,
            **claims,
        },
    ]


def render_document(payload: dict[str, Any]) -> None:
    lines = [
        "# 5376 - D4 uniform-remainder decomposition and bound reduction",
        "",
        "## Decision",
        "",
        f"`{payload['decision']}`",
        "",
        "The accepted Q8/Q8 adaptive leaves were reconstructed for all seven integrated rungs. The saved analytic-pole and regular-numeric columns close back to the canonical integral after the recorded post-integration correction, but they are not separately invariant: adding any finite analytic chi to the pole subtraction and subtracting it from the regular part leaves the integral unchanged. Their large dyadic innovations visibly cancel, so neither raw column is allowed to masquerade as the physical remainder owner.",
        "",
        "## Exact reduction",
        "",
        "With a parent-frozen event/away atlas, write `I=sum_k[H_k Log(e/e_ref)+G_k]+W`. Taylor's theorem gives `H3=sum sup|H_k'''|`, `G3=sum sup|G_k'''|`, and a mapped-away bound `W3=sum Vol(U_a) sup|partial_e^3(f_a J_a)|`. Then",
        "",
        "`M_D4=max(H3,G3+W3)/6`,",
        "",
        "which is sufficient for `|R3|<=M_D4 e^3[1+|Log(e/e_ref)|]`. This is a finite calculational contract, not an existence-only phrase.",
        "",
        "## Diagnostics",
        "",
        f"- maximum raw-component/total dyadic innovation ratio: `{payload['maximum_component_to_total_innovation_ratio']}`;",
        f"- maximum central seven-rung remainder quotient: `{payload['maximum_central_total_discrete_quotient']}`;",
        f"- maximum disk-inclusive seven-rung quotient: `{payload['maximum_disk_inclusive_total_discrete_quotient']}`;",
        f"- leading-C0 coefficient quadratic centre candidate: `{payload['leading_endpoint_coefficient_quadratic_center_candidate']}`;",
        f"- leading-C0 coefficient disk-inclusive finite-rung diagnostic: `{payload['leading_endpoint_coefficient_maximum_disk_inclusive_discrete_quotient']}`.",
        "",
        "The 5357 leading-C0 sequence is comparatively mild, but it is not the full endpoint logarithmic coefficient beyond leading order. The exact primitive also contains `+(s C1/2)(z0/z1)^2`, which contributes at order epsilon squared and must be included when deriving C and H3. The total finite-rung quotient is dominated by the nearly epsilon-independent integration disks at the smallest rung; those disks do not scale as epsilon cubed and therefore cannot certify a uniform Taylor constant. Another blind small-epsilon rung would worsen that mismatch rather than prove the limit.",
        "",
        "## Next target",
        "",
        "Construct one common closed regulator interval and parent-frozen event/away atlas, then interval-enclose H3, G3 and W3. The away mapped-integrand derivative is now the main numerical owner; the raw pole/regular CSV split is retired as a proof route.",
        "",
        "The numeric uniform remainder, unconditional D4 regulator-zero, angular, phase-space, UV, local-GR and full-MTS claims remain false.",
    ]
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    temporary.replace(DOCUMENT)


def execute() -> dict[str, Any]:
    inputs = M5373.load_inputs()
    required = direct_source_paths(inputs)
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(missing)
    evaluation = M5370.evaluate(inputs)
    parent_5359 = read_json(RESULT_5359)
    parent_5360 = read_json(RESULT_5360)
    parent_5373 = read_json(RESULT_5373)
    parent_5375 = read_json(RESULT_5375)
    current_sources = {
        "5357": source_register_current(SOURCES_5357),
        "5359": source_register_current(SOURCES_5359),
        "5360": source_register_current(SOURCES_5360),
        "5373": source_register_current(SOURCES_5373),
        "5375": source_register_current(SOURCES_5375),
    }
    decomposition: list[dict[str, Any]] = []
    maximum_cell_identity_error = 0.0
    for input_row in inputs:
        row, cell_error = selected_leaf_decomposition(input_row)
        decomposition.append(row)
        maximum_cell_identity_error = max(maximum_cell_identity_error, cell_error)
    cancellation = dyadic_cancellation_rows(decomposition)
    total_quotients = total_remainder_rows(inputs, evaluation)
    source_a = complex(
        float(parent_5375["derived_A_real"]),
        float(parent_5375["derived_A_imaginary"]),
    )
    source_a_radius = float(parent_5375["derived_A_disk_radius"])
    (
        endpoint_rows,
        endpoint_slope,
        endpoint_unweighted_slope,
        endpoint_quadratic_candidate,
        endpoint_maximum_center,
        endpoint_maximum_disk,
    ) = endpoint_log_bound_rows(source_a, source_a_radius)
    maximum_total_center = max(
        float(row["central_discrete_remainder_quotient"])
        for row in total_quotients
    )
    maximum_total_disk = max(
        float(row["disk_inclusive_discrete_remainder_quotient"])
        for row in total_quotients
    )
    total_center_owner = max(
        total_quotients,
        key=lambda row: float(row["central_discrete_remainder_quotient"]),
    )["epsilon_id"]
    total_disk_owner = max(
        total_quotients,
        key=lambda row: float(row["disk_inclusive_discrete_remainder_quotient"]),
    )["epsilon_id"]
    maximum_innovation_ratio = max(
        float(row["component_to_total_innovation_ratio"]) for row in cancellation
    )
    maximum_cancelled_fraction = max(
        float(row["fraction_cancelled_before_total"]) for row in cancellation
    )
    decomposition_passes = (
        len(decomposition) == 7
        and all(row["selected_leaf_count"] > 0 for row in decomposition)
        and all(
            row["selected_outer_Q8_node_count"]
            == row["selected_nodes_with_cell_rows"]
            for row in decomposition
        )
        and maximum_cell_identity_error <= 1.0e-10
        and max(float(row["component_closure_error"]) for row in decomposition)
        <= 1.0e-12
    )
    cancellation_passes = (
        len(cancellation) == 5
        and max(float(row["innovation_closure_error"]) for row in cancellation)
        <= 1.0e-11
        and maximum_innovation_ratio > 1.0
    )
    endpoint_passes = (
        len(endpoint_rows) == 6
        and all(
            math.isfinite(
                float(row["central_leading_coefficient_affine_residual_quotient"])
            )
            for row in endpoint_rows
        )
        and all(
            math.isfinite(
                float(
                    row[
                        "disk_inclusive_leading_coefficient_affine_residual_quotient"
                    ]
                )
            )
            for row in endpoint_rows
        )
        and math.isfinite(endpoint_quadratic_candidate)
        and endpoint_maximum_disk >= endpoint_maximum_center >= 0.0
    )
    total_diagnostic_passes = (
        len(total_quotients) == 7
        and all(
            math.isfinite(float(row["disk_inclusive_discrete_remainder_quotient"]))
            for row in total_quotients
        )
        and maximum_total_disk >= maximum_total_center >= 0.0
    )
    parent_role_passes = (
        parent_5359.get("claim_boundary", {}).get(
            "valid_for_D4_endpoint_coefficient_regulator_zero_limit"
        )
        is True
        and parent_5360.get("claim_boundary", {}).get(
            "valid_for_D4_conditional_fixed_A_remainder_normal_form"
        )
        is True
        and parent_5373.get("claim_boundary", {}).get(
            "valid_for_D4_numeric_uniform_remainder_bound"
        )
        is False
        and parent_5375.get("uniform_numeric_remainder_bound_available") is False
    )
    validations = [
        validation_row(
            "all_parent_validations_and_direct_source_registers_are_current",
            all(
                csv_passes(path)
                for path in (
                    VALIDATION_5357,
                    VALIDATION_5359,
                    VALIDATION_5360,
                    VALIDATION_5373,
                    VALIDATION_5375,
                )
            )
            and all(value[0] and value[1] > 0 for value in current_sources.values()),
            {key: value[2] for key, value in current_sources.items()},
        ),
        validation_row(
            "seven_selected_leaf_Q8_Q8_decompositions_close",
            decomposition_passes,
            {
                "maximum_cell_identity_error": maximum_cell_identity_error,
                "maximum_closure_error": max(
                    float(row["component_closure_error"]) for row in decomposition
                ),
            },
        ),
        validation_row(
            "raw_partition_innovations_close_and_exhibit_cancellation",
            cancellation_passes,
            {
                "maximum_ratio": maximum_innovation_ratio,
                "maximum_cancelled_fraction": maximum_cancelled_fraction,
            },
        ),
        validation_row(
            "raw_pole_regular_split_is_algebraically_noninvariant",
            decomposition_passes and cancellation_passes,
            "P+N is invariant under P->P+chi, N->N-chi; P and N are not separate bound owners",
        ),
        validation_row(
            "leading_C0_endpoint_coefficient_finite_rung_diagnostic_is_numeric",
            endpoint_passes,
            {
                "weighted_C": endpoint_slope,
                "maximum_disk_quotient": endpoint_maximum_disk,
            },
        ),
        validation_row(
            "total_finite_rung_remainder_diagnostic_is_numeric",
            total_diagnostic_passes,
            {
                "maximum_center": maximum_total_center,
                "maximum_disk": maximum_total_disk,
            },
        ),
        validation_row(
            "uniform_remainder_is_reduced_to_H3_G3_W3_without_false_numeric_claim",
            parent_role_passes,
            "M_D4=max(H3,G3+W3)/6; all three require interval enclosures",
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
        CLAIM_DECOMPOSITION: artifact_passed and decomposition_passes,
        CLAIM_NONINVARIANCE: artifact_passed and cancellation_passes,
        CLAIM_REDUCTION: artifact_passed and parent_role_passes,
        CLAIM_TOTAL_DIAGNOSTIC: artifact_passed and total_diagnostic_passes,
        CLAIM_LOG_DIAGNOSTIC: artifact_passed and endpoint_passes,
        **false_claims(),
    }
    for rows in (decomposition, cancellation, total_quotients, endpoint_rows):
        for row in rows:
            row.update(claims)
    theorem = theorem_rows(claims)
    payload = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "D4-uniform-remainder-invariant-decomposition-and-bound-reduction",
        "validation_passed": artifact_passed,
        "decision": (
            "D4_REMAINDER_BOUND_REDUCED_TO_PARENT_FROZEN_EVENT_AND_AWAY_C3_ENCLOSURES__RAW_SPLIT_REJECTED"
            if artifact_passed
            else "D4_REMAINDER_DECOMPOSITION_OR_SOURCE_VALIDATION_BLOCKED"
        ),
        "selected_leaf_decomposition_rung_count": len(decomposition),
        "maximum_cell_sum_identity_error": maximum_cell_identity_error,
        "maximum_component_to_total_innovation_ratio": maximum_innovation_ratio,
        "maximum_cancelled_component_fraction": maximum_cancelled_fraction,
        "maximum_central_total_discrete_quotient": maximum_total_center,
        "maximum_central_total_discrete_quotient_owner": total_center_owner,
        "maximum_disk_inclusive_total_discrete_quotient": maximum_total_disk,
        "maximum_disk_inclusive_total_discrete_quotient_owner": total_disk_owner,
        **complex_fields(
            "leading_endpoint_coefficient_anchored_weighted_slope", endpoint_slope
        ),
        **complex_fields(
            "leading_endpoint_coefficient_anchored_unweighted_slope",
            endpoint_unweighted_slope,
        ),
        "leading_endpoint_coefficient_quadratic_center_candidate": endpoint_quadratic_candidate,
        "leading_endpoint_coefficient_maximum_central_discrete_quotient": endpoint_maximum_center,
        "leading_endpoint_coefficient_maximum_disk_inclusive_discrete_quotient": endpoint_maximum_disk,
        "uniform_M_D4_formula": "max(H3,G3+W3)/6",
        "numeric_H3_available": False,
        "numeric_G3_available": False,
        "numeric_W3_available": False,
        "numeric_uniform_M_D4_available": False,
        "claim_boundary": claims,
        "remaining_obstruction": "construct a parent-frozen common event/away atlas, derive the full endpoint H including the C1(z0/z1)^2/2 term, and interval-enclose H3, G3 and W3, with mapped-away W3 as the main unresolved numerical owner",
        "formalization_workbench_modified_file_count": 0,
        "updated_utc": utc_now(),
    }
    atomic_csv(DECOMPOSITION, decomposition)
    atomic_csv(CANCELLATION, cancellation)
    atomic_csv(TOTAL_QUOTIENTS, total_quotients)
    atomic_csv(ENDPOINT_LOG_BOUND, endpoint_rows)
    atomic_csv(THEOREM, theorem)
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
        DECOMPOSITION,
        CANCELLATION,
        TOTAL_QUOTIENTS,
        ENDPOINT_LOG_BOUND,
        THEOREM,
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
        DECOMPOSITION,
        CANCELLATION,
        TOTAL_QUOTIENTS,
        ENDPOINT_LOG_BOUND,
        THEOREM,
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
        "invariant_reduction_is_claimed": payload.get("claim_boundary", {}).get(
            CLAIM_REDUCTION
        )
        is True,
        "numeric_uniform_bound_remains_false": payload.get(
            "numeric_uniform_M_D4_available"
        )
        is False
        and payload.get("claim_boundary", {}).get(FALSE_CLAIMS[0]) is False,
        "all_broad_claims_remain_false": all(
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
            "D4_UNIFORM_REMAINDER_DECOMPOSITION_AND_BOUND_REDUCTION_VALIDATED"
            if all(checks.values())
            else "D4_UNIFORM_REMAINDER_DECOMPOSITION_VALIDATION_FAILED"
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
