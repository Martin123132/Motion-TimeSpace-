from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


TRUE_VALUES = {"1", "true", "yes", "y", "pass", "signed", "derived_zero", "ready", "adopted"}
MISSING_PREFIXES = ("MISSING_", "PENDING_", "PLACEHOLDER_", "SCHEMA_", "NOT_", "UNKNOWN_")

ADOPTION_CLAUSES = (
    "private_scope_declared",
    "standard_lmatter_slot_present",
    "hilbert_variation_before_readout",
    "component_import_graph_ready",
    "no_source_prefactor_theorem_ready",
    "source_label_forgetting_ready",
    "material_projection_readout_only",
    "countermodels_killed",
    "strict_primitive_derivation_not_claimed",
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


def evaluate_adoption_row(row: Dict[str, str], input_path: Path) -> Dict[str, object]:
    source_ok = path_exists(row.get("source_path", ""))
    private_adoption = as_bool(row.get("private_branch_adoption", "False"))
    strict_primitive_derived = as_bool(row.get("strict_primitive_derived", "False"))
    public_authority = as_bool(row.get("public_authority", "False"))
    input_valid = as_bool(row.get("input_valid_for_claim", "False"))
    failed = [clause for clause in ADOPTION_CLAUSES if not as_bool(row.get(clause, ""))]
    invariant_ready = source_ok and not failed
    private_adopted = invariant_ready and private_adoption
    valid_for_claim = private_adopted and strict_primitive_derived and public_authority and input_valid

    reasons = []
    if not source_ok:
        reasons.append("SOURCE_PATH_MISSING")
    reasons.extend(f"OPEN_{clause.upper()}" for clause in failed)
    if not private_adoption:
        reasons.append("PRIVATE_BRANCH_ADOPTION_FALSE")
    if not strict_primitive_derived:
        reasons.append("STRICT_PRIMITIVE_DERIVATION_FALSE")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")
    if not public_authority:
        reasons.append("PUBLIC_AUTHORITY_FALSE")

    if valid_for_claim:
        status = "GR_PARITY_SM_IMPORT_PUBLIC_CLAIM_READY"
    elif private_adopted:
        status = "GR_PARITY_SM_IMPORT_PRIVATE_BRANCH_ADOPTED_NONCLAIM"
    elif invariant_ready:
        status = "GR_PARITY_SM_IMPORT_ADOPTION_INVARIANT_READY_NONCLAIM"
    elif source_ok and as_bool(row.get("standard_lmatter_slot_present")):
        status = "GR_PARITY_SM_IMPORT_ADOPTION_PARTIAL_CLAUSES_OPEN"
    elif source_ok:
        status = "GR_PARITY_SM_IMPORT_ADOPTION_SOURCE_PRESENT_CLAUSES_OPEN"
    else:
        status = "GR_PARITY_SM_IMPORT_ADOPTION_BLOCKED_MISSING_SOURCE"

    return {
        "row_id": row.get("row_id", ""),
        "branch": row.get("branch", ""),
        "invariant": row.get("invariant", ""),
        "input_path": str(input_path),
        "source_path": row.get("source_path", ""),
        "source_exists": source_ok,
        "failed_clauses": "|".join(failed),
        "invariant_ready": invariant_ready,
        "private_branch_adoption": private_adoption,
        "private_adopted": private_adopted,
        "strict_primitive_derived": strict_primitive_derived,
        "input_valid_for_claim": input_valid,
        "public_authority": public_authority,
        "valid_for_claim": valid_for_claim,
        "claim_allowed": valid_for_claim,
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


def evaluate_adoption_rows(input_path: Path) -> List[Dict[str, object]]:
    return [evaluate_adoption_row(row, input_path) for row in read_csv(input_path)]


def evaluate_material_rows(input_path: Path) -> List[Dict[str, object]]:
    return [evaluate_material_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate GR-parity import adoption and material residual gates.")
    parser.add_argument("--mode", choices=["adoption", "material"], required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = evaluate_adoption_rows(args.input) if args.mode == "adoption" else evaluate_material_rows(args.input)
    write_csv(args.output, rows)


if __name__ == "__main__":
    main()
