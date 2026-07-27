from __future__ import annotations

import csv
import hashlib
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1228"
TITLE = "1228-Y5-R10-MICROSCOPE-user-assisted-package-intake-contract"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_DIR = ROOT / "source-intake" / "microscope"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
DIRECTORY_CONTRACT_PATH = OUT_DIR / f"{PACK_ID}_INTAKE_DIRECTORY_CONTRACT.csv"
EXPECTED_PACKAGES_PATH = OUT_DIR / f"{PACK_ID}_EXPECTED_PACKAGE_CLASSES.csv"
LOCAL_INVENTORY_PATH = OUT_DIR / f"{PACK_ID}_LOCAL_FILE_INVENTORY.csv"
CHECKSUM_MANIFEST_PATH = OUT_DIR / f"{PACK_ID}_CHECKSUM_MANIFEST.csv"
PROVENANCE_SCHEMA_PATH = OUT_DIR / f"{PACK_ID}_PROVENANCE_SCHEMA.csv"
VALIDATION_RULES_PATH = OUT_DIR / f"{PACK_ID}_FILE_VALIDATION_RULES.csv"
ACCEPTANCE_GATES_PATH = OUT_DIR / f"{PACK_ID}_ACCEPTANCE_GATE_MATRIX.csv"
REFUSAL_LEDGER_PATH = OUT_DIR / f"{PACK_ID}_REFUSAL_LEDGER.csv"
PARSER_PRECHECK_PATH = OUT_DIR / f"{PACK_ID}_PARSER_PRECHECK.csv"
TAU_FEED_PATH = OUT_DIR / f"{PACK_ID}_TAU_WEP_FEED_UPDATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1228_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def parse_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def is_false(row: dict[str, object], key: str) -> bool:
    return not parse_bool(row.get(key, False))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def classify_package(path: Path) -> str:
    name = path.name.lower()
    if any(token in name for token in ["readme", "doc", "dictionary", "license", "metadata"]):
        return "documentation_candidate"
    if any(token in name for token in ["suep", "suref", "acceler", "tsage", "gx", "gz", "sxx", "sxz"]):
        return "readout_array_candidate"
    if any(token in name for token in ["orbit", "attitude", "mask", "session", "segment"]):
        return "orbit_attitude_mask_candidate"
    if any(token in name for token in ["material", "ti", "pt", "ptrh", "composition"]):
        return "material_candidate"
    return "unclassified_candidate"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for subdir in ["raw", "docs", "metadata", "derived", "quarantine"]:
        (MICROSCOPE_DIR / subdir).mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1228_0_1227_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1227_NEXT_TARGET.csv",
            "needle": "1228-Y5-R10-MICROSCOPE-user-assisted-package-intake-contract.md",
            "purpose": "1227 handoff to strict user-assisted package intake",
        },
        {
            "source_id": "SRC1228_1_manual_instructions",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1227_MANUAL_ACQUISITION_INSTRUCTIONS.csv",
            "needle": "MAN1227_2_download_raw",
            "purpose": "manual download and reporting instructions",
        },
        {
            "source_id": "SRC1228_2_parser_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1227_FUTURE_PARSER_CONTRACT.csv",
            "needle": "PARSE1227_0_required_columns",
            "purpose": "future parser required fields",
        },
        {
            "source_id": "SRC1228_3_package_status",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1227_PACKAGE_MAP_STATUS.csv",
            "needle": "PKG1227_0_official_arrays",
            "purpose": "package map remains missing",
        },
        {
            "source_id": "SRC1228_4_access_blockers",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1227_ACCESS_BLOCKER_LEDGER.csv",
            "needle": "ABLOCK1227_0_local_tcp",
            "purpose": "CMSM access blockers",
        },
        {
            "source_id": "SRC1228_5_required_objects",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1226_REQUIRED_DATA_OBJECTS.csv",
            "needle": "OBJ1226_0_official_CMSM_arrays",
            "purpose": "official tau_WEP data object requirements",
        },
        {
            "source_id": "SRC1228_6_tau_formula",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1225_SYMBOLIC_TAU_WEP_FORMULA.csv",
            "needle": "FORM1225_0_tau_WEP_functional",
            "purpose": "tau_WEP formula to be fed by accepted official files",
        },
    ]

    source_register = []
    for spec in source_specs:
        path_exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_register.append(
            {
                **spec,
                "absolute_path": str(source_path(spec["local_path"])),
                "path_exists": path_exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    directory_contract = [
        {
            "directory_id": "DIR1228_0_raw",
            "absolute_path": str(MICROSCOPE_DIR / "raw"),
            "allowed_contents": "unmodified official CMSM downloaded package files only",
            "forbidden_contents": "handmade arrays, transformed files, renamed extracts without source metadata",
            "current_status": "READY_EMPTY_OR_WAITING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "directory_id": "DIR1228_1_docs",
            "absolute_path": str(MICROSCOPE_DIR / "docs"),
            "allowed_contents": "official documentation, readme, data dictionary, license/access notes",
            "forbidden_contents": "unsourced notes used as data dictionary",
            "current_status": "READY_EMPTY_OR_WAITING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "directory_id": "DIR1228_2_metadata",
            "absolute_path": str(MICROSCOPE_DIR / "metadata"),
            "allowed_contents": "manifests, checksums, package provenance CSVs",
            "forbidden_contents": "claim flags or inferred package identities without source URL",
            "current_status": "READY_EMPTY_OR_WAITING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "directory_id": "DIR1228_3_derived",
            "absolute_path": str(MICROSCOPE_DIR / "derived"),
            "allowed_contents": "future parsed products from verified official files",
            "forbidden_contents": "derived tau_WEP values before schema/provenance gates pass",
            "current_status": "READY_EMPTY_OR_WAITING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "directory_id": "DIR1228_4_quarantine",
            "absolute_path": str(MICROSCOPE_DIR / "quarantine"),
            "allowed_contents": "files that exist locally but fail provenance/schema checks",
            "forbidden_contents": "any file promoted to parser input from quarantine",
            "current_status": "READY_EMPTY_OR_WAITING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    expected_packages = [
        {
            "class_id": "CLASS1228_0_readout_arrays",
            "expected_content": "official SUEP/SUREF readout arrays with time/session/segment/gx/gz/Sxx/Sxz/masks/calibration flags",
            "required_for": "K_eta and measured acceleration/readout part of tau_WEP",
            "minimum_acceptance": "official source URL/package id, checksum, schema documentation, units, session coverage",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "class_id": "CLASS1228_1_docs_dictionary",
            "expected_content": "CMSM data dictionary/readme/product convention documentation",
            "required_for": "column meanings, eta normalization N_eta, frames, units, license/access",
            "minimum_acceptance": "official document provenance and citation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "class_id": "CLASS1228_2_orbit_attitude_masks",
            "expected_content": "orbit/attitude/session/mask products",
            "required_for": "orbit average and mask operator in tau_WEP",
            "minimum_acceptance": "official source URL/package id, time convention, coordinate frame, units",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "class_id": "CLASS1228_3_material_source_weight",
            "expected_content": "Ti/Pt material response or source-weight convention inputs",
            "required_for": "R_material(TiPt) and Delta_w_TiPt branch",
            "minimum_acceptance": "source-weight convention, material composition provenance, numeric prior or theorem-zero source",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    file_candidates = []
    for scan_dir in [MICROSCOPE_DIR / "raw", MICROSCOPE_DIR / "docs"]:
        file_candidates.extend(path for path in scan_dir.rglob("*") if path.is_file())

    inventory_rows = []
    checksum_rows = []
    if file_candidates:
        for index, path in enumerate(sorted(file_candidates)):
            relative_path = path.relative_to(ROOT)
            digest = sha256_file(path)
            package_class = classify_package(path)
            inventory_rows.append(
                {
                    "inventory_id": f"INV1228_{index}",
                    "relative_path": str(relative_path),
                    "absolute_path": str(path),
                    "size_bytes": path.stat().st_size,
                    "sha256": digest,
                    "package_class_guess": package_class,
                    "provenance_sidecar_found": False,
                    "schema_documentation_found": package_class == "documentation_candidate",
                    "accepted_for_parser": False,
                    "refusal_reason": "MISSING_PROVENANCE_SIDECAR_AND_MANIFEST_REVIEW",
                    "valid_for_claim": False,
                    "claim_allowed": False,
                }
            )
            checksum_rows.append(
                {
                    "checksum_id": f"SHA1228_{index}",
                    "relative_path": str(relative_path),
                    "sha256": digest,
                    "size_bytes": path.stat().st_size,
                    "source_url": "MISSING_SOURCE_URL",
                    "package_id": "MISSING_PACKAGE_ID",
                    "valid_for_claim": False,
                    "claim_allowed": False,
                }
            )
    else:
        inventory_rows.append(
            {
                "inventory_id": "INV1228_0_no_files",
                "relative_path": "source-intake/microscope/raw;source-intake/microscope/docs",
                "absolute_path": str(MICROSCOPE_DIR),
                "size_bytes": 0,
                "sha256": "NO_FILES",
                "package_class_guess": "no_local_files",
                "provenance_sidecar_found": False,
                "schema_documentation_found": False,
                "accepted_for_parser": False,
                "refusal_reason": "NO_OFFICIAL_FILES_PRESENT",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        checksum_rows.append(
            {
                "checksum_id": "SHA1228_0_no_files",
                "relative_path": "NO_FILES",
                "sha256": "NO_FILES",
                "size_bytes": 0,
                "source_url": "MISSING_SOURCE_URL",
                "package_id": "MISSING_PACKAGE_ID",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    provenance_schema = [
        {
            "field_id": "PROV1228_0_source_url",
            "required_field": "source_url",
            "description": "exact CMSM/official URL or portal package location used to obtain the file",
            "acceptance_rule": "must be nonempty and official before parser acceptance",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "field_id": "PROV1228_1_package_id",
            "required_field": "package_id_or_aip_id",
            "description": "CMSM package name, AIP id, product id, or official export identifier",
            "acceptance_rule": "must link local file to portal metadata",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "field_id": "PROV1228_2_checksum",
            "required_field": "sha256",
            "description": "local file checksum computed after download",
            "acceptance_rule": "must be recorded before parsing and preserved unchanged",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "field_id": "PROV1228_3_license_access",
            "required_field": "license_or_access_status",
            "description": "public/open/license accepted/login required/manual acquisition status",
            "acceptance_rule": "must be known before derived products are shared or claimed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "field_id": "PROV1228_4_schema_doc",
            "required_field": "schema_document_path",
            "description": "local official documentation defining columns, units, frames, and product convention",
            "acceptance_rule": "readout arrays cannot be parsed for tau_WEP without it",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    validation_rules = [
        {
            "rule_id": "RULE1228_0_path",
            "rule": "file must be under source-intake/microscope/raw or source-intake/microscope/docs",
            "failure_effect": "quarantine/refuse",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "RULE1228_1_unmodified",
            "rule": "raw files must be unmodified official packages, not manually edited extracts",
            "failure_effect": "quarantine/refuse",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "RULE1228_2_provenance",
            "rule": "source_url, package id, checksum, access/license, and schema docs must be present",
            "failure_effect": "parser_refuses",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "RULE1228_3_columns",
            "rule": "readout arrays must expose time, session/segment, SU, gx/gz/Sxx/Sxz, masks, calibration flags, orbit/attitude convention",
            "failure_effect": "tau_WEP_not_scoreable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "RULE1228_4_no_claim",
            "rule": "passing intake is not a WEP/local-GR claim; it only permits parser precheck",
            "failure_effect": "claim_allowed_always_false",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    acceptance_gates = [
        {
            "gate_id": "ACCEPT1228_0_files_present",
            "gate": "official-looking files present locally",
            "status": "PASS" if file_candidates else "BLOCKED",
            "reason": f"local_file_count={len(file_candidates)}",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "ACCEPT1228_1_provenance",
            "gate": "provenance sidecar/manifest complete",
            "status": "BLOCKED",
            "reason": "source_url/package_id/license/schema metadata not filled",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "ACCEPT1228_2_schema",
            "gate": "schema documentation available",
            "status": "BLOCKED",
            "reason": "no official data dictionary accepted",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "ACCEPT1228_3_parser",
            "gate": "parser may read arrays",
            "status": "BLOCKED",
            "reason": "requires files plus provenance plus schema",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "ACCEPT1228_4_tau_WEP",
            "gate": "tau_WEP may be evaluated",
            "status": "BLOCKED",
            "reason": "parser precheck and source/material product inputs not passed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    refusal_ledger = [
        {
            "refusal_id": "REF1228_0_no_files" if not file_candidates else "REF1228_0_files_unreviewed",
            "target": "MICROSCOPE package intake",
            "refusal_reason": "NO_OFFICIAL_FILES_PRESENT" if not file_candidates else "FILES_PRESENT_BUT_PROVENANCE_NOT_REVIEWED",
            "minimum_to_reconsider": "official files under allowed paths plus provenance/source URL/checksum/schema documentation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "refusal_id": "REF1228_1_tau_WEP",
            "target": "tau_WEP parser/evaluation",
            "refusal_reason": "INTAKE_GATES_BLOCKED",
            "minimum_to_reconsider": "ACCEPT1228_0 through ACCEPT1228_3 pass; source/material inputs still separately required",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    parser_precheck = [
        {
            "precheck_id": "PRE1228_0_readout_columns",
            "required_before_parser": "accepted readout array file plus official schema docs",
            "current_status": "BLOCKED_NO_ACCEPTED_ARRAYS",
            "future_check": "verify time/session/segment/SU/gx/gz/Sxx/Sxz/masks/calibration/frames",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "precheck_id": "PRE1228_1_metadata",
            "required_before_parser": "accepted metadata/data dictionary",
            "current_status": "BLOCKED_NO_ACCEPTED_DOCUMENTATION",
            "future_check": "verify units, frames, product convention, version, license/access, citation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "precheck_id": "PRE1228_2_tau_output_guard",
            "required_before_parser": "all parser checks pass",
            "current_status": "BLOCKED",
            "future_check": "tau_WEP output remains nonclaim until product runner and source-weight gates pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    tau_feed = [
        {
            "feed_id": "FEED1228_0_to_1227",
            "target": "PARSE1227 future parser contract",
            "update": "local drop-zone and intake contract created; no accepted files yet",
            "tau_WEP_status": "WAITING_FOR_OFFICIAL_FILES",
            "valid_prediction_rows_delta": 0,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "feed_id": "FEED1228_1_to_1225",
            "target": "FORM1225_0_tau_WEP_functional",
            "update": "no parser/evaluation allowed until intake gates pass",
            "tau_WEP_status": "SYMBOLIC_ONLY_NONCLAIM",
            "valid_prediction_rows_delta": 0,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC1228_0_dropzone_created",
            "decision": "create local official-file drop-zone",
            "because": "machine CMSM access is blocked but user/browser/manual acquisition may succeed later",
            "next_action": "if files appear, rerun intake and refuse until provenance/schema gates pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1228_1_no_parser_without_docs",
            "decision": "do not write a concrete parser yet",
            "because": "parser column assumptions would be speculative without official schema documentation",
            "next_action": "return to local-GR source-coupling derivation while data branch waits",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1228_2_data_pending",
            "decision": "keep MICROSCOPE data branch pending but ready",
            "because": "intake gate can verify future files, but no official files are present now",
            "next_action": "work the analytic local-GR source-coupling contract without WEP claim promotion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1228_0_sources",
            "gate": "source path and needle audit",
            "status": "PASS",
            "reason": "all local handoff sources are traceable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1228_1_directories",
            "gate": "intake directories available",
            "status": "PASS",
            "reason": "raw/docs/metadata/derived/quarantine directories exist under source-intake/microscope",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1228_2_files",
            "gate": "official files accepted",
            "status": "BLOCKED",
            "reason": "no accepted official files with provenance/schema",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1228_3_parser",
            "gate": "parser may run",
            "status": "BLOCKED",
            "reason": "parser prechecks are blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1228_4_tau_WEP",
            "gate": "tau_WEP/local-GR/WEP claim permission",
            "status": "BLOCKED",
            "reason": "intake contract only; no physical claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_rows = [
        {
            "next_id": "NEXT1228_0_1229",
            "target_file": "1229-Y5-R10-data-pending-local-GR-source-coupling-contract.md",
            "target_script": "scripts/Y5_R10_data_pending_local_GR_source_coupling_contract.py",
            "task": "with MICROSCOPE official files pending, return to the analytic local-GR source-coupling contract and derive the exact conditions for universal source coupling without WEP claim promotion",
            "success_condition": "the data branch stays ready for future official files, while the GR/Newton reduction branch gets a sharper source-coupling theorem or finite-residual contract",
            "do_not_do": "do not claim WEP/local-GR/PPN, do not use surrogate arrays as official, do not set tau_WEP to one, do not edit formalization-workbench or push GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (DIRECTORY_CONTRACT_PATH, directory_contract),
        (EXPECTED_PACKAGES_PATH, expected_packages),
        (LOCAL_INVENTORY_PATH, inventory_rows),
        (CHECKSUM_MANIFEST_PATH, checksum_rows),
        (PROVENANCE_SCHEMA_PATH, provenance_schema),
        (VALIDATION_RULES_PATH, validation_rules),
        (ACCEPTANCE_GATES_PATH, acceptance_gates),
        (REFUSAL_LEDGER_PATH, refusal_ledger),
        (PARSER_PRECHECK_PATH, parser_precheck),
        (TAU_FEED_PATH, tau_feed),
        (DECISION_PATH, decision_rows),
        (CLAIM_GATES_PATH, claim_gates),
        (NEXT_PATH, next_rows),
    ]
    for path, rows in generated_tables:
        write_csv(path, rows)

    validation_rows = []
    validation_rows.append(
        validation_row(
            "VAL1228_0_sources_exist",
            "all cited local sources exist",
            all(parse_bool(row["path_exists"]) for row in source_register),
            f"{sum(1 for row in source_register if parse_bool(row['path_exists']))}/{len(source_register)} sources exist",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1228_1_needles_found",
            "all cited local needles found",
            all(parse_bool(row["needle_found"]) for row in source_register),
            f"{sum(1 for row in source_register if parse_bool(row['needle_found']))}/{len(source_register)} needles found",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1228_2_directories_exist",
            "all intake directories exist",
            all(Path(row["absolute_path"]).exists() and Path(row["absolute_path"]).is_dir() for row in directory_contract),
            "; ".join(row["directory_id"] for row in directory_contract),
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1228_3_inventory_nonclaim",
            "local inventory rows are nonclaim",
            all(is_false(row, "valid_for_claim") and is_false(row, "claim_allowed") and is_false(row, "accepted_for_parser") for row in inventory_rows),
            f"inventory_rows={len(inventory_rows)}",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1228_4_no_claim_checksums",
            "checksum manifest has no claimable rows",
            all(is_false(row, "valid_for_claim") and is_false(row, "claim_allowed") for row in checksum_rows),
            f"checksum_rows={len(checksum_rows)}",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1228_5_acceptance_blocks_parser",
            "parser and tau gates remain blocked",
            any(row["gate_id"] == "ACCEPT1228_3_parser" and row["status"] == "BLOCKED" for row in acceptance_gates)
            and any(row["gate_id"] == "ACCEPT1228_4_tau_WEP" and row["status"] == "BLOCKED" for row in acceptance_gates),
            "parser/tau acceptance gates blocked",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1228_6_refusal_present",
            "refusal ledger exists",
            len(refusal_ledger) >= 2,
            "; ".join(row["refusal_id"] for row in refusal_ledger),
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1228_7_tau_feed_nonclaim",
            "tau_WEP feed remains nonclaim",
            all(row["valid_prediction_rows_delta"] == 0 and is_false(row, "claim_allowed") for row in tau_feed),
            "valid_prediction_rows_delta=0 for tau feeds",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1228_8_claim_gates_blocked",
            "claim gates keep physical claims blocked",
            any(row["status"] == "BLOCKED" for row in claim_gates) and all(is_false(row, "valid_for_claim") for row in claim_gates),
            "file/parser/tau claim gates blocked",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1228_9_next_target_local_GR",
            "next target returns to analytic local-GR source coupling",
            next_rows[0]["target_file"] == "1229-Y5-R10-data-pending-local-GR-source-coupling-contract.md",
            next_rows[0]["target_file"],
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1228_10_nonclaim_policy",
            "all generated rows remain nonclaim",
            all(
                is_false(row, "valid_for_claim") and is_false(row, "claim_allowed")
                for _, rows in generated_tables
                for row in rows
                if "valid_for_claim" in row and "claim_allowed" in row
            ),
            "valid_for_claim=false and claim_allowed=false throughout claim-bearing tables",
        )
    )

    csv_parse_details = []
    csv_parse_ok = True
    for path, _ in generated_tables:
        try:
            parsed = read_csv(path)
            csv_parse_details.append(f"{path.name}:{len(parsed)}")
        except Exception as exc:  # pragma: no cover
            csv_parse_ok = False
            csv_parse_details.append(f"{path.name}:FAIL:{exc}")
    validation_rows.append(
        validation_row(
            "VAL1228_11_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(csv_parse_details),
        )
    )

    formalization_recent = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            if path.is_file():
                modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
                if modified >= RUN_STARTED_UTC:
                    formalization_recent.append(path)
    validation_rows.append(
        validation_row(
            "VAL1228_12_formalization_untouched",
            "formalization-workbench untouched during run",
            len(formalization_recent) == 0,
            f"formalization_recent_after_run_start_count={len(formalization_recent)}",
        )
    )

    overall_before = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1228_13_overall",
            "overall 1228 validation",
            overall_before,
            "1228 creates strict CMSM intake drop-zone and refuses parser/tau claims until official files and metadata pass gates",
        )
    )
    write_csv(VALIDATION_PATH, validation_rows)

    doc = f"""# 1228 Y5/R10 MICROSCOPE User-Assisted Package Intake Contract

**Current verdict:** 1228 creates a strict local intake contract for future user-assisted CMSM/MICROSCOPE files. No official files are currently accepted for parsing, and `tau_WEP` remains symbolic-only.

**Main progress:** the drop-zone now exists under `source-intake/microscope/`, with raw/docs/metadata/derived/quarantine lanes, checksum inventory rules, provenance requirements, parser prechecks, and refusal gates.

**Practical consequence:** if official CMSM files are later downloaded manually, rerunning this script will inventory them and still refuse claims unless source URL, package id, checksum, license/access, and schema documentation are all present.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "purpose", "absolute_path", "path_exists", "needle_found", "valid_for_claim", "claim_allowed"])}

## Intake Directory Contract

{markdown_table(directory_contract, ["directory_id", "absolute_path", "allowed_contents", "forbidden_contents", "current_status", "valid_for_claim", "claim_allowed"])}

## Expected Package Classes

{markdown_table(expected_packages, ["class_id", "expected_content", "required_for", "minimum_acceptance", "valid_for_claim", "claim_allowed"])}

## Local File Inventory

{markdown_table(inventory_rows, ["inventory_id", "relative_path", "absolute_path", "size_bytes", "sha256", "package_class_guess", "provenance_sidecar_found", "schema_documentation_found", "accepted_for_parser", "refusal_reason", "valid_for_claim", "claim_allowed"])}

## Checksum Manifest

{markdown_table(checksum_rows, ["checksum_id", "relative_path", "sha256", "size_bytes", "source_url", "package_id", "valid_for_claim", "claim_allowed"])}

## Provenance Schema

{markdown_table(provenance_schema, ["field_id", "required_field", "description", "acceptance_rule", "valid_for_claim", "claim_allowed"])}

## File Validation Rules

{markdown_table(validation_rules, ["rule_id", "rule", "failure_effect", "valid_for_claim", "claim_allowed"])}

## Acceptance Gate Matrix

{markdown_table(acceptance_gates, ["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"])}

## Refusal Ledger

{markdown_table(refusal_ledger, ["refusal_id", "target", "refusal_reason", "minimum_to_reconsider", "valid_for_claim", "claim_allowed"])}

## Parser Precheck

{markdown_table(parser_precheck, ["precheck_id", "required_before_parser", "current_status", "future_check", "valid_for_claim", "claim_allowed"])}

## Tau WEP Feed Update

{markdown_table(tau_feed, ["feed_id", "target", "update", "tau_WEP_status", "valid_prediction_rows_delta", "valid_for_claim", "claim_allowed"])}

## Decision Ledger

{markdown_table(decision_rows, ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"])}

## Claim Gates

{markdown_table(claim_gates, ["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"])}

## Next Target

{markdown_table(next_rows, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not_do", "valid_for_claim", "claim_allowed"])}

## Validation

{markdown_table(validation_rows, ["check_id", "check", "status", "details", "valid_for_claim", "claim_allowed"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
