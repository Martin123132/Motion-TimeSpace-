from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List, Mapping


TRUE_VALUES = {"true", "1", "yes", "y", "pass", "signed"}
SCHEMA_PREFIX = "SCHEMA_"


def as_bool(value: object) -> bool:
    return str(value).strip().lower() in TRUE_VALUES


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
        for row in rows:
            writer.writerow(row)


def source_exists(row: Mapping[str, str]) -> bool:
    source_path = str(row.get("source_path", "")).strip()
    return bool(source_path) and Path(source_path).exists()


def missing_required(row: Mapping[str, str], required: List[str]) -> str:
    return ";".join(name for name in required if str(row.get(name, "")).strip() == "")


def evaluate_source_slot_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "row_id",
        "branch",
        "single_parent_matter_functional",
        "object_language_typed",
        "universal_action_scale_owner",
        "variation_before_readout",
        "hilbert_current_owner",
        "no_source_only_scalar_target",
        "species_blind_measure_coframe",
        "measured_parameters_only",
        "common_mode_calibration_guard",
        "no_hidden_hom",
        "no_post_readout_selector",
        "source_path",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    source_ok = source_exists(row)
    single_functional = as_bool(row.get("single_parent_matter_functional"))
    typed = as_bool(row.get("object_language_typed"))
    action_owner = as_bool(row.get("universal_action_scale_owner"))
    variation_first = as_bool(row.get("variation_before_readout"))
    hilbert_owner = as_bool(row.get("hilbert_current_owner"))
    no_source_scalar = as_bool(row.get("no_source_only_scalar_target"))
    measure_blind = as_bool(row.get("species_blind_measure_coframe"))
    measured_only = as_bool(row.get("measured_parameters_only"))
    common_guard = as_bool(row.get("common_mode_calibration_guard"))
    no_hidden_hom = as_bool(row.get("no_hidden_hom"))
    no_selector = as_bool(row.get("no_post_readout_selector"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    object_contract_ready = all(
        [
            single_functional,
            typed,
            variation_first,
            measured_only,
            no_hidden_hom,
            no_selector,
        ]
    )
    action_scale_ready = action_owner and measure_blind
    source_owner_ready = hilbert_owner and no_source_scalar
    no_source_only_slot_ready = (
        object_contract_ready
        and action_scale_ready
        and source_owner_ready
        and common_guard
        and source_ok
        and not missing
    )
    delta_w_zero_ready = no_source_only_slot_ready
    claim_ready = no_source_only_slot_ready and input_valid and requested_claim

    if claim_ready:
        status = "NO_SOURCE_ONLY_SPECIES_SLOT_PARENT_SIGNED"
    elif no_source_only_slot_ready:
        status = "NO_SOURCE_ONLY_SPECIES_SLOT_CONTRACT_READY_NONCLAIM"
    elif object_contract_ready and not action_scale_ready:
        status = "SOURCE_SLOT_OBJECT_LANGUAGE_READY_ACTION_OWNER_OPEN"
    elif action_scale_ready and not object_contract_ready:
        status = "SOURCE_SLOT_ACTION_OWNER_READY_OBJECT_LANGUAGE_OPEN"
    elif source_ok:
        status = "SOURCE_SLOT_THEOREM_BLOCKED"
    else:
        status = "SOURCE_SLOT_THEOREM_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("single_parent_matter_functional", single_functional),
        ("object_language_typed", typed),
        ("universal_action_scale_owner", action_owner),
        ("variation_before_readout", variation_first),
        ("hilbert_current_owner", hilbert_owner),
        ("no_source_only_scalar_target", no_source_scalar),
        ("species_blind_measure_coframe", measure_blind),
        ("measured_parameters_only", measured_only),
        ("common_mode_calibration_guard", common_guard),
        ("no_hidden_hom", no_hidden_hom),
        ("no_post_readout_selector", no_selector),
        ("input_valid", input_valid),
    ]:
        if not ok:
            blockers.append(name)

    return {
        **{key: str(value) for key, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "source_exists": str(source_ok),
        "object_contract_ready": str(object_contract_ready),
        "action_scale_ready": str(action_scale_ready),
        "source_owner_ready": str(source_owner_ready),
        "no_source_only_slot_ready": str(no_source_only_slot_ready),
        "delta_w_zero_ready": str(delta_w_zero_ready),
        "blockers": ";".join(blockers),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_topological_current_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "row_id",
        "branch",
        "parent_owned_current",
        "same_hilbert_functional",
        "stationary_tau_generator",
        "PiM_chain_map",
        "on_shell_noether_constraint",
        "topological_current_closed",
        "distributional_R_eq_zero",
        "boundary_improvement_zero_flux",
        "fixed_worldtube_support",
        "common_Mref_lock",
        "no_measured_GM_backfill",
        "source_path",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    source_ok = source_exists(row)
    parent_owned = as_bool(row.get("parent_owned_current"))
    same_hilbert = as_bool(row.get("same_hilbert_functional"))
    stationary_tau = as_bool(row.get("stationary_tau_generator"))
    chain_map = as_bool(row.get("PiM_chain_map"))
    noether = as_bool(row.get("on_shell_noether_constraint"))
    closed = as_bool(row.get("topological_current_closed"))
    req_zero = as_bool(row.get("distributional_R_eq_zero"))
    boundary_zero = as_bool(row.get("boundary_improvement_zero_flux"))
    fixed_worldtube = as_bool(row.get("fixed_worldtube_support"))
    mref_lock = as_bool(row.get("common_Mref_lock"))
    anti_backfill = as_bool(row.get("no_measured_GM_backfill"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    closed_current_ready = all([parent_owned, stationary_tau, noether, closed, source_ok, not missing])
    equality_ready = all([same_hilbert, chain_map, req_zero, boundary_zero, fixed_worldtube, mref_lock])
    topological_closure_ready = closed_current_ready and equality_ready and anti_backfill
    claim_ready = topological_closure_ready and input_valid and requested_claim

    if claim_ready:
        status = "TOPOLOGICAL_MASS_CURRENT_ORIGIN_PARENT_SIGNED"
    elif topological_closure_ready:
        status = "TOPOLOGICAL_MASS_CURRENT_CONTRACT_READY_NONCLAIM"
    elif closed_current_ready and not equality_ready:
        status = "CLOSED_TOPOLOGICAL_CURRENT_READY_EQUALITY_OPEN"
    elif equality_ready and not closed_current_ready:
        status = "HILBERT_EQUALITY_READY_CLOSURE_OPEN"
    elif source_ok:
        status = "TOPOLOGICAL_MASS_CURRENT_BLOCKED"
    else:
        status = "TOPOLOGICAL_MASS_CURRENT_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("parent_owned_current", parent_owned),
        ("same_hilbert_functional", same_hilbert),
        ("stationary_tau_generator", stationary_tau),
        ("PiM_chain_map", chain_map),
        ("on_shell_noether_constraint", noether),
        ("topological_current_closed", closed),
        ("distributional_R_eq_zero", req_zero),
        ("boundary_improvement_zero_flux", boundary_zero),
        ("fixed_worldtube_support", fixed_worldtube),
        ("common_Mref_lock", mref_lock),
        ("no_measured_GM_backfill", anti_backfill),
        ("input_valid", input_valid),
    ]:
        if not ok:
            blockers.append(name)

    return {
        **{key: str(value) for key, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "source_exists": str(source_ok),
        "closed_current_ready": str(closed_current_ready),
        "equality_ready": str(equality_ready),
        "topological_closure_ready": str(topological_closure_ready),
        "blockers": ";".join(blockers),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_source_slot_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_source_slot_row(row, input_path) for row in read_csv(input_path)]


def evaluate_topological_current_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_topological_current_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate source-slot or topological-current closure rows.")
    parser.add_argument("--mode", choices=["source-slot", "topological-current"], required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = (
        evaluate_source_slot_rows(args.input)
        if args.mode == "source-slot"
        else evaluate_topological_current_rows(args.input)
    )
    write_csv(args.output, rows)


if __name__ == "__main__":
    main()
