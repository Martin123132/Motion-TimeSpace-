from __future__ import annotations

import csv
import math
import shutil
import ssl
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_STARTED_UTC = datetime.now(timezone.utc)
ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
WORK = ROOT / "post-checkpoint-work"
MTS = WORK / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = WORK / "source-intake" / "local_bounds"
RAB_QUEUE = WORK / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = WORK / "source-intake" / "beta-source" / "docs"
MICROSCOPE_DIR = WORK / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
CMSM_DIR = WORK / "source-intake" / "microscope_cmsm"
SCRIPTS = WORK / "scripts"
FORMALIZATION = ROOT / "formalization-workbench"
DOC = WORK / "2779-Y5-R2FR-MICROSCOPE-data-portal-schema-or-reconstructed-gxS-kernel-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2779_SOURCE_REGISTER.csv",
    "external": MTS / "P8_Y5_R2FR_2779_EXTERNAL_SOURCE_LEDGER.csv",
    "portal": MTS / "P8_Y5_R2FR_2779_PORTAL_ROUTE_PROBE.csv",
    "endpoints": MTS / "P8_Y5_R2FR_2779_CMSM_REGARDS_API_CANDIDATE_ENDPOINTS.csv",
    "requirements": MTS / "P8_Y5_R2FR_2779_RECONSTRUCTION_REQUIREMENTS.csv",
    "dry_meta": MTS / "P8_Y5_R2FR_2779_GXS_DRY_RUN_METADATA_SEGMENT210.csv",
    "dry_preview": MTS / "P8_Y5_R2FR_2779_GXS_DRY_RUN_KERNEL_PREVIEW_SEGMENT210.csv",
    "export_contract": MTS / "P8_Y5_R2FR_2779_CMSM_EXPORT_CONTRACT.csv",
    "array_contract": MTS / "P8_Y5_R2FR_2779_OFFICIAL_ARRAY_SCHEMA_CONTRACT.csv",
    "tau": MTS / "P8_Y5_R2FR_2779_NUMERIC_TAU_STATUS.csv",
    "candidate": MTS / "P8_Y5_R2FR_2779_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv",
    "bounds": MTS / "P8_Y5_R2FR_2779_WEP_BOUND_IMPORT.csv",
    "runner": MTS / "P8_Y5_R2FR_2779_PRODUCT_RUNNER_STATUS.csv",
    "comparisons": MTS / "P8_Y5_R2FR_2779_PRODUCT_COMPARISON_ROWS.csv",
    "gates": MTS / "P8_Y5_R2FR_2779_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2779_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2779_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2779_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2779_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "route_queue": RAB_QUEUE / "JR2779_CMSM_ROUTE_AND_ENDPOINTS_NONCLAIM.csv",
    "dryrun_queue": RAB_QUEUE / "JR2779_SEGMENT210_DRY_RUN_GXS_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "MICROSCOPE_GXS_DRY_RUN_2779_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_gxS_dry_run_2779_nonclaim.csv",
    "cmsm_contract": CMSM_DIR / "CMSM_EXPORT_AND_ARRAY_CONTRACT_2779_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2779_USER_EXPORT_OR_SURROGATE_NEXT.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(WORK))
    except ValueError:
        return str(path)


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["valid_for_claim"] = False
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def csv_row_count(path: Path) -> int:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        cells = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def is_numeric(value: Any) -> bool:
    try:
        float(str(value))
    except (TypeError, ValueError):
        return False
    return True


def has_missing_marker(row: dict[str, Any]) -> bool:
    return "MISSING" in " ".join(str(value) for value in row.values())


def get_local_bound(row_id: str) -> dict[str, str]:
    for row in read_csv_rows(LOCAL_BOUNDS / "local_bound_claims.csv"):
        if row.get("row_id") == row_id:
            return row
    return {}


def source_row(row_id: str, source_key: str, path: Path, needle: str, role: str) -> dict[str, Any]:
    text = read_text(path)
    exists = path.exists()
    return nonclaim({
        "row_id": row_id,
        "source_key": source_key,
        "source_path": str(path),
        "exists": exists,
        "needle": needle,
        "needle_found": exists and needle in text,
        "source_role": role,
    })


def build_sources() -> list[dict[str, Any]]:
    specs = [
        ("SRC2779_00_2778_next", "2778_next", MTS / "P8_Y5_R2FR_2778_NEXT_TARGET.csv", "NEXT2778_0_2779", "current handoff into data-portal schema or gxS reconstruction"),
        ("SRC2779_01_2778_validation", "2778_validation", MTS / "P8_Y5_BRR545_2778_VALIDATION.csv", "VAL2778_OVERALL", "current validation baseline"),
        ("SRC2779_02_2778_kernel", "2778_kernel", MTS / "P8_Y5_R2FR_2778_OFFICIAL_KERNEL_COMPONENTS.csv", "KER2778_6_verdict", "current official kernel skeleton"),
        ("SRC2779_03_2778_segments", "2778_segments", MTS / "P8_Y5_R2FR_2778_SUEP_SEGMENT_TABLE_SOURCE_BACKED.csv", "SUEP2778_210", "current SUEP segment ledger"),
        ("SRC2779_04_2778_portal", "2778_portal", MTS / "P8_Y5_R2FR_2778_DATA_PORTAL_PROBE.csv", "cmsm-ds.onera.fr", "current portal probe"),
        ("SRC2779_05_2778_tau", "2778_tau", MTS / "P8_Y5_R2FR_2778_TAU_PROJECTION_STATUS.csv", "TAU2778_3_verdict", "current tau blocker"),
        ("SRC2779_06_1072_doc", "1072_doc", WORK / "1072-Y5-R10-MICROSCOPE-data-portal-schema-or-reconstructed-gxS-kernel.md", "Dry-run kernel metadata", "R10 precedent for portal route and segment-210 dry-run"),
        ("SRC2779_07_1072_external", "1072_external", MTS / "P8_Y5_R10_1072_EXTERNAL_SOURCE_LEDGER.csv", "EXT1072_2_REGARDS_search_download", "prior external route ledger"),
        ("SRC2779_08_1072_endpoints", "1072_endpoints", MTS / "P8_Y5_R10_1072_CMSM_REGARDS_API_CANDIDATE_ENDPOINTS.csv", "API1072_4_module_config", "prior candidate REGARDS endpoint ledger"),
        ("SRC2779_09_1072_requirements", "1072_requirements", MTS / "P8_Y5_R10_1072_RECONSTRUCTION_REQUIREMENTS.csv", "REQ1072_5_material_parent_map", "prior reconstruction requirement table"),
        ("SRC2779_10_1072_preview", "1072_preview", MTS / "P8_Y5_R10_1072_GXS_DRY_RUN_KERNEL_PREVIEW_SEGMENT210.csv", "GXS1072_210_31", "prior dry-run preview endpoint"),
        ("SRC2779_11_1073_contract", "1073_contract", MTS / "P8_Y5_R10_1073_CMSM_EXPORT_CONTRACT.csv", "CMSM1073_5_official_gxS_arrays", "prior CMSM export contract"),
        ("SRC2779_12_1073_array_contract", "1073_array_contract", MTS / "P8_Y5_R10_1073_OFFICIAL_ARRAY_SCHEMA_CONTRACT.csv", "ARR1073_7_generation_method", "prior official array schema contract"),
        ("SRC2779_13_local_bounds", "local_bounds", LOCAL_BOUNDS / "local_bound_claims.csv", "R1_WEP_source_charge", "local MICROSCOPE WEP bound source row"),
    ]
    return [source_row(*spec) for spec in specs]


def remap(value: str) -> str:
    return value.replace("1072", "2779").replace("1073", "2779")


def build_external_rows() -> list[dict[str, Any]]:
    source_rows = read_csv_rows(MTS / "P8_Y5_R10_1072_EXTERNAL_SOURCE_LEDGER.csv")
    rows: list[dict[str, Any]] = []
    for source in source_rows:
        rows.append(nonclaim({
            "external_id": remap(source.get("external_id", "")),
            "source_url": source.get("source_url", ""),
            "source_lines": source.get("source_lines", ""),
            "use_for_2779": source.get("use_for_1072", "").replace("1072", "2779"),
            "extracted_item": source.get("extracted_item", ""),
            "port_status": "PORTED_FROM_R10_1072_INTO_R2FR_NONCLAIM_BRANCH",
            "generated_utc": ts(),
        }))
    return rows


def probe_url(url: str, retry_unverified_ssl: bool = True) -> dict[str, Any]:
    started = ts()
    request = urllib.request.Request(url, headers={"User-Agent": "MTS-private-checkpoint/2779"})
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            sample = response.read(1024)
            return nonclaim({
                "url": url,
                "probe_status": "HTTP_OK",
                "http_status": getattr(response, "status", ""),
                "content_type": response.headers.get("content-type", ""),
                "bytes_sampled": len(sample),
                "error": "",
                "schema_or_data_inventory_acquired": False,
                "probe_started_utc": started,
            })
    except urllib.error.URLError as exc:
        if retry_unverified_ssl and "CERTIFICATE_VERIFY_FAILED" in str(exc):
            try:
                context = ssl._create_unverified_context()
                with urllib.request.urlopen(request, timeout=5, context=context) as response:
                    sample = response.read(1024)
                    return nonclaim({
                        "url": url,
                        "probe_status": "HTTP_OK_INSECURE_SSL_RETRY",
                        "http_status": getattr(response, "status", ""),
                        "content_type": response.headers.get("content-type", ""),
                        "bytes_sampled": len(sample),
                        "error": "standard SSL verification failed; unverified retry used only to record public page reachability, not for claim evidence",
                        "schema_or_data_inventory_acquired": False,
                        "probe_started_utc": started,
                    })
            except Exception as retry_exc:
                return nonclaim({
                    "url": url,
                    "probe_status": "BLOCKED_OR_UNREACHABLE_FROM_THIS_RUN",
                    "http_status": getattr(retry_exc, "code", ""),
                    "content_type": "",
                    "bytes_sampled": 0,
                    "error": f"{type(retry_exc).__name__}: {retry_exc}",
                    "schema_or_data_inventory_acquired": False,
                    "probe_started_utc": started,
                })
        return nonclaim({
            "url": url,
            "probe_status": "BLOCKED_OR_UNREACHABLE_FROM_THIS_RUN",
            "http_status": getattr(exc, "code", ""),
            "content_type": "",
            "bytes_sampled": 0,
            "error": f"{type(exc).__name__}: {exc}",
            "schema_or_data_inventory_acquired": False,
            "probe_started_utc": started,
        })
    except Exception as exc:
        return nonclaim({
            "url": url,
            "probe_status": "BLOCKED_OR_UNREACHABLE_FROM_THIS_RUN",
            "http_status": getattr(exc, "code", ""),
            "content_type": "",
            "bytes_sampled": 0,
            "error": f"{type(exc).__name__}: {exc}",
            "schema_or_data_inventory_acquired": False,
            "probe_started_utc": started,
        })


def build_portal_rows() -> list[dict[str, Any]]:
    urls = [
        "https://microscope.onera.fr/fr/publication/microscope-data-are-available",
        "https://www.oca.eu/fr/microscope",
        "https://cmsm-ds.onera.fr/user/microscope",
        "https://cmsm-ds.onera.fr/user/microscope/modules/7",
        "https://cmsm-ds.onera.fr/api/v1/rs-access-project/datasets/search",
        "https://cmsm-ds.onera.fr/api/v1/rs-access-project/dataobjects/search",
        "https://cmsm-ds.onera.fr/api/v1/rs-access-project/dataobjects/datasets/search",
        "https://cmsm-ds.onera.fr/api/v1/rs-access-project/applications/microscope/modules",
    ]
    return [probe_url(url) for url in urls]


def build_endpoint_rows() -> list[dict[str, Any]]:
    source_rows = read_csv_rows(MTS / "P8_Y5_R10_1072_CMSM_REGARDS_API_CANDIDATE_ENDPOINTS.csv")
    rows: list[dict[str, Any]] = []
    for source in source_rows:
        rows.append(nonclaim({
            "endpoint_id": remap(source.get("endpoint_id", "")),
            "candidate_url": source.get("candidate_url", ""),
            "regards_basis": source.get("regards_basis", ""),
            "expected_payload": source.get("expected_payload", ""),
            "auth_or_access_risk": source.get("auth_or_access_risk", ""),
            "schema_inventory_acquired": False,
            "generated_utc": ts(),
        }))
    return rows


def build_requirement_rows() -> list[dict[str, Any]]:
    source_rows = read_csv_rows(MTS / "P8_Y5_R10_1072_RECONSTRUCTION_REQUIREMENTS.csv")
    rows: list[dict[str, Any]] = []
    for source in source_rows:
        rows.append(nonclaim({
            "requirement_id": remap(source.get("requirement_id", "")),
            "object": source.get("object", ""),
            "why_needed": source.get("why_needed", ""),
            "current_status": source.get("current_status", ""),
            "source_hint": source.get("source_hint", ""),
            "branch_status": "REQUIRED_BEFORE_R2FR_WEP_SCORE",
        }))
    return rows


def build_dry_run_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    segment = 210
    duration_orbits = 50
    sample_rate_hz = 4
    torb_s = 5946
    full_grid_samples = duration_orbits * torb_s * sample_rate_hz
    preview_rows_written = 32
    forb_hz = 0.00016818
    fspin_hz = 0.00294315
    fep_hz = 0.00311133
    metadata = [
        nonclaim({
            "dry_run_id": "DRY2779_0_segment210_kernel_preview",
            "segment": segment,
            "spin_mode": "V3",
            "duration_orbits": duration_orbits,
            "sample_rate_hz": sample_rate_hz,
            "torb_s": torb_s,
            "full_grid_samples": full_grid_samples,
            "preview_rows_written": preview_rows_written,
            "forb_hz": forb_hz,
            "fspin_hz": fspin_hz,
            "fep_hz": fep_hz,
            "phase_convention": "dry_run_zero_phase_not_claim",
            "amplitude_convention": "dimensionless_unit_columns_not_physical_g_or_S",
            "kernel_status": "DRY_RUN_NUMERIC_PREVIEW_ONLY_NOT_TAU",
            "generated_utc": ts(),
        })
    ]
    preview: list[dict[str, Any]] = []
    step = (full_grid_samples - 9) // (preview_rows_written - 1)
    for index in range(preview_rows_written):
        sample_index = index * step
        t_sec = sample_index / sample_rate_hz
        orbital_phase = (2.0 * math.pi * forb_hz * t_sec) % (2.0 * math.pi)
        fep_phase = (2.0 * math.pi * fep_hz * t_sec) % (2.0 * math.pi)
        preview.append(nonclaim({
            "preview_id": f"GXS2779_210_{index:02d}",
            "segment": segment,
            "sample_index": sample_index,
            "t_sec_from_segment_start": round(t_sec, 12),
            "orbit_fraction_from_start": round(t_sec / torb_s, 12),
            "orbital_phase_zeroed_rad": round(orbital_phase, 12),
            "fep_phase_zeroed_rad": round(fep_phase, 12),
            "gx_unit": round(math.cos(fep_phase), 12),
            "gz_unit": round(math.sin(fep_phase), 12),
            "Sxx_unit": round(math.cos(2.0 * fep_phase), 12),
            "Sxz_unit": round(math.sin(2.0 * fep_phase), 12),
            "poly0": 1.0,
            "poly1_centered": round(sample_index / (full_grid_samples - 1) - 0.5, 12),
            "source_basis": "CQG_eq7_shape_only",
            "phase_convention": "dry_run_zero_phase_not_claim",
            "generated_utc": ts(),
        }))
    return metadata, preview


def build_export_contract() -> list[dict[str, Any]]:
    source_rows = read_csv_rows(MTS / "P8_Y5_R10_1073_CMSM_EXPORT_CONTRACT.csv")
    rows: list[dict[str, Any]] = []
    for source in source_rows:
        rows.append(nonclaim({
            "contract_id": remap(source.get("contract_id", "")),
            "required_artifact": source.get("required_artifact", ""),
            "minimum_fields": source.get("minimum_fields", ""),
            "acceptance_rule": source.get("acceptance_rule", ""),
            "current_status": source.get("current_status", "NOT_ACQUIRED"),
            "target_folder": source.get("target_folder", "").replace("post-checkpoint-work/source-intake/microscope_cmsm/", "source-intake/microscope_cmsm/"),
            "generated_utc": ts(),
        }))
    return rows


def build_array_contract() -> list[dict[str, Any]]:
    source_rows = read_csv_rows(MTS / "P8_Y5_R10_1073_OFFICIAL_ARRAY_SCHEMA_CONTRACT.csv")
    rows: list[dict[str, Any]] = []
    for source in source_rows:
        rows.append(nonclaim({
            "column_id": remap(source.get("column_id", "")),
            "column_name": source.get("column_name", ""),
            "units": source.get("units", ""),
            "required": source.get("required", ""),
            "source_status": source.get("source_status", ""),
            "replaces_1072_dry_run_column": source.get("replaces_1072_dry_run_column", ""),
            "branch_status": "REQUIRED_TO_REPLACE_2779_DRY_RUN_PREVIEW",
            "generated_utc": ts(),
        }))
    return rows


def build_tau_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"status_id": "NTS2779_0_schema_inventory", "object": "CMSM schema/file inventory", "status": "NOT_ACQUIRED_FROM_LOCAL_PROBE", "next_action": "user/browser-supplied CMSM export or exact public REGARDS query response", "claim_allowed": False}),
        nonclaim({"status_id": "NTS2779_1_dry_run_preview", "object": "segment 210 gx/gz/Sxx/Sxz preview", "status": "DRY_RUN_NUMERIC_PREVIEW_ONLY", "next_action": "replace zero-phase/unit-amplitude columns with official arrays or source-reconstructed arrays", "claim_allowed": False}),
        nonclaim({"status_id": "NTS2779_2_export_contract", "object": "CMSM official-array extraction contract", "status": "STAGED_NOT_FILLED", "next_action": "validate incoming export against contract rows before treating it as evidence", "claim_allowed": False}),
        nonclaim({"status_id": "NTS2779_3_tau_WEP", "object": "numeric tau_WEP", "status": "NOT_ACQUIRED", "next_action": "derive tau_WEP only after official arrays and MTS material/source map exist", "claim_allowed": False}),
    ]


def build_candidate_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "prediction_id": "PRED2779_0_WEP_gxS_dry_run_kernel_nonclaim_product",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_OFFICIAL_NUMERIC_TAU_WEP_KERNEL_DRY_RUN_ONLY",
            "product_units": "dimensionless",
            "derivation_status": "DRY_RUN_NUMERIC_PREVIEW_ONLY_NOT_CLAIM",
            "notes": "segment-210 design columns are generated only to exercise the code path; no official CMSM arrays, masks, phase, or MTS product exists yet",
        })
    ]


def build_bound_rows() -> list[dict[str, Any]]:
    bound = get_local_bound("R1_WEP_source_charge")
    return [
        nonclaim({
            "bound_id": "BOUND2779_0_MICROSCOPE_R1_eta_source_charge",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": bound.get("upper_bound", "2.8e-15"),
            "bound_units": bound.get("units", "dimensionless"),
            "bound_type": "source_backed_upper_bound_anchor",
            "source_row_id": "R1_WEP_source_charge",
            "bound_valid_for_internal_runner": True,
        })
    ]


def run_product_runner(predictions: list[dict[str, Any]], bounds: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    valid_predictions = [
        row for row in predictions
        if row.get("valid_for_claim") is True
        and is_numeric(row.get("product_value"))
        and not has_missing_marker(row)
    ]
    valid_bounds = [
        row for row in bounds
        if row.get("bound_valid_for_internal_runner") is True
        and is_numeric(row.get("bound_value"))
        and float(str(row["bound_value"])) > 0.0
        and not has_missing_marker(row)
    ]
    comparisons = [
        nonclaim({"comparison_id": "PRODUCT_COMPARE_NO_VALID_PREDICTIONS", "comparison_status": "not_run", "pass_for_claim": False, "issues": "no valid MTS tau_WEP/direct-product prediction rows"})
    ]
    runner = [
        nonclaim({
            "runner_id": "APR2779_0_WEP_gxS_dry_run_product_stub",
            "prediction_rows": len(predictions),
            "bound_rows": len(bounds),
            "valid_prediction_rows": len(valid_predictions),
            "valid_bound_rows": len(valid_bounds),
            "claim_allowed": False,
            "expected_result": "reject dry-run/placeholder prediction and keep claim false",
        })
    ]
    return runner, comparisons


def build_gates() -> list[dict[str, Any]]:
    return [
        nonclaim({"gate_id": "CG2779_0_portal_schema", "claim_component": "CMSM data schema/file inventory", "gate_pass": False, "claim_allowed": False, "reason": "portal route known but schema/product inventory not acquired by local probe"}),
        nonclaim({"gate_id": "CG2779_1_candidate_endpoints", "claim_component": "REGARDS candidate endpoints", "gate_pass": True, "claim_allowed": False, "reason": "endpoint map staged, but no authenticated/public schema response acquired"}),
        nonclaim({"gate_id": "CG2779_2_dry_run_kernel", "claim_component": "gx/gz/Sxx/Sxz dry-run numeric preview", "gate_pass": True, "claim_allowed": False, "reason": "code path exists, but phase/amplitude/timestamps/masks are dry-run placeholders"}),
        nonclaim({"gate_id": "CG2779_3_export_contract", "claim_component": "official CMSM array contract", "gate_pass": True, "claim_allowed": False, "reason": "contract staged; required official export rows still NOT_ACQUIRED"}),
        nonclaim({"gate_id": "CG2779_4_official_numeric_kernel", "claim_component": "official numeric kernel arrays", "gate_pass": False, "claim_allowed": False, "reason": "MISSING_OFFICIAL_GX_GZ_SXX_SXZ_ARRAYS"}),
        nonclaim({"gate_id": "CG2779_5_tau_WEP_numeric", "claim_component": "numeric tau_WEP or direct parent product", "gate_pass": False, "claim_allowed": False, "reason": "MISSING_OFFICIAL_NUMERIC_TAU_WEP_KERNEL_DRY_RUN_ONLY"}),
        nonclaim({"gate_id": "CG2779_6_product_runner", "claim_component": "WEP product runner", "gate_pass": False, "claim_allowed": False, "reason": "valid_prediction_rows=0"}),
    ]


def build_decisions() -> list[dict[str, Any]]:
    return [
        nonclaim({"decision_id": "DEC2779_0_portal_route_not_enough", "decision": "CMSM/REGARDS route is source-backed but not locally inventory-readable yet", "evidence": "P8_Y5_R2FR_2779_PORTAL_ROUTE_PROBE.csv; P8_Y5_R2FR_2779_CMSM_REGARDS_API_CANDIDATE_ENDPOINTS.csv", "consequence": "do not keep looping on local CMSM probes without a user/session/export change"}),
        nonclaim({"decision_id": "DEC2779_1_dry_run_kernel_path", "decision": "segment 210 dry-run kernel preview establishes the reconstruction code path in the R2/f(R) branch", "evidence": "DRY2779_0_segment210_kernel_preview; GXS2779_210_31", "consequence": "future work can replace unit zero-phase columns with official arrays"}),
        nonclaim({"decision_id": "DEC2779_2_contract_staged", "decision": "official-array import contract is staged now instead of waiting for another blocked browser pass", "evidence": "CMSM2779_5_official_gxS_arrays; ARR2779_7_generation_method", "consequence": "incoming CMSM/manual exports can be validated mechanically"}),
        nonclaim({"decision_id": "DEC2779_3_no_claim", "decision": "do not score WEP/local-GR claim", "evidence": "NTS2779_3_tau_WEP; APR2779_0_WEP_gxS_dry_run_product_stub", "consequence": "numeric tau_WEP remains the barrier"}),
    ]


def build_next() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "row_id": "NEXT2779_0_2780",
            "next_target": "2780-Y5-R2FR-user-assisted-CMSM-export-or-nonclaim-surrogate-orbit-reconstruction-under-AX1090.md",
            "script": "scripts/Y5_R2FR_user_assisted_CMSM_export_or_nonclaim_surrogate_orbit_reconstruction_under_AX1090_2780.py",
            "objective": "either import a user/browser-supplied CMSM schema/file export matching the 2779 contract, or build a clearly nonclaim surrogate segment-210 orbit/gravity reconstruction to test the code path while keeping tau_WEP/product claims blocked",
            "include": "user-supplied CMSM files if available; contract validation; exact required columns; surrogate route labelled nonclaim; no guessed official masks; runner refusal gates",
            "exclude": "repeating blocked CMSM browser loop; treating dry-run/surrogate arrays as official; public WEP/local-GR claim; tau=1; GitHub; formalization edits",
        })
    ]


def copy_branch_outputs(
    external: list[dict[str, Any]],
    portal: list[dict[str, Any]],
    endpoints: list[dict[str, Any]],
    requirements: list[dict[str, Any]],
    dry_meta: list[dict[str, Any]],
    dry_preview: list[dict[str, Any]],
    export_contract: list[dict[str, Any]],
    array_contract: list[dict[str, Any]],
    tau: list[dict[str, Any]],
    candidate: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    route_rows = external + portal + endpoints + requirements + gates
    dryrun_rows = dry_meta + dry_preview + tau + candidate + gates
    beta_rows = requirements + dry_meta + tau + next_rows
    microscope_rows = external + portal + endpoints + requirements + dry_meta + dry_preview + export_contract + array_contract + tau + candidate + next_rows
    contract_rows = export_contract + array_contract + next_rows
    specs = [
        ("BR2779_0_route_queue", "route", route_rows, OUTPUTS["portal"], BRANCH_OUTPUTS["route_queue"], "CMSM/REGARDS route and endpoint nonclaim copy"),
        ("BR2779_1_dryrun_queue", "dryrun", dryrun_rows, OUTPUTS["dry_preview"], BRANCH_OUTPUTS["dryrun_queue"], "segment-210 dry-run gxS nonclaim copy"),
        ("BR2779_2_beta_doc", "beta_doc", beta_rows, OUTPUTS["tau"], BRANCH_OUTPUTS["beta_doc"], "beta/source-facing dry-run kernel copy"),
        ("BR2779_3_microscope_copy", "microscope", microscope_rows, OUTPUTS["candidate"], BRANCH_OUTPUTS["microscope_copy"], "MICROSCOPE gxS dry-run acquisition copy"),
        ("BR2779_4_cmsm_contract", "cmsm_contract", contract_rows, OUTPUTS["export_contract"], BRANCH_OUTPUTS["cmsm_contract"], "CMSM export and official-array contract copy"),
        ("BR2779_5_next_queue", "next", next_rows, OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next user export or surrogate reconstruction target"),
    ]
    rows = []
    for copy_id, table_key, source_rows, source_table, copy_path, purpose in specs:
        write_csv(copy_path, source_rows)
        rows.append(nonclaim({
            "copy_id": copy_id,
            "table_key": table_key,
            "source_table": rel(source_table),
            "copy_path": rel(copy_path),
            "purpose": purpose,
            "exists": copy_path.exists(),
            "row_count": csv_row_count(copy_path) if copy_path.exists() else 0,
        }))
    return rows


def generated_files_under_work() -> bool:
    generated = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    return all(WORK in path.parents or path == WORK for path in generated)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and path.stat().st_mtime > RUN_STARTED_UTC.timestamp():
            return False
    return True


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if str(row.get("valid_for_claim", "False")).lower() == "true":
                return False
            if str(row.get("claim_allowed", "False")).lower() == "true":
                return False
            if str(row.get("pass_for_claim", "False")).lower() == "true":
                return False
    return True


def remove_pycache() -> None:
    pycache = SCRIPTS / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def build_validation(rows_by_name: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    sources = rows_by_name["sources"]
    external = rows_by_name["external"]
    portal = rows_by_name["portal"]
    endpoints = rows_by_name["endpoints"]
    requirements = rows_by_name["requirements"]
    dry_meta = rows_by_name["dry_meta"]
    dry_preview = rows_by_name["dry_preview"]
    export_contract = rows_by_name["export_contract"]
    array_contract = rows_by_name["array_contract"]
    tau = rows_by_name["tau"]
    candidate = rows_by_name["candidate"]
    bounds = rows_by_name["bounds"]
    runner = rows_by_name["runner"]
    gates = rows_by_name["gates"]
    next_rows = rows_by_name["next"]
    branches = rows_by_name["branches"]
    checks = [
        ("VAL2779_0_sources", all(row["exists"] and row["needle_found"] for row in sources), "every cited source path exists and source needle was found"),
        ("VAL2779_1_external_sources_recorded", len(external) >= 7 and any(row["external_id"] == "EXT2779_2_REGARDS_search_download" for row in external), "OCA/ONERA/REGARDS/CQG source rows recorded"),
        ("VAL2779_2_portal_probes_recorded", len(portal) == 8 and all(row["url"].startswith("https://") and row["probe_status"] for row in portal), "CMSM portal and API route probes recorded"),
        ("VAL2779_3_endpoint_candidates", len(endpoints) == 5 and all(row["schema_inventory_acquired"] is False for row in endpoints), "REGARDS candidate API endpoints staged as nonclaim"),
        ("VAL2779_4_requirements_block_claim", len(requirements) >= 6 and any(row["requirement_id"] == "REQ2779_5_material_parent_map" for row in requirements), "core numeric reconstruction requirements remain explicit"),
        ("VAL2779_5_dry_run_metadata", len(dry_meta) == 1 and dry_meta[0]["full_grid_samples"] == 1189200 and dry_meta[0]["kernel_status"] == "DRY_RUN_NUMERIC_PREVIEW_ONLY_NOT_TAU", "dry-run metadata has expected segment 210 sample count and nonclaim status"),
        ("VAL2779_6_preview_rows", len(dry_preview) == 32 and all(row["valid_for_claim"] is False and is_numeric(row["gx_unit"]) and is_numeric(row["Sxz_unit"]) for row in dry_preview), "32 nonclaim preview rows written"),
        ("VAL2779_7_export_contract", len(export_contract) == 6 and any(row["contract_id"] == "CMSM2779_5_official_gxS_arrays" for row in export_contract), "CMSM export contract covers inventory/time/mask/attitude/orbit/gxS"),
        ("VAL2779_8_array_contract", len(array_contract) == 8 and any(row["column_id"] == "ARR2779_7_generation_method" for row in array_contract), "official array schema contract includes required replacement columns"),
        ("VAL2779_9_tau_not_acquired", any(row["status_id"] == "NTS2779_3_tau_WEP" and row["status"] == "NOT_ACQUIRED" and row["claim_allowed"] is False for row in tau), "numeric tau_WEP remains not acquired"),
        ("VAL2779_10_prediction_nonclaim_missing", len(candidate) == 1 and candidate[0]["valid_for_claim"] is False and has_missing_marker(candidate[0]), "prediction row stays nonclaim and missing official numeric kernel"),
        ("VAL2779_11_bound_numeric", len(bounds) == 1 and is_numeric(bounds[0]["bound_value"]) and float(str(bounds[0]["bound_value"])) > 0.0 and bounds[0]["bound_valid_for_internal_runner"] is True, "bound import has positive numeric value"),
        ("VAL2779_12_runner_refuses", runner[0]["valid_prediction_rows"] == 0 and runner[0]["claim_allowed"] is False, "runner reports no valid prediction rows and claim false"),
        ("VAL2779_13_claim_gates_safe", all(row["claim_allowed"] is False for row in gates) and any(row["gate_id"] == "CG2779_2_dry_run_kernel" and row["gate_pass"] is True for row in gates), "all claim gates deny WEP/local-GR claim while acknowledging dry-run path"),
        ("VAL2779_14_next_target", any(row["row_id"] == "NEXT2779_0_2780" and "user-assisted-CMSM-export-or-nonclaim-surrogate" in row["next_target"] for row in next_rows), "next target avoids repeating blocked CMSM loop"),
        ("VAL2779_15_branch_outputs", all(row["exists"] and int(row["row_count"]) > 0 for row in branches), "branch copies exist and contain rows"),
        ("VAL2779_16_csv_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2779_17_no_claim_flags", no_claim_flags(rows_by_name), "no generated row is valid_for_claim=true/claim_allowed=true/pass_for_claim=true"),
        ("VAL2779_18_generated_under_post_checkpoint", generated_files_under_work(), "all generated outputs are under post-checkpoint-work"),
        ("VAL2779_19_formalization_untouched", formalization_untouched(), "formalization-workbench modified-file count remains zero during this run"),
        ("VAL2779_20_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for check_id, passed, detail in checks]
    rows.append({
        "validation_id": "VAL2779_OVERALL",
        "passed": all(row["passed"] for row in rows),
        "detail": "2779 stages CMSM/REGARDS route probes, candidate endpoints, reconstruction requirements, a segment-210 dry-run gx/gz/Sxx/Sxz kernel preview, and the stricter CMSM official-array import contract in the R2/f(R) branch. Official schema/arrays and numeric tau_WEP remain missing, so WEP/local-GR claims are blocked. Next route is user-supplied CMSM export or a clearly nonclaim surrogate orbit/gravity reconstruction, not another blind CMSM loop.",
        "timestamp_utc": ts(),
    })
    return rows


def build_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join([
        "# 2779 - Y5 R2/f(R): MICROSCOPE Data-Portal Schema Or Reconstructed gxS Kernel Under AX1090",
        "## Private Verdict\n\n2779 does not obtain official CMSM arrays, but it moves the live R2/f(R) branch forward: CMSM/REGARDS route probes are recorded, candidate endpoints are staged, the exact reconstruction blockers are explicit, segment 210 has a nonclaim gx/gz/Sxx/Sxz dry-run preview, and the stricter CMSM export/official-array contract is ready. The branch still cannot score WEP/local-GR because numeric tau_WEP is not acquired.",
        "## Source Register\n\n" + markdown_table(rows_by_name["sources"], ["row_id", "source_key", "source_path", "exists", "needle_found", "source_role", "valid_for_claim"]),
        "## External Source Ledger\n\n" + markdown_table(rows_by_name["external"], ["external_id", "source_url", "source_lines", "use_for_2779", "extracted_item", "port_status", "valid_for_claim"]),
        "## Portal Route Probe\n\n" + markdown_table(rows_by_name["portal"], ["url", "probe_status", "http_status", "content_type", "bytes_sampled", "schema_or_data_inventory_acquired", "error", "valid_for_claim"]),
        "## REGARDS Candidate Endpoints\n\n" + markdown_table(rows_by_name["endpoints"], ["endpoint_id", "candidate_url", "regards_basis", "expected_payload", "auth_or_access_risk", "schema_inventory_acquired", "valid_for_claim"]),
        "## Reconstruction Requirements\n\n" + markdown_table(rows_by_name["requirements"], ["requirement_id", "object", "why_needed", "current_status", "source_hint", "branch_status", "valid_for_claim"]),
        "## Dry-Run Kernel Metadata\n\n" + markdown_table(rows_by_name["dry_meta"], ["dry_run_id", "segment", "spin_mode", "duration_orbits", "sample_rate_hz", "torb_s", "full_grid_samples", "preview_rows_written", "forb_hz", "fspin_hz", "fep_hz", "phase_convention", "amplitude_convention", "kernel_status", "valid_for_claim"]),
        "## Dry-Run gxS Preview\n\n" + markdown_table(rows_by_name["dry_preview"][:8], ["preview_id", "sample_index", "t_sec_from_segment_start", "gx_unit", "gz_unit", "Sxx_unit", "Sxz_unit", "phase_convention", "valid_for_claim"]) + "\n\n_Only the first 8 of 32 preview rows are shown here; the full CSV is written separately._",
        "## CMSM Export Contract\n\n" + markdown_table(rows_by_name["export_contract"], ["contract_id", "required_artifact", "minimum_fields", "acceptance_rule", "current_status", "target_folder", "valid_for_claim"]),
        "## Official Array Schema Contract\n\n" + markdown_table(rows_by_name["array_contract"], ["column_id", "column_name", "units", "required", "source_status", "replaces_1072_dry_run_column", "branch_status", "valid_for_claim"]),
        "## Numeric Tau Status\n\n" + markdown_table(rows_by_name["tau"], ["status_id", "object", "status", "next_action", "claim_allowed", "valid_for_claim"]),
        "## Nonclaim Product Candidate\n\n" + markdown_table(rows_by_name["candidate"], ["prediction_id", "arena", "product_symbol", "product_value", "product_units", "derivation_status", "notes", "valid_for_claim"]),
        "## Bound Import\n\n" + markdown_table(rows_by_name["bounds"], ["bound_id", "arena", "product_symbol", "bound_value", "bound_units", "bound_type", "source_row_id", "bound_valid_for_internal_runner", "valid_for_claim"]),
        "## Product Runner Status\n\n" + markdown_table(rows_by_name["runner"], ["runner_id", "prediction_rows", "bound_rows", "valid_prediction_rows", "valid_bound_rows", "claim_allowed", "expected_result", "valid_for_claim"]),
        "## Product Comparison Rows\n\n" + markdown_table(rows_by_name["comparisons"], ["comparison_id", "comparison_status", "pass_for_claim", "issues", "valid_for_claim"]),
        "## Claim Gates\n\n" + markdown_table(rows_by_name["gates"], ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason", "valid_for_claim"]),
        "## Decision Ledger\n\n" + markdown_table(rows_by_name["decision"], ["decision_id", "decision", "evidence", "consequence", "valid_for_claim"]),
        "## Next Target\n\n" + markdown_table(rows_by_name["next"], ["row_id", "next_target", "script", "objective", "include", "exclude", "valid_for_claim"]),
        "## Branch Copies\n\n" + markdown_table(rows_by_name["branches"], ["copy_id", "table_key", "source_table", "copy_path", "purpose", "exists", "row_count", "valid_for_claim"]),
        "## Validation\n\n" + markdown_table(rows_by_name["validation"], ["validation_id", "passed", "detail", "timestamp_utc"]),
        "## Plain-English Read\n\nThis is not the punch, it is footwork: we now have the exact import contract and a working dummy projection shape. The next real advance is either a user/browser CMSM export that fills the contract, or a labelled surrogate orbit/gravity reconstruction that lets us test the maths without pretending it is official MICROSCOPE evidence.",
        "",
    ])


def main() -> None:
    ensure_dirs()
    sources = build_sources()
    external = build_external_rows()
    portal = build_portal_rows()
    endpoints = build_endpoint_rows()
    requirements = build_requirement_rows()
    dry_meta, dry_preview = build_dry_run_rows()
    export_contract = build_export_contract()
    array_contract = build_array_contract()
    tau = build_tau_rows()
    candidate = build_candidate_rows()
    bounds = build_bound_rows()
    runner, comparisons = run_product_runner(candidate, bounds)
    gates = build_gates()
    decision = build_decisions()
    next_rows = build_next()

    for key, rows in [
        ("sources", sources), ("external", external), ("portal", portal), ("endpoints", endpoints),
        ("requirements", requirements), ("dry_meta", dry_meta), ("dry_preview", dry_preview),
        ("export_contract", export_contract), ("array_contract", array_contract), ("tau", tau),
        ("candidate", candidate), ("bounds", bounds), ("runner", runner),
        ("comparisons", comparisons), ("gates", gates), ("decision", decision), ("next", next_rows),
    ]:
        write_csv(OUTPUTS[key], rows)

    branches = copy_branch_outputs(
        external, portal, endpoints, requirements, dry_meta, dry_preview,
        export_contract, array_contract, tau, candidate, gates, next_rows,
    )
    write_csv(OUTPUTS["branches"], branches)
    remove_pycache()

    rows_by_name = {
        "sources": sources,
        "external": external,
        "portal": portal,
        "endpoints": endpoints,
        "requirements": requirements,
        "dry_meta": dry_meta,
        "dry_preview": dry_preview,
        "export_contract": export_contract,
        "array_contract": array_contract,
        "tau": tau,
        "candidate": candidate,
        "bounds": bounds,
        "runner": runner,
        "comparisons": comparisons,
        "gates": gates,
        "decision": decision,
        "next": next_rows,
        "branches": branches,
    }
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    validation = build_validation(rows_by_name, csv_paths)
    rows_by_name["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(build_doc(rows_by_name), encoding="utf-8")
    remove_pycache()

    overall = next(row for row in validation if row["validation_id"] == "VAL2779_OVERALL")
    print(f"2779 complete: overall={overall['passed']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
