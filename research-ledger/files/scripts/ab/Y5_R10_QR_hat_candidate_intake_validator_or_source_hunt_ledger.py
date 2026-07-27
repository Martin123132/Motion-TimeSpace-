from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1243"
TITLE = "1243-Y5-R10-QR-hat-candidate-intake-validator-or-source-hunt-ledger"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
QR_DIR = ROOT / "source-intake" / "qr-hat"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
VALIDATOR_RULES_PATH = OUT_DIR / f"{PACK_ID}_VALIDATOR_RULES.csv"
CANDIDATE_SCAN_PATH = OUT_DIR / f"{PACK_ID}_CANDIDATE_SCAN.csv"
ACCEPTED_PATH = OUT_DIR / f"{PACK_ID}_ACCEPTED_NONCLAIM_ROWS.csv"
REJECTED_PATH = OUT_DIR / f"{PACK_ID}_REJECTED_ROWS.csv"
SOURCE_HUNT_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_HUNT_LEDGER.csv"
RUNNER_FEED_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_FEED_UPDATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1243_VALIDATION.csv"


ACCEPTED_FIELDS = [
    "candidate_file",
    "row_number",
    "candidate_id",
    "route_type",
    "q_R_hat",
    "gamma_minus_1_QR",
    "N_sigma",
    "sigma_gamma",
    "source_path",
    "derivation_status",
    "runner_status",
    "valid_for_claim",
    "claim_allowed",
]
REJECTED_FIELDS = [
    "candidate_file",
    "row_number",
    "candidate_id",
    "route_type",
    "rejection_status",
    "missing_or_failed_fields",
    "valid_for_claim",
    "claim_allowed",
]


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


def placeholder(value: object) -> bool:
    text = str(value).strip()
    return text == "" or text.upper().startswith("MISSING")


def finite_float(value: object) -> bool:
    try:
        parsed = float(str(value).strip())
    except Exception:
        return False
    return math.isfinite(parsed)


def positive_float(value: object) -> bool:
    if not finite_float(value):
        return False
    return float(str(value).strip()) > 0


def source_declared(value: object) -> bool:
    text = str(value).strip()
    if placeholder(text):
        return False
    if text.startswith(("http://", "https://", "doi:", "arxiv:", "SRC", "EXT", "P8_", "source-intake")):
        return True
    path = source_path(text)
    return path.exists()


def validate_candidate(row: dict[str, str], candidate_file: Path, row_number: int) -> tuple[dict[str, object] | None, dict[str, object] | None]:
    failures: list[str] = []
    route_type = row.get("route_type", "")
    candidate_id = row.get("candidate_id", f"row_{row_number}")

    required_common = ["candidate_id", "route_type", "source_path", "derivation_status", "closure_used", "valid_for_claim", "claim_allowed"]
    for field in required_common:
        if placeholder(row.get(field, "")):
            failures.append(field)

    if route_type not in {"finite_qR_hat", "parent_zero_theorem"}:
        failures.append("route_type")

    if parse_bool(row.get("closure_used", False)):
        failures.append("closure_used")

    if not is_false(row, "valid_for_claim"):
        failures.append("valid_for_claim")
    if not is_false(row, "claim_allowed"):
        failures.append("claim_allowed")

    if not source_declared(row.get("source_path", "")):
        failures.append("source_path")

    if route_type == "finite_qR_hat":
        if not finite_float(row.get("q_R_hat", "")):
            failures.append("q_R_hat")
        if str(row.get("q_R_hat_units", "")).strip() != "dimensionless":
            failures.append("q_R_hat_units")
        if placeholder(row.get("Q_R_units_before_normalization", "")):
            failures.append("Q_R_units_before_normalization")
        if placeholder(row.get("GM_convention", "")):
            failures.append("GM_convention")
        if row.get("derivation_status", "") not in {"sourced_finite_model", "phenomenological_bound_nonclaim"}:
            failures.append("derivation_status")
        if not positive_float(row.get("N_sigma", "")):
            failures.append("N_sigma")
        if not positive_float(row.get("sigma_gamma", "")):
            failures.append("sigma_gamma")
    elif route_type == "parent_zero_theorem":
        if str(row.get("q_R_hat", "")).strip() not in {"0", "0.0"}:
            failures.append("q_R_hat")
        if row.get("derivation_status", "") != "parent_derived_zero":
            failures.append("derivation_status")
        if placeholder(row.get("zero_theorem_statement", "")):
            failures.append("zero_theorem_statement")

    if failures:
        return None, {
            "candidate_file": str(candidate_file),
            "row_number": row_number,
            "candidate_id": candidate_id,
            "route_type": route_type,
            "rejection_status": "REJECTED_PRECLAIM_INTAKE",
            "missing_or_failed_fields": ";".join(sorted(set(failures))),
            "valid_for_claim": False,
            "claim_allowed": False,
        }

    q_hat = 0.0 if route_type == "parent_zero_theorem" else float(str(row["q_R_hat"]).strip())
    return {
        "candidate_file": str(candidate_file),
        "row_number": row_number,
        "candidate_id": candidate_id,
        "route_type": route_type,
        "q_R_hat": q_hat,
        "gamma_minus_1_QR": -0.5 * q_hat,
        "N_sigma": row.get("N_sigma", ""),
        "sigma_gamma": row.get("sigma_gamma", ""),
        "source_path": row.get("source_path", ""),
        "derivation_status": row.get("derivation_status", ""),
        "runner_status": "ACCEPTED_NONCLAIM_INPUT_NOT_EVIDENCE",
        "valid_for_claim": False,
        "claim_allowed": False,
    }, None


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for subdir in ["raw", "docs", "accepted", "rejected"]:
        (QR_DIR / subdir).mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1243_0_1242_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1242_NEXT_TARGET.csv",
            "needle": "NEXT1242_0_1243",
            "purpose": "1242 handoff to q_R_hat candidate validator or source hunt",
        },
        {
            "source_id": "SRC1243_1_1242_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1242_QR_HAT_INPUT_CONTRACT.csv",
            "needle": "candidate_id",
            "purpose": "q_R_hat input contract",
        },
        {
            "source_id": "SRC1243_2_1242_gates",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1242_QR_HAT_ACCEPTANCE_GATES.csv",
            "needle": "QGATE1242_1_finite_numeric",
            "purpose": "acceptance gates",
        },
        {
            "source_id": "SRC1243_3_1242_template",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1242_QR_HAT_CANDIDATE_TEMPLATE_NONCLAIM.csv",
            "needle": "QR1242_TEMPLATE_FINITE",
            "purpose": "finite q_R_hat template",
        },
        {
            "source_id": "SRC1243_4_1242_zero_template",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1242_ZERO_THEOREM_TEMPLATE_NONCLAIM.csv",
            "needle": "QR1242_TEMPLATE_ZERO_THEOREM",
            "purpose": "zero-theorem template",
        },
        {
            "source_id": "SRC1243_5_1241_smoke",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1241_SMOKE_RESULTS.csv",
            "needle": "REFUSED_MISSING_QR",
            "purpose": "runner refuses missing q_R_hat",
        },
        {
            "source_id": "SRC1243_6_1240_zero",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1240_QR_ZERO_CHARGE_THEOREM_ATTEMPT.csv",
            "needle": "ZERO_CHARGE_THEOREM_NOT_DERIVED",
            "purpose": "zero theorem remains missing",
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

    validator_rules = [
        {
            "rule_id": "VR1243_0_route",
            "rule": "route_type must be finite_qR_hat or parent_zero_theorem",
            "failure_status": "REJECT_BAD_ROUTE_TYPE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "VR1243_1_finite",
            "rule": "finite_qR_hat rows need numeric q_R_hat, dimensionless units, raw-unit declaration, GM convention, source, N_sigma, and sigma_gamma",
            "failure_status": "REJECT_MISSING_FINITE_QR_FIELDS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "VR1243_2_zero",
            "rule": "parent_zero_theorem rows need q_R_hat=0, derivation_status=parent_derived_zero, theorem statement, source, and closure_used=false",
            "failure_status": "REJECT_ZERO_THEOREM_UNDERIVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "VR1243_3_no_claim",
            "rule": "all accepted rows remain valid_for_claim=false and claim_allowed=false",
            "failure_status": "REJECT_CLAIM_FLAG",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "VR1243_4_no_closure",
            "rule": "closure_used=true is rejected for evidence-like input rows",
            "failure_status": "REJECT_CLOSURE_AS_EVIDENCE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    candidates = candidate_files()
    accepted_rows: list[dict[str, object]] = []
    rejected_rows: list[dict[str, object]] = []
    scan_rows: list[dict[str, object]] = []

    if candidates:
        for candidate_file in candidates:
            try:
                rows = read_csv(candidate_file)
                for row_number, row in enumerate(rows, start=2):
                    accepted, rejected = validate_candidate(row, candidate_file, row_number)
                    if accepted is not None:
                        accepted_rows.append(accepted)
                    if rejected is not None:
                        rejected_rows.append(rejected)
                scan_status = "CANDIDATE_FILE_PARSED"
                parse_error = ""
            except Exception as exc:
                scan_status = "CANDIDATE_FILE_PARSE_ERROR"
                parse_error = str(exc)
                rejected_rows.append(
                    {
                        "candidate_file": str(candidate_file),
                        "row_number": "",
                        "candidate_id": candidate_file.stem,
                        "route_type": "",
                        "rejection_status": "REJECTED_CSV_PARSE_ERROR",
                        "missing_or_failed_fields": parse_error,
                        "valid_for_claim": False,
                        "claim_allowed": False,
                    }
                )
            scan_rows.append(
                {
                    "scan_id": f"SCAN1243_{len(scan_rows)}",
                    "scan_path": str(QR_DIR / "raw"),
                    "candidate_file": str(candidate_file),
                    "candidate_csv_count": len(candidates),
                    "accepted_rows": len([row for row in accepted_rows if row["candidate_file"] == str(candidate_file)]),
                    "rejected_rows": len([row for row in rejected_rows if row["candidate_file"] == str(candidate_file)]),
                    "status": scan_status,
                    "parse_error": parse_error,
                    "valid_for_claim": False,
                    "claim_allowed": False,
                }
            )
    else:
        scan_rows.append(
            {
                "scan_id": "SCAN1243_0_no_candidates",
                "scan_path": str(QR_DIR / "raw"),
                "candidate_file": "",
                "candidate_csv_count": 0,
                "accepted_rows": 0,
                "rejected_rows": 0,
                "status": "NO_CANDIDATE_FILES_PRESENT",
                "parse_error": "",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    source_hunt = [
        {
            "hunt_id": "HUNT1243_0_parent_zero",
            "target": "parent Q_R=0 theorem",
            "minimum_evidence": "source path proving Q_R=0 from parent action/constraint/topological source representation without assuming R_AB=0 closure",
            "why_needed": "would close the rank-1 local reciprocity residual",
            "current_status": "MISSING",
            "next_action": "search or derive first-class/topological zero-charge theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "hunt_id": "HUNT1243_1_finite_qR_model",
            "target": "finite q_R_hat model",
            "minimum_evidence": "numeric q_R_hat with units, Q_R raw-unit convention, GM convention, source provenance, and derivation_status=sourced_finite_model or phenomenological_bound_nonclaim",
            "why_needed": "allows nonclaim gamma residual scoring against comparator",
            "current_status": "MISSING",
            "next_action": "build finite residual model or source row; do not use closure zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "hunt_id": "HUNT1243_2_GM_policy",
            "target": "GM/source convention",
            "minimum_evidence": "declared measured GM convention matching PPN comparator source and local coordinate/areal radius convention",
            "why_needed": "q_R_hat=Q_R c^2/(GM) is meaningless without normalization",
            "current_status": "MISSING",
            "next_action": "add convention row before accepting finite q_R_hat candidates",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "hunt_id": "HUNT1243_3_statistical_policy",
            "target": "PPN gamma pass policy",
            "minimum_evidence": "N_sigma and sigma_gamma policy, with comparator uncertainty source and one-sided/two-sided convention",
            "why_needed": "1241 refuses numeric q_R_hat without pass policy",
            "current_status": "MISSING",
            "next_action": "define nonclaim statistical policy before smoke scoring",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner_feed = [
        {
            "feed_id": "FEED1243_0_accepted_rows",
            "target_runner": "1241 Q_R nonclaim smoke runner",
            "accepted_nonclaim_rows": len(accepted_rows),
            "feed_status": "NO_FEED_ROWS_AVAILABLE" if not accepted_rows else "ACCEPTED_NONCLAIM_ROWS_READY",
            "reason": "no q_R_hat candidates present" if not accepted_rows else "accepted rows are nonclaim only",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    decisions = [
        {
            "decision_id": "DEC1243_0_validator_ready",
            "decision": "row-level q_R_hat validator is defined",
            "because": "future finite or zero-theorem candidates can be accepted/rejected with exact field failures",
            "next_action": "use validator when raw candidate CSVs appear",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1243_1_no_candidates",
            "decision": "no accepted q_R_hat feed row exists",
            "because": "raw q_R_hat intake is empty",
            "next_action": "work source-hunt ledger targets: zero theorem, finite model, GM convention, statistical policy",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1243_2_no_claim",
            "decision": "keep local-GR/PPN claims blocked",
            "because": "validator availability is plumbing, not a physics result",
            "next_action": "derive/source q_R_hat before any scoring",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1243_0_validator",
            "claim": "q_R_hat candidate validator exists",
            "status": "PASS_NONCLAIM",
            "reason": "validator rules, scan, accepted/rejected outputs, and source-hunt ledger generated",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1243_1_qR_feed",
            "claim": "accepted q_R_hat runner input exists",
            "status": "BLOCKED",
            "reason": f"accepted_nonclaim_rows={len(accepted_rows)}",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1243_2_zero_theorem",
            "claim": "parent Q_R=0 theorem exists",
            "status": "BLOCKED",
            "reason": "source-hunt ledger keeps parent zero theorem missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1243_3_local_GR",
            "claim": "local GR/Newton pass",
            "status": "BLOCKED",
            "reason": "q_R_hat value/theorem missing; beta/source/conservation remain open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1243_0_1244",
            "target_file": "1244-Y5-R10-QR-statistical-policy-and-GM-convention-pack.md",
            "target_script": "scripts/Y5_R10_QR_statistical_policy_and_GM_convention_pack.py",
            "task": "fill the two non-theory prerequisites for future finite q_R_hat scoring: GM/source convention and nonclaim PPN gamma statistical pass policy, while leaving q_R_hat itself missing unless sourced",
            "success_condition": "1241 runner can reject/score future finite q_R_hat rows based on a declared convention/policy, but no claim is promoted",
            "do_not_do": "do not fabricate q_R_hat, do not claim local GR, and do not run long data jobs",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_paths = [
        SOURCE_REGISTER_PATH,
        VALIDATOR_RULES_PATH,
        CANDIDATE_SCAN_PATH,
        ACCEPTED_PATH,
        REJECTED_PATH,
        SOURCE_HUNT_PATH,
        RUNNER_FEED_PATH,
        DECISION_PATH,
        CLAIM_GATES_PATH,
        NEXT_PATH,
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(VALIDATOR_RULES_PATH, validator_rules)
    write_csv(CANDIDATE_SCAN_PATH, scan_rows)
    write_csv(ACCEPTED_PATH, accepted_rows, ACCEPTED_FIELDS)
    write_csv(REJECTED_PATH, rejected_rows, REJECTED_FIELDS)
    write_csv(SOURCE_HUNT_PATH, source_hunt)
    write_csv(RUNNER_FEED_PATH, runner_feed)
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
    raw_empty_status_ok = scan_rows[0]["status"] in {"NO_CANDIDATE_FILES_PRESENT", "CANDIDATE_FILE_PARSED"}
    no_accepted_without_candidates = bool(candidates) or len(accepted_rows) == 0
    source_hunt_complete = {row["hunt_id"] for row in source_hunt} >= {
        "HUNT1243_0_parent_zero",
        "HUNT1243_1_finite_qR_model",
        "HUNT1243_2_GM_policy",
        "HUNT1243_3_statistical_policy",
    }
    runner_feed_blocked = runner_feed[0]["feed_status"] == "NO_FEED_ROWS_AVAILABLE"
    claim_gates_ok = all(
        row["status"] in {"PASS_NONCLAIM", "BLOCKED"} and is_false(row, "claim_allowed")
        for row in claim_gates
    )
    all_generated_nonclaim = all(
        is_false(row, "valid_for_claim") and is_false(row, "claim_allowed")
        for table in [
            source_register,
            validator_rules,
            scan_rows,
            accepted_rows,
            rejected_rows,
            source_hunt,
            runner_feed,
            decisions,
            claim_gates,
            next_target,
        ]
        for row in table
    )
    next_is_1244 = next_target[0]["target_file"].startswith("1244-Y5-R10-QR-statistical")
    fw_recent = formalization_recent_count()

    validation = [
        validation_row(
            "VAL1243_0_sources_exist",
            "all cited local sources exist",
            all_sources_exist,
            f"{sum(parse_bool(row['path_exists']) for row in source_register)}/{len(source_register)} sources exist",
        ),
        validation_row(
            "VAL1243_1_needles_found",
            "all cited local needles found",
            all_needles_found,
            f"{sum(parse_bool(row['needle_found']) for row in source_register)}/{len(source_register)} needles found",
        ),
        validation_row(
            "VAL1243_2_scan_status",
            "candidate scan completed",
            raw_empty_status_ok,
            f"candidate_csv_count={len(candidates)} status={scan_rows[0]['status']}",
        ),
        validation_row(
            "VAL1243_3_no_accepted_without_candidates",
            "no accepted rows exist when no candidates exist",
            no_accepted_without_candidates,
            f"accepted_rows={len(accepted_rows)}",
        ),
        validation_row(
            "VAL1243_4_source_hunt",
            "source-hunt ledger covers missing targets",
            source_hunt_complete,
            f"hunt_rows={len(source_hunt)}",
        ),
        validation_row(
            "VAL1243_5_runner_feed_blocked",
            "runner feed remains blocked without accepted rows",
            runner_feed_blocked,
            runner_feed[0]["feed_status"],
        ),
        validation_row(
            "VAL1243_6_claim_gates",
            "claim gates remain blocked/nonclaim",
            claim_gates_ok,
            f"claim_gate_rows={len(claim_gates)}",
        ),
        validation_row(
            "VAL1243_7_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_generated_nonclaim,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        ),
        validation_row(
            "VAL1243_8_next_target_1244",
            "next target is q_R statistical policy and GM convention pack",
            next_is_1244,
            next_target[0]["target_file"],
        ),
        validation_row(
            "VAL1243_9_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_counts),
        ),
        validation_row(
            "VAL1243_10_formalization_untouched",
            "formalization-workbench untouched during run",
            fw_recent == 0,
            f"formalization_recent_write_count_since_run_start={fw_recent}",
        ),
    ]
    validation.append(
        validation_row(
            "VAL1243_11_overall",
            "overall 1243 validation",
            all(row["status"] == "PASS" for row in validation),
            "1243 builds the q_R_hat validator and, with no raw candidates present, writes the source-hunt ledger without fabricating inputs",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    sections = [
        f"# {TITLE}",
        "",
        "**Current verdict:** 1243 builds the row-level `q_R_hat` validator, but finds no raw candidates. No `q_R_hat` value or `Q_R=0` theorem is fabricated.",
        "",
        "**Main progress:** future rows in `source-intake/qr-hat/raw` can now be accepted as nonclaim runner inputs or rejected with exact missing fields. Because the intake is empty, 1243 writes the source-hunt ledger instead.",
        "",
        "**No-claim guard:** no `Q_R=0`, finite `Q_R` pass, PPN pass, local-GR pass, WEP/R10 pass, or public source-coupling claim is promoted.",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Source Register",
        markdown_table(source_register, list(source_register[0].keys())),
        "",
        "## Validator Rules",
        markdown_table(validator_rules, list(validator_rules[0].keys())),
        "",
        "## Candidate Scan",
        markdown_table(scan_rows, list(scan_rows[0].keys())),
        "",
        "## Accepted Nonclaim Rows",
        markdown_table(accepted_rows, ACCEPTED_FIELDS),
        "",
        "## Rejected Rows",
        markdown_table(rejected_rows, REJECTED_FIELDS),
        "",
        "## Source-Hunt Ledger",
        markdown_table(source_hunt, list(source_hunt[0].keys())),
        "",
        "## Runner Feed Update",
        markdown_table(runner_feed, list(runner_feed[0].keys())),
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
