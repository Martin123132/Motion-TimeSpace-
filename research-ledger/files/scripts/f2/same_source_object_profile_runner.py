from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


OWNER_CLAUSES = (
    "parent_action_variation_signed",
    "single_observed_frame_signed",
    "quotient_matter_functor_signed",
    "source_worldtube_support_signed",
    "hilbert_current_variation_owned",
    "hamiltonian_charge_integrable",
    "M_H_ref_normalized",
    "PiM_hamiltonian_map_signed",
    "topological_PD_representative_signed",
    "same_linking_class_signed",
    "exact_Bzero_primitive_signed",
    "Bzero_flux_zero_signed",
    "no_extra_exchange_signed",
    "projector_commutator_zero_signed",
    "radial_closure_signed",
    "no_tautological_definition_signed",
    "no_postfit_readout_signed",
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
    "BOUNDARY_TUNED_TO_GM",
)

PROFILE_NUMERIC_FIELDS = (
    "PiM_JH_integral_kg",
    "JM_top_integral_kg",
    "Bzero_primitive_integral_kg",
    "Bzero_boundary_flux_abs_kg",
    "boundary_reference_shift_abs_kg",
    "collar_flux_abs_kg",
    "frame_mismatch_abs_kg",
    "extra_exchange_abs_kg",
    "projector_commutator_abs_kg",
    "radial_nonclosure_abs_kg",
    "M_H_ref_kg",
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
            "source_path",
            "owner_source",
            "profile_source",
            "zero_theorem_path",
            "provenance",
            "notes",
        )
    ).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_owner_clauses(row: dict[str, Any]) -> list[str]:
    return [clause for clause in OWNER_CLAUSES if not bool_text(row.get(clause))]


def owner_row(row: dict[str, Any]) -> dict[str, Any]:
    owner_id = str(row.get("owner_id", "")).strip() or "UNNAMED_OWNER"
    output: dict[str, Any] = {
        "owner_id": owner_id,
        "row_status_input": row.get("row_status", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "missing_owner_clauses": "FORBIDDEN_TAUTOLOGICAL_OR_POSTFIT_SOURCE",
                "R_eq_abs_kg": "MISSING_NUMERIC_VALUE",
                "B_zero_abs_kg": "MISSING_NUMERIC_VALUE",
                "runner_status": "FAILED_SAME_SOURCE_OBJECT_OWNER_GATE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    missing = missing_owner_clauses(row)
    if not missing:
        status = "SAME_SOURCE_OBJECT_OWNER_ZERO_PRIVATE_OR_CONDITIONAL_NONCLAIM"
        row_status = str(row.get("row_status", "")).lower()
        if "physical" in row_status and "conditional" not in row_status and "private" not in row_status:
            status = "SAME_SOURCE_OBJECT_OWNER_ZERO_CERTIFIED_NONCLAIM"
        output.update(
            {
                "missing_owner_clauses": "",
                "R_eq_abs_kg": "0.000000000000000e+00",
                "B_zero_abs_kg": "0.000000000000000e+00",
                "runner_status": status,
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    output.update(
        {
            "missing_owner_clauses": ";".join(missing),
            "R_eq_abs_kg": "MISSING_NUMERIC_VALUE",
            "B_zero_abs_kg": "MISSING_NUMERIC_VALUE",
            "runner_status": "SAME_SOURCE_OBJECT_OWNER_PARTIAL_BLOCKED_NONCLAIM",
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def profile_row(row: dict[str, Any]) -> dict[str, Any]:
    profile_id = str(row.get("profile_id", "")).strip() or "UNNAMED_PROFILE"
    output: dict[str, Any] = {
        "profile_id": profile_id,
        "system_id": row.get("system_id", ""),
        "branch_id": row.get("branch_id", ""),
        "row_status_input": row.get("row_status", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }

    if forbidden_source_used(row):
        output.update(
            {
                "R_eq_integral_abs_kg": "MISSING_NUMERIC_VALUE",
                "B_zero_abs_kg": "MISSING_NUMERIC_VALUE",
                "same_source_profile_bound_abs_kg": "MISSING_NUMERIC_VALUE",
                "M_H_ref_kg": format_float(parse_float(row.get("M_H_ref_kg"))),
                "epsilon_same_source_abs": "MISSING_NUMERIC_VALUE",
                "missing_inputs": "FORBIDDEN_TAUTOLOGICAL_OR_POSTFIT_SOURCE",
                "runner_status": "FAILED_CIRCULAR_SAME_SOURCE_PROFILE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    values = {field: parse_float(row.get(field)) for field in PROFILE_NUMERIC_FIELDS}
    missing = [field for field, value in values.items() if value is None]
    if missing:
        output.update(
            {
                "R_eq_integral_abs_kg": "MISSING_NUMERIC_VALUE",
                "B_zero_abs_kg": "MISSING_NUMERIC_VALUE",
                "same_source_profile_bound_abs_kg": "MISSING_NUMERIC_VALUE",
                "M_H_ref_kg": format_float(values.get("M_H_ref_kg")),
                "epsilon_same_source_abs": "MISSING_NUMERIC_VALUE",
                "missing_inputs": "MISSING_" + ";MISSING_".join(missing),
                "runner_status": "BLOCKED_MISSING_SAME_SOURCE_PROFILE_INPUTS",
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    m_href = values["M_H_ref_kg"]
    if m_href is None or m_href <= 0:
        output.update(
            {
                "R_eq_integral_abs_kg": "MISSING_NUMERIC_VALUE",
                "B_zero_abs_kg": "MISSING_NUMERIC_VALUE",
                "same_source_profile_bound_abs_kg": "MISSING_NUMERIC_VALUE",
                "M_H_ref_kg": format_float(m_href),
                "epsilon_same_source_abs": "MISSING_NUMERIC_VALUE",
                "missing_inputs": "MISSING_POSITIVE_M_H_REF_KG",
                "runner_status": "BLOCKED_NONPOSITIVE_M_H_REF",
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    req_abs = abs(values["PiM_JH_integral_kg"] - values["JM_top_integral_kg"] - values["Bzero_primitive_integral_kg"])
    bzero_abs = abs(values["Bzero_boundary_flux_abs_kg"]) + abs(values["boundary_reference_shift_abs_kg"]) + abs(values["collar_flux_abs_kg"])
    retained_abs = (
        abs(values["frame_mismatch_abs_kg"])
        + abs(values["extra_exchange_abs_kg"])
        + abs(values["projector_commutator_abs_kg"])
        + abs(values["radial_nonclosure_abs_kg"])
    )
    total = req_abs + bzero_abs + retained_abs
    epsilon = total / m_href
    status = "SAME_SOURCE_PROFILE_COMPUTED_NONCLAIM"
    if total == 0:
        status = "SAME_SOURCE_PROFILE_ZERO_PRIVATE_OR_THEOREM_NONCLAIM"

    output.update(
        {
            "R_eq_integral_abs_kg": format_float(req_abs),
            "B_zero_abs_kg": format_float(bzero_abs),
            "retained_source_object_abs_kg": format_float(retained_abs),
            "same_source_profile_bound_abs_kg": format_float(total),
            "M_H_ref_kg": format_float(m_href),
            "epsilon_same_source_abs": format_float(epsilon),
            "missing_inputs": "",
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
    fieldnames: list[str] = []
    for row in rows:
        for field in row:
            if field not in fieldnames:
                fieldnames.append(field)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def run(owner_input: Path, owner_output: Path, profile_input: Path, profile_output: Path) -> None:
    write_csv(owner_output, [owner_row(row) for row in read_csv(owner_input)])
    write_csv(profile_output, [profile_row(row) for row in read_csv(profile_input)])


def main(argv: list[str]) -> int:
    if len(argv) != 5:
        print(
            "usage: same_source_object_profile_runner.py OWNER_INPUT.csv OWNER_OUTPUT.csv PROFILE_INPUT.csv PROFILE_OUTPUT.csv",
            file=sys.stderr,
        )
        return 2
    run(Path(argv[1]), Path(argv[2]), Path(argv[3]), Path(argv[4]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
