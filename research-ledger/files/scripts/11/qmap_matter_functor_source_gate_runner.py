from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


FUNCTOR_CLAUSES = (
    "parent_q_map_signed",
    "vertical_kernel_signed",
    "observed_coframe_functor_signed",
    "matter_action_factorized",
    "constants_quotient_owned",
    "geometry_stack_descends",
    "boundary_no_tail_signed",
    "no_hidden_visible_morphism_signed",
    "radiative_readout_closure_signed",
    "source_support_functor_signed",
    "hilbert_current_from_variation_signed",
    "no_q_by_declaration_signed",
    "no_vertical_by_label_signed",
)

FORBIDDEN_SOURCE_TOKENS = (
    "Q_BY_DECLARATION",
    "VERTICAL_BY_LABEL",
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

CG_REQUIRED_NUMERIC_FIELDS = (
    "c_g",
    "tau_R10",
    "tau_PPN_gamma",
    "tau_PPN_beta",
    "tau_clock",
    "tau_WEP",
    "tau_orbital",
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
            "functor_source",
            "cg_source",
            "projection_source",
            "zero_theorem_path",
            "provenance",
            "notes",
        )
    ).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def functor_missing(row: dict[str, Any]) -> list[str]:
    return [clause for clause in FUNCTOR_CLAUSES if not bool_text(row.get(clause))]


def functor_row(row: dict[str, Any]) -> dict[str, Any]:
    functor_id = str(row.get("functor_id", "")).strip() or "UNNAMED_FUNCTOR"
    output: dict[str, Any] = {
        "functor_id": functor_id,
        "row_status_input": row.get("row_status", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }

    if forbidden_source_used(row):
        output.update(
            {
                "missing_functor_clauses": "FORBIDDEN_Q_OR_VERTICAL_DECLARATION_OR_POSTFIT_SOURCE",
                "Z_qmatter": False,
                "Z_cg": False,
                "Z_frame": False,
                "source_object_clauses_supplied": "",
                "runner_status": "FAILED_QMAP_MATTER_FUNCTOR_GATE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    missing = functor_missing(row)
    if missing:
        output.update(
            {
                "missing_functor_clauses": ";".join(missing),
                "Z_qmatter": False,
                "Z_cg": False,
                "Z_frame": False,
                "source_object_clauses_supplied": "",
                "runner_status": "QMAP_MATTER_FUNCTOR_PARTIAL_BLOCKED_NONCLAIM",
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    supplied = (
        "parent_action_variation_signed;"
        "single_observed_frame_signed;"
        "quotient_matter_functor_signed;"
        "source_worldtube_support_signed;"
        "hilbert_current_variation_owned;"
        "no_tautological_definition_signed;"
        "no_postfit_readout_signed"
    )
    output.update(
        {
            "missing_functor_clauses": "",
            "Z_qmatter": True,
            "Z_cg": True,
            "Z_frame": True,
            "source_object_clauses_supplied": supplied,
            "runner_status": "QMAP_MATTER_FUNCTOR_TO_SOURCE_OBJECT_PARTIAL_OWNER_NONCLAIM",
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def cg_row(row: dict[str, Any]) -> dict[str, Any]:
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
                "epsilon_cg_R10": "MISSING_NUMERIC_VALUE",
                "epsilon_cg_PPN_gamma": "MISSING_NUMERIC_VALUE",
                "epsilon_cg_PPN_beta": "MISSING_NUMERIC_VALUE",
                "epsilon_cg_clock": "MISSING_NUMERIC_VALUE",
                "epsilon_cg_WEP": "MISSING_NUMERIC_VALUE",
                "epsilon_cg_orbital": "MISSING_NUMERIC_VALUE",
                "epsilon_cg_total_abs": "MISSING_NUMERIC_VALUE",
                "missing_inputs": "FORBIDDEN_Q_OR_VERTICAL_DECLARATION_OR_POSTFIT_SOURCE",
                "runner_status": "FAILED_CIRCULAR_CG_FRAME_LEAK_ROW",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    if bool_text(row.get("Z_cg_zero_theorem_signed")):
        output.update(
            {
                "c_g": "0.000000000000000e+00",
                "epsilon_cg_R10": "0.000000000000000e+00",
                "epsilon_cg_PPN_gamma": "0.000000000000000e+00",
                "epsilon_cg_PPN_beta": "0.000000000000000e+00",
                "epsilon_cg_clock": "0.000000000000000e+00",
                "epsilon_cg_WEP": "0.000000000000000e+00",
                "epsilon_cg_orbital": "0.000000000000000e+00",
                "epsilon_cg_total_abs": "0.000000000000000e+00",
                "missing_inputs": "",
                "runner_status": "CG_ZERO_BY_QMATTER_FUNCTOR_PRIVATE_OR_CONDITIONAL_NONCLAIM",
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    values = {field: parse_float(row.get(field)) for field in CG_REQUIRED_NUMERIC_FIELDS}
    missing = [field for field, value in values.items() if value is None]
    source_fields = ("cg_source", "projection_source", "zero_theorem_path")
    missing_sources = [field for field in source_fields if str(row.get(field, "")).strip().upper().startswith("MISSING") or not str(row.get(field, "")).strip()]
    if missing or missing_sources:
        output.update(
            {
                "c_g": format_float(values.get("c_g")),
                "epsilon_cg_R10": "MISSING_NUMERIC_VALUE",
                "epsilon_cg_PPN_gamma": "MISSING_NUMERIC_VALUE",
                "epsilon_cg_PPN_beta": "MISSING_NUMERIC_VALUE",
                "epsilon_cg_clock": "MISSING_NUMERIC_VALUE",
                "epsilon_cg_WEP": "MISSING_NUMERIC_VALUE",
                "epsilon_cg_orbital": "MISSING_NUMERIC_VALUE",
                "epsilon_cg_total_abs": "MISSING_NUMERIC_VALUE",
                "missing_inputs": ";".join([*(f"MISSING_{field}" for field in missing), *(f"MISSING_{field}" for field in missing_sources)]),
                "runner_status": "BLOCKED_MISSING_CG_FRAME_LEAK_INPUTS",
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    c_g = values["c_g"] or 0.0
    eps_r10 = abs(c_g * (values["tau_R10"] or 0.0))
    eps_gamma = abs(c_g * (values["tau_PPN_gamma"] or 0.0))
    eps_beta = abs(c_g * (values["tau_PPN_beta"] or 0.0))
    eps_clock = abs(c_g * (values["tau_clock"] or 0.0))
    eps_wep = abs(c_g * (values["tau_WEP"] or 0.0))
    eps_orbital = abs(c_g * (values["tau_orbital"] or 0.0))
    total = eps_r10 + eps_gamma + eps_beta + eps_clock + eps_wep + eps_orbital
    output.update(
        {
            "c_g": format_float(c_g),
            "epsilon_cg_R10": format_float(eps_r10),
            "epsilon_cg_PPN_gamma": format_float(eps_gamma),
            "epsilon_cg_PPN_beta": format_float(eps_beta),
            "epsilon_cg_clock": format_float(eps_clock),
            "epsilon_cg_WEP": format_float(eps_wep),
            "epsilon_cg_orbital": format_float(eps_orbital),
            "epsilon_cg_total_abs": format_float(total),
            "missing_inputs": "",
            "runner_status": "CG_FRAME_LEAK_ROW_COMPUTED_NONCLAIM",
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


def run(functor_input: Path, functor_output: Path, cg_input: Path, cg_output: Path) -> None:
    write_csv(functor_output, [functor_row(row) for row in read_csv(functor_input)])
    write_csv(cg_output, [cg_row(row) for row in read_csv(cg_input)])


def main(argv: list[str]) -> int:
    if len(argv) != 5:
        print(
            "usage: qmap_matter_functor_source_gate_runner.py FUNCTOR_INPUT.csv FUNCTOR_OUTPUT.csv CG_INPUT.csv CG_OUTPUT.csv",
            file=sys.stderr,
        )
        return 2
    run(Path(argv[1]), Path(argv[2]), Path(argv[3]), Path(argv[4]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
