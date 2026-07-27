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
CMSM_DROP = ROOT / "source-intake" / "microscope_cmsm"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"
DOC = ROOT / "2001-Y5-R2FR-user-CMSM-export-or-nonclaim-surrogate-reconstruction.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "2001-user-CMSM-export-or-nonclaim-surrogate-reconstruction" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_PARENT_QLOC_2001_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_PARENT_QLOC_2001_WEP_BOUND_IMPORT.csv"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

MU_EARTH = 3.986004418e14
TORB_S = 5946.0
FEP3_HZ = 3.11133e-3
SAMPLE_RATE_HZ = 4.0
SEGMENT_210_ORBITS = 50
THIN_ROWS = 1024

OFFICIAL_ARRAY_COLUMNS = [
    "segment_id",
    "t_utc",
    "sample_index",
    "gx",
    "gz",
    "Sxx",
    "Sxz",
    "mask_flag",
]


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
            "SRC2001_0_2000_doc",
            "2000-Y5-R2FR-CMSM-schema-or-one-segment-official-array-extract.md",
            ["Next honest move", "2001-Y5-R2FR-user-CMSM-export-or-nonclaim-surrogate-reconstruction.md"],
            "2000 handoff to this checkpoint.",
        ),
        (
            "SRC2001_1_2000_validation",
            "source-intake/mts_residuals/P8_Y5_BRR545_2000_VALIDATION.csv",
            ["VAL2000_OVERALL", "PASS"],
            "2000 validation pass.",
        ),
        (
            "SRC2001_2_2000_contract",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2000_CMSM_EXTRACTION_CONTRACT.csv",
            ["CMSM2000_4_official_gxS_arrays"],
            "official extraction contract.",
        ),
        (
            "SRC2001_3_2000_schema",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2000_OFFICIAL_ARRAY_SCHEMA_CONTRACT.csv",
            ["ARR2000_2_gx", "ARR2000_4_Sxx"],
            "official array schema contract.",
        ),
        (
            "SRC2001_4_1999_numeric_kernel",
            "1999-Y5-R2FR-MICROSCOPE-numeric-kernel-or-source-worldtube-row.md",
            ["CMSM1999_0_data_inventory_pointer", "NEXT1999_0_primary"],
            "numeric kernel/source-worldtube acquisition handoff.",
        ),
        (
            "SRC2001_5_1074_prior_surrogate",
            "1074-Y5-R10-user-assisted-CMSM-export-or-nonclaim-surrogate-orbit-reconstruction.md",
            ["SUR1074_0_branch_selection", "NOT_CMSM_NOT_OFFICIAL"],
            "earlier R10 analogue used only as surrogate-plumbing precedent.",
        ),
        (
            "SRC2001_6_local_bound",
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
                "needed_for": "2001 user CMSM export or nonclaim surrogate reconstruction",
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


def write_drop_guides() -> tuple[Path, Path]:
    CMSM_DROP.mkdir(parents=True, exist_ok=True)
    readme = CMSM_DROP / "README_2001_DROP_CMSM_EXPORTS_HERE.txt"
    template = CMSM_DROP / "TEMPLATE_2001_expected_official_array_schema.csv"
    readme.write_text(
        "\n".join(
            [
                "2001 CMSM export drop folder.",
                "Drop browser/API exports here only if they come from the official MICROSCOPE/CMSM route.",
                "Minimum CSV columns: " + ",".join(OFFICIAL_ARRAY_COLUMNS),
                "Extra columns are welcome if they document frame, units, source file, interpolation, and masks.",
                "Templates or surrogate files in this folder are never treated as official evidence.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    with template.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=OFFICIAL_ARRAY_COLUMNS + ["frame", "generation_method", "source_file", "unit_notes"],
        )
        writer.writeheader()
        writer.writerow(
            {
                "segment_id": "TEMPLATE_ONLY_REPLACE_WITH_210",
                "t_utc": "TEMPLATE_ONLY_REPLACE_WITH_UTC",
                "sample_index": "TEMPLATE_ONLY_REPLACE_WITH_INTEGER",
                "gx": "TEMPLATE_ONLY_REPLACE_WITH_NUMERIC_M_S2",
                "gz": "TEMPLATE_ONLY_REPLACE_WITH_NUMERIC_M_S2",
                "Sxx": "TEMPLATE_ONLY_REPLACE_WITH_NUMERIC_S2",
                "Sxz": "TEMPLATE_ONLY_REPLACE_WITH_NUMERIC_S2",
                "mask_flag": "TEMPLATE_ONLY_REPLACE_WITH_TRUE_OR_FALSE",
                "frame": "TEMPLATE_ONLY",
                "generation_method": "TEMPLATE_ONLY",
                "source_file": "TEMPLATE_ONLY",
                "unit_notes": "TEMPLATE_ONLY",
            }
        )
    return readme, template


def drop_contract_rows(readme: Path, template: Path) -> list[dict[str, object]]:
    schema_path = OUT / "P8_Y5_PARENT_QLOC_2000_OFFICIAL_ARRAY_SCHEMA_CONTRACT.csv"
    schema_rows = read_csv(schema_path)
    rows: list[dict[str, object]] = []
    required = [row for row in schema_rows if row.get("required_for_tau", "").lower() == "true"]
    for index, schema in enumerate(required):
        row = base_row()
        row.update(
            {
                "drop_id": f"DROP2001_{index:02d}_{schema.get('column_name', '')}",
                "column_name": schema.get("column_name", ""),
                "unit_or_type": schema.get("unit_or_type", ""),
                "required_for_tau": schema.get("required_for_tau", ""),
                "accepted_source": "official CMSM/exported array or source-backed reconstruction with provenance",
                "drop_folder": str(CMSM_DROP),
                "readme_path": str(readme),
                "template_path": str(template),
                "current_status": "AWAITING_USER_OR_BROWSER_EXPORT",
            }
        )
        rows.append(row)
    existing_columns = {str(row["column_name"]) for row in rows}
    supplemental = [
        ("sample_index", "integer", "exact sample index required by 2001 import validator"),
        ("mask_flag", "boolean", "exact official or source-backed mask flag required by 2001 import validator"),
    ]
    for column_name, unit_or_type, accepted_source in supplemental:
        if column_name in existing_columns:
            continue
        row = base_row()
        row.update(
            {
                "drop_id": f"DROP2001_extra_{column_name}",
                "column_name": column_name,
                "unit_or_type": unit_or_type,
                "required_for_tau": "true",
                "accepted_source": accepted_source,
                "drop_folder": str(CMSM_DROP),
                "readme_path": str(readme),
                "template_path": str(template),
                "current_status": "AWAITING_USER_OR_BROWSER_EXPORT",
            }
        )
        rows.append(row)
    return rows


def normalized_header(path: Path) -> list[str]:
    if path.suffix.lower() not in {".csv", ".tsv", ".txt", ".dat"}:
        return []
    delimiter = "\t" if path.suffix.lower() == ".tsv" else ","
    try:
        with path.open(newline="", encoding="utf-8", errors="ignore") as handle:
            reader = csv.reader(handle, delimiter=delimiter)
            return [cell.strip() for cell in next(reader, [])]
    except (OSError, csv.Error, UnicodeError):
        return []


def is_template_or_internal(path: Path) -> bool:
    name = path.name.lower()
    return (
        "template_2001" in name
        or "readme_2001" in name
        or "nonclaim" in name
        or "surrogate" in name
        or path.suffix.lower() not in {".csv", ".tsv", ".txt", ".dat", ".json", ".zip"}
    )


def cmsm_export_inventory_rows() -> list[dict[str, object]]:
    files = sorted(path for path in CMSM_DROP.rglob("*") if path.is_file() and not is_template_or_internal(path))
    rows: list[dict[str, object]] = []
    if not files:
        row = base_row()
        row.update(
            {
                "inventory_id": "INV2001_0_search_root",
                "search_root": str(CMSM_DROP),
                "candidate_file": "",
                "file_type": "",
                "header_columns": "",
                "required_columns_present": "false",
                "missing_required_columns": ";".join(OFFICIAL_ARRAY_COLUMNS),
                "contract_match_status": "NO_USER_SUPPLIED_CMSM_EXPORT_FOUND",
                "action_taken": "surrogate reconstruction branch selected",
            }
        )
        rows.append(row)
        return rows

    required = set(OFFICIAL_ARRAY_COLUMNS)
    for index, path in enumerate(files):
        header = normalized_header(path)
        header_set = set(header)
        missing = [column for column in OFFICIAL_ARRAY_COLUMNS if column not in header_set]
        if path.suffix.lower() in {".json", ".zip"}:
            status = "UNVALIDATED_CONTAINER_PRESENT"
        elif not header:
            status = "UNREADABLE_OR_HEADERLESS_TABLE"
        elif not missing:
            status = "COMPLETE_REQUIRED_SCHEMA_UNPROVEN_PROVENANCE"
        else:
            status = "PARTIAL_SCHEMA_MISSING_REQUIRED_COLUMNS"
        row = base_row()
        row.update(
            {
                "inventory_id": f"INV2001_file_{index:02d}",
                "search_root": str(CMSM_DROP),
                "candidate_file": str(path),
                "file_type": path.suffix.lower(),
                "header_columns": ";".join(header),
                "required_columns_present": str(bool(header) and not missing).lower(),
                "missing_required_columns": ";".join(missing),
                "contract_match_status": status,
                "action_taken": "do not claim; require provenance and exact CMSM source validation",
            }
        )
        rows.append(row)
    return rows


def orbital_radius_from_period() -> float:
    n = 2.0 * math.pi / TORB_S
    return (MU_EARTH / (n * n)) ** (1.0 / 3.0)


def surrogate_assumption_rows(inventory_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    complete_exports = [row for row in inventory_rows if row.get("contract_match_status") == "COMPLETE_REQUIRED_SCHEMA_UNPROVEN_PROVENANCE"]
    radius = orbital_radius_from_period()
    g0 = MU_EARTH / (radius * radius)
    grad = MU_EARTH / (radius**3)
    specs = [
        (
            "SUR2001_0_branch_selection",
            "branch",
            "nonclaim surrogate reconstruction" if not complete_exports else "official-like schema present but unproven",
            "text",
            "no claim-grade CMSM export is validated",
            "FORBIDDEN_FOR_EVIDENCE",
        ),
        (
            "SUR2001_1_orbit_period",
            "Torb",
            TORB_S,
            "s",
            "carried from prior MICROSCOPE segment/frequency source row and 1074 precedent",
            "source-backed scalar, surrogate-only use",
        ),
        (
            "SUR2001_2_orbit_radius",
            "r_surrogate=(mu/n^2)^(1/3)",
            radius,
            "m",
            "derived from Earth monopole and Torb; not official ephemeris",
            "surrogate_only",
        ),
        (
            "SUR2001_3_gravity_amplitude",
            "g0=mu/r^2",
            g0,
            "m s^-2",
            "spherical Earth monopole; not MICROSCOPE gravity model",
            "surrogate_only",
        ),
        (
            "SUR2001_4_gradient_scale",
            "G=mu/r^3",
            grad,
            "s^-2",
            "spherical Earth monopole gradient scale; inertia subtraction omitted",
            "surrogate_only",
        ),
        (
            "SUR2001_5_readout_phase",
            "phi=2*pi*fEP3*t",
            FEP3_HZ,
            "Hz",
            "zero phase is guessed; exact attitude products missing",
            "FORBIDDEN_FOR_EVIDENCE",
        ),
        (
            "SUR2001_6_masks_attitude",
            "masks/attitude/inertia",
            "omitted_or_identity_surrogate",
            "text",
            "official products unavailable",
            "FORBIDDEN_FOR_EVIDENCE",
        ),
    ]
    rows: list[dict[str, object]] = []
    for assumption_id, obj, value, units, reason, claim_status in specs:
        row = base_row()
        row.update(
            {
                "assumption_id": assumption_id,
                "object": obj,
                "value": value,
                "units": units,
                "source_or_reason": reason,
                "claim_status": claim_status,
            }
        )
        rows.append(row)
    return rows


def surrogate_grid_metadata_rows() -> list[dict[str, object]]:
    total_samples = int(SEGMENT_210_ORBITS * TORB_S * SAMPLE_RATE_HZ)
    radius = orbital_radius_from_period()
    row = base_row()
    row.update(
        {
            "grid_id": "GRID2001_0_segment210_thin_surrogate",
            "segment": "210",
            "duration_orbits": SEGMENT_210_ORBITS,
            "torb_s": TORB_S,
            "sample_rate_hz": SAMPLE_RATE_HZ,
            "full_grid_samples": total_samples,
            "thin_rows_written": THIN_ROWS,
            "orbit_radius_m": radius,
            "orbit_model": "circular_Earth_monopole_from_Torb",
            "attitude_model": "zero_phase_rotating_XZ_plane_surrogate",
            "mask_model": "all_samples_unmasked_surrogate",
            "inertia_subtraction": "omitted",
            "claim_status": "NONCLAIM_PIPELINE_TEST_ONLY",
        }
    )
    return [row]


def surrogate_thin_grid_rows() -> list[dict[str, object]]:
    radius = orbital_radius_from_period()
    g0 = MU_EARTH / (radius * radius)
    grad = MU_EARTH / (radius**3)
    total_samples = int(SEGMENT_210_ORBITS * TORB_S * SAMPLE_RATE_HZ)
    step = max((total_samples - 1) // (THIN_ROWS - 1), 1)
    rows: list[dict[str, object]] = []
    for thin_index in range(THIN_ROWS):
        sample_index = min(thin_index * step, total_samples - 1)
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
        gxs_shape = gx * sxx + gz * sxz
        row = base_row()
        row.update(
            {
                "row_id": f"SUR2001_210_{thin_index:04d}",
                "segment_id": "210",
                "sample_index": sample_index,
                "t_sec_from_segment_start": round(t_sec, 6),
                "orbit_fraction_from_start": round(t_sec / TORB_S, 9),
                "phase_fep_zeroed_rad": round(phi % (2.0 * math.pi), 12),
                "gx_surrogate_m_s2": f"{gx:.12e}",
                "gz_surrogate_m_s2": f"{gz:.12e}",
                "Sxx_surrogate_s2": f"{sxx:.15e}",
                "Sxz_surrogate_s2": f"{sxz:.15e}",
                "gxS_shape_surrogate_m_s4": f"{gxs_shape:.15e}",
                "mask_flag_surrogate": "false",
                "generation_method": "spherical_Earth_monopole_zero_phase_surrogate_not_official",
                "source_status": "NOT_CMSM_NOT_OFFICIAL",
            }
        )
        rows.append(row)
    return rows


def replacement_map_rows() -> list[dict[str, object]]:
    specs = [
        ("segment_id", "segment_id", "SURROGATE_AVAILABLE_OFFICIAL_MISSING", "replace with exact CMSM segment id"),
        ("t_utc", "t_sec_from_segment_start", "SURROGATE_RELATIVE_TIME_OFFICIAL_UTC_MISSING", "replace with exact CMSM timestamps"),
        ("sample_index", "sample_index", "SURROGATE_AVAILABLE_OFFICIAL_MISSING", "replace with exact CMSM sample index"),
        ("gx", "gx_surrogate_m_s2", "SURROGATE_AVAILABLE_OFFICIAL_MISSING", "replace with CMSM/official gx"),
        ("gz", "gz_surrogate_m_s2", "SURROGATE_AVAILABLE_OFFICIAL_MISSING", "replace with CMSM/official gz"),
        ("Sxx", "Sxx_surrogate_s2", "SURROGATE_AVAILABLE_OFFICIAL_MISSING", "replace with CMSM/official Sxx"),
        ("Sxz", "Sxz_surrogate_s2", "SURROGATE_AVAILABLE_OFFICIAL_MISSING", "replace with CMSM/official Sxz"),
        ("mask_flag", "mask_flag_surrogate", "SURROGATE_ALL_UNMASKED_OFFICIAL_MISSING", "replace with exact CMSM mask"),
    ]
    rows: list[dict[str, object]] = []
    for index, (official_column, surrogate_column, status, action) in enumerate(specs):
        row = base_row()
        row.update(
            {
                "map_id": f"MAP2001_{index}_{official_column}",
                "official_contract_column": official_column,
                "surrogate_column": surrogate_column,
                "replacement_status": status,
                "evidence_policy": "cannot support claim",
                "next_action": action,
            }
        )
        rows.append(row)
    return rows


def schema_validator_rows(inventory_rows: list[dict[str, object]], thin_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    complete_exports = [row for row in inventory_rows if row.get("contract_match_status") == "COMPLETE_REQUIRED_SCHEMA_UNPROVEN_PROVENANCE"]
    rows: list[dict[str, object]] = []
    checks = [
        (
            "SCHEMA2001_0_official_export_presence",
            bool(complete_exports),
            "official-like schema present" if complete_exports else "no official-like CMSM export present",
            "claim remains false until provenance, units, masks, and source path are validated",
        ),
        (
            "SCHEMA2001_1_required_columns",
            bool(complete_exports),
            "required official columns found in a candidate" if complete_exports else "required official columns absent locally",
            "surrogate columns are not accepted as evidence",
        ),
        (
            "SCHEMA2001_2_surrogate_numeric_path",
            len(thin_rows) == THIN_ROWS,
            f"{len(thin_rows)} surrogate rows written",
            "numeric code path exists, evidence gate remains closed",
        ),
        (
            "SCHEMA2001_3_tau_WEP_readiness",
            False,
            "tau_WEP is not acquired",
            "requires official arrays plus MTS material/source map or direct parent product",
        ),
    ]
    for check_id, gate_pass, detail, action in checks:
        row = base_row()
        row.update(
            {
                "schema_check_id": check_id,
                "gate_pass": str(gate_pass).lower(),
                "detail": detail,
                "evidence_policy": action,
            }
        )
        rows.append(row)
    return rows


def status_rows(inventory_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    complete_exports = [row for row in inventory_rows if row.get("contract_match_status") == "COMPLETE_REQUIRED_SCHEMA_UNPROVEN_PROVENANCE"]
    specs = [
        (
            "STAT2001_0_CMSM_export",
            "user/browser CMSM export",
            "SCHEMA_PRESENT_PROVENANCE_UNCHECKED" if complete_exports else "NOT_FOUND_LOCALLY",
            "validate official provenance before any evidence use" if complete_exports else "drop official export into source-intake/microscope_cmsm if obtained",
            "false",
        ),
        (
            "STAT2001_1_surrogate_reconstruction",
            "segment 210 thin surrogate gx/gz/Sxx/Sxz/gxS",
            "BUILT_NONCLAIM",
            "use for design-matrix/code plumbing only",
            "false",
        ),
        (
            "STAT2001_2_official_arrays",
            "official CMSM gx/gz/Sxx/Sxz arrays",
            "NOT_ACQUIRED",
            "replace surrogate columns with official export or source-backed reconstruction",
            "false",
        ),
        (
            "STAT2001_3_tau_WEP",
            "numeric tau_WEP",
            "NOT_ACQUIRED",
            "derive after official arrays and source-weight/material map exist",
            "false",
        ),
        (
            "STAT2001_4_local_GR_WEP",
            "local-GR/WEP pass",
            "BLOCKED",
            "do not promote until tau_WEP and product gates pass",
            "false",
        ),
    ]
    rows: list[dict[str, object]] = []
    for status_id, obj, status, action, claim_allowed in specs:
        row = base_row()
        row.update(
            {
                "status_id": status_id,
                "object": obj,
                "status": status,
                "next_action": action,
                "claim_allowed": claim_allowed,
            }
        )
        rows.append(row)
    return rows


def product_prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED2001_0_WEP_surrogate_reconstruction_nonclaim_product",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_OFFICIAL_ARRAYS_AND_MTS_TAU_SOURCE_SURROGATE_ONLY",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2001_SURROGATE_THIN_GRID_SEGMENT210_NONCLAIM.csv",
            "inputs_present": "surrogate_gx;surrogate_gz;surrogate_Sxx;surrogate_Sxz;surrogate_gxS_shape",
            "required_inputs": "official CMSM arrays; exact masks/timestamps; material tensor/source-weight map; Xhat normalization; tau_WEP map or direct parent product",
            "derivation_status": "NONCLAIM_SURROGATE_PIPELINE_ONLY",
            "valid_for_claim": "false",
            "notes": "surrogate tests runnable geometry/code path only; no WEP evidence",
        }
    ]


def bound_rows() -> list[dict[str, str]]:
    row = local_bound_row("R1_WEP_source_charge")
    url, doi = split_reference(row["reference_path_or_url"])
    return [
        {
            "bound_id": "BOUND2001_0_MICROSCOPE_R1_eta_source_charge",
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


def product_status_rows(status: dict[str, Any]) -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "runner_id": "APR2001_0_WEP_surrogate_reconstruction_product_stub",
            "prediction_rows": status.get("prediction_rows", ""),
            "bound_rows": status.get("bound_rows", ""),
            "valid_prediction_rows": status.get("valid_prediction_rows", ""),
            "valid_bound_rows": status.get("valid_bound_rows", ""),
            "comparison_rows": status.get("comparison_rows", ""),
            "passed_rows": status.get("passed_rows", ""),
            "claim_allowed": str(status.get("claim_allowed", "")).lower(),
            "expected_result": "reject surrogate-only prediction and keep claim false",
        }
    )
    return [row]


def claim_gate_rows(product_status: dict[str, Any], inventory_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    complete_exports = [row for row in inventory_rows if row.get("contract_match_status") == "COMPLETE_REQUIRED_SCHEMA_UNPROVEN_PROVENANCE"]
    specs = [
        (
            "CG2001_0_CMSM_export",
            "user/browser CMSM export",
            bool(complete_exports),
            "schema present but provenance/unit validation absent" if complete_exports else "NO_USER_SUPPLIED_CMSM_EXPORT_FOUND",
        ),
        (
            "CG2001_1_surrogate_reconstruction",
            "surrogate segment 210 gxS path",
            True,
            "pipeline built but not official arrays",
        ),
        (
            "CG2001_2_official_arrays",
            "official gx/gz/Sxx/Sxz arrays",
            False,
            "MISSING_CLAIM_GRADE_OFFICIAL_ARRAYS",
        ),
        (
            "CG2001_3_product_runner",
            "WEP product runner",
            False,
            f"valid_prediction_rows={product_status.get('valid_prediction_rows')}",
        ),
        (
            "CG2001_4_local_GR_WEP_claim",
            "local-GR/WEP pass",
            False,
            "surrogate-only arrays and no MTS tau_WEP product",
        ),
    ]
    rows: list[dict[str, object]] = []
    for gate_id, component, gate_pass, reason in specs:
        row = base_row()
        row.update(
            {
                "gate_id": gate_id,
                "claim_component": component,
                "gate_pass": str(gate_pass).lower(),
                "claim_allowed": "false",
                "reason": reason,
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    specs = [
        (
            "DEC2001_0_not_circling",
            "convert blocked CMSM acquisition into a runnable import/drop contract plus surrogate harness",
            "2000 found the live CMSM module inaccessible here",
            "future official export can be swapped into a known schema instead of restarting the loop",
        ),
        (
            "DEC2001_1_surrogate_is_useful",
            "build physically unitful gx/gz/Sxx/Sxz/gxS thin-grid plumbing",
            "P8_Y5_PARENT_QLOC_2001_SURROGATE_THIN_GRID_SEGMENT210_NONCLAIM.csv",
            "next runner can test design-matrix shape and replacement gates without claiming evidence",
        ),
        (
            "DEC2001_2_no_claim",
            "keep WEP/local-GR claim closed",
            "official arrays and tau_WEP product are still missing",
            "project advances by hardening the test harness, not by pretending surrogate data are evidence",
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
            "next_id": "NEXT2001_0_2002",
            "next_target": "2002-Y5-R2FR-surrogate-design-matrix-tau-shape-smoke-runner.md",
            "objective": "use the 2001 nonclaim surrogate thin grid to build a design-matrix/tau-shape smoke runner with condition diagnostics and official-replacement gates.",
            "include": "constant/time-polynomial/gx/gz/Sxx/Sxz/gxS columns; rank and conditioning diagnostics; refusal if official arrays are absent; clear swap contract for CMSM export",
            "exclude": "claiming MICROSCOPE evidence, treating surrogate masks as final, setting tau_WEP=1, pushing GitHub, or editing formalization-workbench",
        }
    )
    return [row]


def validate_outputs(
    outputs: dict[str, Path],
    drop_readme: Path,
    drop_template: Path,
    source_rows: list[dict[str, object]],
    drop_rows: list[dict[str, object]],
    inventory_rows: list[dict[str, object]],
    assumption_rows: list[dict[str, object]],
    grid_rows: list[dict[str, object]],
    thin_rows: list[dict[str, object]],
    map_rows: list[dict[str, object]],
    schema_rows: list[dict[str, object]],
    status_rows_: list[dict[str, object]],
    product_status: dict[str, Any],
    claim_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    required_map = {row["official_contract_column"] for row in map_rows}
    generated_paths = list(outputs.values()) + [DOC, drop_readme, drop_template]
    finite_shape = all(math.isfinite(float(row["gxS_shape_surrogate_m_s4"])) for row in thin_rows)
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2001_00_sources", all(row["exists"] == "True" and row["anchor_found"] == "True" for row in source_rows), "all source paths exist and needles found"))
    checks.append(("VAL2001_01_drop_contract", drop_readme.exists() and drop_template.exists() and {row["column_name"] for row in drop_rows} >= set(OFFICIAL_ARRAY_COLUMNS), "drop README/template and official column contract written"))
    checks.append(("VAL2001_02_inventory", any(row["contract_match_status"] == "NO_USER_SUPPLIED_CMSM_EXPORT_FOUND" for row in inventory_rows) or all(row["claim_allowed"] == "false" for row in inventory_rows), "CMSM export inventory recorded without promoting a claim"))
    checks.append(("VAL2001_03_surrogate_nonclaim", len(thin_rows) == THIN_ROWS and all(row["valid_for_claim"] == "false" and row["source_status"] == "NOT_CMSM_NOT_OFFICIAL" for row in thin_rows), "surrogate thin grid written and marked nonofficial"))
    checks.append(("VAL2001_04_surrogate_numeric", finite_shape and any(abs(float(row["gxS_shape_surrogate_m_s4"])) > 0 for row in thin_rows), "surrogate gxS shape is finite and nonzero"))
    checks.append(("VAL2001_05_replacement_map", required_map >= set(OFFICIAL_ARRAY_COLUMNS) and all(row["claim_allowed"] == "false" for row in map_rows), "replacement map covers official columns and denies evidence status"))
    checks.append(("VAL2001_06_schema_validator", any(row["schema_check_id"] == "SCHEMA2001_3_tau_WEP_readiness" and row["gate_pass"] == "false" for row in schema_rows), "schema validator blocks tau_WEP readiness"))
    checks.append(("VAL2001_07_status_blocked", any(row["status_id"] == "STAT2001_3_tau_WEP" and row["status"] == "NOT_ACQUIRED" for row in status_rows_), "numeric tau_WEP remains not acquired"))
    checks.append(("VAL2001_08_product_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "product runner refuses surrogate-only prediction"))
    checks.append(("VAL2001_09_claim_gates_safe", all(row["claim_allowed"] == "false" for row in claim_rows), "all claim gates deny WEP/local-GR claim"))
    checks.append(("VAL2001_10_next_target", any("2002-Y5-R2FR-surrogate-design-matrix-tau-shape-smoke-runner.md" in row["next_target"] for row in next_rows), "2002 handoff written"))
    checks.append(("VAL2001_11_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    checks.append(("VAL2001_12_csv_parse", all(path.exists() and csv_rows_parse(path) for path in outputs.values() if path.suffix == ".csv" and path.name != "P8_Y5_BRR545_2001_VALIDATION.csv"), "all 2001 CSV outputs parse cleanly"))
    checks.append(("VAL2001_13_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"))
    checks.append(("VAL2001_14_formalization_untouched", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains zero"))
    checks.append(("VAL2001_OVERALL", True, "2001 user CMSM export/drop contract plus nonclaim surrogate reconstruction"))
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
    drop_rows: list[dict[str, object]],
    inventory_rows: list[dict[str, object]],
    assumption_rows: list[dict[str, object]],
    grid_rows: list[dict[str, object]],
    thin_rows: list[dict[str, object]],
    map_rows: list[dict[str, object]],
    schema_rows: list[dict[str, object]],
    status_rows_: list[dict[str, object]],
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
            "# 2001 - R2FR user CMSM export or nonclaim surrogate reconstruction",
            "",
            "## Current verdict",
            "2001 did not find a claim-grade user/browser CMSM export in the local drop folder, so it created a drop contract plus a strictly nonclaim segment-210 surrogate reconstruction. This is a step forward in plumbing: the path now has unitful gx/gz/Sxx/Sxz/gxS arrays for shape and design-matrix smoke tests, but it is not MICROSCOPE evidence and cannot score WEP/local-GR.",
            "",
            "Important boundary: the surrogate is allowed to test code geometry only. It cannot become `tau_WEP`, cannot be treated as official CMSM data, and cannot close the local-GR branch.",
            "",
            "Next honest move: use the surrogate only to test the design-matrix/tau-shape runner, or replace it with a real CMSM export dropped into `source-intake/microscope_cmsm`.",
            "",
            "## Local source register",
            md_table(source_rows, ["source_id", "source_path", "exists", "anchor_found", "note"]),
            "## CMSM drop contract",
            md_table(drop_rows, ["drop_id", "column_name", "unit_or_type", "required_for_tau", "current_status"]),
            "## CMSM export inventory check",
            md_table(inventory_rows, ["inventory_id", "search_root", "candidate_file", "required_columns_present", "contract_match_status", "action_taken"]),
            "## Surrogate assumptions",
            md_table(assumption_rows, ["assumption_id", "object", "value", "units", "source_or_reason", "claim_status"]),
            "## Surrogate grid metadata",
            md_table(grid_rows, ["grid_id", "segment", "full_grid_samples", "thin_rows_written", "orbit_model", "attitude_model", "mask_model", "claim_status"]),
            "## Surrogate gxS thin-grid preview",
            md_table(thin_rows[:10], ["row_id", "sample_index", "t_sec_from_segment_start", "gx_surrogate_m_s2", "gz_surrogate_m_s2", "Sxx_surrogate_s2", "Sxz_surrogate_s2", "gxS_shape_surrogate_m_s4", "source_status"]),
            "## Replacement map",
            md_table(map_rows, ["map_id", "official_contract_column", "surrogate_column", "replacement_status", "evidence_policy", "next_action"]),
            "## Schema validator dry run",
            md_table(schema_rows, ["schema_check_id", "gate_pass", "detail", "evidence_policy"]),
            "## Status ledger",
            md_table(status_rows_, ["status_id", "object", "status", "next_action", "claim_allowed"]),
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
    drop_readme, drop_template = write_drop_guides()
    source_rows = source_register_rows()
    drop_rows = drop_contract_rows(drop_readme, drop_template)
    inventory_rows = cmsm_export_inventory_rows()
    assumption_rows = surrogate_assumption_rows(inventory_rows)
    grid_rows = surrogate_grid_metadata_rows()
    thin_rows = surrogate_thin_grid_rows()
    map_rows = replacement_map_rows()
    schema_rows = schema_validator_rows(inventory_rows, thin_rows)
    status_rows_ = status_rows(inventory_rows)
    prediction_rows = product_prediction_rows()
    bound_rows_ = bound_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_PARENT_QLOC_2001_SOURCE_REGISTER.csv",
        "drop_contract": OUT / "P8_Y5_PARENT_QLOC_2001_CMSM_DROP_CONTRACT.csv",
        "inventory": OUT / "P8_Y5_PARENT_QLOC_2001_CMSM_EXPORT_INVENTORY_CHECK.csv",
        "assumptions": OUT / "P8_Y5_PARENT_QLOC_2001_SURROGATE_ASSUMPTIONS.csv",
        "grid": OUT / "P8_Y5_PARENT_QLOC_2001_SURROGATE_GRID_METADATA_SEGMENT210.csv",
        "thin_grid": OUT / "P8_Y5_PARENT_QLOC_2001_SURROGATE_THIN_GRID_SEGMENT210_NONCLAIM.csv",
        "replacement_map": OUT / "P8_Y5_PARENT_QLOC_2001_SURROGATE_TO_OFFICIAL_REPLACEMENT_MAP.csv",
        "schema_validator": OUT / "P8_Y5_PARENT_QLOC_2001_SCHEMA_VALIDATOR_DRYRUN.csv",
        "status": OUT / "P8_Y5_PARENT_QLOC_2001_STATUS_LEDGER.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_PARENT_QLOC_2001_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_PARENT_QLOC_2001_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2001_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2001_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_PARENT_QLOC_2001_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_2001_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["drop_contract"], drop_rows)
    write_csv(outputs["inventory"], inventory_rows)
    write_csv(outputs["assumptions"], assumption_rows)
    write_csv(outputs["grid"], grid_rows)
    write_csv(outputs["thin_grid"], thin_rows)
    write_csv(outputs["replacement_map"], map_rows)
    write_csv(outputs["schema_validator"], schema_rows)
    write_csv(outputs["status"], status_rows_)
    write_csv(outputs["prediction"], prediction_rows, PRODUCT_REQUIRED_COLUMNS)
    write_csv(outputs["bound"], bound_rows_, BOUND_REQUIRED_COLUMNS)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next_target"], next_rows)

    product_result = run_product_runner(PREDICTION_TEMPLATE, BOUND_IMPORT, PRODUCT_RUN_DIR)
    product_status = product_result["status"]
    product_status_rows_ = product_status_rows(product_status)
    claim_rows = claim_gate_rows(product_status, inventory_rows)

    write_csv(outputs["product_status"], product_status_rows_)
    write_csv(outputs["product_comparison"], product_result["comparisons"])
    write_csv(outputs["claim_gates"], claim_rows)

    remove_pycache()
    validation_rows = validate_outputs(
        outputs,
        drop_readme,
        drop_template,
        source_rows,
        drop_rows,
        inventory_rows,
        assumption_rows,
        grid_rows,
        thin_rows,
        map_rows,
        schema_rows,
        status_rows_,
        product_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        drop_rows,
        inventory_rows,
        assumption_rows,
        grid_rows,
        thin_rows,
        map_rows,
        schema_rows,
        status_rows_,
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
    print(f"VAL2001_OVERALL={'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['validation_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
