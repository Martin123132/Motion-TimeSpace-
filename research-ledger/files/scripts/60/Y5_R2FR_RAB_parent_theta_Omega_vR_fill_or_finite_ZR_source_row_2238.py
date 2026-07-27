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
DOC = ROOT / "2238-Y5-R2FR-RAB-parent-theta-Omega-vR-fill-or-finite-ZR-source-row.md"
BRANCH_ID = "MTS_R2FR_PARENT_QLOC_RAB_THETA_OMEGA_VR_OR_ZR_SOURCE_2238"
START_TS = datetime.now(timezone.utc).timestamp()


SOURCE_FILES = {
    "2237_doc": ROOT / "2237-Y5-R2FR-RAB-vertical-null-presymplectic-degeneracy-or-finite-ZR-intake.md",
    "2237_validation": OUT / "P8_Y5_BRR545_2237_VALIDATION.csv",
    "2237_next": OUT / "P8_Y5_PARENT_QLOC_2237_NEXT_TARGET.csv",
    "2237_null": OUT / "P8_Y5_PARENT_QLOC_2237_PRESYMPLECTIC_NULL_CHAIN.csv",
    "2237_kinetic": OUT / "P8_Y5_PARENT_QLOC_2237_KINETIC_TERM_CONTRADICTION.csv",
    "1565_doc": ROOT / "1565-Y5-RAB-parent-theta-Omega-vR-fill-or-finite-ZR-source-row.md",
    "1565_validation": OUT / "P8_Y5_BRR545_1565_VALIDATION.csv",
    "1565_source": OUT / "P8_Y5_PARENT_QLOC_1565_SOURCE_REGISTER.csv",
    "1565_parent_block": OUT / "P8_Y5_PARENT_QLOC_1565_PARENT_BLOCK_CANDIDATE.csv",
    "1565_theta": OUT / "P8_Y5_PARENT_QLOC_1565_THETA_OMEGA_FILL.csv",
    "1565_vr": OUT / "P8_Y5_PARENT_QLOC_1565_VR_TANGENCY_AUDIT.csv",
    "1565_elim": OUT / "P8_Y5_PARENT_QLOC_1565_SECOND_CLASS_ELIMINATION_CONDITIONS.csv",
    "1565_intake": OUT / "P8_Y5_PARENT_QLOC_1565_FINITE_ZR_SOURCE_ROW_INTAKE.csv",
    "1565_runner": OUT / "P8_Y5_PARENT_QLOC_1565_RUNNER_NONCLAIM.csv",
    "1565_claim": OUT / "P8_Y5_PARENT_QLOC_1565_CLAIM_GATE.csv",
    "1565_decision": OUT / "P8_Y5_PARENT_QLOC_1565_DECISION.csv",
    "1565_next": OUT / "P8_Y5_PARENT_QLOC_1565_NEXT_TARGET.csv",
}


SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_2238_SOURCE_REGISTER.csv"
PARENT_BLOCK = OUT / "P8_Y5_PARENT_QLOC_2238_PARENT_BLOCK_CANDIDATE.csv"
THETA_OMEGA = OUT / "P8_Y5_PARENT_QLOC_2238_THETA_OMEGA_FILL.csv"
VR_TANGENCY = OUT / "P8_Y5_PARENT_QLOC_2238_VR_TANGENCY_AUDIT.csv"
SECOND_CLASS = OUT / "P8_Y5_PARENT_QLOC_2238_SECOND_CLASS_ELIMINATION_CONDITIONS.csv"
FINITE_INTAKE = OUT / "P8_Y5_PARENT_QLOC_2238_FINITE_ZR_SOURCE_ROW_INTAKE.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_2238_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_2238_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_2238_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_2238_NEXT_TARGET.csv"
BRANCH_COPIES = OUT / "P8_Y5_PARENT_QLOC_2238_BRANCH_COPIES.csv"
VALIDATION = OUT / "P8_Y5_BRR545_2238_VALIDATION.csv"


COPY_TARGETS = {
    "queue": QUEUE / "JR2238_THETA_OMEGA_VR_OR_ZR_SOURCE_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "theta_Omega_vR_or_ZR_source_nonclaim_2238.csv",
    "beta_docs": BETA_DOCS / "THETA_OMEGA_VR_OR_ZR_SOURCE_2238_NONCLAIM.csv",
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
        "1564-Y5-RAB-vertical-null-presymplectic-degeneracy-or-finite-ZR-intake.md",
        "2237-Y5-R2FR-RAB-vertical-null-presymplectic-degeneracy-or-finite-ZR-intake.md",
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
        "scripts/Y5_RAB_parent_theta_Omega_vR_fill_or_finite_ZR_source_row.py",
        "scripts/Y5_R2FR_RAB_parent_theta_Omega_vR_fill_or_finite_ZR_source_row_2238.py",
    ),
    (
        "scripts/Y5_RAB_source_boundary_readout_protection_or_finite_ZR_validator.py",
        "scripts/Y5_R2FR_RAB_source_boundary_readout_protection_or_finite_ZR_validator_2239.py",
    ),
    (
        "NEXT_1566_SOURCE_BOUNDARY_READOUT_PROTECTION_OR_FINITE_ZR_VALIDATOR",
        "NEXT_2239_SOURCE_BOUNDARY_READOUT_PROTECTION_OR_FINITE_ZR_VALIDATOR",
    ),
    ("P8_Y5_PARENT_QLOC_1564_", "P8_Y5_PARENT_QLOC_2237_"),
    ("P8_Y5_PARENT_QLOC_1563_", "P8_Y5_PARENT_QLOC_2236_"),
    ("P8_Y5_PARENT_QLOC_1562_", "P8_Y5_PARENT_QLOC_2235_"),
    ("NEXT_1566", "NEXT_2239"),
    ("NEXT1565", "NEXT2238"),
    ("PB1565", "PB2238"),
    ("TO1565", "TO2238"),
    ("VR1565", "VR2238"),
    ("ELIM1565", "ELIM2238"),
    ("INTAKE1565", "INTAKE2238"),
    ("RUN1565", "RUN2238"),
    ("GATE1565", "GATE2238"),
    ("DEC1565", "DEC2238"),
    ("VAL1565", "VAL2238"),
]


GENERATED = [
    SOURCE_REGISTER,
    PARENT_BLOCK,
    THETA_OMEGA,
    VR_TANGENCY,
    SECOND_CLASS,
    FINITE_INTAKE,
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


def formalization_2238_artifacts_absent() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(
        path.is_file()
        and "2238" in path.name
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
        role = "current R2FR vertical-null handoff" if key.startswith("2237") else "older theta/Omega/vR/fallback evidence"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC2238_{index}_{key}",
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


def intake_paths_exist() -> bool:
    return all(resolve_project_path(row["folder_or_file"]).exists() for row in read_csv(FINITE_INTAKE))


def copy_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, target in COPY_TARGETS.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SECOND_CLASS, target)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": copy_id,
                "source_path": rel(SECOND_CLASS),
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
    parent_block: list[dict[str, Any]],
    theta: list[dict[str, Any]],
    vr: list[dict[str, Any]],
    second_class: list[dict[str, Any]],
    intake: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    claim: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 2238 - Y5/R2FR R_AB Parent Theta/Omega/v_R Fill or Finite Z_R Source Row",
            "## Verdict\n"
            "- 2238 imports the old `1565` theta/Omega/v_R checkpoint into the current R2FR chain after `2237` exposed the exact vertical-null theorem contract.\n"
            "- A real piece is filled: if the `R_AB,Lambda_R` sector is a parent-signed algebraic auxiliary block with no derivative grammar, then `theta_R=0`, `Omega_R=0`, and `Pi_R^n=0` at tree level.\n"
            "- This is not a first-class vertical gauge proof: pure `v_R: delta R_AB=eta_AB, delta q=0` fails compatibility-surface tangency, and compatibility-preserving shifts are not q-vertical.\n"
            "- The honest route is now second-class elimination plus source/boundary/readout/operator protection, or finite `Z_R/q_R` source-row intake.\n"
            "- No `Z_R=0`, `q_R=0`, local GR/Newton, R10, PPN, clock, or orbital claim is made.",
            "## Source Register\n"
            + md_table(source, ["source_id", "source_path", "path_exists", "validation_overall_pass", "role"]),
            "## Parent Block Candidate\n"
            + md_table(parent_block, ["block_id", "candidate_object", "role", "what_it_buys", "status", "blocking_gap"]),
            "## Theta/Omega Fill\n"
            + md_table(theta, ["fill_id", "candidate_value", "derivation", "status", "meaning"]),
            "## v_R Tangency Audit\n"
            + md_table(vr, ["tangency_id", "test", "calculation", "status", "meaning"]),
            "## Second-Class Elimination Conditions\n"
            + md_table(second_class, ["elimination_id", "variation_or_clause", "result", "status", "blocking_gap"]),
            "## Strict Finite Z_R Intake Requirements\n"
            + md_table(intake, ["intake_id", "folder_or_file", "rows_found", "status", "required_before_scoring"]),
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
            "This is a proper forward step. We did not get an off-shell gauge-null `v_R`, but we did isolate a mathematically clean auxiliary sector: no derivatives means no `theta_R`, no `Omega_R`, and no normal momentum at tree level. The next gate should stop asking for first-class magic and instead prove the four protections needed for second-class elimination: source silence, boundary silence, readout stability, and operator exclusion. If those fail, finite `Z_R/q_R` is not an embarrassment; it becomes the disciplined empirical fallback.",
            "",
        ]
    )


def validation_rows(generated_paths: list[Path]) -> list[dict[str, Any]]:
    parent_block = read_csv(PARENT_BLOCK)
    theta = read_csv(THETA_OMEGA)
    vr = read_csv(VR_TANGENCY)
    second_class = read_csv(SECOND_CLASS)
    intake = read_csv(FINITE_INTAKE)
    runner = read_csv(RUNNER)
    claim = read_csv(CLAIM_GATE)
    decision = read_csv(DECISION)
    next_target = read_csv(NEXT_TARGET)
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2238_00_sources_exist",
            "result": "PASS" if all(path.exists() for path in SOURCE_FILES.values()) and source_register_paths_exist() else "FAIL",
            "detail": "all direct and registered 2238 source paths exist",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2238_01_prior_validations",
            "result": "PASS" if validation_pass(SOURCE_FILES["2237_validation"]) and validation_pass(SOURCE_FILES["1565_validation"]) else "FAIL",
            "detail": "2237 and 1565 validations pass overall",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2238_02_parent_block_conditional",
            "result": "PASS" if any(row.get("status") == "PARTIAL_FILL_ONLY" for row in parent_block) else "FAIL",
            "detail": "parent block is partial fill only",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2238_03_theta_omega_conditional",
            "result": "PASS"
            if any(row.get("candidate_value") == "theta_R = 0" and row.get("status").startswith("EXACT_IF") for row in theta)
            and any(row.get("candidate_value") == "Omega_R = delta theta_R = 0" and row.get("status").startswith("EXACT_IF") for row in theta)
            else "FAIL",
            "detail": "theta/Omega zero is conditional",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2238_04_vR_not_gauge",
            "result": "PASS"
            if any(row.get("status") == "FAILS_OFF_SHELL_FIRST_CLASS_TANGENCY" for row in vr)
            and any(row.get("status") == "DEMOTE_TO_SECOND_CLASS_ELIMINATION_ROUTE" for row in vr)
            else "FAIL",
            "detail": "v_R first-class promotion rejected",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2238_05_second_class_conditions",
            "result": "PASS"
            if any(row.get("status") == "PASS_ONLY_IF_SOURCES_ZERO" for row in second_class)
            and any(row.get("status") == "EXACT_CONDITIONAL_NOT_PARENT_SIGNED" for row in second_class)
            else "FAIL",
            "detail": "second-class route records source-zero condition",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2238_06_requirements_staged",
            "result": "PASS" if any(row.get("status") == "STRICT_REQUIREMENTS_STAGED_NONCLAIM" for row in intake) else "FAIL",
            "detail": "strict finite-ZR intake requirements staged",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2238_07_no_accepted_rows",
            "result": "PASS" if any(row.get("status") == "NO_ACCEPTED_ROWS" and row.get("rows_found") == "0" for row in intake) else "FAIL",
            "detail": "finite intake has no accepted rows",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2238_08_runner_blocks_claim",
            "result": "PASS" if any(row.get("current_status") == "BLOCKED_NO_CLAIM" for row in runner) else "FAIL",
            "detail": "runner blocks local claim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2238_09_claim_gates",
            "result": "PASS" if all("BLOCKED" in row.get("status", "") or row.get("status", "").startswith("PASS") for row in claim) else "FAIL",
            "detail": "all claim gates remain blocked",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2238_10_path_fields",
            "result": "PASS"
            if delimited_paths_exist([PARENT_BLOCK, THETA_OMEGA, VR_TANGENCY, SECOND_CLASS, CLAIM_GATE], ["source_paths"])
            and intake_paths_exist()
            else "FAIL",
            "detail": "all source path fields and finite-intake files/folders resolve locally",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2238_11_decision_next",
            "result": "PASS" if any(row.get("result") == "NEXT_2239_SOURCE_BOUNDARY_READOUT_PROTECTION_OR_FINITE_ZR_VALIDATOR" for row in decision) else "FAIL",
            "detail": "decision selects source/boundary/readout protection or finite Z_R validator",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2238_12_next_target",
            "result": "PASS" if next_target[0]["next_target"].startswith("2239-Y5-R2FR-RAB-source-boundary-readout-protection") else "FAIL",
            "detail": "next target is current-numbered source/boundary/readout protection validator",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2238_13_csv_parse",
            "result": "PASS" if all(parse_csv(path) for path in generated_paths) else "FAIL",
            "detail": "all generated 2238 CSVs parse cleanly",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2238_14_claim_flags_false",
            "result": "PASS" if generated_flags_false(generated_paths) else "FAIL",
            "detail": "all generated prediction/claim flags remain false",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2238_15_branch_copies",
            "result": "PASS" if all(row["copied"] == "True" and row["parse_ok"] == "True" for row in read_csv(BRANCH_COPIES)) else "FAIL",
            "detail": "branch/quarantine nonclaim copies written",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2238_16_pycache_absent",
            "result": "PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after run",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2238_17_formalization_no_2238",
            "result": "PASS" if formalization_2238_artifacts_absent() else "FAIL",
            "detail": "formalization-workbench has no non-venv 2238 artifacts",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2238_18_formalization_untouched",
            "result": "PASS" if formalization_untouched_since_start() else "FAIL",
            "detail": "formalization-workbench untouched during 2238 run",
        },
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2238_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2238 records partial theta/Omega auxiliary fill, rejects first-class v_R promotion, and selects source/boundary/readout protection or finite Z_R validation next",
        }
    )
    return rows


def main() -> None:
    source = source_rows()
    parent_block = transform_old_csv(SOURCE_FILES["1565_parent_block"])
    theta = transform_old_csv(SOURCE_FILES["1565_theta"])
    vr = transform_old_csv(SOURCE_FILES["1565_vr"])
    second_class = transform_old_csv(SOURCE_FILES["1565_elim"])
    intake = transform_old_csv(SOURCE_FILES["1565_intake"])
    runner = transform_old_csv(SOURCE_FILES["1565_runner"])
    claim = transform_old_csv(SOURCE_FILES["1565_claim"])
    decision = transform_old_csv(SOURCE_FILES["1565_decision"])
    next_target = transform_old_csv(SOURCE_FILES["1565_next"])

    write_csv(SOURCE_REGISTER, source)
    write_csv(PARENT_BLOCK, parent_block)
    write_csv(THETA_OMEGA, theta)
    write_csv(VR_TANGENCY, vr)
    write_csv(SECOND_CLASS, second_class)
    write_csv(FINITE_INTAKE, intake)
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
            parent_block,
            theta,
            vr,
            second_class,
            intake,
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
        raise SystemExit(f"2238 validation failed: {VALIDATION}")


if __name__ == "__main__":
    main()
