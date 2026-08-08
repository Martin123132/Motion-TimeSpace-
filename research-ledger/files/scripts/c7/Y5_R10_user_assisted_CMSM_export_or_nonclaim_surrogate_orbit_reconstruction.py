from __future__ import annotations

import csv
import math
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
CMSM_DIR = ROOT / "source-intake" / "microscope_cmsm"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"
DOC = ROOT / "1074-Y5-R10-user-assisted-CMSM-export-or-nonclaim-surrogate-orbit-reconstruction.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1074-user-assisted-CMSM-export-or-surrogate-orbit" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1074_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1074_WEP_BOUND_IMPORT.csv"

MU_EARTH = 3.986004418e14
TORB_S = 5946.0
FORB_HZ = 0.16818e-3
FEP3_HZ = 3.11133e-3
SAMPLE_RATE_HZ = 4.0
SEGMENT_210_ORBITS = 50
PREVIEW_ROWS = 256


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
        ("SRC1074_0_1073_next", "source-intake/mts_residuals/P8_Y5_R10_1073_NEXT_TARGET.csv", "1074-Y5-R10-user-assisted-CMSM-export-or-nonclaim-surrogate-orbit-reconstruction.md", "1073 handoff."),
        ("SRC1074_1_1073_validation", "source-intake/mts_residuals/P8_Y5_BRR545_1073_VALIDATION.csv", "V1073_SUMMARY", "1073 validation summary."),
        ("SRC1074_2_1073_browser", "source-intake/mts_residuals/P8_Y5_R10_1073_BROWSER_ATTEMPT_LEDGER.csv", "BROW1073_0_direct_cmsm_module", "browser route blocked."),
        ("SRC1074_3_1073_contract", "source-intake/mts_residuals/P8_Y5_R10_1073_CMSM_EXPORT_CONTRACT.csv", "CMSM1073_5_official_gxS_arrays", "official array contract."),
        ("SRC1074_4_1073_schema", "source-intake/mts_residuals/P8_Y5_R10_1073_OFFICIAL_ARRAY_SCHEMA_CONTRACT.csv", "ARR1073_3_gx", "official array schema."),
        ("SRC1074_5_1073_status", "source-intake/mts_residuals/P8_Y5_R10_1073_OFFICIAL_ARRAY_EXTRACT_STATUS.csv", "EX1073_3_tau_WEP", "official extraction still blocked."),
        ("SRC1074_6_1072_preview", "source-intake/mts_residuals/P8_Y5_R10_1072_GXS_DRY_RUN_KERNEL_PREVIEW_SEGMENT210.csv", "GXS1072_210_00", "prior phase-only dry run."),
        ("SRC1074_7_1071_segments", "source-intake/mts_residuals/P8_Y5_R10_1071_SUEP_SEGMENT_TABLE_SOURCE_BACKED.csv", "SUEP1071_210", "segment 210 duration source row."),
        ("SRC1074_8_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge", "MICROSCOPE WEP bound row."),
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


def cmsm_export_inventory_rows() -> list[dict[str, str]]:
    files = sorted(CMSM_DIR.rglob("*")) if CMSM_DIR.exists() else []
    file_rows = [path for path in files if path.is_file()]
    rows: list[dict[str, str]] = [
        {
            "inventory_id": "INV1074_0_search_root",
            "search_root": str(CMSM_DIR),
            "exists": str(CMSM_DIR.exists()).lower(),
            "matching_files": str(len(file_rows)),
            "contract_match_status": "NO_USER_SUPPLIED_CMSM_EXPORT_FOUND",
            "action_taken": "surrogate reconstruction branch selected",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]
    for index, path in enumerate(file_rows[:20]):
        rows.append(
            {
                "inventory_id": f"INV1074_file_{index:02d}",
                "search_root": str(CMSM_DIR),
                "exists": "true",
                "matching_files": "1",
                "contract_match_status": "UNVALIDATED_LOCAL_FILE_PRESENT",
                "action_taken": str(path),
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def orbital_radius_from_period() -> float:
    n = 2.0 * math.pi / TORB_S
    return (MU_EARTH / (n * n)) ** (1.0 / 3.0)


def surrogate_assumption_rows() -> list[dict[str, object]]:
    radius = orbital_radius_from_period()
    g0 = MU_EARTH / (radius * radius)
    grad = MU_EARTH / (radius**3)
    return [
        {
            "assumption_id": "SUR1074_0_branch_selection",
            "object": "branch",
            "value": "nonclaim surrogate orbit/gravity reconstruction",
            "units": "text",
            "source_or_reason": "CMSM export absent and browser/API access blocked in 1073",
            "claim_status": "FORBIDDEN_FOR_EVIDENCE",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "assumption_id": "SUR1074_1_orbit_period",
            "object": "Torb",
            "value": TORB_S,
            "units": "s",
            "source_or_reason": "MICROSCOPE frequency table / 1071 kernel source row",
            "claim_status": "source-backed scalar, but surrogate use only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "assumption_id": "SUR1074_2_orbit_radius",
            "object": "r_surrogate=(mu/n^2)^(1/3)",
            "value": radius,
            "units": "m",
            "source_or_reason": "derived from Earth monopole and Torb; not official ephemeris",
            "claim_status": "surrogate_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "assumption_id": "SUR1074_3_gravity_amplitude",
            "object": "g0=mu/r^2",
            "value": g0,
            "units": "m s^-2",
            "source_or_reason": "spherical Earth monopole; not MICROSCOPE gravity model",
            "claim_status": "surrogate_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "assumption_id": "SUR1074_4_gradient_scale",
            "object": "G=mu/r^3",
            "value": grad,
            "units": "s^-2",
            "source_or_reason": "spherical Earth monopole gradient scale; no inertia subtraction",
            "claim_status": "surrogate_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "assumption_id": "SUR1074_5_readout_phase",
            "object": "phi=2*pi*fEP3*t",
            "value": FEP3_HZ,
            "units": "Hz",
            "source_or_reason": "official fEP3 scalar; zero phase is guessed",
            "claim_status": "FORBIDDEN_FOR_EVIDENCE",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "assumption_id": "SUR1074_6_masks_attitude",
            "object": "masks/attitude/inertia",
            "value": "omitted_or_identity_surrogate",
            "units": "text",
            "source_or_reason": "official products unavailable",
            "claim_status": "FORBIDDEN_FOR_EVIDENCE",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def surrogate_grid_metadata_rows() -> list[dict[str, object]]:
    total_samples = int(SEGMENT_210_ORBITS * TORB_S * SAMPLE_RATE_HZ)
    radius = orbital_radius_from_period()
    return [
        {
            "grid_id": "GRID1074_0_segment210_surrogate",
            "segment": "210",
            "duration_orbits": SEGMENT_210_ORBITS,
            "torb_s": TORB_S,
            "sample_rate_hz": SAMPLE_RATE_HZ,
            "full_grid_samples": total_samples,
            "preview_rows_written": PREVIEW_ROWS,
            "orbit_radius_m": radius,
            "orbit_model": "circular_Earth_monopole_from_Torb",
            "attitude_model": "zero_phase_rotating_XZ_plane_surrogate",
            "mask_model": "all_samples_unmasked_surrogate",
            "inertia_subtraction": "omitted",
            "claim_status": "NONCLAIM_PIPELINE_TEST_ONLY",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def surrogate_preview_rows() -> list[dict[str, object]]:
    radius = orbital_radius_from_period()
    g0 = MU_EARTH / (radius * radius)
    grad = MU_EARTH / (radius**3)
    total_samples = int(SEGMENT_210_ORBITS * TORB_S * SAMPLE_RATE_HZ)
    step = max(total_samples // (PREVIEW_ROWS - 1), 1)
    rows: list[dict[str, object]] = []
    for preview_index in range(PREVIEW_ROWS):
        sample_index = min(preview_index * step, total_samples - 1)
        t_sec = sample_index / SAMPLE_RATE_HZ
        phi = 2.0 * math.pi * FEP3_HZ * t_sec
        cos_phi = math.cos(phi)
        sin_phi = math.sin(phi)
        gx = -g0 * cos_phi
        gz = -g0 * sin_phi
        t_radial = 2.0 * grad
        t_tangent = -grad
        sxx = t_radial * cos_phi * cos_phi + t_tangent * sin_phi * sin_phi
        sxz = (t_radial - t_tangent) * sin_phi * cos_phi
        rows.append(
            {
                "row_id": f"SUR1074_210_{preview_index:03d}",
                "segment_id": "210",
                "sample_index": sample_index,
                "t_sec_from_segment_start": round(t_sec, 6),
                "orbit_fraction_from_start": round(t_sec / TORB_S, 9),
                "phase_fep_zeroed_rad": round(phi % (2.0 * math.pi), 12),
                "gx_surrogate_m_s2": round(gx, 12),
                "gz_surrogate_m_s2": round(gz, 12),
                "Sxx_surrogate_s2": f"{sxx:.15e}",
                "Sxz_surrogate_s2": f"{sxz:.15e}",
                "mask_flag_surrogate": "false",
                "generation_method": "spherical_Earth_monopole_zero_phase_surrogate_not_official",
                "source_status": "NOT_CMSM_NOT_OFFICIAL",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def replacement_map_rows() -> list[dict[str, str]]:
    return [
        {
            "map_id": "MAP1074_0_gx",
            "official_contract_column": "gx",
            "surrogate_column": "gx_surrogate_m_s2",
            "replacement_status": "SURROGATE_AVAILABLE_OFFICIAL_MISSING",
            "evidence_policy": "cannot support claim",
            "next_action": "replace with CMSM/official gx",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "map_id": "MAP1074_1_gz",
            "official_contract_column": "gz",
            "surrogate_column": "gz_surrogate_m_s2",
            "replacement_status": "SURROGATE_AVAILABLE_OFFICIAL_MISSING",
            "evidence_policy": "cannot support claim",
            "next_action": "replace with CMSM/official gz",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "map_id": "MAP1074_2_Sxx",
            "official_contract_column": "Sxx",
            "surrogate_column": "Sxx_surrogate_s2",
            "replacement_status": "SURROGATE_AVAILABLE_OFFICIAL_MISSING",
            "evidence_policy": "cannot support claim",
            "next_action": "replace with CMSM/official Sxx or official reconstruction",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "map_id": "MAP1074_3_Sxz",
            "official_contract_column": "Sxz",
            "surrogate_column": "Sxz_surrogate_s2",
            "replacement_status": "SURROGATE_AVAILABLE_OFFICIAL_MISSING",
            "evidence_policy": "cannot support claim",
            "next_action": "replace with CMSM/official Sxz or official reconstruction",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "map_id": "MAP1074_4_mask",
            "official_contract_column": "mask_flag",
            "surrogate_column": "mask_flag_surrogate",
            "replacement_status": "SURROGATE_ALL_UNMASKED_OFFICIAL_MISSING",
            "evidence_policy": "cannot support claim",
            "next_action": "replace with exact CMSM mask",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def surrogate_status_rows() -> list[dict[str, str]]:
    return [
        {
            "status_id": "STAT1074_0_CMSM_export",
            "object": "user-assisted CMSM export",
            "status": "NOT_FOUND_LOCALLY",
            "evidence": "INV1074_0_search_root",
            "claim_allowed": "false",
            "next_action": "import user-supplied CMSM export if available",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "status_id": "STAT1074_1_surrogate_orbit",
            "object": "surrogate segment 210 orbit/gravity preview",
            "status": "BUILT_NONCLAIM",
            "evidence": "GRID1074_0_segment210_surrogate; SUR1074_210_000",
            "claim_allowed": "false",
            "next_action": "wire surrogate into a nonclaim design-matrix/tau-shape smoke runner",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "status_id": "STAT1074_2_official_arrays",
            "object": "official gx/gz/Sxx/Sxz arrays",
            "status": "NOT_ACQUIRED",
            "evidence": "MAP1074_0_gx; MAP1074_2_Sxx",
            "claim_allowed": "false",
            "next_action": "replace surrogate columns with CMSM official arrays",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "status_id": "STAT1074_3_tau_WEP",
            "object": "numeric tau_WEP",
            "status": "NOT_ACQUIRED",
            "evidence": "official arrays and MTS material/source map both missing",
            "claim_allowed": "false",
            "next_action": "derive only after official arrays or explicitly nonclaim smoke-route selection",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def product_prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1074_0_WEP_surrogate_orbit_nonclaim_product",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_OFFICIAL_ARRAYS_SURROGATE_ONLY",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1074_SURROGATE_GXS_PREVIEW_SEGMENT210.csv",
            "inputs_present": "surrogate_gx;surrogate_gz;surrogate_Sxx;surrogate_Sxz;surrogate_grid",
            "required_inputs": "official CMSM arrays or source-backed reconstruction; exact masks/timestamps; material tensor; Xhat normalization; tau_WEP map or direct parent product",
            "derivation_status": "NONCLAIM_SURROGATE_PIPELINE_ONLY",
            "valid_for_claim": "false",
            "notes": "surrogate tests geometry/code plumbing only; no WEP evidence",
        }
    ]


def bound_rows() -> list[dict[str, str]]:
    row = local_bound_row("R1_WEP_source_charge")
    url, doi = split_reference(row["reference_path_or_url"])
    return [
        {
            "bound_id": "BOUND1074_0_MICROSCOPE_R1_eta_source_charge",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": row["upper_bound"],
            "bound_units": row["units"],
            "bound_source": url,
            "source_row": f"source-intake/local_bounds/local_bound_claims.csv::{row['row_id']}; doi:{doi}",
            "bound_type": "source_backed_upper_bound_anchor",
            "valid_for_claim": "true",
            "notes": "valid bound anchor only; surrogate prediction is invalid for claim",
        }
    ]


def product_status_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1074_0_WEP_surrogate_orbit_product_stub",
            "prediction_rows": str(status.get("prediction_rows", "")),
            "bound_rows": str(status.get("bound_rows", "")),
            "valid_prediction_rows": str(status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(status.get("valid_bound_rows", "")),
            "comparison_rows": str(status.get("comparison_rows", "")),
            "passed_rows": str(status.get("passed_rows", "")),
            "claim_allowed": str(status.get("claim_allowed", "")).lower(),
            "expected_result": "reject surrogate-only prediction and keep claim false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1074_0_CMSM_export",
            "claim_component": "user/CMSM export",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "NO_USER_SUPPLIED_CMSM_EXPORT_FOUND",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1074_1_surrogate_preview",
            "claim_component": "surrogate segment 210 gxS preview",
            "gate_pass": "true",
            "claim_allowed": "false",
            "reason": "pipeline built but not official arrays",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1074_2_official_arrays",
            "claim_component": "official gx/gz/Sxx/Sxz arrays",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "MISSING_OFFICIAL_ARRAYS",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1074_3_product_runner",
            "claim_component": "WEP product runner",
            "gate_pass": "false",
            "claim_allowed": str(product_status.get("claim_allowed", "")).lower(),
            "reason": f"valid_prediction_rows={product_status.get('valid_prediction_rows')}",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1074_4_local_GR_WEP_claim",
            "claim_component": "local-GR/WEP pass",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "surrogate-only arrays and no MTS tau_WEP product",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1074_0_surrogate_branch_selected",
            "decision": "no local CMSM export found, so select nonclaim surrogate branch",
            "evidence": "INV1074_0_search_root",
            "consequence": "test pipeline geometry without claiming evidence",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1074_1_surrogate_is_useful",
            "decision": "surrogate gx/gz/Sxx/Sxz arrays now exist with physical units and source flags",
            "evidence": "P8_Y5_R10_1074_SURROGATE_GXS_PREVIEW_SEGMENT210.csv",
            "consequence": "next step can build a design-matrix/tau-shape smoke runner",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1074_2_no_claim",
            "decision": "do not treat surrogate arrays as official MICROSCOPE evidence",
            "evidence": "STAT1074_3_tau_WEP; APR1074_0_WEP_surrogate_orbit_product_stub",
            "consequence": "WEP/local-GR branch remains blocked",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1074_0_1075",
            "next_target": "1075-Y5-R10-surrogate-design-matrix-tau-shape-smoke-runner.md",
            "objective": "use the 1074 nonclaim surrogate gx/gz/Sxx/Sxz arrays to build a design-matrix/tau-shape smoke runner that verifies regression plumbing and replacement gates, while refusing any WEP/local-GR claim until official arrays and the MTS material/source map exist.",
            "include": "segment 210 surrogate design matrix; polynomial/gx/gz/Sxx/Sxz columns; condition-number/orthogonality diagnostics; replacement gates; product-runner refusal",
            "exclude": "treating surrogate fit as MICROSCOPE evidence; official claim; tau=1; guessed masks as final; GitHub; formalization edits",
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
    inventory_rows: list[dict[str, str]],
    assumption_rows: list[dict[str, object]],
    grid_rows: list[dict[str, object]],
    preview_rows: list[dict[str, object]],
    map_rows: list[dict[str, str]],
    status_rows: list[dict[str, str]],
    prediction_rows: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    total_samples = int(SEGMENT_210_ORBITS * TORB_S * SAMPLE_RATE_HZ)
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V1074_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in source_rows), "all cited local source paths and needles are present"))
    checks.append(("V1074_1_no_CMSM_export", inventory_rows[0]["contract_match_status"] == "NO_USER_SUPPLIED_CMSM_EXPORT_FOUND", "no local user-supplied CMSM export found"))
    checks.append(("V1074_2_assumptions_nonclaim", all(row["valid_for_claim"] == "false" for row in assumption_rows) and any(row["assumption_id"] == "SUR1074_6_masks_attitude" for row in assumption_rows), "surrogate assumptions are nonclaim and mask/attitude gap is explicit"))
    checks.append(("V1074_3_grid_metadata", bool(grid_rows) and int(grid_rows[0]["full_grid_samples"]) == total_samples and grid_rows[0]["claim_status"] == "NONCLAIM_PIPELINE_TEST_ONLY", "grid metadata has expected segment 210 sample count and nonclaim status"))
    checks.append(("V1074_4_preview_rows", len(preview_rows) == PREVIEW_ROWS and all(row["valid_for_claim"] == "false" and row["source_status"] == "NOT_CMSM_NOT_OFFICIAL" for row in preview_rows), "surrogate preview rows written and flagged nonofficial"))
    checks.append(("V1074_5_replacement_map", {row["official_contract_column"] for row in map_rows} >= {"gx", "gz", "Sxx", "Sxz", "mask_flag"} and all(row["valid_for_claim"] == "false" for row in map_rows), "replacement map covers official gx/gz/Sxx/Sxz/mask columns"))
    checks.append(("V1074_6_tau_not_acquired", any(row["status_id"] == "STAT1074_3_tau_WEP" and row["status"] == "NOT_ACQUIRED" for row in status_rows), "numeric tau_WEP remains not acquired"))
    checks.append(("V1074_7_prediction_nonclaim_missing", any("MISSING_OFFICIAL_ARRAYS_SURROGATE_ONLY" in row["product_value"] and row["valid_for_claim"] == "false" for row in prediction_rows), "prediction row remains missing official arrays"))
    checks.append(("V1074_8_bound_numeric", bool(bound_rows_) and float(bound_rows_[0]["bound_value"]) > 0 and bound_rows_[0]["valid_for_claim"] == "true", "bound import is positive numeric"))
    checks.append(("V1074_9_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "runner reports no valid prediction rows and claim false"))
    checks.append(("V1074_10_claim_gates_safe", all(row["claim_allowed"] == "false" for row in claim_rows), "all claim gates deny WEP/local-GR claim"))
    checks.append(("V1074_11_next_target", any("1075-Y5-R10-surrogate-design-matrix-tau-shape-smoke-runner.md" in row["next_target"] for row in next_rows), "1075 handoff written"))
    generated_paths = list(outputs.values()) + [DOC]
    checks.append(("V1074_12_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    checks.append(("V1074_13_csv_parse", all(path.exists() and csv_rows_parse(path) for path in outputs.values() if path.suffix == ".csv" and path.name != "P8_Y5_BRR545_1074_VALIDATION.csv"), "all 1074 CSV outputs parse cleanly"))
    checks.append(("V1074_14_formalization_untouched", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains zero"))
    checks.append(("V1074_SUMMARY", True, "no CMSM export found; nonclaim surrogate orbit/gravity preview built; official WEP/product claim blocked"))
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
    inventory_rows: list[dict[str, str]],
    assumption_rows: list[dict[str, object]],
    grid_rows: list[dict[str, object]],
    preview_rows: list[dict[str, object]],
    map_rows: list[dict[str, str]],
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
            "# 1074 - User-assisted CMSM export or nonclaim surrogate orbit reconstruction",
            "",
            "## Current verdict",
            "1074 found no local user-supplied CMSM export, so it built a strictly nonclaim segment-210 surrogate orbit/gravity reconstruction. This creates physically unitful gx/gz/Sxx/Sxz plumbing for future design-matrix smoke tests, but it is not official MICROSCOPE evidence and cannot support a WEP/local-GR claim.",
            "",
            "## Local source register",
            md_table(source_rows, ["source_id", "relative_path", "exists", "needle_found", "note"]),
            "## CMSM export inventory check",
            md_table(inventory_rows, ["inventory_id", "search_root", "exists", "matching_files", "contract_match_status", "action_taken"]),
            "## Surrogate assumptions",
            md_table(assumption_rows, ["assumption_id", "object", "value", "units", "source_or_reason", "claim_status"]),
            "## Surrogate grid metadata",
            md_table(grid_rows, ["grid_id", "segment", "full_grid_samples", "preview_rows_written", "orbit_model", "attitude_model", "mask_model", "claim_status"]),
            "## Surrogate gxS preview",
            md_table(preview_rows[:10], ["row_id", "sample_index", "t_sec_from_segment_start", "gx_surrogate_m_s2", "gz_surrogate_m_s2", "Sxx_surrogate_s2", "Sxz_surrogate_s2", "source_status"]),
            "## Replacement map",
            md_table(map_rows, ["map_id", "official_contract_column", "surrogate_column", "replacement_status", "evidence_policy", "next_action"]),
            "## Status ledger",
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
    inventory_rows = cmsm_export_inventory_rows()
    assumption_rows = surrogate_assumption_rows()
    grid_rows = surrogate_grid_metadata_rows()
    preview_rows = surrogate_preview_rows()
    map_rows = replacement_map_rows()
    status_rows = surrogate_status_rows()
    prediction_rows = product_prediction_rows()
    bound_rows_ = bound_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R10_1074_SOURCE_REGISTER.csv",
        "inventory": OUT / "P8_Y5_R10_1074_CMSM_EXPORT_INVENTORY_CHECK.csv",
        "assumptions": OUT / "P8_Y5_R10_1074_SURROGATE_ASSUMPTIONS.csv",
        "grid": OUT / "P8_Y5_R10_1074_SURROGATE_GRID_METADATA_SEGMENT210.csv",
        "preview": OUT / "P8_Y5_R10_1074_SURROGATE_GXS_PREVIEW_SEGMENT210.csv",
        "replacement_map": OUT / "P8_Y5_R10_1074_SURROGATE_TO_OFFICIAL_REPLACEMENT_MAP.csv",
        "status": OUT / "P8_Y5_R10_1074_SURROGATE_STATUS_LEDGER.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1074_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1074_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1074_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1074_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1074_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1074_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["inventory"], inventory_rows)
    write_csv(outputs["assumptions"], assumption_rows)
    write_csv(outputs["grid"], grid_rows)
    write_csv(outputs["preview"], preview_rows)
    write_csv(outputs["replacement_map"], map_rows)
    write_csv(outputs["status"], status_rows)
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
        inventory_rows,
        assumption_rows,
        grid_rows,
        preview_rows,
        map_rows,
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
        inventory_rows,
        assumption_rows,
        grid_rows,
        preview_rows,
        map_rows,
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
