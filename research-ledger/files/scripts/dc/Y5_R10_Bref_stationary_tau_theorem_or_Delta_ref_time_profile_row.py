from __future__ import annotations

import csv
import math
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1002-Y5-R10-Bref-stationary-tau-theorem-or-Delta-ref-time-profile-row.md"
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
            "source_id": "S1002_0_handoff_doc",
            "path": "1001-Y5-R10-Bref-radius-surface-term-theorem-or-Delta-ref-radial-profile-row.md",
            "role": "1001 handoff selecting stationary tau/time derivative target",
            "needle": "1002-Y5-R10-Bref-stationary-tau-theorem-or-Delta-ref-time-profile-row.md",
        },
        {
            "source_id": "S1002_1_next_target",
            "path": "source-intake/mts_residuals/P8_Y5_R10_1001_NEXT_TARGET.csv",
            "role": "machine-readable 1002 target",
            "needle": "partial_t Delta_ref",
        },
        {
            "source_id": "S1002_2_derivative_audit",
            "path": "source-intake/mts_residuals/P8_Y5_R10_997_DERIVATIVE_COMPONENT_AUDIT.csv",
            "role": "time derivative blocker from 997",
            "needle": "DVC997_2_time",
        },
        {
            "source_id": "S1002_3_tau_audit",
            "path": "source-intake/mts_residuals/P8_Y5_R10_684_TAU_GENERATOR_AUDIT.csv",
            "role": "tau/source/charge/clock/orbit/boundary identity audit",
            "needle": "TGA684_5_stationary_generator",
        },
        {
            "source_id": "S1002_4_tau_contract",
            "path": "source-intake/mts_residuals/P8_Y5_R10_685_TAU_GENERATOR_CONTRACT.csv",
            "role": "Killing, Hamiltonian, and clock-normalization tau contract",
            "needle": "TGC685_1_Killing_stationary_route",
        },
        {
            "source_id": "S1002_5_nonstationary_tau",
            "path": "source-intake/mts_residuals/P8_Y5_R10_686_NONSTATIONARY_TAU_RESIDUAL_ROW.csv",
            "role": "epsilon_nonstationary_tau fallback row",
            "needle": "NTR686_0_epsilon_nonstationary_tau",
        },
        {
            "source_id": "S1002_6_selector_tau_attempt",
            "path": "source-intake/mts_residuals/P8_Y5_R10_687_SELECTOR_TO_TAU_THEOREM_ATTEMPT.csv",
            "role": "selector-to-stationary generator attempt and verdict",
            "needle": "STT687_5_verdict",
        },
        {
            "source_id": "S1002_7_symgrad_tau",
            "path": "source-intake/mts_residuals/P8_Y5_R10_688_SYMGRAD_TAU_DECOMPOSITION.csv",
            "role": "symgrad tau obstruction decomposition",
            "needle": "SGT688_0_exact_congruence_identity",
        },
        {
            "source_id": "S1002_8_no_cancellation",
            "path": "source-intake/mts_residuals/P8_Y5_R10_994_DELTAH_NO_CANCELLATION_ENVELOPE.csv",
            "role": "absolute residual envelope",
            "needle": "DHE994_1_no_cancellation",
        },
        {
            "source_id": "S1002_9_prior_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_1001_VALIDATION.csv",
            "role": "1001 validation pass",
            "needle": "V1001_SUMMARY",
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


def stationary_tau_theorem_audit_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "STA1002_0_quantity",
            "object": "partial_t Delta_ref",
            "needed_for_zero": "the reference subtraction must be invariant along the same tau used by charge, clocks, and readout",
            "current_evidence": "997 flags MISSING_STATIONARY_TAU_BREF_RULE",
            "status": "blocked_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "STA1002_1_tau_identity",
            "object": "tau_source=tau_charge=tau_clock=tau_boundary=tau_orbit",
            "needed_for_zero": "one parent-selected observed time-flow, not separate post-readout labels",
            "current_evidence": "684/685 keep tau identity conditional and unsigned",
            "status": "unsigned",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "STA1002_2_stationary_generator",
            "object": "L_tau g_obs=0 and nabla_(mu tau_nu)=0",
            "needed_for_zero": "a stationary/Killing observed generator locks the time evolution of the local reference branch",
            "current_evidence": "687 verdict says selector silence is weaker than full observed stationarity",
            "status": "fail_current_claim",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "STA1002_3_Bref_invariance",
            "object": "L_tau B_ref=0",
            "needed_for_zero": "B_ref and its counterterm/reference branch must not drift under tau",
            "current_evidence": "MISSING_PARENT_BREF_TAU_INVARIANCE_CERTIFICATE",
            "status": "unsigned",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "STA1002_4_hamiltonian_clock_lock",
            "object": "H_tau, H_ref, and clock normalization",
            "needed_for_zero": "Hamiltonian integrability, fixed reference, and clock normalization must use the same tau",
            "current_evidence": "685 marks Hamiltonian boundary route and clock normalization route as not signed",
            "status": "unsigned",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "STA1002_5_nonstationary_residual",
            "object": "epsilon_nonstationary_tau",
            "needed_for_zero": "T_H^{mu nu} nabla_(mu tau_nu) and related time drift terms vanish or are source bounded",
            "current_evidence": "686/688 stage nonstationary-tau and symgrad-tau residuals",
            "status": "fallback_required",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "STA1002_6_theorem_verdict",
            "object": "partial_t Delta_ref = 0",
            "needed_for_zero": "tau identity, stationary generator, L_tau B_ref, Hamiltonian integrability, clock lock, fixed reference, and no-exchange clauses parent-signed",
            "current_evidence": "not enough parent tau geometry to promote zero",
            "status": "fail_current_claim",
            "valid_for_claim": "false",
        },
    ]


def time_profile_schema_rows() -> list[dict[str, str]]:
    return [
        {
            "schema_id": "TPS1002_0_profile_formula",
            "target": "Delta_ref_time_profile_over_MH",
            "formula": "abs(partial_t_Delta_ref * Delta_t_profile)/M_H_ref",
            "required_columns": "system_id;time_parameter;tau_definition;Delta_t_profile;partial_t_Delta_ref;Delta_ref_units;M_H_ref;M_H_ref_units;tau_identity_certificate;L_tau_Bref_certificate;clock_lock_certificate;Hamiltonian_integrability_certificate;fixed_reference_certificate;source_path;equation_ref;valid_for_claim",
            "acceptance_rule": "finite same-frame ratio or theorem_zero=true with parent-signed stationary tau theorem; no MISSING markers",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "TPS1002_1_stationary_tau_zero_switch",
            "target": "partial_t_Delta_ref_zero",
            "formula": "theorem_zero=true iff tau_zero_authority=PARENT_SIGNED_STATIONARY_TAU_TRUE",
            "required_columns": "tau_identity_certificate;stationary_generator_certificate;L_tau_Bref_certificate;clock_lock_certificate;Hamiltonian_integrability_certificate;fixed_reference_certificate;no_exchange_certificate;source_path;equation_ref",
            "acceptance_rule": "stationary-by-assumption, clock-choice, and lapse-gauge choices are rejected",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "TPS1002_2_epsilon_tau_fallback",
            "target": "epsilon_nonstationary_tau_to_time_profile_bridge",
            "formula": "Delta_ref_time_profile_over_MH <= C_tau * epsilon_nonstationary_tau when C_tau and denominator are sourced",
            "required_columns": "epsilon_nonstationary_tau;C_tau;stress_source;symgrad_tau_source;M_H_ref;units;source_path;equation_ref",
            "acceptance_rule": "fallback bound is nonclaim until epsilon_tau, C_tau, and M_H_ref are numeric, sourced, and same-frame",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "TPS1002_3_no_cancellation",
            "target": "time contribution to residual envelope",
            "formula": "absolute values only",
            "required_columns": "no_cancellation_guard=ABS_PRODUCT_NO_SIGN_CANCELLATION",
            "acceptance_rule": "no sign cancellation, fitted clock drift cancellation, or lapse rescaling cancellation",
            "valid_for_claim": "false",
        },
    ]


def candidate_time_profile_rows() -> list[dict[str, str]]:
    base = {
        "system_id": "R10_local_reference_branch",
        "time_parameter": "MISSING_TIME_PARAMETER",
        "tau_definition": "MISSING_TAU_DEFINITION",
        "Delta_t_profile": "MISSING_DELTA_T_PROFILE",
        "Delta_t_units": "MISSING_DELTA_T_UNITS",
        "partial_t_Delta_ref": "MISSING_PARTIAL_T_DELTA_REF",
        "partial_t_units": "MISSING_PARTIAL_T_UNITS",
        "Delta_ref_units": "MISSING_DELTA_REF_UNITS",
        "M_H_ref": "MISSING_M_H_REF",
        "M_H_ref_units": "MISSING_M_H_REF_UNITS",
        "tau_identity_certificate": "MISSING_TAU_IDENTITY_CERTIFICATE",
        "stationary_generator_certificate": "MISSING_STATIONARY_GENERATOR_CERTIFICATE",
        "L_tau_Bref_certificate": "MISSING_L_TAU_BREF_CERTIFICATE",
        "clock_lock_certificate": "MISSING_CLOCK_LOCK_CERTIFICATE",
        "Hamiltonian_integrability_certificate": "MISSING_HAMILTONIAN_INTEGRABILITY_CERTIFICATE",
        "fixed_reference_certificate": "MISSING_FIXED_REFERENCE_CERTIFICATE",
        "no_exchange_certificate": "MISSING_NO_EXCHANGE_CERTIFICATE",
        "source_path": "MISSING_SOURCE_FILE",
        "equation_ref": "MISSING_EQUATION_REF",
        "theorem_zero": "false",
        "tau_zero_authority": "MISSING_PARENT_TAU_SIGNATURE",
        "epsilon_nonstationary_tau": "MISSING_EPSILON_NONSTATIONARY_TAU",
        "C_tau": "MISSING_C_TAU",
        "no_cancellation_guard": "MISSING_ABSOLUTE_PRODUCT_GUARD",
        "valid_for_claim": "false",
    }
    variants = [
        ("TPT1002_0_missing_tau_identity", "same tau is not certified across source/charge/clock/boundary/orbit"),
        ("TPT1002_1_missing_time_derivative", "partial_t Delta_ref is not finite or theorem-zero"),
        ("TPT1002_2_missing_time_profile", "Delta_t profile is not sourced"),
        ("TPT1002_3_missing_MHref", "positive same-frame M_H_ref denominator is missing"),
        ("TPT1002_4_zero_switch_unsigned", "theorem-zero switch is requested without parent-signed stationary tau"),
        ("TPT1002_5_missing_clock_hamiltonian_lock", "clock normalization and Hamiltonian integrability are not locked"),
        ("TPT1002_6_all_missing_live_placeholder", "live time row is schema-only and cannot be scored"),
    ]
    rows: list[dict[str, str]] = []
    for row_id, purpose in variants:
        row = {**base, "candidate_id": row_id, "target": "Delta_ref_time_profile_over_MH", "purpose": purpose}
        if row_id == "TPT1002_4_zero_switch_unsigned":
            row["theorem_zero"] = "true"
            row["tau_zero_authority"] = "MISSING_PARENT_TAU_SIGNATURE"
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


def evaluate_time_profile(row: dict[str, str]) -> dict[str, str]:
    reasons: list[str] = []
    derivative_ok, derivative = finite_float(row.get("partial_t_Delta_ref", ""))
    theorem_zero = row.get("theorem_zero", "").strip().lower() == "true"
    parent_signed_tau_zero = theorem_zero and row.get("tau_zero_authority") == "PARENT_SIGNED_STATIONARY_TAU_TRUE"
    if not derivative_ok and not parent_signed_tau_zero:
        reasons.append("MISSING_PARTIAL_T_DELTA_REF_OR_PARENT_SIGNED_STATIONARY_TAU_ZERO")
    if theorem_zero and not parent_signed_tau_zero:
        reasons.append("THEOREM_ZERO_REJECTED_WITHOUT_PARENT_SIGNED_STATIONARY_TAU")
    delta_t_ok, delta_t = finite_float(row.get("Delta_t_profile", ""))
    if not delta_t_ok or delta_t is None or delta_t <= 0:
        reasons.append("MISSING_POSITIVE_DELTA_T_PROFILE")
    mh_ok, mh = finite_float(row.get("M_H_ref", ""))
    if not mh_ok or mh is None or mh <= 0:
        reasons.append("MISSING_POSITIVE_SAME_FRAME_M_H_REF")
    for field in [
        "system_id",
        "time_parameter",
        "tau_definition",
        "Delta_t_units",
        "partial_t_units",
        "Delta_ref_units",
        "M_H_ref_units",
        "tau_identity_certificate",
        "stationary_generator_certificate",
        "L_tau_Bref_certificate",
        "clock_lock_certificate",
        "Hamiltonian_integrability_certificate",
        "fixed_reference_certificate",
        "no_exchange_certificate",
        "equation_ref",
    ]:
        if is_missing(row.get(field, "")):
            reasons.append(f"MISSING_{field.upper()}")
    epsilon_ok, epsilon_value = finite_float(row.get("epsilon_nonstationary_tau", ""))
    c_tau_ok, c_tau_value = finite_float(row.get("C_tau", ""))
    if not parent_signed_tau_zero and not (epsilon_ok and c_tau_ok and epsilon_value is not None and c_tau_value is not None and epsilon_value >= 0 and c_tau_value >= 0):
        reasons.append("MISSING_EPSILON_TAU_FALLBACK_BOUND")
    if not path_exists(row.get("source_path", "")):
        reasons.append("MISSING_EXISTING_SOURCE_PATH")
    if row.get("no_cancellation_guard") != "ABS_PRODUCT_NO_SIGN_CANCELLATION":
        reasons.append("MISSING_NO_CANCELLATION_GUARD")
    if row.get("valid_for_claim") != "true":
        reasons.append("VALID_FOR_CLAIM_FALSE")
    numeric_ratio = "NOT_SCORED"
    if not reasons and derivative is not None and delta_t is not None and mh is not None:
        numeric_ratio = f"{abs(derivative * delta_t) / mh:.16e}"
    verdict = "ACCEPT_NUMERIC_OR_PARENT_SIGNED_STATIONARY_TAU_ZERO" if not reasons else "REFUSED_MISSING_STATIONARY_TAU_PROVENANCE"
    return {
        "runner_id": row["candidate_id"].replace("TPT", "TPR"),
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


def time_profile_runner_rows(candidates: list[dict[str, str]]) -> list[dict[str, str]]:
    return [evaluate_time_profile(row) for row in candidates]


def refusal_ledger_rows(runner: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        {
            "refusal_id": row["runner_id"].replace("TPR", "TRF"),
            "candidate_id": row["candidate_id"],
            "refusal": row["verdict"],
            "why": row["failure_reasons"],
            "required_exit": "parent-signed stationary tau theorem or finite time-profile coefficient with epsilon_tau fallback, units, source, and equation path",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        }
        for row in runner
    ]


def claim_gate_rows(runner: list[dict[str, str]], theorem: list[dict[str, str]]) -> list[dict[str, str]]:
    runner_refuses = all(row["verdict"] == "REFUSED_MISSING_STATIONARY_TAU_PROVENANCE" for row in runner)
    theorem_fails = any(row["audit_id"] == "STA1002_6_theorem_verdict" and row["status"] == "fail_current_claim" for row in theorem)
    return [
        {
            "gate_id": "CG1002_0_partial_t_Delta_ref_zero",
            "claim": "partial_t Delta_ref = 0",
            "gate_pass": "false",
            "reason": "tau identity, stationary generator, L_tau B_ref, clock lock, Hamiltonian integrability, fixed reference, and no-exchange are unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1002_1_Delta_ref_time_profile_bound",
            "claim": "Delta_ref_time_profile_over_MH is bounded",
            "gate_pass": "false",
            "reason": "time derivative/profile/M_H_ref/epsilon_tau inputs are placeholder-only",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1002_2_epsilon_tau_bound",
            "claim": "epsilon_nonstationary_tau supplies a valid fallback bound",
            "gate_pass": "false",
            "reason": "686/687/688 define the residual structure but do not supply numeric same-frame source-backed values",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1002_3_RC994_0",
            "claim": "RC994_0 residual current passes",
            "gate_pass": "false",
            "reason": "time derivative is blocked, and frame/lambda pieces remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1002_4_local_GR_branch",
            "claim": "local-GR branch passes",
            "gate_pass": "false",
            "reason": "R10 residual vector is not zero or source-bounded",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1002_5_guardrail",
            "claim": "stationary tau/time guardrail is installed",
            "gate_pass": flag(runner_refuses and theorem_fails),
            "reason": "theorem is not promoted and all placeholder rows are refused",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1002_0_theorem_not_closed",
            "decision": "do not claim partial_t Delta_ref = 0",
            "reason": "stationary tau identity is still a parent-action contract, not a theorem",
            "effect": "time derivative remains a nonclaim closure or source-bound input",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1002_1_time_profile_staged",
            "decision": "stage Delta_ref_time_profile_over_MH as the fallback row",
            "reason": "if L_tau B_ref cannot be closed, the honest route is a sourced time profile plus epsilon_tau fallback",
            "effect": "future proof/data can fill the row without weakening the gate",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1002_2_next_derivative_target",
            "decision": "move to covariant frame/coframe derivative",
            "reason": "997 lists partial_frame Delta_ref as the next derivative component after source, radius, and time",
            "effect": "1003 should try the frame-gauge theorem or stage Delta_ref_frame_profile_over_MH",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1003-Y5-R10-Bref-covariant-frame-theorem-or-Delta-ref-frame-profile-row.md",
            "objective": "derive frame changes as proper gauge for B_ref/H_ref, or stage a source-backed frame-profile row without claiming a pass",
            "include": "partial_frame Delta_ref, covariant coframe/reference rule, preferred-frame leakage, M_H_ref, source/equation paths, no-cancellation guard",
            "exclude": "frame-choice-by-convention, preferred-frame silence by assumption, RC994_0 pass, FB554_0 pass, local-GR claim, GitHub action",
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
    theorem_ok = any(row["audit_id"] == "STA1002_6_theorem_verdict" and row["status"] == "fail_current_claim" for row in theorem) and all(row["valid_for_claim"] == "false" for row in theorem)
    schema_ok = any(row["target"] == "Delta_ref_time_profile_over_MH" for row in schema) and any("PARENT_SIGNED_STATIONARY_TAU_TRUE" in row["formula"] for row in schema)
    candidates_ok = len(candidates) >= 7 and all(row["valid_for_claim"] == "false" for row in candidates)
    runner_ok = all(row["verdict"] == "REFUSED_MISSING_STATIONARY_TAU_PROVENANCE" and row["score_ready"] == "false" for row in runner)
    zero_switch_ok = any(
        row["candidate_id"] == "TPT1002_4_zero_switch_unsigned"
        and "THEOREM_ZERO_REJECTED_WITHOUT_PARENT_SIGNED_STATIONARY_TAU" in row["failure_reasons"]
        for row in runner
    )
    fallback_ok = any("MISSING_EPSILON_TAU_FALLBACK_BOUND" in row["failure_reasons"] for row in runner)
    refusals_ok = len(refusals) == len(runner) and all(row["claim_allowed"] == "false" for row in refusals)
    claims_ok = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in claims)
    decisions_ok = any(row["decision_id"] == "DEC1002_2_next_derivative_target" for row in decisions)
    next_ok = bool(next_target) and next_target[0]["valid_for_claim"] == "false"
    formalization_count = formalization_changed_after_start()
    checks = [
        {"check_id": "V1002_0_sources_exist", "result": "pass" if sources_ok else "fail", "detail": "all source paths exist and needles are present"},
        {"check_id": "V1002_1_theorem_audit_nonclaim", "result": "pass" if theorem_ok else "fail", "detail": "stationary tau zero theorem remains blocked rather than promoted"},
        {"check_id": "V1002_2_schema_ready", "result": "pass" if schema_ok else "fail", "detail": "time profile and stationary-tau theorem-zero schema rows are present"},
        {"check_id": "V1002_3_candidate_rows_nonclaim", "result": "pass" if candidates_ok else "fail", "detail": "candidate rows remain valid_for_claim=false"},
        {"check_id": "V1002_4_runner_refuses_placeholders", "result": "pass" if runner_ok else "fail", "detail": "runner refuses every current time placeholder row"},
        {"check_id": "V1002_5_stationary_tau_zero_guard", "result": "pass" if zero_switch_ok else "fail", "detail": "theorem_zero=true is refused without PARENT_SIGNED_STATIONARY_TAU_TRUE"},
        {"check_id": "V1002_6_epsilon_tau_fallback_guard", "result": "pass" if fallback_ok else "fail", "detail": "fallback bound is demanded when the parent theorem is absent"},
        {"check_id": "V1002_7_refusal_ledger_nonclaim", "result": "pass" if refusals_ok else "fail", "detail": "refusal ledger mirrors runner and keeps claims false"},
        {"check_id": "V1002_8_claim_gates_blocked", "result": "pass" if claims_ok else "fail", "detail": "time, epsilon_tau, RC994_0, and local-GR claims stay blocked"},
        {"check_id": "V1002_9_decision_written", "result": "pass" if decisions_ok else "fail", "detail": "covariant frame derivative target decision is written"},
        {"check_id": "V1002_10_next_target_written", "result": "pass" if next_ok else "fail", "detail": "1003 target row is present and nonclaim"},
        {"check_id": "V1002_11_formalization_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization-workbench modified-file count since script start is {formalization_count}"},
    ]
    ready = all(row["result"] == "pass" for row in checks)
    checks.append(
        {
            "check_id": "V1002_SUMMARY",
            "result": "pass" if ready else "fail",
            "detail": "1002 stationary tau theorem and time-profile-row validation summary",
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
        "# 1002 Y5 R10 B-ref Stationary Tau Theorem Or Delta-ref Time Profile Row",
        "",
        "**Status:** stationary-tau zero theorem attempted, not closed; fallback time-profile row staged as nonclaim.",
        "",
        "**Claim ceiling:** this checkpoint does not claim partial_t Delta_ref=0, epsilon_tau bound, RC994_0, FB554_0, R10, PPN, or local-GR pass.",
        "",
        "## Source Register",
        "",
        md_table(sources, ["source_id", "path", "role", "needle", "exists", "needle_found", "valid_for_claim"]),
        "",
        "## Stationary Tau Theorem Audit",
        "",
        md_table(theorem, ["audit_id", "object", "needed_for_zero", "current_evidence", "status", "valid_for_claim"]),
        "",
        "## Time Profile Schema",
        "",
        md_table(schema, ["schema_id", "target", "formula", "required_columns", "acceptance_rule", "valid_for_claim"]),
        "",
        "## Candidate Time Profile Template",
        "",
        md_table(candidates, ["candidate_id", "purpose", "target", "partial_t_Delta_ref", "Delta_t_profile", "M_H_ref", "tau_identity_certificate", "theorem_zero", "tau_zero_authority", "epsilon_nonstationary_tau", "no_cancellation_guard", "valid_for_claim"]),
        "",
        "## Time Profile Runner",
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
    theorem = stationary_tau_theorem_audit_rows()
    schema = time_profile_schema_rows()
    candidates = candidate_time_profile_rows()
    runner = time_profile_runner_rows(candidates)
    refusals = refusal_ledger_rows(runner)
    claims = claim_gate_rows(runner, theorem)
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, theorem, schema, candidates, runner, refusals, claims, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_1002_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_1002_STATIONARY_TAU_THEOREM_AUDIT.csv", theorem)
    write_csv(OUT / "P8_Y5_R10_1002_TIME_PROFILE_SCHEMA.csv", schema)
    write_csv(OUT / "P8_Y5_R10_1002_CANDIDATE_TIME_PROFILE_TEMPLATE.csv", candidates)
    write_csv(OUT / "P8_Y5_R10_1002_TIME_PROFILE_RUNNER.csv", runner)
    write_csv(OUT / "P8_Y5_R10_1002_REFUSAL_LEDGER.csv", refusals)
    write_csv(OUT / "P8_Y5_R10_1002_CLAIM_GATE.csv", claims)
    write_csv(OUT / "P8_Y5_R10_1002_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1002_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_1002_VALIDATION.csv", validation)
    write_doc(sources, theorem, schema, candidates, runner, refusals, claims, decisions, validation, next_target)


if __name__ == "__main__":
    main()
