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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1908"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1908-Y5-R2FR-graph-source-extraction-and-TiPt-component-projection.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()

NIST_COMPOSITIONS_URL = "https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl"
NIST_INFO_URL = "https://www.nist.gov/pml/atomic-weights-and-isotopic-compositions-relative-atomic-masses"
MICROSCOPE_ARXIV_URL = "https://arxiv.org/abs/2209.15487"
PDG_QCD_URL = "https://arxiv.org/abs/2312.14015"


INPUTS = {
    "1907_doc": ROOT / "1907-Y5-R2FR-standard-matter-exchange-graph-source-backed-certificate-or-deltaw-input-acquisition.md",
    "1907_validation": OUT / "P8_Y5_BRR545_1907_VALIDATION.csv",
    "1907_web": OUT / "P8_Y5_PARENT_QLOC_1907_WEB_SOURCE_LEDGER_NONCLAIM.csv",
    "1907_graph": OUT / "P8_Y5_PARENT_QLOC_1907_STANDARD_MATTER_EXCHANGE_GRAPH_SOURCE_BACKED_ATTEMPT.csv",
    "1907_graph_rows": OUT / "P8_Y5_PARENT_QLOC_1907_LAB_MATTER_GRAPH_ROW_STATUS_NONCLAIM.csv",
    "1907_deltaw": OUT / "P8_Y5_PARENT_QLOC_1907_DELTAW_INPUT_ACQUISITION_LEDGER_NONCLAIM.csv",
    "1907_next": OUT / "P8_Y5_PARENT_QLOC_1907_NEXT_TARGET.csv",
    "1766_standard_graph": OUT / "P8_Y5_PARENT_QLOC_1766_STANDARD_MATTER_GRAPH_CERTIFICATE_ATTEMPT.csv",
    "1766_exchange_theorem": OUT / "P8_Y5_PARENT_QLOC_1766_ORDINARY_MATTER_EXCHANGE_CONNECTIVITY_THEOREM.csv",
    "1765_exchange_collapse": OUT / "P8_Y5_PARENT_QLOC_1765_NOETHER_EXCHANGE_COLLAPSE_THEOREM.csv",
    "1899_wep_input_pack": OUT / "P8_Y5_PARENT_QLOC_1899_WEP_INPUT_PACK_NONCLAIM.csv",
    "1900_official_data": OUT / "P8_Y5_PARENT_QLOC_1900_OFFICIAL_READOUT_DATA_TARGETS_NONCLAIM.csv",
    "1897_projection_matrix": OUT / "P8_Y5_PARENT_QLOC_1897_DELTAW_ARENA_PROJECTION_MATRIX_NONCLAIM.csv",
    "1897_projection_requirements": OUT / "P8_Y5_PARENT_QLOC_1897_DELTAW_PROJECTION_REQUIREMENTS.csv",
}


SOURCE_NEEDLES = {
    "1907_doc": ["NEXT1907_0_primary", "1908-Y5-R2FR-graph-source-extraction-and-TiPt-component-projection.md"],
    "1907_validation": ["VAL1907_OVERALL,PASS"],
    "1907_web": ["WEB1907_2_NIST_ISOTOPES", "SOURCE_CANDIDATE_RECORDED_NOT_EXTRACTED"],
    "1907_graph": ["SMG1907_6_verdict", "SOURCE_BACKED_EXCHANGE_GRAPH_NOT_CLAIM_GRADE"],
    "1907_graph_rows": ["GR1907_6_verdict", "GRAPH_ROWS_NOT_CLAIM_GRADE"],
    "1907_deltaw": ["DWA1907_5_verdict", "DELTAW_INPUT_ACQUISITION_NONCLAIM_NOT_EXECUTABLE"],
    "1907_next": ["NEXT1907_0_primary", "extract source-backed graph/component rows"],
    "1766_standard_graph": ["SMG1766_4_certificate_verdict", "GRAPH_CERTIFICATE_READY_FOR_SOURCING_NOT_CLAIM"],
    "1766_exchange_theorem": ["OMC1766_4_current_verdict", "CONDITIONAL_ORDINARY_BLOCK_ZERO_PARENT_UNSIGNED"],
    "1765_exchange_collapse": ["NEC1765_2_weight_collapse", "DERIVED_CONDITIONAL_THEOREM"],
    "1899_wep_input_pack": ["WIP1899_8_verdict", "WEP_INPUT_PACK_NOT_EXECUTABLE_NONCLAIM"],
    "1900_official_data": ["OFFICIAL_DATA_TARGET_NOT_ACQUIRED_NONCLAIM", "SURROGATE_DESIGN_MATRIX_NOT_OFFICIAL"],
    "1897_projection_matrix": ["DPM1897_6_no_cancellation_policy", "NO_CANCELLATION_POLICY_ENFORCED_NONCLAIM"],
    "1897_projection_requirements": ["DPR1897_1_arena_tau_K", "MISSING_ARENA_PROJECTION_KERNELS"],
}


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1908_SOURCE_REGISTER.csv",
    "web_extraction": OUT / "P8_Y5_PARENT_QLOC_1908_WEB_EXTRACTION_LEDGER_NONCLAIM.csv",
    "isotope_components": OUT / "P8_Y5_PARENT_QLOC_1908_TIPT_NIST_ISOTOPE_COMPONENTS_SOURCE_BACKED_NONCLAIM.csv",
    "element_projection": OUT / "P8_Y5_PARENT_QLOC_1908_TIPT_ELEMENT_LEVEL_PROJECTION_STUB_NONCLAIM.csv",
    "graph_extraction": OUT / "P8_Y5_PARENT_QLOC_1908_GRAPH_SOURCE_EXTRACTION_STATUS_NONCLAIM.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1908_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1908_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1908_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1908_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1908_VALIDATION.csv",
}


BRANCH_COPIES = {
    "isotope_components": SOURCE_WEIGHT_DOCS / "TIPT_NIST_ISOTOPE_COMPONENTS_1908_NONCLAIM.csv",
    "element_projection": MICROSCOPE_RESIDUALS / OUTPUTS["element_projection"].name,
    "graph_extraction": QUEUE / "JR1908_GRAPH_SOURCE_EXTRACTION_STATUS_NONCLAIM.csv",
}


NIST_ISOTOPES = [
    {"element": "Ti", "Z": 22, "isotope_A": 46, "relative_atomic_mass": "45.95262772(35)", "isotopic_composition": 0.0825, "standard_atomic_weight": "47.867(1)", "nist_line": "110"},
    {"element": "Ti", "Z": 22, "isotope_A": 47, "relative_atomic_mass": "46.95175879(38)", "isotopic_composition": 0.0744, "standard_atomic_weight": "47.867(1)", "nist_line": "111"},
    {"element": "Ti", "Z": 22, "isotope_A": 48, "relative_atomic_mass": "47.94794198(38)", "isotopic_composition": 0.7372, "standard_atomic_weight": "47.867(1)", "nist_line": "112"},
    {"element": "Ti", "Z": 22, "isotope_A": 49, "relative_atomic_mass": "48.94786568(39)", "isotopic_composition": 0.0541, "standard_atomic_weight": "47.867(1)", "nist_line": "113"},
    {"element": "Ti", "Z": 22, "isotope_A": 50, "relative_atomic_mass": "49.94478689(39)", "isotopic_composition": 0.0518, "standard_atomic_weight": "47.867(1)", "nist_line": "114"},
    {"element": "Pt", "Z": 78, "isotope_A": 190, "relative_atomic_mass": "189.9599297(63)", "isotopic_composition": 0.00012, "standard_atomic_weight": "195.084(9)", "nist_line": "471"},
    {"element": "Pt", "Z": 78, "isotope_A": 192, "relative_atomic_mass": "191.9610387(32)", "isotopic_composition": 0.00782, "standard_atomic_weight": "195.084(9)", "nist_line": "472"},
    {"element": "Pt", "Z": 78, "isotope_A": 194, "relative_atomic_mass": "193.9626809(10)", "isotopic_composition": 0.3286, "standard_atomic_weight": "195.084(9)", "nist_line": "473"},
    {"element": "Pt", "Z": 78, "isotope_A": 195, "relative_atomic_mass": "194.9647917(10)", "isotopic_composition": 0.3378, "standard_atomic_weight": "195.084(9)", "nist_line": "474"},
    {"element": "Pt", "Z": 78, "isotope_A": 196, "relative_atomic_mass": "195.96495209(99)", "isotopic_composition": 0.2521, "standard_atomic_weight": "195.084(9)", "nist_line": "475"},
    {"element": "Pt", "Z": 78, "isotope_A": 198, "relative_atomic_mass": "197.9678949(23)", "isotopic_composition": 0.07356, "standard_atomic_weight": "195.084(9)", "nist_line": "476"},
]


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


def web_extraction_rows() -> list[dict[str, Any]]:
    return [
        {"source_id": "WEB1908_0_NIST_Ti_isotopes", "source_url": NIST_COMPOSITIONS_URL, "extraction": "Ti isotope masses and natural isotopic compositions extracted into rows IC1908_Ti_*", "source_status": "SOURCE_BACKED_COMPONENT_ROWS_EXTRACTED_NONCLAIM", "source_backed": True, "usable_for_projection": True, "valid_for_claim": False},
        {"source_id": "WEB1908_1_NIST_Pt_isotopes", "source_url": NIST_COMPOSITIONS_URL, "extraction": "Pt isotope masses and natural isotopic compositions extracted into rows IC1908_Pt_*", "source_status": "SOURCE_BACKED_COMPONENT_ROWS_EXTRACTED_NONCLAIM", "source_backed": True, "usable_for_projection": True, "valid_for_claim": False},
        {"source_id": "WEB1908_2_NIST_metadata", "source_url": NIST_INFO_URL, "extraction": "NIST page records atomic weights/isotopic compositions provenance", "source_status": "PROVENANCE_RECORDED", "source_backed": True, "usable_for_projection": False, "valid_for_claim": False},
        {"source_id": "WEB1908_3_MICROSCOPE_bound", "source_url": MICROSCOPE_ARXIV_URL, "extraction": "Ti/Pt alloy WEP bound and experiment context recorded, but no alloy fractions/readout arrays extracted", "source_status": "BOUND_ANCHOR_RECORDED_PROJECTION_BLOCKED", "source_backed": True, "usable_for_projection": False, "valid_for_claim": False},
        {"source_id": "WEB1908_4_PDG_QCD", "source_url": PDG_QCD_URL, "extraction": "QCD source candidate retained for future nuclear-binding graph row extraction", "source_status": "SOURCE_CANDIDATE_NOT_EXTRACTED", "source_backed": False, "usable_for_projection": False, "valid_for_claim": False},
    ]


def isotope_component_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in NIST_ISOTOPES:
        neutron_number = item["isotope_A"] - item["Z"]
        rows.append(
            {
                "component_id": f"IC1908_{item['element']}_{item['isotope_A']}",
                "element": item["element"],
                "Z": item["Z"],
                "A": item["isotope_A"],
                "N": neutron_number,
                "relative_atomic_mass": item["relative_atomic_mass"],
                "natural_isotopic_composition": item["isotopic_composition"],
                "standard_atomic_weight": item["standard_atomic_weight"],
                "source_url": NIST_COMPOSITIONS_URL,
                "source_lines": item["nist_line"],
                "source_backed": True,
                "alloy_corrected": False,
                "binding_decomposed": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
            }
        )
    return rows


def element_projection_rows() -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in NIST_ISOTOPES:
        grouped.setdefault(item["element"], []).append(item)
    rows: list[dict[str, Any]] = []
    for element, items in grouped.items():
        z_value = items[0]["Z"]
        mean_a = sum(item["isotope_A"] * item["isotopic_composition"] for item in items)
        proton_fraction = z_value / mean_a
        neutron_fraction = (mean_a - z_value) / mean_a
        rows.append(
            {
                "projection_id": f"TP1908_{element}_natural_element_stub",
                "element": element,
                "mean_A_from_natural_isotopes": f"{mean_a:.8f}",
                "Z_over_mean_A": f"{proton_fraction:.12f}",
                "N_over_mean_A": f"{neutron_fraction:.12f}",
                "projection_scope": "natural elemental isotope distribution only",
                "source_url": NIST_COMPOSITIONS_URL,
                "source_backed": True,
                "projection_ready": False,
                "why_not_ready": "MICROSCOPE uses Ti/Pt alloys; alloy fractions, electron/binding/nuclear decomposition, material tensor, source-worldtube, and readout kernel are missing",
                "valid_prediction_row": False,
                "valid_for_claim": False,
            }
        )
    ti = next(row for row in rows if row["element"] == "Ti")
    pt = next(row for row in rows if row["element"] == "Pt")
    rows.append(
        {
            "projection_id": "TP1908_Pt_minus_Ti_natural_element_stub",
            "element": "Pt_minus_Ti",
            "mean_A_from_natural_isotopes": "contrast",
            "Z_over_mean_A": f"{float(pt['Z_over_mean_A']) - float(ti['Z_over_mean_A']):.12f}",
            "N_over_mean_A": f"{float(pt['N_over_mean_A']) - float(ti['N_over_mean_A']):.12f}",
            "projection_scope": "natural element Pt minus Ti isotope-only contrast",
            "source_url": NIST_COMPOSITIONS_URL,
            "source_backed": True,
            "projection_ready": False,
            "why_not_ready": "useful sanity stub only; not alloy/material/binding/readout corrected",
            "valid_prediction_row": False,
            "valid_for_claim": False,
        }
    )
    return rows


def graph_extraction_rows() -> list[dict[str, Any]]:
    return [
        {"row_id": "GX1908_0_node_basis", "needed_row": "Ti/Pt natural isotope node/component rows", "current_status": "PARTIAL_SOURCE_BACKED_ISOTOPE_ROWS_EXTRACTED", "what_closed": "natural Ti/Pt isotope masses and compositions now have source-backed component rows", "what_remains": "alloy fractions, electron/proton/neutron/binding source decomposition, material tensor", "source_anchor": "P8_Y5_PARENT_QLOC_1908_TIPT_NIST_ISOTOPE_COMPONENTS_SOURCE_BACKED_NONCLAIM.csv", "source_backed": True, "claim_ready": False, "valid_for_claim": False},
        {"row_id": "GX1908_1_edge_rows", "needed_row": "nonzero exchange/binding edge rows", "current_status": "MISSING_SOURCE_BACKED_EDGE_ROWS", "what_closed": "none", "what_remains": "extract atomic EM binding, nuclear binding, QCD/nuclear component conventions", "source_anchor": "P8_Y5_PARENT_QLOC_1907_LAB_MATTER_GRAPH_ROW_STATUS_NONCLAIM.csv:GR1907_1_edges", "source_backed": False, "claim_ready": False, "valid_for_claim": False},
        {"row_id": "GX1908_2_component_convention", "needed_row": "rest/EM/nuclear/lattice/alloy convention", "current_status": "MISSING_COMPONENT_CONVENTION", "what_closed": "natural isotope Z/A and N/A sanity stub", "what_remains": "binding-energy split and alloy/material source convention", "source_anchor": "P8_Y5_PARENT_QLOC_1908_TIPT_ELEMENT_LEVEL_PROJECTION_STUB_NONCLAIM.csv", "source_backed": False, "claim_ready": False, "valid_for_claim": False},
        {"row_id": "GX1908_3_TiPt_projection", "needed_row": "Ti/Pt WEP material projection", "current_status": "NATURAL_ELEMENT_STUB_ONLY_PROJECTION_BLOCKED", "what_closed": "Pt-minus-Ti isotope-only Z/A and N/A contrast stub", "what_remains": "MICROSCOPE alloy fractions, material tensor, source-worldtube and readout kernels", "source_anchor": "P8_Y5_PARENT_QLOC_1908_TIPT_ELEMENT_LEVEL_PROJECTION_STUB_NONCLAIM.csv:TP1908_Pt_minus_Ti_natural_element_stub", "source_backed": False, "claim_ready": False, "valid_for_claim": False},
        {"row_id": "GX1908_4_readout_kernel", "needed_row": "MICROSCOPE official readout/source-worldtube kernel", "current_status": "OFFICIAL_ARRAYS_NOT_IMPORTED", "what_closed": "bound/context URL retained", "what_remains": "CMSM arrays or validated equivalent", "source_anchor": "P8_Y5_PARENT_QLOC_1900_OFFICIAL_READOUT_DATA_TARGETS_NONCLAIM.csv:cmsm_ds_onera_root", "source_backed": False, "claim_ready": False, "valid_for_claim": False},
        {"row_id": "GX1908_5_source_shadow", "needed_row": "source-shadow/decoupled sector exclusion", "current_status": "MISSING_SOURCE_SHADOW_EXCLUSION", "what_closed": "none", "what_remains": "parent theorem or arena inventory excluding independent source blocks", "source_anchor": "P8_Y5_PARENT_QLOC_1907_LAB_MATTER_GRAPH_ROW_STATUS_NONCLAIM.csv:GR1907_5_source_shadow", "source_backed": False, "claim_ready": False, "valid_for_claim": False},
        {"row_id": "GX1908_6_verdict", "needed_row": "1908 graph extraction verdict", "current_status": "PARTIAL_COMPONENT_EXTRACTION_GRAPH_CERTIFICATE_STILL_BLOCKED", "what_closed": "NIST isotope/component extraction and element-level projection stub", "what_remains": "GX1908_1 through GX1908_5", "source_anchor": "GX1908_0_node_basis through GX1908_5_source_shadow", "source_backed": False, "claim_ready": False, "valid_for_claim": False},
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {"gate_id": "CG1908_0_isotopes", "condition": "source-backed Ti/Pt isotope rows exist", "current_status": "PASS_COMPONENT_ROWS_EXTRACTED_NONCLAIM", "source_anchor": "P8_Y5_PARENT_QLOC_1908_TIPT_NIST_ISOTOPE_COMPONENTS_SOURCE_BACKED_NONCLAIM.csv", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1908_1_projection", "condition": "Ti/Pt projection is alloy/material/binding/readout corrected", "current_status": "FAIL_NATURAL_ELEMENT_STUB_ONLY_PROJECTION_BLOCKED", "source_anchor": "P8_Y5_PARENT_QLOC_1908_TIPT_ELEMENT_LEVEL_PROJECTION_STUB_NONCLAIM.csv:TP1908_Pt_minus_Ti_natural_element_stub", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1908_2_graph", "condition": "source-backed exchange graph certificate is complete", "current_status": "FAIL_PARTIAL_COMPONENT_EXTRACTION_GRAPH_CERTIFICATE_STILL_BLOCKED", "source_anchor": "P8_Y5_PARENT_QLOC_1908_GRAPH_SOURCE_EXTRACTION_STATUS_NONCLAIM.csv:GX1908_6_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1908_3_claim", "condition": "1908 supports local-GR source universality or claim-grade Delta_w score", "current_status": "CLAIM_BLOCKED", "source_anchor": "CG1908_0_isotopes through CG1908_2_graph", "gate_pass": False, "valid_for_claim": False},
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {"decision_id": "DEC1908_0_keep", "decision": "keep NIST isotope extraction as useful component evidence", "reason": "Ti/Pt natural isotope rows are source-backed and give a reproducible element-level sanity projection", "status": "COMPONENT_EVIDENCE_GAINED_NONCLAIM", "next_dependency": "alloy/material/binding/readout corrections", "valid_for_claim": False},
        {"decision_id": "DEC1908_1_block", "decision": "do not promote graph certificate", "reason": "edge rows, component convention, material projection, source-shadow exclusion and kernels remain missing", "status": "GRAPH_CERTIFICATE_STILL_BLOCKED", "next_dependency": "extract binding/material graph rows", "valid_for_claim": False},
        {"decision_id": "DEC1908_2_next", "decision": "attack binding/material projection next", "reason": "the fastest useful improvement is turning isotope rows into a material/source projection convention", "status": "NEXT_TARGET_SELECTED", "next_dependency": "1909 Ti/Pt alloy-material-binding projection or blocker ledger", "valid_for_claim": False},
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1908_0_primary",
            "selection_status": "selected",
            "target_doc": "1909-Y5-R2FR-TiPt-alloy-material-binding-projection-or-blocker-ledger.md",
            "target_script": "scripts/Y5_R2FR_TiPt_alloy_material_binding_projection_or_blocker_1909.py",
            "objective": "try to upgrade natural Ti/Pt isotope rows into alloy/material/binding projection rows; if unavailable, emit exact blocker ledger and acquisition targets",
            "success_condition": "source-backed alloy/material/binding projection convention, or explicit missing-source blockers",
            "do_not": "do not use natural element isotope stubs as WEP prediction rows, do not claim local-GR/WEP pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {"status_id": "STAT1908_0_gain", "area": "source-backed extraction", "summary": "Ti/Pt natural isotope rows are now extracted from NIST into local nonclaim component tables", "risk_level": "REAL_PROGRESS_NONCLAIM", "project_meaning": "the finite source branch has its first real component data rather than only placeholders", "next_action": "source alloy/material/binding conventions", "valid_for_claim": False},
        {"status_id": "STAT1908_1_block", "area": "projection", "summary": "element-level Z/A and N/A contrast is only a sanity stub, not a MICROSCOPE projection", "risk_level": "PROJECTION_BLOCKED", "project_meaning": "we are not cheating by pretending natural isotopes equal test-body source response", "next_action": "build material projection or blocker ledger", "valid_for_claim": False},
        {"status_id": "STAT1908_2_theory", "area": "GR source route", "summary": "exchange-collapse theorem remains conditional; graph certificate still blocked by missing source rows and source-shadow exclusion", "risk_level": "THEOREM_CONDITIONAL", "project_meaning": "derivation route survives but needs graph/material sourcing before promotion", "next_action": "extract binding/material graph rows", "valid_for_claim": False},
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "web_extraction": web_extraction_rows(),
        "isotope_components": isotope_component_rows(),
        "element_projection": element_projection_rows(),
        "graph_extraction": graph_extraction_rows(),
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


def claim_flags_safe(paths: list[Path]) -> tuple[bool, str]:
    bad: list[str] = []
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            for field in ["valid_for_claim", "valid_prediction_row", "claim_allowed", "projection_ready", "claim_ready", "gate_pass"]:
                if field in row and bool_string(row[field]) == "true":
                    bad.append(f"{path.name}:{index}:{field}=true")
    return not bad, "; ".join(bad) if bad else "all claim/prediction/projection-ready flags remain false"


def isotope_rows_valid(rows: list[dict[str, str]]) -> tuple[bool, str]:
    bad: list[str] = []
    for row in rows:
        try:
            if int(row["A"]) <= int(row["Z"]):
                bad.append(f"{row['component_id']}:A<=Z")
            composition = float(row["natural_isotopic_composition"])
            if composition <= 0:
                bad.append(f"{row['component_id']}:composition<=0")
        except Exception as exc:
            bad.append(f"{row.get('component_id', 'unknown')}:{exc}")
    elements = {row["element"] for row in rows}
    for element in elements:
        total = sum(float(row["natural_isotopic_composition"]) for row in rows if row["element"] == element)
        if abs(total - 1.0) > 5e-4:
            bad.append(f"{element}:composition_sum={total}")
    return not bad, "; ".join(bad) if bad else "NIST isotope rows numeric and compositions sum to unity tolerance"


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks: list[dict[str, Any]] = []
    source_rows_loaded = csv_rows(OUTPUTS["source_register"])
    checks.append({"validation_id": "VAL1908_00_sources", "status": "PASS" if all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows_loaded) else "FAIL", "detail": "all local source paths exist and needles found", "valid_for_claim": False})
    isotope_rows = csv_rows(OUTPUTS["isotope_components"])
    iso_ok, iso_detail = isotope_rows_valid(isotope_rows)
    checks.append({"validation_id": "VAL1908_01_isotope_rows", "status": "PASS" if iso_ok and len(isotope_rows) == 11 else "FAIL", "detail": iso_detail, "valid_for_claim": False})
    projection_rows = csv_rows(OUTPUTS["element_projection"])
    checks.append({"validation_id": "VAL1908_02_projection_stub", "status": "PASS" if len(projection_rows) == 3 and all(bool_string(row["projection_ready"]) == "false" for row in projection_rows) else "FAIL", "detail": "natural element projection stub exists but is not projection-ready", "valid_for_claim": False})
    graph_rows = csv_rows(OUTPUTS["graph_extraction"])
    checks.append({"validation_id": "VAL1908_03_graph_verdict", "status": "PASS" if any(row["row_id"] == "GX1908_6_verdict" and row["current_status"] == "PARTIAL_COMPONENT_EXTRACTION_GRAPH_CERTIFICATE_STILL_BLOCKED" for row in graph_rows) else "FAIL", "detail": "graph certificate remains blocked after partial extraction", "valid_for_claim": False})
    gate_rows = csv_rows(OUTPUTS["claim_gate"])
    checks.append({"validation_id": "VAL1908_04_claim_gate", "status": "PASS" if any(row["gate_id"] == "CG1908_3_claim" and row["current_status"] == "CLAIM_BLOCKED" for row in gate_rows) else "FAIL", "detail": "claim remains blocked", "valid_for_claim": False})
    next_rows = csv_rows(OUTPUTS["next_target"])
    checks.append({"validation_id": "VAL1908_05_next_target", "status": "PASS" if any(row["route_id"] == "NEXT1908_0_primary" and row["selection_status"] == "selected" for row in next_rows) else "FAIL", "detail": "1909 target selected", "valid_for_claim": False})
    flags_ok, flags_detail = claim_flags_safe(generated_without_validation)
    checks.append({"validation_id": "VAL1908_06_claim_flags_safe", "status": "PASS" if flags_ok else "FAIL", "detail": flags_detail, "valid_for_claim": False})
    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append({"validation_id": "VAL1908_07_csv_parse", "status": "PASS" if parse_ok else "FAIL", "detail": parse_detail, "valid_for_claim": False})
    checks.append({"validation_id": "VAL1908_08_branch_copies", "status": "PASS" if all(path.exists() for path in BRANCH_COPIES.values()) else "FAIL", "detail": "; ".join(str(path) for path in BRANCH_COPIES.values()), "valid_for_claim": False})
    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append({"validation_id": "VAL1908_09_pycache_absent", "status": "PASS" if not pycache.exists() else "FAIL", "detail": str(pycache), "valid_for_claim": False})
    formalization_hits = []
    if FORMALIZATION.exists():
        artifact_needles = [
            "1908-Y5-R2FR-graph-source-extraction",
            "P8_Y5_PARENT_QLOC_1908",
            "Y5_R2FR_graph_source_extraction_and_TiPt_component_projection_1908",
        ]
        formalization_hits = [
            path
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and any(needle in path.name for needle in artifact_needles)
        ]
    checks.append({"validation_id": "VAL1908_10_formalization_untouched", "status": "PASS" if not formalization_hits else "FAIL", "detail": f"formalization_1908_artifact_count={len(formalization_hits)}", "valid_for_claim": False})
    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append({"validation_id": "VAL1908_OVERALL", "status": "PASS" if fail_count == 0 else "FAIL", "detail": "1908 graph source extraction and Ti/Pt component projection", "valid_for_claim": False})
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1908 - Graph Source Extraction And Ti/Pt Component Projection

## Purpose

This checkpoint upgrades the previous URL-only source ledger by extracting source-backed natural-isotope component rows for Ti and Pt from NIST, then testing whether that is enough for a graph certificate or WEP projection. It is not enough, but it is real progress.

## Result

- NIST Ti/Pt natural isotope rows are now local, source-backed, and parseable.
- A reproducible natural-element `Z/A` and `N/A` contrast stub is now generated.
- The projection remains nonclaim: MICROSCOPE uses alloys, and the material/binding/readout/source-worldtube pieces are still missing.
- The standard-matter exchange graph remains blocked because edge rows, component conventions, source-shadow exclusion, and arena kernels are not extracted.
- No local-GR, WEP, or `Delta_w` claim is promoted.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Web Extraction Ledger

{markdown_table(rows_by_name["web_extraction"])}

## NIST Ti/Pt Isotope Components

{markdown_table(rows_by_name["isotope_components"])}

## Ti/Pt Element-Level Projection Stub

{markdown_table(rows_by_name["element_projection"])}

## Graph Extraction Status

{markdown_table(rows_by_name["graph_extraction"])}

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
