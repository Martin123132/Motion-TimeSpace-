from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


TRUE_VALUES = {"1", "true", "yes", "y", "pass", "signed", "derived_zero"}
MISSING_PREFIXES = ("MISSING_", "PENDING_", "PLACEHOLDER_", "SCHEMA_", "NOT_", "UNKNOWN_")

SOURCE_CHARGE_CLAUSES = (
    "source_blind_kappa_eff",
    "same_worldtube",
    "Htau_MHref_defined",
    "PiH_glue_private",
    "Htau_integrable",
    "Href_fixed",
    "same_tau_frame_surface",
    "boundary_flux_routed",
    "MHref_positive",
    "anti_circularity",
    "action_measure_owner",
    "same_current_Req_zero",
    "fixed_EM_zero_integrated",
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


def evaluate_source_charge_row(row: Dict[str, str], input_path: Path) -> Dict[str, object]:
    source_ok = path_exists(row.get("source_path", ""))
    public_authority = as_bool(row.get("public_authority", "False"))
    input_valid = as_bool(row.get("input_valid_for_claim", "False"))
    failed_clauses = [clause for clause in SOURCE_CHARGE_CLAUSES if not as_bool(row.get(clause, ""))]
    theorem_core_closed = all(
        as_bool(row.get(clause, ""))
        for clause in (
            "source_blind_kappa_eff",
            "same_worldtube",
            "Htau_MHref_defined",
            "PiH_glue_private",
            "anti_circularity",
            "fixed_EM_zero_integrated",
        )
    )
    tail_contract_closed = not failed_clauses
    valid_for_claim = source_ok and tail_contract_closed and public_authority and input_valid
    reasons = []
    if not source_ok:
        reasons.append("SOURCE_PATH_MISSING")
    reasons.extend(f"OPEN_{clause.upper()}" for clause in failed_clauses)
    if not public_authority:
        reasons.append("PUBLIC_AUTHORITY_FALSE")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")

    if valid_for_claim:
        status = "SOURCE_CHARGE_CLAIM_READY"
    elif source_ok and theorem_core_closed and not tail_contract_closed:
        status = "SOURCE_CHARGE_REDUCED_TO_ACTION_MEASURE_CURRENT_CONTRACT"
    elif source_ok and tail_contract_closed:
        status = "SOURCE_CHARGE_PRIVATE_CLEAN_NONCLAIM"
    elif source_ok:
        status = "SOURCE_CHARGE_CLAUSES_OPEN"
    else:
        status = "SOURCE_CHARGE_BLOCKED_MISSING_SOURCE"

    return {
        "row_id": row.get("row_id", ""),
        "branch": row.get("branch", ""),
        "input_path": str(input_path),
        "source_path": row.get("source_path", ""),
        "source_exists": source_ok,
        "failed_clauses": "|".join(failed_clauses),
        "theorem_core_closed": theorem_core_closed and source_ok,
        "tail_contract_closed": tail_contract_closed and source_ok,
        "public_authority": public_authority,
        "input_valid_for_claim": input_valid,
        "valid_for_claim": valid_for_claim,
        "claim_allowed": valid_for_claim,
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_tail_bound_row(row: Dict[str, str], input_path: Path) -> Dict[str, object]:
    source_ok = path_exists(row.get("source_path", ""))
    projection_ok, projection = parse_float(row.get("projection_coeff", ""))
    epsilon_ok, epsilon_value = parse_float(row.get("epsilon_component_value", ""))
    bound_ok, arena_bound = parse_float(row.get("arena_bound", ""))
    numeric_ready = source_ok and projection_ok and epsilon_ok and bound_ok
    residual = projection * abs(epsilon_value) if numeric_ready else ""
    allowed = arena_bound / projection if numeric_ready and projection > 0 else ""
    within_bound = bool(numeric_ready and float(residual) <= arena_bound)
    input_valid = as_bool(row.get("input_valid_for_claim", "False"))
    valid_for_claim = numeric_ready and within_bound and input_valid

    reasons = []
    if not source_ok:
        reasons.append("SOURCE_PATH_MISSING")
    if not projection_ok:
        reasons.append("MISSING_PROJECTION_COEFF")
    if not epsilon_ok:
        reasons.append("MISSING_EPSILON_COMPONENT_VALUE")
    if not bound_ok:
        reasons.append("MISSING_ARENA_BOUND")
    if numeric_ready and not within_bound:
        reasons.append("TAIL_EXCEEDS_ARENA_BOUND")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")

    if valid_for_claim:
        status = "EPSILON_GSRC_TAIL_CLAIM_READY"
    elif numeric_ready and within_bound:
        status = "EPSILON_GSRC_TAIL_SCHEMA_PASS_NONCLAIM"
    elif numeric_ready:
        status = "EPSILON_GSRC_TAIL_FAILS_BOUND"
    elif source_ok:
        status = "EPSILON_GSRC_TAIL_VALUES_MISSING"
    else:
        status = "EPSILON_GSRC_TAIL_BLOCKED_MISSING_SOURCE"

    return {
        "tail_id": row.get("tail_id", ""),
        "arena": row.get("arena", ""),
        "residual_symbol": row.get("residual_symbol", ""),
        "projection_law": row.get("projection_law", ""),
        "input_path": str(input_path),
        "source_path": row.get("source_path", ""),
        "source_exists": source_ok,
        "projection_coeff": "" if not projection_ok else f"{projection:.12g}",
        "epsilon_component_value": row.get("epsilon_component_value", ""),
        "arena_bound": "" if not bound_ok else f"{arena_bound:.12g}",
        "units": row.get("units", ""),
        "numeric_ready": numeric_ready,
        "allowed_epsilon_component": "" if allowed == "" else f"{allowed:.12g}",
        "projected_residual": "" if residual == "" else f"{residual:.12g}",
        "within_bound": within_bound,
        "input_valid_for_claim": input_valid,
        "valid_for_claim": valid_for_claim,
        "claim_allowed": valid_for_claim,
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_source_charge_rows(input_path: Path) -> List[Dict[str, object]]:
    return [evaluate_source_charge_row(row, input_path) for row in read_csv(input_path)]


def evaluate_tail_bound_rows(input_path: Path) -> List[Dict[str, object]]:
    return [evaluate_tail_bound_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate 4440 source-charge closure and epsilon_Gsrc tail rows.")
    parser.add_argument("--mode", choices=["source", "tail"], required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.mode == "source":
        write_csv(args.output, evaluate_source_charge_rows(args.input))
    else:
        write_csv(args.output, evaluate_tail_bound_rows(args.input))


if __name__ == "__main__":
    main()
