from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_EXCHANGE_GRAPH_GATE_2616"
CHECKPOINT_ID = "2616"

DOC = ROOT / "2616-Y5-R2FR-ordinary-matter-exchange-graph-connectivity-and-source-shadow-ban-or-deltaw-block-bound.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_EXCHANGE_GRAPH_GATE_2616_SOURCE_REGISTER.csv",
    "lineage_ledger": OUT / "P8_Y5_EXCHANGE_GRAPH_GATE_2616_LINEAGE_LEDGER.csv",
    "exchange_connectivity": OUT / "P8_Y5_EXCHANGE_GRAPH_GATE_2616_ORDINARY_MATTER_EXCHANGE_CONNECTIVITY_THEOREM.csv",
    "graph_certificate": OUT / "P8_Y5_EXCHANGE_GRAPH_GATE_2616_STANDARD_MATTER_GRAPH_CERTIFICATE_ATTEMPT.csv",
    "source_shadow": OUT / "P8_Y5_EXCHANGE_GRAPH_GATE_2616_SOURCE_SHADOW_BAN_ATTEMPT.csv",
    "countermodel": OUT / "P8_Y5_EXCHANGE_GRAPH_GATE_2616_COUNTERMODEL_LEDGER.csv",
    "residual_interface": OUT / "P8_Y5_EXCHANGE_GRAPH_GATE_2616_RESIDUAL_BOUND_INTERFACE.csv",
    "source_zero": OUT / "P8_Y5_EXCHANGE_GRAPH_GATE_2616_SOURCE_ZERO_STATUS.csv",
    "claim_gates": OUT / "P8_Y5_EXCHANGE_GRAPH_GATE_2616_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_EXCHANGE_GRAPH_GATE_2616_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_EXCHANGE_GRAPH_GATE_2616_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_EXCHANGE_GRAPH_GATE_2616_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2616_VALIDATION.csv",
}

COPY_TARGETS = {
    "exchange_connectivity": LOCAL_BOUNDS / "Ordinary_matter_exchange_connectivity_theorem_2616_NONCLAIM.csv",
    "residual_interface": LOCAL_BOUNDS / "Residual_bound_interface_2616_NONCLAIM.csv",
    "source_zero": LOCAL_BOUNDS / "Exchange_graph_source_zero_status_2616_NONCLAIM.csv",
    "next_target": QUEUE / "JR2616_SINGLE_SOURCE_MAP_GRAMMAR_NEXT.csv",
}

FALSE_FLAGS = {
    "score_ready": False,
    "valid_prediction_row": False,
    "valid_for_claim": False,
    "claim_allowed": False,
    "accepted_for_scoring": False,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def with_stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def false_flags() -> dict[str, bool]:
    return dict(FALSE_FLAGS)


def row_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    if value is None:
        return ""
    return str(value)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row_value(row.get(field, "")) for field in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), len(rows), ""
    except Exception as exc:
        return False, 0, str(exc)


def path_has_needles(path: Path, needles: list[str]) -> list[str]:
    if not path.exists():
        return needles
    text = path.read_text(encoding="utf-8", errors="replace")
    return [needle for needle in needles if needle not in text]


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        {
            "source_id": "SRC2616_00_2615_handoff_doc",
            "source_key": "2615_exchange_graph_next",
            "source_path": ROOT / "2615-Y5-R2FR-total-Hilbert-source-owner-and-no-prefactor-clause-or-deltaw-species-bound-input.md",
            "needles": ["NEXT2615_0_primary", "EXCHANGE_GRAPH_CONNECTIVITY_AND_SOURCE_SHADOW_BAN_IS_NEXT", "VAL2615_OVERALL"],
            "role": "current 26xx handoff selecting exchange graph/source-shadow gate",
        },
        {
            "source_id": "SRC2616_01_2615_noether",
            "source_key": "2615_noether_collapse",
            "source_path": OUT / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_NOETHER_EXCHANGE_COLLAPSE_THEOREM.csv",
            "needles": ["NEC2615_2_weight_collapse", "NEC2615_3_connected_component_law"],
            "role": "current Noether block law that 2616 tries to close by connectivity",
        },
        {
            "source_id": "SRC2616_02_2615_source_owner",
            "source_key": "2615_source_owner",
            "source_path": OUT / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_TOTAL_HILBERT_SOURCE_OWNER_AUDIT.csv",
            "needles": ["THO2615_3_source_shadow_ban", "THO2615_5_owner_verdict"],
            "role": "current total Hilbert owner/source-shadow gap",
        },
        {
            "source_id": "SRC2616_03_2615_block_input",
            "source_key": "2615_delta_w_block_input",
            "source_path": OUT / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_DELTAW_BLOCK_BOUND_INPUT.csv",
            "needles": ["DWB2615_0_delta_w_block", "DWB2615_6_nonclaim_lock"],
            "role": "current block residual interface",
        },
        {
            "source_id": "SRC2616_04_1766_doc",
            "source_key": "1766_prior_exchange_graph_doc",
            "source_path": ROOT / "1766-Y5-R2FR-ordinary-matter-exchange-graph-connectivity-and-source-shadow-ban-or-deltaw-block-bound.md",
            "needles": ["OMC1766_1_connected_graph_implication", "DEC1766_3_best_next", "VAL1766_OVERALL"],
            "role": "prior exchange graph checkpoint used as lineage evidence",
        },
        {
            "source_id": "SRC2616_05_1766_exchange",
            "source_key": "1766_exchange_connectivity",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1766_ORDINARY_MATTER_EXCHANGE_CONNECTIVITY_THEOREM.csv",
            "needles": ["OMC1766_1_connected_graph_implication", "OMC1766_4_current_verdict"],
            "role": "prior connected ordinary graph theorem and unsigned verdict",
        },
        {
            "source_id": "SRC2616_06_1766_graph_certificate",
            "source_key": "1766_graph_certificate",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1766_STANDARD_MATTER_GRAPH_CERTIFICATE_ATTEMPT.csv",
            "needles": ["SMG1766_0_node_basis", "SMG1766_4_certificate_verdict"],
            "role": "prior candidate graph certificate staged for sourcing",
        },
        {
            "source_id": "SRC2616_07_1766_source_shadow",
            "source_key": "1766_source_shadow_ban",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1766_SOURCE_SHADOW_BAN_ATTEMPT.csv",
            "needles": ["SSB1766_0_target", "SSB1766_4_current_verdict"],
            "role": "prior source-shadow ban and parent unsigned verdict",
        },
        {
            "source_id": "SRC2616_08_1766_residual_interface",
            "source_key": "1766_residual_interface",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1766_RESIDUAL_BOUND_INTERFACE.csv",
            "needles": ["RBI1766_1_delta_w_shadow", "RBI1766_4_nonclaim_lock"],
            "role": "prior refined residual interface for shadow/decoupled sectors",
        },
        {
            "source_id": "SRC2616_09_954_action_clause",
            "source_key": "954_parent_action_clause",
            "source_path": OUT / "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv",
            "needles": ["PAC954_2_total_Hilbert_derivative", "PAC954_3_no_hidden_spurion_return", "PAC954_4_nonHilbert_current_split"],
            "role": "parent action clauses for total source and non-Hilbert bypasses",
        },
        {
            "source_id": "SRC2616_10_955_minimal_matter",
            "source_key": "955_same_action_filter",
            "source_path": OUT / "P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv",
            "needles": ["MMA955_1_same_action_principle", "MMA955_6_verdict"],
            "role": "same-action principle and parent unsigned verdict",
        },
        {
            "source_id": "SRC2616_11_977_constant_certificate",
            "source_key": "977_constant_source_certificate",
            "source_path": OUT / "P8_Y5_R10_977_CONSTANT_SOURCE_CERTIFICATE_ATTEMPT.csv",
            "needles": ["CSC977_3_hilbert_source_current", "CSC977_6_measured_monopole_guard"],
            "role": "Hilbert-source universality and measured-GM guardrail",
        },
    ]
    rows: list[dict[str, Any]] = []
    for spec in specs:
        missing = path_has_needles(spec["source_path"], spec["needles"])
        rows.append(
            with_stamp(
                {
                    "source_id": spec["source_id"],
                    "source_key": spec["source_key"],
                    "source_path": spec["source_path"],
                    "source_exists": spec["source_path"].exists(),
                    "needles": spec["needles"],
                    "needles_present": not missing,
                    "missing_needles": missing,
                    "role": spec["role"],
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def lineage_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "lineage_id": "LIN2616_0_current_parent",
            "input_checkpoint": "2615",
            "input_artifact": "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_*",
            "imported_result": "source weights collapse to exchange-block weights, but block connectivity/source-shadow remain open",
            "2616_use": "try to close ordinary connected block and isolate shadow/decoupled residuals",
        },
        {
            "lineage_id": "LIN2616_1_prior_exchange_graph",
            "input_checkpoint": "1766",
            "input_artifact": "P8_Y5_PARENT_QLOC_1766_*",
            "imported_result": "ordinary lab matter is conditionally connected once binding and interaction stresses are included",
            "2616_use": "port candidate graph certificate into current chain without promoting it",
        },
        {
            "lineage_id": "LIN2616_2_parent_source_signature",
            "input_checkpoint": "954/955/977",
            "input_artifact": "parent action, minimal matter, Hilbert source guardrails",
            "imported_result": "single Hilbert source map is clean but source-shadow/projector bans are unsigned",
            "2616_use": "name the remaining bypass as single-source-map grammar debt",
        },
        {
            "lineage_id": "LIN2616_3_residual_refinement",
            "input_checkpoint": "2615/1766",
            "input_artifact": "delta_w_block and residual bound interfaces",
            "imported_result": "ordinary block residual refines to shadow/projector leakage plus decoupled-sector leakage",
            "2616_use": "track delta_w_shadow and delta_w_decoupled explicitly",
        },
        {
            "lineage_id": "LIN2616_4_claim_policy",
            "input_checkpoint": "all",
            "input_artifact": "claim gates and validation ledgers",
            "imported_result": "no local-GR/Newton/WEP/PPN/clock/orbital/R10 claim without source-backed graph and shadow ban",
            "2616_use": "keep all claim flags false",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def exchange_connectivity_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "theorem_id": "OMC2616_0_graph_definition",
            "claim_piece": "ordinary matter exchange graph",
            "mathematical_form": "G_ord=(V,E), V=Hilbert-source subcurrents, edge i-j iff C_ij^nu is not identically zero",
            "status": "DEFINITION_SHARP",
            "derivation_result": "2615 block weights are constants on connected components of this graph",
            "remaining_gap": "parent must identify the allowed node basis and exchange currents",
        },
        {
            "theorem_id": "OMC2616_1_connected_graph_implication",
            "claim_piece": "connected ordinary matter source",
            "mathematical_form": "G_ord connected => T_active=w_star T_total",
            "status": "DERIVED_CONDITIONAL_THEOREM",
            "derivation_result": "all relative block weights collapse to one common calibration factor",
            "remaining_gap": "connectivity of tested ordinary matter must be parent/source certified",
        },
        {
            "theorem_id": "OMC2616_2_lab_matter_graph",
            "claim_piece": "baryonic laboratory matter connectivity",
            "mathematical_form": "electron -- EM/binding -- proton/nucleus -- nuclear binding -- neutron; atoms/molecules/lattices inherit the same total Hilbert source",
            "status": "STANDARD_MATTER_CONNECTIVITY_CONTRACT",
            "derivation_result": "ordinary atomic test bodies appear connected once interaction/binding stress is included",
            "remaining_gap": "needs source-backed component graph certificate before a public WEP/local-GR claim",
        },
        {
            "theorem_id": "OMC2616_3_decoupled_sector_clause",
            "claim_piece": "decoupled conserved sectors are not ordinary test-body matter unless arena-included",
            "mathematical_form": "T_total=T_ord+T_D with no exchange edge leaves delta_w_decoupled only if T_D is present in the tested source arena",
            "status": "ARENA_EXCLUSION_CONTRACT_NEEDED",
            "derivation_result": "decoupled sectors are no longer loose species weights; they are explicit arena inventory items",
            "remaining_gap": "source inventory must say whether any decoupled block contributes to each local test",
        },
        {
            "theorem_id": "OMC2616_4_current_verdict",
            "claim_piece": "delta_w_block for ordinary test bodies",
            "mathematical_form": "delta_w_block^ordinary=0 if G_ord is connected and source owner is total Hilbert current",
            "status": "CONDITIONAL_ORDINARY_BLOCK_ZERO_PARENT_UNSIGNED",
            "derivation_result": "residual narrowed to source-shadow/projector leakage or truly decoupled block leakage",
            "remaining_gap": "source-shadow ban plus source-backed graph certificate remain unsigned",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def graph_certificate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "graph_id": "SMG2616_0_node_basis",
            "claim_piece": "ordinary source nodes",
            "graph_row": "nodes={leptonic charged matter, baryonic/nuclear matter, EM field/binding, nuclear binding, molecular/lattice binding}",
            "status": "CANDIDATE_NODE_BASIS",
            "claim_status": "PRIVATE_CONTRACT_ONLY",
            "remaining_gap": "source-backed node basis and arena-specific inclusion/exclusion rules",
        },
        {
            "graph_id": "SMG2616_1_electron_nucleus_edge",
            "claim_piece": "charged matter connected by EM/binding stress",
            "graph_row": "C_e^nu + C_EM/bind^nu + C_nucleus^nu=0 in bound atoms",
            "status": "STANDARD_MATTER_EDGE_CONTRACT",
            "claim_status": "PRIVATE_CONTRACT_ONLY",
            "remaining_gap": "source citation/component convention for EM and binding stress",
        },
        {
            "graph_id": "SMG2616_2_proton_neutron_edge",
            "claim_piece": "nuclear components connected by nuclear binding stress",
            "graph_row": "C_p^nu + C_n^nu + C_nuclear_bind^nu=0 inside nuclei",
            "status": "STANDARD_MATTER_EDGE_CONTRACT",
            "claim_status": "PRIVATE_CONTRACT_ONLY",
            "remaining_gap": "source citation/component convention for nuclear binding stress",
        },
        {
            "graph_id": "SMG2616_3_macroscopic_body_edge",
            "claim_piece": "atoms, molecules and solids inherit connected source through binding/lattice stress",
            "graph_row": "T_body=T_rest+T_EM_bind+T_nuclear_bind+T_lattice+... as one Hilbert source",
            "status": "STANDARD_MATTER_EDGE_CONTRACT",
            "claim_status": "PRIVATE_CONTRACT_ONLY",
            "remaining_gap": "arena-specific material model and binding-energy projection",
        },
        {
            "graph_id": "SMG2616_4_decoupled_inventory",
            "claim_piece": "decoupled sector inventory",
            "graph_row": "T_D excluded from ordinary test body unless source inventory explicitly includes it",
            "status": "ARENA_INVENTORY_REQUIRED",
            "claim_status": "PRIVATE_CONTRACT_ONLY",
            "remaining_gap": "test-by-test source inventory for dark/hidden/nonordinary blocks",
        },
        {
            "graph_id": "SMG2616_5_certificate_verdict",
            "claim_piece": "ordinary lab matter exchange graph",
            "graph_row": "candidate graph connected for atomic/nuclear test bodies, excluding decoupled non-test-body sectors",
            "status": "GRAPH_CERTIFICATE_READY_FOR_SOURCING_NOT_CLAIM",
            "claim_status": "PRIVATE_HIGH_LEVEL_ONLY",
            "remaining_gap": "source-backed graph rows, citations, and local-arena projection table",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def source_shadow_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "shadow_id": "SSB2616_0_target",
            "claim_piece": "no source-shadow functional",
            "mathematical_form": "not exists S_source[Psi,e_obs,w_i] separate from S_matter used only in gravitational field equation",
            "status": "TARGET_EXACT",
            "derivation_result": "would remove the cleanest bypass around exchange connectivity",
            "remaining_gap": "parent object language has not yet signed the single-source-owner grammar",
        },
        {
            "shadow_id": "SSB2616_1_variational_owner_filter",
            "claim_piece": "same variational action owns dynamics and source",
            "mathematical_form": "E_Psi=delta S_matter/delta Psi and T=delta S_matter/delta e_obs",
            "status": "CONDITIONAL_OBJECT_LANGUAGE_THEOREM",
            "derivation_result": "a source-shadow weight is not an allowed coordinate if source equals total Hilbert derivative by definition",
            "remaining_gap": "grammar theorem only after the parent action forbids alternate source maps",
        },
        {
            "shadow_id": "SSB2616_2_conservation_filter",
            "claim_piece": "source-shadow current must be conserved or real",
            "mathematical_form": "nabla_mu(E^{mu nu})=0 implies nabla_mu(T_shadow^{mu nu})=0; otherwise field equation is inconsistent",
            "status": "DERIVED_FILTER",
            "derivation_result": "an uncoupled shadow source either violates Bianchi or behaves as a real independently conserved source block",
            "remaining_gap": "real conserved shadow blocks still need exclusion or bound",
        },
        {
            "shadow_id": "SSB2616_3_no_hidden_source_map",
            "claim_piece": "no post-variation material projector",
            "mathematical_form": "T_active != P_material(delta S_matter/delta e_obs) unless P_material=identity",
            "status": "CONTRACT_NEEDED",
            "derivation_result": "post-variation material projectors can reintroduce composition dependence after the connected graph theorem",
            "remaining_gap": "hidden source-map/projector ban remains unsigned",
        },
        {
            "shadow_id": "SSB2616_4_no_nonHilbert_label_current",
            "claim_piece": "no label-carrying non-Hilbert ordinary source current",
            "mathematical_form": "J_src=J_Hilbert and J_NH,label=0, or J_NH,label is explicit residual",
            "status": "CONTRACT_NEEDED",
            "derivation_result": "prevents source labels returning outside total Hilbert exchange graph",
            "remaining_gap": "non-Hilbert current silence remains a parallel gate",
        },
        {
            "shadow_id": "SSB2616_5_current_verdict",
            "claim_piece": "source-shadow ban for current MTS parent",
            "mathematical_form": "T_active=delta S_matter/delta e_obs and no other ordinary source map",
            "status": "CONTRACT_READY_PARENT_UNSIGNED",
            "derivation_result": "source-shadow route is sharply isolated but not eliminated",
            "remaining_gap": "needs 2617 single-action/source-map grammar closure or finite shadow bound",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def countermodel_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "countermodel_id": "CM2616_0_decoupled_conserved_block",
            "countermodel": "ordinary plus decoupled conserved sector",
            "mathematical_form": "T_active=w_ord T_ord + w_D T_D, with nabla T_ord=nabla T_D=0",
            "survives_current_constraints": True,
            "why_survives": "Bianchi permits different weights for truly disconnected conserved blocks",
            "needed_to_kill": "arena proof that T_D is absent from test source or finite bound on w_D-w_ord",
        },
        {
            "countermodel_id": "CM2616_1_source_shadow",
            "countermodel": "source-shadow functional or source map",
            "mathematical_form": "T_active=delta S_matter/delta e_obs + delta_w_shadow T_shadow",
            "survives_current_constraints": True,
            "why_survives": "single-source-owner is not parent-signed",
            "needed_to_kill": "typed parent grammar forbids non-Hilbert/source-shadow ordinary currents",
        },
        {
            "countermodel_id": "CM2616_2_hidden_projector",
            "countermodel": "post-variation material projector",
            "mathematical_form": "T_active=P_A(T_total) with material-dependent P_A",
            "survives_current_constraints": True,
            "why_survives": "connectivity before variation does not ban post-variation readout/source filters",
            "needed_to_kill": "identity-only source map theorem",
        },
        {
            "countermodel_id": "CM2616_3_unsourced_graph",
            "countermodel": "incorrect ordinary graph omits binding or interaction stress",
            "mathematical_form": "T_body split into separately weighted pseudo-components without T_bind",
            "survives_current_constraints": True,
            "why_survives": "a bad component basis can fake disconnected blocks",
            "needed_to_kill": "source-backed Hilbert-current component graph including binding stress",
        },
        {
            "countermodel_id": "CM2616_4_nonHilbert_label_current",
            "countermodel": "label-carrying non-Hilbert current bypasses graph",
            "mathematical_form": "T_active=T_Hilbert + J_NH[label]",
            "survives_current_constraints": True,
            "why_survives": "ordinary graph theorem only controls Hilbert exchange components",
            "needed_to_kill": "non-Hilbert current silence theorem or explicit residual bound",
        },
        {
            "countermodel_id": "CM2616_5_verdict",
            "countermodel": "ordinary block zero remains conditional",
            "mathematical_form": "delta_w_ord=0 conditional; delta_w_shadow/delta_w_decoupled retained",
            "survives_current_constraints": True,
            "why_survives": "2616 narrows the problem but does not sign source-shadow or source-backed graph rows",
            "needed_to_kill": "2617 source-shadow/source-map closure plus graph sourcing",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def residual_interface_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "RBI2616_0_delta_w_ord",
            "quantity": "delta_w_ordinary_connected_block",
            "meaning": "relative ordinary-matter source weight after exchange connectivity",
            "mathematical_form": "delta_w_ord=0 if G_ord connected and T_active=T_Hilbert",
            "units": "dimensionless",
            "status": "CONDITIONAL_ZERO_PARENT_UNSIGNED",
        },
        {
            "row_id": "RBI2616_1_delta_w_shadow",
            "quantity": "delta_w_shadow",
            "meaning": "source-shadow/non-Hilbert/projector leakage after Hilbert variation",
            "mathematical_form": "T_active=T_Hilbert + delta_w_shadow T_shadow",
            "units": "dimensionless",
            "status": "MISSING_SOURCE_SHADOW_BAN_OR_BOUND",
        },
        {
            "row_id": "RBI2616_2_delta_w_decoupled",
            "quantity": "delta_w_decoupled",
            "meaning": "independent weight for decoupled conserved sectors absent from ordinary test bodies",
            "mathematical_form": "T_active=w_ord T_ord + w_D T_D",
            "units": "dimensionless",
            "status": "MISSING_ARENA_EXCLUSION_OR_BOUND",
        },
        {
            "row_id": "RBI2616_3_graph_sources",
            "quantity": "source-backed graph rows",
            "meaning": "citations and component definitions for ordinary exchange edges",
            "mathematical_form": "node, edge, exchange_current, included_binding_term, source_path",
            "units": "table",
            "status": "MISSING_SOURCE_BACKED_GRAPH_CERTIFICATE",
        },
        {
            "row_id": "RBI2616_4_R_source_shadow",
            "quantity": "R_source_shadow",
            "meaning": "shadow/projector/decoupled contribution to ordinary active-source residual",
            "mathematical_form": "||R_source,shadow||_{E*} <= U_B A_shadow + U_B K_dec ||delta_w_decoupled||",
            "units": "E*_dual_or_declared_arena_units",
            "status": "MISSING_SHADOW_AND_DECOUPLED_OPERATOR_NORMS",
        },
        {
            "row_id": "RBI2616_5_nonclaim_lock",
            "quantity": "local-GR/WEP/R10 claim status",
            "meaning": "ordinary block theorem is not yet a public/local pass",
            "mathematical_form": "claim_allowed=false until graph/source-shadow gates are signed",
            "units": "status",
            "status": "NONCLAIM_LOCK",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def source_zero_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "status_id": "SZ2616_0_derivation_gain",
            "quantity": "ordinary source block",
            "current_status": "CONDITIONALLY_CONNECTED",
            "evidence": "OMC2616_1 and OMC2616_2",
            "remaining_gap": "source-backed graph certificate required",
        },
        {
            "status_id": "SZ2616_1_delta_w_block",
            "quantity": "delta_w_block",
            "current_status": "REFINED_TO_SHADOW_OR_DECOUPLED_RESIDUALS",
            "evidence": "OMC2616_4 and RBI2616 rows",
            "remaining_gap": "delta_w_shadow and delta_w_decoupled need proof or bound",
        },
        {
            "status_id": "SZ2616_2_source_shadow",
            "quantity": "source-shadow route",
            "current_status": "NOT_PARENT_EXCLUDED",
            "evidence": "SSB2616_5",
            "remaining_gap": "single-action/source-map grammar must be signed",
        },
        {
            "status_id": "SZ2616_3_nonHilbert_current",
            "quantity": "label-carrying non-Hilbert ordinary source",
            "current_status": "NOT_SILENCED",
            "evidence": "SSB2616_4 and CM2616_4",
            "remaining_gap": "non-Hilbert current silence theorem or finite residual bound",
        },
        {
            "status_id": "SZ2616_4_local_GR",
            "quantity": "local GR / Newton / WEP / R10 / PPN / clock / orbital branch",
            "current_status": "NOT_CLAIMABLE",
            "evidence": "claim gates keep source-shadow and graph sourcing blocked",
            "remaining_gap": "no local pass until graph certificate and single source map are signed or bounded",
        },
        {
            "status_id": "SZ2616_5_next",
            "quantity": "next derivation owner",
            "current_status": "SINGLE_SOURCE_MAP_GRAMMAR_IS_NEXT",
            "evidence": "source-shadow is now the cleanest remaining bypass",
            "remaining_gap": "build 2617 source-shadow/source-map identity theorem or bound",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2616_0_connected_ordinary_graph",
            "claim": "ordinary lab matter exchange graph is connected",
            "gate_pass": False,
            "status": "NONCLAIM_THEOREM_GATE",
            "blocker": "BLOCKED_SOURCE_BACKED_GRAPH_CERTIFICATE_MISSING",
        },
        {
            "gate_id": "GATE2616_1_source_shadow_ban",
            "claim": "no source-shadow/non-Hilbert/projector leakage",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_SINGLE_SOURCE_MAP_GRAMMAR_UNSIGNED",
        },
        {
            "gate_id": "GATE2616_2_delta_w_ord_zero",
            "claim": "delta_w_ordinary_connected_block=0",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_GRAPH_AND_SOURCE_SHADOW_GATES_OPEN",
        },
        {
            "gate_id": "GATE2616_3_delta_w_shadow_bound",
            "claim": "delta_w_shadow finite source-backed bound exists",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_SHADOW_BOUND_OR_ZERO_THEOREM_MISSING",
        },
        {
            "gate_id": "GATE2616_4_delta_w_decoupled_bound",
            "claim": "delta_w_decoupled arena exclusion or bound exists",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_ARENA_SOURCE_INVENTORY_MISSING",
        },
        {
            "gate_id": "GATE2616_5_nonHilbert_current_silence",
            "claim": "label-carrying non-Hilbert ordinary current is absent or bounded",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_NONHILBERT_CURRENT_SILENCE_UNSIGNED",
        },
        {
            "gate_id": "GATE2616_6_local_GR_WEP_R10",
            "claim": "local GR / Newton / WEP / PPN / clock / orbital / R10 source branch passes",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_SOURCE_SHADOW_AND_GRAPH_SOURCING_OPEN",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2616_0_connectivity_gain",
            "decision": "ORDINARY_GRAPH_CONNECTIVITY_CONDITIONALLY_CLOSES_DELTA_W_BLOCK",
            "reason": "connected exchange graph turns all ordinary weights into one common calibration",
            "next_action": "source the graph before any claim",
        },
        {
            "decision_id": "DEC2616_1_residual_refinement",
            "decision": "DELTA_W_BLOCK_REFINED_TO_SHADOW_OR_DECOUPLED",
            "reason": "ordinary connected matter no longer needs species/block weights except via source-shadow or genuinely decoupled sectors",
            "next_action": "track delta_w_shadow and delta_w_decoupled explicitly",
        },
        {
            "decision_id": "DEC2616_2_no_claim",
            "decision": "NO_LOCAL_SOURCE_CLAIM",
            "reason": "source-backed graph certificate and source-shadow ban are not parent-signed",
            "next_action": "keep all local/empirical claim gates closed",
        },
        {
            "decision_id": "DEC2616_3_best_next",
            "decision": "SINGLE_SOURCE_MAP_GRAMMAR_AND_SHADOW_BAN_IS_NEXT",
            "reason": "source-shadow is now the strongest remaining way to bypass the connected ordinary graph theorem",
            "next_action": "build 2617 single-action source-map identity theorem or shadow residual bound",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "next_id": "NEXT2616_0_primary",
            "status": "selected",
            "doc": "2617-Y5-R2FR-single-source-map-grammar-and-source-shadow-ban-or-shadow-bound.md",
            "script": "scripts/Y5_R2FR_single_source_map_grammar_and_source_shadow_ban_or_shadow_bound_2617.py",
            "task": "prove the parent object language admits only the total Hilbert source map and forbids source-shadow/projector currents; otherwise stage delta_w_shadow bound rows",
            "success_condition": "source-shadow/projector route theorem-zero or explicit finite nonclaim residual",
            "guardrail": "no local-GR, Newton, WEP, PPN, clock, orbital or R10 claim from 2616",
        },
        {
            "next_id": "NEXT2616_1_fallback",
            "status": "held_fallback",
            "doc": "2617b-Y5-R2FR-standard-matter-graph-source-certificate-and-arena-inventory.md",
            "script": "scripts/Y5_R2FR_standard_matter_graph_source_certificate_and_arena_inventory_2617b.py",
            "task": "source ordinary matter graph edges and arena exclusion/bound rows for decoupled sectors",
            "success_condition": "source-backed graph certificate and arena inventory ready for future local tests",
            "guardrail": "graph sourcing alone does not close source-shadow/projector branch",
        },
        {
            "next_id": "NEXT2616_2_nonHilbert_queue",
            "status": "queued_parallel",
            "doc": "2617c-Y5-R2FR-nonHilbert-source-current-silence-or-current-bound.md",
            "script": "scripts/Y5_R2FR_nonHilbert_source_current_silence_or_current_bound_2617c.py",
            "task": "exclude or bound label-carrying non-Hilbert ordinary source currents",
            "success_condition": "J_NH,label theorem-zero or finite residual row",
            "guardrail": "do not hide non-Hilbert source debt inside Hilbert graph theorem",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "sources": source_register_rows(),
        "lineage": lineage_rows(),
        "exchange": exchange_connectivity_rows(),
        "graph": graph_certificate_rows(),
        "shadow": source_shadow_rows(),
        "countermodel": countermodel_rows(),
        "residual": residual_interface_rows(),
        "source_zero": source_zero_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }


def copy_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, target in COPY_TARGETS.items():
        source = OUTPUTS[key]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        ok, count, error = csv_parses(target)
        rows.append(
            with_stamp(
                {
                    "copy_id": f"COPY2616_{key}",
                    "source_key": key,
                    "source_path": source,
                    "copy_path": target,
                    "copy_exists": target.exists(),
                    "csv_parse": ok,
                    "row_count": count,
                    "error": error,
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def generated_rows_have_no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    flag_fields = set(FALSE_FLAGS)
    for key, rows in rows_map.items():
        if key == "sources":
            continue
        for row in rows:
            for field in flag_fields:
                if str(row.get(field, "false")).lower() == "true":
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            text = " ".join(row_value(value) for value in row.values())
            if "MISSING_" not in text:
                continue
            if str(row.get("valid_for_claim", "false")).lower() == "true":
                return False
            status = str(row.get("status", row.get("attempt_status", ""))).upper()
            if status in {"READY", "PASS", "VALID_FOR_CLAIM"}:
                return False
    return True


def sources_pass(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return all(row["source_exists"] and row["needles_present"] for row in rows_map["sources"])


def lineage_complete(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    text = " ".join(row_value(value) for row in rows_map["lineage"] for value in row.values())
    return all(token in text for token in ["2615", "1766", "954/955/977"])


def connectivity_theorem_recorded(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("theorem_id") == "OMC2616_1_connected_graph_implication"
        and row.get("status") == "DERIVED_CONDITIONAL_THEOREM"
        for row in rows_map["exchange"]
    )


def graph_certificate_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("graph_id") == "SMG2616_5_certificate_verdict"
        and row.get("status") == "GRAPH_CERTIFICATE_READY_FOR_SOURCING_NOT_CLAIM"
        for row in rows_map["graph"]
    )


def source_shadow_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("shadow_id") == "SSB2616_5_current_verdict"
        and row.get("status") == "CONTRACT_READY_PARENT_UNSIGNED"
        for row in rows_map["shadow"]
    )


def countermodel_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("countermodel_id") == "CM2616_5_verdict"
        and str(row.get("survives_current_constraints", "false")).lower() == "true"
        for row in rows_map["countermodel"]
    )


def residual_interface_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["residual"]
    return any(row.get("row_id") == "RBI2616_1_delta_w_shadow" for row in rows) and all(
        str(row.get("valid_for_claim", "false")).lower() == "false" for row in rows
    )


def ub_power_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("row_id") == "RBI2616_4_R_source_shadow" and "U_B" in row.get("mathematical_form", "")
        for row in rows_map["residual"]
    )


def source_zero_blocked(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("status_id") == "SZ2616_4_local_GR" and row.get("current_status") == "NOT_CLAIMABLE"
        for row in rows_map["source_zero"]
    )


def claim_gates_safe(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return all(str(row.get("gate_pass", "false")).lower() == "false" for row in rows_map["claim_gates"])


def decision_next(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("decision_id") == "DEC2616_3_best_next"
        and "SINGLE_SOURCE_MAP_GRAMMAR" in row.get("decision", "")
        for row in rows_map["decisions"]
    )


def next_selected(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("next_id") == "NEXT2616_0_primary"
        and row.get("status") == "selected"
        and "single-source-map" in row.get("doc", "")
        for row in rows_map["next"]
    )


def no_formalization_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*2616*"))


def pycache_absent() -> bool:
    return not (ROOT / "scripts" / "__pycache__").exists()


def validation_rows(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = [
        ("VAL2616_00_sources_exist", sources_pass(rows_map), "all cited source paths exist and needles are present"),
        ("VAL2616_01_lineage_complete", lineage_complete(rows_map), "lineage covers 2615 current gate plus 1766 and 954/955/977 prior inputs"),
        ("VAL2616_02_connectivity_theorem", connectivity_theorem_recorded(rows_map), "connected graph implication recorded"),
        ("VAL2616_03_graph_certificate_nonclaim", graph_certificate_nonclaim(rows_map), "graph certificate staged as nonclaim"),
        ("VAL2616_04_source_shadow_retained", source_shadow_retained(rows_map), "source-shadow ban remains parent-unsigned"),
        ("VAL2616_05_countermodel_retained", countermodel_retained(rows_map), "shadow/decoupled countermodel remains retained"),
        ("VAL2616_06_residual_interface_nonclaim", residual_interface_nonclaim(rows_map), "residual interface rows remain nonclaim"),
        ("VAL2616_07_U_B_power_retained", ub_power_retained(rows_map), "explicit U_B source-shadow residual factor retained"),
        ("VAL2616_08_source_zero_blocked", source_zero_blocked(rows_map), "local source status remains blocked"),
        ("VAL2616_09_claim_gates_safe", claim_gates_safe(rows_map), "all claim gates remain blocked/nonclaim"),
        ("VAL2616_10_no_claim_flags", generated_rows_have_no_claim_flags(rows_map), "claim/no-score flags stay false"),
        ("VAL2616_11_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        ("VAL2616_12_formalization_untouched", no_formalization_artifacts(), "no 2616 outputs found under formalization-workbench"),
        ("VAL2616_13_decision_next", decision_next(rows_map), "decision selects single-source-map/source-shadow route"),
        ("VAL2616_14_next_selected", next_selected(rows_map), "next target selected"),
        (
            "VAL2616_15_branch_copies",
            all(row["copy_exists"] and row["csv_parse"] for row in rows_map["branch_copies"]),
            "nonclaim branch copies exist and parse",
        ),
        ("VAL2616_16_pycache_absent", pycache_absent(), "scripts __pycache__ absent"),
    ]

    rows: list[dict[str, Any]] = []
    for check_id, passed, detail in checks:
        rows.append(
            with_stamp(
                {
                    "check_id": check_id,
                    "status": "PASS" if passed else "FAIL",
                    "notes": detail,
                    "detail": "",
                    "valid_for_claim": False,
                }
            )
        )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, error = csv_parses(path)
        rows.append(
            with_stamp(
                {
                    "check_id": f"VAL2616_CSV_{path.stem}",
                    "status": "PASS" if ok else "FAIL",
                    "notes": f"CSV parses with {count} rows" if ok else "CSV parse failed",
                    "detail": error,
                    "valid_for_claim": False,
                }
            )
        )

    for key, path in COPY_TARGETS.items():
        ok, count, error = csv_parses(path)
        rows.append(
            with_stamp(
                {
                    "check_id": f"VAL2616_COPY_CSV_{key}",
                    "status": "PASS" if ok else "FAIL",
                    "notes": f"copy CSV parses with {count} rows" if ok else "copy CSV parse failed",
                    "detail": error,
                    "valid_for_claim": False,
                }
            )
        )

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        with_stamp(
            {
                "check_id": "VAL2616_OVERALL",
                "status": "PASS" if overall else "FAIL",
                "notes": "2616 ordinary exchange graph conditionally closes block residual and selects source-shadow grammar proof next",
                "detail": "",
                "valid_for_claim": False,
            }
        )
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(row_value(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validations: list[dict[str, Any]]) -> str:
    return "\n\n".join(
        [
            "# 2616 Y5 R2FR Ordinary Matter Exchange Graph Connectivity And Source-Shadow Ban Or Delta-W Block Bound",
            "## Summary\n"
            "- This checkpoint sharpens the 2615 block law: if the ordinary-matter exchange graph is connected, ordinary source weights collapse to one common calibration factor.\n"
            "- Atomic/nuclear laboratory matter has a plausible connected graph through EM, nuclear, binding, molecular and lattice stresses once those stresses are included in the total Hilbert source.\n"
            "- This is still not a claim because the graph certificate is not source-backed and the parent object language has not banned source-shadow/projector/non-Hilbert source maps.\n"
            "- The live residual is refined again: broad `delta_w_block` becomes `delta_w_shadow` plus arena-specific `delta_w_decoupled`.\n"
            "- Next target: single-source-map grammar and source-shadow ban.",
            "## Source Register\n" + markdown_table(rows_map["sources"], ["source_id", "source_key", "source_path", "source_exists", "needles_present"]),
            "## Lineage Ledger\n" + markdown_table(rows_map["lineage"], ["lineage_id", "input_checkpoint", "imported_result", "2616_use"]),
            "## Ordinary Matter Exchange Connectivity Theorem\n" + markdown_table(rows_map["exchange"], ["theorem_id", "claim_piece", "mathematical_form", "status", "derivation_result", "remaining_gap"]),
            "## Standard Matter Graph Certificate Attempt\n" + markdown_table(rows_map["graph"], ["graph_id", "claim_piece", "graph_row", "status", "claim_status", "remaining_gap"]),
            "## Source-Shadow Ban Attempt\n" + markdown_table(rows_map["shadow"], ["shadow_id", "claim_piece", "mathematical_form", "status", "derivation_result", "remaining_gap"]),
            "## Countermodel Ledger\n" + markdown_table(rows_map["countermodel"], ["countermodel_id", "countermodel", "mathematical_form", "survives_current_constraints", "why_survives", "needed_to_kill"]),
            "## Residual Bound Interface\n" + markdown_table(rows_map["residual"], ["row_id", "quantity", "meaning", "mathematical_form", "units", "status"]),
            "## Source Zero Status\n" + markdown_table(rows_map["source_zero"], ["status_id", "quantity", "current_status", "evidence", "remaining_gap"]),
            "## Claim Gates\n" + markdown_table(rows_map["claim_gates"], ["gate_id", "claim", "gate_pass", "status", "blocker"]),
            "## Decision Ledger\n" + markdown_table(rows_map["decisions"], ["decision_id", "decision", "reason", "next_action"]),
            "## Next Target\n" + markdown_table(rows_map["next"], ["next_id", "status", "doc", "script", "task", "success_condition", "guardrail"]),
            "## Branch Copies\n" + markdown_table(rows_map["branch_copies"], ["copy_id", "source_key", "copy_path", "copy_exists", "csv_parse", "row_count"]),
            "## Validation\n" + markdown_table(validations, ["check_id", "status", "notes", "detail", "valid_for_claim"]),
            "## Working Verdict\n"
            "This is a useful narrowing. The coupling problem is no longer a fog of arbitrary matter-dependent knobs. Ordinary connected matter wants to carry only one Hilbert source normalization. The main remaining enemy is now cleaner: a shadow source map, projector or non-Hilbert current that reintroduces composition after the variational source has already been formed.",
        ]
    ) + "\n"


def main() -> None:
    rows_map = rows_by_key()
    write_csv(OUTPUTS["source_register"], rows_map["sources"])
    write_csv(OUTPUTS["lineage_ledger"], rows_map["lineage"])
    write_csv(OUTPUTS["exchange_connectivity"], rows_map["exchange"])
    write_csv(OUTPUTS["graph_certificate"], rows_map["graph"])
    write_csv(OUTPUTS["source_shadow"], rows_map["shadow"])
    write_csv(OUTPUTS["countermodel"], rows_map["countermodel"])
    write_csv(OUTPUTS["residual_interface"], rows_map["residual"])
    write_csv(OUTPUTS["source_zero"], rows_map["source_zero"])
    write_csv(OUTPUTS["claim_gates"], rows_map["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], rows_map["decisions"])
    write_csv(OUTPUTS["next_target"], rows_map["next"])
    rows_map["branch_copies"] = copy_outputs()
    write_csv(OUTPUTS["branch_copies"], rows_map["branch_copies"])
    validations = validation_rows(rows_map)
    write_csv(OUTPUTS["validation"], validations)
    DOC.write_text(build_markdown(rows_map, validations), encoding="utf-8")
    print(f"wrote {DOC}")
    print(f"validation={OUTPUTS['validation']}")
    print(f"2616 validation {validations[-1]['status']}")


if __name__ == "__main__":
    main()
