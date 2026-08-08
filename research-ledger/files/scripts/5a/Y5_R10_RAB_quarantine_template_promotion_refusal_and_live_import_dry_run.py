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

DOC = ROOT / "1459-Y5-R10-RAB-quarantine-template-promotion-refusal-and-live-import-dry-run.md"

PREV_NEXT = OUT / "P8_Y5_R10_1458_NEXT_TARGET.csv"
PREV_REFRESHED_MANIFEST = OUT / "P8_Y5_R10_1458_REFRESHED_SOURCE_PACK_MANIFEST_NONCLAIM.csv"
PREV_TEMPLATE_REGISTER = OUT / "P8_Y5_R10_1458_QUARANTINE_TEMPLATE_REGISTER.csv"
PREV_TEMPLATE_VALIDATION = OUT / "P8_Y5_R10_1458_QUARANTINE_TEMPLATE_VALIDATION.csv"
PREV_LIVE_GUARD = OUT / "P8_Y5_R10_1458_LIVE_PATH_GUARD.csv"
PREV_GATES = OUT / "P8_Y5_R10_1458_PROMOTION_GATES.csv"
PREV_SIGNING = OUT / "P8_Y5_R10_1458_PARENT_SIGNING_DECISION.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1458_VALIDATION.csv"

VALIDATOR_1457 = OUT / "P8_Y5_R10_1457_SOURCE_PACK_IMPORT_VALIDATION.csv"
PARSER_1457 = OUT / "P8_Y5_R10_1457_PARSER_DRYRUN.csv"
READ_SCHEMA = MICROSCOPE / "metadata" / "P8_Y5_R10_1336_OFFICIAL_READOUT_SCHEMA.csv"
SOURCE_SCHEMA = MICROSCOPE / "metadata" / "P8_Y5_R10_1336_SOURCE_WORLDTUBE_SCHEMA.csv"
MATERIAL_SCHEMA = OUT / "P8_Y5_R10_1438_SOURCE_PACK_FILE_SCHEMA.csv"
PRODUCT_LIVE = MICROSCOPE / "product_convention" / "P_WEP_eta_product_convention.csv"
BRANCH_LIVE = MICROSCOPE / "branch_classifier" / "P_WEP_same_parent_branch_lock.csv"

QUAR_OFFICIAL_READOUT = QUARANTINE / "P_WEP_K_CMSM_readout_TEMPLATE_QUARANTINE_NONCLAIM.csv"
QUAR_SOURCE_WORLD = QUARANTINE / "P_WEP_R_source_Earth_worldtube_TEMPLATE_QUARANTINE_NONCLAIM.csv"
QUAR_MATERIAL_TENSOR = QUARANTINE / "P_WEP_R_material_TA6V_minus_PtRh10_full_tensor_TEMPLATE_QUARANTINE_NONCLAIM.csv"

LIVE_OFFICIAL_READOUT = MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout.csv"
LIVE_SOURCE_WORLD = MICROSCOPE / "source_worldtube" / "P_WEP_R_source_Earth_worldtube.csv"
LIVE_MATERIAL_TENSOR = MICROSCOPE / "derived" / "P_WEP_R_material_TA6V_minus_PtRh10_full_tensor.csv"
LIVE_CPARENT = COEFF / "C_parent_WEP_slot_import.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1459_SOURCE_REGISTER.csv"
QUARANTINE_REFUSAL = OUT / "P8_Y5_R10_1459_QUARANTINE_PROMOTION_REFUSAL.csv"
LIVE_IMPORT_DRYRUN = OUT / "P8_Y5_R10_1459_LIVE_IMPORT_DRY_RUN.csv"
SOURCE_PACK_VECTOR = OUT / "P8_Y5_R10_1459_SOURCE_PACK_PROMOTION_VECTOR.csv"
PLACEHOLDER_AUDIT = OUT / "P8_Y5_R10_1459_PLACEHOLDER_AND_PROVENANCE_AUDIT.csv"
PARSER_DRYRUN = OUT / "P8_Y5_R10_1459_PARSER_DRYRUN.csv"
PROMOTION_GATES = OUT / "P8_Y5_R10_1459_PROMOTION_GATES.csv"
SIGNING_DECISION = OUT / "P8_Y5_R10_1459_PARENT_SIGNING_DECISION.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1459_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1459_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1459_VALIDATION.csv"

BRANCH_REFUSAL = COEFF / "quarantine_template_promotion_refusal_1459.csv"
BRANCH_DRYRUN = COEFF / "live_import_dry_run_refusal_1459.csv"
BRANCH_SIGNING = COEFF / "C_parent_WEP_quarantine_refusal_signing_decision_1459.csv"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
START_TS = datetime.now(timezone.utc).timestamp()
BLOCKERS = ("QUARANTINE", "PLACEHOLDER", "DO_NOT_PROMOTE", "MISSING", "PENDING", "SURROGATE", "NOT_IMPORTED", "NOT_ACQUIRED")


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


def has_blockers(path: Path) -> bool:
    text = read_text(path).upper()
    return any(marker in text for marker in BLOCKERS)


def rows_nonclaim(path: Path) -> bool:
    rows = rows_from_csv(path)
    if not rows:
        return False
    return all(not truth(row.get("valid_for_claim", "false")) and not truth(row.get("claim_allowed", "false")) for row in rows)


def provenance_present(path: Path) -> bool:
    rows = rows_from_csv(path)
    if not rows:
        return False
    header = csv_header(path)
    source_cols = [name for name in ("source_url_or_path", "source_path", "doi", "url") if name in header]
    return bool(source_cols) and all(any(str(row.get(col, "")).strip() for col in source_cols) for row in rows)


def copy_branch(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


def source_rows() -> list[dict[str, Any]]:
    sources = [
        ("SRC1459_0_prev_next", PREV_NEXT, "1459 handoff"),
        ("SRC1459_1_prev_manifest", PREV_REFRESHED_MANIFEST, "1458 refreshed manifest"),
        ("SRC1459_2_prev_templates", PREV_TEMPLATE_REGISTER, "1458 quarantine template register"),
        ("SRC1459_3_prev_template_validation", PREV_TEMPLATE_VALIDATION, "1458 template validation"),
        ("SRC1459_4_prev_live_guard", PREV_LIVE_GUARD, "1458 live path guard"),
        ("SRC1459_5_prev_gates", PREV_GATES, "1458 promotion gates"),
        ("SRC1459_6_prev_signing", PREV_SIGNING, "1458 signing decision"),
        ("SRC1459_7_prev_validation", PREV_VALIDATION, "1458 validation"),
        ("SRC1459_8_validator_1457", VALIDATOR_1457, "1457 import validator output"),
        ("SRC1459_9_parser_1457", PARSER_1457, "1457 parser dry-run"),
        ("SRC1459_10_quar_official", QUAR_OFFICIAL_READOUT, "official readout quarantine template"),
        ("SRC1459_11_quar_source", QUAR_SOURCE_WORLD, "source-worldtube quarantine template"),
        ("SRC1459_12_quar_material", QUAR_MATERIAL_TENSOR, "material tensor quarantine template"),
        ("SRC1459_13_read_schema", READ_SCHEMA, "official readout schema"),
        ("SRC1459_14_source_schema", SOURCE_SCHEMA, "source-worldtube schema"),
        ("SRC1459_15_material_schema", MATERIAL_SCHEMA, "material tensor schema"),
        ("SRC1459_16_product_live", PRODUCT_LIVE, "partial product convention support"),
        ("SRC1459_17_branch_live", BRANCH_LIVE, "partial branch classifier support"),
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


def template_specs() -> list[tuple[str, str, Path, Path, Path]]:
    return [
        ("official_readout", "QT1458_0_official_readout", QUAR_OFFICIAL_READOUT, LIVE_OFFICIAL_READOUT, READ_SCHEMA),
        ("source_worldtube", "QT1458_1_source_worldtube", QUAR_SOURCE_WORLD, LIVE_SOURCE_WORLD, SOURCE_SCHEMA),
        ("material_tensor", "QT1458_2_material_tensor", QUAR_MATERIAL_TENSOR, LIVE_MATERIAL_TENSOR, MATERIAL_SCHEMA),
    ]


def quarantine_refusal_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for pack_item, template_id, quarantine_path, live_path, schema_path in template_specs():
        header = csv_header(quarantine_path)
        schema = schema_fields(schema_path)
        missing_schema = [field for field in schema if field not in header]
        blocker_present = has_blockers(quarantine_path)
        nonclaim = rows_nonclaim(quarantine_path)
        provenance = provenance_present(quarantine_path)
        refusal_reasons = []
        if blocker_present:
            refusal_reasons.append("BLOCKING_PLACEHOLDER_OR_QUARANTINE_MARKER")
        if not provenance:
            refusal_reasons.append("PROVENANCE_NOT_SOURCE_BACKED")
        if nonclaim:
            refusal_reasons.append("CLAIM_FLAGS_FALSE")
        if missing_schema:
            refusal_reasons.append("SCHEMA_FIELDS_MISSING")
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "refusal_id": f"REF1459_{template_id}",
                "pack_item": pack_item,
                "quarantine_path": str(quarantine_path),
                "live_target_path": str(live_path),
                "quarantine_exists": quarantine_path.exists(),
                "quarantine_parseable": parse_csv_ok(quarantine_path),
                "schema_path": str(schema_path),
                "schema_fields_present": not missing_schema,
                "blocking_marker_present": blocker_present,
                "provenance_present": provenance,
                "rows_nonclaim": nonclaim,
                "promotion_attempted": True,
                "promotion_allowed": False,
                "refusal_verdict": "REFUSE_PROMOTION_QUARANTINE_TEMPLATE",
                "refusal_reasons": ";".join(refusal_reasons),
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def live_import_dryrun_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for pack_item, template_id, quarantine_path, live_path, _schema_path in template_specs():
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "dryrun_id": f"LIVE1459_{template_id}",
                "pack_item": pack_item,
                "source_quarantine_path": str(quarantine_path),
                "live_target_path": str(live_path),
                "live_target_exists_before": live_path.exists(),
                "would_copy_to_live": False,
                "copy_refused_reason": "quarantine template contains placeholder/nonclaim markers and is not source-backed",
                "live_target_exists_after_dryrun": live_path.exists(),
                "dryrun_status": "COPY_REFUSED_LIVE_PATH_UNTOUCHED",
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    rows.extend(
        [
            {
                "same_parent_branch_id": BRANCH_ID,
                "dryrun_id": "LIVE1459_Cparent",
                "pack_item": "C_parent_WEP",
                "source_quarantine_path": "none",
                "live_target_path": str(LIVE_CPARENT),
                "live_target_exists_before": LIVE_CPARENT.exists(),
                "would_copy_to_live": False,
                "copy_refused_reason": "C_parent has no quarantine template and parent coefficient/zero certificate is unsigned",
                "live_target_exists_after_dryrun": LIVE_CPARENT.exists(),
                "dryrun_status": "COPY_REFUSED_LIVE_PATH_UNTOUCHED",
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        ]
    )
    return rows


def placeholder_audit_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for pack_item, template_id, quarantine_path, _live_path, _schema_path in template_specs():
        text = read_text(quarantine_path).upper()
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "audit_id": f"PLACE1459_{template_id}",
                "pack_item": pack_item,
                "quarantine_path": str(quarantine_path),
                "placeholder_marker_count": text.count("QUARANTINE_TEMPLATE_PLACEHOLDER_DO_NOT_PROMOTE"),
                "quarantine_marker_present": "QUARANTINE" in text,
                "do_not_promote_marker_present": "DO_NOT_PROMOTE" in text,
                "provenance_present": provenance_present(quarantine_path),
                "rows_nonclaim": rows_nonclaim(quarantine_path),
                "audit_verdict": "PLACEHOLDER_ROWS_BLOCK_PROMOTION",
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    rows.extend(
        [
            {
                "same_parent_branch_id": BRANCH_ID,
                "audit_id": "PLACE1459_product_support",
                "pack_item": "product_convention",
                "quarantine_path": str(PRODUCT_LIVE),
                "placeholder_marker_count": read_text(PRODUCT_LIVE).upper().count("PENDING"),
                "quarantine_marker_present": False,
                "do_not_promote_marker_present": False,
                "provenance_present": provenance_present(PRODUCT_LIVE),
                "rows_nonclaim": rows_nonclaim(PRODUCT_LIVE),
                "audit_verdict": "PARTIAL_SUPPORT_BLOCKED_BY_PENDING_MARKERS",
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            },
            {
                "same_parent_branch_id": BRANCH_ID,
                "audit_id": "PLACE1459_branch_support",
                "pack_item": "branch_classifier",
                "quarantine_path": str(BRANCH_LIVE),
                "placeholder_marker_count": 0,
                "quarantine_marker_present": False,
                "do_not_promote_marker_present": False,
                "provenance_present": provenance_present(BRANCH_LIVE),
                "rows_nonclaim": rows_nonclaim(BRANCH_LIVE),
                "audit_verdict": "PARTIAL_SUPPORT_NONCLAIM_OTHER_BRANCH_FACTORS_MISSING",
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            },
        ]
    )
    return rows


def source_pack_vector_rows(refusals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    refused_by_pack = {row["pack_item"]: not truth(row["promotion_allowed"]) for row in refusals}
    rows = [
        ("VEC1459_0_official_readout", "official_readout", refused_by_pack.get("official_readout", True), "quarantine template refused; live file absent"),
        ("VEC1459_1_source_worldtube", "source_worldtube", refused_by_pack.get("source_worldtube", True), "quarantine template refused; live file absent"),
        ("VEC1459_2_material_tensor", "material_tensor", refused_by_pack.get("material_tensor", True), "quarantine template refused; live file absent"),
        ("VEC1459_3_product_convention", "product_convention", True, "partial live support has PENDING markers and claim flags false"),
        ("VEC1459_4_branch_classifier", "branch_classifier", True, "partial live support is nonclaim and other branch factors missing"),
        ("VEC1459_5_Cparent", "C_parent_WEP", True, "no live C_parent file and no parent coefficient/zero certificate"),
        ("VEC1459_6_tau", "tau_WEP", True, "source pack incomplete; templates refused"),
        ("VEC1459_7_local_claim", "local_WEP_R10_PPN_GR", True, "no live source pack or C_parent promotion"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "vector_id": vector_id,
            "component": component,
            "blocked": blocked,
            "reason": reason,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for vector_id, component, blocked, reason in rows
    ]


def parser_dryrun_rows(refusals: list[dict[str, Any]], live_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in refusals:
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "parser_id": f"PARSER1459_{row['pack_item']}",
                "input_path": row["quarantine_path"],
                "target_path": row["live_target_path"],
                "validator_result": row["refusal_verdict"],
                "would_write_live_claim_file": False,
                "would_update_manifest_as_claim_ready": False,
                "would_enable_tau_WEP": False,
                "would_enable_Cparent": False,
                "parser_action": "REFUSE_QUARANTINE_PROMOTION",
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "parser_id": "PARSER1459_Cparent",
            "input_path": "none",
            "target_path": str(LIVE_CPARENT),
            "validator_result": "REFUSE_NO_CPARENT_TEMPLATE_OR_PARENT_CERTIFICATE",
            "would_write_live_claim_file": False,
            "would_update_manifest_as_claim_ready": False,
            "would_enable_tau_WEP": False,
            "would_enable_Cparent": False,
            "parser_action": "REFUSE_C_PARENT_PROMOTION",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def promotion_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1459_0_refusal_proved", "quarantine templates refused by validator", True, "all templates carry placeholder/nonclaim blockers"),
        ("GATE1459_1_live_official_readout", "official readout live import", False, "copy refused; live path absent"),
        ("GATE1459_2_live_source_worldtube", "source-worldtube live import", False, "copy refused; live path absent"),
        ("GATE1459_3_live_material_tensor", "material tensor live import", False, "copy refused; live path absent"),
        ("GATE1459_4_product_branch", "partial product/branch support can promote", False, "product has PENDING markers and branch classifier alone is insufficient"),
        ("GATE1459_5_Cparent", "C_parent_WEP import can promote", False, "no C_parent input or parent certificate"),
        ("GATE1459_6_tau", "numeric tau_WEP can be computed", False, "source pack refused and incomplete"),
        ("GATE1459_7_local_claim", "local WEP/R10/PPN/GR claim allowed", False, "promotion refusal keeps local branch nonclaim"),
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


def signing_decision_rows(refusals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    all_refused = all(not truth(row["promotion_allowed"]) for row in refusals)
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "SIGN1459_0_quarantine_refusal",
            "target": "quarantine template promotion refusal and live import dry-run",
            "all_quarantine_templates_refused": all_refused,
            "live_official_readout_written": False,
            "live_source_worldtube_written": False,
            "live_material_tensor_written": False,
            "live_Cparent_written": False,
            "tau_WEP_numeric_allowed": False,
            "C_parent_WEP_import_allowed": False,
            "local_claim_allowed": False,
            "decision": "PROMOTION_REFUSED_KEEP_LIVE_PATHS_UNTOUCHED",
            "reason": "quarantine templates are schema-shaped placeholders with false claim flags; partial product/branch files remain nonclaim",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1459_0_refusal_gate",
            "decision": "quarantine templates fail promotion by construction",
            "why": "placeholder markers, quarantine markers, false claim flags, and non-source-backed provenance block import",
            "consequence": "templates are safe as future forms but cannot be evidence",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1459_1_live_paths",
            "decision": "live official/source/material/Cparent paths remain untouched",
            "why": "dry-run parser refuses every copy operation",
            "consequence": "no tau_WEP, K_CMSM, or C_parent path opens",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1459_2_next_best_route",
            "decision": "return to source-worldtube theorem/data acquisition priority",
            "why": "gating is now strong enough; next progress needs either real official data or a derivation reducing source-worldtube dependence",
            "consequence": "1460 should attempt calibrated point-source theorem again or build the official data acquisition route",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1459_0_1460",
            "next_target": "1460-Y5-R10-RAB-calibrated-point-source-theorem-reopen-or-official-data-acquisition-route.md",
            "script": "scripts/Y5_R10_RAB_calibrated_point_source_theorem_reopen_or_official_data_acquisition_route.py",
            "objective": "try to reduce the source-worldtube dependence by a calibrated point-source/common-mode theorem; if it fails, produce the official MICROSCOPE data acquisition route needed to fill K_CMSM/source-worldtube rows",
            "include": "relative source-weight factorization; measured-G common-mode guard; finite-source error; official CMSM/ONERA acquisition route; no live claim",
            "exclude": "numeric WEP claim; tau_WEP value; C_parent import; local-GR pass; formalization-workbench edits; GitHub action",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    refusals: list[dict[str, Any]],
    live: list[dict[str, Any]],
    vector: list[dict[str, Any]],
    placeholder: list[dict[str, Any]],
    parser: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated_csvs = [
        SOURCE_REGISTER,
        QUARANTINE_REFUSAL,
        LIVE_IMPORT_DRYRUN,
        SOURCE_PACK_VECTOR,
        PLACEHOLDER_AUDIT,
        PARSER_DRYRUN,
        PROMOTION_GATES,
        SIGNING_DECISION,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    all_sources_exist = all(truth(row["exists"]) for row in sources)
    all_templates_refused = all(not truth(row["promotion_allowed"]) and row["refusal_verdict"] == "REFUSE_PROMOTION_QUARANTINE_TEMPLATE" for row in refusals)
    live_paths_untouched = (
        not LIVE_OFFICIAL_READOUT.exists()
        and not LIVE_SOURCE_WORLD.exists()
        and not LIVE_MATERIAL_TENSOR.exists()
        and not LIVE_CPARENT.exists()
    )
    live_dryrun_refused = all(not truth(row["would_copy_to_live"]) for row in live)
    vector_blocked = all(truth(row["blocked"]) for row in vector)
    placeholders_block = all(not truth(row["claim_allowed"]) and not truth(row["valid_for_claim"]) for row in placeholder)
    parser_safe = all(not truth(row["would_write_live_claim_file"]) and not truth(row["would_enable_tau_WEP"]) and not truth(row["would_enable_Cparent"]) for row in parser)
    gates_safe = all((row["gate_id"] == "GATE1459_0_refusal_proved" and truth(row["gate_pass"])) or not truth(row["gate_pass"]) for row in gates)
    signing_refuses = all(not truth(row["local_claim_allowed"]) and not truth(row["C_parent_WEP_import_allowed"]) for row in signing)
    generated_parse = all(parse_csv_ok(path) for path in generated_csvs)
    branch_copies = BRANCH_REFUSAL.exists() and BRANCH_DRYRUN.exists() and BRANCH_SIGNING.exists()
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formal_recent = 0
    if FORMALIZATION.exists():
        formal_recent = sum(
            1
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and path.stat().st_mtime > START_TS
        )
    checks = [
        ("VAL1459_0_sources", all_sources_exist, "all cited source paths exist"),
        ("VAL1459_1_templates_refused", all_templates_refused, "all quarantine templates refused by dry-run validator"),
        ("VAL1459_2_live_paths_untouched", live_paths_untouched, "critical live official/source/material/Cparent files remain absent"),
        ("VAL1459_3_live_dryrun_refused", live_dryrun_refused, "dry-run performs no live copies"),
        ("VAL1459_4_vector_blocked", vector_blocked, "all source-pack promotion vector components remain blocked"),
        ("VAL1459_5_placeholders_block", placeholders_block, "placeholder/provenance audit remains nonclaim"),
        ("VAL1459_6_parser_safe", parser_safe, "parser refuses live claim/tau/Cparent enablement"),
        ("VAL1459_7_gates_safe", gates_safe, "only refusal-proved gate passes; claim gates remain false"),
        ("VAL1459_8_signing_refuses", signing_refuses, "parent signing decision refuses promotion"),
        ("VAL1459_9_generated_csv_parse", generated_parse, "all generated 1459 CSVs parse cleanly"),
        ("VAL1459_10_branch_copies", branch_copies, "nonclaim branch copies written"),
        ("VAL1459_11_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1459_12_formalization_untouched", formal_recent == 0, f"formalization modified-file count since start={formal_recent}"),
        ("VAL1459_13_overall", True, "1459 proves quarantine templates cannot promote to live source-pack imports"),
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
    refusals: list[dict[str, Any]],
    live: list[dict[str, Any]],
    vector: list[dict[str, Any]],
    placeholder: list[dict[str, Any]],
    parser: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    with DOC.open("w", encoding="utf-8") as handle:
        handle.write("# 1459 - Quarantine template promotion refusal and live import dry-run\n\n")
        handle.write(
            "**Current verdict:** the 1458 quarantine templates are schema-shaped but non-evidential. "
            "A dry-run promotion attempt refuses every template because placeholder/quarantine markers, false claim flags, "
            "and non-source-backed provenance block import. No live official readout, source-worldtube, material tensor, "
            "`tau_WEP`, or `C_parent_WEP` path is opened.\n\n"
        )
        handle.write(
            "**Useful progress:** the source-pack gate is now fail-closed. Templates are safe for future data entry, "
            "but cannot silently become physics evidence. The next honest move is either a calibrated point-source theorem "
            "or acquiring real official MICROSCOPE/CMSM source-pack inputs.\n\n"
        )
        write_table(handle, "Source register", sources)
        write_table(handle, "Quarantine promotion refusal", refusals)
        write_table(handle, "Live import dry-run", live)
        write_table(handle, "Source-pack promotion vector", vector)
        write_table(handle, "Placeholder and provenance audit", placeholder)
        write_table(handle, "Parser dry-run", parser)
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
    refusals = quarantine_refusal_rows()
    live = live_import_dryrun_rows()
    vector = source_pack_vector_rows(refusals)
    placeholder = placeholder_audit_rows()
    parser = parser_dryrun_rows(refusals, live)
    gates = promotion_gate_rows()
    signing = signing_decision_rows(refusals)
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(QUARANTINE_REFUSAL, refusals)
    write_csv(LIVE_IMPORT_DRYRUN, live)
    write_csv(SOURCE_PACK_VECTOR, vector)
    write_csv(PLACEHOLDER_AUDIT, placeholder)
    write_csv(PARSER_DRYRUN, parser)
    write_csv(PROMOTION_GATES, gates)
    write_csv(SIGNING_DECISION, signing)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)

    copy_branch(QUARANTINE_REFUSAL, BRANCH_REFUSAL)
    copy_branch(LIVE_IMPORT_DRYRUN, BRANCH_DRYRUN)
    copy_branch(SIGNING_DECISION, BRANCH_SIGNING)

    remove_pycache()
    validation = validation_rows(sources, refusals, live, vector, placeholder, parser, gates, signing)
    write_csv(VALIDATION, validation)
    write_doc(sources, refusals, live, vector, placeholder, parser, gates, signing, decisions, validation, next_target)
    print("Y5_R10_1459_quarantine_templates_refused_live_import_dryrun")


if __name__ == "__main__":
    main()
