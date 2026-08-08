from __future__ import annotations

import csv
import math
import shutil
import urllib.request
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
DOC = ROOT / "1072-Y5-R10-MICROSCOPE-data-portal-schema-or-reconstructed-gxS-kernel.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1072-MICROSCOPE-data-portal-schema-or-gxS-kernel" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1072_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1072_WEP_BOUND_IMPORT.csv"

FORB_HZ = 0.16818e-3
FSPIN3_HZ = 2.94315e-3
FEP3_HZ = 3.11133e-3
TORB_S = 5946
SAMPLE_RATE_HZ = 4
SEGMENT_210_ORBITS = 50


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


def probe_url(url: str, timeout: int = 5) -> dict[str, str]:
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "MTS-private-audit/1072"})
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = response.read(1024)
            status = getattr(response, "status", 200)
            content_type = response.headers.get("content-type", "")
        return {
            "url": url,
            "probe_status": "HTTP_OK",
            "http_status": str(status),
            "content_type": content_type,
            "bytes_sampled": str(len(payload)),
            "error": "",
            "schema_or_data_inventory_acquired": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    except Exception as exc:
        return {
            "url": url,
            "probe_status": "BLOCKED_OR_UNREACHABLE_FROM_THIS_RUN",
            "http_status": "",
            "content_type": "",
            "bytes_sampled": "0",
            "error": type(exc).__name__ + ": " + str(exc),
            "schema_or_data_inventory_acquired": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1072_0_1071_next", "source-intake/mts_residuals/P8_Y5_R10_1071_NEXT_TARGET.csv", "1072-Y5-R10-MICROSCOPE-data-portal-schema-or-reconstructed-gxS-kernel.md", "1071 handoff."),
        ("SRC1072_1_1071_validation", "source-intake/mts_residuals/P8_Y5_BRR545_1071_VALIDATION.csv", "V1071_SUMMARY", "1071 validation summary."),
        ("SRC1072_2_1071_kernel", "source-intake/mts_residuals/P8_Y5_R10_1071_OFFICIAL_KERNEL_COMPONENTS.csv", "KER1071_1_fit_basis", "official kernel skeleton."),
        ("SRC1072_3_1071_segments", "source-intake/mts_residuals/P8_Y5_R10_1071_SUEP_SEGMENT_TABLE_SOURCE_BACKED.csv", "SUEP1071_210", "segment 210 source-backed row."),
        ("SRC1072_4_1071_portal", "source-intake/mts_residuals/P8_Y5_R10_1071_DATA_PORTAL_PROBE.csv", "cmsm-ds.onera.fr/user/microscope", "portal probe result."),
        ("SRC1072_5_1071_tau", "source-intake/mts_residuals/P8_Y5_R10_1071_TAU_PROJECTION_STATUS.csv", "TAU1071_3_verdict", "numeric tau still missing."),
        ("SRC1072_6_1071_product", "source-intake/mts_residuals/P8_Y5_R10_1071_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv", "PRED1071_0", "prior product refusal."),
        ("SRC1072_7_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge", "MICROSCOPE WEP bound row."),
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


def external_source_rows() -> list[dict[str, str]]:
    return [
        {
            "external_id": "EXT1072_0_OCA_data_inventory_pointer",
            "source_url": "https://www.oca.eu/fr/microscope",
            "source_lines": "OCA page lines 198-203",
            "extracted_item": "OCA says raw, calibrated, and auxiliary data for analyses are associated with the CMSM REGARDS portal and user support.",
            "use_for_1072": "schema/file inventory target",
            "source_backed": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "external_id": "EXT1072_1_ONERA_data_available",
            "source_url": "https://microscope.onera.fr/fr/publication/microscope-data-are-available",
            "source_lines": "ONERA public data page",
            "extracted_item": "ONERA points mission users to https://cmsm-ds.onera.fr/user/microscope for MICROSCOPE data.",
            "use_for_1072": "portal provenance",
            "source_backed": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "external_id": "EXT1072_2_REGARDS_search_download",
            "source_url": "https://regardsoss.github.io/",
            "source_lines": "REGARDS docs lines 48-64",
            "extracted_item": "REGARDS advertises OpenSearch/GeoJSON/STAC discovery and HTTP file serving.",
            "use_for_1072": "candidate schema/API route",
            "source_backed": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "external_id": "EXT1072_3_REGARDS_access_project",
            "source_url": "https://regardsoss.github.io/docs/development/services/access-project/overview",
            "source_lines": "REGARDS access-project docs lines 91-99",
            "extracted_item": "rs-access-project proxies rs-catalog and rs-storage for search/product access and quotas.",
            "use_for_1072": "candidate API host service",
            "source_backed": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "external_id": "EXT1072_4_REGARDS_api_endpoints",
            "source_url": "https://regardsoss.github.io/docs/development/services/access-project/api-swagger",
            "source_lines": "REGARDS API docs lines 111-116 and 1515-1523",
            "extracted_item": "access-project exposes catalogue search endpoints, including dataobjects/datasets search.",
            "use_for_1072": "candidate endpoint ledger",
            "source_backed": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "external_id": "EXT1072_5_CQG_data_product_requirements",
            "source_url": "https://elib.dlr.de/193667/2/Touboul_2022_Class._Quantum_Grav._39_204009.pdf",
            "source_lines": "CQG 2022 PDF lines 341-351",
            "extracted_item": "MICROSCOPE analysis used 4 Hz accelerometer measurements, same-stamp attitude/angular velocity/angular acceleration, and minute-sampled satellite position/velocity.",
            "use_for_1072": "numeric kernel product requirements",
            "source_backed": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "external_id": "EXT1072_6_CQG_fit_basis",
            "source_url": "https://elib.dlr.de/193667/2/Touboul_2022_Class._Quantum_Grav._39_204009.pdf",
            "source_lines": "CQG 2022 PDF lines 491-543",
            "extracted_item": "corrected X-axis model uses polynomial drift plus gx,gz,Sxx,Sxz columns.",
            "use_for_1072": "dry-run kernel basis",
            "source_backed": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def portal_route_rows() -> list[dict[str, str]]:
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


def candidate_endpoint_rows() -> list[dict[str, str]]:
    base = "https://cmsm-ds.onera.fr"
    return [
        {
            "endpoint_id": "API1072_0_user_module",
            "candidate_url": f"{base}/user/microscope/modules/7",
            "regards_basis": "OCA direct module link; JS REGARDS UI route",
            "expected_payload": "browser UI metadata and module configuration",
            "auth_or_access_risk": "may require reachable REGARDS frontend/session",
            "schema_inventory_acquired": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "endpoint_id": "API1072_1_dataset_search",
            "candidate_url": f"{base}/api/v1/rs-access-project/datasets/search",
            "regards_basis": "access-project catalogue dataset search endpoint",
            "expected_payload": "dataset catalogue entries",
            "auth_or_access_risk": "REGARDS_OAUTH2 or public tenant routing may be required",
            "schema_inventory_acquired": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "endpoint_id": "API1072_2_dataobject_search",
            "candidate_url": f"{base}/api/v1/rs-access-project/dataobjects/search",
            "regards_basis": "access-project product/dataobject search endpoint",
            "expected_payload": "dataobject/product catalogue entries",
            "auth_or_access_risk": "query parameters and auth may be required",
            "schema_inventory_acquired": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "endpoint_id": "API1072_3_joined_dataobject_dataset_search",
            "candidate_url": f"{base}/api/v1/rs-access-project/dataobjects/datasets/search",
            "regards_basis": "documented joined OpenSearch request returning datasets associated with dataobject criteria",
            "expected_payload": "dataset records matching dataobject criteria",
            "auth_or_access_risk": "allParams query object required; may require OAuth2",
            "schema_inventory_acquired": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "endpoint_id": "API1072_4_module_config",
            "candidate_url": f"{base}/api/v1/rs-access-project/applications/microscope/modules",
            "regards_basis": "documented UI module retrieval endpoint pattern",
            "expected_payload": "UI modules for application id microscope if public and correctly named",
            "auth_or_access_risk": "application id may differ; OAuth2 likely",
            "schema_inventory_acquired": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def reconstruction_requirement_rows() -> list[dict[str, str]]:
    return [
        {
            "requirement_id": "REQ1072_0_exact_time_grid",
            "object": "exact segment timestamps",
            "why_needed": "phase of gx,gz,Sxx,Sxz depends on actual timestamps and segment masks",
            "current_status": "MISSING_EXACT_TIMESTAMPS",
            "source_hint": "CMSM 4 Hz accelerometer products",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "requirement_id": "REQ1072_1_orbit_ephemeris",
            "object": "J2000 satellite position/velocity",
            "why_needed": "compute g(Osat) and gravity-gradient tensor T at satellite centre",
            "current_status": "MISSING_NUMERIC_EPHEMERIS",
            "source_hint": "CMSM minute-sampled orbit products",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "requirement_id": "REQ1072_2_attitude_angular_rates",
            "object": "attitude, angular velocity, angular acceleration",
            "why_needed": "rotate gravity into instrument frame and build inertia gradient In",
            "current_status": "MISSING_NUMERIC_ATTITUDE_RATES",
            "source_hint": "CMSM same-stamp attitude products",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "requirement_id": "REQ1072_3_gravity_model",
            "object": "official gravity model convention",
            "why_needed": "MICROSCOPE computes deterministic gx,gz,Sxx,Sxz accurately; MTS must not substitute a guessed spherical model for a claim",
            "current_status": "MISSING_OFFICIAL_GRAVITY_MODEL_OR_APPROVED_SURROGATE",
            "source_hint": "MICROSCOPE processing references and CMSM auxiliary data",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "requirement_id": "REQ1072_4_glitch_masks",
            "object": "removed-sample masks",
            "why_needed": "segment table gives removed percentages, not exact masked samples",
            "current_status": "MISSING_EXACT_MASKS",
            "source_hint": "CMSM data products or MICROSCOPE processing metadata",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "requirement_id": "REQ1072_5_material_parent_map",
            "object": "MTS material/source response tensor",
            "why_needed": "turn official MICROSCOPE design matrix into an MTS product rather than an external fit basis",
            "current_status": "MISSING_PARENT_MATERIAL_MAP",
            "source_hint": "MTS parent action/theorem route",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def dry_run_metadata_rows() -> list[dict[str, object]]:
    sample_count = SEGMENT_210_ORBITS * TORB_S * SAMPLE_RATE_HZ
    return [
        {
            "dry_run_id": "DRY1072_0_segment210_kernel_preview",
            "segment": "210",
            "spin_mode": "V3",
            "duration_orbits": SEGMENT_210_ORBITS,
            "sample_rate_hz": SAMPLE_RATE_HZ,
            "torb_s": TORB_S,
            "full_grid_samples": sample_count,
            "preview_rows_written": 32,
            "forb_hz": FORB_HZ,
            "fspin_hz": FSPIN3_HZ,
            "fep_hz": FEP3_HZ,
            "phase_convention": "dry_run_zero_phase_not_claim",
            "amplitude_convention": "dimensionless_unit_columns_not_physical_g_or_S",
            "kernel_status": "DRY_RUN_NUMERIC_PREVIEW_ONLY_NOT_TAU",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def dry_run_preview_rows() -> list[dict[str, object]]:
    total_samples = SEGMENT_210_ORBITS * TORB_S * SAMPLE_RATE_HZ
    step = max(total_samples // 31, 1)
    rows: list[dict[str, object]] = []
    for preview_index in range(32):
        sample_index = min(preview_index * step, total_samples - 1)
        t_sec = sample_index / SAMPLE_RATE_HZ
        phase = 2.0 * math.pi * FEP3_HZ * t_sec
        orbit_phase = 2.0 * math.pi * FORB_HZ * t_sec
        rows.append(
            {
                "preview_id": f"GXS1072_210_{preview_index:02d}",
                "segment": "210",
                "sample_index": sample_index,
                "t_sec_from_segment_start": round(t_sec, 6),
                "orbit_fraction_from_start": round(t_sec / TORB_S, 9),
                "orbital_phase_zeroed_rad": round(orbit_phase % (2.0 * math.pi), 12),
                "fep_phase_zeroed_rad": round(phase % (2.0 * math.pi), 12),
                "gx_unit": round(math.cos(phase), 12),
                "gz_unit": round(math.sin(phase), 12),
                "Sxx_unit": round(math.cos(2.0 * phase), 12),
                "Sxz_unit": round(math.sin(2.0 * phase), 12),
                "poly0": 1.0,
                "poly1_centered": round((t_sec / (SEGMENT_210_ORBITS * TORB_S)) - 0.5, 12),
                "source_basis": "CQG_eq7_shape_only",
                "phase_convention": "dry_run_zero_phase_not_claim",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def numeric_tau_status_rows() -> list[dict[str, str]]:
    return [
        {
            "status_id": "NTS1072_0_schema_inventory",
            "object": "CMSM schema/file inventory",
            "status": "NOT_ACQUIRED_FROM_LOCAL_PROBE",
            "evidence": "P8_Y5_R10_1072_PORTAL_ROUTE_PROBE.csv",
            "next_action": "use browser/manual session or find public API query parameters",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "status_id": "NTS1072_1_dry_run_preview",
            "object": "segment 210 gx/gz/Sxx/Sxz preview",
            "status": "DRY_RUN_NUMERIC_PREVIEW_ONLY",
            "evidence": "P8_Y5_R10_1072_GXS_DRY_RUN_KERNEL_PREVIEW_SEGMENT210.csv",
            "next_action": "replace zero-phase/unit-amplitude columns with official arrays",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "status_id": "NTS1072_2_tau_WEP",
            "object": "numeric tau_WEP",
            "status": "NOT_ACQUIRED",
            "evidence": "REQ1072_0_exact_time_grid; REQ1072_1_orbit_ephemeris; REQ1072_2_attitude_angular_rates",
            "next_action": "acquire CMSM products or reconstruct official arrays from sourced ephemeris/attitude/gravity-model inputs",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def product_prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1072_0_WEP_gxS_dry_run_kernel_nonclaim_product",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_OFFICIAL_NUMERIC_TAU_WEP_KERNEL_DRY_RUN_ONLY",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1072_GXS_DRY_RUN_KERNEL_PREVIEW_SEGMENT210.csv",
            "inputs_present": "official_kernel_shape;segment210_window;dry_run_zero_phase_unit_columns",
            "required_inputs": "official gx/gz/Sxx/Sxz arrays; exact masks/timestamps; material tensor; Xhat normalization; direct parent product or tau_WEP map",
            "derivation_status": "DRY_RUN_NUMERIC_PREVIEW_ONLY_NOT_CLAIM",
            "valid_for_claim": "false",
            "notes": "numeric preview proves code path only; it is not a MICROSCOPE-derived tau_WEP value",
        }
    ]


def bound_rows() -> list[dict[str, str]]:
    row = local_bound_row("R1_WEP_source_charge")
    url, doi = split_reference(row["reference_path_or_url"])
    return [
        {
            "bound_id": "BOUND1072_0_MICROSCOPE_R1_eta_source_charge",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": row["upper_bound"],
            "bound_units": row["units"],
            "bound_source": url,
            "source_row": f"source-intake/local_bounds/local_bound_claims.csv::{row['row_id']}; doi:{doi}",
            "bound_type": "source_backed_upper_bound_anchor",
            "valid_for_claim": "true",
            "notes": "valid bound anchor only; dry-run kernel is not a scoreable MTS product",
        }
    ]


def product_status_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1072_0_WEP_gxS_dry_run_product_stub",
            "prediction_rows": str(status.get("prediction_rows", "")),
            "bound_rows": str(status.get("bound_rows", "")),
            "valid_prediction_rows": str(status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(status.get("valid_bound_rows", "")),
            "comparison_rows": str(status.get("comparison_rows", "")),
            "passed_rows": str(status.get("passed_rows", "")),
            "claim_allowed": str(status.get("claim_allowed", "")).lower(),
            "expected_result": "reject dry-run/placeholder prediction and keep claim false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1072_0_portal_schema",
            "claim_component": "CMSM data schema/file inventory",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "portal route known but schema/product inventory not acquired by local probe",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1072_1_dry_run_kernel",
            "claim_component": "gx/gz/Sxx/Sxz dry-run numeric preview",
            "gate_pass": "true",
            "claim_allowed": "false",
            "reason": "code path exists, but phase/amplitude/timestamps/masks are dry-run placeholders",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1072_2_official_numeric_kernel",
            "claim_component": "official numeric kernel arrays",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "MISSING_OFFICIAL_GX_GZ_SXX_SXZ_ARRAYS",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1072_3_tau_WEP_numeric",
            "claim_component": "numeric tau_WEP or direct parent product",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "MISSING_OFFICIAL_NUMERIC_TAU_WEP_KERNEL_DRY_RUN_ONLY",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1072_4_product_runner",
            "claim_component": "WEP product runner",
            "gate_pass": "false",
            "claim_allowed": str(product_status.get("claim_allowed", "")).lower(),
            "reason": f"valid_prediction_rows={product_status.get('valid_prediction_rows')}",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1072_0_portal_route_not_enough",
            "decision": "CMSM/REGARDS route is source-backed but not locally inventory-readable yet",
            "evidence": "P8_Y5_R10_1072_PORTAL_ROUTE_PROBE.csv; P8_Y5_R10_1072_CMSM_REGARDS_API_CANDIDATE_ENDPOINTS.csv",
            "consequence": "need browser/manual session or exact public API parameters",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1072_1_dry_run_kernel_path",
            "decision": "segment 210 dry-run kernel preview establishes the reconstruction code path",
            "evidence": "DRY1072_0_segment210_kernel_preview",
            "consequence": "future run can replace unit zero-phase columns with official arrays",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1072_2_no_claim",
            "decision": "do not score WEP/local-GR claim",
            "evidence": "NTS1072_2_tau_WEP; APR1072_0_WEP_gxS_dry_run_product_stub",
            "consequence": "numeric tau_WEP remains the barrier",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1072_0_1073",
            "next_target": "1073-Y5-R10-CMSM-browser-assisted-schema-or-one-segment-official-array-extract.md",
            "objective": "use a browser/manual CMSM session or a discovered public REGARDS query to obtain the actual MICROSCOPE file/schema inventory, then replace the segment-210 dry-run gx/gz/Sxx/Sxz preview with official or source-reconstructed arrays for one pilot segment.",
            "include": "CMSM UI screenshots or API response; dataset/file names; schema columns; one segment exact timestamps/masks; official gx/gz/Sxx/Sxz array extraction; runner refusal gates",
            "exclude": "public WEP/local-GR claim; zero-phase dry-run as evidence; guessed masks; guessed amplitudes; tau=1; GitHub; formalization edits",
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
    external_rows: list[dict[str, str]],
    portal_rows: list[dict[str, str]],
    endpoint_rows: list[dict[str, str]],
    requirement_rows: list[dict[str, str]],
    dry_meta_rows: list[dict[str, object]],
    preview_rows: list[dict[str, object]],
    tau_rows: list[dict[str, str]],
    prediction_rows: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    external_ids = {row["external_id"] for row in external_rows}
    endpoint_ids = {row["endpoint_id"] for row in endpoint_rows}
    requirement_statuses = {row["current_status"] for row in requirement_rows}
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V1072_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in source_rows), "all cited local source paths and needles are present"))
    checks.append(("V1072_1_external_sources_recorded", {"EXT1072_0_OCA_data_inventory_pointer", "EXT1072_2_REGARDS_search_download", "EXT1072_5_CQG_data_product_requirements", "EXT1072_6_CQG_fit_basis"}.issubset(external_ids), "OCA/REGARDS/CQG source rows recorded"))
    checks.append(("V1072_2_portal_probes_recorded", len(portal_rows) >= 6 and any("cmsm-ds.onera.fr/user/microscope/modules/7" in row["url"] for row in portal_rows), "CMSM portal and API route probes recorded"))
    checks.append(("V1072_3_endpoint_candidates", {"API1072_1_dataset_search", "API1072_2_dataobject_search", "API1072_3_joined_dataobject_dataset_search"}.issubset(endpoint_ids), "REGARDS candidate API endpoints staged"))
    checks.append(("V1072_4_requirements_block_claim", "MISSING_EXACT_TIMESTAMPS" in requirement_statuses and "MISSING_NUMERIC_EPHEMERIS" in requirement_statuses and "MISSING_NUMERIC_ATTITUDE_RATES" in requirement_statuses, "core numeric reconstruction requirements remain explicit"))
    checks.append(("V1072_5_dry_run_metadata", bool(dry_meta_rows) and int(dry_meta_rows[0]["full_grid_samples"]) == SEGMENT_210_ORBITS * TORB_S * SAMPLE_RATE_HZ and dry_meta_rows[0]["kernel_status"] == "DRY_RUN_NUMERIC_PREVIEW_ONLY_NOT_TAU", "dry-run metadata has expected segment 210 sample count and nonclaim status"))
    checks.append(("V1072_6_preview_rows", len(preview_rows) == 32 and all(row["valid_for_claim"] == "false" for row in preview_rows), "32 nonclaim preview rows written"))
    checks.append(("V1072_7_tau_not_acquired", any(row["status_id"] == "NTS1072_2_tau_WEP" and row["status"] == "NOT_ACQUIRED" for row in tau_rows), "numeric tau_WEP remains not acquired"))
    checks.append(("V1072_8_prediction_nonclaim_missing", any("MISSING_OFFICIAL_NUMERIC_TAU_WEP_KERNEL" in row["product_value"] and row["valid_for_claim"] == "false" for row in prediction_rows), "prediction row remains nonclaim and missing official numeric kernel"))
    checks.append(("V1072_9_bound_numeric", bool(bound_rows_) and float(bound_rows_[0]["bound_value"]) > 0 and bound_rows_[0]["valid_for_claim"] == "true", "bound import is positive numeric"))
    checks.append(("V1072_10_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "runner reports no valid prediction rows and claim false"))
    checks.append(("V1072_11_claim_gates_safe", all(row["claim_allowed"] == "false" for row in claim_rows), "all claim gates deny WEP/local-GR claim"))
    checks.append(("V1072_12_next_target", any("1073-Y5-R10-CMSM-browser-assisted-schema-or-one-segment-official-array-extract.md" in row["next_target"] for row in next_rows), "1073 handoff written"))
    generated_paths = list(outputs.values()) + [DOC]
    checks.append(("V1072_13_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    checks.append(("V1072_14_csv_parse", all(path.exists() and csv_rows_parse(path) for path in outputs.values() if path.suffix == ".csv" and path.name != "P8_Y5_BRR545_1072_VALIDATION.csv"), "all 1072 CSV outputs parse cleanly"))
    checks.append(("V1072_15_formalization_untouched", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains zero"))
    checks.append(("V1072_SUMMARY", True, "portal/API route staged and dry-run gxS kernel preview built; official numeric tau/product claim blocked"))
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
    external_rows: list[dict[str, str]],
    portal_rows: list[dict[str, str]],
    endpoint_rows: list[dict[str, str]],
    requirement_rows: list[dict[str, str]],
    dry_meta_rows: list[dict[str, object]],
    preview_rows: list[dict[str, object]],
    tau_rows: list[dict[str, str]],
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
            "# 1072 - MICROSCOPE data portal schema or reconstructed gxS kernel",
            "",
            "## Current verdict",
            "1072 does not yet obtain the official CMSM schema or arrays. It does, however, stage the REGARDS/CMSM route, preserve the exact missing requirements, and build a segment-210 `gx/gz/Sxx/Sxz` dry-run preview that exercises the reconstruction path without claiming it is a physical tau_WEP kernel.",
            "",
            "## Local source register",
            md_table(source_rows, ["source_id", "relative_path", "exists", "needle_found", "note"]),
            "## External source ledger",
            md_table(external_rows, ["external_id", "source_url", "source_lines", "use_for_1072", "extracted_item"]),
            "## Portal route probe",
            md_table(portal_rows, ["url", "probe_status", "http_status", "content_type", "bytes_sampled", "schema_or_data_inventory_acquired", "error"]),
            "## REGARDS candidate endpoints",
            md_table(endpoint_rows, ["endpoint_id", "candidate_url", "regards_basis", "expected_payload", "auth_or_access_risk", "schema_inventory_acquired"]),
            "## Reconstruction requirements",
            md_table(requirement_rows, ["requirement_id", "object", "why_needed", "current_status", "source_hint"]),
            "## Dry-run kernel metadata",
            md_table(dry_meta_rows, ["dry_run_id", "segment", "spin_mode", "full_grid_samples", "preview_rows_written", "phase_convention", "kernel_status"]),
            "## Dry-run gxS preview",
            md_table(preview_rows[:8], ["preview_id", "sample_index", "t_sec_from_segment_start", "gx_unit", "gz_unit", "Sxx_unit", "Sxz_unit", "phase_convention"]),
            "## Numeric tau status",
            md_table(tau_rows, ["status_id", "object", "status", "next_action", "claim_allowed"]),
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
    external_rows = external_source_rows()
    portal_rows = portal_route_rows()
    endpoint_rows = candidate_endpoint_rows()
    requirement_rows = reconstruction_requirement_rows()
    dry_meta_rows = dry_run_metadata_rows()
    preview_rows = dry_run_preview_rows()
    tau_rows = numeric_tau_status_rows()
    prediction_rows = product_prediction_rows()
    bound_rows_ = bound_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R10_1072_SOURCE_REGISTER.csv",
        "external_ledger": OUT / "P8_Y5_R10_1072_EXTERNAL_SOURCE_LEDGER.csv",
        "portal_probe": OUT / "P8_Y5_R10_1072_PORTAL_ROUTE_PROBE.csv",
        "endpoint_candidates": OUT / "P8_Y5_R10_1072_CMSM_REGARDS_API_CANDIDATE_ENDPOINTS.csv",
        "requirements": OUT / "P8_Y5_R10_1072_RECONSTRUCTION_REQUIREMENTS.csv",
        "dry_meta": OUT / "P8_Y5_R10_1072_GXS_DRY_RUN_METADATA_SEGMENT210.csv",
        "preview": OUT / "P8_Y5_R10_1072_GXS_DRY_RUN_KERNEL_PREVIEW_SEGMENT210.csv",
        "tau_status": OUT / "P8_Y5_R10_1072_NUMERIC_TAU_STATUS.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1072_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1072_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1072_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1072_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1072_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1072_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["external_ledger"], external_rows)
    write_csv(outputs["portal_probe"], portal_rows)
    write_csv(outputs["endpoint_candidates"], endpoint_rows)
    write_csv(outputs["requirements"], requirement_rows)
    write_csv(outputs["dry_meta"], dry_meta_rows)
    write_csv(outputs["preview"], preview_rows)
    write_csv(outputs["tau_status"], tau_rows)
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
        external_rows,
        portal_rows,
        endpoint_rows,
        requirement_rows,
        dry_meta_rows,
        preview_rows,
        tau_rows,
        prediction_rows,
        bound_rows_,
        product_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        external_rows,
        portal_rows,
        endpoint_rows,
        requirement_rows,
        dry_meta_rows,
        preview_rows,
        tau_rows,
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
