from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Dict, List, Mapping, Tuple


EQUATION_REQUIRED_FIELDS = [
    "candidate_id",
    "route",
    "EH_or_EC_selector_signed",
    "trace_reversal_written",
    "kappa_eff_constant",
    "same_Hilbert_source",
    "local_vacuum_T_zero",
    "residual_tensor_zero_or_bounded",
    "Lambda_eff_zero_or_bounded",
    "same_tau_coframe_support",
    "boundary_projector_silent",
    "parent_authority",
    "source_path",
    "input_valid_for_claim",
    "notes",
]

EQUATION_BOOLEAN_FIELDS = [
    field
    for field in EQUATION_REQUIRED_FIELDS
    if field not in {"candidate_id", "route", "parent_authority", "source_path", "notes"}
]

BOUND_REQUIRED_FIELDS = [
    "bound_id",
    "arena",
    "kappa_eff_abs",
    "T_uu_norm",
    "T_trace_norm",
    "E_res_uu_norm",
    "E_res_trace_norm",
    "Lambda_eff_abs",
    "projector_boundary_abs",
    "K_E_c2_abs",
    "F_E_threshold",
    "source_path",
    "support_certificate_path",
    "input_valid_for_claim",
    "notes",
]

BOUND_NUMERIC_FIELDS = [
    "kappa_eff_abs",
    "T_uu_norm",
    "T_trace_norm",
    "E_res_uu_norm",
    "E_res_trace_norm",
    "Lambda_eff_abs",
    "projector_boundary_abs",
    "K_E_c2_abs",
    "F_E_threshold",
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


def evaluate_equation_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    missing_fields = [
        field
        for field in EQUATION_REQUIRED_FIELDS
        if field not in row or str(row.get(field, "")).strip() == ""
    ]
    bool_values = {field: bool_text(row.get(field, "False")) for field in EQUATION_BOOLEAN_FIELDS}
    source_path = str(row.get("source_path", "")).strip()
    source_exists = Path(source_path).exists() if source_path and "MISSING" not in source_path.upper() else False
    authority = str(row.get("parent_authority", "")).strip()
    parent_authority_ready = authority.startswith("PARENT_SIGNED_")
    input_valid = bool_values["input_valid_for_claim"]

    trace_reversal_ready = (
        bool_values["trace_reversal_written"]
        and bool_values["kappa_eff_constant"]
        and bool_values["same_Hilbert_source"]
    )
    vacuum_ready = bool_values["local_vacuum_T_zero"] and bool_values["same_tau_coframe_support"]
    residual_ready = bool_values["residual_tensor_zero_or_bounded"] and bool_values["Lambda_eff_zero_or_bounded"]
    side_conditions_ready = bool_values["boundary_projector_silent"]
    selector_ready = bool_values["EH_or_EC_selector_signed"]
    ricci_equation_certificate_ready = (
        not missing_fields
        and source_exists
        and trace_reversal_ready
        and vacuum_ready
        and residual_ready
        and side_conditions_ready
        and selector_ready
        and parent_authority_ready
        and input_valid
    )

    failed_clauses = [field for field, value in bool_values.items() if not value]
    reasons: List[str] = []
    if missing_fields:
        reasons.extend([f"MISSING_FIELD_{field}" for field in missing_fields])
    if not source_exists:
        reasons.append("MISSING_EXISTING_SOURCE_PATH")
    if not selector_ready:
        reasons.append("EH_OR_EC_SELECTOR_UNSIGNED")
    if not parent_authority_ready:
        reasons.append("PARENT_AUTHORITY_NOT_SIGNED")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")
    reasons.extend([f"OPEN_{field.upper()}" for field in failed_clauses if field != "input_valid_for_claim"])

    if ricci_equation_certificate_ready:
        status = "RICCI_UU_LOCAL_VACUUM_EQUATION_CERTIFICATE_READY"
        equation_authority = authority
    elif trace_reversal_ready and vacuum_ready and residual_ready and side_conditions_ready:
        status = "RICCI_UU_FORMULA_READY_SELECTOR_OR_AUTHORITY_UNSIGNED"
        equation_authority = "CONDITIONAL_RICCI_UU_FORMULA_UNSIGNED"
    elif trace_reversal_ready:
        status = "RICCI_UU_TRACE_REVERSAL_READY_RESIDUALS_OPEN"
        equation_authority = "CONDITIONAL_TRACE_REVERSAL_RESIDUALS_OPEN"
    else:
        status = "RICCI_UU_EQUATION_CERTIFICATE_BLOCKED"
        equation_authority = "NO_RICCI_UU_EQUATION_AUTHORITY"

    return {
        "candidate_id": str(row.get("candidate_id", "")),
        "route": str(row.get("route", "")),
        "input_path": str(input_path),
        "source_path": source_path,
        "source_exists": str(source_exists),
        "trace_reversal_ready": str(trace_reversal_ready),
        "vacuum_ready": str(vacuum_ready),
        "residual_ready": str(residual_ready),
        "side_conditions_ready": str(side_conditions_ready),
        "selector_ready": str(selector_ready),
        "parent_authority_ready": str(parent_authority_ready),
        "ricci_equation_certificate_ready": str(ricci_equation_certificate_ready),
        "equation_authority": equation_authority,
        "valid_for_claim": str(ricci_equation_certificate_ready),
        "claim_allowed": str(ricci_equation_certificate_ready),
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
    threshold_ready = parsed["F_E_threshold"][0] and parsed["F_E_threshold"][1] > 0.0
    K_ready = parsed["K_E_c2_abs"][0] and parsed["K_E_c2_abs"][1] >= 0.0

    source_path = str(row.get("source_path", "")).strip()
    support_path = str(row.get("support_certificate_path", "")).strip()
    source_exists = Path(source_path).exists() if source_path and "MISSING" not in source_path.upper() else False
    support_exists = Path(support_path).exists() if support_path and "MISSING" not in support_path.upper() else False
    input_valid = bool_text(row.get("input_valid_for_claim", "False"))
    schema_ready = not missing_fields and numeric_ready and threshold_ready and K_ready
    support_ready = source_exists and support_exists

    if numeric_ready:
        kappa_eff = parsed["kappa_eff_abs"][1]
        matter_bound = kappa_eff * (parsed["T_uu_norm"][1] + 0.5 * parsed["T_trace_norm"][1])
        residual_bound = parsed["E_res_uu_norm"][1] + 0.5 * parsed["E_res_trace_norm"][1]
        lambda_bound = parsed["Lambda_eff_abs"][1]
        projector_bound = parsed["projector_boundary_abs"][1]
        Ruu_abs_bound = matter_bound + residual_bound + lambda_bound + projector_bound
        F_E_norm = parsed["K_E_c2_abs"][1] * Ruu_abs_bound
        threshold = parsed["F_E_threshold"][1]
    else:
        matter_bound = math.nan
        residual_bound = math.nan
        lambda_bound = math.nan
        projector_bound = math.nan
        Ruu_abs_bound = math.nan
        F_E_norm = math.nan
        threshold = math.nan

    within_threshold = schema_ready and F_E_norm <= threshold
    valid_for_claim = schema_ready and support_ready and input_valid and within_threshold

    reasons: List[str] = []
    if missing_fields:
        reasons.extend([f"MISSING_FIELD_{field}" for field in missing_fields])
    for field, (ok, value) in parsed.items():
        if not ok:
            reasons.append(f"MISSING_OR_NONNUMERIC_{field}")
        elif value < 0.0:
            reasons.append(f"NEGATIVE_{field}")
    if not threshold_ready:
        reasons.append("MISSING_OR_INVALID_F_E_THRESHOLD")
    if not source_exists:
        reasons.append("MISSING_EXISTING_SOURCE_PATH")
    if not support_exists:
        reasons.append("MISSING_SUPPORT_CERTIFICATE_PATH")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")
    if schema_ready and not within_threshold:
        reasons.append("RICCI_UU_SOURCE_BOUND_EXCEEDS_THRESHOLD")

    if valid_for_claim:
        status = "RICCI_UU_SOURCE_BOUND_ACCEPTS"
    elif schema_ready and support_ready and F_E_norm == 0.0:
        status = "RICCI_UU_SOURCE_ZERO_SCHEMA_READY_NONCLAIM"
    elif schema_ready and support_ready and not within_threshold:
        status = "RICCI_UU_SOURCE_BOUND_FAILS_THRESHOLD"
    elif schema_ready:
        status = "RICCI_UU_SOURCE_BOUND_SCHEMA_READY_NONCLAIM"
    else:
        status = "RICCI_UU_SOURCE_BOUND_BLOCKED"

    return {
        "bound_id": str(row.get("bound_id", "")),
        "arena": str(row.get("arena", "")),
        "input_path": str(input_path),
        "source_path": source_path,
        "source_exists": str(source_exists),
        "support_certificate_path": support_path,
        "support_exists": str(support_exists),
        "schema_ready": str(schema_ready),
        "support_ready": str(support_ready),
        "matter_Ruu_bound": "" if math.isnan(matter_bound) else f"{matter_bound:.12g}",
        "residual_Ruu_bound": "" if math.isnan(residual_bound) else f"{residual_bound:.12g}",
        "Lambda_Ruu_bound": "" if math.isnan(lambda_bound) else f"{lambda_bound:.12g}",
        "projector_boundary_bound": "" if math.isnan(projector_bound) else f"{projector_bound:.12g}",
        "Ruu_abs_bound": "" if math.isnan(Ruu_abs_bound) else f"{Ruu_abs_bound:.12g}",
        "F_E_norm": "" if math.isnan(F_E_norm) else f"{F_E_norm:.12g}",
        "F_E_threshold": "" if math.isnan(threshold) else f"{threshold:.12g}",
        "within_threshold": str(within_threshold),
        "input_valid_for_claim": str(input_valid),
        "valid_for_claim": str(valid_for_claim),
        "claim_allowed": str(valid_for_claim),
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_equation_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_equation_row(row, input_path) for row in read_csv(input_path)]


def evaluate_bound_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_bound_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Gate and bound Ricci_uu source terms for the trace-electric lambda branch.")
    parser.add_argument("--mode", choices=["equation", "bound"], required=True)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.mode == "equation":
        write_csv(args.output, evaluate_equation_rows(args.input))
    else:
        write_csv(args.output, evaluate_bound_rows(args.input))


if __name__ == "__main__":
    main()
