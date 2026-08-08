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
DOC = ROOT / "2234-Y5-R2FR-minimal-parent-weak-field-action-ansatz-and-Euler-Ward-PPN-gate.md"
BRANCH_ID = "MTS_R2FR_PARENT_QLOC_MINIMAL_ACTION_ANSATZ_2234"
START_TS = datetime.now(timezone.utc).timestamp()


SOURCE_FILES = {
    "2233_doc": ROOT / "2233-Y5-R2FR-parent-weak-field-zero-condition-derivation-or-demotion.md",
    "2233_validation": OUT / "P8_Y5_BRR545_2233_VALIDATION.csv",
    "2233_next": OUT / "P8_Y5_PARENT_QLOC_2233_NEXT_TARGET.csv",
    "1561_doc": ROOT / "1561-Y5-minimal-parent-weak-field-action-ansatz-and-Euler-Ward-PPN-gate.md",
    "1561_validation": OUT / "P8_Y5_BRR545_1561_VALIDATION.csv",
    "1561_source": OUT / "P8_Y5_PARENT_QLOC_1561_SOURCE_REGISTER.csv",
    "1561_ansatz": OUT / "P8_Y5_PARENT_QLOC_1561_MINIMAL_ACTION_ANSATZ_REGISTER.csv",
    "1561_euler": OUT / "P8_Y5_PARENT_QLOC_1561_EULER_VARIATION_GATE.csv",
    "1561_ward": OUT / "P8_Y5_PARENT_QLOC_1561_WARD_PPN_GATE.csv",
    "1561_adoption": OUT / "P8_Y5_PARENT_QLOC_1561_ADOPTION_REJECTION_LEDGER.csv",
    "1561_runner": OUT / "P8_Y5_PARENT_QLOC_1561_RUNNER_NONCLAIM.csv",
    "1561_claim": OUT / "P8_Y5_PARENT_QLOC_1561_CLAIM_GATE.csv",
    "1561_decision": OUT / "P8_Y5_PARENT_QLOC_1561_DECISION.csv",
    "1561_next": OUT / "P8_Y5_PARENT_QLOC_1561_NEXT_TARGET.csv",
}


SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_2234_SOURCE_REGISTER.csv"
ANSATZ = OUT / "P8_Y5_PARENT_QLOC_2234_MINIMAL_ACTION_ANSATZ_REGISTER.csv"
EULER = OUT / "P8_Y5_PARENT_QLOC_2234_EULER_VARIATION_GATE.csv"
WARD = OUT / "P8_Y5_PARENT_QLOC_2234_WARD_PPN_GATE.csv"
ADOPTION = OUT / "P8_Y5_PARENT_QLOC_2234_ADOPTION_REJECTION_LEDGER.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_2234_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_2234_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_2234_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_2234_NEXT_TARGET.csv"
BRANCH_COPIES = OUT / "P8_Y5_PARENT_QLOC_2234_BRANCH_COPIES.csv"
VALIDATION = OUT / "P8_Y5_BRR545_2234_VALIDATION.csv"


COPY_TARGETS = {
    "queue": QUEUE / "JR2234_MINIMAL_ACTION_ANSATZ_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "minimal_action_ansatz_nonclaim_2234.csv",
    "beta_docs": BETA_DOCS / "MINIMAL_ACTION_ANSATZ_2234_NONCLAIM.csv",
}


OLD_TO_NEW = [
    (
        "1562-Y5-lambdaR-parent-origin-zero-stress-and-first-class-constraint-test.md",
        "2235-Y5-R2FR-lambdaR-parent-origin-zero-stress-and-first-class-constraint-test.md",
    ),
    (
        "scripts/Y5_lambdaR_parent_origin_zero_stress_and_first_class_constraint_test.py",
        "scripts/Y5_R2FR_lambdaR_parent_origin_zero_stress_and_first_class_constraint_test_2235.py",
    ),
    ("NEXT_1562_LAMBDAR_PARENT_ORIGIN_ZERO_STRESS_TEST", "NEXT_2235_LAMBDAR_PARENT_ORIGIN_ZERO_STRESS_TEST"),
    ("NEXT_1562", "NEXT_2235"),
    ("1562", "2235"),
    ("1561", "2234"),
    ("1560", "2233"),
    ("1559", "2232"),
    ("1558", "2231"),
]


GENERATED = [
    SOURCE_REGISTER,
    ANSATZ,
    EULER,
    WARD,
    ADOPTION,
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


def formalization_2234_artifacts_absent() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(
        path.is_file()
        and "2234" in path.name
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
        role = "current R2FR weak-field zero-condition handoff" if key.startswith("2233") else "older action-ansatz evidence"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC2234_{index}_{key}",
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


def table_source_paths_exist(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            for source_path in row.get("source_paths", "").split(";"):
                if source_path.strip() and not resolve_project_path(source_path).exists():
                    return False
    return True


def claim_source_paths_exist() -> bool:
    for row in read_csv(CLAIM_GATE):
        for source_path in row.get("source_paths", "").split(";"):
            if source_path.strip() and not resolve_project_path(source_path).exists():
                return False
    return True


def copy_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, target in COPY_TARGETS.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ADOPTION, target)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": copy_id,
                "source_path": rel(ADOPTION),
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
    ansatz: list[dict[str, Any]],
    euler: list[dict[str, Any]],
    ward: list[dict[str, Any]],
    adoption: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    claim: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 2234 - Y5/R2FR Minimal Parent Weak-Field Action Ansatz and Euler/Ward/PPN Gate",
            "## Verdict\n"
            "- 2234 imports the old `1561` minimal parent weak-field action ansatz into the current R2FR line after the `2233` zero-condition demotion.\n"
            "- The cleanest conditional repair remains `S_EH[g_obs] + S_matter[g_obs, psi] + int sqrt(-g) lambda_R R_AB + S_silent[Phi,g_obs] + S_boundary`.\n"
            "- The ansatz is useful because `delta lambda_R` formally gives `R_AB=0`, and the EH weak-field core can give the `beta=1` local PPN limit once source/readout ownership is signed.\n"
            "- The ansatz is not adopted as MTS parent theory: `lambda_R` still lacks parent origin, zero-stress/reaction-stress proof, symbol matching, source charge ownership, boundary current ownership, and extra-sector silence.\n"
            "- Therefore local GR/Newton recovery remains a bounded-closure control lane, not a derived claim.\n"
            "- Next target is the narrow `lambda_R` origin/zero-stress/first-class constraint test.",
            "## Source Register\n"
            + md_table(source, ["source_id", "source_path", "path_exists", "validation_overall_pass", "role"]),
            "## Minimal Action Ansatz Register\n"
            + md_table(
                ansatz,
                [
                    "ansatz_id",
                    "candidate_parent_action",
                    "what_it_derives_conditionally",
                    "what_blocks_adoption",
                    "adoption_status",
                ],
            ),
            "## Euler Variation Gate\n"
            + md_table(euler, ["gate_id", "variation_test", "conditional_result", "status", "blocking_issue"]),
            "## Ward/PPN Gate\n"
            + md_table(ward, ["gate_id", "ward_or_ppn_test", "conditional_result", "status", "blocking_issue"]),
            "## Adoption/Rejection Ledger\n"
            + md_table(adoption, ["adoption_id", "requirement", "status", "why_it_blocks"]),
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
            "The positive result is structural: there is a compact action ansatz that would make the local GR route mathematically legible. The negative result is just as important: unless `lambda_R` is derived as a parent-owned stress-silent constraint, this is not yet MTS deriving GR; it is a disciplined closure candidate. The next attack should not broaden. It should decide whether `lambda_R R_AB` is a real first-class/auxiliary parent constraint or a hand-inserted local plateau.",
            "",
        ]
    )


def validation_rows(generated_paths: list[Path]) -> list[dict[str, Any]]:
    ansatz = read_csv(ANSATZ)
    euler = read_csv(EULER)
    ward = read_csv(WARD)
    adoption = read_csv(ADOPTION)
    runner = read_csv(RUNNER)
    claim = read_csv(CLAIM_GATE)
    decision = read_csv(DECISION)
    next_target = read_csv(NEXT_TARGET)
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2234_00_sources_exist",
            "result": "PASS" if all(path.exists() for path in SOURCE_FILES.values()) and source_register_paths_exist() else "FAIL",
            "detail": "all direct and registered 2234 source paths exist",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2234_01_prior_validations",
            "result": "PASS" if validation_pass(SOURCE_FILES["2233_validation"]) and validation_pass(SOURCE_FILES["1561_validation"]) else "FAIL",
            "detail": "2233 and 1561 validations pass overall",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2234_02_best_ansatz",
            "result": "PASS" if any(row.get("adoption_status") == "BEST_CONDITIONAL_ANSATZ_NOT_ADOPTED" for row in ansatz) else "FAIL",
            "detail": "best conditional ansatz written but not adopted",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2234_03_lambda_variation",
            "result": "PASS" if any(row.get("status") == "FORMAL_PASS_IF_LAMBDAR_PARENT_OWNED" for row in euler) else "FAIL",
            "detail": "lambda_R variation formal q_R gate recorded",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2234_04_lambda_stress_fails",
            "result": "PASS" if any(row.get("status") == "FAIL_UNSIGNED_STRESS_SILENCE" for row in euler) else "FAIL",
            "detail": "lambda_R stress-silence failure remains explicit",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2234_05_ward_beta_conditional",
            "result": "PASS" if any(row.get("gate_id") == "WPPN2234_2_beta" and row.get("status") == "CONDITIONAL_UNSIGNED" for row in ward) else "FAIL",
            "detail": "beta gate remains conditional unsigned",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2234_06_adoption_blocks",
            "result": "PASS" if any(row.get("status") == "NOT_ADOPTED_CURRENT_MTS_DERIVATION" for row in adoption) else "FAIL",
            "detail": "adoption rejection ledger blocks current MTS derivation",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2234_07_runner_claim_block",
            "result": "PASS" if any(row.get("current_status") == "BLOCKED_NO_CLAIM" for row in runner) else "FAIL",
            "detail": "runner blocks local GR/Newton claim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2234_08_claim_gates",
            "result": "PASS" if all("BLOCKED" in row.get("status", "") or row.get("status", "").startswith("PASS") for row in claim) else "FAIL",
            "detail": "all claim gates remain blocked/nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2234_09_claim_source_paths",
            "result": "PASS" if claim_source_paths_exist() and table_source_paths_exist([ANSATZ, EULER, WARD, ADOPTION]) else "FAIL",
            "detail": "all semicolon-delimited source paths in claim/euler/ward/ansatz/adoption rows resolve locally",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2234_10_decision_next",
            "result": "PASS" if any(row.get("result") == "NEXT_2235_LAMBDAR_PARENT_ORIGIN_ZERO_STRESS_TEST" for row in decision) else "FAIL",
            "detail": "decision selects lambda_R origin/stress test next",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2234_11_next_target",
            "result": "PASS" if next_target[0]["next_target"].startswith("2235-Y5-R2FR-lambdaR-parent-origin-zero-stress") else "FAIL",
            "detail": "next target is current-numbered lambda_R origin zero-stress test",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2234_12_csv_parse",
            "result": "PASS" if all(parse_csv(path) for path in generated_paths) else "FAIL",
            "detail": "all generated 2234 CSVs parse cleanly",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2234_13_claim_flags_false",
            "result": "PASS" if generated_flags_false(generated_paths) else "FAIL",
            "detail": "all generated prediction/claim flags remain false",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2234_14_branch_copies",
            "result": "PASS" if all(row["copied"] == "True" and row["parse_ok"] == "True" for row in read_csv(BRANCH_COPIES)) else "FAIL",
            "detail": "branch/quarantine nonclaim copies written",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2234_15_pycache_absent",
            "result": "PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after run",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2234_16_formalization_no_2234",
            "result": "PASS" if formalization_2234_artifacts_absent() else "FAIL",
            "detail": "formalization-workbench has no non-venv 2234 artifacts",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2234_17_formalization_untouched",
            "result": "PASS" if formalization_untouched_since_start() else "FAIL",
            "detail": "formalization-workbench untouched during 2234 run",
        },
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2234_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2234 imports the minimal action ansatz, keeps it nonclaim, and selects lambda_R parent-origin/zero-stress next",
        }
    )
    return rows


def main() -> None:
    source = source_rows()
    ansatz = transform_old_csv(SOURCE_FILES["1561_ansatz"])
    euler = transform_old_csv(SOURCE_FILES["1561_euler"])
    ward = transform_old_csv(SOURCE_FILES["1561_ward"])
    adoption = transform_old_csv(SOURCE_FILES["1561_adoption"])
    runner = transform_old_csv(SOURCE_FILES["1561_runner"])
    claim = transform_old_csv(SOURCE_FILES["1561_claim"])
    decision = transform_old_csv(SOURCE_FILES["1561_decision"])
    next_target = transform_old_csv(SOURCE_FILES["1561_next"])

    write_csv(SOURCE_REGISTER, source)
    write_csv(ANSATZ, ansatz)
    write_csv(EULER, euler)
    write_csv(WARD, ward)
    write_csv(ADOPTION, adoption)
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
            ansatz,
            euler,
            ward,
            adoption,
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
        raise SystemExit(f"2234 validation failed: {VALIDATION}")


if __name__ == "__main__":
    main()
