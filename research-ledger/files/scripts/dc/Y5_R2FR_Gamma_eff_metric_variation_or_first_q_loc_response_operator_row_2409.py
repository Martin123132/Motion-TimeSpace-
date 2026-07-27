from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_GAMMA_EFF_METRIC_VARIATION_OR_FIRST_Q_LOC_RESPONSE_OPERATOR_ROW_2409"
SCRIPT_PATH = Path(__file__).resolve()
POST_ROOT = SCRIPT_PATH.parents[1]
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
FORMALIZATION_ROOT = POST_ROOT.parent / "formalization-workbench"
DOC_PATH = POST_ROOT / "2409-Y5-R2FR-Gamma-eff-metric-variation-or-first-q-loc-response-operator-row.md"


def post(path_text: str) -> Path:
    return POST_ROOT / path_text


SOURCES = [
    {
        "source_id": "SRC2409_2408_handoff",
        "path": str(post("2408-Y5-R2FR-topological-Hilbert-equality-R-eq-zero-or-epsilonM-bound-fill.md")),
        "needles": "NEXT2408_0_selected|DEC2408_3_next|VAL2408_OVERALL",
        "role": "immediate handoff selecting Gamma_eff metric variation or first q_loc response row",
    },
    {
        "source_id": "SRC2409_2207_doc",
        "path": str(post("2207-Y5-R2FR-Gamma-eff-metric-variation-or-first-q-loc-response-operator-row.md")),
        "needles": "GMV2207_0_response_doublet_setup|KMR2207_2_Khat_identity|ROP2207_0_PPN_q_loc_linear_response_schema|VAL2207_OVERALL",
        "role": "prior exact 2207 attempt: formal metric variation plus first PPN response schema",
    },
    {
        "source_id": "SRC2409_2207_variation_csv",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2207_GAMMA_EFF_METRIC_VARIATION_ATTEMPT.csv")),
        "needles": "GMV2207_0_response_doublet_setup|GMV2207_3_verdict",
        "role": "machine Gamma_eff metric variation attempt",
    },
    {
        "source_id": "SRC2409_2207_khat_csv",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2207_KHAT_METRIC_RESPONSE_MATCH_AUDIT.csv")),
        "needles": "KMR2207_1_metric_variation_computed_formally|KMR2207_5_overall",
        "role": "machine Khat metric-response match audit",
    },
    {
        "source_id": "SRC2409_2207_response_csv",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2207_FIRST_RESPONSE_OPERATOR_ROW.csv")),
        "needles": "ROP2207_0_PPN_q_loc_linear_response_schema|ROP2207_1_R10_q_loc_range_response_held",
        "role": "first q_loc response-operator schema rows",
    },
    {
        "source_id": "SRC2409_2208_doc",
        "path": str(post("2208-Y5-R2FR-PPN-Green-operator-source-normalization-or-R10-range-kernel.md")),
        "needles": "PPNL2208_0_operator_factorization|R10K2208_0_yukawa_kernel_form|NEXT2208_0_2209|VAL2208_OVERALL",
        "role": "response-row lowering: PPN inverse-divergence blocker and R10 kernel scaffold",
    },
    {
        "source_id": "SRC2409_2191_doc",
        "path": str(post("2191-Y5-R2FR-q_loc-component-projection-runner-and-theorem-zero-certificate.md")),
        "needles": "QCS2191_1_PPN|RUN2191_0_PPN|VAL2191_OVERALL",
        "role": "q_loc component schema and no-scalar-proxy guard",
    },
    {
        "source_id": "SRC2409_1664_doc",
        "path": str(post("1664-Y5-R2FR-Gamma-Khat-metric-response-source-formula-or-Helmholtz-obstruction.md")),
        "needles": "SFA1664_0_live_Gamma_owner|MRT1664_4_verdict|VAL1664_OVERALL",
        "role": "older Gamma/Khat metric-response obstruction and Helmholtz gate",
    },
    {
        "source_id": "SRC2409_GK_metric_response_audit",
        "path": str(post("source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv")),
        "needles": "MA515_0_Gamma_scalar_density_owner|MA515_6_units_and_readout",
        "role": "strict source evidence that live Gamma/Khat ownership remains missing",
    },
    {
        "source_id": "SRC2409_Gamma_owner_candidates",
        "path": str(post("source-intake/mts_residuals/P8_GAMMA_OWNER_CANDIDATE_ACTION.csv")),
        "needles": "GO516_A_response_doublet_quadratic_density|GO516_D_residual_bound_runner",
        "role": "candidate Gamma_eff action densities and fallback residual route",
    },
    {
        "source_id": "SRC2409_2221_doc",
        "path": str(post("2221-Y5-R2FR-delta-g-SGamma-Kmetric-kernel-norm-source-pass.md")),
        "needles": "KNA2221_0_delta_g_SGamma|KNA2221_7_units_projection|VAL2221_OVERALL",
        "role": "later Kmetric kernel-norm bridge showing source-bound/local-lock blockers",
    },
    {
        "source_id": "SRC2409_2222_doc",
        "path": str(post("2222-Y5-R2FR-current-local-frontier-import-and-Jsrc-Binner-source-bound-gate.md")),
        "needles": "CSEL2222_2_core_blocker|NEXT2222_0_2223|VAL2222_OVERALL",
        "role": "parallel derivation frontier: quotient map/vertical generator for source-boundary silence",
    },
]


def source_register_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source in SOURCES:
        source_path = Path(source["path"])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_path": source["path"],
                "exists": str(source_path.exists()).lower(),
                "needles": source["needles"],
                "role": source["role"],
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        )
    return rows


def gamma_variation_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "GMV2409_0_response_doublet",
            "candidate": "Gamma_eff=Gamma0+1/2 M_AB(g,R_even,D,...) Z^A Z^B+O(Z^4)",
            "metric_variation": "K_metric^{mu nu}=2/sqrt(-g) delta[sqrt(-g)Gamma_eff]/delta g_{mu nu}=volume term + 1/2 delta_g M_AB Z^A Z^B + M_AB Z^A delta_g Z^B + derivative/boundary terms",
            "double_zero_status": "CONDITIONAL_DOUBLE_ZERO_AT_Z0",
            "what_is_won": "formal response-doublet density can make K_metric(Phi0)=0 and first Z variation vanish after Gamma0 subtraction",
            "what_is_not_won": "current MTS K_hat is not source-signed as this K_metric",
            "proof_status": "FORMAL_VARIATION_MERGED_NONCLAIM",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "GMV2409_1_positive_auxiliary",
            "candidate": "Gamma_eff=V(Phi)+1/2 G_AB(Phi) nabla Phi^A nabla Phi^B",
            "metric_variation": "ordinary potential/gradient stress response plus derivative and boundary terms",
            "double_zero_status": "CONDITIONAL_GAP_ROUTE",
            "what_is_won": "positive operator/gap route could silence local fields under source-free no-boundary conditions",
            "what_is_not_won": "source-free collar, K_hat identity, and boundary silence are unsigned",
            "proof_status": "HELD_AS_PARENT_ACTION_CANDIDATE",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "GMV2409_2_topological_boundary",
            "candidate": "Gamma_eff=dB_GK or normalized boundary/topological density",
            "metric_variation": "bulk improvement stress can be locally silent only under fixed boundary/topology",
            "double_zero_status": "BOUNDARY_OPEN",
            "what_is_won": "bulk q_loc could be silent in a true topological/improvement branch",
            "what_is_not_won": "theta_GK/Q_GK no-flux, charge units, and fixed boundary class remain open",
            "proof_status": "HELD_WITH_HIGH_BOUNDARY_RISK",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "GMV2409_3_current_verdict",
            "candidate": "current live Gamma_eff/K_hat branch",
            "metric_variation": "formal variation exists only for candidate branches, not for live MTS K_hat",
            "double_zero_status": "NOT_PARENT_SIGNED",
            "what_is_won": "coupling now has a credible parent-action target rather than hand-waving",
            "what_is_not_won": "q_loc=0, local GR, Newton, PPN, or R10 claim",
            "proof_status": "KHAT_IDENTITY_NOT_MATCHED_FIRST_RESPONSE_ROUTE_ACTIVE",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
    ]


def khat_match_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "KMR2409_0_candidate_density",
            "match_clause": "Gamma_eff source-owned scalar density",
            "required_evidence": "explicit local scalar density with field content, metric dependence, units, and boundary convention",
            "current_evidence": "response-doublet candidate exists; live Gamma_eff owner remains missing in MA515/1664",
            "pass_now": "false",
            "residual_if_missing": "q_action_owner_defect",
            "next_action": "write actual parent density or keep residual branch",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "KMR2409_1_formal_variation",
            "match_clause": "formal K_metric formula",
            "required_evidence": "delta[sqrt(-g)Gamma_eff]/delta g_{mu nu} with volume, derivative and boundary terms",
            "current_evidence": "2207 writes the formal response-doublet variation",
            "pass_now": "true",
            "residual_if_missing": "none_for_formal_step",
            "next_action": "compare K_metric to live K_hat symbol map",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "KMR2409_2_Khat_identity",
            "match_clause": "K_hat equals K_metric",
            "required_evidence": "source path proving K_hat is defined as the same metric response under one convention",
            "current_evidence": "no derivation as delta[sqrt(-g)Gamma_eff]/delta g found",
            "pass_now": "false",
            "residual_if_missing": "q_metric_response_defect",
            "next_action": "source/derive K_hat identity or carry q_metric_response_defect",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "KMR2409_3_double_zero",
            "match_clause": "T_GK(Phi0)=0 and first variation zero",
            "required_evidence": "Gamma0 subtraction, Z=0 fixed point, regular M_AB, and no linear metric/readout term maps to physical q_loc",
            "current_evidence": "formal double-zero exists, but physical q_loc component map is missing",
            "pass_now": "false",
            "residual_if_missing": "epsilon_C0_GammaKhat;epsilon_dC_GammaKhat",
            "next_action": "map response-doublet variables to observed q_loc components or retain finite residual",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "KMR2409_4_units_readout",
            "match_clause": "units and PPN/R10 response",
            "required_evidence": "q_loc units, source normalization, response operators into local observables",
            "current_evidence": "2191/2207/2208 leave source normalization and response inputs missing",
            "pass_now": "false",
            "residual_if_missing": "q_units_response_defect",
            "next_action": "lower one response route until it has source-backed units or a blocker ledger",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "KMR2409_5_overall",
            "match_clause": "Khat metric-response parent signature",
            "required_evidence": "all KMR2409_0..4 pass in one branch",
            "current_evidence": "only the formal variation step passes; live ownership and Khat identity fail",
            "pass_now": "false",
            "residual_if_missing": "q_loc_residual_vector_abs",
            "next_action": "do not claim q_loc zero; use response-operator lowering route",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
    ]


def response_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "operator_id": "ROP2409_0_PPN_q_loc_linear_response_schema",
            "arena": "PPN",
            "row_kind": "first_nonclaim_response_operator_schema_retained",
            "input_contract": "observed-frame q_loc components q_T,q_L,q_TF,q_alpha_i plus source normalization and weak-field gauge",
            "output_quantity": "Delta_PPN_q=(Delta_beta,Delta_gamma,Delta_alpha_i,Delta_zeta_i,Delta_xi)",
            "operator_form": "Delta_PPN_A = integral_D G_A^nu(x,xprime) q_loc_nu(xprime)dVprime + boundary/support terms",
            "status": "SCHEMA_READY_NOT_SCORE_READY",
            "blocking_missing_inputs": "MISSING_GREEN_OPERATOR;MISSING_QLOC_PROFILE;MISSING_SOURCE_NORMALIZATION;MISSING_BOUNDARY_SUPPORT_TERMS",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "operator_id": "ROP2409_1_PPN_lowered_stress_blocker",
            "arena": "PPN",
            "row_kind": "lowered_operator_blocker",
            "input_contract": "T_res or parent inverse-divergence map I_div^{-1}[q_loc]",
            "output_quantity": "weak-field metric perturbation and PPN coefficients",
            "operator_form": "R_PPN[q_loc]=Pi_PPN o G_Einstein^lin o I_div^{-1}[q_loc]",
            "status": "LOWERED_BUT_BLOCKED",
            "blocking_missing_inputs": "MISSING_I_DIV_INVERSE_CONVENTION;MISSING_TGK_PROFILE;MISSING_SOURCE_NORMALIZATION;MISSING_PPN_GAUGE",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "operator_id": "ROP2409_2_R10_yukawa_kernel_scaffold",
            "arena": "R10_short_range",
            "row_kind": "selected_next_response_lane",
            "input_contract": "q_loc-to-Yukawa source map, lambda_X, source/test charge normalization, and alpha_bound(lambda)",
            "output_quantity": "alpha_R10_q(lambda)",
            "operator_form": "K_lambda(r)=exp(-r/lambda)/(4*pi*r); compare abs(alpha_R10_q(lambda)) <= alpha_bound(lambda)",
            "status": "SCAFFOLD_READY_NOT_SCORE_READY",
            "blocking_missing_inputs": "MISSING_QLOC_TO_YUKAWA_SOURCE_MAP;MISSING_LAMBDA_X;MISSING_CHARGE_NORMALIZATION;MISSING_REAL_BOUND_CURVE",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
    ]


def route_merge_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "RM2409_0_2408_handoff",
            "route": "Gamma_eff metric variation or q_loc response row",
            "status": "HANDOFF_HANDLED",
            "finding": "2207 already wrote the formal variation and first PPN response schema",
            "action": "merge and validate current numbering rather than re-run the same proof",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "RM2409_1_parent_route",
            "route": "Khat/Gamma_eff metric-response identity",
            "status": "OPEN_PARENT_ROUTE",
            "finding": "response-doublet candidate is promising but not live-MTS signed",
            "action": "keep Khat identity source hunt as parallel route, not a claim",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "RM2409_2_empirical_route",
            "route": "q_loc response operator",
            "status": "ACTIVE_NONCLAIM_TEST_ROUTE",
            "finding": "PPN row lowers to inverse-divergence blocker; R10 lane is narrower",
            "action": "select R10 q_loc-Yukawa source map/bound-curve blocker next",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "RM2409_3_parallel_derivation",
            "route": "source-boundary/local-lock frontier",
            "status": "HELD_PARALLEL",
            "finding": "2221/2222 show local-lock source-boundary norms and Dq[v_m] remain central",
            "action": "return after the R10 lane is lowered or if q_loc-to-source map requires quotient verticality",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG2409_0_formal_variation",
            "gate": "one Gamma_eff formal metric variation is written",
            "status": "PASS_NONCLAIM",
            "implication": "the response-doublet route is a real parent-action target, not proof of current MTS",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG2409_1_Khat_match",
            "gate": "K_hat equals computed K_metric",
            "status": "BLOCKED_NONCLAIM",
            "implication": "q_metric_response_defect remains live",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG2409_2_q_loc_zero",
            "gate": "q_loc=0/local GR can be claimed",
            "status": "BLOCKED_NONCLAIM",
            "implication": "formal variation alone is not enough; action owner, Khat identity, Euler, P_loc, boundary and source clauses remain unsigned",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG2409_3_first_response_row",
            "gate": "first q_loc response schema exists",
            "status": "PASS_NONCLAIM",
            "implication": "testing path is concrete but not score-ready",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG2409_4_PPN_R10_score",
            "gate": "PPN/R10 score can be computed",
            "status": "BLOCKED_NONCLAIM",
            "implication": "PPN lacks inverse-divergence stress reconstruction; R10 lacks source map, lambda, charges and bound curve",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG2409_5_GitHub",
            "gate": "public/GitHub update",
            "status": "BLOCKED_NONCLAIM",
            "implication": "private derivation/testing branch remains mid-proof",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
    ]


def refusal_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2409_0_formal_equals_live",
            "claim": "formal Gamma_eff variation proves live K_hat identity",
            "allowed": "false",
            "reason": "candidate variation is not current-MTS proof unless K_hat is source-defined as the same metric response",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2409_1_q_loc_alone_metric_source",
            "claim": "q_loc alone defines a unique PPN metric source",
            "allowed": "false",
            "reason": "q_loc is a projected divergence; PPN needs T_res or a parent inverse-divergence rule",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": "MTS_R2FR_GAMMA_EFF_METRIC_VARIATION_OR_FIRST_Q_LOC_RESPONSE_OPERATOR_ROW_2409",
            "row_id": "REF2409_2_score_placeholder",
            "claim": "PPN/R10 placeholders can be scored",
            "allowed": "false",
            "reason": "response operators, profiles, source normalization, kernels and bound curves remain missing",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2409_3_cassini_direct",
            "claim": "Cassini proxy is a direct q_loc/MTS bound",
            "allowed": "false",
            "reason": "Cassini is useful pressure only after vector-tail/source-normalization translation gates close",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2409_0_gain",
            "decision": "FORMAL_GAMMA_EFF_VARIATION_MERGED",
            "rationale": "response-doublet candidate gives a real metric-response/double-zero target",
            "next_action": "preserve as parent-action construction route",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2409_1_limit",
            "decision": "KHAT_IDENTITY_NOT_PARENT_SIGNED",
            "rationale": "only the formal variation step passes; live K_hat identity and units/readout fail",
            "next_action": "keep q_metric_response_defect in official residual vector",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2409_2_testing_path",
            "decision": "RESPONSE_OPERATOR_ROUTE_OPEN",
            "rationale": "2207/2208 lower the empirical interface from vague q_loc to PPN stress reconstruction and R10 Yukawa kernel scaffold",
            "next_action": "try R10 q_loc-to-Yukawa source map because it is narrower than full PPN",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2409_3_no_claim",
            "decision": "NO_LOCAL_GR_OR_EMPIRICAL_CLAIM",
            "rationale": "current checkpoint is a merge/gate, not a theorem-zero or score",
            "next_action": "continue deriving or sourcing missing operator/source/profile rows",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2409_0_selected",
            "next_doc": "2410-Y5-R2FR-R10-q-loc-Yukawa-source-map-or-bound-curve-blocker.md",
            "why": "R10 is narrower than full PPN and only needs one finite-range kernel lane, source/test charge normalization, lambda_X, and alpha_bound(lambda)",
            "expected_output": "source-backed q_loc-to-Yukawa source map or a blocker ledger with all missing inputs explicit and valid_for_claim=false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2409_1_parent_parallel",
            "next_doc": "2410B-Y5-R2FR-Khat-identity-source-hunt-or-TGK-stress-reconstruction-for-PPN.md",
            "why": "if Khat identity appears, it supplies the missing inverse-divergence/stress source and reopens parent local-GR/PPN route",
            "expected_output": "K_hat identity source path with matching convention or retained q_metric_response_defect",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2409_2_derivation_parallel",
            "next_doc": "2410C-Y5-R2FR-quotient-map-vertical-generator-frontier-import-or-finite-coupling-row.md",
            "why": "2222 shows Dq[v_m] is the core source-boundary coupling object if the R10 source map requires quotient verticality",
            "expected_output": "Dq[v_m]=0 certificate or finite coupling leakage row, still nonclaim",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
    ]


CSV_BUILDERS = {
    "P8_Y5_PARENT_QLOC_2409_SOURCE_REGISTER.csv": source_register_rows,
    "P8_Y5_PARENT_QLOC_2409_GAMMA_EFF_METRIC_VARIATION_MERGE.csv": gamma_variation_rows,
    "P8_Y5_PARENT_QLOC_2409_KHAT_METRIC_RESPONSE_MATCH_AUDIT.csv": khat_match_rows,
    "P8_Y5_PARENT_QLOC_2409_QLOC_RESPONSE_OPERATOR_STATUS.csv": response_rows,
    "P8_Y5_PARENT_QLOC_2409_ROUTE_MERGE_AUDIT.csv": route_merge_rows,
    "P8_Y5_PARENT_QLOC_2409_CLAIM_GATES.csv": claim_gate_rows,
    "P8_Y5_PARENT_QLOC_2409_REFUSAL_RUNNER.csv": refusal_rows,
    "P8_Y5_PARENT_QLOC_2409_DECISION_LEDGER.csv": decision_rows,
    "P8_Y5_PARENT_QLOC_2409_NEXT_TARGET.csv": next_target_rows,
}


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def sources_exist() -> bool:
    return all(Path(source["path"]).exists() for source in SOURCES)


def needles_found() -> bool:
    for source in SOURCES:
        source_path = Path(source["path"])
        if not source_path.exists():
            return False
        text = source_path.read_text(encoding="utf-8", errors="ignore")
        for needle in source["needles"].split("|"):
            if needle not in text:
                return False
    return True


def generated_rows() -> list[dict[str, str]]:
    return [
        *source_register_rows(),
        *gamma_variation_rows(),
        *khat_match_rows(),
        *response_rows(),
        *route_merge_rows(),
        *claim_gate_rows(),
        *refusal_rows(),
        *decision_rows(),
        *next_target_rows(),
    ]


def generated_text() -> str:
    return "\n".join(str(row) for row in generated_rows())


def csvs_parse() -> bool:
    csv_names = list(CSV_BUILDERS.keys()) + ["P8_Y5_BRR545_2409_VALIDATION.csv"]
    for csv_name in csv_names:
        csv_path = RESIDUALS / csv_name
        if not csv_path.exists():
            return False
        with csv_path.open(newline="", encoding="utf-8") as csv_file:
            rows = list(csv.DictReader(csv_file))
        if not rows:
            return False
    return True


def no_claim_flags() -> bool:
    return all(
        str(row.get("valid_for_claim", "false")).lower() == "false"
        and str(row.get("claim_allowed", "false")).lower() == "false"
        for row in generated_rows()
    )


def formalization_untouched_by_outputs() -> bool:
    output_paths = [DOC_PATH, *(RESIDUALS / csv_name for csv_name in CSV_BUILDERS), RESIDUALS / "P8_Y5_BRR545_2409_VALIDATION.csv"]
    try:
        formalization_resolved = FORMALIZATION_ROOT.resolve()
    except FileNotFoundError:
        return True
    for output_path in output_paths:
        try:
            output_resolved = output_path.resolve()
        except FileNotFoundError:
            output_resolved = output_path.parent.resolve() / output_path.name
        if output_resolved == formalization_resolved or formalization_resolved in output_resolved.parents:
            return False
    return True


def validation_rows() -> list[dict[str, str]]:
    text = generated_text()
    checks = [
        {
            "row_id": "VAL2409_00_sources_exist",
            "status": "PASS" if sources_exist() else "FAIL",
            "detail": "all required source paths exist" if sources_exist() else "one or more source paths are missing",
        },
        {
            "row_id": "VAL2409_01_needles_found",
            "status": "PASS" if needles_found() else "FAIL",
            "detail": "all source needles found" if needles_found() else "one or more source needles are missing",
        },
        {
            "row_id": "VAL2409_02_formal_variation",
            "status": "PASS" if "GMV2409_0_response_doublet" in text and "CONDITIONAL_DOUBLE_ZERO_AT_Z0" in text else "FAIL",
            "detail": "response-doublet formal variation and conditional double-zero are retained",
        },
        {
            "row_id": "VAL2409_03_khat_not_promoted",
            "status": "PASS" if "KMR2409_2_Khat_identity" in text and "pass_now': 'false" in text else "FAIL",
            "detail": "K_hat metric-response identity remains unpromoted",
        },
        {
            "row_id": "VAL2409_04_response_rows",
            "status": "PASS" if "ROP2409_0_PPN_q_loc_linear_response_schema" in text and "ROP2409_2_R10_yukawa_kernel_scaffold" in text else "FAIL",
            "detail": "PPN schema and R10 kernel scaffold are present",
        },
        {
            "row_id": "VAL2409_05_claim_gates",
            "status": "PASS" if "CG2409_2_q_loc_zero" in text and "BLOCKED_NONCLAIM" in text else "FAIL",
            "detail": "q_loc/local-GR and PPN/R10 scoring claims remain blocked",
        },
        {
            "row_id": "VAL2409_06_no_placeholder_scoring",
            "status": "PASS" if "REF2409_2_score_placeholder" in text else "FAIL",
            "detail": "placeholder scoring refusal is explicit",
        },
        {
            "row_id": "VAL2409_07_next_selected",
            "status": "PASS" if "NEXT2409_0_selected" in text and "R10-q-loc-Yukawa-source-map" in text else "FAIL",
            "detail": "R10 q_loc-Yukawa source-map route selected next",
        },
        {
            "row_id": "VAL2409_08_csv_parse",
            "status": "PASS" if csvs_parse() else "FAIL",
            "detail": "generated CSVs parse and have rows",
        },
        {
            "row_id": "VAL2409_09_no_claim_flags",
            "status": "PASS" if no_claim_flags() else "FAIL",
            "detail": "no generated row has valid_for_claim=true or claim_allowed=true",
        },
        {
            "row_id": "VAL2409_10_formalization_untouched_by_outputs",
            "status": "PASS" if formalization_untouched_by_outputs() else "FAIL",
            "detail": "script outputs stay inside post-checkpoint-work",
        },
    ]
    overall = "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL"
    checks.append(
        {
            "row_id": "VAL2409_OVERALL",
            "status": overall,
            "detail": "2409 merges the Gamma_eff metric-variation attempt, refuses Khat identity promotion, retains q_loc response rows, and selects the R10 q_loc-Yukawa source-map blocker next",
        }
    )
    return [{"branch_id": BRANCH_ID, **row} for row in checks]


def markdown_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc() -> None:
    body = f"""# 2409 - Gamma_eff Metric Variation Or First q_loc Response Operator Row

## Result

This checkpoint merges the existing `2207/2208` work into the current post-2408 branch.

The good news: the response-doublet candidate

`Gamma_eff = Gamma0 + 1/2 M_AB(g,R_even,D,...) Z^A Z^B + O(Z^4)`

has a real formal metric variation and a conditional double-zero at `Z=0` after `Gamma0` subtraction.  That is a genuine
parent-action target for the coupling problem.

The hard limit: current MTS still does not prove that live `K_hat` equals that metric response under the same
convention.  So `q_loc=0`, local GR, Newton, PPN, and R10 are not claimable from this.

The empirical path is now disciplined: PPN needs residual-stress reconstruction, while R10 is narrower and should be
lowered next through a Yukawa source map, `lambda_X`, source/test charges, and a real `alpha_bound(lambda)` curve.

## Source Register

{markdown_table(source_register_rows(), ["source_id", "source_path", "exists", "role", "valid_for_claim", "claim_allowed"])}

## Gamma_eff Metric Variation Merge

{markdown_table(gamma_variation_rows(), ["attempt_id", "candidate", "metric_variation", "double_zero_status", "what_is_won", "what_is_not_won", "proof_status", "valid_for_claim", "claim_allowed"])}

## Khat Metric-Response Match Audit

{markdown_table(khat_match_rows(), ["audit_id", "match_clause", "required_evidence", "current_evidence", "pass_now", "residual_if_missing", "next_action", "valid_for_claim", "claim_allowed"])}

## q_loc Response Operator Status

{markdown_table(response_rows(), ["operator_id", "arena", "row_kind", "input_contract", "output_quantity", "operator_form", "status", "blocking_missing_inputs", "valid_for_claim", "claim_allowed"])}

## Route Merge Audit

{markdown_table(route_merge_rows(), ["route_id", "route", "status", "finding", "action", "valid_for_claim", "claim_allowed"])}

## Claim Gates

{markdown_table(claim_gate_rows(), ["gate_id", "gate", "status", "implication", "valid_for_claim", "claim_allowed"])}

## Refusal Runner

{markdown_table(refusal_rows(), ["row_id", "claim", "allowed", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger

{markdown_table(decision_rows(), ["decision_id", "decision", "rationale", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target

{markdown_table(next_target_rows(), ["route_id", "next_doc", "why", "expected_output", "valid_for_claim", "claim_allowed"])}

## Validation

{markdown_table(validation_rows(), ["row_id", "status", "detail"])}

## Practical Status

This is one of those useful “not yet” checkpoints.  The coupling problem now has teeth:

`K_hat ?= 2/sqrt(-g) delta[sqrt(-g) Gamma_eff]/delta g`.

If that identity is sourced, the local-GR route gets a real parent-action clause.  If not, the residual is not vague:
`q_loc` must be projected through explicit response operators.  Full PPN is too broad first, so the next best attack is
the narrower R10 Yukawa/source-map lane.  Still private, still no GitHub.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    for csv_name, builder in CSV_BUILDERS.items():
        write_csv(RESIDUALS / csv_name, builder())
    write_csv(RESIDUALS / "P8_Y5_BRR545_2409_VALIDATION.csv", validation_rows())
    write_csv(RESIDUALS / "P8_Y5_BRR545_2409_VALIDATION.csv", validation_rows())
    write_doc()
    print(f"wrote {DOC_PATH}")
    print(f"wrote {RESIDUALS / 'P8_Y5_BRR545_2409_VALIDATION.csv'}")


if __name__ == "__main__":
    main()
