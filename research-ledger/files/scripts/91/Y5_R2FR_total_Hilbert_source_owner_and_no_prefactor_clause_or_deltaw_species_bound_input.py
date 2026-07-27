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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1765"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1765_0_1764_handoff",
        "source_key": "1764_no_prefactor_next",
        "source_path": ROOT / "1764-Y5-R2FR-species-label-forgetting-source-functor-parent-proof-or-deltaw-species-bound.md",
        "needles": ["NO_SOURCE_PREFACTOR_CLAUSE_IS_NEXT", "NEXT1764_0_primary"],
    },
    {
        "source_id": "SRC1765_1_1764_validation",
        "source_key": "1764_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1764_VALIDATION.csv",
        "needles": ["VAL1764_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1765_2_954_action_clause",
        "source_key": "954_parent_action_clause",
        "source_path": RESIDUALS / "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv",
        "needles": ["PAC954_1_no_source_prefactors", "PAC954_2_total_Hilbert_derivative"],
    },
    {
        "source_id": "SRC1765_3_954_label_attempt",
        "source_key": "954_label_forgetting_attempt",
        "source_path": RESIDUALS / "P8_Y5_R10_954_PARENT_LABEL_FORGETTING_ATTEMPT.csv",
        "needles": ["PLF954_2_prefactor_obstruction", "PLF954_5_verdict"],
    },
    {
        "source_id": "SRC1765_4_955_minimal_matter",
        "source_key": "955_minimal_matter_lemma",
        "source_path": RESIDUALS / "P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv",
        "needles": ["MMA955_1_same_action_principle", "MMA955_3_relative_prefactor"],
    },
    {
        "source_id": "SRC1765_5_977_constant_certificate",
        "source_key": "977_constant_source_certificate",
        "source_path": RESIDUALS / "P8_Y5_R10_977_CONSTANT_SOURCE_CERTIFICATE_ATTEMPT.csv",
        "needles": ["CSC977_4_single_universal_kappa", "RELATIVE_CERTIFICATE_READY_PARENT_UNSIGNED"],
    },
    {
        "source_id": "SRC1765_6_1488_residual_lock",
        "source_key": "1488_delta_w_species_lock",
        "source_path": RESIDUALS / "P8_Y5_R10_1488_WA_DELTAW_RESIDUAL_LOCK.csv",
        "needles": ["WA1488_2_species_label_slot", "MISSING_PARENT_INPUT"],
    },
    {
        "source_id": "SRC1765_7_1764_bound_interface",
        "source_key": "1764_delta_w_species_interface",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1764_DELTAW_SPECIES_BOUND_INTERFACE.csv",
        "needles": ["DWS1764_0_delta_w_species", "MISSING_PARENT_NO_PREFACTOR_OR_NUMERIC_BOUND"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1765_SOURCE_REGISTER.csv",
    "noether_collapse": RESIDUALS / "P8_Y5_PARENT_QLOC_1765_NOETHER_EXCHANGE_COLLAPSE_THEOREM.csv",
    "source_owner": RESIDUALS / "P8_Y5_PARENT_QLOC_1765_TOTAL_HILBERT_SOURCE_OWNER_AUDIT.csv",
    "no_prefactor": RESIDUALS / "P8_Y5_PARENT_QLOC_1765_NO_SOURCE_PREFACTOR_PROOF_ATTEMPT.csv",
    "countermodel": RESIDUALS / "P8_Y5_PARENT_QLOC_1765_COUNTERMODEL_LEDGER.csv",
    "deltaw_block": RESIDUALS / "P8_Y5_PARENT_QLOC_1765_DELTAW_BLOCK_BOUND_INPUT.csv",
    "source_zero_status": RESIDUALS / "P8_Y5_PARENT_QLOC_1765_SOURCE_ZERO_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1765_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1765_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1765_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1765_VALIDATION.csv",
}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": path.exists(),
                "needles_present": all(needle in text for needle in needles),
                "needles": ";".join(needles),
                "role": "total Hilbert source owner and no-prefactor clause or delta_w block bound input",
                "valid_for_claim": False,
            }
        )
    return rows


def noether_collapse_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NEC1765_0_setup",
            "claim_piece": "weighted source conservation problem",
            "mathematical_form": "E_munu=kappa sum_i w_i T_i_munu with nabla_mu E^{mu nu}=0",
            "status": "SETUP_EXACT",
            "derivation_result": "Bianchi requires nabla_mu(sum_i w_i T_i^{mu nu})=0 on matter shell",
            "parent_signed": False,
            "remaining_gap": "which T_i are legitimate parent source components is not yet signed",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NEC1765_1_exchange_identity",
            "claim_piece": "Noether exchange graph",
            "mathematical_form": "nabla_mu T_i^{mu nu}=C_i^nu, sum_i C_i^nu=0",
            "status": "NOETHER_IDENTITY_FORM",
            "derivation_result": "interacting subcurrents need not be separately conserved; only the full Hilbert current is conserved",
            "parent_signed": False,
            "remaining_gap": "need parent decomposition and exchange-current owner",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NEC1765_2_weight_collapse",
            "claim_piece": "relative weights collapse on every live exchange edge",
            "mathematical_form": "0=sum_i w_i C_i^nu; edge i<->j gives (w_i-w_j) C_ij^nu=0, hence w_i=w_j if C_ij not identically zero",
            "status": "DERIVED_CONDITIONAL_THEOREM",
            "derivation_result": "Bianchi plus interaction exchange forbids relative source weights inside each connected exchange component",
            "parent_signed": False,
            "remaining_gap": "must prove ordinary matter source graph is connected and no source-shadow term bypasses the exchange graph",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NEC1765_3_connected_component_law",
            "claim_piece": "block law for remaining prefactors",
            "mathematical_form": "w_i=w_C for all i in connected component C; T_active=sum_C w_C T_C",
            "status": "EXACT_BLOCK_LAW",
            "derivation_result": "relative species weights reduce to block weights over conserved disconnected components",
            "parent_signed": False,
            "remaining_gap": "source blocks and ordinary-matter connectivity are not yet parent-certified",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NEC1765_4_common_mode",
            "claim_piece": "connected ordinary matter gives only common calibration",
            "mathematical_form": "connected graph => T_active=w_star T_total and kappa_eff=kappa w_star",
            "status": "CLEAN_IF_CONNECTED",
            "derivation_result": "if ordinary matter is one connected exchange component, delta_w_species=0 up to Newton/G calibration",
            "parent_signed": False,
            "remaining_gap": "connected-graph premise remains unsigned",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NEC1765_5_current_verdict",
            "claim_piece": "current MTS no-source-prefactor proof",
            "mathematical_form": "delta_w_species -> delta_w_block, with zero only if one ordinary exchange component",
            "status": "PARTIAL_DERIVATION_PARENT_UNSIGNED",
            "derivation_result": "relative weights are not arbitrary species knobs; they are pushed down to disconnected conserved source blocks",
            "parent_signed": False,
            "remaining_gap": "ordinary matter exchange connectivity and source-shadow exclusion must be proved or bounded",
            "valid_for_claim": False,
        },
    ]


def source_owner_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "owner_id": "THO1765_0_total_action",
            "owner_clause": "ordinary active source is derived from one total matter action",
            "mathematical_form": "S_matter[Psi,e_obs,theta]=sum_i S_i + S_int",
            "effect": "source is an action derivative, not an independently chosen force law",
            "status": "CONDITIONAL_OWNER_CLEAN",
            "remaining_gap": "parent action signature not yet forced for all ordinary matter",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "THO1765_1_total_hilbert_derivative",
            "owner_clause": "active source is total Hilbert/coframe derivative",
            "mathematical_form": "T_total := delta S_matter/delta e_obs",
            "effect": "interaction and binding terms contribute to the same conserved source",
            "status": "CONDITIONAL_OWNER_CLEAN",
            "remaining_gap": "non-Hilbert or post-readout source owners must be excluded",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "THO1765_2_interaction_stress",
            "owner_clause": "interaction stress belongs to the same source object",
            "mathematical_form": "T_total=sum_i T_i + T_int, with nabla_mu T_total^{mu nu}=0",
            "effect": "species-only weighted sources cannot ignore exchange/binding stress without a conservation price",
            "status": "DERIVATION_PRESSURE_GAINED",
            "remaining_gap": "need explicit parent decomposition for ordinary matter/binding sectors",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "THO1765_3_source_shadow_ban",
            "owner_clause": "no separate source-shadow functional",
            "mathematical_form": "not exists S_source=sum_i w_i S_i used only in E_munu while S_matter drives nongrav dynamics",
            "effect": "forbids pure source-only weights that do not appear in the matter theory",
            "status": "BEST_PARENT_OBJECT_LANGUAGE_CLAUSE",
            "remaining_gap": "must be signed by parent grammar or derived from quotient minimality",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "THO1765_4_owner_verdict",
            "owner_clause": "total Hilbert source owner",
            "mathematical_form": "ordinary source owner = delta S_matter/delta e_obs",
            "effect": "would close source-side GR/Newton coupling up to left-hand field equation and hidden-current gates",
            "status": "CONTRACT_READY_PARENT_UNSIGNED",
            "remaining_gap": "source-shadow ban and ordinary exchange connectivity remain live",
            "valid_for_claim": False,
        },
    ]


def no_prefactor_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "NSP1765_0_target",
            "claim_piece": "no independent source-only species prefactors",
            "mathematical_form": "partial S_matter/partial w_A = 0 for source-only w_A; equivalently no w_A coordinate exists",
            "proof_status": "TARGET_EXACT",
            "proof_result": "would close PAC954_1 if parent object language signs it",
            "gap": "absence of a coordinate is a parent grammar theorem, not yet derived from existing corpus",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "NSP1765_1_same_action_filter",
            "claim_piece": "same-action principle rejects source-only duplication",
            "mathematical_form": "E_Psi=delta S_matter/delta Psi and T=delta S_matter/delta e_obs from the same S_matter",
            "proof_status": "DERIVED_FILTER",
            "proof_result": "separate source weights are illegal if they live only in a shadow source functional",
            "gap": "does not exclude weights that multiply real disconnected matter subactions",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "NSP1765_2_exchange_filter",
            "claim_piece": "Bianchi/Noether exchange rejects weights across interacting sectors",
            "mathematical_form": "sum_i w_i C_i^nu=0 forces w_i=w_j on every nonzero exchange edge",
            "proof_status": "DERIVED_CONDITIONAL_FILTER",
            "proof_result": "relative species prefactors collapse to conserved exchange-block prefactors",
            "gap": "ordinary matter graph connectivity is not yet proved from parent sources",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "NSP1765_3_common_prefactor",
            "claim_piece": "common prefactor is not a WEP residual",
            "mathematical_form": "S_matter -> w_star S_matter gives kappa_eff=kappa w_star",
            "proof_status": "COMMON_MODE_ABSORBABLE",
            "proof_result": "one common source normalization is calibration, not composition dependence",
            "gap": "only relative block weights remain dangerous",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "NSP1765_4_current_verdict",
            "claim_piece": "current no-source-prefactor theorem",
            "mathematical_form": "no w_A source prefactors",
            "proof_status": "PARTIAL_THEOREM_NOT_FULL_PARENT_PROOF",
            "proof_result": "source-only shadow weights are identified as forbidden-by-contract; interaction-connected relative weights are forbidden conditionally; disconnected block weights remain",
            "gap": "must prove no source shadow and one connected ordinary matter exchange block, or bound delta_w_block",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1765_0_disconnected_conserved_blocks",
            "countermodel": "two independently conserved ordinary source blocks",
            "mathematical_form": "nabla T_A=0, nabla T_B=0, T_active=w_A T_A+w_B T_B",
            "survives_current_constraints": True,
            "why_survives": "Bianchi allows different weights for truly disconnected conserved blocks",
            "what_kills_it": "prove ordinary matter is one connected exchange component for the tested regime",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1765_1_source_shadow_functional",
            "countermodel": "source functional separate from matter-dynamics functional",
            "mathematical_form": "S_dynamics=sum_i S_i, S_source=sum_i w_i S_i",
            "survives_current_constraints": True,
            "why_survives": "same-action principle is a contract unless parent grammar forbids the shadow functional",
            "what_kills_it": "typed object-language theorem: the active source is only delta S_matter/delta e_obs",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1765_2_hidden_nonHilbert_source",
            "countermodel": "non-Hilbert source current carries material labels",
            "mathematical_form": "T_active=T_Hilbert + J_label",
            "survives_current_constraints": True,
            "why_survives": "Hilbert-source theorem does not silence extra parent currents until excluded",
            "what_kills_it": "no non-Hilbert ordinary source current clause",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1765_3_wrong_decomposition",
            "countermodel": "chosen species decomposition hides interaction stress or binding energy",
            "mathematical_form": "T_total != sum_A T_A unless T_int/binding included",
            "survives_current_constraints": True,
            "why_survives": "bound rows need the actual composition/source projection, not loose labels",
            "what_kills_it": "source-backed component basis with binding/interactions included",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1765_4_verdict",
            "countermodel": "delta_w_block residual",
            "mathematical_form": "T_active=sum_C (1+delta_w_C) T_C over disconnected exchange components",
            "survives_current_constraints": True,
            "why_survives": "1765 collapses species weights to block weights but does not yet prove only one block",
            "what_kills_it": "1766 exchange-graph connectivity theorem or finite sourced block bound",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def deltaw_block_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWB1765_0_delta_w_block",
            "quantity": "delta_w_block",
            "meaning": "residual source prefactor over disconnected Noether exchange components",
            "mathematical_form": "T_active=sum_C (1+delta_w_C) T_C",
            "units": "dimensionless",
            "required_input": "prove one connected ordinary matter block or provide finite bound on block weights",
            "status": "MISSING_EXCHANGE_CONNECTIVITY_OR_NUMERIC_BOUND",
            "source_path": str(OUTPUTS["noether_collapse"]),
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWB1765_1_exchange_graph",
            "quantity": "ordinary matter exchange graph",
            "meaning": "nodes are source components; edges are nonzero Noether exchange currents",
            "mathematical_form": "edge i-j iff C_ij^nu not identically zero in tested matter regime",
            "units": "graph",
            "required_input": "parent/source-backed node list and interaction/binding edges",
            "status": "MISSING_SOURCE_GRAPH",
            "source_path": "TBD",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWB1765_2_projection",
            "quantity": "composition-to-block projection",
            "meaning": "map test-body composition to block-source fractions",
            "mathematical_form": "eta_AB ~ sum_C (f_C^A-f_C^B) delta_w_C",
            "units": "dimensionless",
            "required_input": "material fractions, binding fractions, and experiment-specific source projection",
            "status": "MISSING_ARENA_PROJECTION",
            "source_path": "TBD",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWB1765_3_bound_table",
            "quantity": "delta_w_block_bound",
            "meaning": "finite empirical upper bound if exchange graph has more than one block",
            "mathematical_form": "|delta_w_C-delta_w_D| <= bound_from_WEP_R10_PPN_clock_or_orbital_projection",
            "units": "dimensionless",
            "required_input": "source-backed local bound table with projection convention",
            "status": "MISSING_SOURCE_BACKED_BOUND_TABLE",
            "source_path": "source-intake/rab-sector/acquisition-queue/JR1765_DELTAW_BLOCK_BOUND_INPUT.csv",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWB1765_4_nonclaim_lock",
            "quantity": "local-GR/WEP/R10 claim status",
            "meaning": "source coupling branch remains blocked until proof or bound closes",
            "mathematical_form": "claim_allowed=false until no source shadow + connected graph or finite sourced bound",
            "units": "status",
            "required_input": "future 1766 proof/bound validation",
            "status": "NONCLAIM_LOCK",
            "source_path": str(OUTPUTS["claim_gate"]),
            "valid_for_claim": False,
        },
    ]


def source_zero_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1765_0_derivation_gain",
            "quantity": "relative source prefactors",
            "current_status": "COLLAPSED_TO_EXCHANGE_BLOCKS_CONDITIONALLY",
            "evidence": "NEC1765_2 and NEC1765_3",
            "remaining_gap": "prove tested ordinary matter has one connected exchange block",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1765_1_no_source_shadow",
            "quantity": "source-shadow functional",
            "current_status": "NOT_PARENT_EXCLUDED",
            "evidence": "THO1765_3 identifies the needed typed object-language ban",
            "remaining_gap": "parent grammar must forbid a separate source functional",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1765_2_delta_w_species",
            "quantity": "delta_w_species",
            "current_status": "REFINED_TO_DELTA_W_BLOCK",
            "evidence": "Noether exchange collapse kills weights inside connected components",
            "remaining_gap": "block residual remains until connectivity/bound is closed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1765_3_local_GR",
            "quantity": "local GR / WEP / R10 branch",
            "current_status": "NOT_CLAIMABLE",
            "evidence": "delta_w_block and source-shadow gates remain open",
            "remaining_gap": "no local-GR, WEP, PPN, clock, orbital, or R10 pass allowed from 1765",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1765_4_next",
            "quantity": "next derivation owner",
            "current_status": "EXCHANGE_GRAPH_CONNECTIVITY_IS_NEXT",
            "evidence": "1765 converts the old species-prefactor wound into a sharper graph-connectivity/source-shadow problem",
            "remaining_gap": "build 1766 exchange graph connectivity theorem or delta_w_block bound pack",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1765_0_derivation_gain",
            "decision": "NOETHER_EXCHANGE_COLLAPSE_IS_REAL_PROGRESS",
            "reason": "Bianchi conservation plus interaction exchange forces equal weights on every nonzero exchange edge",
            "next_action": "use block law instead of treating every species weight as independent",
            "valid_for_claim": False,
        },
        {
            "branch_id": "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428",
            "decision_id": "DEC1765_1_no_promotion",
            "decision": "NO_LOCAL_SOURCE_CLAIM",
            "reason": "ordinary exchange graph connectivity and source-shadow exclusion remain unsigned",
            "next_action": "retain nonclaim lock",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1765_2_residual_refinement",
            "decision": "DELTA_W_SPECIES_REFINED_TO_DELTA_W_BLOCK",
            "reason": "species-level weights are overbroad if sectors exchange stress; only disconnected conserved blocks can carry independent weights",
            "next_action": "track delta_w_block rather than loose delta_w_species in future bound rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1765_3_best_next",
            "decision": "EXCHANGE_GRAPH_CONNECTIVITY_AND_SOURCE_SHADOW_BAN_IS_NEXT",
            "reason": "these are the exact remaining gates after the Noether collapse theorem",
            "next_action": "build 1766 ordinary matter exchange-graph connectivity theorem or delta_w_block bound pack",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1765_0_noether_collapse",
            "claim": "relative weights collapse on each exchange-connected component",
            "gate_pass": False,
            "status": "NONCLAIM_THEOREM_GATE",
            "blocker": "BLOCKED_PARENT_SOURCE_COMPONENTS_AND_EXCHANGE_GRAPH_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1765_1_connected_ordinary_matter",
            "claim": "tested ordinary matter is one connected source-exchange component",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_ORDINARY_MATTER_EXCHANGE_CONNECTIVITY_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1765_2_no_source_shadow",
            "claim": "no separate source-shadow functional exists",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_PARENT_OBJECT_LANGUAGE_SOURCE_SHADOW_BAN_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1765_3_delta_w_block_zero",
            "claim": "delta_w_block=0",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_DISCONNECTED_BLOCK_COUNTERMODEL_SURVIVES",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1765_4_delta_w_block_bound",
            "claim": "delta_w_block finite source-backed bound exists",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_SOURCE_GRAPH_PROJECTION_BOUND_TABLE_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1765_5_local_GR_WEP_R10",
            "claim": "local GR / WEP / R10 source branch passes",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_DELTA_W_BLOCK_AND_SOURCE_SHADOW_GATES_OPEN",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1765_0_primary",
            "next_target": "1766-Y5-R2FR-ordinary-matter-exchange-graph-connectivity-and-source-shadow-ban-or-deltaw-block-bound.md",
            "script": "scripts/Y5_R2FR_ordinary_matter_exchange_graph_connectivity_and_source_shadow_ban_or_deltaw_block_bound.py",
            "objective": "prove tested ordinary matter is one exchange-connected total-Hilbert source with no source-shadow functional; otherwise stage finite delta_w_block bound inputs",
            "selection_status": "selected",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1765_1_fallback",
            "next_target": "1766b-Y5-R2FR-deltaw-block-source-graph-bound-pack.md",
            "script": "scripts/Y5_R2FR_deltaw_block_source_graph_bound_pack.py",
            "objective": "source component graph, material projections, and experiment bounds for disconnected block weights",
            "selection_status": "held_fallback",
            "valid_for_claim": False,
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "noether_collapse": noether_collapse_rows(),
        "source_owner": source_owner_rows(),
        "no_prefactor": no_prefactor_rows(),
        "countermodel": countermodel_rows(),
        "deltaw_block": deltaw_block_rows(),
        "source_zero_status": source_zero_status_rows(),
        "decision": decision_rows(),
        "claim_gate": claim_gate_rows(),
        "next_target": next_target_rows(),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv_ok(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1765_SOURCE_REGISTER.csv")
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        shutil.copy2(path, MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(path, QUARANTINE / filename)
        shutil.copy2(path, RAB_QUEUE / f"JR1765_{key.upper()}.csv")


def claim_like_field(key: str) -> bool:
    return key.lower() in {
        "valid_for_claim",
        "claim_allowed",
        "gate_pass",
        "prediction_allowed",
        "score_allowed",
        "claim_pass",
        "selected",
    }


def boolish_claim_true(key: str, value: Any) -> bool:
    if key.lower() == "selected":
        return False
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            for key, value in row.items():
                if claim_like_field(key) and boolish_claim_true(key, value):
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    status_keys = {"current_status", "status", "proof_status", "derivation_result", "proof_result"}
    for rows in rows_map.values():
        for row in rows:
            combined_status = " ".join(str(row.get(key, "")) for key in status_keys)
            if "MISSING_" in combined_status:
                for key, value in row.items():
                    if claim_like_field(key) and boolish_claim_true(key, value):
                        return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1765_SOURCE_REGISTER.csv").exists():
        return False
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1765_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched_for_1765() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*1765*"))


def csv_parse_all() -> bool:
    return all(parse_csv_ok(path) for key, path in OUTPUTS.items() if key != "validation")


def noether_theorem_recorded(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["theorem_id"] == "NEC1765_2_weight_collapse"
        and row["status"] == "DERIVED_CONDITIONAL_THEOREM"
        and row["valid_for_claim"] is False
        for row in rows_map["noether_collapse"]
    )


def block_law_recorded(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["theorem_id"] == "NEC1765_3_connected_component_law"
        and row["status"] == "EXACT_BLOCK_LAW"
        for row in rows_map["noether_collapse"]
    )


def no_promotion(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["theorem_id"] == "NEC1765_5_current_verdict"
        and row["status"] == "PARTIAL_DERIVATION_PARENT_UNSIGNED"
        and row["valid_for_claim"] is False
        for row in rows_map["noether_collapse"]
    )


def countermodel_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["countermodel_id"] == "CM1765_4_verdict"
        and row["survives_current_constraints"] is True
        and row["valid_for_claim"] is False
        for row in rows_map["countermodel"]
    )


def deltaw_block_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["deltaw_block"]
    return any(row["row_id"] == "DWB1765_0_delta_w_block" for row in rows) and all(
        row["valid_for_claim"] is False for row in rows
    )


def source_zero_blocked(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["status_id"] == "SZ1765_3_local_GR"
        and row["current_status"] == "NOT_CLAIMABLE"
        and row["claim_allowed"] is False
        for row in rows_map["source_zero_status"]
    )


def next_selected(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["route_id"] == "NEXT1765_0_primary" and row["selection_status"] == "selected"
        for row in rows_map["next_target"]
    )


def check_row(check_id: str, condition: bool, pass_detail: str, fail_detail: str) -> dict[str, str]:
    return {
        "branch_id": BRANCH_ID,
        "check_id": check_id,
        "result": "PASS" if condition else "FAIL",
        "detail": pass_detail if condition else fail_detail,
    }


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    sources = rows_map["source_register"]
    claim_gates = rows_map["claim_gate"]
    checks = [
        check_row("VAL1765_0_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist", "one or more cited source paths missing"),
        check_row("VAL1765_1_needles_present", all(row["needles_present"] for row in sources), "required source needles are present", "one or more source needles missing"),
        check_row("VAL1765_2_noether_theorem", noether_theorem_recorded(rows_map), "Noether exchange collapse theorem recorded", "Noether exchange theorem missing"),
        check_row("VAL1765_3_block_law", block_law_recorded(rows_map), "connected-component block law recorded", "block law missing"),
        check_row("VAL1765_4_not_promoted", no_promotion(rows_map), "1765 theorem remains parent-unsigned/nonclaim", "1765 theorem was promoted"),
        check_row("VAL1765_5_countermodel_retained", countermodel_retained(rows_map), "delta_w_block countermodel remains retained", "delta_w_block countermodel missing or promoted"),
        check_row("VAL1765_6_deltaw_block_nonclaim", deltaw_block_nonclaim(rows_map), "delta_w_block input rows remain nonclaim", "delta_w_block rows missing or promoted"),
        check_row("VAL1765_7_source_zero_blocked", source_zero_blocked(rows_map), "local source status remains blocked", "local source status missing or promoted"),
        check_row(
            "VAL1765_8_claim_gates_safe",
            all(row["gate_pass"] is False and row["status"] in {"BLOCKED", "NONCLAIM_THEOREM_GATE"} for row in claim_gates),
            "all claim gates remain blocked/nonclaim",
            "one or more claim gates opened",
        ),
        check_row("VAL1765_9_no_claim_flags", no_claim_flags(rows_map), "claim/no-score flags stay false", "one or more claim/no-score flags enabled"),
        check_row("VAL1765_10_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready", "a MISSING_* row is marked ready"),
        check_row(
            "VAL1765_11_decision_next",
            any(row["decision_id"] == "DEC1765_3_best_next" and row["decision"] == "EXCHANGE_GRAPH_CONNECTIVITY_AND_SOURCE_SHADOW_BAN_IS_NEXT" for row in rows_map["decision"]),
            "decision selects exchange-graph/source-shadow route",
            "best-next decision missing",
        ),
        check_row("VAL1765_12_next_selected", next_selected(rows_map), "next target selected", "next target missing"),
        check_row("VAL1765_13_csv_parse", csv_parse_all(), "all generated 1765 CSVs parse", "one or more generated 1765 CSVs fail to parse"),
        check_row("VAL1765_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "branch copies missing"),
        check_row("VAL1765_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check_row("VAL1765_16_formalization_untouched", formalization_untouched_for_1765(), "no 1765 outputs found under formalization-workbench", "1765 outputs found under formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in checks)
    checks.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1765_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1765 total Hilbert source owner and no-prefactor clause or delta_w block bound input",
        }
    )
    return checks


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, str]]) -> str:
    sections = [
        "# 1765 - Total Hilbert Source Owner And No-Prefactor Clause Or Delta_w Species Bound Input",
        "",
        "## Verdict",
        "- 1765 makes a genuine derivation gain: Bianchi plus Noether exchange does not allow arbitrary relative source weights across interacting matter subcurrents.",
        "- If `nabla_mu T_i^{mu nu}=C_i^nu` and `sum_i C_i^nu=0`, then a weighted source `sum_i w_i T_i` is conserved only if `sum_i w_i C_i^nu=0`. Every live exchange edge forces equal weights across that edge.",
        "- Therefore the old loose `delta_w_species` residual is too pessimistic. It collapses to `delta_w_block`: a residual only over disconnected conserved source blocks.",
        "- If tested ordinary matter is one exchange-connected total-Hilbert source, the remaining common factor is just `G`/Newton calibration and `delta_w_species=0` follows conditionally.",
        "- Current MTS still cannot claim the pass because the parent corpus has not yet signed the ordinary-matter exchange graph or the ban on separate source-shadow functionals.",
        "- No GitHub, public, local-GR, Newton, PPN, WEP, clock, orbital, R10, or `q_loc=0` claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Noether Exchange Collapse Theorem",
        markdown_table(rows_map["noether_collapse"], ["theorem_id", "claim_piece", "mathematical_form", "status", "derivation_result", "remaining_gap"]),
        "",
        "## Total Hilbert Source Owner Audit",
        markdown_table(rows_map["source_owner"], ["owner_id", "owner_clause", "mathematical_form", "effect", "status", "remaining_gap"]),
        "",
        "## No-Source-Prefactor Proof Attempt",
        markdown_table(rows_map["no_prefactor"], ["attempt_id", "claim_piece", "mathematical_form", "proof_status", "proof_result", "gap"]),
        "",
        "## Countermodel Ledger",
        markdown_table(rows_map["countermodel"], ["countermodel_id", "countermodel", "mathematical_form", "survives_current_constraints", "why_survives", "what_kills_it"]),
        "",
        "## Delta-w Block Bound Input",
        markdown_table(rows_map["deltaw_block"], ["row_id", "quantity", "meaning", "mathematical_form", "units", "status", "valid_for_claim"]),
        "",
        "## Source-Zero Status",
        markdown_table(rows_map["source_zero_status"], ["status_id", "quantity", "current_status", "evidence", "remaining_gap"]),
        "",
        "## Decisions",
        markdown_table(rows_map["decision"], ["decision_id", "decision", "reason", "next_action"]),
        "",
        "## Claim Gates",
        markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "status", "blocker"]),
        "",
        "## Next Target",
        markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
        "",
        "## Validation",
        markdown_table(validation_rows, ["check_id", "result", "detail"]),
        "",
        "## Working Interpretation",
        "This is better than simply saying `the coupling is missing`. The missing coupling has been squeezed: arbitrary species weights are not compatible with a conserved gravitational source once ordinary matter components exchange energy-momentum. The remaining loopholes are sharply named: a separate source-shadow functional, a hidden non-Hilbert source, or genuinely disconnected conserved source blocks. That is the next battlefield.",
        "",
    ]
    return "\n".join(sections)


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1765-Y5-R2FR-total-Hilbert-source-owner-and-no-prefactor-clause-or-deltaw-species-bound-input.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1765 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
