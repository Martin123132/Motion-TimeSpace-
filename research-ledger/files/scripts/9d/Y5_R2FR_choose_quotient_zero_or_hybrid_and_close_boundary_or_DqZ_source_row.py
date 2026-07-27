from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1786"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1786_0_1785_handoff",
        "source_key": "1785_handoff_doc",
        "source_path": ROOT / "1785-Y5-R2FR-parent-Lagrangian-theta-vX-minimal-fill-or-DqZ-geometry-source-row.md",
        "needles": ["PLT1785_8_verdict", "DEC1785_3_best_next", "NEXT1785_0_primary"],
    },
    {
        "source_id": "SRC1786_1_1785_validation",
        "source_key": "1785_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1785_VALIDATION.csv",
        "needles": ["VAL1785_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1786_2_1785_route_matrix",
        "source_key": "1785_minimal_fill_route_matrix",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1785_MINIMAL_FILL_ROUTE_MATRIX.csv",
        "needles": ["MRM1785_0_strict_quotient_zero", "MRM1785_1_hybrid_EH_plus_quotient_extra"],
    },
    {
        "source_id": "SRC1786_3_1785_noether",
        "source_key": "1785_noether_pj_contract",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1785_NOETHER_PJ_CONTRACT_GATE.csv",
        "needles": ["NPJ1785_5_symplectic_flat_closure", "NPJ1785_6_verdict"],
    },
    {
        "source_id": "SRC1786_4_730_decision",
        "source_key": "730_decision_matrix",
        "source_path": RESIDUALS / "P8_Y5_R10_730_DECISION_MATRIX.csv",
        "needles": ["D730_2_best_routes_are_quotient_or_hybrid", "D730_4_edge_coefficients_still_missing"],
    },
    {
        "source_id": "SRC1786_5_670_no_pole",
        "source_key": "670_no_pole_quotient_chain",
        "source_path": RESIDUALS / "P8_Y5_R10_670_NO_POLE_QUOTIENT_PROOF_CHAIN.csv",
        "needles": ["NQ670_0_null_distribution", "NQ670_8_no_pole_result"],
    },
    {
        "source_id": "SRC1786_6_945_q_map",
        "source_key": "945_q_map_candidate",
        "source_path": RESIDUALS / "P8_Y5_R10_945_Q_MAP_CANDIDATE_CONSTRUCTION.csv",
        "needles": ["QMAP945_1_candidate_projection", "QMAP945_6_verdict"],
    },
    {
        "source_id": "SRC1786_7_945_obs_functor",
        "source_key": "945_obs_e_functor",
        "source_path": RESIDUALS / "P8_Y5_R10_945_OBS_E_FUNCTOR_AUDIT.csv",
        "needles": ["OBS945_0_projection_functor", "OBS945_6_verdict"],
    },
    {
        "source_id": "SRC1786_8_946_kernel",
        "source_key": "946_kernel_certificate",
        "source_path": RESIDUALS / "P8_Y5_R10_946_KERNEL_CERTIFICATE_AUDIT.csv",
        "needles": ["KCERT946_0_bulk_presymplectic_null", "KCERT946_6_total"],
    },
    {
        "source_id": "SRC1786_9_946_positive",
        "source_key": "946_partial_positive_register",
        "source_path": RESIDUALS / "P8_Y5_R10_946_PARTIAL_POSITIVE_REGISTER.csv",
        "needles": ["POS946_0_chain_rule", "POS946_3_source_cokernel"],
    },
    {
        "source_id": "SRC1786_10_1030_spm_contract",
        "source_key": "1030_public_metric_action_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_1030_PUBLIC_METRIC_ACTION_CONTRACT.csv",
        "needles": ["SPM1030_0_public_metric_object", "SPM1030_6_contract_verdict"],
    },
    {
        "source_id": "SRC1786_11_1030_spm_derivation",
        "source_key": "1030_single_public_metric_derivation",
        "source_path": RESIDUALS / "P8_Y5_R10_1030_SINGLE_PUBLIC_METRIC_DERIVATION_AUDIT.csv",
        "needles": ["SPD1030_5_quotient_naturality_route", "SPD1030_6_verdict"],
    },
    {
        "source_id": "SRC1786_12_1031_terminal_metric",
        "source_key": "1031_terminal_public_metric_audit",
        "source_path": RESIDUALS / "P8_Y5_R10_1031_TERMINAL_PUBLIC_METRIC_PROOF_AUDIT.csv",
        "needles": ["TPM1031_3_vertical_chain_rule", "TPM1031_6_verdict"],
    },
    {
        "source_id": "SRC1786_13_1031_decision",
        "source_key": "1031_decision_ledger",
        "source_path": RESIDUALS / "P8_Y5_R10_1031_DECISION_LEDGER.csv",
        "needles": ["DEC1031_0_terminality_status", "DEC1031_3_next_target"],
    },
    {
        "source_id": "SRC1786_14_956_source_side",
        "source_key": "956_source_side_gr_newton_spine",
        "source_path": RESIDUALS / "P8_Y5_R10_956_SOURCE_SIDE_GR_NEWTON_SPINE.csv",
        "needles": ["SSG956_0_observed_coframe", "SSG956_5_source_side_verdict"],
    },
    {
        "source_id": "SRC1786_15_956_left_hand",
        "source_key": "956_left_hand_eh_newton_gate",
        "source_path": RESIDUALS / "P8_Y5_R10_956_LEFT_HAND_EH_NEWTON_GATE_MAP.csv",
        "needles": ["LHG956_0_EH_core_selection", "LHG956_5_PPN_completion"],
    },
    {
        "source_id": "SRC1786_16_957_local_gr_spine",
        "source_key": "957_parent_local_gr_spine",
        "source_path": RESIDUALS / "P8_Y5_R10_957_PARENT_LOCAL_GR_SPINE_LEDGER.csv",
        "needles": ["PLG957_2_EH_operator", "PLG957_5_PPN_completion"],
    },
    {
        "source_id": "SRC1786_17_958_eh_core",
        "source_key": "958_eh_core_selection",
        "source_path": RESIDUALS / "P8_Y5_R10_958_EH_CORE_SELECTION_ATTEMPT.csv",
        "needles": ["EH958_1_Lovelock_route", "EH958_5_verdict"],
    },
    {
        "source_id": "SRC1786_18_959_no_extra_field",
        "source_key": "959_no_extra_field_clause",
        "source_path": RESIDUALS / "P8_Y5_R10_959_NO_EXTRA_FIELD_CLAUSE_ATTEMPT.csv",
        "needles": ["NEF959_0_target", "NEF959_5_verdict"],
    },
    {
        "source_id": "SRC1786_19_960_r2_fr",
        "source_key": "960_r2_fr_zero_or_bound",
        "source_path": RESIDUALS / "P8_Y5_R10_960_R2_FR_ZERO_OR_BOUND_ATTEMPT.csv",
        "needles": ["R2FR960_0_target", "R2FR960_4_verdict"],
    },
    {
        "source_id": "SRC1786_20_1555_first_class",
        "source_key": "1555_first_class_constraint_contract",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1555_FIRST_CLASS_CONSTRAINT_CONTRACT.csv",
        "needles": ["FCC1555_0_parent_phase_space", "FCC1555_7_no_GR_import"],
    },
    {
        "source_id": "SRC1786_21_1665_coupling_vertical",
        "source_key": "1665_coupling_vertical_generator",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1665_COUPLING_VERTICAL_GENERATOR_AUDIT.csv",
        "needles": ["CVG1665_3_Dq_verticality", "CVG1665_7_verdict"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1786_SOURCE_REGISTER.csv",
    "branch_choice_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1786_BRANCH_CHOICE_GATE.csv",
    "strict_quotient_zero_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1786_STRICT_QUOTIENT_ZERO_AUDIT.csv",
    "hybrid_eh_quotient_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1786_HYBRID_EH_QUOTIENT_AUDIT.csv",
    "boundary_matter_closure_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1786_BOUNDARY_MATTER_CLOSURE_GATE.csv",
    "dqz_source_row_plan": RESIDUALS / "P8_Y5_PARENT_QLOC_1786_DQZ_SOURCE_ROW_PLAN.csv",
    "countermodel_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1786_COUNTERMODEL_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1786_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1786_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1786_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1786_VALIDATION.csv",
}

DOC_PATH = ROOT / "1786-Y5-R2FR-choose-quotient-zero-or-hybrid-and-close-boundary-or-DqZ-source-row.md"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
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
                "exists": exists,
                "needles": ";".join(needles),
                "needles_present": exists and all(needle in text for needle in needles),
                "role": "1786 quotient-zero versus hybrid EH-plus-quotient branch selection evidence",
            }
        )
    return rows


def branch_choice_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "BCG1786_0_selection_rule",
            "question": "which local-GR route should be active after the parent-fill audit",
            "criterion": "prefer exact quotient-zero if q/kernel/action/matter/boundary all close; otherwise select hybrid EH-plus-quotient-extra and keep finite residual fallbacks",
            "evidence_basis": "1785 route matrix; 670 no-pole chain; 945/946 q-kernel audits; 956-960 EH/local-GR spine",
            "result": "RULE_WRITTEN_NONCLAIM",
            "selected_route": "not_yet",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "BCG1786_1_strict_quotient_zero_result",
            "question": "can strict quotient-zero be promoted now",
            "criterion": "q constructed, ker(Dq) parent-owned, action descends, matter/readout invisible, boundary charge silent, degree count closed",
            "evidence_basis": "NQ670_8; QMAP945_6; KCERT946_6; FCC1555_0 through FCC1555_7",
            "result": "FAILS_CURRENT_PROOF_GATE",
            "selected_route": "retained_as_ideal_theorem_target_not_active_claim",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "BCG1786_2_hybrid_result",
            "question": "is hybrid EH-plus-quotient-extra the better active derivation route",
            "criterion": "EH core can be used as conditional local operator spine while each MTS extra sector is forced to prove silence or become a bounded residual",
            "evidence_basis": "EH958_1; EH958_5; NEF959_2; PLG957_2; PLG957_3",
            "result": "SELECT_ACTIVE_DERIVATION_ROUTE_NONCLAIM",
            "selected_route": "hybrid_EH_plus_quotient_extra",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "BCG1786_3_fallback_result",
            "question": "what happens if hybrid extra-sector silence fails",
            "criterion": "retain Dq_Z, c_g, b_A, b_alpha, q_nonH, Delta_W_support, R2/fR, torsion/nonmetricity and PPN residuals as source-backed rows",
            "evidence_basis": "SPM1030_5; CPG1030_4; R2FR960_4; LHG956_5",
            "result": "FINITE_RESIDUAL_FALLBACK_STAGED",
            "selected_route": "fallback_not_primary",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "BCG1786_4_claim_ceiling",
            "question": "what can be claimed after 1786",
            "criterion": "route selection is not a local-GR proof; it only orders the next derivation",
            "evidence_basis": "all 1786 gates",
            "result": "NO_LOCAL_GR_OR_PPN_OR_R10_CLAIM",
            "selected_route": "hybrid_active_but_nonclaim",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def strict_quotient_zero_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SQA1786_0_q_candidate",
            "required_clause": "parent quotient map exists without projection-by-declaration",
            "mathematical_form": "q: Phi_parent -> Q_obs with observed geometry and physical quotient data",
            "current_evidence": "QMAP945_1 writes q_candidate and QMAP945_6 keeps it candidate-only",
            "status": "CANDIDATE_ONLY",
            "blocker": "field inventory is not a variational parent action and kernel ownership is not proved",
            "exit_condition": "q emerges from parent action/gauge reduction rather than being declared",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SQA1786_1_kernel_ownership",
            "required_clause": "ker(Dq) is a physical gauge/null distribution",
            "mathematical_form": "v in ker(Dq) and i_v Omega_parent=0, with no marker/frame/material leakage",
            "current_evidence": "KCERT946_0 partial conditional; KCERT946_6 certificate failed",
            "status": "KERNEL_CERTIFICATE_FAILED_CURRENT_CORPUS",
            "blocker": "presymplectic null, no-marker, matter invisibility, and boundary silence do not all close",
            "exit_condition": "all kernel certificate clauses pass in one parent branch",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SQA1786_2_action_descent",
            "required_clause": "bulk action descends through q",
            "mathematical_form": "S_bulk[Phi] = S_red[q(Phi)] + boundary/domain terms",
            "current_evidence": "NQ670_3 gives conditional action descent only",
            "status": "ACTION_DESCENT_CONDITIONAL_ONLY",
            "blocker": "parent Lagrangian, boundary/domain terms, and Hessian degeneracy are not signed",
            "exit_condition": "derive descent by varying the signed parent action along v in ker(Dq)",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SQA1786_3_matter_descent",
            "required_clause": "ordinary matter/readout is blind to quotient-vertical directions",
            "mathematical_form": "S_matter = Sbar_m[Obs(q(Phi)), psi, theta] and Lie_v S_matter=0",
            "current_evidence": "POS946_0 and POS946_3 are exact conditional theorems; OBS945_6 says formal only",
            "status": "MATTER_DESCENT_NOT_PARENT_SIGNED",
            "blocker": "representative Weyl/disformal frames, constants, material markers, and readout labels remain legal counterexamples",
            "exit_condition": "parent matter-interface functor excludes representative slots and marker constants",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SQA1786_4_boundary_degree",
            "required_clause": "vertical direction has zero local boundary charge and removes degrees of freedom",
            "mathematical_form": "Q_X=0 or exact/proper, bracket first-class, no edge cocycle, degree count closed",
            "current_evidence": "NQ670_7 and FCC1555 rows keep boundary/bracket/degree count missing",
            "status": "BOUNDARY_AND_DEGREE_NOT_CLOSED",
            "blocker": "differentiable zero charge, bracket closure, no edge mode, and phase-space count are still missing",
            "exit_condition": "parent Hamiltonian/Noether generator has zero/proper Q_X and a first-class closed algebra",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SQA1786_5_verdict",
            "required_clause": "strict quotient-zero is the active local-GR route",
            "mathematical_form": "SQA1786_0 through SQA1786_4 all close",
            "current_evidence": "q math is useful but current certificate fails",
            "status": "STRICT_QUOTIENT_ZERO_NOT_SELECTED_AS_ACTIVE_ROUTE",
            "blocker": "too many unsigned global clauses for current proof path",
            "exit_condition": "reopen if a parent q/kernel/matter/boundary certificate is later derived",
            "parent_signed": False,
            "valid_for_claim": False,
        },
    ]


def hybrid_eh_quotient_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "HQA1786_0_EH_core",
            "required_clause": "local exterior operator has an EH core",
            "mathematical_form": "S_local[g_obs]=int sqrt(-g)(a R - 2 Lambda)+boundary when metric-only second-order premises hold",
            "current_evidence": "EH958_1 Lovelock route is mathematically clean conditional",
            "status": "CONDITIONAL_EH_CORE_AVAILABLE",
            "why_route_survives": "the EH baseline gives a disciplined local-GR target without pretending extra sectors are already dead",
            "remaining_gap": "metric-only, second-order, no-extra-sector premises are not parent-derived",
            "selected_for_active_derivation": "yes_nonclaim",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "HQA1786_1_extra_sector_filter",
            "required_clause": "every non-EH MTS sector is zero, gauge, topological/no-flux, positive source-free silent, or retained as residual",
            "mathematical_form": "DeltaE_extra_i in {0,gauge,topological_no_flux,positive_source_free_silent,retained_bound}",
            "current_evidence": "NEF959_2 exact filter; EH958_2 central obstruction",
            "status": "FILTER_EXACT_INPUTS_MISSING",
            "why_route_survives": "it turns derivation failure into named residual rows rather than handwaving",
            "remaining_gap": "field-specific operators, signs, source charges, and boundary data are not all supplied",
            "selected_for_active_derivation": "yes_nonclaim",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "HQA1786_2_source_side",
            "required_clause": "right-hand source side uses one common observed matter/source geometry",
            "mathematical_form": "source side = kappa_univ T_total + DeltaJ_hidden + DeltaJ_species",
            "current_evidence": "SSG956_0 through SSG956_5 are a sharp conditional spine",
            "status": "SOURCE_SIDE_CONDITIONAL_NOT_CLAIM",
            "why_route_survives": "it separates source-frame/coupling work from left-hand EH operator work",
            "remaining_gap": "DeltaJ_hidden and DeltaJ_species must be theorem-zero or bounded",
            "selected_for_active_derivation": "yes_nonclaim",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "HQA1786_3_public_metric_guard",
            "required_clause": "ordinary matter has no shadow-frame or representative-field slot",
            "mathematical_form": "Allowed[S_matter] excludes A_g(Xhat)e_pub, B_g(Xhat), U_mu and marker constants unless quotient-owned",
            "current_evidence": "SPM1030 contract is written; TPM1031_6 says terminal proof not derived",
            "status": "CLOSURE_AVAILABLE_NOT_PARENT_THEOREM",
            "why_route_survives": "can be used as explicit closure language while derivation continues",
            "remaining_gap": "terminal public metric plus matter-interface functor and field-rename guard are not parent-signed",
            "selected_for_active_derivation": "yes_nonclaim",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "HQA1786_4_R2_fR_priority",
            "required_clause": "R2/fR scalar-mode family is killed or retained with bounds",
            "mathematical_form": "c_R2=c_fR=0 theorem OR scalar mass/coupling bound rows",
            "current_evidence": "R2FR960_4 not closed",
            "status": "PRIORITY_RESIDUAL_FAMILY_RETAINED",
            "why_route_survives": "hybrid route can explicitly score this family instead of claiming EH too early",
            "remaining_gap": "no zero theorem and no sourced weak-field alpha/PPN row yet",
            "selected_for_active_derivation": "yes_nonclaim",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "HQA1786_5_verdict",
            "required_clause": "hybrid EH-plus-quotient-extra is the active route",
            "mathematical_form": "EH core conditional plus extra-sector silence/bound filter plus source-side frame guard",
            "current_evidence": "1785/730 route fork plus 956-960 local-GR spine",
            "status": "HYBRID_SELECTED_AS_ACTIVE_DERIVATION_ROUTE_NONCLAIM",
            "why_route_survives": "least-bad route: mathematically standard EH core, no smuggled quotient-zero axiom, and explicit residual discipline",
            "remaining_gap": "must derive or bound extra-sector residuals before local-GR/Newton claim",
            "selected_for_active_derivation": "yes_nonclaim",
            "valid_for_claim": False,
        },
    ]


def boundary_matter_closure_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "closure_id": "BMC1786_0_boundary_representative",
            "needed_for": "both quotient-zero and hybrid routes",
            "mathematical_form": "j_X -> j_X+dU_X, Q_X fixed by differentiable variational problem and no improper local edge mode",
            "current_status": "BOUNDARY_REPRESENTATIVE_OPEN",
            "blocker": "Q_X/improvement freedom can move edge coefficients",
            "next_action": "derive parent boundary term or retain K_edge/Qbar rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "closure_id": "BMC1786_1_matter_interface",
            "needed_for": "ordinary local-GR source side",
            "mathematical_form": "S_matter: Q_obs x MatterFields x Theta_Q -> R, not S_matter[Phi_rep]",
            "current_status": "MATTER_INTERFACE_NOT_PARENT_SIGNED",
            "blocker": "terminality alone does not stop matter using non-terminal frame labels",
            "next_action": "derive no-extra-matter-frame domain or mark SPM as closure",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "closure_id": "BMC1786_2_field_rename_guard",
            "needed_for": "no hidden coupling migration",
            "mathematical_form": "no A_g hidden as theta_A, alpha_EM, G_eff, T_total, support, clock, or source normalization",
            "current_status": "FIELD_RENAME_GUARD_OPEN",
            "blocker": "constants and material markers remain live counterexamples",
            "next_action": "classify constants as quotient-owned, superselected, or finite residual coefficients",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "closure_id": "BMC1786_3_hidden_current_support",
            "needed_for": "GR/Newton source term",
            "mathematical_form": "DeltaJ_hidden = q_nonH + Delta_W_support + boundary/domain source tails = 0 or bounded",
            "current_status": "HIDDEN_CURRENT_RETAINED",
            "blocker": "source support/local projection theorem is not closed",
            "next_action": "derive zero-current theorem or source finite rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "closure_id": "BMC1786_4_measured_GM_PPN",
            "needed_for": "Newtonian mechanics and local tests",
            "mathematical_form": "mu_EH = mu_obs = G_ref M_H[Pi_M J_H] and gamma=1,beta=1,alpha_i=0,xi=0 plus bounded residual vector",
            "current_status": "MEASURED_GM_AND_PPN_OPEN",
            "blocker": "worldtube charge transfer, source calibration, and residual vector are not all theorem-zero/scored",
            "next_action": "after hybrid split, run measured-GM/PPN residual vector gate",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "closure_id": "BMC1786_5_verdict",
            "needed_for": "local-GR/Newton claim",
            "mathematical_form": "BMC1786_0 through BMC1786_4 close",
            "current_status": "BOUNDARY_MATTER_CLOSURE_NOT_CLOSED",
            "blocker": "claim remains blocked even though active route is selected",
            "next_action": "1787 hybrid split must attack extra-sector silence first",
            "valid_for_claim": False,
        },
    ]


def dqz_source_row_plan_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DZF1786_0_DqZ_geometry",
            "component": "Dq_Z geometry leakage",
            "reason_retained": "strict quotient-zero did not close and hybrid extra-sector silence is not yet signed",
            "required_input": "epsilon_Z_geom, norm bridge, arena projection",
            "current_status": "MISSING_DQZ_GEOMETRY_VALUE",
            "valid_prediction_row": False,
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DZF1786_1_shadow_frame",
            "component": "c_g / representative Weyl-disformal leakage",
            "reason_retained": "SPM/terminal public metric is closure-only, not a parent theorem",
            "required_input": "c_g theorem-zero or finite tau/source row",
            "current_status": "MISSING_PARENT_THEOREM_OR_NUMERIC_CG",
            "valid_prediction_row": False,
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DZF1786_2_material_constants",
            "component": "b_A / b_alpha marker leakage",
            "reason_retained": "matter/constant quotient ownership is not parent-signed",
            "required_input": "constant superselection theorem or finite clock/WEP/source coefficient rows",
            "current_status": "MISSING_CONSTANT_MARKER_OWNER",
            "valid_prediction_row": False,
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DZF1786_3_nonEH_operator",
            "component": "R2/fR, torsion/nonmetricity, scalar/vector/domain residuals",
            "reason_retained": "metric-only second-order no-extra-field premise is not derived",
            "required_input": "zero theorem or weak-field coefficient and bound projection per family",
            "current_status": "MISSING_NON_EH_ZERO_OR_BOUND_INPUTS",
            "valid_prediction_row": False,
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DZF1786_4_local_envelope",
            "component": "absolute local residual envelope",
            "reason_retained": "no cancellation between unknown residual families is allowed",
            "required_input": "all retained rows theorem-zero or source-backed numeric below bounds",
            "current_status": "MISSING_ABSOLUTE_ENVELOPE",
            "valid_prediction_row": False,
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def countermodel_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1786_0_projection_declaration",
            "countermodel": "put e_obs inside q by declaration, then treat all excluded directions as gauge",
            "survives_current_constraints": True,
            "why_survives": "QMAP945 warns that projection is not kernel/null proof",
            "what_kills_it": "derive q and ker(Dq) from parent gauge reduction and symplectic null certificate",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1786_1_terminality_insufficient",
            "countermodel": "terminal public metric exists but matter action depends on non-terminal frame before mapping",
            "survives_current_constraints": True,
            "why_survives": "TPM1031_5 shows terminality alone is not an action-domain exclusion",
            "what_kills_it": "parent signs matter-interface functor through terminal e_pub only",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1786_2_EH_plus_hidden_extra",
            "countermodel": "EH core is present but omega_extra or DeltaE_extra carries local charge/stress",
            "survives_current_constraints": True,
            "why_survives": "EH958_4 and PLG957_3 retain extra-sector obstruction",
            "what_kills_it": "extra sectors are proved gauge/topological/no-flux/source-free silent or bounded below local limits",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1786_3_common_frame_coupling",
            "countermodel": "common conformal/shadow frame coupling evades WEP composition tests but still affects PPN/clocks/source normalization",
            "survives_current_constraints": True,
            "why_survives": "SPD1030_2 says WEP does not unconditionally imply c_g=0",
            "what_kills_it": "no-shadow-frame theorem or finite c_g row passing PPN/clock/R10 bounds",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1786_4_newton_shape_not_GM",
            "countermodel": "field equation has Newton-like shape but exterior mass parameter is not measured orbital GM",
            "survives_current_constraints": True,
            "why_survives": "LHG956_3 keeps measured-GM calibration open",
            "what_kills_it": "Noether/Hamiltonian charge inheritance and worldtube source-measure calibration",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1786_0_strict_quotient_zero_claim",
            "claim": "strict quotient-zero local-GR branch is derived",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "kernel, matter, boundary, and first-class certificates failed/currently missing",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1786_1_hybrid_local_gr_claim",
            "claim": "hybrid EH-plus-quotient-extra proves local GR/Newton",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "extra-sector silence, measured-GM calibration, and PPN residual vector remain open",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1786_2_spm_theorem_claim",
            "claim": "single public metric/no-shadow-frame is parent-derived",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "terminal public metric proof is closure-only without matter-interface domain derivation",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1786_3_finite_residual_score_claim",
            "claim": "Dq_Z/c_g/nonEH finite residual rows are score-ready",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "missing numeric coefficients, units, source paths, and arena projections",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1786_4_public_or_github_claim",
            "claim": "publishable public local-GR claim follows from this route choice",
            "gate_pass": False,
            "status": "REFUSED",
            "blocker": "1786 is private route selection and proof targeting only",
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1786_0_strict_q_status",
            "decision": "STRICT_QUOTIENT_ZERO_NOT_ACTIVE_ROUTE_NOW",
            "reason": "q/kernel/action/matter/boundary conditions are exact as a contract but fail current parent certificates",
            "next_action": "retain as ideal theorem target; do not use as axiom",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1786_1_hybrid_status",
            "decision": "HYBRID_EH_PLUS_QUOTIENT_EXTRA_SELECTED_NONCLAIM",
            "reason": "best current route to derived GR: conditional EH core plus explicit proof-or-bound discipline for every extra sector",
            "next_action": "write hybrid local action split and extra-sector silence gate",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1786_2_spm_policy",
            "decision": "SPM_USED_AS_CLOSURE_UNTIL_PARENT_DERIVED",
            "reason": "terminal public metric and no-shadow-frame are useful but not derived by terminality alone",
            "next_action": "keep SPM as explicit closure branch or prove matter-interface functor",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1786_3_fallback_policy",
            "decision": "FINITE_RESIDUAL_ROWS_RETAINED_WITH_NO_CANCELLATION",
            "reason": "unknown extra families cannot be allowed to cancel each other; each must be zeroed or bounded",
            "next_action": "if 1787 cannot silence a sector, create source-backed residual row",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1786_0_primary",
            "next_target": "1787-Y5-R2FR-hybrid-EH-plus-quotient-extra-local-action-split-and-extra-sector-silence.md",
            "script": "scripts/Y5_R2FR_hybrid_EH_plus_quotient_extra_local_action_split_and_extra_sector_silence.py",
            "objective": "construct the hybrid local branch S_local = S_EH[e_obs] + S_extra and prove each extra-sector contribution is quotient-vertical, gauge, topological/no-flux, positive source-free silent, or retained as a finite residual",
            "selection_status": "selected",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1786_1_secondary",
            "next_target": "1787b-Y5-R2FR-single-public-metric-matter-interface-functor-or-closure-label.md",
            "script": "scripts/Y5_R2FR_single_public_metric_matter_interface_functor_or_closure_label.py",
            "objective": "try to derive the matter-interface/no-shadow-frame clause; otherwise label it as explicit closure and source c_g residual rows",
            "selection_status": "queued_after_1787_split",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1786_2_fallback",
            "next_target": "1787c-Y5-R2FR-DqZ-cg-nonEH-local-residual-source-row-pack.md",
            "script": "scripts/Y5_R2FR_DqZ_cg_nonEH_local_residual_source_row_pack.py",
            "objective": "prepare source-backed nonclaim rows for Dq_Z geometry, c_g, constant markers, R2/fR, torsion/nonmetricity, and PPN residual envelope",
            "selection_status": "deferred_until_silence_attempt_fails",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "branch_choice_gate": branch_choice_gate_rows(),
        "strict_quotient_zero_audit": strict_quotient_zero_audit_rows(),
        "hybrid_eh_quotient_audit": hybrid_eh_quotient_audit_rows(),
        "boundary_matter_closure_gate": boundary_matter_closure_gate_rows(),
        "dqz_source_row_plan": dqz_source_row_plan_rows(),
        "countermodel_ledger": countermodel_ledger_rows(),
        "claim_gate": claim_gate_rows(),
        "decision_ledger": decision_ledger_rows(),
        "next_target": next_target_rows(),
    }


def fieldnames_for(rows: list[dict[str, Any]]) -> list[str]:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    return fieldnames


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames_for(rows))
        writer.writeheader()
        writer.writerows(rows)


def copy_outputs() -> None:
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        shutil.copy2(path, MICROSCOPE_RESIDUALS / path.name)
        shutil.copy2(path, QUARANTINE / path.name)
        shutil.copy2(path, RAB_QUEUE / f"JR1786_{key.upper()}.csv")


def boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"1", "true", "yes", "y", "pass", "passed"}


def sources_ok(rows_map: dict[str, list[dict[str, Any]]]) -> tuple[bool, bool]:
    rows = rows_map["source_register"]
    return (
        all(boolish(row["exists"]) for row in rows),
        all(boolish(row["needles_present"]) for row in rows),
    )


def parse_csv(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except csv.Error:
        return False


def generated_csvs() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            for flag in (
                "valid_for_claim",
                "claim_allowed",
                "score_ready",
                "accepted_for_scoring",
                "theorem_closed_for_claim",
                "parent_signed",
                "valid_prediction_row",
                "gate_pass",
            ):
                if flag in row and boolish(row[flag]):
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            text = " ".join(str(value) for value in row.values()).upper()
            if "MISSING" in text:
                for flag in (
                    "valid_for_claim",
                    "claim_allowed",
                    "score_ready",
                    "accepted_for_scoring",
                    "theorem_closed_for_claim",
                    "valid_prediction_row",
                    "gate_pass",
                ):
                    if boolish(row.get(flag, False)):
                        return False
    return True


def branch_copies_exist() -> bool:
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        if not (MICROSCOPE_RESIDUALS / path.name).exists():
            return False
        if not (QUARANTINE / path.name).exists():
            return False
        if not (RAB_QUEUE / f"JR1786_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    generated_names = {path.name for path in OUTPUTS.values()}
    generated_names.add(DOC_PATH.name)
    return not any(path.name in generated_names for path in FORMALIZATION.rglob("*"))


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    exists_ok, needles_ok = sources_ok(rows_map)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1786_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1786_1_needles_present", needles_ok, "required source needles are present"),
        (
            "VAL1786_2_branch_choice_written",
            any(
                row["gate_id"] == "BCG1786_2_hybrid_result"
                and row["result"] == "SELECT_ACTIVE_DERIVATION_ROUTE_NONCLAIM"
                for row in rows_map["branch_choice_gate"]
            )
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["branch_choice_gate"]),
            "branch choice selects hybrid route without claim",
        ),
        (
            "VAL1786_3_strict_q_not_promoted",
            any(
                row["audit_id"] == "SQA1786_5_verdict"
                and row["status"] == "STRICT_QUOTIENT_ZERO_NOT_SELECTED_AS_ACTIVE_ROUTE"
                for row in rows_map["strict_quotient_zero_audit"]
            )
            and all(not boolish(row["parent_signed"]) and not boolish(row["valid_for_claim"]) for row in rows_map["strict_quotient_zero_audit"]),
            "strict quotient-zero is audited and not promoted",
        ),
        (
            "VAL1786_4_hybrid_selected_nonclaim",
            any(
                row["audit_id"] == "HQA1786_5_verdict"
                and row["status"] == "HYBRID_SELECTED_AS_ACTIVE_DERIVATION_ROUTE_NONCLAIM"
                for row in rows_map["hybrid_eh_quotient_audit"]
            )
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["hybrid_eh_quotient_audit"]),
            "hybrid route is selected but remains nonclaim",
        ),
        (
            "VAL1786_5_boundary_matter_blockers_retained",
            any(
                row["closure_id"] == "BMC1786_5_verdict"
                and row["current_status"] == "BOUNDARY_MATTER_CLOSURE_NOT_CLOSED"
                for row in rows_map["boundary_matter_closure_gate"]
            ),
            "boundary/matter closure blockers remain explicit",
        ),
        (
            "VAL1786_6_dqz_fallback_nonclaim",
            all(
                not boolish(row["valid_for_claim"])
                and not boolish(row["score_ready"])
                and not boolish(row["valid_prediction_row"])
                for row in rows_map["dqz_source_row_plan"]
            ),
            "Dq_Z/source fallback rows are not score-ready and nonclaim",
        ),
        (
            "VAL1786_7_countermodels_retained",
            all(boolish(row["survives_current_constraints"]) for row in rows_map["countermodel_ledger"]),
            "countermodels remain live",
        ),
        (
            "VAL1786_8_claim_gates_blocked",
            all(
                not boolish(row["valid_for_claim"])
                and not boolish(row["gate_pass"])
                and row["status"] in {"BLOCKED", "REFUSED"}
                for row in rows_map["claim_gate"]
            ),
            "claim gates are blocked or refused",
        ),
        ("VAL1786_9_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1786_10_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1786_11_decision_next",
            any(
                row["decision_id"] == "DEC1786_1_hybrid_status"
                and row["decision"] == "HYBRID_EH_PLUS_QUOTIENT_EXTRA_SELECTED_NONCLAIM"
                for row in rows_map["decision_ledger"]
            ),
            "decision selects hybrid split next",
        ),
        (
            "VAL1786_12_next_selected",
            any(row["route_id"] == "NEXT1786_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1786_13_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1786 CSVs parse"),
        ("VAL1786_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1786_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1786_16_formalization_untouched", formalization_untouched(), "no 1786 outputs found under formalization-workbench"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1786_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1786 quotient-zero versus hybrid EH-plus-quotient branch-choice checkpoint",
        }
    )
    return rows


def clean_cell(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "/")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(clean_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, str]]) -> str:
    return "\n".join(
        [
            "# 1786 - Y5/R2FR Choose Quotient-Zero or Hybrid and Close Boundary or DqZ Source Row",
            "",
            "## Verdict",
            "",
            "1786 makes the branch choice explicit. Strict quotient-zero remains the clean ideal theorem, but the current corpus cannot promote it: the q-map is still candidate-only, the kernel certificate fails, action/matter descent are conditional, and boundary/degree closure is unsigned.",
            "",
            "The active route is now the hybrid `EH core + quotient-owned MTS extra sector` branch. This is not a claim of local GR. It is the disciplined route because the EH core gives a known conditional local operator target, while every MTS extra sector must either prove silence or be retained as a finite residual row.",
            "",
            "**Claim ceiling:** no strict quotient-zero claim, no derived local-GR/Newton/PPN/R10 claim, no finite residual score, no GitHub action, and no `formalization-workbench` edit is allowed from 1786.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## Branch Choice Gate",
            markdown_table(rows_map["branch_choice_gate"], ["gate_id", "question", "criterion", "result", "selected_route", "claim_allowed", "valid_for_claim"]),
            "",
            "## Strict Quotient-Zero Audit",
            markdown_table(rows_map["strict_quotient_zero_audit"], ["audit_id", "required_clause", "mathematical_form", "current_evidence", "status", "blocker", "exit_condition", "valid_for_claim"]),
            "",
            "## Hybrid EH-Quotient Audit",
            markdown_table(rows_map["hybrid_eh_quotient_audit"], ["audit_id", "required_clause", "mathematical_form", "current_evidence", "status", "why_route_survives", "remaining_gap", "selected_for_active_derivation", "valid_for_claim"]),
            "",
            "## Boundary and Matter Closure Gate",
            markdown_table(rows_map["boundary_matter_closure_gate"], ["closure_id", "needed_for", "mathematical_form", "current_status", "blocker", "next_action", "valid_for_claim"]),
            "",
            "## DqZ Source Row Plan",
            markdown_table(rows_map["dqz_source_row_plan"], ["row_id", "component", "reason_retained", "required_input", "current_status", "score_ready", "valid_for_claim"]),
            "",
            "## Countermodel Ledger",
            markdown_table(rows_map["countermodel_ledger"], ["countermodel_id", "countermodel", "survives_current_constraints", "why_survives", "what_kills_it"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "status", "blocker", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            markdown_table(rows_map["decision_ledger"], ["decision_id", "decision", "reason", "next_action"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is a good pivot, not a retreat. The strict route would be the knockout, but it currently asks the theory to prove too much at once. The hybrid route is the Mayweather version: use the clean EH core as the ring, make every extra MTS sector show its papers, and only score what survives the proof-or-bound gate.",
            "",
        ]
    )


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1786 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
