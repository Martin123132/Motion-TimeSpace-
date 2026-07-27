from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


VOLUME_LOCK_CLAUSES = (
    "parent_continuity_law_signed",
    "mathcalJ_C_from_parent_action_signed",
    "Sigma_C_source_defined_signed",
    "Phi_C_boundary_flux_defined_signed",
    "stationary_domain_transport_signed",
    "local_no_source_condition_signed",
    "local_no_flux_condition_signed",
    "moving_boundary_zero_or_bound_signed",
    "PD_variation_owner_signed",
    "ND_normalization_variation_signed",
    "FLRW_active_class_preserved_signed",
    "Bianchi_Ward_stress_accounting_signed",
    "matter_selector_same_domain_signed",
    "no_volume_lock_by_assertion_signed",
)

EDGE_BOUND_CLAUSES = (
    "edge_surface_certificate_signed",
    "corner_zero_or_bound_signed",
    "dSFeps_zero_or_bound_signed",
    "bC_norm_source_signed",
    "harmonic_zero_or_bound_signed",
    "residual_zero_or_bound_signed",
    "cocycle_zero_or_bound_signed",
    "projector_tail_zero_or_bound_signed",
    "units_declared_signed",
    "no_edge_cancellation_signed",
)

FORBIDDEN_SOURCE_TOKENS = (
    "ACTION_BY_DECLARATION",
    "CONTINUITY_BY_ASSERTION",
    "VOLUME_LOCK_BY_ASSERTION",
    "LOCAL_FLRW_HAND_SWITCH",
    "SIGMA_BY_DECLARATION",
    "PHI_BY_DECLARATION",
    "DOMAIN_TRANSPORT_BY_DECLARATION",
    "PD_BY_LABEL",
    "PD_BY_DECLARATION",
    "EDGE_CANCELLATION",
    "BOUNDARY_ZERO_BY_ASSERTION",
    "CORNER_ZERO_BY_ASSERTION",
    "DSFEPS_ZERO_BY_ASSERTION",
    "POSTFIT_REFERENCE",
    "OBSERVED_RESIDUAL_CANCEL",
    "ORBITAL_GM_DEFINITION",
    "R10_BOUND_AS_SOURCE",
)


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y", "pass", "signed"}


def missing_text(value: Any) -> bool:
    text = str(value or "").strip()
    return not text or text.upper().startswith("MISSING") or text.upper() in {"NA", "N/A", "NONE", "NOT_COMPUTED"}


def parse_float(value: Any) -> float | None:
    if missing_text(value):
        return None
    try:
        number = float(str(value).strip())
    except ValueError:
        return None
    return number if math.isfinite(number) else None


def format_float(value: float | None) -> str:
    if value is None or not math.isfinite(value):
        return "MISSING_NUMERIC_VALUE"
    return f"{value:.15e}"


def forbidden_source_used(row: dict[str, Any]) -> bool:
    source_text = " ".join(
        str(row.get(field, ""))
        for field in (
            "source_path",
            "continuity_source",
            "JC_source",
            "Sigma_source",
            "Phi_source",
            "domain_transport_source",
            "PD_source",
            "FLRW_source",
            "edge_source",
            "corner_source",
            "dSFeps_source",
            "bC_source",
            "harmonic_source",
            "residual_source",
            "units_source",
            "provenance",
            "notes",
        )
    ).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_clauses(row: dict[str, Any], clauses: tuple[str, ...]) -> list[str]:
    return [clause for clause in clauses if not bool_text(row.get(clause))]


def volume_lock_row(row: dict[str, Any]) -> dict[str, Any]:
    selector_id = str(row.get("selector_id", "")).strip() or "UNNAMED_VOLUME_LOCK"
    output: dict[str, Any] = {
        "selector_id": selector_id,
        "row_status_input": row.get("row_status", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "Z_parent_continuity": False,
                "Z_local_lock": False,
                "Z_FLRW_compatible": False,
                "raw_volume_lock_abs": "MISSING_NUMERIC_VALUE",
                "source_flux_bound_abs": "MISSING_NUMERIC_VALUE",
                "unclosed_volume_lock_abs": "MISSING_NUMERIC_VALUE",
                "missing_volume_lock_inputs": "FORBIDDEN_VOLUME_LOCK_OR_POSTFIT_SOURCE",
                "runner_status": "FAILED_PARENT_VOLUME_LOCK_GATE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    missing = missing_clauses(row, VOLUME_LOCK_CLAUSES)
    if not missing:
        output.update(
            {
                "Z_parent_continuity": True,
                "Z_local_lock": True,
                "Z_FLRW_compatible": True,
                "raw_volume_lock_abs": "0.000000000000000e+00",
                "source_flux_bound_abs": "0.000000000000000e+00",
                "unclosed_volume_lock_abs": "0.000000000000000e+00",
                "missing_volume_lock_inputs": "",
                "runner_status": "PARENT_VOLUME_LOCK_SELECTOR_CONDITIONAL_THEOREM_NONCLAIM",
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    values = {
        "delta_JC_integral": parse_float(row.get("delta_JC_integral")),
        "target_volume_lock": parse_float(row.get("target_volume_lock")),
        "source_term_integral_abs": parse_float(row.get("source_term_integral_abs")),
        "boundary_flux_abs": parse_float(row.get("boundary_flux_abs")),
        "moving_boundary_abs": parse_float(row.get("moving_boundary_abs")),
        "normalization_drift_abs": parse_float(row.get("normalization_drift_abs")),
    }
    numeric_missing = [field for field, value in values.items() if value is None]
    source_missing = [
        field
        for field in ("continuity_source", "Sigma_source", "Phi_source", "domain_transport_source")
        if missing_text(row.get(field))
    ]
    if not numeric_missing and not source_missing:
        raw_lock = abs((values["delta_JC_integral"] or 0.0) - (values["target_volume_lock"] or 0.0))
        source_flux_bound = (
            abs(values["source_term_integral_abs"] or 0.0)
            + abs(values["boundary_flux_abs"] or 0.0)
            + abs(values["moving_boundary_abs"] or 0.0)
            + abs(values["normalization_drift_abs"] or 0.0)
        )
        unclosed = max(0.0, raw_lock - source_flux_bound)
        flrw_compatible = bool_text(row.get("FLRW_active_class_preserved_signed"))
        if unclosed <= 1.0e-15 and source_flux_bound > 0.0:
            status = "VOLUME_BALANCE_FINITE_SOURCE_FLUX_ENVELOPE_NONCLAIM"
        elif raw_lock <= 1.0e-15:
            status = "VOLUME_LOCK_NUMERIC_ZERO_BUT_PARENT_UNSIGNED_NONCLAIM"
        else:
            status = "VOLUME_LOCK_RESIDUAL_COMPUTED_PARENT_SELECTOR_OPEN_NONCLAIM"
        output.update(
            {
                "Z_parent_continuity": False,
                "Z_local_lock": raw_lock <= 1.0e-15,
                "Z_FLRW_compatible": flrw_compatible,
                "raw_volume_lock_abs": format_float(raw_lock),
                "source_flux_bound_abs": format_float(source_flux_bound),
                "unclosed_volume_lock_abs": format_float(unclosed),
                "missing_volume_lock_inputs": ";".join(f"MISSING_{clause}" for clause in missing),
                "runner_status": status,
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    output.update(
        {
            "Z_parent_continuity": False,
            "Z_local_lock": False,
            "Z_FLRW_compatible": bool_text(row.get("FLRW_active_class_preserved_signed")),
            "raw_volume_lock_abs": "MISSING_NUMERIC_VALUE",
            "source_flux_bound_abs": "MISSING_NUMERIC_VALUE",
            "unclosed_volume_lock_abs": "MISSING_NUMERIC_VALUE",
            "missing_volume_lock_inputs": ";".join(
                [
                    *(f"MISSING_{clause}" for clause in missing),
                    *(f"MISSING_{field}" for field in numeric_missing),
                    *(f"MISSING_{field}" for field in source_missing),
                ]
            ),
            "runner_status": "BLOCKED_MISSING_PARENT_VOLUME_LOCK_OR_BALANCE_INPUTS",
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def edge_bound_row(row: dict[str, Any]) -> dict[str, Any]:
    edge_id = str(row.get("edge_id", "")).strip() or "UNNAMED_EDGE"
    output: dict[str, Any] = {
        "edge_id": edge_id,
        "row_status_input": row.get("row_status", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "Q_edge_bound_abs": "MISSING_NUMERIC_VALUE",
                "dSFeps_term_abs": "MISSING_NUMERIC_VALUE",
                "missing_edge_inputs": "FORBIDDEN_EDGE_CANCELLATION_OR_POSTFIT_SOURCE",
                "runner_status": "FAILED_FINITE_EDGE_BOUND_GATE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    missing = missing_clauses(row, EDGE_BOUND_CLAUSES)
    if not missing:
        output.update(
            {
                "Q_edge_bound_abs": "0.000000000000000e+00",
                "dSFeps_term_abs": "0.000000000000000e+00",
                "missing_edge_inputs": "",
                "runner_status": "EDGE_ZERO_CERTIFIED_CONDITIONAL_THEOREM_NONCLAIM",
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    values = {
        "C_corner_abs": parse_float(row.get("C_corner_abs")),
        "norm_dS_Feps": parse_float(row.get("norm_dS_Feps")),
        "norm_bC": parse_float(row.get("norm_bC")),
        "harmonic_edge_abs": parse_float(row.get("harmonic_edge_abs")),
        "residual_edge_abs": parse_float(row.get("residual_edge_abs")),
        "cocycle_abs": parse_float(row.get("cocycle_abs")),
        "projector_tail_abs": parse_float(row.get("projector_tail_abs")),
    }
    numeric_missing = [field for field, value in values.items() if value is None or value < 0.0]
    source_missing = [
        field
        for field in ("edge_source", "corner_source", "dSFeps_source", "bC_source", "harmonic_source", "residual_source", "units_source")
        if missing_text(row.get(field))
    ]
    if not numeric_missing and not source_missing:
        dsfeps_term = (values["norm_dS_Feps"] or 0.0) * (values["norm_bC"] or 0.0)
        q_edge_bound = (
            (values["C_corner_abs"] or 0.0)
            + dsfeps_term
            + (values["harmonic_edge_abs"] or 0.0)
            + (values["residual_edge_abs"] or 0.0)
            + (values["cocycle_abs"] or 0.0)
            + (values["projector_tail_abs"] or 0.0)
        )
        status = "EDGE_BOUND_FINITE_TERMWISE_NONCLAIM"
        if q_edge_bound <= 1.0e-15:
            status = "EDGE_BOUND_NUMERIC_ZERO_BUT_CERTIFICATE_UNSIGNED_NONCLAIM"
        output.update(
            {
                "Q_edge_bound_abs": format_float(q_edge_bound),
                "dSFeps_term_abs": format_float(dsfeps_term),
                "missing_edge_inputs": ";".join(f"MISSING_{clause}" for clause in missing),
                "runner_status": status,
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    output.update(
        {
            "Q_edge_bound_abs": "MISSING_NUMERIC_VALUE",
            "dSFeps_term_abs": "MISSING_NUMERIC_VALUE",
            "missing_edge_inputs": ";".join(
                [
                    *(f"MISSING_{clause}" for clause in missing),
                    *(f"MISSING_{field}" for field in numeric_missing),
                    *(f"MISSING_{field}" for field in source_missing),
                ]
            ),
            "runner_status": "BLOCKED_MISSING_FINITE_EDGE_BOUND_INPUTS",
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def read_csv(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"input CSV has no rows: {path}")
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for field in row:
            if field not in fieldnames:
                fieldnames.append(field)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def run(volume_input: Path, volume_output: Path, edge_input: Path, edge_output: Path) -> None:
    write_csv(volume_output, [volume_lock_row(row) for row in read_csv(volume_input)])
    write_csv(edge_output, [edge_bound_row(row) for row in read_csv(edge_input)])


def main(argv: list[str]) -> int:
    if len(argv) != 5:
        print(
            "usage: volume_lock_edge_bound_gate_runner.py VOLUME_INPUT.csv VOLUME_OUTPUT.csv EDGE_INPUT.csv EDGE_OUTPUT.csv",
            file=sys.stderr,
        )
        return 2
    run(Path(argv[1]), Path(argv[2]), Path(argv[3]), Path(argv[4]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
