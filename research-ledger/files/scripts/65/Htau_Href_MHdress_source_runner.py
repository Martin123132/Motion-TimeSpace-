from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


def parse_float(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.upper().startswith("MISSING") or text.upper() in {"NA", "N/A", "NONE"}:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def format_float(value: float | None) -> str:
    if value is None or not math.isfinite(value):
        return "MISSING_NUMERIC_VALUE"
    return f"{value:.15e}"


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def compute_row(row: dict[str, Any]) -> dict[str, Any]:
    source_id = str(row.get("source_id", "")).strip() or "UNNAMED_SOURCE"
    h_tau = parse_float(row.get("H_tau_kg"))
    h_ref = parse_float(row.get("H_ref_kg"))
    mass_comparator = parse_float(row.get("M_GM_cal_kg"))

    output: dict[str, Any] = {
        "source_id": source_id,
        "row_status_input": row.get("row_status", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }

    if h_tau is None or h_ref is None:
        output.update(
            {
                "M_H_dress_kg": "MISSING_NUMERIC_VALUE",
                "Delta_MH_rel": "MISSING_NUMERIC_VALUE",
                "runner_status": "BLOCKED_MISSING_HTAU_OR_HREF",
                "anti_circularity_status": "PASS_NO_GM_BACKFILL",
            }
        )
        return output

    m_h_dress = h_tau - h_ref
    if m_h_dress <= 0:
        runner_status = "FAILED_NONPOSITIVE_MHDRESS"
    elif mass_comparator is None or mass_comparator <= 0:
        runner_status = "MHDRESS_COMPUTED_COMPARATOR_MISSING_NONCLAIM"
    elif str(row.get("row_status", "")).strip().lower().startswith("counterfactual"):
        runner_status = "MHDRESS_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM"
    else:
        runner_status = "MHDRESS_COMPUTED_NONCLAIM"

    delta_mh = None
    if mass_comparator is not None and mass_comparator > 0:
        delta_mh = (m_h_dress - mass_comparator) / mass_comparator

    output.update(
        {
            "M_H_dress_kg": format_float(m_h_dress),
            "Delta_MH_rel": format_float(delta_mh),
            "runner_status": runner_status,
            "anti_circularity_status": "PASS_HTAU_MINUS_HREF_USED",
        }
    )
    return output


def run(input_csv: Path, output_csv: Path) -> None:
    with input_csv.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"input CSV has no rows: {input_csv}")

    outputs = [compute_row(row) for row in rows]
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(outputs[0].keys()))
        writer.writeheader()
        writer.writerows(outputs)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: Htau_Href_MHdress_source_runner.py INPUT.csv OUTPUT.csv", file=sys.stderr)
        return 2
    run(Path(argv[1]), Path(argv[2]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
