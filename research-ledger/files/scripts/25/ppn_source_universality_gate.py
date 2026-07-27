from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


TRUE_VALUES = {"1", "true", "yes", "y", "pass", "signed", "derived_zero", "ready", "adopted"}
MISSING_PREFIXES = ("MISSING_", "PENDING_", "PLACEHOLDER_", "SCHEMA_", "NOT_", "UNKNOWN_")

PPN_SOURCE_CLAUSES = (
    "private_branch_adopted",
    "delta_w_zero",
    "material_reentry_zero",
    "hilbert_source_single",
    "ppn_mapping_present",
    "source_piece_named",
    "non_source_residual_preserved",
    "public_claim_false",
)

MATERIAL_CLAUSES = (
    "material_inventory_named",
    "source_candidates_recorded",
    "component_convention_defined",
    "projection_coeff_numeric",
    "residual_value_numeric",
    "arena_bound_numeric",
    "readout_no_reentry",
)


def as_bool(value: object) -> bool:
    return str(value).strip().lower() in TRUE_VALUES


def is_missing_like(value: object) -> bool:
    text = str(value).strip()
    return not text or any(text.startswith(prefix) for prefix in MISSING_PREFIXES)


def path_exists(value: object) -> bool:
    text = str(value).strip()
    return bool(text) and not is_missing_like(text) and Path(text).exists()


def parse_float(value: object) -> Tuple[bool, float]:
    text = str(value).strip()
    if is_missing_like(text):
        return False, 0.0
    try:
        return True, float(text)
    except ValueError:
        return False, 0.0


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Iterable[Dict[str, object]]) -> None:
    materialized = [{key: str(value) for key, value in row.items()} for row in rows]
    path.parent.mkdir(parents=True, exist_ok=True)
    if not materialized:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(materialized[0].keys()))
        writer.writeheader()
        writer.writerows(materialized)


def evaluate_ppn_row(row: Dict[str, str], input_path: Path) -> Dict[str, object]:
    source_ok = path_exists(row.get("source_path", ""))
    failed = [clause for clause in PPN_SOURCE_CLAUSES if not as_bool(row.get(clause, ""))]
    zero_ok, zero_value = parse_float(row.get("source_piece_value", ""))
    source_piece_zero = zero_ok and abs(zero_value) == 0.0
    full_observable_claim = as_bool(row.get("full_observable_claim", "False"))
    input_valid = as_bool(row.get("input_valid_for_claim", "False"))
    public_authority = as_bool(row.get("public_authority", "False"))
    source_component_closed = source_ok and not failed and source_piece_zero
    public_claim_ready = source_component_closed and full_observable_claim and input_valid and public_authority

    reasons = []
    if not source_ok:
        reasons.append("SOURCE_PATH_MISSING")
    reasons.extend(f"OPEN_{clause.upper()}" for clause in failed)
    if not zero_ok:
        reasons.append("SOURCE_PIECE_VALUE_MISSING_OR_NONNUMERIC")
    elif not source_piece_zero:
        reasons.append("SOURCE_PIECE_VALUE_NONZERO")
    if not full_observable_claim:
        reasons.append("FULL_OBSERVABLE_CLAIM_FALSE")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")
    if not public_authority:
        reasons.append("PUBLIC_AUTHORITY_FALSE")

    if public_claim_ready:
        status = "PPN_SOURCE_UNIVERSALITY_PUBLIC_CLAIM_READY"
    elif source_component_closed:
        status = "PPN_SOURCE_UNIVERSALITY_COMPONENT_ZERO_PRIVATE_NONCLAIM"
    elif source_ok and zero_ok:
        status = "PPN_SOURCE_UNIVERSALITY_PARTIAL_CLAUSES_OPEN"
    elif source_ok:
        status = "PPN_SOURCE_UNIVERSALITY_SOURCE_PRESENT_VALUE_OR_CLAUSES_OPEN"
    else:
        status = "PPN_SOURCE_UNIVERSALITY_BLOCKED_MISSING_SOURCE"

    return {
        "row_id": row.get("row_id", ""),
        "arena": row.get("arena", ""),
        "observable": row.get("observable", ""),
        "residual_piece": row.get("residual_piece", ""),
        "input_path": str(input_path),
        "source_path": row.get("source_path", ""),
        "source_exists": source_ok,
        "failed_clauses": "|".join(failed),
        "source_piece_value": row.get("source_piece_value", ""),
        "source_piece_zero": source_piece_zero,
        "non_source_residual_preserved": as_bool(row.get("non_source_residual_preserved", "")),
        "non_source_residuals": row.get("non_source_residuals", ""),
        "full_observable_claim": full_observable_claim,
        "input_valid_for_claim": input_valid,
        "public_authority": public_authority,
        "valid_for_claim": public_claim_ready,
        "claim_allowed": public_claim_ready,
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_material_row(row: Dict[str, str], input_path: Path) -> Dict[str, object]:
    source_ok = path_exists(row.get("source_path", ""))
    input_valid = as_bool(row.get("input_valid_for_claim", "False"))
    public_authority = as_bool(row.get("public_authority", "False"))
    failed = [clause for clause in MATERIAL_CLAUSES if not as_bool(row.get(clause, ""))]
    coeff_ok, coeff = parse_float(row.get("projection_coeff", ""))
    value_ok, value = parse_float(row.get("residual_value", ""))
    bound_ok, bound = parse_float(row.get("arena_bound", ""))
    numeric_ready = source_ok and coeff_ok and value_ok and bound_ok
    projected_residual = coeff * abs(value) if numeric_ready else ""
    within_bound = bool(numeric_ready and float(projected_residual) <= bound)
    material_ready = source_ok and not failed and numeric_ready and within_bound
    valid_for_claim = material_ready and input_valid and public_authority

    reasons = []
    if not source_ok:
        reasons.append("SOURCE_PATH_MISSING")
    reasons.extend(f"OPEN_{clause.upper()}" for clause in failed)
    if not coeff_ok:
        reasons.append("PROJECTION_COEFF_MISSING_OR_NONNUMERIC")
    if not value_ok:
        reasons.append("RESIDUAL_VALUE_MISSING_OR_NONNUMERIC")
    if not bound_ok:
        reasons.append("ARENA_BOUND_MISSING_OR_NONNUMERIC")
    if numeric_ready and not within_bound:
        reasons.append("PROJECTED_RESIDUAL_EXCEEDS_BOUND")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")
    if not public_authority:
        reasons.append("PUBLIC_AUTHORITY_FALSE")

    if valid_for_claim:
        status = "MATERIAL_REQ_VALUE_CLAIM_READY"
    elif material_ready:
        status = "MATERIAL_REQ_VALUE_SCHEMA_PASS_NONCLAIM"
    elif numeric_ready and not within_bound:
        status = "MATERIAL_REQ_VALUE_FAILS_BOUND"
    elif source_ok and as_bool(row.get("material_inventory_named")) and as_bool(row.get("source_candidates_recorded")):
        status = "MATERIAL_REQ_SOURCE_CANDIDATES_READY_VALUES_MISSING"
    elif source_ok:
        status = "MATERIAL_REQ_SOURCE_PRESENT_CLAUSES_OPEN"
    else:
        status = "MATERIAL_REQ_BLOCKED_MISSING_SOURCE"

    return {
        "row_id": row.get("row_id", ""),
        "arena": row.get("arena", ""),
        "quantity": row.get("quantity", ""),
        "input_path": str(input_path),
        "source_path": row.get("source_path", ""),
        "source_exists": source_ok,
        "failed_clauses": "|".join(failed),
        "projection_coeff": row.get("projection_coeff", ""),
        "residual_value": row.get("residual_value", ""),
        "arena_bound": row.get("arena_bound", ""),
        "numeric_ready": numeric_ready,
        "projected_residual": projected_residual,
        "within_bound": within_bound,
        "material_ready": material_ready,
        "input_valid_for_claim": input_valid,
        "public_authority": public_authority,
        "valid_for_claim": valid_for_claim,
        "claim_allowed": valid_for_claim,
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_ppn_rows(input_path: Path) -> List[Dict[str, object]]:
    return [evaluate_ppn_row(row, input_path) for row in read_csv(input_path)]


def evaluate_material_rows(input_path: Path) -> List[Dict[str, object]]:
    return [evaluate_material_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate source-universality pieces of the local PPN residual vector.")
    parser.add_argument("--mode", choices=["ppn", "material"], required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = evaluate_ppn_rows(args.input) if args.mode == "ppn" else evaluate_material_rows(args.input)
    write_csv(args.output, rows)


if __name__ == "__main__":
    main()
