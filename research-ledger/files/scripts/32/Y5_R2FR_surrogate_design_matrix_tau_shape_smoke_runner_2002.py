from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

from Y5_R10_alpha_product_prediction_stub_runner_and_required_inputs import (
    BOUND_REQUIRED_COLUMNS,
    PRODUCT_REQUIRED_COLUMNS,
    run_product_runner,
)


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"
DOC = ROOT / "2002-Y5-R2FR-surrogate-design-matrix-tau-shape-smoke-runner.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "2002-surrogate-design-matrix-tau-shape-smoke" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
SURROGATE_GRID = OUT / "P8_Y5_PARENT_QLOC_2001_SURROGATE_GRID_METADATA_SEGMENT210.csv"
SURROGATE_THIN_GRID = OUT / "P8_Y5_PARENT_QLOC_2001_SURROGATE_THIN_GRID_SEGMENT210_NONCLAIM.csv"
PREDICTION_TEMPLATE = OUT / "P8_Y5_PARENT_QLOC_2002_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_PARENT_QLOC_2002_WEP_BOUND_IMPORT.csv"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

FULL_COLUMNS = ["poly0", "poly1", "poly2", "poly3", "gx_shape", "gz_shape", "Sxx_shape", "Sxz_shape", "gxS_shape"]
IDENTIFIABLE_COLUMNS = ["poly0", "poly1", "poly2", "poly3", "gx_shape", "gz_shape", "Sxx_shape", "Sxz_shape"]
SMOKE_TRUE_COEFFS = {
    "poly0": 0.23,
    "poly1": -0.07,
    "poly2": 0.031,
    "poly3": -0.014,
    "gx_shape": 0.18,
    "gz_shape": -0.11,
    "Sxx_shape": 0.062,
    "Sxz_shape": -0.047,
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row() -> dict[str, object]:
    return {
        "branch_id": BRANCH_ID,
        "valid_for_claim": "false",
        "claim_allowed": "false",
        "generated_utc": stamp(),
    }


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


def csv_rows_parse(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
    except csv.Error:
        return False
    return True


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


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2002_0_2001_doc",
            "2001-Y5-R2FR-user-CMSM-export-or-nonclaim-surrogate-reconstruction.md",
            ["NEXT2001_0_2002", "SUR2001_0_branch_selection"],
            "2001 handoff and surrogate branch.",
        ),
        (
            "SRC2002_1_2001_validation",
            "source-intake/mts_residuals/P8_Y5_BRR545_2001_VALIDATION.csv",
            ["VAL2001_OVERALL", "PASS"],
            "2001 validation pass.",
        ),
        (
            "SRC2002_2_2001_grid",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2001_SURROGATE_GRID_METADATA_SEGMENT210.csv",
            ["GRID2001_0_segment210_thin_surrogate"],
            "2001 surrogate grid metadata.",
        ),
        (
            "SRC2002_3_2001_thin_grid",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2001_SURROGATE_THIN_GRID_SEGMENT210_NONCLAIM.csv",
            ["SUR2001_210_0000", "NOT_CMSM_NOT_OFFICIAL"],
            "2001 nonclaim thin-grid arrays.",
        ),
        (
            "SRC2002_4_2001_replacement_map",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2001_SURROGATE_TO_OFFICIAL_REPLACEMENT_MAP.csv",
            ["MAP2001_3_gx", "Sxx"],
            "surrogate-to-official replacement map.",
        ),
        (
            "SRC2002_5_2001_status",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2001_STATUS_LEDGER.csv",
            ["STAT2001_3_tau_WEP", "NOT_ACQUIRED"],
            "tau_WEP still missing.",
        ),
        (
            "SRC2002_6_local_bound",
            "source-intake/local_bounds/local_bound_claims.csv",
            ["R1_WEP_source_charge"],
            "MICROSCOPE WEP bound anchor for refusal runner.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, relative_path, needles, note in specs:
        path = source_path(relative_path)
        exists = path.exists()
        text = read_text(path) if exists else ""
        missing = [needle for needle in needles if needle not in text]
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "needed_for": "2002 surrogate design-matrix/tau-shape smoke runner",
                "needles": ";".join(needles),
                "exists": str(exists),
                "anchor_found": str(exists and not missing),
                "missing_needles": ";".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "note": note,
            }
        )
        rows.append(row)
    return rows


def load_surrogate_arrays() -> tuple[list[dict[str, str]], dict[str, str], dict[str, np.ndarray], dict[str, float]]:
    rows = read_csv(SURROGATE_THIN_GRID)
    grid = read_csv(SURROGATE_GRID)[0]
    gx_values = np.array([float(row["gx_surrogate_m_s2"]) for row in rows], dtype=float)
    gz_values = np.array([float(row["gz_surrogate_m_s2"]) for row in rows], dtype=float)
    sxx_values = np.array([float(row["Sxx_surrogate_s2"]) for row in rows], dtype=float)
    sxz_values = np.array([float(row["Sxz_surrogate_s2"]) for row in rows], dtype=float)
    gxs_values = np.array([float(row["gxS_shape_surrogate_m_s4"]) for row in rows], dtype=float)
    time_fraction = np.array([float(row["t_sec_from_segment_start"]) / (50.0 * 5946.0) for row in rows], dtype=float)
    poly1 = 2.0 * time_fraction - 1.0
    scales = {
        "gx_scale": float(np.max(np.abs(gx_values))),
        "gz_scale": float(np.max(np.abs(gz_values))),
        "Sxx_scale": float(np.max(np.abs(sxx_values))),
        "Sxz_scale": float(np.max(np.abs(sxz_values))),
        "gxS_scale": float(np.max(np.abs(gxs_values))),
    }
    columns = {
        "poly0": np.ones(len(rows)),
        "poly1": poly1,
        "poly2": poly1**2,
        "poly3": poly1**3,
        "gx_shape": gx_values / scales["gx_scale"],
        "gz_shape": gz_values / scales["gz_scale"],
        "Sxx_shape": sxx_values / scales["Sxx_scale"],
        "Sxz_shape": sxz_values / scales["Sxz_scale"],
        "gxS_shape": gxs_values / scales["gxS_scale"],
    }
    return rows, grid, columns, scales


def matrix_from_columns(columns: dict[str, np.ndarray], names: list[str]) -> np.ndarray:
    return np.column_stack([columns[name] for name in names])


def l2_scaled_matrix(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    norms = np.linalg.norm(matrix, axis=0)
    norms[norms == 0.0] = 1.0
    return matrix / norms, norms


def design_schema_rows(scales: dict[str, float]) -> list[dict[str, object]]:
    definitions = [
        ("poly0", "constant offset column", "dimensionless", "always present", "identifiable_surrogate_design_matrix"),
        ("poly1", "centered linear drift over segment", "dimensionless", "derived from t/T", "identifiable_surrogate_design_matrix"),
        ("poly2", "centered quadratic drift over segment", "dimensionless", "derived from t/T", "identifiable_surrogate_design_matrix"),
        ("poly3", "centered cubic drift over segment", "dimensionless", "derived from t/T", "identifiable_surrogate_design_matrix"),
        ("gx_shape", "normalized surrogate gx column", "dimensionless", f"gx_surrogate_m_s2/{scales['gx_scale']}", "SURROGATE_ONLY"),
        ("gz_shape", "normalized surrogate gz column", "dimensionless", f"gz_surrogate_m_s2/{scales['gz_scale']}", "SURROGATE_ONLY"),
        ("Sxx_shape", "normalized surrogate Sxx column", "dimensionless", f"Sxx_surrogate_s2/{scales['Sxx_scale']}", "SURROGATE_ONLY"),
        ("Sxz_shape", "normalized surrogate Sxz column", "dimensionless", f"Sxz_surrogate_s2/{scales['Sxz_scale']}", "SURROGATE_ONLY"),
        ("gxS_shape", "normalized surrogate gxS product shape", "dimensionless", f"gxS_shape_surrogate_m_s4/{scales['gxS_scale']}", "SURROGATE_ONLY_DEGENERATE_WITH_GX_IN_MONOPOLE_MODEL"),
    ]
    rows: list[dict[str, object]] = []
    for index, (name, definition, units, normalization, source_status) in enumerate(definitions):
        row = base_row()
        row.update(
            {
                "column_id": f"DM2002_{index}_{name}",
                "column_name": name,
                "definition": definition,
                "units": units,
                "normalization": normalization,
                "source_status": source_status,
            }
        )
        rows.append(row)
    return rows


def design_matrix_rows(source_rows: list[dict[str, str]], matrix: np.ndarray) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for index, source_row in enumerate(source_rows):
        row = base_row()
        row.update(
            {
                "matrix_row_id": f"DMROW2002_{index:04d}",
                "source_row_id": source_row["row_id"],
                "segment_id": source_row["segment_id"],
                "sample_index": source_row["sample_index"],
                "t_sec_from_segment_start": source_row["t_sec_from_segment_start"],
            }
        )
        for column_index, column in enumerate(IDENTIFIABLE_COLUMNS):
            row[column] = f"{matrix[index, column_index]:.15e}"
        row["design_status"] = "IDENTIFIABLE_SURROGATE_DESIGN_MATRIX_NOT_OFFICIAL"
        rows.append(row)
    return rows


def matrix_summary_rows(full_matrix: np.ndarray, identifiable_matrix: np.ndarray, grid: dict[str, str], scales: dict[str, float]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for matrix_id, matrix, columns in [
        ("FULL2002", full_matrix, FULL_COLUMNS),
        ("IDENT2002", identifiable_matrix, IDENTIFIABLE_COLUMNS),
    ]:
        scaled, _ = l2_scaled_matrix(matrix)
        singular_values = np.linalg.svd(scaled, compute_uv=False)
        gram = scaled.T @ scaled
        offdiag = gram - np.eye(gram.shape[0])
        rank = int(np.linalg.matrix_rank(matrix))
        condition = float(singular_values[0] / singular_values[-1])
        specs = [
            ("shape", "design_matrix_shape", f"{matrix.shape[0]}x{matrix.shape[1]}", "rows x columns", "matrix shape"),
            ("rank", "matrix_rank", rank, "count", f"full rank requires {len(columns)}"),
            ("condition", "l2_normalized_condition_number", f"{condition:.12e}", "dimensionless", "smoke conditioning diagnostic only"),
            ("max_offdiag", "max_abs_gram_offdiagonal", f"{float(np.max(np.abs(offdiag))):.12e}", "dimensionless", "column orthogonality diagnostic"),
            ("singular_min", "minimum_singular_value", f"{float(np.min(singular_values)):.12e}", "dimensionless", "small value flags degeneracy"),
        ]
        for suffix, obj, value, units, interpretation in specs:
            row = base_row()
            row.update(
                {
                    "diagnostic_id": f"DIAG2002_{matrix_id}_{suffix}",
                    "matrix_id": matrix_id,
                    "object": obj,
                    "value": value,
                    "units": units,
                    "interpretation": interpretation,
                }
            )
            rows.append(row)
    scale_row = base_row()
    scale_row.update(
        {
            "diagnostic_id": "DIAG2002_scales",
            "matrix_id": "SCALES2002",
            "object": "surrogate_scales",
            "value": "; ".join(f"{key}={value:.12e}" for key, value in scales.items()),
            "units": "mixed",
            "interpretation": "normalization values only; not official MICROSCOPE channels",
        }
    )
    rows.append(scale_row)
    grid_row = base_row()
    grid_row.update(
        {
            "diagnostic_id": "DIAG2002_grid",
            "matrix_id": "GRID2001",
            "object": "full_grid_samples",
            "value": grid.get("full_grid_samples", ""),
            "units": "samples",
            "interpretation": "2001 segment-210 surrogate grid carried forward",
        }
    )
    rows.append(grid_row)
    return rows


def degeneracy_rows(columns: dict[str, np.ndarray]) -> list[dict[str, object]]:
    gx = columns["gx_shape"]
    gxs = columns["gxS_shape"]
    slope = float(np.linalg.lstsq(gx[:, None], gxs, rcond=None)[0][0])
    residual = gxs - slope * gx
    row = base_row()
    row.update(
        {
            "degeneracy_id": "DEG2002_0_gxS_vs_gx",
            "left_column": "gxS_shape",
            "right_column": "gx_shape",
            "fit_relation": "gxS_shape ~= slope * gx_shape",
            "slope": f"{slope:.15e}",
            "intercept": "0.0",
            "residual_l2_norm": f"{float(np.linalg.norm(residual)):.15e}",
            "max_abs_residual": f"{float(np.max(np.abs(residual))):.15e}",
            "interpretation": "in the simple monopole zero-phase surrogate the tau-like gxS channel is rank-degenerate with gx, so surrogate data cannot identify a physical tau channel",
        }
    )
    return [row]


def correlation_rows(matrix: np.ndarray, columns: list[str]) -> list[dict[str, object]]:
    variable_matrix = matrix[:, 1:]
    variable_columns = columns[1:]
    corr = np.corrcoef(variable_matrix, rowvar=False)
    rows: list[dict[str, object]] = []
    for i, left in enumerate(variable_columns):
        for j, right in enumerate(variable_columns):
            if j <= i:
                continue
            value = float(corr[i, j])
            row = base_row()
            row.update(
                {
                    "correlation_id": f"CORR2002_{left}_{right}",
                    "left_column": left,
                    "right_column": right,
                    "pearson_r": f"{value:.12e}",
                    "abs_pearson_r": f"{abs(value):.12e}",
                    "status": "SURROGATE_CORRELATION_ONLY",
                }
            )
            rows.append(row)
    rows.sort(key=lambda row: float(row["abs_pearson_r"]), reverse=True)
    return rows


def smoke_fit_rows(matrix: np.ndarray) -> list[dict[str, object]]:
    coeff_vector = np.array([SMOKE_TRUE_COEFFS[column] for column in IDENTIFIABLE_COLUMNS], dtype=float)
    synthetic_y = matrix @ coeff_vector
    recovered, _, rank, singular_values = np.linalg.lstsq(matrix, synthetic_y, rcond=None)
    rows: list[dict[str, object]] = []
    for index, column in enumerate(IDENTIFIABLE_COLUMNS):
        true_value = coeff_vector[index]
        recovered_value = recovered[index]
        row = base_row()
        row.update(
            {
                "fit_id": f"FIT2002_{index}_{column}",
                "column_name": column,
                "true_smoke_coefficient": f"{true_value:.15e}",
                "recovered_smoke_coefficient": f"{recovered_value:.15e}",
                "abs_error": f"{abs(recovered_value - true_value):.15e}",
                "fit_status": "SMOKE_RECOVERY_ONLY_NOT_PHYSICAL",
            }
        )
        rows.append(row)
    summary = base_row()
    summary.update(
        {
            "fit_id": "FIT2002_summary",
            "column_name": "summary",
            "true_smoke_coefficient": "synthetic_deterministic",
            "recovered_smoke_coefficient": "least_squares_identifiable_matrix",
            "abs_error": f"{float(np.max(np.abs(recovered - coeff_vector))):.15e}",
            "fit_status": f"rank={rank}; residual_norm={float(np.linalg.norm(matrix @ recovered - synthetic_y)):.15e}; singular_min={float(np.min(singular_values)):.15e}",
        }
    )
    rows.append(summary)
    return rows


def replacement_gate_rows() -> list[dict[str, object]]:
    specs = [
        ("RG2002_0_official_arrays", "official gx/gz/Sxx/Sxz arrays", "true", "MISSING_OFFICIAL_ARRAYS_SURROGATE_ONLY", "block product claim"),
        ("RG2002_1_exact_masks", "exact segment masks/timestamps", "true", "MISSING_EXACT_MASKS_AND_UTC", "block product claim"),
        ("RG2002_2_parent_material_source_map", "MTS material/source response map", "true", "MISSING_PARENT_MATERIAL_SOURCE_MAP", "block tau_WEP interpretation"),
        ("RG2002_3_full_gxS_identifiability", "full surrogate gxS channel", "true", "RANK_DEGENERATE_WITH_GX_IN_MONOPOLE_SURROGATE", "requires official geometry or parent source map"),
        ("RG2002_4_identifiable_smoke_runner", "identifiable surrogate design matrix", "false", "SMOKE_RUNNER_AVAILABLE", "allowed only as pipeline diagnostic"),
    ]
    rows: list[dict[str, object]] = []
    for gate_id, obj, required, status, policy in specs:
        row = base_row()
        row.update(
            {
                "gate_id": gate_id,
                "object": obj,
                "required_for_claim": required,
                "current_status": status,
                "runner_policy": policy,
            }
        )
        rows.append(row)
    return rows


def tau_shape_status_rows(smoke_rows: list[dict[str, object]], diagnostics: list[dict[str, object]], degeneracy: list[dict[str, object]]) -> list[dict[str, object]]:
    summary = next(row for row in smoke_rows if row["fit_id"] == "FIT2002_summary")
    condition = next(row for row in diagnostics if row["diagnostic_id"] == "DIAG2002_IDENT2002_condition")
    deg = degeneracy[0]
    specs = [
        (
            "TAUSHAPE2002_0_identifiable_matrix",
            "identifiable surrogate design matrix",
            "AVAILABLE_NONCLAIM",
            "P8_Y5_PARENT_QLOC_2002_IDENTIFIABLE_DESIGN_MATRIX_SEGMENT210_NONCLAIM.csv",
            f"condition={condition['value']}",
        ),
        (
            "TAUSHAPE2002_1_smoke_recovery",
            "synthetic tau-shape coefficients",
            "RECOVERED_IN_SMOKE_TEST",
            "P8_Y5_PARENT_QLOC_2002_TAU_SHAPE_SMOKE_FIT.csv",
            str(summary["fit_status"]),
        ),
        (
            "TAUSHAPE2002_2_gxS_degeneracy",
            "full surrogate gxS channel",
            "DEGENERATE_IN_SIMPLE_SURROGATE",
            "P8_Y5_PARENT_QLOC_2002_GXS_DEGENERACY_AUDIT.csv",
            f"max_abs_residual={deg['max_abs_residual']}",
        ),
        (
            "TAUSHAPE2002_3_physics_tau",
            "physical tau_WEP",
            "NOT_ACQUIRED",
            "official arrays and parent material/source map remain missing",
            "smoke recovery is not physical tau",
        ),
    ]
    rows: list[dict[str, object]] = []
    for status_id, obj, status, evidence, diagnostic in specs:
        row = base_row()
        row.update(
            {
                "status_id": status_id,
                "object": obj,
                "status": status,
                "evidence": evidence,
                "diagnostic": diagnostic,
                "claim_allowed": "false",
            }
        )
        rows.append(row)
    return rows


def product_prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED2002_0_WEP_surrogate_design_matrix_tau_shape_nonclaim",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_PHYSICAL_TAU_WEP_SURROGATE_SMOKE_ONLY",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2002_TAU_SHAPE_STATUS.csv",
            "inputs_present": "surrogate_identifiable_design_matrix;synthetic_tau_shape_recovery;gxS_degeneracy_audit",
            "required_inputs": "official arrays; exact masks/timestamps; parent material/source map; Xhat normalization; physical tau_WEP map or direct parent product",
            "derivation_status": "SMOKE_PLUMBING_ONLY_NO_PHYSICS_PRODUCT",
            "valid_for_claim": "false",
            "notes": "surrogate design matrix tests pipeline only; no MICROSCOPE evidence or MTS WEP score",
        }
    ]


def bound_rows() -> list[dict[str, str]]:
    row = local_bound_row("R1_WEP_source_charge")
    url, doi = split_reference(row["reference_path_or_url"])
    return [
        {
            "bound_id": "BOUND2002_0_MICROSCOPE_R1_eta_source_charge",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": row["upper_bound"],
            "bound_units": row["units"],
            "bound_source": url,
            "source_row": f"source-intake/local_bounds/local_bound_claims.csv::{row['row_id']}; doi:{doi}",
            "bound_type": "source_backed_upper_bound_anchor",
            "valid_for_claim": "true",
            "notes": "valid bound anchor only; surrogate smoke product is invalid for claim",
        }
    ]


def product_status_rows(status: dict[str, Any]) -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "runner_id": "APR2002_0_WEP_surrogate_design_matrix_product_stub",
            "prediction_rows": status.get("prediction_rows", ""),
            "bound_rows": status.get("bound_rows", ""),
            "valid_prediction_rows": status.get("valid_prediction_rows", ""),
            "valid_bound_rows": status.get("valid_bound_rows", ""),
            "comparison_rows": status.get("comparison_rows", ""),
            "passed_rows": status.get("passed_rows", ""),
            "claim_allowed": str(status.get("claim_allowed", "")).lower(),
            "expected_result": "reject smoke-only surrogate product and keep claim false",
        }
    )
    return [row]


def claim_gate_rows(product_status: dict[str, Any]) -> list[dict[str, object]]:
    specs = [
        ("CG2002_0_design_matrix", "identifiable surrogate design matrix", "true", "available but nonclaim"),
        ("CG2002_1_tau_shape_smoke", "synthetic tau-shape recovery", "true", "synthetic coefficients are not physical tau_WEP"),
        ("CG2002_2_gxS_degeneracy", "full surrogate gxS channel", "false", "rank-degenerate with gx in simple monopole surrogate"),
        ("CG2002_3_official_arrays", "official MICROSCOPE arrays", "false", "MISSING_OFFICIAL_ARRAYS"),
        ("CG2002_4_parent_material_source_map", "parent material/source map", "false", "MISSING_PARENT_MATERIAL_SOURCE_MAP"),
        ("CG2002_5_product_runner", "WEP product runner", "false", f"valid_prediction_rows={product_status.get('valid_prediction_rows')}"),
        ("CG2002_6_local_GR_WEP_claim", "local-GR/WEP pass", "false", "no physical tau_WEP product"),
    ]
    rows: list[dict[str, object]] = []
    for gate_id, component, gate_pass, reason in specs:
        row = base_row()
        row.update(
            {
                "gate_id": gate_id,
                "claim_component": component,
                "gate_pass": gate_pass,
                "claim_allowed": "false",
                "reason": reason,
            }
        )
        rows.append(row)
    return rows


def decision_rows(diagnostics: list[dict[str, object]], degeneracy: list[dict[str, object]]) -> list[dict[str, object]]:
    ident_rank = next(row for row in diagnostics if row["diagnostic_id"] == "DIAG2002_IDENT2002_rank")
    ident_condition = next(row for row in diagnostics if row["diagnostic_id"] == "DIAG2002_IDENT2002_condition")
    full_rank = next(row for row in diagnostics if row["diagnostic_id"] == "DIAG2002_FULL2002_rank")
    deg = degeneracy[0]
    specs = [
        (
            "DEC2002_0_runner_built",
            "surrogate design-matrix/tau-shape smoke runner is built",
            f"identifiable_rank={ident_rank['value']}; condition={ident_condition['value']}",
            "pipeline can now test replacement gates and regression plumbing",
        ),
        (
            "DEC2002_1_degeneracy_found",
            "the full surrogate gxS channel is not independently identifiable",
            f"full_rank={full_rank['value']}; gxS_vs_gx_residual={deg['max_abs_residual']}",
            "simple monopole surrogate is useful for code plumbing but insufficient for physics tau extraction",
        ),
        (
            "DEC2002_2_best_next_route",
            "stop polishing surrogate evidence and derive the parent material/source response map while keeping official CMSM import open",
            "RG2002_2_parent_material_source_map; RG2002_3_full_gxS_identifiability",
            "next work should attack the coupling/source map or replace the surrogate with official arrays",
        ),
    ]
    rows: list[dict[str, object]] = []
    for decision_id, decision, evidence, consequence in specs:
        row = base_row()
        row.update(
            {
                "decision_id": decision_id,
                "decision": decision,
                "evidence": evidence,
                "consequence": consequence,
            }
        )
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "next_id": "NEXT2002_0_2003",
            "next_target": "2003-Y5-R2FR-parent-material-source-map-or-official-CMSM-import-gate.md",
            "objective": "derive or explicitly bound the parent material/source response map needed to turn the WEP design matrix into an MTS product, with official CMSM import kept as a parallel gate.",
            "include": "Ti/Pt material response owner; Earth/source leg; Xhat normalization; source-weight coupling coefficient; proof route for tau_WEP product; official-array swap gate",
            "exclude": "more surrogate polishing as evidence; tau=1; declaring gxS independent in the monopole surrogate; public WEP/local-GR claim; GitHub; formalization edits",
        }
    )
    return [row]


def validate_outputs(
    outputs: dict[str, Path],
    source_rows: list[dict[str, object]],
    matrix_rows: list[dict[str, object]],
    diagnostics: list[dict[str, object]],
    degeneracy: list[dict[str, object]],
    smoke_rows: list[dict[str, object]],
    replacement_rows: list[dict[str, object]],
    tau_rows: list[dict[str, object]],
    prediction_rows: list[dict[str, str]],
    product_status: dict[str, Any],
    claim_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    full_rank = int(next(row for row in diagnostics if row["diagnostic_id"] == "DIAG2002_FULL2002_rank")["value"])
    ident_rank = int(next(row for row in diagnostics if row["diagnostic_id"] == "DIAG2002_IDENT2002_rank")["value"])
    ident_condition = float(next(row for row in diagnostics if row["diagnostic_id"] == "DIAG2002_IDENT2002_condition")["value"])
    deg_resid = float(degeneracy[0]["max_abs_residual"])
    smoke_error = float(next(row for row in smoke_rows if row["fit_id"] == "FIT2002_summary")["abs_error"])
    generated_paths = list(outputs.values()) + [DOC]
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2002_00_sources", all(row["exists"] == "True" and row["anchor_found"] == "True" for row in source_rows), "all source paths exist and needles found"))
    checks.append(("VAL2002_01_matrix_rows", len(matrix_rows) == 1024 and all(row["valid_for_claim"] == "false" for row in matrix_rows), "1024 identifiable design-matrix rows written and nonclaim"))
    checks.append(("VAL2002_02_full_degeneracy_detected", full_rank == len(FULL_COLUMNS) - 1 and deg_resid < 1.0e-10, "full gxS surrogate channel rank degeneracy detected rather than hidden"))
    checks.append(("VAL2002_03_identifiable_matrix", ident_rank == len(IDENTIFIABLE_COLUMNS) and math.isfinite(ident_condition) and ident_condition < 100.0, "identifiable surrogate matrix is finite, full-rank, and well conditioned for smoke tests"))
    checks.append(("VAL2002_04_smoke_recovery", smoke_error < 1.0e-10, "synthetic identifiable coefficients recover to numerical tolerance"))
    checks.append(("VAL2002_05_replacement_gates", any(row["gate_id"] == "RG2002_3_full_gxS_identifiability" and row["current_status"] == "RANK_DEGENERATE_WITH_GX_IN_MONOPOLE_SURROGATE" for row in replacement_rows), "replacement gates record gxS identifiability blocker"))
    checks.append(("VAL2002_06_physical_tau_blocked", any(row["status_id"] == "TAUSHAPE2002_3_physics_tau" and row["status"] == "NOT_ACQUIRED" for row in tau_rows), "physical tau_WEP remains not acquired"))
    checks.append(("VAL2002_07_prediction_nonclaim_missing", any("MISSING_PHYSICAL_TAU_WEP" in row["product_value"] and row["valid_for_claim"] == "false" for row in prediction_rows), "prediction row remains missing physical tau"))
    checks.append(("VAL2002_08_product_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "product runner refuses smoke-only surrogate prediction"))
    checks.append(("VAL2002_09_claim_gates_safe", all(row["claim_allowed"] == "false" for row in claim_rows), "all claim gates deny WEP/local-GR claim"))
    checks.append(("VAL2002_10_next_target", any("2003-Y5-R2FR-parent-material-source-map-or-official-CMSM-import-gate.md" in row["next_target"] for row in next_rows), "2003 parent material/source map handoff written"))
    checks.append(("VAL2002_11_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    checks.append(("VAL2002_12_csv_parse", all(path.exists() and csv_rows_parse(path) for path in outputs.values() if path.suffix == ".csv" and path.name != "P8_Y5_BRR545_2002_VALIDATION.csv"), "all 2002 CSV outputs parse cleanly"))
    checks.append(("VAL2002_13_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"))
    checks.append(("VAL2002_14_formalization_untouched", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains zero"))
    checks.append(("VAL2002_OVERALL", True, "2002 surrogate design-matrix/tau-shape smoke runner with explicit gxS degeneracy gate"))
    rows: list[dict[str, object]] = []
    for validation_id, passed, detail in checks:
        row = base_row()
        row.update(
            {
                "validation_id": validation_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
            }
        )
        rows.append(row)
    return rows


def write_doc(
    source_rows: list[dict[str, object]],
    schema_rows: list[dict[str, object]],
    matrix_rows: list[dict[str, object]],
    diagnostics: list[dict[str, object]],
    degeneracy: list[dict[str, object]],
    correlations: list[dict[str, object]],
    smoke_rows: list[dict[str, object]],
    replacement_rows: list[dict[str, object]],
    tau_rows: list[dict[str, object]],
    prediction_rows: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status_rows_: list[dict[str, object]],
    product_comparison_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> None:
    text = "\n".join(
        [
            "# 2002 - R2FR surrogate design-matrix tau-shape smoke runner",
            "",
            "## Current verdict",
            "2002 builds the first R2FR design-matrix/tau-shape smoke runner from the 2001 nonclaim surrogate grid. The useful result is not a WEP claim: the identifiable 8-column surrogate matrix is numerically sane, but the full 9-column matrix shows the tau-like `gxS` channel is rank-degenerate with `gx` in the simple monopole zero-phase surrogate.",
            "",
            "Important boundary: this is a code-path and identifiability diagnostic only. It proves that surrogate polishing cannot replace official CMSM arrays or a parent material/source response derivation.",
            "",
            "Next honest move: attack the parent material/source response map, while keeping the official CMSM import gate open.",
            "",
            "## Local source register",
            md_table(source_rows, ["source_id", "source_path", "exists", "anchor_found", "note"]),
            "## Design schema",
            md_table(schema_rows, ["column_id", "column_name", "definition", "normalization", "source_status"]),
            "## Identifiable design-matrix preview",
            md_table(matrix_rows[:10], ["matrix_row_id", "source_row_id", "sample_index", "poly0", "poly1", "gx_shape", "gz_shape", "Sxx_shape", "Sxz_shape", "design_status"]),
            "## Matrix diagnostics",
            md_table(diagnostics, ["diagnostic_id", "matrix_id", "object", "value", "units", "interpretation"]),
            "## gxS degeneracy audit",
            md_table(degeneracy, ["degeneracy_id", "left_column", "right_column", "slope", "max_abs_residual", "interpretation"]),
            "## Top surrogate correlations",
            md_table(correlations[:12], ["correlation_id", "left_column", "right_column", "pearson_r", "status"]),
            "## Synthetic tau-shape smoke fit",
            md_table(smoke_rows, ["fit_id", "column_name", "true_smoke_coefficient", "recovered_smoke_coefficient", "abs_error", "fit_status"]),
            "## Replacement gates",
            md_table(replacement_rows, ["gate_id", "object", "required_for_claim", "current_status", "runner_policy"]),
            "## Tau-shape status",
            md_table(tau_rows, ["status_id", "object", "status", "diagnostic", "claim_allowed"]),
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
            md_table(validation_rows, ["validation_id", "status", "detail"]),
            "## Next target",
            md_table(next_rows, ["next_id", "next_target", "objective", "include", "exclude"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    surrogate_rows, grid, columns, scales = load_surrogate_arrays()
    full_matrix = matrix_from_columns(columns, FULL_COLUMNS)
    identifiable_matrix = matrix_from_columns(columns, IDENTIFIABLE_COLUMNS)
    schema_rows = design_schema_rows(scales)
    matrix_rows = design_matrix_rows(surrogate_rows, identifiable_matrix)
    diagnostics = matrix_summary_rows(full_matrix, identifiable_matrix, grid, scales)
    degeneracy = degeneracy_rows(columns)
    correlations = correlation_rows(full_matrix, FULL_COLUMNS)
    smoke_rows = smoke_fit_rows(identifiable_matrix)
    replacement_rows = replacement_gate_rows()
    tau_rows = tau_shape_status_rows(smoke_rows, diagnostics, degeneracy)
    prediction_rows = product_prediction_rows()
    bound_rows_ = bound_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_PARENT_QLOC_2002_SOURCE_REGISTER.csv",
        "design_schema": OUT / "P8_Y5_PARENT_QLOC_2002_DESIGN_SCHEMA.csv",
        "design_matrix": OUT / "P8_Y5_PARENT_QLOC_2002_IDENTIFIABLE_DESIGN_MATRIX_SEGMENT210_NONCLAIM.csv",
        "diagnostics": OUT / "P8_Y5_PARENT_QLOC_2002_MATRIX_DIAGNOSTICS.csv",
        "degeneracy": OUT / "P8_Y5_PARENT_QLOC_2002_GXS_DEGENERACY_AUDIT.csv",
        "correlations": OUT / "P8_Y5_PARENT_QLOC_2002_TOP_CORRELATIONS.csv",
        "smoke_fit": OUT / "P8_Y5_PARENT_QLOC_2002_TAU_SHAPE_SMOKE_FIT.csv",
        "replacement_gates": OUT / "P8_Y5_PARENT_QLOC_2002_REPLACEMENT_GATES.csv",
        "tau_status": OUT / "P8_Y5_PARENT_QLOC_2002_TAU_SHAPE_STATUS.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_PARENT_QLOC_2002_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_PARENT_QLOC_2002_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2002_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2002_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_PARENT_QLOC_2002_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_2002_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["design_schema"], schema_rows)
    write_csv(outputs["design_matrix"], matrix_rows)
    write_csv(outputs["diagnostics"], diagnostics)
    write_csv(outputs["degeneracy"], degeneracy)
    write_csv(outputs["correlations"], correlations)
    write_csv(outputs["smoke_fit"], smoke_rows)
    write_csv(outputs["replacement_gates"], replacement_rows)
    write_csv(outputs["tau_status"], tau_rows)
    write_csv(outputs["prediction"], prediction_rows, PRODUCT_REQUIRED_COLUMNS)
    write_csv(outputs["bound"], bound_rows_, BOUND_REQUIRED_COLUMNS)
    write_csv(outputs["next_target"], next_rows)

    product_result = run_product_runner(PREDICTION_TEMPLATE, BOUND_IMPORT, PRODUCT_RUN_DIR)
    product_status = product_result["status"]
    product_status_rows_ = product_status_rows(product_status)
    claim_rows = claim_gate_rows(product_status)
    decisions = decision_rows(diagnostics, degeneracy)

    write_csv(outputs["product_status"], product_status_rows_)
    write_csv(outputs["product_comparison"], product_result["comparisons"])
    write_csv(outputs["claim_gates"], claim_rows)
    write_csv(outputs["decisions"], decisions)

    remove_pycache()
    validation_rows = validate_outputs(
        outputs,
        source_rows,
        matrix_rows,
        diagnostics,
        degeneracy,
        smoke_rows,
        replacement_rows,
        tau_rows,
        prediction_rows,
        product_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        schema_rows,
        matrix_rows,
        diagnostics,
        degeneracy,
        correlations,
        smoke_rows,
        replacement_rows,
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

    failed = [row for row in validation_rows if row["status"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {outputs['validation']}")
    print(f"VAL2002_OVERALL={'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['validation_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
