from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


CARTAN_IDENTITY_CLAUSES = (
    "spacetime_form_mathcalJ_signed",
    "tau_flow_vector_signed",
    "cartan_formula_signed",
    "source_equation_dJ_equals_Sigma_signed",
    "phi_equals_i_tau_mathcalJ_signed",
    "reynolds_transport_domain_signed",
    "normalization_ND_variation_signed",
)

CARTAN_PARENT_CLAUSES = (
    "parent_source_selector_signed",
    "local_Sigma_zero_signed",
    "local_Phi_zero_signed",
    "domain_motion_zero_signed",
    "FLRW_top_class_preserved_signed",
    "Bianchi_Ward_stress_signed",
    "no_multiplier_closure_signed",
    "no_local_FLRW_hand_switch_signed",
)

PD_IDENTITY_CLAUSES = (
    "domain_weight_WD_parent_field_signed",
    "coframe_measure_mu_signed",
    "ND_integral_definition_signed",
    "domain_average_definition_signed",
    "PD_definition_f_minus_average_signed",
    "average_variation_identity_signed",
)

PD_PARENT_CLAUSES = (
    "delta_WD_mu_stress_accounted_signed",
    "domain_boundary_motion_accounted_signed",
    "idempotence_signed",
    "drel_commutator_accounted_signed",
    "local_FLRW_domain_class_selector_signed",
    "no_external_projector_signed",
)

FORBIDDEN_SOURCE_TOKENS = (
    "CONTINUITY_BY_ASSERTION",
    "MULTIPLIER_CLOSURE_AS_PROOF",
    "VOLUME_LOCK_BY_ASSERTION",
    "LOCAL_FLRW_HAND_SWITCH",
    "SIGMA_BY_DECLARATION",
    "PHI_BY_DECLARATION",
    "PD_BY_LABEL",
    "PD_BY_DECLARATION",
    "EXTERNAL_PROJECTOR",
    "FREEZE_DOMAIN_BOUNDARY",
    "DROP_PROJECTOR_STRESS",
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
            "cartan_source",
            "mathcalJ_source",
            "Sigma_source",
            "Phi_source",
            "domain_source",
            "normalization_source",
            "stress_source",
            "PD_source",
            "WD_source",
            "measure_source",
            "variation_source",
            "drel_source",
            "provenance",
            "notes",
        )
    ).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_clauses(row: dict[str, Any], clauses: tuple[str, ...]) -> list[str]:
    return [clause for clause in clauses if not bool_text(row.get(clause))]


def cartan_balance_row(row: dict[str, Any]) -> dict[str, Any]:
    balance_id = str(row.get("balance_id", "")).strip() or "UNNAMED_CARTAN_BALANCE"
    output: dict[str, Any] = {
        "balance_id": balance_id,
        "row_status_input": row.get("row_status", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "Z_cartan_identity": False,
                "Z_parent_source": False,
                "Z_local_lock": False,
                "Z_FLRW_compatible": False,
                "predicted_delta_JC": "MISSING_NUMERIC_VALUE",
                "cartan_balance_error_abs": "MISSING_NUMERIC_VALUE",
                "local_lock_abs": "MISSING_NUMERIC_VALUE",
                "missing_cartan_inputs": "FORBIDDEN_CARTAN_OR_SOURCE_SELECTOR_SHORTCUT",
                "runner_status": "FAILED_CARTAN_BALANCE_GATE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    missing_identity = missing_clauses(row, CARTAN_IDENTITY_CLAUSES)
    missing_parent = missing_clauses(row, CARTAN_PARENT_CLAUSES)
    identity_ready = not missing_identity
    parent_ready = identity_ready and not missing_parent
    flrw_ok = bool_text(row.get("FLRW_top_class_preserved_signed")) and bool_text(row.get("no_local_FLRW_hand_switch_signed"))

    values = {
        "delta_JC_integral": parse_float(row.get("delta_JC_integral")),
        "sigma_integral": parse_float(row.get("sigma_integral")),
        "phi_boundary_integral": parse_float(row.get("phi_boundary_integral")),
        "domain_motion_integral": parse_float(row.get("domain_motion_integral")),
        "normalization_term": parse_float(row.get("normalization_term")),
    }
    numeric_missing = [field for field, value in values.items() if value is None]

    if parent_ready:
        output.update(
            {
                "Z_cartan_identity": True,
                "Z_parent_source": True,
                "Z_local_lock": True,
                "Z_FLRW_compatible": True,
                "predicted_delta_JC": "0.000000000000000e+00",
                "cartan_balance_error_abs": "0.000000000000000e+00",
                "local_lock_abs": "0.000000000000000e+00",
                "missing_cartan_inputs": "",
                "runner_status": "CARTAN_PARENT_NO_FLUX_VOLUME_LOCK_CONDITIONAL_THEOREM_NONCLAIM",
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    if identity_ready and not numeric_missing:
        predicted = (
            (values["sigma_integral"] or 0.0)
            + (values["phi_boundary_integral"] or 0.0)
            + (values["domain_motion_integral"] or 0.0)
            + (values["normalization_term"] or 0.0)
        )
        delta = values["delta_JC_integral"] or 0.0
        balance_error = abs(delta - predicted)
        local_lock_abs = abs(delta)
        status = "CARTAN_REYNOLDS_BALANCE_COMPUTED_PARENT_SOURCE_OPEN_NONCLAIM"
        if balance_error <= 1.0e-15 and local_lock_abs > 1.0e-15:
            status = "CARTAN_BALANCE_MATCHES_BUT_NOT_LOCAL_SILENCE_NONCLAIM"
        elif balance_error <= 1.0e-15 and local_lock_abs <= 1.0e-15:
            status = "CARTAN_BALANCE_NUMERIC_ZERO_PARENT_STILL_UNSIGNED_NONCLAIM"
        output.update(
            {
                "Z_cartan_identity": True,
                "Z_parent_source": False,
                "Z_local_lock": local_lock_abs <= 1.0e-15 and not missing_parent,
                "Z_FLRW_compatible": flrw_ok,
                "predicted_delta_JC": format_float(predicted),
                "cartan_balance_error_abs": format_float(balance_error),
                "local_lock_abs": format_float(local_lock_abs),
                "missing_cartan_inputs": ";".join([*(f"MISSING_{clause}" for clause in missing_parent)]),
                "runner_status": status,
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    output.update(
        {
            "Z_cartan_identity": identity_ready,
            "Z_parent_source": False,
            "Z_local_lock": False,
            "Z_FLRW_compatible": flrw_ok,
            "predicted_delta_JC": "MISSING_NUMERIC_VALUE",
            "cartan_balance_error_abs": "MISSING_NUMERIC_VALUE",
            "local_lock_abs": "MISSING_NUMERIC_VALUE",
            "missing_cartan_inputs": ";".join(
                [
                    *(f"MISSING_{clause}" for clause in missing_identity),
                    *(f"MISSING_{clause}" for clause in missing_parent),
                    *(f"MISSING_{field}" for field in numeric_missing),
                ]
            ),
            "runner_status": "BLOCKED_MISSING_CARTAN_BALANCE_OR_PARENT_SOURCE_INPUTS",
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def pd_domain_row(row: dict[str, Any]) -> dict[str, Any]:
    pd_id = str(row.get("pd_id", "")).strip() or "UNNAMED_PD_DOMAIN"
    output: dict[str, Any] = {
        "pd_id": pd_id,
        "row_status_input": row.get("row_status", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "Z_PD_average_identity": False,
                "Z_PD_parent_functional": False,
                "delta_average": "MISSING_NUMERIC_VALUE",
                "delta_PD_sample": "MISSING_NUMERIC_VALUE",
                "missing_PD_inputs": "FORBIDDEN_PD_EXTERNAL_PROJECTOR_OR_STRESS_SHORTCUT",
                "runner_status": "FAILED_PD_DOMAIN_FUNCTIONAL_GATE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    missing_identity = missing_clauses(row, PD_IDENTITY_CLAUSES)
    missing_parent = missing_clauses(row, PD_PARENT_CLAUSES)
    identity_ready = not missing_identity
    parent_ready = identity_ready and not missing_parent
    values = {
        "avg_f": parse_float(row.get("avg_f")),
        "avg_delta_f": parse_float(row.get("avg_delta_f")),
        "avg_f_delta_lnWmu": parse_float(row.get("avg_f_delta_lnWmu")),
        "avg_delta_lnWmu": parse_float(row.get("avg_delta_lnWmu")),
        "delta_f_sample": parse_float(row.get("delta_f_sample")),
    }
    numeric_missing = [field for field, value in values.items() if value is None]

    if parent_ready:
        output.update(
            {
                "Z_PD_average_identity": True,
                "Z_PD_parent_functional": True,
                "delta_average": "0.000000000000000e+00",
                "delta_PD_sample": "0.000000000000000e+00",
                "missing_PD_inputs": "",
                "runner_status": "PD_DOMAIN_FUNCTIONAL_CONDITIONAL_THEOREM_NONCLAIM",
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    if identity_ready and not numeric_missing:
        delta_average = (
            (values["avg_delta_f"] or 0.0)
            + (values["avg_f_delta_lnWmu"] or 0.0)
            - (values["avg_f"] or 0.0) * (values["avg_delta_lnWmu"] or 0.0)
        )
        delta_pd = (values["delta_f_sample"] or 0.0) - delta_average
        output.update(
            {
                "Z_PD_average_identity": True,
                "Z_PD_parent_functional": False,
                "delta_average": format_float(delta_average),
                "delta_PD_sample": format_float(delta_pd),
                "missing_PD_inputs": ";".join(f"MISSING_{clause}" for clause in missing_parent),
                "runner_status": "PD_AVERAGE_VARIATION_IDENTITY_COMPUTED_PARENT_STRESS_OPEN_NONCLAIM",
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    output.update(
        {
            "Z_PD_average_identity": identity_ready,
            "Z_PD_parent_functional": False,
            "delta_average": "MISSING_NUMERIC_VALUE",
            "delta_PD_sample": "MISSING_NUMERIC_VALUE",
            "missing_PD_inputs": ";".join(
                [
                    *(f"MISSING_{clause}" for clause in missing_identity),
                    *(f"MISSING_{clause}" for clause in missing_parent),
                    *(f"MISSING_{field}" for field in numeric_missing),
                ]
            ),
            "runner_status": "BLOCKED_MISSING_PD_DOMAIN_FUNCTIONAL_INPUTS",
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


def run(cartan_input: Path, cartan_output: Path, pd_input: Path, pd_output: Path) -> None:
    write_csv(cartan_output, [cartan_balance_row(row) for row in read_csv(cartan_input)])
    write_csv(pd_output, [pd_domain_row(row) for row in read_csv(pd_input)])


def main(argv: list[str]) -> int:
    if len(argv) != 5:
        print(
            "usage: cartan_balance_pd_domain_functional_runner.py CARTAN_INPUT.csv CARTAN_OUTPUT.csv PD_INPUT.csv PD_OUTPUT.csv",
            file=sys.stderr,
        )
        return 2
    run(Path(argv[1]), Path(argv[2]), Path(argv[3]), Path(argv[4]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
