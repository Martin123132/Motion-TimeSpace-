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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1766"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1766_0_1765_handoff",
        "source_key": "1765_exchange_graph_next",
        "source_path": ROOT / "1765-Y5-R2FR-total-Hilbert-source-owner-and-no-prefactor-clause-or-deltaw-species-bound-input.md",
        "needles": ["EXCHANGE_GRAPH_CONNECTIVITY_AND_SOURCE_SHADOW_BAN_IS_NEXT", "NEXT1765_0_primary"],
    },
    {
        "source_id": "SRC1766_1_1765_validation",
        "source_key": "1765_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1765_VALIDATION.csv",
        "needles": ["VAL1765_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1766_2_1765_noether",
        "source_key": "1765_noether_collapse",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1765_NOETHER_EXCHANGE_COLLAPSE_THEOREM.csv",
        "needles": ["NEC1765_2_weight_collapse", "NEC1765_3_connected_component_law"],
    },
    {
        "source_id": "SRC1766_3_1765_source_owner",
        "source_key": "1765_source_owner",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1765_TOTAL_HILBERT_SOURCE_OWNER_AUDIT.csv",
        "needles": ["THO1765_3_source_shadow_ban", "THO1765_4_owner_verdict"],
    },
    {
        "source_id": "SRC1766_4_1765_countermodel",
        "source_key": "1765_countermodels",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1765_COUNTERMODEL_LEDGER.csv",
        "needles": ["CM1765_0_disconnected_conserved_blocks", "CM1765_4_verdict"],
    },
    {
        "source_id": "SRC1766_5_1765_block_input",
        "source_key": "1765_delta_w_block_input",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1765_DELTAW_BLOCK_BOUND_INPUT.csv",
        "needles": ["DWB1765_0_delta_w_block", "MISSING_EXCHANGE_CONNECTIVITY_OR_NUMERIC_BOUND"],
    },
    {
        "source_id": "SRC1766_6_954_action_clause",
        "source_key": "954_total_hilbert_source",
        "source_path": RESIDUALS / "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv",
        "needles": ["PAC954_1_no_source_prefactors", "PAC954_2_total_Hilbert_derivative"],
    },
    {
        "source_id": "SRC1766_7_955_minimal_matter",
        "source_key": "955_same_action_filter",
        "source_path": RESIDUALS / "P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv",
        "needles": ["MMA955_1_same_action_principle", "MMA955_6_verdict"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1766_SOURCE_REGISTER.csv",
    "exchange_connectivity": RESIDUALS / "P8_Y5_PARENT_QLOC_1766_ORDINARY_MATTER_EXCHANGE_CONNECTIVITY_THEOREM.csv",
    "graph_certificate": RESIDUALS / "P8_Y5_PARENT_QLOC_1766_STANDARD_MATTER_GRAPH_CERTIFICATE_ATTEMPT.csv",
    "source_shadow": RESIDUALS / "P8_Y5_PARENT_QLOC_1766_SOURCE_SHADOW_BAN_ATTEMPT.csv",
    "countermodel": RESIDUALS / "P8_Y5_PARENT_QLOC_1766_COUNTERMODEL_LEDGER.csv",
    "residual_interface": RESIDUALS / "P8_Y5_PARENT_QLOC_1766_RESIDUAL_BOUND_INTERFACE.csv",
    "source_zero_status": RESIDUALS / "P8_Y5_PARENT_QLOC_1766_SOURCE_ZERO_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1766_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1766_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1766_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1766_VALIDATION.csv",
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
                "role": "ordinary matter exchange graph connectivity and source-shadow ban or delta_w block bound",
                "valid_for_claim": False,
            }
        )
    return rows


def exchange_connectivity_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "OMC1766_0_graph_definition",
            "claim_piece": "ordinary matter exchange graph",
            "mathematical_form": "G_ord=(V,E), V=Hilbert-source subcurrents, edge i-j iff C_ij^nu is not identically zero",
            "status": "DEFINITION_SHARP",
            "derivation_result": "1765 block weights are constants on connected components of this graph",
            "remaining_gap": "parent must identify the allowed node basis and exchange currents",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "OMC1766_1_connected_graph_implication",
            "claim_piece": "connected ordinary matter source",
            "mathematical_form": "G_ord connected => T_active=w_star T_total",
            "status": "DERIVED_CONDITIONAL_THEOREM",
            "derivation_result": "all relative block weights collapse to one common calibration factor",
            "remaining_gap": "connectivity of tested ordinary matter must be parent/source certified",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "OMC1766_2_lab_matter_graph",
            "claim_piece": "baryonic laboratory matter connectivity",
            "mathematical_form": "electron -- EM/binding -- proton/nucleus -- nuclear binding -- neutron; atoms/molecules/lattices inherit the same total Hilbert source",
            "status": "STANDARD_MATTER_CONNECTIVITY_CONTRACT",
            "derivation_result": "ordinary atomic test bodies appear connected once interaction/binding stress is included",
            "remaining_gap": "needs source-backed component graph certificate before a public WEP/local-GR claim",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "OMC1766_3_decoupled_sector_limit",
            "claim_piece": "decoupled sectors are separate blocks",
            "mathematical_form": "if C_Di^nu=0 for all ordinary i, then T_D can carry independent w_D without violating Bianchi",
            "status": "EXACT_LIMIT",
            "derivation_result": "dark/radiation/neutrino-like non-test-body sectors must be treated as separate blocks or excluded from the local test arena",
            "remaining_gap": "arena-specific source inventory still required",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "OMC1766_4_current_verdict",
            "claim_piece": "delta_w_block for ordinary test bodies",
            "mathematical_form": "delta_w_block^ordinary=0 if G_ord is connected and source owner is total Hilbert current",
            "status": "CONDITIONAL_ORDINARY_BLOCK_ZERO_PARENT_UNSIGNED",
            "derivation_result": "the residual is narrowed to source-shadow or truly decoupled block leakage",
            "remaining_gap": "source-shadow ban plus source-backed graph certificate remain unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def graph_certificate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "cert_id": "SMG1766_0_node_basis",
            "certificate_piece": "ordinary source nodes",
            "mathematical_form": "nodes={leptonic charged matter, baryonic/nuclear matter, EM field/binding, nuclear binding, molecular/lattice binding}",
            "status": "CANDIDATE_NODE_BASIS",
            "confidence": "PRIVATE_CONTRACT_ONLY",
            "missing_for_claim": "source-backed node basis and arena-specific inclusion/exclusion rules",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "cert_id": "SMG1766_1_electron_nucleus_edge",
            "certificate_piece": "charged matter connected by EM/binding stress",
            "mathematical_form": "C_e^nu + C_EM/bind^nu + C_nucleus^nu=0 in bound atoms",
            "status": "STANDARD_MATTER_EDGE_CONTRACT",
            "confidence": "PRIVATE_CONTRACT_ONLY",
            "missing_for_claim": "source citation/component convention for EM and binding stress",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "cert_id": "SMG1766_2_proton_neutron_edge",
            "certificate_piece": "nuclear components connected by nuclear binding stress",
            "mathematical_form": "C_p^nu + C_n^nu + C_nuclear_bind^nu=0 inside nuclei",
            "status": "STANDARD_MATTER_EDGE_CONTRACT",
            "confidence": "PRIVATE_CONTRACT_ONLY",
            "missing_for_claim": "source citation/component convention for nuclear binding stress",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "cert_id": "SMG1766_3_macroscopic_body_edge",
            "certificate_piece": "atoms, molecules and solids inherit connected source through binding/lattice stress",
            "mathematical_form": "T_body=T_rest+T_EM_bind+T_nuclear_bind+T_lattice+... as one Hilbert source",
            "status": "STANDARD_MATTER_EDGE_CONTRACT",
            "confidence": "PRIVATE_CONTRACT_ONLY",
            "missing_for_claim": "arena-specific material model and binding-energy projection",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "cert_id": "SMG1766_4_certificate_verdict",
            "certificate_piece": "ordinary lab matter exchange graph",
            "mathematical_form": "candidate graph connected for atomic/nuclear test bodies, excluding decoupled non-test-body sectors",
            "status": "GRAPH_CERTIFICATE_READY_FOR_SOURCING_NOT_CLAIM",
            "confidence": "PRIVATE_HIGH_LEVEL_ONLY",
            "missing_for_claim": "source-backed graph rows, citations, and local-arena projection table",
            "valid_for_claim": False,
        },
    ]


def source_shadow_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SSB1766_0_target",
            "claim_piece": "no source-shadow functional",
            "mathematical_form": "not exists S_source[Psi,e_obs,w_i] separate from S_matter used only in gravitational field equation",
            "proof_status": "TARGET_EXACT",
            "proof_result": "would remove the cleanest bypass around exchange connectivity",
            "gap": "parent object language has not yet signed the single-source-owner grammar",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SSB1766_1_variational_owner_filter",
            "claim_piece": "same variational action owns dynamics and source",
            "mathematical_form": "E_Psi=delta S_matter/delta Psi and T=delta S_matter/delta e_obs",
            "proof_status": "CONDITIONAL_OBJECT_LANGUAGE_THEOREM",
            "proof_result": "a source-shadow weight is not an allowed coordinate if source equals total Hilbert derivative by definition",
            "gap": "this is a grammar theorem only after the parent action forbids alternate source maps",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SSB1766_2_conservation_filter",
            "claim_piece": "source-shadow current must be conserved or real",
            "mathematical_form": "nabla_mu(E^{mu nu})=0 implies nabla_mu(T_shadow^{mu nu})=0; otherwise field equation is inconsistent",
            "proof_status": "DERIVED_FILTER",
            "proof_result": "an uncoupled shadow source either violates Bianchi or behaves as a real independently conserved source block",
            "gap": "real conserved shadow blocks still need exclusion or bound",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SSB1766_3_no_hidden_source_map",
            "claim_piece": "no post-variation material projector",
            "mathematical_form": "T_active != P_material(delta S_matter/delta e_obs) unless P_material=identity",
            "proof_status": "CONTRACT_NEEDED",
            "proof_result": "post-variation material projectors can reintroduce composition dependence after the connected graph theorem",
            "gap": "hidden source-map/projector ban remains unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SSB1766_4_current_verdict",
            "claim_piece": "source-shadow ban for current MTS parent",
            "mathematical_form": "T_active=delta S_matter/delta e_obs and no other ordinary source map",
            "proof_status": "CONTRACT_READY_PARENT_UNSIGNED",
            "proof_result": "source-shadow route is sharply isolated but not eliminated",
            "gap": "needs 1767 single-action/source-map grammar closure or finite shadow bound",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1766_0_decoupled_conserved_block",
            "countermodel": "ordinary plus decoupled conserved sector",
            "mathematical_form": "T_active=w_ord T_ord + w_D T_D, with nabla T_ord=nabla T_D=0",
            "survives_current_constraints": True,
            "why_survives": "Bianchi permits different weights for truly disconnected conserved blocks",
            "what_kills_it": "arena proof that T_D is absent from test source or finite bound on w_D-w_ord",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1766_1_source_shadow",
            "countermodel": "source-shadow functional or source map",
            "mathematical_form": "T_active=delta S_matter/delta e_obs + delta_w_shadow T_shadow",
            "survives_current_constraints": True,
            "why_survives": "single-source-owner is not parent-signed",
            "what_kills_it": "typed parent grammar forbids non-Hilbert/source-shadow ordinary currents",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1766_2_hidden_projector",
            "countermodel": "post-variation material projector",
            "mathematical_form": "T_active=P_A(T_total) with material-dependent P_A",
            "survives_current_constraints": True,
            "why_survives": "connectivity before variation does not by itself ban post-variation readout/source filters",
            "what_kills_it": "identity-only source map theorem",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1766_3_unsourced_graph",
            "countermodel": "incorrect ordinary graph omits binding or interaction stress",
            "mathematical_form": "T_body split into separately weighted pseudo-components without T_bind",
            "survives_current_constraints": True,
            "why_survives": "a bad component basis can fake disconnected blocks",
            "what_kills_it": "source-backed Hilbert-current component graph including binding stress",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1766_4_verdict",
            "countermodel": "ordinary block zero remains conditional",
            "mathematical_form": "delta_w_ord=0 conditional; delta_w_shadow/decoupled retained",
            "survives_current_constraints": True,
            "why_survives": "1766 narrows the problem but does not sign source-shadow or source-backed graph rows",
            "what_kills_it": "1767 source-shadow/source-map closure plus graph sourcing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def residual_interface_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "RBI1766_0_delta_w_ord",
            "quantity": "delta_w_ordinary_connected_block",
            "meaning": "relative ordinary-matter source weight after exchange connectivity",
            "mathematical_form": "delta_w_ord=0 if G_ord connected and T_active=T_Hilbert",
            "units": "dimensionless",
            "status": "CONDITIONAL_ZERO_PARENT_UNSIGNED",
            "required_input": "source-backed ordinary graph certificate plus source-shadow ban",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RBI1766_1_delta_w_shadow",
            "quantity": "delta_w_shadow",
            "meaning": "source-shadow/non-Hilbert/projector leakage after Hilbert variation",
            "mathematical_form": "T_active=T_Hilbert + delta_w_shadow T_shadow",
            "units": "dimensionless",
            "status": "MISSING_SOURCE_SHADOW_BAN_OR_BOUND",
            "required_input": "single-source-owner theorem or finite bound",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RBI1766_2_delta_w_decoupled",
            "quantity": "delta_w_decoupled",
            "meaning": "independent weight for decoupled conserved sectors absent from ordinary test bodies",
            "mathematical_form": "T_active=w_ord T_ord + w_D T_D",
            "units": "dimensionless",
            "status": "MISSING_ARENA_EXCLUSION_OR_BOUND",
            "required_input": "arena source inventory: WEP/R10/PPN/clock/orbital/cosmology",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RBI1766_3_graph_sources",
            "quantity": "source-backed graph rows",
            "meaning": "citations and component definitions for ordinary exchange edges",
            "mathematical_form": "node, edge, exchange_current, included_binding_term, source_path",
            "units": "table",
            "status": "MISSING_SOURCE_BACKED_GRAPH_CERTIFICATE",
            "required_input": "standard matter graph citation pack",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RBI1766_4_nonclaim_lock",
            "quantity": "local-GR/WEP/R10 claim status",
            "meaning": "ordinary block theorem is not yet a public/local pass",
            "mathematical_form": "claim_allowed=false until graph/source-shadow gates are signed",
            "units": "status",
            "status": "NONCLAIM_LOCK",
            "required_input": "future 1767 validation",
            "valid_for_claim": False,
        },
    ]


def source_zero_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1766_0_derivation_gain",
            "quantity": "ordinary source block",
            "current_status": "CONDITIONALLY_CONNECTED",
            "evidence": "OMC1766_1 and OMC1766_2",
            "remaining_gap": "source-backed graph certificate required",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1766_1_delta_w_block",
            "quantity": "delta_w_block",
            "current_status": "REFINED_TO_SHADOW_OR_DECOUPLED_RESIDUALS",
            "evidence": "OMC1766_4 and RBI1766 rows",
            "remaining_gap": "delta_w_shadow and delta_w_decoupled need proof or bound",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1766_2_source_shadow",
            "quantity": "source-shadow route",
            "current_status": "NOT_PARENT_EXCLUDED",
            "evidence": "SSB1766_4",
            "remaining_gap": "single-action/source-map grammar must be signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1766_3_local_GR",
            "quantity": "local GR / WEP / R10 branch",
            "current_status": "NOT_CLAIMABLE",
            "evidence": "claim gates keep source-shadow and graph sourcing blocked",
            "remaining_gap": "no local-GR, WEP, PPN, clock, orbital, or R10 pass allowed from 1766",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1766_4_next",
            "quantity": "next derivation owner",
            "current_status": "SINGLE_SOURCE_MAP_GRAMMAR_IS_NEXT",
            "evidence": "source-shadow is now the cleanest remaining bypass",
            "remaining_gap": "build 1767 source-shadow/source-map identity theorem or bound",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1766_0_connectivity_gain",
            "decision": "ORDINARY_GRAPH_CONNECTIVITY_CONDITIONALLY_CLOSES_DELTA_W_BLOCK",
            "reason": "connected exchange graph turns all ordinary weights into one common calibration",
            "next_action": "source the graph before any claim",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1766_1_residual_refinement",
            "decision": "DELTA_W_BLOCK_REFINED_TO_SHADOW_OR_DECOUPLED",
            "reason": "ordinary connected matter no longer needs species/block weights except via source-shadow or genuinely decoupled sectors",
            "next_action": "track delta_w_shadow and delta_w_decoupled explicitly",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1766_2_no_claim",
            "decision": "NO_LOCAL_SOURCE_CLAIM",
            "reason": "source-backed graph certificate and source-shadow ban are not parent-signed",
            "next_action": "keep all local/empirical claim gates closed",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1766_3_best_next",
            "decision": "SINGLE_SOURCE_MAP_GRAMMAR_AND_SHADOW_BAN_IS_NEXT",
            "reason": "source-shadow is now the strongest remaining way to bypass the connected ordinary graph theorem",
            "next_action": "build 1767 single-action source-map identity theorem or shadow residual bound",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1766_0_connected_ordinary_graph",
            "claim": "ordinary lab matter exchange graph is connected",
            "gate_pass": False,
            "status": "NONCLAIM_THEOREM_GATE",
            "blocker": "BLOCKED_SOURCE_BACKED_GRAPH_CERTIFICATE_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1766_1_source_shadow_ban",
            "claim": "no source-shadow/non-Hilbert/projector leakage",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_SINGLE_SOURCE_MAP_GRAMMAR_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1766_2_delta_w_ord_zero",
            "claim": "delta_w_ordinary_connected_block=0",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_GRAPH_AND_SOURCE_SHADOW_GATES_OPEN",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1766_3_delta_w_shadow_bound",
            "claim": "delta_w_shadow finite source-backed bound exists",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_SHADOW_BOUND_OR_ZERO_THEOREM_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1766_4_delta_w_decoupled_bound",
            "claim": "delta_w_decoupled arena exclusion or bound exists",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_ARENA_SOURCE_INVENTORY_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1766_5_local_GR_WEP_R10",
            "claim": "local GR / WEP / R10 source branch passes",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_SOURCE_SHADOW_AND_GRAPH_SOURCING_OPEN",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1766_0_primary",
            "next_target": "1767-Y5-R2FR-single-source-map-grammar-and-source-shadow-ban-or-shadow-bound.md",
            "script": "scripts/Y5_R2FR_single_source_map_grammar_and_source_shadow_ban_or_shadow_bound.py",
            "objective": "prove the parent object language admits only the total Hilbert source map and forbids source-shadow/projector currents; otherwise stage delta_w_shadow bound rows",
            "selection_status": "selected",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1766_1_fallback",
            "next_target": "1767b-Y5-R2FR-standard-matter-graph-source-certificate-and-arena-inventory.md",
            "script": "scripts/Y5_R2FR_standard_matter_graph_source_certificate_and_arena_inventory.py",
            "objective": "source ordinary matter graph edges and arena exclusion/bound rows for decoupled sectors",
            "selection_status": "held_fallback",
            "valid_for_claim": False,
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "exchange_connectivity": exchange_connectivity_rows(),
        "graph_certificate": graph_certificate_rows(),
        "source_shadow": source_shadow_rows(),
        "countermodel": countermodel_rows(),
        "residual_interface": residual_interface_rows(),
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
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1766_SOURCE_REGISTER.csv")
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        shutil.copy2(path, MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(path, QUARANTINE / filename)
        shutil.copy2(path, RAB_QUEUE / f"JR1766_{key.upper()}.csv")


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
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1766_SOURCE_REGISTER.csv").exists():
        return False
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1766_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched_for_1766() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*1766*"))


def csv_parse_all() -> bool:
    return all(parse_csv_ok(path) for key, path in OUTPUTS.items() if key != "validation")


def connectivity_theorem_recorded(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["theorem_id"] == "OMC1766_1_connected_graph_implication"
        and row["status"] == "DERIVED_CONDITIONAL_THEOREM"
        and row["valid_for_claim"] is False
        for row in rows_map["exchange_connectivity"]
    )


def graph_certificate_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["cert_id"] == "SMG1766_4_certificate_verdict"
        and row["status"] == "GRAPH_CERTIFICATE_READY_FOR_SOURCING_NOT_CLAIM"
        for row in rows_map["graph_certificate"]
    ) and all(row["valid_for_claim"] is False for row in rows_map["graph_certificate"])


def source_shadow_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["attempt_id"] == "SSB1766_4_current_verdict"
        and row["proof_status"] == "CONTRACT_READY_PARENT_UNSIGNED"
        and row["claim_allowed"] is False
        for row in rows_map["source_shadow"]
    )


def countermodel_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["countermodel_id"] == "CM1766_4_verdict"
        and row["survives_current_constraints"] is True
        and row["valid_for_claim"] is False
        for row in rows_map["countermodel"]
    )


def residual_interface_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["residual_interface"]
    return any(row["row_id"] == "RBI1766_1_delta_w_shadow" for row in rows) and all(
        row["valid_for_claim"] is False for row in rows
    )


def source_zero_blocked(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["status_id"] == "SZ1766_3_local_GR"
        and row["current_status"] == "NOT_CLAIMABLE"
        and row["claim_allowed"] is False
        for row in rows_map["source_zero_status"]
    )


def next_selected(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["route_id"] == "NEXT1766_0_primary" and row["selection_status"] == "selected"
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
        check_row("VAL1766_0_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist", "one or more cited source paths missing"),
        check_row("VAL1766_1_needles_present", all(row["needles_present"] for row in sources), "required source needles are present", "one or more source needles missing"),
        check_row("VAL1766_2_connectivity_theorem", connectivity_theorem_recorded(rows_map), "connected graph implication recorded", "connected graph implication missing"),
        check_row("VAL1766_3_graph_certificate_nonclaim", graph_certificate_nonclaim(rows_map), "graph certificate staged as nonclaim", "graph certificate missing or promoted"),
        check_row("VAL1766_4_source_shadow_retained", source_shadow_retained(rows_map), "source-shadow ban remains parent-unsigned", "source-shadow route promoted or missing"),
        check_row("VAL1766_5_countermodel_retained", countermodel_retained(rows_map), "shadow/decoupled countermodel remains retained", "countermodel missing or promoted"),
        check_row("VAL1766_6_residual_interface_nonclaim", residual_interface_nonclaim(rows_map), "residual interface rows remain nonclaim", "residual interface missing or promoted"),
        check_row("VAL1766_7_source_zero_blocked", source_zero_blocked(rows_map), "local source status remains blocked", "local source status missing or promoted"),
        check_row(
            "VAL1766_8_claim_gates_safe",
            all(row["gate_pass"] is False and row["status"] in {"BLOCKED", "NONCLAIM_THEOREM_GATE"} for row in claim_gates),
            "all claim gates remain blocked/nonclaim",
            "one or more claim gates opened",
        ),
        check_row("VAL1766_9_no_claim_flags", no_claim_flags(rows_map), "claim/no-score flags stay false", "one or more claim/no-score flags enabled"),
        check_row("VAL1766_10_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready", "a MISSING_* row is marked ready"),
        check_row(
            "VAL1766_11_decision_next",
            any(row["decision_id"] == "DEC1766_3_best_next" and row["decision"] == "SINGLE_SOURCE_MAP_GRAMMAR_AND_SHADOW_BAN_IS_NEXT" for row in rows_map["decision"]),
            "decision selects single-source-map/source-shadow route",
            "best-next decision missing",
        ),
        check_row("VAL1766_12_next_selected", next_selected(rows_map), "next target selected", "next target missing"),
        check_row("VAL1766_13_csv_parse", csv_parse_all(), "all generated 1766 CSVs parse", "one or more generated 1766 CSVs fail to parse"),
        check_row("VAL1766_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "branch copies missing"),
        check_row("VAL1766_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check_row("VAL1766_16_formalization_untouched", formalization_untouched_for_1766(), "no 1766 outputs found under formalization-workbench", "1766 outputs found under formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in checks)
    checks.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1766_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1766 ordinary matter exchange graph connectivity and source-shadow ban or delta_w block bound",
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
        "# 1766 - Ordinary Matter Exchange Graph Connectivity And Source-Shadow Ban Or Delta_w Block Bound",
        "",
        "## Verdict",
        "- 1766 sharpens the 1765 block law: if the ordinary-matter exchange graph is connected, all ordinary source weights collapse to one common calibration factor.",
        "- For atomic/nuclear laboratory matter, the candidate graph is connected through EM, nuclear, binding, molecular, and lattice stress once those stresses are included in the total Hilbert source.",
        "- This is not yet a public/local claim because the graph certificate is not source-backed and the parent object language has not yet banned source-shadow or post-variation material projectors.",
        "- The live residual is no longer broad `delta_w_species`; it is now `delta_w_shadow` plus arena-specific `delta_w_decoupled` for truly disconnected sectors.",
        "- No GitHub, public, local-GR, Newton, PPN, WEP, clock, orbital, R10, or `q_loc=0` claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Ordinary Matter Exchange Connectivity Theorem",
        markdown_table(rows_map["exchange_connectivity"], ["theorem_id", "claim_piece", "mathematical_form", "status", "derivation_result", "remaining_gap"]),
        "",
        "## Standard Matter Graph Certificate Attempt",
        markdown_table(rows_map["graph_certificate"], ["cert_id", "certificate_piece", "mathematical_form", "status", "confidence", "missing_for_claim"]),
        "",
        "## Source-Shadow Ban Attempt",
        markdown_table(rows_map["source_shadow"], ["attempt_id", "claim_piece", "mathematical_form", "proof_status", "proof_result", "gap"]),
        "",
        "## Countermodel Ledger",
        markdown_table(rows_map["countermodel"], ["countermodel_id", "countermodel", "mathematical_form", "survives_current_constraints", "why_survives", "what_kills_it"]),
        "",
        "## Residual Bound Interface",
        markdown_table(rows_map["residual_interface"], ["row_id", "quantity", "meaning", "mathematical_form", "units", "status", "valid_for_claim"]),
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
        "This is a useful narrowing. The coupling problem is no longer a fog of arbitrary matter-dependent knobs. Ordinary connected matter wants to carry only one Hilbert source normalization. The main remaining enemy is now cleaner: a shadow source map or projector that reintroduces composition after the variational source has already been formed. That should be attacked directly next.",
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
    doc_path = ROOT / "1766-Y5-R2FR-ordinary-matter-exchange-graph-connectivity-and-source-shadow-ban-or-deltaw-block-bound.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1766 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
