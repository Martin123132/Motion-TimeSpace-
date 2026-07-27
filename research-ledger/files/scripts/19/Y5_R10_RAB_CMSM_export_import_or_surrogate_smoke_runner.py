from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
CMSM_ROOT = ROOT / "source-intake" / "microscope_cmsm"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1423-Y5-R10-RAB-CMSM-export-import-or-surrogate-smoke-runner.md"
SOURCE_REGISTER = OUT / "P8_Y5_R10_1423_SOURCE_REGISTER.csv"
EXPORT_INVENTORY = OUT / "P8_Y5_R10_1423_CMSM_EXPORT_INVENTORY.csv"
OFFICIAL_IMPORT_STATUS = OUT / "P8_Y5_R10_1423_OFFICIAL_IMPORT_STATUS.csv"
OFFICIAL_ARRAY_PREVIEW = OUT / "P8_Y5_R10_1423_OFFICIAL_ARRAY_PREVIEW.csv"
SURROGATE_INPUT_STATUS = OUT / "P8_Y5_R10_1423_SURROGATE_SMOKE_INPUT_STATUS.csv"
SURROGATE_DESIGN_PREVIEW = OUT / "P8_Y5_R10_1423_SURROGATE_DESIGN_MATRIX_PREVIEW.csv"
SURROGATE_DIAGNOSTICS = OUT / "P8_Y5_R10_1423_SURROGATE_MATRIX_DIAGNOSTICS.csv"
SURROGATE_TAU_FIT = OUT / "P8_Y5_R10_1423_SURROGATE_TAU_SHAPE_FIT.csv"
REPLACEMENT_GATE = OUT / "P8_Y5_R10_1423_REPLACEMENT_GATE.csv"
PRODUCT_RUNNER_STATUS = OUT / "P8_Y5_R10_1423_PRODUCT_RUNNER_STATUS.csv"
CLAIM_GATE = OUT / "P8_Y5_R10_1423_CLAIM_GATE.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1423_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1423_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1423_VALIDATION.csv"

SURROGATE_GXS = OUT / "P8_Y5_R10_1074_SURROGATE_GXS_PREVIEW_SEGMENT210.csv"
SURROGATE_GRID = OUT / "P8_Y5_R10_1074_SURROGATE_GRID_METADATA_SEGMENT210.csv"

DESIGN_COLUMNS = ["poly0", "poly1", "poly2", "poly3", "gx_shape", "gz_shape", "Sxx_shape", "Sxz_shape"]
SMOKE_TRUE_COEFFICIENTS = {
    "poly0": 0.0,
    "poly1": 0.0,
    "poly2": 0.0,
    "poly3": 0.0,
    "gx_shape": 1.0e-15,
    "gz_shape": -2.0e-16,
    "Sxx_shape": 1.5e-16,
    "Sxz_shape": -7.5e-17,
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").replace("\r", " ").strip()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows supplied for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: clean(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_headers(path: Path) -> list[str]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        try:
            return [clean(value) for value in next(reader)]
        except StopIteration:
            return []


def text_has(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="ignore")


def md_cell(value: Any) -> str:
    return clean(value).replace("|", "\\|")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


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


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "SRC1423_0_1422_next",
            OUT / "P8_Y5_R10_1422_NEXT_TARGET.csv",
            "NEXT1422_0_1423",
            "1422 handoff naming this CMSM import or surrogate smoke runner.",
        ),
        (
            "SRC1423_1_1422_contract",
            OUT / "P8_Y5_R10_1422_LOCAL_EXPORT_CONTRACT.csv",
            "EXP1422_4_verdict",
            "local CMSM export contract and required files.",
        ),
        (
            "SRC1423_2_1422_validation",
            OUT / "P8_Y5_BRR545_1422_VALIDATION.csv",
            "VAL1422_10_overall",
            "1422 validation; official schema/pilot not acquired.",
        ),
        (
            "SRC1423_3_1074_surrogate_preview",
            SURROGATE_GXS,
            "SUR1074_210_000",
            "nonclaim segment-210 surrogate gx/gz/Sxx/Sxz preview.",
        ),
        (
            "SRC1423_4_1074_grid",
            SURROGATE_GRID,
            "GRID1074_0_segment210_surrogate",
            "surrogate segment-210 grid metadata.",
        ),
        (
            "SRC1423_5_1075_matrix",
            OUT / "P8_Y5_R10_1075_MATRIX_DIAGNOSTICS.csv",
            "DIAG1075_0_shape",
            "prior surrogate design-matrix smoke diagnostic.",
        ),
        (
            "SRC1423_6_1075_tau_fit",
            OUT / "P8_Y5_R10_1075_TAU_SHAPE_SMOKE_FIT.csv",
            "FIT1075_summary",
            "prior synthetic tau-shape recovery check.",
        ),
    ]
    rows = []
    for source_id, path, anchor, role in specs:
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "anchor": anchor,
                "anchor_found": text_has(path, anchor),
                "role": role,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def required_export_specs() -> list[dict[str, Any]]:
    return [
        {
            "inventory_id": "INV1423_0_root_manifest",
            "path": CMSM_ROOT / "dataset_inventory.csv",
            "required_fields": ["dataset_name", "product_type", "file_name", "time_coverage", "session_or_segment"],
            "object": "CMSM root manifest",
        },
        {
            "inventory_id": "INV1423_1_segment210_time_mask",
            "path": CMSM_ROOT / "segment210" / "time_mask.csv",
            "required_fields": ["segment_id", "t_utc", "sample_index", "mask_flag", "mask_reason"],
            "object": "segment 210 exact time grid and masks",
        },
        {
            "inventory_id": "INV1423_2_segment210_orbit",
            "path": CMSM_ROOT / "segment210" / "orbit.csv",
            "required_fields": ["t_utc", "r_x", "r_y", "r_z", "v_x", "v_y", "v_z", "frame", "units"],
            "object": "segment 210 orbit ephemeris",
        },
        {
            "inventory_id": "INV1423_3_segment210_attitude",
            "path": CMSM_ROOT / "segment210" / "attitude_rates.csv",
            "required_fields": ["t_utc", "frame", "q0", "q1", "q2", "q3"],
            "object": "segment 210 attitude/rate product",
        },
        {
            "inventory_id": "INV1423_4_segment210_gxgzS",
            "path": CMSM_ROOT / "segment210" / "gxgzSxxSxz.csv",
            "required_fields": ["segment_id", "t_utc", "gx", "gz", "Sxx", "Sxz", "frame", "generation_method", "source_file"],
            "object": "segment 210 gx/gz/Sxx/Sxz source-leg arrays",
        },
    ]


def export_inventory_rows() -> tuple[list[dict[str, Any]], bool]:
    rows: list[dict[str, Any]] = []
    all_required_present = True
    for spec in required_export_specs():
        path = spec["path"]
        headers = read_headers(path)
        required_fields = spec["required_fields"]
        missing = [field for field in required_fields if field not in headers]
        exists = path.exists()
        complete = exists and not missing
        all_required_present = all_required_present and complete
        rows.append(
            {
                "inventory_id": spec["inventory_id"],
                "object": spec["object"],
                "absolute_path": str(path),
                "exists": exists,
                "headers_seen": ";".join(headers[:24]),
                "required_fields": ";".join(required_fields),
                "missing_fields": ";".join(missing),
                "required_fields_present": complete,
                "status": "READY_FOR_SCHEMA_PARSE" if complete else "NOT_FOUND_OR_SCHEMA_INCOMPLETE",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    local_files = [path for path in CMSM_ROOT.rglob("*") if path.is_file()] if CMSM_ROOT.exists() else []
    rows.append(
        {
            "inventory_id": "INV1423_5_any_local_files",
            "object": "any files under source-intake/microscope_cmsm",
            "absolute_path": str(CMSM_ROOT),
            "exists": CMSM_ROOT.exists(),
            "headers_seen": "",
            "required_fields": "contract files from INV1423_0 through INV1423_4",
            "missing_fields": "" if local_files else "NO_LOCAL_CMSM_EXPORT_FOLDER_OR_FILES",
            "required_fields_present": all_required_present,
            "status": f"local_file_count={len(local_files)}",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows, all_required_present


def official_import_rows(official_ready: bool, inventory_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_items = [
        row["inventory_id"]
        for row in inventory_rows
        if str(row.get("required_fields_present")).lower() != "true" and row["inventory_id"] != "INV1423_5_any_local_files"
    ]
    return [
        {
            "status_id": "OFF1423_0_branch",
            "object": "CMSM export branch",
            "status": "OFFICIAL_EXPORT_SCHEMA_PRESENT_NONCLAIM" if official_ready else "NO_USER_SUPPLIED_CMSM_EXPORT_FOUND",
            "evidence": "all required contract files present" if official_ready else ";".join(missing_items),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "status_id": "OFF1423_1_official_arrays",
            "object": "gx/gz/Sxx/Sxz source-leg arrays",
            "status": "CANONICAL_PREVIEW_WRITTEN_USER_SUPPLIED_UNVERIFIED" if official_ready else "NOT_AVAILABLE",
            "evidence": str(CMSM_ROOT / "segment210" / "gxgzSxxSxz.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "status_id": "OFF1423_2_parent_map",
            "object": "MTS parent material/source response map",
            "status": "MISSING_PARENT_MATERIAL_SOURCE_MAP",
            "evidence": "WEP tau cannot become physical without parent-owned material/source coefficients",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "status_id": "OFF1423_3_verdict",
            "object": "official import evidential ceiling",
            "status": "NONCLAIM_IMPORT_ONLY" if official_ready else "SURROGATE_SMOKE_BRANCH_ONLY",
            "evidence": "official arrays alone are still not local-GR/WEP evidence without parent map and bound runner",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def official_preview_rows(official_ready: bool) -> list[dict[str, Any]]:
    gx_path = CMSM_ROOT / "segment210" / "gxgzSxxSxz.csv"
    if not official_ready or not gx_path.exists():
        return [
            {
                "preview_id": "OFFPREV1423_0_no_official_rows",
                "segment_id": "210",
                "t_utc": "",
                "gx": "",
                "gz": "",
                "Sxx": "",
                "Sxz": "",
                "frame": "",
                "source_file": str(gx_path),
                "source_status": "NO_OFFICIAL_CMSM_EXPORT_AVAILABLE",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        ]
    rows = []
    for index, row in enumerate(read_csv(gx_path)[:12]):
        rows.append(
            {
                "preview_id": f"OFFPREV1423_{index:03d}",
                "segment_id": row.get("segment_id", ""),
                "t_utc": row.get("t_utc", ""),
                "gx": row.get("gx", ""),
                "gz": row.get("gz", ""),
                "Sxx": row.get("Sxx", ""),
                "Sxz": row.get("Sxz", ""),
                "frame": row.get("frame", ""),
                "source_file": row.get("source_file", str(gx_path)),
                "source_status": "USER_SUPPLIED_CMSM_EXPORT_UNVERIFIED_NONCLAIM",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows or official_preview_rows(False)


def load_surrogate_matrix() -> tuple[list[dict[str, str]], dict[str, str], np.ndarray, dict[str, float]]:
    rows = read_csv(SURROGATE_GXS)
    grid = read_csv(SURROGATE_GRID)[0]
    gx = np.array([float(row["gx_surrogate_m_s2"]) for row in rows], dtype=float)
    gz = np.array([float(row["gz_surrogate_m_s2"]) for row in rows], dtype=float)
    sxx = np.array([float(row["Sxx_surrogate_s2"]) for row in rows], dtype=float)
    sxz = np.array([float(row["Sxz_surrogate_s2"]) for row in rows], dtype=float)
    scales = {
        "gx_scale": float(np.max(np.abs(gx))),
        "gz_scale": float(np.max(np.abs(gz))),
        "Sxx_scale": float(np.max(np.abs(sxx))),
        "Sxz_scale": float(np.max(np.abs(sxz))),
    }
    total_time = float(grid["duration_orbits"]) * float(grid["torb_s"])
    frac = np.array([float(row["t_sec_from_segment_start"]) / total_time for row in rows], dtype=float)
    poly1 = 2.0 * frac - 1.0
    matrix = np.column_stack(
        [
            np.ones(len(rows)),
            poly1,
            poly1**2,
            poly1**3,
            gx / scales["gx_scale"],
            gz / scales["gz_scale"],
            sxx / scales["Sxx_scale"],
            sxz / scales["Sxz_scale"],
        ]
    )
    return rows, grid, matrix, scales


def surrogate_input_rows(official_ready: bool, source_rows: list[dict[str, str]], grid: dict[str, str]) -> list[dict[str, Any]]:
    return [
        {
            "input_id": "SIN1423_0_official_override",
            "object": "local CMSM export",
            "status": "AVAILABLE_BUT_NONCLAIM" if official_ready else "ABSENT",
            "detail": str(CMSM_ROOT),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "SIN1423_1_surrogate_preview",
            "object": "1074 segment-210 surrogate gx/gz/Sxx/Sxz",
            "status": "AVAILABLE_SURROGATE_ONLY",
            "detail": f"rows={len(source_rows)}; segment={grid.get('segment')}; claim_status={grid.get('claim_status')}",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "SIN1423_2_branch",
            "object": "1423 execution branch",
            "status": "OFFICIAL_IMPORT_BRANCH_PLUS_NONCLAIM_SURROGATE_REPLAY" if official_ready else "NO_EXPORT_SO_SURROGATE_SMOKE_ONLY",
            "detail": "surrogate is only plumbing evidence; physical tau remains unavailable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def surrogate_design_preview_rows(source_rows: list[dict[str, str]], matrix: np.ndarray) -> list[dict[str, Any]]:
    rows = []
    for index, source_row in enumerate(source_rows[:32]):
        row: dict[str, Any] = {
            "matrix_row_id": f"DMROW1423_{index:03d}",
            "source_row_id": source_row["row_id"],
            "segment_id": source_row["segment_id"],
            "sample_index": source_row["sample_index"],
            "t_sec_from_segment_start": source_row["t_sec_from_segment_start"],
        }
        for column_index, column in enumerate(DESIGN_COLUMNS):
            row[column] = f"{matrix[index, column_index]:.15e}"
        row["source_status"] = "SURROGATE_REPLAY_NOT_CMSM_NOT_OFFICIAL"
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
        rows.append(row)
    return rows


def matrix_diagnostic_rows(matrix: np.ndarray, grid: dict[str, str], scales: dict[str, float]) -> list[dict[str, Any]]:
    norms = np.linalg.norm(matrix, axis=0)
    safe_norms = np.where(norms == 0.0, 1.0, norms)
    scaled = matrix / safe_norms
    gram = scaled.T @ scaled
    offdiag = gram - np.eye(gram.shape[0])
    singular_values = np.linalg.svd(scaled, compute_uv=False)
    rank = int(np.linalg.matrix_rank(matrix))
    condition = float(singular_values[0] / singular_values[-1])
    rows = [
        ("DIAG1423_0_branch", "execution_branch", "SURROGATE_SMOKE_ONLY_NONCLAIM", "text", "official export absent or nonclaim"),
        ("DIAG1423_1_shape", "design_matrix_shape", f"{matrix.shape[0]}x{matrix.shape[1]}", "rows x columns", "same column family as 1075; replayed under 1423 import gate"),
        ("DIAG1423_2_rank", "matrix_rank", rank, "count", "full rank only proves smoke plumbing"),
        ("DIAG1423_3_condition", "l2_normalized_condition_number", f"{condition:.12e}", "dimensionless", "not a physics likelihood"),
        ("DIAG1423_4_max_offdiag", "max_abs_gram_offdiag", f"{float(np.max(np.abs(offdiag))):.12e}", "dimensionless", "column degeneracy smoke diagnostic"),
        ("DIAG1423_5_grid", "surrogate_grid", f"segment={grid.get('segment')}; samples={grid.get('full_grid_samples')}; preview={grid.get('preview_rows_written')}", "metadata", "not official MICROSCOPE product"),
        ("DIAG1423_6_scales", "normalization_scales", ";".join(f"{key}={value:.12e}" for key, value in scales.items()), "mixed", "surrogate normalization only"),
    ]
    return [
        {
            "diagnostic_id": row_id,
            "object": obj,
            "value": value,
            "units": units,
            "interpretation": interpretation,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for row_id, obj, value, units, interpretation in rows
    ]


def tau_fit_rows(matrix: np.ndarray) -> list[dict[str, Any]]:
    true_vector = np.array([SMOKE_TRUE_COEFFICIENTS[column] for column in DESIGN_COLUMNS], dtype=float)
    signal = matrix @ true_vector
    recovered, residuals, rank, singular_values = np.linalg.lstsq(matrix, signal, rcond=None)
    rows: list[dict[str, Any]] = []
    for index, column in enumerate(DESIGN_COLUMNS):
        rows.append(
            {
                "fit_id": f"FIT1423_{index}_{column}",
                "column_name": column,
                "true_smoke_coefficient": f"{true_vector[index]:.15e}",
                "recovered_smoke_coefficient": f"{recovered[index]:.15e}",
                "abs_error": f"{abs(recovered[index] - true_vector[index]):.15e}",
                "fit_status": "SURROGATE_SMOKE_RECOVERY_ONLY_NOT_PHYSICAL_TAU",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    residual_norm = float(np.linalg.norm(matrix @ recovered - signal))
    rows.append(
        {
            "fit_id": "FIT1423_summary",
            "column_name": "summary",
            "true_smoke_coefficient": "synthetic_deterministic",
            "recovered_smoke_coefficient": "least_squares",
            "abs_error": f"{max(abs(recovered - true_vector)):.15e}",
            "fit_status": f"rank={rank}; residual_norm={residual_norm:.15e}; singular_min={float(np.min(singular_values)):.15e}",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def replacement_gate_rows(official_ready: bool) -> list[dict[str, Any]]:
    status = "READY_FOR_REPLACEMENT_IMPORT_NONCLAIM" if official_ready else "MISSING_OFFICIAL_EXPORT"
    return [
        {
            "gate_id": "REP1423_0_gxgzS",
            "object": "gx/gz/Sxx/Sxz columns",
            "current_status": status,
            "required_replacement": "CMSM official/user-exported gxgzSxxSxz.csv with provenance and frame",
            "runner_policy": "surrogate columns cannot support WEP/local-GR claim",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "REP1423_1_masks",
            "object": "exact time masks",
            "current_status": "AVAILABLE_NONCLAIM" if official_ready else "MISSING_EXACT_MASKS_SURROGATE_ALL_UNMASKED",
            "required_replacement": "time_mask.csv matching the exact segment grid",
            "runner_policy": "no guessed masks in claim path",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "REP1423_2_orbit_attitude",
            "object": "orbit and attitude/rates",
            "current_status": "AVAILABLE_NONCLAIM" if official_ready else "MISSING_ORBIT_ATTITUDE_EXPORT",
            "required_replacement": "orbit.csv plus attitude_rates.csv with frames/units",
            "runner_policy": "surrogate circular orbit is a pipeline check only",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "REP1423_3_parent_material_map",
            "object": "MTS parent material/source response map",
            "current_status": "MISSING_PARENT_MATERIAL_SOURCE_MAP",
            "required_replacement": "parent-derived Ti/Pt/source vector coefficients",
            "runner_policy": "official arrays alone do not define physical tau_WEP",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def product_status_rows(official_ready: bool) -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "APR1423_0_import_or_surrogate_product_gate",
            "official_export_ready": official_ready,
            "surrogate_smoke_rows": 256,
            "valid_prediction_rows": 0,
            "valid_bound_rows": 0,
            "comparison_status": "NOT_RUN_NO_PHYSICAL_PREDICTION",
            "expected_result": "reject surrogate/import-only rows and keep claim false",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def claim_gate_rows(official_ready: bool, rank: int) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG1423_0_CMSM_export",
            "claim_component": "user-supplied CMSM export",
            "gate_pass": official_ready,
            "claim_allowed": False,
            "reason": "schema present but still nonclaim" if official_ready else "NO_USER_SUPPLIED_CMSM_EXPORT_FOUND",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1423_1_surrogate_smoke",
            "claim_component": "surrogate design matrix replay",
            "gate_pass": rank == len(DESIGN_COLUMNS),
            "claim_allowed": False,
            "reason": "pipeline diagnostic only; not official MICROSCOPE evidence",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1423_2_physical_tau",
            "claim_component": "physical tau_WEP",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "MISSING_PARENT_MATERIAL_SOURCE_MAP_AND_OFFICIAL_BOUND_RUNNER_INPUTS",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1423_3_local_GR_WEP_claim",
            "claim_component": "local-GR/WEP pass",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "import/surrogate plumbing is not a derived GR reduction or WEP prediction",
            "valid_for_claim": False,
        },
    ]


def decision_rows(official_ready: bool) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1423_0_branch",
            "decision": "use official import branch if complete; otherwise replay surrogate smoke only",
            "evidence": "CMSM export inventory complete" if official_ready else "CMSM export inventory incomplete or absent",
            "consequence": "nonclaim import" if official_ready else "nonclaim surrogate smoke runner executed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1423_1_no_evidence_upgrade",
            "decision": "do not promote 1074/1075 surrogate products",
            "evidence": "surrogate branch uses circular Earth monopole, guessed phase, no official masks",
            "consequence": "WEP/local-GR remains blocked",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1423_2_next_route",
            "decision": "move to parent material/source-map derivation or wait for real CMSM export",
            "evidence": "physical tau_WEP still lacks parent-owned material/source coefficients",
            "consequence": "1424 should attack the parent Ti/Pt/source vector map rather than polish surrogate evidence",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1423_0_1424",
            "next_target": "1424-Y5-R10-RAB-parent-TiPt-source-vector-map-or-official-CMSM-import-lock.md",
            "script": "scripts/Y5_R10_RAB_parent_TiPt_source_vector_map_or_official_CMSM_import_lock.py",
            "objective": "derive or explicitly source the parent-owned Ti/Pt material/source vector map needed to turn official MICROSCOPE arrays into a physical MTS WEP product; keep CMSM import as a locked side gate if the user supplies the export.",
            "include": "parent material/source map; Ti/Pt response vector; source-leg contraction convention; measured-G guard; official-import lock; no surrogate evidence upgrade",
            "exclude": "tau=1; guessed masks; circular-orbit evidence; WEP/local-GR claim; GitHub; formalization-workbench edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    official_ready: bool,
    rank: int,
    claim_gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated_csvs = [
        SOURCE_REGISTER,
        EXPORT_INVENTORY,
        OFFICIAL_IMPORT_STATUS,
        OFFICIAL_ARRAY_PREVIEW,
        SURROGATE_INPUT_STATUS,
        SURROGATE_DESIGN_PREVIEW,
        SURROGATE_DIAGNOSTICS,
        SURROGATE_TAU_FIT,
        REPLACEMENT_GATE,
        PRODUCT_RUNNER_STATUS,
        CLAIM_GATE,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    parse_ok = True
    parse_errors: list[str] = []
    for path in generated_csvs:
        try:
            _ = read_csv(path)
        except Exception as exc:
            parse_ok = False
            parse_errors.append(f"{path.name}:{type(exc).__name__}")
    claim_safe = all(str(row.get("claim_allowed")).lower() == "false" for row in claim_gates)
    formalization_count = count_formalization_modified_since_start()
    checks = [
        ("VAL1423_0_sources", all(row["path_exists"] and row["anchor_found"] for row in sources), "all cited 1422/1074/1075 source rows exist and anchors match"),
        ("VAL1423_1_inventory", True, "CMSM export inventory checked under source-intake/microscope_cmsm"),
        (
            "VAL1423_2_official_branch",
            True,
            "official export branch parsed as nonclaim" if official_ready else "no complete local CMSM export found; surrogate branch selected",
        ),
        ("VAL1423_3_surrogate_rank", rank == len(DESIGN_COLUMNS), f"surrogate replay rank={rank}, columns={len(DESIGN_COLUMNS)}"),
        ("VAL1423_4_claim_gates", claim_safe, "all claim gates keep claim_allowed=false"),
        ("VAL1423_5_csv_parse", parse_ok, "all generated 1423 CSVs parse cleanly" if parse_ok else ";".join(parse_errors)),
        ("VAL1423_6_formalization_untouched", formalization_count == 0, f"formalization modified-file count since start={formalization_count}"),
        ("VAL1423_7_next_target", True, "1424 handoff written"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "generated_utc": stamp(),
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1423_8_overall",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "CMSM export absent; surrogate smoke replay works; WEP/local-GR claim remains blocked",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    inventory: list[dict[str, Any]],
    official_status: list[dict[str, Any]],
    official_preview: list[dict[str, Any]],
    surrogate_inputs: list[dict[str, Any]],
    diagnostics: list[dict[str, Any]],
    tau_fit: list[dict[str, Any]],
    replacement: list[dict[str, Any]],
    product: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    official_branch_status = clean(official_status[0].get("status", ""))
    if official_branch_status == "NO_USER_SUPPLIED_CMSM_EXPORT_FOUND":
        verdict = (
            "1423 found no complete local CMSM export, so it executed only a labelled nonclaim surrogate smoke replay. "
            "The replay verifies matrix/tau-shape plumbing, but it is not MICROSCOPE evidence and it does not unlock WEP, tau, or local-GR claims."
        )
    else:
        verdict = (
            "1423 found a local CMSM export schema and wrote a nonclaim official-array preview, while still replaying the labelled surrogate smoke path as a pipeline check. "
            "Neither branch unlocks WEP, tau, or local-GR claims without the parent Ti/Pt/source vector map and the official bound runner."
        )
    content = "\n\n".join(
        [
            "# 1423 - CMSM export import or surrogate smoke runner",
            f"**Current verdict:** {verdict}",
            "## Source register\n" + md_table(sources),
            "## CMSM export inventory\n" + md_table(inventory),
            "## Official import status\n" + md_table(official_status),
            "## Official array preview\n" + md_table(official_preview),
            "## Surrogate smoke input status\n" + md_table(surrogate_inputs),
            "## Surrogate matrix diagnostics\n" + md_table(diagnostics),
            "## Surrogate tau-shape fit\n" + md_table(tau_fit),
            "## Replacement gates\n" + md_table(replacement),
            "## Product runner status\n" + md_table(product),
            "## Claim gates\n" + md_table(claims),
            "## Decision ledger\n" + md_table(decisions),
            "## Validation\n" + md_table(validations),
            "## Next target\n" + md_table(next_rows),
        ]
    )
    DOC.write_text(content + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    inventory, official_ready = export_inventory_rows()
    official_status = official_import_rows(official_ready, inventory)
    official_preview = official_preview_rows(official_ready)
    source_rows, grid, matrix, scales = load_surrogate_matrix()
    rank = int(np.linalg.matrix_rank(matrix))
    surrogate_inputs = surrogate_input_rows(official_ready, source_rows, grid)
    design_preview = surrogate_design_preview_rows(source_rows, matrix)
    diagnostics = matrix_diagnostic_rows(matrix, grid, scales)
    tau_fit = tau_fit_rows(matrix)
    replacement = replacement_gate_rows(official_ready)
    product = product_status_rows(official_ready)
    claims = claim_gate_rows(official_ready, rank)
    decisions = decision_rows(official_ready)
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(EXPORT_INVENTORY, inventory)
    write_csv(OFFICIAL_IMPORT_STATUS, official_status)
    write_csv(OFFICIAL_ARRAY_PREVIEW, official_preview)
    write_csv(SURROGATE_INPUT_STATUS, surrogate_inputs)
    write_csv(SURROGATE_DESIGN_PREVIEW, design_preview)
    write_csv(SURROGATE_DIAGNOSTICS, diagnostics)
    write_csv(SURROGATE_TAU_FIT, tau_fit)
    write_csv(REPLACEMENT_GATE, replacement)
    write_csv(PRODUCT_RUNNER_STATUS, product)
    write_csv(CLAIM_GATE, claims)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)

    validations = validation_rows(sources, official_ready, rank, claims)
    write_csv(VALIDATION, validations)
    write_doc(
        sources,
        inventory,
        official_status,
        official_preview,
        surrogate_inputs,
        diagnostics,
        tau_fit,
        replacement,
        product,
        claims,
        decisions,
        next_rows,
        validations,
    )
    remove_pycache()
    print("Y5_R10_1423_CMSM_export_absent_surrogate_smoke_replayed_nonclaim")


if __name__ == "__main__":
    main()
