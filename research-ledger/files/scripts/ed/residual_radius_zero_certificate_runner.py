from __future__ import annotations

import csv
import math
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Any


REQUIRED_COMPONENTS = (
    "R_eq_abs_kg",
    "B_zero_abs_kg",
    "boundary_flux_abs_kg",
    "open_EM_abs_kg",
    "nonEM_owner_gap_abs_kg",
    "projector_comm_abs_kg",
    "domain_shadow_abs_kg",
    "kappa_drift_abs_kg",
)

COMPONENT_ALIASES = {
    "R_EQ": "R_eq_abs_kg",
    "REQ": "R_eq_abs_kg",
    "B_ZERO": "B_zero_abs_kg",
    "BZERO": "B_zero_abs_kg",
    "BOUNDARY_FLUX": "boundary_flux_abs_kg",
    "BOUNDARY": "boundary_flux_abs_kg",
    "OPEN_EM": "open_EM_abs_kg",
    "OPENEM": "open_EM_abs_kg",
    "NONEM_OWNER_GAP": "nonEM_owner_gap_abs_kg",
    "NONEM": "nonEM_owner_gap_abs_kg",
    "PROJECTOR_COMM": "projector_comm_abs_kg",
    "PROJECTOR": "projector_comm_abs_kg",
    "DOMAIN_SHADOW": "domain_shadow_abs_kg",
    "DOMAIN": "domain_shadow_abs_kg",
    "KAPPA_DRIFT": "kappa_drift_abs_kg",
    "KAPPA": "kappa_drift_abs_kg",
}

FORBIDDEN_SOURCE_TOKENS = (
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

ZERO_CLAUSE_FIELDS = (
    "same_parent_branch_signed",
    "parent_action_signed",
    "same_frame_signed",
    "qbasic_support_signed",
    "boundary_silent_signed",
    "poynting_accounted_signed",
    "readout_postprocess_signed",
    "no_species_prefactor_signed",
    "no_postfit_signed",
    "component_specific_zero_signed",
)


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
    return number if math.isfinite(number) else None


def format_float(value: float | None) -> str:
    if value is None or not math.isfinite(value):
        return "MISSING_NUMERIC_VALUE"
    return f"{value:.15e}"


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def row_is_counterfactual(row: dict[str, Any]) -> bool:
    text = str(row.get("row_status", "")).strip().lower()
    return text.startswith("counterfactual") or "counterfactual" in text


def row_is_private(row: dict[str, Any]) -> bool:
    text = str(row.get("row_status", "")).strip().lower()
    return text.startswith("private") or "private" in text


def forbidden_source_used(row: dict[str, Any]) -> bool:
    source_text = " ".join(
        str(row.get(field, ""))
        for field in ("zero_source", "bound_source", "component_source", "provenance", "notes")
    ).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def normalized_component(row: dict[str, Any]) -> str | None:
    symbol = str(row.get("component_symbol", "")).strip()
    if not symbol:
        return None
    key = symbol.upper().replace("-", "_").replace(" ", "_")
    return COMPONENT_ALIASES.get(key)


def zero_clauses_signed(row: dict[str, Any]) -> bool:
    return all(bool_text(row.get(field)) for field in ZERO_CLAUSE_FIELDS)


def component_result(row: dict[str, Any]) -> dict[str, Any]:
    certificate_id = str(row.get("certificate_id", "")).strip() or "UNNAMED_CERTIFICATE"
    component_symbol = str(row.get("component_symbol", "")).strip() or "UNNAMED_COMPONENT"
    component_field = normalized_component(row)
    zero_anchor = parse_float(row.get("zero_anchor_abs_kg"))
    bound_value = parse_float(row.get("residual_bound_abs_kg"))
    zero_signed = zero_clauses_signed(row)
    counterfactual = row_is_counterfactual(row)
    private = row_is_private(row)
    forbidden = forbidden_source_used(row)

    output: dict[str, Any] = {
        "certificate_id": certificate_id,
        "component_symbol": component_symbol,
        "component_field": component_field or "UNKNOWN_COMPONENT",
        "row_status_input": row.get("row_status", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
        "zero_clauses_signed": zero_signed,
    }

    if component_field is None:
        output.update(
            {
                "component_abs_kg": "MISSING_NUMERIC_VALUE",
                "runner_status": "FAILED_UNKNOWN_RESIDUAL_COMPONENT",
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    if forbidden and not counterfactual:
        output.update(
            {
                "component_abs_kg": "MISSING_NUMERIC_VALUE",
                "runner_status": "FAILED_CIRCULAR_RESIDUAL_ZERO_SOURCE",
                "anti_circularity_status": "FAIL_OBSERVED_OR_FITTED_QUANTITY_USED_AS_RESIDUAL_SOURCE",
            }
        )
        return output

    if zero_signed and zero_anchor == 0:
        if counterfactual:
            runner_status = "RESIDUAL_ZERO_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM"
        elif private:
            runner_status = "RESIDUAL_ZERO_CERTIFIED_PRIVATE_NONCLAIM"
        else:
            runner_status = "RESIDUAL_ZERO_CERTIFIED_NONCLAIM"
        output.update(
            {
                "component_abs_kg": "0.000000000000000e+00",
                "runner_status": runner_status,
                "anti_circularity_status": "PASS_PARENT_ZERO_CERTIFICATE_NO_FIT_BACKFILL",
            }
        )
        return output

    if bound_value is not None and bound_value >= 0:
        output.update(
            {
                "component_abs_kg": format_float(bound_value),
                "runner_status": "RESIDUAL_BOUND_COMPUTED_NONCLAIM",
                "anti_circularity_status": "PASS_BOUND_SOURCE_NO_FIT_BACKFILL",
            }
        )
        return output

    output.update(
        {
            "component_abs_kg": "MISSING_NUMERIC_VALUE",
            "runner_status": "BLOCKED_MISSING_RESIDUAL_ZERO_OR_BOUND_INPUT",
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def aggregate_certificate(certificate_id: str, component_outputs: list[dict[str, Any]]) -> dict[str, Any]:
    values = {field: None for field in REQUIRED_COMPONENTS}
    statuses = {field: "MISSING_COMPONENT_ROW" for field in REQUIRED_COMPONENTS}
    zero_count = 0
    bound_count = 0
    fail_count = 0
    missing_count = 0
    counterfactual = False
    private = False

    for row in component_outputs:
        field = row["component_field"]
        status = row["runner_status"]
        row_status = str(row.get("row_status_input", "")).lower()
        counterfactual = counterfactual or "counterfactual" in row_status
        private = private or "private" in row_status
        if field in values:
            value = parse_float(row["component_abs_kg"])
            values[field] = value
            statuses[field] = status
        if status.startswith("FAILED"):
            fail_count += 1
        elif status.startswith("BLOCKED") or status == "MISSING_COMPONENT_ROW":
            missing_count += 1
        elif status.startswith("RESIDUAL_ZERO"):
            zero_count += 1
        elif status == "RESIDUAL_BOUND_COMPUTED_NONCLAIM":
            bound_count += 1

    for field, status in statuses.items():
        if status == "MISSING_COMPONENT_ROW":
            missing_count += 1

    complete = fail_count == 0 and missing_count == 0 and all(values[field] is not None for field in REQUIRED_COMPONENTS)
    delta = sum(abs(values[field] or 0.0) for field in REQUIRED_COMPONENTS) if complete else None
    missing_components = [field for field in REQUIRED_COMPONENTS if values[field] is None]
    failed_components = [field for field in REQUIRED_COMPONENTS if statuses[field].startswith("FAILED")]

    if fail_count > 0:
        runner_status = "FAILED_RESIDUAL_ZERO_CERTIFICATE"
    elif not complete:
        runner_status = "RESIDUAL_ZERO_CERTIFICATE_PARTIAL_BLOCKED"
    elif counterfactual and delta == 0:
        runner_status = "RESIDUAL_ZERO_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM"
    elif private and delta == 0:
        runner_status = "RESIDUAL_ZERO_CERTIFICATE_PRIVATE_NONCLAIM"
    elif delta == 0:
        runner_status = "RESIDUAL_ZERO_CERTIFICATE_NONCLAIM"
    else:
        runner_status = "RESIDUAL_RADIUS_BOUND_COMPUTED_NONCLAIM"

    return {
        "certificate_id": certificate_id,
        **{field: format_float(values[field]) if values[field] is not None else "MISSING_NUMERIC_VALUE" for field in REQUIRED_COMPONENTS},
        "Delta_H_abs_kg": format_float(delta),
        "zero_component_count": zero_count,
        "bound_component_count": bound_count,
        "missing_component_count": missing_count,
        "failed_component_count": fail_count,
        "missing_components": ";".join(missing_components),
        "failed_components": ";".join(failed_components),
        "component_statuses": ";".join(f"{field}:{statuses[field]}" for field in REQUIRED_COMPONENTS),
        "valid_for_claim": False,
        "claim_allowed": False,
        "runner_status": runner_status,
    }


def run(input_csv: Path, component_output_csv: Path, aggregate_output_csv: Path) -> None:
    with input_csv.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"input CSV has no rows: {input_csv}")

    grouped: OrderedDict[str, list[dict[str, Any]]] = OrderedDict()
    for row in rows:
        certificate_id = str(row.get("certificate_id", "")).strip() or "UNNAMED_CERTIFICATE"
        grouped.setdefault(certificate_id, []).append(row)

    component_outputs = [component_result(row) for row in rows]
    component_output_csv.parent.mkdir(parents=True, exist_ok=True)
    with component_output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(component_outputs[0].keys()))
        writer.writeheader()
        writer.writerows(component_outputs)

    by_certificate: dict[str, list[dict[str, Any]]] = {certificate_id: [] for certificate_id in grouped}
    for output in component_outputs:
        by_certificate[output["certificate_id"]].append(output)
    aggregate_outputs = [
        aggregate_certificate(certificate_id, by_certificate[certificate_id])
        for certificate_id in grouped
    ]
    with aggregate_output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(aggregate_outputs[0].keys()))
        writer.writeheader()
        writer.writerows(aggregate_outputs)


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print("usage: residual_radius_zero_certificate_runner.py INPUT.csv COMPONENT_OUTPUT.csv AGGREGATE_OUTPUT.csv", file=sys.stderr)
        return 2
    run(Path(argv[1]), Path(argv[2]), Path(argv[3]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
