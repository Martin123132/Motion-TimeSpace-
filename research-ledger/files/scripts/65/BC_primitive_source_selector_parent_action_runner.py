from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


BC_PRIMITIVE_CLAUSES = (
    "parent_boundary_variation_signed",
    "ThetaC_boundary_potential_signed",
    "BC_from_boundary_momentum_signed",
    "PhiC_exact_sector_transport_relation_signed",
    "boundary_counterterm_owned_signed",
    "boundary_class_fixed_signed",
    "harmonic_projection_zero_or_bound_signed",
    "residual_projection_zero_or_bound_signed",
    "closed_weight_or_kernel_bound_signed",
    "charge_preservation_signed",
    "Ward_boundary_stress_signed",
    "no_BC_by_declaration_signed",
    "no_edge_cancellation_signed",
)

SOURCE_ACTION_CLAUSES = (
    "parent_action_source_term_signed",
    "Noether_generator_liftedC_signed",
    "source_equals_Pitop_JC_signed",
    "same_operator_local_FLRW_signed",
    "local_absolute_H3_zero_signed",
    "relative_boundary_silence_or_bound_signed",
    "FLRW_top_class_amplitude_signed",
    "Ward_source_stress_signed",
    "no_source_by_declaration_signed",
    "no_local_FLRW_hand_switch_signed",
)

ROLLUP_CLAUSES = (
    "selector_bound_sourced_signed",
    "PhiBC_bound_sourced_signed",
    "stress_gap_bound_sourced_signed",
    "common_units_signed",
    "no_double_count_signed",
    "arena_projection_signed",
    "test_mapping_signed",
    "no_cancellation_signed",
)

FORBIDDEN_SOURCE_TOKENS = (
    "HAND_SWITCH",
    "LOCAL_FLRW_HAND_SWITCH",
    "SIGMA_ZERO_BY_ASSERTION",
    "PHI_ZERO_BY_ASSERTION",
    "BOUNDARY_ZERO_BY_ASSERTION",
    "BC_PRIMITIVE_BY_DECLARATION",
    "SOURCE_BY_DECLARATION",
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
            "BC_source",
            "Phi_source",
            "boundary_source",
            "source_action_path",
            "selector_source",
            "stress_source",
            "rollup_source",
            "provenance",
            "notes",
        )
    ).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_clauses(row: dict[str, Any], clauses: tuple[str, ...]) -> list[str]:
    return [clause for clause in clauses if not bool_text(row.get(clause))]


def numeric_missing(row: dict[str, Any], fields: tuple[str, ...]) -> tuple[dict[str, float], list[str]]:
    values: dict[str, float] = {}
    missing: list[str] = []
    for field in fields:
        value = parse_float(row.get(field))
        if value is None or value < 0.0:
            missing.append(field)
        else:
            values[field] = value
    return values, missing


def bc_primitive_row(row: dict[str, Any]) -> dict[str, Any]:
    bc_id = str(row.get("bc_id", "")).strip() or "UNNAMED_BC_PRIMITIVE"
    output: dict[str, Any] = {
        "bc_id": bc_id,
        "row_status_input": row.get("row_status", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "Z_BC_primitive_owner": False,
                "Z_PhiBC_parent_silence": False,
                "BC_boundary_bound_abs": "MISSING_NUMERIC_VALUE",
                "missing_BC_inputs": "FORBIDDEN_BC_PRIMITIVE_OR_BOUNDARY_SOURCE",
                "runner_status": "FAILED_BC_PRIMITIVE_GATE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    missing = missing_clauses(row, BC_PRIMITIVE_CLAUSES)
    if not missing:
        output.update(
            {
                "Z_BC_primitive_owner": True,
                "Z_PhiBC_parent_silence": True,
                "BC_boundary_bound_abs": "0.000000000000000e+00",
                "missing_BC_inputs": "",
                "runner_status": "BC_PRIMITIVE_PARENT_NO_FLUX_CONDITIONAL_THEOREM_NONCLAIM",
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    fields = (
        "C_corner_abs",
        "norm_dS_Feps",
        "norm_bC",
        "harmonic_edge_abs",
        "residual_edge_abs",
        "transport_tail_abs",
        "boundary_counterterm_tail_abs",
    )
    values, missing_numbers = numeric_missing(row, fields)
    if not missing_numbers:
        bound = (
            values["C_corner_abs"]
            + values["norm_dS_Feps"] * values["norm_bC"]
            + values["harmonic_edge_abs"]
            + values["residual_edge_abs"]
            + values["transport_tail_abs"]
            + values["boundary_counterterm_tail_abs"]
        )
        relation_ok = (
            bool_text(row.get("PhiC_exact_sector_transport_relation_signed"))
            and bool_text(row.get("no_BC_by_declaration_signed"))
            and bool_text(row.get("no_edge_cancellation_signed"))
        )
        status = "BC_PRIMITIVE_FINITE_BOUND_COMPUTED_PARENT_UNSIGNED_NONCLAIM"
        if bound <= 1.0e-15:
            status = "BC_PRIMITIVE_NUMERIC_ZERO_PARENT_UNSIGNED_NONCLAIM"
        output.update(
            {
                "Z_BC_primitive_owner": False,
                "Z_PhiBC_parent_silence": bound <= 1.0e-15 and not missing,
                "Z_PhiBC_relation": relation_ok,
                "BC_boundary_bound_abs": format_float(bound),
                "missing_BC_inputs": ";".join(f"MISSING_{clause}" for clause in missing),
                "runner_status": status,
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    output.update(
        {
            "Z_BC_primitive_owner": False,
            "Z_PhiBC_parent_silence": False,
            "Z_PhiBC_relation": bool_text(row.get("PhiC_exact_sector_transport_relation_signed")),
            "BC_boundary_bound_abs": "MISSING_NUMERIC_VALUE",
            "missing_BC_inputs": ";".join([*(f"MISSING_{clause}" for clause in missing), *(f"MISSING_{field}" for field in missing_numbers)]),
            "runner_status": "BLOCKED_MISSING_BC_PRIMITIVE_INPUTS",
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def source_action_row(row: dict[str, Any]) -> dict[str, Any]:
    source_id = str(row.get("source_action_id", "")).strip() or "UNNAMED_SOURCE_ACTION"
    output: dict[str, Any] = {
        "source_action_id": source_id,
        "row_status_input": row.get("row_status", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "Z_source_action_owner": False,
                "Z_same_selector_local_FLRW": False,
                "local_source_abs": "MISSING_NUMERIC_VALUE",
                "local_source_boundary_abs": "MISSING_NUMERIC_VALUE",
                "FLRW_source_allowed": False,
                "missing_source_action_inputs": "FORBIDDEN_SOURCE_SELECTOR_OR_HAND_SWITCH_SOURCE",
                "runner_status": "FAILED_SOURCE_ACTION_GATE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    missing = missing_clauses(row, SOURCE_ACTION_CLAUSES)
    if not missing:
        output.update(
            {
                "Z_source_action_owner": True,
                "Z_same_selector_local_FLRW": True,
                "local_source_abs": "0.000000000000000e+00",
                "local_source_boundary_abs": "0.000000000000000e+00",
                "FLRW_source_allowed": True,
                "missing_source_action_inputs": "",
                "runner_status": "SOURCE_SELECTOR_PARENT_ACTION_CONDITIONAL_THEOREM_NONCLAIM",
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    fields = (
        "kappa_top_abs",
        "local_H3_abs",
        "relative_boundary_abs",
        "FLRW_top_abs",
        "normalization_abs",
    )
    values, missing_numbers = numeric_missing(row, fields)
    if not missing_numbers:
        local_top = values["kappa_top_abs"] * values["local_H3_abs"] * values["normalization_abs"]
        local_total = local_top + values["relative_boundary_abs"]
        flrw_allowed = bool_text(row.get("same_operator_local_FLRW_signed")) and values["FLRW_top_abs"] > 0.0
        status = "SOURCE_SELECTOR_LOCAL_TOP_ZERO_BOUNDARY_OPEN_PARENT_UNSIGNED_NONCLAIM"
        if local_total <= 1.0e-15:
            status = "SOURCE_SELECTOR_NUMERIC_LOCAL_ZERO_PARENT_UNSIGNED_NONCLAIM"
        output.update(
            {
                "Z_source_action_owner": False,
                "Z_same_selector_local_FLRW": bool_text(row.get("same_operator_local_FLRW_signed")),
                "local_source_abs": format_float(local_top),
                "local_source_boundary_abs": format_float(local_total),
                "FLRW_source_allowed": flrw_allowed,
                "missing_source_action_inputs": ";".join(f"MISSING_{clause}" for clause in missing),
                "runner_status": status,
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    output.update(
        {
            "Z_source_action_owner": False,
            "Z_same_selector_local_FLRW": bool_text(row.get("same_operator_local_FLRW_signed")),
            "local_source_abs": "MISSING_NUMERIC_VALUE",
            "local_source_boundary_abs": "MISSING_NUMERIC_VALUE",
            "FLRW_source_allowed": bool_text(row.get("same_operator_local_FLRW_signed")),
            "missing_source_action_inputs": ";".join([*(f"MISSING_{clause}" for clause in missing), *(f"MISSING_{field}" for field in missing_numbers)]),
            "runner_status": "BLOCKED_MISSING_SOURCE_ACTION_INPUTS",
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def residual_rollup_row(row: dict[str, Any]) -> dict[str, Any]:
    rollup_id = str(row.get("rollup_id", "")).strip() or "UNNAMED_LOCAL_ROLLUP"
    output: dict[str, Any] = {
        "rollup_id": rollup_id,
        "row_status_input": row.get("row_status", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "Z_local_residual_sourced": False,
                "Z_local_zero_bound": False,
                "local_residual_bound_abs": "MISSING_NUMERIC_VALUE",
                "missing_rollup_inputs": "FORBIDDEN_ROLLUP_OR_CANCELLATION_SOURCE",
                "runner_status": "FAILED_LOCAL_RESIDUAL_ROLLUP_GATE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    missing = missing_clauses(row, ROLLUP_CLAUSES)
    fields = (
        "selector_leak_abs",
        "Phi_boundary_bound_abs",
        "stress_gap_abs",
        "other_projector_tail_abs",
    )
    values, missing_numbers = numeric_missing(row, fields)
    if not missing_numbers:
        total = (
            values["selector_leak_abs"]
            + values["Phi_boundary_bound_abs"]
            + values["stress_gap_abs"]
            + values["other_projector_tail_abs"]
        )
        status = "LOCAL_RESIDUAL_ROLLUP_FINITE_BOUND_COMPUTED_NONCLAIM"
        if total <= 1.0e-15:
            status = "LOCAL_RESIDUAL_ROLLUP_ZERO_CONDITIONAL_THEOREM_NONCLAIM"
        output.update(
            {
                "Z_local_residual_sourced": not missing,
                "Z_local_zero_bound": total <= 1.0e-15 and not missing,
                "selector_leak_abs": format_float(values["selector_leak_abs"]),
                "Phi_boundary_bound_abs": format_float(values["Phi_boundary_bound_abs"]),
                "stress_gap_abs": format_float(values["stress_gap_abs"]),
                "other_projector_tail_abs": format_float(values["other_projector_tail_abs"]),
                "local_residual_bound_abs": format_float(total),
                "missing_rollup_inputs": ";".join(f"MISSING_{clause}" for clause in missing),
                "runner_status": status,
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    output.update(
        {
            "Z_local_residual_sourced": False,
            "Z_local_zero_bound": False,
            "local_residual_bound_abs": "MISSING_NUMERIC_VALUE",
            "missing_rollup_inputs": ";".join([*(f"MISSING_{clause}" for clause in missing), *(f"MISSING_{field}" for field in missing_numbers)]),
            "runner_status": "BLOCKED_MISSING_LOCAL_RESIDUAL_ROLLUP_INPUTS",
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def read_csv(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def run(kind: str, input_path: Path, output_path: Path) -> None:
    functions = {
        "bc": bc_primitive_row,
        "source": source_action_row,
        "rollup": residual_rollup_row,
    }
    if kind not in functions:
        raise ValueError(f"unknown runner kind: {kind}")
    rows = [functions[kind](row) for row in read_csv(input_path)]
    write_csv(output_path, rows)


def main() -> int:
    if len(sys.argv) != 4:
        print("usage: BC_primitive_source_selector_parent_action_runner.py <bc|source|rollup> <input.csv> <output.csv>", file=sys.stderr)
        return 2
    run(sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
