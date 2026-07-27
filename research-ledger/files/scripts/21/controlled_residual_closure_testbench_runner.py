from __future__ import annotations

import csv
import math
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Any


COMPONENT_FIELDS = (
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

BASE_CLAUSES = (
    "same_parent_branch_signed",
    "controlled_Ttotal_profile_signed",
    "variation_before_readout_signed",
    "same_frame_signed",
    "no_postfit_signed",
)

COMPONENT_CLAUSES = {
    "R_eq_abs_kg": ("same_current_identity_signed", "Bzero_primitive_signed", "compact_test_support_signed"),
    "B_zero_abs_kg": ("Bzero_primitive_signed", "boundary_collar_silent_signed", "compact_test_support_signed"),
    "boundary_flux_abs_kg": ("boundary_collar_silent_signed", "no_wall_stress_signed", "fixed_boundary_data_signed"),
    "open_EM_abs_kg": ("poynting_once_signed", "fixed_EM_hodge_signed", "no_radiative_collar_flux_signed"),
    "nonEM_owner_gap_abs_kg": ("hilbert_only_source_signed", "no_spin_torsion_nonhilbert_signed", "no_decoupled_source_block_signed"),
    "projector_comm_abs_kg": ("projector_commutes_signed", "readout_postprocess_signed", "no_source_worldtube_reentry_signed"),
    "domain_shadow_abs_kg": ("fixed_domain_signed", "qbasic_support_signed", "no_birth_death_shell_signed"),
    "kappa_drift_abs_kg": ("kappa_lock_signed", "source_measure_lock_signed", "no_running_kappa_signed"),
}


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


def normalized_component(row: dict[str, Any]) -> str | None:
    symbol = str(row.get("component_symbol", "")).strip()
    if not symbol:
        return None
    key = symbol.upper().replace("-", "_").replace(" ", "_")
    return COMPONENT_ALIASES.get(key)


def forbidden_source_used(row: dict[str, Any]) -> bool:
    source_text = " ".join(
        str(row.get(field, ""))
        for field in ("closure_source", "bound_source", "component_source", "provenance", "notes")
    ).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_clauses(row: dict[str, Any], component_field: str) -> list[str]:
    clauses = [*BASE_CLAUSES, *COMPONENT_CLAUSES[component_field]]
    return [clause for clause in clauses if not bool_text(row.get(clause))]


def compute_component(row: dict[str, Any]) -> dict[str, Any]:
    closure_id = str(row.get("closure_id", "")).strip() or "UNNAMED_CLOSURE"
    component_symbol = str(row.get("component_symbol", "")).strip() or "UNNAMED_COMPONENT"
    component_field = normalized_component(row)
    counterfactual = row_is_counterfactual(row)
    private = row_is_private(row)

    output: dict[str, Any] = {
        "closure_id": closure_id,
        "component_symbol": component_symbol,
        "component_field": component_field or "UNKNOWN_COMPONENT",
        "row_status_input": row.get("row_status", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }

    if component_field is None:
        output.update(
            {
                "component_abs_kg": "MISSING_NUMERIC_VALUE",
                "missing_clauses": "UNKNOWN_COMPONENT",
                "runner_status": "FAILED_UNKNOWN_CONTROLLED_RESIDUAL_COMPONENT",
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    if forbidden_source_used(row) and not counterfactual:
        output.update(
            {
                "component_abs_kg": "MISSING_NUMERIC_VALUE",
                "missing_clauses": "FORBIDDEN_SOURCE",
                "runner_status": "FAILED_CIRCULAR_CONTROLLED_RESIDUAL_CLOSURE",
                "anti_circularity_status": "FAIL_OBSERVED_OR_FITTED_QUANTITY_USED_AS_RESIDUAL_CLOSURE",
            }
        )
        return output

    missing = missing_clauses(row, component_field)
    bound = parse_float(row.get("residual_bound_abs_kg"))
    if not missing:
        if counterfactual:
            status = "CONTROLLED_RESIDUAL_ZERO_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM"
        elif private:
            status = "CONTROLLED_RESIDUAL_ZERO_PRIVATE_TESTBENCH_NONCLAIM"
        else:
            status = "CONTROLLED_RESIDUAL_ZERO_CERTIFIED_NONCLAIM"
        output.update(
            {
                "component_abs_kg": "0.000000000000000e+00",
                "missing_clauses": "",
                "runner_status": status,
                "anti_circularity_status": "PASS_CONTROLLED_CLOSURE_NO_FIT_BACKFILL",
            }
        )
        return output

    if bound is not None and bound >= 0:
        output.update(
            {
                "component_abs_kg": format_float(bound),
                "missing_clauses": ";".join(missing),
                "runner_status": "CONTROLLED_RESIDUAL_BOUND_COMPUTED_NONCLAIM",
                "anti_circularity_status": "PASS_CONTROLLED_BOUND_NO_FIT_BACKFILL",
            }
        )
        return output

    output.update(
        {
            "component_abs_kg": "MISSING_NUMERIC_VALUE",
            "missing_clauses": ";".join(missing),
            "runner_status": "BLOCKED_MISSING_CONTROLLED_RESIDUAL_CLOSURE_CLAUSES",
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def aggregate_closure(closure_id: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    values = {field: None for field in COMPONENT_FIELDS}
    statuses = {field: "MISSING_COMPONENT_ROW" for field in COMPONENT_FIELDS}
    missing_map = {field: "MISSING_COMPONENT_ROW" for field in COMPONENT_FIELDS}
    zero_count = 0
    bound_count = 0
    missing_count = 0
    failed_count = 0
    counterfactual = False
    private = False

    for row in rows:
        field = row["component_field"]
        status = row["runner_status"]
        row_status = str(row.get("row_status_input", "")).lower()
        counterfactual = counterfactual or "counterfactual" in row_status
        private = private or "private" in row_status
        if field in values:
            values[field] = parse_float(row["component_abs_kg"])
            statuses[field] = status
            missing_map[field] = row.get("missing_clauses", "")

    for field in COMPONENT_FIELDS:
        status = statuses[field]
        if status.startswith("FAILED"):
            failed_count += 1
        elif status.startswith("BLOCKED") or status == "MISSING_COMPONENT_ROW":
            missing_count += 1
        elif status.startswith("CONTROLLED_RESIDUAL_ZERO"):
            zero_count += 1
        elif status == "CONTROLLED_RESIDUAL_BOUND_COMPUTED_NONCLAIM":
            bound_count += 1

    complete = failed_count == 0 and missing_count == 0 and all(values[field] is not None for field in COMPONENT_FIELDS)
    delta = sum(abs(values[field] or 0.0) for field in COMPONENT_FIELDS) if complete else None

    if failed_count:
        status = "FAILED_CONTROLLED_RESIDUAL_CLOSURE"
    elif not complete:
        status = "CONTROLLED_RESIDUAL_CLOSURE_PARTIAL_BLOCKED"
    elif counterfactual and delta == 0:
        status = "CONTROLLED_RESIDUAL_CLOSURE_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM"
    elif private and delta == 0:
        status = "CONTROLLED_SOURCE_TESTBENCH_ZERO_PRIVATE_NONCLAIM"
    elif delta == 0:
        status = "CONTROLLED_RESIDUAL_CLOSURE_ZERO_NONCLAIM"
    else:
        status = "CONTROLLED_RESIDUAL_CLOSURE_BOUND_NONCLAIM"

    return {
        "closure_id": closure_id,
        **{field: format_float(values[field]) if values[field] is not None else "MISSING_NUMERIC_VALUE" for field in COMPONENT_FIELDS},
        "Delta_H_abs_kg": format_float(delta),
        "zero_component_count": zero_count,
        "bound_component_count": bound_count,
        "missing_component_count": missing_count,
        "failed_component_count": failed_count,
        "missing_components": ";".join(field for field in COMPONENT_FIELDS if values[field] is None),
        "missing_clause_map": " | ".join(f"{field}:{missing_map[field]}" for field in COMPONENT_FIELDS if missing_map[field]),
        "valid_for_claim": False,
        "claim_allowed": False,
        "runner_status": status,
    }


def run(input_csv: Path, component_output_csv: Path, aggregate_output_csv: Path) -> None:
    with input_csv.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"input CSV has no rows: {input_csv}")

    component_outputs = [compute_component(row) for row in rows]
    grouped: OrderedDict[str, list[dict[str, Any]]] = OrderedDict()
    for output in component_outputs:
        grouped.setdefault(output["closure_id"], []).append(output)

    component_output_csv.parent.mkdir(parents=True, exist_ok=True)
    with component_output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(component_outputs[0].keys()))
        writer.writeheader()
        writer.writerows(component_outputs)

    aggregate_outputs = [aggregate_closure(closure_id, grouped[closure_id]) for closure_id in grouped]
    with aggregate_output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(aggregate_outputs[0].keys()))
        writer.writeheader()
        writer.writerows(aggregate_outputs)


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print("usage: controlled_residual_closure_testbench_runner.py INPUT.csv COMPONENT_OUTPUT.csv AGGREGATE_OUTPUT.csv", file=sys.stderr)
        return 2
    run(Path(argv[1]), Path(argv[2]), Path(argv[3]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
