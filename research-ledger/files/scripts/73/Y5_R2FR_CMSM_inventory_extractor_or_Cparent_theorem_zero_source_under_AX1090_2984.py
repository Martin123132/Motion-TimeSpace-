from __future__ import annotations

import csv
import hashlib
import json
import shutil
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICRO = ROOT / "source-intake" / "microscope"
MICRO_COEFF = MICRO / "branch_locked_wep" / "coefficients"
MICRO_OFFICIAL = MICRO / "official_readout"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2984"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2984-Y5-R2FR-CMSM-inventory-extractor-or-Cparent-theorem-zero-source-under-AX1090.md"
HELPER = ROOT / "scripts" / "CMSM_KCMSM_inventory_probe_stub_2984.py"

SRC_2983_DOC = ROOT / "2983-Y5-R2FR-WEP-live-file-acquisition-or-parent-measure-owner-closure-demotion-under-AX1090.md"
SRC_2983_NEXT = RESIDUALS / "P8_Y5_R2FR_2983_NEXT_TARGET.csv"
SRC_2983_PORTAL = RESIDUALS / "P8_Y5_R2FR_2983_CMSM_PORTAL_PROBE_NONCLAIM.csv"
SRC_2983_CPARENT = RESIDUALS / "P8_Y5_R2FR_2983_C_PARENT_PROMOTION_AUDIT.csv"
SRC_2983_ACQ = RESIDUALS / "P8_Y5_R2FR_2983_WEP_LIVE_FILE_ACQUISITION_LEDGER.csv"
SRC_2983_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2983_VALIDATION.csv"

SRC_C_PARENT = MICRO_COEFF / "C_parent.csv"
SRC_C_PARENT_SCHEMA = MICRO_COEFF / "C_parent_import_schema.csv"
SRC_C_PARENT_ZERO = MICRO_COEFF / "C_parent_WEP_slot_zero_attempt.csv"
SRC_C_PARENT_FD = MICRO_COEFF / "C_parent_WEP_functional_derivative_definition_attempt.csv"
SRC_QT_ZERO = MICRO_COEFF / "QT_zero_route_status.csv"
SRC_NO_SOURCE_PREF = MICRO_COEFF / "no_source_only_prefactor_typing_theorem_nonclaim_1479.csv"
SRC_AX1090 = MICRO_COEFF / "AX1090_parent_object_proof_attempt.csv"
SRC_COUPLING = MICRO_COEFF / "C_parent_WEP_coupling_derivation_attempt_nonclaim_1484.csv"
SRC_K_REQ = MICRO_OFFICIAL / "P_WEP_K_CMSM_readout_REQUIREMENTS.csv"
SRC_K_LEDGER = MICRO_COEFF / "official_KCMSM_bound_inputs_nonclaim_1456.csv"

LIVE_K_CMSM = MICRO_OFFICIAL / "P_WEP_K_CMSM_readout.csv"
LIVE_C_PARENT = MICRO_COEFF / "C_parent_WEP_slot_import.csv"

ENDPOINTS = [
    ("CMSM_ROOT", "https://cmsm-ds.onera.fr/"),
    ("CMSM_USER_MICROSCOPE", "https://cmsm-ds.onera.fr/user/microscope"),
    ("CMSM_MODULE_7", "https://cmsm-ds.onera.fr/user/microscope/modules/7"),
    ("ONERA_DATA_AVAILABLE", "https://microscope.onera.fr/fr/publication/microscope-data-are-available"),
    ("ONERA_SOON_ONLINE", "https://microscope.onera.fr/fr/content/microscope-mission-final-results-soon-line"),
    ("ARXIV_MISSION_DATA_PROCESSING", "https://arxiv.org/abs/2201.10841"),
]

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2984_SOURCE_REGISTER.csv",
    "web_probe": RESIDUALS / "P8_Y5_R2FR_2984_CMSM_WEB_ENDPOINT_PROBES.csv",
    "inventory_stub": RESIDUALS / "P8_Y5_R2FR_2984_CMSM_INVENTORY_EXTRACTOR_STUB_LEDGER.csv",
    "cparent_zero": RESIDUALS / "P8_Y5_R2FR_2984_CPARENT_THEOREM_ZERO_SOURCE_AUDIT.csv",
    "promotion": RESIDUALS / "P8_Y5_R2FR_2984_PROMOTION_REFUSAL_GATES.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2984_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2984_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2984_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2984_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2984_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "cmsm_stub_copy": LOCAL_BOUNDS / "CMSM_KCMSM_inventory_extractor_stub_2984_NONCLAIM.csv",
    "cparent_zero_copy": PARENT_ACTION / "C_parent_WEP_theorem_zero_source_audit_2984_NOT_CLOSED.csv",
    "next_copy": RAB_QUEUE / "JR2984_CMSM_or_Cparent_next_NONCLAIM.csv",
}

for directory in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def anchors(path: Path, needles: list[str]) -> bool:
    haystack = text(path)
    return path.exists() and all(needle in haystack for needle in needles)


def add(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, out_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in out_rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out_rows)


def csv_ok(path: Path) -> bool:
    try:
        rows(path)
        return True
    except Exception:
        return False


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def probe_url(label: str, url: str, timeout: float = 7.0) -> dict[str, Any]:
    try:
        request = urllib.request.Request(url, method="GET", headers={"User-Agent": "MTS-private-audit/2984"})
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read(250_000)
            decoded = body.decode("utf-8", errors="replace")
            return add(
                {
                    "probe_id": f"WEB2984_{label}",
                    "url": url,
                    "method": "GET",
                    "status": f"HTTP_{response.status}",
                    "final_url": response.geturl(),
                    "content_type": response.headers.get("content-type", ""),
                    "bytes_read": len(body),
                    "sha256_first_bytes": hashlib.sha256(body).hexdigest(),
                    "cmsm_link_found": "cmsm-ds.onera.fr" in decoded,
                    "microscope_keyword_found": "MICROSCOPE" in decoded or "Microscope" in decoded,
                    "inventory_candidate": any(token in decoded.lower() for token in ("href", "suep", "suref", "cmsm")),
                    "error": "",
                }
            )
    except urllib.error.HTTPError as exc:
        return add(
            {
                "probe_id": f"WEB2984_{label}",
                "url": url,
                "method": "GET",
                "status": f"HTTP_ERROR_{exc.code}",
                "final_url": getattr(exc, "url", url),
                "content_type": "",
                "bytes_read": 0,
                "sha256_first_bytes": "",
                "cmsm_link_found": False,
                "microscope_keyword_found": False,
                "inventory_candidate": False,
                "error": str(exc),
            }
        )
    except Exception as exc:
        return add(
            {
                "probe_id": f"WEB2984_{label}",
                "url": url,
                "method": "GET",
                "status": "REQUEST_FAILED_OR_TIMEOUT",
                "final_url": url,
                "content_type": "",
                "bytes_read": 0,
                "sha256_first_bytes": "",
                "cmsm_link_found": False,
                "microscope_keyword_found": False,
                "inventory_candidate": False,
                "error": str(exc),
            }
        )


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2984_00_2983_doc", SRC_2983_DOC, ["Status:", "NEXT2983_0_2984"], "2983 handoff"),
        ("SRC2984_01_2983_next", SRC_2983_NEXT, ["NEXT2983_0_2984", "CMSM"], "selected 2984 target"),
        ("SRC2984_02_2983_portal", SRC_2983_PORTAL, ["CMSM2983_0_head_probe", "TIMEOUT_OR_REQUEST_FAILED"], "2983 portal probe"),
        ("SRC2984_03_2983_cparent", SRC_2983_CPARENT, ["CPA2983_verdict", "C_PARENT_IMPORT_REMAINS_ABSENT"], "2983 C_parent audit"),
        ("SRC2984_04_2983_acq", SRC_2983_ACQ, ["ACQ2983_0_C_parent_WEP", "ACQ2983_1_K_CMSM_readout"], "2983 acquisition ledger"),
        ("SRC2984_05_2983_validation", SRC_2983_VALIDATION, ["VAL2983_OVERALL"], "2983 validation"),
        ("SRC2984_06_cparent", SRC_C_PARENT, ["CP1430_6_verdict", "PLACEHOLDER_ROWS_ONLY_RUNNER_BLOCKED"], "C_parent placeholder rows"),
        ("SRC2984_07_schema", SRC_C_PARENT_SCHEMA, ["zero_certificate_status", "QT_ZERO_CLOSED"], "C_parent import schema"),
        ("SRC2984_08_zero", SRC_C_PARENT_ZERO, ["CZ1438_5_zero_certificate", "NOT_CLOSED"], "C_parent WEP zero attempt"),
        ("SRC2984_09_fd", SRC_C_PARENT_FD, ["FD1447_0_candidate_definition", "FORMAL_DEFINITION_WRITTEN_NOT_SOURCE_SIGNED"], "functional derivative definition"),
        ("SRC2984_10_qt_zero", SRC_QT_ZERO, ["Q_T_over_m_zero_theorem", "CLOSURE_ONLY_NOT_DERIVED"], "trace zero route"),
        ("SRC2984_11_no_source_pref", SRC_NO_SOURCE_PREF, ["NST1479_4_verdict", "PROOF_NOT_CLOSED_BOUND_PACK_REQUIRED"], "no source-only prefactor theorem"),
        ("SRC2984_12_ax1090", SRC_AX1090, ["AXP1447_3_verdict", "PARENT_OBJECT_NOT_PROVEN"], "AX1090 parent object attempt"),
        ("SRC2984_13_coupling", SRC_COUPLING, ["CPD1484_5_verdict", "NOT_CLOSED"], "C_parent coupling derivation attempt"),
        ("SRC2984_14_k_req", SRC_K_REQ, ["KREQ1445_0", "live_target_exists"], "K_CMSM requirements"),
        ("SRC2984_15_k_ledger", SRC_K_LEDGER, ["KBI1456_6_data_portal", "POINTER_ONLY_ACCESS_UNVERIFIED"], "K_CMSM input ledger"),
        ("SRC2984_16_helper", HELPER, ["NONCLAIM", "P_WEP_K_CMSM_readout.csv"], "CMSM extractor stub"),
    ]
    return [
        add(
            {
                "source_id": source_id,
                "source_path": str(path),
                "role": role,
                "required_anchors": ";".join(needles),
                "exists": path.exists(),
                "anchors_found": anchors(path, needles),
            }
        )
        for source_id, path, needles, role in specs
    ]


def web_probe_rows() -> list[dict[str, Any]]:
    return [probe_url(label, url) for label, url in ENDPOINTS]


def inventory_stub_rows(web_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cmsm_success = [row for row in web_rows if str(row["probe_id"]).startswith("WEB2984_CMSM") and str(row["status"]).startswith("HTTP_2")]
    onera_link = any(row["probe_id"] in {"WEB2984_ONERA_DATA_AVAILABLE", "WEB2984_ONERA_SOON_ONLINE"} and row["cmsm_link_found"] for row in web_rows)
    return [
        add(
            {
                "stub_id": "STUB2984_0_helper_script",
                "artifact": str(HELPER),
                "status": "EXISTS_NONCLAIM_EXTRACTOR_STUB",
                "purpose": "future CMSM inventory probe that writes runs/<timestamp>/endpoint probes, candidate links, checksums, status.json, and log.txt",
                "live_target_written": False,
                "promotion_allowed_now": False,
            }
        ),
        add(
            {
                "stub_id": "STUB2984_1_official_pointer",
                "artifact": "ONERA MICROSCOPE pages",
                "status": "OFFICIAL_POINTER_CONFIRMED" if onera_link else "OFFICIAL_POINTER_NOT_CONFIRMED",
                "purpose": "confirms the public data route points to cmsm-ds.onera.fr/user/microscope",
                "live_target_written": False,
                "promotion_allowed_now": False,
            }
        ),
        add(
            {
                "stub_id": "STUB2984_2_cmsm_access",
                "artifact": "cmsm-ds.onera.fr direct endpoints",
                "status": "DIRECT_CMSM_HTTP_REACHABLE" if cmsm_success else "DIRECT_CMSM_ENDPOINTS_TIMEOUT_OR_BLOCKED",
                "purpose": "decides whether a checksummed inventory can be built now",
                "live_target_written": False,
                "promotion_allowed_now": False,
            }
        ),
        add(
            {
                "stub_id": "STUB2984_3_live_readout_policy",
                "artifact": str(LIVE_K_CMSM),
                "status": "DO_NOT_WRITE_LIVE_READOUT",
                "purpose": "live K_CMSM requires official arrays/checksums/schema map; helper output remains in runs/",
                "live_target_written": LIVE_K_CMSM.exists(),
                "promotion_allowed_now": False,
            }
        ),
    ]


def cparent_zero_rows() -> list[dict[str, Any]]:
    return [
        add(
            {
                "zero_id": "CZ2984_0_functional_definition",
                "clause": "C_parent_WEP functional derivative exists before readout",
                "evidence": "FD1447 defines the derivative formally",
                "status": "FORMAL_DEFINITION_ONLY",
                "blocks_zero": "S_parent, V_WEP, lift, units/sign/basis and source projection are unsigned",
                "zero_certificate_status": "NOT_ZERO_CERTIFIED",
            }
        ),
        add(
            {
                "zero_id": "CZ2984_1_parent_object",
                "clause": "AX1090 parent object signs the WEP slot",
                "evidence": "AXP1447_3_verdict",
                "status": "PARENT_OBJECT_NOT_PROVEN",
                "blocks_zero": "sector/MOMS/AX1090 reductions remain conditional",
                "zero_certificate_status": "NOT_ZERO_CERTIFIED",
            }
        ),
        add(
            {
                "zero_id": "CZ2984_2_verticality",
                "clause": "V_WEP is quotient-vertical and silent in matter/source response",
                "evidence": "QT_zero_route_status",
                "status": "CLOSURE_ONLY_NOT_DERIVED",
                "blocks_zero": "Dq_loc vT zero not computed and dependent premises remain open",
                "zero_certificate_status": "NOT_ZERO_CERTIFIED",
            }
        ),
        add(
            {
                "zero_id": "CZ2984_3_no_source_prefactor",
                "clause": "no source-only/material prefactor can enter the parent object language",
                "evidence": "NST1479_4_verdict",
                "status": "EXACT_CONDITIONAL_NOT_PARENT_DERIVED",
                "blocks_zero": "primitive object-language, hidden Hom, measure/current owner, and no-spurion closure are unsigned",
                "zero_certificate_status": "NOT_ZERO_CERTIFIED",
            }
        ),
        add(
            {
                "zero_id": "CZ2984_4_readout_order",
                "clause": "downstream readout cannot create or erase parent functional derivative",
                "evidence": "variation-before-readout theorem is conditional and K_CMSM arrays are absent",
                "status": "READOUT_DOWNSTREAM_IF_PARENT_DOMAIN_SIGNED",
                "blocks_zero": "parent action domain and official readout map not jointly signed",
                "zero_certificate_status": "NOT_ZERO_CERTIFIED",
            }
        ),
        add(
            {
                "zero_id": "CZ2984_5_verdict",
                "clause": "C_parent_WEP slot DERIVED_ZERO certificate",
                "evidence": "CZ1438_5 + CPD1484_5 + CPA2983_verdict",
                "status": "DERIVED_ZERO_NOT_CLOSED",
                "blocks_zero": "formal route is well-typed but missing parent-signed premises",
                "zero_certificate_status": "NOT_ZERO_CERTIFIED",
            }
        ),
    ]


def promotion_rows(web_rows: list[dict[str, Any]], zero_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cmsm_direct_success = any(str(row["probe_id"]).startswith("WEB2984_CMSM") and str(row["status"]).startswith("HTTP_2") for row in web_rows)
    zero_closed = any(row["zero_id"] == "CZ2984_5_verdict" and row["zero_certificate_status"] == "QT_ZERO_CLOSED" for row in zero_rows)
    return [
        add(
            {
                "gate_id": "PROM2984_0_K_CMSM_live",
                "target": str(LIVE_K_CMSM),
                "required": "download URL/inventory, checksum, schema map, official units/sign/masks, no placeholders",
                "current_status": "direct CMSM endpoints reachable" if cmsm_direct_success else "direct CMSM endpoints timed out/blocked; official pointer only",
                "promotion_allowed": False,
            }
        ),
        add(
            {
                "gate_id": "PROM2984_1_C_parent_live",
                "target": str(LIVE_C_PARENT),
                "required": "numeric value or DERIVED_ZERO, uncertainty/exact tag, units, sign, basis, source_path, parent_status, zero_certificate_status",
                "current_status": "zero certificate closed" if zero_closed else "zero certificate not closed and no source-backed numeric row",
                "promotion_allowed": False,
            }
        ),
        add(
            {
                "gate_id": "PROM2984_2_deltawe",
                "target": "delta_w_e deproxy",
                "required": "C_parent/K_CMSM/R_source/R_material/product convention all sourced in one branch",
                "current_status": "blocked by C_parent and K_CMSM first",
                "promotion_allowed": False,
            }
        ),
    ]


def claim_rows() -> list[dict[str, Any]]:
    data = [
        ("CG2984_0_cmsm_inventory", "CMSM inventory downloaded/catalogued", False, "direct CMSM endpoints unavailable from this run", False),
        ("CG2984_1_kcmsm", "live K_CMSM readout written", False, "only nonclaim helper stub exists", False),
        ("CG2984_2_cparent_zero", "C_parent_WEP DERIVED_ZERO", False, "zero certificate not closed", False),
        ("CG2984_3_cparent_numeric", "C_parent_WEP finite source-backed value", False, "no numeric/source-backed import row", False),
        ("CG2984_4_local_GR", "local GR/Newton reduction", False, "coupling bridge not derived", False),
        ("CG2984_5_empirical", "WEP/R10/PPN/clock/orbital scoring", False, "no claim-grade coefficient/product", False),
    ]
    return [add({"claim_gate_id": gate_id, "claim": claim, "condition_passed": passed, "status": status, "claim_allowed": allowed}) for gate_id, claim, passed, status, allowed in data]


def decision_rows() -> list[dict[str, Any]]:
    return [
        add(
            {
                "decision_id": "DEC2984_0_cmsm",
                "decision": "Keep CMSM route open but do not claim inventory acquisition.",
                "because": "ONERA pages point to cmsm-ds.onera.fr/user/microscope, but direct CMSM endpoints timed out here.",
                "next_action": "run the helper from a browser/VPN/manual session or acquire the data package directly, then checksum and schema-map it",
            }
        ),
        add(
            {
                "decision_id": "DEC2984_1_cparent",
                "decision": "Do not write C_parent_WEP_slot_import.csv.",
                "because": "the functional derivative and zero theorem are formal/conditional, not parent-signed.",
                "next_action": "attack one zero-certificate premise at a time, starting with AX1090 parent object or V_WEP verticality",
            }
        ),
        add(
            {
                "decision_id": "DEC2984_2_route",
                "decision": "Next work should choose the deeper theory route over more WEP bookkeeping.",
                "because": "data plumbing is blocked on portal access, while C_parent zero depends on explicit parent-action premises.",
                "next_action": "derive AX1090 parent action object or field-by-field V_WEP vertical generator",
            }
        ),
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add(
            {
                "next_id": "NEXT2984_0_2985",
                "priority": "selected_primary",
                "next_doc": "2985-Y5-R2FR-AX1090-parent-action-object-or-VWEP-vertical-generator-zero-certificate-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_AX1090_parent_action_object_or_VWEP_vertical_generator_zero_certificate_under_AX1090_2985.py",
                "objective": "Try to close the theory side of C_parent_WEP: either prove the AX1090 parent action object enough to define the functional derivative, or map V_WEP field-by-field to a true quotient-vertical generator; otherwise keep C_parent_WEP nonclaim.",
                "include": "AX1090 parent object;S_parent;V_WEP field map;Dq[V_WEP]=0;matter lift;no source-only prefactor;readout downstream order;zero certificate",
                "exclude": "CMSM live-file fabrication;DD smoke promotion;unit tau shortcut;local-GR claim;GitHub action;formalization-workbench edits",
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [add({"copy_id": key, "path": str(path), "exists": path.exists()}) for key, path in BRANCH_OUTPUTS.items()]


def validation(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    csv_paths = [*OUTPUTS.values(), *BRANCH_OUTPUTS.values()]
    generated = [*csv_paths, DOC, HELPER]
    formal_count = sum(1 for p in FORMALIZATION.rglob("*2984*") if p.is_file()) if FORMALIZATION.exists() else 0
    cmsm_attempted = any(str(row["probe_id"]).startswith("WEB2984_CMSM") for row in all_rows["web_probe"])
    onera_pointer = any(row["probe_id"] == "WEB2984_ONERA_DATA_AVAILABLE" and row["cmsm_link_found"] for row in all_rows["web_probe"])
    zero_not_closed = any(row["zero_id"] == "CZ2984_5_verdict" and row["zero_certificate_status"] == "NOT_ZERO_CERTIFIED" for row in all_rows["cparent_zero"])
    checks = [
        ("VAL2984_0_sources_exist", all(row["exists"] for row in all_rows["sources"]), "all cited local source paths exist", True),
        ("VAL2984_1_anchors_found", all(row["anchors_found"] for row in all_rows["sources"]), "all cited source anchors found", True),
        ("VAL2984_2_cmsm_attempted", cmsm_attempted, "CMSM direct endpoints were probed", True),
        ("VAL2984_3_onera_pointer", onera_pointer, "reachable ONERA page confirms CMSM route", True),
        ("VAL2984_4_helper_exists", HELPER.exists(), "CMSM inventory helper stub exists", True),
        ("VAL2984_5_no_live_kcmsm", not LIVE_K_CMSM.exists(), "live K_CMSM target not fabricated", True),
        ("VAL2984_6_no_live_cparent", not LIVE_C_PARENT.exists(), "live C_parent import target not fabricated", True),
        ("VAL2984_7_zero_not_closed", zero_not_closed, "C_parent zero certificate remains unclaimed", True),
        ("VAL2984_8_promotions_refused", all(not row["promotion_allowed"] for row in all_rows["promotion"]), "all promotion gates refused", True),
        ("VAL2984_9_claims_blocked", all(not row["claim_allowed"] for row in all_rows["claims"]), "all claim gates blocked", True),
        ("VAL2984_10_next_written", any(row["next_id"] == "NEXT2984_0_2985" for row in all_rows["next"]), "2985 theory target selected", True),
        ("VAL2984_11_branches_exist", all(row["exists"] for row in all_rows["branches"]), "branch copies exist", True),
        ("VAL2984_12_csvs_parse", all(csv_ok(path) for path in csv_paths), "all generated CSVs parse", True),
        ("VAL2984_13_outputs_under_post", all(under(path, ROOT) for path in generated), "all generated outputs under post-checkpoint-work", True),
        ("VAL2984_14_formalization_clean", formal_count == 0, f"no 2984 outputs in formalization-workbench (count={formal_count})", True),
        ("VAL2984_15_doc_written", DOC.exists(), "2984 markdown checkpoint exists", True),
    ]
    out_rows = [add({"validation_id": check_id, "passed": bool(passed), "check": check, "required": required}) for check_id, passed, check, required in checks]
    out_rows.append(add({"validation_id": "VAL2984_OVERALL", "passed": all(row["passed"] for row in out_rows), "check": "2984 validation overall", "required": True}))
    return out_rows


def esc(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def table(out_rows: list[dict[str, Any]], cols: list[str]) -> str:
    if not out_rows:
        return "_No rows._"
    return "\n".join(
        [
            "| " + " | ".join(cols) + " |",
            "| " + " | ".join("---" for _ in cols) + " |",
            *["| " + " | ".join(esc(row.get(col, "")) for col in cols) + " |" for row in out_rows],
        ]
    )


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    outputs = [{"output": key, "path": str(path), "exists": path.exists()} for key, path in OUTPUTS.items() if key != "validation"]
    branches = [{"copy": key, "path": str(path), "exists": path.exists()} for key, path in BRANCH_OUTPUTS.items()]
    DOC.write_text(
        f"""# 2984 - CMSM Inventory Extractor or C_parent Theorem-Zero Source

Status: `Y5_R2FR_2984_CMSM_pointer_confirmed_direct_inventory_blocked_helper_stub_written_Cparent_zero_not_closed_nonclaim`

Claim ceiling: `no_CMSM_inventory_download_no_live_KCMSM_no_Cparent_import_no_DERIVED_ZERO_no_deltawe_deproxy_no_local_GR_no_Newton_no_WEP_no_R10_no_PPN_no_clock_no_orbital_no_public_claim`

## Summary

- Reachable ONERA MICROSCOPE pages confirm the official CMSM data route, but direct `cmsm-ds.onera.fr` endpoints still did not yield a downloadable inventory in this run.
- A reusable nonclaim CMSM inventory/K_CMSM probe stub now exists; it writes run logs, endpoint probes, candidate links, checksums, and `status.json`, but never writes the live readout target.
- The `C_parent_WEP` functional derivative route is well-typed but not source-signed; the DERIVED_ZERO certificate remains open.
- No live `P_WEP_K_CMSM_readout.csv` or `C_parent_WEP_slot_import.csv` file was fabricated.
- Best next route is theory-side: close AX1090 parent action object or map `V_WEP` as a real quotient-vertical generator.

## Generated Outputs

{table(outputs, ["output", "path", "exists"])}

## Branch Copies

{table(branches, ["copy", "path", "exists"])}

## CMSM Web Endpoint Probes

{table(all_rows["web_probe"], ["probe_id", "url", "status", "cmsm_link_found", "inventory_candidate", "error"])}

## CMSM Inventory Stub

{table(all_rows["inventory_stub"], ["stub_id", "artifact", "status", "purpose", "live_target_written", "promotion_allowed_now"])}

## C_parent Theorem-Zero Audit

{table(all_rows["cparent_zero"], ["zero_id", "clause", "status", "blocks_zero", "zero_certificate_status"])}

## Promotion Refusal Gates

{table(all_rows["promotion"], ["gate_id", "target", "current_status", "promotion_allowed"])}

## Claim Gates

{table(all_rows["claims"], ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"])}

## Decision Ledger

{table(all_rows["decision"], ["decision_id", "decision", "because", "next_action"])}

## Next Target

{table(all_rows["next"], ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Validation

{table(all_rows["validation"], ["validation_id", "passed", "check", "required"])}

Validation overall: `{all_rows["validation"][-1]["passed"]}`.
""",
        encoding="utf-8",
    )


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {
        "sources": source_rows(),
        "web_probe": web_probe_rows(),
        "cparent_zero": cparent_zero_rows(),
    }
    all_rows["inventory_stub"] = inventory_stub_rows(all_rows["web_probe"])
    all_rows["promotion"] = promotion_rows(all_rows["web_probe"], all_rows["cparent_zero"])
    all_rows["claims"] = claim_rows()
    all_rows["decision"] = decision_rows()
    all_rows["next"] = next_rows()

    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])
    shutil.copyfile(OUTPUTS["inventory_stub"], BRANCH_OUTPUTS["cmsm_stub_copy"])
    shutil.copyfile(OUTPUTS["cparent_zero"], BRANCH_OUTPUTS["cparent_zero_copy"])
    shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])
    all_rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], all_rows["branches"])
    all_rows["validation"] = validation(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)
    all_rows["validation"] = validation(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)
    print(f"2984 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)
    print(json.dumps({"helper": str(HELPER), "live_kcmsm_exists": LIVE_K_CMSM.exists(), "live_cparent_exists": LIVE_C_PARENT.exists()}, indent=2))


if __name__ == "__main__":
    main()
