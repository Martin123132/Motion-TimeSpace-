from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List, Mapping


REQUIRED_FIELDS = [
    "row_id",
    "object_id",
    "constant_pairing",
    "linear_x_pairing",
    "linear_y_pairing",
    "linear_z_pairing",
    "units",
    "source_path",
    "input_valid_for_claim",
]
FORBIDDEN_MARKERS = ["SYNTHETIC", "SMOKE", "PLACEHOLDER", "MISSING", "NOT_PHYSICAL", "SURROGATE_NOT_OFFICIAL"]


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: List[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: str(row.get(field, "")) for field in fields})


def bool_text(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def contains_forbidden_marker(value: object) -> bool:
    text = str(value).upper()
    return any(marker in text for marker in FORBIDDEN_MARKERS)


def parse_float(row: Mapping[str, str], field: str) -> float:
    return float(str(row.get(field, "")).strip())


def evaluate_row(row: Mapping[str, str], input_path: Path, tolerance: float) -> Dict[str, str]:
    missing_fields = [field for field in REQUIRED_FIELDS if field not in row or str(row.get(field, "")).strip() == ""]
    numeric_parse_ok = True
    pairings: Dict[str, float] = {}
    for field in ["constant_pairing", "linear_x_pairing", "linear_y_pairing", "linear_z_pairing"]:
        try:
            pairings[field] = parse_float(row, field)
        except Exception:
            numeric_parse_ok = False
            pairings[field] = float("nan")
    max_abs_pairing = max(abs(value) for value in pairings.values()) if numeric_parse_ok else float("nan")
    boundary_silent = numeric_parse_ok and max_abs_pairing <= tolerance
    source_path = str(row.get("source_path", "")).strip()
    source_declared = bool(source_path)
    source_exists = Path(source_path).exists() if source_declared and not contains_forbidden_marker(source_path) else False
    no_forbidden_markers = not any(contains_forbidden_marker(value) for value in row.values())
    input_flag = bool_text(row.get("input_valid_for_claim", "False"))
    valid_for_scoring = not missing_fields and numeric_parse_ok and source_declared
    valid_for_claim = valid_for_scoring and boundary_silent and source_exists and no_forbidden_markers and input_flag
    if missing_fields:
        status = "BOUNDARY_ROW_MISSING_FIELDS"
    elif not numeric_parse_ok:
        status = "BOUNDARY_PAIRING_NUMERIC_PARSE_FAILED"
    elif boundary_silent:
        status = "BOUNDARY_AFFINE_PAIRINGS_ZERO_NONCLAIM"
    else:
        status = "BOUNDARY_AFFINE_PAIRINGS_NONZERO_NONCLAIM"
    return {
        "row_id": str(row.get("row_id", "")),
        "object_id": str(row.get("object_id", "")),
        "input_path": str(input_path),
        "constant_pairing": str(row.get("constant_pairing", "")),
        "linear_x_pairing": str(row.get("linear_x_pairing", "")),
        "linear_y_pairing": str(row.get("linear_y_pairing", "")),
        "linear_z_pairing": str(row.get("linear_z_pairing", "")),
        "max_abs_pairing": f"{max_abs_pairing:.16e}",
        "tolerance": f"{tolerance:.16e}",
        "missing_fields": ";".join(missing_fields),
        "numeric_parse_ok": str(numeric_parse_ok),
        "boundary_silent": str(boundary_silent),
        "source_declared": str(source_declared),
        "source_exists": str(source_exists),
        "no_forbidden_markers": str(no_forbidden_markers),
        "input_valid_for_claim": str(input_flag),
        "valid_for_scoring": str(valid_for_scoring),
        "valid_for_claim": str(valid_for_claim),
        "claim_allowed": str(valid_for_claim),
        "current_status": status,
    }


def evaluate_boundary_rows(input_path: Path, tolerance: float = 1.0e-12) -> List[Dict[str, str]]:
    return [evaluate_row(row, input_path, tolerance) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Gate double-divergence affine boundary pairings for source-backed rows.")
    parser.add_argument("--input", required=True, type=Path, help="Boundary pairing CSV.")
    parser.add_argument("--output", required=True, type=Path, help="Gate output CSV.")
    parser.add_argument("--tolerance", type=float, default=1.0e-12, help="Absolute zero tolerance.")
    args = parser.parse_args()
    write_csv(args.output, evaluate_boundary_rows(args.input, args.tolerance))


if __name__ == "__main__":
    main()
