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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1794"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1794_0_1793_doc",
        "source_key": "1793_handoff",
        "source_path": ROOT / "1793-Y5-R2FR-Y5-source-charge-owner-and-Y6-extra-stress-gate-or-finite-coupling-pack.md",
        "needles": ["DEC1793_3_next", "NEXT1793_0_primary"],
        "role": "selects parent Pi_M and observed-time generator as 1794 target",
    },
    {
        "source_id": "SRC1794_1_1793_validation",
        "source_key": "1793_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1793_VALIDATION.csv",
        "needles": ["VAL1793_OVERALL", "PASS"],
        "role": "confirms 1793 passed",
    },
    {
        "source_id": "SRC1794_2_1793_y5_chain",
        "source_key": "1793_y5_chain",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1793_Y5_SOURCE_CHARGE_OWNER_ATTEMPT.csv",
        "needles": ["Y5SC1793_2_parent_source_charge", "Y5SC1793_7_verdict"],
        "role": "Y5 source-charge chain is written but not activated",
    },
    {
        "source_id": "SRC1794_3_1793_mass_flux",
        "source_key": "1793_mass_flux",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1793_SOURCE_MASS_FLUX_CHAIN.csv",
        "needles": ["MFC1793_2_observed_time_generator", "MFC1793_7_verdict"],
        "role": "mass flux chain identifies observed time and Pi_M as missing",
    },
    {
        "source_id": "SRC1794_4_1517_import_gate",
        "source_key": "1517_import_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_PIM_1517_THEOREM_IMPORT_GATE.csv",
        "needles": ["IMP1517_0_R_eq_zero", "IMP1517_5_worldtube_followthrough"],
        "role": "theorem import gate for Hilbert/topological equality, commutator, boundary and mass reference",
    },
    {
        "source_id": "SRC1794_5_1518_commutator",
        "source_key": "1518_commutator",
        "source_path": RESIDUALS / "P8_Y5_PARENT_PIM_1518_COMMUTATOR_ZERO_AUDIT.csv",
        "needles": ["COM1518_0_product_rule", "COM1518_8_verdict"],
        "role": "Pi_M commutator zero is not proved",
    },
    {
        "source_id": "SRC1794_6_1726_observed_time",
        "source_key": "1726_observed_time",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1726_OBSERVED_TIME_GENERATOR_AUDIT.csv",
        "needles": ["OTG1726_0_parent_data", "OTG1726_6_verdict"],
        "role": "observed time generator target but not parent-selected",
    },
    {
        "source_id": "SRC1794_7_1777_hamiltonian_pim",
        "source_key": "1777_hamiltonian_pim",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1777_HAMILTONIAN_PIM_ADOPTION_CONTRACT.csv",
        "needles": ["HPA1777_0_declare_branch", "HPA1777_5_verdict"],
        "role": "Hamiltonian Pi_M adoption contract",
    },
    {
        "source_id": "SRC1794_8_1778_adopted_lemma",
        "source_key": "1778_adopted_lemma",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1778_ADOPTED_PIM_SOURCE_MEASURE_LEMMA.csv",
        "needles": ["ASM1778_0_conditional_theorem", "ASM1778_5_verdict"],
        "role": "adopted Pi_M source-measure lemma shape derived but not proved",
    },
    {
        "source_id": "SRC1794_9_topological_hilbert",
        "source_key": "topological_hilbert_equality",
        "source_path": RESIDUALS / "P8_TOPOLOGICAL_HILBERT_EQUALITY_ATTEMPT.csv",
        "needles": ["EH501_0_equality_statement", "EH501_5_radial_bound_fallback"],
        "role": "Hilbert/topological equality attempt and fallback",
    },
    {
        "source_id": "SRC1794_10_worldtube_glue",
        "source_key": "hilbert_worldtube_glue",
        "source_path": RESIDUALS / "P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv",
        "needles": ["HWT536_0_parent_worldtube_fixed", "HWT536_8_weak_field_readout_after_charge_glue"],
        "role": "worldtube/source-measure glue requirements",
    },
    {
        "source_id": "SRC1794_11_readout_decision",
        "source_key": "hamiltonian_pim_readout",
        "source_path": RESIDUALS / "P8_Y5_HAMILTONIAN_PIM_READOUT_DECISION.csv",
        "needles": ["D540_0_Hamiltonian_PiM_not_enough", "D540_4_private_no_push"],
        "role": "Hamiltonian Pi_M alone does not derive measured GM",
    },
    {
        "source_id": "SRC1794_12_source_current_closure",
        "source_key": "source_current_closure",
        "source_path": RESIDUALS / "P8_Y5_SOURCE_CURRENT_CLOSURE_THEOREM_ATTEMPT.csv",
        "needles": ["SC532_2_charge_current_variation_identity", "SC532_7_measured_GM_next_gate"],
        "role": "charge-current equality and measured-GM downstream gate",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1794_SOURCE_REGISTER.csv",
    "pim_observed_time_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1794_PIM_OBSERVED_TIME_GATE.csv",
    "hamiltonian_pim_adoption_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1794_HAMILTONIAN_PIM_ADOPTION_GATE.csv",
    "commutator_glue_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1794_COMMUTATOR_GLUE_AUDIT.csv",
    "finite_y5_pack": RESIDUALS / "P8_Y5_PARENT_QLOC_1794_FINITE_Y5_PACK.csv",
    "countermodel_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1794_COUNTERMODEL_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1794_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1794_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1794_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1794_VALIDATION.csv",
}

DOC_PATH = ROOT / "1794-Y5-R2FR-parent-PiM-observed-time-generator-or-finite-Y5-pack.md"


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


def pim_observed_time_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "POT1794_0_parent_branch_data",
            "required_clause": "parent local branch supplies e_obs, time orientation, boundary/clock class and exterior domain before readout",
            "mathematical_form": "B_local=(M_local,e_obs,B_clock,B_ref,orientation,domain_class)",
            "current_status": "PARENT_BRANCH_DATA_INCOMPLETE",
            "blocking_gap": "boundary clock class and reference class are not parent-signed",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "POT1794_1_tau_obs_generator",
            "required_clause": "tau_obs is stationary where available or quasilocal time-flow fixed by boundary lapse/shift",
            "mathematical_form": "L_tau g_obs=0, or tau_obs=N n + N^i e_i with (N,N^i)|_B fixed",
            "current_status": "MISSING_LOCAL_STATIONARY_OR_QUASILOCAL_CERTIFICATE",
            "blocking_gap": "no current-branch certificate for the observed time generator",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "POT1794_2_clock_normalization",
            "required_clause": "tau_obs is normalized by the same boundary/local clocks used for redshift and clock readouts",
            "mathematical_form": "g_obs(tau_obs,tau_obs)|_{B_clock}=-1 or N_B[e_obs,tau_obs]=1",
            "current_status": "MISSING_BOUNDARY_CLOCK_NORMALIZATION_THEOREM",
            "blocking_gap": "clock product maps exist but not Hamiltonian generator normalization",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "POT1794_3_same_frame",
            "required_clause": "same e_obs and tau_obs define clocks, rods, photons, source current, Hamiltonian charge and slow-orbit readout",
            "mathematical_form": "e_source=e_clock=e_photon=e_orbit=e_obs and J_H[tau_obs]=star(T_obs(tau_obs,.))",
            "current_status": "SAME_FRAME_CONDITIONAL_NOT_CORPUS_PROVED",
            "blocking_gap": "same-frame clauses are written but not current-MTS derived",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "POT1794_4_pre_readout_selection",
            "required_clause": "tau_obs and Pi_M are selected before source mass, orbital GM, WEP readout or R10 fitting",
            "mathematical_form": "partial_{GM_orbit,Qbar,WEP,R10} tau_obs = 0 and partial_{GM_orbit,Qbar,WEP,R10} Pi_M = 0",
            "current_status": "PRE_READOUT_SELECTION_NOT_SIGNED",
            "blocking_gap": "guardrails exclude shortcuts but do not construct parent-selected tau_obs/Pi_M",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "POT1794_5_Hamiltonian_PiM_adoption",
            "required_clause": "active local mass projector is explicitly adopted as Hamiltonian Pi_M^H or old Pi_M is proven equivalent",
            "mathematical_form": "Pi_M := Pi_M^H, or Pi_M^top J_H = Pi_M^H J_H + dB_H + R_PiH with R_PiH=0 and int dB_H=0",
            "current_status": "CONTRACT_READY_NOT_ADOPTED",
            "blocking_gap": "adoption/equivalence is staged but not signed in a parent action",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "POT1794_6_verdict",
            "required_clause": "parent Pi_M and observed-time generator gate",
            "mathematical_form": "POT1794_0 through POT1794_5 all close",
            "current_status": "PIM_OBSERVED_TIME_NOT_PARENT_OWNED",
            "blocking_gap": "tau_obs, clock normalization, same frame, pre-readout selection and Pi_M adoption remain unsigned",
            "parent_signed": False,
            "valid_for_claim": False,
        },
    ]


def hamiltonian_pim_adoption_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "adoption_id": "HCG1794_0_charge_functional",
            "required_piece": "mass functional from the parent Hamiltonian/covariant-phase-space charge",
            "mathematical_form": "ell_H[J_H;tau,S] := (4*pi*G_ref)^-1 int_S Q_tau^MTS[J_H]",
            "current_status": "FORMAL_CANDIDATE_ONLY",
            "missing_for_claim": "Theta_total/Q_tau owner, integrability, reference lock and tau normalization",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "adoption_id": "HCG1794_1_representative",
            "required_piece": "Hamiltonian charge represented as fixed mass cohomology representative",
            "mathematical_form": "Pi_M^H J_H := ell_H[J_H;tau,S] omega_M^H with integral_L omega_M^H=1",
            "current_status": "CANDIDATE_REPRESENTATIVE_ONLY",
            "missing_for_claim": "omega_M^H parent normalization and no-readout certificate",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "adoption_id": "HCG1794_2_source_measure_lemma",
            "required_piece": "adopted Pi_M^H reads observed dressed worldtube source",
            "mathematical_form": "M_H[W;S]=G_ref^-1 int_S Q_tau^MTS-H_ref = M_eff[Pi_M^H J_H^dress]",
            "current_status": "CONDITIONAL_LEMMA_SHAPE_DERIVED",
            "missing_for_claim": "parent current, integrability, source functor, chain map, boundary flux and exterior C-term silence",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "adoption_id": "HCG1794_3_old_pim_equivalence",
            "required_piece": "old/topological Pi_M cannot be used unless equivalent to Pi_M^H",
            "mathematical_form": "Pi_M^top J_H = Pi_M^H J_H + dB_H + R_PiH",
            "current_status": "EQUIVALENCE_NOT_DERIVED",
            "missing_for_claim": "R_PiH theorem-zero or source-backed bound plus B_H flux rule",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "adoption_id": "HCG1794_4_downstream_debt",
            "required_piece": "Hamiltonian Pi_M adoption does not itself prove Newton/GR",
            "mathematical_form": "adoption + integrability + source-measure glue + Gauss/Poisson + PPN vector all required",
            "current_status": "DEBT_RETAINED",
            "missing_for_claim": "source-measure, Gauss/orbital and PPN rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "adoption_id": "HCG1794_5_verdict",
            "required_piece": "claim-grade Hamiltonian Pi_M adoption",
            "mathematical_form": "HCG1794_0 through HCG1794_4 pass in one parent action with no circular source normalization",
            "current_status": "HAMILTONIAN_PIM_NOT_CLAIM_GRADE",
            "missing_for_claim": "adoption/equivalence, R_PiH, boundary flux and downstream source-measure rows",
            "valid_for_claim": False,
        },
    ]


def commutator_glue_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CGA1794_0_Hilbert_topological_equality",
            "object": "Pi_M J_H equality target",
            "mathematical_form": "Pi_M J_H = J_M_top + dB_zero + R_eq",
            "current_status": "R_EQ_NOT_PARENT_DERIVED_ZERO",
            "what_survives": "closed topological current can be the wrong conserved object",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CGA1794_1_product_rule",
            "object": "Pi_M commutator",
            "mathematical_form": "d(Pi_M J_H)=Pi_M dJ_H+[d,Pi_M]J_H",
            "current_status": "IDENTITY_RETAINED",
            "what_survives": "dropping the commutator would be algebraic handwaving",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CGA1794_2_fixed_chainmap",
            "object": "commutator-zero route",
            "mathematical_form": "fixed topological chain-map implies [d,Pi_M]J_H=0",
            "current_status": "VALID_CONDITIONAL_MATH_ONLY",
            "what_survives": "parent-fixed domain, metric-independent Pi_M and physical current domain are not signed",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CGA1794_3_worldtube_glue",
            "object": "same Hilbert worldtube source",
            "mathematical_form": "W_source = supp(delta S_matter/delta e_obs); linked surfaces enclose same W_source",
            "current_status": "WORLDTUBE_GLUE_NOT_CURRENT_MTS_DERIVED",
            "what_survives": "mass charge can be chosen after the fit or on the wrong source object",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CGA1794_4_boundary_reference",
            "object": "exact and reference terms",
            "mathematical_form": "Pi_M J_H - J_M_top = dB_zero and int_boundary dB_zero = 0",
            "current_status": "MISSING_CERTIFICATE_OR_BOUND",
            "what_survives": "mass equality shifts by boundary bookkeeping",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CGA1794_5_extra_sector_charge_silence",
            "object": "extra sector charge",
            "mathematical_form": "Delta_nonEH = Delta_extra = Delta_symp = Delta_frame = 0 in compact local exterior",
            "current_status": "FIELD_SPECIFIC_SILENCE_QUEUE_OPEN",
            "what_survives": "M_eff can drift or receive hidden non-GR source charge",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CGA1794_6_verdict",
            "object": "Pi_M equality/commutator/glue bundle",
            "mathematical_form": "R_eq=0, [d,Pi_M]J_H=0, int dB_zero=0, same worldtube, no extra sector charge",
            "current_status": "PIM_GLUE_BUNDLE_NOT_CLOSED",
            "what_survives": "finite Delta_Hsrc and source-normalization residual rows remain required",
            "valid_for_claim": False,
        },
    ]


def finite_y5_pack_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "pack_id": "Y5P1794_0_identity",
            "row_type": "branch identity",
            "required_field": "model_id;component_family",
            "current_value": "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428;PiM_observed_time_Y5_pack",
            "units_required": "not applicable",
            "row_status": "CONTRACT_ONLY",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "Y5P1794_1_tau_obs",
            "row_type": "observed-time finite residual",
            "required_field": "tau_obs selection/normalization residual",
            "current_value": "MISSING_TAU_OBS_PARENT_SELECTION_OR_BOUND",
            "units_required": "time-normalization convention and clock/source path",
            "row_status": "MISSING_INPUT",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "Y5P1794_2_R_eq",
            "row_type": "Hilbert/topological equality residual",
            "required_field": "R_eq_integral or theorem-zero certificate",
            "current_value": "MISSING_R_EQ_ZERO_OR_BOUND",
            "units_required": "mass/charge units normalized by M_H_ref",
            "row_status": "MISSING_INPUT",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "Y5P1794_3_I_commutator",
            "row_type": "Pi_M commutator residual",
            "required_field": "I_commutator = integral_A [d,Pi_M]J_H or zero theorem",
            "current_value": "MISSING_COMMUTATOR_ZERO_OR_BOUND",
            "units_required": "mass/charge flux units with source path",
            "row_status": "MISSING_INPUT",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "Y5P1794_4_boundary_reference",
            "row_type": "boundary/reference residual",
            "required_field": "B_H flux and reference C-term",
            "current_value": "MISSING_BOUNDARY_REFERENCE_ZERO_OR_BOUND",
            "units_required": "mass/charge boundary contribution units",
            "row_status": "MISSING_INPUT",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "Y5P1794_5_extra_charge_channels",
            "row_type": "extra source charge residual",
            "required_field": "Delta_nonEH;Delta_extra;Delta_symp;Delta_frame;Delta_cal;Delta_PPN",
            "current_value": "MISSING_EXTRA_CHARGE_ZERO_OR_VECTOR",
            "units_required": "dimensionless epsilon_mu components or mass/charge units",
            "row_status": "MISSING_INPUT",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "Y5P1794_6_MHref",
            "row_type": "normalization denominator",
            "required_field": "positive M_H_ref with same tau/source/charge/readout frame",
            "current_value": "MISSING_TAU_MHREF_LOCK",
            "units_required": "mass units and frame convention",
            "row_status": "MISSING_INPUT",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "Y5P1794_7_acceptance",
            "row_type": "acceptance gate",
            "required_field": "Pi_M/tau theorem bundle or complete finite Y5 residual vector",
            "current_value": "NEITHER_CONDITION_MET",
            "units_required": "all units explicit; all source paths exist",
            "row_status": "REJECT_CURRENT_Y5_PACK",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def countermodel_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1794_0_post_readout_tau",
            "countermodel": "tau_obs is selected or normalized after orbital/source readout and absorbs residuals",
            "survives_current_constraints": True,
            "why_survives": "pre-readout tau selection and clock normalization are not parent-signed",
            "what_kills_it": "parent-selected observed-time generator with same-frame clock normalization",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1794_1_wrong_closed_charge",
            "countermodel": "old/topological Pi_M conserves a charge that is not the Hilbert/Noether measured source mass",
            "survives_current_constraints": True,
            "why_survives": "R_eq and old-vs-Hamiltonian Pi_M equivalence are not derived",
            "what_kills_it": "Pi_M^top equals Pi_M^H up to zero exact/reference terms",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1794_2_commutator_hair",
            "countermodel": "[d,Pi_M]J_H creates finite source-normalization or radial mass hair",
            "survives_current_constraints": True,
            "why_survives": "commutator-zero theorem is conditional only",
            "what_kills_it": "parent-fixed topological chain-map on the physical Hilbert current domain",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1794_3_boundary_reference_shift",
            "countermodel": "boundary/reference terms shift source mass equality",
            "survives_current_constraints": True,
            "why_survives": "B_H flux and reference C-term are missing zero certificates",
            "what_kills_it": "zero exact/reference theorem or finite bounded row",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1794_4_extra_charge_channel",
            "countermodel": "non-EH, memory, boundary, frame or PPN channels carry independent source charge",
            "survives_current_constraints": True,
            "why_survives": "extra-sector charge silence remains open",
            "what_kills_it": "channelwise zero theorem or complete finite source-charge vector",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1794_0_parent_PiM_tau",
            "claim": "Pi_M and observed-time generator are parent-owned",
            "status": "BLOCKED",
            "reason": "tau_obs, clock normalization, same-frame rule, pre-readout selection and Pi_M adoption remain unsigned",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1794_1_Hamiltonian_PiM_adopted",
            "claim": "Hamiltonian Pi_M^H is active claim-grade source mass projector",
            "status": "BLOCKED",
            "reason": "charge functional, representative, source-measure lemma and old-PiM equivalence are not parent-signed",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1794_2_commutator_glue_zero",
            "claim": "R_eq, [d,Pi_M]J_H and boundary/reference terms vanish",
            "status": "BLOCKED",
            "reason": "fixed chain-map, physical current domain, worldtube glue and boundary certificates are missing",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1794_3_finite_Y5_score",
            "claim": "finite Y5 source-normalization rows are score-ready",
            "status": "BLOCKED",
            "reason": "finite Y5 pack is rejected for missing tau, R_eq, commutator, boundary, extra-charge and M_H_ref rows",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1794_4_source_normalized_Newton",
            "claim": "source-normalized Newton is derived",
            "status": "BLOCKED",
            "reason": "Pi_M/tau owner gate fails and Gauss/orbital calibration is downstream",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1794_5_local_GR",
            "claim": "local GR/Newton reduction is derived",
            "status": "BLOCKED",
            "reason": "Y5 source charge, Y6 stress, q_loc, c_R2 and PPN gates are not jointly closed",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1794_0_PiM_route",
            "decision": "HAMILTONIAN_PIM_ROUTE_RETAINED_NOT_ACTIVATED",
            "reason": "Pi_M^H is the best route for avoiding wrong-charge/topological shortcut, but adoption and source-measure equality are not parent-signed",
            "next_action": "try to sign adoption/equivalence or retain Delta_Hsrc components",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1794_1_tau_obs",
            "decision": "OBSERVED_TIME_GENERATOR_NOT_PARENT_SELECTED",
            "reason": "stationary/quasilocal certificate, clock normalization, same-frame rule and pre-readout selection are missing",
            "next_action": "target tau_obs normalization alongside Pi_M adoption",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1794_2_finite_pack",
            "decision": "FINITE_Y5_PACK_REJECTED_NONCLAIM",
            "reason": "tau, R_eq, commutator, boundary, extra charge and M_H_ref rows are not filled",
            "next_action": "use pack as residual schema only",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1794_3_next",
            "decision": "HAMILTONIAN_PIM_ADOPTION_OR_DELTA_HSRC_COMPONENT_PACK_NEXT",
            "reason": "the central unresolved object is Delta_Hsrc: source-measure equality fails unless Pi_M^H adoption/equivalence, boundary, commutator and reference terms close",
            "next_action": "build 1795 Hamiltonian Pi_M adoption/equivalence or Delta_Hsrc residual component pack",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1794_0_primary",
            "next_target": "1795-Y5-R2FR-Hamiltonian-PiM-adoption-or-Delta-Hsrc-component-pack.md",
            "script": "scripts/Y5_R2FR_Hamiltonian_PiM_adoption_or_Delta_Hsrc_component_pack.py",
            "objective": "try to sign Hamiltonian Pi_M adoption/equivalence in the active branch; if not, emit Delta_Hsrc residual components for R_eq, commutator, boundary/reference, extra charge and M_H_ref with units",
            "selection_status": "selected",
            "success_condition": "parent-signed Pi_M^H adoption/equivalence and source-measure lemma, or complete nonclaim Delta_Hsrc component pack",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1794_1_parallel_tau",
            "next_target": "1795b-Y5-R2FR-observed-time-generator-clock-normalization-gate.md",
            "script": "scripts/Y5_R2FR_observed_time_generator_clock_normalization_gate.py",
            "objective": "derive tau_obs from parent boundary/clock data with same-frame and pre-readout normalization",
            "selection_status": "held_parallel",
            "success_condition": "parent-selected tau_obs or finite tau residual row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1794_2_parallel_Gauss",
            "next_target": "1795c-Y5-R2FR-Gauss-orbital-readout-after-source-measure.md",
            "script": "scripts/Y5_R2FR_Gauss_orbital_readout_after_source_measure.py",
            "objective": "hold Gauss/orbital calibration until source-measure equality is owned",
            "selection_status": "held_until_source_measure",
            "success_condition": "inverse-square source-normalized Newton readout or finite residual rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "pim_observed_time_gate": pim_observed_time_gate_rows(),
        "hamiltonian_pim_adoption_gate": hamiltonian_pim_adoption_gate_rows(),
        "commutator_glue_audit": commutator_glue_audit_rows(),
        "finite_y5_pack": finite_y5_pack_rows(),
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
        shutil.copy2(path, RAB_QUEUE / f"JR1794_{key.upper()}.csv")


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
        if not (RAB_QUEUE / f"JR1794_{key.upper()}.csv").exists():
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
        ("VAL1794_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1794_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1794_2_pim_tau_gate_blocks",
            any(row["gate_id"] == "POT1794_6_verdict" and row["current_status"] == "PIM_OBSERVED_TIME_NOT_PARENT_OWNED" for row in rows_map["pim_observed_time_gate"])
            and all(not boolish(row["parent_signed"]) and not boolish(row["valid_for_claim"]) for row in rows_map["pim_observed_time_gate"]),
            "Pi_M/observed-time gate is blocked",
        ),
        (
            "VAL1794_3_hamiltonian_adoption_blocks",
            any(row["adoption_id"] == "HCG1794_5_verdict" and row["current_status"] == "HAMILTONIAN_PIM_NOT_CLAIM_GRADE" for row in rows_map["hamiltonian_pim_adoption_gate"]),
            "Hamiltonian Pi_M adoption is not claim-grade",
        ),
        (
            "VAL1794_4_commutator_glue_blocks",
            any(row["audit_id"] == "CGA1794_6_verdict" and row["current_status"] == "PIM_GLUE_BUNDLE_NOT_CLOSED" for row in rows_map["commutator_glue_audit"]),
            "Pi_M equality/commutator/glue bundle remains open",
        ),
        (
            "VAL1794_5_finite_pack_rejected",
            any(row["pack_id"] == "Y5P1794_7_acceptance" and row["row_status"] == "REJECT_CURRENT_Y5_PACK" for row in rows_map["finite_y5_pack"])
            and all(not boolish(row["score_ready"]) and not boolish(row["valid_prediction_row"]) for row in rows_map["finite_y5_pack"]),
            "finite Y5 pack is rejected and non-scoreable",
        ),
        (
            "VAL1794_6_countermodels_retained",
            all(boolish(row["survives_current_constraints"]) for row in rows_map["countermodel_ledger"]),
            "countermodels remain live",
        ),
        (
            "VAL1794_7_claim_gates_blocked",
            all(row["status"] == "BLOCKED" and not boolish(row["gate_pass"]) and not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "claim gates are blocked",
        ),
        ("VAL1794_8_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1794_9_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1794_10_decision_next",
            any(
                row["decision_id"] == "DEC1794_3_next"
                and row["decision"] == "HAMILTONIAN_PIM_ADOPTION_OR_DELTA_HSRC_COMPONENT_PACK_NEXT"
                for row in rows_map["decision_ledger"]
            ),
            "decision selects Hamiltonian Pi_M adoption or Delta_Hsrc pack next",
        ),
        (
            "VAL1794_11_next_selected",
            any(row["route_id"] == "NEXT1794_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1794_12_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1794 CSVs parse"),
        ("VAL1794_13_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1794_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1794_15_formalization_untouched", formalization_untouched(), "no 1794 outputs found under formalization-workbench"),
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
            "check_id": "VAL1794_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1794 parent Pi_M observed-time generator or finite Y5 pack checkpoint",
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
            "# 1794 - Y5/R2FR Parent PiM Observed-Time Generator or Finite Y5 Pack",
            "",
            "## Verdict",
            "",
            "1794 narrows the source-normalized Newton route to the actual parent objects. The mass projector cannot be a post-readout mask: it must be `Pi_M^H`, a Hamiltonian/covariant-phase-space mass charge map, or the old/topological `Pi_M` must be proven equivalent to it. The observed time generator `tau_obs` must also be selected and normalized by parent boundary/clock data before orbital/source readout.",
            "",
            "The current corpus does not sign those clauses. The Hamiltonian `Pi_M` route remains the best non-cheating route, but it is not claim-grade: adoption/equivalence, source-measure lemma, commutator zero, boundary/reference zero, and extra-charge silence remain open. Therefore 1794 emits a finite nonclaim `Y5` pack around `Delta_Hsrc` rather than pretending measured GM is derived.",
            "",
            "**Claim ceiling:** no parent `Pi_M/tau_obs` claim, no Hamiltonian `Pi_M` adoption claim, no source-normalized Newton, no finite `Y5` score, no local-GR/Newton claim, no GitHub action, and no `formalization-workbench` edit is allowed from 1794.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## PiM Observed-Time Gate",
            markdown_table(rows_map["pim_observed_time_gate"], ["gate_id", "required_clause", "mathematical_form", "current_status", "blocking_gap", "valid_for_claim"]),
            "",
            "## Hamiltonian PiM Adoption Gate",
            markdown_table(rows_map["hamiltonian_pim_adoption_gate"], ["adoption_id", "required_piece", "mathematical_form", "current_status", "missing_for_claim", "valid_for_claim"]),
            "",
            "## Commutator Glue Audit",
            markdown_table(rows_map["commutator_glue_audit"], ["audit_id", "object", "mathematical_form", "current_status", "what_survives", "valid_for_claim"]),
            "",
            "## Finite Y5 Pack",
            markdown_table(rows_map["finite_y5_pack"], ["pack_id", "row_type", "required_field", "current_value", "units_required", "row_status", "score_ready", "valid_prediction_row", "valid_for_claim"]),
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
            "This is one of the cleanest gates so far. The work now knows exactly where source-normalized Newton lives: in `Delta_Hsrc`. Either `Pi_M^H` is adopted/equivalent in the parent action and `Delta_Hsrc=0`, or `Delta_Hsrc` becomes a finite residual vector. That is much stronger than hiding behind an orbital GM fit.",
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
    print(f"1794 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
