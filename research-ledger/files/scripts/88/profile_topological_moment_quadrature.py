from __future__ import annotations

import argparse
import cmath
import csv
import math
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence


def parse_float(row: Mapping[str, str], field: str, default: float = 0.0) -> float:
    value = str(row.get(field, "")).strip()
    if value == "":
        return default
    return float(value)


def first_float(rows: Sequence[Mapping[str, str]], field: str, default: float = 0.0) -> float:
    for row in rows:
        value = str(row.get(field, "")).strip()
        if value:
            return float(value)
    return default


def first_text(rows: Sequence[Mapping[str, str]], field: str, default: str = "") -> str:
    for row in rows:
        value = str(row.get(field, "")).strip()
        if value:
            return value
    return default


def bool_text(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def associated_legendre_lte2(l_value: int, m_value: int, x_value: float) -> float:
    x_value = max(-1.0, min(1.0, x_value))
    root = math.sqrt(max(0.0, 1.0 - x_value * x_value))
    if l_value == 0 and m_value == 0:
        return 1.0
    if l_value == 1 and m_value == 0:
        return x_value
    if l_value == 1 and m_value == 1:
        return -root
    if l_value == 2 and m_value == 0:
        return 0.5 * (3.0 * x_value * x_value - 1.0)
    if l_value == 2 and m_value == 1:
        return -3.0 * x_value * root
    if l_value == 2 and m_value == 2:
        return 3.0 * (1.0 - x_value * x_value)
    raise ValueError(f"unsupported l,m pair: {l_value},{m_value}")


def spherical_harmonic_lte2(l_value: int, m_value: int, x_coord: float, y_coord: float, z_coord: float) -> complex:
    radius = math.sqrt(x_coord * x_coord + y_coord * y_coord + z_coord * z_coord)
    if radius == 0.0:
        if l_value == 0 and m_value == 0:
            return complex(1.0 / math.sqrt(4.0 * math.pi), 0.0)
        return 0j
    if m_value < 0:
        sign = -1.0 if abs(m_value) % 2 else 1.0
        return sign * spherical_harmonic_lte2(l_value, -m_value, x_coord, y_coord, z_coord).conjugate()
    cos_theta = z_coord / radius
    phi = math.atan2(y_coord, x_coord)
    norm = math.sqrt(
        ((2 * l_value + 1) / (4.0 * math.pi))
        * (math.factorial(l_value - m_value) / math.factorial(l_value + m_value))
    )
    condon_shortley = -1.0 if m_value % 2 else 1.0
    p_lm = associated_legendre_lte2(l_value, m_value, cos_theta)
    return condon_shortley * norm * p_lm * cmath.exp(1j * m_value * phi)


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


def group_rows(rows: Iterable[Mapping[str, str]]) -> Dict[str, List[Mapping[str, str]]]:
    groups: Dict[str, List[Mapping[str, str]]] = defaultdict(list)
    for index, row in enumerate(rows):
        profile_id = str(row.get("profile_id", "")).strip() or f"profile_{index:04d}"
        groups[profile_id].append(row)
    return dict(groups)


def compute_profile_rows(profile_id: str, rows: Sequence[Mapping[str, str]]) -> List[Dict[str, str]]:
    center_x = first_float(rows, "center_x", 0.0)
    center_y = first_float(rows, "center_y", 0.0)
    center_z = first_float(rows, "center_z", 0.0)
    m_h = first_float(rows, "M_H", math.nan)
    if math.isnan(m_h):
        m_h = sum(parse_float(row, "rho_H") * parse_float(row, "volume_weight", 1.0) for row in rows)
    max_radius = 0.0
    m_delta = 0.0
    moments: Dict[int, Dict[int, complex]] = {0: {0: 0j}, 1: {-1: 0j, 0: 0j, 1: 0j}, 2: {-2: 0j, -1: 0j, 0: 0j, 1: 0j, 2: 0j}}
    input_valid = all(bool_text(row.get("input_valid_for_claim", "False")) for row in rows)
    for row in rows:
        x_coord = parse_float(row, "x") - center_x
        y_coord = parse_float(row, "y") - center_y
        z_coord = parse_float(row, "z") - center_z
        radius = math.sqrt(x_coord * x_coord + y_coord * y_coord + z_coord * z_coord)
        max_radius = max(max_radius, radius)
        volume_weight = parse_float(row, "volume_weight", 1.0)
        delta_mass = (parse_float(row, "rho_top") - parse_float(row, "rho_H")) * volume_weight
        m_delta += delta_mass
        for l_value in (0, 1, 2):
            for m_value in range(-l_value, l_value + 1):
                y_lm = spherical_harmonic_lte2(l_value, m_value, x_coord, y_coord, z_coord)
                moments[l_value][m_value] += delta_mass * (radius**l_value) * y_lm.conjugate()
    support_radius = first_float(rows, "R", max_radius)
    output_rows: List[Dict[str, str]] = []
    for l_value in (0, 1, 2):
        sum_abs = sum(abs(value) for value in moments[l_value].values())
        max_abs = max(abs(value) for value in moments[l_value].values())
        if l_value == 0:
            e_l_top = ""
            normalization = "monopole_mass_delta"
        elif m_h > 0 and support_radius > 0:
            constant = (8.0 * math.pi / 3.0) if l_value == 1 else (12.0 * math.pi / 5.0)
            e_l_top = f"{constant * sum_abs / (m_h * (support_radius**l_value)):.16e}"
            normalization = "4378_E_l_top_convention"
        else:
            e_l_top = ""
            normalization = "missing_positive_M_H_or_R"
        output_rows.append(
            {
                "profile_id": profile_id,
                "profile_label": first_text(rows, "profile_label", profile_id),
                "source_body": first_text(rows, "source_body"),
                "arena": first_text(rows, "arena"),
                "row_count": str(len(rows)),
                "center_x": f"{center_x:.16e}",
                "center_y": f"{center_y:.16e}",
                "center_z": f"{center_z:.16e}",
                "M_delta": f"{m_delta:.16e}",
                "M_H": f"{m_h:.16e}",
                "R": f"{support_radius:.16e}",
                "multipole_l": str(l_value),
                "sum_abs_M_lm": f"{sum_abs:.16e}",
                "max_abs_M_lm": f"{max_abs:.16e}",
                "M_lm_abs_values": ";".join(
                    f"m={m_value}:{abs(moments[l_value][m_value]):.16e}" for m_value in range(-l_value, l_value + 1)
                ),
                "E_l_top_4378": e_l_top,
                "normalization": normalization,
                "runner_numeric": "True",
                "input_valid_for_claim": str(input_valid),
                "valid_for_claim": "False",
                "claim_allowed": "False",
            }
        )
    return output_rows


def compute_moment_rows(input_path: Path) -> List[Dict[str, str]]:
    rows = read_csv(input_path)
    output_rows: List[Dict[str, str]] = []
    for profile_id, profile_rows in sorted(group_rows(rows).items()):
        output_rows.extend(compute_profile_rows(profile_id, profile_rows))
    return output_rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute l<=2 topological profile moments from rho_H/rho_top sample rows.")
    parser.add_argument("--input", required=True, type=Path, help="CSV with profile_id,x,y,z,volume_weight,rho_H,rho_top rows.")
    parser.add_argument("--output", required=True, type=Path, help="Output CSV with l=0,1,2 moment rows.")
    args = parser.parse_args()
    write_csv(args.output, compute_moment_rows(args.input))


if __name__ == "__main__":
    main()
