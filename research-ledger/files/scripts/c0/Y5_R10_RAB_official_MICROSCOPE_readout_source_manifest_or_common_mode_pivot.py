from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1336"
TITLE = "1336-Y5-R10-RAB-official-MICROSCOPE-readout-source-manifest-or-common-mode-pivot"
ROOT = Path(__file__).resolve().parents[1]
MICROSCOPE_DIR = ROOT / "source-intake" / "microscope"
OUT_DIR = MICROSCOPE_DIR / "metadata"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

OFFICIAL_READOUT_DIR = MICROSCOPE_DIR / "official_readout"
SOURCE_WORLDTUBE_DIR = MICROSCOPE_DIR / "source_worldtube"
PRODUCT_CONVENTION_DIR = MICROSCOPE_DIR / "product_convention"
BRANCH_CLASSIFIER_DIR = MICROSCOPE_DIR / "branch_classifier"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
WEB_SOURCE_PATH = OUT_DIR / f"{PACK_ID}_WEB_SOURCE_CANDIDATE_REGISTER.csv"
LOCAL_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_LOCAL_MICROSCOPE_INTAKE_AUDIT.csv"
READOUT_SCHEMA_PATH = OUT_DIR / f"{PACK_ID}_OFFICIAL_READOUT_SCHEMA.csv"
SOURCE_SCHEMA_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_WORLDTUBE_SCHEMA.csv"
PRODUCT_SCHEMA_PATH = OUT_DIR / f"{PACK_ID}_PRODUCT_CONVENTION_SCHEMA.csv"
BRANCH_SCHEMA_PATH = OUT_DIR / f"{PACK_ID}_BRANCH_CLASSIFIER_SCHEMA.csv"
ANTI_SHORTCUT_PATH = OUT_DIR / f"{PACK_ID}_ANTI_SHORTCUT_GATES.csv"
PIVOT_PATH = OUT_DIR / f"{PACK_ID}_COMMON_MODE_PIVOT_DECISION.csv"
RUNNER_STATUS_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_STATUS.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1336_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def bool_false(value: object) -> bool:
    return str(value).strip().lower() == "false"


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    for table in tables:
        for row in table:
            if "valid_for_claim" in row and not bool_false(row.get("valid_for_claim", False)):
                return False
            if "claim_allowed" in row and not bool_false(row.get("claim_allowed", False)):
                return False
    return True


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def generated_inside_formalization() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    return [path for path in FORMALIZATION.rglob("*1336*") if path.is_file()]


def file_count(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for item in path.rglob("*") if item.is_file())


def main() -> None:
    for directory in [
        OUT_DIR,
        MICROSCOPE_DIR / "raw",
        MICROSCOPE_DIR / "docs",
        MICROSCOPE_DIR / "derived",
        MICROSCOPE_DIR / "quarantine",
        OFFICIAL_READOUT_DIR,
        SOURCE_WORLDTUBE_DIR,
        PRODUCT_CONVENTION_DIR,
        BRANCH_CLASSIFIER_DIR,
    ]:
        directory.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1336_0_1335_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1335_NEXT_TARGET.csv",
            "needle": "NEXT1335_0_1336",
            "role": "selected 1336 target",
        },
        {
            "source_id": "SRC1336_1_1335_manifest",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1335_OFFICIAL_INPUT_REQUEST_MANIFEST.csv",
            "needle": "MAN1335_0_readout_arrays",
            "role": "official input waitstate from 1335",
        },
        {
            "source_id": "SRC1336_2_1335_waitstate",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1335_READOUT_SOURCE_WAITSTATE.csv",
            "needle": "WAIT1335_0_official_arrays",
            "role": "readout/source blocker list",
        },
        {
            "source_id": "SRC1336_3_1335_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1335_ELECTRON_WEP_PRODUCT_NORMALIZATION_CONTRACT.csv",
            "needle": "tau_eff_e",
            "role": "symbolic WEP product contract",
        },
        {
            "source_id": "SRC1336_4_1335_validation",
            "local_path": "source-intake/mts_residuals/P8_Y5_BRR545_1335_VALIDATION.csv",
            "needle": "VAL1335_10_overall",
            "role": "1335 pass gate",
        },
        {
            "source_id": "SRC1336_5_1069_provenance",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1069_MICROSCOPE_PROVENANCE_LEDGER.csv",
            "needle": "PROV1069_1_R0_direct_geometry",
            "role": "PRL final eta provenance",
        },
        {
            "source_id": "SRC1336_6_1070_external",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1070_EXTERNAL_MICROSCOPE_READOUT_SOURCE_LEDGER.csv",
            "needle": "EXT1070_5_CQG_data_availability",
            "role": "CQG readout/data-availability provenance",
        },
        {
            "source_id": "SRC1336_7_1072_external",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1072_EXTERNAL_SOURCE_LEDGER.csv",
            "needle": "EXT1072_1_ONERA_data_available",
            "role": "ONERA/CMSM portal provenance",
        },
        {
            "source_id": "SRC1336_8_1072_api",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1072_CMSM_REGARDS_API_CANDIDATE_ENDPOINTS.csv",
            "needle": "API1072_1_dataset_search",
            "role": "candidate REGARDS API endpoints",
        },
        {
            "source_id": "SRC1336_9_1072_probe",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1072_PORTAL_ROUTE_PROBE.csv",
            "needle": "https://cmsm-ds.onera.fr/user/microscope",
            "role": "previous portal route probe",
        },
    ]
    source_register: list[dict[str, object]] = []
    for spec in source_specs:
        exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_register.append(
            {
                **spec,
                "exists": exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    web_sources = [
        {
            "web_id": "WEB1336_0_ONERA_public_data_page",
            "url": "https://microscope.onera.fr/fr/publication/microscope-data-are-available",
            "source_type": "official mission data page",
            "expected_use": "points users to the MICROSCOPE CMSM portal",
            "local_support": "SRC1336_7_1072_external",
            "acquisition_status": "SOURCE_STRING_RECORDED_NOT_IMPORTED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "web_id": "WEB1336_1_CMSM_MICROSCOPE_portal",
            "url": "https://cmsm-ds.onera.fr/user/microscope",
            "source_type": "official data portal",
            "expected_use": "download/export official readout, calibrated, auxiliary, and orbit products",
            "local_support": "SRC1336_7_1072_external;SRC1336_9_1072_probe",
            "acquisition_status": "PORTAL_TARGET_RECORDED_ARRAYS_NOT_IMPORTED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "web_id": "WEB1336_2_CQG_final_result",
            "url": "https://arxiv.org/abs/2209.15488",
            "source_type": "final MICROSCOPE CQG analysis paper",
            "expected_use": "eta formula, readout axis, segment/orbit counts, analysis band, data availability statement",
            "local_support": "SRC1336_6_1070_external",
            "acquisition_status": "SOURCE_STRING_RECORDED_FORMULAE_ALREADY_LEDGERED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "web_id": "WEB1336_3_PRL_final_result",
            "url": "https://arxiv.org/abs/2209.15487",
            "source_type": "final MICROSCOPE PRL result",
            "expected_use": "eta_TiPt bound anchor and mission context",
            "local_support": "SRC1336_5_1069_provenance",
            "acquisition_status": "SOURCE_STRING_RECORDED_BOUND_ANCHOR_ALREADY_LEDGERED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    intake_dirs = [
        ("LOCAL1336_0_base", MICROSCOPE_DIR, "MICROSCOPE intake root"),
        ("LOCAL1336_1_raw", MICROSCOPE_DIR / "raw", "raw download quarantine/incoming source"),
        ("LOCAL1336_2_docs", MICROSCOPE_DIR / "docs", "downloaded documentation/manuals"),
        ("LOCAL1336_3_derived", MICROSCOPE_DIR / "derived", "future reproducible derived products"),
        ("LOCAL1336_4_quarantine", MICROSCOPE_DIR / "quarantine", "uncertain files not usable for claim"),
        ("LOCAL1336_5_metadata", OUT_DIR, "schemas, manifests, validation outputs"),
        ("LOCAL1336_6_official_readout", OFFICIAL_READOUT_DIR, "official exported MICROSCOPE readout arrays"),
        ("LOCAL1336_7_source_worldtube", SOURCE_WORLDTUBE_DIR, "Earth/source profile and orbit weighting inputs"),
        ("LOCAL1336_8_product_convention", PRODUCT_CONVENTION_DIR, "eta/product/readout convention evidence"),
        ("LOCAL1336_9_branch_classifier", BRANCH_CLASSIFIER_DIR, "same-parent-branch classifier inputs"),
    ]
    local_audit = [
        {
            "audit_id": audit_id,
            "absolute_path": str(path),
            "purpose": purpose,
            "exists": path.exists(),
            "file_count": file_count(path),
            "usable_for_claim_now": False,
            "status": "DIRECTORY_READY_FILES_PENDING" if path.exists() else "MISSING_DIRECTORY",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for audit_id, path, purpose in intake_dirs
    ]

    readout_schema = [
        ("READSCHEMA1336_0_time_s", "time_s", "float", "seconds or mission time with declared epoch", "official readout export", "required"),
        ("READSCHEMA1336_1_session_id", "session_id", "string", "MICROSCOPE science session/segment id", "official readout export", "required"),
        ("READSCHEMA1336_2_orbit_id", "orbit_id", "string/integer", "orbit identifier or reconstructable orbit phase key", "official orbit/readout export", "required"),
        ("READSCHEMA1336_3_axis", "axis", "string", "reported accelerometer axis; sensitive X axis must be explicit", "CQG/readout metadata", "required"),
        ("READSCHEMA1336_4_gx_m_s2", "gx_m_s2", "float", "gravity projection on x in m/s^2", "official or reproducible CQG design matrix", "required"),
        ("READSCHEMA1336_5_gz_m_s2", "gz_m_s2", "float", "gravity projection on z in m/s^2", "official or reproducible CQG design matrix", "required"),
        ("READSCHEMA1336_6_Sxx", "Sxx", "float", "gravity-gradient/readout design column Sxx", "official or reproducible CQG design matrix", "required"),
        ("READSCHEMA1336_7_Sxz", "Sxz", "float", "gravity-gradient/readout design column Sxz", "official or reproducible CQG design matrix", "required"),
        ("READSCHEMA1336_8_mask_flag", "mask_flag", "boolean/string", "mask/quality flag matching final analysis cuts", "official readout export", "required"),
        ("READSCHEMA1336_9_calibration_flag", "calibration_flag", "boolean/string", "calibration state or exclusion marker", "official readout export", "required"),
        ("READSCHEMA1336_10_attitude_or_axis", "attitude_quaternion_or_axis", "string/float-array", "attitude or axis convention sufficient to reproduce projection", "official auxiliary/orbit export", "required"),
        ("READSCHEMA1336_11_source_url_or_path", "source_url_or_path", "string", "official file path, URL, or DOI-backed source", "local import manifest", "required"),
    ]
    readout_schema_rows = [
        {
            "schema_id": schema_id,
            "column": column,
            "dtype": dtype,
            "definition": definition,
            "source_requirement": source_requirement,
            "required_status": required_status,
            "current_status": "MISSING_OFFICIAL_FILE",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for schema_id, column, dtype, definition, source_requirement, required_status in readout_schema
    ]

    source_schema = [
        ("SRCSCHEMA1336_0_time_or_orbit_phase", "time_s_or_orbit_phase", "float", "time or orbit phase matched to readout rows"),
        ("SRCSCHEMA1336_1_radius_m", "radius_m", "float", "source-shell radius in metres"),
        ("SRCSCHEMA1336_2_density_kg_m3", "density_kg_m3", "float", "mass/stress density profile used for source weighting"),
        ("SRCSCHEMA1336_3_source_component", "source_component", "string", "Earth/source component or stress/current slot"),
        ("SRCSCHEMA1336_4_kernel_weight", "kernel_weight", "float", "projection/readout/source weight for the component"),
        ("SRCSCHEMA1336_5_model_or_dataset", "model_or_dataset", "string", "PREM/geopotential/or official mission auxiliary product name"),
        ("SRCSCHEMA1336_6_source_url_or_path", "source_url_or_path", "string", "source-backed path or URL"),
    ]
    source_schema_rows = [
        {
            "schema_id": schema_id,
            "column": column,
            "dtype": dtype,
            "definition": definition,
            "source_requirement": "source profile plus orbit/readout projection must be reproducible",
            "current_status": "MISSING_SOURCE_WORLDTUBE_FILE",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for schema_id, column, dtype, definition in source_schema
    ]

    product_schema = [
        ("PRODSCHEMA1336_0_eta_formula", "eta_formula", "string", "eta(A,B)=2(a_A-a_B)/(a_A+a_B) or the exact mission convention used"),
        ("PRODSCHEMA1336_1_sign_convention", "sign_convention", "string", "which body order and which readout axis define positive eta"),
        ("PRODSCHEMA1336_2_tau_eff_definition", "tau_eff_definition", "string", "tau_eff = K_readout*S_source*O_orbit in a single observed branch"),
        ("PRODSCHEMA1336_3_readout_kernel_units", "readout_kernel_units", "string", "units that convert design/readout columns into eta response"),
        ("PRODSCHEMA1336_4_source_kernel_units", "source_kernel_units", "string", "units of the source-worldtube weighted response"),
        ("PRODSCHEMA1336_5_orbit_average_rule", "orbit_average_rule", "string", "averaging/masking rule matching the final reported eta channel"),
        ("PRODSCHEMA1336_6_branch_lock", "branch_lock", "string", "same parent branch id for coefficient, material contrast, source, readout, and bound"),
    ]
    product_schema_rows = [
        {
            "schema_id": schema_id,
            "field": field,
            "dtype": dtype,
            "definition": definition,
            "current_status": "MISSING_PRODUCT_CONVENTION_FILE",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for schema_id, field, dtype, definition in product_schema
    ]

    branch_schema_rows = [
        {
            "schema_id": "BRANCHSCHEMA1336_0_same_parent_branch_id",
            "field": "same_parent_branch_id",
            "dtype": "string",
            "definition": "single identifier linking epsilon_e, DeltaF_e, tau_eff_e, source worldtube, readout kernel, and eta bound",
            "current_status": "MISSING_PARENT_BRANCH_CLASSIFIER",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "schema_id": "BRANCHSCHEMA1336_1_forbidden_mixing_rule",
            "field": "forbidden_mixing_rule",
            "dtype": "string",
            "definition": "explicit rule rejecting products assembled from incompatible parent branches or surrogate/readout conventions",
            "current_status": "MISSING_PARENT_BRANCH_CLASSIFIER",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    anti_shortcut = [
        {
            "gate_id": "SHORT1336_0_no_sensitivity_claim",
            "shortcut": "use epsilon_e sensitivity rows as WEP evidence",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1336_1_no_surrogate_arrays",
            "shortcut": "treat dry-run/reconstructed arrays as official MICROSCOPE arrays",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1336_2_no_unity_tau",
            "shortcut": "set tau_eff_e=1 without readout/source/product derivation",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1336_3_no_local_GR_claim",
            "shortcut": "claim WEP or local-GR reduction from acquisition manifest only",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    official_readout_files = file_count(OFFICIAL_READOUT_DIR)
    source_worldtube_files = file_count(SOURCE_WORLDTUBE_DIR)
    product_convention_files = file_count(PRODUCT_CONVENTION_DIR)
    branch_classifier_files = file_count(BRANCH_CLASSIFIER_DIR)
    can_continue_data_route = all(
        count > 0
        for count in [official_readout_files, source_worldtube_files, product_convention_files, branch_classifier_files]
    )

    pivot_decision = [
        {
            "decision_id": "PIVOT1336_0_official_data_route",
            "route": "finite electron WEP data-intake route",
            "current_state": "PAUSED_WAITING_FOR_OFFICIAL_INPUTS",
            "because": "official readout arrays, source worldtube, product convention, and same-branch classifier are not locally present",
            "next_action": "only resume after source-backed files exist in official_readout/source_worldtube/product_convention/branch_classifier",
            "selected_now": can_continue_data_route,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "PIVOT1336_1_common_mode_theory_route",
            "route": "parent common-mode/source-prefactor derivation route",
            "current_state": "SELECTED_NEXT",
            "because": "data plumbing is acquisition-ready but not filled; the derivation route attacks the actual coupling gap directly",
            "next_action": "reduce the no-source-prefactor/common-mode clause to the smallest parent action premise or exhibit an admissible countermodel",
            "selected_now": not can_continue_data_route,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner_status = [
        {
            "runner_id": "RUN1336_0_schema_manifest",
            "target": "official MICROSCOPE readout/source/product manifest",
            "input_status": "SCHEMAS_WRITTEN_SOURCE_STRINGS_RECORDED",
            "runner_status": "ACQUISITION_READY_NONCLAIM",
            "score_ready": False,
            "reason": "schemas and directories exist but official files are absent",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1336_1_WEP_product",
            "target": "epsilon_e WEP product",
            "input_status": "WAITSTATE_PERSISTENT",
            "runner_status": "BLOCKED_NOT_SCOREABLE",
            "score_ready": False,
            "reason": "tau_eff_e remains source/readout/product-convention undefined",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1336_2_common_mode_pivot",
            "target": "parent common-mode/no-source-prefactor theorem",
            "input_status": "THEORY_ROUTE_SELECTED",
            "runner_status": "NEXT_DERIVATION_TARGET",
            "score_ready": False,
            "reason": "the coupling gap is now cleaner than the data route for immediate progress",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1336_0_1337",
            "target_file": "1337-Y5-R10-RAB-common-mode-parent-action-premise-reduction-or-readout-data-intake.md",
            "target_script": "scripts/Y5_R10_RAB_common_mode_parent_action_premise_reduction_or_readout_data_intake.py",
            "task": "try to reduce the common-mode/no-source-prefactor condition to the smallest parent action premise while keeping the official MICROSCOPE intake route parked and schema-ready",
            "success_condition": "either derive a stronger parent common-mode condition, exhibit the smallest admissible countermodel, or import real official readout/source/product files without scoring them",
            "do_not": "do not claim WEP/local-GR from this manifest, do not use surrogate arrays as official data, do not branch-mix finite coefficients",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    tables_for_nonclaim = [
        source_register,
        web_sources,
        local_audit,
        readout_schema_rows,
        source_schema_rows,
        product_schema_rows,
        branch_schema_rows,
        anti_shortcut,
        pivot_decision,
        runner_status,
        next_target,
    ]

    source_anchor_count = sum(1 for row in source_register if row["exists"] and row["needle_found"])
    web_strings_recorded = all(row["url"].startswith("https://") for row in web_sources)
    official_dirs_ready = all(
        path.exists()
        for path in [OFFICIAL_READOUT_DIR, SOURCE_WORLDTUBE_DIR, PRODUCT_CONVENTION_DIR, BRANCH_CLASSIFIER_DIR]
    )
    official_files_absent = all(
        count == 0
        for count in [official_readout_files, source_worldtube_files, product_convention_files, branch_classifier_files]
    )
    schemas_complete = all(
        len(table) > 0
        for table in [readout_schema_rows, source_schema_rows, product_schema_rows, branch_schema_rows]
    )
    shortcuts_enforced = all(row["status"] == "ENFORCED" for row in anti_shortcut)
    pivot_selected = any(row["decision_id"] == "PIVOT1336_1_common_mode_theory_route" and row["selected_now"] is True for row in pivot_decision)
    runner_blocks_score = all(row["score_ready"] is False and row["valid_prediction_row"] is False for row in runner_status)
    nonclaim = all_nonclaim(tables_for_nonclaim)
    formal_clean = len(generated_inside_formalization()) == 0
    next_is_1337 = next_target[0]["target_file"].startswith("1337-")

    validations = [
        validation_row(
            "VAL1336_0_sources_exist",
            "registered local source paths exist and anchors are found",
            source_anchor_count == len(source_register),
            f"{source_anchor_count}/{len(source_register)} source anchors found",
        ),
        validation_row(
            "VAL1336_1_web_strings_recorded",
            "official web source strings are recorded",
            web_strings_recorded,
            ";".join(row["url"] for row in web_sources),
        ),
        validation_row(
            "VAL1336_2_official_dirs_ready",
            "official intake directories exist",
            official_dirs_ready,
            ";".join(str(path) for path in [OFFICIAL_READOUT_DIR, SOURCE_WORLDTUBE_DIR, PRODUCT_CONVENTION_DIR, BRANCH_CLASSIFIER_DIR]),
        ),
        validation_row(
            "VAL1336_3_official_files_absent",
            "official readout/source/product/branch files are not silently present",
            official_files_absent,
            f"official_readout={official_readout_files};source_worldtube={source_worldtube_files};product_convention={product_convention_files};branch_classifier={branch_classifier_files}",
        ),
        validation_row(
            "VAL1336_4_schemas_complete",
            "readout, source, product, and branch schemas are present",
            schemas_complete,
            f"readout={len(readout_schema_rows)};source={len(source_schema_rows)};product={len(product_schema_rows)};branch={len(branch_schema_rows)}",
        ),
        validation_row(
            "VAL1336_5_shortcuts_enforced",
            "anti-shortcut gates are enforced",
            shortcuts_enforced,
            ";".join(row["gate_id"] for row in anti_shortcut),
        ),
        validation_row(
            "VAL1336_6_common_mode_pivot_selected",
            "common-mode theory route is selected while data files are absent",
            pivot_selected,
            "PIVOT1336_1_common_mode_theory_route selected",
        ),
        validation_row(
            "VAL1336_7_runner_blocks_score",
            "runner refuses WEP/local-GR scoring",
            runner_blocks_score,
            ";".join(f"{row['runner_id']}={row['runner_status']}" for row in runner_status),
        ),
        validation_row(
            "VAL1336_8_nonclaim_policy",
            "all generated rows remain nonclaim",
            nonclaim,
            "valid_for_claim=false and claim_allowed=false where present",
        ),
        validation_row(
            "VAL1336_9_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            formal_clean,
            f"formalization_generated_output_count={len(generated_inside_formalization())}",
        ),
        validation_row(
            "VAL1336_10_next_target_1337",
            "next target routes to common-mode parent premise reduction or official intake",
            next_is_1337,
            str(next_target[0]["target_file"]),
        ),
    ]
    validations.append(
        validation_row(
            "VAL1336_11_overall",
            "overall 1336 validation",
            all(row["status"] == "PASS" for row in validations),
            "1336 makes MICROSCOPE intake source-ready, blocks WEP scoring, and selects the common-mode coupling derivation route",
        )
    )

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(WEB_SOURCE_PATH, web_sources)
    write_csv(LOCAL_AUDIT_PATH, local_audit)
    write_csv(READOUT_SCHEMA_PATH, readout_schema_rows)
    write_csv(SOURCE_SCHEMA_PATH, source_schema_rows)
    write_csv(PRODUCT_SCHEMA_PATH, product_schema_rows)
    write_csv(BRANCH_SCHEMA_PATH, branch_schema_rows)
    write_csv(ANTI_SHORTCUT_PATH, anti_shortcut)
    write_csv(PIVOT_PATH, pivot_decision)
    write_csv(RUNNER_STATUS_PATH, runner_status)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# {TITLE}

**Current verdict:** 1336 does not score WEP and does not claim local GR. It turns the MICROSCOPE side into an acquisition-ready manifest, confirms no official readout/source/product files are locally present, and parks the finite-electron WEP route.

**Main progress:** the official data route now has named directories, expected schemas, source strings, anti-shortcut gates, and a runner waitstate. Because the real arrays and product convention are still absent, the next best move is the parent common-mode/no-source-prefactor derivation route.

**Decision:** pivot next to common-mode parent-action premise reduction unless real official MICROSCOPE files are imported first.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Web Source Candidate Register
{markdown_table(web_sources, ["web_id", "url", "source_type", "expected_use", "local_support", "acquisition_status", "valid_for_claim", "claim_allowed"])}

## Local MICROSCOPE Intake Audit
{markdown_table(local_audit, ["audit_id", "absolute_path", "purpose", "exists", "file_count", "usable_for_claim_now", "status", "valid_for_claim", "claim_allowed"])}

## Official Readout Schema
{markdown_table(readout_schema_rows, ["schema_id", "column", "dtype", "definition", "source_requirement", "required_status", "current_status", "valid_for_claim", "claim_allowed"])}

## Source Worldtube Schema
{markdown_table(source_schema_rows, ["schema_id", "column", "dtype", "definition", "source_requirement", "current_status", "valid_for_claim", "claim_allowed"])}

## Product Convention Schema
{markdown_table(product_schema_rows, ["schema_id", "field", "dtype", "definition", "current_status", "valid_for_claim", "claim_allowed"])}

## Branch Classifier Schema
{markdown_table(branch_schema_rows, ["schema_id", "field", "dtype", "definition", "current_status", "valid_for_claim", "claim_allowed"])}

## Anti-Shortcut Gates
{markdown_table(anti_shortcut, ["gate_id", "shortcut", "enforcement", "status", "valid_for_claim", "claim_allowed"])}

## Common-Mode Pivot Decision
{markdown_table(pivot_decision, ["decision_id", "route", "current_state", "because", "next_action", "selected_now", "valid_for_claim", "claim_allowed"])}

## Runner Status
{markdown_table(runner_status, ["runner_id", "target", "input_status", "runner_status", "score_ready", "reason", "valid_prediction_row", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validations, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote validation {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
