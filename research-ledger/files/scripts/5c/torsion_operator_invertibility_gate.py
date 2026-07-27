from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, Iterable, List


TRUE_VALUES = {"1", "true", "yes", "y", "pass", "ready", "proved", "signed"}


def as_bool(value: object) -> bool:
    return str(value).strip().lower() in TRUE_VALUES


def path_exists(value: object) -> bool:
    text = str(value).strip()
    return bool(text) and Path(text).exists()


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


def evaluate_irrep_row(row: Dict[str, str]) -> Dict[str, object]:
    source_ok = path_exists(row.get("source_path", ""))
    diagonal = as_bool(row.get("diagonal_by_lorentz_parity", "False"))
    eigenvalue_symbolic = as_bool(row.get("eigenvalue_symbolic_written", "False"))
    nonzero_contract = as_bool(row.get("nonzero_contract_written", "False"))
    positive_parent_signed = as_bool(row.get("positive_parent_signed", "False"))
    numeric_margin = as_bool(row.get("numeric_margin_available", "False"))
    public_claim_false = as_bool(row.get("public_claim_false", "True"))

    if source_ok and diagonal and eigenvalue_symbolic and nonzero_contract and positive_parent_signed and numeric_margin:
        status = "IRREP_NUMERIC_INVERTIBILITY_READY"
    elif source_ok and diagonal and eigenvalue_symbolic and nonzero_contract:
        status = "IRREP_SYMBOLIC_INVERTIBILITY_CONTRACT_READY_PARENT_MARGIN_MISSING"
    elif source_ok and diagonal:
        status = "IRREP_DIAGONALIZATION_READY_EIGENVALUE_CONTRACT_OPEN"
    elif source_ok:
        status = "SOURCE_PRESENT_IRREP_GATE_OPEN"
    else:
        status = "SOURCE_MISSING"

    valid_for_claim = source_ok and diagonal and eigenvalue_symbolic and nonzero_contract and positive_parent_signed and numeric_margin and not public_claim_false
    reasons = []
    if not source_ok:
        reasons.append("SOURCE_PATH_MISSING")
    if not diagonal:
        reasons.append("DIAGONAL_BY_LORENTZ_PARITY_FALSE")
    if not eigenvalue_symbolic:
        reasons.append("EIGENVALUE_SYMBOLIC_WRITTEN_FALSE")
    if not nonzero_contract:
        reasons.append("NONZERO_CONTRACT_WRITTEN_FALSE")
    if not positive_parent_signed:
        reasons.append("POSITIVE_PARENT_SIGNED_FALSE")
    if not numeric_margin:
        reasons.append("NUMERIC_MARGIN_AVAILABLE_FALSE")
    if public_claim_false:
        reasons.append("PUBLIC_CLAIM_FALSE")

    return {
        "irrep_id": row.get("irrep_id", ""),
        "irrep": row.get("irrep", ""),
        "torsion_component": row.get("torsion_component", ""),
        "source_path": row.get("source_path", ""),
        "source_exists": source_ok,
        "operator_eigenvalue": row.get("operator_eigenvalue", ""),
        "critical_surface": row.get("critical_surface", ""),
        "diagonal_by_lorentz_parity": diagonal,
        "eigenvalue_symbolic_written": eigenvalue_symbolic,
        "nonzero_contract_written": nonzero_contract,
        "positive_parent_signed": positive_parent_signed,
        "numeric_margin_available": numeric_margin,
        "current_status": status,
        "valid_for_claim": valid_for_claim,
        "claim_allowed": valid_for_claim,
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
    }


def evaluate_bound_row(row: Dict[str, str]) -> Dict[str, object]:
    source_ok = path_exists(row.get("source_path", ""))
    formula_written = as_bool(row.get("formula_written", "False"))
    lambda_margin_symbolic = as_bool(row.get("lambda_margin_symbolic", "False"))
    spin_source_numeric = as_bool(row.get("spin_source_numeric", "False"))
    experiment_bound_sourced = as_bool(row.get("experiment_bound_sourced", "False"))
    public_claim_false = as_bool(row.get("public_claim_false", "True"))

    if source_ok and formula_written and lambda_margin_symbolic and spin_source_numeric and experiment_bound_sourced:
        status = "SPIN_CONTACT_BOUND_NUMERIC_READY"
    elif source_ok and formula_written and lambda_margin_symbolic:
        status = "SPIN_CONTACT_FORMULA_READY_NUMERIC_INPUTS_MISSING"
    elif source_ok and formula_written:
        status = "SPIN_CONTACT_FORMULA_READY_MARGIN_OPEN"
    elif source_ok:
        status = "SOURCE_PRESENT_BOUND_FORMULA_OPEN"
    else:
        status = "SOURCE_MISSING"

    valid_for_claim = source_ok and formula_written and lambda_margin_symbolic and spin_source_numeric and experiment_bound_sourced and not public_claim_false
    reasons = []
    if not source_ok:
        reasons.append("SOURCE_PATH_MISSING")
    if not formula_written:
        reasons.append("FORMULA_WRITTEN_FALSE")
    if not lambda_margin_symbolic:
        reasons.append("LAMBDA_MARGIN_SYMBOLIC_FALSE")
    if not spin_source_numeric:
        reasons.append("SPIN_SOURCE_NUMERIC_FALSE")
    if not experiment_bound_sourced:
        reasons.append("EXPERIMENT_BOUND_SOURCED_FALSE")
    if public_claim_false:
        reasons.append("PUBLIC_CLAIM_FALSE")

    return {
        "bound_id": row.get("bound_id", ""),
        "arena": row.get("arena", ""),
        "source_path": row.get("source_path", ""),
        "source_exists": source_ok,
        "bound_formula": row.get("bound_formula", ""),
        "formula_written": formula_written,
        "lambda_margin_symbolic": lambda_margin_symbolic,
        "spin_source_numeric": spin_source_numeric,
        "experiment_bound_sourced": experiment_bound_sourced,
        "current_status": status,
        "valid_for_claim": valid_for_claim,
        "claim_allowed": valid_for_claim,
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate torsion operator invertibility and spin-contact bound rows.")
    parser.add_argument("--mode", choices=["irrep", "bound"], required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = read_csv(args.input)
    output = [evaluate_irrep_row(row) for row in rows] if args.mode == "irrep" else [evaluate_bound_row(row) for row in rows]
    write_csv(args.output, output)


if __name__ == "__main__":
    main()
