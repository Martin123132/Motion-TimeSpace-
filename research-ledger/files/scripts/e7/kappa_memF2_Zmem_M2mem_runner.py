from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


ZERO_FIELDS = (
    "typed_domain_zero",
    "fixed_branch_zero",
    "branch_extremum_zero",
    "symmetry_zero",
)

ZERO_CLAUSES = (
    "same_branch_signed",
    "readout_radiative_closure_signed",
    "parent_object_language_signed",
)

AMPLITUDE_FIELDS = (
    "Z_mem_min",
    "M2_mem_min",
    "rho_mem_norm",
    "q_boundary_mem_norm",
    "C_omega",
)

CHAIN_FIELDS = (
    "kappa_memF2_abs",
    "Z_Q_eff_min",
    "K_qbar_EM_abs",
)

FORBIDDEN_SOURCE_TOKENS = (
    "ALPHA_OBS_AS_DERIVATION",
    "BOUND_AS_SOURCE",
    "CALIBRATION_AS_DERIVATION",
    "CANCEL_UNKNOWN_COMPONENTS",
    "FIT_TO_BOUND",
    "GR_IMPORT",
    "MEASURED_G_ABSORPTION",
    "ORBITAL_GM_AS_SOURCE",
    "POYNTING_DOUBLE_COUNT",
    "STANDARD_BRANCH_AS_GLOBAL",
    "WEP_ONLY_AS_ZERO",
)


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y", "pass", "signed", "derived_zero"}


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


def source_ok(row: dict[str, Any]) -> bool:
    text = str(row.get("source_path", "")).strip()
    return bool(text) and not missing_text(text) and Path(text).exists()


def common_missing(row: dict[str, Any]) -> list[str]:
    missing = []
    if not source_ok(row):
        missing.append("MISSING_source_path")
    for flag in ("source_signed", "units_signed", "same_branch_signed"):
        if not bool_text(row.get(flag)):
            missing.append(f"MISSING_{flag}")
    return missing


def amplitude_bound(row: dict[str, Any]) -> tuple[float | None, float | None, list[str]]:
    missing = common_missing(row)
    values: dict[str, float] = {}
    for field in AMPLITUDE_FIELDS:
        value = parse_float(row.get(field))
        if value is None:
            missing.append(f"MISSING_{field}")
        elif value < 0.0:
            missing.append(f"NEGATIVE_{field}")
        else:
            values[field] = value
    if "Z_mem_min" in values and values["Z_mem_min"] <= 0.0:
        missing.append("NONPOSITIVE_Z_mem_min")
    if "M2_mem_min" in values and values["M2_mem_min"] <= 0.0:
        missing.append("NONPOSITIVE_M2_mem_min")
    lambda_mem = None
    delta_bound = None
    if not missing:
        lambda_mem = math.sqrt(values["Z_mem_min"] / values["M2_mem_min"])
        coercive_floor = min(values["Z_mem_min"], values["M2_mem_min"])
        delta_bound = values["C_omega"] * (
            values["rho_mem_norm"] + values["q_boundary_mem_norm"]
        ) / coercive_floor
    return lambda_mem, delta_bound, list(dict.fromkeys(missing))


def evaluate_kappa_zero(row: dict[str, Any]) -> dict[str, Any]:
    missing = []
    if not source_ok(row):
        missing.append("MISSING_source_path")
    if not any(bool_text(row.get(field)) for field in ZERO_FIELDS):
        missing.append("MISSING_zero_route")
    for clause in ZERO_CLAUSES:
        if not bool_text(row.get(clause)):
            missing.append(f"MISSING_{clause}")
    passed = not missing
    return {
        "lambda_mem": "NOT_APPLICABLE_ZERO_ROUTE",
        "Delta_v_m_mem_bound_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "C_memory_F2_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "qbar_EM_memory_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "route_pass": passed,
        "runner_status": "KAPPA_MEMF2_ZERO_PASS_NONCLAIM" if passed else "BLOCKED_KAPPA_MEMF2_ZERO_CLAUSES",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_memory_amplitude(row: dict[str, Any]) -> dict[str, Any]:
    lambda_mem, delta_bound, missing = amplitude_bound(row)
    passed = not missing
    return {
        "lambda_mem": fmt(lambda_mem),
        "Delta_v_m_mem_bound_abs": fmt(delta_bound),
        "C_memory_F2_abs": "MISSING_NUMERIC_VALUE",
        "qbar_EM_memory_abs": "MISSING_NUMERIC_VALUE",
        "route_pass": passed,
        "runner_status": "ZMEM_M2MEM_AMPLITUDE_BOUND_PASS_NONCLAIM" if passed else "BLOCKED_ZMEM_M2MEM_AMPLITUDE_INPUTS",
        "missing_for_claim": "" if passed else ";".join(missing),
    }


def evaluate_finite_chain(row: dict[str, Any]) -> dict[str, Any]:
    lambda_mem, delta_bound, missing = amplitude_bound(row)
    values: dict[str, float] = {}
    for field in CHAIN_FIELDS:
        value = parse_float(row.get(field))
        if value is None:
            missing.append(f"MISSING_{field}")
        elif value < 0.0:
            missing.append(f"NEGATIVE_{field}")
        else:
            values[field] = value
    if "Z_Q_eff_min" in values and values["Z_Q_eff_min"] <= 0.0:
        missing.append("NONPOSITIVE_Z_Q_eff_min")
    C_memory = None
    qbar = None
    if not missing and delta_bound is not None:
        C_memory = values["kappa_memF2_abs"] * delta_bound / values["Z_Q_eff_min"]
        qbar = values["K_qbar_EM_abs"] * C_memory
    passed = not missing
    return {
        "lambda_mem": fmt(lambda_mem),
        "Delta_v_m_mem_bound_abs": fmt(delta_bound),
        "C_memory_F2_abs": fmt(C_memory),
        "qbar_EM_memory_abs": fmt(qbar),
        "route_pass": passed,
        "runner_status": "KAPPA_ZMEM_M2MEM_FINITE_CHAIN_PASS_NONCLAIM" if passed else "BLOCKED_KAPPA_ZMEM_M2MEM_FINITE_CHAIN_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_row(row: dict[str, Any]) -> dict[str, Any]:
    row_id = str(row.get("row_id", "")).strip() or "UNNAMED_KAPPA_ZMEM_ROW"
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
                "lambda_mem": "MISSING_NUMERIC_VALUE",
                "Delta_v_m_mem_bound_abs": "MISSING_NUMERIC_VALUE",
                "C_memory_F2_abs": "MISSING_NUMERIC_VALUE",
                "qbar_EM_memory_abs": "MISSING_NUMERIC_VALUE",
                "route_pass": False,
                "runner_status": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
                "missing_for_claim": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    if route_type == "kappa_zero":
        result = evaluate_kappa_zero(row)
    elif route_type == "memory_amplitude_bound":
        result = evaluate_memory_amplitude(row)
    elif route_type == "finite_chain":
        result = evaluate_finite_chain(row)
    else:
        result = {
            "lambda_mem": "MISSING_NUMERIC_VALUE",
            "Delta_v_m_mem_bound_abs": "MISSING_NUMERIC_VALUE",
            "C_memory_F2_abs": "MISSING_NUMERIC_VALUE",
            "qbar_EM_memory_abs": "MISSING_NUMERIC_VALUE",
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
        print("Usage: kappa_memF2_Zmem_M2mem_runner.py INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    write_csv(Path(sys.argv[2]), [evaluate_row(row) for row in read_csv(Path(sys.argv[1]))])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
