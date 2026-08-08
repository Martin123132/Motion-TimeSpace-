from __future__ import annotations

import csv
import shutil
from collections import defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
QUARANTINE = MICROSCOPE / "quarantine" / "1477"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1477-Y5-R10-RAB-connected-matter-graph-certificate-or-delta-w-input-schema-runner.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
START_TS = datetime.now(timezone.utc).timestamp()

PREV_NEXT = OUT / "P8_Y5_R10_1476_NEXT_TARGET.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1476_VALIDATION.csv"
PREV_PROOF = OUT / "P8_Y5_R10_1476_SOURCE_LABEL_FORGETTING_PROOF_ATTEMPT.csv"
PREV_PREMISE = OUT / "P8_Y5_R10_1476_SOURCE_LABEL_PREMISE_AUDIT.csv"
PREV_DELTAW = OUT / "P8_Y5_R10_1476_DELTA_W_SOURCE_WEIGHT_INPUT_ROW_NONCLAIM.csv"
PREV_EVALUATOR = OUT / "P8_Y5_R10_1476_CI_SOURCE_WEIGHT_EVALUATOR_UPDATE.csv"
CONNECTED_1463 = OUT / "P8_Y5_R10_1463_CONNECTED_MATTER_NATURALITY_AUDIT.csv"
CONNECTED_1464 = OUT / "P8_Y5_R10_1464_CONNECTED_MATTER_CATEGORY_PROOF_ATTEMPT.csv"
CONNECTED_1231 = OUT / "P8_Y5_R10_1231_MATTER_CATEGORY_CONNECTEDNESS_ATTEMPT.csv"
STACK_1231 = OUT / "P8_Y5_R10_1231_SOURCE_LABEL_FORGETTING_PROOF_STACK.csv"
SOURCE_COUPLING_1229 = OUT / "P8_Y5_R10_1229_LOCAL_GR_SOURCE_COUPLING_THEOREM_CONTRACT.csv"
WEP_OWNER_1077 = OUT / "P8_Y5_R10_1077_PARENT_WEP_COUPLING_OWNER_THEOREM_ATTEMPT.csv"
MEASURE_CURRENT_1452 = OUT / "P8_Y5_R10_1452_COMMON_MEASURE_CURRENT_THEOREM_ATTEMPT.csv"
CURRENT_AUDIT_1452 = OUT / "P8_Y5_R10_1452_CURRENT_OWNER_AUDIT.csv"
NO_RELATIVE_1461 = OUT / "P8_Y5_R10_1461_NO_RELATIVE_SOURCE_LABEL_AUDIT.csv"
COUNTER_1461 = OUT / "P8_Y5_R10_1461_SOURCE_LABEL_COUNTERMODEL_AUDIT.csv"
TAU_SCHEMA_1067 = OUT / "P8_Y5_R10_1067_TAU_WEP_ACQUISITION_SCHEMA.csv"
SOURCE_SCALAR_1066 = OUT / "P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv"

GRAPH_NODES = OUT / "P8_Y5_R10_1477_CONNECTED_MATTER_GRAPH_NODES.csv"
GRAPH_EDGES = OUT / "P8_Y5_R10_1477_CONNECTED_MATTER_GRAPH_EDGES.csv"
GRAPH_CERTIFICATE = OUT / "P8_Y5_R10_1477_CONNECTED_MATTER_GRAPH_CERTIFICATE.csv"
ACTION_LINE_AUDIT = OUT / "P8_Y5_R10_1477_ACTION_DENSITY_LINE_OWNER_AUDIT.csv"
DIRECT_SUM_LEDGER = OUT / "P8_Y5_R10_1477_DIRECT_SUM_OBSTRUCTION_LEDGER.csv"
DELTAW_SCHEMA = OUT / "P8_Y5_R10_1477_DELTA_W_TAU_WEP_SCHEMA_V2.csv"
INPUT_TEMPLATE = OUT / "P8_Y5_R10_1477_DELTA_W_TAU_WEP_INPUT_TEMPLATE_NONCLAIM.csv"
EVALUATOR_RULES = OUT / "P8_Y5_R10_1477_CI_SOURCE_WEIGHT_EVALUATOR_RULES_V2.csv"
REDUCTION_GATES = OUT / "P8_Y5_R10_1477_REDUCTION_GATES.csv"
SOURCE_REGISTER = OUT / "P8_Y5_R10_1477_SOURCE_REGISTER.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1477_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1477_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1477_VALIDATION.csv"

QUAR_GRAPH = QUARANTINE / "CONNECTED_MATTER_GRAPH_CERTIFICATE_NONCLAIM.csv"
QUAR_SCHEMA = QUARANTINE / "DELTA_W_TAU_WEP_SCHEMA_V2_NONCLAIM.csv"
BRANCH_GRAPH = COEFF / "connected_matter_graph_certificate_nonclaim_1477.csv"
BRANCH_SCHEMA = COEFF / "delta_w_tau_wep_schema_v2_nonclaim_1477.csv"
BRANCH_GATES = COEFF / "source_weight_reduction_gates_1477.csv"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def parse_csv(path: Path) -> bool:
    with path.open(newline="", encoding="utf-8") as handle:
        list(csv.DictReader(handle))
    return True


def copy_nonclaim(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


def source_rows() -> list[dict[str, Any]]:
    sources = [
        ("SRC1477_0_prev_next", PREV_NEXT, "1476 handoff selecting connected matter graph or schema hardening"),
        ("SRC1477_1_prev_validation", PREV_VALIDATION, "1476 validation baseline"),
        ("SRC1477_2_prev_proof", PREV_PROOF, "conditional source-label forgetting theorem attempt"),
        ("SRC1477_3_prev_premise", PREV_PREMISE, "open premise ledger for source-label forgetting"),
        ("SRC1477_4_prev_deltaw", PREV_DELTAW, "nonclaim delta_w input row emitted by 1476"),
        ("SRC1477_5_prev_evaluator", PREV_EVALUATOR, "CI1474_1 evaluator status from 1476"),
        ("SRC1477_6_connected_1463", CONNECTED_1463, "connected matter naturality audit"),
        ("SRC1477_7_connected_1464", CONNECTED_1464, "connected category proof attempt"),
        ("SRC1477_8_connected_1231", CONNECTED_1231, "older matter category connectedness attempt"),
        ("SRC1477_9_stack_1231", STACK_1231, "source-label forgetting proof stack"),
        ("SRC1477_10_source_coupling_1229", SOURCE_COUPLING_1229, "local-GR source coupling theorem contract"),
        ("SRC1477_11_wep_owner_1077", WEP_OWNER_1077, "parent WEP coupling owner theorem attempt"),
        ("SRC1477_12_measure_current_1452", MEASURE_CURRENT_1452, "measure/current theorem attempt"),
        ("SRC1477_13_current_audit_1452", CURRENT_AUDIT_1452, "current owner audit"),
        ("SRC1477_14_no_relative_1461", NO_RELATIVE_1461, "no relative source-label audit"),
        ("SRC1477_15_counter_1461", COUNTER_1461, "source-label countermodel audit"),
        ("SRC1477_16_tau_schema_1067", TAU_SCHEMA_1067, "tau_WEP acquisition schema"),
        ("SRC1477_17_source_scalar_1066", SOURCE_SCALAR_1066, "source scalar exclusion/naturality route"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "source_id": source_id,
            "path_or_url": rel(path),
            "exists": path.exists(),
            "usage": usage,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path, usage in sources
    ]


def graph_node_rows() -> list[dict[str, Any]]:
    nodes = [
        ("N1477_0_L_parent", "single ordinary matter action-density line", "action_owner", "L_matter_parent", "would make relative source weights illegal if parent-signed"),
        ("N1477_1_electron_lepton", "electron/lepton sector", "ordinary_matter", "w_lepton", "WEP/clock/test-body matter contains electron rest and binding contributions"),
        ("N1477_2_photon_EM", "photon/EM field sector", "ordinary_matter", "w_EM", "atomic/nuclear binding and charge readout communicate through EM"),
        ("N1477_3_quark_flavour", "light quark sector", "ordinary_matter", "w_quark", "nuclear masses and composition dependence depend on light-quark content"),
        ("N1477_4_gluon_QCD", "gluon/QCD binding sector", "ordinary_matter", "w_QCD", "dominant hadronic mass and nuclear binding channel"),
        ("N1477_5_nuclear_bound_state", "nuclear bound-state sector", "composite_matter", "w_nuclear", "Ti/Pt source bodies sample nuclear binding and isotope content"),
        ("N1477_6_atomic_bound_state", "atomic bound-state sector", "composite_matter", "w_atomic", "laboratory matter and clocks use atoms, molecules, and EM binding"),
        ("N1477_7_macroscopic_test_body", "macroscopic ordinary test/source body", "composite_matter", "w_body", "WEP/PPN/orbital observables see integrated ordinary matter stress"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "node_id": node_id,
            "node": node,
            "node_type": node_type,
            "source_weight_symbol": symbol,
            "why_source_relevant": why,
            "candidate_graph_role": "template_node",
            "parent_owned_status": "MISSING_PARENT_ACTION_GRAPH_SIGNATURE" if node_id != "N1477_0_L_parent" else "MISSING_SINGLE_PARENT_ACTION_DENSITY_LINE",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for node_id, node, node_type, symbol, why in nodes
    ]


def graph_edge_rows() -> list[dict[str, Any]]:
    edges = [
        ("E1477_0_L_to_lepton", "N1477_0_L_parent", "N1477_1_electron_lepton", "ordinary matter action line includes lepton kinetic/mass term", "single parent L_matter term"),
        ("E1477_1_L_to_EM", "N1477_0_L_parent", "N1477_2_photon_EM", "ordinary matter/gauge action line includes EM field/current channel", "single parent L_matter/gauge term"),
        ("E1477_2_L_to_quark", "N1477_0_L_parent", "N1477_3_quark_flavour", "ordinary matter action line includes quark kinetic/mass term", "single parent L_matter term"),
        ("E1477_3_L_to_gluon", "N1477_0_L_parent", "N1477_4_gluon_QCD", "ordinary matter/gauge action line includes QCD field/current channel", "single parent L_matter/gauge term"),
        ("E1477_4_lepton_EM", "N1477_1_electron_lepton", "N1477_2_photon_EM", "electron-photon minimal coupling links lepton and EM source components", "parent-owned gauge-current morphism"),
        ("E1477_5_quark_EM", "N1477_3_quark_flavour", "N1477_2_photon_EM", "charged quarks link quark and EM source components", "parent-owned representation charge morphism"),
        ("E1477_6_quark_gluon", "N1477_3_quark_flavour", "N1477_4_gluon_QCD", "QCD coupling links quark and gluon binding source components", "parent-owned QCD morphism"),
        ("E1477_7_qcd_nucleus", "N1477_3_quark_flavour", "N1477_5_nuclear_bound_state", "light-quark content participates in nuclear bound states", "parent-owned bound-state map"),
        ("E1477_8_gluon_nucleus", "N1477_4_gluon_QCD", "N1477_5_nuclear_bound_state", "gluon/QCD binding participates in nuclear bound states", "parent-owned bound-state map"),
        ("E1477_9_nucleus_atom", "N1477_5_nuclear_bound_state", "N1477_6_atomic_bound_state", "nuclei bind to electrons through atomic EM structure", "parent-owned composite map"),
        ("E1477_10_lepton_atom", "N1477_1_electron_lepton", "N1477_6_atomic_bound_state", "electrons participate in atomic bound states", "parent-owned composite map"),
        ("E1477_11_atom_body", "N1477_6_atomic_bound_state", "N1477_7_macroscopic_test_body", "atoms compose laboratory test/source bodies", "parent-owned coarse-graining map"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "edge_id": edge_id,
            "source_node": source,
            "target_node": target,
            "candidate_morphism": morphism,
            "needed_parent_signature": needed,
            "template_edge_present": True,
            "parent_owned": False,
            "parent_owned_status": "PHYSICAL_TEMPLATE_NOT_PARENT_SIGNED",
            "blocks_claim_if_missing": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for edge_id, source, target, morphism, needed in edges
    ]


def connected_components(nodes: list[dict[str, Any]], edges: list[dict[str, Any]], parent_owned_only: bool) -> list[list[str]]:
    graph: dict[str, set[str]] = defaultdict(set)
    for node in nodes:
        graph[node["node_id"]]
    for edge in edges:
        if parent_owned_only and not bool(edge["parent_owned"]):
            continue
        if not parent_owned_only and not bool(edge["template_edge_present"]):
            continue
        a = str(edge["source_node"])
        b = str(edge["target_node"])
        graph[a].add(b)
        graph[b].add(a)

    seen: set[str] = set()
    comps: list[list[str]] = []
    for node_id in graph:
        if node_id in seen:
            continue
        queue: deque[str] = deque([node_id])
        seen.add(node_id)
        comp: list[str] = []
        while queue:
            current = queue.popleft()
            comp.append(current)
            for neighbor in graph[current]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
        comps.append(sorted(comp))
    return sorted(comps, key=lambda item: (len(item), item))


def graph_certificate_rows(nodes: list[dict[str, Any]], edges: list[dict[str, Any]]) -> list[dict[str, Any]]:
    template_comps = connected_components(nodes, edges, parent_owned_only=False)
    parent_comps = connected_components(nodes, edges, parent_owned_only=True)
    template_connected = len(template_comps) == 1
    parent_connected = len(parent_comps) == 1
    all_edges_parent_owned = all(bool(edge["parent_owned"]) for edge in edges)
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "certificate_id": "GRC1477_0_template_connectivity",
            "claim_piece": "candidate ordinary matter graph is connected as a physical template",
            "result": "PASS_TEMPLATE_ONLY" if template_connected else "FAIL_TEMPLATE",
            "template_component_count": len(template_comps),
            "parent_owned_component_count": len(parent_comps),
            "mathematical_effect_if_parent_signed": "naturality would propagate w_A=w_* over source-relevant ordinary matter",
            "current_blocker": "all graph edges remain physical templates rather than parent-owned morphisms",
            "delta_w_zero_promoted": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "certificate_id": "GRC1477_1_parent_owned_connectivity",
            "claim_piece": "parent-owned ordinary matter graph is connected",
            "result": "FAIL_NOT_PARENT_SIGNED" if not parent_connected or not all_edges_parent_owned else "PASS_PARENT_SIGNED",
            "template_component_count": len(template_comps),
            "parent_owned_component_count": len(parent_comps),
            "mathematical_effect_if_parent_signed": "would remove independent connected-component source weights",
            "current_blocker": "missing parent action graph/morphism certificate",
            "delta_w_zero_promoted": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "certificate_id": "GRC1477_2_action_density_line",
            "claim_piece": "single parent action-density line owns ordinary matter weights",
            "result": "FAIL_LINE_OWNER_UNSIGNED",
            "template_component_count": len(template_comps),
            "parent_owned_component_count": len(parent_comps),
            "mathematical_effect_if_parent_signed": "direct-sum sector weights would be common calibration rather than residual physics",
            "current_blocker": "parent syntax has not supplied L_matter_parent=sum_A L_A with one prefactor and no w_A slot",
            "delta_w_zero_promoted": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def action_line_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "ALO1477_0_single_L_matter_line",
            "required_parent_clause": "S_matter = integral dmu_parent L_matter_parent(Psi_A, gauge, theta, g_eff) with one ordinary-matter action-density line",
            "current_status": "MISSING_PARENT_SYNTAX",
            "if_signed": "relative action/source weights collapse to common calibration before readout",
            "if_missing": "S_matter=sum_A (1+delta_w_A) S_A remains a live countermodel",
            "source_artifact": rel(MEASURE_CURRENT_1452),
            "source_anchor": "CMT1452_0_target;CMT1452_3_species_jacobian_countermodel",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "ALO1477_1_naturality_on_nonzero_morphisms",
            "required_parent_clause": "for every parent-owned nonzero morphism f:A->B, w_B F(f)=F(f)w_A",
            "current_status": "EXACT_CONDITIONAL_THEOREM",
            "if_signed": "connected graph forces all source weights equal",
            "if_missing": "weights are unconstrained across disconnected or unsigned components",
            "source_artifact": rel(CONNECTED_1464),
            "source_anchor": "CON1464_1_naturality_lemma",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "ALO1477_2_direct_sum_policy",
            "required_parent_clause": "direct sums do not introduce independent source-normalization scalars",
            "current_status": "COUNTERMODEL_RETAINED",
            "if_signed": "direct-sum decomposition becomes bookkeeping, not physics",
            "if_missing": "w_EM,w_QCD,w_e,w_nuc can differ while preserving additivity",
            "source_artifact": rel(CONNECTED_1463),
            "source_anchor": "CMA1463_1_direct_sum_policy",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "ALO1477_3_common_calibration_silence",
            "required_parent_clause": "common w_* is derivative-silent and absorbed into measured G_N, not range/time/source dependent",
            "current_status": "NOT_SIGNED",
            "if_signed": "common scalar is harmless for Newton/GR source side",
            "if_missing": "Gdot/fifth-force/common-mode calibration rows stay live",
            "source_artifact": rel(CONNECTED_1463),
            "source_anchor": "CMA1463_2_calibration_silence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def direct_sum_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "obstruction_id": "DSO1477_0_component_weights",
            "countermodel": "C_ord = C_EM disjoint-union C_QCD disjoint-union C_lepton with independent constants w_i",
            "why_it_survives": "template physical interactions are not enough unless the parent action declares them source-normalization morphisms",
            "blocks": "delta_w theorem-zero; Newton source-side universality; WEP source cancellation; local-GR promotion",
            "required_kill_condition": "parent-owned connected graph plus single action-density line plus readout no-reentry",
            "retained": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "obstruction_id": "DSO1477_1_post_variation_selector",
            "countermodel": "variation gives total Hilbert stress but readout/source kernel later applies material labels",
            "why_it_survives": "source-label forgetting is conditional and readout kernels remain unsigned",
            "blocks": "WEP/clock/local projection theorem-zero",
            "required_kill_condition": "variation-before-readout theorem and no A-labelled post-readout source slot",
            "retained": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "obstruction_id": "DSO1477_2_nonHilbert_bypass",
            "countermodel": "J_src = kappa T_Hilbert + sum_A zeta_A J_NH,A",
            "why_it_survives": "non-Hilbert currents have not been proven absent, exact, or projected silent",
            "blocks": "source-label forgetting and CI1474_1 evaluator",
            "required_kill_condition": "J_NH=0/exact/projected-silent theorem or numeric residual row",
            "retained": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def schema_rows() -> list[dict[str, Any]]:
    fields = [
        ("row_id", "string", "dimensionless id", "unique stable row key", "required for traceability"),
        ("ci_id", "string", "CI1474_1_source_weight", "must equal source-weight residual target", "prevents accidental import into wrong residual"),
        ("arena", "enum", "WEP|R10|PPN|clock|orbital|Newton|local_GR", "local arena for projection", "forces arena-specific projection instead of vague pass/fail"),
        ("composition_pair", "string", "Ti-Pt or source/test pair", "material/source labels entering observable", "needed for WEP/source weight mapping"),
        ("delta_w_basis", "string", "w_EM,w_QCD,w_lepton,w_nuclear or parent graph component basis", "basis for relative source weights", "stops hidden basis changes"),
        ("delta_w_value", "float_or_symbolic_missing", "dimensionless", "numeric residual or MISSING_THEOREM_ZERO_OR_NUMERIC_DELTA_W", "claim needs numeric or theorem zero"),
        ("delta_w_uncertainty", "float_or_missing", "dimensionless", "one-sigma or conservative interval", "prevents point-value claims without width"),
        ("delta_w_units", "enum", "dimensionless", "must be dimensionless", "unit gate for action/source weights"),
        ("delta_w_sign_convention", "string", "positive means source A couples stronger than reference", "must state sign convention", "avoids fake cancellation"),
        ("tau_projection_value", "float_or_symbolic_missing", "dimensionless", "arena projection tau_X or MISSING_TAU_X", "turns weight into observable"),
        ("tau_projection_units", "enum", "dimensionless", "must be dimensionless after normalization", "unit gate for products"),
        ("observable_bound_value", "float_or_missing", "arena units", "source-backed bound used only after tau is real", "separates data from theory coefficient"),
        ("product_formula", "string", "P_X = delta_w_basis dot tau_X or direct q_source integral", "explicit observable product", "prevents bound inversion by prose"),
        ("no_cancellation_statement", "string", "states whether cancellations are forbidden, bounded, or modelled", "must not be blank", "protects robustness"),
        ("source_path", "path", "local source artifact or external citation", "must exist for local files", "provenance gate"),
        ("source_anchor", "string", "row/table/equation anchor", "must be specific", "prevents unsourced import"),
        ("valid_for_claim", "boolean", "False until all gates pass", "must remain False for templates", "claim firewall"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "schema_id": f"SC1477_{index}",
            "required_column": column,
            "expected_type": expected_type,
            "required_units_or_domain": units,
            "acceptance_rule": rule,
            "why_required": why,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for index, (column, expected_type, units, rule, why) in enumerate(fields)
    ]


def input_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": "DTW1477_0_MICROSCOPE_TiPt_source_weight",
            "ci_id": "CI1474_1_source_weight",
            "arena": "WEP",
            "composition_pair": "Ti-Pt",
            "delta_w_basis": "Delta_w_TiPt in ordinary-matter source-weight basis",
            "delta_w_value": "MISSING_THEOREM_ZERO_OR_NUMERIC_DELTA_W",
            "delta_w_uncertainty": "MISSING_DELTA_W_UNCERTAINTY",
            "delta_w_units": "dimensionless",
            "delta_w_sign_convention": "positive means Ti effective source weight exceeds Pt reference after common calibration removal",
            "tau_projection_value": "MISSING_TAU_WEP",
            "tau_projection_units": "dimensionless",
            "observable_bound_value": "2.8e-15",
            "observable_bound_units": "dimensionless Eotvos parameter placeholder from prior local schema only",
            "product_formula": "eta_TiPt_source = Delta_w_TiPt * tau_WEP or direct q_source integral",
            "no_cancellation_statement": "MISSING_NO_CANCELLATION_STATEMENT",
            "source_path": rel(TAU_SCHEMA_1067),
            "source_anchor": "TAQ1067_2_delta_w_width_if_tau;TAQ1067_3_direct_product_option;TAQ1067_4_refusal_rule",
            "passes_schema": False,
            "numeric_input_present": False,
            "theorem_zero_present": False,
            "valid_for_Newton": False,
            "valid_for_PPN": False,
            "valid_for_local_GR": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": "DTW1477_1_direct_q_source_integral",
            "ci_id": "CI1474_1_source_weight",
            "arena": "local_GR",
            "composition_pair": "generic compact local source",
            "delta_w_basis": "component vector delta_w_A over parent graph components",
            "delta_w_value": "MISSING_COMPONENT_VECTOR",
            "delta_w_uncertainty": "MISSING_COMPONENT_VECTOR_WIDTH",
            "delta_w_units": "dimensionless",
            "delta_w_sign_convention": "positive means component A increases Hilbert source relative to common calibration",
            "tau_projection_value": "MISSING_DIRECT_Q_SOURCE_PROJECTION",
            "tau_projection_units": "dimensionless after normalization",
            "observable_bound_value": "MISSING_LOCAL_ARENA_BOUND",
            "observable_bound_units": "arena-specific",
            "product_formula": "q_source^nu = P_loc nabla_mu[sum_A delta_w_A T_A^{mu nu}] + boundary/projector/readout terms",
            "no_cancellation_statement": "MISSING_BOUNDARY_AND_COMPONENT_NO_CANCELLATION_STATEMENT",
            "source_path": rel(SOURCE_COUPLING_1229),
            "source_anchor": "THM1229_3_residual_vector",
            "passes_schema": False,
            "numeric_input_present": False,
            "theorem_zero_present": False,
            "valid_for_Newton": False,
            "valid_for_PPN": False,
            "valid_for_local_GR": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def evaluator_rule_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "rule_id": "EVR1477_0_theorem_zero_route",
            "route": "theorem_zero",
            "acceptance_condition": "parent graph connected AND single action-density line signed AND direct-sum obstruction killed AND readout/no-nonHilbert gates signed",
            "current_status": "FAIL_UNSIGNED_PARENT_CLAUSES",
            "effect": "if passed, set delta_w theorem_zero_present=True for CI1474_1",
            "valid_for_claim_now": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "rule_id": "EVR1477_1_numeric_WEP_route",
            "route": "numeric_projection",
            "acceptance_condition": "numeric delta_w vector, numeric tau_WEP, source-backed eta bound, units, sign convention, and no-cancellation statement all present",
            "current_status": "FAIL_MISSING_NUMERIC_INPUTS",
            "effect": "if passed, compute abs(delta_w dot tau_WEP) <= eta_bound",
            "valid_for_claim_now": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "rule_id": "EVR1477_2_no_bound_inversion",
            "route": "refusal_guard",
            "acceptance_condition": "do not infer delta_w=0 or local-GR pass from an observational bound alone",
            "current_status": "PASS_GUARD_ACTIVE",
            "effect": "bound rows can constrain but cannot prove parent universality",
            "valid_for_claim_now": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "rule_id": "EVR1477_3_multi_arena_consistency",
            "route": "cross_arena",
            "acceptance_condition": "same delta_w basis and source convention must feed WEP, PPN, clock, orbital, R10, and Newton rows",
            "current_status": "PENDING_SCHEMA_ONLY",
            "effect": "prevents tuning separate couplings per arena",
            "valid_for_claim_now": False,
            "claim_allowed": False,
        },
    ]


def reduction_gate_rows(cert: list[dict[str, Any]], action: list[dict[str, Any]], template: list[dict[str, Any]]) -> list[dict[str, Any]]:
    template_connected = any(row["certificate_id"] == "GRC1477_0_template_connectivity" and row["result"] == "PASS_TEMPLATE_ONLY" for row in cert)
    parent_signed = any(row["certificate_id"] == "GRC1477_1_parent_owned_connectivity" and row["result"] == "PASS_PARENT_SIGNED" for row in cert)
    action_signed = any(row["audit_id"] == "ALO1477_0_single_L_matter_line" and row["current_status"] == "PARENT_SIGNED" for row in action)
    inputs_valid = all(row["passes_schema"] is True for row in template)
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1477_0_template_graph",
            "gate": "ordinary matter template graph connected",
            "gate_pass": template_connected,
            "claim_effect": "useful map for next proof target, but no physics claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1477_1_parent_owned_graph",
            "gate": "all graph edges are parent-owned morphisms",
            "gate_pass": parent_signed,
            "claim_effect": "required before collapsing component source weights",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1477_2_action_density_line",
            "gate": "single parent ordinary-matter action-density line signed",
            "gate_pass": action_signed,
            "claim_effect": "required before direct-sum weights become illegal",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1477_3_schema_rows",
            "gate": "delta_w/tau_WEP rows are numeric or theorem-zero",
            "gate_pass": inputs_valid,
            "claim_effect": "required before evaluator can score WEP/local source residuals",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1477_4_source_weight_claim",
            "gate": "CI1474_1 source-weight residual can be cleared",
            "gate_pass": parent_signed and action_signed and inputs_valid,
            "claim_effect": "must remain false in 1477",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1477_0_graph_result",
            "decision": "use connected ordinary-matter graph as a target certificate, not as proof",
            "reason": "physical template is connected, but parent-owned morphisms/action line are unsigned",
            "consequence": "delta_w_A is not set to zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1477_1_schema_hardened",
            "decision": "promote no rows; harden required delta_w/tau_WEP input schema",
            "reason": "numeric inputs or theorem-zero are still missing",
            "consequence": "future evaluator can reject vague coupling claims mechanically",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1477_2_best_next_step",
            "decision": "attack the single action-density line owner next",
            "reason": "connected graph alone does not beat the direct-sum countermodel",
            "consequence": "1478 should either sign S_matter one-line ownership or force numeric component weights",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1477_0_1478",
            "next_target": "1478-Y5-R10-RAB-single-action-density-line-owner-proof-or-component-delta-w-vector.md",
            "script": "scripts/Y5_R10_RAB_single_action_density_line_owner_proof_or_component_delta_w_vector.py",
            "objective": "try to derive the single parent ordinary-matter action-density line that forbids direct-sum source weights; if it fails, emit a component delta_w vector acquisition template for WEP/PPN/clock/orbital/R10",
            "include": "parent action syntax; single measure/hbar owner; direct-sum no-independent-prefactor clause; component basis; no-cancellation rule",
            "exclude": "GitHub action; formalization-workbench edits; local-GR pass; WEP/R10/clock claim promotion; observational bound inversion",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    cert: list[dict[str, Any]],
    action: list[dict[str, Any]],
    direct_sum: list[dict[str, Any]],
    schema: list[dict[str, Any]],
    template: list[dict[str, Any]],
    rules: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated_paths = [
        SOURCE_REGISTER,
        GRAPH_NODES,
        GRAPH_EDGES,
        GRAPH_CERTIFICATE,
        ACTION_LINE_AUDIT,
        DIRECT_SUM_LEDGER,
        DELTAW_SCHEMA,
        INPUT_TEMPLATE,
        EVALUATOR_RULES,
        REDUCTION_GATES,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    csv_parse_ok = True
    for path in generated_paths:
        try:
            parse_csv(path)
        except Exception:
            csv_parse_ok = False

    branch_copies = all(path.exists() for path in [QUAR_GRAPH, QUAR_SCHEMA, BRANCH_GRAPH, BRANCH_SCHEMA, BRANCH_GATES])
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_untouched = not any(
        file.stat().st_mtime >= START_TS
        for file in FORMALIZATION.rglob("*")
        if file.is_file()
    ) if FORMALIZATION.exists() else True

    template_connected = any(row["certificate_id"] == "GRC1477_0_template_connectivity" and row["result"] == "PASS_TEMPLATE_ONLY" for row in cert)
    parent_graph_refused = any(row["certificate_id"] == "GRC1477_1_parent_owned_connectivity" and row["result"] == "FAIL_NOT_PARENT_SIGNED" for row in cert)
    action_line_block = any(row["audit_id"] == "ALO1477_0_single_L_matter_line" and row["current_status"] == "MISSING_PARENT_SYNTAX" for row in action)
    direct_sum_retained = all(bool(row["retained"]) for row in direct_sum)
    schema_claim_false = all(not bool(row["valid_for_claim"]) and not bool(row["claim_allowed"]) for row in schema + template)
    inputs_fail = all(not bool(row["passes_schema"]) and not bool(row["numeric_input_present"]) and not bool(row["theorem_zero_present"]) for row in template)
    rule_guard_active = any(row["rule_id"] == "EVR1477_2_no_bound_inversion" and row["current_status"] == "PASS_GUARD_ACTIVE" for row in rules)
    claim_gate_false = any(row["gate_id"] == "GATE1477_4_source_weight_claim" and not bool(row["gate_pass"]) for row in gates)

    checks = [
        ("VAL1477_0_sources", all(bool(row["exists"]) for row in sources), "all cited local source paths exist"),
        ("VAL1477_1_nodes", len(nodes) >= 8 and all(row["parent_owned_status"] for row in nodes), "graph nodes written with parent status"),
        ("VAL1477_2_edges", len(edges) >= 10 and all(row["template_edge_present"] for row in edges), "template graph edges written"),
        ("VAL1477_3_template_connected", template_connected, "candidate ordinary matter graph is connected as template"),
        ("VAL1477_4_parent_graph_refused", parent_graph_refused, "parent-owned graph is not claimed"),
        ("VAL1477_5_action_line_blocks", action_line_block, "single action-density line owner remains missing"),
        ("VAL1477_6_direct_sum_retained", direct_sum_retained, "direct-sum/source-selector/nonHilbert obstructions retained"),
        ("VAL1477_7_schema_claim_false", schema_claim_false, "schema/template rows remain nonclaim"),
        ("VAL1477_8_inputs_fail", inputs_fail, "delta_w/tau rows fail until theorem-zero or numeric inputs exist"),
        ("VAL1477_9_no_bound_inversion", rule_guard_active, "bound inversion guard active"),
        ("VAL1477_10_claim_gate_false", claim_gate_false, "CI1474_1 source-weight claim gate remains false"),
        ("VAL1477_11_generated_csv_parse", csv_parse_ok, "all generated 1477 CSVs parse cleanly"),
        ("VAL1477_12_branch_copies", branch_copies, "nonclaim branch/quarantine copies written"),
        ("VAL1477_13_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1477_14_formalization_untouched", formalization_untouched, "formalization modified-file count since start=0"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "generated_utc": now(),
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1477_15_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1477 maps connected matter graph as nonclaim and hardens delta_w/tau_WEP schema",
            "generated_utc": now(),
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    cert: list[dict[str, Any]],
    action: list[dict[str, Any]],
    direct_sum: list[dict[str, Any]],
    schema: list[dict[str, Any]],
    template: list[dict[str, Any]],
    rules: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    lines: list[str] = []
    lines.append("# 1477 — R10/RAB Connected Matter Graph Certificate Or Delta-w Input Schema Runner")
    lines.append("")
    lines.append("## Verdict")
    lines.append("- The ordinary-matter graph is connected as a physical template: leptons, EM, quarks, QCD binding, nuclei, atoms, and macroscopic bodies sit in one candidate web.")
    lines.append("- That is not yet a theorem: the parent action has not signed the graph edges as source-normalization morphisms, and the single ordinary-matter action-density line is still missing.")
    lines.append("- Therefore `delta_w_A = 0` is not promoted; 1477 instead hardens the `delta_w/tau_WEP` schema so future rows must be numeric or theorem-zero.")
    lines.append("")
    lines.append("## Graph Certificate")
    lines.append("| certificate_id | result | current_blocker |")
    lines.append("|---|---|---|")
    for row in cert:
        lines.append(f"| {row['certificate_id']} | {row['result']} | {row['current_blocker']} |")
    lines.append("")
    lines.append("## Candidate Graph Nodes")
    lines.append("| node_id | node | parent_owned_status |")
    lines.append("|---|---|---|")
    for row in nodes:
        lines.append(f"| {row['node_id']} | {row['node']} | {row['parent_owned_status']} |")
    lines.append("")
    lines.append("## Candidate Graph Edges")
    lines.append("| edge_id | source_node | target_node | parent_owned_status |")
    lines.append("|---|---|---|---|")
    for row in edges:
        lines.append(f"| {row['edge_id']} | {row['source_node']} | {row['target_node']} | {row['parent_owned_status']} |")
    lines.append("")
    lines.append("## Action-Density Owner Audit")
    lines.append("| audit_id | current_status | if_missing |")
    lines.append("|---|---|---|")
    for row in action:
        lines.append(f"| {row['audit_id']} | {row['current_status']} | {row['if_missing']} |")
    lines.append("")
    lines.append("## Direct-Sum Obstruction")
    lines.append("| obstruction_id | retained | blocks |")
    lines.append("|---|---:|---|")
    for row in direct_sum:
        lines.append(f"| {row['obstruction_id']} | {row['retained']} | {row['blocks']} |")
    lines.append("")
    lines.append("## Delta-w/Tau Schema")
    lines.append("| schema_id | required_column | acceptance_rule |")
    lines.append("|---|---|---|")
    for row in schema:
        lines.append(f"| {row['schema_id']} | {row['required_column']} | {row['acceptance_rule']} |")
    lines.append("")
    lines.append("## Nonclaim Input Template")
    lines.append("| row_id | arena | delta_w_value | tau_projection_value | passes_schema |")
    lines.append("|---|---|---|---|---:|")
    for row in template:
        lines.append(f"| {row['row_id']} | {row['arena']} | {row['delta_w_value']} | {row['tau_projection_value']} | {row['passes_schema']} |")
    lines.append("")
    lines.append("## Evaluator Rules")
    lines.append("| rule_id | route | current_status |")
    lines.append("|---|---|---|")
    for row in rules:
        lines.append(f"| {row['rule_id']} | {row['route']} | {row['current_status']} |")
    lines.append("")
    lines.append("## Gates")
    lines.append("| gate_id | gate_pass | claim_effect |")
    lines.append("|---|---:|---|")
    for row in gates:
        lines.append(f"| {row['gate_id']} | {row['gate_pass']} | {row['claim_effect']} |")
    lines.append("")
    lines.append("## Decision Ledger")
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} — {row['consequence']}.")
    lines.append("")
    lines.append("## Validation")
    lines.append("| check_id | result | detail |")
    lines.append("|---|---|---|")
    for row in validation:
        lines.append(f"| {row['check_id']} | {row['result']} | {row['detail']} |")
    lines.append("")
    lines.append("## Source Register")
    lines.append("| source_id | exists | path_or_url | usage |")
    lines.append("|---|---:|---|---|")
    for row in sources:
        lines.append(f"| {row['source_id']} | {row['exists']} | `{row['path_or_url']}` | {row['usage']} |")
    lines.append("")
    lines.append("## Next Target")
    for row in next_target:
        lines.append(f"- `{row['next_target']}` via `{row['script']}`: {row['objective']}")
    lines.append("")
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    sources = source_rows()
    nodes = graph_node_rows()
    edges = graph_edge_rows()
    cert = graph_certificate_rows(nodes, edges)
    action = action_line_rows()
    direct_sum = direct_sum_rows()
    schema = schema_rows()
    template = input_template_rows()
    rules = evaluator_rule_rows()
    gates = reduction_gate_rows(cert, action, template)
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(GRAPH_NODES, nodes)
    write_csv(GRAPH_EDGES, edges)
    write_csv(GRAPH_CERTIFICATE, cert)
    write_csv(ACTION_LINE_AUDIT, action)
    write_csv(DIRECT_SUM_LEDGER, direct_sum)
    write_csv(DELTAW_SCHEMA, schema)
    write_csv(INPUT_TEMPLATE, template)
    write_csv(EVALUATOR_RULES, rules)
    write_csv(REDUCTION_GATES, gates)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)

    copy_nonclaim(GRAPH_CERTIFICATE, QUAR_GRAPH)
    copy_nonclaim(DELTAW_SCHEMA, QUAR_SCHEMA)
    copy_nonclaim(GRAPH_CERTIFICATE, BRANCH_GRAPH)
    copy_nonclaim(DELTAW_SCHEMA, BRANCH_SCHEMA)
    copy_nonclaim(REDUCTION_GATES, BRANCH_GATES)

    validation = validation_rows(sources, nodes, edges, cert, action, direct_sum, schema, template, rules, gates)
    write_csv(VALIDATION, validation)
    write_doc(sources, nodes, edges, cert, action, direct_sum, schema, template, rules, gates, decisions, validation, next_target)
    print("Y5_R10_1477_connected_graph_template_nonclaim_delta_w_schema_v2")


if __name__ == "__main__":
    main()
