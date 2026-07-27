from __future__ import annotations

import csv
import math
import sys
from collections.abc import Iterable
from pathlib import Path
from typing import Any


THEOREM_CLAUSES = (
    "same_parent_action_signed",
    "same_observed_frame_signed",
    "source_worldtube_fixed_signed",
    "hilbert_current_variation_owned",
    "hamiltonian_charge_normalized",
    "topological_PD_representative_signed",
    "same_linking_class_signed",
    "exact_boundary_primitive_signed",
    "boundary_flux_zero_signed",
    "no_extra_exchange_signed",
    "projector_commutator_zero_signed",
    "no_tautological_definition_signed",
    "no_readout_worldtube_signed",
)

REQ_CLAUSES = (
    "same_parent_action_signed",
    "same_observed_frame_signed",
    "source_worldtube_fixed_signed",
    "hilbert_current_variation_owned",
    "hamiltonian_charge_normalized",
    "topological_PD_representative_signed",
    "same_linking_class_signed",
    "no_extra_exchange_signed",
    "projector_commutator_zero_signed",
    "no_tautological_definition_signed",
    "no_readout_worldtube_signed",
)

BZERO_CLAUSES = (
    "same_parent_action_signed",
    "same_observed_frame_signed",
    "exact_boundary_primitive_signed",
    "boundary_flux_zero_signed",
    "no_tautological_definition_signed",
    "no_readout_worldtube_signed",
)

FORBIDDEN_SOURCE_TOKENS = (
    "ORBITAL_GM_DEFINITION",
    "GM_AS_SOURCE",
    "FITTED_ACCELERATION",
    "OBSERVED_GM_SOURCE",
    "POSTFIT_REFERENCE",
    "OBSERVED_RESIDUAL_CANCEL",
    "PPN_FIT_AS_SOURCE",
    "CLOCK_CALIBRATION_AS_SOURCE",
    "R10_BOUND_AS_SOURCE",
    "DEFINE_JM_TOP_FROM_PIM_JH",
    "TAUTOLOGICAL_JM_TOP",
)

REQ_COMPONENT_FIELDS = (
    "R_eq_integral_abs_kg",
    "link_charge_mismatch_abs_kg",
    "exterior_nonclosure_abs_kg",
    "frame_mismatch_abs_kg",
    "extra_exchange_abs_kg",
    "projector_commutator_abs_kg",
)

BZERO_COMPONENT_FIELDS = (
    "B_zero_flux_abs_kg",
    "boundary_reference_shift_abs_kg",
    "collar_flux_abs_kg",
)


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y", "pass", "signed"}


def parse_float(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.upper().startswith("MISSING") or text.upper() in {"NA", "N/A", "NONE", "NOT_COMPUTED"}:
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


def forbidden_source_used(row: dict[str, Any]) -> bool:
    source_text = " ".join(
        str(row.get(field, ""))
        for field in (
            "theorem_source",
            "bound_source",
            "source_path",
            "zero_theorem_path",
            "provenance",
            "notes",
        )
    ).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def missing(row: dict[str, Any], clauses: Iterable[str]) -> list[str]:
    return [clause for clause in clauses if not bool_text(row.get(clause))]


def theorem_row(row: dict[str, Any]) -> dict[str, Any]:
    branch_id = str(row.get("branch_id", "")).strip() or "UNNAMED_BRANCH"
    row_status = str(row.get("row_status", "")).strip()
    req_missing = missing(row, REQ_CLAUSES)
    bzero_missing = missing(row, BZERO_CLAUSES)
    all_missing = missing(row, THEOREM_CLAUSES)

    output: dict[str, Any] = {
        "branch_id": branch_id,
        "row_status_input": row_status,
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }

    if forbidden_source_used(row):
        output.update(
            {
                "R_eq_abs_kg": "MISSING_NUMERIC_VALUE",
                "B_zero_abs_kg": "MISSING_NUMERIC_VALUE",
                "req_missing_clauses": "FORBIDDEN_TAUTOLOGICAL_OR_POSTFIT_SOURCE",
                "bzero_missing_clauses": "FORBIDDEN_TAUTOLOGICAL_OR_POSTFIT_SOURCE",
                "identity_missing_clauses": "FORBIDDEN_TAUTOLOGICAL_OR_POSTFIT_SOURCE",
                "R_eq_status": "FAILED_TAUTOLOGICAL_OR_POSTFIT_SAME_CURRENT_IDENTITY",
                "B_zero_status": "FAILED_TAUTOLOGICAL_OR_POSTFIT_BOUNDARY_PRIMITIVE",
                "runner_status": "FAILED_SAME_CURRENT_IDENTITY_GATE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    req_zero = not req_missing
    bzero_zero = not bzero_missing
    identity_zero = not all_missing
    private_or_conditional = any(word in row_status.lower() for word in ("private", "conditional", "counterfactual", "smoke"))

    if identity_zero:
        status = "SAME_CURRENT_IDENTITY_ZERO_CERTIFIED_NONCLAIM"
        if private_or_conditional:
            status = "SAME_CURRENT_IDENTITY_ZERO_PRIVATE_OR_CONDITIONAL_NONCLAIM"
        output.update(
            {
                "R_eq_abs_kg": "0.000000000000000e+00",
                "B_zero_abs_kg": "0.000000000000000e+00",
                "req_missing_clauses": "",
                "bzero_missing_clauses": "",
                "identity_missing_clauses": "",
                "R_eq_status": "R_EQ_ZERO_BY_SAME_OBJECT_DERHAM_LEMMA_NONCLAIM",
                "B_zero_status": "BZERO_ZERO_BY_FIXED_EXACT_PRIMITIVE_NONCLAIM",
                "runner_status": status,
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    output.update(
        {
            "R_eq_abs_kg": "0.000000000000000e+00" if req_zero else "MISSING_NUMERIC_VALUE",
            "B_zero_abs_kg": "0.000000000000000e+00" if bzero_zero else "MISSING_NUMERIC_VALUE",
            "req_missing_clauses": ";".join(req_missing),
            "bzero_missing_clauses": ";".join(bzero_missing),
            "identity_missing_clauses": ";".join(all_missing),
            "R_eq_status": "R_EQ_ZERO_CONDITIONALLY_DERIVED_NONCLAIM" if req_zero else "BLOCKED_MISSING_REQ_SAME_CURRENT_CLAUSES",
            "B_zero_status": "BZERO_ZERO_CONDITIONALLY_DERIVED_NONCLAIM" if bzero_zero else "BLOCKED_MISSING_BZERO_BOUNDARY_CLAUSES",
            "runner_status": "SAME_CURRENT_IDENTITY_PARTIAL_BLOCKED_NONCLAIM",
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def req_bound(row: dict[str, Any]) -> tuple[float | None, str]:
    direct = parse_float(row.get("R_eq_integral_abs_kg"))
    if direct is not None:
        return abs(direct), "DIRECT_R_EQ_INTEGRAL"
    pieces = []
    missing_fields = []
    for field in REQ_COMPONENT_FIELDS[1:]:
        value = parse_float(row.get(field))
        if value is None:
            missing_fields.append(field)
        else:
            pieces.append(abs(value))
    if missing_fields:
        return None, "MISSING_" + ";MISSING_".join(missing_fields)
    return sum(pieces), "ABSOLUTE_COMPONENT_ENVELOPE"


def bzero_bound(row: dict[str, Any]) -> tuple[float | None, str]:
    direct = parse_float(row.get("B_zero_flux_abs_kg"))
    if direct is not None:
        return abs(direct), "DIRECT_B_ZERO_FLUX"
    pieces = []
    missing_fields = []
    for field in BZERO_COMPONENT_FIELDS[1:]:
        value = parse_float(row.get(field))
        if value is None:
            missing_fields.append(field)
        else:
            pieces.append(abs(value))
    if missing_fields:
        return None, "MISSING_" + ";MISSING_".join(missing_fields)
    return sum(pieces), "ABSOLUTE_BOUNDARY_ENVELOPE"


def bound_row(row: dict[str, Any]) -> dict[str, Any]:
    bound_id = str(row.get("bound_id", "")).strip() or "UNNAMED_BOUND"
    output: dict[str, Any] = {
        "bound_id": bound_id,
        "row_status_input": row.get("row_status", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }

    if forbidden_source_used(row):
        output.update(
            {
                "R_eq_abs_kg": "MISSING_NUMERIC_VALUE",
                "B_zero_abs_kg": "MISSING_NUMERIC_VALUE",
                "same_current_bound_abs_kg": "MISSING_NUMERIC_VALUE",
                "M_H_ref_kg": format_float(parse_float(row.get("M_H_ref_kg"))),
                "epsilon_same_current_abs": "MISSING_NUMERIC_VALUE",
                "R_eq_bound_mode": "FORBIDDEN_SOURCE",
                "B_zero_bound_mode": "FORBIDDEN_SOURCE",
                "missing_inputs": "FORBIDDEN_TAUTOLOGICAL_OR_POSTFIT_SOURCE",
                "runner_status": "FAILED_CIRCULAR_SAME_CURRENT_BOUND",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    req_value, req_mode = req_bound(row)
    bzero_value, bzero_mode = bzero_bound(row)
    m_href = parse_float(row.get("M_H_ref_kg"))
    missing_inputs = []
    if req_value is None:
        missing_inputs.append(req_mode)
    if bzero_value is None:
        missing_inputs.append(bzero_mode)
    if m_href is None or m_href <= 0:
        missing_inputs.append("MISSING_POSITIVE_M_H_REF_KG")

    total = None if req_value is None or bzero_value is None else req_value + bzero_value
    epsilon = None if total is None or m_href is None or m_href <= 0 else total / m_href

    if missing_inputs:
        status = "BLOCKED_MISSING_SAME_CURRENT_BOUND_INPUTS"
    elif total == 0:
        status = "SAME_CURRENT_BOUND_ZERO_PRIVATE_OR_THEOREM_NONCLAIM"
    else:
        status = "SAME_CURRENT_BOUND_COMPUTED_NONCLAIM"

    output.update(
        {
            "R_eq_abs_kg": format_float(req_value),
            "B_zero_abs_kg": format_float(bzero_value),
            "same_current_bound_abs_kg": format_float(total),
            "M_H_ref_kg": format_float(m_href),
            "epsilon_same_current_abs": format_float(epsilon),
            "R_eq_bound_mode": req_mode,
            "B_zero_bound_mode": bzero_mode,
            "missing_inputs": ";".join(missing_inputs),
            "runner_status": status,
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
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def run(theorem_input: Path, theorem_output: Path, bound_input: Path, bound_output: Path) -> None:
    theorem_outputs = [theorem_row(row) for row in read_csv(theorem_input)]
    write_csv(theorem_output, theorem_outputs)
    bound_outputs = [bound_row(row) for row in read_csv(bound_input)]
    write_csv(bound_output, bound_outputs)


def main(argv: list[str]) -> int:
    if len(argv) != 5:
        print(
            "usage: same_current_identity_gate_runner.py THEOREM_INPUT.csv THEOREM_OUTPUT.csv BOUND_INPUT.csv BOUND_OUTPUT.csv",
            file=sys.stderr,
        )
        return 2
    run(Path(argv[1]), Path(argv[2]), Path(argv[3]), Path(argv[4]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
