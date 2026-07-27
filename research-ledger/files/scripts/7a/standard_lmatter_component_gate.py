from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


TRUE_VALUES = {"1", "true", "yes", "y", "pass", "signed", "derived_zero", "imported"}
MISSING_PREFIXES = ("MISSING_", "PENDING_", "PLACEHOLDER_", "SCHEMA_", "NOT_", "UNKNOWN_")

STANDARD_COMPONENT_CLAUSES = (
    "template_edge_present",
    "standard_lmatter_imported",
    "component_action_term_named",
    "same_metric_measure",
    "nonzero_standard_morphism",
    "source_current_before_readout",
    "no_species_prefactor_in_import",
    "readout_no_reentry",
)

PARENT_COMPONENT_CLAUSES = (
    "mts_parent_derives_component_action",
    "representation_constants_derived_or_import_contract",
    "yukawa_mass_terms_derived_or_import_contract",
    "material_projection_sourced",
    "no_source_prefactor_parent_signed",
    "source_current_before_readout",
    "readout_no_reentry",
    "constructor_exhaustion_signed",
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


def evaluate_standard_component_row(row: Dict[str, str], input_path: Path) -> Dict[str, object]:
    source_ok = path_exists(row.get("source_path", ""))
    input_valid = as_bool(row.get("input_valid_for_claim", "False"))
    public_authority = as_bool(row.get("public_authority", "False"))
    parent_derived_by_mts = as_bool(row.get("parent_derived_by_MTS", "False"))
    failed = [clause for clause in STANDARD_COMPONENT_CLAUSES if not as_bool(row.get(clause, ""))]
    import_edge_ready = source_ok and not failed
    template_only = source_ok and as_bool(row.get("template_edge_present")) and not as_bool(row.get("standard_lmatter_imported"))
    valid_for_claim = import_edge_ready and parent_derived_by_mts and input_valid and public_authority

    reasons = []
    if not source_ok:
        reasons.append("SOURCE_PATH_MISSING")
    reasons.extend(f"OPEN_{clause.upper()}" for clause in failed)
    if not parent_derived_by_mts:
        reasons.append("MTS_PARENT_DERIVATION_FALSE")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")
    if not public_authority:
        reasons.append("PUBLIC_AUTHORITY_FALSE")

    if valid_for_claim:
        status = "STANDARD_COMPONENT_EDGE_PARENT_CLAIM_READY"
    elif import_edge_ready and not parent_derived_by_mts:
        status = "STANDARD_COMPONENT_EDGE_IMPORT_READY_PARENT_DERIVATION_OPEN_NONCLAIM"
    elif import_edge_ready:
        status = "STANDARD_COMPONENT_EDGE_IMPORT_CONTRACT_READY_NONCLAIM"
    elif template_only:
        status = "STANDARD_COMPONENT_EDGE_TEMPLATE_ONLY_IMPORT_MISSING"
    elif source_ok:
        status = "STANDARD_COMPONENT_EDGE_SOURCE_PRESENT_CLAUSES_OPEN"
    else:
        status = "STANDARD_COMPONENT_EDGE_BLOCKED_MISSING_SOURCE"

    return {
        "edge_id": row.get("edge_id", ""),
        "edge": row.get("edge", ""),
        "source_node": row.get("source_node", ""),
        "target_node": row.get("target_node", ""),
        "branch": row.get("branch", ""),
        "input_path": str(input_path),
        "source_path": row.get("source_path", ""),
        "source_exists": source_ok,
        "failed_clauses": "|".join(failed),
        "import_edge_ready": import_edge_ready,
        "parent_derived_by_MTS": parent_derived_by_mts,
        "template_only": template_only,
        "input_valid_for_claim": input_valid,
        "public_authority": public_authority,
        "valid_for_claim": valid_for_claim,
        "claim_allowed": valid_for_claim,
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_parent_component_row(row: Dict[str, str], input_path: Path) -> Dict[str, object]:
    source_ok = path_exists(row.get("source_path", ""))
    input_valid = as_bool(row.get("input_valid_for_claim", "False"))
    public_authority = as_bool(row.get("public_authority", "False"))
    failed = [clause for clause in PARENT_COMPONENT_CLAUSES if not as_bool(row.get(clause, ""))]
    parent_contract_ready = source_ok and not failed
    valid_for_claim = parent_contract_ready and input_valid and public_authority

    reasons = []
    if not source_ok:
        reasons.append("SOURCE_PATH_MISSING")
    reasons.extend(f"OPEN_{clause.upper()}" for clause in failed)
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")
    if not public_authority:
        reasons.append("PUBLIC_AUTHORITY_FALSE")

    if valid_for_claim:
        status = "PARENT_COMPONENT_DERIVATION_CLAIM_READY"
    elif parent_contract_ready:
        status = "PARENT_COMPONENT_DERIVATION_CONTRACT_READY_NONCLAIM"
    elif source_ok and as_bool(row.get("mts_parent_derives_component_action")):
        status = "PARENT_COMPONENT_DERIVATION_PARTIAL_COUNTERCLAUSES_OPEN"
    elif source_ok:
        status = "PARENT_COMPONENT_DERIVATION_OPEN"
    else:
        status = "PARENT_COMPONENT_DERIVATION_BLOCKED_MISSING_SOURCE"

    return {
        "cert_id": row.get("cert_id", ""),
        "branch": row.get("branch", ""),
        "object": row.get("object", ""),
        "input_path": str(input_path),
        "source_path": row.get("source_path", ""),
        "source_exists": source_ok,
        "failed_clauses": "|".join(failed),
        "parent_contract_ready": parent_contract_ready,
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


def evaluate_standard_component_rows(input_path: Path) -> List[Dict[str, object]]:
    return [evaluate_standard_component_row(row, input_path) for row in read_csv(input_path)]


def evaluate_parent_component_rows(input_path: Path) -> List[Dict[str, object]]:
    return [evaluate_parent_component_row(row, input_path) for row in read_csv(input_path)]


def evaluate_tail_rows(input_path: Path) -> List[Dict[str, object]]:
    return [evaluate_tail_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate standard L_matter component expansion gates.")
    parser.add_argument("--mode", choices=["standard", "parent", "tail"], required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.mode == "standard":
        rows = evaluate_standard_component_rows(args.input)
    elif args.mode == "parent":
        rows = evaluate_parent_component_rows(args.input)
    else:
        rows = evaluate_tail_rows(args.input)
    write_csv(args.output, rows)


if __name__ == "__main__":
    main()
