from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "1881"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / CHECKPOINT_ID
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1881-Y5-R2FR-first-common-frame-response-kernel-or-parent-action-clause.md"

INPUTS = {
    "1880_doc": ROOT / "1880-Y5-R2FR-terminal-public-coframe-no-shadow-frame-or-bg-bound-projection.md",
    "1880_projection_contracts": OUT / "P8_Y5_PARENT_QLOC_1880_COMMON_FRAME_PROJECTION_CONTRACTS.csv",
    "1880_bound_inputs": OUT / "P8_Y5_PARENT_QLOC_1880_BOUND_INPUT_ROWS_NONCLAIM.csv",
    "1880_validation": OUT / "P8_Y5_BRR545_1880_VALIDATION.csv",
    "1741_doc": ROOT / "1741-Y5-R2FR-first-bg-response-map-or-real-R10-bound-curve.md",
    "1741_response_map": OUT / "P8_Y5_PARENT_QLOC_1741_BG_RESPONSE_MAP.csv",
    "1741_gamma_bridge": OUT / "P8_Y5_PARENT_QLOC_1741_PPN_GAMMA_BOUND_BRIDGE.csv",
    "local_bounds": ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv",
    "1030_spm_gate": ROOT / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md",
}

SOURCE_NEEDLES = {
    "1880_doc": [
        "FIRST_RESPONSE_KERNEL_OR_PARENT_ACTION_CLAUSE_SELECTED_NEXT",
        "Projection Contracts",
    ],
    "1880_projection_contracts": [
        "PRC1880_0_PPN_metric",
        "MISSING_RESPONSE_KERNEL_AND_COEFFICIENTS",
    ],
    "1880_bound_inputs": [
        "BIN1880_1_response_kernels",
        "MISSING_RESPONSE_KERNELS",
    ],
    "1880_validation": [
        "VAL1880_OVERALL,PASS",
    ],
    "1741_doc": [
        "CONFORMAL_BG_TO_GAMMA_MAP_STAGED",
        "Cassini",
    ],
    "1741_response_map": [
        "BRM1741_0_conformal_PPN_gamma",
        "gamma_eff=(1+s_X)/(1-s_X)",
    ],
    "1741_gamma_bridge": [
        "PGB1741_0_Cassini_gamma_bridge",
        "2.3e-05",
    ],
    "local_bounds": [
        "Cassini_Shapiro_gamma_2003",
        "R3_gamma",
        "2.3e-05",
    ],
    "1030_spm_gate": [
        "EXACT_CLOSURE_CLAUSE_NOT_DERIVED",
        "single public metric",
    ],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1881_SOURCE_REGISTER.csv",
    "parent_clause_audit": OUT / "P8_Y5_PARENT_QLOC_1881_PARENT_ACTION_CLAUSE_AUDIT.csv",
    "response_kernels": OUT / "P8_Y5_PARENT_QLOC_1881_COMMON_FRAME_RESPONSE_KERNEL_ROWS.csv",
    "ppn_gamma_bridge": OUT / "P8_Y5_PARENT_QLOC_1881_PPN_GAMMA_BRIDGE.csv",
    "gap_ledger": OUT / "P8_Y5_PARENT_QLOC_1881_SIGMAR_PROFILE_GAP_LEDGER.csv",
    "runner_refusal": OUT / "P8_Y5_PARENT_QLOC_1881_RUNNER_REFUSAL.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1881_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1881_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1881_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1881_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1881_VALIDATION.csv",
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
                "usable_for_1881": ok,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def parent_clause_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PCA1881_0_action_domain",
            "clause": "matter action domain excludes independent C_R/J_q frame arguments",
            "needed_statement": "S_matter = Sbar[q_vis(Phi), Psi, theta_pub] with no A_R(C_R), B_R(C_R), w_A(C_R), E(q_vis,C_R), endpoint(C_R), or post-readout slot",
            "current_status": "NOT_FOUND_PARENT_SIGNED",
            "proof_closed": False,
            "why_it_matters": "would force b_R=d_R=w_R=epsilon_endpoint_R=0 rather than bounding them phenomenologically",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PCA1881_1_terminal_public_coframe",
            "clause": "ordinary clocks and rulers use a terminal public coframe",
            "needed_statement": "all ordinary readout maps factor through one terminal e_pub=E(Q_vis) before matter coupling",
            "current_status": "EXACT_CONDITIONAL_ONLY",
            "proof_closed": False,
            "why_it_matters": "would prevent a hidden common-frame metric from surviving as a local PPN/clock/orbital channel",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PCA1881_2_connection_source_boundary",
            "clause": "connection, source support, tau and boundary maps descend through the same public domain",
            "needed_statement": "omega[e_pub], tau, source denominators and endpoint maps cannot reintroduce C_R/J_q dependence",
            "current_status": "INHERITANCE_STACK_UNSIGNED",
            "proof_closed": False,
            "why_it_matters": "otherwise a zero metric shadow can leak through source normalization or endpoint projection",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PCA1881_3_verdict",
            "clause": "parent action no-shadow clause",
            "needed_statement": "PCA1881_0 through PCA1881_2 are parent-signed in one branch",
            "current_status": "PARENT_ACTION_NO_SHADOW_CLAUSE_NOT_DERIVED",
            "proof_closed": False,
            "why_it_matters": "zero route remains alive but not claimable; empirical response-kernel route is needed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def response_kernel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "kernel_id": "RKR1881_0_C_R_conformal_PPN_gamma",
            "projection_id": "PRC1880_0_PPN_metric",
            "arena": "PPN_metric",
            "observable": "gamma_minus_1",
            "coefficient_slot": "b_R",
            "ansatz": "g_obs=exp(2 sigma_R) g_GR, sigma_R=s_R U/c^2, s_R=b_R x_U",
            "derived_response": "gamma_eff=(1+s_R)/(1-s_R); gamma_minus_1=2 s_R/(1-s_R)",
            "response_kernel": "K_gamma_bR = 2 |x_U|/(1-|s_R|)^2 exact-local-envelope; linear K_gamma_bR ~= 2 |x_U|",
            "empirical_bridge": "Cassini R3_gamma: |gamma_minus_1| <= 2.3e-05",
            "source_paths": f"{INPUTS['1741_response_map']};{INPUTS['1741_gamma_bridge']};{INPUTS['local_bounds']}",
            "source_backed_kernel": True,
            "numeric_kernel_ready": False,
            "prediction_ready": False,
            "score_ready": False,
            "current_status": "SOURCE_BACKED_CONDITIONAL_KERNEL_STAGED_NONCLAIM",
            "missing_inputs": "MISSING_b_R_VALUE;MISSING_x_U_PROFILE;MISSING_SOURCE_NORMALIZATION;MISSING_NO_OTHER_PPN_CHANNELS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "kernel_id": "RKR1881_1_common_conformal_WEP_guard",
            "projection_id": "PRC1880_2_clock_WEP",
            "arena": "clock_WEP_material",
            "observable": "eta_AB; Delta nu/nu",
            "coefficient_slot": "b_R;w_R",
            "ansatz": "all ordinary matter sees the same conformal e_obs",
            "derived_response": "pure common-mode conformal rescaling is not composition dependence by itself",
            "response_kernel": "K_WEP_common_mode is undefined until species/source/readout marker sensitivities Delta w_AB are derived",
            "empirical_bridge": "MICROSCOPE/material/clock rows cannot be used without a composition map",
            "source_paths": f"{INPUTS['1741_response_map']}",
            "source_backed_kernel": True,
            "numeric_kernel_ready": False,
            "prediction_ready": False,
            "score_ready": False,
            "current_status": "COMMON_MODE_GUARD_STAGED_NONCLAIM",
            "missing_inputs": "MISSING_COMPOSITION_MAP;MISSING_DELTA_w_AB;MISSING_CLOCK_SENSITIVITY_MATRIX",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "kernel_id": "RKR1881_2_d_R_preferred_frame_PPN",
            "projection_id": "PRC1880_1_PPN_preferred",
            "arena": "PPN_preferred_frame",
            "observable": "alpha1;alpha2;alpha3;xi",
            "coefficient_slot": "d_R",
            "ansatz": "disformal/preferred-frame shadow term in observed metric or connection",
            "derived_response": "no source-backed MTS-specific d_R -> alpha_i kernel found in current sources",
            "response_kernel": "MISSING_K_alpha_i_dR",
            "empirical_bridge": "Will PPN bounds exist locally but cannot be attached to d_R by assertion",
            "source_paths": f"{INPUTS['1880_projection_contracts']};{INPUTS['local_bounds']}",
            "source_backed_kernel": False,
            "numeric_kernel_ready": False,
            "prediction_ready": False,
            "score_ready": False,
            "current_status": "MISSING_RESPONSE_KERNEL",
            "missing_inputs": "MISSING_DISFORMAL_METRIC_ANSATZ;MISSING_PREFERRED_FRAME_NORMALIZATION;MISSING_K_alpha_i_dR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "kernel_id": "RKR1881_3_orbital_light_time",
            "projection_id": "PRC1880_3_orbital",
            "arena": "orbital_light_time",
            "observable": "precession;acceleration;light-time residual",
            "coefficient_slot": "b_R;d_R;epsilon_endpoint_R",
            "ansatz": "common-frame metric residual projected into orbit/light-time observables",
            "derived_response": "can be routed through PPN gamma/beta only after beta/source/endpoint channels are normalized",
            "response_kernel": "MISSING_K_orbital_vector",
            "empirical_bridge": "orbital rows remain downstream of PPN/source normalization",
            "source_paths": f"{INPUTS['1880_projection_contracts']};{INPUTS['1741_gamma_bridge']}",
            "source_backed_kernel": False,
            "numeric_kernel_ready": False,
            "prediction_ready": False,
            "score_ready": False,
            "current_status": "MISSING_RESPONSE_KERNEL",
            "missing_inputs": "MISSING_BETA_CHANNEL;MISSING_ENDPOINT_PROJECTION;MISSING_ORBITAL_RESPONSE_MATRIX",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "kernel_id": "RKR1881_4_R10_wrong_route_guard",
            "projection_id": "PRC1880_4_R10_guarded",
            "arena": "R10_finite_range",
            "observable": "alpha(lambda)",
            "coefficient_slot": "w_R/source_leg_after_finite_operator",
            "ansatz": "finite Yukawa operator plus source/test coupling",
            "derived_response": "common-frame source leg is not a finite-range substitute",
            "response_kernel": "MISSING_Z_R_M_R2_lambda_R_source_test_tau",
            "empirical_bridge": "R10 scoring held until finite range/operator rows exist",
            "source_paths": f"{INPUTS['1880_projection_contracts']}",
            "source_backed_kernel": False,
            "numeric_kernel_ready": False,
            "prediction_ready": False,
            "score_ready": False,
            "current_status": "WRONG_ROUTE_GUARD_ACTIVE",
            "missing_inputs": "MISSING_FINITE_OPERATOR;MISSING_RANGE;MISSING_SOURCE_TEST_COUPLINGS;MISSING_R10_CURVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def ppn_gamma_bridge_rows() -> list[dict[str, Any]]:
    epsilon = 2.3e-5
    exact_sufficient_bound = epsilon / (2.0 + epsilon)
    return [
        {
            "branch_id": BRANCH_ID,
            "bridge_id": "PGB1881_0_Cassini_gamma_to_sR",
            "dataset_id": "Cassini_Shapiro_gamma_2003",
            "row_id": "R3_gamma",
            "observable": "gamma_minus_1",
            "upper_bound": epsilon,
            "units": "dimensionless",
            "exact_inequality": "|2 s_R/(1-s_R)| <= 2.3e-05 with |s_R|<1",
            "exact_sufficient_bound": f"|s_R| <= {exact_sufficient_bound:.12g}",
            "linearized_bound": "|s_R| ~= |b_R x_U| <= 1.15e-05",
            "bridge_formula": "s_R=b_R x_U, so |b_R x_U| is the first PPN-gamma target, not a direct b_R score",
            "reference_path_or_url": "https://www.nature.com/articles/nature01997; doi:10.1038/nature01997",
            "bridge_status": "SOURCE_BACKED_CONDITIONAL_NONCLAIM",
            "why_nonclaim": "b_R, x_U/source profile, normalization, beta channel and no-other-channel theorem are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def gap_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gap_id": "GAP1881_0_bR_value_or_zero",
            "missing_item": "b_R numeric value or theorem-zero certificate",
            "needed_for": "turn PGB1881_0 into an MTS prediction",
            "current_status": "MISSING_COEFFICIENT",
            "next_action": "derive b_R=0 from parent no-shadow clause, or source/bound b_R as finite closure coefficient",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gap_id": "GAP1881_1_xU_profile",
            "missing_item": "x_U profile coefficient in sigma_R=s_R U/c^2",
            "needed_for": "map C_R/R_AB cell amplitude to solar-system PPN potential",
            "current_status": "MISSING_PROFILE_NORMALIZATION",
            "next_action": "derive x_U from C_R=ln(T^2 S), source denominator, and local weak-field normalization",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gap_id": "GAP1881_2_no_other_PPN_channels",
            "missing_item": "no-other-channel theorem or no-cancellation envelope",
            "needed_for": "avoid hiding beta, source, endpoint, preferred-frame, or connection leaks behind gamma-only fit",
            "current_status": "MISSING_CHANNEL_CLOSURE",
            "next_action": "derive beta/preferred-frame/source endpoint silence, or score full residual vector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gap_id": "GAP1881_3_parent_action_clause",
            "missing_item": "terminal public coframe/no-shadow parent action clause",
            "needed_for": "turn empirical kernel route back into a clean GR-reduction theorem",
            "current_status": "NOT_FOUND_PARENT_SIGNED",
            "next_action": "write exact action-domain contract for S_matter and test C_R/J_q exclusion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gap_id": "GAP1881_4_R10_finite_inputs",
            "missing_item": "Z_R, M_R^2, lambda_R, source/test couplings and real bound curve",
            "needed_for": "short-range R10 scoring",
            "current_status": "HELD_BY_WRONG_ROUTE_GUARD",
            "next_action": "do not use common-frame massless kernel as alpha(lambda); return to finite operator acquisition later",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1881_0_ppn_gamma_kernel_smoke",
            "runner": "future b_R/x_U to Cassini gamma comparison",
            "current_status": "REFUSE_CLAIM_RUN",
            "reason": "first response kernel exists but b_R, x_U profile, beta/source/endpoint channels and no-cancellation theorem are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1881_1_local_residual_vector",
            "runner": "future PPN/WEP/clock/orbital residual vector scorer",
            "current_status": "REFUSE_CLAIM_RUN",
            "reason": "only gamma branch has a conditional kernel; d_R,w_R,endpoint, WEP/composition and orbital kernels are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1881_2_R10_alpha_lambda",
            "runner": "future R10 alpha(lambda) scorer",
            "current_status": "REFUSE_CLAIM_RUN_WRONG_ROUTE_GUARD",
            "reason": "finite Z_R/M_R^2/lambda/source/test/tau rows and real curve are still required before source-leg terms can enter R10",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1881_0_internal_kernel",
            "claim": "1881 may use the conformal b_R/x_U to PPN gamma response kernel internally",
            "status": "ALLOW_INTERNAL_NONCLAIM_KERNEL",
            "reason": "the mapping and Cassini bridge are source-backed, but not an MTS prediction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1881_1_ppn_score",
            "claim": "MTS passes Cassini/PPN gamma",
            "status": "BLOCKED",
            "reason": "b_R, x_U profile and no-other-channel theorem are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1881_2_no_shadow_zero",
            "claim": "b_R=d_R=w_R=epsilon_endpoint_R=0 by parent action",
            "status": "BLOCKED",
            "reason": "parent action no-shadow clause is not derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1881_3_local_GR",
            "claim": "local GR/Newton is recovered from the local branch",
            "status": "BLOCKED",
            "reason": "gamma kernel alone is not a GR-reduction theorem; beta, conservation, source, preferred-frame and endpoint closure remain open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1881_0_parent_clause",
            "decision": "PARENT_ACTION_NO_SHADOW_CLAUSE_NOT_DERIVED",
            "basis": "1880/1030 source trail contains exact conditional contracts but not a parent-signed action-domain exclusion",
            "consequence": "zero route remains a target, not a claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1881_1_first_kernel",
            "decision": "FIRST_COMMON_FRAME_PPN_GAMMA_RESPONSE_KERNEL_STAGED",
            "basis": "1741 conformal response map plus Cassini bound bridges b_R x_U to gamma_minus_1",
            "consequence": "the local branch now has a concrete empirical handle: |b_R x_U| must sit below the Cassini gamma target unless zero-derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1881_2_no_score",
            "decision": "NO_NUMERIC_PPN_OR_LOCAL_GR_CLAIM",
            "basis": "coefficient, profile normalization, no-other-channel theorem and full residual vector are missing",
            "consequence": "runners must refuse claim scoring",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1881_3_next",
            "decision": "SIGMAR_PROFILE_OR_NO_SHADOW_ACTION_CONTRACT_SELECTED_NEXT",
            "basis": "the first kernel shifts the missing object from vague local bounds to the exact product s_R=b_R x_U",
            "consequence": "1882 should derive x_U from C_R/source normalization or close the parent action no-shadow clause",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1881_0_primary",
            "target_doc": "1882-Y5-R2FR-sigmaR-profile-coefficient-from-CR-source-normalization-or-no-shadow-action-contract.md",
            "target_script": "scripts/Y5_R2FR_sigmaR_profile_coefficient_from_CR_source_normalization_or_no_shadow_action_contract_1882.py",
            "objective": "derive s_R=b_R x_U from C_R=ln(T^2 S), weak-field/source normalization and public coframe ownership, or prove the parent action no-shadow clause that sets b_R=d_R=w_R=0.",
            "selection_status": "selected",
            "success_condition": "x_U profile coefficient plus no-other-channel ledger, or a parent-signed no-shadow action clause; no PPN/local-GR claim without both coefficient and channel closure.",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1881_1_secondary",
            "target_doc": "1882b-Y5-R2FR-full-local-residual-vector-bound-runner-dryrun.md",
            "target_script": "scripts/Y5_R2FR_full_local_residual_vector_bound_runner_dryrun_1882b.py",
            "objective": "turn b_R,d_R,w_R,endpoint gap rows into a dry-run residual-vector scorer with all current rows blocked.",
            "selection_status": "held_secondary",
            "success_condition": "schema-ready local vector runner that refuses claims until coefficients/kernels/bounds are sourced.",
            "valid_for_claim": False,
        },
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status_id": "STATUS1881_0_big_picture",
            "plain_english": "The local-GR route is alive but still unproved; the strongest current object is a conditional PPN gamma kernel, not a completed GR reduction.",
            "technical_state": "C_R/R_AB coframe shadow can now be projected as s_R=b_R x_U into gamma_minus_1, but b_R/x_U/channel closure are missing",
            "risk_level": "SERIOUS_BUT_USEFUL",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status_id": "STATUS1881_1_good_news",
            "plain_english": "We have turned the vague coupling problem into a sharp target product: |b_R x_U| is bounded by Cassini gamma at about 1.15e-5 under the stated branch assumptions.",
            "technical_state": "first response kernel row RKR1881_0 and bridge PGB1881_0 exist",
            "risk_level": "ACTIONABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status_id": "STATUS1881_2_missing",
            "plain_english": "The missing heart is still the coupling/action-domain ownership: either prove the shadow frame is impossible, or derive its coefficient and profile.",
            "technical_state": "parent no-shadow clause unsigned; b_R, x_U, beta/preferred-frame/source/endpoint channels missing",
            "risk_level": "MAIN_BOTTLENECK",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def all_output_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "parent_clause_audit": parent_clause_audit_rows(),
        "response_kernels": response_kernel_rows(),
        "ppn_gamma_bridge": ppn_gamma_bridge_rows(),
        "gap_ledger": gap_ledger_rows(),
        "runner_refusal": runner_refusal_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }


def copy_branch_artifacts() -> None:
    shutil.copy2(OUTPUTS["response_kernels"], MICROSCOPE_RESIDUALS / OUTPUTS["response_kernels"].name)
    shutil.copy2(OUTPUTS["gap_ledger"], QUARANTINE / OUTPUTS["gap_ledger"].name)
    shutil.copy2(OUTPUTS["response_kernels"], QUEUE / "JR1881_COMMON_FRAME_RESPONSE_KERNEL_ROWS_NONCLAIM.csv")
    shutil.copy2(OUTPUTS["gap_ledger"], QUEUE / "JR1881_SIGMAR_PROFILE_GAP_LEDGER_NONCLAIM.csv")


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
    for path in paths:
        for row in csv_rows(path):
            joined = " ".join(str(value) for value in row.values())
            if "MISSING_" not in joined and "NOT_FOUND" not in joined and "UNSIGNED" not in joined:
                continue
            checked += 1
            for key in ("valid_for_claim", "claim_allowed", "score_ready", "prediction_ready", "numeric_kernel_ready", "proof_closed"):
                if key in row and bool_string(row[key]) == "true":
                    offenders.append(f"{path.name}:{row}")
                    break
    if offenders:
        return False, ";".join(offenders[:5])
    return True, f"checked_missing_or_unsigned_rows={checked}"


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
            "validation_id": "VAL1881_0_sources",
            "status": "PASS" if all(row["needle_check"] == "OK" for row in sources) else "FAIL",
            "detail": "1880/1741/local-bound/1030 sources available and needle-checked",
            "valid_for_claim": False,
        }
    )

    parent = rows_by_name["parent_clause_audit"]
    checks.append(
        {
            "validation_id": "VAL1881_1_parent_clause_unsigned",
            "status": "PASS"
            if any(row["current_status"] == "PARENT_ACTION_NO_SHADOW_CLAUSE_NOT_DERIVED" for row in parent)
            and all(bool_string(row["proof_closed"]) == "false" for row in parent)
            else "FAIL",
            "detail": "parent action no-shadow clause remains unsigned, not promoted",
            "valid_for_claim": False,
        }
    )

    kernels = rows_by_name["response_kernels"]
    first_kernel = [row for row in kernels if row["kernel_id"] == "RKR1881_0_C_R_conformal_PPN_gamma"]
    checks.append(
        {
            "validation_id": "VAL1881_2_first_kernel_staged",
            "status": "PASS"
            if first_kernel
            and first_kernel[0]["source_backed_kernel"] == "True"
            and first_kernel[0]["current_status"] == "SOURCE_BACKED_CONDITIONAL_KERNEL_STAGED_NONCLAIM"
            else "FAIL",
            "detail": "first common-frame PPN gamma response kernel row staged",
            "valid_for_claim": False,
        }
    )

    bridge = rows_by_name["ppn_gamma_bridge"]
    checks.append(
        {
            "validation_id": "VAL1881_3_ppn_bridge",
            "status": "PASS"
            if len(bridge) == 1
            and bridge[0]["row_id"] == "R3_gamma"
            and bridge[0]["upper_bound"] == "2.3e-05"
            and bridge[0]["bridge_status"] == "SOURCE_BACKED_CONDITIONAL_NONCLAIM"
            else "FAIL",
            "detail": "Cassini gamma bridge translated to s_R=b_R x_U target",
            "valid_for_claim": False,
        }
    )

    gaps = rows_by_name["gap_ledger"]
    checks.append(
        {
            "validation_id": "VAL1881_4_gap_ledger",
            "status": "PASS"
            if len(gaps) >= 5
            and any(row["gap_id"] == "GAP1881_1_xU_profile" for row in gaps)
            and all(bool_string(row["valid_for_claim"]) == "false" for row in gaps)
            else "FAIL",
            "detail": "b_R, x_U, channel-closure, parent-clause and R10 gaps remain explicit",
            "valid_for_claim": False,
        }
    )

    runners = rows_by_name["runner_refusal"]
    checks.append(
        {
            "validation_id": "VAL1881_5_runner_refusal",
            "status": "PASS" if all(row["current_status"].startswith("REFUSE_CLAIM_RUN") for row in runners) else "FAIL",
            "detail": "PPN/local/R10 runners refuse claim runs",
            "valid_for_claim": False,
        }
    )

    claims = rows_by_name["claim_gate"]
    checks.append(
        {
            "validation_id": "VAL1881_6_claim_gate",
            "status": "PASS"
            if any(row["status"] == "ALLOW_INTERNAL_NONCLAIM_KERNEL" for row in claims)
            and all(bool_string(row["claim_allowed"]) == "false" for row in claims)
            else "FAIL",
            "detail": "only internal nonclaim kernel use is allowed",
            "valid_for_claim": False,
        }
    )

    decisions = rows_by_name["decision"]
    checks.append(
        {
            "validation_id": "VAL1881_7_decision",
            "status": "PASS"
            if any(row["decision"] == "FIRST_COMMON_FRAME_PPN_GAMMA_RESPONSE_KERNEL_STAGED" for row in decisions)
            and any(row["decision"] == "SIGMAR_PROFILE_OR_NO_SHADOW_ACTION_CONTRACT_SELECTED_NEXT" for row in decisions)
            else "FAIL",
            "detail": "decision selects sigma_R profile or parent no-shadow action contract next",
            "valid_for_claim": False,
        }
    )

    next_targets = rows_by_name["next_target"]
    checks.append(
        {
            "validation_id": "VAL1881_8_next_target",
            "status": "PASS"
            if any(row["route_id"] == "NEXT1881_0_primary" and row["selection_status"] == "selected" for row in next_targets)
            else "FAIL",
            "detail": "1882 sigma_R/profile or no-shadow action contract target selected",
            "valid_for_claim": False,
        }
    )

    status_rows = rows_by_name["project_status"]
    checks.append(
        {
            "validation_id": "VAL1881_9_project_status",
            "status": "PASS"
            if len(status_rows) == 3
            and any(row["risk_level"] == "MAIN_BOTTLENECK" for row in status_rows)
            else "FAIL",
            "detail": "project status snapshot records good news, missing heart, and risk level",
            "valid_for_claim": False,
        }
    )

    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1881_10_claim_flags_false",
            "status": "PASS" if flags_ok else "FAIL",
            "detail": flags_detail,
            "valid_for_claim": False,
        }
    )

    missing_ok, missing_detail = missing_rows_not_ready(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1881_11_missing_not_ready",
            "status": "PASS" if missing_ok else "FAIL",
            "detail": missing_detail,
            "valid_for_claim": False,
        }
    )

    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1881_12_csv_parse",
            "status": "PASS" if parse_ok else "FAIL",
            "detail": parse_detail,
            "valid_for_claim": False,
        }
    )

    copied_paths = [
        MICROSCOPE_RESIDUALS / OUTPUTS["response_kernels"].name,
        QUARANTINE / OUTPUTS["gap_ledger"].name,
        QUEUE / "JR1881_COMMON_FRAME_RESPONSE_KERNEL_ROWS_NONCLAIM.csv",
        QUEUE / "JR1881_SIGMAR_PROFILE_GAP_LEDGER_NONCLAIM.csv",
    ]
    checks.append(
        {
            "validation_id": "VAL1881_13_branch_copies",
            "status": "PASS" if all(path.exists() for path in copied_paths) else "FAIL",
            "detail": ";".join(str(path) for path in copied_paths),
            "valid_for_claim": False,
        }
    )

    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append(
        {
            "validation_id": "VAL1881_14_pycache_absent",
            "status": "PASS" if not pycache.exists() else "FAIL",
            "detail": str(pycache),
            "valid_for_claim": False,
        }
    )

    formalization_hits = list(FORMALIZATION.rglob("*1881*")) if FORMALIZATION.exists() else []
    checks.append(
        {
            "validation_id": "VAL1881_15_formalization_untouched",
            "status": "PASS" if not formalization_hits else "FAIL",
            "detail": f"formalization_1881_count={len(formalization_hits)}",
            "valid_for_claim": False,
        }
    )

    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append(
        {
            "validation_id": "VAL1881_OVERALL",
            "status": "PASS" if fail_count == 0 else "FAIL",
            "detail": "1881 first common-frame response kernel or parent action clause",
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
    content = f"""# 1881 - First Common-Frame Response Kernel Or Parent Action Clause

**Private status:** nonclaim derivation/projection checkpoint.

## Result

The parent no-shadow action clause was **not** found in the current source trail. That keeps the clean zero route alive, but unsigned.

The useful counter-punch is that the local branch now has one concrete response-kernel row:

```text
g_obs = exp(2 sigma_R) g_GR
sigma_R = s_R U/c^2
s_R = b_R x_U
gamma_eff = (1+s_R)/(1-s_R)
gamma_minus_1 = 2 s_R/(1-s_R)
```

Using the Cassini gamma bound, this gives the conditional target

```text
|b_R x_U| = |s_R| <= 1.14998677515e-05
```

under the stated branch assumptions. This is **not** an MTS PPN claim because `b_R`, the `x_U` weak-field/source profile, source normalization, beta/preferred-frame/source/endpoint channels, and the no-cancellation theorem are still missing.

## Parent Action Clause Audit

{markdown_table(rows_by_name["parent_clause_audit"])}

## Common-Frame Response Kernels

{markdown_table(rows_by_name["response_kernels"])}

## PPN Gamma Bridge

{markdown_table(rows_by_name["ppn_gamma_bridge"])}

## Sigma_R Profile Gap Ledger

{markdown_table(rows_by_name["gap_ledger"])}

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
