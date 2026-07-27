from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


COFRAME_CLAUSES = (
    "observer_coframe_defined_signed",
    "reciprocal_cell_formula_signed",
    "residual_component_decomposition_signed",
    "matter_same_coframe_signed",
    "clock_readout_map_signed",
    "R10_source_test_projection_signed",
    "orbital_residual_vector_signed",
    "beta_second_order_signed",
    "parent_BC_no_flux_or_finite_source_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

FORBIDDEN_SOURCE_TOKENS = (
    "GR_IMPORT",
    "SCHWARZSCHILD_AB_IMPORT",
    "EINSTEIN_VACUUM_IMPORT",
    "RETUNE_TO_PASS",
    "FIT_TAU_TO_BOUND",
    "OBSERVED_RESIDUAL_CANCEL",
    "TAU_BY_DECLARATION",
    "BOUND_AS_SOURCE",
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
            "mode_id",
            "source_id",
            "projection_source",
            "notes",
            "provenance",
        )
    ).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_clauses(row: dict[str, Any]) -> list[str]:
    return [clause for clause in COFRAME_CLAUSES if not bool_text(row.get(clause))]


def numeric_inputs(row: dict[str, Any]) -> tuple[dict[str, float], list[str]]:
    fields = (
        "epsilon_local_abs",
        "gamma_bound_abs",
        "beta_bound_abs",
        "clock_bound_abs",
        "R10_bound_abs",
        "orbital_bound_abs",
        "c_T",
        "c_R",
        "c_clock_readout",
        "c_alpha_clock",
        "c_mass_clock",
        "c_beta2",
        "c_source_norm",
        "K_R10",
        "q_source_R10",
        "q_test_R10",
        "c_R10_tail",
    )
    values: dict[str, float] = {}
    missing: list[str] = []
    for field in fields:
        value = parse_float(row.get(field))
        if value is None:
            missing.append(f"MISSING_{field}")
        else:
            values[field] = value
    return values, missing


def coframe_projection_row(row: dict[str, Any]) -> dict[str, Any]:
    mode_id = str(row.get("mode_id", "")).strip() or "UNNAMED_COFRAME_MODE"
    output: dict[str, Any] = {
        "mode_id": mode_id,
        "mode_type": row.get("mode_type", ""),
        "source_id": row.get("source_id", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "runner_status": "FAILED_COFRAME_TAU_PROJECTION_GATE",
                "missing_projection_inputs": "FORBIDDEN_COFRAME_TAU_SOURCE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        for field in (
            "tau_gamma_abs",
            "tau_beta_abs",
            "tau_clock_abs",
            "tau_R10_abs",
            "tau_orbital_abs",
            "pred_gamma_abs",
            "pred_beta_abs",
            "pred_clock_abs",
            "pred_R10_abs",
            "pred_orbital_abs",
        ):
            output[field] = "MISSING_NUMERIC_VALUE"
        output.update(
            {
                "gamma_pass": False,
                "beta_pass": False,
                "clock_pass": False,
                "R10_pass": False,
                "orbital_pass": False,
                "all_numeric_pass": False,
            }
        )
        return output

    missing = missing_clauses(row)
    values, numeric_missing = numeric_inputs(row)
    if numeric_missing:
        output.update(
            {
                "runner_status": "BLOCKED_MISSING_COFRAME_PROJECTION_INPUTS",
                "missing_projection_inputs": ";".join([*missing, *numeric_missing]),
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        for field in (
            "tau_gamma_abs",
            "tau_beta_abs",
            "tau_clock_abs",
            "tau_R10_abs",
            "tau_orbital_abs",
            "pred_gamma_abs",
            "pred_beta_abs",
            "pred_clock_abs",
            "pred_R10_abs",
            "pred_orbital_abs",
        ):
            output[field] = "MISSING_NUMERIC_VALUE"
        output.update(
            {
                "gamma_pass": False,
                "beta_pass": False,
                "clock_pass": False,
                "R10_pass": False,
                "orbital_pass": False,
                "all_numeric_pass": False,
            }
        )
        return output

    epsilon = abs(values["epsilon_local_abs"])
    tau_gamma = abs(values["c_T"] + values["c_R"])
    tau_beta = abs(values["c_beta2"]) + tau_gamma
    tau_clock = abs(values["c_T"] - values["c_clock_readout"]) + abs(values["c_alpha_clock"]) + abs(values["c_mass_clock"])
    tau_r10 = abs(values["K_R10"] * values["q_source_R10"] * values["q_test_R10"] + values["c_R10_tail"])
    tau_orbital = max(tau_gamma, tau_beta, abs(values["c_source_norm"]))

    pred_gamma = tau_gamma * epsilon
    pred_beta = tau_beta * epsilon
    pred_clock = tau_clock * epsilon
    pred_r10 = tau_r10 * epsilon
    pred_orbital = tau_orbital * epsilon

    gamma_pass = pred_gamma <= abs(values["gamma_bound_abs"])
    beta_pass = pred_beta <= abs(values["beta_bound_abs"])
    clock_pass = pred_clock <= abs(values["clock_bound_abs"])
    r10_pass = pred_r10 <= abs(values["R10_bound_abs"])
    orbital_pass = pred_orbital <= abs(values["orbital_bound_abs"])
    all_pass = gamma_pass and beta_pass and clock_pass and r10_pass and orbital_pass

    if epsilon <= 1.0e-30 and all_pass:
        status = "PARENT_BC_NO_FLUX_ZERO_RESIDUAL_CONDITIONAL_THEOREM_NONCLAIM"
    elif tau_gamma <= 1.0e-15 and tau_clock <= 1.0e-15 and all_pass:
        status = "RECIPROCAL_CELL_AND_CLOCK_READOUT_QUIET_PARTIAL_DERIVATION_NONCLAIM"
    elif all_pass and missing:
        status = "NUMERIC_TAU_WINDOW_PASS_BUT_PARENT_MAPPING_UNSIGNED_NONCLAIM"
    elif all_pass:
        status = "NUMERIC_TAU_WINDOW_PASS_SIGNED_MAPPING_NONCLAIM_UNLESS_INPUT_VALID"
    else:
        status = "NUMERIC_TAU_WINDOW_FAILS"

    claim_allowed = bool_text(row.get("valid_for_claim")) and not missing and all_pass
    output.update(
        {
            "tau_gamma_abs": format_float(tau_gamma),
            "tau_beta_abs": format_float(tau_beta),
            "tau_clock_abs": format_float(tau_clock),
            "tau_R10_abs": format_float(tau_r10),
            "tau_orbital_abs": format_float(tau_orbital),
            "pred_gamma_abs": format_float(pred_gamma),
            "pred_beta_abs": format_float(pred_beta),
            "pred_clock_abs": format_float(pred_clock),
            "pred_R10_abs": format_float(pred_r10),
            "pred_orbital_abs": format_float(pred_orbital),
            "gamma_pass": gamma_pass,
            "beta_pass": beta_pass,
            "clock_pass": clock_pass,
            "R10_pass": r10_pass,
            "orbital_pass": orbital_pass,
            "all_numeric_pass": all_pass,
            "runner_status": status,
            "missing_projection_inputs": ";".join(missing),
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            "claim_allowed": claim_allowed,
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


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: observer_coframe_tau_projection_runner.py <input.csv> <output.csv>", file=sys.stderr)
        return 2
    rows = [coframe_projection_row(row) for row in read_csv(Path(sys.argv[1]))]
    write_csv(Path(sys.argv[2]), rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
