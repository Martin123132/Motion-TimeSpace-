from __future__ import annotations

import urllib.error
import urllib.request
from pathlib import Path

from Y5_R2FR_Dq_vX_observed_metric_zero_or_finite_DObs_leak_row_2025 import (
    BRANCH_WEP,
    OUT,
    QUEUE,
    ROOT,
    SOURCE_WEIGHT_DOCS,
    base_row,
    count_formalization_modified,
    csv_rows_parse,
    md_table,
    read_text,
    remove_pycache,
    write_csv,
)


DOC = ROOT / "2120-Y5-R2FR-MICROSCOPE-numeric-source-readout-kernel-acquisition.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
WEB_DIR = ROOT / "source-intake" / "wep-sources" / "2120"

CSV_2119_NEXT = OUT / "P8_Y5_PARENT_QLOC_2119_NEXT_TARGET.csv"
CSV_2119_VAL = OUT / "P8_Y5_BRR545_2119_VALIDATION.csv"
CSV_1071_KERNEL = OUT / "P8_Y5_R10_1071_OFFICIAL_KERNEL_COMPONENTS.csv"
CSV_1068_ORBIT = OUT / "P8_Y5_R10_1068_MICROSCOPE_ORBIT_READOUT_REQUIREMENTS.csv"
CSV_1068_SOURCE = OUT / "P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv"
CSV_1084_READOUT = OUT / "P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv"
CSV_1900_TARGETS = OUT / "P8_Y5_PARENT_QLOC_1900_OFFICIAL_READOUT_DATA_TARGETS_NONCLAIM.csv"
CSV_1071_SEGMENTS = OUT / "P8_Y5_R10_1071_SUEP_SEGMENT_TABLE_SOURCE_BACKED.csv"
CSV_1075_SURROGATE = OUT / "P8_Y5_R10_1075_SURROGATE_DESIGN_MATRIX_SEGMENT210.csv"

CMSM_TEMPLATE = ROOT / "source-intake" / "microscope_cmsm" / "TEMPLATE_2001_expected_official_array_schema.csv"
CMSM_README = ROOT / "source-intake" / "microscope_cmsm" / "README_2001_DROP_CMSM_EXPORTS_HERE.txt"
DROP_README = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "drop-folder" / "1704" / "README_DROP_FILES_1704.md"
DROP_TEMPLATE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "drop-folder" / "1704" / "templates" / "P_WEP_K_CMSM_readout_TEMPLATE.csv"
DROP_LIVE_READOUT = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "drop-folder" / "1704" / "live" / "P_WEP_K_CMSM_readout.csv"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid", "claim_allowed"}


def formalization_has_2120_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2120-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2120*",
        "*Y5_R2FR_MICROSCOPE_numeric_source_readout_kernel_acquisition_2120*",
        "*AFRAME_MICROSCOPE_NUMERIC_2120*",
        "*JR2120_CMSM*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def fetch_probe(probe_id: str, url: str, role: str) -> dict[str, object]:
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    local_path = WEB_DIR / f"{probe_id}.html"
    status = "FETCH_NOT_ATTEMPTED"
    status_code = ""
    content_type = ""
    bytes_written = 0
    contains_data_pointer = False
    error = ""
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "MTS-private-acquisition-check/2120"})
        with urllib.request.urlopen(request, timeout=20) as response:
            status_code = str(getattr(response, "status", ""))
            content_type = response.headers.get("content-type", "")
            payload = response.read(200_000)
        local_path.write_bytes(payload)
        bytes_written = len(payload)
        text = payload.decode("utf-8", errors="replace").lower()
        contains_data_pointer = any(token in text for token in ("cmsm", "microscope", "data", "suep", "suref"))
        status = "FETCHED_SMALL_PAGE"
    except urllib.error.HTTPError as exc:
        status_code = str(exc.code)
        error = f"HTTPError: {exc.reason}"
        status = "HTTP_ERROR_RECORDED"
        try:
            payload = exc.read(50_000)
            local_path.write_bytes(payload)
            bytes_written = len(payload)
        except Exception:
            pass
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
        status = "FETCH_FAILED_RECORDED"
    return row(
        probe_id=probe_id,
        url=url,
        role=role,
        local_path=str(local_path),
        status=status,
        status_code=status_code,
        content_type=content_type,
        bytes_written=bytes_written,
        contains_data_pointer=contains_data_pointer,
        usable_numeric_arrays=False,
        error=error,
    )


def web_probe_rows() -> list[dict[str, object]]:
    probes = [
        ("WEB2120_0_ONERA_data_available", "https://microscope.onera.fr/fr/publication/microscope-data-are-available", "official page saying MICROSCOPE data are available through CMSM"),
        ("WEB2120_1_CMSM_user_microscope", "https://cmsm-ds.onera.fr/user/microscope", "CMSM MICROSCOPE user portal, possible interactive/data route"),
        ("WEB2120_2_CMSM_root", "https://cmsm-ds.onera.fr/", "CMSM data server root"),
        ("WEB2120_3_arxiv_mission_scenario", "https://arxiv.org/abs/2201.10841", "mission scenario, ground segment and data processing paper"),
    ]
    return [fetch_probe(probe_id, url, role) for probe_id, url, role in probes]


def source_register_rows(web_csv: Path) -> list[dict[str, object]]:
    specs = [
        ("SRC2120_00_2119_next", CSV_2119_NEXT, ["NEXT2119_0_2120", "numeric MICROSCOPE"], "2119 selects MICROSCOPE numeric kernel acquisition."),
        ("SRC2120_01_2119_validation", CSV_2119_VAL, ["VAL2119_OVERALL", "PASS"], "2119 validation passed."),
        ("SRC2120_02_1071_kernel", CSV_1071_KERNEL, ["KER1071_6_verdict", "KERNEL_SKELETON_YES_NUMERIC_TAU_NO"], "1071 official kernel skeleton but no numeric tau."),
        ("SRC2120_03_1068_orbit", CSV_1068_ORBIT, ["ORB1068_5_verdict", "ORBIT_READOUT_NOT_ACQUIRED"], "1068 orbit/readout requirements."),
        ("SRC2120_04_1068_source", CSV_1068_SOURCE, ["SWT1068_5_verdict", "SOURCE_WORLDTUBE_NOT_ACQUIRED"], "1068 source-worldtube requirements."),
        ("SRC2120_05_1084_readout", CSV_1084_READOUT, ["RIG1084_0_CMSM_arrays", "OFFICIAL_ARRAYS_NOT_IMPORTED"], "1084 CMSM arrays import gate."),
        ("SRC2120_06_1900_targets", CSV_1900_TARGETS, ["OFFICIAL_DATA_TARGET_NOT_ACQUIRED_NONCLAIM", "SURROGATE_DESIGN_MATRIX_NOT_OFFICIAL"], "1900 official readout target ledger."),
        ("SRC2120_07_segments", CSV_1071_SEGMENTS, ["SUEP1071_210", "segment/window metadata only"], "local source-backed segment metadata."),
        ("SRC2120_08_surrogate", CSV_1075_SURROGATE, ["DMROW1075_000", "SURROGATE_DESIGN_MATRIX_NOT_OFFICIAL"], "local surrogate design matrix."),
        ("SRC2120_09_cmsm_template", CMSM_TEMPLATE, ["segment_id", "gx", "Sxz"], "expected CMSM array schema template."),
        ("SRC2120_10_drop_template", DROP_TEMPLATE, ["same_parent_branch_id", "gx", "gz"], "branch-locked WEP drop template."),
        ("SRC2120_11_web_probe", web_csv, ["WEB2120_0_ONERA_data_available", "WEB2120_3_arxiv_mission_scenario"], "fresh 2120 web probe rows."),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(row(source_id=source_id, source_path=str(path), path_exists=exists, expected_needles="; ".join(needles), needles_found=exists and all(needle in text for needle in needles), role=role))
    return rows


def local_inventory_rows() -> list[dict[str, object]]:
    entries = [
        ("INV2120_0_expected_schema", CMSM_TEMPLATE, "expected official array schema", "TEMPLATE_ONLY"),
        ("INV2120_1_cmsm_readme", CMSM_README, "manual drop instructions", "INSTRUCTIONS_ONLY"),
        ("INV2120_2_drop_readme", DROP_README, "branch locked drop folder instructions", "INSTRUCTIONS_ONLY"),
        ("INV2120_3_drop_template", DROP_TEMPLATE, "readout CSV template", "TEMPLATE_ONLY"),
        ("INV2120_4_drop_live_readout", DROP_LIVE_READOUT, "live official readout CSV", "MISSING_UNLESS_USER_EXPORTS"),
        ("INV2120_5_suep_segments", CSV_1071_SEGMENTS, "SUEP segment metadata", "METADATA_ONLY_NOT_ARRAYS"),
        ("INV2120_6_surrogate_design", CSV_1075_SURROGATE, "surrogate design matrix", "SURROGATE_NOT_OFFICIAL"),
        ("INV2120_7_1900_targets", CSV_1900_TARGETS, "previous data target ledger", "PRIOR_PROBE_NONCLAIM"),
    ]
    rows: list[dict[str, object]] = []
    for inv_id, path, object_name, base_status in entries:
        exists = path.exists()
        size = path.stat().st_size if exists else 0
        status = "LIVE_OFFICIAL_READOUT_PRESENT_UNVERIFIED" if path == DROP_LIVE_READOUT and exists else base_status
        usable = path == DROP_LIVE_READOUT and exists
        rows.append(row(inventory_id=inv_id, object_name=object_name, local_path=str(path), path_exists=exists, size_bytes=size, current_status=status, usable_numeric_arrays=usable, valid_for_claim=False))
    return rows


def numeric_requirement_rows(live_readout_exists: bool) -> list[dict[str, object]]:
    return [
        row(req_id="REQ2120_0_time_session", needed_object="time/session/orbit index", current_status="METADATA_PARTIAL_SEGMENTS_ONLY", source_status="SUEP segment table exists; exact timestamps/arrays missing", blocks_tau=True),
        row(req_id="REQ2120_1_gx_gz", needed_object="gx,gz source gravity basis", current_status="MISSING_OFFICIAL_ARRAYS" if not live_readout_exists else "LIVE_FILE_PRESENT_UNVERIFIED", source_status="1071 skeleton and surrogate exist; official CMSM array not verified", blocks_tau=not live_readout_exists),
        row(req_id="REQ2120_2_Sxx_Sxz", needed_object="Sxx,Sxz gravity-gradient/inertia basis", current_status="MISSING_OFFICIAL_ARRAYS" if not live_readout_exists else "LIVE_FILE_PRESENT_UNVERIFIED", source_status="surrogate basis cannot replace official arrays", blocks_tau=not live_readout_exists),
        row(req_id="REQ2120_3_masks_calibration", needed_object="masks/calibration flags/systematics", current_status="MISSING", source_status="drop schema requires mask/calibration flags", blocks_tau=True),
        row(req_id="REQ2120_4_attitude_axis", needed_object="instrument attitude/sensitive-axis convention", current_status="MISSING", source_status="ORB1068_1 missing", blocks_tau=True),
        row(req_id="REQ2120_5_eta_convention", needed_object="eta_AB normalization/sign convention", current_status="BOUND_IMPORTED_FORMULA_NOT_PARENT_MAPPED", source_status="ORB1068_2 guard only", blocks_tau=True),
        row(req_id="REQ2120_6_source_worldtube", needed_object="source stress/composition/finite support", current_status="SOURCE_WORLDTUBE_NOT_ACQUIRED", source_status="SWT1068_5 verdict", blocks_tau=True),
        row(req_id="REQ2120_7_tau_kernel_verdict", needed_object="numeric tau_WEP kernel", current_status="BLOCKED_OFFICIAL_ARRAYS_AND_SOURCE_WORLDTUBE_MISSING", source_status="cannot run claim-grade tau_WEP", blocks_tau=True),
    ]


def acquisition_status_rows(web_rows: list[dict[str, object]], inventory_rows: list[dict[str, object]], requirement_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    official_pages_attempted = all(str(item["status"]) != "FETCH_NOT_ATTEMPTED" for item in web_rows)
    live_readout = any(item["inventory_id"] == "INV2120_4_drop_live_readout" and truthy(item["usable_numeric_arrays"]) for item in inventory_rows)
    tau_blocked = any(item["req_id"] == "REQ2120_7_tau_kernel_verdict" and str(item["current_status"]).startswith("BLOCKED") for item in requirement_rows)
    return [
        row(status_id="STAT2120_0_web_probe", status="OFFICIAL_SOURCES_PROBED" if official_pages_attempted else "WEB_PROBE_INCOMPLETE", detail="small official pages/portal endpoints probed and recorded", valid_numeric_kernel=False),
        row(status_id="STAT2120_1_live_arrays", status="LIVE_READOUT_PRESENT_UNVERIFIED" if live_readout else "OFFICIAL_ARRAYS_NOT_LOCAL", detail="drop-folder live CMSM readout file checked", valid_numeric_kernel=False),
        row(status_id="STAT2120_2_surrogate", status="SURROGATE_PRESENT_NONCLAIM", detail="1075 surrogate design matrix exists but cannot replace CMSM arrays", valid_numeric_kernel=False),
        row(status_id="STAT2120_3_tau", status="TAU_WEP_BLOCKED" if tau_blocked else "TAU_WEP_UNVERIFIED", detail="numeric tau kernel remains blocked unless official arrays and source-worldtube inputs are supplied", valid_numeric_kernel=False),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        row(gate_id="GATE2120_0_web_probe", gate="official data routes probed", gate_pass=True, rationale="ONERA/CMSM/arXiv routes are recorded as provenance and small fetch attempts"),
        row(gate_id="GATE2120_1_official_arrays", gate="official CMSM arrays local and verified", gate_pass=False, rationale="no verified live readout file with gx/gz/Sxx/Sxz/masks/calibration flags is present"),
        row(gate_id="GATE2120_2_surrogate_allowed", gate="surrogate design matrix can score WEP", gate_pass=False, rationale="surrogate is useful for plumbing only and cannot replace official arrays"),
        row(gate_id="GATE2120_3_tau_WEP_runnable", gate="numeric tau_WEP kernel runnable", gate_pass=False, rationale="official arrays, attitude/masks, eta convention and source worldtube remain missing"),
        row(gate_id="GATE2120_4_claim_allowed", gate="WEP/local-GR empirical claim allowed", gate_pass=False, rationale="data acquisition checkpoint only; no MTS prediction row can be scored"),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(decision_id="DEC2120_0", decision="NUMERIC_KERNEL_NOT_ACQUIRED", because="official portal/source pointers exist but no verified machine-readable CMSM arrays are local.", next_action="manual CMSM export or authenticated browser/data retrieval is needed."),
        row(decision_id="DEC2120_1", decision="SURROGATE_RETAINED_FOR_PLUMBING_ONLY", because="segment metadata and surrogate design matrix can test code shape but not physics.", next_action="keep surrogate rows nonclaim."),
        row(decision_id="DEC2120_2", decision="DERIVATION_CAN_CONTINUE_IN_PARALLEL", because="data blockage is practical, not a theory impasse.", next_action="continue source/readout theorem closure while arranging CMSM export."),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2120_0_2121",
            next_target="2121-Y5-R2FR-source-readout-theorem-closure-or-CMSM-manual-export-workflow.md",
            script="scripts/Y5_R2FR_source_readout_theorem_closure_or_CMSM_manual_export_workflow_2121.py",
            objective="Either continue the derivation route by closing source/readout as owned-coframe functionals, or prepare a manual CMSM export workflow with exact required filenames, columns, validation checks and no-claim import rules.",
            forbidden_shortcuts="treating portal pointers as arrays; using surrogate rows as empirical evidence; fitted-G absorption; cancellation; local-GR/Newton/PPN claim; formalization-workbench edits; GitHub action",
        )
    ]


def write_branch_copies(inventory_rows: list[dict[str, object]], requirement_rows: list[dict[str, object]], status_rows: list[dict[str, object]], next_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    copies = [
        ("COPY2120_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_MICROSCOPE_NUMERIC_2120_NONCLAIM.csv", inventory_rows + requirement_rows + status_rows),
        ("COPY2120_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2120_MICROSCOPE_NUMERIC_STATUS_NONCLAIM.csv", inventory_rows + requirement_rows + status_rows),
        ("COPY2120_2_acquisition_queue", QUEUE / "JR2120_CMSM_MANUAL_EXPORT_OR_THEOREM_QUEUE.csv", next_rows + requirement_rows),
    ]
    result: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        result.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return result


def validation_rows(
    sources: list[dict[str, object]],
    web_rows: list[dict[str, object]],
    inventory_rows: list[dict[str, object]],
    requirement_rows: list[dict[str, object]],
    status_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    web_ok = len(web_rows) >= 4 and all(str(item["status"]) != "FETCH_NOT_ATTEMPTED" for item in web_rows)
    inventory_ok = any(item["inventory_id"] == "INV2120_4_drop_live_readout" for item in inventory_rows)
    tau_blocked_ok = any(item["req_id"] == "REQ2120_7_tau_kernel_verdict" and str(item["current_status"]).startswith("BLOCKED") for item in requirement_rows)
    status_ok = any(item["status_id"] == "STAT2120_3_tau" and item["status"] == "TAU_WEP_BLOCKED" for item in status_rows)
    gates_ok = any(item["gate_id"] == "GATE2120_0_web_probe" and truthy(item["gate_pass"]) for item in gates) and any(item["gate_id"] == "GATE2120_3_tau_WEP_runnable" and not truthy(item["gate_pass"]) for item in gates)
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, web_rows, inventory_rows, requirement_rows, status_rows, gates, decisions, next_rows, copies)
        for item in group
    )
    branch_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2120_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    next_ok = any(item["route_id"] == "NEXT2120_0_2121" for item in next_rows)
    all_ok = all([sources_ok, web_ok, inventory_ok, tau_blocked_ok, status_ok, gates_ok, no_claim_flags, branch_ok, csv_ok, formalization_clean, pycache_clean, next_ok])
    checks = [
        ("VAL2120_00_sources", sources_ok, "all cited local data-acquisition sources exist and contain expected needles"),
        ("VAL2120_01_web_probe", web_ok, "official web routes were probed and recorded"),
        ("VAL2120_02_inventory", inventory_ok, "local drop/template/metadata inventory includes live-readout check"),
        ("VAL2120_03_tau_blocked", tau_blocked_ok, "numeric tau_WEP remains blocked"),
        ("VAL2120_04_status", status_ok, "status ledger records TAU_WEP_BLOCKED"),
        ("VAL2120_05_claim_gates", gates_ok, "web probe passes but tau runnable gate fails"),
        ("VAL2120_06_no_claim_flags", no_claim_flags, "no generated row allows a claim or score"),
        ("VAL2120_07_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2120_08_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2120_09_formalization_clean", formalization_clean, "formalization-workbench untouched by 2120"),
        ("VAL2120_10_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2120_11_next", next_ok, "next target selects source/readout theorem closure or CMSM manual export workflow"),
        ("VAL2120_OVERALL", all_ok, "2120 probes official routes, inventories local MICROSCOPE inputs, blocks numeric tau_WEP honestly, and stages the manual export/theorem next fork."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    web_rows: list[dict[str, object]],
    inventory_rows: list[dict[str, object]],
    requirement_rows: list[dict[str, object]],
    status_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n\n".join(
        [
            "# 2120 - Y5/R2FR MICROSCOPE Numeric Source-Readout Kernel Acquisition",
            "## Current Verdict",
            "2120 probes the official MICROSCOPE/CMSM routes and inventories the local drop folders. The result is useful but not runnable: we have official provenance, templates, segment metadata, and a surrogate design matrix, but no verified CMSM numeric arrays for `gx`, `gz`, `Sxx`, `Sxz`, masks, calibration flags, attitude convention, or source-worldtube normalization.",
            "Therefore `tau_WEP` remains blocked. This is a practical data-access block, not a theory block. The derivation route can continue, and the data route now has exact manual-export requirements.",
            "No MICROSCOPE/WEP/local-GR claim is allowed from this checkpoint.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Web Probe",
            md_table(web_rows, ["probe_id", "url", "status", "status_code", "bytes_written", "contains_data_pointer", "usable_numeric_arrays", "error", "valid_for_claim"]),
            "## Local Inventory",
            md_table(inventory_rows, ["inventory_id", "object_name", "local_path", "path_exists", "size_bytes", "current_status", "usable_numeric_arrays", "valid_for_claim"]),
            "## Numeric Requirements",
            md_table(requirement_rows, ["req_id", "needed_object", "current_status", "source_status", "blocks_tau", "valid_for_claim"]),
            "## Acquisition Status",
            md_table(status_rows, ["status_id", "status", "detail", "valid_numeric_kernel", "valid_for_claim"]),
            "## Claim Gates",
            md_table(gates, ["gate_id", "gate", "gate_pass", "rationale", "valid_for_claim", "claim_allowed"]),
            "## Decision Ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Next Target",
            md_table(next_rows, ["route_id", "next_target", "script", "objective", "forbidden_shortcuts", "valid_for_claim"]),
            "## Branch Copies",
            md_table(copies, ["copy_id", "destination", "path_exists", "row_count", "parse_ok", "valid_for_claim"]),
            "## Validation",
            md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
        ]
    )
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    WEB_DIR.mkdir(parents=True, exist_ok=True)

    paths = {
        "web": OUT / "P8_Y5_PARENT_QLOC_2120_WEB_PROBE.csv",
        "sources": OUT / "P8_Y5_PARENT_QLOC_2120_SOURCE_REGISTER.csv",
        "inventory": OUT / "P8_Y5_PARENT_QLOC_2120_LOCAL_DATA_INVENTORY.csv",
        "requirements": OUT / "P8_Y5_PARENT_QLOC_2120_NUMERIC_KERNEL_REQUIREMENTS.csv",
        "status": OUT / "P8_Y5_PARENT_QLOC_2120_ACQUISITION_STATUS.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2120_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2120_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2120_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2120_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2120_VALIDATION.csv",
    }

    web_rows = web_probe_rows()
    write_csv(paths["web"], web_rows)
    sources = source_register_rows(paths["web"])
    inventory_rows = local_inventory_rows()
    live_readout_exists = any(item["inventory_id"] == "INV2120_4_drop_live_readout" and truthy(item["usable_numeric_arrays"]) for item in inventory_rows)
    requirement_rows = numeric_requirement_rows(live_readout_exists)
    status_rows = acquisition_status_rows(web_rows, inventory_rows, requirement_rows)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(paths["sources"], sources)
    write_csv(paths["inventory"], inventory_rows)
    write_csv(paths["requirements"], requirement_rows)
    write_csv(paths["status"], status_rows)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows)

    copies = write_branch_copies(inventory_rows, requirement_rows, status_rows, next_rows)
    write_csv(paths["branch"], copies)

    remove_pycache()
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, web_rows, inventory_rows, requirement_rows, status_rows, gates, decisions, next_rows, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, web_rows, inventory_rows, requirement_rows, status_rows, gates, decisions, next_rows, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
