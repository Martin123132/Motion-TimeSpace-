from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Tuple


COMPONENT_REQUIRED_FIELDS = [
    "group_id",
    "component_id",
    "component",
    "sector",
    "route",
    "parent_zero_signed",
    "private_zero_usable",
    "same_worldtube_support",
    "same_tau_coframe_support",
    "projection_closed",
    "boundary_closed",
    "coupling_closed",
    "uu_abs",
    "trace_abs",
    "source_path",
    "support_certificate_path",
    "input_valid_for_claim",
    "notes",
]

COMPONENT_BOOLEAN_FIELDS = [
    "parent_zero_signed",
    "private_zero_usable",
    "same_worldtube_support",
    "same_tau_coframe_support",
    "projection_closed",
    "boundary_closed",
    "coupling_closed",
    "input_valid_for_claim",
]

COMPONENT_NUMERIC_FIELDS = ["uu_abs", "trace_abs"]

AGGREGATE_REQUIRED_FIELDS = [
    "group_id",
    "aggregate_id",
    "arena",
    "Lambda_eff_abs",
    "projector_boundary_abs",
    "K_E_c2_abs",
    "F_E_threshold",
    "source_path",
    "support_certificate_path",
    "input_valid_for_claim",
    "notes",
]

AGGREGATE_NUMERIC_FIELDS = [
    "Lambda_eff_abs",
    "projector_boundary_abs",
    "K_E_c2_abs",
    "F_E_threshold",
]


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: List[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: str(row.get(field, "")) for field in fields})


def bool_text(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def parse_float(value: object) -> Tuple[bool, float]:
    text = str(value).strip()
    if not text or "MISSING" in text.upper():
        return False, math.nan
    try:
        number = float(text)
    except ValueError:
        return False, math.nan
    return math.isfinite(number), number


def path_exists(value: object) -> bool:
    text = str(value).strip()
    return bool(text and "MISSING" not in text.upper() and Path(text).exists())


def fmt(value: float) -> str:
    return "" if math.isnan(value) else f"{value:.12g}"


def evaluate_component_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    missing_fields = [
        field
        for field in COMPONENT_REQUIRED_FIELDS
        if field not in row or str(row.get(field, "")).strip() == ""
    ]
    booleans = {field: bool_text(row.get(field, "False")) for field in COMPONENT_BOOLEAN_FIELDS}
    parsed = {field: parse_float(row.get(field, "")) for field in COMPONENT_NUMERIC_FIELDS}
    numeric_ready = all(ok and value >= 0.0 for ok, value in parsed.values())
    source_path = str(row.get("source_path", "")).strip()
    support_path = str(row.get("support_certificate_path", "")).strip()
    source_ready = path_exists(source_path)
    support_ready = path_exists(support_path)
    same_support = booleans["same_worldtube_support"] and booleans["same_tau_coframe_support"]
    local_silence_ready = (
        same_support
        and booleans["projection_closed"]
        and booleans["boundary_closed"]
        and booleans["coupling_closed"]
    )
    zero_ready = (
        booleans["parent_zero_signed"]
        and local_silence_ready
        and source_ready
        and support_ready
    )
    finite_ready = numeric_ready and source_ready and support_ready
    input_valid = booleans["input_valid_for_claim"]
    valid_for_claim = input_valid and (zero_ready or finite_ready)
    component_uu_bound = 0.0 if zero_ready else (parsed["uu_abs"][1] if numeric_ready else math.nan)
    component_trace_bound = 0.0 if zero_ready else (parsed["trace_abs"][1] if numeric_ready else math.nan)
    contribution_ready = zero_ready or numeric_ready
    ricci_component_bound = (
        component_uu_bound + 0.5 * component_trace_bound
        if contribution_ready
        else math.nan
    )

    reasons: List[str] = []
    if missing_fields:
        reasons.extend([f"MISSING_FIELD_{field}" for field in missing_fields])
    for field, (ok, value) in parsed.items():
        if not ok:
            reasons.append(f"MISSING_OR_NONNUMERIC_{field}")
        elif value < 0.0:
            reasons.append(f"NEGATIVE_{field}")
    if not source_ready:
        reasons.append("MISSING_EXISTING_SOURCE_PATH")
    if not support_ready:
        reasons.append("MISSING_SUPPORT_CERTIFICATE_PATH")
    if not booleans["parent_zero_signed"]:
        reasons.append("PARENT_ZERO_UNSIGNED")
    if booleans["private_zero_usable"] and not booleans["parent_zero_signed"]:
        reasons.append("PRIVATE_ZERO_NOT_PARENT_PUBLIC_ZERO")
    for field in [
        "same_worldtube_support",
        "same_tau_coframe_support",
        "projection_closed",
        "boundary_closed",
        "coupling_closed",
    ]:
        if not booleans[field]:
            reasons.append(f"OPEN_{field.upper()}")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")

    if zero_ready and not input_valid:
        status = "PARENT_ZERO_SCHEMA_READY_NONCLAIM"
    elif zero_ready:
        status = "PARENT_ZERO_READY"
    elif finite_ready and not input_valid:
        status = "FINITE_COMPONENT_BOUND_SCHEMA_READY_NONCLAIM"
    elif finite_ready:
        status = "FINITE_COMPONENT_BOUND_READY"
    elif booleans["private_zero_usable"]:
        status = "PRIVATE_ZERO_ONLY_NONCLAIM"
    else:
        status = "SURVIVOR_COMPONENT_BLOCKED"

    return {
        "group_id": str(row.get("group_id", "")),
        "component_id": str(row.get("component_id", "")),
        "component": str(row.get("component", "")),
        "sector": str(row.get("sector", "")),
        "route": str(row.get("route", "")),
        "input_path": str(input_path),
        "source_path": source_path,
        "source_exists": str(source_ready),
        "support_certificate_path": support_path,
        "support_exists": str(support_ready),
        "parent_zero_signed": str(booleans["parent_zero_signed"]),
        "private_zero_usable": str(booleans["private_zero_usable"]),
        "same_support_ready": str(same_support),
        "local_silence_ready": str(local_silence_ready),
        "numeric_bound_ready": str(numeric_ready),
        "zero_ready": str(zero_ready),
        "finite_bound_ready": str(finite_ready),
        "contribution_ready": str(contribution_ready),
        "component_uu_bound": fmt(component_uu_bound),
        "component_trace_bound": fmt(component_trace_bound),
        "ricci_component_bound": fmt(ricci_component_bound),
        "input_valid_for_claim": str(input_valid),
        "valid_for_claim": str(valid_for_claim),
        "claim_allowed": str(valid_for_claim),
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_component_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_component_row(row, input_path) for row in read_csv(input_path)]


def component_groups(component_rows: Iterable[Mapping[str, str]]) -> Dict[str, List[Mapping[str, str]]]:
    groups: Dict[str, List[Mapping[str, str]]] = defaultdict(list)
    for row in component_rows:
        groups[str(row.get("group_id", ""))].append(row)
    return groups


def evaluate_aggregate_row(
    row: Mapping[str, str],
    input_path: Path,
    component_rows: List[Mapping[str, str]],
    component_output_path: Path,
) -> Dict[str, str]:
    missing_fields = [
        field
        for field in AGGREGATE_REQUIRED_FIELDS
        if field not in row or str(row.get(field, "")).strip() == ""
    ]
    parsed = {field: parse_float(row.get(field, "")) for field in AGGREGATE_NUMERIC_FIELDS}
    numeric_ready = all(ok and value >= 0.0 for ok, value in parsed.values())
    threshold_ready = parsed["F_E_threshold"][0] and parsed["F_E_threshold"][1] > 0.0
    K_ready = parsed["K_E_c2_abs"][0] and parsed["K_E_c2_abs"][1] >= 0.0
    source_path = str(row.get("source_path", "")).strip()
    support_path = str(row.get("support_certificate_path", "")).strip()
    source_ready = path_exists(source_path)
    support_ready = path_exists(support_path)
    input_valid = bool_text(row.get("input_valid_for_claim", "False"))

    group_id = str(row.get("group_id", ""))
    group_rows = component_groups(component_rows).get(group_id, [])
    unresolved = [
        str(component.get("component", ""))
        for component in group_rows
        if not bool_text(component.get("contribution_ready", "False"))
    ]
    components_ready = bool(group_rows) and not unresolved
    components_valid = bool(group_rows) and all(
        bool_text(component.get("valid_for_claim", "False")) for component in group_rows
    )

    if components_ready:
        E_res_uu = sum(float(component.get("component_uu_bound", "0") or 0.0) for component in group_rows)
        E_res_trace = sum(float(component.get("component_trace_bound", "0") or 0.0) for component in group_rows)
    else:
        E_res_uu = math.nan
        E_res_trace = math.nan

    if numeric_ready and components_ready:
        Ruu_abs_bound = (
            E_res_uu
            + 0.5 * E_res_trace
            + parsed["Lambda_eff_abs"][1]
            + parsed["projector_boundary_abs"][1]
        )
        F_E_norm = parsed["K_E_c2_abs"][1] * Ruu_abs_bound
        threshold = parsed["F_E_threshold"][1]
    else:
        Ruu_abs_bound = math.nan
        F_E_norm = math.nan
        threshold = math.nan

    schema_ready = (
        not missing_fields
        and numeric_ready
        and threshold_ready
        and K_ready
        and components_ready
    )
    support_ready = source_ready and support_ready
    within_threshold = schema_ready and F_E_norm <= threshold
    valid_for_claim = (
        schema_ready
        and support_ready
        and input_valid
        and components_valid
        and within_threshold
    )

    reasons: List[str] = []
    if missing_fields:
        reasons.extend([f"MISSING_FIELD_{field}" for field in missing_fields])
    for field, (ok, value) in parsed.items():
        if not ok:
            reasons.append(f"MISSING_OR_NONNUMERIC_{field}")
        elif value < 0.0:
            reasons.append(f"NEGATIVE_{field}")
    if not threshold_ready:
        reasons.append("MISSING_OR_INVALID_F_E_THRESHOLD")
    if not source_ready:
        reasons.append("MISSING_EXISTING_SOURCE_PATH")
    if not support_ready:
        reasons.append("MISSING_SUPPORT_CERTIFICATE_PATH")
    if not group_rows:
        reasons.append("MISSING_COMPONENT_GROUP")
    for component in unresolved:
        reasons.append(f"UNRESOLVED_COMPONENT_{component}")
    if not components_valid:
        reasons.append("COMPONENTS_NOT_VALID_FOR_CLAIM")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")
    if schema_ready and not within_threshold:
        reasons.append("RICCI_SURVIVOR_VECTOR_EXCEEDS_THRESHOLD")

    if valid_for_claim:
        status = "RICCI_SURVIVOR_VECTOR_ACCEPTS"
    elif schema_ready and support_ready and F_E_norm == 0.0:
        status = "RICCI_SURVIVOR_VECTOR_ZERO_SCHEMA_READY_NONCLAIM"
    elif schema_ready and support_ready and not within_threshold:
        status = "RICCI_SURVIVOR_VECTOR_FAILS_THRESHOLD"
    elif schema_ready:
        status = "RICCI_SURVIVOR_VECTOR_SCHEMA_READY_NONCLAIM"
    else:
        status = "RICCI_SURVIVOR_VECTOR_BLOCKED"

    return {
        "group_id": group_id,
        "aggregate_id": str(row.get("aggregate_id", "")),
        "arena": str(row.get("arena", "")),
        "input_path": str(input_path),
        "component_output_path": str(component_output_path),
        "source_path": source_path,
        "source_exists": str(source_ready),
        "support_certificate_path": support_path,
        "support_exists": str(support_ready),
        "component_count": str(len(group_rows)),
        "unresolved_components": ";".join(unresolved),
        "components_ready": str(components_ready),
        "components_valid_for_claim": str(components_valid),
        "schema_ready": str(schema_ready),
        "E_res_uu_norm": fmt(E_res_uu),
        "E_res_trace_norm": fmt(E_res_trace),
        "Lambda_eff_abs": "" if not parsed["Lambda_eff_abs"][0] else fmt(parsed["Lambda_eff_abs"][1]),
        "projector_boundary_abs": "" if not parsed["projector_boundary_abs"][0] else fmt(parsed["projector_boundary_abs"][1]),
        "Ruu_abs_bound": fmt(Ruu_abs_bound),
        "F_E_norm": fmt(F_E_norm),
        "F_E_threshold": fmt(threshold),
        "within_threshold": str(within_threshold),
        "input_valid_for_claim": str(input_valid),
        "valid_for_claim": str(valid_for_claim),
        "claim_allowed": str(valid_for_claim),
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_aggregate_rows(
    aggregate_input_path: Path,
    component_output_path: Path,
) -> List[Dict[str, str]]:
    component_rows = read_csv(component_output_path)
    return [
        evaluate_aggregate_row(row, aggregate_input_path, component_rows, component_output_path)
        for row in read_csv(aggregate_input_path)
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Gate local Ricci survivor-vector zeros and finite R_uu source rows.")
    parser.add_argument("--mode", choices=["components", "aggregate"], required=True)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--components-output", type=Path)
    args = parser.parse_args()
    if args.mode == "components":
        write_csv(args.output, evaluate_component_rows(args.input))
    else:
        if args.components_output is None:
            raise SystemExit("--components-output is required in aggregate mode")
        write_csv(args.output, evaluate_aggregate_rows(args.input, args.components_output))


if __name__ == "__main__":
    main()
