from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1742"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1742 - sigma_X Profile Coefficient Or Real R10 Curve"
UTC = datetime.now(timezone.utc).isoformat()


def yesno(value: bool) -> str:
    return "True" if value else "False"


def no() -> str:
    return "False"


SOURCES = [
    {
        "source_id": "SRC1742_0_1741_doc",
        "source_key": "1741_handoff_doc",
        "source_path": ROOT / "1741-Y5-R2FR-first-bg-response-map-or-real-R10-bound-curve.md",
        "needles": ["NEXT1741_0_primary", "VAL1741_OVERALL"],
    },
    {
        "source_id": "SRC1742_1_1741_response",
        "source_key": "1741_bg_response_map",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1741_BG_RESPONSE_MAP.csv",
        "needles": ["BRM1741_0_conformal_PPN_gamma", "MISSING_X_U_PROFILE"],
    },
    {
        "source_id": "SRC1742_2_1741_gamma_bridge",
        "source_key": "1741_ppn_gamma_bridge",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1741_PPN_GAMMA_BOUND_BRIDGE.csv",
        "needles": ["PGB1741_0_Cassini_gamma_bridge", "SOURCE_BACKED_CONDITIONAL_NONCLAIM"],
    },
    {
        "source_id": "SRC1742_3_1521_operator_profile",
        "source_key": "1521_weak_field_operator_profile",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1521_WEAK_FIELD_OPERATOR_SOURCE_PROFILE.csv",
        "needles": ["OP1521_7_acceptance", "CLAIM_BLOCKED"],
    },
    {
        "source_id": "SRC1742_4_1522_scalar_profile",
        "source_key": "1522_scalar_source_profile",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1522_SCALAR_SOURCE_PROFILE_DERIVATION.csv",
        "needles": ["SP1522_5_source_profile_verdict", "MISSING_SOURCE_PROFILE"],
    },
    {
        "source_id": "SRC1742_5_1368_projection_requirements",
        "source_key": "1368_projection_requirements",
        "source_path": RESIDUALS / "P8_Y5_R10_1368_QLOC_TO_PPN_GAMMA_PROJECTION_REQUIREMENTS.csv",
        "needles": ["PROJ1368_5_projection_verdict", "PROJECTION_MAP_BLOCKED"],
    },
    {
        "source_id": "SRC1742_6_1369_runner_schema",
        "source_key": "1369_gamma_runner_schema",
        "source_path": RESIDUALS / "P8_Y5_R10_1369_QLOC_GAMMA_RUNNER_SCHEMA.csv",
        "needles": ["QG1369_4_pass_policy", "POLICY_READY_INPUTS_MISSING"],
    },
    {
        "source_id": "SRC1742_7_1520_Cqgamma",
        "source_key": "1520_Cqgamma_derivation",
        "source_path": RESIDUALS / "P8_Y5_PARENT_LCG_1520_CQGAMMA_DERIVATION_ATTEMPT.csv",
        "needles": ["CQG1520_4_live_value", "NOT_SCORE_READY"],
    },
    {
        "source_id": "SRC1742_8_R10_curve",
        "source_key": "R10_alpha_lambda_curve",
        "source_path": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        "needles": ["MISSING_DIGITIZED_ALPHA_BOUND", "template_invalid_missing_digitized_curve"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1742_SOURCE_REGISTER.csv",
    "sigma_profile_contract": RESIDUALS / "P8_Y5_PARENT_QLOC_1742_SIGMAX_PROFILE_CONTRACT.csv",
    "weak_field_input_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1742_WEAK_FIELD_INPUT_AUDIT.csv",
    "gamma_bound_application": RESIDUALS / "P8_Y5_PARENT_QLOC_1742_GAMMA_BOUND_APPLICATION.csv",
    "r10_curve_status": RESIDUALS / "P8_Y5_PARENT_QLOC_1742_R10_CURVE_STATUS.csv",
    "runner_refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_1742_RUNNER_REFUSAL.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1742_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1742_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1742_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1742_VALIDATION.csv",
}


COPY_MAP = {
    "sigma_profile_contract": "R2FR_1742_SIGMAX_PROFILE_CONTRACT.csv",
    "weak_field_input_audit": "R2FR_1742_WEAK_FIELD_INPUT_AUDIT.csv",
    "gamma_bound_application": "R2FR_1742_GAMMA_BOUND_APPLICATION.csv",
    "r10_curve_status": "R2FR_1742_R10_CURVE_STATUS.csv",
    "runner_refusal": "R2FR_1742_RUNNER_REFUSAL.csv",
    "decision": "R2FR_1742_DECISION_LEDGER.csv",
    "claim_gate": "R2FR_1742_CLAIM_GATE.csv",
    "next_target": "R2FR_1742_NEXT_TARGET.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def source_rows() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": yesno(exists),
                "needles": ";".join(needles),
                "needles_present": yesno(exists and all(needle in text for needle in needles)),
                "checked_utc": UTC,
            }
        )
    return rows


def r10_curve_rows() -> list[dict[str, str]]:
    return read_csv(LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv")


def sigma_profile_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "profile_id": "SXP1742_0_definition",
            "quantity": "s_X",
            "definition": "dimensionless Newtonian-potential profile coefficient in sigma_X=s_X U/c^2",
            "formula": "s_X=b_g,X x_U",
            "units": "dimensionless",
            "required_inputs": "b_g,X;x_U_profile;source_normalization;support_domain;source_path",
            "current_status": "MISSING_BG_VALUE_AND_X_U_PROFILE",
            "value_or_formula": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "source_path": "MISSING_SOURCE_PATH",
            "accepted_for_scoring": no(),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "profile_id": "SXP1742_1_xU_profile",
            "quantity": "x_U",
            "definition": "coefficient relating the residual/profile X to the Newtonian potential U/c^2",
            "formula": "X(r)=x_U U(r)/c^2 + non_scalar_or_boundary_terms",
            "units": "X_units_per_dimensionless_potential_MISSING",
            "required_inputs": "weak_field_operator;source_profile;GM_normalization;boundary_condition;gauge",
            "current_status": "MISSING_WEAK_FIELD_SOURCE_PROFILE",
            "value_or_formula": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "source_path": "MISSING_SOURCE_PATH",
            "accepted_for_scoring": no(),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "profile_id": "SXP1742_2_gamma_prediction",
            "quantity": "gamma_minus_1_bg",
            "definition": "PPN gamma residual from conformal common-frame coefficient",
            "formula": "gamma_minus_1_bg=2 s_X/(1-s_X) ~= 2s_X",
            "units": "dimensionless",
            "required_inputs": "s_X;no_other_PPN_channels;Cassini_bound_policy",
            "current_status": "MISSING_SIGMAX_VALUE",
            "value_or_formula": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "source_path": "MISSING_SOURCE_PATH",
            "accepted_for_scoring": no(),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def weak_field_input_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "input_id": "WFI1742_0_L_PPN",
            "input": "linearized weak-field operator",
            "needed_for": "solve X or metric response relative to U",
            "source_anchor": "OP1521_0_linear_operator",
            "current_status": "MISSING_OPERATOR",
            "blocker": "gauge, trace reversal, areal-radial convention and boundary condition are not fixed",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "WFI1742_1_S_q_or_X_source",
            "input": "scalar source profile",
            "needed_for": "derive X(r)=x_U U/c^2",
            "source_anchor": "SP1522_5_source_profile_verdict",
            "current_status": "MISSING_SOURCE_PROFILE",
            "blocker": "P_loc, Pi_gamma, Khat subtraction, units and support are missing",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "WFI1742_2_normalization",
            "input": "GM/source normalization",
            "needed_for": "compare profile amplitude to Cassini PPN U",
            "source_anchor": "OP1521_3_normalization",
            "current_status": "MISSING_NORMALIZATION",
            "blocker": "same measured GM/source convention is not supplied",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "WFI1742_3_no_cancellation",
            "input": "retained-channel ledger",
            "needed_for": "use gamma bridge without cancellation assumptions",
            "source_anchor": "PROJ1368_4_no_cancellation_rule",
            "current_status": "NO_CANCELLATION_ASSUMPTION_ALLOWED",
            "blocker": "q_loc, DeltaK, boundary, source and memory channels need independent zero/bounds",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "WFI1742_4_C_qgamma",
            "input": "gamma response coefficient",
            "needed_for": "general response beyond conformal toy bridge",
            "source_anchor": "CQG1520_4_live_value",
            "current_status": "NOT_SCORE_READY",
            "blocker": "q_loc_hat, normalization, operator, source averaging and channel split are missing",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def gamma_bound_application_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "application_id": "GBA1742_0_linear_bound",
            "observable": "gamma_minus_1",
            "bound": "2.3e-5",
            "conditional_prediction": "gamma_minus_1_bg ~= 2s_X",
            "conditional_limit": "|s_X| <= 1.15e-5",
            "status": "BOUND_READY_PROFILE_MISSING",
            "missing_to_score": "MISSING_SIGMAX_VALUE;MISSING_NO_OTHER_CHANNELS;MISSING_SOURCE_NORMALIZATION",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "application_id": "GBA1742_1_exact_bound",
            "observable": "gamma_minus_1",
            "bound": "2.3e-5",
            "conditional_prediction": "gamma_minus_1_bg=2s_X/(1-s_X)",
            "conditional_limit": "|2s_X/(1-s_X)| <= 2.3e-5",
            "status": "BOUND_READY_PROFILE_MISSING",
            "missing_to_score": "MISSING_SIGMAX_VALUE;MISSING_SIGN_DOMAIN;MISSING_OTHER_CHANNEL_LEDGER",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def r10_curve_status_rows() -> list[dict[str, Any]]:
    rows = []
    for index, row in enumerate(r10_curve_rows()):
        valid = str(row.get("valid_for_claim", "")).lower() == "true"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "curve_row_id": f"R10CURVE1742_{index}",
                "source_bound_id": row.get("bound_id", "MISSING_BOUND_ID"),
                "lambda_value": row.get("lambda_value", "MISSING_NUMERIC_LAMBDA"),
                "alpha_bound": row.get("alpha_bound", "MISSING_DIGITIZED_ALPHA_BOUND"),
                "digitization_method": row.get("digitization_method", "MISSING_DIGITIZATION_METHOD"),
                "source_valid_for_claim": yesno(valid),
                "curve_status": "REAL_CURVE_AVAILABLE" if valid else "PLACEHOLDER_NONCLAIM",
                "valid_for_claim": no(),
                "claim_allowed": no(),
            }
        )
    return rows


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1742_0_gamma_score",
            "runner": "sigma_X to Cassini gamma score",
            "current_status": "REFUSE_CLAIM_RUN",
            "reason": "s_X value/profile and no-other-channel proof are missing",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1742_1_R10_score",
            "runner": "R10 alpha(lambda) score",
            "current_status": "REFUSE_CLAIM_RUN",
            "reason": "R10 alpha(lambda) curve is still placeholder/nonclaim",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1742_0_profile_contract",
            "decision": "SIGMAX_PROFILE_CONTRACT_STAGED",
            "reason": "1741 response map reduced the empirical question to s_X=b_g,X x_U",
            "next_action": "derive/source x_U or b_g value before any PPN scoring",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1742_1_current_status",
            "decision": "SIGMAX_VALUE_MISSING",
            "reason": "weak-field operator, source profile, normalization and no-cancellation ledger remain missing",
            "next_action": "keep PPN gamma claim blocked",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1742_2_R10_status",
            "decision": "R10_CURVE_STILL_PLACEHOLDER",
            "reason": "local R10 alpha(lambda) file contains placeholder rows only",
            "next_action": "real digitization/acquisition is still required before R10 scoring",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1742_3_best_next_domino",
            "decision": "TARGET_WEAK_FIELD_SOURCE_PROFILE_OR_R10_DIGITIZATION",
            "reason": "the PPN bridge needs x_U; the R10 bridge needs real alpha(lambda)",
            "next_action": "derive first weak-field source/profile row, or run a real R10 curve acquisition workflow",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1742_0_sX_profile",
            "claim": "s_X profile coefficient is known",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "MISSING_X_U_PROFILE_AND_BG_VALUE",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1742_1_gamma_score",
            "claim": "MTS b_g branch passes Cassini gamma",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "MISSING_SIGMAX_VALUE_AND_NO_OTHER_CHANNELS",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1742_2_R10_score",
            "claim": "R10 alpha(lambda) curve is score-ready",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "MISSING_REAL_R10_CURVE",
            "claim_allowed": no(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1742_0_primary",
            "next_target": "1743-Y5-R2FR-weak-field-source-profile-first-row-or-R10-digitization-workflow.md",
            "script": "scripts/Y5_R2FR_weak_field_source_profile_first_row_or_R10_digitization_workflow.py",
            "objective": "derive/source the first weak-field X_U profile input for sigma_X, or run a real R10 alpha(lambda) curve acquisition workflow",
            "success_condition": "first source-backed nonclaim weak-field profile row or real R10 curve rows replacing placeholders",
            "selection_status": "selected",
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1742_1_parallel_readout_marker",
            "next_target": "1743b-Y5-R2FR-source-readout-marker-Dq-zero-or-finite-row.md",
            "script": "scripts/Y5_R2FR_source_readout_marker_Dq_zero_or_finite_row.py",
            "objective": "prove source/readout and marker functors descend through q, or keep finite leak rows",
            "success_condition": "source/readout and marker rows source-backed with units and nonclaim comparisons",
            "selection_status": "held_parallel",
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_allowed": no(),
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_rows(),
        "sigma_profile_contract": sigma_profile_contract_rows(),
        "weak_field_input_audit": weak_field_input_audit_rows(),
        "gamma_bound_application": gamma_bound_application_rows(),
        "r10_curve_status": r10_curve_status_rows(),
        "runner_refusal": runner_refusal_rows(),
        "decision": decision_rows(),
        "claim_gate": claim_gate_rows(),
        "next_target": next_target_rows(),
    }


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    def cell(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "\\|")

    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def copy_outputs() -> None:
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1742_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1742_{key.upper()}.csv")


def generated_csv_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    flag_fields = {
        "accepted_for_scoring",
        "claim_allowed",
        "gate_pass",
        "score_allowed",
        "score_ready",
        "valid_for_claim",
        "valid_prediction_row",
    }
    for rows in rows_map.values():
        for row in rows:
            for key, value in row.items():
                if key in flag_fields and str(value).lower() != "false":
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    readiness = {
        "accepted_for_scoring",
        "claim_allowed",
        "gate_pass",
        "score_ready",
        "valid_for_claim",
        "valid_prediction_row",
    }
    for rows in rows_map.values():
        for row in rows:
            contains_missing = any("MISSING_" in str(value) for value in row.values())
            if contains_missing and any(str(row.get(flag, "")).lower() == "true" for flag in readiness):
                return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1742_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1742_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1742*"):
        path_text = str(path)
        if "\\.venv\\" in path_text or "\\__pycache__\\" in path_text:
            continue
        if path.is_file():
            return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    def check(check_id: str, result: bool, detail_pass: str, detail_fail: str) -> dict[str, Any]:
        return {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail_pass if result else detail_fail,
        }

    parsed_ok = True
    try:
        for path in generated_csv_paths():
            read_csv(path)
    except Exception:
        parsed_ok = False

    source_register = rows_map["source_register"]
    profile_rows = rows_map["sigma_profile_contract"]
    weak_inputs = rows_map["weak_field_input_audit"]
    gamma_rows = rows_map["gamma_bound_application"]
    r10_status = rows_map["r10_curve_status"]
    runner_rows = rows_map["runner_refusal"]
    decision = rows_map["decision"]
    claim_rows = rows_map["claim_gate"]
    next_rows = rows_map["next_target"]

    validation = [
        check("VAL1742_0_sources_exist", all(row["exists"] == "True" for row in source_register), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1742_1_needles_present", all(row["needles_present"] == "True" for row in source_register), "required source needles are present", "one or more required source needles missing"),
        check("VAL1742_2_sigma_contract_present", any(row["profile_id"] == "SXP1742_0_definition" for row in profile_rows), "sigma_X profile coefficient contract is staged", "sigma_X profile contract missing"),
        check("VAL1742_3_profile_rows_nonclaim", all(row["score_ready"] == "False" and row["valid_for_claim"] == "False" for row in profile_rows), "sigma profile rows are nonclaim and not score-ready", "sigma profile row became claim-ready"),
        check("VAL1742_4_weak_inputs_audited", {row["input_id"] for row in weak_inputs} == {"WFI1742_0_L_PPN", "WFI1742_1_S_q_or_X_source", "WFI1742_2_normalization", "WFI1742_3_no_cancellation", "WFI1742_4_C_qgamma"}, "weak-field source/profile inputs are audited", "weak-field input audit missing row"),
        check("VAL1742_5_gamma_bound_ready_profile_missing", all(row["status"] == "BOUND_READY_PROFILE_MISSING" for row in gamma_rows), "gamma bound application is ready but profile missing", "gamma bound application status unexpected"),
        check("VAL1742_6_R10_placeholder_blocked", all(row["curve_status"] == "PLACEHOLDER_NONCLAIM" and row["claim_allowed"] == "False" for row in r10_status), "R10 curve remains placeholder/nonclaim", "R10 curve unexpectedly claim-ready"),
        check("VAL1742_7_runners_refuse", all(row["current_status"] == "REFUSE_CLAIM_RUN" and row["claim_allowed"] == "False" for row in runner_rows), "claim runners refuse missing profile/R10 inputs", "runner refusal missing or opened claim"),
        check("VAL1742_8_decision_next_domino", any(row["decision_id"] == "DEC1742_3_best_next_domino" and row["decision"] == "TARGET_WEAK_FIELD_SOURCE_PROFILE_OR_R10_DIGITIZATION" for row in decision), "decision selects weak-field profile or R10 digitization", "decision ledger did not select weak-field/R10 route"),
        check("VAL1742_9_claim_gates_safe", all(row["gate_pass"] == "False" and row["claim_allowed"] == "False" for row in claim_rows), "all claim gates keep local claims false", "one or more claim gates opened"),
        check("VAL1742_10_no_claim_flags", no_claim_flags(rows_map), "all generated rows keep claim/no-score flags false", "one or more generated flags enabled a claim"),
        check("VAL1742_11_missing_not_ready", missing_rows_not_ready(rows_map), "no row containing MISSING_* is marked claim-ready or score-ready", "a missing row is marked ready"),
        check("VAL1742_12_next_selected", any(row["route_id"] == "NEXT1742_0_primary" and row["selection_status"] == "selected" for row in next_rows), "next target selects weak-field source profile or R10 digitization workflow", "next target missing selected primary route"),
        check("VAL1742_13_csv_parse", parsed_ok, "all generated 1742 CSVs parse", "one or more generated 1742 CSVs failed to parse"),
        check("VAL1742_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1742_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1742_16_formalization_untouched", formalization_untouched(), "no 1742 outputs found under formalization-workbench", "1742 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1742_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1742 sigma_X profile coefficient or real R10 curve validation" if overall else "one or more 1742 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1742 stages the missing profile coefficient explicitly: `s_X=b_g,X x_U` in `sigma_X=s_X U/c^2`.",
        "- The Cassini gamma bridge is ready as a conditional bound, but no MTS score is possible until `s_X` is derived or sourced.",
        "- The weak-field audit shows why: operator, scalar source profile, GM normalization, response coefficient and no-cancellation ledger are still missing.",
        "- The R10 curve remains placeholder-only, so R10 scoring is still blocked.",
        "- No local-GR, Newton, PPN, WEP, clock, orbital, R10, or `q_loc=0` claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## sigma_X Profile Contract",
        markdown_table(rows_map["sigma_profile_contract"], ["profile_id", "quantity", "formula", "required_inputs", "current_status", "value_or_formula"]),
        "",
        "## Weak Field Input Audit",
        markdown_table(rows_map["weak_field_input_audit"], ["input_id", "input", "needed_for", "current_status", "blocker"]),
        "",
        "## Gamma Bound Application",
        markdown_table(rows_map["gamma_bound_application"], ["application_id", "conditional_prediction", "conditional_limit", "status", "missing_to_score"]),
        "",
        "## R10 Curve Status",
        markdown_table(rows_map["r10_curve_status"], ["curve_row_id", "source_bound_id", "lambda_value", "alpha_bound", "digitization_method", "curve_status"]),
        "",
        "## Runner Refusal",
        markdown_table(rows_map["runner_refusal"], ["runner_id", "runner", "current_status", "reason"]),
        "",
        "## Decisions",
        markdown_table(rows_map["decision"], ["decision_id", "decision", "reason", "next_action"]),
        "",
        "## Claim Gates",
        markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "status", "blocker"]),
        "",
        "## Next Target",
        markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
        "",
        "## Validation",
        markdown_table(validation_rows, ["check_id", "result", "detail"]),
        "",
        "## Working Interpretation",
        "The PPN route is now concrete but not scoreable. The next thing to hunt is not another broad theory slogan; it is the first weak-field source/profile row that gives `x_U`, or a real R10 curve if we want the short-range test to move first.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    cleanup_pycache()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1742-Y5-R2FR-sigmaX-profile-coefficient-or-real-R10-curve.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1742_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1742 validation FAIL")
    print("1742 validation PASS")


if __name__ == "__main__":
    main()
