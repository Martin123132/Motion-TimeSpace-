from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence


REQUIRED_FIELDS = ["profile_id", "x", "y", "z", "volume_weight", "rho_H", "rho_top", "R", "source_profile_path"]
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


def parse_float(row: Mapping[str, str], field: str, default: float = 0.0) -> float:
    value = str(row.get(field, "")).strip()
    if value == "":
        return default
    return float(value)


def bool_text(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def group_rows(rows: Iterable[Mapping[str, str]]) -> Dict[str, List[Mapping[str, str]]]:
    groups: Dict[str, List[Mapping[str, str]]] = defaultdict(list)
    for index, row in enumerate(rows):
        profile_id = str(row.get("profile_id", "")).strip() or f"profile_{index:04d}"
        groups[profile_id].append(row)
    return dict(groups)


def contains_forbidden_marker(value: object) -> bool:
    text = str(value).upper()
    return any(marker in text for marker in FORBIDDEN_MARKERS)


def validate_profile(profile_id: str, rows: Sequence[Mapping[str, str]], input_path: Path) -> Dict[str, str]:
    fields = set().union(*(row.keys() for row in rows))
    missing_fields = [field for field in REQUIRED_FIELDS if field not in fields]
    numeric_parse_ok = True
    positive_weight = True
    for row in rows:
        try:
            parse_float(row, "x")
            parse_float(row, "y")
            parse_float(row, "z")
            weight = parse_float(row, "volume_weight")
            parse_float(row, "rho_H")
            parse_float(row, "rho_top")
            parse_float(row, "R")
        except Exception:
            numeric_parse_ok = False
            weight = 0.0
        positive_weight = positive_weight and weight > 0.0
    m_h = sum(parse_float(row, "rho_H") * parse_float(row, "volume_weight", 1.0) for row in rows)
    m_top = sum(parse_float(row, "rho_top") * parse_float(row, "volume_weight", 1.0) for row in rows)
    radius_positive = all(parse_float(row, "R") > 0.0 for row in rows)
    no_forbidden_markers = not any(contains_forbidden_marker(value) for row in rows for value in row.values())
    input_flags_true = all(bool_text(row.get("input_valid_for_claim", "False")) for row in rows)
    source_paths_declared = all(str(row.get("source_profile_path", "")).strip() for row in rows)
    valid_for_scoring = (
        not missing_fields
        and numeric_parse_ok
        and positive_weight
        and m_h > 0.0
        and m_top > 0.0
        and radius_positive
        and source_paths_declared
    )
    valid_for_claim = valid_for_scoring and no_forbidden_markers and input_flags_true
    return {
        "profile_id": profile_id,
        "input_path": str(input_path),
        "row_count": str(len(rows)),
        "missing_fields": ";".join(missing_fields),
        "numeric_parse_ok": str(numeric_parse_ok),
        "positive_volume_weights": str(positive_weight),
        "M_H": f"{m_h:.16e}",
        "M_top": f"{m_top:.16e}",
        "positive_masses": str(m_h > 0.0 and m_top > 0.0),
        "radius_positive": str(radius_positive),
        "source_paths_declared": str(source_paths_declared),
        "no_forbidden_markers": str(no_forbidden_markers),
        "input_valid_flags_true": str(input_flags_true),
        "valid_for_scoring": str(valid_for_scoring),
        "valid_for_claim": str(valid_for_claim),
        "claim_allowed": str(valid_for_claim),
    }


def validate_import(input_path: Path) -> List[Dict[str, str]]:
    rows = read_csv(input_path)
    return [validate_profile(profile_id, profile_rows, input_path) for profile_id, profile_rows in sorted(group_rows(rows).items())]


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate real rho_H/rho_top profile imports before center-lock/quadrature scoring.")
    parser.add_argument("--input", required=True, type=Path, help="Candidate profile CSV.")
    parser.add_argument("--output", required=True, type=Path, help="Validation output CSV.")
    args = parser.parse_args()
    write_csv(args.output, validate_import(args.input))


if __name__ == "__main__":
    main()
