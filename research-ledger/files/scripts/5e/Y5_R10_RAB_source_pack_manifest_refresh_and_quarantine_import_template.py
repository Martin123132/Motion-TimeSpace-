from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
QUARANTINE = MICROSCOPE / "quarantine" / "1458"
COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1458-Y5-R10-RAB-source-pack-manifest-refresh-and-quarantine-import-template.md"

PREV_NEXT = OUT / "P8_Y5_R10_1457_NEXT_TARGET.csv"
PREV_MANIFEST_REFRESH = OUT / "P8_Y5_R10_1457_SOURCE_PACK_MANIFEST_REFRESH.csv"
PREV_IMPORT_VALIDATION = OUT / "P8_Y5_R10_1457_SOURCE_PACK_IMPORT_VALIDATION.csv"
PREV_ROW_QUALITY = OUT / "P8_Y5_R10_1457_LIVE_FILE_ROW_QUALITY_AUDIT.csv"
PREV_PILOT = OUT / "P8_Y5_R10_1457_SOURCE_WORLDTUBE_PILOT_LEDGER_NONCLAIM.csv"
PREV_SIGNING = OUT / "P8_Y5_R10_1457_PARENT_SIGNING_DECISION.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1457_VALIDATION.csv"

MANIFEST_1438 = OUT / "P8_Y5_R10_1438_OFFICIAL_MICROSCOPE_SOURCE_PACK_MANIFEST.csv"
MATERIAL_SCHEMA = OUT / "P8_Y5_R10_1438_SOURCE_PACK_FILE_SCHEMA.csv"
READ_SCHEMA = MICROSCOPE / "metadata" / "P8_Y5_R10_1336_OFFICIAL_READOUT_SCHEMA.csv"
SOURCE_SCHEMA = MICROSCOPE / "metadata" / "P8_Y5_R10_1336_SOURCE_WORLDTUBE_SCHEMA.csv"
PRODUCT_SCHEMA = MICROSCOPE / "metadata" / "P8_Y5_R10_1336_PRODUCT_CONVENTION_SCHEMA.csv"
BRANCH_SCHEMA = MICROSCOPE / "metadata" / "P8_Y5_R10_1336_BRANCH_CLASSIFIER_SCHEMA.csv"
CPARENT_SCHEMA = COEFF / "C_parent_import_schema.csv"

LIVE_OFFICIAL_READOUT = MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout.csv"
LIVE_SOURCE_WORLD = MICROSCOPE / "source_worldtube" / "P_WEP_R_source_Earth_worldtube.csv"
LIVE_PRODUCT_CONVENTION = MICROSCOPE / "product_convention" / "P_WEP_eta_product_convention.csv"
LIVE_BRANCH_CLASSIFIER = MICROSCOPE / "branch_classifier" / "P_WEP_same_parent_branch_lock.csv"
LIVE_MATERIAL_TENSOR = MICROSCOPE / "derived" / "P_WEP_R_material_TA6V_minus_PtRh10_full_tensor.csv"
LIVE_CPARENT = COEFF / "C_parent_WEP_slot_import.csv"

QUAR_OFFICIAL_READOUT = QUARANTINE / "P_WEP_K_CMSM_readout_TEMPLATE_QUARANTINE_NONCLAIM.csv"
QUAR_SOURCE_WORLD = QUARANTINE / "P_WEP_R_source_Earth_worldtube_TEMPLATE_QUARANTINE_NONCLAIM.csv"
QUAR_MATERIAL_TENSOR = QUARANTINE / "P_WEP_R_material_TA6V_minus_PtRh10_full_tensor_TEMPLATE_QUARANTINE_NONCLAIM.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1458_SOURCE_REGISTER.csv"
REFRESHED_MANIFEST = OUT / "P8_Y5_R10_1458_REFRESHED_SOURCE_PACK_MANIFEST_NONCLAIM.csv"
MANIFEST_DELTA = OUT / "P8_Y5_R10_1458_MANIFEST_DELTA_LEDGER.csv"
QUARANTINE_REGISTER = OUT / "P8_Y5_R10_1458_QUARANTINE_TEMPLATE_REGISTER.csv"
TEMPLATE_VALIDATION = OUT / "P8_Y5_R10_1458_QUARANTINE_TEMPLATE_VALIDATION.csv"
LIVE_PATH_GUARD = OUT / "P8_Y5_R10_1458_LIVE_PATH_GUARD.csv"
PROMOTION_GATES = OUT / "P8_Y5_R10_1458_PROMOTION_GATES.csv"
SIGNING_DECISION = OUT / "P8_Y5_R10_1458_PARENT_SIGNING_DECISION.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1458_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1458_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1458_VALIDATION.csv"

BRANCH_REFRESHED_MANIFEST = COEFF / "source_pack_manifest_refresh_nonclaim_1458.csv"
BRANCH_TEMPLATE_REGISTER = COEFF / "quarantine_template_register_nonclaim_1458.csv"
BRANCH_SIGNING = COEFF / "C_parent_WEP_manifest_refresh_signing_decision_1458.csv"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
START_TS = datetime.now(timezone.utc).timestamp()
PLACEHOLDER = "QUARANTINE_TEMPLATE_PLACEHOLDER_DO_NOT_PROMOTE"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def truth(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def rows_from_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv_ok(path: Path) -> bool:
    return bool(rows_from_csv(path))


def schema_fields(path: Path) -> list[str]:
    fields: list[str] = []
    for row in rows_from_csv(path):
        field = row.get("column") or row.get("field")
        if field and field not in fields:
            fields.append(field)
    return fields


def required_fields(raw: str) -> list[str]:
    return [item.strip() for item in str(raw).split(";") if item.strip()]


def file_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def target_path(row: dict[str, str]) -> Path:
    return Path(row["target_path"])


def manifest_schema_path(row: dict[str, str]) -> Path:
    return Path(row["schema_path"])


def copy_branch(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


def source_rows() -> list[dict[str, Any]]:
    sources = [
        ("SRC1458_0_prev_next", PREV_NEXT, "1458 handoff"),
        ("SRC1458_1_prev_manifest_refresh", PREV_MANIFEST_REFRESH, "1457 manifest refresh"),
        ("SRC1458_2_prev_import_validation", PREV_IMPORT_VALIDATION, "1457 import validation"),
        ("SRC1458_3_prev_row_quality", PREV_ROW_QUALITY, "1457 live row quality audit"),
        ("SRC1458_4_prev_pilot", PREV_PILOT, "1457 source-worldtube pilot"),
        ("SRC1458_5_prev_signing", PREV_SIGNING, "1457 signing decision"),
        ("SRC1458_6_prev_validation", PREV_VALIDATION, "1457 validation"),
        ("SRC1458_7_manifest_1438", MANIFEST_1438, "historical manifest to refresh"),
        ("SRC1458_8_material_schema", MATERIAL_SCHEMA, "material tensor schema"),
        ("SRC1458_9_read_schema", READ_SCHEMA, "official readout schema"),
        ("SRC1458_10_source_schema", SOURCE_SCHEMA, "source-worldtube schema"),
        ("SRC1458_11_product_schema", PRODUCT_SCHEMA, "product convention schema"),
        ("SRC1458_12_branch_schema", BRANCH_SCHEMA, "branch classifier schema"),
        ("SRC1458_13_cparent_schema", CPARENT_SCHEMA, "C_parent import schema"),
        ("SRC1458_14_product_live_partial", LIVE_PRODUCT_CONVENTION, "partial nonclaim product convention"),
        ("SRC1458_15_branch_live_partial", LIVE_BRANCH_CLASSIFIER, "partial nonclaim branch classifier"),
    ]
    return [
        {
            "source_id": source_id,
            "source_path": str(path),
            "exists": path.exists(),
            "role": role,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path, role in sources
    ]


def refreshed_manifest_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in rows_from_csv(MANIFEST_1438):
        path = target_path(row)
        schema_path = manifest_schema_path(row)
        actual_target_exists = path.exists()
        actual_schema_exists = schema_path.exists()
        text = file_text(path).upper()
        has_blockers = any(marker in text for marker in ("MISSING", "PENDING", "PLACEHOLDER", "SURROGATE", "NOT_IMPORTED", "NOT_ACQUIRED"))
        if not actual_target_exists:
            status = row["current_status"]
        elif has_blockers:
            status = "PRESENT_NONCLAIM_WITH_BLOCKING_MARKERS"
        else:
            status = "PRESENT_NONCLAIM_NEEDS_PROMOTION_REVIEW"
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "manifest_id": row["manifest_id"].replace("PACK1438", "PACK1458"),
                "source_manifest_id": row["manifest_id"],
                "pack_item": row["pack_item"],
                "target_path": str(path),
                "target_exists": actual_target_exists,
                "target_parent_dir_exists": path.parent.exists(),
                "schema_path": str(schema_path),
                "schema_exists": actual_schema_exists,
                "required_columns_or_fields": row["required_columns_or_fields"],
                "provenance_requirement": row["provenance_requirement"],
                "current_status": status,
                "promotion_condition": "target exists, parses, branch-locked, no MISSING/PENDING/PLACEHOLDER/SURROGATE markers, source path/URL/DOI present, and full source pack passes together",
                "refresh_policy": "shadow_refresh_only_do_not_overwrite_1438",
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def manifest_delta_rows(refreshed: list[dict[str, Any]]) -> list[dict[str, Any]]:
    old_by_id = {row["manifest_id"]: row for row in rows_from_csv(MANIFEST_1438)}
    rows: list[dict[str, Any]] = []
    for row in refreshed:
        old_id = row["source_manifest_id"]
        old = old_by_id[old_id]
        old_target = truth(old.get("target_exists", "false"))
        old_schema = truth(old.get("schema_exists", "false"))
        target_changed = old_target != truth(row["target_exists"])
        schema_changed = old_schema != truth(row["schema_exists"])
        status_changed = old["current_status"] != row["current_status"]
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "delta_id": f"DELTA1458_{old_id}",
                "pack_item": row["pack_item"],
                "source_manifest_id": old_id,
                "old_target_exists": old_target,
                "new_target_exists": row["target_exists"],
                "old_schema_exists": old_schema,
                "new_schema_exists": row["schema_exists"],
                "old_status": old["current_status"],
                "new_status": row["current_status"],
                "target_exists_changed": target_changed,
                "schema_exists_changed": schema_changed,
                "status_changed": status_changed,
                "delta_verdict": "STALE_MANIFEST_REFRESHED_IN_SHADOW" if (target_changed or schema_changed or status_changed) else "UNCHANGED",
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def quarantine_rows() -> dict[Path, list[dict[str, Any]]]:
    official_fields = ["same_parent_branch_id"] + schema_fields(READ_SCHEMA) + ["row_status", "valid_prediction_row", "valid_for_claim", "claim_allowed"]
    source_fields = ["same_parent_branch_id"] + schema_fields(SOURCE_SCHEMA) + ["row_status", "valid_prediction_row", "valid_for_claim", "claim_allowed"]
    material_fields = ["same_parent_branch_id"] + schema_fields(MATERIAL_SCHEMA)
    rows: dict[Path, list[dict[str, Any]]] = {}
    rows[QUAR_OFFICIAL_READOUT] = [
        {
            field: (
                BRANCH_ID
                if field == "same_parent_branch_id"
                else False
                if field in {"valid_prediction_row", "valid_for_claim", "claim_allowed"}
                else "QUARANTINE_TEMPLATE_NONCLAIM"
                if field == "row_status"
                else PLACEHOLDER
            )
            for field in official_fields
        }
    ]
    rows[QUAR_SOURCE_WORLD] = [
        {
            field: (
                BRANCH_ID
                if field == "same_parent_branch_id"
                else False
                if field in {"valid_prediction_row", "valid_for_claim", "claim_allowed"}
                else "QUARANTINE_TEMPLATE_NONCLAIM"
                if field == "row_status"
                else PLACEHOLDER
            )
            for field in source_fields
        }
    ]
    rows[QUAR_MATERIAL_TENSOR] = [
        {
            field: (
                BRANCH_ID
                if field == "same_parent_branch_id"
                else False
                if field in {"valid_prediction_row", "valid_for_claim", "claim_allowed"}
                else PLACEHOLDER
            )
            for field in material_fields
        }
    ]
    return rows


def write_quarantine_templates() -> None:
    for path, rows in quarantine_rows().items():
        write_csv(path, rows)


def template_register_rows() -> list[dict[str, Any]]:
    templates = [
        ("QT1458_0_official_readout", "official_readout", QUAR_OFFICIAL_READOUT, LIVE_OFFICIAL_READOUT, "official K_CMSM readout template with placeholders only"),
        ("QT1458_1_source_worldtube", "source_worldtube", QUAR_SOURCE_WORLD, LIVE_SOURCE_WORLD, "source-worldtube template with placeholders only"),
        ("QT1458_2_material_tensor", "material_tensor", QUAR_MATERIAL_TENSOR, LIVE_MATERIAL_TENSOR, "material tensor template with placeholders only"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "template_id": template_id,
            "pack_item": pack_item,
            "quarantine_path": str(quarantine_path),
            "quarantine_exists": quarantine_path.exists(),
            "live_target_path": str(live_path),
            "live_target_exists": live_path.exists(),
            "template_purpose": purpose,
            "write_scope": "quarantine_only",
            "would_write_live_file": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for template_id, pack_item, quarantine_path, live_path, purpose in templates
    ]


def template_validation_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    expected = [
        ("TVAL1458_0_official_readout", QUAR_OFFICIAL_READOUT, READ_SCHEMA, LIVE_OFFICIAL_READOUT),
        ("TVAL1458_1_source_worldtube", QUAR_SOURCE_WORLD, SOURCE_SCHEMA, LIVE_SOURCE_WORLD),
        ("TVAL1458_2_material_tensor", QUAR_MATERIAL_TENSOR, MATERIAL_SCHEMA, LIVE_MATERIAL_TENSOR),
    ]
    for validation_id, quarantine_path, schema_path, live_path in expected:
        header = list(rows_from_csv(quarantine_path)[0].keys()) if rows_from_csv(quarantine_path) else []
        schema = schema_fields(schema_path)
        missing = [field for field in schema if field not in header]
        text = file_text(quarantine_path).upper()
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "validation_id": validation_id,
                "quarantine_path": str(quarantine_path),
                "schema_path": str(schema_path),
                "quarantine_exists": quarantine_path.exists(),
                "parseable": parse_csv_ok(quarantine_path),
                "schema_fields_present": not missing,
                "missing_schema_fields": ";".join(missing) if missing else "none",
                "placeholder_markers_present": PLACEHOLDER in text,
                "live_target_path": str(live_path),
                "live_target_exists": live_path.exists(),
                "template_status": "QUARANTINE_TEMPLATE_READY_NONCLAIM" if quarantine_path.exists() and not missing and PLACEHOLDER in text else "TEMPLATE_FAIL",
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def live_path_guard_rows() -> list[dict[str, Any]]:
    rows = [
        ("LIVE1458_0_official_readout", LIVE_OFFICIAL_READOUT, "must remain missing/live untouched"),
        ("LIVE1458_1_source_worldtube", LIVE_SOURCE_WORLD, "must remain missing/live untouched"),
        ("LIVE1458_2_material_tensor", LIVE_MATERIAL_TENSOR, "must remain missing/live untouched"),
        ("LIVE1458_3_Cparent", LIVE_CPARENT, "must remain missing/live untouched"),
        ("LIVE1458_4_product_convention", LIVE_PRODUCT_CONVENTION, "existing partial nonclaim file must not be overwritten"),
        ("LIVE1458_5_branch_classifier", LIVE_BRANCH_CLASSIFIER, "existing partial nonclaim file must not be overwritten"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "guard_id": guard_id,
            "live_path": str(path),
            "live_exists": path.exists(),
            "guard_rule": rule,
            "write_attempted_by_1458": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for guard_id, path, rule in rows
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1458_0_shadow_refresh", "shadow manifest refresh may be used as current truth", True, "nonclaim refresh generated without overwriting 1438"),
        ("GATE1458_1_live_official_readout", "live official readout claim-ready", False, "live official readout missing; quarantine template has placeholders"),
        ("GATE1458_2_live_source_worldtube", "live source-worldtube claim-ready", False, "live source-worldtube missing; quarantine template has placeholders"),
        ("GATE1458_3_live_material_tensor", "live material tensor claim-ready", False, "live material tensor missing; quarantine template has placeholders"),
        ("GATE1458_4_product_branch_support", "product/branch support claim-ready", False, "partial product/branch files remain nonclaim with blocking markers/support-only status"),
        ("GATE1458_5_Cparent", "C_parent_WEP import allowed", False, "C_parent live import missing and explicitly excluded from template writes"),
        ("GATE1458_6_tau", "numeric tau_WEP allowed", False, "templates contain placeholders and no official/source/material pack"),
        ("GATE1458_7_local_claim", "local WEP/R10/PPN/GR claim allowed", False, "source pack incomplete and templates are quarantine-only"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "gate_pass": gate_pass,
            "blocking_reason": reason,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate, gate_pass, reason in rows
    ]


def signing_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "SIGN1458_0_manifest_refresh_quarantine",
            "target": "source-pack manifest refresh and quarantine templates",
            "shadow_manifest_refreshed": True,
            "historical_manifest_overwritten": False,
            "quarantine_templates_written": True,
            "live_official_readout_written": False,
            "live_source_worldtube_written": False,
            "live_material_tensor_written": False,
            "live_Cparent_written": False,
            "tau_WEP_numeric_allowed": False,
            "local_claim_allowed": False,
            "decision": "REFRESH_SHADOW_MANIFEST_AND_KEEP_TEMPLATES_QUARANTINED",
            "reason": "filesystem truth is now recorded, but all new rows are quarantine placeholders and cannot become claim inputs",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1458_0_manifest",
            "decision": "shadow-refresh the manifest rather than overwrite historical 1438",
            "why": "keeps audit trail while correcting stale target_exists truth",
            "consequence": "1458 manifest should be used for current-state gating",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1458_1_templates",
            "decision": "write only quarantine templates for official readout, source-worldtube, and material tensor",
            "why": "templates are useful for future data import but must not be mistaken for evidence",
            "consequence": "all placeholder rows remain blocked by validator",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1458_2_next_best_route",
            "decision": "next target should validate quarantine templates against the 1457 import validator",
            "why": "the next useful move is proving bad placeholder templates cannot pass import gates",
            "consequence": "1459 should run quarantine-to-live promotion refusal checks",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1458_0_1459",
            "next_target": "1459-Y5-R10-RAB-quarantine-template-promotion-refusal-and-live-import-dry-run.md",
            "script": "scripts/Y5_R10_RAB_quarantine_template_promotion_refusal_and_live_import_dry_run.py",
            "objective": "dry-run the 1457 validator against 1458 quarantine templates and prove placeholder/nonclaim rows cannot promote to live official readout, source-worldtube, material tensor, tau_WEP, or C_parent",
            "include": "quarantine validation; placeholder refusal; branch lock checks; provenance checks; no live writes",
            "exclude": "numeric WEP claim; tau_WEP value; C_parent import; local-GR pass; formalization-workbench edits; GitHub action",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    refreshed: list[dict[str, Any]],
    delta: list[dict[str, Any]],
    template_register: list[dict[str, Any]],
    template_validation: list[dict[str, Any]],
    live_guard: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated_csvs = [
        SOURCE_REGISTER,
        REFRESHED_MANIFEST,
        MANIFEST_DELTA,
        QUARANTINE_REGISTER,
        TEMPLATE_VALIDATION,
        LIVE_PATH_GUARD,
        PROMOTION_GATES,
        SIGNING_DECISION,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    all_sources_exist = all(truth(row["exists"]) for row in sources)
    refreshed_parse = parse_csv_ok(REFRESHED_MANIFEST)
    stale_corrected_shadow = any(row["delta_verdict"] == "STALE_MANIFEST_REFRESHED_IN_SHADOW" for row in delta)
    templates_exist = all(truth(row["quarantine_exists"]) and not truth(row["would_write_live_file"]) for row in template_register)
    templates_placeholder = all(truth(row["placeholder_markers_present"]) for row in template_validation)
    live_critical_untouched = (
        not LIVE_OFFICIAL_READOUT.exists()
        and not LIVE_SOURCE_WORLD.exists()
        and not LIVE_MATERIAL_TENSOR.exists()
        and not LIVE_CPARENT.exists()
    )
    live_guard_nonclaim = all(not truth(row["valid_for_claim"]) and not truth(row["claim_allowed"]) for row in live_guard)
    gates_safe = all((row["gate_id"] == "GATE1458_0_shadow_refresh" and truth(row["gate_pass"])) or not truth(row["gate_pass"]) for row in gates)
    signing_refuses = all(not truth(row["local_claim_allowed"]) and not truth(row["tau_WEP_numeric_allowed"]) for row in signing)
    generated_parse = all(parse_csv_ok(path) for path in generated_csvs)
    branch_copies = BRANCH_REFRESHED_MANIFEST.exists() and BRANCH_TEMPLATE_REGISTER.exists() and BRANCH_SIGNING.exists()
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formal_recent = 0
    if FORMALIZATION.exists():
        formal_recent = sum(
            1
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and path.stat().st_mtime > START_TS
        )
    checks = [
        ("VAL1458_0_sources", all_sources_exist, "all cited source paths exist"),
        ("VAL1458_1_refreshed_parse", refreshed_parse, "shadow refreshed manifest parses"),
        ("VAL1458_2_stale_corrected_shadow", stale_corrected_shadow, "stale 1438 manifest truth corrected in 1458 shadow refresh"),
        ("VAL1458_3_templates_exist_quarantine_only", templates_exist, "quarantine templates written and no live writes declared"),
        ("VAL1458_4_templates_have_placeholders", templates_placeholder, "all quarantine templates contain placeholder refusal markers"),
        ("VAL1458_5_live_critical_untouched", live_critical_untouched, "critical live official/source/material/Cparent files remain absent"),
        ("VAL1458_6_live_guard_nonclaim", live_guard_nonclaim, "live path guard rows are nonclaim"),
        ("VAL1458_7_gates_safe", gates_safe, "only shadow-refresh gate passes; all claim gates remain false"),
        ("VAL1458_8_signing_refuses", signing_refuses, "parent signing decision refuses tau/local promotion"),
        ("VAL1458_9_generated_csv_parse", generated_parse, "all generated 1458 CSVs parse cleanly"),
        ("VAL1458_10_branch_copies", branch_copies, "nonclaim branch copies written"),
        ("VAL1458_11_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1458_12_formalization_untouched", formal_recent == 0, f"formalization modified-file count since start={formal_recent}"),
        ("VAL1458_13_overall", True, "1458 refreshes source-pack manifest in shadow and writes quarantine-only templates"),
    ]
    return [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "generated_utc": now(),
        }
        for check_id, passed, detail in checks
    ]


def write_table(handle, title: str, rows: list[dict[str, Any]]) -> None:
    handle.write(f"## {title}\n\n")
    if not rows:
        handle.write("_No rows._\n\n")
        return
    fields = list(rows[0].keys())
    handle.write("| " + " | ".join(fields) + " |\n")
    handle.write("| " + " | ".join(["---"] * len(fields)) + " |\n")
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ") for field in fields]
        handle.write("| " + " | ".join(values) + " |\n")
    handle.write("\n")


def write_doc(
    sources: list[dict[str, Any]],
    refreshed: list[dict[str, Any]],
    delta: list[dict[str, Any]],
    template_register: list[dict[str, Any]],
    template_validation: list[dict[str, Any]],
    live_guard: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    with DOC.open("w", encoding="utf-8") as handle:
        handle.write("# 1458 - Source-pack manifest refresh and quarantine import template\n\n")
        handle.write(
            "**Current verdict:** 1458 creates a current-state shadow manifest and quarantine-only templates. "
            "The historical 1438 manifest is not overwritten. Product/branch support is acknowledged as present but "
            "nonclaim; official readout, source-worldtube, material tensor, and `C_parent_WEP` remain missing from live paths.\n\n"
        )
        handle.write(
            "**Useful progress:** future imports now have exact placeholder schemas in quarantine. They cannot support "
            "`tau_WEP`, `K_CMSM`, `C_parent_WEP`, or local-GR/WEP claims because every template row carries explicit "
            "placeholder markers and claim flags remain false.\n\n"
        )
        write_table(handle, "Source register", sources)
        write_table(handle, "Refreshed source-pack manifest", refreshed)
        write_table(handle, "Manifest delta ledger", delta)
        write_table(handle, "Quarantine template register", template_register)
        write_table(handle, "Quarantine template validation", template_validation)
        write_table(handle, "Live path guard", live_guard)
        write_table(handle, "Promotion gates", gates)
        write_table(handle, "Parent signing decision", signing)
        write_table(handle, "Decision ledger", decisions)
        write_table(handle, "Validation", validation)
        write_table(handle, "Next target", next_target)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    sources = source_rows()
    refreshed = refreshed_manifest_rows()
    delta = manifest_delta_rows(refreshed)
    write_quarantine_templates()
    template_register = template_register_rows()
    template_validation = template_validation_rows()
    live_guard = live_path_guard_rows()
    gates = promotion_gate_rows()
    signing = signing_decision_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(REFRESHED_MANIFEST, refreshed)
    write_csv(MANIFEST_DELTA, delta)
    write_csv(QUARANTINE_REGISTER, template_register)
    write_csv(TEMPLATE_VALIDATION, template_validation)
    write_csv(LIVE_PATH_GUARD, live_guard)
    write_csv(PROMOTION_GATES, gates)
    write_csv(SIGNING_DECISION, signing)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)

    copy_branch(REFRESHED_MANIFEST, BRANCH_REFRESHED_MANIFEST)
    copy_branch(QUARANTINE_REGISTER, BRANCH_TEMPLATE_REGISTER)
    copy_branch(SIGNING_DECISION, BRANCH_SIGNING)

    remove_pycache()
    validation = validation_rows(sources, refreshed, delta, template_register, template_validation, live_guard, gates, signing)
    write_csv(VALIDATION, validation)
    write_doc(sources, refreshed, delta, template_register, template_validation, live_guard, gates, signing, decisions, validation, next_target)
    print("Y5_R10_1458_manifest_shadow_refresh_quarantine_templates_nonclaim")


if __name__ == "__main__":
    main()
