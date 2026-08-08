from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")
CMSM_DIR = Path("source-intake/microscope_cmsm")

DOC_PATH = Path("1422-Y5-R10-RAB-MICROSCOPE-source-leg-data-schema-or-gxgzS-kernel-pilot.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1422_SOURCE_REGISTER.csv"
PORTAL_PROBE_PATH = SRC_DIR / "P8_Y5_R10_1422_CURRENT_PORTAL_PROBE.csv"
SCHEMA_STATUS_PATH = SRC_DIR / "P8_Y5_R10_1422_CMSM_SCHEMA_STATUS.csv"
PILOT_STATUS_PATH = SRC_DIR / "P8_Y5_R10_1422_GXGZS_KERNEL_PILOT_STATUS.csv"
BLOCKER_LEDGER_PATH = SRC_DIR / "P8_Y5_R10_1422_EXACT_BLOCKER_LEDGER.csv"
EXPORT_CONTRACT_PATH = SRC_DIR / "P8_Y5_R10_1422_LOCAL_EXPORT_CONTRACT.csv"
DECISION_PATH = SRC_DIR / "P8_Y5_R10_1422_DECISION_LEDGER.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1422_CLAIM_GATE.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1422_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1422_VALIDATION.csv"

GENERATED_UTC = datetime.now(timezone.utc).isoformat()
STATUS = "Y5_R10_1422_CMSM_schema_not_acquired_gxgzS_pilot_blocker_ledger_written_nonclaim"
CLAIM_CEILING = (
    "MICROSCOPE_source_leg_schema_probe_and_gxgzS_pilot_blocker_only_"
    "no_numeric_tau_no_WEP_pass_no_guessed_masks_no_point_source_by_taste"
)


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").replace("\r", " ").strip()


def md_cell(value: Any) -> str:
    return clean(value).replace("|", "\\|")


def write_csv(relative_path: Path, rows: list[dict[str, Any]]) -> None:
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows supplied for {relative_path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: clean(row.get(key, "")) for key in fieldnames})


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def anchor_found(relative_path: str, anchor: str) -> bool:
    path = ROOT / relative_path
    if not path.exists():
        return False
    return anchor in path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC1422_0_1421_doc",
            "source_path": "1421-Y5-R10-RAB-WEP-source-worldtube-or-parent-point-source-theorem.md",
            "anchor": "NEXT1421_0_1422",
            "role": "prior checkpoint selecting CMSM data schema or gx/gz/Sxx/Sxz pilot",
        },
        {
            "source_id": "SRC1422_1_1421_metadata",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1421_WEP_SOURCE_WORLDTUBE_METADATA_ROWS.csv",
            "anchor": "WSW1421_8_verdict",
            "role": "source-worldtube metadata staged but numeric source leg missing",
        },
        {
            "source_id": "SRC1422_2_1071_kernel",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1071_OFFICIAL_KERNEL_COMPONENTS.csv",
            "anchor": "KER1071_6_verdict",
            "role": "official kernel skeleton acquired but numeric tau/source arrays missing",
        },
        {
            "source_id": "SRC1422_3_1071_tau",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1071_TAU_PROJECTION_STATUS.csv",
            "anchor": "TAU1071_3_verdict",
            "role": "numeric tau/source projection not acquired",
        },
        {
            "source_id": "SRC1422_4_1071_segments",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1071_SUEP_SEGMENT_TABLE_SOURCE_BACKED.csv",
            "anchor": "SUEP1071_210",
            "role": "SUEP segment 210 metadata for pilot",
        },
        {
            "source_id": "SRC1422_5_1072_probe",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1072_PORTAL_ROUTE_PROBE.csv",
            "anchor": "https://cmsm-ds.onera.fr/user/microscope",
            "role": "prior CMSM portal probe failure",
        },
        {
            "source_id": "SRC1422_6_1072_requirements",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1072_RECONSTRUCTION_REQUIREMENTS.csv",
            "anchor": "REQ1072_0_exact_time_grid",
            "role": "reconstruction requirement list",
        },
        {
            "source_id": "SRC1422_7_1072_dryrun",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1072_GXS_DRY_RUN_METADATA_SEGMENT210.csv",
            "anchor": "DRY1072_0_segment210_kernel_preview",
            "role": "nonclaim dry-run shape preview",
        },
        {
            "source_id": "SRC1422_8_1073_contract",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1073_CMSM_EXPORT_CONTRACT.csv",
            "anchor": "CMSM1073_5_official_gxS_arrays",
            "role": "CMSM export contract for official gx/gz/Sxx/Sxz arrays",
        },
        {
            "source_id": "SRC1422_9_1073_status",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1073_OFFICIAL_ARRAY_EXTRACT_STATUS.csv",
            "anchor": "EX1073_2_official_segment210_arrays",
            "role": "official arrays not acquired",
        },
        {
            "source_id": "SRC1422_10_1074_inventory",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1074_CMSM_EXPORT_INVENTORY_CHECK.csv",
            "anchor": "INV1074_0_search_root",
            "role": "local CMSM export not found in prior check",
        },
        {
            "source_id": "SRC1422_11_1074_surrogate",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1074_SURROGATE_GRID_METADATA_SEGMENT210.csv",
            "anchor": "GRID1074_0_segment210_surrogate",
            "role": "nonclaim surrogate grid exists",
        },
    ]
    for row in rows:
        row["path_exists"] = (ROOT / row["source_path"]).exists()
        row["anchor_found"] = anchor_found(row["source_path"], row["anchor"])
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def probe_url(url: str) -> dict[str, Any]:
    request = Request(url, headers={"User-Agent": "MTS-1422-schema-probe/1.0"})
    try:
        with urlopen(request, timeout=8) as response:
            body = response.read(1024)
            content_type = response.headers.get("Content-Type", "")
            return {
                "url": url,
                "probe_status": "HTTP_OK",
                "http_status": getattr(response, "status", ""),
                "content_type": content_type,
                "bytes_sampled": len(body),
                "schema_or_arrays_acquired": False,
                "error": "",
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": GENERATED_UTC,
            }
    except Exception as exc:  # network failures are evidence for acquisition state here
        return {
            "url": url,
            "probe_status": "BLOCKED_OR_UNREACHABLE_FROM_THIS_RUN",
            "http_status": "",
            "content_type": "",
            "bytes_sampled": 0,
            "schema_or_arrays_acquired": False,
            "error": f"{type(exc).__name__}: {exc}",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }


def portal_probe_rows() -> list[dict[str, Any]]:
    urls = [
        "https://microscope.onera.fr/fr/publication/microscope-data-are-available",
        "https://cmsm-ds.onera.fr/user/microscope",
        "https://cmsm-ds.onera.fr/api/v1/rs-access-project/datasets/search",
        "https://cmsm-ds.onera.fr/api/v1/rs-access-project/dataobjects/search",
        "https://cmsm-ds.onera.fr/api/v1/rs-access-project/applications/microscope/modules",
    ]
    return [probe_url(url) for url in urls]


def local_export_inventory() -> tuple[bool, int]:
    export_root = ROOT / CMSM_DIR
    if not export_root.exists():
        return False, 0
    files = [path for path in export_root.rglob("*") if path.is_file()]
    return True, len(files)


def schema_status_rows(probes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    export_exists, matching_files = local_export_inventory()
    cmsm_access = any(
        "cmsm-ds.onera.fr" in row["url"] and row["probe_status"] == "HTTP_OK" and row["schema_or_arrays_acquired"]
        for row in probes
    )
    return [
        {
            "schema_id": "CSS1422_0_public_pointer",
            "object": "ONERA public MICROSCOPE data page",
            "status": "REACHABLE" if any("microscope.onera.fr" in row["url"] and row["probe_status"] == "HTTP_OK" for row in probes) else "NOT_REACHED",
            "evidence": "P8_Y5_R10_1422_CURRENT_PORTAL_PROBE.csv",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "schema_id": "CSS1422_1_cmsm_portal",
            "object": "CMSM browser/API schema",
            "status": "NOT_ACQUIRED" if not cmsm_access else "PARTIAL_HTTP_RESPONSE_ONLY",
            "evidence": "P8_Y5_R10_1422_CURRENT_PORTAL_PROBE.csv",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "schema_id": "CSS1422_2_local_export_inventory",
            "object": "local CMSM export folder",
            "status": "NO_LOCAL_EXPORT_FOUND" if not export_exists or matching_files == 0 else "LOCAL_FILES_PRESENT_NEEDS_SCHEMA_CHECK",
            "evidence": str(ROOT / CMSM_DIR),
            "matching_files": matching_files,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "schema_id": "CSS1422_3_official_arrays",
            "object": "official gx/gz/Sxx/Sxz arrays",
            "status": "NOT_ACQUIRED",
            "evidence": "P8_Y5_R10_1073_OFFICIAL_ARRAY_EXTRACT_STATUS.csv::EX1073_2_official_segment210_arrays",
            "matching_files": 0,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "schema_id": "CSS1422_4_verdict",
            "object": "CMSM schema/file inventory",
            "status": "SCHEMA_NOT_ACQUIRED_BLOCKER_LEDGER_REQUIRED",
            "evidence": "CSS1422_0 through CSS1422_3",
            "matching_files": matching_files,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def pilot_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "pilot_id": "GXP1422_0_official_kernel_skeleton",
            "object": "official kernel basis",
            "status": "FORM_ACQUIRED_NOT_NUMERIC",
            "evidence": "KER1071_1_fit_basis;KER1071_2_source_gravity_leg;KER1071_6_verdict",
            "usable_for_claim": False,
            "next_requirement": "numeric gx,gz,Sxx,Sxz arrays or exact reconstruction inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pilot_id": "GXP1422_1_dry_run_preview",
            "object": "1072 unit-shape preview",
            "status": "DRY_RUN_SHAPE_ONLY",
            "evidence": "DRY1072_0_segment210_kernel_preview",
            "usable_for_claim": False,
            "next_requirement": "replace zero-phase/unit-amplitude columns with official or source-reconstructed arrays",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pilot_id": "GXP1422_2_surrogate_preview",
            "object": "1074 circular monopole surrogate",
            "status": "NONCLAIM_PIPELINE_TEST_ONLY",
            "evidence": "GRID1074_0_segment210_surrogate",
            "usable_for_claim": False,
            "next_requirement": "only use as smoke runner after explicit nonclaim flag; never as MICROSCOPE tau",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pilot_id": "GXP1422_3_segment210_window",
            "object": "SUEP segment 210 metadata",
            "status": "SEGMENT_METADATA_AVAILABLE_MASKS_MISSING",
            "evidence": "SUEP1071_210",
            "usable_for_claim": False,
            "next_requirement": "exact timestamps and glitch masks",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pilot_id": "GXP1422_4_pilot_arrays",
            "object": "pilot gx/gz/Sxx/Sxz source-leg arrays",
            "status": "NOT_ACQUIRED_OR_RECONSTRUCTED",
            "evidence": "CSS1422_4_verdict; EBL1422 blockers",
            "usable_for_claim": False,
            "next_requirement": "CMSM export, data schema, or reconstruction inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pilot_id": "GXP1422_5_numeric_tau",
            "object": "numeric tau_WEP / M_WEP,q",
            "status": "NOT_ACQUIRED",
            "evidence": "GXP1422_4_pilot_arrays plus missing residual/material map",
            "usable_for_claim": False,
            "next_requirement": "arrays plus MTS material/source residual map",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def blocker_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker_id": "EBL1422_0_schema_inventory",
            "blocked_object": "CMSM dataset/file inventory",
            "why_needed": "identify official MICROSCOPE products and download/export paths",
            "current_status": "NOT_ACQUIRED",
            "accepted_resolution": "source-backed API/browser export or local file inventory with dataset/product names",
            "do_not_use": "guessed endpoint names as schema",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "EBL1422_1_exact_time_grid",
            "blocked_object": "segment 210 timestamps and masks",
            "why_needed": "phase, DFT alignment, glitch removal, and regression basis depend on exact samples",
            "current_status": "MISSING_EXACT_TIMESTAMPS_AND_MASKS",
            "accepted_resolution": "CMSM time/mask export or exact segment product with mask flags",
            "do_not_use": "duration-only uniform grid as claim-grade timestamps",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "EBL1422_2_orbit_ephemeris",
            "blocked_object": "satellite position/velocity",
            "why_needed": "compute g(O_sat) and gravity-gradient tensor T",
            "current_status": "MISSING_NUMERIC_EPHEMERIS",
            "accepted_resolution": "CMSM minute-sampled orbit product or source-backed equivalent",
            "do_not_use": "circular orbit surrogate as official kernel",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "EBL1422_3_attitude_rates",
            "blocked_object": "attitude/angular velocity/angular acceleration",
            "why_needed": "rotate g/T into instrument frame and build inertia-gradient S",
            "current_status": "MISSING_NUMERIC_ATTITUDE_RATES",
            "accepted_resolution": "same-stamp attitude/rate products or documented interpolation rule",
            "do_not_use": "zero-phase/zero-attitude surrogate as claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "EBL1422_4_gravity_model",
            "blocked_object": "Earth gravity model/source profile",
            "why_needed": "official g/T reconstruction and finite-source/source-worldtube convention",
            "current_status": "MISSING_OFFICIAL_GRAVITY_MODEL_OR_APPROVED_SURROGATE",
            "accepted_resolution": "MICROSCOPE processing gravity model, auxiliary data, or explicitly nonclaim surrogate route",
            "do_not_use": "unlabelled monopole model as official tau",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "EBL1422_5_material_source_map",
            "blocked_object": "MTS material/source residual map",
            "why_needed": "turn gx/gz/Sxx/Sxz fit basis into an MTS source-weight prediction",
            "current_status": "MISSING_PARENT_MATERIAL_MAP",
            "accepted_resolution": "theorem-zero residuals or source-backed qbar/material coefficients in same basis",
            "do_not_use": "alpha/Coulomb smoke row as full source-weight tensor",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "EBL1422_6_verdict",
            "blocked_object": "pilot numeric source-leg kernel",
            "why_needed": "first executable M_WEP,q row",
            "current_status": "BLOCKED_SCHEMA_AND_INPUTS_MISSING",
            "accepted_resolution": "resolve EBL1422_0 through EBL1422_5 or keep only nonclaim smoke runner",
            "do_not_use": "numeric tau_WEP without arrays and MTS source map",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def export_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "EXP1422_0_folder",
            "target_folder": str(ROOT / CMSM_DIR),
            "required_files": "dataset_inventory.csv or equivalent manifest",
            "minimum_fields": "dataset_name;product_type;file_name;download_url_or_order_id;time_coverage;session_or_segment",
            "current_status": "NOT_FOUND_LOCALLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "EXP1422_1_segment210_time_mask",
            "target_folder": str(ROOT / CMSM_DIR / "segment210"),
            "required_files": "time_mask.csv",
            "minimum_fields": "segment_id;t_utc;sample_index;mask_flag;mask_reason",
            "current_status": "NOT_FOUND_LOCALLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "EXP1422_2_segment210_orbit_attitude",
            "target_folder": str(ROOT / CMSM_DIR / "segment210"),
            "required_files": "orbit.csv;attitude_rates.csv",
            "minimum_fields": "t_utc;r_x;r_y;r_z;v_x;v_y;v_z;frame;units and q/Omega/Omegadot fields",
            "current_status": "NOT_FOUND_LOCALLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "EXP1422_3_segment210_gxS",
            "target_folder": str(ROOT / CMSM_DIR / "segment210"),
            "required_files": "gxgzSxxSxz.csv",
            "minimum_fields": "segment_id;t_utc;gx;gz;Sxx;Sxz;frame;generation_method;source_file",
            "current_status": "NOT_FOUND_LOCALLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "EXP1422_4_verdict",
            "target_folder": str(ROOT / CMSM_DIR),
            "required_files": "all EXP1422 rows",
            "minimum_fields": "source path, units, frame, provenance, and mask convention",
            "current_status": "EXPORT_CONTRACT_READY_INPUTS_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1422_0_schema_verdict",
            "decision": "CMSM schema/file inventory not acquired from current run",
            "reason": "public ONERA page reachable; CMSM browser/API endpoints unreachable or do not yield schema",
            "next_action": "use browser/manual export or provide exact CMSM files/API response",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1422_1_pilot_verdict",
            "decision": "gx/gz/Sxx/Sxz pilot remains blocked",
            "reason": "dry-run and surrogate previews exist but exact timestamps, ephemeris, attitude/rates, gravity model, masks, and material map are missing",
            "next_action": "fill export contract or choose explicitly nonclaim smoke-runner path",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1422_2_best_next",
            "decision": "target user/browser CMSM export import or nonclaim smoke runner next",
            "reason": "automated portal access is not providing schema; a local export would unblock official pilot arrays fastest",
            "next_action": "if export is available, ingest it; otherwise run a labelled surrogate-only smoke runner that cannot be cited as evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG1422_0_schema_claim",
            "claim": "CMSM schema/file inventory acquired",
            "allowed": False,
            "reason": "CSS1422_4 remains schema not acquired",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1422_1_kernel_claim",
            "claim": "official gx/gz/Sxx/Sxz arrays acquired or reconstructed",
            "allowed": False,
            "reason": "GXP1422_4 remains not acquired/reconstructed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1422_2_tau_claim",
            "claim": "numeric tau_WEP or M_WEP,q source leg is available",
            "allowed": False,
            "reason": CLAIM_CEILING,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1422_3_WEP_claim",
            "claim": "WEP source projection can be scored or passed",
            "allowed": False,
            "reason": "schema, arrays, residual/material map, and WEP projection row are incomplete",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1422_0_1423",
            "target_doc": "1423-Y5-R10-RAB-CMSM-export-import-or-surrogate-smoke-runner.md",
            "target_script": "scripts/Y5_R10_RAB_CMSM_export_import_or_surrogate_smoke_runner.py",
            "task": "look for a user-supplied CMSM export under source-intake/microscope_cmsm; if absent, run only a labelled surrogate smoke runner and keep all WEP/tau/local-GR claims blocked",
            "success_condition": "official export is parsed into schema rows, or surrogate smoke output is generated with explicit nonclaim status and replacement map",
            "do_not_claim": "official tau from surrogate; WEP pass; guessed masks/phases; measured-G absorption",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "next_id": "NEXT1422_1_parallel_theory",
            "target_doc": "future-MWEP-source-leg-theorem-zero-route.md",
            "target_script": "future_theory_route",
            "task": "continue theory route for source-leg theorem-zero while data export remains blocked",
            "success_condition": "M_WEP,q is theorem-zero/common-mode or retained as finite residual",
            "do_not_claim": "data blocker as theory proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    probes: list[dict[str, Any]],
    schema_rows: list[dict[str, Any]],
    pilot_rows: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    export_contract: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_paths = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        PORTAL_PROBE_PATH,
        SCHEMA_STATUS_PATH,
        PILOT_STATUS_PATH,
        BLOCKER_LEDGER_PATH,
        EXPORT_CONTRACT_PATH,
        DECISION_PATH,
        CLAIM_GATE_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
    ]
    rows: list[dict[str, Any]] = []

    def add(check_id: str, condition: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "status": "PASS" if condition else "FAIL",
                "detail": detail,
                "generated_utc": GENERATED_UTC,
            }
        )

    add(
        "VAL1422_0_sources",
        all(row["path_exists"] and row["anchor_found"] for row in sources),
        "all cited local source paths exist and anchors are present",
    )
    add(
        "VAL1422_1_current_probe",
        len(probes) >= 3 and any("microscope.onera.fr" in row["url"] for row in probes),
        "current portal probe rows were written",
    )
    add(
        "VAL1422_2_schema_status",
        any(row["schema_id"] == "CSS1422_4_verdict" and row["status"] == "SCHEMA_NOT_ACQUIRED_BLOCKER_LEDGER_REQUIRED" for row in schema_rows),
        "schema status remains blocked and explicit",
    )
    add(
        "VAL1422_3_pilot_status",
        any(row["pilot_id"] == "GXP1422_4_pilot_arrays" and row["status"] == "NOT_ACQUIRED_OR_RECONSTRUCTED" for row in pilot_rows),
        "pilot gx/gz/Sxx/Sxz arrays are not claimed",
    )
    required_blockers = {
        "EBL1422_0_schema_inventory",
        "EBL1422_1_exact_time_grid",
        "EBL1422_2_orbit_ephemeris",
        "EBL1422_3_attitude_rates",
        "EBL1422_4_gravity_model",
        "EBL1422_5_material_source_map",
    }
    add(
        "VAL1422_4_blockers",
        required_blockers.issubset({row["blocker_id"] for row in blockers}) and all(row["claim_allowed"] is False for row in blockers),
        "exact blocker ledger covers schema, time grid, ephemeris, attitude, gravity model, and material map",
    )
    add(
        "VAL1422_5_export_contract",
        any(row["contract_id"] == "EXP1422_4_verdict" for row in export_contract),
        "local CMSM export contract is written",
    )
    add(
        "VAL1422_6_claim_refusal",
        all(row["allowed"] is False and row["claim_allowed"] is False for row in claim_gates),
        "schema, kernel, tau, and WEP claims are refused",
    )
    add(
        "VAL1422_7_decision",
        any(row["decision_id"] == "DEC1422_2_best_next" and "CMSM export import" in row["decision"] for row in decisions),
        "decision ledger selects export import or surrogate smoke runner next",
    )
    add(
        "VAL1422_8_next_target",
        any(row["next_id"] == "NEXT1422_0_1423" for row in next_targets),
        "next target 1423 is staged",
    )
    add(
        "VAL1422_9_scope",
        all((ROOT / path).resolve().is_relative_to(ROOT.resolve()) for path in output_paths),
        "outputs are confined to post-checkpoint-work paths",
    )
    add(
        "VAL1422_10_overall",
        True,
        "1422 fails CMSM schema/pilot acquisition and writes exact blocker ledger as nonclaim",
    )
    if any(row["status"] == "FAIL" for row in rows):
        for row in rows:
            if row["check_id"] == "VAL1422_10_overall":
                row["status"] = "FAIL"
                row["detail"] = "one or more 1422 validation checks failed"
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    probes: list[dict[str, Any]],
    schema_rows: list[dict[str, Any]],
    pilot_rows: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    export_contract: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    doc = f"""# 1422 - MICROSCOPE Source-Leg Data Schema Or gx/gz/Sxx/Sxz Kernel Pilot

**Current verdict:** the CMSM/MICROSCOPE schema and official `gx/gz/Sxx/Sxz` pilot arrays are not acquired. The ONERA public information page is reachable, but the CMSM browser/API routes did not provide a usable schema or arrays in this run. Existing 1072/1074 dry-run and surrogate previews remain nonclaim pipeline tests only.

**Discipline move:** this checkpoint writes the exact blocker ledger and local export contract. The next data step is either ingest a user/browser CMSM export under `source-intake/microscope_cmsm`, or run a clearly labelled surrogate smoke runner that cannot be cited as WEP/tau evidence.

**Status:** `{STATUS}`

## Source Register

{md_table(sources)}

## Current Portal Probe

{md_table(probes)}

## CMSM Schema Status

{md_table(schema_rows)}

## gx/gz/Sxx/Sxz Kernel Pilot Status

{md_table(pilot_rows)}

## Exact Blocker Ledger

{md_table(blockers)}

## Local Export Contract

{md_table(export_contract)}

## Decision Ledger

{md_table(decisions)}

## Claim Gate

{md_table(claim_gates)}

## Next Target

{md_table(next_targets)}

## Validation

{md_table(validations)}
"""
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    probes = portal_probe_rows()
    schema_rows = schema_status_rows(probes)
    pilot_rows = pilot_status_rows()
    blockers = blocker_ledger_rows()
    export_contract = export_contract_rows()
    decisions = decision_rows()
    claim_gates = claim_gate_rows()
    next_targets = next_target_rows()
    validations = validation_rows(sources, probes, schema_rows, pilot_rows, blockers, export_contract, decisions, claim_gates, next_targets)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(PORTAL_PROBE_PATH, probes)
    write_csv(SCHEMA_STATUS_PATH, schema_rows)
    write_csv(PILOT_STATUS_PATH, pilot_rows)
    write_csv(BLOCKER_LEDGER_PATH, blockers)
    write_csv(EXPORT_CONTRACT_PATH, export_contract)
    write_csv(DECISION_PATH, decisions)
    write_csv(CLAIM_GATE_PATH, claim_gates)
    write_csv(NEXT_TARGET_PATH, next_targets)
    write_csv(VALIDATION_PATH, validations)
    write_doc(sources, probes, schema_rows, pilot_rows, blockers, export_contract, decisions, claim_gates, next_targets, validations)

    if any(row["status"] != "PASS" for row in validations):
        raise SystemExit("1422 validation failed")

    print(STATUS)


if __name__ == "__main__":
    main()
