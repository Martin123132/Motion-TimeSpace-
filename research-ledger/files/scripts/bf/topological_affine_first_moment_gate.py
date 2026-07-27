from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence


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


def contains_forbidden_marker(value: object) -> bool:
    text = str(value).upper()
    return any(marker in text for marker in FORBIDDEN_MARKERS)


def first_text(rows: Sequence[Mapping[str, str]], field: str, default: str = "") -> str:
    for row in rows:
        value = str(row.get(field, "")).strip()
        if value:
            return value
    return default


def first_float(rows: Sequence[Mapping[str, str]], field: str, default: float = 0.0) -> float:
    for row in rows:
        value = str(row.get(field, "")).strip()
        if value:
            return float(value)
    return default


def group_rows(rows: Iterable[Mapping[str, str]]) -> Dict[str, List[Mapping[str, str]]]:
    groups: Dict[str, List[Mapping[str, str]]] = defaultdict(list)
    for index, row in enumerate(rows):
        profile_id = str(row.get("profile_id", "")).strip() or f"profile_{index:04d}"
        groups[profile_id].append(row)
    return dict(groups)


def affine_first_moment_row(profile_id: str, rows: Sequence[Mapping[str, str]], input_path: Path, tolerance: float) -> Dict[str, str]:
    m_h = 0.0
    m_top = 0.0
    delta_m = 0.0
    moment_x = 0.0
    moment_y = 0.0
    moment_z = 0.0
    numeric_parse_ok = True
    positive_weight = True
    source_paths_declared = True
    input_flags_true = True
    no_forbidden_markers = True
    for row in rows:
        try:
            weight = parse_float(row, "volume_weight", 1.0)
            x_value = parse_float(row, "x")
            y_value = parse_float(row, "y")
            z_value = parse_float(row, "z")
            rho_h = parse_float(row, "rho_H")
            rho_top = parse_float(row, "rho_top")
        except Exception:
            numeric_parse_ok = False
            weight = 0.0
            x_value = 0.0
            y_value = 0.0
            z_value = 0.0
            rho_h = 0.0
            rho_top = 0.0
        positive_weight = positive_weight and weight > 0.0
        source_paths_declared = source_paths_declared and bool(str(row.get("source_profile_path", "")).strip())
        input_flags_true = input_flags_true and bool_text(row.get("input_valid_for_claim", "False"))
        no_forbidden_markers = no_forbidden_markers and not any(contains_forbidden_marker(value) for value in row.values())
        delta_density = rho_top - rho_h
        m_h += rho_h * weight
        m_top += rho_top * weight
        delta_m += delta_density * weight
        moment_x += x_value * delta_density * weight
        moment_y += y_value * delta_density * weight
        moment_z += z_value * delta_density * weight
    radius = first_float(rows, "R", 0.0)
    if radius <= 0.0:
        radius = math.nan
    if m_h > 0.0:
        b_x = moment_x / m_h
        b_y = moment_y / m_h
        b_z = moment_z / m_h
        b_norm = math.sqrt(b_x * b_x + b_y * b_y + b_z * b_z)
    else:
        b_x = math.nan
        b_y = math.nan
        b_z = math.nan
        b_norm = math.nan
    b_over_r = b_norm / radius if radius and radius > 0.0 and not math.isnan(b_norm) else math.nan
    monopole_zero = abs(delta_m) <= tolerance
    linear_zero = not math.isnan(b_norm) and b_norm <= tolerance
    profile_scoreable = numeric_parse_ok and positive_weight and m_h > 0.0 and m_top > 0.0 and radius > 0.0 and source_paths_declared
    valid_for_claim = profile_scoreable and input_flags_true and no_forbidden_markers and monopole_zero and linear_zero
    if not numeric_parse_ok:
        status = "AFFINE_MOMENT_NUMERIC_PARSE_FAILED"
    elif m_h <= 0.0 or m_top <= 0.0:
        status = "AFFINE_MOMENT_MASS_NOT_POSITIVE"
    elif not monopole_zero:
        status = "AFFINE_MONOPOLE_NONZERO_COMPUTED_NONCLAIM"
    elif linear_zero:
        status = "AFFINE_FIRST_MOMENT_ZERO_COMPUTED_NONCLAIM"
    else:
        status = "AFFINE_FIRST_MOMENT_NONZERO_COMPUTED_NONCLAIM"
    return {
        "profile_id": profile_id,
        "profile_label": first_text(rows, "profile_label", profile_id),
        "input_path": str(input_path),
        "row_count": str(len(rows)),
        "M_H": f"{m_h:.16e}",
        "M_top": f"{m_top:.16e}",
        "Delta_M_top_H": f"{delta_m:.16e}",
        "B_top_x": f"{b_x:.16e}",
        "B_top_y": f"{b_y:.16e}",
        "B_top_z": f"{b_z:.16e}",
        "B_top_norm": f"{b_norm:.16e}",
        "R": f"{radius:.16e}",
        "B_top_norm_over_R": f"{b_over_r:.16e}",
        "tolerance": f"{tolerance:.16e}",
        "monopole_zero": str(monopole_zero),
        "linear_affine_zero": str(linear_zero),
        "numeric_parse_ok": str(numeric_parse_ok),
        "positive_volume_weights": str(positive_weight),
        "source_paths_declared": str(source_paths_declared),
        "input_valid_flags_true": str(input_flags_true),
        "no_forbidden_markers": str(no_forbidden_markers),
        "valid_for_scoring": str(profile_scoreable),
        "valid_for_claim": str(valid_for_claim),
        "claim_allowed": str(valid_for_claim),
        "current_status": status,
    }


def affine_first_moment_rows(input_path: Path, tolerance: float = 1.0e-12) -> List[Dict[str, str]]:
    rows = read_csv(input_path)
    return [
        affine_first_moment_row(profile_id, profile_rows, input_path, tolerance)
        for profile_id, profile_rows in sorted(group_rows(rows).items())
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute monopole and affine first-moment residuals for rho_top-rho_H.")
    parser.add_argument("--input", required=True, type=Path, help="Profile CSV with x,y,z,volume_weight,rho_H,rho_top,R.")
    parser.add_argument("--output", required=True, type=Path, help="Output affine first-moment CSV.")
    parser.add_argument("--tolerance", type=float, default=1.0e-12, help="Absolute zero tolerance for monopole and B_top.")
    args = parser.parse_args()
    write_csv(args.output, affine_first_moment_rows(args.input, args.tolerance))


if __name__ == "__main__":
    main()
