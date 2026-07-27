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


def evaluate_em_closure_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required_fields = [
        "row_id",
        "branch",
        "same_hodge_zero",
        "scale_current_zero",
        "readout_postprocess",
        "no_effective_action_reentry",
        "no_loop_hidden_argument",
        "closed_collar_pointwise_no_flux",
        "orientation_normal_fixed",
        "poynting_once_only",
        "open_flux_routed_to_boundary",
        "source_path",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required_fields)
    source_ok = path_exists(row.get("source_path"))
    same_hodge = as_bool(row.get("same_hodge_zero"))
    scale_current = as_bool(row.get("scale_current_zero"))
    readout = as_bool(row.get("readout_postprocess"))
    no_effective = as_bool(row.get("no_effective_action_reentry"))
    no_loop_hidden = as_bool(row.get("no_loop_hidden_argument"))
    closed_flux = as_bool(row.get("closed_collar_pointwise_no_flux"))
    orientation = as_bool(row.get("orientation_normal_fixed"))
    poynting_once = as_bool(row.get("poynting_once_only"))
    open_routed = as_bool(row.get("open_flux_routed_to_boundary"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    readout_closed = readout and no_effective and no_loop_hidden
    radiation_closed = closed_flux and orientation and poynting_once
    boundary_safe = radiation_closed or open_routed
    total_fixed_zero = (
        source_ok
        and same_hodge
        and scale_current
        and readout_closed
        and radiation_closed
        and poynting_once
        and not missing
    )
    routed_nonzero_branch = source_ok and same_hodge and scale_current and readout_closed and open_routed and not closed_flux
    score_ready = total_fixed_zero and input_valid
    claim_ready = score_ready and requested_claim

    if claim_ready:
        status = "TOTAL_FIXED_BRANCH_EM_CLAIM_READY"
    elif score_ready:
        status = "TOTAL_FIXED_BRANCH_EM_ZERO_READY_NONCLAIM"
    elif total_fixed_zero:
        status = "TOTAL_FIXED_BRANCH_EM_ZERO_INPUT_INVALID_NONCLAIM"
    elif routed_nonzero_branch:
        status = "OPEN_RADIATIVE_BRANCH_ROUTED_BOUNDARY_VALUE_REQUIRED"
    elif source_ok and same_hodge and scale_current and not readout_closed:
        status = "EM_READOUT_RADIATIVE_REGENERATION_OPEN"
    elif source_ok and same_hodge and scale_current and not radiation_closed:
        status = "EM_RADIATIVE_COLLAR_FLUX_OPEN"
    elif source_ok and not scale_current:
        status = "EM_SCALE_CURRENT_OPEN"
    elif source_ok:
        status = "EM_CLOSURE_SOURCE_PRESENT_CLAUSES_OPEN"
    else:
        status = "EM_CLOSURE_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for field_name, ok in [
        ("source_exists", source_ok),
        ("same_hodge_zero", same_hodge),
        ("scale_current_zero", scale_current),
        ("readout_postprocess", readout),
        ("no_effective_action_reentry", no_effective),
        ("no_loop_hidden_argument", no_loop_hidden),
        ("closed_collar_pointwise_no_flux", closed_flux),
        ("orientation_normal_fixed", orientation),
        ("poynting_once_only", poynting_once),
        ("boundary_safe", boundary_safe),
        ("input_valid", input_valid),
    ]:
        if not ok:
            blockers.append(field_name)

    return {
        **{field_name: str(value) for field_name, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "source_exists": str(source_ok),
        "readout_closed": str(readout_closed),
        "radiation_closed": str(radiation_closed),
        "boundary_safe": str(boundary_safe),
        "total_fixed_zero": str(total_fixed_zero),
        "score_ready": str(score_ready),
        "blockers": ";".join(blockers),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_em_closure_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_em_closure_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate 4438 radiative/readout EM closure rows.")
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    write_csv(args.output, evaluate_em_closure_rows(args.input))


if __name__ == "__main__":
    main()
