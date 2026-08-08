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
QUARANTINE = MICROSCOPE / "quarantine" / "1466"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1466-Y5-R10-RAB-EM-current-edge-owner-proof-or-CMSM-browser-session-capture.md"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
START_TS = datetime.now(timezone.utc).timestamp()

PREV_NEXT = OUT / "P8_Y5_R10_1465_NEXT_TARGET.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1465_VALIDATION.csv"
PREV_EDGES = OUT / "P8_Y5_R10_1465_ORDINARY_MATTER_GRAPH_EDGES.csv"
PREV_CAPTURE = OUT / "P8_Y5_R10_1465_CMSM_SESSION_FILELIST_CAPTURE_PLAN.csv"
PREV_PROBE = OUT / "P8_Y5_R10_1465_CMSM_SESSION_PROBE_RESULT.csv"
PREV_REQUESTS = OUT / "P8_Y5_R10_1465_REGARDS_REQUEST_TEMPLATE_NONCLAIM.csv"
PREV_SIGNING = OUT / "P8_Y5_R10_1465_PARENT_SIGNING_DECISION.csv"

GRAPH_1232 = OUT / "P8_Y5_R10_1232_ORDINARY_MATTER_GRAPH_EDGE_AUDIT.csv"
GRAPH_CERT_1232 = OUT / "P8_Y5_R10_1232_INTERACTION_GRAPH_CERTIFICATE_ATTEMPT.csv"
EM_1233 = OUT / "P8_Y5_R10_1233_EM_CURRENT_EDGE_OWNER_PROOF_ATTEMPT.csv"
DEMOTION_1233 = OUT / "P8_Y5_R10_1233_GRAPH_EDGE_DEMOTION_LEDGER.csv"
ROLLUP_1327 = OUT / "P8_Y5_R10_1327_GRAPH_EDGE_STATUS_ROLLUP.csv"
REENTRY_1328 = OUT / "P8_Y5_R10_1328_GRAPH_EDGE_OWNER_REENTRY_BLOCKERS.csv"
WARD_951 = OUT / "P8_Y5_R10_951_SOURCE_CURRENT_WARD_ACTION_ATTEMPT.csv"
PARENT_990 = OUT / "P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv"
PARENT_1055 = OUT / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv"
CHARGE_1065 = OUT / "P8_Y5_R10_1065_CHARGE_INTERACTION_NORMALIZATION_AUDIT.csv"
CURRENT_1453 = OUT / "P8_Y5_R10_1453_CURRENT_SOURCE_NORMALIZATION_OWNER_THEOREM_ATTEMPT.csv"
SELECTOR_1453 = OUT / "P8_Y5_R10_1453_CURRENT_RESCALING_SELECTOR_MATRIX.csv"
SIGNING_1453 = OUT / "P8_Y5_R10_1453_PARENT_SIGNING_DECISION.csv"
REQ_1453 = OUT / "P8_Y5_R10_1453_CURRENT_SOURCE_BOUND_INPUT_REQUIREMENTS.csv"

LIVE_OFFICIAL_READOUT = MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout.csv"
LIVE_SOURCE_WORLD = MICROSCOPE / "source_worldtube" / "P_WEP_R_source_Earth_worldtube.csv"
LIVE_MATERIAL_TENSOR = MICROSCOPE / "derived" / "P_WEP_R_material_TA6V_minus_PtRh10_full_tensor.csv"
LIVE_CPARENT = COEFF / "C_parent_WEP_slot_import.csv"
LIVE_CMSM_FILELIST = MICROSCOPE / "official_filelists" / "CMSM_MICROSCOPE_filelist_checksummed.csv"
LIVE_EM_EDGE_IMPORT = COEFF / "EM_current_edge_parent_signed_import.csv"

CMSM_MODULE_7 = "https://cmsm-ds.onera.fr/user/microscope/modules/7"
CMSM_PORTAL = "https://cmsm-ds.onera.fr/user/microscope"
REGARDS_COMPLEX_SEARCH = "https://cmsm-ds.onera.fr/user/microscope/api/v1/rs-catalog/complex/search"
REGARDS_DATAOBJECT_SEARCH = "https://cmsm-ds.onera.fr/user/microscope/api/v1/rs-access-project/dataobjects/search"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1466_SOURCE_REGISTER.csv"
EM_EDGE_ATTEMPT = OUT / "P8_Y5_R10_1466_EM_CURRENT_EDGE_OWNER_PROOF_ATTEMPT.csv"
EM_REQUIREMENTS = OUT / "P8_Y5_R10_1466_EM_OWNER_REQUIREMENT_MATRIX.csv"
EM_COUNTERMODELS = OUT / "P8_Y5_R10_1466_EM_EDGE_COUNTERMODEL_LEDGER.csv"
GRAPH_EDGE_UPDATE = OUT / "P8_Y5_R10_1466_GRAPH_EDGE_STATUS_UPDATE.csv"
CMSM_CAPTURE_WORKFLOW = OUT / "P8_Y5_R10_1466_CMSM_BROWSER_SESSION_CAPTURE_WORKFLOW.csv"
CMSM_CAPTURE_RESULT = OUT / "P8_Y5_R10_1466_CMSM_SESSION_CAPTURE_RESULT_NONCLAIM.csv"
REGARDS_REUSE = OUT / "P8_Y5_R10_1466_REGARDS_REQUEST_REUSE_LEDGER.csv"
LIVE_GUARD = OUT / "P8_Y5_R10_1466_LIVE_IMPORT_GUARD.csv"
REDUCTION_GATES = OUT / "P8_Y5_R10_1466_REDUCTION_GATES.csv"
SIGNING_DECISION = OUT / "P8_Y5_R10_1466_PARENT_SIGNING_DECISION.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1466_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1466_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1466_VALIDATION.csv"

QUAR_CAPTURE_WORKFLOW = QUARANTINE / "CMSM_BROWSER_SESSION_CAPTURE_WORKFLOW_NONCLAIM.csv"
QUAR_CAPTURE_RESULT = QUARANTINE / "CMSM_SESSION_CAPTURE_RESULT_NONCLAIM.csv"
QUAR_REGARDS_REUSE = QUARANTINE / "REGARDS_REQUEST_REUSE_LEDGER_NONCLAIM.csv"

BRANCH_EM_EDGE = COEFF / "EM_current_edge_owner_proof_attempt_1466.csv"
BRANCH_CMSM_CAPTURE = COEFF / "CMSM_browser_session_capture_workflow_nonclaim_1466.csv"
BRANCH_SIGNING = COEFF / "C_parent_WEP_EM_edge_signing_decision_1466.csv"


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
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def copy_branch(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)


def formalization_modified_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and path.stat().st_mtime >= START_TS:
            count += 1
    return count


def source_rows() -> list[dict[str, Any]]:
    local_sources = [
        ("SRC1466_0_1465_next", PREV_NEXT, "1465 target explicitly requests EM-current edge proof or CMSM browser-session capture"),
        ("SRC1466_1_1465_validation", PREV_VALIDATION, "1465 validation guard and formalization boundary"),
        ("SRC1466_2_1465_edges", PREV_EDGES, "electron-photon candidate edge status from ordinary matter graph"),
        ("SRC1466_3_1465_capture", PREV_CAPTURE, "CMSM session capture plan inherited from 1465"),
        ("SRC1466_4_1465_probe", PREV_PROBE, "previous probe result: no file rows acquired"),
        ("SRC1466_5_1465_requests", PREV_REQUESTS, "REGARDS request templates inherited from 1465"),
        ("SRC1466_6_1465_signing", PREV_SIGNING, "1465 graph certificate signing refusal"),
        ("SRC1466_7_1232_edges", GRAPH_1232, "ordinary matter edge audit"),
        ("SRC1466_8_1232_certificate", GRAPH_CERT_1232, "conditional connected-graph theorem"),
        ("SRC1466_9_1233_em", EM_1233, "previous EM-current edge owner proof attempt"),
        ("SRC1466_10_1233_demotion", DEMOTION_1233, "edge demotion ledger"),
        ("SRC1466_11_1327_rollup", ROLLUP_1327, "graph edge status rollup"),
        ("SRC1466_12_1328_reentry", REENTRY_1328, "edge-owner reentry blockers"),
        ("SRC1466_13_951_ward", WARD_951, "Ward/current source action attempt"),
        ("SRC1466_14_990_parent", PARENT_990, "parent action contract including EM lock"),
        ("SRC1466_15_1055_parent", PARENT_1055, "parent action candidate including EM owner"),
        ("SRC1466_16_1065_charge", CHARGE_1065, "charge interaction normalization audit"),
        ("SRC1466_17_1453_current", CURRENT_1453, "current/source normalization owner theorem attempt"),
        ("SRC1466_18_1453_selector", SELECTOR_1453, "current rescaling selector matrix"),
        ("SRC1466_19_1453_signing", SIGNING_1453, "current owner signing decision"),
        ("SRC1466_20_1453_requirements", REQ_1453, "current/source bound input requirements"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, usage in local_sources:
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local_file",
                "path_or_url": str(path.relative_to(ROOT)),
                "exists": path.exists(),
                "usage": usage,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    rows.extend(
        [
            {
                "source_id": "SRC1466_21_CMSM_module_7",
                "source_type": "web_url_string",
                "path_or_url": CMSM_MODULE_7,
                "exists": "not_checked_by_1466",
                "usage": "manual/authenticated browser-session target for official MICROSCOPE data file-list capture",
                "valid_for_claim": False,
                "claim_allowed": False,
            },
            {
                "source_id": "SRC1466_22_CMSM_portal",
                "source_type": "web_url_string",
                "path_or_url": CMSM_PORTAL,
                "exists": "not_checked_by_1466",
                "usage": "portal context for session capture",
                "valid_for_claim": False,
                "claim_allowed": False,
            },
        ]
    )
    return rows


def em_edge_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "EME1466_0_target",
            "edge_id": "E1465_0_electron_photon",
            "claim_piece": "electron-photon/EM current edge is a parent-owned nonzero morphism on L_action",
            "formal_statement": "A_Q, F_Q^2, electron representation charge q_e, and electron current J_e are all owned by one parent action term before readout; the edge counts only if this ownership is parent-signed.",
            "result": "TARGET_REOPENED_AND_SHARPENED",
            "what_is_proved_here": "the exact conditional theorem below says what the edge would buy if the parent EM owner is real",
            "what_is_not_proved_here": "no parent derivation of unique A_Q owner, unique F2 coefficient, or source-label forgetting is supplied",
            "blocks_claim": "MISSING_PARENT_EM_OWNER_SIGNATURE",
            "counts_for_connected_graph": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "EME1466_1_action_setup",
            "edge_id": "E1465_0_electron_photon",
            "claim_piece": "minimal common EM/electron action form",
            "formal_statement": "S[A_Q,psi_e]=-(4 g_*^2)^-1 int sqrt(-g) F_Q^2 + int sqrt(-g) psi_bar_e(i gamma^mu(nabla_mu+i q_e A_Q_mu)-m_e)psi_e plus other matter terms sharing A_Q.",
            "result": "EXACT_ACTION_TEMPLATE",
            "what_is_proved_here": "if this form descends from the parent action, electron and EM sectors share an action-density slot",
            "what_is_not_proved_here": "MTS has not yet derived this as the only allowed parent-visible EM slot",
            "blocks_claim": "ACTION_TEMPLATE_NOT_PARENT_UNIQUE",
            "counts_for_connected_graph": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "EME1466_2_variation_nonzero_edge",
            "edge_id": "E1465_0_electron_photon",
            "claim_piece": "variation shows a nonzero electron-photon morphism",
            "formal_statement": "delta S/delta A_Q_nu gives nabla_mu(g_*^-2 F_Q^{mu nu})=J_e^nu+J_other^nu, while delta S/delta psi_bar_e gives a Dirac equation containing q_e A_Q; for q_e not zero and electron field support not empty, the action coupling is nonzero.",
            "result": "EXACT_CONDITIONAL_SUBTHEOREM",
            "what_is_proved_here": "standard variational structure supplies the nonzero edge once the parent action owns the common A_Q slot",
            "what_is_not_proved_here": "it does not stop a hidden gravitational source prefactor w_e multiplying the Hilbert source before variation",
            "blocks_claim": "SOURCE_WEIGHT_COUNTERMODEL_SURVIVES",
            "counts_for_connected_graph": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "EME1466_3_ward_current",
            "edge_id": "E1465_0_electron_photon",
            "claim_piece": "Ward identity supports current ownership but is not source universality",
            "formal_statement": "U(1) gauge invariance gives the conserved charge current and fixes charge-current bookkeeping inside the EM sector.",
            "result": "CONDITIONAL_WARD_CURRENT_RESULT",
            "what_is_proved_here": "electric charge is observable interaction data, not a pure invisible gravitational source weight",
            "what_is_not_proved_here": "Ward conservation is homogeneous under independent source weights and does not set w_A=1",
            "blocks_claim": "HILBERT_SOURCE_NORMALIZATION_NOT_FIXED_BY_GAUGE_WARD",
            "counts_for_connected_graph": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "EME1466_4_no_hidden_F2_needed",
            "edge_id": "E1465_0_electron_photon",
            "claim_piece": "unique EM owner must forbid hidden representative F2 slots",
            "formal_statement": "The edge becomes parent-signed only if no coefficient f(Xhat)F_Q^2, duplicate A_Q copy, or representative-dependent EM kinetic/readout branch exists.",
            "result": "REQUIREMENT_NOT_DERIVED",
            "what_is_proved_here": "this identifies the exact place the coupling hunt bites: parent uniqueness, not QED algebra",
            "what_is_not_proved_here": "the no-hidden-F2 theorem is still missing",
            "blocks_claim": "MISSING_NO_HIDDEN_F2_THEOREM",
            "counts_for_connected_graph": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "EME1466_5_verdict",
            "edge_id": "E1465_0_electron_photon",
            "claim_piece": "1466 electron-photon edge verdict",
            "formal_statement": "QED/Ward structure gives a clean exact conditional edge theorem, but connected-graph theorem-zero needs parent-signed EM owner, no hidden F2/current branch, source-label forgetting, and readout/radiative closure.",
            "result": "EXACT_CONDITIONAL_EDGE_THEOREM_NOT_PARENT_SIGNED",
            "what_is_proved_here": "the EM edge is mathematically sharp and worth keeping as the first graph edge target",
            "what_is_not_proved_here": "the edge cannot count for Delta_w=0 or local-GR/WEP/R10 claims",
            "blocks_claim": "MISSING_PARENT_OWNER_AND_SOURCE_FUNCTOR_SIGNATURES",
            "counts_for_connected_graph": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def em_requirement_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "requirement_id": "REQ1466_0_unique_AQ",
            "requirement": "unique observed EM connection owner",
            "needed_statement": "A_Q is a single parent-owned visible U(1) connection, not a representative-dependent or sector-specific copy",
            "current_status": "UNSIGNED",
            "if_signed_effect": "electron and photon slots share the same action object",
            "blocking_marker": "MISSING_PARENT_EM_OWNER_SIGNATURE",
            "counts_for_edge": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "requirement_id": "REQ1466_1_unique_F2",
            "requirement": "unique Maxwell kinetic coefficient",
            "needed_statement": "F_Q^2 has one fixed coefficient g_*^-2 or a fully sourced running law, with no hidden f(Xhat)F_Q^2 slot",
            "current_status": "UNSIGNED",
            "if_signed_effect": "alpha/EM marker channels stop re-entering as unowned local source terms",
            "blocking_marker": "MISSING_NO_HIDDEN_F2_THEOREM",
            "counts_for_edge": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "requirement_id": "REQ1466_2_electron_rep_charge",
            "requirement": "electron representation charge owner",
            "needed_statement": "q_e is fixed representation/topological data under the allowed vertical flow",
            "current_status": "CONDITIONAL_FROM_PARENT_CONTRACT",
            "if_signed_effect": "charge is interaction data rather than a tunable hidden source prefactor",
            "blocking_marker": "MISSING_REPRESENTATION_OWNER_DERIVATION",
            "counts_for_edge": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "requirement_id": "REQ1466_3_current_normalization",
            "requirement": "charge-current normalization owner",
            "needed_statement": "J_Q is extracted from the same parent action before readout and cannot be rescaled by a source-only c_A after extraction",
            "current_status": "PARTIAL_CURRENT_THEOREM_NOT_CLOSED",
            "if_signed_effect": "kills post-current rescalings inside the EM edge",
            "blocking_marker": "MISSING_CURRENT_OWNER_READOUT_ORDER",
            "counts_for_edge": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "requirement_id": "REQ1466_4_source_label_forgetting",
            "requirement": "no independent gravitational source weight",
            "needed_statement": "Hilbert/source functor forgets species labels before gravitational coupling, so no w_e or beta_source_alpha can multiply the source separately",
            "current_status": "UNSIGNED_AND_NOT_SUPPLIED_BY_EM_WARD",
            "if_signed_effect": "turns the EM edge from interaction-coupled into source-coupled for WEP/local tests",
            "blocking_marker": "MISSING_SOURCE_LABEL_FORGETTING",
            "counts_for_edge": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "requirement_id": "REQ1466_5_radiative_readout",
            "requirement": "radiative/readout closure",
            "needed_statement": "effective, renormalized, and measured readout maps preserve the same quotient/constant owner and do not regenerate Xhat-dependent EM/source coefficients",
            "current_status": "UNSIGNED",
            "if_signed_effect": "tree-level EM edge proof survives clock/WEP/R10 readout",
            "blocking_marker": "MISSING_RADIATIVE_READOUT_CLOSURE",
            "counts_for_edge": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def em_countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1466_0_hidden_F2",
            "countermodel": "S_EM contains -(4g_*^2)^-1 F^2 -(4)^-1 f_X(Xhat) F^2",
            "why_it_survives": "ordinary EM coupling can still exist while alpha/source response drifts with hidden representative data",
            "killed_by_1466": False,
            "needed_to_kill": "parent operator classification excluding hidden visible-coefficient maps",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1466_1_pre_action_source_weight",
            "countermodel": "S_source or S_matter carries w_e S_e before Hilbert/source variation",
            "why_it_survives": "Ward identities and nonzero EM interaction remain true while gravitational source normalization changes",
            "killed_by_1466": False,
            "needed_to_kill": "source-label-forgetting theorem on the parent matter/source functor",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1466_2_duplicate_AQ",
            "countermodel": "electron and Coulomb/readout use action-coupled but not quotient-identical A_Q representatives",
            "why_it_survives": "a visible interaction template does not by itself prove quotient identity of readout branches",
            "killed_by_1466": False,
            "needed_to_kill": "unique A_Q owner plus representative-readout silence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1466_3_nonHilbert_current",
            "countermodel": "J_src = kappa T_H + zeta_e J_NH,e with a non-Hilbert current component",
            "why_it_survives": "EM Noether current conservation does not rule out an extra gravitational source current",
            "killed_by_1466": False,
            "needed_to_kill": "non-Hilbert current absence theorem or sourced bound rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1466_4_radiative_readout_reentry",
            "countermodel": "tree-level owner exists but EFT/readout map generates an Xhat-dependent measured EM/source coefficient",
            "why_it_survives": "parent tree algebra alone is not enough for observed WEP/clock/R10 maps",
            "killed_by_1466": False,
            "needed_to_kill": "radiative/readout closure theorem or explicit residual bounds",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def graph_edge_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "edge_id": "E1465_0_electron_photon",
            "previous_status": "PHYSICAL_EDGE_TEMPLATE_NOT_PARENT_CERTIFICATE",
            "new_status": "EXACT_CONDITIONAL_EDGE_THEOREM_NOT_PARENT_SIGNED",
            "what_was_gained": "the nonzero EM current edge is now written as an exact conditional variational theorem",
            "what_still_blocks": "unique parent EM owner, no-hidden-F2 theorem, source-label forgetting, and readout/radiative closure",
            "counts_for_connected_graph": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "edge_id": "E1465_1_quark_photon",
            "previous_status": "PHYSICAL_EDGE_TEMPLATE_NOT_PARENT_CERTIFICATE",
            "new_status": "PENDING_AFTER_ELECTRON_PHOTON",
            "what_was_gained": "electron-photon edge provides the model for a later charge-current proof",
            "what_still_blocks": "quark representation charge owner and hadron/material transfer remain unaudited in 1466",
            "counts_for_connected_graph": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "edge_id": "E1465_7_measure_all",
            "previous_status": "PHYSICAL_EDGE_TEMPLATE_NOT_PARENT_CERTIFICATE",
            "new_status": "STILL_REQUIRED_FOR_SOURCE_READOUT",
            "what_was_gained": "EM edge proof clarifies that interaction coupling is not enough without source/readout owner",
            "what_still_blocks": "measure/readout descent and official CMSM file-list/source maps",
            "counts_for_connected_graph": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def cmsm_capture_workflow_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "step_id": "CAP1466_0_auth_browser",
            "route": "authenticated browser session",
            "target": CMSM_MODULE_7,
            "action": "open CMSM MICROSCOPE module 7 in the user's browser session and confirm the page is authenticated",
            "expected_evidence": "page title/module identity plus session cookies or authenticated network responses visible in DevTools/HAR",
            "current_status": "WORKFLOW_WRITTEN_NOT_EXECUTED_BY_1466",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "step_id": "CAP1466_1_network_filter",
            "route": "browser DevTools network capture",
            "target": "rs-catalog; rs-access-project; datasets; dataobjects; download",
            "action": "filter network traffic for REGARDS catalog/access endpoints while navigating data products",
            "expected_evidence": "request URL, method, status, payload keys, response row counts, and downloadable file metadata",
            "current_status": "WORKFLOW_WRITTEN_NOT_EXECUTED_BY_1466",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "step_id": "CAP1466_2_dataset_filelist",
            "route": "dataset/dataobject capture",
            "target": REGARDS_DATAOBJECT_SEARCH,
            "action": "capture dataset_id, product_id, file_name, file_role, checksum, byte_count, row_count, metadata_schema, and download_url",
            "expected_evidence": "machine-readable CSV/JSON rows written first to microscope/quarantine/1466",
            "current_status": "WORKFLOW_WRITTEN_NOT_EXECUTED_BY_1466",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "step_id": "CAP1466_3_download_hash",
            "route": "quarantine-only download verification",
            "target": str((QUARANTINE / "downloads").relative_to(ROOT)),
            "action": "download only official files needed for source/readout maps, compute checksums, and record provenance before parsing",
            "expected_evidence": "local checksum ledger with no live coefficient promotion",
            "current_status": "WORKFLOW_WRITTEN_NOT_EXECUTED_BY_1466",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "step_id": "CAP1466_4_source_pack",
            "route": "quarantine source-pack build",
            "target": str((QUARANTINE / "CMSM_filelist_candidate_nonclaim.csv").relative_to(ROOT)),
            "action": "convert captured file list into a source-pack candidate and run validators before any branch import",
            "expected_evidence": "no MISSING_FILELIST, MISSING_CHECKSUM, or MISSING_DOWNLOAD_URL markers",
            "current_status": "WORKFLOW_WRITTEN_NOT_EXECUTED_BY_1466",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "step_id": "CAP1466_5_import_guard",
            "route": "promotion guard",
            "target": "branch_locked_wep coefficients",
            "action": "promote nothing unless official source/readout files are checksummed, parsed, and validation says claim gates are open",
            "expected_evidence": "future validation must explicitly flip valid_for_claim to true from sourced rows, not from this workflow",
            "current_status": "GUARD_ACTIVE_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def cmsm_capture_result_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "capture_id": "PROBE1466_0_browser_session",
            "route": "CMSM authenticated browser-session capture",
            "executed_in_1466": False,
            "result": "NOT_EXECUTED_NO_AUTHENTICATED_BROWSER_CAPTURE_ATTACHED",
            "filelist_acquired": False,
            "checksums_acquired": False,
            "download_urls_acquired": False,
            "claim_impact": "no official source/readout file list imported; all CMSM data remains quarantine-only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "capture_id": "PROBE1466_1_request_templates",
            "route": "reuse 1465 REGARDS request templates",
            "executed_in_1466": False,
            "result": "TEMPLATES_STAGED_ONLY",
            "filelist_acquired": False,
            "checksums_acquired": False,
            "download_urls_acquired": False,
            "claim_impact": "request strings are not data and cannot unlock WEP/local claims",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def regards_reuse_rows() -> list[dict[str, Any]]:
    templates = [
        ("REQ1466_0_complex_search", "POST", REGARDS_COMPLEX_SEARCH, "catalog complex search candidate"),
        ("REQ1466_1_dataobjects", "POST", REGARDS_DATAOBJECT_SEARCH, "access-project dataobject/product search candidate"),
        ("REQ1466_2_module_7", "GET", CMSM_MODULE_7, "human/browser module target"),
        ("REQ1466_3_portal", "GET", CMSM_PORTAL, "portal root context"),
        ("REQ1466_4_filelist_contract", "LOCAL_CONTRACT", str((QUARANTINE / "CMSM_filelist_candidate_nonclaim.csv").relative_to(ROOT)), "required captured file-list shape"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "request_id": request_id,
            "method": method,
            "url_or_template": url,
            "purpose": purpose,
            "status": "REUSED_OR_STAGED_NOT_VERIFIED",
            "required_success_evidence": "authenticated response plus dataset/product/file rows and checksums",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for request_id, method, url, purpose in templates
    ]


def live_guard_rows() -> list[dict[str, Any]]:
    guarded_paths = [
        ("LG1466_0_official_readout", LIVE_OFFICIAL_READOUT, "official MICROSCOPE readout kernel"),
        ("LG1466_1_source_worldtube", LIVE_SOURCE_WORLD, "source worldtube/projection table"),
        ("LG1466_2_material_tensor", LIVE_MATERIAL_TENSOR, "material tensor from official data"),
        ("LG1466_3_Cparent", LIVE_CPARENT, "live C_parent WEP coefficient import"),
        ("LG1466_4_CMSM_filelist", LIVE_CMSM_FILELIST, "live CMSM official file-list import"),
        ("LG1466_5_EM_edge_import", LIVE_EM_EDGE_IMPORT, "live parent-signed EM edge import"),
    ]
    return [
        {
            "guard_id": guard_id,
            "path": str(path.relative_to(ROOT)),
            "meaning": meaning,
            "exists_now": path.exists(),
            "would_write_in_1466": False,
            "status": "ABSENT_EXPECTED" if not path.exists() else "PRESENT_PREEXISTING_REVIEW_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for guard_id, path, meaning in guarded_paths
    ]


def reduction_gate_rows(edge_attempt: list[dict[str, Any]], capture_workflow: list[dict[str, Any]]) -> list[dict[str, Any]]:
    edge_sharpened = any(row["result"] == "EXACT_CONDITIONAL_EDGE_THEOREM_NOT_PARENT_SIGNED" for row in edge_attempt)
    return [
        {
            "gate_id": "GATE1466_0_exact_conditional_edge",
            "gate": "QED/Ward variational edge theorem is stated exactly",
            "gate_pass": edge_sharpened,
            "claim_effect": "math sharpened only; no connected-graph count",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1466_1_parent_EM_owner",
            "gate": "unique parent EM owner is signed",
            "gate_pass": False,
            "claim_effect": "edge cannot count without this",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1466_2_no_hidden_F2",
            "gate": "no representative-dependent F2/current coefficient slot",
            "gate_pass": False,
            "claim_effect": "alpha/Coulomb branch remains open",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1466_3_source_label_forgetting",
            "gate": "EM interaction owner also forbids source-only species weights",
            "gate_pass": False,
            "claim_effect": "WEP/local source universality remains unclaimed",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1466_4_CMSM_workflow_written",
            "gate": "browser-session capture workflow is written",
            "gate_pass": len(capture_workflow) >= 6,
            "claim_effect": "workflow only; no data imported",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1466_5_CMSM_filelist_acquired",
            "gate": "official CMSM file list and checksums acquired",
            "gate_pass": False,
            "claim_effect": "official data source pack remains missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1466_6_local_claim",
            "gate": "local GR/WEP/R10 claim allowed",
            "gate_pass": False,
            "claim_effect": "explicitly forbidden in 1466",
            "valid_for_claim": False,
        },
    ]


def signing_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "SIGN1466_0_EM_edge",
            "target": "electron-photon/EM current edge owner",
            "exact_conditional_edge_theorem": True,
            "unique_parent_EM_owner_signed": False,
            "unique_F2_current_owner_signed": False,
            "source_label_forgetting_signed": False,
            "radiative_readout_closure_signed": False,
            "CMSM_filelist_imported": False,
            "edge_counts_for_connected_graph": False,
            "Delta_w_zero_import_allowed": False,
            "C_parent_WEP_import_allowed": False,
            "tau_WEP_numeric_allowed": False,
            "local_claim_allowed": False,
            "decision": "KEEP_EM_EDGE_AS_EXACT_CONDITIONAL_NOT_PARENT_SIGNED_AND_STAGE_CMSM_BROWSER_CAPTURE",
            "reason": "the coupling is real as conditional action math, but parent uniqueness/source functor/readout data are still missing",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1466_0_math",
            "decision": "retain the electron-photon edge as the first serious graph-edge target",
            "why": "the variational QED/Ward structure gives a clean exact conditional nonzero edge",
            "consequence": "future proof work should focus on parent EM owner uniqueness rather than re-proving the obvious interaction",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1466_1_no_promotion",
            "decision": "do not count the edge for connectedness or source-universality",
            "why": "source-only weights, hidden F2 coefficients, and readout/radiative reentry all survive",
            "consequence": "Delta_w, WEP, R10, PPN, clock, and local-GR branches remain blocked",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1466_2_CMSM",
            "decision": "stage the browser-session capture path but import no official data",
            "why": "no authenticated CMSM file list/checksum evidence is attached to this run",
            "consequence": "the next data step is an actual captured file-list/source-pack session, not a claim",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1466_0_1467",
            "next_target": "1467-Y5-R10-RAB-unique-EM-owner-no-hidden-F2-proof-or-CMSM-browser-session-run.md",
            "script": "scripts/Y5_R10_RAB_unique_EM_owner_no_hidden_F2_proof_or_CMSM_browser_session_run.py",
            "objective": "try to derive the unique EM owner/no-hidden-F2 theorem; if still unsigned, perform or record the actual CMSM authenticated file-list capture",
            "include": "unique A_Q owner; no f(Xhat)F_Q^2 slot; charge-current normalization; source-label forgetting impact; CMSM session evidence if available",
            "exclude": "local-GR pass; WEP/R10 claim; C_parent promotion; formalization-workbench edits; GitHub action",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def generated_csvs() -> list[Path]:
    return [
        SOURCE_REGISTER,
        EM_EDGE_ATTEMPT,
        EM_REQUIREMENTS,
        EM_COUNTERMODELS,
        GRAPH_EDGE_UPDATE,
        CMSM_CAPTURE_WORKFLOW,
        CMSM_CAPTURE_RESULT,
        REGARDS_REUSE,
        QUAR_CAPTURE_WORKFLOW,
        QUAR_CAPTURE_RESULT,
        QUAR_REGARDS_REUSE,
        LIVE_GUARD,
        REDUCTION_GATES,
        SIGNING_DECISION,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]


def csv_parse_clean(paths: list[Path]) -> bool:
    try:
        for path in paths:
            rows = read_csv_rows(path)
            if not rows:
                return False
        return True
    except Exception:
        return False


def branch_copies_exist() -> bool:
    return BRANCH_EM_EDGE.exists() and BRANCH_CMSM_CAPTURE.exists() and BRANCH_SIGNING.exists()


def validation_rows(
    sources: list[dict[str, Any]],
    edge_attempt: list[dict[str, Any]],
    requirements: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    graph_update: list[dict[str, Any]],
    capture_workflow: list[dict[str, Any]],
    capture_result: list[dict[str, Any]],
    regards_reuse: list[dict[str, Any]],
    live_guard: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    local_sources_exist = all(row["source_type"] != "local_file" or truth(row["exists"]) for row in sources)
    exact_conditional_edge = any(row["result"] == "EXACT_CONDITIONAL_EDGE_THEOREM_NOT_PARENT_SIGNED" for row in edge_attempt)
    no_edge_promotion = all(not truth(row["counts_for_connected_graph"]) for row in edge_attempt + graph_update)
    requirement_markers = {row["blocking_marker"] for row in requirements}
    requirements_cover_gaps = {
        "MISSING_PARENT_EM_OWNER_SIGNATURE",
        "MISSING_NO_HIDDEN_F2_THEOREM",
        "MISSING_SOURCE_LABEL_FORGETTING",
        "MISSING_RADIATIVE_READOUT_CLOSURE",
    }.issubset(requirement_markers)
    countermodels_retained = all(not truth(row["killed_by_1466"]) for row in countermodels)
    capture_nonclaim = all(not truth(row["claim_allowed"]) for row in capture_workflow + capture_result + regards_reuse)
    capture_not_imported = all(not truth(row["filelist_acquired"]) for row in capture_result)
    regards_templates_ok = len(regards_reuse) >= 5
    live_paths_untouched = all(not truth(row["exists_now"]) and not truth(row["would_write_in_1466"]) for row in live_guard)
    safe_gate_pattern = truth(gates[0]["gate_pass"]) and truth(gates[4]["gate_pass"]) and all(
        not truth(row["gate_pass"]) for row in gates[1:4] + gates[5:]
    )
    signing_refuses = all(
        truth(row["exact_conditional_edge_theorem"])
        and not truth(row["edge_counts_for_connected_graph"])
        and not truth(row["Delta_w_zero_import_allowed"])
        and not truth(row["C_parent_WEP_import_allowed"])
        and not truth(row["tau_WEP_numeric_allowed"])
        and not truth(row["local_claim_allowed"])
        for row in signing
    )
    generated_parse = csv_parse_clean(generated_csvs())
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_untouched = formalization_modified_count() == 0

    checks = [
        ("VAL1466_0_sources", local_sources_exist, "all cited local source paths exist"),
        ("VAL1466_1_exact_edge", exact_conditional_edge, "exact conditional EM-current edge theorem written"),
        ("VAL1466_2_no_edge_promotion", no_edge_promotion, "edge does not count for connected graph"),
        ("VAL1466_3_requirement_gaps", requirements_cover_gaps, "parent EM owner/no-hidden-F2/source/readout gaps are explicit"),
        ("VAL1466_4_countermodels", countermodels_retained, "all EM/source countermodels retained"),
        ("VAL1466_5_capture_nonclaim", capture_nonclaim, "capture workflow/request rows remain nonclaim"),
        ("VAL1466_6_capture_not_imported", capture_not_imported, "no CMSM file list/checksums imported"),
        ("VAL1466_7_regards_templates", regards_templates_ok, "REGARDS/CMSM request reuse ledger has enough templates"),
        ("VAL1466_8_live_paths_untouched", live_paths_untouched, "critical live official/source/material/Cparent/EM files remain absent"),
        ("VAL1466_9_gate_pattern_safe", safe_gate_pattern, "only math-sharpening and workflow gates pass; claim gates false"),
        ("VAL1466_10_signing_refuses", signing_refuses, "parent signing refuses edge promotion and local claims"),
        ("VAL1466_11_generated_csv_parse", generated_parse, "all generated 1466 CSVs parse cleanly"),
        ("VAL1466_12_branch_copies", branch_copies_exist(), "nonclaim branch copies written"),
        ("VAL1466_13_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1466_14_formalization_untouched", formalization_untouched, f"formalization modified-file count since start={formalization_modified_count()}"),
    ]
    overall = all(result for _, result, _ in checks)
    checks.append(
        (
            "VAL1466_15_overall",
            overall,
            "1466 sharpens the EM-current edge but refuses graph/local/data promotion",
        )
    )
    generated = now()
    return [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "generated_utc": generated,
        }
        for check_id, result, detail in checks
    ]


def write_doc(
    sources: list[dict[str, Any]],
    edge_attempt: list[dict[str, Any]],
    requirements: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    graph_update: list[dict[str, Any]],
    capture_workflow: list[dict[str, Any]],
    capture_result: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    lines: list[str] = []
    lines.append("# 1466 - Y5 R10 RAB EM Current Edge Owner Proof Or CMSM Browser Session Capture")
    lines.append("")
    lines.append("## Verdict")
    lines.append("- The electron-photon/EM current edge is now sharpened into an exact conditional variational theorem.")
    lines.append("- The edge is not parent-signed: unique parent `A_Q`, no hidden `F_Q^2` slot, source-label forgetting, and radiative/readout closure are still missing.")
    lines.append("- No `Delta_w=0`, WEP, R10, PPN, clock, orbital, local-GR, or `C_parent` claim is allowed from this checkpoint.")
    lines.append("- Because the proof did not close, 1466 writes the CMSM authenticated browser-session capture workflow but imports no official data.")
    lines.append("")
    lines.append("## Source Register")
    lines.append("| source_id | type | exists | path_or_url | usage |")
    lines.append("|---|---:|---:|---|---|")
    for row in sources:
        lines.append(f"| {row['source_id']} | {row['source_type']} | {row['exists']} | `{row['path_or_url']}` | {row['usage']} |")
    lines.append("")
    lines.append("## EM Edge Proof Attempt")
    lines.append("| proof_id | result | blocks_claim | counts_for_connected_graph |")
    lines.append("|---|---|---|---:|")
    for row in edge_attempt:
        lines.append(f"| {row['proof_id']} | {row['result']} | {row['blocks_claim']} | {row['counts_for_connected_graph']} |")
    lines.append("")
    lines.append("### Exact Conditional Theorem")
    lines.append("If the parent action owns one observed EM connection `A_Q`, one Maxwell kinetic coefficient `g_*^-2`, and the electron representation charge `q_e` before readout, then")
    lines.append("")
    lines.append("`delta S/delta A_Q_nu -> nabla_mu(g_*^-2 F_Q^{mu nu}) = J_e^nu + J_other^nu`")
    lines.append("")
    lines.append("and the electron equation of motion contains `q_e A_Q`. For `q_e != 0` and non-empty electron support, this is a nonzero electron-photon action morphism.")
    lines.append("")
    lines.append("What this theorem does **not** prove is just as important: it does not forbid pre-variation source weights, duplicate EM representatives, hidden `f(Xhat)F_Q^2` coefficients, non-Hilbert currents, or radiative/readout reentry.")
    lines.append("")
    lines.append("## Missing Parent Signatures")
    lines.append("| requirement_id | requirement | status | blocking_marker |")
    lines.append("|---|---|---|---|")
    for row in requirements:
        lines.append(f"| {row['requirement_id']} | {row['requirement']} | {row['current_status']} | {row['blocking_marker']} |")
    lines.append("")
    lines.append("## Countermodels Retained")
    lines.append("| countermodel_id | killed_by_1466 | needed_to_kill |")
    lines.append("|---|---:|---|")
    for row in countermodels:
        lines.append(f"| {row['countermodel_id']} | {row['killed_by_1466']} | {row['needed_to_kill']} |")
    lines.append("")
    lines.append("## Graph Edge Update")
    lines.append("| edge_id | new_status | counts_for_connected_graph |")
    lines.append("|---|---|---:|")
    for row in graph_update:
        lines.append(f"| {row['edge_id']} | {row['new_status']} | {row['counts_for_connected_graph']} |")
    lines.append("")
    lines.append("## CMSM Browser Session Workflow")
    lines.append("| step_id | route | status |")
    lines.append("|---|---|---|")
    for row in capture_workflow:
        lines.append(f"| {row['step_id']} | {row['route']} | {row['current_status']} |")
    lines.append("")
    lines.append("## CMSM Capture Result")
    lines.append("| capture_id | result | filelist_acquired | checksums_acquired |")
    lines.append("|---|---|---:|---:|")
    for row in capture_result:
        lines.append(f"| {row['capture_id']} | {row['result']} | {row['filelist_acquired']} | {row['checksums_acquired']} |")
    lines.append("")
    lines.append("## Gates")
    lines.append("| gate_id | gate_pass | claim_effect |")
    lines.append("|---|---:|---|")
    for row in gates:
        lines.append(f"| {row['gate_id']} | {row['gate_pass']} | {row['claim_effect']} |")
    lines.append("")
    lines.append("## Parent Signing Decision")
    for row in signing:
        lines.append(f"- `{row['decision_id']}`: `{row['decision']}` because {row['reason']}.")
    lines.append("")
    lines.append("## Decision Ledger")
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} - {row['consequence']}.")
    lines.append("")
    lines.append("## Validation")
    lines.append("| check_id | result | detail |")
    lines.append("|---|---|---|")
    for row in validation:
        lines.append(f"| {row['check_id']} | {row['result']} | {row['detail']} |")
    lines.append("")
    lines.append("## Next Target")
    for row in next_target:
        lines.append(f"- `{row['next_target']}` via `{row['script']}`: {row['objective']}")
    lines.append("")
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    sources = source_rows()
    edge_attempt = em_edge_attempt_rows()
    requirements = em_requirement_rows()
    countermodels = em_countermodel_rows()
    graph_update = graph_edge_update_rows()
    capture_workflow = cmsm_capture_workflow_rows()
    capture_result = cmsm_capture_result_rows()
    regards_reuse = regards_reuse_rows()
    live_guard = live_guard_rows()
    gates = reduction_gate_rows(edge_attempt, capture_workflow)
    signing = signing_decision_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(EM_EDGE_ATTEMPT, edge_attempt)
    write_csv(EM_REQUIREMENTS, requirements)
    write_csv(EM_COUNTERMODELS, countermodels)
    write_csv(GRAPH_EDGE_UPDATE, graph_update)
    write_csv(CMSM_CAPTURE_WORKFLOW, capture_workflow)
    write_csv(CMSM_CAPTURE_RESULT, capture_result)
    write_csv(REGARDS_REUSE, regards_reuse)
    write_csv(QUAR_CAPTURE_WORKFLOW, capture_workflow)
    write_csv(QUAR_CAPTURE_RESULT, capture_result)
    write_csv(QUAR_REGARDS_REUSE, regards_reuse)
    write_csv(LIVE_GUARD, live_guard)
    write_csv(REDUCTION_GATES, gates)
    write_csv(SIGNING_DECISION, signing)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)

    copy_branch(EM_EDGE_ATTEMPT, BRANCH_EM_EDGE)
    copy_branch(CMSM_CAPTURE_WORKFLOW, BRANCH_CMSM_CAPTURE)
    copy_branch(SIGNING_DECISION, BRANCH_SIGNING)

    validation = validation_rows(
        sources,
        edge_attempt,
        requirements,
        countermodels,
        graph_update,
        capture_workflow,
        capture_result,
        regards_reuse,
        live_guard,
        gates,
        signing,
    )
    write_csv(VALIDATION, validation)
    write_doc(
        sources,
        edge_attempt,
        requirements,
        countermodels,
        graph_update,
        capture_workflow,
        capture_result,
        gates,
        signing,
        decisions,
        validation,
        next_target,
    )
    print("Y5_R10_1466_EM_current_edge_conditional_not_parent_signed_CMSM_workflow_nonclaim")


if __name__ == "__main__":
    main()
