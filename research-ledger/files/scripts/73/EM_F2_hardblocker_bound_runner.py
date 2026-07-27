from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


IMAGE_ZERO_CLAUSES = (
    "parent_image_signed",
    "no_hidden_hom_signed",
    "fixed_representation_signed",
    "same_current_signed",
    "readout_radiative_closure_signed",
    "boundary_flux_signed",
)

FINITE_FIELDS = (
    "H_XF2_abs",
    "z_g_abs",
    "delta_lambda_rad_abs",
    "delta_lambda_readout_abs",
    "C_JQ_abs",
    "C_Hodge_readout_abs",
    "Phi_EM_rad_abs",
    "K_qbar_EM_abs",
)

POYNTING_CLAUSES = (
    "same_visible_action_signed",
    "hilbert_stress_owned",
    "poynting_once_signed",
    "closed_collar_or_flux_bound_signed",
)

FORBIDDEN_SOURCE_TOKENS = (
    "ALPHA_OBS_AS_ZERO",
    "BOUND_AS_SOURCE",
    "CALIBRATION_AS_DERIVATION",
    "CANCEL_UNKNOWN_COMPONENTS",
    "FIT_TO_BOUND",
    "GR_IMPORT",
    "MEASURED_G_ABSORPTION",
    "ORBITAL_GM_AS_SOURCE",
    "POYNTING_DOUBLE_COUNT",
    "WEP_ONLY_AS_ZERO",
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


def fmt(value: float | None) -> str:
    if value is None or not math.isfinite(value):
        return "MISSING_NUMERIC_VALUE"
    return f"{value:.15e}"


def forbidden_source_used(row: dict[str, Any]) -> bool:
    text = " ".join(
        str(row.get(field, ""))
        for field in ("row_id", "route_type", "source_path", "equation_ref", "notes", "provenance")
    ).upper()
    return any(token in text for token in FORBIDDEN_SOURCE_TOKENS)


def evaluate_image_zero(row: dict[str, Any]) -> dict[str, Any]:
    missing = [f"MISSING_{clause}" for clause in IMAGE_ZERO_CLAUSES if not bool_text(row.get(clause))]
    passed = not missing
    return {
        "lambdaF2_bound_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "b_alpha_bound_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "qbar_EM_bound_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "poynting_extra_abs": "MISSING_NUMERIC_VALUE",
        "route_pass": passed,
        "runner_status": "EM_F2_IMAGE_ZERO_PASS_NONCLAIM" if passed else "BLOCKED_EM_F2_IMAGE_ZERO_CLAUSES",
        "missing_for_claim": "" if passed else ";".join(missing),
    }


def evaluate_finite_bound(row: dict[str, Any]) -> dict[str, Any]:
    missing: list[str] = []
    values: dict[str, float] = {}
    for field in FINITE_FIELDS:
        value = parse_float(row.get(field))
        if value is None or value < 0.0:
            missing.append(f"MISSING_{field}")
        else:
            values[field] = value
    for flag in ("source_signed", "units_signed", "same_branch_signed"):
        if not bool_text(row.get(flag)):
            missing.append(f"MISSING_{flag}")
    lambda_bound = None
    b_alpha_bound = None
    qbar_em_bound = None
    if not missing:
        lambda_bound = values["H_XF2_abs"] + values["delta_lambda_rad_abs"] + values["delta_lambda_readout_abs"]
        b_alpha_bound = 2.0 * values["z_g_abs"] + lambda_bound
        qbar_em_bound = values["K_qbar_EM_abs"] * (
            b_alpha_bound + values["C_JQ_abs"] + values["C_Hodge_readout_abs"] + values["Phi_EM_rad_abs"]
        )
    passed = not missing
    return {
        "lambdaF2_bound_abs": fmt(lambda_bound),
        "b_alpha_bound_abs": fmt(b_alpha_bound),
        "qbar_EM_bound_abs": fmt(qbar_em_bound),
        "poynting_extra_abs": "MISSING_NUMERIC_VALUE",
        "route_pass": passed,
        "runner_status": "EM_F2_FINITE_BOUND_PASS_NONCLAIM" if passed else "BLOCKED_EM_F2_FINITE_BOUND_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_poynting_once(row: dict[str, Any]) -> dict[str, Any]:
    missing = [f"MISSING_{clause}" for clause in POYNTING_CLAUSES if not bool_text(row.get(clause))]
    passed = not missing
    return {
        "lambdaF2_bound_abs": "MISSING_NUMERIC_VALUE",
        "b_alpha_bound_abs": "MISSING_NUMERIC_VALUE",
        "qbar_EM_bound_abs": "MISSING_NUMERIC_VALUE",
        "poynting_extra_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "route_pass": passed,
        "runner_status": "POYNTING_ONCE_PASS_NONCLAIM" if passed else "BLOCKED_POYNTING_ONCE_CLAUSES",
        "missing_for_claim": "" if passed else ";".join(missing),
    }


def evaluate_row(row: dict[str, Any]) -> dict[str, Any]:
    row_id = str(row.get("row_id", "")).strip() or "UNNAMED_EMF2_ROW"
    route_type = str(row.get("route_type", "")).strip()
    output: dict[str, Any] = {
        "row_id": row_id,
        "route_type": route_type,
        "route": row.get("route", ""),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "lambdaF2_bound_abs": "MISSING_NUMERIC_VALUE",
                "b_alpha_bound_abs": "MISSING_NUMERIC_VALUE",
                "qbar_EM_bound_abs": "MISSING_NUMERIC_VALUE",
                "poynting_extra_abs": "MISSING_NUMERIC_VALUE",
                "route_pass": False,
                "runner_status": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
                "missing_for_claim": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    if missing_text(row.get("source_path")):
        result = {
            "lambdaF2_bound_abs": "MISSING_NUMERIC_VALUE",
            "b_alpha_bound_abs": "MISSING_NUMERIC_VALUE",
            "qbar_EM_bound_abs": "MISSING_NUMERIC_VALUE",
            "poynting_extra_abs": "MISSING_NUMERIC_VALUE",
            "route_pass": False,
            "runner_status": "BLOCKED_MISSING_SOURCE_PATH",
            "missing_for_claim": "MISSING_SOURCE_PATH",
        }
    elif route_type == "image_zero":
        result = evaluate_image_zero(row)
    elif route_type == "finite_bound":
        result = evaluate_finite_bound(row)
    elif route_type == "poynting_once":
        result = evaluate_poynting_once(row)
    else:
        result = {
            "lambdaF2_bound_abs": "MISSING_NUMERIC_VALUE",
            "b_alpha_bound_abs": "MISSING_NUMERIC_VALUE",
            "qbar_EM_bound_abs": "MISSING_NUMERIC_VALUE",
            "poynting_extra_abs": "MISSING_NUMERIC_VALUE",
            "route_pass": False,
            "runner_status": "FAILED_UNKNOWN_ROUTE_TYPE",
            "missing_for_claim": "UNKNOWN_ROUTE_TYPE",
        }
    output.update(result)
    output["anti_circularity_status"] = "PASS_NO_FORBIDDEN_SOURCE_USED"
    return output


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(dict.fromkeys(field for row in rows for field in row))
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: EM_F2_hardblocker_bound_runner.py INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    write_csv(Path(sys.argv[2]), [evaluate_row(row) for row in read_csv(Path(sys.argv[1]))])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
