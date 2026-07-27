from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, Iterable, List, Mapping


GUARD_REQUIRED_FIELDS = [
    "guard_id",
    "branch",
    "no_independent_connection",
    "gamma_equals_lc",
    "projective_mode_absent",
    "projective_mode_pure_trace",
    "symmetric_ricci_projective_blind",
    "projective_fixed_before_coupling",
    "all_sector_projective_invariant",
    "boundary_functional_metric_lc_only",
    "boundary_variation_fixed_induced_coframe",
    "boundary_improvement_fixed_before_readout",
    "no_boundary_torsion_current",
    "clock_light_orbit_metric_only",
    "no_readout_torsion_current",
    "same_tau_coframe_worldtube_support",
    "parent_branch_selector_signed",
    "affine_counterbranch_excluded",
    "source_path",
    "input_valid",
    "valid_for_claim",
    "notes",
]


P4_PROJECTIVE_REQUIRED_FIELDS = [
    "row_id",
    "p4_component",
    "arena",
    "residual_symbol",
    "source_coefficient",
    "coefficient_units",
    "uu_projection",
    "symmetric_ricci_projection",
    "antisymmetric_ricci_projection",
    "support_certificate",
    "observable_map",
    "comparator_bound",
    "no_cancellation_guard",
    "source_path",
    "input_valid",
    "valid_for_claim",
    "issues",
]


TRUE_VALUES = {"1", "true", "yes", "y", "pass", "passed", "closed"}
FALSE_VALUES = {"0", "false", "no", "n", "fail", "failed", "open", ""}
MISSING_MARKERS = {"", "missing", "missing_*", "none", "null", "na", "n/a", "tbd", "unknown"}


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Iterable[Mapping[str, object]]) -> None:
    materialized = [dict(row) for row in rows]
    if not materialized:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in materialized:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in materialized:
            writer.writerow(row)


def as_bool(value: object) -> bool:
    return str(value).strip().lower() in TRUE_VALUES


def is_missing(value: object) -> bool:
    return str(value).strip().lower() in MISSING_MARKERS or str(value).strip().upper().startswith("MISSING")


def as_float(value: object) -> float | None:
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return None


def source_exists(row: Mapping[str, str]) -> bool:
    source = str(row.get("source_path", "")).strip()
    return bool(source) and not source.upper().startswith("MISSING") and Path(source).exists()


def missing_fields(row: Mapping[str, str], required: Iterable[str]) -> str:
    missing = [field for field in required if field not in row or is_missing(row.get(field, ""))]
    return ";".join(missing)


def evaluate_guard_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    missing = missing_fields(row, GUARD_REQUIRED_FIELDS)
    source_ok = source_exists(row)
    no_independent_connection = as_bool(row.get("no_independent_connection"))
    gamma_equals_lc = as_bool(row.get("gamma_equals_lc"))
    projective_mode_absent = as_bool(row.get("projective_mode_absent"))
    projective_mode_pure_trace = as_bool(row.get("projective_mode_pure_trace"))
    symmetric_ricci_projective_blind = as_bool(row.get("symmetric_ricci_projective_blind"))
    projective_fixed_before_coupling = as_bool(row.get("projective_fixed_before_coupling"))
    all_sector_projective_invariant = as_bool(row.get("all_sector_projective_invariant"))
    boundary_functional_metric_lc_only = as_bool(row.get("boundary_functional_metric_lc_only"))
    boundary_variation_fixed_induced_coframe = as_bool(row.get("boundary_variation_fixed_induced_coframe"))
    boundary_improvement_fixed_before_readout = as_bool(row.get("boundary_improvement_fixed_before_readout"))
    no_boundary_torsion_current = as_bool(row.get("no_boundary_torsion_current"))
    clock_light_orbit_metric_only = as_bool(row.get("clock_light_orbit_metric_only"))
    no_readout_torsion_current = as_bool(row.get("no_readout_torsion_current"))
    same_tau_coframe_worldtube_support = as_bool(row.get("same_tau_coframe_worldtube_support"))
    parent_branch_selector_signed = as_bool(row.get("parent_branch_selector_signed"))
    affine_counterbranch_excluded = as_bool(row.get("affine_counterbranch_excluded"))
    input_valid = as_bool(row.get("input_valid"))

    projective_absence_closed = no_independent_connection and gamma_equals_lc and projective_mode_absent
    projective_pure_trace_ruu_closed = (
        projective_mode_pure_trace
        and symmetric_ricci_projective_blind
        and (projective_fixed_before_coupling or all_sector_projective_invariant)
    )
    projective_guard_closed = projective_absence_closed or projective_pure_trace_ruu_closed
    boundary_guard_closed = (
        boundary_functional_metric_lc_only
        and boundary_variation_fixed_induced_coframe
        and boundary_improvement_fixed_before_readout
        and no_boundary_torsion_current
    )
    readout_guard_closed = (
        clock_light_orbit_metric_only
        and no_readout_torsion_current
        and same_tau_coframe_worldtube_support
    )
    selector_closed = parent_branch_selector_signed and affine_counterbranch_excluded
    branch_guard_ready = projective_guard_closed and boundary_guard_closed and readout_guard_closed
    public_ready = branch_guard_ready and selector_closed and input_valid and source_ok and not missing

    if missing or not source_ok:
        status = "PROJECTIVE_BOUNDARY_READOUT_GUARD_BLOCKED_MISSING_INPUT"
    elif public_ready:
        status = "PROJECTIVE_BOUNDARY_READOUT_GUARD_PUBLIC_READY"
    elif branch_guard_ready and selector_closed and not input_valid:
        status = "PROJECTIVE_BOUNDARY_READOUT_GUARD_SCHEMA_READY_NONCLAIM"
    elif branch_guard_ready:
        status = "PROJECTIVE_BOUNDARY_READOUT_GUARD_BRANCH_READY_SELECTOR_OPEN"
    elif projective_guard_closed:
        status = "PROJECTIVE_GUARD_CLOSED_BOUNDARY_OR_READOUT_OPEN"
    else:
        status = "PROJECTIVE_BOUNDARY_READOUT_GUARD_BLOCKED"

    valid_for_claim = public_ready and as_bool(row.get("valid_for_claim"))
    return {
        **{key: str(value) for key, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "source_exists": str(source_ok),
        "projective_absence_closed": str(projective_absence_closed),
        "projective_pure_trace_ruu_closed": str(projective_pure_trace_ruu_closed),
        "projective_guard_closed": str(projective_guard_closed),
        "boundary_guard_closed": str(boundary_guard_closed),
        "readout_guard_closed": str(readout_guard_closed),
        "selector_closed": str(selector_closed),
        "branch_guard_ready": str(branch_guard_ready),
        "public_ready": str(public_ready),
        "current_status": status,
        "valid_for_claim": str(valid_for_claim),
    }


def evaluate_p4_projective_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    missing = missing_fields(row, P4_PROJECTIVE_REQUIRED_FIELDS)
    source_ok = source_exists(row)
    source_coefficient = as_float(row.get("source_coefficient"))
    uu_projection = as_float(row.get("uu_projection"))
    symmetric_ricci_projection = as_float(row.get("symmetric_ricci_projection"))
    antisymmetric_ricci_projection = as_float(row.get("antisymmetric_ricci_projection"))
    comparator_bound = as_float(row.get("comparator_bound"))
    support_ready = not is_missing(row.get("support_certificate")) and not is_missing(row.get("observable_map"))
    no_cancellation_guard = as_bool(row.get("no_cancellation_guard"))
    input_valid = as_bool(row.get("input_valid"))

    numeric_ready = all(
        value is not None
        for value in [
            source_coefficient,
            uu_projection,
            symmetric_ricci_projection,
            antisymmetric_ricci_projection,
            comparator_bound,
        ]
    )
    geometric_ruu_zero = (
        numeric_ready
        and source_coefficient == 0.0
        and uu_projection == 0.0
        and symmetric_ricci_projection == 0.0
    )
    score_ready = numeric_ready and support_ready and no_cancellation_guard and source_ok and not missing
    claim_ready = score_ready and input_valid and as_bool(row.get("valid_for_claim"))

    if claim_ready:
        status = "P4_PROJECTIVE_RUU_ROW_READY"
    elif geometric_ruu_zero and score_ready:
        status = "P4_PROJECTIVE_RUU_GEOMETRIC_ZERO_NONCLAIM"
    elif score_ready:
        status = "P4_PROJECTIVE_RUU_SCHEMA_READY_NONCLAIM"
    elif missing or not source_ok:
        status = "P4_PROJECTIVE_RUU_ROW_BLOCKED_MISSING_INPUT"
    else:
        status = "P4_PROJECTIVE_RUU_ROW_BLOCKED"

    return {
        **{key: str(value) for key, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "source_exists": str(source_ok),
        "numeric_ready": str(numeric_ready),
        "support_ready": str(support_ready),
        "geometric_ruu_zero": str(geometric_ruu_zero),
        "score_ready": str(score_ready),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_guard_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_guard_row(row, input_path) for row in read_csv(input_path)]


def evaluate_p4_projective_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_p4_projective_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate projective/boundary/readout guard rows.")
    parser.add_argument("--mode", choices=["guard", "p4"], required=True)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    if args.mode == "guard":
        rows = evaluate_guard_rows(args.input)
    else:
        rows = evaluate_p4_projective_rows(args.input)
    write_csv(args.output, rows)


if __name__ == "__main__":
    main()
