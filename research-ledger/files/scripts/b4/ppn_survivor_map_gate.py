from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, Iterable, List


TRUE_VALUES = {"1", "true", "yes", "y", "pass", "signed", "closed", "closed_private", "proved"}
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


def evaluate_survivor_row(row: Dict[str, str], input_path: Path) -> Dict[str, object]:
    source_ok = path_exists(row.get("source_path", ""))
    private_closed = as_bool(row.get("private_closed", "False"))
    conditional_theorem = as_bool(row.get("conditional_theorem", "False"))
    parent_signed = as_bool(row.get("parent_signed", "False"))
    empirical_ready = as_bool(row.get("empirical_ready", "False"))
    public_claim_false = as_bool(row.get("public_claim_false", "False"))
    primary_target = as_bool(row.get("primary_derivation_target", "False"))
    active_blocker = as_bool(row.get("active_blocker", "False"))
    reactivation_guard = as_bool(row.get("reactivation_guard", "False"))

    reasons = []
    if not source_ok:
        reasons.append("SOURCE_PATH_MISSING")
    if not parent_signed:
        reasons.append("PARENT_SIGNATURE_FALSE")
    if not empirical_ready:
        reasons.append("EMPIRICAL_READY_FALSE")
    if public_claim_false:
        reasons.append("PUBLIC_CLAIM_FALSE")
    if active_blocker:
        reasons.append("ACTIVE_BLOCKER")

    if primary_target and active_blocker:
        status = "PRIMARY_DERIVATION_TARGET"
    elif private_closed and reactivation_guard and not parent_signed:
        status = "CLOSED_PRIVATE_PARENT_ADOPTION_OPEN"
    elif private_closed and reactivation_guard:
        status = "CLOSED_PRIVATE_REACTIVATION_GUARD"
    elif conditional_theorem and not parent_signed:
        status = "CONDITIONAL_THEOREM_EFFECTIVE_GR_LABEL_ACTIVE"
    elif active_blocker:
        status = "SURVIVES_AS_ACTIVE_PUBLIC_BLOCKER"
    elif source_ok:
        status = "SOURCE_PRESENT_CLASSIFICATION_INCOMPLETE"
    else:
        status = "BLOCKED_MISSING_SOURCE"

    valid_for_claim = source_ok and private_closed and parent_signed and empirical_ready and not public_claim_false and not active_blocker

    return {
        "row_id": row.get("row_id", ""),
        "residual_family": row.get("residual_family", ""),
        "observable_targets": row.get("observable_targets", ""),
        "source_path": row.get("source_path", ""),
        "source_exists": source_ok,
        "private_closed": private_closed,
        "conditional_theorem": conditional_theorem,
        "parent_signed": parent_signed,
        "empirical_ready": empirical_ready,
        "reactivation_guard": reactivation_guard,
        "primary_derivation_target": primary_target,
        "active_blocker": active_blocker,
        "priority_rank": row.get("priority_rank", ""),
        "next_action": row.get("next_action", ""),
        "valid_for_claim": valid_for_claim,
        "claim_allowed": valid_for_claim,
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_target_row(row: Dict[str, str], input_path: Path) -> Dict[str, object]:
    source_ok = path_exists(row.get("source_path", ""))
    chosen = as_bool(row.get("chosen", "False"))
    moves_derivation = as_bool(row.get("moves_derivation", "False"))
    avoids_repeating_closed_work = as_bool(row.get("avoids_repeating_closed_work", "False"))
    has_next_artifact = bool(row.get("next_artifact", "").strip())
    rank = int(row.get("priority_rank", "999"))
    target_ready = source_ok and chosen and moves_derivation and avoids_repeating_closed_work and has_next_artifact and rank == 1

    if target_ready:
        status = "NEXT_TARGET_SELECTED"
    elif chosen:
        status = "CHOSEN_TARGET_HAS_OPEN_CLAUSES"
    elif source_ok:
        status = "NOT_SELECTED"
    else:
        status = "TARGET_SOURCE_MISSING"

    return {
        "target_id": row.get("target_id", ""),
        "target": row.get("target", ""),
        "priority_rank": rank,
        "chosen": chosen,
        "source_path": row.get("source_path", ""),
        "source_exists": source_ok,
        "moves_derivation": moves_derivation,
        "avoids_repeating_closed_work": avoids_repeating_closed_work,
        "next_artifact": row.get("next_artifact", ""),
        "valid_for_claim": False,
        "claim_allowed": False,
        "current_status": status,
    }


def evaluate_survivor_rows(input_path: Path) -> List[Dict[str, object]]:
    return [evaluate_survivor_row(row, input_path) for row in read_csv(input_path)]


def evaluate_target_rows(input_path: Path) -> List[Dict[str, object]]:
    return [evaluate_target_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Classify non-source PPN survivors and select the next derivation target.")
    parser.add_argument("--mode", choices=["survivor", "target"], required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = evaluate_survivor_rows(args.input) if args.mode == "survivor" else evaluate_target_rows(args.input)
    write_csv(args.output, rows)


if __name__ == "__main__":
    main()
