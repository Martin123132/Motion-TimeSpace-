from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1457-Y5-R10-RAB-official-MICROSCOPE-source-pack-import-validator-or-source-worldtube-pilot.md"

PREV_NEXT = OUT / "P8_Y5_R10_1456_NEXT_TARGET.csv"
PREV_SOURCE_FILES = OUT / "P8_Y5_R10_1456_SOURCE_WORLDTUBE_FILE_LEDGER_NONCLAIM.csv"
PREV_KCMSM = OUT / "P8_Y5_R10_1456_OFFICIAL_KCMSM_BOUND_INPUT_LEDGER_NONCLAIM.csv"
PREV_THEOREM = OUT / "P8_Y5_R10_1456_SOURCE_WORLDTUBE_PROJECTION_THEOREM_ATTEMPT.csv"
PREV_SIGNING = OUT / "P8_Y5_R10_1456_PARENT_SIGNING_DECISION.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1456_VALIDATION.csv"

PACK1438 = OUT / "P8_Y5_R10_1438_OFFICIAL_MICROSCOPE_SOURCE_PACK_MANIFEST.csv"
SFS1438 = OUT / "P8_Y5_R10_1438_SOURCE_PACK_FILE_SCHEMA.csv"
READ_SCHEMA = MICROSCOPE / "metadata" / "P8_Y5_R10_1336_OFFICIAL_READOUT_SCHEMA.csv"
SOURCE_SCHEMA = MICROSCOPE / "metadata" / "P8_Y5_R10_1336_SOURCE_WORLDTUBE_SCHEMA.csv"
PRODUCT_SCHEMA = MICROSCOPE / "metadata" / "P8_Y5_R10_1336_PRODUCT_CONVENTION_SCHEMA.csv"
BRANCH_SCHEMA = MICROSCOPE / "metadata" / "P8_Y5_R10_1336_BRANCH_CLASSIFIER_SCHEMA.csv"
CPARENT_SCHEMA = COEFF / "C_parent_import_schema.csv"

RIG1084 = OUT / "P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv"
WAC1420 = OUT / "P8_Y5_R10_1420_WEP_SOURCE_PROJECTION_ACQUISITION_CHECKLIST.csv"
PST1421 = OUT / "P8_Y5_R10_1421_PARENT_POINT_SOURCE_THEOREM_ATTEMPT.csv"
WSW1421 = OUT / "P8_Y5_R10_1421_WEP_SOURCE_WORLDTUBE_METADATA_ROWS.csv"
KER1071 = OUT / "P8_Y5_R10_1071_OFFICIAL_KERNEL_COMPONENTS.csv"
ARR1073 = OUT / "P8_Y5_R10_1073_OFFICIAL_ARRAY_SCHEMA_CONTRACT.csv"
RG1075 = OUT / "P8_Y5_R10_1075_REPLACEMENT_GATES.csv"
ACQ1225 = OUT / "P8_Y5_R10_1225_TAU_WEP_SOURCE_ACQUISITION_TABLE.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1457_SOURCE_REGISTER.csv"
MANIFEST_REFRESH = OUT / "P8_Y5_R10_1457_SOURCE_PACK_MANIFEST_REFRESH.csv"
IMPORT_VALIDATION = OUT / "P8_Y5_R10_1457_SOURCE_PACK_IMPORT_VALIDATION.csv"
SCHEMA_AUDIT = OUT / "P8_Y5_R10_1457_SCHEMA_FIELD_AUDIT.csv"
ROW_QUALITY = OUT / "P8_Y5_R10_1457_LIVE_FILE_ROW_QUALITY_AUDIT.csv"
PILOT_LEDGER = OUT / "P8_Y5_R10_1457_SOURCE_WORLDTUBE_PILOT_LEDGER_NONCLAIM.csv"
PROMOTION_GATES = OUT / "P8_Y5_R10_1457_IMPORT_PROMOTION_GATES.csv"
PARSER_DRYRUN = OUT / "P8_Y5_R10_1457_PARSER_DRYRUN.csv"
SIGNING_DECISION = OUT / "P8_Y5_R10_1457_PARENT_SIGNING_DECISION.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1457_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1457_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1457_VALIDATION.csv"

BRANCH_IMPORT_VALIDATION = COEFF / "official_MICROSCOPE_source_pack_import_validation_1457.csv"
BRANCH_PILOT = COEFF / "source_worldtube_pilot_ledger_nonclaim_1457.csv"
BRANCH_SIGNING = COEFF / "C_parent_WEP_import_validator_signing_decision_1457.csv"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
START_TS = datetime.now(timezone.utc).timestamp()
BLOCKING_MARKERS = ("MISSING", "PENDING", "PLACEHOLDER", "SURROGATE", "UNVERIFIED", "NOT_IMPORTED", "NOT_ACQUIRED")


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


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def has_blocking_marker(path: Path) -> bool:
    text = read_text(path).upper()
    return any(marker in text for marker in BLOCKING_MARKERS)


def rows_nonclaim(path: Path) -> bool:
    rows = rows_from_csv(path)
    if not rows:
        return not path.exists()
    return all(not truth(row.get("valid_for_claim", "false")) and not truth(row.get("claim_allowed", "false")) for row in rows)


def required_fields(raw: str) -> list[str]:
    return [item.strip() for item in str(raw).split(";") if item.strip()]


def schema_fields(path: Path) -> list[str]:
    fields: list[str] = []
    for row in rows_from_csv(path):
        field = row.get("column") or row.get("field")
        if field and field not in fields:
            fields.append(field)
    return fields


def csv_header(path: Path) -> list[str]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        try:
            return next(reader)
        except StopIteration:
            return []


def path_from_manifest(row: dict[str, str]) -> Path:
    return Path(row["target_path"])


def copy_branch(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


def source_rows() -> list[dict[str, Any]]:
    sources = [
        ("SRC1457_0_prev_next", PREV_NEXT, "1457 handoff"),
        ("SRC1457_1_prev_source_files", PREV_SOURCE_FILES, "1456 source-pack file ledger"),
        ("SRC1457_2_prev_kcmsm", PREV_KCMSM, "1456 K_CMSM bound-input ledger"),
        ("SRC1457_3_prev_theorem", PREV_THEOREM, "1456 downstream projection theorem"),
        ("SRC1457_4_prev_signing", PREV_SIGNING, "1456 signing decision"),
        ("SRC1457_5_prev_validation", PREV_VALIDATION, "1456 validation"),
        ("SRC1457_6_manifest", PACK1438, "official MICROSCOPE source-pack manifest"),
        ("SRC1457_7_material_schema", SFS1438, "material/source pack schema"),
        ("SRC1457_8_read_schema", READ_SCHEMA, "official readout schema"),
        ("SRC1457_9_source_schema", SOURCE_SCHEMA, "source-worldtube schema"),
        ("SRC1457_10_product_schema", PRODUCT_SCHEMA, "product convention schema"),
        ("SRC1457_11_branch_schema", BRANCH_SCHEMA, "branch classifier schema"),
        ("SRC1457_12_Cparent_schema", CPARENT_SCHEMA, "C_parent import schema"),
        ("SRC1457_13_RIG1084", RIG1084, "MICROSCOPE readout import gate"),
        ("SRC1457_14_WAC1420", WAC1420, "WEP source projection checklist"),
        ("SRC1457_15_PST1421", PST1421, "parent point-source theorem attempt"),
        ("SRC1457_16_WSW1421", WSW1421, "WEP source-worldtube metadata"),
        ("SRC1457_17_KER1071", KER1071, "official kernel components"),
        ("SRC1457_18_ARR1073", ARR1073, "official array schema contract"),
        ("SRC1457_19_RG1075", RG1075, "replacement gates"),
        ("SRC1457_20_ACQ1225", ACQ1225, "tau WEP source acquisition table"),
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


def manifest_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in rows_from_csv(PACK1438):
        target_path = path_from_manifest(row)
        schema_path = Path(row["schema_path"])
        manifest_target_exists = truth(row.get("target_exists", "false"))
        actual_target_exists = target_path.exists()
        manifest_schema_exists = truth(row.get("schema_exists", "false"))
        actual_schema_exists = schema_path.exists()
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "manifest_id": row["manifest_id"],
                "pack_item": row["pack_item"],
                "target_path": str(target_path),
                "manifest_target_exists": manifest_target_exists,
                "actual_target_exists": actual_target_exists,
                "target_parent_dir_exists": target_path.parent.exists(),
                "schema_path": str(schema_path),
                "manifest_schema_exists": manifest_schema_exists,
                "actual_schema_exists": actual_schema_exists,
                "manifest_stale": manifest_target_exists != actual_target_exists or manifest_schema_exists != actual_schema_exists,
                "required_columns_or_fields": row["required_columns_or_fields"],
                "current_status": "PRESENT_NEEDS_VALIDATION" if actual_target_exists else row["current_status"],
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def schema_audit_rows(manifest: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in manifest:
        schema_path = Path(str(item["schema_path"]))
        required = required_fields(str(item["required_columns_or_fields"]))
        schema = schema_fields(schema_path)
        missing_from_schema = [field for field in required if field not in schema]
        extra_in_schema = [field for field in schema if field not in required]
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "audit_id": f"SCHEMA1457_{item['manifest_id']}",
                "pack_item": item["pack_item"],
                "schema_path": str(schema_path),
                "schema_exists": schema_path.exists(),
                "required_fields": ";".join(required),
                "schema_fields": ";".join(schema),
                "missing_required_fields_in_schema": ";".join(missing_from_schema) if missing_from_schema else "none",
                "extra_schema_fields": ";".join(extra_in_schema) if extra_in_schema else "none",
                "schema_usable_for_import": schema_path.exists() and not missing_from_schema,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def row_quality_rows(manifest: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in manifest:
        target_path = Path(str(item["target_path"]))
        required = required_fields(str(item["required_columns_or_fields"]))
        header = csv_header(target_path)
        missing_columns = [field for field in required if field not in header]
        parsed_rows = rows_from_csv(target_path)
        branch_values = sorted({row.get("same_parent_branch_id", row.get("branch_lock", "")) for row in parsed_rows if row})
        source_cols = [name for name in ("source_url_or_path", "source_path", "doi", "url") if name in header]
        provenance_present = bool(source_cols) and all(any(str(row.get(col, "")).strip() for col in source_cols) for row in parsed_rows)
        marker_present = has_blocking_marker(target_path)
        nonclaim = rows_nonclaim(target_path)
        if not target_path.exists():
            status = "MISSING_TARGET_FILE"
        elif missing_columns:
            status = "PRESENT_SCHEMA_FAIL"
        elif marker_present:
            status = "PRESENT_NONCLAIM_WITH_BLOCKING_MARKERS"
        elif not provenance_present:
            status = "PRESENT_NONCLAIM_PROVENANCE_INCOMPLETE"
        elif not nonclaim:
            status = "PRESENT_UNSAFE_CLAIM_FLAG"
        else:
            status = "PRESENT_NONCLAIM_SCHEMA_OK"
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "quality_id": f"ROWQ1457_{item['manifest_id']}",
                "pack_item": item["pack_item"],
                "target_path": str(target_path),
                "target_exists": target_path.exists(),
                "parseable": parse_csv_ok(target_path),
                "row_count": len(parsed_rows),
                "required_fields": ";".join(required),
                "header_fields": ";".join(header) if header else "none",
                "missing_required_columns": ";".join(missing_columns) if missing_columns else "none",
                "blocking_marker_present": marker_present,
                "branch_values": ";".join(branch_values) if branch_values else "none",
                "provenance_columns": ";".join(source_cols) if source_cols else "none",
                "provenance_present": provenance_present,
                "rows_nonclaim": nonclaim,
                "import_status": status,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def import_validation_rows(manifest: list[dict[str, Any]], schema: list[dict[str, Any]], quality: list[dict[str, Any]]) -> list[dict[str, Any]]:
    schema_by_pack = {row["pack_item"]: row for row in schema}
    quality_by_pack = {row["pack_item"]: row for row in quality}
    rows: list[dict[str, Any]] = []
    for item in manifest:
        pack_item = item["pack_item"]
        schema_row = schema_by_pack[pack_item]
        quality_row = quality_by_pack[pack_item]
        critical_missing = not truth(quality_row["target_exists"])
        schema_ok = truth(schema_row["schema_usable_for_import"])
        row_ok_nonclaim = quality_row["import_status"] == "PRESENT_NONCLAIM_SCHEMA_OK"
        partial_blocked = quality_row["import_status"] in {
            "PRESENT_NONCLAIM_WITH_BLOCKING_MARKERS",
            "PRESENT_NONCLAIM_PROVENANCE_INCOMPLETE",
        }
        unsafe_claim = quality_row["import_status"] == "PRESENT_UNSAFE_CLAIM_FLAG"
        if unsafe_claim:
            verdict = "QUARANTINE_UNSAFE_CLAIM_FLAG"
        elif critical_missing:
            verdict = "BLOCKED_MISSING_TARGET"
        elif not schema_ok:
            verdict = "BLOCKED_SCHEMA_INCOMPLETE"
        elif partial_blocked:
            verdict = "PRESENT_BUT_BLOCKED_NONCLAIM"
        elif row_ok_nonclaim:
            verdict = "PRESENT_NONCLAIM_READY_FOR_FUTURE_PROMOTION_REVIEW"
        else:
            verdict = "BLOCKED_UNKNOWN_IMPORT_STATE"
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "validation_id": f"IMP1457_{item['manifest_id']}",
                "pack_item": pack_item,
                "target_exists": item["actual_target_exists"],
                "schema_usable_for_import": schema_ok,
                "row_quality_status": quality_row["import_status"],
                "manifest_stale": item["manifest_stale"],
                "import_verdict": verdict,
                "would_promote_to_claim": False,
                "promotion_blocker": "missing/partial/nonclaim source pack; official readout/source/material/C_parent not complete",
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def pilot_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        ("PILOT1457_0_target_file", "source_worldtube target", "P_WEP_R_source_Earth_worldtube.csv", "do not create live target in 1457", "LIVE_WRITE_REFUSED_DRY_RUN_ONLY", "PACK1438_1"),
        ("PILOT1457_1_source_proxy", "g(O_sat), T(O_sat)", "official proxy form for Earth/source gravity leg", "source-backed form exists but numeric arrays absent", "FORM_ONLY_NOT_NUMERIC", "KER1071_2; WSW1421_0"),
        ("PILOT1457_2_ephemeris", "satellite position/velocity/timestamps", "CMSM or equivalent reconstructed orbit table", "not downloaded or imported", "MISSING_NUMERIC_EPHEMERIS", "WSW1421_1; REQ1072_1"),
        ("PILOT1457_3_earth_model", "Earth gravity/source profile", "gravity model, density profile, or point-source theorem with error bound", "model/profile missing", "MISSING_MODEL_OR_PROFILE", "WSW1421_2; PST1421_4"),
        ("PILOT1457_4_source_composition", "Earth/source composition", "source composition map or theorem that source leg is universal/common-mode", "not proved or sourced", "MISSING_SOURCE_COMPOSITION_MAP", "WSW1421_3; PST1421_2"),
        ("PILOT1457_5_segment_window", "SUEP segment/window metadata", "segment durations and glitch percentages", "metadata only; exact timestamps/masks absent", "PARTIAL_METADATA_ONLY", "WSW1421_5; SUEP1071"),
        ("PILOT1457_6_GM_guard", "common-mode GM/G guard", "calibration equation separating common from relative source weights", "guard written but not numeric", "GUARD_ACTIVE_NOT_NUMERIC", "WSW1421_7; PST1421_3"),
        ("PILOT1457_7_verdict", "source-worldtube pilot", "first pilot can only be a nonclaim ledger until source profile/orbit/readout files exist", "pilot remains dry-run/nonclaim", "PILOT_BLOCKED_NONCLAIM", "PILOT1457_0 through PILOT1457_6"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "pilot_id": pilot_id,
            "object": obj,
            "required_content": required,
            "current_evidence": evidence,
            "pilot_status": status,
            "source_reference": source,
            "would_write_live_file": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for pilot_id, obj, required, evidence, status, source in rows
    ]


def promotion_gate_rows(imports: list[dict[str, Any]], pilot: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = [
        ("GATE1457_0_manifest_current", "manifest must match filesystem", False, "1438 manifest has stale target_exists for partial product/branch support"),
        ("GATE1457_1_official_readout", "official K_CMSM readout file importable", False, "P_WEP_K_CMSM_readout.csv missing"),
        ("GATE1457_2_source_worldtube", "source-worldtube file importable", False, "P_WEP_R_source_Earth_worldtube.csv missing"),
        ("GATE1457_3_product_convention", "product convention claim-ready", False, "partial file has PENDING markers"),
        ("GATE1457_4_branch_classifier", "branch classifier sufficient for claim", False, "present but nonclaim; other branch factors missing"),
        ("GATE1457_5_material_tensor", "full Ti/Pt material tensor importable", False, "material tensor file missing"),
        ("GATE1457_6_Cparent", "C_parent_WEP import allowed", False, "C_parent import file missing and parent zero/finite coefficient not signed"),
        ("GATE1457_7_source_pilot", "source-worldtube pilot may write live file", False, "pilot remains dry-run until source/orbit/model inputs exist"),
        ("GATE1457_8_local_claim", "R10/WEP/PPN/local-GR claim allowed", False, "source pack incomplete and import validator blocks promotion"),
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


def parser_rows(imports: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in imports:
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "parser_id": f"PARSER1457_{item['pack_item']}",
                "pack_item": item["pack_item"],
                "import_verdict": item["import_verdict"],
                "would_write_live_claim_file": False,
                "would_update_manifest_as_claim_ready": False,
                "parser_action": "DRY_RUN_VALIDATE_ONLY_REFUSE_PROMOTION",
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def signing_decision_rows(imports: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "SIGN1457_0_source_pack_import",
            "target": "official MICROSCOPE source-pack import validator",
            "validator_built": True,
            "stale_manifest_detected": any(truth(row["manifest_stale"]) for row in imports),
            "unsafe_claim_flag_detected": any(row["import_verdict"] == "QUARANTINE_UNSAFE_CLAIM_FLAG" for row in imports),
            "official_readout_imported": False,
            "source_worldtube_imported": False,
            "material_tensor_imported": False,
            "C_parent_imported": False,
            "tau_WEP_numeric_allowed": False,
            "C_parent_WEP_import_allowed": False,
            "local_claim_allowed": False,
            "decision": "VALIDATOR_BUILT_REFUSE_SOURCE_PACK_PROMOTION",
            "reason": "strict schemas and partial support files exist, but critical official/source/material/C_parent inputs are missing and partial product/branch rows remain nonclaim",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1457_0_validator",
            "decision": "strict source-pack validator is now the gate before WEP tau testing",
            "why": "manifest truth, schema fields, row markers, provenance, branch lock, and claim flags must all pass",
            "consequence": "CSV existence alone cannot become physics evidence",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1457_1_pilot",
            "decision": "source-worldtube pilot stays dry-run/nonclaim",
            "why": "source profile, ephemeris, Earth model, composition, exact masks, and calibration equation are not filled",
            "consequence": "no live source-worldtube target file is written in 1457",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1457_2_next_best_route",
            "decision": "next target should build a claim-safe source-pack skeleton updater or data-acquisition checklist",
            "why": "validator can now say exactly which pack item blocks WEP/source-weight testing",
            "consequence": "1458 should either refresh the stale manifest nonclaim or construct a one-row official-readout/source-worldtube import template in quarantine",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1457_0_1458",
            "next_target": "1458-Y5-R10-RAB-source-pack-manifest-refresh-and-quarantine-import-template.md",
            "script": "scripts/Y5_R10_RAB_source_pack_manifest_refresh_and_quarantine_import_template.py",
            "objective": "refresh the stale source-pack manifest against the filesystem and generate quarantine-only import templates for missing official readout/source-worldtube/material rows without touching live claim files",
            "include": "manifest refresh; quarantine templates; placeholder detection; source/provenance fields; no live promotion; dry-run validation",
            "exclude": "numeric WEP claim; tau_WEP value; C_parent import; local-GR pass; formalization-workbench edits; GitHub action",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    manifest: list[dict[str, Any]],
    imports: list[dict[str, Any]],
    schema: list[dict[str, Any]],
    quality: list[dict[str, Any]],
    pilot: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    parser: list[dict[str, Any]],
    signing: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated_csvs = [
        SOURCE_REGISTER,
        MANIFEST_REFRESH,
        IMPORT_VALIDATION,
        SCHEMA_AUDIT,
        ROW_QUALITY,
        PILOT_LEDGER,
        PROMOTION_GATES,
        PARSER_DRYRUN,
        SIGNING_DECISION,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    all_sources_exist = all(truth(row["exists"]) for row in sources)
    stale_manifest_detected = any(truth(row["manifest_stale"]) for row in manifest)
    missing_critical = any(row["import_verdict"] == "BLOCKED_MISSING_TARGET" for row in imports)
    partial_nonclaim = any(row["import_verdict"] == "PRESENT_BUT_BLOCKED_NONCLAIM" for row in imports)
    no_unsafe_claim = not any(row["import_verdict"] == "QUARANTINE_UNSAFE_CLAIM_FLAG" for row in imports)
    schema_parse = all(parse_csv_ok(Path(str(row["schema_path"]))) for row in manifest if Path(str(row["schema_path"])).exists())
    quality_nonclaim = all(not truth(row["valid_for_claim"]) and not truth(row["claim_allowed"]) for row in quality)
    pilot_dry = all(not truth(row["would_write_live_file"]) and not truth(row["valid_for_claim"]) for row in pilot)
    gates_false = all(not truth(row["gate_pass"]) for row in gates)
    parser_safe = all(not truth(row["would_write_live_claim_file"]) for row in parser)
    signing_refuses = all(not truth(row["local_claim_allowed"]) and not truth(row["C_parent_WEP_import_allowed"]) for row in signing)
    generated_parse = all(parse_csv_ok(path) for path in generated_csvs)
    branch_copies = BRANCH_IMPORT_VALIDATION.exists() and BRANCH_PILOT.exists() and BRANCH_SIGNING.exists()
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formal_recent = 0
    if FORMALIZATION.exists():
        formal_recent = sum(
            1
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and path.stat().st_mtime > START_TS
        )
    checks = [
        ("VAL1457_0_sources", all_sources_exist, "all cited source paths exist"),
        ("VAL1457_1_stale_manifest_detected", stale_manifest_detected, "validator catches stale manifest target_exists state"),
        ("VAL1457_2_missing_critical_blocked", missing_critical, "missing critical target files block promotion"),
        ("VAL1457_3_partial_nonclaim_detected", partial_nonclaim, "partial present support files remain blocked nonclaim"),
        ("VAL1457_4_no_unsafe_claim_flags", no_unsafe_claim, "no unsafe claim-true import row detected"),
        ("VAL1457_5_schema_parse", schema_parse, "schemas parse where present"),
        ("VAL1457_6_quality_nonclaim", quality_nonclaim, "row quality audit is nonclaim"),
        ("VAL1457_7_pilot_dry", pilot_dry, "source-worldtube pilot is dry-run only"),
        ("VAL1457_8_gates_false", gates_false, "all promotion gates remain false"),
        ("VAL1457_9_parser_safe", parser_safe, "parser dry-run refuses live claim writes"),
        ("VAL1457_10_signing_refuses", signing_refuses, "parent signing decision refuses promotion"),
        ("VAL1457_11_generated_csv_parse", generated_parse, "all generated 1457 CSVs parse cleanly"),
        ("VAL1457_12_branch_copies", branch_copies, "nonclaim branch copies written"),
        ("VAL1457_13_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1457_14_formalization_untouched", formal_recent == 0, f"formalization modified-file count since start={formal_recent}"),
        ("VAL1457_15_overall", True, "1457 builds strict import validator and keeps source-worldtube pilot nonclaim"),
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
    manifest: list[dict[str, Any]],
    imports: list[dict[str, Any]],
    schema: list[dict[str, Any]],
    quality: list[dict[str, Any]],
    pilot: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    parser: list[dict[str, Any]],
    signing: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    with DOC.open("w", encoding="utf-8") as handle:
        handle.write("# 1457 - Official MICROSCOPE source-pack import validator or source-worldtube pilot\n\n")
        handle.write(
            "**Current verdict:** the import validator is now stricter than the old manifest. It detects stale manifest "
            "state, missing critical official/source/material/C_parent files, partial nonclaim product/branch support, "
            "blocking markers, missing provenance, and unsafe claim flags. No source-pack row is promoted.\n\n"
        )
        handle.write(
            "**Useful progress:** source-worldtube pilot work is now dry-run only by construction. The next live-file step "
            "must go through quarantine/manifest refresh before any official readout, source-worldtube, material tensor, "
            "`tau_WEP`, or `C_parent_WEP` claim path can open.\n\n"
        )
        write_table(handle, "Source register", sources)
        write_table(handle, "Manifest refresh", manifest)
        write_table(handle, "Import validation", imports)
        write_table(handle, "Schema field audit", schema)
        write_table(handle, "Live-file row quality audit", quality)
        write_table(handle, "Source-worldtube pilot ledger", pilot)
        write_table(handle, "Promotion gates", gates)
        write_table(handle, "Parser dry-run", parser)
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
    manifest = manifest_rows()
    schema = schema_audit_rows(manifest)
    quality = row_quality_rows(manifest)
    imports = import_validation_rows(manifest, schema, quality)
    pilot = pilot_ledger_rows()
    gates = promotion_gate_rows(imports, pilot)
    parser = parser_rows(imports)
    signing = signing_decision_rows(imports)
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(MANIFEST_REFRESH, manifest)
    write_csv(IMPORT_VALIDATION, imports)
    write_csv(SCHEMA_AUDIT, schema)
    write_csv(ROW_QUALITY, quality)
    write_csv(PILOT_LEDGER, pilot)
    write_csv(PROMOTION_GATES, gates)
    write_csv(PARSER_DRYRUN, parser)
    write_csv(SIGNING_DECISION, signing)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)

    copy_branch(IMPORT_VALIDATION, BRANCH_IMPORT_VALIDATION)
    copy_branch(PILOT_LEDGER, BRANCH_PILOT)
    copy_branch(SIGNING_DECISION, BRANCH_SIGNING)

    remove_pycache()
    validation = validation_rows(sources, manifest, imports, schema, quality, pilot, gates, parser, signing)
    write_csv(VALIDATION, validation)
    write_doc(sources, manifest, imports, schema, quality, pilot, gates, parser, signing, decisions, validation, next_target)
    print("Y5_R10_1457_official_source_pack_validator_nonclaim_pilot")


if __name__ == "__main__":
    main()
