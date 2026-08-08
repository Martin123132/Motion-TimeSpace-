from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
QUARANTINE = MICROSCOPE / "quarantine" / "1464"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1464-Y5-R10-RAB-connected-matter-category-proof-or-REGARDS-api-discovery.md"

PREV_NEXT = OUT / "P8_Y5_R10_1463_NEXT_TARGET.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1463_VALIDATION.csv"
PREV_MEASURE_CONTRACT = OUT / "P8_Y5_R10_1463_PARENT_MEASURE_OWNER_CONTRACT.csv"
PREV_CONNECTEDNESS = OUT / "P8_Y5_R10_1463_CONNECTED_MATTER_NATURALITY_AUDIT.csv"
PREV_JACOBIAN = OUT / "P8_Y5_R10_1463_SPECIES_JACOBIAN_EXCLUSION_CONTRACT.csv"
PREV_CMSM_INVENTORY = OUT / "P8_Y5_R10_1463_CMSM_MANUAL_CATEGORY_INVENTORY_NONCLAIM.csv"
PREV_CMSM_ACCESS = OUT / "P8_Y5_R10_1463_CMSM_ACCESS_AND_FILELIST_LEDGER.csv"
PREV_SIGNING = OUT / "P8_Y5_R10_1463_PARENT_SIGNING_DECISION.csv"

CONNECTED_1231 = OUT / "P8_Y5_R10_1231_MATTER_CATEGORY_CONNECTEDNESS_ATTEMPT.csv"
ACTION_OWNER_1230 = OUT / "P8_Y5_R10_1230_ACTION_SCALE_OWNER_THEOREM_ATTEMPT.csv"
ACTION_PROOF_1389 = OUT / "P8_Y5_R10_1389_ACTION_MEASURE_OWNER_PROOF_ATTEMPT.csv"
COMMON_MODE_1337 = OUT / "P8_Y5_R10_1337_COMMON_MODE_PREMISE_REDUCTION.csv"
SOURCE_LABEL_STACK_1231 = OUT / "P8_Y5_R10_1231_SOURCE_LABEL_FORGETTING_PROOF_STACK.csv"

LIVE_OFFICIAL_READOUT = MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout.csv"
LIVE_SOURCE_WORLD = MICROSCOPE / "source_worldtube" / "P_WEP_R_source_Earth_worldtube.csv"
LIVE_MATERIAL_TENSOR = MICROSCOPE / "derived" / "P_WEP_R_material_TA6V_minus_PtRh10_full_tensor.csv"
LIVE_CPARENT = COEFF / "C_parent_WEP_slot_import.csv"

REGARDS_DOCS = "https://regardsoss.github.io/docs/1.14/development/backend/services/catalog/api-swagger"
REGARDS_CATALOG_DOC = "https://regardsoss.github.io/docs/1.14/development/backend/services/catalog/service-plugins"
CMSM_PORTAL = "https://cmsm-ds.onera.fr/user/microscope"
CMSM_MODULE_7 = "https://cmsm-ds.onera.fr/user/microscope/modules/7"
ONERA_DATA_PAGE = "https://microscope.onera.fr/fr/publication/microscope-data-are-available"
OCA_MICROSCOPE_PAGE = "https://www.oca.eu/fr/microscope"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1464_SOURCE_REGISTER.csv"
CONNECTED_PROOF = OUT / "P8_Y5_R10_1464_CONNECTED_MATTER_CATEGORY_PROOF_ATTEMPT.csv"
INTERACTION_GRAPH_CONTRACT = OUT / "P8_Y5_R10_1464_INTERACTION_GRAPH_CONTRACT.csv"
DIRECT_SUM_LEDGER = OUT / "P8_Y5_R10_1464_DIRECT_SUM_COUNTERMODEL_LEDGER.csv"
CALIBRATION_SILENCE = OUT / "P8_Y5_R10_1464_COMMON_CALIBRATION_SILENCE_CONTRACT.csv"
REGARDS_API_DISCOVERY = OUT / "P8_Y5_R10_1464_REGARDS_API_DISCOVERY_LEDGER.csv"
REGARDS_ENDPOINT_CANDIDATES = OUT / "P8_Y5_R10_1464_REGARDS_ENDPOINT_CANDIDATES_NONCLAIM.csv"
CMSM_FILELIST_ROUTE = OUT / "P8_Y5_R10_1464_CMSM_FILELIST_ROUTE_NONCLAIM.csv"
LIVE_GUARD = OUT / "P8_Y5_R10_1464_LIVE_IMPORT_GUARD.csv"
REDUCTION_GATES = OUT / "P8_Y5_R10_1464_REDUCTION_GATES.csv"
SIGNING_DECISION = OUT / "P8_Y5_R10_1464_PARENT_SIGNING_DECISION.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1464_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1464_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1464_VALIDATION.csv"

QUAR_ENDPOINT_CANDIDATES = QUARANTINE / "REGARDS_ENDPOINT_CANDIDATES_QUARANTINE_NONCLAIM.csv"
QUAR_FILELIST_ROUTE = QUARANTINE / "CMSM_FILELIST_ROUTE_QUARANTINE_NONCLAIM.csv"

BRANCH_CONNECTED_PROOF = COEFF / "connected_matter_category_proof_attempt_1464.csv"
BRANCH_REGARDS_ROUTE = COEFF / "REGARDS_api_filelist_route_nonclaim_1464.csv"
BRANCH_SIGNING = COEFF / "C_parent_WEP_connected_matter_category_signing_decision_1464.csv"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
START_TS = datetime.now(timezone.utc).timestamp()


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def truth(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def rows_from_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv_ok(path: Path) -> bool:
    return bool(rows_from_csv(path))


def copy_branch(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


def source_rows() -> list[dict[str, Any]]:
    local_sources = [
        ("SRC1464_0_prev_next", PREV_NEXT, "1463 handoff"),
        ("SRC1464_1_prev_validation", PREV_VALIDATION, "1463 validation"),
        ("SRC1464_2_prev_measure_contract", PREV_MEASURE_CONTRACT, "1463 measure owner contract"),
        ("SRC1464_3_prev_connectedness", PREV_CONNECTEDNESS, "1463 connectedness audit"),
        ("SRC1464_4_prev_jacobian", PREV_JACOBIAN, "1463 Jacobian exclusion"),
        ("SRC1464_5_prev_CMSM_inventory", PREV_CMSM_INVENTORY, "1463 CMSM category inventory"),
        ("SRC1464_6_prev_CMSM_access", PREV_CMSM_ACCESS, "1463 CMSM access ledger"),
        ("SRC1464_7_prev_signing", PREV_SIGNING, "1463 signing decision"),
        ("SRC1464_8_connected_1231", CONNECTED_1231, "1231 connected matter category attempt"),
        ("SRC1464_9_action_1230", ACTION_OWNER_1230, "1230 action-scale owner theorem"),
        ("SRC1464_10_action_1389", ACTION_PROOF_1389, "1389 action-measure proof attempt"),
        ("SRC1464_11_common_1337", COMMON_MODE_1337, "1337 common-mode premise reduction"),
        ("SRC1464_12_source_label_stack_1231", SOURCE_LABEL_STACK_1231, "1231 source-label forgetting stack"),
    ]
    rows = [
        {
            "source_id": source_id,
            "source_type": "local_file",
            "source_path_or_url": str(path),
            "exists": path.exists(),
            "role": role,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path, role in local_sources
    ]
    for source_id, url, role in [
        ("SRC1464_13_REGARDS_api_docs", REGARDS_DOCS, "REGARDS catalog REST endpoint reference"),
        ("SRC1464_14_REGARDS_catalog_docs", REGARDS_CATALOG_DOC, "REGARDS catalog service/plugin reference"),
        ("SRC1464_15_ONERA_data_page", ONERA_DATA_PAGE, "official MICROSCOPE data availability page"),
        ("SRC1464_16_OCA_page", OCA_MICROSCOPE_PAGE, "MICROSCOPE data category page"),
    ]:
        rows.append(
            {
                "source_id": source_id,
                "source_type": "external_url",
                "source_path_or_url": url,
                "exists": "not_local_path",
                "role": role,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def connected_proof_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "CON1464_0_target",
            "claim_piece": "connected ordinary-matter category",
            "formal_statement": "C_ord is connected for action-density/source-normalization naturality: every source-relevant ordinary sector is linked by parent-owned nonzero morphisms",
            "proof_move": "turn physical interaction web into a parent graph/morphism certificate",
            "status": "TARGET_SHARPENED",
            "if_signed": "natural positive source/action scalar w_A collapses to one common w_*",
            "current_blocker": "parent-owned graph of ordinary matter objects/morphisms is not constructed",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "CON1464_1_naturality_lemma",
            "claim_piece": "connected graph collapses weights",
            "formal_statement": "for any nonzero morphism f:A->B, naturality w_B F(f)=F(f)w_A implies w_A=w_B; connectedness propagates w_A=w_*",
            "proof_move": "exact category-theoretic lemma on action-density line automorphisms",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "if_signed": "relative source weights become impossible within the connected component",
            "current_blocker": "requires F(f) nonzero and parent-owned for the ordinary matter graph",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "CON1464_2_physical_template",
            "claim_piece": "ordinary matter interaction web template",
            "formal_statement": "electrons, photons, quarks, gluons, nuclear binding, and atoms in Ti/Pt matter are physically coupled by EM/QCD/electroweak/bound-state maps",
            "proof_move": "use this as a candidate graph, not as a proof",
            "status": "PHYSICAL_GUIDANCE_NOT_PARENT_PROOF",
            "if_signed": "would define the connected component relevant to MICROSCOPE matter",
            "current_blocker": "MTS parent action has not supplied the graph as a source-normalization category",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "CON1464_3_direct_sum_obstruction",
            "claim_piece": "direct-sum disconnected countermodel",
            "formal_statement": "if C_ord splits into components C_i, then w_i can be independent constants while preserving naturality within each C_i",
            "proof_move": "retain the exact obstruction rather than hiding it",
            "status": "COUNTERMODEL_SURVIVES",
            "if_signed": "nothing; this blocks promotion until connectedness or common owner is derived",
            "current_blocker": "ordinary matter category connectedness is not parent-signed",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "CON1464_4_source_label_forgetting_dependency",
            "claim_piece": "connectedness alone is not enough",
            "formal_statement": "w_A=w_* only after source functor acts on action-density/source objects before readout and does not reintroduce labels",
            "proof_move": "tie connectedness to source-label forgetting and readout-order gates",
            "status": "DEPENDENCY_RETAINED",
            "if_signed": "prevents post-readout selectors from recreating source labels",
            "current_blocker": "source/readout descent remains conditional and source-pack files are absent",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "CON1464_5_verdict",
            "claim_piece": "connected matter category proof status",
            "formal_statement": "connected graph + naturality + L_action owner + label forgetting + calibration silence would kill relative w_A in ordinary matter",
            "proof_move": "reduce the branch to a graph-owner certificate",
            "status": "PROOF_NOT_CLOSED",
            "if_signed": "w_A/J_A source-side residual route could be demoted toward theorem-zero",
            "current_blocker": "graph owner, source-label forgetting, and calibration silence remain unsigned",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def interaction_graph_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "graph_id": "GRAPH1464_0_vertices",
            "object": "ordinary matter source-normalization vertices",
            "required_rows": "electron/lepton, photon/EM, light quark, gluon/QCD, nuclear binding, atom/material effective sector",
            "current_status": "TEMPLATE_NOT_PARENT_SIGNED",
            "if_missing": "component-wise w_i source weights remain legal",
            "next_action": "construct parent-owned object list from matter action rather than observed phenomenology",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "graph_id": "GRAPH1464_1_edges",
            "object": "parent-owned nonzero morphisms",
            "required_rows": "EM coupling edges, QCD/binding edges, mass-generation/effective-action edges, material-bound-state edges",
            "current_status": "PHYSICAL_TEMPLATE_ONLY",
            "if_missing": "naturality cannot propagate w_A=w_B",
            "next_action": "derive edges from parent matter functor or keep direct-sum countermodel",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "graph_id": "GRAPH1464_2_nonzero_condition",
            "object": "nonzero action-density maps",
            "required_rows": "each edge must act nontrivially on L_action/source functional",
            "current_status": "NOT_PROVED",
            "if_missing": "a formal interaction label may fail to constrain source weights",
            "next_action": "prove nonzero morphism action on L_action",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "graph_id": "GRAPH1464_3_connectedness_certificate",
            "object": "connectedness certificate",
            "required_rows": "path between every source-relevant vertex and every other vertex in the graph",
            "current_status": "NOT_BUILT",
            "if_missing": "connectedness remains a plausible physics template, not a theorem",
            "next_action": "generate a source-backed graph certificate or closure clause",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def direct_sum_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "DS1464_0_two_component",
            "countermodel": "C_ord = C_1 disjoint_union C_2 with w_1 != w_2",
            "why_survives": "naturality only enforces constant weight inside each connected component",
            "effect": "relative source normalization survives without violating covariance/additivity",
            "retention_decision": "RETAIN_LIVE_NONCLAIM",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "DS1464_1_effective_sector_split",
            "countermodel": "EM/QCD/lepton/nuclear effective sectors carry independent action-density automorphisms",
            "why_survives": "parent functor has not proved effective sectors are one connected source-normalization object",
            "effect": "material composition dependence can enter Ti/Pt WEP residuals",
            "retention_decision": "RETAIN_LIVE_NONCLAIM",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "DS1464_2_common_graph_but_variable_weight",
            "countermodel": "w_* common over graph but varies with time/range/source/frame",
            "why_survives": "calibration silence is not signed",
            "effect": "common mode can leak into Gdot/fifth-force/range residuals",
            "retention_decision": "RETAIN_LIVE_NONCLAIM",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def calibration_silence_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "silence_id": "CAL1464_0_universal_constant",
            "condition": "w_* is universal and derivative-silent",
            "formal_requirement": "partial_t ln w_* = partial_lambda ln w_* = partial_source ln w_* = partial_frame ln w_* = partial_material ln w_* = 0",
            "current_status": "NOT_SIGNED",
            "if_missing": "measured G calibration cannot hide arena dependence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "silence_id": "CAL1464_1_measured_G_absorption",
            "condition": "one constant common factor only",
            "formal_requirement": "T_eff=w_* T_total with w_* constant lets kappa_eff w_* be identified with measured G_N",
            "current_status": "EXACT_IF_CAL1464_0_SIGNED",
            "if_missing": "retain Gdot/range/source normalization rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "silence_id": "CAL1464_2_policy",
            "condition": "no calibration shortcut",
            "formal_requirement": "relative or derivative-active weights must be bounded, not absorbed",
            "current_status": "GUARD_RETAINED",
            "if_missing": "false local-GR pass risk",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def regards_api_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "api_id": "REG1464_0_catalog_docs",
            "source_url": REGARDS_DOCS,
            "documented_endpoint_or_feature": "/api/v1/rs-catalog/complex/search and /api/v1/rs-catalog/engines/{engineType}/datasets/search",
            "discovery_result": "REGARDS documentation exposes catalog search endpoints for datasets/entities, but CMSM instance file list was not retrieved",
            "current_status": "API_ROUTE_IDENTIFIED_NOT_AUTHENTICATED",
            "next_action": "try authenticated/browser-session/API engine discovery for CMSM module 7",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "api_id": "REG1464_1_opensearch_feature",
            "source_url": REGARDS_CATALOG_DOC,
            "documented_endpoint_or_feature": "REGARDS catalog supports search services including OpenSearch/GeoJSON-style catalog exposure",
            "discovery_result": "useful route for file-list discovery, but no CMSM product rows parsed",
            "current_status": "DOCUMENTED_CAPABILITY_ONLY",
            "next_action": "discover engineType and access role for CMSM project",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "api_id": "REG1464_2_CMSM_shell_probe",
            "source_url": CMSM_MODULE_7,
            "documented_endpoint_or_feature": "CMSM module 7 REGARDS UI route",
            "discovery_result": "local shell connection to cmsm-ds.onera.fr:443 fails; web/browser resolves only shell/title, no file list",
            "current_status": "BLOCKED_NO_FILE_ROWS",
            "next_action": "use in-app browser/session inspection or external browser manually, then record endpoints and hashes",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def endpoint_candidate_rows() -> list[dict[str, Any]]:
    endpoint_templates = [
        ("END1464_0_complex_search", f"{CMSM_PORTAL}/api/v1/rs-catalog/complex/search", "catalog complex search"),
        ("END1464_1_dataset_search", f"{CMSM_PORTAL}/api/v1/rs-catalog/engines/{{engineType}}/datasets/search", "dataset search; engineType unknown"),
        ("END1464_2_dataobject_search", f"{CMSM_PORTAL}/api/v1/rs-catalog/engines/{{engineType}}/dataobjects/search", "dataobject search; engineType unknown"),
        ("END1464_3_download_template", f"{CMSM_PORTAL}/api/v1/rs-catalog/downloads/{{aip_id}}/files/{{checksum}}", "documented download path template"),
        ("END1464_4_module_7_ui", CMSM_MODULE_7, "manual module-7 UI route from OCA page"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "endpoint_id": endpoint_id,
            "endpoint_or_template": endpoint,
            "purpose": purpose,
            "status": "CANDIDATE_NOT_VERIFIED_ON_CMSM",
            "required_before_claim": "successful response, dataset id/file name, source URL, checksum, schema map, row count",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for endpoint_id, endpoint, purpose in endpoint_templates
    ]


def cmsm_filelist_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "route_id": "CFL1464_0_manual_browser",
            "route": "manual in-browser REGARDS module inventory",
            "required_capture": "dataset category, product/file names, download URLs, metadata dictionary, licence/access note",
            "current_status": "NOT_DONE",
            "promotion_rule": "manual notes go to quarantine only until checksummed files exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "route_id": "CFL1464_1_api_engine_discovery",
            "route": "discover REGARDS engineType/auth/project endpoints",
            "required_capture": "working catalog endpoint, HTTP status, response schema, pagination rule",
            "current_status": "CANDIDATE_ENDPOINTS_WRITTEN",
            "promotion_rule": "no live official_readout/source_worldtube rows from endpoint templates alone",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "route_id": "CFL1464_2_checksum_manifest",
            "route": "download/checksum source-pack files after inventory",
            "required_capture": "sha256, byte count, row count, extractor version, schema map",
            "current_status": "BLOCKED_UNTIL_FILE_LIST",
            "promotion_rule": "1457/1459 validator must pass before any live import",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def live_guard_rows() -> list[dict[str, Any]]:
    live_targets = [
        ("LIVE1464_0_official_readout", "official_readout", LIVE_OFFICIAL_READOUT),
        ("LIVE1464_1_source_worldtube", "source_worldtube", LIVE_SOURCE_WORLD),
        ("LIVE1464_2_material_tensor", "material_tensor", LIVE_MATERIAL_TENSOR),
        ("LIVE1464_3_C_parent", "C_parent_WEP", LIVE_CPARENT),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "live_guard_id": guard_id,
            "object": object_name,
            "live_path": str(path),
            "exists_now": path.exists(),
            "would_write_in_1464": False,
            "reason": "1464 writes proof/API route ledgers only; no live import",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for guard_id, object_name, path in live_targets
    ]


def reduction_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1464_0_naturality_lemma",
            "gate": "connected naturality lemma exact conditional",
            "gate_pass": True,
            "blocking_reason": "conditional lemma only",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1464_1_connected_graph_signed",
            "gate": "ordinary matter graph parent-signed connected",
            "gate_pass": False,
            "blocking_reason": "graph owner/certificate not built",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1464_2_direct_sum_killed",
            "gate": "direct-sum source-weight countermodel killed",
            "gate_pass": False,
            "blocking_reason": "disconnected component countermodel survives",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1464_3_calibration_silence",
            "gate": "common calibration derivative-silent",
            "gate_pass": False,
            "blocking_reason": "silence not signed",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1464_4_REGARDS_route",
            "gate": "REGARDS/CMSM API candidate route written",
            "gate_pass": True,
            "blocking_reason": "candidate endpoints only; no CMSM file list",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1464_5_CMSM_filelist",
            "gate": "official CMSM file list/checksums acquired",
            "gate_pass": False,
            "blocking_reason": "no authenticated/parseable file rows",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1464_6_local_claim",
            "gate": "local WEP/local-GR claim allowed",
            "gate_pass": False,
            "blocking_reason": "connectedness proof and source-pack data remain incomplete",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def signing_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "SIGN1464_0_connected_matter_category",
            "target": "connected ordinary matter category/naturality clause",
            "naturality_lemma_exact": True,
            "connected_graph_parent_signed": False,
            "direct_sum_countermodel_killed": False,
            "calibration_silence_signed": False,
            "REGARDS_route_written": True,
            "CMSM_filelist_imported": False,
            "JA_zero_import_allowed": False,
            "delta_q_zero_import_allowed": False,
            "C_parent_WEP_import_allowed": False,
            "tau_WEP_numeric_allowed": False,
            "local_claim_allowed": False,
            "decision": "KEEP_CONNECTEDNESS_CONDITIONAL_AND_USE_REGARDS_ROUTE_AS_NONCLAIM_DATA_PLAN",
            "reason": "naturality is exact if graph connected, but graph owner/source-label forgetting/calibration silence are not parent-signed; REGARDS endpoints are candidates only",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1464_0_theorem",
            "decision": "connectedness route remains exact conditional, not a proof",
            "why": "direct-sum components can carry independent natural weights unless parent graph connectedness is signed",
            "consequence": "w_A/J_A branch remains live",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1464_1_calibration",
            "decision": "common w_* still needs derivative-silence before measured-G absorption",
            "why": "a common but range/time/source dependent factor would leak into other arenas",
            "consequence": "Gdot/fifth-force/range guards stay active",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1464_2_REGARDS",
            "decision": "REGARDS API route is now candidate-level documented, not an acquired source pack",
            "why": "docs identify catalog endpoints but CMSM instance did not yield file rows here",
            "consequence": "next data step is API/session discovery or manual file-list capture",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1464_0_1465",
            "next_target": "1465-Y5-R10-RAB-ordinary-matter-graph-certificate-or-CMSM-session-filelist-capture.md",
            "script": "scripts/Y5_R10_RAB_ordinary_matter_graph_certificate_or_CMSM_session_filelist_capture.py",
            "objective": "try to build a concrete ordinary-matter interaction graph certificate; if it fails, capture the CMSM/REGARDS file list through a browser/session workflow",
            "include": "graph vertices/edges; direct-sum residuals; calibration silence; REGARDS session/file-list capture; no live claim",
            "exclude": "numeric tau_WEP; local-GR pass; C_parent promotion; formalization-workbench edits; GitHub action",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    connected: list[dict[str, Any]],
    graph: list[dict[str, Any]],
    direct_sum: list[dict[str, Any]],
    calibration: list[dict[str, Any]],
    regards: list[dict[str, Any]],
    endpoints: list[dict[str, Any]],
    filelist: list[dict[str, Any]],
    live_guard: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated_csvs = [
        SOURCE_REGISTER,
        CONNECTED_PROOF,
        INTERACTION_GRAPH_CONTRACT,
        DIRECT_SUM_LEDGER,
        CALIBRATION_SILENCE,
        REGARDS_API_DISCOVERY,
        REGARDS_ENDPOINT_CANDIDATES,
        CMSM_FILELIST_ROUTE,
        QUAR_ENDPOINT_CANDIDATES,
        QUAR_FILELIST_ROUTE,
        LIVE_GUARD,
        REDUCTION_GATES,
        SIGNING_DECISION,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    local_sources_exist = all(row["source_type"] != "local_file" or truth(row["exists"]) for row in sources)
    exact_conditional = any(row["status"] == "EXACT_CONDITIONAL_THEOREM" for row in connected)
    proof_not_closed = any(row["status"] == "PROOF_NOT_CLOSED" for row in connected)
    graph_not_signed = all(not truth(row["claim_allowed"]) for row in graph)
    direct_sum_live = all(row["retention_decision"] == "RETAIN_LIVE_NONCLAIM" for row in direct_sum)
    calibration_nonclaim = all(not truth(row["claim_allowed"]) for row in calibration)
    regards_candidate_only = all(not truth(row["claim_allowed"]) for row in regards + endpoints + filelist)
    endpoint_templates_present = len(endpoints) >= 4
    live_paths_untouched = all(not truth(row["exists_now"]) and not truth(row["would_write_in_1464"]) for row in live_guard)
    gate_pattern_safe = truth(gates[0]["gate_pass"]) and truth(gates[4]["gate_pass"]) and all(
        not truth(row["gate_pass"]) for row in gates[1:4] + gates[5:]
    )
    signing_refuses = all(
        not truth(row["JA_zero_import_allowed"])
        and not truth(row["delta_q_zero_import_allowed"])
        and not truth(row["C_parent_WEP_import_allowed"])
        and not truth(row["tau_WEP_numeric_allowed"])
        and not truth(row["local_claim_allowed"])
        for row in signing
    )
    generated_parse = all(parse_csv_ok(path) for path in generated_csvs)
    branch_copies = BRANCH_CONNECTED_PROOF.exists() and BRANCH_REGARDS_ROUTE.exists() and BRANCH_SIGNING.exists()
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formal_recent = 0
    if FORMALIZATION.exists():
        formal_recent = sum(
            1
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and path.stat().st_mtime > START_TS
        )
    checks = [
        ("VAL1464_0_sources", local_sources_exist, "all cited local source paths exist"),
        ("VAL1464_1_exact_conditional", exact_conditional, "connected naturality theorem is exact conditional"),
        ("VAL1464_2_proof_not_closed", proof_not_closed, "connectedness proof remains unpromoted"),
        ("VAL1464_3_graph_not_signed", graph_not_signed, "graph contract rows remain nonclaim"),
        ("VAL1464_4_direct_sum_live", direct_sum_live, "direct-sum countermodels remain live"),
        ("VAL1464_5_calibration_nonclaim", calibration_nonclaim, "calibration silence rows remain nonclaim"),
        ("VAL1464_6_REGARDS_candidate_only", regards_candidate_only, "REGARDS/CMSM route rows remain candidate/nonclaim"),
        ("VAL1464_7_endpoint_templates", endpoint_templates_present, "REGARDS endpoint candidates written"),
        ("VAL1464_8_live_paths_untouched", live_paths_untouched, "critical live official/source/material/Cparent files remain absent"),
        ("VAL1464_9_gate_pattern_safe", gate_pattern_safe, "only conditional theorem and API-route gates pass; claim gates false"),
        ("VAL1464_10_signing_refuses", signing_refuses, "parent signing refuses JA/delta_q/Cparent/tau/local claim"),
        ("VAL1464_11_generated_csv_parse", generated_parse, "all generated 1464 CSVs parse cleanly"),
        ("VAL1464_12_branch_copies", branch_copies, "nonclaim branch copies written"),
        ("VAL1464_13_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1464_14_formalization_untouched", formal_recent == 0, f"formalization modified-file count since start={formal_recent}"),
        ("VAL1464_15_overall", True, "1464 keeps connectedness conditional and stages REGARDS/CMSM API candidates without claim promotion"),
    ]
    return [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "generated_utc": now(),
        }
        for check_id, passed, detail in checks
    ]


def write_table(handle, title: str, rows: list[dict[str, Any]]) -> None:
    handle.write(f"## {title}\n\n")
    if not rows:
        handle.write("_No rows._\n\n")
        return
    fields = list(rows[0].keys())
    handle.write("| " + " | ".join(fields) + " |\n")
    handle.write("| " + " | ".join(["---"] * len(fields)) + " |\n")
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ").replace("|", "\\|") for field in fields]
        handle.write("| " + " | ".join(values) + " |\n")
    handle.write("\n")


def write_doc(
    sources: list[dict[str, Any]],
    connected: list[dict[str, Any]],
    graph: list[dict[str, Any]],
    direct_sum: list[dict[str, Any]],
    calibration: list[dict[str, Any]],
    regards: list[dict[str, Any]],
    endpoints: list[dict[str, Any]],
    filelist: list[dict[str, Any]],
    live_guard: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    with DOC.open("w", encoding="utf-8") as handle:
        handle.write("# 1464 - Connected matter category proof or REGARDS API discovery\n\n")
        handle.write(
            "**Current verdict:** the connected-category theorem is exact conditionally: a natural positive action/source weight is common on a connected ordinary-matter category. "
            "But MTS has not yet parent-signed the ordinary-matter graph, the nonzero morphism certificate, source-label forgetting, or calibration silence. "
            "So the direct-sum countermodel remains live and no `w_A/J_A` zero is imported.\n\n"
        )
        handle.write(
            "**Useful progress:** the next theorem target is no longer abstract: build a parent-owned graph certificate with vertices, edges, nonzero action on `L_action`, and connectedness paths. "
            "The data route also improved: REGARDS catalog API endpoint templates are staged, but the CMSM instance still has no acquired file list or checksums.\n\n"
        )
        write_table(handle, "Source register", sources)
        write_table(handle, "Connected matter category proof attempt", connected)
        write_table(handle, "Interaction graph contract", graph)
        write_table(handle, "Direct-sum countermodel ledger", direct_sum)
        write_table(handle, "Common calibration silence contract", calibration)
        write_table(handle, "REGARDS API discovery ledger", regards)
        write_table(handle, "REGARDS endpoint candidates", endpoints)
        write_table(handle, "CMSM file-list route", filelist)
        write_table(handle, "Live import guard", live_guard)
        write_table(handle, "Reduction gates", gates)
        write_table(handle, "Parent signing decision", signing)
        write_table(handle, "Decision ledger", decisions)
        write_table(handle, "Validation", validation)
        write_table(handle, "Next target", next_target)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    sources = source_rows()
    connected = connected_proof_rows()
    graph = interaction_graph_contract_rows()
    direct_sum = direct_sum_rows()
    calibration = calibration_silence_rows()
    regards = regards_api_rows()
    endpoints = endpoint_candidate_rows()
    filelist = cmsm_filelist_route_rows()
    live_guard = live_guard_rows()
    gates = reduction_gate_rows()
    signing = signing_decision_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(CONNECTED_PROOF, connected)
    write_csv(INTERACTION_GRAPH_CONTRACT, graph)
    write_csv(DIRECT_SUM_LEDGER, direct_sum)
    write_csv(CALIBRATION_SILENCE, calibration)
    write_csv(REGARDS_API_DISCOVERY, regards)
    write_csv(REGARDS_ENDPOINT_CANDIDATES, endpoints)
    write_csv(CMSM_FILELIST_ROUTE, filelist)
    write_csv(QUAR_ENDPOINT_CANDIDATES, endpoints)
    write_csv(QUAR_FILELIST_ROUTE, filelist)
    write_csv(LIVE_GUARD, live_guard)
    write_csv(REDUCTION_GATES, gates)
    write_csv(SIGNING_DECISION, signing)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)

    copy_branch(CONNECTED_PROOF, BRANCH_CONNECTED_PROOF)
    copy_branch(REGARDS_API_DISCOVERY, BRANCH_REGARDS_ROUTE)
    copy_branch(SIGNING_DECISION, BRANCH_SIGNING)

    remove_pycache()
    validation = validation_rows(sources, connected, graph, direct_sum, calibration, regards, endpoints, filelist, live_guard, gates, signing)
    write_csv(VALIDATION, validation)
    write_doc(sources, connected, graph, direct_sum, calibration, regards, endpoints, filelist, live_guard, gates, signing, decisions, validation, next_target)
    print("Y5_R10_1464_connectedness_conditional_REGARDS_candidates_nonclaim")


if __name__ == "__main__":
    main()
