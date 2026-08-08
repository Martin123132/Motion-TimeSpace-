from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
METADATA = MICROSCOPE / "metadata"
BRANCH_ROOT = MICROSCOPE / "branch_locked_wep"
COEFFICIENT_ROOT = BRANCH_ROOT / "coefficients"
RESIDUAL_ROOT = BRANCH_ROOT / "residuals"
PRODUCT_ROOT = BRANCH_ROOT / "product"
GUARD_ROOT = BRANCH_ROOT / "guards"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1438-Y5-R10-RAB-WEP-slot-C-parent-zero-or-official-source-pack-intake.md"

BRANCH_ID_FILE = BRANCH_ROOT / "branch_id.csv"
C_PARENT_FILE = COEFFICIENT_ROOT / "C_parent.csv"
C_PARENT_IMPORT_SCHEMA = COEFFICIENT_ROOT / "C_parent_import_schema.csv"
ETA_PRODUCT_CONVENTION = PRODUCT_ROOT / "eta_product_convention.csv"
MEASURED_G_GUARD = GUARD_ROOT / "measured_G_guard.csv"

NEXT_1437 = OUT / "P8_Y5_R10_1437_NEXT_TARGET.csv"
READINESS_1437 = OUT / "P8_Y5_R10_1437_INPUT_READINESS_AUDIT.csv"
ACQUISITION_1437 = OUT / "P8_Y5_R10_1437_SOURCE_ACQUISITION_LEDGER.csv"
VALIDATION_1437 = OUT / "P8_Y5_BRR545_1437_VALIDATION.csv"
BOUND_SEPARATION_1437 = OUT / "P8_Y5_R10_1437_BOUND_VS_PROJECTION_SEPARATION.csv"
WEP_ROW_ATTEMPT_1437 = RESIDUAL_ROOT / "P_WEP_first_row_attempt.csv"
WEP_ACQUISITION_1437 = RESIDUAL_ROOT / "P_WEP_source_acquisition_ledger.csv"

LOCAL_AUDIT_1336 = METADATA / "P8_Y5_R10_1336_LOCAL_MICROSCOPE_INTAKE_AUDIT.csv"
READOUT_SCHEMA_1336 = METADATA / "P8_Y5_R10_1336_OFFICIAL_READOUT_SCHEMA.csv"
SOURCE_SCHEMA_1336 = METADATA / "P8_Y5_R10_1336_SOURCE_WORLDTUBE_SCHEMA.csv"
PRODUCT_SCHEMA_1336 = METADATA / "P8_Y5_R10_1336_PRODUCT_CONVENTION_SCHEMA.csv"
BRANCH_SCHEMA_1336 = METADATA / "P8_Y5_R10_1336_BRANCH_CLASSIFIER_SCHEMA.csv"
WEB_SOURCES_1336 = METADATA / "P8_Y5_R10_1336_WEB_SOURCE_CANDIDATE_REGISTER.csv"
VALIDATION_1336 = METADATA / "P8_Y5_BRR545_1336_VALIDATION.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1438_SOURCE_REGISTER.csv"
C_PARENT_ZERO_ATTEMPT = OUT / "P8_Y5_R10_1438_C_PARENT_WEP_SLOT_ZERO_ATTEMPT.csv"
C_PARENT_SLOT_STATUS = OUT / "P8_Y5_R10_1438_C_PARENT_WEP_SLOT_STATUS.csv"
OFFICIAL_SOURCE_PACK_MANIFEST = OUT / "P8_Y5_R10_1438_OFFICIAL_MICROSCOPE_SOURCE_PACK_MANIFEST.csv"
SOURCE_PACK_FILE_SCHEMA = OUT / "P8_Y5_R10_1438_SOURCE_PACK_FILE_SCHEMA.csv"
LOCAL_DIRECTORY_AUDIT = OUT / "P8_Y5_R10_1438_LOCAL_INTAKE_DIRECTORY_AUDIT.csv"
RUNNER_DRYRUN_STATUS = OUT / "P8_Y5_R10_1438_SOURCE_PACK_RUNNER_DRYRUN_STATUS.csv"
PROMOTION_GATES = OUT / "P8_Y5_R10_1438_PROMOTION_GATES.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1438_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1438_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1438_VALIDATION.csv"

BRANCH_C_PARENT_ATTEMPT = COEFFICIENT_ROOT / "C_parent_WEP_slot_zero_attempt.csv"
BRANCH_SOURCE_PACK_MANIFEST = RESIDUAL_ROOT / "official_microscope_source_pack_manifest.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").replace("\r", " ").strip()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows supplied for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: clean(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def text_has(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="ignore")


def md_cell(value: Any) -> str:
    return clean(value).replace("|", "\\|")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


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


def branch_id() -> str:
    rows = read_csv(BRANCH_ID_FILE)
    if len(rows) != 1:
        raise ValueError(f"expected one branch row, got {len(rows)}")
    value = rows[0].get("same_parent_branch_id", "").strip()
    if not value:
        raise ValueError("same_parent_branch_id missing")
    return value


def file_count(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for item in path.rglob("*") if item.is_file())


def source_register_rows(branch: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC1438_0_1437_next", NEXT_1437, "NEXT1437_0_1438", "1437 handoff selecting WEP-slot C_parent/source-pack fork."),
        ("SRC1438_1_1437_validation", VALIDATION_1437, "VAL1437_10_overall", "1437 validation summary."),
        ("SRC1438_2_1437_readiness", READINESS_1437, "IRA1437_0_C_parent", "1437 readiness audit."),
        ("SRC1438_3_1437_acquisition", ACQUISITION_1437, "ACQ1437_0_C_parent", "1437 source acquisition ledger."),
        ("SRC1438_4_1437_bound_sep", BOUND_SEPARATION_1437, "BPS1437_1_projection_missing", "1437 bound/projection separation."),
        ("SRC1438_5_branch_id", BRANCH_ID_FILE, branch, "active branch lock."),
        ("SRC1438_6_c_parent", C_PARENT_FILE, "CP1430_6_verdict", "current C_parent placeholder/refusal rows."),
        ("SRC1438_7_c_parent_schema", C_PARENT_IMPORT_SCHEMA, "C_PARENT_IMPORT_SCHEMA_1431", "C_parent import schema."),
        ("SRC1438_8_wep_attempt_1437", WEP_ROW_ATTEMPT_1437, "PWA1437_0_first_row", "branch WEP row attempt."),
        ("SRC1438_9_wep_acq_1437", WEP_ACQUISITION_1437, "ACQ1437_0_C_parent", "branch WEP acquisition ledger."),
        ("SRC1438_10_eta_guard", ETA_PRODUCT_CONVENTION, "tau_eff = branch_locked_orbit_average", "eta product guard."),
        ("SRC1438_11_g_guard", MEASURED_G_GUARD, "MGG1429_0_no_relative_absorption", "measured-G guard."),
        ("SRC1438_12_1336_local_audit", LOCAL_AUDIT_1336, "LOCAL1336_6_official_readout", "MICROSCOPE intake directory audit."),
        ("SRC1438_13_1336_readout_schema", READOUT_SCHEMA_1336, "READSCHEMA1336_11_source_url_or_path", "official readout schema."),
        ("SRC1438_14_1336_source_schema", SOURCE_SCHEMA_1336, "SRCSCHEMA1336_6_source_url_or_path", "source worldtube schema."),
        ("SRC1438_15_1336_product_schema", PRODUCT_SCHEMA_1336, "PRODSCHEMA1336_6_branch_lock", "product convention schema."),
        ("SRC1438_16_1336_branch_schema", BRANCH_SCHEMA_1336, "BRANCHSCHEMA1336_1_forbidden_mixing_rule", "branch classifier schema."),
        ("SRC1438_17_1336_web_sources", WEB_SOURCES_1336, "WEB1336_1_CMSM_MICROSCOPE_portal", "official web source strings."),
        ("SRC1438_18_1336_validation", VALIDATION_1336, "VAL1336_11_overall", "1336 validation summary."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, anchor, role in specs:
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "anchor": anchor,
                "anchor_found": text_has(path, anchor),
                "role": role,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def c_parent_zero_attempt_rows(branch: str) -> list[dict[str, Any]]:
    clauses = [
        (
            "CZ1438_0_define_slot",
            "define WEP-slot C_parent as derivative of parent matter/source coupling along the Ti/Pt differential trace/material direction",
            "DEFINED_SYMBOLICALLY",
            "the slot can be named, but not evaluated",
        ),
        (
            "CZ1438_1_matter_descent",
            "ordinary matter action descends only through one observed coframe/common metric with no species-dependent parent response",
            "UNSIGNED",
            "1432/1437 leave matter descent and species/material response incomplete",
        ),
        (
            "CZ1438_2_source_common_mode",
            "Earth/source coupling enters only as common-mode acceleration absorbable into shared denominator, not relative Ti/Pt acceleration",
            "UNSIGNED",
            "measured-G guard forbids relative absorption; no zero theorem proves source is common-mode only",
        ),
        (
            "CZ1438_3_full_material_tensor",
            "full TA6V-minus-PtRh10 material tensor has zero projection in the active parent basis",
            "UNSIGNED",
            "existing rows are composition/DD-smoke only, not a full MTS parent tensor",
        ),
        (
            "CZ1438_4_no_readout_leak",
            "official readout/orbit kernel has no branch-specific relative projection after masking/averaging",
            "UNSIGNED",
            "official K_CMSM/readout arrays are absent",
        ),
        (
            "CZ1438_5_zero_certificate",
            "all above clauses combine into DERIVED_ZERO for C_parent WEP slot",
            "NOT_CLOSED",
            "no parent-signed certificate exists; C_parent cannot be promoted",
        ),
    ]
    return [
        {
            "same_parent_branch_id": branch,
            "clause_id": clause_id,
            "zero_condition": zero_condition,
            "status": status,
            "detail": detail,
            "slot_result": "C_PARENT_WEP_SLOT_NOT_ZERO_CERTIFIED",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for clause_id, zero_condition, status, detail in clauses
    ]


def c_parent_slot_status_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": branch,
            "slot_status_id": "CPS1438_0_WEP_C_parent",
            "slot": "C_parent_WEP_TiPt",
            "current_value": "MISSING_DERIVED_ZERO_OR_NUMERIC_SOURCE",
            "current_units": "MISSING_PARENT_BASIS_UNITS",
            "current_basis": "MISSING_MTS_PARENT_WEP_BASIS",
            "zero_certificate_status": "NOT_ZERO_CERTIFIED",
            "numeric_source_status": "NO_SOURCE_BACKED_NUMERIC_ROW",
            "runner_status": "BLOCKS_P_WEP_AND_LOCAL_GR_CLAIMS",
            "source_path": str(DOC),
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def source_pack_manifest_rows(branch: str) -> list[dict[str, Any]]:
    specs = [
        (
            "PACK1438_0_official_readout",
            "official_readout",
            MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout.csv",
            READOUT_SCHEMA_1336,
            "time_s;session_id;orbit_id;axis;gx_m_s2;gz_m_s2;Sxx;Sxz;mask_flag;calibration_flag;attitude_quaternion_or_axis;source_url_or_path",
            "official MICROSCOPE export or reproducible design matrix",
            "MISSING_OFFICIAL_FILE",
        ),
        (
            "PACK1438_1_source_worldtube",
            "source_worldtube",
            MICROSCOPE / "source_worldtube" / "P_WEP_R_source_Earth_worldtube.csv",
            SOURCE_SCHEMA_1336,
            "time_s_or_orbit_phase;radius_m;density_kg_m3;source_component;kernel_weight;model_or_dataset;source_url_or_path",
            "source profile plus orbit/readout projection in same parent basis",
            "MISSING_SOURCE_WORLDTUBE_FILE",
        ),
        (
            "PACK1438_2_product_convention",
            "product_convention",
            MICROSCOPE / "product_convention" / "P_WEP_eta_product_convention.csv",
            PRODUCT_SCHEMA_1336,
            "eta_formula;sign_convention;tau_eff_definition;readout_kernel_units;source_kernel_units;orbit_average_rule;branch_lock",
            "official eta/sign/product convention matching final eta_TiPt channel",
            "MISSING_PRODUCT_CONVENTION_FILE",
        ),
        (
            "PACK1438_3_branch_classifier",
            "branch_classifier",
            MICROSCOPE / "branch_classifier" / "P_WEP_same_parent_branch_lock.csv",
            BRANCH_SCHEMA_1336,
            "same_parent_branch_id;forbidden_mixing_rule",
            "branch classifier proving all product factors share one parent branch",
            "MISSING_PARENT_BRANCH_CLASSIFIER_FILE",
        ),
        (
            "PACK1438_4_material_tensor",
            "derived",
            MICROSCOPE / "derived" / "P_WEP_R_material_TA6V_minus_PtRh10_full_tensor.csv",
            OUT / "P8_Y5_R10_1438_SOURCE_PACK_FILE_SCHEMA.csv",
            "material_id;channel_id;response_value;units;basis;double_count_rule;source_url_or_path;valid_for_claim",
            "source-backed full material tensor derived from official composition plus parent-basis response model",
            "MISSING_FULL_MATERIAL_TENSOR_FILE",
        ),
        (
            "PACK1438_5_C_parent_import",
            "branch_locked_wep_coefficients",
            COEFFICIENT_ROOT / "C_parent_WEP_slot_import.csv",
            C_PARENT_IMPORT_SCHEMA,
            "same_parent_branch_id;component;value;uncertainty;units;sign_convention;basis;source_path;parent_status;zero_certificate_status",
            "DERIVED_ZERO or source-backed numeric C_parent WEP slot",
            "MISSING_C_PARENT_IMPORT_FILE",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for manifest_id, pack_item, target_path, schema_path, required_columns, provenance_requirement, missing_status in specs:
        rows.append(
            {
                "same_parent_branch_id": branch,
                "manifest_id": manifest_id,
                "pack_item": pack_item,
                "target_path": str(target_path),
                "target_exists": target_path.exists(),
                "target_parent_dir_exists": target_path.parent.exists(),
                "schema_path": str(schema_path),
                "schema_exists": schema_path.exists() or schema_path == SOURCE_PACK_FILE_SCHEMA,
                "required_columns_or_fields": required_columns,
                "provenance_requirement": provenance_requirement,
                "current_status": missing_status,
                "promotion_condition": "target file exists, parses, declares same_parent_branch_id, has no MISSING/PENDING placeholders, and cites source path/URL/DOI",
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def source_pack_file_schema_rows(branch: str) -> list[dict[str, Any]]:
    schema = [
        ("material_id", "string", "TA6V, PtRh10, or TA6V_minus_PtRh10 row id"),
        ("channel_id", "string", "parent-basis material/source channel"),
        ("response_value", "float_or_DERIVED_ZERO", "numeric response or theorem-zero tag"),
        ("uncertainty", "float_or_exact", "uncertainty or exact-theorem tag"),
        ("units", "string", "declared SI/natural unit conversion"),
        ("basis", "string", "must match C_parent and R_source basis"),
        ("double_count_rule", "string", "prevents overlap of mass, EM, nuclear, and binding channels"),
        ("source_url_or_path", "path_or_url_or_doi", "source-backed provenance"),
        ("same_parent_branch_id", "string", "must match active branch id"),
        ("valid_for_claim", "boolean", "false until all promotion gates pass"),
        ("claim_allowed", "boolean", "false until full WEP scorepack passes"),
    ]
    return [
        {
            "same_parent_branch_id": branch,
            "schema_id": f"SFS1438_{index}",
            "field": field,
            "type": field_type,
            "rule": rule,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for index, (field, field_type, rule) in enumerate(schema)
    ]


def local_directory_audit_rows(branch: str) -> list[dict[str, Any]]:
    dirs = [
        ("DIR1438_0_raw", MICROSCOPE / "raw", "raw incoming files"),
        ("DIR1438_1_docs", MICROSCOPE / "docs", "downloaded official docs/manuals"),
        ("DIR1438_2_official_readout", MICROSCOPE / "official_readout", "official readout/design matrix arrays"),
        ("DIR1438_3_source_worldtube", MICROSCOPE / "source_worldtube", "Earth/source profile and orbit weighting rows"),
        ("DIR1438_4_product_convention", MICROSCOPE / "product_convention", "eta/sign/product convention files"),
        ("DIR1438_5_branch_classifier", MICROSCOPE / "branch_classifier", "same-parent branch classifier rows"),
        ("DIR1438_6_derived", MICROSCOPE / "derived", "reproducible derived files such as material tensors"),
        ("DIR1438_7_metadata", MICROSCOPE / "metadata", "schemas and validation ledgers"),
    ]
    rows: list[dict[str, Any]] = []
    for audit_id, path, purpose in dirs:
        count = file_count(path)
        rows.append(
            {
                "same_parent_branch_id": branch,
                "audit_id": audit_id,
                "absolute_path": str(path),
                "purpose": purpose,
                "exists": path.exists(),
                "file_count": count,
                "usable_for_claim_now": False,
                "status": "DIRECTORY_READY_FILES_PENDING" if count == 0 and path.name != "metadata" else "METADATA_ONLY_OR_NONCLAIM",
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def runner_dryrun_rows(branch: str, manifest: list[dict[str, Any]], zero_attempt: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_targets = [row["manifest_id"] for row in manifest if row["target_exists"] is False]
    unsigned_clauses = [row["clause_id"] for row in zero_attempt if row["status"] in {"UNSIGNED", "NOT_CLOSED"}]
    return [
        {
            "same_parent_branch_id": branch,
            "runner_id": "RUN1438_0_C_parent_zero",
            "dryrun_result": "REFUSED_ZERO_NOT_CERTIFIED",
            "detail": ";".join(unsigned_clauses),
            "next_action": "derive minimal WEP-slot parent clause or import valid C_parent_WEP_slot row",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": branch,
            "runner_id": "RUN1438_1_source_pack",
            "dryrun_result": "REFUSED_OFFICIAL_FILES_MISSING",
            "detail": ";".join(missing_targets),
            "next_action": "populate official/source/derived files matching manifest schemas before score",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def promotion_gate_rows(branch: str) -> list[dict[str, Any]]:
    gates = [
        ("GATE1438_0_zero_certificate", "C_parent_WEP must be DERIVED_ZERO by parent theorem or source-backed numeric; placeholder rows fail."),
        ("GATE1438_1_same_basis", "C_parent, R_source, R_material, K_CMSM, and eta convention must share the same branch/basis."),
        ("GATE1438_2_official_readout", "official or reproducibly derived MICROSCOPE readout/design matrix must be present."),
        ("GATE1438_3_source_worldtube", "Earth/source worldtube vector must exist in the same parent basis."),
        ("GATE1438_4_full_material_tensor", "full material tensor must replace composition-only and DD-smoke rows."),
        ("GATE1438_5_product_sign", "eta formula, body order, sensitive axis, units, and orbit average must be explicit."),
        ("GATE1438_6_no_shortcuts", "no tau_eff=1, no measured-G relative absorption, no bound-as-prediction substitution."),
    ]
    return [
        {
            "same_parent_branch_id": branch,
            "gate_id": gate_id,
            "gate": gate,
            "gate_status": "LOCKED_CLAIM_FALSE",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate in gates
    ]


def decision_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": branch,
            "decision_id": "DEC1438_0_zero_route_not_closed",
            "decision": "do not close C_parent_WEP as zero",
            "why": "the required matter descent, common-mode source, full material tensor, and readout-silence clauses are unsigned",
            "consequence": "C_parent_WEP remains missing and blocks WEP/local-GR claims",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": branch,
            "decision_id": "DEC1438_1_source_pack_executable",
            "decision": "activate official MICROSCOPE source-pack manifest as executable intake contract",
            "why": "if the zero theorem does not close, the only honest route is a same-basis empirical projection pack",
            "consequence": "next work can dry-run exact file schemas without scoring",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1438_0_1439",
            "next_target": "1439-Y5-R10-RAB-minimal-WEP-slot-parent-clause-or-source-pack-parser-dry-run.md",
            "script": "scripts/Y5_R10_RAB_minimal_WEP_slot_parent_clause_or_source_pack_parser_dry_run.py",
            "objective": "try to state the minimal parent-action clause that would force C_parent_WEP=0; in parallel, dry-run the official MICROSCOPE source-pack parser against the manifest and keep all missing-file refusals explicit.",
            "include": "minimal parent clause; countermodel if clause too strong; parser dry-run; no-shortcut guards",
            "exclude": "numeric WEP score; local-GR claim; placeholder promotion; formalization edits; GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def write_branch_files(zero_attempt: list[dict[str, Any]], manifest: list[dict[str, Any]]) -> None:
    write_csv(BRANCH_C_PARENT_ATTEMPT, zero_attempt)
    write_csv(BRANCH_SOURCE_PACK_MANIFEST, manifest)


def validation_rows(
    sources: list[dict[str, Any]],
    zero_attempt: list[dict[str, Any]],
    slot_status: list[dict[str, Any]],
    manifest: list[dict[str, Any]],
    directory_audit: list[dict[str, Any]],
    dryrun: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    csvs = [
        SOURCE_REGISTER,
        C_PARENT_ZERO_ATTEMPT,
        C_PARENT_SLOT_STATUS,
        OFFICIAL_SOURCE_PACK_MANIFEST,
        SOURCE_PACK_FILE_SCHEMA,
        LOCAL_DIRECTORY_AUDIT,
        RUNNER_DRYRUN_STATUS,
        PROMOTION_GATES,
        DECISION_LEDGER,
        NEXT_TARGET,
        BRANCH_C_PARENT_ATTEMPT,
        BRANCH_SOURCE_PACK_MANIFEST,
    ]
    parse_ok = True
    parse_errors: list[str] = []
    truthy_claim_flags: list[str] = []
    for path in csvs:
        try:
            parsed_rows = read_csv(path)
        except Exception as exc:
            parse_ok = False
            parse_errors.append(f"{path.name}:{type(exc).__name__}")
            continue
        for index, row in enumerate(parsed_rows, start=2):
            for key in ("claim_allowed", "valid_for_claim", "valid_prediction_row"):
                if (row.get(key) or "").strip().lower() == "true":
                    truthy_claim_flags.append(f"{path.name}:{index}:{key}=true")
    sources_ok = all(row["path_exists"] and row["anchor_found"] for row in sources)
    zero_not_closed = any(row["status"] == "NOT_CLOSED" for row in zero_attempt) and all(
        row["slot_result"] == "C_PARENT_WEP_SLOT_NOT_ZERO_CERTIFIED" for row in zero_attempt
    )
    slot_blocks = len(slot_status) == 1 and slot_status[0]["runner_status"] == "BLOCKS_P_WEP_AND_LOCAL_GR_CLAIMS"
    manifest_executable = all(row["target_parent_dir_exists"] and row["schema_exists"] for row in manifest)
    manifest_refuses = all(row["target_exists"] is False for row in manifest)
    dirs_ready = all(row["exists"] for row in directory_audit)
    dryrun_refuses = all(row["dryrun_result"].startswith("REFUSED") for row in dryrun)
    gates_safe = all(row["gate_status"] == "LOCKED_CLAIM_FALSE" for row in gates) and not truthy_claim_flags
    branch_files_ok = BRANCH_C_PARENT_ATTEMPT.exists() and BRANCH_SOURCE_PACK_MANIFEST.exists()
    formalization_count = count_formalization_modified_since_start()
    checks = [
        ("VAL1438_0_source_register", sources_ok, "all 1438 cited source paths and anchors resolve"),
        ("VAL1438_1_zero_not_closed", zero_not_closed, "C_parent_WEP zero attempt is explicit and not closed"),
        ("VAL1438_2_slot_blocks", slot_blocks, "C_parent_WEP slot remains missing and blocks claims"),
        ("VAL1438_3_manifest_executable", manifest_executable, "manifest target directories and schemas exist"),
        ("VAL1438_4_manifest_refuses_missing_files", manifest_refuses, "manifest target files are absent and therefore refuse scoring"),
        ("VAL1438_5_dirs_ready", dirs_ready, "MICROSCOPE intake directories exist"),
        ("VAL1438_6_dryrun_refuses", dryrun_refuses, "zero and source-pack dry-runs refuse claim scoring"),
        ("VAL1438_7_claim_gates", gates_safe, "all claim/valid/prediction flags remain false"),
        ("VAL1438_8_csv_parse", parse_ok, "all generated 1438 CSVs parse cleanly" if parse_ok else ";".join(parse_errors)),
        ("VAL1438_9_branch_files", branch_files_ok, "branch-locked C_parent attempt and source-pack manifest written"),
        ("VAL1438_10_formalization_untouched", formalization_count == 0, f"formalization modified-file count since start={formalization_count}"),
        ("VAL1438_11_next_target", True, "1439 handoff written"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "generated_utc": stamp(),
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1438_12_overall",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1438 leaves C_parent_WEP unclosed and activates the official MICROSCOPE source-pack manifest without claims",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(sections: dict[str, list[dict[str, Any]]]) -> None:
    content = "\n\n".join(
        [
            "# 1438 - WEP-slot C_parent zero or official source-pack intake",
            "**Current verdict:** `C_parent_WEP` is not zero-certified. The source-pack route is now executable as a manifest, but every target file is still absent, so no WEP/local-GR claim is allowed.",
            "**Main progress:** the fork is now explicit: either derive a minimal parent-action clause forcing the WEP slot to zero, or import official/same-basis MICROSCOPE readout, source-worldtube, material-tensor, product, branch, and coefficient rows.",
            "## Source register\n" + md_table(sections["sources"]),
            "## C_parent WEP-slot zero attempt\n" + md_table(sections["zero_attempt"]),
            "## C_parent WEP-slot status\n" + md_table(sections["slot_status"]),
            "## Official MICROSCOPE source-pack manifest\n" + md_table(sections["manifest"]),
            "## Source-pack file schema\n" + md_table(sections["file_schema"]),
            "## Local intake directory audit\n" + md_table(sections["directory_audit"]),
            "## Runner dry-run status\n" + md_table(sections["dryrun"]),
            "## Promotion gates\n" + md_table(sections["gates"]),
            "## Decision ledger\n" + md_table(sections["decisions"]),
            "## Validation\n" + md_table(sections["validation"]),
            "## Next target\n" + md_table(sections["next"]),
        ]
    )
    DOC.write_text(content + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    COEFFICIENT_ROOT.mkdir(parents=True, exist_ok=True)
    RESIDUAL_ROOT.mkdir(parents=True, exist_ok=True)
    branch = branch_id()
    sources = source_register_rows(branch)
    zero_attempt = c_parent_zero_attempt_rows(branch)
    slot_status = c_parent_slot_status_rows(branch)
    manifest = source_pack_manifest_rows(branch)
    file_schema = source_pack_file_schema_rows(branch)
    directory_audit = local_directory_audit_rows(branch)
    dryrun = runner_dryrun_rows(branch, manifest, zero_attempt)
    gates = promotion_gate_rows(branch)
    decisions = decision_rows(branch)
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(C_PARENT_ZERO_ATTEMPT, zero_attempt)
    write_csv(C_PARENT_SLOT_STATUS, slot_status)
    write_csv(OFFICIAL_SOURCE_PACK_MANIFEST, manifest)
    write_csv(SOURCE_PACK_FILE_SCHEMA, file_schema)
    write_csv(LOCAL_DIRECTORY_AUDIT, directory_audit)
    write_csv(RUNNER_DRYRUN_STATUS, dryrun)
    write_csv(PROMOTION_GATES, gates)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)
    write_branch_files(zero_attempt, manifest)

    validation = validation_rows(sources, zero_attempt, slot_status, manifest, directory_audit, dryrun, gates)
    write_csv(VALIDATION, validation)
    write_doc(
        {
            "sources": sources,
            "zero_attempt": zero_attempt,
            "slot_status": slot_status,
            "manifest": manifest,
            "file_schema": file_schema,
            "directory_audit": directory_audit,
            "dryrun": dryrun,
            "gates": gates,
            "decisions": decisions,
            "validation": validation,
            "next": next_rows,
        }
    )
    remove_pycache()
    print("Y5_R10_1438_C_parent_WEP_not_zero_certified_source_pack_manifest_executable_nonclaim")


if __name__ == "__main__":
    main()
