from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np


RUN_STARTED_UTC = datetime.now(timezone.utc)
ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
WORK = ROOT / "post-checkpoint-work"
MTS = WORK / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = WORK / "source-intake" / "local_bounds"
RAB_QUEUE = WORK / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = WORK / "source-intake" / "beta-source" / "docs"
MICROSCOPE_DIR = WORK / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SCRIPTS = WORK / "scripts"
FORMALIZATION = ROOT / "formalization-workbench"
DOC = WORK / "2781-Y5-R2FR-surrogate-design-matrix-tau-shape-smoke-runner-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2781_SOURCE_REGISTER.csv",
    "schema": MTS / "P8_Y5_R2FR_2781_DESIGN_MATRIX_SCHEMA.csv",
    "matrix": MTS / "P8_Y5_R2FR_2781_SURROGATE_DESIGN_MATRIX_SEGMENT210.csv",
    "diagnostics": MTS / "P8_Y5_R2FR_2781_MATRIX_DIAGNOSTICS.csv",
    "correlations": MTS / "P8_Y5_R2FR_2781_COLUMN_CORRELATION_PAIRS.csv",
    "fit": MTS / "P8_Y5_R2FR_2781_TAU_SHAPE_SMOKE_FIT.csv",
    "replacement": MTS / "P8_Y5_R2FR_2781_REPLACEMENT_GATES.csv",
    "tau": MTS / "P8_Y5_R2FR_2781_TAU_SHAPE_STATUS.csv",
    "candidate": MTS / "P8_Y5_R2FR_2781_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv",
    "bounds": MTS / "P8_Y5_R2FR_2781_WEP_BOUND_IMPORT.csv",
    "runner": MTS / "P8_Y5_R2FR_2781_PRODUCT_RUNNER_STATUS.csv",
    "comparisons": MTS / "P8_Y5_R2FR_2781_PRODUCT_COMPARISON_ROWS.csv",
    "gates": MTS / "P8_Y5_R2FR_2781_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2781_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2781_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2781_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2781_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "matrix_queue": RAB_QUEUE / "JR2781_SURROGATE_DESIGN_MATRIX_DIAGNOSTICS_NONCLAIM.csv",
    "gate_queue": RAB_QUEUE / "JR2781_REPLACEMENT_AND_PARENT_GATES_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "MICROSCOPE_SURROGATE_TAU_SHAPE_2781_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_surrogate_tau_shape_2781_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2781_PARENT_WEP_COUPLING_OWNER_NEXT.csv",
}

COLUMN_NAMES = ["poly0", "poly1", "poly2", "poly3", "gx_shape", "gz_shape", "Sxx_shape", "Sxz_shape"]
SMOKE_COEFFICIENTS = {
    "poly0": 0.0,
    "poly1": 0.0,
    "poly2": 0.0,
    "poly3": 0.0,
    "gx_shape": 1.0e-15,
    "gz_shape": -2.0e-16,
    "Sxx_shape": 1.5e-16,
    "Sxz_shape": -7.5e-17,
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
        ("SRC2781_00_2780_next", "2780_next", MTS / "P8_Y5_R2FR_2780_NEXT_TARGET.csv", "NEXT2780_0_2781", "current handoff into surrogate design-matrix smoke runner"),
        ("SRC2781_01_2780_validation", "2780_validation", MTS / "P8_Y5_BRR545_2780_VALIDATION.csv", "VAL2780_OVERALL", "current validation baseline"),
        ("SRC2781_02_2780_grid", "2780_grid", MTS / "P8_Y5_R2FR_2780_SURROGATE_GRID_METADATA_SEGMENT210.csv", "GRID2780_0_segment210_surrogate", "current surrogate grid metadata"),
        ("SRC2781_03_2780_preview", "2780_preview", MTS / "P8_Y5_R2FR_2780_SURROGATE_GXS_PREVIEW_SEGMENT210.csv", "SUR2780_210_255", "current surrogate gxS rows"),
        ("SRC2781_04_2780_replacement", "2780_replacement", MTS / "P8_Y5_R2FR_2780_SURROGATE_TO_OFFICIAL_REPLACEMENT_MAP.csv", "MAP2780_4_mask", "current replacement map"),
        ("SRC2781_05_2780_status", "2780_status", MTS / "P8_Y5_R2FR_2780_SURROGATE_STATUS_LEDGER.csv", "STAT2780_3_tau_WEP", "current physical tau blocker"),
        ("SRC2781_06_2779_array_contract", "2779_array_contract", MTS / "P8_Y5_R2FR_2779_OFFICIAL_ARRAY_SCHEMA_CONTRACT.csv", "ARR2779_7_generation_method", "current official-array schema contract"),
        ("SRC2781_07_1075_doc", "1075_doc", WORK / "1075-Y5-R10-surrogate-design-matrix-tau-shape-smoke-runner.md", "Tau-shape smoke fit", "R10 precedent for design matrix diagnostics"),
        ("SRC2781_08_1076_next", "1076_next", MTS / "P8_Y5_R10_1076_NEXT_TARGET.csv", "NEXT1076_0_1077", "R10 precedent for next parent coupling-owner route"),
        ("SRC2781_09_local_bounds", "local_bounds", LOCAL_BOUNDS / "local_bound_claims.csv", "R1_WEP_source_charge", "local MICROSCOPE WEP bound source row"),
    ]
    return [source_row(*spec) for spec in specs]


def build_schema_rows() -> list[dict[str, Any]]:
    rows = [
        ("DM2781_0_poly0", "poly0", "constant offset column", "always present", "surrogate_design_matrix"),
        ("DM2781_1_poly1", "poly1", "centered linear drift over segment preview", "x in [-1,1] from preview row order", "surrogate_design_matrix"),
        ("DM2781_2_poly2", "poly2", "centered quadratic drift over segment preview", "x^2", "surrogate_design_matrix"),
        ("DM2781_3_poly3", "poly3", "centered cubic drift over segment preview", "x^3", "surrogate_design_matrix"),
        ("DM2781_4_gx_shape", "gx_shape", "normalized surrogate gx column", "gx_surrogate_m_s2/max_abs_gx", "SURROGATE_ONLY"),
        ("DM2781_5_gz_shape", "gz_shape", "normalized surrogate gz column", "gz_surrogate_m_s2/max_abs_gz", "SURROGATE_ONLY"),
        ("DM2781_6_Sxx_shape", "Sxx_shape", "normalized surrogate Sxx column", "Sxx_surrogate_s2/max_abs_Sxx", "SURROGATE_ONLY"),
        ("DM2781_7_Sxz_shape", "Sxz_shape", "normalized surrogate Sxz column", "Sxz_surrogate_s2/max_abs_Sxz", "SURROGATE_ONLY"),
    ]
    return [
        nonclaim({"column_id": column_id, "column_name": name, "definition": definition, "normalization": normalization, "source_status": source_status})
        for column_id, name, definition, normalization, source_status in rows
    ]


def load_surrogate_preview() -> list[dict[str, str]]:
    return read_csv_rows(MTS / "P8_Y5_R2FR_2780_SURROGATE_GXS_PREVIEW_SEGMENT210.csv")


def build_matrix(preview_rows: list[dict[str, str]]) -> tuple[np.ndarray, dict[str, float], list[dict[str, Any]]]:
    n_rows = len(preview_rows)
    gx = np.array([float(row["gx_surrogate_m_s2"]) for row in preview_rows], dtype=float)
    gz = np.array([float(row["gz_surrogate_m_s2"]) for row in preview_rows], dtype=float)
    sxx = np.array([float(row["Sxx_surrogate_s2"]) for row in preview_rows], dtype=float)
    sxz = np.array([float(row["Sxz_surrogate_s2"]) for row in preview_rows], dtype=float)
    x = np.linspace(-1.0, 1.0, n_rows)
    scales = {
        "gx": float(np.max(np.abs(gx))),
        "gz": float(np.max(np.abs(gz))),
        "Sxx": float(np.max(np.abs(sxx))),
        "Sxz": float(np.max(np.abs(sxz))),
    }
    columns = [
        np.ones(n_rows),
        x,
        x**2,
        x**3,
        gx / scales["gx"],
        gz / scales["gz"],
        sxx / scales["Sxx"],
        sxz / scales["Sxz"],
    ]
    matrix = np.column_stack(columns)
    rows: list[dict[str, Any]] = []
    for index, source in enumerate(preview_rows):
        row = {
            "matrix_row_id": f"DMROW2781_{index:03d}",
            "segment": source.get("segment", "210"),
            "sample_index": source.get("sample_index", ""),
            "t_sec_from_segment_start": source.get("t_sec_from_segment_start", ""),
        }
        for col_index, name in enumerate(COLUMN_NAMES):
            row[name] = f"{matrix[index, col_index]:.15e}"
        row["source_status"] = "SURROGATE_DESIGN_MATRIX_ONLY"
        rows.append(nonclaim(row))
    return matrix, scales, rows


def normalized_matrix(matrix: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(matrix, axis=0)
    norms[norms == 0.0] = 1.0
    return matrix / norms


def build_diagnostics(matrix: np.ndarray, scales: dict[str, float]) -> list[dict[str, Any]]:
    normalized = normalized_matrix(matrix)
    singular_values = np.linalg.svd(normalized, compute_uv=False)
    rank = int(np.linalg.matrix_rank(normalized))
    condition_number = float(singular_values[0] / singular_values[-1])
    gram = normalized.T @ normalized
    offdiag = gram - np.eye(gram.shape[0])
    max_offdiag = float(np.max(np.abs(offdiag)))
    return [
        nonclaim({"diagnostic_id": "DIAG2781_0_shape", "object": "design_matrix", "value": f"{matrix.shape[0]}x{matrix.shape[1]}", "units": "rows x columns", "interpretation": "surrogate preview design matrix shape"}),
        nonclaim({"diagnostic_id": "DIAG2781_1_rank", "object": "matrix_rank", "value": rank, "units": "count", "interpretation": "full rank if rank equals 8"}),
        nonclaim({"diagnostic_id": "DIAG2781_2_condition_number", "object": "l2_normalized_condition_number", "value": f"{condition_number:.12e}", "units": "dimensionless", "interpretation": "smoke diagnostic only; large values flag column degeneracy"}),
        nonclaim({"diagnostic_id": "DIAG2781_3_max_abs_offdiag", "object": "max_abs_gram_offdiagonal", "value": f"{max_offdiag:.12e}", "units": "dimensionless", "interpretation": "orthogonality smoke check after l2 column normalization"}),
        nonclaim({"diagnostic_id": "DIAG2781_4_surrogate_scale_g", "object": "gx_gz_scales", "value": f"gx={scales['gx']:.12e}; gz={scales['gz']:.12e}", "units": "m s^-2", "interpretation": "surrogate normalization values, not official MICROSCOPE channels"}),
        nonclaim({"diagnostic_id": "DIAG2781_5_surrogate_scale_S", "object": "Sxx_Sxz_scales", "value": f"Sxx={scales['Sxx']:.12e}; Sxz={scales['Sxz']:.12e}", "units": "s^-2", "interpretation": "surrogate gradient normalization values"}),
    ]


def build_correlations(matrix: np.ndarray) -> list[dict[str, Any]]:
    nonconstant_indices = [index for index, name in enumerate(COLUMN_NAMES) if name != "poly0"]
    centered = matrix[:, nonconstant_indices] - np.mean(matrix[:, nonconstant_indices], axis=0)
    corr = np.corrcoef(centered, rowvar=False)
    pairs: list[dict[str, Any]] = []
    for left_pos, left_index in enumerate(nonconstant_indices):
        for right_pos in range(left_pos + 1, len(nonconstant_indices)):
            right_index = nonconstant_indices[right_pos]
            value = float(corr[left_pos, right_pos])
            pairs.append(nonclaim({
                "correlation_id": f"CORR2781_{COLUMN_NAMES[left_index]}_{COLUMN_NAMES[right_index]}",
                "left_column": COLUMN_NAMES[left_index],
                "right_column": COLUMN_NAMES[right_index],
                "pearson_r": f"{value:.12e}",
                "abs_pearson_r": f"{abs(value):.12e}",
            }))
    pairs.sort(key=lambda row: float(row["abs_pearson_r"]), reverse=True)
    return pairs[:10]


def build_smoke_fit(matrix: np.ndarray) -> list[dict[str, Any]]:
    true_vector = np.array([SMOKE_COEFFICIENTS[name] for name in COLUMN_NAMES], dtype=float)
    synthetic = matrix @ true_vector
    recovered, residuals, rank, singular_values = np.linalg.lstsq(matrix, synthetic, rcond=None)
    rows: list[dict[str, Any]] = []
    max_error = 0.0
    for index, name in enumerate(COLUMN_NAMES):
        abs_error = abs(float(recovered[index] - true_vector[index]))
        max_error = max(max_error, abs_error)
        rows.append(nonclaim({
            "fit_id": f"FIT2781_{index}_{name}",
            "column_name": name,
            "true_smoke_coefficient": f"{true_vector[index]:.15e}",
            "recovered_smoke_coefficient": f"{recovered[index]:.15e}",
            "abs_error": f"{abs_error:.15e}",
            "fit_status": "SMOKE_RECOVERY_ONLY_NOT_PHYSICAL",
        }))
    residual_norm = float(np.linalg.norm(matrix @ recovered - synthetic))
    rows.append(nonclaim({
        "fit_id": "FIT2781_summary",
        "column_name": "summary",
        "true_smoke_coefficient": "synthetic_deterministic",
        "recovered_smoke_coefficient": "least_squares",
        "abs_error": f"{max_error:.15e}",
        "fit_status": f"rank={int(rank)}; residual_norm={residual_norm:.15e}; singular_min={float(np.min(singular_values)):.15e}",
    }))
    return rows


def build_replacement_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"gate_id": "RG2781_0_official_arrays", "object": "official gx/gz/Sxx/Sxz arrays", "required_for_claim": True, "current_status": "MISSING_OFFICIAL_ARRAYS_SURROGATE_ONLY", "runner_policy": "block product claim"}),
        nonclaim({"gate_id": "RG2781_1_exact_masks", "object": "exact segment masks", "required_for_claim": True, "current_status": "MISSING_EXACT_MASKS_SURROGATE_ALL_UNMASKED", "runner_policy": "block product claim"}),
        nonclaim({"gate_id": "RG2781_2_material_source_map", "object": "MTS material/source response map", "required_for_claim": True, "current_status": "MISSING_PARENT_MATERIAL_SOURCE_MAP", "runner_policy": "block tau_WEP interpretation"}),
        nonclaim({"gate_id": "RG2781_3_design_matrix_plumbing", "object": "surrogate design-matrix plumbing", "required_for_claim": False, "current_status": "SMOKE_RUNNER_AVAILABLE", "runner_policy": "allowed only as pipeline diagnostic"}),
        nonclaim({"gate_id": "RG2781_4_tau_shape", "object": "tau-shape smoke fit", "required_for_claim": False, "current_status": "SYNTHETIC_RECOVERY_ONLY", "runner_policy": "does not define tau_WEP"}),
    ]


def build_tau_rows(diagnostics: list[dict[str, Any]], fit_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    condition = next(row["value"] for row in diagnostics if row["diagnostic_id"] == "DIAG2781_2_condition_number")
    summary = next(row for row in fit_rows if row["fit_id"] == "FIT2781_summary")
    return [
        nonclaim({"status_id": "TAUSHAPE2781_0_matrix_available", "object": "surrogate design matrix", "status": "AVAILABLE_NONCLAIM", "diagnostic": f"condition={condition}", "claim_allowed": False}),
        nonclaim({"status_id": "TAUSHAPE2781_1_smoke_recovery", "object": "synthetic tau-shape coefficients", "status": "RECOVERED_IN_SMOKE_TEST", "diagnostic": summary["fit_status"], "claim_allowed": False}),
        nonclaim({"status_id": "TAUSHAPE2781_2_physics_tau", "object": "physical tau_WEP", "status": "NOT_ACQUIRED", "diagnostic": "smoke recovery is not physical tau", "claim_allowed": False}),
    ]


def build_candidate_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "prediction_id": "PRED2781_0_WEP_surrogate_design_matrix_tau_shape_nonclaim",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_PHYSICAL_TAU_WEP_SURROGATE_SMOKE_ONLY",
            "product_units": "dimensionless",
            "derivation_status": "SMOKE_PLUMBING_ONLY_NO_PHYSICS_PRODUCT",
            "notes": "synthetic recovery verifies matrix plumbing only; it is not official MICROSCOPE evidence and not an MTS tau_WEP prediction",
        })
    ]


def build_bound_rows() -> list[dict[str, Any]]:
    bound = get_local_bound("R1_WEP_source_charge")
    return [
        nonclaim({
            "bound_id": "BOUND2781_0_MICROSCOPE_R1_eta_source_charge",
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
            "runner_id": "APR2781_0_WEP_surrogate_design_matrix_product_stub",
            "prediction_rows": len(predictions),
            "bound_rows": len(bounds),
            "valid_prediction_rows": len(valid_predictions),
            "valid_bound_rows": len(valid_bounds),
            "claim_allowed": False,
            "expected_result": "reject smoke-only surrogate product and keep claim false",
        })
    ]
    return runner, comparisons


def build_gates() -> list[dict[str, Any]]:
    return [
        nonclaim({"gate_id": "CG2781_0_design_matrix_smoke", "claim_component": "surrogate design matrix", "gate_pass": True, "claim_allowed": False, "reason": "pipeline diagnostic only"}),
        nonclaim({"gate_id": "CG2781_1_tau_shape_smoke", "claim_component": "synthetic tau-shape recovery", "gate_pass": True, "claim_allowed": False, "reason": "synthetic coefficients are not physical tau_WEP"}),
        nonclaim({"gate_id": "CG2781_2_official_arrays", "claim_component": "official MICROSCOPE arrays", "gate_pass": False, "claim_allowed": False, "reason": "MISSING_OFFICIAL_ARRAYS"}),
        nonclaim({"gate_id": "CG2781_3_parent_material_source_map", "claim_component": "parent material/source map", "gate_pass": False, "claim_allowed": False, "reason": "MISSING_PARENT_MATERIAL_SOURCE_MAP"}),
        nonclaim({"gate_id": "CG2781_4_product_runner", "claim_component": "WEP product runner", "gate_pass": False, "claim_allowed": False, "reason": "valid_prediction_rows=0"}),
    ]


def build_decision_rows(diagnostics: list[dict[str, Any]]) -> list[dict[str, Any]]:
    condition = next(row["value"] for row in diagnostics if row["diagnostic_id"] == "DIAG2781_2_condition_number")
    rank = next(row["value"] for row in diagnostics if row["diagnostic_id"] == "DIAG2781_1_rank")
    return [
        nonclaim({"decision_id": "DEC2781_0_runner_built", "decision": "surrogate design-matrix/tau-shape smoke runner is built in the R2/f(R) branch", "evidence": f"rank={rank}; condition={condition}", "consequence": "pipeline can now test replacement gates and regression plumbing"}),
        nonclaim({"decision_id": "DEC2781_1_not_evidence", "decision": "do not use surrogate smoke fit as MICROSCOPE evidence", "evidence": "RG2781_0_official_arrays; RG2781_2_material_source_map", "consequence": "official-array and parent-map gates remain hard blockers"}),
        nonclaim({"decision_id": "DEC2781_2_next_route", "decision": "next best route is parent material/source coupling-owner theorem or official CMSM import", "evidence": "TAUSHAPE2781_2_physics_tau", "consequence": "derive WEP coupling owner rather than polishing surrogate evidence"}),
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "row_id": "NEXT2781_0_2782",
            "next_target": "2782-Y5-R2FR-WEP-parent-material-source-map-or-official-CMSM-import-gate-under-AX1090.md",
            "script": "scripts/Y5_R2FR_WEP_parent_material_source_map_or_official_CMSM_import_gate_under_AX1090_2782.py",
            "objective": "try to derive the parent material/source response map needed to turn the WEP design matrix into an MTS product, while keeping an alternative gate open for official CMSM array import if the data become available",
            "include": "Ti/Pt material response owner; Earth/source leg; Xhat normalization; coupling coefficient ownership; official-array import gate; product-runner refusal",
            "exclude": "more surrogate polishing as evidence; tau=1; Delta_w=0 by taste; measured-G absorption; public WEP/local-GR claim; GitHub; formalization edits",
        })
    ]


def copy_branch_outputs(
    schema: list[dict[str, Any]],
    matrix_rows: list[dict[str, Any]],
    diagnostics: list[dict[str, Any]],
    correlations: list[dict[str, Any]],
    fit: list[dict[str, Any]],
    replacement: list[dict[str, Any]],
    tau: list[dict[str, Any]],
    candidate: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    matrix_queue_rows = schema + diagnostics + correlations + fit + matrix_rows[:16]
    gate_rows = replacement + tau + candidate + gates
    beta_rows = diagnostics + fit + tau + next_rows
    microscope_rows = schema + matrix_rows + diagnostics + correlations + fit + replacement + tau + candidate + next_rows
    specs = [
        ("BR2781_0_matrix_queue", "matrix", matrix_queue_rows, OUTPUTS["diagnostics"], BRANCH_OUTPUTS["matrix_queue"], "surrogate design-matrix diagnostics nonclaim copy"),
        ("BR2781_1_gate_queue", "gates", gate_rows, OUTPUTS["replacement"], BRANCH_OUTPUTS["gate_queue"], "replacement and parent gates nonclaim copy"),
        ("BR2781_2_beta_doc", "beta_doc", beta_rows, OUTPUTS["tau"], BRANCH_OUTPUTS["beta_doc"], "beta/source-facing tau-shape smoke copy"),
        ("BR2781_3_microscope_copy", "microscope", microscope_rows, OUTPUTS["candidate"], BRANCH_OUTPUTS["microscope_copy"], "MICROSCOPE surrogate tau-shape smoke copy"),
        ("BR2781_4_next_queue", "next", next_rows, OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next parent coupling-owner route"),
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


def build_validation(rows_by_name: dict[str, list[dict[str, Any]]], matrix: np.ndarray, csv_paths: list[Path]) -> list[dict[str, Any]]:
    sources = rows_by_name["sources"]
    schema = rows_by_name["schema"]
    matrix_rows = rows_by_name["matrix"]
    diagnostics = rows_by_name["diagnostics"]
    correlations = rows_by_name["correlations"]
    fit = rows_by_name["fit"]
    replacement = rows_by_name["replacement"]
    tau = rows_by_name["tau"]
    candidate = rows_by_name["candidate"]
    bounds = rows_by_name["bounds"]
    runner = rows_by_name["runner"]
    gates = rows_by_name["gates"]
    next_rows = rows_by_name["next"]
    branches = rows_by_name["branches"]
    rank = int(next(row["value"] for row in diagnostics if row["diagnostic_id"] == "DIAG2781_1_rank"))
    condition = float(next(row["value"] for row in diagnostics if row["diagnostic_id"] == "DIAG2781_2_condition_number"))
    fit_summary = next(row for row in fit if row["fit_id"] == "FIT2781_summary")
    checks = [
        ("VAL2781_0_sources", all(row["exists"] and row["needle_found"] for row in sources), "every cited source path exists and source needle was found"),
        ("VAL2781_1_schema_complete", len(schema) == 8 and [row["column_name"] for row in schema] == COLUMN_NAMES, "design schema has all expected columns"),
        ("VAL2781_2_matrix_rows", len(matrix_rows) == 256 and all(row["valid_for_claim"] is False for row in matrix_rows), "256 surrogate design-matrix rows written and nonclaim"),
        ("VAL2781_3_rank_condition", np.all(np.isfinite(matrix)) and rank == 8 and condition < 100.0, "design matrix is finite and full-rank for smoke purposes"),
        ("VAL2781_4_correlations", len(correlations) == 10 and all(is_numeric(row["pearson_r"]) for row in correlations), "top non-constant column pair correlations written"),
        ("VAL2781_5_smoke_recovery", "rank=8" in fit_summary["fit_status"] and float(fit_summary["abs_error"]) < 1.0e-28, "synthetic coefficient recovery works but remains nonclaim"),
        ("VAL2781_6_replacement_gates", len(replacement) == 5 and any(row["gate_id"] == "RG2781_0_official_arrays" and row["current_status"] == "MISSING_OFFICIAL_ARRAYS_SURROGATE_ONLY" for row in replacement), "official-array replacement gate remains closed"),
        ("VAL2781_7_physical_tau_blocked", any(row["status_id"] == "TAUSHAPE2781_2_physics_tau" and row["status"] == "NOT_ACQUIRED" and row["claim_allowed"] is False for row in tau), "physical tau_WEP remains not acquired"),
        ("VAL2781_8_prediction_nonclaim_missing", len(candidate) == 1 and candidate[0]["valid_for_claim"] is False and has_missing_marker(candidate[0]), "prediction row remains missing physical tau"),
        ("VAL2781_9_bound_numeric", len(bounds) == 1 and is_numeric(bounds[0]["bound_value"]) and float(str(bounds[0]["bound_value"])) > 0.0 and bounds[0]["bound_valid_for_internal_runner"] is True, "bound import is positive numeric"),
        ("VAL2781_10_runner_refuses", runner[0]["valid_prediction_rows"] == 0 and runner[0]["claim_allowed"] is False, "runner reports no valid prediction rows and claim false"),
        ("VAL2781_11_claim_gates_safe", all(row["claim_allowed"] is False for row in gates) and any(row["gate_id"] == "CG2781_0_design_matrix_smoke" and row["gate_pass"] is True for row in gates), "all claim gates deny WEP/local-GR claim"),
        ("VAL2781_12_next_target", any(row["row_id"] == "NEXT2781_0_2782" and "WEP-parent-material-source-map" in row["next_target"] for row in next_rows), "next target selects parent material/source map or official CMSM import gate"),
        ("VAL2781_13_branch_outputs", all(row["exists"] and int(row["row_count"]) > 0 for row in branches), "branch copies exist and contain rows"),
        ("VAL2781_14_csv_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2781_15_no_claim_flags", no_claim_flags(rows_by_name), "no generated row is valid_for_claim=true/claim_allowed=true/pass_for_claim=true"),
        ("VAL2781_16_generated_under_post_checkpoint", generated_files_under_work(), "all generated outputs are under post-checkpoint-work"),
        ("VAL2781_17_formalization_untouched", formalization_untouched(), "formalization-workbench modified-file count remains zero during this run"),
        ("VAL2781_18_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for check_id, passed, detail in checks]
    rows.append({
        "validation_id": "VAL2781_OVERALL",
        "passed": all(row["passed"] for row in rows),
        "detail": "2781 builds a working nonclaim surrogate design-matrix/tau-shape smoke runner for SUEP segment 210 in the R2/f(R) branch. Regression plumbing, rank/condition diagnostics, correlation checks, and synthetic coefficient recovery pass. Official MICROSCOPE arrays, exact masks, and parent material/source map remain missing, so WEP/local-GR claims stay blocked and 2782 targets the coupling-owner/material-source map gate.",
        "timestamp_utc": ts(),
    })
    return rows


def build_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join([
        "# 2781 - Y5 R2/f(R): Surrogate Design-Matrix Tau-Shape Smoke Runner Under AX1090",
        "## Private Verdict\n\n2781 builds the surrogate MICROSCOPE design-matrix/tau-shape smoke runner in the live R2/f(R) branch. The matrix is full-rank, synthetic coefficient recovery works, and the replacement gates are explicit. This is useful plumbing, not evidence: official MICROSCOPE arrays, exact masks, and the parent material/source map are still missing, so WEP/local-GR claims remain blocked.",
        "## Source Register\n\n" + markdown_table(rows_by_name["sources"], ["row_id", "source_key", "source_path", "exists", "needle_found", "source_role", "valid_for_claim"]),
        "## Design Matrix Schema\n\n" + markdown_table(rows_by_name["schema"], ["column_id", "column_name", "definition", "normalization", "source_status", "valid_for_claim"]),
        "## Matrix Diagnostics\n\n" + markdown_table(rows_by_name["diagnostics"], ["diagnostic_id", "object", "value", "units", "interpretation", "valid_for_claim"]),
        "## Top Column Correlations\n\n" + markdown_table(rows_by_name["correlations"], ["correlation_id", "left_column", "right_column", "pearson_r", "abs_pearson_r", "valid_for_claim"]),
        "## Tau-Shape Smoke Fit\n\n" + markdown_table(rows_by_name["fit"], ["fit_id", "column_name", "true_smoke_coefficient", "recovered_smoke_coefficient", "abs_error", "fit_status", "valid_for_claim"]),
        "## Design Matrix Preview\n\n" + markdown_table(rows_by_name["matrix"][:8], ["matrix_row_id", "sample_index", "poly0", "poly1", "gx_shape", "gz_shape", "Sxx_shape", "Sxz_shape", "valid_for_claim"]) + "\n\n_Only the first 8 of 256 design rows are shown here; the full CSV is written separately._",
        "## Replacement Gates\n\n" + markdown_table(rows_by_name["replacement"], ["gate_id", "object", "required_for_claim", "current_status", "runner_policy", "valid_for_claim"]),
        "## Tau-Shape Status\n\n" + markdown_table(rows_by_name["tau"], ["status_id", "object", "status", "diagnostic", "claim_allowed", "valid_for_claim"]),
        "## Nonclaim Product Candidate\n\n" + markdown_table(rows_by_name["candidate"], ["prediction_id", "arena", "product_symbol", "product_value", "product_units", "derivation_status", "notes", "valid_for_claim"]),
        "## Bound Import\n\n" + markdown_table(rows_by_name["bounds"], ["bound_id", "arena", "product_symbol", "bound_value", "bound_units", "bound_type", "source_row_id", "bound_valid_for_internal_runner", "valid_for_claim"]),
        "## Product Runner Status\n\n" + markdown_table(rows_by_name["runner"], ["runner_id", "prediction_rows", "bound_rows", "valid_prediction_rows", "valid_bound_rows", "claim_allowed", "expected_result", "valid_for_claim"]),
        "## Product Comparison Rows\n\n" + markdown_table(rows_by_name["comparisons"], ["comparison_id", "comparison_status", "pass_for_claim", "issues", "valid_for_claim"]),
        "## Claim Gates\n\n" + markdown_table(rows_by_name["gates"], ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason", "valid_for_claim"]),
        "## Decision Ledger\n\n" + markdown_table(rows_by_name["decision"], ["decision_id", "decision", "evidence", "consequence", "valid_for_claim"]),
        "## Next Target\n\n" + markdown_table(rows_by_name["next"], ["row_id", "next_target", "script", "objective", "include", "exclude", "valid_for_claim"]),
        "## Branch Copies\n\n" + markdown_table(rows_by_name["branches"], ["copy_id", "table_key", "source_table", "copy_path", "purpose", "exists", "row_count", "valid_for_claim"]),
        "## Validation\n\n" + markdown_table(rows_by_name["validation"], ["validation_id", "passed", "detail", "timestamp_utc"]),
        "## Plain-English Read\n\nThis is a good little gym session: the matrix machinery behaves, so the next bottleneck is not linear algebra. The next serious fight is the coupling owner: what parent object makes Ti/Pt respond differently, or proves they cannot differ under universal metric/coframe coupling?",
        "",
    ])


def main() -> None:
    ensure_dirs()
    sources = build_sources()
    schema = build_schema_rows()
    preview_rows = load_surrogate_preview()
    matrix, scales, matrix_rows = build_matrix(preview_rows)
    diagnostics = build_diagnostics(matrix, scales)
    correlations = build_correlations(matrix)
    fit = build_smoke_fit(matrix)
    replacement = build_replacement_rows()
    tau = build_tau_rows(diagnostics, fit)
    candidate = build_candidate_rows()
    bounds = build_bound_rows()
    runner, comparisons = run_product_runner(candidate, bounds)
    gates = build_gates()
    decision = build_decision_rows(diagnostics)
    next_rows = build_next_rows()

    for key, rows in [
        ("sources", sources), ("schema", schema), ("matrix", matrix_rows),
        ("diagnostics", diagnostics), ("correlations", correlations), ("fit", fit),
        ("replacement", replacement), ("tau", tau), ("candidate", candidate),
        ("bounds", bounds), ("runner", runner), ("comparisons", comparisons),
        ("gates", gates), ("decision", decision), ("next", next_rows),
    ]:
        write_csv(OUTPUTS[key], rows)

    branches = copy_branch_outputs(schema, matrix_rows, diagnostics, correlations, fit, replacement, tau, candidate, gates, next_rows)
    write_csv(OUTPUTS["branches"], branches)
    remove_pycache()

    rows_by_name = {
        "sources": sources,
        "schema": schema,
        "matrix": matrix_rows,
        "diagnostics": diagnostics,
        "correlations": correlations,
        "fit": fit,
        "replacement": replacement,
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
    validation = build_validation(rows_by_name, matrix, csv_paths)
    rows_by_name["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(build_doc(rows_by_name), encoding="utf-8")
    remove_pycache()

    overall = next(row for row in validation if row["validation_id"] == "VAL2781_OVERALL")
    print(f"2781 complete: overall={overall['passed']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
