from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Dict, List, Mapping, Tuple


CLASSIFIER_REQUIRED_FIELDS = [
    "coefficient_id",
    "coefficient",
    "residual_role",
    "current_status",
    "private_zero_basis",
    "parent_zero_signed",
    "same_support",
    "public_scope_allowed",
    "retained_bound_route",
    "source_path",
    "input_valid_for_claim",
    "notes",
]

CLASSIFIER_BOOLEAN_FIELDS = [
    field
    for field in CLASSIFIER_REQUIRED_FIELDS
    if field
    not in {
        "coefficient_id",
        "coefficient",
        "residual_role",
        "current_status",
        "source_path",
        "notes",
    }
]

PAYLOAD_REQUIRED_FIELDS = [
    "payload_id",
    "arena",
    "cGamma_uu_abs",
    "cGamma_trace_abs",
    "cR2_uu_abs",
    "cR2_trace_abs",
    "spin_torsion_uu_abs",
    "spin_torsion_trace_abs",
    "boundary_open_uu_abs",
    "boundary_open_trace_abs",
    "Lambda_eff_abs",
    "projector_boundary_abs",
    "K_E_c2_abs",
    "F_E_threshold",
    "source_path",
    "support_certificate_path",
    "input_valid_for_claim",
    "notes",
]

PAYLOAD_NUMERIC_FIELDS = [
    "cGamma_uu_abs",
    "cGamma_trace_abs",
    "cR2_uu_abs",
    "cR2_trace_abs",
    "spin_torsion_uu_abs",
    "spin_torsion_trace_abs",
    "boundary_open_uu_abs",
    "boundary_open_trace_abs",
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


def evaluate_classifier_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    missing_fields = [
        field
        for field in CLASSIFIER_REQUIRED_FIELDS
        if field not in row or str(row.get(field, "")).strip() == ""
    ]
    bool_values = {field: bool_text(row.get(field, "False")) for field in CLASSIFIER_BOOLEAN_FIELDS}
    source_path = str(row.get("source_path", "")).strip()
    source_exists = Path(source_path).exists() if source_path and "MISSING" not in source_path.upper() else False
    input_valid = bool_values["input_valid_for_claim"]

    private_zero_usable = bool_values["private_zero_basis"] and bool_values["same_support"] and source_exists
    public_zero_ready = (
        bool_values["parent_zero_signed"]
        and bool_values["same_support"]
        and bool_values["public_scope_allowed"]
        and source_exists
        and input_valid
    )
    bound_required = bool_values["retained_bound_route"] and not public_zero_ready
    private_only_trap = private_zero_usable and not public_zero_ready
    contributes_to_private_residual = not private_zero_usable or bool_values["retained_bound_route"]

    failed_clauses = [field for field, value in bool_values.items() if not value]
    reasons: List[str] = []
    if missing_fields:
        reasons.extend([f"MISSING_FIELD_{field}" for field in missing_fields])
    if not source_exists:
        reasons.append("MISSING_EXISTING_SOURCE_PATH")
    if private_only_trap:
        reasons.append("PRIVATE_ZERO_NOT_PUBLIC_CLAIM")
    if bound_required:
        reasons.append("RETAINED_BOUND_ROUTE")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")
    reasons.extend([f"OPEN_{field.upper()}" for field in failed_clauses if field != "input_valid_for_claim"])

    if public_zero_ready:
        status = "PARENT_ZERO_READY"
    elif private_zero_usable:
        status = "PRIVATE_ZERO_USABLE_FOR_SELECTOR_ONLY"
    elif bound_required:
        status = "RETAINED_RESIDUAL_REQUIRES_BOUND"
    else:
        status = "RESIDUAL_CLASSIFICATION_BLOCKED"

    return {
        "coefficient_id": str(row.get("coefficient_id", "")),
        "coefficient": str(row.get("coefficient", "")),
        "residual_role": str(row.get("residual_role", "")),
        "input_path": str(input_path),
        "source_path": source_path,
        "source_exists": str(source_exists),
        "private_zero_usable": str(private_zero_usable),
        "public_zero_ready": str(public_zero_ready),
        "bound_required": str(bound_required),
        "private_only_trap": str(private_only_trap),
        "contributes_to_private_residual": str(contributes_to_private_residual),
        "valid_for_claim": str(public_zero_ready),
        "claim_allowed": str(public_zero_ready),
        "failed_clauses": ";".join(failed_clauses),
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_payload_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    missing_fields = [
        field for field in PAYLOAD_REQUIRED_FIELDS if field not in row or str(row.get(field, "")).strip() == ""
    ]
    parsed = {field: parse_float(row.get(field, "")) for field in PAYLOAD_NUMERIC_FIELDS}
    numeric_ready = all(ok and value >= 0.0 for ok, value in parsed.values())
    threshold_ready = parsed["F_E_threshold"][0] and parsed["F_E_threshold"][1] > 0.0

    source_path = str(row.get("source_path", "")).strip()
    support_path = str(row.get("support_certificate_path", "")).strip()
    source_exists = Path(source_path).exists() if source_path and "MISSING" not in source_path.upper() else False
    support_exists = Path(support_path).exists() if support_path and "MISSING" not in support_path.upper() else False
    input_valid = bool_text(row.get("input_valid_for_claim", "False"))
    schema_ready = not missing_fields and numeric_ready and threshold_ready
    support_ready = source_exists and support_exists

    if numeric_ready:
        E_res_uu_norm = (
            parsed["cGamma_uu_abs"][1]
            + parsed["cR2_uu_abs"][1]
            + parsed["spin_torsion_uu_abs"][1]
            + parsed["boundary_open_uu_abs"][1]
        )
        E_res_trace_norm = (
            parsed["cGamma_trace_abs"][1]
            + parsed["cR2_trace_abs"][1]
            + parsed["spin_torsion_trace_abs"][1]
            + parsed["boundary_open_trace_abs"][1]
        )
        Ruu_abs_bound = (
            E_res_uu_norm
            + 0.5 * E_res_trace_norm
            + parsed["Lambda_eff_abs"][1]
            + parsed["projector_boundary_abs"][1]
        )
        F_E_norm = parsed["K_E_c2_abs"][1] * Ruu_abs_bound
        threshold = parsed["F_E_threshold"][1]
    else:
        E_res_uu_norm = math.nan
        E_res_trace_norm = math.nan
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
        reasons.append("LOCAL_RESIDUAL_PAYLOAD_EXCEEDS_THRESHOLD")

    if valid_for_claim:
        status = "LOCAL_COSMOLOGICAL_RESIDUAL_PAYLOAD_ACCEPTS"
    elif schema_ready and support_ready and F_E_norm == 0.0:
        status = "LOCAL_COSMOLOGICAL_RESIDUAL_ZERO_SCHEMA_READY_NONCLAIM"
    elif schema_ready and support_ready and not within_threshold:
        status = "LOCAL_COSMOLOGICAL_RESIDUAL_PAYLOAD_FAILS_THRESHOLD"
    elif schema_ready:
        status = "LOCAL_COSMOLOGICAL_RESIDUAL_PAYLOAD_SCHEMA_READY_NONCLAIM"
    else:
        status = "LOCAL_COSMOLOGICAL_RESIDUAL_PAYLOAD_BLOCKED"

    return {
        "payload_id": str(row.get("payload_id", "")),
        "arena": str(row.get("arena", "")),
        "input_path": str(input_path),
        "source_path": source_path,
        "source_exists": str(source_exists),
        "support_certificate_path": support_path,
        "support_exists": str(support_exists),
        "schema_ready": str(schema_ready),
        "support_ready": str(support_ready),
        "E_res_uu_norm": "" if math.isnan(E_res_uu_norm) else f"{E_res_uu_norm:.12g}",
        "E_res_trace_norm": "" if math.isnan(E_res_trace_norm) else f"{E_res_trace_norm:.12g}",
        "Lambda_eff_abs": "" if not parsed["Lambda_eff_abs"][0] else f"{parsed['Lambda_eff_abs'][1]:.12g}",
        "projector_boundary_abs": "" if not parsed["projector_boundary_abs"][0] else f"{parsed['projector_boundary_abs'][1]:.12g}",
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


def evaluate_classifier_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_classifier_row(row, input_path) for row in read_csv(input_path)]


def evaluate_payload_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_payload_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Gate local Lambda_eff/E_res residual zeros or source-bound payloads.")
    parser.add_argument("--mode", choices=["classify", "payload"], required=True)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.mode == "classify":
        write_csv(args.output, evaluate_classifier_rows(args.input))
    else:
        write_csv(args.output, evaluate_payload_rows(args.input))


if __name__ == "__main__":
    main()
