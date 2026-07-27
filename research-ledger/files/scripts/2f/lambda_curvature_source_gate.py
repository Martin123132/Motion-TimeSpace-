from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Dict, List, Mapping, Tuple


CANCELLATION_REQUIRED_FIELDS = [
    "candidate_id",
    "route",
    "parent_counter_source_declared",
    "same_parent_variation",
    "opposite_kernel_exact",
    "no_new_tuned_coefficient",
    "does_not_cancel_density_owner",
    "boundary_terms_cancel",
    "Ward_EM_guard",
    "parent_authority",
    "source_path",
    "input_valid_for_claim",
    "notes",
]

CANCELLATION_BOOLEAN_FIELDS = [
    field
    for field in CANCELLATION_REQUIRED_FIELDS
    if field not in {"candidate_id", "route", "parent_authority", "source_path", "notes"}
]

BOUND_REQUIRED_FIELDS = [
    "bound_id",
    "arena",
    "F_E_norm",
    "C_poincare",
    "C_elliptic_H2",
    "K_lambda_stress",
    "K_projection",
    "arena_threshold",
    "boundary_condition",
    "zero_mode_fixed",
    "boundary_flux_silent",
    "source_path",
    "support_certificate_path",
    "input_valid_for_claim",
    "notes",
]

BOUND_NUMERIC_FIELDS = [
    "F_E_norm",
    "C_poincare",
    "C_elliptic_H2",
    "K_lambda_stress",
    "K_projection",
    "arena_threshold",
]

RECOGNIZED_BOUNDARY_CONDITIONS = {"Dirichlet", "zero_mean_Neumann", "mixed_anchored"}

RICCI_ZERO_REQUIRED_FIELDS = [
    "candidate_id",
    "route",
    "trace_electric_identified_as_Ricci_uu",
    "local_vacuum_domain_declared",
    "parent_metric_equation_Ricci_uu_zero",
    "matter_support_excluded_or_bounded",
    "projector_extrinsic_terms_bounded",
    "boundary_zero_mode_fixed",
    "parent_authority",
    "source_path",
    "input_valid_for_claim",
    "notes",
]

RICCI_ZERO_BOOLEAN_FIELDS = [
    field
    for field in RICCI_ZERO_REQUIRED_FIELDS
    if field not in {"candidate_id", "route", "parent_authority", "source_path", "notes"}
]


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: List[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: str(row.get(field, "")) for field in fields})


def bool_text(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def parse_float(value: object) -> Tuple[bool, float]:
    text = str(value).strip()
    if not text or "MISSING" in text.upper():
        return False, math.nan
    try:
        number = float(text)
    except ValueError:
        return False, math.nan
    return math.isfinite(number), number


def evaluate_cancellation_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    missing_fields = [
        field
        for field in CANCELLATION_REQUIRED_FIELDS
        if field not in row or str(row.get(field, "")).strip() == ""
    ]
    bool_values = {field: bool_text(row.get(field, "False")) for field in CANCELLATION_BOOLEAN_FIELDS}
    source_path = str(row.get("source_path", "")).strip()
    source_exists = Path(source_path).exists() if source_path and "MISSING" not in source_path.upper() else False
    authority = str(row.get("parent_authority", "")).strip()
    parent_authority_ready = authority.startswith("PARENT_SIGNED_")
    input_valid = bool_values["input_valid_for_claim"]

    algebra_ready = all(
        bool_values[field]
        for field in [
            "parent_counter_source_declared",
            "same_parent_variation",
            "opposite_kernel_exact",
        ]
    )
    nontrivial_ready = bool_values["no_new_tuned_coefficient"] and bool_values["does_not_cancel_density_owner"]
    side_conditions_ready = bool_values["boundary_terms_cancel"] and bool_values["Ward_EM_guard"]
    trivial_counterterm_trap = algebra_ready and not nontrivial_ready
    cancellation_certificate_ready = (
        not missing_fields
        and source_exists
        and algebra_ready
        and nontrivial_ready
        and side_conditions_ready
        and parent_authority_ready
        and input_valid
    )

    failed_clauses = [field for field, value in bool_values.items() if not value]
    reasons: List[str] = []
    if missing_fields:
        reasons.extend([f"MISSING_FIELD_{field}" for field in missing_fields])
    if not source_exists:
        reasons.append("MISSING_EXISTING_SOURCE_PATH")
    if trivial_counterterm_trap:
        reasons.append("TRIVIAL_COUNTERTERM_OR_DENSITY_OWNER_REMOVAL")
    if not parent_authority_ready:
        reasons.append("PARENT_AUTHORITY_NOT_SIGNED")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")
    reasons.extend([f"OPEN_{field.upper()}" for field in failed_clauses if field != "input_valid_for_claim"])

    if cancellation_certificate_ready:
        status = "LAMBDA_CURVATURE_SOURCE_PARENT_CANCELLATION_READY"
        cancellation_authority = authority
    elif trivial_counterterm_trap:
        status = "TRIVIAL_COUNTERTERM_TRAP_NOT_PARENT_CANCELLATION"
        cancellation_authority = "NO_AUTHORITY_TRIVIAL_COUNTERTERM"
    elif algebra_ready:
        status = "CANCELLATION_ALGEBRA_READY_SIDE_CONDITIONS_UNSIGNED"
        cancellation_authority = "CONDITIONAL_CANCELLATION_UNSIGNED"
    else:
        status = "CANCELLATION_CERTIFICATE_BLOCKED"
        cancellation_authority = "NO_CANCELLATION_AUTHORITY"

    return {
        "candidate_id": str(row.get("candidate_id", "")),
        "route": str(row.get("route", "")),
        "input_path": str(input_path),
        "source_path": source_path,
        "source_exists": str(source_exists),
        "algebra_ready": str(algebra_ready),
        "nontrivial_ready": str(nontrivial_ready),
        "side_conditions_ready": str(side_conditions_ready),
        "trivial_counterterm_trap": str(trivial_counterterm_trap),
        "parent_authority_ready": str(parent_authority_ready),
        "cancellation_certificate_ready": str(cancellation_certificate_ready),
        "cancellation_authority": cancellation_authority,
        "valid_for_claim": str(cancellation_certificate_ready),
        "claim_allowed": str(cancellation_certificate_ready),
        "failed_clauses": ";".join(failed_clauses),
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_bound_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    missing_fields = [
        field for field in BOUND_REQUIRED_FIELDS if field not in row or str(row.get(field, "")).strip() == ""
    ]
    parsed = {field: parse_float(row.get(field, "")) for field in BOUND_NUMERIC_FIELDS}
    numeric_ready = all(ok and value >= 0.0 for ok, value in parsed.values())
    positive_constants_ready = all(
        parsed[field][0] and parsed[field][1] > 0.0
        for field in ["C_poincare", "C_elliptic_H2", "K_lambda_stress", "K_projection", "arena_threshold"]
    )

    source_path = str(row.get("source_path", "")).strip()
    support_path = str(row.get("support_certificate_path", "")).strip()
    source_exists = Path(source_path).exists() if source_path and "MISSING" not in source_path.upper() else False
    support_exists = Path(support_path).exists() if support_path and "MISSING" not in support_path.upper() else False
    boundary_condition = str(row.get("boundary_condition", "")).strip()
    boundary_condition_recognized = boundary_condition in RECOGNIZED_BOUNDARY_CONDITIONS
    zero_mode_fixed = bool_text(row.get("zero_mode_fixed", "False"))
    boundary_flux_silent = bool_text(row.get("boundary_flux_silent", "False"))
    input_valid = bool_text(row.get("input_valid_for_claim", "False"))
    boundary_ready = boundary_condition_recognized and zero_mode_fixed and boundary_flux_silent
    support_ready = source_exists and support_exists
    schema_ready = not missing_fields and numeric_ready and positive_constants_ready and boundary_condition_recognized

    if numeric_ready:
        F_E = parsed["F_E_norm"][1]
        C_poincare = parsed["C_poincare"][1]
        C_elliptic = parsed["C_elliptic_H2"][1]
        K_lambda = parsed["K_lambda_stress"][1]
        K_projection = parsed["K_projection"][1]
        threshold = parsed["arena_threshold"][1]
        lambda_L2_bound = (C_poincare**2) * F_E
        grad_lambda_L2_bound = C_poincare * F_E
        lambda_H2_bound = C_elliptic * F_E
        payload_score = K_lambda * K_projection * (lambda_L2_bound + grad_lambda_L2_bound + lambda_H2_bound)
    else:
        threshold = math.nan
        lambda_L2_bound = math.nan
        grad_lambda_L2_bound = math.nan
        lambda_H2_bound = math.nan
        payload_score = math.nan

    payload_within_threshold = schema_ready and payload_score <= threshold
    valid_for_claim = schema_ready and boundary_ready and support_ready and input_valid and payload_within_threshold

    reasons: List[str] = []
    if missing_fields:
        reasons.extend([f"MISSING_FIELD_{field}" for field in missing_fields])
    for field, (ok, value) in parsed.items():
        if not ok:
            reasons.append(f"MISSING_OR_NONNUMERIC_{field}")
        elif value < 0.0:
            reasons.append(f"NEGATIVE_{field}")
    if not positive_constants_ready:
        reasons.append("NONPOSITIVE_REQUIRED_CONSTANT")
    if not boundary_condition_recognized:
        reasons.append("UNRECOGNIZED_BOUNDARY_CONDITION")
    if not zero_mode_fixed:
        reasons.append("ZERO_MODE_NOT_FIXED")
    if not boundary_flux_silent:
        reasons.append("BOUNDARY_FLUX_NOT_SILENT")
    if not source_exists:
        reasons.append("MISSING_EXISTING_SOURCE_PATH")
    if not support_exists:
        reasons.append("MISSING_SUPPORT_CERTIFICATE_PATH")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")
    if schema_ready and not payload_within_threshold:
        reasons.append("LAMBDA_CURVATURE_PAYLOAD_EXCEEDS_THRESHOLD")

    if valid_for_claim:
        status = "LAMBDA_CURVATURE_PAYLOAD_BOUND_ACCEPTS"
    elif schema_ready and boundary_ready and support_ready and not payload_within_threshold:
        status = "LAMBDA_CURVATURE_PAYLOAD_BOUND_FAILS_THRESHOLD"
    elif schema_ready:
        status = "LAMBDA_CURVATURE_PAYLOAD_BOUND_SCHEMA_READY_NONCLAIM"
    else:
        status = "LAMBDA_CURVATURE_PAYLOAD_BOUND_BLOCKED"

    return {
        "bound_id": str(row.get("bound_id", "")),
        "arena": str(row.get("arena", "")),
        "input_path": str(input_path),
        "source_path": source_path,
        "source_exists": str(source_exists),
        "support_certificate_path": support_path,
        "support_exists": str(support_exists),
        "schema_ready": str(schema_ready),
        "boundary_ready": str(boundary_ready),
        "support_ready": str(support_ready),
        "lambda_L2_bound": "" if math.isnan(lambda_L2_bound) else f"{lambda_L2_bound:.12g}",
        "grad_lambda_L2_bound": "" if math.isnan(grad_lambda_L2_bound) else f"{grad_lambda_L2_bound:.12g}",
        "lambda_H2_bound": "" if math.isnan(lambda_H2_bound) else f"{lambda_H2_bound:.12g}",
        "lambda_curvature_payload_score": "" if math.isnan(payload_score) else f"{payload_score:.12g}",
        "arena_threshold": "" if math.isnan(threshold) else f"{threshold:.12g}",
        "payload_within_threshold": str(payload_within_threshold),
        "input_valid_for_claim": str(input_valid),
        "valid_for_claim": str(valid_for_claim),
        "claim_allowed": str(valid_for_claim),
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_ricci_zero_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    missing_fields = [
        field
        for field in RICCI_ZERO_REQUIRED_FIELDS
        if field not in row or str(row.get(field, "")).strip() == ""
    ]
    bool_values = {field: bool_text(row.get(field, "False")) for field in RICCI_ZERO_BOOLEAN_FIELDS}
    source_path = str(row.get("source_path", "")).strip()
    source_exists = Path(source_path).exists() if source_path and "MISSING" not in source_path.upper() else False
    authority = str(row.get("parent_authority", "")).strip()
    parent_authority_ready = authority.startswith("PARENT_SIGNED_")
    input_valid = bool_values["input_valid_for_claim"]

    source_classified = bool_values["trace_electric_identified_as_Ricci_uu"]
    vacuum_ready = bool_values["local_vacuum_domain_declared"] and bool_values["matter_support_excluded_or_bounded"]
    metric_ready = bool_values["parent_metric_equation_Ricci_uu_zero"]
    side_conditions_ready = bool_values["projector_extrinsic_terms_bounded"] and bool_values["boundary_zero_mode_fixed"]
    ricci_zero_certificate_ready = (
        not missing_fields
        and source_exists
        and source_classified
        and vacuum_ready
        and metric_ready
        and side_conditions_ready
        and parent_authority_ready
        and input_valid
    )

    failed_clauses = [field for field, value in bool_values.items() if not value]
    reasons: List[str] = []
    if missing_fields:
        reasons.extend([f"MISSING_FIELD_{field}" for field in missing_fields])
    if not source_exists:
        reasons.append("MISSING_EXISTING_SOURCE_PATH")
    if not parent_authority_ready:
        reasons.append("PARENT_AUTHORITY_NOT_SIGNED")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")
    reasons.extend([f"OPEN_{field.upper()}" for field in failed_clauses if field != "input_valid_for_claim"])

    if ricci_zero_certificate_ready:
        status = "RICCI_TRACE_SOURCE_ZERO_CERTIFICATE_READY"
        zero_authority = authority
    elif source_classified and vacuum_ready and not metric_ready:
        status = "RICCI_TRACE_SOURCE_IDENTIFIED_PARENT_VACUUM_EQUATION_UNSIGNED"
        zero_authority = "CONDITIONAL_RICCI_ZERO_PARENT_METRIC_EQUATION_UNSIGNED"
    elif source_classified and not vacuum_ready:
        status = "RICCI_TRACE_SOURCE_IDENTIFIED_MATTER_PAYLOAD_REMAINS"
        zero_authority = "CONDITIONAL_RICCI_SOURCE_MATTER_PAYLOAD"
    elif source_classified:
        status = "RICCI_TRACE_SOURCE_IDENTIFIED_SIDE_CONDITIONS_UNSIGNED"
        zero_authority = "CONDITIONAL_RICCI_SOURCE_SIDE_CONDITIONS_UNSIGNED"
    else:
        status = "RICCI_ZERO_CERTIFICATE_BLOCKED"
        zero_authority = "NO_RICCI_ZERO_AUTHORITY"

    return {
        "candidate_id": str(row.get("candidate_id", "")),
        "route": str(row.get("route", "")),
        "input_path": str(input_path),
        "source_path": source_path,
        "source_exists": str(source_exists),
        "source_classified": str(source_classified),
        "vacuum_ready": str(vacuum_ready),
        "metric_ready": str(metric_ready),
        "side_conditions_ready": str(side_conditions_ready),
        "parent_authority_ready": str(parent_authority_ready),
        "ricci_zero_certificate_ready": str(ricci_zero_certificate_ready),
        "zero_authority": zero_authority,
        "valid_for_claim": str(ricci_zero_certificate_ready),
        "claim_allowed": str(ricci_zero_certificate_ready),
        "failed_clauses": ";".join(failed_clauses),
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_cancellation_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_cancellation_row(row, input_path) for row in read_csv(input_path)]


def evaluate_bound_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_bound_row(row, input_path) for row in read_csv(input_path)]


def evaluate_ricci_zero_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_ricci_zero_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Gate parent cancellation or elliptic bounds for curvature-sourced lambda_S.")
    parser.add_argument("--mode", choices=["cancellation", "bound", "ricci-zero"], required=True)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.mode == "cancellation":
        write_csv(args.output, evaluate_cancellation_rows(args.input))
    elif args.mode == "bound":
        write_csv(args.output, evaluate_bound_rows(args.input))
    else:
        write_csv(args.output, evaluate_ricci_zero_rows(args.input))


if __name__ == "__main__":
    main()
