from __future__ import annotations

import csv
import math
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1005-Y5-R10-Delta-ref-derivative-vector-norm-gate.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def md_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "S1005_0_handoff_doc",
            "path": "1004-Y5-R10-Bref-range-independence-theorem-or-Delta-ref-lambda-profile-row.md",
            "role": "1004 handoff selecting derivative-vector aggregate gate",
            "needle": "1005-Y5-R10-Delta-ref-derivative-vector-norm-gate.md",
        },
        {
            "source_id": "S1005_1_next_target",
            "path": "source-intake/mts_residuals/P8_Y5_R10_1004_NEXT_TARGET.csv",
            "role": "machine-readable 1005 target",
            "needle": "||D_ref Delta_ref||_1/M_H_ref",
        },
        {
            "source_id": "S1005_2_derivative_audit",
            "path": "source-intake/mts_residuals/P8_Y5_R10_997_DERIVATIVE_COMPONENT_AUDIT.csv",
            "role": "derivative-vector blocker from 997",
            "needle": "DVC997_5_vector_norm",
        },
        {
            "source_id": "S1005_3_no_cancellation",
            "path": "source-intake/mts_residuals/P8_Y5_R10_994_DELTAH_NO_CANCELLATION_ENVELOPE.csv",
            "role": "absolute residual envelope",
            "needle": "DHE994_1_no_cancellation",
        },
        {
            "source_id": "S1005_4_MHref_provenance",
            "path": "source-intake/mts_residuals/P8_Y5_R10_999_DELTA_REF_SOURCE_COEFFICIENT_PROVENANCE.csv",
            "role": "M_H_ref positive same-frame provenance requirement",
            "needle": "DCP999_3_MHref",
        },
        {
            "source_id": "S1005_5_source_runner",
            "path": "source-intake/mts_residuals/P8_Y5_R10_1000_STRICT_PROVENANCE_RUNNER.csv",
            "role": "source component strict runner",
            "needle": "REFUSED_MISSING_PROVENANCE_OR_PARENT_SELECTOR",
        },
        {
            "source_id": "S1005_6_radius_runner",
            "path": "source-intake/mts_residuals/P8_Y5_R10_1001_RADIAL_PROFILE_RUNNER.csv",
            "role": "radial component strict runner",
            "needle": "REFUSED_MISSING_RADIAL_SURFACE_PROVENANCE",
        },
        {
            "source_id": "S1005_7_time_runner",
            "path": "source-intake/mts_residuals/P8_Y5_R10_1002_TIME_PROFILE_RUNNER.csv",
            "role": "time component strict runner",
            "needle": "REFUSED_MISSING_STATIONARY_TAU_PROVENANCE",
        },
        {
            "source_id": "S1005_8_frame_runner",
            "path": "source-intake/mts_residuals/P8_Y5_R10_1003_FRAME_PROFILE_RUNNER.csv",
            "role": "frame component strict runner",
            "needle": "REFUSED_MISSING_COVARIANT_FRAME_PROVENANCE",
        },
        {
            "source_id": "S1005_9_lambda_runner",
            "path": "source-intake/mts_residuals/P8_Y5_R10_1004_LAMBDA_PROFILE_RUNNER.csv",
            "role": "lambda component strict runner",
            "needle": "REFUSED_MISSING_RANGE_INDEPENDENCE_PROVENANCE",
        },
        {
            "source_id": "S1005_10_1004_claim_gate",
            "path": "source-intake/mts_residuals/P8_Y5_R10_1004_CLAIM_GATE.csv",
            "role": "1004 derivative-vector gate precedent",
            "needle": "CG1004_3_derivative_vector",
        },
        {
            "source_id": "S1005_11_prior_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_1004_VALIDATION.csv",
            "role": "1004 validation pass",
            "needle": "V1004_SUMMARY",
        },
    ]
    rows: list[dict[str, str]] = []
    for spec in specs:
        path = source_path(spec["path"])
        text = read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": flag(path.exists()),
                "needle_found": flag(spec["needle"] in text),
                "valid_for_claim": "false",
            }
        )
    return rows


def component_ledger_rows() -> list[dict[str, str]]:
    return [
        {
            "component_id": "DVC1005_0_source",
            "component": "partial_source Delta_ref",
            "normalized_row": "Delta_ref_source_component_over_MH",
            "source_runner": "P8_Y5_R10_1000_STRICT_PROVENANCE_RUNNER.csv",
            "current_status": "guarded_but_refused",
            "theorem_zero_status": "missing_parent_signed_selector_zero",
            "source_bound_status": "missing_numeric_derivative_scale_Bref_rule_MHref",
            "score_ready": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "component_id": "DVC1005_1_radius",
            "component": "partial_r Delta_ref",
            "normalized_row": "Delta_ref_radial_profile_over_MH",
            "source_runner": "P8_Y5_R10_1001_RADIAL_PROFILE_RUNNER.csv",
            "current_status": "guarded_but_refused",
            "theorem_zero_status": "missing_parent_signed_surface_zero",
            "source_bound_status": "missing_radial_derivative_profile_surface_class_MHref",
            "score_ready": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "component_id": "DVC1005_2_time",
            "component": "partial_t Delta_ref",
            "normalized_row": "Delta_ref_time_profile_over_MH",
            "source_runner": "P8_Y5_R10_1002_TIME_PROFILE_RUNNER.csv",
            "current_status": "guarded_but_refused",
            "theorem_zero_status": "missing_parent_signed_stationary_tau_zero",
            "source_bound_status": "missing_time_derivative_profile_tau_lock_epsilon_tau_MHref",
            "score_ready": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "component_id": "DVC1005_3_frame",
            "component": "partial_frame Delta_ref",
            "normalized_row": "Delta_ref_frame_profile_over_MH",
            "source_runner": "P8_Y5_R10_1003_FRAME_PROFILE_RUNNER.csv",
            "current_status": "guarded_but_refused",
            "theorem_zero_status": "missing_parent_signed_covariant_frame_zero",
            "source_bound_status": "missing_frame_derivative_profile_epsilon_frame_MHref",
            "score_ready": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "component_id": "DVC1005_4_lambda",
            "component": "partial_lambda Delta_ref",
            "normalized_row": "Delta_ref_lambda_profile_over_MH",
            "source_runner": "P8_Y5_R10_1004_LAMBDA_PROFILE_RUNNER.csv",
            "current_status": "guarded_but_refused",
            "theorem_zero_status": "missing_parent_signed_range_independence_zero",
            "source_bound_status": "missing_lambda_derivative_profile_range_cokernel_MHref",
            "score_ready": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def vector_norm_schema_rows() -> list[dict[str, str]]:
    return [
        {
            "schema_id": "VNS1005_0_vector_formula",
            "target": "Delta_ref_derivative_vector_norm_over_MH",
            "formula": "||D_ref Delta_ref||_1/M_H_ref = sum_i abs(component_i)/M_H_ref",
            "required_columns": "system_id;source_component;radius_component;time_component;frame_component;lambda_component;M_H_ref;M_H_ref_units;component_units;component_source_paths;equation_refs;valid_for_claim",
            "acceptance_rule": "every component is parent-signed zero or finite numeric same-frame source-bound; M_H_ref positive and sourced; no MISSING markers",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "VNS1005_1_component_zero_switches",
            "target": "component theorem-zero flags",
            "formula": "component_zero=true only with its matching PARENT_SIGNED_*_TRUE authority",
            "required_columns": "source_zero_authority;surface_zero_authority;tau_zero_authority;frame_zero_authority;lambda_zero_authority;source_path;equation_ref",
            "acceptance_rule": "closure-only zeros and assumed plateaus are rejected component-by-component",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "VNS1005_2_MHref_gate",
            "target": "positive same-frame denominator",
            "formula": "M_H_ref = H_tau[S_link] - H_ref > 0 in the same source/clock/readout frame",
            "required_columns": "H_tau_source;H_ref_source;tau_frame_id;coframe_id;units;source_path;equation_ref;not_orbital_GM_imported",
            "acceptance_rule": "no orbital-GM import, no fitted denominator, no frame-mismatched M_H_ref",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "VNS1005_3_no_cancellation",
            "target": "vector norm contribution to residual envelope",
            "formula": "absolute values only; vector norm is an L1 upper envelope",
            "required_columns": "no_cancellation_guard=ABS_SUM_NO_COMPONENT_CANCELLATION",
            "acceptance_rule": "component cancellation, branch cancellation, and sign cancellation are rejected",
            "valid_for_claim": "false",
        },
    ]


def candidate_vector_rows() -> list[dict[str, str]]:
    base = {
        "system_id": "R10_local_reference_branch",
        "source_component": "MISSING_SOURCE_COMPONENT",
        "radius_component": "MISSING_RADIUS_COMPONENT",
        "time_component": "MISSING_TIME_COMPONENT",
        "frame_component": "MISSING_FRAME_COMPONENT",
        "lambda_component": "MISSING_LAMBDA_COMPONENT",
        "component_units": "MISSING_COMPONENT_UNITS",
        "M_H_ref": "MISSING_M_H_REF",
        "M_H_ref_units": "MISSING_M_H_REF_UNITS",
        "source_zero_authority": "MISSING_SOURCE_ZERO_AUTHORITY",
        "surface_zero_authority": "MISSING_SURFACE_ZERO_AUTHORITY",
        "tau_zero_authority": "MISSING_TAU_ZERO_AUTHORITY",
        "frame_zero_authority": "MISSING_FRAME_ZERO_AUTHORITY",
        "lambda_zero_authority": "MISSING_LAMBDA_ZERO_AUTHORITY",
        "component_source_paths": "MISSING_COMPONENT_SOURCE_PATHS",
        "equation_refs": "MISSING_EQUATION_REFS",
        "M_H_ref_source_path": "MISSING_M_H_REF_SOURCE_PATH",
        "not_orbital_GM_imported": "false",
        "no_cancellation_guard": "MISSING_ABS_SUM_GUARD",
        "valid_for_claim": "false",
    }
    variants = [
        ("VCT1005_0_all_components_missing", "all five component values are missing"),
        ("VCT1005_1_MHref_missing", "positive same-frame M_H_ref denominator is missing"),
        ("VCT1005_2_zero_authorities_missing", "component zero flags have no parent-signed authorities"),
        ("VCT1005_3_component_sources_missing", "component source paths and equation refs are missing"),
        ("VCT1005_4_cancellation_attempt", "component cancellation is attempted rather than L1 absolute summing"),
        ("VCT1005_5_live_placeholder", "live vector norm row is schema-only and cannot be scored"),
    ]
    rows: list[dict[str, str]] = []
    for row_id, purpose in variants:
        row = {**base, "candidate_id": row_id, "target": "Delta_ref_derivative_vector_norm_over_MH", "purpose": purpose}
        if row_id == "VCT1005_4_cancellation_attempt":
            row["source_component"] = "1.0"
            row["radius_component"] = "-1.0"
            row["time_component"] = "0.0"
            row["frame_component"] = "0.0"
            row["lambda_component"] = "0.0"
            row["component_units"] = "same_as_Delta_ref"
            row["M_H_ref"] = "1.0"
            row["M_H_ref_units"] = "same_as_Delta_ref"
            row["no_cancellation_guard"] = "SIGNED_SUM_CANCELLATION_ATTEMPT"
        rows.append(row)
    return rows


def is_missing(value: str) -> bool:
    stripped = str(value).strip()
    return not stripped or stripped.upper().startswith("MISSING") or stripped.upper().startswith("SCHEMA_ONLY")


def finite_float(value: str) -> tuple[bool, float | None]:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False, None
    return math.isfinite(number), number


def path_list_exists(value: str) -> bool:
    if is_missing(value):
        return False
    paths = [item.strip() for item in value.split(";") if item.strip()]
    if not paths:
        return False
    for item in paths:
        path = Path(item)
        if not path.is_absolute():
            path = ROOT / item
        if not path.exists():
            return False
    return True


def evaluate_vector(row: dict[str, str]) -> dict[str, str]:
    reasons: list[str] = []
    component_fields = ["source_component", "radius_component", "time_component", "frame_component", "lambda_component"]
    component_values: list[float] = []
    for field in component_fields:
        ok, value = finite_float(row.get(field, ""))
        if not ok or value is None:
            reasons.append(f"MISSING_VECTOR_COMPONENT_{field.upper()}")
        else:
            component_values.append(value)
    mh_ok, mh_value = finite_float(row.get("M_H_ref", ""))
    if not mh_ok or mh_value is None or mh_value <= 0:
        reasons.append("MISSING_POSITIVE_SAME_FRAME_M_H_REF")
    for field in ["component_units", "M_H_ref_units", "equation_refs"]:
        if is_missing(row.get(field, "")):
            reasons.append(f"MISSING_{field.upper()}")
    if not path_list_exists(row.get("component_source_paths", "")):
        reasons.append("MISSING_EXISTING_COMPONENT_SOURCE_PATHS")
    if not path_list_exists(row.get("M_H_ref_source_path", "")):
        reasons.append("MISSING_EXISTING_M_H_REF_SOURCE_PATH")
    if row.get("not_orbital_GM_imported") != "true":
        reasons.append("M_H_REF_ORBITAL_GM_IMPORT_NOT_EXCLUDED")
    if row.get("no_cancellation_guard") != "ABS_SUM_NO_COMPONENT_CANCELLATION":
        reasons.append("MISSING_ABS_SUM_NO_COMPONENT_CANCELLATION_GUARD")
    zero_authorities = [
        "source_zero_authority",
        "surface_zero_authority",
        "tau_zero_authority",
        "frame_zero_authority",
        "lambda_zero_authority",
    ]
    for field in zero_authorities:
        value = row.get(field, "")
        if is_missing(value):
            reasons.append(f"MISSING_{field.upper()}")
        elif not value.startswith("PARENT_SIGNED_"):
            reasons.append(f"UNSIGNED_{field.upper()}")
    if row.get("valid_for_claim") != "true":
        reasons.append("VALID_FOR_CLAIM_FALSE")
    numeric_ratio = "NOT_SCORED"
    if not reasons and mh_value is not None:
        numeric_ratio = f"{sum(abs(value) for value in component_values) / mh_value:.16e}"
    verdict = "ACCEPT_VECTOR_NORM" if not reasons else "REFUSED_MISSING_VECTOR_COMPONENTS_OR_MHREF"
    return {
        "runner_id": row["candidate_id"].replace("VCT", "VNR"),
        "candidate_id": row["candidate_id"],
        "target": row["target"],
        "verdict": verdict,
        "score_ready": flag(not reasons),
        "claim_allowed": "false",
        "valid_for_claim": "false",
        "computed_L1_over_MHref": numeric_ratio,
        "failure_reasons": ";".join(reasons) if reasons else "none",
        "generated_utc": stamp(),
    }


def vector_runner_rows(candidates: list[dict[str, str]]) -> list[dict[str, str]]:
    return [evaluate_vector(row) for row in candidates]


def refusal_ledger_rows(runner: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        {
            "refusal_id": row["runner_id"].replace("VNR", "VRF"),
            "candidate_id": row["candidate_id"],
            "refusal": row["verdict"],
            "why": row["failure_reasons"],
            "required_exit": "all five components parent-zero or source-bounded, positive sourced M_H_ref, existing source paths, and ABS_SUM_NO_COMPONENT_CANCELLATION",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        }
        for row in runner
    ]


def claim_gate_rows(components: list[dict[str, str]], runner: list[dict[str, str]]) -> list[dict[str, str]]:
    runner_refuses = all(row["verdict"] == "REFUSED_MISSING_VECTOR_COMPONENTS_OR_MHREF" for row in runner)
    components_blocked = all(row["score_ready"] == "false" and row["valid_for_claim"] == "false" for row in components)
    return [
        {
            "gate_id": "CG1005_0_components_guarded",
            "claim": "all five Delta_ref derivative components have strict guardrails",
            "gate_pass": flag(len(components) == 5 and components_blocked),
            "reason": "1000-1004 produce refused nonclaim runners for source/radius/time/frame/lambda",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1005_1_vector_norm_bound",
            "claim": "||D_ref Delta_ref||_1/M_H_ref is bounded",
            "gate_pass": "false",
            "reason": "component values and positive same-frame M_H_ref are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1005_2_no_component_cancellation",
            "claim": "component cancellation can be used to pass the vector gate",
            "gate_pass": "false",
            "reason": "L1 absolute sum is required; signed cancellation rows are refused",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1005_3_RC994_0",
            "claim": "RC994_0 residual current passes",
            "gate_pass": "false",
            "reason": "Delta_ref derivative vector norm and M_H_ref denominator remain nonclaim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1005_4_FB554_0_local_GR",
            "claim": "FB554_0/local-GR branch passes",
            "gate_pass": "false",
            "reason": "local R10 residual vector is scaffolded but not zero or source-bounded",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1005_5_guardrail",
            "claim": "derivative-vector norm guardrail is installed",
            "gate_pass": flag(runner_refuses and components_blocked),
            "reason": "all component placeholders are refused and vector norm runner blocks promotion",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1005_0_vector_not_claimed",
            "decision": "do not claim ||D_ref Delta_ref||_1/M_H_ref is finite or small",
            "reason": "all five components are guarded but missing parent-zero or source-bound values; M_H_ref is also missing",
            "effect": "RC994_0 and local-GR remain blocked",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1005_1_no_cancellation_policy",
            "decision": "use L1 absolute component sum only",
            "reason": "signed component cancellation would fake a local-GR pass",
            "effect": "future component rows must be individually zero or bounded",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1005_2_next_MHref_target",
            "decision": "move to positive same-frame M_H_ref denominator",
            "reason": "M_H_ref is a shared blocker across all component bounds",
            "effect": "1006 should prove or source H_tau[S_link]-H_ref before any numeric vector gate can score",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md",
            "objective": "prove positive same-frame M_H_ref=H_tau[S_link]-H_ref or stage a strict nonclaim denominator source row",
            "include": "H_tau, H_ref, tau/frame/coframe ids, source/equation paths, positivity, no orbital-GM import, compatibility with component bounds",
            "exclude": "fitted denominator, orbital GM substitution, frame-mismatched mass, RC994_0 pass, FB554_0 pass, local-GR claim, GitHub action",
            "valid_for_claim": "false",
        }
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    start_timestamp = SCRIPT_START_UTC.timestamp()
    for dirpath, _, filenames in os.walk(FORMALIZATION):
        for filename in filenames:
            path = Path(dirpath) / filename
            try:
                if path.stat().st_mtime > start_timestamp:
                    count += 1
            except OSError:
                count += 1
    return count


def validation_rows(
    sources: list[dict[str, str]],
    components: list[dict[str, str]],
    schema: list[dict[str, str]],
    candidates: list[dict[str, str]],
    runner: list[dict[str, str]],
    refusals: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    components_ok = len(components) == 5 and all(row["score_ready"] == "false" and row["valid_for_claim"] == "false" for row in components)
    schema_ok = any(row["schema_id"] == "VNS1005_0_vector_formula" for row in schema) and any(row["schema_id"] == "VNS1005_3_no_cancellation" for row in schema)
    candidates_ok = len(candidates) >= 6 and all(row["valid_for_claim"] == "false" for row in candidates)
    runner_ok = all(row["verdict"] == "REFUSED_MISSING_VECTOR_COMPONENTS_OR_MHREF" and row["score_ready"] == "false" for row in runner)
    cancellation_ok = any(
        row["candidate_id"] == "VCT1005_4_cancellation_attempt"
        and "MISSING_ABS_SUM_NO_COMPONENT_CANCELLATION_GUARD" in row["failure_reasons"]
        for row in runner
    )
    mhref_ok = any("MISSING_POSITIVE_SAME_FRAME_M_H_REF" in row["failure_reasons"] for row in runner)
    refusals_ok = len(refusals) == len(runner) and all(row["claim_allowed"] == "false" for row in refusals)
    claims_ok = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in claims)
    vector_gate_ok = any(row["gate_id"] == "CG1005_1_vector_norm_bound" and row["gate_pass"] == "false" for row in claims)
    decisions_ok = any(row["decision_id"] == "DEC1005_2_next_MHref_target" for row in decisions)
    next_ok = bool(next_target) and next_target[0]["valid_for_claim"] == "false"
    formalization_count = formalization_changed_after_start()
    checks = [
        {"check_id": "V1005_0_sources_exist", "result": "pass" if sources_ok else "fail", "detail": "all source paths exist and needles are present"},
        {"check_id": "V1005_1_component_ledger_complete", "result": "pass" if components_ok else "fail", "detail": "five derivative components are represented and nonclaim"},
        {"check_id": "V1005_2_schema_ready", "result": "pass" if schema_ok else "fail", "detail": "vector formula and no-cancellation schema rows are present"},
        {"check_id": "V1005_3_candidate_rows_nonclaim", "result": "pass" if candidates_ok else "fail", "detail": "candidate vector rows remain valid_for_claim=false"},
        {"check_id": "V1005_4_runner_refuses_placeholders", "result": "pass" if runner_ok else "fail", "detail": "runner refuses every current vector placeholder row"},
        {"check_id": "V1005_5_no_cancellation_guard", "result": "pass" if cancellation_ok else "fail", "detail": "signed cancellation attempt is refused"},
        {"check_id": "V1005_6_MHref_guard", "result": "pass" if mhref_ok else "fail", "detail": "positive same-frame M_H_ref is demanded"},
        {"check_id": "V1005_7_refusal_ledger_nonclaim", "result": "pass" if refusals_ok else "fail", "detail": "refusal ledger mirrors runner and keeps claims false"},
        {"check_id": "V1005_8_claim_gates_blocked", "result": "pass" if claims_ok else "fail", "detail": "vector, RC994_0, FB554_0, and local-GR claims stay blocked"},
        {"check_id": "V1005_9_vector_gate_written", "result": "pass" if vector_gate_ok else "fail", "detail": "derivative-vector aggregate gate is present and blocked"},
        {"check_id": "V1005_10_decision_written", "result": "pass" if decisions_ok else "fail", "detail": "M_H_ref denominator target decision is written"},
        {"check_id": "V1005_11_next_target_written", "result": "pass" if next_ok else "fail", "detail": "1006 target row is present and nonclaim"},
        {"check_id": "V1005_12_formalization_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization-workbench modified-file count since script start is {formalization_count}"},
    ]
    ready = all(row["result"] == "pass" for row in checks)
    checks.append(
        {
            "check_id": "V1005_SUMMARY",
            "result": "pass" if ready else "fail",
            "detail": "1005 derivative-vector norm gate validation summary",
            "generated_utc": stamp(),
        }
    )
    for row in checks:
        row.setdefault("generated_utc", stamp())
    return checks


def write_doc(
    sources: list[dict[str, str]],
    components: list[dict[str, str]],
    schema: list[dict[str, str]],
    candidates: list[dict[str, str]],
    runner: list[dict[str, str]],
    refusals: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> None:
    lines = [
        "# 1005 Y5 R10 Delta-ref Derivative Vector Norm Gate",
        "",
        "**Status:** derivative-vector aggregate gate installed; all five components are guarded, but the vector norm is not claimable.",
        "",
        "**Claim ceiling:** this checkpoint does not claim a vector bound, RC994_0, FB554_0, R10, PPN, WEP, clock, orbital, or local-GR pass.",
        "",
        "## Source Register",
        "",
        md_table(sources, ["source_id", "path", "role", "needle", "exists", "needle_found", "valid_for_claim"]),
        "",
        "## Component Ledger",
        "",
        md_table(components, ["component_id", "component", "normalized_row", "source_runner", "current_status", "theorem_zero_status", "source_bound_status", "score_ready", "claim_allowed", "valid_for_claim"]),
        "",
        "## Vector Norm Schema",
        "",
        md_table(schema, ["schema_id", "target", "formula", "required_columns", "acceptance_rule", "valid_for_claim"]),
        "",
        "## Candidate Vector Template",
        "",
        md_table(candidates, ["candidate_id", "purpose", "target", "source_component", "radius_component", "time_component", "frame_component", "lambda_component", "M_H_ref", "no_cancellation_guard", "valid_for_claim"]),
        "",
        "## Vector Norm Runner",
        "",
        md_table(runner, ["runner_id", "candidate_id", "verdict", "score_ready", "claim_allowed", "computed_L1_over_MHref", "failure_reasons", "generated_utc"]),
        "",
        "## Refusal Ledger",
        "",
        md_table(refusals, ["refusal_id", "candidate_id", "refusal", "why", "required_exit", "claim_allowed", "valid_for_claim"]),
        "",
        "## Claim Gate",
        "",
        md_table(claims, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decisions, ["decision_id", "decision", "reason", "effect", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(validation, ["check_id", "result", "detail", "generated_utc"]),
        "",
        "## Next Target",
        "",
        md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    components = component_ledger_rows()
    schema = vector_norm_schema_rows()
    candidates = candidate_vector_rows()
    runner = vector_runner_rows(candidates)
    refusals = refusal_ledger_rows(runner)
    claims = claim_gate_rows(components, runner)
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, components, schema, candidates, runner, refusals, claims, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_1005_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_1005_COMPONENT_LEDGER.csv", components)
    write_csv(OUT / "P8_Y5_R10_1005_VECTOR_NORM_SCHEMA.csv", schema)
    write_csv(OUT / "P8_Y5_R10_1005_CANDIDATE_VECTOR_TEMPLATE.csv", candidates)
    write_csv(OUT / "P8_Y5_R10_1005_VECTOR_NORM_RUNNER.csv", runner)
    write_csv(OUT / "P8_Y5_R10_1005_REFUSAL_LEDGER.csv", refusals)
    write_csv(OUT / "P8_Y5_R10_1005_CLAIM_GATE.csv", claims)
    write_csv(OUT / "P8_Y5_R10_1005_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1005_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_1005_VALIDATION.csv", validation)
    write_doc(sources, components, schema, candidates, runner, refusals, claims, decisions, validation, next_target)


if __name__ == "__main__":
    main()
