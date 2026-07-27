from __future__ import annotations

import csv
import math
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1001-Y5-R10-Bref-radius-surface-term-theorem-or-Delta-ref-radial-profile-row.md"
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
            "source_id": "S1001_0_handoff_doc",
            "path": "1000-Y5-R10-Delta-ref-source-coefficient-strict-provenance-runner.md",
            "role": "1000 handoff selecting radial/surface-term target",
            "needle": "1001-Y5-R10-Bref-radius-surface-term-theorem-or-Delta-ref-radial-profile-row.md",
        },
        {
            "source_id": "S1001_1_next_target",
            "path": "source-intake/mts_residuals/P8_Y5_R10_1000_NEXT_TARGET.csv",
            "role": "machine-readable 1001 target",
            "needle": "partial_r Delta_ref",
        },
        {
            "source_id": "S1001_2_derivative_audit",
            "path": "source-intake/mts_residuals/P8_Y5_R10_997_DERIVATIVE_COMPONENT_AUDIT.csv",
            "role": "radial derivative blocker from 997",
            "needle": "DVC997_1_radius",
        },
        {
            "source_id": "S1001_3_no_cancellation",
            "path": "source-intake/mts_residuals/P8_Y5_R10_994_DELTAH_NO_CANCELLATION_ENVELOPE.csv",
            "role": "absolute residual envelope",
            "needle": "DHE994_1_no_cancellation",
        },
        {
            "source_id": "S1001_4_strict_runner",
            "path": "source-intake/mts_residuals/P8_Y5_R10_1000_STRICT_PROVENANCE_RUNNER.csv",
            "role": "precedent for refusing missing provenance",
            "needle": "REFUSED_MISSING_PROVENANCE_OR_PARENT_SELECTOR",
        },
        {
            "source_id": "S1001_5_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_1000_VALIDATION.csv",
            "role": "1000 validation pass",
            "needle": "V1000_SUMMARY",
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


def radius_theorem_audit_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "RSA1001_0_quantity",
            "object": "partial_r Delta_ref",
            "needed_for_zero": "Delta_ref[S_r] must be independent of allowed radial deformations of the comparison surface S_r",
            "current_evidence": "997 flags MISSING_SURFACE_CLASS_OR_RADIAL_PROFILE",
            "status": "blocked_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "RSA1001_1_surface_class",
            "object": "radial surface family S_r",
            "needed_for_zero": "parent action supplies a fixed homology/cohomology class with fixed corners and no leakage through the radial annulus",
            "current_evidence": "MISSING_PARENT_SURFACE_CLASS",
            "status": "unsigned",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "RSA1001_2_stokes_route",
            "object": "integral_S_r B_ref",
            "needed_for_zero": "dB_ref=0 on the annulus and corner terms vanish, so d/dr integral_S_r B_ref = integral_boundary_annulus B_ref + integral_annulus dB_ref = 0",
            "current_evidence": "MISSING_CLOSED_BREF_AND_CORNER_CERTIFICATE",
            "status": "conditional_only",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "RSA1001_3_surface_deformation",
            "object": "Lie_n B_ref",
            "needed_for_zero": "radial deformation vector n maps to gauge/exact variation or a proven zero physical flux",
            "current_evidence": "MISSING_RADIAL_DEFORMATION_RULE",
            "status": "unsigned",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "RSA1001_4_reference_charge",
            "object": "reference charge between linked surfaces",
            "needed_for_zero": "no source charge is crossed and B_ref is not retuned as r changes",
            "current_evidence": "MISSING_NO_CROSSED_SOURCE_AND_NO_RETUNE_CERTIFICATE",
            "status": "unsigned",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "RSA1001_5_theorem_verdict",
            "object": "partial_r Delta_ref = 0",
            "needed_for_zero": "all surface-class, closed-form, corner, deformation, and no-retune clauses parent-signed",
            "current_evidence": "not enough parent geometry to promote zero",
            "status": "fail_current_claim",
            "valid_for_claim": "false",
        },
    ]


def radial_profile_schema_rows() -> list[dict[str, str]]:
    return [
        {
            "schema_id": "RPS1001_0_profile_formula",
            "target": "Delta_ref_radial_profile_over_MH",
            "formula": "abs(partial_r_Delta_ref * Delta_r_profile)/M_H_ref",
            "required_columns": "surface_id;r_parameter;Delta_r_profile;partial_r_Delta_ref;Delta_ref_units;M_H_ref;M_H_ref_units;surface_class_id;B_ref_rule;corner_condition;source_path;equation_ref;valid_for_claim",
            "acceptance_rule": "finite same-frame ratio or theorem_zero=true with parent-signed surface theorem; no MISSING markers",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "RPS1001_1_surface_theorem_switch",
            "target": "partial_r_Delta_ref_zero",
            "formula": "theorem_zero=true iff surface_zero_authority=PARENT_SIGNED_SURFACE_CLASS_TRUE",
            "required_columns": "surface_class_id;closed_B_ref_certificate;corner_certificate;radial_deformation_rule;no_retune_certificate;source_path;equation_ref",
            "acceptance_rule": "zero-by-boundary-silence and zero-by-fixed-radius are rejected",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "RPS1001_2_no_cancellation",
            "target": "radial contribution to residual envelope",
            "formula": "absolute values only",
            "required_columns": "no_cancellation_guard=ABS_PRODUCT_NO_SIGN_CANCELLATION",
            "acceptance_rule": "no sign cancellation, branch cancellation, or fitted radius cancellation",
            "valid_for_claim": "false",
        },
    ]


def candidate_profile_rows() -> list[dict[str, str]]:
    base = {
        "surface_id": "MISSING_SURFACE_ID",
        "r_parameter": "MISSING_R_PARAMETER",
        "Delta_r_profile": "MISSING_DELTA_R_PROFILE",
        "Delta_r_units": "MISSING_DELTA_R_UNITS",
        "partial_r_Delta_ref": "MISSING_PARTIAL_R_DELTA_REF",
        "partial_r_units": "MISSING_PARTIAL_R_UNITS",
        "Delta_ref_units": "MISSING_DELTA_REF_UNITS",
        "M_H_ref": "MISSING_M_H_REF",
        "M_H_ref_units": "MISSING_M_H_REF_UNITS",
        "surface_class_id": "MISSING_SURFACE_CLASS_ID",
        "closed_B_ref_certificate": "MISSING_CLOSED_BREF_CERTIFICATE",
        "corner_certificate": "MISSING_CORNER_CERTIFICATE",
        "radial_deformation_rule": "MISSING_RADIAL_DEFORMATION_RULE",
        "no_retune_certificate": "MISSING_NO_RETUNE_CERTIFICATE",
        "B_ref_rule": "MISSING_PARENT_BREF_RULE",
        "source_path": "MISSING_SOURCE_FILE",
        "equation_ref": "MISSING_EQUATION_REF",
        "theorem_zero": "false",
        "surface_zero_authority": "MISSING_PARENT_SURFACE_SIGNATURE",
        "no_cancellation_guard": "MISSING_ABSOLUTE_PRODUCT_GUARD",
        "valid_for_claim": "false",
    }
    variants = [
        ("RPT1001_0_missing_surface_class", "surface class/corner/annulus theorem is absent"),
        ("RPT1001_1_missing_radial_derivative", "partial_r Delta_ref is not a finite sourced derivative"),
        ("RPT1001_2_missing_radial_profile", "Delta_r profile is not sourced"),
        ("RPT1001_3_missing_MHref", "positive same-frame M_H_ref denominator is missing"),
        ("RPT1001_4_zero_switch_unsigned", "theorem-zero switch is requested without parent-signed surface class"),
        ("RPT1001_5_all_missing_live_placeholder", "live radial row is schema-only and cannot be scored"),
    ]
    rows: list[dict[str, str]] = []
    for row_id, purpose in variants:
        row = {**base, "candidate_id": row_id, "target": "Delta_ref_radial_profile_over_MH", "purpose": purpose}
        if row_id == "RPT1001_4_zero_switch_unsigned":
            row["theorem_zero"] = "true"
            row["surface_zero_authority"] = "MISSING_PARENT_SURFACE_SIGNATURE"
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


def evaluate_profile(row: dict[str, str]) -> dict[str, str]:
    reasons: list[str] = []
    derivative_ok, derivative = finite_float(row.get("partial_r_Delta_ref", ""))
    theorem_zero = row.get("theorem_zero", "").strip().lower() == "true"
    parent_signed_surface_zero = theorem_zero and row.get("surface_zero_authority") == "PARENT_SIGNED_SURFACE_CLASS_TRUE"
    if not derivative_ok and not parent_signed_surface_zero:
        reasons.append("MISSING_PARTIAL_R_DELTA_REF_OR_PARENT_SIGNED_SURFACE_ZERO")
    if theorem_zero and not parent_signed_surface_zero:
        reasons.append("THEOREM_ZERO_REJECTED_WITHOUT_PARENT_SIGNED_SURFACE_CLASS")
    delta_r_ok, delta_r = finite_float(row.get("Delta_r_profile", ""))
    if not delta_r_ok or delta_r is None or delta_r <= 0:
        reasons.append("MISSING_POSITIVE_DELTA_R_PROFILE")
    mh_ok, mh = finite_float(row.get("M_H_ref", ""))
    if not mh_ok or mh is None or mh <= 0:
        reasons.append("MISSING_POSITIVE_SAME_FRAME_M_H_REF")
    for field in [
        "surface_id",
        "r_parameter",
        "Delta_r_units",
        "partial_r_units",
        "Delta_ref_units",
        "M_H_ref_units",
        "surface_class_id",
        "closed_B_ref_certificate",
        "corner_certificate",
        "radial_deformation_rule",
        "no_retune_certificate",
        "equation_ref",
    ]:
        if is_missing(row.get(field, "")):
            reasons.append(f"MISSING_{field.upper()}")
    if is_missing(row.get("B_ref_rule", "")):
        reasons.append("MISSING_PARENT_BREF_RULE")
    if not path_exists(row.get("source_path", "")):
        reasons.append("MISSING_EXISTING_SOURCE_PATH")
    if row.get("no_cancellation_guard") != "ABS_PRODUCT_NO_SIGN_CANCELLATION":
        reasons.append("MISSING_NO_CANCELLATION_GUARD")
    if row.get("valid_for_claim") != "true":
        reasons.append("VALID_FOR_CLAIM_FALSE")
    numeric_ratio = "NOT_SCORED"
    if not reasons and derivative is not None and delta_r is not None and mh is not None:
        numeric_ratio = f"{abs(derivative * delta_r) / mh:.16e}"
    verdict = "ACCEPT_NUMERIC_OR_PARENT_SIGNED_SURFACE_ZERO" if not reasons else "REFUSED_MISSING_RADIAL_SURFACE_PROVENANCE"
    return {
        "runner_id": row["candidate_id"].replace("RPT", "RPR"),
        "candidate_id": row["candidate_id"],
        "target": row["target"],
        "verdict": verdict,
        "score_ready": flag(not reasons),
        "claim_allowed": "false",
        "valid_for_claim": "false",
        "computed_abs_ratio": numeric_ratio,
        "failure_reasons": ";".join(reasons) if reasons else "none",
        "generated_utc": stamp(),
    }


def radial_profile_runner_rows(candidates: list[dict[str, str]]) -> list[dict[str, str]]:
    return [evaluate_profile(row) for row in candidates]


def refusal_ledger_rows(runner: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        {
            "refusal_id": row["runner_id"].replace("RPR", "RRF"),
            "candidate_id": row["candidate_id"],
            "refusal": row["verdict"],
            "why": row["failure_reasons"],
            "required_exit": "parent-signed surface theorem or finite radial-profile coefficient with units/source/equation path",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        }
        for row in runner
    ]


def claim_gate_rows(runner: list[dict[str, str]], theorem: list[dict[str, str]]) -> list[dict[str, str]]:
    runner_refuses = all(row["verdict"] == "REFUSED_MISSING_RADIAL_SURFACE_PROVENANCE" for row in runner)
    theorem_fails = any(row["audit_id"] == "RSA1001_5_theorem_verdict" and row["status"] == "fail_current_claim" for row in theorem)
    return [
        {
            "gate_id": "CG1001_0_partial_r_Delta_ref_zero",
            "claim": "partial_r Delta_ref = 0",
            "gate_pass": "false",
            "reason": "surface class, closed B_ref, corner, deformation, and no-retune clauses are not parent-signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1001_1_Delta_ref_radial_profile_bound",
            "claim": "Delta_ref_radial_profile_over_MH is bounded",
            "gate_pass": "false",
            "reason": "radial derivative/profile/M_H_ref inputs are placeholder-only",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1001_2_RC994_0",
            "claim": "RC994_0 residual current passes",
            "gate_pass": "false",
            "reason": "radial source term is blocked, and source/time/frame/lambda terms remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1001_3_local_GR_branch",
            "claim": "local-GR branch passes",
            "gate_pass": "false",
            "reason": "R10 residual vector is not zero or source-bounded",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1001_4_guardrail",
            "claim": "radius/surface guardrail is installed",
            "gate_pass": flag(runner_refuses and theorem_fails),
            "reason": "theorem is not promoted and all placeholder rows are refused",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1001_0_theorem_not_closed",
            "decision": "do not claim partial_r Delta_ref = 0",
            "reason": "Stokes/homology route is viable only conditionally; parent surface class and corner certificates are absent",
            "effect": "radial piece remains a nonclaim closure or source-bound input",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1001_1_radial_profile_staged",
            "decision": "stage Delta_ref_radial_profile_over_MH as the fallback row",
            "reason": "if the zero theorem cannot be closed, the only honest route is a sourced radial profile with units and no-cancellation",
            "effect": "future data/proof can fill the row without weakening the gate",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1001_2_next_derivative_target",
            "decision": "move to stationary tau/time derivative",
            "reason": "997 lists partial_t Delta_ref as the next derivative component after source and radius",
            "effect": "1002 should try L_tau B_ref=0 or stage Delta_ref_time_profile_over_MH",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1002-Y5-R10-Bref-stationary-tau-theorem-or-Delta-ref-time-profile-row.md",
            "objective": "derive L_tau B_ref=0 under the charge/clock/readout tau, or stage a source-backed time-profile row without claiming a pass",
            "include": "partial_t Delta_ref, L_tau B_ref, tau/readout identity, clock compatibility, M_H_ref, source/equation paths, no-cancellation guard",
            "exclude": "stationary-by-assumption, fitted clock drift, Gdot claim, RC994_0 pass, FB554_0 pass, local-GR claim, GitHub action",
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
    theorem: list[dict[str, str]],
    schema: list[dict[str, str]],
    candidates: list[dict[str, str]],
    runner: list[dict[str, str]],
    refusals: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    theorem_ok = any(row["audit_id"] == "RSA1001_5_theorem_verdict" and row["status"] == "fail_current_claim" for row in theorem) and all(row["valid_for_claim"] == "false" for row in theorem)
    schema_ok = any(row["target"] == "Delta_ref_radial_profile_over_MH" for row in schema) and any("theorem_zero=true" in row["formula"] for row in schema)
    candidates_ok = len(candidates) >= 6 and all(row["valid_for_claim"] == "false" for row in candidates)
    runner_ok = all(row["verdict"] == "REFUSED_MISSING_RADIAL_SURFACE_PROVENANCE" and row["score_ready"] == "false" for row in runner)
    zero_switch_ok = any(
        row["candidate_id"] == "RPT1001_4_zero_switch_unsigned"
        and "THEOREM_ZERO_REJECTED_WITHOUT_PARENT_SIGNED_SURFACE_CLASS" in row["failure_reasons"]
        for row in runner
    )
    refusals_ok = len(refusals) == len(runner) and all(row["claim_allowed"] == "false" for row in refusals)
    claims_ok = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in claims)
    decisions_ok = any(row["decision_id"] == "DEC1001_2_next_derivative_target" for row in decisions)
    next_ok = bool(next_target) and next_target[0]["valid_for_claim"] == "false"
    formalization_count = formalization_changed_after_start()
    checks = [
        {"check_id": "V1001_0_sources_exist", "result": "pass" if sources_ok else "fail", "detail": "all source paths exist and needles are present"},
        {"check_id": "V1001_1_theorem_audit_nonclaim", "result": "pass" if theorem_ok else "fail", "detail": "radial zero theorem remains blocked rather than promoted"},
        {"check_id": "V1001_2_schema_ready", "result": "pass" if schema_ok else "fail", "detail": "radial profile and theorem-zero schema rows are present"},
        {"check_id": "V1001_3_candidate_rows_nonclaim", "result": "pass" if candidates_ok else "fail", "detail": "candidate rows remain valid_for_claim=false"},
        {"check_id": "V1001_4_runner_refuses_placeholders", "result": "pass" if runner_ok else "fail", "detail": "runner refuses every current radial placeholder row"},
        {"check_id": "V1001_5_surface_zero_guard", "result": "pass" if zero_switch_ok else "fail", "detail": "theorem_zero=true is refused without PARENT_SIGNED_SURFACE_CLASS_TRUE"},
        {"check_id": "V1001_6_refusal_ledger_nonclaim", "result": "pass" if refusals_ok else "fail", "detail": "refusal ledger mirrors runner and keeps claims false"},
        {"check_id": "V1001_7_claim_gates_blocked", "result": "pass" if claims_ok else "fail", "detail": "radial, RC994_0, and local-GR claims stay blocked"},
        {"check_id": "V1001_8_decision_written", "result": "pass" if decisions_ok else "fail", "detail": "stationary tau/time derivative target decision is written"},
        {"check_id": "V1001_9_next_target_written", "result": "pass" if next_ok else "fail", "detail": "1002 target row is present and nonclaim"},
        {"check_id": "V1001_10_formalization_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization-workbench modified-file count since script start is {formalization_count}"},
    ]
    ready = all(row["result"] == "pass" for row in checks)
    checks.append(
        {
            "check_id": "V1001_SUMMARY",
            "result": "pass" if ready else "fail",
            "detail": "1001 radial/surface theorem and profile-row validation summary",
            "generated_utc": stamp(),
        }
    )
    for row in checks:
        row.setdefault("generated_utc", stamp())
    return checks


def write_doc(
    sources: list[dict[str, str]],
    theorem: list[dict[str, str]],
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
        "# 1001 Y5 R10 B-ref Radius Surface-Term Theorem Or Delta-ref Radial Profile Row",
        "",
        "**Status:** radial/surface zero theorem attempted, not closed; fallback radial-profile row staged as nonclaim.",
        "",
        "**Claim ceiling:** this checkpoint does not claim partial_r Delta_ref=0, RC994_0, FB554_0, R10, PPN, or local-GR pass.",
        "",
        "## Source Register",
        "",
        md_table(sources, ["source_id", "path", "role", "needle", "exists", "needle_found", "valid_for_claim"]),
        "",
        "## Radius Surface Theorem Audit",
        "",
        md_table(theorem, ["audit_id", "object", "needed_for_zero", "current_evidence", "status", "valid_for_claim"]),
        "",
        "## Radial Profile Schema",
        "",
        md_table(schema, ["schema_id", "target", "formula", "required_columns", "acceptance_rule", "valid_for_claim"]),
        "",
        "## Candidate Profile Template",
        "",
        md_table(candidates, ["candidate_id", "purpose", "target", "partial_r_Delta_ref", "Delta_r_profile", "M_H_ref", "surface_class_id", "theorem_zero", "surface_zero_authority", "no_cancellation_guard", "valid_for_claim"]),
        "",
        "## Radial Profile Runner",
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
    theorem = radius_theorem_audit_rows()
    schema = radial_profile_schema_rows()
    candidates = candidate_profile_rows()
    runner = radial_profile_runner_rows(candidates)
    refusals = refusal_ledger_rows(runner)
    claims = claim_gate_rows(runner, theorem)
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, theorem, schema, candidates, runner, refusals, claims, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_1001_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_1001_RADIUS_SURFACE_THEOREM_AUDIT.csv", theorem)
    write_csv(OUT / "P8_Y5_R10_1001_RADIAL_PROFILE_SCHEMA.csv", schema)
    write_csv(OUT / "P8_Y5_R10_1001_CANDIDATE_PROFILE_TEMPLATE.csv", candidates)
    write_csv(OUT / "P8_Y5_R10_1001_RADIAL_PROFILE_RUNNER.csv", runner)
    write_csv(OUT / "P8_Y5_R10_1001_REFUSAL_LEDGER.csv", refusals)
    write_csv(OUT / "P8_Y5_R10_1001_CLAIM_GATE.csv", claims)
    write_csv(OUT / "P8_Y5_R10_1001_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1001_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_1001_VALIDATION.csv", validation)
    write_doc(sources, theorem, schema, candidates, runner, refusals, claims, decisions, validation, next_target)


if __name__ == "__main__":
    main()
