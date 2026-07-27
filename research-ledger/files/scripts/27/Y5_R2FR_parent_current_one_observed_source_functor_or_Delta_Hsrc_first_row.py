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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1779"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1779_0_1778_handoff",
        "source_key": "1778_handoff",
        "source_path": ROOT / "1778-Y5-R2FR-adopted-PiM-source-measure-glue-or-RPiH-first-row.md",
        "needles": ["NEXT1778_0_primary", "PCA1778_0_parent_current", "PCA1778_2_one_observed_source_functor", "DHS1778_0_Delta_Hsrc"],
    },
    {
        "source_id": "SRC1779_1_1778_validation",
        "source_key": "1778_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1778_VALIDATION.csv",
        "needles": ["VAL1778_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1779_2_993_current_gate",
        "source_key": "993_current_extraction_gate",
        "source_path": RESIDUALS / "P8_Y5_R10_993_CURRENT_EXTRACTION_GATE.csv",
        "needles": ["CEG993_1_variation_owner", "CEG993_4_verdict"],
    },
    {
        "source_id": "SRC1779_3_993_sector_ledger",
        "source_key": "993_sector_current_ledger",
        "source_path": RESIDUALS / "P8_Y5_R10_993_SECTOR_CURRENT_EXTRACTION_LEDGER.csv",
        "needles": ["SEC993_2_universal_matter", "SEC993_6_metric_readout_PiM"],
    },
    {
        "source_id": "SRC1779_4_994_residual_pack",
        "source_key": "994_mts_residual_current_pack",
        "source_path": RESIDUALS / "P8_Y5_R10_994_MTS_RESIDUAL_CURRENT_PACK.csv",
        "needles": ["RC994_0_reference_boundary", "RC994_3_matter_source_glue"],
    },
    {
        "source_id": "SRC1779_5_1519_coframe_tau",
        "source_key": "1519_coframe_tau_lock",
        "source_path": RESIDUALS / "P8_Y5_PARENT_FRAME_1519_COFRAME_TAU_LOCK_AUDIT.csv",
        "needles": ["OCF1519_2_observed_coframe", "OCF1519_4_tau_lock", "OCF1519_7_verdict"],
    },
    {
        "source_id": "SRC1779_6_1720_JH_definition",
        "source_key": "1720_JH_definition",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1720_JH_CURRENT_DEFINITION_THEOREM.csv",
        "needles": ["JHT1720_0_definition", "JHT1720_3_source_prefactor_countermodel"],
    },
    {
        "source_id": "SRC1779_7_1720_matter_functor",
        "source_key": "1720_matter_functor_signature",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1720_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
        "needles": ["MFS1720_2_ordinary_matter_functor", "MFS1720_8_verdict"],
    },
    {
        "source_id": "SRC1779_8_1733_current_owner",
        "source_key": "1733_theta_qtau_current_owner",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1733_THETA_QTAU_CURRENT_OWNER_AUDIT.csv",
        "needles": ["COA1733_0_L_parent", "COA1733_7_owner_verdict"],
    },
    {
        "source_id": "SRC1779_9_1733_descent_lemma",
        "source_key": "1733_descent_current_lemma",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1733_DESCENT_CURRENT_LEMMA.csv",
        "needles": ["DCL1733_0_contract", "DCL1733_6_matter_source_descent", "DCL1733_7_verdict"],
    },
    {
        "source_id": "SRC1779_10_1733_component_rows",
        "source_key": "1733_theta_qtau_component_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1733_THETA_QTAU_COMPONENT_ROWS.csv",
        "needles": ["TQC1733_0_EH", "TQC1733_6_total_Qtau"],
    },
    {
        "source_id": "SRC1779_11_1765_total_hilbert",
        "source_key": "1765_total_hilbert_owner",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1765_TOTAL_HILBERT_SOURCE_OWNER_AUDIT.csv",
        "needles": ["THO1765_1_total_hilbert_derivative", "THO1765_4_owner_verdict"],
    },
    {
        "source_id": "SRC1779_12_1768_normal_form",
        "source_key": "1768_parent_action_normal_form",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1768_PARENT_ACTION_NORMAL_FORM_SIGNATURE.csv",
        "needles": ["ANF1768_2_hilbert_matter_owner", "ANF1768_5_forbidden_source_map"],
    },
    {
        "source_id": "SRC1779_13_1768_source_map",
        "source_key": "1768_source_map_identity_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1768_SOURCE_MAP_IDENTITY_GATE.csv",
        "needles": ["SMG1768_1_no_shadow_map_gate", "SMG1768_4_current_verdict"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1779_SOURCE_REGISTER.csv",
    "common_antecedent_join": RESIDUALS / "P8_Y5_PARENT_QLOC_1779_COMMON_ANTECEDENT_JOIN.csv",
    "convergence_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1779_PARENT_CURRENT_SOURCE_FUNCTOR_CONVERGENCE.csv",
    "delta_hsrc_components": RESIDUALS / "P8_Y5_PARENT_QLOC_1779_DELTA_HSRC_COMPONENT_LEDGER.csv",
    "first_row_pack": RESIDUALS / "P8_Y5_PARENT_QLOC_1779_FIRST_ROW_ACQUISITION_PACK.csv",
    "countermodel": RESIDUALS / "P8_Y5_PARENT_QLOC_1779_COUNTERMODEL_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1779_CLAIM_GATE.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1779_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1779_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1779_VALIDATION.csv",
}


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
                "role": "1779 parent-current plus one-observed-source-functor convergence evidence",
            }
        )
    return rows


def common_antecedent_join_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "join_id": "CAJ1779_0_parent_normal_form",
            "antecedent": "one typed parent action normal form",
            "current_side_need": "delta L_parent=E_A delta Phi^A+dTheta_total and Q_tau^MTS=sum_s Q_tau_s",
            "source_functor_need": "ordinary active source is delta S_matter_min/delta e_obs with no post-variation source map",
            "best_existing_support": "ANF1768_0;ANF1768_2;ANF1768_5;CEG993_0",
            "current_status": "CONTRACT_READY_PARENT_UNSIGNED",
            "why_not_closed": "complete parent action inventory and object-language signature are not supplied",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "join_id": "CAJ1779_1_q_Dq_observed_coframe",
            "antecedent": "quotient map q and observed coframe functor Obs_e(q)",
            "current_side_need": "Theta/Q_tau descends through q without vertical-current leakage",
            "source_functor_need": "J_H is computed in the same observed coframe used by clocks, sources, and orbits",
            "best_existing_support": "DCL1733_1;DCL1733_6;OCF1519_0;OCF1519_2;MFS1720_1",
            "current_status": "MISSING_Q_DQ_AND_OBSERVED_COFRAME_FUNCTOR",
            "why_not_closed": "q is not computable and Obs_e(q) is not constructed before readout",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "join_id": "CAJ1779_2_tau_projectability",
            "antecedent": "one observed time generator tau is projectable and fixed",
            "current_side_need": "H_tau and delta H_tau use the same tau in charge variation and boundary terms",
            "source_functor_need": "J_H[tau], source support, clocks, and orbital readout use the same tau",
            "best_existing_support": "DCL1733_3;COA1733_3;OCF1519_4;MFS1720_5",
            "current_status": "MISSING_TAU_PROJECTABILITY_AND_LOCK",
            "why_not_closed": "source, charge, boundary, clock, and orbit time choices remain split",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "join_id": "CAJ1779_3_matter_source_owner",
            "antecedent": "ordinary matter is one total Hilbert source functor",
            "current_side_need": "matter/source part of Q_tau is tied to parent constraints rather than fitted GM",
            "source_functor_need": "J_H^dress includes interaction/binding stress and excludes source-only weights",
            "best_existing_support": "JHT1720_0;MFS1720_2;THO1765_1;THO1765_2;THO1765_3",
            "current_status": "CONDITIONAL_OWNER_CLEAN_BUT_UNSIGNED",
            "why_not_closed": "ordinary exchange connectivity, no source-shadow functional, and non-Hilbert source silence remain unsigned",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "join_id": "CAJ1779_4_boundary_reference",
            "antecedent": "boundary/reference improvement is fixed before readout",
            "current_side_need": "B_ref and B_H cannot shift Q_tau or H_ref with source/radius/frame choices",
            "source_functor_need": "worldtube/source equality is not changed by bookkeeping flux",
            "best_existing_support": "COA1733_4;QDEC993_1;RC994_0;PCA1778_4",
            "current_status": "MISSING_BOUNDARY_REFERENCE_ZERO_OR_BOUND",
            "why_not_closed": "boundary no-hair, reference derivative silence, and B_H flux rows are not sourced",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "join_id": "CAJ1779_5_projector_chain_map",
            "antecedent": "Pi_M^H is the parent mass-channel chain map",
            "current_side_need": "Pi_M^H is part of the Hamiltonian current/source decomposition",
            "source_functor_need": "Pi_M^H J_H^dress is closed or carries a source-backed commutator residual",
            "best_existing_support": "TQC1733_2;QDEC993_3;PCA1778_3;RBH1778_0",
            "current_status": "MISSING_PIMH_CHAIN_MAP_OR_RPIH_BOUND",
            "why_not_closed": "delta Pi_M, [d,Pi_M]J_H, R_PiH, and B_H flux remain unowned",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "join_id": "CAJ1779_6_exterior_extra_silence",
            "antecedent": "extra/projector/boundary sectors are zero, exact, LHS-only, or bounded in the exterior",
            "current_side_need": "Q_tau^MTS differs from Q_tau^EH only by signed zero/proper pieces or explicit residuals",
            "source_functor_need": "non-Hilbert source currents do not sneak into J_H^dress",
            "best_existing_support": "SEC993_3;SEC993_4;RC994_1;RC994_2;MFS1720_7",
            "current_status": "MISSING_SECTOR_CURRENT_EXTRACTION_AND_NONHILBERT_SILENCE",
            "why_not_closed": "extra fields, kinetic signs, projector/domain algebra, and non-Hilbert current classification are not complete",
            "valid_for_claim": False,
        },
    ]


def convergence_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PCS1779_0_convergence_statement",
            "claim": "parent current and observed source functor converge to the same source-measure object",
            "mathematical_form": "if CAJ1779_0..6 pass, then G_ref^-1 int_S Q_tau^MTS-H_ref = M_eff[Pi_M^H J_H^dress]",
            "current_status": "CONDITIONAL_THEOREM_WRITTEN",
            "derivation_content": "Stokes/covariant phase-space gives the exterior charge; the same parent action and observed coframe define the Hilbert source; the remaining equality is exact up to named residuals",
            "missing_for_claim": "all common antecedents must be parent-signed with no placeholder sectors",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PCS1779_1_EH_comparator_policy",
            "claim": "EH current is a comparator, not a proof of the MTS current",
            "mathematical_form": "Q_tau^MTS = Q_tau^EH + Q_X + Q_projector + Q_boundary + Q_source_glue",
            "current_status": "COMPARATOR_ALLOWED_IMPORT_FORBIDDEN",
            "derivation_content": "EH supplies the GR/Newton target shape, while every non-EH/projector/boundary/source term remains a residual until extracted",
            "missing_for_claim": "Q_X, Q_projector, Q_boundary, Q_source_glue zero/bound rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PCS1779_2_source_functor_gain",
            "claim": "source-only species weights collapse to a sharper source-shadow/block problem",
            "mathematical_form": "T_active=T_H only if no F_shadow(T_H,labels) and ordinary matter is one exchange-connected source block",
            "current_status": "PARTIAL_DERIVATION_IMPORTED_NONCLAIM",
            "derivation_content": "1765 and 1768 reduce arbitrary coupling ambiguity but leave no-shadow and exchange-connectivity gates open",
            "missing_for_claim": "source-shadow ban, connected exchange graph, non-Hilbert silence",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PCS1779_3_Delta_Hsrc_identity",
            "claim": "failed convergence becomes the Delta_Hsrc component vector",
            "mathematical_form": "Delta_Hsrc = Delta_current + Delta_frame_tau + Delta_shadow + Delta_boundary + Delta_projector + Delta_extra",
            "current_status": "RESIDUAL_DECOMPOSITION_STAGED",
            "derivation_content": "each missing common antecedent has an explicit component row and no-cancellation rule",
            "missing_for_claim": "theorem-zero or source-backed finite rows for every component",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PCS1779_4_current_verdict",
            "claim": "current MTS owns the parent current and one observed source functor needed for Delta_Hsrc=0",
            "mathematical_form": "CAJ1779_0..6 pass and Delta_Hsrc=0",
            "current_status": "FAIL_CURRENT_PARENT_PROOF",
            "derivation_content": "the convergence theorem is useful, but current source paths show the same core antecedents are unsigned",
            "missing_for_claim": "q/Dq, tau, parent action inventory, matter functor, boundary, PiM chain map, and extra-sector current rows",
            "valid_for_claim": False,
        },
    ]


def delta_hsrc_component_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "component_id": "DHC1779_0_parent_current",
            "quantity": "Delta_current",
            "definition": "difference between full Q_tau^MTS and the parent-extracted current pieces",
            "formula": "Q_tau^MTS-(Q_EH+Q_X+Q_projector+Q_boundary+Q_source)",
            "status": "MISSING_SECTOR_CURRENT_EXTRACTION",
            "required_source": "sector L_s, Theta_s, Q_tau_s, C_tau_s, boundary term, source path",
            "no_cancellation_rule": "component absolute value retained; EH baseline cannot cancel unextracted MTS pieces",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "DHC1779_1_frame_tau",
            "quantity": "Delta_frame_tau",
            "definition": "source coframe/tau differs from charge, clock, boundary, or orbital readout coframe/tau",
            "formula": "J_H[tau_source,e_source]-J_H[tau_charge,e_obs]",
            "status": "MISSING_ONE_OBSERVED_COFRAME_TAU_LOCK",
            "required_source": "q;Obs_e(q);tau_projectability;source normal;surface pair;frame map",
            "no_cancellation_rule": "frame/tau residual cannot be absorbed into H_ref or fitted GM",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "DHC1779_2_source_shadow",
            "quantity": "Delta_shadow",
            "definition": "post-Hilbert source map, source-only prefactor, or disconnected source block contribution",
            "formula": "F_shadow(T_H,labels)-T_H + sum_C delta_w_C T_C",
            "status": "MISSING_NO_SHADOW_AND_EXCHANGE_CONNECTIVITY",
            "required_source": "source-shadow ban; ordinary exchange graph; non-Hilbert current classification",
            "no_cancellation_rule": "relative source blocks scored independently, not hidden inside a universal G calibration",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "DHC1779_3_boundary_reference",
            "quantity": "Delta_boundary_reference",
            "definition": "B_ref, B_H, or boundary improvement flux shifts H_tau-H_ref or PiM equality",
            "formula": "int_S dB_ref + int_boundary dB_H + Delta_ref",
            "status": "MISSING_BOUNDARY_REFERENCE_BH_FLUX",
            "required_source": "B_ref owner; B_H definition; boundary class; zero-flux theorem or finite bound",
            "no_cancellation_rule": "boundary/reference shifts cannot be chosen after readout",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "DHC1779_4_projector_chain",
            "quantity": "Delta_projector_chain",
            "definition": "Pi_M^H chain-map failure, projector variation stress, old/new PiM mismatch",
            "formula": "[d,Pi_M^H]J_H + (delta Pi_M^H)J_H + R_PiH",
            "status": "MISSING_PIM_CHAIN_MAP_AND_RPIH",
            "required_source": "Pi_M^H definition; commutator theorem/bound; delta PiM stress; R_PiH row",
            "no_cancellation_rule": "projector residual must pass as an operator/channel component",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "DHC1779_5_extra_nonHilbert",
            "quantity": "Delta_extra_nonHilbert",
            "definition": "extra motion/time/domain/memory/range/connection currents carrying source charge",
            "formula": "Q_X+C_extra+C_domain+C_memory+C_connection+J_nonH",
            "status": "MISSING_EXTRA_SECTOR_AND_NONHILBERT_SILENCE",
            "required_source": "field list; kinetic/potential signs; proper/exact/topological proof or coefficient bounds",
            "no_cancellation_rule": "each channel must zero/bound separately before local-GR/Newton use",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "DHC1779_6_total_abs",
            "quantity": "epsilon_Delta_Hsrc_total_abs",
            "definition": "absolute no-cancellation envelope for the parent-current/source-functor mismatch",
            "formula": "sum_i abs(DHC1779_i)",
            "status": "MISSING_COMPONENT_VALUES",
            "required_source": "all component rows theorem-zero or finite sourced, common M_H_ref denominator, units",
            "no_cancellation_rule": "cannot score until all nonclaim components have source paths and units",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def first_row_pack_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "FRP1779_0_sector_current_table",
            "target_quantity": "Delta_current first row",
            "required_columns": "sector;L_term;Theta_term;Q_tau_term;constraint_term;boundary_term;source_path;units;valid_for_claim",
            "current_status": "MISSING_SECTOR_CURRENT_TABLE",
            "acceptance_rule": "every retained sector has source path or is explicitly absent/proper/exact with proof",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FRP1779_1_coframe_tau_table",
            "target_quantity": "Delta_frame_tau first row",
            "required_columns": "system_id;q_id;Obs_e_id;tau_id;source_normal;surface_pair;frame_map;Delta_frame_tau;source_path;valid_for_claim",
            "current_status": "MISSING_OBSERVED_COFRAME_TAU_TABLE",
            "acceptance_rule": "same observed coframe/tau theorem-zero or finite residual with source path",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FRP1779_2_source_functor_table",
            "target_quantity": "Delta_shadow/source-functor first row",
            "required_columns": "matter_action_id;Hilbert_current;exchange_graph;source_shadow_rule;delta_w_block;nonHilbert_current;source_path;valid_for_claim",
            "current_status": "MISSING_SOURCE_FUNCTOR_TABLE",
            "acceptance_rule": "no-shadow plus connected exchange graph, or finite block/source-shadow residual",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FRP1779_3_Delta_Hsrc_total",
            "target_quantity": "epsilon_Delta_Hsrc_total_abs first score row",
            "required_columns": "system_id;component_values;M_H_ref;units;component_source_paths;no_cancellation_flag;valid_for_claim",
            "current_status": "BLOCKED_UNTIL_COMPONENTS_FILLED",
            "acceptance_rule": "all components must be theorem-zero or source-backed before any score/readout",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1779_0_EH_only_smuggling",
            "countermodel": "use EH Q_tau as Q_tau^MTS while extra/projector/boundary sectors remain unvaried",
            "survives_current_constraints": True,
            "why_survives": "EH baseline is allowed only as comparator and total Q_tau^MTS is not extracted",
            "what_kills_it": "sector-by-sector current extraction or zero/bound rows for every residual current",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1779_1_two_frames",
            "countermodel": "source Hilbert current and orbital/clock readout use different coframes or tau choices",
            "survives_current_constraints": True,
            "why_survives": "observed coframe functor and tau projectability are not parent-signed",
            "what_kills_it": "q/Obs_e(q) construction plus tau_source=tau_charge=tau_clock=tau_orbit theorem",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1779_2_source_shadow",
            "countermodel": "post-Hilbert source map or source-only prefactor alters active gravitational source",
            "survives_current_constraints": True,
            "why_survives": "normal-form and no-shadow clauses are contracts, not a completed parent grammar theorem",
            "what_kills_it": "parent object language forbids F_shadow and ordinary exchange graph is connected or bounded",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1779_3_boundary_shift",
            "countermodel": "reference or improvement flux shifts H_tau-H_ref without changing the formal charge equation",
            "survives_current_constraints": True,
            "why_survives": "B_ref, B_H flux, and boundary no-hair rows remain unsourced",
            "what_kills_it": "fixed boundary/reference branch and zero-flux theorem or finite bound rows",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1779_4_nonHilbert_extra_current",
            "countermodel": "extra/domain/memory/range/connection current carries mass-channel source charge",
            "survives_current_constraints": True,
            "why_survives": "non-Hilbert current silence and extra-sector current extraction are not complete",
            "what_kills_it": "proper/exact/topological/no-source theorem per channel or finite residual vector",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1779_0_parent_current_owner",
            "claim": "Theta_total and Q_tau^MTS are extracted from one parent action",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "sector current table is missing and total Q_tau remains not promoted",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1779_1_one_observed_source_functor",
            "claim": "ordinary J_H^dress is parent-owned in one observed coframe/tau",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "matter functor, coframe/tau lock, no-shadow, and non-Hilbert silence are unsigned",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1779_2_Delta_Hsrc_zero",
            "claim": "Delta_Hsrc=0 or source-bounded for scoring",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "component rows are schema-only and not score-ready",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1779_3_Newton_GR_local",
            "claim": "source-normalized Newton, GR reduction, PPN, R10, clock, WEP, or orbital pass follows",
            "gate_pass": False,
            "status": "REFUSED",
            "blocker": "source-measure and weak-field/PPN readout gates remain downstream",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1779_0_convergence_gain",
            "decision": "PARENT_CURRENT_AND_SOURCE_FUNCTOR_SHARE_COMMON_ANTECEDENTS",
            "reason": "theta/Q_tau ownership and observed Hilbert source ownership both reduce to parent normal form, q/Obs_e, tau lock, no-shadow, boundary, and sector silence",
            "next_action": "attack the shared antecedents rather than treating current and source as separate problems",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1779_1_current_status",
            "decision": "FAIL_CURRENT_PARENT_PROOF",
            "reason": "existing source paths show only conditional EH/current/source-functor support; no total Q_tau or one observed source functor is signed",
            "next_action": "keep Delta_Hsrc as componentized nonclaim residual",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1779_2_first_rows",
            "decision": "DELTA_HSRC_COMPONENT_ROWS_STAGED_NONCLAIM",
            "reason": "the fallback is now executable: sector current, frame/tau, source-shadow, boundary, projector, and extra-current rows",
            "next_action": "fill no component without source path, units, and no-cancellation flag",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1779_3_best_next",
            "decision": "Q_DQ_TAU_PROJECTABILITY_AND_SOURCE_FUNCTOR_SIGNATURE_IS_NEXT",
            "reason": "q/Obs_e and tau projectability are the shared bottleneck for both current descent and observed source definition",
            "next_action": "build 1780 q/Dq/tau/source-functor signature gate or first Delta_frame_tau row",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1779_0_primary",
            "next_target": "1780-Y5-R2FR-q-Dq-tau-source-functor-signature-or-Delta-frame-tau-first-row.md",
            "script": "scripts/Y5_R2FR_q_Dq_tau_source_functor_signature_or_Delta_frame_tau_first_row.py",
            "objective": "prove q/Obs_e, Dq kernel, tau projectability, and source-functor signature together; if not, stage the first Delta_frame_tau source row",
            "selection_status": "selected",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1779_1_parallel",
            "next_target": "1780b-Y5-R2FR-sector-current-table-first-row-pack.md",
            "script": "scripts/Y5_R2FR_sector_current_table_first_row_pack.py",
            "objective": "prepare sector L/Theta/Q_tau/C_tau rows for Delta_current without claiming parent-current ownership",
            "selection_status": "held_parallel",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1779_2_later",
            "next_target": "1781-Y5-R2FR-source-shadow-and-nonHilbert-current-silence-or-Delta-shadow-row.md",
            "script": "scripts/Y5_R2FR_source_shadow_and_nonHilbert_current_silence_or_Delta_shadow_row.py",
            "objective": "after q/tau frame is sharpened, close or bound source-shadow and non-Hilbert source-current leakage",
            "selection_status": "later",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "common_antecedent_join": common_antecedent_join_rows(),
        "convergence_theorem": convergence_theorem_rows(),
        "delta_hsrc_components": delta_hsrc_component_rows(),
        "first_row_pack": first_row_pack_rows(),
        "countermodel": countermodel_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        shutil.copy2(path, MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(path, QUARANTINE / filename)
        shutil.copy2(path, RAB_QUEUE / f"JR1779_{key.upper()}.csv")


def parse_csv(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def boolish(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def generated_csvs() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def sources_ok(rows_map: dict[str, list[dict[str, Any]]]) -> tuple[bool, bool]:
    rows = rows_map["source_register"]
    return all(boolish(row["exists"]) for row in rows), all(boolish(row["needles_present"]) for row in rows)


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in rows_map.items():
        if key == "source_register":
            continue
        for row in rows:
            for flag in ("valid_for_claim", "claim_allowed", "score_ready", "accepted_for_scoring"):
                if flag in row and boolish(row[flag]):
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            text = " ".join(str(value) for value in row.values()).upper()
            if "MISSING" in text:
                if any(boolish(row.get(flag, False)) for flag in ("valid_for_claim", "claim_allowed", "score_ready", "accepted_for_scoring")):
                    return False
    return True


def branch_copies_exist() -> bool:
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1779_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    generated_names = {path.name for path in OUTPUTS.values()}
    generated_names.add("1779-Y5-R2FR-parent-current-one-observed-source-functor-or-Delta-Hsrc-first-row.md")
    return not any(path.name in generated_names for path in FORMALIZATION.rglob("*"))


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    exists_ok, needles_ok = sources_ok(rows_map)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1779_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1779_1_needles_present", needles_ok, "required source needles are present"),
        (
            "VAL1779_2_common_antecedents_joined",
            len(rows_map["common_antecedent_join"]) >= 7 and all(not boolish(row["valid_for_claim"]) for row in rows_map["common_antecedent_join"]),
            "common parent-current/source-functor antecedents are joined and nonclaim",
        ),
        (
            "VAL1779_3_convergence_theorem_written",
            any(row["theorem_id"] == "PCS1779_0_convergence_statement" and row["current_status"] == "CONDITIONAL_THEOREM_WRITTEN" for row in rows_map["convergence_theorem"]),
            "parent-current/source-functor convergence theorem is written",
        ),
        (
            "VAL1779_4_current_proof_not_promoted",
            any(row["theorem_id"] == "PCS1779_4_current_verdict" and row["current_status"] == "FAIL_CURRENT_PARENT_PROOF" for row in rows_map["convergence_theorem"]),
            "current parent proof remains unpromoted",
        ),
        (
            "VAL1779_5_Delta_Hsrc_components_nonclaim",
            all(not boolish(row["valid_for_claim"]) and not boolish(row["score_ready"]) for row in rows_map["delta_hsrc_components"]),
            "Delta_Hsrc component rows remain nonclaim and not score-ready",
        ),
        (
            "VAL1779_6_first_row_pack_nonclaim",
            all(not boolish(row["valid_for_claim"]) and not boolish(row["score_ready"]) for row in rows_map["first_row_pack"]),
            "first-row acquisition pack remains nonclaim",
        ),
        (
            "VAL1779_7_countermodels_retained",
            all(boolish(row["survives_current_constraints"]) for row in rows_map["countermodel"]),
            "countermodels remain live until theorem or bound rows close them",
        ),
        (
            "VAL1779_8_claim_gates_blocked",
            all(not boolish(row["valid_for_claim"]) and row["status"] in {"BLOCKED", "REFUSED"} for row in rows_map["claim_gate"]),
            "claim gates are blocked or refused",
        ),
        ("VAL1779_9_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1779_10_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1779_11_decision_next",
            any(row["decision_id"] == "DEC1779_3_best_next" and "Q_DQ_TAU_PROJECTABILITY" in row["decision"] for row in rows_map["decision"]),
            "decision selects q/Dq/tau/source-functor signature next",
        ),
        (
            "VAL1779_12_next_selected",
            any(row["route_id"] == "NEXT1779_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1779_13_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1779 CSVs parse"),
        ("VAL1779_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1779_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1779_16_formalization_untouched", formalization_untouched(), "no 1779 outputs found under formalization-workbench"),
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
            "check_id": "VAL1779_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1779 parent-current one-observed-source-functor or Delta_Hsrc first-row checkpoint",
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(str(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, str]]) -> str:
    return "\n".join(
        [
            "# 1779 - Y5/R2FR Parent Current, One Observed Source Functor, or Delta-Hsrc First Row",
            "",
            "## Verdict",
            "",
            "1779 squeezes the problem again. The Hamiltonian-current side and the Hilbert-source side are not two unrelated gaps: they share the same parent antecedents. A single typed parent action, a computable quotient `q`, an observed coframe functor `Obs_e(q)`, a projectable `tau`, a no-shadow matter functor, fixed boundary/reference data, a `Pi_M^H` chain map, and extra-sector silence would make the adopted-`Pi_M` source-measure theorem go through.",
            "",
            "Current MTS does not yet have that parent signature. So the result is a useful convergence theorem plus a strict `Delta_Hsrc` component ledger, not a Newton/GR pass. This is the right kind of failure: less fog, fewer places for a hidden coupling to hide.",
            "",
            "**Claim ceiling:** no parent-current owner, one-observed-source-functor proof, `Delta_Hsrc=0`, measured-GM/Newton/Gauss/orbit reduction, PPN/R10/R11/WEP/clock pass, local-GR pass, GitHub action, or `formalization-workbench` edit is allowed from 1779.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## Common Antecedent Join",
            markdown_table(rows_map["common_antecedent_join"], ["join_id", "antecedent", "current_side_need", "source_functor_need", "best_existing_support", "current_status", "why_not_closed", "valid_for_claim"]),
            "",
            "## Convergence Theorem",
            markdown_table(rows_map["convergence_theorem"], ["theorem_id", "claim", "mathematical_form", "current_status", "derivation_content", "missing_for_claim", "valid_for_claim"]),
            "",
            "## Delta-Hsrc Components",
            markdown_table(rows_map["delta_hsrc_components"], ["component_id", "quantity", "definition", "formula", "status", "required_source", "no_cancellation_rule", "score_ready", "valid_for_claim"]),
            "",
            "## First-Row Acquisition Pack",
            markdown_table(rows_map["first_row_pack"], ["row_id", "target_quantity", "required_columns", "current_status", "acceptance_rule", "score_ready", "valid_for_claim"]),
            "",
            "## Countermodel Ledger",
            markdown_table(rows_map["countermodel"], ["countermodel_id", "countermodel", "survives_current_constraints", "why_survives", "what_kills_it"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "status", "blocker", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            markdown_table(rows_map["decision"], ["decision_id", "decision", "reason", "next_action"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "The best next shot is not to invent a mass equality. It is to make `q/Obs_e/tau` do real work. If `q`, `Dq`, `Obs_e(q)`, and one `tau` are parent-owned, then both the current descent and the observed Hilbert source become parts of the same mechanism. If that cannot be proved, `Delta_frame_tau` becomes the first honest row.",
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
    doc_path = ROOT / "1779-Y5-R2FR-parent-current-one-observed-source-functor-or-Delta-Hsrc-first-row.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1779 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
