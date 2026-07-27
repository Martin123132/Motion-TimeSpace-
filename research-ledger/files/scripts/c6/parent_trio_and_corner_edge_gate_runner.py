from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


TRIO_CLAUSES = (
    "lifted_C_field_signed",
    "lifted_C_form_degree_units_signed",
    "parent_action_term_signed",
    "PD_projector_owner_signed",
    "PD_idempotence_signed",
    "PD_variation_rule_signed",
    "drel_complex_signed",
    "drel_nilpotent_signed",
    "boundary_pullback_signed",
    "closedness_identity_signed",
    "BC_primitive_or_harmonic_bound_signed",
    "local_FLRW_selector_signed",
    "matter_selector_same_domain_signed",
    "no_scalar_Cperp_promotion_signed",
    "no_projected_metric_theorem_by_closure_signed",
)

CORNER_ZERO_CLAUSES = (
    "domain_U_oriented_smooth_chain_signed",
    "boundary_S_closed_or_relative_boundary_signed",
    "partial_boundary_zero_signed",
    "no_regulator_joint_signed",
    "orientation_convention_signed",
    "corner_term_definition_signed",
    "stokes_boundary_of_boundary_signed",
    "no_corner_zero_by_assertion_signed",
)

FORBIDDEN_SOURCE_TOKENS = (
    "SCALAR_CPERP_PROMOTED",
    "PROJECTED_METRIC_BY_CLOSURE",
    "CPERP_BY_DECLARATION",
    "BOUNDARY_ZERO_BY_ASSERTION",
    "CORNER_ZERO_BY_ASSERTION",
    "REGULATOR_IGNORED",
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
            "C_source",
            "PD_source",
            "drel_source",
            "action_source",
            "domain_source",
            "corner_source",
            "bound_source",
            "zero_theorem_path",
            "provenance",
            "notes",
        )
    ).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_clauses(row: dict[str, Any], clauses: tuple[str, ...]) -> list[str]:
    return [clause for clause in clauses if not bool_text(row.get(clause))]


def trio_row(row: dict[str, Any]) -> dict[str, Any]:
    trio_id = str(row.get("trio_id", "")).strip() or "UNNAMED_TRIO"
    output: dict[str, Any] = {
        "trio_id": trio_id,
        "route": row.get("route", ""),
        "row_status_input": row.get("row_status", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }

    if forbidden_source_used(row):
        output.update(
            {
                "Z_parent_trio": False,
                "Z_lifted_route": False,
                "missing_trio_clauses": "FORBIDDEN_SCALAR_CLOSURE_OR_POSTFIT_SOURCE",
                "runner_status": "FAILED_PARENT_TRIO_GATE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    missing = missing_clauses(row, TRIO_CLAUSES)
    if missing:
        scalar_flags_ok = bool_text(row.get("no_scalar_Cperp_promotion_signed")) and bool_text(row.get("no_projected_metric_theorem_by_closure_signed"))
        output.update(
            {
                "Z_parent_trio": False,
                "Z_lifted_route": False,
                "missing_trio_clauses": ";".join(missing),
                "runner_status": "PARENT_C_PD_DREL_TRIO_PARTIAL_BLOCKED_NONCLAIM",
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED" if scalar_flags_ok else "WARN_SCALAR_CLOSURE_GUARDS_UNSIGNED",
            }
        )
        return output

    output.update(
        {
            "Z_parent_trio": True,
            "Z_lifted_route": True,
            "missing_trio_clauses": "",
            "runner_status": "PARENT_C_PD_DREL_TRIO_CONDITIONAL_SOURCE_STACK_NONCLAIM",
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def corner_row(row: dict[str, Any]) -> dict[str, Any]:
    corner_id = str(row.get("corner_id", "")).strip() or "UNNAMED_CORNER"
    output: dict[str, Any] = {
        "corner_id": corner_id,
        "row_status_input": row.get("row_status", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }

    if forbidden_source_used(row):
        output.update(
            {
                "C_corner_abs": "MISSING_NUMERIC_VALUE",
                "corner_measure": "MISSING_NUMERIC_VALUE",
                "corner_density_bound": "MISSING_NUMERIC_VALUE",
                "missing_corner_inputs": "FORBIDDEN_CORNER_OR_POSTFIT_SOURCE",
                "runner_status": "FAILED_CIRCULAR_CORNER_EDGE_GATE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    missing_zero = missing_clauses(row, CORNER_ZERO_CLAUSES)
    if not missing_zero:
        output.update(
            {
                "C_corner_abs": "0.000000000000000e+00",
                "corner_measure": "0.000000000000000e+00",
                "corner_density_bound": "0.000000000000000e+00",
                "missing_corner_inputs": "",
                "runner_status": "CCORNER_ZERO_BY_BOUNDARY_OF_BOUNDARY_THEOREM_CONDITIONAL_NONCLAIM",
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    measure = parse_float(row.get("corner_measure"))
    density = parse_float(row.get("corner_density_bound"))
    source_missing = [
        field
        for field in ("corner_source", "bound_source")
        if missing_text(row.get(field))
    ]
    if measure is not None and density is not None and measure >= 0 and density >= 0 and not source_missing:
        bound = measure * density
        output.update(
            {
                "C_corner_abs": format_float(bound),
                "corner_measure": format_float(measure),
                "corner_density_bound": format_float(density),
                "missing_corner_inputs": ";".join(f"MISSING_{clause}" for clause in missing_zero),
                "runner_status": "CCORNER_FINITE_BOUND_COMPUTED_NONCLAIM",
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    numeric_missing: list[str] = []
    if measure is None:
        numeric_missing.append("corner_measure")
    if density is None:
        numeric_missing.append("corner_density_bound")
    output.update(
        {
            "C_corner_abs": "MISSING_NUMERIC_VALUE",
            "corner_measure": format_float(measure),
            "corner_density_bound": format_float(density),
            "missing_corner_inputs": ";".join([*(f"MISSING_{clause}" for clause in missing_zero), *(f"MISSING_{field}" for field in numeric_missing), *(f"MISSING_{field}" for field in source_missing)]),
            "runner_status": "BLOCKED_MISSING_CCORNER_ZERO_OR_BOUND_INPUTS",
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


def run(trio_input: Path, trio_output: Path, corner_input: Path, corner_output: Path) -> None:
    write_csv(trio_output, [trio_row(row) for row in read_csv(trio_input)])
    write_csv(corner_output, [corner_row(row) for row in read_csv(corner_input)])


def main(argv: list[str]) -> int:
    if len(argv) != 5:
        print(
            "usage: parent_trio_and_corner_edge_gate_runner.py TRIO_INPUT.csv TRIO_OUTPUT.csv CORNER_INPUT.csv CORNER_OUTPUT.csv",
            file=sys.stderr,
        )
        return 2
    run(Path(argv[1]), Path(argv[2]), Path(argv[3]), Path(argv[4]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
