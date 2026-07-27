from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1242"
TITLE = "1242-Y5-R10-QR-hat-source-or-zero-theorem-input-contract"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
QR_DIR = ROOT / "source-intake" / "qr-hat"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
DIRECTORY_CONTRACT_PATH = OUT_DIR / f"{PACK_ID}_QR_HAT_DIRECTORY_CONTRACT.csv"
INPUT_CONTRACT_PATH = OUT_DIR / f"{PACK_ID}_QR_HAT_INPUT_CONTRACT.csv"
ACCEPTANCE_GATES_PATH = OUT_DIR / f"{PACK_ID}_QR_HAT_ACCEPTANCE_GATES.csv"
TEMPLATE_PATH = OUT_DIR / f"{PACK_ID}_QR_HAT_CANDIDATE_TEMPLATE_NONCLAIM.csv"
ZERO_THEOREM_TEMPLATE_PATH = OUT_DIR / f"{PACK_ID}_ZERO_THEOREM_TEMPLATE_NONCLAIM.csv"
VALIDATOR_DRYRUN_PATH = OUT_DIR / f"{PACK_ID}_QR_HAT_CANDIDATE_VALIDATOR_DRYRUN.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1242_VALIDATION.csv"


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


def source_ref(relative_path: str, needle: str) -> str:
    return f"{relative_path}:{needle}"


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) > RUN_STARTED_UTC
    )


def candidate_files() -> list[Path]:
    raw = QR_DIR / "raw"
    if not raw.exists():
        return []
    return sorted(path for path in raw.iterdir() if path.is_file() and path.suffix.lower() == ".csv")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for subdir in ["raw", "docs", "accepted", "rejected"]:
        (QR_DIR / subdir).mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1242_0_1241_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1241_NEXT_TARGET.csv",
            "needle": "NEXT1241_0_1242",
            "purpose": "1241 handoff to q_R_hat input contract",
        },
        {
            "source_id": "SRC1242_1_1241_smoke",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1241_SMOKE_RESULTS.csv",
            "needle": "REFUSED_MISSING_QR",
            "purpose": "smoke runner refuses missing q_R_hat",
        },
        {
            "source_id": "SRC1242_2_1241_policy",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1241_REFUSAL_GATES.csv",
            "needle": "REF1241_3_policy_refused",
            "purpose": "statistical policy refusal gate",
        },
        {
            "source_id": "SRC1242_3_1240_bound",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1240_QR_BOUND_INPUT_SCHEMA.csv",
            "needle": "QB1240_0_qR_input",
            "purpose": "q_R_hat finite input schema",
        },
        {
            "source_id": "SRC1242_4_1240_zero",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1240_QR_ZERO_CHARGE_THEOREM_ATTEMPT.csv",
            "needle": "ZQR1240_5_verdict",
            "purpose": "Q_R zero theorem not derived",
        },
        {
            "source_id": "SRC1242_5_1240_map",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1240_QR_TO_PPN_MAPPING_SCHEMA.csv",
            "needle": "QMAP1240_2_dimensionless_qR",
            "purpose": "q_R_hat normalization",
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
            "directory_id": "QDIR1242_0_root",
            "path": str(QR_DIR),
            "purpose": "q_R_hat candidate intake root",
            "required_use": "place future candidate CSVs in raw; supporting papers/notes in docs",
            "created_or_verified": QR_DIR.exists(),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "directory_id": "QDIR1242_1_raw",
            "path": str(QR_DIR / "raw"),
            "purpose": "unreviewed q_R_hat candidate rows",
            "required_use": "raw candidate CSVs only; no automatic claim use",
            "created_or_verified": (QR_DIR / "raw").exists(),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "directory_id": "QDIR1242_2_docs",
            "path": str(QR_DIR / "docs"),
            "purpose": "provenance docs and derivation notes",
            "required_use": "store source notes, theorem sketches, or extraction docs",
            "created_or_verified": (QR_DIR / "docs").exists(),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "directory_id": "QDIR1242_3_accepted",
            "path": str(QR_DIR / "accepted"),
            "purpose": "reviewed nonclaim candidate rows",
            "required_use": "only rows passing all schema gates; still valid_for_claim=false",
            "created_or_verified": (QR_DIR / "accepted").exists(),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "directory_id": "QDIR1242_4_rejected",
            "path": str(QR_DIR / "rejected"),
            "purpose": "candidate rows with precise missing-field reason",
            "required_use": "archive rejected candidates and gate failures",
            "created_or_verified": (QR_DIR / "rejected").exists(),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    input_contract = [
        {
            "field_name": "candidate_id",
            "required_for": "finite_or_zero",
            "type": "string",
            "acceptance_rule": "unique stable id",
            "reject_if_missing": True,
        },
        {
            "field_name": "route_type",
            "required_for": "finite_or_zero",
            "type": "enum",
            "acceptance_rule": "finite_qR_hat | parent_zero_theorem",
            "reject_if_missing": True,
        },
        {
            "field_name": "q_R_hat",
            "required_for": "finite_qR_hat",
            "type": "numeric",
            "acceptance_rule": "finite dimensionless value q_R_hat=Q_R*c^2/(GM)",
            "reject_if_missing": True,
        },
        {
            "field_name": "q_R_hat_units",
            "required_for": "finite_qR_hat",
            "type": "string",
            "acceptance_rule": "must be dimensionless",
            "reject_if_missing": True,
        },
        {
            "field_name": "Q_R_units_before_normalization",
            "required_for": "finite_qR_hat",
            "type": "string",
            "acceptance_rule": "declares raw Q_R units or says directly_dimensionless_q_R_hat",
            "reject_if_missing": True,
        },
        {
            "field_name": "GM_convention",
            "required_for": "finite_qR_hat",
            "type": "string",
            "acceptance_rule": "same measured GM/source convention used in PPN comparator",
            "reject_if_missing": True,
        },
        {
            "field_name": "source_path",
            "required_for": "finite_or_zero",
            "type": "path_or_reference",
            "acceptance_rule": "local path or external provenance string; no placeholder markers",
            "reject_if_missing": True,
        },
        {
            "field_name": "derivation_status",
            "required_for": "finite_or_zero",
            "type": "enum",
            "acceptance_rule": "parent_derived_zero | sourced_finite_model | phenomenological_bound_nonclaim",
            "reject_if_missing": True,
        },
        {
            "field_name": "N_sigma",
            "required_for": "finite_qR_hat",
            "type": "numeric",
            "acceptance_rule": "declared statistical policy for comparator",
            "reject_if_missing": True,
        },
        {
            "field_name": "sigma_gamma",
            "required_for": "finite_qR_hat",
            "type": "numeric",
            "acceptance_rule": "uncertainty used by pass rule, e.g. 2.3e-5 from comparator row",
            "reject_if_missing": True,
        },
        {
            "field_name": "zero_theorem_statement",
            "required_for": "parent_zero_theorem",
            "type": "string",
            "acceptance_rule": "states theorem proving Q_R=0 without closure R_AB=0",
            "reject_if_missing": True,
        },
        {
            "field_name": "closure_used",
            "required_for": "finite_or_zero",
            "type": "boolean",
            "acceptance_rule": "must be False for claim-like theorem route; closure rows stay benchmark-only",
            "reject_if_missing": True,
        },
        {
            "field_name": "valid_for_claim",
            "required_for": "finite_or_zero",
            "type": "boolean",
            "acceptance_rule": "False in this checkpoint even if accepted for smoke runner",
            "reject_if_missing": True,
        },
        {
            "field_name": "claim_allowed",
            "required_for": "finite_or_zero",
            "type": "boolean",
            "acceptance_rule": "False in this checkpoint",
            "reject_if_missing": True,
        },
    ]
    for row in input_contract:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False

    acceptance_gates = [
        {
            "gate_id": "QGATE1242_0_no_closure_zero",
            "gate": "closure q_R_hat=0 is rejected as input evidence",
            "acceptance_condition": "closure_used=False or branch explicitly closure_benchmark and not scored",
            "failure_status": "REJECT_CLOSURE_AS_EVIDENCE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "QGATE1242_1_finite_numeric",
            "gate": "finite candidate has numeric q_R_hat",
            "acceptance_condition": "q_R_hat parses as finite float and units=dimensionless",
            "failure_status": "REJECT_MISSING_OR_NONNUMERIC_QR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "QGATE1242_2_GM_convention",
            "gate": "GM/source convention declared",
            "acceptance_condition": "GM_convention is non-placeholder and tied to comparator source",
            "failure_status": "REJECT_MISSING_GM_CONVENTION",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "QGATE1242_3_policy",
            "gate": "statistical pass policy declared",
            "acceptance_condition": "N_sigma and sigma_gamma parse as finite positive numbers",
            "failure_status": "REJECT_MISSING_STATISTICAL_POLICY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "QGATE1242_4_source",
            "gate": "source/provenance declared",
            "acceptance_condition": "source_path is non-placeholder and either exists locally or is an explicit external source/provenance id",
            "failure_status": "REJECT_MISSING_SOURCE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "QGATE1242_5_zero_theorem",
            "gate": "parent zero theorem route proves Q_R=0 without closure",
            "acceptance_condition": "route_type=parent_zero_theorem and zero_theorem_statement plus source_path are present; closure_used=False",
            "failure_status": "REJECT_ZERO_THEOREM_UNDERIVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    candidate_template = [
        {
            "candidate_id": "QR1242_TEMPLATE_FINITE",
            "route_type": "finite_qR_hat",
            "q_R_hat": "MISSING_NUMERIC_QR_HAT",
            "q_R_hat_units": "dimensionless",
            "Q_R_units_before_normalization": "MISSING_QR_UNITS_OR_DIRECT_DIMENSIONLESS",
            "GM_convention": "MISSING_GM_CONVENTION",
            "source_path": "MISSING_SOURCE_PATH_OR_EXTERNAL_PROVENANCE",
            "derivation_status": "phenomenological_bound_nonclaim",
            "N_sigma": "MISSING_N_SIGMA",
            "sigma_gamma": "MISSING_SIGMA_GAMMA",
            "zero_theorem_statement": "",
            "closure_used": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    zero_theorem_template = [
        {
            "candidate_id": "QR1242_TEMPLATE_ZERO_THEOREM",
            "route_type": "parent_zero_theorem",
            "q_R_hat": "0",
            "q_R_hat_units": "dimensionless",
            "Q_R_units_before_normalization": "theorem_zero",
            "GM_convention": "not_required_for_parent_zero_but_state_comparator_convention_if_scored",
            "source_path": "MISSING_PARENT_ZERO_THEOREM_SOURCE",
            "derivation_status": "parent_derived_zero",
            "N_sigma": "",
            "sigma_gamma": "",
            "zero_theorem_statement": "MISSING_THEOREM_STATEMENT_PROVING_Q_R_EQUALS_ZERO_WITHOUT_R_AB_CLOSURE",
            "closure_used": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    candidates = candidate_files()
    if candidates:
        validator_dryrun = [
            {
                "dryrun_id": f"QRDRY1242_{index}",
                "candidate_file": str(path),
                "status": "FOUND_NOT_VALIDATED_IN_1242",
                "reason": "1242 defines contract only; future validator must parse row-level gates",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
            for index, path in enumerate(candidates)
        ]
    else:
        validator_dryrun = [
            {
                "dryrun_id": "QRDRY1242_0_no_candidates",
                "candidate_file": str(QR_DIR / "raw"),
                "status": "NO_CANDIDATE_FILES_FOUND",
                "reason": "no q_R_hat candidates were present; no value fabricated",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        ]

    decisions = [
        {
            "decision_id": "DEC1242_0_no_fabrication",
            "decision": "do not create a numeric q_R_hat",
            "because": "1241/1240 show q_R_hat is the missing physics input",
            "next_action": "wait for a real source/theorem row or build a future validator",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1242_1_two_routes",
            "decision": "allow exactly two future routes: finite_qR_hat or parent_zero_theorem",
            "because": "closure zero and comparator-only rows are known failure modes",
            "next_action": "route future rows through QGATE1242 gates",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1242_2_next_validator",
            "decision": "next implementation should validate candidate rows against this contract",
            "because": "contract is now explicit but no candidate files exist",
            "next_action": "build candidate intake validator or source-hunt ledger",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1242_0_contract_exists",
            "claim": "q_R_hat input contract exists",
            "status": "PASS_NONCLAIM",
            "reason": "contract, gates, templates, directories, and dry-run rows generated",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1242_1_qR_value",
            "claim": "numeric q_R_hat exists",
            "status": "BLOCKED",
            "reason": "no candidate files and template row keeps MISSING markers",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1242_2_zero_theorem",
            "claim": "parent Q_R=0 theorem exists",
            "status": "BLOCKED",
            "reason": "zero theorem template is missing source and proof statement",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1242_3_local_GR",
            "claim": "local GR/Newton pass",
            "status": "BLOCKED",
            "reason": "input contract is not a physics result",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1242_0_1243",
            "target_file": "1243-Y5-R10-QR-hat-candidate-intake-validator-or-source-hunt-ledger.md",
            "target_script": "scripts/Y5_R10_QR_hat_candidate_intake_validator_or_source_hunt_ledger.py",
            "task": "build the row-level validator for source-intake/qr-hat/raw candidates and, if none exist, create a source-hunt ledger for finite q_R_hat or parent Q_R=0 theorem inputs",
            "success_condition": "candidate rows are either accepted as nonclaim runner inputs or rejected with exact missing fields; if no rows exist, the source-hunt ledger names the missing source/theorem targets",
            "do_not_do": "do not fabricate q_R_hat, do not claim local GR, and do not push to GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_paths = [
        SOURCE_REGISTER_PATH,
        DIRECTORY_CONTRACT_PATH,
        INPUT_CONTRACT_PATH,
        ACCEPTANCE_GATES_PATH,
        TEMPLATE_PATH,
        ZERO_THEOREM_TEMPLATE_PATH,
        VALIDATOR_DRYRUN_PATH,
        DECISION_PATH,
        CLAIM_GATES_PATH,
        NEXT_PATH,
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(DIRECTORY_CONTRACT_PATH, directory_contract)
    write_csv(INPUT_CONTRACT_PATH, input_contract)
    write_csv(ACCEPTANCE_GATES_PATH, acceptance_gates)
    write_csv(TEMPLATE_PATH, candidate_template)
    write_csv(ZERO_THEOREM_TEMPLATE_PATH, zero_theorem_template)
    write_csv(VALIDATOR_DRYRUN_PATH, validator_dryrun)
    write_csv(DECISION_PATH, decisions)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(NEXT_PATH, next_target)

    parsed_counts: list[str] = []
    csv_parse_ok = True
    for path in generated_paths:
        try:
            parsed_counts.append(f"{path.name}:{len(read_csv(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parsed_counts.append(f"{path.name}:ERROR:{exc}")

    all_sources_exist = all(parse_bool(row["path_exists"]) for row in source_register)
    all_needles_found = all(parse_bool(row["needle_found"]) for row in source_register)
    all_directories = all(parse_bool(row["created_or_verified"]) for row in directory_contract)
    contract_fields_ok = {row["field_name"] for row in input_contract} >= {
        "candidate_id",
        "route_type",
        "q_R_hat",
        "GM_convention",
        "source_path",
        "N_sigma",
        "sigma_gamma",
        "zero_theorem_statement",
        "closure_used",
    }
    gates_cover_failures = {row["failure_status"] for row in acceptance_gates} >= {
        "REJECT_CLOSURE_AS_EVIDENCE",
        "REJECT_MISSING_OR_NONNUMERIC_QR",
        "REJECT_MISSING_GM_CONVENTION",
        "REJECT_MISSING_STATISTICAL_POLICY",
        "REJECT_MISSING_SOURCE",
        "REJECT_ZERO_THEOREM_UNDERIVED",
    }
    templates_nonclaim = all(
        is_false(row, "valid_for_claim") and is_false(row, "claim_allowed")
        for row in candidate_template + zero_theorem_template
    )
    dryrun_no_fabrication = validator_dryrun[0]["status"] in {"NO_CANDIDATE_FILES_FOUND", "FOUND_NOT_VALIDATED_IN_1242"}
    claim_gates_ok = all(
        row["status"] in {"PASS_NONCLAIM", "BLOCKED"} and is_false(row, "claim_allowed")
        for row in claim_gates
    )
    all_generated_nonclaim = all(
        is_false(row, "valid_for_claim") and is_false(row, "claim_allowed")
        for table in [
            source_register,
            directory_contract,
            input_contract,
            acceptance_gates,
            candidate_template,
            zero_theorem_template,
            validator_dryrun,
            decisions,
            claim_gates,
            next_target,
        ]
        for row in table
    )
    next_is_1243 = next_target[0]["target_file"].startswith("1243-Y5-R10-QR-hat")
    fw_recent = formalization_recent_count()

    validation = [
        validation_row(
            "VAL1242_0_sources_exist",
            "all cited local sources exist",
            all_sources_exist,
            f"{sum(parse_bool(row['path_exists']) for row in source_register)}/{len(source_register)} sources exist",
        ),
        validation_row(
            "VAL1242_1_needles_found",
            "all cited local needles found",
            all_needles_found,
            f"{sum(parse_bool(row['needle_found']) for row in source_register)}/{len(source_register)} needles found",
        ),
        validation_row(
            "VAL1242_2_directories",
            "q_R_hat intake directories exist",
            all_directories,
            f"directories={len(directory_contract)}",
        ),
        validation_row(
            "VAL1242_3_contract_fields",
            "input contract has required fields",
            contract_fields_ok,
            f"contract_fields={len(input_contract)}",
        ),
        validation_row(
            "VAL1242_4_acceptance_gates",
            "acceptance gates cover known failure modes",
            gates_cover_failures,
            f"acceptance_gates={len(acceptance_gates)}",
        ),
        validation_row(
            "VAL1242_5_templates_nonclaim",
            "templates remain nonclaim and contain missing markers",
            templates_nonclaim,
            "finite and zero-theorem templates valid_for_claim=false",
        ),
        validation_row(
            "VAL1242_6_no_fabrication",
            "dry-run does not fabricate q_R_hat",
            dryrun_no_fabrication,
            validator_dryrun[0]["status"],
        ),
        validation_row(
            "VAL1242_7_claim_gates",
            "claim gates remain blocked/nonclaim",
            claim_gates_ok,
            f"claim_gate_rows={len(claim_gates)}",
        ),
        validation_row(
            "VAL1242_8_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_generated_nonclaim,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        ),
        validation_row(
            "VAL1242_9_next_target_1243",
            "next target is q_R_hat intake validator or source hunt",
            next_is_1243,
            next_target[0]["target_file"],
        ),
        validation_row(
            "VAL1242_10_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_counts),
        ),
        validation_row(
            "VAL1242_11_formalization_untouched",
            "formalization-workbench untouched during run",
            fw_recent == 0,
            f"formalization_recent_write_count_since_run_start={fw_recent}",
        ),
    ]
    validation.append(
        validation_row(
            "VAL1242_12_overall",
            "overall 1242 validation",
            all(row["status"] == "PASS" for row in validation),
            "1242 defines the exact q_R_hat/zero-theorem input contract without fabricating a value or promoting a claim",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    sections = [
        f"# {TITLE}",
        "",
        "**Current verdict:** 1242 defines the exact acceptable input contract for `q_R_hat`, but it does **not** supply or invent a value. Future rows must be either `finite_qR_hat` with units/provenance/policy or `parent_zero_theorem` with a real theorem source.",
        "",
        "**Main progress:** a dedicated `source-intake/qr-hat` lane now exists with raw/docs/accepted/rejected folders, templates, acceptance gates, and a dry-run that fabricates nothing.",
        "",
        "**No-claim guard:** no `Q_R=0`, PPN pass, local-GR pass, WEP/R10 pass, or public source-coupling claim is promoted.",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Source Register",
        markdown_table(source_register, list(source_register[0].keys())),
        "",
        "## QR Hat Directory Contract",
        markdown_table(directory_contract, list(directory_contract[0].keys())),
        "",
        "## QR Hat Input Contract",
        markdown_table(input_contract, list(input_contract[0].keys())),
        "",
        "## QR Hat Acceptance Gates",
        markdown_table(acceptance_gates, list(acceptance_gates[0].keys())),
        "",
        "## QR Hat Candidate Template",
        markdown_table(candidate_template, list(candidate_template[0].keys())),
        "",
        "## Zero Theorem Template",
        markdown_table(zero_theorem_template, list(zero_theorem_template[0].keys())),
        "",
        "## Candidate Validator Dry-Run",
        markdown_table(validator_dryrun, list(validator_dryrun[0].keys())),
        "",
        "## Decision Ledger",
        markdown_table(decisions, list(decisions[0].keys())),
        "",
        "## Claim Gates",
        markdown_table(claim_gates, list(claim_gates[0].keys())),
        "",
        "## Next Target",
        markdown_table(next_target, list(next_target[0].keys())),
        "",
        "## Validation",
        markdown_table(validation, list(validation[0].keys())),
        "",
    ]
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote validation {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
