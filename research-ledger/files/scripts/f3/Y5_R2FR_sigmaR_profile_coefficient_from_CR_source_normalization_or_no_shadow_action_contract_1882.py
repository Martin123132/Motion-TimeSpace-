from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "1882"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / CHECKPOINT_ID
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1882-Y5-R2FR-sigmaR-profile-coefficient-from-CR-source-normalization-or-no-shadow-action-contract.md"

INPUTS = {
    "1881_doc": ROOT / "1881-Y5-R2FR-first-common-frame-response-kernel-or-parent-action-clause.md",
    "1881_kernel": OUT / "P8_Y5_PARENT_QLOC_1881_COMMON_FRAME_RESPONSE_KERNEL_ROWS.csv",
    "1881_bridge": OUT / "P8_Y5_PARENT_QLOC_1881_PPN_GAMMA_BRIDGE.csv",
    "1881_gap": OUT / "P8_Y5_PARENT_QLOC_1881_SIGMAR_PROFILE_GAP_LEDGER.csv",
    "1881_validation": OUT / "P8_Y5_BRR545_1881_VALIDATION.csv",
    "motion_load": ROOT / "02-motion-load-local-GR-reduction.md",
    "coframe_leak": OUT / "P8_Y5_PARENT_QLOC_1879_COMMON_FRAME_LEAK_BOUND_ROWS.csv",
    "coframe_ownership_doc": ROOT / "1879-Y5-R2FR-parent-coframe-ownership-or-common-frame-leak-bound.md",
    "terminal_coframe_doc": ROOT / "1880-Y5-R2FR-terminal-public-coframe-no-shadow-frame-or-bg-bound-projection.md",
    "profile_1743": OUT / "P8_Y5_PARENT_QLOC_1743_WEAK_FIELD_PROFILE_FIRST_ROW.csv",
    "tail_1746_doc": ROOT / "1746-Y5-R2FR-screened-tail-derivative-law-or-finite-transition-wall-bound.md",
    "local_bounds": ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv",
}

SOURCE_NEEDLES = {
    "1881_doc": [
        "SIGMAR_PROFILE_OR_NO_SHADOW_ACTION_CONTRACT_SELECTED_NEXT",
        "|b_R x_U|",
    ],
    "1881_kernel": [
        "RKR1881_0_C_R_conformal_PPN_gamma",
        "s_R=b_R x_U",
    ],
    "1881_bridge": [
        "PGB1881_0_Cassini_gamma_to_sR",
        "1.14998677515e-05",
    ],
    "1881_gap": [
        "GAP1881_1_xU_profile",
        "MISSING_PROFILE_NORMALIZATION",
    ],
    "1881_validation": [
        "VAL1881_OVERALL,PASS",
    ],
    "motion_load": [
        "T^2 = 1 - L",
        "S_p = 1 + 2p U/c^2",
        "gamma = p",
    ],
    "coframe_leak": [
        "CFL1879_0_bR",
        "d ln A_R(C_R)/dC_R",
    ],
    "coframe_ownership_doc": [
        "C_R excluded from Q_vis or killed before readout",
        "=> b_R = 0",
    ],
    "terminal_coframe_doc": [
        "no C_R/J_q Weyl, disformal, source-prefactor, endpoint, or post-readout slot exists",
        "TERMINAL_PUBLIC_COFRAME_NO_SHADOW_NOT_DERIVED",
    ],
    "profile_1743": [
        "WFP1743_1_screened_scaling_shape",
        "x_U = O(U_B^(2pS), U_B^pL, U_B^pT)",
    ],
    "tail_1746_doc": [
        "TAIL_DERIVATIVE_LAW_DERIVED_CONDITIONALLY",
        "mu_m^2",
    ],
    "local_bounds": [
        "Cassini_Shapiro_gamma_2003",
        "R3_gamma",
        "2.3e-05",
    ],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1882_SOURCE_REGISTER.csv",
    "cr_weak_field_identity": OUT / "P8_Y5_PARENT_QLOC_1882_CR_WEAK_FIELD_IDENTITY.csv",
    "sigmaR_no_circularity_map": OUT / "P8_Y5_PARENT_QLOC_1882_SIGMAR_NO_CIRCULARITY_MAP.csv",
    "ppn_combination_bound": OUT / "P8_Y5_PARENT_QLOC_1882_PPN_COMBINATION_BOUND.csv",
    "source_normalization_audit": OUT / "P8_Y5_PARENT_QLOC_1882_SOURCE_NORMALIZATION_AUDIT.csv",
    "tail_route_integration": OUT / "P8_Y5_PARENT_QLOC_1882_TAIL_ROUTE_INTEGRATION.csv",
    "runner_refusal": OUT / "P8_Y5_PARENT_QLOC_1882_RUNNER_REFUSAL.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1882_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1882_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1882_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1882_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1882_VALIDATION.csv",
}


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)


def bool_string(value: Any) -> str:
    return str(value).strip().lower()


def path_has_needles(path: Path, needles: list[str]) -> tuple[bool, str]:
    if not path.exists():
        return False, "MISSING_SOURCE_PATH"
    text = path.read_text(encoding="utf-8", errors="ignore")
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return False, "MISSING_NEEDLES=" + ";".join(missing)
    return True, "OK"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path in INPUTS.items():
        ok, detail = path_has_needles(path, SOURCE_NEEDLES[source_id])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(path),
                "required_needles": " ; ".join(SOURCE_NEEDLES[source_id]),
                "source_exists": path.exists(),
                "needle_check": detail,
                "usable_for_1882": ok,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def cr_weak_field_identity_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "identity_id": "CRID1882_0_definitions",
            "object": "C_R/R_AB",
            "definition": "C_R = R_AB = ln(T^2 S)",
            "weak_field_inputs": "u=U/c^2; T^2=1-2u+O(u^2); S=1+2p u+O(u^2)",
            "derived_identity": "C_R = 2(p-1) u + O(u^2)",
            "profile_coefficient": "x_U_CR := dC_R/du|0 = 2(p-1)",
            "status": "DERIVED_SYMBOLIC_IDENTITY_NONCLAIM",
            "missing_before_claim": "p-1 source normalization from parent field equations; reciprocal-lock theorem T^2 S=1; coordinate/gauge ownership; beta/channel closure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "identity_id": "CRID1882_1_GR_limit",
            "object": "reciprocal lock",
            "definition": "T^2 S=1 implies C_R=0",
            "weak_field_inputs": "p=1 at first PPN order",
            "derived_identity": "x_U_CR=0",
            "profile_coefficient": "no first-order C_R Weyl source exists if reciprocal lock is parent-derived",
            "status": "EXACT_CONDITIONAL_ZERO_ROUTE",
            "missing_before_claim": "parent derivation of T^2 S=1 or terminal public coframe/no-shadow action clause",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "identity_id": "CRID1882_2_nonGR_residual",
            "object": "finite reciprocal residual",
            "definition": "delta_p := p-1",
            "weak_field_inputs": "C_R = 2 delta_p U/c^2 + O(U^2/c^4)",
            "derived_identity": "x_U_CR=2 delta_p",
            "profile_coefficient": "the C_R x_U profile is not independent of the PPN spatial-curvature residual",
            "status": "FREE_PROFILE_ROUTE_REJECTED_FOR_CR_CHANNEL",
            "missing_before_claim": "delta_p value/theorem-zero; no-cancellation residual vector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def sigmaR_no_circularity_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "map_id": "SNCM1882_0_sigma_from_CR",
            "assumption": "common Weyl/log-coframe shadow uses b_R := d ln A_R(C_R)/dC_R",
            "substitution": "sigma_R = b_R C_R + O(C_R^2)",
            "using_CR_identity": "C_R=2 delta_p U/c^2 + O(U^2/c^4)",
            "result": "sigma_R = 2 b_R delta_p U/c^2 + higher order",
            "sR_value": "s_R = 2 b_R delta_p",
            "status": "DERIVED_SYMBOLIC_COMPOSITION_NONCLAIM",
            "warning": "Cassini cannot be used as if x_U were independent; the same delta_p controls the baseline reciprocal-lock failure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "SNCM1882_1_generalized_gamma",
            "assumption": "baseline weak-field spatial coefficient is p=1+delta_p and conformal shadow is sigma_R=s_R U/c^2",
            "substitution": "g_obs=exp(2 sigma_R) g_base",
            "using_CR_identity": "s_R=2b_R delta_p",
            "result": "gamma_obs=(p+s_R)/(1-s_R); gamma_obs-1=(delta_p+2s_R)/(1-s_R)",
            "sR_value": "gamma_obs-1=(delta_p+4b_R delta_p)/(1-2b_R delta_p)",
            "status": "FIRST_ORDER_NO_CIRCULARITY_LAW",
            "warning": "PPN gamma bounds the combined residual delta_p and b_R, not b_R alone and not x_U alone",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "SNCM1882_2_small_residual",
            "assumption": "|delta_p| << 1 and |b_R delta_p| << 1",
            "substitution": "linearize generalized gamma",
            "using_CR_identity": "s_R=2b_R delta_p",
            "result": "gamma_obs-1 ~= delta_p(1+4b_R)",
            "sR_value": "Cassini target becomes |delta_p(1+4b_R)| <= 2.3e-5 at leading order",
            "status": "LINEAR_BOUND_FORM_NONCLAIM",
            "warning": "a tuned b_R≈-1/4 cancellation is not allowed as evidence without a no-cancellation theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def ppn_combination_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "bound_id": "PCB1882_0_exact_combo",
            "observable": "gamma_obs_minus_1",
            "empirical_bound": "2.3e-05",
            "bound_formula": "|(delta_p+4b_R delta_p)/(1-2b_R delta_p)| <= 2.3e-05",
            "source_row": "Cassini_Shapiro_gamma_2003:R3_gamma",
            "status": "BOUND_FORM_READY_VALUES_MISSING",
            "missing_to_score": "delta_p theorem-zero or numeric bound; b_R theorem-zero or numeric bound; no-cancellation policy; beta/source/preferred-frame residuals",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        },
        {
            "branch_id": BRANCH_ID,
            "bound_id": "PCB1882_1_zero_delta_p",
            "observable": "gamma_obs_minus_1",
            "empirical_bound": "2.3e-05",
            "bound_formula": "if delta_p=0 by parent reciprocal lock, then C_R=0 and the first-order b_R C_R channel vanishes",
            "source_row": "02-motion-load-local-GR-reduction.md:p=1_if_T2S=1",
            "status": "EXACT_CONDITIONAL_ZERO_ROUTE_VALUES_MISSING",
            "missing_to_score": "parent derivation of reciprocal lock; beta=1 second-order closure; action-domain no-shadow or higher-order C_R residual control",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        },
        {
            "branch_id": BRANCH_ID,
            "bound_id": "PCB1882_2_zero_bR",
            "observable": "gamma_obs_minus_1",
            "empirical_bound": "2.3e-05",
            "bound_formula": "if b_R=0 by terminal public coframe/no-shadow action, then gamma_obs-1 reduces to delta_p",
            "source_row": "1879/1880 no-shadow conditional theorem",
            "status": "EXACT_CONDITIONAL_ZERO_ROUTE_VALUES_MISSING",
            "missing_to_score": "parent terminal public coframe/action-domain proof; delta_p field-equation source normalization",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        },
        {
            "branch_id": BRANCH_ID,
            "bound_id": "PCB1882_3_no_cancellation_guard",
            "observable": "gamma_obs_minus_1",
            "empirical_bound": "2.3e-05",
            "bound_formula": "do not count delta_p(1+4b_R) cancellation as stable evidence unless b_R=-1/4 is parent-derived and beta/source channels also close",
            "source_row": "1881 gap ledger no-other-channel rule",
            "status": "NO_CANCELLATION_GUARD_ACTIVE",
            "missing_to_score": "full local residual vector with independent gates",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        },
    ]


def source_normalization_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SNA1882_0_clock_coefficient",
            "requirement": "T^2=1-2U/c^2 is owned by measured GM/source normalization",
            "current_evidence": "motion-load weak-field lane supplies T^2=1-L with L=2GM/(rc^2)",
            "status": "CONDITIONAL_INPUT_AVAILABLE",
            "missing": "parent field equation and source stress map that make measured GM the same GM used by PPN comparison",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SNA1882_1_spatial_coefficient",
            "requirement": "p=1 or delta_p source equation",
            "current_evidence": "p=1 follows if T^2S=1, but reciprocal lock remains parent-unsigned",
            "status": "MISSING_PARENT_RECIPROCAL_LOCK_OR_DELTA_P_SOURCE",
            "missing": "Euler/Bianchi/source-normalized equation for delta_p; not a fitted PPN insertion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SNA1882_2_beta_channel",
            "requirement": "second-order beta=1 or explicit beta residual",
            "current_evidence": "02 marks beta completion as conditional, not parent-derived",
            "status": "MISSING_BETA_CLOSURE",
            "missing": "second-order metric completion in same gauge/source normalization as gamma",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SNA1882_3_source_shadow",
            "requirement": "source prefactor w_R and endpoint/tau channels do not reopen the same C_R dependence",
            "current_evidence": "1879/1880 keep w_R and endpoint rows live",
            "status": "MISSING_SOURCE_ENDPOINT_TAU_CLOSURE",
            "missing": "terminal public coframe/source descent or finite bound rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def tail_route_integration_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "integration_id": "TRI1882_0_CR_kinematic_route",
            "route": "C_R/R_AB weak-field kinematic identity",
            "what_it_now_supplies": "x_U_CR=2delta_p symbolically",
            "what_it_does_not_supply": "numeric delta_p, parent reciprocal lock, beta/source closure",
            "status": "BEST_FOR_LOCAL_GR_REDUCTION",
            "next_use": "derive delta_p=0 or build full PPN residual vector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "integration_id": "TRI1882_1_q_loc_profile_route",
            "route": "Gamma_eff/Khat screened-tail profile",
            "what_it_now_supplies": "source/profile formula shape and conditional tail derivative law",
            "what_it_does_not_supply": "C_R first-order coefficient independent of delta_p",
            "status": "RETAIN_FOR_QLOC_AND_FINITE_RESIDUALS",
            "next_use": "use for q_loc/source residual bounds, not as a free replacement for x_U_CR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "integration_id": "TRI1882_2_no_shadow_route",
            "route": "terminal public coframe/no extra action slot",
            "what_it_now_supplies": "exact conditional b_R=d_R=w_R=endpoint=0",
            "what_it_does_not_supply": "parent-signed action-domain exclusion",
            "status": "CLEAN_ZERO_ROUTE_UNSIGNED",
            "next_use": "continue only if parent action grammar can exclude C_R/J_q slots",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1882_0_combo_gamma_runner",
            "runner": "future delta_p/b_R to Cassini gamma comparison",
            "current_status": "REFUSE_CLAIM_RUN",
            "reason": "combo formula exists, but delta_p and b_R are both missing theorem-zero/numeric source rows and beta/source channels are open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1882_1_reciprocal_lock_runner",
            "runner": "future T^2S=1 parent proof checker",
            "current_status": "REFUSE_CLAIM_RUN",
            "reason": "reciprocal lock is an exact conditional route but not parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1882_2_local_GR_runner",
            "runner": "future local GR/Newton reduction gate",
            "current_status": "REFUSE_CLAIM_RUN",
            "reason": "gamma identity alone lacks beta, Bianchi/conservation, source normalization, no-shadow and residual-vector closure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1882_0_internal_identity",
            "claim": "1882 may use x_U_CR=2(p-1) internally for the C_R/R_AB channel",
            "status": "ALLOW_INTERNAL_NONCLAIM_IDENTITY",
            "reason": "it is a first-order algebraic consequence of C_R=ln(T^2S) and the weak-field metric expansion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1882_1_xU_known_numeric",
            "claim": "x_U is numerically known for scoring",
            "status": "BLOCKED",
            "reason": "x_U_CR=2delta_p but delta_p is not derived or sourced",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1882_2_ppn_pass",
            "claim": "MTS passes PPN gamma/Cassini",
            "status": "BLOCKED",
            "reason": "only a combo-bound form exists; coefficients and channel closure are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1882_3_local_GR",
            "claim": "local GR/Newton is derived",
            "status": "BLOCKED",
            "reason": "reciprocal lock/no-shadow/beta/source conservation are not parent-derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1882_0_xU_identity",
            "decision": "XU_CR_PROFILE_DERIVED_SYMBOLICALLY_AS_2_DELTA_P",
            "basis": "C_R=ln(T^2S), T^2=1-2U/c^2, S=1+2pU/c^2",
            "consequence": "x_U is no longer a free knob for the C_R branch; it is the reciprocal-lock residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1882_1_no_circular_score",
            "decision": "CASSINI_BOUNDS_DELTA_P_AND_BR_NOT_BR_ALONE",
            "basis": "gamma_obs=(p+s_R)/(1-s_R) with s_R=2b_Rdelta_p",
            "consequence": "future runner must score the combined residual vector and reject cancellation-only wins",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1882_2_zero_routes",
            "decision": "TWO_CLEAN_ZERO_ROUTES_IDENTIFIED",
            "basis": "delta_p=0 from reciprocal lock kills C_R first order; b_R=0 from no-shadow action kills common Weyl response",
            "consequence": "derive reciprocal lock first if aiming at GR reduction; derive no-shadow action if aiming at matter-frame ownership",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1882_3_next",
            "decision": "RECIPROCAL_LOCK_DELTA_P_ZERO_OR_FULL_PPN_VECTOR_SELECTED_NEXT",
            "basis": "the remaining unknown is now delta_p plus beta/source channels, not an unconstrained x_U",
            "consequence": "1883 should try to derive T^2S=1/delta_p=0 from parent constraints, or build the full delta_p,b_R,beta,w_R residual-vector dry-runner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1882_0_primary",
            "target_doc": "1883-Y5-R2FR-reciprocal-lock-delta-p-zero-or-full-PPN-residual-vector.md",
            "target_script": "scripts/Y5_R2FR_reciprocal_lock_delta_p_zero_or_full_PPN_residual_vector_1883.py",
            "objective": "attempt to parent-derive T^2S=1/delta_p=0 from the C_R constraint/source-normalized field equations; if not, build a full PPN residual vector for delta_p,b_R,beta,w_R,d_R,endpoint with claim refusal.",
            "selection_status": "selected",
            "success_condition": "parent-signed reciprocal lock, or schema-ready full PPN residual-vector runner that prevents gamma-only or cancellation-only claims.",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1882_1_secondary",
            "target_doc": "1883b-Y5-R2FR-parent-action-no-shadow-slot-exclusion-retry.md",
            "target_script": "scripts/Y5_R2FR_parent_action_no_shadow_slot_exclusion_retry_1883b.py",
            "objective": "retry the terminal public coframe/action-domain exclusion specifically for the A_R(C_R) Weyl slot after the x_U_CR identity.",
            "selection_status": "held_secondary",
            "success_condition": "parent grammar excludes A_R(C_R), or b_R remains finite residual input.",
            "valid_for_claim": False,
        },
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status_id": "STATUS1882_0_progress",
            "plain_english": "The C_R profile coefficient is now sharply identified: for the weak-field local branch, x_U_CR=2(p-1).",
            "technical_state": "first-order expansion of ln(T^2S) converts x_U into the reciprocal-lock residual delta_p",
            "risk_level": "REAL_PROGRESS_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status_id": "STATUS1882_1_caution",
            "plain_english": "This removes a free knob, but it also means Cassini gamma cannot be used circularly to prove the same gamma residual is small.",
            "technical_state": "gamma_obs-1=(delta_p+4b_Rdelta_p)/(1-2b_Rdelta_p) under the conformal C_R branch",
            "risk_level": "NO_CIRCULARITY_GUARD",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status_id": "STATUS1882_2_missing",
            "plain_english": "The next heart of the problem is delta_p: prove reciprocal lock from the parent theory, or score the full residual vector honestly.",
            "technical_state": "delta_p, b_R, beta, source/endpoint/preferred-frame channels remain unclosed",
            "risk_level": "MAIN_BOTTLENECK",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def all_output_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "cr_weak_field_identity": cr_weak_field_identity_rows(),
        "sigmaR_no_circularity_map": sigmaR_no_circularity_rows(),
        "ppn_combination_bound": ppn_combination_bound_rows(),
        "source_normalization_audit": source_normalization_audit_rows(),
        "tail_route_integration": tail_route_integration_rows(),
        "runner_refusal": runner_refusal_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }


def copy_branch_artifacts() -> None:
    shutil.copy2(OUTPUTS["cr_weak_field_identity"], MICROSCOPE_RESIDUALS / OUTPUTS["cr_weak_field_identity"].name)
    shutil.copy2(OUTPUTS["ppn_combination_bound"], QUARANTINE / OUTPUTS["ppn_combination_bound"].name)
    shutil.copy2(OUTPUTS["sigmaR_no_circularity_map"], QUEUE / "JR1882_SIGMAR_NO_CIRCULARITY_MAP_NONCLAIM.csv")
    shutil.copy2(OUTPUTS["source_normalization_audit"], QUEUE / "JR1882_SOURCE_NORMALIZATION_AUDIT_NONCLAIM.csv")


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    checked = 0
    offenders: list[str] = []
    for path in paths:
        for row in csv_rows(path):
            for key in ("valid_for_claim", "claim_allowed", "score_ready", "prediction_ready", "valid_prediction_row"):
                if key in row:
                    checked += 1
                    if bool_string(row[key]) == "true":
                        offenders.append(f"{path.name}:{key}=true")
    if offenders:
        return False, ";".join(offenders)
    return True, f"checked={checked}"


def missing_rows_not_ready(paths: list[Path]) -> tuple[bool, str]:
    checked = 0
    offenders: list[str] = []
    markers = ("MISSING_", "UNSIGNED", "BLOCKED", "NOT_PARENT", "NOT_FOUND")
    for path in paths:
        for row in csv_rows(path):
            joined = " ".join(str(value) for value in row.values())
            if not any(marker in joined for marker in markers):
                continue
            checked += 1
            for key in ("valid_for_claim", "claim_allowed", "score_ready", "prediction_ready", "numeric_kernel_ready", "proof_closed"):
                if key in row and bool_string(row[key]) == "true":
                    offenders.append(f"{path.name}:{row}")
                    break
    if offenders:
        return False, ";".join(offenders[:5])
    return True, f"checked_missing_or_blocked_rows={checked}"


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    details: list[str] = []
    for path in paths:
        rows = csv_rows(path)
        if not rows:
            return False, f"{path.name}:NO_ROWS"
        details.append(f"{path.name}:{len(rows)}")
    return True, ";".join(details)


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    rows_by_name = {key: csv_rows(path) for key, path in OUTPUTS.items() if key != "validation"}
    checks: list[dict[str, Any]] = []

    sources = rows_by_name["source_register"]
    checks.append(
        {
            "validation_id": "VAL1882_0_sources",
            "status": "PASS" if all(row["needle_check"] == "OK" for row in sources) else "FAIL",
            "detail": "1881/weak-field/coframe/profile/tail/local-bound sources available and needle-checked",
            "valid_for_claim": False,
        }
    )

    identities = rows_by_name["cr_weak_field_identity"]
    checks.append(
        {
            "validation_id": "VAL1882_1_cr_identity",
            "status": "PASS"
            if any(row["profile_coefficient"] == "x_U_CR := dC_R/du|0 = 2(p-1)" for row in identities)
            and any(row["status"] == "FREE_PROFILE_ROUTE_REJECTED_FOR_CR_CHANNEL" for row in identities)
            else "FAIL",
            "detail": "C_R weak-field identity derives x_U_CR=2(p-1) and rejects free x_U for this channel",
            "valid_for_claim": False,
        }
    )

    no_circular = rows_by_name["sigmaR_no_circularity_map"]
    checks.append(
        {
            "validation_id": "VAL1882_2_no_circularity_map",
            "status": "PASS"
            if any(row["sR_value"] == "s_R = 2 b_R delta_p" for row in no_circular)
            and any("gamma_obs-1" in row["result"] for row in no_circular)
            else "FAIL",
            "detail": "sigma_R map now binds b_R to delta_p and gives generalized gamma law",
            "valid_for_claim": False,
        }
    )

    bounds = rows_by_name["ppn_combination_bound"]
    checks.append(
        {
            "validation_id": "VAL1882_3_combo_bound",
            "status": "PASS"
            if len(bounds) == 4
            and all(bool_string(row["score_ready"]) == "false" for row in bounds)
            and any(row["status"] == "NO_CANCELLATION_GUARD_ACTIVE" for row in bounds)
            else "FAIL",
            "detail": "Cassini bound is a nonclaim combined delta_p/b_R bound with no-cancellation guard",
            "valid_for_claim": False,
        }
    )

    audit = rows_by_name["source_normalization_audit"]
    checks.append(
        {
            "validation_id": "VAL1882_4_source_audit",
            "status": "PASS"
            if any(row["status"] == "MISSING_PARENT_RECIPROCAL_LOCK_OR_DELTA_P_SOURCE" for row in audit)
            and any(row["status"] == "MISSING_BETA_CLOSURE" for row in audit)
            else "FAIL",
            "detail": "source normalization audit keeps delta_p, beta, source and endpoint gaps open",
            "valid_for_claim": False,
        }
    )

    integration = rows_by_name["tail_route_integration"]
    checks.append(
        {
            "validation_id": "VAL1882_5_tail_integration",
            "status": "PASS"
            if any(row["status"] == "BEST_FOR_LOCAL_GR_REDUCTION" for row in integration)
            and any(row["status"] == "RETAIN_FOR_QLOC_AND_FINITE_RESIDUALS" for row in integration)
            else "FAIL",
            "detail": "C_R kinematic route and q_loc screened-tail route are separated",
            "valid_for_claim": False,
        }
    )

    runners = rows_by_name["runner_refusal"]
    checks.append(
        {
            "validation_id": "VAL1882_6_runner_refusal",
            "status": "PASS" if all(row["current_status"].startswith("REFUSE_CLAIM_RUN") for row in runners) else "FAIL",
            "detail": "combo gamma, reciprocal lock and local-GR runners refuse claim runs",
            "valid_for_claim": False,
        }
    )

    claims = rows_by_name["claim_gate"]
    checks.append(
        {
            "validation_id": "VAL1882_7_claim_gate",
            "status": "PASS"
            if any(row["status"] == "ALLOW_INTERNAL_NONCLAIM_IDENTITY" for row in claims)
            and all(bool_string(row["claim_allowed"]) == "false" for row in claims)
            else "FAIL",
            "detail": "only internal nonclaim identity use is allowed",
            "valid_for_claim": False,
        }
    )

    decisions = rows_by_name["decision"]
    checks.append(
        {
            "validation_id": "VAL1882_8_decision",
            "status": "PASS"
            if any(row["decision"] == "XU_CR_PROFILE_DERIVED_SYMBOLICALLY_AS_2_DELTA_P" for row in decisions)
            and any(row["decision"] == "RECIPROCAL_LOCK_DELTA_P_ZERO_OR_FULL_PPN_VECTOR_SELECTED_NEXT" for row in decisions)
            else "FAIL",
            "detail": "decision selects reciprocal lock delta_p zero or full PPN vector next",
            "valid_for_claim": False,
        }
    )

    next_targets = rows_by_name["next_target"]
    checks.append(
        {
            "validation_id": "VAL1882_9_next_target",
            "status": "PASS"
            if any(row["route_id"] == "NEXT1882_0_primary" and row["selection_status"] == "selected" for row in next_targets)
            else "FAIL",
            "detail": "1883 reciprocal lock or full PPN residual vector target selected",
            "valid_for_claim": False,
        }
    )

    status_rows = rows_by_name["project_status"]
    checks.append(
        {
            "validation_id": "VAL1882_10_project_status",
            "status": "PASS"
            if len(status_rows) == 3
            and any(row["risk_level"] == "NO_CIRCULARITY_GUARD" for row in status_rows)
            and any(row["risk_level"] == "MAIN_BOTTLENECK" for row in status_rows)
            else "FAIL",
            "detail": "project status records progress, no-circularity guard and delta_p bottleneck",
            "valid_for_claim": False,
        }
    )

    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1882_11_claim_flags_false",
            "status": "PASS" if flags_ok else "FAIL",
            "detail": flags_detail,
            "valid_for_claim": False,
        }
    )

    missing_ok, missing_detail = missing_rows_not_ready(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1882_12_missing_not_ready",
            "status": "PASS" if missing_ok else "FAIL",
            "detail": missing_detail,
            "valid_for_claim": False,
        }
    )

    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1882_13_csv_parse",
            "status": "PASS" if parse_ok else "FAIL",
            "detail": parse_detail,
            "valid_for_claim": False,
        }
    )

    copied_paths = [
        MICROSCOPE_RESIDUALS / OUTPUTS["cr_weak_field_identity"].name,
        QUARANTINE / OUTPUTS["ppn_combination_bound"].name,
        QUEUE / "JR1882_SIGMAR_NO_CIRCULARITY_MAP_NONCLAIM.csv",
        QUEUE / "JR1882_SOURCE_NORMALIZATION_AUDIT_NONCLAIM.csv",
    ]
    checks.append(
        {
            "validation_id": "VAL1882_14_branch_copies",
            "status": "PASS" if all(path.exists() for path in copied_paths) else "FAIL",
            "detail": ";".join(str(path) for path in copied_paths),
            "valid_for_claim": False,
        }
    )

    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append(
        {
            "validation_id": "VAL1882_15_pycache_absent",
            "status": "PASS" if not pycache.exists() else "FAIL",
            "detail": str(pycache),
            "valid_for_claim": False,
        }
    )

    formalization_hits = list(FORMALIZATION.rglob("*1882*")) if FORMALIZATION.exists() else []
    checks.append(
        {
            "validation_id": "VAL1882_16_formalization_untouched",
            "status": "PASS" if not formalization_hits else "FAIL",
            "detail": f"formalization_1882_count={len(formalization_hits)}",
            "valid_for_claim": False,
        }
    )

    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append(
        {
            "validation_id": "VAL1882_OVERALL",
            "status": "PASS" if fail_count == 0 else "FAIL",
            "detail": "1882 sigmaR profile coefficient from C_R source normalization or no-shadow action contract",
            "valid_for_claim": False,
        }
    )
    return checks


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1882 - Sigma_R Profile Coefficient From C_R Source Normalization Or No-Shadow Action Contract

**Private status:** nonclaim derivation/projection checkpoint.

## Result

The `C_R/R_AB` weak-field profile coefficient is no longer free:

```text
u = U/c^2
T^2 = 1 - 2u + O(u^2)
S = 1 + 2p u + O(u^2)
C_R = R_AB = ln(T^2 S)
C_R = 2(p-1)u + O(u^2)
x_U_CR = dC_R/du|0 = 2(p-1)
```

So if the common Weyl/log-coframe coupling is `sigma_R=b_R C_R`, then

```text
s_R = 2 b_R delta_p, where delta_p=p-1
gamma_obs = (p+s_R)/(1-s_R)
gamma_obs - 1 = (delta_p + 4 b_R delta_p)/(1 - 2 b_R delta_p)
```

This is real progress because `x_U` has stopped being a foggy free coefficient for the `C_R` channel. It is also a guardrail: Cassini gamma bounds the combined `delta_p,b_R` residual, not `b_R` alone. No PPN/local-GR pass is claimed.

## C_R Weak-Field Identity

{markdown_table(rows_by_name["cr_weak_field_identity"])}

## Sigma_R No-Circularity Map

{markdown_table(rows_by_name["sigmaR_no_circularity_map"])}

## PPN Combination Bound

{markdown_table(rows_by_name["ppn_combination_bound"])}

## Source Normalization Audit

{markdown_table(rows_by_name["source_normalization_audit"])}

## Tail Route Integration

{markdown_table(rows_by_name["tail_route_integration"])}

## Runner Refusal

{markdown_table(rows_by_name["runner_refusal"])}

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Claim Gate

{markdown_table(rows_by_name["claim_gate"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Project Status Snapshot

{markdown_table(rows_by_name["project_status"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Validation

{markdown_table(validation)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows_by_name = all_output_rows()
    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    remove_pycache()
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()
