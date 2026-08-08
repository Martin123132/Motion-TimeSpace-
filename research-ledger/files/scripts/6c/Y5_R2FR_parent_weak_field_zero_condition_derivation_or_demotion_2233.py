from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "2233-Y5-R2FR-parent-weak-field-zero-condition-derivation-or-demotion.md"
BRANCH_ID = "MTS_R2FR_PARENT_QLOC_WEAK_FIELD_ZERO_CONDITION_2233"
START_TS = datetime.now(timezone.utc).timestamp()


SOURCE_FILES = {
    "2232_doc": ROOT / "2232-Y5-R2FR-qR-delta-beta-two-parameter-PPN-control-runner-and-zero-condition-hunt.md",
    "2232_validation": OUT / "P8_Y5_BRR545_2232_VALIDATION.csv",
    "2232_next": OUT / "P8_Y5_PARENT_QLOC_2232_NEXT_TARGET.csv",
    "1560_doc": ROOT / "1560-Y5-parent-weak-field-zero-condition-derivation-or-demotion.md",
    "1560_validation": OUT / "P8_Y5_BRR545_1560_VALIDATION.csv",
    "1560_weak": OUT / "P8_Y5_PARENT_QLOC_1560_WEAK_FIELD_DERIVATION_ATTEMPT.csv",
    "1560_qr": OUT / "P8_Y5_PARENT_QLOC_1560_QR_ZERO_ROUTE_AUDIT.csv",
    "1560_beta": OUT / "P8_Y5_PARENT_QLOC_1560_BETA_ZERO_ROUTE_AUDIT.csv",
    "1560_contract": OUT / "P8_Y5_PARENT_QLOC_1560_CONDITIONAL_ZERO_THEOREM_CONTRACT.csv",
    "1560_demotion": OUT / "P8_Y5_PARENT_QLOC_1560_BOUNDED_CLOSURE_DEMOTION.csv",
    "1560_runner": OUT / "P8_Y5_PARENT_QLOC_1560_RUNNER_NONCLAIM.csv",
    "1560_claim": OUT / "P8_Y5_PARENT_QLOC_1560_CLAIM_GATE.csv",
    "1560_decision": OUT / "P8_Y5_PARENT_QLOC_1560_DECISION.csv",
    "1560_next": OUT / "P8_Y5_PARENT_QLOC_1560_NEXT_TARGET.csv",
}


SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_2233_SOURCE_REGISTER.csv"
WEAK_FIELD_ATTEMPT = OUT / "P8_Y5_PARENT_QLOC_2233_WEAK_FIELD_DERIVATION_ATTEMPT.csv"
QR_ZERO_AUDIT = OUT / "P8_Y5_PARENT_QLOC_2233_QR_ZERO_ROUTE_AUDIT.csv"
BETA_ZERO_AUDIT = OUT / "P8_Y5_PARENT_QLOC_2233_BETA_ZERO_ROUTE_AUDIT.csv"
CONDITIONAL_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_2233_CONDITIONAL_ZERO_THEOREM_CONTRACT.csv"
BOUNDED_DEMOTION = OUT / "P8_Y5_PARENT_QLOC_2233_BOUNDED_CLOSURE_DEMOTION.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_2233_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_2233_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_2233_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_2233_NEXT_TARGET.csv"
BRANCH_COPIES = OUT / "P8_Y5_PARENT_QLOC_2233_BRANCH_COPIES.csv"
VALIDATION = OUT / "P8_Y5_BRR545_2233_VALIDATION.csv"


COPY_TARGETS = {
    "queue": QUEUE / "JR2233_WEAK_FIELD_ZERO_CONDITION_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "weak_field_zero_condition_nonclaim_2233.csv",
    "beta_docs": BETA_DOCS / "WEAK_FIELD_ZERO_CONDITION_2233_NONCLAIM.csv",
}


OLD_TO_NEW = [
    ("1561-Y5-minimal-parent-weak-field-action-ansatz-and-Euler-Ward-PPN-gate.md", "2234-Y5-R2FR-minimal-parent-weak-field-action-ansatz-and-Euler-Ward-PPN-gate.md"),
    ("scripts/Y5_minimal_parent_weak_field_action_ansatz_and_Euler_Ward_PPN_gate.py", "scripts/Y5_R2FR_minimal_parent_weak_field_action_ansatz_and_Euler_Ward_PPN_gate_2234.py"),
    ("NEXT_1561_MINIMAL_PARENT_WEAK_FIELD_ACTION_ANSATZ", "NEXT_2234_MINIMAL_PARENT_WEAK_FIELD_ACTION_ANSATZ"),
    ("NEXT_1561", "NEXT_2234"),
    ("1561", "2234"),
    ("1560", "2233"),
    ("1559", "2232"),
    ("1558", "2231"),
]


GENERATED = [
    SOURCE_REGISTER,
    WEAK_FIELD_ATTEMPT,
    QR_ZERO_AUDIT,
    BETA_ZERO_AUDIT,
    CONDITIONAL_CONTRACT,
    BOUNDED_DEMOTION,
    RUNNER,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
    BRANCH_COPIES,
    VALIDATION,
]


def flags() -> dict[str, bool]:
    return {
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def rewrite_value(value: str) -> str:
    rewritten = value
    for old, new in OLD_TO_NEW:
        rewritten = rewritten.replace(old, new)
    return rewritten


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def transform_old_csv(path: Path) -> list[dict[str, Any]]:
    rows = []
    for row in read_csv(path):
        new_row: dict[str, Any] = {"branch_id": BRANCH_ID}
        for key, value in row.items():
            if key == "same_parent_branch_id":
                continue
            new_row[key] = rewrite_value(value)
        rows.append(new_row)
    return rows


def validation_pass(path: Path) -> bool:
    if not path.exists():
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = "check_id" if "check_id" in rows[0] else "validation_id"
    result_key = "result" if "result" in rows[0] else "status"
    overall_rows = [row for row in rows if "overall" in row.get(id_key, "").lower()]
    if overall_rows:
        return all(row.get(result_key) == "PASS" for row in overall_rows)
    return all(row.get(result_key) == "PASS" for row in rows)


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    keys = [
        "numeric_value_present",
        "source_backed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_2233_artifacts_absent() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(
        path.is_file()
        and "2233" in path.name
        and ".venv" not in path.relative_to(FORMALIZATION).parts
        for path in FORMALIZATION.rglob("*")
    )


def formalization_untouched_since_start() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(path.is_file() and path.stat().st_mtime >= START_TS for path in FORMALIZATION.rglob("*"))


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        role = "current qR/delta-beta control handoff" if key.startswith("2232") else "older weak-field zero-condition evidence"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC2233_{index}_{key}",
                "source_path": rel(path),
                "path_exists": path.exists(),
                "validation_overall_pass": validation_pass(path) if key.endswith("validation") else "",
                "role": role,
                **flags(),
            }
        )
    return rows


def copy_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, target in COPY_TARGETS.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(CONDITIONAL_CONTRACT, target)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": copy_id,
                "source_path": rel(CONDITIONAL_CONTRACT),
                "target_path": rel(target),
                "copied": target.exists(),
                "parse_ok": parse_csv(target),
                **flags(),
            }
        )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_doc(
    source: list[dict[str, Any]],
    weak: list[dict[str, Any]],
    qr: list[dict[str, Any]],
    beta: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    demotion: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    claim: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 2233 - Y5/R2FR Parent Weak-Field Zero-Condition Derivation Or Demotion",
            "## Verdict\n"
            "- 2233 imports the old `1560` parent weak-field zero-condition attempt into the current R2FR line.\n"
            "- The current corpus does not derive both `q_R=0` and `delta_beta=0`: kinetic reciprocal strain leaves `Q_R` hair, the multiplier route is closure unless parent-owned, and the second-order beta completion is not varied from an explicit parent action.\n"
            "- This is not a dead end: the conditional theorem contract is now exact and says what must be supplied for local GR recovery.\n"
            "- Until those premises are signed, the local GR/Newton branch is demoted to a bounded-closure control lane, using the `2232` runner as a nonclaim residual harness.\n"
            "- Next target is the minimal parent weak-field action ansatz with Euler/Ward/PPN gates.",
            "## Source Register\n"
            + md_table(source, ["source_id", "source_path", "path_exists", "validation_overall_pass", "role"]),
            "## Weak-Field Derivation Attempt\n"
            + md_table(weak, ["attempt_id", "route", "equation_or_condition", "consequence", "status", "limitation"]),
            "## q_R Zero Route Audit\n"
            + md_table(qr, ["route_id", "route", "test_equation", "result", "status", "missing_or_forbidden"]),
            "## Beta Zero Route Audit\n"
            + md_table(beta, ["route_id", "route", "test_equation", "result", "status", "missing_or_forbidden"]),
            "## Conditional Zero Theorem Contract\n"
            + md_table(contract, ["contract_id", "premise", "required_statement", "why_needed", "status"]),
            "## Bounded Closure Demotion\n"
            + md_table(demotion, ["demotion_id", "object", "new_status", "reason", "allowed_use"]),
            "## Runner\n"
            + md_table(runner, ["runner_id", "test", "current_status", "detail"]),
            "## Claim Gate\n"
            + md_table(claim, ["gate_id", "claim_gate", "status", "reason"]),
            "## Decision Ledger\n"
            + md_table(decision, ["decision_id", "decision", "result", "reason"]),
            "## Next Target\n"
            + md_table(next_target, ["next_id", "next_target", "script", "objective", "do_not"]),
            "## Branch Copies\n"
            + md_table(copies, ["copy_id", "source_path", "target_path", "copied", "parse_ok"]),
            "## Validation\n"
            + md_table(validation, ["check_id", "result", "detail"]),
            "## Working Interpretation\n\n"
            "This is a sober but useful result. The local branch cannot honestly be advertised as a derived GR limit yet, but it now has a precise repair contract: an explicit parent weak-field action, an owned reciprocal zero mechanism, common source normalization, universal matter/coframe descent, second-order beta completion, a Ward/Bianchi identity, and silence or bounds for extra modes. That is the route forward, not more local fitting.",
            "",
        ]
    )


def validation_rows(generated_paths: list[Path]) -> list[dict[str, Any]]:
    weak = read_csv(WEAK_FIELD_ATTEMPT)
    qr = read_csv(QR_ZERO_AUDIT)
    beta = read_csv(BETA_ZERO_AUDIT)
    demotion = read_csv(BOUNDED_DEMOTION)
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2233_00_sources_exist",
            "result": "PASS" if all(path.exists() for path in SOURCE_FILES.values()) else "FAIL",
            "detail": "all cited 2233 source paths exist",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2233_01_prior_validations",
            "result": "PASS" if validation_pass(SOURCE_FILES["2232_validation"]) and validation_pass(SOURCE_FILES["1560_validation"]) else "FAIL",
            "detail": "2232 and 1560 validations pass overall",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2233_02_weak_verdict",
            "result": "PASS" if any(row.get("status") == "DERIVATION_FAILED_DEMOTE_TO_BOUNDED_CLOSURE" for row in weak) else "FAIL",
            "detail": "weak-field derivation verdict is explicit",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2233_03_qR_no_route",
            "result": "PASS" if any(row.get("status") == "NO_ACCEPTED_PARENT_ZERO_ROUTE" for row in qr) else "FAIL",
            "detail": "q_R has no accepted parent zero route",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2233_04_beta_no_route",
            "result": "PASS" if any(row.get("status") == "NO_ACCEPTED_PARENT_BETA_ROUTE" for row in beta) else "FAIL",
            "detail": "delta_beta has no accepted parent route",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2233_05_contract_complete",
            "result": "PASS" if len(read_csv(CONDITIONAL_CONTRACT)) >= 8 else "FAIL",
            "detail": "conditional zero theorem contract written",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2233_06_demotion",
            "result": "PASS" if any(row.get("new_status") == "BOUNDED_CLOSURE_CONTROL_NOT_DERIVED" for row in demotion) else "FAIL",
            "detail": "local GR branch demoted to bounded closure control",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2233_07_runner_demotion",
            "result": "PASS" if any(row.get("current_status") == "DERIVATION_FAILED_DEMOTED_TO_BOUNDED_CLOSURE" for row in read_csv(RUNNER)) else "FAIL",
            "detail": "runner records derivation failure and demotion",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2233_08_claim_gates",
            "result": "PASS" if all("BLOCKED" in row.get("status", "") or row.get("status", "").startswith("PASS") for row in read_csv(CLAIM_GATE)) else "FAIL",
            "detail": "all claim gates remain blocked/nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2233_09_decision_next",
            "result": "PASS" if any(row.get("result") == "NEXT_2234_MINIMAL_PARENT_WEAK_FIELD_ACTION_ANSATZ" for row in read_csv(DECISION)) else "FAIL",
            "detail": "decision selects minimal parent weak-field action ansatz next",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2233_10_next_target",
            "result": "PASS" if read_csv(NEXT_TARGET)[0]["next_target"].startswith("2234-Y5-R2FR-minimal-parent-weak-field") else "FAIL",
            "detail": "next target is current-numbered minimal parent weak-field action ansatz",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2233_11_csv_parse",
            "result": "PASS" if all(parse_csv(path) for path in generated_paths) else "FAIL",
            "detail": "all generated 2233 CSVs parse cleanly",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2233_12_claim_flags_false",
            "result": "PASS" if generated_flags_false(generated_paths) else "FAIL",
            "detail": "all generated flags remain nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2233_13_branch_copies",
            "result": "PASS" if all(row["copied"] == "True" and row["parse_ok"] == "True" for row in read_csv(BRANCH_COPIES)) else "FAIL",
            "detail": "branch copies written and parse",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2233_14_pycache_absent",
            "result": "PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after run",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2233_15_formalization_no_2233",
            "result": "PASS" if formalization_2233_artifacts_absent() else "FAIL",
            "detail": "formalization-workbench has no non-venv 2233 artifacts",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2233_16_formalization_untouched",
            "result": "PASS" if formalization_untouched_since_start() else "FAIL",
            "detail": "formalization-workbench untouched during 2233 run",
        },
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2233_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2233 imports parent weak-field zero-condition failure/demotion, records the conditional theorem contract, and selects minimal parent weak-field action ansatz next",
        }
    )
    return rows


def main() -> None:
    source = source_rows()
    weak = transform_old_csv(SOURCE_FILES["1560_weak"])
    qr = transform_old_csv(SOURCE_FILES["1560_qr"])
    beta = transform_old_csv(SOURCE_FILES["1560_beta"])
    contract = transform_old_csv(SOURCE_FILES["1560_contract"])
    demotion = transform_old_csv(SOURCE_FILES["1560_demotion"])
    runner = transform_old_csv(SOURCE_FILES["1560_runner"])
    claim = transform_old_csv(SOURCE_FILES["1560_claim"])
    decision = transform_old_csv(SOURCE_FILES["1560_decision"])
    next_target = transform_old_csv(SOURCE_FILES["1560_next"])

    write_csv(SOURCE_REGISTER, source)
    write_csv(WEAK_FIELD_ATTEMPT, weak)
    write_csv(QR_ZERO_AUDIT, qr)
    write_csv(BETA_ZERO_AUDIT, beta)
    write_csv(CONDITIONAL_CONTRACT, contract)
    write_csv(BOUNDED_DEMOTION, demotion)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, claim)
    write_csv(DECISION, decision)
    write_csv(NEXT_TARGET, next_target)
    copies = copy_rows()
    write_csv(BRANCH_COPIES, copies)

    remove_pycache()
    generated_before_validation = [path for path in GENERATED if path != VALIDATION]
    validation = validation_rows(generated_before_validation)
    write_csv(VALIDATION, validation)
    remove_pycache()

    DOC.write_text(
        build_doc(
            source,
            weak,
            qr,
            beta,
            contract,
            demotion,
            runner,
            claim,
            decision,
            next_target,
            copies,
            validation,
        ),
        encoding="utf-8",
    )

    if not validation_pass(VALIDATION):
        raise SystemExit(f"2233 validation failed: {VALIDATION}")


if __name__ == "__main__":
    main()
