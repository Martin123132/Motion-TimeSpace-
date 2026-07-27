from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, Iterable, List


TRUE_VALUES = {"1", "true", "yes", "y", "pass", "signed", "proved", "ready"}


def as_bool(value: object) -> bool:
    return str(value).strip().lower() in TRUE_VALUES


def path_exists(value: object) -> bool:
    text = str(value).strip()
    return bool(text) and Path(text).exists()


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


def evaluate_condition_row(row: Dict[str, str]) -> Dict[str, object]:
    source_ok = path_exists(row.get("source_path", ""))
    private_ready = as_bool(row.get("private_ready", "False"))
    parent_signed = as_bool(row.get("parent_signed", "False"))
    public_claim_false = as_bool(row.get("public_claim_false", "True"))

    if source_ok and parent_signed:
        status = "PARENT_SIGNED_CONDITION_AVAILABLE"
    elif source_ok and private_ready:
        status = "PRIVATE_CONDITIONAL_INPUT_AVAILABLE"
    elif source_ok:
        status = "SOURCE_PRESENT_UNSIGNED_CONDITION"
    else:
        status = "SOURCE_MISSING"

    valid_for_claim = source_ok and parent_signed and not public_claim_false
    reasons = []
    if not source_ok:
        reasons.append("SOURCE_PATH_MISSING")
    if not parent_signed:
        reasons.append("PARENT_SIGNED_FALSE")
    if public_claim_false:
        reasons.append("PUBLIC_CLAIM_FALSE")

    return {
        "condition_id": row.get("condition_id", ""),
        "condition": row.get("condition", ""),
        "source_path": row.get("source_path", ""),
        "source_exists": source_ok,
        "private_ready": private_ready,
        "parent_signed": parent_signed,
        "public_claim_false": public_claim_false,
        "current_status": status,
        "valid_for_claim": valid_for_claim,
        "claim_allowed": valid_for_claim,
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
    }


def evaluate_theorem_row(row: Dict[str, str]) -> Dict[str, object]:
    source_ok = path_exists(row.get("source_path", ""))
    algebraic = as_bool(row.get("algebraic_no_derivatives", "False"))
    spinless_zero = as_bool(row.get("spinless_zero", "False"))
    long_range_zero = as_bool(row.get("long_range_zero", "False"))
    contact_remaining = as_bool(row.get("contact_remaining", "False"))
    open_parent_clause = as_bool(row.get("open_parent_clause", "True"))
    public_claim_false = as_bool(row.get("public_claim_false", "True"))

    if source_ok and algebraic and spinless_zero and long_range_zero and contact_remaining:
        status = "CONDITIONAL_SPINLESS_ZERO_CONTACT_CHANNEL_REMAINS"
    elif source_ok and algebraic and spinless_zero:
        status = "CONDITIONAL_SPINLESS_TORSION_ZERO"
    elif source_ok and contact_remaining:
        status = "CONTACT_BOUND_ROW_REQUIRED"
    elif source_ok:
        status = "THEOREM_ROW_SOURCE_PRESENT_OPEN"
    else:
        status = "SOURCE_MISSING"

    valid_for_claim = source_ok and algebraic and spinless_zero and long_range_zero and not contact_remaining and not open_parent_clause and not public_claim_false
    reasons = []
    if not source_ok:
        reasons.append("SOURCE_PATH_MISSING")
    if not algebraic:
        reasons.append("ALGEBRAIC_NO_DERIVATIVES_FALSE")
    if not spinless_zero:
        reasons.append("SPINLESS_ZERO_FALSE")
    if contact_remaining:
        reasons.append("CONTACT_CHANNEL_REMAINS")
    if open_parent_clause:
        reasons.append("OPEN_PARENT_CLAUSE_TRUE")
    if public_claim_false:
        reasons.append("PUBLIC_CLAIM_FALSE")

    return {
        "theorem_id": row.get("theorem_id", ""),
        "claim_piece": row.get("claim_piece", ""),
        "source_path": row.get("source_path", ""),
        "source_exists": source_ok,
        "equation_form": row.get("equation_form", ""),
        "algebraic_no_derivatives": algebraic,
        "spinless_zero": spinless_zero,
        "long_range_zero": long_range_zero,
        "contact_remaining": contact_remaining,
        "open_parent_clause": open_parent_clause,
        "current_status": status,
        "valid_for_claim": valid_for_claim,
        "claim_allowed": valid_for_claim,
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate the torsion-spin residual zero/contact-bound branch.")
    parser.add_argument("--mode", choices=["conditions", "theorem"], required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = read_csv(args.input)
    if args.mode == "conditions":
        output = [evaluate_condition_row(row) for row in rows]
    else:
        output = [evaluate_theorem_row(row) for row in rows]
    write_csv(args.output, output)


if __name__ == "__main__":
    main()
