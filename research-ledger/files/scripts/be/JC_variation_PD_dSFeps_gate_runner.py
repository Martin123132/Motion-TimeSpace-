from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


JC_VARIATION_CLAUSES = (
    "JC_definition_from_Q_signed",
    "detQ_variation_identity_signed",
    "coframe_volume_variation_rule_signed",
    "normalization_ND_variation_rule_signed",
    "domain_variation_or_fixed_domain_signed",
    "top_form_closedness_signed",
    "parent_action_density_signed",
    "constraint_multiplier_owned",
    "PD_owner_connected_to_domain_signed",
    "drel_source_terms_signed",
    "volume_lock_selector_signed",
    "FLRW_active_class_preserved_signed",
    "matter_selector_same_domain_signed",
    "no_action_by_declaration_signed",
)

PD_OWNER_CLAUSES = (
    "PD_domain_representative_signed",
    "PD_idempotence_signed",
    "deltaPD_variation_signed",
    "PD_metric_dependency_accounted",
    "PD_stress_tensor_accounted",
    "PD_drel_commutator_signed",
    "PD_boundary_class_preserved",
    "PD_no_postfit_domain_signed",
    "PD_no_label_only_signed",
)

DSFEPS_ZERO_CLAUSES = (
    "surface_S_signed",
    "F_lambda_defined_on_S",
    "epsilon_X_allowed_generator_signed",
    "dS_operator_signed",
    "dS_Fepsilon_zero_signed",
    "no_physical_charge_erased_signed",
    "boundary_class_fixed_signed",
    "no_dSFeps_zero_by_assertion_signed",
)

FORBIDDEN_SOURCE_TOKENS = (
    "ACTION_BY_DECLARATION",
    "PD_BY_LABEL",
    "PD_BY_DECLARATION",
    "DREL_BY_DECLARATION",
    "VOLUME_LOCK_BY_ASSERTION",
    "LOCAL_FLRW_HAND_SWITCH",
    "DSFEPS_ZERO_BY_ASSERTION",
    "PROPER_GAUGE_ERASES_PHYSICAL_CHARGE",
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
            "JC_source",
            "variation_source",
            "PD_source",
            "drel_source",
            "volume_lock_source",
            "surface_source",
            "epsilon_source",
            "bound_source",
            "zero_theorem_path",
            "provenance",
            "notes",
        )
    ).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_clauses(row: dict[str, Any], clauses: tuple[str, ...]) -> list[str]:
    return [clause for clause in clauses if not bool_text(row.get(clause))]


def jc_variation_row(row: dict[str, Any]) -> dict[str, Any]:
    variation_id = str(row.get("variation_id", "")).strip() or "UNNAMED_VARIATION"
    output: dict[str, Any] = {
        "variation_id": variation_id,
        "row_status_input": row.get("row_status", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "delta_JC_density": "MISSING_NUMERIC_VALUE",
                "delta_JC_integral": "MISSING_NUMERIC_VALUE",
                "volume_lock_abs": "MISSING_NUMERIC_VALUE",
                "missing_variation_inputs": "FORBIDDEN_ACTION_VOLUME_LOCK_OR_POSTFIT_SOURCE",
                "runner_status": "FAILED_JC_VARIATION_GATE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    missing = missing_clauses(row, JC_VARIATION_CLAUSES)
    if not missing:
        output.update(
            {
                "delta_JC_density": "0.000000000000000e+00",
                "delta_JC_integral": "0.000000000000000e+00",
                "volume_lock_abs": "0.000000000000000e+00",
                "missing_variation_inputs": "",
                "runner_status": "JC_VARIATION_VOLUME_LOCK_CONDITIONAL_PARENT_THEOREM_NONCLAIM",
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    values = {
        "JC_density": parse_float(row.get("JC_density")),
        "trace_Qinv_dQ": parse_float(row.get("trace_Qinv_dQ")),
        "delta_log_omega0": parse_float(row.get("delta_log_omega0")),
        "delta_log_ND": parse_float(row.get("delta_log_ND")),
        "domain_boundary_flux_density": parse_float(row.get("domain_boundary_flux_density")),
        "domain_volume": parse_float(row.get("domain_volume")),
        "target_volume_lock": parse_float(row.get("target_volume_lock")),
    }
    numeric_missing = [field for field, value in values.items() if value is None]
    source_missing = [
        field
        for field in ("JC_source", "variation_source")
        if missing_text(row.get(field))
    ]
    if not numeric_missing and not source_missing:
        density = (values["JC_density"] or 0.0) * (
            (values["trace_Qinv_dQ"] or 0.0)
            + (values["delta_log_omega0"] or 0.0)
            - (values["delta_log_ND"] or 0.0)
        ) + (values["domain_boundary_flux_density"] or 0.0)
        integral = density * (values["domain_volume"] or 0.0)
        lock_abs = abs(integral - (values["target_volume_lock"] or 0.0))
        status = "JC_VARIATION_COMPUTED_VOLUME_LOCK_OPEN_NONCLAIM"
        if lock_abs == 0.0:
            status = "JC_VARIATION_COMPUTED_VOLUME_LOCK_ZERO_NUMERIC_NONCLAIM"
        output.update(
            {
                "delta_JC_density": format_float(density),
                "delta_JC_integral": format_float(integral),
                "volume_lock_abs": format_float(lock_abs),
                "missing_variation_inputs": ";".join(f"MISSING_{clause}" for clause in missing),
                "runner_status": status,
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    output.update(
        {
            "delta_JC_density": "MISSING_NUMERIC_VALUE",
            "delta_JC_integral": "MISSING_NUMERIC_VALUE",
            "volume_lock_abs": "MISSING_NUMERIC_VALUE",
            "missing_variation_inputs": ";".join([*(f"MISSING_{clause}" for clause in missing), *(f"MISSING_{field}" for field in numeric_missing), *(f"MISSING_{field}" for field in source_missing)]),
            "runner_status": "BLOCKED_MISSING_JC_VARIATION_OR_VOLUME_LOCK_INPUTS",
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def pd_owner_row(row: dict[str, Any]) -> dict[str, Any]:
    pd_id = str(row.get("pd_id", "")).strip() or "UNNAMED_PD"
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
                "Z_PD_owner": False,
                "Z_deltaPD": False,
                "missing_PD_clauses": "FORBIDDEN_PD_LABEL_OR_POSTFIT_SOURCE",
                "runner_status": "FAILED_PD_OWNER_GATE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    missing = missing_clauses(row, PD_OWNER_CLAUSES)
    if missing:
        output.update(
            {
                "Z_PD_owner": False,
                "Z_deltaPD": False,
                "missing_PD_clauses": ";".join(missing),
                "runner_status": "PD_OWNER_PARTIAL_BLOCKED_NONCLAIM",
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    output.update(
        {
            "Z_PD_owner": True,
            "Z_deltaPD": True,
            "missing_PD_clauses": "",
            "runner_status": "PD_OWNER_VARIATION_CONDITIONAL_NONCLAIM",
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def dsfeps_row(row: dict[str, Any]) -> dict[str, Any]:
    dsfeps_id = str(row.get("dsfeps_id", "")).strip() or "UNNAMED_DSFEPS"
    output: dict[str, Any] = {
        "dsfeps_id": dsfeps_id,
        "row_status_input": row.get("row_status", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "norm_dS_Feps": "MISSING_NUMERIC_VALUE",
                "norm_bC": "MISSING_NUMERIC_VALUE",
                "dSFeps_bound_abs": "MISSING_NUMERIC_VALUE",
                "missing_dSFeps_inputs": "FORBIDDEN_DSFEPS_OR_POSTFIT_SOURCE",
                "runner_status": "FAILED_DSFEPS_GATE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    missing_zero = missing_clauses(row, DSFEPS_ZERO_CLAUSES)
    if not missing_zero:
        output.update(
            {
                "norm_dS_Feps": "0.000000000000000e+00",
                "norm_bC": format_float(parse_float(row.get("norm_bC")) or 0.0),
                "dSFeps_bound_abs": "0.000000000000000e+00",
                "missing_dSFeps_inputs": "",
                "runner_status": "DSFEPS_ZERO_CERTIFIED_CONDITIONAL_NONCLAIM",
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    norm = parse_float(row.get("norm_dS_Feps"))
    primitive = parse_float(row.get("norm_bC"))
    source_missing = [
        field
        for field in ("surface_source", "epsilon_source", "bound_source")
        if missing_text(row.get(field))
    ]
    numeric_missing = []
    if norm is None or norm < 0:
        numeric_missing.append("norm_dS_Feps")
    if primitive is None or primitive < 0:
        numeric_missing.append("norm_bC")
    if not numeric_missing and not source_missing:
        bound = (norm or 0.0) * (primitive or 0.0)
        output.update(
            {
                "norm_dS_Feps": format_float(norm),
                "norm_bC": format_float(primitive),
                "dSFeps_bound_abs": format_float(bound),
                "missing_dSFeps_inputs": ";".join(f"MISSING_{clause}" for clause in missing_zero),
                "runner_status": "DSFEPS_FINITE_BOUND_COMPUTED_NONCLAIM",
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    output.update(
        {
            "norm_dS_Feps": format_float(norm),
            "norm_bC": format_float(primitive),
            "dSFeps_bound_abs": "MISSING_NUMERIC_VALUE",
            "missing_dSFeps_inputs": ";".join([*(f"MISSING_{clause}" for clause in missing_zero), *(f"MISSING_{field}" for field in numeric_missing), *(f"MISSING_{field}" for field in source_missing)]),
            "runner_status": "BLOCKED_MISSING_DSFEPS_ZERO_OR_BOUND_INPUTS",
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


def run(
    variation_input: Path,
    variation_output: Path,
    pd_input: Path,
    pd_output: Path,
    dsfeps_input: Path,
    dsfeps_output: Path,
) -> None:
    write_csv(variation_output, [jc_variation_row(row) for row in read_csv(variation_input)])
    write_csv(pd_output, [pd_owner_row(row) for row in read_csv(pd_input)])
    write_csv(dsfeps_output, [dsfeps_row(row) for row in read_csv(dsfeps_input)])


def main(argv: list[str]) -> int:
    if len(argv) != 7:
        print(
            "usage: JC_variation_PD_dSFeps_gate_runner.py VARIATION_INPUT.csv VARIATION_OUTPUT.csv PD_INPUT.csv PD_OUTPUT.csv DSFEPS_INPUT.csv DSFEPS_OUTPUT.csv",
            file=sys.stderr,
        )
        return 2
    run(Path(argv[1]), Path(argv[2]), Path(argv[3]), Path(argv[4]), Path(argv[5]), Path(argv[6]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
