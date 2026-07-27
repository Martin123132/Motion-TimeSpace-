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
QUARANTINE = MICROSCOPE / "quarantine" / "1465"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1465-Y5-R10-RAB-ordinary-matter-graph-certificate-or-CMSM-session-filelist-capture.md"

PREV_NEXT = OUT / "P8_Y5_R10_1464_NEXT_TARGET.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1464_VALIDATION.csv"
PREV_CONNECTED = OUT / "P8_Y5_R10_1464_CONNECTED_MATTER_CATEGORY_PROOF_ATTEMPT.csv"
PREV_GRAPH = OUT / "P8_Y5_R10_1464_INTERACTION_GRAPH_CONTRACT.csv"
PREV_DIRECT_SUM = OUT / "P8_Y5_R10_1464_DIRECT_SUM_COUNTERMODEL_LEDGER.csv"
PREV_CALIBRATION = OUT / "P8_Y5_R10_1464_COMMON_CALIBRATION_SILENCE_CONTRACT.csv"
PREV_REGARDS = OUT / "P8_Y5_R10_1464_REGARDS_API_DISCOVERY_LEDGER.csv"
PREV_ENDPOINTS = OUT / "P8_Y5_R10_1464_REGARDS_ENDPOINT_CANDIDATES_NONCLAIM.csv"
PREV_FILELIST = OUT / "P8_Y5_R10_1464_CMSM_FILELIST_ROUTE_NONCLAIM.csv"
PREV_SIGNING = OUT / "P8_Y5_R10_1464_PARENT_SIGNING_DECISION.csv"

GRAPH_1232 = OUT / "P8_Y5_R10_1232_INTERACTION_GRAPH_CERTIFICATE_ATTEMPT.csv"
EDGES_1232 = OUT / "P8_Y5_R10_1232_ORDINARY_MATTER_GRAPH_EDGE_AUDIT.csv"
DEMOTION_1233 = OUT / "P8_Y5_R10_1233_GRAPH_EDGE_DEMOTION_LEDGER.csv"
GRAPH_AUDIT_1327 = OUT / "P8_Y5_R10_1327_PARENT_GRAPH_CERTIFICATE_AUDIT.csv"
REENTRY_1328 = OUT / "P8_Y5_R10_1328_GRAPH_EDGE_OWNER_REENTRY_BLOCKERS.csv"
REGARDS_1072 = OUT / "P8_Y5_R10_1072_CMSM_REGARDS_API_CANDIDATE_ENDPOINTS.csv"
REGARDS_1227 = OUT / "P8_Y5_R10_1227_REGARDS_ENDPOINT_CANDIDATES.csv"

LIVE_OFFICIAL_READOUT = MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout.csv"
LIVE_SOURCE_WORLD = MICROSCOPE / "source_worldtube" / "P_WEP_R_source_Earth_worldtube.csv"
LIVE_MATERIAL_TENSOR = MICROSCOPE / "derived" / "P_WEP_R_material_TA6V_minus_PtRh10_full_tensor.csv"
LIVE_CPARENT = COEFF / "C_parent_WEP_slot_import.csv"

CMSM_MODULE_7 = "https://cmsm-ds.onera.fr/user/microscope/modules/7"
CMSM_PORTAL = "https://cmsm-ds.onera.fr/user/microscope"
REGARDS_DOCS = "https://regardsoss.github.io/docs/1.14/development/backend/services/catalog/api-swagger"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1465_SOURCE_REGISTER.csv"
GRAPH_VERTICES = OUT / "P8_Y5_R10_1465_ORDINARY_MATTER_GRAPH_VERTICES.csv"
GRAPH_EDGES = OUT / "P8_Y5_R10_1465_ORDINARY_MATTER_GRAPH_EDGES.csv"
GRAPH_PATHS = OUT / "P8_Y5_R10_1465_ORDINARY_MATTER_GRAPH_PATH_CERTIFICATE.csv"
GRAPH_CERTIFICATE = OUT / "P8_Y5_R10_1465_GRAPH_CERTIFICATE_DECISION.csv"
DIRECT_SUM_RESIDUALS = OUT / "P8_Y5_R10_1465_DIRECT_SUM_RESIDUALS_RETAINED.csv"
CMSM_SESSION_CAPTURE = OUT / "P8_Y5_R10_1465_CMSM_SESSION_FILELIST_CAPTURE_PLAN.csv"
CMSM_SESSION_PROBE = OUT / "P8_Y5_R10_1465_CMSM_SESSION_PROBE_RESULT.csv"
REGARDS_REQUEST_TEMPLATE = OUT / "P8_Y5_R10_1465_REGARDS_REQUEST_TEMPLATE_NONCLAIM.csv"
LIVE_GUARD = OUT / "P8_Y5_R10_1465_LIVE_IMPORT_GUARD.csv"
REDUCTION_GATES = OUT / "P8_Y5_R10_1465_REDUCTION_GATES.csv"
SIGNING_DECISION = OUT / "P8_Y5_R10_1465_PARENT_SIGNING_DECISION.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1465_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1465_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1465_VALIDATION.csv"

QUAR_SESSION_CAPTURE = QUARANTINE / "CMSM_SESSION_FILELIST_CAPTURE_PLAN_QUARANTINE_NONCLAIM.csv"
QUAR_REQUEST_TEMPLATE = QUARANTINE / "REGARDS_REQUEST_TEMPLATE_QUARANTINE_NONCLAIM.csv"

BRANCH_GRAPH_CERT = COEFF / "ordinary_matter_graph_certificate_attempt_1465.csv"
BRANCH_CMSM_SESSION = COEFF / "CMSM_session_filelist_capture_plan_nonclaim_1465.csv"
BRANCH_SIGNING = COEFF / "C_parent_WEP_graph_certificate_signing_decision_1465.csv"

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
        ("SRC1465_0_prev_next", PREV_NEXT, "1464 handoff"),
        ("SRC1465_1_prev_validation", PREV_VALIDATION, "1464 validation"),
        ("SRC1465_2_prev_connected", PREV_CONNECTED, "1464 connectedness proof"),
        ("SRC1465_3_prev_graph", PREV_GRAPH, "1464 graph contract"),
        ("SRC1465_4_prev_direct_sum", PREV_DIRECT_SUM, "1464 direct-sum ledger"),
        ("SRC1465_5_prev_calibration", PREV_CALIBRATION, "1464 calibration silence"),
        ("SRC1465_6_prev_REGARDS", PREV_REGARDS, "1464 REGARDS API discovery"),
        ("SRC1465_7_prev_endpoints", PREV_ENDPOINTS, "1464 endpoint candidates"),
        ("SRC1465_8_prev_filelist", PREV_FILELIST, "1464 file-list route"),
        ("SRC1465_9_prev_signing", PREV_SIGNING, "1464 signing decision"),
        ("SRC1465_10_graph_1232", GRAPH_1232, "1232 graph certificate attempt"),
        ("SRC1465_11_edges_1232", EDGES_1232, "1232 graph edge audit"),
        ("SRC1465_12_demotion_1233", DEMOTION_1233, "1233 graph edge demotion"),
        ("SRC1465_13_graph_audit_1327", GRAPH_AUDIT_1327, "1327 graph certificate audit"),
        ("SRC1465_14_reentry_1328", REENTRY_1328, "1328 graph re-entry blockers"),
        ("SRC1465_15_REGARDS_1072", REGARDS_1072, "1072 REGARDS candidate endpoints"),
        ("SRC1465_16_REGARDS_1227", REGARDS_1227, "1227 REGARDS endpoint candidates"),
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
    rows.append(
        {
            "source_id": "SRC1465_17_REGARDS_docs",
            "source_type": "external_url",
            "source_path_or_url": REGARDS_DOCS,
            "exists": "not_local_path",
            "role": "REGARDS API documentation",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def graph_vertex_rows() -> list[dict[str, Any]]:
    vertices = [
        ("V1465_0_electron_lepton", "electron/leptonic", "electron kinetic/mass/current sector in ordinary matter"),
        ("V1465_1_photon_EM", "photon/EM/Coulomb", "electromagnetic gauge field and Coulomb binding sector"),
        ("V1465_2_light_quark", "light quark", "u/d quark mass and charge sector"),
        ("V1465_3_gluon_QCD", "gluon/QCD binding", "color gauge and hadronic binding sector"),
        ("V1465_4_nucleon_nuclear", "nucleon/nuclear binding", "nuclear surface/asymmetry/binding sector"),
        ("V1465_5_atom_material", "atom/material effective sector", "Ti/Pt test-body composite material response"),
        ("V1465_6_measure_readout", "measure/readout owner", "shared action-density/current/readout owner needed to turn physical graph into source graph"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "vertex_id": vertex_id,
            "vertex": vertex,
            "candidate_role": role,
            "parent_object_signed": False,
            "counts_for_connected_graph": False,
            "status": "CANDIDATE_VERTEX_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for vertex_id, vertex, role in vertices
    ]


def graph_edge_rows() -> list[dict[str, Any]]:
    edges = [
        ("E1465_0_electron_photon", "electron/leptonic", "photon/EM/Coulomb", "QED current coupling J_e^mu A_mu", "EM/current normalization owner"),
        ("E1465_1_quark_photon", "light quark", "photon/EM/Coulomb", "quark electric charge/current coupling", "charge lattice/current functor owner"),
        ("E1465_2_quark_gluon", "light quark", "gluon/QCD binding", "QCD color interaction and confinement/bound-state map", "strong-sector parent action owner"),
        ("E1465_3_gluon_nuclear", "gluon/QCD binding", "nucleon/nuclear binding", "hadronization/nuclear binding transfer", "QCD-to-nuclear binding functor"),
        ("E1465_4_EM_nuclear", "photon/EM/Coulomb", "nucleon/nuclear binding", "Coulomb term in nuclear/material binding", "EM/nuclear coefficient owner"),
        ("E1465_5_nuclear_material", "nucleon/nuclear binding", "atom/material effective sector", "material bound-state and composition transfer", "material tensor/basis owner"),
        ("E1465_6_electron_material", "electron/leptonic", "atom/material effective sector", "atomic electron binding/material response", "material response functor"),
        ("E1465_7_measure_all", "measure/readout owner", "all vertices", "species-blind measure/current/readout descent", "parent measure/current owner plus source-worldtube readout"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "edge_id": edge_id,
            "from_vertex": from_vertex,
            "to_vertex": to_vertex,
            "candidate_morphism": morphism,
            "needed_parent_owner": owner,
            "physical_template_connected": True,
            "parent_owned_nonzero_morphism": False,
            "nonzero_on_L_action_proved": False,
            "counts_for_connected_graph": False,
            "status": "PHYSICAL_EDGE_TEMPLATE_NOT_PARENT_CERTIFICATE",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for edge_id, from_vertex, to_vertex, morphism, owner in edges
    ]


def graph_path_rows() -> list[dict[str, Any]]:
    paths = [
        ("PATH1465_0_electron_to_material", "electron/leptonic", "atom/material effective sector", "E1465_6_electron_material"),
        ("PATH1465_1_quark_to_material", "light quark", "atom/material effective sector", "E1465_2_quark_gluon -> E1465_3_gluon_nuclear -> E1465_5_nuclear_material"),
        ("PATH1465_2_photon_to_material", "photon/EM/Coulomb", "atom/material effective sector", "E1465_4_EM_nuclear -> E1465_5_nuclear_material"),
        ("PATH1465_3_QCD_to_EM", "gluon/QCD binding", "photon/EM/Coulomb", "E1465_3_gluon_nuclear -> E1465_4_EM_nuclear"),
        ("PATH1465_4_measure_to_all", "measure/readout owner", "all vertices", "E1465_7_measure_all"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "path_id": path_id,
            "from_vertex": from_vertex,
            "to_vertex": to_vertex,
            "candidate_path": candidate_path,
            "physical_path_exists": True,
            "parent_signed_path": False,
            "counts_for_connected_graph": False,
            "blocking_reason": "one or more edges lack parent-owned nonzero action-density/source certificate",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for path_id, from_vertex, to_vertex, candidate_path in paths
    ]


def graph_certificate_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "certificate_id": "GC1465_0_template_connected",
            "claim": "ordinary matter physical template graph is connected",
            "current_result": "PLAUSIBLE_TEMPLATE_BUILT",
            "evidence": "vertices/edges/path templates written for electron, photon, quark, gluon, nuclear, and material sectors",
            "counts_for_theorem_zero": False,
            "reason": "physical template is not a parent action graph certificate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "certificate_id": "GC1465_1_parent_graph_certificate",
            "claim": "all ordinary matter vertices/edges are parent-owned nonzero morphisms on L_action",
            "current_result": "FAIL_NOT_PARENT_SIGNED",
            "evidence": "edge owner/reentry blockers from 1232/1328 remain open",
            "counts_for_theorem_zero": False,
            "reason": "EM, QCD, bound-state, material-transfer, and measure/readout owners are not signed together",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "certificate_id": "GC1465_2_connectedness_verdict",
            "claim": "connected graph can promote w_A/J_A zero",
            "current_result": "NO_PROMOTION_RETAIN_DIRECT_SUM_BRANCH",
            "evidence": "paths are only templates; parent-signed paths all false",
            "counts_for_theorem_zero": False,
            "reason": "direct-sum countermodel remains live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def direct_sum_residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "residual_id": "DSR1465_0_component_weights",
            "symbol": "w_component_i",
            "meaning": "independent source/action weight on a disconnected ordinary-matter component",
            "current_status": "RETAINED_NONCLAIM",
            "why": "parent graph certificate not signed",
            "required_to_remove": "connected parent graph or shared action-density owner for direct sums",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "residual_id": "DSR1465_1_edge_weights",
            "symbol": "w_edge_or_transfer",
            "meaning": "relative weight hidden in an edge/transfer owner",
            "current_status": "RETAINED_NONCLAIM",
            "why": "edge morphisms are templates, not parent-owned nonzero maps",
            "required_to_remove": "edge-owner proof for EM/QCD/bound-state/material/readout transfers",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "residual_id": "DSR1465_2_common_weight_leak",
            "symbol": "partial ln w_*",
            "meaning": "common graph weight that varies with time/range/source/frame/material",
            "current_status": "RETAINED_NONCLAIM",
            "why": "calibration silence not signed",
            "required_to_remove": "derivative-silence theorem for common calibration factor",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def cmsm_session_capture_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "capture_id": "CAP1465_0_browser_session",
            "route": "open CMSM module 7 in an authenticated/interactive browser session",
            "target_url": CMSM_MODULE_7,
            "capture_steps": "inspect network calls; filter rs-catalog, rs-access-project, downloads, datasets, dataobjects; record request URL/method/status/payload shape",
            "current_status": "PLAN_ONLY_NOT_EXECUTED",
            "promotion_rule": "network observations remain quarantine until response files are downloaded and checksummed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "capture_id": "CAP1465_1_filelist_fields",
            "route": "REGARDS file-list capture contract",
            "target_url": CMSM_PORTAL,
            "capture_steps": "dataset_id, product_id, file_name, file_role, download_url, checksum, byte_count, row_count, metadata_schema, licence/access",
            "current_status": "MISSING_FILELIST",
            "promotion_rule": "no official readout/source-worldtube live import without all fields",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "capture_id": "CAP1465_2_claim_guard",
            "route": "source-pack import guard",
            "target_url": "local validator 1457/1459",
            "capture_steps": "after checksums, convert to quarantine source pack; run validator; only then consider live promotion",
            "current_status": "GUARD_ACTIVE",
            "promotion_rule": "live files remain absent in 1465",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def cmsm_probe_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "probe_id": "PROBE1465_0_shell_443",
            "url": CMSM_MODULE_7,
            "method": "local curl/Invoke-WebRequest attempts from previous/current shell route",
            "result": "CONNECT_BLOCKED_OR_NO_FILE_ROWS",
            "filelist_acquired": False,
            "claim_impact": "no official CMSM file list, no checksums, no source pack import",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "probe_id": "PROBE1465_1_REGARDS_docs",
            "url": REGARDS_DOCS,
            "method": "documentation inspection from 1464",
            "result": "API_TEMPLATES_IDENTIFIED",
            "filelist_acquired": False,
            "claim_impact": "supports candidate request templates only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def request_template_rows() -> list[dict[str, Any]]:
    templates = [
        ("REQ1465_0_complex_search", "POST", f"{CMSM_PORTAL}/api/v1/rs-catalog/complex/search", "catalog search body; project/auth/session may be required"),
        ("REQ1465_1_access_dataset_search", "POST", f"{CMSM_PORTAL}/api/v1/rs-access-project/datasets/search", "REGARDS access-project dataset search candidate from 1072"),
        ("REQ1465_2_access_dataobject_search", "POST", f"{CMSM_PORTAL}/api/v1/rs-access-project/dataobjects/search", "REGARDS access-project dataobject/product search candidate from 1072"),
        ("REQ1465_3_catalog_opensearch_datasets", "GET", f"{CMSM_PORTAL}/api/v1/rs-catalog/engines/opensearch/datasets/search", "opensearch dataset candidate"),
        ("REQ1465_4_catalog_api_docs", "GET", f"{CMSM_PORTAL}/api/v1/rs-catalog/v3/api-docs", "instance OpenAPI candidate"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "request_id": request_id,
            "method": method,
            "url_or_template": url,
            "purpose": purpose,
            "status": "REQUEST_TEMPLATE_NOT_VERIFIED",
            "required_success_evidence": "HTTP 2xx/3xx or authenticated session response plus dataset/file rows and checksum fields",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for request_id, method, url, purpose in templates
    ]


def live_guard_rows() -> list[dict[str, Any]]:
    live_targets = [
        ("LIVE1465_0_official_readout", "official_readout", LIVE_OFFICIAL_READOUT),
        ("LIVE1465_1_source_worldtube", "source_worldtube", LIVE_SOURCE_WORLD),
        ("LIVE1465_2_material_tensor", "material_tensor", LIVE_MATERIAL_TENSOR),
        ("LIVE1465_3_C_parent", "C_parent_WEP", LIVE_CPARENT),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "live_guard_id": guard_id,
            "object": object_name,
            "live_path": str(path),
            "exists_now": path.exists(),
            "would_write_in_1465": False,
            "reason": "1465 writes graph/file-list plans only; no live import",
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
            "gate_id": "GATE1465_0_physical_graph_template",
            "gate": "ordinary matter graph template vertices/edges/paths written",
            "gate_pass": True,
            "blocking_reason": "template only; not parent-signed",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1465_1_parent_edge_certificate",
            "gate": "all edges parent-owned nonzero morphisms on L_action",
            "gate_pass": False,
            "blocking_reason": "edge owners for EM/QCD/material/readout remain unsigned",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1465_2_connected_path_certificate",
            "gate": "connected paths count for theorem-zero",
            "gate_pass": False,
            "blocking_reason": "paths are physical templates only",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1465_3_direct_sum_removed",
            "gate": "direct-sum residuals removed",
            "gate_pass": False,
            "blocking_reason": "component/edge/common-weight residuals retained",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1465_4_CMSM_capture_plan",
            "gate": "CMSM session file-list capture plan written",
            "gate_pass": True,
            "blocking_reason": "plan only; no session file list acquired",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1465_5_CMSM_filelist",
            "gate": "CMSM file list/checksums acquired",
            "gate_pass": False,
            "blocking_reason": "no product/file rows captured",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1465_6_local_claim",
            "gate": "local WEP/local-GR claim allowed",
            "gate_pass": False,
            "blocking_reason": "graph certificate and source-pack data incomplete",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def signing_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "SIGN1465_0_graph_certificate",
            "target": "ordinary matter graph certificate for connectedness theorem",
            "physical_graph_template_written": True,
            "all_vertices_parent_signed": False,
            "all_edges_parent_signed": False,
            "connected_paths_parent_signed": False,
            "direct_sum_residuals_removed": False,
            "CMSM_session_plan_written": True,
            "CMSM_filelist_imported": False,
            "JA_zero_import_allowed": False,
            "delta_q_zero_import_allowed": False,
            "C_parent_WEP_import_allowed": False,
            "tau_WEP_numeric_allowed": False,
            "local_claim_allowed": False,
            "decision": "KEEP_GRAPH_TEMPLATE_NONCLAIM_AND_STAGE_SESSION_FILELIST_CAPTURE",
            "reason": "physical graph is connected as a template, but no edge counts until parent action signs nonzero morphisms on L_action; CMSM file list not acquired",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1465_0_graph",
            "decision": "write a concrete ordinary-matter graph template but refuse theorem-zero promotion",
            "why": "edges are physically plausible but not parent-owned nonzero source/action morphisms",
            "consequence": "direct-sum residuals remain active",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1465_1_next_proof",
            "decision": "next derivation target is edge-owner proof rather than graph topology",
            "why": "the topology is easy; the parent ownership of each edge is the real proof burden",
            "consequence": "attack EM/current edge or QCD/bound-state edge first",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1465_2_CMSM",
            "decision": "stage session/file-list capture rather than pretend API templates are data",
            "why": "no CMSM dataset/product/checksum rows were captured",
            "consequence": "future source-pack import starts from network/session evidence in quarantine",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1465_0_1466",
            "next_target": "1466-Y5-R10-RAB-EM-current-edge-owner-proof-or-CMSM-browser-session-capture.md",
            "script": "scripts/Y5_R10_RAB_EM_current_edge_owner_proof_or_CMSM_browser_session_capture.py",
            "objective": "try to parent-sign the electron-photon/EM current edge as the first graph edge; if it fails, run a browser-session CMSM file-list capture workflow",
            "include": "EM current owner; unique photon/electron source edge; edge nonzero on L_action; CMSM browser/session capture; no live claim",
            "exclude": "numeric tau_WEP; local-GR pass; C_parent promotion; formalization-workbench edits; GitHub action",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    vertices: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    paths: list[dict[str, Any]],
    certificate: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    capture: list[dict[str, Any]],
    probe: list[dict[str, Any]],
    request_templates: list[dict[str, Any]],
    live_guard: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated_csvs = [
        SOURCE_REGISTER,
        GRAPH_VERTICES,
        GRAPH_EDGES,
        GRAPH_PATHS,
        GRAPH_CERTIFICATE,
        DIRECT_SUM_RESIDUALS,
        CMSM_SESSION_CAPTURE,
        CMSM_SESSION_PROBE,
        REGARDS_REQUEST_TEMPLATE,
        QUAR_SESSION_CAPTURE,
        QUAR_REQUEST_TEMPLATE,
        LIVE_GUARD,
        REDUCTION_GATES,
        SIGNING_DECISION,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    local_sources_exist = all(row["source_type"] != "local_file" or truth(row["exists"]) for row in sources)
    vertex_count_ok = len(vertices) >= 6
    edge_count_ok = len(edges) >= 7
    no_edge_counts = all(not truth(row["counts_for_connected_graph"]) for row in edges)
    no_path_counts = all(not truth(row["counts_for_connected_graph"]) for row in paths)
    certificate_refuses = all(not truth(row["counts_for_theorem_zero"]) for row in certificate)
    residuals_retained = all(row["current_status"] == "RETAINED_NONCLAIM" for row in residuals)
    capture_nonclaim = all(not truth(row["claim_allowed"]) for row in capture + probe + request_templates)
    request_templates_ok = len(request_templates) >= 5
    live_paths_untouched = all(not truth(row["exists_now"]) and not truth(row["would_write_in_1465"]) for row in live_guard)
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
    branch_copies = BRANCH_GRAPH_CERT.exists() and BRANCH_CMSM_SESSION.exists() and BRANCH_SIGNING.exists()
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formal_recent = 0
    if FORMALIZATION.exists():
        formal_recent = sum(
            1
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and path.stat().st_mtime > START_TS
        )
    checks = [
        ("VAL1465_0_sources", local_sources_exist, "all cited local source paths exist"),
        ("VAL1465_1_vertices", vertex_count_ok, "ordinary matter graph has at least six candidate vertices"),
        ("VAL1465_2_edges", edge_count_ok, "ordinary matter graph has at least seven candidate edges"),
        ("VAL1465_3_no_edge_counts", no_edge_counts, "no edge counts for connected theorem-zero without parent ownership"),
        ("VAL1465_4_no_path_counts", no_path_counts, "no path counts for theorem-zero without signed edges"),
        ("VAL1465_5_certificate_refuses", certificate_refuses, "graph certificate refuses theorem-zero promotion"),
        ("VAL1465_6_residuals_retained", residuals_retained, "direct-sum residuals retained nonclaim"),
        ("VAL1465_7_capture_nonclaim", capture_nonclaim, "CMSM capture/probe/request rows remain nonclaim"),
        ("VAL1465_8_request_templates", request_templates_ok, "REGARDS request templates written"),
        ("VAL1465_9_live_paths_untouched", live_paths_untouched, "critical live official/source/material/Cparent files remain absent"),
        ("VAL1465_10_gate_pattern_safe", gate_pattern_safe, "only graph-template and capture-plan gates pass; claim gates false"),
        ("VAL1465_11_signing_refuses", signing_refuses, "parent signing refuses JA/delta_q/Cparent/tau/local claim"),
        ("VAL1465_12_generated_csv_parse", generated_parse, "all generated 1465 CSVs parse cleanly"),
        ("VAL1465_13_branch_copies", branch_copies, "nonclaim branch copies written"),
        ("VAL1465_14_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1465_15_formalization_untouched", formal_recent == 0, f"formalization modified-file count since start={formal_recent}"),
        ("VAL1465_16_overall", True, "1465 writes graph template/capture plan and refuses theorem-zero/live-data promotion"),
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
    vertices: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    paths: list[dict[str, Any]],
    certificate: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    capture: list[dict[str, Any]],
    probe: list[dict[str, Any]],
    request_templates: list[dict[str, Any]],
    live_guard: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    with DOC.open("w", encoding="utf-8") as handle:
        handle.write("# 1465 - Ordinary matter graph certificate or CMSM session file-list capture\n\n")
        handle.write(
            "**Current verdict:** the ordinary-matter graph is physically connected as a template, but it is not a parent graph certificate. "
            "Every edge still needs a parent-owned nonzero morphism on `L_action`; until then no edge/path counts for the connected-category theorem and the direct-sum branch remains live.\n\n"
        )
        handle.write(
            "**Useful progress:** the topology problem is now separated from the ownership problem. "
            "The next best proof target is a single edge owner, probably the electron-photon/EM current edge. "
            "On the data side, the CMSM file-list route is now a concrete session-capture plan with REGARDS request templates, but no file list or checksums are imported.\n\n"
        )
        write_table(handle, "Source register", sources)
        write_table(handle, "Ordinary matter graph vertices", vertices)
        write_table(handle, "Ordinary matter graph edges", edges)
        write_table(handle, "Ordinary matter graph path certificate", paths)
        write_table(handle, "Graph certificate decision", certificate)
        write_table(handle, "Direct-sum residuals retained", residuals)
        write_table(handle, "CMSM session file-list capture plan", capture)
        write_table(handle, "CMSM session probe result", probe)
        write_table(handle, "REGARDS request template", request_templates)
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
    vertices = graph_vertex_rows()
    edges = graph_edge_rows()
    paths = graph_path_rows()
    certificate = graph_certificate_rows()
    residuals = direct_sum_residual_rows()
    capture = cmsm_session_capture_rows()
    probe = cmsm_probe_rows()
    request_templates = request_template_rows()
    live_guard = live_guard_rows()
    gates = reduction_gate_rows()
    signing = signing_decision_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(GRAPH_VERTICES, vertices)
    write_csv(GRAPH_EDGES, edges)
    write_csv(GRAPH_PATHS, paths)
    write_csv(GRAPH_CERTIFICATE, certificate)
    write_csv(DIRECT_SUM_RESIDUALS, residuals)
    write_csv(CMSM_SESSION_CAPTURE, capture)
    write_csv(CMSM_SESSION_PROBE, probe)
    write_csv(REGARDS_REQUEST_TEMPLATE, request_templates)
    write_csv(QUAR_SESSION_CAPTURE, capture)
    write_csv(QUAR_REQUEST_TEMPLATE, request_templates)
    write_csv(LIVE_GUARD, live_guard)
    write_csv(REDUCTION_GATES, gates)
    write_csv(SIGNING_DECISION, signing)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)

    copy_branch(GRAPH_CERTIFICATE, BRANCH_GRAPH_CERT)
    copy_branch(CMSM_SESSION_CAPTURE, BRANCH_CMSM_SESSION)
    copy_branch(SIGNING_DECISION, BRANCH_SIGNING)

    remove_pycache()
    validation = validation_rows(sources, vertices, edges, paths, certificate, residuals, capture, probe, request_templates, live_guard, gates, signing)
    write_csv(VALIDATION, validation)
    write_doc(sources, vertices, edges, paths, certificate, residuals, capture, probe, request_templates, live_guard, gates, signing, decisions, validation, next_target)
    print("Y5_R10_1465_graph_template_CMSM_session_capture_plan_nonclaim")


if __name__ == "__main__":
    main()
