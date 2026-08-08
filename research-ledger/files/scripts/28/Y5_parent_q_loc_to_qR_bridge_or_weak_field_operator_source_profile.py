from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1521-Y5-parent-q_loc-to-qR-bridge-or-weak-field-operator-source-profile.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1520_doc": ROOT / "1520-Y5-parent-Lcg-contract-or-q_loc-weak-field-response-coefficient.md",
    "1520_next": OUT / "P8_Y5_PARENT_LCG_1520_NEXT_TARGET.csv",
    "1520_cq": OUT / "P8_Y5_PARENT_LCG_1520_CQGAMMA_DERIVATION_ATTEMPT.csv",
    "1520_runner": OUT / "P8_Y5_PARENT_LCG_1520_QLOC_GAMMA_RUNNER_INPUT_ROW.csv",
    "1520_validation": OUT / "P8_Y5_BRR545_1520_VALIDATION.csv",
    "1240_qr_map": OUT / "P8_Y5_R10_1240_QR_TO_PPN_MAPPING_SCHEMA.csv",
    "1244_doc": ROOT / "1244-Y5-R10-QR-statistical-policy-and-GM-convention-pack.md",
    "1244_policy": OUT / "P8_Y5_R10_1244_RUNNER_POLICY_FEED.csv",
    "1181_ppn": OUT / "P8_Y5_R10_1181_EXTERNAL_PPN_SOURCE_REGISTER.csv",
    "1368_projection": OUT / "P8_Y5_R10_1368_QLOC_TO_PPN_GAMMA_PROJECTION_REQUIREMENTS.csv",
    "1369_runner": OUT / "P8_Y5_R10_1369_QLOC_GAMMA_RUNNER_SCHEMA.csv",
    "1369_smoke": OUT / "P8_Y5_R10_1369_QLOC_GAMMA_SMOKE_RESULT.csv",
    "1367_kernel": OUT / "P8_Y5_R10_1367_KMETRIC_CHAIN_KERNEL_ATTEMPT.csv",
    "1365_qbound": OUT / "P8_Y5_R10_1365_QLOC_BOUND_SOURCE_ROW.csv",
    "1366_env": OUT / "P8_Y5_R10_1366_QLOC_ENVELOPE_INTAKE_ROWS.csv",
    "1289_delta": OUT / "P8_Y5_R10_1289_DELTAK00_COMPARISON_TEMPLATE.csv",
    "776_kgamma": OUT / "P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1521_SOURCE_REGISTER.csv"
QR_BRIDGE_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1521_QLOC_TO_QR_BRIDGE_AUDIT.csv"
OPERATOR_PROFILE = OUT / "P8_Y5_PARENT_QLOC_1521_WEAK_FIELD_OPERATOR_SOURCE_PROFILE.csv"
RUNNER_UPDATE = OUT / "P8_Y5_PARENT_QLOC_1521_QLOC_GAMMA_RUNNER_UPDATE.csv"
CHANNEL_BUDGET = OUT / "P8_Y5_PARENT_QLOC_1521_RETAINED_CHANNEL_BUDGET.csv"
REJECTION_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1521_REJECTION_LEDGER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1521_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1521_DECISION.csv"
LOCAL_STATUS = OUT / "P8_Y5_PARENT_QLOC_1521_LOCAL_GR_NEWTON_STATUS.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1521_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1521_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1521"
QUAR_BRIDGE = QUARANTINE / "QLOC_TO_QR_BRIDGE_AUDIT_NONCLAIM.csv"
QUAR_OPERATOR = QUARANTINE / "WEAK_FIELD_OPERATOR_SOURCE_PROFILE_NONCLAIM.csv"
QUAR_RUNNER = QUARANTINE / "QLOC_GAMMA_RUNNER_UPDATE_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "QLOC_DECISION_NONCLAIM.csv"
BRANCH_BRIDGE = BRANCH_RESIDUALS / "q_loc_to_qR_bridge_audit_nonclaim_1521.csv"
BRANCH_OPERATOR = BRANCH_RESIDUALS / "weak_field_operator_source_profile_nonclaim_1521.csv"
BRANCH_RUNNER = BRANCH_RESIDUALS / "q_loc_gamma_runner_update_nonclaim_1521.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "q_loc_decision_nonclaim_1521.csv"


def flags() -> dict[str, bool]:
    return {
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_list(*keys: str) -> str:
    return "; ".join(rel(SOURCE_FILES[key]) for key in keys)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = [
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "passes_for_claim",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source_id, (key, path) in enumerate(SOURCE_FILES.items()):
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1521_{source_id}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "purpose": "input evidence for q_loc-to-q_R bridge and weak-field operator profile",
                **flags(),
            }
        )
    return rows


def qr_bridge_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "QBRG1521_0_qR_exterior_hair",
            "q_R convention",
            "R_AB=-Q_R/r with q_R_hat=Q_R c^2/(G M_source)",
            "SOURCE_SCHEMA_EXISTS",
            "q_R is an exterior scalar hair scoring convention, not yet a live MTS value",
            source_list("1240_qr_map", "1244_doc", "1244_policy"),
        ),
        (
            "QBRG1521_1_q_loc_identity_target",
            "q_loc bridge target",
            "integrate/project q_loc^nu into the same exterior scalar hair Q_R and same R_AB channel",
            "TARGET_WRITTEN",
            "requires scalar trace projection, exterior Green solution, boundary conditions, and source averaging",
            source_list("1368_projection", "1369_runner", "1520_cq"),
        ),
        (
            "QBRG1521_2_scalar_trace_only",
            "no vector/tensor/gauge leakage",
            "q_loc^nu must contribute only to the PPN gamma scalar-slip channel",
            "NOT_PROVED",
            "q_loc currently has retained DeltaK, boundary, source, vector/gauge, and projector channels",
            source_list("1368_projection", "1367_kernel", "776_kgamma"),
        ),
        (
            "QBRG1521_3_same_normalization",
            "q_loc_hat == q_R_hat",
            "q_loc_hat must equal Q_R c^2/(G M_source) with the same Sun/GM/source convention",
            "MISSING_NORMALIZATION_BRIDGE",
            "no q_loc profile, integral, source averaging, or GM denominator is supplied",
            source_list("1244_policy", "1369_runner", "1520_runner"),
        ),
        (
            "QBRG1521_4_same_sign_and_boundary",
            "gamma_minus_1=-q_loc_hat/2",
            "the exterior solution must use R_infinity=0, areal-radial matching, and the same sign as QMAP1240",
            "MISSING_SIGN_BOUNDARY_PROOF",
            "a local divergence residual does not automatically have the Q_R exterior sign",
            source_list("1240_qr_map", "1520_cq"),
        ),
        (
            "QBRG1521_5_no_retained_channels",
            "q_loc is the only active local weak-field residual",
            "DeltaK, K_conn, K_domain, K_boundary, source normalization, and matter-constant channels are zero-derived or independently bounded",
            "NOT_PROVED",
            "no-cancellation rule blocks importing q_R policy as a q_loc pass",
            source_list("1368_projection", "1366_env", "1365_qbound"),
        ),
        (
            "QBRG1521_6_bridge_verdict",
            "current MTS proves q_loc_hat == q_R_hat",
            "all bridge clauses above pass with source paths and no retained channels",
            "QLOC_TO_QR_BRIDGE_NOT_PROVED",
            "C_qgamma=-1/2 remains conditional-only; direct weak-field operator profile is required",
            source_list("1520_doc", "1520_validation"),
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "bridge_id": bridge_id,
            "claim_piece": claim_piece,
            "required_identity": identity,
            "status": status,
            "why_not_claim": why,
            "source_paths": sources,
            **flags(),
        }
        for bridge_id, claim_piece, identity, status, why, sources in rows
    ]


def operator_profile_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "OP1521_0_linear_operator",
            "L_PPN",
            "linearized weak-field operator in fixed gauge mapping metric potentials to source/residual channels",
            "MISSING_OPERATOR",
            "choose gauge, trace reversal, areal-radial convention, and boundary condition",
        ),
        (
            "OP1521_1_observable_readout",
            "R_gamma",
            "readout functional extracting gamma_minus_1 from h_00 and h_ij relative to U=GM/r",
            "MISSING_READOUT",
            "must match Cassini/QMAP1240 convention",
        ),
        (
            "OP1521_2_q_source_projection",
            "S_q := P_obs P_loc(nabla Gamma_eff - div K_hat)",
            "source term produced by the q_loc residual in the scalar PPN channel",
            "MISSING_SOURCE_PROFILE",
            "needs q_loc profile, source average, units, and support",
        ),
        (
            "OP1521_3_normalization",
            "N_q",
            "dimensionless normalization converting the integrated q_loc source to q_loc_hat",
            "MISSING_NORMALIZATION",
            "must use same measured GM/source convention or a direct dimensionless value",
        ),
        (
            "OP1521_4_response_coefficient",
            "C_qgamma",
            "C_qgamma = R_gamma[L_PPN^{-1} S_q] / q_loc_hat",
            "OPERATOR_FORM_ONLY",
            "cannot evaluate until OP1521_0 through OP1521_3 are supplied",
        ),
        (
            "OP1521_5_DeltaK_response",
            "C_DeltaK",
            "same operator/readout applied to DeltaK/Kmetric mismatch channel",
            "MISSING_RESPONSE",
            "retained channel must be zero-derived or bounded independently",
        ),
        (
            "OP1521_6_boundary_source_response",
            "C_boundary;C_source",
            "operator/readout response for boundary flux and source-normalization residuals",
            "MISSING_RESPONSE",
            "cannot assume cancellation with q_loc",
        ),
        (
            "OP1521_7_acceptance",
            "weak-field operator profile",
            "all operator, source, normalization, coefficient, and retained-channel rows are source-backed",
            "CLAIM_BLOCKED",
            "runner stays schema-only until no MISSING rows remain",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "profile_id": profile_id,
            "quantity": quantity,
            "definition": definition,
            "status": status,
            "required_input": required,
            "source_paths": source_list("1368_projection", "1369_runner", "1520_cq"),
            **flags(),
        }
        for profile_id, quantity, definition, status, required in rows
    ]


def runner_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1521_0_bridge_refusal",
            "branch": "q_loc_to_gamma_after_bridge_attempt",
            "bridge_status": "QLOC_TO_QR_BRIDGE_NOT_PROVED",
            "q_loc_hat": "MISSING_QLOC_VALUE",
            "q_R_hat": "MISSING_QR_VALUE_UNCHANGED",
            "C_qgamma_live": "MISSING_WEAK_FIELD_RESPONSE",
            "C_qgamma_qR_conditional": "-0.5_IF_QLOC_TO_QR_BRIDGE_PROVED",
            "gamma_minus_1_predicted": "MISSING",
            "sigma_gamma": "2.3e-05",
            "q_R_hat_abs_guardrail": "4.6e-05",
            "result": "BLOCKED_BRIDGE_AND_OPERATOR_INPUTS_MISSING",
            "source_paths": source_list("1244_policy", "1369_runner", "1520_runner"),
            **flags(),
        }
    ]


def channel_budget_rows() -> list[dict[str, Any]]:
    rows = [
        ("CH1521_0_q_loc_scalar", "q_loc scalar trace", "MISSING_SOURCE_PROFILE", "main bridge target"),
        ("CH1521_1_DeltaK", "K_hat - K_metric mismatch", "RETAINED_UNBOUNDED", "can source gamma independently"),
        ("CH1521_2_Kconn", "connection response", "RETAINED_UNBOUNDED", "hidden derivative channel"),
        ("CH1521_3_Kdomain", "domain/projector response", "RETAINED_UNBOUNDED", "local mask/readout leakage"),
        ("CH1521_4_Kboundary", "boundary/no-flux response", "RETAINED_UNBOUNDED", "exterior condition risk"),
        ("CH1521_5_source_norm", "M_H_ref/source normalization", "RETAINED_UNBOUNDED", "Newton denominator still missing"),
        ("CH1521_6_matter_constants", "matter/clock/source constants", "RETAINED_UNBOUNDED", "universal coupling not parent-signed"),
        ("CH1521_7_acceptance", "no-cancellation local residual budget", "CLAIM_BLOCKED", "each retained channel must be zeroed or independently bounded"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "channel_id": channel_id,
            "channel": channel,
            "status": status,
            "reason": reason,
            "source_paths": source_list("1368_projection", "1519_blockers") if "1519_blockers" in SOURCE_FILES else source_list("1368_projection"),
            **flags(),
        }
        for channel_id, channel, status, reason in rows
    ]


def rejection_rows() -> list[dict[str, Any]]:
    rows = [
        ("REJ1521_0_name_equivalence", "treat q_loc and q_R as equal because both are local residual symbols", "REJECTED", "one is a projected local residual, the other an exterior scalar-hair convention"),
        ("REJ1521_1_skip_integral", "use q_R guardrail without integrating q_loc to Q_R", "REJECTED", "requires source averaging and exterior Green solution"),
        ("REJ1521_2_ignore_channels", "ignore DeltaK/boundary/source channels", "REJECTED", "no-cancellation discipline forbids hiding retained channels"),
        ("REJ1521_3_fit_Cqgamma", "fit C_qgamma to Cassini", "REJECTED", "response coefficient must come from linearized weak-field solve"),
        ("REJ1521_4_import_qR_value", "pretend q_R_hat exists", "REJECTED", "1244 explicitly keeps q_R_hat missing"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "rejection_id": rejection_id,
            "shortcut": shortcut,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for rejection_id, shortcut, status, reason in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1521_0_qR_policy", "q_R policy and Cassini comparator exist", "PASS_NONCLAIM", "1244 supplies policy and guardrail but not q_R_hat", False),
        ("GATE1521_1_q_loc_qR_bridge", "q_loc_hat equals q_R_hat with same convention", "BLOCKED", "projection, source averaging, sign, GM convention, and retained-channel silence are missing", False),
        ("GATE1521_2_Cqgamma_import", "C_qgamma=-1/2 can be used live", "BLOCKED", "conditional coefficient requires bridge proof", False),
        ("GATE1521_3_operator_profile", "direct weak-field operator response can be evaluated", "BLOCKED", "L_PPN, R_gamma, S_q, N_q, C_DeltaK, and boundary/source responses are missing", False),
        ("GATE1521_4_runner_score", "q_loc gamma runner can score", "BLOCKED", "both bridge and direct operator paths remain missing", False),
        ("GATE1521_5_local_GR_or_PPN_claim", "local GR / PPN pass can be claimed", "BLOCKED_NO_CLAIM", "no q_loc-to-observable response is live", False),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "gate_pass": gate_pass,
            **flags(),
        }
        for gate_id, claim, status, reason, gate_pass in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC1521_0_bridge_not_proved", "Do not import the q_R guardrail into q_loc.", "QLOC_TO_QR_BRIDGE_NOT_PROVED", "the bridge needs scalar projection, exterior integration, same normalization, and retained-channel silence."),
        ("DEC1521_1_operator_lane", "Use a weak-field operator/source profile as the honest fallback.", "OPERATOR_PROFILE_STAGED", "this is the non-smuggled route to C_qgamma, C_DeltaK, and gamma residuals."),
        ("DEC1521_2_next", "Next target is q_loc scalar source profile and normalization first row.", "NEXT_1522_QLOC_SOURCE_PROFILE", "without S_q and N_q, neither the q_R bridge nor direct operator runner can score."),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "result": result,
            "rationale": rationale,
            **flags(),
        }
        for decision_id, decision, result, rationale in rows
    ]


def local_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("LOCAL1521_0_qR", "q_R policy", "POLICY_EXISTS_NONCLAIM", "guardrail exists but q_R_hat missing"),
        ("LOCAL1521_1_q_loc_bridge", "q_loc-to-q_R bridge", "NOT_PROVED", "local residual has not been integrated to the same exterior hair"),
        ("LOCAL1521_2_Cqgamma", "q_loc-to-gamma coefficient", "MISSING_LIVE_RESPONSE", "conditional -1/2 coefficient not importable"),
        ("LOCAL1521_3_PPN", "Cassini/PPN scoring", "NOT_CLAIMED", "runner blocked by bridge/operator inputs"),
        ("LOCAL1521_4_GR_Newton", "derived local GR/Newton", "NOT_CLAIMED", "M_H_ref/source normalization and q_loc response remain open"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": status_id,
            "claim": claim,
            "current_status": status,
            "reason": reason,
            **flags(),
        }
        for status_id, claim, status, reason in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1521_0_1522",
            "next_target": "1522-Y5-parent-q_loc-scalar-source-profile-and-normalization-first-row.md",
            "script": "scripts/Y5_parent_q_loc_scalar_source_profile_and_normalization_first_row.py",
            "objective": "derive or source the first q_loc scalar-channel profile S_q and normalization N_q needed by both the q_loc-to-q_R bridge and the direct weak-field operator runner",
            "do_not": "do not score Cassini/PPN, do not import q_R, do not assume cancellations, and do not claim local GR",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (QR_BRIDGE_AUDIT, QUAR_BRIDGE),
        (OPERATOR_PROFILE, QUAR_OPERATOR),
        (RUNNER_UPDATE, QUAR_RUNNER),
        (DECISION, QUAR_DECISION),
        (QR_BRIDGE_AUDIT, BRANCH_BRIDGE),
        (OPERATOR_PROFILE, BRANCH_OPERATOR),
        (RUNNER_UPDATE, BRANCH_RUNNER),
        (DECISION, BRANCH_DECISION),
    ]
    for source, destination in copies:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    bridge = read_csv(QR_BRIDGE_AUDIT)
    operator = read_csv(OPERATOR_PROFILE)
    runner = read_csv(RUNNER_UPDATE)
    channels = read_csv(CHANNEL_BUDGET)
    rejections = read_csv(REJECTION_LEDGER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1521_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1521 input source paths exist"),
        ("VAL1521_1_bridge_not_proved", any(row["bridge_id"] == "QBRG1521_6_bridge_verdict" and row["status"] == "QLOC_TO_QR_BRIDGE_NOT_PROVED" for row in bridge), "q_loc-to-q_R bridge remains unproved"),
        ("VAL1521_2_bridge_requirements_complete", len(bridge) >= 7 and any(row["bridge_id"] == "QBRG1521_3_same_normalization" for row in bridge), "bridge audit covers exterior hair, projection, normalization, sign, and retained channels"),
        ("VAL1521_3_operator_profile_staged", any(row["profile_id"] == "OP1521_4_response_coefficient" and row["status"] == "OPERATOR_FORM_ONLY" for row in operator), "operator form for C_qgamma is staged but not evaluated"),
        ("VAL1521_4_runner_blocked", any(row["runner_id"] == "RUN1521_0_bridge_refusal" and row["result"] == "BLOCKED_BRIDGE_AND_OPERATOR_INPUTS_MISSING" for row in runner), "runner refuses missing bridge/operator inputs"),
        ("VAL1521_5_channel_budget_no_cancellation", any(row["channel_id"] == "CH1521_7_acceptance" and row["status"] == "CLAIM_BLOCKED" for row in channels), "retained-channel budget blocks cancellation shortcuts"),
        ("VAL1521_6_rejections_guardrails", len(rejections) >= 5 and all(row["status"] == "REJECTED" for row in rejections), "qR import, skipped integral, fitting, and channel shortcuts rejected"),
        ("VAL1521_7_claim_gates_block_claim", any(row["gate_id"] == "GATE1521_5_local_GR_or_PPN_claim" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates), "local GR/PPN claim remains blocked"),
        ("VAL1521_8_decision_next", any(row["result"] == "NEXT_1522_QLOC_SOURCE_PROFILE" for row in decisions), "decision selects q_loc scalar source profile next"),
        ("VAL1521_9_next_target", any("1522-Y5-parent-q_loc-scalar-source-profile" in row["next_target"] for row in next_rows), "next target is q_loc scalar source profile and normalization"),
        ("VAL1521_10_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1521 CSVs parse cleanly"),
        ("VAL1521_11_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1521_12_branch_copies", all(path.exists() for path in [QUAR_BRIDGE, QUAR_OPERATOR, QUAR_RUNNER, QUAR_DECISION, BRANCH_BRIDGE, BRANCH_OPERATOR, BRANCH_RUNNER, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1521_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1521_14_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1521_15_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1521 refuses q_R import, stages the weak-field operator/source profile, keeps the q_loc gamma runner blocked, and selects q_loc scalar profile/normalization next"
            if overall
            else "1521 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append(
            "| "
            + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns)
            + " |"
        )
    return "\n".join(output)


def write_doc(
    sources: list[dict[str, Any]],
    bridge: list[dict[str, Any]],
    operator: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    channels: list[dict[str, Any]],
    rejections: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    local_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1521 - Parent q_loc-to-qR Bridge or Weak-Field Operator Source Profile",
                "",
                "## Verdict",
                "- The `q_R` policy is real and useful, but it is an exterior scalar-hair convention; it is not automatically the same object as `q_loc^nu`.",
                "- The bridge would close only if `q_loc` projects/integrates to the same `Q_R/r` exterior hair with the same normalization, sign, GM convention, and no retained channels.",
                "- Current MTS does not prove that bridge, so `C_qgamma=-1/2` remains conditional-only and cannot be used as live q_loc evidence.",
                "- The honest fallback is now a weak-field operator/source profile: define `L_PPN`, `R_gamma`, `S_q`, `N_q`, `C_qgamma`, and retained-channel responses before any Cassini/PPN scoring.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "purpose"]),
                "",
                "## q_loc to q_R Bridge Audit",
                md_table(bridge, ["bridge_id", "claim_piece", "required_identity", "status", "why_not_claim"]),
                "",
                "## Weak-Field Operator Source Profile",
                md_table(operator, ["profile_id", "quantity", "definition", "status", "required_input"]),
                "",
                "## q_loc Gamma Runner Update",
                md_table(runner, ["runner_id", "branch", "bridge_status", "q_loc_hat", "C_qgamma_live", "C_qgamma_qR_conditional", "result"]),
                "",
                "## Retained Channel Budget",
                md_table(channels, ["channel_id", "channel", "status", "reason"]),
                "",
                "## Rejection Ledger",
                md_table(rejections, ["rejection_id", "shortcut", "status", "reason"]),
                "",
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "",
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "result", "rationale"]),
                "",
                "## Local GR / Newton Status",
                md_table(local_rows, ["status_id", "claim", "current_status", "reason"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_id", "next_target", "script", "objective", "do_not"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    bridge = qr_bridge_rows()
    operator = operator_profile_rows()
    runner = runner_update_rows()
    channels = channel_budget_rows()
    rejections = rejection_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    local_rows = local_status_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(QR_BRIDGE_AUDIT, bridge)
    write_csv(OPERATOR_PROFILE, operator)
    write_csv(RUNNER_UPDATE, runner)
    write_csv(CHANNEL_BUDGET, channels)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(LOCAL_STATUS, local_rows)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        QR_BRIDGE_AUDIT,
        OPERATOR_PROFILE,
        RUNNER_UPDATE,
        CHANNEL_BUDGET,
        REJECTION_LEDGER,
        CLAIM_GATE,
        DECISION,
        LOCAL_STATUS,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, bridge, operator, runner, channels, rejections, gates, decisions, local_rows, validation, next_rows)


if __name__ == "__main__":
    main()
