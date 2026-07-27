from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List, Mapping


TRUE_VALUES = {"true", "1", "yes", "y", "pass", "signed", "derived_zero"}
MISSING_PREFIXES = ("MISSING_", "PENDING_", "PLACEHOLDER_", "SCHEMA_", "NOT_", "UNKNOWN_")


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


def write_csv(path: Path, rows: List[Mapping[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def missing_required(row: Mapping[str, str], required_fields: List[str]) -> str:
    return ";".join(field_name for field_name in required_fields if str(row.get(field_name, "")).strip() == "")


def evaluate_same_owner_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required_fields = [
        "row_id",
        "branch",
        "action_edge_signed",
        "fixed_theta_obs",
        "fixed_lambda_A",
        "fixed_g_J",
        "no_independent_F2_slot",
        "same_current_owner",
        "alpha_readout_qbasic",
        "readout_after_variation",
        "no_hidden_coefficient_slot",
        "no_dynamic_coefficient_branch",
        "source_path",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required_fields)
    source_ok = path_exists(row.get("source_path"))
    edge = as_bool(row.get("action_edge_signed"))
    theta = as_bool(row.get("fixed_theta_obs"))
    lambda_fixed = as_bool(row.get("fixed_lambda_A"))
    current_fixed = as_bool(row.get("fixed_g_J"))
    no_f2 = as_bool(row.get("no_independent_F2_slot"))
    same_current = as_bool(row.get("same_current_owner"))
    alpha_qbasic = as_bool(row.get("alpha_readout_qbasic"))
    readout = as_bool(row.get("readout_after_variation"))
    no_hidden = as_bool(row.get("no_hidden_coefficient_slot"))
    no_dynamic = as_bool(row.get("no_dynamic_coefficient_branch"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    alpha_drift_zero = lambda_fixed and current_fixed and alpha_qbasic and readout
    unique_f2_zero = no_f2 and no_hidden and no_dynamic
    current_zero = same_current and current_fixed and theta
    same_owner_ready = (
        source_ok
        and edge
        and theta
        and alpha_drift_zero
        and unique_f2_zero
        and current_zero
        and not missing
    )
    score_ready = same_owner_ready and input_valid
    claim_ready = score_ready and requested_claim

    if claim_ready:
        status = "SAME_OWNER_COUPLING_CLAIM_READY"
    elif score_ready:
        status = "SAME_OWNER_COUPLING_BRANCH_ZERO_READY_NONCLAIM"
    elif same_owner_ready:
        status = "SAME_OWNER_COUPLING_BRANCH_ZERO_INPUT_INVALID_NONCLAIM"
    elif source_ok and alpha_drift_zero and not unique_f2_zero:
        status = "ALPHA_CURRENT_ZERO_UNIQUE_F2_OPEN"
    elif source_ok and edge and not alpha_drift_zero:
        status = "EM_EDGE_SIGNED_ALPHA_CURRENT_DRIFT_OPEN"
    elif source_ok and not edge:
        status = "GLOBAL_OR_DYNAMIC_BRANCH_NOT_EDGE_SIGNED"
    elif source_ok:
        status = "SAME_OWNER_SOURCE_PRESENT_CLAUSES_OPEN"
    else:
        status = "SAME_OWNER_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for field_name, ok in [
        ("source_exists", source_ok),
        ("action_edge_signed", edge),
        ("fixed_theta_obs", theta),
        ("fixed_lambda_A", lambda_fixed),
        ("fixed_g_J", current_fixed),
        ("no_independent_F2_slot", no_f2),
        ("same_current_owner", same_current),
        ("alpha_readout_qbasic", alpha_qbasic),
        ("readout_after_variation", readout),
        ("no_hidden_coefficient_slot", no_hidden),
        ("no_dynamic_coefficient_branch", no_dynamic),
        ("input_valid", input_valid),
    ]:
        if not ok:
            blockers.append(field_name)

    return {
        **{field_name: str(value) for field_name, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "source_exists": str(source_ok),
        "alpha_drift_zero": str(alpha_drift_zero),
        "unique_F2_zero": str(unique_f2_zero),
        "current_zero": str(current_zero),
        "same_owner_ready": str(same_owner_ready),
        "score_ready": str(score_ready),
        "blockers": ";".join(blockers),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_same_owner_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_same_owner_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate 4437 EM same-owner coupling rows.")
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    write_csv(args.output, evaluate_same_owner_rows(args.input))


if __name__ == "__main__":
    main()
