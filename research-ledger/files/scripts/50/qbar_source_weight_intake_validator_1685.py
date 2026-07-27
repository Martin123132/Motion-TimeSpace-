from __future__ import annotations

import math
import re
from pathlib import Path


EXPECTED_BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
EXPECTED_BASIS_COMPONENT = "qbar_source_weight"
EXPECTED_COEFFICIENT_SYMBOL = "zeta_source_weight_I"

IDENTITY_FIELDS = (
    "branch_id",
    "candidate_id",
    "basis_component",
    "coefficient_symbol",
    "accepted_form",
)

ROUTE_FIELDS = (
    "theorem_route_status",
    "finite_route_status",
    "source_label_forgetting_status",
    "ordinary_matter_connectedness_status",
)

VALUE_FIELDS = (
    "value_or_bound",
    "uncertainty",
    "sign_convention",
    "material_or_source_tags",
    "lambda_or_domain_if_range_dependent",
)

BASIS_FIELDS = (
    "parent_basis_X_I",
    "normalization",
    "units",
    "coordinate_dimension",
    "common_mode_measured_G_convention",
)

SOURCE_FIELDS = (
    "local_source_path",
    "source_anchor",
    "derivation_or_data_method",
    "confidence",
    "extraction_status",
)

PROJECTION_FIELDS = (
    "WEP_tau_material_worldtube",
    "R10_lambda_alpha_projection",
    "Newton_GM_calibration",
    "R11_operator_projection",
    "PPN_local_GR_projection",
)

CLAIM_FIELDS = (
    "accepted_for_scoring",
    "score_ready",
    "valid_prediction_row",
    "valid_for_claim",
    "claim_allowed",
)

REQUIRED_FIELDS = (
    *IDENTITY_FIELDS,
    *ROUTE_FIELDS,
    *VALUE_FIELDS,
    *BASIS_FIELDS,
    *SOURCE_FIELDS,
    *PROJECTION_FIELDS,
    *CLAIM_FIELDS,
)

NUMERIC_FIELDS = ("value_or_bound", "uncertainty")

PLACEHOLDER_MARKERS = (
    "MISSING",
    "PLACEHOLDER",
    "TBD",
    "TODO",
    "UNSIGNED",
    "BLOCKED",
    "NOT_DERIVED",
    "NOT_FILLED",
    "NONCLAIM",
    "NONE",
    "UNKNOWN",
    "NO_VALUE",
    "NO_BOUND",
)

FINITE_ROUTE_STATUSES = {"FINITE_VALUE_SOURCED", "FINITE_BOUND_SOURCED"}
THEOREM_ROUTE_STATUS = "THEOREM_ZERO_PARENT_SIGNED"
PARENT_SIGNED_STATUS = "PARENT_SIGNED"


def truth(value: object) -> bool:
    return str(value).strip().lower() == "true"


def blank(value: object) -> bool:
    return str(value).strip() == ""


def looks_placeholder(value: object) -> bool:
    text = str(value).strip().upper()
    if text == "":
        return True
    return any(marker in text for marker in PLACEHOLDER_MARKERS)


def parse_numeric_token(value: object) -> float | None:
    text = str(value).strip()
    if looks_placeholder(text):
        return None
    match = re.search(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?", text)
    if match is None:
        return None
    try:
        numeric_value = float(match.group(0))
    except ValueError:
        return None
    if not math.isfinite(numeric_value):
        return None
    return numeric_value


def resolve_source_path(value: object, root: str | Path | None = None) -> tuple[bool, str]:
    raw_path = str(value).strip()
    if looks_placeholder(raw_path):
        return False, raw_path
    candidate = Path(raw_path)
    if not candidate.is_absolute() and root is not None:
        candidate = Path(root) / candidate
    return candidate.exists(), str(candidate)


def evaluate_qbar_source_weight_row(row: dict[str, object], root: str | Path | None = None) -> dict[str, object]:
    normalized = {str(key): "" if value is None else str(value).strip() for key, value in row.items()}
    missing_fields = [field for field in REQUIRED_FIELDS if field not in normalized or blank(normalized.get(field, ""))]
    placeholder_fields = [
        field
        for field in REQUIRED_FIELDS
        if field in normalized and looks_placeholder(normalized[field])
    ]

    identity_failures: list[str] = []
    if normalized.get("branch_id") != EXPECTED_BRANCH_ID:
        identity_failures.append("branch_id")
    if normalized.get("basis_component") != EXPECTED_BASIS_COMPONENT:
        identity_failures.append("basis_component")
    if normalized.get("coefficient_symbol") != EXPECTED_COEFFICIENT_SYMBOL:
        identity_failures.append("coefficient_symbol")

    numeric_failures: list[str] = []
    numeric_values: dict[str, float] = {}
    for field in NUMERIC_FIELDS:
        parsed_value = parse_numeric_token(normalized.get(field, ""))
        if parsed_value is None:
            numeric_failures.append(field)
            continue
        if field == "uncertainty" and parsed_value < 0:
            numeric_failures.append(field)
            continue
        numeric_values[field] = parsed_value

    source_path_exists, resolved_source_path = resolve_source_path(normalized.get("local_source_path", ""), root=root)

    theorem_zero_signed = (
        normalized.get("theorem_route_status") == THEOREM_ROUTE_STATUS
        and normalized.get("source_label_forgetting_status") == PARENT_SIGNED_STATUS
        and normalized.get("ordinary_matter_connectedness_status") == PARENT_SIGNED_STATUS
    )
    finite_route_sourced = normalized.get("finite_route_status") in FINITE_ROUTE_STATUSES
    route_ok = theorem_zero_signed or finite_route_sourced
    route = "theorem_zero" if theorem_zero_signed else "finite" if finite_route_sourced else "none"

    claim_flags = {field: truth(normalized.get(field, "False")) for field in CLAIM_FIELDS}
    all_claim_flags_true = all(claim_flags.values())

    core_ok = (
        not missing_fields
        and not placeholder_fields
        and not identity_failures
        and not numeric_failures
        and source_path_exists
        and route_ok
    )
    row_pass = core_ok and all_claim_flags_true
    claim_safety_violation = (not core_ok) and any(claim_flags.values())

    reason_parts: list[str] = []
    if missing_fields:
        reason_parts.append("MISSING_REQUIRED_FIELDS")
    if placeholder_fields:
        reason_parts.append("PLACEHOLDER_OR_BLOCKED_FIELDS")
    if identity_failures:
        reason_parts.append("WRONG_QBAR_IDENTITY")
    if numeric_failures:
        reason_parts.append("NON_NUMERIC_VALUE_OR_UNCERTAINTY")
    if not source_path_exists:
        reason_parts.append("SOURCE_PATH_NOT_FOUND")
    if not route_ok:
        reason_parts.append("NO_PARENT_SIGNED_ZERO_OR_SOURCED_FINITE_ROUTE")
    if not all_claim_flags_true:
        reason_parts.append("CLAIM_FLAGS_NOT_ALL_TRUE")
    if claim_safety_violation:
        reason_parts.append("UNSAFE_TRUE_CLAIM_FLAG_ON_REJECTED_ROW")

    return {
        "row_pass": row_pass,
        "reason": "PASS" if row_pass else ";".join(reason_parts),
        "route": route,
        "route_ok": route_ok,
        "missing_fields": missing_fields,
        "placeholder_fields": placeholder_fields,
        "identity_failures": identity_failures,
        "numeric_failures": numeric_failures,
        "numeric_values": numeric_values,
        "source_path_exists": source_path_exists,
        "resolved_source_path": resolved_source_path,
        "claim_flags": claim_flags,
        "claim_safety_violation": claim_safety_violation,
        "valid_for_claim": row_pass,
        "claim_allowed": row_pass,
    }


def require_qbar_source_weight_row(row: dict[str, object], root: str | Path | None = None) -> dict[str, object]:
    result = evaluate_qbar_source_weight_row(row, root=root)
    if not result["row_pass"]:
        raise RuntimeError(f"qbar source-weight intake rejected: {result}")
    return result
