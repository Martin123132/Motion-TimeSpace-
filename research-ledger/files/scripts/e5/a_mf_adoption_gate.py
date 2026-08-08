from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, Iterable, List


TRUE_VALUES = {"1", "true", "yes", "y", "pass", "signed", "adopted", "proved", "ready"}
MISSING_PREFIXES = ("MISSING_", "PENDING_", "PLACEHOLDER_", "UNKNOWN_", "NOT_")


def as_bool(value: object) -> bool:
    return str(value).strip().lower() in TRUE_VALUES


def is_missing_like(value: object) -> bool:
    text = str(value).strip()
    return not text or any(text.startswith(prefix) for prefix in MISSING_PREFIXES)


def path_exists(value: object) -> bool:
    text = str(value).strip()
    return bool(text) and not is_missing_like(text) and Path(text).exists()


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


def evaluate_evidence_row(row: Dict[str, str], input_path: Path) -> Dict[str, object]:
    source_ok = path_exists(row.get("source_path", ""))
    supports = as_bool(row.get("supports_A_MF", "False"))
    proves = as_bool(row.get("proves_A_MF", "False"))
    counter = as_bool(row.get("counterevidence", "False"))
    adoption_ready = as_bool(row.get("adoption_ready", "False"))
    public_claim_false = as_bool(row.get("public_claim_false", "False"))

    if source_ok and proves and not counter:
        status = "OLDER_PRIMITIVE_DERIVATION_FOUND"
    elif source_ok and counter:
        status = "COUNTEREVIDENCE_BLOCKS_PUBLIC_DERIVATION"
    elif source_ok and adoption_ready and supports:
        status = "ADOPTION_READY_PRIVATE_AXIOM_INPUT"
    elif source_ok and supports and not proves:
        status = "SUPPORTS_ADOPTION_NOT_DERIVATION"
    elif source_ok:
        status = "SOURCE_PRESENT_NO_A_MF_PROOF"
    else:
        status = "SOURCE_MISSING"

    valid_for_claim = source_ok and proves and not counter and not public_claim_false
    reasons = []
    if not source_ok:
        reasons.append("SOURCE_PATH_MISSING")
    if not proves:
        reasons.append("PROVES_A_MF_FALSE")
    if counter:
        reasons.append("COUNTEREVIDENCE_TRUE")
    if public_claim_false:
        reasons.append("PUBLIC_CLAIM_FALSE")

    return {
        "row_id": row.get("row_id", ""),
        "evidence_class": row.get("evidence_class", ""),
        "claim_piece": row.get("claim_piece", ""),
        "source_path": row.get("source_path", ""),
        "source_exists": source_ok,
        "supports_A_MF": supports,
        "proves_A_MF": proves,
        "counterevidence": counter,
        "adoption_ready": adoption_ready,
        "public_claim_false": public_claim_false,
        "current_status": status,
        "valid_for_claim": valid_for_claim,
        "claim_allowed": valid_for_claim,
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
    }


def evaluate_contract_row(row: Dict[str, str], input_path: Path) -> Dict[str, object]:
    source_ok = path_exists(row.get("source_path", ""))
    clause_signed_private = as_bool(row.get("clause_signed_private", "False"))
    consequences_written = as_bool(row.get("consequences_written", "False"))
    ir_selector_needed = as_bool(row.get("ir_selector_needed", "False"))
    public_claim_false = as_bool(row.get("public_claim_false", "False"))
    adoption_valid = source_ok and clause_signed_private and consequences_written and ir_selector_needed and public_claim_false

    if adoption_valid:
        status = "A_MF_ADOPTED_PRIVATE_BRANCH_IR_SELECTOR_STILL_REQUIRED"
    elif source_ok and clause_signed_private:
        status = "A_MF_PRIVATE_ADOPTION_CLAUSES_OPEN"
    elif source_ok:
        status = "A_MF_CONTRACT_SOURCE_PRESENT_UNSIGNED"
    else:
        status = "A_MF_CONTRACT_SOURCE_MISSING"

    return {
        "contract_id": row.get("contract_id", ""),
        "clause": row.get("clause", ""),
        "source_path": row.get("source_path", ""),
        "source_exists": source_ok,
        "clause_signed_private": clause_signed_private,
        "consequences_written": consequences_written,
        "ir_selector_needed": ir_selector_needed,
        "public_claim_false": public_claim_false,
        "current_status": status,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def evaluate_evidence_rows(input_path: Path) -> List[Dict[str, object]]:
    return [evaluate_evidence_row(row, input_path) for row in read_csv(input_path)]


def evaluate_contract_rows(input_path: Path) -> List[Dict[str, object]]:
    return [evaluate_contract_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate A_MF derivation/adoption evidence and private branch contract.")
    parser.add_argument("--mode", choices=["evidence", "contract"], required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = evaluate_evidence_rows(args.input) if args.mode == "evidence" else evaluate_contract_rows(args.input)
    write_csv(args.output, rows)


if __name__ == "__main__":
    main()
