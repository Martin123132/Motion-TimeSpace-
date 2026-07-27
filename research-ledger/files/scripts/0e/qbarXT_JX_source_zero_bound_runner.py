from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


SOURCE_ZERO_CLAUSES = (
    "q_kernel_signed",
    "observed_coframe_signed",
    "matter_functor_signed",
    "no_marker_signed",
    "EM_F2_silence_signed",
    "hidden_tail_silence_signed",
    "support_boundary_domain_signed",
    "readout_silence_signed",
    "same_branch_signed",
)

QBAR_COMPONENTS = (
    "qbar_geom_abs",
    "qbar_theta_marker_abs",
    "qbar_EM_abs",
    "qbar_nonH_abs",
    "qbar_support_abs",
    "qbar_boundary_abs",
    "qbar_domain_abs",
    "qbar_readout_abs",
)

FORBIDDEN_SOURCE_TOKENS = (
    "WEP_ONLY_AS_ZERO",
    "MEASURED_G_ABSORPTION",
    "ORBITAL_GM_AS_SOURCE",
    "CANCEL_UNKNOWN_COMPONENTS",
    "FIT_TO_BOUND",
    "BOUND_AS_SOURCE",
    "GR_IMPORT",
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


def missing_clauses(row: dict[str, Any]) -> list[str]:
    return [f"MISSING_{clause}" for clause in SOURCE_ZERO_CLAUSES if not bool_text(row.get(clause))]


def evaluate_zero(row: dict[str, Any]) -> dict[str, Any]:
    missing = missing_clauses(row)
    passed = not missing
    return {
        "qbar_XT_bound_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "coupling_product_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "route_pass": passed,
        "runner_status": "QBARXT_JX_SOURCE_ZERO_PASS_NONCLAIM" if passed else "BLOCKED_SOURCE_ZERO_COMPONENTS",
        "missing_for_claim": "" if passed else ";".join(missing),
    }


def evaluate_qbar_bound(row: dict[str, Any]) -> dict[str, Any]:
    missing: list[str] = []
    values: list[float] = []
    for component in QBAR_COMPONENTS:
        value = parse_float(row.get(component))
        if value is None or value < 0.0:
            missing.append(f"MISSING_{component}")
        else:
            values.append(value)
    if not bool_text(row.get("source_signed")):
        missing.append("MISSING_source_signed")
    if not bool_text(row.get("units_signed")):
        missing.append("MISSING_units_signed")
    if not bool_text(row.get("same_branch_signed")):
        missing.append("MISSING_same_branch_signed")
    total = sum(values) if not any(item.startswith("MISSING_qbar") for item in missing) else None
    passed = bool(total is not None and not missing)
    return {
        "qbar_XT_bound_abs": fmt(total),
        "coupling_product_abs": "MISSING_NUMERIC_VALUE",
        "route_pass": passed,
        "runner_status": "QBARXT_COMPONENT_BOUND_PASS_NONCLAIM" if passed else "BLOCKED_QBARXT_COMPONENT_BOUND_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_product(row: dict[str, Any]) -> dict[str, Any]:
    missing: list[str] = []
    values: dict[str, float | None] = {}
    for field in ("K_eff_abs", "Qbar_XH_abs", "qbar_XT_bound_abs", "alpha_edge_abs", "FB5540_abs", "alpha_R11_abs", "alpha_bound"):
        values[field] = parse_float(row.get(field))
        if values[field] is None:
            missing.append(f"MISSING_{field}")
    if not bool_text(row.get("source_signed")):
        missing.append("MISSING_source_signed")
    if not bool_text(row.get("units_signed")):
        missing.append("MISSING_units_signed")
    product = None
    if all(values[field] is not None for field in values):
        product = (
            values["K_eff_abs"] * values["Qbar_XH_abs"] * values["qbar_XT_bound_abs"]
            + abs(values["alpha_edge_abs"])
            + abs(values["FB5540_abs"])
            + abs(values["alpha_R11_abs"])
        )
        if values["alpha_bound"] <= 0:
            missing.append("NONPOSITIVE_alpha_bound")
    passed = bool(product is not None and values["alpha_bound"] is not None and product <= values["alpha_bound"] and not missing)
    status = "COUPLING_PRODUCT_BOUND_PASS_NONCLAIM" if passed else "BLOCKED_OR_FAILED_COUPLING_PRODUCT_INPUTS"
    if product is not None and values["alpha_bound"] is not None and product > values["alpha_bound"] and not missing:
        status = "COUPLING_PRODUCT_NUMERIC_FAIL"
        missing.append("COUPLING_PRODUCT_EXCEEDS_BOUND")
    return {
        "qbar_XT_bound_abs": fmt(values.get("qbar_XT_bound_abs")),
        "coupling_product_abs": fmt(product),
        "route_pass": passed,
        "runner_status": status,
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_row(row: dict[str, Any]) -> dict[str, Any]:
    row_id = str(row.get("row_id", "")).strip() or "UNNAMED_QBAR_ROW"
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
                "qbar_XT_bound_abs": "MISSING_NUMERIC_VALUE",
                "coupling_product_abs": "MISSING_NUMERIC_VALUE",
                "route_pass": False,
                "runner_status": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
                "missing_for_claim": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    if missing_text(row.get("source_path")):
        result = {
            "qbar_XT_bound_abs": "MISSING_NUMERIC_VALUE",
            "coupling_product_abs": "MISSING_NUMERIC_VALUE",
            "route_pass": False,
            "runner_status": "BLOCKED_MISSING_SOURCE_PATH",
            "missing_for_claim": "MISSING_SOURCE_PATH",
        }
    elif route_type == "source_zero":
        result = evaluate_zero(row)
    elif route_type == "qbar_bound":
        result = evaluate_qbar_bound(row)
    elif route_type == "coupling_product":
        result = evaluate_product(row)
    else:
        result = {
            "qbar_XT_bound_abs": "MISSING_NUMERIC_VALUE",
            "coupling_product_abs": "MISSING_NUMERIC_VALUE",
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
        print("Usage: qbarXT_JX_source_zero_bound_runner.py INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    write_csv(Path(sys.argv[2]), [evaluate_row(row) for row in read_csv(Path(sys.argv[1]))])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
