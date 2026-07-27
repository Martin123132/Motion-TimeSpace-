from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


TOPO_SELECTOR_CLAUSES = (
    "Pi_top_operator_defined_signed",
    "same_operator_local_FLRW_signed",
    "local_absolute_H3_zero_signed",
    "local_relative_boundary_zero_or_bound_signed",
    "FLRW_top_class_nonzero_allowed_signed",
    "parent_source_equals_top_projection_signed",
    "amplitude_normalization_signed",
    "no_hand_switch_signed",
)

PHIBC_CLAUSES = (
    "Phi_equals_i_tau_mathcalJ_signed",
    "JC_decomposition_dBC_plus_top_signed",
    "PhiC_BC_transport_relation_signed",
    "BC_primitive_owned_signed",
    "boundary_surface_certificate_signed",
    "no_corner_or_corner_bound_signed",
    "no_harmonic_or_harmonic_bound_signed",
    "no_residual_or_residual_bound_signed",
    "closed_weight_or_dSFeps_bound_signed",
    "charge_preservation_signed",
)

STRESS_LEDGER_CLAUSES = (
    "T_mathcalJ_accounted_signed",
    "T_Sigma_accounted_signed",
    "T_Phi_accounted_signed",
    "T_PD_accounted_signed",
    "T_domain_boundary_accounted_signed",
    "T_edge_bound_accounted_signed",
    "Ward_identity_written_signed",
    "no_hidden_external_force_signed",
)

FORBIDDEN_SOURCE_TOKENS = (
    "HAND_SWITCH",
    "LOCAL_FLRW_HAND_SWITCH",
    "SIGMA_ZERO_BY_ASSERTION",
    "PHI_ZERO_BY_ASSERTION",
    "TOP_CLASS_BY_DECLARATION",
    "BOUNDARY_ZERO_BY_ASSERTION",
    "BC_PRIMITIVE_BY_DECLARATION",
    "EDGE_CANCELLATION",
    "DROP_PROJECTOR_STRESS",
    "DROP_BOUNDARY_STRESS",
    "EXTERNAL_PROJECTOR",
    "POSTFIT_REFERENCE",
    "OBSERVED_RESIDUAL_CANCEL",
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
            "selector_source",
            "topology_source",
            "FLRW_source",
            "Phi_source",
            "BC_source",
            "boundary_source",
            "stress_source",
            "Ward_source",
            "provenance",
            "notes",
        )
    ).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_clauses(row: dict[str, Any], clauses: tuple[str, ...]) -> list[str]:
    return [clause for clause in clauses if not bool_text(row.get(clause))]


def topological_selector_row(row: dict[str, Any]) -> dict[str, Any]:
    selector_id = str(row.get("selector_id", "")).strip() or "UNNAMED_TOPO_SELECTOR"
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
                "Z_top_selector": False,
                "Z_local_top_zero": False,
                "Z_FLRW_active_allowed": False,
                "local_sigma_top_abs": "MISSING_NUMERIC_VALUE",
                "local_selector_leak_abs": "MISSING_NUMERIC_VALUE",
                "missing_selector_inputs": "FORBIDDEN_TOPO_SELECTOR_OR_HAND_SWITCH_SOURCE",
                "runner_status": "FAILED_TOPOLOGICAL_SELECTOR_GATE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    missing = missing_clauses(row, TOPO_SELECTOR_CLAUSES)
    if not missing:
        output.update(
            {
                "Z_top_selector": True,
                "Z_local_top_zero": True,
                "Z_FLRW_active_allowed": True,
                "local_sigma_top_abs": "0.000000000000000e+00",
                "local_selector_leak_abs": "0.000000000000000e+00",
                "missing_selector_inputs": "",
                "runner_status": "TOPOLOGICAL_LOCAL_ZERO_FLRW_ACTIVE_CONDITIONAL_THEOREM_NONCLAIM",
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    values = {
        "top_coupling_abs": parse_float(row.get("top_coupling_abs")),
        "local_H3_abs": parse_float(row.get("local_H3_abs")),
        "relative_boundary_leak_abs": parse_float(row.get("relative_boundary_leak_abs")),
        "FLRW_top_class_abs": parse_float(row.get("FLRW_top_class_abs")),
    }
    numeric_missing = [field for field, value in values.items() if value is None or value < 0.0]
    if not numeric_missing:
        local_sigma = (values["top_coupling_abs"] or 0.0) * (values["local_H3_abs"] or 0.0)
        leak = local_sigma + (values["relative_boundary_leak_abs"] or 0.0)
        flrw_allowed = (values["FLRW_top_class_abs"] or 0.0) > 0.0 and bool_text(row.get("same_operator_local_FLRW_signed"))
        status = "TOPOLOGICAL_SELECTOR_LOCAL_TOP_ZERO_BUT_BOUNDARY_LEAK_OPEN_NONCLAIM"
        if leak <= 1.0e-15:
            status = "TOPOLOGICAL_SELECTOR_NUMERIC_LOCAL_ZERO_PARENT_UNSIGNED_NONCLAIM"
        output.update(
            {
                "Z_top_selector": False,
                "Z_local_top_zero": local_sigma <= 1.0e-15,
                "Z_FLRW_active_allowed": flrw_allowed,
                "local_sigma_top_abs": format_float(local_sigma),
                "local_selector_leak_abs": format_float(leak),
                "missing_selector_inputs": ";".join(f"MISSING_{clause}" for clause in missing),
                "runner_status": status,
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    output.update(
        {
            "Z_top_selector": False,
            "Z_local_top_zero": False,
            "Z_FLRW_active_allowed": bool_text(row.get("FLRW_top_class_nonzero_allowed_signed")),
            "local_sigma_top_abs": "MISSING_NUMERIC_VALUE",
            "local_selector_leak_abs": "MISSING_NUMERIC_VALUE",
            "missing_selector_inputs": ";".join([*(f"MISSING_{clause}" for clause in missing), *(f"MISSING_{field}" for field in numeric_missing)]),
            "runner_status": "BLOCKED_MISSING_TOPOLOGICAL_SELECTOR_INPUTS",
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def phiBC_row(row: dict[str, Any]) -> dict[str, Any]:
    phi_id = str(row.get("phi_id", "")).strip() or "UNNAMED_PHIBC"
    output: dict[str, Any] = {
        "phi_id": phi_id,
        "row_status_input": row.get("row_status", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "Z_PhiBC_relation": False,
                "Z_boundary_silence": False,
                "Phi_boundary_bound_abs": "MISSING_NUMERIC_VALUE",
                "missing_PhiBC_inputs": "FORBIDDEN_PHIBC_BOUNDARY_OR_CANCELLATION_SOURCE",
                "runner_status": "FAILED_PHIBC_BOUNDARY_GATE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    missing = missing_clauses(row, PHIBC_CLAUSES)
    if not missing:
        output.update(
            {
                "Z_PhiBC_relation": True,
                "Z_boundary_silence": True,
                "Phi_boundary_bound_abs": "0.000000000000000e+00",
                "missing_PhiBC_inputs": "",
                "runner_status": "PHIBC_BOUNDARY_SILENCE_CONDITIONAL_THEOREM_NONCLAIM",
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
        "transport_tail_abs": parse_float(row.get("transport_tail_abs")),
    }
    numeric_missing = [field for field, value in values.items() if value is None or value < 0.0]
    if not numeric_missing:
        bound = (
            (values["C_corner_abs"] or 0.0)
            + (values["norm_dS_Feps"] or 0.0) * (values["norm_bC"] or 0.0)
            + (values["harmonic_edge_abs"] or 0.0)
            + (values["residual_edge_abs"] or 0.0)
            + (values["transport_tail_abs"] or 0.0)
        )
        relation_ok = bool_text(row.get("Phi_equals_i_tau_mathcalJ_signed")) and bool_text(row.get("JC_decomposition_dBC_plus_top_signed")) and bool_text(row.get("PhiC_BC_transport_relation_signed"))
        status = "PHIBC_BOUNDARY_FINITE_BOUND_COMPUTED_NONCLAIM"
        if bound <= 1.0e-15:
            status = "PHIBC_BOUNDARY_NUMERIC_ZERO_CERTIFICATE_UNSIGNED_NONCLAIM"
        output.update(
            {
                "Z_PhiBC_relation": relation_ok,
                "Z_boundary_silence": bound <= 1.0e-15 and not missing,
                "Phi_boundary_bound_abs": format_float(bound),
                "missing_PhiBC_inputs": ";".join(f"MISSING_{clause}" for clause in missing),
                "runner_status": status,
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    output.update(
        {
            "Z_PhiBC_relation": False,
            "Z_boundary_silence": False,
            "Phi_boundary_bound_abs": "MISSING_NUMERIC_VALUE",
            "missing_PhiBC_inputs": ";".join([*(f"MISSING_{clause}" for clause in missing), *(f"MISSING_{field}" for field in numeric_missing)]),
            "runner_status": "BLOCKED_MISSING_PHIBC_BOUNDARY_INPUTS",
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def stress_ledger_row(row: dict[str, Any]) -> dict[str, Any]:
    stress_id = str(row.get("stress_id", "")).strip() or "UNNAMED_STRESS"
    output: dict[str, Any] = {
        "stress_id": stress_id,
        "row_status_input": row.get("row_status", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "Z_stress_ledger": False,
                "unaccounted_stress_abs": "MISSING_NUMERIC_VALUE",
                "missing_stress_inputs": "FORBIDDEN_STRESS_LEDGER_SHORTCUT",
                "runner_status": "FAILED_STRESS_LEDGER_GATE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    missing = missing_clauses(row, STRESS_LEDGER_CLAUSES)
    if not missing:
        output.update(
            {
                "Z_stress_ledger": True,
                "unaccounted_stress_abs": "0.000000000000000e+00",
                "missing_stress_inputs": "",
                "runner_status": "STRESS_WARD_LEDGER_CONDITIONAL_THEOREM_NONCLAIM",
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    values = {
        "T_mathcalJ_abs": parse_float(row.get("T_mathcalJ_abs")),
        "T_Sigma_abs": parse_float(row.get("T_Sigma_abs")),
        "T_Phi_abs": parse_float(row.get("T_Phi_abs")),
        "T_PD_abs": parse_float(row.get("T_PD_abs")),
        "T_domain_boundary_abs": parse_float(row.get("T_domain_boundary_abs")),
        "T_edge_abs": parse_float(row.get("T_edge_abs")),
        "Ward_accounted_abs": parse_float(row.get("Ward_accounted_abs")),
    }
    numeric_missing = [field for field, value in values.items() if value is None or value < 0.0]
    if not numeric_missing:
        total = sum(values[field] or 0.0 for field in ("T_mathcalJ_abs", "T_Sigma_abs", "T_Phi_abs", "T_PD_abs", "T_domain_boundary_abs", "T_edge_abs"))
        unaccounted = max(0.0, total - (values["Ward_accounted_abs"] or 0.0))
        output.update(
            {
                "Z_stress_ledger": False,
                "unaccounted_stress_abs": format_float(unaccounted),
                "missing_stress_inputs": ";".join(f"MISSING_{clause}" for clause in missing),
                "runner_status": "STRESS_WARD_LEDGER_FINITE_GAP_COMPUTED_NONCLAIM",
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    output.update(
        {
            "Z_stress_ledger": False,
            "unaccounted_stress_abs": "MISSING_NUMERIC_VALUE",
            "missing_stress_inputs": ";".join([*(f"MISSING_{clause}" for clause in missing), *(f"MISSING_{field}" for field in numeric_missing)]),
            "runner_status": "BLOCKED_MISSING_STRESS_LEDGER_INPUTS",
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


def run(selector_input: Path, selector_output: Path, phibc_input: Path, phibc_output: Path, stress_input: Path, stress_output: Path) -> None:
    write_csv(selector_output, [topological_selector_row(row) for row in read_csv(selector_input)])
    write_csv(phibc_output, [phiBC_row(row) for row in read_csv(phibc_input)])
    write_csv(stress_output, [stress_ledger_row(row) for row in read_csv(stress_input)])


def main(argv: list[str]) -> int:
    if len(argv) != 7:
        print(
            "usage: local_zero_phiBC_stress_ledger_runner.py SELECTOR_IN.csv SELECTOR_OUT.csv PHIBC_IN.csv PHIBC_OUT.csv STRESS_IN.csv STRESS_OUT.csv",
            file=sys.stderr,
        )
        return 2
    run(Path(argv[1]), Path(argv[2]), Path(argv[3]), Path(argv[4]), Path(argv[5]), Path(argv[6]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
