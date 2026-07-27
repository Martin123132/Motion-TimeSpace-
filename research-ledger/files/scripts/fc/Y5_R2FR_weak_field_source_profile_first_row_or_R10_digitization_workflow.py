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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1743"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1743 - Weak Field Source Profile First Row Or R10 Digitization Workflow"
UTC = datetime.now(timezone.utc).isoformat()


def yesno(value: bool) -> str:
    return "True" if value else "False"


def no() -> str:
    return "False"


SOURCES = [
    {
        "source_id": "SRC1743_0_1742_doc",
        "source_key": "1742_handoff_doc",
        "source_path": ROOT / "1742-Y5-R2FR-sigmaX-profile-coefficient-or-real-R10-curve.md",
        "needles": ["NEXT1742_0_primary", "VAL1742_OVERALL"],
    },
    {
        "source_id": "SRC1743_1_1742_profile_contract",
        "source_key": "1742_sigmax_contract",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1742_SIGMAX_PROFILE_CONTRACT.csv",
        "needles": ["SXP1742_1_xU_profile", "MISSING_WEAK_FIELD_SOURCE_PROFILE"],
    },
    {
        "source_id": "SRC1743_2_1742_weak_inputs",
        "source_key": "1742_weak_field_input_audit",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1742_WEAK_FIELD_INPUT_AUDIT.csv",
        "needles": ["WFI1742_1_S_q_or_X_source", "MISSING_SOURCE_PROFILE"],
    },
    {
        "source_id": "SRC1743_3_1522_scalar_profile",
        "source_key": "1522_scalar_profile",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1522_SCALAR_SOURCE_PROFILE_DERIVATION.csv",
        "needles": ["SP1522_2_Gamma_gradient_seed", "SOURCE_BACKED_FORMULA_SHAPE_NONCLAIM"],
    },
    {
        "source_id": "SRC1743_4_798_gamma_expansion",
        "source_key": "798_gamma_source_expansion",
        "source_path": RESIDUALS / "P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
        "needles": ["GSE798_4_screened_source_scaling", "conditional_scaling_law"],
    },
    {
        "source_id": "SRC1743_5_1366_envelope",
        "source_key": "1366_q_loc_envelope",
        "source_path": RESIDUALS / "P8_Y5_R10_1366_QLOC_ENVELOPE_INTAKE_ROWS.csv",
        "needles": ["ENV1366_1_memory_gradient_envelope", "PROFILE_MISSING"],
    },
    {
        "source_id": "SRC1743_6_1365_profile_template",
        "source_key": "1365_q_loc_profile",
        "source_path": RESIDUALS / "P8_Y5_R10_1365_QLOC_BOUND_SOURCE_ROW.csv",
        "needles": ["QBR1365_0_q_loc_profile", "CLAIM_BLOCKED_PROFILE_TEMPLATE"],
    },
    {
        "source_id": "SRC1743_7_1289_derivative_kernel",
        "source_key": "1289_first_derivative_kernel",
        "source_path": RESIDUALS / "P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
        "needles": ["KDR1289_1_local_zero_condition_for_chain_kernel", "ZERO_GATE_CONDITIONAL_NOT_DERIVED"],
    },
    {
        "source_id": "SRC1743_8_R10_curve",
        "source_key": "R10_alpha_lambda_curve",
        "source_path": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        "needles": ["MISSING_DIGITIZED_ALPHA_BOUND", "template_invalid_missing_digitized_curve"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1743_SOURCE_REGISTER.csv",
    "weak_field_profile_first_row": RESIDUALS / "P8_Y5_PARENT_QLOC_1743_WEAK_FIELD_PROFILE_FIRST_ROW.csv",
    "profile_derivation_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1743_PROFILE_DERIVATION_AUDIT.csv",
    "sigma_gamma_runner_input": RESIDUALS / "P8_Y5_PARENT_QLOC_1743_SIGMAX_GAMMA_RUNNER_INPUT.csv",
    "r10_digitization_status": RESIDUALS / "P8_Y5_PARENT_QLOC_1743_R10_DIGITIZATION_WORKFLOW_STATUS.csv",
    "runner_refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_1743_RUNNER_REFUSAL.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1743_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1743_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1743_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1743_VALIDATION.csv",
}


COPY_MAP = {
    "weak_field_profile_first_row": "R2FR_1743_WEAK_FIELD_PROFILE_FIRST_ROW.csv",
    "profile_derivation_audit": "R2FR_1743_PROFILE_DERIVATION_AUDIT.csv",
    "sigma_gamma_runner_input": "R2FR_1743_SIGMAX_GAMMA_RUNNER_INPUT.csv",
    "r10_digitization_status": "R2FR_1743_R10_DIGITIZATION_WORKFLOW_STATUS.csv",
    "runner_refusal": "R2FR_1743_RUNNER_REFUSAL.csv",
    "decision": "R2FR_1743_DECISION_LEDGER.csv",
    "claim_gate": "R2FR_1743_CLAIM_GATE.csv",
    "next_target": "R2FR_1743_NEXT_TARGET.csv",
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


def weak_field_profile_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "profile_row_id": "WFP1743_0_Gamma_gradient_shape",
            "quantity": "S_X_shape",
            "definition": "first weak-field scalar/profile source shape feeding X_U or q_loc-like local residual",
            "formula": "S_X := Pi_gamma P_obs P_loc[L_cg^-2 F_prime(m) nabla m - 2 L_cg^-3 F(m) nabla L_cg - div K_hat]",
            "source_formula_anchor": "SP1522_2_Gamma_gradient_seed;GSE798_1_gradient_expansion;SP1522_4_Khat_subtraction",
            "formula_source_backed": "True",
            "units": "MISSING_FORCE_OR_ACCELERATION_NORMALIZATION",
            "needed_to_promote": "Pi_gamma;P_obs;P_loc;Khat_scalar_profile;units;support_domain;boundary_condition;source_path",
            "current_status": "FORMULA_SHAPE_SOURCE_BACKED_INPUTS_MISSING",
            "value_or_formula": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "profile_row_id": "WFP1743_1_screened_scaling_shape",
            "quantity": "x_U_scaling_shape",
            "definition": "screened source-power scaling for the profile coefficient x_U",
            "formula": "x_U = O(U_B^(2pS), U_B^pL, U_B^pT) times operator/support constants",
            "source_formula_anchor": "GSE798_4_screened_source_scaling",
            "formula_source_backed": "True",
            "units": "dimensionless_profile_coefficient_MISSING_NORMALIZATION",
            "needed_to_promote": "U_B;pS;pL;pT;L_tr;operator_constants;boundary_decay;K_perp_control",
            "current_status": "SCALING_LAW_SOURCE_BACKED_POWERS_MISSING",
            "value_or_formula": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "profile_row_id": "WFP1743_2_sigmaX_first_row",
            "quantity": "s_X",
            "definition": "profile coefficient entering sigma_X=s_X U/c^2",
            "formula": "s_X=b_g,X x_U with x_U derived from WFP1743_0 or WFP1743_1",
            "source_formula_anchor": "SXP1742_0_definition;BRM1741_0_conformal_PPN_gamma",
            "formula_source_backed": "True",
            "units": "dimensionless",
            "needed_to_promote": "b_g,X;x_U;source_normalization;no_other_PPN_channels",
            "current_status": "FIRST_ROW_STAGED_PROFILE_NUMERIC_MISSING",
            "value_or_formula": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def profile_derivation_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PDA1743_0_formula_shape",
            "requirement": "profile formula shape",
            "current_evidence": "Gamma_eff gradient identity and Khat subtraction schema exist",
            "status": "PARTIAL_PASS_SOURCE_BACKED_SHAPE",
            "missing": "MISSING_PROJECTORS_UNITS_KHAT_PROFILE",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PDA1743_1_support_powers",
            "requirement": "support powers pS,pL,pT",
            "current_evidence": "screened scaling law exists conditionally",
            "status": "MISSING_SUPPORT_POWER_DERIVATION",
            "missing": "MISSING_U_B_POWERS_TRANSITION_WIDTH_BOUNDARY_DECAY",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PDA1743_2_operator_normalization",
            "requirement": "weak-field operator and GM normalization",
            "current_evidence": "operator/readout schema exists",
            "status": "MISSING_OPERATOR_AND_NORMALIZATION",
            "missing": "MISSING_L_PPN_GAUGE_TRACE_REVERSAL_GM_CONVENTION",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PDA1743_3_no_cancellation",
            "requirement": "no-cancellation retained-channel ledger",
            "current_evidence": "1368 no-cancellation rule active",
            "status": "NO_CANCELLATION_ASSUMPTION_ALLOWED",
            "missing": "MISSING_DELTK_BOUNDARY_SOURCE_MEMORY_INDEPENDENT_ROWS",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def sigma_gamma_runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_input_id": "SGR1743_0_sigmaX_gamma",
            "observable": "gamma_minus_1",
            "prediction_formula": "gamma_minus_1_bg=2s_X/(1-s_X)",
            "linear_bound": "|s_X| <= 1.15e-5",
            "input_s_X": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "input_x_U": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "input_b_g": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "other_channels": "MISSING_NO_OTHER_PPN_CHANNELS",
            "runner_status": "SCHEMA_READY_INPUTS_MISSING",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
    ]


def r10_digitization_status_rows() -> list[dict[str, Any]]:
    curve_rows = read_csv(LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv")
    rows = []
    for index, row in enumerate(curve_rows):
        valid = str(row.get("valid_for_claim", "")).lower() == "true"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "workflow_row_id": f"R10D1743_{index}",
                "source_bound_id": row.get("bound_id", "MISSING_BOUND_ID"),
                "lambda_value": row.get("lambda_value", "MISSING_NUMERIC_LAMBDA"),
                "alpha_bound": row.get("alpha_bound", "MISSING_DIGITIZED_ALPHA_BOUND"),
                "digitization_method": row.get("digitization_method", "MISSING_DIGITIZATION_METHOD"),
                "workflow_status": "REAL_CURVE_AVAILABLE" if valid else "DIGITIZATION_REQUIRED_PLACEHOLDER_ONLY",
                "next_digitization_action": "extract or digitize real lambda-alpha curve from source figure/table before scoring",
                "valid_for_claim": no(),
                "claim_allowed": no(),
            }
        )
    return rows


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1743_0_gamma_score",
            "runner": "sigma_X to Cassini gamma score",
            "current_status": "REFUSE_CLAIM_RUN",
            "reason": "first profile row is formula-shape only; s_X, x_U, b_g and no-other-channel inputs are missing",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1743_1_R10_score",
            "runner": "R10 alpha(lambda) score",
            "current_status": "REFUSE_CLAIM_RUN",
            "reason": "R10 bound curve remains placeholder-only",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1743_0_route_choice",
            "decision": "WEAK_FIELD_PROFILE_FIRST_ROW_CHOSEN",
            "reason": "existing corpus supports a formula-shape profile row; R10 still needs external digitization before scoring",
            "next_action": "promote source-backed shape to first nonclaim profile row",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1743_1_profile_status",
            "decision": "PROFILE_SHAPE_SOURCE_BACKED_NUMERIC_MISSING",
            "reason": "Gamma_eff gradient and screened scaling exist, but projectors, units, support powers, normalization and Khat subtraction are missing",
            "next_action": "derive support powers pS,pL,pT and Khat scalar profile",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1743_2_test_status",
            "decision": "CASSINI_BOUND_READY_PROFILE_NOT",
            "reason": "gamma bound bridge is ready but s_X remains missing",
            "next_action": "keep PPN claim blocked",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1743_3_best_next_domino",
            "decision": "TARGET_SUPPORT_POWERS_AND_KHAT_SCALAR_PROFILE",
            "reason": "these are the exact missing inputs that turn profile shape into x_U",
            "next_action": "derive pS,pL,pT/L_tr support-power gate or Khat scalar subtraction first row",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1743_0_profile_shape",
            "claim": "weak-field profile formula shape exists",
            "gate_pass": "True",
            "status": "PASS_NONCLAIM_ONLY",
            "blocker": "numeric/profile promotion still blocked",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1743_1_xU_value",
            "claim": "x_U profile coefficient is known",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "MISSING_SUPPORT_POWERS_PROJECTORS_UNITS_KHAT_NORMALIZATION",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1743_2_gamma_score",
            "claim": "MTS b_g branch can be scored against Cassini gamma",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "MISSING_SIGMAX_VALUE_AND_NO_OTHER_CHANNELS",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1743_0_primary",
            "next_target": "1744-Y5-R2FR-support-powers-pS-pL-pT-or-Khat-scalar-profile.md",
            "script": "scripts/Y5_R2FR_support_powers_or_Khat_scalar_profile.py",
            "objective": "derive support powers pS,pL,pT/L_tr for x_U, or stage the Khat scalar subtraction profile needed by the weak-field row",
            "success_condition": "source-backed nonclaim support-power row or Khat scalar profile row with units and blockers",
            "selection_status": "selected",
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1743_1_R10_digitization",
            "next_target": "1744b-Y5-R2FR-real-R10-alpha-lambda-digitization-workflow.md",
            "script": "scripts/Y5_R2FR_real_R10_alpha_lambda_digitization_workflow.py",
            "objective": "replace placeholder R10 alpha(lambda) rows with real digitized/source-backed curve rows",
            "success_condition": "positive numeric lambda/alpha rows with source path and valid_for_claim policy separated from MTS prediction rows",
            "selection_status": "held_parallel",
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_allowed": no(),
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_rows(),
        "weak_field_profile_first_row": weak_field_profile_rows(),
        "profile_derivation_audit": profile_derivation_audit_rows(),
        "sigma_gamma_runner_input": sigma_gamma_runner_rows(),
        "r10_digitization_status": r10_digitization_status_rows(),
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
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1743_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1743_{key.upper()}.csv")


def generated_csv_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    flag_fields = {
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
                    if str(value) == "True" and str(row.get("status", "")) == "PASS_NONCLAIM_ONLY":
                        continue
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    readiness = {
        "claim_allowed",
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
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1743_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1743_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1743*"):
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
    profile_rows = rows_map["weak_field_profile_first_row"]
    audit_rows = rows_map["profile_derivation_audit"]
    runner_input = rows_map["sigma_gamma_runner_input"]
    r10_rows = rows_map["r10_digitization_status"]
    runner_rows = rows_map["runner_refusal"]
    decision = rows_map["decision"]
    claim_rows = rows_map["claim_gate"]
    next_rows = rows_map["next_target"]

    validation = [
        check("VAL1743_0_sources_exist", all(row["exists"] == "True" for row in source_register), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1743_1_needles_present", all(row["needles_present"] == "True" for row in source_register), "required source needles are present", "one or more required source needles missing"),
        check("VAL1743_2_profile_shape_row", any(row["profile_row_id"] == "WFP1743_0_Gamma_gradient_shape" and row["formula_source_backed"] == "True" for row in profile_rows), "first weak-field profile formula-shape row is source-backed", "weak-field profile row missing or not source-backed"),
        check("VAL1743_3_scaling_row", any(row["profile_row_id"] == "WFP1743_1_screened_scaling_shape" and row["formula_source_backed"] == "True" for row in profile_rows), "screened scaling law row is staged", "screened scaling row missing"),
        check("VAL1743_4_profile_rows_nonclaim", all(row["score_ready"] == "False" and row["valid_for_claim"] == "False" for row in profile_rows), "profile rows remain nonclaim and not score-ready", "profile row became claim-ready or score-ready"),
        check("VAL1743_5_audit_blocks_profile", all(row["claim_allowed"] == "False" and "MISSING_" in row["missing"] for row in audit_rows), "profile audit preserves missing support/operator/normalization blockers", "profile audit did not preserve missing blockers"),
        check("VAL1743_6_runner_input_blocked", all(row["runner_status"] == "SCHEMA_READY_INPUTS_MISSING" and row["score_ready"] == "False" for row in runner_input), "sigma gamma runner input remains blocked on missing values", "sigma gamma runner input unexpectedly ready"),
        check("VAL1743_7_R10_placeholder", all(row["workflow_status"] == "DIGITIZATION_REQUIRED_PLACEHOLDER_ONLY" and row["claim_allowed"] == "False" for row in r10_rows), "R10 digitization workflow remains placeholder-only", "R10 curve unexpectedly available/claim-ready"),
        check("VAL1743_8_runners_refuse", all(row["current_status"] == "REFUSE_CLAIM_RUN" and row["claim_allowed"] == "False" for row in runner_rows), "claim runners refuse missing profile/R10 inputs", "runner refusal missing or opened claim"),
        check("VAL1743_9_decision_next_domino", any(row["decision_id"] == "DEC1743_3_best_next_domino" and row["decision"] == "TARGET_SUPPORT_POWERS_AND_KHAT_SCALAR_PROFILE" for row in decision), "decision selects support powers and Khat scalar profile", "decision ledger did not select support powers/Khat route"),
        check("VAL1743_10_claim_gates_safe", all(row["claim_allowed"] == "False" for row in claim_rows), "all claim gates keep local claims false", "one or more claim gates opened"),
        check("VAL1743_11_no_claim_flags", no_claim_flags(rows_map), "all generated rows keep claim/no-score flags false except explicit nonclaim pass marker", "one or more generated flags enabled a claim"),
        check("VAL1743_12_missing_not_ready", missing_rows_not_ready(rows_map), "no row containing MISSING_* is marked claim-ready or score-ready", "a missing row is marked ready"),
        check("VAL1743_13_next_selected", any(row["route_id"] == "NEXT1743_0_primary" and row["selection_status"] == "selected" for row in next_rows), "next target selects support powers or Khat scalar profile", "next target missing selected primary route"),
        check("VAL1743_14_csv_parse", parsed_ok, "all generated 1743 CSVs parse", "one or more generated 1743 CSVs failed to parse"),
        check("VAL1743_15_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1743_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1743_17_formalization_untouched", formalization_untouched(), "no 1743 outputs found under formalization-workbench", "1743 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1743_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1743 weak-field source profile first row or R10 digitization workflow validation" if overall else "one or more 1743 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1743 chooses the weak-field profile route because the corpus already contains a source-backed formula shape for `nabla Gamma_eff`, while R10 remains placeholder-only.",
        "- The first weak-field profile row is now staged: `S_X := Pi_gamma P_obs P_loc[L_cg^-2 F'(m)nabla m - 2L_cg^-3F(m)nabla L_cg - div K_hat]`.",
        "- The screened scaling law is also staged: `x_U = O(U_B^(2pS), U_B^pL, U_B^pT)` up to operator/support constants.",
        "- This is not a prediction yet; support powers, projectors, units, Khat scalar subtraction, operator normalization and no-cancellation rows are still missing.",
        "- No local-GR, Newton, PPN, WEP, clock, orbital, R10, or `q_loc=0` claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Weak Field Profile First Row",
        markdown_table(rows_map["weak_field_profile_first_row"], ["profile_row_id", "quantity", "formula", "formula_source_backed", "needed_to_promote", "current_status"]),
        "",
        "## Profile Derivation Audit",
        markdown_table(rows_map["profile_derivation_audit"], ["audit_id", "requirement", "current_evidence", "status", "missing"]),
        "",
        "## sigma_X Gamma Runner Input",
        markdown_table(rows_map["sigma_gamma_runner_input"], ["runner_input_id", "prediction_formula", "linear_bound", "input_s_X", "input_x_U", "runner_status"]),
        "",
        "## R10 Digitization Status",
        markdown_table(rows_map["r10_digitization_status"], ["workflow_row_id", "source_bound_id", "lambda_value", "alpha_bound", "workflow_status", "next_digitization_action"]),
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
        "This is good progress, but it is still pre-score. The profile route now has a concrete formula and a concrete scaling law; the next fight is to derive the support powers `pS,pL,pT` and the `Khat` scalar subtraction so `x_U` stops being a placeholder.",
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
    doc_path = ROOT / "1743-Y5-R2FR-weak-field-source-profile-first-row-or-R10-digitization-workflow.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1743_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1743 validation FAIL")
    print("1743 validation PASS")


if __name__ == "__main__":
    main()
