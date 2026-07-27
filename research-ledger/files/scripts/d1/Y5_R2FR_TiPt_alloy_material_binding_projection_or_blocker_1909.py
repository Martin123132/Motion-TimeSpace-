from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1909"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1909-Y5-R2FR-TiPt-alloy-material-binding-projection-or-blocker-ledger.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()

MICROSCOPE_FINAL_ARXIV = "https://arxiv.org/abs/2209.15487"
MICROSCOPE_CQG_ARXIV = "https://arxiv.org/abs/2209.15488"
MICROSCOPE_CQG_DOI = "https://doi.org/10.1088/1361-6382/ac84be"
MICROSCOPE_MISSION_PDF = "https://inspirehep.net/files/9a51796b3d7d940b16bd170876e35e4e"
NIST_COMPOSITIONS_URL = "https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl"


INPUTS = {
    "1908_doc": ROOT / "1908-Y5-R2FR-graph-source-extraction-and-TiPt-component-projection.md",
    "1908_validation": OUT / "P8_Y5_BRR545_1908_VALIDATION.csv",
    "1908_next": OUT / "P8_Y5_PARENT_QLOC_1908_NEXT_TARGET.csv",
    "1908_isotopes": OUT / "P8_Y5_PARENT_QLOC_1908_TIPT_NIST_ISOTOPE_COMPONENTS_SOURCE_BACKED_NONCLAIM.csv",
    "1908_element_stub": OUT / "P8_Y5_PARENT_QLOC_1908_TIPT_ELEMENT_LEVEL_PROJECTION_STUB_NONCLAIM.csv",
    "1908_graph_status": OUT / "P8_Y5_PARENT_QLOC_1908_GRAPH_SOURCE_EXTRACTION_STATUS_NONCLAIM.csv",
    "983_constituents": OUT / "P8_Y5_R10_983_MATERIAL_CONSTITUENTS.csv",
    "983_proxy_vectors": OUT / "P8_Y5_R10_983_MATERIAL_PROXY_CHARGE_VECTORS.csv",
    "1061_material_convention": OUT / "P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv",
    "1424_material_candidates": OUT / "P8_Y5_R10_1424_TIPT_MATERIAL_VECTOR_CANDIDATES.csv",
    "1330_electron_fractions": ROOT / "source-intake" / "component-fractions" / "raw" / "P8_Y5_R10_1330_AUDITED_ELECTRON_FRACTION_CANDIDATE_NONCLAIM.csv",
    "1481_context_pack": MICROSCOPE_RESIDUALS.parent / "coefficients" / "WEP_material_context_pack_nonclaim_1481.csv",
    "1607_tensor_audit": MICROSCOPE_RESIDUALS / "R2FR_material_tensor_context_audit_nonclaim_1607.csv",
    "1900_official_data": OUT / "P8_Y5_PARENT_QLOC_1900_OFFICIAL_READOUT_DATA_TARGETS_NONCLAIM.csv",
}


SOURCE_NEEDLES = {
    "1908_doc": ["NEXT1908_0_primary", "1909-Y5-R2FR-TiPt-alloy-material-binding-projection-or-blocker-ledger.md"],
    "1908_validation": ["VAL1908_OVERALL,PASS"],
    "1908_next": ["NEXT1908_0_primary", "alloy/material/binding projection rows"],
    "1908_isotopes": ["IC1908_Ti_46", "IC1908_Pt_198"],
    "1908_element_stub": ["TP1908_Pt_minus_Ti_natural_element_stub", "valid_for_claim"],
    "1908_graph_status": ["GX1908_6_verdict", "PARTIAL_COMPONENT_EXTRACTION_GRAPH_CERTIFICATE_STILL_BLOCKED"],
    "983_constituents": ["M983_0_PtRh10", "M983_1_TiAlloy"],
    "983_proxy_vectors": ["proxy_charge_vector_computed", "Y_e_proxy"],
    "1061_material_convention": ["MCON1061_0_test_pair", "TA6V outer test mass minus PtRh10 inner test mass"],
    "1424_material_candidates": ["MAT1424_2_electron_mass_fraction", "AUDITED_NUMERIC_PARENT_NORMALIZATION_MISSING"],
    "1330_electron_fractions": ["CFI1330_TA6V_electron", "CFI1330_PtRh10_electron"],
    "1481_context_pack": ["MAT1481_6_full_tensor", "MISSING_FULL_PARENT_MATERIAL_TENSOR"],
    "1607_tensor_audit": ["MTA1607_5_full_tensor", "MISSING_FULL_PARENT_MATERIAL_TENSOR"],
    "1900_official_data": ["OFFICIAL_DATA_TARGET_NOT_ACQUIRED_NONCLAIM", "SURROGATE_DESIGN_MATRIX_NOT_OFFICIAL"],
}


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1909_SOURCE_REGISTER.csv",
    "web_source_ledger": OUT / "P8_Y5_PARENT_QLOC_1909_WEB_SOURCE_LEDGER_NONCLAIM.csv",
    "alloy_composition": OUT / "P8_Y5_PARENT_QLOC_1909_TIPT_ALLOY_COMPOSITION_SOURCE_BACKED_NONCLAIM.csv",
    "alloy_proxy": OUT / "P8_Y5_PARENT_QLOC_1909_TIPT_ALLOY_PROXY_VECTOR_NONCLAIM.csv",
    "binding_blockers": OUT / "P8_Y5_PARENT_QLOC_1909_MATERIAL_BINDING_PROJECTION_BLOCKER_LEDGER_NONCLAIM.csv",
    "projection_status": OUT / "P8_Y5_PARENT_QLOC_1909_TIPT_MATERIAL_BINDING_PROJECTION_STATUS_NONCLAIM.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1909_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1909_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1909_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1909_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1909_VALIDATION.csv",
}


BRANCH_COPIES = {
    "alloy_proxy": SOURCE_WEIGHT_DOCS / "TIPT_ALLOY_PROXY_VECTOR_1909_NONCLAIM.csv",
    "projection_status": MICROSCOPE_RESIDUALS / OUTPUTS["projection_status"].name,
    "binding_blockers": QUEUE / "JR1909_TIPT_MATERIAL_BINDING_BLOCKERS_NONCLAIM.csv",
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
        {
            "source_id": "WEB1909_0_MICROSCOPE_FINAL_PRL_ARXIV",
            "source_url": MICROSCOPE_FINAL_ARXIV,
            "role": "final MICROSCOPE WEP result and Ti/Pt alloy experiment context",
            "extracted_or_used": "bound/context only; no official readout arrays imported",
            "source_status": "SOURCE_URL_RECORDED_CONTEXT_ONLY",
            "source_backed": True,
            "valid_for_claim": False,
        },
        {
            "source_id": "WEB1909_1_MICROSCOPE_CQG_RESULT",
            "source_url": MICROSCOPE_CQG_ARXIV,
            "role": "long-form MICROSCOPE WEP analysis and material/readout context",
            "extracted_or_used": "composition convention cross-check; no source-worldtube kernel imported",
            "source_status": "SOURCE_URL_RECORDED_CONTEXT_ONLY",
            "source_backed": True,
            "valid_for_claim": False,
        },
        {
            "source_id": "WEB1909_2_MICROSCOPE_CQG_DOI",
            "source_url": MICROSCOPE_CQG_DOI,
            "role": "published CQG DOI for WEP result",
            "extracted_or_used": "bibliographic provenance for local nonclaim composition context",
            "source_status": "DOI_RECORDED",
            "source_backed": True,
            "valid_for_claim": False,
        },
        {
            "source_id": "WEB1909_3_MICROSCOPE_MISSION_COMPOSITION",
            "source_url": MICROSCOPE_MISSION_PDF,
            "role": "mission summary source for PtRh10 and TA6V composition convention",
            "extracted_or_used": "supports PtRh10=90% Pt/10% Rh and TA6V=90% Ti/6% Al/4% V context already present in local 983 rows",
            "source_status": "SOURCE_URL_RECORDED_COMPOSITION_CONTEXT",
            "source_backed": True,
            "valid_for_claim": False,
        },
        {
            "source_id": "WEB1909_4_NIST_ISOTOPIC_CONTEXT",
            "source_url": NIST_COMPOSITIONS_URL,
            "role": "natural isotope/atomic weight context from 1908",
            "extracted_or_used": "Ti/Pt extracted in 1908; Al/V/Rh exact isotope expansion still not imported here",
            "source_status": "PARTIAL_COMPONENT_SOURCE_RECORDED",
            "source_backed": True,
            "valid_for_claim": False,
        },
    ]


def constituent_rows_by_material() -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in csv_rows(INPUTS["983_constituents"]):
        grouped.setdefault(row["material_id"], []).append(row)
    return grouped


def electron_fraction_lookup() -> dict[str, dict[str, str]]:
    return {row["material_id"]: row for row in csv_rows(INPUTS["1330_electron_fractions"])}


def proxy_lookup() -> dict[str, dict[str, str]]:
    return {row["material_id"]: row for row in csv_rows(INPUTS["983_proxy_vectors"])}


def public_material_name(material_id: str) -> str:
    if material_id == "M983_0_PtRh10":
        return "PtRh10"
    if material_id == "M983_1_TiAlloy":
        return "TA6V"
    return material_id


def material_id_for_public(public_name: str) -> str:
    if public_name == "PtRh10":
        return "M983_0_PtRh10"
    if public_name == "TA6V":
        return "M983_1_TiAlloy"
    return public_name


def material_metrics(rows: list[dict[str, str]]) -> dict[str, float]:
    mass_fraction_sum = sum(float(row["mass_fraction"]) for row in rows)
    z_over_a = sum(float(row["mass_fraction"]) * float(row["Z"]) / float(row["A"]) for row in rows)
    n_over_a = sum(float(row["mass_fraction"]) * (float(row["A"]) - float(row["Z"])) / float(row["A"]) for row in rows)
    neutron_excess = n_over_a - z_over_a
    a_bar = sum(float(row["mass_fraction"]) * float(row["A"]) for row in rows)
    z_bar = sum(float(row["mass_fraction"]) * float(row["Z"]) for row in rows)
    return {
        "mass_fraction_sum": mass_fraction_sum,
        "Z_over_A_proxy": z_over_a,
        "N_over_A_proxy": n_over_a,
        "neutron_excess_proxy": neutron_excess,
        "A_bar_proxy": a_bar,
        "Z_bar_proxy": z_bar,
    }


def alloy_composition_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for material_id, entries in constituent_rows_by_material().items():
        metrics = material_metrics(entries)
        for entry in entries:
            rows.append(
                {
                    "composition_id": f"AC1909_{public_material_name(material_id)}_{entry['element']}",
                    "material_id": public_material_name(material_id),
                    "element": entry["element"],
                    "mass_fraction": f"{float(entry['mass_fraction']):.12f}",
                    "A_context": entry["A"],
                    "Z": entry["Z"],
                    "source_row": entry["source"],
                    "local_source_path": str(INPUTS["983_constituents"]),
                    "web_source_context": f"{MICROSCOPE_CQG_ARXIV}; {MICROSCOPE_MISSION_PDF}",
                    "mass_fraction_sum_for_material": f"{metrics['mass_fraction_sum']:.12f}",
                    "source_backed_composition_context": True,
                    "exact_flight_isotope_mix": False,
                    "binding_decomposed": False,
                    "readout_corrected": False,
                    "valid_projection_row": False,
                    "valid_for_claim": False,
                }
            )
    return rows


def material_proxy_rows() -> list[dict[str, Any]]:
    grouped = constituent_rows_by_material()
    electron_lookup = electron_fraction_lookup()
    proxy_rows = proxy_lookup()
    rows: list[dict[str, Any]] = []
    material_order = ["M983_0_PtRh10", "M983_1_TiAlloy"]
    material_summaries: dict[str, dict[str, float]] = {}
    for material_id in material_order:
        metrics = material_metrics(grouped[material_id])
        material_summaries[material_id] = metrics
        public_name = public_material_name(material_id)
        electron_row = electron_lookup[public_name]
        proxy_row = proxy_rows[material_id]
        rows.append(
            {
                "proxy_id": f"AP1909_{public_name}",
                "material_id": public_name,
                "left_minus_right": "not_applicable",
                "mass_fraction_sum": f"{metrics['mass_fraction_sum']:.12f}",
                "Z_over_A_proxy": f"{metrics['Z_over_A_proxy']:.12e}",
                "N_over_A_proxy": f"{metrics['N_over_A_proxy']:.12e}",
                "neutron_excess_proxy": f"{metrics['neutron_excess_proxy']:.12e}",
                "electron_rest_mass_fraction": electron_row["fraction_value"],
                "coulomb_formula_proxy": proxy_row["coulomb_proxy"],
                "A_bar_proxy": f"{metrics['A_bar_proxy']:.12e}",
                "basis_convention": "MICROSCOPE alloy mass-fraction proxy from 983 plus electron candidate 1330",
                "source_anchor": f"{INPUTS['983_constituents'].name}; {INPUTS['1330_electron_fractions'].name}",
                "usable_level": "ALLOY_PROXY_CONTEXT_ONLY",
                "missing_for_claim": "binding-energy split, parent MTS response basis, source-worldtube/readout kernels, tau normalization",
                "source_backed_composition_context": True,
                "binding_decomposed": False,
                "projection_ready": False,
                "valid_for_claim": False,
            }
        )
    ta6v = material_summaries["M983_1_TiAlloy"]
    ptrh = material_summaries["M983_0_PtRh10"]
    ta6v_e = float(electron_lookup["TA6V"]["fraction_value"])
    ptrh_e = float(electron_lookup["PtRh10"]["fraction_value"])
    ta6v_proxy = proxy_rows["M983_1_TiAlloy"]
    ptrh_proxy = proxy_rows["M983_0_PtRh10"]
    rows.append(
        {
            "proxy_id": "AP1909_TA6V_minus_PtRh10",
            "material_id": "TA6V_minus_PtRh10",
            "left_minus_right": "TA6V_minus_PtRh10",
            "mass_fraction_sum": "not_applicable",
            "Z_over_A_proxy": f"{ta6v['Z_over_A_proxy'] - ptrh['Z_over_A_proxy']:.12e}",
            "N_over_A_proxy": f"{ta6v['N_over_A_proxy'] - ptrh['N_over_A_proxy']:.12e}",
            "neutron_excess_proxy": f"{ta6v['neutron_excess_proxy'] - ptrh['neutron_excess_proxy']:.12e}",
            "electron_rest_mass_fraction": f"{ta6v_e - ptrh_e:.12e}",
            "coulomb_formula_proxy": f"{float(ta6v_proxy['coulomb_proxy']) - float(ptrh_proxy['coulomb_proxy']):.12e}",
            "A_bar_proxy": f"{ta6v['A_bar_proxy'] - ptrh['A_bar_proxy']:.12e}",
            "basis_convention": "same sign as MCON1061_0_test_pair and 1481 context pack",
            "source_anchor": f"{INPUTS['1061_material_convention'].name}:MCON1061_0_test_pair; {INPUTS['1424_material_candidates'].name}:MAT1424_2_electron_mass_fraction",
            "usable_level": "DIFFERENTIAL_ALLOY_PROXY_CONTEXT_ONLY",
            "missing_for_claim": "full material tensor, MTS parent coefficient owner, no-double-counting rule, source/readout/tau normalization",
            "source_backed_composition_context": True,
            "binding_decomposed": False,
            "projection_ready": False,
            "valid_for_claim": False,
        }
    )
    return rows


def binding_blocker_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker_id": "BB1909_0_flight_material_isotopes",
            "needed_object": "flight-material isotope fractions for PtRh10 and TA6V",
            "current_input": "natural Ti/Pt isotope rows plus alloy elemental mass fractions",
            "why_it_blocks": "flight material may not equal natural elemental isotope mix; Al, V, Rh isotope rows were not expanded in 1909",
            "minimum_acceptance": "source-backed isotope table for Pt, Rh, Ti, Al, V or official statement permitting natural abundance proxy",
            "candidate_source": f"{NIST_COMPOSITIONS_URL}; {MICROSCOPE_CQG_ARXIV}",
            "status": "MISSING_FULL_FLIGHT_ISOTOPE_MIX",
            "valid_for_claim": False,
        },
        {
            "blocker_id": "BB1909_1_atomic_nuclear_mass_convention",
            "needed_object": "atomic-to-nuclear mass and electron subtraction convention",
            "current_input": "electron rest-mass fraction proxy from 1330",
            "why_it_blocks": "atomic masses include electrons and chemical/nuclear conventions; WEP response tensor needs one no-double-counting mass functional",
            "minimum_acceptance": "parent-signed mass functional or source-backed convention splitting electron, proton, neutron, binding, and residual mass",
            "candidate_source": "P8_Y5_R10_1330_AUDITED_ELECTRON_FRACTION_CANDIDATE_NONCLAIM.csv; PDG/CODATA/AME source pack",
            "status": "MISSING_MASS_FUNCTIONAL_NO_DOUBLE_COUNT_RULE",
            "valid_for_claim": False,
        },
        {
            "blocker_id": "BB1909_2_EM_Coulomb_binding_owner",
            "needed_object": "EM/Coulomb binding response under MTS parent generator",
            "current_input": "DD-style smoke components and rough coulomb_formula_proxy",
            "why_it_blocks": "external Damour-Donoghue or liquid-drop proxies cannot be imported as MTS parent coefficients without an operator owner",
            "minimum_acceptance": "MTS parent EM owner, sign convention, derivative map, and bounded mismatch to any external proxy",
            "candidate_source": "P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv; C_parent_WEP_EM_edge_signing_decision_1466.csv",
            "status": "MISSING_PARENT_EM_BINDING_OPERATOR_OWNER",
            "valid_for_claim": False,
        },
        {
            "blocker_id": "BB1909_3_nuclear_binding_decomposition",
            "needed_object": "nuclear volume/surface/asymmetry/pairing/QCD split",
            "current_input": "surface/binding smoke contrast only",
            "why_it_blocks": "one scalar surface proxy cannot stand in for a source-basis tensor unless the parent basis selects it",
            "minimum_acceptance": "exact mass-defect tensor or parent theorem reducing nuclear binding to retained components",
            "candidate_source": "AME2020/nuclear-mass source pack; P8_Y5_R10_1080_MATERIAL_COMPOSITION_AND_TENSOR_CANDIDATES.csv",
            "status": "MISSING_NUCLEAR_BINDING_TENSOR",
            "valid_for_claim": False,
        },
        {
            "blocker_id": "BB1909_4_lattice_impurity_and_shape",
            "needed_object": "alloy lattice/chemical binding, impurities, coatings, and test-body geometry convention",
            "current_input": "bulk mass-fraction alloy labels only",
            "why_it_blocks": "flight test bodies are not abstract elemental mixtures; local source response may depend on material processing/coatings if parent coupling sees those sectors",
            "minimum_acceptance": "official material spec or parent theorem proving these sectors are common-mode/negligible",
            "candidate_source": f"{MICROSCOPE_CQG_ARXIV}; {MICROSCOPE_CQG_DOI}",
            "status": "MISSING_FLIGHT_MATERIAL_SYSTEMATICS_OR_ZERO_THEOREM",
            "valid_for_claim": False,
        },
        {
            "blocker_id": "BB1909_5_source_readout_kernel",
            "needed_object": "source-worldtube/readout/tau kernel",
            "current_input": "official portal targets and surrogate guard from 1900",
            "why_it_blocks": "a material vector is not an eta prediction until it is contracted with source, readout, and normalization kernels",
            "minimum_acceptance": "official CMSM arrays or parent-signed point-source/common-mode theorem plus tau/product convention",
            "candidate_source": "P8_Y5_PARENT_QLOC_1900_OFFICIAL_READOUT_DATA_TARGETS_NONCLAIM.csv",
            "status": "MISSING_SOURCE_READOUT_TAU_KERNEL",
            "valid_for_claim": False,
        },
    ]


def projection_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "MP1909_0_alloy_composition",
            "object": "PtRh10 and TA6V alloy mass-fraction composition",
            "current_status": "SOURCE_BACKED_COMPOSITION_CONTEXT_FILLED",
            "gain": "moves beyond 1908 natural Ti/Pt element-only stub",
            "remaining_blocker": "not a binding/material response tensor",
            "source_anchor": OUTPUTS["alloy_composition"].name,
            "projection_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "MP1909_1_differential_proxy",
            "object": "TA6V_minus_PtRh10 differential alloy proxy vector",
            "current_status": "NUMERIC_PROXY_CONTEXT_FILLED_NONCLAIM",
            "gain": "Z/A, N/A, neutron-excess, electron-rest-mass, Coulomb-proxy and Abar contrasts are now in one sign convention",
            "remaining_blocker": "parent basis/no-double-count/readout/source/tau missing",
            "source_anchor": OUTPUTS["alloy_proxy"].name + ":AP1909_TA6V_minus_PtRh10",
            "projection_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "MP1909_2_binding_projection",
            "object": "material binding projection row",
            "current_status": "BINDING_PROJECTION_BLOCKED_EXPLICITLY",
            "gain": "blockers are now separated by isotope, mass convention, EM owner, nuclear tensor, flight material, and readout kernel",
            "remaining_blocker": "BB1909_0 through BB1909_5",
            "source_anchor": OUTPUTS["binding_blockers"].name,
            "projection_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "MP1909_3_verdict",
            "object": "1909 Ti/Pt material projection",
            "current_status": "ALLOY_PROXY_GAINED_MATERIAL_BINDING_PROJECTION_STILL_BLOCKED",
            "gain": "source-backed alloy proxy scaffold is usable for smoke/debug only",
            "remaining_blocker": "full parent material tensor and source/readout product",
            "source_anchor": "MP1909_0_alloy_composition; MP1909_1_differential_proxy; MP1909_2_binding_projection",
            "projection_ready": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG1909_0_alloy",
            "condition": "alloy mass fractions are source-backed and sum to unity",
            "current_status": "PASS_CONTEXT_ONLY",
            "source_anchor": OUTPUTS["alloy_composition"].name,
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1909_1_binding",
            "condition": "material binding tensor is source-backed or parent-derived",
            "current_status": "FAIL_BINDING_PROJECTION_BLOCKED_EXPLICITLY",
            "source_anchor": OUTPUTS["binding_blockers"].name,
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1909_2_readout",
            "condition": "material tensor is contracted with source-worldtube/readout/tau kernels",
            "current_status": "FAIL_SOURCE_READOUT_TAU_KERNEL_MISSING",
            "source_anchor": "P8_Y5_PARENT_QLOC_1900_OFFICIAL_READOUT_DATA_TARGETS_NONCLAIM.csv",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1909_3_claim",
            "condition": "1909 supports WEP/local-GR claim-grade projection",
            "current_status": "CLAIM_BLOCKED",
            "source_anchor": "CG1909_0_alloy through CG1909_2_readout",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1909_0_keep",
            "decision": "keep alloy proxy scaffold",
            "reason": "it is a real improvement over natural Ti/Pt stubs and fixes the sign convention around TA6V_minus_PtRh10",
            "status": "ALLOY_PROXY_CONTEXT_GAINED_NONCLAIM",
            "next_dependency": "binding/material tensor owner",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1909_1_block",
            "decision": "do not promote binding projection",
            "reason": "binding decomposition, parent basis, no-double-counting, and readout/source kernels are still absent",
            "status": "MATERIAL_BINDING_PROJECTION_BLOCKED",
            "next_dependency": "derive parent material response functional or source exact mass-defect tensor",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1909_2_next",
            "decision": "attack parent material response functional before more data polishing",
            "reason": "more alloy proxies will not become physics until a parent-owned tensor says what the retained components mean",
            "status": "NEXT_TARGET_SELECTED",
            "next_dependency": "1910 parent material response functional or exact mass-defect tensor contract",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1909_0_primary",
            "selection_status": "selected",
            "target_doc": "1910-Y5-R2FR-parent-material-response-functional-or-exact-mass-defect-tensor-contract.md",
            "target_script": "scripts/Y5_R2FR_parent_material_response_functional_or_exact_mass_defect_tensor_contract_1910.py",
            "objective": "derive the parent material response functional that maps constituent/binding data into Delta_w, or write the exact source contract for an external mass-defect tensor",
            "success_condition": "parent-owned no-double-count response basis, or precise external tensor acquisition contract that cannot be mistaken for a claim",
            "do_not": "do not promote alloy proxies, DD smoke components, or natural isotope rows as MTS WEP predictions",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT1909_0_gain",
            "area": "material data",
            "summary": "1909 now carries source-backed PtRh10/TA6V alloy composition and a unified differential proxy vector",
            "risk_level": "REAL_PROGRESS_NONCLAIM",
            "project_meaning": "the WEP branch has moved from element stubs to actual alloy context",
            "next_action": "derive parent material response functional",
            "valid_for_claim": False,
        },
        {
            "status_id": "STAT1909_1_block",
            "area": "binding projection",
            "summary": "the real missing piece is not more Z/A arithmetic; it is the parent-owned material/binding response tensor",
            "risk_level": "CENTRAL_THEORY_GAP_EXPOSED",
            "project_meaning": "this is exactly the coupling/material-response hole the local branch has been circling",
            "next_action": "prove or contract the response functional",
            "valid_for_claim": False,
        },
        {
            "status_id": "STAT1909_2_claim",
            "area": "WEP/local-GR",
            "summary": "claim remains blocked; the new rows are smoke/debug scaffolds only",
            "risk_level": "SAFE_NONCLAIM",
            "project_meaning": "we gained usable structure without weakening the standards",
            "next_action": "1910 response functional route",
            "valid_for_claim": False,
        },
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "web_source_ledger": web_source_rows(),
        "alloy_composition": alloy_composition_rows(),
        "alloy_proxy": material_proxy_rows(),
        "binding_blockers": binding_blocker_rows(),
        "projection_status": projection_status_rows(),
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
            for field in [
                "valid_for_claim",
                "claim_allowed",
                "valid_projection_row",
                "projection_ready",
                "gate_pass",
                "readout_corrected",
                "binding_decomposed",
            ]:
                if field in row and bool_string(row[field]) == "true":
                    bad.append(f"{path.name}:{index}:{field}=true")
    return not bad, "; ".join(bad) if bad else "all claim/projection/binding/readout flags remain false"


def alloy_rows_valid(rows: list[dict[str, str]]) -> tuple[bool, str]:
    bad: list[str] = []
    material_sums: dict[str, float] = {}
    for row in rows:
        try:
            material = row["material_id"]
            mass_fraction = float(row["mass_fraction"])
            a_context = float(row["A_context"])
            z_value = float(row["Z"])
            if mass_fraction <= 0:
                bad.append(f"{row['composition_id']}:mass_fraction<=0")
            if a_context <= z_value:
                bad.append(f"{row['composition_id']}:A<=Z")
            material_sums[material] = material_sums.get(material, 0.0) + mass_fraction
        except Exception as exc:
            bad.append(f"{row.get('composition_id', 'unknown')}:{exc}")
    for material, total in material_sums.items():
        if abs(total - 1.0) > 1e-12:
            bad.append(f"{material}:mass_fraction_sum={total}")
    return not bad, "; ".join(bad) if bad else "alloy rows numeric and mass fractions sum to unity"


def proxy_rows_valid(rows: list[dict[str, str]]) -> tuple[bool, str]:
    bad: list[str] = []
    required = {"AP1909_PtRh10", "AP1909_TA6V", "AP1909_TA6V_minus_PtRh10"}
    present = {row["proxy_id"] for row in rows}
    if not required.issubset(present):
        bad.append(f"missing={sorted(required - present)}")
    numeric_fields = [
        "Z_over_A_proxy",
        "N_over_A_proxy",
        "neutron_excess_proxy",
        "electron_rest_mass_fraction",
        "coulomb_formula_proxy",
        "A_bar_proxy",
    ]
    for row in rows:
        for field in numeric_fields:
            if row[field] == "not_applicable":
                continue
            try:
                value = float(row[field])
                if not math.isfinite(value):
                    bad.append(f"{row['proxy_id']}:{field}=nonfinite")
            except Exception as exc:
                bad.append(f"{row.get('proxy_id', 'unknown')}:{field}:{exc}")
    return not bad, "; ".join(bad) if bad else "proxy rows finite and include TA6V_minus_PtRh10 contrast"


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks: list[dict[str, Any]] = []
    source_rows_loaded = csv_rows(OUTPUTS["source_register"])
    checks.append(
        {
            "validation_id": "VAL1909_00_sources",
            "status": "PASS" if all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows_loaded) else "FAIL",
            "detail": "all local source paths exist and needles found",
            "valid_for_claim": False,
        }
    )
    alloy_ok, alloy_detail = alloy_rows_valid(csv_rows(OUTPUTS["alloy_composition"]))
    checks.append({"validation_id": "VAL1909_01_alloy_rows", "status": "PASS" if alloy_ok else "FAIL", "detail": alloy_detail, "valid_for_claim": False})
    proxy_ok, proxy_detail = proxy_rows_valid(csv_rows(OUTPUTS["alloy_proxy"]))
    checks.append({"validation_id": "VAL1909_02_proxy_rows", "status": "PASS" if proxy_ok else "FAIL", "detail": proxy_detail, "valid_for_claim": False})
    blockers = csv_rows(OUTPUTS["binding_blockers"])
    checks.append(
        {
            "validation_id": "VAL1909_03_blocker_ledger",
            "status": "PASS" if len(blockers) >= 6 and all("MISSING" in row["status"] for row in blockers) else "FAIL",
            "detail": "binding/source/readout blockers remain explicit",
            "valid_for_claim": False,
        }
    )
    projection = csv_rows(OUTPUTS["projection_status"])
    checks.append(
        {
            "validation_id": "VAL1909_04_projection_status",
            "status": "PASS" if any(row["row_id"] == "MP1909_3_verdict" and row["current_status"] == "ALLOY_PROXY_GAINED_MATERIAL_BINDING_PROJECTION_STILL_BLOCKED" for row in projection) else "FAIL",
            "detail": "projection remains blocked after alloy proxy gain",
            "valid_for_claim": False,
        }
    )
    gates = csv_rows(OUTPUTS["claim_gate"])
    checks.append(
        {
            "validation_id": "VAL1909_05_claim_gate",
            "status": "PASS" if any(row["gate_id"] == "CG1909_3_claim" and row["current_status"] == "CLAIM_BLOCKED" for row in gates) else "FAIL",
            "detail": "claim remains blocked",
            "valid_for_claim": False,
        }
    )
    next_rows = csv_rows(OUTPUTS["next_target"])
    checks.append(
        {
            "validation_id": "VAL1909_06_next_target",
            "status": "PASS" if any(row["route_id"] == "NEXT1909_0_primary" and row["selection_status"] == "selected" for row in next_rows) else "FAIL",
            "detail": "1910 parent response functional route selected",
            "valid_for_claim": False,
        }
    )
    flags_ok, flags_detail = claim_flags_safe(generated_without_validation)
    checks.append({"validation_id": "VAL1909_07_claim_flags_safe", "status": "PASS" if flags_ok else "FAIL", "detail": flags_detail, "valid_for_claim": False})
    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append({"validation_id": "VAL1909_08_csv_parse", "status": "PASS" if parse_ok else "FAIL", "detail": parse_detail, "valid_for_claim": False})
    checks.append({"validation_id": "VAL1909_09_branch_copies", "status": "PASS" if all(path.exists() for path in BRANCH_COPIES.values()) else "FAIL", "detail": "; ".join(str(path) for path in BRANCH_COPIES.values()), "valid_for_claim": False})
    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append({"validation_id": "VAL1909_10_pycache_absent", "status": "PASS" if not pycache.exists() else "FAIL", "detail": str(pycache), "valid_for_claim": False})
    formalization_hits = []
    if FORMALIZATION.exists():
        artifact_needles = [
            "1909-Y5-R2FR-TiPt-alloy",
            "P8_Y5_PARENT_QLOC_1909",
            "Y5_R2FR_TiPt_alloy_material_binding_projection_or_blocker_1909",
        ]
        formalization_hits = [
            path
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and any(needle in path.name for needle in artifact_needles)
        ]
    checks.append({"validation_id": "VAL1909_11_formalization_untouched", "status": "PASS" if not formalization_hits else "FAIL", "detail": f"formalization_1909_artifact_count={len(formalization_hits)}", "valid_for_claim": False})
    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append({"validation_id": "VAL1909_OVERALL", "status": "PASS" if fail_count == 0 else "FAIL", "detail": "1909 Ti/Pt alloy material-binding projection or blocker ledger", "valid_for_claim": False})
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1909 - Ti/Pt Alloy Material-Binding Projection Or Blocker Ledger

## Purpose

This checkpoint tries to upgrade the 1908 natural Ti/Pt element stub into the actual MICROSCOPE alloy/material branch. It succeeds only at the scaffold level: PtRh10 and TA6V alloy composition plus a differential proxy vector are now source-backed local nonclaim rows, but the binding/material response tensor and readout/source contraction remain absent.

## Result

- PtRh10 and TA6V alloy mass-fraction composition is now staged as source-backed context.
- The branch sign convention is locked to `TA6V_minus_PtRh10`, matching the existing MICROSCOPE WEP material convention rows.
- A single nonclaim proxy vector now carries `Z/A`, `N/A`, neutron-excess, electron-rest-mass, Coulomb-proxy, and `Abar` contrasts.
- Material-binding projection is explicitly blocked by six separated blockers.
- No WEP, local-GR, or material-response claim is promoted.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Web Source Ledger

{markdown_table(rows_by_name["web_source_ledger"])}

## Alloy Composition Rows

{markdown_table(rows_by_name["alloy_composition"])}

## Alloy Proxy Vector

{markdown_table(rows_by_name["alloy_proxy"])}

## Binding Projection Blocker Ledger

{markdown_table(rows_by_name["binding_blockers"])}

## Projection Status

{markdown_table(rows_by_name["projection_status"])}

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
