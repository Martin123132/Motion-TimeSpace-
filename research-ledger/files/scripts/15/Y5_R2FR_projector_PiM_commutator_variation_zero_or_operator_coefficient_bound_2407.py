from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_PROJECTOR_PIM_COMMUTATOR_VARIATION_ZERO_OR_OPERATOR_COEFFICIENT_BOUND_2407"
SCRIPT_PATH = Path(__file__).resolve()
POST_ROOT = SCRIPT_PATH.parents[1]
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
FORMALIZATION_ROOT = POST_ROOT.parent / "formalization-workbench"
DOC_PATH = POST_ROOT / "2407-Y5-R2FR-projector-PiM-commutator-variation-zero-or-operator-coefficient-bound.md"


def post(path_text: str) -> Path:
    return POST_ROOT / path_text


SOURCES = [
    {
        "source_id": "SRC2407_2406_handoff",
        "path": str(post("2406-Y5-R2FR-sector-by-sector-MTS-residual-variation-and-local-scaling-silence-or-operator-bounds.md")),
        "needles": "NEXT2406_0_selected|SVC2406_2_projector_domain|SCL2406_2_projector_domain|VAL2406_OVERALL",
        "role": "immediate handoff selecting Pi_M commutator/projector variation as the next concrete target",
    },
    {
        "source_id": "SRC2407_1772_doc",
        "path": str(post("1772-Y5-R2FR-PiM-commutator-projector-variation-zero-or-coefficient-bound.md")),
        "needles": "PCZ1772_1_topological_zero|PCB1772_1_I_commutator|GATE1772_0_commutator_zero|VAL1772_OVERALL",
        "role": "earlier Pi_M theorem/bound checkpoint",
    },
    {
        "source_id": "SRC2407_1772_zero_csv",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1772_PIM_COMMUTATOR_ZERO_ATTEMPT.csv")),
        "needles": "PCZ1772_0_product_rule|PCZ1772_4_current_verdict",
        "role": "1772 commutator-zero attempt",
    },
    {
        "source_id": "SRC2407_1772_bound_csv",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1772_PIM_COEFFICIENT_BOUND_PACK.csv")),
        "needles": "PCB1772_1_I_commutator|PCB1772_3_projector_stress_beta_equiv|PCB1772_5_epsilon_radial_Meff",
        "role": "1772 nonclaim coefficient rows",
    },
    {
        "source_id": "SRC2407_1518_commutator_csv",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_PIM_1518_COMMUTATOR_ZERO_AUDIT.csv")),
        "needles": "COM1518_0_product_rule|COM1518_8_verdict",
        "role": "same-parent Pi_M commutator-zero audit",
    },
    {
        "source_id": "SRC2407_1518_chainmap_csv",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_PIM_1518_FIXED_CHAINMAP_CONTRACT.csv")),
        "needles": "FCM1518_0_selector|FCM1518_6_tau_MHref",
        "role": "fixed-chainmap parent requirements",
    },
    {
        "source_id": "SRC2407_1715_commutator_csv",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1715_PIM_COMMUTATOR_ZERO_ATTEMPT.csv")),
        "needles": "PCZ1715_1_conditional_chainmap_lemma|PCZ1715_8_verdict",
        "role": "R2FR commutator zero clauses",
    },
    {
        "source_id": "SRC2407_1719_domain_csv",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1719_DPIM_DOMAIN_OPERATOR_AUDIT.csv")),
        "needles": "DPO1719_0_operator_definition|DPO1719_4_verdict",
        "role": "domain-derivative operator audit",
    },
    {
        "source_id": "SRC2407_2181_doc",
        "path": str(post("2181-Y5-R2FR-PiM-commutator-worldtube-source-glue-zero-or-epsilonM-fill.md")),
        "needles": "PCA2181_1_fixed_topological_route|EMD2181_4_total_envelope|NEXT2181_0_2182|VAL2181_OVERALL",
        "role": "latest worldtube/source-glue synthesis",
    },
    {
        "source_id": "SRC2407_2181_commutator_csv",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2181_PIM_COMMUTATOR_ZERO_AUDIT.csv")),
        "needles": "PCA2181_1_fixed_topological_route|PCA2181_5_current_status",
        "role": "2181 commutator audit",
    },
    {
        "source_id": "SRC2407_2181_worldtube_csv",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2181_WORLDTUBE_SOURCE_GLUE_AUDIT.csv")),
        "needles": "WTG2181_0_source_identity|WTG2181_5_current_status",
        "role": "worldtube source-glue audit",
    },
    {
        "source_id": "SRC2407_2181_epsilon_csv",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2181_EPSILON_M_DECOMPOSITION.csv")),
        "needles": "EMD2181_4_total_envelope",
        "role": "epsilon_M no-cancellation envelope",
    },
    {
        "source_id": "SRC2407_2181_finite_csv",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2181_EPSILON_M_FINITE_ROWS.csv")),
        "needles": "EFR2181_1_I_commutator|EFR2181_8_total",
        "role": "finite nonclaim rows for epsilon_M components",
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


def zero_theorem_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "proof_id": "PZ2407_0_product_rule",
            "claim_piece": "projected-current product rule",
            "mathematical_form": "d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H",
            "status": "EXACT_OBSTRUCTION_ACTIVE",
            "proof_result": "commutator term is real unless Pi_M is a chain-map on the physical current complex",
            "remaining_gap": "none algebraically; the issue is parent ownership of the chain-map/current/domain",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "PZ2407_1_fixed_chainmap_lemma",
            "claim_piece": "fixed chain-map kills commutator",
            "mathematical_form": "if d Pi_M = Pi_M d on C_H(A_ext), then [d,Pi_M]J_H=0",
            "status": "CONDITIONAL_THEOREM_CLEAN",
            "proof_result": "the zero proof is mathematically sound for a fixed parent-selected chain-map",
            "remaining_gap": "must prove physical J_H lives in that same complex and Pi_M is selected before readout",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "PZ2407_2_metric_independent_projector",
            "claim_piece": "projector variation stress zero",
            "mathematical_form": "delta_g Pi_M=0 if Pi_M is fixed absolute/topological data rather than Hodge/Green/domain data",
            "status": "CONDITIONAL_NO_STRESS_ROUTE",
            "proof_result": "a topological Pi_M can avoid T_PiM, but a Hodge/domain Pi_M cannot be ignored",
            "remaining_gap": "parent has not signed topological metric independence for the observed source map",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "PZ2407_3_parent_domain_lock",
            "claim_piece": "source worldtube and exterior annulus fixed",
            "mathematical_form": "delta W_M=delta A_ext=delta[S2]_M=0 before orbital/readout fitting",
            "status": "NOT_PARENT_SIGNED",
            "proof_result": "without a fixed domain, dPi_M domain terms survive",
            "remaining_gap": "parent selector/domain theorem or source-backed D_D Pi_M bound",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "PZ2407_4_physical_current_domain",
            "claim_piece": "Hilbert current in same chain complex",
            "mathematical_form": "J_H[e_obs,tau] in C_H(A_ext) with source/species/boundary/extra channels included or zeroed",
            "status": "SOURCE_DOMAIN_NOT_LOCKED",
            "proof_result": "chain-map lemma may target a surrogate current unless J_H is locked",
            "remaining_gap": "same-frame physical-current domain certificate",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "PZ2407_5_topological_Hilbert_equality",
            "claim_piece": "closed topological current is the observed Hilbert source current",
            "mathematical_form": "Pi_M J_H = J_M_top + dB_zero",
            "status": "KEY_BLOCKER_NOT_DERIVED",
            "proof_result": "a conserved closed current can be the wrong object for Newton/source normalization",
            "remaining_gap": "R_eq=0 theorem or source-backed R_eq_integral row",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "PZ2407_6_boundary_zero_flux",
            "claim_piece": "exact boundary improvement is silent",
            "mathematical_form": "integral_boundary dB_zero = 0 on the compact linked boundary",
            "status": "BOUNDARY_FLUX_UNSIGNED",
            "proof_result": "boundary exactness is not enough unless its linked flux vanishes in the same domain",
            "remaining_gap": "B_zero_flux=0 theorem or source-backed B_zero_flux row",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "PZ2407_7_tau_MHref_lock",
            "claim_piece": "same denominator and time generator",
            "mathematical_form": "tau_source=tau_charge=tau_clock=tau_readout and M_H_ref is parent-owned",
            "status": "MISSING_TAU_MHREF_LOCK",
            "proof_result": "I_commutator/R_eq cannot be claim-normalized without a same-frame denominator",
            "remaining_gap": "Hamiltonian/source denominator theorem or finite denominator source row",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "PZ2407_8_current_verdict",
            "claim_piece": "current MTS proves Pi_M commutator and projector variation zero",
            "mathematical_form": "[d,Pi_M]J_H=0 and delta_g Pi_M=0 for the physical source current/domain",
            "status": "PIM_COMMUTATOR_ZERO_NOT_PROVED",
            "proof_result": "conditional zero route is retained but not promoted",
            "remaining_gap": "topological-Hilbert equality, boundary zero flux, domain lock, current lock, and M_H_ref lock",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
    ]


def stress_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "stress_id": "PVS2407_0_variation_rule",
            "object": "projector variation",
            "mathematical_form": "delta(Pi_M J_H)=Pi_M delta J_H + (delta Pi_M)J_H",
            "status": "EXACT_VARIATION_RULE",
            "local_effect": "nonzero delta Pi_M produces source/projector stress",
            "required_for_zero": "delta_g Pi_M=0 and delta_domain Pi_M=0 before readout",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "stress_id": "PVS2407_1_topological_no_stress",
            "object": "fixed topological Pi_M",
            "mathematical_form": "Pi_M J=ell_M[J] omega_M_top with omega_M_top fixed and metric-independent",
            "status": "CONDITIONAL_NO_STRESS",
            "local_effect": "T_PiM can vanish if the projector is not a metric/domain functional",
            "required_for_zero": "parent-signed selector plus physical Hilbert equality",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "stress_id": "PVS2407_2_hodge_domain_stress",
            "object": "Hodge/DeWitt/Green/domain Pi_M",
            "mathematical_form": "Pi_M=Pi_M[g,n_mu,G_B,chi_D,W_M,A_ext]",
            "status": "STRESS_RETAINED_IF_USED",
            "local_effect": "delta_g Pi_M and domain variation map to PPN/source-normalization residuals",
            "required_for_zero": "zero theorem for each metric/domain derivative or finite operator bound",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "stress_id": "PVS2407_3_domain_derivative",
            "object": "domain derivative operator",
            "mathematical_form": "(dPi_M)_domain := D_D Pi_M[delta W_M,delta A_ext,delta[S2]_M]",
            "status": "FORMAL_SPLIT_ONLY",
            "local_effect": "moving support/linking surfaces can create I_commutator-like flux",
            "required_for_zero": "fixed support/homology theorem or C_DPiM ||delta_D|| bound",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "stress_id": "PVS2407_4_current_verdict",
            "object": "projector stress zero status",
            "mathematical_form": "T_PiM_munu := -2/sqrt(-g) delta S_PiM/delta g_munu = 0",
            "status": "PROJECTOR_STRESS_ZERO_NOT_PROVED",
            "local_effect": "local GR/PPN remains blocked if this is not zero or bounded",
            "required_for_zero": "topological no-stress proof or source-backed projector_stress_beta_equiv row",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
    ]


def bound_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCB2407_0_I_commutator",
            "symbol": "I_commutator",
            "definition": "M_H_ref^-1 integral_A [d,Pi_M]J_H on the finite exterior annulus",
            "units": "dimensionless_after_MHref_normalization_or_GM_flux_units",
            "status": "MISSING_ZERO_THEOREM_OR_NUMERIC_VALUE",
            "observable_link": "Newton_source;PPN_gamma_beta;R10;R11;orbital_GM",
            "value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCB2407_1_R_eq_integral",
            "symbol": "R_eq_integral",
            "definition": "M_H_ref^-1 integral_S(Pi_M J_H - J_M_top - dB_zero)",
            "units": "dimensionless_after_MHref_normalization",
            "status": "MISSING_TOPOLOGICAL_HILBERT_EQUALITY_OR_VALUE",
            "observable_link": "Newton_source;local_GR;source_normalization",
            "value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCB2407_2_B_zero_flux",
            "symbol": "B_zero_flux",
            "definition": "linked-boundary flux of exact/reference improvement dB_zero",
            "units": "GM_flux_or_dimensionless",
            "status": "MISSING_BOUNDARY_ZERO_FLUX_OR_VALUE",
            "observable_link": "boundary_reference;PPN_beta;Gdot;orbital_GM",
            "value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCB2407_3_projector_stress_beta_equiv",
            "symbol": "projector_stress_beta_equiv",
            "definition": "weak-field/PPN equivalent of metric stress generated by delta_g Pi_M",
            "units": "PPN_or_operator_units",
            "status": "MISSING_PROJECTOR_STRESS_MAP_OR_VALUE",
            "observable_link": "PPN_beta;PPN_gamma;preferred_frame;local_GR",
            "value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCB2407_4_DPiM_domain",
            "symbol": "D_D_PiM",
            "definition": "operator norm for Pi_M variation under worldtube/exterior/linking-class domain changes",
            "units": "declared_operator_norm",
            "status": "MISSING_OPERATOR_NORM_AND_DOMAIN_VARIATION_AMPLITUDE",
            "observable_link": "source_normalization;radial_hair;R10;orbital",
            "value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCB2407_5_epsilon_worldtube",
            "symbol": "epsilon_worldtube",
            "definition": "worldtube/source-domain selector mismatch in source mass",
            "units": "dimensionless",
            "status": "MISSING_WORLDTUBE_GLUE_ZERO_OR_VALUE",
            "observable_link": "Newton;WEP;clock;orbital",
            "value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCB2407_6_epsilon_extra_current",
            "symbol": "epsilon_extra_current",
            "definition": "normalized extra-current/anomaly/source-channel leakage in projected source closure",
            "units": "dimensionless_or_GM_flux_units",
            "status": "MISSING_EXTRA_CHANNEL_ZERO_OR_VALUE",
            "observable_link": "Newton;PPN;R11;species_coupling",
            "value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCB2407_7_epsilon_calibration",
            "symbol": "epsilon_calibration",
            "definition": "absolute calibration offset between surface charge and v-source mass",
            "units": "dimensionless",
            "status": "MISSING_PARENT_FIXED_CALIBRATION_OR_VALUE",
            "observable_link": "Newton;Gdot;PPN_beta",
            "value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCB2407_8_epsilon_M_abs",
            "symbol": "epsilon_M_abs",
            "definition": "absolute no-cancellation envelope for source-normalization residuals",
            "units": "declared_common_norm",
            "status": "MISSING_COMPONENT_VALUES",
            "observable_link": "all_local_arenas",
            "value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
    ]


def envelope_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "envelope_id": "ENV2407_0_no_cancellation",
            "quantity": "epsilon_M_abs",
            "formula": "abs(epsilon_M)<=abs(epsilon_worldtube)+abs(I_commutator)+abs(epsilon_extra_current)+abs(R_eq_integral)+abs(B_zero_flux)+abs(epsilon_calibration)+abs(projector_stress_beta_equiv)",
            "rule": "no cancellation credit without a parent identity",
            "status": "EXACT_BOUND_LEDGER_NONCLAIM",
            "next_needed": "zero theorem or source-backed value for each numerator component plus M_H_ref denominator",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "envelope_id": "ENV2407_1_local_GR_readout",
            "quantity": "c_projector_operator",
            "formula": "epsilon_PiM ~ abs(I_commutator)+abs(projector_stress_beta_equiv)+abs(D_D_PiM delta_D)+abs(R_eq_integral)+abs(B_zero_flux)",
            "rule": "local GR/Newton can reopen only if the envelope is zero or below arena thresholds",
            "status": "LOCAL_GR_REMAINS_BLOCKED",
            "next_needed": "topological-Hilbert equality or finite bound acquisition",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG2407_0_commutator_zero",
            "gate": "[d,Pi_M]J_H=0",
            "status": "BLOCKED",
            "blocker": "fixed chain-map theorem is conditional; physical Hilbert current/domain equality is unsigned",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG2407_1_projector_stress_zero",
            "gate": "delta_g Pi_M=0 and T_PiM=0",
            "status": "BLOCKED",
            "blocker": "topological no-stress route is not parent-signed; Hodge/domain route retains stress",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG2407_2_topological_Hilbert_equality",
            "gate": "Pi_M J_H=J_M_top+dB_zero",
            "status": "BLOCKED",
            "blocker": "closed wrong-charge countermodel remains active",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG2407_3_coefficient_bounds",
            "gate": "I_commutator/R_eq/B_zero/T_PiM rows are source-backed",
            "status": "BLOCKED",
            "blocker": "finite rows have missing numeric values, units normalization, and source paths",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG2407_4_Newton_local_GR",
            "gate": "Newton/local-GR source bridge reopens",
            "status": "BLOCKED",
            "blocker": "projector/source normalization residual remains live",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
    ]


def refusal_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2407_0_closed_wrong_charge",
            "claim": "closed topological current proves measured mass",
            "allowed": "false",
            "reason": "closed conserved object can be the wrong source unless Pi_M J_H=J_M_top+dB_zero with zero flux",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2407_1_hodge_free_lunch",
            "claim": "Hodge/domain projector has no stress",
            "allowed": "false",
            "reason": "metric/domain dependence gives delta_g Pi_M and domain derivative terms",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2407_2_post_readout_mask",
            "claim": "choose Pi_M after orbital/readout calibration",
            "allowed": "false",
            "reason": "that is GM laundering/closure-only, not a derivation of Newton or GR",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2407_3_cancellation",
            "claim": "source residuals cancel",
            "allowed": "false",
            "reason": "no cancellation credit without a parent identity tying the components",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2407_0_gain",
            "decision": "conditional commutator-zero theorem accepted",
            "reason": "fixed parent-selected chain-map implies [d,Pi_M]J_H=0 on the correct current complex",
            "consequence": "the algebra is no longer the blocker; parent ownership/equality is",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2407_1_no_promotion",
            "decision": "do not promote Pi_M zero for current MTS",
            "reason": "physical Hilbert equality, zero boundary flux, domain lock, current lock, and M_H_ref lock are unsigned",
            "consequence": "I_commutator and projector_stress_beta_equiv remain live finite rows",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2407_2_best_next",
            "decision": "attack topological-Hilbert equality/R_eq next",
            "reason": "once the chain-map lemma is conditional-clean, the wrong-conserved-object blocker is the bottleneck",
            "consequence": "2408 should try to prove Pi_M J_H=J_M_top+dB_zero with zero flux or fill R_eq/I_commutator rows",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2407_0_selected",
            "next_doc": "2408-Y5-R2FR-topological-Hilbert-equality-R-eq-zero-or-epsilonM-bound-fill.md",
            "why": "Pi_M commutator zero is conditional-clean only if the closed topological current is the same object as the Hilbert/worldtube source current",
            "expected_output": "prove Pi_M J_H=J_M_top+dB_zero with zero compact boundary flux, or emit R_eq/I_commutator/epsilon_M source-backed nonclaim rows",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2407_1_parallel_bound",
            "next_doc": "2408B-Y5-R2FR-projector-stress-and-Icommutator-bound-source-acquisition.md",
            "why": "if equality proof stalls, finite projector/source residual rows are the honest empirical interface",
            "expected_output": "source-backed units, normalization, and arena projection for I_commutator, T_PiM, D_D_PiM, and epsilon_M_abs",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
    ]


CSV_BUILDERS = {
    "P8_Y5_PARENT_QLOC_2407_SOURCE_REGISTER.csv": source_register_rows,
    "P8_Y5_PARENT_QLOC_2407_PIM_ZERO_THEOREM_ATTEMPT.csv": zero_theorem_rows,
    "P8_Y5_PARENT_QLOC_2407_PROJECTOR_VARIATION_STRESS_AUDIT.csv": stress_rows,
    "P8_Y5_PARENT_QLOC_2407_PIM_COEFFICIENT_BOUND_PACK.csv": bound_rows,
    "P8_Y5_PARENT_QLOC_2407_EPSILON_M_ENVELOPE.csv": envelope_rows,
    "P8_Y5_PARENT_QLOC_2407_CLAIM_GATES.csv": claim_gate_rows,
    "P8_Y5_PARENT_QLOC_2407_REFUSAL_RUNNER.csv": refusal_rows,
    "P8_Y5_PARENT_QLOC_2407_DECISION_LEDGER.csv": decision_rows,
    "P8_Y5_PARENT_QLOC_2407_NEXT_TARGET.csv": next_target_rows,
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
        source_text = source_path.read_text(encoding="utf-8", errors="ignore")
        for needle in source["needles"].split("|"):
            if needle not in source_text:
                return False
    return True


def csvs_parse() -> bool:
    csv_paths = list(CSV_BUILDERS.keys()) + ["P8_Y5_BRR545_2407_VALIDATION.csv"]
    for csv_name in csv_paths:
        csv_path = RESIDUALS / csv_name
        if not csv_path.exists():
            return False
        with csv_path.open(newline="", encoding="utf-8") as csv_file:
            parsed_rows = list(csv.DictReader(csv_file))
        if not parsed_rows:
            return False
    return True


def generated_rows() -> list[dict[str, str]]:
    return [
        *source_register_rows(),
        *zero_theorem_rows(),
        *stress_rows(),
        *bound_rows(),
        *envelope_rows(),
        *claim_gate_rows(),
        *refusal_rows(),
        *decision_rows(),
        *next_target_rows(),
    ]


def generated_text() -> str:
    return "\n".join(str(row) for row in generated_rows())


def no_claim_flags() -> bool:
    return all(
        str(row.get("valid_for_claim", "false")).lower() == "false"
        and str(row.get("claim_allowed", "false")).lower() == "false"
        for row in generated_rows()
    )


def all_bound_rows_nonclaim_missing_values() -> bool:
    rows = bound_rows()
    return len(rows) == 9 and all(row["score_ready"] == "false" and row["value"] == "MISSING_NUMERIC_VALUE" for row in rows)


def claims_blocked() -> bool:
    return all(row["status"] == "BLOCKED" for row in claim_gate_rows())


def formalization_untouched_by_outputs() -> bool:
    output_paths = [DOC_PATH, *(RESIDUALS / csv_name for csv_name in CSV_BUILDERS), RESIDUALS / "P8_Y5_BRR545_2407_VALIDATION.csv"]
    try:
        formalization_resolved = FORMALIZATION_ROOT.resolve()
    except FileNotFoundError:
        return True
    for output_path in output_paths:
        try:
            output_resolved = output_path.resolve()
        except FileNotFoundError:
            output_resolved = output_path.parent.resolve() / output_path.name
        if formalization_resolved == output_resolved or formalization_resolved in output_resolved.parents:
            return False
    return True


def validation_rows() -> list[dict[str, str]]:
    text = generated_text()
    checks = [
        {
            "row_id": "VAL2407_00_sources_exist",
            "status": "PASS" if sources_exist() else "FAIL",
            "detail": "all required source paths exist" if sources_exist() else "one or more source paths are missing",
        },
        {
            "row_id": "VAL2407_01_needles_found",
            "status": "PASS" if needles_found() else "FAIL",
            "detail": "all source needles found" if needles_found() else "one or more source needles are missing",
        },
        {
            "row_id": "VAL2407_02_conditional_chainmap_theorem",
            "status": "PASS" if "PZ2407_1_fixed_chainmap_lemma" in text and "CONDITIONAL_THEOREM_CLEAN" in text else "FAIL",
            "detail": "fixed chain-map zero theorem is recorded as conditional-clean",
        },
        {
            "row_id": "VAL2407_03_zero_not_promoted",
            "status": "PASS" if "PIM_COMMUTATOR_ZERO_NOT_PROVED" in text and "claim_allowed': 'false" in text else "FAIL",
            "detail": "current MTS Pi_M zero is not promoted",
        },
        {
            "row_id": "VAL2407_04_projector_stress_retained",
            "status": "PASS" if "PROJECTOR_STRESS_ZERO_NOT_PROVED" in text and "STRESS_RETAINED_IF_USED" in text else "FAIL",
            "detail": "projector variation stress remains retained unless topological no-stress is parent-signed",
        },
        {
            "row_id": "VAL2407_05_bound_rows_nonclaim",
            "status": "PASS" if all_bound_rows_nonclaim_missing_values() else "FAIL",
            "detail": "all nine Pi_M/epsilon_M bound rows remain nonclaim and missing numeric values",
        },
        {
            "row_id": "VAL2407_06_envelope_no_cancellation",
            "status": "PASS" if "ENV2407_0_no_cancellation" in text and "no cancellation credit" in text else "FAIL",
            "detail": "epsilon_M no-cancellation envelope is recorded",
        },
        {
            "row_id": "VAL2407_07_claims_blocked",
            "status": "PASS" if claims_blocked() else "FAIL",
            "detail": "commutator, projector stress, equality, finite bounds, and local GR gates are blocked",
        },
        {
            "row_id": "VAL2407_08_next_selected",
            "status": "PASS" if "NEXT2407_0_selected" in text and "topological-Hilbert" in text else "FAIL",
            "detail": "topological-Hilbert equality/R_eq zero route is selected next",
        },
        {
            "row_id": "VAL2407_09_csv_parse",
            "status": "PASS" if csvs_parse() else "FAIL",
            "detail": "generated CSVs parse and have rows",
        },
        {
            "row_id": "VAL2407_10_no_claim_flags",
            "status": "PASS" if no_claim_flags() else "FAIL",
            "detail": "no generated row has valid_for_claim=true or claim_allowed=true",
        },
        {
            "row_id": "VAL2407_11_formalization_untouched_by_outputs",
            "status": "PASS" if formalization_untouched_by_outputs() else "FAIL",
            "detail": "script outputs stay inside post-checkpoint-work",
        },
    ]
    overall = "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL"
    checks.append(
        {
            "row_id": "VAL2407_OVERALL",
            "status": overall,
            "detail": "2407 proves the Pi_M commutator route only conditionally, keeps projector/source residuals nonclaim, and selects topological-Hilbert equality/R_eq as the next bottleneck",
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
    body = f"""# 2407 - Projector Pi_M Commutator Variation Zero Or Operator Coefficient Bound

## Result

This checkpoint takes the 2406 best target seriously: can the `Pi_M` projector/source-readout obstruction be killed?

Answer: conditionally yes, currently no.

The clean theorem is:

`d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H`

so if `Pi_M` is a fixed parent-selected chain-map on the physical Hilbert-current complex, then `[d,Pi_M]J_H=0`.
If the same `Pi_M` is metric-independent topological data, then `delta_g Pi_M=0` and projector stress can vanish too.

But the live MTS branch does not yet parent-sign the necessary physical object clauses: the Hilbert current must be in
the same chain complex, the source worldtube/exterior annulus must be fixed before readout, the closed topological
current must equal the observed Hilbert source current up to zero-flux exact terms, and the same `M_H_ref/tau`
denominator must normalize the row.

So the algebra is not the enemy anymore.  The bottleneck is topological-Hilbert/source-worldtube equality.

## Source Register

{markdown_table(source_register_rows(), ["source_id", "source_path", "exists", "role", "valid_for_claim", "claim_allowed"])}

## Pi_M Zero Theorem Attempt

{markdown_table(zero_theorem_rows(), ["proof_id", "claim_piece", "mathematical_form", "status", "proof_result", "remaining_gap", "valid_for_claim", "claim_allowed"])}

## Projector Variation Stress Audit

{markdown_table(stress_rows(), ["stress_id", "object", "mathematical_form", "status", "local_effect", "required_for_zero", "valid_for_claim", "claim_allowed"])}

## Pi_M Coefficient Bound Pack

{markdown_table(bound_rows(), ["row_id", "symbol", "definition", "units", "status", "observable_link", "value", "source_path", "score_ready", "valid_for_claim", "claim_allowed"])}

## Epsilon_M Envelope

{markdown_table(envelope_rows(), ["envelope_id", "quantity", "formula", "rule", "status", "next_needed", "valid_for_claim", "claim_allowed"])}

## Claim Gates

{markdown_table(claim_gate_rows(), ["gate_id", "gate", "status", "blocker", "valid_for_claim", "claim_allowed"])}

## Refusal Runner

{markdown_table(refusal_rows(), ["row_id", "claim", "allowed", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger

{markdown_table(decision_rows(), ["decision_id", "decision", "reason", "consequence", "valid_for_claim", "claim_allowed"])}

## Next Target

{markdown_table(next_target_rows(), ["route_id", "next_doc", "why", "expected_output", "valid_for_claim", "claim_allowed"])}

## Validation

{markdown_table(validation_rows(), ["row_id", "status", "detail"])}

## Practical Status

This is progress, not circling.  We have pushed the `Pi_M` problem from "maybe the commutator vanishes?" to a sharper
contract:

`Pi_M J_H = J_M_top + dB_zero`, with zero compact boundary flux and the same parent-owned source worldtube/denominator.

If 2408 proves that, the projector/source-normalization obstruction can genuinely shrink.  If 2408 fails, the honest
move is not despair; it is a finite `epsilon_M` source-normalization residual that goes into empirical bounds.  No
GitHub/public claim is made here.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    for csv_name, builder in CSV_BUILDERS.items():
        write_csv(RESIDUALS / csv_name, builder())
    write_csv(RESIDUALS / "P8_Y5_BRR545_2407_VALIDATION.csv", validation_rows())
    write_csv(RESIDUALS / "P8_Y5_BRR545_2407_VALIDATION.csv", validation_rows())
    write_doc()
    print(f"wrote {DOC_PATH}")
    print(f"wrote {RESIDUALS / 'P8_Y5_BRR545_2407_VALIDATION.csv'}")


if __name__ == "__main__":
    main()
