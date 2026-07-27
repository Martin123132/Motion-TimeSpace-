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


def is_number(value: object) -> bool:
    try:
        float(str(value).strip())
        return True
    except ValueError:
        return False


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


def missing_required(row: Mapping[str, str], required: List[str]) -> str:
    return ";".join(name for name in required if str(row.get(name, "")).strip() == "")


def evaluate_nohom_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "row_id",
        "clause",
        "stress_total_domain",
        "parent_generator_exhausted",
        "species_label_absent",
        "hidden_marker_absent",
        "readout_no_reentry",
        "constant_sector_universal",
        "common_calibration_removed",
        "source_path",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    source_ok = path_exists(row.get("source_path"))
    stress_domain = as_bool(row.get("stress_total_domain"))
    generator = as_bool(row.get("parent_generator_exhausted"))
    species_absent = as_bool(row.get("species_label_absent"))
    hidden_absent = as_bool(row.get("hidden_marker_absent"))
    readout = as_bool(row.get("readout_no_reentry"))
    constants = as_bool(row.get("constant_sector_universal"))
    calibration = as_bool(row.get("common_calibration_removed"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    contract_ready = (
        stress_domain
        and generator
        and species_absent
        and hidden_absent
        and readout
        and constants
        and calibration
        and source_ok
        and not missing
    )
    score_ready = contract_ready and input_valid
    claim_ready = score_ready and requested_claim
    reduced = stress_domain and species_absent and calibration and source_ok and (not generator or not hidden_absent or not readout or not constants)
    domain_only = stress_domain and calibration and source_ok and not species_absent
    countermodel = source_ok and (not species_absent or not constants) and not generator
    partial = source_ok and (stress_domain or species_absent or calibration)

    if claim_ready:
        status = "CONSTRUCTOR_NOHOM_CLAIM_READY"
    elif score_ready:
        status = "CONSTRUCTOR_NOHOM_READY_NONCLAIM"
    elif contract_ready:
        status = "CONSTRUCTOR_NOHOM_CONTRACT_READY_NONCLAIM"
    elif reduced:
        status = "CONSTRUCTOR_NOHOM_REDUCES_TO_GENERATOR_EXHAUSTION_AND_REENTRY"
    elif countermodel:
        status = "CONSTRUCTOR_NOHOM_COUNTERMODEL_SURVIVES"
    elif domain_only:
        status = "CONSTRUCTOR_NOHOM_STRESS_TOTAL_DOMAIN_ONLY"
    elif partial:
        status = "CONSTRUCTOR_NOHOM_PARTIAL"
    elif source_ok:
        status = "CONSTRUCTOR_NOHOM_SOURCE_PRESENT_BUT_CLAUSES_OPEN"
    else:
        status = "CONSTRUCTOR_NOHOM_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("stress_total_domain", stress_domain),
        ("parent_generator_exhausted", generator),
        ("species_label_absent", species_absent),
        ("hidden_marker_absent", hidden_absent),
        ("readout_no_reentry", readout),
        ("constant_sector_universal", constants),
        ("common_calibration_removed", calibration),
        ("input_valid", input_valid),
    ]:
        if not ok:
            blockers.append(name)

    return {
        **{key: str(value) for key, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "source_exists": str(source_ok),
        "contract_ready": str(contract_ready),
        "score_ready": str(score_ready),
        "blockers": ";".join(blockers),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_shadow_split_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "row_id",
        "component",
        "definition",
        "pure_source_only",
        "action_scale",
        "hidden_return",
        "readout_projector",
        "killed_by_variational_owner",
        "reassigned_channel",
        "source_path",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    source_ok = path_exists(row.get("source_path"))
    pure_source = as_bool(row.get("pure_source_only"))
    action_scale = as_bool(row.get("action_scale"))
    hidden_return = as_bool(row.get("hidden_return"))
    readout_projector = as_bool(row.get("readout_projector"))
    killed = as_bool(row.get("killed_by_variational_owner"))
    reassigned = str(row.get("reassigned_channel", "")).strip()
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    contract_ready = source_ok and not missing and (killed or not is_missing_like(reassigned))
    score_ready = contract_ready and input_valid
    claim_ready = score_ready and requested_claim

    if claim_ready and killed:
        status = "SHADOW_SPLIT_ZERO_CLAIM_READY"
    elif killed and contract_ready:
        status = "SHADOW_PURE_SOURCE_ONLY_ZERO_CONTRACT_READY_NONCLAIM"
    elif action_scale and "action" in reassigned.lower():
        status = "SHADOW_REASSIGNED_ACTION_SCALE_OR_BLOCK"
    elif hidden_return and "hidden" in reassigned.lower():
        status = "SHADOW_REASSIGNED_HIDDEN_RETURN"
    elif readout_projector and "readout" in reassigned.lower():
        status = "SHADOW_REASSIGNED_READOUT_PROJECTOR"
    elif contract_ready:
        status = "SHADOW_SPLIT_FINITE_RESIDUAL_RETAINED"
    elif source_ok:
        status = "SHADOW_SPLIT_PARTIAL"
    else:
        status = "SHADOW_SPLIT_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    if not source_ok:
        blockers.append("source_exists")
    if not killed and is_missing_like(reassigned):
        blockers.append("reassigned_channel")
    if not input_valid:
        blockers.append("input_valid")

    return {
        **{key: str(value) for key, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "source_exists": str(source_ok),
        "contract_ready": str(contract_ready),
        "score_ready": str(score_ready),
        "blockers": ";".join(blockers),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_kmshadow_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "row_id",
        "product",
        "subcomponent",
        "value",
        "units",
        "parent_source",
        "source_leg",
        "projection",
        "bound_value",
        "source_path",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    source_ok = path_exists(row.get("source_path"))
    value = str(row.get("value", "")).strip()
    numeric_value = is_number(value)
    derived_zero = value.upper() == "DERIVED_ZERO"
    bound_only = value.upper().startswith("BOUND_ONLY")
    reassigned = value.upper().startswith("REASSIGNED_")
    units_ok = not is_missing_like(row.get("units"))
    parent_ok = not is_missing_like(row.get("parent_source"))
    source_leg_ok = not is_missing_like(row.get("source_leg"))
    projection_ok = not is_missing_like(row.get("projection"))
    bound_ok = is_number(row.get("bound_value"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    contract_ready = source_ok and units_ok and projection_ok and bound_ok and not missing
    numeric_ready = contract_ready and (numeric_value or derived_zero) and parent_ok and source_leg_ok
    score_ready = numeric_ready and input_valid
    claim_ready = score_ready and requested_claim

    if claim_ready:
        status = "KM_SHADOW_PRODUCT_CLAIM_READY"
    elif score_ready:
        status = "KM_SHADOW_PRODUCT_READY_NONCLAIM"
    elif numeric_ready:
        status = "KM_SHADOW_PRODUCT_INPUT_INVALID_NONCLAIM"
    elif bound_only and contract_ready:
        status = "KM_SHADOW_PRODUCT_BOUND_TARGET_ONLY"
    elif reassigned and contract_ready:
        status = "KM_SHADOW_PRODUCT_REASSIGNED_NOT_NUMERIC"
    elif contract_ready:
        status = "KM_SHADOW_PRODUCT_CONTRACT_ONLY"
    elif source_ok:
        status = "KM_SHADOW_PRODUCT_PARTIAL"
    else:
        status = "KM_SHADOW_PRODUCT_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("numeric_or_zero_value", numeric_value or derived_zero),
        ("units", units_ok),
        ("parent_source", parent_ok),
        ("source_leg", source_leg_ok),
        ("projection", projection_ok),
        ("bound_value_numeric", bound_ok),
        ("input_valid", input_valid),
    ]:
        if not ok:
            blockers.append(name)

    return {
        **{key: str(value) for key, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "source_exists": str(source_ok),
        "contract_ready": str(contract_ready),
        "numeric_ready": str(numeric_ready),
        "score_ready": str(score_ready),
        "blockers": ";".join(blockers),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_nohom_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_nohom_row(row, input_path) for row in read_csv(input_path)]


def evaluate_shadow_split_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_shadow_split_row(row, input_path) for row in read_csv(input_path)]


def evaluate_kmshadow_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_kmshadow_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate 4432 constructor/no-Hom and K_m_shadow rows.")
    parser.add_argument("--kind", choices=["nohom", "split", "kmshadow"], required=True)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    if args.kind == "nohom":
        rows = evaluate_nohom_rows(args.input)
    elif args.kind == "split":
        rows = evaluate_shadow_split_rows(args.input)
    else:
        rows = evaluate_kmshadow_rows(args.input)
    write_csv(args.output, rows)


if __name__ == "__main__":
    main()
