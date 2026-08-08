from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_CURRENT_DESCENT_REBASE_2602"
CHECKPOINT_ID = "2602"

DOC = ROOT / "2602-Y5-R2FR-current-descent-lemma-Dq-tau-projectability-or-theta-leak-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_CURRENT_DESCENT_REBASE_2602_SOURCE_REGISTER.csv",
    "lineage_ledger": OUT / "P8_Y5_CURRENT_DESCENT_REBASE_2602_LINEAGE_LEDGER.csv",
    "descent_gate": OUT / "P8_Y5_CURRENT_DESCENT_REBASE_2602_DESCENT_GATE_STATUS.csv",
    "bg_bridge": OUT / "P8_Y5_CURRENT_DESCENT_REBASE_2602_BG_RESPONSE_BRIDGE.csv",
    "runner_refusal": OUT / "P8_Y5_CURRENT_DESCENT_REBASE_2602_RUNNER_REFUSAL.csv",
    "claim_gates": OUT / "P8_Y5_CURRENT_DESCENT_REBASE_2602_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_CURRENT_DESCENT_REBASE_2602_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_CURRENT_DESCENT_REBASE_2602_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_CURRENT_DESCENT_REBASE_2602_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2602_VALIDATION.csv",
}

COPY_TARGETS = {
    "descent_gate": LOCAL_BOUNDS / "Current_descent_Dq_tau_gate_2602_NONCLAIM.csv",
    "bg_bridge": LOCAL_BOUNDS / "Current_descent_to_bg_gamma_bridge_2602_NONCLAIM.csv",
    "next_target": QUEUE / "JR2602_SIGMAX_PROFILE_OR_REAL_R10_CURVE_NEXT.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def with_stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def row_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    if value is None:
        return ""
    return str(value)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row_value(row.get(field, "")) for field in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), len(rows), ""
    except Exception as exc:
        return False, 0, str(exc)


def path_has_needles(path: Path, needles: list[str]) -> list[str]:
    if not path.exists():
        return needles
    text = path.read_text(encoding="utf-8", errors="replace")
    return [needle for needle in needles if needle not in text]


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        {
            "source_id": "SRC2602_00_2601_handoff",
            "source_path": ROOT / "2601-Y5-R2FR-Tobs-support-annulus-split-or-first-norm-source-row.md",
            "needles": ["BR2601_3_Q_tau_total", "NEXT2601_0_selected", "VAL2601_OVERALL"],
            "role": "current branch handoff selecting current descent through q/Dq and projectable tau",
        },
        {
            "source_id": "SRC2602_01_1734_doc",
            "source_path": ROOT / "1734-Y5-R2FR-current-descent-lemma-Dq-tau-projectability-or-theta-leak-row.md",
            "needles": ["DTP1734_6_verdict", "TLR1734_0_Dq_tau_commutator", "NEXT1734_0_primary", "VAL1734_OVERALL"],
            "role": "Dq/tau projectability audit and theta/Q_tau leak rows",
        },
        {
            "source_id": "SRC2602_02_1734_leak_rows",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1734_THETA_QTAU_LEAK_ROWS.csv",
            "needles": ["TLR1734_0_Dq_tau_commutator", "TLR1734_4_total_theta_qtau_leak"],
            "role": "projectability leak rows feeding local arenas",
        },
        {
            "source_id": "SRC2602_03_1735_doc",
            "source_path": ROOT / "1735-Y5-R2FR-Dq-tau-theta-leak-source-pack-units-and-arena-projections.md",
            "needles": ["E_Dq_tau_commutator_norm", "R10_fifth_force", "NEXT1735_0_primary", "VAL1735_OVERALL"],
            "role": "unit conventions and arena projections for theta/Q_tau leak pack",
        },
        {
            "source_id": "SRC2602_04_1736_doc",
            "source_path": ROOT / "1736-Y5-R2FR-Dq-tau-commutator-zero-or-first-finite-bound-row.md",
            "needles": ["DTC1736_7_verdict", "EDT1736_0_total_commutator_norm", "NEXT1736_0_primary", "VAL1736_OVERALL"],
            "role": "exact Dq/tau commutator theorem and finite fallback row",
        },
        {
            "source_id": "SRC2602_05_1736_finite_schema",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1736_FIRST_FINITE_BOUND_ROW_SCHEMA.csv",
            "needles": ["EDT1736_0_total_commutator_norm", "MISSING_Q_MAP", "MISSING_VERTICAL_BASIS"],
            "role": "finite E_Dq_tau commutator source-row schema",
        },
        {
            "source_id": "SRC2602_06_1737_doc",
            "source_path": ROOT / "1737-Y5-R2FR-q-map-Dq-vertical-basis-source-row-or-coframe-functor-zero.md",
            "needles": ["QMAP1737_5_Z_phi_RAB", "DQM1737_5_Dq_total_kernel", "NEXT1737_0_primary", "VAL1737_OVERALL"],
            "role": "q-map, Dq matrix and candidate vertical basis source rows",
        },
        {
            "source_id": "SRC2602_07_1738_doc",
            "source_path": ROOT / "1738-Y5-R2FR-observed-coframe-kernel-zero-or-first-finite-DObs-e-row.md",
            "needles": ["DOK1738_1_same_coframe_not_enough", "DBG1738_0_common_frame_log_derivative", "NEXT1738_0_primary", "VAL1738_OVERALL"],
            "role": "observed coframe kernel theorem and same-coframe countermodel",
        },
        {
            "source_id": "SRC2602_08_1738_dobs_rows",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1738_FINITE_DOBS_E_SOURCE_ROWS.csv",
            "needles": ["DBG1738_0_common_frame_log_derivative", "DOE1738_0_vZ"],
            "role": "finite observed coframe derivative rows",
        },
        {
            "source_id": "SRC2602_09_1739_doc",
            "source_path": ROOT / "1739-Y5-R2FR-parent-coframe-ownership-or-common-frame-log-derivative-row.md",
            "needles": ["PCO1739_9_verdict", "BG1739_0_generic", "NEXT1739_0_primary", "VAL1739_OVERALL"],
            "role": "parent coframe ownership attempt and b_g rows",
        },
        {
            "source_id": "SRC2602_10_1739_bg_rows",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1739_COMMON_FRAME_LOG_DERIVATIVE_ROWS.csv",
            "needles": ["BG1739_0_generic", "BG1739_5_total_abs"],
            "role": "b_g/common-frame finite residual rows",
        },
        {
            "source_id": "SRC2602_11_1740_doc",
            "source_path": ROOT / "1740-Y5-R2FR-no-shadow-frame-zero-or-bg-bound-projection-map.md",
            "needles": ["NSF1740_6_verdict", "BMAP1740_1_gamma_beta", "NEXT1740_0_primary", "VAL1740_OVERALL"],
            "role": "no-shadow-frame zero attempt and b_g bound projection map",
        },
        {
            "source_id": "SRC2602_12_1740_projection_map",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1740_BG_BOUND_PROJECTION_MAP.csv",
            "needles": ["BMAP1740_0_WEP", "BMAP1740_1_gamma_beta", "BMAP1740_4_R10"],
            "role": "b_g/shadow projection map into local bounds",
        },
        {
            "source_id": "SRC2602_13_1741_doc",
            "source_path": ROOT / "1741-Y5-R2FR-first-bg-response-map-or-real-R10-bound-curve.md",
            "needles": ["BRM1741_0_conformal_PPN_gamma", "R10CURVE1741_0", "NEXT1741_0_primary", "VAL1741_OVERALL"],
            "role": "first b_g response map and R10 placeholder status",
        },
        {
            "source_id": "SRC2602_14_1741_response_map",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1741_BG_RESPONSE_MAP.csv",
            "needles": ["BRM1741_0_conformal_PPN_gamma", "gamma_eff=(1+s_X)/(1-s_X)"],
            "role": "source-backed nonclaim b_g to Cassini gamma response map",
        },
        {
            "source_id": "SRC2602_15_1741_r10_status",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1741_R10_CURVE_STATUS.csv",
            "needles": ["R10CURVE1741_0", "PLACEHOLDER_NONCLAIM"],
            "role": "R10 curve placeholder blocker",
        },
        {
            "source_id": "SRC2602_16_1741_next",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1741_NEXT_TARGET.csv",
            "needles": ["NEXT1741_0_primary", "sigmaX-profile-coefficient-or-real-R10-curve"],
            "role": "selected sigma_X profile or real R10 curve next target",
        },
    ]
    rows: list[dict[str, Any]] = []
    for spec in specs:
        missing_needles = path_has_needles(spec["source_path"], spec["needles"])
        rows.append(
            with_stamp(
                {
                    "source_id": spec["source_id"],
                    "source_path": spec["source_path"],
                    "exists": spec["source_path"].exists(),
                    "missing_needles": missing_needles,
                    "source_pass": spec["source_path"].exists() and not missing_needles,
                    "role": spec["role"],
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def lineage_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "step_id": "LIN2602_0_2601",
            "checkpoint": "2601",
            "question": "What does the annulus/boundary route require next?",
            "result": "Theta_total/Q_tau current descent through q/Dq plus projectable tau",
            "status": "HANDOFF_REBASED",
            "next_dependency": "Dq/tau current descent",
        },
        {
            "step_id": "LIN2602_1_1734",
            "checkpoint": "1734",
            "question": "Does Dq/tau projectability sign current descent?",
            "result": "not signed; E_Dq_tau commutator leak defined",
            "status": "PROJECTABILITY_NOT_SIGNED",
            "next_dependency": "leak units and arena projections",
        },
        {
            "step_id": "LIN2602_2_1735",
            "checkpoint": "1735",
            "question": "Can the theta/Q_tau leak be made testable?",
            "result": "unit conventions and R0-R11 arena projections staged; values missing",
            "status": "SOURCE_PACK_NONCLAIM",
            "next_dependency": "commutator zero or finite row",
        },
        {
            "step_id": "LIN2602_3_1736",
            "checkpoint": "1736",
            "question": "Does the Dq/tau commutator vanish?",
            "result": "exact conditional theorem exists; q/Dq/vertical/tau/norm inputs missing",
            "status": "COMMUTATOR_ZERO_NOT_SIGNED",
            "next_dependency": "q-map/Dq/vertical basis",
        },
        {
            "step_id": "LIN2602_4_1737",
            "checkpoint": "1737",
            "question": "Can q, Dq and vertical basis be made explicit?",
            "result": "Q_vis and candidate vertical basis staged; DObs_e/source/marker/boundary/tau components remain finite",
            "status": "DQ_KERNEL_NOT_CLOSED",
            "next_dependency": "observed coframe kernel",
        },
        {
            "step_id": "LIN2602_5_1738",
            "checkpoint": "1738",
            "question": "Does the observed coframe kill vertical directions?",
            "result": "chain-rule theorem exact; same-coframe countermodel survives through b_g",
            "status": "DOBS_E_KERNEL_NOT_SIGNED",
            "next_dependency": "parent coframe ownership or b_g row",
        },
        {
            "step_id": "LIN2602_6_1739",
            "checkpoint": "1739",
            "question": "Does parent coframe ownership kill b_g?",
            "result": "ownership not signed; b_g rows retained as finite local metric residuals",
            "status": "PARENT_COFRAME_OWNERSHIP_NOT_SIGNED",
            "next_dependency": "no-shadow-frame zero or b_g projection",
        },
        {
            "step_id": "LIN2602_7_1740",
            "checkpoint": "1740",
            "question": "Are shadow frame routes forbidden?",
            "result": "no-shadow-frame contract exact but not signed; b_g projection map staged",
            "status": "NO_SHADOW_FRAME_NOT_SIGNED",
            "next_dependency": "first response map or R10 curve",
        },
        {
            "step_id": "LIN2602_8_1741",
            "checkpoint": "1741",
            "question": "Can b_g touch a real local bound?",
            "result": "first source-backed nonclaim b_g -> Cassini gamma response map exists; R10 curve remains placeholder",
            "status": "FIRST_RESPONSE_MAP_NONCLAIM",
            "next_dependency": "s_X profile coefficient or real R10 curve",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def descent_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "DGR2602_0_projectable_current",
            "object": "current descent lemma",
            "theorem_shape": "if q is explicit, tau is q-projectable, vertical symplectic pieces are zero/exact, and boundary/reference data are fixed, then Theta_total/Q_tau descends",
            "current_status": "CONTRACT_ONLY_NOT_SIGNED",
            "blocking_gap": "q/Dq, tau projectability, vertical silence, boundary/reference, matter/source descent",
            "next_owner": "E_Dq_tau and b_g rows",
        },
        {
            "gate_id": "DGR2602_1_commutator",
            "object": "E_Dq_tau_commutator_norm",
            "theorem_shape": "Dq([L_tau,v])-[L_tau_red,Dq(v)]=0 when v in ker(Dq) and tau is q-related to tau_red",
            "current_status": "EXACT_CONDITIONAL_THEOREM_ZERO_NOT_SIGNED",
            "blocking_gap": "q_map, Dq, vertical basis, tau pushforward, quotient norm, readout guard",
            "next_owner": "finite nonclaim commutator row or q/Dq theorem",
        },
        {
            "gate_id": "DGR2602_2_coframe_kernel",
            "object": "DObs_e[v]",
            "theorem_shape": "if e_obs=E(q(Phi)) and Dq[v]=0 then DObs_e[v]=0",
            "current_status": "CHAIN_RULE_THEOREM_EXACT_CURRENT_ZERO_UNSIGNED",
            "blocking_gap": "parent coframe ownership and kernel membership",
            "next_owner": "b_g common-frame derivative",
        },
        {
            "gate_id": "DGR2602_3_no_shadow_frame",
            "object": "b_g/shadow frame derivatives",
            "theorem_shape": "no Weyl/disformal/source-prefactor/readout/endpoint shadow derivatives imply b_g=0",
            "current_status": "NO_SHADOW_FRAME_CONTRACT_NOT_SIGNED",
            "blocking_gap": "Weyl, disformal, source-prefactor, post-readout and endpoint countermodels survive",
            "next_owner": "b_g response map and bounds",
        },
        {
            "gate_id": "DGR2602_4_empirical_bridge",
            "object": "b_g -> Cassini gamma response",
            "theorem_shape": "g_obs=e^(2 sigma_X)g_GR, sigma_X=s_X U/c^2 gives gamma_eff=(1+s_X)/(1-s_X)",
            "current_status": "SOURCE_BACKED_RESPONSE_MAP_NONCLAIM",
            "blocking_gap": "b_g value, X_U profile coefficient, source normalization and no-other-channel theorem missing",
            "next_owner": "s_X=b_g,X x_U profile coefficient",
        },
    ]
    return [with_stamp({**row, "score_ready": False, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def bg_bridge_rows() -> list[dict[str, Any]]:
    source_paths = [
        OUT / "P8_Y5_PARENT_QLOC_1734_THETA_QTAU_LEAK_ROWS.csv",
        OUT / "P8_Y5_PARENT_QLOC_1736_FIRST_FINITE_BOUND_ROW_SCHEMA.csv",
        OUT / "P8_Y5_PARENT_QLOC_1738_FINITE_DOBS_E_SOURCE_ROWS.csv",
        OUT / "P8_Y5_PARENT_QLOC_1739_COMMON_FRAME_LOG_DERIVATIVE_ROWS.csv",
        OUT / "P8_Y5_PARENT_QLOC_1740_BG_BOUND_PROJECTION_MAP.csv",
        OUT / "P8_Y5_PARENT_QLOC_1741_BG_RESPONSE_MAP.csv",
        OUT / "P8_Y5_PARENT_QLOC_1741_R10_CURVE_STATUS.csv",
    ]
    rows = [
        {
            "row_id": "BGB2602_0_E_Dq_tau",
            "symbol": "E_Dq_tau_commutator_norm",
            "formula": "||Dq([L_tau,v])-[L_tau_red,Dq(v)]||",
            "status": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "missing_inputs": "MISSING_Q_MAP;MISSING_DQ;MISSING_VERTICAL_BASIS;MISSING_TAU_ACTION;MISSING_NORM",
            "empirical_role": "upstream projectability leak feeding WEP/PPN/R10 arenas",
        },
        {
            "row_id": "BGB2602_1_b_g",
            "symbol": "b_g,X",
            "formula": "||e_obs^-1 DObs_e[partial_X]||",
            "status": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "missing_inputs": "MISSING_PARENT_COFRAME_OWNERSHIP;MISSING_DQ_KERNEL;MISSING_NO_SHADOW_FRAME_RULE;MISSING_SOURCE_PATH",
            "empirical_role": "finite local metric residual if coframe kernel zero fails",
        },
        {
            "row_id": "BGB2602_2_shadow_abs",
            "symbol": "epsilon_shadow_abs",
            "formula": "|epsilon_bg_abs|+|b_disformal|+|delta w|+|b_readout|+|b_endpoint|",
            "status": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "missing_inputs": "MISSING_BG_OR_SHADOW_COEFFICIENTS;MISSING_ARENA_RESPONSE_MAPS",
            "empirical_role": "no-shadow-frame fallback envelope",
        },
        {
            "row_id": "BGB2602_3_gamma_response",
            "symbol": "s_X=b_g,X x_U",
            "formula": "gamma_eff=(1+s_X)/(1-s_X); gamma_minus_1≈2s_X",
            "status": "RESPONSE_MAP_SOURCE_BACKED_PROFILE_MISSING",
            "missing_inputs": "MISSING_BG_VALUE;MISSING_X_U_PROFILE;MISSING_SOURCE_NORMALIZATION;MISSING_NO_OTHER_CHANNELS",
            "empirical_role": "Cassini gamma bridge with conditional |s_X| <= 1.15e-05",
        },
        {
            "row_id": "BGB2602_4_R10_curve",
            "symbol": "R10_alpha_lambda_bound_curve",
            "formula": "alpha_pred(lambda) <= alpha_bound(lambda)",
            "status": "PLACEHOLDER_NONCLAIM",
            "missing_inputs": "MISSING_DIGITIZED_ALPHA_BOUND;MISSING_NUMERIC_LAMBDA;MISSING_ALPHA_PREDICTION",
            "empirical_role": "short-range bound route held until real curve exists",
        },
    ]
    return [
        with_stamp(
            {
                **row,
                "source_paths": source_paths,
                "source_paths_exist": all(path.exists() for path in source_paths),
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        for row in rows
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "runner_id": "RUN2602_0_current_descent",
            "target": "Theta_total/Q_tau descends through q",
            "verdict": "BLOCKED_NO_CLAIM",
            "failure_reasons": "MISSING_Q_DQ;MISSING_TAU_PROJECTABILITY;MISSING_VERTICAL_SYMPLECTIC_SILENCE;MISSING_BOUNDARY_REFERENCE;MISSING_MATTER_DESCENT",
        },
        {
            "runner_id": "RUN2602_1_commutator_zero",
            "target": "E_Dq_tau_commutator_norm=0",
            "verdict": "BLOCKED_NO_CLAIM",
            "failure_reasons": "MISSING_Q_MAP;MISSING_DQ;MISSING_VERTICAL_BASIS;MISSING_TAU_PUSHFORWARD;MISSING_NORM",
        },
        {
            "runner_id": "RUN2602_2_bg_gamma_score",
            "target": "b_g Cassini gamma comparison",
            "verdict": "REFUSE_CLAIM_RUN",
            "failure_reasons": "MISSING_BG_VALUE;MISSING_X_U_PROFILE;MISSING_SOURCE_NORMALIZATION;MISSING_NO_OTHER_CHANNELS",
        },
        {
            "runner_id": "RUN2602_3_R10_score",
            "target": "R10 alpha(lambda) comparison",
            "verdict": "REFUSE_CLAIM_RUN",
            "failure_reasons": "MISSING_REAL_R10_CURVE;MISSING_ALPHA_PREDICTION;MISSING_RANGE_AND_RESPONSE_MAP",
        },
        {
            "runner_id": "RUN2602_4_local_GR_Newton",
            "target": "local GR/Newton recovery",
            "verdict": "BLOCKED_NO_CLAIM",
            "failure_reasons": "NO_CURRENT_DESCENT;NO_BG_ZERO_OR_BOUND;NO_HTAU_MHREF;NO_PPN_VECTOR_PASS",
        },
    ]
    return [with_stamp({**row, "accepted_for_scoring": False, "claim_allowed": False, "valid_for_claim": False}) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "CG2602_0_current_descent",
            "claim": "parent observed-time current descends through q",
            "gate_status": "BLOCKED_NO_CLAIM",
            "reason": "1734 keeps q/Dq/tau projectability unsigned",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2602_1_bg_response_map",
            "claim": "first b_g response map exists",
            "gate_status": "PASS_NONCLAIM_ONLY",
            "reason": "1741 stages a source-backed conditional conformal map to Cassini gamma",
            "gate_pass": True,
        },
        {
            "gate_id": "CG2602_2_gamma_score",
            "claim": "MTS passes Cassini gamma through b_g map",
            "gate_status": "BLOCKED_NO_CLAIM",
            "reason": "s_X profile coefficient and no-other-channel proof are missing",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2602_3_R10_curve",
            "claim": "R10 curve is real and score-ready",
            "gate_status": "BLOCKED_NO_CLAIM",
            "reason": "1741 records R10 curve as placeholder/nonclaim",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2602_4_local_GR",
            "claim": "local GR/Newton branch is derived",
            "gate_status": "BLOCKED_NO_CLAIM",
            "reason": "current descent, b_g zero/bound, H_tau/M_H_ref and full PPN vector remain open",
            "gate_pass": False,
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2602_0_no_duplicate_projectability",
            "decision": "do not rerun 1734 as if new",
            "reason": "1734-1736 already identify the exact Dq/tau commutator theorem and finite fallback",
            "effect": "2602 rebases those results into the current branch",
        },
        {
            "decision_id": "DEC2602_1_metric_residual_named",
            "decision": "use b_g as the live local metric residual",
            "reason": "1738-1740 show same-coframe is insufficient unless common-frame derivatives vanish",
            "effect": "future local tests target b_g/shadow coefficients rather than vague frame language",
        },
        {
            "decision_id": "DEC2602_2_first_empirical_bridge",
            "decision": "keep the Cassini gamma bridge as first response map",
            "reason": "1741 gives gamma_eff=(1+s_X)/(1-s_X) and a conditional |s_X| bound, while R10 curve is placeholder",
            "effect": "next target is sigma_X profile coefficient or real R10 curve",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False}) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2602_0_selected",
            "selection_status": "selected",
            "target_file": "2603-Y5-R2FR-sigmaX-profile-coefficient-or-real-R10-curve.md",
            "target_script": "scripts/Y5_R2FR_sigmaX_profile_coefficient_or_real_R10_curve_2603.py",
            "task": "derive or source s_X=b_g,X x_U for the PPN gamma bridge, or replace the placeholder R10 alpha(lambda) curve with real source-backed rows",
            "success_condition": "finite nonclaim s_X row with units/source path or real digitized R10 curve rows with valid schema",
            "fallback_condition": "keep b_g gamma bridge nonclaim and select first source-backed b_g/profile input row",
            "guardrails": "no numeric PPN claim without b_g and x_U; no R10 claim from placeholder curve; no no-other-channel shortcut; no local-GR claim; no GitHub; no formalization-workbench edits",
        }
    ]
    return [with_stamp({**row, "valid_for_claim": False}) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, target_path in COPY_TARGETS.items():
        source_path = OUTPUTS[copy_id]
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            with_stamp(
                {
                    "copy_id": f"COPY2602_{copy_id}",
                    "source_path": source_path,
                    "target_path": target_path,
                    "source_exists": source_path.exists(),
                    "target_exists": target_path.exists(),
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def generated_rows_have_no_claim_flags(data: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in data.values():
        for row in rows:
            if row.get("valid_for_claim") is True or row.get("claim_allowed") is True:
                return False
            if row.get("score_ready") is True or row.get("accepted_for_scoring") is True:
                return False
    return True


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, condition: bool, notes: str, detail: str = "") -> None:
        rows.append(
            with_stamp(
                {
                    "check_id": check_id,
                    "status": "PASS" if condition else "FAIL",
                    "notes": notes,
                    "detail": detail,
                    "valid_for_claim": False,
                }
            )
        )

    add("VAL2602_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    expected_lineage = {f"LIN2602_{idx}_{suffix}" for idx, suffix in enumerate(["2601", "1734", "1735", "1736", "1737", "1738", "1739", "1740", "1741"])}
    add("VAL2602_01_lineage_complete", expected_lineage == {row["step_id"] for row in data["lineage"]}, "lineage ledger covers 2601 and 1734-1741")
    expected_gate_objects = {"current descent lemma", "E_Dq_tau_commutator_norm", "DObs_e[v]", "b_g/shadow frame derivatives", "b_g -> Cassini gamma response"}
    add("VAL2602_02_descent_gate_complete", expected_gate_objects.issubset({row["object"] for row in data["descent_gate"]}), "descent gate covers projectability, commutator, coframe, shadow and empirical bridge")
    expected_symbols = {"E_Dq_tau_commutator_norm", "b_g,X", "epsilon_shadow_abs", "s_X=b_g,X x_U", "R10_alpha_lambda_bound_curve"}
    add("VAL2602_03_bg_bridge_complete", expected_symbols.issubset({row["symbol"] for row in data["bg_bridge"]}), "b_g bridge rows cover commutator, coframe residual, shadow envelope, gamma bridge and R10 curve")
    add("VAL2602_04_bridge_sources_exist", all(row["source_paths_exist"] is True for row in data["bg_bridge"]), "bridge rows cite existing local sources")
    add("VAL2602_05_runner_refuses", all(row["accepted_for_scoring"] is False and row["claim_allowed"] is False for row in data["runner_refusal"]), "runners refuse current descent, gamma score, R10 score and local-GR claims")
    add("VAL2602_06_claim_gates_safe", all(row["claim_allowed"] is False for row in data["claim_gates"]) and any(row["gate_id"] == "CG2602_1_bg_response_map" and row["gate_status"] == "PASS_NONCLAIM_ONLY" for row in data["claim_gates"]), "claim gates allow only the nonclaim response-map result")
    add("VAL2602_07_no_claim_flags", generated_rows_have_no_claim_flags(data), "no generated row promotes scoring or claim flags")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in (
            "*2602-Y5-R2FR-current-descent*",
            "*Y5_R2FR_current_descent*2602*",
            "*P8_Y5_CURRENT_DESCENT_REBASE_2602*",
            "*JR2602*",
        ):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add("VAL2602_08_no_formalization_artifacts", not formalization_artifacts, "no 2602 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))
    add("VAL2602_09_next_selected", any(row["route_id"] == "NEXT2602_0_selected" and "2603-Y5-R2FR-sigmaX-profile-coefficient" in row["target_file"] for row in data["next"]), "2603 sigmaX profile or real R10 curve target selected")
    add("VAL2602_10_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2602_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2602_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2602_OVERALL",
        overall,
        "2602 rebases the current-descent chain through b_g response mapping, keeps all local claims blocked, and selects sigmaX profile coefficient or real R10 curve next",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = [row_value(row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2602 Y5 R2FR current descent lemma Dq tau projectability or theta leak row",
        "",
        "**Status:** private nonclaim rebase checkpoint. The current-descent target selected by 2601 is preserved, but the prior 1734-1741 chain already drove it down to the live local metric residual `b_g` and a first nonclaim Cassini-gamma response map.",
        "",
        "**Main result:** the clean derivation path remains alive but unsigned. Current descent requires `q/Dq`, projectable `tau`, vertical symplectic silence, and boundary/reference/matter descent. When those fail, the leak becomes `E_Dq_tau`, then `DObs_e`, then the common-frame derivative `b_g`. The first empirical bridge is now source-backed in form: for `g_obs=e^(2 sigma_X) g_GR` with `sigma_X=s_X U/c^2`, `gamma_eff=(1+s_X)/(1-s_X)` and small `s_X` gives `|s_X| <= 1.15e-05` from Cassini gamma. No numeric MTS PPN/R10/local-GR claim is made because `b_g`, `x_U`, source normalization, no-other-channel proof, and the real R10 curve remain missing.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role", "valid_for_claim"]),
        "",
        "## Lineage Ledger",
        markdown_table(data["lineage"], ["step_id", "checkpoint", "question", "result", "status", "next_dependency", "valid_for_claim", "claim_allowed"]),
        "",
        "## Descent Gate Status",
        markdown_table(data["descent_gate"], ["gate_id", "object", "theorem_shape", "current_status", "blocking_gap", "next_owner", "score_ready", "valid_for_claim", "claim_allowed"]),
        "",
        "## b_g Response Bridge",
        markdown_table(data["bg_bridge"], ["row_id", "symbol", "formula", "status", "missing_inputs", "empirical_role", "source_paths", "source_paths_exist", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Runner Refusal",
        markdown_table(data["runner_refusal"], ["runner_id", "target", "verdict", "failure_reasons", "accepted_for_scoring", "claim_allowed", "valid_for_claim"]),
        "",
        "## Claim Gates",
        markdown_table(data["claim_gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "valid_for_claim", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect", "valid_for_claim"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "success_condition", "fallback_condition", "guardrails", "valid_for_claim"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists", "valid_for_claim"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail", "valid_for_claim"]),
        "",
        "## Practical Status",
        "",
        "This is not a retreat; it is the local branch finally naming the thing that has to survive a judge's scorecard. Either the parent action kills shadow-frame/common-frame derivatives, or `b_g` must be small enough under real PPN/WEP/clock/R10 maps. The next useful move is to derive/source the `s_X=b_g,X x_U` profile coefficient, or replace the placeholder R10 curve with a real bound curve.",
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)

    data = {
        "sources": source_register_rows(),
        "lineage": lineage_rows(),
        "descent_gate": descent_gate_rows(),
        "bg_bridge": bg_bridge_rows(),
        "runner_refusal": runner_refusal_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["lineage_ledger"], data["lineage"])
    write_csv(OUTPUTS["descent_gate"], data["descent_gate"])
    write_csv(OUTPUTS["bg_bridge"], data["bg_bridge"])
    write_csv(OUTPUTS["runner_refusal"], data["runner_refusal"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2602_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
