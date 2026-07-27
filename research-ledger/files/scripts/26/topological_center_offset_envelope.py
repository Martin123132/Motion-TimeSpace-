from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Dict, List


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


def center_offset_constant(multipole_l: int) -> float:
    if multipole_l == 1:
        return 4.0 * math.sqrt(math.pi)
    if multipole_l == 2:
        return 6.0 * math.sqrt(math.pi)
    raise ValueError(f"unsupported multipole_l={multipole_l}; only l=1,2 are implemented")


def center_offset_rows(bound_rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for row in bound_rows:
        multipole_l = int(row["multipole_l"])
        if multipole_l not in (1, 2):
            continue
        geometry_factor = float(row["geometry_factor_s_l"])
        constant = center_offset_constant(multipole_l)
        coefficient = geometry_factor * constant
        offset_symbol = "(b/R)" if multipole_l == 1 else "(b/R)^2"
        required_formula = (
            f"b/R <= delta_N/{coefficient:.16e}"
            if multipole_l == 1
            else f"b/R <= sqrt(delta_N/{coefficient:.16e})"
        )
        rows.append(
            {
                "envelope_id": f"COE4382_{row['bound_id']}",
                "bound_id": row["bound_id"],
                "support_id": row["support_id"],
                "source_body": row["source_body"],
                "test_body_or_readout": row["test_body_or_readout"],
                "multipole_l": str(multipole_l),
                "geometry_factor_s_l": row["geometry_factor_s_l"],
                "center_offset_constant_C_l": f"{constant:.16e}",
                "deltaa_over_a_coeff": f"{coefficient:.16e}",
                "center_offset_power": str(multipole_l),
                "envelope_law": f"|deltaa_top,l={multipole_l}|/|a_N| <= {coefficient:.16e} {offset_symbol}",
                "pass_formula": required_formula,
                "delta_N_value": "MISSING_DELTA_N",
                "b_over_R_value": "MISSING_PARENT_CENTER_OFFSET_BOUND",
                "current_status": "CENTER_OFFSET_ENVELOPE_READY_VALUES_MISSING",
                "valid_for_claim": "False",
                "claim_allowed": "False",
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Build center-offset envelope rows from 4378 topological multipole bound rows.")
    parser.add_argument("--bounds", required=True, type=Path, help="4378 topological multipole bound CSV.")
    parser.add_argument("--output", required=True, type=Path, help="Output center-offset envelope CSV.")
    args = parser.parse_args()
    write_csv(args.output, center_offset_rows(read_csv(args.bounds)))


if __name__ == "__main__":
    main()
