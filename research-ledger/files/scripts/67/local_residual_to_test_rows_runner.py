from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


ARENA_CLAUSES = (
    "residual_source_signed",
    "arena_projection_signed",
    "observable_mapping_signed",
    "units_signed",
    "bound_source_signed",
    "parent_BC_source_signed",
    "no_cancellation_signed",
)

FORBIDDEN_SOURCE_TOKENS = (
    "HAND_SWITCH",
    "LOCAL_FLRW_HAND_SWITCH",
    "BOUND_BY_DESIRE",
    "BOUND_ZERO_BY_ASSERTION",
    "OBSERVED_RESIDUAL_CANCEL",
    "EDGE_CANCELLATION",
    "POSTFIT_REFERENCE",
    "RETUNE_TO_PASS",
    "USE_BOUND_AS_SOURCE_COUPLING",
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
            "arena_id",
            "source_id",
            "source_url",
            "source_title",
            "projection_source",
            "notes",
            "provenance",
        )
    ).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_clauses(row: dict[str, Any]) -> list[str]:
    return [clause for clause in ARENA_CLAUSES if not bool_text(row.get(clause))]


def arena_projection_row(row: dict[str, Any]) -> dict[str, Any]:
    arena_id = str(row.get("arena_id", "")).strip() or "UNNAMED_ARENA"
    output: dict[str, Any] = {
        "arena_id": arena_id,
        "sector": row.get("sector", ""),
        "observable": row.get("observable", ""),
        "source_id": row.get("source_id", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "epsilon_local_abs": "MISSING_NUMERIC_VALUE",
                "observable_bound_abs": "MISSING_NUMERIC_VALUE",
                "tau_projection_abs": "MISSING_NUMERIC_VALUE",
                "tau_required_max_abs": "MISSING_NUMERIC_VALUE",
                "predicted_observable_abs": "MISSING_NUMERIC_VALUE",
                "numeric_bound_pass": False,
                "runner_status": "FAILED_ARENA_PROJECTION_GATE",
                "missing_arena_inputs": "FORBIDDEN_ARENA_PROJECTION_OR_CANCELLATION_SOURCE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    epsilon = parse_float(row.get("epsilon_local_abs"))
    bound = parse_float(row.get("observable_bound_abs"))
    tau = parse_float(row.get("tau_projection_abs"))
    missing: list[str] = missing_clauses(row)
    if epsilon is None or epsilon < 0.0:
        missing.append("MISSING_epsilon_local_abs")
    if bound is None or bound < 0.0:
        missing.append("MISSING_observable_bound_abs")

    if epsilon is None or bound is None or epsilon < 0.0 or bound < 0.0:
        output.update(
            {
                "epsilon_local_abs": format_float(epsilon),
                "observable_bound_abs": format_float(bound),
                "tau_projection_abs": "MISSING_NUMERIC_VALUE",
                "tau_required_max_abs": "MISSING_NUMERIC_VALUE",
                "predicted_observable_abs": "MISSING_NUMERIC_VALUE",
                "numeric_bound_pass": False,
                "runner_status": "BLOCKED_MISSING_BOUND_OR_RESIDUAL_INPUTS",
                "missing_arena_inputs": ";".join(missing),
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    if epsilon <= 1.0e-30:
        predicted = 0.0 if tau is None else abs(tau) * epsilon
        output.update(
            {
                "epsilon_local_abs": format_float(epsilon),
                "observable_bound_abs": format_float(bound),
                "tau_projection_abs": format_float(tau),
                "tau_required_max_abs": "INFINITE_ZERO_RESIDUAL",
                "predicted_observable_abs": format_float(predicted),
                "numeric_bound_pass": predicted <= bound,
                "runner_status": "ZERO_RESIDUAL_CONDITIONAL_PARENT_THEOREM_NONCLAIM",
                "missing_arena_inputs": ";".join(missing),
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    tau_required = bound / epsilon
    if tau is None:
        output.update(
            {
                "epsilon_local_abs": format_float(epsilon),
                "observable_bound_abs": format_float(bound),
                "tau_projection_abs": "MISSING_NUMERIC_VALUE",
                "tau_required_max_abs": format_float(tau_required),
                "predicted_observable_abs": "MISSING_NUMERIC_VALUE",
                "numeric_bound_pass": False,
                "runner_status": "REQUIRED_TAU_COMPUTED_PROJECTION_MISSING_NONCLAIM",
                "missing_arena_inputs": ";".join([*missing, "MISSING_tau_projection_abs"]),
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    predicted = abs(tau) * epsilon
    numeric_pass = predicted <= bound
    if numeric_pass and missing:
        status = "NUMERIC_PASS_IF_GIVEN_TAU_BUT_PARENT_OR_MAPPING_UNSIGNED_NONCLAIM"
    elif numeric_pass:
        status = "NUMERIC_PASS_WITH_SIGNED_MAPPING_NONCLAIM_UNLESS_INPUT_VALID"
    else:
        status = "NUMERIC_FAIL_GIVEN_TAU"

    claim_allowed = bool_text(row.get("valid_for_claim")) and not missing and numeric_pass
    output.update(
        {
            "epsilon_local_abs": format_float(epsilon),
            "observable_bound_abs": format_float(bound),
            "tau_projection_abs": format_float(abs(tau)),
            "tau_required_max_abs": format_float(tau_required),
            "predicted_observable_abs": format_float(predicted),
            "numeric_bound_pass": numeric_pass,
            "runner_status": status,
            "missing_arena_inputs": ";".join(missing),
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
        print("usage: local_residual_to_test_rows_runner.py <input.csv> <output.csv>", file=sys.stderr)
        return 2
    rows = [arena_projection_row(row) for row in read_csv(Path(sys.argv[1]))]
    write_csv(Path(sys.argv[2]), rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
