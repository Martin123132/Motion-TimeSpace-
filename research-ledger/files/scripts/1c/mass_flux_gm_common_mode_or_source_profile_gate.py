from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, Iterable, List, Mapping


CLOSURE_REQUIRED_FIELDS = [
    "closure_id",
    "branch",
    "same_projected_source_current",
    "stationary_time_generator",
    "ward_conservation_signed",
    "topological_current_equals_PiJ",
    "euler_constraint_origin_signed",
    "no_boundary_flux",
    "Href_MH_lock",
    "same_frame_source_orbit",
    "Gref_constant_universal",
    "NoSourceOnlySpeciesSlot",
    "no_measured_GM_backfill",
    "EH_Poisson_operator_ready",
    "source_profile_claim_grade",
    "parent_policy_signed",
    "source_path",
    "input_valid",
    "valid_for_claim",
    "notes",
]


BOUND_REQUIRED_FIELDS = [
    "bound_id",
    "residual",
    "arena",
    "normal_form",
    "dln_Meff_dt",
    "partial_r_ln_mu_obs",
    "Delta_flux",
    "Delta_cal",
    "epsilon_mu",
    "Gref_derivative",
    "source_profile_value",
    "material_response",
    "comparator_bound",
    "source_path",
    "no_cancellation_guard",
    "official_numeric_source",
    "parent_coefficient_source",
    "input_valid",
    "valid_for_claim",
    "issues",
]


TRUE_VALUES = {"1", "true", "yes", "y", "pass", "passed", "closed", "signed", "zero"}
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
        writer.writerows(materialized)


def as_bool(value: object) -> bool:
    return str(value).strip().lower() in TRUE_VALUES


def is_missing(value: object) -> bool:
    stripped = str(value).strip()
    return stripped.lower() in MISSING_MARKERS or stripped.upper().startswith("MISSING")


def is_schema(value: object) -> bool:
    return str(value).strip().upper().startswith("SCHEMA_")


def as_float(value: object) -> float | None:
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return None


def numeric_ready(value: object) -> bool:
    numeric = as_float(value)
    return numeric is not None


def source_exists(row: Mapping[str, str]) -> bool:
    source = str(row.get("source_path", "")).strip()
    return bool(source) and not source.upper().startswith("MISSING") and Path(source).exists()


def missing_fields(row: Mapping[str, str], required: Iterable[str]) -> str:
    return ";".join(field for field in required if field not in row or is_missing(row.get(field, "")))


def evaluate_closure_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    missing = missing_fields(row, CLOSURE_REQUIRED_FIELDS)
    source_ok = source_exists(row)
    same_current = as_bool(row.get("same_projected_source_current"))
    stationary_time = as_bool(row.get("stationary_time_generator"))
    ward_signed = as_bool(row.get("ward_conservation_signed"))
    topo_equals = as_bool(row.get("topological_current_equals_PiJ"))
    euler_origin = as_bool(row.get("euler_constraint_origin_signed"))
    no_boundary_flux = as_bool(row.get("no_boundary_flux"))
    href_lock = as_bool(row.get("Href_MH_lock"))
    same_frame = as_bool(row.get("same_frame_source_orbit"))
    gref_constant = as_bool(row.get("Gref_constant_universal"))
    no_source_slot = as_bool(row.get("NoSourceOnlySpeciesSlot"))
    no_backfill = as_bool(row.get("no_measured_GM_backfill"))
    eh_poisson = as_bool(row.get("EH_Poisson_operator_ready"))
    profile_claim_grade = as_bool(row.get("source_profile_claim_grade"))
    parent_policy = as_bool(row.get("parent_policy_signed"))
    input_valid = as_bool(row.get("input_valid"))

    ward_route_ready = same_current and stationary_time and ward_signed and no_boundary_flux
    topological_route_ready = same_current and topo_equals and no_boundary_flux
    euler_route_ready = same_current and euler_origin and no_boundary_flux
    flux_closure_ready = ward_route_ready or topological_route_ready or euler_route_ready
    common_mode_ready = gref_constant and no_source_slot and no_backfill
    poisson_chain_ready = eh_poisson and same_frame
    source_lock_ready = href_lock and same_current
    profile_bound_ready = profile_claim_grade
    newton_transfer_ready = (
        flux_closure_ready
        and common_mode_ready
        and poisson_chain_ready
        and source_lock_ready
        and parent_policy
        and input_valid
        and source_ok
        and not missing
    )
    contract_ready_nonclaim = (
        flux_closure_ready
        and common_mode_ready
        and poisson_chain_ready
        and source_lock_ready
        and parent_policy
        and source_ok
        and not missing
        and not input_valid
    )

    if missing or not source_ok:
        status = "MASS_FLUX_GM_BLOCKED_MISSING_INPUT"
    elif newton_transfer_ready:
        status = "MASS_FLUX_GM_PUBLIC_NEWTON_READY"
    elif contract_ready_nonclaim:
        status = "MASS_FLUX_GM_CONTRACT_READY_NONCLAIM"
    elif poisson_chain_ready and source_lock_ready and common_mode_ready and not flux_closure_ready:
        status = "POISSON_COMMON_MODE_READY_FLUX_CLOSURE_OPEN"
    elif poisson_chain_ready and source_lock_ready and flux_closure_ready and not common_mode_ready:
        status = "POISSON_FLUX_READY_COMMON_MODE_OPEN"
    elif poisson_chain_ready and no_backfill:
        status = "POISSON_GAUSS_CHAIN_READY_SOURCE_LOCKS_OPEN"
    elif profile_bound_ready:
        status = "SOURCE_PROFILE_BOUND_ROUTE_READY_NONCLAIM"
    else:
        status = "MASS_FLUX_GM_BLOCKED"

    clauses = [
        ("same_projected_source_current", same_current),
        ("stationary_time_generator", stationary_time),
        ("ward_conservation_signed", ward_signed),
        ("topological_current_equals_PiJ", topo_equals),
        ("euler_constraint_origin_signed", euler_origin),
        ("no_boundary_flux", no_boundary_flux),
        ("Href_MH_lock", href_lock),
        ("same_frame_source_orbit", same_frame),
        ("Gref_constant_universal", gref_constant),
        ("NoSourceOnlySpeciesSlot", no_source_slot),
        ("no_measured_GM_backfill", no_backfill),
        ("EH_Poisson_operator_ready", eh_poisson),
        ("source_profile_claim_grade", profile_claim_grade),
        ("parent_policy_signed", parent_policy),
        ("input_valid", input_valid),
    ]

    return {
        **{key: str(value) for key, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "source_exists": str(source_ok),
        "ward_route_ready": str(ward_route_ready),
        "topological_route_ready": str(topological_route_ready),
        "euler_route_ready": str(euler_route_ready),
        "flux_closure_ready": str(flux_closure_ready),
        "common_mode_ready": str(common_mode_ready),
        "poisson_chain_ready": str(poisson_chain_ready),
        "source_lock_ready": str(source_lock_ready),
        "newton_transfer_ready": str(newton_transfer_ready),
        "open_clauses": ";".join(name for name, ok in clauses if not ok),
        "current_status": status,
        "valid_for_claim": str(newton_transfer_ready and as_bool(row.get("valid_for_claim"))),
    }


def evaluate_bound_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    missing = missing_fields(row, BOUND_REQUIRED_FIELDS)
    source_ok = source_exists(row)
    normal_form_ready = not is_missing(row.get("normal_form"))
    dln_ready = numeric_ready(row.get("dln_Meff_dt")) or is_schema(row.get("dln_Meff_dt"))
    radial_ready = numeric_ready(row.get("partial_r_ln_mu_obs")) or is_schema(row.get("partial_r_ln_mu_obs"))
    flux_ready = numeric_ready(row.get("Delta_flux")) or is_schema(row.get("Delta_flux"))
    cal_ready = numeric_ready(row.get("Delta_cal")) or is_schema(row.get("Delta_cal"))
    epsilon_ready = numeric_ready(row.get("epsilon_mu")) or is_schema(row.get("epsilon_mu"))
    gref_ready = numeric_ready(row.get("Gref_derivative")) or is_schema(row.get("Gref_derivative"))
    profile_ready = numeric_ready(row.get("source_profile_value")) or is_schema(row.get("source_profile_value"))
    material_ready = numeric_ready(row.get("material_response")) or is_schema(row.get("material_response"))
    comparator_ready = numeric_ready(row.get("comparator_bound")) or is_schema(row.get("comparator_bound"))
    no_cancellation = as_bool(row.get("no_cancellation_guard"))
    official_numeric = as_bool(row.get("official_numeric_source"))
    parent_coeff = as_bool(row.get("parent_coefficient_source"))
    input_valid = as_bool(row.get("input_valid"))

    schema_ready = (
        source_ok
        and normal_form_ready
        and dln_ready
        and radial_ready
        and flux_ready
        and cal_ready
        and epsilon_ready
        and gref_ready
        and profile_ready
        and material_ready
        and comparator_ready
        and no_cancellation
        and not missing
    )
    values_numeric = all(
        numeric_ready(row.get(field))
        for field in [
            "dln_Meff_dt",
            "partial_r_ln_mu_obs",
            "Delta_flux",
            "Delta_cal",
            "epsilon_mu",
            "Gref_derivative",
            "source_profile_value",
            "material_response",
            "comparator_bound",
        ]
    )
    score_ready = schema_ready and values_numeric and official_numeric and parent_coeff and input_valid
    claim_ready = score_ready and as_bool(row.get("valid_for_claim"))

    if claim_ready:
        status = "SOURCE_GM_BOUND_VALUES_READY"
    elif score_ready:
        status = "SOURCE_GM_BOUND_SCORE_READY_NONCLAIM"
    elif schema_ready:
        status = "SOURCE_GM_BOUND_SCHEMA_READY_VALUES_MISSING_NONCLAIM"
    elif source_ok:
        status = "SOURCE_GM_BOUND_BLOCKED_MISSING_INPUT"
    else:
        status = "SOURCE_GM_BOUND_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("normal_form", normal_form_ready),
        ("dln_Meff_dt", dln_ready),
        ("partial_r_ln_mu_obs", radial_ready),
        ("Delta_flux", flux_ready),
        ("Delta_cal", cal_ready),
        ("epsilon_mu", epsilon_ready),
        ("Gref_derivative", gref_ready),
        ("source_profile_value", profile_ready),
        ("material_response", material_ready),
        ("comparator_bound", comparator_ready),
        ("no_cancellation_guard", no_cancellation),
        ("official_numeric_source", official_numeric),
        ("parent_coefficient_source", parent_coeff),
        ("input_valid", input_valid),
    ]:
        if not ok:
            blockers.append(name)

    return {
        **{key: str(value) for key, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "source_exists": str(source_ok),
        "schema_ready": str(schema_ready),
        "values_numeric": str(values_numeric),
        "score_ready": str(score_ready),
        "blockers": ";".join(blockers),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_closure_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_closure_row(row, input_path) for row in read_csv(input_path)]


def evaluate_bound_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_bound_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate mass-flux/GM closure rows or source-profile bound rows.")
    parser.add_argument("--mode", choices=["closure", "bound"], required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = evaluate_closure_rows(args.input) if args.mode == "closure" else evaluate_bound_rows(args.input)
    write_csv(args.output, rows)


if __name__ == "__main__":
    main()
