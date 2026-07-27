from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
MICROSCOPE_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1837"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
P4_RUN = ROOT / "runs" / "20260602-141500-metric-compatibility-Levi-Civita-or-R11-connection-row" / "results"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1837-Y5-R2FR-PWEP-response-operator-from-matter-functor-or-component-bound-row.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1837_0_1836_next",
        "source_key": "1836_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1836_NEXT_TARGET.csv",
        "needles": ["NEXT1836_0_primary", "selected"],
        "role": "1836 selects P_WEP response operator from matter functor as the primary next target.",
    },
    {
        "source_id": "SRC1837_1_1836_validation",
        "source_key": "1836_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1836_VALIDATION.csv",
        "needles": ["VAL1836_OVERALL", "PASS"],
        "role": "confirms the 1836 WEP/clock/lightcone skeleton passed as a nonclaim checkpoint.",
    },
    {
        "source_id": "SRC1837_2_1836_skeleton",
        "source_key": "1836_projection_skeleton",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1836_WEP_CLOCK_LIGHTCONE_PROJECTION_SKELETON.csv",
        "needles": ["P1836_WEP_0_eta_total", "MISSING_WEP_PROJECTION_MATRIX"],
        "role": "defines the missing WEP response operator and its blockers.",
    },
    {
        "source_id": "SRC1837_3_1045_matter_functor",
        "source_key": "1045_parent_matter_functor",
        "source_path": ROOT / "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md",
        "needles": ["MFS1045_2_matter_bundle_functor", "MATTER_CATEGORY_NOT_PARENT_CONSTRUCTED"],
        "role": "matter functor descent is exact in shape but not parent-signed.",
    },
    {
        "source_id": "SRC1837_4_1155_coframe",
        "source_key": "1155_single_observed_coframe",
        "source_path": ROOT / "1155-Y5-R10-single-observed-coframe-source-frame-owner-or-frame-residual-row.md",
        "needles": ["COF1155_3_geometry_stack", "SINGLE_OBSERVED_COFRAME_NOT_DERIVED"],
        "role": "same observed coframe/source/readout stack remains unsigned.",
    },
    {
        "source_id": "SRC1837_5_1561_matter_descent",
        "source_key": "1561_matter_gate",
        "source_path": ROOT / "1561-Y5-minimal-parent-weak-field-action-ansatz-and-Euler-Ward-PPN-gate.md",
        "needles": ["EUL1561_4_matter", "OPEN_MATTER_DESCENT"],
        "role": "minimal weak-field ansatz leaves universal matter descent open.",
    },
    {
        "source_id": "SRC1837_6_537_source_frame",
        "source_key": "537_source_frame_contract",
        "source_path": ROOT / "537-Y5-Hilbert-worldtube-parent-action-contract-or-PiM-input-fill.md",
        "needles": ["PAC537_1_single_observed_source_frame", "not_yet_derived"],
        "role": "source frame and Hilbert worldtube glue are contract-only.",
    },
    {
        "source_id": "SRC1837_7_1009_universal_matter",
        "source_key": "1009_parent_current_chain",
        "source_path": ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
        "needles": ["PCS1009_2_universal_matter", "no species-dependent extra coupling"],
        "role": "universal matter block is a conditional source input, not an adopted parent theorem.",
    },
    {
        "source_id": "SRC1837_8_1077_WEP_owner",
        "source_key": "1077_WEP_coupling_owner",
        "source_path": RESIDUALS / "P8_Y5_R10_1077_PARENT_WEP_COUPLING_OWNER_THEOREM_ATTEMPT.csv",
        "needles": ["WCO1077_1_conditional_theorem", "THEOREM_ZERO_NOT_CLOSED_CURRENT_CORPUS"],
        "role": "prior WEP owner theorem gives a clean conditional P_WEP=0 theorem but refuses the current claim.",
    },
    {
        "source_id": "SRC1837_9_1485_double_zero",
        "source_key": "1485_universal_matter_double_zero",
        "source_path": MICROSCOPE / "quarantine" / "1485" / "UNIVERSAL_MATTER_DOUBLE_ZERO_ATTEMPT_NONCLAIM.csv",
        "needles": ["DZ1485_0_exact_neighbourhood_theorem", "PROOF_SHARPENED_NOT_CLOSED"],
        "role": "neighbourhood quotient descent gives exact double zero if parent-signed.",
    },
    {
        "source_id": "SRC1837_10_branch_lock",
        "source_key": "same_parent_branch_lock",
        "source_path": MICROSCOPE / "branch_classifier" / "P_WEP_same_parent_branch_lock.csv",
        "needles": ["forbidden_mixing_rule", "BRANCH_CLASSIFIER_FIRST_FILL_NONCLAIM"],
        "role": "prevents mixed-basis WEP coefficient rows from becoming predictions.",
    },
    {
        "source_id": "SRC1837_11_eta_convention",
        "source_key": "eta_product_convention",
        "source_path": MICROSCOPE / "product_convention" / "P_WEP_eta_product_convention.csv",
        "needles": ["eta(A,B)=2(a_A-a_B)/(a_A+a_B)", "PRODUCT_CONVENTION_OFFICIAL_PARTIAL_EXTRACTION_NONCLAIM"],
        "role": "records the nonclaim Ti/Pt eta convention and readout/product missing pieces.",
    },
    {
        "source_id": "SRC1837_12_MICROSCOPE_provenance",
        "source_key": "1069_MICROSCOPE_provenance",
        "source_path": RESIDUALS / "P8_Y5_R10_1069_MICROSCOPE_PROVENANCE_LEDGER.csv",
        "needles": ["PROV1069_1_R0_direct_geometry", "PhysRevLett.129.121102"],
        "role": "source-backed MICROSCOPE Ti/Pt bound anchor, still nonclaim for MTS prediction rows.",
    },
    {
        "source_id": "SRC1837_13_tau_WEP_schema",
        "source_key": "1067_tau_WEP_schema",
        "source_path": RESIDUALS / "P8_Y5_R10_1067_TAU_WEP_ACQUISITION_SCHEMA.csv",
        "needles": ["TAQ1067_0_tau_zero_option", "MISSING_THEOREM_ZERO"],
        "role": "tau_WEP/product rows remain missing unless theorem-zero or numeric projection is sourced.",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1837_SOURCE_REGISTER.csv",
    "PWEP_derivation_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1837_PWEP_DERIVATION_ATTEMPT.csv",
    "response_contract": RESIDUALS / "P8_Y5_PARENT_QLOC_1837_PWEP_RESPONSE_CONTRACT.csv",
    "component_bound_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1837_WEP_COMPONENT_BOUND_ROWS.csv",
    "current_corpus_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1837_CURRENT_CORPUS_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1837_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1837_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1837_VALIDATION.csv",
}


def ensure_dirs() -> None:
    for directory in [RESIDUALS, MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
        directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        exists = path.exists()
        text = read_text(path) if exists else ""
        missing_needles = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": exists,
                "needles": ";".join(source["needles"]),
                "needles_present": exists and not missing_needles,
                "missing_needles": ";".join(missing_needles),
                "role": source["role"],
            }
        )
    return rows


def PWEP_derivation_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PWD1837_0_target",
            "claim_piece": "P_WEP response operator",
            "formal_statement": "For ordinary matter species A,B, eta_AB = n_mu[(a_A^mu-a_B^mu)]/g_N = P_WEP_eta_AB · DeltaGamma_WEP.",
            "proof_move": "derive the species acceleration from the descended matter action and subtract A-B before inserting any empirical bound",
            "current_status": "TARGET_DEFINED",
            "missing_for_parent_claim": "P_WEP_eta_AB must be derived from parent matter functor and readout, not fitted",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PWD1837_1_conditional_zero_theorem",
            "claim_piece": "universal observed matter descent gives P_WEP=0",
            "formal_statement": "If every ordinary S_A factors as Sbar_A[Psi_A,e_obs(q(Phi)),omega[e_obs],theta_A] with quotient-owned constants and no independent Gamma/source-only species selector, then a_A^mu=a_B^mu for structureless test bodies and P_WEP_eta_AB=0.",
            "proof_move": "chain rule gives delta_v e_obs=0 for vertical representatives; minimal observed-metric Euler equation is species-blind; subtracting A-B kills the common mode",
            "current_status": "EXACT_CONDITIONAL_THEOREM",
            "missing_for_parent_claim": "matter category, no-shadow-frame, constants/current owner and source/readout closure are unsigned",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PWD1837_2_response_decomposition",
            "claim_piece": "non-universal leakage decomposition",
            "formal_statement": "a_A^mu-a_B^mu = (P_A^spin-P_B^spin)DeltaGamma_spin + (P_A^mat-P_B^mat)DeltaGamma_material + (P_A^clock-P_B^clock)DeltaGamma_clock + (P_A^proj-P_B^proj)DeltaGamma_projective + Delta_frame/readout.",
            "proof_move": "retain every species-dependent variation channel as a linearized response coefficient until a parent theorem kills it",
            "current_status": "FORMAL_DECOMPOSITION_WRITTEN",
            "missing_for_parent_claim": "component response tensors and common units are missing",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PWD1837_3_no_source_only_scalar",
            "claim_piece": "species-label/source-weight silence",
            "formal_statement": "No species-indexed w_A, A_A(X), B_A(X), or m_A(X) may appear unless carried by an observable parent field/current/representation object.",
            "proof_move": "object-language/source-label forgetting would forbid source-only scalars before variation",
            "current_status": "CONDITIONAL_ONLY",
            "missing_for_parent_claim": "parent object language and measure/current owner remain unsigned",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PWD1837_4_geometry_stack",
            "claim_piece": "same geometry stack for force, clock and readout",
            "formal_statement": "mu_m,e_m,g_m,omega_m,D_m and test-body readout all descend through the same q(Phi) branch.",
            "proof_move": "single observed coframe plus connection descent would remove frame and connection re-entry into WEP",
            "current_status": "NOT_PARENT_SIGNED",
            "missing_for_parent_claim": "q-map, matter functor, geometry stack, tau/normal lock and arena functors are not all signed",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PWD1837_5_MICROSCOPE_product",
            "claim_piece": "eta bound comparison",
            "formal_statement": "A WEP prediction row may compare to the MICROSCOPE Ti/Pt bound only after P_WEP, product convention, material/source/readout kernels and branch lock share the same parent branch.",
            "proof_move": "separate prediction-side derivation from comparison-side bound anchor",
            "current_status": "BOUND_ANCHOR_EXISTS_PREDICTION_SIDE_MISSING",
            "missing_for_parent_claim": "official readout/source kernels and P_WEP coefficients are not imported or derived",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PWD1837_6_verdict",
            "claim_piece": "current MTS derives P_WEP",
            "formal_statement": "P_WEP=0 or P_WEP numeric is available for current MTS.",
            "proof_move": "all parent-signature clauses or all component-bound rows would have to pass",
            "current_status": "PWEP_NOT_DERIVED_CURRENT_CORPUS",
            "missing_for_parent_claim": "conditional theorem is clean but parent signature and component-bound inputs are missing",
            "parent_signed": False,
            "valid_for_claim": False,
        },
    ]


def response_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "operator_id": "PWC1837_0_total",
            "operator": "P_WEP_eta_AB",
            "definition": "linearized map from retained DeltaGamma_WEP components to eta_AB",
            "formula": "eta_AB = g_N^-1 n_mu [(P_A-P_B)^mu_i DeltaGamma_WEP^i]",
            "required_inputs": "species pair; local source normal n_mu; g_N convention; common DeltaGamma units; source/readout branch; component response tensors",
            "zero_condition": "P_A=P_B for all ordinary species or DeltaGamma_WEP=0 by parent theorem",
            "fallback_bound": "absolute-summed component rows below MICROSCOPE eta bound, no cancellation",
            "current_status": "CONTRACT_ONLY",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "operator_id": "PWC1837_1_spin",
            "operator": "P_WEP_spin",
            "definition": "spin/hypermomentum response difference between test materials",
            "formula": "eta_spin_AB = g_N^-1 n_mu (P_A^spin-P_B^spin)^mu_i DeltaGamma_spin^i",
            "required_inputs": "spin current norm; spin content of materials; torsion/spin response; same branch lock",
            "zero_condition": "spin torsion source is absent or species-universal under parent matter descent",
            "fallback_bound": "source-backed eta_spin_AB row",
            "current_status": "MISSING_SPIN_RESPONSE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "operator_id": "PWC1837_2_material_source",
            "operator": "P_WEP_material",
            "definition": "composition/source-weight response difference",
            "formula": "eta_material_AB = Delta_w_AB * tau_WEP or direct parent product P_WEP_material · DeltaGamma_material",
            "required_inputs": "Delta_w_AB or material tensor; tau_WEP/direct product; source current owner; product convention",
            "zero_condition": "source-label forgetting and single current owner make Delta_w_AB=0",
            "fallback_bound": "finite Delta_w_AB row after tau_WEP or direct product is sourced",
            "current_status": "MISSING_MATERIAL_SOURCE_PRODUCT",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "operator_id": "PWC1837_3_clock_nonmetric",
            "operator": "P_WEP_clock",
            "definition": "clock/rod/nonmetric contribution to differential acceleration readout",
            "formula": "eta_clock_AB = g_N^-1 n_mu (P_A^Qtrace-P_B^Qtrace)^mu_i DeltaGamma_clock^i",
            "required_inputs": "clock/rod material response; Q_trace value and units; same coframe/readout proof",
            "zero_condition": "metric-compatible observed coframe and universal clock/rod descent",
            "fallback_bound": "clock/nonmetric WEP component row",
            "current_status": "MISSING_CLOCK_RESPONSE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "operator_id": "PWC1837_4_projective",
            "operator": "P_WEP_projective",
            "definition": "projective trace leakage into source or test-body response",
            "formula": "eta_projective_AB = g_N^-1 n_mu (P_A^proj-P_B^proj)^mu_i DeltaGamma_projective^i",
            "required_inputs": "projective all-sector invariance certificate or trace coupling bound",
            "zero_condition": "all sectors projectively invariant or parent gauge fixes the trace before matter coupling",
            "fallback_bound": "projective leakage row",
            "current_status": "MISSING_PROJECTIVE_CERTIFICATE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "operator_id": "PWC1837_5_guard",
            "operator": "no_cancellation_guard",
            "definition": "WEP pass requires each retained component to be zero/bounded, not a tuned total",
            "formula": "abs(eta_total) <= sum_i abs(eta_i); every eta_i must pass or a parent identity must cancel it",
            "required_inputs": "component rows; sourced bound; parent cancellation identity if used",
            "zero_condition": "all component rows are theorem-zero",
            "fallback_bound": "absolute-summed finite vector",
            "current_status": "GUARD_ACTIVE",
            "valid_for_claim": False,
        },
    ]


def component_bound_rows() -> list[dict[str, Any]]:
    bound_source = RESIDUALS / "P8_Y5_R10_1069_MICROSCOPE_PROVENANCE_LEDGER.csv"
    tau_source = RESIDUALS / "P8_Y5_R10_1067_TAU_WEP_ACQUISITION_SCHEMA.csv"
    return [
        {
            "branch_id": BRANCH_ID,
            "bound_row_id": "WCB1837_0_spin",
            "component": "spin_hypermomentum",
            "target": "eta_spin_AB",
            "formula": "abs(g_N^-1 n_mu (P_A^spin-P_B^spin)^mu_i DeltaGamma_spin^i)",
            "accepted_evidence": "parent spin-torsion zero theorem OR numeric spin response with units/source path",
            "current_value": "MISSING_SPIN_RESPONSE_AND_DELTAGAMMA_SPIN",
            "units": "dimensionless",
            "comparison_bound": "MICROSCOPE_TiPt_eta_bound_anchor_nonclaim",
            "source_path": str(bound_source),
            "status": "COMPONENT_BOUND_ROW_STAGED_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "bound_row_id": "WCB1837_1_material_source_weight",
            "component": "material_marker_connection_current",
            "target": "eta_material_AB",
            "formula": "abs(Delta_w_TiPt * tau_WEP) or abs(P_WEP_material · DeltaGamma_material)",
            "accepted_evidence": "source-label forgetting zero theorem OR numeric Delta_w_TiPt and tau_WEP/direct product",
            "current_value": "MISSING_DELTA_W_AND_TAU_WEP",
            "units": "dimensionless",
            "comparison_bound": "MICROSCOPE_TiPt_eta_bound_anchor_nonclaim",
            "source_path": str(tau_source),
            "status": "COMPONENT_BOUND_ROW_STAGED_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "bound_row_id": "WCB1837_2_clock_rods",
            "component": "clock_rod_nonmetric_connection_current",
            "target": "eta_clock_AB",
            "formula": "abs(g_N^-1 n_mu (P_A^Qtrace-P_B^Qtrace)^mu_i DeltaGamma_clock^i)",
            "accepted_evidence": "clock/rod metric descent theorem OR numeric Q_trace clock/rod response",
            "current_value": "MISSING_CLOCK_ROD_RESPONSE_AND_Q_TRACE",
            "units": "dimensionless",
            "comparison_bound": "MICROSCOPE_TiPt_eta_bound_anchor_nonclaim",
            "source_path": str(bound_source),
            "status": "COMPONENT_BOUND_ROW_STAGED_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "bound_row_id": "WCB1837_3_projective_trace",
            "component": "projective_trace_current",
            "target": "eta_projective_AB",
            "formula": "abs(g_N^-1 n_mu (P_A^proj-P_B^proj)^mu_i DeltaGamma_projective^i)",
            "accepted_evidence": "all-sector projective invariance theorem OR sourced trace leakage bound",
            "current_value": "MISSING_PROJECTIVE_INVARIANCE_OR_TRACE_BOUND",
            "units": "dimensionless",
            "comparison_bound": "MICROSCOPE_TiPt_eta_bound_anchor_nonclaim",
            "source_path": str(bound_source),
            "status": "COMPONENT_BOUND_ROW_STAGED_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "bound_row_id": "WCB1837_4_frame_readout",
            "component": "Delta_frame_Delta_cal_Delta_tau_n",
            "target": "eta_frame_readout_AB",
            "formula": "abs(P_frame · Delta_frame + P_cal · Delta_cal + P_tau · Delta_tau_n)",
            "accepted_evidence": "single observed coframe/source/readout theorem OR numeric frame/readout residuals",
            "current_value": "MISSING_SINGLE_FRAME_THEOREM_OR_NUMERIC_FRAME_RESIDUAL",
            "units": "dimensionless",
            "comparison_bound": "MICROSCOPE_TiPt_eta_bound_anchor_nonclaim",
            "source_path": str(ROOT / "1155-Y5-R10-single-observed-coframe-source-frame-owner-or-frame-residual-row.md"),
            "status": "COMPONENT_BOUND_ROW_STAGED_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "bound_row_id": "WCB1837_5_total_guard",
            "component": "WEP_component_vector",
            "target": "eta_total_guard",
            "formula": "sum_i abs(eta_i) <= eta_bound, unless parent identity proves exact cancellation",
            "accepted_evidence": "all WCB1837 component rows pass or theorem-zero vector identity is parent-signed",
            "current_value": "MISSING_COMPONENT_VALUES",
            "units": "dimensionless",
            "comparison_bound": "MICROSCOPE_TiPt_eta_bound_anchor_nonclaim",
            "source_path": str(MICROSCOPE / "branch_classifier" / "P_WEP_same_parent_branch_lock.csv"),
            "status": "TOTAL_SCORE_REFUSED",
            "valid_for_claim": False,
        },
    ]


def current_corpus_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1837_0_conditional_theorem",
            "claim": "conditional universal matter descent implies P_WEP=0",
            "gate_pass": True,
            "reason": "the chain-rule/geodesic common-mode theorem is mathematically exact under its premises",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1837_1_parent_matter_functor",
            "claim": "current corpus parent-signs the ordinary matter functor",
            "gate_pass": False,
            "reason": "1045 and 1561 keep matter category/descent open",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1837_2_single_observed_frame",
            "claim": "current corpus proves one coframe/source/clock/readout branch",
            "gate_pass": False,
            "reason": "1155 and 537 keep single observed source frame and geometry stack unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1837_3_no_source_only_species_selector",
            "claim": "current corpus forbids source-only species weights",
            "gate_pass": False,
            "reason": "1077 and 1485 give conditional theorem-zero routes but do not parent-sign object language/current owner",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1837_4_component_bound_rows",
            "claim": "current corpus has score-ready WEP component-bound rows",
            "gate_pass": False,
            "reason": "component values, response tensors, tau_WEP/direct product and official kernels are missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1837_5_current_PWEP",
            "claim": "current corpus derives or numerically sources P_WEP",
            "gate_pass": False,
            "reason": "P_WEP remains a contract/ledger object; no WEP/local-GR claim follows",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1837_0_conditional_success",
            "decision": "PWEP_ZERO_THEOREM_SHAPE_IS_EXACT_CONDITIONAL",
            "reason": "universal observed-matter descent would make WEP common-mode and force P_WEP=0",
            "next_action": "try to parent-sign the ordinary matter action signature",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1837_1_current_refusal",
            "decision": "PWEP_NOT_CLAIMED_FOR_CURRENT_MTS",
            "reason": "matter functor, single observed frame, no source-only selector, and official readout/product kernels remain unsigned or missing",
            "next_action": "keep WEP rows nonclaim and do not promote local GR",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1837_2_best_next",
            "decision": "ORDINARY_MATTER_ACTION_SIGNATURE_NEXT",
            "reason": "the least-cheatable route is to prove the ordinary matter category has one observed coframe, one measure/current owner and no source-label scalar",
            "next_action": "1838-Y5-R2FR-ordinary-matter-action-signature-source-label-forgetting-or-WEP-bound-first-fill.md",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1837_0_primary",
            "next_target": "1838-Y5-R2FR-ordinary-matter-action-signature-source-label-forgetting-or-WEP-bound-first-fill.md",
            "script": "scripts/Y5_R2FR_ordinary_matter_action_signature_source_label_forgetting_or_WEP_bound_first_fill.py",
            "objective": "try to parent-sign the ordinary matter action signature that kills source-only WEP species labels; if it fails, fill the first explicit WEP component-bound input row without claiming",
            "selection_status": "selected",
            "success_condition": "either ordinary matter descent/no-source-label theorem is parent-signed, or the first component-bound row is ready as sourced nonclaim input",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1837_1_secondary",
            "next_target": "1838b-Y5-R2FR-Pclock-Plightcone-after-PWEP-matter-signature.md",
            "script": "scripts/Y5_R2FR_Pclock_Plightcone_after_PWEP_matter_signature.py",
            "objective": "derive clock and lightcone response operators only after the matter signature route is settled",
            "selection_status": "held_secondary",
            "success_condition": "clock/lightcone operators inherit a signed matter/coframe branch or remain nonclaim residual rows",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "PWEP_derivation_attempt": PWEP_derivation_attempt_rows(),
        "response_contract": response_contract_rows(),
        "component_bound_rows": component_bound_rows(),
        "current_corpus_gate": current_corpus_gate_rows(),
        "decision_ledger": decision_ledger_rows(),
        "next_target": next_target_rows(),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def copy_csvs(paths: list[Path]) -> None:
    for path in paths:
        for directory in [MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
            directory.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, directory / path.name)


def csv_parse_ok(paths: list[Path]) -> bool:
    try:
        for path in paths:
            with path.open("r", encoding="utf-8", newline="") as handle:
                list(csv.DictReader(handle))
    except Exception:
        return False
    return True


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    guarded_keys = {"valid_for_claim", "claim_allowed", "valid_prediction_row"}
    for rows in rows_map.values():
        for row in rows:
            for guarded_key in guarded_keys.intersection(row):
                if str(row[guarded_key]).lower() == "true":
                    return False
    return True


def no_formalization_outputs() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        name = path.name
        if "1837-Y5-R2FR" in name or name.startswith("P8_Y5_PARENT_QLOC_1837") or name.startswith("P8_Y5_BRR545_1837"):
            return False
    return True


def branch_copies_exist(paths: list[Path]) -> bool:
    for path in paths:
        for directory in [MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
            if not (directory / path.name).exists():
                return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]], copied_paths: list[Path]) -> list[dict[str, Any]]:
    source_rows = rows_map["source_register"]
    output_paths = [OUTPUTS[key] for key in rows_map.keys()]
    derivation_rows = rows_map["PWEP_derivation_attempt"]
    contract_rows = rows_map["response_contract"]
    component_rows = rows_map["component_bound_rows"]
    gate_rows = rows_map["current_corpus_gate"]
    checks: list[tuple[str, bool, str]] = [
        ("VAL1837_0_sources_exist", all(str(row["exists"]).lower() == "true" for row in source_rows), "all cited source paths exist"),
        ("VAL1837_1_needles_present", all(str(row["needles_present"]).lower() == "true" for row in source_rows), "all cited source needles are present"),
        (
            "VAL1837_2_conditional_theorem_written",
            any(row["theorem_id"] == "PWD1837_1_conditional_zero_theorem" and row["current_status"] == "EXACT_CONDITIONAL_THEOREM" for row in derivation_rows),
            "conditional P_WEP=0 theorem is written",
        ),
        (
            "VAL1837_3_current_verdict_blocks_claim",
            any(row["theorem_id"] == "PWD1837_6_verdict" and row["current_status"] == "PWEP_NOT_DERIVED_CURRENT_CORPUS" for row in derivation_rows),
            "current corpus does not claim P_WEP",
        ),
        (
            "VAL1837_4_response_contract_declared",
            any(row["operator"] == "P_WEP_eta_AB" and row["current_status"] == "CONTRACT_ONLY" for row in contract_rows),
            "P_WEP_eta_AB response contract is declared but nonclaim",
        ),
        (
            "VAL1837_5_component_rows_nonclaim",
            len(component_rows) == 6 and all(row["valid_for_claim"] is False for row in component_rows),
            "six WEP component-bound rows are staged as nonclaim",
        ),
        (
            "VAL1837_6_gate_refuses_current_PWEP",
            any(row["gate_id"] == "CG1837_5_current_PWEP" and row["gate_pass"] is False for row in gate_rows),
            "current P_WEP gate refuses the claim",
        ),
        (
            "VAL1837_7_next_selected",
            any(row["route_id"] == "NEXT1837_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selects ordinary matter action signature/source-label forgetting",
        ),
        ("VAL1837_8_no_claim_flags", no_claim_flags(rows_map), "no generated claim flags are true"),
        ("VAL1837_9_csv_parse", csv_parse_ok(output_paths), "all generated 1837 CSVs parse"),
        ("VAL1837_10_branch_copies", branch_copies_exist(copied_paths), "branch/quarantine/queue copies exist"),
        ("VAL1837_11_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1837_12_formalization_untouched", no_formalization_outputs(), "no 1837 outputs found under formalization-workbench"),
    ]
    rows = [{"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail} for check_id, passed, detail in checks]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1837_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1837 P_WEP response operator from matter functor or component-bound row checkpoint",
        }
    )
    return rows


def markdown_cell(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    return "\n".join(
        [
            "# 1837 Y5 R2FR P_WEP response operator from matter functor or component-bound row",
            "",
            "**Progress:** 1837 derives the exact conditional WEP route: if ordinary matter descends through one observed coframe/metric with one current/measure owner and no source-only species labels, then `P_WEP=0`. It also stages the fallback WEP component-bound rows if that parent signature cannot be signed.",
            "",
            "**Current verdict:** the theorem shape is clean, but current MTS does not yet parent-sign the matter functor, single observed frame, no-source-label rule, or readout/product kernels. Therefore `P_WEP` is not claimed and all WEP component rows remain `valid_for_claim=false`.",
            "",
            "**Claim ceiling:** no WEP pass, no `P_WEP=0` claim, no MICROSCOPE score, no clock/lightcone inheritance, no local GR/Newton promotion, no GitHub action, and no `formalization-workbench` edit is allowed from 1837.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## P_WEP Derivation Attempt",
            markdown_table(rows_map["PWEP_derivation_attempt"], ["theorem_id", "claim_piece", "formal_statement", "proof_move", "current_status", "missing_for_parent_claim", "parent_signed", "valid_for_claim"]),
            "",
            "## P_WEP Response Contract",
            markdown_table(rows_map["response_contract"], ["operator_id", "operator", "definition", "formula", "required_inputs", "zero_condition", "fallback_bound", "current_status", "valid_for_claim"]),
            "",
            "## WEP Component-Bound Rows",
            markdown_table(rows_map["component_bound_rows"], ["bound_row_id", "component", "target", "formula", "accepted_evidence", "current_value", "units", "comparison_bound", "source_path", "status", "valid_for_claim"]),
            "",
            "## Current Corpus Gate",
            markdown_table(rows_map["current_corpus_gate"], ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            markdown_table(rows_map["decision_ledger"], ["decision_id", "decision", "reason", "next_action"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is a good pressure result. We did not get to claim WEP silence, but we did get the cleanest possible condition for it: universal observed-matter descent. The next target should try to sign that ordinary-matter action signature directly. If it fails, the honest route is to fill one WEP component-bound row rather than smuggling in `P_WEP=0`.",
            "",
        ]
    )


def main() -> None:
    ensure_dirs()
    rows_map = rows_by_key()
    nonvalidation_paths: list[Path] = []
    for key, rows in rows_map.items():
        path = OUTPUTS[key]
        write_csv(path, rows)
        nonvalidation_paths.append(path)
    copy_csvs(nonvalidation_paths)
    validation_rows = build_validation(rows_map, nonvalidation_paths)
    write_csv(OUTPUTS["validation"], validation_rows)
    copy_csvs([OUTPUTS["validation"]])
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1837 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
