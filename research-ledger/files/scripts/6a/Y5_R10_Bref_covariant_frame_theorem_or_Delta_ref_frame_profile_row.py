from __future__ import annotations

import csv
import math
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1003-Y5-R10-Bref-covariant-frame-theorem-or-Delta-ref-frame-profile-row.md"
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
            "source_id": "S1003_0_handoff_doc",
            "path": "1002-Y5-R10-Bref-stationary-tau-theorem-or-Delta-ref-time-profile-row.md",
            "role": "1002 handoff selecting covariant frame/coframe derivative target",
            "needle": "1003-Y5-R10-Bref-covariant-frame-theorem-or-Delta-ref-frame-profile-row.md",
        },
        {
            "source_id": "S1003_1_next_target",
            "path": "source-intake/mts_residuals/P8_Y5_R10_1002_NEXT_TARGET.csv",
            "role": "machine-readable 1003 target",
            "needle": "partial_frame Delta_ref",
        },
        {
            "source_id": "S1003_2_derivative_audit",
            "path": "source-intake/mts_residuals/P8_Y5_R10_997_DERIVATIVE_COMPONENT_AUDIT.csv",
            "role": "frame derivative blocker from 997",
            "needle": "DVC997_3_frame",
        },
        {
            "source_id": "S1003_3_same_coframe",
            "path": "source-intake/mts_residuals/P8_Y5_SAME_COFRAME_PARENT_CLAUSE.csv",
            "role": "same observed coframe parent clause",
            "needle": "UOC519_5_no_conformal_disformal_shadow_frame",
        },
        {
            "source_id": "S1003_4_frame_lock_contract",
            "path": "source-intake/mts_residuals/P8_Y5_R10_684_FRAME_LOCK_CONTRACT.csv",
            "role": "observed frame lock contract",
            "needle": "FLC684_6_verdict",
        },
        {
            "source_id": "S1003_5_source_frame_lock",
            "path": "source-intake/mts_residuals/P8_Y5_R10_942_SOURCE_FRAME_LOCK_AUDIT.csv",
            "role": "source/frame lock audit",
            "needle": "FRAME942_6_total_verdict",
        },
        {
            "source_id": "S1003_6_coframe_contract",
            "path": "source-intake/mts_residuals/P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv",
            "role": "coframe coupling parent contract",
            "needle": "CFC943_7_contract_verdict",
        },
        {
            "source_id": "S1003_7_frame_source_pack",
            "path": "source-intake/mts_residuals/P8_Y5_R10_943_FRAME_RESIDUAL_SOURCE_PACK.csv",
            "role": "frame/coupling residual source pack",
            "needle": "FRS943_7_epsilon_frame_coupling",
        },
        {
            "source_id": "S1003_8_frame_bound_pack",
            "path": "source-intake/mts_residuals/P8_Y5_R10_944_FRAME_LEAK_BOUND_PACK.csv",
            "role": "frame leak bound pack",
            "needle": "FLB944_7_epsilon_frame_leak",
        },
        {
            "source_id": "S1003_9_first_bound_rows",
            "path": "source-intake/mts_residuals/P8_Y5_R10_945_FIRST_FRAME_LEAK_BOUND_ROWS.csv",
            "role": "first frame leak bound rows",
            "needle": "BND945_7_score_gate",
        },
        {
            "source_id": "S1003_10_coframe_zero",
            "path": "source-intake/mts_residuals/P8_Y5_R10_863_COFRAME_ZERO_THEOREM.csv",
            "role": "conditional coframe chain-rule zero theorem",
            "needle": "CZT863_5_zero_verdict",
        },
        {
            "source_id": "S1003_11_no_cancellation",
            "path": "source-intake/mts_residuals/P8_Y5_R10_994_DELTAH_NO_CANCELLATION_ENVELOPE.csv",
            "role": "absolute residual envelope",
            "needle": "DHE994_1_no_cancellation",
        },
        {
            "source_id": "S1003_12_prior_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_1002_VALIDATION.csv",
            "role": "1002 validation pass",
            "needle": "V1002_SUMMARY",
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


def covariant_frame_theorem_audit_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "CFA1003_0_quantity",
            "object": "partial_frame Delta_ref",
            "needed_for_zero": "allowed frame/coframe changes must be gauge transformations of the same B_ref/H_ref charge, not physical matter-frame changes",
            "current_evidence": "997 flags MISSING_COVARIANT_COFRAME_REFERENCE_RULE",
            "status": "blocked_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "CFA1003_1_quotient_coframe_descent",
            "object": "e_obs(Phi)=Obs_e(q(Phi))",
            "needed_for_zero": "Dq(v_frame)=0 implies Lie_v e_obs=0 by chain rule",
            "current_evidence": "863 gives conditional proof, but parent must sign the local vertical directions",
            "status": "conditional_only",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "CFA1003_2_matter_functor",
            "object": "ordinary matter, clocks, rods, photons, and orbits",
            "needed_for_zero": "all ordinary readouts use the same descended coframe with no species/source frame split",
            "current_evidence": "519/684/943 write the contract but keep it not parent-derived",
            "status": "unsigned",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "CFA1003_3_Bref_Href_covariance",
            "object": "B_ref, H_ref, counterterms, and boundary class",
            "needed_for_zero": "reference subtraction is a covariant functional of e_obs and fixed boundary data, not a representative-frame convention",
            "current_evidence": "MISSING_COVARIANT_BREF_HREF_REFERENCE_RULE",
            "status": "unsigned",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "CFA1003_4_no_shadow_frame",
            "object": "Weyl/disformal/species/connection frame channels",
            "needed_for_zero": "no hidden A_g(X), B_g(X), m_A(X), non-Hilbert current, tau-normal, or support shift survives",
            "current_evidence": "942/943/944/945 retain frame leak rows with missing parent zero or numeric bounds",
            "status": "fallback_required",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "CFA1003_5_preferred_frame_ppn",
            "object": "preferred-frame leakage",
            "needed_for_zero": "frame changes must not induce PPN preferred-frame, WEP, clock, or R10 response",
            "current_evidence": "preferred-frame/source rows are staged but not source-backed",
            "status": "unsigned",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "CFA1003_6_theorem_verdict",
            "object": "partial_frame Delta_ref = 0",
            "needed_for_zero": "quotient coframe descent, matter functor, covariant B_ref/H_ref, no-shadow-frame, tau/support locks, and preferred-frame silence parent-signed",
            "current_evidence": "not enough parent coframe/reference geometry to promote zero",
            "status": "fail_current_claim",
            "valid_for_claim": "false",
        },
    ]


def frame_profile_schema_rows() -> list[dict[str, str]]:
    return [
        {
            "schema_id": "FPS1003_0_profile_formula",
            "target": "Delta_ref_frame_profile_over_MH",
            "formula": "abs(partial_frame_Delta_ref * Delta_frame_profile)/M_H_ref",
            "required_columns": "system_id;frame_parameter;frame_map_definition;Delta_frame_profile;partial_frame_Delta_ref;Delta_ref_units;M_H_ref;M_H_ref_units;coframe_descent_certificate;matter_functor_certificate;B_ref_covariance_certificate;H_ref_covariance_certificate;no_shadow_frame_certificate;source_path;equation_ref;valid_for_claim",
            "acceptance_rule": "finite same-frame ratio or theorem_zero=true with parent-signed covariant frame theorem; no MISSING markers",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "FPS1003_1_covariant_frame_zero_switch",
            "target": "partial_frame_Delta_ref_zero",
            "formula": "theorem_zero=true iff frame_zero_authority=PARENT_SIGNED_COVARIANT_FRAME_TRUE",
            "required_columns": "coframe_descent_certificate;matter_functor_certificate;B_ref_covariance_certificate;H_ref_covariance_certificate;no_shadow_frame_certificate;tau_normal_lock_certificate;support_equivalence_certificate;source_path;equation_ref",
            "acceptance_rule": "frame-choice-by-convention, gauge-wording, and preferred-frame silence-by-assumption are rejected",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "FPS1003_2_frame_leak_fallback",
            "target": "epsilon_frame_leak_to_frame_profile_bridge",
            "formula": "Delta_ref_frame_profile_over_MH <= C_frame * epsilon_frame_leak when C_frame and denominator are sourced",
            "required_columns": "epsilon_frame_leak;C_frame;c_g;b_dis;b_A;q_nonH;Delta_tau_n;Delta_W_support;M_H_ref;units;source_path;equation_ref",
            "acceptance_rule": "fallback is nonclaim until every retained frame component is numeric, sourced, same-frame, and absolute-summed",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "FPS1003_3_no_cancellation",
            "target": "frame contribution to residual envelope",
            "formula": "absolute values only",
            "required_columns": "no_cancellation_guard=ABS_PRODUCT_NO_SIGN_CANCELLATION",
            "acceptance_rule": "no sign cancellation, frame-transfer cancellation, or preferred-frame cancellation",
            "valid_for_claim": "false",
        },
    ]


def candidate_frame_profile_rows() -> list[dict[str, str]]:
    base = {
        "system_id": "R10_local_reference_branch",
        "frame_parameter": "MISSING_FRAME_PARAMETER",
        "frame_map_definition": "MISSING_FRAME_MAP_DEFINITION",
        "Delta_frame_profile": "MISSING_DELTA_FRAME_PROFILE",
        "Delta_frame_units": "MISSING_DELTA_FRAME_UNITS",
        "partial_frame_Delta_ref": "MISSING_PARTIAL_FRAME_DELTA_REF",
        "partial_frame_units": "MISSING_PARTIAL_FRAME_UNITS",
        "Delta_ref_units": "MISSING_DELTA_REF_UNITS",
        "M_H_ref": "MISSING_M_H_REF",
        "M_H_ref_units": "MISSING_M_H_REF_UNITS",
        "coframe_descent_certificate": "MISSING_COFRAME_DESCENT_CERTIFICATE",
        "matter_functor_certificate": "MISSING_MATTER_FUNCTOR_CERTIFICATE",
        "B_ref_covariance_certificate": "MISSING_B_REF_COVARIANCE_CERTIFICATE",
        "H_ref_covariance_certificate": "MISSING_H_REF_COVARIANCE_CERTIFICATE",
        "no_shadow_frame_certificate": "MISSING_NO_SHADOW_FRAME_CERTIFICATE",
        "tau_normal_lock_certificate": "MISSING_TAU_NORMAL_LOCK_CERTIFICATE",
        "support_equivalence_certificate": "MISSING_SUPPORT_EQUIVALENCE_CERTIFICATE",
        "source_path": "MISSING_SOURCE_FILE",
        "equation_ref": "MISSING_EQUATION_REF",
        "theorem_zero": "false",
        "frame_zero_authority": "MISSING_PARENT_FRAME_SIGNATURE",
        "epsilon_frame_leak": "MISSING_EPSILON_FRAME_LEAK",
        "C_frame": "MISSING_C_FRAME",
        "c_g": "MISSING_C_G",
        "b_dis": "MISSING_B_DIS",
        "b_A": "MISSING_B_A",
        "q_nonH": "MISSING_Q_NONH",
        "Delta_tau_n": "MISSING_DELTA_TAU_N",
        "Delta_W_support": "MISSING_DELTA_W_SUPPORT",
        "no_cancellation_guard": "MISSING_ABSOLUTE_PRODUCT_GUARD",
        "valid_for_claim": "false",
    }
    variants = [
        ("FPT1003_0_missing_coframe_descent", "coframe descent/quotient certificate is absent"),
        ("FPT1003_1_missing_frame_derivative", "partial_frame Delta_ref is not finite or theorem-zero"),
        ("FPT1003_2_missing_frame_profile", "Delta_frame profile is not sourced"),
        ("FPT1003_3_missing_MHref", "positive same-frame M_H_ref denominator is missing"),
        ("FPT1003_4_zero_switch_unsigned", "theorem-zero switch is requested without parent-signed covariant frame theorem"),
        ("FPT1003_5_missing_shadow_frame_guard", "no-shadow-frame and preferred-frame leakage guard is missing"),
        ("FPT1003_6_missing_frame_leak_fallback", "epsilon_frame_leak fallback components are not sourced"),
        ("FPT1003_7_all_missing_live_placeholder", "live frame row is schema-only and cannot be scored"),
    ]
    rows: list[dict[str, str]] = []
    for row_id, purpose in variants:
        row = {**base, "candidate_id": row_id, "target": "Delta_ref_frame_profile_over_MH", "purpose": purpose}
        if row_id == "FPT1003_4_zero_switch_unsigned":
            row["theorem_zero"] = "true"
            row["frame_zero_authority"] = "MISSING_PARENT_FRAME_SIGNATURE"
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


def evaluate_frame_profile(row: dict[str, str]) -> dict[str, str]:
    reasons: list[str] = []
    derivative_ok, derivative = finite_float(row.get("partial_frame_Delta_ref", ""))
    theorem_zero = row.get("theorem_zero", "").strip().lower() == "true"
    parent_signed_frame_zero = theorem_zero and row.get("frame_zero_authority") == "PARENT_SIGNED_COVARIANT_FRAME_TRUE"
    if not derivative_ok and not parent_signed_frame_zero:
        reasons.append("MISSING_PARTIAL_FRAME_DELTA_REF_OR_PARENT_SIGNED_COVARIANT_FRAME_ZERO")
    if theorem_zero and not parent_signed_frame_zero:
        reasons.append("THEOREM_ZERO_REJECTED_WITHOUT_PARENT_SIGNED_COVARIANT_FRAME")
    delta_frame_ok, delta_frame = finite_float(row.get("Delta_frame_profile", ""))
    if not delta_frame_ok or delta_frame is None or delta_frame <= 0:
        reasons.append("MISSING_POSITIVE_DELTA_FRAME_PROFILE")
    mh_ok, mh = finite_float(row.get("M_H_ref", ""))
    if not mh_ok or mh is None or mh <= 0:
        reasons.append("MISSING_POSITIVE_SAME_FRAME_M_H_REF")
    for field in [
        "system_id",
        "frame_parameter",
        "frame_map_definition",
        "Delta_frame_units",
        "partial_frame_units",
        "Delta_ref_units",
        "M_H_ref_units",
        "coframe_descent_certificate",
        "matter_functor_certificate",
        "B_ref_covariance_certificate",
        "H_ref_covariance_certificate",
        "no_shadow_frame_certificate",
        "tau_normal_lock_certificate",
        "support_equivalence_certificate",
        "equation_ref",
    ]:
        if is_missing(row.get(field, "")):
            reasons.append(f"MISSING_{field.upper()}")
    epsilon_ok, epsilon_value = finite_float(row.get("epsilon_frame_leak", ""))
    c_frame_ok, c_frame_value = finite_float(row.get("C_frame", ""))
    retained_components = ["c_g", "b_dis", "b_A", "q_nonH", "Delta_tau_n", "Delta_W_support"]
    retained_values_ok = True
    for field in retained_components:
        component_ok, component_value = finite_float(row.get(field, ""))
        if not component_ok or component_value is None:
            retained_values_ok = False
            reasons.append(f"MISSING_FRAME_LEAK_COMPONENT_{field.upper()}")
    if not parent_signed_frame_zero and not (
        epsilon_ok
        and c_frame_ok
        and epsilon_value is not None
        and c_frame_value is not None
        and epsilon_value >= 0
        and c_frame_value >= 0
        and retained_values_ok
    ):
        reasons.append("MISSING_EPSILON_FRAME_LEAK_FALLBACK_BOUND")
    if not path_exists(row.get("source_path", "")):
        reasons.append("MISSING_EXISTING_SOURCE_PATH")
    if row.get("no_cancellation_guard") != "ABS_PRODUCT_NO_SIGN_CANCELLATION":
        reasons.append("MISSING_NO_CANCELLATION_GUARD")
    if row.get("valid_for_claim") != "true":
        reasons.append("VALID_FOR_CLAIM_FALSE")
    numeric_ratio = "NOT_SCORED"
    if not reasons and derivative is not None and delta_frame is not None and mh is not None:
        numeric_ratio = f"{abs(derivative * delta_frame) / mh:.16e}"
    verdict = "ACCEPT_NUMERIC_OR_PARENT_SIGNED_COVARIANT_FRAME_ZERO" if not reasons else "REFUSED_MISSING_COVARIANT_FRAME_PROVENANCE"
    return {
        "runner_id": row["candidate_id"].replace("FPT", "FPR"),
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


def frame_profile_runner_rows(candidates: list[dict[str, str]]) -> list[dict[str, str]]:
    return [evaluate_frame_profile(row) for row in candidates]


def refusal_ledger_rows(runner: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        {
            "refusal_id": row["runner_id"].replace("FPR", "FRF"),
            "candidate_id": row["candidate_id"],
            "refusal": row["verdict"],
            "why": row["failure_reasons"],
            "required_exit": "parent-signed covariant frame theorem or finite frame-profile coefficient with epsilon_frame_leak fallback, units, source, and equation path",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        }
        for row in runner
    ]


def claim_gate_rows(runner: list[dict[str, str]], theorem: list[dict[str, str]]) -> list[dict[str, str]]:
    runner_refuses = all(row["verdict"] == "REFUSED_MISSING_COVARIANT_FRAME_PROVENANCE" for row in runner)
    theorem_fails = any(row["audit_id"] == "CFA1003_6_theorem_verdict" and row["status"] == "fail_current_claim" for row in theorem)
    return [
        {
            "gate_id": "CG1003_0_partial_frame_Delta_ref_zero",
            "claim": "partial_frame Delta_ref = 0",
            "gate_pass": "false",
            "reason": "coframe descent, matter functor, B_ref/H_ref covariance, no-shadow-frame, tau/support locks, and preferred-frame silence are unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1003_1_Delta_ref_frame_profile_bound",
            "claim": "Delta_ref_frame_profile_over_MH is bounded",
            "gate_pass": "false",
            "reason": "frame derivative/profile/M_H_ref/epsilon_frame inputs are placeholder-only",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1003_2_epsilon_frame_leak_bound",
            "claim": "epsilon_frame_leak supplies a valid fallback bound",
            "gate_pass": "false",
            "reason": "943/944/945 define retained channels but do not supply numeric same-frame source-backed values",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1003_3_RC994_0",
            "claim": "RC994_0 residual current passes",
            "gate_pass": "false",
            "reason": "frame derivative is blocked, and lambda/range piece remains open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1003_4_local_GR_branch",
            "claim": "local-GR branch passes",
            "gate_pass": "false",
            "reason": "R10 residual vector is not zero or source-bounded",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1003_5_guardrail",
            "claim": "covariant frame/coframe guardrail is installed",
            "gate_pass": flag(runner_refuses and theorem_fails),
            "reason": "theorem is not promoted and all placeholder rows are refused",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1003_0_theorem_not_closed",
            "decision": "do not claim partial_frame Delta_ref = 0",
            "reason": "same-coframe/covariant-reference route is mathematically plausible but not parent-signed",
            "effect": "frame derivative remains a nonclaim closure or source-bound input",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1003_1_frame_profile_staged",
            "decision": "stage Delta_ref_frame_profile_over_MH as the fallback row",
            "reason": "if covariant frame descent cannot be closed, retained frame-leak components must be source-backed and absolute-summed",
            "effect": "future proof/data can fill the row without weakening the gate",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1003_2_next_derivative_target",
            "decision": "move to range/lambda independence",
            "reason": "997 lists partial_lambda Delta_ref as the last derivative component after source, radius, time, and frame",
            "effect": "1004 should try the range/domain-scale independence theorem or stage Delta_ref_lambda_profile_over_MH",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1004-Y5-R10-Bref-range-independence-theorem-or-Delta-ref-lambda-profile-row.md",
            "objective": "derive B_ref independence from R10 range/memory/domain/sector scales, or stage a source-backed lambda-profile row without claiming a pass",
            "include": "partial_lambda Delta_ref, R10 range parameter, memory/domain/sector scale dependence, M_H_ref, source/equation paths, no-cancellation guard",
            "exclude": "range independence by notation, fitted lambda cancellation, RC994_0 pass, FB554_0 pass, local-GR claim, GitHub action",
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
    theorem_ok = any(row["audit_id"] == "CFA1003_6_theorem_verdict" and row["status"] == "fail_current_claim" for row in theorem) and all(row["valid_for_claim"] == "false" for row in theorem)
    schema_ok = any(row["target"] == "Delta_ref_frame_profile_over_MH" for row in schema) and any("PARENT_SIGNED_COVARIANT_FRAME_TRUE" in row["formula"] for row in schema)
    candidates_ok = len(candidates) >= 8 and all(row["valid_for_claim"] == "false" for row in candidates)
    runner_ok = all(row["verdict"] == "REFUSED_MISSING_COVARIANT_FRAME_PROVENANCE" and row["score_ready"] == "false" for row in runner)
    zero_switch_ok = any(
        row["candidate_id"] == "FPT1003_4_zero_switch_unsigned"
        and "THEOREM_ZERO_REJECTED_WITHOUT_PARENT_SIGNED_COVARIANT_FRAME" in row["failure_reasons"]
        for row in runner
    )
    fallback_ok = any("MISSING_EPSILON_FRAME_LEAK_FALLBACK_BOUND" in row["failure_reasons"] for row in runner)
    components_ok = any("MISSING_FRAME_LEAK_COMPONENT_C_G" in row["failure_reasons"] for row in runner)
    refusals_ok = len(refusals) == len(runner) and all(row["claim_allowed"] == "false" for row in refusals)
    claims_ok = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in claims)
    decisions_ok = any(row["decision_id"] == "DEC1003_2_next_derivative_target" for row in decisions)
    next_ok = bool(next_target) and next_target[0]["valid_for_claim"] == "false"
    formalization_count = formalization_changed_after_start()
    checks = [
        {"check_id": "V1003_0_sources_exist", "result": "pass" if sources_ok else "fail", "detail": "all source paths exist and needles are present"},
        {"check_id": "V1003_1_theorem_audit_nonclaim", "result": "pass" if theorem_ok else "fail", "detail": "covariant frame zero theorem remains blocked rather than promoted"},
        {"check_id": "V1003_2_schema_ready", "result": "pass" if schema_ok else "fail", "detail": "frame profile and covariant-frame theorem-zero schema rows are present"},
        {"check_id": "V1003_3_candidate_rows_nonclaim", "result": "pass" if candidates_ok else "fail", "detail": "candidate rows remain valid_for_claim=false"},
        {"check_id": "V1003_4_runner_refuses_placeholders", "result": "pass" if runner_ok else "fail", "detail": "runner refuses every current frame placeholder row"},
        {"check_id": "V1003_5_covariant_frame_zero_guard", "result": "pass" if zero_switch_ok else "fail", "detail": "theorem_zero=true is refused without PARENT_SIGNED_COVARIANT_FRAME_TRUE"},
        {"check_id": "V1003_6_epsilon_frame_fallback_guard", "result": "pass" if fallback_ok else "fail", "detail": "fallback bound is demanded when the parent theorem is absent"},
        {"check_id": "V1003_7_component_guard", "result": "pass" if components_ok else "fail", "detail": "retained frame-leak components such as c_g are demanded explicitly"},
        {"check_id": "V1003_8_refusal_ledger_nonclaim", "result": "pass" if refusals_ok else "fail", "detail": "refusal ledger mirrors runner and keeps claims false"},
        {"check_id": "V1003_9_claim_gates_blocked", "result": "pass" if claims_ok else "fail", "detail": "frame, epsilon_frame, RC994_0, and local-GR claims stay blocked"},
        {"check_id": "V1003_10_decision_written", "result": "pass" if decisions_ok else "fail", "detail": "range/lambda derivative target decision is written"},
        {"check_id": "V1003_11_next_target_written", "result": "pass" if next_ok else "fail", "detail": "1004 target row is present and nonclaim"},
        {"check_id": "V1003_12_formalization_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization-workbench modified-file count since script start is {formalization_count}"},
    ]
    ready = all(row["result"] == "pass" for row in checks)
    checks.append(
        {
            "check_id": "V1003_SUMMARY",
            "result": "pass" if ready else "fail",
            "detail": "1003 covariant frame theorem and frame-profile-row validation summary",
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
        "# 1003 Y5 R10 B-ref Covariant Frame Theorem Or Delta-ref Frame Profile Row",
        "",
        "**Status:** covariant-frame zero theorem attempted, not closed; fallback frame-profile row staged as nonclaim.",
        "",
        "**Claim ceiling:** this checkpoint does not claim partial_frame Delta_ref=0, epsilon_frame_leak bound, RC994_0, FB554_0, R10, PPN, WEP, clock, orbital, or local-GR pass.",
        "",
        "## Source Register",
        "",
        md_table(sources, ["source_id", "path", "role", "needle", "exists", "needle_found", "valid_for_claim"]),
        "",
        "## Covariant Frame Theorem Audit",
        "",
        md_table(theorem, ["audit_id", "object", "needed_for_zero", "current_evidence", "status", "valid_for_claim"]),
        "",
        "## Frame Profile Schema",
        "",
        md_table(schema, ["schema_id", "target", "formula", "required_columns", "acceptance_rule", "valid_for_claim"]),
        "",
        "## Candidate Frame Profile Template",
        "",
        md_table(candidates, ["candidate_id", "purpose", "target", "partial_frame_Delta_ref", "Delta_frame_profile", "M_H_ref", "coframe_descent_certificate", "theorem_zero", "frame_zero_authority", "epsilon_frame_leak", "no_cancellation_guard", "valid_for_claim"]),
        "",
        "## Frame Profile Runner",
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
    theorem = covariant_frame_theorem_audit_rows()
    schema = frame_profile_schema_rows()
    candidates = candidate_frame_profile_rows()
    runner = frame_profile_runner_rows(candidates)
    refusals = refusal_ledger_rows(runner)
    claims = claim_gate_rows(runner, theorem)
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, theorem, schema, candidates, runner, refusals, claims, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_1003_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_1003_COVARIANT_FRAME_THEOREM_AUDIT.csv", theorem)
    write_csv(OUT / "P8_Y5_R10_1003_FRAME_PROFILE_SCHEMA.csv", schema)
    write_csv(OUT / "P8_Y5_R10_1003_CANDIDATE_FRAME_PROFILE_TEMPLATE.csv", candidates)
    write_csv(OUT / "P8_Y5_R10_1003_FRAME_PROFILE_RUNNER.csv", runner)
    write_csv(OUT / "P8_Y5_R10_1003_REFUSAL_LEDGER.csv", refusals)
    write_csv(OUT / "P8_Y5_R10_1003_CLAIM_GATE.csv", claims)
    write_csv(OUT / "P8_Y5_R10_1003_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1003_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_1003_VALIDATION.csv", validation)
    write_doc(sources, theorem, schema, candidates, runner, refusals, claims, decisions, validation, next_target)


if __name__ == "__main__":
    main()
