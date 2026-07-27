from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PACK_ID = "P8_Y5_R10_1249"
TITLE = "1249-Y5-R10-finite-qRhat-source-acquisition-and-policy-runner"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
QR_INTAKE_DIR = ROOT / "source-intake" / "qr-hat"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
INTAKE_SCAN_PATH = OUT_DIR / f"{PACK_ID}_FINITE_QRHAT_INTAKE_SCAN.csv"
VALIDATION_RULES_PATH = OUT_DIR / f"{PACK_ID}_FINITE_QRHAT_VALIDATION_RULES.csv"
CANDIDATE_RESULTS_PATH = OUT_DIR / f"{PACK_ID}_FINITE_QRHAT_CANDIDATE_RESULTS.csv"
POLICY_RUNNER_RESULTS_PATH = OUT_DIR / f"{PACK_ID}_POLICY_RUNNER_RESULTS.csv"
SOURCE_ACQUISITION_LEDGER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_ACQUISITION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1249_VALIDATION.csv"


REQUIRED_FIELDS = [
    "candidate_id",
    "route_type",
    "q_R_hat",
    "q_R_hat_units",
    "Q_R_units_before_normalization",
    "GM_convention",
    "source_path",
    "derivation_status",
    "N_sigma",
    "sigma_gamma",
    "zero_theorem_statement",
    "closure_used",
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


def parse_bool(value: object) -> bool | None:
    text = str(value).strip().lower()
    if text in {"true", "1", "yes", "y"}:
        return True
    if text in {"false", "0", "no", "n"}:
        return False
    return None


def is_false(row: dict[str, object], key: str) -> bool:
    return str(row.get(key, "")).strip().lower() in {"false", "0", "no"}


def is_placeholder(value: object) -> bool:
    text = str(value).strip()
    if text == "":
        return True
    upper = text.upper()
    return upper.startswith("MISSING") or upper in {"PLACEHOLDER", "TBD", "TODO", "NONE", "NULL", "N/A"}


def parse_float(value: object) -> float | None:
    try:
        number = float(str(value).strip())
    except Exception:
        return None
    if math.isfinite(number):
        return number
    return None


def source_reference_ok(value: object) -> bool:
    text = str(value).strip()
    if is_placeholder(text):
        return False
    if text.startswith(("http://", "https://", "doi:", "arxiv:", "SRC", "source-intake/")):
        return True
    return source_path(text).exists()


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
    }


def scan_candidate_files() -> tuple[list[dict[str, object]], list[dict[str, str]]]:
    scan_rows: list[dict[str, object]] = []
    candidate_rows: list[dict[str, str]] = []
    dirs = [QR_INTAKE_DIR / "raw", QR_INTAKE_DIR / "accepted"]
    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)
        csv_files = sorted(directory.glob("*.csv"))
        if not csv_files:
            scan_rows.append(
                {
                    "scan_id": f"SCAN1249_{directory.name}_empty",
                    "directory": str(directory),
                    "file": "",
                    "rows_found": 0,
                    "scan_status": "NO_CANDIDATE_FILES_FOUND",
                    "valid_for_claim": False,
                    "claim_allowed": False,
                }
            )
            continue
        for file_path in csv_files:
            try:
                rows = read_csv(file_path)
                scan_status = "CSV_PARSED"
                for index, row in enumerate(rows, start=1):
                    row["_source_file"] = str(file_path)
                    row["_source_row"] = str(index)
                    candidate_rows.append(row)
            except Exception as exc:
                rows = []
                scan_status = f"CSV_PARSE_FAILED:{exc}"
            scan_rows.append(
                {
                    "scan_id": f"SCAN1249_{directory.name}_{file_path.stem}",
                    "directory": str(directory),
                    "file": str(file_path),
                    "rows_found": len(rows),
                    "scan_status": scan_status,
                    "valid_for_claim": False,
                    "claim_allowed": False,
                }
            )
    return scan_rows, candidate_rows


def validate_candidate(row: dict[str, Any], policy: dict[str, str]) -> dict[str, object]:
    failures: list[str] = []
    route_type = str(row.get("route_type", "")).strip()
    q_value = row.get("q_R_hat", "")
    q_number = parse_float(q_value)
    closure_used = parse_bool(row.get("closure_used", ""))
    valid_for_claim = parse_bool(row.get("valid_for_claim", ""))
    claim_allowed = parse_bool(row.get("claim_allowed", ""))

    for field in REQUIRED_FIELDS:
        if field not in row:
            failures.append(f"MISSING_FIELD_{field}")

    if route_type != "finite_qR_hat":
        failures.append("REJECT_BAD_ROUTE_TYPE")
    if q_number is None:
        failures.append("REJECT_MISSING_OR_NONNUMERIC_QR")
    if str(row.get("q_R_hat_units", "")).strip().lower() != "dimensionless":
        failures.append("REJECT_BAD_QR_UNITS")
    if is_placeholder(row.get("Q_R_units_before_normalization", "")):
        failures.append("REJECT_MISSING_RAW_QR_UNIT_DECLARATION")
    if is_placeholder(row.get("GM_convention", "")):
        failures.append("REJECT_MISSING_GM_CONVENTION")
    if not source_reference_ok(row.get("source_path", "")):
        failures.append("REJECT_MISSING_SOURCE")
    if str(row.get("derivation_status", "")).strip() not in {"sourced_finite_model", "phenomenological_bound_nonclaim"}:
        failures.append("REJECT_BAD_DERIVATION_STATUS")
    if parse_float(row.get("N_sigma", "")) != parse_float(policy["N_sigma"]):
        failures.append("REJECT_POLICY_NSIGMA_MISMATCH")
    if parse_float(row.get("sigma_gamma", "")) != parse_float(policy["sigma_gamma"]):
        failures.append("REJECT_POLICY_SIGMA_MISMATCH")
    if closure_used is not False:
        failures.append("REJECT_CLOSURE_AS_EVIDENCE")
    if valid_for_claim is not False or claim_allowed is not False:
        failures.append("REJECT_CLAIM_FLAG")

    gamma_minus_1 = ""
    abs_gamma_minus_1 = ""
    raw_numeric_pass = False
    if q_number is not None:
        gamma = -0.5 * q_number
        gamma_minus_1 = gamma
        abs_gamma_minus_1 = abs(gamma)
        raw_numeric_pass = abs(gamma) <= float(policy["N_sigma"]) * float(policy["sigma_gamma"])

    acceptance_status = "ACCEPTED_NONCLAIM_FINITE_QRHAT" if not failures else ";".join(failures)
    return {
        "candidate_id": row.get("candidate_id", ""),
        "source_file": row.get("_source_file", ""),
        "source_row": row.get("_source_row", ""),
        "route_type": route_type,
        "q_R_hat": q_value,
        "gamma_minus_1_QR": gamma_minus_1,
        "abs_gamma_minus_1_QR": abs_gamma_minus_1,
        "N_sigma": row.get("N_sigma", ""),
        "sigma_gamma": row.get("sigma_gamma", ""),
        "raw_numeric_pass": raw_numeric_pass,
        "acceptance_status": acceptance_status,
        "runner_eligible": acceptance_status == "ACCEPTED_NONCLAIM_FINITE_QRHAT",
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def recent_formalization_writes() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    recent: list[Path] = []
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            mtime = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if mtime >= RUN_STARTED_UTC:
                recent.append(path)
    return recent


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1249_0_1248_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1248_NEXT_TARGET.csv",
            "needle": "NEXT1248_0_1249",
            "purpose": "handoff to finite q_Rhat fallback",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1249_1_1248_zero_reject",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1248_ZERO_THEOREM_CANDIDATE_STATUS.csv",
            "needle": "REJECT_ZERO_THEOREM_UNDERIVED",
            "purpose": "ansatz zero must not enter finite runner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1249_2_1248_handoff",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1248_FINITE_QR_HANDOFF.csv",
            "needle": "READY_AS_NEXT_FALLBACK",
            "purpose": "finite q_Rhat fallback requirements",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1249_3_1242_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1242_QR_HAT_INPUT_CONTRACT.csv",
            "needle": "finite_qR_hat",
            "purpose": "finite q_Rhat row contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1249_4_1243_rules",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1243_VALIDATOR_RULES.csv",
            "needle": "VR1243_1_finite",
            "purpose": "finite validator rules",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1249_5_1244_policy",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1244_RUNNER_POLICY_FEED.csv",
            "needle": "4.6e-05",
            "purpose": "strict q_Rhat guardrail and policy",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1249_6_1244_GM",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1244_GM_CONVENTION_PACK.csv",
            "needle": "GM1244_0_qR_definition",
            "purpose": "GM convention required for finite rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1249_7_1240_map",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1240_QR_TO_PPN_MAPPING_SCHEMA.csv",
            "needle": "QMAP1240_3_gamma_projection",
            "purpose": "gamma projection for policy runner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    policy = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1244_RUNNER_POLICY_FEED.csv"))[0]
    zero_candidate = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1248_ZERO_THEOREM_CANDIDATE_STATUS.csv"))[0]
    intake_scan, candidate_rows = scan_candidate_files()

    validation_rules = [
        {
            "rule_id": "QRV1249_0_route",
            "rule": "route_type must be finite_qR_hat",
            "reject_status": "REJECT_BAD_ROUTE_TYPE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "QRV1249_1_numeric",
            "rule": "q_R_hat must parse as finite dimensionless float",
            "reject_status": "REJECT_MISSING_OR_NONNUMERIC_QR;REJECT_BAD_QR_UNITS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "QRV1249_2_source_GM",
            "rule": "source_path and GM_convention must be non-placeholder; raw-unit declaration required",
            "reject_status": "REJECT_MISSING_SOURCE;REJECT_MISSING_GM_CONVENTION;REJECT_MISSING_RAW_QR_UNIT_DECLARATION",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "QRV1249_3_policy",
            "rule": "N_sigma and sigma_gamma must match 1244 policy",
            "reject_status": "REJECT_POLICY_NSIGMA_MISMATCH;REJECT_POLICY_SIGMA_MISMATCH",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "QRV1249_4_no_closure",
            "rule": "closure_used must be false; ansatz zero and closure zero are refused",
            "reject_status": "REJECT_CLOSURE_AS_EVIDENCE;REJECT_ZERO_THEOREM_UNDERIVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "QRV1249_5_no_claim_flags",
            "rule": "valid_for_claim and claim_allowed must remain false in this checkpoint",
            "reject_status": "REJECT_CLAIM_FLAG",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    candidate_results = [validate_candidate(row, policy) for row in candidate_rows]
    rejected_special_rows = [
        {
            "candidate_id": zero_candidate["candidate_id"],
            "source_file": "source-intake/mts_residuals/P8_Y5_R10_1248_ZERO_THEOREM_CANDIDATE_STATUS.csv",
            "source_row": "1",
            "route_type": zero_candidate["route_type"],
            "q_R_hat": zero_candidate["q_R_hat"],
            "gamma_minus_1_QR": "",
            "abs_gamma_minus_1_QR": "",
            "N_sigma": "",
            "sigma_gamma": "",
            "raw_numeric_pass": False,
            "acceptance_status": zero_candidate["acceptance_status"],
            "runner_eligible": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]
    candidate_results.extend(rejected_special_rows)

    accepted_candidates = [row for row in candidate_results if row["runner_eligible"] is True]
    policy_runner_results: list[dict[str, object]] = []
    if accepted_candidates:
        for row in accepted_candidates:
            numeric_pass = bool(row["raw_numeric_pass"])
            policy_runner_results.append(
                {
                    "run_id": f"RUN1249_{row['candidate_id']}",
                    "candidate_id": row["candidate_id"],
                    "q_R_hat": row["q_R_hat"],
                    "gamma_minus_1_QR": row["gamma_minus_1_QR"],
                    "strict_guardrail": f"abs(gamma_minus_1_QR)<={float(policy['N_sigma']) * float(policy['sigma_gamma'])}",
                    "runner_status": "READY_NONCLAIM_NUMERIC_PASS" if numeric_pass else "READY_NONCLAIM_NUMERIC_FAIL",
                    "valid_for_claim": False,
                    "claim_allowed": False,
                }
            )
    else:
        policy_runner_results.append(
            {
                "run_id": "RUN1249_0_no_accepted_candidates",
                "candidate_id": "NONE",
                "q_R_hat": "MISSING_QR_VALUE",
                "gamma_minus_1_QR": "",
                "strict_guardrail": f"abs(q_R_hat)<={policy['q_R_hat_abs_guardrail']}",
                "runner_status": "NO_ACCEPTED_FINITE_QRHAT_ROWS",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    accepted_count = len(accepted_candidates)
    numeric_pass_count = sum(1 for row in accepted_candidates if bool(row["raw_numeric_pass"]))
    has_live_candidate_rows = len(candidate_rows) > 0
    finite_value_gate_status = "PASS_NONCLAIM" if accepted_count else "BLOCKED"
    finite_value_gate_reason = (
        f"{accepted_count} finite q_Rhat candidate row(s) accepted for nonclaim smoke"
        if accepted_count
        else "qr-hat intake folders contain no accepted finite candidate rows"
    )
    policy_score_gate_status = "PASS_NONCLAIM" if numeric_pass_count else "BLOCKED"
    policy_score_gate_reason = (
        f"{numeric_pass_count} accepted nonclaim row(s) pass the strict gamma smoke guardrail"
        if numeric_pass_count
        else "policy runner has no accepted finite q_Rhat row passing the strict guardrail"
    )

    source_acquisition_ledger = [
        {
            "ledger_id": "SA1249_0_parent_coefficients",
            "target": "derive finite q_R_hat from parent coefficients",
            "required_evidence": "H_core/L_MTS_core, canonical brackets, boundary class, and coefficient map producing q_R_hat",
            "current_status": "MISSING_PARENT_COEFFICIENT_MAP",
            "next_action": "return to H_core only if deriving a real coefficient map, not another closure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "ledger_id": "SA1249_1_phenomenological_bound",
            "target": "nonclaim phenomenological q_R_hat bound row",
            "required_evidence": "source-backed model or fit-derived q_R_hat with units, no closure, GM convention, and uncertainty policy",
            "current_status": "NONCLAIM_BOUND_ROW_PRESENT" if accepted_count else "MISSING_NUMERIC_SOURCE_ROW",
            "next_action": "treat accepted bound rows as ceilings only; derive a parent coefficient before any theory claim" if accepted_count else "prepare a template only; do not invent a value",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "ledger_id": "SA1249_2_raw_QR_conversion",
            "target": "raw Q_R plus GM conversion",
            "required_evidence": "raw Q_R units, source body, measured GM, coordinate convention, and q_R_hat=Q_R c^2/(G M_source)",
            "current_status": "MISSING_RAW_QR_AND_GM_SOURCE",
            "next_action": "bind any future dimensional Q_R to 1244 GM convention before scoring",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "ledger_id": "SA1249_3_boundary_charge",
            "target": "finite reciprocal boundary charge",
            "required_evidence": "boundary/corner audit showing allowed nonzero Q_R and how it enters exterior weak-field gamma",
            "current_status": "MISSING_BOUNDARY_CHARGE_AUDIT",
            "next_action": "if boundary route opens, create finite_qR_hat candidate row; otherwise keep local PPN blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1249_0_intake_runner",
            "claim": "finite q_Rhat intake runner exists",
            "status": "PASS_NONCLAIM",
            "reason": "scanner, validator, and policy runner generated",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1249_1_ansatz_zero",
            "claim": "1248 ansatz zero is valid q_Rhat input",
            "status": "BLOCKED",
            "reason": "ZTC1248_0_minimal_ansatz remains REJECT_ZERO_THEOREM_UNDERIVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1249_2_finite_qRhat_value",
            "claim": "finite q_Rhat source row exists",
            "status": finite_value_gate_status,
            "reason": finite_value_gate_reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1249_3_policy_score",
            "claim": "finite q_Rhat nonclaim smoke row passes PPN gamma policy",
            "status": policy_score_gate_status,
            "reason": policy_score_gate_reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1249_4_local_GR",
            "claim": "derived local GR/Newton limit",
            "status": "BLOCKED",
            "reason": "Q_R theorem/value, beta, matter coupling, conservation, and boundary terms remain open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1249_0_no_fabrication",
            "decision": "do not treat finite q_Rhat intake as a theory prediction",
            "because": "accepted rows, if present, are nonclaim source/bound rows and 1248 ansatz zero is rejected",
            "next_action": "derive a parent coefficient/map before promoting any q_Rhat value beyond smoke",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1249_1_runner_ready",
            "decision": "keep finite runner ready for future rows",
            "because": "policy and GM convention are ready, and row-level rejection rules now exist",
            "next_action": "next checkpoint should make a source template and exact evidence checklist for the first finite row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1249_2_local_status",
            "decision": "local branch remains blocked but disciplined",
            "because": "we now know the precise missing theorem/value, not just a vague GR-reduction gap",
            "next_action": "choose between parent H_core coefficient map or empirical finite q_Rhat bound source",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1249_0_1250",
            "target_file": "1250-Y5-R10-first-finite-qRhat-template-and-Hcore-coefficient-checklist.md",
            "target_script": "scripts/Y5_R10_first_finite_qRhat_template_and_Hcore_coefficient_checklist.py",
            "task": "create the exact first finite q_Rhat source-row template and H_core coefficient checklist so the next real candidate can be entered without ambiguity or placeholder leakage",
            "success_condition": "template includes all 1249-required fields, rejects ansatz/closure zero, and identifies the minimum parent or phenomenological evidence needed for the first q_Rhat row",
            "do_not": "do not fabricate q_Rhat or treat no-candidate runner output as evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_sets = [
        source_register,
        intake_scan,
        validation_rules,
        candidate_results,
        policy_runner_results,
        source_acquisition_ledger,
        claim_gates,
        decisions,
        next_target,
    ]

    output_paths = [
        SOURCE_REGISTER_PATH,
        INTAKE_SCAN_PATH,
        VALIDATION_RULES_PATH,
        CANDIDATE_RESULTS_PATH,
        POLICY_RUNNER_RESULTS_PATH,
        SOURCE_ACQUISITION_LEDGER_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(INTAKE_SCAN_PATH, intake_scan)
    write_csv(VALIDATION_RULES_PATH, validation_rules)
    write_csv(CANDIDATE_RESULTS_PATH, candidate_results)
    write_csv(POLICY_RUNNER_RESULTS_PATH, policy_runner_results)
    write_csv(SOURCE_ACQUISITION_LEDGER_PATH, source_acquisition_ledger)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_target)

    source_checks = [exists_and_contains(row["local_path"], row["needle"]) for row in source_register]
    all_sources_exist = all(exists for exists, _ in source_checks)
    all_needles_found = all(found for _, found in source_checks)
    qr_dirs_exist = all((QR_INTAKE_DIR / name).exists() for name in ["raw", "accepted", "rejected", "docs"])
    scan_well_formed = all(row["scan_status"] in {"NO_CANDIDATE_FILES_FOUND", "CSV_PARSED"} for row in intake_scan)
    ansatz_zero_rejected = any(row["candidate_id"] == "ZTC1248_0_minimal_ansatz" and row["acceptance_status"] == "REJECT_ZERO_THEOREM_UNDERIVED" for row in candidate_results)
    runner_result_consistent = (
        (accepted_count == 0 and policy_runner_results[0]["runner_status"] == "NO_ACCEPTED_FINITE_QRHAT_ROWS")
        or (accepted_count > 0 and all(str(row["runner_status"]).startswith("READY_NONCLAIM_NUMERIC_") for row in policy_runner_results))
    )
    policy_loaded = policy["N_sigma"] == "1" and policy["sigma_gamma"] == "2.3e-5" and policy["q_R_hat_abs_guardrail"] == "4.6e-05"
    claim_gates_blocked = all(
        row["status"] in {"PASS_NONCLAIM", "BLOCKED"} and is_false(row, "claim_allowed")
        for row in claim_gates
    )
    all_generated_nonclaim = all(
        is_false(row, "valid_for_claim") and (("claim_allowed" not in row) or is_false(row, "claim_allowed"))
        for rows in generated_sets
        for row in rows
        if "valid_for_claim" in row
    )
    next_is_1250 = next_target[0]["next_id"] == "NEXT1249_0_1250"

    parsed_counts: list[str] = []
    csv_parse_ok = True
    for path in output_paths:
        try:
            parsed_counts.append(f"{path.name}:{len(read_csv(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parsed_counts.append(f"{path.name}:PARSE_FAIL:{exc}")

    fw_recent = recent_formalization_writes()

    validation = [
        validation_row("VAL1249_0_sources_exist", "all cited local sources exist", all_sources_exist, f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist"),
        validation_row("VAL1249_1_needles_found", "all cited local needles found", all_needles_found, f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found"),
        validation_row("VAL1249_2_qr_dirs", "qr-hat intake directories exist", qr_dirs_exist, "raw/accepted/rejected/docs directories present"),
        validation_row("VAL1249_3_candidate_scan", "candidate scan is well formed", scan_well_formed, f"live_candidate_rows={len(candidate_rows)}; scan_rows={len(intake_scan)}"),
        validation_row("VAL1249_4_ansatz_zero_rejected", "1248 ansatz zero is rejected", ansatz_zero_rejected, "ZTC1248_0 -> REJECT_ZERO_THEOREM_UNDERIVED"),
        validation_row("VAL1249_5_runner_result_consistent", "policy runner result matches accepted candidate state", runner_result_consistent, f"accepted_count={accepted_count}; numeric_pass_count={numeric_pass_count}"),
        validation_row("VAL1249_6_policy_loaded", "1244 policy values are loaded", policy_loaded, f"N_sigma={policy['N_sigma']} sigma_gamma={policy['sigma_gamma']} q_guardrail={policy['q_R_hat_abs_guardrail']}"),
        validation_row("VAL1249_7_claim_gates", "claim gates remain blocked/nonclaim", claim_gates_blocked, f"claim_gate_rows={len(claim_gates)}"),
        validation_row("VAL1249_8_nonclaim_policy", "all generated rows remain nonclaim", all_generated_nonclaim, "valid_for_claim=false and claim_allowed=false throughout generated tables"),
        validation_row("VAL1249_9_next_target_1250", "next target is finite q_Rhat template/checklist", next_is_1250, next_target[0]["target_file"]),
        validation_row("VAL1249_10_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(parsed_counts)),
        validation_row("VAL1249_11_formalization_untouched", "formalization-workbench untouched during run", len(fw_recent) == 0, f"formalization_recent_write_count_since_run_start={len(fw_recent)}"),
    ]
    validation.append(
        validation_row(
            "VAL1249_12_overall",
            "overall 1249 validation",
            all(row["status"] == "PASS" for row in validation),
            "1249 validates finite q_Rhat intake rows as nonclaim smoke inputs, rejects ansatz zero/placeholders, and keeps local-GR claims blocked",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    sections = [
        f"# {TITLE}",
        "",
        "**Current verdict:** 1249 validates the finite `q_R_hat` source-intake and policy runner. Candidate rows, if present, are accepted only as nonclaim smoke inputs; the 1248 ansatz-zero row is explicitly rejected, and no local-GR claim is promoted.",
        "",
        f"**Main progress:** the fallback branch is executable. Live candidate rows found: `{len(candidate_rows)}`; accepted nonclaim rows: `{accepted_count}`; strict gamma smoke passes: `{numeric_pass_count}`. A row must carry numeric dimensionless `q_R_hat`, source/provenance, GM convention, policy fields, no closure, and false claim flags.",
        "",
        "**No-claim guard:** no local GR, local PPN, R10/WEP, or source-coupling claim is promoted. No placeholder or closure-zero row is accepted.",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Source Register",
        markdown_table(source_register, list(source_register[0].keys())),
        "",
        "## Finite QRhat Intake Scan",
        markdown_table(intake_scan, list(intake_scan[0].keys())),
        "",
        "## Finite QRhat Validation Rules",
        markdown_table(validation_rules, list(validation_rules[0].keys())),
        "",
        "## Finite QRhat Candidate Results",
        markdown_table(candidate_results, list(candidate_results[0].keys())),
        "",
        "## Policy Runner Results",
        markdown_table(policy_runner_results, list(policy_runner_results[0].keys())),
        "",
        "## Source Acquisition Ledger",
        markdown_table(source_acquisition_ledger, list(source_acquisition_ledger[0].keys())),
        "",
        "## Claim Gates",
        markdown_table(claim_gates, list(claim_gates[0].keys())),
        "",
        "## Decision Ledger",
        markdown_table(decisions, list(decisions[0].keys())),
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
