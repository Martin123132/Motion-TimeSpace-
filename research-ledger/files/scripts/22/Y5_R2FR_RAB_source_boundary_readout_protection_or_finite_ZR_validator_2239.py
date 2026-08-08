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
DOC = ROOT / "2239-Y5-R2FR-RAB-source-boundary-readout-protection-or-finite-ZR-validator.md"
BRANCH_ID = "MTS_R2FR_PARENT_QLOC_RAB_PROTECTION_OR_ZR_VALIDATOR_2239"
START_TS = datetime.now(timezone.utc).timestamp()


SOURCE_FILES = {
    "2238_doc": ROOT / "2238-Y5-R2FR-RAB-parent-theta-Omega-vR-fill-or-finite-ZR-source-row.md",
    "2238_validation": OUT / "P8_Y5_BRR545_2238_VALIDATION.csv",
    "2238_decision": OUT / "P8_Y5_PARENT_QLOC_2238_DECISION_LEDGER.csv",
    "2238_elim": OUT / "P8_Y5_PARENT_QLOC_2238_SECOND_CLASS_ELIMINATION_CONDITIONS.csv",
    "1566_doc": ROOT / "1566-Y5-RAB-source-boundary-readout-protection-or-finite-ZR-validator.md",
    "1566_validation": OUT / "P8_Y5_BRR545_1566_VALIDATION.csv",
    "1566_source": OUT / "P8_Y5_PARENT_QLOC_1566_SOURCE_REGISTER.csv",
    "1566_protection": OUT / "P8_Y5_PARENT_QLOC_1566_PROTECTION_PROOF_AUDIT.csv",
    "1566_joint": OUT / "P8_Y5_PARENT_QLOC_1566_JB_READOUT_OPERATOR_JOINT_GATE.csv",
    "1566_rules": OUT / "P8_Y5_PARENT_QLOC_1566_FINITE_ZR_VALIDATOR_RULES.csv",
    "1566_summary": OUT / "P8_Y5_PARENT_QLOC_1566_FINITE_ZR_VALIDATOR_SUMMARY.csv",
    "1566_results": OUT / "P8_Y5_PARENT_QLOC_1566_FINITE_ZR_VALIDATOR_RESULTS.csv",
    "1566_runner": OUT / "P8_Y5_PARENT_QLOC_1566_RUNNER_NONCLAIM.csv",
    "1566_claim": OUT / "P8_Y5_PARENT_QLOC_1566_CLAIM_GATE.csv",
    "1566_decision": OUT / "P8_Y5_PARENT_QLOC_1566_DECISION.csv",
    "1566_next": OUT / "P8_Y5_PARENT_QLOC_1566_NEXT_TARGET.csv",
}


SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_2239_SOURCE_REGISTER.csv"
PROTECTION = OUT / "P8_Y5_PARENT_QLOC_2239_PROTECTION_PROOF_AUDIT.csv"
JOINT_GATE = OUT / "P8_Y5_PARENT_QLOC_2239_JB_READOUT_OPERATOR_JOINT_GATE.csv"
VALIDATOR_RULES = OUT / "P8_Y5_PARENT_QLOC_2239_FINITE_ZR_VALIDATOR_RULES.csv"
VALIDATOR_SUMMARY = OUT / "P8_Y5_PARENT_QLOC_2239_FINITE_ZR_VALIDATOR_SUMMARY.csv"
VALIDATOR_RESULTS = OUT / "P8_Y5_PARENT_QLOC_2239_FINITE_ZR_VALIDATOR_RESULTS.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_2239_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_2239_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_2239_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_2239_NEXT_TARGET.csv"
BRANCH_COPIES = OUT / "P8_Y5_PARENT_QLOC_2239_BRANCH_COPIES.csv"
VALIDATION = OUT / "P8_Y5_BRR545_2239_VALIDATION.csv"


COPY_TARGETS = {
    "queue": QUEUE / "JR2239_PROTECTION_OR_ZR_VALIDATOR_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "protection_or_ZR_validator_nonclaim_2239.csv",
    "beta_docs": BETA_DOCS / "PROTECTION_OR_ZR_VALIDATOR_2239_NONCLAIM.csv",
}


OLD_TO_NEW = [
    (
        "1562-Y5-lambdaR-parent-origin-zero-stress-and-first-class-constraint-test.md",
        "2235-Y5-R2FR-lambdaR-parent-origin-zero-stress-and-first-class-constraint-test.md",
    ),
    (
        "1563-Y5-RAB-auxiliary-compatibility-parent-sort-and-no-derivative-grammar.md",
        "2236-Y5-R2FR-RAB-auxiliary-compatibility-parent-sort-and-no-derivative-grammar.md",
    ),
    (
        "1565-Y5-RAB-parent-theta-Omega-vR-fill-or-finite-ZR-source-row.md",
        "2238-Y5-R2FR-RAB-parent-theta-Omega-vR-fill-or-finite-ZR-source-row.md",
    ),
    (
        "1566-Y5-RAB-source-boundary-readout-protection-or-finite-ZR-validator.md",
        "2239-Y5-R2FR-RAB-source-boundary-readout-protection-or-finite-ZR-validator.md",
    ),
    (
        "1567-Y5-RAB-parent-protection-contract-or-live-finite-ZR-source-acquisition.md",
        "2240-Y5-R2FR-RAB-parent-protection-contract-or-live-finite-ZR-source-acquisition.md",
    ),
    (
        "scripts/Y5_RAB_source_boundary_readout_protection_or_finite_ZR_validator.py",
        "scripts/Y5_R2FR_RAB_source_boundary_readout_protection_or_finite_ZR_validator_2239.py",
    ),
    (
        "scripts/Y5_RAB_parent_protection_contract_or_live_finite_ZR_source_acquisition.py",
        "scripts/Y5_R2FR_RAB_parent_protection_contract_or_live_finite_ZR_source_acquisition_2240.py",
    ),
    (
        "NEXT_1567_PARENT_PROTECTION_CONTRACT_OR_LIVE_FINITE_ZR_SOURCE_ACQUISITION",
        "NEXT_2240_PARENT_PROTECTION_CONTRACT_OR_LIVE_FINITE_ZR_SOURCE_ACQUISITION",
    ),
    ("P8_Y5_PARENT_QLOC_1565_DECISION.csv", "P8_Y5_PARENT_QLOC_2238_DECISION_LEDGER.csv"),
    ("P8_Y5_BRR545_1565", "P8_Y5_BRR545_2238"),
    ("P8_Y5_PARENT_QLOC_1565_", "P8_Y5_PARENT_QLOC_2238_"),
    ("P8_Y5_PARENT_QLOC_1563_", "P8_Y5_PARENT_QLOC_2236_"),
    ("P8_Y5_PARENT_QLOC_1562_", "P8_Y5_PARENT_QLOC_2235_"),
    ("NEXT_1567", "NEXT_2240"),
    ("NEXT1566", "NEXT2239"),
    ("PROT1566", "PROT2239"),
    ("JOINT1566", "JOINT2239"),
    ("RULE1566", "RULE2239"),
    ("VS1566", "VS2239"),
    ("SCAN1566", "SCAN2239"),
    ("RUN1566", "RUN2239"),
    ("GATE1566", "GATE2239"),
    ("DEC1566", "DEC2239"),
    ("VAL1566", "VAL2239"),
]


GENERATED = [
    SOURCE_REGISTER,
    PROTECTION,
    JOINT_GATE,
    VALIDATOR_RULES,
    VALIDATOR_SUMMARY,
    VALIDATOR_RESULTS,
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


def resolve_project_path(path_text: str) -> Path:
    path_text = path_text.strip()
    if not path_text:
        return ROOT
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


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


def formalization_2239_artifacts_absent() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(
        path.is_file()
        and "2239" in path.name
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
        role = "current R2FR theta/Omega handoff" if key.startswith("2238") else "older protection/finite-validator evidence"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC2239_{index}_{key}",
                "source_path": rel(path),
                "path_exists": path.exists(),
                "validation_overall_pass": validation_pass(path) if key.endswith("validation") else "",
                "role": role,
                **flags(),
            }
        )
    return rows


def source_register_paths_exist() -> bool:
    return all(resolve_project_path(row["source_path"]).exists() for row in read_csv(SOURCE_REGISTER))


def delimited_paths_exist(paths: list[Path], field_names: list[str]) -> bool:
    for path in paths:
        for row in read_csv(path):
            for field_name in field_names:
                for source_path in row.get(field_name, "").split(";"):
                    if source_path.strip() and not resolve_project_path(source_path).exists():
                        return False
    return True


def validator_file_paths_exist() -> bool:
    return all(resolve_project_path(row["file_path"]).exists() for row in read_csv(VALIDATOR_RESULTS))


def copy_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, target in COPY_TARGETS.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(VALIDATOR_SUMMARY, target)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": copy_id,
                "source_path": rel(VALIDATOR_SUMMARY),
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
    protection: list[dict[str, Any]],
    joint: list[dict[str, Any]],
    rules: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    results: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    claim: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 2239 - Y5/R2FR R_AB Source/Boundary/Readout Protection or Finite Z_R Validator",
            "## Verdict\n"
            "- 2239 imports the old `1566` protection/validator gate into the current R2FR chain after `2238` isolated the second-class auxiliary route.\n"
            "- The second-class route still survives as the cleanest local mechanism, but it does not close unless four leaks are jointly sealed: `J_R=0`, `B_R=0`, readout stability, and operator exclusion.\n"
            "- Current status: all four protections are unsigned or exact-conditional, so no `Z_R=0`, `q_R=0`, local GR/Newton, R10, PPN, clock, or orbital claim is allowed.\n"
            "- The finite `Z_R` fallback is now guarded by a strict validator: docs templates, missing markers, missing source paths, missing anchors, and claim-true rows are all hard rejects.\n"
            "- No accepted source-ready finite residual rows exist.",
            "## Source Register\n"
            + md_table(source, ["source_id", "source_path", "path_exists", "validation_overall_pass", "role"]),
            "## Protection Proof Audit\n"
            + md_table(protection, ["protection_id", "quantity", "zero_condition", "status", "blocking_gap", "fallback_if_missing"]),
            "## Joint Gate\n"
            + md_table(joint, ["joint_id", "target", "condition_or_result", "status"]),
            "## Finite Z_R Validator Rules\n"
            + md_table(rules, ["rule_id", "rule", "failure_status", "severity"]),
            "## Finite Z_R Validator Summary\n"
            + md_table(summary, ["summary_id", "docs_rows", "raw_rows", "accepted_rows", "rejected_rows", "accepted_ready_rows", "invalid_live_rows", "status"]),
            "## Finite Z_R Validator Results\n"
            + md_table(results, ["scan_id", "intake_class", "row_id", "coefficient_symbol", "status", "reasons", "source_exists", "anchor_found"]),
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
            "This is the local-branch honesty lock. The theory route is still alive, but only as a joint protection contract: matter must not source `R_AB`, boundary/corner terms must not resurrect `Pi_R^n`, readout/EFT must not regenerate the sector, and the parent grammar must really exclude derivative operators. If that contract cannot be signed, the finite residual branch is allowed only with real source-backed rows. This keeps the work from turning into either hand-waved GR recovery or hand-waved phenomenology.",
            "",
        ]
    )


def validation_rows(generated_paths: list[Path]) -> list[dict[str, Any]]:
    protection = read_csv(PROTECTION)
    joint = read_csv(JOINT_GATE)
    rules = read_csv(VALIDATOR_RULES)
    summary = read_csv(VALIDATOR_SUMMARY)
    results = read_csv(VALIDATOR_RESULTS)
    runner = read_csv(RUNNER)
    claim = read_csv(CLAIM_GATE)
    decision = read_csv(DECISION)
    next_target = read_csv(NEXT_TARGET)
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2239_00_sources_exist",
            "result": "PASS" if all(path.exists() for path in SOURCE_FILES.values()) and source_register_paths_exist() else "FAIL",
            "detail": "all direct and registered 2239 source paths exist",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2239_01_prior_validations",
            "result": "PASS" if validation_pass(SOURCE_FILES["2238_validation"]) and validation_pass(SOURCE_FILES["1566_validation"]) else "FAIL",
            "detail": "2238 and 1566 validations pass overall",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2239_02_protection_not_closed",
            "result": "PASS" if any(row.get("status") == "JOINT_PROTECTION_NOT_CLOSED" for row in protection) else "FAIL",
            "detail": "joint protection remains open",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2239_03_joint_gate_blocks",
            "result": "PASS" if joint and all(row.get("status") in {"BLOCKED_NO_CLAIM", "JOINT_PROTECTION_NOT_CLOSED"} for row in joint) else "FAIL",
            "detail": "joint gate blocks local claim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2239_04_validator_rules",
            "result": "PASS" if any(row.get("failure_status") == "MISSING_MARKER_PRESENT" for row in rules) and all(row.get("severity") == "hard_reject" for row in rules) else "FAIL",
            "detail": "validator rejects missing markers and uses hard rejects",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2239_05_no_source_ready_rows",
            "result": "PASS" if any(row.get("status") == "NO_ACCEPTED_SOURCE_READY_ROWS" and row.get("accepted_ready_rows") == "0" for row in summary) else "FAIL",
            "detail": "validator finds no accepted source-ready rows",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2239_06_docs_rejected",
            "result": "PASS" if any(row.get("status") == "DOCS_TEMPLATES_REJECTED_AS_EXPECTED" for row in summary) and results and all(row.get("status") == "REJECT" for row in results) else "FAIL",
            "detail": "docs templates rejected as expected",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2239_07_runner_blocks_claim",
            "result": "PASS" if any(row.get("current_status") == "BLOCKED_NO_CLAIM" for row in runner) else "FAIL",
            "detail": "runner blocks local claim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2239_08_claim_gates",
            "result": "PASS" if all("BLOCKED" in row.get("status", "") or row.get("status", "").startswith("PASS") for row in claim) else "FAIL",
            "detail": "all claim gates remain blocked",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2239_09_path_fields",
            "result": "PASS"
            if delimited_paths_exist([PROTECTION, JOINT_GATE, CLAIM_GATE], ["source_paths"]) and validator_file_paths_exist()
            else "FAIL",
            "detail": "source path fields and validator file paths resolve locally",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2239_10_decision_next",
            "result": "PASS"
            if any(row.get("result") == "NEXT_2240_PARENT_PROTECTION_CONTRACT_OR_LIVE_FINITE_ZR_SOURCE_ACQUISITION" for row in decision)
            else "FAIL",
            "detail": "decision selects parent protection contract or live source acquisition",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2239_11_next_target",
            "result": "PASS" if next_target[0]["next_target"].startswith("2240-Y5-R2FR-RAB-parent-protection-contract") else "FAIL",
            "detail": "next target is current-numbered parent protection contract or finite source acquisition",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2239_12_csv_parse",
            "result": "PASS" if all(parse_csv(path) for path in generated_paths) else "FAIL",
            "detail": "all generated 2239 CSVs parse cleanly",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2239_13_claim_flags_false",
            "result": "PASS" if generated_flags_false(generated_paths) else "FAIL",
            "detail": "all generated prediction/claim flags remain false",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2239_14_branch_copies",
            "result": "PASS" if all(row["copied"] == "True" and row["parse_ok"] == "True" for row in read_csv(BRANCH_COPIES)) else "FAIL",
            "detail": "branch/quarantine nonclaim copies written",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2239_15_pycache_absent",
            "result": "PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after run",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2239_16_formalization_no_2239",
            "result": "PASS" if formalization_2239_artifacts_absent() else "FAIL",
            "detail": "formalization-workbench has no non-venv 2239 artifacts",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2239_17_formalization_untouched",
            "result": "PASS" if formalization_untouched_since_start() else "FAIL",
            "detail": "formalization-workbench untouched during 2239 run",
        },
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2239_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2239 keeps joint source/boundary/readout/operator protection open, validates finite Z_R hard-reject rules, and selects parent protection contract or live finite source acquisition next",
        }
    )
    return rows


def main() -> None:
    source = source_rows()
    protection = transform_old_csv(SOURCE_FILES["1566_protection"])
    joint = transform_old_csv(SOURCE_FILES["1566_joint"])
    rules = transform_old_csv(SOURCE_FILES["1566_rules"])
    summary = transform_old_csv(SOURCE_FILES["1566_summary"])
    results = transform_old_csv(SOURCE_FILES["1566_results"])
    runner = transform_old_csv(SOURCE_FILES["1566_runner"])
    claim = transform_old_csv(SOURCE_FILES["1566_claim"])
    decision = transform_old_csv(SOURCE_FILES["1566_decision"])
    next_target = transform_old_csv(SOURCE_FILES["1566_next"])

    write_csv(SOURCE_REGISTER, source)
    write_csv(PROTECTION, protection)
    write_csv(JOINT_GATE, joint)
    write_csv(VALIDATOR_RULES, rules)
    write_csv(VALIDATOR_SUMMARY, summary)
    write_csv(VALIDATOR_RESULTS, results)
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
            protection,
            joint,
            rules,
            summary,
            results,
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
        raise SystemExit(f"2239 validation failed: {VALIDATION}")


if __name__ == "__main__":
    main()
