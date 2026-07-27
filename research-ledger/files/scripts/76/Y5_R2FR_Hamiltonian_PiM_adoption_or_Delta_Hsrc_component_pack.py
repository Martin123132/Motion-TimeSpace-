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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1795"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1795_0_1794_doc",
        "source_key": "1794_handoff",
        "source_path": ROOT / "1794-Y5-R2FR-parent-PiM-observed-time-generator-or-finite-Y5-pack.md",
        "needles": ["DEC1794_3_next", "NEXT1794_0_primary"],
        "role": "selects Hamiltonian Pi_M adoption or Delta_Hsrc pack as 1795 target",
    },
    {
        "source_id": "SRC1795_1_1794_validation",
        "source_key": "1794_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1794_VALIDATION.csv",
        "needles": ["VAL1794_OVERALL", "PASS"],
        "role": "confirms 1794 passed",
    },
    {
        "source_id": "SRC1795_2_1794_pim_gate",
        "source_key": "1794_pim_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1794_PIM_OBSERVED_TIME_GATE.csv",
        "needles": ["POT1794_5_Hamiltonian_PiM_adoption", "POT1794_6_verdict"],
        "role": "Pi_M/tau gate remains not parent-owned",
    },
    {
        "source_id": "SRC1795_3_1794_finite_y5",
        "source_key": "1794_finite_y5_pack",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1794_FINITE_Y5_PACK.csv",
        "needles": ["Y5P1794_2_R_eq", "Y5P1794_7_acceptance"],
        "role": "finite Y5 residual pack is missing components",
    },
    {
        "source_id": "SRC1795_4_1777_adoption",
        "source_key": "1777_hamiltonian_pim",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1777_HAMILTONIAN_PIM_ADOPTION_CONTRACT.csv",
        "needles": ["HPA1777_1_charge_functional", "HPA1777_5_verdict"],
        "role": "Hamiltonian Pi_M adoption contract",
    },
    {
        "source_id": "SRC1795_5_1778_lemma",
        "source_key": "1778_adopted_source_measure",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1778_ADOPTED_PIM_SOURCE_MEASURE_LEMMA.csv",
        "needles": ["ASM1778_0_conditional_theorem", "ASM1778_5_verdict"],
        "role": "adopted Pi_M source-measure lemma and Delta_Hsrc identity",
    },
    {
        "source_id": "SRC1795_6_1517_import_gate",
        "source_key": "1517_import_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_PIM_1517_THEOREM_IMPORT_GATE.csv",
        "needles": ["IMP1517_0_R_eq_zero", "IMP1517_4_mass_ref"],
        "role": "R_eq, commutator, boundary and M_H_ref import gaps",
    },
    {
        "source_id": "SRC1795_7_1518_commutator",
        "source_key": "1518_commutator",
        "source_path": RESIDUALS / "P8_Y5_PARENT_PIM_1518_COMMUTATOR_ZERO_AUDIT.csv",
        "needles": ["COM1518_0_product_rule", "COM1518_8_verdict"],
        "role": "commutator zero is conditional only",
    },
    {
        "source_id": "SRC1795_8_topological_hilbert",
        "source_key": "topological_hilbert",
        "source_path": RESIDUALS / "P8_TOPOLOGICAL_HILBERT_EQUALITY_ATTEMPT.csv",
        "needles": ["EH501_0_equality_statement", "EH501_5_radial_bound_fallback"],
        "role": "Hilbert/topological equality and radial fallback",
    },
    {
        "source_id": "SRC1795_9_worldtube_glue",
        "source_key": "worldtube_glue",
        "source_path": RESIDUALS / "P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv",
        "needles": ["HWT536_3_Hilbert_to_PiM_charge_map", "HWT536_8_weak_field_readout_after_charge_glue"],
        "role": "worldtube source-measure glue requirements",
    },
    {
        "source_id": "SRC1795_10_hamiltonian_residual_inputs",
        "source_key": "hamiltonian_source_measure_inputs",
        "source_path": RESIDUALS / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_RESIDUAL_INPUTS.csv",
        "needles": ["HSI541_0_boundary_reference", "HSI541_6_PPN_vector"],
        "role": "finite source-measure input requirements",
    },
    {
        "source_id": "SRC1795_11_hamiltonian_scorecard",
        "source_key": "hamiltonian_source_measure_scorecard",
        "source_path": RESIDUALS / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_SCORECARD.csv",
        "needles": ["HSS541_0_Hamiltonian_PiM_branch", "HSS541_7_PPN_followthrough"],
        "role": "Hamiltonian Pi_M source-measure scorecard fails current claim",
    },
    {
        "source_id": "SRC1795_12_repair_decomposition",
        "source_key": "hamiltonian_pim_repair_decomposition",
        "source_path": RESIDUALS / "P8_Y5_HAMILTONIAN_PIM_REPAIR_RESIDUAL_DECOMPOSITION.csv",
        "needles": ["HPRD553_0_integrability", "HPRD553_6_total_no_cancellation"],
        "role": "Hamiltonian Pi_M repair residual decomposition",
    },
    {
        "source_id": "SRC1795_13_charge_residual_decomposition",
        "source_key": "epsilon_charge_residual",
        "source_path": RESIDUALS / "P8_Y5_EPSILON_CHARGE_RESIDUAL_DECOMPOSITION.csv",
        "needles": ["ECD532_1_PiM_equality", "ECD532_6_total_no_cancellation"],
        "role": "charge-current residual decomposition",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1795_SOURCE_REGISTER.csv",
    "hamiltonian_pim_adoption_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1795_HAMILTONIAN_PIM_ADOPTION_ATTEMPT.csv",
    "delta_hsrc_identity": RESIDUALS / "P8_Y5_PARENT_QLOC_1795_DELTA_HSRC_IDENTITY.csv",
    "delta_hsrc_component_pack": RESIDUALS / "P8_Y5_PARENT_QLOC_1795_DELTA_HSRC_COMPONENT_PACK.csv",
    "adoption_equivalence_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1795_ADOPTION_EQUIVALENCE_GATE.csv",
    "countermodel_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1795_COUNTERMODEL_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1795_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1795_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1795_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1795_VALIDATION.csv",
}

DOC_PATH = ROOT / "1795-Y5-R2FR-Hamiltonian-PiM-adoption-or-Delta-Hsrc-component-pack.md"


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
                "role": source["role"],
            }
        )
    return rows


def hamiltonian_pim_adoption_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "HPA1795_0_active_branch_declaration",
            "required_piece": "declare the active source-mass projector as Hamiltonian Pi_M^H or prove old Pi_M equivalence",
            "mathematical_form": "Pi_M := Pi_M^H OR Pi_M^top J_H = Pi_M^H J_H + dB_H + R_PiH with R_PiH=0 and int dB_H=0",
            "current_status": "CONTRACT_READY_NOT_ADOPTED",
            "blocking_gap": "no single parent action adopts/equates the projector without circular source normalization",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "HPA1795_1_charge_functional",
            "required_piece": "mass functional from the parent Hamiltonian/covariant-phase-space charge",
            "mathematical_form": "ell_H[J_H;tau,S]=(4*pi*G_ref)^-1 int_S Q_tau^MTS[J_H]",
            "current_status": "FORMAL_CANDIDATE_ONLY",
            "blocking_gap": "Theta_total/Q_tau owner, integrability, fixed reference and tau normalization remain missing",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "HPA1795_2_source_measure_lemma",
            "required_piece": "Hamiltonian Pi_M^H reads the observed dressed worldtube source",
            "mathematical_form": "M_H[W;S]=G_ref^-1 int_S Q_tau^MTS-H_ref=M_eff[Pi_M^H J_H^dress]",
            "current_status": "CONDITIONAL_LEMMA_SHAPE_DERIVED",
            "blocking_gap": "parent current, source functor, chain map, boundary flux and exterior C-term silence are not signed",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "HPA1795_3_old_pim_guardrail",
            "required_piece": "old/topological Pi_M cannot be counted unless equivalent to Pi_M^H",
            "mathematical_form": "Pi_M^top J_H = Pi_M^H J_H + dB_H + R_PiH",
            "current_status": "EQUIVALENCE_NOT_DERIVED",
            "blocking_gap": "R_PiH zero theorem/source bound and B_H flux rule are missing",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "HPA1795_4_no_circular_readout",
            "required_piece": "Gauss/orbital calibration cannot prove source-measure equality",
            "mathematical_form": "M_orbit=G_ref M_H only after source-measure equality and PG/PPN gates pass",
            "current_status": "NO_CIRCULAR_DENOMINATOR_POLICY_RETAINED",
            "blocking_gap": "orbital GM remains downstream evidence, not proof of Delta_Hsrc=0",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "HPA1795_5_verdict",
            "required_piece": "claim-grade Hamiltonian Pi_M adoption/equivalence",
            "mathematical_form": "HPA1795_0 through HPA1795_4 pass in one parent action",
            "current_status": "HAMILTONIAN_PIM_ADOPTION_NOT_SIGNED",
            "blocking_gap": "the theorem route remains alive but not activated",
            "parent_signed": False,
            "valid_for_claim": False,
        },
    ]


def delta_hsrc_identity_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "identity_id": "DHI1795_0_definition",
            "object": "Delta_Hsrc",
            "mathematical_form": "Delta_Hsrc := G_ref^-1 int_S Q_tau^MTS - H_ref - M_eff[Pi_M^H J_H^dress]",
            "meaning": "failure of Hamiltonian source-measure equality",
            "current_status": "IDENTITY_STAGED_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "identity_id": "DHI1795_1_component_split",
            "object": "Delta_Hsrc decomposition",
            "mathematical_form": "Delta_Hsrc = Delta_integrability + R_eq + I_commutator + B_ref + Delta_extra_charge + Delta_tau_MHref + Delta_Gauss_PPN",
            "meaning": "all unproved source-measure pieces become named residual components",
            "current_status": "DECOMPOSITION_WRITTEN_INPUTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "identity_id": "DHI1795_2_no_cancellation_envelope",
            "object": "epsilon_Hsrc_abs",
            "mathematical_form": "epsilon_Hsrc_abs = (|Delta_integrability|+|R_eq|+|I_commutator|+|B_ref|+|Delta_extra_charge|+|Delta_tau_MHref|+|Delta_Gauss_PPN|)/M_H_ref",
            "meaning": "strict absolute envelope; no cancellation credit",
            "current_status": "NOT_COMPUTABLE_COMPONENTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "identity_id": "DHI1795_3_zero_theorem_condition",
            "object": "Delta_Hsrc=0 theorem",
            "mathematical_form": "Delta_Hsrc=0 iff Hamiltonian Pi_M adoption/equivalence, integrability/reference, source functor, commutator, boundary/reference, extra charge silence, tau/M_H_ref and readout followthrough all close",
            "meaning": "source-normalized Newton can start only after this condition",
            "current_status": "ZERO_THEOREM_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "identity_id": "DHI1795_4_verdict",
            "object": "Delta_Hsrc current status",
            "mathematical_form": "identity and component slots exist; no zero theorem or finite numeric vector exists",
            "meaning": "retain Delta_Hsrc as the central Y5 source-normalization blocker",
            "current_status": "DELTA_HSRC_RETAINED_NONCLAIM",
            "valid_for_claim": False,
        },
    ]


def delta_hsrc_component_pack_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "component_id": "DHC1795_0_integrability_reference",
            "symbol": "Delta_integrability",
            "definition": "failure of Q_tau to define an integrable fixed-reference Hamiltonian mass functional",
            "formula": "abs(delta_H_tau_nonintegrable_over_MH)+abs(Delta_ref_over_MH)",
            "required_input": "delta_H_tau_nonintegrable_over_MH;Delta_ref_over_MH;source_file;assumptions",
            "current_status": "MISSING_INTEGRABILITY_REFERENCE_INPUTS",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "DHC1795_1_R_eq_source_equality",
            "symbol": "R_eq / epsilon_PiM_equality",
            "definition": "Hilbert/topological/source-measure equality residual",
            "formula": "abs(M_source_W-G_ref^-1 int_S Q_tau)/M_H_ref or (Q_parent-M_H[Pi_M J_H])/M_H",
            "required_input": "source_frame;readout_frame;source_charge_mismatch_over_MH;Delta_frame;Delta_cal;source_file",
            "current_status": "MISSING_R_EQ_SOURCE_EQUALITY_INPUTS",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "DHC1795_2_I_commutator_radial",
            "symbol": "I_commutator",
            "definition": "finite-shell product-rule leakage from d(Pi_M J_H)",
            "formula": "M_H_ref^-1 int_A [d,Pi_M]J_H",
            "required_input": "I_commutator profile or theorem-zero; annulus; source_file; units",
            "current_status": "MISSING_COMMUTATOR_ZERO_OR_PROFILE",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "DHC1795_3_old_PiM_equivalence",
            "symbol": "R_PiH",
            "definition": "old/topological/Hodge Pi_M differs from Hamiltonian Pi_M representative",
            "formula": "abs(int_S(Pi_M_old J_H-Pi_M^H J_H-dB_zero))/M_H_ref",
            "required_input": "old_new_PiM_mismatch_over_MH;B_zero_flux_over_MH;projector_variation_over_MH",
            "current_status": "MISSING_OLD_PIM_EQUIVALENCE_INPUTS",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "DHC1795_4_boundary_reference",
            "symbol": "B_ref",
            "definition": "boundary improvement, reference, multiplier or parent-anomaly offset in source charge",
            "formula": "M_H_ref^-1(int_boundary Pi_M K_owner + int_A A_parent)",
            "required_input": "B_zero_flux;Delta_symp;reference convention;source_file;units",
            "current_status": "MISSING_BOUNDARY_REFERENCE_INPUTS",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "DHC1795_5_extra_charge",
            "symbol": "Delta_extra_charge",
            "definition": "non-EH/domain/memory/range/frame/boundary/projector sectors carry independent Hamiltonian mass charge",
            "formula": "sum_i abs(Delta_i_over_MH)",
            "required_input": "channel;Delta_charge_over_MH;coefficient_to_lock;source_file",
            "current_status": "MISSING_EXTRA_CHARGE_CHANNEL_INPUTS",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "DHC1795_6_tau_MHref_readout",
            "symbol": "Delta_tau_MHref + Delta_Gauss_PPN",
            "definition": "tau/M_H_ref denominator and downstream Gauss/orbital/PPN readout mismatch",
            "formula": "abs(G_ref*M_H_ref/GM_orbit-1)+readout_residuals",
            "required_input": "tau_obs lock;M_H_ref;GM_orbit;Delta_cal;alpha_lambda;partial_r_ln_mu_obs;PPN_vector",
            "current_status": "MISSING_TAU_MHREF_GAUSS_PPN_INPUTS",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "DHC1795_7_total_abs_envelope",
            "symbol": "epsilon_Hsrc_abs",
            "definition": "strict no-cancellation Delta_Hsrc absolute envelope",
            "formula": "sum_abs(DHC1795_0..DHC1795_6)",
            "required_input": "all component rows theorem-zero or source-backed; no cancellation credit",
            "current_status": "REJECT_CURRENT_DELTA_HSRC_PACK",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def adoption_equivalence_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AEG1795_0_R_eq_zero",
            "gate": "Hilbert/topological equality theorem",
            "required_evidence": "R_eq=0 for the same source worldtube and same Pi_M J_H",
            "current_status": "NOT_DERIVED_CURRENT_CORPUS",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AEG1795_1_commutator_zero",
            "gate": "Pi_M fixed/covariantly constant theorem",
            "required_evidence": "[d,Pi_M]J_H=0 on the physical Hilbert source-current domain",
            "current_status": "NEXT_THEOREM_TARGET_NOT_CLOSED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AEG1795_2_boundary_zero",
            "gate": "exact/reference boundary theorem",
            "required_evidence": "boundary exact/reference flux integrates to zero on linked surfaces",
            "current_status": "MISSING_CERTIFICATE_OR_BOUND",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AEG1795_3_stress_zero",
            "gate": "projector stress theorem",
            "required_evidence": "Pi_M projector stress vanishes or is bounded below local locks",
            "current_status": "MISSING_CERTIFICATE_OR_NUMERIC_BOUND",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AEG1795_4_MHref",
            "gate": "same-frame Hilbert mass reference",
            "required_evidence": "positive M_H_ref with units/source path in observed coframe",
            "current_status": "MISSING_M_H_REF",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AEG1795_5_verdict",
            "gate": "Hamiltonian Pi_M source-measure adoption/equivalence gate",
            "required_evidence": "AEG1795_0 through AEG1795_4 close before Gauss/orbital followthrough",
            "current_status": "ADOPTION_EQUIVALENCE_NOT_CLOSED",
            "valid_for_claim": False,
        },
    ]


def countermodel_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1795_0_wrong_source_measure",
            "countermodel": "Hamiltonian boundary charge and Hilbert/source measure are not the same object",
            "survives_current_constraints": True,
            "why_survives": "Delta_Hsrc source-measure lemma is conditional only",
            "what_kills_it": "parent-signed Pi_M^H source-measure lemma or finite Delta_Hsrc bound",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1795_1_old_topological_wrong_charge",
            "countermodel": "old/topological Pi_M closes but measures the wrong conserved charge",
            "survives_current_constraints": True,
            "why_survives": "old Pi_M equivalence to Pi_M^H is not derived",
            "what_kills_it": "R_PiH=0 and exact boundary flux zero",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1795_2_commutator_radial_hair",
            "countermodel": "finite [d,Pi_M]J_H creates radial mass/source-normalization hair",
            "survives_current_constraints": True,
            "why_survives": "commutator-zero theorem is not parent-signed",
            "what_kills_it": "fixed chain-map theorem on physical Hilbert current domain or finite bound row",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1795_3_boundary_reference_offset",
            "countermodel": "boundary/reference terms shift source mass equality",
            "survives_current_constraints": True,
            "why_survives": "B_zero_flux, Delta_symp and reference convention are unfilled",
            "what_kills_it": "boundary/reference zero theorem or source-backed residual row",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1795_4_extra_charge_channel",
            "countermodel": "non-EH/memory/domain/range/frame/PPN channels carry independent source charge",
            "survives_current_constraints": True,
            "why_survives": "field-specific silence queue is open",
            "what_kills_it": "channelwise zero theorem or finite absolute envelope",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1795_0_Hamiltonian_PiM_adoption",
            "claim": "Hamiltonian Pi_M^H adoption/equivalence is parent-signed",
            "status": "BLOCKED",
            "reason": "active-branch declaration, charge functional, source-measure lemma and old-PiM equivalence are not signed",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1795_1_Delta_Hsrc_zero",
            "claim": "Delta_Hsrc=0 theorem",
            "status": "BLOCKED",
            "reason": "R_eq, commutator, boundary/reference, extra charge and M_H_ref gates remain open",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1795_2_finite_Delta_Hsrc_score",
            "claim": "finite Delta_Hsrc component pack can be scored",
            "status": "BLOCKED",
            "reason": "component rows are missing source-backed values, units and assumptions",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1795_3_source_normalized_Newton",
            "claim": "source-normalized Newton is derived",
            "status": "BLOCKED",
            "reason": "Delta_Hsrc is retained and Gauss/orbital readout is downstream",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1795_4_local_GR_Newton",
            "claim": "derived local GR/Newton reduction",
            "status": "BLOCKED",
            "reason": "Y5 Delta_Hsrc, Y6 stress, q_loc, c_R2 and PPN gates are not jointly closed",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1795_0_adoption",
            "decision": "HAMILTONIAN_PIM_ADOPTION_NOT_SIGNED",
            "reason": "Pi_M^H remains the best route, but active-branch adoption/equivalence is not in a parent action",
            "next_action": "do not promote measured GM; retain Delta_Hsrc",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1795_1_identity",
            "decision": "DELTA_HSRC_IDENTITY_IS_ACTIVE_BLOCKER",
            "reason": "Delta_Hsrc names the exact source-measure mismatch instead of hiding it in orbital calibration",
            "next_action": "fill theorem-zero or finite component rows",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1795_2_pack",
            "decision": "DELTA_HSRC_COMPONENT_PACK_REJECTED_NONCLAIM",
            "reason": "integrability, R_eq, commutator, old-PiM equivalence, boundary/reference, extra charge and readout rows are unfilled",
            "next_action": "prioritize integrability/reference and first source-backed residual component",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1795_3_next",
            "decision": "HAMILTONIAN_INTEGRABILITY_REFERENCE_OR_FIRST_DELTA_HSRC_ROW_NEXT",
            "reason": "integrability/reference is the first highest-priority component in the Hamiltonian source-measure scorecard",
            "next_action": "build 1796 Hamiltonian charge integrability/reference lock or first Delta_Hsrc residual row",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1795_0_primary",
            "next_target": "1796-Y5-R2FR-Hamiltonian-charge-integrability-reference-or-first-Delta-Hsrc-row.md",
            "script": "scripts/Y5_R2FR_Hamiltonian_charge_integrability_reference_or_first_Delta_Hsrc_row.py",
            "objective": "try to prove Q_tau integrability and fixed-reference silence for the Hamiltonian mass functional; if not, emit the first source-backed/nonclaim Delta_integrability row schema",
            "selection_status": "selected",
            "success_condition": "integrable fixed-reference Hamiltonian charge with source path, or strict finite Delta_integrability residual row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1795_1_parallel_commutator",
            "next_target": "1796b-Y5-R2FR-PiM-commutator-chainmap-or-finite-Icommutator-row.md",
            "script": "scripts/Y5_R2FR_PiM_commutator_chainmap_or_finite_Icommutator_row.py",
            "objective": "prove fixed-chainmap commutator silence or fill finite I_commutator profile row",
            "selection_status": "held_parallel",
            "success_condition": "parent-signed commutator zero theorem or source-backed finite profile",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1795_2_parallel_R_eq",
            "next_target": "1796c-Y5-R2FR-Hilbert-topological-equality-or-Req-bound-row.md",
            "script": "scripts/Y5_R2FR_Hilbert_topological_equality_or_Req_bound_row.py",
            "objective": "prove Hilbert/topological equality for the same worldtube/source current or fill R_eq residual row",
            "selection_status": "held_parallel",
            "success_condition": "R_eq zero theorem or source-backed residual bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "hamiltonian_pim_adoption_attempt": hamiltonian_pim_adoption_attempt_rows(),
        "delta_hsrc_identity": delta_hsrc_identity_rows(),
        "delta_hsrc_component_pack": delta_hsrc_component_pack_rows(),
        "adoption_equivalence_gate": adoption_equivalence_gate_rows(),
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
        shutil.copy2(path, RAB_QUEUE / f"JR1795_{key.upper()}.csv")


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
                "score_emitted",
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
                    "score_emitted",
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
        if not (RAB_QUEUE / f"JR1795_{key.upper()}.csv").exists():
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
        ("VAL1795_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1795_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1795_2_adoption_not_signed",
            any(row["attempt_id"] == "HPA1795_5_verdict" and row["current_status"] == "HAMILTONIAN_PIM_ADOPTION_NOT_SIGNED" for row in rows_map["hamiltonian_pim_adoption_attempt"])
            and all(not boolish(row["parent_signed"]) and not boolish(row["valid_for_claim"]) for row in rows_map["hamiltonian_pim_adoption_attempt"]),
            "Hamiltonian Pi_M adoption is not signed",
        ),
        (
            "VAL1795_3_delta_identity_written",
            any(row["identity_id"] == "DHI1795_0_definition" for row in rows_map["delta_hsrc_identity"])
            and any(row["identity_id"] == "DHI1795_4_verdict" and row["current_status"] == "DELTA_HSRC_RETAINED_NONCLAIM" for row in rows_map["delta_hsrc_identity"]),
            "Delta_Hsrc identity is written and retained nonclaim",
        ),
        (
            "VAL1795_4_component_pack_rejected",
            any(row["component_id"] == "DHC1795_7_total_abs_envelope" and row["current_status"] == "REJECT_CURRENT_DELTA_HSRC_PACK" for row in rows_map["delta_hsrc_component_pack"])
            and all(not boolish(row["score_ready"]) and not boolish(row["valid_prediction_row"]) for row in rows_map["delta_hsrc_component_pack"]),
            "Delta_Hsrc component pack is rejected and non-scoreable",
        ),
        (
            "VAL1795_5_equivalence_gate_blocks",
            any(row["gate_id"] == "AEG1795_5_verdict" and row["current_status"] == "ADOPTION_EQUIVALENCE_NOT_CLOSED" for row in rows_map["adoption_equivalence_gate"]),
            "adoption/equivalence gate is blocked",
        ),
        (
            "VAL1795_6_countermodels_retained",
            all(boolish(row["survives_current_constraints"]) for row in rows_map["countermodel_ledger"]),
            "countermodels remain live",
        ),
        (
            "VAL1795_7_claim_gates_blocked",
            all(row["status"] == "BLOCKED" and not boolish(row["gate_pass"]) and not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "claim gates are blocked",
        ),
        ("VAL1795_8_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1795_9_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1795_10_decision_next",
            any(
                row["decision_id"] == "DEC1795_3_next"
                and row["decision"] == "HAMILTONIAN_INTEGRABILITY_REFERENCE_OR_FIRST_DELTA_HSRC_ROW_NEXT"
                for row in rows_map["decision_ledger"]
            ),
            "decision selects integrability/reference or first Delta_Hsrc row next",
        ),
        (
            "VAL1795_11_next_selected",
            any(row["route_id"] == "NEXT1795_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1795_12_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1795 CSVs parse"),
        ("VAL1795_13_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1795_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1795_15_formalization_untouched", formalization_untouched(), "no 1795 outputs found under formalization-workbench"),
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
            "check_id": "VAL1795_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1795 Hamiltonian Pi_M adoption or Delta_Hsrc component pack checkpoint",
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
            "# 1795 - Y5/R2FR Hamiltonian PiM Adoption or Delta-Hsrc Component Pack",
            "",
            "## Verdict",
            "",
            "1795 tries the theorem route first. Hamiltonian `Pi_M^H` remains the best repair because it avoids the wrong-charge problem: source mass should be a parent Hamiltonian/covariant-phase-space charge, not an orbital fit and not an arbitrary topological label. But the active branch still does not sign adoption/equivalence in one parent action.",
            "",
            "So the checkpoint promotes `Delta_Hsrc` as the exact nonclaim object:",
            "",
            "`Delta_Hsrc := G_ref^-1 int_S Q_tau^MTS - H_ref - M_eff[Pi_M^H J_H^dress]`.",
            "",
            "If the theorem route closes, `Delta_Hsrc=0`. If it does not, the residual must be decomposed into integrability/reference, Hilbert/source equality, commutator, old-PiM equivalence, boundary/reference, extra charge and readout/denominator components. The component pack is strict and rejected until those rows are theorem-zero or source-backed with units.",
            "",
            "**Claim ceiling:** no Hamiltonian `Pi_M` adoption claim, no `Delta_Hsrc=0`, no finite `Delta_Hsrc` score, no source-normalized Newton, no local-GR/Newton claim, no GitHub action, and no `formalization-workbench` edit is allowed from 1795.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## Hamiltonian PiM Adoption Attempt",
            markdown_table(rows_map["hamiltonian_pim_adoption_attempt"], ["attempt_id", "required_piece", "mathematical_form", "current_status", "blocking_gap", "valid_for_claim"]),
            "",
            "## Delta-Hsrc Identity",
            markdown_table(rows_map["delta_hsrc_identity"], ["identity_id", "object", "mathematical_form", "meaning", "current_status", "valid_for_claim"]),
            "",
            "## Delta-Hsrc Component Pack",
            markdown_table(rows_map["delta_hsrc_component_pack"], ["component_id", "symbol", "definition", "formula", "required_input", "current_status", "score_ready", "valid_prediction_row", "valid_for_claim"]),
            "",
            "## Adoption Equivalence Gate",
            markdown_table(rows_map["adoption_equivalence_gate"], ["gate_id", "gate", "required_evidence", "current_status", "valid_for_claim"]),
            "",
            "## Countermodel Ledger",
            markdown_table(rows_map["countermodel_ledger"], ["countermodel_id", "countermodel", "survives_current_constraints", "why_survives", "what_kills_it"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["claim_id", "claim", "status", "reason", "gate_pass", "valid_for_claim"]),
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
            "This is a good narrowing. The Newton-source problem is no longer spread across vague GM language. It is now one object, `Delta_Hsrc`, with a no-cancellation component envelope. The next best attack is the first component: Hamiltonian charge integrability and fixed-reference silence. If that fails, fill the first finite row honestly.",
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
    print(f"1795 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
