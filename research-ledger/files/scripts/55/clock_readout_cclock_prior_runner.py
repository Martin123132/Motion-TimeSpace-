from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


CLOCK_CLAUSES = (
    "same_observer_coframe_signed",
    "clock_action_lapse_signed",
    "atomic_readout_constants_signed",
    "rest_mass_source_same_signed",
    "no_hidden_redshift_reentry_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

FORBIDDEN_SOURCE_TOKENS = (
    "GR_IMPORT",
    "SCHWARZSCHILD_AB_IMPORT",
    "EINSTEIN_VACUUM_IMPORT",
    "FIT_TO_BOUND",
    "BOUND_AS_SOURCE",
    "OBSERVED_RED_SHIFT_CANCEL",
    "CLOCK_BY_DECLARATION",
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
    source_text = " ".join(str(row.get(field, "")) for field in ("clock_id", "prior_id", "source_path", "equation_ref", "notes", "provenance")).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_clauses(row: dict[str, Any]) -> list[str]:
    return [clause for clause in CLOCK_CLAUSES if not bool_text(row.get(clause))]


def component_from_parts(row: dict[str, Any]) -> tuple[float | None, list[str]]:
    fields = ("c_T", "c_clock", "c_alpha", "c_mass")
    parsed: dict[str, float] = {}
    missing: list[str] = []
    for field in fields:
        value = parse_float(row.get(field))
        if value is None:
            missing.append(f"MISSING_{field}")
        else:
            parsed[field] = value
    if missing:
        return None, missing
    component = abs(parsed["c_T"] - parsed["c_clock"]) + abs(parsed["c_alpha"]) + abs(parsed["c_mass"])
    return component, []


def clock_identity_row(row: dict[str, Any]) -> dict[str, Any]:
    clock_id = str(row.get("clock_id", "")).strip() or "UNNAMED_CLOCK_IDENTITY"
    output: dict[str, Any] = {
        "clock_id": clock_id,
        "route": row.get("route", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "clock_component_abs": "MISSING_NUMERIC_VALUE",
                "clock_identity_theorem": False,
                "runner_status": "FAILED_CLOCK_IDENTITY_GATE",
                "missing_clock_inputs": "FORBIDDEN_CLOCK_SOURCE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    component, numeric_missing = component_from_parts(row)
    missing = [*missing_clauses(row), *numeric_missing]
    if component is None:
        output.update(
            {
                "clock_component_abs": "MISSING_NUMERIC_VALUE",
                "clock_identity_theorem": False,
                "runner_status": "BLOCKED_MISSING_CLOCK_IDENTITY_INPUTS",
                "missing_clock_inputs": ";".join(missing),
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    if not missing and component <= 1.0e-15:
        status = "CLOCK_READOUT_IDENTITY_ZERO_CONDITIONAL_THEOREM_NONCLAIM"
        theorem = True
    elif component <= 1.0e-15:
        status = "CLOCK_READOUT_ZERO_NUMERIC_PARENT_UNSIGNED_NONCLAIM"
        theorem = False
    else:
        status = "CLOCK_READOUT_FINITE_COMPONENT_COMPUTED_NONCLAIM"
        theorem = False
    output.update(
        {
            "clock_component_abs": format_float(component),
            "clock_identity_theorem": theorem,
            "runner_status": status,
            "missing_clock_inputs": ";".join(missing),
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def prior_row(row: dict[str, Any]) -> dict[str, Any]:
    prior_id = str(row.get("prior_id", "")).strip() or "UNNAMED_CCLOCK_PRIOR"
    output: dict[str, Any] = {
        "prior_id": prior_id,
        "component_expr": row.get("component_expr", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "clock_component_abs": "MISSING_NUMERIC_VALUE",
                "required_abs_max": format_float(parse_float(row.get("required_abs_max"))),
                "numeric_window_pass": False,
                "runner_status": "FAILED_CCLOCK_PRIOR_GATE",
                "missing_prior_inputs": "FORBIDDEN_CLOCK_PRIOR_SOURCE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    required = parse_float(row.get("required_abs_max"))
    direct_component = parse_float(row.get("clock_component_abs"))
    computed_component, component_missing = component_from_parts(row)
    component = direct_component if direct_component is not None else computed_component
    missing: list[str] = []
    if required is None or required <= 0.0:
        missing.append("MISSING_required_abs_max")
    if component is None:
        missing.extend(component_missing or ["MISSING_clock_component_abs"])
    if missing_text(row.get("source_path")):
        missing.append("MISSING_source_path")
    if missing_text(row.get("equation_ref")):
        missing.append("MISSING_equation_ref")
    if not bool_text(row.get("source_signed")):
        missing.append("MISSING_source_signed")

    if required is None or required <= 0.0 or component is None:
        output.update(
            {
                "clock_component_abs": "MISSING_NUMERIC_VALUE",
                "required_abs_max": format_float(required),
                "numeric_window_pass": False,
                "runner_status": "BLOCKED_MISSING_CCLOCK_PRIOR_INPUTS",
                "missing_prior_inputs": ";".join(missing),
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    passes = component <= required
    if not passes:
        status = "CCLOCK_PRIOR_NUMERIC_WINDOW_FAIL"
    elif bool_text(row.get("source_signed")) and bool_text(row.get("valid_for_claim")):
        status = "CCLOCK_PRIOR_NUMERIC_WINDOW_PASS_SOURCE_SIGNED_NONCLAIM"
    else:
        status = "CCLOCK_PRIOR_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM"
    output.update(
        {
            "clock_component_abs": format_float(component),
            "required_abs_max": format_float(required),
            "numeric_window_pass": passes,
            "runner_status": status,
            "missing_prior_inputs": ";".join(missing),
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({field for row in rows for field in row})
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    if len(sys.argv) != 4 or sys.argv[1] not in {"identity", "prior"}:
        print("Usage: clock_readout_cclock_prior_runner.py identity|prior INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    mode = sys.argv[1]
    input_path = Path(sys.argv[2])
    output_path = Path(sys.argv[3])
    rows = read_csv(input_path)
    outputs = [clock_identity_row(row) for row in rows] if mode == "identity" else [prior_row(row) for row in rows]
    write_csv(output_path, outputs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
