from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


TRUE_VALUES = {"1", "true", "yes", "y", "pass", "signed", "derived_zero", "ready"}
MISSING_PREFIXES = ("MISSING_", "PENDING_", "PLACEHOLDER_", "SCHEMA_", "NOT_", "UNKNOWN_")

IMPORT_CLAUSES = (
    "standard_lmatter_slot_present",
    "total_hilbert_variation_signed",
    "component_import_edges_ready",
    "single_metric_measure",
    "matter_internal_constants_quarantined",
    "parent_import_clause_written",
    "variation_before_readout",
    "no_component_source_weight_in_import",
)

NO_PREFAC_CLAUSES = (
    "typed_domain_declared",
    "hom_species_to_source_empty",
    "action_density_line_unique",
    "source_label_forgetting",
    "selector_blind_source_action",
    "component_graph_connected_import",
    "readout_no_reentry",
    "material_projection_scope_declared",
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


def evaluate_import_row(row: Dict[str, str], input_path: Path) -> Dict[str, object]:
    source_ok = path_exists(row.get("source_path", ""))
    input_valid = as_bool(row.get("input_valid_for_claim", "False"))
    public_authority = as_bool(row.get("public_authority", "False"))
    adopted_by_parent = as_bool(row.get("adopted_by_parent", "False"))
    failed = [clause for clause in IMPORT_CLAUSES if not as_bool(row.get(clause, ""))]
    theorem_ready = source_ok and not failed
    valid_for_claim = theorem_ready and adopted_by_parent and input_valid and public_authority

    reasons = []
    if not source_ok:
        reasons.append("SOURCE_PATH_MISSING")
    reasons.extend(f"OPEN_{clause.upper()}" for clause in failed)
    if not adopted_by_parent:
        reasons.append("PARENT_ADOPTION_FALSE")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")
    if not public_authority:
        reasons.append("PUBLIC_AUTHORITY_FALSE")

    if valid_for_claim:
        status = "GR_PARITY_SM_IMPORT_CLAIM_READY"
    elif theorem_ready and not adopted_by_parent:
        status = "GR_PARITY_SM_IMPORT_THEOREM_READY_ADOPTION_OPEN_NONCLAIM"
    elif theorem_ready:
        status = "GR_PARITY_SM_IMPORT_CONTRACT_READY_NONCLAIM"
    elif source_ok:
        status = "GR_PARITY_SM_IMPORT_SOURCE_PRESENT_CLAUSES_OPEN"
    else:
        status = "GR_PARITY_SM_IMPORT_BLOCKED_MISSING_SOURCE"

    return {
        "row_id": row.get("row_id", ""),
        "branch": row.get("branch", ""),
        "object": row.get("object", ""),
        "input_path": str(input_path),
        "source_path": row.get("source_path", ""),
        "source_exists": source_ok,
        "failed_clauses": "|".join(failed),
        "theorem_ready": theorem_ready,
        "adopted_by_parent": adopted_by_parent,
        "input_valid_for_claim": input_valid,
        "public_authority": public_authority,
        "valid_for_claim": valid_for_claim,
        "claim_allowed": valid_for_claim,
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_no_prefac_row(row: Dict[str, str], input_path: Path) -> Dict[str, object]:
    source_ok = path_exists(row.get("source_path", ""))
    input_valid = as_bool(row.get("input_valid_for_claim", "False"))
    public_authority = as_bool(row.get("public_authority", "False"))
    adopted_by_parent = as_bool(row.get("adopted_by_parent", "False"))
    failed = [clause for clause in NO_PREFAC_CLAUSES if not as_bool(row.get(clause, ""))]
    theorem_ready = source_ok and not failed
    valid_for_claim = theorem_ready and adopted_by_parent and input_valid and public_authority

    reasons = []
    if not source_ok:
        reasons.append("SOURCE_PATH_MISSING")
    reasons.extend(f"OPEN_{clause.upper()}" for clause in failed)
    if not adopted_by_parent:
        reasons.append("PARENT_ADOPTION_FALSE")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")
    if not public_authority:
        reasons.append("PUBLIC_AUTHORITY_FALSE")

    if valid_for_claim:
        status = "NO_SOURCE_PREFAC_CLAIM_READY"
    elif theorem_ready and not adopted_by_parent:
        status = "NO_SOURCE_PREFAC_THEOREM_READY_ADOPTION_OPEN_NONCLAIM"
    elif theorem_ready:
        status = "NO_SOURCE_PREFAC_CONTRACT_READY_NONCLAIM"
    elif source_ok and as_bool(row.get("typed_domain_declared")) and as_bool(row.get("action_density_line_unique")):
        status = "NO_SOURCE_PREFAC_PARTIAL_TYPED_ACTION_READY"
    elif source_ok:
        status = "NO_SOURCE_PREFAC_SOURCE_PRESENT_CLAUSES_OPEN"
    else:
        status = "NO_SOURCE_PREFAC_BLOCKED_MISSING_SOURCE"

    return {
        "row_id": row.get("row_id", ""),
        "branch": row.get("branch", ""),
        "object": row.get("object", ""),
        "input_path": str(input_path),
        "source_path": row.get("source_path", ""),
        "source_exists": source_ok,
        "failed_clauses": "|".join(failed),
        "theorem_ready": theorem_ready,
        "adopted_by_parent": adopted_by_parent,
        "input_valid_for_claim": input_valid,
        "public_authority": public_authority,
        "valid_for_claim": valid_for_claim,
        "claim_allowed": valid_for_claim,
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_tail_row(row: Dict[str, str], input_path: Path) -> Dict[str, object]:
    source_ok = path_exists(row.get("source_path", ""))
    coeff_ok, coeff = parse_float(row.get("projection_coeff", ""))
    value_ok, value = parse_float(row.get("tail_value", ""))
    bound_ok, bound = parse_float(row.get("arena_bound", ""))
    numeric_ready = source_ok and coeff_ok and value_ok and bound_ok
    projected_residual = coeff * abs(value) if numeric_ready else ""
    allowed_tail_value = bound / coeff if numeric_ready and coeff > 0 else ""
    within_bound = bool(numeric_ready and float(projected_residual) <= bound)
    input_valid = as_bool(row.get("input_valid_for_claim", "False"))
    public_authority = as_bool(row.get("public_authority", "False"))
    valid_for_claim = numeric_ready and within_bound and input_valid and public_authority

    reasons = []
    if not source_ok:
        reasons.append("SOURCE_PATH_MISSING")
    if not coeff_ok:
        reasons.append("PROJECTION_COEFF_MISSING_OR_NONNUMERIC")
    if not value_ok:
        reasons.append("TAIL_VALUE_MISSING_OR_NONNUMERIC")
    if not bound_ok:
        reasons.append("ARENA_BOUND_MISSING_OR_NONNUMERIC")
    if numeric_ready and not within_bound:
        reasons.append("PROJECTED_RESIDUAL_EXCEEDS_BOUND")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")
    if not public_authority:
        reasons.append("PUBLIC_AUTHORITY_FALSE")

    if valid_for_claim:
        status = "REQ_COMPACT_TEST_TAIL_CLAIM_READY"
    elif numeric_ready and within_bound:
        status = "REQ_COMPACT_TEST_TAIL_SCHEMA_PASS_NONCLAIM"
    elif numeric_ready and not within_bound:
        status = "REQ_COMPACT_TEST_TAIL_FAILS_BOUND"
    elif source_ok:
        status = "REQ_COMPACT_TEST_TAIL_VALUES_MISSING"
    else:
        status = "REQ_COMPACT_TEST_TAIL_BLOCKED_MISSING_SOURCE"

    return {
        "tail_id": row.get("tail_id", ""),
        "quantity": row.get("quantity", ""),
        "arena": row.get("arena", ""),
        "distributional_definition": row.get("distributional_definition", ""),
        "input_path": str(input_path),
        "source_path": row.get("source_path", ""),
        "source_exists": source_ok,
        "projection_coeff": row.get("projection_coeff", ""),
        "tail_value": row.get("tail_value", ""),
        "arena_bound": row.get("arena_bound", ""),
        "numeric_ready": numeric_ready,
        "projected_residual": projected_residual,
        "allowed_tail_value": allowed_tail_value,
        "within_bound": within_bound,
        "input_valid_for_claim": input_valid,
        "public_authority": public_authority,
        "valid_for_claim": valid_for_claim,
        "claim_allowed": valid_for_claim,
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_import_rows(input_path: Path) -> List[Dict[str, object]]:
    return [evaluate_import_row(row, input_path) for row in read_csv(input_path)]


def evaluate_no_prefac_rows(input_path: Path) -> List[Dict[str, object]]:
    return [evaluate_no_prefac_row(row, input_path) for row in read_csv(input_path)]


def evaluate_tail_rows(input_path: Path) -> List[Dict[str, object]]:
    return [evaluate_tail_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate GR-parity SM import and no-source-prefactor gates.")
    parser.add_argument("--mode", choices=["import", "noprefac", "tail"], required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.mode == "import":
        rows = evaluate_import_rows(args.input)
    elif args.mode == "noprefac":
        rows = evaluate_no_prefac_rows(args.input)
    else:
        rows = evaluate_tail_rows(args.input)
    write_csv(args.output, rows)


if __name__ == "__main__":
    main()
