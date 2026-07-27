from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
RESIDUALS = ROOT / "post-checkpoint-work" / "source-intake" / "mts_residuals"
DEFAULT_INPUT = RESIDUALS / "P8_Y5_R10_799_TRANSITION_CALCULATOR_INPUT_TEMPLATE.csv"
DEFAULT_OUTPUT = RESIDUALS / "P8_Y5_R10_799_TRANSITION_CALCULATOR_SMOKE_OUTPUT.csv"

OUTPUT_FIELDS = [
    "case_id",
    "row_status",
    "numeric_ready",
    "q_gamma_quad",
    "q_mL_drift",
    "q_trace_drift",
    "q_boundary",
    "q_bmem",
    "q_total_bound",
    "epsilon_q",
    "K_trace_amp_bound",
    "epsilon_N_trace",
    "Kperp_amp_bound",
    "epsilon_N_Kperp",
    "epsilon_q_limit",
    "epsilon_N_limit",
    "passes_symbolic_gate",
    "valid_for_claim",
    "notes",
]

REQUIRED_NUMERIC_FIELDS = [
    "U_B",
    "pS",
    "pL",
    "pT",
    "pB",
    "pK",
    "L_cg",
    "L_tr",
    "L_sys",
    "K_matter_00",
    "rho",
    "F2",
    "A_S",
    "A_L",
    "A_T",
    "A_B",
    "A_K",
    "b_mem",
    "c",
    "G",
    "epsilon_q_limit",
    "epsilon_N_limit",
]


def parse_float(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.upper().startswith("MISSING") or text.upper() in {"NA", "N/A", "NONE"}:
        return None
    try:
        number = float(text)
    except ValueError:
        return None
    if not math.isfinite(number):
        return None
    return number


def evaluate_row(row: dict[str, str]) -> dict[str, Any]:
    parsed = {field: parse_float(row.get(field)) for field in REQUIRED_NUMERIC_FIELDS}
    missing = [field for field, value in parsed.items() if value is None]
    base = {
        "case_id": row.get("case_id", ""),
        "row_status": row.get("row_status", "unspecified"),
        "valid_for_claim": str(row.get("valid_for_claim", "false")).lower(),
    }
    if missing:
        return {
            **base,
            "numeric_ready": "false",
            "q_gamma_quad": "MISSING_INPUT",
            "q_mL_drift": "MISSING_INPUT",
            "q_trace_drift": "MISSING_INPUT",
            "q_boundary": "MISSING_INPUT",
            "q_bmem": "MISSING_INPUT",
            "q_total_bound": "MISSING_INPUT",
            "epsilon_q": "MISSING_INPUT",
            "K_trace_amp_bound": "MISSING_INPUT",
            "epsilon_N_trace": "MISSING_INPUT",
            "Kperp_amp_bound": "MISSING_INPUT",
            "epsilon_N_Kperp": "MISSING_INPUT",
            "epsilon_q_limit": row.get("epsilon_q_limit", "MISSING_INPUT"),
            "epsilon_N_limit": row.get("epsilon_N_limit", "MISSING_INPUT"),
            "passes_symbolic_gate": "false",
            "notes": "missing_numeric_fields:" + ";".join(missing),
        }

    values = {field: float(value) for field, value in parsed.items() if value is not None}
    U_B = values["U_B"]
    if U_B < 0:
        return {
            **base,
            "numeric_ready": "false",
            "q_gamma_quad": "INVALID_INPUT",
            "q_mL_drift": "INVALID_INPUT",
            "q_trace_drift": "INVALID_INPUT",
            "q_boundary": "INVALID_INPUT",
            "q_bmem": "INVALID_INPUT",
            "q_total_bound": "INVALID_INPUT",
            "epsilon_q": "INVALID_INPUT",
            "K_trace_amp_bound": "INVALID_INPUT",
            "epsilon_N_trace": "INVALID_INPUT",
            "Kperp_amp_bound": "INVALID_INPUT",
            "epsilon_N_Kperp": "INVALID_INPUT",
            "epsilon_q_limit": values["epsilon_q_limit"],
            "epsilon_N_limit": values["epsilon_N_limit"],
            "passes_symbolic_gate": "false",
            "notes": "U_B must be non-negative",
        }

    L_cg = values["L_cg"]
    L_tr = values["L_tr"]
    L_sys = values["L_sys"]
    K_matter_00 = abs(values["K_matter_00"])
    rho = abs(values["rho"])
    c = values["c"]
    G = values["G"]
    if min(L_cg, L_tr, L_sys, K_matter_00, rho, c, G) <= 0:
        return {
            **base,
            "numeric_ready": "false",
            "q_gamma_quad": "INVALID_INPUT",
            "q_mL_drift": "INVALID_INPUT",
            "q_trace_drift": "INVALID_INPUT",
            "q_boundary": "INVALID_INPUT",
            "q_bmem": "INVALID_INPUT",
            "q_total_bound": "INVALID_INPUT",
            "epsilon_q": "INVALID_INPUT",
            "K_trace_amp_bound": "INVALID_INPUT",
            "epsilon_N_trace": "INVALID_INPUT",
            "Kperp_amp_bound": "INVALID_INPUT",
            "epsilon_N_Kperp": "INVALID_INPUT",
            "epsilon_q_limit": values["epsilon_q_limit"],
            "epsilon_N_limit": values["epsilon_N_limit"],
            "passes_symbolic_gate": "false",
            "notes": "length/source constants must be positive",
        }

    source_amp = abs(values["A_S"]) * U_B ** values["pS"]
    mL_amp = abs(values["A_L"]) * U_B ** values["pL"]
    trace_amp = abs(values["A_T"]) * U_B ** values["pT"]
    boundary_amp = abs(values["A_B"]) * U_B ** values["pB"]
    Kperp_amp_dimless = abs(values["A_K"]) * U_B ** values["pK"]

    q_gamma_quad = abs(values["F2"]) * source_amp**2 / (L_cg**2 * L_tr)
    q_mL_drift = mL_amp / (L_cg**2 * L_tr)
    q_trace_drift = trace_amp / L_tr
    q_boundary = boundary_amp / (L_cg**2 * L_tr)
    q_bmem = abs(values["b_mem"]) * source_amp**2 / (L_tr**3)
    q_total_bound = q_gamma_quad + q_mL_drift + q_trace_drift + q_boundary + q_bmem
    epsilon_q = L_sys * q_total_bound / K_matter_00

    K_trace_amp_bound = (
        0.5 * abs(values["F2"]) * source_amp**2 / L_cg**2
        + mL_amp / L_cg**2
        + trace_amp
        + boundary_amp / L_cg**2
    )
    denominator = 4.0 * math.pi * G * rho
    epsilon_N_trace = c**2 * K_trace_amp_bound / denominator
    Kperp_amp_bound = Kperp_amp_dimless / L_cg**2
    epsilon_N_Kperp = c**2 * Kperp_amp_bound / denominator

    passes_symbolic_gate = (
        epsilon_q <= values["epsilon_q_limit"]
        and epsilon_N_trace <= values["epsilon_N_limit"]
        and epsilon_N_Kperp <= values["epsilon_N_limit"]
        and str(row.get("valid_for_claim", "false")).lower() == "true"
    )

    return {
        **base,
        "numeric_ready": "true",
        "q_gamma_quad": f"{q_gamma_quad:.12e}",
        "q_mL_drift": f"{q_mL_drift:.12e}",
        "q_trace_drift": f"{q_trace_drift:.12e}",
        "q_boundary": f"{q_boundary:.12e}",
        "q_bmem": f"{q_bmem:.12e}",
        "q_total_bound": f"{q_total_bound:.12e}",
        "epsilon_q": f"{epsilon_q:.12e}",
        "K_trace_amp_bound": f"{K_trace_amp_bound:.12e}",
        "epsilon_N_trace": f"{epsilon_N_trace:.12e}",
        "Kperp_amp_bound": f"{Kperp_amp_bound:.12e}",
        "epsilon_N_Kperp": f"{epsilon_N_Kperp:.12e}",
        "epsilon_q_limit": f"{values['epsilon_q_limit']:.12e}",
        "epsilon_N_limit": f"{values['epsilon_N_limit']:.12e}",
        "passes_symbolic_gate": str(passes_symbolic_gate).lower(),
        "notes": "numeric_nonclaim_evaluation" if str(row.get("valid_for_claim", "false")).lower() != "true" else "claimable_only_if_sources_are_real",
    }


def evaluate_file(input_path: Path, output_path: Path) -> list[dict[str, Any]]:
    with input_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    outputs = [evaluate_row(row) for row in rows]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        for output in outputs:
            writer.writerow(output)
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate the MTS transition-current local-safety bound contract.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    outputs = evaluate_file(args.input, args.output)
    failures = [row for row in outputs if row["numeric_ready"] != "true"]
    print(f"wrote {args.output}")
    print(f"rows={len(outputs)}")
    print(f"numeric_ready={len(outputs)-len(failures)}")
    print(f"passes_symbolic_gate={sum(1 for row in outputs if row['passes_symbolic_gate'] == 'true')}")


if __name__ == "__main__":
    main()
