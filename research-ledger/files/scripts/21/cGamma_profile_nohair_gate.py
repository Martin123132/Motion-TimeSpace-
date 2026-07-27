from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Dict, List, Mapping, Tuple


NOHAIR_REQUIRED_FIELDS = [
    "candidate_id",
    "route",
    "parent_memory_equation_signed",
    "positive_relaxation_operator",
    "source_terms_zero_or_boundary_routed",
    "static_tau_branch",
    "spatial_gradient_source_absent",
    "transition_shell_excluded_or_projected",
    "zero_mode_fixed",
    "same_tau_coframe_support",
    "D_t_Xi_zero",
    "grad_perp_Xi_zero",
    "alpha3_profile_zero",
    "parent_authority",
    "source_path",
    "input_valid_for_claim",
    "notes",
]

NOHAIR_BOOLEAN_FIELDS = [
    field
    for field in NOHAIR_REQUIRED_FIELDS
    if field not in {"candidate_id", "route", "parent_authority", "source_path", "notes"}
]

PRODUCT_REQUIRED_FIELDS = [
    "profile_id",
    "channel",
    "cGamma_abs",
    "profile_abs",
    "bound_value",
    "units",
    "source_path",
    "support_certificate_path",
    "input_valid_for_claim",
    "notes",
]

AJ_REQUIRED_FIELDS = [
    "pressure_id",
    "branch",
    "A_J_eff_abs",
    "cGamma_abs",
    "Pi_B",
    "T_res_over_tauL",
    "source_path",
    "support_certificate_path",
    "input_valid_for_claim",
    "notes",
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


def existing_path(path_text: str) -> bool:
    return bool(path_text) and "MISSING" not in path_text.upper() and Path(path_text).exists()


def evaluate_nohair_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    missing_fields = [
        field
        for field in NOHAIR_REQUIRED_FIELDS
        if field not in row or str(row.get(field, "")).strip() == ""
    ]
    bool_values = {field: bool_text(row.get(field, "False")) for field in NOHAIR_BOOLEAN_FIELDS}
    source_path = str(row.get("source_path", "")).strip()
    source_exists = existing_path(source_path)
    authority = str(row.get("parent_authority", "")).strip()
    parent_authority_ready = authority.startswith("PARENT_SIGNED_")
    input_valid = bool_values["input_valid_for_claim"]

    equation_ready = (
        bool_values["parent_memory_equation_signed"]
        and bool_values["positive_relaxation_operator"]
    )
    source_silence_ready = (
        bool_values["source_terms_zero_or_boundary_routed"]
        and bool_values["static_tau_branch"]
        and bool_values["spatial_gradient_source_absent"]
        and bool_values["transition_shell_excluded_or_projected"]
    )
    support_ready = bool_values["zero_mode_fixed"] and bool_values["same_tau_coframe_support"]
    observable_zero_ready = (
        bool_values["D_t_Xi_zero"]
        and bool_values["grad_perp_Xi_zero"]
        and bool_values["alpha3_profile_zero"]
    )
    nohair_certificate_ready = (
        not missing_fields
        and source_exists
        and equation_ready
        and source_silence_ready
        and support_ready
        and observable_zero_ready
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

    if nohair_certificate_ready:
        status = "CGAMMA_MEMORY_NOHAIR_CERTIFICATE_READY"
        nohair_authority = authority
    elif equation_ready and source_silence_ready and support_ready:
        status = "CGAMMA_MEMORY_NOHAIR_FORM_READY_AUTHORITY_UNSIGNED"
        nohair_authority = "CONDITIONAL_MEMORY_NOHAIR_UNSIGNED"
    elif source_silence_ready:
        status = "CGAMMA_SOURCE_SILENCE_READY_MEMORY_EQUATION_UNSIGNED"
        nohair_authority = "CONDITIONAL_SOURCE_SILENCE_MEMORY_EQUATION_UNSIGNED"
    else:
        status = "CGAMMA_MEMORY_NOHAIR_CERTIFICATE_BLOCKED"
        nohair_authority = "NO_MEMORY_NOHAIR_AUTHORITY"

    return {
        "candidate_id": str(row.get("candidate_id", "")),
        "route": str(row.get("route", "")),
        "input_path": str(input_path),
        "source_path": source_path,
        "source_exists": str(source_exists),
        "equation_ready": str(equation_ready),
        "source_silence_ready": str(source_silence_ready),
        "support_ready": str(support_ready),
        "observable_zero_ready": str(observable_zero_ready),
        "parent_authority_ready": str(parent_authority_ready),
        "nohair_certificate_ready": str(nohair_certificate_ready),
        "nohair_authority": nohair_authority,
        "valid_for_claim": str(nohair_certificate_ready),
        "claim_allowed": str(nohair_certificate_ready),
        "failed_clauses": ";".join(failed_clauses),
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_product_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    missing_fields = [
        field
        for field in PRODUCT_REQUIRED_FIELDS
        if field not in row or str(row.get(field, "")).strip() == ""
    ]
    c_ok, c_gamma = parse_float(row.get("cGamma_abs", ""))
    p_ok, profile = parse_float(row.get("profile_abs", ""))
    b_ok, bound = parse_float(row.get("bound_value", ""))
    numeric_ready = c_ok and p_ok and b_ok and c_gamma >= 0.0 and profile >= 0.0 and bound >= 0.0
    source_path = str(row.get("source_path", "")).strip()
    support_path = str(row.get("support_certificate_path", "")).strip()
    source_exists = existing_path(source_path)
    support_exists = existing_path(support_path)
    input_valid = bool_text(row.get("input_valid_for_claim", "False"))

    product_value = c_gamma * profile if numeric_ready else math.nan
    product_within_bound = numeric_ready and product_value <= bound
    valid_for_claim = (
        not missing_fields
        and numeric_ready
        and source_exists
        and support_exists
        and input_valid
        and product_within_bound
    )

    reasons: List[str] = []
    if missing_fields:
        reasons.extend([f"MISSING_FIELD_{field}" for field in missing_fields])
    if not c_ok:
        reasons.append("MISSING_OR_NONNUMERIC_cGamma_abs")
    if not p_ok:
        reasons.append("MISSING_OR_NONNUMERIC_profile_abs")
    if not b_ok:
        reasons.append("MISSING_OR_NONNUMERIC_bound_value")
    if c_ok and c_gamma < 0.0:
        reasons.append("NEGATIVE_cGamma_abs")
    if p_ok and profile < 0.0:
        reasons.append("NEGATIVE_profile_abs")
    if not source_exists:
        reasons.append("MISSING_EXISTING_SOURCE_PATH")
    if not support_exists:
        reasons.append("MISSING_SUPPORT_CERTIFICATE_PATH")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")
    if numeric_ready and not product_within_bound:
        reasons.append("CGAMMA_PRODUCT_EXCEEDS_BOUND")

    if valid_for_claim:
        status = "CGAMMA_PRODUCT_BOUND_ACCEPTS"
    elif numeric_ready and source_exists and support_exists and not product_within_bound:
        status = "CGAMMA_PRODUCT_BOUND_FAILS"
    elif numeric_ready:
        status = "CGAMMA_PRODUCT_SCHEMA_READY_NONCLAIM"
    else:
        status = "CGAMMA_PRODUCT_BOUND_BLOCKED"

    return {
        "profile_id": str(row.get("profile_id", "")),
        "channel": str(row.get("channel", "")),
        "input_path": str(input_path),
        "source_path": source_path,
        "source_exists": str(source_exists),
        "support_certificate_path": support_path,
        "support_exists": str(support_exists),
        "schema_ready": str(not missing_fields and numeric_ready),
        "cGamma_abs": "" if not c_ok else f"{c_gamma:.12g}",
        "profile_abs": "" if not p_ok else f"{profile:.12g}",
        "product_value": "" if math.isnan(product_value) else f"{product_value:.12g}",
        "bound_value": "" if not b_ok else f"{bound:.12g}",
        "product_within_bound": str(product_within_bound),
        "input_valid_for_claim": str(input_valid),
        "valid_for_claim": str(valid_for_claim),
        "claim_allowed": str(valid_for_claim),
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_aj_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    missing_fields = [
        field for field in AJ_REQUIRED_FIELDS if field not in row or str(row.get(field, "")).strip() == ""
    ]
    parsed = {
        field: parse_float(row.get(field, ""))
        for field in ["A_J_eff_abs", "cGamma_abs", "Pi_B", "T_res_over_tauL"]
    }
    numeric_ready = all(ok and value >= 0.0 for ok, value in parsed.values())
    pi_ok = parsed["Pi_B"][0] and parsed["Pi_B"][1] > 0.0
    source_path = str(row.get("source_path", "")).strip()
    support_path = str(row.get("support_certificate_path", "")).strip()
    source_exists = existing_path(source_path)
    support_exists = existing_path(support_path)
    input_valid = bool_text(row.get("input_valid_for_claim", "False"))

    coefficient = 0.167893843691
    if numeric_ready and pi_ok:
        required_T = parsed["A_J_eff_abs"][1] * parsed["cGamma_abs"][1] / (coefficient * parsed["Pi_B"][1])
        pressure_pass = parsed["T_res_over_tauL"][1] + 1.0e-12 >= required_T
    else:
        required_T = math.nan
        pressure_pass = False

    valid_for_claim = (
        not missing_fields
        and numeric_ready
        and pi_ok
        and source_exists
        and support_exists
        and input_valid
        and pressure_pass
    )

    reasons: List[str] = []
    if missing_fields:
        reasons.extend([f"MISSING_FIELD_{field}" for field in missing_fields])
    for field, (ok, value) in parsed.items():
        if not ok:
            reasons.append(f"MISSING_OR_NONNUMERIC_{field}")
        elif value < 0.0:
            reasons.append(f"NEGATIVE_{field}")
    if not pi_ok:
        reasons.append("NONPOSITIVE_Pi_B")
    if not source_exists:
        reasons.append("MISSING_EXISTING_SOURCE_PATH")
    if not support_exists:
        reasons.append("MISSING_SUPPORT_CERTIFICATE_PATH")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")
    if numeric_ready and pi_ok and not pressure_pass:
        reasons.append("CGAMMA_AJ_PRESSURE_REQUIREMENT_FAILS")

    if valid_for_claim:
        status = "CGAMMA_AJ_PRESSURE_BOUND_ACCEPTS"
    elif numeric_ready and pi_ok and source_exists and support_exists and not pressure_pass:
        status = "CGAMMA_AJ_PRESSURE_BOUND_FAILS"
    elif numeric_ready and pi_ok:
        status = "CGAMMA_AJ_PRESSURE_SCHEMA_READY_NONCLAIM"
    else:
        status = "CGAMMA_AJ_PRESSURE_BOUND_BLOCKED"

    return {
        "pressure_id": str(row.get("pressure_id", "")),
        "branch": str(row.get("branch", "")),
        "input_path": str(input_path),
        "source_path": source_path,
        "source_exists": str(source_exists),
        "support_certificate_path": support_path,
        "support_exists": str(support_exists),
        "schema_ready": str(not missing_fields and numeric_ready and pi_ok),
        "A_J_eff_abs": "" if not parsed["A_J_eff_abs"][0] else f"{parsed['A_J_eff_abs'][1]:.12g}",
        "cGamma_abs": "" if not parsed["cGamma_abs"][0] else f"{parsed['cGamma_abs'][1]:.12g}",
        "Pi_B": "" if not parsed["Pi_B"][0] else f"{parsed['Pi_B'][1]:.12g}",
        "T_res_over_tauL": "" if not parsed["T_res_over_tauL"][0] else f"{parsed['T_res_over_tauL'][1]:.12g}",
        "required_T_res_over_tauL": "" if math.isnan(required_T) else f"{required_T:.12g}",
        "pressure_pass": str(pressure_pass),
        "input_valid_for_claim": str(input_valid),
        "valid_for_claim": str(valid_for_claim),
        "claim_allowed": str(valid_for_claim),
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_nohair_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_nohair_row(row, input_path) for row in read_csv(input_path)]


def evaluate_product_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_product_row(row, input_path) for row in read_csv(input_path)]


def evaluate_aj_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_aj_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Gate c_Gamma memory no-hair, product bounds, and AJ pressure rows.")
    parser.add_argument("--mode", choices=["nohair", "product", "aj"], required=True)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.mode == "nohair":
        write_csv(args.output, evaluate_nohair_rows(args.input))
    elif args.mode == "product":
        write_csv(args.output, evaluate_product_rows(args.input))
    else:
        write_csv(args.output, evaluate_aj_rows(args.input))


if __name__ == "__main__":
    main()
