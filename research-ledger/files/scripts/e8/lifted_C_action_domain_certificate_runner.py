from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


ACTION_CLAUSES = (
    "JC_from_Q_or_coframe_defined",
    "detQ_variation_identity_signed",
    "JC_normalization_units_signed",
    "parent_action_density_signed",
    "constraint_multiplier_owned",
    "PD_projector_variational_owner_signed",
    "PD_idempotence_variation_signed",
    "drel_complex_instantiated_signed",
    "drel_nilpotency_signed",
    "boundary_BC_primitive_channel_signed",
    "closedness_or_source_terms_signed",
    "bianchi_ward_stress_accounting_signed",
    "matter_selector_same_domain_signed",
    "local_FLRW_selector_signed",
    "amplitude_locks_signed",
    "no_scalar_Cperp_promotion_signed",
    "no_projected_metric_by_closure_signed",
)

DOMAIN_ZERO_CLAUSES = (
    "domain_U_oriented_smooth_chain_signed",
    "boundary_S_closed_or_relative_boundary_signed",
    "partial_boundary_zero_signed",
    "no_regulator_joint_signed",
    "fixed_boundary_class_signed",
    "orientation_convention_signed",
    "allowed_variations_preserve_boundary_signed",
    "no_corner_zero_by_assertion_signed",
)

FORBIDDEN_SOURCE_TOKENS = (
    "SCALAR_CPERP_PROMOTED",
    "PROJECTED_METRIC_BY_CLOSURE",
    "ACTION_BY_DECLARATION",
    "PD_BY_DECLARATION",
    "DREL_BY_DECLARATION",
    "CORNER_ZERO_BY_ASSERTION",
    "BOUNDARY_ZERO_BY_ASSERTION",
    "REGULATOR_IGNORED",
    "POSTFIT_REFERENCE",
    "OBSERVED_RESIDUAL_CANCEL",
    "ORBITAL_GM_DEFINITION",
    "R10_BOUND_AS_SOURCE",
)


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y", "pass", "signed"}


def missing_text(value: Any) -> bool:
    text = str(value or "").strip()
    return not text or text.upper().startswith("MISSING") or text.upper() in {"NA", "N/A", "NONE", "NOT_COMPUTED"}


def parse_float(value: Any) -> float | None:
    if missing_text(value):
        return None
    try:
        number = float(str(value).strip())
    except ValueError:
        return None
    return number if math.isfinite(number) else None


def format_float(value: float | None) -> str:
    if value is None or not math.isfinite(value):
        return "MISSING_NUMERIC_VALUE"
    return f"{value:.15e}"


def forbidden_source_used(row: dict[str, Any]) -> bool:
    source_text = " ".join(
        str(row.get(field, ""))
        for field in (
            "source_path",
            "action_source",
            "JC_source",
            "variation_source",
            "PD_source",
            "drel_source",
            "domain_source",
            "corner_source",
            "bound_source",
            "zero_theorem_path",
            "provenance",
            "notes",
        )
    ).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_clauses(row: dict[str, Any], clauses: tuple[str, ...]) -> list[str]:
    return [clause for clause in clauses if not bool_text(row.get(clause))]


def det3(matrix: list[float]) -> float:
    a, b, c, d, e, f, g, h, i = matrix
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def inv3(matrix: list[float]) -> list[float] | None:
    determinant = det3(matrix)
    if abs(determinant) <= 1.0e-15:
        return None
    a, b, c, d, e, f, g, h, i = matrix
    cofactors = [
        e * i - f * h,
        c * h - b * i,
        b * f - c * e,
        f * g - d * i,
        a * i - c * g,
        c * d - a * f,
        d * h - e * g,
        b * g - a * h,
        a * e - b * d,
    ]
    return [value / determinant for value in cofactors]


def matmul_trace(left: list[float], right: list[float]) -> float:
    return (
        left[0] * right[0]
        + left[1] * right[3]
        + left[2] * right[6]
        + left[3] * right[1]
        + left[4] * right[4]
        + left[5] * right[7]
        + left[6] * right[2]
        + left[7] * right[5]
        + left[8] * right[8]
    )


def parse_matrix(value: Any) -> list[float] | None:
    if missing_text(value):
        return None
    text = str(value).replace(";", ",").replace(" ", ",")
    parts = [part for part in text.split(",") if part]
    if len(parts) != 9:
        return None
    try:
        matrix = [float(part) for part in parts]
    except ValueError:
        return None
    return matrix if all(math.isfinite(number) for number in matrix) else None


def action_row(row: dict[str, Any]) -> dict[str, Any]:
    action_id = str(row.get("action_id", "")).strip() or "UNNAMED_ACTION"
    output: dict[str, Any] = {
        "action_id": action_id,
        "route": row.get("route", ""),
        "row_status_input": row.get("row_status", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "Z_action_contract": False,
                "Z_detQ_variation": False,
                "missing_action_clauses": "FORBIDDEN_ACTION_PROJECTOR_OR_CLOSURE_SOURCE",
                "runner_status": "FAILED_LIFTED_C_ACTION_CONTRACT_GATE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    missing = missing_clauses(row, ACTION_CLAUSES)
    detq_ready = bool_text(row.get("JC_from_Q_or_coframe_defined")) and bool_text(row.get("detQ_variation_identity_signed"))
    if missing:
        status = "LIFTED_C_ACTION_CONTRACT_PARTIAL_BLOCKED_NONCLAIM"
        if detq_ready:
            status = "DETQ_VARIATION_IDENTITY_DERIVED_BUT_PARENT_ACTION_BLOCKED_NONCLAIM"
        output.update(
            {
                "Z_action_contract": False,
                "Z_detQ_variation": detq_ready,
                "missing_action_clauses": ";".join(missing),
                "runner_status": status,
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    output.update(
        {
            "Z_action_contract": True,
            "Z_detQ_variation": True,
            "missing_action_clauses": "",
            "runner_status": "LIFTED_C_ACTION_PD_DREL_CONDITIONAL_CONTRACT_NONCLAIM",
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def detq_row(row: dict[str, Any]) -> dict[str, Any]:
    detq_id = str(row.get("detq_id", "")).strip() or "UNNAMED_DETQ"
    output: dict[str, Any] = {
        "detq_id": detq_id,
        "row_status_input": row.get("row_status", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "det_Q": "MISSING_NUMERIC_VALUE",
                "trace_Qinv_dQ": "MISSING_NUMERIC_VALUE",
                "linear_delta_det": "MISSING_NUMERIC_VALUE",
                "finite_delta_det": "MISSING_NUMERIC_VALUE",
                "identity_error_abs": "MISSING_NUMERIC_VALUE",
                "missing_inputs": "FORBIDDEN_DETQ_SOURCE",
                "runner_status": "FAILED_DETQ_VARIATION_GATE",
            }
        )
        return output

    q_matrix = parse_matrix(row.get("Q_matrix"))
    dq_matrix = parse_matrix(row.get("dQ_matrix"))
    epsilon = parse_float(row.get("epsilon"))
    missing = []
    if q_matrix is None:
        missing.append("Q_matrix")
    if dq_matrix is None:
        missing.append("dQ_matrix")
    if epsilon is None or epsilon <= 0:
        missing.append("positive_epsilon")
    if missing:
        output.update(
            {
                "det_Q": "MISSING_NUMERIC_VALUE",
                "trace_Qinv_dQ": "MISSING_NUMERIC_VALUE",
                "linear_delta_det": "MISSING_NUMERIC_VALUE",
                "finite_delta_det": "MISSING_NUMERIC_VALUE",
                "identity_error_abs": "MISSING_NUMERIC_VALUE",
                "missing_inputs": "MISSING_" + ";MISSING_".join(missing),
                "runner_status": "BLOCKED_MISSING_DETQ_VARIATION_INPUTS",
            }
        )
        return output

    determinant = det3(q_matrix)
    inverse = inv3(q_matrix)
    if inverse is None:
        output.update(
            {
                "det_Q": format_float(determinant),
                "trace_Qinv_dQ": "MISSING_NUMERIC_VALUE",
                "linear_delta_det": "MISSING_NUMERIC_VALUE",
                "finite_delta_det": "MISSING_NUMERIC_VALUE",
                "identity_error_abs": "MISSING_NUMERIC_VALUE",
                "missing_inputs": "SINGULAR_Q_MATRIX",
                "runner_status": "BLOCKED_SINGULAR_Q_FOR_DETQ_VARIATION",
            }
        )
        return output

    trace = matmul_trace(inverse, dq_matrix)
    linear_delta = determinant * trace
    q_plus = [q_value + epsilon * dq_value for q_value, dq_value in zip(q_matrix, dq_matrix)]
    finite_delta = (det3(q_plus) - determinant) / epsilon
    error = abs(finite_delta - linear_delta)
    tolerance = max(1.0e-9, 100.0 * epsilon)
    status = "DETQ_VARIATION_IDENTITY_NUMERIC_SMOKE_PASS_NONCLAIM" if error <= tolerance else "DETQ_VARIATION_IDENTITY_NUMERIC_SMOKE_WARN_NONCLAIM"
    output.update(
        {
            "det_Q": format_float(determinant),
            "trace_Qinv_dQ": format_float(trace),
            "linear_delta_det": format_float(linear_delta),
            "finite_delta_det": format_float(finite_delta),
            "identity_error_abs": format_float(error),
            "missing_inputs": "",
            "runner_status": status,
        }
    )
    return output


def domain_row(row: dict[str, Any]) -> dict[str, Any]:
    domain_id = str(row.get("domain_id", "")).strip() or "UNNAMED_DOMAIN"
    output: dict[str, Any] = {
        "domain_id": domain_id,
        "row_status_input": row.get("row_status", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "C_corner_abs": "MISSING_NUMERIC_VALUE",
                "joint_abs": "MISSING_NUMERIC_VALUE",
                "regulator_abs": "MISSING_NUMERIC_VALUE",
                "domain_edge_abs": "MISSING_NUMERIC_VALUE",
                "missing_domain_inputs": "FORBIDDEN_CORNER_OR_BOUNDARY_SOURCE",
                "runner_status": "FAILED_DOMAIN_CORNER_CERTIFICATE_GATE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    missing_zero = missing_clauses(row, DOMAIN_ZERO_CLAUSES)
    if not missing_zero:
        output.update(
            {
                "C_corner_abs": "0.000000000000000e+00",
                "joint_abs": "0.000000000000000e+00",
                "regulator_abs": "0.000000000000000e+00",
                "domain_edge_abs": "0.000000000000000e+00",
                "missing_domain_inputs": "",
                "runner_status": "DOMAIN_CCORNER_ZERO_CERTIFIED_CONDITIONAL_NONCLAIM",
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    corner_measure = parse_float(row.get("corner_measure"))
    corner_density = parse_float(row.get("corner_density_bound"))
    joint_measure = parse_float(row.get("joint_measure"))
    joint_density = parse_float(row.get("joint_density_bound"))
    regulator_abs = parse_float(row.get("regulator_collar_flux_abs"))
    source_missing = [field for field in ("domain_source", "corner_source", "bound_source") if missing_text(row.get(field))]
    numeric_missing = []
    for field, value in (
        ("corner_measure", corner_measure),
        ("corner_density_bound", corner_density),
        ("joint_measure", joint_measure),
        ("joint_density_bound", joint_density),
        ("regulator_collar_flux_abs", regulator_abs),
    ):
        if value is None or value < 0:
            numeric_missing.append(field)
    if not numeric_missing and not source_missing:
        corner_abs = (corner_measure or 0.0) * (corner_density or 0.0)
        joint_abs = (joint_measure or 0.0) * (joint_density or 0.0)
        total = corner_abs + joint_abs + (regulator_abs or 0.0)
        output.update(
            {
                "C_corner_abs": format_float(corner_abs),
                "joint_abs": format_float(joint_abs),
                "regulator_abs": format_float(regulator_abs),
                "domain_edge_abs": format_float(total),
                "missing_domain_inputs": ";".join(f"MISSING_{clause}" for clause in missing_zero),
                "runner_status": "DOMAIN_CCORNER_FINITE_BOUND_COMPUTED_NONCLAIM",
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    output.update(
        {
            "C_corner_abs": "MISSING_NUMERIC_VALUE",
            "joint_abs": "MISSING_NUMERIC_VALUE",
            "regulator_abs": format_float(regulator_abs),
            "domain_edge_abs": "MISSING_NUMERIC_VALUE",
            "missing_domain_inputs": ";".join([*(f"MISSING_{clause}" for clause in missing_zero), *(f"MISSING_{field}" for field in numeric_missing), *(f"MISSING_{field}" for field in source_missing)]),
            "runner_status": "BLOCKED_MISSING_DOMAIN_CORNER_ZERO_OR_BOUND_INPUTS",
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def read_csv(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"input CSV has no rows: {path}")
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for field in row:
            if field not in fieldnames:
                fieldnames.append(field)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def run(action_input: Path, action_output: Path, detq_input: Path, detq_output: Path, domain_input: Path, domain_output: Path) -> None:
    write_csv(action_output, [action_row(row) for row in read_csv(action_input)])
    write_csv(detq_output, [detq_row(row) for row in read_csv(detq_input)])
    write_csv(domain_output, [domain_row(row) for row in read_csv(domain_input)])


def main(argv: list[str]) -> int:
    if len(argv) != 7:
        print(
            "usage: lifted_C_action_domain_certificate_runner.py ACTION_INPUT.csv ACTION_OUTPUT.csv DETQ_INPUT.csv DETQ_OUTPUT.csv DOMAIN_INPUT.csv DOMAIN_OUTPUT.csv",
            file=sys.stderr,
        )
        return 2
    run(Path(argv[1]), Path(argv[2]), Path(argv[3]), Path(argv[4]), Path(argv[5]), Path(argv[6]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
