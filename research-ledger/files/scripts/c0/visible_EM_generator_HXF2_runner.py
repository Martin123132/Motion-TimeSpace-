from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


EDGE_FIELDS = (
    "action_block_present",
    "observed_hodge_owned",
    "same_parent_action_line",
    "parent_owned_action_domain",
    "fixed_representation_constants",
    "no_species_source_prefactor",
    "readout_after_variation",
    "poynting_once_only",
)

SCALE_FIELDS = (
    "unique_F2_no_extra_prefactor",
    "charge_current_owner",
    "radiative_closure",
)

MEMORY_FIELDS = (
    "kappa_memF2_abs",
    "Z_Q_eff_min",
    "Delta_v_m_mem_abs",
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


def evaluate_generator(row: dict[str, Any]) -> dict[str, Any]:
    missing = []
    has_source = source_ok(row)
    if not has_source:
        missing.append("MISSING_source_path")
    edge_missing = [field for field in EDGE_FIELDS if not bool_text(row.get(field))]
    scale_missing = [field for field in SCALE_FIELDS if not bool_text(row.get(field))]
    if not bool_text(row.get("input_valid", True)):
        missing.append("MISSING_input_valid")
    edge_ready = has_source and not edge_missing
    full_ready = edge_ready and not scale_missing and not missing
    if full_ready:
        status = "VISIBLE_EM_GENERATOR_SIGNATURE_PASS_NONCLAIM"
    elif edge_ready:
        status = "VISIBLE_EM_EDGE_SIGNATURE_READY_SCALE_GATES_OPEN"
    else:
        status = "BLOCKED_VISIBLE_EM_GENERATOR_SIGNATURE"
    blockers = [f"MISSING_{field}" for field in edge_missing + scale_missing] + missing
    return {
        "edge_signature_ready": edge_ready,
        "full_generator_ready": full_ready,
        "C_memory_F2_abs": "MISSING_NUMERIC_VALUE",
        "qbar_EM_memory_abs": "MISSING_NUMERIC_VALUE",
        "route_pass": full_ready,
        "runner_status": status,
        "missing_for_claim": "" if full_ready else ";".join(dict.fromkeys(blockers)),
    }


def evaluate_memory_bound(row: dict[str, Any]) -> dict[str, Any]:
    missing = []
    values: dict[str, float] = {}
    if not source_ok(row):
        missing.append("MISSING_source_path")
    for field in MEMORY_FIELDS:
        value = parse_float(row.get(field))
        if value is None or value < 0.0:
            missing.append(f"MISSING_{field}")
        else:
            values[field] = value
    for flag in ("source_signed", "units_signed", "same_branch_signed"):
        if not bool_text(row.get(flag)):
            missing.append(f"MISSING_{flag}")
    C_memory = None
    qbar = None
    if "Z_Q_eff_min" in values and values["Z_Q_eff_min"] <= 0.0:
        missing.append("NONPOSITIVE_Z_Q_eff_min")
    if not missing:
        C_memory = values["kappa_memF2_abs"] * values["Delta_v_m_mem_abs"] / values["Z_Q_eff_min"]
        qbar = values["K_qbar_EM_abs"] * C_memory
    passed = not missing
    return {
        "edge_signature_ready": False,
        "full_generator_ready": False,
        "C_memory_F2_abs": fmt(C_memory),
        "qbar_EM_memory_abs": fmt(qbar),
        "route_pass": passed,
        "runner_status": "HXF2_MEMORY_SOURCE_BOUND_PASS_NONCLAIM" if passed else "BLOCKED_HXF2_MEMORY_SOURCE_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_memory_zero(row: dict[str, Any]) -> dict[str, Any]:
    zero_switch = any(
        bool_text(row.get(field))
        for field in (
            "typed_domain_zero",
            "fixed_branch_zero",
            "branch_extremum_zero",
            "symmetry_zero",
        )
    )
    missing = []
    if not source_ok(row):
        missing.append("MISSING_source_path")
    if not zero_switch:
        missing.append("MISSING_zero_switch")
    for flag in ("readout_radiative_closure_signed", "same_branch_signed"):
        if not bool_text(row.get(flag)):
            missing.append(f"MISSING_{flag}")
    passed = not missing
    return {
        "edge_signature_ready": False,
        "full_generator_ready": False,
        "C_memory_F2_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "qbar_EM_memory_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "route_pass": passed,
        "runner_status": "HXF2_MEMORY_ZERO_PASS_NONCLAIM" if passed else "BLOCKED_HXF2_MEMORY_ZERO_CLAUSES",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_row(row: dict[str, Any]) -> dict[str, Any]:
    row_id = str(row.get("row_id", "")).strip() or "UNNAMED_VISIBLE_EM_HXF2_ROW"
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
                "edge_signature_ready": False,
                "full_generator_ready": False,
                "C_memory_F2_abs": "MISSING_NUMERIC_VALUE",
                "qbar_EM_memory_abs": "MISSING_NUMERIC_VALUE",
                "route_pass": False,
                "runner_status": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
                "missing_for_claim": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    if route_type == "generator_signature":
        result = evaluate_generator(row)
    elif route_type == "hxf2_memory_bound":
        result = evaluate_memory_bound(row)
    elif route_type == "hxf2_memory_zero":
        result = evaluate_memory_zero(row)
    else:
        result = {
            "edge_signature_ready": False,
            "full_generator_ready": False,
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
        print("Usage: visible_EM_generator_HXF2_runner.py INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    write_csv(Path(sys.argv[2]), [evaluate_row(row) for row in read_csv(Path(sys.argv[1]))])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
