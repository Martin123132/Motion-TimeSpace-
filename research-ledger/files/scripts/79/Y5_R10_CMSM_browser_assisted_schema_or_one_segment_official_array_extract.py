from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from Y5_R10_alpha_product_prediction_stub_runner_and_required_inputs import (
    BOUND_REQUIRED_COLUMNS,
    PRODUCT_REQUIRED_COLUMNS,
    run_product_runner,
)


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"
DOC = ROOT / "1073-Y5-R10-CMSM-browser-assisted-schema-or-one-segment-official-array-extract.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1073-CMSM-browser-assisted-schema-or-array-extract" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1073_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1073_WEP_BOUND_IMPORT.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED
    )


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def local_bound_row(row_id: str) -> dict[str, str]:
    for row in read_csv(LOCAL_BOUNDS):
        if row.get("row_id") == row_id:
            return row
    raise ValueError(f"missing local bound row {row_id}")


def split_reference(reference: str) -> tuple[str, str]:
    parts = [part.strip() for part in reference.split(";")]
    url = next((part for part in parts if part.startswith("http")), "")
    doi = next((part.replace("doi:", "").strip() for part in parts if part.lower().startswith("doi:")), "")
    return url, doi


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1073_0_1072_next", "source-intake/mts_residuals/P8_Y5_R10_1072_NEXT_TARGET.csv", "1073-Y5-R10-CMSM-browser-assisted-schema-or-one-segment-official-array-extract.md", "1072 handoff."),
        ("SRC1073_1_1072_validation", "source-intake/mts_residuals/P8_Y5_BRR545_1072_VALIDATION.csv", "V1072_SUMMARY", "1072 validation summary."),
        ("SRC1073_2_1072_portal", "source-intake/mts_residuals/P8_Y5_R10_1072_PORTAL_ROUTE_PROBE.csv", "cmsm-ds.onera.fr/user/microscope/modules/7", "prior portal route probes."),
        ("SRC1073_3_1072_endpoints", "source-intake/mts_residuals/P8_Y5_R10_1072_CMSM_REGARDS_API_CANDIDATE_ENDPOINTS.csv", "API1072_3_joined_dataobject_dataset_search", "candidate REGARDS endpoints."),
        ("SRC1073_4_1072_requirements", "source-intake/mts_residuals/P8_Y5_R10_1072_RECONSTRUCTION_REQUIREMENTS.csv", "REQ1072_0_exact_time_grid", "missing reconstruction inputs."),
        ("SRC1073_5_1072_dry_meta", "source-intake/mts_residuals/P8_Y5_R10_1072_GXS_DRY_RUN_METADATA_SEGMENT210.csv", "DRY1072_0_segment210_kernel_preview", "dry-run preview metadata."),
        ("SRC1073_6_1072_preview", "source-intake/mts_residuals/P8_Y5_R10_1072_GXS_DRY_RUN_KERNEL_PREVIEW_SEGMENT210.csv", "GXS1072_210_00", "dry-run preview columns."),
        ("SRC1073_7_1072_tau", "source-intake/mts_residuals/P8_Y5_R10_1072_NUMERIC_TAU_STATUS.csv", "NTS1072_2_tau_WEP", "numeric tau still missing."),
        ("SRC1073_8_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge", "MICROSCOPE WEP bound row."),
    ]
    rows: list[dict[str, str]] = []
    for source_id, relative_path, needle, note in specs:
        path = source_path(relative_path)
        exists = path.exists()
        needle_found = exists and needle in read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "relative_path": relative_path,
                "absolute_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle_found).lower(),
                "note": note,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def browser_attempt_rows() -> list[dict[str, str]]:
    return [
        {
            "browser_id": "BROW1073_0_direct_cmsm_module",
            "surface": "Codex in-app browser",
            "target_url": "https://cmsm-ds.onera.fr/user/microscope/modules/7",
            "observed_title": "This site can't be reached",
            "observed_status": "ERR_CONNECTION_REFUSED",
            "schema_inventory_acquired": "false",
            "official_array_acquired": "false",
            "note": "browser-facing route refused connection from this runtime; no CMSM UI schema or file inventory visible",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "browser_id": "BROW1073_1_dom_or_log_inspection",
            "surface": "Codex in-app browser",
            "target_url": "https://cmsm-ds.onera.fr/user/microscope/modules/7",
            "observed_title": "not_available_after_blocked_error_state",
            "observed_status": "DOM_AND_LOG_INSPECTION_NOT_AVAILABLE",
            "schema_inventory_acquired": "false",
            "official_array_acquired": "false",
            "note": "after the refused connection, further DOM/log inspection was unavailable; no workaround was attempted",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def api_response_attempt_rows() -> list[dict[str, str]]:
    prior_rows = read_csv(OUT / "P8_Y5_R10_1072_PORTAL_ROUTE_PROBE.csv")
    rows: list[dict[str, str]] = []
    for index, row in enumerate(prior_rows):
        rows.append(
            {
                "attempt_id": f"API1073_prior_{index}",
                "target_url": row.get("url", ""),
                "probe_status": row.get("probe_status", ""),
                "http_status": row.get("http_status", ""),
                "content_type": row.get("content_type", ""),
                "schema_inventory_acquired": row.get("schema_or_data_inventory_acquired", "false"),
                "official_array_acquired": "false",
                "error_summary": row.get("error", ""),
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def cmsm_export_contract_rows() -> list[dict[str, str]]:
    return [
        {
            "contract_id": "CMSM1073_0_dataset_inventory",
            "required_artifact": "dataset/file inventory",
            "minimum_fields": "dataset_name;product_type;file_name;download_url_or_order_id;time_coverage;sensor_unit;session_or_segment",
            "acceptance_rule": "source-backed CMSM/REGARDS export or screenshot/API response naming MICROSCOPE data products",
            "current_status": "NOT_ACQUIRED",
            "target_folder": "post-checkpoint-work/source-intake/microscope_cmsm/",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "CMSM1073_1_time_mask",
            "required_artifact": "segment 210 exact timestamps and mask",
            "minimum_fields": "segment_id;t_utc;sample_index;mask_flag;mask_reason",
            "acceptance_rule": "must be exact exported time grid, not reconstructed from duration only",
            "current_status": "NOT_ACQUIRED",
            "target_folder": "post-checkpoint-work/source-intake/microscope_cmsm/segment210/",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "CMSM1073_2_acceleration_channel",
            "required_artifact": "corrected X-axis differential acceleration or raw+calibration products",
            "minimum_fields": "segment_id;t_utc;Gamma_x_corr_d OR Gamma1_x/Gamma2_x plus calibration flags",
            "acceptance_rule": "must state whether channel is raw, calibrated, corrected, reconstructed, or masked",
            "current_status": "NOT_ACQUIRED",
            "target_folder": "post-checkpoint-work/source-intake/microscope_cmsm/segment210/",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "CMSM1073_3_attitude_rate",
            "required_artifact": "attitude/angular velocity/angular acceleration products",
            "minimum_fields": "t_utc;q0;q1;q2;q3;Omega_x;Omega_y;Omega_z;Omegadot_x;Omegadot_y;Omegadot_z;frame",
            "acceptance_rule": "same timestamp grid as accelerometer or documented interpolation rule",
            "current_status": "NOT_ACQUIRED",
            "target_folder": "post-checkpoint-work/source-intake/microscope_cmsm/segment210/",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "CMSM1073_4_orbit_ephemeris",
            "required_artifact": "satellite J2000 position/velocity",
            "minimum_fields": "t_utc;r_x;r_y;r_z;v_x;v_y;v_z;frame;units",
            "acceptance_rule": "CMSM minute-sampled orbit product or source-backed official ephemeris",
            "current_status": "NOT_ACQUIRED",
            "target_folder": "post-checkpoint-work/source-intake/microscope_cmsm/segment210/",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "CMSM1073_5_official_gxS_arrays",
            "required_artifact": "gx,gz,Sxx,Sxz arrays or inputs sufficient to reproduce them",
            "minimum_fields": "segment_id;t_utc;gx;gz;Sxx;Sxz;frame;generation_method;source_file",
            "acceptance_rule": "official arrays or exact source-reconstruction with documented gravity model and attitude/orbit inputs",
            "current_status": "NOT_ACQUIRED",
            "target_folder": "post-checkpoint-work/source-intake/microscope_cmsm/segment210/",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def official_array_schema_contract_rows() -> list[dict[str, str]]:
    return [
        {
            "column_id": "ARR1073_0_segment_id",
            "column_name": "segment_id",
            "units": "label",
            "required": "true",
            "source_status": "MISSING_CMSM_EXPORT",
            "replaces_1072_dry_run_column": "segment",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "column_id": "ARR1073_1_t_utc",
            "column_name": "t_utc",
            "units": "UTC timestamp",
            "required": "true",
            "source_status": "MISSING_EXACT_TIMESTAMPS",
            "replaces_1072_dry_run_column": "t_sec_from_segment_start",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "column_id": "ARR1073_2_mask_flag",
            "column_name": "mask_flag",
            "units": "boolean_or_enum",
            "required": "true",
            "source_status": "MISSING_EXACT_MASKS",
            "replaces_1072_dry_run_column": "none",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "column_id": "ARR1073_3_gx",
            "column_name": "gx",
            "units": "m s^-2 or documented normalized convention",
            "required": "true",
            "source_status": "MISSING_OFFICIAL_ARRAY",
            "replaces_1072_dry_run_column": "gx_unit",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "column_id": "ARR1073_4_gz",
            "column_name": "gz",
            "units": "m s^-2 or documented normalized convention",
            "required": "true",
            "source_status": "MISSING_OFFICIAL_ARRAY",
            "replaces_1072_dry_run_column": "gz_unit",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "column_id": "ARR1073_5_Sxx",
            "column_name": "Sxx",
            "units": "s^-2",
            "required": "true",
            "source_status": "MISSING_OFFICIAL_ARRAY",
            "replaces_1072_dry_run_column": "Sxx_unit",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "column_id": "ARR1073_6_Sxz",
            "column_name": "Sxz",
            "units": "s^-2",
            "required": "true",
            "source_status": "MISSING_OFFICIAL_ARRAY",
            "replaces_1072_dry_run_column": "Sxz_unit",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "column_id": "ARR1073_7_generation_method",
            "column_name": "generation_method",
            "units": "text",
            "required": "true",
            "source_status": "MISSING_PROVENANCE",
            "replaces_1072_dry_run_column": "source_basis",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def extraction_status_rows() -> list[dict[str, str]]:
    return [
        {
            "status_id": "EX1073_0_browser_schema",
            "object": "CMSM browser schema/file inventory",
            "status": "NOT_ACQUIRED_CONNECTION_REFUSED",
            "evidence": "BROW1073_0_direct_cmsm_module",
            "claim_allowed": "false",
            "next_action": "open CMSM in a user-controlled normal browser/session or obtain API response from accessible network",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "status_id": "EX1073_1_api_schema",
            "object": "REGARDS API schema/file inventory",
            "status": "NOT_ACQUIRED",
            "evidence": "P8_Y5_R10_1072_PORTAL_ROUTE_PROBE.csv; P8_Y5_R10_1073_PRIOR_API_RESPONSE_ATTEMPTS.csv",
            "claim_allowed": "false",
            "next_action": "supply public endpoint response, login/export, or exact query parameters",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "status_id": "EX1073_2_official_segment210_arrays",
            "object": "official segment 210 gx/gz/Sxx/Sxz arrays",
            "status": "NOT_ACQUIRED",
            "evidence": "CMSM1073_5_official_gxS_arrays",
            "claim_allowed": "false",
            "next_action": "replace 1072 dry-run preview with source-backed official arrays",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "status_id": "EX1073_3_tau_WEP",
            "object": "numeric tau_WEP",
            "status": "NOT_ACQUIRED",
            "evidence": "EX1073_2_official_segment210_arrays; ARR1073_3_gx; ARR1073_5_Sxx",
            "claim_allowed": "false",
            "next_action": "derive tau_WEP only after official arrays and MTS material/source map exist",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def product_prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1073_0_WEP_CMSM_extract_blocked_nonclaim_product",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_CMSM_SCHEMA_AND_OFFICIAL_SEGMENT210_ARRAYS",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1073_OFFICIAL_ARRAY_EXTRACT_STATUS.csv",
            "inputs_present": "browser_attempt;api_route_ledger;dry_run_replacement_contract",
            "required_inputs": "CMSM schema/file inventory; exact timestamps/masks; official gx/gz/Sxx/Sxz arrays; material tensor; Xhat normalization; tau_WEP map or direct parent product",
            "derivation_status": "EXTRACTION_BLOCKED_NO_NUMERIC_PRODUCT",
            "valid_for_claim": "false",
            "notes": "browser/API route did not yield schema or official arrays; no WEP score allowed",
        }
    ]


def bound_rows() -> list[dict[str, str]]:
    row = local_bound_row("R1_WEP_source_charge")
    url, doi = split_reference(row["reference_path_or_url"])
    return [
        {
            "bound_id": "BOUND1073_0_MICROSCOPE_R1_eta_source_charge",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": row["upper_bound"],
            "bound_units": row["units"],
            "bound_source": url,
            "source_row": f"source-intake/local_bounds/local_bound_claims.csv::{row['row_id']}; doi:{doi}",
            "bound_type": "source_backed_upper_bound_anchor",
            "valid_for_claim": "true",
            "notes": "valid bound anchor only; official prediction arrays remain absent",
        }
    ]


def product_status_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1073_0_WEP_CMSM_extract_blocked_product_stub",
            "prediction_rows": str(status.get("prediction_rows", "")),
            "bound_rows": str(status.get("bound_rows", "")),
            "valid_prediction_rows": str(status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(status.get("valid_bound_rows", "")),
            "comparison_rows": str(status.get("comparison_rows", "")),
            "passed_rows": str(status.get("passed_rows", "")),
            "claim_allowed": str(status.get("claim_allowed", "")).lower(),
            "expected_result": "reject blocked-extraction placeholder and keep claim false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1073_0_browser_access",
            "claim_component": "CMSM browser access",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "ERR_CONNECTION_REFUSED; schema/file inventory not visible",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1073_1_schema_inventory",
            "claim_component": "CMSM schema/file inventory",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "NOT_ACQUIRED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1073_2_official_arrays",
            "claim_component": "official segment 210 gx/gz/Sxx/Sxz arrays",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "MISSING_OFFICIAL_ARRAYS",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1073_3_product_runner",
            "claim_component": "WEP product runner",
            "gate_pass": "false",
            "claim_allowed": str(product_status.get("claim_allowed", "")).lower(),
            "reason": f"valid_prediction_rows={product_status.get('valid_prediction_rows')}",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1073_4_local_GR_WEP_claim",
            "claim_component": "local-GR/WEP pass",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "no official arrays and no MTS tau_WEP/product",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1073_0_browser_route_blocked",
            "decision": "CMSM browser route was attempted and blocked/refused from this runtime",
            "evidence": "BROW1073_0_direct_cmsm_module",
            "consequence": "do not keep looping on CMSM from this runtime",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1073_1_contract_not_data",
            "decision": "1073 produces an extraction contract, not official arrays",
            "evidence": "CMSM1073_5_official_gxS_arrays; ARR1073_3_gx",
            "consequence": "future official extraction has exact acceptance columns",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1073_2_no_claim",
            "decision": "keep WEP/local-GR branch blocked",
            "evidence": "EX1073_3_tau_WEP; APR1073_0_WEP_CMSM_extract_blocked_product_stub",
            "consequence": "next work must be user-assisted CMSM export or nonclaim surrogate reconstruction only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1073_0_1074",
            "next_target": "1074-Y5-R10-user-assisted-CMSM-export-or-nonclaim-surrogate-orbit-reconstruction.md",
            "objective": "either import a user/browser-supplied CMSM schema/file export matching the 1073 contract, or build a clearly nonclaim surrogate segment-210 orbit/gravity reconstruction to test the code path while keeping tau_WEP/product claims blocked.",
            "include": "user-supplied CMSM files if available; contract validation; exact required columns; surrogate route labelled nonclaim; no guessed official masks; runner refusal gates",
            "exclude": "repeating blocked CMSM browser loop; treating dry-run/surrogate arrays as official; public WEP/local-GR claim; tau=1; GitHub; formalization edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def csv_rows_parse(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
    except csv.Error:
        return False
    return True


def validate_outputs(
    outputs: dict[str, Path],
    source_rows: list[dict[str, str]],
    browser_rows: list[dict[str, str]],
    api_rows: list[dict[str, str]],
    contract_rows: list[dict[str, str]],
    schema_rows: list[dict[str, str]],
    status_rows: list[dict[str, str]],
    prediction_rows: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    contract_ids = {row["contract_id"] for row in contract_rows}
    column_names = {row["column_name"] for row in schema_rows}
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V1073_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in source_rows), "all cited local source paths and needles are present"))
    checks.append(("V1073_1_browser_block_recorded", any(row["browser_id"] == "BROW1073_0_direct_cmsm_module" and row["observed_status"] == "ERR_CONNECTION_REFUSED" and row["schema_inventory_acquired"] == "false" for row in browser_rows), "browser route refusal recorded"))
    checks.append(("V1073_2_prior_api_attempts_imported", len(api_rows) >= 6 and all(row["official_array_acquired"] == "false" for row in api_rows), "prior API attempts imported and remain nonclaim"))
    checks.append(("V1073_3_contract_complete", {"CMSM1073_0_dataset_inventory", "CMSM1073_1_time_mask", "CMSM1073_3_attitude_rate", "CMSM1073_4_orbit_ephemeris", "CMSM1073_5_official_gxS_arrays"}.issubset(contract_ids), "CMSM extraction contract covers inventory/time/mask/attitude/orbit/gxS"))
    checks.append(("V1073_4_schema_columns", {"t_utc", "mask_flag", "gx", "gz", "Sxx", "Sxz", "generation_method"}.issubset(column_names), "official array schema contract includes required replacement columns"))
    checks.append(("V1073_5_status_not_acquired", all(row["status"] != "ACQUIRED" and row["claim_allowed"] == "false" for row in status_rows), "all extraction statuses remain blocked/nonclaim"))
    checks.append(("V1073_6_prediction_nonclaim_missing", any("MISSING_CMSM_SCHEMA_AND_OFFICIAL_SEGMENT210_ARRAYS" in row["product_value"] and row["valid_for_claim"] == "false" for row in prediction_rows), "prediction row remains missing official arrays"))
    checks.append(("V1073_7_bound_numeric", bool(bound_rows_) and float(bound_rows_[0]["bound_value"]) > 0 and bound_rows_[0]["valid_for_claim"] == "true", "bound import is positive numeric"))
    checks.append(("V1073_8_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "runner reports no valid prediction rows and claim false"))
    checks.append(("V1073_9_claim_gates_safe", all(row["claim_allowed"] == "false" for row in claim_rows), "all claim gates deny WEP/local-GR claim"))
    checks.append(("V1073_10_next_target", any("1074-Y5-R10-user-assisted-CMSM-export-or-nonclaim-surrogate-orbit-reconstruction.md" in row["next_target"] for row in next_rows), "1074 handoff written"))
    generated_paths = list(outputs.values()) + [DOC]
    checks.append(("V1073_11_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    checks.append(("V1073_12_csv_parse", all(path.exists() and csv_rows_parse(path) for path in outputs.values() if path.suffix == ".csv" and path.name != "P8_Y5_BRR545_1073_VALIDATION.csv"), "all 1073 CSV outputs parse cleanly"))
    checks.append(("V1073_13_formalization_untouched", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains zero"))
    checks.append(("V1073_SUMMARY", True, "CMSM browser/API extraction blocked; official array contract staged; WEP/product claim blocked"))
    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for check_id, passed, detail in checks
    ]


def write_doc(
    source_rows: list[dict[str, str]],
    browser_rows: list[dict[str, str]],
    api_rows: list[dict[str, str]],
    contract_rows: list[dict[str, str]],
    schema_rows: list[dict[str, str]],
    status_rows: list[dict[str, str]],
    prediction_rows: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status_rows_: list[dict[str, str]],
    product_comparison_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1073 - CMSM browser-assisted schema or one-segment official array extract",
            "",
            "## Current verdict",
            "1073 attempted the browser-assisted CMSM route and did not obtain schema/data: the CMSM REGARDS module refused connection from this runtime. This checkpoint therefore stages the exact official-array extraction contract and keeps the WEP/local-GR product branch blocked.",
            "",
            "## Local source register",
            md_table(source_rows, ["source_id", "relative_path", "exists", "needle_found", "note"]),
            "## Browser attempt ledger",
            md_table(browser_rows, ["browser_id", "surface", "target_url", "observed_title", "observed_status", "schema_inventory_acquired", "official_array_acquired", "note"]),
            "## Prior API response attempts",
            md_table(api_rows, ["attempt_id", "target_url", "probe_status", "http_status", "schema_inventory_acquired", "official_array_acquired", "error_summary"]),
            "## CMSM export contract",
            md_table(contract_rows, ["contract_id", "required_artifact", "minimum_fields", "acceptance_rule", "current_status"]),
            "## Official array schema contract",
            md_table(schema_rows, ["column_id", "column_name", "units", "required", "source_status", "replaces_1072_dry_run_column"]),
            "## Extraction status",
            md_table(status_rows, ["status_id", "object", "status", "next_action", "claim_allowed"]),
            "## Nonclaim product candidate",
            md_table(prediction_rows, ["prediction_id", "product_symbol", "product_value", "derivation_status", "valid_for_claim"]),
            "## Bound import",
            md_table(bound_rows_, ["bound_id", "product_symbol", "bound_value", "bound_units", "valid_for_claim"]),
            "## Product runner status",
            md_table(product_status_rows_, ["runner_id", "valid_prediction_rows", "valid_bound_rows", "claim_allowed", "expected_result"]),
            "## Product comparison rows",
            md_table(product_comparison_rows, ["comparison_id", "comparison_status", "pass_for_claim", "issues"]),
            "## Claim gates",
            md_table(claim_rows, ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason"]),
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "evidence", "consequence"]),
            "## Validation",
            md_table(validation_rows, ["check_id", "result", "detail"]),
            "## Next target",
            md_table(next_rows, ["next_id", "next_target", "objective", "include", "exclude"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    browser_rows = browser_attempt_rows()
    api_rows = api_response_attempt_rows()
    contract_rows = cmsm_export_contract_rows()
    schema_rows = official_array_schema_contract_rows()
    status_rows = extraction_status_rows()
    prediction_rows = product_prediction_rows()
    bound_rows_ = bound_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R10_1073_SOURCE_REGISTER.csv",
        "browser_attempt": OUT / "P8_Y5_R10_1073_BROWSER_ATTEMPT_LEDGER.csv",
        "api_attempts": OUT / "P8_Y5_R10_1073_PRIOR_API_RESPONSE_ATTEMPTS.csv",
        "export_contract": OUT / "P8_Y5_R10_1073_CMSM_EXPORT_CONTRACT.csv",
        "schema_contract": OUT / "P8_Y5_R10_1073_OFFICIAL_ARRAY_SCHEMA_CONTRACT.csv",
        "extract_status": OUT / "P8_Y5_R10_1073_OFFICIAL_ARRAY_EXTRACT_STATUS.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1073_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1073_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1073_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1073_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1073_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1073_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["browser_attempt"], browser_rows)
    write_csv(outputs["api_attempts"], api_rows)
    write_csv(outputs["export_contract"], contract_rows)
    write_csv(outputs["schema_contract"], schema_rows)
    write_csv(outputs["extract_status"], status_rows)
    write_csv(outputs["prediction"], prediction_rows, PRODUCT_REQUIRED_COLUMNS)
    write_csv(outputs["bound"], bound_rows_, BOUND_REQUIRED_COLUMNS)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next_target"], next_rows)

    product_result = run_product_runner(PREDICTION_TEMPLATE, BOUND_IMPORT, PRODUCT_RUN_DIR)
    product_status = product_result["status"]
    product_status_rows_ = product_status_rows(product_status)
    claim_rows = claim_gate_rows(product_status)

    write_csv(outputs["product_status"], product_status_rows_)
    write_csv(outputs["product_comparison"], product_result["comparisons"])
    write_csv(outputs["claim_gates"], claim_rows)

    remove_pycache()
    validation_rows = validate_outputs(
        outputs,
        source_rows,
        browser_rows,
        api_rows,
        contract_rows,
        schema_rows,
        status_rows,
        prediction_rows,
        bound_rows_,
        product_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        browser_rows,
        api_rows,
        contract_rows,
        schema_rows,
        status_rows,
        prediction_rows,
        bound_rows_,
        product_status_rows_,
        product_result["comparisons"],
        claim_rows,
        decisions,
        validation_rows,
        next_rows,
    )
    remove_pycache()

    failed = [row for row in validation_rows if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
