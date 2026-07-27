from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1753"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1753 - Source Support Parent Invariant Or A_src Coefficient Row"
UTC = datetime.now(timezone.utc).isoformat()

STRONG_WINDOW_UB = 3.7965595357794454e-7
WEAK_WINDOW_UB = 1.0e-4
POINT_MASS_UB = 9.725553695716371e-14
LOCAL_SOURCE_BUDGET = 1.0e-8


def no() -> str:
    return "False"


def yesno(value: bool) -> str:
    return "True" if value else "False"


def numeric_text(value: float) -> str:
    if value == 0:
        return "0"
    if abs(value) < 1.0e-3 or abs(value) >= 1.0e5:
        return f"{value:.12e}"
    return f"{value:.12g}"


SOURCES = [
    {
        "source_id": "SRC1753_0_1752_doc",
        "source_key": "1752_handoff",
        "source_path": ROOT / "1752-Y5-R2FR-source-support-or-boundary-no-flux-first-residual-zero-bound.md",
        "needles": ["TARGET_SOURCE_SUPPORT_PARENT_INVARIANT_OR_A_SRC_ROW", "R_source = U_B S_cg"],
    },
    {
        "source_id": "SRC1753_1_1752_source_audit",
        "source_key": "1752_source_support_audit",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1752_SOURCE_SUPPORT_ZERO_BOUND_AUDIT.csv",
        "needles": ["SSA1752_6_verdict", "MISSING_PARENT_SUPPORT_INVARIANT"],
    },
    {
        "source_id": "SRC1753_2_73_support_powers",
        "source_key": "73_support_powers_kperp",
        "source_path": FORMALIZATION / "73-support-powers-kperp-lemma.md",
        "needles": ["support_powers_kperp_conditional_not_derived", "M_src <= U_B^(1+pS) A_src"],
    },
    {
        "source_id": "SRC1753_3_74_support_results",
        "source_key": "74_support_powers_results",
        "source_path": FORMALIZATION / "74-support-powers-kperp-first-results.md",
        "needles": ["complete_support_powers_kperp_conditional_not_derived", "pS_required = 1.0000000000000004"],
    },
    {
        "source_id": "SRC1753_4_79_fixed_point",
        "source_key": "79_local_fixed_point",
        "source_path": FORMALIZATION / "79-local-fixed-point-mechanism.md",
        "needles": ["local_fixed_point_mechanism_conditional_closure_not_parent_derived", "S_cg = O(D_L)"],
    },
    {
        "source_id": "SRC1753_5_80_fixed_point_results",
        "source_key": "80_local_fixed_point_results",
        "source_path": FORMALIZATION / "80-local-fixed-point-mechanism-first-results.md",
        "needles": ["complete_local_fixed_point_mechanism_conditional_closure_not_parent_derived", "open_local_fixed_point_not_parent_derived"],
    },
    {
        "source_id": "SRC1753_6_122_parent_DL",
        "source_key": "122_parent_DL_fixed_point_silence",
        "source_path": FORMALIZATION / "122-parent-DL-fixed-point-silence.md",
        "needles": ["parent_DL_fixed_point_silence_partial_F1_only", "S_cg_linear_silence = not_derived_closure_only"],
    },
    {
        "source_id": "SRC1753_7_124_ZL_origin",
        "source_key": "124_fixed_point_extremality_origin",
        "source_path": FORMALIZATION / "124-fixed-point-extremality-origin.md",
        "needles": ["fixed_point_extremality_origin_best_route_ZL_not_parent_derived", "S_cg is odd/linear in Z_L"],
    },
    {
        "source_id": "SRC1753_8_800_powers",
        "source_key": "800_universal_XB_PiB",
        "source_path": ROOT / "800-Y5-R10-universal-XB-PiB-support-powers-or-Kperp-boundary-zero-lemma.md",
        "needles": ["pS_equals_1_conditional_only", "not_derived_as_parent_theorem"],
    },
    {
        "source_id": "SRC1753_9_836_fill_attempt",
        "source_key": "836_active_gamma_fill_attempt",
        "source_path": ROOT / "836-Y5-R10-fill-active-Gamma-bound-from-source-support-or-demote-local-branch.md",
        "needles": ["C_D/C_U", "response matrices"],
    },
    {
        "source_id": "SRC1753_10_942_selector",
        "source_key": "942_worldtube_selector",
        "source_path": RESIDUALS / "P8_Y5_R10_942_SELECTOR_THEOREM_ATTEMPT.csv",
        "needles": ["SEL942_3_support_selector", "SEL942_7_total_verdict"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1753_SOURCE_REGISTER.csv",
    "power_convention_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1753_SOURCE_POWER_CONVENTION_AUDIT.csv",
    "parent_invariant_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1753_PARENT_SUPPORT_INVARIANT_ATTEMPT.csv",
    "asrc_threshold_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1753_ASRC_THRESHOLD_LEDGER.csv",
    "first_residual_update": RESIDUALS / "P8_Y5_PARENT_QLOC_1753_FIRST_RESIDUAL_UPDATE.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1753_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1753_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1753_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1753_VALIDATION.csv",
}


COPY_MAP = {
    "power_convention_audit": "R2FR_1753_SOURCE_POWER_CONVENTION_AUDIT.csv",
    "parent_invariant_attempt": "R2FR_1753_PARENT_SUPPORT_INVARIANT_ATTEMPT.csv",
    "asrc_threshold_ledger": "R2FR_1753_ASRC_THRESHOLD_LEDGER.csv",
    "first_residual_update": "R2FR_1753_FIRST_RESIDUAL_UPDATE.csv",
    "decision": "R2FR_1753_DECISION_LEDGER.csv",
    "claim_gate": "R2FR_1753_CLAIM_GATE.csv",
    "next_target": "R2FR_1753_NEXT_TARGET.csv",
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
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("|", "\\|").replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = source["needles"]
        needles_present = all(needle in text for needle in needles)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": yesno(exists),
                "needles": "; ".join(needles),
                "needles_present": yesno(needles_present),
                "used_for": "1753 source-support parent invariant and A_src threshold audit",
                "timestamp_utc": UTC,
            }
        )
    return rows


def power_convention_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PCA1753_0_definitions",
            "clause": "source-power convention",
            "statement": "J_src = R_source = U_B S_cg, and if S_cg = U_B^p_int S_* then R_source = U_B^p_total S_* with p_total=1+p_int",
            "derived_status": "EXACT_BOOKKEEPING_IDENTITY",
            "claim_effect": "prevents double-counting the explicit U_B switch as both external factor and internal S_cg silence",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PCA1753_1_v0_factor",
            "clause": "what parent v0 actually gives",
            "statement": "The open-system law gives the explicit U_B factor multiplying S_cg, so bounded S_cg gives p_total=1 and p_int=0",
            "derived_status": "CONDITIONAL_FROM_EXISTING_SOURCE_LAW",
            "claim_effect": "this is useful but usually too weak unless A_src is tiny",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PCA1753_2_old_pS_translation",
            "clause": "older pS wording",
            "statement": "Older rows saying pS=1 from U_B S_cg are reinterpreted as total source-residual power p_total=1 unless a separate S_cg=O(U_B) theorem is supplied",
            "derived_status": "CONVENTION_REPAIR_NONCLAIM",
            "claim_effect": "prevents accidental promotion of p_total=2 from only one U_B factor",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PCA1753_3_linear_silence_route",
            "clause": "internal source silence",
            "statement": "If D_L <= C_D U_B and S_cg = D_L S_1 + O(D_L^2), then S_cg=O(U_B) and R_source=O(U_B^2)",
            "derived_status": "EXACT_CONDITIONAL_THEOREM_SHAPE",
            "claim_effect": "this is the clean route that makes the local residual naturally small",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PCA1753_4_zero_route",
            "clause": "exact zero route",
            "statement": "R_source=0 requires U_B=0, S_*=0, or a parent source-kernel theorem; finite logistic screening alone gives none of these exactly",
            "derived_status": "EXACT_ZERO_STILL_BLOCKED",
            "claim_effect": "keeps local-GR/nohair claims closed",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def parent_invariant_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "PIA1753_0_worldtube_selector",
            "candidate_parent_invariant": "W_source = closure supp rho_H from one observed Hilbert current",
            "mathematical_role": "fixes compact source support before exterior readout and prevents source-domain retuning",
            "result": "DOMAIN_GUARDRAIL_ONLY",
            "blocker": "does not by itself prove S_cg amplitude or U_B power silence",
            "parent_signed": no(),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "PIA1753_1_ZL_leakage_vector",
            "candidate_parent_invariant": "local leakage vector Z_L with squared invariant s_L=G_AB Z_L^A Z_L^B",
            "mathematical_role": "gives a non-cheating origin for odd/linear S_cg and even/quadratic m_L/trace baselines",
            "result": "BEST_ROUTE_NOT_PARENT_DERIVED",
            "blocker": "Z_L, G_AB, and the D_L relation are not parent-owned",
            "parent_signed": no(),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "PIA1753_2_DL_UB_lock",
            "candidate_parent_invariant": "D_L = U_B H_L(X_B), with 0 <= H_L <= C_D",
            "mathematical_role": "turns linear source silence S_cg=O(D_L) into S_cg=O(U_B)",
            "result": "CANDIDATE_LOCK_NOT_PROVED",
            "blocker": "H_L and universal C_D bound are not derived; D_L could become a renamed switch",
            "parent_signed": no(),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "PIA1753_3_source_amplitude_norm",
            "candidate_parent_invariant": "A_src = ||S_*|| in the same E* norm used by the local elliptic residual",
            "mathematical_role": "turns the conditional bound into a scorer row: |R_source| <= U_B^p_total A_src",
            "result": "FINITE_COEFFICIENT_ROW_REQUIRED",
            "blocker": "S_* norm, E* dual norm, arena projection, and source paths are missing",
            "parent_signed": no(),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "PIA1753_4_verdict",
            "candidate_parent_invariant": "source support parent invariant",
            "mathematical_role": "would promote R_source from conditional algebra to a finite source-backed residual row",
            "result": "NOT_PARENT_SIGNED_KEEP_FINITE_A_SRC_LEDGER",
            "blocker": "MISSING_Z_L_OR_D_L_PARENT_THEOREM; MISSING_A_SRC_NORM; MISSING_ARENA_PROJECTION",
            "parent_signed": no(),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def asrc_threshold_row(case_id: str, local_window: str, unscreened_fraction: float, internal_power: int, source_norm_status: str, notes: str) -> dict[str, Any]:
    total_power = 1 + internal_power
    suppression_factor = unscreened_fraction**total_power
    max_source_amplitude = LOCAL_SOURCE_BUDGET / suppression_factor
    return {
        "branch_id": BRANCH_ID,
        "case_id": case_id,
        "local_window": local_window,
        "U_B": numeric_text(unscreened_fraction),
        "p_int": str(internal_power),
        "p_total": str(total_power),
        "suppression_factor_U_B_p_total": numeric_text(suppression_factor),
        "local_source_budget": numeric_text(LOCAL_SOURCE_BUDGET),
        "A_src_max_for_budget": numeric_text(max_source_amplitude),
        "source_norm_status": source_norm_status,
        "valid_prediction_row": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
        "notes": notes,
        "timestamp_utc": UTC,
    }


def asrc_threshold_ledger_rows() -> list[dict[str, Any]]:
    return [
        asrc_threshold_row(
            "ASRC1753_0_strong_bounded_Scg",
            "strong_window43",
            STRONG_WINDOW_UB,
            0,
            "MISSING_A_SRC_NORM",
            "bounded S_cg with only the explicit U_B factor; useful only if A_src is very small",
        ),
        asrc_threshold_row(
            "ASRC1753_1_weak_bounded_Scg",
            "weak_window_1e_minus_4",
            WEAK_WINDOW_UB,
            0,
            "MISSING_A_SRC_NORM",
            "weak local margin makes bounded S_cg alone too strict unless A_src<=1e-4",
        ),
        asrc_threshold_row(
            "ASRC1753_2_strong_linear_silence",
            "strong_window43",
            STRONG_WINDOW_UB,
            1,
            "MISSING_PARENT_LINEAR_SILENCE_AND_A_SRC_NORM",
            "if S_cg=O(U_B), source residual is U_B^2 and the amplitude allowance becomes large",
        ),
        asrc_threshold_row(
            "ASRC1753_3_weak_linear_silence",
            "weak_window_1e_minus_4",
            WEAK_WINDOW_UB,
            1,
            "MISSING_PARENT_LINEAR_SILENCE_AND_A_SRC_NORM",
            "weak local margin with linear silence needs A_src<=1 in normalized units",
        ),
        asrc_threshold_row(
            "ASRC1753_4_weak_quadratic_silence",
            "weak_window_1e_minus_4",
            WEAK_WINDOW_UB,
            2,
            "MISSING_PARENT_QUADRATIC_SOURCE_SILENCE_AND_A_SRC_NORM",
            "quadratic internal source silence would make the weak margin roomy, but this is not derived",
        ),
        asrc_threshold_row(
            "ASRC1753_5_point_mass_U2_smoke",
            "point_mass_proxy",
            POINT_MASS_UB,
            1,
            "SMOKE_ONLY_MISSING_RESPONSE_AND_A_SRC_NORM",
            "point-mass proxy gives a tiny U_B^2 factor, but 836 already blocks it without coefficients and response matrices",
        ),
    ]


def first_residual_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "residual_id": "RV1753_0_source_power_convention",
            "parent_residual_id": "RV1752_0_source_leak_bound",
            "quantity": "R_source_power",
            "formula_or_description": "R_source = U_B S_cg = U_B^(1+p_int) S_*; use p_total=1+p_int",
            "current_status": "CONVENTION_REPAIRED_NONCLAIM",
            "missing_to_promote": "MISSING_A_SRC_NORM_AND_PARENT_INTERNAL_POWER",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "RV1753_1_parent_invariant",
            "parent_residual_id": "RV1752_0_source_leak_bound",
            "quantity": "source_support_parent_invariant",
            "formula_or_description": "D_L<=C_D U_B and S_cg=D_L S_1+O(D_L^2) would imply p_total>=2",
            "current_status": "BEST_ROUTE_NOT_PARENT_SIGNED",
            "missing_to_promote": "MISSING_Z_L; MISSING_D_L_LOCK; MISSING_C_D; MISSING_S1_NORM",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "RV1753_2_A_src_thresholds",
            "parent_residual_id": "RV1752_0_source_leak_bound",
            "quantity": "A_src_max",
            "formula_or_description": "A_src <= M_budget / U_B^p_total for each local window and power assumption",
            "current_status": "THRESHOLD_ROWS_STAGED_NONCLAIM",
            "missing_to_promote": "MISSING_REAL_A_SRC_VALUE; MISSING_ESTAR_NORM; MISSING_ARENA_PROJECTION",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "RV1753_3_verdict",
            "parent_residual_id": "RV1751_10_verdict",
            "quantity": "first source residual",
            "formula_or_description": "source residual is sharper but still active: exact bookkeeping plus threshold rows, no parent invariant or A_src value",
            "current_status": "SOURCE_RESIDUAL_ACTIVE_NONCLAIM",
            "missing_to_promote": "MISSING_PARENT_SUPPORT_INVARIANT_OR_SOURCE_NORM_ROW",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1753_0_convention",
            "decision": "REPAIR_SOURCE_POWER_CONVENTION",
            "reason": "explicit U_B in the residual and internal S_cg silence must be counted separately",
            "next_action": "use p_total=1+p_int in all future source-residual rows",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1753_1_parent_result",
            "decision": "PARENT_SUPPORT_INVARIANT_NOT_SIGNED",
            "reason": "worldtube selector fixes source domain, while Z_L/D_L is the best amplitude-power route, but neither signs S_cg=O(U_B)",
            "next_action": "do not promote source zero or source-bound claims",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1753_2_A_src_result",
            "decision": "A_SRC_THRESHOLDS_STAGED_NOT_MEASURED",
            "reason": "threshold rows show exactly how small or large A_src may be, but the actual norm is missing",
            "next_action": "acquire or derive A_src in the same E* norm before any local scoring",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1753_3_best_next",
            "decision": "TARGET_ZL_DL_PARENT_LEAKAGE_VECTOR_OR_ASRC_NORM",
            "reason": "the cleanest route is to derive Z_L/D_L and S_cg linear silence; fallback is a real A_src norm acquisition row",
            "next_action": "build 1754 Z_L/D_L parent leakage vector or A_src norm acquisition checkpoint",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1753_0_convention",
            "claim": "source residual power is unambiguous",
            "gate_pass": "True",
            "status": "BOOKKEEPING_GATE_ONLY",
            "blocker": "does not by itself provide a prediction row",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1753_1_parent_invariant",
            "claim": "S_cg=O(U_B) follows from parent support invariant",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_Z_L_D_L_PARENT_THEOREM",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1753_2_A_src_value",
            "claim": "A_src is sourced in the correct E* norm",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_A_SRC_NORM_SOURCE",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1753_3_source_residual_score",
            "claim": "R_source finite bound can score against local arenas",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_ARENA_PROJECTION_NORMS_AND_A_SRC",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1753_4_local_reentry",
            "claim": "local GR/Newton/PPN/R10/WEP branch can claim",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_SOURCE_RESIDUAL_ACTIVE_NONCLAIM",
            "claim_allowed": no(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1753_0_primary",
            "next_target": "1754-Y5-R2FR-ZL-DL-parent-leakage-vector-or-A-src-norm-acquisition.md",
            "script": "scripts/Y5_R2FR_ZL_DL_parent_leakage_vector_or_A_src_norm_acquisition.py",
            "objective": "try to parent-derive Z_L, D_L<=C_D U_B, and S_cg=D_L S_1+O(D_L^2), or acquire a real A_src norm row",
            "success_condition": "source residual obtains parent-signed p_total>=2 or a sourced finite A_src row without opening local claims",
            "selection_status": "selected",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1753_1_fallback",
            "next_target": "1754b-Y5-R2FR-local-response-projection-norms-for-source-residual.md",
            "script": "scripts/Y5_R2FR_local_response_projection_norms_for_source_residual.py",
            "objective": "source arena projection norms so a finite source residual can be mapped into PPN/R10/WEP/clock/orbital limits",
            "success_condition": "projection rows become source-backed nonclaim inputs while R_source remains blocked until A_src is real",
            "selection_status": "held_fallback",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "power_convention_audit": power_convention_audit_rows(),
        "parent_invariant_attempt": parent_invariant_attempt_rows(),
        "asrc_threshold_ledger": asrc_threshold_ledger_rows(),
        "first_residual_update": first_residual_update_rows(),
        "decision": decision_rows(),
        "claim_gate": claim_gate_rows(),
        "next_target": next_target_rows(),
    }


def generated_csv_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1753_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1753_{key.upper()}.csv")


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            for field in ("score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if row.get(field) == "True":
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            text = " ".join(str(value) for value in row.values())
            if "MISSING_" in text:
                for field in ("score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                    if row.get(field) == "True":
                        return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1753_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1753_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1753*"):
        path_text = str(path)
        if "\\.venv\\" in path_text or "\\__pycache__\\" in path_text:
            continue
        if path.is_file():
            return False
    return True


def convention_identity_present(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["power_convention_audit"]
    return any(
        row["audit_id"] == "PCA1753_0_definitions"
        and "p_total=1+p_int" in row["statement"]
        and row["derived_status"] == "EXACT_BOOKKEEPING_IDENTITY"
        for row in rows
    )


def old_convention_repaired(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["power_convention_audit"]
    return any(
        row["audit_id"] == "PCA1753_2_old_pS_translation"
        and "p_total=1" in row["statement"]
        and row["valid_for_claim"] == "False"
        for row in rows
    )


def parent_invariant_blocked(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["parent_invariant_attempt"]
    return any(
        row["attempt_id"] == "PIA1753_4_verdict"
        and row["result"] == "NOT_PARENT_SIGNED_KEEP_FINITE_A_SRC_LEDGER"
        and row["parent_signed"] == "False"
        for row in rows
    )


def asrc_rows_positive_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["asrc_threshold_ledger"]
    if not rows:
        return False
    for row in rows:
        numeric_fields = ["U_B", "p_total", "suppression_factor_U_B_p_total", "local_source_budget", "A_src_max_for_budget"]
        for field in numeric_fields:
            if float(row[field]) <= 0:
                return False
        if row["valid_for_claim"] != "False" or row["claim_allowed"] != "False":
            return False
    return True


def strong_linear_allows_large_amplitude(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for row in rows_map["asrc_threshold_ledger"]:
        if row["case_id"] == "ASRC1753_2_strong_linear_silence":
            return float(row["A_src_max_for_budget"]) > 1.0
    return False


def weak_bounded_is_strict(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for row in rows_map["asrc_threshold_ledger"]:
        if row["case_id"] == "ASRC1753_1_weak_bounded_Scg":
            return float(row["A_src_max_for_budget"]) <= 1.0e-4 * (1.0 + 1.0e-12)
    return False


def source_residual_active(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["residual_id"] == "RV1753_3_verdict"
        and row["current_status"] == "SOURCE_RESIDUAL_ACTIVE_NONCLAIM"
        for row in rows_map["first_residual_update"]
    )


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

    sources = rows_map["source_register"]
    claims = rows_map["claim_gate"]
    next_rows = rows_map["next_target"]

    validation = [
        check("VAL1753_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1753_1_needles_present", all(row["needles_present"] == "True" for row in sources), "required source needles are present", "one or more source needles missing"),
        check("VAL1753_2_convention_identity", convention_identity_present(rows_map), "p_total=1+p_int convention identity written", "source power convention identity missing"),
        check("VAL1753_3_old_convention_repaired", old_convention_repaired(rows_map), "older pS wording translated without promotion", "old pS convention repair missing"),
        check("VAL1753_4_parent_invariant_blocked", parent_invariant_blocked(rows_map), "parent support invariant remains blocked", "parent invariant accidentally promoted or missing"),
        check("VAL1753_5_asrc_rows_positive", asrc_rows_positive_nonclaim(rows_map), "A_src threshold rows are positive numeric nonclaim rows", "A_src threshold rows malformed or promoted"),
        check("VAL1753_6_strong_linear_roomy", strong_linear_allows_large_amplitude(rows_map), "strong linear-silence route allows A_src > 1 as smoke evidence", "strong linear-silence threshold not present or too strict"),
        check("VAL1753_7_weak_bounded_strict", weak_bounded_is_strict(rows_map), "weak bounded-S_cg route is correctly strict", "weak bounded-S_cg threshold is not strict"),
        check("VAL1753_8_source_residual_active", source_residual_active(rows_map), "source residual remains active and nonclaim", "source residual verdict missing"),
        check("VAL1753_9_claim_gates_safe", all(row["claim_allowed"] == "False" for row in claims) and all(row["gate_pass"] != "True" or row["status"] == "BOOKKEEPING_GATE_ONLY" for row in claims), "claim gates remain blocked except bookkeeping-only convention gate", "one or more claim gates opened"),
        check("VAL1753_10_no_claim_flags", no_claim_flags(rows_map), "claim/no-score flags stay false", "one or more claim/no-score flags enabled"),
        check("VAL1753_11_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready", "a MISSING_* row is marked ready"),
        check("VAL1753_12_decision_next", any(row["decision_id"] == "DEC1753_3_best_next" and row["decision"] == "TARGET_ZL_DL_PARENT_LEAKAGE_VECTOR_OR_ASRC_NORM" for row in rows_map["decision"]), "decision selects Z_L/D_L or A_src norm target", "best-next decision missing"),
        check("VAL1753_13_next_selected", any(row["route_id"] == "NEXT1753_0_primary" and row["selection_status"] == "selected" for row in next_rows), "next target selected", "next target missing"),
        check("VAL1753_14_csv_parse", parsed_ok, "all generated 1753 CSVs parse", "one or more generated 1753 CSVs failed to parse"),
        check("VAL1753_15_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1753_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1753_17_formalization_untouched", formalization_untouched(), "no 1753 outputs found under formalization-workbench", "1753 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1753_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1753 source-support parent invariant or A_src coefficient row checkpoint" if overall else "one or more 1753 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1753 fixes a real bookkeeping risk: the explicit `U_B` in `R_source = U_B S_cg` must not be counted again as internal `S_cg` silence.",
        "- The safe convention is `p_total = 1 + p_int`, where `p_int` is the extra source silence in `S_cg = U_B^p_int S_*`.",
        "- Parent v0 currently gives `p_total=1` if `S_cg` is merely bounded; it does not by itself give `S_cg=O(U_B)`.",
        "- The clean derivation route is still alive: derive `D_L <= C_D U_B` and `S_cg = D_L S_1 + O(D_L^2)` from a parent `Z_L/D_L` leakage invariant.",
        "- Since that route is not parent-signed, 1753 stages explicit `A_src` threshold rows and keeps every local-GR/Newton/PPN/R10/WEP claim blocked.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Source Power Convention Audit",
        markdown_table(rows_map["power_convention_audit"], ["audit_id", "clause", "statement", "derived_status", "claim_effect"]),
        "",
        "## Parent Support Invariant Attempt",
        markdown_table(rows_map["parent_invariant_attempt"], ["attempt_id", "candidate_parent_invariant", "mathematical_role", "result", "blocker"]),
        "",
        "## A_src Threshold Ledger",
        markdown_table(rows_map["asrc_threshold_ledger"], ["case_id", "local_window", "U_B", "p_int", "p_total", "suppression_factor_U_B_p_total", "A_src_max_for_budget", "source_norm_status"]),
        "",
        "## First Residual Update",
        markdown_table(rows_map["first_residual_update"], ["residual_id", "quantity", "formula_or_description", "current_status", "missing_to_promote"]),
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
        "This is a useful tightening move. Bounded `S_cg` plus the explicit switch is not enough unless the source amplitude is tiny. Linear internal silence, `S_cg=O(U_B)`, is the route that makes the residual naturally small without pretending exact zero. So the next hunt should go after the parent leakage vector `Z_L`/distance `D_L`, with a fallback that sources the real `A_src` norm.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    if not math.isclose(POINT_MASS_UB**2, 9.458639468826237e-27, rel_tol=1.0e-12):
        raise SystemExit("point-mass U_B proxy mismatch")
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    cleanup_pycache()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1753-Y5-R2FR-source-support-parent-invariant-or-A-src-coefficient-row.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1753_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1753 validation FAIL")
    print("1753 validation PASS")


if __name__ == "__main__":
    main()
