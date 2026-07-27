from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, Iterable, List, Mapping


SELECTOR_REQUIRED_FIELDS = [
    "selector_id",
    "branch",
    "no_affine_generator",
    "q_to_eobs_signed",
    "matter_no_gamma",
    "spin_no_gamma",
    "em_hilbert_no_affine",
    "poynting_flux_owned_or_bounded",
    "source_readout_srng_signed",
    "clock_light_orbit_downstream",
    "boundary_href_gm_locked",
    "projective_ruu_closed",
    "projective_source_readout_closed",
    "affine_counterbranch_excluded",
    "leakage_bound_ready",
    "source_path",
    "input_valid",
    "valid_for_claim",
    "notes",
]


KERNEL_REQUIRED_FIELDS = [
    "kernel_id",
    "residual_component",
    "arena",
    "observable",
    "kernel_formula",
    "coefficient",
    "coefficient_units",
    "projection_matrix",
    "support_certificate",
    "comparator_bound",
    "source_path",
    "no_cancellation_guard",
    "input_valid",
    "valid_for_claim",
    "issues",
]


TRUE_VALUES = {"1", "true", "yes", "y", "pass", "passed", "closed"}
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


def source_exists(row: Mapping[str, str]) -> bool:
    source = str(row.get("source_path", "")).strip()
    return bool(source) and not source.upper().startswith("MISSING") and Path(source).exists()


def missing_fields(row: Mapping[str, str], required: Iterable[str]) -> str:
    missing = [field for field in required if field not in row or is_missing(row.get(field, ""))]
    return ";".join(missing)


def as_float(value: object) -> float | None:
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return None


def evaluate_selector_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    missing = missing_fields(row, SELECTOR_REQUIRED_FIELDS)
    source_ok = source_exists(row)
    no_affine_generator = as_bool(row.get("no_affine_generator"))
    q_to_eobs_signed = as_bool(row.get("q_to_eobs_signed"))
    matter_no_gamma = as_bool(row.get("matter_no_gamma"))
    spin_no_gamma = as_bool(row.get("spin_no_gamma"))
    em_hilbert_no_affine = as_bool(row.get("em_hilbert_no_affine"))
    poynting_flux_owned_or_bounded = as_bool(row.get("poynting_flux_owned_or_bounded"))
    source_readout_srng_signed = as_bool(row.get("source_readout_srng_signed"))
    clock_light_orbit_downstream = as_bool(row.get("clock_light_orbit_downstream"))
    boundary_href_gm_locked = as_bool(row.get("boundary_href_gm_locked"))
    projective_ruu_closed = as_bool(row.get("projective_ruu_closed"))
    projective_source_readout_closed = as_bool(row.get("projective_source_readout_closed"))
    affine_counterbranch_excluded = as_bool(row.get("affine_counterbranch_excluded"))
    leakage_bound_ready = as_bool(row.get("leakage_bound_ready"))
    input_valid = as_bool(row.get("input_valid"))

    branch_core_ready = (
        no_affine_generator
        and matter_no_gamma
        and spin_no_gamma
        and em_hilbert_no_affine
        and projective_ruu_closed
    )
    selector_product_factors = [
        no_affine_generator,
        q_to_eobs_signed,
        matter_no_gamma,
        spin_no_gamma,
        em_hilbert_no_affine,
        poynting_flux_owned_or_bounded,
        source_readout_srng_signed,
        clock_light_orbit_downstream,
        boundary_href_gm_locked,
        projective_ruu_closed,
        projective_source_readout_closed,
        affine_counterbranch_excluded,
    ]
    selector_product = all(selector_product_factors)
    bounded_selector_ready = branch_core_ready and leakage_bound_ready and source_ok and not missing
    public_ready = selector_product and input_valid and source_ok and not missing

    if missing or not source_ok:
        status = "LC_SELECTOR_BLOCKED_MISSING_INPUT"
    elif public_ready:
        status = "LC_SELECTOR_PUBLIC_READY"
    elif selector_product and not input_valid:
        status = "LC_SELECTOR_CONTRACT_READY_NONCLAIM"
    elif branch_core_ready and not selector_product:
        status = "LC_SELECTOR_CORE_BRANCH_READY_SECTOR_PRODUCT_OPEN"
    elif bounded_selector_ready:
        status = "LC_SELECTOR_BOUNDED_FALLBACK_READY_NONCLAIM"
    else:
        status = "LC_SELECTOR_BLOCKED"

    valid_for_claim = public_ready and as_bool(row.get("valid_for_claim"))
    open_factors = [
        name
        for name, value in [
            ("no_affine_generator", no_affine_generator),
            ("q_to_eobs_signed", q_to_eobs_signed),
            ("matter_no_gamma", matter_no_gamma),
            ("spin_no_gamma", spin_no_gamma),
            ("em_hilbert_no_affine", em_hilbert_no_affine),
            ("poynting_flux_owned_or_bounded", poynting_flux_owned_or_bounded),
            ("source_readout_srng_signed", source_readout_srng_signed),
            ("clock_light_orbit_downstream", clock_light_orbit_downstream),
            ("boundary_href_gm_locked", boundary_href_gm_locked),
            ("projective_ruu_closed", projective_ruu_closed),
            ("projective_source_readout_closed", projective_source_readout_closed),
            ("affine_counterbranch_excluded", affine_counterbranch_excluded),
        ]
        if not value
    ]
    return {
        **{key: str(value) for key, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "source_exists": str(source_ok),
        "branch_core_ready": str(branch_core_ready),
        "selector_product": str(selector_product),
        "open_product_factors": ";".join(open_factors),
        "bounded_selector_ready": str(bounded_selector_ready),
        "public_ready": str(public_ready),
        "current_status": status,
        "valid_for_claim": str(valid_for_claim),
    }


def evaluate_kernel_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    missing = missing_fields(row, KERNEL_REQUIRED_FIELDS)
    source_ok = source_exists(row)
    coefficient = as_float(row.get("coefficient"))
    projection = as_float(row.get("projection_matrix"))
    comparator = as_float(row.get("comparator_bound"))
    no_cancellation_guard = as_bool(row.get("no_cancellation_guard"))
    input_valid = as_bool(row.get("input_valid"))
    formula_ready = not is_missing(row.get("kernel_formula")) and not is_missing(row.get("coefficient_units"))
    support_ready = not is_missing(row.get("support_certificate"))
    numeric_ready = coefficient is not None and projection is not None and comparator is not None
    score_ready = numeric_ready and formula_ready and support_ready and source_ok and no_cancellation_guard and not missing
    schema_staged = formula_ready and source_ok and not is_missing(row.get("issues"))
    claim_ready = score_ready and input_valid and as_bool(row.get("valid_for_claim"))

    if claim_ready:
        status = "PROJECTIVE_SOURCE_READOUT_KERNEL_READY"
    elif score_ready:
        status = "PROJECTIVE_SOURCE_READOUT_KERNEL_SCORE_READY_NONCLAIM"
    elif schema_staged:
        status = "PROJECTIVE_SOURCE_READOUT_KERNEL_SCHEMA_STAGED_NONCLAIM"
    elif missing or not source_ok:
        status = "PROJECTIVE_SOURCE_READOUT_KERNEL_BLOCKED_MISSING_INPUT"
    else:
        status = "PROJECTIVE_SOURCE_READOUT_KERNEL_BLOCKED"

    return {
        **{key: str(value) for key, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "source_exists": str(source_ok),
        "formula_ready": str(formula_ready),
        "support_ready": str(support_ready),
        "numeric_ready": str(numeric_ready),
        "score_ready": str(score_ready),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_selector_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_selector_row(row, input_path) for row in read_csv(input_path)]


def evaluate_kernel_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_kernel_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate LC selector product rows or projective kernel rows.")
    parser.add_argument("--mode", choices=["selector", "kernel"], required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = evaluate_selector_rows(args.input) if args.mode == "selector" else evaluate_kernel_rows(args.input)
    write_csv(args.output, rows)


if __name__ == "__main__":
    main()
