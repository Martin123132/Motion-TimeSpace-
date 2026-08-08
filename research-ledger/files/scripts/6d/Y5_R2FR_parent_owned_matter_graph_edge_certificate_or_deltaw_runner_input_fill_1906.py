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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1906"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1906-Y5-R2FR-parent-owned-matter-graph-edge-certificate-or-deltaw-runner-input-fill.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()


INPUTS = {
    "1905_doc": ROOT / "1905-Y5-R2FR-connected-matter-category-action-density-line-or-deltaw-runner.md",
    "1905_validation": OUT / "P8_Y5_BRR545_1905_VALIDATION.csv",
    "1905_connected": OUT / "P8_Y5_PARENT_QLOC_1905_CONNECTED_MATTER_CATEGORY_ATTEMPT.csv",
    "1905_line": OUT / "P8_Y5_PARENT_QLOC_1905_ACTION_DENSITY_LINE_OWNER_GATE.csv",
    "1905_runner": OUT / "P8_Y5_PARENT_QLOC_1905_DELTAW_RUNNER_CONTRACT_NONCLAIM.csv",
    "1905_next": OUT / "P8_Y5_PARENT_QLOC_1905_NEXT_TARGET.csv",
    "1605_graph_certificate": OUT / "P8_Y5_PARENT_QLOC_1605_CONNECTED_MATTER_GRAPH_CERTIFICATE.csv",
    "1606_edge_audit": OUT / "P8_Y5_PARENT_QLOC_1606_PARENT_OWNED_EDGE_AUDIT.csv",
    "1606_graph_theorem": OUT / "P8_Y5_PARENT_QLOC_1606_PARENT_OWNED_GRAPH_THEOREM_ATTEMPT.csv",
    "1232_interaction_certificate": OUT / "P8_Y5_R10_1232_INTERACTION_GRAPH_CERTIFICATE_ATTEMPT.csv",
    "1232_edge_audit": OUT / "P8_Y5_R10_1232_ORDINARY_MATTER_GRAPH_EDGE_AUDIT.csv",
    "1466_edge_update": OUT / "P8_Y5_R10_1466_GRAPH_EDGE_STATUS_UPDATE.csv",
    "1722_action_density_edge": OUT / "P8_Y5_PARENT_QLOC_1722_PARENT_ACTION_DENSITY_EDGE_AUDIT.csv",
    "1766_standard_graph": OUT / "P8_Y5_PARENT_QLOC_1766_STANDARD_MATTER_GRAPH_CERTIFICATE_ATTEMPT.csv",
    "1766_exchange_theorem": OUT / "P8_Y5_PARENT_QLOC_1766_ORDINARY_MATTER_EXCHANGE_CONNECTIVITY_THEOREM.csv",
    "1762_bound_interface": OUT / "P8_Y5_PARENT_QLOC_1762_DELTAW_BOUND_INTERFACE.csv",
    "1763_source_acquisition": OUT / "P8_Y5_PARENT_QLOC_1763_DELTAW_SOURCE_ACQUISITION_LEDGER.csv",
    "1764_species_bound": OUT / "P8_Y5_PARENT_QLOC_1764_DELTAW_SPECIES_BOUND_INTERFACE.csv",
    "1765_block_bound": OUT / "P8_Y5_PARENT_QLOC_1765_DELTAW_BLOCK_BOUND_INPUT.csv",
    "1897_projection_matrix": OUT / "P8_Y5_PARENT_QLOC_1897_DELTAW_ARENA_PROJECTION_MATRIX_NONCLAIM.csv",
    "1897_projection_requirements": OUT / "P8_Y5_PARENT_QLOC_1897_DELTAW_PROJECTION_REQUIREMENTS.csv",
    "1694_variation_identity": OUT / "P8_Y5_PARENT_QLOC_1694_SOURCE_WEIGHT_VARIATION_IDENTITY.csv",
}


SOURCE_NEEDLES = {
    "1905_doc": ["NEXT1905_0_primary", "1906-Y5-R2FR-parent-owned-matter-graph-edge-certificate-or-deltaw-runner-input-fill.md"],
    "1905_validation": ["VAL1905_OVERALL,PASS"],
    "1905_connected": ["CMC1905_5_verdict", "CONNECTED_MATTER_CATEGORY_NOT_PARENT_DERIVED"],
    "1905_line": ["ADL1905_5_verdict", "ACTION_DENSITY_LINE_OWNER_NOT_DERIVED"],
    "1905_runner": ["DWR1905_6_verdict", "DELTAW_RUNNER_CONTRACT_NONCLAIM_NOT_EXECUTABLE"],
    "1905_next": ["NEXT1905_0_primary", "certify ordinary matter graph vertices/edges"],
    "1605_graph_certificate": ["GRC1605_6_verdict", "physical connectedness is not enough"],
    "1606_edge_audit": ["EDGE1606_7_verdict", "NOT_PARENT_CERTIFIED"],
    "1606_graph_theorem": ["POG1606_4_verdict", "PARENT_OWNED_GRAPH_NOT_DERIVED"],
    "1232_interaction_certificate": ["IGC1232_4_verdict", "GRAPH_CERTIFICATE_NOT_CLOSED"],
    "1232_edge_audit": ["EDGE1232_5_measure_readout_all", "UNSIGNED_AND_DATA_PENDING"],
    "1466_edge_update": ["E1465_0_electron_photon", "EXACT_CONDITIONAL_EDGE_THEOREM_NOT_PARENT_SIGNED"],
    "1722_action_density_edge": ["PED1722_4_verdict", "PARENT_EDGE_NOT_DERIVED"],
    "1766_standard_graph": ["SMG1766_4_certificate_verdict", "GRAPH_CERTIFICATE_READY_FOR_SOURCING_NOT_CLAIM"],
    "1766_exchange_theorem": ["OMC1766_4_current_verdict", "CONDITIONAL_ORDINARY_BLOCK_ZERO_PARENT_UNSIGNED"],
    "1762_bound_interface": ["DW1762_1_delta_w_A", "MISSING_COMPONENT_BASIS_OR_THEOREM_ZERO"],
    "1763_source_acquisition": ["DWA1763_0_delta_w_species", "MISSING_HOM_SPECIES_EXCLUSION_OR_NUMERIC_BOUND"],
    "1764_species_bound": ["DWS1764_4_nonclaim_lock", "NONCLAIM_LOCK"],
    "1765_block_bound": ["DWB1765_4_nonclaim_lock", "NONCLAIM_LOCK"],
    "1897_projection_matrix": ["DPM1897_6_no_cancellation_policy", "NO_CANCELLATION_POLICY_ENFORCED_NONCLAIM"],
    "1897_projection_requirements": ["DPR1897_0_parent_zero_or_values", "MISSING_PARENT_DELTAW_VALUES"],
    "1694_variation_identity": ["VAR1694_5_identity_verdict", "source-weight variation identity"],
}


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1906_SOURCE_REGISTER.csv",
    "edge_certificate": OUT / "P8_Y5_PARENT_QLOC_1906_PARENT_OWNED_MATTER_GRAPH_EDGE_CERTIFICATE_ATTEMPT.csv",
    "edge_status": OUT / "P8_Y5_PARENT_QLOC_1906_EDGE_STATUS_MATRIX_NONCLAIM.csv",
    "runner_input_fill": OUT / "P8_Y5_PARENT_QLOC_1906_DELTAW_RUNNER_INPUT_FILL_NONCLAIM.csv",
    "dryrun_cases": OUT / "P8_Y5_PARENT_QLOC_1906_EDGE_DELTW_DRYRUN_CASES.csv",
    "dryrun_results": OUT / "P8_Y5_PARENT_QLOC_1906_EDGE_DELTW_DRYRUN_RESULTS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1906_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1906_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1906_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1906_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1906_VALIDATION.csv",
}


BRANCH_COPIES = {
    "edge_certificate": SOURCE_WEIGHT_DOCS / "PARENT_OWNED_EDGE_CERTIFICATE_1906_NONCLAIM.csv",
    "edge_status": MICROSCOPE_RESIDUALS / OUTPUTS["edge_status"].name,
    "runner_input_fill": QUEUE / "JR1906_DELTAW_RUNNER_INPUT_FILL_NONCLAIM.csv",
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


def edge_certificate_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "EDGE1906_0_target",
            "claim_piece": "parent-owned matter graph edge certificate",
            "formal_statement": "Every source-relevant ordinary matter edge must be a nonzero parent-owned morphism on one action-density/source functor before source extraction.",
            "status": "TARGET_SHARP",
            "proof_or_obstruction": "this is the certificate needed to turn physical interaction connectedness into source-weight universality",
            "source_anchor": "P8_Y5_PARENT_QLOC_1905_NEXT_TARGET.csv:NEXT1905_0_primary; P8_Y5_PARENT_QLOC_1606_PARENT_OWNED_GRAPH_THEOREM_ATTEMPT.csv:POG1606_0_target",
            "conditional_theorem": True,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "EDGE1906_1_exact_edge_lemma",
            "claim_piece": "nonzero edge weight equality",
            "formal_statement": "If e:A->B is parent-owned and F(e) is nonzero on L_action/source, then naturality w_B F(e)=F(e) w_A forces w_A=w_B.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "proof_or_obstruction": "the algebra is clean; the missing item is not the lemma, but parent-owned nonzero edge evidence",
            "source_anchor": "P8_Y5_PARENT_QLOC_1606_PARENT_OWNED_GRAPH_THEOREM_ATTEMPT.csv:POG1606_1_exact_graph_lemma; P8_Y5_PARENT_QLOC_1722_PARENT_ACTION_DENSITY_EDGE_AUDIT.csv:PED1722_0_target",
            "conditional_theorem": True,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "EDGE1906_2_best_edge_electron_photon",
            "claim_piece": "electron-photon edge",
            "formal_statement": "The QED current edge can be written as an exact conditional variational theorem, but it still needs unique EM owner, source-label forgetting, no-hidden-F2, and readout closure.",
            "status": "EXACT_CONDITIONAL_EDGE_THEOREM_NOT_PARENT_SIGNED",
            "proof_or_obstruction": "one strong edge candidate is not enough until its parent owner/readout stack is signed",
            "source_anchor": "P8_Y5_R10_1466_GRAPH_EDGE_STATUS_UPDATE.csv:E1465_0_electron_photon",
            "conditional_theorem": True,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "EDGE1906_3_remaining_edges",
            "claim_piece": "QCD, mass, binding, material, measure/current/readout edges",
            "formal_statement": "Quark-gluon, quark-photon, EM/nuclear, nuclear/material, mass/Yukawa, measure, current, and readout edges are physical templates or partial clauses, not parent-owned edge certificates.",
            "status": "REMAINING_EDGES_TEMPLATE_OR_UNSIGNED",
            "proof_or_obstruction": "the graph remains physically connected but not source-normalization connected in the parent-action sense",
            "source_anchor": "P8_Y5_PARENT_QLOC_1606_PARENT_OWNED_EDGE_AUDIT.csv:EDGE1606_1_EM_nuclear through EDGE1606_7_verdict; P8_Y5_R10_1232_ORDINARY_MATTER_GRAPH_EDGE_AUDIT.csv:EDGE1232_1_quark_photon through EDGE1232_5_measure_readout_all",
            "conditional_theorem": False,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "EDGE1906_4_standard_matter_exchange_route",
            "claim_piece": "ordinary lab matter exchange graph",
            "formal_statement": "For atomic/nuclear lab matter, connected exchange currents would collapse block weights to one common calibration if source-backed graph rows and arena projection are supplied.",
            "status": "PROMISING_CONDITIONAL_SOURCE_BACKED_ROUTE_NOT_CLAIM",
            "proof_or_obstruction": "1766 narrows the problem to lab-matter exchange graph sourcing, but source citations/component conventions/projections are missing",
            "source_anchor": "P8_Y5_PARENT_QLOC_1766_ORDINARY_MATTER_EXCHANGE_CONNECTIVITY_THEOREM.csv:OMC1766_4_current_verdict; P8_Y5_PARENT_QLOC_1766_STANDARD_MATTER_GRAPH_CERTIFICATE_ATTEMPT.csv:SMG1766_4_certificate_verdict",
            "conditional_theorem": True,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "EDGE1906_5_verdict",
            "claim_piece": "promote parent-owned graph edge certificate",
            "formal_statement": "Current MTS corpus certifies all source-relevant ordinary matter graph edges as parent-owned nonzero action-density/source morphisms.",
            "status": "PARENT_OWNED_MATTER_GRAPH_EDGE_CERTIFICATE_NOT_DERIVED",
            "proof_or_obstruction": "edge equality theorem is exact and lab-matter exchange route is promising, but current edges remain template-only/conditional/source-backed-needed",
            "source_anchor": "EDGE1906_0_target through EDGE1906_4_standard_matter_exchange_route",
            "conditional_theorem": True,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def edge_status_rows() -> list[dict[str, Any]]:
    return [
        {"edge_id": "ES1906_0_electron_photon", "edge": "electron/leptonic -> photon/EM", "best_status": "EXACT_CONDITIONAL_EDGE_THEOREM_NOT_PARENT_SIGNED", "missing_for_claim": "unique EM owner, no-hidden-F2, source-label forgetting, readout/radiative closure", "source_anchor": "P8_Y5_R10_1466_GRAPH_EDGE_STATUS_UPDATE.csv:E1465_0_electron_photon", "counts_for_connected_graph": False, "valid_for_claim": False},
        {"edge_id": "ES1906_1_quark_gluon", "edge": "light quark -> gluon/QCD", "best_status": "PHYSICAL_TEMPLATE_NOT_PARENT_CERTIFICATE", "missing_for_claim": "strong-sector parent action owner and nonzero source morphism", "source_anchor": "P8_Y5_PARENT_QLOC_1606_PARENT_OWNED_EDGE_AUDIT.csv:EDGE1606_2_quark_QCD", "counts_for_connected_graph": False, "valid_for_claim": False},
        {"edge_id": "ES1906_2_mass_yukawa", "edge": "fermion -> mass/Yukawa/source", "best_status": "PHYSICAL_TEMPLATE_NOT_PARENT_CERTIFICATE", "missing_for_claim": "mass edge mapped to MTS parent action-density line", "source_anchor": "P8_Y5_PARENT_QLOC_1605_CONNECTED_MATTER_GRAPH_CERTIFICATE.csv:GRC1605_3_Yukawa_edge; P8_Y5_PARENT_QLOC_1606_PARENT_OWNED_EDGE_AUDIT.csv:EDGE1606_3_quark_mass", "counts_for_connected_graph": False, "valid_for_claim": False},
        {"edge_id": "ES1906_3_binding_material", "edge": "QCD/EM/nuclear -> atom/material", "best_status": "STANDARD_MATTER_EDGE_CONTRACT_PRIVATE_ONLY", "missing_for_claim": "source-backed component graph, binding fractions, isotope/alloy projection, material tensor", "source_anchor": "P8_Y5_PARENT_QLOC_1766_STANDARD_MATTER_GRAPH_CERTIFICATE_ATTEMPT.csv:SMG1766_1_electron_nucleus_edge;SMG1766_3_macroscopic_body_edge", "counts_for_connected_graph": False, "valid_for_claim": False},
        {"edge_id": "ES1906_4_measure_current", "edge": "all matter sectors -> measure/current owner", "best_status": "UNSIGNED_PARENT_CLAUSE", "missing_for_claim": "species-blind measure/current owner; no J_A/hbar_A source reentry", "source_anchor": "P8_Y5_PARENT_QLOC_1606_PARENT_OWNED_EDGE_AUDIT.csv:EDGE1606_5_measure;EDGE1606_6_current", "counts_for_connected_graph": False, "valid_for_claim": False},
        {"edge_id": "ES1906_5_readout", "edge": "source/current -> readout/worldtube", "best_status": "UNSIGNED_AND_DATA_PENDING", "missing_for_claim": "readout no-reentry, source-worldtube map, official arrays/kernels", "source_anchor": "P8_Y5_R10_1232_ORDINARY_MATTER_GRAPH_EDGE_AUDIT.csv:EDGE1232_5_measure_readout_all", "counts_for_connected_graph": False, "valid_for_claim": False},
        {"edge_id": "ES1906_6_verdict", "edge": "full graph", "best_status": "NO_EDGE_COUNTS_FOR_CLAIM_GRADE_CONNECTED_GRAPH", "missing_for_claim": "at least a source-backed lab-matter exchange graph certificate or parent-owned edge theorem", "source_anchor": "P8_Y5_R10_1327_PARENT_GRAPH_CERTIFICATE_AUDIT.csv:GRAPH1327_1_edge_rollup; P8_Y5_PARENT_QLOC_1606_PARENT_OWNED_EDGE_AUDIT.csv:EDGE1606_7_verdict", "counts_for_connected_graph": False, "valid_for_claim": False},
    ]


def runner_input_fill_rows() -> list[dict[str, Any]]:
    return [
        {"fill_id": "DWI1906_0_parent_zero_or_values", "object": "Delta_w component values/theorem-zero", "current_status": "MISSING_PARENT_DELTAW_VALUES", "missing_for_claim": "each component has parent numeric value, uncertainty/bound, or theorem-zero proof", "source_anchor": "P8_Y5_PARENT_QLOC_1897_DELTAW_PROJECTION_REQUIREMENTS.csv:DPR1897_0_parent_zero_or_values; P8_Y5_PARENT_QLOC_1762_DELTAW_BOUND_INTERFACE.csv:DW1762_1_delta_w_A", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"fill_id": "DWI1906_1_component_basis", "object": "ordinary component/block basis", "current_status": "MISSING_COMPONENT_BASIS", "missing_for_claim": "source-backed node/block basis or parent-derived smaller basis", "source_anchor": "P8_Y5_PARENT_QLOC_1764_DELTAW_SPECIES_BOUND_INTERFACE.csv:DWS1764_1_component_basis; P8_Y5_PARENT_QLOC_1765_DELTAW_BLOCK_BOUND_INPUT.csv:DWB1765_1_exchange_graph", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"fill_id": "DWI1906_2_source_graph", "object": "ordinary matter source/exchange graph", "current_status": "MISSING_SOURCE_GRAPH", "missing_for_claim": "source-backed graph rows for atomic/nuclear lab matter and decoupled-sector exclusions", "source_anchor": "P8_Y5_PARENT_QLOC_1766_STANDARD_MATTER_GRAPH_CERTIFICATE_ATTEMPT.csv:SMG1766_4_certificate_verdict; P8_Y5_PARENT_QLOC_1765_DELTAW_BLOCK_BOUND_INPUT.csv:DWB1765_1_exchange_graph", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"fill_id": "DWI1906_3_arena_projection", "object": "composition/material/readout projection", "current_status": "MISSING_ARENA_PROJECTION_KERNELS", "missing_for_claim": "WEP/R10/PPN/clock/orbital kernels, material fractions, binding fractions, source-worldtube convention", "source_anchor": "P8_Y5_PARENT_QLOC_1897_DELTAW_ARENA_PROJECTION_MATRIX_NONCLAIM.csv:DPM1897_1_WEP_MICROSCOPE through DPM1897_5_orbital", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"fill_id": "DWI1906_4_bound_table", "object": "finite empirical Delta_w bounds", "current_status": "MISSING_SOURCE_BACKED_BOUND_TABLE", "missing_for_claim": "source-backed bound table with projection convention for species/block weights", "source_anchor": "P8_Y5_PARENT_QLOC_1764_DELTAW_SPECIES_BOUND_INTERFACE.csv:DWS1764_3_bound_source; P8_Y5_PARENT_QLOC_1765_DELTAW_BLOCK_BOUND_INPUT.csv:DWB1765_3_bound_table", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"fill_id": "DWI1906_5_no_cancellation", "object": "no-cancellation/covariance policy", "current_status": "POLICY_WRITTEN_NONCLAIM", "missing_for_claim": "sourced covariance envelope or parent identity for signed cancellation", "source_anchor": "P8_Y5_PARENT_QLOC_1897_DELTAW_ARENA_PROJECTION_MATRIX_NONCLAIM.csv:DPM1897_6_no_cancellation_policy", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"fill_id": "DWI1906_6_verdict", "object": "Delta_w runner input fill", "current_status": "DELTAW_RUNNER_INPUTS_NOT_EXECUTABLE_NONCLAIM", "missing_for_claim": "DWI1906_0 through DWI1906_5 filled or theorem-zero", "source_anchor": "DWI1906_0_parent_zero_or_values through DWI1906_5_no_cancellation", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    return [
        {"case_id": "DRY1906_0_physical_template", "uses_physical_edge_as_parent_edge": True, "electron_photon_only": False, "standard_graph_sourced": False, "parent_values": False, "arena_kernels": False, "uses_eom_division": False, "expected_status": "REFUSED_PHYSICAL_EDGE_NOT_PARENT_CERTIFICATE", "valid_for_claim": False},
        {"case_id": "DRY1906_1_electron_edge_only", "uses_physical_edge_as_parent_edge": False, "electron_photon_only": True, "standard_graph_sourced": False, "parent_values": False, "arena_kernels": False, "uses_eom_division": False, "expected_status": "REFUSED_SINGLE_EDGE_CONDITIONAL_NOT_GRAPH", "valid_for_claim": False},
        {"case_id": "DRY1906_2_standard_graph_unsourced", "uses_physical_edge_as_parent_edge": False, "electron_photon_only": False, "standard_graph_sourced": False, "parent_values": False, "arena_kernels": False, "uses_eom_division": False, "expected_status": "REFUSED_PARENT_EDGE_CERTIFICATE_NOT_DERIVED", "valid_for_claim": False},
        {"case_id": "DRY1906_3_parent_values_missing", "uses_physical_edge_as_parent_edge": False, "electron_photon_only": False, "standard_graph_sourced": True, "parent_values": False, "arena_kernels": False, "uses_eom_division": False, "expected_status": "REFUSED_PARENT_DELTAW_VALUES_MISSING", "valid_for_claim": False},
        {"case_id": "DRY1906_4_kernels_missing", "uses_physical_edge_as_parent_edge": False, "electron_photon_only": False, "standard_graph_sourced": True, "parent_values": True, "arena_kernels": False, "uses_eom_division": False, "expected_status": "REFUSED_ARENA_KERNELS_MISSING", "valid_for_claim": False},
        {"case_id": "DRY1906_5_eom_division", "uses_physical_edge_as_parent_edge": False, "electron_photon_only": False, "standard_graph_sourced": False, "parent_values": False, "arena_kernels": False, "uses_eom_division": True, "expected_status": "REFUSED_EOM_DIVISION_FALSE_POSITIVE", "valid_for_claim": False},
    ]


def validate_dryrun_case(row: dict[str, Any]) -> dict[str, Any]:
    if bool_string(row["uses_eom_division"]) == "true":
        status = "REFUSED_EOM_DIVISION_FALSE_POSITIVE"
    elif bool_string(row["uses_physical_edge_as_parent_edge"]) == "true":
        status = "REFUSED_PHYSICAL_EDGE_NOT_PARENT_CERTIFICATE"
    elif bool_string(row["electron_photon_only"]) == "true":
        status = "REFUSED_SINGLE_EDGE_CONDITIONAL_NOT_GRAPH"
    elif bool_string(row["standard_graph_sourced"]) != "true":
        status = "REFUSED_PARENT_EDGE_CERTIFICATE_NOT_DERIVED"
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
        {"gate_id": "CG1906_0_edge", "condition": "parent-owned nonzero matter graph edge certificate exists", "current_status": "FAIL_PARENT_OWNED_MATTER_GRAPH_EDGE_CERTIFICATE_NOT_DERIVED", "source_anchor": "P8_Y5_PARENT_QLOC_1906_PARENT_OWNED_MATTER_GRAPH_EDGE_CERTIFICATE_ATTEMPT.csv:EDGE1906_5_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1906_1_graph", "condition": "enough edges count for connected source/action graph", "current_status": "FAIL_NO_EDGE_COUNTS_FOR_CLAIM_GRADE_CONNECTED_GRAPH", "source_anchor": "P8_Y5_PARENT_QLOC_1906_EDGE_STATUS_MATRIX_NONCLAIM.csv:ES1906_6_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1906_2_runner", "condition": "Delta_w runner has parent values and arena kernels if graph theorem fails", "current_status": "FAIL_DELTAW_RUNNER_INPUTS_NOT_EXECUTABLE_NONCLAIM", "source_anchor": "P8_Y5_PARENT_QLOC_1906_DELTAW_RUNNER_INPUT_FILL_NONCLAIM.csv:DWI1906_6_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1906_3_verdict", "condition": "1906 supports local-GR source universality or claim-grade Delta_w score", "current_status": "CLAIM_BLOCKED", "source_anchor": "CG1906_0_edge through CG1906_2_runner", "gate_pass": False, "valid_for_claim": False},
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {"decision_id": "DEC1906_0_edge", "decision": "do not promote parent-owned edge theorem", "reason": "edge lemma is exact and electron-photon is strongest candidate, but no full parent-owned graph certificate exists", "status": "EDGE_ROUTE_SHARP_BUT_UNSIGNED", "next_dependency": "source-backed ordinary lab matter exchange graph or parent edge theorem", "valid_for_claim": False},
        {"decision_id": "DEC1906_1_standard_matter", "decision": "promote standard-matter exchange graph to next sourcing target", "reason": "1766 narrows the local test arena to atomic/nuclear lab matter where exchange graph connectivity is physically plausible", "status": "SOURCE_BACKED_GRAPH_ROUTE_SELECTED", "next_dependency": "citations, component conventions, binding/material projection rows", "valid_for_claim": False},
        {"decision_id": "DEC1906_2_runner", "decision": "keep Delta_w runner nonclaim", "reason": "parent Delta_w values, component basis, arena kernels, and source-backed bound tables remain missing", "status": "RUNNER_INPUT_FILL_STAGED_NONCLAIM", "next_dependency": "fill DWI1906_0 through DWI1906_5", "valid_for_claim": False},
        {"decision_id": "DEC1906_3_next", "decision": "attack source-backed standard-matter exchange graph next", "reason": "this route is less post-hoc than fitting Delta_w and may collapse ordinary lab-matter source weights before testing", "status": "NEXT_TARGET_SELECTED", "next_dependency": "1907 standard-matter exchange graph source-backed certificate or Delta_w input acquisition", "valid_for_claim": False},
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1906_0_primary",
            "selection_status": "selected",
            "target_doc": "1907-Y5-R2FR-standard-matter-exchange-graph-source-backed-certificate-or-deltaw-input-acquisition.md",
            "target_script": "scripts/Y5_R2FR_standard_matter_exchange_graph_source_backed_certificate_or_deltaw_input_acquisition_1907.py",
            "objective": "source-back the ordinary lab-matter exchange graph for electrons, nuclei, binding, and materials; if not claim-grade, emit Delta_w input acquisition rows",
            "success_condition": "source-backed graph certificate for tested ordinary matter, or explicit Delta_w component/projection/bound acquisition ledger",
            "do_not": "do not count physical template edges as parent-owned proof, do not use EOM division, and do not claim local-GR/WEP pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {"status_id": "STAT1906_0_theory", "area": "parent graph edges", "summary": "the graph theorem is exact but the parent-owned edge certificate is not derived", "risk_level": "EDGE_CERTIFICATE_MISSING", "project_meaning": "the local-GR source route still has a clear mathematical target", "next_action": "source-back or parent-sign ordinary lab-matter exchange edges", "valid_for_claim": False},
        {"status_id": "STAT1906_1_promising", "area": "standard lab matter", "summary": "atomic/nuclear lab matter exchange connectivity may collapse block weights if sourced and projected correctly", "risk_level": "PROMISING_SOURCE_BACKED_ROUTE", "project_meaning": "we have a practical non-galaxy way to discipline the coupling branch", "next_action": "build source-backed graph/component/projection table", "valid_for_claim": False},
        {"status_id": "STAT1906_2_runner", "area": "Delta_w runner", "summary": "runner remains non-executable until parent values, component basis, graph/source inventory, arena kernels, and bound tables exist", "risk_level": "RUNNER_INPUTS_MISSING", "project_meaning": "if derivation stalls, the finite-residual test route remains explicit rather than hidden", "next_action": "fill input acquisition ledger", "valid_for_claim": False},
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    cases = dryrun_case_rows()
    return {
        "source_register": source_register_rows(),
        "edge_certificate": edge_certificate_rows(),
        "edge_status": edge_status_rows(),
        "runner_input_fill": runner_input_fill_rows(),
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
    fields = {"valid_for_claim", "claim_allowed", "valid_prediction_row", "score_ready", "gate_pass", "parent_signed", "counts_for_connected_graph"}
    bad: list[str] = []
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            for field in fields.intersection(row.keys()):
                if bool_string(row[field]) == "true":
                    bad.append(f"{path.name}:{index}:{field}=true")
    return not bad, "; ".join(bad) if bad else "all generated claim/scoring/signature flags remain false"


def blocked_rows_not_ready(paths: list[Path]) -> tuple[bool, str]:
    markers = ["MISSING", "UNSIGNED", "NOT_DERIVED", "NOT_PARENT", "BLOCKED", "FAIL", "COUNTER", "NONCLAIM", "NOT_EXECUTABLE", "REFUSED"]
    fields = {"valid_for_claim", "claim_allowed", "valid_prediction_row", "score_ready", "gate_pass", "parent_signed", "counts_for_connected_graph"}
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


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks: list[dict[str, Any]] = []
    source_rows_loaded = csv_rows(OUTPUTS["source_register"])
    checks.append({"validation_id": "VAL1906_00_sources", "status": "PASS" if all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows_loaded) else "FAIL", "detail": "all local source paths exist and needles found", "valid_for_claim": False})
    edge_rows = csv_rows(OUTPUTS["edge_certificate"])
    checks.append({"validation_id": "VAL1906_01_edge_verdict", "status": "PASS" if any(row["attempt_id"] == "EDGE1906_5_verdict" and row["status"] == "PARENT_OWNED_MATTER_GRAPH_EDGE_CERTIFICATE_NOT_DERIVED" for row in edge_rows) else "FAIL", "detail": "parent-owned edge certificate remains unsigned", "valid_for_claim": False})
    status_rows = csv_rows(OUTPUTS["edge_status"])
    checks.append({"validation_id": "VAL1906_02_edge_status", "status": "PASS" if any(row["edge_id"] == "ES1906_6_verdict" and row["best_status"] == "NO_EDGE_COUNTS_FOR_CLAIM_GRADE_CONNECTED_GRAPH" for row in status_rows) and all(bool_string(row["counts_for_connected_graph"]) == "false" for row in status_rows) else "FAIL", "detail": "no edge counts for claim-grade connected graph", "valid_for_claim": False})
    input_rows = csv_rows(OUTPUTS["runner_input_fill"])
    checks.append({"validation_id": "VAL1906_03_runner_inputs", "status": "PASS" if any(row["fill_id"] == "DWI1906_6_verdict" and row["current_status"] == "DELTAW_RUNNER_INPUTS_NOT_EXECUTABLE_NONCLAIM" for row in input_rows) and all(bool_string(row["valid_prediction_row"]) == "false" for row in input_rows) else "FAIL", "detail": "Delta_w runner inputs remain nonclaim/not executable", "valid_for_claim": False})
    dry_rows = csv_rows(OUTPUTS["dryrun_results"])
    checks.append({"validation_id": "VAL1906_04_dryrun", "status": "PASS" if all(bool_string(row["status_match"]) == "true" and bool_string(row["claim_allowed"]) == "false" for row in dry_rows) else "FAIL", "detail": "dry-run refuses physical-edge proof, single-edge shortcut, missing inputs, and EOM division", "valid_for_claim": False})
    gate_rows = csv_rows(OUTPUTS["claim_gate"])
    checks.append({"validation_id": "VAL1906_05_claim_gate", "status": "PASS" if any(row["gate_id"] == "CG1906_3_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in gate_rows) else "FAIL", "detail": "claim remains blocked", "valid_for_claim": False})
    next_rows = csv_rows(OUTPUTS["next_target"])
    checks.append({"validation_id": "VAL1906_06_next_target", "status": "PASS" if any(row["route_id"] == "NEXT1906_0_primary" and row["selection_status"] == "selected" for row in next_rows) else "FAIL", "detail": "1907 target selected", "valid_for_claim": False})
    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append({"validation_id": "VAL1906_07_claim_flags_false", "status": "PASS" if flags_ok else "FAIL", "detail": flags_detail, "valid_for_claim": False})
    blocked_ok, blocked_detail = blocked_rows_not_ready(generated_without_validation)
    checks.append({"validation_id": "VAL1906_08_blocked_markers_not_ready", "status": "PASS" if blocked_ok else "FAIL", "detail": blocked_detail, "valid_for_claim": False})
    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append({"validation_id": "VAL1906_09_csv_parse", "status": "PASS" if parse_ok else "FAIL", "detail": parse_detail, "valid_for_claim": False})
    checks.append({"validation_id": "VAL1906_10_branch_copies", "status": "PASS" if all(path.exists() for path in BRANCH_COPIES.values()) else "FAIL", "detail": "; ".join(str(path) for path in BRANCH_COPIES.values()), "valid_for_claim": False})
    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append({"validation_id": "VAL1906_11_pycache_absent", "status": "PASS" if not pycache.exists() else "FAIL", "detail": str(pycache), "valid_for_claim": False})
    formalization_hits = []
    if FORMALIZATION.exists():
        artifact_needles = [
            "1906-Y5-R2FR-parent-owned-matter-graph-edge",
            "P8_Y5_PARENT_QLOC_1906",
            "Y5_R2FR_parent_owned_matter_graph_edge_certificate_or_deltaw_runner_input_fill_1906",
        ]
        formalization_hits = [
            path
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and any(needle in path.name for needle in artifact_needles)
        ]
    checks.append({"validation_id": "VAL1906_12_formalization_untouched", "status": "PASS" if not formalization_hits else "FAIL", "detail": f"formalization_1906_artifact_count={len(formalization_hits)}", "valid_for_claim": False})
    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append({"validation_id": "VAL1906_OVERALL", "status": "PASS" if fail_count == 0 else "FAIL", "detail": "1906 parent-owned matter graph edge certificate or Delta_w runner input fill", "valid_for_claim": False})
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1906 - Parent-Owned Matter Graph Edge Certificate Or Delta_w Runner Input Fill

## Purpose

This checkpoint tests whether the ordinary matter graph edges can be promoted from physical interaction templates to parent-owned nonzero action-density/source morphisms. If not, it fills the missing `Delta_w` runner inputs as a nonclaim acquisition ledger.

## Result

- The edge/naturality theorem is exact conditionally: a connected parent-owned graph would collapse source weights to one common calibration mode.
- The best individual edge, electron-photon, is only an exact conditional theorem; it is not yet parent-signed.
- The full graph remains template-only or source-backed-needed; no edge counts for a claim-grade connected graph.
- The most promising next path is the source-backed standard-matter exchange graph for atomic/nuclear lab matter.
- The `Delta_w` runner still lacks parent values/theorem-zero rows, component basis, source graph, arena kernels, and bound tables.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Parent-Owned Edge Certificate Attempt

{markdown_table(rows_by_name["edge_certificate"])}

## Edge Status Matrix

{markdown_table(rows_by_name["edge_status"])}

## Delta_w Runner Input Fill

{markdown_table(rows_by_name["runner_input_fill"])}

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
