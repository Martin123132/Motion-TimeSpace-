from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


FORBIDDEN_SOURCE_TOKENS = (
    "FIT_TO_BOUND",
    "BOUND_AS_SOURCE",
    "R10_ANCHOR_AS_PARENT",
    "WEP_ONLY_AS_ZERO",
    "CANCEL_UNKNOWN_COMPONENTS",
    "GR_IMPORT",
)

SOURCE_ZERO_CLAUSES = (
    "q_kernel_signed",
    "observed_coframe_signed",
    "matter_functor_signed",
    "no_marker_signed",
    "hidden_tail_silence_signed",
    "boundary_projector_silence_signed",
    "same_branch_signed",
)

METRIC_CLAUSES = (
    "metric_signed",
    "direction_signed",
    "units_signed",
    "cross_block_signed",
    "spectral_floor_signed",
    "same_branch_signed",
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


def missing_booleans(row: dict[str, Any], clauses: tuple[str, ...]) -> list[str]:
    return [f"MISSING_{clause}" for clause in clauses if not bool_text(row.get(clause))]


def metric_route(row: dict[str, Any]) -> dict[str, Any]:
    missing = missing_booleans(row, METRIC_CLAUSES)
    g_xx = parse_float(row.get("G_xx"))
    f_x2 = parse_float(row.get("f_x2"))
    rho_sqrt = parse_float(row.get("rho_sqrt"))
    beta_eff = parse_float(row.get("beta_eff"))
    beta_min = parse_float(row.get("beta_min"))
    metric_lock_tol = parse_float(row.get("metric_lock_tol"))
    for field, value in (
        ("G_xx", g_xx),
        ("f_x2", f_x2),
        ("rho_sqrt", rho_sqrt),
        ("beta_eff", beta_eff),
        ("beta_min", beta_min),
        ("metric_lock_tol", metric_lock_tol),
    ):
        if value is None:
            missing.append(f"MISSING_{field}")
    if rho_sqrt is not None and rho_sqrt <= 0:
        missing.append("NONPOSITIVE_rho_sqrt")
    metric_lock_ratio = None
    if g_xx is not None and f_x2 is not None and rho_sqrt is not None and rho_sqrt > 0:
        metric_lock_ratio = g_xx * f_x2 / rho_sqrt
    metric_lock_pass = bool(metric_lock_ratio is not None and metric_lock_tol is not None and abs(metric_lock_ratio - 1.0) <= metric_lock_tol)
    beta_pass = bool(beta_eff is not None and beta_min is not None and beta_eff >= beta_min and beta_min > 0)
    if not metric_lock_pass:
        missing.append("METRIC_LOCK_NOT_PROVED")
    if not beta_pass:
        missing.append("BETA_EIGENVALUE_NOT_PROVED")
    passed = not missing
    return {
        "metric_lock_ratio": fmt(metric_lock_ratio),
        "alpha_total_guard": "MISSING_NUMERIC_VALUE",
        "route_pass": passed,
        "runner_status": "PARENT_METRIC_EIGENVALUE_PASS_NONCLAIM" if passed else "BLOCKED_PARENT_METRIC_EIGENVALUE_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def source_zero_route(row: dict[str, Any]) -> dict[str, Any]:
    missing = missing_booleans(row, SOURCE_ZERO_CLAUSES)
    passed = not missing
    return {
        "metric_lock_ratio": "MISSING_NUMERIC_VALUE",
        "alpha_total_guard": "MISSING_NUMERIC_VALUE",
        "route_pass": passed,
        "runner_status": "SOURCE_ZERO_THEOREM_PASS_NONCLAIM" if passed else "BLOCKED_SOURCE_ZERO_INPUTS",
        "missing_for_claim": "" if passed else ";".join(missing),
    }


def bounded_coupling_route(row: dict[str, Any]) -> dict[str, Any]:
    missing: list[str] = []
    values: dict[str, float | None] = {}
    for field in ("K_X_abs", "Qbar_XH_abs", "qbar_XT_abs", "alpha_edge_abs", "FB5540_abs", "alpha_R11_abs", "alpha_bound"):
        values[field] = parse_float(row.get(field))
        if values[field] is None:
            missing.append(f"MISSING_{field}")
    if not bool_text(row.get("source_signed")):
        missing.append("MISSING_source_signed")
    if not bool_text(row.get("units_signed")):
        missing.append("MISSING_units_signed")
    alpha_total = None
    if all(values[field] is not None for field in values):
        alpha_total = (
            values["K_X_abs"] * values["Qbar_XH_abs"] * values["qbar_XT_abs"]
            + abs(values["alpha_edge_abs"])
            + abs(values["FB5540_abs"])
            + abs(values["alpha_R11_abs"])
        )
        if values["alpha_bound"] <= 0:
            missing.append("NONPOSITIVE_alpha_bound")
    passed = bool(alpha_total is not None and values["alpha_bound"] is not None and alpha_total <= values["alpha_bound"] and not missing)
    status = "BOUNDED_COUPLING_PASS_NONCLAIM" if passed else "BLOCKED_OR_FAILED_BOUNDED_COUPLING_INPUTS"
    if alpha_total is not None and values["alpha_bound"] is not None and alpha_total > values["alpha_bound"] and not missing:
        status = "BOUNDED_COUPLING_NUMERIC_FAIL"
        missing.append("ALPHA_TOTAL_EXCEEDS_BOUND")
    return {
        "metric_lock_ratio": "MISSING_NUMERIC_VALUE",
        "alpha_total_guard": fmt(alpha_total),
        "route_pass": passed,
        "runner_status": status,
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_row(row: dict[str, Any]) -> dict[str, Any]:
    row_id = str(row.get("row_id", "")).strip() or "UNNAMED_ROUTE"
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
                "metric_lock_ratio": "MISSING_NUMERIC_VALUE",
                "alpha_total_guard": "MISSING_NUMERIC_VALUE",
                "route_pass": False,
                "runner_status": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
                "missing_for_claim": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    if missing_text(row.get("source_path")):
        result = {
            "metric_lock_ratio": "MISSING_NUMERIC_VALUE",
            "alpha_total_guard": "MISSING_NUMERIC_VALUE",
            "route_pass": False,
            "runner_status": "BLOCKED_MISSING_SOURCE_PATH",
            "missing_for_claim": "MISSING_SOURCE_PATH",
        }
    elif route_type == "metric_eigenvalue":
        result = metric_route(row)
    elif route_type == "source_zero":
        result = source_zero_route(row)
    elif route_type == "bounded_coupling":
        result = bounded_coupling_route(row)
    else:
        result = {
            "metric_lock_ratio": "MISSING_NUMERIC_VALUE",
            "alpha_total_guard": "MISSING_NUMERIC_VALUE",
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
        print("Usage: parent_metric_source_zero_selector_runner.py INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    write_csv(Path(sys.argv[2]), [evaluate_row(row) for row in read_csv(Path(sys.argv[1]))])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
