from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


FORBIDDEN_SOURCE_TOKENS = (
    "ORBITAL_GM_DEFINITION",
    "GM_AS_SOURCE",
    "FITTED_ACCELERATION",
    "POSTFIT_REFERENCE",
    "OBSERVED_RESIDUAL_CANCEL",
)


def parse_float(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.upper().startswith("MISSING") or text.upper() in {"NA", "N/A", "NONE"}:
        return None
    try:
        number = float(text)
    except ValueError:
        return None
    return number if math.isfinite(number) else None


def format_float(value: float | None) -> str:
    if value is None or not math.isfinite(value):
        return "MISSING_NUMERIC_VALUE"
    return f"{value:.15e}"


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def row_is_counterfactual(row: dict[str, Any]) -> bool:
    text = str(row.get("row_status", "")).strip().lower()
    return text.startswith("counterfactual") or "counterfactual" in text


def row_is_private(row: dict[str, Any]) -> bool:
    text = str(row.get("row_status", "")).strip().lower()
    return text.startswith("private") or "private" in text


def forbidden_source_used(row: dict[str, Any]) -> bool:
    source_text = " ".join(
        str(row.get(field, ""))
        for field in ("anchor_source", "reference_selector_source", "counterterm_source", "provenance")
    ).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def residual_abs_sum(row: dict[str, Any]) -> float | None:
    residual_fields = (
        "Delta_ref_selector_abs_kg",
        "Delta_ref_boundary_abs_kg",
        "Delta_ref_frame_abs_kg",
        "Delta_ref_readout_abs_kg",
        "Delta_ref_counterterm_abs_kg",
    )
    total = 0.0
    for field in residual_fields:
        value = parse_float(row.get(field))
        if value is None:
            return None
        total += abs(value)
    return total


def all_zero_clauses_signed(row: dict[str, Any]) -> bool:
    clause_fields = (
        "zero_anchor_signed",
        "source_blind_signed",
        "fixed_before_readout_signed",
        "qbasic_descent_signed",
        "same_tau_eobs_surface_signed",
        "no_postfit_signed",
        "boundary_no_flux_signed",
        "reference_curl_zero_signed",
    )
    return all(bool_text(row.get(field)) for field in clause_fields)


def compute_row(row: dict[str, Any]) -> dict[str, Any]:
    reference_id = str(row.get("reference_id", "")).strip() or "UNNAMED_HREF_ROW"
    h_ref_anchor = parse_float(row.get("H_ref_anchor_kg"))
    m_lower = parse_float(row.get("M_lower_kg"))
    residual_radius = residual_abs_sum(row)
    counterfactual = row_is_counterfactual(row)
    private = row_is_private(row)
    circular_source = forbidden_source_used(row)
    zero_clauses = all_zero_clauses_signed(row)

    output: dict[str, Any] = {
        "reference_id": reference_id,
        "row_status_input": row.get("row_status", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
        "zero_clauses_signed": zero_clauses,
    }

    if circular_source and not counterfactual:
        output.update(
            {
                "H_ref_kg": "MISSING_NUMERIC_VALUE",
                "H_ref_abs_bound_kg": "MISSING_NUMERIC_VALUE",
                "epsilon_Href_abs": "MISSING_NUMERIC_VALUE",
                "runner_status": "FAILED_CIRCULAR_POSTFIT_REFERENCE",
                "anti_circularity_status": "FAIL_REFERENCE_USES_FITTED_OR_OBSERVED_RESIDUAL_SOURCE",
            }
        )
        return output

    if h_ref_anchor is None:
        output.update(
            {
                "H_ref_kg": "MISSING_NUMERIC_VALUE",
                "H_ref_abs_bound_kg": "MISSING_NUMERIC_VALUE",
                "epsilon_Href_abs": "MISSING_NUMERIC_VALUE",
                "runner_status": "BLOCKED_MISSING_HREF_ANCHOR",
                "anti_circularity_status": "PASS_NO_POSTFIT_REFERENCE",
            }
        )
        return output

    if residual_radius is None:
        output.update(
            {
                "H_ref_kg": format_float(h_ref_anchor),
                "H_ref_abs_bound_kg": "MISSING_NUMERIC_VALUE",
                "epsilon_Href_abs": "MISSING_NUMERIC_VALUE",
                "runner_status": "BLOCKED_MISSING_HREF_RESIDUAL_RADIUS",
                "anti_circularity_status": "PASS_NO_POSTFIT_REFERENCE",
            }
        )
        return output

    h_ref_abs_bound = abs(h_ref_anchor) + residual_radius
    epsilon_href = h_ref_abs_bound / m_lower if m_lower is not None and m_lower > 0 else None

    if zero_clauses and h_ref_anchor == 0 and residual_radius == 0:
        if counterfactual:
            runner_status = "HREF_COUNTERFACTUAL_ZERO_SMOKE_PASS_NONCLAIM"
        elif private:
            runner_status = "HREF_ZERO_CERTIFIED_PRIVATE_NONCLAIM"
        else:
            runner_status = "HREF_ZERO_CERTIFIED_NONCLAIM"
    elif zero_clauses and residual_radius == 0:
        runner_status = "HREF_FIXED_VALUE_CERTIFIED_NONCLAIM"
    elif m_lower is None or m_lower <= 0:
        runner_status = "HREF_BOUND_COMPUTED_BLOCKED_MLOWER"
    else:
        runner_status = "HREF_BOUND_COMPUTED_NONCLAIM"

    output.update(
        {
            "H_ref_kg": format_float(h_ref_anchor),
            "H_ref_abs_bound_kg": format_float(h_ref_abs_bound),
            "epsilon_Href_abs": format_float(epsilon_href),
            "runner_status": runner_status,
            "anti_circularity_status": "PASS_FIXED_REFERENCE_NO_POSTFIT",
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
        print("usage: Href_zero_certificate_runner.py INPUT.csv OUTPUT.csv", file=sys.stderr)
        return 2
    run(Path(argv[1]), Path(argv[2]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
