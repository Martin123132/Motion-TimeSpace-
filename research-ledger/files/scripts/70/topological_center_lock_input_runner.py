from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence


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


def group_rows(rows: Iterable[Mapping[str, str]]) -> Dict[str, List[Mapping[str, str]]]:
    groups: Dict[str, List[Mapping[str, str]]] = defaultdict(list)
    for index, row in enumerate(rows):
        profile_id = str(row.get("profile_id", "")).strip() or f"profile_{index:04d}"
        groups[profile_id].append(row)
    return dict(groups)


def mass_center(rows: Sequence[Mapping[str, str]], density_field: str) -> Dict[str, float]:
    total_mass = 0.0
    moment_x = 0.0
    moment_y = 0.0
    moment_z = 0.0
    for row in rows:
        mass_piece = parse_float(row, density_field) * parse_float(row, "volume_weight", 1.0)
        total_mass += mass_piece
        moment_x += mass_piece * parse_float(row, "x")
        moment_y += mass_piece * parse_float(row, "y")
        moment_z += mass_piece * parse_float(row, "z")
    if total_mass == 0.0:
        return {"mass": 0.0, "x": math.nan, "y": math.nan, "z": math.nan}
    return {
        "mass": total_mass,
        "x": moment_x / total_mass,
        "y": moment_y / total_mass,
        "z": moment_z / total_mass,
    }


def profile_center_rows(profile_rows: Sequence[Mapping[str, str]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    profile_id = str(profile_rows[0].get("profile_id", "")).strip()
    center_h = mass_center(profile_rows, "rho_H")
    center_top = mass_center(profile_rows, "rho_top")
    radius = first_float(profile_rows, "R", 0.0)
    if radius <= 0.0:
        radius = max(
            math.sqrt(parse_float(row, "x") ** 2 + parse_float(row, "y") ** 2 + parse_float(row, "z") ** 2)
            for row in profile_rows
        )
    if center_h["mass"] == 0.0 or center_top["mass"] == 0.0 or radius <= 0.0:
        b_value = math.nan
        b_over_r = math.nan
        status = "CENTER_UNDEFINED_MISSING_POSITIVE_MASS_OR_RADIUS"
    else:
        dx = center_top["x"] - center_h["x"]
        dy = center_top["y"] - center_h["y"]
        dz = center_top["z"] - center_h["z"]
        b_value = math.sqrt(dx * dx + dy * dy + dz * dz)
        b_over_r = b_value / radius
        status = "CENTER_OFFSET_COMPUTED_NONCLAIM"
    input_valid = all(bool_text(row.get("input_valid_for_claim", "False")) for row in profile_rows)
    rows.append(
        {
            "profile_id": profile_id,
            "profile_label": first_text(profile_rows, "profile_label", profile_id),
            "source_body": first_text(profile_rows, "source_body"),
            "arena": first_text(profile_rows, "arena"),
            "row_count": str(len(profile_rows)),
            "M_H": f"{center_h['mass']:.16e}",
            "M_top": f"{center_top['mass']:.16e}",
            "center_H_x": f"{center_h['x']:.16e}",
            "center_H_y": f"{center_h['y']:.16e}",
            "center_H_z": f"{center_h['z']:.16e}",
            "center_top_x": f"{center_top['x']:.16e}",
            "center_top_y": f"{center_top['y']:.16e}",
            "center_top_z": f"{center_top['z']:.16e}",
            "b_center_offset": f"{b_value:.16e}",
            "R": f"{radius:.16e}",
            "b_over_R": f"{b_over_r:.16e}",
            "input_valid_for_claim": str(input_valid),
            "current_status": status,
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    )
    return rows


def compute_profile_center_rows(input_path: Path) -> List[Dict[str, str]]:
    rows = read_csv(input_path)
    output_rows: List[Dict[str, str]] = []
    for _, profile_rows in sorted(group_rows(rows).items()):
        output_rows.extend(profile_center_rows(profile_rows))
    return output_rows


def envelope_score_rows(center_rows: Sequence[Mapping[str, str]], envelope_rows: Sequence[Mapping[str, str]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for center_row in center_rows:
        b_over_r = parse_float(center_row, "b_over_R", math.nan)
        for envelope in envelope_rows:
            power = int(envelope["center_offset_power"])
            coefficient = float(envelope["deltaa_over_a_coeff"])
            if math.isnan(b_over_r):
                predicted = math.nan
                status = "CENTER_OFFSET_MISSING"
            else:
                predicted = coefficient * (b_over_r**power)
                status = "CENTER_OFFSET_SCORE_COMPUTED_NONCLAIM"
            rows.append(
                {
                    "score_id": f"CLS4383_{center_row['profile_id']}_{envelope['support_id']}_l{envelope['multipole_l']}",
                    "profile_id": center_row["profile_id"],
                    "support_id": envelope["support_id"],
                    "source_body": envelope["source_body"],
                    "test_body_or_readout": envelope["test_body_or_readout"],
                    "multipole_l": envelope["multipole_l"],
                    "b_over_R": center_row["b_over_R"],
                    "deltaa_over_a_coeff": envelope["deltaa_over_a_coeff"],
                    "predicted_deltaa_over_a_envelope": f"{predicted:.16e}",
                    "delta_N_value": envelope.get("delta_N_value", "MISSING_DELTA_N"),
                    "pass_formula": envelope["pass_formula"],
                    "current_status": status if envelope.get("delta_N_value") != "MISSING_DELTA_N" else "SCORE_COMPUTED_DELTA_N_MISSING_NONCLAIM",
                    "valid_for_claim": "False",
                    "claim_allowed": "False",
                }
            )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute topological/Hilbert center offsets and envelope scores.")
    parser.add_argument("--input", required=True, type=Path, help="Profile CSV with profile_id,x,y,z,volume_weight,rho_H,rho_top,R.")
    parser.add_argument("--envelopes", required=True, type=Path, help="4382 center-offset envelope rows.")
    parser.add_argument("--centers-output", required=True, type=Path, help="Output profile-center rows.")
    parser.add_argument("--scores-output", required=True, type=Path, help="Output arena score rows.")
    args = parser.parse_args()
    center_rows = compute_profile_center_rows(args.input)
    write_csv(args.centers_output, center_rows)
    write_csv(args.scores_output, envelope_score_rows(center_rows, read_csv(args.envelopes)))


if __name__ == "__main__":
    main()
