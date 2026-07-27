from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


TRUE_VALUES = {"1", "true", "yes", "y", "pass", "signed", "derived_zero"}
MISSING_PREFIXES = ("MISSING_", "PENDING_", "PLACEHOLDER_", "SCHEMA_", "NOT_", "UNKNOWN_")

OWNER_CLAUSES = (
    "single_phase_seed",
    "universal_hbar_parent",
    "universal_measure_owner",
    "action_density_owner",
    "constructor_exhaustion",
    "hom_species_to_source_empty",
    "connected_matter_graph",
    "total_source_current_owner",
    "fixed_EM_edge_signed",
    "fixed_EM_tail_zero",
    "same_current_Req_zero",
    "boundary_improvement_zero_flux",
    "Htau_MHref_locks",
    "no_readout_reentry",
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


def evaluate_owner_row(row: Dict[str, str], input_path: Path) -> Dict[str, object]:
    source_ok = path_exists(row.get("source_path", ""))
    public_authority = as_bool(row.get("public_authority", "False"))
    input_valid = as_bool(row.get("input_valid_for_claim", "False"))
    failed = [clause for clause in OWNER_CLAUSES if not as_bool(row.get(clause, ""))]
    em_subcontract_closed = source_ok and as_bool(row.get("fixed_EM_edge_signed")) and as_bool(row.get("fixed_EM_tail_zero"))
    total_owner_closed = source_ok and not failed
    nonem_owner_closed = source_ok and all(
        as_bool(row.get(clause, ""))
        for clause in (
            "single_phase_seed",
            "universal_hbar_parent",
            "universal_measure_owner",
            "action_density_owner",
            "constructor_exhaustion",
            "hom_species_to_source_empty",
            "connected_matter_graph",
            "total_source_current_owner",
            "same_current_Req_zero",
            "boundary_improvement_zero_flux",
            "Htau_MHref_locks",
            "no_readout_reentry",
        )
    )
    valid_for_claim = total_owner_closed and public_authority and input_valid
    reasons = []
    if not source_ok:
        reasons.append("SOURCE_PATH_MISSING")
    reasons.extend(f"OPEN_{clause.upper()}" for clause in failed)
    if not public_authority:
        reasons.append("PUBLIC_AUTHORITY_FALSE")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")

    if valid_for_claim:
        status = "ACTION_MEASURE_CURRENT_OWNER_CLAIM_READY"
    elif em_subcontract_closed and not nonem_owner_closed:
        status = "FIXED_EM_OWNER_SUBCONTRACT_CLOSED_NONEM_OWNER_OPEN"
    elif total_owner_closed:
        status = "ACTION_MEASURE_CURRENT_OWNER_CONTRACT_READY_NONCLAIM"
    elif source_ok:
        status = "ACTION_MEASURE_CURRENT_OWNER_CLAUSES_OPEN"
    else:
        status = "ACTION_MEASURE_CURRENT_OWNER_BLOCKED_MISSING_SOURCE"

    return {
        "owner_id": row.get("owner_id", ""),
        "branch": row.get("branch", ""),
        "input_path": str(input_path),
        "source_path": row.get("source_path", ""),
        "source_exists": source_ok,
        "failed_clauses": "|".join(failed),
        "em_subcontract_closed": em_subcontract_closed,
        "nonem_owner_closed": nonem_owner_closed,
        "total_owner_closed": total_owner_closed,
        "public_authority": public_authority,
        "input_valid_for_claim": input_valid,
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
    residual = coeff * abs(value) if numeric_ready else ""
    allowed_value = bound / coeff if numeric_ready and coeff > 0 else ""
    within_bound = bool(numeric_ready and float(residual) <= bound)
    input_valid = as_bool(row.get("input_valid_for_claim", "False"))
    valid_for_claim = numeric_ready and within_bound and input_valid
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

    if valid_for_claim:
        status = "OWNER_TAIL_CLAIM_READY"
    elif numeric_ready and within_bound:
        status = "OWNER_TAIL_SCHEMA_PASS_NONCLAIM"
    elif numeric_ready:
        status = "OWNER_TAIL_FAILS_BOUND"
    elif source_ok:
        status = "OWNER_TAIL_VALUES_MISSING"
    else:
        status = "OWNER_TAIL_BLOCKED_MISSING_SOURCE"

    return {
        "tail_id": row.get("tail_id", ""),
        "tail": row.get("tail", ""),
        "arena": row.get("arena", ""),
        "normal_form": row.get("normal_form", ""),
        "input_path": str(input_path),
        "source_path": row.get("source_path", ""),
        "source_exists": source_ok,
        "projection_coeff": "" if not coeff_ok else f"{coeff:.12g}",
        "tail_value": row.get("tail_value", ""),
        "arena_bound": "" if not bound_ok else f"{bound:.12g}",
        "units": row.get("units", ""),
        "numeric_ready": numeric_ready,
        "allowed_tail_value": "" if allowed_value == "" else f"{allowed_value:.12g}",
        "projected_residual": "" if residual == "" else f"{residual:.12g}",
        "within_bound": within_bound,
        "input_valid_for_claim": input_valid,
        "valid_for_claim": valid_for_claim,
        "claim_allowed": valid_for_claim,
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_owner_rows(input_path: Path) -> List[Dict[str, object]]:
    return [evaluate_owner_row(row, input_path) for row in read_csv(input_path)]


def evaluate_tail_rows(input_path: Path) -> List[Dict[str, object]]:
    return [evaluate_tail_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate 4441 action-measure/current owner and finite tail rows.")
    parser.add_argument("--mode", choices=["owner", "tail"], required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.mode == "owner":
        write_csv(args.output, evaluate_owner_rows(args.input))
    else:
        write_csv(args.output, evaluate_tail_rows(args.input))


if __name__ == "__main__":
    main()
