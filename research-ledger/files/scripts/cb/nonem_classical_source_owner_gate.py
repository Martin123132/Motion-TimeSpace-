from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


TRUE_VALUES = {"1", "true", "yes", "y", "pass", "signed", "derived_zero"}
MISSING_PREFIXES = ("MISSING_", "PENDING_", "PLACEHOLDER_", "SCHEMA_", "NOT_", "UNKNOWN_")

CLASSICAL_OWNER_CLAUSES = (
    "one_classical_parent_action",
    "common_classical_measure",
    "variation_before_readout",
    "action_density_owner",
    "typed_no_source_hom",
    "constructor_exhaustion",
    "hidden_readout_no_reentry",
    "parent_connected_graph",
    "derivative_silent_common_mode",
    "total_hilbert_current_owner",
    "fixed_EM_subcontract_removed",
)

LOCAL_CLOSURE_CLAUSES = (
    "same_current_Req_zero",
    "B_zero_flux_silent",
    "Htau_MHref_locks",
)

QUANTUM_GUARD_CLAUSES = (
    "universal_hbar_parent",
    "quantum_measure_owner",
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


def evaluate_route_row(row: Dict[str, str], input_path: Path) -> Dict[str, object]:
    source_ok = path_exists(row.get("source_path", ""))
    public_authority = as_bool(row.get("public_authority", "False"))
    input_valid = as_bool(row.get("input_valid_for_claim", "False"))
    classical_failed = [clause for clause in CLASSICAL_OWNER_CLAUSES if not as_bool(row.get(clause, ""))]
    local_failed = [clause for clause in LOCAL_CLOSURE_CLAUSES if not as_bool(row.get(clause, ""))]
    quantum_failed = [clause for clause in QUANTUM_GUARD_CLAUSES if not as_bool(row.get(clause, ""))]
    classical_owner_closed = source_ok and not classical_failed
    local_source_closed = classical_owner_closed and not local_failed
    quantum_guard_closed = source_ok and not quantum_failed
    hbar_only = quantum_guard_closed and not classical_owner_closed
    valid_for_claim = local_source_closed and public_authority and input_valid

    reasons = []
    if not source_ok:
        reasons.append("SOURCE_PATH_MISSING")
    reasons.extend(f"OPEN_{clause.upper()}" for clause in classical_failed)
    reasons.extend(f"OPEN_{clause.upper()}" for clause in local_failed)
    if not quantum_guard_closed:
        reasons.extend(f"QUANTUM_GUARD_OPEN_{clause.upper()}" for clause in quantum_failed)
    if not public_authority:
        reasons.append("PUBLIC_AUTHORITY_FALSE")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")

    if valid_for_claim:
        status = "NONEM_LOCAL_SOURCE_OWNER_CLAIM_READY"
    elif hbar_only:
        status = "HBAR_MEASURE_OWNER_ALONE_INSUFFICIENT_FOR_LOCAL_SOURCE"
    elif local_source_closed and not quantum_guard_closed:
        status = "CLASSICAL_LOCAL_SOURCE_OWNER_CONTRACT_READY_HBAR_QUANTUM_GUARD_OPEN_NONCLAIM"
    elif classical_owner_closed:
        status = "CLASSICAL_OWNER_ZERO_READY_REQ_BZERO_HTAU_OPEN_NONCLAIM"
    elif as_bool(row.get("fixed_EM_subcontract_removed")) and source_ok:
        status = "CLASSICAL_SOURCE_OWNER_CLAUSES_OPEN_EM_REMOVED"
    elif source_ok:
        status = "NONEM_SOURCE_OWNER_CLAUSES_OPEN"
    else:
        status = "NONEM_SOURCE_OWNER_BLOCKED_MISSING_SOURCE"

    return {
        "row_id": row.get("row_id", ""),
        "branch": row.get("branch", ""),
        "input_path": str(input_path),
        "source_path": row.get("source_path", ""),
        "source_exists": source_ok,
        "classical_failed_clauses": "|".join(classical_failed),
        "local_failed_clauses": "|".join(local_failed),
        "quantum_guard_failed_clauses": "|".join(quantum_failed),
        "classical_owner_closed": classical_owner_closed,
        "local_source_closed": local_source_closed,
        "quantum_guard_closed": quantum_guard_closed,
        "hbar_only_inadequate": hbar_only,
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
    projected_residual = coeff * abs(value) if numeric_ready else ""
    allowed_tail_value = bound / coeff if numeric_ready and coeff > 0 else ""
    within_bound = bool(numeric_ready and float(projected_residual) <= bound)
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
        status = "REQ_BZERO_TAIL_CLAIM_READY"
    elif numeric_ready and within_bound:
        status = "REQ_BZERO_TAIL_SCHEMA_PASS_NONCLAIM"
    elif numeric_ready:
        status = "REQ_BZERO_TAIL_FAILS_BOUND"
    elif source_ok:
        status = "REQ_BZERO_TAIL_VALUES_MISSING"
    else:
        status = "REQ_BZERO_TAIL_BLOCKED_MISSING_SOURCE"

    return {
        "tail_id": row.get("tail_id", ""),
        "quantity": row.get("quantity", ""),
        "target": row.get("target", ""),
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
        "valid_for_claim": valid_for_claim,
        "claim_allowed": valid_for_claim,
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_route_rows(input_path: Path) -> List[Dict[str, object]]:
    return [evaluate_route_row(row, input_path) for row in read_csv(input_path)]


def evaluate_tail_rows(input_path: Path) -> List[Dict[str, object]]:
    return [evaluate_tail_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate 4442 non-EM classical source-owner and R_eq/B_zero tail rows.")
    parser.add_argument("--mode", choices=["route", "tail"], required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.mode == "route":
        write_csv(args.output, evaluate_route_rows(args.input))
    else:
        write_csv(args.output, evaluate_tail_rows(args.input))


if __name__ == "__main__":
    main()
