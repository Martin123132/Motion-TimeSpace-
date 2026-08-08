from __future__ import annotations

import csv
import math
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1000-Y5-R10-Delta-ref-source-coefficient-strict-provenance-runner.md"
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
            "source_id": "S1000_0_handoff_doc",
            "path": "999-Y5-R10-Bref-fixed-branch-selector-or-Delta-ref-source-coefficient-provenance.md",
            "role": "999 handoff selecting strict provenance runner",
            "needle": "1000-Y5-R10-Delta-ref-source-coefficient-strict-provenance-runner.md",
        },
        {
            "source_id": "S1000_1_coefficient_provenance",
            "path": "source-intake/mts_residuals/P8_Y5_R10_999_DELTA_REF_SOURCE_COEFFICIENT_PROVENANCE.csv",
            "role": "finite coefficient provenance requirements",
            "needle": "DCP999_0_partial_source_derivative",
        },
        {
            "source_id": "S1000_2_runner_readiness",
            "path": "source-intake/mts_residuals/P8_Y5_R10_999_COEFFICIENT_RUNNER_READINESS.csv",
            "role": "schema-ready but values-not-ready state",
            "needle": "DCR999_0_schema_ready",
        },
        {
            "source_id": "S1000_3_parent_selector_contract",
            "path": "source-intake/mts_residuals/P8_Y5_R10_999_PARENT_SELECTOR_CONTRACT.csv",
            "role": "future parent selector contract",
            "needle": "FBC999_0_selector_function",
        },
        {
            "source_id": "S1000_4_selector_attempt",
            "path": "source-intake/mts_residuals/P8_Y5_R10_999_FIXED_BRANCH_SELECTOR_ATTEMPT.csv",
            "role": "failed fixed-branch selector theorem attempt",
            "needle": "FBS999_7_verdict",
        },
        {
            "source_id": "S1000_5_component_template",
            "path": "source-intake/mts_residuals/P8_Y5_R10_998_DELTA_REF_SOURCE_COMPONENT_TEMPLATE.csv",
            "role": "source component formula and required columns",
            "needle": "DSC998_0_component_schema",
        },
        {
            "source_id": "S1000_6_refusal_precedent",
            "path": "source-intake/mts_residuals/P8_Y5_R10_998_STRICT_REFUSAL_LEDGER.csv",
            "role": "prior refusal for unsourced source calibration",
            "needle": "REF998_1_no_source_calibration",
        },
        {
            "source_id": "S1000_7_derivative_audit",
            "path": "source-intake/mts_residuals/P8_Y5_R10_997_DERIVATIVE_COMPONENT_AUDIT.csv",
            "role": "partial_source Delta_ref identified as derivative component",
            "needle": "DVC997_0_source",
        },
        {
            "source_id": "S1000_8_no_cancellation",
            "path": "source-intake/mts_residuals/P8_Y5_R10_994_DELTAH_NO_CANCELLATION_ENVELOPE.csv",
            "role": "absolute-value no-cancellation guard",
            "needle": "DHE994_1_no_cancellation",
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


def strict_schema_rows() -> list[dict[str, str]]:
    return [
        {
            "schema_id": "SIS1000_0_partial_source_Delta_ref",
            "field": "partial_source_Delta_ref",
            "required_input": "finite numeric derivative or theorem_zero=true with theorem_zero_authority=PARENT_SIGNED_TRUE",
            "units_requirement": "partial_source_units and Delta_ref_units must be explicit",
            "source_requirement": "source_path exists and equation_ref identifies the parent equation",
            "rejects": "MISSING_NUMERIC_DERIVATIVE_OR_THEOREM_ZERO; closure-zero; fitted-zero; inferred-zero",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "SIS1000_1_Delta_source_scale",
            "field": "Delta_source_scale",
            "required_input": "finite positive numeric scale for the source variation being tested",
            "units_requirement": "Delta_source_scale_units must be explicit and same-frame",
            "source_requirement": "source parameter definition and extraction/source path are required",
            "rejects": "chosen-to-shrink residual; unitless placeholder; MISSING_SOURCE_SCALE",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "SIS1000_2_Bref_rule",
            "field": "B_ref_rule",
            "required_input": "fixed formula and branch id for B_ref before source/readout is known",
            "units_requirement": "formula must declare frame and normalization convention",
            "source_requirement": "parent selector equation or finite provenance source path",
            "rejects": "hidden observed-GM labels; source labels; post-fit branch selection; MISSING_PARENT_BREF_RULE",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "SIS1000_3_MHref",
            "field": "M_H_ref",
            "required_input": "finite positive denominator in the same reference frame as Delta_ref",
            "units_requirement": "M_H_ref_units required",
            "source_requirement": "definition source path and equation_ref required",
            "rejects": "orbital-GM import; fitted denominator; MISSING_M_H_REF",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "SIS1000_4_theorem_zero_switch",
            "field": "theorem_zero_authority",
            "required_input": "PARENT_SIGNED_TRUE if theorem_zero=true",
            "units_requirement": "units still recorded for the zeroed derivative slot",
            "source_requirement": "parent theorem path, selector equation, and component certificate",
            "rejects": "zero-by-closure; notation-zero; silence of the boundary projector",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "SIS1000_5_no_cancellation",
            "field": "no_cancellation_guard",
            "required_input": "ABS_PRODUCT_NO_SIGN_CANCELLATION",
            "units_requirement": "absolute finite ratio abs(partial_source_Delta_ref * Delta_source_scale) / M_H_ref",
            "source_requirement": "no sign cancellation may be used to pass a local bound",
            "rejects": "opposite-sign cancellation; tuned cancellation; branch cancellation",
            "valid_for_claim": "false",
        },
    ]


def candidate_input_template_rows() -> list[dict[str, str]]:
    base = {
        "system_id": "R10_local_reference_branch",
        "target": "Delta_ref_source_component_over_MH",
        "formula": "abs(partial_source_Delta_ref * Delta_source_scale)/M_H_ref",
        "source_parameter": "MISSING_SOURCE_PARAMETER",
        "Delta_source_scale": "MISSING_SOURCE_SCALE",
        "Delta_source_scale_units": "MISSING_SOURCE_SCALE_UNITS",
        "partial_source_Delta_ref": "MISSING_NUMERIC_DERIVATIVE_OR_THEOREM_ZERO",
        "partial_source_units": "MISSING_PARTIAL_SOURCE_UNITS",
        "Delta_ref_units": "MISSING_DELTA_REF_UNITS",
        "M_H_ref": "MISSING_M_H_REF",
        "M_H_ref_units": "MISSING_M_H_REF_UNITS",
        "B_ref_rule": "MISSING_PARENT_BREF_RULE",
        "fixed_branch_id": "MISSING_FIXED_BRANCH_ID",
        "source_path": "MISSING_SOURCE_FILE",
        "equation_ref": "MISSING_EQUATION_REF",
        "theorem_zero": "false",
        "theorem_zero_authority": "MISSING_PARENT_SIGNATURE",
        "no_cancellation_guard": "MISSING_ABSOLUTE_PRODUCT_GUARD",
        "valid_for_claim": "false",
    }
    rows: list[dict[str, str]] = []
    variants = [
        ("CIR1000_0_missing_derivative", "derivative slot has no finite number and no parent-signed zero theorem"),
        ("CIR1000_1_missing_scale", "source scale is not defined or sourced"),
        ("CIR1000_2_missing_Bref_rule", "B_ref rule is not fixed by parent branch selector"),
        ("CIR1000_3_missing_MHref", "same-frame positive M_H_ref denominator is missing"),
        ("CIR1000_4_zero_switch_missing_parent_signature", "theorem-zero switch is requested without PARENT_SIGNED_TRUE"),
        ("CIR1000_5_all_missing_live_placeholder", "live row remains placeholder-only and cannot be scored"),
    ]
    for row_id, purpose in variants:
        row = {**base, "candidate_id": row_id, "purpose": purpose}
        if row_id == "CIR1000_4_zero_switch_missing_parent_signature":
            row["theorem_zero"] = "true"
            row["theorem_zero_authority"] = "MISSING_PARENT_SIGNATURE"
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


def path_exists(value: str) -> bool:
    if is_missing(value):
        return False
    path = Path(value)
    if not path.is_absolute():
        path = ROOT / value
    return path.exists()


def evaluate_candidate(row: dict[str, str]) -> dict[str, str]:
    reasons: list[str] = []
    derivative_ok, derivative_value = finite_float(row.get("partial_source_Delta_ref", ""))
    theorem_zero = row.get("theorem_zero", "").strip().lower() == "true"
    parent_signed_zero = theorem_zero and row.get("theorem_zero_authority") == "PARENT_SIGNED_TRUE"
    if not derivative_ok and not parent_signed_zero:
        reasons.append("MISSING_NUMERIC_DERIVATIVE_OR_PARENT_SIGNED_ZERO")
    if theorem_zero and not parent_signed_zero:
        reasons.append("THEOREM_ZERO_REJECTED_WITHOUT_PARENT_SIGNED_TRUE")
    scale_ok, scale_value = finite_float(row.get("Delta_source_scale", ""))
    if not scale_ok or scale_value is None or scale_value <= 0:
        reasons.append("MISSING_POSITIVE_DELTA_SOURCE_SCALE")
    mh_ok, mh_value = finite_float(row.get("M_H_ref", ""))
    if not mh_ok or mh_value is None or mh_value <= 0:
        reasons.append("MISSING_POSITIVE_SAME_FRAME_M_H_REF")
    for field in ["source_parameter", "Delta_source_scale_units", "partial_source_units", "Delta_ref_units", "M_H_ref_units", "equation_ref", "fixed_branch_id"]:
        if is_missing(row.get(field, "")):
            reasons.append(f"MISSING_{field.upper()}")
    bref_rule = row.get("B_ref_rule", "")
    if is_missing(bref_rule):
        reasons.append("MISSING_PARENT_BREF_RULE")
    forbidden = ["GM", "source", "observed", "fit", "calibration"]
    if not is_missing(bref_rule) and any(token.lower() in bref_rule.lower() for token in forbidden):
        reasons.append("BREF_RULE_CONTAINS_FORBIDDEN_SOURCE_OR_FIT_LABEL")
    if not path_exists(row.get("source_path", "")):
        reasons.append("MISSING_EXISTING_SOURCE_PATH")
    if row.get("no_cancellation_guard") != "ABS_PRODUCT_NO_SIGN_CANCELLATION":
        reasons.append("MISSING_NO_CANCELLATION_GUARD")
    if row.get("valid_for_claim") != "true":
        reasons.append("VALID_FOR_CLAIM_FALSE")
    numeric_ratio = "NOT_SCORED"
    if not reasons and derivative_value is not None and scale_value is not None and mh_value is not None:
        numeric_ratio = f"{abs(derivative_value * scale_value) / mh_value:.16e}"
    verdict = "ACCEPT_NUMERIC_OR_PARENT_SIGNED_ZERO" if not reasons else "REFUSED_MISSING_PROVENANCE_OR_PARENT_SELECTOR"
    return {
        "runner_id": row["candidate_id"].replace("CIR", "RUN"),
        "candidate_id": row["candidate_id"],
        "target": row["target"],
        "verdict": verdict,
        "score_ready": flag(not reasons),
        "claim_allowed": flag(False),
        "valid_for_claim": flag(False),
        "computed_abs_ratio": numeric_ratio,
        "failure_reasons": ";".join(reasons) if reasons else "none",
        "generated_utc": stamp(),
    }


def strict_runner_rows(candidates: list[dict[str, str]]) -> list[dict[str, str]]:
    return [evaluate_candidate(row) for row in candidates]


def refusal_ledger_rows(runner: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for run in runner:
        rows.append(
            {
                "refusal_id": run["runner_id"].replace("RUN", "REF"),
                "candidate_id": run["candidate_id"],
                "refusal": run["verdict"],
                "why": run["failure_reasons"],
                "required_exit": "finite sourced coefficient provenance or parent-signed theorem-zero selector",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            }
        )
    return rows


def claim_gate_rows(runner: list[dict[str, str]]) -> list[dict[str, str]]:
    blocked = all(row["verdict"] == "REFUSED_MISSING_PROVENANCE_OR_PARENT_SELECTOR" for row in runner)
    return [
        {
            "gate_id": "CG1000_0_Delta_ref_source_component",
            "claim": "Delta_ref source component is zero or locally bounded",
            "gate_pass": "false",
            "reason": "strict runner refuses every current placeholder row",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1000_1_RC994_0",
            "claim": "RC994_0 residual current passes",
            "gate_pass": "false",
            "reason": "Delta_ref source component remains unsigned and unbounded",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1000_2_FB554_0_local_GR",
            "claim": "FB554_0/local-GR branch passes",
            "gate_pass": "false",
            "reason": "local R10 residual source coefficient is still blocked",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1000_3_runner_guardrail",
            "claim": "runner enforces no zero-by-closure and no hidden cancellation",
            "gate_pass": flag(blocked),
            "reason": "all current rows are refused unless strict provenance or parent theorem appears",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1000_0_runner_installed",
            "decision": "keep current Delta_ref source rows nonclaim",
            "reason": "the runner now blocks missing derivative, scale, B_ref rule, M_H_ref, source path, theorem-zero authority, and cancellation guard",
            "effect": "future rows can be smoke-tested without accidentally promoting R10/local-GR claims",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1000_1_no_theorem_zero_without_parent",
            "decision": "do not accept theorem_zero=true unless theorem_zero_authority=PARENT_SIGNED_TRUE",
            "reason": "closure preference and notation silence are not derivations",
            "effect": "zero proof must be supplied by a parent action selector or component certificate",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1000_2_next_derivative_target",
            "decision": "move from source derivative to radial/surface derivative route",
            "reason": "997 identifies remaining derivative components; 1000 has guarded the source component",
            "effect": "1001 should try the radius/surface-term theorem or stage a radial-profile source row",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1001-Y5-R10-Bref-radius-surface-term-theorem-or-Delta-ref-radial-profile-row.md",
            "objective": "derive the radius/surface contribution to Delta_ref as zero, or stage a source-backed radial profile row without claiming a pass",
            "include": "partial_r Delta_ref, boundary surface term, radial profile, same-frame M_H_ref, source/equation paths, no-cancellation guard",
            "exclude": "zero-by-boundary-silence, fitted radius profile, RC994_0 pass, FB554_0 pass, local-GR claim, GitHub action",
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
    schema: list[dict[str, str]],
    candidates: list[dict[str, str]],
    runner: list[dict[str, str]],
    refusals: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    required_fields = {
        "partial_source_Delta_ref",
        "Delta_source_scale",
        "B_ref_rule",
        "M_H_ref",
        "theorem_zero_authority",
        "no_cancellation_guard",
    }
    schema_ok = required_fields.issubset({row["field"] for row in schema})
    candidates_ok = all(row["valid_for_claim"] == "false" for row in candidates) and len(candidates) >= 6
    runner_ok = all(row["verdict"] == "REFUSED_MISSING_PROVENANCE_OR_PARENT_SELECTOR" and row["score_ready"] == "false" for row in runner)
    theorem_switch_ok = any(
        row["candidate_id"] == "CIR1000_4_zero_switch_missing_parent_signature"
        and "THEOREM_ZERO_REJECTED_WITHOUT_PARENT_SIGNED_TRUE" in row["failure_reasons"]
        for row in runner
    )
    refusal_ok = len(refusals) == len(runner) and all(row["claim_allowed"] == "false" for row in refusals)
    claims_ok = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in claims)
    decisions_ok = any(row["decision_id"] == "DEC1000_2_next_derivative_target" for row in decisions)
    next_ok = bool(next_target) and next_target[0]["valid_for_claim"] == "false"
    formalization_count = formalization_changed_after_start()
    checks = [
        {"check_id": "V1000_0_sources_exist", "result": "pass" if sources_ok else "fail", "detail": "all source paths exist and needles are present"},
        {"check_id": "V1000_1_schema_core_fields", "result": "pass" if schema_ok else "fail", "detail": "strict schema includes derivative, scale, B_ref, M_H_ref, theorem-zero, and no-cancellation fields"},
        {"check_id": "V1000_2_candidate_rows_nonclaim", "result": "pass" if candidates_ok else "fail", "detail": "candidate template rows remain valid_for_claim=false"},
        {"check_id": "V1000_3_runner_refuses_placeholders", "result": "pass" if runner_ok else "fail", "detail": "runner refuses every current placeholder row"},
        {"check_id": "V1000_4_theorem_zero_guard", "result": "pass" if theorem_switch_ok else "fail", "detail": "theorem_zero=true is refused without PARENT_SIGNED_TRUE"},
        {"check_id": "V1000_5_refusal_ledger_nonclaim", "result": "pass" if refusal_ok else "fail", "detail": "refusal ledger mirrors runner and keeps claims false"},
        {"check_id": "V1000_6_claim_gates_blocked", "result": "pass" if claims_ok else "fail", "detail": "Delta_ref, RC994_0, FB554_0, and local-GR claims stay blocked"},
        {"check_id": "V1000_7_decision_written", "result": "pass" if decisions_ok else "fail", "detail": "next derivative target decision is written"},
        {"check_id": "V1000_8_next_target_written", "result": "pass" if next_ok else "fail", "detail": "1001 target row is present and nonclaim"},
        {"check_id": "V1000_9_formalization_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization-workbench modified-file count since script start is {formalization_count}"},
    ]
    ready = all(row["result"] == "pass" for row in checks)
    checks.append(
        {
            "check_id": "V1000_SUMMARY",
            "result": "pass" if ready else "fail",
            "detail": "1000 strict provenance runner validation summary",
            "generated_utc": stamp(),
        }
    )
    for row in checks:
        row.setdefault("generated_utc", stamp())
    return checks


def write_doc(
    sources: list[dict[str, str]],
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
        "# 1000 Y5 R10 Delta-ref Source Coefficient Strict Provenance Runner",
        "",
        "**Status:** strict refusal runner installed; no Delta_ref, RC994_0, FB554_0, R10, PPN, or local-GR pass is claimed.",
        "",
        "**Claim ceiling:** this checkpoint is plumbing only. It makes the source coefficient harder to fake; it does not solve the coefficient.",
        "",
        "## Source Register",
        "",
        md_table(sources, ["source_id", "path", "role", "needle", "exists", "needle_found", "valid_for_claim"]),
        "",
        "## Strict Input Schema",
        "",
        md_table(schema, ["schema_id", "field", "required_input", "units_requirement", "source_requirement", "rejects", "valid_for_claim"]),
        "",
        "## Candidate Input Template",
        "",
        md_table(candidates, ["candidate_id", "purpose", "target", "formula", "partial_source_Delta_ref", "Delta_source_scale", "B_ref_rule", "M_H_ref", "theorem_zero", "theorem_zero_authority", "no_cancellation_guard", "valid_for_claim"]),
        "",
        "## Strict Provenance Runner",
        "",
        md_table(runner, ["runner_id", "candidate_id", "verdict", "score_ready", "claim_allowed", "computed_abs_ratio", "failure_reasons", "generated_utc"]),
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
    schema = strict_schema_rows()
    candidates = candidate_input_template_rows()
    runner = strict_runner_rows(candidates)
    refusals = refusal_ledger_rows(runner)
    claims = claim_gate_rows(runner)
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, schema, candidates, runner, refusals, claims, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_1000_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_1000_STRICT_INPUT_SCHEMA.csv", schema)
    write_csv(OUT / "P8_Y5_R10_1000_CANDIDATE_INPUT_TEMPLATE.csv", candidates)
    write_csv(OUT / "P8_Y5_R10_1000_STRICT_PROVENANCE_RUNNER.csv", runner)
    write_csv(OUT / "P8_Y5_R10_1000_REFUSAL_LEDGER.csv", refusals)
    write_csv(OUT / "P8_Y5_R10_1000_CLAIM_GATE.csv", claims)
    write_csv(OUT / "P8_Y5_R10_1000_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1000_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_1000_VALIDATION.csv", validation)
    write_doc(sources, schema, candidates, runner, refusals, claims, decisions, validation, next_target)


if __name__ == "__main__":
    main()
