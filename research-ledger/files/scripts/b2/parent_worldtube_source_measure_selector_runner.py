from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


SELECTOR_CLAUSES = (
    "parent_action_signed",
    "single_observed_frame_signed",
    "tau_fixed_signed",
    "compact_support_signed",
    "linking_surface_class_signed",
    "M_H_ref_integrable_signed",
    "PiM_Hamiltonian_map_signed",
    "coupling_descent_signed",
    "boundary_reference_lock_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

FIRST_COMPONENTS = (
    "B_zero_flux_abs",
    "Delta_symp_abs",
    "H_ref_shift_abs",
    "Delta_worldtube_domain_abs",
    "Delta_frame_source_abs",
    "B_obs_source_measure_abs",
)

FORBIDDEN_SOURCE_TOKENS = (
    "GR_IMPORT",
    "FIT_TO_BOUND",
    "BOUND_AS_SOURCE",
    "ORBITAL_GM_AS_SOURCE",
    "POST_READOUT_MASK",
    "REFERENCE_ONLY_ZERO",
    "BARE_MASS_SHORTCUT",
    "LATE_EQUALITY_MULTIPLIER",
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
    source_text = " ".join(str(row.get(field, "")) for field in ("selector_id", "input_id", "source_path", "equation_ref", "notes", "provenance")).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_clauses(row: dict[str, Any]) -> list[str]:
    return [clause for clause in SELECTOR_CLAUSES if not bool_text(row.get(clause))]


def first_epsilon(row: dict[str, Any]) -> tuple[float | None, list[str]]:
    values: list[float] = []
    missing: list[str] = []
    for component in FIRST_COMPONENTS:
        value = parse_float(row.get(component))
        if value is None or value < 0.0:
            missing.append(f"MISSING_{component}")
        else:
            values.append(value)
    mh_ref = parse_float(row.get("M_H_ref_abs"))
    if mh_ref is None or mh_ref <= 0.0:
        missing.append("MISSING_M_H_ref_abs")
    if missing:
        return None, missing
    return sum(values) / mh_ref, []


def selector_row(row: dict[str, Any]) -> dict[str, Any]:
    selector_id = str(row.get("selector_id", "")).strip() or "UNNAMED_SELECTOR"
    output: dict[str, Any] = {
        "selector_id": selector_id,
        "route": row.get("route", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "epsilon_selector_abs": "MISSING_NUMERIC_VALUE",
                "selector_theorem": False,
                "runner_status": "FAILED_SELECTOR_GATE",
                "missing_selector_inputs": "FORBIDDEN_SELECTOR_SOURCE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    epsilon, numeric_missing = first_epsilon(row)
    missing = [*missing_clauses(row), *numeric_missing]
    if epsilon is None:
        output.update(
            {
                "epsilon_selector_abs": "MISSING_NUMERIC_VALUE",
                "selector_theorem": False,
                "runner_status": "BLOCKED_MISSING_SELECTOR_INPUTS",
                "missing_selector_inputs": ";".join(missing),
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    if not missing and epsilon <= 1.0e-15:
        status = "PARENT_SELECTOR_ZERO_CONDITIONAL_THEOREM_NONCLAIM"
        theorem = True
    elif epsilon <= 1.0e-15:
        status = "PARENT_SELECTOR_ZERO_NUMERIC_PARENT_UNSIGNED_NONCLAIM"
        theorem = False
    else:
        status = "PARENT_SELECTOR_FINITE_INPUT_COMPUTED_NONCLAIM"
        theorem = False
    output.update(
        {
            "epsilon_selector_abs": format_float(epsilon),
            "selector_theorem": theorem,
            "runner_status": status,
            "missing_selector_inputs": ";".join(missing),
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def first_input_row(row: dict[str, Any]) -> dict[str, Any]:
    input_id = str(row.get("input_id", "")).strip() or "UNNAMED_FIRST_INPUT"
    output: dict[str, Any] = {
        "input_id": input_id,
        "component_expr": row.get("component_expr", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "epsilon_selector_abs": "MISSING_NUMERIC_VALUE",
                "required_abs_max": format_float(parse_float(row.get("required_abs_max"))),
                "numeric_window_pass": False,
                "runner_status": "FAILED_FIRST_INPUT_GATE",
                "missing_first_inputs": "FORBIDDEN_FIRST_INPUT_SOURCE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    required = parse_float(row.get("required_abs_max"))
    direct_value = parse_float(row.get("epsilon_selector_abs"))
    computed_value, computed_missing = first_epsilon(row)
    value = direct_value if direct_value is not None else computed_value
    missing: list[str] = []
    if required is None or required <= 0.0:
        missing.append("MISSING_required_abs_max")
    if value is None:
        missing.extend(computed_missing or ["MISSING_epsilon_selector_abs"])
    if missing_text(row.get("source_path")):
        missing.append("MISSING_source_path")
    if missing_text(row.get("equation_ref")):
        missing.append("MISSING_equation_ref")
    if not bool_text(row.get("source_signed")):
        missing.append("MISSING_source_signed")
    if required is None or required <= 0.0 or value is None:
        output.update(
            {
                "epsilon_selector_abs": "MISSING_NUMERIC_VALUE",
                "required_abs_max": format_float(required),
                "numeric_window_pass": False,
                "runner_status": "BLOCKED_MISSING_FIRST_INPUTS",
                "missing_first_inputs": ";".join(missing),
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    passes = value <= required
    status = "FIRST_INPUT_NUMERIC_WINDOW_FAIL"
    if passes:
        status = "FIRST_INPUT_NUMERIC_WINDOW_PASS_SOURCE_SIGNED_NONCLAIM" if bool_text(row.get("source_signed")) and bool_text(row.get("valid_for_claim")) else "FIRST_INPUT_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM"
    output.update(
        {
            "epsilon_selector_abs": format_float(value),
            "required_abs_max": format_float(required),
            "numeric_window_pass": passes,
            "runner_status": status,
            "missing_first_inputs": ";".join(missing),
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
    if len(sys.argv) != 4 or sys.argv[1] not in {"selector", "first"}:
        print("Usage: parent_worldtube_source_measure_selector_runner.py selector|first INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    mode = sys.argv[1]
    rows = read_csv(Path(sys.argv[2]))
    outputs = [selector_row(row) for row in rows] if mode == "selector" else [first_input_row(row) for row in rows]
    write_csv(Path(sys.argv[3]), outputs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
