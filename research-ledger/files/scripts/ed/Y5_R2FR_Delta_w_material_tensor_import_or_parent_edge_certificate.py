from __future__ import annotations

import csv
import shutil
from decimal import Decimal
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
QUARANTINE = MICROSCOPE / "quarantine" / "1607"
INPUT = QUARANTINE / "input"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1607-Y5-R2FR-Delta_w-material-tensor-import-or-parent-edge-certificate.md"

SOURCE_FILES = {
    "1606_doc": ROOT / "1606-Y5-R2FR-parent-owned-matter-graph-or-Delta_w-component-bound-pack.md",
    "1606_validation": OUT / "P8_Y5_BRR545_1606_VALIDATION.csv",
    "1606_pack": OUT / "P8_Y5_PARENT_QLOC_1606_DELTA_W_COMPONENT_BOUND_PACK.csv",
    "1606_readiness": OUT / "P8_Y5_PARENT_QLOC_1606_DELTA_W_SCORE_READINESS.csv",
    "1606_edges": OUT / "P8_Y5_PARENT_QLOC_1606_PARENT_OWNED_EDGE_AUDIT.csv",
    "1606_next": OUT / "P8_Y5_PARENT_QLOC_1606_NEXT_TARGET.csv",
    "1595_bound_anchor": OUT / "P8_Y5_PARENT_QLOC_1595_SOURCE_BACKED_BETA_DELTAW_CANDIDATE.csv",
    "1595_claim_limits": OUT / "P8_Y5_PARENT_QLOC_1595_CANDIDATE_CLAIM_LIMITS.csv",
    "1595_next_inputs": OUT / "P8_Y5_PARENT_QLOC_1595_NEXT_INPUT_REQUIREMENTS.csv",
    "1481_material_context": COEFF / "WEP_material_context_pack_nonclaim_1481.csv",
    "1479_component_pack": COEFF / "component_delta_w_bound_pack_nonclaim_1479.csv",
    "983_constituents": OUT / "P8_Y5_R10_983_MATERIAL_CONSTITUENTS.csv",
    "1424_material_vectors": OUT / "P8_Y5_R10_1424_TIPT_MATERIAL_VECTOR_CANDIDATES.csv",
    "983_proxy_vectors": OUT / "P8_Y5_R10_983_MATERIAL_PROXY_CHARGE_VECTORS.csv",
    "1053_charge_matrix": OUT / "P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv",
    "1080_tensor_candidates": OUT / "P8_Y5_R10_1080_MATERIAL_COMPOSITION_AND_TENSOR_CANDIDATES.csv",
}

NEEDLES = {
    "1606_doc": ["POG1606_4_verdict", "PARENT_OWNED_GRAPH_NOT_DERIVED"],
    "1606_validation": ["VAL1606_OVERALL", "PASS"],
    "1606_pack": ["DWB1606_1_delta_w_e", "PROXY_UNIT_KERNEL_ONLY"],
    "1606_readiness": ["READY1606_5_verdict", "Delta_w branch score-ready"],
    "1606_edges": ["EDGE1606_7_verdict", "NOT_PARENT_CERTIFIED"],
    "1606_next": ["1607-Y5-R2FR-Delta_w-material-tensor-import-or-parent-edge-certificate.md", "parent material-response tensor"],
    "1595_bound_anchor": ["SBC1595_0_MICROSCOPE_Delta_w_tau_bound_anchor", "absolute product bound"],
    "1595_claim_limits": ["CLM1595_3_material_map_missing", "material map missing"],
    "1595_next_inputs": ["NIR1595_2_material_map", "Ti/Pt response tensor"],
    "1481_material_context": ["MAT1481_6_full_tensor", "MISSING_FULL_PARENT_MATERIAL_TENSOR"],
    "1479_component_pack": ["CBP1479_1_delta_w_e", "PROXY_UNIT_KERNEL_ONLY"],
    "983_constituents": ["M983_0_PtRh10", "M983_1_TiAlloy"],
    "1424_material_vectors": ["MAT1424_2_electron_mass_fraction", "AUDITED_NUMERIC_PARENT_NORMALIZATION_MISSING"],
    "983_proxy_vectors": ["M983_0_PtRh10", "proxy_charge_vector_computed"],
    "1053_charge_matrix": ["WCM1053_6", "MISSING_FULL_MATERIAL_TENSOR"],
    "1080_tensor_candidates": ["MAT1080_4_full_tensor_upgrade", "MISSING_FULL_MATERIAL_TENSOR"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1607_SOURCE_REGISTER.csv"
TENSOR_SCHEMA = OUT / "P8_Y5_PARENT_QLOC_1607_MATERIAL_TENSOR_IMPORT_SCHEMA.csv"
TENSOR_TEMPLATE = OUT / "P8_Y5_PARENT_QLOC_1607_MATERIAL_TENSOR_IMPORT_TEMPLATE.csv"
TENSOR_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1607_MATERIAL_TENSOR_CONTEXT_AUDIT.csv"
SENSITIVITY_PACK = OUT / "P8_Y5_PARENT_QLOC_1607_COMPONENT_SENSITIVITY_PACK.csv"
BOUND_INVERSION = OUT / "P8_Y5_PARENT_QLOC_1607_BOUND_INVERSION_AUDIT.csv"
PARENT_EDGE = OUT / "P8_Y5_PARENT_QLOC_1607_PARENT_EDGE_CERTIFICATE_STATUS.csv"
SCORE_READINESS = OUT / "P8_Y5_PARENT_QLOC_1607_SCORE_READINESS.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1607_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1607_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1607_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1607_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1607_VALIDATION.csv"

COPY_TARGETS = {
    TENSOR_SCHEMA: [
        QUARANTINE / "MATERIAL_TENSOR_IMPORT_SCHEMA_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_material_tensor_import_schema_nonclaim_1607.csv",
    ],
    TENSOR_TEMPLATE: [
        INPUT / "TiPt_parent_material_response_tensor_TEMPLATE.csv",
        BRANCH_RESIDUALS / "R2FR_material_tensor_import_template_nonclaim_1607.csv",
    ],
    TENSOR_AUDIT: [
        QUARANTINE / "MATERIAL_TENSOR_CONTEXT_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_material_tensor_context_audit_nonclaim_1607.csv",
    ],
    SENSITIVITY_PACK: [
        QUARANTINE / "COMPONENT_SENSITIVITY_PACK_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_component_sensitivity_pack_nonclaim_1607.csv",
    ],
    BOUND_INVERSION: [
        QUARANTINE / "BOUND_INVERSION_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_bound_inversion_audit_nonclaim_1607.csv",
    ],
    PARENT_EDGE: [
        QUARANTINE / "PARENT_EDGE_CERTIFICATE_STATUS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_parent_edge_certificate_status_nonclaim_1607.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1607.csv",
    ],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (source_id, path) in enumerate(SOURCE_FILES.items()):
        text = read_text(path) if path.exists() else ""
        needles = NEEDLES[source_id]
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1607_{index}_{source_id}",
                "source_path": rel(path) if path.exists() else str(path),
                "exists": path.exists(),
                "needle_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "source_role": "1607_material_tensor_import_or_parent_edge_certificate_input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def tensor_schema_rows() -> list[dict[str, Any]]:
    fields = [
        ("row_id", "stable tensor row id"),
        ("composition_pair", "TA6V_minus_PtRh10 or declared source/test pair"),
        ("component", "electron|EM_Coulomb|light_quark|QCD_gluon|nuclear_binding|measure_J|current_c|nonHilbert_zeta|other_parent_component"),
        ("sensitivity_value", "finite numeric tensor component or DERIVED_ZERO"),
        ("sensitivity_uncertainty", "numeric uncertainty/interval or exact theorem tag"),
        ("units", "dimensionless sensitivity in declared MTS parent WEP basis"),
        ("sign_convention", "TA6V_minus_PtRh10 and positive-couples-stronger convention"),
        ("basis", "MTS parent material-response basis; external DD smoke basis must be labelled proxy"),
        ("source_path", "local artifact, DOI, or URL; local path must exist"),
        ("source_anchor", "row/table/equation anchor"),
        ("parent_owner_status", "PARENT_OWNED|SOURCE_BACKED_CONTEXT|PROXY_NONCLAIM|MISSING"),
        ("no_bound_inversion", "true for claim-grade rows; false/templates rejected"),
        ("no_double_counting_rule", "states component independence/covariance rule"),
        ("valid_for_claim", "false until full tensor, tau, source/readout and component gates pass"),
        ("claim_allowed", "false until full local branch gates pass"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "schema_id": f"MTS1607_{index}_{field}",
            "field": field,
            "required_policy": policy,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for index, (field, policy) in enumerate(fields)
    ]


def tensor_template_rows() -> list[dict[str, Any]]:
    components = ["electron", "EM_Coulomb", "light_quark", "QCD_gluon", "nuclear_binding", "measure_J", "current_c", "nonHilbert_zeta"]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": f"MTT1607_{index}_{component}",
            "composition_pair": "TA6V_minus_PtRh10",
            "component": component,
            "sensitivity_value": "MISSING_PARENT_MATERIAL_TENSOR_COMPONENT",
            "sensitivity_uncertainty": "MISSING_UNCERTAINTY_OR_EXACT",
            "units": "dimensionless",
            "sign_convention": "TA6V_minus_PtRh10; positive means TA6V couples stronger than PtRh10 in declared parent source basis",
            "basis": "MISSING_MTS_PARENT_WEP_MATERIAL_RESPONSE_BASIS",
            "source_path": "MISSING_SOURCE_PATH",
            "source_anchor": "MISSING_ROW_TABLE_EQUATION",
            "parent_owner_status": "MISSING",
            "no_bound_inversion": False,
            "no_double_counting_rule": "MISSING_COMPONENT_COVARIANCE_OR_INDEPENDENCE_RULE",
            "parser_status": "TEMPLATE_ONLY_NOT_IMPORTABLE",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for index, component in enumerate(components)
    ]


def tensor_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "MTA1607_0_pair_convention",
            "object": "MICROSCOPE Ti/Pt pair convention",
            "value_or_status": "TA6V_minus_PtRh10",
            "source_path": "source-intake/microscope/branch_locked_wep/coefficients/WEP_material_context_pack_nonclaim_1481.csv",
            "source_anchor": "MAT1481_0_pair_convention",
            "usable_level": "CONTEXT_ONLY",
            "why_not_claim": "pair convention does not supply parent material-response tensor",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "MTA1607_1_composition",
            "object": "PtRh10 and TA6V alloy mass fractions",
            "value_or_status": "PtRh10=Pt0.90/Rh0.10;TA6V=Ti0.90/Al0.06/V0.04",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_983_MATERIAL_CONSTITUENTS.csv",
            "source_anchor": "M983_0_PtRh10;M983_1_TiAlloy",
            "usable_level": "SOURCE_BACKED_COMPOSITION_CONTEXT",
            "why_not_claim": "composition is not an MTS parent response tensor",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "MTA1607_2_electron_fraction_proxy",
            "object": "electron rest-mass fraction contrast",
            "value_or_status": "3.129116287420e-05",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1424_TIPT_MATERIAL_VECTOR_CANDIDATES.csv",
            "source_anchor": "MAT1424_2_electron_mass_fraction",
            "usable_level": "AUDITED_NUMERIC_PROXY",
            "why_not_claim": "parent mass functional and source/readout/tau normalization missing",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "MTA1607_3_DD_alpha_smoke",
            "object": "external DD alpha/Coulomb contrast",
            "value_or_status": "-1.989808886825e-03",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv",
            "source_anchor": "WCM1053_4",
            "usable_level": "EXTERNAL_SMOKE_NUMERIC_NOT_PARENT_BASIS",
            "why_not_claim": "MTS parent EM/Coulomb owner and basis map missing",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "MTA1607_4_DD_surface_smoke",
            "object": "external DD surface/binding contrast",
            "value_or_status": "-3.306456347405e-03",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv",
            "source_anchor": "WCM1053_5",
            "usable_level": "EXTERNAL_SMOKE_NUMERIC_NOT_FULL_TENSOR",
            "why_not_claim": "full nuclear/isotopic tensor and MTS basis map missing",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "MTA1607_5_full_tensor",
            "object": "full R_TA6V_minus_PtRh10 material tensor",
            "value_or_status": "MISSING_FULL_PARENT_MATERIAL_TENSOR",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1080_MATERIAL_COMPOSITION_AND_TENSOR_CANDIDATES.csv",
            "source_anchor": "MAT1080_4_full_tensor_upgrade",
            "usable_level": "BLOCKED",
            "why_not_claim": "parent response basis, isotope/alloy averaging, component covariance and source/readout environment stack missing",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def sensitivity_pack_rows() -> list[dict[str, Any]]:
    rows = [
        ("SEN1607_0_electron", "electron", "3.129116287420e-05", "AUDITED_NUMERIC_PROXY_PARENT_NORMALIZATION_MISSING", "MAT1424_2_electron_mass_fraction", "electron rest-mass fraction contrast; not parent mass functional"),
        ("SEN1607_1_EM_Coulomb", "EM_Coulomb", "-1.989808886825e-03", "DD_SMOKE_NOT_MTS_PARENT_BASIS", "WCM1053_4", "external DD Coulomb smoke contrast only"),
        ("SEN1607_2_nuclear_surface", "nuclear_binding", "-3.306456347405e-03", "DD_SMOKE_NOT_FULL_TENSOR", "WCM1053_5", "external DD surface/binding smoke contrast only"),
        ("SEN1607_3_light_quark", "light_quark", "MISSING_PARENT_COMPONENT_SENSITIVITY", "MISSING", "MAT1080_4_full_tensor_upgrade", "light-quark/sigma material sensitivity not sourced"),
        ("SEN1607_4_QCD_gluon", "QCD_gluon", "MISSING_PARENT_COMPONENT_SENSITIVITY", "MISSING", "MAT1080_4_full_tensor_upgrade", "QCD/gluon/bulk material sensitivity not sourced"),
        ("SEN1607_5_measure_J", "measure_J", "MISSING_PARENT_COMPONENT_SENSITIVITY", "MISSING", "MAT1080_4_full_tensor_upgrade", "species-measure/Jacobian sensitivity not sourced"),
        ("SEN1607_6_current_c", "current_c", "MISSING_PARENT_COMPONENT_SENSITIVITY", "MISSING", "MAT1080_4_full_tensor_upgrade", "current/source normalization sensitivity not sourced"),
        ("SEN1607_7_nonHilbert_zeta", "nonHilbert_zeta", "MISSING_PARENT_COMPONENT_SENSITIVITY", "MISSING", "MAT1080_4_full_tensor_upgrade", "non-Hilbert/readout sensitivity not sourced"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "sensitivity_id": sensitivity_id,
            "composition_pair": "TA6V_minus_PtRh10",
            "component": component,
            "sensitivity_value": value,
            "sensitivity_uncertainty": "MISSING_CLAIM_GRADE_UNCERTAINTY",
            "units": "dimensionless",
            "basis": "MTS_PARENT_BASIS_MISSING_OR_PROXY_LABELLED",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1080_MATERIAL_COMPOSITION_AND_TENSOR_CANDIDATES.csv",
            "source_anchor": anchor,
            "status": status,
            "why_not_claim": why_not_claim,
            "no_bound_inversion": True,
            "no_double_counting_rule": "MISSING_FULL_COVARIANCE_OR_COMPONENT_INDEPENDENCE_RULE",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for sensitivity_id, component, value, status, anchor, why_not_claim in rows
    ]


def bound_inversion_rows() -> list[dict[str, Any]]:
    electron_fraction = Decimal("3.129116287420e-05")
    delta_w_e_proxy = Decimal("8.948213306283e-11")
    product = electron_fraction * delta_w_e_proxy
    anchor = Decimal("2.8e-15")
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "BIA1607_0_electron_proxy_product",
            "formula": "abs(DeltaF_e_TiPt * delta_w_e_proxy)",
            "inputs": "DeltaF_e=3.129116287420e-05;delta_w_e_proxy=8.948213306283e-11",
            "computed_value": f"{product:.15E}",
            "comparison_anchor": "MICROSCOPE product-bound anchor 2.8e-15",
            "relative_difference": f"{abs(product - anchor) / anchor:.15E}",
            "status": "BOUND_INVERSION_PROXY_DETECTED",
            "effect": "may be used as nonclaim smoke/validator check only, not as MTS prediction",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "BIA1607_1_missing_tau",
            "formula": "abs(Delta_w_TiPt*tau_WEP) <= bound cannot become abs(Delta_w_TiPt) <= bound/tau without tau_WEP",
            "inputs": "tau_WEP=MISSING",
            "computed_value": "NOT_COMPUTABLE",
            "comparison_anchor": "NIR1595_0_tau_WEP",
            "relative_difference": "N/A",
            "status": "TAU_WEP_MISSING_BLOCKS_BOUND_INVERSION",
            "effect": "Delta_w prior width remains blocked",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "BIA1607_2_material_map_missing",
            "formula": "Delta_w_TiPt = DeltaF_TiPt dot delta_w_component_vector + residuals",
            "inputs": "DeltaF_TiPt_FULL_PARENT_TENSOR=MISSING",
            "computed_value": "NOT_COMPUTABLE",
            "comparison_anchor": "NIR1595_2_material_map;MAT1481_6_full_tensor",
            "relative_difference": "N/A",
            "status": "FULL_MATERIAL_TENSOR_MISSING",
            "effect": "no WEP material score",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def parent_edge_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "edge_id": "PEC1607_0_parent_edge_certificate",
            "target": "prove QED/QCD/Yukawa/binding/material edges are parent-owned L_action morphisms",
            "current_status": "NOT_DERIVED",
            "evidence": "1606 edge audit remains physical-template/partial only",
            "effect": "cannot theorem-zero Delta_w_component_vector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "edge_id": "PEC1607_1_material_tensor_vs_edge",
            "target": "use material tensor as finite route, not graph-zero proof",
            "current_status": "FINITE_ROUTE_ONLY",
            "evidence": "source-backed/proxy material sensitivities do not certify parent-owned morphisms",
            "effect": "material import can bound components but cannot by itself collapse w_A to w_*",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "edge_id": "PEC1607_2_verdict",
            "target": "parent edge certificate route",
            "current_status": "PARENT_EDGE_CERTIFICATE_MISSING",
            "evidence": "no explicit parent action graph source file or theorem imported",
            "effect": "continue finite vector route or source parent-edge theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def score_readiness_rows() -> list[dict[str, Any]]:
    rows = [
        ("READY1607_0_full_tensor", "full parent material-response tensor", False, "MAT1080_4/MAT1481_6 remain MISSING_FULL_PARENT_MATERIAL_TENSOR"),
        ("READY1607_1_component_sensitivities", "all component sensitivities numeric or theorem-zero", False, "electron/EM/nuclear are proxy/smoke; light-quark/QCD/measure/current/NH missing"),
        ("READY1607_2_bound_inversion", "no bound-inverted component proxies", False, "electron proxy product equals MICROSCOPE bound anchor"),
        ("READY1607_3_tau_readout", "tau_WEP/source worldtube/readout kernel exists", False, "NIR1595 tau/source/readout requirements remain open"),
        ("READY1607_4_parent_edges", "parent-owned edge certificate exists", False, "PEC1607 keeps edge route missing"),
        ("READY1607_5_verdict", "Delta_w material branch score-ready", False, "full tensor/component/tau/readout/edge gates open"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "readiness_id": readiness_id,
            "requirement": requirement,
            "ready": ready,
            "blocker": blocker,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for readiness_id, requirement, ready, blocker in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1607_0_material_tensor_import",
            "acceptance_rule": "material tensor import must supply all declared component sensitivities, units, sign, MTS parent basis, source anchors, covariance/no-double-counting rule",
            "input_state": "context/proxy/smoke rows only; full parent tensor missing",
            "runner_result": "MATERIAL_TENSOR_NOT_SCORE_READY",
            "effect": "finite Delta_w_TiPt score blocked",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1607_1_bound_inversion_firewall",
            "acceptance_rule": "component values derived from empirical bound inversion cannot be treated as theory predictions",
            "input_state": "electron proxy product reconstructs 2.8e-15 bound",
            "runner_result": "REJECT_BOUND_INVERTED_PROXY_AS_PREDICTION",
            "effect": "electron proxy retained only as nonclaim smoke check",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1607_2_parent_edge_certificate",
            "acceptance_rule": "parent edge certificate must be an explicit parent action graph theorem/source, not physical connectedness alone",
            "input_state": "no parent-edge source imported",
            "runner_result": "REJECT_PARENT_EDGE_THEOREM_ZERO",
            "effect": "no Delta_w theorem-zero",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG1607_0_material_tensor", "full Ti/Pt parent material-response tensor", "BLOCKED", "full tensor missing; proxies/smoke only"),
        ("CG1607_1_component_sensitivities", "component sensitivity pack score", "BLOCKED", "not all components sourced/numeric/theorem-zero"),
        ("CG1607_2_bound_firewall", "bound-inverted proxy as prediction", "BLOCKED", "electron proxy reconstructs product bound"),
        ("CG1607_3_parent_edges", "parent-owned graph theorem-zero", "BLOCKED", "no parent edge certificate"),
        ("CG1607_4_tau_readout", "tau_WEP/source/readout projection", "BLOCKED", "tau/source/readout kernel still missing"),
        ("CG1607_5_WEP_local_GR", "WEP/Newton/local-GR claim", "BLOCKED", "material/tau/coupling gates open"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, status, reason in gates
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1607_0_material_route",
            "decision": "MATERIAL_TENSOR_CONTEXT_READY_FULL_TENSOR_MISSING",
            "reason": "composition/proxy/smoke rows exist, but not a full MTS parent material-response tensor",
            "next_action": "source/import claim-safe Ti/Pt parent material tensor or keep material score blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1607_1_bound_proxy",
            "decision": "BOUND_INVERTED_ELECTRON_PROXY_QUARANTINED",
            "reason": "electron sensitivity times delta_w_e proxy reconstructs the 2.8e-15 empirical bound",
            "next_action": "do not treat electron proxy as prediction; require parent coefficient or independent source-backed component value",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1607_2_next",
            "decision": "NEXT_1608_TAU_WEP_READOUT_KERNEL_OR_MATERIAL_TENSOR_SOURCE_FILE",
            "reason": "material tensor remains missing, and tau/source/readout is required before any bound or material row becomes a WEP score",
            "next_action": "derive/source tau_WEP and readout kernel, or import a real Ti/Pt parent material tensor file into the 1607 input schema",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1608-Y5-R2FR-tau-WEP-readout-kernel-or-material-tensor-source-file.md",
            "script": "scripts/Y5_R2FR_tau_WEP_readout_kernel_or_material_tensor_source_file.py",
            "objective": "derive/source tau_WEP and MICROSCOPE readout/source projection, or import a real Ti/Pt parent material tensor through the 1607 schema",
            "success_condition": "claim-safe nonclaim tau/readout/material input that is independent of bound inversion, with units/sign/source anchors; no WEP/local-GR claim until all gates pass",
            "do_not": "do not use bound inversion, tau_eff=1, DD-only proxies, physical connectedness alone, closure-only zero, measured-G absorption, or public/local-GR claims",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def csv_parses(paths: list[Path]) -> bool:
    try:
        for path in paths:
            read_csv(path)
    except Exception:
        return False
    return True


def no_claim_flags(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            for field in ("score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if truthy(row.get(field, "")):
                    return False
    return True


def no_formalization_1607() -> bool:
    if not FORMALIZATION.exists():
        return True
    artifact_markers = (
        "1607-Y5",
        "P8_Y5_PARENT_QLOC_1607",
        "P8_Y5_BRR545_1607",
        "Y5_R2FR_Delta_w_material_tensor_import_or_parent_edge_certificate",
        "R2FR_material_tensor",
    )
    return not any(any(marker in path.name for marker in artifact_markers) for path in FORMALIZATION.rglob("*"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    schema = read_csv(TENSOR_SCHEMA)
    template = read_csv(TENSOR_TEMPLATE)
    audit = read_csv(TENSOR_AUDIT)
    sensitivities = read_csv(SENSITIVITY_PACK)
    bound = read_csv(BOUND_INVERSION)
    edges = read_csv(PARENT_EDGE)
    readiness = read_csv(SCORE_READINESS)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    copies = [target for targets in COPY_TARGETS.values() for target in targets]
    checks = [
        ("VAL1607_0_sources_exist", all(truthy(row["exists"]) for row in sources), "all cited 1607 local source paths exist"),
        ("VAL1607_1_needles_found", all(truthy(row["needle_found"]) for row in sources), "all required 1607 source needles found"),
        ("VAL1607_2_tensor_schema", len(schema) >= 10 and any(row["field"] == "no_double_counting_rule" for row in schema), "material tensor import schema written"),
        ("VAL1607_3_template_nonimportable", template and all(row["parser_status"] == "TEMPLATE_ONLY_NOT_IMPORTABLE" for row in template), "material tensor template remains nonimportable"),
        ("VAL1607_4_full_tensor_missing", any(row["audit_id"] == "MTA1607_5_full_tensor" and row["usable_level"] == "BLOCKED" for row in audit), "full parent material tensor remains missing"),
        ("VAL1607_5_sensitivities_nonclaim", sensitivities and all(row["claim_allowed"].lower() == "false" for row in sensitivities), "component sensitivity rows remain nonclaim"),
        ("VAL1607_6_bound_inversion_detected", any(row["audit_id"] == "BIA1607_0_electron_proxy_product" and row["status"] == "BOUND_INVERSION_PROXY_DETECTED" for row in bound), "electron proxy bound inversion detected"),
        ("VAL1607_7_parent_edge_missing", any(row["edge_id"] == "PEC1607_2_verdict" and row["current_status"] == "PARENT_EDGE_CERTIFICATE_MISSING" for row in edges), "parent edge certificate remains missing"),
        ("VAL1607_8_score_not_ready", any(row["readiness_id"] == "READY1607_5_verdict" and row["ready"].lower() == "false" for row in readiness), "Delta_w material branch remains not score-ready"),
        ("VAL1607_9_runner_refuses_claims", any(row["runner_id"] == "RUN1607_1_bound_inversion_firewall" and row["runner_result"] == "REJECT_BOUND_INVERTED_PROXY_AS_PREDICTION" for row in runner), "runner refuses bound-inverted proxy as prediction"),
        ("VAL1607_10_claim_gates_closed", gates and all(row["claim_allowed"].lower() == "false" and row["status"] == "BLOCKED" for row in gates), "all 1607 claim gates remain closed"),
        ("VAL1607_11_decision_next", any(row["decision"] == "NEXT_1608_TAU_WEP_READOUT_KERNEL_OR_MATERIAL_TENSOR_SOURCE_FILE" for row in decisions), "decision selects 1608 tau/readout or material tensor source file"),
        ("VAL1607_12_csv_parse", csv_parses(generated_csvs), "all generated 1607 CSVs parse"),
        ("VAL1607_13_claim_safety_flags", no_claim_flags(generated_csvs), "no generated 1607 rows are score-ready, prediction rows, valid-for-claim, or claim-allowed"),
        ("VAL1607_14_branch_copies", all(path.exists() for path in copies), "branch/quarantine nonclaim copies exist"),
        ("VAL1607_15_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1607_16_formalization_untouched", no_formalization_1607(), "no 1607 outputs found under formalization-workbench"),
    ]
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if ok else "FAIL",
            "detail": detail,
        }
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1607_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1607 Delta_w material tensor import or parent edge certificate validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "/") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    schema: list[dict[str, Any]],
    template: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    sensitivities: list[dict[str, Any]],
    bound: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    readiness: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1607 - R2/fR Delta_w Material Tensor Import Or Parent Edge Certificate",
                "## Verdict\n"
                "- 1607 audits the finite `Delta_w` material route instead of trying to zero the coupling by physical connectedness alone.\n"
                "- The current corpus has useful Ti/Pt composition context plus electron, Coulomb, and surface/binding proxy/smoke sensitivities, but not a full MTS parent material-response tensor.\n"
                "- The electron proxy is explicitly quarantined: `DeltaF_e * delta_w_e_proxy` reconstructs the `2.8e-15` MICROSCOPE product-bound anchor, so it is bound-inverted smoke, not a prediction.\n"
                "- Parent-edge certificate route remains open but unproved; material tensor rows can bound finite residuals but cannot by themselves theorem-zero `Delta_w_A`.\n"
                "- No WEP, R10, PPN, clock, orbital, Newton, local-GR, beta/coupling, or public claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## Material Tensor Import Schema",
                md_table(schema, ["schema_id", "field", "required_policy"]),
                "## Material Tensor Import Template",
                md_table(template, ["row_id", "component", "sensitivity_value", "basis", "parser_status"]),
                "## Material Tensor Context Audit",
                md_table(audit, ["audit_id", "object", "value_or_status", "usable_level", "why_not_claim"]),
                "## Component Sensitivity Pack",
                md_table(sensitivities, ["sensitivity_id", "component", "sensitivity_value", "status", "why_not_claim"]),
                "## Bound-Inversion Audit",
                md_table(bound, ["audit_id", "formula", "computed_value", "comparison_anchor", "status", "effect"]),
                "## Parent Edge Certificate Status",
                md_table(edges, ["edge_id", "target", "current_status", "effect"]),
                "## Score Readiness",
                md_table(readiness, ["readiness_id", "requirement", "ready", "blocker"]),
                "## Runner Refusal",
                md_table(runner, ["runner_id", "acceptance_rule", "input_state", "runner_result", "effect"]),
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "reason", "next_action"]),
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "success_condition", "do_not"]),
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    INPUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    schema = tensor_schema_rows()
    template = tensor_template_rows()
    audit = tensor_audit_rows()
    sensitivities = sensitivity_pack_rows()
    bound = bound_inversion_rows()
    edges = parent_edge_rows()
    readiness = score_readiness_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        TENSOR_SCHEMA,
        TENSOR_TEMPLATE,
        TENSOR_AUDIT,
        SENSITIVITY_PACK,
        BOUND_INVERSION,
        PARENT_EDGE,
        SCORE_READINESS,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(TENSOR_SCHEMA, schema)
    write_csv(TENSOR_TEMPLATE, template)
    write_csv(TENSOR_AUDIT, audit)
    write_csv(SENSITIVITY_PACK, sensitivities)
    write_csv(BOUND_INVERSION, bound)
    write_csv(PARENT_EDGE, edges)
    write_csv(SCORE_READINESS, readiness)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, schema, template, audit, sensitivities, bound, edges, readiness, runner, gates, decisions, next_rows, validation)


if __name__ == "__main__":
    main()
