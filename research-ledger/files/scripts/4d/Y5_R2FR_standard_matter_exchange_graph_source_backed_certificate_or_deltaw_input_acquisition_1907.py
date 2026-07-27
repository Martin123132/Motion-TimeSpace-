from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1907"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1907-Y5-R2FR-standard-matter-exchange-graph-source-backed-certificate-or-deltaw-input-acquisition.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()


INPUTS = {
    "1906_doc": ROOT / "1906-Y5-R2FR-parent-owned-matter-graph-edge-certificate-or-deltaw-runner-input-fill.md",
    "1906_validation": OUT / "P8_Y5_BRR545_1906_VALIDATION.csv",
    "1906_edge_certificate": OUT / "P8_Y5_PARENT_QLOC_1906_PARENT_OWNED_MATTER_GRAPH_EDGE_CERTIFICATE_ATTEMPT.csv",
    "1906_edge_status": OUT / "P8_Y5_PARENT_QLOC_1906_EDGE_STATUS_MATRIX_NONCLAIM.csv",
    "1906_runner_fill": OUT / "P8_Y5_PARENT_QLOC_1906_DELTAW_RUNNER_INPUT_FILL_NONCLAIM.csv",
    "1906_next": OUT / "P8_Y5_PARENT_QLOC_1906_NEXT_TARGET.csv",
    "1766_standard_graph": OUT / "P8_Y5_PARENT_QLOC_1766_STANDARD_MATTER_GRAPH_CERTIFICATE_ATTEMPT.csv",
    "1766_exchange_theorem": OUT / "P8_Y5_PARENT_QLOC_1766_ORDINARY_MATTER_EXCHANGE_CONNECTIVITY_THEOREM.csv",
    "1765_exchange_collapse": OUT / "P8_Y5_PARENT_QLOC_1765_NOETHER_EXCHANGE_COLLAPSE_THEOREM.csv",
    "1765_block_bound": OUT / "P8_Y5_PARENT_QLOC_1765_DELTAW_BLOCK_BOUND_INPUT.csv",
    "1764_species_bound": OUT / "P8_Y5_PARENT_QLOC_1764_DELTAW_SPECIES_BOUND_INTERFACE.csv",
    "1763_source_acquisition": OUT / "P8_Y5_PARENT_QLOC_1763_DELTAW_SOURCE_ACQUISITION_LEDGER.csv",
    "1762_bound_interface": OUT / "P8_Y5_PARENT_QLOC_1762_DELTAW_BOUND_INTERFACE.csv",
    "1897_projection_matrix": OUT / "P8_Y5_PARENT_QLOC_1897_DELTAW_ARENA_PROJECTION_MATRIX_NONCLAIM.csv",
    "1897_projection_requirements": OUT / "P8_Y5_PARENT_QLOC_1897_DELTAW_PROJECTION_REQUIREMENTS.csv",
    "1899_wep_input_pack": OUT / "P8_Y5_PARENT_QLOC_1899_WEP_INPUT_PACK_NONCLAIM.csv",
    "1900_official_data": OUT / "P8_Y5_PARENT_QLOC_1900_OFFICIAL_READOUT_DATA_TARGETS_NONCLAIM.csv",
    "1694_variation_identity": OUT / "P8_Y5_PARENT_QLOC_1694_SOURCE_WEIGHT_VARIATION_IDENTITY.csv",
}


SOURCE_NEEDLES = {
    "1906_doc": ["NEXT1906_0_primary", "1907-Y5-R2FR-standard-matter-exchange-graph-source-backed-certificate-or-deltaw-input-acquisition.md"],
    "1906_validation": ["VAL1906_OVERALL,PASS"],
    "1906_edge_certificate": ["EDGE1906_5_verdict", "PARENT_OWNED_MATTER_GRAPH_EDGE_CERTIFICATE_NOT_DERIVED"],
    "1906_edge_status": ["ES1906_6_verdict", "NO_EDGE_COUNTS_FOR_CLAIM_GRADE_CONNECTED_GRAPH"],
    "1906_runner_fill": ["DWI1906_6_verdict", "DELTAW_RUNNER_INPUTS_NOT_EXECUTABLE_NONCLAIM"],
    "1906_next": ["NEXT1906_0_primary", "source-back the ordinary lab-matter exchange graph"],
    "1766_standard_graph": ["SMG1766_4_certificate_verdict", "GRAPH_CERTIFICATE_READY_FOR_SOURCING_NOT_CLAIM"],
    "1766_exchange_theorem": ["OMC1766_4_current_verdict", "CONDITIONAL_ORDINARY_BLOCK_ZERO_PARENT_UNSIGNED"],
    "1765_exchange_collapse": ["NEC1765_5_current_verdict", "PARTIAL_DERIVATION_PARENT_UNSIGNED"],
    "1765_block_bound": ["DWB1765_4_nonclaim_lock", "NONCLAIM_LOCK"],
    "1764_species_bound": ["DWS1764_4_nonclaim_lock", "NONCLAIM_LOCK"],
    "1763_source_acquisition": ["DWA1763_0_delta_w_species", "MISSING_HOM_SPECIES_EXCLUSION_OR_NUMERIC_BOUND"],
    "1762_bound_interface": ["DW1762_1_delta_w_A", "MISSING_COMPONENT_BASIS_OR_THEOREM_ZERO"],
    "1897_projection_matrix": ["DPM1897_6_no_cancellation_policy", "NO_CANCELLATION_POLICY_ENFORCED_NONCLAIM"],
    "1897_projection_requirements": ["DPR1897_1_arena_tau_K", "MISSING_ARENA_PROJECTION_KERNELS"],
    "1899_wep_input_pack": ["WIP1899_8_verdict", "WEP_INPUT_PACK_NOT_EXECUTABLE_NONCLAIM"],
    "1900_official_data": ["OFFICIAL_DATA_TARGET_NOT_ACQUIRED_NONCLAIM", "METADATA_ONLY_NOT_OFFICIAL_ARRAYS"],
    "1694_variation_identity": ["VAR1694_5_identity_verdict", "source-weight variation identity"],
}


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1907_SOURCE_REGISTER.csv",
    "web_source_ledger": OUT / "P8_Y5_PARENT_QLOC_1907_WEB_SOURCE_LEDGER_NONCLAIM.csv",
    "exchange_graph": OUT / "P8_Y5_PARENT_QLOC_1907_STANDARD_MATTER_EXCHANGE_GRAPH_SOURCE_BACKED_ATTEMPT.csv",
    "graph_rows": OUT / "P8_Y5_PARENT_QLOC_1907_LAB_MATTER_GRAPH_ROW_STATUS_NONCLAIM.csv",
    "deltaw_acquisition": OUT / "P8_Y5_PARENT_QLOC_1907_DELTAW_INPUT_ACQUISITION_LEDGER_NONCLAIM.csv",
    "dryrun_cases": OUT / "P8_Y5_PARENT_QLOC_1907_GRAPH_DELTW_DRYRUN_CASES.csv",
    "dryrun_results": OUT / "P8_Y5_PARENT_QLOC_1907_GRAPH_DELTW_DRYRUN_RESULTS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1907_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1907_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1907_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1907_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1907_VALIDATION.csv",
}


BRANCH_COPIES = {
    "exchange_graph": SOURCE_WEIGHT_DOCS / "STANDARD_MATTER_EXCHANGE_GRAPH_1907_NONCLAIM.csv",
    "graph_rows": MICROSCOPE_RESIDUALS / OUTPUTS["graph_rows"].name,
    "deltaw_acquisition": QUEUE / "JR1907_DELTAW_INPUT_ACQUISITION_LEDGER_NONCLAIM.csv",
    "dryrun_results": QUARANTINE / OUTPUTS["dryrun_results"].name,
}


def ensure_dirs() -> None:
    for path in [OUT, MICROSCOPE_RESIDUALS, QUEUE, SOURCE_WEIGHT_DOCS, QUARANTINE]:
        path.mkdir(parents=True, exist_ok=True)


def bool_string(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value).strip().lower()


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path in INPUTS.items():
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        missing = [needle for needle in SOURCE_NEEDLES[source_id] if needle not in text]
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle_count": len(SOURCE_NEEDLES[source_id]),
                "missing_needles": "; ".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "SOURCE_OR_NEEDLE_MISSING",
                "valid_for_claim": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def web_source_rows() -> list[dict[str, Any]]:
    return [
        {"source_id": "WEB1907_0_PDG_RPP", "source_url": "https://pdg.lbl.gov/", "role": "authoritative particle-physics review index for Standard Model sectors and material/nuclear reference tables", "extraction_needed": "specific review/table URLs and component conventions, not just homepage citation", "current_status": "SOURCE_CANDIDATE_RECORDED_NOT_EXTRACTED", "usable_for_claim": False, "valid_for_claim": False},
        {"source_id": "WEB1907_1_PDG_QCD", "source_url": "https://arxiv.org/abs/2312.14015", "role": "QCD/strong-sector review source candidate for quark-gluon and nuclear-binding graph edges", "extraction_needed": "source-backed edge statement and mapping to action-density/source morphism", "current_status": "SOURCE_CANDIDATE_RECORDED_NOT_EXTRACTED", "usable_for_claim": False, "valid_for_claim": False},
        {"source_id": "WEB1907_2_NIST_ISOTOPES", "source_url": "https://www.nist.gov/pml/atomic-weights-and-isotopic-compositions-relative-atomic-masses", "role": "isotopic masses/compositions source candidate for Ti/Pt component rows", "extraction_needed": "Ti/Pt alloy/isotope/material fractions and binding convention", "current_status": "SOURCE_CANDIDATE_RECORDED_NOT_EXTRACTED", "usable_for_claim": False, "valid_for_claim": False},
        {"source_id": "WEB1907_3_NIST_COMPOSITIONS_TABLE", "source_url": "https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl", "role": "machine-readable-ish isotope composition table candidate", "extraction_needed": "bounded table extraction for Ti/Pt isotopic source components", "current_status": "SOURCE_CANDIDATE_RECORDED_NOT_EXTRACTED", "usable_for_claim": False, "valid_for_claim": False},
        {"source_id": "WEB1907_4_MICROSCOPE_FINAL", "source_url": "https://arxiv.org/abs/2209.15487", "role": "WEP bound and Ti/Pt experiment context", "extraction_needed": "material/test-mass conventions, official readout arrays, and projection kernel", "current_status": "BOUND_ANCHOR_KNOWN_NOT_GRAPH_PROJECTION", "usable_for_claim": False, "valid_for_claim": False},
        {"source_id": "WEB1907_5_MICROSCOPE_PRL", "source_url": "https://link.aps.org/doi/10.1103/PhysRevLett.129.121102", "role": "published MICROSCOPE final result DOI", "extraction_needed": "projection/readout data, not just result citation", "current_status": "SOURCE_CANDIDATE_RECORDED_NOT_EXTRACTED", "usable_for_claim": False, "valid_for_claim": False},
    ]


def exchange_graph_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "SMG1907_0_target",
            "claim_piece": "source-backed standard-matter exchange graph",
            "formal_statement": "Build a source-backed graph for tested atomic/nuclear lab matter whose nodes are Hilbert-source subcurrents and whose edges are nonzero exchange/binding currents.",
            "status": "TARGET_SHARP",
            "proof_or_obstruction": "this is weaker than a full parent-edge theorem but stronger than an unsourced physical template",
            "source_anchor": "P8_Y5_PARENT_QLOC_1906_NEXT_TARGET.csv:NEXT1906_0_primary; P8_Y5_PARENT_QLOC_1766_STANDARD_MATTER_GRAPH_CERTIFICATE_ATTEMPT.csv:SMG1766_4_certificate_verdict",
            "source_candidate": "WEB1907_0_PDG_RPP; WEB1907_1_PDG_QCD; WEB1907_2_NIST_ISOTOPES",
            "source_backed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "SMG1907_1_exchange_theorem",
            "claim_piece": "connected exchange graph collapse",
            "formal_statement": "If ordinary tested matter is one connected exchange component, then T_active=w_star T_total and relative block weights vanish modulo common calibration.",
            "status": "DERIVED_CONDITIONAL_THEOREM",
            "proof_or_obstruction": "1765/1766 already derive the block-collapse law; the missing part is source-backed graph connectivity and source-shadow exclusion",
            "source_anchor": "P8_Y5_PARENT_QLOC_1765_NOETHER_EXCHANGE_COLLAPSE_THEOREM.csv:NEC1765_2_weight_collapse; P8_Y5_PARENT_QLOC_1766_ORDINARY_MATTER_EXCHANGE_CONNECTIVITY_THEOREM.csv:OMC1766_1_connected_graph_implication",
            "source_candidate": "local theorem rows",
            "source_backed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "SMG1907_2_electron_nucleus_binding",
            "claim_piece": "electron/EM/nucleus exchange edge",
            "formal_statement": "Atomic matter should connect electron rest/current, EM binding stress, and nuclear source stress through nonzero exchange/binding terms.",
            "status": "SOURCE_CANDIDATE_RECORDED_NOT_GRAPH_ROW",
            "proof_or_obstruction": "PDG/NIST candidates are recorded, but no extracted component row yet defines the edge and source convention",
            "source_anchor": "P8_Y5_PARENT_QLOC_1766_STANDARD_MATTER_GRAPH_CERTIFICATE_ATTEMPT.csv:SMG1766_1_electron_nucleus_edge",
            "source_candidate": "WEB1907_0_PDG_RPP; WEB1907_2_NIST_ISOTOPES",
            "source_backed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "SMG1907_3_nuclear_binding",
            "claim_piece": "proton/neutron/nuclear binding edge",
            "formal_statement": "Nuclear components should connect through nuclear binding/exchange stress inside nuclei.",
            "status": "SOURCE_CANDIDATE_RECORDED_NOT_GRAPH_ROW",
            "proof_or_obstruction": "QCD/nuclear source candidates are recorded, but no extracted nuclear-binding component convention is attached",
            "source_anchor": "P8_Y5_PARENT_QLOC_1766_STANDARD_MATTER_GRAPH_CERTIFICATE_ATTEMPT.csv:SMG1766_2_proton_neutron_edge",
            "source_candidate": "WEB1907_1_PDG_QCD; WEB1907_0_PDG_RPP",
            "source_backed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "SMG1907_4_material_inheritance",
            "claim_piece": "atoms/materials inherit connected source",
            "formal_statement": "Macroscopic Ti/Pt test bodies inherit source graph connectivity through atoms, molecules, lattice, alloy, and binding stresses only after material fractions/projections are sourced.",
            "status": "MATERIAL_PROJECTION_NOT_SOURCED",
            "proof_or_obstruction": "MICROSCOPE/NIST rows do not yet provide full alloy, isotope, binding, and readout projection tensors",
            "source_anchor": "P8_Y5_PARENT_QLOC_1766_STANDARD_MATTER_GRAPH_CERTIFICATE_ATTEMPT.csv:SMG1766_3_macroscopic_body_edge; P8_Y5_PARENT_QLOC_1899_WEP_INPUT_PACK_NONCLAIM.csv:WIP1899_3_material_tensor",
            "source_candidate": "WEB1907_2_NIST_ISOTOPES; WEB1907_4_MICROSCOPE_FINAL; WEB1907_5_MICROSCOPE_PRL",
            "source_backed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "SMG1907_5_decoupled_sector_limit",
            "claim_piece": "arena-specific decoupled sector exclusion",
            "formal_statement": "Any sector not connected to tested ordinary lab matter must be excluded from the local WEP source inventory or retained as an independent block weight.",
            "status": "EXACT_LIMIT_ARENA_INVENTORY_MISSING",
            "proof_or_obstruction": "the decoupled-sector theorem is exact, but the tested-source inventory is not complete",
            "source_anchor": "P8_Y5_PARENT_QLOC_1766_ORDINARY_MATTER_EXCHANGE_CONNECTIVITY_THEOREM.csv:OMC1766_3_decoupled_sector_limit",
            "source_candidate": "local theorem rows plus future source inventory",
            "source_backed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "SMG1907_6_verdict",
            "claim_piece": "promote source-backed exchange graph certificate",
            "formal_statement": "Current source candidates prove tested ordinary lab matter is one connected exchange source graph, so Delta_w_block^ordinary=0.",
            "status": "SOURCE_BACKED_EXCHANGE_GRAPH_NOT_CLAIM_GRADE",
            "proof_or_obstruction": "source URLs are recorded and the theorem route is sharp, but graph rows, component conventions, material projections, source-shadow exclusion, and arena kernels are not extracted",
            "source_anchor": "SMG1907_0_target through SMG1907_5_decoupled_sector_limit",
            "source_candidate": "WEB1907_0 through WEB1907_5",
            "source_backed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def graph_row_status_rows() -> list[dict[str, Any]]:
    return [
        {"row_id": "GR1907_0_nodes", "needed_row": "node/component basis for tested ordinary matter", "current_status": "MISSING_SOURCE_BACKED_NODE_BASIS", "required_source": "PDG/NIST/MICROSCOPE extracted component inventory for Ti/Pt ordinary matter", "blocks_claim": True, "source_backed": False, "valid_for_claim": False},
        {"row_id": "GR1907_1_edges", "needed_row": "nonzero exchange/binding edge list", "current_status": "MISSING_SOURCE_BACKED_EDGE_ROWS", "required_source": "extracted atomic/nuclear/binding stress/exchange rows with conventions", "blocks_claim": True, "source_backed": False, "valid_for_claim": False},
        {"row_id": "GR1907_2_component_convention", "needed_row": "rest mass, EM binding, nuclear binding, lattice/alloy convention", "current_status": "MISSING_COMPONENT_CONVENTION", "required_source": "material model and binding-energy decomposition convention", "blocks_claim": True, "source_backed": False, "valid_for_claim": False},
        {"row_id": "GR1907_3_TiPt_projection", "needed_row": "Ti/Pt material/source projection", "current_status": "MISSING_MATERIAL_PROJECTION", "required_source": "test-mass alloy/isotope/material fractions and source projection tensor", "blocks_claim": True, "source_backed": False, "valid_for_claim": False},
        {"row_id": "GR1907_4_readout_kernel", "needed_row": "MICROSCOPE readout/source-worldtube kernel", "current_status": "OFFICIAL_ARRAYS_NOT_IMPORTED", "required_source": "official CMSM arrays or validated equivalent", "blocks_claim": True, "source_backed": False, "valid_for_claim": False},
        {"row_id": "GR1907_5_source_shadow", "needed_row": "source-shadow/decoupled sector exclusion", "current_status": "MISSING_SOURCE_SHADOW_EXCLUSION", "required_source": "parent theorem or arena inventory excluding independent source blocks", "blocks_claim": True, "source_backed": False, "valid_for_claim": False},
        {"row_id": "GR1907_6_verdict", "needed_row": "source-backed graph certificate", "current_status": "GRAPH_ROWS_NOT_CLAIM_GRADE", "required_source": "GR1907_0 through GR1907_5 pass", "blocks_claim": True, "source_backed": False, "valid_for_claim": False},
    ]


def deltaw_acquisition_rows() -> list[dict[str, Any]]:
    return [
        {"acq_id": "DWA1907_0_delta_w_species", "quantity": "delta_w_species", "needed_input": "no labelled-source-domain theorem or numeric bound on species-labelled source prefactor", "current_status": "MISSING_HOM_SPECIES_EXCLUSION_OR_NUMERIC_BOUND", "source_anchor": "P8_Y5_PARENT_QLOC_1763_DELTAW_SOURCE_ACQUISITION_LEDGER.csv:DWA1763_0_delta_w_species", "priority": 1, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False},
        {"acq_id": "DWA1907_1_delta_w_block", "quantity": "delta_w_block", "needed_input": "connected ordinary exchange graph proof or finite block-weight bound", "current_status": "MISSING_EXCHANGE_CONNECTIVITY_OR_NUMERIC_BOUND", "source_anchor": "P8_Y5_PARENT_QLOC_1765_DELTAW_BLOCK_BOUND_INPUT.csv:DWB1765_0_delta_w_block", "priority": 2, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False},
        {"acq_id": "DWA1907_2_component_basis", "quantity": "component basis", "needed_input": "electron/proton/neutron/EM-binding/nuclear-binding/material or parent-reduced basis", "current_status": "MISSING_COMPONENT_BASIS", "source_anchor": "P8_Y5_PARENT_QLOC_1764_DELTAW_SPECIES_BOUND_INTERFACE.csv:DWS1764_1_component_basis", "priority": 3, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False},
        {"acq_id": "DWA1907_3_arena_projection", "quantity": "arena projection", "needed_input": "WEP/R10/PPN/clock/orbit projection from component weights to observables", "current_status": "MISSING_ARENA_PROJECTION", "source_anchor": "P8_Y5_PARENT_QLOC_1764_DELTAW_SPECIES_BOUND_INTERFACE.csv:DWS1764_2_test_body_projection; P8_Y5_PARENT_QLOC_1897_DELTAW_PROJECTION_REQUIREMENTS.csv:DPR1897_1_arena_tau_K", "priority": 4, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False},
        {"acq_id": "DWA1907_4_bound_table", "quantity": "source-backed bound table", "needed_input": "finite empirical upper bounds with projection conventions", "current_status": "MISSING_SOURCE_BACKED_BOUND_TABLE", "source_anchor": "P8_Y5_PARENT_QLOC_1764_DELTAW_SPECIES_BOUND_INTERFACE.csv:DWS1764_3_bound_source; P8_Y5_PARENT_QLOC_1765_DELTAW_BLOCK_BOUND_INPUT.csv:DWB1765_3_bound_table", "priority": 5, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False},
        {"acq_id": "DWA1907_5_verdict", "quantity": "Delta_w input acquisition", "needed_input": "DWA1907_0 through DWA1907_4 filled or theorem-zero", "current_status": "DELTAW_INPUT_ACQUISITION_NONCLAIM_NOT_EXECUTABLE", "source_anchor": "DWA1907_0_delta_w_species through DWA1907_4_bound_table", "priority": 6, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False},
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    return [
        {"case_id": "DRY1907_0_url_only", "web_sources_recorded": True, "graph_rows_extracted": False, "component_convention": False, "material_projection": False, "parent_values": False, "arena_kernels": False, "uses_eom_division": False, "expected_status": "REFUSED_URLS_NOT_GRAPH_CERTIFICATE", "valid_for_claim": False},
        {"case_id": "DRY1907_1_graph_no_convention", "web_sources_recorded": True, "graph_rows_extracted": True, "component_convention": False, "material_projection": False, "parent_values": False, "arena_kernels": False, "uses_eom_division": False, "expected_status": "REFUSED_COMPONENT_CONVENTION_MISSING", "valid_for_claim": False},
        {"case_id": "DRY1907_2_projection_missing", "web_sources_recorded": True, "graph_rows_extracted": True, "component_convention": True, "material_projection": False, "parent_values": False, "arena_kernels": False, "uses_eom_division": False, "expected_status": "REFUSED_MATERIAL_PROJECTION_MISSING", "valid_for_claim": False},
        {"case_id": "DRY1907_3_parent_values_missing", "web_sources_recorded": True, "graph_rows_extracted": True, "component_convention": True, "material_projection": True, "parent_values": False, "arena_kernels": False, "uses_eom_division": False, "expected_status": "REFUSED_PARENT_DELTAW_VALUES_MISSING", "valid_for_claim": False},
        {"case_id": "DRY1907_4_kernels_missing", "web_sources_recorded": True, "graph_rows_extracted": True, "component_convention": True, "material_projection": True, "parent_values": True, "arena_kernels": False, "uses_eom_division": False, "expected_status": "REFUSED_ARENA_KERNELS_MISSING", "valid_for_claim": False},
        {"case_id": "DRY1907_5_eom_division", "web_sources_recorded": False, "graph_rows_extracted": False, "component_convention": False, "material_projection": False, "parent_values": False, "arena_kernels": False, "uses_eom_division": True, "expected_status": "REFUSED_EOM_DIVISION_FALSE_POSITIVE", "valid_for_claim": False},
    ]


def validate_dryrun_case(row: dict[str, Any]) -> dict[str, Any]:
    if bool_string(row["uses_eom_division"]) == "true":
        status = "REFUSED_EOM_DIVISION_FALSE_POSITIVE"
    elif bool_string(row["web_sources_recorded"]) != "true" or bool_string(row["graph_rows_extracted"]) != "true":
        status = "REFUSED_URLS_NOT_GRAPH_CERTIFICATE"
    elif bool_string(row["component_convention"]) != "true":
        status = "REFUSED_COMPONENT_CONVENTION_MISSING"
    elif bool_string(row["material_projection"]) != "true":
        status = "REFUSED_MATERIAL_PROJECTION_MISSING"
    elif bool_string(row["parent_values"]) != "true":
        status = "REFUSED_PARENT_DELTAW_VALUES_MISSING"
    elif bool_string(row["arena_kernels"]) != "true":
        status = "REFUSED_ARENA_KERNELS_MISSING"
    else:
        status = "WOULD_REQUIRE_FULL_NUMERIC_NONCLAIM_REVIEW"
    return {
        "case_id": row["case_id"],
        "computed_status": status,
        "expected_status": row["expected_status"],
        "status_match": status == row["expected_status"],
        "claim_allowed": False,
        "valid_for_claim": False,
        "generated_utc": GENERATED_UTC,
    }


def dryrun_result_rows(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [validate_dryrun_case(row) for row in cases]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {"gate_id": "CG1907_0_sources", "condition": "source URLs are extracted into graph rows with component conventions", "current_status": "FAIL_SOURCE_BACKED_EXCHANGE_GRAPH_NOT_CLAIM_GRADE", "source_anchor": "P8_Y5_PARENT_QLOC_1907_STANDARD_MATTER_EXCHANGE_GRAPH_SOURCE_BACKED_ATTEMPT.csv:SMG1907_6_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1907_1_graph_rows", "condition": "all graph row status requirements pass", "current_status": "FAIL_GRAPH_ROWS_NOT_CLAIM_GRADE", "source_anchor": "P8_Y5_PARENT_QLOC_1907_LAB_MATTER_GRAPH_ROW_STATUS_NONCLAIM.csv:GR1907_6_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1907_2_deltaw", "condition": "Delta_w input acquisition is executable if graph route fails", "current_status": "FAIL_DELTAW_INPUT_ACQUISITION_NONCLAIM_NOT_EXECUTABLE", "source_anchor": "P8_Y5_PARENT_QLOC_1907_DELTAW_INPUT_ACQUISITION_LEDGER_NONCLAIM.csv:DWA1907_5_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1907_3_verdict", "condition": "1907 supports local-GR source universality or claim-grade Delta_w score", "current_status": "CLAIM_BLOCKED", "source_anchor": "CG1907_0_sources through CG1907_2_deltaw", "gate_pass": False, "valid_for_claim": False},
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {"decision_id": "DEC1907_0_graph", "decision": "do not promote source-backed exchange graph", "reason": "source candidates are recorded but component conventions, material projection, source-shadow exclusion, and arena kernels are not extracted", "status": "GRAPH_SOURCE_ROUTE_STAGED_NONCLAIM", "next_dependency": "extract graph rows and Ti/Pt projection convention", "valid_for_claim": False},
        {"decision_id": "DEC1907_1_deltaw", "decision": "emit Delta_w acquisition ledger", "reason": "the finite residual route needs species/block values, component basis, projection kernels, and bound table", "status": "DELTAW_ACQUISITION_STAGED_NONCLAIM", "next_dependency": "fill source-backed bound and projection rows", "valid_for_claim": False},
        {"decision_id": "DEC1907_2_next", "decision": "attack graph source extraction next", "reason": "this is still the least post-hoc path: source the ordinary matter graph before fitting finite Delta_w", "status": "NEXT_TARGET_SELECTED", "next_dependency": "1908 graph-source extraction and Ti/Pt component projection", "valid_for_claim": False},
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1907_0_primary",
            "selection_status": "selected",
            "target_doc": "1908-Y5-R2FR-graph-source-extraction-and-TiPt-component-projection.md",
            "target_script": "scripts/Y5_R2FR_graph_source_extraction_and_TiPt_component_projection_1908.py",
            "objective": "extract source-backed graph/component rows for ordinary Ti/Pt lab matter and map them into a projection convention; if still incomplete, preserve Delta_w acquisition blocks",
            "success_condition": "bounded source-backed node/edge/component/projection rows, or explicit blockers for each missing row",
            "do_not": "do not treat URLs as graph proof, do not use EOM division, and do not claim WEP/local-GR pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {"status_id": "STAT1907_0_sources", "area": "standard matter graph", "summary": "authoritative source candidates are recorded, but no extracted graph certificate exists yet", "risk_level": "SOURCE_EXTRACTION_GAP", "project_meaning": "the derivation route is now tied to real source acquisition rather than intuition", "next_action": "extract node/edge/component/projection rows", "valid_for_claim": False},
        {"status_id": "STAT1907_1_theorem", "area": "exchange collapse", "summary": "Bianchi/Noether exchange collapse remains a strong conditional theorem for connected lab matter", "risk_level": "PROMISING_CONDITIONAL_THEOREM", "project_meaning": "this is a serious route to GR-like source universality if graph sourcing closes", "next_action": "source-back ordinary exchange graph and exclude source shadows", "valid_for_claim": False},
        {"status_id": "STAT1907_2_runner", "area": "Delta_w fallback", "summary": "finite residual branch remains honest but not executable", "risk_level": "ACQUISITION_REQUIRED", "project_meaning": "if the derivation route fails, testing needs explicit component/projection/bound inputs", "next_action": "build acquisition tables before scoring", "valid_for_claim": False},
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    cases = dryrun_case_rows()
    return {
        "source_register": source_register_rows(),
        "web_source_ledger": web_source_rows(),
        "exchange_graph": exchange_graph_rows(),
        "graph_rows": graph_row_status_rows(),
        "deltaw_acquisition": deltaw_acquisition_rows(),
        "dryrun_cases": cases,
        "dryrun_results": dryrun_result_rows(cases),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }


def copy_branch_artifacts() -> None:
    for key, target in BRANCH_COPIES.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(OUTPUTS[key], target)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    fields = {"valid_for_claim", "claim_allowed", "valid_prediction_row", "score_ready", "gate_pass", "source_backed", "usable_for_claim"}
    bad: list[str] = []
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            for field in fields.intersection(row.keys()):
                if bool_string(row[field]) == "true":
                    bad.append(f"{path.name}:{index}:{field}=true")
    return not bad, "; ".join(bad) if bad else "all generated claim/scoring/source-backed flags remain false"


def blocked_rows_not_ready(paths: list[Path]) -> tuple[bool, str]:
    markers = ["MISSING", "UNSIGNED", "NOT_DERIVED", "NOT_CLAIM", "BLOCKED", "FAIL", "NONCLAIM", "NOT_EXECUTABLE", "REFUSED", "NOT_EXTRACTED"]
    fields = {"valid_for_claim", "claim_allowed", "valid_prediction_row", "score_ready", "gate_pass", "source_backed", "usable_for_claim"}
    bad: list[str] = []
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            text = " ".join(str(value) for value in row.values())
            if any(marker in text for marker in markers):
                for field in fields.intersection(row.keys()):
                    if bool_string(row[field]) == "true":
                        bad.append(f"{path.name}:{index}:{field}=true despite blocked marker")
    return not bad, "; ".join(bad) if bad else "blocked/unsigned/nonclaim rows are not score-ready"


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    bad: list[str] = []
    for path in paths:
        try:
            rows = csv_rows(path)
            if not rows:
                bad.append(f"{path.name}:empty")
        except Exception as exc:
            bad.append(f"{path.name}:{exc}")
    return not bad, "; ".join(bad) if bad else f"parsed {len(paths)} csv files"


def web_source_check(path: Path) -> tuple[bool, str]:
    bad: list[str] = []
    for index, row in enumerate(csv_rows(path), start=2):
        if not row.get("source_url", "").startswith("https://"):
            bad.append(f"{path.name}:{index}:missing_https_url")
        if bool_string(row.get("usable_for_claim", "")) == "true":
            bad.append(f"{path.name}:{index}:usable_for_claim=true")
    return not bad, "; ".join(bad) if bad else "web source candidates recorded as nonclaim provenance only"


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks: list[dict[str, Any]] = []
    source_rows_loaded = csv_rows(OUTPUTS["source_register"])
    checks.append({"validation_id": "VAL1907_00_sources", "status": "PASS" if all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows_loaded) else "FAIL", "detail": "all local source paths exist and needles found", "valid_for_claim": False})
    web_ok, web_detail = web_source_check(OUTPUTS["web_source_ledger"])
    checks.append({"validation_id": "VAL1907_01_web_sources", "status": "PASS" if web_ok else "FAIL", "detail": web_detail, "valid_for_claim": False})
    graph_rows = csv_rows(OUTPUTS["exchange_graph"])
    checks.append({"validation_id": "VAL1907_02_graph_verdict", "status": "PASS" if any(row["attempt_id"] == "SMG1907_6_verdict" and row["status"] == "SOURCE_BACKED_EXCHANGE_GRAPH_NOT_CLAIM_GRADE" for row in graph_rows) else "FAIL", "detail": "source-backed graph remains not claim-grade", "valid_for_claim": False})
    status_rows = csv_rows(OUTPUTS["graph_rows"])
    checks.append({"validation_id": "VAL1907_03_graph_rows", "status": "PASS" if any(row["row_id"] == "GR1907_6_verdict" and row["current_status"] == "GRAPH_ROWS_NOT_CLAIM_GRADE" for row in status_rows) else "FAIL", "detail": "graph row requirements remain blocked", "valid_for_claim": False})
    acq_rows = csv_rows(OUTPUTS["deltaw_acquisition"])
    checks.append({"validation_id": "VAL1907_04_deltaw_acquisition", "status": "PASS" if any(row["acq_id"] == "DWA1907_5_verdict" and row["current_status"] == "DELTAW_INPUT_ACQUISITION_NONCLAIM_NOT_EXECUTABLE" for row in acq_rows) and all(bool_string(row["valid_prediction_row"]) == "false" for row in acq_rows) else "FAIL", "detail": "Delta_w acquisition remains nonclaim/not executable", "valid_for_claim": False})
    dry_rows = csv_rows(OUTPUTS["dryrun_results"])
    checks.append({"validation_id": "VAL1907_05_dryrun", "status": "PASS" if all(bool_string(row["status_match"]) == "true" and bool_string(row["claim_allowed"]) == "false" for row in dry_rows) else "FAIL", "detail": "dry-run refuses URL-only graph, missing conventions/projections/values/kernels, and EOM shortcut", "valid_for_claim": False})
    gate_rows = csv_rows(OUTPUTS["claim_gate"])
    checks.append({"validation_id": "VAL1907_06_claim_gate", "status": "PASS" if any(row["gate_id"] == "CG1907_3_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in gate_rows) else "FAIL", "detail": "claim remains blocked", "valid_for_claim": False})
    next_rows = csv_rows(OUTPUTS["next_target"])
    checks.append({"validation_id": "VAL1907_07_next_target", "status": "PASS" if any(row["route_id"] == "NEXT1907_0_primary" and row["selection_status"] == "selected" for row in next_rows) else "FAIL", "detail": "1908 target selected", "valid_for_claim": False})
    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append({"validation_id": "VAL1907_08_claim_flags_false", "status": "PASS" if flags_ok else "FAIL", "detail": flags_detail, "valid_for_claim": False})
    blocked_ok, blocked_detail = blocked_rows_not_ready(generated_without_validation)
    checks.append({"validation_id": "VAL1907_09_blocked_markers_not_ready", "status": "PASS" if blocked_ok else "FAIL", "detail": blocked_detail, "valid_for_claim": False})
    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append({"validation_id": "VAL1907_10_csv_parse", "status": "PASS" if parse_ok else "FAIL", "detail": parse_detail, "valid_for_claim": False})
    checks.append({"validation_id": "VAL1907_11_branch_copies", "status": "PASS" if all(path.exists() for path in BRANCH_COPIES.values()) else "FAIL", "detail": "; ".join(str(path) for path in BRANCH_COPIES.values()), "valid_for_claim": False})
    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append({"validation_id": "VAL1907_12_pycache_absent", "status": "PASS" if not pycache.exists() else "FAIL", "detail": str(pycache), "valid_for_claim": False})
    formalization_hits = []
    if FORMALIZATION.exists():
        artifact_needles = [
            "1907-Y5-R2FR-standard-matter-exchange-graph",
            "P8_Y5_PARENT_QLOC_1907",
            "Y5_R2FR_standard_matter_exchange_graph_source_backed_certificate_or_deltaw_input_acquisition_1907",
        ]
        formalization_hits = [
            path
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and any(needle in path.name for needle in artifact_needles)
        ]
    checks.append({"validation_id": "VAL1907_13_formalization_untouched", "status": "PASS" if not formalization_hits else "FAIL", "detail": f"formalization_1907_artifact_count={len(formalization_hits)}", "valid_for_claim": False})
    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append({"validation_id": "VAL1907_OVERALL", "status": "PASS" if fail_count == 0 else "FAIL", "detail": "1907 standard-matter exchange graph source-backed certificate or Delta_w input acquisition", "valid_for_claim": False})
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1907 - Standard-Matter Exchange Graph Source-Backed Certificate Or Delta_w Input Acquisition

## Purpose

This checkpoint records authoritative source candidates for the ordinary lab-matter exchange graph and tests whether that is enough to promote the connected-source theorem. It is not; URLs are provenance, not a graph certificate.

## Result

- The Noether/exchange collapse theorem remains a strong conditional route to GR-like source universality.
- PDG, NIST, and MICROSCOPE source candidates are recorded, but no extracted graph/component/projection table is claim-grade.
- The standard-matter graph route is staged, not promoted.
- The finite `Delta_w` route receives an explicit acquisition ledger for source weights, block weights, component basis, arena projection, and bound tables.
- No local-GR, Newtonian-limit, WEP, or claim-grade residual score is promoted.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Web Source Ledger

{markdown_table(rows_by_name["web_source_ledger"])}

## Standard-Matter Exchange Graph Attempt

{markdown_table(rows_by_name["exchange_graph"])}

## Lab Matter Graph Row Status

{markdown_table(rows_by_name["graph_rows"])}

## Delta_w Input Acquisition

{markdown_table(rows_by_name["deltaw_acquisition"])}

## Dry-Run Cases

{markdown_table(rows_by_name["dryrun_cases"])}

## Dry-Run Results

{markdown_table(rows_by_name["dryrun_results"])}

## Claim Gate

{markdown_table(rows_by_name["claim_gate"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Project Status Snapshot

{markdown_table(rows_by_name["project_status"])}

## Validation

{markdown_table(validation)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows_by_name = build_rows()
    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    remove_pycache()
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()
