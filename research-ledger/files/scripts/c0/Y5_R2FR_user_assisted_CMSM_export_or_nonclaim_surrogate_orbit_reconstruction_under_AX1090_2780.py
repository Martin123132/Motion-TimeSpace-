from __future__ import annotations

import csv
import math
import shutil
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
DOC = WORK / "2780-Y5-R2FR-user-assisted-CMSM-export-or-nonclaim-surrogate-orbit-reconstruction-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2780_SOURCE_REGISTER.csv",
    "inventory": MTS / "P8_Y5_R2FR_2780_CMSM_EXPORT_INVENTORY_CHECK.csv",
    "assumptions": MTS / "P8_Y5_R2FR_2780_SURROGATE_ASSUMPTIONS.csv",
    "grid": MTS / "P8_Y5_R2FR_2780_SURROGATE_GRID_METADATA_SEGMENT210.csv",
    "preview": MTS / "P8_Y5_R2FR_2780_SURROGATE_GXS_PREVIEW_SEGMENT210.csv",
    "replacement": MTS / "P8_Y5_R2FR_2780_SURROGATE_TO_OFFICIAL_REPLACEMENT_MAP.csv",
    "status": MTS / "P8_Y5_R2FR_2780_SURROGATE_STATUS_LEDGER.csv",
    "candidate": MTS / "P8_Y5_R2FR_2780_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv",
    "bounds": MTS / "P8_Y5_R2FR_2780_WEP_BOUND_IMPORT.csv",
    "runner": MTS / "P8_Y5_R2FR_2780_PRODUCT_RUNNER_STATUS.csv",
    "comparisons": MTS / "P8_Y5_R2FR_2780_PRODUCT_COMPARISON_ROWS.csv",
    "gates": MTS / "P8_Y5_R2FR_2780_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2780_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2780_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2780_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2780_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "inventory_queue": RAB_QUEUE / "JR2780_CMSM_EXPORT_INVENTORY_OR_SURROGATE_NONCLAIM.csv",
    "surrogate_queue": RAB_QUEUE / "JR2780_SEGMENT210_SURROGATE_GXS_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "MICROSCOPE_SURROGATE_GXS_2780_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_surrogate_gxS_2780_nonclaim.csv",
    "cmsm_surrogate": CMSM_DIR / "SURROGATE_SEGMENT210_GXS_2780_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2780_SURROGATE_DESIGN_MATRIX_NEXT.csv",
}

KNOWN_NON_EXPORT_FILES = {
    "CMSM_EXPORT_AND_ARRAY_CONTRACT_2779_NONCLAIM.csv",
    "README_2001_DROP_CMSM_EXPORTS_HERE.txt",
    "TEMPLATE_2001_expected_official_array_schema.csv",
}

EARTH_MU_M3_S2 = 3.986004418e14
TORB_S = 5946.0
SAMPLE_RATE_HZ = 4.0
SEGMENT_ID = 210
DURATION_ORBITS = 50
FORB_HZ = 0.00016818
FSPIN3_HZ = 0.00294315
FEP3_HZ = 0.00311133
PREVIEW_ROWS = 256


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent, CMSM_DIR}:
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
        ("SRC2780_00_2779_next", "2779_next", MTS / "P8_Y5_R2FR_2779_NEXT_TARGET.csv", "NEXT2779_0_2780", "current handoff into CMSM export or surrogate reconstruction"),
        ("SRC2780_01_2779_validation", "2779_validation", MTS / "P8_Y5_BRR545_2779_VALIDATION.csv", "VAL2779_OVERALL", "current validation baseline"),
        ("SRC2780_02_2779_contract", "2779_contract", MTS / "P8_Y5_R2FR_2779_CMSM_EXPORT_CONTRACT.csv", "CMSM2779_5_official_gxS_arrays", "current CMSM export contract"),
        ("SRC2780_03_2779_array_contract", "2779_array_contract", MTS / "P8_Y5_R2FR_2779_OFFICIAL_ARRAY_SCHEMA_CONTRACT.csv", "ARR2779_7_generation_method", "current official-array schema contract"),
        ("SRC2780_04_2779_dry_run", "2779_dry_run", MTS / "P8_Y5_R2FR_2779_GXS_DRY_RUN_KERNEL_PREVIEW_SEGMENT210.csv", "GXS2779_210_31", "current phase-only dry-run path"),
        ("SRC2780_05_2779_tau", "2779_tau", MTS / "P8_Y5_R2FR_2779_NUMERIC_TAU_STATUS.csv", "NTS2779_3_tau_WEP", "current numeric tau blocker"),
        ("SRC2780_06_1074_doc", "1074_doc", WORK / "1074-Y5-R10-user-assisted-CMSM-export-or-nonclaim-surrogate-orbit-reconstruction.md", "Surrogate assumptions", "R10 precedent for nonclaim surrogate reconstruction"),
        ("SRC2780_07_1074_assumptions", "1074_assumptions", MTS / "P8_Y5_R10_1074_SURROGATE_ASSUMPTIONS.csv", "SUR1074_6_masks_attitude", "prior surrogate assumption ledger"),
        ("SRC2780_08_1074_replacement", "1074_replacement", MTS / "P8_Y5_R10_1074_SURROGATE_TO_OFFICIAL_REPLACEMENT_MAP.csv", "MAP1074_4_mask", "prior surrogate replacement map"),
        ("SRC2780_09_local_bounds", "local_bounds", LOCAL_BOUNDS / "local_bound_claims.csv", "R1_WEP_source_charge", "local MICROSCOPE WEP bound source row"),
    ]
    return [source_row(*spec) for spec in specs]


def candidate_cmsm_export_files() -> list[Path]:
    if not CMSM_DIR.exists():
        return []
    candidates: list[Path] = []
    for path in CMSM_DIR.rglob("*"):
        if not path.is_file():
            continue
        if path.name in KNOWN_NON_EXPORT_FILES:
            continue
        if path.name.startswith("SURROGATE_") or path.name.startswith("CMSM_EXPORT_AND_ARRAY_CONTRACT_"):
            continue
        if path.suffix.lower() in {".csv", ".txt", ".json", ".xml", ".fits", ".dat", ".zip"}:
            candidates.append(path)
    return candidates


def build_inventory_rows() -> list[dict[str, Any]]:
    CMSM_DIR.mkdir(parents=True, exist_ok=True)
    candidates = candidate_cmsm_export_files()
    known_files = sorted(path.name for path in CMSM_DIR.rglob("*") if path.is_file())
    return [
        nonclaim({
            "inventory_id": "INV2780_0_search_root",
            "search_root": str(CMSM_DIR),
            "exists": CMSM_DIR.exists(),
            "known_non_export_files_seen": ";".join(name for name in known_files if name in KNOWN_NON_EXPORT_FILES or name.startswith("CMSM_EXPORT_AND_ARRAY_CONTRACT_") or name.startswith("SURROGATE_")),
            "matching_files": len(candidates),
            "matching_file_list": ";".join(str(path) for path in candidates),
            "contract_match_status": "NO_USER_SUPPLIED_CMSM_EXPORT_FOUND" if not candidates else "POSSIBLE_USER_SUPPLIED_EXPORT_NEEDS_CONTRACT_VALIDATION",
            "action_taken": "surrogate reconstruction branch selected" if not candidates else "official import branch deferred pending contract validation",
        })
    ]


def surrogate_scalars() -> dict[str, float]:
    mean_motion = 2.0 * math.pi / TORB_S
    radius = (EARTH_MU_M3_S2 / (mean_motion * mean_motion)) ** (1.0 / 3.0)
    gravity = EARTH_MU_M3_S2 / (radius * radius)
    gradient = EARTH_MU_M3_S2 / (radius * radius * radius)
    return {
        "mean_motion_rad_s": mean_motion,
        "radius_m": radius,
        "gravity_m_s2": gravity,
        "gradient_s2": gradient,
    }


def build_assumptions() -> list[dict[str, Any]]:
    scalars = surrogate_scalars()
    return [
        nonclaim({"assumption_id": "SUR2780_0_branch_selection", "object": "branch", "value": "nonclaim surrogate orbit/gravity reconstruction", "units": "text", "source_or_reason": "CMSM export absent and CMSM/API access blocked in 2779", "claim_status": "FORBIDDEN_FOR_EVIDENCE"}),
        nonclaim({"assumption_id": "SUR2780_1_orbit_period", "object": "Torb", "value": TORB_S, "units": "s", "source_or_reason": "MICROSCOPE frequency table / 2778 kernel source row", "claim_status": "source-backed scalar, but surrogate use only"}),
        nonclaim({"assumption_id": "SUR2780_2_orbit_radius", "object": "r_surrogate=(mu/n^2)^(1/3)", "value": scalars["radius_m"], "units": "m", "source_or_reason": "derived from Earth monopole and Torb; not official ephemeris", "claim_status": "surrogate_only"}),
        nonclaim({"assumption_id": "SUR2780_3_gravity_amplitude", "object": "g0=mu/r^2", "value": scalars["gravity_m_s2"], "units": "m s^-2", "source_or_reason": "spherical Earth monopole; not MICROSCOPE gravity model", "claim_status": "surrogate_only"}),
        nonclaim({"assumption_id": "SUR2780_4_gradient_scale", "object": "G=mu/r^3", "value": scalars["gradient_s2"], "units": "s^-2", "source_or_reason": "spherical Earth monopole gradient scale; no inertia subtraction", "claim_status": "surrogate_only"}),
        nonclaim({"assumption_id": "SUR2780_5_readout_phase", "object": "phi=2*pi*fEP3*t", "value": FEP3_HZ, "units": "Hz", "source_or_reason": "official fEP3 scalar; zero phase is guessed", "claim_status": "FORBIDDEN_FOR_EVIDENCE"}),
        nonclaim({"assumption_id": "SUR2780_6_masks_attitude", "object": "masks/attitude/inertia", "value": "omitted_or_identity_surrogate", "units": "text", "source_or_reason": "official products unavailable", "claim_status": "FORBIDDEN_FOR_EVIDENCE"}),
    ]


def build_surrogate_grid_and_preview() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    scalars = surrogate_scalars()
    full_grid_samples = int(DURATION_ORBITS * TORB_S * SAMPLE_RATE_HZ)
    grid = [
        nonclaim({
            "grid_id": "GRID2780_0_segment210_surrogate",
            "segment": SEGMENT_ID,
            "duration_orbits": DURATION_ORBITS,
            "torb_s": TORB_S,
            "sample_rate_hz": SAMPLE_RATE_HZ,
            "full_grid_samples": full_grid_samples,
            "preview_rows_written": PREVIEW_ROWS,
            "orbit_radius_m": scalars["radius_m"],
            "orbit_model": "circular_Earth_monopole_from_Torb",
            "attitude_model": "zero_phase_rotating_XZ_plane_surrogate",
            "mask_model": "all_samples_unmasked_surrogate",
            "inertia_subtraction": "omitted",
            "claim_status": "NONCLAIM_PIPELINE_TEST_ONLY",
        })
    ]
    preview: list[dict[str, Any]] = []
    step = (full_grid_samples - 1) // (PREVIEW_ROWS - 1)
    gravity = scalars["gravity_m_s2"]
    gradient = scalars["gradient_s2"]
    for index in range(PREVIEW_ROWS):
        sample_index = min(index * step, full_grid_samples - 1)
        t_sec = sample_index / SAMPLE_RATE_HZ
        phase = (2.0 * math.pi * FEP3_HZ * t_sec) % (2.0 * math.pi)
        gx = -gravity * math.cos(phase)
        gz = -gravity * math.sin(phase)
        sxx = 2.0 * gradient * math.cos(2.0 * phase)
        sxz = gradient * 1.5 * math.sin(2.0 * phase)
        preview.append(nonclaim({
            "row_id": f"SUR2780_210_{index:03d}",
            "segment": SEGMENT_ID,
            "sample_index": sample_index,
            "t_sec_from_segment_start": round(t_sec, 12),
            "gx_surrogate_m_s2": f"{gx:.12f}",
            "gz_surrogate_m_s2": f"{gz:.12f}",
            "Sxx_surrogate_s2": f"{sxx:.15e}",
            "Sxz_surrogate_s2": f"{sxz:.15e}",
            "mask_flag_surrogate": "unmasked_surrogate",
            "source_status": "NOT_CMSM_NOT_OFFICIAL",
        }))
    return grid, preview


def build_replacement_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"map_id": "MAP2780_0_gx", "official_contract_column": "gx", "surrogate_column": "gx_surrogate_m_s2", "replacement_status": "SURROGATE_AVAILABLE_OFFICIAL_MISSING", "evidence_policy": "cannot support claim", "next_action": "replace with CMSM/official gx"}),
        nonclaim({"map_id": "MAP2780_1_gz", "official_contract_column": "gz", "surrogate_column": "gz_surrogate_m_s2", "replacement_status": "SURROGATE_AVAILABLE_OFFICIAL_MISSING", "evidence_policy": "cannot support claim", "next_action": "replace with CMSM/official gz"}),
        nonclaim({"map_id": "MAP2780_2_Sxx", "official_contract_column": "Sxx", "surrogate_column": "Sxx_surrogate_s2", "replacement_status": "SURROGATE_AVAILABLE_OFFICIAL_MISSING", "evidence_policy": "cannot support claim", "next_action": "replace with CMSM/official Sxx or official reconstruction"}),
        nonclaim({"map_id": "MAP2780_3_Sxz", "official_contract_column": "Sxz", "surrogate_column": "Sxz_surrogate_s2", "replacement_status": "SURROGATE_AVAILABLE_OFFICIAL_MISSING", "evidence_policy": "cannot support claim", "next_action": "replace with CMSM/official Sxz or official reconstruction"}),
        nonclaim({"map_id": "MAP2780_4_mask", "official_contract_column": "mask_flag", "surrogate_column": "mask_flag_surrogate", "replacement_status": "SURROGATE_ALL_UNMASKED_OFFICIAL_MISSING", "evidence_policy": "cannot support claim", "next_action": "replace with exact CMSM mask"}),
    ]


def build_status_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"status_id": "STAT2780_0_CMSM_export", "object": "user-assisted CMSM export", "status": "NOT_FOUND_LOCALLY", "next_action": "import user-supplied CMSM export if available", "claim_allowed": False}),
        nonclaim({"status_id": "STAT2780_1_surrogate_orbit", "object": "surrogate segment 210 orbit/gravity preview", "status": "BUILT_NONCLAIM", "next_action": "wire surrogate into a nonclaim design-matrix/tau-shape smoke runner", "claim_allowed": False}),
        nonclaim({"status_id": "STAT2780_2_official_arrays", "object": "official gx/gz/Sxx/Sxz arrays", "status": "NOT_ACQUIRED", "next_action": "replace surrogate columns with CMSM official arrays", "claim_allowed": False}),
        nonclaim({"status_id": "STAT2780_3_tau_WEP", "object": "numeric tau_WEP", "status": "NOT_ACQUIRED", "next_action": "derive only after official arrays or explicitly nonclaim smoke-route selection", "claim_allowed": False}),
    ]


def build_candidate_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "prediction_id": "PRED2780_0_WEP_surrogate_orbit_nonclaim_product",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_OFFICIAL_ARRAYS_SURROGATE_ONLY",
            "product_units": "dimensionless",
            "derivation_status": "NONCLAIM_SURROGATE_PIPELINE_ONLY",
            "notes": "surrogate arrays are unitful plumbing checks, not MICROSCOPE evidence and not an MTS tau_WEP product",
        })
    ]


def build_bound_rows() -> list[dict[str, Any]]:
    bound = get_local_bound("R1_WEP_source_charge")
    return [
        nonclaim({
            "bound_id": "BOUND2780_0_MICROSCOPE_R1_eta_source_charge",
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
            "runner_id": "APR2780_0_WEP_surrogate_orbit_product_stub",
            "prediction_rows": len(predictions),
            "bound_rows": len(bounds),
            "valid_prediction_rows": len(valid_predictions),
            "valid_bound_rows": len(valid_bounds),
            "claim_allowed": False,
            "expected_result": "reject surrogate-only prediction and keep claim false",
        })
    ]
    return runner, comparisons


def build_gates() -> list[dict[str, Any]]:
    return [
        nonclaim({"gate_id": "CG2780_0_CMSM_export", "claim_component": "user/CMSM export", "gate_pass": False, "claim_allowed": False, "reason": "NO_USER_SUPPLIED_CMSM_EXPORT_FOUND"}),
        nonclaim({"gate_id": "CG2780_1_surrogate_preview", "claim_component": "surrogate segment 210 gxS preview", "gate_pass": True, "claim_allowed": False, "reason": "pipeline built but not official arrays"}),
        nonclaim({"gate_id": "CG2780_2_replacement_map", "claim_component": "surrogate-to-official replacement map", "gate_pass": True, "claim_allowed": False, "reason": "replacement requirements explicit"}),
        nonclaim({"gate_id": "CG2780_3_official_arrays", "claim_component": "official gx/gz/Sxx/Sxz arrays", "gate_pass": False, "claim_allowed": False, "reason": "MISSING_OFFICIAL_ARRAYS"}),
        nonclaim({"gate_id": "CG2780_4_product_runner", "claim_component": "WEP product runner", "gate_pass": False, "claim_allowed": False, "reason": "valid_prediction_rows=0"}),
        nonclaim({"gate_id": "CG2780_5_local_GR_WEP_claim", "claim_component": "local-GR/WEP pass", "gate_pass": False, "claim_allowed": False, "reason": "surrogate-only arrays and no MTS tau_WEP product"}),
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"decision_id": "DEC2780_0_surrogate_branch_selected", "decision": "no local CMSM export found, so select nonclaim surrogate branch", "evidence": "INV2780_0_search_root", "consequence": "test pipeline geometry without claiming evidence"}),
        nonclaim({"decision_id": "DEC2780_1_surrogate_is_useful", "decision": "surrogate gx/gz/Sxx/Sxz arrays now exist with physical units and source flags in the R2/f(R) branch", "evidence": "P8_Y5_R2FR_2780_SURROGATE_GXS_PREVIEW_SEGMENT210.csv", "consequence": "next step can build a design-matrix/tau-shape smoke runner"}),
        nonclaim({"decision_id": "DEC2780_2_no_claim", "decision": "do not treat surrogate arrays as official MICROSCOPE evidence", "evidence": "STAT2780_3_tau_WEP; APR2780_0_WEP_surrogate_orbit_product_stub", "consequence": "WEP/local-GR branch remains blocked"}),
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "row_id": "NEXT2780_0_2781",
            "next_target": "2781-Y5-R2FR-surrogate-design-matrix-tau-shape-smoke-runner-under-AX1090.md",
            "script": "scripts/Y5_R2FR_surrogate_design_matrix_tau_shape_smoke_runner_under_AX1090_2781.py",
            "objective": "use the 2780 nonclaim surrogate gx/gz/Sxx/Sxz arrays to build a design-matrix/tau-shape smoke runner that verifies regression plumbing and replacement gates, while refusing any WEP/local-GR claim until official arrays and the MTS material/source map exist",
            "include": "segment 210 surrogate design matrix; polynomial/gx/gz/Sxx/Sxz columns; condition-number/orthogonality diagnostics; replacement gates; product-runner refusal",
            "exclude": "treating surrogate fit as MICROSCOPE evidence; official claim; tau=1; guessed masks as final; GitHub; formalization edits",
        })
    ]


def copy_branch_outputs(
    inventory: list[dict[str, Any]],
    assumptions: list[dict[str, Any]],
    grid: list[dict[str, Any]],
    preview: list[dict[str, Any]],
    replacement: list[dict[str, Any]],
    status: list[dict[str, Any]],
    candidate: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    inventory_rows = inventory + status + gates
    surrogate_rows = assumptions + grid + preview + replacement + status + candidate + gates
    beta_rows = assumptions + grid + status + next_rows
    microscope_rows = inventory + assumptions + grid + preview + replacement + status + candidate + next_rows
    next_queue_rows = next_rows
    specs = [
        ("BR2780_0_inventory_queue", "inventory", inventory_rows, OUTPUTS["inventory"], BRANCH_OUTPUTS["inventory_queue"], "CMSM inventory decision nonclaim copy"),
        ("BR2780_1_surrogate_queue", "surrogate", surrogate_rows, OUTPUTS["preview"], BRANCH_OUTPUTS["surrogate_queue"], "segment-210 surrogate gxS nonclaim copy"),
        ("BR2780_2_beta_doc", "beta_doc", beta_rows, OUTPUTS["status"], BRANCH_OUTPUTS["beta_doc"], "beta/source-facing surrogate kernel copy"),
        ("BR2780_3_microscope_copy", "microscope", microscope_rows, OUTPUTS["candidate"], BRANCH_OUTPUTS["microscope_copy"], "MICROSCOPE surrogate orbit acquisition copy"),
        ("BR2780_4_cmsm_surrogate", "cmsm_surrogate", preview, OUTPUTS["preview"], BRANCH_OUTPUTS["cmsm_surrogate"], "surrogate file placed beside CMSM drop folder for replacement workflow"),
        ("BR2780_5_next_queue", "next", next_queue_rows, OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next surrogate design-matrix smoke-runner target"),
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
    inventory = rows_by_name["inventory"]
    assumptions = rows_by_name["assumptions"]
    grid = rows_by_name["grid"]
    preview = rows_by_name["preview"]
    replacement = rows_by_name["replacement"]
    status = rows_by_name["status"]
    candidate = rows_by_name["candidate"]
    bounds = rows_by_name["bounds"]
    runner = rows_by_name["runner"]
    gates = rows_by_name["gates"]
    next_rows = rows_by_name["next"]
    branches = rows_by_name["branches"]
    checks = [
        ("VAL2780_0_sources", all(row["exists"] and row["needle_found"] for row in sources), "every cited source path exists and source needle was found"),
        ("VAL2780_1_no_CMSM_export", inventory[0]["matching_files"] == 0 and inventory[0]["contract_match_status"] == "NO_USER_SUPPLIED_CMSM_EXPORT_FOUND", "no local user-supplied CMSM export found"),
        ("VAL2780_2_assumptions_nonclaim", len(assumptions) == 7 and all(row["valid_for_claim"] is False for row in assumptions) and any(row["assumption_id"] == "SUR2780_6_masks_attitude" and row["claim_status"] == "FORBIDDEN_FOR_EVIDENCE" for row in assumptions), "surrogate assumptions are nonclaim and mask/attitude gap is explicit"),
        ("VAL2780_3_grid_metadata", len(grid) == 1 and grid[0]["full_grid_samples"] == 1189200 and grid[0]["preview_rows_written"] == PREVIEW_ROWS and grid[0]["claim_status"] == "NONCLAIM_PIPELINE_TEST_ONLY", "grid metadata has expected segment 210 sample count and nonclaim status"),
        ("VAL2780_4_preview_rows", len(preview) == PREVIEW_ROWS and all(row["source_status"] == "NOT_CMSM_NOT_OFFICIAL" and row["valid_for_claim"] is False for row in preview), "surrogate preview rows written and flagged nonofficial"),
        ("VAL2780_5_preview_units_numeric", all(is_numeric(row["gx_surrogate_m_s2"]) and is_numeric(row["Sxx_surrogate_s2"]) for row in preview), "surrogate gx/S values are numeric unitful columns"),
        ("VAL2780_6_replacement_map", len(replacement) == 5 and any(row["map_id"] == "MAP2780_4_mask" for row in replacement), "replacement map covers official gx/gz/Sxx/Sxz/mask columns"),
        ("VAL2780_7_tau_not_acquired", any(row["status_id"] == "STAT2780_3_tau_WEP" and row["status"] == "NOT_ACQUIRED" and row["claim_allowed"] is False for row in status), "numeric tau_WEP remains not acquired"),
        ("VAL2780_8_prediction_nonclaim_missing", len(candidate) == 1 and candidate[0]["valid_for_claim"] is False and has_missing_marker(candidate[0]), "prediction row remains missing official arrays"),
        ("VAL2780_9_bound_numeric", len(bounds) == 1 and is_numeric(bounds[0]["bound_value"]) and float(str(bounds[0]["bound_value"])) > 0.0 and bounds[0]["bound_valid_for_internal_runner"] is True, "bound import is positive numeric"),
        ("VAL2780_10_runner_refuses", runner[0]["valid_prediction_rows"] == 0 and runner[0]["claim_allowed"] is False, "runner reports no valid prediction rows and claim false"),
        ("VAL2780_11_claim_gates_safe", all(row["claim_allowed"] is False for row in gates) and any(row["gate_id"] == "CG2780_1_surrogate_preview" and row["gate_pass"] is True for row in gates), "all claim gates deny WEP/local-GR claim while acknowledging surrogate build"),
        ("VAL2780_12_next_target", any(row["row_id"] == "NEXT2780_0_2781" and "surrogate-design-matrix-tau-shape-smoke-runner" in row["next_target"] for row in next_rows), "next target selects surrogate design-matrix tau-shape smoke runner"),
        ("VAL2780_13_branch_outputs", all(row["exists"] and int(row["row_count"]) > 0 for row in branches), "branch copies exist and contain rows"),
        ("VAL2780_14_csv_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2780_15_no_claim_flags", no_claim_flags(rows_by_name), "no generated row is valid_for_claim=true/claim_allowed=true/pass_for_claim=true"),
        ("VAL2780_16_generated_under_post_checkpoint", generated_files_under_work(), "all generated outputs are under post-checkpoint-work"),
        ("VAL2780_17_formalization_untouched", formalization_untouched(), "formalization-workbench modified-file count remains zero during this run"),
        ("VAL2780_18_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for check_id, passed, detail in checks]
    rows.append({
        "validation_id": "VAL2780_OVERALL",
        "passed": all(row["passed"] for row in rows),
        "detail": "2780 finds no user-supplied CMSM export in the current drop folder, selects the explicitly nonclaim surrogate branch, builds unitful segment-210 gx/gz/Sxx/Sxz surrogate rows with replacement gates, refuses WEP/local-GR scoring, and selects a surrogate design-matrix/tau-shape smoke runner as 2781.",
        "timestamp_utc": ts(),
    })
    return rows


def build_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join([
        "# 2780 - Y5 R2/f(R): User-Assisted CMSM Export Or Nonclaim Surrogate Orbit Reconstruction Under AX1090",
        "## Private Verdict\n\n2780 found no local user-supplied CMSM export, so it selected the only honest route available from this machine: a strictly nonclaim segment-210 surrogate orbit/gravity reconstruction. This gives the R2/f(R) branch unitful gx/gz/Sxx/Sxz plumbing for the next smoke runner, but it is not official MICROSCOPE evidence and cannot support a WEP/local-GR claim.",
        "## Source Register\n\n" + markdown_table(rows_by_name["sources"], ["row_id", "source_key", "source_path", "exists", "needle_found", "source_role", "valid_for_claim"]),
        "## CMSM Export Inventory Check\n\n" + markdown_table(rows_by_name["inventory"], ["inventory_id", "search_root", "exists", "known_non_export_files_seen", "matching_files", "contract_match_status", "action_taken", "valid_for_claim"]),
        "## Surrogate Assumptions\n\n" + markdown_table(rows_by_name["assumptions"], ["assumption_id", "object", "value", "units", "source_or_reason", "claim_status", "valid_for_claim"]),
        "## Surrogate Grid Metadata\n\n" + markdown_table(rows_by_name["grid"], ["grid_id", "segment", "duration_orbits", "torb_s", "sample_rate_hz", "full_grid_samples", "preview_rows_written", "orbit_radius_m", "orbit_model", "attitude_model", "mask_model", "inertia_subtraction", "claim_status", "valid_for_claim"]),
        "## Surrogate gxS Preview\n\n" + markdown_table(rows_by_name["preview"][:10], ["row_id", "sample_index", "t_sec_from_segment_start", "gx_surrogate_m_s2", "gz_surrogate_m_s2", "Sxx_surrogate_s2", "Sxz_surrogate_s2", "source_status", "valid_for_claim"]) + "\n\n_Only the first 10 of 256 preview rows are shown here; the full CSV is written separately._",
        "## Replacement Map\n\n" + markdown_table(rows_by_name["replacement"], ["map_id", "official_contract_column", "surrogate_column", "replacement_status", "evidence_policy", "next_action", "valid_for_claim"]),
        "## Status Ledger\n\n" + markdown_table(rows_by_name["status"], ["status_id", "object", "status", "next_action", "claim_allowed", "valid_for_claim"]),
        "## Nonclaim Product Candidate\n\n" + markdown_table(rows_by_name["candidate"], ["prediction_id", "arena", "product_symbol", "product_value", "product_units", "derivation_status", "notes", "valid_for_claim"]),
        "## Bound Import\n\n" + markdown_table(rows_by_name["bounds"], ["bound_id", "arena", "product_symbol", "bound_value", "bound_units", "bound_type", "source_row_id", "bound_valid_for_internal_runner", "valid_for_claim"]),
        "## Product Runner Status\n\n" + markdown_table(rows_by_name["runner"], ["runner_id", "prediction_rows", "bound_rows", "valid_prediction_rows", "valid_bound_rows", "claim_allowed", "expected_result", "valid_for_claim"]),
        "## Product Comparison Rows\n\n" + markdown_table(rows_by_name["comparisons"], ["comparison_id", "comparison_status", "pass_for_claim", "issues", "valid_for_claim"]),
        "## Claim Gates\n\n" + markdown_table(rows_by_name["gates"], ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason", "valid_for_claim"]),
        "## Decision Ledger\n\n" + markdown_table(rows_by_name["decision"], ["decision_id", "decision", "evidence", "consequence", "valid_for_claim"]),
        "## Next Target\n\n" + markdown_table(rows_by_name["next"], ["row_id", "next_target", "script", "objective", "include", "exclude", "valid_for_claim"]),
        "## Branch Copies\n\n" + markdown_table(rows_by_name["branches"], ["copy_id", "table_key", "source_table", "copy_path", "purpose", "exists", "row_count", "valid_for_claim"]),
        "## Validation\n\n" + markdown_table(rows_by_name["validation"], ["validation_id", "passed", "detail", "timestamp_utc"]),
        "## Plain-English Read\n\nWe did not get through the official-data door, so we stopped rattling the handle and built the sparring partner. The surrogate is not evidence, but it is useful: it lets us test whether the MICROSCOPE regression/tau plumbing is mathematically sane before we spend another round hunting official arrays.",
        "",
    ])


def main() -> None:
    ensure_dirs()
    sources = build_sources()
    inventory = build_inventory_rows()
    assumptions = build_assumptions()
    grid, preview = build_surrogate_grid_and_preview()
    replacement = build_replacement_rows()
    status = build_status_rows()
    candidate = build_candidate_rows()
    bounds = build_bound_rows()
    runner, comparisons = run_product_runner(candidate, bounds)
    gates = build_gates()
    decision = build_decision_rows()
    next_rows = build_next_rows()

    for key, rows in [
        ("sources", sources), ("inventory", inventory), ("assumptions", assumptions),
        ("grid", grid), ("preview", preview), ("replacement", replacement),
        ("status", status), ("candidate", candidate), ("bounds", bounds),
        ("runner", runner), ("comparisons", comparisons), ("gates", gates),
        ("decision", decision), ("next", next_rows),
    ]:
        write_csv(OUTPUTS[key], rows)

    branches = copy_branch_outputs(inventory, assumptions, grid, preview, replacement, status, candidate, gates, next_rows)
    write_csv(OUTPUTS["branches"], branches)
    remove_pycache()

    rows_by_name = {
        "sources": sources,
        "inventory": inventory,
        "assumptions": assumptions,
        "grid": grid,
        "preview": preview,
        "replacement": replacement,
        "status": status,
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

    overall = next(row for row in validation if row["validation_id"] == "VAL2780_OVERALL")
    print(f"2780 complete: overall={overall['passed']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
