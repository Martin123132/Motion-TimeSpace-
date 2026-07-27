from __future__ import annotations

import csv
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
SOURCE_DIR = MICROSCOPE / "branch_locked_wep" / "source"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1704"
DROP = MICROSCOPE / "branch_locked_wep" / "drop-folder" / "1704"
DROP_LIVE = DROP / "live"
DROP_TEMPLATES = DROP / "templates"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1704-Y5-R2FR-MICROSCOPE-parser-shell-dry-run-or-manual-data-request.md"
REQUEST_DOC = SOURCE_DIR / "MICROSCOPE_WEP_data_request_update_1704.md"
DROP_README = DROP / "README_DROP_FILES_1704.md"
DROP_MANIFEST_TEMPLATE = DROP_TEMPLATES / "P_WEP_tau_parser_manifest_TEMPLATE.json"

SOURCE_FILES = {
    "1703_doc": ROOT / "1703-Y5-R2FR-WEP-source-weight-product-first-fill-or-MICROSCOPE-parser-shell.md",
    "1703_validation": OUT / "P8_Y5_BRR545_1703_VALIDATION.csv",
    "1703_requirements": OUT / "P8_Y5_PARENT_QLOC_1703_MICROSCOPE_PARSER_SHELL_REQUIREMENTS.csv",
    "1703_dryrun": OUT / "P8_Y5_PARENT_QLOC_1703_MICROSCOPE_PARSER_DRY_RUN.csv",
    "1703_next": OUT / "P8_Y5_PARENT_QLOC_1703_NEXT_TARGET.csv",
    "1703_manifest_template": MICROSCOPE / "quarantine" / "1703" / "input" / "P_WEP_tau_parser_manifest_TEMPLATE.json",
    "1699_request_template": SOURCE_DIR / "MICROSCOPE_WEP_data_request_template_1699.md",
    "1482_web_candidates": OUT / "P8_Y5_R10_1482_OFFICIAL_WEB_SOURCE_CANDIDATES.csv",
    "1482_manifest": OUT / "P8_Y5_R10_1482_OFFICIAL_INPUT_MANIFEST_UPDATE.csv",
    "product_convention_live": MICROSCOPE / "product_convention" / "P_WEP_eta_product_convention.csv",
    "branch_lock_live": MICROSCOPE / "branch_classifier" / "P_WEP_same_parent_branch_lock.csv",
}

NEEDLES = {
    "1703_doc": ["HARD_BLOCKED_TO_PARSER_SHELL", "NEXT1703_0_primary"],
    "1703_validation": ["VAL1703_OVERALL", "PASS"],
    "1703_requirements": ["PSR1703_0_readout_matrix", "P_WEP_tau_parser_manifest.json"],
    "1703_dryrun": ["PDR1703_8_overall", "REFUSED_MISSING_REQUIRED_INPUTS"],
    "1703_next": ["1704-Y5-R2FR-MICROSCOPE-parser-shell-dry-run-or-manual-data-request.md", "selected"],
    "1703_manifest_template": ["template_only_not_live", "required_artifacts"],
    "1699_request_template": ["Requested Items", "Non-Claim Guardrail"],
    "1482_web_candidates": ["WEB1482_0_CNES_project", "WEB1482_2_PRL_arxiv"],
    "1482_manifest": ["MAN1482_0_live_readout", "MISSING_REQUIRED_LIVE_FILE"],
    "product_convention_live": ["PRODUCT_CONVENTION_OFFICIAL_PARTIAL_EXTRACTION_NONCLAIM", "False"],
    "branch_lock_live": ["BRANCH_CLASSIFIER_FIRST_FILL_NONCLAIM", "False"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1704_SOURCE_REGISTER.csv"
DROP_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1704_DROP_FOLDER_CONTRACT.csv"
DROP_INVENTORY = OUT / "P8_Y5_PARENT_QLOC_1704_DROP_FOLDER_INVENTORY.csv"
SCHEMA_PRECHECK = OUT / "P8_Y5_PARENT_QLOC_1704_SCHEMA_PRECHECK.csv"
PARSER_RESULT = OUT / "P8_Y5_PARENT_QLOC_1704_PARSER_DRY_RUN_RESULT.csv"
REQUEST_UPDATE = OUT / "P8_Y5_PARENT_QLOC_1704_MANUAL_DATA_REQUEST_UPDATE.csv"
COMPUTATION_PLAN = OUT / "P8_Y5_PARENT_QLOC_1704_IF_UNLOCKED_COMPUTATION_PLAN.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1704_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1704_NEXT_TARGET.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1704_CLAIM_GATE.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1704_VALIDATION.csv"

GENERATED_CSVS = [
    SOURCE_REGISTER,
    DROP_CONTRACT,
    DROP_INVENTORY,
    SCHEMA_PRECHECK,
    PARSER_RESULT,
    REQUEST_UPDATE,
    COMPUTATION_PLAN,
    DECISION,
    NEXT_TARGET,
    CLAIM_GATE,
]

CLAIM_CHECKED_CSVS = [
    DROP_CONTRACT,
    DROP_INVENTORY,
    SCHEMA_PRECHECK,
    PARSER_RESULT,
    REQUEST_UPDATE,
    COMPUTATION_PLAN,
    DECISION,
    NEXT_TARGET,
    CLAIM_GATE,
]

COPY_TARGETS = {
    DROP_CONTRACT: [
        QUARANTINE / "DROP_FOLDER_CONTRACT.csv",
        BRANCH_RESIDUALS / "R2FR_drop_folder_contract_1704.csv",
        QUEUE / "JR1704_DROP_FOLDER_CONTRACT.csv",
    ],
    DROP_INVENTORY: [
        QUARANTINE / "DROP_FOLDER_INVENTORY.csv",
        BRANCH_RESIDUALS / "R2FR_drop_folder_inventory_1704.csv",
        QUEUE / "JR1704_DROP_FOLDER_INVENTORY.csv",
    ],
    SCHEMA_PRECHECK: [
        QUARANTINE / "SCHEMA_PRECHECK.csv",
        BRANCH_RESIDUALS / "R2FR_schema_precheck_1704.csv",
        QUEUE / "JR1704_SCHEMA_PRECHECK.csv",
    ],
    PARSER_RESULT: [
        QUARANTINE / "PARSER_DRY_RUN_RESULT.csv",
        BRANCH_RESIDUALS / "R2FR_parser_dry_run_result_1704.csv",
        QUEUE / "JR1704_PARSER_DRY_RUN_RESULT.csv",
    ],
    REQUEST_UPDATE: [
        QUARANTINE / "MANUAL_DATA_REQUEST_UPDATE.csv",
        BRANCH_RESIDUALS / "R2FR_manual_data_request_update_1704.csv",
        QUEUE / "JR1704_MANUAL_DATA_REQUEST_UPDATE.csv",
    ],
    COMPUTATION_PLAN: [
        QUARANTINE / "IF_UNLOCKED_COMPUTATION_PLAN.csv",
        BRANCH_RESIDUALS / "R2FR_if_unlocked_computation_plan_1704.csv",
        QUEUE / "JR1704_IF_UNLOCKED_COMPUTATION_PLAN.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1704.csv",
        QUEUE / "JR1704_NEXT_TARGET.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_1704.csv",
        QUEUE / "JR1704_CLAIM_GATE.csv",
    ],
}


def artifact_contracts() -> list[dict[str, Any]]:
    return [
        {
            "artifact_id": "ART1704_0_readout",
            "artifact": "P_WEP_K_CMSM_readout.csv",
            "canonical_path": MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout.csv",
            "drop_path": DROP_LIVE / "P_WEP_K_CMSM_readout.csv",
            "required_columns": "same_parent_branch_id;session_id;time_s;orbit_phase;gx;gz;readout_component;mask_flag;calibration_flag;axis_sign;units;source_path;valid_for_claim;claim_allowed",
            "minimum_rows": 1,
            "source_requirement": "official MICROSCOPE/CMSM readout or exact source-backed equivalent with units, masks, segment/session identity and sign convention",
            "reject_if": "absent;requirements_only;surrogate_only;missing_hash;missing_units;MISSING/PENDING/NONCLAIM markers;claim flags true before validation",
            "priority": "highest",
        },
        {
            "artifact_id": "ART1704_1_source_worldtube",
            "artifact": "P_WEP_R_source_Earth_worldtube.csv",
            "canonical_path": MICROSCOPE / "source_worldtube" / "P_WEP_R_source_Earth_worldtube.csv",
            "drop_path": DROP_LIVE / "P_WEP_R_source_Earth_worldtube.csv",
            "required_columns": "same_parent_branch_id;shell_id;radius_m;density_kg_m3;source_response;orbit_kernel;units;source_path;valid_for_claim;claim_allowed",
            "minimum_rows": 1,
            "source_requirement": "Earth/source worldtube or reproducible source-profile weighting in the observed local frame",
            "reject_if": "absent;bulk_description_only;missing_orbit_weighting;missing_units;MISSING/PENDING/NONCLAIM markers;claim flags true before validation",
            "priority": "highest",
        },
        {
            "artifact_id": "ART1704_2_material_tensor",
            "artifact": "P_WEP_TiPt_material_response_tensor.csv",
            "canonical_path": SOURCE_DIR / "P_WEP_TiPt_material_response_tensor.csv",
            "drop_path": DROP_LIVE / "P_WEP_TiPt_material_response_tensor.csv",
            "required_columns": "same_parent_branch_id;material;component;sensitivity_value;uncertainty;basis;sign_convention;units;source_path;valid_for_claim;claim_allowed",
            "minimum_rows": 2,
            "source_requirement": "TA6V and PtRh10 material response tensor in the same parent source-weight basis",
            "reject_if": "absent;alloy_label_only;missing_basis;missing_uncertainty;MISSING/PENDING/NONCLAIM markers;claim flags true before validation",
            "priority": "highest",
        },
        {
            "artifact_id": "ART1704_3_product_convention",
            "artifact": "P_WEP_eta_product_convention.csv",
            "canonical_path": MICROSCOPE / "product_convention" / "P_WEP_eta_product_convention.csv",
            "drop_path": DROP_LIVE / "P_WEP_eta_product_convention.csv",
            "required_columns": "same_parent_branch_id;eta_formula;sign_convention;tau_eff_definition;readout_kernel_units;source_kernel_units;orbit_average_rule;branch_lock;source_path;row_status;valid_prediction_row;valid_for_claim;claim_allowed",
            "minimum_rows": 1,
            "source_requirement": "reported eta convention, sign, absolute-value rule, orbit-average rule, units and branch basis",
            "reject_if": "partial_pending;requirements_only;missing_sign;missing_orbit_average;MISSING/PENDING/NONCLAIM markers;claim flags true before validation",
            "priority": "high",
        },
        {
            "artifact_id": "ART1704_4_branch_lock",
            "artifact": "P_WEP_same_parent_branch_lock.csv",
            "canonical_path": MICROSCOPE / "branch_classifier" / "P_WEP_same_parent_branch_lock.csv",
            "drop_path": DROP_LIVE / "P_WEP_same_parent_branch_lock.csv",
            "required_columns": "same_parent_branch_id;forbidden_mixing_rule;source_path;row_status;valid_prediction_row;valid_for_claim;claim_allowed",
            "minimum_rows": 1,
            "source_requirement": "same-parent branch guard tying C_parent, source, material, readout, product convention and bound comparator to one branch",
            "reject_if": "guard_only;branch_mismatch;surrogate_or_mixed_basis;MISSING/PENDING/NONCLAIM markers;claim flags true before validation",
            "priority": "high",
        },
        {
            "artifact_id": "ART1704_5_c_parent",
            "artifact": "P_WEP_C_parent_or_zero_certificate.csv",
            "canonical_path": SOURCE_DIR / "P_WEP_C_parent_or_zero_certificate.csv",
            "drop_path": DROP_LIVE / "P_WEP_C_parent_or_zero_certificate.csv",
            "required_columns": "same_parent_branch_id;route;coefficient_or_theorem_id;value;uncertainty;units;source_path;theorem_status;valid_for_claim;claim_allowed",
            "minimum_rows": 1,
            "source_requirement": "finite same-branch parent coefficient or parent-signed zero certificate",
            "reject_if": "absent;closure_only;unsigned_theorem;missing_units;MISSING/PENDING/NONCLAIM markers;claim flags true before validation",
            "priority": "highest",
        },
        {
            "artifact_id": "ART1704_6_tau_min",
            "artifact": "P_WEP_tau_min_lower_bound.csv",
            "canonical_path": SOURCE_DIR / "P_WEP_tau_min_lower_bound.csv",
            "drop_path": DROP_LIVE / "P_WEP_tau_min_lower_bound.csv",
            "required_columns": "same_parent_branch_id;tau_min;confidence;sign_or_abs_convention;derivation_or_source_path;assumptions;units;valid_for_claim;claim_allowed",
            "minimum_rows": 1,
            "source_requirement": "strictly positive abs(tau_WEP)>=tau_min>0 from official data or parent nondegeneracy theorem",
            "reject_if": "absent;tau_min<=0;tau_eff=1_shortcut;missing_derivation;MISSING/PENDING/NONCLAIM markers;claim flags true before validation",
            "priority": "highest",
        },
        {
            "artifact_id": "ART1704_7_manifest",
            "artifact": "P_WEP_tau_parser_manifest.json",
            "canonical_path": SOURCE_DIR / "P_WEP_tau_parser_manifest.json",
            "drop_path": DROP_LIVE / "P_WEP_tau_parser_manifest.json",
            "required_columns": "json:branch_id;manifest_status;artifact_hashes;schema_versions;units;sign_conventions;source_paths;license;citation;valid_for_claim;claim_allowed",
            "minimum_rows": 1,
            "source_requirement": "manifest with source paths, hashes, schemas, units, sign conventions, license/citation and no-shortcut assertions",
            "reject_if": "absent;template_only;missing_hash;missing_source;MISSING/PENDING/NONCLAIM markers;claim flags true before validation",
            "priority": "highest",
        },
    ]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def falsey(value: Any) -> bool:
    return str(value).strip().lower() in {"false", "0", "no", "n", ""}


def cell_has_block_marker(value: Any) -> bool:
    text = str(value).upper()
    return any(marker in text for marker in ("MISSING", "PENDING", "NONCLAIM", "TEMPLATE_ONLY", "REQUIREMENTS_ONLY", "SURROGATE"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def split_columns(value: str) -> list[str]:
    if value.startswith("json:"):
        return value.removeprefix("json:").split(";")
    return value.split(";")


def write_drop_templates(contracts: list[dict[str, Any]]) -> None:
    DROP_LIVE.mkdir(parents=True, exist_ok=True)
    DROP_TEMPLATES.mkdir(parents=True, exist_ok=True)
    for contract in contracts:
        artifact = str(contract["artifact"])
        columns = split_columns(str(contract["required_columns"]))
        if artifact.endswith(".csv"):
            template = DROP_TEMPLATES / artifact.replace(".csv", "_TEMPLATE.csv")
            write_csv(
                template,
                [
                    {
                        column: "FILL_ME_NO_CLAIM"
                        for column in columns
                    }
                ],
            )
        else:
            template_payload = {
                "branch_id": BRANCH_ID,
                "manifest_status": "template_only_not_live",
                "artifact": artifact,
                "artifact_hashes": {},
                "schema_versions": {},
                "units": {},
                "sign_conventions": {},
                "source_paths": {},
                "license": "FILL_ME_NO_CLAIM",
                "citation": "FILL_ME_NO_CLAIM",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
            write_text(DROP_MANIFEST_TEMPLATE, json.dumps(template_payload, indent=2))
    readme_lines = [
        "# MICROSCOPE WEP Drop Folder - 1704",
        "",
        "Private non-claim intake shell. Drop live source-backed files into:",
        f"`{DROP_LIVE}`",
        "",
        "Rules:",
        "- Do not rename the live files; use the exact artifact names.",
        "- Do not put templates in the live folder as evidence.",
        "- Every source-backed file needs units, sign convention, source path, and branch id.",
        "- The parser refuses `MISSING`, `PENDING`, `NONCLAIM`, `template_only`, surrogate-only, tau=1 shortcut, or bound-as-prediction rows.",
        "- Claim flags stay false until a later validator promotes a complete, source-backed set.",
        "",
        "Expected artifacts:",
    ]
    for contract in contracts:
        readme_lines.append(f"- `{contract['artifact']}`: {contract['source_requirement']}")
    write_text(DROP_README, "\n".join(readme_lines) + "\n")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (source_key, path) in enumerate(SOURCE_FILES.items()):
        text = read_text(path) if path.exists() else ""
        needles = NEEDLES[source_key]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC1704_{index}_{source_key}",
                "source_key": source_key,
                "source_path": str(path),
                "exists": path.exists(),
                "needles_present": all(needle in text for needle in needles),
                "required_needles": ";".join(needles),
                "use_in_1704": "MICROSCOPE drop-folder parser dry-run and manual data request refresh",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def drop_contract_rows(contracts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for contract in contracts:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "artifact_id": contract["artifact_id"],
                "artifact": contract["artifact"],
                "canonical_path": str(contract["canonical_path"]),
                "drop_path": str(contract["drop_path"]),
                "template_path": str(DROP_TEMPLATES / str(contract["artifact"]).replace(".csv", "_TEMPLATE.csv")) if str(contract["artifact"]).endswith(".csv") else str(DROP_MANIFEST_TEMPLATE),
                "required_columns": contract["required_columns"],
                "minimum_rows": contract["minimum_rows"],
                "source_requirement": contract["source_requirement"],
                "reject_if": contract["reject_if"],
                "priority": contract["priority"],
                "parser_ready": False,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def inspect_csv_artifact(path: Path, required_columns: list[str], minimum_rows: int) -> dict[str, Any]:
    try:
        rows = read_csv(path)
    except Exception as exc:
        return {
            "parse_ok": False,
            "row_count": 0,
            "missing_columns": ";".join(required_columns),
            "block_marker_present": True,
            "claim_flags_true": False,
            "claim_flags_false_or_missing": True,
            "inspection_status": f"CSV_PARSE_ERROR:{type(exc).__name__}",
        }
    columns = set(rows[0].keys()) if rows else set()
    missing = [column for column in required_columns if column not in columns]
    block_marker = any(cell_has_block_marker(value) for row in rows for value in row.values())
    claim_flags_true = any(
        truthy(row.get(field, ""))
        for row in rows
        for field in ("score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed", "accepted_for_scoring")
        if field in row
    )
    claim_flags_false_or_missing = all(
        falsey(row.get(field, ""))
        for row in rows
        for field in ("valid_for_claim", "claim_allowed")
        if field in row
    )
    if missing:
        status = "MISSING_REQUIRED_COLUMNS"
    elif len(rows) < minimum_rows:
        status = "TOO_FEW_ROWS"
    elif block_marker:
        status = "BLOCK_MARKERS_PRESENT"
    elif claim_flags_true:
        status = "CLAIM_FLAGS_TRUE_BEFORE_PROMOTION"
    else:
        status = "SCHEMA_ONLY_OK_NOT_SCORE_READY"
    return {
        "parse_ok": True,
        "row_count": len(rows),
        "missing_columns": ";".join(missing),
        "block_marker_present": block_marker,
        "claim_flags_true": claim_flags_true,
        "claim_flags_false_or_missing": claim_flags_false_or_missing,
        "inspection_status": status,
    }


def inspect_json_artifact(path: Path, required_keys: list[str]) -> dict[str, Any]:
    try:
        payload = json.loads(read_text(path))
    except Exception as exc:
        return {
            "parse_ok": False,
            "row_count": 0,
            "missing_columns": ";".join(required_keys),
            "block_marker_present": True,
            "claim_flags_true": False,
            "claim_flags_false_or_missing": True,
            "inspection_status": f"JSON_PARSE_ERROR:{type(exc).__name__}",
        }
    missing = [key for key in required_keys if key not in payload]
    text = json.dumps(payload, sort_keys=True)
    block_marker = cell_has_block_marker(text)
    claim_flags_true = truthy(payload.get("valid_for_claim", "")) or truthy(payload.get("claim_allowed", ""))
    if missing:
        status = "MISSING_REQUIRED_KEYS"
    elif block_marker:
        status = "BLOCK_MARKERS_PRESENT"
    elif claim_flags_true:
        status = "CLAIM_FLAGS_TRUE_BEFORE_PROMOTION"
    else:
        status = "SCHEMA_ONLY_OK_NOT_SCORE_READY"
    return {
        "parse_ok": True,
        "row_count": 1,
        "missing_columns": ";".join(missing),
        "block_marker_present": block_marker,
        "claim_flags_true": claim_flags_true,
        "claim_flags_false_or_missing": not claim_flags_true,
        "inspection_status": status,
    }


def inventory_rows(contracts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for contract in contracts:
        artifact = str(contract["artifact"])
        canonical_path = Path(contract["canonical_path"])
        drop_path = Path(contract["drop_path"])
        selected_path = canonical_path if canonical_path.exists() else drop_path
        target_exists = selected_path.exists()
        selected_source = "canonical" if canonical_path.exists() else "drop" if drop_path.exists() else "absent"
        required_columns = split_columns(str(contract["required_columns"]))
        if target_exists:
            if artifact.endswith(".json"):
                inspection = inspect_json_artifact(selected_path, required_columns)
            else:
                inspection = inspect_csv_artifact(selected_path, required_columns, int(contract["minimum_rows"]))
            checksum = sha256(selected_path)
            byte_count = selected_path.stat().st_size
        else:
            inspection = {
                "parse_ok": False,
                "row_count": 0,
                "missing_columns": ";".join(required_columns),
                "block_marker_present": False,
                "claim_flags_true": False,
                "claim_flags_false_or_missing": True,
                "inspection_status": "TARGET_ABSENT",
            }
            checksum = "not_available"
            byte_count = 0
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "inventory_id": str(contract["artifact_id"]).replace("ART", "INV"),
                "artifact": artifact,
                "canonical_path": str(canonical_path),
                "drop_path": str(drop_path),
                "selected_source": selected_source,
                "selected_path": str(selected_path),
                "target_exists": target_exists,
                "byte_count": byte_count,
                "sha256": checksum,
                "parse_ok": inspection["parse_ok"],
                "row_count": inspection["row_count"],
                "missing_columns": inspection["missing_columns"],
                "block_marker_present": inspection["block_marker_present"],
                "claim_flags_true": inspection["claim_flags_true"],
                "claim_flags_false_or_missing": inspection["claim_flags_false_or_missing"],
                "inspection_status": inspection["inspection_status"],
                "accepted_for_parser": False,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def schema_precheck_rows(inventory: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in inventory:
        if not truthy(item["target_exists"]):
            precheck_status = "FAIL_ABSENT"
            refusal_reason = "live artifact is absent from canonical and drop-folder paths"
        elif not truthy(item["parse_ok"]):
            precheck_status = "FAIL_PARSE"
            refusal_reason = str(item["inspection_status"])
        elif str(item["missing_columns"]):
            precheck_status = "FAIL_SCHEMA"
            refusal_reason = f"missing columns/keys: {item['missing_columns']}"
        elif truthy(item["block_marker_present"]):
            precheck_status = "FAIL_BLOCK_MARKERS"
            refusal_reason = "file contains MISSING/PENDING/NONCLAIM/template/surrogate marker"
        elif truthy(item["claim_flags_true"]):
            precheck_status = "FAIL_PREMATURE_CLAIM_FLAGS"
            refusal_reason = "file sets claim/scoring flags true before branch validation"
        else:
            precheck_status = "PASS_SCHEMA_ONLY_NONCLAIM"
            refusal_reason = "schema parses, but score promotion is disabled in 1704"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "precheck_id": str(item["inventory_id"]).replace("INV", "SPC"),
                "artifact": item["artifact"],
                "selected_source": item["selected_source"],
                "precheck_status": precheck_status,
                "refusal_reason": refusal_reason,
                "accepted_for_parser": False,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def parser_result_rows(precheck: list[dict[str, Any]]) -> list[dict[str, Any]]:
    failures = [row for row in precheck if not str(row["precheck_status"]).startswith("PASS_SCHEMA_ONLY")]
    fail_summary = ";".join(f"{row['artifact']}={row['precheck_status']}" for row in failures)
    return [
        {
            "branch_id": BRANCH_ID,
            "parser_id": "PRS1704_0_dry_run",
            "parser_mode": "drop_folder_preflight_only",
            "input_count": len(precheck),
            "failure_count": len(failures),
            "parser_status": "REFUSED_MISSING_OR_NONCLAIM_ARTIFACTS",
            "failure_summary": fail_summary,
            "computed_quantity": "none",
            "computed_value": "not_evaluated",
            "units": "not_applicable",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "parser_id": "PRS1704_1_no_bound_inversion",
            "parser_mode": "guardrail",
            "input_count": len(precheck),
            "failure_count": len(failures),
            "parser_status": "BOUND_AS_PREDICTION_REFUSED",
            "failure_summary": "MICROSCOPE bound may be used only as comparator after forward product exists",
            "computed_quantity": "P_WEP_source_weight",
            "computed_value": "not_evaluated",
            "units": "dimensionless",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "parser_id": "PRS1704_2_no_tau_unity",
            "parser_mode": "guardrail",
            "input_count": len(precheck),
            "failure_count": len(failures),
            "parser_status": "TAU_UNITY_SHORTCUT_REFUSED",
            "failure_summary": "tau_WEP must come from readout/source/material projection or tau_min theorem",
            "computed_quantity": "tau_WEP",
            "computed_value": "not_evaluated",
            "units": "dimensionless",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def request_update_rows(contracts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for contract in contracts:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "request_id": str(contract["artifact_id"]).replace("ART", "REQ"),
                "requested_artifact": contract["artifact"],
                "why_needed": contract["source_requirement"],
                "required_format": contract["required_columns"],
                "preferred_drop_path": str(contract["drop_path"]),
                "canonical_path_after_validation": str(contract["canonical_path"]),
                "priority": contract["priority"],
                "request_status": "READY_TO_REQUEST_NOT_ACQUIRED",
                "recipient_or_route": "CNES/ONERA/CMSM team, mission archive, or parent-theory derivation for coefficient/theorem artifacts",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def computation_plan_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "step_id": "CPU1704_0_load",
            "step": "load live artifacts",
            "formula_or_action": "read K_CMSM, S_Earth, M_TiPt, C_parent/zero, product convention, tau_min and manifest",
            "requires": "all schema prechecks pass without block markers",
            "current_status": "NOT_RUN_INPUTS_MISSING",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "step_id": "CPU1704_1_direct_product",
            "step": "compute forward direct product",
            "formula_or_action": "P_WEP_source_weight = N_eta^-1 <K_CMSM, C_parent[S_Earth,M_TiPt]>",
            "requires": "source/readout/material vectors in one branch basis and no bound inversion",
            "current_status": "NOT_RUN_INPUTS_MISSING",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "step_id": "CPU1704_2_compare",
            "step": "compare to MICROSCOPE bound",
            "formula_or_action": "abs(P_WEP_source_weight) <= 2.8e-15 only after forward product is computed",
            "requires": "claim-grade comparator provenance and branch validation",
            "current_status": "NOT_RUN_PRODUCT_MISSING",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "step_id": "CPU1704_3_delta_w_optional",
            "step": "optional Delta_w conversion",
            "formula_or_action": "abs(Delta_w_TiPt) <= 2.8e-15/tau_min if tau_min>0 exists",
            "requires": "strictly positive tau_min row; tau=1 shortcut forbidden",
            "current_status": "NOT_RUN_TAU_MIN_MISSING",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1704_0_parser_shell",
            "decision": "DROP_FOLDER_PARSER_SHELL_READY",
            "reason": "templates, README, inventory and dry-run refusal now exist",
            "next_action": "acquire live artifacts or use parser shell as exact request checklist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1704_1_current_result",
            "decision": "PARSER_REFUSES_SCORE",
            "reason": "missing live readout/source/material/C_parent/tau_min/manifest and nonclaim product/branch rows",
            "next_action": "do not score WEP until parser has live source-backed inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1704_2_next",
            "decision": "NEXT_1705_PUBLIC_SOURCE_PROBE_OR_PARENT_ZERO_ROUTE_SWITCH",
            "reason": "with parser shell done, the next work is either external source acquisition or a theory-side demotion of split Delta_w",
            "next_action": "try a public archive/source probe, then fall back to Delta_w parent-zero/direct-product route if no files are available",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1704_0_primary",
            "next_target": "1705-Y5-R2FR-MICROSCOPE-public-source-probe-or-parent-zero-route-switch.md",
            "script": "scripts/Y5_R2FR_MICROSCOPE_public_source_probe_or_parent_zero_route_switch.py",
            "objective": "probe whether public MICROSCOPE/CMSM data files can be located and mapped into the 1704 drop contract; if not, switch to the theory-side Delta_w demotion/direct-product route",
            "selection_status": "selected",
            "success_condition": "source-backed filelist or explicit no-public-file blocker; no WEP/local-GR claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1704_1_theory",
            "next_target": "1705a-Y5-R2FR-Delta-w-parent-zero-final-route-or-direct-product-only.md",
            "script": "scripts/Y5_R2FR_Delta_w_parent_zero_final_route_or_direct_product_only.py",
            "objective": "make final parent-signature attempt for Delta_w=0; if not signed, demote the split Delta_w route and keep direct product only",
            "selection_status": "held_fallback",
            "success_condition": "parent-signed zero theorem or explicit demotion with no claim flags",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1704_2_r10",
            "next_target": "1705b-Y5-R2FR-R10-alpha-lambda-projection-fill-runner.md",
            "script": "scripts/Y5_R2FR_R10_alpha_lambda_projection_fill_runner.py",
            "objective": "return to R10 alpha(lambda) once WEP parser source acquisition is blocked or staged",
            "selection_status": "held_fallback",
            "success_condition": "R10 projection inputs or explicit blockers are source-backed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1704_0_parser_ready",
            "claim": "MICROSCOPE WEP parser can evaluate source-weight product",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "dry run refuses missing/nonclaim artifacts",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1704_1_wep_score",
            "claim": "MTS WEP source-weight score",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "forward P_WEP_source_weight is not computed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1704_2_delta_w_bound",
            "claim": "finite Delta_w_TiPt bound",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "tau_min is missing and tau=1 shortcut is forbidden",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1704_3_local_GR",
            "claim": "derived local GR/Newton through WEP source branch",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "local coupling/source-weight branch remains unresolved",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def write_request_doc(request_rows: list[dict[str, Any]]) -> None:
    lines = [
        "# MICROSCOPE WEP Data Request Update - 1704",
        "",
        "Private MTS consistency work only. This request pack does not claim data have been acquired or that MTS passes WEP/local GR.",
        "",
        "## Purpose",
        "",
        "We need source-backed MICROSCOPE/CMSM readout, source/worldtube, material-response and metadata files to compute a forward `P_WEP_source_weight` product. The bound is not used as a prediction.",
        "",
        "## Exact Requested Artifacts",
        "",
        "| artifact | why needed | required format | preferred drop path |",
        "| --- | --- | --- | --- |",
    ]
    for row in request_rows:
        lines.append(
            f"| `{row['requested_artifact']}` | {row['why_needed']} | `{row['required_format']}` | `{row['preferred_drop_path']}` |"
        )
    lines.extend(
        [
            "",
            "## Non-Claim Guardrail",
            "",
            "Until these artifacts exist, parse, hash, unit-check, sign-check and branch-check together, keep `valid_for_claim=false`, `claim_allowed=false`, and no WEP/local-GR/Newton claim.",
        ]
    )
    write_text(REQUEST_DOC, "\n".join(lines) + "\n")


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    for source, targets in {
        REQUEST_DOC: [
            QUARANTINE / "MICROSCOPE_WEP_data_request_update_1704.md",
            BRANCH_RESIDUALS / "R2FR_MICROSCOPE_WEP_data_request_update_1704.md",
            QUEUE / "JR1704_MICROSCOPE_WEP_data_request_update.md",
        ],
        DROP_README: [
            QUARANTINE / "README_DROP_FILES_1704.md",
            BRANCH_RESIDUALS / "R2FR_README_DROP_FILES_1704.md",
        ],
        DROP_MANIFEST_TEMPLATE: [
            QUARANTINE / "P_WEP_tau_parser_manifest_TEMPLATE.json",
            BRANCH_RESIDUALS / "R2FR_P_WEP_tau_parser_manifest_TEMPLATE_1704.json",
            QUEUE / "JR1704_P_WEP_tau_parser_manifest_TEMPLATE.json",
        ],
    }.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def csv_parses(paths: list[Path]) -> bool:
    try:
        for path in paths:
            read_csv(path)
    except Exception:
        return False
    return True


def no_claim_flags(paths: list[Path]) -> bool:
    fields = (
        "accepted_for_parser",
        "accepted_for_scoring",
        "parser_ready",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
    )
    for path in paths:
        for row in read_csv(path):
            for field in fields:
                if field in row and truthy(row[field]):
                    return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    markers = (
        "1704-Y5",
        "P8_Y5_PARENT_QLOC_1704",
        "P8_Y5_BRR545_1704",
        "Y5_R2FR_MICROSCOPE_parser_shell_dry_run_or_manual_data_request",
    )
    for path in FORMALIZATION.rglob("*"):
        if ".venv" in path.parts or "__pycache__" in path.parts:
            continue
        if any(marker in path.name for marker in markers):
            return False
    return True


def validation_rows() -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    contract = read_csv(DROP_CONTRACT)
    inventory = read_csv(DROP_INVENTORY)
    precheck = read_csv(SCHEMA_PRECHECK)
    parser = read_csv(PARSER_RESULT)
    request = read_csv(REQUEST_UPDATE)
    plan = read_csv(COMPUTATION_PLAN)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)
    gates = read_csv(CLAIM_GATE)
    copies = [target for targets in COPY_TARGETS.values() for target in targets]
    artifacts = {row["artifact"] for row in contract}
    required_artifacts = {contract["artifact"] for contract in artifact_contracts()}
    template_paths = [Path(row["template_path"]) for row in contract]
    checks = [
        ("VAL1704_0_sources_exist", all(truthy(row["exists"]) for row in sources), "all cited local source paths exist"),
        ("VAL1704_1_needles_present", all(truthy(row["needles_present"]) for row in sources), "all required source needles are present"),
        ("VAL1704_2_drop_contract_complete", required_artifacts.issubset(artifacts), "drop-folder contract lists every required artifact"),
        ("VAL1704_3_drop_dirs_exist", DROP.exists() and DROP_LIVE.exists() and DROP_TEMPLATES.exists(), "drop-folder live/template directories exist"),
        ("VAL1704_4_templates_exist", all(path.exists() for path in template_paths), "all drop-folder templates exist"),
        ("VAL1704_5_inventory_complete", len(inventory) == len(contract) and all("inspection_status" in row for row in inventory), "inventory inspects every artifact"),
        ("VAL1704_6_precheck_refuses", any(row["precheck_status"].startswith("FAIL") for row in precheck), "schema precheck refuses absent/nonclaim artifacts"),
        ("VAL1704_7_parser_refuses", any(row["parser_id"] == "PRS1704_0_dry_run" and row["parser_status"] == "REFUSED_MISSING_OR_NONCLAIM_ARTIFACTS" for row in parser), "parser dry-run refuses current inputs"),
        ("VAL1704_8_no_computation", all(row["current_status"].startswith("NOT_RUN") for row in plan), "computation plan is not run"),
        ("VAL1704_9_request_ready", REQUEST_DOC.exists() and len(request) == len(contract), "manual data request update exists and covers every artifact"),
        ("VAL1704_10_decision_next", any(row["decision"] == "NEXT_1705_PUBLIC_SOURCE_PROBE_OR_PARENT_ZERO_ROUTE_SWITCH" for row in decisions), "decision selects 1705 source probe or theory switch"),
        ("VAL1704_11_next_selected", any(row["route_id"] == "NEXT1704_0_primary" and row["selection_status"] == "selected" for row in next_rows), "next target selected"),
        ("VAL1704_12_claim_gates_blocked", gates and all(row["status"] == "BLOCKED_NO_CLAIM" and not truthy(row["claim_allowed"]) for row in gates), "all claim gates remain blocked"),
        ("VAL1704_13_csv_parse", csv_parses(GENERATED_CSVS), "all generated 1704 CSVs parse"),
        ("VAL1704_14_no_claim_flags", no_claim_flags(CLAIM_CHECKED_CSVS), "all generated score/prediction/claim flags remain false"),
        ("VAL1704_15_branch_copies", all(path.exists() for path in copies), "branch/quarantine/queue copies exist"),
        ("VAL1704_16_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1704_17_formalization_untouched", formalization_untouched(), "no 1704 outputs found under formalization-workbench outside vendor/env folders"),
    ]
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1704_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1704 MICROSCOPE parser shell dry-run/manual request validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "/") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def write_doc(
    sources: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    inventory: list[dict[str, Any]],
    precheck: list[dict[str, Any]],
    parser: list[dict[str, Any]],
    request: list[dict[str, Any]],
    plan: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    write_text(
        DOC,
        "\n\n".join(
            [
                "# 1704 - MICROSCOPE Parser Shell Dry Run Or Manual Data Request",
                "## Verdict\n"
                "- 1704 turns the WEP parser into a real drop-folder preflight shell.\n"
                f"- Live files should be dropped into `{DROP_LIVE}` using exact artifact names; templates live in `{DROP_TEMPLATES}`.\n"
                "- Current dry run refuses to score because required live readout, source-worldtube, material, `C_parent`/zero, `tau_min`, and manifest artifacts are absent, while existing product/branch files are still nonclaim guards.\n"
                "- The request update is now exact enough to hand to a human or archive search: it names every file, field set, and reason.\n"
                "- No WEP, local-GR/Newton, coupling, PPN, R10, clock, orbital or public claim is made.",
                "## Source Register",
                markdown_table(sources, ["source_id", "source_key", "source_path", "exists", "needles_present"]),
                "## Drop-Folder Contract",
                markdown_table(contract, ["artifact_id", "artifact", "drop_path", "required_columns", "priority"]),
                "## Drop-Folder Inventory",
                markdown_table(inventory, ["inventory_id", "artifact", "selected_source", "target_exists", "row_count", "inspection_status"]),
                "## Schema Precheck",
                markdown_table(precheck, ["precheck_id", "artifact", "precheck_status", "refusal_reason"]),
                "## Parser Dry Run Result",
                markdown_table(parser, ["parser_id", "parser_status", "failure_count", "computed_quantity", "computed_value"]),
                "## Manual Data Request Update",
                markdown_table(request, ["request_id", "requested_artifact", "priority", "request_status", "preferred_drop_path"]),
                "## If-Unlocked Computation Plan",
                markdown_table(plan, ["step_id", "step", "formula_or_action", "current_status"]),
                "## Decision",
                markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"]),
                "## Next Target",
                markdown_table(next_rows, ["route_id", "next_target", "objective", "selection_status"]),
                "## Claim Gates",
                markdown_table(gates, ["claim_id", "claim", "status", "reason"]),
                "## Validation",
                markdown_table(validation, ["check_id", "result", "detail"]),
                "## Working Interpretation\n"
                "The WEP/coupling path is now split cleanly: data route or theory route. The data route has a concrete door: if real MICROSCOPE/CMSM artifacts appear, the parser can inspect them without rewriting the theory. If they do not appear, the next honest move is to either probe public sources once or demote the separate `Delta_w` split and keep only the direct product branch.",
            ]
        )
        + "\n",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    contracts = artifact_contracts()
    write_drop_templates(contracts)

    sources = source_register_rows()
    contract_rows = drop_contract_rows(contracts)
    inventory = inventory_rows(contracts)
    precheck = schema_precheck_rows(inventory)
    parser = parser_result_rows(precheck)
    request = request_update_rows(contracts)
    plan = computation_plan_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    gates = claim_gate_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(DROP_CONTRACT, contract_rows)
    write_csv(DROP_INVENTORY, inventory)
    write_csv(SCHEMA_PRECHECK, precheck)
    write_csv(PARSER_RESULT, parser)
    write_csv(REQUEST_UPDATE, request)
    write_csv(COMPUTATION_PLAN, plan)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    write_csv(CLAIM_GATE, gates)
    write_request_doc(request)
    copy_outputs()
    remove_pycache()
    validation = validation_rows()
    write_csv(VALIDATION, validation)
    write_doc(sources, contract_rows, inventory, precheck, parser, request, plan, decisions, next_rows, gates, validation)

    failed = [row for row in validation if row["result"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("1704 validation PASS")


if __name__ == "__main__":
    main()
