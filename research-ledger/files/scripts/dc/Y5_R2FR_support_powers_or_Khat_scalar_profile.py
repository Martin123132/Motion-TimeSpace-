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
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1744"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1744 - Support Powers pS pL pT Or Khat Scalar Profile"
UTC = datetime.now(timezone.utc).isoformat()


def yesno(value: bool) -> str:
    return "True" if value else "False"


def no() -> str:
    return "False"


SOURCES = [
    {
        "source_id": "SRC1744_0_1743_doc",
        "source_key": "1743_handoff_doc",
        "source_path": ROOT / "1743-Y5-R2FR-weak-field-source-profile-first-row-or-R10-digitization-workflow.md",
        "needles": ["NEXT1743_0_primary", "VAL1743_OVERALL"],
    },
    {
        "source_id": "SRC1744_1_1743_profile_row",
        "source_key": "1743_weak_profile_first_row",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1743_WEAK_FIELD_PROFILE_FIRST_ROW.csv",
        "needles": ["WFP1743_1_screened_scaling_shape", "SCALING_LAW_SOURCE_BACKED_POWERS_MISSING"],
    },
    {
        "source_id": "SRC1744_2_799_support_gates",
        "source_key": "799_support_power_gates",
        "source_path": RESIDUALS / "P8_Y5_R10_799_SUPPORT_POWER_GATES.csv",
        "needles": ["SPG799_1_pS", "SPG799_5_pK"],
    },
    {
        "source_id": "SRC1744_3_800_support_audit",
        "source_key": "800_support_power_derivation",
        "source_path": RESIDUALS / "P8_Y5_R10_800_SUPPORT_POWER_DERIVATION_AUDIT.csv",
        "needles": ["SPD800_5_verdict", "not_derived_as_parent_theorem"],
    },
    {
        "source_id": "SRC1744_4_798_gamma_expansion",
        "source_key": "798_gamma_expansion",
        "source_path": RESIDUALS / "P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
        "needles": ["GSE798_4_screened_source_scaling", "conditional_scaling_law"],
    },
    {
        "source_id": "SRC1744_5_1524_Khat_profile",
        "source_key": "1524_Khat_DeltaK_profile",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1524_KHAT_DELTAK_SCALAR_PROFILE.csv",
        "needles": ["KDS1524_5_verdict", "MISSING_SCALAR_PROFILE"],
    },
    {
        "source_id": "SRC1744_6_833_Khat_amplitude",
        "source_key": "833_Hessian_Khat_amplitude",
        "source_path": RESIDUALS / "P8_Y5_R10_833_HESSIAN_KHAT_AMPLITUDE_LAW.csv",
        "needles": ["AL833_3_Newton_fraction_gate", "epsilon_K_bound_formula"],
    },
    {
        "source_id": "SRC1744_7_1522_scalar_profile",
        "source_key": "1522_scalar_source_profile",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1522_SCALAR_SOURCE_PROFILE_DERIVATION.csv",
        "needles": ["SP1522_4_Khat_subtraction", "MISSING_KHAT_SCALAR_PROFILE"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1744_SOURCE_REGISTER.csv",
    "support_power_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1744_SUPPORT_POWER_GATE.csv",
    "support_power_candidate": RESIDUALS / "P8_Y5_PARENT_QLOC_1744_SUPPORT_POWER_CANDIDATE_ROW.csv",
    "khat_scalar_profile": RESIDUALS / "P8_Y5_PARENT_QLOC_1744_KHAT_SCALAR_PROFILE_ROW.csv",
    "xU_promotion_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1744_XU_PROMOTION_GATE.csv",
    "runner_refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_1744_RUNNER_REFUSAL.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1744_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1744_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1744_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1744_VALIDATION.csv",
}


COPY_MAP = {
    "support_power_gate": "R2FR_1744_SUPPORT_POWER_GATE.csv",
    "support_power_candidate": "R2FR_1744_SUPPORT_POWER_CANDIDATE_ROW.csv",
    "khat_scalar_profile": "R2FR_1744_KHAT_SCALAR_PROFILE_ROW.csv",
    "xU_promotion_gate": "R2FR_1744_XU_PROMOTION_GATE.csv",
    "runner_refusal": "R2FR_1744_RUNNER_REFUSAL.csv",
    "decision": "R2FR_1744_DECISION_LEDGER.csv",
    "claim_gate": "R2FR_1744_CLAIM_GATE.csv",
    "next_target": "R2FR_1744_NEXT_TARGET.csv",
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


def support_power_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "power_id": "SP1744_0_pS",
            "power": "pS",
            "candidate_value": "1",
            "derivation_status": "CONDITIONAL_FROM_V0_SOURCE_LAW",
            "evidence": "open-system source has U_B S_cg, so pS=1 if S_cg is bounded and no hidden source survives",
            "missing_to_promote": "MISSING_BOUNDED_SCG;MISSING_NO_HIDDEN_SOURCE_CHANNEL",
        },
        {
            "power_id": "SP1744_1_pL",
            "power": "pL",
            "candidate_value": "1_generic_or_2_if_double_zero",
            "derivation_status": "DOUBLE_ZERO_NOT_DERIVED",
            "evidence": "generic smooth m_L(U_B)=m_*+a1 U_B+... gives pL=1; pL=2 requires a1=0 fixed-point/double-zero mechanism",
            "missing_to_promote": "MISSING_LOCAL_FIXED_POINT_DOUBLE_ZERO_FOR_ML",
        },
        {
            "power_id": "SP1744_2_pT",
            "power": "pT",
            "candidate_value": "1_generic_or_2_if_trace_double_zero",
            "derivation_status": "TRACE_DOUBLE_ZERO_NOT_DERIVED",
            "evidence": "generic trace baseline has b1 U_B drift; pT=2 requires trace-baseline double zero",
            "missing_to_promote": "MISSING_TRACE_BASELINE_DOUBLE_ZERO",
        },
        {
            "power_id": "SP1744_3_pB",
            "power": "pB",
            "candidate_value": "MISSING_OR_>=2_IF_BOUNDARY_SILENCE",
            "derivation_status": "BOUNDARY_SILENCE_NOT_DERIVED",
            "evidence": "scalar Pi_B law alone gives no boundary/source-measure power",
            "missing_to_promote": "MISSING_BOUNDARY_SOURCE_MEASURE_SILENCE",
        },
        {
            "power_id": "SP1744_4_pK",
            "power": "pK",
            "candidate_value": "pB_if_coercive_Kperp_operator_else_MISSING",
            "derivation_status": "KPERP_BOUND_CONDITIONAL_ONLY",
            "evidence": "coercive tensor operator with zero/decay boundary would give pK=pB, but operator and boundary data are unsigned",
            "missing_to_promote": "MISSING_COERCIVE_TENSOR_OPERATOR;MISSING_NO_ZERO_MODE;MISSING_BOUNDARY_DATA",
        },
    ]
    for row in rows:
        row.update(
            {
                "branch_id": BRANCH_ID,
                "valid_for_claim": no(),
                "claim_allowed": no(),
                "score_ready": no(),
            }
        )
    return rows


def support_power_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "candidate_id": "SPC1744_0_minimal_finite_margin_set",
            "candidate_set": "pS=1,pL=2,pT=2,pB>=2,pK>=2_or_Kperp=0",
            "source_anchor": "SPD800_5_verdict",
            "status": "CLOSURE_LEVEL_NOT_PARENT_DERIVED",
            "why": "only pS has conditional support; pL/pT double zeros, pB boundary silence and pK tensor control are not derived",
            "effect_if_signed": "x_U becomes parametrically suppressed by U_B powers rather than a free coefficient",
            "value_or_formula": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_ready": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "candidate_id": "SPC1744_1_conservative_generic_set",
            "candidate_set": "pS=1,pL=1,pT=1,pB=MISSING,pK=MISSING",
            "source_anchor": "SPD800_0_to_SPD800_4",
            "status": "GENERIC_UNSAFE_FOR_LOCAL_GR",
            "why": "linear pL/pT drift and missing boundary/tensor powers can reintroduce local PPN/fifth-force sources",
            "effect_if_signed": "not enough for local-GR pass; remains finite residual route",
            "value_or_formula": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_ready": no(),
        },
    ]


def khat_scalar_profile_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "khat_row_id": "KSP1744_0_scalar_DeltaK_channel",
            "quantity": "S_Delta",
            "definition": "Khat/Kmetric scalar subtraction entering the weak-field profile",
            "formula": "S_Delta := -Pi_gamma[P_loc nabla_mu Delta_K^{mu nu}], Delta_K=K_hat-K_metric[Gamma_eff]",
            "source_anchor": "KDS1524_3_scalar_DeltaK_channel",
            "status": "SCALAR_CHANNEL_SCHEMA_WRITTEN_INPUTS_MISSING",
            "needed_to_promote": "Pi_gamma;P_loc;Delta_K_components;response_coefficients;units;boundary_terms",
            "value_or_formula": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_ready": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "khat_row_id": "KSP1744_1_Khat_amplitude_guard",
            "quantity": "epsilon_K",
            "definition": "Newton/PPN fraction from Hessian Khat carrier if it enters the metric source",
            "formula": "epsilon_K ~= metric_response_coeff * |Kbar_00| / |4 pi G rho/c^2|, with |Kbar_00| <= f_00 sqrt(n/(n-1)) ||Gamma||",
            "source_anchor": "AL833_3_Newton_fraction_gate",
            "status": "BOUND_FORMULA_SOURCE_BACKED_INPUTS_MISSING",
            "needed_to_promote": "Gamma_loc;f_00;matter_curvature;response_coefficient;units",
            "value_or_formula": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_ready": no(),
        },
    ]


def xu_promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "XUP1744_0_support_power_gate",
            "requirement": "support powers sufficient for x_U",
            "needed": "pS,pL,pT,pB,pK plus U_B,L_tr/operator constants",
            "current_status": "BLOCKED_DOUBLE_ZERO_BOUNDARY_TENSOR_MISSING",
            "effect": "x_U cannot be promoted from scaling shape to numeric/source-backed row",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "XUP1744_1_Khat_subtraction_gate",
            "requirement": "Khat scalar subtraction is zero or bounded",
            "needed": "S_Delta row or theorem-zero certificate",
            "current_status": "BLOCKED_KHAT_SCALAR_PROFILE_MISSING",
            "effect": "profile source cannot be compared to Cassini without retained channel budget",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "XUP1744_2_gamma_runner_gate",
            "requirement": "sigma_X gamma runner can score",
            "needed": "s_X numeric/source-backed, no-other-channel ledger, Cassini bound",
            "current_status": "BLOCKED_SIGMAX_NUMERIC_MISSING",
            "effect": "no PPN score or local-GR claim",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1744_0_support_power_calculator",
            "runner": "x_U support-power calculator",
            "current_status": "REFUSE_CLAIM_RUN",
            "reason": "pL/pT double zeros, pB/pK boundary/tensor powers, U_B and operator constants are missing",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1744_1_Khat_scalar_runner",
            "runner": "Khat scalar subtraction profile",
            "current_status": "REFUSE_CLAIM_RUN",
            "reason": "Delta_K components, projectors, units and response coefficients are missing",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1744_0_support_power_status",
            "decision": "PS_CONDITIONAL_PL_PT_NOT_DERIVED",
            "reason": "pS=1 follows conditionally from U_B S_cg, but pL/pT need double-zero mechanisms",
            "next_action": "derive the local fixed-point/double-zero route or keep pL/pT generic and unsafe",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1744_1_Khat_status",
            "decision": "KHAT_SCALAR_PROFILE_SCHEMA_ONLY",
            "reason": "S_Delta formula exists but Delta_K components/projectors/units are missing",
            "next_action": "stage Khat scalar subtraction first row before scoring",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1744_2_profile_status",
            "decision": "XU_NOT_PROMOTED",
            "reason": "support powers and Khat subtraction remain nonclaim",
            "next_action": "keep Cassini gamma runner blocked",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1744_3_best_next_domino",
            "decision": "TARGET_DOUBLE_ZERO_FOR_PL_PT_OR_KHAT_COMPONENTS",
            "reason": "pL/pT double zeros or Khat scalar components are the smallest missing proof inputs",
            "next_action": "attempt fixed-point double-zero for m_L/trace baseline or fill Delta_K component row",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1744_0_support_powers",
            "claim": "support powers are sufficient for local suppression",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "MISSING_PL_PT_DOUBLE_ZERO_PB_PK_CONTROL",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1744_1_Khat_scalar",
            "claim": "Khat scalar subtraction is zero or bounded",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "MISSING_DELTAK_COMPONENTS_PROJECTORS_UNITS",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1744_2_local_GR",
            "claim": "local GR/Newton limit follows through profile suppression",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "XU_NOT_PROMOTED_NO_SIGMAX_SCORE",
            "claim_allowed": no(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1744_0_primary",
            "next_target": "1745-Y5-R2FR-fixed-point-double-zero-for-pL-pT-or-DeltaK-component-row.md",
            "script": "scripts/Y5_R2FR_fixed_point_double_zero_or_DeltaK_component_row.py",
            "objective": "derive pL/pT double-zero from local fixed-point mechanism, or fill first Delta_K/Khat scalar component row",
            "success_condition": "parent-signed double-zero theorem for m_L/trace baseline or source-backed nonclaim Delta_K component row",
            "selection_status": "selected",
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1744_1_R10_digitization",
            "next_target": "1745b-Y5-R2FR-real-R10-alpha-lambda-digitization-workflow.md",
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
        "support_power_gate": support_power_gate_rows(),
        "support_power_candidate": support_power_candidate_rows(),
        "khat_scalar_profile": khat_scalar_profile_rows(),
        "xU_promotion_gate": xu_promotion_gate_rows(),
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
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1744_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1744_{key.upper()}.csv")


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
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    readiness = {
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
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1744_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1744_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1744*"):
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
    support_rows = rows_map["support_power_gate"]
    candidate_rows = rows_map["support_power_candidate"]
    khat_rows = rows_map["khat_scalar_profile"]
    xu_rows = rows_map["xU_promotion_gate"]
    runner_rows = rows_map["runner_refusal"]
    decision = rows_map["decision"]
    claim_rows = rows_map["claim_gate"]
    next_rows = rows_map["next_target"]

    validation = [
        check("VAL1744_0_sources_exist", all(row["exists"] == "True" for row in source_register), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1744_1_needles_present", all(row["needles_present"] == "True" for row in source_register), "required source needles are present", "one or more required source needles missing"),
        check("VAL1744_2_support_rows_complete", {row["power"] for row in support_rows} == {"pS", "pL", "pT", "pB", "pK"}, "support power gate covers pS,pL,pT,pB,pK", "support power gate missing power row"),
        check("VAL1744_3_pS_conditional_only", any(row["power"] == "pS" and row["derivation_status"] == "CONDITIONAL_FROM_V0_SOURCE_LAW" for row in support_rows), "pS=1 is retained as conditional only", "pS conditional row missing"),
        check("VAL1744_4_double_zero_blocked", any(row["power"] == "pL" and row["derivation_status"] == "DOUBLE_ZERO_NOT_DERIVED" for row in support_rows) and any(row["power"] == "pT" and row["derivation_status"] == "TRACE_DOUBLE_ZERO_NOT_DERIVED" for row in support_rows), "pL/pT double-zero blockers are explicit", "pL/pT blockers missing"),
        check("VAL1744_5_candidate_nonclaim", all(row["score_ready"] == "False" and row["valid_for_claim"] == "False" for row in candidate_rows), "support power candidates remain nonclaim", "support candidate became claim-ready"),
        check("VAL1744_6_Khat_rows_nonclaim", all(row["score_ready"] == "False" and row["valid_for_claim"] == "False" for row in khat_rows), "Khat scalar rows are nonclaim", "Khat row became claim-ready"),
        check("VAL1744_7_xU_gates_blocked", all(row["claim_allowed"] == "False" and row["current_status"].startswith("BLOCKED") for row in xu_rows), "x_U promotion gates remain blocked", "x_U promotion gate opened"),
        check("VAL1744_8_runners_refuse", all(row["current_status"] == "REFUSE_CLAIM_RUN" and row["claim_allowed"] == "False" for row in runner_rows), "claim runners refuse support/Khat missing inputs", "runner refusal missing or opened claim"),
        check("VAL1744_9_decision_next_domino", any(row["decision_id"] == "DEC1744_3_best_next_domino" and row["decision"] == "TARGET_DOUBLE_ZERO_FOR_PL_PT_OR_KHAT_COMPONENTS" for row in decision), "decision selects double-zero or Khat component row", "decision ledger did not select double-zero/Khat route"),
        check("VAL1744_10_claim_gates_safe", all(row["gate_pass"] == "False" and row["claim_allowed"] == "False" for row in claim_rows), "all claim gates keep local claims false", "one or more claim gates opened"),
        check("VAL1744_11_no_claim_flags", no_claim_flags(rows_map), "all generated rows keep claim/no-score flags false", "one or more generated flags enabled a claim"),
        check("VAL1744_12_missing_not_ready", missing_rows_not_ready(rows_map), "no row containing MISSING_* is marked claim-ready or score-ready", "a missing row is marked ready"),
        check("VAL1744_13_next_selected", any(row["route_id"] == "NEXT1744_0_primary" and row["selection_status"] == "selected" for row in next_rows), "next target selects fixed-point double-zero or DeltaK component row", "next target missing selected primary route"),
        check("VAL1744_14_csv_parse", parsed_ok, "all generated 1744 CSVs parse", "one or more generated 1744 CSVs failed to parse"),
        check("VAL1744_15_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1744_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1744_17_formalization_untouched", formalization_untouched(), "no 1744 outputs found under formalization-workbench", "1744 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1744_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1744 support powers or Khat scalar profile validation" if overall else "one or more 1744 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- `pS=1` is conditionally available from the v0 source law, but only if `S_cg` is bounded and no hidden source survives.",
        "- The safe local suppression set still needs `pL=2`, `pT=2`, boundary power `pB`, and tensor/Kperp control `pK`; these are not parent-derived.",
        "- `Khat` scalar subtraction has a schema but no computable profile: `S_Delta=-Pi_gamma[P_loc div Delta_K]` remains input-missing.",
        "- Therefore `x_U` is not promoted and the Cassini/sigma_X runner remains blocked.",
        "- No local-GR, Newton, PPN, WEP, clock, orbital, R10, or `q_loc=0` claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Support Power Gate",
        markdown_table(rows_map["support_power_gate"], ["power_id", "power", "candidate_value", "derivation_status", "missing_to_promote"]),
        "",
        "## Support Power Candidate Rows",
        markdown_table(rows_map["support_power_candidate"], ["candidate_id", "candidate_set", "status", "why", "effect_if_signed"]),
        "",
        "## Khat Scalar Profile Rows",
        markdown_table(rows_map["khat_scalar_profile"], ["khat_row_id", "quantity", "formula", "status", "needed_to_promote"]),
        "",
        "## x_U Promotion Gates",
        markdown_table(rows_map["xU_promotion_gate"], ["gate_id", "requirement", "needed", "current_status", "effect"]),
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
        "This checkpoint narrows the missing proof sharply: local suppression now wants either a fixed-point/double-zero theorem for `m_L` and the trace baseline, or a concrete `Delta_K` component profile. Until one of those exists, `x_U` stays a nonclaim placeholder.",
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
    doc_path = ROOT / "1744-Y5-R2FR-support-powers-pS-pL-pT-or-Khat-scalar-profile.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1744_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1744 validation FAIL")
    print("1744 validation PASS")


if __name__ == "__main__":
    main()
