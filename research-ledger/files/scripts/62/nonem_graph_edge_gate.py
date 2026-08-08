from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


TRUE_VALUES = {"1", "true", "yes", "y", "pass", "signed", "derived_zero"}
MISSING_PREFIXES = ("MISSING_", "PENDING_", "PLACEHOLDER_", "SCHEMA_", "NOT_", "UNKNOWN_")

ROOT_EDGE_CLAUSES = (
    "standard_lmatter_present",
    "metric_variation_to_hilbert_stress",
    "same_parent_measure",
    "nonEM_total_block",
    "current_before_readout",
    "no_species_prefactor_for_total_block",
    "component_decomposition_not_claimed",
)

SPECIES_EDGE_CLAUSES = (
    "template_edge_present",
    "standard_action_term_present",
    "same_parent_action_line",
    "parent_owned_morphism",
    "nonzero_morphism",
    "source_current_owner",
    "no_species_prefactor",
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


def evaluate_root_edge_row(row: Dict[str, str], input_path: Path) -> Dict[str, object]:
    source_ok = path_exists(row.get("source_path", ""))
    input_valid = as_bool(row.get("input_valid_for_claim", "False"))
    public_authority = as_bool(row.get("public_authority", "False"))
    failed = [clause for clause in ROOT_EDGE_CLAUSES if not as_bool(row.get(clause, ""))]
    root_edge_signed = source_ok and not failed
    valid_for_claim = root_edge_signed and input_valid and public_authority

    reasons = []
    if not source_ok:
        reasons.append("SOURCE_PATH_MISSING")
    reasons.extend(f"OPEN_{clause.upper()}" for clause in failed)
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")
    if not public_authority:
        reasons.append("PUBLIC_AUTHORITY_FALSE")

    if valid_for_claim:
        status = "NONEM_HILBERT_STRESS_ROOT_EDGE_CLAIM_READY"
    elif root_edge_signed:
        status = "NONEM_HILBERT_STRESS_ROOT_EDGE_SIGNED_BRANCH_NONCLAIM"
    elif source_ok and as_bool(row.get("standard_lmatter_present")) and as_bool(row.get("metric_variation_to_hilbert_stress")):
        status = "NONEM_HILBERT_STRESS_ROOT_EDGE_PARTIAL_COUNTERCLAUSES_OPEN"
    elif source_ok:
        status = "NONEM_HILBERT_STRESS_ROOT_EDGE_SOURCE_PRESENT_CLAUSES_OPEN"
    else:
        status = "NONEM_HILBERT_STRESS_ROOT_EDGE_BLOCKED_MISSING_SOURCE"

    return {
        "row_id": row.get("row_id", ""),
        "edge": row.get("edge", ""),
        "source_block": row.get("source_block", ""),
        "target_object": row.get("target_object", ""),
        "input_path": str(input_path),
        "source_path": row.get("source_path", ""),
        "source_exists": source_ok,
        "failed_clauses": "|".join(failed),
        "root_edge_signed": root_edge_signed,
        "input_valid_for_claim": input_valid,
        "public_authority": public_authority,
        "valid_for_claim": valid_for_claim,
        "claim_allowed": valid_for_claim,
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_species_edge_row(row: Dict[str, str], input_path: Path) -> Dict[str, object]:
    source_ok = path_exists(row.get("source_path", ""))
    input_valid = as_bool(row.get("input_valid_for_claim", "False"))
    public_authority = as_bool(row.get("public_authority", "False"))
    failed = [clause for clause in SPECIES_EDGE_CLAUSES if not as_bool(row.get(clause, ""))]
    parent_edge_signed = source_ok and not failed
    template_only = source_ok and as_bool(row.get("template_edge_present")) and not as_bool(row.get("parent_owned_morphism"))
    valid_for_claim = parent_edge_signed and input_valid and public_authority

    reasons = []
    if not source_ok:
        reasons.append("SOURCE_PATH_MISSING")
    reasons.extend(f"OPEN_{clause.upper()}" for clause in failed)
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")
    if not public_authority:
        reasons.append("PUBLIC_AUTHORITY_FALSE")

    if valid_for_claim:
        status = "NONEM_SPECIES_GRAPH_EDGE_CLAIM_READY"
    elif parent_edge_signed:
        status = "NONEM_SPECIES_GRAPH_EDGE_CONTRACT_READY_NONCLAIM"
    elif template_only:
        status = "NONEM_SPECIES_GRAPH_EDGE_TEMPLATE_ONLY_PARENT_SIGNATURE_MISSING"
    elif source_ok:
        status = "NONEM_SPECIES_GRAPH_EDGE_SOURCE_PRESENT_CLAUSES_OPEN"
    else:
        status = "NONEM_SPECIES_GRAPH_EDGE_BLOCKED_MISSING_SOURCE"

    return {
        "edge_id": row.get("edge_id", ""),
        "edge": row.get("edge", ""),
        "source_node": row.get("source_node", ""),
        "target_node": row.get("target_node", ""),
        "input_path": str(input_path),
        "source_path": row.get("source_path", ""),
        "source_exists": source_ok,
        "failed_clauses": "|".join(failed),
        "parent_edge_signed": parent_edge_signed,
        "template_only": template_only,
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
        reasons.append("MISSING_PROJECTION_COEFF")
    if not value_ok:
        reasons.append("MISSING_TAIL_VALUE")
    if not bound_ok:
        reasons.append("MISSING_ARENA_BOUND")
    if numeric_ready and not within_bound:
        reasons.append("TAIL_EXCEEDS_BOUND")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")
    if not public_authority:
        reasons.append("PUBLIC_AUTHORITY_FALSE")

    if valid_for_claim:
        status = "REQ_COMPACT_TEST_TAIL_CLAIM_READY"
    elif numeric_ready and within_bound:
        status = "REQ_COMPACT_TEST_TAIL_SCHEMA_PASS_NONCLAIM"
    elif numeric_ready:
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
        "projection_coeff": "" if not coeff_ok else f"{coeff:.12g}",
        "tail_value": row.get("tail_value", ""),
        "arena_bound": "" if not bound_ok else f"{bound:.12g}",
        "units": row.get("units", ""),
        "numeric_ready": numeric_ready,
        "allowed_tail_value": "" if allowed_tail_value == "" else f"{allowed_tail_value:.12g}",
        "projected_residual": "" if projected_residual == "" else f"{projected_residual:.12g}",
        "within_bound": within_bound,
        "input_valid_for_claim": input_valid,
        "public_authority": public_authority,
        "valid_for_claim": valid_for_claim,
        "claim_allowed": valid_for_claim,
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_root_edge_rows(input_path: Path) -> List[Dict[str, object]]:
    return [evaluate_root_edge_row(row, input_path) for row in read_csv(input_path)]


def evaluate_species_edge_rows(input_path: Path) -> List[Dict[str, object]]:
    return [evaluate_species_edge_row(row, input_path) for row in read_csv(input_path)]


def evaluate_tail_rows(input_path: Path) -> List[Dict[str, object]]:
    return [evaluate_tail_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate 4443 non-EM root/species graph edge and R_eq compact-test tail rows.")
    parser.add_argument("--mode", choices=["root", "species", "tail"], required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.mode == "root":
        write_csv(args.output, evaluate_root_edge_rows(args.input))
    elif args.mode == "species":
        write_csv(args.output, evaluate_species_edge_rows(args.input))
    else:
        write_csv(args.output, evaluate_tail_rows(args.input))


if __name__ == "__main__":
    main()
