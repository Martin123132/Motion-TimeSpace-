import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3803"
BRANCH = "MTS_R2FR_Y5_QX_SAME_SOURCE_NO_EXTRA_FORCE_OR_EPSILON_SOURCE_XQ_BOUND_3803"
ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main"
)
PCW = ROOT / "post-checkpoint-work"
FWB = ROOT / "formalization-workbench"
RESIDUALS = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3803-Y5-R2FR-qX-same-source-no-extra-force-closure-or-epsilon-sourceXQ-bound.md"
SCRIPT_PATH = PCW / "scripts" / "Y5_R2FR_3803_qX_same_source_no_extra_force_closure_or_epsilon_sourceXQ_bound.py"

P_3770 = PCW / "3770-Y5-R2FR-source-action-leak-zero-or-WEP-EM-PPN-bound.md"
P_3776 = PCW / "3776-Y5-R2FR-total-Hilbert-source-inclusion-EM-Poynting-and-interior-monopole-closure.md"
P_3784 = PCW / "3784-Y5-R2FR-parent-U1-action-clause-or-EM-finite-bound-mode.md"
P_3792 = PCW / "3792-Y5-R2FR-same-current-Ward-Hilbert-stress-owner-or-epsilonJ-bound.md"
P_3801 = PCW / "3801-Y5-R2FR-qobs-Qshear-spectral-ownership-or-selector-leakage-fill.md"
P_3802 = PCW / "3802-Y5-R2FR-parent-Qshear-spectral-action-clause-or-epsilonYV-bound.md"
P_SPINE = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

C_3801_CONTRACT = RESIDUALS / "P8_Y5_R2FR_3801_QOBS_XQ_OWNERSHIP_CONTRACT.csv"
C_3802_THEOREM = RESIDUALS / "P8_Y5_R2FR_3802_PARENT_QSHEAR_SPECTRAL_ACTION_THEOREM.csv"
C_3802_BOUND = RESIDUALS / "P8_Y5_R2FR_3802_EPSILON_YV_BOUND_FILL_ROWS.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3803_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_3803_QX_SOURCE_SAFETY_THEOREM.csv",
    "contract": RESIDUALS / "P8_Y5_R2FR_3803_NO_EXTRA_FORCE_CONTRACT.csv",
    "audit": RESIDUALS / "P8_Y5_R2FR_3803_CURRENT_CORPUS_SOURCE_SAFETY_AUDIT.csv",
    "bound_rows": RESIDUALS / "P8_Y5_R2FR_3803_EPSILON_SOURCE_XQ_BOUND_ROWS.csv",
    "arena_rows": RESIDUALS / "P8_Y5_R2FR_3803_ARENA_SOURCE_PROJECTION_ROWS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3803_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3803_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3803_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3803_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3803_VALIDATION.csv",
}

SOURCE_SPECS = [
    {
        "source_id": "SRC3803_0_3802_handoff",
        "path": P_3802,
        "needle": "source safety condition",
        "role": "3802 selected q_X source-safety/no-extra-force as the next gate",
    },
    {
        "source_id": "SRC3803_1_3801_qx_refinement",
        "path": P_3801,
        "needle": "q_X=(q_obs,X_Q)",
        "role": "exact quotient-refinement identity and no-free-lunch rule",
    },
    {
        "source_id": "SRC3803_2_3792_same_current",
        "path": P_3792,
        "needle": "Assume S_src=S_charged[psi,g_obs,A_Q,theta]+S_EM",
        "role": "same-current Ward/Hilbert theorem used to internalize Lorentz exchange",
    },
    {
        "source_id": "SRC3803_3_3770_source_leak",
        "path": P_3770,
        "needle": "J_A^src := delta S_src/dzeta^A",
        "role": "source-action leak definition and WEP/PPN bound interface",
    },
    {
        "source_id": "SRC3803_4_3776_total_hilbert",
        "path": P_3776,
        "needle": "The Poynting vector and field momentum are part of T_EM",
        "role": "total Hilbert source inclusion rule for EM/Poynting/binding stresses",
    },
    {
        "source_id": "SRC3803_5_3784_U1_action",
        "path": P_3784,
        "needle": "S_U1=int sqrt(-g_eff)",
        "role": "parent U1 action grammar and B_Q owner slot",
    },
    {
        "source_id": "SRC3803_6_3801_contract",
        "path": C_3801_CONTRACT,
        "needle": "QXC3801_5_same_source_EM",
        "role": "q_X ownership contract inherited from 3801",
    },
    {
        "source_id": "SRC3803_7_3802_theorem",
        "path": C_3802_THEOREM,
        "needle": "QSA3802_4_same_source_no_force_condition",
        "role": "3802 source-safety theorem row",
    },
    {
        "source_id": "SRC3803_8_3802_bound",
        "path": C_3802_BOUND,
        "needle": "EYB3802_6_epsilon_source_XQ",
        "role": "epsilon_source_XQ inherited finite-row slot",
    },
    {
        "source_id": "SRC3803_9_spine",
        "path": P_SPINE,
        "needle": "source-safety blocker",
        "role": "live spine target for this checkpoint",
    },
]


def read_text(path):
    return path.read_text(encoding="utf-8", errors="replace")


def load_csv(path):
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path):
    try:
        load_csv(path)
        return True
    except Exception:
        return False


def bool_text(value):
    return "true" if value else "false"


def source_register(timestamp):
    rows = []
    for spec in SOURCE_SPECS:
        exists = spec["path"].exists()
        needle_found = False
        if exists:
            needle_found = spec["needle"] in read_text(spec["path"])
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "source_id": spec["source_id"],
                "source_path": str(spec["path"]),
                "exists": bool_text(exists),
                "needle": spec["needle"],
                "needle_found": bool_text(needle_found),
                "role": spec["role"],
                "valid_for_claim": "false",
            }
        )
    return rows


def theorem_rows(timestamp):
    specs = [
        (
            "QXS3803_0_source_safety_setup",
            "q_X source-safety object language",
            "Work with q_X=(q_obs,X_Q), Y_Q=Pi4(X_Q), and a source action S_src=S_vis[psi,g_obs,A_Q[B_Q(Y_Q)],theta]+S_Qspec[X_Q,Y_Q,lambda_X,lambda_Y]+S_tail. Define the direct X_Q source force as J_XQ_dir := (1/sqrt(-g_obs)) partial S_src/partial X_Q at fixed g_obs,A_Q,B_Q,Y_Q,psi,theta, so it excludes the declared EM response path and isolates hidden matter/source-normalization dependence.",
            "DEFINITION_AND_VARIATIONAL_SPLIT",
            "The dangerous quantity is not q_X itself; it is direct non-EM dependence on X_Q after the EM/B_Q channel is held fixed.",
            "strict corpus has not supplied this fixed-variable exclusion certificate",
        ),
        (
            "QXS3803_1_direct_derivative_zero",
            "no independent X_Q matter force",
            "If partial L_matter/partial X_Q=0, partial L_binding/partial X_Q=0, partial L_apparatus/partial X_Q=0, partial L_int/partial X_Q=0, partial L_source_norm/partial X_Q=0, and partial theta_I/partial X_Q=0 at fixed q_obs,A_Q,B_Q,Y_Q, then J_XQ_dir=0 by the ordinary chain rule.",
            "EXACT_CONDITIONAL_CHAIN_RULE_ZERO",
            "Q-shear spectral ownership does not act as a fifth force or source-normalization dial outside the declared EM/Hilbert sector.",
            "no parent source grammar currently signs all direct X_Q derivatives zero",
        ),
        (
            "QXS3803_2_same_source_internal_exchange",
            "EM response is internal exchange, not extra force",
            "If the X_Q dependence enters visible matter only through Y_Q, B_Q[Y_Q], and A_Q inside one descended S_src, and J_Q^a=(1/sqrt(-g_obs))delta S_src/delta A_Qa is the same current that sources Maxwell, then the FJ terms in div(T_EM) and div(T_charged+T_binding) cancel inside div(T_total).",
            "EXACT_CONDITIONAL_WARD_HILBERT_IMPORT_FROM_3792",
            "The allowed B_Q/EM path can be kept inside one total Hilbert stress rather than becoming an unbooked fifth-force channel.",
            "same-current, B_Q owner, Z_EM/lambda, and total-domain clauses remain unsigned",
        ),
        (
            "QXS3803_3_Qspec_stress_guard",
            "Qspec constraint stress inclusion",
            "The constraint sector L_Qspec=lambda_X.(X_Q-Spec(S[Q]))+lambda_Y.(Y_Q-Pi4(X_Q))+L_degen+L_domain is source-safe only if its metric/coframe variation is included in the same total Hilbert source, is projected silent on the local arena, or is bounded as epsilon_Qspec_stress.",
            "REQUIRED_HILBERT_STRESS_GUARD",
            "The Qspec owner clause cannot be hidden outside the stress tensor while still claiming local GR.",
            "no parent-signed Qspec Hilbert-stress inclusion or projection-silence certificate exists",
        ),
        (
            "QXS3803_4_qX_no_extra_force_zero_theorem",
            "q_X no-extra-force theorem",
            "If QXS3803_1 direct derivatives vanish, QXS3803_2 same-source EM/Hilbert ownership holds, QXS3803_3 Qspec stress is included or silent, and theta/kappa/shadow/Z_EM/current/boundary/domain companions are zero or q_X-owned, then epsilon_source_XQ=0 and the q_X refinement adds no independent local source force.",
            "EXACT_CONDITIONAL_ZERO_THEOREM",
            "The 3801/3802 q_X route becomes locally source-safe as a parent extension rather than a hidden coupling insertion.",
            "all companion clauses are contract-level, not strict-current signatures",
        ),
        (
            "QXS3803_5_finite_force_bound",
            "epsilon_source_XQ finite branch",
            "If the zero theorem is not signed, keep epsilon_XQ_force_abs = epsilon_source_XQ + epsilon_theta_XQ + epsilon_kappa_XQ + epsilon_shadow_XQ + epsilon_Qspec_stress + epsilon_boundary_XQ + epsilon_domain_XQ + epsilon_ZEM_XQ + epsilon_J_Q and N_qX_local_abs = N_Qspec_local_abs + epsilon_XQ_force_abs.",
            "DERIVED_ABS_SUM_BOUND_BRANCH",
            "A failure to prove no-extra-force becomes a named local residual vector feeding WEP/PPN/R10/clock/orbital rows.",
            "numeric/theorem-zero values for every component are missing",
        ),
        (
            "QXS3803_6_counterexample_guard",
            "why the clause is necessary",
            "A legal-looking term f(X_Q)L_matter, m_A(X_Q) psi_bar psi, Z_EM(X_Q)F^2, kappa(X_Q)R, or boundary weight D(X_Q) can preserve the q_X quotient identity while changing active source strength, composition response, alpha, PPN, or clocks. Therefore q_X kernel closure alone is insufficient.",
            "NO_SMUGGLE_COUNTEREXAMPLE",
            "This prevents us from celebrating Hperp basicness while accidentally introducing a source coupling through the back door.",
            "strict corpus must exclude these terms or bound their amplitudes",
        ),
    ]
    rows = []
    for theorem_id, claim_piece, mathematical_form, derivation_status, result_if_signed, missing in specs:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "theorem_id": theorem_id,
                "claim_piece": claim_piece,
                "mathematical_form": mathematical_form,
                "derivation_status": derivation_status,
                "result_if_signed": result_if_signed,
                "missing_for_current_claim": missing,
                "valid_for_claim": "false",
            }
        )
    return rows


def contract_rows(timestamp):
    specs = [
        (
            "NEF3803_0_qX_parent_selection",
            "q_X parent quotient selection",
            "q_X=(q_obs,X_Q) is declared by the parent object language before EM/data readout and projects back to q_obs.",
            "MISSING_QX_PARENT_QUOTIENT_SIGNATURE",
        ),
        (
            "NEF3803_1_direct_matter_derivatives",
            "no direct visible-matter X_Q argument",
            "partial L_matter/partial X_Q=partial L_binding/partial X_Q=partial L_apparatus/partial X_Q=partial L_int/partial X_Q=0 at fixed q_obs,A_Q,B_Q,Y_Q,psi,theta.",
            "MISSING_NO_DIRECT_XQ_MATTER_FORCE_CERTIFICATE",
        ),
        (
            "NEF3803_2_XQ_only_through_BQ",
            "allowed X_Q path only through B_Q",
            "Visible X_Q dependence appears only as X_Q->Y_Q=Pi4(X_Q)->B_Q[Y_Q]->A_Q,F_Q inside the declared EM sector.",
            "MISSING_BQ_ONLY_PATH_CERTIFICATE",
        ),
        (
            "NEF3803_3_same_source_hilbert",
            "same source/current/stress owner",
            "J_Q, charged matter, Maxwell stress, binding, apparatus, interactions, and EM/Poynting domain terms are varied inside one descended total source action.",
            "MISSING_QX_SAME_SOURCE_HILBERT_SIGNATURE",
        ),
        (
            "NEF3803_4_Qspec_stress",
            "Qspec Hilbert stress inclusion or silence",
            "The metric/coframe variation of L_Qspec is either part of T_total, projected silent in the local arena, or bounded as epsilon_Qspec_stress.",
            "MISSING_QSPEC_STRESS_INCLUSION_OR_BOUND",
        ),
        (
            "NEF3803_5_theta_source_markers",
            "theta/source markers silent under X_Q",
            "Masses, material labels, clock markers, binding fractions, charge labels, and source normalization are q_X-owned/superselected or bounded.",
            "MISSING_THETA_XQ_SILENCE_CERTIFICATE",
        ),
        (
            "NEF3803_6_kappa_shadow_frame",
            "no kappa or shadow-frame X_Q leak",
            "kappa_eff, sector frames, local coframe, and source metric have no independent X_Q dependence outside q_obs or bounded residual rows.",
            "MISSING_KAPPA_SHADOW_XQ_CERTIFICATE",
        ),
        (
            "NEF3803_7_ZEM_current_calibration",
            "Z_EM/current/calibration companions",
            "q_*, Z_EM, lambda_A, beta_Z,A, and epsilon_J_Q are zeroed or bounded under the same q_X branch.",
            "MISSING_QX_CALIBRATION_COMPANIONS",
        ),
        (
            "NEF3803_8_boundary_domain",
            "boundary/domain silence",
            "Qspec constraints, B_Q/EM fields, Poynting tails, and total-source support have no unbooked boundary/domain flux under q_X.",
            "MISSING_BOUNDARY_DOMAIN_XQ_CERTIFICATE",
        ),
        (
            "NEF3803_9_no_postfit_source_path",
            "no data-fitted source path",
            "No X_Q-dependent coefficient is chosen from R10, PPN, clock, orbital, or alpha data before the parent action fixes the source grammar.",
            "MISSING_NONCIRCULAR_SOURCE_COEFFICIENT_PROOF",
        ),
    ]
    rows = []
    for clause_id, clause, requirement, current_status in specs:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "clause_id": clause_id,
                "clause": clause,
                "requirement": requirement,
                "current_status": current_status,
                "valid_for_claim": "false",
                "blocks_claim": "true",
            }
        )
    return rows


def audit_rows(timestamp):
    specs = [
        (
            "AUD3803_0_qX_identity",
            "q_X kernel identity",
            "3801 proves ker(Dq_X)=ker(Dq_obs) cap ker(DX_Q), so q_X verticals cannot move X_Q.",
            "EXACT_CONDITIONAL",
            "does not by itself exclude direct source couplings to X_Q",
        ),
        (
            "AUD3803_1_Qspec_action",
            "Qspec action grammar",
            "3802 writes L_Qspec and the spectral-projector repair as a coherent parent extension.",
            "ACTION_GRAMMAR_WRITTEN_NOT_STRICT_CURRENT",
            "strict corpus still lacks parent signatures for Qspec/Pi4/q_X",
        ),
        (
            "AUD3803_2_same_current",
            "same-current theorem shape",
            "3792 supplies the exact one-action Ward/Hilbert theorem that would internalize Lorentz exchange.",
            "EXACT_CONDITIONAL_ONLY",
            "one descended total q_X source action is not parent-signed",
        ),
        (
            "AUD3803_3_source_descent",
            "source-action descent",
            "3770 proves source-current zero if S_src descends and markers are silent.",
            "THEOREM_EXISTS_BUT_UNSIGNED",
            "source descent and marker silence are not signed for X_Q",
        ),
        (
            "AUD3803_4_total_hilbert_domain",
            "total Hilbert/Poynting inclusion",
            "3776 shows EM/Poynting/binding stresses must be included in M_H,total or kept as explicit residuals.",
            "CONDITIONAL_SOURCE_DISCIPLINE",
            "Qspec/B_Q field support and boundary tails are not closed",
        ),
        (
            "AUD3803_5_BQ_U1_owner",
            "B_Q/U1 owner",
            "3784 writes a parent U1 action but keeps B_Q, Z_EM, lambda_A, q_*, and current ownership open.",
            "PARENT_EXTENSION_MODE",
            "B_Q-only path and calibration companions remain unsigned",
        ),
        (
            "AUD3803_6_direct_XQ_force",
            "direct X_Q force certificate",
            "No inspected strict source row supplies partial L_matter/partial X_Q=0 and companion derivative-zero clauses.",
            "FAIL_CURRENT_ZERO_CLAIM",
            "epsilon_source_XQ must remain live",
        ),
        (
            "AUD3803_7_bound_branch",
            "finite epsilon_source_XQ branch",
            "3801/3802 already named epsilon_source_XQ; 3803 expands it into arena projection rows.",
            "BOUND_FORM_READY_VALUES_MISSING",
            "no local-GR, R10, PPN, clock, WEP, or orbital claim",
        ),
    ]
    rows = []
    for audit_id, item, current_evidence, status, missing in specs:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "audit_id": audit_id,
                "item": item,
                "current_evidence": current_evidence,
                "status": status,
                "missing_for_claim": missing,
                "valid_for_claim": "false",
            }
        )
    return rows


def bound_rows(timestamp):
    specs = [
        (
            "ESX3803_0_epsilon_source_XQ",
            "epsilon_source_XQ",
            "sup_U ||P_nonEM delta S_src/delta X_Q||/S_ref at fixed q_obs,A_Q,B_Q,Y_Q,psi,theta",
            "dimensionless",
            "MISSING_NO_DIRECT_XQ_MATTER_FORCE_CERTIFICATE",
            "theorem-zero direct matter/source derivative or numeric bound",
            "WEP;PPN;R10;clock;orbital",
        ),
        (
            "ESX3803_1_epsilon_theta_XQ",
            "epsilon_theta_XQ",
            "normalized X_Q derivative of masses/material labels/clock markers/binding fractions/source-normalization theta_I",
            "dimensionless",
            "MISSING_THETA_XQ_SILENCE_CERTIFICATE",
            "theta superselection/q_X ownership proof or finite marker sensitivities",
            "WEP;clock;R10;Newton_source",
        ),
        (
            "ESX3803_2_epsilon_kappa_XQ",
            "epsilon_kappa_XQ",
            "|partial_XQ ln kappa_eff| times local X_Q amplitude/rate envelope",
            "dimensionless",
            "MISSING_KAPPA_XQ_OWNER",
            "kappa q_X ownership/superselection or source-backed derivative bound",
            "Gdot;PPN;orbital",
        ),
        (
            "ESX3803_3_epsilon_shadow_XQ",
            "epsilon_shadow_XQ",
            "norm of sector metric/coframe/frame dependence on X_Q outside q_obs",
            "dimensionless",
            "MISSING_SHADOW_FRAME_XQ_BOUND",
            "one-frame theorem under q_X or finite frame projection coefficient",
            "PPN;clock;preferred_frame",
        ),
        (
            "ESX3803_4_epsilon_Qspec_stress",
            "epsilon_Qspec_stress",
            "normalized Hilbert/coframe stress contribution of L_Qspec not included in T_total or projected silent",
            "dimensionless",
            "MISSING_QSPEC_STRESS_INCLUSION_OR_BOUND",
            "include Qspec stress in total source, prove projection silence, or source bound",
            "PPN;Newton;orbital;WEP",
        ),
        (
            "ESX3803_5_epsilon_boundary_XQ",
            "epsilon_boundary_XQ",
            "normalized boundary/corner/edge flux from Qspec, B_Q, EM/Poynting, or source domain under q_X",
            "dimensionless",
            "MISSING_QX_BOUNDARY_FLUX_CERTIFICATE",
            "compact support/no-flux proof or finite boundary source row",
            "R10;orbital;Newton;clock",
        ),
        (
            "ESX3803_6_epsilon_domain_XQ",
            "epsilon_domain_XQ",
            "normalized mismatch between q_X source domain and total Hilbert/Poynting field support",
            "dimensionless",
            "MISSING_QX_TOTAL_DOMAIN_CERTIFICATE",
            "total-system domain proof or tail/domain bound",
            "Newton;orbital;PPN;WEP",
        ),
        (
            "ESX3803_7_epsilon_ZEM_XQ",
            "epsilon_ZEM_XQ",
            "|partial_XQ ln Z_EM| plus hidden X_Q-dependent F^2 operator coefficient lambda_XQ",
            "dimensionless",
            "MISSING_ZEM_LAMBDA_XQ_CERTIFICATE",
            "Z_EM q_X ownership/no-independent-F2 proof or alpha/clock bound row",
            "R10;clock;WEP;PPN",
        ),
        (
            "ESX3803_8_epsilon_J_Q",
            "epsilon_J_Q",
            "same-current residual vector from 3792 under the q_X branch",
            "dimensionless",
            "MISSING_QX_SAME_CURRENT_CERTIFICATE",
            "one descended total source action and Ward/Hilbert proof under q_X",
            "WEP;PPN;Newton;R10;clock",
        ),
        (
            "ESX3803_9_epsilon_XQ_force_abs",
            "epsilon_XQ_force_abs",
            "epsilon_source_XQ + epsilon_theta_XQ + epsilon_kappa_XQ + epsilon_shadow_XQ + epsilon_Qspec_stress + epsilon_boundary_XQ + epsilon_domain_XQ + epsilon_ZEM_XQ + epsilon_J_Q",
            "dimensionless",
            "ABS_SUM_BOUND_READY_COMPONENTS_MISSING",
            "all component values theorem-zero or source-backed numeric",
            "local_GR_gate;WEP;PPN;R10;clock;orbital",
        ),
        (
            "ESX3803_10_N_qX_local_abs",
            "N_qX_local_abs",
            "N_Qspec_local_abs + epsilon_XQ_force_abs",
            "dimensionless",
            "LOCAL_QX_BOUND_READY_NUMERIC_INPUTS_MISSING",
            "Qspec selector rows plus source-force rows all filled",
            "local_GR_gate",
        ),
    ]
    rows = []
    for row_id, symbol, formula, units, current_value, required, feeds in specs:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "row_id": row_id,
                "symbol": symbol,
                "formula": formula,
                "units": units,
                "current_value": current_value,
                "required_source_or_zero": required,
                "feeds": feeds,
                "status": "REQUIRED_NOT_FILLED",
                "valid_for_claim": "false",
                "blocks_claim": "true",
            }
        )
    return rows


def arena_rows(timestamp):
    specs = [
        (
            "ARX3803_0_WEP",
            "eta_XQ_AB",
            "eta_XQ_AB <= C_XQ_WEP*epsilon_XQ_force_abs + C_theta*epsilon_theta_XQ + C_Z*epsilon_ZEM_XQ",
            "dimensionless",
            "2.8e-15",
            "WEP composition response",
        ),
        (
            "ARX3803_1_PPN_gamma",
            "delta_gamma_XQ",
            "delta_gamma_XQ <= C_XQ_gamma*epsilon_XQ_force_abs + C_shadow*epsilon_shadow_XQ + C_Qspec*epsilon_Qspec_stress",
            "dimensionless",
            "2.3e-05",
            "Cassini/PPN gamma",
        ),
        (
            "ARX3803_2_PPN_beta",
            "delta_beta_XQ",
            "delta_beta_XQ <= C_XQ_beta*epsilon_XQ_force_abs + C_kappa*epsilon_kappa_XQ + C_domain*epsilon_domain_XQ",
            "dimensionless",
            "7.8e-05",
            "PPN beta/self-coupling",
        ),
        (
            "ARX3803_3_R10",
            "alpha_R10_XQ(lambda)",
            "alpha_R10_XQ(lambda) <= C_R10_XQ(lambda)*epsilon_XQ_force_abs + C_Z(lambda)*epsilon_ZEM_XQ + C_boundary(lambda)*epsilon_boundary_XQ",
            "dimensionless",
            "requires sourced alpha_bound(lambda)",
            "short-range fifth-force/R10",
        ),
        (
            "ARX3803_4_clock",
            "b_clock_XQ",
            "|b_clock_XQ| <= C_clock_XQ*epsilon_XQ_force_abs + C_alpha*epsilon_ZEM_XQ + C_theta*epsilon_theta_XQ",
            "yr^-1_or_dimensionless_product",
            "requires clock sensitivity/product split",
            "clock drift/alpha sensitivity",
        ),
        (
            "ARX3803_5_orbital",
            "delta_mu_XQ",
            "|delta ln mu_obs|_XQ <= C_mu_XQ*epsilon_XQ_force_abs + C_domain*epsilon_domain_XQ + C_boundary*epsilon_boundary_XQ",
            "dimensionless",
            "requires Newton/orbital source denominator",
            "orbital GM/source calibration",
        ),
        (
            "ARX3803_6_Gdot",
            "dlnG_XQ_dt",
            "|d_t ln G_eff|_XQ <= |d_t epsilon_kappa_XQ| + |d_t epsilon_source_XQ| + |d_t epsilon_domain_XQ|",
            "yr^-1",
            "9.6e-15 yr^-1",
            "Gdot/local coupling drift",
        ),
    ]
    rows = []
    for arena_id, observable, formula, units, bound_reference, arena in specs:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "arena_id": arena_id,
                "observable": observable,
                "projection_formula": formula,
                "units": units,
                "bound_reference": bound_reference,
                "arena": arena,
                "coefficient_status": "MISSING_ARENA_PROJECTION_COEFFICIENTS",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        )
    return rows


def claim_gate_rows(timestamp, grouped):
    sources_ok = all(row["exists"] == "true" for row in grouped["sources"])
    needles_ok = all(row["needle_found"] == "true" for row in grouped["sources"])
    bound_nonclaim = all(row["valid_for_claim"] == "false" and row["blocks_claim"] == "true" for row in grouped["bound_rows"])
    arena_nonclaim = all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" for row in grouped["arena_rows"])
    specs = [
        (
            "CG3803_0_sources",
            sources_ok and needles_ok,
            "all source paths and needles found",
        ),
        (
            "CG3803_1_source_safety_theorem",
            True,
            "conditional q_X source-safety/no-extra-force theorem emitted",
        ),
        (
            "CG3803_2_direct_derivative_zero_signed",
            False,
            "strict corpus does not sign partial L_matter/partial X_Q=0 and companion direct derivative clauses",
        ),
        (
            "CG3803_3_same_source_qX_signed",
            False,
            "one descended q_X total source action and B_Q/Z_EM/current/domain clauses remain unsigned",
        ),
        (
            "CG3803_4_Qspec_stress_signed",
            False,
            "Qspec Hilbert stress is not yet included, projected silent, or source-bounded",
        ),
        (
            "CG3803_5_bound_rows_nonclaim",
            bound_nonclaim,
            "epsilon_source_XQ component rows emitted as blockers",
        ),
        (
            "CG3803_6_arena_rows_nonclaim",
            arena_nonclaim,
            "WEP/PPN/R10/clock/orbital/Gdot projection rows emitted without claims",
        ),
        (
            "CG3803_7_local_GR_claim",
            False,
            "q_X local-GR closure remains blocked until no-extra-force and calibration companions close",
        ),
    ]
    rows = []
    for gate_id, passed, details in specs:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "gate_id": gate_id,
                "pass": bool_text(passed),
                "claim_allowed": "false",
                "details": details,
                "valid_for_claim": "false",
            }
        )
    return rows


def decision_rows(timestamp):
    specs = [
        (
            "DEC3803_0_progress",
            "q_X source-safety has an exact conditional theorem now.",
            "The direct derivative split shows precisely when X_Q is harmless and when it becomes a source/fifth-force channel.",
            "Keep the theorem as a parent-extension contract, not a strict-current claim.",
        ),
        (
            "DEC3803_1_nonclaim",
            "No local-GR/R10/PPN/WEP/clock/orbital claim follows from 3803.",
            "The current corpus lacks direct X_Q derivative-zero clauses, q_X same-source action, Qspec stress inclusion, and calibration companions.",
            "Retain epsilon_XQ_force_abs and arena projection rows as blockers.",
        ),
        (
            "DEC3803_2_best_next",
            "The next target should attack q_X calibration companions and local-bound runner wiring together.",
            "Even if direct source force is later zeroed, q_*, Z_EM, lambda_A, epsilon_J_Q, boundary/domain, and Qspec stress can still leak into local tests.",
            "Move to 3804 qX calibration companion closure or local bound runner.",
        ),
    ]
    rows = []
    for decision_id, decision, rationale, action in specs:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "decision_id": decision_id,
                "decision": decision,
                "rationale": rationale,
                "action": action,
                "valid_for_claim": "false",
            }
        )
    return rows


def next_target_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "target_doc": "3804-Y5-R2FR-qX-calibration-companion-closure-or-local-bound-runner.md",
            "target_script": "scripts/Y5_R2FR_3804_qX_calibration_companion_closure_or_local_bound_runner.py",
            "objective": "Close or explicitly bound the q_X companion gates q_*, Z_EM, lambda_A, epsilon_J_Q, theta/source markers, Qspec stress, boundary/domain, and arena projection coefficients; then wire a local nonclaim bound runner for WEP/PPN/R10/clock/orbital.",
            "avoid": "do not treat q_X Hperp/source-safety as local GR while calibration and arena projection coefficients remain live",
            "valid_for_claim": "false",
        }
    ]


def status_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "status": "PASS_NONCLAIM_QX_SOURCE_SAFETY_THEOREM_AND_EPSILON_SOURCE_ROWS",
            "headline": "q_X source safety is reduced to direct X_Q derivative silence plus same-source EM/Hilbert ownership; strict corpus does not sign those clauses, so epsilon_XQ_force_abs remains live.",
            "claim_allowed": "false",
            "next_target": "3804 qX calibration companion closure or local bound runner",
        }
    ]


def validation_rows(timestamp, grouped):
    sources_ok = all(row["exists"] == "true" for row in grouped["sources"])
    needles_ok = all(row["needle_found"] == "true" for row in grouped["sources"])
    csv_ok = all(csv_parses(path) for key, path in OUTPUTS.items() if key != "validation")
    theorem_text = "\n".join(row["mathematical_form"] for row in grouped["theorem"])
    contract_text = "\n".join(row["requirement"] for row in grouped["contract"])
    bound_nonclaim = all(row["valid_for_claim"] == "false" and row["blocks_claim"] == "true" for row in grouped["bound_rows"])
    arena_nonclaim = all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" for row in grouped["arena_rows"])
    gates_closed = all(row["claim_allowed"] == "false" for row in grouped["gates"])
    fwb_patterns = ("*Y5_R2FR_3803*", "*3803-Y5*", "*P8_Y5*3803*")
    fwb_hits = []
    if FWB.exists():
        for pattern in fwb_patterns:
            fwb_hits.extend(FWB.rglob(pattern))
    fwb_clean = not fwb_hits
    pycache_clean = not (PCW / "scripts" / "__pycache__").exists()
    doc_text = read_text(DOC_PATH) if DOC_PATH.exists() else ""
    script_text = read_text(SCRIPT_PATH) if SCRIPT_PATH.exists() else ""
    mojibake_c2 = chr(0x00C2)
    replacement_char = chr(0xFFFD)
    bad_chars_clean = mojibake_c2 not in doc_text + script_text and replacement_char not in doc_text + script_text
    checks = [
        ("sources_exist", sources_ok, "every cited source path exists"),
        ("needles_found", needles_ok, "every cited source needle was found"),
        ("csv_outputs_parse", csv_ok, "all generated CSV outputs exist and parse"),
        ("doc_written", DOC_PATH.exists(), "3803 markdown document written"),
        (
            "direct_derivative_condition",
            "partial L_matter/partial X_Q=0" in theorem_text,
            "direct X_Q matter-force derivative condition emitted",
        ),
        (
            "same_source_internal_exchange",
            "FJ terms" in theorem_text and "cancel inside div(T_total)" in theorem_text,
            "same-source internal Lorentz exchange theorem imported",
        ),
        (
            "contract_complete",
            "Visible X_Q dependence appears only as X_Q->Y_Q=Pi4(X_Q)->B_Q[Y_Q]" in contract_text
            and "Qspec constraints" in contract_text,
            "no-extra-force contract includes B_Q path and Qspec stress/domain guards",
        ),
        ("bound_rows_nonclaim", bound_nonclaim, "all epsilon_source_XQ rows remain nonclaim blockers"),
        ("arena_rows_nonclaim", arena_nonclaim, "all arena projection rows remain nonclaim"),
        ("claims_closed", gates_closed, "no claim gate allows a claim"),
        ("formalization_clean", fwb_clean, "no 3803 files written under formalization-workbench"),
        ("pycache_removed", pycache_clean, "scripts __pycache__ removed"),
        ("bad_chars_clean", bad_chars_clean, "new doc/script contain no mojibake replacement characters"),
    ]
    rows = []
    for check_id, passed, detail in checks:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "check_id": check_id,
                "result": "PASS" if passed else "FAIL",
                "detail": detail,
            }
        )
    return rows


def row_bullet(row, key_fields):
    label = " ".join(f"`{row[field]}`" for field in key_fields if field in row and row[field])
    rest = "; ".join(
        f"{key}: {value}"
        for key, value in row.items()
        if key not in key_fields and key not in {"timestamp_utc", "branch_id", "checkpoint_id"}
    )
    return f"- {label}: {rest}"


def write_markdown(grouped):
    lines = [
        "# 3803 - qX Same-Source No-Extra-Force Closure or epsilon_source_XQ Bound",
        "",
        "## Status",
        "",
        "`PASS_NONCLAIM_QX_SOURCE_SAFETY_THEOREM_AND_EPSILON_SOURCE_ROWS`.",
        "",
        "3803 does the thing we actually needed after the Qspec doorway: it varies the q_X branch against the source side instead of only asking whether `Hperp` can be made basic. The result is sharp.",
        "",
        "The q_X route is source-safe only if the direct source derivative vanishes:",
        "",
        "`partial L_matter/partial X_Q=partial L_binding/partial X_Q=partial L_apparatus/partial X_Q=partial L_int/partial X_Q=partial L_source_norm/partial X_Q=0`",
        "",
        "at fixed `q_obs,A_Q,B_Q,Y_Q,psi,theta`, with any remaining X_Q dependence entering only through `Y_Q=Pi4(X_Q) -> B_Q[Y_Q] -> A_Q,F_Q` inside one same-source Hilbert action.",
        "",
        "If that package is signed, `epsilon_source_XQ=0` and the q_X refinement does not introduce an independent local force. The strict current corpus does not sign it yet, so the checkpoint keeps the finite vector `epsilon_XQ_force_abs` live and projects it into WEP/PPN/R10/clock/orbital/Gdot rows.",
        "",
        "## Result In Plain Terms",
        "",
        "This is progress, but not a victory lap. We now know the exact contract a future parent action has to satisfy: X_Q may own the EM geometry, but it must not also sneak into matter masses, source normalization, kappa, frames, Z_EM, or boundary/domain terms as an unbooked force.",
        "",
        "So the next route is no longer vague coupling-hunting. It is a concrete companion-gate attack: q_*, Z_EM, lambda_A, epsilon_J_Q, Qspec stress, theta/source markers, boundary/domain support, and arena projection coefficients.",
        "",
        "## Compact Result",
        "",
        "`q_X` kernel closure plus `Hperp` basicness is not enough by itself.",
        "",
        "`X_Q` is harmless only when its direct non-EM source derivative is zero or bounded.",
        "",
        "The allowed EM route must be same-source: Lorentz/Poynting exchange is internal to `T_total`, not a side force.",
        "",
        "`epsilon_XQ_force_abs` is now the live no-extra-force residual vector.",
        "",
    ]
    sections = [
        ("Source Register", "sources", ["source_id"]),
        ("qX Source-Safety Theorem", "theorem", ["theorem_id", "claim_piece"]),
        ("No-Extra-Force Contract", "contract", ["clause_id", "clause"]),
        ("Current Corpus Source-Safety Audit", "audit", ["audit_id", "item"]),
        ("epsilon_source_XQ Bound Rows", "bound_rows", ["row_id", "symbol"]),
        ("Arena Source Projection Rows", "arena_rows", ["arena_id", "observable"]),
        ("Claim Gates", "gates", ["gate_id"]),
        ("Decisions", "decisions", ["decision_id"]),
        ("Next Target", "next_target", ["target_doc"]),
        ("Validation", "validation", ["check_id", "result"]),
    ]
    for title, key, key_fields in sections:
        lines.append(f"## {title}")
        for row in grouped[key]:
            lines.append(row_bullet(row, key_fields))
    DOC_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def cleanup_pycache():
    pycache = PCW / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main():
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    grouped = {
        "sources": source_register(timestamp),
        "theorem": theorem_rows(timestamp),
        "contract": contract_rows(timestamp),
        "audit": audit_rows(timestamp),
        "bound_rows": bound_rows(timestamp),
        "arena_rows": arena_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["gates"] = claim_gate_rows(timestamp, grouped)

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["theorem"], grouped["theorem"])
    write_csv(OUTPUTS["contract"], grouped["contract"])
    write_csv(OUTPUTS["audit"], grouped["audit"])
    write_csv(OUTPUTS["bound_rows"], grouped["bound_rows"])
    write_csv(OUTPUTS["arena_rows"], grouped["arena_rows"])
    write_csv(OUTPUTS["gates"], grouped["gates"])
    write_csv(OUTPUTS["decisions"], grouped["decisions"])
    write_csv(OUTPUTS["next_target"], grouped["next_target"])
    write_csv(OUTPUTS["status"], grouped["status"])

    grouped["validation"] = [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "check_id": "pending",
            "result": "PASS",
            "detail": "placeholder before final validation",
        }
    ]
    write_markdown(grouped)
    cleanup_pycache()
    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])
    write_markdown(grouped)
    cleanup_pycache()

    failed = [row for row in grouped["validation"] if row["result"] != "PASS"]
    print(grouped["status"][0]["status"])
    print(f"wrote {DOC_PATH}")
    if failed:
        raise SystemExit(f"validation failed: {failed}")


if __name__ == "__main__":
    main()
