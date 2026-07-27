from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


PROFILE_ZERO_CLAUSES = (
    "same_action_hilbert_derivative",
    "no_source_only_functional",
    "no_nonhilbert_current",
    "no_hidden_source_label_hom",
    "variation_before_readout",
    "same_worldtube",
    "topological_distributional_equality",
    "rest_bulk_metric_nullity",
    "boundary_projection_silent",
    "readout_profile_silent",
)

EPROFILE_COMPONENTS = (
    "E_shadow",
    "E_top_profile",
    "E_nonHilbert_profile",
    "E_readout_profile",
)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Iterable[Dict[str, object]]) -> None:
    materialized = [{key: str(value) for key, value in row.items()} for row in rows]
    path.parent.mkdir(parents=True, exist_ok=True)
    if not materialized:
        path.write_text("", encoding="utf-8")
        return
    fields: List[str] = []
    for row in materialized:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows({field: row.get(field, "") for field in fields} for row in materialized)


def parse_bool(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def parse_float(value: object) -> Tuple[bool, float]:
    try:
        text = str(value).strip()
        if not text or text.upper().startswith("MISSING"):
            return False, 0.0
        parsed = float(text)
        return True, parsed
    except (TypeError, ValueError):
        return False, 0.0


def evaluate_profile_zero_row(row: Dict[str, str], input_path: Path) -> Dict[str, object]:
    source_path = row.get("source_path", "")
    source_exists = bool(source_path) and Path(source_path).exists()
    failed = [clause for clause in PROFILE_ZERO_CLAUSES if not parse_bool(row.get(clause, ""))]
    private_profile_zero = source_exists and not failed
    parent_signed = parse_bool(row.get("parent_signed", "False"))
    public_authority = parse_bool(row.get("public_authority", "False"))
    input_valid = parse_bool(row.get("input_valid_for_claim", "False"))
    valid_for_claim = private_profile_zero and parent_signed and public_authority and input_valid
    reasons = []
    if not source_exists:
        reasons.append("SOURCE_PATH_MISSING")
    reasons.extend(f"OPEN_{clause.upper()}" for clause in failed)
    if not parent_signed:
        reasons.append("PARENT_SIGNED_FALSE")
    if not public_authority:
        reasons.append("PUBLIC_AUTHORITY_FALSE")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")
    if valid_for_claim:
        status = "EPROFILE_ZERO_CLAIM_READY"
    elif private_profile_zero:
        status = "EPROFILE_ZERO_PRIVATE_CLEAN_NONCLAIM"
    else:
        status = "EPROFILE_ZERO_BLOCKED"
    return {
        "profile_zero_id": row.get("profile_zero_id", ""),
        "branch": row.get("branch", ""),
        "input_path": str(input_path),
        "source_path": source_path,
        "source_exists": source_exists,
        "failed_clauses": "|".join(failed),
        "private_profile_zero": private_profile_zero,
        "parent_signed": parent_signed,
        "public_authority": public_authority,
        "input_valid_for_claim": input_valid,
        "valid_for_claim": valid_for_claim,
        "claim_allowed": valid_for_claim,
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_eprofile_bound_row(row: Dict[str, str], input_path: Path) -> Dict[str, object]:
    source_path = row.get("source_path", "")
    source_exists = bool(source_path) and Path(source_path).exists()
    component_values = {component: parse_float(row.get(component, "")) for component in EPROFILE_COMPONENTS}
    k_ok, k_value = parse_float(row.get("K_N", ""))
    delta_ok, delta_value = parse_float(row.get("delta_N", ""))
    numeric_components = all(ok for ok, _ in component_values.values())
    numeric_ready = source_exists and numeric_components and k_ok and delta_ok
    eprofile_sum = sum(abs(value) for _, value in component_values.values()) if numeric_components else ""
    if numeric_ready:
        residual_fraction = k_value * float(eprofile_sum)
        within_bound = residual_fraction <= delta_value
        allowed_Eprofile_sum = delta_value / k_value if k_value > 0 else float("nan")
    else:
        residual_fraction = ""
        within_bound = False
        allowed_Eprofile_sum = ""
    input_valid = parse_bool(row.get("input_valid_for_claim", "False"))
    valid_for_claim = numeric_ready and within_bound and input_valid
    reasons = []
    if not source_exists:
        reasons.append("SOURCE_PATH_MISSING")
    reasons.extend(f"MISSING_{component.upper()}" for component, (ok, _) in component_values.items() if not ok)
    if not k_ok:
        reasons.append("MISSING_K_N")
    if not delta_ok:
        reasons.append("MISSING_DELTA_N")
    if numeric_ready and not within_bound:
        reasons.append("EPROFILE_BOUND_EXCEEDS_DELTA_N")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")
    if valid_for_claim:
        status = "EPROFILE_BOUND_CLAIM_READY"
    elif numeric_ready and within_bound:
        status = "EPROFILE_BOUND_SCHEMA_READY_NONCLAIM"
    elif numeric_ready:
        status = "EPROFILE_BOUND_FAILS"
    else:
        status = "EPROFILE_BOUND_BLOCKED"
    return {
        "bound_id": row.get("bound_id", ""),
        "arena": row.get("arena", ""),
        "branch": row.get("branch", ""),
        "input_path": str(input_path),
        "source_path": source_path,
        "source_exists": source_exists,
        "numeric_components": numeric_components,
        "K_N": "" if not k_ok else f"{k_value:.12g}",
        "delta_N": "" if not delta_ok else f"{delta_value:.12g}",
        "E_shadow": row.get("E_shadow", ""),
        "E_top_profile": row.get("E_top_profile", ""),
        "E_nonHilbert_profile": row.get("E_nonHilbert_profile", ""),
        "E_readout_profile": row.get("E_readout_profile", ""),
        "Eprofile_sum": "" if eprofile_sum == "" else f"{eprofile_sum:.12g}",
        "allowed_Eprofile_sum": "" if allowed_Eprofile_sum == "" else f"{allowed_Eprofile_sum:.12g}",
        "residual_fraction": "" if residual_fraction == "" else f"{residual_fraction:.12g}",
        "within_bound": within_bound,
        "input_valid_for_claim": input_valid,
        "valid_for_claim": valid_for_claim,
        "claim_allowed": valid_for_claim,
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_profile_zero_rows(input_path: Path) -> List[Dict[str, object]]:
    return [evaluate_profile_zero_row(row, input_path) for row in read_csv(input_path)]


def evaluate_eprofile_bound_rows(input_path: Path) -> List[Dict[str, object]]:
    return [evaluate_eprofile_bound_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Gate density-profile zero clauses and finite E_profile source-shadow bounds.")
    parser.add_argument("--mode", choices=["profile-zero", "eprofile-bound"], required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.mode == "profile-zero":
        write_csv(args.output, evaluate_profile_zero_rows(args.input))
    else:
        write_csv(args.output, evaluate_eprofile_bound_rows(args.input))


if __name__ == "__main__":
    main()
