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
SURROGATE_PREVIEW = OUT / "P8_Y5_R10_1074_SURROGATE_GXS_PREVIEW_SEGMENT210.csv"
SURROGATE_GRID = OUT / "P8_Y5_R10_1074_SURROGATE_GRID_METADATA_SEGMENT210.csv"
DOC = ROOT / "1075-Y5-R10-surrogate-design-matrix-tau-shape-smoke-runner.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1075-surrogate-design-matrix-tau-shape-smoke" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1075_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1075_WEP_BOUND_IMPORT.csv"


DESIGN_COLUMNS = ["poly0", "poly1", "poly2", "poly3", "gx_shape", "gz_shape", "Sxx_shape", "Sxz_shape"]
SMOKE_TRUE_COEFFS = {
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
        ("SRC1075_0_1074_next", "source-intake/mts_residuals/P8_Y5_R10_1074_NEXT_TARGET.csv", "1075-Y5-R10-surrogate-design-matrix-tau-shape-smoke-runner.md", "1074 handoff."),
        ("SRC1075_1_1074_validation", "source-intake/mts_residuals/P8_Y5_BRR545_1074_VALIDATION.csv", "V1074_SUMMARY", "1074 validation summary."),
        ("SRC1075_2_1074_grid", "source-intake/mts_residuals/P8_Y5_R10_1074_SURROGATE_GRID_METADATA_SEGMENT210.csv", "GRID1074_0_segment210_surrogate", "surrogate grid metadata."),
        ("SRC1075_3_1074_preview", "source-intake/mts_residuals/P8_Y5_R10_1074_SURROGATE_GXS_PREVIEW_SEGMENT210.csv", "SUR1074_210_000", "surrogate gxS rows."),
        ("SRC1075_4_1074_map", "source-intake/mts_residuals/P8_Y5_R10_1074_SURROGATE_TO_OFFICIAL_REPLACEMENT_MAP.csv", "MAP1074_0_gx", "surrogate-to-official replacement map."),
        ("SRC1075_5_1074_status", "source-intake/mts_residuals/P8_Y5_R10_1074_SURROGATE_STATUS_LEDGER.csv", "STAT1074_3_tau_WEP", "numeric tau still missing."),
        ("SRC1075_6_1073_schema", "source-intake/mts_residuals/P8_Y5_R10_1073_OFFICIAL_ARRAY_SCHEMA_CONTRACT.csv", "ARR1073_3_gx", "official array schema contract."),
        ("SRC1075_7_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge", "MICROSCOPE WEP bound row."),
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


def load_surrogate_arrays() -> tuple[list[dict[str, str]], dict[str, str], np.ndarray, dict[str, float]]:
    rows = read_csv(SURROGATE_PREVIEW)
    grid = read_csv(SURROGATE_GRID)[0]
    gx_values = np.array([float(row["gx_surrogate_m_s2"]) for row in rows], dtype=float)
    gz_values = np.array([float(row["gz_surrogate_m_s2"]) for row in rows], dtype=float)
    sxx_values = np.array([float(row["Sxx_surrogate_s2"]) for row in rows], dtype=float)
    sxz_values = np.array([float(row["Sxz_surrogate_s2"]) for row in rows], dtype=float)
    scales = {
        "gx_scale": float(np.max(np.abs(gx_values))),
        "gz_scale": float(np.max(np.abs(gz_values))),
        "Sxx_scale": float(np.max(np.abs(sxx_values))),
        "Sxz_scale": float(np.max(np.abs(sxz_values))),
    }
    time_fraction = np.array([float(row["t_sec_from_segment_start"]) / (50.0 * 5946.0) for row in rows], dtype=float)
    poly1 = 2.0 * time_fraction - 1.0
    matrix = np.column_stack(
        [
            np.ones(len(rows)),
            poly1,
            poly1**2,
            poly1**3,
            gx_values / scales["gx_scale"],
            gz_values / scales["gz_scale"],
            sxx_values / scales["Sxx_scale"],
            sxz_values / scales["Sxz_scale"],
        ]
    )
    return rows, grid, matrix, scales


def design_schema_rows(scales: dict[str, float]) -> list[dict[str, str]]:
    definitions = [
        ("poly0", "constant offset column", "dimensionless", "always present", "surrogate_design_matrix"),
        ("poly1", "centered linear drift over segment preview", "dimensionless", "derived from t/T", "surrogate_design_matrix"),
        ("poly2", "centered quadratic drift over segment preview", "dimensionless", "derived from t/T", "surrogate_design_matrix"),
        ("poly3", "centered cubic drift over segment preview", "dimensionless", "derived from t/T", "surrogate_design_matrix"),
        ("gx_shape", "normalized surrogate gx column", "dimensionless", f"gx_surrogate_m_s2/{scales['gx_scale']}", "SURROGATE_ONLY"),
        ("gz_shape", "normalized surrogate gz column", "dimensionless", f"gz_surrogate_m_s2/{scales['gz_scale']}", "SURROGATE_ONLY"),
        ("Sxx_shape", "normalized surrogate Sxx column", "dimensionless", f"Sxx_surrogate_s2/{scales['Sxx_scale']}", "SURROGATE_ONLY"),
        ("Sxz_shape", "normalized surrogate Sxz column", "dimensionless", f"Sxz_surrogate_s2/{scales['Sxz_scale']}", "SURROGATE_ONLY"),
    ]
    return [
        {
            "column_id": f"DM1075_{index}_{name}",
            "column_name": name,
            "definition": definition,
            "units": units,
            "normalization": normalization,
            "source_status": source_status,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for index, (name, definition, units, normalization, source_status) in enumerate(definitions)
    ]


def design_matrix_rows(source_rows: list[dict[str, str]], matrix: np.ndarray) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for index, source_row in enumerate(source_rows):
        row: dict[str, object] = {
            "matrix_row_id": f"DMROW1075_{index:03d}",
            "source_row_id": source_row["row_id"],
            "segment_id": source_row["segment_id"],
            "sample_index": source_row["sample_index"],
            "t_sec_from_segment_start": source_row["t_sec_from_segment_start"],
        }
        for column_index, column in enumerate(DESIGN_COLUMNS):
            row[column] = f"{matrix[index, column_index]:.15e}"
        row.update(
            {
                "design_status": "SURROGATE_DESIGN_MATRIX_NOT_OFFICIAL",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
        rows.append(row)
    return rows


def scaled_matrix(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    norms = np.linalg.norm(matrix, axis=0)
    norms[norms == 0.0] = 1.0
    return matrix / norms, norms


def diagnostics_rows(matrix: np.ndarray, grid: dict[str, str], scales: dict[str, float]) -> list[dict[str, object]]:
    scaled, norms = scaled_matrix(matrix)
    gram = scaled.T @ scaled
    offdiag = gram - np.eye(gram.shape[0])
    rank = int(np.linalg.matrix_rank(matrix))
    singular_values = np.linalg.svd(scaled, compute_uv=False)
    condition_number = float(singular_values[0] / singular_values[-1])
    return [
        {
            "diagnostic_id": "DIAG1075_0_shape",
            "object": "design_matrix",
            "value": f"{matrix.shape[0]}x{matrix.shape[1]}",
            "units": "rows x columns",
            "interpretation": "surrogate preview design matrix shape",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "diagnostic_id": "DIAG1075_1_rank",
            "object": "matrix_rank",
            "value": rank,
            "units": "count",
            "interpretation": "full rank if rank equals 8",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "diagnostic_id": "DIAG1075_2_condition_number",
            "object": "l2_normalized_condition_number",
            "value": f"{condition_number:.12e}",
            "units": "dimensionless",
            "interpretation": "smoke diagnostic only; large values flag column degeneracy",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "diagnostic_id": "DIAG1075_3_max_abs_offdiag",
            "object": "max_abs_gram_offdiagonal",
            "value": f"{float(np.max(np.abs(offdiag))):.12e}",
            "units": "dimensionless",
            "interpretation": "orthogonality smoke check after l2 column normalization",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "diagnostic_id": "DIAG1075_4_surrogate_scale_g",
            "object": "gx_gz_scales",
            "value": f"gx={scales['gx_scale']:.12e}; gz={scales['gz_scale']:.12e}",
            "units": "m s^-2",
            "interpretation": "surrogate normalization values, not official MICROSCOPE channels",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "diagnostic_id": "DIAG1075_5_grid_source",
            "object": "full_grid_samples",
            "value": grid["full_grid_samples"],
            "units": "samples",
            "interpretation": "1074 segment-210 surrogate full-grid sample count carried forward",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def correlation_rows(matrix: np.ndarray) -> list[dict[str, object]]:
    variable_matrix = matrix[:, 1:]
    variable_columns = DESIGN_COLUMNS[1:]
    corr = np.corrcoef(variable_matrix, rowvar=False)
    rows: list[dict[str, object]] = []
    for i, left in enumerate(variable_columns):
        for j, right in enumerate(variable_columns):
            if j <= i:
                continue
            value = float(corr[i, j])
            rows.append(
                {
                    "correlation_id": f"CORR1075_{left}_{right}",
                    "left_column": left,
                    "right_column": right,
                    "pearson_r": f"{value:.12e}",
                    "abs_pearson_r": f"{abs(value):.12e}",
                    "status": "SURROGATE_CORRELATION_ONLY",
                    "valid_for_claim": "false",
                    "generated_utc": stamp(),
                }
            )
    rows.sort(key=lambda row: float(row["abs_pearson_r"]), reverse=True)
    return rows


def smoke_fit_rows(matrix: np.ndarray) -> list[dict[str, object]]:
    coeff_vector = np.array([SMOKE_TRUE_COEFFS[column] for column in DESIGN_COLUMNS], dtype=float)
    synthetic_y = matrix @ coeff_vector
    recovered, residuals, rank, singular_values = np.linalg.lstsq(matrix, synthetic_y, rcond=None)
    rows: list[dict[str, object]] = []
    for index, column in enumerate(DESIGN_COLUMNS):
        true_value = coeff_vector[index]
        recovered_value = recovered[index]
        rows.append(
            {
                "fit_id": f"FIT1075_{index}_{column}",
                "column_name": column,
                "true_smoke_coefficient": f"{true_value:.15e}",
                "recovered_smoke_coefficient": f"{recovered_value:.15e}",
                "abs_error": f"{abs(recovered_value - true_value):.15e}",
                "fit_status": "SMOKE_RECOVERY_ONLY_NOT_PHYSICAL",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    rows.append(
        {
            "fit_id": "FIT1075_summary",
            "column_name": "summary",
            "true_smoke_coefficient": "synthetic_deterministic",
            "recovered_smoke_coefficient": "least_squares",
            "abs_error": f"{float(np.max(np.abs(recovered - coeff_vector))):.15e}",
            "fit_status": f"rank={rank}; residual_norm={float(np.linalg.norm(matrix @ recovered - synthetic_y)):.15e}; singular_min={float(np.min(singular_values)):.15e}",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    )
    return rows


def replacement_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "RG1075_0_official_arrays",
            "object": "official gx/gz/Sxx/Sxz arrays",
            "required_for_claim": "true",
            "current_status": "MISSING_OFFICIAL_ARRAYS_SURROGATE_ONLY",
            "runner_policy": "block product claim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "RG1075_1_exact_masks",
            "object": "exact segment masks",
            "required_for_claim": "true",
            "current_status": "MISSING_EXACT_MASKS_SURROGATE_ALL_UNMASKED",
            "runner_policy": "block product claim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "RG1075_2_material_source_map",
            "object": "MTS material/source response map",
            "required_for_claim": "true",
            "current_status": "MISSING_PARENT_MATERIAL_SOURCE_MAP",
            "runner_policy": "block tau_WEP interpretation",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "RG1075_3_design_matrix_plumbing",
            "object": "surrogate design-matrix plumbing",
            "required_for_claim": "false",
            "current_status": "SMOKE_RUNNER_AVAILABLE",
            "runner_policy": "allowed only as pipeline diagnostic",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "RG1075_4_tau_shape",
            "object": "tau-shape smoke fit",
            "required_for_claim": "false",
            "current_status": "SYNTHETIC_RECOVERY_ONLY",
            "runner_policy": "does not define tau_WEP",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def tau_shape_status_rows(smoke_rows: list[dict[str, object]], diagnostics: list[dict[str, object]]) -> list[dict[str, str]]:
    summary = next(row for row in smoke_rows if row["fit_id"] == "FIT1075_summary")
    condition = next(row for row in diagnostics if row["diagnostic_id"] == "DIAG1075_2_condition_number")
    return [
        {
            "status_id": "TAUSHAPE1075_0_matrix_available",
            "object": "surrogate design matrix",
            "status": "AVAILABLE_NONCLAIM",
            "evidence": "P8_Y5_R10_1075_SURROGATE_DESIGN_MATRIX_SEGMENT210.csv",
            "diagnostic": f"condition={condition['value']}",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "status_id": "TAUSHAPE1075_1_smoke_recovery",
            "object": "synthetic tau-shape coefficients",
            "status": "RECOVERED_IN_SMOKE_TEST",
            "evidence": "P8_Y5_R10_1075_TAU_SHAPE_SMOKE_FIT.csv",
            "diagnostic": str(summary["fit_status"]),
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "status_id": "TAUSHAPE1075_2_physics_tau",
            "object": "physical tau_WEP",
            "status": "NOT_ACQUIRED",
            "evidence": "official arrays and parent material/source map remain missing",
            "diagnostic": "smoke recovery is not physical tau",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def product_prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1075_0_WEP_surrogate_design_matrix_tau_shape_nonclaim",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_PHYSICAL_TAU_WEP_SURROGATE_SMOKE_ONLY",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1075_TAU_SHAPE_STATUS.csv",
            "inputs_present": "surrogate_design_matrix;synthetic_tau_shape_recovery;column_diagnostics",
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
            "bound_id": "BOUND1075_0_MICROSCOPE_R1_eta_source_charge",
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


def product_status_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1075_0_WEP_surrogate_design_matrix_product_stub",
            "prediction_rows": str(status.get("prediction_rows", "")),
            "bound_rows": str(status.get("bound_rows", "")),
            "valid_prediction_rows": str(status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(status.get("valid_bound_rows", "")),
            "comparison_rows": str(status.get("comparison_rows", "")),
            "passed_rows": str(status.get("passed_rows", "")),
            "claim_allowed": str(status.get("claim_allowed", "")).lower(),
            "expected_result": "reject smoke-only surrogate product and keep claim false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1075_0_design_matrix_smoke",
            "claim_component": "surrogate design matrix",
            "gate_pass": "true",
            "claim_allowed": "false",
            "reason": "pipeline diagnostic only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1075_1_tau_shape_smoke",
            "claim_component": "synthetic tau-shape recovery",
            "gate_pass": "true",
            "claim_allowed": "false",
            "reason": "synthetic coefficients are not physical tau_WEP",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1075_2_official_arrays",
            "claim_component": "official MICROSCOPE arrays",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "MISSING_OFFICIAL_ARRAYS",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1075_3_parent_material_source_map",
            "claim_component": "parent material/source map",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "MISSING_PARENT_MATERIAL_SOURCE_MAP",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1075_4_product_runner",
            "claim_component": "WEP product runner",
            "gate_pass": "false",
            "claim_allowed": str(product_status.get("claim_allowed", "")).lower(),
            "reason": f"valid_prediction_rows={product_status.get('valid_prediction_rows')}",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows(diagnostics: list[dict[str, object]]) -> list[dict[str, str]]:
    rank = next(row for row in diagnostics if row["diagnostic_id"] == "DIAG1075_1_rank")
    condition = next(row for row in diagnostics if row["diagnostic_id"] == "DIAG1075_2_condition_number")
    return [
        {
            "decision_id": "DEC1075_0_runner_built",
            "decision": "surrogate design-matrix/tau-shape smoke runner is built",
            "evidence": f"rank={rank['value']}; condition={condition['value']}",
            "consequence": "pipeline can now test replacement gates and regression plumbing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1075_1_not_evidence",
            "decision": "do not use surrogate smoke fit as MICROSCOPE evidence",
            "evidence": "RG1075_0_official_arrays; RG1075_2_material_source_map",
            "consequence": "official-array and parent-map gates remain hard blockers",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1075_2_next_route",
            "decision": "next best route is parent material/source map derivation or official CMSM import",
            "evidence": "TAUSHAPE1075_2_physics_tau",
            "consequence": "derive WEP coupling owner rather than polishing surrogate evidence",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1075_0_1076",
            "next_target": "1076-Y5-R10-WEP-parent-material-source-map-or-official-CMSM-import-gate.md",
            "objective": "try to derive the parent material/source response map needed to turn the WEP design matrix into an MTS product, while keeping an alternative gate open for official CMSM array import if the data become available.",
            "include": "Ti/Pt material response owner; Earth/source leg; Xhat normalization; coupling coefficient ownership; official-array import gate; product-runner refusal",
            "exclude": "more surrogate polishing as evidence; tau=1; Delta_w=0 by taste; measured-G absorption; public WEP/local-GR claim; GitHub; formalization edits",
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
    schema_rows: list[dict[str, str]],
    matrix_rows: list[dict[str, object]],
    diagnostics: list[dict[str, object]],
    corr_rows: list[dict[str, object]],
    smoke_rows: list[dict[str, object]],
    replacement_rows: list[dict[str, str]],
    tau_rows: list[dict[str, str]],
    prediction_rows: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rank_row = next(row for row in diagnostics if row["diagnostic_id"] == "DIAG1075_1_rank")
    condition_row = next(row for row in diagnostics if row["diagnostic_id"] == "DIAG1075_2_condition_number")
    smoke_summary = next(row for row in smoke_rows if row["fit_id"] == "FIT1075_summary")
    max_smoke_error = float(smoke_summary["abs_error"])
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V1075_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in source_rows), "all cited local source paths and needles are present"))
    checks.append(("V1075_1_schema_complete", {row["column_name"] for row in schema_rows} == set(DESIGN_COLUMNS), "design schema has all expected columns"))
    checks.append(("V1075_2_matrix_rows", len(matrix_rows) == 256 and all(row["valid_for_claim"] == "false" for row in matrix_rows), "256 surrogate design-matrix rows written and nonclaim"))
    checks.append(("V1075_3_rank_condition", int(rank_row["value"]) == len(DESIGN_COLUMNS) and math.isfinite(float(condition_row["value"])), "design matrix is finite and full-rank for smoke purposes"))
    checks.append(("V1075_4_correlations", len(corr_rows) == 21 and all(row["valid_for_claim"] == "false" for row in corr_rows), "all non-constant column pair correlations written"))
    checks.append(("V1075_5_smoke_recovery", max_smoke_error < 1.0e-25 and all(row["valid_for_claim"] == "false" for row in smoke_rows), "synthetic coefficient recovery works but remains nonclaim"))
    checks.append(("V1075_6_replacement_gates", any(row["gate_id"] == "RG1075_0_official_arrays" and row["current_status"] == "MISSING_OFFICIAL_ARRAYS_SURROGATE_ONLY" for row in replacement_rows), "official-array replacement gate remains closed"))
    checks.append(("V1075_7_physical_tau_blocked", any(row["status_id"] == "TAUSHAPE1075_2_physics_tau" and row["status"] == "NOT_ACQUIRED" for row in tau_rows), "physical tau_WEP remains not acquired"))
    checks.append(("V1075_8_prediction_nonclaim_missing", any("MISSING_PHYSICAL_TAU_WEP" in row["product_value"] and row["valid_for_claim"] == "false" for row in prediction_rows), "prediction row remains missing physical tau"))
    checks.append(("V1075_9_bound_numeric", bool(bound_rows_) and float(bound_rows_[0]["bound_value"]) > 0 and bound_rows_[0]["valid_for_claim"] == "true", "bound import is positive numeric"))
    checks.append(("V1075_10_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "runner reports no valid prediction rows and claim false"))
    checks.append(("V1075_11_claim_gates_safe", all(row["claim_allowed"] == "false" for row in claim_rows), "all claim gates deny WEP/local-GR claim"))
    checks.append(("V1075_12_next_target", any("1076-Y5-R10-WEP-parent-material-source-map-or-official-CMSM-import-gate.md" in row["next_target"] for row in next_rows), "1076 handoff written"))
    generated_paths = list(outputs.values()) + [DOC]
    checks.append(("V1075_13_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    checks.append(("V1075_14_csv_parse", all(path.exists() and csv_rows_parse(path) for path in outputs.values() if path.suffix == ".csv" and path.name != "P8_Y5_BRR545_1075_VALIDATION.csv"), "all 1075 CSV outputs parse cleanly"))
    checks.append(("V1075_15_formalization_untouched", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains zero"))
    checks.append(("V1075_SUMMARY", True, "surrogate design-matrix/tau-shape smoke runner built; physical WEP/product claim blocked"))
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
    schema_rows: list[dict[str, str]],
    matrix_rows: list[dict[str, object]],
    diagnostics: list[dict[str, object]],
    corr_rows: list[dict[str, object]],
    smoke_rows: list[dict[str, object]],
    replacement_rows: list[dict[str, str]],
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
            "# 1075 - Surrogate design-matrix tau-shape smoke runner",
            "",
            "## Current verdict",
            "1075 builds a working surrogate design-matrix/tau-shape smoke runner for SUEP segment 210. It verifies regression plumbing, column diagnostics, and synthetic coefficient recovery, but it still has zero WEP/local-GR evidential force because official MICROSCOPE arrays and the MTS parent material/source map remain missing.",
            "",
            "## Local source register",
            md_table(source_rows, ["source_id", "relative_path", "exists", "needle_found", "note"]),
            "## Design matrix schema",
            md_table(schema_rows, ["column_id", "column_name", "definition", "normalization", "source_status"]),
            "## Matrix diagnostics",
            md_table(diagnostics, ["diagnostic_id", "object", "value", "units", "interpretation"]),
            "## Top column correlations",
            md_table(corr_rows[:10], ["correlation_id", "left_column", "right_column", "pearson_r", "abs_pearson_r"]),
            "## Tau-shape smoke fit",
            md_table(smoke_rows, ["fit_id", "column_name", "true_smoke_coefficient", "recovered_smoke_coefficient", "abs_error", "fit_status"]),
            "## Design matrix preview",
            md_table(matrix_rows[:8], ["matrix_row_id", "sample_index", "poly0", "poly1", "gx_shape", "gz_shape", "Sxx_shape", "Sxz_shape"]),
            "## Replacement gates",
            md_table(replacement_rows, ["gate_id", "object", "current_status", "runner_policy"]),
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
            md_table(validation_rows, ["check_id", "result", "detail"]),
            "## Next target",
            md_table(next_rows, ["next_id", "next_target", "objective", "include", "exclude"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    surrogate_rows, grid, matrix, scales = load_surrogate_arrays()
    schema_rows = design_schema_rows(scales)
    matrix_rows = design_matrix_rows(surrogate_rows, matrix)
    diagnostics = diagnostics_rows(matrix, grid, scales)
    corr_rows = correlation_rows(matrix)
    smoke_rows = smoke_fit_rows(matrix)
    replacement_rows = replacement_gate_rows()
    tau_rows = tau_shape_status_rows(smoke_rows, diagnostics)
    prediction_rows = product_prediction_rows()
    bound_rows_ = bound_rows()
    decisions = decision_rows(diagnostics)
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R10_1075_SOURCE_REGISTER.csv",
        "schema": OUT / "P8_Y5_R10_1075_DESIGN_MATRIX_SCHEMA.csv",
        "matrix": OUT / "P8_Y5_R10_1075_SURROGATE_DESIGN_MATRIX_SEGMENT210.csv",
        "diagnostics": OUT / "P8_Y5_R10_1075_MATRIX_DIAGNOSTICS.csv",
        "correlations": OUT / "P8_Y5_R10_1075_COLUMN_CORRELATION_PAIRS.csv",
        "smoke_fit": OUT / "P8_Y5_R10_1075_TAU_SHAPE_SMOKE_FIT.csv",
        "replacement_gates": OUT / "P8_Y5_R10_1075_REPLACEMENT_GATES.csv",
        "tau_status": OUT / "P8_Y5_R10_1075_TAU_SHAPE_STATUS.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1075_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1075_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1075_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1075_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1075_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1075_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["schema"], schema_rows)
    write_csv(outputs["matrix"], matrix_rows)
    write_csv(outputs["diagnostics"], diagnostics)
    write_csv(outputs["correlations"], corr_rows)
    write_csv(outputs["smoke_fit"], smoke_rows)
    write_csv(outputs["replacement_gates"], replacement_rows)
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
        schema_rows,
        matrix_rows,
        diagnostics,
        corr_rows,
        smoke_rows,
        replacement_rows,
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
        schema_rows,
        matrix_rows,
        diagnostics,
        corr_rows,
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

    failed = [row for row in validation_rows if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
