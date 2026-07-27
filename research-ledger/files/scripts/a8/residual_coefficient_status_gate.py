from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, Iterable, List


TRUE_VALUES = {"1", "true", "yes", "y", "pass", "signed", "adopted", "proved", "ready"}
MISSING_PREFIXES = ("MISSING_", "PENDING_", "PLACEHOLDER_", "UNKNOWN_", "NOT_")


def as_bool(value: object) -> bool:
    return str(value).strip().lower() in TRUE_VALUES


def as_int(value: object, default: int = 0) -> int:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return default


def is_missing_like(value: object) -> bool:
    text = str(value).strip()
    return not text or any(text.startswith(prefix) for prefix in MISSING_PREFIXES)


def source_paths_exist(value: object) -> bool:
    paths = [piece.strip() for piece in str(value).split(";") if piece.strip()]
    return bool(paths) and all(not is_missing_like(path) and Path(path).exists() for path in paths)


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


def evaluate_coefficient_row(row: Dict[str, str]) -> Dict[str, object]:
    sources_ok = source_paths_exist(row.get("source_paths", ""))
    parent_status = row.get("parent_route_status", "")
    scale_status = row.get("scale_status", "")
    bound_status = row.get("bound_status", "")
    current_class = row.get("current_class", "")
    selected_next = as_bool(row.get("selected_next", "False"))
    public_claim_false = as_bool(row.get("public_claim_false", "True"))

    parent_public_zero = parent_status == "PARENT_SIGNED_ZERO"
    scale_ready = scale_status == "PARENT_SCALE_NUMERIC_READY"
    bound_ready = bound_status == "SOURCE_BOUND_NUMERIC_READY"
    valid_for_claim = sources_ok and not public_claim_false and (parent_public_zero or scale_ready or bound_ready)

    if selected_next:
        status = "SELECTED_NEXT_DERIVATION_TARGET"
    elif parent_status == "PRIVATE_ZERO_ROUTED":
        status = "PRIVATE_ZERO_ROUTED_PARENT_ADOPTION_OPEN"
    elif parent_status == "PRIVATE_STRUCTURAL_COUPLING":
        status = "PRIVATE_STRUCTURAL_COUPLING_CALIBRATED_G_NOT_PREDICTED"
    elif current_class == "finite_survivor":
        status = "FINITE_SURVIVOR_PARENT_SCALE_OR_BOUND_REQUIRED"
    elif current_class == "empirical_fallback":
        status = "EMPIRICAL_FALLBACK_NOT_MAIN_DERIVATION_ROUTE"
    elif not sources_ok:
        status = "SOURCE_PATH_MISSING"
    else:
        status = "MAPPED_NONCLAIM"

    reasons = []
    if not sources_ok:
        reasons.append("SOURCE_PATH_MISSING")
    if public_claim_false:
        reasons.append("PUBLIC_CLAIM_FALSE")
    if not parent_public_zero:
        reasons.append("PARENT_SIGNED_ZERO_FALSE")
    if not scale_ready:
        reasons.append("PARENT_SCALE_NUMERIC_READY_FALSE")
    if not bound_ready:
        reasons.append("SOURCE_BOUND_NUMERIC_READY_FALSE")

    return {
        "coefficient_id": row.get("coefficient_id", ""),
        "coefficient": row.get("coefficient", ""),
        "family": row.get("family", ""),
        "local_gr_role": row.get("local_gr_role", ""),
        "observable_arenas": row.get("observable_arenas", ""),
        "source_paths": row.get("source_paths", ""),
        "source_paths_exist": sources_ok,
        "parent_route": row.get("parent_route", ""),
        "parent_route_status": parent_status,
        "scale_status": scale_status,
        "bound_status": bound_status,
        "current_class": current_class,
        "selected_next": selected_next,
        "current_status": status,
        "valid_for_claim": valid_for_claim,
        "claim_allowed": valid_for_claim,
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
    }


def evaluate_target_row(row: Dict[str, str]) -> Dict[str, object]:
    leverage = as_int(row.get("derivation_leverage", "0"))
    clean_theorem_route = as_int(row.get("clean_theorem_route", "0"))
    already_chased_penalty = as_int(row.get("already_chased_penalty", "0"))
    dependency_penalty = as_int(row.get("dependency_penalty", "0"))
    empirical_fallback_penalty = as_int(row.get("empirical_fallback_penalty", "0"))
    score = (2 * leverage) + clean_theorem_route - already_chased_penalty - dependency_penalty - empirical_fallback_penalty
    return {
        "target_id": row.get("target_id", ""),
        "target": row.get("target", ""),
        "why": row.get("why", ""),
        "derivation_leverage": leverage,
        "clean_theorem_route": clean_theorem_route,
        "already_chased_penalty": already_chased_penalty,
        "dependency_penalty": dependency_penalty,
        "empirical_fallback_penalty": empirical_fallback_penalty,
        "score": score,
        "selected": False,
        "next_artifact": row.get("next_artifact", ""),
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def evaluate_targets(input_path: Path) -> List[Dict[str, object]]:
    rows = [evaluate_target_row(row) for row in read_csv(input_path)]
    if not rows:
        return rows
    best_score = max(int(row["score"]) for row in rows)
    best_seen = False
    for row in rows:
        selected = int(row["score"]) == best_score and not best_seen
        row["selected"] = selected
        if selected:
            best_seen = True
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate residual coefficient status and next derivation target.")
    parser.add_argument("--mode", choices=["coefficients", "targets"], required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.mode == "coefficients":
        rows = [evaluate_coefficient_row(row) for row in read_csv(args.input)]
    else:
        rows = evaluate_targets(args.input)
    write_csv(args.output, rows)


if __name__ == "__main__":
    main()
