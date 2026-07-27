from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List, Mapping


TRUE_VALUES = {"true", "1", "yes", "y", "pass", "signed"}
MISSING_PREFIXES = ("MISSING_", "PENDING_", "PLACEHOLDER_", "SCHEMA_", "NOT_")


def as_bool(value: object) -> bool:
    return str(value).strip().lower() in TRUE_VALUES


def is_missing_like(value: object) -> bool:
    text = str(value).strip()
    return any(text.startswith(prefix) for prefix in MISSING_PREFIXES)


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


def evaluate_no_extension_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "row_id",
        "clause",
        "quotient_verticality_declared",
        "hidden_invariant_algebra_trivial",
        "no_extension_marker",
        "visible_coefficient_domain_excludes_hidden",
        "parent_action_domain_signed",
        "radiative_readout_closure",
        "source_label_forgetting",
        "source_path",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    source_ok = path_exists(row.get("source_path"))
    quotient_vertical = as_bool(row.get("quotient_verticality_declared"))
    hidden_trivial = as_bool(row.get("hidden_invariant_algebra_trivial"))
    no_marker = as_bool(row.get("no_extension_marker"))
    domain_excludes_hidden = as_bool(row.get("visible_coefficient_domain_excludes_hidden"))
    parent_domain = as_bool(row.get("parent_action_domain_signed"))
    readout_closed = as_bool(row.get("radiative_readout_closure"))
    source_forgets = as_bool(row.get("source_label_forgetting"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    scalar_route_closed = quotient_vertical and hidden_trivial
    typed_route_closed = quotient_vertical and no_marker and domain_excludes_hidden and parent_domain
    static_no_extension = (scalar_route_closed or typed_route_closed) and source_forgets and source_ok and not missing
    observable_no_extension = static_no_extension and readout_closed and input_valid
    claim_ready = observable_no_extension and requested_claim

    if claim_ready:
        status = "NO_EXTENSION_THEOREM_PARENT_SIGNED"
    elif observable_no_extension:
        status = "NO_EXTENSION_THEOREM_READY_NONCLAIM"
    elif static_no_extension and readout_closed:
        status = "NO_EXTENSION_CONTRACT_READY_NONCLAIM"
    elif scalar_route_closed and not readout_closed:
        status = "TREE_LEVEL_SCALAR_ROUTE_READY_READOUT_REENTRY_OPEN"
    elif typed_route_closed and not readout_closed:
        status = "TREE_LEVEL_TYPED_ROUTE_READY_READOUT_REENTRY_OPEN"
    elif quotient_vertical and not hidden_trivial and not no_marker:
        status = "SCALAR_INVARIANT_EXTENSION_COUNTERMODEL_LIVE"
    elif domain_excludes_hidden and not parent_domain:
        status = "TYPED_DOMAIN_CONDITIONAL_NOT_PARENT_SIGNED"
    elif source_ok:
        status = "NO_EXTENSION_PARTIAL"
    else:
        status = "NO_EXTENSION_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("quotient_verticality_declared", quotient_vertical),
        ("hidden_invariant_algebra_trivial_or_no_extension_marker", hidden_trivial or no_marker),
        ("visible_coefficient_domain_excludes_hidden_if_marker_route", True if hidden_trivial else domain_excludes_hidden),
        ("parent_action_domain_signed_if_typed_route", True if hidden_trivial else parent_domain),
        ("source_label_forgetting", source_forgets),
        ("radiative_readout_closure", readout_closed),
        ("input_valid", input_valid),
    ]:
        if not ok:
            blockers.append(name)

    return {
        **{key: str(value) for key, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "source_exists": str(source_ok),
        "scalar_route_closed": str(scalar_route_closed),
        "typed_route_closed": str(typed_route_closed),
        "static_no_extension": str(static_no_extension),
        "observable_no_extension": str(observable_no_extension),
        "blockers": ";".join(blockers),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_import_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "row_id",
        "coefficient",
        "value",
        "units",
        "parent_basis",
        "sign_convention",
        "source_path",
        "zero_certificate_source",
        "independent_of_bound",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    value = str(row.get("value", "")).strip()
    numeric = is_number(value)
    derived_zero = value == "DERIVED_ZERO"
    source_ok = path_exists(row.get("source_path"))
    zero_source_ok = path_exists(row.get("zero_certificate_source"))
    basis_ok = not is_missing_like(row.get("parent_basis"))
    sign_ok = not is_missing_like(row.get("sign_convention"))
    independent = as_bool(row.get("independent_of_bound"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    numeric_ready = numeric and source_ok and basis_ok and sign_ok and independent and not missing
    zero_ready = derived_zero and zero_source_ok and basis_ok and sign_ok and independent and not missing
    score_ready = (numeric_ready or zero_ready) and input_valid
    claim_ready = score_ready and requested_claim

    if claim_ready:
        status = "CPARENT_WEP_IMPORT_CLAIM_READY"
    elif score_ready:
        status = "CPARENT_WEP_IMPORT_SCORE_READY_NONCLAIM"
    elif numeric_ready:
        status = "CPARENT_WEP_NUMERIC_READY_INPUT_INVALID_NONCLAIM"
    elif zero_ready:
        status = "CPARENT_WEP_ZERO_READY_INPUT_INVALID_NONCLAIM"
    elif source_ok or zero_source_ok:
        status = "CPARENT_WEP_IMPORT_BLOCKED_MISSING_VALUE_OR_CERTIFICATE"
    else:
        status = "CPARENT_WEP_IMPORT_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists_for_numeric", True if not numeric else source_ok),
        ("zero_certificate_source_exists_for_zero", True if not derived_zero else zero_source_ok),
        ("numeric_or_derived_zero", numeric or derived_zero),
        ("parent_basis_declared", basis_ok),
        ("sign_convention_declared", sign_ok),
        ("independent_of_bound", independent),
        ("input_valid", input_valid),
    ]:
        if not ok:
            blockers.append(name)

    return {
        **{key: str(value) for key, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "numeric_value": str(numeric),
        "derived_zero": str(derived_zero),
        "source_exists": str(source_ok),
        "zero_certificate_source_exists": str(zero_source_ok),
        "numeric_ready": str(numeric_ready),
        "zero_ready": str(zero_ready),
        "score_ready": str(score_ready),
        "blockers": ";".join(blockers),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_no_extension_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_no_extension_row(row, input_path) for row in read_csv(input_path)]


def evaluate_import_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_import_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate hidden-invariant no-extension and C_parent WEP import rows.")
    parser.add_argument("--mode", choices=["no-extension", "import"], required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = evaluate_no_extension_rows(args.input) if args.mode == "no-extension" else evaluate_import_rows(args.input)
    write_csv(args.output, rows)


if __name__ == "__main__":
    main()
