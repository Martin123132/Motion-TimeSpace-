from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List, Mapping


TRUE_VALUES = {"true", "1", "yes", "y", "pass", "signed"}


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
        writer.writerows(rows)


def missing_required(row: Mapping[str, str], required: List[str]) -> str:
    return ";".join(name for name in required if str(row.get(name, "")).strip() == "")


def source_exists(row: Mapping[str, str]) -> bool:
    source_path = str(row.get("source_path", "")).strip()
    return bool(source_path) and Path(source_path).exists()


def evaluate_density_owner_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "row_id",
        "branch",
        "parent_sorts_declared",
        "primitive_constructor_list",
        "ordinary_domain_exhausted",
        "hom_species_to_source_empty",
        "no_source_only_prefactor",
        "action_density_line_unique",
        "common_hbar_measure_owner",
        "species_blind_measure_jacobian",
        "connected_matter_graph",
        "representation_constants_exempt",
        "hidden_marker_no_reentry",
        "readout_eft_closure",
        "variation_before_readout",
        "source_path",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    source_ok = source_exists(row)
    parent_sorts = as_bool(row.get("parent_sorts_declared"))
    constructors = as_bool(row.get("primitive_constructor_list"))
    domain = as_bool(row.get("ordinary_domain_exhausted"))
    hom_empty = as_bool(row.get("hom_species_to_source_empty"))
    no_prefactor = as_bool(row.get("no_source_only_prefactor"))
    action_line = as_bool(row.get("action_density_line_unique"))
    hbar_measure = as_bool(row.get("common_hbar_measure_owner"))
    jacobian = as_bool(row.get("species_blind_measure_jacobian"))
    connected = as_bool(row.get("connected_matter_graph"))
    constants = as_bool(row.get("representation_constants_exempt"))
    no_reentry = as_bool(row.get("hidden_marker_no_reentry"))
    readout = as_bool(row.get("readout_eft_closure"))
    variation = as_bool(row.get("variation_before_readout"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    typed_domain_ready = parent_sorts and constructors and domain and constants
    no_slot_ready = typed_domain_ready and hom_empty and no_prefactor
    action_owner_ready = no_slot_ready and action_line and hbar_measure and jacobian and variation
    stability_ready = connected and no_reentry and readout
    density_owner_ready = action_owner_ready and stability_ready and source_ok and not missing
    claim_ready = density_owner_ready and input_valid and requested_claim

    if claim_ready:
        status = "ACTION_DENSITY_OWNER_PARENT_SIGNED"
    elif density_owner_ready:
        status = "ACTION_DENSITY_OWNER_CONTRACT_READY_NONCLAIM"
    elif typed_domain_ready and not no_slot_ready:
        status = "TYPED_DOMAIN_READY_HOM_NO_SLOT_OPEN"
    elif no_slot_ready and not action_owner_ready:
        status = "HOM_NO_SLOT_READY_ACTION_MEASURE_OPEN"
    elif action_owner_ready and not stability_ready:
        status = "ACTION_OWNER_READY_CONNECTIVITY_READOUT_OPEN"
    elif parent_sorts or action_line:
        status = "ACTION_DENSITY_OWNER_PARTIAL_PARENT_SYNTAX"
    elif source_ok:
        status = "ACTION_DENSITY_OWNER_BLOCKED"
    else:
        status = "ACTION_DENSITY_OWNER_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("parent_sorts_declared", parent_sorts),
        ("primitive_constructor_list", constructors),
        ("ordinary_domain_exhausted", domain),
        ("hom_species_to_source_empty", hom_empty),
        ("no_source_only_prefactor", no_prefactor),
        ("action_density_line_unique", action_line),
        ("common_hbar_measure_owner", hbar_measure),
        ("species_blind_measure_jacobian", jacobian),
        ("connected_matter_graph", connected),
        ("representation_constants_exempt", constants),
        ("hidden_marker_no_reentry", no_reentry),
        ("readout_eft_closure", readout),
        ("variation_before_readout", variation),
        ("input_valid", input_valid),
    ]:
        if not ok:
            blockers.append(name)

    return {
        **{key: str(value) for key, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "source_exists": str(source_ok),
        "typed_domain_ready": str(typed_domain_ready),
        "no_slot_ready": str(no_slot_ready),
        "action_owner_ready": str(action_owner_ready),
        "stability_ready": str(stability_ready),
        "density_owner_ready": str(density_owner_ready),
        "blockers": ";".join(blockers),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_density_owner_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_density_owner_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate action-density line owner rows.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    write_csv(args.output, evaluate_density_owner_rows(args.input))


if __name__ == "__main__":
    main()
