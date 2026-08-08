from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


PNONHILBERT_CLAUSES = (
    "parent_selector_private",
    "kgamma_owner_constructed",
    "adjoint_gap_positive",
    "boundary_silent",
    "no_incoming_RI",
    "kperp_clean_sector",
)

OFF_WORLDTUBE_CLAUSES = (
    "parent_selector_private",
    "same_worldtube",
    "full_domain_before_readout",
    "no_inner_boundary",
    "trace_defect_zero",
)

BOUND_FIELDS = (
    "owner_tail_bound",
    "trace_defect_bound",
    "source_hair_bound",
    "projection_factor",
    "arena_bound",
)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Iterable[Dict[str, object]]) -> None:
    rows = [{key: str(value) for key, value in row.items()} for row in rows]
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_bool(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def parse_float(value: object) -> Tuple[bool, float]:
    try:
        text = str(value).strip()
        if not text or text.upper().startswith("MISSING"):
            return False, 0.0
        return True, float(text)
    except (TypeError, ValueError):
        return False, 0.0


def clauses_for(row: Dict[str, str]) -> Tuple[str, ...]:
    component = row.get("component", "")
    if component == "P_nonHilbert_action_domain":
        return PNONHILBERT_CLAUSES
    if component == "P_off_worldtube_readout_order":
        return OFF_WORLDTUBE_CLAUSES
    return PNONHILBERT_CLAUSES + OFF_WORLDTUBE_CLAUSES


def evaluate_zero_row(row: Dict[str, str], input_path: Path) -> Dict[str, object]:
    source_path = row.get("source_path", "")
    source_exists = bool(source_path) and Path(source_path).exists()
    clauses = clauses_for(row)
    failed_clauses = [clause for clause in clauses if not parse_bool(row.get(clause, ""))]
    private_zero = source_exists and not failed_clauses
    public_authority = parse_bool(row.get("public_authority", "False"))
    input_valid = parse_bool(row.get("input_valid_for_claim", "False"))
    valid_for_claim = private_zero and public_authority and input_valid
    if valid_for_claim:
        status = "PLEAK_COMPONENT_ZERO_CLAIM_READY"
    elif private_zero:
        status = "PLEAK_COMPONENT_PRIVATE_ZERO_NONCLAIM"
    else:
        status = "PLEAK_COMPONENT_ZERO_BLOCKED"
    reasons = []
    if not source_exists:
        reasons.append("SOURCE_PATH_MISSING")
    reasons.extend(f"OPEN_{clause.upper()}" for clause in failed_clauses)
    if not public_authority:
        reasons.append("PUBLIC_AUTHORITY_FALSE")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")
    return {
        "component_id": row.get("component_id", ""),
        "component": row.get("component", ""),
        "branch": row.get("branch", ""),
        "input_path": str(input_path),
        "source_path": source_path,
        "source_exists": source_exists,
        "required_clauses": "|".join(clauses),
        "failed_clauses": "|".join(failed_clauses),
        "private_zero": private_zero,
        "public_authority": public_authority,
        "input_valid_for_claim": input_valid,
        "valid_for_claim": valid_for_claim,
        "claim_allowed": valid_for_claim,
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_bound_row(row: Dict[str, str], input_path: Path) -> Dict[str, object]:
    source_path = row.get("source_path", "")
    source_exists = bool(source_path) and Path(source_path).exists()
    parsed = {field: parse_float(row.get(field, "")) for field in BOUND_FIELDS}
    numeric_ready = all(ok for ok, _ in parsed.values())
    if numeric_ready:
        owner_tail = parsed["owner_tail_bound"][1]
        trace_defect = parsed["trace_defect_bound"][1]
        source_hair = parsed["source_hair_bound"][1]
        projection = parsed["projection_factor"][1]
        arena_bound = parsed["arena_bound"][1]
        total = abs(projection) * (abs(owner_tail) + abs(trace_defect) + abs(source_hair))
        within_bound = total <= arena_bound
    else:
        total = ""
        within_bound = False
    input_valid = parse_bool(row.get("input_valid_for_claim", "False"))
    valid_for_claim = source_exists and numeric_ready and within_bound and input_valid
    reasons = []
    if not source_exists:
        reasons.append("SOURCE_PATH_MISSING")
    reasons.extend(f"MISSING_{field.upper()}" for field, (ok, _) in parsed.items() if not ok)
    if numeric_ready and not within_bound:
        reasons.append("PLEAK_BOUND_EXCEEDS_ARENA")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")
    if valid_for_claim:
        status = "PLEAK_BOUND_CLAIM_READY"
    elif numeric_ready and source_exists and within_bound:
        status = "PLEAK_BOUND_SCHEMA_READY_NONCLAIM"
    elif numeric_ready and source_exists:
        status = "PLEAK_BOUND_FAILS"
    else:
        status = "PLEAK_BOUND_BLOCKED"
    return {
        "bound_id": row.get("bound_id", ""),
        "branch": row.get("branch", ""),
        "arena": row.get("arena", ""),
        "input_path": str(input_path),
        "source_path": source_path,
        "source_exists": source_exists,
        "numeric_ready": numeric_ready,
        "owner_tail_bound": row.get("owner_tail_bound", ""),
        "trace_defect_bound": row.get("trace_defect_bound", ""),
        "source_hair_bound": row.get("source_hair_bound", ""),
        "projection_factor": row.get("projection_factor", ""),
        "total_projected_bound": "" if total == "" else f"{total:.12g}",
        "arena_bound": row.get("arena_bound", ""),
        "within_bound": within_bound,
        "input_valid_for_claim": input_valid,
        "valid_for_claim": valid_for_claim,
        "claim_allowed": valid_for_claim,
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_zero_rows(input_path: Path) -> List[Dict[str, object]]:
    return [evaluate_zero_row(row, input_path) for row in read_csv(input_path)]


def evaluate_bound_rows(input_path: Path) -> List[Dict[str, object]]:
    return [evaluate_bound_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Gate the first two transition-shell P_leak components.")
    parser.add_argument("--mode", choices=["zero", "bound"], required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.mode == "zero":
        write_csv(args.output, evaluate_zero_rows(args.input))
    else:
        write_csv(args.output, evaluate_bound_rows(args.input))


if __name__ == "__main__":
    main()
