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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1793"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1793_0_1792_doc",
        "source_key": "1792_handoff",
        "source_path": ROOT / "1792-Y5-R2FR-source-functional-evenness-and-JZ-BZ-coupling-lock-or-profile-acquisition.md",
        "needles": ["DEC1792_3_next", "NEXT1792_0_primary"],
        "role": "selects Y5 source-charge owner and Y6 extra-stress gate as 1793 target",
    },
    {
        "source_id": "SRC1793_1_1792_validation",
        "source_key": "1792_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1792_VALIDATION.csv",
        "needles": ["VAL1792_OVERALL", "PASS"],
        "role": "confirms 1792 passed",
    },
    {
        "source_id": "SRC1793_2_1792_component_gate",
        "source_key": "1792_component_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1792_COMPONENT_COUPLING_GATE.csv",
        "needles": ["CCG1792_3_Y5_source_normalization", "CCG1792_4_Y6_extra_stress"],
        "role": "identifies Y5 and Y6 as hard coupling blockers",
    },
    {
        "source_id": "SRC1793_3_1792_acquisition",
        "source_key": "1792_acquisition",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1792_JZ_BZ_ACQUISITION_LEDGER.csv",
        "needles": ["ACQ1792_2_Y5_source_normalization", "ACQ1792_3_Y6_extra_stress"],
        "role": "names finite Y5/Y6 coefficient debt",
    },
    {
        "source_id": "SRC1793_4_y5_owner",
        "source_key": "y5_owner_theorem",
        "source_path": RESIDUALS / "P8_Y5_SOURCE_NORMALIZATION_OWNER_THEOREM.csv",
        "needles": ["Y5O_3_parent_source_charge", "Y5O_8_owner_theorem"],
        "role": "source-normalization owner theorem requirements",
    },
    {
        "source_id": "SRC1793_5_source_current_closure",
        "source_key": "source_current_closure",
        "source_path": RESIDUALS / "P8_Y5_SOURCE_CURRENT_CLOSURE_THEOREM_ATTEMPT.csv",
        "needles": ["SC532_2_charge_current_variation_identity", "SC532_7_measured_GM_next_gate"],
        "role": "charge-current equality and downstream measured-GM gate",
    },
    {
        "source_id": "SRC1793_6_ward_bridge",
        "source_key": "ward_bridge",
        "source_path": RESIDUALS / "P8_Y5_SOURCE_CURRENT_WARD_BRIDGE.csv",
        "needles": ["WB520_4_exact_product_obstruction", "WB520_6_conditional_closure_theorem"],
        "role": "projected mass-current closure obstruction and conditional theorem",
    },
    {
        "source_id": "SRC1793_7_source_measure_flux",
        "source_key": "source_measure_flux",
        "source_path": RESIDUALS / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
        "needles": ["T509_0_charge_identity_needed", "T509_2_no_extra_mass_channel"],
        "role": "measured source mass needs charge identity and no extra mass channel",
    },
    {
        "source_id": "SRC1793_8_source_calibrated_EH",
        "source_key": "source_calibrated_EH",
        "source_path": RESIDUALS / "P8_Y5_SOURCE_CALIBRATED_EH_PROOF_STACK.csv",
        "needles": ["SCEH529_3_measured_mu_calibration", "SCEH529_7_beta_local_GR_gate"],
        "role": "EH mass-family to measured-GM and PPN stack",
    },
    {
        "source_id": "SRC1793_9_source_calibrated_blockers",
        "source_key": "source_calibrated_blockers",
        "source_path": RESIDUALS / "P8_Y5_SOURCE_CALIBRATED_EH_BLOCKERS.csv",
        "needles": ["BL529_1_measured_GM", "BL529_3_boundary_domain_projector"],
        "role": "measured-GM and projector/domain blockers",
    },
    {
        "source_id": "SRC1793_10_yloc_component",
        "source_key": "yloc_component_audit",
        "source_path": RESIDUALS / "P8_YLOC_NO_LINEAR_SOURCE_COMPONENT_AUDIT.csv",
        "needles": ["Y5_source_normalization", "Y6_stress_Bianchi"],
        "role": "older component audit agrees Y5/Y6 are not zeroed",
    },
    {
        "source_id": "SRC1793_11_projector_stress",
        "source_key": "1772_projector_stress",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1772_PROJECTOR_STRESS_AUDIT.csv",
        "needles": ["PSA1772_1_T_PiM", "PSA1772_4_verdict"],
        "role": "projector stress map is missing and remains retained",
    },
    {
        "source_id": "SRC1793_12_projector_gate",
        "source_key": "1514_projector_stress",
        "source_path": RESIDUALS / "P8_Y5_PARENT_GENERATOR_1514_PROJECTOR_STRESS_GATE.csv",
        "needles": ["PS1514_0_exact_conditional", "PS1514_4_verdict"],
        "role": "projector stress zero has a conditional topological route but is not parent-owned",
    },
    {
        "source_id": "SRC1793_13_bianchi_gate",
        "source_key": "908_bianchi_gate",
        "source_path": RESIDUALS / "P8_Y5_R10_908_BIANCHI_WARD_GATE.csv",
        "needles": ["BWG908_0_contract", "BWG908_3_local_GR_limit"],
        "role": "Bianchi/Ward gate says projector stress must be zero, cancelled, or retained",
    },
    {
        "source_id": "SRC1793_14_projector_fate",
        "source_key": "908_projector_fate",
        "source_path": RESIDUALS / "P8_Y5_R10_908_PROJECTOR_STRESS_FATE_AUDIT.csv",
        "needles": ["PFA908_3_Hamiltonian_PiM_route", "PFA908_4_retained_residual"],
        "role": "Hamiltonian Pi_M route is promising but not closed",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1793_SOURCE_REGISTER.csv",
    "y5_source_charge_owner_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1793_Y5_SOURCE_CHARGE_OWNER_ATTEMPT.csv",
    "source_mass_flux_chain": RESIDUALS / "P8_Y5_PARENT_QLOC_1793_SOURCE_MASS_FLUX_CHAIN.csv",
    "y6_extra_stress_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1793_Y6_EXTRA_STRESS_GATE.csv",
    "finite_y5y6_coupling_pack": RESIDUALS / "P8_Y5_PARENT_QLOC_1793_FINITE_Y5Y6_COUPLING_PACK.csv",
    "countermodel_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1793_COUNTERMODEL_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1793_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1793_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1793_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1793_VALIDATION.csv",
}

DOC_PATH = ROOT / "1793-Y5-R2FR-Y5-source-charge-owner-and-Y6-extra-stress-gate-or-finite-coupling-pack.md"


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


def y5_source_charge_owner_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "owner_id": "Y5SC1793_0_observable_split",
            "required_clause": "observed local source strength is split into parent source charge plus explicit extra source-normalization channels",
            "mathematical_form": "mu_obs = G_eff M_H[Pi_M J_H] + mu_extra = G_eff M_H(1 + epsilon_mu)",
            "if_closed": "Y5 cannot hide as fitted GM; deviations are theorem-zero or finite residual rows",
            "current_status": "DEFINITION_WRITTEN_NOT_PARENT_DERIVED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "Y5SC1793_1_same_observed_coframe",
            "required_clause": "matter, clocks, photons, source current, exterior charge and orbital readout use one observed coframe",
            "mathematical_form": "e_obs = e_matter = e_source = e_charge = e_orbit",
            "if_closed": "source normalization cannot hide in a frame split",
            "current_status": "NOT_PARENT_DERIVED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "Y5SC1793_2_parent_source_charge",
            "required_clause": "measured source mass is a parent Noether/Hamiltonian/Hilbert charge before orbital fitting",
            "mathematical_form": "M_H[W] = integral_S Q_M[tau] = (4*pi*G_ref)^-1 integral_S Pi_M J_H",
            "if_closed": "M_eff has a source-side owner before Kepler readout",
            "current_status": "NOT_PARENT_DERIVED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "Y5SC1793_3_flux_closure",
            "required_clause": "projected Hilbert mass current is closed in compact source-free exterior regions",
            "mathematical_form": "M_H(S2)-M_H(S1)=integral_A d(Pi_M J_H); d(Pi_M J_H)=0",
            "if_closed": "no radial M_eff hair or local source-mass drift survives",
            "current_status": "NOT_DERIVED_PROJECTOR_COMMUTATOR_OPEN",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "Y5SC1793_4_no_extra_mass_projection",
            "required_clause": "non-EH, boundary, domain, projector, memory, frame, species, calibration and PPN channels carry no independent mass projection",
            "mathematical_form": "mu_extra = Delta_nonEH + Delta_symp + Delta_PiM + Delta_extra + Delta_frame + Delta_cal + Delta_PPN = 0",
            "if_closed": "epsilon_mu=0 rather than tuned source-normalization cancellation",
            "current_status": "NOT_DERIVED_EXTRA_MASS_CHANNELS_ACTIVE",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "Y5SC1793_5_Gauss_orbital_calibration",
            "required_clause": "closed parent charge normalizes to inverse-square orbital coefficient with one universal G_ref",
            "mathematical_form": "nabla^2 Phi = 4*pi*G_ref rho_H; r^2|a_r| = G_ref M_H",
            "if_closed": "Kepler/Newton measured GM becomes consequence, not input",
            "current_status": "DOWNSTREAM_GATE_OPEN",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "Y5SC1793_6_second_order_PPN_stability",
            "required_clause": "same source charge remains stable through beta/gamma/preferred-frame PPN order",
            "mathematical_form": "Delta_PPN_source = {gamma-1,beta-1,alpha_i,xi,zeta_i}_source = 0 or explicitly bounded",
            "if_closed": "local Newton does not pass while local GR quietly fails at second order",
            "current_status": "NOT_DERIVED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "Y5SC1793_7_verdict",
            "required_clause": "Y5 source-normalization owner theorem",
            "mathematical_form": "Y5SC1793_1 through Y5SC1793_6 all close together => mu_obs=G0 M_H, d ln mu_obs=0, epsilon_mu=0, Y5=0",
            "if_closed": "source-normalized Newton becomes derived rather than fitted",
            "current_status": "SOURCE_CHARGE_OWNER_THEOREM_NOT_ACTIVATED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
    ]


def source_mass_flux_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "chain_id": "MFC1793_0_Hilbert_source_current",
            "identity": "same coframe defines a Hilbert/source current before orbital fitting",
            "mathematical_form": "J_H[tau] := T_m^{mu nu}[e_obs] tau_nu dSigma_mu",
            "current_status": "CONDITIONAL_SOURCE_CURRENT_DEFINED_NOT_MASS_CLOSED",
            "missing_piece": "parent-defined mass projector and mass generator",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "chain_id": "MFC1793_1_Ward_conservation",
            "identity": "diffeomorphism invariance gives stress conservation on matter equations",
            "mathematical_form": "E_psi=0 and delta_xi S_m=0 => nabla_mu T_m^{mu nu}=0",
            "current_status": "STANDARD_CONDITIONAL",
            "missing_piece": "does not select a closed scalar mass-channel current by itself",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "chain_id": "MFC1793_2_observed_time_generator",
            "identity": "stress conservation becomes mass-current conservation only after an observed-time generator is owned",
            "mathematical_form": "j_M^mu := T_m^{mu nu} tau_nu; nabla_mu j_M^mu = T_m^{mu nu} nabla_(mu tau_nu)",
            "current_status": "OBSERVED_TIME_GENERATOR_NOT_PARENT_DERIVED",
            "missing_piece": "stationary/Hamiltonian tau or boundary charge generator",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "chain_id": "MFC1793_3_projected_current_obstruction",
            "identity": "projected mass current has a product-rule obstruction",
            "mathematical_form": "d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H",
            "current_status": "OBSTRUCTION_ACTIVE",
            "missing_piece": "Pi_M parent origin, commutator silence and no projected exchange",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "chain_id": "MFC1793_4_extra_exchange_obstruction",
            "identity": "even conserved Hilbert source can exchange mass projection with non-Hilbert sectors",
            "mathematical_form": "d(Pi_M J_H)=-Pi_M dJ_extra + [d,Pi_M]J_H + A_parent",
            "current_status": "EXTRA_EXCHANGE_ACTIVE",
            "missing_piece": "zero extra projection, zero boundary flux and zero anomaly",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "chain_id": "MFC1793_5_conditional_closure",
            "identity": "conditional source mass closure theorem",
            "mathematical_form": "Ward_M + D Pi_M=0 + Pi_M dJ_extra=0 + A_parent=0 => d(Pi_M J_H)=0",
            "current_status": "EXACT_CONDITIONAL_NOT_MTS_DERIVED",
            "missing_piece": "current proof of all premises",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "chain_id": "MFC1793_6_measured_GM_calibration",
            "identity": "closed source charge must still calibrate to measured orbital GM",
            "mathematical_form": "nabla^2 Phi=4*pi G_eff rho_H; surface_int grad Phi dS=4*pi G_eff M_H; r^2|a_r|=G_eff M_H",
            "current_status": "DOWNSTREAM_GATE_OPEN",
            "missing_piece": "Gauss/orbital readout and PPN stability",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "chain_id": "MFC1793_7_verdict",
            "identity": "source mass flux chain for Y5",
            "mathematical_form": "MFC1793_0 through MFC1793_6 all close",
            "current_status": "MASS_FLUX_CHAIN_NOT_CLOSED",
            "missing_piece": "Pi_M, observed time, commutator, extra projection and orbital calibration",
            "valid_for_claim": False,
        },
    ]


def y6_extra_stress_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "stress_id": "Y6G1793_0_Bianchi_contract",
            "statement": "Bianchi/Ward identity requires total stress conservation",
            "mathematical_form": "nabla_mu(T_matter + T_EH + T_MTS + T_boundary + T_projector + T_extra)^{mu nu}=0",
            "current_status": "IDENTITY_CONTRACT_EXPLICIT",
            "needed_for_zero": "individual extra/projector stress must be zero, pure improvement, cancelled by owned exchange current, or retained",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "stress_id": "Y6G1793_1_topological_projector_route",
            "statement": "metric-independent topological projector can have zero bulk stress only if parent-owned",
            "mathematical_form": "delta_g Pi_M=0 and [d,Pi_M]J_H=0 with fixed domain/homology",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "needed_for_zero": "parent ownership, Hilbert equality, boundary/local projection silence",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "stress_id": "Y6G1793_2_projector_stress_map",
            "statement": "projector stress must be mapped or zeroed",
            "mathematical_form": "T_PiM^{mu nu} := -2/sqrt(-g) delta S_PiM/delta g_munu",
            "current_status": "MISSING_PROJECTOR_STRESS_MAP",
            "needed_for_zero": "show T_PiM=0 or supply PPN/source-stress response rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "stress_id": "Y6G1793_3_exchange_carrier",
            "statement": "nonzero projector divergence needs an exchange carrier or residual map",
            "mathematical_form": "find T_Q^{mu nu} with nabla_mu T_Q^{mu nu}=-q_P^nu, or prove q_P^nu=0",
            "current_status": "NOT_DERIVED",
            "needed_for_zero": "owned exchange current or q_P zero theorem",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "stress_id": "Y6G1793_4_local_GR_projection",
            "statement": "local GR requires projector/extra stress suppression or sourced projection into arenas",
            "mathematical_form": "q_P^nu -> {gamma-1,beta-1,alpha_i,xi,Gdot/G,anomalous acceleration,clocks,R10}",
            "current_status": "BOUND_INTERFACE_NEEDED",
            "needed_for_zero": "zero theorem or finite projection coefficients with units",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "stress_id": "Y6G1793_5_verdict",
            "statement": "Y6 extra-stress gate",
            "mathematical_form": "Y6G1793_1 through Y6G1793_4 close with source paths",
            "current_status": "Y6_EXTRA_STRESS_NOT_ZEROED",
            "needed_for_zero": "topological/projector-null theorem or finite PPN/source-stress rows",
            "valid_for_claim": False,
        },
    ]


def finite_y5y6_coupling_pack_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "pack_id": "FY1793_0_identity",
            "row_type": "branch identity",
            "required_field": "model_id;component_family",
            "current_value": "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428;Y5_Y6_coupling_pack",
            "units_required": "not applicable",
            "row_status": "CONTRACT_ONLY",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "FY1793_1_Y5_Gdot",
            "row_type": "Y5 finite source-normalization",
            "required_field": "d ln mu_obs/dt or d ln G_eff/dt",
            "current_value": "MISSING_GDOT_SOURCE_COEFFICIENT",
            "units_required": "1/time with source path and clock/orbital convention",
            "row_status": "MISSING_INPUT",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "FY1793_2_Y5_radial_range",
            "row_type": "Y5 finite radial/range source hair",
            "required_field": "d ln M_eff/dr; lambda/range dependence",
            "current_value": "MISSING_RADIAL_RANGE_SOURCE_COEFFICIENTS",
            "units_required": "1/length, SI lambda, and dimensionless alpha-like projection if applicable",
            "row_status": "MISSING_INPUT",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "FY1793_3_Y5_species_frame",
            "row_type": "Y5 finite species/frame/domain source hair",
            "required_field": "species/material charge vector; frame/domain derivative",
            "current_value": "MISSING_SPECIES_FRAME_DOMAIN_COEFFICIENTS",
            "units_required": "dimensionless material charges plus frame/domain derivative convention",
            "row_status": "MISSING_INPUT",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "FY1793_4_Y5_mu_extra_PPN",
            "row_type": "Y5 finite mu_extra and PPN source projection",
            "required_field": "mu_extra; Delta_beta_source; Delta_gamma_source; alpha_i_source; xi_source",
            "current_value": "MISSING_MU_EXTRA_PPN_SOURCE_VECTOR",
            "units_required": "dimensionless PPN/source-normalization vector",
            "row_status": "MISSING_INPUT",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "FY1793_5_Y6_Textra_PPN",
            "row_type": "Y6 finite extra-stress projection",
            "required_field": "T_extra^{mu nu}; Pi_PPN T_extra; stress response coefficients",
            "current_value": "MISSING_TEXTRA_PPN_STRESS_VECTOR",
            "units_required": "stress-energy units plus dimensionless PPN projection",
            "row_status": "MISSING_INPUT",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "FY1793_6_Y6_qP_Khat_q_loc",
            "row_type": "Y6 finite Ward/Khat/q_loc projection",
            "required_field": "q_P^nu; Delta_K[Y6]; q_loc projection",
            "current_value": "MISSING_QP_KHAT_QLOC_PROJECTION",
            "units_required": "force-density/stress-divergence units and arena conversion",
            "row_status": "MISSING_INPUT",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "FY1793_7_acceptance",
            "row_type": "acceptance gate",
            "required_field": "Y5/Y6 theorem-zero bundle or complete finite numeric/source-backed rows",
            "current_value": "NEITHER_CONDITION_MET",
            "units_required": "all units explicit; all source paths exist",
            "row_status": "REJECT_CURRENT_Y5Y6_COUPLING_PACK",
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
            "countermodel_id": "CM1793_0_orbital_fit_mass",
            "countermodel": "M_eff is only an orbital fit and not a parent Hilbert/Noether source charge",
            "survives_current_constraints": True,
            "why_survives": "parent source charge and Gauss/orbital calibration are not derived",
            "what_kills_it": "M_H equals parent charge and calibrates to r^2|a_r|/G_ref before fitting",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1793_1_projector_commutator_mass_hair",
            "countermodel": "[d,Pi_M]J_H produces radial or source-normalization mass hair",
            "survives_current_constraints": True,
            "why_survives": "Pi_M origin and commutator silence are open",
            "what_kills_it": "parent topological/Hamiltonian Pi_M with zero commutator",
        },
        {
            "branch_id": "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428",
            "countermodel_id": "CM1793_2_extra_mass_projection",
            "countermodel": "non-EH, boundary, domain, memory, frame or calibration sectors carry independent mass projection",
            "survives_current_constraints": True,
            "why_survives": "no-extra-mass-projection theorem is not derived",
            "what_kills_it": "channelwise zero theorem or finite coefficient bounds",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1793_3_projector_extra_stress",
            "countermodel": "projector/domain stress is conserved or exchanged but nonzero in PPN/local arenas",
            "survives_current_constraints": True,
            "why_survives": "Bianchi/Ward ownership does not prove stress silence",
            "what_kills_it": "topological/projector-null theorem or finite stress-response rows",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1793_4_second_order_source_slip",
            "countermodel": "Newtonian source charge looks closed but beta/gamma/preferred-frame source terms fail at second PPN order",
            "survives_current_constraints": True,
            "why_survives": "PPN source stability is not derived",
            "what_kills_it": "source charge stable through beta/gamma/alpha_i/xi/zeta_i or finite PPN source vector",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1793_0_Y5_source_charge_owner",
            "claim": "Y5 source-normalization is theorem-zero",
            "status": "BLOCKED",
            "reason": "source charge owner chain lacks parent Pi_M, observed time, flux closure, no-extra-projection and orbital/PPN calibration",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1793_1_Y6_extra_stress_zero",
            "claim": "Y6 extra stress is absent or projector-null",
            "status": "BLOCKED",
            "reason": "projector stress map and topological/projector-null theorem are not parent-signed",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1793_2_no_linear_source",
            "claim": "J_Z[Y5] and J_Z[Y6] vanish",
            "status": "BLOCKED",
            "reason": "Y5/Y6 owner gates remain open",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1793_3_finite_Y5Y6_scores",
            "claim": "finite Y5/Y6 coupling rows can be scored",
            "status": "BLOCKED",
            "reason": "finite coupling pack is rejected for missing coefficients, units and arena maps",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1793_4_q_loc_cR2_R10_PPN",
            "claim": "q_loc/c_R2/R10/PPN scores can run from Y5/Y6 pack",
            "status": "BLOCKED",
            "reason": "Y5/Y6 source vectors are not theorem-zero or finite source-backed",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1793_5_local_GR_Newton",
            "claim": "derived local GR/Newton reduction",
            "status": "BLOCKED",
            "reason": "source-normalized Newton and extra-stress gates are not jointly closed",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1793_0_Y5_chain",
            "decision": "Y5_SOURCE_CHARGE_CHAIN_WRITTEN_NOT_ACTIVATED",
            "reason": "the exact source-normalized Newton chain is clear, but parent Pi_M, observed time, commutator silence, no-extra projection and calibration are open",
            "next_action": "attack parent Pi_M/Hamiltonian mass generator first",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1793_1_Y6_gate",
            "decision": "Y6_EXTRA_STRESS_GATE_SEPARATED",
            "reason": "Bianchi conservation is not stress silence; projector/domain stress must be zero theorem or finite residual",
            "next_action": "hold Y6 as parallel topological/projector-null stress gate",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1793_2_finite_pack",
            "decision": "FINITE_Y5Y6_COUPLING_PACK_REJECTED_NONCLAIM",
            "reason": "Gdot, radial/range, species/frame, mu_extra/PPN, T_extra and q_P/Khat/q_loc coefficients are missing",
            "next_action": "use the pack as future test input schema only",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1793_3_next",
            "decision": "PARENT_PIM_AND_OBSERVED_TIME_GENERATOR_NEXT",
            "reason": "the least-scrutiny Y5 route is to derive Pi_M as a parent Hamiltonian/covariant-phase-space mass charge map with observed-time normalization",
            "next_action": "build 1794 parent Pi_M/observed-time generator gate or finite Y5 pack",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1793_0_primary",
            "next_target": "1794-Y5-R2FR-parent-PiM-observed-time-generator-or-finite-Y5-pack.md",
            "script": "scripts/Y5_R2FR_parent_PiM_observed_time_generator_or_finite_Y5_pack.py",
            "objective": "try to derive Pi_M as a parent Hamiltonian/covariant-phase-space mass charge map with integrability, fixed reference, same observed coframe and zero commutator; otherwise emit finite nonclaim Y5 source-normalization rows",
            "selection_status": "selected",
            "success_condition": "parent-owned Pi_M and observed-time generator with zero commutator/no extra projection, or source-backed finite Y5 rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1793_1_parallel_Y6",
            "next_target": "1794b-Y5-R2FR-Y6-topological-projector-null-stress-gate.md",
            "script": "scripts/Y5_R2FR_Y6_topological_projector_null_stress_gate.py",
            "objective": "test whether Y6 extra/projector stress is topological, projector-null, pure improvement, or finite residual",
            "selection_status": "held_parallel",
            "success_condition": "Y6 stress-zero theorem or finite PPN/source-stress rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1793_2_parallel_Gauss",
            "next_target": "1794c-Y5-R2FR-Gauss-orbital-calibration-and-PPN-source-stability.md",
            "script": "scripts/Y5_R2FR_Gauss_orbital_calibration_and_PPN_source_stability.py",
            "objective": "after Pi_M ownership, calibrate the closed charge to inverse-square orbital GM and second-order PPN source stability",
            "selection_status": "held_until_PiM",
            "success_condition": "Gauss/orbital calibration and source PPN stability, or finite residual rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "y5_source_charge_owner_attempt": y5_source_charge_owner_attempt_rows(),
        "source_mass_flux_chain": source_mass_flux_chain_rows(),
        "y6_extra_stress_gate": y6_extra_stress_gate_rows(),
        "finite_y5y6_coupling_pack": finite_y5y6_coupling_pack_rows(),
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
        shutil.copy2(path, RAB_QUEUE / f"JR1793_{key.upper()}.csv")


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
        if not (RAB_QUEUE / f"JR1793_{key.upper()}.csv").exists():
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
        ("VAL1793_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1793_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1793_2_y5_chain_written",
            any(row["owner_id"] == "Y5SC1793_7_verdict" and row["current_status"] == "SOURCE_CHARGE_OWNER_THEOREM_NOT_ACTIVATED" for row in rows_map["y5_source_charge_owner_attempt"]),
            "Y5 source-charge owner theorem chain is written and not activated",
        ),
        (
            "VAL1793_3_mass_flux_chain_blocks",
            any(row["chain_id"] == "MFC1793_7_verdict" and row["current_status"] == "MASS_FLUX_CHAIN_NOT_CLOSED" for row in rows_map["source_mass_flux_chain"]),
            "source mass flux chain remains not closed",
        ),
        (
            "VAL1793_4_y6_gate_blocks",
            any(row["stress_id"] == "Y6G1793_5_verdict" and row["current_status"] == "Y6_EXTRA_STRESS_NOT_ZEROED" for row in rows_map["y6_extra_stress_gate"]),
            "Y6 extra stress gate remains open",
        ),
        (
            "VAL1793_5_finite_pack_rejected",
            any(row["pack_id"] == "FY1793_7_acceptance" and row["row_status"] == "REJECT_CURRENT_Y5Y6_COUPLING_PACK" for row in rows_map["finite_y5y6_coupling_pack"])
            and all(not boolish(row["score_ready"]) and not boolish(row["valid_prediction_row"]) for row in rows_map["finite_y5y6_coupling_pack"]),
            "finite Y5/Y6 coupling pack is rejected and non-scoreable",
        ),
        (
            "VAL1793_6_countermodels_retained",
            all(boolish(row["survives_current_constraints"]) for row in rows_map["countermodel_ledger"]),
            "countermodels remain live",
        ),
        (
            "VAL1793_7_claim_gates_blocked",
            all(row["status"] == "BLOCKED" and not boolish(row["gate_pass"]) and not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "claim gates are blocked",
        ),
        ("VAL1793_8_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1793_9_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1793_10_decision_next",
            any(
                row["decision_id"] == "DEC1793_3_next"
                and row["decision"] == "PARENT_PIM_AND_OBSERVED_TIME_GENERATOR_NEXT"
                for row in rows_map["decision_ledger"]
            ),
            "decision selects parent Pi_M and observed-time generator next",
        ),
        (
            "VAL1793_11_next_selected",
            any(row["route_id"] == "NEXT1793_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1793_12_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1793 CSVs parse"),
        ("VAL1793_13_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1793_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1793_15_formalization_untouched", formalization_untouched(), "no 1793 outputs found under formalization-workbench"),
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
            "check_id": "VAL1793_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1793 Y5 source-charge owner and Y6 extra-stress gate checkpoint",
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
            "# 1793 - Y5/R2FR Y5 Source-Charge Owner and Y6 Extra-Stress Gate",
            "",
            "## Verdict",
            "",
            "1793 writes the least-smuggly route for source-normalized Newton: the observed mass parameter must be a parent EH/Hilbert/Noether charge before orbital fitting. The exact chain is now explicit: one observed coframe, parent mass projector `Pi_M`, observed-time/Hamiltonian generator, flux closure `d(Pi_M J_H)=0`, zero extra mass projection, Gauss/orbital calibration, and second-order PPN source stability.",
            "",
            "The chain is not activated for current MTS. `Pi_M` is not yet parent-owned, its commutator can leak radial/source-mass hair, extra mass projection channels remain active, and Gauss/orbital/PPN calibration is downstream. `Y6` is also separated cleanly: Bianchi/Ward conservation owns total stress, but does not prove extra/projector stress is absent. So `Y6` needs a topological/projector-null theorem or finite stress-response rows.",
            "",
            "**Claim ceiling:** no Y5 theorem-zero, no Y6 theorem-zero, no no-linear-source promotion, no finite Y5/Y6 score, no `q_loc/c_R2/R10/PPN` score, no local-GR/Newton claim, no GitHub action, and no `formalization-workbench` edit is allowed from 1793.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## Y5 Source-Charge Owner Attempt",
            markdown_table(rows_map["y5_source_charge_owner_attempt"], ["owner_id", "required_clause", "mathematical_form", "if_closed", "current_status", "valid_for_claim"]),
            "",
            "## Source Mass Flux Chain",
            markdown_table(rows_map["source_mass_flux_chain"], ["chain_id", "identity", "mathematical_form", "current_status", "missing_piece", "valid_for_claim"]),
            "",
            "## Y6 Extra-Stress Gate",
            markdown_table(rows_map["y6_extra_stress_gate"], ["stress_id", "statement", "mathematical_form", "current_status", "needed_for_zero", "valid_for_claim"]),
            "",
            "## Finite Y5/Y6 Coupling Pack",
            markdown_table(rows_map["finite_y5y6_coupling_pack"], ["pack_id", "row_type", "required_field", "current_value", "units_required", "row_status", "score_ready", "valid_prediction_row", "valid_for_claim"]),
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
            "The route is getting cleaner, not softer. If `Y5` closes, Newtonian source mass stops being an input and becomes a parent charge. But the next real hinge is narrow: own `Pi_M` and the observed-time generator, or admit finite source-normalization rows. That is the best route because it attacks the exact place a critic would say 'you fitted GM'.",
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
    print(f"1793 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
