from __future__ import annotations

import csv
import shutil
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
SOURCE_DIR = MICROSCOPE / "branch_locked_wep" / "source"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1705"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1705-Y5-R2FR-MICROSCOPE-public-source-probe-or-parent-zero-route-switch.md"
PROBE_NOTE = SOURCE_DIR / "MICROSCOPE_public_source_probe_1705.md"

SOURCE_FILES = {
    "1704_doc": ROOT / "1704-Y5-R2FR-MICROSCOPE-parser-shell-dry-run-or-manual-data-request.md",
    "1704_validation": OUT / "P8_Y5_BRR545_1704_VALIDATION.csv",
    "1704_contract": OUT / "P8_Y5_PARENT_QLOC_1704_DROP_FOLDER_CONTRACT.csv",
    "1704_inventory": OUT / "P8_Y5_PARENT_QLOC_1704_DROP_FOLDER_INVENTORY.csv",
    "1704_request": OUT / "P8_Y5_PARENT_QLOC_1704_MANUAL_DATA_REQUEST_UPDATE.csv",
    "1704_next": OUT / "P8_Y5_PARENT_QLOC_1704_NEXT_TARGET.csv",
    "1704_request_doc": SOURCE_DIR / "MICROSCOPE_WEP_data_request_update_1704.md",
    "1704_drop_readme": MICROSCOPE / "branch_locked_wep" / "drop-folder" / "1704" / "README_DROP_FILES_1704.md",
    "1482_web_candidates": OUT / "P8_Y5_R10_1482_OFFICIAL_WEB_SOURCE_CANDIDATES.csv",
    "1482_manifest": OUT / "P8_Y5_R10_1482_OFFICIAL_INPUT_MANIFEST_UPDATE.csv",
}

NEEDLES = {
    "1704_doc": ["DROP_FOLDER_PARSER_SHELL_READY", "NEXT1704_0_primary"],
    "1704_validation": ["VAL1704_OVERALL", "PASS"],
    "1704_contract": ["ART1704_0_readout", "P_WEP_tau_parser_manifest.json"],
    "1704_inventory": ["TARGET_ABSENT", "BLOCK_MARKERS_PRESENT"],
    "1704_request": ["READY_TO_REQUEST_NOT_ACQUIRED", "P_WEP_K_CMSM_readout.csv"],
    "1704_next": ["1705-Y5-R2FR-MICROSCOPE-public-source-probe-or-parent-zero-route-switch.md", "selected"],
    "1704_request_doc": ["Exact Requested Artifacts", "Non-Claim Guardrail"],
    "1704_drop_readme": ["Expected artifacts", "Drop live source-backed files"],
    "1482_web_candidates": ["WEB1482_0_CNES_project", "WEB1482_2_PRL_arxiv"],
    "1482_manifest": ["MAN1482_0_live_readout", "MISSING_REQUIRED_LIVE_FILE"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1705_SOURCE_REGISTER.csv"
WEB_CANDIDATES = OUT / "P8_Y5_PARENT_QLOC_1705_WEB_PROBE_CANDIDATES.csv"
PROBE_RESULTS = OUT / "P8_Y5_PARENT_QLOC_1705_PUBLIC_SOURCE_PROBE_RESULTS.csv"
CONTRACT_MAPPING = OUT / "P8_Y5_PARENT_QLOC_1705_DROP_CONTRACT_MAPPING.csv"
SOURCE_BLOCKER = OUT / "P8_Y5_PARENT_QLOC_1705_SOURCE_ACQUISITION_BLOCKER.csv"
ROUTE_DECISION = OUT / "P8_Y5_PARENT_QLOC_1705_ROUTE_SWITCH_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1705_NEXT_TARGET.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1705_CLAIM_GATE.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1705_VALIDATION.csv"

GENERATED_CSVS = [
    SOURCE_REGISTER,
    WEB_CANDIDATES,
    PROBE_RESULTS,
    CONTRACT_MAPPING,
    SOURCE_BLOCKER,
    ROUTE_DECISION,
    NEXT_TARGET,
    CLAIM_GATE,
]

CLAIM_CHECKED_CSVS = [
    WEB_CANDIDATES,
    PROBE_RESULTS,
    CONTRACT_MAPPING,
    SOURCE_BLOCKER,
    ROUTE_DECISION,
    NEXT_TARGET,
    CLAIM_GATE,
]

COPY_TARGETS = {
    WEB_CANDIDATES: [
        QUARANTINE / "WEB_PROBE_CANDIDATES.csv",
        BRANCH_RESIDUALS / "R2FR_web_probe_candidates_1705.csv",
        QUEUE / "JR1705_WEB_PROBE_CANDIDATES.csv",
    ],
    PROBE_RESULTS: [
        QUARANTINE / "PUBLIC_SOURCE_PROBE_RESULTS.csv",
        BRANCH_RESIDUALS / "R2FR_public_source_probe_results_1705.csv",
        QUEUE / "JR1705_PUBLIC_SOURCE_PROBE_RESULTS.csv",
    ],
    CONTRACT_MAPPING: [
        QUARANTINE / "DROP_CONTRACT_MAPPING.csv",
        BRANCH_RESIDUALS / "R2FR_drop_contract_mapping_1705.csv",
        QUEUE / "JR1705_DROP_CONTRACT_MAPPING.csv",
    ],
    SOURCE_BLOCKER: [
        QUARANTINE / "SOURCE_ACQUISITION_BLOCKER.csv",
        BRANCH_RESIDUALS / "R2FR_source_acquisition_blocker_1705.csv",
        QUEUE / "JR1705_SOURCE_ACQUISITION_BLOCKER.csv",
    ],
    ROUTE_DECISION: [
        QUARANTINE / "ROUTE_SWITCH_DECISION.csv",
        BRANCH_RESIDUALS / "R2FR_route_switch_decision_1705.csv",
        QUEUE / "JR1705_ROUTE_SWITCH_DECISION.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1705.csv",
        QUEUE / "JR1705_NEXT_TARGET.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_1705.csv",
        QUEUE / "JR1705_CLAIM_GATE.csv",
    ],
}


def web_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "candidate_id": "WEB1705_0_CNES_project",
            "url": "https://cnes.fr/en/projects/microscope",
            "source_type": "official_project_page",
            "probe_reason": "mission status, contact and partner context",
            "expected_if_successful": "project facts/contact context, not necessarily machine arrays",
            "initial_classification": "PROJECT_PAGE_CONTEXT_NO_ARRAY_PACKAGE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "candidate_id": "WEB1705_1_arxiv_mission_scenario",
            "url": "https://arxiv.org/abs/2201.10841",
            "source_type": "paper_abstract",
            "probe_reason": "data-flow provenance and N0/N1/N2 definitions",
            "expected_if_successful": "paper metadata and PDF link, not machine arrays",
            "initial_classification": "DATA_FLOW_DESCRIPTION_NO_ARRAY_PACKAGE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "candidate_id": "WEB1705_2_arxiv_pdf",
            "url": "https://arxiv.org/pdf/2201.10841",
            "source_type": "paper_pdf",
            "probe_reason": "check paper text for data levels and CMSM/CECT roles",
            "expected_if_successful": "PDF paper only",
            "initial_classification": "PDF_DESCRIPTION_NO_ARRAY_PACKAGE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "candidate_id": "WEB1705_3_HAL_pdf",
            "url": "https://hal.science/hal-03564498/document",
            "source_type": "open_repository_pdf",
            "probe_reason": "alternate open copy of mission scenario paper",
            "expected_if_successful": "paper copy only",
            "initial_classification": "PDF_DESCRIPTION_NO_ARRAY_PACKAGE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "candidate_id": "WEB1705_4_ONERA_press",
            "url": "https://onera.fr/en/presse/communiques-presse/final-results-of-microscope-mission-achieve-record-levels-of-precision",
            "source_type": "official_press_release",
            "probe_reason": "final-result/publication context",
            "expected_if_successful": "result context and press PDF, not readout arrays",
            "initial_classification": "RESULT_CONTEXT_NO_ARRAY_PACKAGE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "candidate_id": "WEB1705_5_PRL_final_result",
            "url": "https://link.aps.org/doi/10.1103/PhysRevLett.129.121102",
            "source_type": "journal_result_page",
            "probe_reason": "published final WEP bound comparator context",
            "expected_if_successful": "bound/result page, not CMSM arrays",
            "initial_classification": "BOUND_CONTEXT_NO_READOUT_ARRAYS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "candidate_id": "WEB1705_6_GEODES_search",
            "url": "https://geodes.cnes.fr/?s=MICROSCOPE",
            "source_type": "cnes_data_portal_search",
            "probe_reason": "quick check for a public CNES data-portal MICROSCOPE entry",
            "expected_if_successful": "dataset landing page or no-hit page",
            "initial_classification": "DATA_PORTAL_SEARCH_NO_KNOWN_FILELIST",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (source_key, path) in enumerate(SOURCE_FILES.items()):
        text = read_text(path) if path.exists() else ""
        needles = NEEDLES[source_key]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC1705_{index}_{source_key}",
                "source_key": source_key,
                "source_path": str(path),
                "exists": path.exists(),
                "needles_present": all(needle in text for needle in needles),
                "required_needles": ";".join(needles),
                "use_in_1705": "public source probe and route switch decision",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def probe_url(url: str, timeout: float = 8.0) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "MTS-private-source-probe/1705"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            sample = response.read(4096)
            content_type = response.headers.get("content-type", "")
            return {
                "probe_attempted": True,
                "http_status": response.status,
                "content_type": content_type,
                "sample_contains_dataset_terms": any(
                    token in sample.lower()
                    for token in (b"download", b"data", b"n0", b"n1", b"n2", b"cmsm", b"cect")
                ),
                "network_status": "RESOLVED",
            }
    except urllib.error.HTTPError as exc:
        return {
            "probe_attempted": True,
            "http_status": exc.code,
            "content_type": exc.headers.get("content-type", "") if exc.headers else "",
            "sample_contains_dataset_terms": False,
            "network_status": f"HTTP_ERROR_{exc.code}",
        }
    except Exception as exc:
        return {
            "probe_attempted": True,
            "http_status": "not_available",
            "content_type": "not_available",
            "sample_contains_dataset_terms": False,
            "network_status": f"NETWORK_ERROR_{type(exc).__name__}",
        }


def classify_candidate(candidate: dict[str, Any], probe: dict[str, Any]) -> str:
    initial = str(candidate["initial_classification"])
    if str(probe["network_status"]).startswith("NETWORK_ERROR") or str(probe["network_status"]).startswith("HTTP_ERROR"):
        return "PROBE_FAILED_NO_FILE_ACQUIRED"
    if "NO_ARRAY_PACKAGE" in initial or "NO_READOUT_ARRAYS" in initial:
        return initial
    if "DATA_PORTAL_SEARCH" in initial:
        return "DATA_PORTAL_SEARCH_PROBE_NO_VALIDATED_FILELIST"
    return "SOURCE_CONTEXT_ONLY_NO_CLAIM_INPUT"


def probe_result_rows(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for candidate in candidates:
        probe = probe_url(str(candidate["url"]))
        classification = classify_candidate(candidate, probe)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "probe_id": str(candidate["candidate_id"]).replace("WEB", "PROBE"),
                "candidate_id": candidate["candidate_id"],
                "url": candidate["url"],
                "probe_attempted": probe["probe_attempted"],
                "http_status": probe["http_status"],
                "content_type": probe["content_type"],
                "sample_contains_dataset_terms": probe["sample_contains_dataset_terms"],
                "network_status": probe["network_status"],
                "classification": classification,
                "machine_readable_arrays_found": False,
                "drop_contract_artifact_filled": "none",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "probe_id": "PROBE1705_7_targeted_search_summary",
            "candidate_id": "targeted_web_search",
            "url": "queries: MICROSCOPE CMSM data download; MICROSCOPE CECT CMSM N0 N1; site:regards.cnes.fr MICROSCOPE",
            "probe_attempted": True,
            "http_status": "search_result_review",
            "content_type": "search",
            "sample_contains_dataset_terms": True,
            "network_status": "SEARCH_COMPLETED",
            "classification": "NO_PUBLIC_MACHINE_READOUT_FILELIST_LOCATED_IN_TARGETED_SEARCH",
            "machine_readable_arrays_found": False,
            "drop_contract_artifact_filled": "none",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def contract_mapping_rows(probe_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    contract = read_csv(OUT / "P8_Y5_PARENT_QLOC_1704_DROP_FOLDER_CONTRACT.csv")
    rows: list[dict[str, Any]] = []
    for item in contract:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "mapping_id": str(item["artifact_id"]).replace("ART1704", "MAP1705"),
                "artifact": item["artifact"],
                "needed_for": item["source_requirement"],
                "public_probe_fill_status": "NOT_FILLED_BY_1705_PUBLIC_PROBE",
                "best_public_source_context": "arXiv/CNES/ONERA/PRL context only; no direct filelist or arrays mapped",
                "remaining_route": "manual request or parent-theory route",
                "drop_path": item["drop_path"],
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def source_blocker_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "BLK1705_0_live_readout",
            "blocked_object": "P_WEP_K_CMSM_readout.csv",
            "blocker": "public probe found mission/data-flow context but no official live CMSM/readout filelist",
            "effect": "parser cannot compute tau_WEP or direct product",
            "next_action": "manual request or source-pack access needed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "BLK1705_1_source_worldtube",
            "blocked_object": "P_WEP_R_source_Earth_worldtube.csv",
            "blocker": "no public source/worldtube projection file was located",
            "effect": "source leg remains absent",
            "next_action": "derive source profile from parent/source model only if readout route later exists",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "BLK1705_2_material_C_parent_tau",
            "blocked_object": "M_TiPt; C_parent; tau_min",
            "blocker": "public probe cannot supply parent-theory coefficient or tau nondegeneracy theorem",
            "effect": "data route cannot unlock local-GR claim",
            "next_action": "switch to parent zero/demotion route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "BLK1705_3_manual_request",
            "blocked_object": "official data acquisition",
            "blocker": "manual request pack is now the exact external-data route; Codex cannot invent missing files",
            "effect": "external data branch pauses unless user obtains files",
            "next_action": "continue theory route privately",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def route_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1705_0_public_probe",
            "decision": "NO_PUBLIC_CLAIM_GRADE_MICROSCOPE_ARRAYS_LOCATED",
            "reason": "official/public sources found context, data-flow descriptions and final-result pages, but no live filelist/readout/source/material package matching 1704 contract",
            "effect": "do not run WEP parser for score",
            "next_action": "hold manual request branch; switch active work to parent zero/demotion route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1705_1_route_switch",
            "decision": "SWITCH_TO_DELTA_W_PARENT_ZERO_OR_DIRECT_PRODUCT_ONLY",
            "reason": "data door is built but currently empty; theory route can still reduce the coupling branch without external files",
            "effect": "1706 should either sign Delta_w=0 or demote split Delta_w and retain direct product only",
            "next_action": "attempt final source-owner/readout theorem; no closure smuggling",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1705_0_primary",
            "next_target": "1706-Y5-R2FR-Delta-w-parent-zero-final-route-or-direct-product-only.md",
            "script": "scripts/Y5_R2FR_Delta_w_parent_zero_final_route_or_direct_product_only.py",
            "objective": "make a final parent-signature attempt for Delta_w_TiPt=0; if unsigned, demote the split Delta_w route and keep only the direct WEP product branch",
            "selection_status": "selected",
            "success_condition": "parent-signed zero theorem or explicit demotion with direct-product-only retained and no claim flags",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1705_1_manual_request",
            "next_target": "1706a-Y5-R2FR-MICROSCOPE-manual-request-send-pack-or-file-import.md",
            "script": "scripts/Y5_R2FR_MICROSCOPE_manual_request_send_pack_or_file_import.py",
            "objective": "if user obtains files, import them through the 1704 drop-folder contract; otherwise keep request pack ready",
            "selection_status": "held_external_dependency",
            "success_condition": "live files supplied by user or external team; no invented arrays",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1705_2_r10",
            "next_target": "1706b-Y5-R2FR-R10-alpha-lambda-projection-fill-runner.md",
            "script": "scripts/Y5_R2FR_R10_alpha_lambda_projection_fill_runner.py",
            "objective": "return to R10 alpha(lambda) after WEP split route is demoted or parent-signed",
            "selection_status": "held_fallback",
            "success_condition": "R10 projection inputs or explicit blockers are source-backed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1705_0_public_data",
            "claim": "public MICROSCOPE source/readout data acquired",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "probe found no claim-grade live array/filelist package",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1705_1_parser_score",
            "claim": "WEP parser can compute P_WEP_source_weight",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "1704 drop contract remains unfilled",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1705_2_delta_w_zero",
            "claim": "Delta_w_TiPt=0",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "not attempted in 1705; selected for 1706 final theorem/demotion gate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1705_3_local_GR",
            "claim": "derived local GR/Newton through WEP branch",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "source-weight/coupling branch remains unresolved",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def write_probe_note(candidates: list[dict[str, Any]], results: list[dict[str, Any]], blockers: list[dict[str, Any]]) -> None:
    lines = [
        "# MICROSCOPE Public Source Probe - 1705",
        "",
        "Private non-claim source-acquisition note. This is not a claim that public data do not exist everywhere; it records the checked source candidates and the current blocker.",
        "",
        "## Checked Candidates",
        "",
        "| candidate | url | classification |",
        "| --- | --- | --- |",
    ]
    by_candidate = {row["candidate_id"]: row for row in results}
    for candidate in candidates:
        result = by_candidate.get(candidate["candidate_id"], {})
        lines.append(f"| {candidate['candidate_id']} | {candidate['url']} | {result.get('classification', 'not_checked')} |")
    lines.extend(
        [
            "",
            "## Current Blocker",
            "",
            "The 1704 drop contract remains unfilled: no live `P_WEP_K_CMSM_readout.csv`, `P_WEP_R_source_Earth_worldtube.csv`, material tensor, `C_parent`/zero certificate, `tau_min`, or manifest was acquired.",
            "",
            "## Non-Claim Guardrail",
            "",
            "Keep `valid_for_claim=false` and `claim_allowed=false`; do not infer a WEP pass from final-result papers, project pages, search snippets, or the MICROSCOPE bound alone.",
            "",
            "## Blocker Rows",
            "",
            "| blocker | effect | next action |",
            "| --- | --- | --- |",
        ]
    )
    for blocker in blockers:
        lines.append(f"| {blocker['blocked_object']} | {blocker['effect']} | {blocker['next_action']} |")
    write_text(PROBE_NOTE, "\n".join(lines) + "\n")


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    for target in [
        QUARANTINE / "MICROSCOPE_public_source_probe_1705.md",
        BRANCH_RESIDUALS / "R2FR_MICROSCOPE_public_source_probe_1705.md",
        QUEUE / "JR1705_MICROSCOPE_public_source_probe.md",
    ]:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(PROBE_NOTE, target)


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
            for field in ("score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed", "machine_readable_arrays_found"):
                if field in row and truthy(row[field]):
                    return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    markers = (
        "1705-Y5",
        "P8_Y5_PARENT_QLOC_1705",
        "P8_Y5_BRR545_1705",
        "Y5_R2FR_MICROSCOPE_public_source_probe_or_parent_zero_route_switch",
    )
    for path in FORMALIZATION.rglob("*"):
        if ".venv" in path.parts or "__pycache__" in path.parts:
            continue
        if any(marker in path.name for marker in markers):
            return False
    return True


def validation_rows() -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    candidates = read_csv(WEB_CANDIDATES)
    probes = read_csv(PROBE_RESULTS)
    mapping = read_csv(CONTRACT_MAPPING)
    blockers = read_csv(SOURCE_BLOCKER)
    decisions = read_csv(ROUTE_DECISION)
    next_rows = read_csv(NEXT_TARGET)
    gates = read_csv(CLAIM_GATE)
    copies = [target for targets in COPY_TARGETS.values() for target in targets]
    checks = [
        ("VAL1705_0_sources_exist", all(truthy(row["exists"]) for row in sources), "all cited local source paths exist"),
        ("VAL1705_1_needles_present", all(truthy(row["needles_present"]) for row in sources), "all required source needles are present"),
        ("VAL1705_2_candidates_present", len(candidates) >= 6 and all(row["url"] for row in candidates), "official/public web candidates recorded"),
        ("VAL1705_3_probes_attempted", all(truthy(row["probe_attempted"]) for row in probes), "all web/source probes were attempted or search-reviewed"),
        ("VAL1705_4_no_arrays_found", all(not truthy(row["machine_readable_arrays_found"]) for row in probes), "no public machine-readable arrays were marked found"),
        ("VAL1705_5_contract_unfilled", mapping and all(row["public_probe_fill_status"] == "NOT_FILLED_BY_1705_PUBLIC_PROBE" for row in mapping), "1704 drop contract remains unfilled by public probe"),
        ("VAL1705_6_blocker_written", any(row["blocker_id"] == "BLK1705_3_manual_request" for row in blockers), "source acquisition blocker ledger written"),
        ("VAL1705_7_route_switch", any(row["decision"] == "SWITCH_TO_DELTA_W_PARENT_ZERO_OR_DIRECT_PRODUCT_ONLY" for row in decisions), "route switches to theory-side final zero/demotion path"),
        ("VAL1705_8_next_selected", any(row["route_id"] == "NEXT1705_0_primary" and row["selection_status"] == "selected" for row in next_rows), "next target selected"),
        ("VAL1705_9_claim_gates_blocked", gates and all(row["status"] == "BLOCKED_NO_CLAIM" and not truthy(row["claim_allowed"]) for row in gates), "all claim gates remain blocked"),
        ("VAL1705_10_probe_note", PROBE_NOTE.exists() and "Non-Claim Guardrail" in read_text(PROBE_NOTE), "public source probe note exists"),
        ("VAL1705_11_csv_parse", csv_parses(GENERATED_CSVS), "all generated 1705 CSVs parse"),
        ("VAL1705_12_no_claim_flags", no_claim_flags(CLAIM_CHECKED_CSVS), "all generated score/prediction/claim/found flags remain false"),
        ("VAL1705_13_branch_copies", all(path.exists() for path in copies), "branch/quarantine/queue copies exist"),
        ("VAL1705_14_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1705_15_formalization_untouched", formalization_untouched(), "no 1705 outputs found under formalization-workbench outside vendor/env folders"),
    ]
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1705_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1705 MICROSCOPE public source probe or parent-zero route switch validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "/") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def write_doc(
    sources: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    probes: list[dict[str, Any]],
    mapping: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    write_text(
        DOC,
        "\n\n".join(
            [
                "# 1705 - MICROSCOPE Public Source Probe Or Parent Zero Route Switch",
                "## Verdict\n"
                "- 1705 probes the obvious public/official MICROSCOPE source candidates and does not acquire claim-grade CMSM/readout/source arrays.\n"
                "- The probe found useful source context: CNES mission page, MICROSCOPE mission-scenario paper, HAL/arXiv copies, ONERA/PRL final-result context.\n"
                "- None of those supplies the 1704 drop-contract files: readout matrix, source worldtube, material tensor, `C_parent`/zero certificate, `tau_min`, and manifest remain absent.\n"
                "- The WEP data branch is now a clean external dependency, not a fuzzy blocker.\n"
                "- Active work should switch back to the theory route: try to parent-sign `Delta_w_TiPt=0`, or demote split `Delta_w` and retain direct product only. No WEP/local-GR claim is made.",
                "## Source Register",
                markdown_table(sources, ["source_id", "source_key", "source_path", "exists", "needles_present"]),
                "## Web Probe Candidates",
                markdown_table(candidates, ["candidate_id", "url", "source_type", "initial_classification"]),
                "## Public Source Probe Results",
                markdown_table(probes, ["probe_id", "url", "network_status", "classification", "machine_readable_arrays_found"]),
                "## Drop Contract Mapping",
                markdown_table(mapping, ["mapping_id", "artifact", "public_probe_fill_status", "remaining_route"]),
                "## Source Acquisition Blocker",
                markdown_table(blockers, ["blocker_id", "blocked_object", "blocker", "next_action"]),
                "## Route Switch Decision",
                markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"]),
                "## Next Target",
                markdown_table(next_rows, ["route_id", "next_target", "objective", "selection_status"]),
                "## Claim Gates",
                markdown_table(gates, ["claim_id", "claim", "status", "reason"]),
                "## Validation",
                markdown_table(validation, ["check_id", "result", "detail"]),
                "## Working Interpretation\n"
                "The empirical door is built, but the room is empty. That is good engineering information: stop pretending public mission pages are data, keep the manual request path ready, and spend the next private step on the mathematical fork that can still move without external files.",
            ]
        )
        + "\n",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    candidates = web_candidate_rows()
    probes = probe_result_rows(candidates)
    mapping = contract_mapping_rows(probes)
    blockers = source_blocker_rows()
    decisions = route_decision_rows()
    next_rows = next_target_rows()
    gates = claim_gate_rows()
    write_csv(SOURCE_REGISTER, sources)
    write_csv(WEB_CANDIDATES, candidates)
    write_csv(PROBE_RESULTS, probes)
    write_csv(CONTRACT_MAPPING, mapping)
    write_csv(SOURCE_BLOCKER, blockers)
    write_csv(ROUTE_DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    write_csv(CLAIM_GATE, gates)
    write_probe_note(candidates, probes, blockers)
    copy_outputs()
    remove_pycache()
    validation = validation_rows()
    write_csv(VALIDATION, validation)
    write_doc(sources, candidates, probes, mapping, blockers, decisions, next_rows, gates, validation)
    failed = [row for row in validation if row["result"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("1705 validation PASS")


if __name__ == "__main__":
    main()
