from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


EXACTNESS_CLAUSES = (
    "parent_C_object_signed",
    "parent_PD_projector_signed",
    "Cperp_definition_signed",
    "form_degree_units_signed",
    "drel_complex_signed",
    "drel_closedness_signed",
    "Hrel_trivial_or_bounded_signed",
    "primitive_BC_constructed_signed",
    "boundary_pullback_decomposition_signed",
    "boundary_primitive_zero_signed",
    "edge_charge_silent_signed",
    "presymplectic_kernel_signed",
    "vX_null_generator_signed",
    "matter_descent_same_domain_signed",
    "kinetic_rank_guard_signed",
    "local_FLRW_branch_selector_signed",
    "no_Cperp_by_declaration_signed",
    "no_boundary_zero_by_assertion_signed",
)

FORBIDDEN_SOURCE_TOKENS = (
    "CPERP_BY_DECLARATION",
    "BOUNDARY_ZERO_BY_ASSERTION",
    "Q_BY_DECLARATION",
    "VERTICAL_BY_LABEL",
    "DEFINE_CPERP_AS_CG",
    "CG_BY_DEFINITION",
    "ORBITAL_GM_DEFINITION",
    "GM_AS_SOURCE",
    "FITTED_ACCELERATION",
    "OBSERVED_GM_SOURCE",
    "POSTFIT_REFERENCE",
    "OBSERVED_RESIDUAL_CANCEL",
    "PPN_FIT_AS_SOURCE",
    "CLOCK_CALIBRATION_AS_SOURCE",
    "R10_BOUND_AS_SOURCE",
)

CG_NUMERIC_FIELDS = (
    "c_g",
    "tau_R10",
    "tau_PPN_gamma",
    "tau_PPN_beta",
    "tau_clock",
    "tau_WEP",
    "tau_orbital",
    "K_X_R10",
    "Qbar_XH",
    "lambda_X_m",
    "alpha_bound_R10",
    "ppn_gamma_bound",
    "ppn_beta_bound",
    "clock_bound",
    "wep_bound",
    "orbital_bound",
)

CG_SOURCE_FIELDS = (
    "Ag_source",
    "Xhat_source",
    "cg_source",
    "projection_source",
    "bound_source",
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
            "Cperp_source",
            "drel_source",
            "boundary_source",
            "theorem_source",
            "Ag_source",
            "Xhat_source",
            "cg_source",
            "projection_source",
            "bound_source",
            "zero_theorem_path",
            "provenance",
            "notes",
        )
    ).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def exactness_missing(row: dict[str, Any]) -> list[str]:
    return [clause for clause in EXACTNESS_CLAUSES if not bool_text(row.get(clause))]


def cperp_row(row: dict[str, Any]) -> dict[str, Any]:
    cperp_id = str(row.get("cperp_id", "")).strip() or "UNNAMED_CPERP"
    output: dict[str, Any] = {
        "cperp_id": cperp_id,
        "candidate": row.get("candidate", ""),
        "row_status_input": row.get("row_status", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }

    if forbidden_source_used(row):
        output.update(
            {
                "Z_cperp_exact": False,
                "Z_boundary_silent": False,
                "Z_cg": False,
                "boundary_abs": "MISSING_NUMERIC_VALUE",
                "missing_exactness_clauses": "FORBIDDEN_CPERP_BOUNDARY_OR_POSTFIT_SOURCE",
                "runner_status": "FAILED_CPERP_EXACTNESS_GATE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    missing = exactness_missing(row)
    if missing:
        output.update(
            {
                "Z_cperp_exact": False,
                "Z_boundary_silent": bool_text(row.get("boundary_primitive_zero_signed")) and bool_text(row.get("edge_charge_silent_signed")),
                "Z_cg": False,
                "boundary_abs": "MISSING_NUMERIC_VALUE",
                "missing_exactness_clauses": ";".join(missing),
                "runner_status": "CPERP_EXACTNESS_PARTIAL_BLOCKED_NONCLAIM",
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    output.update(
        {
            "Z_cperp_exact": True,
            "Z_boundary_silent": True,
            "Z_cg": True,
            "boundary_abs": "0.000000000000000e+00",
            "missing_exactness_clauses": "",
            "runner_status": "CPERP_EXACTNESS_BOUNDARY_SILENCE_ZERO_PRIVATE_OR_CONDITIONAL_NONCLAIM",
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def unit_status(row: dict[str, Any]) -> str:
    xhat_units = str(row.get("Xhat_units", "")).strip()
    cg_units = str(row.get("c_g_units", "")).strip()
    if missing_text(xhat_units) or missing_text(cg_units):
        return "BLOCKED_MISSING_UNITS"
    if xhat_units.lower() == "dimensionless":
        return "PASS_DIMENSIONLESS_XHAT" if cg_units.lower() in {"dimensionless", "1"} else "FAIL_DIMENSIONLESS_MISMATCH"
    allowed = {f"1/{xhat_units}", f"per_{xhat_units}", f"{xhat_units}^-1"}
    return "PASS_DECLARED_UNITS" if cg_units in allowed else "PASS_DECLARED_NONSTANDARD_UNITS_NONCLAIM"


def cg_source_row(row: dict[str, Any]) -> dict[str, Any]:
    cg_id = str(row.get("cg_id", "")).strip() or "UNNAMED_CG"
    output: dict[str, Any] = {
        "cg_id": cg_id,
        "row_status_input": row.get("row_status", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }

    if forbidden_source_used(row):
        output.update(
            {
                "c_g": "MISSING_NUMERIC_VALUE",
                "alpha_R10_abs": "MISSING_NUMERIC_VALUE",
                "ppn_gamma_abs": "MISSING_NUMERIC_VALUE",
                "ppn_beta_abs": "MISSING_NUMERIC_VALUE",
                "clock_abs": "MISSING_NUMERIC_VALUE",
                "wep_abs": "MISSING_NUMERIC_VALUE",
                "orbital_abs": "MISSING_NUMERIC_VALUE",
                "all_bounds_pass": False,
                "missing_inputs": "FORBIDDEN_CG_OR_POSTFIT_SOURCE",
                "unit_status": "BLOCKED_FORBIDDEN_SOURCE",
                "runner_status": "FAILED_CIRCULAR_CG_SOURCE_PACK",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    zero_path = row.get("zero_theorem_path")
    if bool_text(row.get("Z_cg_zero_theorem_signed")):
        if missing_text(zero_path):
            output.update(
                {
                    "c_g": "MISSING_NUMERIC_VALUE",
                    "alpha_R10_abs": "MISSING_NUMERIC_VALUE",
                    "ppn_gamma_abs": "MISSING_NUMERIC_VALUE",
                    "ppn_beta_abs": "MISSING_NUMERIC_VALUE",
                    "clock_abs": "MISSING_NUMERIC_VALUE",
                    "wep_abs": "MISSING_NUMERIC_VALUE",
                    "orbital_abs": "MISSING_NUMERIC_VALUE",
                    "all_bounds_pass": False,
                    "missing_inputs": "MISSING_zero_theorem_path",
                    "unit_status": "ZERO_THEOREM_SOURCE_MISSING",
                    "runner_status": "BLOCKED_MISSING_CG_ZERO_THEOREM_SOURCE",
                    "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
                }
            )
            return output
        output.update(
            {
                "c_g": "0.000000000000000e+00",
                "alpha_R10_abs": "0.000000000000000e+00",
                "ppn_gamma_abs": "0.000000000000000e+00",
                "ppn_beta_abs": "0.000000000000000e+00",
                "clock_abs": "0.000000000000000e+00",
                "wep_abs": "0.000000000000000e+00",
                "orbital_abs": "0.000000000000000e+00",
                "all_bounds_pass": True,
                "missing_inputs": "",
                "unit_status": "ZERO_THEOREM_BRANCH",
                "runner_status": "CG_ZERO_BY_CPERP_EXACTNESS_PRIVATE_OR_CONDITIONAL_NONCLAIM",
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    values = {field: parse_float(row.get(field)) for field in CG_NUMERIC_FIELDS}
    missing = [field for field, value in values.items() if value is None]
    missing_sources = [field for field in CG_SOURCE_FIELDS if missing_text(row.get(field))]
    units = unit_status(row)
    if missing or missing_sources or units.startswith("BLOCKED") or units.startswith("FAIL"):
        output.update(
            {
                "c_g": format_float(values.get("c_g")),
                "alpha_R10_abs": "MISSING_NUMERIC_VALUE",
                "ppn_gamma_abs": "MISSING_NUMERIC_VALUE",
                "ppn_beta_abs": "MISSING_NUMERIC_VALUE",
                "clock_abs": "MISSING_NUMERIC_VALUE",
                "wep_abs": "MISSING_NUMERIC_VALUE",
                "orbital_abs": "MISSING_NUMERIC_VALUE",
                "all_bounds_pass": False,
                "missing_inputs": ";".join([*(f"MISSING_{field}" for field in missing), *(f"MISSING_{field}" for field in missing_sources)] + ([] if units.startswith("PASS") else [units])),
                "unit_status": units,
                "runner_status": "BLOCKED_MISSING_CG_SOURCE_PACK_INPUTS",
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    c_g = values["c_g"] or 0.0
    alpha = abs((values["K_X_R10"] or 0.0) * (values["Qbar_XH"] or 0.0) * (values["tau_R10"] or 0.0) * c_g)
    ppn_gamma = abs((values["tau_PPN_gamma"] or 0.0) * c_g)
    ppn_beta = abs((values["tau_PPN_beta"] or 0.0) * c_g)
    clock = abs((values["tau_clock"] or 0.0) * c_g)
    wep = abs((values["tau_WEP"] or 0.0) * c_g)
    orbital = abs((values["tau_orbital"] or 0.0) * c_g)
    comparisons = (
        alpha <= (values["alpha_bound_R10"] or -1.0),
        ppn_gamma <= (values["ppn_gamma_bound"] or -1.0),
        ppn_beta <= (values["ppn_beta_bound"] or -1.0),
        clock <= (values["clock_bound"] or -1.0),
        wep <= (values["wep_bound"] or -1.0),
        orbital <= (values["orbital_bound"] or -1.0),
    )
    output.update(
        {
            "c_g": format_float(c_g),
            "lambda_X_m": format_float(values["lambda_X_m"]),
            "alpha_R10_abs": format_float(alpha),
            "ppn_gamma_abs": format_float(ppn_gamma),
            "ppn_beta_abs": format_float(ppn_beta),
            "clock_abs": format_float(clock),
            "wep_abs": format_float(wep),
            "orbital_abs": format_float(orbital),
            "all_bounds_pass": all(comparisons),
            "missing_inputs": "",
            "unit_status": units,
            "runner_status": "CG_SOURCE_PACK_COMPUTED_NONCLAIM",
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


def run(cperp_input: Path, cperp_output: Path, cg_input: Path, cg_output: Path) -> None:
    write_csv(cperp_output, [cperp_row(row) for row in read_csv(cperp_input)])
    write_csv(cg_output, [cg_source_row(row) for row in read_csv(cg_input)])


def main(argv: list[str]) -> int:
    if len(argv) != 5:
        print(
            "usage: cperp_exactness_cg_source_pack_runner.py CPERP_INPUT.csv CPERP_OUTPUT.csv CG_INPUT.csv CG_OUTPUT.csv",
            file=sys.stderr,
        )
        return 2
    run(Path(argv[1]), Path(argv[2]), Path(argv[3]), Path(argv[4]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
