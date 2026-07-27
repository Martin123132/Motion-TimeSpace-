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
DOC = ROOT / "2240-Y5-R2FR-RAB-parent-protection-contract-or-live-finite-ZR-source-acquisition.md"
BRANCH_ID = "MTS_R2FR_PARENT_QLOC_RAB_PROTECTION_CONTRACT_OR_SOURCE_ACQ_2240"
START_TS = datetime.now(timezone.utc).timestamp()


SOURCE_FILES = {
    "2239_doc": ROOT / "2239-Y5-R2FR-RAB-source-boundary-readout-protection-or-finite-ZR-validator.md",
    "2239_validation": OUT / "P8_Y5_BRR545_2239_VALIDATION.csv",
    "2239_decision": OUT / "P8_Y5_PARENT_QLOC_2239_DECISION_LEDGER.csv",
    "2239_protection": OUT / "P8_Y5_PARENT_QLOC_2239_PROTECTION_PROOF_AUDIT.csv",
    "2239_joint": OUT / "P8_Y5_PARENT_QLOC_2239_JB_READOUT_OPERATOR_JOINT_GATE.csv",
    "2239_validator": OUT / "P8_Y5_PARENT_QLOC_2239_FINITE_ZR_VALIDATOR_SUMMARY.csv",
    "1567_doc": ROOT / "1567-Y5-RAB-parent-protection-contract-or-live-finite-ZR-source-acquisition.md",
    "1567_validation": OUT / "P8_Y5_BRR545_1567_VALIDATION.csv",
    "1567_source": OUT / "P8_Y5_PARENT_QLOC_1567_SOURCE_REGISTER.csv",
    "1567_web": OUT / "P8_Y5_PARENT_QLOC_1567_WEB_SOURCE_REGISTER.csv",
    "1567_contract": OUT / "P8_Y5_PARENT_QLOC_1567_PARENT_PROTECTION_CONTRACT.csv",
    "1567_audit": OUT / "P8_Y5_PARENT_QLOC_1567_CONTRACT_PROOF_AUDIT.csv",
    "1567_theorem": OUT / "P8_Y5_PARENT_QLOC_1567_CONDITIONAL_THEOREM.csv",
    "1567_acquisition": OUT / "P8_Y5_PARENT_QLOC_1567_LIVE_SOURCE_ACQUISITION_QUEUE.csv",
    "1567_runner": OUT / "P8_Y5_PARENT_QLOC_1567_RUNNER_NONCLAIM.csv",
    "1567_claim": OUT / "P8_Y5_PARENT_QLOC_1567_CLAIM_GATE.csv",
    "1567_decision": OUT / "P8_Y5_PARENT_QLOC_1567_DECISION.csv",
    "1567_next": OUT / "P8_Y5_PARENT_QLOC_1567_NEXT_TARGET.csv",
}


SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_2240_SOURCE_REGISTER.csv"
WEB_SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_2240_WEB_SOURCE_REGISTER.csv"
PARENT_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_2240_PARENT_PROTECTION_CONTRACT.csv"
CONTRACT_AUDIT = OUT / "P8_Y5_PARENT_QLOC_2240_CONTRACT_PROOF_AUDIT.csv"
CONDITIONAL_THEOREM = OUT / "P8_Y5_PARENT_QLOC_2240_CONDITIONAL_THEOREM.csv"
ACQUISITION_QUEUE = OUT / "P8_Y5_PARENT_QLOC_2240_LIVE_SOURCE_ACQUISITION_QUEUE.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_2240_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_2240_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_2240_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_2240_NEXT_TARGET.csv"
BRANCH_COPIES = OUT / "P8_Y5_PARENT_QLOC_2240_BRANCH_COPIES.csv"
VALIDATION = OUT / "P8_Y5_BRR545_2240_VALIDATION.csv"


COPY_TARGETS = {
    "queue": QUEUE / "JR2240_PARENT_CONTRACT_OR_SOURCE_ACQ_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "parent_contract_or_source_acq_nonclaim_2240.csv",
    "beta_docs": BETA_DOCS / "PARENT_CONTRACT_OR_SOURCE_ACQ_2240_NONCLAIM.csv",
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
        "1568-Y5-RAB-parent-contract-derivation-from-MTS-primitives-or-first-live-ZR-row.md",
        "2241-Y5-R2FR-RAB-parent-contract-derivation-from-MTS-primitives-or-first-live-ZR-row.md",
    ),
    (
        "scripts/Y5_RAB_parent_protection_contract_or_live_finite_ZR_source_acquisition.py",
        "scripts/Y5_R2FR_RAB_parent_protection_contract_or_live_finite_ZR_source_acquisition_2240.py",
    ),
    (
        "scripts/Y5_RAB_parent_contract_derivation_from_MTS_primitives_or_first_live_ZR_row.py",
        "scripts/Y5_R2FR_RAB_parent_contract_derivation_from_MTS_primitives_or_first_live_ZR_row_2241.py",
    ),
    (
        "NEXT_1568_PARENT_CONTRACT_DERIVATION_FROM_MTS_PRIMITIVES_OR_FIRST_LIVE_ZR_ROW",
        "NEXT_2241_PARENT_CONTRACT_DERIVATION_FROM_MTS_PRIMITIVES_OR_FIRST_LIVE_ZR_ROW",
    ),
    ("P8_Y5_BRR545_1566", "P8_Y5_BRR545_2239"),
    ("P8_Y5_PARENT_QLOC_1566_DECISION.csv", "P8_Y5_PARENT_QLOC_2239_DECISION_LEDGER.csv"),
    ("P8_Y5_PARENT_QLOC_1566_", "P8_Y5_PARENT_QLOC_2239_"),
    ("P8_Y5_PARENT_QLOC_1565_", "P8_Y5_PARENT_QLOC_2238_"),
    ("P8_Y5_PARENT_QLOC_1563_", "P8_Y5_PARENT_QLOC_2236_"),
    ("P8_Y5_PARENT_QLOC_1562_", "P8_Y5_PARENT_QLOC_2235_"),
    ("NEXT_1568", "NEXT_2241"),
    ("NEXT1567", "NEXT2240"),
    ("SRC1567", "SRC2240"),
    ("WEB1567", "WEB2240"),
    ("CON1567", "CON2240"),
    ("AUD1567", "AUD2240"),
    ("THM1567", "THM2240"),
    ("ACQ1567", "ACQ2240"),
    ("ZR1567", "ZR2240"),
    ("RUN1567", "RUN2240"),
    ("GATE1567", "GATE2240"),
    ("DEC1567", "DEC2240"),
    ("VAL1567", "VAL2240"),
]


GENERATED = [
    SOURCE_REGISTER,
    WEB_SOURCE_REGISTER,
    PARENT_CONTRACT,
    CONTRACT_AUDIT,
    CONDITIONAL_THEOREM,
    ACQUISITION_QUEUE,
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


def formalization_2240_artifacts_absent() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(
        path.is_file()
        and "2240" in path.name
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
        role = "current R2FR protection validator handoff" if key.startswith("2239") else "older parent-contract/source-acquisition evidence"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC2240_{index}_{key}",
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


def web_queue_nonclaim() -> bool:
    rows = read_csv(WEB_SOURCE_REGISTER)
    return bool(rows) and all(
        row.get("url", "").startswith("http")
        and row.get("local_copy_path") == "NOT_DOWNLOADED_THIS_CHECKPOINT"
        and row.get("row_status") == "EXTERNAL_ARENA_SOURCE_CANDIDATE_NONCLAIM"
        for row in rows
    )


def acquisition_queue_nonready() -> bool:
    rows = read_csv(ACQUISITION_QUEUE)
    return bool(rows) and all(
        row.get("ready_for_raw") == "False"
        and row.get("ready_for_accepted") == "False"
        and row.get("current_status", "").startswith("MISSING_")
        for row in rows
    )


def copy_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, target in COPY_TARGETS.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ACQUISITION_QUEUE, target)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": copy_id,
                "source_path": rel(ACQUISITION_QUEUE),
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
    web: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    acquisition: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    claim: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 2240 - Y5/R2FR R_AB Parent Protection Contract or Live Finite Z_R Source Acquisition",
            "## Verdict\n"
            "- 2240 imports the old `1567` parent-protection/source-acquisition checkpoint into the current R2FR chain after `2239` installed the hard finite-residual validator.\n"
            "- The single parent-protection contract is now explicit: typed parent sorts, action-image exhaustion, matter descent, boundary descent, readout closure, and operator exclusion must close together.\n"
            "- If that contract is parent-signed, the second-class route kills `J_R`, `B_R`, `readout_regen`, and `Z_R` without a plateau axiom.\n"
            "- It is not signed from MTS primitives yet, so no `Z_R=0`, `q_R=0`, local GR/Newton, R10, PPN, WEP, clock, or orbital claim is made.\n"
            "- The fallback is live but nonclaim: internal coefficient targets are separated from external arena-bound sources, with no raw/accepted score row ready.",
            "## Source Register\n"
            + md_table(source, ["source_id", "source_path", "path_exists", "validation_overall_pass", "role"]),
            "## External Arena Source Queue\n"
            + md_table(web, ["source_id", "arena", "url", "description", "use_for", "local_copy_path", "row_status"]),
            "## Parent Protection Contract\n"
            + md_table(contract, ["contract_id", "contract_clause", "effect_if_signed", "current_status", "missing_for_claim"]),
            "## Contract Proof Audit\n"
            + md_table(audit, ["audit_id", "target_zero", "required_contract_clause", "current_status", "fallback"]),
            "## Conditional Theorem\n"
            + md_table(theorem, ["theorem_id", "statement", "calculation_or_role", "status", "why_not_claimed"]),
            "## Live Source Acquisition Queue\n"
            + md_table(acquisition, ["acquisition_id", "source_class", "target", "needed_evidence", "preferred_source_kind", "arena_projection", "current_status", "ready_for_raw", "ready_for_accepted"]),
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
            "This is a clean fork in the road, not a failure. The theorem route now has a single contract to derive from motion/time/space primitives. The empirical fallback now has a source acquisition queue that refuses to score placeholders. Next we either derive the contract from primitives or fill the first source-backed finite/theorem-zero row without moving it to accepted.",
            "",
        ]
    )


def validation_rows(generated_paths: list[Path]) -> list[dict[str, Any]]:
    contract = read_csv(PARENT_CONTRACT)
    audit = read_csv(CONTRACT_AUDIT)
    theorem = read_csv(CONDITIONAL_THEOREM)
    runner = read_csv(RUNNER)
    claim = read_csv(CLAIM_GATE)
    decision = read_csv(DECISION)
    next_target = read_csv(NEXT_TARGET)
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2240_00_sources_exist",
            "result": "PASS" if all(path.exists() for path in SOURCE_FILES.values()) and source_register_paths_exist() else "FAIL",
            "detail": "all direct and registered 2240 source paths exist",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2240_01_prior_validations",
            "result": "PASS" if validation_pass(SOURCE_FILES["2239_validation"]) and validation_pass(SOURCE_FILES["1567_validation"]) else "FAIL",
            "detail": "2239 and 1567 validations pass overall",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2240_02_web_sources_queued",
            "result": "PASS" if web_queue_nonclaim() else "FAIL",
            "detail": "external arena source URLs queued nonclaim and not treated as downloaded evidence",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2240_03_contract_written",
            "result": "PASS" if any(row.get("current_status") == "CONTRACT_WRITTEN_NOT_SIGNED" for row in contract) else "FAIL",
            "detail": "joint parent protection contract is written but unsigned",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2240_04_audit_failed_parent_proof",
            "result": "PASS" if any(row.get("current_status") == "FAILED_CURRENT_PARENT_PROOF" for row in audit) else "FAIL",
            "detail": "contract audit refuses parent proof",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2240_05_conditional_theorem",
            "result": "PASS" if any(row.get("status") == "EXACT_IF_CONTRACT_PARENT_SIGNED" for row in theorem) else "FAIL",
            "detail": "conditional theorem is explicit",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2240_06_acquisition_queue",
            "result": "PASS" if acquisition_queue_nonready() else "FAIL",
            "detail": "live acquisition queue exists but is not raw/accepted-ready",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2240_07_runner_blocks_claim",
            "result": "PASS" if any(row.get("current_status") == "BLOCKED_NO_CLAIM" for row in runner) else "FAIL",
            "detail": "runner blocks local claim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2240_08_claim_gates",
            "result": "PASS" if all("BLOCKED" in row.get("status", "") or row.get("status", "").startswith("PASS_SOURCE_QUEUE_NONCLAIM") for row in claim) else "FAIL",
            "detail": "claim gates remain closed except nonclaim source queue",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2240_09_path_fields",
            "result": "PASS"
            if delimited_paths_exist([PARENT_CONTRACT, CONTRACT_AUDIT, CONDITIONAL_THEOREM, CLAIM_GATE], ["source_paths"])
            else "FAIL",
            "detail": "source path fields resolve locally",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2240_10_decision_next",
            "result": "PASS"
            if any(row.get("result") == "NEXT_2241_PARENT_CONTRACT_DERIVATION_FROM_MTS_PRIMITIVES_OR_FIRST_LIVE_ZR_ROW" for row in decision)
            else "FAIL",
            "detail": "decision selects parent derivation or first live finite row",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2240_11_next_target",
            "result": "PASS" if next_target[0]["next_target"].startswith("2241-Y5-R2FR-RAB-parent-contract-derivation") else "FAIL",
            "detail": "next target is current-numbered parent contract derivation or first live row",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2240_12_csv_parse",
            "result": "PASS" if all(parse_csv(path) for path in generated_paths) else "FAIL",
            "detail": "all generated 2240 CSVs parse cleanly",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2240_13_claim_flags_false",
            "result": "PASS" if generated_flags_false(generated_paths) else "FAIL",
            "detail": "all generated prediction/claim flags remain false",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2240_14_branch_copies",
            "result": "PASS" if all(row["copied"] == "True" and row["parse_ok"] == "True" for row in read_csv(BRANCH_COPIES)) else "FAIL",
            "detail": "branch/quarantine nonclaim copies written",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2240_15_pycache_absent",
            "result": "PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after run",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2240_16_formalization_no_2240",
            "result": "PASS" if formalization_2240_artifacts_absent() else "FAIL",
            "detail": "formalization-workbench has no non-venv 2240 artifacts",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2240_17_formalization_untouched",
            "result": "PASS" if formalization_untouched_since_start() else "FAIL",
            "detail": "formalization-workbench untouched during 2240 run",
        },
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2240_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2240 writes the parent protection contract, keeps the exact theorem conditional, starts nonclaim finite-source acquisition, and selects primitive derivation or first live row next",
        }
    )
    return rows


def main() -> None:
    source = source_rows()
    web = transform_old_csv(SOURCE_FILES["1567_web"])
    contract = transform_old_csv(SOURCE_FILES["1567_contract"])
    audit = transform_old_csv(SOURCE_FILES["1567_audit"])
    theorem = transform_old_csv(SOURCE_FILES["1567_theorem"])
    acquisition = transform_old_csv(SOURCE_FILES["1567_acquisition"])
    runner = transform_old_csv(SOURCE_FILES["1567_runner"])
    claim = transform_old_csv(SOURCE_FILES["1567_claim"])
    decision = transform_old_csv(SOURCE_FILES["1567_decision"])
    next_target = transform_old_csv(SOURCE_FILES["1567_next"])

    write_csv(SOURCE_REGISTER, source)
    write_csv(WEB_SOURCE_REGISTER, web)
    write_csv(PARENT_CONTRACT, contract)
    write_csv(CONTRACT_AUDIT, audit)
    write_csv(CONDITIONAL_THEOREM, theorem)
    write_csv(ACQUISITION_QUEUE, acquisition)
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
            web,
            contract,
            audit,
            theorem,
            acquisition,
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
        raise SystemExit(f"2240 validation failed: {VALIDATION}")


if __name__ == "__main__":
    main()
